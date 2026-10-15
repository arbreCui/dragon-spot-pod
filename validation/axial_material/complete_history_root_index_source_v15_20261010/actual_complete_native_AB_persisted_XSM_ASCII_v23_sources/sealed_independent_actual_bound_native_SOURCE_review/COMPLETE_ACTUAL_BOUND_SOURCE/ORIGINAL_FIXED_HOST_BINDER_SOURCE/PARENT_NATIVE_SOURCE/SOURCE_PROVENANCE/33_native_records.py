"""Generic byte-only native LCM ASCII decoding; no physics targets or I/O."""
from __future__ import annotations

import re
import numpy as np

HEADER = re.compile(r'^->\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+<-\s*(\d{8})?\s*$')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode(raw):
    require(type(raw) is bytes and raw, 'empty/non-byte native export')
    lines = raw.decode('ascii').splitlines()
    nodes, records, cursor, ended = {}, {}, 0, False
    while cursor < len(lines):
        header = HEADER.fullmatch(lines[cursor])
        require(header is not None, f'invalid native header at line {cursor + 1}')
        cursor += 1
        level, flags, kind, count = map(int, header.groups()[:4])
        index = int(header[5]) if header[5] else None
        if level < 0:
            require(flags == kind == count == 0 and index is None, 'invalid closing header')
            for k in list(nodes):
                if k >= -level:
                    del nodes[k]
            if level == -1 and cursor == len(lines):
                ended = True
            continue
        require(level > 0 and flags in (0, 12), 'unsupported native level/flags')
        for k in list(nodes):
            if k >= level:
                del nodes[k]
        if flags == 12:
            require(index is None and cursor < len(lines), 'invalid named record')
            name = lines[cursor].strip()
            cursor += 1
            require(name and not HEADER.fullmatch(name), 'missing native name')
        else:
            require(index is not None and index > 0, 'missing list index')
            name = index
        path = tuple(nodes[k] for k in sorted(nodes)) + (name,)
        require(path not in records, f'duplicate record {path}')
        if kind in (0, 10, 99):
            require((kind == 0 and count == -1) or (kind == 10 and count >= 0)
                    or (kind == 99 and count == 0), 'invalid native directory/list')
            value = count
            if kind != 99:
                nodes[level] = name
        elif kind in (1, 2, 4):
            require(count >= 0, 'negative payload length')
            payload = []
            while len(payload) < count:
                require(cursor < len(lines) and not HEADER.fullmatch(lines[cursor]), 'truncated numeric record')
                tokens = lines[cursor].split()
                cursor += 1
                require(len(payload) + len(tokens) <= count, 'numeric payload overflow')
                payload.extend(int(v) if kind == 1 else float(v.replace('D', 'E').replace('d', 'e')) for v in tokens)
            require(np.isfinite(payload).all(), f'nonfinite record {path}')
            value = tuple(payload)
        elif kind == 3:
            require(count >= 0, 'negative string length')
            widths = []
            while len(widths) < count:
                require(cursor < len(lines) and not HEADER.fullmatch(lines[cursor]), 'truncated string sizes')
                widths.extend(int(v) for v in lines[cursor].split())
                cursor += 1
            require(len(widths) == count and all(n == 4 for n in widths), 'non-four-character string chunks')
            content = ''
            while len(content) < 4 * count:
                require(cursor < len(lines) and not HEADER.fullmatch(lines[cursor]), 'truncated native string')
                content += lines[cursor]
                cursor += 1
            require(not content[4 * count:].strip(), 'native string overflow')
            value = content[:4 * count].rstrip()
        else:
            raise ValueError('unsupported native type')
        records[path] = (kind, value)
    require(ended, 'native export has no terminal closing header')
    return records


def data(records, path, kind=None):
    require(path in records, f'missing record {path}')
    k, value = records[path]
    require(kind is None or k == kind, f'wrong type {path}')
    return value


def macro(raw, groups, mixtures):
    records = decode(raw)
    require(data(records, ('SIGNATURE',), 3) == 'L_MACROLIB', 'not a native Macrolib')
    state = data(records, ('STATE-VECTOR',), 1)
    require(len(state) == 40 and state[:2] == (groups, mixtures), 'Macrolib dimensions differ')
    require(data(records, ('GROUP',), 10) == groups, 'group-list dimension differs')
    rows = {}
    for g in range(1, groups + 1):
        require(data(records, ('GROUP', g), 0) == -1, 'missing populated group')
        rows[g] = {p[2]: v[1] for p, v in records.items() if len(p) == 3 and p[:2] == ('GROUP', g)}
    require({p[1] for p in records if len(p) >= 2 and p[0] == 'GROUP'} == set(rows), 'unexpected group index')
    return {'records': records, 'root': {p[0]: v[1] for p, v in records.items() if len(p) == 1},
            'rows': rows, 'groups': groups, 'mixtures': mixtures}


def field(parsed, name):
    rows = [parsed['rows'][g].get(name) for g in range(1, parsed['groups'] + 1)]
    require(all(a is not None and len(a) == parsed['mixtures'] for a in rows), 'missing/malformed macro ' + name)
    a = np.asarray(rows, dtype=float).T
    require(np.isfinite(a).all(), 'nonfinite macro ' + name)
    return a


def scatter(parsed, order):
    nm, ng = parsed['mixtures'], parsed['groups']
    result = np.zeros((nm, ng, ng))
    suffix = f'{order:02d}'
    for target in range(ng):
        row = parsed['rows'][target + 1]
        arrays = [row.get(n + suffix) for n in ('NJJS', 'IJJS', 'IPOS', 'SCAT')]
        require(all(a is not None for a in arrays), 'missing sparse scattering')
        counts, tops, offsets, values = arrays
        require(len(counts) == len(tops) == len(offsets) == nm, 'sparse mixture dimensions differ')
        cursor = 0
        for m, (count, top, offset) in enumerate(zip(counts, tops, offsets)):
            require(all(type(v) is int for v in (count, top, offset)) and 0 <= count <= ng
                    and (count == 0 or count <= top <= ng) and offset == cursor + 1, 'invalid sparse span')
            require(cursor + count <= len(values), 'truncated sparse scattering')
            for source in range(top - 1, top - count - 1, -1):
                result[m, target, source] = values[cursor]
                cursor += 1
        require(cursor == len(values), 'unused sparse scattering')
    require(np.isfinite(result).all(), 'nonfinite scattering')
    return result


def cpo_scatter(fields, order, groups=33):
    suffix = f'{order:02d}'
    counts, tops, values = (fields[n + suffix] for n in ('NJJS', 'IJJS', 'SCAT'))
    require(len(counts) == len(tops) == groups, 'CPO scattering dimensions differ')
    result = np.zeros((groups, groups))
    cursor = 0
    for t, (count, top) in enumerate(zip(counts, tops)):
        require(type(count) is int and type(top) is int and 0 <= count <= groups
                and (count == 0 or count <= top <= groups), 'bad CPO scattering span')
        for s in range(top - 1, top - count - 1, -1):
            require(cursor < len(values), 'truncated CPO scattering')
            result[t, s] = values[cursor]
            cursor += 1
    require(cursor == len(values) and np.isfinite(result).all(), 'invalid CPO sparse values')
    return result

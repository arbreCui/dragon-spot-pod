"""Bounded native LCM ASCII reader, compatible with pinned native_records.decode.

All records are validated, including discarded numeric values and duplicate keys.
The caller selects retained records; no physical value is synthesized here.
The source is a binary line iterator (not a pathname); this module performs no I/O.
"""
import math
import re

HEADER = re.compile(r'^->\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+<-\s*(\d{8})?\s*$')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode_stream(source, select=lambda path, kind, count: True):
    lines = iter(source)
    line_number = 0

    def next_line():
        nonlocal line_number
        raw = next(lines, None)
        if raw is None:
            return None
        require(type(raw) is bytes and len(raw) <= 1024**2, 'bounded binary line required')
        line_number += 1
        return raw.decode('ascii').rstrip('\r\n')

    def payload_line(message):
        value = next_line()
        require(value is not None and not HEADER.fullmatch(value), message)
        return value

    nodes, seen, records = {}, set(), {}
    last_closing = False
    scalar_count = 0
    while (line := next_line()) is not None:
        last_closing = False
        header = HEADER.fullmatch(line)
        require(header is not None, f'invalid native header at line {line_number}')
        level, flags, kind, count = map(int, header.groups()[:4])
        index = int(header[5]) if header[5] else None
        if level < 0:
            require(flags == kind == count == 0 and index is None, 'invalid closing header')
            for k in list(nodes):
                if k >= -level:
                    del nodes[k]
            last_closing = level == -1
            continue
        require(level > 0 and flags in (0, 12), 'unsupported native level/flags')
        for k in list(nodes):
            if k >= level:
                del nodes[k]
        if flags == 12:
            require(index is None, 'invalid named record')
            name = payload_line('invalid named record').strip()
            require(name, 'missing native name')
        else:
            require(index is not None and index > 0, 'missing list index')
            name = index
        path = tuple(nodes[k] for k in sorted(nodes)) + (name,)
        require(path not in seen, f'duplicate record {path}')
        seen.add(path)
        require(len(seen) <= 2_000_000, 'record-key count limit')
        keep = bool(select(path, kind, count))
        if kind in (0, 10, 99):
            require((kind == 0 and count == -1) or (kind == 10 and count >= 0)
                    or (kind == 99 and count == 0), 'invalid native directory/list')
            value = count
            if kind != 99:
                nodes[level] = name
        elif kind in (1, 2, 4):
            require(0 <= count <= 100_000_000, 'invalid/bounded payload length')
            consumed, payload = 0, []
            while consumed < count:
                tokens = payload_line('truncated numeric record').split()
                require(consumed + len(tokens) <= count, 'numeric payload overflow')
                for token in tokens:
                    value = int(token) if kind == 1 else float(token.replace('D', 'E').replace('d', 'e'))
                    require(math.isfinite(value), f'nonfinite record {path}')
                    if keep:
                        payload.append(value)
                consumed += len(tokens)
            scalar_count += consumed
            value = tuple(payload) if keep else None
        elif kind == 3:
            require(0 <= count <= 1_000_000, 'invalid/bounded string length')
            consumed = 0
            while consumed < count:
                widths = [int(v) for v in payload_line('truncated string sizes').split()]
                require(consumed + len(widths) <= count and all(n == 4 for n in widths),
                        'non-four-character string chunks')
                consumed += len(widths)
            content = ''
            while len(content) < 4 * count:
                content += payload_line('truncated native string')
            require(not content[4 * count:].strip(), 'native string overflow')
            value = content[:4 * count].rstrip() if keep else None
        else:
            raise ValueError('unsupported native type')
        if keep:
            records[path] = (kind, value)
    require(last_closing, 'native export has no terminal closing header')
    return records, {'lines': line_number, 'all_records_validated': len(seen),
                     'retained_records': len(records), 'numeric_values_validated': scalar_count}


CHANNELS = {'NG', 'NA', 'NFTOT', 'NUSIGF'}


def reaction_selection(path, kind, count):
    """Retain root metadata, isotope channels, and independent/embedded macro channels."""
    if len(path) == 1 or kind in (0, 10, 99):
        return True
    if path[0] == 'ISOTOPESLIST':
        return len(path) == 3 and (path[-1] in CHANNELS or kind in (1, 3))
    if path[0] == 'MACROLIB':
        return len(path) == 2 or (len(path) == 4 and path[-1] in CHANNELS)
    if path[0] == 'GROUP':
        return len(path) == 3 and path[-1] in CHANNELS
    return False

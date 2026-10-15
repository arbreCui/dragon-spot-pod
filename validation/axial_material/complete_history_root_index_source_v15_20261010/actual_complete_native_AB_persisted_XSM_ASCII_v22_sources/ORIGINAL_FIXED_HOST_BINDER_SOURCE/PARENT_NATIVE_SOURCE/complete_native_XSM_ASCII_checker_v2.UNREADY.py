"""Root-only, UNREADY stdlib byte checker. No transport or native API calls.

Reads original Ganlib XSM bytes and every original ROOT/MACROLIB ASCII record.
Native persisted bytes are distinct from the historical process's RAM bytes.
Root must bind exact inputs and run under the unchanged genuine supervisor.
This file has only been parsed as SOURCE; it has never been imported/executed.
"""
import argparse
from contextlib import ExitStack
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import stat
import struct
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
ROOT_BOUND_BINDING_SHA256 = None
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
            joint_archive_bytes=2*2**30, history_bytes=96*2**30,
            free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
HEADER = re.compile(rb'^->\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+<-\s*(\d{8})?\s*$')
MAGIC = b'AXMAT_FULL_TYPED_LCM_V1\x00'
FALSE = dict(historical_native_RAM_bits_verified=False, original_XSM_memory_bits_verified=False,
             reaction_multiplicity_qualified=False, TRANC_semantics_qualified=False,
             physical_neutron_balance_qualified=False,
             coupled_370group_reference_qualified=False, scientific_accuracy_qualified=False,
             AAA_accuracy_qualified=False, ABA_admitted=False,
             native_transport_executed=False, whole_combined_build_or_INPUT_qualified=False)


def require(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def strict_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'duplicate metadata key')
            result[key] = value
        return result
    def bad(value):
        raise ValueError('nonfinite JSON literal ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def pin(path):
    path = Path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            'ordinary unaliased pinned file required')
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == identity(before), 'open identity changed')
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        require(identity(os.fstat(stream.fileno())) == identity(before), 'full EOF identity changed')
    require(identity(path.lstat()) == identity(before), 'path identity changed')
    return dict(path=str(path), sha256=digest, size_bytes=before.st_size, identity=identity(before))


def exact_pin(expected):
    require(type(expected) is dict and pin(expected['path']) == expected, 'exact full EOF/SHA/7ID pin differs')


def line_json(stream, value):
    stream.write(json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False) + '\n')


class Budget:
    def __init__(self, output):
        self.started, self.output = time.monotonic(), output
    def check(self):
        require(time.monotonic() - self.started < CAPS['stage_seconds'], 'original600-second child bound')
        total = 0
        for p in self.output.rglob('*'):
            s = p.lstat()
            require(not stat.S_ISLNK(s.st_mode), 'output aliases forbidden')
            if stat.S_ISREG(s.st_mode):
                total += s.st_size
        require(total < CAPS['joint_archive_bytes'], 'child output already exceeds original joint2GiB')
        # Root genuine guard additionally counts all declared Source/H/O/E roots.


class DiskRecords:
    """Full path index on disk, with bounded SQLite cache; never a Python tree."""
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('PRAGMA cache_size=-8192')
        self.db.execute('PRAGMA mmap_size=0')
        self.db.execute('PRAGMA temp_store=FILE')
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('CREATE TABLE records(key TEXT PRIMARY KEY, ordinal INTEGER UNIQUE, api_key TEXT UNIQUE, row TEXT, micro_ordinal INTEGER UNIQUE, macro_ordinal INTEGER UNIQUE)')
        self.count = 0
    @staticmethod
    def key(path):
        return json.dumps(list(path), ensure_ascii=True, separators=(',', ':'))
    def __len__(self):
        return self.count
    def __contains__(self, path):
        return self.db.execute('SELECT 1 FROM records WHERE key=?', (self.key(path),)).fetchone() is not None
    def __getitem__(self, path):
        row = self.get(path)
        if row is None:
            raise KeyError(path)
        return row
    def get(self, path):
        row = self.db.execute('SELECT row FROM records WHERE key=?', (self.key(path),)).fetchone()
        return None if row is None else strict_json(row[0])
    def insert(self, path, row, api_rank):
        self.db.execute('INSERT INTO records(key,ordinal,api_key,row) VALUES(?,?,?,?)',
            (self.key(path), self.count, '/'.join(f'{i:010d}' for i in api_rank),
             json.dumps(row, separators=(',', ':'), allow_nan=False)))
        self.count += 1
    def iter_rows(self, prefix=(), api=False, absent_label=None):
        clauses, args = [], []
        if prefix:
            text = self.key(prefix)[:-1]+','
            clauses.append('substr(key,1,?)=?')
            args.extend((len(text), text))
        if absent_label is not None:
            require(absent_label in ('MICROLIB', 'MACROLIB'), 'fixed ASCII ordinal column')
            clauses.append(('micro_ordinal' if absent_label == 'MICROLIB' else 'macro_ordinal')+' IS NULL')
        sql = 'SELECT row FROM records'+(' WHERE '+' AND '.join(clauses) if clauses else '')
        # api_key is the original Ganlib-derived sibling rank, never field-name sorting.
        sql += ' ORDER BY '+('api_key' if api else 'ordinal')
        for row in self.db.execute(sql, args):
            yield strict_json(row[0])
    def set_ascii_ordinal(self, path, label, ordinal):
        require(label in ('MICROLIB', 'MACROLIB'), 'fixed ASCII ordinal column')
        column = 'micro_ordinal' if label == 'MICROLIB' else 'macro_ordinal'
        cursor = self.db.execute(f'UPDATE records SET {column}=? WHERE key=? AND {column} IS NULL', (ordinal, self.key(path)))
        require(cursor.rowcount == 1, 'duplicate original ASCII typed path or missing native path')
    def checkpoint(self):
        self.db.commit()
    def close(self):
        self.db.commit()
        self.db.close()


class ReadOnlyFileBytes:
    """Bounded pread cache, matching KDI byte offsets without whole-file mmap."""
    def __init__(self, stream):
        self.fd = stream.fileno()
        self.size = os.fstat(self.fd).st_size
        self.cache_begin, self.cache = -1, b''
    def __len__(self):
        return self.size
    def __getitem__(self, span):
        require(type(span) is slice and span.step is None and type(span.start) is int
                and type(span.stop) is int and 0 <= span.start <= span.stop <= self.size,
                'exact bounded native byte slice required')
        begin, end = span.start, span.stop
        if begin == end:
            return b''
        require(end-begin <= 2**20, 'native byte reads must use bounded1MiB chunks')
        if not self.cache_begin <= begin <= end <= self.cache_begin+len(self.cache):
            self.cache_begin = begin
            self.cache = os.pread(self.fd, min(2**20, self.size-begin), begin)
            require(len(self.cache) == min(2**20, self.size-begin), 'truncated original read-only pread')
        return self.cache[begin-self.cache_begin:end-self.cache_begin]


class XSM:
    """xsmdir/xsmlid/xsmlen/lcmlel layout, without calling those APIs."""
    def __init__(self, data, physical, payload, budget, records):
        self.data, self.physical, self.payload, self.budget = data, physical, payload, budget
        require(self.read(0, 3)[:4] == b'$XSM', 'little-endian four-byte-word XSM required')
        self.high_address, self.root = self.ints(1, 2)
        self.rows, self.active = records, set()
        self.directory_count = self.extent_count = 0

    def read(self, offset, words):
        require(type(offset) is int and type(words) is int and offset >= 0 and words >= 0
                and (offset + words)*4 <= len(self.data), 'XSM pointer/count outside actual file')
        return self.data[offset*4:(offset+words)*4]

    def ints(self, offset, count):
        return struct.unpack(f'<{count}i', self.read(offset, count))

    def directory(self, start, owner):
        seen, entries, names, offset = set(), [], set(), start
        self.directory_count += 1
        while offset not in seen:
            require(len(seen) < 2_000_000, 'native extent safety bound')
            seen.add(offset)
            header = self.read(offset, 8)
            magic, capacity, count, following, parent = struct.unpack_from('<4s4i', header)
            require(magic == b'$$$$' and 0 <= count <= capacity <= 30, 'invalid native directory extent')
            # xsmdir imports no array when nmt=0. Preserve all available unused
            # bytes, but do not invent a required payload beyond actual EOF.
            available = min(6*capacity, max(0, len(self.data)//4-offset-8))
            require(count == 0 or available == 6*capacity, 'truncated populated directory arrays')
            raw = self.read(offset + 8, available)
            line_json(self.physical, dict(entry='physical_directory_extent', owner=list(owner),
                offset_words=offset, capacity=capacity, count=count, following_words=following,
                parent_words=parent, raw_header_hex=header.hex(), raw_array_hex=raw.hex(),
                available_array_words=available, allocated_array_words=6*capacity,
                raw_sha256=hashlib.sha256(header+raw).hexdigest()))
            self.extent_count += 1
            for i in range(count):
                at, words, kind = [struct.unpack_from('<i', raw, 4*(k*capacity+i))[0] for k in range(3)]
                name_raw = raw[12*(capacity+i):12*(capacity+i+1)]
                # xsmdir trims trailing spaces and terminates at the first NUL.
                name = name_raw.split(b'\0', 1)[0].rstrip(b' ').decode('ascii')
                line_json(self.physical, dict(entry='physical_native_slot', owner=list(owner),
                    extent_words=offset, slot_zero_based=i, original_name_bytes_hex=name_raw.hex(),
                    name=name, value_offset_words=at, stored_word_count=words, kind=kind,
                    logical_tombstone=(name == '***DEL***')))
                if name == '***DEL***':
                    entries.append(None)  # Kept above physically; not a current LCM record.
                    continue
                require(name and name not in names, 'duplicate/blank native directory name')
                names.add(name)
                entries.append(dict(name=name, offset_words=at, words=words, kind=kind,
                                    extent_words=offset, slot_zero_based=i))
            offset = following
        require(offset == start, 'native directory cycle does not close at origin')
        return entries

    def emit(self, path, entry, api_rank):
        require(path not in self.rows and len(self.rows) < 2_000_000, 'duplicate/full native record bound')
        kind, words, offset = entry['kind'], entry['words'], entry['offset_words']
        require(kind in (0, 1, 2, 3, 4, 5, 6, 10, 99), 'unknown native record kind; no filtering')
        if kind == 0:
            require(words == -1, 'native scalar directory length must be -1')
            count, payload_words = -1, 0
        elif kind == 99:
            require(words == 0, 'native empty node count must be zero')
            count, payload_words = 0, 0
        elif kind == 10:
            require(words >= 0, 'negative native list length')
            count, payload_words = words, 0
            for at in range(0, count, 16384):
                pointer_bytes = self.read(offset+at, min(16384, count-at))
                line_json(self.physical, dict(entry='complete_native_list_pointer_array_chunk',
                    owner=list(path), original_total_pointer_count=count, offset_words=offset+at,
                    words=len(pointer_bytes)//4, original_bytes_hex=pointer_bytes.hex(),
                    original_bytes_sha256=hashlib.sha256(pointer_bytes).hexdigest()))
        else:
            require(words >= 0 and (kind not in (4, 6) or words % 2 == 0), 'invalid native word/type length')
            count = words//2 if kind in (4, 6) else words
            payload_words = words
        begin = self.payload.tell()
        digest = hashlib.sha256()
        for at in range(0, payload_words, 262144):
            raw = self.read(offset+at, min(262144, payload_words-at))
            digest.update(raw)
            self.payload.write(raw)
        row = dict(path=list(path), path_types=['str' if type(x) is str else 'int' for x in path],
            kind=kind, declared_count=count, original_word_count=words, native_offset_words=offset,
            native_physical_record_index=len(self.rows), native_payload_begin_byte=begin,
            native_payload_end_byte=self.payload.tell(), native_payload_sha256=digest.hexdigest(),
            native_slot_extent_words=entry.get('extent_words'), native_slot_zero_based=entry.get('slot_zero_based'))
        self.rows.insert(path, row, api_rank)
        if len(self.rows) % 1000 == 0:
            self.budget.check()

    def walk_table(self, start, prefix, api_prefix):
        require(start not in self.active, 'native hierarchy ancestor cycle')
        self.active.add(start)
        slots = self.directory(start, prefix)
        entries = [e for e in slots if e is not None]
        require(all(e['name'] != '***HANDLE***' for e in entries), 'reserved handle in named table')
        # xsmnxt(' ') starts after slot1; retain this separate API order.
        rotated = slots[1:]+slots[:1] if slots else []
        api_ranks = {e['name']:i for i,e in enumerate(rotated, 1) if e is not None}
        for e in entries:
            self.walk_entry(prefix+(e['name'],), e, api_prefix+(api_ranks[e['name']],))
        self.active.remove(start)

    def walk_entry(self, path, entry, api_rank):
        self.emit(path, entry, api_rank)
        if entry['kind'] == 0:
            self.walk_table(entry['offset_words'], path, api_rank)
        elif entry['kind'] == 10:
            for i in range(1, entry['words']+1):
                pointer = self.ints(entry['offset_words']+i-1, 1)[0]
                require(pointer not in self.active, 'list item ancestor cycle')
                slots = self.directory(pointer, path+(i,))
                logical = [e for e in slots if e is not None]
                if not logical:
                    item = dict(offset_words=pointer, words=0, kind=99)
                else:
                    require(len(logical) == 1 and logical[0]['name'] == '***HANDLE***',
                            'native list storage item must contain exactly reserved handle')
                    item = logical[0]
                self.active.add(pointer)
                self.walk_entry(path+(i,), item, api_rank+(i,))
                self.active.remove(pointer)

    def walk(self):
        self.walk_table(self.root, (), ())
        self.rows.checkpoint()

    def bytes_for(self, row):
        return self.read(row['native_offset_words'], row['original_word_count']) if row['kind'] not in (0, 10, 99) else b''


def typed_numeric(kind, tokens):
    data = bytearray()
    for token in tokens:
        if kind == 1:
            value = int(token)
            data.extend(str(value).encode('ascii')+b'\n')
        elif kind == 5:
            require(token in (b'T', b'F'), 'invalid original LOGICAL token')
            data.extend(struct.pack('<i', 1 if token == b'T' else 0))
        else:
            value = float(token.replace(b'D', b'E').replace(b'd', b'e'))
            require(math.isfinite(value), 'nonfinite original floating token')
            chunk = struct.pack('<d', value) if kind == 4 else struct.pack('<fd', value, value)
            require(kind == 4 or math.isfinite(struct.unpack('<f', chunk[:4])[0]), 'REAL32 overflow/nonfinite rounding')
            data.extend(chunk)
    return bytes(data)


def native_projection(kind, typed):
    if kind == 1:
        return b''.join(struct.pack('<i', int(v)) for v in typed.splitlines())
    if kind in (2, 6):
        require(len(typed) % 12 == 0, 'all rounded32/parser64 components retained')
        return b''.join(typed[i:i+4] for i in range(0, len(typed), 12))
    return typed


def compare_ascii(path, native, native_prefix, folder, label, budget, macro_saved=None):
    """Stream every original record/line/close; complete indexes stay on disk."""
    record_count = header_count = numeric_count = mismatches = 0
    physical_equal = api_equal = True
    nodes = {}
    stack = ExitStack()
    with stack:
        src = stack.enter_context(Path(path).open('rb'))
        inventory = stack.enter_context((folder/(label+'_complete_original_header_spans.jsonl')).open('x'))
        report = stack.enter_context((folder/(label+'_complete_native_bit_comparison.jsonl')).open('x'))
        orders = stack.enter_context((folder/(label+'_complete_ASCII_order.jsonl')).open('x'))
        typed_out = stack.enter_context((folder/(label+'_complete_ASCII_typed_payload.bin')).open('xb'))
        typed_out.write(MAGIC)
        physical_order = iter(native.rows.iter_rows(native_prefix))
        api_order = iter(native.rows.iter_rows(native_prefix, api=True))
        saved_index = saved_payload = None
        if macro_saved is not None:
            saved_index = stack.enter_context(Path(macro_saved['index']['path']).open('rb'))
            saved_payload = stack.enter_context(Path(macro_saved['typed']['path']).open('rb'))
            require(saved_payload.read(len(MAGIC)) == MAGIC, 'saved full macro typed format differs')
        ended = False
        while True:
            begin, raw = src.tell(), src.readline(2**20+1)
            if not raw:
                break
            require(not ended, 'original terminal root close must be final; second root forbidden')
            require(len(raw) <= 2**20, 'original complete ASCII line bound')
            match = HEADER.fullmatch(raw.rstrip(b'\r\n'))
            require(match is not None, 'invalid complete ASCII header')
            level, flags, kind, count = [int(v) for v in match.groups()[:4]]
            index = int(match[5]) if match[5] else None
            digest = hashlib.sha256(raw)
            row = dict(physical_header_index=header_count, level=level, flags=flags, kind=kind, declared_count=count)
            header_count += 1
            ended = False
            comparison = previous = None
            def payload_line():
                line = src.readline(2**20+1)
                require(bool(line) and len(line) <= 2**20 and HEADER.fullmatch(line.rstrip(b'\r\n')) is None,
                        'truncated/premature header in complete ASCII payload')
                digest.update(line)
                return line.rstrip(b'\r\n')
            if level < 0:
                require(flags == kind == count == 0 and index is None, 'invalid original close header')
                require(sorted(nodes) == list(range(1, len(nodes)+1)) and 1 <= -level <= len(nodes)+1,
                        'original close outside current contiguous export ancestry')
                for k in list(nodes):
                    if k >= -level:
                        del nodes[k]
                ended = level == -1
                row['entry'] = 'close'
            else:
                require(level > 0 and flags in (0, 12), 'original ASCII level/flags')
                for k in list(nodes):
                    if k >= level:
                        del nodes[k]
                require(sorted(nodes) == list(range(1, level)), 'original positive parent levels must be contiguous')
                if flags == 12:
                    require(index is None, 'named original header has list index')
                    name = payload_line().rstrip(b' ').decode('ascii')
                    require(bool(name), 'original named record has no name')
                else:
                    require(index is not None and index > 0, 'original list index absent')
                    name = index
                key = tuple(nodes[k] for k in sorted(nodes))+(name,)
                row.update(entry='record', record_index=record_count, path=list(key),
                           path_types=['str' if type(v) is str else 'int' for v in key])
                native_key = native_prefix+key
                nr = native.rows.get(native_key)
                require(nr is not None, 'original ASCII record absent from full native tree')
                native.rows.set_ascii_ordinal(native_key, label, record_count)
                record_count += 1
                require(nr['kind'] == kind and nr['declared_count'] == count, 'native/ASCII exact kind/count differs')
                pr, ar = next(physical_order, None), next(api_order, None)
                physical_equal = physical_equal and pr is not None and pr['path'][len(native_prefix):] == list(key)
                api_equal = api_equal and ar is not None and ar['path'][len(native_prefix):] == list(key)
                line_json(orders, dict(original_ASCII_record_index=record_count-1, path=list(key), path_types=row['path_types']))
                tbegin, native_position, equal = typed_out.tell(), 0, True
                typed_digest, native_digest, projected_digest = hashlib.sha256(), hashlib.sha256(), hashlib.sha256()
                first_mismatch_byte = None
                if saved_index is not None:
                    previous = strict_json(saved_index.readline())
                    for field in ('record_index', 'physical_header_index', 'path', 'path_types', 'level', 'flags', 'kind', 'declared_count'):
                        require(previous[field] == row[field] and type(previous[field]) is type(row[field]), 'complete saved macro index/order/type differs')
                def store_and_compare(typed, projection):
                    nonlocal native_position, equal, first_mismatch_byte
                    require(len(projection) % 4 == 0 and native_position+len(projection) <= max(0, nr['original_word_count'])*4,
                            'streamed native projection extent differs')
                    original = native.read(nr['native_offset_words']+native_position//4, len(projection)//4)
                    if original != projection:
                        equal = False
                        if first_mismatch_byte is None:
                            first_mismatch_byte = native_position+next(i for i,(a,b) in enumerate(zip(original,projection)) if a != b)
                    native_position += len(projection)
                    native_digest.update(original)
                    projected_digest.update(projection)
                    typed_digest.update(typed)
                    typed_out.write(typed)
                    if saved_payload is not None:
                        require(saved_payload.read(len(typed)) == typed, 'saved parser64/rounded32/all typed bytes differ')
                if kind in (0, 10, 99):
                    require((kind == 0 and count == -1) or (kind == 10 and count >= 0) or (kind == 99 and count == 0), 'directory/list/empty original shape')
                    if kind != 99:
                        nodes[level] = name
                elif kind == 3:
                    require(0 <= count <= 1_000_000, 'original character count')
                    widths = 0
                    while widths < count:
                        values = [int(v) for v in payload_line().split()]
                        require(widths+len(values) <= count and all(v == 4 for v in values), 'all original character widths')
                        widths += len(values)
                    content = bytearray()
                    while len(content) < 4*count:
                        content.extend(payload_line())
                    require(not bytes(content[4*count:]).strip(), 'original character payload overflow')
                    char_original = bytes(content[:4*count])
                    # Match the preserved original ASCII decoder's .rstrip()
                    # artifact only. Native CHAR bit proof uses all original
                    # words/padding; no trimming is applied to that comparison.
                    store_and_compare(char_original.rstrip(), char_original)
                elif kind in (1, 2, 4, 5, 6):
                    require(0 <= count <= 100_000_000, 'all original numeric lengths')
                    needed, consumed = count*(2 if kind == 6 else 1), 0
                    while consumed < needed:
                        tokens = payload_line().split()
                        require(consumed+len(tokens) <= needed, 'original numeric payload overflow')
                        chunk = typed_numeric(kind, tokens)
                        store_and_compare(chunk, native_projection(kind, chunk))
                        consumed += len(tokens)
                    numeric_count += consumed
                else:
                    raise ValueError('unknown original ASCII kind; cannot omit record')
                expected_bytes = 0 if kind in (0, 10, 99) else nr['original_word_count']*4
                require(native_position == expected_bytes, 'every native original value byte must be compared')
                mismatches += int(not equal)
                row.update(typed_payload_begin_byte=tbegin, typed_payload_end_byte=typed_out.tell(),
                           typed_payload_sha256=typed_digest.hexdigest())
                if previous is not None:
                    for field in ('typed_payload_begin_byte', 'typed_payload_end_byte', 'typed_payload_sha256'):
                        require(previous[field] == row[field], 'saved complete typed extent/hash differs')
                comparison = dict(original_ASCII_record=row, native_record=nr,
                    persisted_native_value_bits_equal_ASCII_export_projection=equal,
                    native_raw_bytes_sha256=native_digest.hexdigest(), ASCII_export_projection_sha256=projected_digest.hexdigest(),
                    first_mismatch_native_byte_zero_based=first_mismatch_byte,
                    comparison_kind=('raw_character_words_with_padding' if kind == 3 else
                        'native_REAL32_bits_vs_ASCII_rounded32_preserving_separate_parser64' if kind in (2, 6) else
                        'native_REAL64_bits_vs_ASCII_parser64_no_tolerance' if kind == 4 else 'exact_original_type_value'),
                    historical_RAM_bits_certified=False, no_tolerance=True, no_missing_value_fill=True)
            row.update(raw_begin_byte=begin, raw_end_byte=src.tell(), raw_span_sha256=digest.hexdigest())
            if previous is not None:
                for field in ('raw_begin_byte', 'raw_end_byte', 'raw_span_sha256'):
                    require(previous[field] == row[field], 'saved complete original macro span differs')
            line_json(inventory, row)
            if comparison is not None:
                line_json(report, comparison)
            if header_count % 1000 == 0:
                budget.check()
        require(ended and src.tell() == Path(path).stat().st_size, 'original full ASCII EOF and terminal root close')
        if saved_index is not None:
            require(saved_index.read(1) == saved_payload.read(1) == b'', 'saved complete macro EOF differs')
        physical_equal = physical_equal and next(physical_order, None) is None
        api_equal = api_equal and next(api_order, None) is None
    native.rows.checkpoint()
    # lcmexp_part1 skips named zero-length nodes; preserve every omission on disk.
    absent_count = 0
    with (folder/(label+'_complete_native_records_absent_from_original_ASCII.jsonl')).open('x') as out:
        for row in native.rows.iter_rows(native_prefix, absent_label=label):
            require(type(row['path'][-1]) is str and row['declared_count'] == 0,
                    'native/ASCII full domain differs beyond source-declared named zero-length omissions')
            line_json(out, dict(native_record=row, omission_source='lcm_c.c:lcmexp_part1 jlong!=0', hidden_or_filled=False))
            absent_count += 1
    return dict(records=record_count, physical_headers_including_all_closes=header_count, numeric_components=numeric_count,
        mismatching_native_value_bit_records=mismatches, full_record_domain_equal=(absent_count == 0),
        original_ASCII_export_omitted_native_zero_length_records=absent_count,
        native_physical_preorder_equal_original_ASCII=physical_equal, native_XSM_API_export_preorder_equal_original_ASCII=api_equal,
        all_complete_orders_preserved_on_disk=True, original_byte_and_parser_bits_preserved=True,
        all_persisted_native_value_bits_equal_ASCII=(mismatches == 0 and absent_count == 0 and physical_equal),
        original_LCM_copy_physical_record_order_verified=physical_equal,
        order_source_note='Original MAT_OUT is a LCM copy; MACRO_OUT/MICRO_OUT export memory LCM. xsmnxt initial anchor advances past first physical slot. Storage and native re-export API orders are recorded separately; no name sorting.')


def evidence(native, folder):
    def record(path, kind, count=None):
        row = native.rows.get(tuple(path))
        kinds = kind if type(kind) is tuple else (kind,)
        require(row is not None and row['kind'] in kinds, 'required original ownership/type absent')
        require(count is None or row['declared_count'] == count, 'original ownership count differs')
        return row, native.bytes_for(row)
    def integers(path, count=None):
        row, raw = record(path, 1, count)
        return row, list(struct.unpack(f'<{row["declared_count"]}i', raw))
    root_state, rstate = integers(('STATE-VECTOR',), 40)
    macro_state, mstate = integers(('MACROLIB', 'STATE-VECTOR'), 40)
    require(rstate[:5] == [8, 62, 370, 3, 1] and mstate[:4] == [370, 8, 3, 32], 'full current dimensions/transport flags differ')
    record(('ISOTOPESLIST',), 10, 62)
    record(('MACROLIB', 'GROUP'), 10, 370)
    used_row, used = record(('ISOTOPESUSED',), 3, 3*62)
    refs_row, refs = record(('ISOTOPERNAME',), 3, 3*62)
    mix_row, mixes = integers(('ISOTOPESMIX',), 62)
    dens_row, density = record(('ISOTOPESDENS',), 2, 62)
    temp_row, temperature = record(('ISOTOPESTEMP',), 2, 62)
    aliases = []  # Exactly62 scalar indices, never the complete micro tree.
    with (folder/'complete_native_isotope_region_and_all_field_evidence.jsonl').open('x') as out:
        for i in range(1, 63):
            item = native.rows[('ISOTOPESLIST', i)]
            used_name, ref = used[12*(i-1):12*i], refs[12*(i-1):12*i]
            require(1 <= mixes[i-1] <= 8, 'native isotope mixture outside eight regions')
            if item['kind'] == 99 and item['declared_count'] == 0:
                earlier = [j for j in range(i-1) if used[12*j:12*(j+1)] == used_name and aliases[j] is not None]
                resolved = aliases[earlier[0]] if earlier else None
            else:
                require(item['kind'] == 0 and item['declared_count'] == -1, 'native isotope item is neither directory nor empty')
                resolved = i
            aliases.append(resolved)
            require(resolved is not None, 'unresolved LIBIPS complete twelve-byte isotope alias')
            j = resolved-1
            require(ref == refs[12*j:12*(j+1)] and temperature[4*(i-1):4*i] == temperature[4*j:4*(j+1)], 'native alias reference/temperature bits differ')
            owner = ('ISOTOPESLIST', resolved)
            line_json(out, dict(entry='isotope_region_binding', isotope_index_one_based=i, native_item=item,
                full_alias_name_bytes_hex=used_name.hex(), reference_name_bytes_hex=ref.hex(), mixture_one_based=mixes[i-1],
                density_REAL32_bits_hex=density[4*(i-1):4*i].hex(), temperature_REAL32_bits_hex=temperature[4*(i-1):4*i].hex(),
                resolved_LIBIPS_original_index_one_based=resolved,
                named_reaction_presence={name:dict(present=owner+(name,) in native.rows,
                    native_record=native.rows.get(owner+(name,))) for name in ('NFTOT', 'NUSIGF', 'NG', 'N2N', 'N3N', 'N4N', 'TRANC', 'NTOT0', 'SIGS00', 'SIGS01', 'SIGS02')},
                reaction_multiplicity_or_transport_semantics_qualified=False))
            # Stream every resolved isotope field, including every extra/nested field.
            for field in native.rows.iter_rows(owner):
                line_json(out, dict(entry='complete_original_resolved_isotope_field', isotope_index_one_based=i,
                    resolved_original_index_one_based=resolved, original_field=field))
    findex_row, findex = integers(('MACROLIB', 'FISSIONINDEX'))
    require(len(findex) % 8 == 0, 'native fission isotope-slot matrix has nonintegral eight-region columns')
    with (folder/'complete_original_fission_slot_region_isotope_binding.jsonl').open('x') as out:
        for slot in range(len(findex)//8):
            for mix in range(1, 9):
                idx = findex[8*slot+mix-1]
                require(0 <= idx <= 62 and (idx == 0 or mixes[idx-1] == mix), 'native fission index does not bind original isotope to region')
                line_json(out, dict(original_slot_one_based=slot+1, mixture_one_based=mix, original_isotope_index=idx,
                    resolved_original_index=(None if idx == 0 else aliases[idx-1]), original_zero_is_preserved_not_synthesized=(idx == 0)))
    sparse_count = tranc_count = fission_components_count = 0
    with ExitStack() as stack:
        sparse_out = stack.enter_context((folder/'complete370x8x3_original_sparse_reference_evidence.jsonl').open('x'))
        tranc_out = stack.enter_context((folder/'complete370group_original_TRANC_evidence.jsonl').open('x'))
        fission_out = stack.enter_context((folder/'complete370group_8region_32fission_component_records.jsonl').open('x'))
        for g in range(1, 371):
            record(('MACROLIB', 'GROUP', g), 0, -1)
            for name in ('NUSIGF', 'CHI'):
                fr, unused = record(('MACROLIB', 'GROUP', g, name), (2, 4), 8*32)
                line_json(fission_out, dict(group_one_based=g, original_record=fr, full8region32component_count=256,
                    isotope_slot_vs_spectrum_component_mapping_qualified=False))
                fission_components_count += 1
            for moment in range(3):
                suffix = f'{moment:02d}'
                cr, counts = integers(('MACROLIB', 'GROUP', g, 'NJJS'+suffix), 8)
                tr, tops = integers(('MACROLIB', 'GROUP', g, 'IJJS'+suffix), 8)
                ir, offsets = integers(('MACROLIB', 'GROUP', g, 'IPOS'+suffix), 8)
                sr, unused = record(('MACROLIB', 'GROUP', g, 'SCAT'+suffix), (2, 4))
                word_stride = 2 if sr['kind'] == 4 else 1
                for m, (count, top, at) in enumerate(zip(counts, tops, offsets), 1):
                    require(0 <= count <= 370 and (count == 0 or count <= top <= 370)
                            and (count == 0 or 1 <= at and at-1+count <= sr['declared_count']), 'full original active sparse span outside native payload')
                    selected = b'' if count == 0 else native.read(sr['native_offset_words']+word_stride*(at-1), word_stride*count)
                    line_json(sparse_out, dict(group_one_based=g, region_one_based=m, moment_zero_based=moment,
                        original_count=count, original_top_one_based=top, original_offset_one_based=at,
                        original_NJJS=cr, original_IJJS=tr, original_IPOS=ir, original_SCAT=sr,
                        native_original_selected_span_sha256=hashlib.sha256(selected).hexdigest(),
                        original_count_zero_pointer_is_preserved_without_dereference=(count == 0),
                        no_sparse_repacking=True, all_padding_preserved_in_complete_payload=True))
                    sparse_count += 1
            key = ('MACROLIB', 'GROUP', g, 'TRANC')
            row = native.rows.get(key)
            require(row is None or row['kind'] in (2, 4) and row['declared_count'] == 8, 'native TRANC full eight-region type/count')
            line_json(tranc_out, dict(group_one_based=g, original_TRANC_present=row is not None, original_TRANC_record=row,
                missing_TRANC_values=None if row is None else 'none_missing', physical_transport_semantics_qualified=False))
            tranc_count += 1
    result = dict(schema='COMPLETE_NATIVE_RAW_OWNERSHIP_EVIDENCE_NOT_REACTION_QUALIFICATION_V1',
        root_full_STATE_VECTOR=rstate, macro_full_STATE_VECTOR=mstate,
        original_fission_index=findex, fission_index_original_record=findex_row,
        original_macro_fission_components=32, original_macro_fission_component_records=fission_components_count,
        unchanged_old_contract_expected_fission_index_count=256, actual_original_fission_index_count=len(findex),
        old_contract_gap_retained=(len(findex) != 256), no_index_repair_or_fill=True,
        isotope_rows=62, resolved_original_isotope_aliases=aliases, full_sparse_rows=sparse_count, TRANC_group_rows=tranc_count,
        complete_raw_micro_and_macro_field_maps_saved=True, **FALSE)
    with (folder/'complete_native_ownership_evidence_summary.json').open('x') as out:
        json.dump(result, out, separators=(',', ':'), allow_nan=False)
    return result


def state_check(name, state, output, budget):
    folder = output/name
    folder.mkdir()
    native_pin = state['native_XSM']
    with ExitStack() as stack:
        stream = stack.enter_context(Path(native_pin['path']).open('rb'))
        require(identity(os.fstat(stream.fileno())) == native_pin['identity'], 'native open exact7ID')
        data = ReadOnlyFileBytes(stream)
        physical = stack.enter_context((folder/'complete_native_physical_directory_slots.jsonl').open('x'))
        payload = stack.enter_context((folder/'complete_native_original_value_bytes.bin').open('xb'))
        records = DiskRecords(folder/'complete_native_original_path_index.sqlite')
        stack.callback(records.close)
        native = XSM(data, physical, payload, budget, records)
        native.walk()
        payload.flush()
        with (folder/'complete_native_logical_record_inventory.jsonl').open('x') as index:
            for row in native.rows.iter_rows():
                line_json(index, row)
        with (folder/'complete_native_xsmnxt_export_record_order.jsonl').open('x') as index:
            for ordinal, row in enumerate(native.rows.iter_rows(api=True)):
                line_json(index, dict(native_API_export_record_index=ordinal, original_native_record=row))
        micro = compare_ascii(state['original_MICROLIB_ASCII']['path'], native, (), folder, 'MICROLIB', budget)
        macro = compare_ascii(state['original_MACROLIB_ASCII']['path'], native, ('MACROLIB',), folder, 'MACROLIB', budget,
                              state['saved_complete_macro'])
        require(macro['records'] == 19619 and macro['physical_headers_including_all_closes'] == 19990
                and macro['numeric_components'] == 2264113, 'original full19619/19990/2264113 macro scope must remain')
        own = evidence(native, folder)
        require(identity(os.fstat(stream.fileno())) == native_pin['identity'], 'native read-only fd identity changed')
        result = dict(state=name, native_total_records=len(native.rows), native_directories=native.directory_count,
            native_extents=native.extent_count, native_declared_high_word_address=native.high_address,
            complete_MICROLIB=micro, complete_MACROLIB=macro, complete_original_ownership_evidence=own,
            native_persisted_XSM_value_bits_verified=(micro['all_persisted_native_value_bits_equal_ASCII']
                                                     and macro['all_persisted_native_value_bits_equal_ASCII']),
            original_source_tree_subtree_relation='material.xsm ROOT=MICROLIB2; ROOT/MACROLIB=macro.ascii', **FALSE)
    # File, fixed1MiB pread cache, SQLite and per-directory rows released before B.
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binding', required=True)
    parser.add_argument('--binding-sha256', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--expected-parent-pid', required=True, type=int)
    args = parser.parse_args()
    require(SOURCE_STATUS == 'ROOT_BOUND_SOURCE_ONLY_NOT_QUALIFIED' and ROOT_BOUND_BINDING_SHA256 is not None,
            'UNREADY: Root must create separately bound SOURCE and genuine host invocation')
    require(args.binding_sha256 == ROOT_BOUND_BINDING_SHA256 and os.getppid() == args.expected_parent_pid,
            'exact Root binding/real own-parent required')
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        require(os.environ.get(key) == '1', 'original one-thread environment required')
    binding_pin = pin(args.binding)
    require(binding_pin['sha256'] == ROOT_BOUND_BINDING_SHA256, 'Root exact binding full SHA')
    binding = strict_json(Path(args.binding).read_bytes())
    require(binding['schema'] == 'ROOT_ACTUAL_COMPLETE_NATIVE_XSM_ASCII_BINDING_V1' and binding['original_caps'] == CAPS
            and binding['state_order'] == ['A', 'B'] and binding['Root_only_actual_execution'] is True,
            'original complete Root-only bound scope/caps')
    require(binding['format'] == dict(endian='little', word_bytes=4, integer_bytes=4, REAL32_bytes=4, REAL64_bytes=8)
            and binding['source_runtime_format_evidence'] is not None, 'actual pinned build/format provenance required')
    require(binding['unchanged_genuine_host_guard_required'] is True and binding['all_science_flags_false'] is True,
            'Root guard and science boundary required')
    inputs = binding['complete_input_pins']
    require(type(inputs) is list and len({p['path'] for p in inputs}) == len(inputs), 'complete unique explicit input pins')
    pathmap = {p['path']:p for p in inputs}
    for p in inputs:
        exact_pin(p)
    for name in ('A', 'B'):
        st = binding['states'][name]
        for field in ('native_XSM', 'original_MICROLIB_ASCII', 'original_MACROLIB_ASCII'):
            require(pathmap.get(st[field]['path']) == st[field], 'all original state source pins must be fully admitted')
        for p in st['saved_complete_macro'].values():
            require(pathmap.get(p['path']) == p, 'every saved full macro evidence pin must be admitted')
        require(st['saved_complete_macro']['original_raw']['sha256'] == st['original_MACROLIB_ASCII']['sha256']
                and st['saved_complete_macro']['original_raw']['size_bytes'] == st['original_MACROLIB_ASCII']['size_bytes'],
                'saved full macro archive must be byte-equal to original material export')
        for field in ('original_material_provenance_pin', 'original_material_deck_pin'):
            p = st[field]
            require(type(p) is dict and pathmap.get(p['path']) == p,
                    'complete original material creation/deck/provenance pins required')
    require(type(binding['source_runtime_format_evidence']) is dict
            and type(binding['source_runtime_format_evidence']['complete_original_format_Source_pins']) is list,
            'actual original format Source provenance required')
    for p in binding['source_runtime_format_evidence']['complete_original_format_Source_pins']:
        require(pathmap.get(p['path']) == p, 'every original format Source pin must be fully admitted')
    output = Path(args.output_dir)
    require(not output.exists() and output.is_absolute(), 'fresh Root output namespace required')
    output.mkdir()
    budget = Budget(output)
    rows = []
    for name in ('A', 'B'):
        rows.append(state_check(name, binding['states'][name], output, budget))
        budget.check()
    for p in inputs:
        exact_pin(p)
    exact_pin(binding_pin)
    full = all(r['native_persisted_XSM_value_bits_verified'] for r in rows)
    report = dict(schema='ACTUAL_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_BIT_EVIDENCE_ONLY_V1',
        status='ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_COMPARISON_SAVED' if full else 'ACTUAL_NATIVE_ASCII_BIT_MISMATCH_SAVED',
        actual_child_PID=os.getpid(), actual_parent_PID=os.getppid(), source_binding=binding_pin,
        states=rows, original_caps=CAPS, all_complete_state_scope_retained=True,
        native_persisted_XSM_value_bits_verified=full, genuine_supervisor_watch_verified_here=False,
        native_persisted_byte_qualification_sha256=None, actual_scientific_qualification_sha256=None,
        actual_material_scientific_INPUT_qualification_sha256=None,
        classification_is_not_a_scientific_PASS=True, retries=0, state_order=['A', 'B'],
        execution_seconds=time.monotonic()-budget.started, **FALSE)
    report_path = output/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json'
    with report_path.open('x') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    budget.check()
    print(json.dumps(dict(status=report['status'], report=pin(report_path), native_persisted_XSM_value_bits_verified=full,
                          genuine_supervisor_watch_verified_here=False, **FALSE), allow_nan=False), flush=True)
    require(full, 'full evidence saved but at least one original native/ASCII value-bit mismatch; no tolerance or retry')


if __name__ == '__main__':
    main()

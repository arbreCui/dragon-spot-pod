"""UNREADY: complete bounded saved-native data access, not an aggregation engine.

No project/native/helper/API/guard imports. This Source is not executed by its
author. Root must bind actual closed native evidence and a genuine bounded host
before using it. Calling this file directly deliberately cannot read payloads.
"""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import struct

SOURCE_STATUS = 'UNREADY_DATA_ACCESS_ONLY_NO_AGGREGATION_OR_QUALIFICATION'
ROOT_ACTUAL_NATIVE_CLOSED_RECEIPT_PIN = None
ROOT_ACTUAL_NATIVE_INDEPENDENT_REVIEW_PIN = None
ROOT_BOUND_GENUINE_AGGREGATION_HOST_PIN = None
ROOT_BOUND_COMPLETE_AGGREGATION_ENGINE_PIN = None
ORIGINAL_CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
    joint_archive_bytes=2*2**30, history_bytes=96*2**30,
    free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
CHUNK = 2**20
PIN_KEYS = {'path', 'sha256', 'size_bytes', 'identity'}
ROW_KEYS = {'path', 'path_types', 'kind', 'declared_count',
    'original_word_count', 'native_offset_words', 'native_physical_record_index',
    'native_payload_begin_byte', 'native_payload_end_byte',
    'native_payload_sha256', 'native_slot_extent_words', 'native_slot_zero_based'}
KINDS = (0, 1, 2, 3, 4, 5, 6, 10, 99)
SQL_COLUMNS = ('key', 'ordinal', 'api_key', 'row', 'micro_ordinal', 'macro_ordinal')


def require(condition, message):
    if condition is not True:
        raise ValueError(message)


def exact_int(value, minimum=0):
    require(type(value) is int and value >= minimum, 'exact integer required')
    return value


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def typed_pin(pin):
    require(type(pin) is dict and set(pin) == PIN_KEYS, 'exact four-field input pin')
    require(type(pin['path']) is str and Path(pin['path']).is_absolute(), 'absolute actual input')
    require(type(pin['sha256']) is str and len(pin['sha256']) == 64
        and all(c in '0123456789abcdef' for c in pin['sha256']), 'lowercase full SHA256')
    exact_int(pin['size_bytes'])
    require(type(pin['identity']) is list and len(pin['identity']) == 7,
        'complete seven-field identity')
    for value in pin['identity']:
        exact_int(value)
    require(pin['identity'][3] == 1 and pin['identity'][4] == pin['size_bytes'],
        'original single-link input and matching size required')
    return pin


def verify_full_pin(pin, budget):
    """Future Root-only full EOF check; no payload decoded or retained here."""
    typed_pin(pin)
    require(callable(budget), 'bound genuine budget callback mandatory')
    p = Path(pin['path'])
    for parent in (p, *p.parents):
        require(not stat.S_ISLNK(parent.lstat().st_mode), 'input ancestor alias forbidden')
    before = p.lstat()
    require(stat.S_ISREG(before.st_mode) and identity(before) == pin['identity'],
        'actual regular input identity differs')
    digest, total = hashlib.sha256(), 0
    with p.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == pin['identity'], 'opened inode differs')
        while True:
            budget()
            raw = stream.read(CHUNK)
            if not raw:
                break
            total += len(raw)
            digest.update(raw)
        require(identity(os.fstat(stream.fileno())) == pin['identity'], 'input changed while hashing')
    require(total == pin['size_bytes'] and digest.hexdigest() == pin['sha256'],
        'full EOF/size/SHA mismatch')
    require(identity(p.lstat()) == pin['identity'], 'input changed after full EOF')


def path_key(path):
    require(type(path) in (list, tuple), 'typed path sequence required')
    for value in path:
        require(type(value) is str or (type(value) is int and value >= 1),
            'only exact original names and one-based list indices')
    return json.dumps(list(path), ensure_ascii=True, separators=(',', ':'))


class SavedNativeInput:
    """Read-only existing SQLite plus its paired complete original byte pool.

    Root's genuine host pins both inputs before/after, and budgets all H/O/C/D/E
    including SQLite FILE temp storage, spools and journals. No material XSM or
    ASCII is opened by this adapter. All record ranges can be streamed.
    """
    def __init__(self, sql_pin, pool_pin, temp_directory, budget):
        require(callable(budget), 'genuine bounded host callback required')
        self.budget, self.sql_pin, self.pool_pin = budget, sql_pin, pool_pin
        verify_full_pin(sql_pin, budget)
        verify_full_pin(pool_pin, budget)
        temp = Path(temp_directory)
        require(temp.is_absolute() and temp.is_dir() and not temp.is_symlink(),
            'actual owned output temp directory required')
        for parent in temp.parents:
            require(not parent.is_symlink(), 'SQLite temporary ancestor alias forbidden')
        os.environ['SQLITE_TMPDIR'] = str(temp)
        self.db, self.pool = None, None
        try:
            self.pool = Path(pool_pin['path']).open('rb')
            require(identity(os.fstat(self.pool.fileno())) == pool_pin['identity'], 'opened pool differs')
            self.db = sqlite3.connect(Path(sql_pin['path']).as_uri()+'?mode=ro', uri=True)
            self.db.execute('PRAGMA query_only=ON')
            self.db.execute('PRAGMA cache_size=-8192')
            self.db.execute('PRAGMA mmap_size=0')
            self.db.execute('PRAGMA temp_store=FILE')
            self.db.set_progress_handler(self._sqlite_budget, 1000)
            columns = tuple(row[1] for row in self.db.execute('PRAGMA table_info(records)'))
            require(columns == SQL_COLUMNS, 'exact saved native walker schema required')
            require(self.db.execute('PRAGMA query_only').fetchone() == (1,), 'read-only SQL required')
            require(self.db.execute('PRAGMA cache_size').fetchone() == (-8192,), '8MiB cache required')
            require(self.db.execute('PRAGMA mmap_size').fetchone() == (0,), 'SQL mmap forbidden')
            require(self.db.execute('PRAGMA temp_store').fetchone() == (1,), 'FILE temp required')
            require(identity(Path(sql_pin['path']).lstat()) == sql_pin['identity'], 'SQL inode changed')
        except BaseException:
            if self.db is not None:
                self.db.close()
            if self.pool is not None:
                self.pool.close()
            raise

    def _sqlite_budget(self):
        self.budget()
        return 0

    def row(self, path):
        result = self.db.execute('SELECT row FROM records WHERE key=?', (path_key(path),)).fetchone()
        if result is None:
            return None
        row = strict_json(result[0])
        self.validate_row(row)
        require(row['path'] == list(path), 'SQL primary path/row mismatch')
        return row

    def validate_row(self, row):
        require(type(row) is dict and set(row) == ROW_KEYS, 'complete original native row schema')
        path_key(row['path'])
        require(row['path_types'] == ['str' if type(x) is str else 'int' for x in row['path']],
            'path key types differ')
        require(type(row['kind']) is int and row['kind'] in KINDS, 'original native type required')
        kind, count, words = row['kind'], row['declared_count'], row['original_word_count']
        require(type(count) is int and type(words) is int, 'typed native lengths')
        for key in ('native_offset_words', 'native_physical_record_index',
                    'native_payload_begin_byte', 'native_payload_end_byte'):
            exact_int(row[key])
        for key in ('native_slot_extent_words', 'native_slot_zero_based'):
            require(row[key] is None or (type(row[key]) is int and row[key] >= 0),
                'original optional physical slot metadata')
        if kind == 0:
            require(count == words == -1, 'directory length differs')
            expected = 0
        elif kind == 10:
            require(count == words and count >= 0, 'list count differs')
            expected = 0
        elif kind == 99:
            require(count == words == 0, 'empty list element differs')
            expected = 0
        else:
            require(count >= 0 and words == count*(2 if kind in (4, 6) else 1), 'typed word count differs')
            expected = 4*words
        begin, end = row['native_payload_begin_byte'], row['native_payload_end_byte']
        require(end-begin == expected and 0 <= begin <= end <= self.pool_pin['size_bytes'],
            'paired byte-pool span differs')
        require(type(row['native_payload_sha256']) is str and len(row['native_payload_sha256']) == 64
            and all(c in '0123456789abcdef' for c in row['native_payload_sha256']), 'full record hash required')
        return row

    def iter_all(self):
        """Preserve complete physical preorder and both saved ASCII ordinals."""
        for key, ordinal, api_key, raw, micro, macro in self.db.execute(
                'SELECT key,ordinal,api_key,row,micro_ordinal,macro_ordinal FROM records ORDER BY ordinal'):
            self.budget()
            row = self.validate_row(strict_json(raw))
            require(key == path_key(row['path']) and type(ordinal) is int
                and ordinal == row['native_physical_record_index'], 'original indexed order differs')
            require(type(api_key) is str, 'saved Ganlib API rank required')
            for value in (micro, macro):
                require(value is None or (type(value) is int and value >= 0), 'typed original ASCII ordinal')
            yield dict(record=row, physical_ordinal=ordinal, api_key=api_key,
                       micro_ASCII_ordinal=micro, macro_ASCII_ordinal=macro)

    def range_bytes(self, row, begin, size):
        self.validate_row(row)
        exact_int(begin)
        exact_int(size)
        require(size <= CHUNK and begin+size <= row['native_payload_end_byte']-row['native_payload_begin_byte'],
            'bounded original record slice required')
        self.budget()
        raw = os.pread(self.pool.fileno(), size, row['native_payload_begin_byte']+begin)
        require(len(raw) == size, 'saved native pool truncated')
        return raw

    def iter_raw(self, row):
        self.validate_row(row)
        size = row['native_payload_end_byte']-row['native_payload_begin_byte']
        digest = hashlib.sha256()
        for begin in range(0, size, CHUNK):
            raw = self.range_bytes(row, begin, min(CHUNK, size-begin))
            digest.update(raw)
            yield raw
        require(digest.hexdigest() == row['native_payload_sha256'], 'complete original record bytes differ')

    def scalar_bits(self, row, index):
        require(row['kind'] in (1, 2, 4, 5, 6), 'numeric original type required')
        exact_int(index)
        require(index < row['declared_count'], 'numeric original element outside record')
        width = 8 if row['kind'] in (4, 6) else 4
        return self.range_bytes(row, index*width, width)

    def fixed_small(self, path, kind, count):
        """Only explicit small context vectors, never a full micro field tree."""
        row = self.row(path)
        require(row is not None and type(kind) is int and row['kind'] == kind
            and type(count) is int and row['declared_count'] == count,
            'mandatory actual context type/count missing')
        require(row['native_payload_end_byte']-row['native_payload_begin_byte'] <= CHUNK,
            'small context must use streaming for larger records')
        return row, b''.join(self.iter_raw(row))

    def close(self):
        self.db.close()
        self.pool.close()
        verify_full_pin(self.sql_pin, self.budget)
        verify_full_pin(self.pool_pin, self.budget)


def capture_complete_fixed_context(saved):
    """Actual future metadata capture only; neither aggregation nor historical proof."""
    rows = {}
    def take(path, kind, count):
        row, raw = saved.fixed_small(path, kind, count)
        rows[path_key(path)] = dict(original_record=row, original_bytes_hex=raw.hex())
        return raw
    root = struct.unpack('<40i', take(('STATE-VECTOR',), 1, 40))
    macro = struct.unpack('<40i', take(('MACROLIB','STATE-VECTOR'), 1, 40))
    require(root[:5] == (8,62,370,3,1) and root[12] == 18 and root[15] == 4
        and root[18] == 6 and macro[:4] == (370,8,3,32), 'complete current scope differs')
    used = take(('ISOTOPESUSED',), 3, 186)
    take(('ISOTOPERNAME',), 3, 186)
    mixes = struct.unpack('<62i', take(('ISOTOPESMIX',), 1, 62))
    take(('ISOTOPESDENS',), 2, 62)
    take(('ISOTOPESTEMP',), 2, 62)
    take(('ISOTOPESSHI',), 1, 62)
    extra = take(('ADDXSNAME-P0',), 3, 36)
    take(('MACROLIB','ADDXSNAME-P0'), 3, 36)
    take(('CHI-LIMITS',), 1, 5)
    take(('ENERGY',), 2, 371)
    take(('MACROLIB','ENERGY'), 2, 371)
    take(('MACROLIB','FISSIONINDEX'), 1, 64)
    aliases = []
    list_row = saved.row(('ISOTOPESLIST',))
    require(list_row is not None and list_row['kind'] == 10 and list_row['declared_count'] == 62,
        'all original isotope list slots required')
    for index in range(1, 63):
        item = saved.row(('ISOTOPESLIST',index))
        require(item is not None and 1 <= mixes[index-1] <= 8, 'complete real isotope/mix required')
        if item['kind'] == 0 and item['declared_count'] == -1:
            resolved = index
        else:
            require(item['kind'] == 99 and item['declared_count'] == 0, 'original empty alias required')
            matching = [j for j in range(index-1) if used[12*j:12*j+12] == used[12*(index-1):12*index]
                        and aliases[j] is not None]
            resolved = aliases[matching[0]] if matching else None
        require(resolved is not None, 'original LIBIPS alias unresolved')
        aliases.append(resolved)
    optional = {}
    for path in (('SHIBA','STATE-VECTOR'), ('SHIBA','EPS-SHIBA'), ('SHIBA','TCEPS-SHIBA'),
            ('MACROLIB','TIMESTAMP'), ('TIMESPER',),
            ('ISOTOPESVOL',), ('MIXTURESVOL',), ('PARTICLE',), ('PARTICLE-NAM',),
            ('PARTICLE-NGR',), ('PARTICLE-MC2',), ('MACROLIB','SPH'),
            ('MACROLIB','LAMBDA-D')):
        row = saved.row(path)
        optional[path_key(path)] = dict(present=row is not None, original_record=row,
            original_bytes_hex=None)
        if row is not None:
            size = row['native_payload_end_byte']-row['native_payload_begin_byte']
            if size <= CHUNK:
                optional[path_key(path)]['original_bytes_hex'] = b''.join(saved.iter_raw(row)).hex()
    return dict(schema='ROOT_FUTURE_FINAL_MICRO_MACRO_FIXED_CONTEXT_ONLY_V1',
        status='ACTUAL_CONTEXT_ONLY_NOT_AGGREGATION_OR_HISTORICAL_REPLAY',
        original_context_records=rows, optional_original_presence=optional,
        original_18_extra_name_bytes_hex=[extra[8*i:8*i+8].hex() for i in range(18)],
        complete62_LIBIPS_aliases_one_based=aliases, historical_track_MAT_pin=None,
        historical_pre_call_MACROLIB_pin=None, compiled_Source_binary_link_proved=False,
        aggregation_executed=False, numerical_or_scientific_qualification=False)


if __name__ == '__main__':
    raise SystemExit('UNREADY data access Source only: no genuine aggregation host/engine binding; no payload read')

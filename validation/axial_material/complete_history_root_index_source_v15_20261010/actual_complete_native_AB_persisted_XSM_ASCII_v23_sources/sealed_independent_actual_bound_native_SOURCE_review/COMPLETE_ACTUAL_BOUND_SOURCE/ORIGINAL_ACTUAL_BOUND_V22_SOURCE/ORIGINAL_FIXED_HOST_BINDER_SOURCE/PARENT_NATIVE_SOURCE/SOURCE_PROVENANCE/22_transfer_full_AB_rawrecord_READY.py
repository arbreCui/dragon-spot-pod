"""UNREADY SOURCE design: complete current A/B MACROLIB raw-record transfer.

No action at import. main requires an actual Root SOURCE binding and execution
by a separately admitted genuine one-child supervisor. The supervisor alone
provides the actual 512 MiB/watch/resource/EXIT evidence; this wrapper does not
fabricate a watcher or a physical qualification. No input or success pins are
bound in this SOURCE template.

The full byte decoder runs first and is released. The full default streaming
decoder then runs independently and is compared against the complete spooled
first result. Both retain every record, energy group, moment, component and
unknown field. Original ASCII bytes and every original header/payload span are
retained alongside the type/bit-preserving payload. No dense scattering matrix,
physics solve, reaction synthesis, clipping, CHI repair or group reduction.
"""
import argparse
import gc
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import re
import stat
import struct
import sys
import time

SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
SOURCE_QUALIFICATION_SHA256 = '7534059b4fdd9392f9c5b797808a86c69b1e6cdee371010f3e0ad02188fd5407'
ACTUAL_ROOT_BINDING_RECEIPT_SHA256 = '0ec92e4192a821966ab23e167943bdd3b397e737a4fb589157292d6e2d9205e3'
ACTUAL_TRANSFER_QUALIFICATION_SHA256 = None
REACTION_MULTIPLICITY_QUALIFICATION_SHA256 = None
ACTUAL_SCIENTIFIC_REFERENCE_SHA256 = None
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
INPUTS = {s: ART / ('axial-material-inputs-20261003/' + s + '/macro.ascii') for s in ('A', 'B')}
READERS = {
    'native_records': (Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/fullpitch_pnl_s30_b0_closure_v1_20260907/native_records.py'), '67fe414c25f5867e80cc0509c9951522253e572b92998c83c6b32a254c59342b'),
    'stream_records': (Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/finegroup_acceptance/stream_records.py'), 'dc2d4e5f6cfa6b6d312669f44db98df5873d049707672bb166b26719fad2df0f'),
}
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')
CAPS = {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_archive_bytes': 2*2**30, 'history_bytes': 96*2**30, 'free_floor_bytes': 8*2**30, 'threads': 1, 'children_at_once': 1, 'retries': 0}
EXPECTED_DIMENSIONS = (370, 8, 3, 32)
HEADER = re.compile(r'^->\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+<-\s*(\d{8})?\s*$')
PAYLOAD_MAGIC = b'AXMAT_FULL_TYPED_LCM_V1\x00'
SMALL_META_LIMIT = 2*2**20
FALSE_SCIENCE = {'scientific_accuracy_qualified': False, 'physical_neutron_balance_qualified': False, 'AAA_accuracy_qualified': False, 'ABA_admitted': False, 'coupled_370group_reference_qualified': False, 'native_transport_executed': False, 'whole_combined_build_or_INPUT_qualified': False}

def require(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def ordinary(path, directory=False):
    require(path.is_absolute() and '..' not in path.parts, 'absolute ordinary path required')
    for parent in [*reversed(path.parents), path]:
        s = parent.lstat()
        require(not stat.S_ISLNK(s.st_mode), 'no source/input/output alias allowed')
    s = path.lstat()
    require(stat.S_ISDIR(s.st_mode) if directory else stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'ordinary directory/singlelink file required')

def full_pin(path):
    ordinary(path)
    before = identity(path)
    digest = hashlib.sha256()
    count = 0
    with path.open('rb') as stream:
        while block := stream.read(2**20):
            digest.update(block)
            count += len(block)
    require(identity(path) == before and count == before[4], 'full EOF pin changed')
    return {'path': str(path), 'sha256': digest.hexdigest(), 'size_bytes': count, 'identity': before}

def exact_pin(pin):
    require(type(pin) is dict and set(pin) == {'path', 'sha256', 'size_bytes', 'identity'}, 'complete actual pin required')
    require(type(pin['path']) is str and type(pin['sha256']) is str and len(pin['sha256']) == 64 and all(c in '0123456789abcdef' for c in pin['sha256']) and pin['sha256'] != '0'*64, 'actual nonzero pin SHA required')
    require(type(pin['size_bytes']) is int and pin['size_bytes'] >= 0 and type(pin['identity']) is list and len(pin['identity']) == 7 and all(type(v) is int for v in pin['identity']) and pin['identity'][4] == pin['size_bytes'], 'exact integer7 pin required')
    require(full_pin(Path(pin['path'])) == pin, 'all source/input actual full SHA7ID exact')

def strict_json(raw):
    def pairs(items):
        d = {}
        for key, value in items:
            require(key not in d, 'duplicate metadata key')
            d[key] = value
        return d
    def bad(value):
        raise ValueError('nonfinite metadata literal ' + value)
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    def finite(v):
        if type(v) is dict:
            return all(finite(x) for x in v.values())
        if type(v) is list:
            return all(finite(x) for x in v)
        return type(v) is not float or math.isfinite(v)
    require(finite(value), 'metadata derived number must be finite')
    return value

def write_meta(path, value):
    raw = (json.dumps(value, ensure_ascii=True, allow_nan=False, indent=2) + '\n').encode()
    require(len(raw) <= SMALL_META_LIMIT, 'small metadata exceeds predeclared complete bound')
    with path.open('xb') as f:
        f.write(raw)

def json_line(stream, value):
    stream.write(json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False) + '\n')

def load_reader(name, pin):
    expected_path, expected_sha = READERS[name]
    require(pin['path'] == str(expected_path) and pin['sha256'] == expected_sha, 'original complete reader SOURCE required')
    exact_pin(pin)
    spec = importlib.util.spec_from_file_location('axmat_full_transfer_' + name, expected_path)
    require(spec is not None and spec.loader is not None, 'reader import spec required')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def archive_raw(original, archived, expected):
    exact_pin(expected)
    digest = hashlib.sha256()
    count = 0
    with original.open('rb') as src, archived.open('xb') as dst:
        while block := src.read(2**20):
            dst.write(block)
            digest.update(block)
            count += len(block)
    require(count == expected['size_bytes'] and digest.hexdigest() == expected['sha256'], 'complete raw archive mismatch')
    exact_pin(expected)
    return full_pin(archived)

def raw_inventory(raw_path, output_path):
    """Independent header/span inventory; never synthesizes numeric fields.

    Every physical header, closing header and complete payload is represented.
    Byte intervals are contiguous and cover the entire original raw file.
    Count/width parsing locates boundaries only; the two default readers decide
    complete numeric semantic values independently below.
    """
    nodes, seen = {}, set()
    record_count = physical_headers = numeric_count = 0
    last_closed = False
    with raw_path.open('rb') as src, output_path.open('x') as out:
        while True:
            begin = src.tell()
            raw = src.readline()
            if not raw:
                break
            require(len(raw) <= 2**20, 'bounded full binary line required')
            line = raw.decode('ascii').rstrip('\r\n')
            match = HEADER.fullmatch(line)
            require(match is not None, 'complete raw inventory header required')
            physical_headers += 1
            level, flags, kind, count = map(int, match.groups()[:4])
            index = int(match[5]) if match[5] else None
            digest = hashlib.sha256(raw)
            last_closed = False
            def payload_line():
                b = src.readline()
                require(bool(b) and len(b) <= 2**20, 'raw payload truncation/line bound')
                text = b.decode('ascii').rstrip('\r\n')
                require(HEADER.fullmatch(text) is None, 'raw payload premature header')
                digest.update(b)
                return text
            if level < 0:
                require(flags == kind == count == 0 and index is None, 'raw close header invalid')
                for k in list(nodes):
                    if k >= -level:
                        del nodes[k]
                last_closed = level == -1
                row = {'entry': 'close', 'physical_header_index': physical_headers - 1, 'level': level, 'flags': flags, 'kind': kind, 'declared_count': count}
            else:
                require(level > 0 and flags in (0, 12), 'raw level/flags invalid')
                for k in list(nodes):
                    if k >= level:
                        del nodes[k]
                if flags == 12:
                    require(index is None, 'raw named header index invalid')
                    name = payload_line().strip()
                    require(bool(name), 'raw named record missing name')
                else:
                    require(index is not None and index > 0, 'raw list index invalid')
                    name = index
                path = tuple(nodes[k] for k in sorted(nodes)) + (name,)
                require(path not in seen and len(seen) < 2_000_000, 'raw duplicate/record bound')
                seen.add(path)
                row = {'entry': 'record', 'record_index': record_count, 'physical_header_index': physical_headers - 1, 'path': list(path), 'path_types': ['str' if type(x) is str else 'int' for x in path], 'level': level, 'flags': flags, 'kind': kind, 'declared_count': count}
                record_count += 1
                if kind in (0, 10, 99):
                    require((kind == 0 and count == -1) or (kind == 10 and count >= 0) or (kind == 99 and count == 0), 'raw directory/list shape invalid')
                    if kind != 99:
                        nodes[level] = name
                elif kind in (1, 2, 4):
                    require(0 <= count <= 100_000_000, 'raw numeric count invalid')
                    consumed = 0
                    while consumed < count:
                        tokens = payload_line().split()
                        require(consumed + len(tokens) <= count, 'raw numeric payload overflow')
                        consumed += len(tokens)
                    numeric_count += consumed
                elif kind == 3:
                    require(0 <= count <= 1_000_000, 'raw character count invalid')
                    consumed = 0
                    while consumed < count:
                        widths = [int(v) for v in payload_line().split()]
                        require(consumed + len(widths) <= count and all(v == 4 for v in widths), 'raw character widths invalid')
                        consumed += len(widths)
                    size = 0
                    while size < 4*count:
                        text = payload_line()
                        remaining = 4*count - size
                        require(len(text) <= remaining or not text[remaining:].strip(), 'raw character overflow')
                        size += len(text)
                    row['original_character_width'] = 4
                    row['original_character_bytes'] = 4*count
                else:
                    raise ValueError('unsupported raw LCM record type')
            row.update(raw_begin_byte=begin, raw_end_byte=src.tell(), raw_span_sha256=digest.hexdigest())
            json_line(out, row)
        require(last_closed and src.tell() == raw_path.stat().st_size, 'raw full EOF/terminal close required')
    return {'records': record_count, 'physical_headers_including_closes': physical_headers, 'numeric_values': numeric_count, 'full_original_raw_byte_interval_coverage': True}

def raw_record_rows(path):
    with path.open() as f:
        for line in f:
            row = strict_json(line)
            if row['entry'] == 'record':
                yield row

def payload_chunks(kind, value):
    """Exact decoded types/bits. Original ASCII bytes remain independently saved.

    Kind2 stores both LCM REAL32 IEEE bits and the parser float64 IEEE bits.
    This distinguishes a value/type/floatbit mismatch, including signed zero.
    ASCII alone does not independently certify the original XSM memory bits.
    """
    if kind in (0, 10, 99):
        require(type(value) is int, 'directory/list count must be exact int')
        return
    if kind == 1:
        require(type(value) is tuple and all(type(x) is int for x in value), 'all integer payload types required')
        for x in value:
            yield str(x).encode('ascii') + b'\n'
    elif kind in (2, 4):
        require(type(value) is tuple, 'all real payload tuple required')
        for x in value:
            require(type(x) is float and math.isfinite(x), 'exact finite real value type required')
            if kind == 2:
                chunk = struct.pack('<fd', x, x)
                require(math.isfinite(struct.unpack('<f', chunk[:4])[0]), 'nonrepresentable REAL32 rejected, no fixup')
            else:
                chunk = struct.pack('<d', x)
            yield chunk
    elif kind == 3:
        require(type(value) is str, 'exact character payload type required')
        yield value.encode('ascii')
    else:
        raise ValueError('unsupported decoded LCM record type')

def expected_payload_count(kind, value):
    if kind in (1, 2, 4):
        return len(value)
    if kind in (0, 10, 99):
        return value
    return None  # Original character count is preserved by raw header, not guessed from rstrip().

def spool_first_reader(records, inventory_path, index_path, payload_path):
    require(type(records) is dict, 'full first reader dict required')
    with index_path.open('x') as index, payload_path.open('xb') as payload:
        payload.write(PAYLOAD_MAGIC)
        for pair, row in itertools.zip_longest(records.items(), raw_record_rows(inventory_path)):
            require(pair is not None and row is not None, 'full first decoder/raw record inventory count differs')
            key, (kind, value) = pair
            require(type(key) is tuple and list(key) == row['path'] and ['str' if type(v) is str else 'int' for v in key] == row['path_types'] and all(type(v) in (str, int) for v in key), 'complete first decoder/raw key order or key type differs')
            require(type(kind) is int and kind == row['kind'], 'original record kind differs')
            count = expected_payload_count(kind, value)
            require(count is None or count == row['declared_count'], 'original numeric/directory count differs')
            begin = payload.tell()
            digest = hashlib.sha256()
            for chunk in payload_chunks(kind, value):
                payload.write(chunk)
                digest.update(chunk)
            row.update(typed_payload_begin_byte=begin, typed_payload_end_byte=payload.tell(), typed_payload_sha256=digest.hexdigest(), python_value_type=type(value).__name__, payload_encoding={0:'directory_count_in_header',10:'list_count_in_header',99:'empty_in_header',1:'exact_signed_decimal_integer_lines',2:'little_endian_IEEE_float32_plus_parser_float64_per_value',3:'ASCII_decoded_character_with_original_padding_in_raw_span',4:'little_endian_IEEE_float64'}[kind])
            json_line(index, row)

def compare_second_reader(records, stats, index_path, payload_path, expected_records):
    require(type(records) is dict and stats['all_records_validated'] == stats['retained_records'] == len(records) == expected_records, 'default full streaming retention required')
    with index_path.open() as index, payload_path.open('rb') as payload:
        require(payload.read(len(PAYLOAD_MAGIC)) == PAYLOAD_MAGIC, 'typed payload format mismatch')
        for pair, line in itertools.zip_longest(records.items(), index):
            require(pair is not None and line is not None, 'complete second decoder record count differs')
            key, (kind, value) = pair
            row = strict_json(line)
            require(type(key) is tuple and list(key) == row['path'] and ['str' if type(v) is str else 'int' for v in key] == row['path_types'] and all(type(v) in (str, int) for v in key), 'second decoder exact full key type/order differs')
            require(type(kind) is int and kind == row['kind'] and type(value).__name__ == row['python_value_type'], 'second decoder exact original kind/value type differs')
            count = expected_payload_count(kind, value)
            require(count is None or count == row['declared_count'], 'second decoder full raw count differs')
            require(payload.tell() == row['typed_payload_begin_byte'], 'typed payload complete order/offset differs')
            digest = hashlib.sha256()
            for chunk in payload_chunks(kind, value):
                require(payload.read(len(chunk)) == chunk, 'independent readers complete exact types/values/rawfloatbits differ')
                digest.update(chunk)
            require(payload.tell() == row['typed_payload_end_byte'] and digest.hexdigest() == row['typed_payload_sha256'], 'second decoder complete field extent/hash differs')
        require(payload.read(1) == b'', 'uncompared typed trailing payload forbidden')
    return {'all_records': len(records), 'all_paths_types_order_values_floatbits_equal': True, 'all_stream_records_retained': True, 'full_first_payload_compared_byteexact': True, 'complete_stream_statistics': stats}

def contract_inventory(records, contract_path, spans_path):
    """Report actual missing/invalid fields. Never fill any record or rate.

    This is a structure/readiness inventory, not a neutron reaction model. All
    detailed required-field outcomes and all sparse spans are saved in full.
    Unknown extra records/reactions remain in the full typed payload and raw.
    """
    gaps = {}
    checks = 0
    def outcome(stream, path, expected_kind, expected_count):
        nonlocal checks
        checks += 1
        actual = records.get(path)
        reasons = []
        if actual is None:
            reasons.append('missing_real_record_no_substitution')
        else:
            kind, value = actual
            if kind not in expected_kind:
                reasons.append('unexpected_original_kind')
            actual_count = len(value) if type(value) is tuple else value if kind in (0,10,99) else None
            if expected_count is not None and actual_count != expected_count:
                reasons.append('unexpected_actual_count')
        for reason in reasons:
            gaps[reason] = gaps.get(reason, 0) + 1
        json_line(stream, {'path': list(path), 'expected_original_kind_one_of': list(expected_kind), 'expected_count': expected_count, 'present': actual is not None, 'actual_kind': actual[0] if actual is not None else None, 'actual_count': len(actual[1]) if actual is not None and type(actual[1]) is tuple else actual[1] if actual is not None and actual[0] in (0,10,99) else None, 'gap_reasons': reasons})
        return actual if not reasons else None
    with contract_path.open('x') as c, spans_path.open('x') as spans:
        signature = outcome(c, ('SIGNATURE',), (3,), None)
        if signature is not None and signature[1] != 'L_MACROLIB':
            gaps['actual_SIGNATURE_not_L_MACROLIB'] = 1
        state = outcome(c, ('STATE-VECTOR',), (1,), 40)
        if state is not None and tuple(state[1][:4]) != EXPECTED_DIMENSIONS:
            gaps['actual_STATE_VECTOR_dims_not_370_8_3_32'] = 1
        energy = outcome(c, ('ENERGY',), (2,4), 371)
        if energy is not None and not all(energy[1][i] > energy[1][i+1] for i in range(370)):
            gaps['original_energy_order_not_strictly_descending'] = 1
        outcome(c, ('FISSIONINDEX',), (1,), 8*32)
        outcome(c, ('GROUP',), (10,), 370)
        groups = {p[1] for p in records if len(p) >= 2 and p[0] == 'GROUP'}
        if groups != set(range(1,371)):
            gaps['actual_group_index_set_not_full_370'] = 1
        for destination in range(1,371):
            outcome(c, ('GROUP', destination), (0,), -1)
            for name in ('NTOT0','TRANC','SIGS00','SIGS01','SIGS02','SIGW00','SIGW01','SIGW02'):
                outcome(c, ('GROUP', destination, name), (2,4), 8)
            for name in ('NUSIGF','CHI'):
                outcome(c, ('GROUP', destination, name), (2,4), 8*32)
            for moment in range(3):
                suffix = str(moment).zfill(2)
                fields = [outcome(c, ('GROUP', destination, name+suffix), (1,) if name != 'SCAT' else (2,4), 8 if name != 'SCAT' else None) for name in ('NJJS','IJJS','IPOS','SCAT')]
                if any(x is None for x in fields):
                    json_line(spans, {'destination_group':destination,'raw_Legendre_moment':moment,'status':'required_raw_sparse_fields_missing_or_malformed_no_expansion'})
                    continue
                counts, tops, offsets, values = [x[1] for x in fields]
                for mixture, (count, top, offset) in enumerate(zip(counts,tops,offsets),1):
                    valid = all(type(x) is int for x in (count,top,offset)) and 0 <= count <= 370 and (count == 0 or count <= top <= 370) and (count == 0 or 1 <= offset and offset-1+count <= len(values))
                    if not valid:
                        gaps['actual_sparse_reference_out_of_range'] = gaps.get('actual_sparse_reference_out_of_range',0)+1
                    json_line(spans, {'destination_group':destination,'mixture':mixture,'raw_Legendre_moment':moment,'count':count,'top_source_group':top,'one_based_raw_offset':offset,'raw_SCAT_record_count':len(values),'source_indices_formula':'top-jnd+1 for jnd=1..count','valid_referenced_span':valid,'raw_unreferenced_padding_retained_without_interpretation':True,'contiguous_packing_required_or_assumed':False})
    field_names = sorted({p[2] for p in records if len(p)==3 and p[0]=='GROUP' and type(p[2])is str})
    state_value = records.get(('STATE-VECTOR',))
    return {'required_record_checks':checks,'gap_counts':gaps,'actual_STATE_VECTOR':list(state_value[1]) if state_value is not None and type(state_value[1])is tuple else None,'all_actual_GROUP_field_names_including_extra_reactions':field_names,'original_LCM_memory_bit_identity_directly_verified':False,'true_physical_loss_reaction_multiplicity_verified':False,'transport_correction_semantics_qualified':False,'raw_Legendre_no_angular_factor_applied':True,'no_fields_filled_clipped_normalized_or_inferred':True,'future_solver_scientific_input_admitted':False}

def transfer_state(state, expected, folder, first_reader, second_reader):
    folder.mkdir()
    raw_path = folder/'original_macro.ascii'
    raw_archive = archive_raw(INPUTS[state], raw_path, expected)
    inventory_path = folder/'complete_raw_header_span_inventory.jsonl'
    counts = raw_inventory(raw_path, inventory_path)
    index_path = folder/'complete_typed_record_index.jsonl'
    payload_path = folder/'complete_typed_payload.bin'
    with raw_path.open('rb') as f:
        raw = f.read()
    require(len(raw) == expected['size_bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'], 'first complete raw bytes mismatch')
    records = first_reader.decode(raw)
    del raw
    spool_first_reader(records, inventory_path, index_path, payload_path)
    contract = contract_inventory(records, folder/'full_required_field_contract.jsonl', folder/'full_sparse_reference_spans.jsonl')
    require(len(records) == counts['records'], 'complete first reader count differs')
    del records
    gc.collect()  # Release full first state before the independent full second decoder.
    with raw_path.open('rb') as binary_lines:
        second_records, second_stats = second_reader.decode_stream(binary_lines)
    comparison = compare_second_reader(second_records, second_stats, index_path, payload_path, counts['records'])
    del second_records, second_stats
    gc.collect()  # Release the full second state before the next A/B input.
    exact_pin(expected)
    require(full_pin(raw_path) == raw_archive, 'full archived raw bytes/identity changed')
    result = {'state':state,'original_input':expected,'full_raw_archive':raw_archive,'full_inventory':counts,'independent_full_reader_comparison':comparison,'scientific_contract_inventory':contract,'source_total_object_lifetime':'one complete reader record dict at a time; first released before second and state released before next state','complete_payload_files':[full_pin(p)for p in (inventory_path,index_path,payload_path,folder/'full_required_field_contract.jsonl',folder/'full_sparse_reference_spans.jsonl')],**FALSE_SCIENCE}
    write_meta(folder/'small_state_metadata.json', result)
    return result

def admit(args):
    require(SOURCE_STATUS == 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED' and type(SOURCE_QUALIFICATION_SHA256)is str and len(SOURCE_QUALIFICATION_SHA256)==64 and type(ACTUAL_ROOT_BINDING_RECEIPT_SHA256)is str and len(ACTUAL_ROOT_BINDING_RECEIPT_SHA256)==64, 'UNREADY SOURCE template cannot execute')
    require(ACTUAL_TRANSFER_QUALIFICATION_SHA256 is None and REACTION_MULTIPLICITY_QUALIFICATION_SHA256 is None and ACTUAL_SCIENTIFIC_REFERENCE_SHA256 is None, 'future runtime/science success pins must remain None')
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None and all(os.environ.get(k)=='1'for k in THREAD_KEYS), 'original unprofiled nonoptimized one-thread environment required')
    require(type(args.expected_parent_pid)is int and args.expected_parent_pid>1 and os.getppid()==args.expected_parent_pid, 'actual separately genuine supervisor parent PID required')
    binding_path = Path(args.binding)
    binding_pin = full_pin(binding_path)
    require(binding_pin['sha256']==args.binding_sha256==ACTUAL_ROOT_BINDING_RECEIPT_SHA256 and binding_pin['size_bytes']<=SMALL_META_LIMIT, 'Root actual SOURCE binding wholeSHA required')
    binding = strict_json(binding_path.read_bytes())
    require(binding['schema']=='ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1' and binding['source_only']is True and binding['scientific_qualification_created']is False, 'actual binding SOURCE-only schema required')
    require(binding['source_qualification_sha256']==SOURCE_QUALIFICATION_SHA256 and binding['original_caps']==CAPS and all(type(v)is int for v in binding['original_caps'].values()), 'original true Source qualification/caps required')
    require(Path(sys.executable).resolve()==Path(binding['python']['path']).resolve(), 'Root genuine host pinned Python required')
    exact_pin(binding['python'])
    for state in ('A','B'):
        require(binding['inputs'][state]['path']==str(INPUTS[state]), 'same original full A/B input path required')
        exact_pin(binding['inputs'][state])
    for name in READERS:
        exact_pin(binding['readers'][name])
    require(binding['public_reader_calls']==['native_records.decode(raw_bytes)','stream_records.decode_stream(binary_iterator)'] and binding['full_default_retention']is True, 'both original full APIs/default retention required')
    out = Path(args.output_dir)
    require(out.is_absolute() and out.is_relative_to(ART) and out!=ART and '..'not in out.parts and not os.path.lexists(out), 'fresh strict ART descendant output/no retry required')
    ordinary(out.parent, directory=True)
    return binding, binding_pin, out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding',required=True)
    parser.add_argument('--binding-sha256',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--expected-parent-pid',type=int,required=True)
    args=parser.parse_args()
    started=time.monotonic()
    binding,binding_pin,out=admit(args)
    out.mkdir()
    results=[]
    try:
        first_reader=load_reader('native_records',binding['readers']['native_records'])
        second_reader=load_reader('stream_records',binding['readers']['stream_records'])
        for state in ('A','B'):
            require(time.monotonic()-started<CAPS['stage_seconds'], 'original child600 stage exhausted')
            results.append(transfer_state(state,binding['inputs'][state],out/state,first_reader,second_reader))
        del first_reader,second_reader
        gc.collect()
        for p in [*binding['inputs'].values(),*binding['readers'].values(),binding['python']]:
            exact_pin(p)
        require(full_pin(Path(args.binding))==binding_pin,'Root binding fullEOF unchanged')
        elapsed=time.monotonic()-started
        require(math.isfinite(elapsed) and 0<=elapsed<CAPS['stage_seconds'],'original child stage wall cap')
        files={str(p.relative_to(out)):full_pin(p)for p in sorted(out.rglob('*'))if p.is_file()}
        bytes_before_report=sum(p['size_bytes']for p in files.values())
        require(bytes_before_report<CAPS['joint_archive_bytes'],'raw transfer outputs exceed original archive ceiling')
        write_meta(out/'complete_payload_manifest.json',{'schema':'CURRENT150_AB_FULL_RAWRECORD_PAYLOAD_MANIFEST_V1','files':files,'complete_RAW_TYPED_contract_and_sparse_payload_retained':True,'all_raw_original_inputs_unchanged':True,**FALSE_SCIENCE})
        result={'schema':'CURRENT150_AB_ACTUAL_FULL_RAWRECORD_SOFTWARE_TRANSFER_REPORT_V1','status':'ACTUAL_COMPLETE_TWO_READER_RAW_TRANSFER_ONLY_SCIENTIFIC_INPUT_NOT_ADMITTED','source_binding':binding_pin,'actual_child_PID':os.getpid(),'actual_parent_PID':os.getppid(),'child_seconds':elapsed,'declared_original_caps':CAPS,'genuine_supervisor_watch_verified_here':False,'external_actual_ROOT_EXIT0_closed_and_genuine512_watch_review_still_required':True,'states':results,'payload_manifest':full_pin(out/'complete_payload_manifest.json'),'actual_full_raw_and_typed_two_reader_transfer_complete':True,'all_both_reader_records_default_retained':True,'scientific_missing_or_unbound_requirements':['all true loss/reaction event multiplicity semantics and independently bound transport correction','original native LCM/XSM memory bits not independently certified from the ASCII archive alone','same-MG full370x8x3/32fission finite150 coupled reference and original AAA/ABA scientific gates'],'production_model_or_physics_modified':False,**FALSE_SCIENCE}
        write_meta(out/'ACTUAL_TRANSFER_REPORT.json',result)
        require(sum(p.stat().st_size for p in out.rglob('*')if p.is_file())<CAPS['joint_archive_bytes'],'final raw transfer archive ceiling')
        print(json.dumps({'status':result['status'],'report':full_pin(out/'ACTUAL_TRANSFER_REPORT.json'),'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False},allow_nan=False),flush=True)
    except BaseException as error:
        failed=out/'FAILED_TRANSFER_REPORT.json'
        if not failed.exists():
            write_meta(failed,{'schema':'CURRENT150_AB_FULL_RAWRECORD_TRANSFER_FAILURE_V1','status':'ACTUAL_FAILED_OR_PARTIAL_TRANSFER_NO_RETRY_NO_QUALIFICATION','error_type':type(error).__name__,'error':str(error),'completed_states':results,'failure_retained_no_same_namespace_retry':True,**FALSE_SCIENCE})
        raise

if __name__=='__main__':
    main()

import base64
import hashlib
import importlib.util
import json
import math
import os
import stat
import time
from pathlib import Path

TMP = Path('/private/tmp/axmat_v8_actual_prep_independent_review_20261009')
T = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009')
ROOT = Path('/Users/wen/spot')
HELPER = ROOT / 'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
HELPER_SHA = '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
GRAPH_SHA = '242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044'
PINS = {}
START = time.monotonic()

def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(path, sha=None):
    path = Path(path)
    before = identity(path)
    assert stat.S_ISREG(before[2]) and path.parent.resolve(strict=True) == path.parent
    h = hashlib.sha256()
    with path.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino] == before[:2]
        while block := stream.read(4 * 1024**2):
            h.update(block)
    assert identity(path) == before
    record = dict(path=str(path), identity=before, size=before[3], sha256=h.hexdigest())
    if sha:
        assert record['sha256'] == sha, str(path)
    PINS[str(path)] = record
    return record

def read_json(path, sha=None):
    record = pin(path, sha)
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, ('duplicate key', str(path), key)
            result[key] = value
        return result
    def floating(text):
        value = float(text)
        assert math.isfinite(value)
        return value
    def reject(text):
        raise ValueError('nonfinite JSON literal: ' + text)
    value = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_float=floating, parse_constant=reject)
    assert identity(path) == record['identity']
    return value

def canonical_pieces(value):
    return json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).iterencode(value)

def digest(value):
    result = hashlib.sha256()
    for text in canonical_pieces(value):
        result.update(text.encode('utf-8'))
    return result.hexdigest()

def decode_rows(table):
    codec = table['rows']
    assert type(codec) is dict and set(codec) == {'schema', 'encoding', 'row_count', 'column_count', 'data'}
    assert codec['schema'] == 'AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1'
    assert codec['encoding'] == 'CANONICAL_UNSIGNED_LEB128_BASE64'
    assert type(codec['row_count']) is int and codec['row_count'] == 235528
    assert type(codec['column_count']) is int and codec['column_count'] == 5
    assert type(codec['data']) is str and len(codec['data']) % 4 == 0
    raw = base64.b64decode(codec['data'].encode('ascii'), validate=True)
    assert base64.b64encode(raw).decode('ascii') == codec['data']
    assert codec['row_count'] * 5 <= len(raw)
    limits = [len(table['paths']), len(table['paths']), len(table['owners']), len(table['categories']), len(table['binding_roles'])]
    offset = 0
    for _ in range(codec['row_count']):
        row = []
        for limit in limits:
            value = 0
            shift = 0
            groups = 0
            while True:
                assert offset < len(raw)
                byte = raw[offset]
                offset += 1
                groups += 1
                value |= (byte & 127) << shift
                assert value < limit
                if byte < 128:
                    assert groups == 1 or byte != 0
                    break
                shift += 7
                assert shift < max(1, limit.bit_length())
            row.append(value)
        yield tuple(row)
    assert offset == len(raw)

def independent_legacy_digest(graph):
    value = dict(graph)
    value.pop('content_sha256')
    value.pop('wire_encoding')
    value['schema'] = 'AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_V5'
    table = dict(value['requirements'])
    table['schema'] = 'AXMAT_COMBINED_RUNTIME_COMPLETE_TYPED_REQUIREMENT_TABLE_V1'
    h = hashlib.sha256()
    def emit(item):
        for piece in canonical_pieces(item):
            h.update(piece.encode('utf-8'))
    h.update(b'{')
    for index, key in enumerate(sorted(value)):
        if index:
            h.update(b',')
        emit(key)
        h.update(b':')
        if key != 'requirements':
            emit(value[key])
            continue
        h.update(b'{')
        for column, field in enumerate(sorted(table)):
            if column:
                h.update(b',')
            emit(field)
            h.update(b':')
            if field != 'rows':
                emit(table[field])
                continue
            h.update(b'[')
            for row_index, row in enumerate(decode_rows(table)):
                if row_index:
                    h.update(b',')
                h.update(('[' + ','.join(map(str, row)) + ']').encode('ascii'))
            h.update(b']')
        h.update(b'}')
    h.update(b'}')
    return h.hexdigest()

def main():
    config = read_json(T / 'config.json')
    source, out, term = (Path(config[key]) for key in ('SOURCE', 'OUT', 'TERM'))
    assert config['factorySha'] == '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
    assert config['declarationSha'] == '3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae'
    assert config['prepSha'] == 'b61c126fa40179d6133ce4258df599156e0c55a0092227f9ca4669b8a9581c56'
    future_keys = ('sealSha', 'terminalSha', 'terminalPath', 'failed_terminal_sha')
    assert all(config[key] is None for key in future_keys)
    declaration = read_json(out / 'declaration.json', config['declarationSha'])
    assert not (out / 'seal.json').exists() and not (out / 'result.json').exists()
    assert declaration['input_graph']['sha256'] == GRAPH_SHA
    graph_path = out / 'input_graph.json'
    graph = read_json(graph_path, GRAPH_SHA)
    assert pin(graph_path)['size'] == 64639433 < 64 * 1024**2
    assert graph['schema'] == 'AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
    value = dict(graph)
    value.pop('content_sha256')
    wire_digest = digest(value)
    assert wire_digest == graph['content_sha256'] == declaration['input_graph']['content_sha256'] == '78af9070a3bee70e17a098200ed87b34fe97d1584f6dd3274968d68a63ed4ae5'
    table = graph['requirements']
    assert table['columns'] == ['path', 'canonical_path', 'owner', 'category', 'binding_role']
    assert table['duplicate_edges_retained'] is True
    assert table['paths'] == sorted(set(table['paths'])) and table['owners'] == sorted(set(table['owners']))
    roles = {}
    categories = {}
    duplicates = 0
    rows = 0
    row_digest = hashlib.sha256()
    previous_key = None
    for row in decode_rows(table):
        p, canonical, owner, category, role = row
        key = (table['paths'][canonical], table['owners'][owner], table['paths'][p], table['categories'][category], table['binding_roles'][role])
        assert previous_key is None or previous_key <= key
        duplicates += previous_key == key
        previous_key = key
        rows += 1
        row_digest.update(json.dumps(row, separators=(',', ':')).encode('ascii') + b'\n')
        roles[table['binding_roles'][role]] = roles.get(table['binding_roles'][role], 0) + 1
        categories[table['categories'][category]] = categories.get(table['categories'][category], 0) + 1
    assert rows == 235528
    legacy = independent_legacy_digest(graph)
    assert legacy == graph['wire_encoding']['decoded_content_sha256'] == '90c9a6df2dc08b3e28bbf635b84e1150c6f7a76e4cf25346b1823e456726350d'
    print('Independent all-row canonical codec +wire/same-V8 legacy semantic digests PASS', flush=True)
    old_path = ROOT / 'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/input_graph.json'
    old = read_json(old_path, '9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68')
    new_files = {row['path']: row for row in graph['canonical_files']}
    old_files = {row['path']: row for row in old['canonical_files']}
    added = sorted(new_files.keys() - old_files.keys())
    removed = sorted(old_files.keys() - new_files.keys())
    changed_shared = [p for p in new_files.keys() & old_files.keys() if new_files[p] != old_files[p]]
    assert (len(new_files), len(old_files), len(added), len(removed), len(changed_shared)) == (35647, 35646, 15, 14, 0)
    newly_preserved_roots = sorted(set(graph['live_resource_roots']) - set(old['live_resource_roots']))
    assert len(old['live_resource_roots']) == 225 and len(graph['live_resource_roots']) == 228
    assert not set(old['live_resource_roots']) - set(graph['live_resource_roots'])
    assert set(newly_preserved_roots) == {str(source), str(out), str(term)}
    # This reviewed module contains only standard-library metadata mechanics.
    # It does not import a business factory or install its optional audit hook.
    pin(HELPER, HELPER_SHA)
    spec = importlib.util.spec_from_file_location('independent_reviewed_input_metadata_graph', HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.MAX_JSON_BYTES == 67108864 and module.CONSUMER_PHASES == ()
    streams = dict(files=0, bytes=0, all_files_digest=hashlib.sha256())
    original_stream = module._stream
    def progress_stream(*args, **kwargs):
        record, payload = original_stream(*args, **kwargs)
        streams['files'] += 1
        streams['bytes'] += record['size_bytes']
        streams['all_files_digest'].update(json.dumps(record, sort_keys=True, separators=(',', ':')).encode() + b'\n')
        if streams['files'] % 5000 == 0:
            print('Complete pure-metadata fresh byte input union reads:', streams['files'], flush=True)
        return record, payload
    module._stream = progress_stream
    verification = module.verify_graph(str(graph_path), expected_sha256=GRAPH_SHA, phase='independent_actual_V8_PREP_metadata_review')
    assert verification['classification'] == 'FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY'
    assert verification['canonical_files_read'] == 35647 and verification['actual_bytes_read'] == 35803092598
    assert verification['logical_owner_requirements'] == 235528 and verification['exhaustive_namespaces_checked'] == 86 and verification['explicit_aliases_checked'] == 186
    assert verification['typed_snapshot'] == graph['typed_snapshot']
    assert verification['live_subprocesses_reexecuted'] is False and verification['science_qualification_created'] is False
    assert verification['live_resources_verified'] is False and verification['external_declaration_exit0_verified'] is False
    assert len(graph['absence_inputs']) == verification['declared_absence_inputs_checked_before_and_after_bytes'] == 445
    assert streams['files'] == 35648 and streams['bytes'] == 35803092598 + 64639433
    assert pin(HELPER)['sha256'] == HELPER_SHA
    for p, record in PINS.items():
        assert identity(p) == record['identity']
    assert read_json(T / 'config.json') == config
    assert all(config[key] is None for key in future_keys)
    assert not (out / 'seal.json').exists() and not (out / 'result.json').exists()
    for key in ('native_transport_executed', 'mathematical_controls_newly_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted'):
        assert declaration[key] is False
    report = dict(schema='AXMAT_V8_ACTUAL_PREP_INDEPENDENT_COMPLETE_INPUT_METADATA_GRAPH_REVIEW_V1', status='PASS', scope='ACTUAL_PREP_INPUT_METADATA_ONLY_NO_RUNTIME_NATIVE_OR_SCIENCE_ADMISSION',
        config_pin=PINS[str(T / 'config.json')], declaration_pin=PINS[str(out / 'declaration.json')], graph_pin=PINS[str(graph_path)], metadata_helper_pin=PINS[str(HELPER)],
        wire_content_sha256=wire_digest, same_V8_decoded_legacy_content_sha256=legacy, old_V7_graph_semantic_digest_claimed_equal=False,
        complete_rows=rows, row_sequence_sha256=row_digest.hexdigest(), adjacent_duplicate_rows_retained=duplicates, row_role_counts=roles, row_category_counts=categories,
        every_column_symbol_range_and_canonical_unsigned_varint_and_base64_checked=True, saved_second_full_decoded_row_table_built=False,
        canonical_delta_from_V7=dict(previous_count=35646,current_count=35647,added=added,removed_from_current_input_canonical_union=removed,changed_shared=changed_shared,explanation='Twelve family-local bindings move from V7 to the freshly owned V8 SOURCE/OUT paths; the formal factory and graph helper bindings change to their fresh V8 identities; the added private predicate declaration-lifetime helper gives the net plus one. Shared 35632 canonical entries remain byte-identical. Historical resource roots retain every old225 path.'),
        live_resource_roots=dict(previous_count=225,current_count=228,old_roots_missing=[],new_roots=newly_preserved_roots),
        stored_json_bytes=64639433, unchanged_max_json_bytes=67108864, remaining_original_cap_bytes=2469431,
        full_fresh_verification={key: verification[key] for key in ('schema','classification','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources')},
        full_fresh_canonical_pin_sequence_digest=streams['all_files_digest'].hexdigest(), graph_plus_union_read_count=streams['files'], graph_plus_union_read_bytes=streams['bytes'],
        ownership_coverage_and_trace_coverage_rebuilt_exactly=True, namespace_and_alias_before_after_checks_preserved=True,
        only_reviewed_standard_library_metadata_helper_imported=True, business_factory_or_scientific_module_imported=False,
        business_API_or_constructor_or_PREP_or_RUN_executed=False, native_child_or_numeric_solve_executed=False,
        files_deleted=0, formal_or_ART_writes=False, fresh_RUNTIME_RSS_or_AAA_or_ABA_credit=False,
        run_seal_result_absent=True, future_config_seal_and_RUN_fields_None=True,
        audit_source_pin=pin(Path(__file__)), elapsed_seconds=time.monotonic()-START)
    TMP.mkdir(parents=True, exist_ok=True)
    output = TMP / 'complete_graph_actual_PREP_review.json'
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status='PASS',report=str(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),canonical_fresh=35647,complete_rows=235528,namespace_fresh=86,aliases_fresh=186,bytes=35803092598,elapsed_seconds=report['elapsed_seconds'])),flush=True)

if __name__ == '__main__':
    main()

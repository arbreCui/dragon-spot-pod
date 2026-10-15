import base64
import hashlib
import importlib.util
import json
import math
import os
import stat
import shutil
import time
from pathlib import Path

TMP = Path('/private/tmp/axmat_v9_actual_prep_independent_review_20261009')
T = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
ROOT = Path('/Users/wen/spot')
HELPER = ROOT / 'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
HELPER_SHA = '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
GRAPH_SHA = '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
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

def root_validation(roots, art):
    assert type(roots) is list and roots and all(type(p) is str for p in roots)
    paths = [Path(p) for p in roots]
    assert len(paths) == len(set(paths))
    for p in paths:
        assert p.is_absolute() and '..' not in p.parts and art in p.parents
        for ancestor in [p] + list(p.parents):
            s = ancestor.lstat()
            assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode), str(ancestor)
            if ancestor == art:
                break
    for i, p in enumerate(paths):
        assert not any(p in q.parents or q in p.parents for q in paths[i+1:])
    return paths

def dynamic_roots(declared, art):
    return sorted(set(declared) | {str(p) for p in art.glob('axial-material-*')})

def resource_inventory(roots, art):
    # Reproduce the inherited no-follow apparent-byte scope using only stdlib.
    # Regular hard links count per path, matching the original resource contract.
    root_validation(roots, art)
    total = 0
    regular = 0
    directories = 0
    symlinks_ignored = 0
    h = hashlib.sha256()
    def emit(kind, path, s):
        record = [kind, str(path), s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]
        h.update(json.dumps(record,separators=(',',':')).encode() + b'\n')
    def visit(path):
        nonlocal total, regular, directories, symlinks_ignored
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            s = os.fstat(fd)
            emit('directory',path,s)
            directories += 1
            with os.scandir(fd) as iterator:
                entries = sorted(iterator, key=lambda e:e.name)
            for entry in entries:
                p = path / entry.name
                s = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):
                    visit(p)
                elif stat.S_ISREG(s.st_mode):
                    emit('regular',p,s)
                    total += s.st_size
                    regular += 1
                elif stat.S_ISLNK(s.st_mode):
                    emit('ignored_symlink',p,s)
                    symlinks_ignored += 1
                else:
                    emit('other_ignored',p,s)
        finally:
            os.close(fd)
    for path in map(Path,roots):
        visit(path)
    return dict(artifact_bytes=total,regular_files=regular,directories=directories,symlinks_ignored=symlinks_ignored,
                full_path_identity_inventory_sha256=h.hexdigest(),scope='Original complete axial-family live resource roots; no symlink following; apparent bytes per regular path')

def main():
    config = read_json(T / 'config.json')
    source, out, term = (Path(config[key]) for key in ('SOURCE', 'OUT', 'TERM'))
    assert config['factorySha'] == '44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
    assert config['declarationSha'] == '7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0'
    assert config['prepSha'] == '0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'
    pin(config['F'],config['factorySha'])
    pin(term / 'declaration_terminal_return.json',config['prepSha'])
    future_keys = ('sealSha', 'terminalSha', 'terminalPath', 'failed_terminal_sha')
    assert all(config[key] is None for key in future_keys)
    declaration = read_json(out / 'declaration.json', config['declarationSha'])
    assert not (out / 'seal.json').exists() and not (out / 'result.json').exists()
    assert declaration['input_graph']['sha256'] == GRAPH_SHA
    graph_path = out / 'input_graph.json'
    graph = read_json(graph_path, GRAPH_SHA)
    graph_bytes = PINS[str(graph_path)]['size']
    assert graph_bytes == 64644869 < 64 * 1024**2
    assert graph['schema'] == 'AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
    value = dict(graph)
    value.pop('content_sha256')
    wire_digest = digest(value)
    assert wire_digest == graph['content_sha256'] == declaration['input_graph']['content_sha256'] == 'f91b0168754de2d1e207eda794bd5b4ecd143f84c53f58c27fbb7d45e24ff946'
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
    assert legacy == graph['wire_encoding']['decoded_content_sha256'] == 'e9634f406032b9872240ae0be7abd28159389146fa020494d03a4787264b05d2'
    print('Independent all235528-row canonical codec +wire/same-V9 legacy semantic digests PASS', flush=True)
    old_path = ROOT / 'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/input_graph.json'
    old = read_json(old_path, '242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
    new_files = {row['path']: row for row in graph['canonical_files']}
    old_files = {row['path']: row for row in old['canonical_files']}
    assert len(new_files) == len(graph['canonical_files']) and len(old_files) == len(old['canonical_files'])
    added = sorted(new_files.keys() - old_files.keys())
    removed = sorted(old_files.keys() - new_files.keys())
    changed_shared = sorted(p for p in new_files.keys() & old_files.keys() if new_files[p] != old_files[p])
    assert len(new_files) == len(old_files) == 35647 and len(added) == len(removed)
    assert changed_shared == []
    newly_preserved_roots = sorted(set(graph['live_resource_roots']) - set(old['live_resource_roots']))
    assert len(old['live_resource_roots']) == 228 and len(graph['live_resource_roots']) == 231
    assert not set(old['live_resource_roots']) - set(graph['live_resource_roots'])
    assert set(newly_preserved_roots) == {str(source), str(out), str(term)}
    assert graph['live_resource_roots'] == declaration['resource_roots'] == declaration['resources_before']['resource_roots']
    art = ROOT / 'validation/artifacts'
    declared = declaration['resources_before']['declared_resource_roots']
    roots = graph['live_resource_roots']
    assert dynamic_roots(declared, art) == roots
    assert declaration['artifact_budget_bytes'] == declaration['resources_before']['artifact_budget_bytes'] == 96 * 1024**3
    assert declaration['min_free_bytes'] == declaration['resources_before']['min_free_bytes'] == 8 * 1024**3
    assert declaration['archive_reserve_bytes'] == 2 * 1024**3
    assert declaration['resources_before']['artifact_bytes'] < 96 * 1024**3
    assert declaration['resources_before']['disk_free_bytes'] >= 8 * 1024**3
    assert declaration['resources_before']['artifact_bytes'] + declaration['archive_reserve_bytes'] < 96 * 1024**3
    assert declaration['resources_before']['disk_free_bytes'] - declaration['archive_reserve_bytes'] >= 8 * 1024**3
    resource_before = resource_inventory(roots, art)
    resource_free_before = shutil.disk_usage(art).free
    print('Complete231 original resource roots read before byte audit:',resource_before['regular_files'],'regular files',resource_before['artifact_bytes'],'apparent bytes',flush=True)
    # Only this reviewed stdlib metadata module is imported. No business factory,
    # optional audit hook, scientific provider, or constructor is imported/called.
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
    expected_canonical_bytes = sum(record['size_bytes'] for record in graph['canonical_files'])
    assert expected_canonical_bytes == 35803098221
    verification = module.verify_graph(str(graph_path), expected_sha256=GRAPH_SHA, phase='independent_actual_V9_PREP_metadata_review')
    assert verification['classification'] == 'FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY'
    assert verification['canonical_files_read'] == len(new_files) and verification['actual_bytes_read'] == expected_canonical_bytes
    assert verification['logical_owner_requirements'] == rows and verification['exhaustive_namespaces_checked'] == len(graph['namespaces']) == 86 and verification['explicit_aliases_checked'] == len(graph['aliases']) == 186
    assert verification['typed_snapshot'] == graph['typed_snapshot']
    assert verification['live_subprocesses_reexecuted'] is False and verification['science_qualification_created'] is False
    assert verification['live_resources_verified'] is False and verification['external_declaration_exit0_verified'] is False
    assert len(graph['absence_inputs']) == verification['declared_absence_inputs_checked_before_and_after_bytes'] == 445
    assert streams['files'] == len(new_files)+1 and streams['bytes'] == expected_canonical_bytes + graph_bytes
    resource_after = resource_inventory(roots, art)
    resource_free_after = shutil.disk_usage(art).free
    assert resource_after == resource_before
    assert dynamic_roots(declared, art) == roots
    root_validation(roots, art)
    assert resource_after['artifact_bytes'] < 96 * 1024**3 and resource_after['artifact_bytes']+2*1024**3 < 96*1024**3
    assert min(resource_free_before,resource_free_after) >= 8 * 1024**3
    assert pin(HELPER)['sha256'] == HELPER_SHA
    for p, record in PINS.items():
        assert identity(p) == record['identity']
    assert read_json(T / 'config.json') == config
    assert all(config[key] is None for key in future_keys)
    assert not (out / 'seal.json').exists() and not (out / 'result.json').exists()
    for key in ('native_transport_executed', 'mathematical_controls_newly_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted'):
        assert declaration[key] is False
    report = dict(schema='AXMAT_V9_ACTUAL_PREP_INDEPENDENT_COMPLETE_INPUT_METADATA_GRAPH_REVIEW_V1', status='PASS', scope='ACTUAL_PREP_INPUT_METADATA_ONLY_NO_RUNTIME_NATIVE_OR_SCIENCE_ADMISSION',
        config_pin=PINS[str(T / 'config.json')], declaration_pin=PINS[str(out / 'declaration.json')], graph_pin=PINS[str(graph_path)], metadata_helper_pin=PINS[str(HELPER)],
        wire_content_sha256=wire_digest, same_V9_decoded_legacy_content_sha256=legacy, old_V8_graph_semantic_digest_claimed_equal=False,
        complete_rows=rows, row_sequence_sha256=row_digest.hexdigest(), adjacent_duplicate_rows_retained=duplicates, row_role_counts=roles, row_category_counts=categories,
        every_column_symbol_range_and_canonical_unsigned_varint_and_base64_checked=True, saved_second_full_decoded_row_table_built=False,
        canonical_delta_from_V8=dict(previous_count=len(old_files),current_count=len(new_files),added=added,removed_from_current_input_canonical_union=removed,changed_shared=changed_shared,shared_unchanged_count=len(new_files.keys() & old_files.keys()),explanation='Actual complete union comparison: family-local bindings and formal factory/current-predicate helper identities are freshly retargeted. Every shared record remains identical; old paths removed from this current input union remain in retained immutable historical resource roots. No equal prior-V8 semantic digest claim.'),
        live_resource_roots=dict(previous_count=228,current_count=231,old_roots_missing=[],new_roots=newly_preserved_roots,full_current_roots=roots,all_original_declared_extras_retained=True,actual_current_dynamic_union_exact=True),
        full_history_resources=dict(original_caps_retained=True,original_budget_bytes=96*1024**3,original_min_free_bytes=8*1024**3,original_reservation_bytes=2*1024**3,Root_actual_PREP_before=declaration['resources_before'],independent_before=resource_before,independent_after=resource_after,disk_free_before=resource_free_before,disk_free_after=resource_free_after,current_identity_inventory_stable_before_after=True,Root_before_and_current_exact_bytes_claimed_equal=False,filesystem_free_change_attributed_to_PREP=False),
        stored_json_bytes=graph_bytes, unchanged_max_json_bytes=67108864, remaining_original_cap_bytes=67108864-graph_bytes,
        full_fresh_verification={key: verification[key] for key in ('schema','classification','scope','phase','graph_content_sha256','fresh_reader_contract','canonical_files_read','actual_bytes_read','byte_count_scope','logical_owner_requirements','exhaustive_namespaces_checked','explicit_aliases_checked','live_subprocesses_reexecuted','declared_absence_inputs_checked_before_and_after_bytes','science_qualification_created','live_resources_verified','external_declaration_exit0_verified','caller_must_verify_live_environment_modules_PID_time_and_resources')},
        full_fresh_canonical_pin_sequence_digest=streams['all_files_digest'].hexdigest(), graph_plus_union_read_count=streams['files'], graph_plus_union_read_bytes=streams['bytes'],
        ownership_coverage_and_trace_coverage_rebuilt_exactly=True, namespace_and_alias_before_after_checks_preserved=True,
        only_reviewed_standard_library_metadata_helper_imported=True, business_factory_or_scientific_module_imported=False,
        business_API_or_constructor_or_PREP_or_RUN_executed=False, native_child_or_numeric_solve_executed=False,
        files_deleted=0, formal_or_ART_writes=False, fresh_RUNTIME_RSS_or_AAA_or_ABA_credit=False,
        run_seal_result_absent=True, future_config_seal_and_RUN_fields_None=True,
        small_SOURCE_witness_scope_review_separately_required=True,
        audit_source_pin=pin(Path(__file__)), elapsed_seconds=time.monotonic()-START)
    output = TMP / 'complete_graph_actual_PREP_review.json'
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status='PASS',report=str(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),canonical_fresh=len(new_files),complete_rows=rows,namespace_fresh=86,aliases_fresh=186,bytes=expected_canonical_bytes,elapsed_seconds=report['elapsed_seconds'])),flush=True)

if __name__ == '__main__':
    main()

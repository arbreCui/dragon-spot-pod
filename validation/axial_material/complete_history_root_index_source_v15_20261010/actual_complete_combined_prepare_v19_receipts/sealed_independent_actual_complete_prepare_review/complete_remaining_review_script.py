"""Finite saved PREP evidence review. Standard-library I/O only; no project import/API/business."""
import ast
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
import time

OUT = Path(__file__).parent
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E = BASE / 'actual_complete_combined_prepare_v19_receipts'
SUMMARY = E / 'Root_actual_complete_combined_prepare_summary.json'
NAMESPACE = E / 'Root_actual_complete_prepare_namespace_manifest.json'
START = time.monotonic()
PRIOR = json.loads((OUT/'REVIEW.json').read_text())
assert PRIOR['status'] == 'ACTUAL_PREP_EVIDENCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE'
assert PRIOR['blocking_findings'] == ["ValueError('fresh_H_S_O_T_D_full_regular_byte_total_matches_saved_ROOT')"]
assert len(PRIOR['file_pins']) == 82
checks = {k:v for k,v in PRIOR['checks'].items() if k != 'fresh_H_S_O_T_D_full_regular_byte_total_matches_saved_ROOT'}
assert all(type(v) is bool and v is True for v in checks.values())
pins = dict(PRIOR['file_pins'])
raw_cache = {}
keep = {str(SUMMARY), str(NAMESPACE)}
namespace_witnesses = []

def check(label, condition):
    if type(condition) is not bool:
        raise TypeError('nonboolean check: ' + label)
    checks[label] = condition
    if condition is not True:
        raise ValueError(label)

def identity(path, follow=False):
    s = path.stat() if follow else path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def finite(value):
    return type(value) in (int, float) and value == value and abs(value) < float('inf')

def file_pin(path, expected=None, wanted_sha=None):
    path = Path(path)
    key = str(path)
    check('bounded_readonly_project_path:' + key, key.startswith('/Users/wen/spot/'))
    if key not in pins:
        before = identity(path)
        check('regular_no_symlink:' + key, stat.S_ISREG(before[2]))
        digest = hashlib.sha256()
        count = 0
        parts = [] if key in keep else None
        with path.open('rb') as f:
            while True:
                block = f.read(2**20)
                if not block:
                    break
                digest.update(block)
                count += len(block)
                if parts is not None:
                    parts.append(block)
        after = identity(path)
        check('fresh_full_EOF_and_7ID_stable:' + key, count == before[4] and before == after)
        pins[key] = dict(path=key, sha256=digest.hexdigest(), size_bytes=count, before7ID=before, after7ID=after)
        if parts is not None:
            raw_cache[key] = b''.join(parts)
    pin = pins[key]
    check('retained_first_pass_hash_fresh_current_7ID:' + key, identity(path) == pin['after7ID'])
    if key in keep and key not in raw_cache:
        before = identity(path)
        raw = path.read_bytes()
        after = identity(path)
        check('remaining_metadata_full_EOF_same_original_hash_7ID:' + key, before == after == pin['after7ID'] and len(raw) == pin['size_bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'])
        raw_cache[key] = raw
    if expected is not None:
        check('saved_path_exact:' + key, expected['path'] == key)
        check('saved_SHA_exact:' + key, expected['sha256'] == pin['sha256'])
        if 'identity' in expected:
            check('saved_7ID_exact:' + key, expected['identity'] == pin['before7ID'])
    if wanted_sha is not None:
        check('fixed_SHA_exact:' + key, pin['sha256'] == wanted_sha)
    return pin

def read_json(path, expected=None, wanted_sha=None):
    key = str(path)
    keep.add(key)
    file_pin(path, expected, wanted_sha)
    check('metadata_bytes_cached_once:' + key, key in raw_cache)
    return json.loads(raw_cache[key])

def enumerate_namespace(root):
    files = {}
    directories = {}
    symlinks = {}
    before_root = identity(root)
    def walk(directory):
        with os.scandir(directory) as it:
            entries = sorted(it, key=lambda e: e.name)
        for entry in entries:
            p = Path(entry.path)
            rel = str(p.relative_to(root))
            ident = identity(p)
            if stat.S_ISREG(ident[2]):
                files[rel] = p
            elif stat.S_ISDIR(ident[2]):
                directories[rel] = ident
                walk(p)
            elif stat.S_ISLNK(ident[2]):
                symlinks[rel] = dict(target=os.readlink(p), identity=ident)
            else:
                raise ValueError('unsupported saved namespace node: ' + str(p))
    walk(root)
    after_root = identity(root)
    check('namespace_root_7ID_stable:' + str(root), before_root == after_root)
    return files, directories, symlinks, before_root

review = dict(
    schema='AXMAT_V19_INDEPENDENT_ACTUAL_COMPLETE_PREP_EVIDENCE_REVIEW_V1',
    scope='SAVED_ACTUAL_COMPLETE_PREP_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE',
    project_module_imported=False, project_API_or_helper_called=False,
    business_executed=False, numeric_computation_or_payload_interpretation=False,
    resource_or_guard_called=False, original_namespace_or_input_modified=False,
    physical_precision_or_balance_qualified=False, cleanup_performed=False,
    blocking_findings=[])

try:
    summary = read_json(SUMMARY, wanted_sha='17992f59e84611b0456e3451f0e6abbdc56baf2a0e985f5e1ad895d24e52c046')
    manifest = read_json(NAMESPACE, wanted_sha='603ed9d1088b94ac5519d63e03b4b2eacabed27baf013c34906cf925985fc9eb')
    check('summary_truthful_PREP_only_status', summary['status'] == 'ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
    check('five_complete_saved_namespaces', len(manifest['namespaces']) == 5)
    H, S, O, T, D = [Path(n['root']) for n in manifest['namespaces']]
    expected_counts = (5, 11, 4, 6, 42)
    inputs = manifest['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']
    check('all_51_saved_original_input_descriptors_unique', len(inputs) == len({x['path'] for x in inputs}) == 51)
    root_terminal = Path(summary['actual_root_terminal']['path'])
    formal_terminal = Path(summary['formal_PREP_terminal']['path'])
    graph_path = Path(summary['actual_input_graph']['path'])
    declaration_path = Path(summary['actual_declaration']['path'])
    support_path = BASE / 'actual_prepare_sources/prepare_cli_host_v15.py'
    metadata_paths = [H/'result.json', H/'COMBINED_PREPARATION/stages.json', H/'run/prepare.watchdog.json', H/'run/prepare.log', declaration_path, graph_path, root_terminal, formal_terminal, T/'Root_actual_SOURCE_inventory.json', T/'actual_external_host_stdout.json', T/'actual_child_merged_stdout_stderr.json', T/'actual_external_host_stderr.txt', T/'actual_external_Root_tool_terminal.json', S/'source_admission.json', D/'combined_prepare_host.py', D/'sealed_independent_normal_PREP_host_source_review/REVIEW.json', support_path, E/'Root_prelaunch_complete_source_freeze.json', E/'Root_final_prelaunch_source_and_reserve_check.json', E/'parent_stdout.log', E/'parent_stderr.log']
    keep.update(str(p) for p in metadata_paths)
    for i, namespace in enumerate(manifest['namespaces']):
        root = Path(namespace['root'])
        actual_files, actual_dirs, actual_syms, root_id = enumerate_namespace(root)
        check('complete_namespace_file_count:' + str(root), len(actual_files) == len(namespace['files']) == expected_counts[i])
        check('complete_namespace_file_names:' + str(root), set(actual_files) == set(namespace['files']))
        expected_dirs = {x['path']: x['identity'] for x in namespace['directories']}
        check('complete_namespace_directories_7ID:' + str(root), actual_dirs == expected_dirs)
        check('complete_namespace_no_symlinks_exact:' + str(root), actual_syms == namespace['symlinks'] == {})
        for rel, expected in namespace['files'].items():
            check('saved_relative_absolute_name:' + str(root/rel), Path(expected['path']) == root/rel)
            file_pin(root/rel, expected)
        namespace_witnesses.append(dict(root=str(root), root7ID=root_id, regular_files=len(actual_files), directories=actual_dirs, symlinks=actual_syms, full_SHA7ID_verified=True, regular_bytes=sum(namespace['files'][rel]['identity'][4] for rel in actual_files)))
    for entry in inputs:
        file_pin(entry['path'], entry)
    for key in ('actual_root_terminal', 'formal_PREP_terminal', 'actual_host_result', 'actual_declaration', 'actual_input_graph', 'actual_complete_input_graph', 'actual_complete_creation_trace', 'namespace_manifest'):
        entry = summary[key]
        file_pin(entry['path'], entry)
    canonical = manifest['canonical_factory']
    file_pin(canonical['path'], canonical, '34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b')
    host = read_json(H/'result.json')
    declaration = read_json(declaration_path)
    formal = read_json(formal_terminal)
    terminal = read_json(root_terminal)
    watch = read_json(H/'run/prepare.watchdog.json')
    stages = read_json(H/'COMBINED_PREPARATION/stages.json')
    freeze = read_json(E/'Root_prelaunch_complete_source_freeze.json')
    prelaunch = read_json(E/'Root_final_prelaunch_source_and_reserve_check.json')
    host_source = raw_cache[str(D/'combined_prepare_host.py')].decode()
    source_review = read_json(D/'sealed_independent_normal_PREP_host_source_review/REVIEW.json')
    support_source = raw_cache[str(support_path)].decode()
    input_by_path = {entry['path']: entry for entry in inputs}
    host_input_union = host['input_sources'] + [host['original_helper'], host['resource_factory']]
    check('actual_host_before_after_51_descriptors_equal_Root_closed_pins', len(host['input_sources']) == 49 and len(host_input_union) == 51 and {entry['path']: entry for entry in host_input_union} == input_by_path)
    for entry in host_input_union:
        file_pin(entry['path'], entry)
    check('frozen_D_42files_same_full_SHA7ID_as_prelaunch', freeze['all_source_files'] == manifest['namespaces'][4]['files'])
    file_pin(freeze['canonical_factory']['path'], freeze['canonical_factory'])
    file_pin(freeze['host']['path'], freeze['host'])
    check('prelaunch_complete_source_freeze_flags_true', freeze['all_business_namespaces_absent'] is True and freeze['business_executed'] is False and prelaunch['all42_frozen_source_files_full_SHA7ID_unchanged'] is True and prelaunch['canonical_factory_and_host_full_SHA7ID_unchanged'] is True and prelaunch['all4_business_namespaces_absent'] is True)
    check('genuine_host_source_fixed_f5c947', pins[str(D/'combined_prepare_host.py')]['sha256'] == 'f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580')
    check('source_qualified_genuine_guard_MRO_and_POST_pin_checks_retained', 'helper.guard_admission(full)' in host_source and 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)' in host_source and 'type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources' in host_source and 'for entry in inputs+[hpin,rpin]:' in host_source and "support.pin(entry['path'],entry['sha256'])!=entry" in host_source and 'STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30' in host_source)
    support_tree = ast.parse(support_source)
    pin_function = next(n for n in support_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'pin')
    pin_segment = ast.get_source_segment(support_source, pin_function)
    check('original_support_pin_reads_complete_bytes_and_stat_identity', "path.open('rb')" in pin_segment and "hashlib.file_digest(stream, 'sha256')" in pin_segment and 'identity(path) != before' in pin_segment and "'identity': before" in pin_segment)
    check('genuine_guard_MRO_profile_record_flags_unmodified', host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False and prelaunch['original_guard_class_MRO_unchanged'] is True)
    check('actual_root_terminal_typed_integer0_closed_not_repolled', type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and terminal['closed'] is True and terminal['session_repolled_after_close'] is False and terminal['original_session_id'] == 2985 and terminal['initial_tool_return']['chunk_id'] == '03c3a5' and terminal['initial_tool_return']['session_id'] == 2985 and terminal['terminal_tool_return']['chunk_id'] == 'c5790b' and type(terminal['terminal_tool_return']['exit_code']) is int and terminal['terminal_tool_return']['exit_code'] == 0 and 'session_id' not in terminal['terminal_tool_return'])
    check('formal_PREP_terminal_binds_actual_external_closed_return', type(formal['returncode']) is int and formal['returncode'] == 0 and formal['actual_tool_result'] == terminal['terminal_tool_return'] and formal['record_written_after_actual_terminal_return'] is True and formal['actual_tool_terminal_return_observed'] is True)
    check('formal_actual_ROOT_tool_return_copy_byteexact', raw_cache[str(T/'actual_external_Root_tool_terminal.json')] == raw_cache[str(root_terminal)])
    command = ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py', 'prepare-build']
    check('actual_canonical_child_command_exact', watch['command'] == host['actual_canonical_command'] == formal['command'] == command)
    check('actual_child_watchdog_same_saved_host_watchdog', watch == host['watchdog'])
    check('actual_child_watchdog_typed_PID_returncode_and_cleanup', type(watch['pid']) is int and watch['pid'] == 96184 and type(watch['returncode']) is int and watch['returncode'] == 0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
    check('one_actual_genuine_PREP_stage_PASS_full_log_and_saved_receipts', host['stage_records'] == stages['stages'] and len(host['stage_records']) == 1 and host['stage_records'][0]['label'] == 'run/prepare' and host['stage_records'][0]['status'] == 'PASS' and host['stage_records'][0]['command'] == command and host['stage_records'][0]['log_sha256'] == pins[str(H/'run/prepare.log')]['sha256'])
    cap_expected = dict(whole_wall_cap_seconds=1800, stage_wall_cap_seconds=600, rss_mib=512, joint_archive_cap_bytes=2*2**30, history_cap_bytes=96*2**30, free_floor_bytes=8*2**30, threads=1, children=1, retries=0)
    check('actual_summary_all_original_caps_exact', all(summary[k] == v for k, v in cap_expected.items()) and summary['original_caps_preserved'] is True)
    check('actual_host_original_caps_exact', (host['whole_wall_cap_seconds'], host['stage_wall_cap_seconds'], host['rss_cap_mib'], host['archive_cap_bytes'], host['threads'], host['children_at_once'], host['retries']) == (1800, 600, 512, 2*2**30, 1, 1, 0))
    check('complete_declaration_original_five_stages_and_limits', declaration['stages'] == ['build/link', 'metadata/objects', 'metadata/executable', 'metadata/dependencies', 'audit/audit'] and (declaration['total_wall_seconds'], declaration['stage_wall_seconds'], declaration['rss_cap_mib'], declaration['archive_reserve_bytes'], declaration['artifact_budget_bytes'], declaration['min_free_bytes'], declaration['threads'], declaration['numeric_children_at_once'], declaration['retries']) == (1800, 600, 512, 2*2**30, 96*2**30, 8*2**30, 1, 1, 0))
    check('measured_elapsed_and_RSS_finite_below_original_limits', all(finite(v) for v in (summary['whole_seconds'], summary['child_seconds'], summary['sampled_peak_rss_mib'], watch['wall_cap_seconds'], host['stage_records'][0]['elapsed_seconds'])) and summary['whole_seconds'] == host['whole_seconds'] == 199.32746954192407 and summary['child_seconds'] == watch['elapsed_seconds'] == 198.1557341669686 and summary['sampled_peak_rss_mib'] == watch['sampled_peak_rss_mib'] == 473.09375 and 0 <= watch['sampled_peak_rss_mib'] < watch['rss_cap_mib'] == 512 and 0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= 600 and 0 <= host['stage_records'][0]['elapsed_seconds'] < 600 and 0 <= host['whole_seconds'] < 1800)
    for label, resources in [('host_before', host['resources_before']), ('host_after', host['resources_after']), ('stage_before', host['stage_records'][0]['resource_before']), ('stage_after', host['stage_records'][0]['resource_after']), ('prelaunch', prelaunch['genuine_resource_state'])]:
        check('saved_real_resource_caps_and_finite_values:' + label, resources['min_free_bytes'] == 8*2**30 and resources['artifact_budget_bytes'] == 96*2**30 and type(resources['artifact_bytes']) is int and 0 <= resources['artifact_bytes'] < 96*2**30 and type(resources['disk_free_bytes']) is int and resources['disk_free_bytes'] >= 8*2**30 and resources['resource_scope_policy'] == 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and resources['resource_scope_contract']['all_declared_extras_retained'] is True and resources['resource_scope_contract']['entire_project_artifact_cap_claimed'] is False)
    check('original_full_2GiB_reserve_was_available_before_child', host['resources_before']['artifact_bytes'] + 2*2**30 < 96*2**30 and host['resources_before']['disk_free_bytes'] - 2*2**30 >= 8*2**30 and prelaunch['original_2GiB_reserve_passed'] is True)
    actual_joint = sum(n['regular_bytes'] for n in namespace_witnesses)
    later_E_metadata_names = {'Root_actual_complete_combined_prepare_summary.json', 'REPORT.txt', 'Root_actual_full_encoded_graph_metadata_counts.json', 'Root_actual_full_encoded_graph_metadata_counts_initial_incorrect_wrapper_count.json'}
    E_regular = [p for p in E.iterdir() if p.is_file() and not p.is_symlink()]
    saved_pre_summary_E_bytes = sum(p.stat().st_size for p in E_regular if p.name not in later_E_metadata_names)
    current_E_bytes = sum(p.stat().st_size for p in E_regular)
    canonical_bytes = pins[canonical['path']]['size_bytes']
    check('correct_saved_ROOT_archive_scope_H_S_O_T_D_E_before_summary_plus_FACTORY', actual_joint == 138488083 and saved_pre_summary_E_bytes == 200940 and canonical_bytes == 180593 and actual_joint + saved_pre_summary_E_bytes + canonical_bytes == summary['joint_archive_bytes'] == 138869616)
    check('current_all_saved_archive_with_later_E_metadata_still_below_original_2GiB', actual_joint + current_E_bytes + canonical_bytes < 2*2**30 and 0 <= host['archive_before_result_bytes'] <= actual_joint)
    keep.add(str(E/'write_actual_prepare_terminal.py'))
    writer_pin = file_pin(E/'write_actual_prepare_terminal.py')
    writer_text = raw_cache[str(E/'write_actual_prepare_terminal.py')].decode()
    check('actual_ROOT_metadata_writer_archive_scope_matches_saved_number', 'total=sum(p.stat().st_size for root in (H,S,O,T,D,E)' in writer_text and '+FACTORY.stat().st_size' in writer_text)

    inventory = read_json(T/'Root_actual_SOURCE_inventory.json')
    check('formal_source_inventory_all11files_exact', inventory['files'] == {rel: entry['sha256'] for rel, entry in manifest['namespaces'][1]['files'].items()} and inventory['symlinks'] == {} and set(inventory['directories']) == {'runtime'} and summary['all_source_files_verified_count'] == 11)
    child_stdout = raw_cache[str(T/'actual_child_merged_stdout_stderr.json')]
    check('full_formal_child_merged_stream_byteexact_to_actual_log', child_stdout == raw_cache[str(H/'run/prepare.log')] and json.loads(child_stdout) == {'declaration': str(declaration_path), 'declaration_sha256': pins[str(declaration_path)]['sha256']})
    file_pin(E/'parent_stdout.log')
    file_pin(E/'parent_stderr.log')
    check('full_formal_real_external_host_stream_copies_exact', raw_cache[str(E/'parent_stdout.log')] == raw_cache[str(T/'actual_external_host_stdout.json')] and raw_cache[str(E/'parent_stderr.log')] == raw_cache[str(T/'actual_external_host_stderr.txt')] == b'')
    check('formal_stream_labels_honest_no_separate_child_stderr_claim', formal['full_stdout_scope'] == 'ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope'] == 'ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False)
    for entry in (formal['full_stdout'], formal['full_stderr'], formal['source_inventory'], formal['actual_child_watchdog'], formal['actual_root_host_terminal_tool_return'], formal['actual_root_host_stdout'], formal['source'], formal['declaration'], formal['input_graph'], formal['original_executor_merged_capture_source']):
        file_pin(entry['path'], entry)
    check('formal_records_actual_child_vs_outer_ROOT_distinct', formal['actual_root_host_launchargs'] == terminal['actual_launch_arguments'] and formal['actual_child_watchdog']['path'] == str(H/'run/prepare.watchdog.json'))
    for key in ('genuine_supervisor_source', 'genuine_parent_class_source', 'actual_local_supervisor_helper', 'actual_resource_class_factory'):
        entry = declaration[key]
        file_pin(entry['path'], entry)
    check('actual_genuine619_705_38de_bc_ebbb_source_pins_exact', host['original_helper']['sha256'] == '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743' and declaration['genuine_supervisor_source']['sha256'] == '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6' and declaration['genuine_parent_class_source']['sha256'] == '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128' and declaration['actual_local_supervisor_helper']['sha256'] == 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09' and host['resource_factory']['sha256'] == declaration['actual_resource_class_factory']['sha256'] == 'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')
    check('recorded_genuine_constructor_preflight_scope_only', declaration['actual_supervisor_constructor_preflight']['actual_original_constructor_exercised'] is True and declaration['actual_supervisor_constructor_preflight']['native_or_numeric_child_launched'] is False and declaration['actual_resource_class_factory']['genuine_class_not_overlay'] is True)
    check('graph_and_trace_full_EOF_fixed_lengths_SHA', pins[str(graph_path)]['size_bytes'] == 45526587 and pins[str(graph_path)]['sha256'] == '257ddbd44f3123dd85f7b0cf50572ca68c92475b9a491ef83d0ec21b74e63d60' and pins[summary['actual_complete_creation_trace']['path']]['size_bytes'] == 40959538 and pins[summary['actual_complete_creation_trace']['path']]['sha256'] == 'c1e2daeef559de7c518ce7407230c43e5c911062e3d744651e8a6e007dd05712')
    encoded = json.loads(raw_cache.pop(str(graph_path)))
    check('standard_library_parse_encoded_complete_graph_only', encoded['schema'] == 'AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1' and isinstance(encoded['graph'], dict) and declaration['input_graph']['scope'] == formal['input_graph']['scope'] == 'COMPLETE_HISTORICAL_INPUT_ONLY')
    graph = encoded['graph']
    graph_shape = {key: dict(type=type(value).__name__, count=len(value) if isinstance(value, (dict, list)) else None) for key, value in graph.items()}
    requirement_codec = graph['requirements']['rows']
    check('encoded_requirement_rows_wrapper_metadata_not_five_dict_keys', set(requirement_codec) == {'schema', 'encoding', 'row_count', 'column_count', 'data'} and requirement_codec['schema'] == 'AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1' and requirement_codec['encoding'] == 'CANONICAL_UNSIGNED_LEB128_BASE64' and type(requirement_codec['row_count']) is int and requirement_codec['row_count'] == 238441 and type(requirement_codec['column_count']) is int and requirement_codec['column_count'] == 5 and isinstance(requirement_codec['data'], str))
    requirement_raw = base64.b64decode(requirement_codec['data'], validate=True)
    check('independent_saved_metadata_varint_cell_count_matches_rows_times5', len(requirement_raw) > 0 and requirement_raw[-1] < 128 and sum(byte < 128 for byte in requirement_raw) == requirement_codec['row_count'] * requirement_codec['column_count'])
    del requirement_raw
    canonical_rows = graph['canonical_files']['rows']
    trace_table = graph['read_trace']['records']
    graph_rows = dict(requirements=238441, requirement_columns=5, canonical_files=len(canonical_rows), owners=len(graph['owners']), namespaces=len(graph['namespaces']), aliases=len(graph['aliases']), read_trace_records=trace_table['row_count'], absences=len(graph['absence_inputs']), closure_categories=len(graph['closure_categories']))
    check('actual_complete_saved_graph_metadata_counts', graph_rows == dict(requirements=238441, requirement_columns=5, canonical_files=37111, owners=4473, namespaces=86, aliases=186, read_trace_records=63452, absences=479, closure_categories=9) and isinstance(canonical_rows, list) and type(trace_table['row_count']) is int and trace_table['row_count'] == len(trace_table['rows']))
    check('saved_graph_no_new_declaration_consumer_or_science_scope', graph['newly_declared_input_paths'] == [] and graph['newly_declared_input_pins'] == {} and graph['consumer_scope'] is None and graph['science_qualification_created'] is False and graph['live_resources_verified'] is False and graph['external_declaration_exit0_verified'] is False and len(graph['coverage']) == 9)
    graph_count_metadata = {key: value for key, value in graph.items() if type(value) in (int, bool, str) and len(str(value)) <= 300}
    graph_shape['storage_top_keys'] = list(encoded)
    del graph, encoded
    flags = ('new_five_stage_build_executed', 'whole_combined_INPUT_admitted', 'new_native_transport_executed', 'AAA_accuracy_qualified', 'ABA_admitted', 'goal_complete', 'original_five_build_stages_executed', 'native_RSS_qualified', 'cleanup_performed')
    check('summary_all_build_INPUT_native_science_goal_flags_typed_false', all(summary[k] is False for k in flags))
    check('root_terminal_does_not_promote_PREP_to_build_INPUT_native_science', all(terminal[k] is False for k in ('new_five_stage_build_executed', 'whole_combined_INPUT_executed', 'new_native_transport_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('formal_terminal_no_build_math_native_precision_claim', all(formal[k] is False for k in ('successful_new_runtime_build_observed', 'original_component_APIs_executed_now', 'native_transport_executed', 'mathematical_controls_newly_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('declaration_fullscope_preserved_no_build_native_science_credit', declaration['input_graph_source_root_inventory_is_exhaustive'] is True and declaration['historical_whole_component_body']['whole_seven_key_body_retained'] is True and declaration['historical_whole_component_body']['original_component_API_execution_claimed'] is False and declaration['historical_whole_component_body']['historical_FAILED_RUN_promoted'] is False and all(declaration[k] is False for k in ('original_component_APIs_executed_now', 'historical_failed_combined_RUN_promoted', 'mathematical_controls_newly_executed', 'native_transport_executed', 'production_pipeline_prepared', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('no_successful_build_seal_or_five_stage_execution_outputs', 'seal.json' not in manifest['namespaces'][2]['files'] and not (O/'seal.json').exists() and not (O/'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19/stages.json').exists())
    # End-of-review checks inspect metadata only, without rereading or replaying business.
    for key, pin in pins.items():
        check('end_review_all_verified_files_7ID_still_equal:' + key, identity(Path(key)) == pin['after7ID'])
    for namespace, witness in zip(manifest['namespaces'], namespace_witnesses):
        check('end_review_namespace_root_7ID_still_equal:' + namespace['root'], identity(Path(namespace['root'])) == witness['root7ID'])
    review.update(status='ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE', checks=checks, all_checks_typed_true=True, file_pins=pins, namespace_witnesses=namespace_witnesses, namespace_files_verified=68, frozen_D_source_files_verified=42, complete_S_source_inventory_files_verified=11, original_inputs_full_EOF_SHA7ID_verified=51, actual_root_closed_integer_exit0=True, actual_root_terminal_chunk_id='c5790b', actual_root_session_id=2985, actual_root_session_repolled_after_close=False, actual_child_PID=96184, actual_whole_seconds=host['whole_seconds'], actual_child_seconds=watch['elapsed_seconds'], actual_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'], original_caps=cap_expected, joint_H_S_O_T_D_regular_bytes=actual_joint, saved_ROOT_joint_including_E_before_summary_and_FACTORY_bytes=summary['joint_archive_bytes'], saved_pre_summary_E_regular_bytes=saved_pre_summary_E_bytes, canonical_factory_bytes=canonical_bytes, current_joint_including_later_E_metadata_bytes=actual_joint+current_E_bytes+canonical_bytes, first_readonly_audit_exit1_retained_archive_scope_assumption_correction_only=True, full_graph_storage_shape=graph_shape, graph_saved_row_counts=graph_rows, graph_saved_scalar_metadata=graph_count_metadata, full_graph_SHA=pins[str(graph_path)]['sha256'], full_trace_SHA=pins[summary['actual_complete_creation_trace']['path']]['sha256'], actual_genuine_MRO_and_POST_pinning_bound_by_fixed_independently_reviewed_host=True, observed_child_watchdog_PID_only_not_unrecorded_host_PID=True, qualification=dict(actual_complete_PREP_resource_result_verified=True, complete_five_stage_build=False, whole_combined_INPUT_admitted=False, new_native_transport=False, native_RSS=False, AAA_accuracy=False, ABA_admitted=False, physical_balance=False, goal_complete=False), remaining_requirements=['Fresh original five-stage build still required; PREP is not build or whole INPUT admission.', 'No native or scientific precision/balance qualification is obtained from this saved PREP evidence.'])
except BaseException as error:
    review.update(status='ACTUAL_PREP_EVIDENCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE', error=repr(error), blocking_findings=[repr(error)], checks=checks, file_pins=pins, namespace_witnesses=namespace_witnesses)
review['readonly_review_seconds'] = time.monotonic() - START
with (OUT/'FINAL_REVIEW.json').open('x') as f:
    json.dump(review, f, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    f.write('\n')
with (OUT/'FINAL_REPORT.txt').open('x') as f:
    f.write('原首次审查保存int1：审查器误以为joint_archive只含H/S/O/T/D。正确Root口径还含E当时200940B和规范FACTORY180593B，138488083+200940+180593=138869616；没有改保存摘要或科学/资源阈值。后续复用已完成82唯一文件完整SHA7ID证据，并检查当前7ID，只完成剩余保存metadata读数。\n')
    f.write('V19实际完整PREP保存证据有限只读复核：' + review['status'] + '\n')
    f.write('固定17992摘要、603ed namespace：H/S/O/T/D全部68 files、14 subdirectories、0 symlinks；42冻结SOURCE、11 SOURCE库存、51原pinned inputs完整EOF SHA7ID对照。实际Root c5790b整数退出0/session2985 CLOSED/no repoll；子watch PID96184、唯一stage PASS、whole199.32746954192407/child198.1557341669686、sampled peak473.09375<512。原1800/600/512/2GiB/history96GiB/free8GiB、threads/children/retries=1/1/0保持。\n')
    f.write('原真实619/705/38de/bc/ebbb源码和固定host/post-pins一致；formalT逐字保存实际子进程合并stdout/stderr与真实outer host stderr，正确标明两种范围，没有独立child stderr为空声明。完整45526587B图257ddbd和40959538B读取轨迹c1e2dae完成全hash；图只标准库解析encoded graph行数，不调用图/helper API，不授whole INPUT资格。\n')
    f.write('只实际PREP证据通过；未import project/API/helper/guard或执行业务/数值/资源检查；没有改原H/S/O/T/D/E/输入，没有清理。build五stage/完整INPUT/native RSS/AAA/ABA/物理平衡及目标完成仍false；没有把未保存的host OS PID推断成实际记录。\n')
    if review['blocking_findings']:
        f.write('具体阻碍：' + repr(review['blocking_findings']) + '\n')
raw = (OUT/'FINAL_REVIEW.json').read_bytes()
print(json.dumps(dict(status=review['status'], directory=str(OUT), review_sha256=hashlib.sha256(raw).hexdigest(), review_bytes=len(raw), finite_readonly_checks=len(checks), unique_files_full_EOF_SHA7ID=len(pins), root_terminal_integer0_closed=review.get('actual_root_closed_integer_exit0', False), sampled_peak_rss_mib=review.get('actual_sampled_peak_rss_mib'), business_executed=False, project_API_import_or_call=False, whole_INPUT_build_native_science_credit=False), indent=2))
if review['blocking_findings']:
    raise SystemExit(1)

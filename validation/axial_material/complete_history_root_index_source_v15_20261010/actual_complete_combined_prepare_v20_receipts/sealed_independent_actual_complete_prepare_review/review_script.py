"""Finite saved V20 PREP evidence review: standard-library metadata and SHA I/O only."""
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
import time

OUT = Path(__file__).parent
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E = BASE / 'actual_complete_combined_prepare_v20_receipts'
SUMMARY = E / 'Root_actual_complete_combined_prepare_summary.json'
NAMESPACE = E / 'Root_actual_complete_prepare_namespace_manifest.json'
START = time.monotonic()
checks, pins, raw_cache = {}, {}, {}
keep = {str(SUMMARY), str(NAMESPACE)}
namespace_witnesses = []

def check(label, condition):
    if type(condition) is not bool:
        raise TypeError('nonboolean check: ' + label)
    checks[label] = condition
    if condition is not True:
        raise ValueError(label)

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def finite(value):
    return type(value) in (int, float) and value == value and abs(value) < float('inf')

def file_pin(path, expected=None, wanted_sha=None):
    path = Path(path)
    key = str(path)
    check('bounded_project_read:' + key, key.startswith('/Users/wen/spot/'))
    if key not in pins:
        before = identity(path)
        check('regular_not_symlink:' + key, stat.S_ISREG(before[2]))
        digest, count = hashlib.sha256(), 0
        parts = [] if key in keep else None
        with path.open('rb') as stream:
            while True:
                block = stream.read(2**20)
                if not block:
                    break
                digest.update(block)
                count += len(block)
                if parts is not None:
                    parts.append(block)
        after = identity(path)
        check('full_EOF_stable_SHA7ID:' + key, count == before[4] and before == after)
        pins[key] = dict(path=key, sha256=digest.hexdigest(), size_bytes=count, before7ID=before, after7ID=after)
        if parts is not None:
            raw_cache[key] = b''.join(parts)
    pin = pins[key]
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
    check('metadata_cached_once:' + key, key in raw_cache)
    return json.loads(raw_cache[key])

def enumerate_namespace(root):
    files, directories, symlinks = {}, {}, {}
    root_before = identity(root)
    def walk(directory):
        with os.scandir(directory) as stream:
            entries = sorted(stream, key=lambda entry: entry.name)
        for entry in entries:
            path = Path(entry.path)
            rel = str(path.relative_to(root))
            ident = identity(path)
            if stat.S_ISREG(ident[2]):
                files[rel] = path
            elif stat.S_ISDIR(ident[2]):
                directories[rel] = ident
                walk(path)
            elif stat.S_ISLNK(ident[2]):
                symlinks[rel] = dict(target=os.readlink(path), identity=ident)
            else:
                raise ValueError('unsupported namespace node: ' + str(path))
    walk(root)
    check('namespace_root_stable:' + str(root), root_before == identity(root))
    return files, directories, symlinks, root_before

review = dict(schema='AXMAT_V20_INDEPENDENT_ACTUAL_COMPLETE_PREP_EVIDENCE_REVIEW_V1',
              scope='SAVED_ACTUAL_COMPLETE_PREP_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE',
              project_module_imported=False, project_API_or_helper_called=False,
              business_executed=False, numeric_computation_or_payload_interpretation=False,
              resource_or_guard_called=False, original_namespace_or_input_modified=False,
              source_qualification_repeated=False, whole_history_rescanned=False,
              cleanup_performed=False, blocking_findings=[])
try:
    summary = read_json(SUMMARY, wanted_sha='b1f717ce39a3ba148fa358838ffd4e0c5bbcc0e72c5cca7364dfbd2b8dff438d')
    manifest = read_json(NAMESPACE, wanted_sha='001a7f5fdf9bb6202935cae853a1106a6851ad9ada260671c3770a072b1fc1eb')
    check('summary_PREP_only_schema_status', summary['schema'] == 'ROOT_V20_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status'] == 'ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
    check('five_complete_saved_namespaces', len(manifest['namespaces']) == 5 and manifest['no_build_or_native_credit'] is True)
    H, S, O, T, D = [Path(n['root']) for n in manifest['namespaces']]
    expected_counts = (5, 11, 4, 6, 37)
    inputs = manifest['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']
    check('46_unique_original_input_pins', len(inputs) == len({x['path'] for x in inputs}) == summary['all_original_pinned_inputs_unchanged_count'] == 46)
    root_terminal = Path(summary['actual_root_terminal']['path'])
    formal_terminal = Path(summary['formal_PREP_terminal']['path'])
    graph_path = Path(summary['actual_input_graph']['path'])
    declaration_path = Path(summary['actual_declaration']['path'])
    metadata_paths = [H/'result.json', H/'COMBINED_PREPARATION/stages.json', H/'run/prepare.watchdog.json', H/'run/prepare.log', declaration_path, graph_path, root_terminal, formal_terminal, T/'Root_actual_SOURCE_inventory.json', T/'actual_external_host_stdout.json', T/'actual_child_merged_stdout_stderr.json', T/'actual_external_host_stderr.txt', T/'actual_external_Root_tool_terminal.json', S/'source_admission.json', E/'Root_prelaunch_complete_source_freeze.json', E/'Root_final_prelaunch_source_and_reserve_check.json', E/'Root_actual_prepare_metadata_writer_tool_return.json', E/'parent_stdout.log', E/'parent_stderr.log']
    keep.update(str(path) for path in metadata_paths)
    for index, namespace in enumerate(manifest['namespaces']):
        root = Path(namespace['root'])
        files, directories, symlinks, root_id = enumerate_namespace(root)
        check('namespace_full_file_count:' + str(root), len(files) == len(namespace['files']) == expected_counts[index])
        check('namespace_full_file_names:' + str(root), set(files) == set(namespace['files']))
        check('namespace_all_directories_7ID:' + str(root), directories == {entry['path']: entry['identity'] for entry in namespace['directories']})
        check('namespace_all_symlinks_exact:' + str(root), symlinks == namespace['symlinks'] == {})
        for rel, expected in namespace['files'].items():
            check('relative_absolute_path_exact:' + str(root/rel), Path(expected['path']) == root/rel)
            file_pin(root/rel, expected)
        namespace_witnesses.append(dict(root=str(root), root7ID=root_id, regular_files=len(files), directories=directories, symlinks=symlinks, full_SHA7ID_verified=True, regular_bytes=sum(pins[str(path)]['size_bytes'] for path in files.values())))
    check('63_files_15_directories_zero_symlinks', sum(x['regular_files'] for x in namespace_witnesses) == 63 and sum(len(x['directories']) for x in namespace_witnesses) == 15 and all(not x['symlinks'] for x in namespace_witnesses))
    for entry in inputs:
        file_pin(entry['path'], entry)
    for key in ('actual_root_terminal', 'Root_actual_terminal', 'formal_PREP_terminal', 'actual_host_result', 'actual_declaration', 'actual_input_graph', 'actual_complete_input_graph', 'actual_complete_creation_trace', 'namespace_manifest'):
        entry = summary[key]
        file_pin(entry['path'], entry)
    canonical = manifest['canonical_factory']
    file_pin(canonical['path'], canonical, '566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3')
    host = read_json(H/'result.json')
    declaration = read_json(declaration_path)
    formal = read_json(formal_terminal)
    terminal = read_json(root_terminal)
    watch = read_json(H/'run/prepare.watchdog.json')
    stages = read_json(H/'COMBINED_PREPARATION/stages.json')
    freeze = read_json(E/'Root_prelaunch_complete_source_freeze.json')
    prelaunch = read_json(E/'Root_final_prelaunch_source_and_reserve_check.json')
    writer_receipt = read_json(E/'Root_actual_prepare_metadata_writer_tool_return.json')
    source_admission = read_json(S/'source_admission.json')
    input_by_path = {entry['path']: entry for entry in inputs}
    host_union = host['input_sources'] + [host['original_helper'], host['resource_factory']]
    check('host_before_after_44_plus2_match_all46_closed_input_pins', len(host['input_sources']) == 44 and len(host_union) == 46 and {entry['path']: entry for entry in host_union} == input_by_path)
    for entry in host_union:
        file_pin(entry['path'], entry)
    check('37_frozen_D_files_equal_prelaunch_full_SHA7ID', freeze['all_source_files'] == manifest['namespaces'][4]['files'] and prelaunch['all_frozen_source_files_count'] == 37 and prelaunch['all_source_files_unchanged'] is True)
    for name in ('canonical_factory', 'normal_host', 'metadata_writer'):
        check('freeze_prelaunch_same_pin:' + name, freeze[name] == prelaunch[name])
        file_pin(freeze[name]['path'], freeze[name])
    check('canonical_factory_and_normal_host_fixed', freeze['canonical_factory'] == canonical and freeze['normal_host']['sha256'] == 'a9d4a1eadae7f6f346138029ea4bbd5e9a5c26c0b5efbb8d256c08b06e757de1' and freeze['metadata_writer']['sha256'] == 'af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539')
    check('prelaunch_source_only_and_genuine_MRO_binding', freeze['source_only'] is True and freeze['business_executed'] is False and prelaunch['source_only'] is True and prelaunch['business_executed'] is False and prelaunch['genuine_supervisor_and_MRO_unchanged'] is True and host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False)
    for entry in prelaunch['original_sources'] + [prelaunch['original_helper'], prelaunch['resource_factory']]:
        file_pin(entry['path'], entry)
    check('actual_root_typed_int0_closed_no_repoll', type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and terminal['closed'] is True and terminal['session_repolled_after_close'] is False and terminal['original_session_id'] == 65180 and terminal['initial_tool_return']['chunk_id'] == '81b621' and terminal['initial_tool_return']['session_id'] == 65180 and terminal['terminal_tool_return']['chunk_id'] == 'ef6952' and type(terminal['terminal_tool_return']['exit_code']) is int and terminal['terminal_tool_return']['exit_code'] == 0 and 'session_id' not in terminal['terminal_tool_return'])
    check('formal_PREP_binds_actual_closed_Root_return', type(formal['returncode']) is int and formal['returncode'] == 0 and formal['actual_tool_result'] == terminal['terminal_tool_return'] and formal['record_written_after_actual_terminal_return'] is True and formal['actual_tool_terminal_return_observed'] is True)
    check('formal_Root_terminal_copy_byteexact', raw_cache[str(T/'actual_external_Root_tool_terminal.json')] == raw_cache[str(root_terminal)])
    check('actual_metadata_writer_typed_int0_closed', type(writer_receipt['exit_code']) is int and writer_receipt['exit_code'] == 0 and writer_receipt['closed'] is True and writer_receipt['actual_tool_return']['chunk_id'] == '5851b9' and type(writer_receipt['actual_tool_return']['exit_code']) is int and writer_receipt['actual_tool_return']['exit_code'] == 0 and 'session_id' not in writer_receipt['actual_tool_return'] and writer_receipt['actual_PREP_exit_code'] == 0 and writer_receipt['new_build_executed'] is False and writer_receipt['native_executed'] is False)
    command = ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', canonical['path'], 'prepare-build']
    check('actual_canonical_command_exact', watch['command'] == host['actual_canonical_command'] == formal['command'] == command)
    check('watch_saved_in_host_exact', watch == host['watchdog'])
    check('actual_watch_typed_PID99514_return0_cleanup', type(watch['pid']) is int and watch['pid'] == 99514 and type(watch['returncode']) is int and watch['returncode'] == 0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
    check('one_actual_PREP_PASS_full_log', host['stage_records'] == stages['stages'] and len(host['stage_records']) == 1 and host['stage_records'][0]['label'] == 'run/prepare' and host['stage_records'][0]['status'] == 'PASS' and host['stage_records'][0]['command'] == command and host['stage_records'][0]['log_sha256'] == pins[str(H/'run/prepare.log')]['sha256'])
    cap_expected = dict(whole_wall_cap_seconds=1800, stage_wall_cap_seconds=600, rss_mib=512, joint_archive_cap_bytes=2*2**30, history_cap_bytes=96*2**30, free_floor_bytes=8*2**30, threads=1, children=1, retries=0)
    check('summary_original_caps_exact', all(type(summary[key]) is int and summary[key] == value for key, value in cap_expected.items()) and summary['original_caps_preserved'] is True)
    check('host_original_caps_exact', (host['whole_wall_cap_seconds'], host['stage_wall_cap_seconds'], host['rss_cap_mib'], host['archive_cap_bytes'], host['threads'], host['children_at_once'], host['retries']) == (1800, 600, 512, 2*2**30, 1, 1, 0))
    check('prelaunch_original_caps_exact', (prelaunch['whole_seconds'], prelaunch['stage_seconds'], prelaunch['rss_mib'], prelaunch['archive_cap_bytes'], prelaunch['history_cap_bytes'], prelaunch['free_floor_bytes'], prelaunch['threads'], prelaunch['children'], prelaunch['retries']) == (1800, 600, 512, 2*2**30, 96*2**30, 8*2**30, 1, 1, 0))
    check('declaration_original_five_stages_and_caps', declaration['stages'] == ['build/link', 'metadata/objects', 'metadata/executable', 'metadata/dependencies', 'audit/audit'] and (declaration['total_wall_seconds'], declaration['stage_wall_seconds'], declaration['rss_cap_mib'], declaration['archive_reserve_bytes'], declaration['artifact_budget_bytes'], declaration['min_free_bytes'], declaration['threads'], declaration['numeric_children_at_once'], declaration['retries']) == (1800, 600, 512, 2*2**30, 96*2**30, 8*2**30, 1, 1, 0))
    check('actual_elapsed_RSS_finite_and_below_caps', all(finite(value) for value in (summary['whole_seconds'], summary['child_seconds'], summary['sampled_peak_rss_mib'], watch['wall_cap_seconds'], host['stage_records'][0]['elapsed_seconds'])) and summary['whole_seconds'] == host['whole_seconds'] == 203.04176241601817 and summary['child_seconds'] == watch['elapsed_seconds'] == 201.81788908399176 and summary['sampled_peak_rss_mib'] == watch['sampled_peak_rss_mib'] == 474.578125 and 0 <= watch['sampled_peak_rss_mib'] < watch['rss_cap_mib'] == 512 and 0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= 600 and 0 <= host['stage_records'][0]['elapsed_seconds'] < 600 and 0 <= host['whole_seconds'] < 1800)
    saved_resources = [('host_before', host['resources_before']), ('host_after', host['resources_after']), ('stage_before', host['stage_records'][0]['resource_before']), ('stage_after', host['stage_records'][0]['resource_after']), ('prelaunch', prelaunch['resources_before'])]
    for label, resources in saved_resources:
        check('saved_genuine_resource_caps:' + label, resources['min_free_bytes'] == 8*2**30 and resources['artifact_budget_bytes'] == 96*2**30 and type(resources['artifact_bytes']) is int and 0 <= resources['artifact_bytes'] < 96*2**30 and type(resources['disk_free_bytes']) is int and resources['disk_free_bytes'] >= 8*2**30 and resources['resource_scope_policy'] == 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and resources['resource_scope_contract']['all_declared_extras_retained'] is True and resources['resource_scope_contract']['entire_project_artifact_cap_claimed'] is False)
    check('original_2GiB_reserve_saved_before_child', all(resources['artifact_bytes'] + 2*2**30 < 96*2**30 and resources['disk_free_bytes'] - 2*2**30 >= 8*2**30 for resources in (host['resources_before'], prelaunch['resources_before'])))
    namespace_bytes = sum(w['regular_bytes'] for w in namespace_witnesses)
    e_files, e_dirs, e_syms, e_root = enumerate_namespace(E)
    check('E_receipts_flat_regular_no_symlinks', e_dirs == {} and e_syms == {})
    cutoff = pins[str(SUMMARY)]['before7ID'][5]
    presummary = {}
    for rel, path in e_files.items():
        pin = file_pin(path)
        if rel != SUMMARY.name and pin['before7ID'][6] < cutoff:
            presummary[rel] = pin
    e_presummary_bytes = sum(pin['size_bytes'] for pin in presummary.values())
    joint_bytes = namespace_bytes + e_presummary_bytes + pins[canonical['path']]['size_bytes']
    current_joint_bytes = namespace_bytes + sum(pins[str(path)]['size_bytes'] for path in e_files.values()) + pins[canonical['path']]['size_bytes']
    check('saved_joint_H_S_O_T_D_E_before_summary_plus_FACTORY_exact', namespace_bytes == 138288697 and e_presummary_bytes == 198428 and len(presummary) == 10 and joint_bytes == summary['joint_archive_bytes'] == 138667899 and joint_bytes < 2*2**30 and 0 <= host['archive_before_result_bytes'] <= joint_bytes)
    check('current_receipt_docs_and_FACTORY_joint_below_cap', current_joint_bytes < 2*2**30)
    inventory = read_json(T/'Root_actual_SOURCE_inventory.json')
    check('formal_complete11_SOURCE_inventory_exact', inventory['files'] == {rel: entry['sha256'] for rel, entry in manifest['namespaces'][1]['files'].items()} and inventory['symlinks'] == {} and set(inventory['directories']) == {'runtime'} and summary['all_source_files_verified_count'] == 11)
    child_stdout = raw_cache[str(T/'actual_child_merged_stdout_stderr.json')]
    check('child_full_merged_stream_equals_actual_log', child_stdout == raw_cache[str(H/'run/prepare.log')] and json.loads(child_stdout) == {'declaration': str(declaration_path), 'declaration_sha256': pins[str(declaration_path)]['sha256']})
    check('full_external_host_streams_byteexact', raw_cache[str(E/'parent_stdout.log')] == raw_cache[str(T/'actual_external_host_stdout.json')] and raw_cache[str(E/'parent_stderr.log')] == raw_cache[str(T/'actual_external_host_stderr.txt')] == b'')
    check('honest_merged_stream_labels_no_separate_child_stderr_claim', formal['full_stdout_scope'] == 'ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope'] == 'ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False)
    for entry in (formal['full_stdout'], formal['full_stderr'], formal['source_inventory'], formal['actual_child_watchdog'], formal['actual_root_host_terminal_tool_return'], formal['actual_root_host_stdout'], formal['source'], formal['declaration'], formal['input_graph'], formal['original_executor_merged_capture_source'], host['actual_prepare_stdout'], host['actual_declaration'], host['actual_source_admission'], host['actual_watchdog']):
        file_pin(entry['path'], entry)
    check('formal_child_vs_outer_Root_distinct', formal['actual_root_host_launchargs'] == terminal['actual_launch_arguments'] and formal['actual_child_watchdog']['path'] == str(H/'run/prepare.watchdog.json'))
    for key in ('genuine_supervisor_source', 'genuine_parent_class_source', 'actual_local_supervisor_helper', 'actual_resource_class_factory'):
        entry = declaration[key]
        file_pin(entry['path'], entry)
    check('genuine619_705_38de_bc_ebbb_pinned_unchanged', host['original_helper']['sha256'] == '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743' and declaration['genuine_supervisor_source']['sha256'] == '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6' and declaration['genuine_parent_class_source']['sha256'] == '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128' and declaration['actual_local_supervisor_helper']['sha256'] == 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09' and host['resource_factory']['sha256'] == declaration['actual_resource_class_factory']['sha256'] == 'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')
    check('saved_genuine_constructor_scope_no_numeric_child', declaration['actual_supervisor_constructor_preflight']['actual_original_constructor_exercised'] is True and declaration['actual_supervisor_constructor_preflight']['native_or_numeric_child_launched'] is False and declaration['actual_resource_class_factory']['genuine_class_not_overlay'] is True)
    trace_path = summary['actual_complete_creation_trace']['path']
    check('full_graph_and_trace_exact_lengths_SHA', pins[str(graph_path)]['size_bytes'] == 45530035 and pins[str(graph_path)]['sha256'] == 'dfaaaff743d8edf4c94b262c5ee8104f606eddecaf39260010167f0884c6d976' and pins[trace_path]['size_bytes'] == 40969633 and pins[trace_path]['sha256'] == '0e136a5e6200cdbec9c9035156f8ed2ff95a29c953544f673865171772ba59a4')
    encoded = json.loads(raw_cache.pop(str(graph_path)))
    check('encoded_graph_metadata_schema', encoded['schema'] == 'AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1' and isinstance(encoded['graph'], dict))
    graph = encoded['graph']
    check('external_descriptor_scope_vs_internal_graph_scope_correct', declaration['input_graph']['scope'] == formal['input_graph']['scope'] == 'COMPLETE_HISTORICAL_INPUT_ONLY' and graph['scope'] == 'INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and graph['content_sha256'] == declaration['input_graph']['content_sha256'])
    codec = graph['requirements']['rows']
    check('requirement_wrapper_rows_times5_not_dict_key_count', set(codec) == {'schema', 'encoding', 'row_count', 'column_count', 'data'} and codec['schema'] == 'AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1' and codec['encoding'] == 'CANONICAL_UNSIGNED_LEB128_BASE64' and type(codec['row_count']) is int and codec['row_count'] == 238441 and type(codec['column_count']) is int and codec['column_count'] == 5 and isinstance(codec['data'], str))
    requirement_wire = base64.b64decode(codec['data'], validate=True)
    check('independent_varint_metadata_cell_count_rows_times5', len(requirement_wire) > 0 and requirement_wire[-1] < 128 and sum(byte < 128 for byte in requirement_wire) == codec['row_count'] * codec['column_count'])
    del requirement_wire
    trace_table = graph['read_trace']['records']
    graph_counts = dict(requirements=codec['row_count'], requirement_columns=codec['column_count'], canonical_files=len(graph['canonical_files']['rows']), owners=len(graph['owners']['rows']), namespaces=len(graph['namespaces']), aliases=len(graph['aliases']), read_trace_records=trace_table['row_count'], absences=len(graph['absence_inputs']), closure_categories=len(graph['closure_categories']), coverage=len(graph['coverage']))
    check('actual_saved_complete_graph_encoded_counts', graph_counts == dict(requirements=238441, requirement_columns=5, canonical_files=37111, owners=4473, namespaces=86, aliases=186, read_trace_records=63469, absences=479, closure_categories=9, coverage=9) and isinstance(graph['canonical_files']['rows'], list) and isinstance(graph['owners']['rows'], list) and type(trace_table['row_count']) is int and trace_table['row_count'] == len(trace_table['rows']))
    check('no_new_declaration_or_consumer_or_science_in_graph', graph['newly_declared_input_paths'] == {} and graph['newly_declared_input_pins'] == {} and graph['consumer_scope'] is None and graph['science_qualification_created'] is False and graph['live_resources_verified'] is False and graph['external_declaration_exit0_verified'] is False)
    graph_metadata = {key: value for key, value in graph.items() if type(value) in (int, bool, str) and len(str(value)) <= 300}
    del graph, encoded
    check('summary_all_build_INPUT_native_science_goal_flags_false', all(summary[key] is False for key in ('new_five_stage_build_executed', 'whole_combined_INPUT_admitted', 'new_native_transport_executed', 'AAA_accuracy_qualified', 'ABA_admitted', 'goal_complete', 'original_five_build_stages_executed', 'native_RSS_qualified', 'cleanup_performed')))
    check('Root_terminal_all_build_INPUT_native_science_flags_false', all(terminal[key] is False for key in ('new_five_stage_build_executed', 'whole_combined_INPUT_executed', 'new_native_transport_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('formal_all_build_math_native_science_flags_false', all(formal[key] is False for key in ('successful_new_runtime_build_observed', 'original_component_APIs_executed_now', 'native_transport_executed', 'mathematical_controls_newly_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('declaration_complete_scope_retained_no_failed_promotion', declaration['input_graph_source_root_inventory_is_exhaustive'] is True and declaration['historical_whole_component_body']['whole_seven_key_body_retained'] is True and declaration['historical_whole_component_body']['original_component_API_execution_claimed'] is False and declaration['historical_whole_component_body']['historical_FAILED_RUN_promoted'] is False and all(declaration[key] is False for key in ('original_component_APIs_executed_now', 'historical_failed_combined_RUN_promoted', 'mathematical_controls_newly_executed', 'native_transport_executed', 'production_pipeline_prepared', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted')))
    check('SOURCE_admission_scope_no_runtime_science_credit', source_admission['trim_component_API_executed_in_this_PREP'] is True and source_admission['historical_failed_combined_RUN_grants_success'] is False and source_admission['original_component_APIs_executed_now'] is False and source_admission['combined_runtime_native_RSS_not_proved'] is True and source_admission['AAA_accuracy_qualified'] is False and source_admission['ABA_admitted'] is False)
    check('no_successful_build_seal_or_five_stage_outputs', 'seal.json' not in manifest['namespaces'][2]['files'] and not (O/'seal.json').exists() and not (O/'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V20/stages.json').exists())
    for key, pin in pins.items():
        check('end_all_verified_files_7ID_unchanged:' + key, identity(Path(key)) == pin['after7ID'])
    for namespace, witness in zip(manifest['namespaces'], namespace_witnesses):
        check('end_namespace_root_7ID_unchanged:' + namespace['root'], identity(Path(namespace['root'])) == witness['root7ID'])
    review.update(status='ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE', all_checks_typed_true=True, namespace_files_verified=63, namespace_directories_verified=15, frozen_D_source_files_verified=37, complete_S_source_inventory_files_verified=11, original_inputs_full_EOF_SHA7ID_verified=46, actual_root_closed_integer_exit0=True, actual_root_terminal_chunk_id='ef6952', actual_root_session_id=65180, actual_root_session_repolled_after_close=False, actual_child_watchdog_PID=99514, actual_host_PID_unrecorded_not_inferred=True, actual_metadata_writer_chunk_id='5851b9', actual_whole_seconds=host['whole_seconds'], actual_child_seconds=watch['elapsed_seconds'], actual_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'], original_caps=cap_expected, joint_H_S_O_T_D_regular_bytes=namespace_bytes, saved_E_before_summary_regular_bytes=e_presummary_bytes, canonical_FACTORY_bytes=pins[canonical['path']]['size_bytes'], saved_complete_joint_archive_bytes=joint_bytes, current_complete_joint_archive_bytes=current_joint_bytes, saved_E_presummary_file_pins=presummary, full_graph_SHA=pins[str(graph_path)]['sha256'], full_trace_SHA=pins[trace_path]['sha256'], graph_saved_row_counts=graph_counts, graph_saved_scalar_metadata=graph_metadata, fixed_independent_SOURCE_qualification_reused_without_reaudit=True, source_scope_physical_requirements_preserved=True, qualification=dict(actual_complete_PREP_resource_result_verified=True, complete_five_stage_build=False, whole_combined_INPUT_admitted=False, new_native_transport=False, native_RSS=False, AAA_accuracy=False, ABA_admitted=False, physical_balance=False, goal_complete=False))
except BaseException as error:
    review.update(status='ACTUAL_PREP_EVIDENCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE', error=repr(error), blocking_findings=[repr(error)])

review.update(checks=checks, file_pins=pins, namespace_witnesses=namespace_witnesses, unique_files_full_EOF_SHA7ID_verified=len(pins), readonly_review_seconds=time.monotonic()-START)
(OUT/'REVIEW.json').write_text(json.dumps(review, indent=2, ensure_ascii=False)+'\n')
report = '\n'.join([review['status'], 'Finite standard-library metadata/full SHA7ID review only; no project import/API/guard/business/numeric execution.', 'No source qualification repetition, whole-history rescan, source/namespace/input modification, or cleanup.', 'Actual PREP qualification only. Five-stage build, whole INPUT, native, AAA/ABA, physical balance and goal completion remain false.', 'Checks: '+str(len(checks))+'; full-file witnesses: '+str(len(pins)), 'Blocking findings: '+repr(review['blocking_findings'])])+'\n'
(OUT/'REPORT.txt').write_text(report)
print(json.dumps(dict(status=review['status'], checks=len(checks), files=len(pins), blocking_findings=review['blocking_findings'])))
raise SystemExit(0 if not review['blocking_findings'] else 1)

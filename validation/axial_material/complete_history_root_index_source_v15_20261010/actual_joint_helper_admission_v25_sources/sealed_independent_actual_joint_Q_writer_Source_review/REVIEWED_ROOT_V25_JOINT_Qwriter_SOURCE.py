"""Root metadata-only qualification from the two actual CLOSED0 V25 families.

No project imports, candidate/helper/API execution, numerical payload replay,
old qualification credit, or scientific/build/INPUT qualification. Complete
saved namespaces and lossless Source archives are verified before new Q write.
"""
import argparse
import gzip
import hashlib
import json
import math
import os
import stat
import struct
import sys
import tarfile
from pathlib import Path

R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = R / 'validation/artifacts'
Q = B / 'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
HELPER = R / 'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
SEEDS = {
    'pure': ('actual_complete_graph_helper_controls_v25', 'axial-material-complete-graph-inactive-audit-helper-controls', '782bbb4cc04b07e54fd0e56714093d24b366457ef5127d644db4f36fd8247901', '6ddf0165b0eb2d098e7919a028e90a1902666e93eee02df000c8df2825ff77c0', 'acc8a84c7357391ea4d985be2ffe4552579f90432645e3aa653c0088168b9851', '69486274c2a93dda63dd8bea17ba5ebcf84230e1cbe8dad290087aae7930fb83', 'ca2666', '6fa312'),
    'fresh': ('actual_complete_graph_fresh_verifier_v25', 'axial-material-complete-graph-inactive-audit-fresh-verifier', 'a8f87e41083804691ab4bf21726c472db016884eabbda462841c656be7fd33f6', '2acfd8ee254a9abcad16c918ed3901cf22fd3cc81d16a4eb58743a9c80eff574', '0deb5e48c974906b7f13dc9df15015ce11328f60f487df2b112bde1df8cbc2a5', 'e41968403f9a00ea7ad68a7acb74b69233723b96d5d989c9946295fec42ea281', 'd1d77b', '514729'),
}
SNAPSHOT_FIELDS = ['schema', 'coverage', 'records', 'subprocess_records', 'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed', 'native_libc_HDF5_loader_and_directory_stat_are_not_traced']
FRESH_FIELDS = ['schema', 'classification', 'consumer_scope', 'consumer_selected_literal_and_canonical_paths', 'consumer_complete_namespace_root_sequence', 'scope', 'phase', 'graph_content_sha256', 'fresh_reader_contract', 'canonical_files_read', 'actual_bytes_read', 'byte_count_scope', 'logical_owner_requirements', 'exhaustive_namespaces_checked', 'explicit_aliases_checked', 'coverage', 'trace_coverage', 'live_io_scope', 'live_subprocesses_reexecuted', 'declared_absence_inputs_checked_before_and_after_bytes', 'absence_inputs_are_not_regular_bytes_or_science', 'caller_must_recheck_current_OS_identity_and_live_probe_results', 'typed_snapshot', 'science_qualification_created', 'live_resources_verified', 'external_declaration_exit0_verified', 'caller_must_verify_live_environment_modules_PID_time_and_resources']
FALSE_KEYS = ['fresh_production_graph_created', 'fresh_runtime_INPUT_qualified', 'new_combined_prepared', 'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted', 'whole_build_qualified', 'whole_INPUT_admitted', 'physical_balance_qualified', 'canonical_wired']
INPUTS = {}


def check(value, message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(p):
    p = Path(p); before = identity(p)
    check(stat.S_ISREG(before[2]) and not p.is_symlink(), 'ordinary regular input required: ' + str(p))
    h = hashlib.sha256()
    with p.open('rb') as f:
        while data := f.read(1024 * 1024): h.update(data)
    check(identity(p) == before, 'input changed: ' + str(p))
    return dict(path=str(p), sha256=h.hexdigest(), size_bytes=before[4], identity=before)


def verify(expected):
    actual = pin(expected['path'])
    check(actual['sha256'] == expected['sha256'] and actual['identity'] == expected.get('identity', expected.get('identity7')), 'pin mismatch: ' + actual['path'])
    if 'size_bytes' in expected: check(type(expected['size_bytes']) is int and actual['size_bytes'] == expected['size_bytes'], 'size mismatch')
    if actual['path'] in INPUTS: check(INPUTS[actual['path']] == actual, 'repeated input changed')
    INPUTS[actual['path']] = actual
    return actual


def pairs(rows):
    d = {}
    for k, v in rows:
        check(k not in d, 'duplicate JSON key: ' + k); d[k] = v
    return d


def nonfinite(value):
    raise ValueError('nonfinite JSON: ' + value)


def read(p, sha=None):
    before = pin(p)
    if sha is not None: check(before['sha256'] == sha, 'Source-bound SHA mismatch: ' + str(p))
    d = json.loads(Path(p).read_bytes(), object_pairs_hook=pairs, parse_constant=nonfinite)
    check(pin(p) == before, 'JSON read changed input'); INPUTS[before['path']] = before
    return d


def exact(a, b, ordered=True):
    if type(a) is not type(b): return False
    if type(a) is dict: return (list(a) == list(b) if ordered else set(a) == set(b)) and all(exact(a[k], b[k], ordered) for k in a)
    if type(a) is list: return len(a) == len(b) and all(exact(x, y, ordered) for x, y in zip(a, b))
    if type(a) is float: return math.isfinite(a) and math.isfinite(b) and struct.pack('>d', a) == struct.pack('>d', b)
    return a == b


def closed0(value, chunk):
    check(type(value['exit_code']) is int and value['exit_code'] == 0 and 'session_id' not in value and value['chunk_id'] == chunk, 'actual strict CLOSED0 required')


def archive(entry):
    verify(entry['compressed_archive'])
    check(entry['all_member_bytes_and_SHA_verified_after_decompression'] is True and entry['no_original_member_omission'] is True and entry['runtime_Source_entrypoints_are_separate_original_bytes'] is True, 'whole Source archive contract')
    files = entry['full_decompressed_members']; dirs = set(entry['full_decompressed_directories']); seen = set(); seen_dirs = set()
    with tarfile.open(entry['compressed_archive']['path'], 'r|gz') as tf:
        for member in tf:
            check(member.name not in seen and member.name not in seen_dirs and not member.name.startswith('/') and '..' not in Path(member.name).parts, 'archive name/duplicate')
            if member.isdir(): seen_dirs.add(member.name); continue
            check(member.isfile() and member.name in files, 'Source archive member type/name')
            expected = files[member.name]; h = hashlib.sha256(); n = 0
            f = tf.extractfile(member); check(f is not None, 'missing archive file stream')
            with f:
                while data := f.read(1024 * 1024): h.update(data); n += len(data)
            check(n == expected['size_bytes'] == member.size and h.hexdigest() == expected['sha256'], 'complete Source member bytes/SHA')
            seen.add(member.name)
    with gzip.open(entry['compressed_archive']['path'], 'rb') as f:
        while f.read(1024 * 1024): pass
    check(seen == set(files) and seen_dirs == dirs and len(files) == entry['complete_file_count_including_manifest'] and len(dirs) == entry['complete_directory_count_including_root'], 'whole archive EOF/members/directories')
    verify(entry['compressed_archive'])


def retention(p, sha):
    d = read(p, sha)
    check(d['source_only'] is True and d['new_qualification_created'] is False and d['helper_guard_business_executed'] is False, 'metadata retention only')
    for v in d['complete_original_members'].values():
        verify(v['original']); verify(v['saved'])
        check(v['original']['sha256'] == v['saved']['sha256'] and v['original']['size_bytes'] == v['saved']['size_bytes'], 'whole saved review copy')
    for key in ('original_actual_peer_seal_receipt', 'saved_actual_peer_seal_receipt'): verify(d[key])
    t = read(d['saved_actual_peer_seal_receipt']['path'])
    check(t['closed'] is True, 'actual peer seal closed')
    tr = t.get('terminal_tool_return', t.get('exec_command_result', t.get('actual_tool_return')))
    check(type(tr['exit_code']) is int and tr['exit_code'] == 0 and 'session_id' not in tr, 'actual peer seal terminal')
    return d


def owner_controls(d):
    check(d['schema'] == 'AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1', 'original owner schema')
    check([len(d[k]) for k in ('positive_controls', 'private_guard_rejections', 'accepted_str_subclass_equivalence_controls', 'partial_invalid_second_owner_rejections')] == [4, 3, 2, 2], 'whole original owner controls')
    for row in d['positive_controls']:
        check(row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default'] is True and exact(row['expected_complete_descriptor_signature'], row['actual_complete_descriptor_signature']), 'owner whole normalized signature')
        field = 'owned_list_completely_cleared_after_success' if row['case'] == 'owned_builtin_list_True' else 'caller_full_identity_type_order_value_attrs_floatbits_unchanged'
        check(row[field] is True, 'original owner clear/default boundary')
    for row in d['private_guard_rejections']:
        check(row['class'] == 'InputGraphError' and row['message'] == 'private owner consume needs a bool and an exclusively owned builtin list' and row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True, 'original owner rejects')
    for row in d['accepted_str_subclass_equivalence_controls']:
        check(row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True and row['owned_list_completely_cleared_after_success'] is True and row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default'] is True and exact(row['expected_complete_descriptor_signature'], row['actual_complete_descriptor_signature']), 'whole owner subtype control')
    for row in d['partial_invalid_second_owner_rejections']:
        check(row['class'] == 'InputGraphError' and row['message'] == 'missing file owner', 'original partial second-owner error')
    for key in ('first_valid_slot_None_after_original_validate_and_append', 'invalid_second_slot_original_identity_and_value_unchanged', 'default_partial_caller_unchanged', 'original_owner_rejection_class_order_message_preserved', 'original_protocol_controls_fixtures_and_caps_unchanged', 'no_new_fixture_file_or_IO_created'): check(d[key] is True, key)
    check(d['new_helper_qualification_created'] is False and d['business_or_science_qualification_created'] is False, 'original owner control scope')


def family(kind):
    base, artifact, summary_sha, manifest_sha, peer_sha, retained_sha, chunk, peer_chunk = SEEDS[kind]
    e = B / (base + '_receipts'); h = ART / (artifact + '-host-v25-20261010'); o = ART / (artifact + '-v25-20261010')
    summary_path = e / 'Root_actual_complete_qualification_postclose_summary.json'
    s = read(summary_path, summary_sha); ns = read(e / 'Root_actual_complete_qualification_postclose_namespace_manifest.json', manifest_sha)
    check(s['schema'] == 'ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and s['kind'] == kind and s['actual_closed'] is True and type(s['actual_exit_code']) is int and s['actual_exit_code'] == 0 and s['actual_complete_control_success'] is True and s['actual_failure'] is None and s['actual_terminal_chunk_id'] == chunk, 'genuine Root full-family success')
    check(s['whole_frozen_D_E_files_and_directories_unchanged_before_writer'] is True and s['original_normal_archive_under_cap'] is True and s['new_actual_helper_qualification'] is None, 'actual original namespace/cap scope')
    verify(s['namespace_manifest']); verify(s['actual_prelaunch']); verify(s['Root_actual_bundle']); verify(s['Source_postclose_writer'])
    t = read(s['actual_terminal_receipt']['path']); verify(s['actual_terminal_receipt']); closed0(t['terminal_tool_return'], chunk)
    check(t['schema'] == 'ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and t['closed'] is True and t['actual_tool_terminal_return_observed'] is True and t['new_actual_helper_qualification'] is None, 'actual terminal receipt')
    for name, view in ns['views'].items():
        for item in view['files']: verify(item)
        if name != 'E':
            root = Path(view['root']); actual_files = {str(p.relative_to(root)) for p in root.rglob('*') if stat.S_ISREG(p.lstat().st_mode)}
            expected_files = {str(Path(item['path']).relative_to(root)) for item in view['files']}
            check(actual_files == expected_files, 'unchanged whole H/O/D file names')
            actual_dirs = {'.'} | {str(p.relative_to(root)) for p in root.rglob('*') if stat.S_ISDIR(p.lstat().st_mode)}
            check(actual_dirs == set(view['directories']), 'unchanged whole H/O/D directories')
            for rel, ident in view['directories'].items(): check(identity(root if rel == '.' else root / rel) == ident, 'unchanged whole H/O/D directory identity')
        for item in view.get('original_fixture_symlinks', []):
            p = Path(item['path']); check(p.is_symlink() and identity(p) == item['identity'] and os.readlink(p) == item['symlink_target_text'], 'original literal alias unchanged'); verify(item['actual_resolved_target_full_EOF_pin'])
    host = read(h / 'result.json'); report = read(o / 'ACTUAL_REPORT.json'); verify(host['actual_control_report'])
    watch = host['watchdog']; check(type(watch['returncode']) is int and watch['returncode'] == 0 and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['limit_failure'] is None and watch['rss_cap_mib'] == 512, 'genuine own-child watchdog')
    whole, stage = (60, 60) if kind == 'pure' else (1800, 600)
    check(host['whole_wall_cap_seconds'] == whole and host['stage_wall_cap_seconds'] == stage and host['rss_cap_mib'] == 512 and host['archive_cap_bytes'] == 64 * 2**20 and host['threads'] == host['children_at_once'] == 1 and host['retries'] == 0 and host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False, 'all original supervisor caps/class/thread/retry')
    check(0 <= s['whole_host_seconds'] == host['whole_seconds'] < whole and 0 <= s['actual_child_seconds'] == watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= stage and 0 <= s['actual_own_child_sampled_peak_RSS_MiB'] == watch['sampled_peak_rss_mib'] < 512, 'actual resource measurements coupled')
    for resources in (host['resources_before'], host['resources_after']): check(resources['artifact_budget_bytes'] == 96 * 2**30 and resources['min_free_bytes'] == 8 * 2**30 and resources['artifact_bytes'] < resources['artifact_budget_bytes'] and resources['disk_free_bytes'] >= resources['min_free_bytes'], 'original history/free-space caps')
    for item in host['input_sources']: verify(item)
    verify(host['original_helper']); verify(host['resource_factory']); verify(host['actual_watchdog'])
    freeze = read(e / 'Root_final_complete_qualification_SOURCE_freeze.json')
    check(freeze['schema'] == 'ROOT_V25_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['kind'] == kind and freeze['source_only'] is True and freeze['new_actual_helper_qualification'] is None, 'genuine frozen complete Source')
    verify(freeze['actual_installed_helper']); check(freeze['actual_installed_helper']['sha256'] == HELPER_SHA, 'exact installed helper')
    check(len(ns['views']['D']['files']) == (9 if kind == 'pure' else 10), 'original exact full physical Source namespace')
    for entry in freeze['lossless_complete_Source_archives'].values(): archive(entry)
    check([x['complete_file_count_including_manifest'] for x in freeze['lossless_complete_Source_archives'].values()] == [184, 199], 'whole logical Source scope retained')
    for item in freeze['original_helper_Q_canonical_fullEOF_unchanged']: verify(item)
    saved = e / ('sealed_independent_actual_complete_v25_' + kind + '_saved_Source_META_review')
    peer = read(saved / 'REVIEW.json', peer_sha)
    check(peer['schema'] == 'INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_' + kind.upper() + '_SAVED_SOURCE_META_REVIEW_V1' and peer['status'] == ('PASS_SAVED_ACTUAL_PURE_CONTROLS_SOURCE_META_ONLY' if kind == 'pure' else 'PASS_SAVED_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_META_ONLY') and peer['source_only'] is True and peer['all_checks_typed_true'] is True and peer['blockers'] == [] and type(peer['check_count']) is int and peer['check_count'] == len(peer['checks']) == (55 if kind == 'pure' else 42) and all(type(c['passed']) is bool and c['passed'] is True for c in peer['checks']), 'new independent complete saved Source/META PASS')
    retained_path = e / ('Root_actual_complete_v25_' + kind + '_saved_Source_META_peer_retention_record.json'); retained = retention(retained_path, retained_sha)
    if kind == 'pure':
        tool_path = saved / 'ACTUAL_INDEPENDENT_SOURCE_META_INSPECTION_AND_REVIEW_TOOL_RETURNS.json'; tool = read(tool_path)
        actual = [x['actual_tool_return'] for x in tool['records'] if x['key'] == 'v25_actual_complete_pure_saved_Source_META_review_attempt1']; check(len(actual) == 1 and tool['own_review_terminal_closed_strict_EXIT0'] is True, 'actual pure peer review tool'); closed0(actual[0], peer_chunk)
        mapping = {'actual_Root_pure_summary_pin': summary_path, 'actual_Root_terminal_receipt_pin': Path(s['actual_terminal_receipt']['path']), 'actual_complete_HODE_namespace_manifest_pin': Path(s['namespace_manifest']['path'])}
    else:
        tool_path = saved / 'ACTUAL_SAVED_SOURCE_META_REVIEW_TOOL_RETURN.json'; tool = read(tool_path); check(tool['closed'] is True and tool['actual_tool_terminal_return_observed'] is True, 'actual fresh peer review tool'); closed0(tool['terminal_tool_return'], peer_chunk)
        mapping = {'actual_Root_fresh_summary_pin': summary_path, 'actual_Root_fresh_terminal_pin': Path(s['actual_terminal_receipt']['path']), 'actual_complete_namespace_manifest_pin': Path(s['namespace_manifest']['path'])}
    for key, path in mapping.items(): check(verify(peer[key]) == pin(path), 'peer actual result coupling')
    check(peer['new_actual_helper_qualification'] is None, 'peer no new Q authority')
    evidence = dict(actual_root_terminal=pin(s['actual_terminal_receipt']['path']), actual_controls_summary=pin(summary_path), actual_host_result=pin(h / 'result.json'), actual_control_report=pin(o / 'ACTUAL_REPORT.json'), complete_namespace_manifest=pin(s['namespace_manifest']['path']), independent_actual_review=pin(saved / 'REVIEW.json'), independent_actual_review_tool_return=pin(tool_path), source_manifest=pin(e / 'Root_final_complete_qualification_SOURCE_freeze.json'), independent_review_retention_record=pin(retained_path), independent_review_actual_seal=verify(retained['saved_actual_peer_seal_receipt']), actual_measurement=dict(whole_seconds=s['whole_host_seconds'], child_seconds=s['actual_child_seconds'], sampled_peak_rss_mib=s['actual_own_child_sampled_peak_RSS_MiB'], actual_original_archive_bytes=s['normal_HOD_bytes'] if kind == 'pure' else s['complete_HODE_bytes'], original_archive_scope=s['normal_host_archive_scope'], original_caps=dict(whole_seconds=whole, stage_seconds=stage, rss_mib=512, archive_bytes=64 * 2**20, history_bytes=96 * 2**30, free_bytes=8 * 2**30, threads=1, children=1, retries=0)))
    return report, peer, evidence


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--source-sha256', required=True); args = parser.parse_args()
    check(sys.flags.optimize == 0 and not bool(os.environ.get('PYTHONOPTIMIZE')), 'nonoptimized Root Source writer required')
    source = pin(__file__); check(source['sha256'] == args.source_sha256, 'exact reviewed writer Source required'); INPUTS[source['path']] = source
    check(not Q.exists(), 'fresh Q only')
    install_path = B / 'actual_complete_graph_helper_controls_v23_receipts/Root_actual_complete_helper_SOURCE_install_record.json'
    install_tool_path = install_path.with_name('Root_actual_complete_helper_SOURCE_install_tool_return.json')
    install = read(install_path, '079d4dfec16d0df86459abc2fc9238f7aabade38fca8c7adc0659a50f37dc5cf'); install_tool = read(install_tool_path, 'a305a84b712276aecadd5ebc7fced99d0d58b68a061e228747f0ccfbeed63c12')
    closed0(install_tool['terminal_tool_return'], '10a0e4'); check(install_tool['source_only'] is True and install_tool['closed'] is True and install['source_only'] is True and install_tool['new_Q'] is None, 'actual Source-only installation')
    helper = verify(install['installed_helper']); check(helper == verify(install_tool['installed_helper']) and helper['path'] == str(HELPER) and helper['sha256'] == HELPER_SHA and helper['size_bytes'] == 150986, 'same actual installed helper Source')
    pure, pp, pe = family('pure'); fresh, fp, fe = family('fresh')
    check(verify(pure['helper']) == helper and verify(fresh['actual_success_pins']['helper']) == helper, 'both actual complete families use this exact helper')
    fixture = read(ART / 'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_fixture_controls.json'); small = read(ART / 'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_codec_and_rejection_controls.json')
    check(pure['status'] == 'ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' and fixture['producer_full_exact_values_types_order_floatbits'] is True and fixture['caller_full_value_and_mutable_identity_preserved'] is True and len(fixture['rejections']) == 37 and len(fixture['complete_rejected_arguments']) == 18, 'original complete fixture producer/rejects')
    check([s['stage'] for s in pure['stages']] == ['real_small_fixture_producer_equivalence_and_rejections', 'all_new_codecs_and_both_strict_entrances_small_controls', 'full_63379_creation_trace_roundtrip_and_stored_size', 'full_old_saved_graph_codec_and_two_normal_strict_entrances', 'all_original_saved_metadata_bytes_identity_unchanged'], 'five original full stages')
    check(small['all_default_inputs_unmodified'] is True and small['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True and small['ordinary_and_both_storage_strict_dispatches'] is True and len(small['rejections']) == pure['small_codecs']['rejections'] == 61, 'whole codec/type/order/floatbit/reject scope')
    subtypes = pure['small_fixture']['accepted_str_subclass_equivalence_controls']; check(len(subtypes) == 2 and all(x['complete_builtin_output_values_types_order_floatbits_equal'] is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True for x in subtypes), 'original subtype attrs/identity')
    old = pure['full_old_saved_graph']; meta = old['complete_original_metadata']; trace = pure['full_new_creation_trace']
    check(exact(meta, old['normal_strict_file_entrance_full_semantics_and_counts']) and exact(meta, old['normal_strict_payload_entrance_full_semantics_and_counts']) and old['full_default_roundtrip_exact'] is True and old['old_read_trace_not_replaced_by_new_trace'] is True and old['original_legacy_semantic_sha_preserved'] is True, 'whole old graph two normal strict entrances')
    counts = meta['complete_counts']; check(counts['canonical_files'] == 36776 and counts['requirements'] == 237767 and counts['read_trace_records'] == 62332, 'whole original graph counts')
    check(trace['exact_full_roundtrip'] is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse'] is True and trace['default_source_nonmutation'] is True and trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886, 'whole new trace default/order/roundtrip')
    owner_controls(pure['private_owner_consume_controls'])
    snapshot = read(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact']['path']); verify(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact'])
    check(exact(snapshot, pure['private_inactive_audit_snapshot_controls'], ordered=False), 'full ordered artifact and original report same values/types/floatbits')
    check(snapshot['schema'] == 'PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1' and snapshot['status'] == 'ACTUAL_PRIVATE_SNAPSHOT_CONTROLS_RETURNED_METADATA_ONLY' and [len(snapshot[k]) for k in ('positive_controls', 'private_guard_rejections', 'last_use_failure_controls')] == [5, 13, 3], 'complete new snapshot scope')
    for index, row in enumerate(snapshot['positive_controls']):
        check(row['default_and_explicitFalse_complete_state_unchanged'] is True and row['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default'] is True, 'default unchanged and all nine fields')
        if index < 3:
            check(row['owned_same_builtin_records_map_completely_cleared'] is True and row['all_other_audit_state_and_actual_Popen_references_unchanged'] is True and list(row['actual_full_expected_snapshot']) == SNAPSHOT_FIELDS and exact(row['actual_full_expected_snapshot'], row['actual_full_consumed_snapshot']), 'owned full ordered nine fields/Popen/clear')
        else: check(row['private_True_not_permitted_for_subclass'] is True, 'default subtype compatibility retained')
    check(all(r['rejected'] is True and r['class_name'] == 'InputGraphError' and r['complete_audit_state_identity_type_order_value_bits_unchanged'] is True for r in snapshot['private_guard_rejections']), 'all 13 private guards')
    check([r['case'] for r in snapshot['last_use_failure_controls']] == ['invalid_second_row_before_clear', 'missing_attempt_count_before_clear', 'nonfinite_clone_after_clear'], 'original last-use failure order')
    for i, row in enumerate(snapshot['last_use_failure_controls']): check(row['original_error_class_and_message_retained'] is True and row['no_transactional_private_mode_promise'] is True and row['both_callers_unchanged_before_clear_or_default'] is (i < 2) and row['private_clone_failure_after_clear_consumption_observed'] is (i == 2), 'honest before/after-clear failure boundary')
    check(snapshot['actual_child_returncode'] == 0 and snapshot['actual_same_observation_full_record_role_comparison'] is True and snapshot['no_cross_process_PID_FD_inode_normalization'] is True and snapshot['default_original_complete_protocol_preserved'] is True and snapshot['native_or_numeric_component_executed'] is False and snapshot['helper_qualification_created'] is False and snapshot['business_or_science_qualification_created'] is False, 'same genuine Popen and metadata-only control')
    check(fresh['complete_return_fields_retained'] == FRESH_FIELDS and fresh['actual_complete_trace_counts'] == dict(records=37112, attempts=37112, canonical_files=37111, external_graph_reads=1, no_subprocess_reexecuted=True) and fresh['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is True, 'complete fresh 27-field return/current read counts')
    pc = fresh['private_trace_controls']; check(len(pc['positive_controls']) == 4 and len(pc['rejections']) == 3 and all(r['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True for r in pc['positive_controls']) and all(r['rejected'] is True and r['class_name'] == 'InputGraphError' and r['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for r in pc['rejections']), 'original complete fresh four/three controls')
    fc = fresh['private_full_inactive_audit_snapshot_controls']
    for k in ('default_snapshot_full_original_records_unchanged', 'owned_same_builtin_records_map_completely_cleared', 'all_other_audit_state_unchanged', 'all_nine_fields_full_type_order_value_floatbits_and_counts_equal', 'no_second_graph_or_input_phase_substituted', 'all37112_actual_reads_from_same_genuine_phase', 'no_cross_phase_hash_or_stat_cache'): check(fc[k] is True, 'fresh full snapshot ' + k)
    check(exact(fc['default_complete_descriptor_type_order_floatbit_pin'], fc['consumed_complete_descriptor_type_order_floatbit_pin']) and fc['default_complete_descriptor_type_order_floatbit_pin']['complete_node_count'] == 779371 and fc['complete_consumed_vs_default_wire']['complete_nine_snapshot_fields'] == SNAPSHOT_FIELDS and fc['complete_consumed_vs_default_wire']['uncompressed_JSON_bytes'] == 21411449 and fc['complete_consumed_vs_default_wire']['every_default_and_consumed_wire_byte_compared'] is True and fc['complete_consumed_vs_default_wire']['full_gzip_EOF_verified'] is True, 'every full same-phase nine-field wire byte compared')
    gzips = {k: verify(fresh[k]) for k in ('expected_complete_return_contract', 'actual_complete_verifier_return', 'actual_complete_ReadOpenAudit_trace')}
    for k in gzips: check(fresh[k]['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and fresh[k]['no_fields_or_records_filtered'] is True, 'all original full gzip evidence retained')
    check(fresh['expected_complete_return_contract']['sha256'] == fresh['actual_complete_verifier_return']['sha256'] and fresh['expected_complete_return_contract']['uncompressed_JSON_sha256'] == fresh['actual_complete_verifier_return']['uncompressed_JSON_sha256'], 'complete expected/current return bytes equal')
    full_protocol = dict(original_and_fresh_small_producer_values_types_order_floatbits_exact=True, all_caller_mutable_identity_and_subtype_attributes_unchanged=True, accepted_str_subtype_groups=len(subtypes), small_codec_rejections=pure['small_codecs']['rejections'], complete_original_graph_counts=counts, complete_old_graph_two_normal_strict_entrances_exact=True, complete_old_legacy_semantic_sha256=meta['legacy_semantic_sha256'], complete_old_wire_content_sha256=meta['wire_content_sha256'], complete_new_creation_trace_records=trace['full_record_count'], complete_new_creation_trace_actual_attempts=trace['actual_attempt_count'], new_creation_trace_not_substituted_into_old_graph=True, full_json_types_order_floatbits_and_values_retained=True, default_source_nonmutation=True)
    fe.update(all27_return_fields=fresh['complete_return_fields_retained'], full_saved_graph_metadata=fresh['independent_full_saved_graph_metadata'], private_trace_controls=pc, private_full_inactive_audit_snapshot_controls=fc, complete_gzip_pins={k: fresh[k] for k in gzips}, complete_actual_read_counts=fresh['actual_complete_trace_counts'])
    q = dict(schema='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25', status='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25', helper=helper, **{k:v for k,v in pe.items() if k != 'actual_measurement'}, actual_measurement=pe['actual_measurement'], actual_SOURCE_install_record=pin(install_path), actual_SOURCE_install_tool_return=pin(install_tool_path), full_protocol=full_protocol, private_owner_consume_controls=pure['private_owner_consume_controls'], private_inactive_audit_snapshot_controls=snapshot, private_inactive_audit_snapshot_controls_order_preserved_artifact=verify(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact']), complete_current_graph_fresh_verifier=fe, full_protocol_additional_complete_fixture_artifact=pin(ART / 'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_fixture_controls.json'), full_protocol_additional_complete_codec_artifact=pin(ART / 'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_codec_and_rejection_controls.json'), Root_actual_Source_writer=source, independent_saved_review_counts=dict(pure=55, fresh=42, auxiliary_pure_small_controls=136), lossless_complete_original_Source_files_per_family=[184,199], pure_source_member_count=9, fresh_source_member_count=10, supervisor_class_or_MRO_modified=False, profile_used=False, scope='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE', original_protocol_preserved_and_new_owner_controls_independently_saved_reviewed=True, original_protocol_and_new_snapshot_controls_and_full_current_graph_independently_saved_reviewed=True, **{k:False for k in FALSE_KEYS})
    q['original_caps'] = pe['actual_measurement']['original_caps']
    check(len(full_protocol) == 13, 'original full protocol field scope')
    for item in tuple(INPUTS.values()): check(pin(item['path']) == item, 'whole qualification input changed before new Q')
    q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs'] = list(INPUTS.values())
    q['Root_finite_joint_META_only_no_project_API_or_numeric'] = True
    with Q.open('x') as f:
        json.dump(q, f, ensure_ascii=False, indent=2, allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(dict(actual_metadata_Q=pin(Q), actual_Source_writer=source, full_protocol_fields=13, complete_return_fields=27, actual_complete_read_count=37112, pure_saved_review_checks=55, fresh_saved_review_checks=42, whole_build_qualified=False, whole_INPUT_admitted=False, AAA_accuracy_qualified=False, ABA_admitted=False, candidate_or_API_or_numeric_executed=False)))


if __name__ == '__main__': main()

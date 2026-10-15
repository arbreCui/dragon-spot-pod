import hashlib
import json
import stat
from pathlib import Path

R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
P = B / 'actual_complete_graph_helper_controls_v21_receipts'
E = B / 'actual_complete_graph_fresh_verifier_v21b_receipts'
PP = P / 'sealed_independent_actual_original_pure_protocol_review'
FP = E / 'sealed_independent_actual_complete_fresh_verifier_META_review'
PH = R / 'validation/artifacts/axial-material-complete-graph-private-verifier-helper-controls-host-v21-20261010'
PO = R / 'validation/artifacts/axial-material-complete-graph-private-verifier-helper-controls-v21-20261010'
FH = R / 'validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21b-20261010'
FO = R / 'validation/artifacts/axial-material-complete-graph-fresh-verifier-v21b-20261010'
D = B / 'actual_complete_graph_fresh_verifier_v21b_sources'
Q = B / 'Root_actual_complete_graph_private_verifier_helper_admission_v21.json'
inputs = {}

def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(p):
    p = Path(p)
    before = identity(p)
    assert stat.S_ISREG(before[2]) and not p.is_symlink(), str(p)
    digest = hashlib.sha256()
    with p.open('rb') as f:
        while chunk := f.read(1024 * 1024):
            digest.update(chunk)
    assert identity(p) == before, str(p)
    return {'path': str(p), 'sha256': digest.hexdigest(), 'size_bytes': before[4], 'identity': before}

def verify(expected):
    actual = pin(expected['path'])
    assert actual['sha256'] == expected['sha256'], actual['path']
    assert actual['identity'] == expected.get('identity', expected.get('identity7')), actual['path']
    if 'size_bytes' in expected:
        assert type(expected['size_bytes']) is int and actual['size_bytes'] == expected['size_bytes']
    if actual['path'] in inputs:
        assert inputs[actual['path']] == actual
    inputs[actual['path']] = actual
    return actual

def pairs(items):
    d = {}
    for k, v in items:
        assert k not in d, k
        d[k] = v
    return d

def nonfinite(value):
    raise ValueError(value)

def read(p, sha=None):
    item = pin(p)
    if sha is not None:
        assert item['sha256'] == sha, str(p)
    inputs[item['path']] = item
    data = json.loads(Path(p).read_bytes(), object_pairs_hook=pairs, parse_constant=nonfinite)
    assert pin(p) == item
    return data

def terminal(p, initial_chunk, session, terminal_chunk):
    d = read(p)
    a = d['initial_tool_return']
    t = d['terminal_tool_return']
    assert a['chunk_id'] == initial_chunk and type(a['session_id']) is int and a['session_id'] == session
    assert t['chunk_id'] == terminal_chunk and type(t['exit_code']) is int and t['exit_code'] == 0
    assert 'session_id' not in t and d['closed'] is True
    if 'no_closed_session_repoll' in d:
        assert d['no_closed_session_repoll'] is True
    else:
        assert d['session_repolled_after_close'] is False
    return d

assert not Q.exists()
pure = read(P / 'Root_actual_pure_protocol_summary.json', 'e01e594a2f211faddee3daa4aea7ea141e323c0ce973d161bede48e3489ff1b9')
fresh = read(E / 'Root_actual_v21b_full_fresh_verifier_summary.json', '0b6d8a5038e81d0e0cc74c30fafdbb7377d19afa108b4daa471b10c21feda733')
pure_peer = read(PP / 'REVIEW.json', '70d454ce4c2ec377f28bfca67de46313fe29987cfc456c36190824973dec7908')
fresh_peer = read(FP / 'REVIEW.json', 'ae7d9d8f1373cfd57ceea6803db86b0a194f613d778a023d86eee0e884b8b231')
assert pure_peer['blockers'] == []
assert pure_peer['status'] == 'ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER'
assert fresh_peer['status'] == 'SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED'
assert pure_peer['all_explicit_input_SHA7ID_before_after_exact'] is True
assert fresh_peer['all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal'] is True
for entry in pure_peer['pins'] + fresh_peer['input_pins']:
    verify(entry)
pure_term_path = P / 'Root_actual_pure_protocol_tool_terminal_return.json'
fresh_term_path = E / 'Root_actual_v21b_fresh_verifier_tool_terminal_return.json'
terminal(pure_term_path, 'ea406f', 49247, '5e1034')
terminal(fresh_term_path, '45eca8', 38770, '59fbf2')
pure_tools = read(PP / 'actual_META_review_tool_return.json')
pure_review_return = pure_tools['actual_review_tool_result']
assert pure_review_return['chunk_id'] == '2eb342'
assert type(pure_review_return['exit_code']) is int and pure_review_return['exit_code'] == 0
assert 'session_id' not in pure_review_return
fresh_tools = read(FP / 'actual_META_tool_returns.json')
fresh_review_return = fresh_tools['actual_review_terminal_return']
assert fresh_review_return['chunk_id'] == '45cf76'
assert type(fresh_review_return['exit_code']) is int and fresh_review_return['exit_code'] == 0
assert 'session_id' not in fresh_review_return and fresh_tools['actual_review_closed'] is True
helper_pin = verify(pure['installed_helper'])
assert helper_pin['sha256'] == 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
assert helper_pin['size_bytes'] == 147870
pure_report = read(PO / 'ACTUAL_REPORT.json', '0beb228acd998a8693ff21244a8ed188c57389753222165f2d827ffd16f4d64d')
small = read(PO / 'small_codec_and_rejection_controls.json')
fixture = read(PO / 'small_fixture_controls.json')
fresh_report = read(FO / 'ACTUAL_REPORT.json')
assert pure_report['status'] == 'ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'
assert fixture['producer_full_exact_values_types_order_floatbits'] is True
assert [s['stage'] for s in pure_report['stages']] == [
    'real_small_fixture_producer_equivalence_and_rejections',
    'all_new_codecs_and_both_strict_entrances_small_controls',
    'full_63379_creation_trace_roundtrip_and_stored_size',
    'full_old_saved_graph_codec_and_two_normal_strict_entrances',
    'all_original_saved_metadata_bytes_identity_unchanged',
]
assert fresh_report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is True
assert fresh_peer['all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal'] is True
assert fresh_peer['complete_expected_actual_JSON_wire_bytes_equal'] is True
assert fresh_peer['one_genuine_stage_PASS'] is True and fresh_peer['liveness_group_cleanup'] is True
assert fresh_peer['limit_failure'] is None and fresh_peer['retries'] == 0
assert len(fresh_report['complete_return_fields_retained']) == 27
assert fresh_report['actual_complete_trace_counts'] == {'records': 37112, 'attempts': 37112, 'canonical_files': 37111, 'external_graph_reads': 1, 'no_subprocess_reexecuted': True}
assert fresh_peer['private_positive_controls'] == 4 and fresh_peer['private_rejections'] == 3
old = pure_report['full_old_saved_graph']
meta = old['complete_original_metadata']
assert meta == old['normal_strict_file_entrance_full_semantics_and_counts'] == old['normal_strict_payload_entrance_full_semantics_and_counts']
assert old['full_default_roundtrip_exact'] is True and old['old_read_trace_not_replaced_by_new_trace'] is True
assert old['original_legacy_semantic_sha_preserved'] is True
counts = meta['complete_counts']
assert counts['canonical_files'] == 36776 and counts['requirements'] == 237767 and counts['read_trace_records'] == 62332
assert pure_peer['full_report_original_metadata_and_both_strict_entrances_equal'] is True
assert pure_peer['full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified'] is True
subtypes = pure_report['small_fixture']['accepted_str_subclass_equivalence_controls']
assert len(subtypes) == 2
assert all(x['complete_builtin_output_values_types_order_floatbits_equal'] is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True for x in subtypes)
assert pure_report['small_fixture']['caller_full_value_and_mutable_identity_preserved'] is True
assert small['all_default_inputs_unmodified'] is True and small['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True
assert small['ordinary_and_both_storage_strict_dispatches'] is True and len(small['rejections']) == pure_report['small_codecs']['rejections'] == 61
trace = pure_report['full_new_creation_trace']
assert trace['exact_full_roundtrip'] is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse'] is True and trace['default_source_nonmutation'] is True
assert trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886
assert pure['actual_original_pure_protocol_pass'] is True and pure['closed'] is True
assert pure['whole_seconds_cap'] == pure['stage_seconds_cap'] == 60 and pure['rss_mib_cap'] == 512
assert pure['whole_seconds'] < 60 and pure['child_seconds'] < 60 and pure['sampled_peak_rss_mib'] < 512
assert pure['joint_source_host_out_bytes'] < pure['archive_bytes_cap'] == 64 * 2**20
assert fresh['whole_seconds_cap'] == 1800 and fresh['stage_seconds_cap'] == 600 and fresh['rss_mib_cap'] == 512
assert fresh['whole_seconds'] < 1800 and fresh['child_seconds'] < 600 and fresh['sampled_peak_rss_mib'] < 512
assert fresh_peer['driver_reported_own_peak_rss_mib'] < 512
for doc in [pure, fresh]:
    assert doc['threads'] == doc['children'] == 1 and doc['retries'] == 0
    assert doc['history_bytes_cap'] == 96 * 2**30
    assert doc.get('free_bytes_floor', doc.get('min_free_bytes')) == 8 * 2**30
full_gzips = {k: verify(fresh_report[k]) for k in ['expected_complete_return_contract', 'actual_complete_verifier_return', 'actual_complete_ReadOpenAudit_trace']}
current_joint_bytes = 0
for root in [D, E, FH, FO]:
    for p in root.rglob('*'):
        s = p.lstat()
        assert not stat.S_ISLNK(s.st_mode), str(p)
        if stat.S_ISREG(s.st_mode):
            current_joint_bytes += s.st_size
        else:
            assert stat.S_ISDIR(s.st_mode), str(p)
assert current_joint_bytes < 64 * 2**20
original_caps = {'whole_seconds': 60, 'stage_seconds': 60, 'rss_mib': 512, 'archive_bytes': 64 * 2**20, 'history_bytes': 96 * 2**30, 'free_bytes': 8 * 2**30, 'threads': 1, 'children': 1, 'retries': 0}
full_protocol = {
    'original_and_fresh_small_producer_values_types_order_floatbits_exact': True,
    'all_caller_mutable_identity_and_subtype_attributes_unchanged': True,
    'accepted_str_subtype_groups': len(subtypes),
    'small_codec_rejections': pure_report['small_codecs']['rejections'],
    'complete_original_graph_counts': counts,
    'complete_old_graph_two_normal_strict_entrances_exact': True,
    'complete_old_legacy_semantic_sha256': meta['legacy_semantic_sha256'],
    'complete_old_wire_content_sha256': meta['wire_content_sha256'],
    'complete_new_creation_trace_records': trace['full_record_count'],
    'complete_new_creation_trace_actual_attempts': trace['actual_attempt_count'],
    'new_creation_trace_not_substituted_into_old_graph': True,
    'full_json_types_order_floatbits_and_values_retained': True,
    'default_source_nonmutation': True,
}
admission = {
    'schema': 'AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21',
    'status': 'QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21',
    'helper': helper_pin,
    'actual_root_terminal': pin(pure_term_path),
    'actual_controls_summary': pin(P / 'Root_actual_pure_protocol_summary.json'),
    'actual_host_result': pin(PH / 'result.json'),
    'actual_control_report': pin(PO / 'ACTUAL_REPORT.json'),
    'complete_namespace_manifest': pin(P / 'Root_actual_pure_protocol_namespace_manifest.json'),
    'independent_actual_review': pin(PP / 'REVIEW.json'),
    'independent_actual_review_tool_return': pin(PP / 'actual_META_review_tool_return.json'),
    'source_manifest': pin(P / 'Root_full_pure_protocol_SOURCE_namespace_freeze.json'),
    'full_protocol': full_protocol,
    'full_protocol_additional_complete_fixture_artifact': pin(PO / 'small_fixture_controls.json'),
    'full_protocol_additional_complete_codec_artifact': pin(PO / 'small_codec_and_rejection_controls.json'),
    'actual_measurement': {
        'whole_seconds': pure['whole_seconds'], 'child_seconds': pure['child_seconds'],
        'sampled_peak_rss_mib': pure['sampled_peak_rss_mib'],
        'actual_final_host_out_source_bytes': pure['joint_source_host_out_bytes'],
        'old_complete_graph_stored_bytes': old['stored_wholegraph']['size_bytes'],
        'new_complete_trace_original_compact_bytes': trace['original_insertion_order_compact_source']['size_bytes'],
        'new_complete_trace_stored_bytes': trace['encoded_artifact']['size_bytes'],
    },
    'original_caps': original_caps,
    'complete_current_graph_fresh_verifier': {
        'actual_root_terminal': pin(fresh_term_path),
        'actual_controls_summary': pin(E / 'Root_actual_v21b_full_fresh_verifier_summary.json'),
        'actual_host_result': pin(FH / 'result.json'),
        'actual_control_report': pin(FO / 'ACTUAL_REPORT.json'),
        'complete_namespace_manifest': pin(E / 'Root_actual_v21b_full_fresh_verifier_finite_saved_manifest.json'),
        'independent_actual_review': pin(FP / 'REVIEW.json'),
        'independent_actual_review_tool_return': pin(FP / 'actual_META_tool_returns.json'),
        'sealed_independent_actual_review_manifest': pin(FP / 'sealed_manifest.json'),
        'source_manifest': pin(E / 'Root_generated_full_SOURCE_namespace_freeze.json'),
        'source_binding_record': pin(E / 'Root_generated_SOURCE_binding_only.json'),
        'complete_gzips': full_gzips,
        'original_caps': {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_HOST_OUT_SOURCE_E_archive_bytes': 64 * 2**20, 'history_bytes': 96 * 2**30, 'free_bytes': 8 * 2**30, 'threads': 1, 'children': 1, 'retries': 0},
        'actual_measurement': {'whole_seconds': fresh['whole_seconds'], 'child_seconds': fresh['child_seconds'], 'sampled_peak_rss_mib': fresh['sampled_peak_rss_mib'], 'driver_reported_own_peak_rss_mib': fresh_peer['driver_reported_own_peak_rss_mib'], 'sample_and_self_peaks_are_distinct': True, 'joint_snapshot_plus_manifest_bytes_at_original_closeout': fresh_peer['joint_archive_snapshot_plus_manifest_bytes'], 'current_joint_regular_bytes_after_saved_peer_and_copy_receipts': current_joint_bytes},
        'full_public_return_field_order': fresh_report['complete_return_fields_retained'],
        'full_current_graph_metadata': fresh_report['independent_full_saved_graph_metadata'],
        'all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal': True,
        'complete_actual_unfiltered_read_trace_counts': fresh_report['actual_complete_trace_counts'],
        'private_positive_controls': 4, 'private_reject_controls': 3,
        'SOURCE33_and_all_fixed_inputs_before_after_unchanged': True,
        'actual_external_Root_exit0_closed_and_saved_peer_pass': True,
        'scope': 'Complete current graph metadata verifier only; no business production INPUT/native/numeric/science qualification.',
    },
    'supervisor_class_or_MRO_modified': False, 'profile_used': False,
    'fresh_production_graph_created': False, 'fresh_runtime_INPUT_qualified': False,
    'new_combined_prepared': False, 'native_RSS_verified': False,
    'AAA_accuracy_qualified': False, 'ABA_admitted': False,
    'whole_build_qualified': False, 'whole_INPUT_admitted': False,
    'physical_balance_qualified': False,
    'scope': 'Root jointly admits the new helper metadata protocol from two distinct actual closed exit-zero trials and their saved independent reviews. The original 60-second producer/codec protocol and complete-current-graph verifier have separate caps and actual terminals. No production build, whole INPUT, native transport, independent physical reference, AAA accuracy or ABA is qualified.',
    'Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count': len(inputs),
    'Root_finite_joint_META_only_no_project_API_or_numeric': True,
}
for item in inputs.values():
    assert pin(item['path']) == item, item['path']
with Q.open('x') as f:
    json.dump(admission, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({'status': admission['status'], 'qualification': pin(Q), 'unique_fresh_explicit_inputs': len(inputs), 'pure_Root_terminal': '5e1034', 'fresh_Root_terminal': '59fbf2', 'whole_build_INPUT_native_AAA_ABA_physics_qualified': False}, ensure_ascii=False))

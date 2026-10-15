"""UNREADY V22 complete Root helper joint-admission META writer template.

Only the new actual V22 pure/fresh summaries and terminals are Source-bound.
Saved-review pins/field shapes remain unknown. No execution at import, no oldQ
qualification credit, no helper/guard/API/numeric code. Root must review and bind
actual saved reviews before this writer can create a fresh metadata-only Q.
"""
import math
import os
import sys
WRITER_SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22'
ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED = None
PURE_PEER_PATH = None
PURE_PEER_SHA256 = None
FRESH_PEER_PATH = None
FRESH_PEER_SHA256 = None
PURE_PEER_TOOL_PATH = None
PURE_PEER_TOOL_SHA256 = None
FRESH_PEER_TOOL_PATH = None
FRESH_PEER_TOOL_SHA256 = None
FRESH_SOURCE_BINDING_RECORD_PATH = None
FRESH_SOURCE_BINDING_RECORD_SHA256 = None
FRESH_PEER_SEAL_PATH = None
FRESH_PEER_SEAL_SHA256 = None
FRESH_SOURCE_BINDING_RECORD_IDENTITY7 = None
REQUIRED_FUTURE_BINDING_FIELDS = ('PURE_PEER_PATH', 'PURE_PEER_SHA256', 'FRESH_PEER_PATH', 'FRESH_PEER_SHA256', 'PURE_PEER_TOOL_PATH', 'PURE_PEER_TOOL_SHA256', 'FRESH_PEER_TOOL_PATH', 'FRESH_PEER_TOOL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_PATH', 'FRESH_SOURCE_BINDING_RECORD_SHA256', 'FRESH_PEER_SEAL_PATH', 'FRESH_PEER_SEAL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_IDENTITY7')

import hashlib
import json
import stat
from pathlib import Path

R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
P = B / 'actual_complete_graph_helper_controls_v22_receipts'
E = B / 'actual_complete_graph_fresh_verifier_v22_receipts'
PP = None  # actual future saved-review directory must be supplied; no old peer credit
FP = None  # actual future saved-review directory must be supplied; no old peer credit
PH = R / 'validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-host-v22-20261010'
PO = R / 'validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010'
FH = R / 'validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v22-20261010'
FO = R / 'validation/artifacts/axial-material-complete-graph-fresh-verifier-v22-20261010'
D = B / 'actual_complete_graph_fresh_verifier_v22_sources'
Q = B / 'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
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


def validate_terminal_v22(value, schema):
    assert value['schema'] == schema and value['closed'] is True
    assert value['actual_tool_terminal_return_observed'] is True
    assert value['session_repolled_after_close'] is False
    tr = value['terminal_tool_return']
    assert type(tr['exit_code']) is int and tr['exit_code'] == 0 and 'session_id' not in tr
    assert type(tr['wall_time_seconds']) in (int, float) and not isinstance(tr['wall_time_seconds'], bool)
    assert math.isfinite(tr['wall_time_seconds']) and tr['wall_time_seconds'] >= 0
    assert type(tr['output']) is str
    assert value['actual_new_helper_qualification_sha256'] is None

def validate_summary_v22(value, kind):
    assert value['schema'] == 'ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1'
    assert value['status'] == 'ACTUAL_EXIT0_CLOSED_COMPLETE_' + kind + '_CONTROLS_SAVED_REVIEW_REQUIRED'
    assert type(value['actual_Root_exit_code']) is int and value['actual_Root_exit_code'] == 0 and value['closed'] is True
    assert value['independent_saved_actual_review_pass'] is False
    assert value['actual_new_helper_qualification_sha256'] is None
    assert value['all_source_files_before_after_exact'] is True
    assert type(value['source_file_count']) is int and value['source_file_count'] > 0
    assert type(value['host_input_sources_and_original_helper_resource_factory_post_close_exact']) is int
    assert value['host_input_sources_and_original_helper_resource_factory_post_close_exact'] > 0
    for key in ('whole_build_qualified', 'whole_INPUT_admitted', 'native_RSS_qualified', 'AAA_accuracy_qualified', 'ABA_admitted', 'physical_balance_qualified'):
        assert value[key] is False
    assert value['separate_child_stderr_capture_verified'] is False
    assert value['child_stdout_stderr_merge_is_original_normal_guard'] is True
    for key in ('whole_seconds', 'child_seconds', 'sampled_peak_rss_mib'):
        assert type(value[key]) in (int, float) and not isinstance(value[key], bool)
        assert math.isfinite(value[key]) and value[key] >= 0
    for key in ('actual_external_Root_terminal', 'source_namespace_freeze', 'complete_namespace_manifest', 'actual_host_result', 'actual_control_report', 'actual_watchdog', 'actual_control_child_merged_stdout_stderr', 'actual_external_parent_stdout', 'actual_external_parent_stderr'):
        verify(value[key])

def validate_private_owner_controls(value):
    assert value['schema'] == 'AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1'
    assert value['status'] == 'ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY'
    positives = value['positive_controls']; rejects = value['private_guard_rejections']
    subtypes = value['accepted_str_subclass_equivalence_controls']; partial = value['partial_invalid_second_owner_rejections']
    assert len(positives) == 4 and [r['case'] for r in positives] == ['default_list', 'default_tuple', 'explicit_False_list', 'owned_builtin_list_True']
    for row in positives:
        assert row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default'] is True
        assert row['expected_complete_descriptor_signature'] == row['actual_complete_descriptor_signature']
        if row['case'] == 'owned_builtin_list_True': assert row['owned_list_completely_cleared_after_success'] is True
        else: assert row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
    assert len(rejects) == 3 and [r['case'] for r in rejects] == ['nonbool_consume', 'tuple_True', 'list_subclass_True']
    for row in rejects:
        assert row['class'] == 'InputGraphError'
        assert row['message'] == 'private owner consume needs a bool and an exclusively owned builtin list'
        assert row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
    assert len(subtypes) == 2 and [r['case'] for r in subtypes] == ['plain_accepted_str', 'accepted_str_with_str_override']
    for row in subtypes:
        assert row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True
        assert row['owned_list_completely_cleared_after_success'] is True
        assert row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default'] is True
        assert row['expected_complete_descriptor_signature'] == row['actual_complete_descriptor_signature']
    assert len(partial) == 2 and [r['case'] for r in partial] == ['invalid_second_owner_default', 'invalid_second_owner_owned_True']
    assert all(r['class'] == 'InputGraphError' and r['message'] == 'missing file owner' for r in partial)
    for key in ('first_valid_slot_None_after_original_validate_and_append', 'invalid_second_slot_original_identity_and_value_unchanged', 'default_partial_caller_unchanged', 'original_owner_rejection_class_order_message_preserved', 'original_protocol_controls_fixtures_and_caps_unchanged', 'no_new_fixture_file_or_IO_created'):
        assert value[key] is True
    assert value['new_helper_qualification_created'] is False and value['business_or_science_qualification_created'] is False

def require_bound_saved_reviews():
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    assert WRITER_SOURCE_STATUS == 'READY_ROOT_ACTUAL_SAVED_META_BOUND_V22'
    for key in REQUIRED_FUTURE_BINDING_FIELDS:
        value = globals()[key]
        if key.endswith('IDENTITY7'): assert type(value) is list and len(value) == 7 and all(type(v) is int for v in value)
        else: assert type(value) is str and bool(value)
    # The two immutable saved-review receipts still need Source adaptation to their
    # actual schemas/field names. This guard prevents using guessed old shapes.
    assert ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED is True


def main():
    require_bound_saved_reviews()
    assert not Q.exists()
    pure = read(P / 'Root_actual_pure_protocol_summary.json', 'f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4')
    fresh = read(E / 'Root_actual_fresh_verifier_summary.json', 'fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e')
    pure_peer = read(Path(PURE_PEER_PATH), PURE_PEER_SHA256)
    fresh_peer = read(Path(FRESH_PEER_PATH), FRESH_PEER_SHA256)
    assert pure_peer['blockers'] == []
    assert pure_peer['status'] == 'ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER'
    assert fresh_peer['status'] == 'SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED'
    assert pure_peer['all_explicit_input_SHA7ID_before_after_exact'] is True
    assert fresh_peer['all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal'] is True
    for entry in pure_peer['pins'] + fresh_peer['input_pins']:
        verify(entry)
    pure_term_path = P / 'Root_actual_pure_protocol_tool_terminal_return.json'
    fresh_term_path = E / 'Root_actual_fresh_verifier_tool_terminal_return.json'
    pure_terminal = terminal(pure_term_path, '86ab9d', 74949, '6f6847')
    validate_terminal_v22(pure_terminal, 'ROOT_V22_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1')
    assert pin(pure_term_path)['sha256'] == '12d8bbdef3cd59c2f9889d507cf8e5e646f37f4d7e0df1649381373c82100e78'
    fresh_terminal = terminal(fresh_term_path, '55ef8e', 29568, '57a6f5')
    validate_terminal_v22(fresh_terminal, 'ROOT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_TOOL_TERMINAL_RETURN_V1')
    assert pin(fresh_term_path)['sha256'] == 'de3750d802a442329089c5301d36939bda610ddc88bc7770dbe0c0f7f65a76f4'
    pure_tools = read(Path(PURE_PEER_TOOL_PATH), PURE_PEER_TOOL_SHA256)
    pure_review_return = pure_tools['actual_review_tool_result']
    assert type(pure_review_return['chunk_id']) is str and bool(pure_review_return['chunk_id'])
    assert type(pure_review_return['exit_code']) is int and pure_review_return['exit_code'] == 0
    assert 'session_id' not in pure_review_return
    fresh_tools = read(Path(FRESH_PEER_TOOL_PATH), FRESH_PEER_TOOL_SHA256)
    fresh_review_return = fresh_tools['actual_review_terminal_return']
    assert type(fresh_review_return['chunk_id']) is str and bool(fresh_review_return['chunk_id'])
    assert type(fresh_review_return['exit_code']) is int and fresh_review_return['exit_code'] == 0
    assert 'session_id' not in fresh_review_return and fresh_tools['actual_review_closed'] is True
    helper_pin = verify(pure['installed_helper'])
    assert helper_pin['sha256'] == 'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
    assert helper_pin['size_bytes'] == 148965
    assert verify(fresh['installed_helper']) == helper_pin
    pure_report = read(PO / 'ACTUAL_REPORT.json', '68a4fe6ca874a767221cf850bc2b37c33f8143613a56061b15c46c947a7cb4f5')
    small = read(PO / 'small_codec_and_rejection_controls.json')
    fixture = read(PO / 'small_fixture_controls.json')
    fresh_report = read(FO / 'ACTUAL_REPORT.json', 'bfd366a07fe897d210c61efc8c9aefdfa89add814ef210273ef97f2f10569976')
    assert fresh_report == fresh['complete_actual_report']
    validate_summary_v22(pure, 'PURE')
    validate_summary_v22(fresh, 'FRESH')
    owner_controls = pure_report['private_owner_consume_controls']
    assert owner_controls == pure['private_owner_consume_controls']
    validate_private_owner_controls(owner_controls)
    # Saved reviews are future immutable evidence, not the false closeout snapshot flags.
    assert pure_peer['private_owner_consume_full_contract_verified'] is True
    assert fresh_peer['complete_new_helper_namespace_lifetime_all_27_fields_verified'] is True
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
    assert pure['actual_pure_controls_pass'] is True and pure['closed'] is True
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
        'schema': 'AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_OWNER_NAMESPACE_HELPER_ACTUAL_JOINT_ADMISSION_V22',
        'status': 'QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V22',
        'helper': helper_pin,
        'actual_root_terminal': pin(pure_term_path),
        'actual_controls_summary': pin(P / 'Root_actual_pure_protocol_summary.json'),
        'actual_host_result': pin(PH / 'result.json'),
        'actual_control_report': pin(PO / 'ACTUAL_REPORT.json'),
        'complete_namespace_manifest': pin(P / 'Root_actual_pure_protocol_namespace_manifest.json'),
        'independent_actual_review': pin(Path(PURE_PEER_PATH)),
        'independent_actual_review_tool_return': pin(Path(PURE_PEER_TOOL_PATH)),
        'source_manifest': pin(P / 'Root_final_complete_qualification_SOURCE_freeze.json'),
        'full_protocol': full_protocol,
        'private_owner_consume_controls': owner_controls,
        'original_protocol_preserved_and_new_owner_controls_independently_saved_reviewed': True,
        'pure_source_member_count': pure['source_file_count'],
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
            'actual_controls_summary': pin(E / 'Root_actual_fresh_verifier_summary.json'),
            'actual_host_result': pin(FH / 'result.json'),
            'actual_control_report': pin(FO / 'ACTUAL_REPORT.json'),
            'complete_namespace_manifest': pin(E / 'Root_actual_fresh_verifier_namespace_manifest.json'),
            'independent_actual_review': pin(Path(FRESH_PEER_PATH)),
            'independent_actual_review_tool_return': pin(Path(FRESH_PEER_TOOL_PATH)),
            'sealed_independent_actual_review_manifest': pin(Path(FRESH_PEER_SEAL_PATH)),
            'source_manifest': pin(E / 'Root_final_complete_qualification_SOURCE_freeze.json'),
            'source_binding_record': verify(dict(path=FRESH_SOURCE_BINDING_RECORD_PATH, sha256=FRESH_SOURCE_BINDING_RECORD_SHA256, identity=FRESH_SOURCE_BINDING_RECORD_IDENTITY7)),
            'complete_gzips': full_gzips,
            'original_caps': {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_HOST_OUT_SOURCE_E_archive_bytes': 64 * 2**20, 'history_bytes': 96 * 2**30, 'free_bytes': 8 * 2**30, 'threads': 1, 'children': 1, 'retries': 0},
            'actual_measurement': {'whole_seconds': fresh['whole_seconds'], 'child_seconds': fresh['child_seconds'], 'sampled_peak_rss_mib': fresh['sampled_peak_rss_mib'], 'driver_reported_own_peak_rss_mib': fresh_peer['driver_reported_own_peak_rss_mib'], 'sample_and_self_peaks_are_distinct': True, 'joint_snapshot_plus_manifest_bytes_at_original_closeout': fresh_peer['joint_archive_snapshot_plus_manifest_bytes'], 'current_joint_regular_bytes_after_saved_peer_and_copy_receipts': current_joint_bytes},
            'full_public_return_field_order': fresh_report['complete_return_fields_retained'],
            'full_current_graph_metadata': fresh_report['independent_full_saved_graph_metadata'],
            'all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal': True,
            'complete_actual_unfiltered_read_trace_counts': fresh_report['actual_complete_trace_counts'],
            'private_positive_controls': 4, 'private_reject_controls': 3,
            'SOURCE33_and_all_fixed_inputs_before_after_unchanged': True,
            'legacy_SOURCE33_key_is_compatibility_alias_not_V22_source_count': True,
            'complete_source_member_count': fresh['source_file_count'],
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
    print(json.dumps({'status': admission['status'], 'qualification': pin(Q), 'unique_fresh_explicit_inputs': len(inputs), 'pure_Root_terminal': '6f6847', 'fresh_Root_terminal': '57a6f5', 'whole_build_INPUT_native_AAA_ABA_physics_qualified': False}, ensure_ascii=False))

if __name__ == '__main__':
    main()

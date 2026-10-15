"""UNREADY V22 complete Root helper joint-admission META writer template.

Only the new actual V22 pure/fresh summaries and terminals are Source-bound.
Both actual new saved-review field shapes are Source-adapted; archive pins remain
unbound None. No execution at import, no oldQ
qualification credit, no helper/guard/API/numeric code. Root must review and bind
actual saved reviews before this writer can create a fresh metadata-only Q.
"""
import math
import struct
import os
import sys
WRITER_SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_ACTUAL_SAVED_REVIEWS_REQUIRED_V22'
ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED = True  # Source-only exact new saved-META schema adaptation
PURE_PEER_PATH = None
PURE_PEER_SHA256 = None
FRESH_PEER_PATH = None
FRESH_PEER_SHA256 = None
PURE_PEER_TOOL_PATH = None
PURE_PEER_TOOL_SHA256 = None
PURE_PEER_SEAL_PATH = None
PURE_PEER_SEAL_SHA256 = None
PURE_PEER_SEAL_TOOL_PATH = None
PURE_PEER_SEAL_TOOL_SHA256 = None
FRESH_PEER_TOOL_PATH = None
FRESH_PEER_TOOL_SHA256 = None
FRESH_SOURCE_BINDING_RECORD_PATH = None
FRESH_SOURCE_BINDING_RECORD_SHA256 = None
FRESH_PEER_SEAL_PATH = None
FRESH_PEER_SEAL_SHA256 = None
FRESH_PEER_SEAL_TOOL_PATH = None
FRESH_PEER_SEAL_TOOL_SHA256 = None
FRESH_SOURCE_BINDING_RECORD_IDENTITY7 = None
REQUIRED_FUTURE_BINDING_FIELDS = ('PURE_PEER_PATH', 'PURE_PEER_SHA256', 'FRESH_PEER_PATH', 'FRESH_PEER_SHA256', 'PURE_PEER_TOOL_PATH', 'PURE_PEER_TOOL_SHA256', 'PURE_PEER_SEAL_PATH', 'PURE_PEER_SEAL_SHA256', 'PURE_PEER_SEAL_TOOL_PATH', 'PURE_PEER_SEAL_TOOL_SHA256', 'FRESH_PEER_TOOL_PATH', 'FRESH_PEER_TOOL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_PATH', 'FRESH_SOURCE_BINDING_RECORD_SHA256', 'FRESH_PEER_SEAL_PATH', 'FRESH_PEER_SEAL_SHA256', 'FRESH_PEER_SEAL_TOOL_PATH', 'FRESH_PEER_SEAL_TOOL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_IDENTITY7')

EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S = {'PURE_PEER_SHA256': '7afd373869bb7b130247dac45378918260a9110c25e548c4ee8ed4c1ce5a5bac', 'PURE_PEER_TOOL_SHA256': '38285bb20003c83028460af861a02e2c86690f7bf1e842a0732dc05cb9cbac33', 'PURE_PEER_SEAL_SHA256': '292237bebb6cea27559544c8dd357c7dc532ff8db741cc736bfd21e67b85f53a', 'PURE_PEER_SEAL_TOOL_SHA256': 'f889c4aabcc1487dd8b2253dba2568c5dccd193bf96ca77a41292437471526a7', 'FRESH_PEER_SHA256': 'a143da6f31aa8802d25799e8853591dcdc19ae5b4b285def64a8109c97df389f', 'FRESH_PEER_TOOL_SHA256': '701afc8dfdcf58e54c841956954b4a1c7bc3e6de68a4476dbc3c9f61823d171f', 'FRESH_PEER_SEAL_SHA256': 'ba5ff1e7600d8526393fbbce2087ece9cb46d142672de5d91b6881f597e8ea34', 'FRESH_PEER_SEAL_TOOL_SHA256': 'bf1c914537e6c11f78cbfb8e2edb00fead93667868e662dced65f88940879331'}

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
    # Field shapes are now the two new saved V22 schemas, never a guessed V21 shape.
    # All actual archive pins must still be Root-bound after this Source is reviewed.
    assert ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED is True
    for key, expected in EXPECTED_ACTUAL_SAVED_REVIEW_SHA256S.items():
        assert globals()[key] == expected



def exact_META(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return list(a) == list(b) and all(exact_META(a[k], b[k]) for k in a)
    if type(a) in (list, tuple):
        return len(a) == len(b) and all(exact_META(x, y) for x, y in zip(a, b))
    if type(a) is float:
        return math.isfinite(a) and math.isfinite(b) and struct.pack('>d', a) == struct.pack('>d', b)
    return a == b

def validate_pure_saved_review_v22(value):
    assert value['schema'] == 'INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1'
    assert value['PASS'] is True and value['hard_blockers'] == []
    assert type(value['check_count']) is int and value['check_count'] == len(value['checks']) == 1084
    assert all(type(x) is dict and type(x['PASS']) is bool and x['PASS'] is True for x in value['checks'])
    assert type(value['complete_full_EOF_reads']) is list and value['complete_full_EOF_reads']
    assert len({p['path'] for p in value['complete_full_EOF_reads']}) == 117
    for p in value['complete_full_EOF_reads']:
        assert type(p['identity']) is list and len(p['identity']) == 7 and all(type(i) is int for i in p['identity'])
        assert type(p['size_bytes']) is int and p['size_bytes'] == p['identity'][4]
    assert [x['label'] for x in value['complete_namespace_snapshots']] == ['D', 'H', 'O', 'E_pre_summary']
    for snapshot in value['complete_namespace_snapshots']:
        assert type(snapshot['regular_file_count']) is int and snapshot['regular_file_count'] == len(snapshot['regular_files'])
        assert type(snapshot['directory_count']) is int and snapshot['directory_count'] == len(snapshot['directories'])
        for entry in snapshot['regular_files'].values(): verify(entry)
        for identity7 in snapshot['directories'].values():
            assert type(identity7) is list and len(identity7) == 7 and all(type(i) is int for i in identity7)
        for link in snapshot['symlinks'].values():
            p = Path(link['path'])
            assert identity(p) == link['identity'] and p.is_symlink() and os.readlink(p) == link['target_text']
    assert value['pure_protocol_saved_evidence_independently_reviewed'] is True
    assert value['all_original_large_metadata_artifacts_fully_stream_hashed_without_API_or_decoder'] is True
    for k in ('material_or_actual_numerical_payload_read_or_decoded', 'helper_protocol_host_guard_driver_API_compile_or_numeric_executed_by_peer', 'Root_original_Project_D_E_ART_or_TMP_Source_packages_mutated_by_peer', 'old_closed_session_repolled', 'full_current_graph_verifier_qualified', 'whole_build_INPUT_native_physics_AAA_ABA_goal_credit'):
        assert value[k] is False
    assert value['new_Q'] is None

def validate_pure_saved_seal_v22(value, tool, audit):
    assert value['schema'] == 'INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL_V1'
    assert exact_META(value['actual_peer_audit_tool_return'], audit)
    assert type(value['actual_peer_exit_code']) is int and value['actual_peer_exit_code'] == 0 and value['actual_peer_closed'] is True
    assert value['all1084savedactualchecksPASS'] is True
    assert type(value['all_unique_explicit_Source_META_inputs_second_complete_EOF_SHA7ID_unchanged']) is int and value['all_unique_explicit_Source_META_inputs_second_complete_EOF_SHA7ID_unchanged'] == 117
    assert value['all_scoped_directory7IDs_and_two_literal_symlinks_second_checked'] is True
    assert value['actual_pure_protocol_saved_artifacts_reviewed'] is True and value['new_Q'] is None
    for k in ('full_current_graph_qualified_by_this_review', 'native_whole_Input_physics_AAA_ABA_or_goal_qualification', 'helper_guard_protocol_driver_API_compile_numeric_executed_by_peer', 'Root_original_project_D_E_ART_or_Source_packages_written', 'actual_original67_or_history_ART_wide_scan_performed'):
        assert value[k] is False
    for entry in value['complete_fresh_TMP_files_before_this_seal_and_future_actual_seal_receipt'].values(): verify(entry)
    assert tool['schema'] == 'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_PEER_SEAL_TOOL_RETURN_V1'
    assert tool['closed'] is True and tool['new_Q'] is None and tool['full_current_graph_or_native_or_science_qualified'] is False
    tr = tool['terminal_tool_return']
    assert tr['chunk_id'] == '28f447' and type(tr['exit_code']) is int and tr['exit_code'] == 0 and 'session_id' not in tr


def validate_fresh_saved_review_v22(value):
    assert value['schema'] == 'INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_SAVED_META_PEER_REVIEW_V1'
    assert value['PASS'] is True and value['hard_blockers'] == []
    assert type(value['check_count']) is int and value['check_count'] == len(value['checks']) == 686
    assert all(type(x['PASS']) is bool and x['PASS'] is True for x in value['checks'])
    assert value['full_current_graph_saved_evidence_independently_reviewed'] is True
    assert value['helper_metadata_qualification_receipt_created'] is False and value['new_Q'] is None
    for key in ('complete_build_qualified', 'whole_INPUT_admitted', 'native_RSS_qualified', 'AAA_accuracy_qualified', 'ABA_admitted', 'physical_balance_qualified'):
        assert value[key] is False
    assert len(value['all27_return_fields']) == 27
    assert len(value['complete_full_EOF_reads']) == 112 and len(value['unique_complete_fresh_rechecked_input_pins']) == 41
    assert [x['label'] for x in value['complete_namespace_snapshots']] == ['D', 'H', 'O', 'E_pre_summary']
    for snapshot in value['complete_namespace_snapshots']:
        assert type(snapshot['regular_file_count']) is int and snapshot['regular_file_count'] == len(snapshot['complete_regular_files'])
        assert type(snapshot['directory_count']) is int and snapshot['directory_count'] == len(snapshot['directories'])
        assert snapshot['symlinks'] == {}
        for entry in snapshot['complete_regular_files'].values(): verify(entry)
        for id7 in snapshot['directories'].values(): assert type(id7) is list and len(id7) == 7 and all(type(i) is int for i in id7)
    archive = value['original_archive_full_HODE_scope']
    assert archive['original_normal_guard_scope'] == ['H', 'O', 'D', 'E']
    assert archive['Root_DHO_ledger_is_not_original_HODE_scope'] is True
    assert type(archive['Root_saved_DHO_ledger_bytes']) is int and archive['Root_saved_DHO_ledger_bytes'] == 1611101
    assert type(archive['original_business_post_result_HODE_bytes']) is int and archive['original_business_post_result_HODE_bytes'] == 1620310
    assert type(archive['peer_current_full_HODE_bytes']) is int and archive['peer_current_full_HODE_bytes'] == 1664302
    assert archive['original_business_post_result_HODE_bytes'] < 64 * 2**20 and archive['peer_current_full_HODE_bytes'] < 64 * 2**20
    assert type(value['driver_own_peak_rss_bytes']) is int and value['driver_own_peak_rss_bytes'] / 2**20 == value['driver_own_peak_rss_mib'] < 512
    assert value['genuine_watchdog_sampled_peak_rss_mib'] == 345.390625
    assert value['unfiltered37112trace_complete_order_path_sequence_sha256'] == '54e9a6fe108093c2f92d31c8c2c5e38e0cad153ee170eafc8e59c44fa6d99a30'
    controls = value['actual_private_trace_controls']
    assert controls['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is True and controls['old60pure_control_functions_not_changed'] is True
    assert [r['case'] for r in controls['positive_controls']] == ['default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True']
    assert [r['case'] for r in controls['rejections']] == ['nonbool_consume','tuple_True','list_subclass_True']
    for r in controls['positive_controls']:
        assert r['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True
        if r['case'] == 'probe_owned_builtin_list_True': assert r['owned_list_completely_cleared'] is True
        else: assert r['caller_full_identity_type_order_value_floatbits_unchanged'] is True
    for r in controls['rejections']:
        assert r['class_name'] == 'InputGraphError' and r['message'] == 'private trace consume needs a bool and an exclusively owned builtin list'
        assert r['rejected'] is True and r['caller_type_identity_nested_value_order_floatbits_unchanged'] is True
    gzips = value['all_three_complete_gzip_pins']
    assert list(gzips) == ['expected_complete_return_contract', 'actual_complete_verifier_return', 'actual_complete_ReadOpenAudit_trace']
    for item in gzips.values():
        verify(item)
        assert item['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and item['no_fields_or_records_filtered'] is True
        assert type(item['uncompressed_JSON_bytes']) is int and item['uncompressed_JSON_bytes'] <= 64 * 2**20
    a = gzips['expected_complete_return_contract']; b = gzips['actual_complete_verifier_return']
    assert a['sha256'] == b['sha256'] and a['uncompressed_JSON_sha256'] == b['uncompressed_JSON_sha256'] and a['uncompressed_JSON_bytes'] == b['uncompressed_JSON_bytes']

def validate_fresh_saved_seal_v22(value, tool, audit):
    assert value['schema'] == 'INDEPENDENT_V22_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_META_PEER_SEAL_V1'
    assert exact_META(value['actual_peer_audit_tool_return'], audit)
    assert type(value['actual_peer_exit_code']) is int and value['actual_peer_exit_code'] == 0 and value['actual_peer_closed'] is True
    assert value['all686_saved_actual_checksPASS'] is True and type(value['hard_blocker_count']) is int and value['hard_blocker_count'] == 0
    assert value['all_unique_explicit_Source_META_inputs_second_complete_EOF_SHA7ID_unchanged'] is True
    assert type(value['unique_explicit_Source_META_inputs_rechecked_at_seal']) is int and value['unique_explicit_Source_META_inputs_rechecked_at_seal'] == 41
    assert value['all_complete_finite_namespace_directory7ID_and_member_sets_unchanged'] is True
    assert value['full_current_graph_saved_evidence_independently_reviewed'] is True and value['helper_metadata_qualification_receipt_created'] is False and value['new_Q'] is None
    for key in ('complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','Source_driver_host_guard_API_or_business_executed_by_peer','material_numeric_payload_or_broad_ART_read_by_peer','project_original_D_E_canonical_or_Root_artifact_written_by_peer'):
        assert value[key] is False
    assert value['original_frozen_D13files2dirs_not_appended'] is True
    verify(value['independent_saved_actual_review_report']); verify(value['actual_peer_audit_tool_receipt']); verify(value['actual_Root_fresh_tool_receipt'])
    for item in value['all_fresh_TMP_files_before_this_seal_and_future_actual_seal_tool_receipt'].values(): verify(item)
    assert tool['schema'] == 'INDEPENDENT_ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_META_PEER_SEAL_TOOL_RETURN_V1'
    assert tool['closed'] is True and tool['new_Q'] is None and tool['no_business_INPUT_native_RSS_or_science_credit'] is True
    tr = tool['terminal_tool_return']; assert tr['chunk_id'] == '407e5a' and type(tr['exit_code']) is int and tr['exit_code'] == 0 and 'session_id' not in tr

def main():
    require_bound_saved_reviews()
    assert not Q.exists()
    pure = read(P / 'Root_actual_pure_protocol_summary.json', 'f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4')
    fresh = read(E / 'Root_actual_fresh_verifier_summary.json', 'fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e')
    pure_peer = read(Path(PURE_PEER_PATH), PURE_PEER_SHA256)
    fresh_peer = read(Path(FRESH_PEER_PATH), FRESH_PEER_SHA256)
    validate_pure_saved_review_v22(pure_peer)
    validate_fresh_saved_review_v22(fresh_peer)
    # V22 complete EOF rows and sealed second reads replace the old peer-only alias.
    # V22 fresh complete EOF rows, second seal rechecks and member snapshots replace the old alias.
    for entry in pure_peer['complete_full_EOF_reads'] + fresh_peer['complete_full_EOF_reads'] + fresh_peer['unique_complete_fresh_rechecked_input_pins']:
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
    pure_review_return = pure_tools  # actual V22 peer stores the full raw exec_result
    assert pure_review_return['chunk_id'] == 'bfea93'
    pure_peer_seal = read(Path(PURE_PEER_SEAL_PATH), PURE_PEER_SEAL_SHA256)
    pure_peer_seal_tool = read(Path(PURE_PEER_SEAL_TOOL_PATH), PURE_PEER_SEAL_TOOL_SHA256)
    validate_pure_saved_seal_v22(pure_peer_seal, pure_peer_seal_tool, pure_tools)
    assert type(pure_review_return['chunk_id']) is str and bool(pure_review_return['chunk_id'])
    assert type(pure_review_return['exit_code']) is int and pure_review_return['exit_code'] == 0
    assert 'session_id' not in pure_review_return
    fresh_tools = read(Path(FRESH_PEER_TOOL_PATH), FRESH_PEER_TOOL_SHA256)
    assert fresh_tools['schema'] == 'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN_V1'
    assert fresh_tools['closed'] is True and fresh_tools['new_Q'] is None
    fresh_review_return = fresh_tools['terminal_tool_return']
    assert fresh_review_return['chunk_id'] == '722af0'
    assert type(fresh_review_return['chunk_id']) is str and bool(fresh_review_return['chunk_id'])
    assert type(fresh_review_return['exit_code']) is int and fresh_review_return['exit_code'] == 0
    assert 'session_id' not in fresh_review_return
    fresh_peer_seal = read(Path(FRESH_PEER_SEAL_PATH), FRESH_PEER_SEAL_SHA256)
    fresh_peer_seal_tool = read(Path(FRESH_PEER_SEAL_TOOL_PATH), FRESH_PEER_SEAL_TOOL_SHA256)
    validate_fresh_saved_seal_v22(fresh_peer_seal, fresh_peer_seal_tool, fresh_review_return)
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
    assert exact_META(pure_peer['actual_Root_pure_tool_receipt'], pure_terminal)
    assert verify(pure_peer['Root_summary_pin']) == pin(P / 'Root_actual_pure_protocol_summary.json')
    assert verify(pure_peer['Root_namespace_manifest_pin']) == verify(pure['complete_namespace_manifest'])
    saved_owner = pure_peer['original_and_new_complete_controls']
    for key, actual_key in [('new_owner_positive_controls', 'positive_controls'), ('new_owner_guard_rejections', 'private_guard_rejections'), ('new_owner_subtypes', 'accepted_str_subclass_equivalence_controls'), ('new_owner_invalid_second_rejections', 'partial_invalid_second_owner_rejections')]:
        assert exact_META(saved_owner[key], owner_controls[actual_key])
    assert verify(fresh_peer['actual_Root_fresh_tool_receipt']) == pin(fresh_term_path)
    assert exact_META(fresh_peer['actual_Root_terminal_tool_return'], fresh_terminal['terminal_tool_return'])
    assert verify(fresh_peer['Root_summary_pin']) == pin(E / 'Root_actual_fresh_verifier_summary.json')
    assert verify(fresh_peer['Root_namespace_manifest_pin']) == verify(fresh['complete_namespace_manifest'])
    assert exact_META(fresh_peer['complete_saved_graph_counts_and_fields'], fresh_report['independent_full_saved_graph_metadata'])
    assert exact_META(fresh_peer['actual_private_trace_controls'], fresh_report['private_trace_controls'])
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
    assert fresh_peer['all27_return_fields'] == fresh_report['complete_return_fields_retained']
    assert fresh_peer_seal['all27_fields_three_complete_gzip_streams_and37112_actual_records_retained'] is True
    assert fresh_peer_seal['original_full_graph_private_trace4positive3reject_and_original_caps_kept'] is True
    watch = fresh_peer['actual_watchdog']
    assert type(watch['returncode']) is int and watch['returncode'] == 0
    assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
    assert watch['limit_failure'] is None and watch['rss_cap_mib'] == 512 and watch['wall_cap_seconds'] <= 600
    assert len(fresh_report['complete_return_fields_retained']) == 27
    assert fresh_report['actual_complete_trace_counts'] == {'records': 37112, 'attempts': 37112, 'canonical_files': 37111, 'external_graph_reads': 1, 'no_subprocess_reexecuted': True}
    assert len(fresh_peer['actual_private_trace_controls']['positive_controls']) == 4 and len(fresh_peer['actual_private_trace_controls']['rejections']) == 3
    old = pure_report['full_old_saved_graph']
    meta = old['complete_original_metadata']
    assert meta == old['normal_strict_file_entrance_full_semantics_and_counts'] == old['normal_strict_payload_entrance_full_semantics_and_counts']
    assert old['full_default_roundtrip_exact'] is True and old['old_read_trace_not_replaced_by_new_trace'] is True
    assert old['original_legacy_semantic_sha_preserved'] is True
    counts = meta['complete_counts']
    assert counts['canonical_files'] == 36776 and counts['requirements'] == 237767 and counts['read_trace_records'] == 62332
    assert exact_META(saved_owner['complete_old_graph_counts'], counts)
    assert saved_owner['original_fixture_rejections'] == len(fixture['rejections']) == 37
    assert saved_owner['original_paired_fixture_rejection_cases'] == len(fixture['complete_rejected_arguments']) == 18
    assert saved_owner['original_codec_rejections'] == len(small['rejections']) == 61
    assert saved_owner['original_subtype_controls'] == len(pure_report['small_fixture']['accepted_str_subclass_equivalence_controls']) == 2
    assert exact_META(saved_owner['five_original_pure_checkpoints'], pure_report['stages'])
    subtypes = pure_report['small_fixture']['accepted_str_subclass_equivalence_controls']
    assert len(subtypes) == 2
    assert all(x['complete_builtin_output_values_types_order_floatbits_equal'] is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True for x in subtypes)
    assert pure_report['small_fixture']['caller_full_value_and_mutable_identity_preserved'] is True
    assert small['all_default_inputs_unmodified'] is True and small['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True
    assert small['ordinary_and_both_storage_strict_dispatches'] is True and len(small['rejections']) == pure_report['small_codecs']['rejections'] == 61
    trace = pure_report['full_new_creation_trace']
    assert trace['exact_full_roundtrip'] is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse'] is True and trace['default_source_nonmutation'] is True
    assert trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886
    assert saved_owner['full_new_trace_records'] == trace['full_record_count']
    pure_ledger = pure_peer['archive_ledger_scope']
    assert pure_ledger['joint_scope'] == ['D', 'H', 'O']
    assert pure_ledger['cap_bytes'] == 64 * 2**20
    assert pure_ledger['original_normal_guard_regular_file_bytes'] == 61013090
    assert pure_ledger['conservative_META_extra_symlink_literal_bytes'] == 38
    assert pure_ledger['Root_saved_META_total_DHO_bytes'] == pure['joint_source_host_out_bytes'] == 61013128
    assert pure_ledger['original_normal_guard_regular_file_bytes'] + pure_ledger['conservative_META_extra_symlink_literal_bytes'] == pure_ledger['Root_saved_META_total_DHO_bytes']
    assert pure_peer['pure_driver_peak_rss_bytes'] / 2**20 == pure['sampled_peak_rss_mib']
    assert pure_peer['actual_host_whole_seconds'] == pure['whole_seconds']
    assert pure['actual_pure_controls_pass'] is True and pure['closed'] is True
    assert pure['whole_seconds_cap'] == pure['stage_seconds_cap'] == 60 and pure['rss_mib_cap'] == 512
    assert pure['whole_seconds'] < 60 and pure['child_seconds'] < 60 and pure['sampled_peak_rss_mib'] < 512
    assert pure['joint_source_host_out_bytes'] < pure['archive_bytes_cap'] == 64 * 2**20
    assert fresh['whole_seconds_cap'] == 1800 and fresh['stage_seconds_cap'] == 600 and fresh['rss_mib_cap'] == 512
    assert fresh['whole_seconds'] < 1800 and fresh['child_seconds'] < 600 and fresh['sampled_peak_rss_mib'] < 512
    assert fresh_peer['driver_own_peak_rss_mib'] < 512
    for doc in [pure, fresh]:
        assert doc['threads'] == doc['children'] == 1 and doc['retries'] == 0
        assert doc['history_bytes_cap'] == 96 * 2**30
        assert doc.get('free_bytes_floor', doc.get('min_free_bytes')) == 8 * 2**30
    full_gzips = {k: verify(fresh_report[k]) for k in ['expected_complete_return_contract', 'actual_complete_verifier_return', 'actual_complete_ReadOpenAudit_trace']}
    assert exact_META(fresh_peer['all_three_complete_gzip_pins'], {k: fresh_report[k] for k in full_gzips})
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
        'sealed_independent_pure_actual_review_manifest': pin(Path(PURE_PEER_SEAL_PATH)),
        'independent_pure_actual_review_seal_tool_return': pin(Path(PURE_PEER_SEAL_TOOL_PATH)),
        'full_protocol_additional_complete_fixture_artifact': pin(PO / 'small_fixture_controls.json'),
        'full_protocol_additional_complete_codec_artifact': pin(PO / 'small_codec_and_rejection_controls.json'),
        'actual_measurement': {
            'whole_seconds': pure['whole_seconds'], 'child_seconds': pure['child_seconds'],
            'sampled_peak_rss_mib': pure['sampled_peak_rss_mib'],
            'actual_final_host_out_source_bytes': pure['joint_source_host_out_bytes'],
            'original_normal_guard_regular_file_bytes': pure_ledger['original_normal_guard_regular_file_bytes'],
            'conservative_META_extra_symlink_literal_bytes': pure_ledger['conservative_META_extra_symlink_literal_bytes'],
            'regular_and_symlink_literal_ledgers_are_distinct': True,
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
            'independent_actual_review_seal_tool_return': pin(Path(FRESH_PEER_SEAL_TOOL_PATH)),
            'source_manifest': pin(E / 'Root_final_complete_qualification_SOURCE_freeze.json'),
            'source_binding_record': verify(dict(path=FRESH_SOURCE_BINDING_RECORD_PATH, sha256=FRESH_SOURCE_BINDING_RECORD_SHA256, identity=FRESH_SOURCE_BINDING_RECORD_IDENTITY7)),
            'complete_gzips': full_gzips,
            'original_caps': {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_HOST_OUT_SOURCE_E_archive_bytes': 64 * 2**20, 'history_bytes': 96 * 2**30, 'free_bytes': 8 * 2**30, 'threads': 1, 'children': 1, 'retries': 0},
            'actual_measurement': {'whole_seconds': fresh['whole_seconds'], 'child_seconds': fresh['child_seconds'], 'sampled_peak_rss_mib': fresh['sampled_peak_rss_mib'], 'driver_reported_own_peak_rss_mib': fresh_peer['driver_own_peak_rss_mib'], 'sample_and_self_peaks_are_distinct': True, 'joint_snapshot_plus_manifest_bytes_at_original_closeout': fresh_peer['original_archive_full_HODE_scope']['original_business_post_result_HODE_bytes'], 'Root_saved_DHO_ledger_bytes_not_HODE_scope': fresh_peer['original_archive_full_HODE_scope']['Root_saved_DHO_ledger_bytes'], 'saved_peer_full_HODE_bytes': fresh_peer['original_archive_full_HODE_scope']['peer_current_full_HODE_bytes'], 'full_original_HODE_scope_preserved': True, 'current_joint_regular_bytes_after_saved_peer_and_copy_receipts': current_joint_bytes},
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

"""Finite SOURCE transformation only; does not execute generated META writer."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).absolute().parent
PARENT=HERE/'write_actual_joint_helper_admission_v22.exact_pure_saved_META.UNREADY.py'
raw=PARENT.read_bytes();assert hashlib.sha256(raw).hexdigest()=='e6925e7720dd2cd213c24c0d4c35ddf2391d6e3ccbb5d7883819c037be0a54f4'
text=raw.decode();hunks=[]
def edit(old,new):
 global text
 assert text.count(old)==1,old[:120]
 text=text.replace(old,new,1);hunks.append(dict(old=old,new=new))

edit('Saved-review pins/field shapes remain unknown. No execution at import, no oldQ\n', 'Both actual new saved-review field shapes are Source-adapted; archive pins remain\nunbound None. No execution at import, no oldQ\n')
edit('ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED = None', 'ACTUAL_SAVED_PEER_FIELD_SHAPES_SOURCE_REVIEWED = True  # Source-only exact new saved-META schema adaptation')
edit('FRESH_PEER_SEAL_SHA256 = None\n', 'FRESH_PEER_SEAL_SHA256 = None\nFRESH_PEER_SEAL_TOOL_PATH = None\nFRESH_PEER_SEAL_TOOL_SHA256 = None\n')
edit("'FRESH_PEER_SEAL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_IDENTITY7'", "'FRESH_PEER_SEAL_SHA256', 'FRESH_PEER_SEAL_TOOL_PATH', 'FRESH_PEER_SEAL_TOOL_SHA256', 'FRESH_SOURCE_BINDING_RECORD_IDENTITY7'")
edit("    # The two immutable saved-review receipts still need Source adaptation to their\n    # actual schemas/field names. This guard prevents using guessed old shapes.\n", "    # Field shapes are now the two new saved V22 schemas, never a guessed V21 shape.\n    # All actual archive pins must still be Root-bound after this Source is reviewed.\n")
edit("    assert fresh_peer['status'] == 'SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED'\n", "    validate_fresh_saved_review_v22(fresh_peer)\n")
edit("    assert fresh_peer['all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal'] is True\n", "    # V22 fresh complete EOF rows, second seal rechecks and member snapshots replace the old alias.\n")
edit("pure_peer['complete_full_EOF_reads'] + fresh_peer['input_pins']", "pure_peer['complete_full_EOF_reads'] + fresh_peer['complete_full_EOF_reads'] + fresh_peer['unique_complete_fresh_rechecked_input_pins']")
edit("    fresh_review_return = fresh_tools['actual_review_terminal_return']\n", "    assert fresh_tools['schema'] == 'INDEPENDENT_ACTUAL_COMPLETE_FRESH_VERIFIER_META_PEER_AUDIT_TOOL_RETURN_V1'\n    assert fresh_tools['closed'] is True and fresh_tools['new_Q'] is None\n    fresh_review_return = fresh_tools['terminal_tool_return']\n    assert fresh_review_return['chunk_id'] == '722af0'\n")
edit("    assert 'session_id' not in fresh_review_return and fresh_tools['actual_review_closed'] is True\n", "    assert 'session_id' not in fresh_review_return\n    fresh_peer_seal = read(Path(FRESH_PEER_SEAL_PATH), FRESH_PEER_SEAL_SHA256)\n    fresh_peer_seal_tool = read(Path(FRESH_PEER_SEAL_TOOL_PATH), FRESH_PEER_SEAL_TOOL_SHA256)\n    validate_fresh_saved_seal_v22(fresh_peer_seal, fresh_peer_seal_tool, fresh_review_return)\n")
edit("    assert fresh_peer['complete_new_helper_namespace_lifetime_all_27_fields_verified'] is True\n", "    assert verify(fresh_peer['actual_Root_fresh_tool_receipt']) == pin(fresh_term_path)\n    assert exact_META(fresh_peer['actual_Root_terminal_tool_return'], fresh_terminal['terminal_tool_return'])\n    assert verify(fresh_peer['Root_summary_pin']) == pin(E / 'Root_actual_fresh_verifier_summary.json')\n    assert verify(fresh_peer['Root_namespace_manifest_pin']) == verify(fresh['complete_namespace_manifest'])\n    assert exact_META(fresh_peer['complete_saved_graph_counts_and_fields'], fresh_report['independent_full_saved_graph_metadata'])\n    assert exact_META(fresh_peer['actual_private_trace_controls'], fresh_report['private_trace_controls'])\n")
edit("    assert fresh_peer['all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal'] is True\n    assert fresh_peer['complete_expected_actual_JSON_wire_bytes_equal'] is True\n    assert fresh_peer['one_genuine_stage_PASS'] is True and fresh_peer['liveness_group_cleanup'] is True\n    assert fresh_peer['limit_failure'] is None and fresh_peer['retries'] == 0\n", "    assert fresh_peer['all27_return_fields'] == fresh_report['complete_return_fields_retained']\n    assert fresh_peer_seal['all27_fields_three_complete_gzip_streams_and37112_actual_records_retained'] is True\n    assert fresh_peer_seal['original_full_graph_private_trace4positive3reject_and_original_caps_kept'] is True\n    watch = fresh_peer['actual_watchdog']\n    assert type(watch['returncode']) is int and watch['returncode'] == 0\n    assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True\n    assert watch['limit_failure'] is None and watch['rss_cap_mib'] == 512 and watch['wall_cap_seconds'] <= 600\n")
edit("    assert fresh_peer['private_positive_controls'] == 4 and fresh_peer['private_rejections'] == 3\n", "    assert len(fresh_peer['actual_private_trace_controls']['positive_controls']) == 4 and len(fresh_peer['actual_private_trace_controls']['rejections']) == 3\n")
edit("    assert fresh_peer['driver_reported_own_peak_rss_mib'] < 512", "    assert fresh_peer['driver_own_peak_rss_mib'] < 512")
edit("'driver_reported_own_peak_rss_mib': fresh_peer['driver_reported_own_peak_rss_mib']", "'driver_reported_own_peak_rss_mib': fresh_peer['driver_own_peak_rss_mib']")
edit("'joint_snapshot_plus_manifest_bytes_at_original_closeout': fresh_peer['joint_archive_snapshot_plus_manifest_bytes']", "'joint_snapshot_plus_manifest_bytes_at_original_closeout': fresh_peer['original_archive_full_HODE_scope']['original_business_post_result_HODE_bytes'], 'Root_saved_DHO_ledger_bytes_not_HODE_scope': fresh_peer['original_archive_full_HODE_scope']['Root_saved_DHO_ledger_bytes'], 'saved_peer_full_HODE_bytes': fresh_peer['original_archive_full_HODE_scope']['peer_current_full_HODE_bytes'], 'full_original_HODE_scope_preserved': True")
edit("    current_joint_bytes = 0\n", "    assert exact_META(fresh_peer['all_three_complete_gzip_pins'], {k: fresh_report[k] for k in full_gzips})\n    current_joint_bytes = 0\n")
edit("            'sealed_independent_actual_review_manifest': pin(Path(FRESH_PEER_SEAL_PATH)),\n", "            'sealed_independent_actual_review_manifest': pin(Path(FRESH_PEER_SEAL_PATH)),\n            'independent_actual_review_seal_tool_return': pin(Path(FRESH_PEER_SEAL_TOOL_PATH)),\n")

new_helpers='''
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

'''
edit('\ndef main():\n', '\n'+new_helpers+'def main():\n')
dest=HERE/'write_actual_joint_helper_admission_v22.COMPLETE.UNREADY.py';assert not dest.exists();dest.write_text(text);ast.parse(text)
restored=text
for h in reversed(hunks):assert restored.count(h['new'])==1;restored=restored.replace(h['new'],h['old'],1)
assert restored.encode()==raw
proof={'schema':'V22_EXACT_FRESH_SAVED_META_COMPLETE_WRITER_SOURCE_INVERSE_V1','source_only':True,'parent_path':str(PARENT),'parent_sha256':hashlib.sha256(raw).hexdigest(),'candidate_path':str(dest),'candidate_sha256':hashlib.sha256(text.encode()).hexdigest(),'complete_finite_hunks':hunks,'fullbyte_inverse':True,'fullAST_inverse':ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),'old_7_functions_unchanged':True,'both_actual_saved_peer_shapes_exact_Source_known':True,'all_actual_archived_peer_bindings_None':True,'new_Q_created':False,'generated_writer_executed':False}
with(HERE/'EXACT_FRESH_SAVED_META_COMPLETE_FULL_SOURCE_INVERSE.json').open('x')as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'source_only':True,'candidate':str(dest),'sha256':proof['candidate_sha256'],'size_bytes':len(text.encode()),'hunks':len(hunks),'new_Q_created':False,'still_UNREADY':True}))

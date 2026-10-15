"""Finite SOURCE transformation; never executes generated admission writer."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).absolute().parent
PARENT = HERE / 'write_actual_joint_helper_admission_v22.UNREADY.py'
raw = PARENT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'dc816f899d01623ed63a3cf421a4faa6bdb62ba1eac05972c1ff402e19d36217'
text = raw.decode('utf-8')
hunks = []

def edit(old, new):
    global text
    assert text.count(old) == 1, old[:120]
    text = text.replace(old, new, 1)
    hunks.append({'old': old, 'new': new})

edit('import math\n', 'import math\nimport struct\n')
edit('PURE_PEER_TOOL_SHA256 = None\n', 'PURE_PEER_TOOL_SHA256 = None\nPURE_PEER_SEAL_PATH = None\nPURE_PEER_SEAL_SHA256 = None\nPURE_PEER_SEAL_TOOL_PATH = None\nPURE_PEER_SEAL_TOOL_SHA256 = None\n')
edit("'PURE_PEER_TOOL_SHA256', 'FRESH_PEER_TOOL_PATH'", "'PURE_PEER_TOOL_SHA256', 'PURE_PEER_SEAL_PATH', 'PURE_PEER_SEAL_SHA256', 'PURE_PEER_SEAL_TOOL_PATH', 'PURE_PEER_SEAL_TOOL_SHA256', 'FRESH_PEER_TOOL_PATH'")
edit("    assert pure_peer['blockers'] == []\n    assert pure_peer['status'] == 'ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER'\n", "    validate_pure_saved_review_v22(pure_peer)\n")
edit("    assert pure_peer['all_explicit_input_SHA7ID_before_after_exact'] is True\n", "    # V22 complete EOF rows and sealed second reads replace the old peer-only alias.\n")
edit("    for entry in pure_peer['pins'] + fresh_peer['input_pins']:\n", "    for entry in pure_peer['complete_full_EOF_reads'] + fresh_peer['input_pins']:\n")
edit("    pure_review_return = pure_tools['actual_review_tool_result']\n", "    pure_review_return = pure_tools  # actual V22 peer stores the full raw exec_result\n    assert pure_review_return['chunk_id'] == 'bfea93'\n    pure_peer_seal = read(Path(PURE_PEER_SEAL_PATH), PURE_PEER_SEAL_SHA256)\n    pure_peer_seal_tool = read(Path(PURE_PEER_SEAL_TOOL_PATH), PURE_PEER_SEAL_TOOL_SHA256)\n    validate_pure_saved_seal_v22(pure_peer_seal, pure_peer_seal_tool, pure_tools)\n")
edit("    assert pure_peer['private_owner_consume_full_contract_verified'] is True\n", "    assert exact_META(pure_peer['actual_Root_pure_tool_receipt'], pure_terminal)\n    assert verify(pure_peer['Root_summary_pin']) == pin(P / 'Root_actual_pure_protocol_summary.json')\n    assert verify(pure_peer['Root_namespace_manifest_pin']) == verify(pure['complete_namespace_manifest'])\n    saved_owner = pure_peer['original_and_new_complete_controls']\n    for key, actual_key in [('new_owner_positive_controls', 'positive_controls'), ('new_owner_guard_rejections', 'private_guard_rejections'), ('new_owner_subtypes', 'accepted_str_subclass_equivalence_controls'), ('new_owner_invalid_second_rejections', 'partial_invalid_second_owner_rejections')]:\n        assert exact_META(saved_owner[key], owner_controls[actual_key])\n")
edit("    assert pure_peer['full_report_original_metadata_and_both_strict_entrances_equal'] is True\n    assert pure_peer['full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified'] is True\n", "    assert exact_META(saved_owner['complete_old_graph_counts'], counts)\n    assert saved_owner['original_fixture_rejections'] == len(fixture['rejections']) == 37\n    assert saved_owner['original_paired_fixture_rejection_cases'] == len(fixture['complete_rejected_arguments']) == 18\n    assert saved_owner['original_codec_rejections'] == len(small['rejections']) == 61\n    assert saved_owner['original_subtype_controls'] == len(pure_report['small_fixture']['accepted_str_subclass_equivalence_controls']) == 2\n    assert exact_META(saved_owner['five_original_pure_checkpoints'], pure_report['stages'])\n")
edit("    assert trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886\n", "    assert trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886\n    assert saved_owner['full_new_trace_records'] == trace['full_record_count']\n    pure_ledger = pure_peer['archive_ledger_scope']\n    assert pure_ledger['joint_scope'] == ['D', 'H', 'O']\n    assert pure_ledger['cap_bytes'] == 64 * 2**20\n    assert pure_ledger['original_normal_guard_regular_file_bytes'] == 61013090\n    assert pure_ledger['conservative_META_extra_symlink_literal_bytes'] == 38\n    assert pure_ledger['Root_saved_META_total_DHO_bytes'] == pure['joint_source_host_out_bytes'] == 61013128\n    assert pure_ledger['original_normal_guard_regular_file_bytes'] + pure_ledger['conservative_META_extra_symlink_literal_bytes'] == pure_ledger['Root_saved_META_total_DHO_bytes']\n    assert pure_peer['pure_driver_peak_rss_bytes'] / 2**20 == pure['sampled_peak_rss_mib']\n    assert pure_peer['actual_host_whole_seconds'] == pure['whole_seconds']\n")
edit("        'pure_source_member_count': pure['source_file_count'],\n", "        'pure_source_member_count': pure['source_file_count'],\n        'sealed_independent_pure_actual_review_manifest': pin(Path(PURE_PEER_SEAL_PATH)),\n        'independent_pure_actual_review_seal_tool_return': pin(Path(PURE_PEER_SEAL_TOOL_PATH)),\n")
edit("            'actual_final_host_out_source_bytes': pure['joint_source_host_out_bytes'],\n", "            'actual_final_host_out_source_bytes': pure['joint_source_host_out_bytes'],\n            'original_normal_guard_regular_file_bytes': pure_ledger['original_normal_guard_regular_file_bytes'],\n            'conservative_META_extra_symlink_literal_bytes': pure_ledger['conservative_META_extra_symlink_literal_bytes'],\n            'regular_and_symlink_literal_ledgers_are_distinct': True,\n")

new_helpers = '''
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

'''
edit('\ndef main():\n', '\n' + new_helpers + 'def main():\n')
dest = HERE / 'write_actual_joint_helper_admission_v22.exact_pure_saved_META.UNREADY.py'
assert not dest.exists()
dest.write_text(text)
ast.parse(text)
restored = text
for h in reversed(hunks):
    assert restored.count(h['new']) == 1
    restored = restored.replace(h['new'], h['old'], 1)
assert restored.encode() == raw
proof = {'schema':'V22_EXACT_ACTUAL_PURE_SAVED_META_WRITER_SOURCE_INVERSE_V1','source_only':True,'parent_path':str(PARENT),'parent_sha256':hashlib.sha256(raw).hexdigest(),'candidate_path':str(dest),'candidate_sha256':hashlib.sha256(text.encode()).hexdigest(),'complete_finite_hunks':hunks,'fullbyte_inverse':True,'fullAST_inverse':ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),'old_7_functions_unchanged':True,'fresh_peer_field_shape_still_unknown':True,'all_actual_archived_peer_pins_None':True,'new_Q_created':False,'generated_writer_executed':False}
with (HERE/'EXACT_PURE_SAVED_META_FULL_SOURCE_INVERSE.json').open('x') as f: json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'source_only':True,'candidate_path':str(dest),'sha256':proof['candidate_sha256'],'size_bytes':len(text.encode()),'hunks':len(hunks),'new_Q_created':False,'still_UNREADY':True}))

import ast
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
DEST=Path('/private/tmp/axmat_v12_producer_final_binding_independent_review_20261009')
CD=Path('/private/tmp/axmat_v12_graph_table_final_helper_pin_unready_source_only_20261009')
CP=CD/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.UNREADY.py'
MP=Path('/private/tmp/axmat_v12_owned_specs_identity_key_delta_graph_table_combined_source_only_20261009/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.UNREADY.py')
V11=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.py'
HELPER=ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/canonical_file_table_storage_Root_source_admission/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.READY_REVIEW_CANDIDATE.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def funcs(t,whole=False):
 nodes=ast.walk(ast.parse(t))if whole else ast.parse(t).body
 return {n.name:ast.get_source_segment(t,n)for n in nodes if isinstance(n,ast.FunctionDef)}
def inv(t,edits):
 for e in reversed(edits):
  assert t.count(e['new'])==1
  t=t.replace(e['new'],e['old'],1)
 return t
assert sha(CP)=='d5d1701a89651c877f2db3cda7a7118365a1267cf3b203211f55e4f6e2fcefb8'
assert sha(MP)=='4dd133d341c457d1ffb9ecc9ebd7c543ff430c221310d4869fcdce750e295c4c'
assert sha(V11)=='66d09b9c8a818e25c7c12acf10ba7551256d71f5fd60bde1c80da6d35d0d9481'
assert sha(HELPER)=='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
assert sha(CD/'REPORT.json')=='3d3be29f21ebea48021ac66fca2362bef0d9bdf74e9ff137ed092d3c1e4d0233'
assert sha(CD/'source_complete_inverse_proof.json')=='5c757c9cf6a7f29da340ecc2043f71ab4ab1f4606ef2353698801699544d0e44'
ct=CP.read_text();mt=MP.read_text();vt=V11.read_text();proof=read(CD/'source_complete_inverse_proof.json');report=read(CD/'REPORT.json');receipt=read(CD/'actual_source_binder_tool_receipt.json')
assert inv(ct,[proof['one_region_edit']])==mt
assert len(proof['full_edits'])==11 and inv(ct,proof['full_edits'])==vt
assert len(funcs(ct))==65 and funcs(ct)==funcs(mt)
assert len(funcs(ct,True))==70 and funcs(ct,True)==funcs(mt,True)
assert "'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py','e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28')" in ct
assert "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_CANONICAL_FILE_TABLE_COMBINED_V12'" in ct
assert len(report['future_actual'])==25 and all(v is None for v in report['future_actual'].values())
for key,value in report['retained_real_V11_component_pins'].items():
 assert key+' = '+repr(value) in ct
assert len(report['retained_real_V11_component_pins'])==6
for line in vt.splitlines():
 if any(line.startswith(k+' =') for k in ('TOTAL_WALL, STAGE_WALL, RSS','RESERVE, HISTORY_CAP, FREE_FLOOR','BODY_BINDING')):assert line in ct
p=funcs(ct);v=funcs(vt)
assert p['create_complete_input_graph'].replace('json.dump(g.encode_canonical_file_table_storage(graph),f,','json.dump(graph,f,',1)==v['create_complete_input_graph']
for key in v:
 if key!='create_complete_input_graph':assert p[key]==v[key]
assert receipt['actual_tool_return_observed'] is True and receipt['record_written_after_actual_return'] is True
assert type(receipt['actual_tool']['exit_code'])is int and receipt['actual_tool']['exit_code']==0
assert receipt['candidate']['sha256']==sha(CP) and receipt['complete_inverse_proof']['sha256']==sha(CD/'source_complete_inverse_proof.json')
for key in ('no_business_import','no_business_execution','no_project_write','no_Root_session_poll'):assert receipt[key] is True
for key in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert receipt[key] is False
READY_DIR=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
READY=READY_DIR/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.READY_REVIEW_CANDIDATE.py'
READY_PROOF=READY_DIR/'Root_READY_producer_13_region_complete_inverse_proof.json'
assert sha(READY)=='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
assert sha(READY_PROOF)=='7e287ac67264bdb81afe2e13134056ceaeb57bbe71c17b6c88a7c8c30c646af9'
rt=READY.read_text();rp=read(READY_PROOF)
assert len(rp['Root_only_two_text_regions'])==2 and inv(rt,rp['Root_only_two_text_regions'])==ct
assert len(rp['complete_regions'])==13 and inv(rt,rp['complete_regions'])==vt
assert funcs(rt)==funcs(ct) and funcs(rt,True)==funcs(ct,True)
assert "DRAFT_STATUS = 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'" in rt
assert "'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py','e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28')" in rt
assert 'Future combined build success, native RSS, AAA accuracy and ABA require actual fresh qualification.' in rt
result=dict(schema='AXMAT_V12_FINAL_READY_HELPER_PIN_PRODUCER_INDEPENDENT_STATIC_REVIEW_V1',status='PASS_SOURCE_PIN_BINDING_ONLY_PRODUCER_STILL_UNREADY',candidate=dict(path=str(CP),sha256=sha(CP)),mother=dict(path=str(MP),sha256=sha(MP)),bound_READY_helper=dict(path=str(HELPER),sha256=sha(HELPER)),single_region_final_helper_hash_binding=True,all65_top_and70_total_function_bodies_byteexact_to4dd=True,full11region_inverse_to66d=True,all64_nonwriter_functions_byteexact_to66d=True,writer_only_explicit_nonmutating_storage_expression_changed=True,all6_actual_V11_component_pins_exact=True,all25_report_future_success_count_inventory_fields_None=True,UNREADY_status_retained=True,full7INPUT_complete_graph_members_owners_aliases_trace_and_live_resources_not_changed=True,genuine_module_and_class_MRO_contracts_retained=True,all_original_budget_constants_unchanged=True,source_copy_inventory_and_code_self_owner_identity_propagation_retained=True,existing_59_pure_controls_not_reexecuted=True,original_binder_actual_receipt=dict(path=str(CD/'actual_source_binder_tool_receipt.json'),sha256=sha(CD/'actual_source_binder_tool_receipt.json'),chunk_id=receipt['actual_tool']['chunk_id'],returncode=receipt['actual_tool']['exit_code']),required_before_actual_PREP=['Root READY and truthful docstring conversion is only source text/status; keep a complete inverse proof for those two additional regions and all original function bodies.','Install final reviewed helper e8 and final factory ordinary files with matching SHA pins; prospective new source/runtime helper and factory copies are inventoried fresh by genuine PREP.','Fresh actual graph/declaration/pins/counts and PREP terminal witness remain unproven until the real new bounded operation returns; older failed V11 run remains failed.'],findings=[],project_files_written=False,business_imports_or_calls=False,new_formal_PREP_or_RUN_executed=False,new_combined_build_admission_verified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
result.update(status='PASS_FINAL_ROOT_READY_PRODUCER_SOURCE_ONLY',Root_READY_candidate=dict(path=str(READY),sha256=sha(READY)),Root_READY_proof=dict(path=str(READY_PROOF),sha256=sha(READY_PROOF)),Root_READY_only_doc_and_status_two_regions=True,Root_READY_all65_top_and70_total_functions_byteexact=True,Root_READY_complete13region_inverse_to66d=True,Root_READY_binding_final_e8_helper=True)
DEST.mkdir(exist_ok=True)
out=DEST/'REPORT.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(status=result['status'],path=str(out),sha256=sha(out)),ensure_ascii=False))

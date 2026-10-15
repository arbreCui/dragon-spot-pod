#!/usr/bin/env python3
"""Review newly authored actual admissions and frozen candidate metadata; never imports Host."""
import ast,hashlib,json,os,stat,difflib
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
C=R/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014';D=R/'independent_v15_actual_candidate_final_Source_review_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,q=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 with p.open('rb')as f:assert ids(os.fstat(f.fileno()))==ids(s);b=f.read();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);pf=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
 if q is not None:assert pf==norm(q),(str(p),'PF')
 return b,pf
def load(p,q=None):
 b,pf=read(p,q);return json.loads(b),pf
def segments(s):return{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
ready,readyp=load(C/'SOURCE_REVIEW_READY.json');plan,planp=load(C/'ACTUAL_PREREQUISITE_BOUND_V15_SOURCE_PREPARATION_PLAN.json')
hb,hostp=read(C/'run_actual_three_plane_pipeline.py',plan['host_source']);text=hb.decode();ast.parse(hb)
assert hostp['sha256']=='b104643ec979c438ccc638e4e5278bc7e0a7279540dd567e9411090d8496f365'and hostp['size_bytes']==114682
assert planp['sha256']=='822d81f0c8d7443be8ff99c9e6ad2024d018148afb7c9a7a92f2006813732c20'
assert ready['host_source']==hostp and ready['plan_pin']==planp and ready['source_only']is True and ready['failure']is None
inverse,ip=load(plan['complete_byte_inverse_pin']['path'],plan['complete_byte_inverse_pin']);basebytes,basep=read(inverse['original_pin']['path'],inverse['original_pin'])
assert inverse['candidate_pin']==hostp and len(inverse['changes'])==5
restored=text
for block in reversed(inverse['changes']):assert restored.count(block['after'])==1;restored=restored.replace(block['after'],block['before'],1)
assert restored.encode()==basebytes and hashlib.sha256(restored.encode()).hexdigest()=='bb1ee861ae91318ea67ea12bbb5b6eb19c0be7690064b1b0caf4de3d2aa54fdc'
for block in inverse['changes'][1:3]:assert block['before'].startswith('+')and block['after']==block['before'][1:]
helpers=[]
for pair in plan['helper_byte_equality']:
 b,p=read(pair['candidate_pin']['path'],pair['candidate_pin']);a,o=read(pair['predecessor_pin']['path'],pair['predecessor_pin']);assert b==a;helpers.append(dict(candidate_pin=p,predecessor_pin=o,wholebytes_equal=True))
oldhf,oldhfp=load(plan['original_v14_Host_freeze_pin']['path'],plan['original_v14_Host_freeze_pin'])
assert len(oldhf['dependencies'])==377 and plan['original377_dependency_rows_to_retain']==oldhf['dependencies']
old14bytes,old14p=read(oldhf['host_source']['path'],oldhf['host_source']);old14text=old14bytes.decode()
for name in ['ParentObservationFailure','ParentMemoryObservation','FirstFatal']:assert segments(text)[name]==segments(old14text)[name],name
assert segments(text)['PhaseResources']==segments(basebytes.decode())['PhaseResources']
assert segments(text)['classify_storage_inventory']==segments(basebytes.decode())['classify_storage_inventory']
assert inverse['original50_continuous_source_bytes']==18902 and inverse['original50_continuous_source_unchanged']is True
assert inverse['original50_continuous_source_sha256']=='7cc6f56f2864cfd8eb1e9300221434a6b6b41605a40f8604889ad13c1b65c801'
assert all('BOOT_positive'not in block['after']and 'GLOBAL_positive'not in block['after']for block in inverse['changes'])
deps=plan['dependencies'];assert len(deps)==2790 and len({q['path']for q in deps})==2790
table={q['path']:norm(q)for q in deps}
for q in deps:assert ids(Path(q['path']).lstat())==q['identity']and stat.S_ISREG(q['identity'][2]),q['path']
for q in oldhf['dependencies']:assert table[q['path']]==norm(q)
selected=plan['selected_actual_prerequisites'];documents={}
for key,q in selected.items():assert table[q['path']]==q;documents[key]=load(q['path'],q)[0]
report_HF_pairs=[('selected_actual_new_build70_report_pin','selected_new_build_Host_freeze_pin',2),('selected_actual_fresh17_report_pin','selected_fresh17_Host_freeze_pin',20),('selected_actual_private_model_report_pin','selected_private_model_Host_freeze_pin',3),('selected_actual_public7_report_pin','selected_public7_Host_freeze_pin',11)]
for rkey,hkey,count in report_HF_pairs:
 report=documents[rkey];own=documents[hkey]
 assert report['actual_host_Source_freeze_pin']==selected[hkey]and len(report['records'])==count and all(x['status']=='PASS'for x in report['records'])
 assert report['failure']is None and report['after_check_error']is None and report['secondary_failures']==[]and report['final_report_resource_check_passed']is True
 for q in[own['host_source']]+own['dependencies']+report['fixed_current_pins']+report['output_pins']:assert table[q['path']]==norm(q),q['path']
bindings,bindingp=load(plan['direct_alias_binding_pin']['path'],plan['direct_alias_binding_pin'])
build=documents['selected_actual_new_build70_report_pin'];new70=bindings['actual_original_ordered_70_link_inputs']
assert len(new70)==70 and len({q['path']for q in new70})==70 and [q['path']for q in new70]==build['actual_complete70_link_inputs']
assert bindings['selected_actual_build70_report_pin']==selected['selected_actual_new_build70_report_pin']
assert bindings['actual_complete70_source_freeze_pin']==selected['selected_new_Fortran_Source_freeze_pin']
assert new70[12]==bindings['excluded_original_main_pin']and Path(new70[12]['path']).name=='DRAGON.o'
assert new70[40]['sha256']=='1118ab3d4b705d3732914aa2bd774919a173c24c20ff932cfd7650f35d51e574'
assert bindings['only_main_object_replacement']is True and bindings['physics_qualification']is False and bindings['actual_pipeline_executed']is False
assert bindings['new_probe_source']==str(C/'direct_alias_entry_controls.f90')
assert [ix for ix,(old,new)in enumerate(zip(build['original_ordered70_input_pins'],new70))if old!=new]==[40]
public=documents['selected_actual_public7_report_pin'];phf=documents['selected_public7_Host_freeze_pin']
event=public['actual_completed_bundle_retirements'][0];assert len(public['actual_completed_bundle_retirements'])==1
intent,intentp=load(event['intent_pin']['path'],event['intent_pin']);receipt,receiptp=load(event['receipt_pin']['path'],event['receipt_pin'])
assert receipt==event['operation']and all(receipt[k]is True for k in ['intent_parent_fsync_returned','unlink_returned','parent_fsync_returned','retirement_completed','removed_current_owned_fullpin'])
assert event['current_bundle_pin']is None and event['post_receipt_failure']is None and receipt['actual_retired_count']==1
src=next(x for x in public['actual_stale_host_evidence']if x['case']=='public_read_stale_BQ_SRC')
mac=next(x for x in public['actual_stale_host_evidence']if x['case']=='public_read_stale_BQ_MAC')
historical=src['actual_bundle_before_pin'];assert historical==src['actual_bundle_after_pin']and src['current_bundle_pin']is None and not os.path.lexists(historical['path'])
assert mac['current_bundle_pin']==mac['actual_bundle_after_pin']and table[mac['current_bundle_pin']['path']]==mac['current_bundle_pin']
for q in deps:assert q['path']!=historical['path']and q['identity'][:2]!=historical['identity'][:2]
parent=Path(historical['path']).parent.lstat();after=receipt['parent_after_identity']
assert ids(parent)[:3]==after[:3]and parent.st_nlink==after[3]+1 and parent.st_size==after[4]+32 and parent.st_mtime_ns>=after[5]and parent.st_ctime_ns>=after[6]
lifetime=documents['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin']
assert phf['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin']==selected['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin']
assert lifetime['maximum_live_synthetic_context_bundles']==1 and lifetime['future_actual_public7_report_pin']is None
for q in[event['intent_pin'],event['receipt_pin']]:assert table[q['path']]==q
for required in ["if any(key not in document or document[key]is not None for key in keys)","receipt!=event['operation']","before_parent[3]!=before_intent[3]+1","after_parent[3]!=before_parent[3]-1","parent.st_nlink!=after_parent[3]+1","exact_public_live_pin(report,bundle,cwd/'coherent_complete_context.xsm')","for rows in (hf['dependencies'],own['dependencies'],report['fixed_current_pins'],report['output_pins'],report['owned_runtime_pins'])","old17_is_historical_source_oracle_only=True","current70_link=build['actual_complete70_link_inputs']","core[5]=compact['object_pin']['path']","observed=actual.get(key[9:])","includes=['-I'+str(root/'build'),'-I'+str(Path(compact['object_pin']['path']).parent)"]:assert required in text,required
assert text.count('def admit_exact_public_stale_lifetimes')==1
assert not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='unlink'for n in ast.walk(ast.parse(segments(text)['admit_exact_public_stale_lifetimes'])))
csf=documents['selected_post_release_Common_Source_freeze_pin'];assert plan['current_Common_Source_freeze_pin']==selected['selected_post_release_Common_Source_freeze_pin']
assert csf['new_Common_Source_pin']==phf['selected_post_release_Common_Source_pin']and table[csf['new_Common_Source_pin']['path']]==csf['new_Common_Source_pin']
assert csf['new_Common_Source_pin']['path']in text
caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=536870912,threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2147483648,history_cap_bytes=103079215104,filesystem_floor_bytes=8589934592,original_cold_reserve_bytes=20971764748)
assert plan['original_caps']==caps and plan['strict_forecast_MiB']==dict(BOOT_solve=2032,BOOT_seal=1888,aux=128,fresh=2048)
assert plan['actual_prerequisite_counts']==dict(new_build70=2,fresh17=20,private_model=3,public7=11)
assert plan['original_pipeline_records_expected']==dict(total=50,PASS=17,expected_refusal=33)
assert all(plan[k]is False for k in['actual_pipeline_executed','compiler_executed','numerical_executed','files_deleted','AAA_qualified','ABA_admitted'])
assert all(plan[k]is None for k in['own_Host_freeze_pin','own_CLI_pin','future_actual_v15_report_pin'])
assert not Path(plan['planned_output_root']).exists()and not (C/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').exists()and not(C/'DECLARED_EXECUTION_INTERFACE.json').exists()
prep,prepp=load(R/'ACTUAL_V15_ACTUAL_PREREQUISITE_BOUND_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json');pr=prep['actual_Source_preparation_return']
assert prep['observed_closed']is True and type(pr['exit_code'])is int and pr['exit_code']==0 and pr.get('session_id')is None and pr['chunk_id']=='0003b0'
freezerb,freezerp=read(R/'freeze_v15_actual_compact_pipeline_host_source_only_v1_20261014.py');assert freezerp['sha256']=='ceb506b4f37f7643c85d87343a94a1100e92bc770eb6a3b5d97ddee1123811dc';ast.parse(freezerb)
for required in [b"type(actual.get('exit_code'))is not int",b"tools.get('observed_closed')is not True",b"actual.get('session_id')is not None",b"json.loads(lines[-1]).get('review_pin')!=review_pin",b"review.get('numerical_executed')is not False",b"if row not in reviewed",b"dependencies=unique(plan['dependencies']",b"freeze=dict(original)",b"complete_original_v14_dependency_rows_retained=377",b"future_actual_v15_summary_pin=None",b"'private-model','public-read-seven'",b"exact_reviewable_argv=argv"]:assert required in freezerb,required
assert b'exec_module'not in freezerb and b'os.unlink'not in freezerb and b'subprocess'not in freezerb
report=dict(schema='INDEPENDENT_V15_ACTUAL_BOUND_CANDIDATE_NEW_SOURCE_REVIEW_V1',status='PASS_V15_ACTUAL_BOUND_CANDIDATE_NEW_SOURCE_READY_FOR_SOURCE_ONLY_FREEZE',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,Host_imported_or_executed=False,
 candidate_host_source_pin=hostp,actual_Source_plan_pin=planp,actual_Source_ready_pin=readyp,whole_Source_inverse_pin=ip,direct_alias_binding_pin=bindingp,Source_freezer_pin=freezerp,
 actual_Source_preparation_true_tools_pin=prepp,genuine_actual_Source_preparation_return=pr,predecessor_draft2_Source_pin=basep,original_v14_Host_freeze_pin=oldhfp,original_v14_Host_Source_pin=old14p,exact_five_changed_blocks_whole_inverse_matches_draft2=True,two_literal_leading_plus_semantic_faults_removed=True,expected_prefix_token_strip9_verified=True,
 original50_continuous18902_source_bytes_preserved=True,original50_continuous_source_sha256=inverse['original50_continuous_source_sha256'],original_ParentObservation_FirstFatal_classes_wholebytes_unchanged=True,three_helpers_wholebytes_equal=helpers,
 selected_actual_prerequisite_pins=selected,all4_actual_closed_counts_and_ownHF_Fixed_Output_closures_bound=True,actual_prerequisite_counts=plan['actual_prerequisite_counts'],current_Source_dependency_count=2790,original377_all_PF_rows_retained=True,all2790_current7_reobserved=True,
 actual_new_ordered70_index40_only_changes_BOOTQ_and_alias_only_main_index12=True,actual_core6_newQ_same_across_build_fresh17_model_public7=True,old69_cache70_and_old17_sources_retained_historical_math_oracle_only=True,
 exact_first_SRC_retirement_currentNone_and_current_MAC_admission=True,actual_retirement_intent_pin=intentp,actual_retirement_receipt_pin=receiptp,retired_SRC_historical_completed_before_after_fullpin=historical,retired_SRC_path_and_inode_absent_from_current_dependency_closure=True,exact_SRC_current_directory_after_retained_receipt_contract_matches_actual=True,no_generic_missing_PF_allowance=True,
 current_Common_Source_freeze_pin=plan['current_Common_Source_freeze_pin'],original_caps=caps,strict_forecast_MiB=plan['strict_forecast_MiB'],original_50_record_plan=plan['original_pipeline_records_expected'],original_math_material_or_threshold_changes=False,
 final_HF_and_CLI_not_created_by_review=True,future_actual_v15_report_pin=None,planned_v15_OUT_absent=True,original_draft1_and_draft2_authored_by_this_reviewer=True,
 independent_review_scope='New five-block candidate changes and final actual admissions authored by parent; unchanged draft1/draft2 conservation is byte/inverse verified and earlier independent Root/child reviews remain necessary. No self-authored baseline logic is presented as independently authored or newly qualified.',
 fixtures_repeated=False,science_fullEOF_repeated=False,all_file_descriptors_closed=True,production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,
 limitation='Source-only readiness for one frozen HF/CLI. Root must separately run all50 original stages and evaluate actual terminal/scientific/physical results; no complete pipeline success is inherited from precursor controls.')
D.mkdir(exist_ok=True);p=D/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 b=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,b)==len(b);os.fsync(fd)
finally:os.close(fd)
_,qp=read(p);print(json.dumps(dict(status=report['status'],review_pin=qp,candidate_host_source_pin=hostp,source_only=True,numerical_executed=False,all_file_descriptors_closed=True)))

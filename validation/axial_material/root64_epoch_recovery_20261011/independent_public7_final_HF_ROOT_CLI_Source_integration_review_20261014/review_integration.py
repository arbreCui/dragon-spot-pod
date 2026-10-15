#!/usr/bin/env python3
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');P=R/'public_read_compact_bq_admission_control_host_source_v7_20261014';D=R/'independent_public7_final_HF_ROOT_CLI_Source_integration_review_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(q):return{k:q[k]for k in('path','sha256','size_bytes','identity')}
def read(p,q=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 with p.open('rb')as f:assert ids(os.fstat(f.fileno()))==ids(s);b=f.read();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);pf=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
 if q is not None:assert pf==norm(q),str(p)
 return b,pf
def load(p,q=None):
 b,pf=read(p,q);return json.loads(b),pf
def current(q):
 s=Path(q['path']).lstat();assert stat.S_ISREG(s.st_mode)and ids(s)==q['identity']
hf,hfp=load(P/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json');assert hfp['sha256']=='394f0bc9b7b5492bc7465fbfd105ac331f9b6b07c83cc89d4b733312e461b6e6'and len(hf['dependencies'])==2629
template,templatep=load(P/'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json');assert templatep['sha256']=='17942a547e91c57531e4b115967762d9421393a41cc1ae556dd62034eae54f18'
cli,clip=load(R/'ROOT_EXACT_COMPACT_BQ_PUBLIC_CONTROLS_V7_ARGV_BOUND_TO_ACTUAL_BUILD_20261014.json');assert clip['sha256']=='21754746151bacef8135535ca0beb36d8d15826949648283dc08886f56a53e2c'
hb,hostp=read(hf['host_source']['path'],hf['host_source']);assert hostp['sha256']=='b5585624107b4e6b8fc027621d52ba868295b9140cca0c7f943c616e3f41512a'
ast.parse(hb);plan,planp=load(hf['control_host_plan_pin']['path'],hf['control_host_plan_pin'])
life,lifep=load(hf['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin']['path'],hf['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin'])
bhf,bhfp=load(hf['selected_new_build_Host_freeze_pin']['path'],hf['selected_new_build_Host_freeze_pin'])
old,oldp=load(hf['predecessor_Host_source_freeze_pin']['path'],hf['predecessor_Host_source_freeze_pin'])
original,originalp=load(R/'bq64_compact_expected_build_host_source_v3_20261013/COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json')
table={q['path']:norm(q)for q in hf['dependencies']};assert len(table)==2629
for q in hf['dependencies']:current(q)
for group,expected in [(bhf['dependencies'],2565),(old['dependencies'],2609),(original['dependencies'],2532)]:
 assert len(group)==expected
 for q in group:assert table[q['path']]==norm(q)
peer,peerp=load(hf['independent_Host_Source_review_pin']['path'],hf['independent_Host_Source_review_pin'])
tools,toolp=load(hf['independent_Host_Source_true_tool_return_pin']['path'],hf['independent_Host_Source_true_tool_return_pin'])
ar=tools['actual_review_return'];assert tools['observed_closed']is True and type(ar['exit_code'])is int and ar['exit_code']==0 and ar.get('session_id')is None and ar['chunk_id']=='4af06c'
assert norm(json.loads(ar['output'].strip().splitlines()[-1])['review_pin'])==peerp
assert peer['failure']is None and peer['source_only']is True and peer['business_executed']is False and peer['compiled']is False and peer['numeric']is False
assert peer['actual_Host_source_pin']==hostp and peer['actual_control_host_plan_pin']==planp and peer['actual_lifetime_Source_plan_pin']==lifep
freeze,freezep=load(R/'ACTUAL_PUBLIC7_COMPLETED_FIRST_SRC_BUNDLE_LIFETIME_FINAL_SOURCE_FREEZE_TRUE_TOOL_RETURNS_20261014.json')
fr=freeze['actual_final_Source_freeze_tool_return'];first=freeze['initial_actual_failed_metadata_interface_Source_freeze_tool_return']
assert fr['chunk_id']=='f9d72d'and type(fr['exit_code'])is int and fr['exit_code']==0 and fr.get('session_id')is None
assert first['chunk_id']=='ff0320'and type(first['exit_code'])is int and first['exit_code']==1
fp=json.loads(fr['output'].strip().splitlines()[-1])['packages'];assert len(fp)==1 and fp[0]['host_freeze_pin']==hfp and fp[0]['argv_Source_template_pin']==templatep and fp[0]['host_source_pin']==hostp and fp[0]['dependency_count']==2629
freezerb,freezerp=read(R/'freeze_public_read_compact_bq_lifetime_host_source_v7_source_only_20261014.py');assert freezerp['sha256']=='b457bc42d27df002288ccb198d1671c7343cb9ece0f87a78a3a5bb9cbfec0937';ast.parse(freezerb)
assert b"peer.get('numerical_executed',peer.get('numeric'))is False"in freezerb and b"actual.get('session_id')is None"in freezerb and b"type(actual['exit_code'])is int"in freezerb
for key in ['selected_new_build_Host_freeze_pin','selected_new_Fortran_Source_freeze_pin','selected_control_Source_freeze_pin','selected_post_release_Common_Source_freeze_pin','selected_post_release_Common_Source_pin']:
 assert hf[key]==plan[key]and table[hf[key]['path']]==hf[key]
for key in ['selected_completed_first_SRC_bundle_lifetime_Source_plan_pin','independent_Host_Source_review_pin','independent_Host_Source_true_tool_return_pin','actual_failed_public5_summary_pin','actual_failed_public5_true_tool_return_pin','actual_exact_release_receipt_pin','actual_exact_release_true_tool_return_pin','actual_independent_postrelease_review_pin','actual_independent_postrelease_true_tool_return_pin']:
 q=hf[key];assert table[q['path']]==q
assert lifep==plan['completed_first_SRC_bundle_lifetime_Source_plan_pin']
assert life['logical_controls']==7 and life['phases']==9 and life['total_guarded_stages']==11 and life['maximum_live_synthetic_context_bundles']==1
assert life['exact_retirement_case']=='public_read_stale_BQ_SRC'and life['exact_bundle_relative_path']=='public_read_stale_BQ_SRC/coherent_complete_context.xsm'
assert life['exact_expected_read_status']==1 and life['exact_expected_control_calls']==1 and life['exact_expected_baseline_calls']==0
for key in ['intent_parent_entry_fsync_before_unlink','exact_APFS_creation_delta_nlink_plus1_size_plus32_and_times_monotonic','only_exact_new_owned_completed_SRC_bundle_unlink_authorized','only_retired_bundle_removed_from_current_owned_PFs','second_MAC_bundle_retained_current_through_final_report','original_manifest_sentinel_both_logs_current_and_unchanged','no_sparse_compression_move_threshold_or_generic_missing_skip','no_retries']:
 assert life[key]is True,key
assert life['future_actual_retirement_receipt_pin']is None and life['future_actual_public7_report_pin']is None
assert life['unchanged_public_Fortran_Source_freeze_pin']==hf['selected_control_Source_freeze_pin']
for q in [life['unchanged_Fortran_Source_pin'],life['unchanged_public_Fortran_Source_freeze_pin']]:assert table[q['path']]==q;read(q['path'],q)
for key in hf:
 if key.startswith('actual_future_'):assert hf[key]is None
assert hf['compiler_executed']is False and hf['numerical_executed']is False and hf['Host_imported_or_executed']is False
for key in ['compile_qualified','reader_qualified','old17_PASS_inherited','AAA_qualified','ABA_admitted']:assert hf[key]is False
assert template['required_new_build70_parameters']['sha256']is None and template['required_new_build70_parameters']['seven_id']is None and template['future_actual_control_report_pin']is None
assert template['host_source_pin']==hostp and template['host_freeze_pin']==hfp and template['Source_freeze_pin']==hf['selected_control_Source_freeze_pin']
env=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hostp['path']]
argv=cli['argv'];assert len(argv)==30 and argv[:12]==env
base,bp=load(plan['new_build_expected_report_path']);assert bp['sha256']=='74197904b3225f511408d609cb087db59ef963fe1162ec8b78c7751e2bdc307f'
bindings=[('new-build70',bp),('source-freeze',hf['selected_control_Source_freeze_pin']),('host-freeze',hfp)]
for ix,(name,q)in enumerate(bindings):
 k=12+6*ix;assert argv[k:k+4]==['--'+name+'-summary',q['path'],'--'+name+'-sha256',q['sha256']]
 assert argv[k+4]=='--'+name+'-seven-id'and json.loads(argv[k+5])==q['identity']
out=Path(hf['planned_output_root']);assert not out.exists()and not out.is_symlink()
text=hb.decode();assert "c.same_pin(__file__,hf['host_source'])"in text and "fixed=unique(fixed+[phf,hf['host_source'],plan_pin,psf,pbase,new_object]"in text
assert text.index("(OUT/('compact-'+KIND+'-controls')).mkdir()")<text.index('runner=full.OwnRSSSerialExecutor')
assert "owned.remove(before)"in text and "bundle_lifetime_status='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE'"in text and 'current_bundle_pin=None'in text
assert "bundle_lifetime_status='CURRENT_RETAINED_AFTER_COMPLETED_READ'"in text
caps=hf['original_caps'];assert caps==plan['original_caps']==base['original_caps']and hf['original_aux_cap_bytes']==134217728 and hf['original_pending_metadata_bytes']==8388608
model,modelp=load(R/'bq64_private_GANLIB_model_control_host_source_v5_20261013/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json');modelactual,modelactualp=load(Path(model['planned_output_root'])/'Root_actual_control_summary.json')
assert modelp['sha256']=='04d05551c688cee59e421a3f5e2cba9ff1a45905bd4333b1392c2ed60617c269'and modelactualp['sha256']=='a7724f8d8c9d334cd75a2c2e088269645385ef46d059af74ee9accff1c6b74f1'
for q in hf['dependencies']+[hfp,hostp,planp,lifep,templatep,clip,peerp,toolp,freezep,freezerp,bp,modelp,modelactualp]:current(q)
report=dict(schema='INDEPENDENT_PUBLIC7_FINAL_HF_ROOT_CLI_SOURCE_INTEGRATION_REVIEW_V1',status='PASS_PUBLIC7_FINAL_HF_ROOT_CLI_SOURCE_INTEGRATION_ONLY',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,Host_imported_or_executed=False,
 host_freeze_pin=hfp,CLI_pin=clip,Source_argv_template_pin=templatep,host_source_pin=hostp,plan_pin=planp,lifetime_Source_plan_pin=lifep,actual_Source_freeze_true_tools_pin=freezep,actual_Source_freeze_return=fr,preserved_actual_Source_freeze_first_failure=first,final_freezer_Source_pin=freezerp,
 genuine_child_Host_Source_review_pin=peerp,genuine_child_Host_Source_true_tools_pin=toolp,actual_child_Source_review_return=ar,selected_build_HF_pin=bhfp,selected_new_Fortran_Source_freeze_pin=hf['selected_new_Fortran_Source_freeze_pin'],selected_control_Source_freeze_pin=hf['selected_control_Source_freeze_pin'],selected_Common_Source_freeze_pin=hf['selected_post_release_Common_Source_freeze_pin'],
 current_HF_dependency_count=2629,all_current_dependency_all7_reobserved_before_and_after=True,original_build2532_all_rows_retained=True,selected_build2565_all_rows_retained=True,original_public5_2609_all_rows_retained=True,old_failed5_actual_evidence_and_independent_post0_retained=True,
 own_Host_topfield_samepin_then_all_stage_fixed_guard_verified=True,own_record_directory_creation_before_constructor_and_every_execute=True,exact_Root_actual_argv_count=30,exact_Root_external_bindings=[dict(role=x,pin=q)for x,q in bindings],environment_one_thread_nooptimize_B_verified=True,
 planned_output_root=str(out),planned_OUT_absent_at_review=True,all_future_actual_controls_and_retirement_receipt_PFs_None=True,original_caps=caps,original_aux_bytes=134217728,original_pending_bytes=8388608,
 only_exact_completed_new_SRC_bundle_lifetime_retirement_allowed=True,first_SRC_historical_afterread_PF_and_currentNone_MAC_current_contract=True,preunlink_intent_creation_APFS_and_dirfsync_requirements_bound=True,original_7_controls_9_phases_11_commands_Fortran_math_unchanged=True,
 model5_HF_pin_unchanged=modelp,model5_actual_report_pin_unchanged=modelactualp,independent_science_fullEOF_repeated=False,independent_finite_fixtures_repeated=False,all_file_descriptors_closed=True,production_reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,
 downstream_v15_existing_draft2_still_requires_exact_SRC_retirement_admission_Source_update=True,limitation='Source integration only. Root must run the new unique public7 controls; actual report and one genuine eligible retirement proof remain unknown. Existing v15 draft2 rejects retired historical SRC bundle as current and needs a separate exact Source change before pipeline qualification.')
D.mkdir(exist_ok=True);rp=D/'REVIEW.json';fd=os.open(rp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
try:
 b=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();assert os.write(fd,b)==len(b);os.fsync(fd)
finally:os.close(fd)
_,rv=read(rp);print(json.dumps(dict(status=report['status'],review_pin=rv,current_HF_dependency_count=2629,Root_actual_argv_count=30,business_executed=False,all_file_descriptors_closed=True)))

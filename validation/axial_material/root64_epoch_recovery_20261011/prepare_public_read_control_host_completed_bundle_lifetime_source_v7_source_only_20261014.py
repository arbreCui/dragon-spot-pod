#!/usr/bin/env python3
"""Source-only public v6 one-completed-SRC-bundle lifetime candidate; never runs or deletes."""
import ast,base64,copy,difflib,hashlib,json,os,stat
from pathlib import Path
REC=Path(__file__).resolve().parent
OLD=REC/'public_read_compact_bq_admission_control_host_source_v5_20261013'
NEW=REC/'public_read_compact_bq_admission_control_host_source_v7_20261014'
HELPER=REC/'public_read_v7_completed_SRC_bundle_retirement_helper_source_draft_v2_20261014.py'
FAIL=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/Root_actual_control_summary.json')
FAIL_TOOL=REC/'ROOT_ACTUAL_COMPACT_BQ_PUBLIC_V5_AUXILIARY128_FAILURE_TRUE_TOOL_RETURNS_20261013.json'
POST=REC/'independent_compact_BQ_public_v5_auxiliary128_failure_postverify_20261014/REVIEW.json'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 b=p.read_bytes();assert len(b)==s.st_size and ids(p.lstat())==ids(s)
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def read(p):
 b,pf=pin(p);return json.loads(b),pf
def put(name,value):
 b=value if isinstance(value,bytes)else(json.dumps(value,indent=2)+'\n').encode()
 p=NEW/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 try:assert os.write(fd,b)==len(b);os.fsync(fd)
 finally:os.close(fd)
 assert pin(p)[0]==b;return pin(p)[1]
def main():
 original,originalpf=pin(OLD/'run_guarded_public_controls.py');text=original.decode()
 oldplan,oldplanpf=read(OLD/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json')
 oldhf,oldhfpf=read(OLD/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')
 _,oldclipf=pin(OLD/'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json')
 helper,helperpf=pin(HELPER);ast.parse(helper)
 fail,failpf=read(FAIL);_,failtoolpf=pin(FAIL_TOOL);post,postpf=read(POST);_,posttoolpf=pin(POST.parent/'TRUE_TOOL_RETURNS.json')
 assert failpf['sha256']=='c60ae9b8eb0b410fd286e0b93e11dc110b029f69d5a3240b4b23184895d1652e'
 assert len(fail['records'])==10 and len(fail['actual_control_results'])==7 and len(fail['actual_stale_host_evidence'])==1
 assert '128MiB'in fail['failure']and fail['actual_seven_genuine_public_READ_controls_passed']is False
 assert len(oldplan['planned_run_phases'])==9 and oldplan['planned_total_guarded_stages']==11
 changes=[]
 def change(before,after,why):
  nonlocal text
  assert text.count(before)==1,why;text=text.replace(before,after,1);changes.append(dict(before=before,after=after,reason=why))
 change('axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5','axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7','new unique owned output only')
 change('def main():\n    parser=argparse.ArgumentParser()',helper.decode().rstrip()+'\n\n\ndef main():\n    parser=argparse.ArgumentParser()','exact first SRC bundle retirement implementation')
 change('first=FirstFailure();watches=[];actual=[];stale=[];after=None;verified=False',
        'first=FirstFailure();watches=[];actual=[];stale=[];retirements=[];after=None;verified=False','truthful bounded lifetime attempt evidence')
 change("                command=[exe,name]+([phase]if is_stale else[])",
        "                if name=='public_read_stale_BQ_MAC'and phase=='prepare':\n                    if len(retirements)!=1 or retirements[0]['retirement_completed']is not True or \\\n                       (OUT/'public_read_stale_BQ_SRC/coherent_complete_context.xsm').exists()or \\\n                       (OUT/'public_read_stale_BQ_SRC/coherent_complete_context.xsm').is_symlink():\n                        raise RuntimeError('exact first completed SRC bundle retirement before second MAC prepare')\n                command=[exe,name]+([phase]if is_stale else[])",
        'one bundle live at the actual second prepare boundary')
 change("state=dict(case=name,manifest_pin=c.pin(mf),bundle_pin=bundle_pin,stale_pin=stale_pin)",
        "state=dict(case=name,manifest_pin=c.pin(mf),bundle_pin=bundle_pin,stale_pin=stale_pin,actual_prepare_record=record)",
        'exact completed prepare record preserves original before manifest')
 before="""                    stale.append(dict(case=name,actual_before_manifest_pin=state['manifest_pin'],
                      actual_bundle_before_pin=state['bundle_pin'],actual_bundle_after_pin=c.pin(state['bundle_pin']['path']),
                      actual_stale_before_pin=state['stale_pin'],actual_stale_after_pin=c.pin(state['stale_pin']['path']),
                      actual_two_files_full_EOF_SHA_all7_unchanged=True,actual_other_BQ_absent=True,
                      genuine_read_child_closed0=True,actual_read_record=record))"""
 after="""                    proof=dict(case=name,actual_before_manifest_pin=state['manifest_pin'],
                      actual_bundle_before_pin=state['bundle_pin'],actual_bundle_after_pin=c.pin(state['bundle_pin']['path']),
                      actual_stale_before_pin=state['stale_pin'],actual_stale_after_pin=c.pin(state['stale_pin']['path']),
                      actual_two_files_full_EOF_SHA_all7_unchanged=True,actual_other_BQ_absent=True,
                      genuine_read_child_closed0=True,actual_read_record=record)
                    if name=='public_read_stale_BQ_SRC':
                        event=retire_completed_first_SRC_bundle(c,cwd,state,record,actual[-1],owned,fixed,retirements)
                        proof.update(bundle_lifetime_status='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE',
                          current_bundle_pin=None,actual_completed_bundle_retirement=event)
                    else:
                        proof.update(bundle_lifetime_status='CURRENT_RETAINED_AFTER_COMPLETED_READ',
                          current_bundle_pin=proof['actual_bundle_after_pin'])
                    stale.append(proof)"""
 change(before,after,'original full EOF before==after proof retained; sole SRC historical versus MAC current explicit')
 change("        if KIND=='public'and(len(actual)!=9 or len(stale)!=2):raise RuntimeError('seven public controls/nine phases/two independent stale manifests')",
        "        if KIND=='public'and(len(actual)!=9 or len(stale)!=2 or len(retirements)!=1 or retirements[0]['retirement_completed']is not True):\n            raise RuntimeError('seven public controls/nine phases/two independent stale manifests/one exact SRC bundle retirement')",
        'original complete seven/nine/eleven guard plus exactly one lifetime success')
 change('actual_watchdog_checks=watches,actual_control_results=actual,actual_stale_host_evidence=stale,',
        'actual_watchdog_checks=watches,actual_control_results=actual,actual_stale_host_evidence=stale,\n          actual_completed_bundle_retirements=retirements,',
        'truthful actual lifecycle attempt/raw receipt evidence even on later failure')
 ast.parse(text)
 back=text
 for block in reversed(changes):assert back.count(block['after'])==1;back=back.replace(block['after'],block['before'],1)
 assert back.encode()==original
 oldtree,newtree=ast.parse(original),ast.parse(text)
 def node_bytes(raw,tree,name):return ast.get_source_segment(raw,next(x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))and x.name==name))
 immutable=['safe_repr','FirstFailure','direct_aux_inventory','ControlsResources','log_rows','model_oracle','public_oracle','make_commands','load_common','rewrite_summary','unique']
 for name in immutable:assert node_bytes(original.decode(),oldtree,name)==node_bytes(text,newtree,name),name
 assert text.index("(OUT/('compact-'+KIND+'-controls')).mkdir()")<text.index('runner=full.OwnRSSSerialExecutor(')
 out='/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7';assert not Path(out).exists()
 NEW.mkdir(exist_ok=False);hostpf=put('run_guarded_public_controls.py',text.encode())
 plan=copy.deepcopy(oldplan);plan['host_source_pin']=hostpf;plan['planned_output_root']=out
 protocol=dict(schema='EXACT_PUBLIC_READ_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN_V1',
   source_only=True,logical_controls=7,phases=9,total_guarded_stages=11,
   unchanged_Fortran_Source_pin=plan['control_Source_pin'],unchanged_public_Fortran_Source_freeze_pin=plan['selected_control_Source_freeze_pin'],
   exact_retirement_case='public_read_stale_BQ_SRC',exact_bundle_leaf='coherent_complete_context.xsm',
   exact_bundle_relative_path='public_read_stale_BQ_SRC/coherent_complete_context.xsm',
   eligibility='closed prepare+read; original exact statuses/counters; beforeMF+bundle+sentinel fullEOF/all7 stable; otherBQ absent',
   exact_expected_read_status=1,exact_expected_control_calls=1,exact_expected_baseline_calls=0,
   fsynced_intent_before_single_attempt=True,intent_parent_entry_fsync_before_unlink=True,
   exact_APFS_creation_delta_nlink_plus1_size_plus32_and_times_monotonic=True,
   owned_directory_fd_NOFOLLOW_UID_singlelink_full_identity=True,
   only_exact_new_owned_completed_SRC_bundle_unlink_authorized=True,
   truthful_attempted_returned_unlink_parent_fsync_receipt_before_close_or_any_after_check=True,
   receipt_and_intent_retained_as_current_owned_metadata=True,only_retired_bundle_removed_from_current_owned_PFs=True,
   original_before_and_after_completed_read_PFs_retained_as_historical_time_facts=True,
   original_manifest_sentinel_both_logs_current_and_unchanged=True,
   second_MAC_bundle_retained_current_through_final_report=True,
   maximum_live_synthetic_context_bundles=1,original_aux_bytes=128*2**20,pending_bytes=8*2**20,
   no_sparse_compression_move_threshold_or_generic_missing_skip=True,no_retries=True,
   old_v5_output_unmodified=True,Fortran_math_old17_phase_oracle_flags_firsterror_unchanged=True,
   downstream_v15_only_SRC_exact_completed_retirement_proof_admission_required=True,
   future_actual_retirement_receipt_pin=None,future_actual_public7_report_pin=None,
   compiler_executed=False,numerical_executed=False,reader_qualified=False)
 protocolpf=put('EXACT_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN.json',protocol)
 plan['completed_first_SRC_bundle_lifetime_Source_plan_pin']=protocolpf
 planpf=put('EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json',plan)
 deltas={k:oldplan.get(k)for k in set(plan)|set(oldplan)if plan.get(k)!=oldplan.get(k)}
 restored=copy.deepcopy(plan)
 for k,v in deltas.items():
  if k in oldplan:restored[k]=v
  else:restored.pop(k)
 assert restored==oldplan
 inversepf=put('COMPLETE_PUBLIC_HOST_V5_TO_V7_LIFETIME_WHOLE_BYTE_DATA_INVERSE.json',dict(
   schema='COMPLETE_PUBLIC_READ_V5_TO_V7_LIFETIME_WHOLE_BYTE_DATA_INVERSE_V1',
   original_Host_pin=originalpf,new_Host_pin=hostpf,Host_exact_changes=changes,Host_whole_byte_inverse_observed=True,
   original_plan_pin=oldplanpf,new_plan_pin=planpf,exact_original_changed_plan_fields=deltas,plan_whole_canonical_data_inverse_observed=True,
   unchanged_11_functions_and_classes=immutable,Fortran_and_mathematical_source_changed=False,
   old_v5_failed_summary_pin=failpf,old_v5_failed_true_tool_pin=failtoolpf,
   old_v5_independent_failure_postverification_pin=postpf,old_v5_independent_failure_true_tool_pin=posttoolpf,
   old_v5_Host_freeze_pin=oldhfpf,old_v5_Source_argv_template_pin=oldclipf,
   no_import_compiler_publicRun_pipeline_or_deletion_by_preparation=True))
 ready=put('HOST_SOURCE_REVIEW_READY.json',dict(
   schema='COMPACT_BQ_PUBLIC7_LIFETIME_HOST_SOURCE_REVIEW_READY_V1',kind='public',source_only=True,
   compiler_executed=False,numerical_executed=False,Host_imported=False,files_deleted=False,
   host_source=hostpf,control_host_plan_pin=planpf,lifetime_Source_plan_pin=protocolpf,
   complete_Host_plan_inverse_pin=inversepf,private_retirement_helper_Source_pin=helperpf,
   predecessor_unfrozen_public6_Source_pin=pin(REC/'public_read_compact_bq_admission_control_host_source_v6_20261014/run_guarded_public_controls.py')[1],
   corrected_public6_parent_nlink_creation_gate_and_missing_preunlink_intent_directory_fsync=True,
   predecessor_Host_source_freeze_pin=oldhfpf,predecessor_argv_Source_template_pin=oldclipf,
   actual_failed_public5_summary_pin=failpf,actual_failed_public5_true_tool_return_pin=failtoolpf,
   actual_failed_public5_independent_postverification_pin=postpf,actual_failed_public5_independent_true_tool_pin=posttoolpf,
   future_Host_freeze_pin=None,future_actual_public7_report_pin=None,future_actual_retirement_receipt_pin=None,
   selected_Model5_Host_freeze_not_changed=True,reader_qualified=False,AAA_qualified=False))
 print(json.dumps({'status':'SOURCE_ONLY_PUBLIC7_EXACT_COMPLETED_FIRST_SRC_BUNDLE_LIFETIME_CANDIDATE_PREPARED',
   'host_source_pin':hostpf,'control_host_plan_pin':planpf,'lifetime_Source_plan_pin':protocolpf,
   'whole_inverse_pin':inversepf,'source_review_ready_pin':ready,
   'compiler_executed':False,'numerical_executed':False,'files_deleted':False,'old_v5_output_unmodified':True}))
if __name__=='__main__':main()

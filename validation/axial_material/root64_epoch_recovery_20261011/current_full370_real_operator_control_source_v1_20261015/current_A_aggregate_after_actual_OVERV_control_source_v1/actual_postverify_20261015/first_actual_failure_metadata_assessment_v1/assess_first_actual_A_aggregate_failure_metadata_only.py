"""Independent first actual Aagg failure facts; Source/report metadata and stat only."""
import hashlib,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parents[2]
OUT=Path(__file__).absolute().parent
START=time.monotonic();EOF=[]
ROOT_PIN=dict(path=str(BASE/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json'),sha256='f991c6a02048198b0d70d9c026fa98c778e7fdf2bb396095256c45ab6964dde3',size_bytes=6590,identity=[16777229,50547538,33188,1,6590,1792019326567392855,1792019326567392855])
HOST_PIN=dict(path='/Users/wen/spot/validation/artifacts/axial-material-current-A-full-aggregate-after-actual-OVERV-control-20261015-v1/Root_actual_current_A_aggregate_after_OVERV_control_summary.json',sha256='c6ae7431dc040cc2ba43912d358e1d3cd77c59958cf6d23f3c43837901b0ba27',size_bytes=2558613,identity=[16777229,50547526,33188,1,2558613,1792019310518324569,1792019310518324569])
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def budget():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(peak<512*2**20 and time.monotonic()-START<600,'own original SELF512/stage600')
def current(p):
 need(type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'exact Python integer PF')
 q=Path(p['path']);s=q.lstat();compiler=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==2
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ident(s)==p['identity']and(s.st_nlink==1 or compiler)and not any(a.is_symlink()for a in(q,*q.parents)),'current7 exact private file/original compiler2')
 return q
def ownpin(p):
 b=p.read_bytes();s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ident(s))
def full(p,parse=False):
 q=current(p);need(p['size_bytes']<8*2**20,'bounded Source/report/new-output metadata8MiB');fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();parts=[];n=0
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b);parts.append(b);budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'metadata wholeEOF SHA');current(p);EOF.append(p);raw=b''.join(parts)
 return json.loads(raw)if parse else raw

def digest_meta(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def main():
 root=full(ROOT_PIN,True);ret=root['actual_terminal_return']
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==1 and type(ret['exit_code'])is int and ret['exit_code']==1 and'session_id'not in ret and ret['chunk_id']=='ed099c'and root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine actual Root1 unchanged/no retry')
 for k in ['actual_LIGHT_return','actual_publication_return']:need(type(root[k]['exit_code'])is int and root[k]['exit_code']==0,'original Source publication/Light0 preserved separately')
 host=full(HOST_PIN,True);need(host['schema']=='ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_CONTROL_GUARDED_REPORT_V1'and host['status']=='FAILED_CURRENT_A_AGGREGATE_AFTER_OVERV_NO_RETRY'and host['current_source_gap_resolved']is False and host['failure']=="RuntimeError('preserve original FAILED record and actual evidence-only child2 with complete resource closure')"and host['secondary_failures']==[],'original failed Host exact facts')
 need(host['actual_child_receipt']is None and host['actual_evidence']is None and type(host['actual_child_evidence_only_integer_exit_code'])is int and host['actual_child_evidence_only_integer_exit_code']==1,'enumfield name does not change actual child1 to expected engineering2')
 need(host['final_report_resource_check_passed']is True and host['native_engines_started']==0 and host['original_runner_FAILED_record_not_reclassified']is True and host['old_report_issue1_retained']is True,'guard closure preserved; no computation success')
 sf=full(host['source_freeze_pin'],True);hf=full(host['host_freeze_pin'],True);plan=full(sf['control_plan_pin'],True)
 need(host['original_caps']==hf['original_caps']==plan['original_caps']==CAPS and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==63,'original complete63/caps untouched')
 out=Path(plan['planned_actual_output_root']);need(HOST_PIN['path']==str(out/'Root_actual_current_A_aggregate_after_OVERV_control_summary.json')and plan['complete_joint_roots'][-1]==str(out),'one owning newOUT63; no reset')
 need(plan['bounded_new_output_reservation_bytes']==320*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['host_summary_hard_bound_bytes']==6*2**20 and plan['execution_request_hard_bound_bytes']==4*2**20,'original unchanged bounds')
 need(len(host['records'])==len(host['actual_watchdog_checks'])==1,'one guarded child no retry')
 record=host['records'][0];need(record['status']=='FAILED'and record['error']=='own-child stage failed; no retry','original FAILED/error retained')
 wp=host['actual_watchdog_checks'][0]['actual_watchdog_pin'];watch=full(wp,True);need(watch==host['actual_watchdog_checks'][0]['actual_watchdog']and watch['command']==record['command'],'same original watchdog/command')
 need(type(watch['returncode'])is int and watch['returncode']==1 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512,'true child1/watch resources; no timeout/RSSkill claim')
 outputs={p['path']:p for p in host['complete_output_pins']};need(len(outputs)==len(host['complete_output_pins'])==5,'all five prior new outputs plus Host6')
 files={str(p)for p in out.rglob('*')if p.is_file()};need(files==set(outputs)|{HOST_PIN['path']}and len(files)==6,'exact six file scene only')
 for p in outputs.values():need(Path(p['path']).is_relative_to(out),'new output precise owner');full(p)
 lp=outputs[str(out/(record['label']+'.log'))];log=full(lp).decode('utf-8');need(log.splitlines()[-1]=='ValueError: output counted in fresh joint evidence'and "require(output in budget.roots,'output counted in fresh joint evidence')"in log,'underlying original pathgate failure before math')
 child_source=next(p for p in sf['complete_source_file_pins']if p['path'].endswith('/current_material_lineage_evidence.py'));text=full(child_source).decode('utf-8')
 gate="budget=Budget(request['joint_archive_roots']);require(output in budget.roots,'output counted in fresh joint evidence')"
 need(gate in text and text.index(gate)<text.index('source_table,fixed=source_admission(request,budget.check);output.mkdir()')<text.index('report=operation(request,output,budget,source_table)'),'Source proves gate before input admission/engine/context execution')
 requestpin=outputs[str(out/'ACTUAL_A_AGGREGATE_EXECUTION_REQUEST.json')];request=full(requestpin,True);need(request['joint_archive_roots']==plan['complete_joint_roots']and request['output_directory']==str(out/'evidence')and request['output_directory']not in request['joint_archive_roots']and str(out)in request['joint_archive_roots'],'precise parent-counted child-subdirectory mismatch; no numerical inference')
 need(not os.path.lexists(out/'evidence')and not any(p.endswith('/ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json')for p in files),'no child report/evidence directory/result created')
 stagespin=outputs[str(out/'evidence-stage/stages.json')];stages=full(stagespin,True);need(len(stages['stages'])==1 and stages['stages'][0]['status']=='FAILED'and stages['stages'][0]['error']=='own-child stage failed; no retry','original saved stageFAILED/error intact')
 need(plan['original_complete_A_input_count']==5937 and plan['current_live_historical_A_input_count']==5934 and len(plan['exact_retired_guard_only_input_pins'])==3,'correct historical5937/live5934 mapping; wrong zero-intersection draft not reused')
 historical=full(plan['historical_complete_input_request_pin'],True);prior=full(plan['original_A_aggregate_request_pin'],True)
 need(len(historical['complete_input_pins'])==5937 and len(prior['complete_input_pins'])==5934,'both original and corrected metadata requests preserved')
 retired=plan['exact_retired_guard_only_input_pins'];retiredpaths={p['path']for p in retired};need(all(not os.path.lexists(p['path'])for p in retired),'exact prior retired3 remain absent')
 histmap={p['path']:p for p in historical['complete_input_pins']};livemap={p['path']:p for p in prior['complete_input_pins']};need({k:v for k,v in histmap.items()if k not in retiredpaths}==livemap and all(histmap[p['path']]==p for p in retired),'only exact admitted historical guard3 removed from live metadata roles')
 reqmap={p['path']:p for p in request['complete_input_pins']};need(all(reqmap[p['path']]==p for p in prior['complete_input_pins']),'all live5934 old inputs retained exact fullPF descriptors')
 for p in prior['complete_input_pins']:current(p)
 binding=prior['aggregation_binding'];pairs=binding['actual_context_states']['A']['all_snapshot_pairs'];need(len(pairs)==8 and len(binding['actual_context_states']['A']['complete_context_pins'])==55,'all eight tree and55context input roles retained')
 for p in pairs:
  for k in ['input_pin','sqlite_pin','native_pool_pin']:current(p[k])
 for p in binding['actual_context_states']['A']['complete_context_pins']:current(p)
 for p in host['fixed_current_pins']+plan['inherited_metadata_current7_pins']:current(p)
 for snap in [host['resources_before'],host['resources_after'],host['resources_after_including_summary_bytes']]:
  need(snap['host_SELF_peak_bytes']<512*2**20 and 0<=snap['whole_elapsed_seconds']<1800 and snap['complete_joint']['artifact_bytes']+snap['explicit_external_metadata_bytes']+snap['host_open_unlinked_bytes']<2*2**30,'actual original host/63 cumulative resource closure')
  need(snap['original_history']['artifact_bytes']+20971764748+64*2**20<96*2**30 and snap['complete_joint']['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history/cold/free reservations')
 for k in ['physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','physical_neutron_balance_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete']:need(host[k]is False,'failure all qualification flagsfalse '+k)
 unique={p['path']:p for p in EOF}
 for p in unique.values():full(p)
 for p in host['fixed_current_pins']+plan['inherited_metadata_current7_pins']+prior['complete_input_pins']:current(p)
 need(all(not os.path.lexists(p['path'])for p in retired)and not os.path.lexists(out/'evidence'),'absence retained twice')
 report=dict(schema='INDEPENDENT_CURRENT_A_AGGREGATE_FIRST_ACTUAL_FAILURE_METADATA_ASSESSMENT_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,metadata_only=True,actual_Host_report_pin=HOST_PIN,actual_Root_true_tools_pin=ROOT_PIN,actual_Root_return=ret,actual_Root_integer_exit_code=1,actual_child_integer_exit_code=1,actual_child_evidence_only_integer_exit_code_field_is_unqualified1=True,expected_engineering_child2_not_achieved=True,actual_original_runner_record=record,actual_original_watchdog=watch,actual_child_log_pin=lp,actual_child_log_final_line=log.splitlines()[-1],underlying_failure_before_source_admission_or_math_proved_from_Source=True,actual_child_report_present=False,actual_evidence_directory_present=False,actual_source_gap_resolved=False,actual_comparison_counts_unknown_no_results=True,actual_first_failure_preserved=True,original_Source_publication_and_Light0_separate_from_actualRoot1=True,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_failed_complete_output_pins=list(outputs.values())+[HOST_PIN],actual_new_output_count=6,new_outputs_blindEOF_SHA_current7_verified_twice=True,Source_metadata_fullEOF_current7_twice_pins=list(unique.values()),Source_metadata_fullEOF_count=len(unique),current_live_historical_input_count=5934,historical_input_count=5937,exact_historical_retired_guard_only_input_pins=retired,original_eight_tree_and55context_inputs_current7_only=True,original14earlierSQL_pool_inputs_retained=True,old_SCI_GENDF_XSM_SQL_pool_scientific_bodies_opened=False,old_scientific_body_SHA_recomputed=False,old_JSONL_or_array_payloads_opened=False,fixed_current7_role_count=len(host['fixed_current_pins']),fixed_current7_descriptor_sha256=digest_meta(host['fixed_current_pins']),fixed_roles_reference='Immutable failed Host fixed_current_pins fullPF list',complete_joint_roots=plan['complete_joint_roots'],original_caps=CAPS,actual_final_report_resource_check_passed=True,actual_resources_after_including_summary_bytes=host['resources_after_including_summary_bytes'],reviewer_source_pin=ownpin(Path(__file__).absolute()),worker_or_original_helpers_imported=False,retirement_or_business_repeated=False,business_executed=False,numerical_executed=False,compiler_executed=False,PS_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024),wall_seconds=time.monotonic()-START)
 target=OUT/'REVIEW.json';need(not target.exists(),'independent failurefacts once');raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'report8MiB')
 with target.open('xb')as f:f.write(raw)
 print(json.dumps(dict(status=report['status'],review_pin=ownpin(target))),flush=True)
if __name__=='__main__':main()

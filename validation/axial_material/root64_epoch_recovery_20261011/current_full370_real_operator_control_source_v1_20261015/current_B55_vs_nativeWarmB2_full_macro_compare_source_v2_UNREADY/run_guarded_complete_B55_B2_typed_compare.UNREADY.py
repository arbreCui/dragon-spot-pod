"""Root sole owning host for complete B55 versus B2 typed word comparison; evidence child2 remains FAILED."""
import argparse,hashlib,importlib.util,json,os,shutil,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent

def main():
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args()
 with(BASE/'ROOT_B55_B2_COMPARISON_ONCE_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_CURRENT_B55_B2_COMPARISON_EXCLUSIVE_ONCE_CLAIM_V1',PID=os.getpid(),original_started=started,argv=sys.argv,claim_before_project_import_and_payload_IO=True,retries=0),f);f.write('\n');f.flush();os.fsync(f.fileno())
 def freeze(role):
  k=role.replace('-','_');seven=json.loads(getattr(a,k+'_seven_id'));q=Path(getattr(a,k+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(a,k+'_sha256'),size_bytes=seven[4],identity=seven);raw=q.read_bytes()
  if len(raw)>=8*2**20 or[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=seven or hashlib.sha256(raw).hexdigest()!=p['sha256']:raise RuntimeError('exact bounded Source/host freeze')
  return json.loads(raw),p
 sf,psf=freeze('source-freeze');hf,phf=freeze('host-freeze');pc=hf['contract_Source_pin'];q=Path(pc['path'])
 if q!=BASE/'B55_B2_compare_Source_contract.UNREADY.py'or hashlib.sha256(q.read_bytes()).hexdigest()!=pc['sha256']:raise RuntimeError('whole exact local contract Source')
 spec=importlib.util.spec_from_file_location('B2_Root_owning_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current(pc)
 m.need(sf['schema']=='COMPLETE_CURRENT_B55_B2_TYPED_COMPARISON_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False and hf['schema']=='CURRENT_B55_B2_COMPLETE_COMPARISON_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==m.CAPS,'exact reviewed Source and owning host freeze')
 packet=m.metadata(sf['control_plan_pin']);build,bm,extractplan,extraction,post=m.admit(packet)
 peer=m.metadata(hf['independent_Source_review_pin']);m.genuine(m.metadata(hf['independent_Source_review_tools_pin']),'actual_review_return',hf['independent_Source_review_pin'],'review_pin')
 m.need(peer['status']=='PASS_SOURCE_ONLY_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON'and peer['failure']is None and peer['source_only']is True and peer['control_plan_pin']==sf['control_plan_pin']and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'same full Source independent review0')
 c=m.source(packet['original_Common_Source_pin'],'B2_Root_original_common');support=m.source(packet['original_support_Source_pin'],'B2_Root_original_support');m.source(packet['original_production_inputs_Source_pin'],'production_inputs')
 m.need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and Path(sys.executable).resolve()==support.PYTHON and all(os.environ.get(k)=='1'for k in c.THREADS),'original exact interpreter/thread1/unoptimized/unprofiled')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B2_Root_original_guard_helper');full,production=helper.modules();guard_files=helper.guard_admission(full)
 m.need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unchanged original private OwnRSS and SerialExecutor class/MRO/origins')
 resources=m.Resources(packet,build,bm,hf['explicit_cumulative_metadata_file_pins']+[psf,phf,pc,sf['control_plan_pin']],started,1800);before=resources.check();reservation=m.admit_reservation(packet,before)
 def check_all():
  for p in sf['complete_source_file_pins']:m.need(m.pin(p['path'])==p,'whole Source through owning runtime')
  for p in packet['retained_current7_pins']+packet['retained_B2_current_epoch_readonly_pins']:m.current(p)
  return resources.check()
 check_all();m.OUT.mkdir();(m.OUT/'runtime').mkdir();(m.OUT/'compare-stage').mkdir();(m.OUT/'evidence').mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');bounded=m.pin(m.OUT/'runtime/run_bounded_dragon.py');m.need(bounded['sha256']==packet['original_bounded_Source_pin']['sha256'],'whole original owned bounded Source')
 rb=dict(source_freeze_pin=psf,host_freeze_pin=phf,parent_PID=os.getpid(),original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,owned_bounded_pin=bounded)
 request=dict(schema='CURRENT_B55_TO_NATIVEWARM_B2_COMPLETE_TYPED_WORD_COMPARISON_REQUEST_V1',owning_host_output_directory=str(m.OUT),child_output_directory=str(m.OUT/'evidence'),root_owning_runtime_Source_binding=rb)
 for k in('actual_current_epoch_B2_archive_pin','observed_B55_pair','native_B2_pair','actual_B2_complete_extraction_report_pin','actual_B2_complete_extraction_post_pin','actual_latest_complete_prefix_plan_pin','actual_B2_lineage_metadata_audit_pin'):request[k]=packet[k]
 request_path=m.OUT/'ACTUAL_B55_B2_COMPLETE_COMPARISON_EXECUTION_REQUEST.json';m.write(request_path,request);preq=m.pin(request_path)
 child=BASE/'run_complete_B55_B2_typed_comparison_child.UNREADY.py';command=[str(support.PYTHON),'-B',str(child),'--request-pin',json.dumps(preq,separators=(',',':')),'--contract-source-pin',json.dumps(pc,separators=(',',':')),'--expected-parent-pid',str(os.getpid())]
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-started),'compare-stage',resources);m.need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','one genuine unchanged owning runner and exact bounded Source')
 first=None;secondary=[];original_error=None;receipt=None;watch=None;wp=None;lp=None;after=None;good=False;childreport=None
 try:
  check_all()
  try:runner.execute(m.OUT/'compare-stage','complete_B55_nativeWarm_B2_typed_word_compare',command,600)
  except RuntimeError as e:original_error=str(e)
  m.need(len(runner.records)==1,'one child only; no retry');record=runner.records[0];wp=m.pin(m.OUT/(record['label']+'.watchdog.json'));lp=m.pin(m.OUT/(record['label']+'.log'));watch=m.metadata(wp)
  m.need(original_error=='own-child stage failed; no retry'and record['status']=='FAILED'and record['error']==original_error and type(watch['returncode'])is int and watch['returncode']==2 and watch['command']==command and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'intentional complete typed comparison child2 remains original FAILED/error with real private guard closure')
  lines=Path(lp['path']).read_text().splitlines();m.need(len(lines)==1,'one complete child receipt');receipt=json.loads(lines[0]);m.need(receipt['status']=='ACTUAL_COMPLETE_B55_NATIVEWARM_B2_COMPARISON_EVIDENCE_ONLY_EXIT2','complete typed comparison evidence receipt only');childreport=receipt['report_pin'];m.need(Path(childreport['path'])==m.OUT/'evidence/ACTUAL_B55_NATIVEWARM_B2_COMPLETE_TYPED_MACRO_COMPARISON_REPORT.json','exact owning complete comparison child report path');v=m.metadata(childreport)
  m.need(v['schema']=='ACTUAL_B55_NATIVEWARM_B2_FULL_TYPED_PATH_RAW_WORD_COMPARISON_V1'and v['status']=='ACTUAL_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_ONLY'and v['observed_B55_pair']==packet['observed_B55_pair']and v['native_B2_pair']==packet['native_B2_pair']and v['compared_all_macro_records']==19620 and v['path_sets_equal']is True and v['all_original_records_and_typed_root_preserved']is True and v['original_archive_not_redecoded']is True and v['constructed_19249_field_subset_used']is False,'complete exact19620 bidirectional typed root/all words, no reconstructed field subset or repeat decoder')
  m.need(type(v['compared_original_payload_words'])is int and v['compared_original_payload_words']>0 and type(v['raw_word_mismatches'])is int and v['raw_word_mismatches']>=0 and type(v['metadata_mismatches'])is int and v['metadata_mismatches']>=0,'actual complete comparison counts recorded without changing thresholds or inventing zero mismatches')
  m.need(Path(v['detail_pin']['path'])==m.OUT/'evidence/B55_nativeWarmB2_complete_canonical_macro_comparison.jsonl','one complete canonical typed comparison detail file retained');m.current(v['detail_pin'])
  m.need(receipt['actual_parent_PID']==os.getpid()and receipt['resources_after']['current_parent_PID']==os.getpid()and receipt['resources_after']['actual_PS_return']['returncode']==0,'actual child direct owning ancestry and same-PID PS guard evidence')
  after=check_all();good=True
 except BaseException as e:first=e
 finally:
  if runner.records and watch is None:
   try:
    record=runner.records[-1];q=m.OUT/(record['label']+'.watchdog.json')
    if q.exists():wp=m.pin(q);watch=m.metadata(wp)
    q=m.OUT/(record['label']+'.log')
    if q.exists():lp=m.pin(q)
   except BaseException as e:secondary.append(repr(e))
  try:after=check_all()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_GUARDED_ROOT_REPORT_V1',status='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_CHILD2_CLOSED_ONLY'if good and first is None else'FAILED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,records=runner.records,original_runner_error=original_error,actual_child_integer_exit_code=None if watch is None else watch['returncode'],actual_intentional_exit2_normal_closure=good and first is None,actual_child_receipt=receipt,actual_child_resources_after=None if receipt is None else receipt.get('resources_after'),actual_child_report_pin=childreport,actual_watchdog_full_pin=wp,actual_watchdog=watch,actual_log_full_pin=lp,source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=sf['control_plan_pin'],actual_execution_request_pin=preq,actual_current_epoch_B2_archive_pin=packet['actual_current_epoch_B2_archive_pin'],actual_B2_complete_extraction_report_pin=packet['actual_B2_complete_extraction_report_pin'],actual_B2_complete_extraction_post_pin=packet['actual_B2_complete_extraction_post_pin'],complete_typed_word_comparison_completed=good and first is None,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=m.CAPS,complete_joint_roots=packet['complete_joint_roots'],actual_stage_reservation=reservation,resources_before=before,resources_after=after,final_report_resource_check_passed=False,B2_archive_redecoded=False,**m.FALSE)
  q=m.OUT/'Root_actual_current_B55_nativeWarm_B2_complete_comparison_summary.json';m.write(q,report)
  try:
   resources.check();report['final_report_resource_check_passed']=True
   with q.open('w')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
   resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
 if first is not None:raise first
 print(json.dumps(dict(status=report['status'],report_pin=m.pin(q),actual_child_evidence_only_integer_exit_code=2,original_runner_FAILED_record_preserved=True,**m.FALSE)),flush=True)
if __name__=='__main__':main()

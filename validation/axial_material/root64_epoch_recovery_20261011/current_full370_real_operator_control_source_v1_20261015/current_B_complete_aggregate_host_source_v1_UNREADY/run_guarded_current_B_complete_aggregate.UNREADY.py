"""UNREADY Root owning complete B six-phase aggregation. Intentional child2 remains FAILED."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def frozen_arg(a,role):
 n=role.replace('-','_');ids=json.loads(getattr(a,n+'_seven_id'));q=Path(getattr(a,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=ids[4],identity=ids)
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==ids and s.st_size<8*2**20,'exact freeze current7')
 raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'whole freeze SHA');return json.loads(raw),p
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();start=time.monotonic()
 with(BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_CURRENT_B_COMPLETE_AGGREGATE_CLAIM_V1',Root_PID=os.getpid(),original_monotonic_start=start,argv=sys.argv,claim_before_metadata_EOF_import_or_decoder=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 sf,psf=frozen_arg(a,'source-freeze');hf,phf=frozen_arg(a,'host-freeze');cp=hf['contract_Source_pin']
 need(Path(cp['path'])==BASE/'aggregate_Source_contract.UNREADY.py'and hashlib.sha256(Path(cp['path']).read_bytes()).hexdigest()==cp['sha256'],'exact author-frozen extract contract')
 spec=importlib.util.spec_from_file_location('owning_B_aggregate_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current(cp)
 need(sf['schema']=='COMPLETE_CURRENT_B_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False and hf['schema']=='CURRENT_B_COMPLETE_AGGREGATE_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==m.CAPS,'exact aggregate-only Source/host publication')
 packet=m.metadata(sf['control_plan_pin']);build,bm,manifest,binding,state,extraction,extraction_post=m.admit(packet)
 c=m.source(packet['original_Common_Source_pin'],'B_aggregate_original_common');support=m.source(packet['original_support_Source_pin'],'B_aggregate_original_support');m.source(packet['original_production_inputs_Source_pin'],'production_inputs')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original exact Python and one-thread environment')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B_aggregate_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'B_aggregate_original_resource_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unaltered private original OwnRSS/SerialExecutor Source and MRO')
 roots=packet['complete_joint_roots'];joined=production.DiskResources(m.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800,'original hostSELF512/whole1800 from initial exclusive claim')
   h=history.check();j=joined.check();own=0
   if m.OUT.exists():
    for q in m.OUT.rglob('*'):
     s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no output alias')
     if stat.S_ISREG(s.st_mode):own+=s.st_size
   need(own<m.OUTPUT_BOUND,'all complete extraction SQL/pool/JSONL/context/report/runtime/log/watch/request under320MiB')
   need(sum(q.stat().st_size for q in BASE.rglob('*')if q.is_file())<m.SOURCE_BOUND,'Source/metadata16MiB')
   extra=0
   for p in hf['explicit_cumulative_metadata_file_pins']:
    bm.current_metadata_role(p,build)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:s=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged joint2/history96/cold/meta/free8 including external metadata and open-unlinked')
   return dict(original_history=h,complete_joint=j,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),entire_aggregate_output_bytes=own,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();reservation=m.admit_aggregate_only_stage(packet,binding,before)
 request_builder=m.source(next(p for p in sf['complete_source_file_pins']if Path(p['path']).name=='build_current_B_complete_aggregate_request.UNREADY.py'),'B_aggregate_request_constructor')
 worker_inputs=m.live_worker_inputs(packet,state,extraction_post,sf['complete_source_file_pins'])
 fixed=m.unique(worker_inputs+[packet['current_B_case_input_binding_pin'],packet['actual_observation_manifest_pin'],binding['current_case_spec_pin'],binding['original_v10_seed_plan_pin'],packet['original_production_inputs_Source_pin'],packet['original_Common_Source_pin'],packet['original_support_Source_pin'],packet['original_bounded_Source_pin'],packet['original_guard_build_contract_Source_pin'],psf,phf,cp,sf['control_plan_pin']]+[c.pin(q)for q in guard_files+[support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT]]);owned=[]
 def check_all():
  for p in fixed:m.current(p);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  for p in packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
  return resources.check()
 check_all();m.OUT.mkdir();(m.OUT/'runtime').mkdir();(m.OUT/'evidence').mkdir();(m.OUT/'evidence-stage').mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');bounded=c.pin(m.OUT/'runtime/run_bounded_dragon.py');need(bounded['sha256']==packet['original_bounded_Source_pin']['sha256'],'whole unchanged original bounded Source');owned.append(bounded)
 coverage=m.coverage(packet,state,extraction_post);coverage_path=m.OUT/'ACTUAL_COMPLETE_B_SNAPSHOT_COVERAGE_FOR_AGGREGATION.json';m.write(coverage_path,coverage);coverage_pin=c.pin(coverage_path);owned.append(coverage_pin)
 request_inputs=dict(actual_B_manifest=manifest,actual_B_input_binding=binding,actual_B_extraction_post=extraction_post,actual_B_extraction_report=extraction,complete_source_freeze_pin=psf,operation_owning_output_root=str(m.OUT),complete_joint_roots=roots,latest_complete_plan=m.metadata(packet['latest_complete_plan_pin']),latest_complete_plan_pin=packet['latest_complete_plan_pin'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'],actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],actual_B_extraction_report_pin=packet['actual_B_extraction_report_pin'],actual_B_extraction_Host_report_pin=packet['actual_B_extraction_Host_report_pin'],actual_B_extraction_post_pin=packet['actual_B_extraction_post_pin'],actual_extraction_coverage_contract_pin=coverage_pin,exact_B4_product_lifecycle_binding=packet['exact_B4_product_lifecycle_binding'],current_B55_OVERV_control_binding=packet['current_B55_OVERV_control_binding'],stage_reservation_binding=reservation,complete_fixed_pins=worker_inputs,explicit_cumulative_metadata_file_pins=packet['child_ordinary_explicit_metadata_pins'])
 request,checked_coverage=request_builder.build(request_inputs);need(checked_coverage==coverage,'same complete Root-reviewed actual B coverage, no synthetic pair or omitted context')
 request_path=m.OUT/'ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EXECUTION_REQUEST.json';m.write(request_path,request);pr=c.pin(request_path);owned.append(pr)
 child=BASE/'current_B_material_lineage_evidence.UNREADY.py';command=[str(support.PYTHON),'-B',str(child),'aggregate','--request-pin',json.dumps(pr,separators=(',',':')),'--output-dir',request['output_directory'],'--expected-parent-pid',str(os.getpid())]
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'evidence-stage',resources)
 need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','original private runner/owned bounded Source')
 first=None;secondary=[];original_error=None;receipt=None;watch=None;wp=None;lp=None;after=None;good=False;child_report=None
 try:
  check_all()
  try:runner.execute(m.OUT/'evidence-stage','complete_B_aggregate',command,600)
  except RuntimeError as e:original_error=str(e)
  need(len(runner.records)==1,'one actual decoder child only, no retry')
  record=runner.records[0];watch_path=m.OUT/(record['label']+'.watchdog.json');log_path=m.OUT/(record['label']+'.log');wp=c.pin(watch_path);lp=c.pin(log_path);watch=m.metadata(wp)
  need(original_error=='own-child stage failed; no retry'and record['status']=='FAILED'and record['error']==original_error and type(watch['returncode'])is int and watch['returncode']==2 and watch['command']==command and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'preserve genuine evidence child2 and original FAILED/error with complete normal original resource closure')
  lines=log_path.read_text().splitlines();need(len(lines)==1,'one complete child receipt, no omitted warnings or traceback');receipt=json.loads(lines[0]);need(receipt['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2','actual full six-phase aggregate evidence receipt only')
  child_report=receipt['report'];need(Path(child_report['path'])==m.OUT/'evidence/aggregate/ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json','exact fresh complete aggregate report role');c.same_pin(child_report['path'],child_report);v=m.metadata(child_report)
  need(v['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and v['status']=='ACTUAL_CURRENT_COMPLETE_ORIGINAL_MATH_CONSTRUCTION_EVIDENCE_ONLY_EXIT2'and v['error']is None and v['state_order']==['B']and len(v['states'])==1 and v['states'][0]['state']=='B'and v['current_B_case_input_binding_pin']==packet['current_B_case_input_binding_pin']and v['all_complete_state_scope_retained']is True,'all original complete current B construction evidence, not a copied A aggregate')
  facts=v['states'][0];phases=facts['phase_results']
  need(facts['original_context_event_count']==55 and facts['all_original_snapshot_count']==8 and [p['phase']for p in phases]==['scattering','scalar','fission','extras','overv_fallback','metadata']and all(p['computation_finished']is True for p in phases)and type(facts['complete_source_field_comparisons'])is int and facts['complete_source_field_comparisons']>0 and facts['all_mismatching_elements']==facts['all_context_or_operand_issues']==facts['unknown_macro_producers']==0,'all original B fields and six phases complete with actual comparison counts and zero mismatch/unknown/issues; no A count or prior B issue1 invented')
  admitted=v['current_OVERV_control_admission'];need(admitted==facts['current_OVERV_control_admission']and admitted['schema']=='CURRENT_B55_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1'and admitted['prior_B_aggregate_executed']is False and admitted['prior_B_issue_count']is None and admitted['issue_count_adjustment_performed']is False and admitted['control_metadata_pins']==packet['current_B55_OVERV_control_binding']['metadata_pins'],'same genuine B55 current control is consumed without historical count subtraction')
  for k in('reaction_multiplicity_qualified','physical_neutron_balance_qualified','coupled_370group_reference_qualified','scientific_accuracy_qualified','goal_complete'):need(receipt[k]is False and v[k]is False,'complete construction evidence cannot mint physical or goal qualification')
  need(v['complete_final_construction_qualified']is False and v['new_aggregation_qualification_sha256']is None and v['actual_scientific_qualification_sha256']is None,'engineering evidence only, no final physical qualification')
  after=check_all();good=True
 except BaseException as e:first=e
 finally:
  if runner.records and watch is None:
   try:
    record=runner.records[-1];q=m.OUT/(record['label']+'.watchdog.json')
    if q.exists():wp=c.pin(q);watch=m.metadata(wp)
    q=m.OUT/(record['label']+'.log')
    if q.exists():lp=c.pin(q)
   except BaseException as e:secondary.append(dict(where='failed-stage monitor metadata',error=repr(e)))
  try:after=check_all()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_GUARDED_ROOT_REPORT_V1',status='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EVIDENCE_CHILD2_CLOSED_ONLY'if good and first is None else'FAILED_CURRENT_B_COMPLETE_AGGREGATE_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,operation='aggregate',records=runner.records,original_runner_error=original_error,actual_child_integer_exit_code=None if watch is None else watch['returncode'],actual_intentional_exit2_normal_closure=good and first is None,actual_complete_child_receipt=receipt,actual_child_report_pin=child_report,actual_watchdog_full_pin=wp,actual_watchdog=watch,actual_log_full_pin=lp,source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=sf['control_plan_pin'],actual_execution_request_pin=pr,actual_capture_Host_report_pin=packet['actual_capture_Host_report_pin'],actual_B_extraction_report_pin=packet['actual_B_extraction_report_pin'],actual_B_extraction_post_pin=packet['actual_B_extraction_post_pin'],actual_B55_control_binding=packet['current_B55_OVERV_control_binding'],actual_B4_lifecycle_binding=packet['exact_B4_product_lifecycle_binding'],actual_coverage_contract_pin=coverage_pin,current_source_control_bound=good and first is None,B_six_phase_construction_completed=good and first is None,prior_B_aggregate_executed=False,prior_B_issue_count=None,issue_count_adjustment_performed=False,actual_observation_manifest_pin=packet['actual_observation_manifest_pin'],current_B_case_input_binding_pin=packet['current_B_case_input_binding_pin'],original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=m.CAPS,complete_joint_roots=roots,actual_aggregate_only_stage_reservation=reservation,resources_before=before,resources_after=after,fixed_current_pins=fixed,final_report_resource_check_passed=False,**m.FALSE)
  q=m.OUT/'Root_actual_current_B_complete_aggregate_summary.json';m.write(q,report)
  try:
   resources.check();report['final_report_resource_check_passed']=True
   with q.open('w')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
   resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
 if first is not None:raise first
 print(json.dumps(dict(status=report['status'],report_pin=c.pin(q),actual_child_evidence_only_integer_exit_code=2,original_runner_FAILED_record_preserved=True,**m.FALSE)),flush=True)
if __name__=='__main__':main()

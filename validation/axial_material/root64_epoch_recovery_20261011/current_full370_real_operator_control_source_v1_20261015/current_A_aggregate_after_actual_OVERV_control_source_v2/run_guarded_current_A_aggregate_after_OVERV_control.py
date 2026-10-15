"""Original OwnRSS guard reused for complete A aggregation after actual OVERV control."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,struct,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS={'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'fresh_bytes': 2147483648, 'history_bytes': 103079215104, 'cold_reserve_bytes': 20971764748, 'metadata_reserve_bytes': 67108864, 'free_floor_bytes': 8589934592, 'threads': 1, 'children_at_once': 1, 'retries': 0}
FALSE={'original_evaluation_neutron_yield_branch_captured':False,'MF6_GENDF_label_proves_original_processing_branch':False,'MT5_partition_qualified':False,'fission_producer_replayed':False,'reaction_exclusive_partition_qualified':False,'finite18_replayed':False,'temperature_interpolation_replayed':False,'scientific_accuracy_qualified':False,'unreduced_reference_qualified':False,'historical_whole_ASCII_file_reconstruction_qualified':False,'whole_original_NJOY_build_reproduced':False,'current_SPH_MASK_context_applied':False,'physical_neutron_balance_qualified':False,'physics_qualified': False, 'historical_machine_bit_replay': False, 'historical_native_RAM_bits_verified': False, 'original_XSM_memory_bits_verified': False, 'complete_reaction_authority_qualified': False, 'full_reference_qualified': False, 'formal_H150_NZ48_full_controls_qualified': False, 'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False}
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
 q=Path(p['path']);s=q.lstat();compiler=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==2 and s.st_nlink==2
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or compiler)and identity(s)==p['identity'],'exactcurrent7, sole original compiler two-link role')
 return s
def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m
def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v


def rewrite_summary(c,path,previous,data):
    require(len((json.dumps(data,indent=2,allow_nan=False)+'\n').encode())<6*2**20,'own replay host summary6MiB hard bound')
    if previous['identity'][3] != 1 or previous['path'] != str(path):
        raise RuntimeError('only owning single-link summary can be rewritten')
    c.same_pin(path,previous)
    fd = os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] != previous['identity']:
            raise RuntimeError('owned summary opened7ID changed')
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            fd = None
            stream.seek(0)
            stream.truncate(0)
            json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if fd is not None:
            os.close(fd)
    if c.identity(path)[:4] != previous['identity'][:4]:
        raise RuntimeError('own summary physical role changed')

def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:
            raise RuntimeError('inconsistent complete PF for same input path')
        table[row['path']]=row
    return list(table.values())

def safe_repr(error):
    try:return repr(error)
    except BaseException:return '<exception repr unavailable>'

class FirstFailure:
    def __init__(self):
        self.error=None;self.traceback=None;self.secondary=[]
    def capture(self,error,where):
        if self.error is None:
            self.error=error;self.traceback=error.__traceback__
        else:self.secondary.append(dict(where=where,error=safe_repr(error)))
    def reraise(self):
        if self.error is not None:raise self.error.with_traceback(self.traceback)

def compact_resources(value):
 result={k:v for k,v in value.items()if k not in('original_history','complete_joint')}
 for role in('original_history','complete_joint'):
  original=value[role];selected={k:v for k,v in original.items()if k not in('resource_roots','declared_resource_roots','resource_scope_contract')}
  for key in('resource_roots','declared_resource_roots','resource_scope_contract'):
   if key in original:
    selected[key+'_sha256']=hashlib.sha256(json.dumps(original[key],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    if isinstance(original[key],(list,dict)):selected[key+'_count']=len(original[key])
  result[role]=selected
 return result
def compact_record(value):
 result=dict(value)
 for key in('resource_before','resource_after'):
  if isinstance(result.get(key),dict):result[key]=compact_resources(result[key])
 return result
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 args=ap.parse_args();start=time.monotonic()
 claim=BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json'
 with claim.open('x')as stream:json.dump(dict(schema='ROOT_EXCLUSIVE_CURRENT_A_AGGREGATE_AFTER_OVERV_EXECUTION_CLAIM_V1',Root_PID=os.getpid(),original_monotonic_start=start,argv=sys.argv,claim_before_metadata_fullEOF_or_business=True,Root_required_exec_command_sandbox_permissions='require_escalated',original_caps=CAPS),stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
 def argument(role):
  n=role.replace('-','_');q=Path(getattr(args,n+'_summary'));ids=json.loads(getattr(args,n+'_seven_id'));p=dict(path=str(q),sha256=getattr(args,n+'_sha256'),size_bytes=ids[4],identity=ids);return metadata(p),p
 sf,psf=argument('source-freeze');hf,phf=argument('host-freeze')
 require(sf['schema']=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='CURRENT_A_AGGREGATE_AFTER_ACTUAL_OVERV_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==CAPS,'exact new complete Source-only package/original guard host')
 plan=metadata(sf['control_plan_pin']);out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh current A aggregation output, no retry')
 c=source_module(plan['original_Common_Source_pin'],'current_A_aggregate_original_common');support=source_module(plan['original_support_Source_pin'],'current_A_aggregate_original_support')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original interpreter/unoptimized/unprofiled/single thread')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'current_A_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'current_A_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original actual OwnRSS class/MRO')
 roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))==64 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete inherited63 prefix plus one whole owning output64')
 joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure).check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation')
 retirement=metadata(plan['actual_literal3_ASCII_retirement_receipt_pin'])
 require(retirement['schema']=='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL3_COMPLETED_A_ASCII_EXPORTS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==346861973 and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==3 and retirement['all14_earlier_SQL_pool_files_retained']is True and retirement['original_A_aggregate_issue1_preserved']is True,'real literal3 lifecycle retirement; hold every earlier SQL/pool')
 retired={p['path']:p for p in retirement['actual_released_pins']}
 for p in retired.values():require(not os.path.lexists(p['path']),'only exact completed ASCII role remains absent')
 prior_request=metadata(plan['original_A_aggregate_request_pin'])
 historical_inputs=prior_request['complete_input_pins'];inputs=[];retired_inputs=[]
 for p in historical_inputs:
  if p['path']in retired:require(p==retired[p['path']],'exact historical fullPF equals genuinely released guard role');retired_inputs.append(p)
  else:inputs.append(p)
 require(len(historical_inputs)==5937 and len(inputs)==5934 and len(retired_inputs)==3,'all5937 historical =5934 live+exact3 retired guard inputs')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-start<1800,'original whole1800/hostSELF512')
   h=history.check();f=joined.check();own_bytes=sum(p.lstat().st_size for p in out.rglob('*')if p.is_file())if out.exists()else 0;require(own_bytes<plan['bounded_new_output_reservation_bytes'],'entire current A output below320MiB hard bound')
   require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/free8 reservations')
   extra=0
   for p in hf['explicit_cumulative_metadata_file_pins']:
    current7(p)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   unlinked={}
   for fd in os.listdir('/dev/fd'):
    try:s=os.fstat(int(fd))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   require(f['artifact_bytes']+extra+sum(unlinked.values())<2*2**30,'original cumulative2GiB including external metadata/open-unlinked');return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();require(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']+plan['bounded_new_output_reservation_bytes']<2*2**30,'whole original cumulative2GiB preserves full320MiB output reservation')
 fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+sf['complete_source_file_pins']+inputs+[c.pin(p)for p in guard_files]);owned=[]
 for p in plan['inherited_metadata_current7_pins']:current7(p)
 for p in fixed:current7(p);c.same_pin(p['path'],p)
 out.mkdir();runtime=out/'runtime';runtime.mkdir();stage=out/'evidence-stage';stage.mkdir();childout=out/'evidence'
 shutil.copy2(support.BOUNDED,runtime/'run_bounded_dragon.py');owned.append(c.pin(runtime/'run_bounded_dragon.py'));require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copied')
 role_proof=dict(receipt=plan['actual_literal3_ASCII_retirement_receipt_pin'],tools=plan['actual_literal3_ASCII_retirement_true_tools_pin'],post=plan['actual_literal3_ASCII_retirement_post0_pin'],post_tools=plan['actual_literal3_ASCII_retirement_post0_true_tools_pin'])
 historical_reference=dict(original_request_full_pin=plan['original_A_aggregate_request_pin'],original_member='complete_input_pins',ordered_fullPF_count=5937,ordered_fullPF_canonical_sha256=hashlib.sha256(json.dumps(historical_inputs,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest())
 request=dict(prior_request,complete_source_freeze_pin=psf,complete_input_pins=unique(inputs+[psf]+list(plan['current_OVERV_control_binding']['metadata_pins'].values())+list(role_proof.values())),historical_complete_input_pins=historical_reference,historical_complete_input_request_pin=plan['original_A_aggregate_request_pin'],exact_retired_input_pins=retired_inputs,current_live_historical_input_count=5934,retired_guard_input_admission_pins=role_proof,owning_host_output_directory=str(out),output_directory=str(childout),joint_archive_roots=roots,current_OVERV_control_binding=plan['current_OVERV_control_binding'],inherited_prior_request_pin=plan['original_A_aggregate_request_pin'],actual_literal3_ASCII_retirement_receipt_pin=plan['actual_literal3_ASCII_retirement_receipt_pin'])
 request_path=out/'ACTUAL_A_AGGREGATE_EXECUTION_REQUEST.json';require(len((json.dumps(request,indent=2,allow_nan=False)+'\n').encode())<4*2**20,'complete live plus exact original historical reference request4MiB hard bound');c.write(request_path,request);prequest=c.pin(request_path);owned.append(prequest)
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'evidence-stage',resources);require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==runtime/'run_bounded_dragon.py','same actual original owning runner and bounded Source')
 first=FirstFailure();watches=[];after=None;verified=False;receipt=result=None
 def check_all():
  for p in plan['inherited_metadata_current7_pins']:current7(p)
  for p in fixed:current7(p);c.same_pin(p['path'],p)
  for p in owned:current7(p);c.same_pin(p['path'],p)
  for p in retired.values():require(not os.path.lexists(p['path']),'precise released role stays absent')
  return resources.check()
 try:
  check_all();cmd=[str(support.PYTHON),'-B',str(BASE/'current_material_lineage_evidence.py'),'aggregate','--request-pin',json.dumps(prequest,separators=(',',':')),'--output-dir',str(childout),'--expected-parent-pid',str(os.getpid())]
  original_error=None
  try:runner.execute(stage,'complete_A_aggregate_after_OVERV_control',cmd,600)
  except RuntimeError as error:original_error=str(error)
  require(len(runner.records)==1,'one original owning child; no retry')
  record=runner.records[0];watchpath=out/(record['label']+'.watchdog.json');log=out/(record['label']+'.log');watch=metadata(c.pin(watchpath));watches.append(dict(actual_watchdog_pin=c.pin(watchpath),actual_watchdog=watch))
  require(original_error=='own-child stage failed; no retry'and record['status']=='FAILED'and type(watch['returncode'])is int and watch['returncode']==2 and watch['limit_failure']is None and watch['command']==cmd and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512,'preserve original FAILED record and actual evidence-only child2 with complete resource closure')
  check_all();lines=log.read_text().splitlines();require(len(lines)==1,'one complete original child receipt')
  receipt=json.loads(lines[0]);require(receipt['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2','actual original evidence completion only')
  pchild=receipt['report'];c.same_pin(pchild['path'],pchild);result=metadata(pchild)
  require(Path(pchild['path']).parent==childout and result['state_order']==['A']and result['all_complete_state_scope_retained']is True and result['error']is None and len(result['states'])==1,'exact full current A mathematical report')
  facts=result['states'][0]
  require(facts['complete_source_field_comparisons']==19249 and facts['original_context_event_count']==55 and facts['all_original_snapshot_count']==8 and facts['all_mismatching_elements']==0 and facts['all_context_or_operand_issues']==0 and facts['unknown_macro_producers']==0 and len(facts['phase_results'])==6 and all(p['computation_finished']is True for p in facts['phase_results'])and result['current_OVERV_control_admission']['original_issue_fact']['category']=='SOURCE_CONTEXT_NOT_SAVED'and result['current_OVERV_control_admission']['issue_count_adjustment_performed']is False,'all original full A phases and comparisons complete, resolved actual control evidence only; no arithmetic qualification')
  require(all(result[k]is False for k in('reaction_multiplicity_qualified','physical_neutron_balance_qualified','coupled_370group_reference_qualified','scientific_accuracy_qualified','goal_complete')),'no physical or broader reaction acceptance')
  verified=True
 except BaseException as error:first.capture(error,'actual_full_A_aggregation_or_report')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_current_A_aggregate_after_OVERV_control_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_CONTROL_GUARDED_REPORT_V1',status='ACTUAL_CURRENT_A_FULL_MATH_CONTROL_EVIDENCE_EXIT2_CLOSED_ONLY'if good else'FAILED_CURRENT_A_AGGREGATE_AFTER_OVERV_NO_RETRY',current_source_gap_resolved=good,failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=[compact_record(r)for r in runner.records],actual_watchdog_checks=watches,fixed_current_pins=fixed,complete_output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_child_receipt=receipt,actual_evidence=result,actual_child_evidence_only_integer_exit_code=None if not watches else watches[0]['actual_watchdog']['returncode'],original_runner_FAILED_record_not_reclassified=True,source_freeze_pin=psf,host_freeze_pin=phf,actual_literal3_ASCII_retirement_receipt_pin=plan['actual_literal3_ASCII_retirement_receipt_pin'],resources_before=compact_resources(before),resources_after=None if after is None else compact_resources(after),original_guard_MRO_unchanged=True,original_caps=CAPS,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,native_engines_started=0,old_report_issue1_retained=True,**FALSE)
  require(len((json.dumps(summary,indent=2,allow_nan=False)+'\n').encode())<6*2**20,'owning aggregate host summary6MiB hard bound');c.write(target,summary);summary['resources_after_including_summary_bytes']=compact_resources(check_all());summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:summary.update(status='FAILED_CURRENT_A_AGGREGATE_AFTER_OVERV_NO_RETRY',current_source_gap_resolved=False,failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'actual complete current A evidence only');print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

"""Original one-child OwnRSS guard around saved MT5 NX producer control only."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';BASE=Path(__file__).absolute().parent
FALSE=dict(complete_reaction_authority_qualified=False,DRAGR_complete_packed_kernel_replayed=False,finite_dilution_NX_replayed=False,current_SPH_MASK_context_applied=False,physics_qualified=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def metadata(p):
 q=Path(p['path']);s=q.lstat();require(identity(s)==p['identity']and stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in(q,*q.parents)),'exact ordinary metadata current7')
 raw=q.read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256']and identity(q.lstat())==p['identity'],'whole metadata bytes/current7');return json.loads(raw)
def load_source(p,name):
 metadata_bytes=Path(p['path']).read_bytes();require(hashlib.sha256(metadata_bytes).hexdigest()==p['sha256']and identity(Path(p['path']).lstat())==p['identity'],'whole exact original guard Source')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def rewrite_summary(c,path,previous,data):
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

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();start=time.monotonic()
 def arg(role):
  n=role.replace('-','_');p=Path(getattr(a,n+'_summary'));value=dict(path=str(p),sha256=getattr(a,n+'_sha256'),identity=json.loads(getattr(a,n+'_seven_id')),size_bytes=p.stat().st_size);return metadata(value),value
 sf,psf=arg('source-freeze');hf,phf=arg('host-freeze')
 require(sf['schema']=='SAVED_MT5_NX_RAW32_YIELD_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='SAVED_MT5_NX_RAW32_YIELD_HOST_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute()),'exact Source-only MT5 host')
 plan=metadata(sf['control_plan_pin']);require(plan['source_only']is True and plan['original_caps']==hf['original_caps']and len(plan['complete_joint_roots'])==36,'complete prior34 plus corrected NX Source/owning output, no reset')
 c=load_source(plan['original_Common_Source_pin'],'NX_original_common');support=load_source(plan['original_support_Source_pin'],'NX_original_support')
 require(Path(sys.executable).resolve()==support.PYTHON and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original Python/unoptimized/unprofiled/single-thread environment')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'NX_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'NX_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine original OwnRSS class/MRO')
 out=Path(plan['planned_actual_output_root']);require(out.parent==c.ART and not os.path.lexists(out),'fresh single output namespace')
 roots=plan['complete_joint_roots'];joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure).check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original complete-family fullfresh2/cold/meta history96 reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-start<1800,'original SELF512/whole1800')
   h=history.check();f=joined.check();extra=0
   require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original cold/history96/free8 reserves')
   for p in plan['explicit_cumulative_metadata_file_pins']:
    require(identity(Path(p['path']).lstat())==p['identity'],'explicit metadata current7')
    if not any(Path(p['path']).is_relative_to(Path(v))for v in roots):extra+=p['size_bytes']
   require(f['artifact_bytes']+extra<2*2**30,'unchanged cumulative root2GiB plus exact external metadata')
   return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,complete_joint_bytes=f['artifact_bytes']+extra,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files])
 for p in fixed:c.same_pin(p['path'],p)
 out.mkdir();(out/'runtime').mkdir();(out/'NX-control').mkdir();shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
 require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copied')
 binding=dict(schema='SAVED_MT5_NX_RAW32_YIELD_EXECUTION_BINDING_V1',source_freeze_pin=psf,complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],original_caps=plan['original_caps'],output_directory=str(out/'diagnostic'),SCI1_whole_PF_verified_by_original_parent_before_child=True,**FALSE)
 bindingpath=out/'ACTUAL_SAVED_MT5_NX_RAW32_YIELD_BINDING.json';c.write(bindingpath,binding);pb=c.pin(bindingpath);owned.append(pb)
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'NX-control',resources);require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources,'original actual owning guard')
 first=FirstFailure();watchpin=logpin=childpin=None;after=None;verified=False
 def check_all():
  for p in fixed:
   if p in (plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_context_only_pin']):require(identity(Path(p['path']).lstat())==p['identity'],'original SCI exactcurrent7 after parent fullEOF/selected-leaf checks')
   else:c.same_pin(p['path'],p)
  for p in owned:c.same_pin(p['path'],p)
  return resources.check()
 try:
  check_all();runner.execute(out/'NX-control','saved_MT5_NX_raw32_yield',[str(support.PYTHON),sf['child_source_pin']['path'],'--binding-pin',json.dumps(pb,separators=(',',':')),'--expected-parent-pid',str(os.getpid())],600)
  require(len(runner.records)==1,'one original actual child, no retry');record=runner.records[0];watchpin=c.pin(out/(record['label']+'.watchdog.json'));logpin=c.pin(out/(record['label']+'.log'));watch=metadata(watchpin)
  require(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['sampled_peak_rss_mib']<512,'genuine child0/noLimit/originalcaps')
  lines=Path(logpin['path']).read_text().splitlines();require(len(lines)==1,'one exact complete child receipt');receipt=json.loads(lines[0]);require(receipt['status']=='ALL_ORIGINAL_NX_PRODUCER_RAW32_EQUAL','actual all-temperature NX producer pass only');childpin=receipt['report'];value=metadata(childpin)
  require(value['schema']=='ACTUAL_SAVED_MT5_NX_RAW32_PRODUCER_REPLAY_AND_YIELD_DIAGNOSTIC_V1'and value['actual_NX_producer_all_temperature_replay_passed']is True and value['compared_unique_nuclides']==11 and value['compared_temperature_records']==79 and value['complete_reaction_authority_qualified']is False,'all eleven and every real SCI temperature, no scientific promotion');after=check_all();verified=True
 except BaseException as e:first.capture(e,'control_or_close')
 try:after=check_all()
 except BaseException as e:first.capture(e,'after_check')
 good=verified and first.error is None;target=out/'Root_actual_saved_MT5_NX_raw32_yield_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_ROOT_GUARDED_SAVED_MT5_NX_RAW32_YIELD_DIAGNOSTIC_V1',status='ACTUAL_SAVED_MT5_NX_PRODUCER_REPLAY_CHILD0_CLOSED_ONLY'if good else'ACTUAL_SAVED_MT5_NX_PRODUCER_FAILED_NO_RETRY',failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=runner.records,actual_watchdog_full_pin=watchpin,actual_log_full_pin=logpin,actual_child_report_pin=childpin,fixed_current_pins=fixed,complete_output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],resources_before=before,resources_after=after,original_guard_class_MRO_unchanged=True,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as e:
  first.capture(e,'publication')
  if summary is not None and target.exists():
   try:summary.update(status='ACTUAL_SAVED_MT5_NX_PRODUCER_FAILED_NO_RETRY',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'complete original NX producer replay only');print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

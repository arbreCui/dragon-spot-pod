"""Original serial guard: actual full370 library origin and two component suites only."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS={'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'fresh_bytes': 2147483648, 'history_bytes': 103079215104, 'cold_reserve_bytes': 20971764748, 'metadata_reserve_bytes': 67108864, 'free_floor_bytes': 8589934592, 'threads': 1, 'children_at_once': 1, 'retries': 0}
FALSE={'physics_qualified': False, 'historical_machine_bit_replay': False, 'historical_native_RAM_bits_verified': False, 'original_XSM_memory_bits_verified': False, 'complete_reaction_authority_qualified': False, 'full_reference_qualified': False, 'formal_H150_NZ48_full_controls_qualified': False, 'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False}
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
 q=Path(p['path']);s=q.lstat();system_tool=q==Path('/usr/bin/clang++')and s.st_uid==0 and s.st_nlink>=1 and bool(s.st_mode&0o111);require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and((s.st_uid==os.getuid()and s.st_nlink==1)or system_tool)and identity(s)==p['identity'],'literal ordinary frozen current7 with exact preexisting compiler tool role');return s
def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m
def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v


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
 args=ap.parse_args();start=time.monotonic()
 def argument(role):
  n=role.replace('-','_');q=Path(getattr(args,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(args,n+'_sha256'),size_bytes=s.st_size,identity=json.loads(getattr(args,n+'_seven_id')));return metadata(p),p
 sf,psf=argument('source-freeze');hf,phf=argument('host-freeze')
 require(sf['schema']=='COMPLETE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='COMPLETE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['selected_source_freeze_pin']==psf,'exact Source-only package')
 require(hf['host_source_pin']['path']==str(Path(__file__).absolute())and sf['original_caps']==CAPS and hf['original_caps']==CAPS,'exact host/unchanged original caps')
 plan=metadata(sf['control_plan_pin']);out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh single control namespace, zero retry')
 c=source_module(plan['original_Common_Source_pin'],'full370_kernel_original_common')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original unoptimized/unprofiled single-thread host')
 support=source_module(plan['original_support_Source_pin'],'full370_kernel_original_support')
 require(Path(sys.executable).resolve()==support.PYTHON,'exact original Python')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'full370_kernel_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'full370_kernel_original_resource_factory')
 full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine original OwnRSS class and MRO')
 for p in hf['dependencies']:
  current7(p)
  if p not in plan['scientific_input_current7_pins']:c.same_pin(p['path'],p)
 roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'all retained disjoint stage roots')
 joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30)
 history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 allfamily=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=allfamily.check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'genuine complete-family fullfresh2/cold/meta reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
   require(peak<512*2**20 and time.monotonic()-start<1800,'original whole1800 and host SELF512')
   h=history.check();f=joined.check();require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original cold/history96/free8 reserves')
   extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current7(p)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   require(f['artifact_bytes']+extra<2*2**30,'same cumulative joint2GiB including exact external metadata')
   return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files]);owned=[]
 out.mkdir();(out/'runtime').mkdir();(out/'component').mkdir();(out/'kernel-component').mkdir()
 shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned.append(c.pin(out/'runtime/run_bounded_dragon.py'))
 require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copy')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'kernel-component',resources)
 require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py','original owning runner binding')
 first=FirstFailure();watches=[];after=None;actual=None;verified=False
 def check_all():
  for p in fixed:
   current7(p)
   if p not in plan['scientific_input_current7_pins']:c.same_pin(p['path'],p)
  for p in owned:current7(p);c.same_pin(p['path'],p)
  return resources.check()
 def run(label,command):
  check_all();runner.execute(out/'component',label,command,600);watches.append(helper.check_watch(out,runner.records[-1]));check_all();return runner.records[-1]
 receipt=metadata(sf['actual_retirement_receipt_pin'])
 require(Path(sf['actual_retirement_receipt_pin']['path']).parent==Path(plan['required_retirement_directory']),'only exact retirement receipt directory')
 def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
 require(all(contains(receipt,p)and not os.path.lexists(p['path'])for p in plan['exact_four_retired_intermediate_pins']),'only four literal closed intermediary retirements')
 for p in plan['exact_retained_native_archive_pins']:current7(p)
 command=[str(support.PYTHON),'-B',plan['worker_source_pin']['path'],'--plan-pin',json.dumps(sf['control_plan_pin'],separators=(',',':')),'--report',str(out/'component/ONE_ACTUAL_TRACK_COMPONENT_REPORT.json'),'--expected-parent-pid',str(os.getpid())]
 try:
  run('one_actual_track',command);rp=c.pin(out/'component/ONE_ACTUAL_TRACK_COMPONENT_REPORT.json');owned.append(rp);result=metadata(rp)
  require(result['passed']is True and result['groups']==370 and result['retained_moments']==9 and result['nz']==48 and result['H']==150. and result['offset_order']==32 and result['actual_tracks_executed']==1 and result['actual_actions_executed']==16 and result['formal_H150_NZ48_full_controls_qualified']is False,'precise one complete actual track/all16 original actions full-dimension component scope')
  require(len(runner.records)==1 and runner.records[0]['status']=='PASS','one original guarded child PASS')
  actual=dict(actual_component_report_pin=rp,all_one_stage_PASS=True,actual_kernel_origin_pin=plan['actual_kernel_origin_pin'],actual_kernel_library_pin=plan['actual_kernel_library_pin'],all370_white_and_nine_moment_transport_compared=True,**FALSE);verified=True
 except BaseException as error:first.capture(error,'execute_or_component_report')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_one_actual_track_component_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_ONE_REAL_TRACK_COMPONENT_GUARDED_REPORT_V1',status='ACTUAL_ONE_REAL_TRACK_FULL_DIMENSION_COMPONENT_CLOSED0_ONLY'if good else'ACTUAL_ONE_REAL_TRACK_COMPONENT_FAILED_UNQUALIFIED',failure=None if first.error is None else safe_repr(first.error),after_check_error=None,secondary_failures=first.secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_control_results=actual,actual_compile_command=command,original_guard_MRO_unchanged=True,original_caps=CAPS,resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,component_only=True,actual_track_scope='one original complete track/all16 actions;H150NZ48;370groups;9moments;offset32',formal_H150_NZ48_11364tracks_181824actions_controls_executed=False,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()

 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:
    summary.update(status='ACTUAL_ONE_REAL_TRACK_COMPONENT_FAILED_UNQUALIFIED',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'complete current guarded components only')
 print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),origin_pin=plan['actual_kernel_origin_pin'],library_pin=plan['actual_kernel_library_pin'],**FALSE)),flush=True)
if __name__=='__main__':main()

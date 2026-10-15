"""Original unchanged OwnRSS guard for one four-original-ASCII streaming child."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,struct,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS={'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'fresh_bytes': 2147483648, 'history_bytes': 103079215104, 'cold_reserve_bytes': 20971764748, 'metadata_reserve_bytes': 67108864, 'free_floor_bytes': 8589934592, 'threads': 1, 'children_at_once': 1, 'retries': 0}
FALSE={'scientific_accuracy_qualified':False,'unreduced_reference_qualified':False,'historical_whole_ASCII_file_reconstruction_qualified':False,'whole_original_NJOY_build_reproduced':False,'current_SPH_MASK_context_applied':False,'physical_neutron_balance_qualified':False,'physics_qualified': False, 'historical_machine_bit_replay': False, 'historical_native_RAM_bits_verified': False, 'original_XSM_memory_bits_verified': False, 'complete_reaction_authority_qualified': False, 'full_reference_qualified': False, 'formal_H150_NZ48_full_controls_qualified': False, 'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False}
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
 require(sf['schema']=='FOUR_ORIGINAL_ASCII_GENDF_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='FOUR_ORIGINAL_ASCII_GENDF_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and sf['original_caps']==CAPS and hf['original_caps']==CAPS,'exact same-round Source-only package/host/original caps')
 plan=metadata(sf['control_plan_pin']);require(all(p in hf['explicit_cumulative_metadata_file_pins']for p in plan['explicit_cumulative_metadata_file_pins']),'complete original metadata retained plus same-round proof files');out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh control namespace; no retry')
 c=source_module(plan['original_Common_Source_pin'],'four_ascii_original_common');support=source_module(plan['original_support_Source_pin'],'four_ascii_original_support')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original interpreter/unoptimized/unprofiled/single thread')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'four_ascii_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'four_ascii_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original actual OwnRSS class/MRO')
 roots=plan['complete_joint_roots'];require(len(roots)==44 and len(set(roots))==44 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete prior43 preserved plus new originalASCII output v2')
 joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure).check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-start<1800,'original whole1800/hostSELF512')
   h=history.check();f=joined.check();require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/free8 reservations')
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
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files]);owned=[]
 for p in fixed:current7(p);c.same_pin(p['path'],p)
 retirement=metadata(hf['actual_precise_retirement_receipt_pin']);require(hf['actual_precise_retirement_receipt_pin']==plan['actual_precise_retirement_receipt_pin']and retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==405417320 and len(retirement['actual_released_pins'])==4 and retirement['actual_released_pins']==retirement['exact_target_pins'],'exact real four completed spool retirement')
 for p in retirement['actual_released_pins']:require(not os.path.lexists(p['path']),'retired spool remains absent, history retained')
 out.mkdir();runtime=out/'runtime';runtime.mkdir();stage=out/'gendf-stage';stage.mkdir();inventories=out/'inventories';inventories.mkdir()
 shutil.copy2(support.BOUNDED,runtime/'run_bounded_dragon.py');owned.append(c.pin(runtime/'run_bounded_dragon.py'));require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copied')
 binding=out/'ACTUAL_FOUR_ORIGINAL_ASCII_EXECUTION_BINDING.json';small=[p for p in fixed if p['path'].endswith('.json')and p['size_bytes']<8*2**20]
 c.write(binding,dict(schema='FOUR_ORIGINAL_ASCII_GENDF_EXECUTION_BINDING_V1',control_plan_pin=sf['control_plan_pin'],source_freeze_pin=psf,complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=hf['explicit_cumulative_metadata_file_pins'],output_directory=str(inventories),fixed_small_metadata_pins=small,original_caps=CAPS,**FALSE));pb=c.pin(binding);owned.append(pb)
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources);require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources,'same actual original owning runner')
 first=FirstFailure();watches=[];after=None;verified=False;receipt=result=None
 def check_all():
  for row in plan['inputs']:current7(row['gzip_primary_current_full_pin'])
  for p in fixed:current7(p);c.same_pin(p['path'],p)
  for p in owned:current7(p);c.same_pin(p['path'],p)
  for p in retirement['actual_released_pins']:require(not os.path.lexists(p['path']),'precise released role stays absent')
  return resources.check()
 try:
  check_all();cmd=[str(support.PYTHON),'-B',str(BASE/'stream_four_original_ascii_gendf.py'),'--binding-pin',json.dumps(pb,separators=(',',':')),'--expected-parent-pid',str(os.getpid())]
  runner.execute(stage,'four_original_ASCII_fullEOF_inventory',cmd,600);watches.append(helper.check_watch(out,runner.records[-1]));check_all()
  require(len(runner.records)==1 and runner.records[0]['status']=='PASS','one original owning child closed0, no retry');log=out/(runner.records[0]['label']+'.log');lines=log.read_text().splitlines();require(len(lines)==1,'one complete actual child receipt');receipt=json.loads(lines[0]);require(receipt['status']=='ACTUAL_ALL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY','actual whole4 completion')
  pchild=receipt['report_pin'];c.same_pin(pchild['path'],pchild);result=metadata(pchild);require(Path(pchild['path']).parent==inventories and result['execution_binding_pin']==pb and len(result['actual_extractions'])==4 and all(result[k]is False for k in ('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete')),'exact four originalASCII report origin, evidence only')
  require(sum(r['actual_decompressed_bytes']for r in result['actual_extractions'])==plan['original_decompressed_payload_expected_bytes']and all(r['MF1_grids']==8 for r in result['actual_extractions']),'complete4 originalASCII bytes and all8 grids');verified=True
 except BaseException as error:first.capture(error,'actual_streaming_child_or_report')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_four_original_ASCII_GENDF_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_GUARDED_REPORT_V1',status='ACTUAL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY'if good else'FAILED_FOUR_ORIGINAL_ASCII_NO_RETRY',failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,complete_output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_child_receipt=receipt,actual_evidence=result,source_freeze_pin=psf,host_freeze_pin=phf,actual_precise_retirement_receipt_pin=hf['actual_precise_retirement_receipt_pin'],resources_before=before,resources_after=after,original_guard_MRO_unchanged=True,original_caps=CAPS,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,native_engines_started=0,original_ASCII_files_written=0,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:summary.update(status='FAILED_FOUR_ORIGINAL_ASCII_NO_RETRY',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'actual complete originalASCII evidence only');print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()

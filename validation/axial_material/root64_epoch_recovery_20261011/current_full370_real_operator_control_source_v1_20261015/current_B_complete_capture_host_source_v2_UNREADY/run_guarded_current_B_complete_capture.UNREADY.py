"""UNREADY owning Root host. Sole native B child under whole original OwnRSS guard."""
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
 claim=BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json'
 with claim.open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_CURRENT_B_NATIVE_CAPTURE_CLAIM_V1',Root_PID=os.getpid(),output_root='/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003/A/b63',original_monotonic_start=start,argv=sys.argv,claim_before_metadata_EOF_import_or_native=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 sf,psf=frozen_arg(a,'source-freeze');hf,phf=frozen_arg(a,'host-freeze');cp=hf['contract_Source_pin']
 need(Path(cp['path'])==BASE/'capture_Source_contract.UNREADY.py'and hashlib.sha256(Path(cp['path']).read_bytes()).hexdigest()==cp['sha256'],'exact frozen author contract')
 spec=importlib.util.spec_from_file_location('owning_B_capture_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current(cp)
 need(sf['schema']=='CURRENT_B_COMPLETE_CAPTURE_SOURCE_FREEZE_V1'and hf['schema']=='CURRENT_B_COMPLETE_CAPTURE_HOST_FREEZE_V1'and sf['source_only']is True and sf['native_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==m.CAPS,'exact Source-only publication pair')
 packet=m.metadata(sf['control_plan_pin']);build,bm=m.admit(packet)
 c=m.source(packet['original_Common_Source_pin'],'current_B_original_common');support=m.source(packet['original_support_Source_pin'],'current_B_original_support')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original exact Python and one-thread guard environment')
 m.source(packet['original_production_inputs_Source_pin'],'production_inputs')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'current_B_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'current_B_original_resource_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unaltered original OwnRSS class/PID/MRO')
 roots=packet['complete_joint_roots'];joined=production.DiskResources(m.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800,'original hostSELF512/whole1800 from initial claim')
   h=history.check();j=joined.check();own=0
   if m.OUT.exists():
    for q in m.OUT.rglob('*'):
     s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no native-output alias')
     if stat.S_ISREG(s.st_mode):own+=s.st_size
   need(own<m.CAPTURE_BOUND,'all native four exports/55contexts/8trees/CLE caches/log/watch/report640MiB')
   source=sum(q.stat().st_size for q in BASE.rglob('*')if q.is_file());need(source<m.SOURCE_BOUND,'Source/metadata16MiB')
   extra=0
   for p in hf['explicit_cumulative_metadata_file_pins']:
    bm.current_metadata_role(p,build)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:s=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged joint2/history96/cold/meta/free8 including external metadata/open-unlinked')
   return dict(original_history=h,complete_joint=j,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),entire_capture_output_bytes=own,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();prospective=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes'];need(prospective+m.CAPTURE_BOUND+m.SOURCE_BOUND<2*2**30,'complete current prefix+full capture640MiB+Source16MiB before native; no forecast fit assumed')
 fixed=m.unique(sf['complete_source_file_pins']+[psf,phf,cp,sf['control_plan_pin'],packet['new_IO_runtime_pin'],packet['original_v10_seed_plan_pin'],packet['original_production_inputs_Source_pin']]+[r['input_pin']for r in packet['original_B_native_stage_inputs']]+list(packet['actual_consumed_readonly_cwd_role_pins'].values())+[c.pin(q)for q in guard_files]);owned=[]
 def check_all():
  for p in fixed:m.current(p);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  for p in packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
  return resources.check()
 def checked_fullpin(path,budget):
  budget();p=c.pin(path);budget();return p
 def checked_recheck(p,budget):
  budget();m.current(p);c.same_pin(p['path'],p);budget()
 check_all();route=m.source(next(p for p in sf['complete_source_file_pins']if Path(p['path']).name=='B_original_input_binding.UNREADY.py'),'current_B_capture_route');oldcwd=route.snapshot_old_cwd_current7()
 need(oldcwd==packet['all_old_cwd_entries_current7_before_child'],'all original SCI-cwd names current7 freshly bound before output mkdir')
 m.OUT.mkdir();(m.OUT/'runtime').mkdir();(m.OUT/'native').mkdir();(m.OUT/'B_capture').mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');bounded=c.pin(m.OUT/'runtime/run_bounded_dragon.py');need(bounded['sha256']==packet['original_bounded_Source_pin']['sha256'],'whole original bounded Source, no guard edit');owned.append(bounded)
 binding=dict(packet['B_binding_template'],entry_mode='Root',actual_Root_PID=os.getpid(),business_admission_complete=True,new_IO_build_and_publication_closed0=True,exclusive_Root_claim_pin=c.pin(claim),original_OwnRSS_Source_pin=c.pin(support.FULL),original_SerialExecutor_Source_pin=c.pin(support.PARENT),owned_original_bounded_Source_pin=bounded,execution_Source_pins=sf['complete_source_file_pins'],prospective_existing_joint_bytes=prospective,complete_latest_prefix_roots=roots[:-1],context_tree_extraction_reserve_bytes=m.CAPTURE_BOUND-423456221,new_build_reserve_bytes=0,new_IO_runtime_pin=packet['new_IO_runtime_pin'],all_old_cwd_entries_current7_before_child=oldcwd)
 binding_path=m.OUT/'ACTUAL_B_ORIGINAL_INPUT_AND_FRESH_IO_BINDING.json';m.write(binding_path,binding);pb=c.pin(binding_path);owned.append(pb)
 core=m.source(next(p for p in sf['complete_source_file_pins']if Path(p['path']).name=='capture_current_original_B.UNREADY.py'),'current_B_complete_capture_core');seed=m.metadata(packet['original_v10_seed_plan_pin']);runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'B_capture',resources)
 need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','exact unchanged private original runner and bounded Source')
 state=None;first=None;secondary=[];watches=[];after=None;good=False
 try:
  state,record=core.execute_B_with_original_runner(runner,full,production,resources,binding,pb,seed,packet['original_v10_seed_plan_pin'],checked_fullpin,checked_recheck,resources.check)
  need(len(runner.records)==1 and record==runner.records[0]and record['status']=='PASS','sole actual B native child0, no retry')
  wp=m.OUT/(record['label']+'.watchdog.json');lp=m.OUT/(record['label']+'.log');w=m.metadata(c.pin(wp));watches.append(dict(actual_stage_record_label=record['label'],actual_watchdog_pin=c.pin(wp),actual_watchdog=w,actual_log_pin=c.pin(lp)))
  need(watches[-1]['actual_log_pin']['sha256']==record['log_sha256']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original material child0/record.label log/watch/PS/RSS/wall/group closure')
  after=check_all();route.recheck_old_cwd_current7(oldcwd);good=True
 except BaseException as e:first=e
 finally:
  if runner.records and not watches:
   try:
    record=runner.records[-1];wp=m.OUT/(record['label']+'.watchdog.json');lp=m.OUT/(record['label']+'.log')
    if wp.exists():watches.append(dict(actual_stage_record_label=record['label'],actual_watchdog_pin=c.pin(wp),actual_watchdog=m.metadata(c.pin(wp)),actual_log_pin=c.pin(lp)if lp.exists()else None))
   except BaseException as e:secondary.append(dict(where='failed-stage raw monitor',error=repr(e)))
  for closing in(check_all,lambda:route.recheck_old_cwd_current7(oldcwd)):
   try:after=closing()or after
   except BaseException as e:
    if first is None:first=e
    else:secondary.append(repr(e))
  cwd_after=None
  try:cwd_after=route.snapshot_old_cwd_current7()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(dict(where='final old-cwd snapshot',error=repr(e)))
  report=dict(schema='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1',status='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'if good and first is None else'FAILED_CURRENT_B_NATIVE_CAPTURE_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,records=runner.records,actual_watchdog_checks=watches,actual_B_state=state,source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=sf['control_plan_pin'],actual_B_input_binding_pin=pb,actual_B_IO_build_Host_report_pin=packet['actual_B_IO_build_Host_report_pin'],actual_B_IO_build_post_pin=packet['actual_B_IO_build_post_pin'],new_IO_runtime_pin=packet['new_IO_runtime_pin'],original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=m.CAPS,complete_joint_roots=roots,resources_before=before,resources_after=after,all_old_cwd_entries_current7_before=oldcwd,all_old_cwd_entries_current7_after=cwd_after,final_report_resource_check_passed=False,**m.FALSE)
  path=m.OUT/'Root_actual_current_B_complete_capture_summary.json';m.write(path,report)
  try:
   resources.check();report['final_report_resource_check_passed']=True
   with path.open('w')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
   resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
 if first is not None:raise first
 report_pin=c.pin(path);manifest=core.make_B_manifest(state,binding,pb,report_pin);manifest_path=m.OUT/'CURRENT_FORMAL_COMPLETE_B_MATERIAL_OBSERVATION_MANIFEST.json';m.write(manifest_path,manifest);manifest_pin=c.pin(manifest_path);check_all();route.recheck_old_cwd_current7(oldcwd);resources.check()
 print(json.dumps(dict(status=report['status'],report_pin=report_pin,manifest_pin=manifest_pin,actual_B_native_capture_closed0=True,**m.FALSE)),flush=True)
if __name__=='__main__':main()

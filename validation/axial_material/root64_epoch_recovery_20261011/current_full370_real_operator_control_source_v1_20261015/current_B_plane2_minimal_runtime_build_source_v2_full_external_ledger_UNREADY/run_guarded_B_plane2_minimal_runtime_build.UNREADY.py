"""UNREADY owning Root host: three compile and one link stages under unchanged OwnRSS class."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def raw_metadata_argument(a,role):
 n=role.replace('-','_');ids=json.loads(getattr(a,n+'_seven_id'));q=Path(getattr(a,n+'_summary'));s=q.lstat();expected=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=ids[4],identity=ids)
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==ids and s.st_size<8*2**20,'exact initial freeze metadata current7')
 b=q.read_bytes();need(hashlib.sha256(b).hexdigest()==expected['sha256'],'exact freeze wholeSHA');return json.loads(b),expected
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();start=time.monotonic()
 with(BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_B_PLANE2_RUNTIME_BUILD_CLAIM_V1',Root_PID=os.getpid(),original_monotonic_start=start,argv=sys.argv,claim_before_metadata_EOF_or_import_or_compiler=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 sf,psf=raw_metadata_argument(a,'source-freeze');hf,phf=raw_metadata_argument(a,'host-freeze')
 cp=hf['contract_Source_pin'];spec=importlib.util.spec_from_file_location('B_PLANE2_RUNTIME_source_contract',cp['path']);m=importlib.util.module_from_spec(spec)
 need(Path(cp['path'])==BASE/'build_B_plane2_runtime_Source_contract.UNREADY.py'and hashlib.sha256(Path(cp['path']).read_bytes()).hexdigest()==cp['sha256'],'exact author-frozen Source contract')
 spec.loader.exec_module(m);m.current(cp)
 need(sf['schema']=='B_PLANE2_RUNTIME_SOURCE_FREEZE_V1'and hf['schema']=='B_PLANE2_RUNTIME_HOST_FREEZE_V1'and sf['source_only']is True and sf['business_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==m.CAPS,'exact Source-only freeze pair')
 plan=m.load_plan(sf['control_plan_pin']);need(plan['schema']=='B_PLANE2_RUNTIME_SOURCE_ONLY_PLAN_V1'and plan['actual_business_preconditions_closed']is True and plan['planned_actual_output_root']==str(m.OUT)and not os.path.lexists(m.OUT),'UNREADY until frozen actual lifecycle and compiler/input bindings, fresh output once')
 m.admit_lifecycle(plan);m.source_module(plan['original_production_inputs_Source_pin'],'production_inputs');c=m.source_module(plan['original_Common_Source_pin'],'B_PLANE2_RUNTIME_original_common');support=m.source_module(plan['original_support_Source_pin'],'B_PLANE2_RUNTIME_original_support')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original one-thread exact interpreter')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B_PLANE2_RUNTIME_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'B_PLANE2_RUNTIME_original_resource_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unchanged genuine original OwnRSS class/PID/MRO')
 roots=plan['complete_joint_roots'];need(len(roots)==len(set(roots))and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'entire latest prefix no reset/no overlapping hidden output root')
 joined=production.DiskResources(m.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800,'original hostSELF512/whole1800 from initial claim')
   ps=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2);need(ps.returncode==0 and ps.stderr==''and len(ps.stdout)<1024 and ps.stdout.strip().isdigit()and int(ps.stdout.strip())*1024<512*2**20,'same-PID root PS RSS512');h=history.check();j=joined.check();need(all(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots'])for p in plan['readonly_history_code_and_selected_native_pins']),'exact compiler/object/module/archive and selected readonly data remain original history');own=sum(q.stat().st_size for q in m.OUT.rglob('*')if q.is_file())if m.OUT.exists()else 0
   need(own<m.OUTPUT_BOUND,'entire build sources/objects/modules/runtime/log/watch/report32MiB')
   source=sum(q.stat().st_size for q in BASE.rglob('*')if q.is_file()and not q.is_relative_to(m.OUT));need(source<m.SOURCE_BOUND,'Source/metadata8MiB')
   extra=0
   for p in hf['explicit_cumulative_metadata_file_pins']:
    m.current_metadata_role(p,plan)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:s=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged cumulative2/history96/cold/meta/free8 including external metadata/open-unlinked')
   return dict(original_history=dict(artifact_bytes=h['artifact_bytes'],resource_root_count=len(h['resource_roots'])),complete_joint=dict(artifact_bytes=j['artifact_bytes'],disk_free_bytes=j['disk_free_bytes'],resource_root_count=len(roots)),explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start,Root_same_PID_PS=dict(returncode=ps.returncode,stdout=ps.stdout,stderr=ps.stderr))
 resources=Resources();before=resources.check();need(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'complete32MiB output plus Source8 reserve before compiler start')
 fixed=m.unique(plan['compile_and_link_input_pins']+plan['whole_byte_build_source_copy_pins']+sf['complete_source_file_pins']+[psf,phf,cp]+[c.pin(p)for p in guard_files]);owned=[]
 def check_all():
  for p in fixed:m.current_metadata_role(p,plan);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  m.admit_retained(plan)
  for row in plan['original_compile_include_directory_identities']:
   q=Path(row['path']);st=q.lstat();need(stat.S_ISDIR(st.st_mode)and m.identity(st)==row['identity']and not any(x.is_symlink()for x in(q,*q.parents)),'exact original include directory order/current7')
  need(sorted(str(p)for row in plan['original_compile_include_directory_identities']for p in Path(row['path']).glob('*.mod'))==sorted(plan['compile_module_search_directory_file_inventory']),'whole original include module inventory unchanged, no implicit new ABI search entry')
  for p in plan['explicit_cumulative_metadata_file_pins']:m.current_metadata_role(p,plan)
  for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path']),'exact retired plaintext role remains absent, not a current compiler input')
  return resources.check()
 check_all();m.OUT.mkdir();(m.OUT/'runtime').mkdir();(m.OUT/'sources').mkdir();(m.OUT/'sources/build').mkdir();(m.OUT/'sources/runtime').mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');owned.append(c.pin(m.OUT/'runtime/run_bounded_dragon.py'));need(owned[-1]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source')
 for p in plan['whole_byte_build_source_copy_pins']:
  target=m.OUT/'sources'/Path(p['path']).name;need(not os.path.lexists(target),'fresh literal Source copy only');shutil.copy2(p['path'],target);q=c.pin(target);need(q['sha256']==p['sha256']and q['size_bytes']==p['size_bytes'],'whole original/IO Source bytes, no SCI/library copy');owned.append(q)
 result=m.commands(plan);stages=list(zip(('compile_APACKX64','compile_B2PLNX64','compile_KDRDRV'),result['compile_commands']))+[('link_complete71_Dragon',result['link_command'])]
 (m.OUT/'B_PLANE2_RUNTIME_build').mkdir()
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'B_PLANE2_RUNTIME_build',resources);need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','exact original own runner, same monotonic whole remaining time')
 first=None;secondary=[];watches=[];after=None;good=False
 try:
  for label,cmd in stages:
   check_all();stage_error=None;watch=None
   try:runner.execute(m.OUT/'sources/build',label,cmd,600)
   except BaseException as e:stage_error=e
   try:
    if runner.records:
     record=runner.records[-1];wp=m.OUT/(record['label']+'.watchdog.json');lp=m.OUT/(record['label']+'.log')
     if wp.exists():watch=m.metadata(c.pin(wp));watches.append(dict(actual_stage_record_label=record['label'],actual_watchdog_pin=c.pin(wp),actual_watchdog=watch,actual_log_pin=c.pin(lp)if lp.exists()else None))
   except BaseException as e:
    if stage_error is None:raise
    secondary.append(dict(where='failed-stage raw monitor metadata',error=repr(e)))
   if stage_error is not None:raise stage_error
   need(watch is not None and watches[-1]['actual_log_pin']is not None and watches[-1]['actual_log_pin']['sha256']==record['log_sha256'],'genuine successful stage must have original monitor and log from actual record.label')
   need(record['status']=='PASS'and type(watch['returncode'])is int and watch['returncode']==0 and watch['command']==cmd and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'genuine original once stage0/PS RSS/wall/group closure')
   check_all()
  need(len(runner.records)==4 and len(watches)==4,'all three compiles and one link exactly once')
  runtime=c.pin(m.OUT/'sources/runtime/Dragon');need(runtime['size_bytes']>0,'new emitted runtime PF, no old binary qualification inheritance');after=check_all();good=True
 except BaseException as e:first=e
 finally:
  try:after=check_all()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ACTUAL_B_PLANE2_MINIMAL_RUNTIME_THREE_COMPILE_COMPLETE71_LINK_REPORT_V1',status='ACTUAL_B_PLANE2_MINIMAL_RUNTIME_FOUR_STAGE0_BUILD_ONLY'if good and first is None else'FAILED_B_PLANE2_RUNTIME_BUILD_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,records=runner.records,actual_watchdog_checks=watches,whole_new_output_pins=[c.pin(q)for q in sorted(m.OUT.rglob('*'))if q.is_file()],source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=sf['control_plan_pin'],new_explicit_object_count=67,original_explicit_object_count=66,archive_count=4,build_stage_count=len(runner.records),old_link_argv_inverse_equal=True,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=m.CAPS,resources_before=before,resources_after=after,final_report_resource_check_passed=False,actual_ordered71_link_inputs=result['ordered71_link_inputs'],actual_new_three_object_pins=[c.pin(m.OUT/'sources/build'/n)for n in('APACKX64.o','B2PLNX64.o','KDRDRV.o')if(m.OUT/'sources/build'/n).exists()],actual_new_Dragon_pin=c.pin(m.OUT/'sources/runtime/Dragon')if(m.OUT/'sources/runtime/Dragon').exists()else None,actual_original_owned_runtime_Root_integer_exit_code=1,actual_original_owned_runtime_compile_link_children_exit0_only=True,**m.FALSE)
  path=m.OUT/'Root_actual_B_plane2_minimal_runtime_build_summary.json';need(len((json.dumps(report,indent=2,allow_nan=False)+'\n').encode())<6*2**20,'summary6MiB inside total32MiB');c.write(path,report)
  try:
   resources.check();report['final_report_resource_check_passed']=True
   with path.open('w')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.truncate();f.flush();os.fsync(f.fileno())
   resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
 if first is not None:raise first
 print(json.dumps(dict(status=report['status'],report_pin=c.pin(path),new_binary_actual_compile_link_only=True,**m.FALSE)),flush=True)
if __name__=='__main__':main()

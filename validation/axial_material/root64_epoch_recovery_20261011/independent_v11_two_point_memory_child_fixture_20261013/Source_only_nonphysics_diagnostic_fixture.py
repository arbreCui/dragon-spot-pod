"""Existing-metadata memory fixture only. No pipeline import/child/science work.

Original resource classes and original dump_json remain unmodified. Writes only
own diagnostic prefixes, never business records; original source/evidence reach
EOF before and retain every SHA/identity after measurement. Peak RSS is not reset.
"""
import argparse,ast,gc,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
HERE=REC/'independent_v11_two_point_memory_child_fixture_20261013'
FIXTURE=Path('/Users/wen/spot/validation/artifacts/axial-material-v11-two-point-memory-child-metadata-diagnostic-20261013')
START=time.monotonic();PF={};SAMPLES=[];checks=0
sys.dont_write_bytecode=True

def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,wanted=None):
 global checks
 p=Path(p);b=identity(p);assert stat.S_ISREG(b[2])and not any(x.is_symlink()for x in(p,*p.parents))
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==b
  h=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==b==identity(p)
 v=dict(path=str(p),sha256=h,size_bytes=b[4],identity=b)
 if wanted is not None:assert v==wanted
 assert str(p)not in PF or PF[str(p)]==v
 PF[str(p)]=v;checks+=1;return v
def module(p,name):
 before=pin(p);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);assert pin(p)==before;return m
def size(root):
 seen=set();stack=[root];total=0
 while stack:
  v=stack.pop()
  if id(v)in seen:continue
  seen.add(id(v));total+=sys.getsizeof(v)
  if isinstance(v,dict):stack.extend(v.keys());stack.extend(v.values())
  elif isinstance(v,(tuple,list,set,frozenset)):stack.extend(v)
 return total,len(seen)
def metric(label,**extra):
 raw=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
 assert raw.returncode==0 and raw.stdout.strip().isdigit(),'actual own process RSS unavailable'
 r=dict(label=label,current_RSS_bytes=int(raw.stdout.strip())*1024,ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  allocated_blocks=sys.getallocatedblocks(),gc_count=list(gc.get_count()),gc_stats=gc.get_stats(),elapsed_seconds=time.monotonic()-START,**extra)
 SAMPLES.append(r)
 if r['ru_maxrss_bytes']>=512*2**20:raise RuntimeError('readonly fixture unchanged SELF512 ceiling reached')
 if time.monotonic()-START>=1800:raise RuntimeError('readonly fixture original whole1800 ceiling reached')
 return r
def write(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
 assert not HERE.exists()and not FIXTURE.exists(),'fresh diagnostic only, no overwrite or retry'
 assert all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
 assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
 HERE.mkdir();FIXTURE.mkdir();(FIXTURE/'runtime').mkdir();(FIXTURE/'diagnostic').mkdir()
 metric('initial')
 c=module(REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py','diagnostic_original_current_common')
 support=module(c.SUPPORT,'diagnostic_original_support')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'diagnostic_original_helper')
 factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'diagnostic_original_factory')
 full,production=helper.modules();assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__)==support.FULL and Path(production.__file__)==support.PARENT
 for p in(support.FULL,support.PARENT,support.BOUNDED,support.RESOURCE_FACTORY,support.OLD_HELPER):pin(p)
 assert factory.DynamicHistoryResources.check.__module__==factory.__name__
 metric('genuine_original_common_support_factory_guard_imports')
 cli_path=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json';pin(cli_path);cli=json.loads(cli_path.read_text())
 catalog=c.current_catalog();binding=json.loads(c.BIND.read_text());pin(c.BIND)
 objects={}
 for name,p in cli['mandatory_external_bindings'].items():
  d,p2=c.load_json_exact(p['path'],p['sha256'],json.dumps(p['identity']));assert p==p2;objects[name]=d;pin(p['path'],p)
  if name in('a1','a2','a3'):c.closed_report(d,helper,Path(p['path']).parent,4)
  metric('admitted_metadata_'+name)
 build=objects['build70']
 for name,key in(('current69','original_actual69_handle_lifetime_report_pin'),('original69','original_actual69_v4_report_pin')):
  p=build[key];d,p2=c.load_json_exact(p['path'],p['sha256'],json.dumps(p['identity']));assert p==p2;objects[name]=d;pin(p['path'],p)
 eighteen,p17=c.admit17(cli['mandatory_external_bindings']['seventeen']['path'],cli['mandatory_external_bindings']['seventeen']['sha256'],json.dumps(cli['mandatory_external_bindings']['seventeen']['identity']),helper)
 objects['admitted17']=eighteen
 metric('all_original_large_metadata_live',unique_heap_bytes=size(objects)[0])
 cached=dict(compiler=build['records'][0]['command'][0],includes=tuple(x for x in build['records'][0]['command']if x.startswith('-I')),
  archives=tuple(x for x in build['records'][-1]['command']if x.endswith('.a')),exe=dict(next(x for x in build['output_pins']if Path(x['path']).name=='Dragon')),
  link_command=build['records'][-1]['command'],bounded_sha256=binding['original_bounded']['sha256'])
 hf=objects['host-freeze'];objects.clear();del build,eighteen,binding,d,p2,p;collected=gc.collect()
 metric('v11_style_large_metadata_closed_and_one_explicit_gc',collected=collected,required_cached_command_heap_bytes=size(cached)[0])
 stagepath=OUT/'AAA3-streaming/stages.json';rawpath=OUT/'Root_actual_complete_execution_record_before_final_publication.json'
 ledger_pin=pin(stagepath);raw_pin=pin(rawpath);loaded=json.loads(stagepath.read_bytes());records=loaded['stages'];assert len(records)==45;del loaded
 # Raw read validates exact original records; then close that extra decode.
 raw=json.loads(rawpath.read_bytes());assert raw['records']==records;fixed=raw['fixed_current_pins'];proofs=raw['actual_complete_readback_proofs'];cases=raw['actual_operator_refusals'];release=raw['actual_private_release_ledger'];scratch=raw['actual_closed_CLE_scratch_archival_ledger'];del raw;gc.collect()
 metric('true_original45_raw_resource_payload_live',records_unique_heap_bytes=size(records)[0],preserved_business_state_heap_bytes=size([records,fixed,proofs,cases,release,scratch,cached,hf,catalog])[0])
 history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(OUT),str(FIXTURE)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 fresh=production.DiskResources(c.ART,[str(FIXTURE)],8*2**30,2*2**30)
 # Extract exact class declarations only. Never import candidate pipeline or
 # execute initialize/main, alter original classes or replace serialization.
 commontext=Path(c.__file__).read_text();ct=ast.parse(commontext);initialize=next(n for n in ct.body if isinstance(n,ast.FunctionDef)and n.name=='initialize');resourceclass=next(n for n in initialize.body if isinstance(n,ast.ClassDef)and n.name=='Resources')
 env={'history':history,'fresh':fresh};exec(compile(ast.Module(body=[resourceclass],type_ignores=[]),'<exact original Resources class declaration>','exec'),env);original_resources=env['Resources']()
 host=REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py';pin(host);hosttext=host.read_text();ht=ast.parse(hosttext);phaseclass=next(n for n in ht.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources')
 penv={'Path':Path,'WORK':FIXTURE/'diagnostic','OUT':FIXTURE,'MI':2**20};exec(compile(ast.Module(body=[phaseclass],type_ignores=[]),'<exact original PhaseResources class declaration>','exec'),penv);resources=penv['PhaseResources'](original_resources);resources.phase='NONPHYSICS_DUMMY_PROCESS_METADATA_DIAGNOSTIC'
 metric('exact_original_resource_classes_constructed',history_own_keys=list(history.__dict__),phase_own_keys=list(resources.__dict__))

 import shutil
 bp=pin(OUT/'runtime/run_bounded_dragon.py');assert bp['sha256']==support.BOUNDED_SHA
 shutil.copy2(OUT/'runtime/run_bounded_dragon.py',FIXTURE/'runtime/run_bounded_dragon.py');copied=pin(FIXTURE/'runtime/run_bounded_dragon.py');assert copied['sha256']==bp['sha256']and copied['identity'][:2]!=bp['identity'][:2]
 runner=full.OwnRSSSerialExecutor(FIXTURE,1800-(time.monotonic()-START),'diagnostic',resources)
 assert type(runner)is full.OwnRSSSerialExecutor and runner.__class__.__bases__==(production.SerialExecutor,)and Path(runner.bounded.__file__).resolve()==FIXTURE/'runtime/run_bounded_dragon.py'
 original_class_source=ast.get_source_segment(Path(full.__file__).read_text(),next(n for n in ast.parse(Path(full.__file__).read_bytes()).body if isinstance(n,ast.ClassDef)and n.name=='OwnRSSSerialExecutor'))
 original_process_source=ast.get_source_segment(Path(full.__file__).read_text(),next(n for n in ast.walk(ast.parse(Path(full.__file__).read_bytes()))if isinstance(n,ast.FunctionDef)and n.name=='_process'))
 baseline=metric('same_original_admitted_metadata_closed_actual45_live_before_ps')

 import threading
 stop=threading.Event();monitor_rows=[];monitor_errors=[];state={'point':'baseline','child_pidfile':None};cap_flag=threading.Event()
 def monitor_parent():
  while not stop.is_set():
   try:
    proc=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
    if proc.returncode!=0 or not proc.stdout.strip().isdigit():raise RuntimeError('own-parent real ps RSS unavailable')
    child_rss=None;child_pid=None
    path=state['child_pidfile']
    if path is not None and path.exists():
     child_pid=int(path.read_text());q=subprocess.run(['/bin/ps','-o','rss=','-p',str(child_pid)],capture_output=True,text=True,timeout=2)
     if q.returncode==0 and q.stdout.strip().isdigit():child_rss=int(q.stdout.strip())*1024
    maximum=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    monitor_rows.append(dict(point=state['point'],elapsed_seconds=time.monotonic()-START,parent_pid=os.getpid(),parent_current_RSS_bytes=int(proc.stdout.strip())*1024,parent_ru_maxrss_bytes=maximum,actual_dummy_child_pid=child_pid,actual_dummy_child_current_RSS_bytes=child_rss,SELF512_crossed=maximum>=512*2**20))
    if maximum>=512*2**20 or time.monotonic()-START>=1800:cap_flag.set()
   except BaseException as exc:monitor_errors.append(type(exc).__name__+': '+str(exc));cap_flag.set();return
   stop.wait(.1)
 monitor=threading.Thread(target=monitor_parent,name='readonly-own-parent-and-owned-memory-child-monitor',daemon=True);monitor.start();time.sleep(.25)
 monitor_baseline=metric('baseline_with_independent_readonly_parent_monitor_thread')
 child_rows=[];status='NONPHYSICS_TWO_POINT_MEMORY_CHILD_DIAGNOSTIC_COMPLETE';failure=None
 try:
  for label,size_mib in [('LOW_NONPHYSICS_32MIB',32),('HIGH_NONPHYSICS_470MIB',470)]:
   if cap_flag.is_set():raise RuntimeError('original SELF512 or whole1800 or ownmonitor refusal before next diagnostic point')
   log=FIXTURE/'diagnostic'/(label+'.log');pidfile=FIXTURE/'diagnostic'/(label+'.pid')
   code="import os,sys,time,resource,json; from pathlib import Path; Path(sys.argv[1]).write_text(str(os.getpid())); n=int(sys.argv[2]); data=bytearray(n); [(data.__setitem__(i,1)) for i in range(0,n,4096)]; print(json.dumps({'schema':'NONPHYSICS_PURE_MEMORY_CHILD_V1','pid':os.getpid(),'actual_allocated_bytearray_bytes':len(data),'actual_child_ru_maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'all_pages_touched':True,'physics_or_science_business':False}),flush=True); time.sleep(1.2)"
   command=[sys.executable,'-B','-c',code,str(pidfile),str(size_mib*2**20)]
   state['point']=label;state['child_pidfile']=pidfile;resources.check();pre=metric('before_'+label);error=None;limit=min(600.,1800.-(time.monotonic()-START));assert limit>0
   with log.open('xb')as output:
    try:runner._process(command,FIXTURE/'diagnostic',subprocess.DEVNULL,output,limit)
    except RuntimeError as exc:error=str(exc)
   watch=log.with_suffix('.watchdog.json');wp=pin(watch);w=json.loads(watch.read_bytes());logpin=pin(log);pidpin=pin(pidfile);value=json.loads(log.read_bytes())
   assert value['schema']=='NONPHYSICS_PURE_MEMORY_CHILD_V1'and value['all_pages_touched']is True and value['actual_allocated_bytearray_bytes']==size_mib*2**20 and value['physics_or_science_business']is False
   assert int(pidfile.read_text())==value['pid']==w['pid']and w['command']==command
   assert w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600
   try:os.killpg(w['pid'],0)
   except ProcessLookupError:absent=True
   else:absent=False
   assert absent,'only own dummy process group must close'
   state['point']=label+'_CLOSED';state['child_pidfile']=None;post=metric('after_'+label)
   observations=[x for x in monitor_rows if x['point']==label]
   child_rows.append(dict(label=label,pure_memory_diagnostic=True,allocated_bytes=size_mib*2**20,all_pages_touched=True,actual_child_pid=w['pid'],actual_guard_watchdog_fullpin=wp,actual_dummy_log_fullpin=logpin,actual_pid_metadata_fullpin=pidpin,actual_guard_watchdog=w,actual_child_own_logged_self_ru_maxrss_bytes=value['actual_child_ru_maxrss_bytes'],actual_guard_error=error,actual_returncode=w['returncode'],actual_own_child_group_absent=absent,parent_before=pre,parent_after=post,parent_max_current_RSS_during_child_bytes=max(x['parent_current_RSS_bytes']for x in observations),parent_max_ru_maxrss_during_child_bytes=max(x['parent_ru_maxrss_bytes']for x in observations),max_independent_actual_child_RSS_bytes=max([x['actual_dummy_child_current_RSS_bytes']for x in observations if x['actual_dummy_child_current_RSS_bytes']is not None],default=0),independent_monitor_sample_count=len(observations),physics_or_science_control_qualification=False))
   if error is not None or w['returncode']!=0 or w['limit_failure']is not None or w['sampled_peak_rss_mib']>=512:raise RuntimeError('original own child guard refused nonphysics memory point: '+str(error))
   if post['ru_maxrss_bytes']>=512*2**20 or cap_flag.is_set():raise RuntimeError('original SELF512 or whole1800 diagnostic limit refusal')
   resources.check();time.sleep(.25);collected=gc.collect();metric('after_'+label+'_one_explicit_gc',collected=collected)
 except BaseException as exc:status='NONPHYSICS_TWO_POINT_MEMORY_CHILD_LIMIT_OR_ERROR_REFUSAL';failure=type(exc).__name__+': '+str(exc)
 finally:stop.set();monitor.join(timeout=5)
 assert not monitor.is_alive()and runner.records==[]
 assert records==json.loads(stagepath.read_bytes())['stages']and len(records)==45
 assert type(runner)is full.OwnRSSSerialExecutor and full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
 assert ast.get_source_segment(Path(full.__file__).read_text(),next(n for n in ast.parse(Path(full.__file__).read_bytes()).body if isinstance(n,ast.ClassDef)and n.name=='OwnRSSSerialExecutor'))==original_class_source
 for q in list(PF.values()):pin(q['path'],q)
 actual_outputs=[pin(p)for p in sorted(FIXTURE.rglob('*'))if p.is_file()];real_output_bytes=sum(q['size_bytes']for q in actual_outputs);resource_after=resources.check()
 assert resource_after['fresh_output']['artifact_bytes']==real_output_bytes and resource_after['fresh_output']['regular_files']==len(actual_outputs)and str(FIXTURE)in resource_after['resource_roots']
 last=dict(parent_current_RSS_bytes=monitor_rows[-1]['parent_current_RSS_bytes'],parent_ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 report=dict(schema='GENUINE_ORIGINAL_GUARD_TWO_POINT_PURE_MEMORY_CHILD_DIAGNOSTIC_V1',status=status,failure=failure,namespace=str(FIXTURE),diagnostic_points=child_rows,independent_readonly_parent_monitor='PASSIVE_PARENT_THREAD_TRUE_OWN_PID_PS_PLUS_TRUE_RUSAGE_SELF_AND_OWN_CHILD_PID_PS',monitor_errors=monitor_errors,all_actual_parent_and_child_monitor_samples=monitor_rows,monitor_joined_and_stopped=True,SELF512_crossed_during_diagnostic=any(x['SELF512_crossed']for x in monitor_rows),original_MRO_guard_and_process_method_unchanged=True,original_process_method_whole_body=original_process_source,original_Source_and_actual_metadata_fullpins=list(PF.values()),all_original45_raw_resource_records_preserved=True,actual_original_stage_ledger_pin=ledger_pin,actual_original_raw_record_pin=raw_pin,actual_diagnostic_artifact_fullpins=actual_outputs,actual_diagnostic_ART_bytes=real_output_bytes,actual_original_resources_after=resource_after,original_history_fresh_cold_free_SELF_child_whole_stage_caps_unchanged=True,actual_metadata_closed_raw45_baseline=baseline,baseline_with_passive_monitor=monitor_baseline,all_true_parent_metrics=SAMPLES,last_true_parent_metric=last,actual_dummy_child_count=len(child_rows),scientific_execution_record_count=0,diagnostic_runner_records=[],native_or_solver_numerical_business_executed=False,no_stage_or_child_retry=True,RSS_or_resource_algorithm_not_modified=True,ru_maxrss_never_reset=True,profile_disabled=True,original_execute_or_dump_json_not_called=True,new_pipeline_Source_or_v7_Source_modified=False,SELF_review_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START,engineering_three_plane_closed0=False,physics_or_science_control_qualification=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(HERE/'REVIEW.json',report)
 print(json.dumps(dict(status=status,failure=failure,review_pin=pin(HERE/'REVIEW.json'),metadata_baseline_RSS=baseline['current_RSS_bytes'],metadata_baseline_ru_maxrss=baseline['ru_maxrss_bytes'],monitor_baseline_RSS=monitor_baseline['current_RSS_bytes'],monitor_baseline_ru_maxrss=monitor_baseline['ru_maxrss_bytes'],last_parent_metric=last,actual_CHILD_points=[{k:v for k,v in x.items()if k in('label','allocated_bytes','actual_returncode','actual_child_own_logged_self_ru_maxrss_bytes','parent_max_current_RSS_during_child_bytes','parent_max_ru_maxrss_during_child_bytes','max_independent_actual_child_RSS_bytes','independent_monitor_sample_count')}for x in child_rows],actual_diag_ART_bytes=real_output_bytes,wall_seconds=report['elapsed_seconds'])),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

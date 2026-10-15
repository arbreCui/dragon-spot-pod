"""Existing-metadata memory fixture only. No pipeline import/child/science work.

Original resource classes and original dump_json remain unmodified. Writes only
own diagnostic prefixes, never business records; original source/evidence reach
EOF before and retain every SHA/identity after measurement. Peak RSS is not reset.
"""
import argparse,ast,gc,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
HERE=REC/'independent_v11_watchdog_dummy_process_memory_fixture_20261013'
FIXTURE=Path('/Users/wen/spot/validation/artifacts/axial-material-v11-watchdog-dummy-metadata-memory-diagnostic-20261013')
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
 for i in range(30):metric('diagnostic_own_self_ps_'+str(i+1))
 after_ps=metric('after30_genuine_own_ps_only_before_gc')
 ps_gc=gc.collect();after_ps_gc=metric('after30_own_ps_one_explicit_gc',collected=ps_gc)
 child_rows=[];status='NONPHYSICS_DUMMY_PROCESS_WATCHDOG_MEMORY_DIAGNOSTIC_COMPLETE';failure=None
 try:
  for i in range(16):
   expected=i%2;label='DIAGNOSTIC_DUMMY_EXIT_'+str(expected)+'_'+str(i+1).zfill(2);log=FIXTURE/'diagnostic'/(label+'.log')
   command=[sys.executable,'-B','-c','import sys,time; time.sleep(0.25); sys.exit('+str(expected)+')']
   resources.check();pre=metric('before_'+label);error=None
   limit=min(600.,1800.-(time.monotonic()-START))
   assert limit>0
   with log.open('xb')as output:
    try:runner._process(command,FIXTURE/'diagnostic',subprocess.DEVNULL,output,limit)
    except RuntimeError as exc:error=str(exc)
   watch=log.with_suffix('.watchdog.json');wp=pin(watch);w=json.loads(watch.read_bytes());logpin=pin(log)
   assert w['command']==command and w['returncode']==expected and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True
   assert 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512
   assert error==('own-child stage failed; no retry'if expected else None)
   try:os.killpg(w['pid'],0)
   except ProcessLookupError:absent=True
   else:absent=False
   assert absent,'own dummy child process group remains after genuine original cleanup'
   assert runner.records==[],'direct original _process must not create scientific execution stage records'
   resources.check();post=metric('after_'+label)
   child_rows.append(dict(label=label,explicitly_nonphysics_metadata_dummy=True,expected_exit_code=expected,actual_returncode=w['returncode'],original_own_guard_error_string=error,genuine_watchdog_fullpin=wp,dummy_log_fullpin=logpin,actual_child_pid=w['pid'],own_child_group_absent_after_original_watchdog_finish=True,elapsed_seconds=w['elapsed_seconds'],original_child_peak_RSS_MiB=w['sampled_peak_rss_mib'],original_cap_rss_mib=512,original_stage_wall_seconds=limit,SELF_current_before=pre['current_RSS_bytes'],SELF_current_after=post['current_RSS_bytes'],SELF_ru_maxrss_before=pre['ru_maxrss_bytes'],SELF_ru_maxrss_after=post['ru_maxrss_bytes'],scientific_control_or_business_qualification=False))
  no_gc=metric('after16_original_process_real_watchdog_before_gc');collected=gc.collect();final=metric('after16_processes_one_explicit_gc',collected=collected)
 except BaseException as exc:
  status='NONPHYSICS_DUMMY_PROCESS_DIAGNOSTIC_LIMIT_OR_ERROR_REFUSAL';failure=type(exc).__name__+': '+str(exc);final=metric('diagnostic_refusal_snapshot')
 assert records==json.loads(stagepath.read_bytes())['stages']and len(records)==45
 assert runner.records==[]and type(runner)is full.OwnRSSSerialExecutor and full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
 assert ast.get_source_segment(Path(full.__file__).read_text(),next(n for n in ast.parse(Path(full.__file__).read_bytes()).body if isinstance(n,ast.ClassDef)and n.name=='OwnRSSSerialExecutor'))==original_class_source
 for q in list(PF.values()):pin(q['path'],q)
 actual_outputs=[pin(p)for p in sorted(FIXTURE.rglob('*'))if p.is_file()];real_output_bytes=sum(q['size_bytes']for q in actual_outputs)
 resource_after=resources.check();assert resource_after['fresh_output']['artifact_bytes']==real_output_bytes and resource_after['fresh_output']['regular_files']==len(actual_outputs)and str(FIXTURE)in resource_after['resource_roots']
 report=dict(schema='GENUINE_ORIGINAL_PROCESS_WATCHDOG_DUMMY_MEMORY_DIAGNOSTIC_V1',status=status,failure=failure,namespace=str(FIXTURE),genuine_original_MRO_and_class_source_unchanged=True,original_process_method_whole_body=original_process_source,original_Source_and_actual_metadata_fullpins=list(PF.values()),actual_business45_raw_records_unchanged=True,actual_original_stage_ledger_pin=ledger_pin,actual_original_raw_record_pin=raw_pin,actual_business_records_count=45,diagnostic_runner_records=[],scientific_execution_record_count=0,diagnostic_dummy_child_count=len(child_rows),expected_dummy_exit0_count=sum(q['expected_exit_code']==0 for q in child_rows),expected_dummy_exit1_count=sum(q['expected_exit_code']==1 for q in child_rows),original_child_own_watchdog_results=child_rows,all_original_output_full_EOF_pins=actual_outputs,actual_diagnostic_ART_bytes_before_report=real_output_bytes,actual_diagnostic_output_file_count_before_report=len(actual_outputs),actual_original_resources_after=resource_after,all_actual_resource_snapshots_retained=True,resource_OR_serialization_faked=False,original_execute_OR_dump_json_called=False,measurements=SAMPLES,baseline=baseline,after30_ps=after_ps,after30_ps_gc=after_ps_gc,final=final,actual_current_RSS_difference_final_minus_baseline=final['current_RSS_bytes']-baseline['current_RSS_bytes'],actual_ru_maxrss_difference_final_minus_baseline=final['ru_maxrss_bytes']-baseline['ru_maxrss_bytes'],original_cap_SELF_and_child_bytes=512*2**20,original_cap_whole_seconds=1800,original_cap_stage_max_seconds=600,original_caps_no_change=True,SELF_review_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START,process_path_fixture_only_no_native_solver=True,new_pipeline_Source_or_v7_Source_modified=False,physics_or_science_control_qualification=False,engineering_three_plane_closed0=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(HERE/'REVIEW.json',report)
 print(json.dumps(dict(status=status,failure=failure,review_pin=pin(HERE/'REVIEW.json'),dummy_children=len(child_rows),scientific_stage_records=0,baseline_currentRSS=baseline['current_RSS_bytes'],final_currentRSS=final['current_RSS_bytes'],baseline_ru_maxrss=baseline['ru_maxrss_bytes'],final_ru_maxrss=final['ru_maxrss_bytes'],SELF_current_change_bytes=report['actual_current_RSS_difference_final_minus_baseline'],SELF_peak_change_bytes=report['actual_ru_maxrss_difference_final_minus_baseline'],actual_diag_ART_bytes=real_output_bytes,wall_seconds=report['elapsed_seconds'])),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

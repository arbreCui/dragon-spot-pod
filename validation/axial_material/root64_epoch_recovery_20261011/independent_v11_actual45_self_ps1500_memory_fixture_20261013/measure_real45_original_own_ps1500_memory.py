"""Existing-metadata memory fixture only. No pipeline import/child/science work.

Original resource classes and original dump_json remain unmodified. Writes only
own diagnostic prefixes, never business records; original source/evidence reach
EOF before and retain every SHA/identity after measurement. Peak RSS is not reset.
"""
import argparse,ast,gc,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
HERE=Path(__file__).resolve().parent
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
 SAMPLES.append(r);print(json.dumps(r),flush=True)
 if r['ru_maxrss_bytes']>=512*2**20:raise RuntimeError('readonly fixture unchanged SELF512 ceiling reached')
 if time.monotonic()-START>=1800:raise RuntimeError('readonly fixture original whole1800 ceiling reached')
 return r
def write(p,v):
 with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('real45-ownps1500',),required=True);args=parser.parse_args()
 own=HERE/args.mode;own.mkdir();status='READONLY_FIXTURE_COMPLETE_NOT_BUSINESS_PROOF';failure=None
 pin(__file__);pin(REC/'independent_v11_resource_serialization_memory_fixture_20261013/measure_original_resources_and_prefix_serialization.py')
 if sys.flags.optimize or sys.getprofile() is not None or any(os.environ.get(k)!='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')):raise RuntimeError('original nonoptimized unprofiled env1')
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
 raw=json.loads(rawpath.read_bytes());assert raw['records']==records;fixed=raw['fixed_current_pins'];owned=raw['owned_runtime_pins'];proofs=raw['actual_complete_readback_proofs'];cases=raw['actual_operator_refusals'];release=raw['actual_private_release_ledger'];scratch=raw['actual_closed_CLE_scratch_archival_ledger'];del raw;gc.collect()
 metric('true_original45_raw_resource_payload_live',records_unique_heap_bytes=size(records)[0],preserved_business_state_heap_bytes=size([records,fixed,proofs,cases,release,scratch,cached,hf,catalog])[0])
 history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(OUT)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 fresh=production.DiskResources(c.ART,[str(OUT)],8*2**30,2*2**30)
 # Extract exact class declarations only. Never import candidate pipeline or
 # execute initialize/main, alter original classes or replace serialization.
 commontext=Path(c.__file__).read_text();ct=ast.parse(commontext);initialize=next(n for n in ct.body if isinstance(n,ast.FunctionDef)and n.name=='initialize');resourceclass=next(n for n in initialize.body if isinstance(n,ast.ClassDef)and n.name=='Resources')
 env={'history':history,'fresh':fresh};exec(compile(ast.Module(body=[resourceclass],type_ignores=[]),'<exact original Resources class declaration>','exec'),env);original_resources=env['Resources']()
 host=REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py';pin(host);hosttext=host.read_text();ht=ast.parse(hosttext);phaseclass=next(n for n in ht.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources')
 penv={'Path':Path,'WORK':OUT/'AAA','OUT':OUT,'MI':2**20};exec(compile(ast.Module(body=[phaseclass],type_ignores=[]),'<exact original PhaseResources class declaration>','exec'),penv);resources=penv['PhaseResources'](original_resources);resources.phase='BOOT_storage_controls'
 metric('exact_original_resource_classes_constructed',history_own_keys=list(history.__dict__),phase_own_keys=list(resources.__dict__))
 # Exactly1500 real own-RSS ps monitor calls at the original0.2s cadence.
 # Do not invoke explicit GC inside this loop or reset any peak. No business.
 assert len(fixed)==2643 and len(owned)==163 and len(records)==45
 all_before=True;completed=0;failure=None;status='READONLY_REAL45_1500_OWNPS_CALLS_COMPLETE_NOT_RUNNER_OR_BUSINESS_PROOF';loop_samples=[];all_exits0=True;active_own_ps=[];loop_start=None;budget_before=None;budget_after=None
 def record(label,result,**extra):
  if result.returncode!=0 or not result.stdout.strip().isdigit():raise RuntimeError('original own ps monitor failed: returncode='+str(result.returncode)+' stderr='+result.stderr[:500])
  row=dict(label=label,current_RSS_bytes=int(result.stdout.strip())*1024,ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,allocated_blocks=sys.getallocatedblocks(),subprocess_active_length=len(subprocess._active),own_fd_count=len(os.listdir('/dev/fd')),gc_count=list(gc.get_count()),elapsed_seconds=time.monotonic()-START,**extra)
  loop_samples.append(row);print(json.dumps(row),flush=True)
  if row['ru_maxrss_bytes']>=512*2**20:raise RuntimeError('original SELF512 ceiling reached; stop no retry')
  if time.monotonic()-START>=1800 or(loop_start is not None and time.monotonic()-loop_start>=600):raise RuntimeError('original whole1800/stage600 ceiling reached; stop no retry')
  return row
 try:
  c.verify_rows(fixed);c.verify_rows(owned)
  for row in fixed+owned:assert identity(row['path'])==row['identity'],'current fixed/owned7 before'
  budget_before=resources.check()
  loop_start=time.monotonic()
  for i in range(1,1501):
   result=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
   if result.returncode!=0 or not result.stdout.strip().isdigit():all_exits0=False;raise RuntimeError('original own ps monitor first failure at call'+str(i)+': '+str(result.returncode)+' '+result.stderr[:500])
   completed=i
   if i==1 or i%100==0:record('completed_own_ps_'+str(i),result,completed_calls=i)
   if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-loop_start>=600 or time.monotonic()-START>=1800:raise RuntimeError('original SELF512/stage600/whole1800 ceiling reached; stop no retry')
   if i<1500:time.sleep(0.2)
  c.verify_rows(fixed);c.verify_rows(owned)
  budget_after=resources.check()
  current=subprocess.run(['/bin/ps','-axo','pid=,ppid=,comm='],capture_output=True,text=True,timeout=2)
  if current.returncode!=0:raise RuntimeError('final genuine own child process metadata unavailable')
  for line in current.stdout.splitlines():
   fields=line.strip().split(None,2)
   if len(fields)==3 and int(fields[1])==os.getpid() and Path(fields[2]).name=='ps':active_own_ps.append(dict(pid=int(fields[0]),ppid=int(fields[1]),comm=fields[2]))
  # The inventory may observe its own ps while running. After run waited and
  # closed it, null-signal reads confirm those real own child PIDs no longer
  # exist. A remaining PID is recorded rather than inferred away.
  actually_remaining=[]
  for child in active_own_ps:
   try:os.kill(child['pid'],0)
   except ProcessLookupError:continue
   actually_remaining.append(child)
  active_own_ps=actually_remaining
  if active_own_ps:raise RuntimeError('actual own ps child remains after wait')
 except BaseException as exc:
  status='READONLY_OWNPS_FIRST_ERROR_OR_LIMIT_STOPPED_NO_RETRY';failure=type(exc).__name__+': '+str(exc)
 finally:
  for row in fixed+owned:assert identity(row['path'])==row['identity'],'current fixed/owned7 after'
  for row in list(PF.values()):pin(row['path'],row)
 report=dict(schema='REAL_V11_CURRENT45_BASELINE_ORIGINAL1500_OWN_PS_FORK_MONITOR_MEMORY_MEASUREMENT_V1',status=status,failure=failure,requested_calls=1500,completed_calls=completed,actual_monitor_command=['/bin/ps','-o','rss=','-p',str(os.getpid())],original_capture_output_text_timeout2=True,all1500_calls_original_returncode0_and_waited_closed=completed==1500 and all_exits0,original_monitor_sleep_between_calls_seconds=0.2,
  actual_v11_original45_ledger_pin=ledger_pin,actual_v11_actual_raw_pin=raw_pin,actual_fixed_current_pins=fixed,actual_owned_runtime_pins=owned,current_live_fixed2643_and_owned163_before_after_exact7_and_fullEOF=True,setup_Source_and_existing_metadata_fullpins=list(PF.values()),metadata_setup_measurements=SAMPLES,loop_measurements=loop_samples,
  original_resources_before=budget_before,original_resources_after=budget_after,original_history96GiB_fresh2GiB_cold20971764748_metadata64MiB_free8GiB_constraints_unmodified=True,
  subprocess_active_length_after=len(subprocess._active),final_ps_inventory_observed_own_children=active_own_ps,no_monitor_child_left_running=completed==1500 and all_exits0 and len(subprocess._active)==0,
  explicit_GC_inside_monitor_loop=False,ru_maxrss_reset=False,profiling_enabled=False,all7CLI_current69_original69_admit17_complete_setup_preserved=True,original45_fixed_owned_proofs_cases_release_scratch_catalog_hf_cached_fields_held=True,
  fixture_output_maximum_bytes=8*2**20,original_SELF512_stage600_whole1800_env1_retained=True,original_guard_and_Source_unmodified=True,original_runner_control_executed=False,Dragon_or_solver_or_new_business_executed=False,physical_inputs_copied_or_deleted=False,observed_v11_SELF548_failure_explained=False,v12_fix_claimed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(own/'REVIEW.json',report)
 size_output=sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file());assert size_output<=8*2**20,'diagnostic namespace exceeds8MiB'
 print(json.dumps(dict(status=status,failure=failure,completed_calls=completed,review_pin=pin(own/'REVIEW.json'),fixture_bytes_before_true_returns=size_output),allow_nan=False),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

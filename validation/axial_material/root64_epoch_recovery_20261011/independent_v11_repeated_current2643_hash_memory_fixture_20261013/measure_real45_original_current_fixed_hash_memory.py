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
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('actual-fixed2643-20',),required=True);args=parser.parse_args()
 own=HERE/args.mode;own.mkdir();status='READONLY_FIXTURE_COMPLETE_NOT_BUSINESS_PROOF';failure=None
 pin(__file__);pin(REC/'independent_v11_resource_serialization_memory_fixture_20261013/measure_original_resources_and_prefix_serialization.py')
 if sys.flags.optimize or any(os.environ.get(k)!='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')):raise RuntimeError('original nonoptimized env1 required')
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
 # Isolate original repeated full hashing. No copy, resource.scan, dump,
 # child, candidate import, numerical work, or original Source patch.
 assert len(fixed)==2643 and len(owned)==163 and len(records)==45
 for row in fixed+owned:assert identity(row['path'])==row['identity'],'actual fixed/owned must remain current live all7'
 baseline=None;rounds=0;failure=None;status='READONLY_20_FIXED_HASH_ROUNDS_COMPLETE_NOT_BUSINESS_PROOF'
 try:
  c.verify_rows(owned)
  n=gc.collect();baseline=metric('all163_owned_preverified_real45_baseline',collected=n,fixed_count=2643,owned_count=163,fixed_bytes=sum(p['size_bytes']for p in fixed),owned_bytes=sum(p['size_bytes']for p in owned),retained_state_heap_bytes=size([records,fixed,owned,proofs,cases,release,scratch,cached,hf,catalog,history.__dict__,resources.__dict__])[0])
  for i in range(1,21):
   metric('before_original_fixed_hash_'+str(i),completed_rounds=rounds)
   c.verify_rows(fixed);rounds=i
   after=metric('after_original_fixed_hash_'+str(i),completed_rounds=rounds)
   if max(after['current_RSS_bytes']-baseline['current_RSS_bytes'],after['ru_maxrss_bytes']-baseline['ru_maxrss_bytes'])>=100*2**20:raise RuntimeError('readonly original hashing grew by at least100MiB; stop subsequent rounds without retry')
   n=gc.collect();metric('after_explicit_gc_fixed_hash_'+str(i),collected=n,completed_rounds=rounds)
  c.verify_rows(owned);metric('all163_owned_postverified')
 except BaseException as exc:
  status='READONLY_HASH_LIMIT_OR_INPUT_REFUSAL_STOPPED_NO_RETRY';failure=type(exc).__name__+': '+str(exc)
 finally:
  for row in fixed+owned:assert identity(row['path'])==row['identity'],'current fixed/owned7 changed'
  for row in PF.values():assert identity(row['path'])==row['identity'],'Source or baseline metadata identity changed'
 report=dict(schema='REAL_V11_CURRENT2643_REPEATED_ORIGINAL_FILE_DIGEST_MEMORY_MEASUREMENT_V1',status=status,failure=failure,maximum_rounds=20,completed_original_fixed_verify_rounds=rounds,actual_v11_raw_pin=raw_pin,actual_original45_ledger_pin=ledger_pin,
  actual_fixed_current_pins=fixed,actual_owned_runtime_pins=owned,all_fixed_and_owned_initially_current_live_exact7=True,historical_released_PF_not_treated_as_current_inputs=True,
  original_common_verify_rows_and_hashlib_file_digest_unmodified=True,all7_real_CLI_and_current69_original69_admit17_exact_setup_preserved=True,original_catalog_and_small_hf_cached_fields_and45records_preserved=True,
  original_resources_and_phase_classes_constructed_without_copy_or_scan=True,measurements=SAMPLES,baseline=baseline,full_EOF_fixed_bytes_per_round=sum(p['size_bytes']for p in fixed),complete_own_setup_input_pins=list(PF.values()),
  own_ru_maxrss_never_reset=True,SELF512_whole1800_env1_retained=True,stop_on100MiB_growth_no_retry=True,compiler_or_solver_or_CLE_or_pipeline_business_started=False,physical_input_copied=False,physical_input_deleted=False,original_Source_changed=False,
  observed_v11_SELF548_failure_explained=False,v12_fix_claimed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(own/'REVIEW.json',report);row=pin(own/'REVIEW.json');print(json.dumps(dict(status=status,failure=failure,completed_rounds=rounds,review_pin=row),allow_nan=False),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

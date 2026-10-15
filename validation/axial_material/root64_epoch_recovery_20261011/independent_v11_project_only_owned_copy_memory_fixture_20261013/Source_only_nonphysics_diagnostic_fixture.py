"""Existing-metadata memory fixture only. No pipeline import/child/science work.

Original resource classes and original dump_json remain unmodified. Writes only
own diagnostic prefixes, never business records; original source/evidence reach
EOF before and retain every SHA/identity after measurement. Peak RSS is not reset.
"""
import argparse,ast,gc,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11')
HERE=REC/'independent_v11_project_only_owned_copy_memory_fixture_20261013'
FIXTURE=Path('/Users/wen/spot/validation/artifacts/axial-material-v11-project-only-owned-copy-metadata-diagnostic-20261013')
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
 original_shutil_module=pin(Path(shutil.__file__))
 actual_raw=json.loads(rawpath.read_bytes())
 project=next(p for p in actual_raw['owned_runtime_pins']if p['path']==str(OUT/'AAA/projected_boot.xsm'))
 a1=next(p for p in actual_raw['fixed_current_pins']if p['path']=='/Users/wen/spot/validation/artifacts/axial-material-new-REAL64-native-warm-A-20261012-v3/A/new_native_A.xsm')
 assert project['size_bytes']==749355952 and a1['size_bytes']==156880856
 del actual_raw;gc.collect();pin(project['path'],project);pin(a1['path'],a1)
 baseline=metric('same_admitted_metadata_closed_raw45_before_owned_copy')
 receipts=[];status='NONPHYSICS_OWNED_COPY_MEMORY_DIAGNOSTIC_COMPLETE';failure=None;stopped_on_growth=False
 def realmetric(label,**kw):
  p=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
  assert p.returncode==0 and p.stdout.strip().isdigit(),'real own parent ps unavailable'
  v=dict(label=label,current_RSS_bytes=int(p.stdout.strip())*1024,ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START,gc_count=list(gc.get_count()),allocated_blocks=sys.getallocatedblocks(),**kw);SAMPLES.append(v);return v
 try:
  for label,sourcepin in [('PROJECT_1',project),('PROJECT_2',project),('PROJECT_3',project)]:
   target=FIXTURE/'diagnostic'/'projected_boot.xsm';assert not os.path.lexists(target)
   pin(sourcepin['path'],sourcepin);c.same_pin(sourcepin['path'],sourcepin);resources.check();before=realmetric('before_'+label)
   if before['ru_maxrss_bytes']>=512*2**20 or time.monotonic()-START>=1800:raise RuntimeError('original SELF512 or whole1800 before finite copy')
   shutil.copy2(sourcepin['path'],target);after_copy=realmetric('after_original_shutil_copy2_'+label)
   actual=c.pin(target);assert pin(target)==actual
   assert actual['sha256']==sourcepin['sha256']and actual['size_bytes']==sourcepin['size_bytes']and actual['identity'][:2]!=sourcepin['identity'][:2]and actual['identity'][3]==1
   assert stat.S_ISREG(actual['identity'][2])and target.lstat().st_uid==os.getuid()and target.parent==FIXTURE/'diagnostic'and not target.is_symlink()
   assert all(q['identity'][:2]!=actual['identity'][:2]for q in fixed)
   after_pin=realmetric('after_original_c_pin_full_EOF_'+label)
   during=resources.check();assert during['fresh_output']['artifact_bytes']>=actual['size_bytes']
   pin(sourcepin['path'],sourcepin);c.same_pin(sourcepin['path'],sourcepin)
   # Sole authorized cleanup: this fresh, fully EOF-pinned, closed-reader clone.
   assert c.pin(target)==actual and identity(target)==actual['identity'];target.unlink();assert not os.path.lexists(target);PF.pop(str(target))
   after_delete=realmetric('after_only_own_clone_release_'+label);collected=gc.collect();after_gc=realmetric('after_'+label+'_explicit_gc',collected=collected)
   resources.check();pin(sourcepin['path'],sourcepin)
   growth=max(after_copy['ru_maxrss_bytes'],after_pin['ru_maxrss_bytes'],after_delete['ru_maxrss_bytes'],after_gc['ru_maxrss_bytes'])-baseline['ru_maxrss_bytes']
   record=dict(label=label,explicitly_nonphysics_copy_fixture=True,source_fullpin=sourcepin,original_shutil_copy2_called_once=True,original_Common_pin_whole_EOF_called=True,actual_closed_EOF_owned_clone_pin=actual,independent_inode=True,owned_regular_singlelink=True,source_fullSHA_all7ID_unchanged=True,only_this_own_clone_released=True,clone_now_absent=True,full_EOF_reader_closed_before_unlink=True,before=before,after_copy=after_copy,after_original_pin=after_pin,after_release=after_delete,after_explicit_gc=after_gc,actual_peak_growth_from_baseline_bytes=growth,actual_original_resources_while_clone_live=during,physics_or_science_control_qualification=False)
   receipt_path=FIXTURE/('DIAGNOSTIC_ONLY_'+label+'_EXACT_OWN_COPY_RELEASE_RECEIPT.json');write(receipt_path,record);receipt_pin=pin(receipt_path);record['diagnostic_receipt_pin']=receipt_pin;receipts.append(record)
   if after_gc['ru_maxrss_bytes']>=512*2**20 or time.monotonic()-START>=1800:raise RuntimeError('original SELF512 or whole1800 finite copy diagnostic refusal')
   if growth>=100*2**20:status='NONPHYSICS_COPY_DIAGNOSTIC_STOPPED_AFTER_ACTUAL_LARGE_GROWTH';stopped_on_growth=True;break
 except BaseException as exc:status='NONPHYSICS_COPY_DIAGNOSTIC_LIMIT_OR_ERROR_REFUSAL';failure=type(exc).__name__+': '+str(exc)
 pin(project['path'],project);pin(a1['path'],a1);assert records==json.loads(stagepath.read_bytes())['stages']and len(records)==45
 for q in list(PF.values()):
  if q['path']==str(FIXTURE/'diagnostic/projected_boot.xsm'):
   if os.path.lexists(q['path']):pin(q['path'],q)
   continue
  pin(q['path'],q)
 outputs=[pin(p)for p in sorted(FIXTURE.rglob('*'))if p.is_file()];actual_bytes=sum(q['size_bytes']for q in outputs);after=resources.check()
 assert after['fresh_output']['artifact_bytes']==actual_bytes and after['fresh_output']['regular_files']==len(outputs)
 final=realmetric('copy_diagnostic_final')
 report=dict(schema='REAL_ORIGINAL_PROJECT_ONLY_SHUTIL_COPY2_AND_COMMON_PIN_OWNED_RELEASE_MEMORY_FIXTURE_V1',status=status,failure=failure,namespace=str(FIXTURE),actual_copy_receipts=receipts,actual_copy_count=len(receipts),A1_copy_deliberately_not_retried=True,PROJECT_points_only=True,actual_A1_source_pin=a1,actual_PROJECT_source_pin=project,actual_original_shutil_module_pin=original_shutil_module,only_owned_diagnostic_clones_released=True,source_never_deleted_or_modified=True,source_all_SHA_seven_field_identity_unchanged=True,whole_original45_raw_resource_records_preserved=True,actual_original_stage_ledger_pin=ledger_pin,actual_original_raw_record_pin=raw_pin,all_actual_parent_measurements=SAMPLES,metadata_closed_raw45_baseline=baseline,last_actual_parent_metric=final,stopped_after_100MiB_actual_growth=stopped_on_growth,retained_diagnostic_output_full_EOF_pins=outputs,actual_retained_diagnostic_ART_bytes=actual_bytes,actual_original_resources_after=after,original_Source_and_existing_metadata_fullpins=[p for p in PF.values()if not p['path']==str(FIXTURE/'diagnostic/projected_boot.xsm')],original_c_pin_copy2_resource_classes_and_caps_unmodified=True,original_SELF_child_stage_whole_history_fresh_cold_free_caps_unchanged=True,original_MRO_unmodified=True,original_numerical_execution_records=[],actual_scientific_control_stage_count=0,no_retry=True,profile_disabled=True,ru_maxrss_never_reset=True,new_pipeline_Source_or_v7_Source_modified=False,compiler_or_CLE_or_solver_or_physics_or_pipeline_business_started=False,SELF_review_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START,engineering_three_plane_closed0=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(HERE/'REVIEW.json',report)
 print(json.dumps(dict(status=status,failure=failure,review_pin=pin(HERE/'REVIEW.json'),actual_copy_count=len(receipts),baseline_RSS=baseline['current_RSS_bytes'],baseline_peak=baseline['ru_maxrss_bytes'],final_RSS=final['current_RSS_bytes'],final_peak=final['ru_maxrss_bytes'],copy_points=[dict(label=x['label'],copy_RSS=x['after_copy']['current_RSS_bytes'],copy_peak=x['after_copy']['ru_maxrss_bytes'],pin_RSS=x['after_original_pin']['current_RSS_bytes'],pin_peak=x['after_original_pin']['ru_maxrss_bytes'],GC_RSS=x['after_explicit_gc']['current_RSS_bytes'],GC_peak=x['after_explicit_gc']['ru_maxrss_bytes'],growth_bytes=x['actual_peak_growth_from_baseline_bytes'])for x in receipts],actual_retained_diag_ART_bytes=actual_bytes,wall_seconds=report['elapsed_seconds'])),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

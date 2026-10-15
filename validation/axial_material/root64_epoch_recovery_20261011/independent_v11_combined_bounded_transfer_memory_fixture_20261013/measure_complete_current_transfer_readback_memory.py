"""Existing-metadata memory fixture only. No pipeline import/child/science work.

Original resource classes and original dump_json remain unmodified. Writes only
own diagnostic prefixes, never business records; original source/evidence reach
EOF before and retain every SHA/identity after measurement. Peak RSS is not reset.
"""
import argparse,ast,contextlib,gc,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
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
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('combined-current-readback',),required=True);args=parser.parse_args()
 own=HERE/args.mode;own.mkdir();status='READONLY_FIXTURE_COMPLETE_NOT_BUSINESS_PROOF';failure=None
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
 history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(OUT)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 fresh=production.DiskResources(c.ART,[str(OUT)],8*2**30,2*2**30)
 # Extract exact class declarations only. Never import candidate pipeline or
 # execute initialize/main, alter original classes or replace serialization.
 commontext=Path(c.__file__).read_text();ct=ast.parse(commontext);initialize=next(n for n in ct.body if isinstance(n,ast.FunctionDef)and n.name=='initialize');resourceclass=next(n for n in initialize.body if isinstance(n,ast.ClassDef)and n.name=='Resources')
 env={'history':history,'fresh':fresh};exec(compile(ast.Module(body=[resourceclass],type_ignores=[]),'<exact original Resources class declaration>','exec'),env);original_resources=env['Resources']()
 host=REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py';pin(host);hosttext=host.read_text();ht=ast.parse(hosttext);phaseclass=next(n for n in ht.body if isinstance(n,ast.ClassDef)and n.name=='PhaseResources')
 penv={'Path':Path,'WORK':OUT/'AAA','OUT':OUT,'MI':2**20};exec(compile(ast.Module(body=[phaseclass],type_ignores=[]),'<exact original PhaseResources class declaration>','exec'),penv);resources=penv['PhaseResources'](original_resources);resources.phase='BOOT_storage_controls'
 metric('exact_original_resource_classes_constructed',history_own_keys=list(history.__dict__),phase_own_keys=list(resources.__dict__))

 source=REC/'aaa_three_plane_streaming_pipeline_source_v11/actual_inputs_and_readback.py';data=module(source,'diagnostic_original_v11_passive_data_reader');pin(data.PARSER)
 plan,_=c.read_bound_json_current(data.PLAN,c.pin(data.PLAN));pin(data.PLAN)
 project=OUT/'AAA/projected_boot.xsm';transfer=proofs[1]['actual_tree_proof'];packed=proofs[0]['actual_full_items'];pin(project,proofs[1]['project_full_pin'])
 assert len(packed)==18 and len(transfer['original_three_planes'])==18 and len(transfer['independent_six_contexts'])==6
 input_paths=[project]+[Path(row['archive']['path'])for row in plan['producers']]
 contexts={'AX':'ax_current.xsm','AXTRACK':'axial_track.xsm','AXSYSTEM':'initial_system.xsm','AXMACRO':'axial_macro.xsm','RCON':'global_rcon.xsm'}
 input_paths += [OUT/'AAA'/name for name in contexts.values()]
 for p in input_paths:pin(p)
 metric('complete_passive_reader_plan_and_current_inputs_admitted',preserved_state_heap_bytes=size([records,fixed,proofs,cases,release,scratch,cached,hf,catalog,plan])[0])
 result=[];failure=None;status='READONLY_CURRENT_RETAINED_TRANSFER_AND_ALL18_ORIGINAL_TREES_CLOSED_NOT_BUSINESS_PROOF'
 try:
  with contextlib.ExitStack()as stack:
   a=stack.enter_context(data._open_xsm(project));pg=data.node(a,a.root,['GLOBAL64']);archive=data.node(a,pg,['ARCHIVE'])
   original_readers=[]
   for row in plan['producers']:
    pin(row['archive']['path'],row['archive']);original_readers.append(stack.enter_context(data._open_xsm(row['archive']['path'])))
   context_readers={name:stack.enter_context(data._open_xsm(OUT/'AAA'/filename))for name,filename in contexts.items()}
   metric('all9_current_input_descriptors_opened_together')
   digest=data.tree_digest(a,pg);assert digest==transfer['complete_global'];result.append(dict(scope='retained_PROJECT/GLOBAL64',digest=digest,equals_original_independent_transferred_GLOBAL_proof=True))
   metric('complete_retained_GLOBAL64_digest',leaves=digest['leaves'],payload_bytes=digest['bytes'])
   digest=data.tree_digest(a,archive);assert digest==transfer['complete_archive']==transfer['retained_complete_archive'];result.append(dict(scope='retained_PROJECT/GLOBAL64/ARCHIVE',digest=digest,equals_original_independent_PACK_and_retained_ARCHIVE_proofs=True))
   metric('complete_retained_ARCHIVE_digest',leaves=digest['leaves'],payload_bytes=digest['bytes'])
   for plane,b in enumerate(original_readers,1):
    for field in ['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND']:
     digest=data.exact_tree(a,data.node(a,archive,[field,plane]),b,data.node(b,b.root,[field,1]))
     assert digest==next(x['complete_tree']for x in packed if(x['plane'],x['field'])==(plane,field))
     assert digest==next(x['complete_tree']for x in transfer['original_three_planes']if(x['plane'],x['field'])==(plane,field))
     result.append(dict(scope='all18_independent_original_plane_fields',plane=plane,field=field,digest=digest,equals_both_original_pack_and_transfer_proofs=True))
    metric('all6_original_plane_fields_'+str(plane),digests_completed=len(result))
   for name,b in context_readers.items():
    digest=data.exact_tree(a,data.node(a,pg,[name]),b,b.root)
    assert digest==next(x['complete_tree']for x in transfer['independent_six_contexts']if x['field']==name)
    result.append(dict(scope='retained_PROJECT_vs_independent_current_context',field=name,digest=digest))
    metric('complete_current_context_'+name,leaves=digest['leaves'],payload_bytes=digest['bytes'])
   metric('all_current_contexts_complete_while_all9_fds_open')
  metric('all9_fd_contexts_closed_before_gc',total_verified_tree_digests=len(result),retained_digest_heap_bytes=size(result)[0])
  collected=gc.collect();metric('after_explicit_gc_at_complete_current_readback',collected_objects=collected)
  assert len(result)==25
 except BaseException as error:status='READONLY_COMBINED_TREE_MEMORY_REFUSED_OR_DATA_MISMATCH';failure=type(error).__name__+': '+str(error)
 finally:
  for p in PF.values():assert pin(p['path'])==p,'all original Source/current data fullEOF7 changed'
 report=dict(schema='REAL_CURRENT_RETAINED_TRANSFER_COMBINED_BOUNDED_READER_MEMORY_FIXTURE_V1',status=status,failure=failure,
  actual_original45_stage_ledger_pin=ledger_pin,actual_original45_raw_record_pin=raw_pin,all_current_input_fullpins=[PF[str(p)]for p in input_paths],
  original_Source_and_metadata_fullpins=list(PF.values()),measurements=SAMPLES,all25_complete_logical_current_tree_proofs=result,
  exact_existing_data_helper_node_tree_digest_exact_tree_and_ExitStack_only=True,wholePROJECT_unrelated_deleted_record_directories_not_traversed=True,
  actual_original_PACK_GLOBAL_physical_files_are_released_not_current_reissued=True,
  original_PACK_GLOBAL_historical_fullpins_for_provenance_only=[proofs[1]['pack_full_pin'],proofs[1]['global_full_pin']],
  original_PACK_GLOBAL_byte_replay_not_claimed=True,current_retained_subtrees_compared_to_true_independent_pre_release_logical_proofs=True,
  no_mmap_no_math_no_changed_group_type_or_payload=True,all_Source_and_data_files_unmodified_and_no_data_files_written_or_deleted=True,
  original_guard_MRO_and_all_memory_storage_wall_limits_unchanged=True,ru_maxrss_not_reset=True,
  scalar_terminal_math_MT_parser_or_solver_or_physics_or_pipeline_business_not_executed=True,
  actual_v11_after50_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 write(own/'REVIEW.json',report);print(json.dumps(dict(status=status,failure=failure,review_pin=pin(own/'REVIEW.json'),all25_tree_comparisons_completed=len(result)==25,
  final_RSS_bytes=SAMPLES[-1]['current_RSS_bytes'],true_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),allow_nan=False),flush=True)
 if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()

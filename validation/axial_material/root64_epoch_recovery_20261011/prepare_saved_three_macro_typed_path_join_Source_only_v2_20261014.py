"""Only Source preparation for the already-saved exact typed-path comparison."""
import ast,base64,hashlib,json,os
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=REC/'saved_three_macro_exact_typed_path_join_source_v1_20261014'
OLD=REC/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014'
ART=Path('/Users/wen/spot/validation/artifacts')
def pin(p):
 p=Path(p);s=p.stat();b=p.read_bytes();ids=lambda z:[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
 if s.st_size>64*2**20 or ids(p.stat())!=ids(s):raise RuntimeError('bounded Source/metadata current7')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def write(p,v):
 b=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def read(p):return json.loads(Path(p).read_bytes())
CHILD=r'''"""One bounded comparison of existing typed SQLite indices and original byte pools."""
import argparse,hashlib,importlib.util,itertools,json,os,sys
from pathlib import Path
BASE=Path(__file__).absolute().parent
from current_material_lineage_evidence import Budget,admit_owning_stage,check,pin,read,require,strict,FALSE
import saved_native_data_access_adapter as adapter
def current7(expected):
 p=Path(expected['path']);s=p.lstat();require(not any(a.is_symlink()for a in(p,*p.parents))and[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==expected['identity'],'original physical archive current7 only; no new decode')
def under(saved,prefix):
 for value in saved.iter_all():
  if tuple(value['record']['path'][:len(prefix)])==prefix:yield value
def keys(saved,prefix):
 result=set()
 for value in under(saved,prefix):
  original=value['record']['path'];canonical=original if prefix==('MACROLIB',)else original[2:]
  require(canonical[:1]==['MACROLIB'],'only exact native MICROLIB2,1,MACROLIB prefix normalized')
  key=adapter.path_key(canonical);require(key not in result,'unique canonical typed path, no record overwritten');result.add(key)
 return result
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);args=ap.parse_args()
 require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None,'genuine owning parent/unprofiled unoptimized child')
 require(all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'original single thread')
 bindingpin=strict(args.binding_pin);binding=read(bindingpin,lambda:None)
 require(binding['schema']=='ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_BINDING_V1','one exact saved-pair operation')
 budget=Budget(binding['joint_archive_roots'],binding['explicit_cumulative_metadata_file_pins']);budget.check()
 for p in binding['source_file_pins']:check(p,budget.check)
 out=Path(binding['child_output_directory']);require(out.is_dir()and not any(out.iterdir()),'fresh owned comparison subdirectory')
 temp=out/'sqlite_temp';temp.mkdir();pair=binding['observed_pair']
 saved=adapter.SavedNativeInput(pair['sqlite_pin'],pair['native_pool_pin'],temp,budget.check);reports=[]
 try:
  observed_keys=keys(saved,('MACROLIB',));require(len(observed_keys)==binding['expected_macro_record_count'],'all original19620 records including typed root')
  for plane,row in enumerate(binding['native_pairs'],1):
   require(row['plane']==plane,'original three plane order');producer=binding['original_native_producers'][plane-1]
   require(row['archive_pin']==producer['archive_pin'],'same original physical producer')
   current7(row['archive_pin']);admit_owning_stage(producer['actual_report_pin'],producer['actual_solve_label'],producer['actual_solve_command'],budget.check)
   native=adapter.SavedNativeInput(row['sqlite_pin'],row['native_pool_pin'],temp,budget.check)
   try:
    native_keys=keys(native,('MICROLIB2',1,'MACROLIB'))
    require(native_keys==observed_keys,'complete bidirectional typed path inventories, no dropped or invented record')
    count=words=word_mismatches=metadata_mismatches=0;detail=out/('A'+str(plane)+'_canonical_macro_comparison.jsonl')
    with detail.open('x')as output:
     # Preserve the observed API/physical order; lookup does not sort either archive.
     for value in under(saved,('MACROLIB',)):
      budget.check();a=value['record'];right_path=['MICROLIB2',1]+a['path'];b=native.row(right_path)
      require(b is not None,'exact typed native path lookup')
      right_info=native.db.execute('SELECT ordinal,api_key FROM records WHERE key=?',(adapter.path_key(right_path),)).fetchone();require(right_info is not None,'original native physical/API ordinal retained')
      meta=a['path_types']==b['path_types'][2:]and all(a[k]==b[k]for k in('kind','declared_count','original_word_count'))
      nwords=ndiff=0
      for aa,bb in itertools.zip_longest(saved.iter_raw(a),native.iter_raw(b),fillvalue=b''):
       budget.check();nwords+=max(len(aa),len(bb))//4
       ndiff+=sum(aa[i:i+4]!=bb[i:i+4]for i in range(0,max(len(aa),len(bb)),4))
      count+=1;words+=nwords;word_mismatches+=ndiff;metadata_mismatches+=int(not meta)
      item=dict(canonical_path=a['path'],kind=a['kind'],declared_count=a['declared_count'],original_word_count=a['original_word_count'],metadata_equal=meta,raw_word_mismatches=ndiff,compared_words=nwords,observation_payload_SHA=a['native_payload_sha256'],archive_payload_SHA=b['native_payload_sha256'],original_observation_ordinal=value['physical_ordinal'],original_observation_api_key=value['api_key'],original_archive_ordinal=right_info[0],original_archive_api_key=right_info[1])
      output.write(json.dumps(item,separators=(',',':'),allow_nan=False)+'\n')
     output.flush();os.fsync(output.fileno())
    require(count==len(observed_keys)==len(native_keys),'all records compared once, including root')
    current7(row['archive_pin']);reports.append(dict(plane=plane,compared_all_macro_records=count,compared_original_payload_words=words,raw_word_mismatches=word_mismatches,metadata_mismatches=metadata_mismatches,path_sets_equal=True,all_original_records_and_typed_root_preserved=True,original_archive_not_redecoded=True,original_orders_not_sorted_or_rewritten=True,detail_pin=pin(detail,budget.check),native_sqlite_pin=row['sqlite_pin'],native_pool_pin=row['native_pool_pin']))
   finally:native.close()
 finally:saved.close()
 report=out/'ACTUAL_SAVED_THREE_MACRO_CANONICAL_PATH_COMPARISONS.json'
 value=dict(schema='ACTUAL_SAVED_THREE_MACRO_CANONICAL_PATH_RAW_WORD_COMPARISON_V1',original_failed_compare_authority_pins=binding['original_failed_compare_authority_pins'],original_Root_exit_code_retained=1,original_positional_mismatch_report_not_modified=True,observed_pair=pair,comparisons=reports,all_raw_word_mismatches=sum(r['raw_word_mismatches']for r in reports),all_metadata_mismatches=sum(r['metadata_mismatches']for r in reports),all_three_original_producer_seals_preserved=True,comparison_contract='EXACT_TYPED_FULL_PATH_KIND_COUNT_WORDS_AND_ALL_RAW_BYTES',**FALSE)
 with report.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 check(bindingpin,budget.check);budget.check();print(json.dumps(dict(status='ACTUAL_SAVED_THREE_TYPED_PATH_COMPARISONS_CLOSED_ONLY_EXIT2',report=pin(report,budget.check),**FALSE)),flush=True);raise SystemExit(2)
if __name__=='__main__':main()
'''
HOST=r'''"""Original one-child OwnRSS guard around the existing saved-pair comparison."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';BASE=Path(__file__).absolute().parent
FALSE=dict(physics_qualified=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def metadata(p):
 q=Path(p['path']);s=q.lstat();require(identity(s)==p['identity']and stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in(q,*q.parents)),'exact ordinary metadata current7')
 raw=q.read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256']and identity(q.lstat())==p['identity'],'whole metadata bytes/current7');return json.loads(raw)
def load_source(p,name):
 metadata_bytes=Path(p['path']).read_bytes();require(hashlib.sha256(metadata_bytes).hexdigest()==p['sha256']and identity(Path(p['path']).lstat())==p['identity'],'whole exact original guard Source')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();start=time.monotonic()
 def arg(role):
  n=role.replace('-','_');p=Path(getattr(a,n+'_summary'));value=dict(path=str(p),sha256=getattr(a,n+'_sha256'),identity=json.loads(getattr(a,n+'_seven_id')),size_bytes=p.stat().st_size);return metadata(value),value
 sf,psf=arg('source-freeze');hf,phf=arg('host-freeze')
 require(sf['schema']=='COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute()),'exact Source-only saved-pair host')
 require(hf['actual_duplicate_physical_release_proof_pin']is not None and hf['actual_duplicate_physical_release_Root_tool_pin']is not None,'unknown future exact duplicate release cannot initialize')
 plan=metadata(sf['control_plan_pin']);release=metadata(hf['actual_duplicate_physical_release_proof_pin']);root=metadata(hf['actual_duplicate_physical_release_Root_tool_pin']);terminal=root['actual_terminal_return']
 require(type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None and root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==0,'actual closed duplicate-release Root0 retained')
 require(release['schema']==hf['actual_duplicate_release_schema']and all(contains(release,p)and not os.path.lexists(p['path'])for p in plan['historical_A2_A3_physical_pins']),'only the two exact historical physical duplicates have been released')
 c=load_source(plan['original_Common_Source_pin'],'saved_typed_path_original_common');support=load_source(plan['original_support_Source_pin'],'saved_typed_path_original_support')
 require(Path(sys.executable).resolve()==support.PYTHON and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original Python/unoptimized/unprofiled/single-thread environment')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'saved_typed_path_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'saved_typed_path_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine original OwnRSS class/MRO')
 out=Path(plan['planned_actual_output_root']);require(out.parent==c.ART and not os.path.lexists(out),'fresh single output namespace')
 roots=plan['complete_joint_roots'];joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure).check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original complete-family fullfresh2/cold/meta history96 reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-start<1800,'original SELF512/whole1800')
   h=history.check();f=joined.check();extra=0
   require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original cold/history96/free8 reserves')
   for p in plan['explicit_cumulative_metadata_file_pins']:
    require(identity(Path(p['path']).lstat())==p['identity'],'explicit metadata current7')
    if not any(Path(p['path']).is_relative_to(Path(v))for v in roots):extra+=p['size_bytes']
   require(f['artifact_bytes']+extra<2*2**30,'unchanged cumulative root2GiB plus exact external metadata')
   return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,complete_joint_bytes=f['artifact_bytes']+extra,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files]);c.same_pin(plan['retained_A1_physical_pin']['path'],plan['retained_A1_physical_pin'])
 out.mkdir();(out/'runtime').mkdir();(out/'saved-compare').mkdir();(out/'comparison').mkdir();shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
 require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copied')
 binding=dict(schema='ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_BINDING_V1',observed_pair=plan['observed_pair'],native_pairs=plan['native_pairs'],original_native_producers=plan['original_native_producers'],source_file_pins=sf['complete_source_file_pins'],joint_archive_roots=roots,explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],expected_macro_record_count=19620,original_failed_compare_authority_pins=plan['original_failed_compare_authority_pins'],child_output_directory=str(out/'comparison'),**FALSE)
 bindingpath=out/'ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_BINDING.json';c.write(bindingpath,binding);pb=c.pin(bindingpath);owned.append(pb)
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'saved-compare',resources);require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources,'original actual owning guard')
 first=FirstFailure();watchpin=logpin=childpin=None;after=None;verified=False
 def check_all():
  for p in fixed:
   if p in plan['data_pair_pins']:require(identity(Path(p['path']).lstat())==p['identity'],'saved pair current7')
   else:c.same_pin(p['path'],p)
  for p in owned:c.same_pin(p['path'],p)
  return resources.check()
 try:
  check_all();error=None
  try:runner.execute(out/'saved-compare','typed_path_raw_word_compare',[str(support.PYTHON),sf['child_source_pin']['path'],'--binding-pin',json.dumps(pb,separators=(',',':')),'--expected-parent-pid',str(os.getpid())],600)
  except RuntimeError as caught:error=str(caught)
  require(error=='own-child stage failed; no retry'and len(runner.records)==1,'original intentional evidence exit2, no retry');record=runner.records[0];watchpin=c.pin(out/(record['label']+'.watchdog.json'));logpin=c.pin(out/(record['label']+'.log'));watch=metadata(watchpin)
  require(type(watch['returncode'])is int and watch['returncode']==2 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['sampled_peak_rss_mib']<512,'genuine child2/noLimit/caps')
  lines=Path(logpin['path']).read_text().splitlines();require(len(lines)==1,'one exact complete child receipt');receipt=json.loads(lines[0]);require(receipt['status']=='ACTUAL_SAVED_THREE_TYPED_PATH_COMPARISONS_CLOSED_ONLY_EXIT2','same saved-pair child scope');childpin=receipt['report'];value=metadata(childpin)
  require(value['schema']=='ACTUAL_SAVED_THREE_MACRO_CANONICAL_PATH_RAW_WORD_COMPARISON_V1'and len(value['comparisons'])==3 and all(row['compared_all_macro_records']==19620 and row['path_sets_equal']is True for row in value['comparisons']),'all three original complete typed scopes');after=check_all();verified=True
 except BaseException as e:first.capture(e,'compare_or_close')
 try:after=check_all()
 except BaseException as e:first.capture(e,'after_check')
 good=verified and first.error is None;target=out/'Root_actual_saved_three_macro_typed_path_comparison_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_ROOT_GUARDED_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_V1',status='ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_EXIT2_CLOSED_ONLY'if good else'ACTUAL_SAVED_COMPARISON_FAILED_NO_RETRY',failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=runner.records,actual_watchdog_full_pin=watchpin,actual_log_full_pin=logpin,actual_child_report_pin=childpin,fixed_current_pins=fixed,complete_output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],resources_before=before,resources_after=after,original_Root_exit_code_retained=1,original_failed_compare_authority_pins=plan['original_failed_compare_authority_pins'],old_positional_reports_not_modified=True,original_archives_not_redecoded=True,original_guard_class_MRO_unchanged=True,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as e:
  first.capture(e,'publication')
  if summary is not None and target.exists():
   try:summary.update(status='ACTUAL_SAVED_COMPARISON_FAILED_NO_RETRY',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'complete factual saved-pair comparison');print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()
'''
def main():
 if BASE.exists():raise RuntimeError('fresh Source-only namespace')
 postpath=REC/'independent_compare_three_v7_actual_failure_facts_postverify_20261014/REVIEW.json';post=read(postpath);child=read(post['actual_aggregate_report_pin']['path']);request=read(post['actual_request_pin']['path'])
 if post['schema']!='INDEPENDENT_COMPARE_THREE_V7_ACTUAL_FAILURE_FACTS_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_COMPARE_THREE_V7_FAILURE_FACTS_POSTVERIFICATION'or post['failure']is not None or post['actual_Root_integer_exit_code']!=1:raise RuntimeError('actual immutable failed compare source authority')
 pairs=[];phys=[]
 for row in child['comparisons']:
  files={Path(p['path']).name:p for p in row['all_output_pins']};pairs.append(dict(plane=row['plane'],archive_pin=row['archive_pin'],sqlite_pin=files['original_archive_index.sqlite'],native_pool_pin=files['original_words.bin']));phys.append(files['physical.jsonl'])
 for p in [request['observed_final_A_pair']['sqlite_pin'],request['observed_final_A_pair']['native_pool_pin']]+[p for row in pairs for p in(row['sqlite_pin'],row['native_pool_pin'])]:
  s=Path(p['path']).lstat()
  if[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=p['identity']:raise RuntimeError('actual saved pair current7 only; no body read')
 model=Path(REC/'bq64_private_GANLIB_model_control_host_source_v5_20261013/run_guarded_model_controls.py').read_text();tree=ast.parse(model);borrowed=[]
 for name in('rewrite_summary','unique','safe_repr','FirstFailure'):
  node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name);borrowed.append(dict(name=name,original_source_line=node.lineno,whole_bytes=ast.get_source_segment(model,node)))
 host=HOST.replace('def main():\n','\n\n'.join(v['whole_bytes']for v in borrowed)+'\n\ndef main():\n',1)
 ast.parse(host);ast.parse(CHILD);BASE.mkdir();hostpin=write(BASE/'run_saved_three_macro_typed_path_compare_original_guard.py',host.encode());childpin=write(BASE/'compare_saved_three_macro_exact_typed_path_words.py',CHILD.encode())
 code=[]
 for before,name in[(OLD/'current_material_lineage_evidence.py','current_material_lineage_evidence.py'),(OLD/'saved_native_data_access_adapter.UNREADY.py','saved_native_data_access_adapter.py')]:code.append(dict(original_Source_pin=pin(before),candidate_Source_pin=write(BASE/name,before.read_bytes()),whole_bytes_unchanged=True))
 control=read(REC/'OVERV_original_guarded_integer_control_source_v3_20261014/PLAN.json');out=ART/'axial-material-current-saved-three-macro-typed-path-compare-20261014-v1';releasepostpath=REC/'independent_literal2_new_compare_duplicate_physical_actual_release_postverify_20261014/REVIEW.json';releasepost=read(releasepostpath);releasepkg=Path(releasepost['actual_release_receipt_pin']['path']).parent;releasesourcepeer=Path(releasepost['actual_Source_review_pin']['path']).parent
 roots=list(dict.fromkeys(request['joint_archive_roots']+[str(out),str(BASE),str(releasepkg),str(releasesourcepeer),str(releasepostpath.parent)]))
 if any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b):raise RuntimeError('all cumulative old25 plus exact new/release evidence roots disjoint')
 authority=[pin(postpath),pin(postpath.parent/'TRUE_TOOL_RETURNS.json'),post['actual_aggregate_host_pin'],post['actual_aggregate_report_pin'],post['actual_Root_true_tool_pin'],post['actual_Root_argv_pin'],post['actual_request_pin'],post['actual_Root_saved_output_typed_path_diagnosis_pin']]
 data=[request['observed_final_A_pair']['sqlite_pin'],request['observed_final_A_pair']['native_pool_pin']]+[p for row in pairs for p in(row['sqlite_pin'],row['native_pool_pin'])]
 plan=dict(schema='SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(out),observed_pair=request['observed_final_A_pair'],native_pairs=pairs,original_native_producers=request['actual_native_producers'],original_failed_compare_authority_pins=authority,data_pair_pins=data,retained_A1_physical_pin=phys[0],historical_A2_A3_physical_pins=phys[1:],retired_physical_duplicate_byte_total=68743634,retired_physical_full_SHA_equals_retained_A1=True,original_ordinal_detail_pins=[p for row in child['comparisons']for p in row['all_output_pins']if Path(p['path']).name=='complete_macro_comparison.jsonl'],original_Common_Source_pin=control['original_Common_Source_pin'],original_support_Source_pin=control['original_support_Source_pin'],original_bounded_Source_pin=control['original_bounded_Source_pin'],complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=request['explicit_cumulative_metadata_file_pins'],source_dependency_pins=authority+data+[phys[0]]+[p['actual_report_pin']for p in request['actual_native_producers']]+[control['original_Common_Source_pin'],control['original_support_Source_pin'],control['original_bounded_Source_pin']]+request['explicit_cumulative_metadata_file_pins'],actual_duplicate_physical_release_proof_pin=releasepost['actual_release_receipt_pin'],actual_duplicate_physical_release_Root_tool_pin=releasepost['actual_Root_release_true_tool_pin'],actual_comparison_report_pin=None,physics_qualified=False,original_archive_decode_repeated=False,original_report_or_physical_record_order_rewritten=False)

 plan['actual_release_independent_post_pin']=pin(releasepostpath);plan['actual_release_independent_post_tools_pin']=pin(releasepostpath.parent/'TRUE_TOOL_RETURNS.json');plan['original_recipe_pin']=pin(REC/'OVERV_original_guarded_integer_control_source_v3_20261014/ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json');plan['source_dependency_pins'] += [plan['actual_duplicate_physical_release_proof_pin'],plan['actual_duplicate_physical_release_Root_tool_pin'],plan['actual_release_independent_post_pin'],plan['actual_release_independent_post_tools_pin'],plan['original_recipe_pin']];writerpin=write(BASE/'write_once_saved_three_macro_typed_path_SF_HF_CLI.py',base64.b64decode('IiIiUHVibGlzaCBleGFjdCByZXZpZXdlZCBTb3VyY2UgbWV0YWRhdGEgb25jZTsgbm8gc2NpZW50aWZpYyBleGVjdXRpb24uIiIiCmltcG9ydCBhcmdwYXJzZSxoYXNobGliLGpzb24sb3Msc2hsZXgsc3RhdApmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKQkFTRT1QYXRoKF9fZmlsZV9fKS5hYnNvbHV0ZSgpLnBhcmVudApkZWYgcmVxdWlyZSh2LHQpOgogaWYgdHlwZSh2KWlzIG5vdCBib29sIG9yIG5vdCB2OnJhaXNlIFJ1bnRpbWVFcnJvcih0KQpkZWYgaWRzKHMpOnJldHVybltzLnN0X2RldixzLnN0X2lubyxzLnN0X21vZGUscy5zdF9ubGluayxzLnN0X3NpemUscy5zdF9tdGltZV9ucyxzLnN0X2N0aW1lX25zXQpkZWYgcGluKHApOgogcD1QYXRoKHApO3M9cC5sc3RhdCgpO3JlcXVpcmUocC5pc19hYnNvbHV0ZSgpYW5kIHN0YXQuU19JU1JFRyhzLnN0X21vZGUpYW5kIHMuc3Rfbmxpbms9PTEgYW5kIG5vdCBhbnkoeC5pc19zeW1saW5rKClmb3IgeCBpbihwLCpwLnBhcmVudHMpKWFuZCBzLnN0X3NpemU8NjQqMioqMjAsJ29yZGluYXJ5IGJvdW5kZWQgbWV0YWRhdGEnKTtyYXc9cC5yZWFkX2J5dGVzKCk7cmVxdWlyZShpZHMocC5sc3RhdCgpKT09aWRzKHMpLCdtZXRhZGF0YSBiZWZvcmVhZnRlcjcnKTtyZXR1cm4gZGljdChwYXRoPXN0cihwKSxzaGEyNTY9aGFzaGxpYi5zaGEyNTYocmF3KS5oZXhkaWdlc3QoKSxzaXplX2J5dGVzPXMuc3Rfc2l6ZSxpZGVudGl0eT1pZHMocykpCmRlZiByZWFkKHApOnJlcXVpcmUocGluKHBbJ3BhdGgnXSk9PXAsJ2Z1bGwgZXhhY3QgbWV0YWRhdGEgUEYnKTtyZXR1cm4ganNvbi5sb2FkcyhQYXRoKHBbJ3BhdGgnXSkucmVhZF9ieXRlcygpKQpkZWYgaGFzKHYscCk6cmV0dXJuIHY9PXAgb3IgaXNpbnN0YW5jZSh2LGRpY3QpYW5kIGFueShoYXMoeCxwKWZvciB4IGluIHYudmFsdWVzKCkpb3IgaXNpbnN0YW5jZSh2LGxpc3QpYW5kIGFueShoYXMoeCxwKWZvciB4IGluIHYpCmRlZiB3cml0ZShwLGQpOgogd2l0aCBwLm9wZW4oJ3hiJylhcyBmOmYud3JpdGUoKGpzb24uZHVtcHMoZCxpbmRlbnQ9MikrJ1xuJykuZW5jb2RlKCkpO2YuZmx1c2goKTtvcy5mc3luYyhmLmZpbGVubygpKQogcmV0dXJuIHBpbihwKQpkZWYgbWFpbigpOgogYXA9YXJncGFyc2UuQXJndW1lbnRQYXJzZXIoYWxsb3dfYWJicmV2PUZhbHNlKQogZm9yIHJvbGUgaW4oJ3BlZXItcmV2aWV3JywncGVlci10b29scycpOgogIGZvciBzdWZmaXggaW4oJ3N1bW1hcnknLCdzaGEyNTYnLCdzZXZlbi1pZCcpOmFwLmFkZF9hcmd1bWVudCgnLS0nK3JvbGUrJy0nK3N1ZmZpeCxyZXF1aXJlZD1UcnVlKQogYT1hcC5wYXJzZV9hcmdzKCk7cHJvb2Y9e30KIGZvciByb2xlIGluKCdwZWVyLXJldmlldycsJ3BlZXItdG9vbHMnKToKICBrPXJvbGUucmVwbGFjZSgnLScsJ18nKTtwPXBpbihnZXRhdHRyKGEsaysnX3N1bW1hcnknKSk7cmVxdWlyZShwWydzaGEyNTYnXT09Z2V0YXR0cihhLGsrJ19zaGEyNTYnKWFuZCBwWydpZGVudGl0eSddPT1qc29uLmxvYWRzKGdldGF0dHIoYSxrKydfc2V2ZW5faWQnKSksJ2V4YWN0IHBlZXIgdHJpcGxlJyk7cHJvb2Zbcm9sZV09cAogcGVlcj1yZWFkKHByb29mWydwZWVyLXJldmlldyddKTt0b29sPXJlYWQocHJvb2ZbJ3BlZXItdG9vbHMnXSk7ej10b29sWydhY3R1YWxfcmV2aWV3X3JldHVybiddO3JlcXVpcmUocGVlclsnc291cmNlX29ubHknXWlzIFRydWUgYW5kIHBlZXJbJ2ZhaWx1cmUnXWlzIE5vbmUgYW5kIHBlZXJbJ3N0YXR1cyddLnN0YXJ0c3dpdGgoJ1BBU1MnKWFuZCBhbGwocGVlcltrXWlzIEZhbHNlIGZvciBrIGluKCdidXNpbmVzc19leGVjdXRlZCcsJ2NvbXBpbGVyX2V4ZWN1dGVkJywnbnVtZXJpY2FsX2V4ZWN1dGVkJywnZmlsZXNfZGVsZXRlZCcpKSwnc2FtZSByb3VuZCBTb3VyY2Ugb25seScpO3JlcXVpcmUodG9vbFsnb2JzZXJ2ZWRfY2xvc2VkJ11pcyBUcnVlIGFuZCB0eXBlKHRvb2xbJ29yaWdpbmFsX2ludGVnZXJfZXhpdF9jb2RlJ10paXMgaW50IGFuZCB0b29sWydvcmlnaW5hbF9pbnRlZ2VyX2V4aXRfY29kZSddPT0wIGFuZCB0eXBlKHpbJ2V4aXRfY29kZSddKWlzIGludCBhbmQgelsnZXhpdF9jb2RlJ109PTAgYW5kIHouZ2V0KCdzZXNzaW9uX2lkJylpcyBOb25lIGFuZCBqc29uLmxvYWRzKHpbJ291dHB1dCddLnN0cmlwKCkuc3BsaXRsaW5lcygpWy0xXSlbJ3Jldmlld19waW4nXT09cHJvb2ZbJ3BlZXItcmV2aWV3J10sJ2dlbnVpbmUgU291cmNlIHJldmlldzAnKQogcnA9cGluKEJBU0UvJ1NPVVJDRV9SRVZJRVdfUkVBRFkuanNvbicpO3JlYWR5PXJlYWQocnApO3NlbGVjdGVkPVtyZWFkeVtrXWZvciBrIGluKCdob3N0X3NvdXJjZV9waW4nLCdjaGlsZF9zb3VyY2VfcGluJywnb3JpZ2luYWxfYWRtaXNzaW9uX1NvdXJjZV9waW4nLCdvcmlnaW5hbF9hZGFwdGVyX1NvdXJjZV9waW4nLCdwbGFuX3BpbicsJ2ludmVyc2VfcGluJywnU291cmNlX2F1dGhvcl9waW4nLCd3cml0ZXJfc291cmNlX3BpbicpXStbcnBdO3JlcXVpcmUoYWxsKGhhcyhwZWVyLHApZm9yIHAgaW4gc2VsZWN0ZWQpLCdzYW1lIHJvdW5kIG5pbmUgZXhhY3Qgc2VsZWN0ZWQgU291cmNlIGZ1bGxQRicpO3BsYW49cmVhZChyZWFkeVsncGxhbl9waW4nXSkKIHRhYmxlPXt9CiBmb3IgcCBpbiBzZWxlY3RlZCtsaXN0KHByb29mLnZhbHVlcygpKStwbGFuWydzb3VyY2VfZGVwZW5kZW5jeV9waW5zJ106CiAgcmVxdWlyZShwWydwYXRoJ11ub3QgaW4gdGFibGUgb3IgdGFibGVbcFsncGF0aCddXT09cCwnb25lIGV4YWN0IGN1cnJlbnQgZnVsbFBGIHBlciBwYXRoJyk7dGFibGVbcFsncGF0aCddXT1wCiBkZXBzPWxpc3QodGFibGUudmFsdWVzKCkpCiBmb3IgcCBpbiBkZXBzOgogIHE9UGF0aChwWydwYXRoJ10pO3M9cS5sc3RhdCgpO3JlcXVpcmUoc3RhdC5TX0lTUkVHKHMuc3RfbW9kZSlhbmQgaWRzKHMpPT1wWydpZGVudGl0eSddYW5kIG5vdCBhbnkoeC5pc19zeW1saW5rKClmb3IgeCBpbihxLCpxLnBhcmVudHMpKSwnY3VycmVudCBkZXBlbmRlbmN5IGV4YWN0NycpCiBjb2RlPVtyZWFkeVtrXWZvciBrIGluKCdob3N0X3NvdXJjZV9waW4nLCdjaGlsZF9zb3VyY2VfcGluJywnb3JpZ2luYWxfYWRtaXNzaW9uX1NvdXJjZV9waW4nLCdvcmlnaW5hbF9hZGFwdGVyX1NvdXJjZV9waW4nKV07c3A9d3JpdGUoQkFTRS8nQ09NUExFVEVfU0FWRURfVEhSRUVfTUFDUk9fVFlQRURfUEFUSF9TT1VSQ0VfT05MWV9GUkVFWkUuanNvbicsZGljdChzY2hlbWE9J0NPTVBMRVRFX1NBVkVEX1RIUkVFX01BQ1JPX1RZUEVEX1BBVEhfU09VUkNFX09OTFlfRlJFRVpFX1YxJyxzb3VyY2Vfb25seT1UcnVlLGNvbnRyb2xfcGxhbl9waW49cmVhZHlbJ3BsYW5fcGluJ10sY2hpbGRfc291cmNlX3Bpbj1yZWFkeVsnY2hpbGRfc291cmNlX3BpbiddLGNvbXBsZXRlX3NvdXJjZV9maWxlX3BpbnM9Y29kZSxzYW1lX3JvdW5kX3Jldmlld19waW49cHJvb2ZbJ3BlZXItcmV2aWV3J10sc2FtZV9yb3VuZF90b29sc19waW49cHJvb2ZbJ3BlZXItdG9vbHMnXSxhY3R1YWxfY29tcGFyaXNvbl9yZXBvcnRfcGluPU5vbmUscGh5c2ljc19xdWFsaWZpZWQ9RmFsc2UpKQogaHA9d3JpdGUoQkFTRS8nQ09NUExFVEVfU0FWRURfVEhSRUVfTUFDUk9fVFlQRURfUEFUSF9IT1NUX1NPVVJDRV9PTkxZX0ZSRUVaRS5qc29uJyxkaWN0KHNjaGVtYT0nQ09NUExFVEVfU0FWRURfVEhSRUVfTUFDUk9fVFlQRURfUEFUSF9IT1NUX1NPVVJDRV9PTkxZX0ZSRUVaRV9WMScsc291cmNlX29ubHk9VHJ1ZSxob3N0X3NvdXJjZV9waW49cmVhZHlbJ2hvc3Rfc291cmNlX3BpbiddLHNlbGVjdGVkX3NvdXJjZV9mcmVlemVfcGluPXNwLGRlcGVuZGVuY2llcz1kZXBzK1tzcF0sYWN0dWFsX2R1cGxpY2F0ZV9waHlzaWNhbF9yZWxlYXNlX3Byb29mX3Bpbj1wbGFuWydhY3R1YWxfZHVwbGljYXRlX3BoeXNpY2FsX3JlbGVhc2VfcHJvb2ZfcGluJ10sYWN0dWFsX2R1cGxpY2F0ZV9waHlzaWNhbF9yZWxlYXNlX1Jvb3RfdG9vbF9waW49cGxhblsnYWN0dWFsX2R1cGxpY2F0ZV9waHlzaWNhbF9yZWxlYXNlX1Jvb3RfdG9vbF9waW4nXSxhY3R1YWxfZHVwbGljYXRlX3JlbGVhc2Vfc2NoZW1hPSdFWEFDVF9MSVRFUkFMMl9EVVBMSUNBVEVfUEhZU0lDQUxfUkVMRUFTRV9SRUNFSVBUX1YxJyxwaHlzaWNzX3F1YWxpZmllZD1GYWxzZSkpCiBvbGQ9cmVhZChwbGFuWydvcmlnaW5hbF9yZWNpcGVfcGluJ10pO2FyZ3Y9b2xkWydhcmd2J11bOjExXStbcmVhZHlbJ2hvc3Rfc291cmNlX3BpbiddWydwYXRoJ11dCiBmb3Igcm9sZSxwIGluKCgnc291cmNlLWZyZWV6ZScsc3ApLCgnaG9zdC1mcmVlemUnLGhwKSk6YXJndis9WyctLScrcm9sZSsnLXN1bW1hcnknLHBbJ3BhdGgnXSwnLS0nK3JvbGUrJy1zaGEyNTYnLHBbJ3NoYTI1NiddLCctLScrcm9sZSsnLXNldmVuLWlkJyxqc29uLmR1bXBzKHBbJ2lkZW50aXR5J10sc2VwYXJhdG9ycz0oJywnLCc6JykpXQogcmVxdWlyZShsZW4oYXJndik9PTI0LCdvcmlnaW5hbCBlbnYxMSBhbmQgaG9zdCBwbHVzIHR3byBhY3R1YWwgdHJpcGxlcycpO2NwPXdyaXRlKEJBU0UvJ1JPT1RfUkVWSUVXQUJMRV9TQVZFRF9USFJFRV9NQUNST19UWVBFRF9QQVRIX0FDVFVBTDI0X0FSR1YuanNvbicsZGljdChzY2hlbWE9J1JPT1RfUkVWSUVXQUJMRV9TQVZFRF9USFJFRV9NQUNST19UWVBFRF9QQVRIX0FDVFVBTF9BUkdWX1YxJyxhcmd2PWFyZ3Ysc2hlbGxfc2FmZV9jb21tYW5kPXNobGV4LmpvaW4oYXJndiksc291cmNlX2ZyZWV6ZV9waW49c3AsaG9zdF9mcmVlemVfcGluPWhwLHBoeXNpY3NfcXVhbGlmaWVkPUZhbHNlKSk7ZmQ9b3Mub3BlbihCQVNFLG9zLk9fUkRPTkxZfG9zLk9fRElSRUNUT1JZKQogdHJ5Om9zLmZzeW5jKGZkKQogZmluYWxseTpvcy5jbG9zZShmZCkKIHByaW50KGpzb24uZHVtcHMoZGljdChzdGF0dXM9J1NBVkVEX1RZUEVEX1BBVEhfU09VUkNFX1NGX0hGX0NMSTI0X1BVQkxJU0hFRF9PTkxZJyxTb3VyY2VfZnJlZXplX3Bpbj1zcCxIb3N0X2ZyZWV6ZV9waW49aHAsQ0xJX3Bpbj1jcCxidXNpbmVzc19leGVjdXRlZD1GYWxzZSxjb21waWxlcl9leGVjdXRlZD1GYWxzZSxudW1lcmljYWxfZXhlY3V0ZWQ9RmFsc2UsZmlsZXNfZGVsZXRlZD1GYWxzZSkpLGZsdXNoPVRydWUpCmlmIF9fbmFtZV9fPT0nX19tYWluX18nOm1haW4oKQo='))
 # The original producer object uses actual_report_pin; no renamed producer seal is created.
 pp=write(BASE/'PLAN.json',plan);iv=write(BASE/'COMPLETE_SAVED_TYPED_PATH_COMPARISON_SOURCE_BINDING_INVERSE.json',dict(schema='COMPLETE_SAVED_TYPED_PATH_COMPARISON_SOURCE_BINDING_INVERSE_V1',source_only=True,original_wrong_positional_child_Source_pin=pin(OLD/'current_material_lineage_evidence.py'),original_wrong_compare_function_whole_bytes=ast.get_source_segment((OLD/'current_material_lineage_evidence.py').read_text(),next(n for n in ast.parse((OLD/'current_material_lineage_evidence.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='compare_raw_macro')),new_child_Source_pin=childpin,new_host_Source_pin=hostpin,unchanged_admission_and_adapter_Source_copies=code,original_guard_methods_whole_bytes=borrowed,all_original_type_count_word_raw_payload_and_ordinal_fields_preserved=True,no_new_native_tree_decode_or_archive_spool=True,actual_comparison_report_pin=None,physics_qualified=False))
 rp=write(BASE/'SOURCE_REVIEW_READY.json',dict(schema='SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_SOURCE_ONLY_READY_V1',source_only=True,host_source_pin=hostpin,child_source_pin=childpin,original_admission_Source_pin=code[0]['candidate_Source_pin'],original_adapter_Source_pin=code[1]['candidate_Source_pin'],plan_pin=pp,inverse_pin=iv,Source_author_pin=pin(__file__),writer_source_pin=writerpin,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_CLI_pin=None,actual_duplicate_physical_release_proof_pin=releasepost['actual_release_receipt_pin'],actual_duplicate_physical_release_Root_tool_pin=releasepost['actual_Root_release_true_tool_pin'],actual_comparison_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 print(json.dumps(dict(status='SAVED_THREE_MACRO_TYPED_PATH_COMPARE_SOURCE_ONLY_READY',ready_pin=rp,plan_pin=pp,inverse_pin=iv,host_source_pin=hostpin,child_source_pin=childpin,Source_author_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()

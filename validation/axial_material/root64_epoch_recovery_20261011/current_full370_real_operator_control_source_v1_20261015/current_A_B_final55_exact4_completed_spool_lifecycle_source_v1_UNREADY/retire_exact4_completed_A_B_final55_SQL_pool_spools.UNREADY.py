"""UNREADY exact four completed A/B final55 SQL/pool temporary spools; canonical native and scientific results remain, with no old-byte archive claim."""
import argparse,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts')
READONLY_CONTEXT=None
FALSE=dict(numerical_executed=False,compiler_executed=False,JSONL_or_array_values_decoded=False,
 compression_repeated=False,decompression_repeated=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,target=False):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
  and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'exact integer fullPF')
 q=Path(p['path']);s=q.lstat();owned=s.st_uid==501==os.getuid()and s.st_nlink==1
 require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'literal original role exact7')
 if target:require(owned,'only exact four completed final55 SQL/pool targets owned501/nlink1; no readonly-role exception')
 elif not owned:
  require(READONLY_CONTEXT is not None,'specific frozen B3 readonly role context required')
  build,bm,buildpin,bmpin=READONLY_CONTEXT
  current(buildpin);current(bmpin);bm.current_metadata_role(p,build)
 return q
def current_failed_v1(p,plan):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q
def current_failed_pool(p,plan):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool metadata/runtime rows, never fullPF/SHA or deletion targets')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-pool retained row stable current7 only')
 return q
def unique(rows):
 out={}
 for p in rows:require(p['path']not in out or out[p['path']]==p,'same path same fullPF');out[p['path']]=p
 return list(out.values())
def exact_historical_absence(plan):
 early=plan['exact16_retired_temporary_target_pins'];presence=plan['historical_retired_presence_full_pin'];originals=plan['exact28_retired_result_JSONL_target_pins']
 require(len(early)==16 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in early[:15])and set(early[-1])=={'path','size_bytes','identity'}and len(originals)==28 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in originals),'exact16 mixed historical plus28 fullPF retired JSONL, no generic missing role')
 historical=early+[presence]+originals
 require(len({p['path']for p in historical})==45,'only exact16+presence+28 historical paths')
 for p in historical:require(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only specifically closed oldpaths absent; do not stat/relabel retired fullPFs')

def full(p,budget,parse=False):
 q=current(p);require(not parse or p['size_bytes']<8*2**20,'metadata8MiB');h=hashlib.sha256();n=0;parts=[]
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  require(ids(os.fstat(fd))==p['identity'],'opened exact7')
  while b:=os.read(fd,2**20):
   h.update(b);n+=len(b)
   if parse:parts.append(b)
   budget()
  require(ids(os.fstat(fd))==p['identity'],'EOF exact7')
 finally:os.close(fd)
 current(p);require(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind wholeEOF SHA/length')
 return json.loads(b''.join(parts))if parse else None
def pin(q):
 s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  while b:=f.read(2**20):h.update(b)
 require(ids(q.lstat())==ids(s),'own metadata stable')
 return dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
def module(p,name,budget):
 full(p,budget);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def genuine(d,key,p,role):
 r=d[key];require(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0
  and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r
  and json.loads(r['output'].splitlines()[-1])[role]==p,'genuine typed original closed0 exact stdout PF')
def snapshot(f,d):
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'receipt8MiB')
 previous=f.seek(0,os.SEEK_END);sourceBytes=sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file())
 require(sourceBytes-previous+len(raw)<8*2**20,'entire retirement Source/receipts8MiB before rewrite')
 f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())

def admit_completed_consumers(plan,budget,archiveplan):
 audit=full(plan['actual_completed_spool_role_audit_pin'],budget,True)
 require(audit['schema']=='FINAL_A_B_FINAL55_EXACT4_COMPLETED_DERIVED_SPOOL_SOURCE_METADATA_AUDIT_V1'and audit['source_only']is True and audit['metadata_only']is True and audit['formal_retirement_admission']is False and audit['payload_SQL_pool_XSM_gzip_or_scientific_JSONL_body_read_or_hashed']is False,'independent Source/meta audit is role evidence, not execution admission')
 targets=plan['exact_target_pins'];native=plan['retained_exact_canonical_observer_XSM_full_pins'];require(targets==audit['exact_ordered4_candidate_target_full_pins']==plan['ordered_completed_derived_spool_full_pins']and len(targets)==4 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in targets)and [p['size_bytes']for p in targets]==[16953344,74693004,16953344,74693004]and sum(p['size_bytes']for p in targets)==183292696 and native==audit['retained_exact_canonical_observer_XSM_full_pins']and len(native)==2,'exact ordered finalA SQL/pool then finalB SQL/pool and their canonical observer native2')
 posts={};reports={}
 specs=(('A_full_aggregate','INDEPENDENT_ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_METADATA_POSTVERIFY_V1','PASS_RECORDED_CURRENT_A_FULL_AGGREGATE_SOURCE_GAP0_METADATA_ONLY_CHILD2_PRESERVED','actual_Host_report_pin','actual_Root_tools_pin'),('A_three_producer_typed_compare','INDEPENDENT_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION_V1','PASS_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION','actual_Host_report_pin','actual_Root_true_tool_pin'),('A_OVERV_control','INDEPENDENT_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_ACTUAL_POSTVERIFICATION_V1','PASS_ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_CURRENT_CONTROL_FACTS_POSTVERIFIED_NO_HISTORICAL_OR_PHYSICS_QUALIFICATION','actual_report_pin','actual_Root_true_tool_return_pin'),('B_full_aggregate',None,None,'actual_Host_report_pin','actual_Root_tools_pin'),('B_B55_vs_nativeB2_typed_compare','RECORDED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_TYPED_COMPARISON_METADATA_POSTVERIFY_V2','PASS_ACTUAL_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_V2_ROOT0_CHILD2_METADATA_ONLY_DIFFERENCES_RECORDED','actual_Host_report_pin','actual_Root_tools_pin'),('B55_OVERV_control','RECORDED_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_METADATA_POSTVERIFY_V1','PASS_ACTUAL_CURRENT_B55_OVERV_THREE_STAGE0_2960_WORDS_MATCH_METADATA_ONLY_NO_PHYSICS_QUALIFICATION','actual_Host_report_pin','actual_Root_tools_pin'))
 for name,schema,status,hostfield,toolsfield in specs:
  c=audit['completed_consumer_closures'][name];report=full(c['Root_report'],budget,True);raw=full(c['Root_tools'],budget,True);post=full(c['post'],budget,True);tools=full(c['post_tools'],budget,True)
  genuine(raw,'actual_terminal_return',c['Root_report'],'report_pin')
  if name=='A_three_producer_typed_compare':
   r=tools['actual_terminal_return'];text=tools['actual_initial_return']['output']+r['output']
   require(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r and tools['actual_full_stdout']==text and json.loads(text.splitlines()[-1])['review_pin']==c['post'],'exact historical A3post initialstdout+terminal0 source, no fabricated terminal stdout alias')
  else:genuine(tools,'actual_review_return',c['post'],'review_pin')
  if name=='B_full_aggregate':schema=c['post_schema'];status=c['post_status']
  require(report['failure']is None and post['schema']==schema and post['status']==status and post['failure']is None and post[hostfield]==c['Root_report']and post[toolsfield]==c['Root_tools']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0,'six genuine completed Root0/independentpost0 exact report/tool roles, not Source status substituted')
  posts[name]=post;reports[name]=report
 A=posts['A_full_aggregate'];B=posts['B_full_aggregate'];T=posts['A_three_producer_typed_compare'];C=posts['B_B55_vs_nativeB2_typed_compare'];AC=posts['A_OVERV_control'];BC=posts['B55_OVERV_control']
 for post in(A,B,C):require(type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2,'original completed evidence-only child2/FAILED preserved')
 require(type(T['original_intentional_evidence_child_exit_code'])is int and T['original_intentional_evidence_child_exit_code']==2,'original A-three comparison evidence child2 preserved')
 require(A['actual_snapshot_count']==8 and A['actual_context_event_count']==55 and A['actual_compared_source_fields']==19249 and A['actual_all_mismatch_elements']==A['actual_unknown_macro_producers']==A['actual_context_or_operand_issues']==0 and A['complete_phases']==[dict(phase=x,computation_finished=True)for x in('scattering','scalar','fission','extras','overv_fallback','metadata')],'A8/55/full19249/sixphase completed actual zeros')
 expectedB=dict(actual_compared_source_fields=19249,actual_compared_known_elements=1829421,actual_context_or_operand_issues=0,actual_all_mismatch_elements=0,actual_unknown_macro_producers=0)
 require(all(type(B[k])is int and B[k]==v for k,v in expectedB.items())and B['actual_snapshot_pair_count']==8 and B['actual_context_event_count']==55 and B['actual_six_phase_results']==A['complete_phases'],'B8/55/full19249/1829421/sixphase completed actual zeros')
 ar=full(A['actual_execution_request_pin'],budget,True);apair=ar['aggregation_binding']['actual_context_states']['A']['all_snapshot_pairs'][-1];bpair=B['all_snapshot_pairs'][-1]
 require(apair['event']==bpair['event']==55 and apair['role']==bpair['role']=='final-complete-micro'and [apair['sqlite_pin'],apair['native_pool_pin'],bpair['sqlite_pin'],bpair['native_pool_pin']]==targets and [apair['input_pin'],bpair['input_pin']]==native,'completed original consumers actually used these exact four derived spools from two retained native snapshots')
 tc=full(T['actual_child_report_pin'],budget,True);cc=full(C['control_plan_pin'],budget,True)
 require(tc['observed_pair']==apair and (T['total_macro_record_comparisons'],T['total_compared_original_words'],T['all_raw_word_mismatches'],T['all_metadata_mismatches'])==(58860,6792456,0,0)and cc['observed_B55_pair']==bpair and C['actual_comparison_counts']==dict(compared_all_macro_records=19620,compared_original_payload_words=2264152,raw_word_mismatches=0,metadata_mismatches=0)and C['actual_path_sets_equal']is True and C['actual_exact_inventory_metadata_and_all_words_equal']is True,'A wholethree58860/6792456 and B19620/2264152 completed original typed/allword comparisons zero')
 am=A['current_OVERV_control_admission_metadata'];ac=audit['completed_consumer_closures']['A_OVERV_control'];bc=audit['completed_consumer_closures']['B55_OVERV_control']
 require(am['same_original_final_pair']==apair and all(am['control_metadata_pins'][k]==ac[j]for k,j in(('control_report','Root_report'),('control_returns','Root_tools'),('control_post','post'),('control_post_returns','post_tools')))
  and AC['actual_current_overv_words_compared']==2960 and AC['all_current_native_vs_independent_integer_model_vs_saved_words_equal']is True and len(AC['actual_watchdog_results'])==3 and all(type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None for w in AC['actual_watchdog_results'])and BC['selected_actual_B55_SQL_pool_pair']==dict(sqlite_pin=targets[2],native_pool_pin=targets[3])and BC['actual_child_integer_exit_codes']==[0,0,0]and all(type(x)is int for x in BC['actual_child_integer_exit_codes'])and BC['all_current_native_vs_integer_model_vs_saved_word_equality_recorded_by_actual_Root']is True,'both actual ENERGY/2960word OVERV controls consumed exact final pairs; all original stage0 facts preserved')
 pending=full(plan['specific_pending_new_B_context_Source_plan_pin'],budget,True)
 require(pending['schema']=='DRAFT_NEW_A1_B2_A3_COMPLETE_CONTEXT_AND_PLANE2_UNSEALED_CONSUMER_PLAN_V1'and pending['Source_only']is True and pending['Source_admission_ready']is False and pending['draft_unready']is True and pending['compiler_executed']is False and pending['native_executed']is False and pending['actual_new_ARCHIVE_pin']is None and pending['actual_new_GLOBAL_pin']is None and pending['actual_new_PROJECT_pin']is None and pending['actual_plane2_QBUILD_and_strict_BOOTB_result_pin']is None,'only this specified unfinished newB native-only Source plan audited, never all future science consumers globally waived')
 for e in audit['actual_consumer_and_future_native_only_Source_evidence']:
  full(e['Source_pin'],budget);lines=Path(e['Source_pin']['path']).read_text().splitlines();require(all(lines[x['line']-1]==x['text']for x in e['exact_lines']),'exact completed consumer and specified future native-only Source call evidence')
 for p in native+audit['required_result_documents_preserved_pins']:require(p in plan['retained_current7_pins'],'canonical native and all result documents are never temporary targets');current(p)
 require(plan['future_use_requires_new_full_native_extraction_and_independent_admission']is True and plan['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False and plan['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False and plan['all_original_spool_file_bytes_archived_or_reconstructable_claimed']is False,'completed temporary spool lifecycle only; replay requires newly admitted full extraction, no oldbyte or SQLgzip/newpool compatibility promise')
 return audit,dict(completed_consumer_closure_pins=audit['completed_consumer_closures'],A_full6phase_counts=audit['A_full6phase_counts'],A_saved_three_typed_counts=audit['A_saved_three_typed_counts'],B_full6phase_counts=expectedB,B_full_typed_counts=C['actual_comparison_counts'],retained_exact_canonical_observer_XSM_full_pins=native,specific_pending_native_only_B_context_Source_plan_pin=plan['specific_pending_new_B_context_Source_plan_pin'],all_future_scientific_consumers_claimed_native_only=False)

def main():
 global READONLY_CONTEXT
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=('check','execute'),required=True)
 for role in('source','plan','review','review-tools'):ap.add_argument('--'+role+'-pin',required=True)
 ap.add_argument('--readonly-receipt-pin')
 for role in('readonly-tools','readonly-post','readonly-post-tools'):ap.add_argument('--'+role+'-pin')
 a=ap.parse_args();started=time.monotonic();state={};plan=None
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
  and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'original env/thread1/unoptimized/unprofiled')
 def budget(force=False):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-started<600,'SELF512/stage600 within whole1800; no clock reset')
  require(sum(q.lstat().st_size for q in BASE.rglob('*')if q.is_file())<8*2**20,'whole owning retirement Source/metadata8MiB')
  if state and(force or time.monotonic()-state['last']>=0.25):
   sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
   require(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit()
    and int(sample.stdout.strip())*1024<512*2**20,'original same-PID PS guard; system role never target')
   h=state['history'].check();j=state['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
   for p in plan['retained_B2_current_epoch_readonly_pins']:
    current(p);require(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'every selected old B2 readonly role remains in original history, not fresh metadata')
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   exact_historical_absence(plan)
   unlinked={}
   for fd in os.listdir('/dev/fd'):
    try:s=os.fstat(int(fd))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   require(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30
    and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30
    and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'whole original joint/history/cold/free including external/open-unlinked')
   state.update(last=time.monotonic(),latest=dict(history=h,joint=j,external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-started,actual_PS_return=dict(returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr)))
 ps=json.loads(a.source_pin);pp=json.loads(a.plan_pin);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin)
 require(ps['path']==str(Path(__file__).absolute())and pp['path']==str(BASE/'PLAN.json'),'exact owning frozen Source/PLAN')
 receipt=BASE/('READONLY_RECEIPT.json'if a.mode=='check'else'EXECUTION_RECEIPT.json')
 d=dict(schema='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,
  source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,
  files_deleted=False,temporary_completed_derived_spool_lifecycle_only=True,all_authoritative_native_and_completed_result_documents_preserved=True,retired_spool_file_bytes_archived_or_byte_reconstructable_claimed=False,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_PLAN_V1'
    and plan['Source_admission_ready']is True and plan['draft_unready']is False
    and plan['actual_six_completed_consumers_closed0']is True and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20,'NULL draft is never admitted')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
    and peer['source_pin']==ps and peer['plan_pin']==pp,'actual independent frozen Source review0')
   archiveplan=full(plan['inherited_exact28_retirement_plan_pin'],budget,True)
   roots=plan['complete_joint_roots'];require(roots==archiveplan['complete_joint_roots']and len(roots)==83
    and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']
    and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),
    'entire real83 prefix/no reset or new temporary-spool data root')
   buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin']
   build=full(buildpin,budget,True);bm=module(bmpin,'B2_physical_directory_retirement_original_build_metadata_roles',budget)
   require(buildpin==archiveplan['original_guard_build_plan_pin']and bmpin==archiveplan['original_guard_build_contract_Source_pin'],'exact inherited frozen readonly role delegation')
   READONLY_CONTEXT=(build,bm,buildpin,bmpin)
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
   production=module(plan['original_production_resource_Source_pin'],'B2_physical_directory_retirement_original_production',budget)
   factory=module(plan['original_history_resource_Source_pin'],'B2_physical_directory_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),
    joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   cp=plan['actual_exact28_retirement_closure_pins'];require(all(type(cp[k])is dict for k in('receipt','Root_tools','post','post_tools'))and plan['actual_exact28_execute0_independent_post0_complete']is True,'future exact28 actualexecute0 plus independentpost0 NULL hard reject')
   receipt28=full(cp['receipt'],budget,True);raw28=full(cp['Root_tools'],budget,True);post28=full(cp['post'],budget,True);tools28=full(cp['post_tools'],budget,True)
   genuine(raw28,'actual_terminal_return',cp['receipt'],'receipt_pin');genuine(tools28,'actual_review_return',cp['post'],'review_pin')
   contract=plan['actual_exact28_post_key_projection'];require(type(contract)is dict and type(plan['actual_exact28_post_Source_projection_pin'])is dict,'exact future frozen execute-post schema/field projection required')
   projection=full(plan['actual_exact28_post_Source_projection_pin'],budget,True);require(projection['schema']==contract['schema']and projection['status']==contract['status'],'same frozen execute-post Source contract')
   require(receipt28['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt28['mode']=='execute'and receipt28['status']=='RETIRED_CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt28['failure']is None and receipt28['plan_pin']==plan['inherited_exact28_retirement_plan_pin']and receipt28['exact_target_pins']==receipt28['actual_released_pins']==archiveplan['exact_target_pins']==plan['exact28_retired_result_JSONL_target_pins']and receipt28['actual_released_bytes']==249929878 and receipt28['files_deleted']is True and receipt28['resources_after_original_classes_forced_fresh']is True,'genuine exact28 result plaintext retirement execute0, never readonly/postonly substituted')
   require(post28['schema']==contract['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'and post28['status']==contract['status']=='PASS_ACTUAL_B_COMPLETE28_JSONL_EXACT28_ORIGINALS_RETIRED_FULL_BYTES_ARCHIVED_METADATA_ONLY'and post28['failure']is None and post28['metadata_only']is True and post28['actual_execution_receipt_pin']==cp['receipt']and post28['actual_Root_tools_pin']==cp['Root_tools']and post28['plan_pin']==plan['inherited_exact28_retirement_plan_pin']and post28['source_pin']==receipt28['source_pin']and type(post28['actual_Root_integer_exit_code'])is int and post28['actual_Root_integer_exit_code']==0 and post28['exact_target_pins']==post28['actual_released_pins']==plan['exact28_retired_result_JSONL_target_pins']and post28['actual_released_bytes']==249929878 and post28['files_deleted']is True and post28['files_deleted_by_post']is False and post28['resources_after_original_classes_forced_fresh']is True and post28[contract['exact28_absence_twice_field']]is True,'real independent exact28 execute metadata0 including preciseabsence, originalfullbytes archived')
   targets=plan['exact_target_pins'];completed=plan['ordered_completed_derived_spool_full_pins'];require(targets==completed and len(targets)==len({p['path']for p in targets})==4 and sum(p['size_bytes']for p in targets)==plan['planned_released_bytes']==plan['target_total_bytes']==183292696,'only four completed finalA/finalB SQL/pool derived temporaries, never original data')
   audit,consumedProof=admit_completed_consumers(plan,budget,archiveplan)
   require(post28[contract['retained_current7_array_field']]==receipt28['retained_current7_pins']and post28['all_retained_roles_current7_verified_twice']is True and plan['retained_current7_pins']==unique([p for p in post28[contract['retained_current7_array_field']]if p not in targets]+audit['retained_exact_canonical_observer_XSM_full_pins']+audit['required_result_documents_preserved_pins'])and plan['retained_failed_v1_current7_only_pins']==archiveplan['retained_failed_v1_current7_only_pins']and plan['retained_failed_pool_archive_current7_only_pins']==archiveplan['retained_failed_pool_archive_current7_only_pins']and plan['retained_B2_current_epoch_readonly_pins']==archiveplan['retained_B2_current_epoch_readonly_pins'],'latest exact28 actual post current-role array minus only four targets plus explicitly preserved native/docs, never assume old E16 selected roles were complete')
   gzips=plan['permanent_result28_gzip_pins'];entries=plan['permanent_result28_entry_pins'];indexpin=plan['permanent_result28_lookup_index_pin'];empty=plan['retained_empty_numeric_mismatch_JSONL_pin']
   require(gzips==archiveplan['retained_ordered_result_JSONL_gzip_pins']==receipt28['compressed_result_full_pins']==post28['retained_ordered_result_JSONL_gzip_pins']and entries==archiveplan['retained_ordered_result_JSONL_entry_pins']==receipt28['retained_ordered_result_JSONL_entry_pins']==post28['retained_ordered_result_JSONL_entry_pins']and indexpin==archiveplan['actual_archive_closure_pins']['index']==receipt28['original_lookup_index_pin']==post28['original_lookup_index_pin']and len(gzips)==len(entries)==28 and empty==archiveplan['retained_empty_numeric_mismatch_JSONL_pin']==post28['retained_empty_numeric_mismatch_JSONL_pin']and empty['size_bytes']==0 and post28['exact16_retired_temporary_target_pins']==plan['exact16_retired_temporary_target_pins']and post28['historical_retired_presence_full_pin']==plan['historical_retired_presence_full_pin']and post28['past_exact16_and_presence_historical_absence_only']is True,'permanent full28 gzip/entry/lookup exact original order and empty0 plus exact historical roles genuinely checked by actual post; original entry creation history unchanged')
   index=full(indexpin,budget,True);require(index['ordered_original_result_JSONL_pins']==plan['exact28_retired_result_JSONL_target_pins']and index['ordered_result_JSONL_archive_entry_pins']==entries and [r['compressed_archive_full_pin']for r in index['entries']]==gzips,'precise permanent result restoremapping for full28 no generic missing skip')
   proofpins=list(cp.values())+[plan['inherited_exact28_retirement_plan_pin'],plan['actual_exact28_post_Source_projection_pin'],plan['actual_completed_spool_role_audit_pin'],plan['specific_pending_new_B_context_Source_plan_pin']]+[c[k]for c in audit['completed_consumer_closures'].values()for k in('Root_report','Root_tools','post','post_tools')]+[e['Source_pin']for e in audit['actual_consumer_and_future_native_only_Source_evidence']]
   require(plan['retained_archive_metadata_current7_pins']==unique(archiveplan['retained_archive_metadata_current7_pins']+proofpins)and plan['explicit_cumulative_metadata_file_pins']==unique(archiveplan['explicit_cumulative_metadata_file_pins']+proofpins),'full inherited cumulativemetadata plus exact new lifecycle/sixconsumer/Source proofs, no excluded externalaccounting')
   require(plan['exact16_retired_temporary_target_pins']==archiveplan['exact16_retired_temporary_target_pins']and plan['historical_retired_presence_full_pin']==archiveplan['historical_retired_presence_full_pin'],'same exact priorhistorical roles, never current relabelled')
   retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+gzips+entries+[indexpin,empty]
   require(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},'precise four target paths excluded from everyretained role; native/results/docs/archive/history never target')
   for p in retained:current(p)
   exact_historical_absence(plan)
   for p in completed:current(p,True);full(p,budget)
   d.update(exact_target_pins=targets,completed_derived_spool_full_pins=completed,target_role_kinds=plan['target_role_kinds'],actual_completed_consumer_proof=consumedProof,actual_exact28_retirement_closure_pins=cp,
    exact16_retired_temporary_target_pins=plan['exact16_retired_temporary_target_pins'],historical_retired_presence_full_pin=plan['historical_retired_presence_full_pin'],exact28_retired_result_JSONL_target_pins=plan['exact28_retired_result_JSONL_target_pins'],
    permanent_result28_gzip_pins=gzips,permanent_result28_entry_pins=entries,permanent_result28_lookup_index_pin=indexpin,retained_empty_numeric_mismatch_JSONL_pin=empty,
    future_use_requires_new_full_native_extraction_and_independent_admission=True,new_SQL_or_pool_byte_identity_with_retired_file_claimed=False,old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed=False,
    all_future_scientific_consumers_claimed_native_only=False,specific_pending_native_only_B_context_Source_plan_pin=plan['specific_pending_new_B_context_Source_plan_pin'],
    complete_joint_roots=roots,complete_pair_archive_success=False,all_authoritative_native_and_completed_result_documents_preserved=True,historical_original_PFs_not_current_relabelled=True,generic_missing_path_skip_authorized=False,
    retained_current7_pins=plan['retained_current7_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_NO_UNLINK'
     and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['actual_released_pins']==[],'successful exact1 failed-pool-partial recovery once readonly; no reuse of a failed check')
    require(plan['independent_readonly_post0_required_before_execute']is True and all(v is not None for v in(a.readonly_tools_pin,a.readonly_post_pin,a.readonly_post_tools_pin)),'independent actual readonly metadata post0 and tools required before unlink')
    pchecktools=json.loads(a.readonly_tools_pin);checktools=full(pchecktools,budget,True)
    genuine(checktools,'actual_readonly_return',pcheck,'receipt_pin');require(checktools['actual_readonly_permission_mode']=='require_escalated','actual original readonly permission route')
    pcheckpost=json.loads(a.readonly_post_pin);pcheckposttools=json.loads(a.readonly_post_tools_pin)
    checkpost=full(pcheckpost,budget,True);checkposttools=full(pcheckposttools,budget,True)
    genuine(checkposttools,'actual_review_return',pcheckpost,'review_pin');contract=plan['readonly_post_report_contract']
    require(checkpost['schema']==contract['schema']and checkpost['status']==contract['status']and checkpost['failure']is None
     and checkpost['metadata_only']is True and checkpost['actual_readonly_receipt_pin']==pcheck
     and checkpost['actual_readonly_tools_pin']==pchecktools and checkpost['source_pin']==ps and checkpost['plan_pin']==pp
     and checkpost['exact_target_pins']==targets and checkpost['actual_released_pins']==[]and checkpost['actual_released_bytes']==0
     and checkpost['files_deleted']is False and checkpost['resources_after_original_classes_forced_fresh']is True
     and type(checkpost['actual_readonly_Root_integer_exit_code'])is int and checkpost['actual_readonly_Root_integer_exit_code']==0,
     'separate genuine readonly metadata peer0 for exact same Source/plan/receipt/tools/targets/no-unlink/fresh resources')
    d.update(actual_readonly_receipt_pin=pcheck,actual_readonly_tools_pin=pchecktools,
     actual_readonly_post_pin=pcheckpost,actual_readonly_post_tools_pin=pcheckposttools)
    command=['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]
    r=subprocess.run(command,capture_output=True,timeout=30)
    require(len(r.stdout)+len(r.stderr)<2*2**20,'bounded actual lsof owner evidence')
    d['actual_lsof_owner_check']=dict(argv=command,returncode=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode())
    require(r.returncode==1 and r.stdout==b''and r.stderr==b'','no live plaintext owners; never unlink live files')
    snapshot(f,d);budget(True)
    for p in targets:
     q=current(p,True);fd=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
     try:
      require(ids(os.stat(q.name,dir_fd=fd,follow_symlinks=False))==p['identity'],'immediate exact private target7')
      os.unlink(q.name,dir_fd=fd);os.fsync(fd);d['actual_released_pins'].append(p);d['actual_released_bytes']+=p['size_bytes'];d['files_deleted']=True
     finally:os.close(fd)
     d['status']='PARTIAL_CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE';snapshot(f,d);budget()
    require(d['actual_released_bytes']==plan['planned_released_bytes']and len(d['actual_released_pins'])==4
     and all(not os.path.lexists(p['path'])for p in targets),'only exact four completed derived spool targets absent; canonical native and all scientific results preserved')
    d['status']='RETIRED_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_DERIVED_TEMPORARIES_ONLY'
   else:d['status']='READONLY_READY_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_NO_UNLINK'
   d['completed_derived_spools_retired']=a.mode=='execute'
   for p in retained:current(p)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   exact_historical_absence(plan)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

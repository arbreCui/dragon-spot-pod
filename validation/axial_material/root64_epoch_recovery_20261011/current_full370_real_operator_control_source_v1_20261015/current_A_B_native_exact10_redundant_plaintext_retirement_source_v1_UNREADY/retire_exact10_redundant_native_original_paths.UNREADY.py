"""UNREADY exact10 native redundant-original retirement. Every original byte requires an exact live copy/archive recovery mapping and a new genuine independent bytecontrol; no completed-spool justification."""
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
 if target:require(owned,'only exact native10 targets owned501/nlink1; no readonly-role exception')
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
 rows=plan['exact49_historical_absent_pins'];require(len(rows)==len({p['path']for p in rows})==49,'only exact inherited49 historical paths, never generic missing')
 for p in rows:require(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'precise already closed historical path absence only')

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

def admit_native_byte_control(plan,budget):
 cp=plan['actual_native_byte_control_closure_pins'];require(type(cp)is dict and all(type(cp[k])is dict for k in('report','Root_tools','post','post_tools'))and plan['actual_native_byte_control_Root0_independent_post0_complete']is True,'future genuine new native control Root0/post0 roles NULL hard reject')
 controlplan=full(plan['native_byte_control_plan_pin'],budget,True);control=full(cp['report'],budget,True);raw=full(cp['Root_tools'],budget,True);post=full(cp['post'],budget,True);tools=full(cp['post_tools'],budget,True)
 genuine(raw,'actual_terminal_return',cp['report'],'report_pin');genuine(tools,'actual_review_return',cp['post'],'review_pin')
 contract=plan['actual_native_byte_control_post_key_projection'];projection=full(plan['actual_native_byte_control_post_Source_projection_pin'],budget,True);postauthor=full(plan['actual_native_byte_control_post_author_freeze_pin'],budget,True);full(plan['actual_native_byte_control_post_Source_pin'],budget)
 require(type(contract)is dict and contract['schema']==projection['schema']and contract['status']==projection['status'],'frozen actual post Source projection exact schema/status; no guessed PASS')
 require(post['schema']==contract['schema']and post['status']==contract['status']and post['failure']is None and post['metadata_only']is True and post[contract['Root_report_pin_field']]==cp['report']and post[contract['Root_tools_pin_field']]==cp['Root_tools']and type(post[contract['Root_integer_exit_code_field']])is int and post[contract['Root_integer_exit_code_field']]==0,'genuine separate control metadata0 binds same Root report/tools typed0')
 require(post['reviewer_Source_pin']==plan['actual_native_byte_control_post_Source_pin']==postauthor['post_Source_pin']and postauthor['core_plan_pin']==plan['native_byte_control_plan_pin']and postauthor['core_Source_author_freeze_pin']==plan['native_byte_control_author_freeze_pin']and postauthor['exact_success_field_projection_pin']==plan['actual_native_byte_control_post_Source_projection_pin']and Path(plan['actual_native_byte_control_post_Source_pin']['path']).parent==Path(cp['post']['path']).parent and post['Root_recorded_all17_native_fullEOF_SHA_and_stable7_verified']is True and post['Root_new_B_final55_independent_complete_stream_verified']is True and post['retirement_authorized']is False and post['files_deleted']is False,'same genuinely executed corrected post Source/author/projection path and explicit17/newBfinal proof; old unexecuted post is not actual evidence')
 require(control['schema']=='ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT_V1'and control['status']=='PASS_ROOT_NATIVE_EXACT10_COMPLETE_BYTE_PRESERVATION_CONTROL_NO_RETIREMENT'and control['failure']is None and control['source_pin']==plan['native_byte_control_Source_pin']and control['plan_pin']==plan['native_byte_control_plan_pin']and control['role_projection_pin']==plan['native_role_projection_pin']and control['children_started']==0 and control['actual_child_integer_exit_code']is None and control['files_deleted']is False and control['retirement_authorized']is False and control['final_report_resource_check_passed']is True and control['native_or_scientific_values_decoded']is False and control['restored_large_file_written']is False,'only actual Root byte preservation control completed; never old m proof, native rerun, deletion or new scientific qualification')
 targets=plan['exact_target_pins'];canonical=plan['retained_ordered7_canonical_native_full_pins'];maps=plan['exact_ordered10_recovery_mappings'];all17=control['all17_native_full_pins']
 require(targets==control['exact_ordered10_candidate_full_pins']==controlplan['exact_ordered10_candidate_full_pins']and canonical==control['retained_ordered7_canonical_native_full_pins']==controlplan['retained_ordered7_canonical_native_full_pins']and maps==control['exact_ordered10_recovery_mappings']==controlplan['exact_ordered10_recovery_mappings']and len(targets)==10 and len(canonical)==7 and all17==controlplan['all17_native_full_pins']==unique(targets+canonical)and len(all17)==17 and len({p['path']for p in all17})==17 and len(maps)==10 and[m['target_pin']for m in maps]==targets and sum(p['size_bytes']for p in targets)==control['candidate_total_bytes']==plan['planned_released_bytes']==232289584,'precise10 candidate maps plus canonical7 native fullPF roles, no generic duplicate reduction')
 require(control['all17_native_fullEOF_SHA_and_stable7_verified']is True and control['all17_native_current7_verified_before_and_after']is True and len(control['all17_native_blind_fullEOF_SHA_length_proofs'])==17,'new actual complete17 blindSHA and stable7 proof')
 for row,p in zip(control['all17_native_blind_fullEOF_SHA_length_proofs'],all17):
  r=row['blind_fullEOF_SHA_length'];require(row['original_full_pin']==p and r['sha256']==p['sha256']and r['size_bytes']==p['size_bytes']and r['full_EOF']is True and r['stable_opened_and_EOF_identity']==p['identity'],'each actual fullEOF SHA/length and stable7 exactly matches saved original/canonical PF')
 gzip=plan['retained_complete_B4_gzip_pin'];entry=plan['retained_B4_member0_entry_pin'];index=plan['retained_B4_all4_lookup_index_pin'];bf=targets[1]
 require(gzip==control['existing_complete_B4_gzip_pin']==controlplan['existing_complete_B4_gzip_pin']and entry==control['existing_B4_member0_entry_pin']and index==control['existing_B4_all4_lookup_index_pin']and control['new_B_final55_full_pin']==bf and control['new_B_final55_independent_complete_stream_verified']is True and control['new_B_final55_streamed_decompressed_SHA']==bf['sha256']and control['new_B_final55_streamed_decompressed_length']==bf['size_bytes']==76594248 and control['gzip_blind_fullEOF_before']==control['gzip_blind_fullEOF_after']and control['gzip_blind_fullEOF_before']['sha256']==gzip['sha256']and control['gzip_blind_fullEOF_before']['size_bytes']==gzip['size_bytes']==33559716 and control['gzip_blind_fullEOF_before']['full_EOF']is True,'genuine new Bfinal complete stream restoration proof and blind2 same retained gzip; old B4m proof alone insufficient')
 require(control['old_A_Root_integer_exit_code']==1 and control['A_continuation_Root_integer_exit_code']==0 and control['A_continuation_new_material_children_started']==0 and control['old_B4_member0_proof_relabelled_as_new_B_final55_control']is False,'old A Root1/continuation0/no newchild and old m/newBfinal distinction preserved')
 for m in maps:
  p=m['target_pin']
  if m['mode']=='retained_native_copy':
   c=m['canonical_pin'];require(c in canonical and c['path']!=p['path']and (c['sha256'],c['size_bytes'])==(p['sha256'],p['size_bytes']),'each native-copy full byte map exact, no native-as-spool waiver')
  else:require(m['mode']=='existing_complete_gzip_member'and p==bf and m['canonical_gzip_pin']==gzip and m['canonical_entry_pin']==entry and m['canonical_B4_lookup_index_pin']==index,'only exact Bfinal uses complete permanent compressed original byte map')
 require(plan['complete_joint_roots']==control['complete_joint_roots']==controlplan['complete_joint_roots']and len(plan['complete_joint_roots'])==83 and plan['original_caps']==control['original_caps']==controlplan['original_caps']and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and plan['exact49_historical_absent_pins']==control['exact49_historical_absent_pins']==controlplan['exact49_historical_absent_pins'],'unchanged original83/caps/Source8 and exact prior49absence')
 expected=unique([p for p in control['retained_current7_pins']if p['path']not in{q['path']for q in targets}]+canonical+[gzip,entry,index])
 require(plan['retained_current7_pins']==expected and plan['retained_B2_current_epoch_readonly_pins']==control['retained_B2_current_epoch_readonly_pins']and plan['retained_failed_v1_current7_only_pins']==control['retained_failed_v1_current7_only_pins']and plan['retained_failed_pool_archive_current7_only_pins']==control['retained_failed_pool_archive_current7_only_pins'],'latest real control live roles minus only exact10 plus explicit canonical/gzip/entry/index, never selected-table completeness assumption')
 proofs=list(cp.values())+[plan['native_byte_control_plan_pin'],plan['native_byte_control_Source_pin'],plan['native_byte_control_author_freeze_pin'],plan['native_role_projection_pin'],plan['actual_native_byte_control_post_Source_projection_pin'],plan['actual_native_byte_control_post_Source_pin'],plan['actual_native_byte_control_post_author_freeze_pin']]
 require(plan['explicit_cumulative_metadata_file_pins']==unique(controlplan['explicit_cumulative_metadata_file_pins']+proofs)and plan['retained_archive_metadata_current7_pins']==unique(control['retained_archive_metadata_current7_pins']+proofs),'entire inherited cumulative metadata plus all new control/post proofs; no omitted external bytes')
 for key in('original_guard_build_plan_pin','original_guard_build_contract_Source_pin','original_production_inputs_Source_pin','original_production_resource_Source_pin','original_history_resource_Source_pin','original_complete_ENV_Python_B_prefix'):require(plan[key]==controlplan[key],'same frozen original guard/runtime Source roles')
 return controlplan,control

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
 d=dict(schema='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,files_deleted=False,native_original_complete_bytes_preserved_by_exact_recovery_maps=False,completed_spool_lifecycle_used_as_native_retirement_basis=False,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['actual_native_byte_control_Root0_independent_post0_complete']is True and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20,'unclosed native-control NULL draft never authorizes readonly or unlink')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'same independent Source review0 before helpers')
   controlplan=full(plan['native_byte_control_plan_pin'],budget,True);roots=plan['complete_joint_roots']
   require(roots==controlplan['complete_joint_roots']and len(roots)==len(set(roots))==83 and plan['no_new_output_root']is True and plan['original_caps']==controlplan['original_caps']and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'entire real83 no newdata root or narrowed originalcaps')
   buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin'];build=full(buildpin,budget,True);bm=module(bmpin,'native_exact10_retirement_original_build_metadata_roles',budget);READONLY_CONTEXT=(build,bm,buildpin,bmpin)
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget);production=module(plan['original_production_resource_Source_pin'],'native_exact10_retirement_original_production',budget);factory=module(plan['original_history_resource_Source_pin'],'native_exact10_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   controlplan,control=admit_native_byte_control(plan,budget);targets=plan['exact_target_pins'];canonical=plan['retained_ordered7_canonical_native_full_pins'];maps=plan['exact_ordered10_recovery_mappings'];gzip=plan['retained_complete_B4_gzip_pin'];entry=plan['retained_B4_member0_entry_pin'];index=plan['retained_B4_all4_lookup_index_pin']
   retained=unique(plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+canonical+[gzip,entry,index])
   require(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},'exact10 targets excluded from every retained role; canonical/results/docs/archives never targets')
   for p in retained:current(p)
   exact_historical_absence(plan)
   for p in targets:current(p,True);full(p,budget)
   d.update(native_original_complete_bytes_preserved_by_exact_recovery_maps=True,exact_target_pins=targets,retained_ordered7_canonical_native_full_pins=canonical,exact_ordered10_recovery_mappings=maps,retained_complete_B4_gzip_pin=gzip,retained_B4_member0_entry_pin=entry,retained_B4_all4_lookup_index_pin=index,actual_native_byte_control_closure_pins=plan['actual_native_byte_control_closure_pins'],native_byte_control_plan_pin=plan['native_byte_control_plan_pin'],native_byte_control_Source_pin=plan['native_byte_control_Source_pin'],native_role_projection_pin=plan['native_role_projection_pin'],new_B_final55_independent_complete_stream_verified=control['new_B_final55_independent_complete_stream_verified'],new_B_final55_streamed_decompressed_SHA=control['new_B_final55_streamed_decompressed_SHA'],new_B_final55_streamed_decompressed_length=control['new_B_final55_streamed_decompressed_length'],all17_original_and_canonical_native_fullEOF_proof_pins=control['all17_native_full_pins'],all17_original_and_canonical_native_fullEOF_SHA_verified=control['all17_native_fullEOF_SHA_and_stable7_verified'],complete_joint_roots=roots,original_caps=plan['original_caps'],exact49_historical_absent_pins=plan['exact49_historical_absent_pins'],future_consumer_must_restore_exact_native_role_from_explicit_map_then_admit_new_current_identity=True,historical_original_current7_identity_reused_after_restore=False,generic_missing_path_skip_authorized=False,old_A_Root_integer_exit_code=1,A_continuation_Root_integer_exit_code=0,A_continuation_new_material_children_started=0,retained_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_CURRENT_A_B_NATIVE_EXACT10_NO_UNLINK'
     and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['actual_released_pins']==[],'successful same native10 original-byte-preserved readonly; no reuse of failed check')
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
     d['status']='PARTIAL_CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT';snapshot(f,d);budget()
    require(d['actual_released_bytes']==plan['planned_released_bytes']and len(d['actual_released_pins'])==10
     and all(not os.path.lexists(p['path'])for p in targets),'only exact native10 original paths absent; all original bytes preserved in canonical copies or exact complete gzip')
    d['status']='RETIRED_CURRENT_A_B_NATIVE_EXACT10_ORIGINAL_BYTES_PRESERVED_IN_EXACT_RECOVERY_MAPS'
   else:d['status']='READONLY_READY_CURRENT_A_B_NATIVE_EXACT10_NO_UNLINK'
   d['native_redundant_originals_retired']=a.mode=='execute'
   for p in retained:current(p)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   exact_historical_absence(plan)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

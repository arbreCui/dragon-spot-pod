"""UNREADY Source: one recoverable B original and one failed partial archive; no full4 claim."""
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
 if target:require(owned,'only exact two cleanup targets owned501/nlink1; no readonly-role exception')
 elif not owned:
  require(READONLY_CONTEXT is not None,'specific frozen B3 readonly role context required')
  build,bm,buildpin,bmpin=READONLY_CONTEXT
  current(buildpin);current(bmpin);bm.current_metadata_role(p,build)
 return q
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
 require(sourceBytes-previous+len(raw)<16*2**20,'entire retirement Source/receipts16MiB before rewrite')
 f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())

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
  require(sum(q.lstat().st_size for q in BASE.rglob('*')if q.is_file())<16*2**20,'whole owning retirement Source/metadata16MiB')
  if state and(force or time.monotonic()-state['last']>=0.25):
   sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
   require(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit()
    and int(sample.stdout.strip())*1024<512*2**20,'original same-PID PS guard; system role never target')
   h=state['history'].check();j=state['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
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
 d=dict(schema='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,
  source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,
  files_deleted=False,all_complete_result_bytes_preserved=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_PLAN_V1'
    and plan['Source_admission_ready']is True and plan['draft_unready']is False,'NULL draft is never admitted')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
    and peer['source_pin']==ps and peer['plan_pin']==pp,'actual independent frozen Source review0')
   archiveplan=full(plan['inherited_complete_archive_plan_pin'],budget,True)
   roots=plan['complete_joint_roots'];require(roots==plan['actual_archive_complete_prefix']==archiveplan['complete_joint_roots']
    and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']
    and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b), 'entire actual archive latest prefix; no reset or new retirement output root')
   buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin']
   build=full(buildpin,budget,True);bm=module(bmpin,'B4_retirement_original_build_metadata_roles',budget)
   require(buildpin==archiveplan['original_guard_build_plan_pin']and bmpin==archiveplan['original_guard_build_contract_Source_pin'],'exact inherited frozen readonly role delegation')
   READONLY_CONTEXT=(build,bm,buildpin,bmpin)
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
   production=module(plan['original_production_resource_Source_pin'],'B4_retirement_original_production',budget)
   factory=module(plan['original_history_resource_Source_pin'],'B4_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),
    joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   cp=plan['actual_failed_archive_closure_pins'];host=full(cp['Host'],budget,True);raw=full(cp['Root_tools'],budget,True)
   failure=full(cp['first_failure'],budget,True);watch=full(cp['watchdog'],budget,True)
   post=full(cp['post'],budget,True);posttools=full(cp['post_tools'],budget,True)
   r=raw['actual_terminal_return'];require(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
    and raw['original_integer_exit_code']==1 and type(r['exit_code'])is int and r['exit_code']==1 and 'session_id'not in r
    and raw['exact_executed_command']==full(plan['actual_failed_archive_published_CLI_pin'],budget,True)['command'],'genuine original failed B4 Root1 actual published command, no successful stdout PF invented')
   genuine(posttools,'actual_review_return',cp['post'],'review_pin')
   require(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False
    and host['schema']=='ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
    and host['status']=='FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED'and host['archive_complete']is False
    and host['all4_original_products_current7_retained']is True and host['final_report_resource_check_passed']is True
    and host['original_caps']==plan['original_caps']and host['complete_joint_roots']==roots
    and len(host['records'])==1 and host['records'][0]['status']=='FAILED'
    and host['records'][0]['error']=='own-child stage failed; no retry','actual failed B4 full4 archive remains failed')
   label=host['records'][0]['label'];require(cp['watchdog']['path']==str(Path(archiveplan['planned_actual_output_root'])/(label+'.watchdog.json'))
    and type(watch['returncode'])is int and watch['returncode']==1 and watch['limit_failure']is None
    and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True
    and watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512,'actual failed child1 and unchanged original private OwnRSS guard')
   require(failure['phase']=='ARCHIVE_1'and failure['failure']=="RuntimeError('all4 gzip payload below56MiB; no compression assumption')"
    and failure['completed_entry_pins']==[plan['retained_member0_entry_pin']],'exact real phase1 partial archive, one completed member0 only')
   targets=plan['exact_target_pins'];require(len(targets)==len({p['path']for p in targets})==2
    and sum(p['size_bytes']for p in targets)==plan['planned_released_bytes']==plan['target_total_bytes']
    and targets[0]==archiveplan['all4_product_pins'][0]
    and targets[1]['path']==str(Path(archiveplan['planned_actual_output_root'])/'archives/001_u.asc.gz')
    and failure['partial_archive_paths']==[plan['retained_member0_gzip_pin']['path'],targets[1]['path']],'only exact redundant m.xsm original and failed incomplete u.asc gzip paths')
   projection=plan['actual_failure_post_key_projection']
   require(post['schema']==projection['schema']and post['status']==projection['status']and post['failure']is None
    and post['metadata_only']is True and post[projection['Host_pin_field']]==cp['Host']
    and post[projection['Root_tools_pin_field']]==cp['Root_tools']
    and post['actual_Root_integer_exit_code']==1 and post['actual_recorded_child_integer_exit_codes']==[]
    and host['actual_watchdog']is None and host['actual_child_receipt']is None,'original independent failed-Root1 post0 child_codes[] and Host NULL roles preserved')
   sp=plan['actual_failure_supplemental_post_pin'];sup=full(sp,budget,True);stools=full(plan['actual_failure_supplemental_post_tools_pin'],budget,True)
   genuine(stools,'actual_review_return',sp,'review_pin');projected=full(plan['actual_failure_supplemental_field_projection_pin'],budget,True)
   require(projected['supplement_report_pin']==sp and projected['supplement_true_tools_pin']==plan['actual_failure_supplemental_post_tools_pin']
    and sup['schema']==projected['supplement_schema']and sup['status']==projected['supplement_status']
    and sup['failure']is None and sup['metadata_only']is True,'genuine supplemental metadata0 exact recorded-field projection')
   require(sup['actual_Host_report_pin']==cp['Host']and sup['actual_Root_tools_pin']==cp['Root_tools']
    and sup['prior_post_pin']==cp['post']and sup['prior_post_tools_pin']==cp['post_tools']
    and sup['original_Host_actual_watchdog']is None and sup['original_Host_actual_child_receipt']is None
    and sup['original_prior_post_recorded_child_integer_exit_codes']==[]
    and sup['supplemental_actual_recorded_child_integer_exit_codes']==[1]
    and sup['standalone_watchdog_pin']==cp['watchdog']and sup['standalone_watchdog']==watch
    and sup['first_archive_failure_pin']==cp['first_failure']and sup['first_archive_failure']==failure
    and sup['uniquely_completed_entry000_pin']==plan['retained_member0_entry_pin']
    and sup['current_complete_member000_gzip_blind_fullEOF_twice_pin']==plan['retained_member0_gzip_pin']
    and sup['incomplete_gzip001_current7_only_pin']==targets[1]
    and sup['current_original_all4_plain_current7_only_pins']==archiveplan['all4_product_pins']
    and sup['archive_all4_complete']is False and sup['streamed_decompressed_bytes_independently_recomputed_by_supplement']is False,
    'actual standalone child1/member0/partial facts from supplemental0; never full4 success or independent stream inferred')
   ep=plan['retained_member0_entry_pin'];entry=full(ep,budget,True);pgz=plan['retained_member0_gzip_pin'];original=targets[0]
   require(sup['recorded_complete_member000']==entry and entry['ordinal']==0 and entry['original_plain_full_pin']==original and entry['compressed_archive_full_pin']==pgz
    and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==original['sha256']
    and entry['compression_input_length']==entry['streamed_decompressed_length']==original['size_bytes']
    and entry['exact_original_plain_bytes_recoverable']is True and entry['original_plain_preserved']is True,'actual member0 original stream and gzip roundtrip exact complete SHA/length proof')
   vp=plan['actual_single_member_verification_closure_pins'];verification=full(vp['Root_report'],budget,True)
   vtools=full(vp['Root_tools'],budget,True);vpost=full(vp['post'],budget,True);vposttools=full(vp['post_tools'],budget,True)
   genuine(vtools,'actual_terminal_return',vp['Root_report'],'report_pin');genuine(vposttools,'actual_review_return',vp['post'],'review_pin')
   vr=plan['actual_single_member_Root_key_projection'];vpr=plan['actual_single_member_post_key_projection']
   require(verification['schema']==vr['schema']and verification['status']==vr['status']and verification['failure']is None
    and verification[vr['entry_pin_field']]==ep and verification[vr['original_pin_field']]==original
    and verification[vr['gzip_pin_field']]==pgz and verification[vr['decompressed_SHA_field']]==original['sha256']
    and verification[vr['decompressed_length_field']]==original['size_bytes']
    and verification[vr['streamed_complete_field']]is True,'separate genuine Root0 full member0 gzip streamed decompression SHA/length proof')
   require(vpost['schema']==vpr['schema']and vpost['status']==vpr['status']and vpost['failure']is None
    and vpost['metadata_only']is True and vpost[vpr['Root_report_pin_field']]==vp['Root_report']
    and vpost[vpr['Root_tools_pin_field']]==vp['Root_tools']and vpost[vpr['entry_pin_field']]==ep
    and vpost[vpr['original_pin_field']]==original and vpost[vpr['gzip_pin_field']]==pgz
    and vpost[vpr['separate_Root_stream_proof_matched_field']]is True,'independent metadata peer0 for same separate genuine member0 Root0')
   archivepins=[pgz];full(pgz,budget)
   for p in targets:current(p,True);full(p,budget)
   require(plan['retained_other3_original_product_pins']==archiveplan['all4_product_pins'][1:]
    and len(plan['retained_other3_original_product_pins'])==3
    and plan['retained_native_current7_pins']==archiveplan['retained_native_current7_pins']
    and plan['original_B_native_and_readonly_input_current7_pins']==archiveplan['original_B_native_and_readonly_input_current7_pins']
    and len(plan['retained_native_current7_pins'])==79 and len(plan['original_B_native_and_readonly_input_current7_pins'])==11,'other three original products and all55contexts/eightXSM/sixteenSQLpool/eleven inputs retained')
   retained=plan['retained_other3_original_product_pins']+plan['retained_native_current7_pins']+plan['original_B_native_and_readonly_input_current7_pins']+plan['retained_archive_metadata_current7_pins']+archivepins+plan['explicit_cumulative_metadata_file_pins']
   require(not{p['path']for p in targets}&{p['path']for p in retained},'exact2 target set excludes every result/document/complete gzip/entry/input/context/snapshot/pair retainer')
   for p in plan['retained_other3_original_product_pins']+plan['retained_native_current7_pins']:current(p,True)
   for p in plan['original_B_native_and_readonly_input_current7_pins']+plan['retained_archive_metadata_current7_pins']:current(p)
   d.update(exact_target_pins=targets,actual_failed_archive_closure_pins=cp,actual_single_member_verification_closure_pins=vp,
    actual_failure_supplemental_post_pin=sp,actual_failure_supplemental_post_tools_pin=plan['actual_failure_supplemental_post_tools_pin'],
    compressed_result_full_pins=archivepins,retained_member0_entry_pin=ep,complete_joint_roots=roots,
    historical_original_PFs_not_current_relabelled=True,original_member0_full_pin=original,
    retained_other3_original_product_pins=plan['retained_other3_original_product_pins'],
    original_B_native_and_readonly_input_current7_pins=plan['original_B_native_and_readonly_input_current7_pins'],
    future_full4_archive_index_still_required=True,archive_lookup_required_for_future_consumer=True,
    retained_native_current7_pins=plan['retained_native_current7_pins'],
    retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_CURRENT_B4_EXACT2_RECOVERY_PATHS'
     and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['actual_released_pins']==[],'successful exact2 once readonly; no reuse of a failed check')
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
     d['status']='PARTIAL_CURRENT_B4_EXACT2_RECOVERY';snapshot(f,d);budget()
    require(d['actual_released_bytes']==plan['planned_released_bytes']and len(d['actual_released_pins'])==2
     and all(not os.path.lexists(p['path'])for p in targets),'only exact recoverable m.xsm original and failed incomplete gzip paths absent')
    d['status']='RETIRED_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED'
   else:d['status']='READONLY_READY_CURRENT_B4_EXACT2_RECOVERY_PATHS'
   for p in archivepins:current(p)
   current(plan['retained_member0_entry_pin'])
   for p in plan['retained_other3_original_product_pins']+plan['retained_native_current7_pins']:current(p,True)
   for p in plan['original_B_native_and_readonly_input_current7_pins']:current(p)
   for p in plan['retained_archive_metadata_current7_pins']:current(p)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_CURRENT_B4_EXACT2_RECOVERY'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

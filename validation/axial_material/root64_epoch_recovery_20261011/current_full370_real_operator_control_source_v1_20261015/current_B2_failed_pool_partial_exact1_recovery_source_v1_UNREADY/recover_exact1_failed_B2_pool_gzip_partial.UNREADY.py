"""UNREADY recovery Source: discard only the exact incomplete new pool gzip; every original and complete archive retained."""
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
 if target:require(owned,'only exact incomplete new pool gzip path owned501/nlink1; no readonly-role exception')
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
def current_partial(p,plan):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p==plan['exact_failed_pool_partial_current7_only_pin'],
  'only declared incomplete new pool gzip stat-only target; no fullPF/SHA or generalized exception')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes']==67099371,'exact owned failed fragment current7; body never opened or hashed')
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
def failed_pool_rows(out):
 rows=[];todo=[out]
 while todo:
  with os.scandir(todo.pop())as entries:
   for e in entries:
    st=e.stat(follow_symlinks=False);require(not stat.S_ISLNK(st.st_mode),'entire failed archive has no aliases')
    if stat.S_ISDIR(st.st_mode):todo.append(Path(e.path))
    elif stat.S_ISREG(st.st_mode):rows.append(dict(path=e.path,size_bytes=st.st_size,identity=ids(st)))
    else:raise RuntimeError('failed archive special file not admitted')
 return sorted(rows,key=lambda p:p['path'])
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
   for p in plan['retained_B2_current_epoch_readonly_pins']:
    current(p);require(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'every selected old B2 readonly role remains in original history, not fresh metadata')
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
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
 d=dict(schema='CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,
  source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,
  files_deleted=False,all_complete_result_bytes_preserved=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'
    and plan['Source_admission_ready']is True and plan['draft_unready']is False,'NULL draft is never admitted')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
    and peer['source_pin']==ps and peer['plan_pin']==pp,'actual independent frozen Source review0')
   archiveplan=full(plan['inherited_failed_pool_archive_plan_pin'],budget,True)
   roots=plan['complete_joint_roots'];require(roots==archiveplan['complete_joint_roots']and len(roots)==82
    and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']
    and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),
    'entire real failed-pool82 prefix, no root reset or new recovery data root')
   buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin']
   build=full(buildpin,budget,True);bm=module(bmpin,'B2_physical_directory_retirement_original_build_metadata_roles',budget)
   require(buildpin==archiveplan['original_guard_build_plan_pin']and bmpin==archiveplan['original_guard_build_contract_Source_pin'],'exact inherited frozen readonly role delegation')
   READONLY_CONTEXT=(build,bm,buildpin,bmpin)
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
   production=module(plan['original_production_resource_Source_pin'],'B2_physical_directory_retirement_original_production',budget)
   factory=module(plan['original_history_resource_Source_pin'],'B2_physical_directory_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),
    joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   cp=plan['actual_pool_failure_closure_pins'];host=full(cp['Host'],budget,True);raw=full(cp['Root_tools'],budget,True)
   first=full(cp['first_failure'],budget,True);watch=full(cp['watchdog'],budget,True)
   failurepost=full(cp['post'],budget,True);failuretools=full(cp['post_tools'],budget,True)
   cli=full(plan['actual_failed_pool_reviewable_CLI_pin'],budget,True)
   terminal=raw['actual_terminal_return'];require(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
    and raw['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1
    and terminal.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'
    and raw['actual_retried']is False and raw['exact_executed_command']==cli['command'],
    'real new pool archive Root1 exact executed CLI preserved, never treated as complete pair success or retried')
   genuine(failuretools,'actual_review_return',cp['post'],'review_pin')
   out=Path(archiveplan['planned_actual_output_root']);targets=plan['exact_target_pins'];partial=plan['exact_failed_pool_partial_current7_only_pin']
   require(targets==[partial]and set(partial)=={'path','size_bytes','identity'}and partial['size_bytes']==67099371
    and partial['path']==str(out/'archives/001_complete_native_original_value_bytes.bin.gz')
    and plan['planned_released_bytes']==plan['target_total_bytes']==67099371,
    'sole incomplete new gzip fragment target, never original pool, complete SQL gzip, entry or any result file')
   require(host['schema']=='ACTUAL_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
    and host['status']=='FAILED_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED'
    and host['failure']=="RuntimeError('own-child stage failed; no retry')"and host['archive_complete']is False
    and host['actual_watchdog']is None and host['actual_child_receipt']is None and host['final_report_resource_check_passed']is True
    and host['binding_pin']==plan['inherited_failed_pool_archive_plan_pin']and host['complete_joint_roots']==roots
    and host['original_caps']==plan['original_caps']and host['original_pool_current7_retained']is True
    and host['historical_SQL_original_retired']is True and len(host['records'])==1
    and host['records'][0]['status']=='FAILED'and host['records'][0]['error']=='own-child stage failed; no retry',
    'original new archive Host failure and NULL watch/receipt retained exactly')
   record=host['records'][0];require(cp['watchdog']['path']==str(out/(record['label']+'.watchdog.json'))
    and watch['command']==record['command']and type(watch['returncode'])is int and watch['returncode']==1
    and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True
    and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512
    and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'genuine per-record standalone child1, not invented embedded Host child result')
   gzip=archiveplan['reused_SQL_member0_gzip_pin'];ep=archiveplan['reused_SQL_member0_entry_pin'];pool=archiveplan['all1_plain_pins'][0]
   require(first['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_FIRST_FAILURE_V1'and first['phase']=='ARCHIVE_1'
    and first['failure']=="RuntimeError('paired gzip payload below64MiB; no compression assumption')"
    and first['completed_entry_pins']==[ep]and first['partial_archive_paths']==[partial['path']]
    and first['original_plain_files_deleted']is False and first['retry_performed']is False
    and not os.path.lexists(out/'archive_entry_001.json')
    and not os.path.lexists(out/'CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_INDEX.json')
    and not os.path.lexists(out/'ACTUAL_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_REPORT.json'),
    'exact new pool gzip64cap failure, only existing old SQL entry reused, no new pool entry/complete index/child success report')
   projection=plan['actual_failure_post_key_projection']
   require(failurepost['schema']==projection['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1'
    and failurepost['status']==projection['status']=='PASS_FAILURE_FACTS_ONLY'and failurepost['failure']is None
    and failurepost['metadata_only']is True and failurepost['actual_Host_report_pin']==cp['Host']
    and failurepost['actual_Root_tools_pin']==cp['Root_tools']and type(failurepost['actual_Root_integer_exit_code'])is int
    and failurepost['actual_Root_integer_exit_code']==1 and failurepost['actual_Host_status']==host['status']
    and failurepost['actual_Host_failure']==host['failure']and failurepost['actual_Host_embedded_watchdog']is None
    and failurepost['actual_Host_child_receipt']is None and failurepost['actual_standalone_watchdog_pin']==cp['watchdog']
    and failurepost['actual_standalone_watchdog']==watch and type(failurepost['actual_recorded_child_integer_exit_codes'])is list
    and failurepost['actual_recorded_child_integer_exit_codes']==[1]
    and all(type(x)is int for x in failurepost['actual_recorded_child_integer_exit_codes'])
    and failurepost['archive_success_or_roundtrip_or_complete_pair_inferred']is False
    and failurepost['failed_gzip_or_partial_payload_body_opened_or_hashed']is False
    and failurepost['execution_binding_pin']==plan['inherited_failed_pool_archive_plan_pin'],
    'genuine independent failurefacts post0, Root1 and explicit typed child1 list; it does not parse FIRST failure or assert restored-byte proof')
   failureRows=failurepost['failed_output_current7_only_three_field_rows']
   require(failureRows==plan['actual_failed_pool_output_current7_only_pins']and all(set(p)=={'path','size_bytes','identity'}for p in failureRows)
    and partial in failureRows and len(failureRows)==8 and failureRows==failed_pool_rows(out)
    and plan['retained_failed_pool_archive_current7_only_pins']==[p for p in failureRows if p!=partial],
    'entire closed failed archive8rows stat-only, only one fragment removed and remaining7 retained with no partial SHA invented')
   current_partial(partial,plan)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   require(plan['retained_current7_pins']==archiveplan['all1_plain_pins']+archiveplan['retained_current7_pins']
    and plan['retained_original_pool_full_pin']==pool and pool['size_bytes']==150267572
    and plan['retained_complete_SQL_gzip_pin']==gzip and plan['retained_SQL_entry_pin']==ep
    and plan['SQL_with_exact_live_original_pool_recovery_map']==archiveplan['SQL_with_exact_live_original_pool_recovery_map']
    and plan['retained_failed_v1_current7_only_pins']==archiveplan['retained_failed_v1_current7_only_pins']
    and plan['retained_B2_current_epoch_readonly_pins']==archiveplan['retained_B2_current_epoch_readonly_pins'],
    'complete original pool, old complete SQL gzip/entry/map, all native/comparison/physical/B4/docs/failed8/cold9 preserved; no bytecontrol or pair qualification needed for discarded fragment')
   historical=archiveplan['exact_historical_SQL_and_discarded_partial_target_pins']
   require(plan['prior_exact_historical_SQL_and_partial_target_pins']==historical and historical[0]==archiveplan['historical_SQL_full_pin']
    and set(historical[1])=={'path','size_bytes','identity'},'old exact SQL and old discarded partial stay historical, distinct from this new failed target')
   for p in historical:require(not os.path.lexists(p['path']),'only known retired historical paths absent; no current7/body probe or generic missing skip')
   retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']
   require(partial['path']not in{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},
    'strict partial3 target excluded from every retained fullPF/metadata/failed7 role; original pool and complete gzip never unlink targets')
   for p in plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']:current(p)
   d.update(exact_target_pins=targets,actual_pool_failure_closure_pins=cp,actual_failed_pool_output_current7_only_pins=failureRows,
    retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],
    retained_original_pool_full_pin=pool,retained_complete_SQL_gzip_pin=gzip,retained_SQL_entry_pin=ep,
    SQL_with_exact_live_original_pool_recovery_map=plan['SQL_with_exact_live_original_pool_recovery_map'],
    prior_exact_historical_SQL_and_partial_target_pins=historical,complete_joint_roots=roots,
    partial_target_body_opened_or_hashed=False,new_byte_control_executed_or_required=False,
    complete_pair_archive_success=False,original_pool_retired=False,all_complete_results_preserved=True,
    historical_original_PFs_not_current_relabelled=True,generic_missing_path_skip_authorized=False,
    retained_current7_pins=plan['retained_current7_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],
    retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],
    retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_NO_UNLINK'
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
     q=current_partial(p,plan);fd=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
     try:
      require(ids(os.stat(q.name,dir_fd=fd,follow_symlinks=False))==p['identity'],'immediate exact private target7')
      os.unlink(q.name,dir_fd=fd);os.fsync(fd);d['actual_released_pins'].append(p);d['actual_released_bytes']+=p['size_bytes'];d['files_deleted']=True
     finally:os.close(fd)
     d['status']='PARTIAL_CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_ORIGINAL_RETIREMENT';snapshot(f,d);budget()
    require(d['actual_released_bytes']==plan['planned_released_bytes']and len(d['actual_released_pins'])==1
     and all(not os.path.lexists(p['path'])for p in targets),'only exact incomplete new pool gzip path absent; complete gzip and all other result bytes retained')
    d['status']='RECOVERED_CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_INCOMPLETE_GZIP_DISCARDED'
   else:d['status']='READONLY_READY_CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_NO_UNLINK'
   current(gzip);current(ep)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   require(failed_pool_rows(out)==(failureRows if a.mode=='check'else plan['retained_failed_pool_archive_current7_only_pins']),'entire failed root retains all other7 exact stat rows after the sole target operation')
   for p in plan['retained_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']:current(p)
   for p in plan['retained_archive_metadata_current7_pins']:current(p)
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_CURRENT_B2_FAILED_POOL_PARTIAL_EXACT1_ORIGINAL_RETIREMENT'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

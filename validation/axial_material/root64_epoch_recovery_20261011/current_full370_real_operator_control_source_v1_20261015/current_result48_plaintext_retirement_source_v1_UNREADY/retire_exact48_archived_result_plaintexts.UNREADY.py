"""UNREADY Source: exact48 plain lifecycle only after genuine complete archive/post0."""
import argparse,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts')
SYSTEM={'/bin/ps':'a06fe087161557f1f8c030672eaedcd90bc6a8e92b8f2d44e07cffedc3349205',
 '/usr/sbin/lsof':'deff85c7b4750a948a69fcd48eae3b394a37575e5048e5eb4a35b7a0482c3dc8'}
FALSE=dict(numerical_executed=False,compiler_executed=False,JSONL_or_array_values_decoded=False,
 compression_repeated=False,decompression_repeated=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,target=False):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
  and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'exact integer fullPF')
 q=Path(p['path']);s=q.lstat();owned=s.st_uid==os.getuid()and s.st_nlink==1
 system=not target and str(q)in SYSTEM and s.st_uid==0 and s.st_nlink==1 and p['sha256']==SYSTEM[str(q)]
 compiler=not target and str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'
 compiler=compiler and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==p['identity'][3]==2
 require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and ids(s)==p['identity']and s.st_size==p['size_bytes']and(owned or system or compiler),
  'target owned501/nlink1 only; exact readonly system/compiler role exceptions are never targets')
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
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=('check','execute'),required=True)
 for role in('source','plan','review','review-tools'):ap.add_argument('--'+role+'-pin',required=True)
 ap.add_argument('--readonly-receipt-pin');a=ap.parse_args();started=time.monotonic();state={};plan=None
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
 d=dict(schema='EXACT48_ARCHIVED_RESULT_PLAINTEXT_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,
  source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,
  files_deleted=False,all_complete_result_bytes_preserved_in_archive=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='EXACT48_ARCHIVED_RESULT_PLAINTEXT_RETIREMENT_PLAN_V1'
    and plan['Source_admission_ready']is True and plan['draft_unready']is False,'NULL draft is never admitted')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
    and peer['source_pin']==ps and peer['plan_pin']==pp,'actual independent frozen Source review0')
   roots=plan['complete_joint_roots'];require(roots[:65]==plan['actual_archive_complete65_prefix']
    and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b), 'latest full prefix preserves entire archive65, no reset/new retirement output root')
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
   production=module(plan['original_production_resource_Source_pin'],'result48_retirement_original_production',budget)
   factory=module(plan['original_history_resource_Source_pin'],'result48_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),
    joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   cp=plan['actual_archive_closure_pins'];host=full(cp['Host'],budget,True);raw=full(cp['Root_tools'],budget,True)
   post=full(cp['post'],budget,True);posttools=full(cp['post_tools'],budget,True);index=full(cp['index'],budget,True)
   genuine(raw,'actual_terminal_return',cp['Host'],'report_pin');genuine(posttools,'actual_review_return',cp['post'],'review_pin')
   require(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'actual original archive permission/no retry')
   require(host['status']=='ACTUAL_ALL48_ARCHIVED_ROUNDTRIP_CLOSED0_PLAIN_RETAINED'and host['failure']is None
    and host['archive_complete']is True and host['final_report_resource_check_passed']is True
    and len(host['records'])==1 and host['records'][0]['status']=='PASS'
    and type(host['actual_watchdog']['returncode'])is int and host['actual_watchdog']['returncode']==0
    and host['actual_watchdog']['limit_failure']is None and host['actual_watchdog']['rss_cap_mib']==512,
    'real complete archive Root0/child0 original guard before plain retirement')
   projection=plan['actual_archive_post_key_projection']
   require(post['schema']==projection['schema']and post['status']==projection['status']and post['failure']is None
    and post[projection['Host_pin_field']]==cp['Host']and post[projection['Root_tools_pin_field']]==cp['Root_tools']
    and post[projection['index_pin_field']]==cp['index'],'actual audited separate post0 projection, no invented future fields')
   targets=plan['exact_target_pins'];rows=index['entries'];require(len(targets)==len(rows)==48
    and len({p['path']for p in targets})==48 and sum(p['size_bytes']for p in targets)==805236925
    and [r['original_plain_full_pin']for r in rows]==targets,'exact48 complete original lookup; all results survive')
   archivepins=[]
   for r,p in zip(rows,targets):
    require(r['compression_input_SHA']==r['streamed_decompressed_SHA']==p['sha256']
     and r['compression_input_length']==r['streamed_decompressed_length']==p['size_bytes']
     and r['exact_original_plain_bytes_recoverable']is True and r['original_plain_preserved']is True,'actual full-stream verified decomposition byte proof')
    archivepins.append(r['compressed_archive_full_pin']);full(r['compressed_archive_full_pin'],budget)
    full(r['entry_pin'],budget)
    current(p,True);full(p,budget)
   require(post[projection['ordered_original_pins_field']]==targets
    and post[projection['ordered_archive_pins_field']]==archivepins,'independent actual metadata post exact48 fullPF scope')
   require(post['metadata_only']is True and post['all48_plain_current7_retained']is True
    and post['compressed48_fullEOF_SHA_current7_verified_twice']is True
    and post['Root_actual_streamed_decompression_proofs_matched_original_fullPF']is True
    and post['actual_Root_integer_exit_code']==post['actual_child_integer_exit_code']==0
    and post['old30_historical_guard_pins']==plan['old30_historical_guard_pins']
    and post['new5_completed_A2_result_pins']==plan['new5_completed_A2_result_pins'], 'actual independent post scope and exact old30/new5 role map')
   require(len(plan['old30_historical_guard_pins'])==30 and len(plan['new5_completed_A2_result_pins'])==5
    and all(p in targets for p in plan['old30_historical_guard_pins']+plan['new5_completed_A2_result_pins']), 'only genuinely consumed historical/result roles')
   for p in plan['retained_native_current7_pins']:current(p,True)
   for p in plan['retained_archive_metadata_current7_pins']:current(p)
   d.update(exact_target_pins=targets,actual_archive_closure_pins=cp,compressed_result_full_pins=archivepins,
    complete_joint_roots=roots,historical_original_PFs_not_current_relabelled=True,original_lookup_index_pin=cp['index'],
    old30_historical_guard_pins=plan['old30_historical_guard_pins'],new5_completed_A2_result_pins=plan['new5_completed_A2_result_pins'],
    archive_lookup_required_for_future_consumer=True,retained_native_current7_pins=plan['retained_native_current7_pins'],
    retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_EXACT48_ARCHIVED_RESULT_PLAINTEXTS'
     and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['actual_released_pins']==[],'successful exact48 once readonly; no reuse of a failed check')
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
     d['status']='PARTIAL_EXACT48_ARCHIVED_RESULT_PLAINTEXT_RETIREMENT';snapshot(f,d);budget()
    require(d['actual_released_bytes']==805236925 and all(not os.path.lexists(p['path'])for p in targets),'only exact48 plaintext paths absent')
    d['status']='RETIRED_EXACT48_PLAINTEXTS_COMPLETE_RESULT_BYTES_IN_ARCHIVE'
   else:d['status']='READONLY_READY_EXACT48_ARCHIVED_RESULT_PLAINTEXTS'
   for p in archivepins:current(p)
   current(cp['index'])
   for p in plan['retained_native_current7_pins']:current(p,True)
   for p in plan['retained_archive_metadata_current7_pins']:current(p)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_EXACT48_ARCHIVED_RESULT_PLAINTEXT_RETIREMENT'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

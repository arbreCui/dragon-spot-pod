"""UNREADY Source: exact one Bagg presence original only after single archive Root0/child0/post0."""
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
 if target:require(owned,'only exact one presence original owned501/nlink1; no readonly-role exception')
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
   for p in plan['retained_B2_current_epoch_readonly_pins']:
    current(p);require(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'every selected old B2 readonly role remains in original history, not fresh metadata')
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
 d=dict(schema='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,
  source_pin=ps,plan_pin=pp,peer_review_pin=pr,peer_tools_pin=pt,actual_released_pins=[],actual_released_bytes=0,
  files_deleted=False,all_complete_result_bytes_preserved=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);peer=full(pr,budget,True);tools=full(pt,budget,True)
   require(plan['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'
    and plan['Source_admission_ready']is True and plan['draft_unready']is False,'NULL draft is never admitted')
   genuine(tools,'actual_review_return',pr,'review_pin')
   require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
    and peer['source_pin']==ps and peer['plan_pin']==pp,'actual independent frozen Source review0')
   archiveplan=full(plan['inherited_complete_archive_plan_pin'],budget,True)
   roots=plan['complete_joint_roots'];require(roots==plan['actual_archive_complete_prefix']==archiveplan['complete_joint_roots']
    and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']
    and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b), 'entire actual archive latest prefix; no reset or new retirement output root')
   buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin']
   build=full(buildpin,budget,True);bm=module(bmpin,'presence_retirement_original_build_metadata_roles',budget)
   require(buildpin==archiveplan['original_guard_build_plan_pin']and bmpin==archiveplan['original_guard_build_contract_Source_pin'],'exact inherited frozen readonly role delegation')
   READONLY_CONTEXT=(build,bm,buildpin,bmpin)
   module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
   production=module(plan['original_production_resource_Source_pin'],'presence_retirement_original_production',budget)
   factory=module(plan['original_history_resource_Source_pin'],'presence_retirement_original_history',budget)
   state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),
    joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0);budget(True);d['resources_before']=state['latest']
   cp=plan['actual_archive_closure_pins'];host=full(cp['Host'],budget,True);raw=full(cp['Root_tools'],budget,True)
   child=full(cp['child_report'],budget,True);index=full(cp['index'],budget,True)
   post=full(cp['post'],budget,True);posttools=full(cp['post_tools'],budget,True)
   genuine(raw,'actual_terminal_return',cp['Host'],'report_pin');genuine(posttools,'actual_review_return',cp['post'],'review_pin')
   require(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False
    and host['schema']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
    and host['status']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'
    and host['failure']is None and host['archive_complete']is True and host['final_report_resource_check_passed']is True
    and host['original_caps']==plan['original_caps']and host['complete_joint_roots']==roots
    and host['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(host['records'])==1
    and host['records'][0]['status']=='PASS'and host['actual_child_receipt']['report_pin']==cp['child_report']
    and host['all1_original_plain_current7_retained']is True,'actual single-presence archive Root0 and one complete guarded child report')
   watch=host['actual_watchdog'];require(type(watch['returncode'])is int and watch['returncode']==0
    and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True
    and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512
    and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'real original private OwnRSS one-child archive0 guard')
   require(child['schema']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'
    and child['status']=='SINGLE_BAGG_PRESENCE_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None
    and child['completed_count']==1 and child['all1_original_plain_current7_retained']is True
    and child['index_pin']==cp['index']and child['binding_pin']==plan['inherited_complete_archive_plan_pin'], 'complete single-presence child0 proof')
   targets=plan['exact_target_pins'];rows=index['entries'];original=archiveplan['actual_presence_original_pin']
   require(len(targets)==len({p['path']for p in targets})==1 and targets==archiveplan['all1_plain_pins']==[original]
    and original['path']==plan['exact_presence_original_path']and original['sha256']=='9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7'
    and original['size_bytes']==169615994==plan['planned_released_bytes']==plan['target_total_bytes'], 'only exact complete presence original, never other aggregate output or native role')
   require(index['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'
    and index['status']=='SINGLE_BAGG_PRESENCE_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'
    and index['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(rows)==1
    and index['ordered_original_plain_count']==1 and index['ordered_original_plain_total_bytes']==169615994
    and index['all1_original_plain_retained']is True and index['future_consumer_must_use_exact_single_presence_archive_mapping']is True
    and index['generic_missing_path_skip_authorized']is False,'actual exact ordered index1, generic absent-path skip never authorized')
   row=rows[0];require(row['ordinal']==0 and row['original_plain_full_pin']==original
    and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']
    and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']
    and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True
    and row['actual_Bagg_output_role']=='COMPLETE_PRESENCE_BRANCH_AND_MISSING_LEDGER','complete original/compressed/decompressed SHA-length proof metadata')
   entry=full(row['entry_pin'],budget,True)
   require(entry=={k:v for k,v in row.items()if k!='entry_pin'}and entry['original_plain_preserved']is True,'exact entry creation metadata and original-preserved history retained unchanged')
   archivepins=[row['compressed_archive_full_pin']];entrypins=[row['entry_pin']]
   require(archivepins==plan['retained_presence_gzip_pins']and entrypins==plan['retained_presence_entry_pins'],'single exact complete archive and entry permanently retained')
   full(archivepins[0],budget)
   projection=plan['actual_archive_post_key_projection']
   require(post['schema']==projection['schema']and post['status']==projection['status']and post['failure']is None and post['metadata_only']is True
    and post['actual_Host_report_pin']==cp['Host']and post['actual_Root_tools_pin']==cp['Root_tools']
    and post['actual_archive_index_pin']==cp['index']and post['actual_child_report_pin']==cp['child_report']
    and post['execution_binding_pin']==plan['inherited_complete_archive_plan_pin']
    and post['original_presence_full_pin']==original and post['compressed_presence_archive_full_pin']==archivepins[0]
    and post['presence_entry_pin']==entrypins[0]and post['complete_joint_roots']==roots,'actual independent single-presence archive metadata post0 exact scope')
   require(type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0
    and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==0
    and post['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True
    and post['original_presence_current7_verified_twice_only']is True and post['compressed_presence_fullEOF_SHA_current7_verified_twice']is True,
    'independent actual Root0/child0 complete byte-proof facts; no future successful post inferred')
   prior=full(archiveplan['latest_complete_plan_pin'],budget,True);life=prior['exact_B4_product_lifecycle_binding']
   require(plan['retained_Bagg_output_current7_pins']==archiveplan['retained_Bagg_output_current7_pins']
    and len(plan['retained_Bagg_output_current7_pins'])==16 and original not in plan['retained_Bagg_output_current7_pins']
    and plan['retained_native_current7_pins']==archiveplan['retained_native_current7_pins']
    and plan['retained_current7_pins']==archiveplan['retained_current7_pins']
    and archiveplan['retained_native_current7_pins']==life['ordered_exact4_current_archive_pins']+life['ordered_exact4_current_entry_pins']+[life['complete4_archive']['index_pin']]+prior['prospective_worker_live_input_pins'],
    'all sixteen other Bagg outputs, original full8pairs/55contexts inputs and B4 all4 gzip/entries/index exact retained')
   bridge=full(archiveplan['actual_current_epoch_B2_bridge_report_pin'],budget,True)
   bridgetools=full(archiveplan['actual_current_epoch_B2_bridge_tools_pin'],budget,True)
   genuine(bridgetools,'actual_terminal_return',archiveplan['actual_current_epoch_B2_bridge_report_pin'],'report_pin')
   require(bridge['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'
    and bridge['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bridge['failure']is None
    and bridge['complete_joint_roots']==archiveplan['inherited_latest_complete_joint_roots']and bridge['original_caps']==plan['original_caps']
    and bridge['final_report_resource_check_passed']is True and len(bridge['ordered_role_pairs'])==9
    and plan['retained_B2_current_epoch_readonly_pins']==[r['current_epoch_full_pin']for r in bridge['ordered_role_pairs']],
    'exact nine independently bridged historical readonly roles retained, never deleted or recertified as all4790')
   for r in bridge['ordered_role_pairs']:
    require(r['blind_complete_SHA_and_length_equal']is True and r['before_open_EOF_after_current7_stable']is True
     and r['current_epoch_full_pin']['sha256']==r['historical_full_pin']['sha256']
     and r['current_epoch_full_pin']['size_bytes']==r['historical_full_pin']['size_bytes'],'genuine recorded bridge equality preserved; no repeated large-body read')
    current(r['current_epoch_full_pin'])
   retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+archivepins+entrypins+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']
   require(not{p['path']for p in targets}&{p['path']for p in retained},'exact1 excludes all archives/entries/index/reports/meta/other Bagg outputs/native/cold readonly inputs')
   for p in targets:current(p,True);full(p,budget)
   for p in plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+entrypins:current(p)
   d.update(exact_target_pins=targets,actual_archive_closure_pins=cp,compressed_result_full_pins=archivepins,
    retained_presence_entry_pins=entrypins,original_lookup_index_pin=cp['index'],complete_joint_roots=roots,
    historical_original_PFs_not_current_relabelled=True,archive_lookup_required_for_future_consumer=True,
    future_consumer_must_use_exact_single_presence_archive_mapping=True,generic_missing_path_skip_authorized=False,
    exact_presence_complete_result_bytes_preserved_in_archive=True,retained_Bagg_output_current7_pins=plan['retained_Bagg_output_current7_pins'],
    retained_native_current7_pins=plan['retained_native_current7_pins'],retained_current7_pins=plan['retained_current7_pins'],
    retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],
    retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'])
   snapshot(f,d)
   if a.mode=='execute':
    require(a.readonly_receipt_pin is not None,'genuine separately completed readonly receipt required')
    pcheck=json.loads(a.readonly_receipt_pin);check=full(pcheck,budget,True)
    require(pcheck['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_CURRENT_BAGG_PRESENCE_EXACT1_ARCHIVED_ORIGINAL'
     and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['actual_released_pins']==[],'successful exact1 presence once readonly; no reuse of a failed check')
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
     d['status']='PARTIAL_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT';snapshot(f,d);budget()
    require(d['actual_released_bytes']==plan['planned_released_bytes']and len(d['actual_released_pins'])==1
     and all(not os.path.lexists(p['path'])for p in targets),'only exact one presence original absent; complete gzip and all other result bytes retained')
    d['status']='RETIRED_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'
   else:d['status']='READONLY_READY_CURRENT_BAGG_PRESENCE_EXACT1_ARCHIVED_ORIGINAL'
   for p in archivepins:current(p)
   for p in plan['retained_presence_entry_pins']:current(p)
   current(plan['actual_archive_closure_pins']['index'])
   for p in plan['retained_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']:current(p)
   for p in plan['retained_archive_metadata_current7_pins']:current(p)
   budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True;snapshot(f,d)
  except BaseException as error:
   d['status']='FAILED_PARTIAL_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(error);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)

if __name__=='__main__':main()

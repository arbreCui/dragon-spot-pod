"""Retire only the three completed A text exports; keep all XSMs and results."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts')
PREFIX=ART/'axial-material-new-current-formal-material-observations-short-FIL-after-v18-saved370-20261014-v10/A'
TARGETS=[
 dict(path=str(PREFIX/'microlib.ascii'),sha256='c63c3ab85b3a00bd6feccc25811cf6f32b808d12c44503deb7019c6cf631932f',size_bytes=305414157,identity=[16777229,50145157,33188,1,305414157,1791957877204003582,1791957877204003582]),
 dict(path=str(PREFIX/'macro.ascii'),sha256='1ef4420e14d3c478c061f8b15b5967404c607a6b4a90103a0e32d013d5f592b5',size_bytes=39546544,identity=[16777229,50145163,33188,1,39546544,1791957877365472131,1791957877365472131]),
 dict(path=str(PREFIX/'metadata.ascii'),sha256='18e83af7823ad6582a0df8b462d018533bfe273a205b0f467936ef5dd07c3d0d',size_bytes=1901272,identity=[16777229,50145164,33188,1,1901272,1791957877383316271,1791957877383316271])]
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'complete integer PF')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and s.st_size==p['size_bytes']and ident(s)==p['identity']and not any(a.is_symlink()for a in(q,*q.parents)),'same ordinary owned current7')
 return q
def current_identity(p):
 need(set(p)=={'path','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'honest identity-only retained role')
 q=Path(p['path']);s=q.lstat();need(ident(s)==p['identity']and s.st_size==p['size_bytes']and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents)),'retained identity-only7')
def full(p,budget,parse=False):
 q=current(p);need(not parse or p['size_bytes']<8*2**20,'bounded metadata8MiB')
 digest=hashlib.sha256();parts=[];size=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   raw=os.read(fd,2**20)
   if not raw:break
   digest.update(raw);size+=len(raw)
   if parse:parts.append(raw)
   budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 current(p);need(size==p['size_bytes']and digest.hexdigest()==p['sha256'],'blind EOF SHA')
 return json.loads(b''.join(parts))if parse else None
def pin(q):
 s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=ident(s));current(p);return p
def snapshot(f,d):
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'receipt8MiB')
 f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())
def module(p,name,budget):
 full(p,budget);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=['check','execute'],required=True)
 for role in('source','plan','review'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 ap.add_argument('--readonly-receipt-pin')
 a=ap.parse_args();started=time.monotonic();last=0.0;resources={}
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'original SELF512/stage600, also whole1800')
  if resources and time.monotonic()-resources['last']>=0.25:
   h=resources['history'].check();j=resources['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
   unlinked={}
   for fd in os.listdir('/dev/fd'):
    try:s=os.fstat(int(fd))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30,'same complete cumulative2GiB')
   need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/meta/fresh2/free8 reservations')
   resources['last']=time.monotonic();resources['latest']=dict(history_bytes=h['artifact_bytes'],joint_bytes=j['artifact_bytes'],external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),disk_free_bytes=j['disk_free_bytes'],SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-started)
 def arg(role):
  ids=json.loads(getattr(a,role+'_seven_id'));return dict(path=getattr(a,role+'_summary'),sha256=getattr(a,role+'_sha256'),size_bytes=ids[4],identity=ids)
 ps=arg('source');pp=arg('plan');pr=arg('review')
 need(ps['path']==str(Path(__file__).absolute())and pp['path']==str(BASE/'PLAN.json'),'literal Source/plan')
 receipt=BASE/('READONLY_RECEIPT.json'if a.mode=='check'else'EXECUTION_RECEIPT.json')
 d=dict(schema='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,source_pin=ps,plan_pin=pp,peer_review_pin=pr,exact_target_pins=TARGETS,actual_released_pins=[],actual_released_bytes=0,raw_export_lifecycle_only=True,duplicate_byte_identity_claim=False,all14_earlier_SQL_pool_files_retained=True,original_A_aggregate_issue1_preserved=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);review=full(pr,budget,True)
   need(plan['schema']=='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_PLAN_V1'and plan['target_pins']==TARGETS and plan['planned_released_bytes']==346861973,'only exact3 completed ASCII exports')
   need(review['status'].startswith('PASS')and review['failure']is None and review['source_pin']==ps and review['plan_pin']==pp,'peer same exact Source/plan')
   need(len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==62,'complete62 prefix; no new ledger namespace')
   failure=full(plan['prior_readonly_failure_true_tools_pin'],budget,True);need(failure['observed_closed']is True and type(failure['original_integer_exit_code'])is int and failure['original_integer_exit_code']==failure['actual_readonly_return']['exit_code']==1 and failure['execute_invoked']is False and failure['files_deleted']is False,'genuine prior readonly failure1 retained, no execute')
   old_check=full(plan['prior_failed_readonly_receipt_pin'],budget,True);need(old_check['status']=='FAILED_BEFORE_UNLINK'and old_check['actual_released_pins']==[]and old_check['actual_released_bytes']==0,'old failed check unchanged, no lost file')
   inputs=module(plan['original_production_inputs_Source_pin'],'production_inputs',budget);need(Path(inputs.__file__).absolute()==Path(plan['original_production_inputs_Source_pin']['path']),'original exact production_inputs import origin')
   production=module(plan['original_production_resource_Source_pin'],'literal3_export_production',budget);factory=module(plan['original_history_resource_Source_pin'],'literal3_export_history',budget)
   resources.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),joint=production.DiskResources(ART.parent,plan['complete_joint_roots'],8*2**30,2*2**30),last=0.0)
   budget();d['resources_before']=resources['latest']
   closed=full(plan['closure_pins']['completion_post'],budget,True);tools=full(plan['closure_pins']['completion_post_tools'],budget,True);root=full(plan['closure_pins']['completion_root_tools'],budget,True)
   need(closed['status']=='PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'and closed['failure']is None and closed['actual_material_stage_closed0']is True and closed['actual_new_material_child_launch_count']==0 and closed['actual_Root_integer_exit_code']==0 and closed['actual_original_Root_integer_exit_code']==1,'original completed native lifecycle; historical Root1 retained')
   for v,k in((tools,'actual_review_return'),(root,'actual_terminal_return')):
    t=v[k];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine original closure0')
   need(json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']==plan['closure_pins']['completion_post'],'exact closure post stdout')
   manifest=full(plan['closure_pins']['observation_manifest'],budget,True);extract=full(plan['closure_pins']['complete_extraction_report'],budget,True)
   need(closed['actual_observation_manifest_pin']==plan['closure_pins']['observation_manifest'],'exact original manifest')
   state=manifest['states']['A'];need(manifest['state_order']==['A']and state['actual_material_child_closed_before_manifest']is True and state['all_actual_events_and_snapshots_saved']is True and len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8 and all(p in state['actual_material_product_pins']for p in TARGETS),'exact completed A exports and all original context/snapshots')
   need(extract['actual_observation_manifest_pin']==plan['closure_pins']['observation_manifest']and extract['state_order']==['A']and extract['all_complete_state_scope_retained']is True and extract['all_handles_closed_between_snapshots']is True and len(extract['states']['A'])==8 and all(r['ASCII_used_or_invented']is False for r in extract['states']['A']),'downstream complete XSM extraction used no ASCII exports')
   for p in plan['retained_current7_pins']:current(p)
   for p in plan['retained_identity_only_roles']:current_identity(p)
   for p in TARGETS:full(p,budget)
   d['retained_current7_pins']=plan['retained_current7_pins'];d['closure_pins']=plan['closure_pins'];d['complete_joint_roots']=plan['complete_joint_roots']
   if a.mode=='execute':
    need(a.readonly_receipt_pin is not None,'true readonly receipt')
    pcheck=json.loads(a.readonly_receipt_pin);need(pcheck['path']==str(BASE/'READONLY_RECEIPT.json'),'literal readonly receipt')
    check=full(pcheck,budget,True);need(check['status']=='READONLY_READY_EXACT_LITERAL3_A_EXPORTS'and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['peer_review_pin']==pr and check['actual_released_pins']==[],'prior exact successful readonly check')
    command=['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in TARGETS]
    r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
    need(len(r.stdout)+len(r.stderr)<2*2**20,'bounded current open-owner check')
    d['actual_lsof_owner_check']=dict(argv=command,returncode=r.returncode,stdout=r.stdout.decode('utf-8'),stderr=r.stderr.decode('utf-8'))
    need(r.returncode==1 and r.stdout==b''and r.stderr==b'','no current open file owner; do not unlink live exports')
    budget();snapshot(f,d)
    for p in TARGETS:
     q=current(p);fd=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
     try:
      need(ident(os.stat(q.name,dir_fd=fd,follow_symlinks=False))==p['identity'],'immediate target7')
      os.unlink(q.name,dir_fd=fd);d['actual_released_pins'].append(p);d['actual_released_bytes']+=p['size_bytes'];os.fsync(fd)
     finally:os.close(fd)
     d['status']='PARTIAL_EXACT_LITERAL3_A_EXPORTS';snapshot(f,d);budget()
    need(d['actual_released_bytes']==346861973 and all(not os.path.lexists(p['path'])for p in TARGETS),'all exact3 retired')
    d['status']='RETIRED_EXACT_LITERAL3_COMPLETED_A_ASCII_EXPORTS_ONLY'
   else:d['status']='READONLY_READY_EXACT_LITERAL3_A_EXPORTS'
   for p in plan['retained_current7_pins']:current(p)
   for p in plan['retained_identity_only_roles']:current_identity(p)
   budget();d['resources_after']=resources['latest'];snapshot(f,d);budget()
  except BaseException as e:
   d['status']='FAILED_PARTIAL_EXACT_LITERAL3_A_EXPORTS'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(e);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)
if __name__=='__main__':main()


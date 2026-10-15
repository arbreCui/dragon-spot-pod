"""Separate-executor metadata post draft. No old plain reads, decompression or unlink."""
import argparse,hashlib,json,os,resource,shlex,stat,time
from pathlib import Path

BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
AUTHOR_TASK='/root/formal_goal_remaining_audit'
FALSE=dict(worker_or_resource_helpers_imported=False,old_plain_or_scientific_body_opened=False,
 old_plain_or_scientific_SHA_recomputed=False,JSONL_or_array_values_decoded=False,numerical_executed=False,
 compression_repeated=False,decompression_repeated=False,retirement_repeated=False,PS_executed=False,lsof_executed=False,
 files_deleted_by_post=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def cur(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1
  and s.st_uid==os.getuid()and ids(s)==p['identity']and s.st_size==p['size_bytes']
  and not any(a.is_symlink()for a in(q,*q.parents)),'ordinary retained current7')
 return q
def full(p,budget):
 q=cur(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 cur(p);need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind fullEOF SHA/current7')
def read(p,budget):
 need(p['size_bytes']<8*2**20,'metadata8MiB');full(p,budget);v=json.loads(Path(p['path']).read_bytes());full(p,budget);return v
def pin(q,budget):
 s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  while b:=f.read(2**20):h.update(b);budget()
 need(ids(q.lstat())==ids(s),'own metadata stable')
 return dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
def genuine(d,key,p,role):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int
  and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0
  and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[role]==p,'genuine original closed0 exact stdout PF')
def resource_check(d):
 h=d['history'];j=d['joint'];ps=d['actual_PS_return']
 need(d['SELF_peak_bytes']<512*2**20 and d['elapsed_seconds']<600
  and ps['returncode']==0 and ps['stderr']==''and ps['stdout'].strip().isdigit()
  and int(ps['stdout'].strip())*1024<512*2**20,'actual saved original SELF/PS/stage600 withinwhole1800')
 need(j['artifact_budget_bytes']==2*2**30 and h['artifact_budget_bytes']==96*2**30
  and j['artifact_bytes']+d['external_metadata_bytes']+d['open_unlinked_bytes']<2*2**30
  and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30
  and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'saved full joint/history/cold/free original cap facts')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('receipt','execution-tools','readonly-receipt','readonly-tools'):ap.add_argument('--'+role+'-pin',required=True)
 ap.add_argument('--executor-task-name',required=True);a=ap.parse_args();started=time.monotonic()
 need(a.executor_task_name.startswith('/root/')and a.executor_task_name!=AUTHOR_TASK,'separate actual executor, not Source author')
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if __import__('sys').platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'post SELF512/stage600')
 pr=json.loads(a.receipt_pin);pt=json.loads(a.execution_tools_pin);pc=json.loads(a.readonly_receipt_pin);pct=json.loads(a.readonly_tools_pin)
 receipt=read(pr,budget);raw=read(pt,budget);check=read(pc,budget);checktools=read(pct,budget)
 authorP=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json',budget);author=read(authorP,budget);plan=read(author['whole_plan_pin'],budget)
 need(pr['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and pc['path']==str(PACKAGE/'READONLY_RECEIPT.json')
  and receipt['schema']=='EXACT48_ARCHIVED_RESULT_PLAINTEXT_RETIREMENT_RECEIPT_V1','exact literal package/receipt schema')
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
  and type(raw['actual_execution_return']['exit_code'])is int
  and raw['actual_execution_return']['exit_code']==raw['original_integer_exit_code'],'actual original closed integer preserved')
 targets=plan['exact_target_pins'];need(len(targets)==48 and sum(p['size_bytes']for p in targets)==805236925,'exact48 plaintext scope')
 need(receipt['source_pin']in author['whole_Source_file_pins']and receipt['plan_pin']==author['whole_plan_pin'],'same frozen Source/PLAN')
 for p in author['whole_Source_file_pins']:full(p,budget);full(p,budget)
 # Nonzero is failurefacts only; never rerun retirement or manufacture complete absence.
 if raw['original_integer_exit_code']!=0:
  observed=[]
  for p in targets:
   present=os.path.lexists(p['path'])
   if present:cur(p)
   observed.append(dict(original_full_pin=p,present=present))
  review=dict(schema='EXACT48_RETIREMENT_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,
   actual_execution_receipt_pin=pr,actual_Root_execution_tools_pin=pt,actual_Root_integer_exit_code=raw['original_integer_exit_code'],
   actual_failed_receipt_status=receipt['status'],actual_failed_receipt_failure=receipt['failure'],actual_released_pins=receipt['actual_released_pins'],
   actual_released_bytes=receipt['actual_released_bytes'],observed48_path_states=observed,completion_or_physics_inferred=False,**FALSE)
 else:
  genuine(raw,'actual_execution_return',pr,'receipt_pin');genuine(checktools,'actual_readonly_return',pc,'receipt_pin')
  need(raw['actual_execution_permission_mode']=='require_escalated'
   and checktools['actual_readonly_permission_mode']=='require_escalated','original PS/lsof permission route, no guard bypass')
  need(receipt['mode']=='execute'and receipt['status']=='RETIRED_EXACT48_PLAINTEXTS_COMPLETE_RESULT_BYTES_IN_ARCHIVE'
   and receipt['failure']is None and receipt['files_deleted']is True
   and receipt['actual_released_pins']==receipt['exact_target_pins']==targets and receipt['actual_released_bytes']==805236925,'only exact48 actual released plain paths')
  need(check['mode']=='check'and check['status']=='READONLY_READY_EXACT48_ARCHIVED_RESULT_PLAINTEXTS'
   and check['failure']is None and check['files_deleted']is False and check['actual_released_pins']==[]
   and check['source_pin']==receipt['source_pin']and check['plan_pin']==receipt['plan_pin'],'same original readonly0 before actual unlink')
  peer=read(receipt['peer_review_pin'],budget);peerTools=read(receipt['peer_tools_pin'],budget)
  genuine(peerTools,'actual_review_return',receipt['peer_review_pin'],'review_pin')
  need(peer['source_only']is True and peer['status'].startswith('PASS')and peer['failure']is None
   and peer['source_pin']==receipt['source_pin']and peer['plan_pin']==receipt['plan_pin'],'actual independent Source peer0')
  cliPins=[]
  for name,r in [('ROOT_READONLY_REVIEWABLE_CLI.json',checktools),('ROOT_EXECUTE_REVIEWABLE_CLI.json',raw)]:
   p=pin(PACKAGE/name,budget);cli=read(p,budget);cliPins.append(p)
   need(shlex.split(r['exact_executed_command'])==cli['argv']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual command equals frozen mode CLI')
  owner=receipt['actual_lsof_owner_check']
  need(owner['returncode']==1 and owner['stdout']==owner['stderr']==''
   and owner['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets],'actual immediate lsof no-owner proof for exact48')
  for _ in range(2):
   for p in targets:need(not os.path.lexists(p['path']),'exact48 absent twice')
   for p in plan['retained_all48_gzip_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_native_current7_pins']:cur(p)
  need(receipt['compressed_result_full_pins']==plan['retained_all48_gzip_pins']and len(receipt['compressed_result_full_pins'])==48,'every compressed result retained')
  for p in plan['retained_all48_gzip_pins']:full(p,budget);full(p,budget)
  cp=plan['actual_archive_closure_pins'];archiveIndex=read(cp['index'],budget)
  need([r['original_plain_full_pin']for r in archiveIndex['entries']]==targets
   and [r['compressed_archive_full_pin']for r in archiveIndex['entries']]==plan['retained_all48_gzip_pins'], 'unchanged complete byte recovery lookup; no deleted result content')
  need(receipt['old30_historical_guard_pins']==plan['old30_historical_guard_pins']
   and receipt['new5_completed_A2_result_pins']==plan['new5_completed_A2_result_pins']
   and len(plan['old30_historical_guard_pins'])==30 and len(plan['new5_completed_A2_result_pins'])==5,'old30/new5 exact archived historical roles')
  need(receipt['complete_joint_roots']==plan['complete_joint_roots']and len(plan['complete_joint_roots'])==65,'whole actual65 prefix, no new output/reset')
  need(receipt['resources_after_original_classes_forced_fresh']is True
   and check['resources_after_original_classes_forced_fresh']is True,'saved force-fresh original resource class calls')
  for facts in(receipt['resources_before'],receipt['resources_after'],check['resources_before'],check['resources_after']):resource_check(facts)
  before=receipt['resources_before'];after=receipt['resources_after']
  need(after['history']['checked_unix']>=before['history']['checked_unix']
   and after['joint']['checked_unix']>=before['joint']['checked_unix']and after['elapsed_seconds']>=before['elapsed_seconds'], 'saved resource clocks advance within original run')
  need(all(receipt[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','numerical_executed','JSONL_or_array_values_decoded')),'lifecycle only, physical and goal flags false')
  review=dict(schema='EXACT48_ARCHIVED_PLAINTEXT_ACTUAL_RETIREMENT_METADATA_POSTVERIFY_V1',
   status='PASS_ACTUAL_EXACT48_PLAINTEXT_RETIREMENT_805236925B_COMPLETE_RESULT_ARCHIVES_RETAINED_METADATA_ONLY',failure=None,
   actual_execution_receipt_pin=pr,actual_Root_execution_tools_pin=pt,actual_Root_integer_exit_code=0,
   actual_readonly_receipt_pin=pc,actual_readonly_tools_pin=pct,actual_readonly_integer_exit_code=0,
   Source_author_freeze_pin=authorP,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],
   actual_mode_CLI_pins=cliPins,actual_released_pins=targets,actual_released_bytes=805236925,exact48_absence_verified_twice=True,
   complete48_archives_fullEOF_SHA_and_current7_verified_twice=True,all66_native_current7_verified_twice_only=True,
   all_archive_index_entries_reports_and_metadata_current7_retained=True,actual_archive_index_pin=cp['index'],actual_archive_closure_pins=cp,
   retained48_gzip_pins=plan['retained_all48_gzip_pins'],old30_historical_guard_pins=plan['old30_historical_guard_pins'],
   new5_completed_A2_result_pins=plan['new5_completed_A2_result_pins'],historical_plain_PFs_not_claimed_current=True,
   future_consumer_requires_exact_retirement_receipt_and_archive_lookup=True,complete_joint_roots=plan['complete_joint_roots'],original_caps=plan['original_caps'],
   execute_resource_facts=after,readonly_resource_facts=check['resources_after'],
   force_fresh_after_unlink_supported_by_frozen_Source_order_and_saved_flag=True,
   last_unlink_timestamp_recorded=False,no_unrecorded_unlink_timestamp_invented=True,**FALSE)
 review.update(metadata_only=True,Source_author_task=AUTHOR_TASK,actual_executor_task=a.executor_task_name,
  Source_author_also_authored_retirement_workflow=True,actual_assessment_not_self_executed_by_Source_author=True,
  wall_seconds=time.monotonic()-started,reviewer_Source_pin=pin(Path(__file__).absolute(),budget))
 target=BASE/'REVIEW.json';b=(json.dumps(review,indent=2,allow_nan=False)+'\n').encode();need(len(b)<8*2**20,'own review8MiB')
 with target.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=review['status'],review_pin=pin(target,budget))),flush=True)

if __name__=='__main__':main()

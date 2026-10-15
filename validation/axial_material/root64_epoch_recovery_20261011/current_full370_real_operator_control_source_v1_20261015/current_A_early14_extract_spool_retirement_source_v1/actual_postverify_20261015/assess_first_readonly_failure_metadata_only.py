"""Frozen independent readonly1 failure facts; never imports worker, runs PS or deletes."""
import hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent

def need(v,m):
 if v is not True:raise ValueError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and
  ident(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7 '+str(q));return s
def pin(q):
 q=Path(q);s=q.lstat();r=q.read_bytes();return dict(path=str(q),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=ident(s))
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'bounded Source/metadata8MiB')
 q=Path(p['path'])
 with q.open('rb')as f:
  need(ident(os.fstat(f.fileno()))==p['identity'],'Source/meta opened7');r=f.read();need(ident(os.fstat(f.fileno()))==p['identity'],'Source/meta EOF7')
 need(len(r)==p['size_bytes']and hashlib.sha256(r).hexdigest()==p['sha256'],'exact Source/meta SHA');current(p);return r
def read(p):return json.loads(full(p))
def unique(rows):
 d={}
 for p in rows:need(p['path']not in d or d[p['path']]==p,'consistent PF');d[p['path']]=p
 return list(d.values())
def genuine0(d,key,chunk,p,field):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and
  type(r['exit_code'])is int and r['exit_code']==0 and r['chunk_id']==chunk and r.get('session_id')is None and
  json.loads(r['output'].strip().splitlines()[-1])[field]==p,'genuine original0/PF')

def main():
 ptools=pin(D/'ROOT_READONLY_TRUE_TOOL_RETURNS.json');need(ptools['sha256']=='4faae2ed5b912fd27a11911c30ce1890c84ac177c1e720715cf4fc5bc9b28fe3'and ptools['size_bytes']==4325,'exact Root readonly1 raw')
 preceipt=pin(D/'READONLY_RECEIPT.json');need(preceipt['sha256']=='6de0f657bd960b2fe2f1e5c599698b0d0f7c2ca7708991e037fc90bb9a025699'and preceipt['size_bytes']==11999,'exact closed failed metadata receipt')
 pcli=pin(D/'ROOT_READONLY_REVIEWABLE_CLI.json');tools=read(ptools);receipt=read(preceipt);cli=read(pcli)
 t=tools['actual_readonly_return'];need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==1 and
  type(t['exit_code'])is int and t['exit_code']==1 and t.get('session_id')is None and t['chunk_id']=='4a4090'and
  tools['actual_readonly_permission_mode']=='require_escalated'and tools['readonly_retried']is False,'genuine failed readonly1/no retry')
 need(receipt['schema']=='LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='check'and receipt['status']=='FAILED_BEFORE_UNLINK'and
  receipt['failure']=="RuntimeError('same ordinary owned current7')"and receipt['actual_released_pins']==[]and receipt['actual_released_bytes']==0 and receipt['files_deleted']is False,'original failed readonly facts only/no unlink')
 need("for p in plan['retained_current7_pins']:current_metadata(p)"in t['output']and 'same ordinary owned current7'in t['output'],'raw failure retained ownership-gate traceback')
 need(cli['mode']=='check'and cli['source_pin']==receipt['source_pin']and cli['plan_pin']==receipt['plan_pin']and
  cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['command']==tools['exact_executed_command']and
  cli['actual_readonly_receipt_pin']is None and cli['actual_readonly_tools_pin']is None,'same exact published check command/source/plan/review')
 author=read(pin(D/'AUTHOR_SOURCE_FREEZE.json'));plan=read(receipt['plan_pin']);peer=read(cli['independent_Source_review_pin']);peer_tools=read(cli['independent_Source_review_tools_pin'])
 need(author['whole_Source_pin']==receipt['source_pin']and author['whole_plan_pin']==receipt['plan_pin']and peer['source_only']is True and
  peer['status'].startswith('PASS')and peer['failure']is None and peer['source_pin']==receipt['source_pin']and peer['plan_pin']==receipt['plan_pin'],'preserved Sourcepeer PASS is Source-only, not runtime success')
 genuine0(peer_tools,'actual_review_return','f073c2',cli['independent_Source_review_pin'],'review_pin')
 selected=unique(peer['selected_Source_and_metadata_pins']+[ptools,preceipt,pcli,cli['independent_Source_review_pin'],cli['independent_Source_review_tools_pin']])
 raw={p['path']:full(p)for p in selected};targets=plan['target_pins'];retained=plan['retained_current7_pins']
 need(len(targets)==14 and sum(p['size_bytes']for p in targets)==149659264 and receipt['exact_target_pins']==targets and len(retained)==6006,'same exact14 and6006 retained roles')
 for p in retained+targets:current(p)
 owner_roles=[]
 for p in retained:
  s=current(p)
  if s.st_uid!=os.getuid():owner_roles.append(dict(pin=p,observed_owner_uid=s.st_uid,current7_unchanged=True))
 need({r['pin']['path']for r in owner_roles}=={'/bin/ps','/usr/sbin/lsof'}and all(r['observed_owner_uid']==0 for r in owner_roles)and os.getuid()==501,'only exact two unchanged system-tool metadata ownership roles')
 for p in targets:need(current(p).st_uid==os.getuid()and p['identity'][3]==1,'all target owned single-link guards remain valid')
 worker=raw[receipt['source_pin']['path']].decode();need('s.st_uid==os.getuid()'in worker and 'else:current(p)'in worker and
  worker.index("for p in plan['retained_current7_pins']:current_metadata(p)")<worker.index('for p in TARGETS:full(p,budget)'),'failure before target blindEOF/lsof/execute path from exact Source')
 for p in plan['retained_identity_only_roles']+plan['new_A_result_JSONL_current7_pins']:current(p)
 need(len(plan['retained_identity_only_roles'])==43 and len(plan['new_A_result_JSONL_current7_pins'])==5,'all43 old and5 new result documents preserved')
 cp=plan['closure_pins'];root=json.loads(raw[cp['new_A_Root_tools']['path']]);posttools=json.loads(raw[cp['new_A_post_tools']['path']]);post=json.loads(raw[cp['new_A_post']['path']])
 genuine0(root,'actual_terminal_return','da510e',cp['new_A_host'],'report_pin');genuine0(posttools,'actual_review_return','4d14cc',cp['new_A_post'],'review_pin')
 need(post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2 and post['actual_compared_source_fields']==19249 and
  post['actual_context_event_count']==55 and post['actual_snapshot_count']==8 and post['actual_all_mismatch_elements']==post['actual_unknown_macro_producers']==post['actual_context_or_operand_issues']==0 and
  post['prior_actual_v1_Root1_child1_preserved']is True and post['old_issue1_report_not_rewritten']is True,'original A2 and v1 facts preserved')
 need(len(plan['complete_joint_roots'])==64 and peer['complete_joint_roots']==plan['complete_joint_roots'],'complete64 resource prefix preserved')
 absent=[D/n for n in('ROOT_EXECUTE_REVIEWABLE_CLI.json','EXECUTION_RECEIPT.json','ROOT_EXECUTION_TRUE_TOOL_RETURNS.json')]
 need(all(not os.path.lexists(q)for q in absent),'execute was never published or invoked in failed v1 namespace')
 need('resources_after'not in receipt and 'actual_same_PID_PS_RSS_samples'not in receipt and 'actual_lsof_owner_check'not in receipt,'no fabricated final-resource/PS sample/lsof evidence')
 for p in selected:full(p)
 for p in retained+targets+plan['retained_identity_only_roles']+plan['new_A_result_JSONL_current7_pins']:current(p)
 need(all(not os.path.lexists(q)for q in absent),'still no execute artifacts')
 report=dict(schema='INDEPENDENT_EARLY14_FIRST_READONLY_FAILURE_METADATA_ASSESSMENT_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,metadata_only=True,source_only=True,
  actual_readonly_true_tools_pin=ptools,actual_failed_readonly_receipt_pin=preceipt,actual_readonly_cli_pin=pcli,actual_readonly_return=t,
  original_actual_readonly_integer_exit_code=1,actual_readonly_permission_mode='require_escalated',original_readonly_failure=receipt['failure'],readonly_retried=False,
  source_pin=receipt['source_pin'],plan_pin=receipt['plan_pin'],author_Source_freeze_pin=pin(D/'AUTHOR_SOURCE_FREEZE.json'),
  original_Source_peer_review_pin=cli['independent_Source_review_pin'],original_Source_peer_true_tools_pin=cli['independent_Source_review_tools_pin'],
  original_Source_only_PASS_not_reclassified_as_runtime_success=True,actual_released_pins=[],actual_released_bytes=0,actual_released_count=0,
  exact_target_pins=targets,all14_targets_still_live_current7_verified_twice=True,all6006_retained_current7_verified_twice=True,
  all43_old_identity_roles_and_new5_results_current7_only_preserved=True,complete_joint_roots=plan['complete_joint_roots'],original_caps=plan['original_caps'],
  exact_unchanged_system_tool_metadata_owner_roles=owner_roles,observed_worker_uid=os.getuid(),
  underlying_failure_is_readonly_metadata_owner_gate_before_target_EOF_and_unlink=True,target_owned501_guard_unchanged_and_valid=True,
  original_A2_Root0_child2_and_actual_post0_pins=cp,original_A2_19249_55events8trees0counts_preserved=True,old_A_v1_failure_and_issue1_preserved=True,
  original_recorded_resources_before=receipt['resources_before'],final_resources_after_available=False,sampled_live_PS_RSS_peak_available=False,
  final_resource_PASS_or_0MiB_PS_memory_claim=False,execute_artifacts_absent=[str(q)for q in absent],actual_execution_was_started=False,
  Source_metadata_fullEOF_current7_twice_pins=selected,Source_metadata_fullEOF_count=len(selected),
  reviewer_source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),
  worker_or_helpers_imported=False,readonly_or_retirement_repeated=False,business_executed=False,numerical_executed=False,compiler_executed=False,
  PS_executed=False,lsof_executed=False,files_deleted=False,scientific_bodies_opened=False,scientific_body_SHA_recomputed=False,JSONL_or_array_values_decoded=False,
  physics_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()

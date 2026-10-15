"""Prepared bounded actual14 metadata post; run only after Root supplies terminal PFs."""
import argparse,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent
ROLES={'execute-receipt':'EXECUTION_RECEIPT.json','execute-tools':'ROOT_EXECUTION_TRUE_TOOL_RETURNS.json',
 'readonly-receipt':'READONLY_RECEIPT.json','readonly-tools':'ROOT_READONLY_TRUE_TOOL_RETURNS.json',
 'execute-cli':'ROOT_EXECUTE_REVIEWABLE_CLI.json','readonly-cli':'ROOT_READONLY_REVIEWABLE_CLI.json'}

def need(v,m):
 if v is not True:raise ValueError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and
  ident(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7 '+str(q))
def pin(q):
 q=Path(q);s=q.lstat();r=q.read_bytes();return dict(path=str(q),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=ident(s))
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'bounded exact Source/report/receipt metadata8MiB')
 with Path(p['path']).open('rb')as f:
  need(ident(os.fstat(f.fileno()))==p['identity'],'metadata opened7');r=f.read();need(ident(os.fstat(f.fileno()))==p['identity'],'metadata EOF7')
 need(len(r)==p['size_bytes']and hashlib.sha256(r).hexdigest()==p['sha256'],'whole metadata SHA');current(p);return r
def read(p):return json.loads(full(p))
def unique(rows):
 d={}
 for p in rows:need(p['path']not in d or d[p['path']]==p,'consistent fullPF');d[p['path']]=p
 return list(d.values())
def actual(d,key,p,field,expected):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==expected and
  type(r['exit_code'])is int and r['exit_code']==expected and r.get('session_id')is None,'genuine original typed terminal return')
 if expected==0:need(json.loads(r['output'].strip().splitlines()[-1])[field]==p,'genuine exact stdout receipt/PF')
 return r
def resources(d,unlinked):
 need(d['resources_after_original_classes_forced_fresh']is True and d['resources_after_measured_after_all_requested_unlinks']is unlinked,'original forced-fresh resource closure')
 r=d['resources_after'];start=d['resources_after_fresh_scan_started_unix'];need(r['history_checked_unix']>=start and r['joint_checked_unix']>=start,'both original classes measured after fresh start')
 need(r['SELF_peak_bytes']<512*2**20 and r['elapsed_seconds']<600 and r['joint_bytes']+r['external_metadata_bytes']+r['open_unlinked_bytes']<2*2**30 and
  r['history_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and r['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original SELF512/stage600/fresh2/history96/cold/free8')
 samples=d['actual_same_PID_PS_RSS_samples'];last=samples['last_actual_return'];need(type(samples['sample_count'])is int and samples['sample_count']>0 and
  0<samples['sampled_peak_rss_bytes']<512*2**20 and last['returncode']==0 and last['stderr']==''and last['stdout'].strip().isdigit()and
  int(last['stdout'].strip())*1024<=samples['sampled_peak_rss_bytes']and last['argv'][:4]==['/bin/ps','-o','rss=','-p']and
  len(last['argv'])==5 and last['argv'][4].isdigit()and int(last['argv'][4])>0,'recorded original same-PID PS samples/peak; no fake0MiB')
 return dict(original_resources_after=r,original_same_PID_PS_RSS_samples=samples,original_PS_recorded_PID=int(last['argv'][4]))

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in ROLES:ap.add_argument('--'+role+'-pin',required=True)
 a=ap.parse_args();pf={role:json.loads(getattr(a,role.replace('-','_')+'_pin'))for role in ROLES}
 need(pf==json.loads((BASE/'EXACT_ACTUAL_METADATA_ARGUMENTS.json').read_text())['role_pins'],'exact frozen original6 actual metadata PFinteger arguments')
 for role,p in pf.items():need(p['path']==str(D/ROLES[role]),'literal actual role '+role)
 values={role:read(p)for role,p in pf.items()};executed=values['execute-receipt'];readonly=values['readonly-receipt'];et=values['execute-tools'];rt=values['readonly-tools'];ec=values['execute-cli'];rc=values['readonly-cli']
 need(type(et['original_integer_exit_code'])is int and et['original_integer_exit_code']in(0,1),'actual execute terminal0 or preserved1')
 code=et['original_integer_exit_code'];er=actual(et,'actual_execution_return',pf['execute-receipt'],'receipt_pin',code);rr=actual(rt,'actual_readonly_return',pf['readonly-receipt'],'receipt_pin',0)
 need(et['actual_execution_permission_mode']=='require_escalated'and rt['actual_readonly_permission_mode']=='require_escalated','unchanged actual permission routes')
 need(et['execution_retried']is False and rt['readonly_retried']is False and er['chunk_id']=='92150e'and rr['chunk_id']=='c0ba8e','exact original execute/readonly terminal chunks/no retry')
 need(rc['mode']=='check'and ec['mode']=='execute'and ec['actual_readonly_receipt_pin']==pf['readonly-receipt']and ec['actual_readonly_tools_pin']==pf['readonly-tools'],'true readonly0 required by exact execute CLI')
 for cli,tools in((rc,rt),(ec,et)):need(cli['command']==tools['exact_executed_command'],'same exact published and executed command')
 author=read(pin(D/'AUTHOR_SOURCE_FREEZE.json'));plan=read(author['whole_plan_pin']);peer_pin=ec['independent_Source_review_pin'];peer_tools_pin=ec['independent_Source_review_tools_pin'];peer=read(peer_pin);peer_tools=read(peer_tools_pin)
 pr=actual(peer_tools,'actual_review_return',peer_pin,'review_pin',0);need(pr['chunk_id']=='a1e8ab'and peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS'),'actual v2 Sourcepeer0')
 need(author['whole_plan_pin']['sha256']=='34198096fbd8d941e6f91c3a19d258d830074a572f2e37dffb2ca64f23a382ab'and author['whole_Source_pin']['sha256']=='60c7c7e127fb547d48a79cbc1ec0cdf3cf60cac5350d0b03db8723eca0126e92','same reviewed v2 Source/plan')
 for d in(readonly,executed):need(d['source_pin']==author['whole_Source_pin']and d['plan_pin']==author['whole_plan_pin']and d['peer_review_pin']==peer_pin and d['exact_target_pins']==plan['target_pins'],'same exact actual Source/plan/14 target scope')
 need(readonly['status']=='READONLY_READY_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'and readonly['mode']=='check'and readonly['failure']is None and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False,'genuine completed readonly0 without deletion')
 readonly_resources=resources(readonly,False)
 selected=unique(peer['selected_Source_and_metadata_pins']+list(pf.values())+[peer_pin,peer_tools_pin]);raw={p['path']:full(p)for p in selected}
 cp=plan['closure_pins'];root=json.loads(raw[cp['new_A_Root_tools']['path']]);posttools=json.loads(raw[cp['new_A_post_tools']['path']]);actual(root,'actual_terminal_return',cp['new_A_host'],'report_pin',0);actual(posttools,'actual_review_return',cp['new_A_post'],'review_pin',0)
 target=plan['target_pins'];need(len(target)==14 and sum(p['size_bytes']for p in target)==149659264,'exact14 release bound')
 released=executed['actual_released_pins'];need(len({p['path']for p in released})==len(released)and all(p in target for p in released)and executed['actual_released_bytes']==sum(p['size_bytes']for p in released),'exact released fullPF membership/bytes')
 retained=plan['retained_current7_pins'];need(len(retained)==6016 and not({p['path']for p in target}&{p['path']for p in retained}),'6016 retained projection excludes only actual target roles')
 for p in retained+plan['retained_identity_only_roles']+plan['new_A_result_JSONL_current7_pins']:current(p)
 for p in target:
  if p in released:need(not os.path.lexists(p['path']),'actual released target absent')
  else:current(p)
 if code==0:
  need(executed['mode']=='execute'and executed['status']=='RETIRED_EXACT_LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOLS_ONLY'and executed['failure']is None and
   released==target and executed['actual_released_bytes']==149659264 and executed['files_deleted']is True,'genuine exact14 actual retirement0')
  execute_resources=resources(executed,True);lsof=executed['actual_lsof_owner_check'];need(lsof['returncode']==1 and lsof['stdout']==lsof['stderr']==''and
   lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in target],'actual lsof1-empty exact14 owner check')
  status='PASS_ACTUAL_EXACT14_COMPLETED_A_DERIVED_SPOOL_RETIREMENT_149659264B_METADATA_ONLY'
 else:
  need(executed['failure']is not None and executed['status']in('FAILED_BEFORE_UNLINK','FAILED_PARTIAL_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'),'original actual execution1 failure facts only')
  execute_resources=None;status='PASS_FAILURE_FACTS_ONLY'
 for d in(readonly,executed):
  for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(d[k]is False,'lifecycle never physics qualification')
 for p in selected:full(p)
 for p in retained+plan['retained_identity_only_roles']+plan['new_A_result_JSONL_current7_pins']:current(p)
 for p in target:
  if p in released:need(not os.path.lexists(p['path']),'released path still absent')
  else:current(p)
 report=dict(schema='INDEPENDENT_EARLY14_V2_ACTUAL_RETIREMENT_METADATA_POSTVERIFY_V1',status=status,failure=None,metadata_only=True,source_only=True,
  actual_execution_receipt_pin=pf['execute-receipt'],actual_Root_execution_tools_pin=pf['execute-tools'],actual_readonly_receipt_pin=pf['readonly-receipt'],actual_readonly_tools_pin=pf['readonly-tools'],
  actual_execute_cli_pin=pf['execute-cli'],actual_readonly_cli_pin=pf['readonly-cli'],actual_Root_integer_exit_code=code,actual_readonly_integer_exit_code=0,
  actual_execution_return=er,actual_readonly_return=rr,original_actual_execution_failure=executed['failure'],actual_released_pins=released,actual_released_bytes=executed['actual_released_bytes'],
  exact14_absence_current7_verified_twice=code==0,all6016_retained_current7_verified_twice=True,all43_original_identity_and_new5_result_roles_preserved=True,
  original_XSM_and_final55_SQL_pool_pair_retained=True,source_pin=author['whole_Source_pin'],plan_pin=author['whole_plan_pin'],
  author_Source_freeze_pin=pin(D/'AUTHOR_SOURCE_FREEZE.json'),Source_peer_review_pin=peer_pin,Source_peer_true_tools_pin=peer_tools_pin,
  original_v1_readonly_failure1_preserved=True,prior_v1_failurefacts_post_pin=plan['prior_readonly_failure_post_pin'],prior_v1_failurefacts_post_tools_pin=plan['prior_readonly_failure_post_tools_pin'],
  original_A2_Root0_child2_post0_closure_pins=cp,complete_joint_roots=plan['complete_joint_roots'],original_caps=plan['original_caps'],
  readonly_resource_facts=readonly_resources,execute_resource_facts=execute_resources,actual_resource_guards_passed=code==0,
  Source_metadata_fullEOF_current7_twice_pins=selected,Source_metadata_fullEOF_count=len(selected),old_scientific_payload_body_opened=False,old_scientific_payload_SHA_recomputed=False,
  old_Host_fixed_list_treated_as_consumed_history_not_current_live=True,historical5937_table_unchanged=True,
  future_current_live_historical_input_count_only_after_exact14_actual0_post0=5920 if code==0 else None,independent_numerical_recomparison_performed=False,
  reviewer_source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),worker_or_helpers_imported=False,
  retirement_or_business_repeated=False,business_executed=False,numerical_executed=False,compiler_executed=False,PS_executed=False,lsof_executed=False,files_deleted=False,
  JSONL_or_array_values_decoded=False,physics_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()

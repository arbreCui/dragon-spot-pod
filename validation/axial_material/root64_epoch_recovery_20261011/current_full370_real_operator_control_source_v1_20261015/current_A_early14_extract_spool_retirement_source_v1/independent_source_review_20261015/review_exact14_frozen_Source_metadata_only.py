"""Independent exact14 lifecycle Source review; imports no candidate or science module."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent

def need(v,message):
 if v is not True:raise ValueError(message)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and
  ident(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7 '+str(q))
def full(p):
 current(p);need(p['size_bytes']<8*2**20,'Source/control metadata8MiB')
 q=Path(p['path'])
 with q.open('rb')as f:
  need(ident(os.fstat(f.fileno()))==p['identity'],'opened Source/meta7');raw=f.read()
  need(ident(os.fstat(f.fileno()))==p['identity'],'EOF Source/meta7')
 need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole Source/meta SHA');current(p);return raw
def pin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes()
 return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s))
def unique(rows):
 d={}
 for p in rows:
  need(p['path']not in d or d[p['path']]==p,'consistent fullPF');d[p['path']]=p
 return list(d.values())
def genuine(d,key,chunk,p,field):
 r=d[key]
 need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and
  type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and r['chunk_id']==chunk and
  json.loads(r['output'].strip().splitlines()[-1])[field]==p,'genuine original typed0 and exact stdout PF')
def function(s,name):
 return ast.get_source_segment(s,next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name==name))

def main():
 pa=pin(D/'AUTHOR_SOURCE_FREEZE.json');need(pa['sha256']=='c081bd028169212459dadc4a30122e43136a58f08ce06c9efc48c6f8955e9c6b'and pa['size_bytes']==6007,'exact supplied author freeze')
 author=json.loads(full(pa));pp=author['whole_plan_pin'];ps=author['whole_Source_pin']
 need(pp['sha256']=='cd2cd2b2f052e6853e8a1cd05e022ba5287e51de14c41a978dc1f8e0b94f0c7e'and pp['size_bytes']==2970665 and
  ps['sha256']=='dfa02083a831ef5d674d86903393b44af8b38de4b631720a1e977a4898d302e2'and ps['size_bytes']==23911,'exact frozen plan/worker')
 plan=json.loads(full(pp));need(author['Source_frozen_before_peer_review']is True and author['author_Source_writes_stopped_after_this_freeze']is True and
  author['Source_or_modules_imported_by_author']is False and author['check_or_execute_invoked']is False and
  author['science_bodies_opened_or_hashed_by_author']is False,'author Source-only stop')
 source_roles=['original_verified_literal3_v2_Source_pin','original_production_inputs_Source_pin','original_production_resource_Source_pin',
  'original_history_resource_Source_pin','original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin']
 meta_roles=['candidate_registry_pin','actual_completed_A_plan_pin','original_result43_saved_fullPF_registry_pin',
  'original_first_failed_A_Root1_child1_raw_pin','original_first_failed_A_failurefacts_post_pin']
 selected=unique([pa,pp,author['whole_inverse_pin'],author['CLI_templates_pin']]+author['whole_Source_file_pins']+
  [plan[k]for k in source_roles+meta_roles]+list(plan['closure_pins'].values())+[plan['historical_input_reference_packet']['original_request_full_pin']])
 raw={p['path']:full(p)for p in selected}
 need(plan['original_caps']==author['original_caps']and plan['original_caps']==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
  fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
  free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),'complete original resource caps')
 for p in author['whole_Source_file_pins']:ast.parse(raw[p['path']].decode(),filename=p['path'])
 worker=raw[ps['path']].decode();publisher_pin=next(p for p in author['whole_Source_file_pins']if p!=ps);publisher=raw[publisher_pin['path']].decode()
 target_literal=next(n.value for n in ast.parse(worker).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='TARGETS'for t in n.targets))
 targets=ast.literal_eval(target_literal);need(targets==plan['target_pins']and len(targets)==14 and sum(p['size_bytes']for p in targets)==149659264,'literal exact14/149659264')
 need(len({p['path']for p in targets})==len({tuple(p['identity'][:2])for p in targets})==14,'distinct exact target paths/nodes')
 for p in targets:current(p);need(p['identity'][3]==1,'single-link target')
 inverse=json.loads(raw[author['whole_inverse_pin']['path']]);oldworker=raw[plan['original_verified_literal3_v2_Source_pin']['path']].decode()
 lines=worker.splitlines(keepends=True)
 for edit in reversed(inverse['ordered_inverse_blocks']):
  start=edit['new_line_start']-1;end=start+len(edit['new_lines']);need(lines[start:end]==edit['new_lines'],'inverse exact new Source block');lines[start:end]=edit['original_lines']
 need(''.join(lines)==oldworker,'whole original validated literal3v2 worker restored')
 for name in inverse['unchanged_whole_functions']:need(function(worker,name)==function(oldworker,name),'whole original function '+name)
 need(len(inverse['unchanged_whole_functions'])==8 and inverse['original_resource_classes_modified']is False,'eight whole helper functions/no resource class edit')
 need(worker.index("inputs=module(plan['original_production_inputs_Source_pin']")<worker.index("production=module(plan['original_production_resource_Source_pin']"),'exact original production_inputs preload')
 for fragment in ("r.returncode==1 and r.stdout==b''and r.stderr==b''",'os.stat(q.name,dir_fd=fd,follow_symlinks=False)',
  'os.unlink(q.name,dir_fd=fd)',"receipt.open('xb')",'os.fsync(fd)',"command=['/bin/ps','-o','rss=','-p',str(os.getpid())]",
  "resources['last']=0.0;fresh_started_unix=time.time();budget()",
  "resources['latest']['history_checked_unix']>=fresh_started_unix and resources['latest']['joint_checked_unix']>=fresh_started_unix"):
  need(fragment in worker,'reviewed exact resource/unlink/no-overwrite gate')
 need("genuine(ct,'actual_readonly_return',checkpin,'receipt_pin')"in publisher and "ct['actual_readonly_permission_mode']=='require_escalated'"in publisher and
  "genuine(tools,'actual_review_return',pr,'review_pin')"in publisher and "not os.path.lexists(outfile)"in publisher,'exact check then execute publication Source gates')
 closure={k:json.loads(raw[p['path']])for k,p in plan['closure_pins'].items()};cp=plan['closure_pins'];host=closure['new_A_host'];post=closure['new_A_post'];req=closure['new_A_execution_request']
 genuine(closure['new_A_Root_tools'],'actual_terminal_return','da510e',cp['new_A_host'],'report_pin')
 genuine(closure['new_A_post_tools'],'actual_review_return','4d14cc',cp['new_A_post'],'review_pin')
 need(closure['new_A_Root_tools']['actual_execution_permission_mode']=='require_escalated'and closure['new_A_Root_tools']['actual_retried']is False,'actual A2 proper permission/no retry')
 need(host['status']=='ACTUAL_CURRENT_A_FULL_MATH_CONTROL_EVIDENCE_EXIT2_CLOSED_ONLY'and host['failure']is None and host['actual_child_evidence_only_integer_exit_code']==2 and
  host['original_runner_FAILED_record_not_reclassified']is True and host['current_source_gap_resolved']is True and host['final_report_resource_check_passed']is True,'A2 Root0/child2 original FAILED retained')
 evidence=host['actual_evidence'];fact=evidence['states'][0]
 need(evidence['state_order']==['A']and len(evidence['states'])==1 and evidence['error']is None and fact['original_context_event_count']==55 and
  fact['all_original_snapshot_count']==8 and fact['complete_source_field_comparisons']==19249 and fact['all_mismatching_elements']==fact['unknown_macro_producers']==fact['all_context_or_operand_issues']==0 and
  [x['phase']for x in fact['phase_results']]==['scattering','scalar','fission','extras','overv_fallback','metadata']and
  all(x['computation_finished']is True for x in fact['phase_results']),'complete recorded A sixphase/19249/55/8/zero counts')
 need(post['schema']==plan['actual_A_post_schema']=='INDEPENDENT_ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_METADATA_POSTVERIFY_V1'and
  post['status']==plan['actual_A_post_status']=='PASS_RECORDED_CURRENT_A_FULL_AGGREGATE_SOURCE_GAP0_METADATA_ONLY_CHILD2_PRESERVED'and post['failure']is None and
  post['actual_Host_report_pin']==cp['new_A_host']and post['actual_Root_tools_pin']==cp['new_A_Root_tools']and post['actual_execution_request_pin']==cp['new_A_execution_request']and
  post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2 and post['original_FAILED_error2_record_retained']is True and
  post['prior_actual_v1_Root1_child1_preserved']is True and post['old_issue1_report_not_rewritten']is True,'exact independent actual post0; no old failure laundering')
 old_request=json.loads(raw[plan['historical_input_reference_packet']['original_request_full_pin']['path']]);history=old_request['complete_input_pins'];live=req['complete_input_pins'];pairs=req['aggregation_binding']['actual_context_states']['A']['all_snapshot_pairs']
 need(len(history)==5937 and len(live)==5949 and req['current_live_historical_input_count']==5934 and len(pairs)==8,'immutable history5937/live role5934/actual proof union5949')
 need(req['historical_complete_input_pins']==plan['historical_input_reference_packet']and hashlib.sha256(json.dumps(history,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==plan['historical_input_reference_packet']['ordered_fullPF_canonical_sha256'],'whole original historical table/digest preserved')
 expected=[pair[k]for pair in pairs[:-1]for k in('sqlite_pin','native_pool_pin')]
 need({p['path']:p for p in expected}=={p['path']:p for p in targets}and all(p in history and p in live for p in targets),'targets are only all seven earlier derived pairs actually consumed')
 need(pairs[-1]['event']==55 and pairs[-1]['sqlite_pin']==plan['retained_final55_SQLite_pin']and pairs[-1]['native_pool_pin']==plan['retained_final55_pool_pin'],'final55 numerical pair retained')
 completed=json.loads(raw[plan['actual_completed_A_plan_pin']['path']]);need(plan['complete_joint_roots']==completed['complete_joint_roots']==req['joint_archive_roots']and
  len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==64,'entire completed64 prefix unchanged')
 retained=plan['retained_current7_pins'];need(len(retained)==6006 and not ({p['path']for p in retained}&{p['path']for p in targets}),'6006 retained roles disjoint from exact14')
 for p in retained:current(p)
 for p in plan['retained_identity_only_roles']:current(p)
 registry=json.loads(raw[plan['original_result43_saved_fullPF_registry_pin']['path']]);need(len(registry['selected_pins'])==43 and len(plan['retained_identity_only_roles'])==43,'all original43 result metadata')
 need({p['path']:{k:v for k,v in p.items()if k!='sha256'}for p in registry['selected_pins']}=={p['path']:p for p in plan['retained_identity_only_roles']},'43 identity roles match exact saved fullPF metadata')
 for p in registry['selected_pins']+plan['new_A_result_JSONL_current7_pins']:current(p)
 need(len(plan['new_A_result_JSONL_current7_pins'])==5 and len(plan['retained_seven_original_observer_XSM_pins'])==7,'all new5 results and original7 earlier XSM retained')
 for p in plan['retained_seven_original_observer_XSM_pins']+[plan['retained_final55_XSM_pin'],plan['retained_original_A_material_XSM_pin']]:current(p);need(p not in targets,'XSM not a target')
 failed=json.loads(raw[plan['original_first_failed_A_Root1_child1_raw_pin']['path']]);failurepost=json.loads(raw[plan['original_first_failed_A_failurefacts_post_pin']['path']])
 need(failed['original_integer_exit_code']==1 and failed['actual_terminal_return']['exit_code']==1 and failurepost['actual_Root_integer_exit_code']==failurepost['actual_child_integer_exit_code']==1,'original failed A v1 Root1/child1 unchanged')
 for k in ('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(host[k]is False,'current evidence not physics qualification')
 for p in selected:full(p)
 for p in retained+targets+registry['selected_pins']+plan['new_A_result_JSONL_current7_pins']:current(p)
 report=dict(schema='INDEPENDENT_EXACT14_COMPLETED_A_DERIVED_SPOOL_RETIREMENT_SOURCE_REVIEW_V1',status='PASS_FROZEN_SOURCE_ONLY_EXACT14_COMPLETED_A_SQL_POOL_LIFECYCLE_AND_ORIGINAL_RESOURCE_GATES',failure=None,
  source_only=True,source_pin=ps,plan_pin=pp,author_Source_freeze_pin=pa,publisher_Source_pin=publisher_pin,
  selected_Source_and_metadata_pins=selected,complete_selected_Source_metadata_count=len(selected),complete_Source_metadata_fullEOF_SHA_current7_verified_twice=True,
  target_pins=targets,target_count=14,target_total_bytes=149659264,target_current7_verified_twice_only_no_body_SHA=True,
  retained_current7_count=6006,retained_current7_verified_twice=True,retained_fullPF_table_reference=pp,
  original43_JSONL_and_new5_JSONL_current7_only_preserved=True,all_original_XSM_and_final55_SQL_pool_pair_preserved=True,
  actual_new_A_closure_pins=cp,actual_new_A_Root_integer_exit_code=0,actual_new_A_child_integer_exit_code=2,original_FAILED_error2_record_retained=True,
  actual_A_six_phases_finished=True,actual_reported_comparisons=19249,actual_reported_context_events=55,actual_reported_snapshot_count=8,
  actual_reported_mismatch_count=0,actual_reported_unknown_macro_count=0,actual_reported_context_issue_count=0,independent_numerical_recomparison_performed=False,
  original_A_v1_Root1_child1_and_old_issue1_preserved=True,historical5937_fullPF_table_and_digest_retained=True,
  current_live_historical_count_before_retirement=5934,future_live_historical_count_only_after_exact14_actual0_post0=5920,
  future_consumers_require_exact_retirement_receipt_and_actual0_post0_absence=True,complete_joint_roots=plan['complete_joint_roots'],
  whole_worker_inverse_to_validated_literal3_v2=True,whole_original_helper_function_count=8,original_resource_classes_modified=False,
  production_inputs_preload_preserved=True,readonly_then_execute_genuine0_receipt_gate=True,
  exact_lsof_return1_empty_gate=True,dirfd_immediate7_unlink_fsync_journal_gate=True,same_PID_original_PS512_guard=True,
  original_resources_forced_fresh_after_final_unlink_and_both_checked_unix_gated=True,retirement_runtime_resource_claim=False,
  original_caps=plan['original_caps'],no_new_output_root=True,new_Source_metadata_bound_bytes=16*2**20,each_receipt_bound_bytes=8*2**20,
  reviewer_source_pin=pin(Path(__file__).absolute()),auditor_Source_freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json'),
  worker_or_helpers_imported=False,Source_generation_executed=False,publisher_executed=False,readonly_check_executed=False,retirement_executed=False,
  business_executed=False,numerical_executed=False,compiler_executed=False,PS_executed=False,lsof_executed=False,files_deleted=False,
  scientific_bodies_opened=False,scientific_body_SHA_recomputed=False,JSONL_or_array_values_decoded=False,
  physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=BASE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(q)),separators=(',',':')),flush=True)
if __name__=='__main__':main()

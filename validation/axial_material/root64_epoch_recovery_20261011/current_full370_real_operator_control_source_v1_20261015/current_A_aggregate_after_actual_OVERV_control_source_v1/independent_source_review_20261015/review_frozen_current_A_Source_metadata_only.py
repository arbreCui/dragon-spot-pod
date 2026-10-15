"""Independent frozen Source/metadata audit; never imports candidate modules."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
D=BASE.parent
REC=D.parent.parent
OLD=REC/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
FLAGS=dict(business_executed=False,compiler_executed=False,numerical_executed=False,
 files_deleted=False,physics_qualified=False,historical_machine_bit_replay=False,
 historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,
 scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)

def identity(s):
 return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def require(ok,message):
 if type(ok)is not bool or not ok:raise ValueError(message)
def current(p):
 q=Path(p['path']);s=q.lstat()
 require(not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and
  identity(s)==p['identity']and s.st_size==p['size_bytes'],'current7 '+str(q))
def full(p):
 current(p);require(p['size_bytes']<8*2**20,'selected Source/control metadata8MiB')
 q=Path(p['path'])
 with q.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened Source/meta7')
  raw=f.read();require(identity(os.fstat(f.fileno()))==p['identity'],'fullEOF Source/meta7')
 require(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole Source/meta SHA')
 current(p);return raw
def pin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes()
 return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def read(p):return json.loads(full(p))
def genuine(v,key,chunk,payload_key,expected):
 t=v[key];require(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and
  v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and
  t['chunk_id']==chunk and t.get('session_id')is None and
  json.loads(t['output'].strip().splitlines()[-1])[payload_key]==expected,'genuine original closed0/PF')
def unique(rows):
 table={}
 for p in rows:
  require(p['path']not in table or table[p['path']]==p,'consistent Source/meta PF')
  table[p['path']]=p
 return list(table.values())

def main():
 ready_pin=pin(D/'SOURCE_REVIEW_READY.json');gen_pin=pin(D/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
 require(ready_pin['sha256']=='a4cbf7f69a491b2990b773145287892ba090ca3c79689f4f8a8fcdc47635e36e'and
  gen_pin['sha256']=='6c7c823026e365f9d2e51bff37133dea77952fde6499eca71f5f68eaf97b5a90','exact Root ready/gen')
 ready=read(ready_pin);gen=read(gen_pin)
 genuine(gen,'actual_Source_preparation_return','ab9955','ready_pin',ready_pin)
 selected=unique(ready['selected_Source_pins']+[ready_pin,gen_pin])
 raw={p['path']:full(p)for p in selected}
 require(len(raw)==len(selected),'complete selected union once')
 author_pin=next(p for p in selected if p['path'].endswith('/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'))
 require(author_pin['sha256']=='332640228825c35a667efbcf50c2cad8cfdd65c29a91a73882368441735b41cb','exact frozen author')
 author=json.loads(raw[author_pin['path']])
 require(author['Source_files_frozen_before_Root_generation']is True and
  all(author[k]is False for k in('Source_preparation_executed_by_author','Source_publication_executed_by_author',
   'business_executed_by_author','scientific_payload_decoded_by_author','compiler_or_native_executed_by_author')),
  'Source author freeze/no business')
 for p in author['whole_Source_file_pins']+author['preserved_wrong_no_retired_intersection_unexecuted_Source_pins']:
  full(p)
 for p in ready['complete_source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(raw[p['path']].decode(),filename=p['path'])
 plan=json.loads(raw[ready['control_plan_pin']['path']])
 require(plan['original_caps']==ready['original_caps']==author['original_caps']and
  plan['bounded_new_output_reservation_bytes']==320*2**20 and
  plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and
  plan['execution_request_hard_bound_bytes']==4*2**20 and
  plan['Source_only_cumulative_bytes_before_reservations']+336*2**20<2*2**30,
  'unchanged caps and complete320MiB+Source16MiB prospective fit')
 require(len(plan['complete_joint_roots'])==63 and len(set(plan['complete_joint_roots']))==63 and
  not os.path.lexists(plan['planned_actual_output_root']),'exact63/fresh unexecuted OUT')
 for p in plan['inherited_metadata_current7_pins']:current(p)
 old_request_pin=plan['original_A_aggregate_request_pin'];request=json.loads(raw[old_request_pin['path']])
 retirement=json.loads(raw[plan['actual_literal3_ASCII_retirement_receipt_pin']['path']])
 retire_tools=json.loads(raw[plan['actual_literal3_ASCII_retirement_true_tools_pin']['path']])
 retire_post_tools=json.loads(raw[plan['actual_literal3_ASCII_retirement_post0_true_tools_pin']['path']])
 genuine(retire_tools,'actual_execution_return','ef0657','receipt_pin',plan['actual_literal3_ASCII_retirement_receipt_pin'])
 genuine(retire_post_tools,'actual_review_return','2e6e5f','review_pin',plan['actual_literal3_ASCII_retirement_post0_pin'])
 retired={p['path']:p for p in retirement['actual_released_pins']};history=request['complete_input_pins'];live=[]
 for p in history:
  if p['path']in retired:require(p==retired[p['path']]and not os.path.lexists(p['path']),'exact retired old PF absence')
  else:current(p);live.append(p)
 require(len(history)==5937 and len(live)==5934 and len(retired)==3 and
  {p['path']:p for p in plan['exact_retired_guard_only_input_pins']}==retired,
  'complete historical5937/current5934/exact3 lifecycle')
 intersection=json.loads(raw[str(D/'RESULT43_OLD_A_INPUT_INTERSECTION_SOURCE_ONLY.json')])
 require(len(intersection['exact_original_input_intersection_pins'])==30,'all30 result-input roles')
 for p in intersection['exact_original_input_intersection_pins']:require(p in live,'all result-input roles retained');current(p)
 controls={k:json.loads(raw[p['path']])for k,p in plan['current_OVERV_control_binding']['metadata_pins'].items()}
 spec=plan['current_OVERV_control_binding']['metadata_pins']
 genuine(controls['control_returns'],'actual_terminal_return','fa62fd','report_pin',spec['control_report'])
 genuine(controls['control_post_returns'],'actual_postverification_return','93f79f','review_pin',spec['control_post'])
 post=controls['control_post'];control=controls['control_report'];prior=controls['prior_aggregate_post']
 require(post['actual_current_overv_words_compared']==2960 and post['actual_current_overv_groups']==370 and
  post['actual_current_overv_mixtures']==8 and post['actual_original_guarded_payload_bytes']==13324 and
  post['all_current_native_vs_independent_integer_model_vs_saved_words_equal']is True and
  post['original_SOURCE_CONTEXT_NOT_SAVED_issue_removed']is False and
  control['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted']is True and
  prior['actual_context_or_operand_issues']==1 and prior['actual_comparison_file_rows']==19249,
  'real current control only; original issue1/19249 retained')
 actual=request['aggregation_binding']['actual_context_states']['A'];desc=controls['control_plan']['selected_final_snapshot_descriptor']
 pair=dict(event=desc['event'],role=desc['role'],root_prefix=desc['root_prefix'],input_pin=desc['input_pin'],
  sqlite_pin=desc['paired_SQLite_pin'],native_pool_pin=desc['paired_original_pool_pin'])
 require(len(actual['all_snapshot_pairs'])==8 and len(actual['complete_context_pins'])==55 and
  pair==actual['all_snapshot_pairs'][-1]and pair['event']==55,'same original full final55 SQL/pool/8tree/55context')
 # Source-only whole inverse. No model/runtime or saved data code is imported.
 old=(OLD/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py').read_text()
 restored=raw[str(D/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py')].decode()
 a=restored.index('\n\n    def current_overv_context_evidence(self):');b=restored.index('\n    def extras(self):',a)
 restored=restored[:a]+restored[b:]
 restored=restored.replace('            self.current_overv_context_evidence()',"            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',\n                original_all370x8_words_compared=True,historical_machine_bit_replay=False)")
 a=restored.index("        current_control=binding.get('current_OVERV_control_admission')");b=restored.index('        model=ContextAwareConstruction(',a)
 restored=(restored[:a]+restored[b:]).replace('        model.current_OVERV_control_admission=current_control\n','').replace('            current_OVERV_control_admission=current_control,\n','')
 require(restored==old,'whole original v4 engine including scalar/6phase/issue counter inverse')
 for p in selected:full(p)
 for p in live:current(p)
 for p in plan['inherited_metadata_current7_pins']:current(p)
 for p in retired.values():require(not os.path.lexists(p['path']),'retired3 remain absent after Source review')
 reviewer_pin=pin(Path(__file__).absolute());freeze_pin=pin(BASE/'AUDITOR_SOURCE_ONLY_FREEZE.json')
 report=dict(schema='INDEPENDENT_CURRENT_A_AGGREGATE_AFTER_OVERV_SOURCE_REVIEW_V1',source_only=True,
  status='PASS_FROZEN_SOURCE_AND_METADATA_ONLY_CURRENT_A_OVERV_CONTROL_AND_EXACT_RETIRED_GUARD_ROLES',failure=None,
  selected_Source_pins=selected,complete_selected_Source_union_count=len(selected),
  selected_complete_fullEOF_SHA_and_current7_verified_twice=True,author_Source_freeze_pin=author_pin,
  Root_Source_generation_true_tools_pin=gen_pin,Source_review_ready_pin=ready_pin,control_plan_pin=ready['control_plan_pin'],
  reviewer_source_pin=reviewer_pin,auditor_Source_freeze_pin=freeze_pin,
  original5937_complete_historical_request_pin=old_request_pin,current_live_historical_input_count=5934,
  historical_original_input_count=5937,exact_retired_guard_only_input_pins=list(retired.values()),
  complete_live_original_input_current7_verified_twice=True,original_30_live_result_input_intersection_preserved=True,
  original_old_report_issue_count=1,issue_count_adjustment_performed=False,
  CURRENT_CONTROL_RESOLVED_is_current_control_evidence_only=True,whole_original_engine_inverse_equal=True,
  original_scalar_and_sixphase_and_issue_counter_math_unchanged=True,
  original_complete55_contexts8_trees19249_comparisons_scope_preserved=True,
  original_child_evidence_only_integer_exit_code=2,original_runner_FAILED_record_preserved=True,
  metadata_each_hard_bound_bytes=8*2**20,new_Source_metadata_hard_bound_bytes=16*2**20,
  new_complete_output_hard_bound_bytes=320*2**20,original_caps=plan['original_caps'],
  publisher_role_names=['peer-review','peer-tools','generation','retirement'],
  publisher_role_suffixes=['summary','sha256','seven-id'],
  preserved_first_stat_error_path=str(D/'INDEPENDENT_NARROW_PREFLIGHT_FIRST_STAT_FAILURE_TRUE_TOOL_RETURNS_20261015.json'),
  Source_and_report_metadata_read_only=True,scientific_bodies_opened=False,scientific_body_SHA_recomputed=False,
  scientific_array_decoded=False,candidate_imported=False,Source_generation_repeated=False,publisher_executed=False,
  actual_business_started=False,**FLAGS)
 path=BASE/'REVIEW.json'
 with path.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=pin(path)),separators=(',',':')),flush=True)

if __name__=='__main__':main()

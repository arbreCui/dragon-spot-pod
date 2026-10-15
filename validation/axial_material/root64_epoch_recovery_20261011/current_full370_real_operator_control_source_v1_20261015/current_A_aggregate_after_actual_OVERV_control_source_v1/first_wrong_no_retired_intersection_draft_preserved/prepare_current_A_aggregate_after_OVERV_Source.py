"""Root-only thin Source preparation; no array, SQL, XSM or native decoding."""
import argparse,ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts';BASE=Path(__file__).absolute().parent
PRIOR=BASE.parent/'current_extra_reaction_operand_replay_source_v2'
OLD=REC/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
CONTROL=REC/'OVERV_original_guarded_integer_control_source_v3_20261014'
POST=REC/'independent_OVERV_original_integer_current_control_actual_postverify_20261014'
OLDPOST=REC/'independent_empty_root_cumulative12_first_A_aggregate_actual_evidence_postverify_20261014'
OUT=ART/'axial-material-current-A-full-aggregate-after-actual-OVERV-control-20261015-v1'
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
NAMES=('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','current_material_lineage_evidence.py','current_OVERV_control_evidence_admission.UNREADY.py','saved_native_data_access_adapter.UNREADY.py','extract_actual_complete_context_with_SPH_decisions.UNREADY.py','current_material_prerequisite_admission.py','run_guarded_current_A_aggregate_after_OVERV_control.py','prepare_current_A_aggregate_after_OVERV_Source.py','write_once_Root_current_A_aggregate_SF_HF_CLI.py','DRAFT_WHOLE_SOURCE_INVERSE.json','RESULT43_OLD_A_INPUT_INTERSECTION_SOURCE_ONLY.json','SOURCE_METADATA_PROSPECTIVE_SIZE_ENVELOPE.json','POST_RETIREMENT_SOURCE_ONLY_PROSPECTIVE_RESERVATION_SNAPSHOT.json')
def require(ok,m):
 if type(ok)is not bool or not ok:raise RuntimeError(m)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();compiler=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==s.st_nlink==2
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or compiler)and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7, only original immutable compiler exception')
def pin(q):
 q=Path(q);s=q.lstat()
 with q.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'opened Source/metadata7')
  h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/metadata7')
 p=dict(path=str(q),sha256=h,size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(q):
 p=pin(q);require(p['size_bytes']<8*2**20,'Source/metadata8MiB')
 v=json.loads(Path(q).read_bytes());require(pin(q)==p,'same exact Source/metadata PF');return v,p
def bound_read(p):
 current(p);v,actual=read(p['path']);require(actual==p,'exact supplied metadata PF');return v
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'each Source metadata8MiB')
 require(sum(p.lstat().st_size for p in BASE.rglob('*.json')if p.is_file())+len(raw)<16*2**20,'all new Source metadata16MiB')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:require(t[p['path']]==p,'same path inconsistent fullPF')
  t[p['path']]=p
 return list(t.values())
def genuine(v,key,code):
 t=v[key];require(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine original closed typed return')
 return json.loads(t['output'].strip().splitlines()[-1])
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def cumulative(roots,explicit):
 n=0
 for root in roots:
  if not Path(root).exists():continue
  for q in Path(root).rglob('*'):
   s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'no output namespace alias')
   if stat.S_ISREG(s.st_mode):n+=s.st_size
 for p in explicit:
  current(p)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):n+=p['size_bytes']
 return n
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('retirement-receipt','retirement-tools','retirement-post','retirement-post-tools'):ap.add_argument('--'+role+'-pin',required=True)
 a=ap.parse_args();pr=json.loads(a.retirement_receipt_pin);pt=json.loads(a.retirement_tools_pin);pRetirePost=json.loads(a.retirement_post_pin);pRetirePostTools=json.loads(a.retirement_post_tools_pin)
 require(not any(os.path.lexists(p)for p in(OUT,BASE/'PLAN.json',BASE/'SOURCE_REVIEW_READY.json')),'fresh Source/OUT once, no retry')
 author,pa=read(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json')
 require(author['Source_files_frozen_before_Root_generation']is True and all(author[k]is False for k in('Source_preparation_executed_by_author','Source_publication_executed_by_author','business_executed_by_author','scientific_payload_decoded_by_author')),'author Source-only freeze, Root sole business')
 for p in author['whole_Source_file_pins']:require(pin(p['path'])==p,'all author-frozen Source bytes intact')
 retirement=bound_read(pr);rt=bound_read(pt)
 require(retirement['schema']=='LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL3_COMPLETED_A_ASCII_EXPORTS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==346861973 and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==3 and retirement['all14_earlier_SQL_pool_files_retained']is True and retirement['original_A_aggregate_issue1_preserved']is True,'true completed literal3 resource receipt')
 require(genuine(rt,'actual_execution_return',0)['receipt_pin']==pr and rt['actual_execution_permission_mode']=='require_escalated','true cleanup execution0 binds exact receipt and original permission route')
 retirepost=bound_read(pRetirePost);retireposttools=bound_read(pRetirePostTools)
 require(genuine(retireposttools,'actual_review_return',0)['review_pin']==pRetirePost and retirepost['schema']=='INDEPENDENT_ACTUAL_LITERAL3_A_ASCII_EXPORT_RETIREMENT_METADATA_POSTVERIFY_V1'and retirepost['status']=='PASS_ACTUAL_EXACT_LITERAL3_A_ASCII_EXPORT_RETIREMENT_346861973B_METADATA_ONLY'and retirepost['failure']is None and retirepost['actual_retirement_receipt_pin']==pr and retirepost['actual_Root_execution_tools_pin']==pt and retirepost['actual_Root_integer_exit_code']==0 and retirepost['all14_earlier_SQL_pool_files_still_live']is True and retirepost['all43_result_JSONL_preserved']is True and retirepost['original_A_aggregate_issue1_preserved']is True,'independent exact real resource post0; all old operands/results and issue retained')
 for p in retirement['actual_released_pins']:require(not os.path.lexists(p['path']),'retired exact ASCII role remains absent')
 prior,pp=read(PRIOR/'PLAN.json');roottools,pRoot=read(PRIOR/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');post,pPost=read(PRIOR/'actual_postverify_20261015/REVIEW.json');posttools,pPostTools=read(PRIOR/'actual_postverify_20261015/TRUE_TOOL_RETURNS.json')
 require(genuine(roottools,'actual_terminal_return',0)['report_pin']==post['actual_Host_report_pin']and genuine(posttools,'actual_review_return',0)['review_pin']==pPost and post['status']=='PASS_REPORTED_ACTUAL_131_NEW_OPERAND_ZERO_BIT_REPLAY_METADATA_ONLY'and post['metadata_only']is True and post['same_Source_author_metadata_assessment']is True and post['independent_numerical_assessment_claimed']is False,'completed62 prior Root0 and sameauthor nonnumerical post0 only')
 roots=prior['complete_joint_roots']+[str(OUT)]
 require(len(roots)==len(set(roots))==63 and roots[:-1]==post['complete_joint_roots']and roots[:-1]==retirement['complete_joint_roots']and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'exact entire latest62 inherited prefix plus OUT63, no reset')
 oldpost,pOldPost=read(OLDPOST/'REVIEW.json');request,pRequest=read(oldpost['actual_request_pin']['path'])
 require(pRequest==oldpost['actual_request_pin']and len(request['complete_input_pins'])==5937 and len(request['aggregation_binding']['actual_context_states']['A']['all_snapshot_pairs'])==8 and len(request['aggregation_binding']['actual_context_states']['A']['complete_context_pins'])==55,'all5937 original inputs/all8pairs/all55events retained')
 retired={p['path']for p in retirement['actual_released_pins']};require(not any(p['path']in retired for p in request['complete_input_pins']),'none of exact retired3 are aggregate input roles')
 for p in request['complete_input_pins']:current(p)
 for k in('saved_native_data_access_adapter.UNREADY.py','extract_actual_complete_context_with_SPH_decisions.UNREADY.py','current_material_prerequisite_admission.py'):require((BASE/k).read_bytes()==(OLD/k).read_bytes(),'whole original helper Source')
 sources=[pin(BASE/k)for k in NAMES]
 for k in NAMES:
  if k.endswith('.py'):ast.parse((BASE/k).read_text())
 oldengine=(OLD/NAMES[0]).read_text();newengine=(BASE/NAMES[0]).read_text()
 def methods(source):
  cls=next(n for n in ast.parse(source).body if isinstance(n,ast.ClassDef)and n.name=='ContextAwareConstruction')
  return{n.name:ast.get_source_segment(source,n)for n in cls.body if isinstance(n,ast.FunctionDef)}
 om,nm=methods(oldengine),methods(newengine)
 require(set(nm)==set(om)|{'current_overv_context_evidence'},'only one new metadata evidence method')
 for k in om:
  if k!='scalar':require(om[k]==nm[k],'whole original numerical method '+k)
 restored_scalar=nm['scalar'].replace('            self.current_overv_context_evidence()',"            self.evidence.event('SOURCE_CONTEXT_NOT_SAVED',field='OVERV',reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',\n                original_all370x8_words_compared=True,historical_machine_bit_replay=False)")
 require(restored_scalar==om['scalar'],'entire original scalar math restored by sole evidence event inverse')
 inverse,pInverse=read(BASE/'DRAFT_WHOLE_SOURCE_INVERSE.json');require(inverse['engine_whole_inverse_equal']is True and inverse['entry_whole_inverse_equal']is True and inverse['original_DiskEvidence_event_issue_counter_whole_unchanged']is True and inverse['original_sixphase_loop_whole_unchanged']is True,'whole mathematical Source inverse evidence')
 controlpost,pControlPost=read(POST/'REVIEW.json')
 metadata_pins=dict(control_plan=pin(CONTROL/'PLAN.json'),control_source_freeze=controlpost['actual_Source_freeze_pin'],control_report=controlpost['actual_report_pin'],control_returns=controlpost['actual_Root_true_tool_return_pin'],control_post=pControlPost,control_post_returns=pin(POST/'TRUE_TOOL_RETURNS.json'),prior_aggregate_post=pOldPost,prior_aggregate_report=oldpost['actual_aggregate_report_pin'],prior_aggregate_request=pRequest,original_arithmetic_binding=pin(REC/'OVERV_original_mixed_precision_independent_control_source_v1_20261014/COMPLETE_ORIGINAL_OVERV_ARITHMETIC_STATEMENT_SOURCE_BINDING.json'))
 for p in metadata_pins.values():bound_read(p)
 spec=dict(schema='CURRENT_A_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1',metadata_pins=metadata_pins)
 inherited=unique(prior['explicit_cumulative_metadata_file_pins']);meta=unique([pp,pRoot,pPost,pPostTools,pr,pt,pRetirePost,pRetirePostTools,pa]+list(metadata_pins.values()));explicit=unique(inherited+meta+sources)
 for p in explicit:current(p)
 before=cumulative(roots,explicit);require(before+320*2**20+16*2**20<2*2**30,'unchanged cumulative2GiB preserves full320MiB output+Source16MiB')
 cli,pCLI=read(PRIOR/'FINAL_ROOT_REVIEWABLE_CLI.json')
 plan=dict(schema='CURRENT_A_AGGREGATE_AFTER_ACTUAL_OVERV_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(OUT),complete_joint_roots=roots,inherited_complete62_plan_pin=pp,explicit_cumulative_metadata_file_pins=explicit,inherited_metadata_current7_pins=inherited,original_A_aggregate_request_pin=pRequest,current_OVERV_control_binding=spec,actual_literal3_ASCII_retirement_receipt_pin=pr,actual_literal3_ASCII_retirement_true_tools_pin=pt,actual_literal3_ASCII_retirement_post0_pin=pRetirePost,actual_literal3_ASCII_retirement_post0_true_tools_pin=pRetirePostTools,original_Common_Source_pin=prior['original_Common_Source_pin'],original_support_Source_pin=prior['original_support_Source_pin'],original_bounded_Source_pin=prior['original_bounded_Source_pin'],original_caps=CAPS,bounded_new_output_reservation_bytes=320*2**20,bounded_new_Source_metadata_reservation_bytes=16*2**20,host_summary_hard_bound_bytes=6*2**20,execution_request_hard_bound_bytes=4*2**20,original_complete_A_input_count=5937,original_snapshot_count=8,original_context_event_count=55,original_expected_comparison_count=19249,original_child_evidence_only_exit_code=2,original_runner_FAILED_record_preserved=True,original_math_whole_inverse_pin=pInverse,Root_actual_exec_command_sandbox_permissions_required='require_escalated',Source_only_cumulative_bytes_before_reservations=before,scientific_payload_decoded_by_Sourcegen=False,original_early14_SQL_pool_roles_still_live=True,**FALSE)
 write(BASE/'PLAN.json',plan);pPlan=pin(BASE/'PLAN.json')
 deps=unique(meta+sources+[pPlan]);ready=dict(schema='CURRENT_A_AGGREGATE_AFTER_ACTUAL_OVERV_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pPlan,host_source_pin=pin(BASE/'run_guarded_current_A_aggregate_after_OVERV_control.py'),final_publisher_Source_pin=pin(BASE/'write_once_Root_current_A_aggregate_SF_HF_CLI.py'),complete_source_file_pins=sources,dependencies=deps,selected_Source_pins=deps,original_caps=CAPS,original_complete_ENV_Python_B_prefix=cli['argv'][:11],actual_business_started=False,Root_final_publication_executed=False,Root_actual_exec_command_sandbox_permissions_required='require_escalated',**FALSE)
 write(BASE/'SOURCE_REVIEW_READY.json',ready);require(cumulative(roots,unique(explicit+[pPlan,pin(BASE/'SOURCE_REVIEW_READY.json')]))+320*2**20<2*2**30,'actual new metadata plus full A output reservation within unchanged2GiB')
 print(json.dumps(dict(status='CURRENT_A_AGGREGATE_AFTER_ACTUAL_OVERV_SOURCE_PREPARATION_ONLY',ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json'),**FALSE)),flush=True)
if __name__=='__main__':main()


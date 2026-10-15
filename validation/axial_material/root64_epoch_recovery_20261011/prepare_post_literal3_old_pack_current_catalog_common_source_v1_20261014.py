"""Source-only exact retired PACK catalog role migration; no runtime import or body read."""
import ast,copy,hashlib,json,os,shlex,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'post_curated66_current_catalog_common_source_v2_20261013'
NEW=REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014'
CAT_NAME='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json'
BIND_NAME='CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json'
POST=REC/'independent_literal3_before_saved370_old_pack_macro_v2_actual_exact_release_postverify_20261014/REVIEW.json'
POST_TOOLS=POST.with_name('TRUE_TOOL_RETURNS.json')
OLD_SF=OLD/'COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json'
PF=('path','sha256','size_bytes','identity')
def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata bounded ordinary fullEOF only')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  if seven(os.fstat(f.fileno()))!=seven(s):raise RuntimeError('opened7')
  raw=f.read()
  if seven(os.fstat(f.fileno()))!=seven(s):raise RuntimeError('EOF7')
 if seven(p.lstat())!=seven(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=seven(s))
def read(path):
 p=pin(path);raw=Path(path).read_bytes()
 if len(raw)!=p['size_bytes']or hashlib.sha256(raw).hexdigest()!=p['sha256']or seven(Path(path).lstat())!=p['identity']:raise RuntimeError('metadata reread7')
 return json.loads(raw),p,raw
def encoded(d):return(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def stat7(p):
 s=Path(p['path']).lstat()
 if not stat.S_ISREG(s.st_mode)or seven(s)!=p['identity']:raise RuntimeError('remaining current row exact7 '+p['path'])
def term0(t):
 if type(t.get('exit_code'))is not int or t['exit_code']!=0 or t.get('session_id')is not None or not isinstance(t.get('output'),str):raise RuntimeError('genuine closed integer0')
def write(p,raw):
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def replace_pf(value,before,after):
 if isinstance(value,dict):
  if value==before:return copy.deepcopy(after),1
  d={};n=0
  for k,v in value.items():d[k],m=replace_pf(v,before,after);n+=m
  return d,n
 if isinstance(value,list):
  d=[];n=0
  for v in value:a,m=replace_pf(v,before,after);d.append(a);n+=m
  return d,n
 return value,0
def main():
 if os.path.lexists(NEW):raise RuntimeError('unique new Source namespace only')
 post,postpin,_=read(POST);tools,toolpin,_=read(POST_TOOLS)
 if post['schema']!='INDEPENDENT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_EXACT_RELEASE_POSTVERIFICATION'or post['failure']is not None or any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','deletion_executed_by_reviewer')):raise RuntimeError('exact literal3 independent post')
 for key in('actual_review_return','actual_postverification_return'):
  term0(tools[key])
  if json.loads(tools[key]['output'].strip().splitlines()[-1])['review_pin']!=postpin:raise RuntimeError('post original stdout binds exact REVIEW')
 if tools['observed_closed']is not True or type(tools['original_integer_exit_code'])is not int or tools['original_integer_exit_code']!=0:raise RuntimeError('post observed integer0')
 receipt,rpin,_=read(post['actual_release_receipt_pin']['path']);root,rootpin,_=read(post['actual_Root_true_tool_pin']['path']);mf,mfpin,_=read(post['actual_manifest_pin']['path']);argv,argvpin,_=read(post['Root_exact_readonly_execute_argv_pin']['path'])
 if any(post[k]!=v for k,v in [('actual_release_receipt_pin',rpin),('actual_Root_true_tool_pin',rootpin),('actual_manifest_pin',mfpin),('Root_exact_readonly_execute_argv_pin',argvpin)]):raise RuntimeError('actual canonical release fullPF')
 term0(root['actual_terminal_return'])
 if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=argv['execute_argv']or len(argv['execute_argv'])!=17 or argv['execute_argv'].count('--execute')!=1:raise RuntimeError('Root unique actual exact17 execute closed0')
 rootlast=json.loads(root['actual_terminal_return']['output'].strip().splitlines()[-1])
 if rootlast['receipt_pin']!=rpin or rootlast['deleted_files']!=3 or receipt['manifest_pin']!=mfpin or receipt['deleted_files']!=3 or receipt['logical_bytes_released']!=526645544 or receipt['schema']!='ACTUAL_EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_RECEIPT_V1'or receipt['status']!='EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED':raise RuntimeError('literal3 actual receipt')
 targets=mf['target_full_EOF_pins']
 if len(targets)!=3 or sum(p['size_bytes']for p in targets)!=526645544 or [row['original_fullpin']for row in receipt['deletion_records']]!=targets:raise RuntimeError('exact literal3 ordered bodies')
 for p,row in zip(targets,receipt['deletion_records']):
  if os.path.lexists(p['path'])or any(row[k]is not True for k in('actual_unlink_returned','target_directory_fsync_attempted','target_directory_fsync_returned','confirmed_absent')):raise RuntimeError('exact genuine returned deletion proof and current absence')
 oldc,oldcp,oldcb=read(OLD/CAT_NAME);oldb,oldbp,oldbb=read(OLD/BIND_NAME);_,oldsfpin,_=read(OLD_SF);oldcommonpin=pin(OLD/'guarded_warm_A_common.py')
 if encoded(oldc)!=oldcb or encoded(oldb)!=oldbb:raise RuntimeError('complete original canonical byte encoding')
 matches=[(i,row)for i,row in enumerate(oldc['rows'])if row['current_pin']in targets]
 if len(oldc['rows'])!=3030 or len(matches)!=1 or matches[0][0]!=1812 or matches[0][1]['current_pin']!=targets[0]or matches[0][1]['mandatory']is not False:raise RuntimeError('only exact optional PACK catalog1812')
 index,retired=matches[0]
 if any(p in targets for p in oldb['fixed_current_pins'])or len(oldb['fixed_current_pins'])!=2012 or [i for i,p in enumerate(oldb['fixed_current_pins'])if p==oldcp]!=[2006]:raise RuntimeError('BIND2012 has no target body and exact CAT slot2006')
 remaining=oldc['rows'][:index]+oldc['rows'][index+1:]
 for row in remaining:stat7(row['current_pin'])
 proof=dict(actual_release_receipt_pin=rpin,actual_Root_true_tool_pin=rootpin,actual_manifest_pin=mfpin,actual_Root_exact_argv_pin=argvpin,actual_independent_postrelease_review_pin=postpin,actual_independent_postrelease_true_tool_pin=toolpin)
 historical=dict(schema='EXACT_ACTUALLY_RELEASED_OLD_PRIVATE_PACK_HISTORICAL_DECLARATION_V1',original_catalog_row_index=index,historical_pin=retired['historical_pin'],last_observed_before_actual_release_pin=retired['current_pin'],mandatory=False,roles=retired['roles'],declaration_occurrence_count=retired['declaration_occurrence_count'],original_device_transition=retired['device_transition'],actual_exact_release_proof=proof,current_role='HISTORICAL_ONLY_NO_CURRENT_BODY_READ',current_body_absent=True,no_current_pin_declared=True)
 unique={row['current_pin']['path']:row['current_pin']for row in remaining}
 reconcile=dict(schema='EXACT_LITERAL3_ACTUAL_OLD_PACK_ONLY_CATALOG_ROLE_RECONCILIATION_V1',predecessor_catalog_pin=oldcp,predecessor_binding_pin=oldbp,predecessor_Common_Source_pin=oldcommonpin,predecessor_Common_Source_freeze_pin=oldsfpin,exact_release_scope_three_target_pins=targets,exact_retired_catalog_row_count=1,original_retired_catalog_indices=[1812],actual_release_proof=proof,retained_row_count=3029,retained_current_declared_unique_regular_files=len(unique),retained_current_declared_unique_bytes=sum(p['size_bytes']for p in unique.values()),all3029_remaining_rows_whole_data_and_order_unchanged=True,all_remaining_current_rows_all7_verified_twice=True,scientific_body_EOF_not_repeated_by_this_Source_step=True,inherited_predecessor_complete_EOF_attestation_preserved=True,original_top_accounting_and_prior_reconciliation_are_historical_predecessor_attestations=True,other_literal3_MAC_targets_have_no_catalog_row=True,BIND2012_target_body_direct_rows_absent=True,missing_or_optional_unreleased_rows_skipped=False,historical_reports_sources_unmodified=True,Source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,physics_qualified=False)
 c=copy.deepcopy(oldc);c['rows']=remaining;c['historical_non_live_declarations'].append(historical);c['post_literal3_old_pack_role_reconciliation']=reconcile
 restored=copy.deepcopy(c);del restored['post_literal3_old_pack_role_reconciliation'];last=restored['historical_non_live_declarations'].pop()
 if last!=historical:raise RuntimeError('exact new sole historical declaration')
 restored['rows'].insert(index,retired)
 if encoded(restored)!=oldcb:raise RuntimeError('whole catalog byte inverse')
 source=(OLD/'guarded_warm_A_common.py').read_bytes();before="BASE = REC/'post_curated66_current_catalog_common_source_v2_20261013'";after="BASE = REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014'"
 text=source.decode()
 if text.count(before)!=1:raise RuntimeError('one Source namespace literal')
 candidate=text.replace(before,after,1);ast.parse(candidate)
 if candidate.replace(after,before,1).encode()!=source:raise RuntimeError('Common whole byte inverse')
 def defs(s):
  return{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 if defs(candidate)!=defs(text):raise RuntimeError('all Common functions/classes wholebytes unchanged')
 NEW.mkdir()
 commonpin=write(NEW/'guarded_warm_A_common.py',candidate.encode());cp=write(NEW/CAT_NAME,encoded(c))
 b,bc=replace_pf(oldb,oldcp,cp)
 if bc!=2 or b['fixed_current_pins'][2006]!=cp:raise RuntimeError('exact selectedCAT and fixedCAT two complete PF replacements')
 b['post_literal3_old_pack_role_reconciliation']=dict(reconcile,selected_current_catalog_pin=cp,selected_current_Common_Source_pin=commonpin)
 backb=copy.deepcopy(b);del backb['post_literal3_old_pack_role_reconciliation'];backb,backbc=replace_pf(backb,cp,oldcp)
 if backbc!=2 or encoded(backb)!=oldbb:raise RuntimeError('whole BIND byte inverse')
 bp=write(NEW/BIND_NAME,encoded(b))
 inverse=dict(schema='COMPLETE_EXACT_LITERAL3_OLD_PACK_CATALOG_BINDING_COMMON_WHOLE_BYTE_INVERSE_V1',original_Common_Source_pin=oldcommonpin,candidate_Common_Source_pin=commonpin,Common_changes=[dict(before=before,after=after)],all_original_Common_functions_classes_wholebytes_unchanged=True,original_catalog_pin=oldcp,candidate_catalog_pin=cp,catalog_original_retired_row_index=index,catalog_original_complete_retired_row=retired,catalog_added_historical_declaration=historical,catalog_added_reconciliation=reconcile,restore_catalog_instructions='remove exact post_literal3_old_pack_role_reconciliation; pop exact added last historical declaration; insert exact original row at1812; original canonical UTF8 indent2 newline',whole_catalog_byte_inverse_equal=True,original_binding_pin=oldbp,candidate_binding_pin=bp,binding_exact_catalog_fullPF_replacement_count=2,binding_added_reconciliation=b['post_literal3_old_pack_role_reconciliation'],restore_binding_instructions='remove exact added reconciliation; replace candidateCAT completePF by originalCAT completePF exactlytwo places; canonical UTF8 indent2 newline',whole_binding_byte_inverse_equal=True,all_other3029_catalog_rows_data_and_order_unchanged=True,BIND2012_no_body_rows_changed=True,Source_only=True)
 iv=write(NEW/'COMPLETE_POST_LITERAL3_OLD_PACK_CATALOG_BINDING_COMMON_WHOLE_BYTE_INVERSE.json',encoded(inverse))
 plan=dict(schema='POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_PLAN_V1',Source_only=True,failure=None,actual_common_source_pin=commonpin,actual_catalog_pin=cp,actual_binding_pin=bp,complete_inverse_pin=iv,preparer_source_pin=pin(Path(__file__).absolute()),original_common_source_pin=oldcommonpin,original_catalog_pin=oldcp,original_binding_pin=oldbp,original_Common_Source_freeze_pin=oldsfpin,actual_release_proof=proof,exact_scope_three_target_pins=targets,exact_retired_catalog_row_index1812=index,current_catalog_row_count3029=3029,current_binding_fixed_count2012=2012,all_Common_functions_classes_wholebytes_unchanged=True,all_remaining_rows_current7_checked_not_new_full_EOF=True,selected_future_Common_Source_freeze_path=str(NEW/'COMPLETE_POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json'),actual_future_Common_Source_freeze_pin=None,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,physics_qualified=False)
 pp=write(NEW/'POST_LITERAL3_OLD_PACK_COMMON_SOURCE_PLAN.json',encoded(plan))
 for row in remaining:stat7(row['current_pin'])
 ready=write(NEW/'SOURCE_REVIEW_READY.json',encoded(dict(schema='POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_REVIEW_READY_V1',status='SOURCE_ONLY_READY_FOR_SAME_ROUND_INDEPENDENT_REVIEW',failure=None,actual_common_source_pin=commonpin,actual_catalog_pin=cp,actual_binding_pin=bp,complete_inverse_pin=iv,plan_pin=pp,actual_release_proof=proof,all_original_Common_functions_classes_wholebytes_unchanged=True,current_rows3029_all7_verified_twice=True,Source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,actual_runtime_or_qualification=None)))
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='POST_LITERAL3_OLD_PACK_CURRENT_CATALOG_BINDING_COMMON_SOURCE_ONLY_READY',actual_common_source_pin=commonpin,actual_catalog_pin=cp,actual_binding_pin=bp,complete_inverse_pin=iv,plan_pin=pp,ready_pin=ready,current_catalog_row_count=3029,current_binding_fixed_count=2012,retired_original_catalog_index=1812,all_Common_functions_classes_wholebytes_unchanged=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()


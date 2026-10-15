"""Independent exact16 Source and metadata review. No candidate/helper imports or payload reads."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
FULL={'path','sha256','size_bytes','identity'};ONLY={'path','size_bytes','identity'};SDK=[]
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,target=False):
 assert type(p)is dict and set(p)in(FULL,ONLY)and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and s.st_nlink==1
 assert s.st_uid==os.getuid()or(not target and p in SDK and s.st_uid==0)
 return q
def full(p):
 assert set(p)==FULL and p['size_bytes']<8*2**20
 q=current(p);b=q.read_bytes();assert len(b)==p['size_bytes']and hashlib.sha256(b).hexdigest()==p['sha256'];current(p);assert hashlib.sha256(q.read_bytes()).hexdigest()==p['sha256'];return b
def meta(p):return json.loads(full(p))
def pin(q):
 q=Path(q).absolute();s=q.lstat();assert stat.S_ISREG(s.st_mode)and s.st_size<8*2**20;b=q.read_bytes();assert ids(q.lstat())==ids(s);return dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def zero(p,key,field,want):
 j=meta(p);r=j[key];assert j['observed_closed']is True and type(j['original_integer_exit_code'])is int and j['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want;return j
ap=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=meta(ap);assert ap['sha256']=='090458db226c526ab0a0760dcee61eabcdd356bb4c3042c1ea83cdd18ce29f6a'and a['source_only']is True and a['Source_author_did_not_execute_GEN_pub_worker_helper_PS_lsof_payload_or_delete']is True and a['Source_author_stopped_editing']is True
pp=a['whole_plan_pin'];plan=meta(pp);assert pp['sha256']=='6a0329db333c71f07b604e48bda416ad571d40c1c183046dc3a1fb4d509a4bb6'
source={}
for p in a['whole_Source_file_pins']:
 s=full(p).decode();ast.parse(s);source[Path(p['path']).name]=s
assert len(source)==2
wp=next(p for p in a['whole_Source_file_pins']if Path(p['path']).name.startswith('retire_'));worker=source[Path(wp['path']).name];pub=source['write_once_exact16_completed_derived_spool_lifecycle_CLI.UNREADY.py'];inv=meta(a['whole_original_inverse_pin']);assert len(inv['rows'])==2
for row in inv['rows']:
 assert row['candidate_pin']in a['whole_Source_file_pins'];s=full(row['candidate_pin']).decode()
 for v in reversed(row['replacements']):
  lo,hi=v['candidate_start'],v['candidate_end'];assert s[lo:hi]==v['candidate_literal'];s=s[:lo]+v['original_literal']+s[hi:]
 assert s.encode()==full(row['original_pin'])and row['whole_original_restored']is True
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
assert plan['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==caps and plan['no_new_output_root']is True and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20
audit=meta(plan['actual_completed_spool_role_audit_pin']);assert plan['actual_completed_spool_role_audit_pin']['sha256']=='911d0d42695fef282c55f1b9d56557cf32d8fd053bfc747e2d2994bb7967e43c'and audit['formal_retirement_admission']is False
targets=plan['exact_target_pins'];completed=plan['ordered_completed_derived_spool_full_pins'];partial=plan['exact_failed_pool_partial_current7_only_pin']
assert targets==completed+[partial]==audit['exact_ordered16_target_pins']and completed==audit['exact_ordered15_fullPF_target_pins']and len(completed)==15 and all(set(p)==FULL for p in completed)and len(targets)==len({p['path']for p in targets})==16 and set(partial)==ONLY and partial['size_bytes']==67099371
assert sum(p['size_bytes']for p in completed[:14])==149659264 and completed[-1]['size_bytes']==150267572 and sum(p['size_bytes']for p in targets)==367026207==plan['planned_released_bytes']==plan['target_total_bytes']
assert plan['target_role_kinds']==audit['target_role_kinds']and plan['completed_B2_derived_pool_full_pin']==completed[-1]
build=meta(plan['original_guard_build_plan_pin']);SDK=build['readonly_system_SDK_header_pins'];assert len(SDK)==3
poolplan=meta(plan['inherited_failed_pool_archive_plan_pin']);roots=plan['complete_joint_roots'];assert roots==poolplan['complete_joint_roots']==plan['actual_failed_pool_complete_prefix']and len(roots)==len(set(roots))==82 and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)
posts={}
for name,child,field in [('actual_B_extract_closure',2,'actual_Host_report_pin'),('actual_B_aggregate_closure',2,'actual_Host_report_pin'),('actual_B2_epoch_bridge_closure',None,'actual_bridge_report_pin'),('actual_B2_complete_extract_closure',2,'actual_Host_report_pin'),('actual_B2_complete_compare_closure',2,'actual_Host_report_pin')]:
 c=audit[name];root=meta(c['Root_report']);post=meta(c['post']);zero(c['Root_tools'],'actual_terminal_return','report_pin',c['Root_report']);zero(c['post_tools'],'actual_review_return','review_pin',c['post'])
 assert root['failure']is None and post['failure']is None and post['metadata_only']is True and post['schema']==c['post_schema']and post['status']==c['post_status']and post[field]==c['Root_report']and post['actual_Root_tools_pin']==c['Root_tools']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==child and(child is None or type(post['actual_child_integer_exit_code'])is int)
 posts[name]=post
E=posts['actual_B_extract_closure'];B=posts['actual_B_aggregate_closure'];X=posts['actual_B2_complete_extract_closure'];C=posts['actual_B2_complete_compare_closure'];N=posts['actual_B2_epoch_bridge_closure']
early=audit['exact_early7_snapshot_descriptors'];assert [p['event']for p in early]==[4,7,8,10,51,52,54]and len(early)==7 and [p[k]for p in early for k in('sqlite_pin','native_pool_pin')]==completed[:14]
assert E['all_snapshot_pairs']==B['all_snapshot_pairs']==early+[audit['retained_final55_snapshot_descriptor']]and E['complete_context_pins']==B['complete_context_pins']==audit['retained_all55_context_pins']and len(E['complete_context_pins'])==55
assert B['actual_snapshot_pair_count']==8 and B['actual_context_event_count']==55 and B['actual_B_six_phase_engine_evidence_completed']is True and B['actual_six_phase_results']==[dict(phase=x,computation_finished=True)for x in('scattering','scalar','fission','extras','overv_fallback','metadata')]
expectedB=dict(actual_compared_source_fields=19249,actual_compared_known_elements=1829421,actual_context_or_operand_issues=0,actual_all_mismatch_elements=0,actual_unknown_macro_producers=0);assert all(type(B[k])is int and B[k]==v for k,v in expectedB.items())
assert X['actual_full_physical_tree_counts']==dict(complete_physical_tree_records=62798,complete_directories=7958,complete_extents=8766,complete_MICROLIB2_list1_MACROLIB_records=19620)and C['actual_comparison_counts']==dict(compared_all_macro_records=19620,compared_original_payload_words=2264152,raw_word_mismatches=0,metadata_mismatches=0)and C['actual_path_sets_equal']is True and C['actual_exact_inventory_metadata_and_all_words_equal']is True and X['paired_original_pool_pin']==C['native_B2_pair']['native_pool_pin']==completed[-1]
native=audit['retained_B2_current_epoch_native_archive_pin'];assert native['sha256']=='f44b2dcb0441f9405b8c927b8fab8cb9903bad9e036dfbb66d025e9c2790c61c'and native['size_bytes']==156880856 and N['ordered_role_pairs']==audit['retained_B2_selected9_readonly_current_epoch_role_pairs']and len(N['ordered_role_pairs'])==9 and plan['retained_B2_current_epoch_readonly_pins']==[p['current_epoch_full_pin']for p in N['ordered_role_pairs']]and native in plan['retained_B2_current_epoch_readonly_pins']
for r in N['ordered_role_pairs']:assert r['blind_complete_SHA_and_length_equal']is True and r['before_open_EOF_after_current7_stable']is True and r['current_epoch_full_pin']['sha256']==r['historical_full_pin']['sha256']and r['current_epoch_full_pin']['size_bytes']==r['historical_full_pin']['size_bytes']
preserved=audit['retained_seven_original_observer_XSM_pins']+[audit['retained_final55_SQLite_pin'],audit['retained_final55_pool_pin'],audit['retained_final55_XSM_pin']]+audit['retained_all55_context_pins']+audit['all_retained_B2_comparison_result_pins'];assert all(p in plan['retained_current7_pins']for p in preserved)and C['new_complete_output_full_pins']==audit['all_retained_B2_comparison_result_pins']and C['actual_complete_comparison_detail_pin']==audit['retained_B2_comparison_detail_pin']
for ev in audit['actual_consumer_Source_evidence']:
 lines=full(ev['Source_pin']).decode().splitlines();assert all(lines[r['line']-1]==r['text']for r in ev['lines'])
assert plan['future_policy']==audit['future_policy']and plan['A14_verified_precedent']==audit['A14_verified_precedent']and plan['temporary_completed_derived_spool_lifecycle_only']is True and plan['all_original_spool_file_bytes_archived_or_reconstructable_claimed']is False
for k in ['new_SQL_or_pool_byte_identity_with_retired_file_claimed','old_SQLgzip_plus_newly_extracted_pool_automatically_compatible_claimed','whole_pair_gzip_archive_success_claimed','generic_missing_path_skip_authorized']:assert plan['future_policy'][k]is False
assert plan['future_policy']['old8_snapshot_or_B2_pair_consumers_must_not_receive_absent_paths']is True
cp=plan['actual_pool_failure_closure_pins'];host=meta(cp['Host']);raw=meta(cp['Root_tools']);failurepost=meta(cp['post']);zero(cp['post_tools'],'actual_review_return','review_pin',cp['post']);watch=meta(cp['watchdog']);first=meta(cp['first_failure']);ret=raw['actual_terminal_return']
assert raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==1 and type(ret['exit_code'])is int and ret['exit_code']==1 and ret.get('session_id')is None and raw['actual_retried']is False and raw['actual_execution_permission_mode']=='require_escalated'
cli=meta(plan['actual_failed_pool_reviewable_CLI_pin']);assert raw['exact_executed_command']==cli['command']and host['failure']is not None and host['archive_complete']is False and host['actual_watchdog']is None and host['actual_child_receipt']is None and host['final_report_resource_check_passed']is True and host['original_pool_current7_retained']is True and len(host['records'])==1 and host['records'][0]['status']=='FAILED'
assert watch['returncode']==1 and type(watch['returncode'])is int and watch['limit_failure']is None and first['phase']=='ARCHIVE_1'and first['failure']=="RuntimeError('paired gzip payload below64MiB; no compression assumption')"and first['completed_entry_pins']==[poolplan['reused_SQL_member0_entry_pin']]and first['partial_archive_paths']==[partial['path']]
assert failurepost['actual_Root_integer_exit_code']==1 and failurepost['actual_recorded_child_integer_exit_codes']==[1]and all(type(x)is int for x in failurepost['actual_recorded_child_integer_exit_codes'])and failurepost['archive_success_or_roundtrip_or_complete_pair_inferred']is False and failurepost['actual_Host_embedded_watchdog']is None and failurepost['actual_Host_child_receipt']is None
failedrows=failurepost['failed_output_current7_only_three_field_rows'];assert failedrows==plan['actual_failed_pool_output_current7_only_pins']and len(failedrows)==8 and partial in failedrows and all(set(p)==ONLY for p in failedrows)and plan['retained_failed_pool_archive_current7_only_pins']==[p for p in failedrows if p!=partial]
assert plan['retained_current7_pins']==[p for p in poolplan['all1_plain_pins']+poolplan['retained_current7_pins']if p not in completed]and plan['retained_B2_current_epoch_readonly_pins']==poolplan['retained_B2_current_epoch_readonly_pins']and plan['retained_failed_v1_current7_only_pins']==poolplan['retained_failed_v1_current7_only_pins']
assert plan['retained_complete_SQL_gzip_pin']==poolplan['reused_SQL_member0_gzip_pin']and plan['retained_SQL_entry_pin']==poolplan['reused_SQL_member0_entry_pin']and plan['SQL_with_exact_live_original_pool_recovery_map']==poolplan['SQL_with_exact_live_original_pool_recovery_map']
historical=plan['prior_exact_historical_SQL_and_partial_target_pins'];assert historical==poolplan['exact_historical_SQL_and_discarded_partial_target_pins']
for p in historical:assert not os.path.lexists(p['path'])
retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins'];assert not{p['path']for p in targets}&{p['path']for p in retained}and len(plan['retained_failed_v1_current7_only_pins'])==8 and all(set(p)==ONLY for p in plan['retained_failed_v1_current7_only_pins'])
for _ in range(2):
 for p in targets:current(p,True)
 for p in retained:current(p)
for term in("q=current_partial(p,plan)if p==partial else current(p,True)","full(p,budget)","os.O_DIRECTORY|os.O_NOFOLLOW","os.stat(q.name,dir_fd=fd,follow_symlinks=False)","os.unlink(q.name,dir_fd=fd);os.fsync(fd)","r.returncode==1 and r.stdout==b''and r.stderr==b''","budget(True);d['resources_after']=state['latest']","len(d['actual_released_pins'])==16","current_source","state.update(last=time.monotonic()"):
 if term=='current_source':continue
 assert term in worker
assert worker.index("with receipt.open('xb')as f:")<worker.index("bm=module(")and "512*2**20"in worker and "time.monotonic()-started<600"in worker and '96*2**30'in worker and '2*2**30'in worker
assert "for p in completed:current(p,True);full(p,budget)"in worker and "partial_body_read_or_hashed_or_upgraded_to_fullPF"not in worker
for term in("genuine(checktools,'actual_readonly_return'","genuine(checkposttools,'actual_review_return'","checkpost['actual_readonly_receipt_pin']==pcheck","checkpost['exact_target_pins']==targets","checkpost['files_deleted']is False"):
 assert term in worker
for term in("ap.add_argument('--mode',choices=['check','execute']","genuine(ct,'actual_readonly_return'","genuine(cpt,'actual_review_return'","cp['exact_target_pins']==plan['exact_target_pins']"):
 assert term in pub
for p in a['whole_Source_file_pins']+[ap,pp,plan['actual_completed_spool_role_audit_pin']]:full(p)
r=dict(schema='INDEPENDENT_COMPLETED_B_DERIVED_SPOOL_EXACT16_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE',failure=None,source_only=True,source_pin=wp,plan_pin=pp,author_freeze_pin=ap,complete_source_file_pins=a['whole_Source_file_pins'],whole_original_inverse_pin=a['whole_original_inverse_pin'],whole_two_Source_inverse_reconstructed=True,actual_completed_spool_role_audit_pin=plan['actual_completed_spool_role_audit_pin'],exact_ordered16_target_pins=targets,planned_released_bytes=367026207,target_fullPF_count=15,target_incomplete_stat_only_count=1,all15_target_bytes_SHA_check_only_by_Root_worker=True,incomplete_fragment_never_body_opened_or_SHA_claimed=True,all_target_current7_checked_twice_without_payload_IO=True,five_completed_consumer_Root0_and_independent_post0_closures_verified=True,actual_B_sixphase8_snapshot55_context_consumption_verified=True,actual_B2_62798_record_complete_tree_and19620_macro_all2264152_words_doublezero_verified=True,retained_canonical_native_and_final55pair55contexts_and_comparison_detail_current7_twice=True,all_prior_result_docs_archives_metadata_and_failed_history_current7_verified_twice=True,old_exact_SQL_pool_map_preserved_as_history=True,future_replay_requires_new_full_native_extraction_and_independent_admission=True,old_SQL_or_pool_byte_reconstruction_or_complete_pair_gzip_success_claimed=False,complete_joint_roots=roots,no_new_output_root=True,Source_metadata_component_bound_bytes=8*2**20,original_caps=caps,original_PS_lsof_owner_uid_dirfd7_fsync_resource_guards_retained=True,readonly0_then_independent_readonly_post0_before_execute_required=True,final_original_resource_scan_forced_after_last_unlink=True,actual_resource_snapshot_is_Source_only_and_Root_fresh_original_classes_required=True,worker_or_helpers_PS_lsof_or_business_executed=False,old_SQL_pool_native_gzip_payload_body_opened_or_hashed=False,files_deleted=False,numerical_executed=False,compiler_executed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
q=BASE/'REVIEW.json';assert not q.exists();q.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],review_pin=pin(q))))

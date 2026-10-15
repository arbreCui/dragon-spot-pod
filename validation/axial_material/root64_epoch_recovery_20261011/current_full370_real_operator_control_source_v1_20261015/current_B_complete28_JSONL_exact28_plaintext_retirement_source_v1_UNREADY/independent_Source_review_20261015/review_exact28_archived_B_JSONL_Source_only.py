"""Independent exact28 Source and metadata review. No candidate/helper imports or payload reads."""
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
ap=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=meta(ap)
assert ap['sha256']=='82967f9bea56bb9ba5c19d26931fb6bfa2a068ee6dd036bb8e162cf32efa2325'and a['Source_only']is True and a['actual_readonly_or_execution_done_by_author']is False and a['Root_only_business_executor']is True and a['all_source_metadata_writes_bounded_entire_Source8']is True
pp=a['whole_plan_pin'];plan=meta(pp);assert pp['sha256']=='f287d6e4c594b860058ac99762aed7542b3b42e9a4a320fef658f0ecfe4c1516'
S={}
for p in a['whole_Source_file_pins']:
 s=full(p).decode();ast.parse(s);S[Path(p['path']).name]=s
wp=next(p for p in a['whole_Source_file_pins']if Path(p['path']).name.startswith('retire_'));worker=S[Path(wp['path']).name];pub=S['write_once_exact28_B_result_JSONL_reviewable_CLI.UNREADY.py'];assert len(S)==2
for t in (ast.parse(worker),ast.parse(pub)):
 keys={n.slice.value for n in ast.walk(t)if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='plan'and isinstance(n.slice,ast.Constant)and type(n.slice.value)is str}
 assert keys<=set(plan)
inv=meta(a['whole_original_inverse_pin']);assert len(inv['rows'])==2
for row in inv['rows']:
 assert row['candidate_pin']in a['whole_Source_file_pins'];s=full(row['candidate_pin']).decode()
 for v in reversed(row['replacements']):
  lo,hi=v['candidate_start'],v['candidate_end'];assert s[lo:hi]==v['candidate_literal'];s=s[:lo]+v['original_literal']+s[hi:]
 assert s.encode()==full(row['original_pin'])
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
assert plan['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==caps and plan['no_new_output_root']is True and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20
build=meta(plan['original_guard_build_plan_pin']);SDK=build['readonly_system_SDK_header_pins'];assert len(SDK)==3
archive=meta(plan['inherited_complete_archive_plan_pin']);roots=plan['complete_joint_roots'];assert roots==archive['complete_joint_roots']==plan['actual_archive_complete_prefix']and len(roots)==len(set(roots))==83 and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and plan['original_caps']==archive['original_caps']
assert plan['actual_archive_Root0_child0_complete']is True and plan['actual_archive_independent_post0_complete']is True and a['actual_B28_archive_Root0_child0_independent_post0_complete']is True
cp=plan['actual_archive_closure_pins'];assert set(cp)=={'Host','Root_tools','child_report','index','post','post_tools'}
host=meta(cp['Host']);raw=zero(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);child=meta(cp['child_report']);index=meta(cp['index']);post=meta(cp['post']);zero(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
assert raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False and host['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'and host['status']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and host['failure']is None and host['archive_complete']is True and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['original_caps']==caps and host['complete_joint_roots']==roots and host['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(host['records'])==1 and host['records'][0]['status']=='PASS'and host['actual_child_receipt']['report_pin']==cp['child_report']and host['all28_original_plain_current7_retained']is True
watch=host['actual_watchdog'];assert type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600
assert child['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'and child['status']=='COMPLETE28_B_JSONL_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None and type(child['completed_count'])is int and child['completed_count']==28 and child['all28_original_plain_current7_retained']is True and child['index_pin']==cp['index']and child['binding_pin']==plan['inherited_complete_archive_plan_pin']
sf=meta(host['source_freeze_pin']);commonpin=plan['inherited_archive_common_Source_pin'];assert sf['execution_binding_pin']==plan['inherited_complete_archive_plan_pin']and commonpin in sf['complete_source_file_pins'];common=full(commonpin).decode();ast.parse(common)
targets=plan['exact_target_pins'];empty=plan['retained_empty_numeric_mismatch_JSONL_pin'];assert targets==archive['all28_plain_pins']and len(targets)==len({p['path']for p in targets})==28 and sum(p['size_bytes']for p in targets)==249929878==plan['planned_released_bytes']==plan['target_total_bytes']and all(set(p)==FULL and p['path'].endswith('.jsonl')and p['size_bytes']>0 for p in targets)and empty==archive['retained_empty_numeric_mismatch_JSONL_pin']and empty['size_bytes']==0 and empty not in targets
assert index['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and index['status']=='COMPLETE28_B_JSONL_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'and index['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(index['entries'])==index['ordered_original_plain_count']==28 and index['ordered_original_plain_total_bytes']==249929878 and index['ordered_original_result_JSONL_pins']==targets and index['all28_original_plain_retained']is True and index['future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping']is True and index['retained_empty_numeric_mismatch_JSONL_pin']==empty and index['generic_missing_path_skip_authorized']is False
gz=[];entries=[]
for ordinal,(row,original)in enumerate(zip(index['entries'],targets)):
 assert row['ordinal']==ordinal and row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True and row['actual_B_output_role']=='COMPLETE_B_EXTRACT_OR_SIXPHASE_RESULT_JSONL'
 assert meta(row['entry_pin'])=={k:v for k,v in row.items()if k!='entry_pin'};gz.append(row['compressed_archive_full_pin']);entries.append(row['entry_pin'])
assert gz==plan['retained_ordered_result_JSONL_gzip_pins']and entries==plan['retained_ordered_result_JSONL_entry_pins']==index['ordered_result_JSONL_archive_entry_pins']
projection=plan['actual_archive_post_key_projection'];projection_source=meta(plan['actual_archive_post_key_projection_Source_pin']);assert projection_source['schema']==projection['schema']and projection_source['status']==projection['status']
assert post['schema']==projection['schema']=='RECORDED_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and post['status']==projection['status']=='PASS_ACTUAL_COMPLETE28_B_JSONL_STREAMED_SHA_LENGTH_ARCHIVE_ROOT0_CHILD0_METADATA_ONLY_ORIGINALS_RETAINED'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==cp['Host']and post['actual_Root_tools_pin']==cp['Root_tools']and post['actual_archive_index_pin']==cp['index']and post['actual_child_report_pin']==cp['child_report']and post['execution_binding_pin']==plan['inherited_complete_archive_plan_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==0
assert post['original_ordered_result_JSONL_full_pins']==targets and post['compressed_ordered_result_JSONL_archive_full_pins']==gz and post['ordered_result_JSONL_entry_pins']==entries and post['completed_count']==28 and post['complete_joint_roots']==roots and post['Root_recorded_all28_original_and_decompressed_SHA_length_match']is True and post['all28_original_current7_verified_twice_only']is True and post['all28_compressed_blind_fullEOF_SHA_current7_verified_twice']is True
assert post['retained_empty_numeric_mismatch_JSONL_pin']==empty and post['retained_empty_numeric_mismatch_current7_verified_twice']is True and post['exact16_retired_temporary_target_pins']==archive['exact16_retired_temporary_target_pins']and post['exact16_historical_absence_only_verified_twice']is True
assert len(post['all_new_output_blind_fullEOF_SHA_current7_twice_pins'])==64 and post['actual_all28_original_JSONL_bytes']==249929878 and post['actual_all28_gzip_bytes']==24003048 and post['actual_entire_archive_output_bytes']==25912521

def unique(rows):
 out={}
 for p in rows:assert p['path']not in out or out[p['path']]==p;out[p['path']]=p
 return list(out.values())
assert plan['retained_current7_pins']==unique(archive['retained_current7_pins']+post['all_new_output_blind_fullEOF_SHA_current7_twice_pins'])and post['retained_all_current7_pins']==archive['retained_current7_pins']and plan['retained_B2_current_epoch_readonly_pins']==archive['retained_B2_current_epoch_readonly_pins']==post['bridge9_cold_readonly_current7_pins']and len(plan['retained_B2_current_epoch_readonly_pins'])==9
assert plan['retained_failed_v1_current7_only_pins']==archive['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']and len(plan['retained_failed_v1_current7_only_pins'])==8 and plan['retained_failed_pool_archive_current7_only_pins']==archive['retained_failed_pool_archive_current7_only_pins']==post['retained_failed_pool_archive_current7_only_pins']and len(plan['retained_failed_pool_archive_current7_only_pins'])==7 and all(set(p)==ONLY for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins'])
assert plan['exact16_retired_temporary_target_pins']==archive['exact16_retired_temporary_target_pins']and plan['historical_retired_presence_full_pin']==archive['historical_retired_presence_full_pin']
archiveproofs=list(cp.values())+[commonpin,host['source_freeze_pin'],host['host_freeze_pin'],plan['actual_archive_post_key_projection_Source_pin'],plan['inherited_complete_archive_plan_pin']]
assert plan['retained_archive_metadata_current7_pins']==unique(archiveproofs+entries)and plan['explicit_cumulative_metadata_file_pins']==unique(archive['explicit_cumulative_metadata_file_pins']+archiveproofs+entries)
retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+gz+entries+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+[empty]+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins'];assert not{p['path']for p in targets}&{p['path']for p in retained}
for _ in range(2):
 for p in targets:current(p,True)
 for p in retained:current(p)
 for p in plan['exact16_retired_temporary_target_pins']+[plan['historical_retired_presence_full_pin']]:assert not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents)
for term in ("for p in archivepins:full(p,budget)","for p in targets:current(p,True);full(p,budget)","c.admit(archiveplan)","os.O_DIRECTORY|os.O_NOFOLLOW","os.stat(q.name,dir_fd=fd,follow_symlinks=False)","os.unlink(q.name,dir_fd=fd);os.fsync(fd)","r.returncode==1 and r.stdout==b''and r.stderr==b''","len(d['actual_released_pins'])==28","budget(True);d['resources_after']=state['latest']","state.update(last=time.monotonic()","512*2**20","time.monotonic()-started<600","96*2**30","2*2**30"):
 assert term in worker
assert worker.index("with receipt.open('xb')as f:")<worker.index("bm=module(")and worker.count('c.admit(archiveplan)')==1 and worker.index('c.admit(archiveplan)')<worker.index("os.unlink(q.name,dir_fd=fd)")
after=worker[worker.index("os.unlink(q.name,dir_fd=fd)"):];assert 'c.admit('not in after and 'for p in targets:current('not in after
for term in("genuine(checktools,'actual_readonly_return'","genuine(checkposttools,'actual_review_return'","checkpost['actual_readonly_receipt_pin']==pcheck","checkpost['exact_target_pins']==targets","checkpost['files_deleted']is False"):
 assert term in worker
for term in("ap.add_argument('--mode',choices=['check','execute']","genuine(ct,'actual_readonly_return'","genuine(cpt,'actual_review_return'","cp['exact_target_pins']==plan['exact_target_pins']"):
 assert term in pub
assert plan['independent_readonly_post0_required_before_execute']is True and plan['readonly_post_report_contract']==dict(schema='CURRENT_B_COMPLETE28_JSONL_EXACT28_READONLY_METADATA_POSTVERIFY_V1',status='PASS_CURRENT_B_COMPLETE28_JSONL_EXACT28_READONLY0_NO_UNLINK_METADATA_ONLY',actual_report_not_yet_created=True)and plan['execute_post_report_contract']==dict(schema='CURRENT_B_COMPLETE28_JSONL_EXACT28_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_B_COMPLETE28_JSONL_EXACT28_ORIGINALS_RETIRED_FULL_BYTES_ARCHIVED_METADATA_ONLY',actual_report_not_yet_created=True)
assert plan['future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping']is True and plan['generic_missing_path_skip_authorized']is False
for k in('files_deleted','archive_business_executed_by_Source_author','body_or_SQL_pool_or_gzip_read_by_Source_author','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):assert plan[k]is False
snap=plan['actual_original_resource_snapshot'];assert snap['source_metadata_stat_only']is True and snap['original_resource_classes_not_imported_or_executed']is True and snap['Root_actual_original_resource_classes_recheck_required']is True
for p in a['whole_Source_file_pins']+[ap,pp]:full(p)
r=dict(schema='INDEPENDENT_B_COMPLETE28_JSONL_EXACT28_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT',failure=None,source_only=True,source_pin=wp,plan_pin=pp,author_freeze_pin=ap,complete_source_file_pins=a['whole_Source_file_pins'],whole_original_inverse_pin=a['whole_original_inverse_pin'],whole_two_Source_inverse_reconstructed=True,exact_target_pins=targets,planned_released_bytes=249929878,actual_archive_closure_pins=cp,actual_archive_Root0_child0_independent_post0_verified=True,all28_ordered_full_original_gzip_entry_index_exact_metadata_mapping_verified=True,all28_Root_recorded_streamed_original_and_decompressed_SHA_length_equal=True,all64_new_archive_outputs_retained=True,empty_mismatch_original_retained=True,all_target_and_retained_current7_checked_twice_without_body_IO=True,all_prior_failed_stat_only_rows_preserved=True,exact16_and_prior_presence_history_only_absence_preserved=True,complete_joint_roots=roots,no_new_output_root=True,Source_metadata_component_bound_bytes=8*2**20,original_caps=caps,original_PS_lsof_owner_uid_dirfd7_fsync_resource_guards_retained=True,readonly0_then_independent_readonly_post0_before_execute_required=True,final_original_resource_scan_forced_after_last_unlink=True,actual_resource_snapshot_is_Source_only_and_Root_fresh_original_classes_required=True,candidate_or_helpers_PS_lsof_or_business_executed=False,old_JSONL_SQL_pool_native_gzip_payload_body_opened_or_hashed=False,files_deleted=False,numerical_executed=False,compiler_executed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
q=BASE/'REVIEW.json';assert not q.exists();raw=(json.dumps(r,indent=2)+'\n').encode();assert sum(p.stat().st_size for p in D.rglob('*')if p.is_file())+len(raw)<8*2**20;q.write_bytes(raw);print(json.dumps(dict(status=r['status'],review_pin=pin(q))))

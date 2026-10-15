"""Independent Source/metadata/current7 review only; never run cleanup or payload IO."""
import ast,hashlib,json,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
F={'path','sha256','size_bytes','identity'};P={'path','size_bytes','identity'}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 assert set(p)in(F,P)and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'];return q

def full(p):
 assert set(p)==F and p['size_bytes']<8*2**20;q=current(p);b=q.read_bytes();assert len(b)==p['size_bytes']and hashlib.sha256(b).hexdigest()==p['sha256'];current(p);return b

def read(p):v=json.loads(full(p));full(p);return v

def pin(q):
 s=q.lstat();b=q.read_bytes();assert ids(q.lstat())==ids(s);return dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))

def closed(p,key,code,field=None,want=None):
 v=read(p);r=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and r.get('session_id')is None
 if field is not None:assert json.loads(r['output'].splitlines()[-1])[field]==want
 return v

ap=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=read(ap);assert ap['sha256']=='aa4eec2a4acb191284a87568bc67a5e0f1a6b505512ae699a03168171d9c3fff'and a['source_only']is True and a['Source_author_stopped_editing']is True and a['Source_author_did_not_execute_GEN_pub_worker_helper_PS_lsof_payload_or_delete']is True
pp=a['whole_plan_pin'];p=read(pp);assert pp['sha256']=='c408ccc0477bde4b1fe1f39c3c1444e2c1b0e88d9dd0835bb837ab640b2bcf44'and p['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_PLAN_V1'and p['Source_admission_ready']is True and p['draft_unready']is False
sources={}
for q in a['whole_Source_file_pins']:
 s=full(q).decode();full(q);ast.parse(s);sources[Path(q['path']).name]=s
assert len(sources)==2
sp=next(q for q in a['whole_Source_file_pins']if Path(q['path']).name.startswith('recover_'));worker=sources[Path(sp['path']).name];publisher=sources['write_once_SQL_partial_exact2_recovery_CLI.UNREADY.py']
inv=read(a['whole_original_inverse_pin']);assert len(inv['rows'])==2
for row in inv['rows']:
 assert row['candidate_pin']in a['whole_Source_file_pins'];s=full(row['candidate_pin']).decode()
 for edit in sorted(row['replacements'],key=lambda e:e['candidate_start'],reverse=True):
  begin,end=edit['candidate_start'],edit['candidate_end'];assert s[begin:end]==edit['candidate_literal'];s=s[:begin]+edit['original_literal']+s[end:]
 assert s.encode()==full(row['original_frozen_pin']);full(row['original_frozen_pin'])
archive=read(p['original_pair_execution_binding_pin']);roots=p['complete_joint_roots'];assert roots==archive['complete_joint_roots']==p['actual_failed_pair_complete_prefix']and len(roots)==len(set(roots))==81 and p['no_new_output_root']is True and p['original_caps']==archive['original_caps']
cp=p['actual_pair_failure_closure_pins'];h=read(cp['Host']);raw=closed(cp['Root_tools'],'actual_terminal_return',1);ff=read(cp['first_failure']);w=read(cp['watchdog']);fp=read(cp['post']);closed(cp['post_tools'],'actual_review_return',0,'review_pin',cp['post'])
assert raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False and h['failure']is not None and h['archive_complete']is False and h['actual_watchdog']is None and h['actual_child_receipt']is None and len(h['records'])==1 and h['records'][0]['status']=='FAILED'and h['records'][0]['error']=='own-child stage failed; no retry'
assert w['command']==h['records'][0]['command']and type(w['returncode'])is int and w['returncode']==1 and w['limit_failure']is None
sql=p['exact_original_SQL_full_pin'];partial=p['exact_partial_pool_current7_only_pin'];assert set(sql)==F and set(partial)==P and p['exact_target_pins']==[sql,partial]and sql==archive['all2_plain_pins'][0]and [sql['size_bytes'],partial['size_bytes']]==[52441088,17639368]and p['planned_released_bytes']==p['target_total_bytes']==70080456 and p['target_role_kinds']==['RESTORABLE_SQL_FULLPF','INCOMPLETE_POOL_GZIP_CURRENT7_ONLY']
assert fp['original_SQL_pool_ordered_full_pins']==archive['all2_plain_pins']and fp['actual_Root_integer_exit_code']==fp['actual_child_integer_exit_code']==1 and fp['actual_complete_pair_archive_success']is False and fp['pool_partial_current7_only_pin']==partial
entrypin=p['retained_SQL_member0_entry_pin'];entry=read(entrypin);gz=p['retained_SQL_member0_gzip_pin'];assert ff['phase']=='ARCHIVE_1'and ff['completed_entry_pins']==[entrypin]and entry['ordinal']==0 and entry['original_plain_full_pin']==sql and entry['compressed_archive_full_pin']==gz and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==sql['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==52441088 and entry['original_plain_preserved']is True and gz['size_bytes']==7025974
mp=p['actual_SQL_member0_control_closure_pins'];m=read(mp['Root_report']);closed(mp['Root_tools'],'actual_terminal_return',0,'report_pin',mp['Root_report']);post=read(mp['post']);closed(mp['post_tools'],'actual_review_return',0,'review_pin',mp['post'])
assert m['failure']is None and m['original_member0_saved_full_pin']==sql and m['complete_member0_gzip_pin']==gz and m['retained_member0_entry_pin']==entrypin and m['streamed_complete_member0_verified']is True and m['streamed_decompressed_SHA']==sql['sha256']and m['streamed_decompressed_length']==52441088 and m['children_started']==0 and m['paired_SQL_pool_archive_complete']is False and m['partial_pool_gzip_current7_only_pin']==partial and m['partial_pool_gzip_body_opened_or_hashed']is False
assert post['failure']is None and post['metadata_only']is True and post['actual_member0_Root_report_pin']==mp['Root_report']and post['actual_Root_tools_pin']==mp['Root_tools']and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']is None and post['Root_actual_complete_member0_stream_verified']is True and post['paired_SQL_pool_archive_complete']is False
pool=archive['all2_plain_pins'][1];mapping=p['SQL_with_exact_live_original_pool_recovery_map'];assert mapping==dict(historical_SQL_full_pin=sql,complete_SQL_gzip_full_pin=gz,SQL_member0_entry_pin=entrypin,exact_live_original_pool_full_pin=pool,SQL_member0_Root_control_pin=mp['Root_report'],SQL_member0_independent_post_pin=mp['post'],restore_SQL_and_use_exact_original_pool_together=True,whole_pair_archive_complete=False,generic_missing_path_skip_authorized=False)and pool['size_bytes']==150267572 and pool in p['retained_current7_pins']
assert p['retained_current7_pins']==[q for q in archive['all2_plain_pins']+archive['retained_current7_pins']if q!=sql]and p['retained_failed_v1_current7_only_pins']==archive['retained_failed_v1_current7_only_pins']and len(p['retained_failed_v1_current7_only_pins'])==8 and p['retained_B2_current_epoch_readonly_pins']==archive['retained_B2_current_epoch_readonly_pins']and len(p['retained_B2_current_epoch_readonly_pins'])==9
retain=p['retained_current7_pins']+p['retained_archive_metadata_current7_pins']+[gz,entrypin]+p['explicit_cumulative_metadata_file_pins']+p['retained_B2_current_epoch_readonly_pins'];assert not{q['path']for q in p['exact_target_pins']}&{q['path']for q in retain+p['retained_failed_v1_current7_only_pins']}and all(set(q)==P for q in p['retained_failed_v1_current7_only_pins'])
for repeat in range(2):
 for q in p['exact_target_pins']+retain+p['retained_failed_v1_current7_only_pins']:current(q)
assert p['actual_pair_failure_Root1_child1_post0_complete']is True and p['actual_SQL_member0_Root0_independent_post0_complete']is True and p['independent_readonly_post0_required_before_execute']is True and p['readonly_post_report_contract']['actual_report_not_yet_created']is True and p['execute_post_report_contract']['actual_report_not_yet_created']is True
# All direct frozen plan keys in actual Source exist; partial can enter only the stat-only helper.
for s in sources.values():
 t=ast.parse(s);keys={n.slice.value for n in ast.walk(t)if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='plan'and isinstance(n.slice,ast.Constant)and isinstance(n.slice.value,str)};assert not keys-set(p)
for needle in("q=current(sql,True)if p==sql else current_partial(p,plan)",'ids(os.stat(q.name,dir_fd=fd,follow_symlinks=False))','os.unlink(q.name,dir_fd=fd);os.fsync(fd)','state.update(last=time.monotonic()',"'/bin/ps'","'/usr/sbin/lsof'",'budget(True)'):assert needle in worker
assert 'full(partial'not in worker and 'full(p,budget)'not in worker and 'partial_target_body_opened_or_hashed=False'in worker and worker.index("with receipt.open('xb')")<worker.index('bm=module(')<worker.index('os.unlink(')
for s in(worker,publisher):
 for term in('actual_readonly_return','actual_review_return','readonly_post_report_contract','resources_after_original_classes_forced_fresh'):assert term in s
for q in a['whole_Source_file_pins']+[pp,ap]:full(q);full(q)
r=dict(schema='INDEPENDENT_CURRENT_B2_SQL_PARTIAL_EXACT2_RECOVERY_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B2_SQL_PARTIAL_EXACT2_RECOVERY',failure=None,source_only=True,source_pin=sp,plan_pin=pp,complete_source_file_pins=a['whole_Source_file_pins'],author_freeze_pin=ap,whole_original_inverse_pin=a['whole_original_inverse_pin'],both_original_frozen_Source_whole_inverse_independently_reconstructed=True,exact_target_pins=p['exact_target_pins'],target_role_kinds=p['target_role_kinds'],planned_released_bytes=70080456,retained_original_pool_full_pin=pool,retained_SQL_gzip_pin=gz,retained_SQL_entry_pin=entrypin,SQL_with_exact_live_original_pool_recovery_map=mapping,actual_pair_failure_closure_pins=cp,actual_SQL_member0_control_closure_pins=mp,complete_joint_roots=roots,no_new_data_root=True,original_caps=p['original_caps'],own_Source_metadata_bound_bytes=16*2**20,partial_target_and_oldfailed_eight_roles_strict_three_field_stat_only=True,all_target_and_retained_roles_current7_checked_twice=True,full_reading_of_partial_target_forbidden_in_worker=True,original_PS_lsof_privateUID_dirfd_exact7_fsync_partial_log_and_final_forced_fresh_guards_retained=True,readonly_actual0_then_independent_post0_required_before_execute_in_worker_and_publisher=True,Root_must_recheck_original_resource_classes_before_target_IO=True,failed_pair_Root1_child1_and_SQL_member0_Root0_nochild_preserved=True,candidate_worker_pub_helper_PS_lsof_or_cleanup_executed=False,original_SQL_pool_gzip_or_partial_body_opened_or_hashed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
f=BASE/'REVIEW.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],review_pin=pin(f))))

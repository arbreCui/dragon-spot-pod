"""Source/meta/current7 independent review; never invokes retirement or publisher."""
import ast,hashlib,json,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'];return q

def full(p):
 q=current(p);assert p['size_bytes']<8*2**20;raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256'];current(p);return raw

def read(p):
 v=json.loads(full(p));full(p);return v

def pin(q):
 s=q.stat();return dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=ids(s))

def zero(p,key,field,want):
 v=read(p);r=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want;return v

authorpin=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=read(authorpin);assert authorpin['sha256']=='9b4ebffb17edcb1ae9a907daf296cc04013e9655e519ceec7a4ae52406bd4154'and a['source_only']is True and a['author_STOP_WRITES']is True and a['author_no_GEN_pub_worker_helpers_PS_lsof_native_compiler_or_cleanup']is True
pp=a['whole_plan_pin'];p=read(pp);assert pp['sha256']=='7ae77351eccbfa5834e78cf9bb2e26c903cc38596a55db990ccc7501c821928f'and p['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and p['Source_admission_ready']is True and p['draft_unready']is False
sources={}
for q in a['whole_Source_file_pins']:text=full(q).decode();full(q);ast.parse(text);sources[Path(q['path']).name]=text
assert len(sources)==2
workerpin=next(q for q in a['whole_Source_file_pins']if Path(q['path']).name=='retire_exact1_archived_Bagg_presence.UNREADY.py');worker=sources[Path(workerpin['path']).name];publisher=sources['write_once_exact1_Bagg_presence_reviewable_CLI.UNREADY.py']
inversepin=pin(D/'DRAFT_WHOLE_REMAINING3_SOURCE_INVERSE_EVIDENCE.json');inverse=read(inversepin)
for row in inverse['files']:
 text=full(row['Source_pin']).decode()
 for edit in sorted(row['inverse_literal_offset_edits'],key=lambda e:e['new_start'],reverse=True):
  start,end=edit['new_start'],edit['new_end'];assert text[start:end]==edit['new_literal'];text=text[:start]+edit['original_literal']+text[end:]
 assert text.encode()==full(row['original_frozen_Source_pin'])and hashlib.sha256(text.encode()).hexdigest()==row['whole_original_restored_SHA']
cp=p['actual_archive_closure_pins'];h=read(cp['Host']);child=read(cp['child_report']);index=read(cp['index']);post=read(cp['post']);zero(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);zero(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
assert h['schema']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'and h['status']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and h['failure']is None and h['archive_complete']is True and h['final_report_resource_check_passed']is True and h['records'][0]['status']=='PASS'and h['actual_watchdog']['returncode']==0 and h['actual_child_receipt']['report_pin']==cp['child_report']
assert child['index_pin']==cp['index']and child['completed_count']==1 and child['failure']is None
archive=read(p['inherited_complete_archive_plan_pin']);roots=p['complete_joint_roots'];assert roots==p['actual_archive_complete_prefix']==archive['complete_joint_roots']==h['complete_joint_roots']and len(roots)==len(set(roots))==76 and p['no_new_output_root']is True and p['original_caps']==archive['original_caps']==h['original_caps']
assert p['actual_archive_Root0_child0_complete']is True and p['actual_archive_independent_post0_complete']is True and p['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and p['bounded_own_Source_metadata_receipts_bytes']==16*2**20
original=p['exact_target_pins'][0];assert p['exact_target_pins']==archive['all1_plain_pins']==[archive['actual_presence_original_pin']]==a['exact_target_pins']and original['size_bytes']==p['planned_released_bytes']==p['target_total_bytes']==169615994 and original['path']==p['exact_presence_original_path']and original['sha256']=='9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7'
row=index['entries'][0];assert len(index['entries'])==1 and row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True
assert p['retained_presence_gzip_pins']==[row['compressed_archive_full_pin']]and p['retained_presence_entry_pins']==[row['entry_pin']]and read(row['entry_pin'])=={k:v for k,v in row.items()if k!='entry_pin'}
assert post['schema']=='RECORDED_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_SINGLE_BAGG_PRESENCE_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_ORIGINAL_RETAINED'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==cp['Host']and post['actual_Root_tools_pin']==cp['Root_tools']and post['actual_child_report_pin']==cp['child_report']and post['actual_archive_index_pin']==cp['index']and post['original_presence_full_pin']==original and post['compressed_presence_archive_full_pin']==row['compressed_archive_full_pin']and post['presence_entry_pin']==row['entry_pin']and post['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True and post['actual_Root_integer_exit_code']==post['actual_child_integer_exit_code']==0
assert p['retained_Bagg_output_current7_pins']==archive['retained_Bagg_output_current7_pins']and len(p['retained_Bagg_output_current7_pins'])==16 and p['retained_native_current7_pins']==archive['retained_native_current7_pins']and p['retained_current7_pins']==archive['retained_current7_pins']
bridge=read(archive['actual_current_epoch_B2_bridge_report_pin']);zero(archive['actual_current_epoch_B2_bridge_tools_pin'],'actual_terminal_return','report_pin',archive['actual_current_epoch_B2_bridge_report_pin']);assert p['retained_B2_current_epoch_readonly_pins']==[x['current_epoch_full_pin']for x in bridge['ordered_role_pairs']]and len(p['retained_B2_current_epoch_readonly_pins'])==9
retain=p['retained_current7_pins']+p['retained_archive_metadata_current7_pins']+p['retained_presence_gzip_pins']+p['retained_presence_entry_pins']+p['explicit_cumulative_metadata_file_pins']+p['retained_B2_current_epoch_readonly_pins'];assert original['path']not in{q['path']for q in retain}and not{q['path']for q in p['retained_B2_current_epoch_readonly_pins']}&{q['path']for q in p['explicit_cumulative_metadata_file_pins']}
for q in [original]+retain:current(q)
for key in p:
 if key.startswith('future_')and key.endswith('_pin'):assert p[key]is None
assert p['independent_readonly_post0_required_before_execute']is True and p['forced_fresh_original_resource_classes_after_final_unlink']is True and p['readonly_and_execute_once_each']is True and p['future_consumer_must_use_exact_single_presence_archive_mapping']is True and p['generic_missing_path_skip_authorized']is False
for text in(worker,publisher):assert 'actual_readonly_return'in text and 'actual_review_return'in text and 'resources_after_original_classes_forced_fresh'in text and 'readonly_post_report_contract'in text
assert worker.index("with receipt.open('xb')")<worker.index('bm=module(')<worker.index('os.unlink(q.name,dir_fd=fd)')and "'/usr/sbin/lsof'"in worker and "'/bin/ps'"in worker and 'budget(True)'in worker and 'state.update(last=time.monotonic()'in worker and 'ids(os.stat(q.name,dir_fd=fd,follow_symlinks=False))'in worker and 'os.fsync(fd)'in worker
for q in a['whole_Source_file_pins']+[pp]:full(q);full(q)
r=dict(schema='INDEPENDENT_CURRENT_BAGG_PRESENCE_EXACT1_RETIREMENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_BAGG_PRESENCE_EXACT1_RETIREMENT',failure=None,source_only=True,source_pin=workerpin,plan_pin=pp,complete_source_file_pins=a['whole_Source_file_pins'],author_freeze_pin=authorpin,whole_remaining3_inverse_evidence_pin=inversepin,whole_two_original_remaining3_Source_inverse_reconstructed=True,actual_archive_Root0_child0_post0_pins=cp,exact_target_pins=p['exact_target_pins'],planned_released_bytes=169615994,complete_joint_root_count=76,new_output_root_created=False,original_caps=p['original_caps'],whole_Source_metadata_bound_bytes=16*2**20,all16_other_Bagg_outputs_and_full_native_inputs_and_B4archives_entries_index_preserved_current7=True,nine_B2_current_epoch_cold_readonly_roles_retained_in_original_history=True,large_cold_inputs_not_ordinary_freshmetadata=True,original_PS_lsof_privateUID_dirfd_unlinklog_and_forced_fresh_guards_retained=True,independent_readonly_actual0_then_post0_required_before_execute_in_both_publisher_worker=True,all_future_readonly_execute_actual_credentials_NULL=True,Source_reviewer_worker_publisher_helper_PS_lsof_or_unlink_executed=False,original_or_gzip_or_SQLpool_or_scientific_body_read_or_hashed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
f=BASE/'REVIEW.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],review_pin=pin(f))))

"""Independent Source/metadata/current7 review only; never import or run cleanup, helpers or payloads."""
import ast,hashlib,json,stat,difflib
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 assert type(p)is dict and set(p)in({'path','sha256','size_bytes','identity'},{'path','size_bytes','identity'})
 assert type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'];return q

def full(p):
 assert set(p)=={'path','sha256','size_bytes','identity'}and p['size_bytes']<8*2**20
 q=current(p);b=q.read_bytes();assert len(b)==p['size_bytes']and hashlib.sha256(b).hexdigest()==p['sha256'];current(p);return b

def read(p):
 v=json.loads(full(p));full(p);return v

def pin(q):
 q=q.absolute();s=q.lstat();b=q.read_bytes();assert ids(q.lstat())==ids(s);return dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))

def zero(p,key,field,want):
 v=read(p);r=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want;return v

authorpin=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=read(authorpin)
assert authorpin['sha256']=='38294882f2b56a4ce2cbfb92ecf005d518df26a8eab0dee6edb90c1a3504cfb0'and a['source_only']is True and a['Source_author_stopped_editing']is True and a['Source_author_did_not_execute_GEN_pub_worker_helper_PS_lsof_payload_or_delete']is True
pp=a['whole_plan_pin'];p=read(pp);assert pp['sha256']=='36fc830079f4ac2c5e3e9534c0487dece092cc35cef53d5e53549a90efea4494'and p['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and p['Source_admission_ready']is True and p['draft_unready']is False
sources={}
for q in a['whole_Source_file_pins']:
 b=full(q);full(q);ast.parse(b);sources[Path(q['path']).name]=b.decode()
assert len(sources)==2
workerpin=next(q for q in a['whole_Source_file_pins']if Path(q['path']).name=='retire_exact1_archived_B2_physical_directory.UNREADY.py');worker=sources[Path(workerpin['path']).name];publisher=sources['write_once_exact1_B2_physical_directory_reviewable_CLI.UNREADY.py']
inversepin=a['whole_original_inverse_pin'];inv=read(inversepin);edits={}
for role,new,oldpin in zip(('worker','publisher'),(worker,publisher),inv['original_Source_full_pins']):
 old=inv['whole_original_Source_text'][role];assert old.encode()==full(oldpin);full(oldpin)
 sm=difflib.SequenceMatcher(None,old,new,autojunk=False);ed=[dict(old_start=i,old_end=j,new_start=k,new_end=l,old_literal=old[i:j],new_literal=new[k:l])for tag,i,j,k,l in sm.get_opcodes()if tag!='equal']
 restored=new
 for e in reversed(ed):
  assert restored[e['new_start']:e['new_end']]==e['new_literal'];restored=restored[:e['new_start']]+e['old_literal']+restored[e['new_end']:]
 assert restored.encode()==full(oldpin);edits[role]=dict(edit_count=len(ed),whole_original_restored_SHA=hashlib.sha256(restored.encode()).hexdigest())
# AST equality for byte-sensitive guard helpers; all adapted main flow was independently read in full.
def function(text,name):
 t=ast.parse(text);n=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name==name);return ast.dump(n,include_attributes=False)
for name in('require','ids','full','pin','module','genuine','snapshot'):
 assert function(worker,name)==function(inv['whole_original_Source_text']['worker'],name)
for name in('need','ident','pin','read','genuine'):
 assert function(publisher,name)==function(inv['whole_original_Source_text']['publisher'],name)
cp=p['actual_archive_closure_pins'];h=read(cp['Host']);ch=read(cp['child_report']);idx=read(cp['index']);post=read(cp['post']);raw=zero(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);zero(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
assert cp['post']['sha256']=='ee24ba6b45c74705ba6291eb405e7ad29703a261d57f1a5cd50c3c094fc19671'and cp['post_tools']['sha256']=='fe1e025501d95ec0e9f4c1de41e3d58c41897434614bc663df5f76293ed50294'
assert raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False
assert h['schema']=='ACTUAL_CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'and h['status']=='ACTUAL_CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and h['failure']is None and h['archive_complete']is True and h['final_report_resource_check_passed']is True and len(h['records'])==1 and h['records'][0]['status']=='PASS'and h['actual_watchdog']['returncode']==0 and h['actual_child_receipt']['report_pin']==cp['child_report']
assert ch['index_pin']==cp['index']and ch['completed_count']==1 and ch['failure']is None
ap=read(p['inherited_complete_archive_plan_pin']);roots=p['complete_joint_roots'];assert roots==p['actual_archive_complete_prefix']==ap['complete_joint_roots']==h['complete_joint_roots']and len(roots)==len(set(roots))==80 and p['no_new_output_root']is True and p['original_caps']==ap['original_caps']==h['original_caps']
assert p['original_caps']==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
original=p['exact_target_pins'][0];assert p['exact_target_pins']==ap['all1_plain_pins']==[ap['actual_physical_directory_original_pin']]and original['size_bytes']==p['planned_released_bytes']==p['target_total_bytes']==34371817 and original['path']==p['exact_physical_directory_original_path']and original['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60'
assert len(idx['entries'])==1;row=idx['entries'][0]
assert row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True
assert p['retained_physical_directory_gzip_pins']==[row['compressed_archive_full_pin']]and p['retained_physical_directory_entry_pins']==[row['entry_pin']]and read(row['entry_pin'])=={k:v for k,v in row.items()if k!='entry_pin'}and row['compressed_archive_full_pin']['size_bytes']==1550218
proj=p['actual_archive_post_key_projection'];assert read(p['actual_archive_post_key_projection_Source_pin'])==proj
assert post['schema']==proj['schema']and post['status']==proj['status']and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==cp['Host']and post['actual_Root_tools_pin']==cp['Root_tools']and post['actual_child_report_pin']==cp['child_report']and post['actual_archive_index_pin']==cp['index']and post['execution_binding_pin']==p['inherited_complete_archive_plan_pin']and post[proj['original_full_pin_field']]==original and post[proj['compressed_archive_full_pin_field']]==row['compressed_archive_full_pin']and post[proj['entry_pin_field']]==row['entry_pin']and post['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True and post['actual_Root_integer_exit_code']==post['actual_child_integer_exit_code']==0
prior=read(ap['latest_complete_plan_pin']);comp=read(ap['actual_comparison_post_pin']);zero(ap['actual_comparison_post_tools_pin'],'actual_review_return','review_pin',ap['actual_comparison_post_pin'])
assert comp['actual_comparison_counts']==ap['actual_comparison_counts']==dict(compared_all_macro_records=19620,compared_original_payload_words=2264152,raw_word_mismatches=0,metadata_mismatches=0)and comp['actual_exact_inventory_metadata_and_all_words_equal']is True and comp['actual_Root_integer_exit_code']==0 and comp['actual_child_integer_exit_code']==2
assert p['retained_current7_pins']==ap['retained_current7_pins']and p['retained_B2_current_epoch_readonly_pins']==ap['retained_B2_current_epoch_readonly_pins']and p['retained_failed_v1_current7_only_pins']==ap['retained_failed_v1_current7_only_pins']==prior['retained_failed_v1_current7_only_pins']==comp['retained_failed_v1_current7_only_pins']and len(p['retained_failed_v1_current7_only_pins'])==8
assert comp['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved']is True and comp['prior_v1_partial_payload_body_not_opened_or_hashed_by_post']is True
ex=read(prior['actual_latest_complete_prefix_plan_pin']);bridge=read(ex['actual_B2_current_epoch_bridge_report_pin']);zero(ex['actual_B2_current_epoch_bridge_Root_tools_pin'],'actual_terminal_return','report_pin',ex['actual_B2_current_epoch_bridge_report_pin'])
assert p['retained_B2_current_epoch_readonly_pins']==[r['current_epoch_full_pin']for r in bridge['ordered_role_pairs']]and len(p['retained_B2_current_epoch_readonly_pins'])==9
retained=p['retained_current7_pins']+p['retained_archive_metadata_current7_pins']+p['retained_physical_directory_gzip_pins']+p['retained_physical_directory_entry_pins']+p['explicit_cumulative_metadata_file_pins']+p['retained_B2_current_epoch_readonly_pins'];assert original['path']not in{q['path']for q in retained+p['retained_failed_v1_current7_only_pins']}and not{q['path']for q in p['retained_B2_current_epoch_readonly_pins']}&{q['path']for q in p['explicit_cumulative_metadata_file_pins']}
for q in p['retained_failed_v1_current7_only_pins']:assert set(q)=={'path','size_bytes','identity'}
for repeat in range(2):
 for q in [original]+retained+p['retained_failed_v1_current7_only_pins']:current(q)
assert p['independent_readonly_post0_required_before_execute']is True and p['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and p['generic_missing_path_skip_authorized']is False
for text in(worker,publisher):
 for term in('actual_readonly_return','actual_review_return','resources_after_original_classes_forced_fresh','readonly_post_report_contract'):assert term in text
assert worker.index("with receipt.open('xb')")<worker.index('bm=module(')<worker.index('os.unlink(q.name,dir_fd=fd)')and "'/usr/sbin/lsof'"in worker and "'/bin/ps'"in worker and 'budget(True)'in worker and 'state.update(last=time.monotonic()'in worker and 'ids(os.stat(q.name,dir_fd=fd,follow_symlinks=False))'in worker and 'os.fsync(fd)'in worker and "receipt.open('xb')"in worker
for q in a['whole_Source_file_pins']+[pp]:full(q);full(q)
r=dict(schema='INDEPENDENT_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_RETIREMENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_RETIREMENT',failure=None,source_only=True,source_pin=workerpin,plan_pin=pp,complete_source_file_pins=a['whole_Source_file_pins'],author_freeze_pin=authorpin,whole_original_Source_inverse_evidence_pin=inversepin,independently_reconstructed_whole_original_Source_inverse=edits,actual_archive_Root0_child0_corrected_post0_closure_pins=cp,exact_target_pins=p['exact_target_pins'],planned_released_bytes=34371817,complete_joint_root_count=80,new_data_output_root_created=False,original_caps=p['original_caps'],own_Source_metadata_bound_bytes=16*2**20,all_SQL_pools_other_outputs_native_B4archives_entries_index_retained_current7_twice=True,nine_B2_cold_readonly_roles_retained_in_original_history=True,failed_v1_eight_roles_strict_three_field_current7_only=True,ordinary_fullPF_metadata_not_relaxed=True,original_PS_lsof_privateUID_dirfd_exact7_fsync_and_final_forced_fresh_guards_retained=True,independent_readonly_actual0_then_post0_required_before_execute_in_publisher_and_worker=True,Root_fresh_original_resource_class_admission_still_required=True,worker_publisher_helper_PS_lsof_or_unlink_executed_by_reviewer=False,original_gzip_SQLpool_or_scientific_body_read_or_hashed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
f=BASE/'REVIEW.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],review_pin=pin(f))))

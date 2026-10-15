"""Independent recorded pair-archive Root1/child1 failure metadata and complete SQL member0 facts.
Only bounded Source/control metadata and the completed SQL gzip are blind-hashed.
Original SQL/pool bodies are never opened; pool partial remains strict three-field stat-only.
No pair completion, decompression, cleanup, scientific decoding or worker execution.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B2_SQL_pool_lossless_archive_source_v2_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '573f0df24c1b2e6096325d71f6bed264cecf2683801a09282f47bb5d69c588e6', 'size_bytes': 7372, 'identity': [16777229, 50887089, 33188, 1, 7372, 1792070692319248443, 1792070692319248443]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(result_values_decoded=False,numerical_executed=False,compiler_executed=False,native_executed=False,worker_or_guard_helpers_imported=False,PS_executed=False,lsof_executed=False,compression_repeated=False,decompression_repeated=False,files_deleted=False,old_plain_payload_body_opened=False,old_plain_payload_SHA_recomputed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,plain_retirement_authorized=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh paired SQL/pool archive output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def archive_resources(v,roots,seconds):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<seconds and v['complete_joint']['resource_roots']==roots,'actual original SELF/wall and dynamic complete current roots')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history/cumulative/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
ART=ROOT/'validation/artifacts'
OUT_CAP=32*2**20;ARCHIVE_CAP=24*2**20;SOURCE_CAP=16*2**20
def true0(p,key,stdout_role,expected):
 v=meta(p);genuine(v,key,expected,stdout_role);return v
def unique(rows):
 out={}
 for p in rows:need(p['path']not in out or out[p['path']]==p,'same path same wholePF');out[p['path']]=p
 return list(out.values())
def admit_prior(binding):
 need(binding['schema']=='CURRENT_B2_PAIRED_SQL_POOL_LOSSLESS_ARCHIVE_BINDING_V1'and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False and binding['Source_admission_ready']is False and binding['original_caps']==CAPS and type(binding['actual_current_resource_stage_budget'])is dict,'NULL physical exact1 Root0/post0/latest budget never admits SQL-pool archive or GEN')
 previouspin=binding['actual_physical_directory_retirement_plan_pin'];previous=meta(previouspin)
 receipt=meta(binding['actual_physical_directory_retirement_receipt_pin']);post=meta(binding['actual_physical_directory_retirement_post_pin'])
 true0(binding['actual_physical_directory_retirement_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_physical_directory_retirement_receipt_pin'])
 true0(binding['actual_physical_directory_retirement_post_tools_pin'],'actual_review_return','review_pin',binding['actual_physical_directory_retirement_post_pin'])
 historical=binding['historical_retired_physical_directory_full_pin']
 need(previous['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and previous['Source_admission_ready']is True and previous['draft_unready']is False and previous['no_new_output_root']is True and previous['original_caps']==CAPS and previous['exact_target_pins']==[historical]and historical['size_bytes']==34371817 and historical['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60','only exact physical JSONL historical PF retired; no generic missing role skip')
 need(receipt['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==[historical]and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==34371817 and receipt['files_deleted']is True and receipt['resources_after_original_classes_forced_fresh']is True and receipt['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and receipt['generic_missing_path_skip_authorized']is False,'genuine exact1 physical retirementRoot0 with forced fresh resources and permanent byte mapping')
 need(post['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_RETIRED_COMPLETE_RESULT_BYTES_IN_ARCHIVE_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_physical_directory_retirement_receipt_pin']and post['actual_Root_tools_pin']==binding['actual_physical_directory_retirement_Root_tools_pin']and post['plan_pin']==previouspin and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['exact_target_pins']==post['actual_released_pins']==[historical]and type(post['actual_released_bytes'])is int and post['actual_released_bytes']==34371817 and post['files_deleted']is True and post['files_deleted_by_post']is False and post['historical_retired_physical_directory_full_pin']==historical and post['historical_deleted_fullPF_not_claimed_current']is True and post['exact_one_target_absent_verified_twice']is True and post['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and post['generic_missing_path_skip_authorized']is False,'genuine independent exact1 metadata post0 for the same Source/plan/receipt, not archive or readonly success substituted')
 need(not os.path.lexists(historical['path'])and not any(q.is_symlink()for q in Path(historical['path']).parents),'only proved retired physical original absent, never current-stat/hash it or skip other missing files')
 archivepin=previous['inherited_complete_archive_plan_pin'];archive=meta(archivepin);cp=previous['actual_archive_closure_pins'];apost=meta(cp['post']);index=meta(cp['index'])
 true0(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);true0(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
 projection=previous['actual_archive_post_key_projection'];gzip=previous['retained_physical_directory_gzip_pins'];entries=previous['retained_physical_directory_entry_pins']
 need(len(gzip)==len(entries)==len(index['entries'])==1 and archive['actual_physical_directory_original_pin']==historical and archive['all1_plain_pins']==[historical]and apost['schema']==projection['schema']and apost['status']==projection['status']and apost['failure']is None and apost[projection['original_full_pin_field']]==historical and apost[projection['compressed_archive_full_pin_field']]==gzip[0]and apost[projection['entry_pin_field']]==entries[0]and apost['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True and post['retained_physical_directory_gzip_pins']==gzip and post['retained_physical_directory_entry_pins']==entries and post['original_lookup_index_pin']==cp['index'],'retired physical original permanently recoverable via same complete gzip/entry/index, creation history preserved')
 row=index['entries'][0];entry=meta(entries[0]);need(row['entry_pin']==entries[0]and entry=={k:v for k,v in row.items()if k!='entry_pin'}and row['original_plain_full_pin']==historical and row['compressed_archive_full_pin']==gzip[0]and row['compression_input_SHA']==row['streamed_decompressed_SHA']==historical['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==34371817 and row['original_plain_preserved']is True,'exact physical entry creation-time preservation remains history, not a current original claim')
 compareplan=meta(archive['latest_complete_plan_pin']);pair=compareplan['native_B2_pair'];ordered=[pair['sqlite_pin'],pair['native_pool_pin']]
 need(binding['all2_plain_pins']==ordered and binding['actual_B2_SQL_pool_original_pair']==dict(sqlite_pin=ordered[0],native_pool_pin=ordered[1])and [p['size_bytes']for p in ordered]==[52441088,150267572]and binding['original_plain_total_bytes']==202708660 and binding['compression_order']=='SQL_THEN_ORIGINAL_POOL','only complete actual paired SQL index then original pool; no numerical parsing or repeat native decoding')
 expected=unique(previous['retained_current7_pins']+previous['retained_archive_metadata_current7_pins']+gzip+entries+[cp['index']]+previous['retained_B2_current_epoch_readonly_pins'])
 need(all(p in expected for p in ordered)and binding['retained_current7_pins']==[p for p in expected if p not in ordered]and historical['path']not in{p['path']for p in expected}and binding['retained_physical_directory_gzip_pins']==gzip and binding['retained_physical_directory_entry_pins']==entries and binding['retained_physical_directory_index_pin']==cp['index'],'all other native/B4/current comparison detail/docs/physical archive bytes retained; only SQL/pool targets separated')
 need(binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']and post['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved']is True and post['prior_v1_partial_payload_body_not_opened_or_hashed_by_post']is True and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins'],'all eight failed-v1 files current7-only and cold9 roles preserved without fullPF/SHA invention')
 proofs=[binding[k]for k in('actual_physical_directory_retirement_plan_pin','actual_physical_directory_retirement_receipt_pin','actual_physical_directory_retirement_Root_tools_pin','actual_physical_directory_retirement_post_pin','actual_physical_directory_retirement_post_tools_pin')]+[archivepin]+list(cp.values())
 need(binding['latest_complete_plan_pin']==previouspin and binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),'complete inherited80 metadata union plus exact retirement actual proofs, no dropped external roles or large cold payload in metadata')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots'];need(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']==archive['complete_joint_roots']and len(prefix)==80 and binding['complete_joint_roots']==prefix+[str(out)]and out.parent==ART and len(binding['complete_joint_roots'])==81 and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),'entire inherited80 plus exactly one owning paired archive81 root, no scope reset')
 need(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP and binding['future_consumer_must_restore_exact_SQL_pool_pair_together']is True,'whole32MiB=24gzip+8runtime metadata plus Source16; failures retained without retry or assumed compression')
 return out
EXPECTED_ACTUAL_ROOT_TOOLS_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B2_SQL_pool_lossless_archive_source_v2_UNREADY/ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json', 'sha256': 'eeed874a503895454acbe59c841822cf69d6cf39c24df73cbc4173d51697952e', 'size_bytes': 3680, 'identity': [16777229, 50887618, 33188, 1, 3680, 1792071352369059361, 1792071352369059361]}
EXPECTED_ACTUAL_HOST_PIN={'path': '/Users/wen/spot/validation/artifacts/axial-material-current-B2-paired-SQL-pool-lossless-archive-20261015-v1/Root_actual_single_B2_SQL_pool_lossless_archive_summary.json', 'sha256': '2d88cec03c74aae32d3955c1055eafa66f970ac0209b2df43d87db0fe77c0f51', 'size_bytes': 876872, 'identity': [16777229, 50887611, 33152, 1, 876872, 1792071339434192296, 1792071339434192296]}
def partial_current7(p):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'partial archive has exact three-field current7-only role, never SHA/fullPF')
 return current(p)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'actual independent executor and once-only immutable failure facts post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);need(pRoot==EXPECTED_ACTUAL_ROOT_TOOLS_PIN and pHost==EXPECTED_ACTUAL_HOST_PIN,'only this exact recorded genuine Root1/Host failure episode')
 root=meta(pRoot);host=meta(pHost);terminal=root['actual_terminal_return']
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1 and terminal.get('session_id')is None and root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine closed Root1 and original permission/retry facts, never Root0 inferred')
 pb=host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];source_limit=b['bounded_Source_metadata_bytes'];limit=b['bounded_total_output_bytes']
 need(pHost['path']==str(out/'Root_actual_single_B2_SQL_pool_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_B2_PAIRED_SQL_POOL_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'and host['status']=='FAILED_B2_PAIRED_SQL_POOL_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED'and host['failure']=="RuntimeError('own-child stage failed; no retry')"and host['secondary_failures']==[]and host['archive_complete']is False and host['actual_child_receipt']is None and host['actual_watchdog']is None and host['all2_original_plain_current7_retained']is True and host['original_caps']==CAPS and host['retries']==0 and host['original_guard_class_and_MRO_unchanged']is True and host['final_report_resource_check_passed']is True,'actual failed Host with original None receipt/watch preserved, no complete child/pair claimed')
 need(admit_prior(b)==out and limit==32*2**20 and b['bounded_archive_payload_bytes']==24*2**20 and source_limit==16*2**20 and host['complete_joint_roots']==roots and len(roots)==81,'same frozen full81 admission, historical physical exact1 evidence, original32/24/Source16 caps')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
 need(author['whole_Source_file_pins']==sf['complete_source_file_pins']==ready['complete_source_file_pins']and len(sf['complete_source_file_pins'])==5 and author['original48_archive_one_wholebytes_equal']is True and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and hf['selected_source_freeze_pin']==host['source_freeze_pin']and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'exact frozen five Source/PLAN and unchanged original byte archival algorithm')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['failure']is None and peer['status']=='PASS_SOURCE_ONLY_CURRENT_PAIRED_B2_SQL_POOL_LOSSLESS_ARCHIVE'and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'actual same-round Source review0 does not imply archive success')
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(root['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','genuine Root original exact24argv/command and frozen Source identity')
 need(len(host['records'])==1,'one original failed stage, no retry');record=host['records'][0];need(record['status']=='FAILED'and record['error']=='own-child stage failed; no retry','original FAILED/error record preserved verbatim')
 wp=pin(out/(record['label']+'.watchdog.json'));lp=pin(out/(record['label']+'.log'));w=meta(wp);log=full(lp).read_text();full(lp)
 need(type(w['returncode'])is int and w['returncode']==1 and w['limit_failure']is None and w['command']==record['command']and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'standalone record.label watchdog real child1 distinct from Host embedded None')
 need(log.endswith('RuntimeError: paired gzip payload below24MiB; no compression assumption\n')and 'BoundedArchiveSink'not in log or log.endswith('RuntimeError: paired gzip payload below24MiB; no compression assumption\n'),'actual saved child traceback ends at original gzip payload cap')
 claimpin=pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json');claim=meta(claimpin);cmd=record['command'];need(len(cmd)==9 and cmd[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',ready['worker_source_pin']['path'],'--binding-pin']and json.loads(cmd[4])==pb and cmd[5]=='--common-source-pin'and json.loads(cmd[6])==hf['common_source_pin']and cmd[7:]==['--expected-parent-pid',str(claim['PID'])],'actual worker command and original exclusive parent Source/binding identity')
 ccp=pin(out/'CHILD_ARCHIVE_CLAIM.json');cc=meta(ccp);need(cc['PID']==w['pid']and cc['parent_PID']==claim['PID']and cc['retries']==0,'original one actual child PID/parent, no retry')
 ffp=pin(out/'FIRST_ARCHIVE_FAILURE.json');ff=meta(ffp);need(ff['schema']=='CURRENT_B2_PAIRED_SQL_POOL_ARCHIVE_FIRST_FAILURE_V1'and ff['failure']=="RuntimeError('paired gzip payload below24MiB; no compression assumption')"and ff['phase']=='ARCHIVE_1'and ff['original_plain_files_deleted']is False and ff['retry_performed']is False and len(ff['completed_entry_pins'])==1,'real first failure in pool phase after exactly one completed entry')
 ep=ff['completed_entry_pins'][0];entry=meta(ep);originals=b['all2_plain_pins'];need(len(originals)==2 and [p['size_bytes']for p in originals]==[52441088,150267572]and b['compression_order']=='SQL_THEN_ORIGINAL_POOL','whole original ordered SQL/pool retained, no truncation or numerical parsing')
 sql=originals[0];pool=originals[1];gz=entry['compressed_archive_full_pin'];need(ep['path']==str(out/'archive_entry_000.json')and entry['ordinal']==0 and entry['actual_B2_output_role']=='PAIRED_SQLITE_INDEX'and entry['original_plain_full_pin']==sql and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==sql['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==sql['size_bytes']==52441088 and entry['exact_original_plain_bytes_recoverable']is True and entry['original_plain_preserved']is True and entry['result_values_decoded']is False and entry['scientific_values_decoded']is False and entry['filename_field']==''and entry['mtime']==0 and entry['compresslevel']==6,'durable SQL member0 completed Root-streamed input/decompression SHA/length metadata, original still preserved')
 need(gz['path']==str(out/'archives/000_complete_native_original_path_index.sqlite.gz')and gz['size_bytes']==7025974,'only completed SQL gzip may be blindly hashed twice');full(gz);full(gz)
 partial=out/'archives/001_complete_native_original_value_bytes.bin.gz';st=partial.lstat();ppart=dict(path=str(partial),size_bytes=st.st_size,identity=ids(st));partial_current7(ppart)
 need(ppart['size_bytes']==17639368 and ff['partial_archive_paths']==[gz['path'],str(partial)]and not os.path.lexists(out/'archive_entry_001.json')and not os.path.lexists(out/'CURRENT_PAIRED_B2_SQL_POOL_LOSSLESS_ARCHIVE_INDEX.json')and not os.path.lexists(out/'ACTUAL_PAIRED_B2_SQL_POOL_LOSSLESS_ARCHIVE_REPORT.json'),'pool partial stat-only with no completion entry, pair index or child report')
 # Full output inventory accounting; never open/hash the partial pool gzip.
 observed=[];metadata_pins=[];ownbytes=0
 for p in sorted(out.rglob('*')):
  st=p.lstat();need(not stat.S_ISLNK(st.st_mode),'no output alias')
  if stat.S_ISREG(st.st_mode):
   observed.append(str(p));ownbytes+=st.st_size
   if p==partial:partial_current7(ppart)
   elif str(p)==gz['path']:current(gz)
   else:
    need(st.st_size<8*2**20 and p.suffix in('.json','.log','.py'),'only bounded Source/control metadata apart from exact complete SQL gzip and exact pool partial')
    pm=pin(p);full(pm);metadata_pins.append(pm)
  else:need(stat.S_ISDIR(st.st_mode),'ordinary output directory')
 need(len(observed)==10 and ownbytes<limit,'complete failed output inventory and original32MiB cap, no dropped partial bytes')
 build=meta(b['original_guard_build_plan_pin'])
 for _ in range(2):
  for p in originals+b['retained_current7_pins']+b['retained_B2_current_epoch_readonly_pins']:current(p)
  for p in b['retained_failed_v1_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'old failed eight roles remain strict three-field stat-only');current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  partial_current7(ppart);current(gz)
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 before=host['resources_before'];need(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes']+limit+source_limit<2*2**30,'actual original prelaunch worst32+Source16 reservation retained even though compression failed')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full81/external/open-unlinked/cold/free caps count all complete and partial bytes')
 for obj in(host,ff):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(obj[key]is False,'failure facts cannot grant pair completion, science or retirement qualification')
 result=dict(schema='RECORDED_CURRENT_B2_PAIRED_SQL_POOL_ARCHIVE_FAILURE_AND_SQL_MEMBER0_METADATA_POSTVERIFY_V1',status='PASS_RECORDED_ACTUAL_B2_SQL_POOL_ARCHIVE_ROOT1_CHILD1_SQL_MEMBER0_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=1,actual_child_integer_exit_code=w['returncode'],actual_Host_status=host['status'],actual_Host_failure=host['failure'],actual_Host_embedded_watchdog=host['actual_watchdog'],actual_Host_child_receipt=host['actual_child_receipt'],actual_child_report_pin=None,actual_archive_index_pin=None,actual_complete_pair_archive_success=False,actual_pair_archive_complete=host['archive_complete'],actual_original_runner_record=record,actual_standalone_child_watchdog=w,actual_watchdog_pin=wp,actual_child_log_pin=lp,actual_first_archive_failure_pin=ffp,actual_first_archive_failure=ff,execution_binding_pin=pb,original_SQL_pool_ordered_full_pins=originals,original_pair_current7_verified_twice=True,actual_complete_SQL_entry_pin=ep,actual_complete_SQL_gzip_full_pin=gz,actual_original_SQL_full_pin=sql,actual_SQL_member0_entry_metadata=entry,SQL_member0_recorded_complete_archive_entry=True,actual_Root_recorded_SQL_input_and_decompression_SHA_length_match=True,complete_SQL_gzip_blind_fullEOF_SHA_current7_verified_twice=True,pool_partial_current7_only_pin=ppart,pool_partial_body_opened_or_hashed=False,partial_pool_complete_or_restorable_inferred=False,all_other_output_Source_or_metadata_blind_SHA_pins=metadata_pins,all_failed_output_paths=observed,actual_entire_failed_archive_output_bytes=ownbytes,complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,actual_original_Host_resources_before=host['resources_before'],actual_original_Host_resources_after=host['resources_after'],actual_original_Host_resources_after_including_summary=host['resources_after_including_summary_bytes'],final_original_report_resource_check_passed=host['final_report_resource_check_passed'],retained_current7_pins=b['retained_current7_pins'],retained_failed_v1_current7_only_pins=b['retained_failed_v1_current7_only_pins'],retained_B2_current_epoch_readonly_pins=b['retained_B2_current_epoch_readonly_pins'],all_originals_and_retained_roles_current7_verified_twice=True,core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_CLI_pin=cli_pin,actual_Source_freeze_pin=host['source_freeze_pin'],actual_Host_freeze_pin=host['host_freeze_pin'],actual_Root_claim_pin=claimpin,actual_child_claim_pin=ccp,future_SQL_member0_independent_restore_Root_report_pin=None,future_SQL_member0_independent_restore_post_pin=None,complete_SQL_pool_pair_or_original_retirement_authorized=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

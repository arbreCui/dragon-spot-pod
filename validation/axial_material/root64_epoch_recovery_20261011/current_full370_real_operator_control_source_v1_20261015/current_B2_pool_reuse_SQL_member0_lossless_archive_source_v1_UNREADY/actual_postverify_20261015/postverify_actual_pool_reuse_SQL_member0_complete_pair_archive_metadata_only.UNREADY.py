"""UNREADY independent metadata post for an actual pool archive reusing the independently verified retired SQL member0.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. New compressed outputs are blindly hashed; no original payload read, repeat decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B2_pool_reuse_SQL_member0_lossless_archive_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '7b2505af64f6c6fc8d0b3c7dbe2ee03df2739a46f33c19303b2e5399524758af', 'size_bytes': 5917, 'identity': [16777229, 50890614, 33188, 1, 5917, 1792073321183178118, 1792073321183178118]}
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
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh single physical directory archive output')
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
OUT_CAP=72*2**20;ARCHIVE_CAP=64*2**20;SOURCE_CAP=8*2**20
def true0(p,key,stdout_role,expected):
 v=meta(p);genuine(v,key,expected,stdout_role);return v
def unique(rows):
 out={}
 for p in rows:need(p['path']not in out or out[p['path']]==p,'same path same wholePF');out[p['path']]=p
 return list(out.values())
def current_retired_SQL_and_discarded_partial(binding):
 rows=binding['exact_historical_SQL_and_discarded_partial_target_pins']
 need(type(rows)is list and len(rows)==2 and rows[0]==binding['historical_SQL_full_pin']
  and rows[1]==binding['discarded_partial_pool_current7_only_pin']and set(rows[1])=={'path','size_bytes','identity'},
  'exact historical SQL fullPF and discarded incomplete pool gzip stat3, never generalized missing skip')
 for p in rows:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),
   'only proved retired SQL and discarded exact incomplete pool gzip absent; never current-stat historical deleted targets')
def admit_prior(binding):
 need(binding['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_BINDING_V1'
  and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False
  and binding['Source_admission_ready']is False and binding['original_caps']==CAPS
  and type(binding['actual_current_resource_stage_budget'])is dict,
  'future exact SQL-plus-partial Root0/post0 and complete81 latest72plus16 budget NULL hard reject')
 previouspin=binding['actual_SQL_partial_recovery_plan_pin'];previous=meta(previouspin)
 receipt=meta(binding['actual_SQL_partial_recovery_receipt_pin']);post=meta(binding['actual_SQL_partial_recovery_post_pin'])
 true0(binding['actual_SQL_partial_recovery_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_SQL_partial_recovery_receipt_pin'])
 true0(binding['actual_SQL_partial_recovery_post_tools_pin'],'actual_review_return','review_pin',binding['actual_SQL_partial_recovery_post_pin'])
 sql=binding['historical_SQL_full_pin'];partial=binding['discarded_partial_pool_current7_only_pin'];targets=[sql,partial]
 need(previous['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_PLAN_V1'
  and previous['Source_admission_ready']is True and previous['draft_unready']is False and previous['no_new_output_root']is True
  and previous['original_caps']==CAPS and previous['exact_target_pins']==targets
  and previous['exact_original_SQL_full_pin']==sql and previous['exact_partial_pool_current7_only_pin']==partial
  and previous['target_role_kinds']==['RESTORABLE_SQL_FULLPF','INCOMPLETE_POOL_GZIP_CURRENT7_ONLY']
  and sql['size_bytes']==52441088 and set(partial)=={'path','size_bytes','identity'}and partial['size_bytes']==17639368,
  'only exact recovered SQL fullPF plus incomplete pool-gzip3 targets, never complete original pool retirement or wholepair success')
 need(receipt['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_RECEIPT_V1'
  and receipt['mode']=='execute'and receipt['status']=='RECOVERED_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED'
  and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==targets
  and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==70080456 and receipt['files_deleted']is True
  and receipt['resources_after_original_classes_forced_fresh']is True and receipt['whole_pair_archive_complete']is False
  and receipt['partial_target_body_opened_or_hashed']is False and receipt['generic_missing_path_skip_authorized']is False,
  'genuine new exact2 recovery Root0, original pair Root1/child1 failure remains failure')
 contract=binding['actual_SQL_partial_recovery_post_contract']
 need(post['schema']==contract['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'
  and post['status']==contract['status']=='PASS_ACTUAL_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED_METADATA_ONLY'
  and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_SQL_partial_recovery_receipt_pin']
  and post['actual_Root_tools_pin']==binding['actual_SQL_partial_recovery_Root_tools_pin']and post['plan_pin']==previouspin
  and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0
  and post['exact_target_pins']==post['actual_released_pins']==targets and type(post['actual_released_bytes'])is int and post['actual_released_bytes']==70080456
  and post['files_deleted']is True and post['files_deleted_by_post']is False and post['exact_two_targets_absent_verified_twice']is True
  and post['resources_after_original_classes_forced_fresh']is True and post['partial_target_body_opened_or_hashed']is False
  and post['whole_pair_archive_complete']is False and post['all_complete_results_preserved']is True
  and post['historical_deleted_target_PFs_not_claimed_current']is True and post['future_consumer_must_restore_SQL_with_exact_original_pool']is True
  and post['generic_missing_path_skip_authorized']is False,'genuine independent exact2 recovery metadata post0; no prior pair-success gate bypass')
 originalpin=previous['original_pair_execution_binding_pin'];original=meta(originalpin)
 pool=original['all2_plain_pins'][1];gzip=binding['reused_SQL_member0_gzip_pin'];ep=binding['reused_SQL_member0_entry_pin'];entry=meta(ep)
 need(original['all2_plain_pins']==[sql,pool]and pool['size_bytes']==150267572
  and binding['all1_plain_pins']==[pool]and binding['all2_original_pair_pins']==[sql,pool]
  and binding['original_plain_total_bytes']==150267572 and binding['original_pair_total_bytes']==202708660
  and binding['compression_order']=='ONLY_LIVE_ORIGINAL_POOL_REUSE_COMPLETE_SQL_MEMBER0_IN_PLACE',
  'only pool150267572 compressed; original SQL is historical and its complete gzip reused at original path without copy or link')
 mp=previous['actual_SQL_member0_control_closure_pins'];member=meta(mp['Root_report']);memberpost=meta(mp['post'])
 true0(mp['Root_tools'],'actual_terminal_return','report_pin',mp['Root_report']);true0(mp['post_tools'],'actual_review_return','review_pin',mp['post'])
 need(member['schema']=='ROOT_CURRENT_B2_SQL_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1'
  and member['status']=='PASS_CURRENT_B2_SQL_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY'and member['failure']is None
  and member['original_member0_saved_full_pin']==sql and member['complete_member0_gzip_pin']==gzip and member['retained_member0_entry_pin']==ep
  and member['streamed_complete_member0_verified']is True and member['streamed_decompressed_SHA']==sql['sha256']and member['streamed_decompressed_length']==52441088
  and member['paired_SQL_pool_archive_complete']is False and member['original_member0_body_opened']is False
  and memberpost['actual_member0_Root_report_pin']==mp['Root_report']and memberpost['actual_Root_tools_pin']==mp['Root_tools']
  and memberpost['failure']is None and memberpost['Root_actual_complete_member0_stream_verified']is True
  and memberpost['original_member0_saved_full_pin']==sql and memberpost['complete_member0_gzip_pin']==gzip,
  'independent SQL member0 Root-only byteproof0 plus separate metadata post0 before exact recovery')
 mapping=previous['SQL_with_exact_live_original_pool_recovery_map']
 need(receipt['SQL_with_exact_live_original_pool_recovery_map']==post['SQL_with_exact_live_original_pool_recovery_map']==binding['SQL_with_exact_live_original_pool_recovery_map']==mapping
  and mapping==dict(historical_SQL_full_pin=sql,complete_SQL_gzip_full_pin=gzip,SQL_member0_entry_pin=ep,exact_live_original_pool_full_pin=pool,
   SQL_member0_Root_control_pin=mp['Root_report'],SQL_member0_independent_post_pin=mp['post'],restore_SQL_and_use_exact_original_pool_together=True,
   whole_pair_archive_complete=False,generic_missing_path_skip_authorized=False)
  and previous['retained_SQL_member0_gzip_pin']==post['retained_SQL_member0_gzip_pin']==gzip
  and previous['retained_SQL_member0_entry_pin']==post['retained_SQL_member0_entry_pin']==ep,
  'exact historical SQL-to-live-original-pool restoration mapping retained, never inferred pair success')
 need(entry['ordinal']==0 and entry['actual_B2_output_role']=='PAIRED_SQLITE_INDEX'and entry['original_plain_full_pin']==sql
  and entry['compressed_archive_full_pin']==gzip and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==sql['sha256']
  and entry['compression_input_length']==entry['streamed_decompressed_length']==52441088 and entry['exact_original_plain_bytes_recoverable']is True
  and entry['original_plain_preserved']is True,'old SQL entry preserved whole; true original_plain_preserved means archive-creation history only')
 expected=unique(previous['retained_current7_pins']+previous['retained_archive_metadata_current7_pins']+[gzip,ep])
 need(pool in expected and binding['retained_current7_pins']==[p for p in expected if p!=pool]
  and binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']
  and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins']
  and not{p['path']for p in targets}&{p['path']for p in expected},'all complete results/native/comparison/physical permanent mapping/failed8/cold9 retained; missing exception exact SQL and discarded partial only')
 proofs=[binding[k]for k in('actual_SQL_partial_recovery_plan_pin','actual_SQL_partial_recovery_receipt_pin','actual_SQL_partial_recovery_Root_tools_pin','actual_SQL_partial_recovery_post_pin','actual_SQL_partial_recovery_post_tools_pin')]+[originalpin]+list(previous['actual_pair_failure_closure_pins'].values())+list(mp.values())+[ep]
 need(binding['latest_complete_plan_pin']==previouspin and binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']
  and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),
  'complete existing explicit metadata table plus exact recovery failure/member0 closures, no lost old Host or external bytes')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots']
 need(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']and len(prefix)==81
  and binding['complete_joint_roots']==prefix+[str(out)]and len(binding['complete_joint_roots'])==82 and out.parent==ART
  and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))
  and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),
  'entire real existing81 including all failed roots plus only one fresh pool owning82 root')
 need(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP
  and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP
  and binding['SQL_recompressed_copied_or_hardlinked']is False and binding['future_consumer_must_restore_exact_SQL_pool_pair_together']is True,
  'candidate whole72MiB=64newpoolgzip+8runtime metadata plus Source8 must fit actual fullscope2GiB; no compression or future budget assumption')
 return out
def failure_facts(root,pRoot,host,pHost,b,pb,out,source_limit):
 standalone=None;wp=None;observed=[];rows=[]
 if host is not None:
  for record in host['records']:
   q=out/(record['label']+'.watchdog.json')
   if os.path.lexists(q):
    wp=pin(q);standalone=meta(wp);need(standalone['command']==record['command']and type(standalone['returncode'])is int,'only actual per-label standalone child watchdog fact');observed.append(standalone['returncode'])
 if os.path.lexists(out):
  for q in sorted(out.rglob('*')):
   st=q.lstat();need(not stat.S_ISLNK(st.st_mode),'actual failed output no alias')
   if stat.S_ISREG(st.st_mode):rows.append(dict(path=str(q),size_bytes=st.st_size,identity=ids(st)))
 result=dict(schema='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=root['original_integer_exit_code'],actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_Host_embedded_watchdog=None if host is None else host['actual_watchdog'],actual_Host_child_receipt=None if host is None else host['actual_child_receipt'],actual_standalone_watchdog_pin=wp,actual_standalone_watchdog=standalone,actual_recorded_child_integer_exit_codes=observed,actual_stage_records=None if host is None else host['records'],absent_child_code_invented=False,archive_success_or_roundtrip_or_complete_pair_inferred=False,failed_output_current7_only_three_field_rows=rows,failed_gzip_or_partial_payload_body_opened_or_hashed=False,execution_binding_pin=pb)
 save(result,source_limit)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+role,required=True)
 args=ap.parse_args();need(args.executor_task_name==EXECUTOR and args.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent exact executor, immutable single metadata execution')
 pRoot=json.loads(args.Root_tools_pin);pHost=json.loads(args.Host_pin);root=meta(pRoot);terminal=root['actual_terminal_return'];host=None if pHost is None else meta(pHost)
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==root['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed original Root integer, no live handle inference')
 full(EXPECTED_CORE_AUTHOR_FREEZE);author=meta(EXPECTED_CORE_AUTHOR_FREEZE);pb=pin(PACKAGE/'PLAN.json')if host is None else host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];limit=b['bounded_total_output_bytes'];source_limit=b['bounded_Source_metadata_bytes'];code=root['original_integer_exit_code']
 need(b['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_BINDING_V1'and b['original_caps']==CAPS and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and limit==OUT_CAP==72*2**20 and b['bounded_archive_payload_bytes']==ARCHIVE_CAP==64*2**20 and b['metadata_runtime_headroom_bytes']==8*2**20 and source_limit==SOURCE_CAP==8*2**20 and roots[-1]==str(out),'frozen local72=64newpoolgzip+8metadata/runtime and localSource8, original global caps unchanged')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_single_B2_pool_reuse_SQL_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1','exact real owning pool-reuse-SQL Host report')
 if code!=0:failure_facts(root,pRoot,host,pHost,b,pb,out,source_limit);return
 need(host is not None,'Root0 requires actual emitted Host PF');genuine(root,'actual_terminal_return',pHost,'report_pin')
 need(root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False and host['status']=='ACTUAL_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and host['failure']is None and host['secondary_failures']==[]and host['archive_complete']is True and host['retries']==0 and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False and host['independent_archive_post0_required']is True and host['original_pool_current7_retained']is True and host['historical_SQL_original_retired']is True,'actual Root0 complete paired archive with original pool live and historical SQL retired')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin);static=meta(author['source_static_evidence_pin'])
 need(author['Source_only_frozen_before_Root_generation']is True and author['whole_Source_file_pins']==sf['complete_source_file_pins']and len(sf['complete_source_file_pins'])==5 and static['archive_one_original_function_wholebytes_SHA']=='db8a6b9fe2234c77f460274fe3d73d5fe43377089ef8341c305b8b20da892495'and static['archive_one_original_function_bytes']==2311,'exact frozen five Source table and original48 archive_one wholebytes proof')
 need(ready['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and sf['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_HOST_FREEZE_V1'and hf['source_only']is True and hf['selected_source_freeze_pin']==host['source_freeze_pin']and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and ready['complete_source_file_pins']==sf['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'same actual READY/SF/HF complete Source and exact plan')
 admission=meta(ready['Root_completed_admission_binding_pin']);template=meta(author['whole_NULL_admission_binding_template_pin']);mutable=set(author['Root_final_binding_fields_filled_after_genuine_SQL_partial_recovery0']);need(set(admission)==set(template)and all(admission[k]==v for k,v in template.items()if k not in mutable)and all(b[k]==v for k,v in admission.items()),'only author-declared true recovery and budget fields filled; remaining template preserved')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin');need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE'and peer['failure']is None and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'same genuine independent complete Source0 and RootGEN0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(root['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact original Root command string/full24argv/Source identities')
 latest=meta(b['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==b['inherited_latest_complete_joint_roots']+[str(out)]and roots[:-1]==latest['complete_joint_roots']and len(roots)==len(set(roots))==82 and len(roots[:-1])==81 and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'full actual81 including failed roots plus only one fresh82, Source already counted')
 need(admit_prior(b)==out,'same frozen common admission reproduced in pure metadata, no candidate/helper import');originals=b['all2_original_pair_pins'];pool=b['all1_plain_pins'][0];sql=b['historical_SQL_full_pin'];oldgzip=b['reused_SQL_member0_gzip_pin'];oldentrypin=b['reused_SQL_member0_entry_pin'];oldentry=meta(oldentrypin)
 need(originals==[sql,pool]and [p['size_bytes']for p in originals]==[52441088,150267572]and b['all1_plain_pins']==[pool]and host['reused_SQL_member0_gzip_pin']==oldgzip and host['reused_SQL_member0_entry_pin']==oldentrypin,'exact SQL52M historical member0 and pool150M only new compressed original; old gzip/entry reused in place')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins)
 need(len(host['records'])==1 and host['records'][0]['status']=='PASS','one original guarded child0 no retry');record=host['records'][0];wp=table[str(out/(record['label']+'.watchdog.json'))];lp=table[str(out/(record['label']+'.log'))];w=meta(wp)
 need(w==host['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and lp['sha256']==record['log_sha256'],'genuine record.label watchdog/log/wall/RSS/liveness child0')
 claim=meta(pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'));command=record['command'];need(len(command)==9 and command[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',str(PACKAGE/'archive_B2_pool_reuse_SQL_serial.UNREADY.py'),'--binding-pin']and json.loads(command[4])==pb and command[5]=='--common-source-pin'and json.loads(command[6])==hf['common_source_pin']and command[7:]==['--expected-parent-pid',str(claim['PID'])],'actual exact sole child command, real parent Root PID and same common/binding')
 log=full(lp);need(lp['size_bytes']<8*2**20,'small child receipt metadata');lines=log.read_text().splitlines();need(len(lines)==1,'one complete child receipt');receipt=json.loads(lines[0]);need(receipt==host['actual_child_receipt'],'same actual Host/child receipt')
 childpin=receipt['report_pin'];child=meta(childpin);need(childpin['path']==str(out/'ACTUAL_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_REPORT.json')and child['schema']=='ACTUAL_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'and child['status']=='B2_POOL_REUSE_SQL_MEMBER0_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None and type(child['completed_count'])is int and child['completed_count']==2 and child['binding_pin']==pb and child['original_pool_current7_retained']is True and child['historical_SQL_original_retired']is True and child['reused_SQL_count']==child['newly_compressed_pool_count']==1 and child['all_other_current_outputs_native_and_inputs_current7_retained']is True,'actual complete pair child report, one SQL reused and one new pool')
 indexpin=child['index_pin'];index=meta(indexpin);need(indexpin['path']==str(out/'CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_INDEX.json')and index['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and index['status']=='B2_POOL_REUSE_SQL_MEMBER0_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'and index['binding_pin']==pb and len(index['entries'])==index['ordered_original_plain_count']==2 and index['ordered_original_plain_total_bytes']==child['original_pair_total_bytes']==b['original_pair_total_bytes']==202708660 and index['paired_SQL_pool_original_pins']==originals and index['reused_SQL_count']==index['newly_compressed_pool_count']==1 and index['historical_SQL_original_retired']is True and index['original_pool_current7_retained']is True and index['SQL_original_preserved_at_archive_creation_only']is True and index['compression_ratio_assumed']is False and index['requires_independent_post0_before_separate_plain_retirement']is True and index['future_consumer_must_restore_exact_SQL_pool_pair_together']is True and index['generic_missing_path_skip_authorized']is False,'new complete pair lookup index with exact ordered SQL/pool proofs and exact one-retired one-live lifecycle')
 row0,row1=index['entries'];expected0=dict(oldentry);expected0.update(original_plain_preserved_at_archive_creation=oldentry['original_plain_preserved'],original_plain_preserved=False,original_plain_retired=True,original_plain_retirement_receipt_pin=b['actual_SQL_partial_recovery_receipt_pin'],entry_pin=oldentrypin,reused_existing_member0_without_copy_or_link=True)
 need(oldentry['original_plain_preserved']is True and row0==expected0 and row0['compressed_archive_full_pin']==oldgzip and row0['original_plain_full_pin']==sql,'only exact six-field lifecycle overlay on whole original SQL entry; original entry creation-history True never changed')
 pgz=row1['compressed_archive_full_pin'];pe=row1['entry_pin'];newentry=meta(pe)
 need(row1['ordinal']==1 and type(row1['ordinal'])is int and row1['original_plain_full_pin']==pool and row1['original_plain_preserved']is True and newentry=={k:v for k,v in row1.items()if k!='entry_pin'}and pgz['path']==str(out/'archives'/('001_'+Path(pool['path']).name+'.gz'))and table[pgz['path']]==pgz and pe['path']==str(out/'archive_entry_001.json')and table[pe['path']]==pe,'new pool durable entry exactly equals index row1, complete unique pool gzip only')
 proofs=[]
 for ordinal,(row,original)in enumerate(zip(index['entries'],originals,strict=True)):
  need(row['ordinal']==ordinal and row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['result_values_decoded']is False and row['scientific_values_decoded']is False and row['actual_B2_output_role']==('PAIRED_SQLITE_INDEX','PAIRED_ORIGINAL_PAYLOAD_POOL')[ordinal]and row['filename_field']==''and row['mtime']==0 and row['compresslevel']==6,'both Root-recorded full original/decompressed SHA and lengths equal exact original fullPFs, no repeated decompression')
  proofs.append(dict(original_plain_full_pin=original,compressed_archive_full_pin=row['compressed_archive_full_pin'],entry_pin=row['entry_pin'],actual_streamed_original_SHA=row['streamed_decompressed_SHA'],actual_streamed_original_length=row['streamed_decompressed_length'],newly_compressed_by_this_stage=ordinal==1))
 gzips=[oldgzip,pgz];entrypins=[oldentrypin,pe];need(index['paired_SQL_pool_archive_entry_pins']==entrypins and index['new_pool_gzip_bytes']==child['new_pool_gzip_bytes']==pgz['size_bytes']<b['bounded_archive_payload_bytes']and index['reused_SQL_gzip_bytes']==oldgzip['size_bytes']and sum(p['size_bytes']for p in gzips)==index['total_gzip_bytes']==child['total_gzip_bytes']and ownbytes<limit and {p['path']for p in newpins if Path(p['path']).suffix=='.gz'}=={pgz['path']},'only one newly produced pool gzip bounded64MiB, old SQL gzip reused in place outside new output; complete pair count2')
 childclaim=meta(table[str(out/'CHILD_ARCHIVE_CLAIM.json')]);need(childclaim['PID']==w['pid']and childclaim['parent_PID']==claim['PID']and childclaim['retries']==0,'actual own sole child PID and no retry')
 build=meta(b['original_guard_build_plan_pin'])
 for _ in range(2):
  current(pool);current(oldgzip);current(oldentrypin);current_retired_SQL_and_discarded_partial(b)
  for p in b['retained_current7_pins']:current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  for p in b['retained_B2_current_epoch_readonly_pins']+b['retained_failed_v1_current7_only_pins']:current(p)
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 archive_resources(child['resources_after'],roots,600);before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes'];need(existing+limit+source_limit<2*2**30 and before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'real full81 plus actual external/open-unlinked before launch plus72output/8Source reservation within original caps')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full82 joint/external/open-unlinked/cold/free original limits')
 for item in(host,child,index):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(item[key]is False,'byte archive does not grant scientific/physics/native/retirement qualification')
 for p in[pHost,childpin,indexpin,wp,lp,pgz,pe]:need(table[p['path']]==p,'every current completed new output blindly fullSHA twice; old SQL gzip never hashed by post')
 previous_post=meta(b['actual_SQL_partial_recovery_post_pin'])
 result=dict(schema='RECORDED_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_COMPLETE_PAIR_ARCHIVE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_B2_COMPLETE_SQL_POOL_PAIR_REUSED_SQL1_NEW_POOL1_ROOT0_CHILD0_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,actual_child_report_pin=childpin,actual_archive_index_pin=indexpin,execution_binding_pin=pb,original_SQL_pool_ordered_full_pins=originals,compressed_SQL_pool_ordered_archive_full_pins=gzips,SQL_pool_ordered_entry_pins=entrypins,Root_actual_streamed_decompression_proofs_matched_ordered_original_fullPFs=True,actual_SQL_pool_roundtrip_byte_proofs=proofs,complete_pair_byte_archive_proof=True,completed_count=2,reused_SQL_count=1,newly_compressed_pool_count=1,only_original_pool_current7_verified_twice=True,historical_SQL_original_absence_verified_twice=True,reused_SQL_gzip_current7_verified_twice=True,reused_SQL_entry_creation_history_preserved=True,reused_SQL_index_row_exact_lifecycle_overlay_verified=True,new_pool_gzip_blind_fullEOF_SHA_current7_verified_twice=True,new_pool_entry_whole_index_row_verified=True,all_retained_current7_verified_twice=True,actual_SQL_partial_recovery_plan_pin=b['actual_SQL_partial_recovery_plan_pin'],actual_SQL_partial_recovery_receipt_pin=b['actual_SQL_partial_recovery_receipt_pin'],actual_SQL_partial_recovery_Root_tools_pin=b['actual_SQL_partial_recovery_Root_tools_pin'],actual_SQL_partial_recovery_post_pin=b['actual_SQL_partial_recovery_post_pin'],actual_SQL_partial_recovery_post_tools_pin=b['actual_SQL_partial_recovery_post_tools_pin'],SQL_with_exact_live_original_pool_recovery_map=b['SQL_with_exact_live_original_pool_recovery_map'],historical_SQL_original_full_pin=sql,historical_discarded_partial_pool_current7_only_pin=b['discarded_partial_pool_current7_only_pin'],historical_SQL_and_partial_exact_absence_only=True,original_failed_pair_still_failed=True,old_SQL_entry_file_modified=False,old_SQL_original_current7_or_body_or_SHA_attempted=False,old_SQL_gzip_body_opened_or_hashed=False,retained_failed_v1_current7_only_pins=b['retained_failed_v1_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=previous_post['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved'],prior_v1_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=b['retained_current7_pins'],bridge9_cold_readonly_current7_pins=b['retained_B2_current_epoch_readonly_pins'],actual_historical_ordered_original_pair_bytes=sum(p['size_bytes']for p in originals),actual_original_pool_retained_bytes=pool['size_bytes'],actual_complete_pair_gzip_bytes=sum(p['size_bytes']for p in gzips),actual_new_pool_gzip_bytes=pgz['size_bytes'],actual_entire_archive_output_bytes=ownbytes,actual_original_runner_record=record,actual_original_watchdog=w,actual_watchdog_pin=wp,actual_child_log_pin=lp,actual_index_entry_metadata=index['entries'],complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,local_Source_bound_bytes=source_limit,local_new_output_bound_bytes=limit,actual_original_Host_resources_before=host['resources_before'],actual_original_Host_resources_after=host['resources_after'],actual_original_Host_resources_after_including_summary=host['resources_after_including_summary_bytes'],actual_original_child_resources_after=child['resources_after'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_CLI_pin=cli_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,future_consumer_must_restore_exact_SQL_pool_pair_together=True,generic_missing_path_skip_authorized=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

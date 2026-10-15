"""UNREADY independent metadata post for an actual SQL and incomplete pool gzip exact1 readonly check.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Source and plan are checked against the real owning receipt and author freeze; future actual parameters remain NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_early14_B2_pool_and_failed_partial_exact16_spool_lifecycle_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '090458db226c526ab0a0760dcee61eabcdd356bb4c3042c1ea83cdd18ce29f6a', 'size_bytes': 3314, 'identity': [16777229, 50891714, 33188, 1, 3314, 1792074733206352470, 1792074733206352470]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(target_payload_body_opened_or_hashed=False,gzip_payload_body_opened_or_hashed=False,worker_or_guard_helpers_imported=False,worker_executed=False,lsof_executed=False,PS_executed=False,native_executed=False,compiler_executed=False,compression_repeated=False,decompression_repeated=False,numerical_executed=False,JSONL_or_array_values_decoded=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B55 control output')
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
def readonly_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['joint']['resource_roots']==roots,'actual same original SELF512/stage600 and complete joint root topology')
 h=v['history'];j=v['joint'];sample=v['actual_PS_return']
 need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'actual saved original same-PID PS return/RSS facts, PS not repeated by post')
 need(j['artifact_bytes']+v['external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original joint/history/cold/metadata/free caps including external/open-unlinked')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
def current_failed_v1(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q
def current_partial(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p==plan['exact_failed_pool_partial_current7_only_pin'],
  'only declared incomplete new pool gzip stat-only target; no fullPF/SHA or generalized exception')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes']==67099371,'exact owned failed fragment current7; body never opened or hashed')
 return q
def current_failed_pool(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool metadata/runtime rows, never fullPF/SHA or deletion targets')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-pool retained row stable current7 only')
 return q
def failed_pool_rows(out):
 rows=[];todo=[out]
 while todo:
  with os.scandir(todo.pop())as entries:
   for e in entries:
    st=e.stat(follow_symlinks=False);need(not stat.S_ISLNK(st.st_mode),'entire failed archive has no aliases')
    if stat.S_ISDIR(st.st_mode):todo.append(Path(e.path))
    elif stat.S_ISREG(st.st_mode):rows.append(dict(path=e.path,size_bytes=st.st_size,identity=ids(st)))
    else:raise RuntimeError('failed archive special file not admitted')
 return sorted(rows,key=lambda p:p['path'])
def admit_completed_consumers(plan,archiveplan):
 audit=meta(plan['actual_completed_spool_role_audit_pin'])
 need(audit['schema']=='EXACT16_COMPLETED_DERIVED_SPOOL_AND_FAILED_PARTIAL_ROLE_PROJECTION_SOURCE_METADATA_ONLY_V1'
  and audit['source_only']is True and audit['metadata_only']is True and audit['formal_retirement_admission']is False
  and audit['no_payload_body_opened_or_hashed']is True and audit['target_count']==16 and audit['target_total_bytes']==367026207,
  'independent role audit supplies exact roles, never substitutes final resource or execution admission')
 roles=(('actual_B_extract_closure',2,'actual_Host_report_pin'),('actual_B_aggregate_closure',2,'actual_Host_report_pin'),
  ('actual_B2_epoch_bridge_closure',None,'actual_bridge_report_pin'),('actual_B2_complete_extract_closure',2,'actual_Host_report_pin'),
  ('actual_B2_complete_compare_closure',2,'actual_Host_report_pin'))
 posts={}
 for name,childcode,reportfield in roles:
  c=audit[name];report=meta(c['Root_report']);raw=meta(c['Root_tools'])
  post=meta(c['post']);tools=meta(c['post_tools'])
  genuine(raw,'actual_terminal_return',c['Root_report'],'report_pin');genuine(tools,'actual_review_return',c['post'],'review_pin')
  need(report['failure']is None and post['schema']==c['post_schema']and post['status']==c['post_status']
   and post['failure']is None and post['metadata_only']is True and post[reportfield]==c['Root_report']
   and post['actual_Root_tools_pin']==c['Root_tools']and type(post['actual_Root_integer_exit_code'])is int
   and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==childcode
   and (post['actual_child_integer_exit_code']is None if childcode is None else type(post['actual_child_integer_exit_code'])is int),
   'five genuine completed Root0 plus independent post0 closures, original child2/FAILED or Root-only nochild preserved')
  posts[name]=post
 early=audit['exact_early7_snapshot_descriptors'];B=posts['actual_B_aggregate_closure'];E=posts['actual_B_extract_closure']
 need([r['event']for r in early]==[4,7,8,10,51,52,54]and len(early)==7
  and B['actual_snapshot_pair_count']==8 and B['actual_context_event_count']==55
  and B['all_snapshot_pairs']==early+[audit['retained_final55_snapshot_descriptor']]
  and E['all_snapshot_pairs']==B['all_snapshot_pairs']and E['actual_snapshot_pair_count']==8 and E['actual_context_pin_count']==55
  and E['complete_context_pins']==B['complete_context_pins']==audit['retained_all55_context_pins']
  and B['actual_six_phase_results']==[dict(phase=x,computation_finished=True)for x in('scattering','scalar','fission','extras','overv_fallback','metadata')]
  and B['actual_B_six_phase_engine_evidence_completed']is True,
  'complete actual B8 snapshots55contexts6phases consumed all seven early full SQL-pool pairs; final55 pair and all contexts stay')
 expectedB=dict(actual_compared_source_fields=19249,actual_compared_known_elements=1829421,actual_context_or_operand_issues=0,actual_all_mismatch_elements=0,actual_unknown_macro_producers=0)
 need(audit['actual_B_counts']==expectedB and all(type(B[k])is int and B[k]==v for k,v in expectedB.items()),
  'completed B full19249 fields1829421 elements and actual zero issues/mismatch/unknown, no historical issue rewriting')
 fulltargets=[p for row in early for p in(row['sqlite_pin'],row['native_pool_pin'])]
 X=posts['actual_B2_complete_extract_closure'];C=posts['actual_B2_complete_compare_closure'];N=posts['actual_B2_epoch_bridge_closure']
 need(X['actual_full_physical_tree_counts']==dict(complete_physical_tree_records=62798,complete_directories=7958,complete_extents=8766,complete_MICROLIB2_list1_MACROLIB_records=19620)
  and C['actual_comparison_counts']==dict(compared_all_macro_records=19620,compared_original_payload_words=2264152,raw_word_mismatches=0,metadata_mismatches=0)
  and C['actual_path_sets_equal']is True and C['actual_exact_inventory_metadata_and_all_words_equal']is True,
  'complete independent B2 extraction and full19620/all2264152 original-word comparison consumed exact pool with actual doublezero')
 pool=X['paired_original_pool_pin'];fulltargets.append(pool)
 need(pool==archiveplan['all1_plain_pins'][0]and pool['size_bytes']==150267572
  and fulltargets==audit['exact_ordered15_fullPF_target_pins']==plan['ordered_completed_derived_spool_full_pins']
  and sum(p['size_bytes']for p in fulltargets[:14])==149659264 and sum(p['size_bytes']for p in fulltargets)==299926836,
  'exact ordered seven completed B SQL/pool pairs then completed nativeB2 derived pool, not authoritative native data')
 native=audit['retained_B2_current_epoch_native_archive_pin'];pairs=N['ordered_role_pairs']
 need(len(pairs)==9 and pairs==audit['retained_B2_selected9_readonly_current_epoch_role_pairs']
  and plan['retained_B2_current_epoch_readonly_pins']==[p['current_epoch_full_pin']for p in pairs]
  and native in plan['retained_B2_current_epoch_readonly_pins']and native['sha256']=='f44b2dcb0441f9405b8c927b8fab8cb9903bad9e036dfbb66d025e9c2790c61c'
  and native['size_bytes']==156880856,'exact preserved nativeB2 currentepoch blindRoot0+post0 role, no transitive4790 requalification')
 for pair in pairs:
  need(pair['blind_complete_SHA_and_length_equal']is True and pair['before_open_EOF_after_current7_stable']is True
   and pair['current_epoch_full_pin']['sha256']==pair['historical_full_pin']['sha256']
   and pair['current_epoch_full_pin']['size_bytes']==pair['historical_full_pin']['size_bytes'],'preserved genuine nativeepoch blind-byte equality facts')
  current(pair['current_epoch_full_pin'])
 preserved=audit['retained_seven_original_observer_XSM_pins']+[audit['retained_final55_SQLite_pin'],audit['retained_final55_pool_pin'],audit['retained_final55_XSM_pin']]+audit['retained_all55_context_pins']+audit['all_retained_B2_comparison_result_pins']
 need([row['input_pin']for row in early]==audit['retained_seven_original_observer_XSM_pins']
  and B['all_snapshot_pairs'][-1]['sqlite_pin']==audit['retained_final55_SQLite_pin']
  and B['all_snapshot_pairs'][-1]['native_pool_pin']==audit['retained_final55_pool_pin']
  and B['all_snapshot_pairs'][-1]['input_pin']==audit['retained_final55_XSM_pin']
  and len(audit['all_retained_B2_comparison_result_pins'])==9
  and C['new_complete_output_full_pins']==audit['all_retained_B2_comparison_result_pins']
  and C['actual_complete_comparison_detail_pin']==audit['retained_B2_comparison_detail_pin']
  and all(p in plan['retained_current7_pins']for p in preserved),
  'canonical raw8/final55pair/55contexts/fullcomparison9includingdetail preserved as current; no result document or native target')
 for p in preserved:current(p)
 for evidence in audit['actual_consumer_Source_evidence']:
  full(evidence['Source_pin']);lines=Path(evidence['Source_pin']['path']).read_text().splitlines()
  need(all(type(r['line'])is int and lines[r['line']-1]==r['text']for r in evidence['lines']),
   'exact preserved consumer Source lines: completed native extraction uses spools; future unexecuted pack reads native rather than old SQL-pool')
 need(audit['future_policy']['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False
  and audit['future_policy']['old_SQLgzip_plus_newly_extracted_pool_automatically_compatible_claimed']is False
  and audit['future_policy']['whole_pair_gzip_archive_success_claimed']is False
  and audit['future_policy']['old8_snapshot_or_B2_pair_consumers_must_not_receive_absent_paths']is True
  and audit['future_policy']['generic_missing_path_skip_authorized']is False,'new exact temporary lifecycle policy, not relaxation of any failed archive success gate')
 return audit,dict(completed_consumer_closure_pins={k:audit[k]for k,_,_ in roles},actual_B_counts=expectedB,
  actual_B2_extract_counts=X['actual_full_physical_tree_counts'],actual_B2_comparison_counts=C['actual_comparison_counts'],
  retained_canonical_B_native_pins=audit['retained_seven_original_observer_XSM_pins']+[audit['retained_final55_XSM_pin']],
  retained_B2_current_epoch_native_archive_pin=native)
def complete_archive_metadata(plan,receipt,check_targets_live):
 archiveplan=meta(plan['inherited_failed_pool_archive_plan_pin']);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==archiveplan['complete_joint_roots']and len(roots)==82 and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']==CAPS and len(roots)==len(set(roots))and all(not Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'entire existing82 including failures, no new data root/resource reset')
 need(plan['actual_completed_consumers_and_native_epoch_closed0']is True and plan['actual_pool_failure_Root1_child1_independent_post0_complete']is True and plan['temporary_completed_derived_spool_lifecycle_only']is True and plan['all_original_spool_file_bytes_archived_or_reconstructable_claimed']is False,'exact completed temporary lifecycle based on actual consumers/native, not failed archive gate relaxation or byte-reconstruction promise')
 cp=plan['actual_pool_failure_closure_pins'];host=meta(cp['Host']);raw=meta(cp['Root_tools'])
 first=meta(cp['first_failure']);watch=meta(cp['watchdog'])
 failurepost=meta(cp['post']);failuretools=meta(cp['post_tools'])
 cli=meta(plan['actual_failed_pool_reviewable_CLI_pin'])
 terminal=raw['actual_terminal_return'];need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
  and raw['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1
  and terminal.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'
  and raw['actual_retried']is False and raw['exact_executed_command']==cli['command'],
  'real new pool archive Root1 exact executed CLI preserved, never treated as complete pair success or retried')
 genuine(failuretools,'actual_review_return',cp['post'],'review_pin')
 out=Path(archiveplan['planned_actual_output_root']);targets=plan['exact_target_pins'];completed=plan['ordered_completed_derived_spool_full_pins'];partial=plan['exact_failed_pool_partial_current7_only_pin']
 need(targets==completed+[partial]and len(completed)==15 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in completed)
  and len(targets)==len({p['path']for p in targets})==16 and set(partial)=={'path','size_bytes','identity'}and partial['size_bytes']==67099371
  and partial['path']==str(out/'archives/001_complete_native_original_value_bytes.bin.gz')
  and plan['planned_released_bytes']==plan['target_total_bytes']==367026207,
  'exact15 completed derived spools plus one incomplete gzip fragment; no authoritative native, final55pair, context, archive or result target')
 need(host['schema']=='ACTUAL_CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
  and host['status']=='FAILED_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED'
  and host['failure']=="RuntimeError('own-child stage failed; no retry')"and host['archive_complete']is False
  and host['actual_watchdog']is None and host['actual_child_receipt']is None and host['final_report_resource_check_passed']is True
  and host['binding_pin']==plan['inherited_failed_pool_archive_plan_pin']and host['complete_joint_roots']==roots
  and host['original_caps']==plan['original_caps']and host['original_pool_current7_retained']is True
  and host['historical_SQL_original_retired']is True and len(host['records'])==1
  and host['records'][0]['status']=='FAILED'and host['records'][0]['error']=='own-child stage failed; no retry',
  'original new archive Host failure and NULL watch/receipt retained exactly')
 record=host['records'][0];need(cp['watchdog']['path']==str(out/(record['label']+'.watchdog.json'))
  and watch['command']==record['command']and type(watch['returncode'])is int and watch['returncode']==1
  and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True
  and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512
  and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'genuine per-record standalone child1, not invented embedded Host child result')
 gzip=archiveplan['reused_SQL_member0_gzip_pin'];ep=archiveplan['reused_SQL_member0_entry_pin'];pool=archiveplan['all1_plain_pins'][0]
 need(first['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_FIRST_FAILURE_V1'and first['phase']=='ARCHIVE_1'
  and first['failure']=="RuntimeError('paired gzip payload below64MiB; no compression assumption')"
  and first['completed_entry_pins']==[ep]and first['partial_archive_paths']==[partial['path']]
  and first['original_plain_files_deleted']is False and first['retry_performed']is False
  and not os.path.lexists(out/'archive_entry_001.json')
  and not os.path.lexists(out/'CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_INDEX.json')
  and not os.path.lexists(out/'ACTUAL_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_REPORT.json'),
  'exact new pool gzip64cap failure, only existing old SQL entry reused, no new pool entry/complete index/child success report')
 projection=plan['actual_failure_post_key_projection']
 need(failurepost['schema']==projection['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1'
  and failurepost['status']==projection['status']=='PASS_FAILURE_FACTS_ONLY'and failurepost['failure']is None
  and failurepost['metadata_only']is True and failurepost['actual_Host_report_pin']==cp['Host']
  and failurepost['actual_Root_tools_pin']==cp['Root_tools']and type(failurepost['actual_Root_integer_exit_code'])is int
  and failurepost['actual_Root_integer_exit_code']==1 and failurepost['actual_Host_status']==host['status']
  and failurepost['actual_Host_failure']==host['failure']and failurepost['actual_Host_embedded_watchdog']is None
  and failurepost['actual_Host_child_receipt']is None and failurepost['actual_standalone_watchdog_pin']==cp['watchdog']
  and failurepost['actual_standalone_watchdog']==watch and type(failurepost['actual_recorded_child_integer_exit_codes'])is list
  and failurepost['actual_recorded_child_integer_exit_codes']==[1]
  and all(type(x)is int for x in failurepost['actual_recorded_child_integer_exit_codes'])
  and failurepost['archive_success_or_roundtrip_or_complete_pair_inferred']is False
  and failurepost['failed_gzip_or_partial_payload_body_opened_or_hashed']is False
  and failurepost['execution_binding_pin']==plan['inherited_failed_pool_archive_plan_pin'],
  'genuine independent failurefacts post0, Root1 and explicit typed child1 list; it does not parse FIRST failure or assert restored-byte proof')
 failureRows=failurepost['failed_output_current7_only_three_field_rows']
 need(failureRows==plan['actual_failed_pool_output_current7_only_pins']and all(set(p)=={'path','size_bytes','identity'}for p in failureRows)
  and partial in failureRows and len(failureRows)==8
  and plan['retained_failed_pool_archive_current7_only_pins']==[p for p in failureRows if p!=partial],
  'entire closed failed archive8rows stat-only, only one fragment removed and remaining7 retained with no partial SHA invented')
 for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
 audit,consumedProof=admit_completed_consumers(plan,archiveplan)
 need(plan['retained_current7_pins']==[p for p in archiveplan['all1_plain_pins']+archiveplan['retained_current7_pins']if p not in completed]
  and plan['completed_B2_derived_pool_full_pin']==pool and pool['size_bytes']==150267572
  and plan['retained_complete_SQL_gzip_pin']==gzip and plan['retained_SQL_entry_pin']==ep
  and plan['SQL_with_exact_live_original_pool_recovery_map']==archiveplan['SQL_with_exact_live_original_pool_recovery_map']
  and plan['retained_failed_v1_current7_only_pins']==archiveplan['retained_failed_v1_current7_only_pins']
  and plan['retained_B2_current_epoch_readonly_pins']==archiveplan['retained_B2_current_epoch_readonly_pins'],
  'all canonical native/final55pair/context/comparison/docs/archives/failedhistory preserved; exact completed derived spools are independently admitted temporary targets')
 historical=archiveplan['exact_historical_SQL_and_discarded_partial_target_pins']
 need(plan['prior_exact_historical_SQL_and_partial_target_pins']==historical and historical[0]==archiveplan['historical_SQL_full_pin']
  and set(historical[1])=={'path','size_bytes','identity'},'old exact SQL and old discarded partial stay historical, distinct from this new failed target')
 for p in historical:need(not os.path.lexists(p['path']),'only known retired historical paths absent; no current7/body probe or generic missing skip')
 retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']
 need(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},
  'all exact16 target paths excluded from every retained native/result/metadata/archive/failed7 role; partial stays stat3, completed15 remain distinct fullPF temporary targets')
 need(failed_pool_rows(out)==(failureRows if check_targets_live else plan['retained_failed_pool_archive_current7_only_pins']),'whole failed pool root exact8 before or remaining7 after; no partial body hash')
 need(receipt['exact_target_pins']==targets and receipt['actual_pool_failure_closure_pins']==cp and receipt['actual_failed_pool_output_current7_only_pins']==failureRows and receipt['retained_failed_pool_archive_current7_only_pins']==plan['retained_failed_pool_archive_current7_only_pins']and receipt['completed_B2_derived_pool_full_pin']==pool and receipt['retained_complete_SQL_gzip_pin']==gzip and receipt['retained_SQL_entry_pin']==ep and receipt['completed_derived_spool_full_pins']==completed and receipt['actual_completed_consumer_proof']==consumedProof,'actual receipt consumes exact independent five completed closures/counts/native and same15 completed temporary roles plus failed fragment')
 need(receipt['temporary_completed_derived_spool_lifecycle_only']is True and receipt['all_authoritative_native_and_completed_result_documents_preserved']is True and receipt['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False and receipt['partial_target_body_opened_or_hashed']is False and receipt['new_byte_control_executed_or_required']is False and receipt['complete_pair_archive_success']is False and receipt['historical_original_PFs_not_current_relabelled']is True and receipt['generic_missing_path_skip_authorized']is False,'temporary lifecycle only, no archive success/new byteproof or scientific qualification inferred')
 need(receipt['historical_SQL_with_exact_live_original_pool_recovery_map']==plan['SQL_with_exact_live_original_pool_recovery_map']and receipt['old_live_pool_map_replaced_by_exact_temporary_lifecycle_after_successful_execute']is True and receipt['future_use_requires_new_full_native_extraction_and_independent_admission']is True and receipt['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False and receipt['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False and receipt['completed_derived_spools_retired']is(not check_targets_live)and receipt['original_pool_retired']is(not check_targets_live),'old live-pool map historical after execute; new full native extraction and independent admission required, no identical pool file or oldSQL compatibility promise')
 for k in('retained_current7_pins','retained_failed_v1_current7_only_pins','retained_B2_current_epoch_readonly_pins','retained_archive_metadata_current7_pins'):need(receipt[k]==plan[k],'actual whole retainer tables match exact plan')
 for _ in range(2):
  if check_targets_live:
   for p in completed:current(p)
   current_partial(partial,plan)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact16 genuinely retired paths absent; never restat original targets as current')
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
  for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
 return roots,targets,[gzip],[ep],cp,historical,consumedProof
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('readonly-receipt-pin','readonly-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable once-only readonly post')
 pReceipt=json.loads(a.readonly_receipt_pin);pTools=json.loads(a.readonly_tools_pin);receipt=meta(pReceipt);tools=meta(pTools);actual=tools['actual_readonly_return']
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==tools['original_integer_exit_code']and actual.get('session_id')is None,'genuine observed closed readonly Root integer, no live handle inference')
 need(pReceipt['path']==str(PACKAGE/'READONLY_RECEIPT.json')and receipt['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_RECEIPT_V1'and receipt['mode']=='check','exact actual readonly receipt role/schema/mode')
 ps=receipt['source_pin'];pp=receipt['plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];need(source_limit==8*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and ps['path']==str(PACKAGE/'retire_exact16_completed_B_early14_B2_pool_and_failed_fragment.UNREADY.py'),'same exact Source/PLAN and original Source16MiB bound')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_READONLY_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_readonly_receipt_pin=pReceipt,actual_readonly_tools_pin=pTools,actual_readonly_Root_integer_exit_code=code,actual_readonly_status=receipt['status'],actual_readonly_failure=receipt['failure'],source_pin=ps,plan_pin=pp,actual_recorded_released_pins=receipt['actual_released_pins'],actual_recorded_released_bytes=receipt['actual_released_bytes'],actual_recorded_files_deleted=receipt['files_deleted'],readonly0_or_no_unlink_success_inferred=False)
  save(result,source_limit);return
 genuine(tools,'actual_readonly_return',pReceipt,'receipt_pin')
 need(tools['actual_readonly_permission_mode']=='require_escalated'and receipt['status']=='READONLY_READY_CURRENT_B_COMPLETED_SPOOL_EXACT16_NO_UNLINK'and receipt['failure']is None and receipt['actual_released_pins']==[]and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==0 and receipt['files_deleted']is False and receipt['all_authoritative_native_and_completed_result_documents_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True and 'actual_lsof_owner_check'not in receipt,'genuine readonly0/no target released/no lsof branch and final original resource refresh')
 need(plan['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS and plan['independent_readonly_post0_required_before_execute']is True and plan['actual_completed_consumers_and_native_epoch_closed0']is True and plan['actual_pool_failure_Root1_child1_independent_post0_complete']is True,'actual fully bound B_completed_spool_exact16 plan; original caps and actual prerequisite roles are closed')
 contract=plan['readonly_post_report_contract'];need(contract['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_READONLY_METADATA_POSTVERIFY_V1'and contract['status']=='PASS_CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_READONLY0_NO_UNLINK_METADATA_ONLY','exact readonly metadata post0 contract schema/status, identity/zero release/fresh checks retained separately')
 cli_pin=pin(PACKAGE/'ROOT_READONLY_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(cli['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='check'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and all(cli[k]is None for k in('actual_readonly_receipt_pin','actual_readonly_tools_pin','actual_readonly_post_pin','actual_readonly_post_tools_pin')),'actual exact genuine readonly published CLI, frozen same Source/PLAN/peer roles and NULL execute-only credentials')
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent complete Source-only review0 for same readonly worker/plan')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');need(author_pin==EXPECTED_CORE_AUTHOR_FREEZE,'exact frozen core author metadata PF');author=meta(author_pin);need(author['whole_plan_pin']==pp and ps in author['whole_Source_file_pins'],'exact original author-frozen Source and whole plan table')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 full(ps);full(ps)
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,True)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved actual after-original-class resource scans follow actual before scans; no invented unlink timing')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'readonly evidence cannot mint science/physics/goal qualifications')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original cumulative/free reserve including post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin):full(p)
 result=dict(schema=contract['schema'],status=contract['status'],failure=None,actual_readonly_receipt_pin=pReceipt,actual_readonly_tools_pin=pTools,actual_readonly_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=[],actual_released_bytes=0,resources_after_original_classes_forced_fresh=True,actual_readonly_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,retained_complete_SQL_gzip_pin=archives[0],retained_SQL_entry_pin=entries[0],actual_pool_failure_closure_pins=archive_cp,completed_derived_spool_full_pins=plan['ordered_completed_derived_spool_full_pins'],completed_B2_derived_pool_full_pin=plan['completed_B2_derived_pool_full_pin'],exact_failed_pool_partial_current7_only_pin=plan['exact_failed_pool_partial_current7_only_pin'],target_role_kinds=plan['target_role_kinds'],actual_completed_consumer_proof=archive_post,temporary_completed_derived_spool_lifecycle_only=True,all_authoritative_native_and_completed_result_documents_preserved=True,retired_spool_file_bytes_archived_or_byte_reconstructable_claimed=False,historical_SQL_with_exact_live_original_pool_recovery_map=plan['SQL_with_exact_live_original_pool_recovery_map'],old_live_pool_map_replaced_by_exact_temporary_lifecycle_after_successful_execute=True,future_use_requires_new_full_native_extraction_and_independent_admission=True,new_SQL_or_pool_byte_identity_with_retired_file_claimed=False,old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed=False,partial_target_body_opened_or_hashed=False,new_byte_control_executed_or_required=False,complete_pair_archive_success=False,completed_derived_spools_retired=False,original_pool_retired=False,retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=True,prior_v1_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],all_retained_roles_current7_verified_twice=True,generic_missing_path_skip_authorized=False,historical_deleted_target_PFs_not_claimed_current=True,local_Source_bound_bytes=source_limit,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

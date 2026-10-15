"""UNREADY independent metadata post for an actual complete28 B result JSONL byte archive.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. New compressed outputs are blindly hashed; no original payload read, repeat decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_complete28_JSONL_lossless_archive_source_v2_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '6f70fc4160f3e4ad002f06e82c66db8f2c655bfd5f53bc38e6a95990f9ebbc6e', 'size_bytes': 6493, 'identity': [16777229, 50894494, 33188, 1, 6493, 1792076138918104692, 1792076138918104692]}
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
OUT_CAP=264*2**20;ARCHIVE_CAP=256*2**20;SOURCE_CAP=8*2**20
def true0(p,key,stdout_role,expected):
 v=meta(p);genuine(v,key,expected,stdout_role);return v
def unique(rows):
 out={}
 for p in rows:need(p['path']not in out or out[p['path']]==p,'same path same wholePF');out[p['path']]=p
 return list(out.values())
def current_failed_v1(p,binding):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in binding['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role; no SHA/fullPF claimed')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-v1 file stable current7, no partial body open/hash or generic missing skip')
 return s
def current_failed_pool(p,binding):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in binding['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool7rows stat3, never partial SHA/fullPF or generic missing exception')
 q=Path(p['path']);st=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(st.st_mode)
  and st.st_uid==os.getuid()and st.st_nlink==1 and ids(st)==p['identity']and st.st_size==p['size_bytes'],
  'entire retained failed-pool metadata/runtime row current7 only')
def current_exact16_historical_absence(binding):
 targets=binding['exact16_retired_temporary_target_pins']
 need(type(targets)is list and len(targets)==16 and len({p['path']for p in targets})==16
  and all(set(p)=={'path','sha256','size_bytes','identity'}for p in targets[:15])
  and set(targets[-1])=={'path','size_bytes','identity'}and targets[-1]['size_bytes']==67099371,
  'exact15 completed fullPF temporaries and sole failed partialstat3 history, not generic absent path skip')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(x.is_symlink()for x in Path(p['path']).parents),
   'only precisely proved temporary16 absent, never current-stat/hash retired SQL/pool or partial')
def admit_prior(binding):
 need(binding['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_BINDING_V1'
  and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False
  and binding['Source_admission_ready']is False and binding['original_caps']==CAPS
  and type(binding['actual_current_resource_stage_budget'])is dict,
  'future completed-spool exact16 genuine execute0/post0 and latest full82plus264plusSource8 budget NULL hard reject')
 previouspin=binding['actual_completed_spool_exact16_plan_pin'];previous=meta(previouspin)
 receipt=meta(binding['actual_completed_spool_exact16_receipt_pin']);post=meta(binding['actual_completed_spool_exact16_post_pin'])
 true0(binding['actual_completed_spool_exact16_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_completed_spool_exact16_receipt_pin'])
 true0(binding['actual_completed_spool_exact16_post_tools_pin'],'actual_review_return','review_pin',binding['actual_completed_spool_exact16_post_pin'])
 historical=binding['exact16_retired_temporary_target_pins']
 need(previous['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_PLAN_V1'
  and previous['Source_admission_ready']is True and previous['draft_unready']is False
  and previous['actual_completed_consumers_and_native_epoch_closed0']is True and previous['no_new_output_root']is True
  and previous['exact_target_pins']==historical and previous['target_total_bytes']==367026207
  and previous['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and previous['original_caps']==CAPS,
  'independent new completed-derived temporary lifecycle, never failed archive success gate weakened')
 need(receipt['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_RECEIPT_V1'
  and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_B_COMPLETED_SPOOL_EXACT16_DERIVED_TEMPORARIES_AND_FAILED_FRAGMENT'
  and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==historical
  and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==367026207
  and receipt['files_deleted']is True and receipt['resources_after_original_classes_forced_fresh']is True
  and receipt['temporary_completed_derived_spool_lifecycle_only']is True
  and receipt['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False
  and receipt['future_use_requires_new_full_native_extraction_and_independent_admission']is True
  and receipt['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False
  and receipt['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False
  and receipt['complete_pair_archive_success']is False and receipt['generic_missing_path_skip_authorized']is False,
  'genuine exact16 temporary lifecycle receipt0, native/results retained; old SQL/pool file byte identity not promised')
 contract=binding['actual_completed_spool_exact16_post_contract'];projection=meta(binding['actual_completed_spool_exact16_post_Source_projection_pin'])
 need(projection['schema']==contract['schema']and projection['status']==contract['status'],'same frozen exact16 actualpost Source projection; its NULL future PF fields are never execution evidence')
 need(post['schema']==contract['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_EXECUTION_METADATA_POSTVERIFY_V1'
  and post['status']==contract['status']=='PASS_ACTUAL_B_COMPLETED_DERIVED_SPOOL_EXACT16_TEMPORARIES_RETIRED_NATIVE_AND_RESULTS_PRESERVED_METADATA_ONLY'
  and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_completed_spool_exact16_receipt_pin']
  and post['actual_Root_tools_pin']==binding['actual_completed_spool_exact16_Root_tools_pin']and post['plan_pin']==previouspin
  and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0
  and post['exact_target_pins']==post['actual_released_pins']==historical and post['actual_released_bytes']==367026207
  and post['files_deleted']is True and post['files_deleted_by_post']is False
  and post['resources_after_original_classes_forced_fresh']is True and post['exact_sixteen_targets_absent_verified_twice']is True
  and post['temporary_completed_derived_spool_lifecycle_only']is True
  and post['all_authoritative_native_and_completed_result_documents_preserved']is True
  and post['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False
  and post['complete_pair_archive_success']is False
  and post['future_use_requires_new_full_native_extraction_and_independent_admission']is True
  and post['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False
  and post['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False,
  'genuine independent exact16 actual metadata post0, no readonly or failed post substituted for execution')
 current_exact16_historical_absence(binding)
 audit=meta(previous['actual_completed_spool_role_audit_pin']);e=audit['actual_B_extract_closure'];g=audit['actual_B_aggregate_closure']
 ep=meta(e['post']);gp=meta(g['post'])
 true0(e['Root_tools'],'actual_terminal_return','report_pin',e['Root_report']);true0(e['post_tools'],'actual_review_return','review_pin',e['post'])
 true0(g['Root_tools'],'actual_terminal_return','report_pin',g['Root_report']);true0(g['post_tools'],'actual_review_return','review_pin',g['post'])
 need(ep['schema']==e['post_schema']and ep['status']==e['post_status']and ep['failure']is None
  and ep['actual_Host_report_pin']==e['Root_report']and ep['actual_Root_tools_pin']==e['Root_tools']
  and gp['schema']==g['post_schema']and gp['status']==g['post_status']and gp['failure']is None
  and gp['actual_Host_report_pin']==g['Root_report']and gp['actual_Root_tools_pin']==g['Root_tools'],
  'both original complete B extract and aggregate actual Root0/post0 whole-output PF inventories')
 # Presence is already archived/retired by its separate genuine historical exact1 closure, not a missing-path filter.
 pc=binding['inherited_presence_exact1_closure_pins'];pres=meta(pc['receipt']);ppost=meta(pc['post'])
 true0(pc['Root_tools'],'actual_terminal_return','receipt_pin',pc['receipt']);true0(pc['post_tools'],'actual_review_return','review_pin',pc['post'])
 presence=binding['historical_retired_presence_full_pin']
 need(pres['mode']=='execute'and pres['failure']is None and pres['actual_released_pins']==[presence]
  and pres['actual_released_bytes']==169615994 and pres['files_deleted']is True
  and ppost['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'
  and ppost['status']=='PASS_ACTUAL_CURRENT_BAGG_PRESENCE_EXACT1_RETIRED_COMPLETE_RESULT_BYTES_IN_ARCHIVE_METADATA_ONLY'
  and ppost['failure']is None and ppost['actual_execution_receipt_pin']==pc['receipt']and ppost['actual_Root_tools_pin']==pc['Root_tools']
  and type(ppost['actual_Root_integer_exit_code'])is int and ppost['actual_Root_integer_exit_code']==0
  and ppost['historical_retired_presence_full_pin']==presence and ppost['exact_one_target_absent_verified_twice']is True
  and not os.path.lexists(presence['path']),'known exact169615994 presence already retired with permanent archive; never a new target or generic missing role')
 rows=ep['actual_complete_output_full_EOF_twice_pins']+gp['all_new_output_blind_fullEOF_SHA_current7_twice_pins']
 JSONL=[p for p in rows if p['path'].endswith('.jsonl')]
 need(len(JSONL)==30 and presence in JSONL,'complete recorded inventories include25extract plus5aggregate JSONL with exact historical presence')
 live=[p for p in JSONL if p!=presence];ordered=[p for p in live if p['size_bytes']>0];empty=[p for p in live if p['size_bytes']==0]
 need(len(live)==29 and len(ordered)==28 and sum(p['size_bytes']for p in ordered)==249929878
  and len(empty)==1 and empty[0]['path'].endswith('/all_numeric_mismatches.jsonl')and empty[0]==binding['retained_empty_numeric_mismatch_JSONL_pin']
  and binding['all28_plain_pins']==ordered and binding['original_plain_total_bytes']==249929878
  and all(p in rows and p not in historical for p in live),
  'all28 real nonempty full result JSONL exact original postPF order, no subset, values or compression assumption; empty mismatch remains at original path')
 need(binding['retained_current7_pins']==[p for p in previous['retained_current7_pins']if p not in ordered]
  and binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']
  and binding['retained_failed_pool_archive_current7_only_pins']==previous['retained_failed_pool_archive_current7_only_pins']
  and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins'],
  'all rawnative/final55pair/55contexts/oldgzip-entry-index/docs/comparison detail/failed histories retained and not archived away')
 proofs=[binding[k]for k in('actual_completed_spool_exact16_plan_pin','actual_completed_spool_exact16_receipt_pin','actual_completed_spool_exact16_Root_tools_pin','actual_completed_spool_exact16_post_pin','actual_completed_spool_exact16_post_tools_pin','actual_completed_spool_exact16_post_Source_projection_pin')]+[previous['actual_completed_spool_role_audit_pin']]+[c[k]for c in(e,g)for k in('Root_report','Root_tools','post','post_tools')]+list(pc.values())
 need(binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']
  and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),
  'complete cumulative metadata table plus actual16/consumer/presence proofs, no lost external/cold accounting')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots']
 need(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']and len(prefix)==82
  and binding['complete_joint_roots']==prefix+[str(out)]and len(binding['complete_joint_roots'])==83 and out.parent==ART
  and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))
  and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),
  'entire real82 prefix including all failed roots plus exactly one new owning83 archive root')
 need(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP
  and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP
  and binding['compression_order']=='ORIGINAL_POST_INVENTORY_ORDER_ALL28_NONEMPTY_JSONL'
  and binding['plain_retirement_authorized']is False,'new component264MiB=256gzip+8runtime plusSource8; originals retained, separate future retirement only after independent post0')
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
 result=dict(schema='CURRENT_B_COMPLETE28_JSONL_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=root['original_integer_exit_code'],actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_Host_embedded_watchdog=None if host is None else host['actual_watchdog'],actual_Host_child_receipt=None if host is None else host['actual_child_receipt'],actual_standalone_watchdog_pin=wp,actual_standalone_watchdog=standalone,actual_recorded_child_integer_exit_codes=observed,actual_stage_records=None if host is None else host['records'],absent_child_code_invented=False,archive_success_or_roundtrip_or_complete_pair_inferred=False,failed_output_current7_only_three_field_rows=rows,failed_gzip_or_partial_payload_body_opened_or_hashed=False,execution_binding_pin=pb)
 save(result,source_limit)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+role,required=True)
 args=ap.parse_args();need(args.executor_task_name==EXECUTOR and args.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent exact executor, immutable single metadata execution')
 pRoot=json.loads(args.Root_tools_pin);pHost=json.loads(args.Host_pin);root=meta(pRoot);terminal=root['actual_terminal_return'];host=None if pHost is None else meta(pHost)
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==root['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed original Root integer, no live handle inference')
 full(EXPECTED_CORE_AUTHOR_FREEZE);author=meta(EXPECTED_CORE_AUTHOR_FREEZE);pb=pin(PACKAGE/'PLAN.json')if host is None else host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];limit=b['bounded_total_output_bytes'];source_limit=b['bounded_Source_metadata_bytes'];code=root['original_integer_exit_code']
 need(b['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_BINDING_V1'and b['original_caps']==CAPS and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and limit==OUT_CAP==264*2**20 and b['bounded_archive_payload_bytes']==ARCHIVE_CAP==256*2**20 and b['metadata_runtime_headroom_bytes']==8*2**20 and source_limit==SOURCE_CAP==8*2**20 and roots[-1]==str(out),'frozen local264=256gzip+8metadata/runtime and localSource8, original global caps unchanged')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_complete28_B_JSONL_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1','exact real owning complete28 B JSONL Host report')
 if code!=0:failure_facts(root,pRoot,host,pHost,b,pb,out,source_limit);return
 need(host is not None,'Root0 requires actual emitted Host PF');genuine(root,'actual_terminal_return',pHost,'report_pin')
 need(root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False and host['status']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and host['failure']is None and host['secondary_failures']==[]and host['archive_complete']is True and host['retries']==0 and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False and host['independent_archive_post0_required']is True and host['all28_original_plain_current7_retained']is True,'actual Root0 complete paired archive with original pool live and historical SQL retired')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin);static=meta(author['source_static_evidence_pin'])
 need(author['Source_only_frozen_before_Root_generation']is True and author['whole_Source_file_pins']==sf['complete_source_file_pins']and len(sf['complete_source_file_pins'])==5 and static['original_archive_one_whole2311_SHA']=='db8a6b9fe2234c77f460274fe3d73d5fe43377089ef8341c305b8b20da892495','exact frozen five Source table and original48 archive_one wholebytes proof')
 need(ready['schema']=='CURRENT_B_COMPLETE28_JSONL_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and sf['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_HOST_FREEZE_V1'and hf['source_only']is True and hf['selected_source_freeze_pin']==host['source_freeze_pin']and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and ready['complete_source_file_pins']==sf['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'same actual READY/SF/HF complete Source and exact plan')
 admission=meta(ready['Root_completed_admission_binding_pin']);template=meta(author['whole_NULL_admission_binding_template_pin']);mutable=set(author['Root_final_binding_fields_filled_after_genuine_completed_spool_exact16_lifecycle0']);need(set(admission)==set(template)and all(admission[k]==v for k,v in template.items()if k not in mutable)and all(b[k]==v for k,v in admission.items()),'only author-declared true recovery and budget fields filled; remaining template preserved')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin');need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE'and peer['failure']is None and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'same genuine independent complete Source0 and RootGEN0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(root['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact original Root command string/full24argv/Source identities')
 latest=meta(b['actual_completed_spool_exact16_plan_pin']);need(host['complete_joint_roots']==roots==b['inherited_latest_complete_joint_roots']+[str(out)]and roots[:-1]==latest['complete_joint_roots']and len(roots)==len(set(roots))==83 and len(roots[:-1])==82 and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'full actual82 including failed roots plus only one fresh83, Source already counted')
 need(admit_prior(b)==out,'same frozen B28 admission reproduced only using metadata, no helper or science import')
 originals=b['all28_plain_pins'];need(len(originals)==28 and sum(p['size_bytes']for p in originals)==249929878 and all(p['size_bytes']>0 for p in originals),'all28 nonempty original B result JSONL exact original post inventory, no subset or value decoding')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins)
 need(len(host['records'])==1 and host['records'][0]['status']=='PASS','one original guarded child0 no retry');record=host['records'][0];wp=table[str(out/(record['label']+'.watchdog.json'))];lp=table[str(out/(record['label']+'.log'))];w=meta(wp)
 need(w==host['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and lp['sha256']==record['log_sha256'],'genuine record.label watchdog/log/wall/RSS/liveness child0')
 claim=meta(pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'));command=record['command'];need(len(command)==9 and command[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',str(PACKAGE/'archive_B_complete28_JSONL_serial.UNREADY.py'),'--binding-pin']and json.loads(command[4])==pb and command[5]=='--common-source-pin'and json.loads(command[6])==hf['common_source_pin']and command[7:]==['--expected-parent-pid',str(claim['PID'])],'actual exact sole child command, real parent Root PID and same common/binding')
 log=full(lp);need(lp['size_bytes']<8*2**20,'small child receipt metadata');lines=log.read_text().splitlines();need(len(lines)==1,'one complete child receipt');receipt=json.loads(lines[0]);need(receipt==host['actual_child_receipt'],'same actual Host/child receipt')
 childpin=receipt['report_pin'];child=meta(childpin);need(childpin['path']==str(out/'ACTUAL_COMPLETE28_B_JSONL_LOSSLESS_ARCHIVE_REPORT.json')and child['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'and child['status']=='COMPLETE28_B_JSONL_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None and type(child['completed_count'])is int and child['completed_count']==28 and child['binding_pin']==pb and child['all28_original_plain_current7_retained']is True and child['all_other_current_outputs_native_and_inputs_current7_retained']is True,'actual complete28 JSONL child byteproof report and every other current result retained')
 indexpin=child['index_pin'];index=meta(indexpin)
 need(indexpin['path']==str(out/'CURRENT_COMPLETE28_B_JSONL_LOSSLESS_ARCHIVE_INDEX.json')and index['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and index['status']=='COMPLETE28_B_JSONL_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'and index['binding_pin']==pb and len(index['entries'])==index['ordered_original_plain_count']==28 and index['ordered_original_plain_total_bytes']==child['original_plain_total_bytes']==b['original_plain_total_bytes']==249929878 and index['ordered_original_result_JSONL_pins']==originals and index['compression_ratio_assumed']is False and index['all28_original_plain_retained']is True and index['requires_independent_post0_before_separate_plain_retirement']is True and index['retained_empty_numeric_mismatch_JSONL_pin']==b['retained_empty_numeric_mismatch_JSONL_pin']and index['future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping']is True and index['generic_missing_path_skip_authorized']is False,'complete all28 ordered original-path archive lookup, empty mismatch retained and future exact restore mapping required')
 gzips=[];entrypins=[];proofs=[]
 for ordinal,(row,plain)in enumerate(zip(index['entries'],originals,strict=True)):
  need(type(row['ordinal'])is int and row['ordinal']==ordinal and row['original_plain_full_pin']==plain and row['compression_input_SHA']==row['streamed_decompressed_SHA']==plain['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==plain['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True and row['result_values_decoded']is False and row['scientific_values_decoded']is False and row['actual_B_output_role']=='COMPLETE_B_EXTRACT_OR_SIXPHASE_RESULT_JSONL'and row['filename_field']==''and row['mtime']==0 and row['compresslevel']==6,'every actual Root-recorded full input/decompressed SHA and length equals exact original JSONL PF, no repeated decompression')
  pgz=row['compressed_archive_full_pin'];pe=row['entry_pin']
  need(pgz['path']==str(out/'archives'/(str(ordinal).zfill(3)+'_'+Path(plain['path']).name+'.gz'))and table[pgz['path']]==pgz and pe['path']==str(out/('archive_entry_'+str(ordinal).zfill(3)+'.json'))and table[pe['path']]==pe and meta(pe)=={k:v for k,v in row.items()if k!='entry_pin'},'all28 durable whole entry metadata exactly match index rows; each unique complete gzip blindly fullSHA twice')
  gzips.append(pgz);entrypins.append(pe);proofs.append(dict(original_plain_full_pin=plain,compressed_archive_full_pin=pgz,entry_pin=pe,Root_recorded_streamed_SHA=row['streamed_decompressed_SHA'],Root_recorded_streamed_length=row['streamed_decompressed_length']))
 need(index['ordered_result_JSONL_archive_entry_pins']==entrypins and len({p['path']for p in gzips})==len({p['path']for p in entrypins})==28 and sum(p['size_bytes']for p in gzips)==index['total_gzip_bytes']==child['total_gzip_bytes']<b['bounded_archive_payload_bytes']and ownbytes<limit and {p['path']for p in newpins if Path(p['path']).suffix=='.gz'}=={p['path']for p in gzips},'all and only complete28 gzip below256MiB; whole owning264MiB, no truncation or partial success')
 childclaim=meta(table[str(out/'CHILD_ARCHIVE_CLAIM.json')]);need(childclaim['PID']==w['pid']and childclaim['parent_PID']==claim['PID']and childclaim['retries']==0,'actual own sole child PID and no retry')
 build=meta(b['original_guard_build_plan_pin'])
 for _ in range(2):
  for p in originals:current(p)
  for p in b['retained_current7_pins']:current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  for p in b['retained_B2_current_epoch_readonly_pins']:current(p)
  for p in b['retained_failed_v1_current7_only_pins']:current_failed_v1(p,b)
  for p in b['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,b)
  current_exact16_historical_absence(b);current(b['retained_empty_numeric_mismatch_JSONL_pin'])
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 archive_resources(child['resources_after'],roots,600);before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes'];need(existing+limit+source_limit<2*2**30 and before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'real full81 plus actual external/open-unlinked before launch plus264output/8Source reservation within original caps')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full83 joint/external/open-unlinked/cold/free original limits')
 for item in(host,child,index):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(item[key]is False,'byte archive does not grant scientific/physics/native/retirement qualification')
 for p in[pHost,childpin,indexpin,wp,lp]+gzips+entrypins:need(table[p['path']]==p,'all completed new outputs blindly fullEOF SHA/current7 twice; original JSONL values never read')
 result=dict(schema='RECORDED_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_COMPLETE28_B_JSONL_STREAMED_SHA_LENGTH_ARCHIVE_ROOT0_CHILD0_METADATA_ONLY_ORIGINALS_RETAINED',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,actual_child_report_pin=childpin,actual_archive_index_pin=indexpin,execution_binding_pin=pb,original_ordered_result_JSONL_full_pins=originals,compressed_ordered_result_JSONL_archive_full_pins=gzips,ordered_result_JSONL_entry_pins=entrypins,Root_recorded_all28_original_and_decompressed_SHA_length_match=True,actual_ordered_roundtrip_byte_proofs=proofs,all28_original_current7_verified_twice_only=True,all28_compressed_blind_fullEOF_SHA_current7_verified_twice=True,all28_original_plain_retained=True,completed_count=28,all_retained_current7_verified_twice=True,retained_empty_numeric_mismatch_JSONL_pin=b['retained_empty_numeric_mismatch_JSONL_pin'],retained_empty_numeric_mismatch_current7_verified_twice=True,exact16_retired_temporary_target_pins=b['exact16_retired_temporary_target_pins'],exact16_historical_absence_only_verified_twice=True,actual_completed_spool_exact16_plan_pin=b['actual_completed_spool_exact16_plan_pin'],actual_completed_spool_exact16_receipt_pin=b['actual_completed_spool_exact16_receipt_pin'],actual_completed_spool_exact16_Root_tools_pin=b['actual_completed_spool_exact16_Root_tools_pin'],actual_completed_spool_exact16_post_pin=b['actual_completed_spool_exact16_post_pin'],actual_completed_spool_exact16_post_tools_pin=b['actual_completed_spool_exact16_post_tools_pin'],historical_retired_presence_full_pin=b['historical_retired_presence_full_pin'],retired_presence_exact_independent_closure_preserved=True,inherited_presence_exact1_closure_pins=b['inherited_presence_exact1_closure_pins'],retained_failed_v1_current7_only_pins=b['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=b['retained_failed_pool_archive_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=True,prior_failed_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=b['retained_current7_pins'],bridge9_cold_readonly_current7_pins=b['retained_B2_current_epoch_readonly_pins'],actual_all28_original_JSONL_bytes=sum(p['size_bytes']for p in originals),actual_all28_gzip_bytes=sum(p['size_bytes']for p in gzips),actual_entire_archive_output_bytes=ownbytes,actual_original_runner_record=record,actual_original_watchdog=w,actual_watchdog_pin=wp,actual_child_log_pin=lp,actual_index_entry_metadata=index['entries'],complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,local_Source_bound_bytes=source_limit,local_new_output_bound_bytes=limit,actual_original_Host_resources_before=host['resources_before'],actual_original_Host_resources_after=host['resources_after'],actual_original_Host_resources_after_including_summary=host['resources_after_including_summary_bytes'],actual_original_child_resources_after=child['resources_after'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_CLI_pin=cli_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping=True,generic_missing_path_skip_authorized=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

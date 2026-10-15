"""UNREADY independent metadata post after actual single B2 physical directory exact1 execution.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Source and plan are checked against the real owning receipt and author freeze; future actual parameters remain NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_complete28_JSONL_exact28_plaintext_retirement_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '82967f9bea56bb9ba5c19d26931fb6bfa2a068ee6dd036bb8e162cf32efa2325', 'size_bytes': 3202, 'identity': [16777229, 50895248, 33188, 1, 3202, 1792076980104199364, 1792076980104199364]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(target_payload_body_opened_or_hashed=False,gzip_payload_body_opened_or_hashed=False,worker_or_guard_helpers_imported=False,worker_executed=False,lsof_executed=False,PS_executed=False,native_executed=False,compiler_executed=False,compression_repeated=False,decompression_repeated=False,numerical_executed=False,JSONL_or_array_values_decoded=False,files_deleted_by_post=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
ART=ROOT/'validation/artifacts'
OUT_CAP=264*2**20;ARCHIVE_CAP=256*2**20;SOURCE_CAP=8*2**20
def true0(p,key,stdout_role,expected):
 v=meta(p);genuine(v,key,expected,stdout_role);return v
def current_failed_v1(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q
def current_failed_pool(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],'only exact7 failed-pool metadata/runtime rows stat3, no generic missing or partial SHA role')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==501==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes'],'exact failed-pool current7 without body read/hash')
def exact_historical_absence(plan):
 targets=plan['exact16_retired_temporary_target_pins']
 need(len(targets)==len({p['path']for p in targets})==16 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in targets[:15])and set(targets[-1])=={'path','size_bytes','identity'},'only exact15 completed spools and1 failed partial history')
 for p in targets+[plan['historical_retired_presence_full_pin']]:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only recorded exact temporary16 and presence historicalabsence, no generic skip')
def unique(rows):
 out={}
 for p in rows:
  need(p['path']not in out or out[p['path']]==p,'same path same fullPF');out[p['path']]=p
 return list(out.values())
def current_exact16_historical_absence(binding):
 targets=binding['exact16_retired_temporary_target_pins']
 need(type(targets)is list and len(targets)==16 and len({p['path']for p in targets})==16
  and all(set(p)=={'path','sha256','size_bytes','identity'}for p in targets[:15])
  and set(targets[-1])=={'path','size_bytes','identity'}and targets[-1]['size_bytes']==67099371,
  'exact15 completed fullPF temporaries and sole failed partialstat3 history, not generic absent path skip')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(x.is_symlink()for x in Path(p['path']).parents),
   'only precisely proved temporary16 absent, never current-stat/hash retired SQL/pool or partial')
def admit_archive_metadata(binding):
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
  and ppost['historical_retired_presence_full_pin']==presence and ppost['exact_twenty_eight_targets_absent_verified_twice']is True
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
def complete_archive_metadata(plan,receipt,check_targets_live):
 archiveplan=meta(plan['inherited_complete_archive_plan_pin']);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==plan['actual_archive_complete_prefix']==archiveplan['complete_joint_roots']and len(roots)==83 and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']==CAPS and len(roots)==len(set(roots))and all(not Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'entire real83, no new retirement output root/resource reset')
 cp=plan['actual_archive_closure_pins'];need(all(type(cp[k])is dict for k in('Host','Root_tools','child_report','index','post','post_tools'))and plan['actual_archive_Root0_child0_complete']is True and plan['actual_archive_independent_post0_complete']is True,'future complete28 archive Root0/child0/independentpost0 NULL hard reject')
 host=meta(cp['Host']);raw=meta(cp['Root_tools']);child=meta(cp['child_report']);index=meta(cp['index']);post=meta(cp['post']);posttools=meta(cp['post_tools'])
 genuine(raw,'actual_terminal_return',cp['Host'],'report_pin');genuine(posttools,'actual_review_return',cp['post'],'review_pin')
 need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False
  and host['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
  and host['status']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'
  and host['failure']is None and host['archive_complete']is True and host['final_report_resource_check_passed']is True
  and host['original_guard_class_and_MRO_unchanged']is True and host['original_caps']==plan['original_caps']and host['complete_joint_roots']==roots
  and host['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(host['records'])==1 and host['records'][0]['status']=='PASS'
  and host['actual_child_receipt']['report_pin']==cp['child_report']and host['all28_original_plain_current7_retained']is True,'real complete28 Root0/one originalguard child0 report; never GEN0 or failurepost0 substituted')
 watch=host['actual_watchdog'];need(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'real private OwnRSS child0 original600/512 guard')
 need(child['schema']=='ACTUAL_CURRENT_B_COMPLETE28_JSONL_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'
  and child['status']=='COMPLETE28_B_JSONL_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None
  and type(child['completed_count'])is int and child['completed_count']==28 and child['all28_original_plain_current7_retained']is True
  and child['index_pin']==cp['index']and child['binding_pin']==plan['inherited_complete_archive_plan_pin'],'real complete28 serial child0 byteproof, no partial archive admission')
 sf=meta(host['source_freeze_pin']);commonpin=plan['inherited_archive_common_Source_pin']
 need(sf['execution_binding_pin']==plan['inherited_complete_archive_plan_pin']and commonpin in sf['complete_source_file_pins'],'exact whole reviewed archivecommon Source belongs actual Sourcefreeze')
 need(admit_archive_metadata(archiveplan)==Path(archiveplan['planned_actual_output_root']),'same frozen archive metadata admission without candidate/helper import or original28 current read after retirement')
 targets=plan['exact_target_pins'];rows=index['entries'];empty=plan['retained_empty_numeric_mismatch_JSONL_pin']
 need(targets==archiveplan['all28_plain_pins']and len(targets)==len({p['path']for p in targets})==28 and sum(p['size_bytes']for p in targets)==249929878==plan['planned_released_bytes']==plan['target_total_bytes']
  and all(p['path'].endswith('.jsonl')and p['size_bytes']>0 for p in targets)and empty==archiveplan['retained_empty_numeric_mismatch_JSONL_pin']and empty['size_bytes']==0 and empty not in targets,'exact ordered28 nonempty fullPF249929878; empty0 stays original path')
 need(index['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'
  and index['status']=='COMPLETE28_B_JSONL_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'
  and index['binding_pin']==plan['inherited_complete_archive_plan_pin']and len(rows)==index['ordered_original_plain_count']==28
  and index['ordered_original_plain_total_bytes']==249929878 and index['ordered_original_result_JSONL_pins']==targets
  and index['all28_original_plain_retained']is True and index['future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping']is True
  and index['retained_empty_numeric_mismatch_JSONL_pin']==empty and index['generic_missing_path_skip_authorized']is False,'actual full28 exactlookup; original-preserved creation metadata remains unchanged')
 archivepins=[];entrypins=[]
 for ordinal,(row,original)in enumerate(zip(rows,targets)):
  need(row['ordinal']==ordinal and row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True and row['actual_B_output_role']=='COMPLETE_B_EXTRACT_OR_SIXPHASE_RESULT_JSONL','each original ordinal/compression/decompression fullPF exact')
  entry=meta(row['entry_pin']);need(entry=={k:v for k,v in row.items()if k!='entry_pin'},'whole unchanged entry creation metadata')
  archivepins.append(row['compressed_archive_full_pin']);entrypins.append(row['entry_pin'])
 need(archivepins==plan['retained_ordered_result_JSONL_gzip_pins']and entrypins==plan['retained_ordered_result_JSONL_entry_pins']==index['ordered_result_JSONL_archive_entry_pins'],'permanent complete28 orderedgzip+entry+index exact arrays')
 projection=plan['actual_archive_post_key_projection'];projection_source=meta(plan['actual_archive_post_key_projection_Source_pin'])
 need(projection_source['schema']==projection['schema']and projection_source['status']==projection['status'],'actual frozen archivepost Sourceprojection, never its future NULL result used')
 need(post['schema']==projection['schema']=='RECORDED_CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'
  and post['status']==projection['status']=='PASS_ACTUAL_COMPLETE28_B_JSONL_STREAMED_SHA_LENGTH_ARCHIVE_ROOT0_CHILD0_METADATA_ONLY_ORIGINALS_RETAINED'
  and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==cp['Host']and post['actual_Root_tools_pin']==cp['Root_tools']and post['actual_archive_index_pin']==cp['index']and post['actual_child_report_pin']==cp['child_report']and post['execution_binding_pin']==plan['inherited_complete_archive_plan_pin']
  and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==0
  and post['original_ordered_result_JSONL_full_pins']==targets and post['compressed_ordered_result_JSONL_archive_full_pins']==archivepins and post['ordered_result_JSONL_entry_pins']==entrypins
  and post['Root_recorded_all28_original_and_decompressed_SHA_length_match']is True and post['all28_original_current7_verified_twice_only']is True and post['all28_compressed_blind_fullEOF_SHA_current7_verified_twice']is True and post['completed_count']==28 and post['complete_joint_roots']==roots,'independent genuine archive Root0/child0/post0 exact all28 original/completegzip/entry/index facts')
 need(post['retained_empty_numeric_mismatch_JSONL_pin']==empty and post['retained_empty_numeric_mismatch_current7_verified_twice']is True and post['exact16_retired_temporary_target_pins']==archiveplan['exact16_retired_temporary_target_pins']and post['exact16_historical_absence_only_verified_twice']is True,'empty stays and only exact16 historicalmissing admitted')
 need(plan['retained_current7_pins']==unique(archiveplan['retained_current7_pins']+post['all_new_output_blind_fullEOF_SHA_current7_twice_pins'])and post['retained_all_current7_pins']==archiveplan['retained_current7_pins']
  and plan['retained_B2_current_epoch_readonly_pins']==archiveplan['retained_B2_current_epoch_readonly_pins']==post['bridge9_cold_readonly_current7_pins']
  and plan['retained_failed_v1_current7_only_pins']==archiveplan['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']
  and plan['retained_failed_pool_archive_current7_only_pins']==archiveplan['retained_failed_pool_archive_current7_only_pins']==post['retained_failed_pool_archive_current7_only_pins']
  and plan['exact16_retired_temporary_target_pins']==archiveplan['exact16_retired_temporary_target_pins']and plan['historical_retired_presence_full_pin']==archiveplan['historical_retired_presence_full_pin'],'all native/final55pair/context/comparison detail/docs/archive/failed histories unchanged, no lost roles')
 archiveproofs=list(cp.values())+[commonpin,host['source_freeze_pin'],host['host_freeze_pin'],plan['actual_archive_post_key_projection_Source_pin'],plan['inherited_complete_archive_plan_pin']]
 need(plan['retained_archive_metadata_current7_pins']==unique(archiveproofs+entrypins)and plan['explicit_cumulative_metadata_file_pins']==unique(archiveplan['explicit_cumulative_metadata_file_pins']+archiveproofs+entrypins),'complete exact archiveclosure and inherited cumulative externalmetadata table')
 retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+archivepins+entrypins+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+[empty]
 need(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},'only exact28 plaintext originals, no gzip/entry/index/native/empty/results/docs/cold/history target')
 for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
 for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
 exact_historical_absence(plan)
 need(receipt['exact_target_pins']==targets and receipt['actual_archive_closure_pins']==cp and receipt['compressed_result_full_pins']==archivepins and receipt['retained_ordered_result_JSONL_entry_pins']==entrypins and receipt['original_lookup_index_pin']==cp['index']and receipt['retained_empty_numeric_mismatch_JSONL_pin']==empty and receipt['exact16_retired_temporary_target_pins']==plan['exact16_retired_temporary_target_pins'],'actual exact28 receipt same full archive closure, all28 gzip/entries/index and empty/old16 evidence')
 need(receipt['historical_original_PFs_not_current_relabelled']is True and receipt['archive_lookup_required_for_future_consumer']is True and receipt['future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping']is True and receipt['generic_missing_path_skip_authorized']is False and receipt['exact_all28_complete_result_bytes_preserved_in_archive']is True,'exact original bytes restorable via permanent full28 mapping; old entry-preserved flags are archive creation history')
 for k in('retained_current7_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','retained_B2_current_epoch_readonly_pins','retained_archive_metadata_current7_pins'):need(receipt[k]==plan[k],'actual same exact retainer tables')
 for _ in range(2):
  if check_targets_live:
   for p in targets:current(p)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact28 actual retired JSONL original paths absent; no current7 or SHA replay')
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
  for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
  current(empty);exact_historical_absence(plan)
 return roots,targets,archivepins,entrypins,cp,plan['exact16_retired_temporary_target_pins'],post
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('execution-receipt-pin','Root-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable single execution post')
 pReceipt=json.loads(a.execution_receipt_pin);pTools=json.loads(a.Root_tools_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];receipt=None if pReceipt is None else meta(pReceipt)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed execution Root integer; no live handle inference')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');need(author_pin==EXPECTED_CORE_AUTHOR_FREEZE,'exact frozen core author metadata PF');author=meta(author_pin);pp=author['whole_plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];ps=next(p for p in author['whole_Source_file_pins']if p['path']==str(PACKAGE/'retire_exact28_archived_B_result_JSONL_originals.UNREADY.py'))
 need(source_limit==8*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and plan['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS,'same frozen B_complete28_JSONL_exact28 Source/PLAN and unchanged original caps/localSource8MiB')
 if pReceipt is not None:need(pReceipt['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and receipt['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['source_pin']==ps and receipt['plan_pin']==pp,'actual exact owning execution receipt/schema/mode and Source/plan')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B_COMPLETE28_JSONL_EXACT28_EXECUTION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=code,actual_receipt_status=None if receipt is None else receipt['status'],actual_receipt_failure=None if receipt is None else receipt['failure'],actual_released_pins=None if receipt is None else receipt['actual_released_pins'],actual_released_bytes=None if receipt is None else receipt['actual_released_bytes'],files_deleted=None if receipt is None else receipt['files_deleted'],source_pin=ps,plan_pin=pp,full_B_complete28_JSONL_exact28_retirement_success_inferred=False)
  save(result,source_limit);return
 need(receipt is not None,'actual execution Root0 requires emitted exact receipt PF');genuine(tools,'actual_terminal_return',pReceipt,'receipt_pin')
 need(tools['actual_execution_permission_mode']=='require_escalated'and receipt['status']=='RETIRED_CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['files_deleted']is True and receipt['all_complete_result_bytes_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True,'actual B_complete28_JSONL_exact28 execution Root0/retirement/no lost complete result bytes/fresh original resource closure')
 targets=plan['exact_target_pins'];released=receipt['actual_released_pins'];releasedbytes=receipt['actual_released_bytes'];expectedbytes=sum(p['size_bytes']for p in targets)
 need(receipt['exact_target_pins']==released==targets and len(targets)==len({p['path']for p in targets})==28 and type(releasedbytes)is int and releasedbytes==expectedbytes==plan['target_total_bytes']==plan['planned_released_bytes']and json.loads(terminal['output'].strip().splitlines()[-1])['actual_released_bytes']==releasedbytes,'actual precisely ordered one B2 physical directory fullPF target and exact bytes in receipt/genuine stdout')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only genuinely deleted exact target paths absent; historical fullPF never relabelled current')
 cli_pin=pin(PACKAGE/'ROOT_EXECUTE_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='execute'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'actual exact published execute CLI and same Source/plan/peer identities')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent Source review0 for same exact worker/plan')
 readonly_pin=receipt['actual_readonly_receipt_pin'];readonly_tools_pin=receipt['actual_readonly_tools_pin'];readonly_post_pin=receipt['actual_readonly_post_pin'];readonly_post_tools_pin=receipt['actual_readonly_post_tools_pin']
 need(cli['actual_readonly_receipt_pin']==readonly_pin and cli['actual_readonly_tools_pin']==readonly_tools_pin and cli['actual_readonly_post_pin']==readonly_post_pin and cli['actual_readonly_post_tools_pin']==readonly_post_tools_pin,'actual execute CLI/receipt consumes exact genuine readonly0/post0 PFs')
 readonly=meta(readonly_pin);readonly_tools=meta(readonly_tools_pin);readonly_post=meta(readonly_post_pin);readonly_post_tools=meta(readonly_post_tools_pin);genuine(readonly_tools,'actual_readonly_return',readonly_pin,'receipt_pin');genuine(readonly_post_tools,'actual_review_return',readonly_post_pin,'review_pin')
 need(readonly_pin['path']==str(PACKAGE/'READONLY_RECEIPT.json')and readonly_tools['actual_readonly_permission_mode']=='require_escalated'and readonly['schema']=='CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_RECEIPT_V1'and readonly['mode']=='check'and readonly['status']=='READONLY_READY_CURRENT_B_COMPLETE28_JSONL_EXACT28_ARCHIVED_ORIGINAL'and readonly['failure']is None and readonly['source_pin']==ps and readonly['plan_pin']==pp and readonly['exact_target_pins']==targets and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False and readonly['resources_after_original_classes_forced_fresh']is True,'actual earlier readonly Root0/no-unlink/fresh resource proof remains historical and unmodified')
 contract=plan['readonly_post_report_contract'];need(readonly_post['schema']==contract['schema']and readonly_post['status']==contract['status']and readonly_post['failure']is None and readonly_post['metadata_only']is True and readonly_post['actual_readonly_receipt_pin']==readonly_pin and readonly_post['actual_readonly_tools_pin']==readonly_tools_pin and readonly_post['source_pin']==ps and readonly_post['plan_pin']==pp and readonly_post['exact_target_pins']==targets and readonly_post['actual_released_pins']==[]and readonly_post['actual_released_bytes']==0 and readonly_post['files_deleted']is False and readonly_post['resources_after_original_classes_forced_fresh']is True and type(readonly_post['actual_readonly_Root_integer_exit_code'])is int and readonly_post['actual_readonly_Root_integer_exit_code']==0,'genuine independent readonly metadata post0 exact execution prerequisite, not self-reexecuted')
 lsof=receipt['actual_lsof_owner_check'];need(lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(lsof['returncode'])is int and lsof['returncode']==1 and lsof['stdout']==lsof['stderr']=='','actual saved original B_complete28_JSONL_exact28 lsof owner check1/empty only; lsof not repeated by post')
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,False)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved forced-fresh after original resource scans follow before scans, no fabricated final-unlink timestamp')
 need(receipt['exact_all28_complete_result_bytes_preserved_in_archive']is True and receipt['archive_lookup_required_for_future_consumer']is True,'single complete B2 physical directory byte archive retained and exact archive lookup remains required')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'exact cleanup metadata cannot mint science/physical/goal qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current unchanged original cumulative/free reserve with post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin,readonly_pin,readonly_tools_pin,readonly_post_pin,readonly_post_tools_pin):full(p)
 result=dict(schema='CURRENT_B_COMPLETE28_JSONL_EXACT28_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_B_COMPLETE28_JSONL_EXACT28_ORIGINALS_RETIRED_FULL_BYTES_ARCHIVED_METADATA_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=released,actual_released_bytes=releasedbytes,files_deleted=True,exact_twenty_eight_targets_absent_verified_twice=True,resources_after_original_classes_forced_fresh=True,actual_readonly_receipt_pin=readonly_pin,actual_readonly_tools_pin=readonly_tools_pin,actual_readonly_post_pin=readonly_post_pin,actual_readonly_post_tools_pin=readonly_post_tools_pin,actual_execute_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_saved_lsof_owner_check=lsof,retained_ordered_result_JSONL_gzip_pins=archives,retained_ordered_result_JSONL_entry_pins=entries,original_lookup_index_pin=archive_cp['index'],actual_archive_closure_pins=archive_cp,exact_ordered_result_JSONL_original_full_pins=targets,exact_all28_complete_result_bytes_preserved_in_archive=True,archive_entry_original_preserved_creation_history_only=True,retained_empty_numeric_mismatch_JSONL_pin=plan['retained_empty_numeric_mismatch_JSONL_pin'],retained_empty_numeric_mismatch_current7_verified_twice=True,exact16_retired_temporary_target_pins=plan['exact16_retired_temporary_target_pins'],historical_retired_presence_full_pin=plan['historical_retired_presence_full_pin'],past_exact16_and_presence_historical_absence_only=True,retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=True,prior_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],all_retained_roles_current7_verified_twice=True,future_consumer_must_restore_exact_JSONL_original_bytes_and_path_mapping=True,generic_missing_path_skip_authorized=False,historical_deleted_target_PFs_not_claimed_current=True,local_Source_bound_bytes=source_limit,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

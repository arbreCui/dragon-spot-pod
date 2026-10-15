"""UNREADY independent metadata post after actual SQL and incomplete pool gzip exact1 execution.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Source and plan are checked against the real owning receipt and author freeze; future actual parameters remain NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B2_SQL_partial_archive_exact2_recovery_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': 'aa4eec2a4acb191284a87568bc67a5e0f1a6b505512ae699a03168171d9c3fff', 'size_bytes': 3134, 'identity': [16777229, 50889093, 33188, 1, 3134, 1792072500439181620, 1792072500439181620]}
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
def current_failed_v1(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q
def current_partial(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p==plan['exact_partial_pool_current7_only_pin'],'only declared incomplete pool gzip stat-only target; no fullPF/SHA or generalized exception')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==501==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']==17639368,'literal exact private incomplete partial target current7; never read or hash its body')
 return q
def complete_archive_metadata(plan,receipt,check_targets_live):
 archiveplan=meta(plan['original_pair_execution_binding_pin']);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==archiveplan['complete_joint_roots']and len(roots)==81 and plan['no_new_output_root']is True and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'complete original81 topology; no new recovery data root or resource reset')
 need(plan['original_caps']==archiveplan['original_caps']==CAPS and plan['actual_pair_failure_Root1_child1_post0_complete']is True and plan['actual_SQL_member0_Root0_independent_post0_complete']is True,'actual pair Root1/child1 failurepost0 and independent SQL member0 Root0/post0 are distinct closed prerequisites')
 cp=plan['actual_pair_failure_closure_pins'];host=meta(cp['Host']);raw=meta(cp['Root_tools'])
 first=meta(cp['first_failure']);watch=meta(cp['watchdog'])
 failurepost=meta(cp['post']);failuretools=meta(cp['post_tools'])
 terminal=raw['actual_terminal_return'];need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
  and raw['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1
  and terminal.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'
  and raw['actual_retried']is False,'real failed pair Root1 retained, never pair success or retry')
 genuine(failuretools,'actual_review_return',cp['post'],'review_pin')
 targets=plan['exact_target_pins'];sql=plan['exact_original_SQL_full_pin'];partial=plan['exact_partial_pool_current7_only_pin']
 need(targets==[sql,partial]and len({p['path']for p in targets})==2 and sql==archiveplan['all2_plain_pins'][0]
  and sql['size_bytes']==52441088 and set(partial)=={'path','size_bytes','identity'}and partial['size_bytes']==17639368
  and plan['target_role_kinds']==['RESTORABLE_SQL_FULLPF','INCOMPLETE_POOL_GZIP_CURRENT7_ONLY']
  and plan['planned_released_bytes']==plan['target_total_bytes']==70080456,
  'only SQL fullPF plus incomplete pool-gzip stat-only path, never original pool or complete SQL gzip')
 out=Path(archiveplan['planned_actual_output_root']);ep=plan['retained_SQL_member0_entry_pin'];entry=meta(ep)
 need(host['schema']=='ACTUAL_CURRENT_B2_PAIRED_SQL_POOL_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
  and host['status']=='FAILED_B2_PAIRED_SQL_POOL_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED'and host['failure']is not None
  and host['archive_complete']is False and host['actual_watchdog']is None and host['actual_child_receipt']is None
  and host['binding_pin']==plan['original_pair_execution_binding_pin']and host['complete_joint_roots']==roots
  and len(host['records'])==1 and host['records'][0]['status']=='FAILED'
  and host['records'][0]['error']=='own-child stage failed; no retry','original Host null watch/receipt and failed pair status preserved')
 record=host['records'][0];need(cp['watchdog']['path']==str(out/(record['label']+'.watchdog.json'))
  and watch['command']==record['command']and type(watch['returncode'])is int and watch['returncode']==1
  and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True
  and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512
  and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'real standalone child1 private guard, not a fabricated Host watchdog')
 need(first['phase']=='ARCHIVE_1'and first['failure']=="RuntimeError('paired gzip payload below24MiB; no compression assumption')"
  and first['completed_entry_pins']==[ep]and first['original_plain_files_deleted']is False and first['retry_performed']is False
  and partial['path']==str(out/'archives/001_complete_native_original_value_bytes.bin.gz')
  and not os.path.lexists(out/'archive_entry_001.json'),'precise failed partial pool gzip has no completed entry1, never a complete result')
 fc=plan['failure_post_key_projection'];need(failurepost['schema']==fc['schema']and failurepost['status']==fc['status']
  and failurepost['failure']is None and failurepost['metadata_only']is True
  and failurepost[fc['Host_pin_field']]==cp['Host']and failurepost[fc['Root_tools_pin_field']]==cp['Root_tools']
  and type(failurepost[fc['Root_integer_exit_code_field']])is int and failurepost[fc['Root_integer_exit_code_field']]==1
  and type(failurepost[fc['child_integer_exit_code_field']])is int and failurepost[fc['child_integer_exit_code_field']]==1
  and failurepost[fc['entry0_pin_field']]==ep and failurepost[fc['gzip0_pin_field']]==plan['retained_SQL_member0_gzip_pin']
  and failurepost['pool_partial_current7_only_pin']==partial and failurepost['actual_complete_pair_archive_success']is False,
  'genuine independent failure-facts post0 records completed SQL member0 and incomplete pool partial only')
 mp=plan['actual_SQL_member0_control_closure_pins'];member=meta(mp['Root_report'])
 mraw=meta(mp['Root_tools']);mpost=meta(mp['post']);mtools=meta(mp['post_tools'])
 genuine(mraw,'actual_terminal_return',mp['Root_report'],'report_pin');genuine(mtools,'actual_review_return',mp['post'],'review_pin')
 gzip=plan['retained_SQL_member0_gzip_pin'];need(member['schema']=='ROOT_CURRENT_B2_SQL_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1'
  and member['status']=='PASS_CURRENT_B2_SQL_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY'
  and member['failure']is None and member['original_member0_saved_full_pin']==sql
  and member['complete_member0_gzip_pin']==gzip and member['retained_member0_entry_pin']==ep
  and member['streamed_complete_member0_verified']is True and member['streamed_decompressed_SHA']==sql['sha256']
  and member['streamed_decompressed_length']==52441088 and member['paired_SQL_pool_archive_complete']is False
  and member['partial_pool_gzip_current7_only_pin']==partial and member['partial_pool_gzip_body_opened_or_hashed']is False
  ,'genuine full SQL member0 Root0 stream proof, partial remained stat-only')
 need(member['original_member0_body_opened']is False and member['restored_product_file_written']is False
  and member['children_started']==0 and member['final_report_resource_check_passed']is True
  and member['complete_joint_roots']==roots and member['original_caps']==plan['original_caps'],
  'genuine full independent SQL byte restoration proof and original caps, no paired success')
 mc=plan['member0_post_key_projection'];need(mpost['schema']==mc['schema']and mpost['status']==mc['status']
  and mpost['failure']is None and mpost['metadata_only']is True
  and mpost[mc['Root_report_pin_field']]==mp['Root_report']and mpost[mc['Root_tools_pin_field']]==mp['Root_tools']
  and type(mpost[mc['Root_integer_exit_code_field']])is int and mpost[mc['Root_integer_exit_code_field']]==0
  and mpost[mc['stream_verified_field']]is True,'separate genuine member0 metadata post0 for same Root report/tools')
 need(entry['ordinal']==0 and entry['original_plain_full_pin']==sql and entry['compressed_archive_full_pin']==gzip
  and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==sql['sha256']
  and entry['compression_input_length']==entry['streamed_decompressed_length']==52441088
  and entry['exact_original_plain_bytes_recoverable']is True and entry['original_plain_preserved']is True,
  'completed SQL gzip and entry are permanent recovery proof, never discarded')
 pool=archiveplan['all2_plain_pins'][1];mapping=plan['SQL_with_exact_live_original_pool_recovery_map']
 need(mapping==dict(historical_SQL_full_pin=sql,complete_SQL_gzip_full_pin=gzip,SQL_member0_entry_pin=ep,
  exact_live_original_pool_full_pin=pool,SQL_member0_Root_control_pin=mp['Root_report'],SQL_member0_independent_post_pin=mp['post'],
  restore_SQL_and_use_exact_original_pool_together=True,whole_pair_archive_complete=False,generic_missing_path_skip_authorized=False)
  and pool['size_bytes']==150267572 and pool in plan['retained_current7_pins'],
  'future consumer must restore this exact SQL and pair it only with the still-live exact original pool')
 need(plan['retained_current7_pins']==[p for p in archiveplan['all2_plain_pins']+archiveplan['retained_current7_pins']if p!=sql]
  and plan['retained_failed_v1_current7_only_pins']==archiveplan['retained_failed_v1_current7_only_pins']
  and plan['retained_B2_current_epoch_readonly_pins']==archiveplan['retained_B2_current_epoch_readonly_pins'],
  'original pool/native B2/comparison results/physical permanent mapping and all oldscope remain current')
 archivepins=[gzip];entrypins=[ep]
 retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+archivepins+entrypins+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']
 need(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']},'exact1 excludes all archives/entries/index/reports/meta/all SQL-pool and other current outputs/native/cold readonly inputs')
 need(receipt['exact_target_pins']==targets and receipt['target_role_kinds']==plan['target_role_kinds']and receipt['actual_pair_failure_closure_pins']==cp and receipt['actual_SQL_member0_control_closure_pins']==mp and receipt['retained_SQL_member0_gzip_pin']==gzip and receipt['retained_SQL_member0_entry_pin']==ep and receipt['SQL_with_exact_live_original_pool_recovery_map']==mapping and receipt['partial_target_body_opened_or_hashed']is False and receipt['all_complete_results_preserved']is True and receipt['whole_pair_archive_complete']is False and receipt['historical_original_PFs_not_current_relabelled']is True and receipt['future_consumer_must_restore_SQL_with_exact_original_pool']is True and receipt['generic_missing_path_skip_authorized']is False,'same precise SQL plus partial recovery, permanent exact SQL-gzip/live-pool map; no complete pair archive inferred')
 for k in('retained_current7_pins','retained_failed_v1_current7_only_pins','retained_B2_current_epoch_readonly_pins','retained_archive_metadata_current7_pins'):need(receipt[k]==plan[k],'same full retainer tables in actual receipt and frozen plan')
 for _ in range(2):
  if check_targets_live:current(sql);current_partial(partial,plan)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact SQL/fullPF and partial/stat-only target paths absent; historical roles never called current')
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
 return roots,targets,archivepins,entrypins,cp,mapping,mpost
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('execution-receipt-pin','Root-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable single execution post')
 pReceipt=json.loads(a.execution_receipt_pin);pTools=json.loads(a.Root_tools_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];receipt=None if pReceipt is None else meta(pReceipt)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed execution Root integer; no live handle inference')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');need(author_pin==EXPECTED_CORE_AUTHOR_FREEZE,'exact frozen core author metadata PF');author=meta(author_pin);pp=author['whole_plan_pin'];plan=meta(pp);source_limit=16*2**20;ps=next(p for p in author['whole_Source_file_pins']if p['path']==str(PACKAGE/'recover_exact2_SQL_and_partial_pool_archive.UNREADY.py'))
 need(source_limit==16*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and plan['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS,'same frozen B2_SQL_partial_exact2 Source/PLAN and unchanged original caps/Source16MiB')
 if pReceipt is not None:need(pReceipt['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and receipt['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['source_pin']==ps and receipt['plan_pin']==pp,'actual exact owning execution receipt/schema/mode and Source/plan')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B2_SQL_PARTIAL_EXACT2_EXECUTION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=code,actual_receipt_status=None if receipt is None else receipt['status'],actual_receipt_failure=None if receipt is None else receipt['failure'],actual_released_pins=None if receipt is None else receipt['actual_released_pins'],actual_released_bytes=None if receipt is None else receipt['actual_released_bytes'],files_deleted=None if receipt is None else receipt['files_deleted'],source_pin=ps,plan_pin=pp,full_B2_SQL_partial_exact2_retirement_success_inferred=False)
  save(result,source_limit);return
 need(receipt is not None,'actual execution Root0 requires emitted exact receipt PF');genuine(tools,'actual_terminal_return',pReceipt,'receipt_pin')
 need(tools['actual_execution_permission_mode']=='require_escalated'and receipt['status']=='RECOVERED_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED'and receipt['failure']is None and receipt['files_deleted']is True and receipt['all_complete_result_bytes_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True,'actual B2_SQL_partial_exact2 execution Root0/retirement/no lost complete result bytes/fresh original resource closure')
 targets=plan['exact_target_pins'];released=receipt['actual_released_pins'];releasedbytes=receipt['actual_released_bytes'];expectedbytes=sum(p['size_bytes']for p in targets)
 need(receipt['exact_target_pins']==released==targets and len(targets)==len({p['path']for p in targets})==2 and type(releasedbytes)is int and releasedbytes==expectedbytes==plan['target_total_bytes']==plan['planned_released_bytes']and json.loads(terminal['output'].strip().splitlines()[-1])['actual_released_bytes']==releasedbytes,'actual precisely ordered two exact SQL/partial fullPF target and exact bytes in receipt/genuine stdout')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only genuinely deleted exact target paths absent; historical fullPF never relabelled current')
 cli_pin=pin(PACKAGE/'ROOT_EXECUTE_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='execute'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'actual exact published execute CLI and same Source/plan/peer identities')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent Source review0 for same exact worker/plan')
 readonly_pin=receipt['actual_readonly_receipt_pin'];readonly_tools_pin=receipt['actual_readonly_tools_pin'];readonly_post_pin=receipt['actual_readonly_post_pin'];readonly_post_tools_pin=receipt['actual_readonly_post_tools_pin']
 need(cli['actual_readonly_receipt_pin']==readonly_pin and cli['actual_readonly_tools_pin']==readonly_tools_pin and cli['actual_readonly_post_pin']==readonly_post_pin and cli['actual_readonly_post_tools_pin']==readonly_post_tools_pin,'actual execute CLI/receipt consumes exact genuine readonly0/post0 PFs')
 readonly=meta(readonly_pin);readonly_tools=meta(readonly_tools_pin);readonly_post=meta(readonly_post_pin);readonly_post_tools=meta(readonly_post_tools_pin);genuine(readonly_tools,'actual_readonly_return',readonly_pin,'receipt_pin');genuine(readonly_post_tools,'actual_review_return',readonly_post_pin,'review_pin')
 need(readonly_pin['path']==str(PACKAGE/'READONLY_RECEIPT.json')and readonly_tools['actual_readonly_permission_mode']=='require_escalated'and readonly['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_RECEIPT_V1'and readonly['mode']=='check'and readonly['status']=='READONLY_READY_CURRENT_B2_SQL_PARTIAL_EXACT2_ARCHIVED_ORIGINAL'and readonly['failure']is None and readonly['source_pin']==ps and readonly['plan_pin']==pp and readonly['exact_target_pins']==targets and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False and readonly['resources_after_original_classes_forced_fresh']is True,'actual earlier readonly Root0/no-unlink/fresh resource proof remains historical and unmodified')
 contract=plan['readonly_post_report_contract'];need(readonly_post['schema']==contract['schema']and readonly_post['status']==contract['status']and readonly_post['failure']is None and readonly_post['metadata_only']is True and readonly_post['actual_readonly_receipt_pin']==readonly_pin and readonly_post['actual_readonly_tools_pin']==readonly_tools_pin and readonly_post['source_pin']==ps and readonly_post['plan_pin']==pp and readonly_post['exact_target_pins']==targets and readonly_post['actual_released_pins']==[]and readonly_post['actual_released_bytes']==0 and readonly_post['files_deleted']is False and readonly_post['resources_after_original_classes_forced_fresh']is True and type(readonly_post['actual_readonly_Root_integer_exit_code'])is int and readonly_post['actual_readonly_Root_integer_exit_code']==0,'genuine independent readonly metadata post0 exact execution prerequisite, not self-reexecuted')
 lsof=receipt['actual_lsof_owner_check'];need(lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(lsof['returncode'])is int and lsof['returncode']==1 and lsof['stdout']==lsof['stderr']=='','actual saved original B2_SQL_partial_exact2 lsof owner check1/empty only; lsof not repeated by post')
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,False)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved forced-fresh after original resource scans follow before scans, no fabricated final-unlink timestamp')
 need(receipt['all_complete_results_preserved']is True and receipt['whole_pair_archive_complete']is False and receipt['future_consumer_must_restore_SQL_with_exact_original_pool']is True,'complete SQL gzip and exact live original pool retained; whole pair archive remains failed')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'exact cleanup metadata cannot mint science/physical/goal qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current unchanged original cumulative/free reserve with post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin,readonly_pin,readonly_tools_pin,readonly_post_pin,readonly_post_tools_pin):full(p)
 result=dict(schema='CURRENT_B2_SQL_PARTIAL_EXACT2_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED_METADATA_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=released,actual_released_bytes=releasedbytes,files_deleted=True,exact_two_targets_absent_verified_twice=True,resources_after_original_classes_forced_fresh=True,actual_readonly_receipt_pin=readonly_pin,actual_readonly_tools_pin=readonly_tools_pin,actual_readonly_post_pin=readonly_post_pin,actual_readonly_post_tools_pin=readonly_post_tools_pin,actual_execute_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_saved_lsof_owner_check=lsof,retained_SQL_member0_gzip_pin=archives[0],retained_SQL_member0_entry_pin=entries[0],actual_pair_failure_closure_pins=archive_cp,actual_SQL_member0_control_closure_pins=plan['actual_SQL_member0_control_closure_pins'],SQL_with_exact_live_original_pool_recovery_map=historical,exact_original_SQL_full_pin=plan['exact_original_SQL_full_pin'],exact_partial_pool_current7_only_pin=plan['exact_partial_pool_current7_only_pin'],target_role_kinds=plan['target_role_kinds'],partial_target_body_opened_or_hashed=False,whole_pair_archive_complete=False,all_complete_results_preserved=True,retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=True,prior_v1_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],all_retained_roles_current7_verified_twice=True,future_consumer_must_restore_SQL_with_exact_original_pool=True,generic_missing_path_skip_authorized=False,historical_deleted_target_PFs_not_claimed_current=True,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

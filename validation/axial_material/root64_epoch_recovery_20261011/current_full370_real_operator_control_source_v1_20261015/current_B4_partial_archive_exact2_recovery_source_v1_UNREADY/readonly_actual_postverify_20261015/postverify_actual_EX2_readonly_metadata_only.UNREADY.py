"""UNREADY independent metadata post for an actual EX2 readonly check.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
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
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('readonly-receipt-pin','readonly-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable once-only readonly post')
 pReceipt=json.loads(a.readonly_receipt_pin);pTools=json.loads(a.readonly_tools_pin);receipt=meta(pReceipt);tools=meta(pTools);actual=tools['actual_readonly_return']
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==tools['original_integer_exit_code']and actual.get('session_id')is None,'genuine observed closed readonly Root integer, no live handle inference')
 need(pReceipt['path']==str(PACKAGE/'READONLY_RECEIPT.json')and receipt['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1'and receipt['mode']=='check','exact actual readonly receipt role/schema/mode')
 ps=receipt['source_pin'];pp=receipt['plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];need(source_limit==16*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and ps['path']==str(PACKAGE/'recover_exact2_B4_partial_archive_paths.UNREADY.py'),'same exact Source/PLAN and original Source16MiB bound')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B4_EXACT2_READONLY_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_readonly_receipt_pin=pReceipt,actual_readonly_tools_pin=pTools,actual_readonly_Root_integer_exit_code=code,actual_readonly_status=receipt['status'],actual_readonly_failure=receipt['failure'],source_pin=ps,plan_pin=pp,actual_recorded_released_pins=receipt['actual_released_pins'],actual_recorded_released_bytes=receipt['actual_released_bytes'],actual_recorded_files_deleted=receipt['files_deleted'],readonly0_or_no_unlink_success_inferred=False)
  save(result,source_limit);return
 genuine(tools,'actual_readonly_return',pReceipt,'receipt_pin')
 need(tools['actual_readonly_permission_mode']=='require_escalated'and receipt['status']=='READONLY_READY_CURRENT_B4_EXACT2_RECOVERY_PATHS'and receipt['failure']is None and receipt['actual_released_pins']==[]and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==0 and receipt['files_deleted']is False and receipt['all_complete_result_bytes_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True and 'actual_lsof_owner_check'not in receipt,'genuine readonly0/no target released/no lsof branch and final original resource refresh')
 need(plan['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS and plan['independent_readonly_post0_required_before_execute']is True and plan['actual_failed_archive_facts_post0_complete']is True and plan['actual_single_member_Root0_stream_and_metadata_peer0_complete']is True,'actual fully bound exact2 plan; original caps and actual prerequisite roles are closed')
 contract=plan['readonly_post_report_contract'];need(contract['schema']=='CURRENT_B4_EXACT2_READONLY_METADATA_POSTVERIFY_V1'and contract['status']=='PASS_CURRENT_B4_EXACT2_READONLY0_NO_UNLINK_METADATA_ONLY'and contract['required_identity_fields']==['actual_readonly_receipt_pin','actual_readonly_tools_pin','source_pin','plan_pin','exact_target_pins']and contract['required_empty_released_pins']==[]and contract['required_actual_released_bytes']==0 and contract['required_files_deleted']is False and contract['required_fresh_original_resources']is True and contract['required_genuine_readonly_Root_integer_exit_code']==0,'exact actual execute-gate readonly post report contract, no predicted future PASS')
 cli_pin=pin(PACKAGE/'ROOT_READONLY_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(cli['schema']=='CURRENT_B4_EXACT2_RECOVERY_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='check'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and all(cli[k]is None for k in('actual_readonly_receipt_pin','actual_readonly_tools_pin','actual_readonly_post_pin','actual_readonly_post_tools_pin')),'actual exact genuine readonly published CLI, frozen same Source/PLAN/peer roles and NULL execute-only credentials')
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent complete Source-only review0 for same readonly worker/plan')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');author=meta(author_pin);need(author['whole_plan_pin']==pp and ps in author['whole_Source_file_pins'],'exact original author-frozen Source and whole plan table')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 full(ps);full(ps)
 inherited=meta(plan['inherited_complete_archive_plan_pin']);roots=plan['complete_joint_roots'];need(roots==receipt['complete_joint_roots']==plan['actual_archive_complete_prefix']==inherited['complete_joint_roots']and plan['no_new_output_root']is True and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(root))for root in roots),'entire exact current failed-archive prefix retained, no count substitution/reset/new cleanup root')
 targets=plan['exact_target_pins'];need(receipt['exact_target_pins']==targets and len(targets)==len({p['path']for p in targets})==plan['target_count']==2 and sum(p['size_bytes']for p in targets)==plan['target_total_bytes']==plan['planned_released_bytes']and targets[0]==inherited['all4_product_pins'][0]and targets[1]['path']==str(Path(inherited['planned_actual_output_root'])/'archives/001_u.asc.gz'),'same exact two target fullPFs/count/bytes, no broader cleanup or original four-product success')
 need(receipt['compressed_result_full_pins']==[plan['retained_member0_gzip_pin']]and receipt['retained_member0_entry_pin']==plan['retained_member0_entry_pin']and receipt['original_member0_full_pin']==targets[0]and receipt['historical_original_PFs_not_current_relabelled']is True and receipt['future_full4_archive_index_still_required']is True and receipt['archive_lookup_required_for_future_consumer']is True,'completed member0 bytes retained with explicit historical path/lookup role, whole4 still pending')
 need(receipt['actual_failed_archive_closure_pins']==plan['actual_failed_archive_closure_pins']and receipt['actual_single_member_verification_closure_pins']==plan['actual_single_member_verification_closure_pins']and receipt['actual_failure_supplemental_post_pin']==plan['actual_failure_supplemental_post_pin']and receipt['actual_failure_supplemental_post_tools_pin']==plan['actual_failure_supplemental_post_tools_pin'],'actual readonly uses same failed-archive facts/member0 Root0+post0 metadata closure')
 build=meta(plan['original_guard_build_plan_pin']);retained=plan['retained_other3_original_product_pins']+plan['retained_native_current7_pins']+plan['original_B_native_and_readonly_input_current7_pins']+plan['retained_archive_metadata_current7_pins']+[plan['retained_member0_gzip_pin'],plan['retained_member0_entry_pin']]
 need(len(plan['retained_other3_original_product_pins'])==3 and len(plan['retained_native_current7_pins'])==79 and len(plan['original_B_native_and_readonly_input_current7_pins'])==11 and not{p['path']for p in targets}&{p['path']for p in retained},'all exact retained result/other three original/context/eight tree/SQL-pool/input roles excluded from targets')
 need(receipt['retained_other3_original_product_pins']==plan['retained_other3_original_product_pins']and receipt['retained_native_current7_pins']==plan['retained_native_current7_pins']and receipt['original_B_native_and_readonly_input_current7_pins']==plan['original_B_native_and_readonly_input_current7_pins']and receipt['retained_archive_metadata_current7_pins']==plan['retained_archive_metadata_current7_pins'],'same exact full retention lists preserved in genuine readonly receipt')
 for _ in range(2):
  for p in targets:current(p)
  for p in retained:current_role(p,build)
  for p in plan['explicit_cumulative_metadata_file_pins']:current_role(p,build)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved actual after-original-class resource scans follow actual before scans; no invented unlink timing')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'readonly evidence cannot mint science/physics/goal qualifications')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original cumulative/free reserve including post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin):full(p)
 result=dict(schema=contract['schema'],status=contract['status'],failure=None,metadata_only=True,actual_readonly_receipt_pin=pReceipt,actual_readonly_tools_pin=pTools,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=[],actual_released_bytes=0,resources_after_original_classes_forced_fresh=True,actual_readonly_Root_integer_exit_code=0,actual_readonly_mode='check',actual_readonly_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],complete_joint_roots=roots,no_new_output_root=True,exact_targets_current7_verified_twice_only=True,all_retained_result_input_context_tree_and_metadata_roles_current7_verified_twice=True,all4_archive_failure_not_promoted_to_success=True,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

"""UNREADY independent metadata post for the actual Root-only B4 member000 byte control.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. Original products and gzip files get current7 only; no repeated decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B4_member0_independent_restore_byte_control_source_v2_UNREADY/AUTHOR_SOURCE_ONLY_FREEZE.json', 'sha256': '04e03f4a8e20fc032043722f6db3632b922b765316310b3ada2cd3a47e5930c3', 'size_bytes': 2944, 'identity': [16777229, 50873901, 33188, 1, 2944, 1792061086713867998, 1792061086713867998]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(compiler_executed=False,native_executed=False,children_started_by_post=False,worker_or_guard_helpers_imported=False,original_plain_payload_body_opened=False,original_plain_payload_SHA_recomputed=False,gzip_payload_body_opened_by_post=False,compression_repeated=False,decompression_repeated=False,restored_product_file_written=False,scientific_values_decoded=False,files_deleted=False,retirement_authorized=False,all4_archive_complete=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
def member0_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<600 and v['complete_joint_root_count']==len(roots)and v['non_scalar_resource_inventories_omitted']is True,'actual original Root-only SELF512/stage600 and scalar snapshots for entire bound root topology')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual saved original cumulative/history/cold/metadata/free caps')
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
 for n in('Root-tools-pin','report-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'separate independent executor and immutable once-only metadata post')
 pRoot=json.loads(a.Root_tools_pin);pReport=json.loads(a.report_pin);raw=meta(pRoot);report=None if pReport is None else meta(pReport);terminal=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False,'genuine closed Root integer/no retry, no mid-run inference')
 core=meta(EXPECTED_CORE_AUTHOR_FREEZE);bpin=core['bound_actual_metadata_pin'];b=meta(bpin);sourcepin=core['algorithm_Source_pin'];full(sourcepin);full(sourcepin);cli=meta(core['reviewable_CLI_pin']);archive_binding=meta(b['original_B4_execution_binding_pin']);roots=archive_binding['complete_joint_roots'];source_limit=b['new_Source_metadata_hard_bound_bytes']
 need(core['schema']=='B4_MEMBER0_ROOT_ONLY_VERIFIER_V2_SOURCE_AUTHOR_FREEZE_V1'and core['Source_only_frozen']is True and core['actual_supplement_schema_and_pins_audited']is True and core['original_limited_post_child_codes_empty_preserved']is True and b['schema']=='ROOT_CURRENT_B4_MEMBER0_RESTORATION_BYTE_CONTROL_BINDING_V1'and b['actual_preconditions_closed']is True and b['actual_failed_archive_and_post_roles_audited']is True and b['only_member0_restore_bytes_control']is True and b['all4_archive_completed']is False and b['original_m_xsm_body_must_not_be_opened']is True and b['Root_stage_seconds']==600 and source_limit==16*2**20 and b['new_owning_ledger_root_created']is False and b['complete_joint_roots']==roots and b['original_caps']==CAPS,'same exact v2 author Source/binding and Root-only member0 scope, no new ledger root or all4 success')
 if pReport is not None:need(pReport['path']==str(PACKAGE/'ROOT_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_REPORT.json')and report['schema']=='ROOT_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1','actual owning Root member0 report role')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B4_MEMBER0_ROOT_CONTROL_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_member0_Root_report_pin=pReport,actual_Root_integer_exit_code=code,actual_report_status=None if report is None else report['status'],actual_report_failure=None if report is None else report['failure'],Source_pin=sourcepin,binding_pin=bpin,no_child_code_inferred=True,member0_complete_or_all4_success_inferred=False)
  save(result,source_limit);return
 need(report is not None,'Root0 requires actual emitted member0 report PF');genuine(raw,'actual_terminal_return',pReport,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(stdout['member0_only']is True and stdout['all4_archive_complete']is False and stdout['files_deleted']is False,'actual Root stdout limited to member0 byte control')
 need(cli['schema']=='ROOT_ONLY_B4_MEMBER0_RESTORATION_BYTE_CONTROL_REVIEWABLE_CLI_V2'and cli['Source_pin']==sourcepin and cli['binding_pin']==bpin and cli['Root_only_once']is True and cli['children_started']==0 and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and raw['actual_execution_permission_mode']=='require_escalated'and shlex.split(raw['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'exact published v2 Root-only Source/binding command and original permission')
 need(report['status']=='PASS_CURRENT_B4_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY'and report['failure']is None and report['binding_pin']==bpin and report['Source_pin']==sourcepin and report['frozen_original_B4_common_Source_pin']==b['frozen_B4_common_Source_pin']and report['original_B4_execution_binding_pin']==b['original_B4_execution_binding_pin']and report['actual_failed_archive_closure_pins']==b['actual_failed_archive_closure_pins']and report['final_report_resource_check_passed']is True,'genuine actual member0 Root0 byte restoration closure and exact frozen metadata identities')
 full(report['frozen_original_B4_common_Source_pin']);full(report['frozen_original_B4_common_Source_pin'])
 original=report['original_member0_saved_full_pin'];pgz=report['complete_member0_gzip_pin'];entrypin=report['retained_member0_entry_pin'];entry=meta(entrypin)
 need(original==b['original_member0_saved_full_pin']==archive_binding['all4_product_pins'][0]==entry['original_plain_full_pin']and pgz==b['complete_member0_gzip_pin']==entry['compressed_archive_full_pin']and entrypin==b['retained_member0_entry_pin']and Path(original['path']).name=='m.xsm'and Path(pgz['path']).name=='000_m.xsm.gz'and entry['ordinal']==0 and entry['actual_B_capture_product_name']=='m.xsm','only exact originally completed member000 and complete gzip role')
 expected_compressed=dict(sha256=pgz['sha256'],size_bytes=pgz['size_bytes']);need(report['gzip_blind_SHA_length_before']==report['gzip_blind_SHA_length_after']==expected_compressed and type(report['streamed_decompressed_length'])is int and report['streamed_decompressed_length']==original['size_bytes']==entry['compression_input_length']==entry['streamed_decompressed_length']and report['streamed_decompressed_SHA']==original['sha256']==entry['compression_input_SHA']==entry['streamed_decompressed_SHA']and report['streamed_complete_member0_verified']is True,'Root actually streamed complete gzip before/after SHA and decompressed exact original byte SHA/length; post reads recorded metadata only')
 need(report['all4_original_products_current7_retained']is True and report['original_member0_body_opened']is False and report['original_member0_format_or_numeric_values_decoded']is False and report['restored_product_file_written']is False and type(report['children_started'])is int and report['children_started']==0 and report['original_private_guard_Source_or_class_modified']is False and report['new_owning_ledger_root_created']is False and report['new_Source_metadata_hard_bound_bytes']==source_limit,'actual Root-only stream emitted no restored file/child and read no original body/numeric format')
 cp=b['actual_failed_archive_closure_pins'];prior=meta(cp['post']);prior_tools=meta(cp['post_tools']);failed=meta(cp['Host']);failed_tools=meta(cp['Root_tools']);supplement=meta(cp['supplement']);supplement_tools=meta(cp['supplement_tools']);watch=meta(cp['watchdog']);first=meta(cp['first_failure'])
 genuine(prior_tools,'actual_review_return',cp['post'],'review_pin');genuine(supplement_tools,'actual_review_return',cp['supplement'],'review_pin')
 need(failed_tools['observed_closed']is True and type(failed_tools['original_integer_exit_code'])is int and failed_tools['original_integer_exit_code']==1 and type(failed_tools['actual_terminal_return']['exit_code'])is int and failed_tools['actual_terminal_return']['exit_code']==1 and failed_tools['actual_terminal_return'].get('session_id')is None and failed['status']=='FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED'and failed['archive_complete']is False and failed['actual_watchdog']is None and failed['actual_child_receipt']is None and prior['actual_recorded_child_integer_exit_codes']==[]and report['original_limited_failure_post_recorded_child_codes']==[]and report['original_failed_Root_integer_exit_code']==1 and type(report['original_failed_Root_integer_exit_code'])is int and report['original_failed_child_integer_exit_code']==1 and type(report['original_failed_child_integer_exit_code'])is int and report['original_failed_archive_still_failed']is True,'original whole4 Root1/Host NULLwatch/old post0 empty code list preserved, no failed-run promotion')
 need(supplement['schema']=='SUPPLEMENTAL_B4_ACTUAL_FAILURE_CHILD1_MEMBER0_METADATA_FACTS_V1'and supplement['status']=='PASS_SUPPLEMENTAL_B4_FAILURE_CHILD1_MEMBER0_RECORDED_FACTS_METADATA_ONLY'and supplement['failure']is None and supplement['original_prior_post_recorded_child_integer_exit_codes']==[]and supplement['supplemental_actual_recorded_child_integer_exit_codes']==[1]and all(type(x)is int for x in supplement['supplemental_actual_recorded_child_integer_exit_codes'])and supplement['standalone_watchdog_pin']==cp['watchdog']and supplement['uniquely_completed_entry000_pin']==entrypin and supplement['current_complete_member000_gzip_blind_fullEOF_twice_pin']==pgz and supplement['recorded_complete_member000']['original_plain_full_pin']==original and supplement['future_Root_independent_single_member_stream_control_pin']is None and supplement['archive_all4_complete']is False and type(watch['returncode'])is int and watch['returncode']==1 and first['phase']=='ARCHIVE_1'and first['completed_entry_pins']==[entrypin],'distinct genuine supplemental child1 metadata/unique completed entry0 retained; its historical pending control field remains NULL')
 need(report['complete_joint_roots']==roots and any(PACKAGE.is_relative_to(Path(root))for root in roots)and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and report['original_caps']==archive_binding['original_caps']==CAPS,'entire original existing failed-archive prefix retained without adding/resetting a ledger root')
 build=meta(archive_binding['original_guard_build_plan_pin']);oldpins=archive_binding['all4_product_pins']+archive_binding['retained_native_current7_pins']+archive_binding['original_B_native_and_readonly_input_current7_pins']
 need(len(archive_binding['all4_product_pins'])==4 and len(archive_binding['retained_native_current7_pins'])==79 and len(archive_binding['original_B_native_and_readonly_input_current7_pins'])==11,'actual unchanged all4 products/79 native-context-pairs/11 inputs retained')
 for _ in range(2):
  for p in oldpins+[pgz]:current(p)
  for p in archive_binding['explicit_cumulative_metadata_file_pins']:current_role(p,build)
 need(type(report['Root_SELF_peak_bytes'])is int and report['Root_SELF_peak_bytes']<512*2**20 and 0<report['Root_elapsed_seconds']<600 and report['new_Source_metadata_hard_bound_bytes']==source_limit,'actual Root-only SELF512/stage600/Source16 preserved')
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):member0_resource_facts(report[key],roots)
 need(len(report['original_resource_scalar_snapshots'])>0,'actual resource snapshot series retained')
 for snapshot in report['original_resource_scalar_snapshots']:member0_resource_facts(snapshot,roots)
 for key in('all4_archive_complete','files_deleted','retirement_authorized','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(report[key]is False,'member0 byte control cannot mint whole4/archive retirement/physics/goal qualifications')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in archive_binding['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original full cumulative/free reserve including new Source metadata and own open-unlinked')
 for p in [pRoot,pReport,bpin,sourcepin,core['reviewable_CLI_pin'],EXPECTED_CORE_AUTHOR_FREEZE,entrypin,*cp.values()]:full(p)
 result=dict(schema='RECORDED_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_ROOT_MEMBER0_STREAMED_ORIGINAL_SHA_LENGTH_CLOSED0_METADATA_ONLY_ALL4_REMAINS_FAILED',failure=None,actual_Root_tools_pin=pRoot,actual_member0_Root_report_pin=pReport,actual_Root_integer_exit_code=0,actual_member0_children_started=0,actual_child_integer_exit_code=None,no_child0_or_child1_invented_for_Root_only_control=True,binding_pin=bpin,algorithm_Source_pin=sourcepin,core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_reviewable_CLI_pin=core['reviewable_CLI_pin'],frozen_original_B4_common_Source_pin=b['frozen_B4_common_Source_pin'],original_B4_execution_binding_pin=b['original_B4_execution_binding_pin'],retained_member0_entry_pin=entrypin,original_member0_saved_full_pin=original,complete_member0_gzip_pin=pgz,actual_gzip_blind_SHA_length_before=report['gzip_blind_SHA_length_before'],actual_gzip_blind_SHA_length_after=report['gzip_blind_SHA_length_after'],actual_streamed_decompressed_SHA=report['streamed_decompressed_SHA'],actual_streamed_decompressed_length=report['streamed_decompressed_length'],Root_actual_complete_member0_stream_verified=True,independent_stream_or_original_body_recomparison_by_post=False,actual_failed_archive_closure_pins=cp,original_failed_Root_integer_exit_code=1,original_failed_child_integer_exit_code=1,original_prior_failure_post_integer_exit_code=0,original_limited_failure_post_recorded_child_codes=[],supplemental_watchdog_child_codes=[1],all4_original_products_current7_retained=True,all79_context_snapshot_SQL_pool_current7_retained=True,all11_originalB_inputs_current7_retained=True,member0_gzip_current7_only_by_post=True,complete_joint_roots=roots,new_owning_ledger_root_created=False,original_caps=CAPS,actual_Root_SELF_peak_bytes=report['Root_SELF_peak_bytes'],actual_Root_elapsed_seconds=report['Root_elapsed_seconds'],actual_original_scalar_resources_before=report['resources_before'],actual_original_scalar_resources_after=report['resources_after'],actual_original_scalar_resources_after_including_summary=report['resources_after_including_summary_bytes'],actual_original_resource_scalar_snapshots=report['original_resource_scalar_snapshots'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

"""UNREADY independent metadata post for actual B4 v2 complete product byte archives, one reused member and three new members.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. New compressed outputs are blindly hashed; no original payload read, repeat decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B4_complete_products_lossless_archive_source_v2_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': 'fa605cbbe239a766bc3e10beae2cfa380ff90b2274900ac9a57cb0decb89b819', 'size_bytes': 7654, 'identity': [16777229, 50875010, 33188, 1, 7654, 1792061995690988217, 1792061995690988217]}
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
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B4 v2 output')
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
def closed(v,key,code,p=None,field=None):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine exact original typed closed terminal code')
 if p is not None:need(json.loads(t['output'].strip().splitlines()[-1])[field]==p,'same genuine output metadata PF')
def previous_closure(b):
 need(b['separate_member0_stream0_peer0_and_exact2_cleanup0_post0_bound']is True and b['actual_exact2_cleanup_Root0_bound']is True and b['actual_exact2_cleanup_post0_bound']is True and b['reused_member0_entry_original_plain_preserved_is_creation_time_history']is True and b['all4_original_products_retained']is False and b['old_capture_all4_products_retained_before_exact2_is_historical_only']is True,'actual pre-existing member0 and exact2 gates; one retired original never relabelled live')
 cp=b['actual_exact2_cleanup_closure_pins'];ep=meta(cp['plan']);execution=meta(cp['execution_receipt']);et=meta(cp['Root_tools']);post=meta(cp['post']);posttools=meta(cp['post_tools']);roles=b['actual_exact2_cleanup_post_projection']
 genuine(et,'actual_terminal_return',cp['execution_receipt'],'receipt_pin');genuine(posttools,'actual_review_return',cp['post'],'review_pin')
 need(et['actual_execution_permission_mode']=='require_escalated'and execution['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1'and execution['mode']=='execute'and execution['status']=='RETIRED_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED'and execution['failure']is None and execution['plan_pin']==cp['plan']and execution['actual_released_pins']==ep['exact_target_pins']and len(ep['exact_target_pins'])==2 and ep['exact_target_pins'][0]==b['retired_original_product_pins'][0]and execution['actual_released_bytes']==sum(p['size_bytes']for p in ep['exact_target_pins'])==101693287 and execution['files_deleted']is True and execution['resources_after_original_classes_forced_fresh']is True,'genuine exact2 original plus incomplete archive retirement0; exact bytes preserved')
 need(post['schema']==roles['schema']and post['status']==roles['status']and post['failure']is None and post['metadata_only']is True and post[roles['execution_receipt_pin_field']]==cp['execution_receipt']and post[roles['Root_tools_pin_field']]==cp['Root_tools']and post[roles['released_pins_field']]==ep['exact_target_pins']and post[roles['released_bytes_field']]==101693287 and post['files_deleted']is True and post['files_deleted_by_post']is False,'same independently completed exact2 metadata post0')
 need(ep['retained_member0_entry_pin']==b['reused_member0_entry_pin']and ep['retained_member0_gzip_pin']==b['reused_member0_gzip_pin']and ep['retained_other3_original_product_pins']==b['live_original_product_pins']and ep['retained_native_current7_pins']==b['retained_native_current7_pins']and ep['original_B_native_and_readonly_input_current7_pins']==b['original_B_native_and_readonly_input_current7_pins']and ep['complete_joint_roots']==b['inherited_latest_complete_joint_roots'],'exact old retained classes and full inherited prefix')
 for target in ep['exact_target_pins']:need(not os.path.lexists(target['path']),'exact2 targets remain absent, no old body read')
 for p in ep['retained_archive_metadata_current7_pins']:current(p)
 vp=ep['actual_single_member_verification_closure_pins'];vr=ep['actual_single_member_Root_key_projection'];pr=ep['actual_single_member_post_key_projection'];verify=meta(vp['Root_report']);vtools=meta(vp['Root_tools']);vpost=meta(vp['post']);vptools=meta(vp['post_tools']);original=b['all4_product_pins'][0]
 genuine(vtools,'actual_terminal_return',vp['Root_report'],'report_pin');genuine(vptools,'actual_review_return',vp['post'],'review_pin')
 need(verify['schema']==vr['schema']and verify['status']==vr['status']and verify['failure']is None and verify[vr['entry_pin_field']]==b['reused_member0_entry_pin']and verify[vr['original_pin_field']]==original and verify[vr['gzip_pin_field']]==b['reused_member0_gzip_pin']and verify[vr['decompressed_SHA_field']]==original['sha256']and verify[vr['decompressed_length_field']]==original['size_bytes']and verify[vr['streamed_complete_field']]is True and verify['children_started']==0,'genuine prior independent complete member0 restoration stream0, no repeat decompression')
 need(vpost['schema']==pr['schema']and vpost['status']==pr['status']and vpost['failure']is None and vpost['metadata_only']is True and vpost[pr['Root_report_pin_field']]==vp['Root_report']and vpost[pr['Root_tools_pin_field']]==vp['Root_tools']and vpost[pr['entry_pin_field']]==b['reused_member0_entry_pin']and vpost[pr['original_pin_field']]==original and vpost[pr['gzip_pin_field']]==b['reused_member0_gzip_pin']and vpost[pr['separate_Root_stream_proof_matched_field']]is True,'same genuine independent member0 metadata post0')
 fp=ep['actual_failed_archive_closure_pins'];failedhost=meta(fp['Host']);failedtools=meta(fp['Root_tools']);failedwatch=meta(fp['watchdog']);failedpost=meta(fp['post']);fptools=meta(fp['post_tools']);closed(failedtools,'actual_terminal_return',1);genuine(fptools,'actual_review_return',fp['post'],'review_pin')
 need(failedhost['status']=='FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED'and failedhost['archive_complete']is False and failedhost['actual_watchdog']is None and failedhost['actual_child_receipt']is None and type(failedwatch['returncode'])is int and failedwatch['returncode']==1 and failedpost['status']=='PASS_FAILURE_FACTS_ONLY'and failedpost['actual_Root_integer_exit_code']==1 and failedpost['actual_recorded_child_integer_exit_codes']==[],'original failed Root1, standalone child1 and old limited post child_codes[] all preserved')
 sp=b['actual_failed_archive_supplemental_post_pin'];sup=meta(sp);stools=meta(b['actual_failed_archive_supplemental_post_tools_pin']);sr=b['actual_failed_archive_supplemental_post_projection'];genuine(stools,'actual_review_return',sp,'review_pin')
 need(sup['schema']==sr['schema']and sup['status']==sr['status']and sup['failure']is None and sup['metadata_only']is True and sup[sr['Host_pin_field']]==fp['Host']and sup[sr['Root_tools_pin_field']]==fp['Root_tools']and sup[sr['member0_entry_pin_field']]==b['reused_member0_entry_pin']and sup[sr['member0_gzip_pin_field']]==b['reused_member0_gzip_pin']and sup['original_prior_post_recorded_child_integer_exit_codes']==[]and sup['supplemental_actual_recorded_child_integer_exit_codes']==[1]and sup['original_prior_post_integer_exit_code']==0,'separate supplementary standalone child1 source, no rewrite of old absent watchdog or child list')
 return ep,cp,fp,vp

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact separate executor and immutable single post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);root=meta(pRoot);host=None if pHost is None else meta(pHost);actual=root['actual_terminal_return']
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==root['original_integer_exit_code']and actual.get('session_id')is None and root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine original typed closed Root terminal/permission/no retry')
 pb=pin(PACKAGE/'PLAN.json')if host is None else host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];limit=b['bounded_total_output_bytes'];source_limit=b['bounded_Source_metadata_bytes']
 need(b['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_REUSE_MEMBER0_BINDING_V2'and b['original_caps']==CAPS and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and limit==96*2**20 and b['bounded_archive_payload_bytes']==88*2**20 and b['metadata_runtime_headroom_bytes']==8*2**20 and source_limit==16*2**20 and roots[-1]==str(out),'actual B4 v2 binding/96 total88 new payload8 metadata/Source16 and original caps')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_B4_products_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_GUARDED_HOST_REPORT_V2','actual B4 v2 Host report role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins);code=root['original_integer_exit_code']
 if code!=0:
  observed=[];watchpins=[]
  if host is not None:
   for record in host['records']:
    wp=table.get(str(out/(record['label']+'.watchdog.json')))
    if wp is not None:
     w=meta(wp);need(type(w['returncode'])is int and w['command']==record['command'],'record-label standalone actual watchdog and typed code');observed.append(w['returncode']);watchpins.append(wp)
  result=dict(schema='CURRENT_B4_V2_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_standalone_record_label_watchdog_pins=watchpins,actual_recorded_child_integer_exit_codes=observed,absent_child_code_invented=False,child_code_inferred_from_Root_return=False,new_partial_output_blind_fullEOF_twice_pins=newpins,archive_success_or_roundtrip_inferred=False,execution_binding_pin=pb,archive_complete=False)
  save(result,source_limit);return
 need(host is not None,'Root0 requires genuine Host report PF');genuine(root,'actual_terminal_return',pHost,'report_pin')
 need(host['status']=='ACTUAL_CURRENT_B4_ALL_PRODUCTS_ARCHIVE_REUSE_MEMBER0_CLOSED0_ONE_RETIRED_THREE_LIVE'and host['failure']is None and host['secondary_failures']==[]and host['archive_complete']is True and host['retries']==0 and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False and host['independent_archive_post0_required']is True and host['original_products_exact1_retired3_current7_live']is True,'actual original private OwnRSS closed0 complete B4 byte archive: one retired, three live')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
 need(core['Source_only_frozen_before_Root_generation']is True and core['whole_Source_file_pins']==sf['complete_source_file_pins']and core['original_archive_one_wholebytes']is True and core['entry0_original_plain_preserved_only_creation_history']is True,'exact whole five Source roles, unchanged archive_one and historical legacy entry')
 admitted=meta(core['whole_admission_binding_pin']);need(ready['author_admission_binding_pin']==core['whole_admission_binding_pin']and all(b[k]==v for k,v in admitted.items()),'whole author admission binding retained by Root generated plan')
 need(ready['schema']=='CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_REUSE_MEMBER0_SOURCE_REVIEW_READY_V2'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and sf['schema']=='CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_SOURCE_FREEZE_V2'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_HOST_FREEZE_V2'and hf['source_only']is True and hf['selected_source_freeze_pin']==host['source_freeze_pin']and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and ready['complete_source_file_pins']==sf['complete_source_file_pins']and len(sf['complete_source_file_pins'])==5 and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'same actual B4 v2 READY.execution_binding_pin and exact publication')
 peer=meta(hf['independent_Source_review_pin']);pt=meta(hf['independent_Source_review_tools_pin']);gt=meta(hf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',hf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_REUSE_MEMBER0_V2'and peer['failure']is None and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins']and sf['independent_Source_review_pin']==hf['independent_Source_review_pin']and sf['independent_Source_review_tools_pin']==hf['independent_Source_review_tools_pin']and sf['Root_Source_generation_true_tools_pin']==hf['Root_Source_generation_true_tools_pin'],'genuine exact v2 independent Source review0 and canonical true Root SourceGEN0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_FINAL_REVIEWABLE_ROOT_CLI_V2'and shlex.split(root['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual complete published24 Root argv and freeze PFs')
 latest=meta(b['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(out)]and roots[:-1]==b['inherited_latest_complete_joint_roots']and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'whole dynamic then-latest73 prefix plus one counted B4 v2 output root; Source stays counted')
 static=meta(core['static_evidence_pin']);need(static['prefix_before']==len(roots)-1 and static['prefix_with_new_own_output']==len(roots)and static['original_archive_one_wholebytes']is True,'frozen complete dynamic prefix counts match own Source audit')
 build=meta(b['original_guard_build_plan_pin']);capture=meta(b['actual_B_capture_Host_report_pin']);manifest=meta(b['actual_B_manifest_pin']);input_binding=meta(b['actual_B_input_binding_pin']);extract=meta(b['actual_B_extraction_child_report_pin']);state=capture['actual_B_state']
 originals=b['all4_product_pins'];retired=b['retired_original_product_pins'];live=b['live_original_product_pins'];retained=b['retained_native_current7_pins'];inputs=b['original_B_native_and_readonly_input_current7_pins']
 need(originals==state['actual_material_product_pins']and len(originals)==len({p['path']for p in originals})==4 and [Path(p['path']).name for p in originals]==['m.xsm','u.asc','a.asc','t.asc']and all(Path(p['path']).parent==Path(input_binding['actual_output_root'])for p in originals)and manifest['state_order']==['B']and manifest['states']['B']['actual_owning_report_pin']==b['actual_B_capture_Host_report_pin']and manifest['current_B_case_input_binding_pin']==b['actual_B_input_binding_pin']and retired==originals[:1]and live==originals[1:]and len(live)==3,'exact producer-order four historical product PFs, retired original0 and three live; no relabelling old scope')
 need(retained==state['complete_context_pins']+[x['input_pin']for x in state['complete_state_snapshot_inputs']]+[p for x in extract['states']['B']for p in(x['paired_SQLite_pin'],x['paired_original_pool_pin'])]and len(retained)==79 and len(inputs)==11 and not{p['path']for p in originals}&{p['path']for p in retained},'all55contexts/eight native XSM/sixteen SQL-pool and all11 original B inputs current7 only')
 ep,cp,fp,vp=previous_closure(b)
 for key in('retired_original_product_pins','live_original_product_pins','reused_member0_gzip_pin','reused_member0_entry_pin'):need(host[key]==b[key],'same host product lifecycle and reused member pins')
 need(len(host['records'])==1 and host['records'][0]['status']=='PASS','one actual original guarded archive child0, no retry');record=host['records'][0];wp=table[str(out/(record['label']+'.watchdog.json'))];lp=table[str(out/(record['label']+'.log'))];w=meta(wp)
 need(w==host['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and lp['sha256']==record['log_sha256'],'actual OwnRSS child0/record.label log/watch/original RSS/wall/liveness closure')
 claim=meta(pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'));command=record['command']
 need(len(command)==9 and command[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',str(PACKAGE/'archive_B4_products_serial.UNREADY.py'),'--binding-pin']and json.loads(command[4])==pb and command[5]=='--common-source-pin'and json.loads(command[6])==hf['common_source_pin']and command[7:] ==['--expected-parent-pid',str(claim['PID'])],'exact original child argv/whole binding/common Source and owning Root PID')
 logpath=full(lp);need(lp['size_bytes']<8*2**20,'bounded complete JSON child receipt log');lines=logpath.read_text().splitlines();need(len(lines)==1,'one genuine complete archive child receipt');receipt=json.loads(lines[0]);need(receipt==host['actual_child_receipt'],'actual original child receipt matches Host')
 childpin=receipt['report_pin'];child=meta(childpin)
 need(childpin['path']==str(out/'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REPORT.json')and child['schema']=='ACTUAL_CURRENT_B4_SERIAL_LOSSLESS_ARCHIVE_REUSE_MEMBER0_REPORT_V2'and child['status']=='ALL4_COMPLETE_B_PRODUCT_BYTE_PROOF_CLOSED0_ONE_RETIRED_THREE_LIVE'and receipt['status']==child['status']and child['failure']is None and type(child['completed_count'])is int and child['completed_count']==4 and type(child['newly_archived_count'])is int and child['newly_archived_count']==3 and type(child['reused_complete_archive_count'])is int and child['reused_complete_archive_count']==1 and child['binding_pin']==pb and child['original_products_exact1_retired3_current7_live']is True and child['all79_context_snapshot_and_saved_pair_files_current7_retained']is True,'actual serial complete4/one reused/three new child report')
 indexpin=child['index_pin'];index=meta(indexpin);rows=index['entries'];originalbytes=sum(p['size_bytes']for p in originals)
 need(indexpin['path']==str(out/'CURRENT_B4_LOSSLESS_ARCHIVE_INDEX.json')and index['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V2'and index['status']=='ALL4_COMPLETE_B_PRODUCTS_BYTE_PROOF_CLOSED_ONE_RETIRED_THREE_LIVE'and index['binding_pin']==pb and len(rows)==index['ordered_original_product_count']==4 and type(index['ordered_original_product_count'])is int and index['ordered_original_product_total_bytes']==child['original_product_total_bytes']==b['original4_product_total_bytes']==originalbytes and index['compression_ratio_assumed']is False and index['original_products_exact1_retired3_current7_live']is True and index['requires_independent_post0_before_separate_original_product_retirement']is True,'complete4 original-path lookup and byte totals, exact one-retired three-live lifecycle')
 for item in(child,index):
  for key in('retired_original_product_pins','live_original_product_pins','reused_member0_gzip_pin','reused_member0_entry_pin'):need(item[key]==b[key],'same child/index lifecycle and original member0 references')
 legacy=meta(b['reused_member0_entry_pin']);expected_reused=dict(entry_pin=b['reused_member0_entry_pin'],**legacy);expected_reused.update(original_plain_preserved_at_entry_creation=legacy['original_plain_preserved'],original_plain_preserved=False,original_product_current_lifecycle='EXACT_ARCHIVED_ORIGINAL_RETIRED',reused_complete_archive_from_failed_v1=True,actual_exact2_cleanup_execution_receipt_pin=cp['execution_receipt'])
 need(rows[0]==expected_reused and legacy['original_plain_preserved']is True,'legacy entry file unchanged creation history True, index copied lifecycle False with actual cleanup binding')
 archives=[];entrypins=[];proofs=[]
 for ordinal,(row,p)in enumerate(zip(rows,originals)):
  need(type(row['ordinal'])is int and row['ordinal']==ordinal and row['original_plain_full_pin']==p and row['actual_B_capture_product_name']==Path(p['path']).name and row['original_product_is_complete']is True and row['compression_input_SHA']==row['streamed_decompressed_SHA']==p['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==p['size_bytes']and type(row['compression_input_length'])is int and type(row['streamed_decompressed_length'])is int and row['exact_original_plain_bytes_recoverable']is True and row['result_values_decoded']is False and row['scientific_values_decoded']is False and row['filename_field']==''and type(row['mtime'])is int and row['mtime']==0 and type(row['compresslevel'])is int and row['compresslevel']==6,'actual recorded stream input/decompressed SHA and length equal exact originalPF; no repeat stream or science')
  pgz=row['compressed_archive_full_pin'];entrypin=row['entry_pin']
  if ordinal==0:
   need(pgz==b['reused_member0_gzip_pin']and entrypin==b['reused_member0_entry_pin']and row['original_plain_preserved']is False and row['original_plain_preserved_at_entry_creation']is True,'reused complete original-path member0 and historical entry')
   full(pgz);full(pgz);need(not os.path.lexists(p['path']),'retired member0 plain remains absent')
  else:
   need(pgz['path']==str(out/'archives'/(str(ordinal).zfill(3)+'_'+Path(p['path']).name+'.gz'))and table[pgz['path']]==pgz and row['original_plain_preserved']is True,'new compressed1-3 matched blindSHA twice, their originals remain live')
   need(entrypin['path']==str(out/('archive_entry_'+str(ordinal).zfill(3)+'.json'))and meta(entrypin)=={k:v for k,v in row.items()if k!='entry_pin'}and table[entrypin['path']]==entrypin,'new durable per-product entry equals exact index row')
   current(p)
  archives.append(pgz);entrypins.append(entrypin);proofs.append({k:row[k]for k in('ordinal','original_plain_full_pin','compressed_archive_full_pin','compression_input_SHA','compression_input_length','streamed_decompressed_SHA','streamed_decompressed_length','exact_original_plain_bytes_recoverable','original_plain_preserved')})
 gzipbytes=sum(p['size_bytes']for p in archives);newbytes=sum(p['size_bytes']for p in archives[1:]);need(gzipbytes==index['total_gzip_bytes']==child['total_gzip_bytes']and newbytes==index['new3_gzip_bytes']==child['new3_gzip_bytes']<b['bounded_archive_payload_bytes']and ownbytes<limit,'new3 payload88MiB/whole own96MiB, reused member remains counted in old root')
 need({p['path']for p in newpins if Path(p['path']).suffix=='.gz'}=={p['path']for p in archives[1:]},'all and only three new gzip files accounted, no duplicate old member')
 for p in[pHost,childpin,indexpin,wp,lp]+archives[1:]+entrypins[1:]:need(table[p['path']]==p,'all new complete archive controls and outputs blind SHA matched')
 childclaim=meta(table[str(out/'CHILD_ARCHIVE_CLAIM.json')]);need(type(childclaim['PID'])is int and type(childclaim['parent_PID'])is int and childclaim['PID']==w['pid']and childclaim['parent_PID']==claim['PID']and childclaim['retries']==0,'actual sole child PID and genuine owning parent, no retry')
 for _ in range(2):
  for p in live+retained+inputs+[b['reused_member0_entry_pin'],b['reused_member0_gzip_pin']]+ep['retained_archive_metadata_current7_pins']:current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  for p in ep['exact_target_pins']:need(not os.path.lexists(p['path']),'only exact2 absent paths remain absent')
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 archive_resources(child['resources_after'],roots,600)
 before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes'];need(existing+limit+source_limit<2*2**30 and before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'actual prelaunch complete prefix plus full96/Source16/current2GiB/history96 reservation, no compression assumption')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full cumulative/cold/free reserves, including own open-unlinked')
 for item in(host,child,index):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(item[key]is False,'complete byte archival cannot issue scientific/control/retirement/goal qualification')
 need(b['all48_or_JSONL_old_scope_reused_as_current_fact']is False and b['product_formats_decoded_or_claimed']is False and b['original_plain_retirement_in_this_stage']is False and b['future_aggregate_budget_added_to_this_stage']is False,'exact B4 byte archive scope only, no old labels or future scientific/retirement budget admission')
 result=dict(schema='RECORDED_CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_REUSE_MEMBER0_METADATA_POSTVERIFY_V2',status='PASS_ACTUAL_ALL4_COMPLETE_B_PRODUCTS_BYTE_PROOF_ONE_REUSED_THREE_NEW_ONE_RETIRED_THREE_LIVE_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],execution_binding_pin=pb,actual_child_report_pin=childpin,actual_archive_index_pin=indexpin,ordered4_original_product_full_pins=originals,ordered4_compressed_archive_full_pins=archives,ordered4_entry_pins=entrypins,actual_four_streamed_SHA_and_length_proof_records=proofs,original_product_bytes=originalbytes,gzip_bytes=gzipbytes,new3_gzip_bytes=newbytes,entire_archive_output_bytes=ownbytes,archive_complete=True,completed_count=4,newly_archived_count=3,reused_complete_archive_count=1,original_products_exact1_retired3_current7_live=True,retired_original_product_pins=retired,live_original_product_pins=live,reused_member0_gzip_pin=b['reused_member0_gzip_pin'],reused_member0_entry_pin=b['reused_member0_entry_pin'],legacy_entry_original_plain_preserved_is_creation_history=True,legacy_entry_file_original_plain_preserved=True,index_entry0_current_original_plain_preserved=False,live3_original_current7_verified_twice_only=True,compressed3_new_and1_reused_fullEOF_SHA_current7_verified_twice=True,Root_recorded_stream_decompression_proofs_matched_original_fullPF=True,independent_decompression_or_numeric_recomparison=False,all4_original_products_current7_retained=False,all79_native_context_tree_and_SQL_pool_current7_retained=True,all11_originalB_input_current7_retained=True,retained79_native_context_tree_SQL_pool_current7_pins=retained,original11_B_input_current7_pins=inputs,actual_exact2_cleanup_closure_pins=cp,actual_member0_independent_stream_closure_pins=vp,original_failed_archive_closure_pins=fp,original_failed_archive_Root_integer_exit_code=1,original_failed_archive_child_integer_exit_code=1,original_limited_failure_post_child_codes=[],supplemental_standalone_child_codes=[1],original_failed_archive_still_failed=True,original_guard_class_and_MRO_unchanged=True,actual_original_runner_record=record,actual_original_watchdog=w,actual_watchdog_pin=wp,actual_child_receipt_log_pin=lp,complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,actual_original_host_resources_before=host['resources_before'],actual_original_host_resources_after=host['resources_after'],actual_original_host_resources_after_including_summary=host['resources_after_including_summary_bytes'],actual_child_resource_facts=child['resources_after'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_CLI_pin=cli_pin,actual_Source_peer_pin=hf['independent_Source_review_pin'],actual_Source_peer_tools_pin=hf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=hf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,Source_author_also_authored_archive_workflow=False,old48_JSONL_A2_early14_fixed_labels_used_as_current_facts=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

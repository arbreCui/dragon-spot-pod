"""UNREADY independent metadata post for complete nativeWarmB2 extraction.

Source and bounded metadata are read in full; old payloads are current7 only.
Only this completed extraction's new outputs receive two blind byte SHA passes.
No helper/candidate import, SQL/native/JSONL value decode or native execution.
The exact author core freeze and every actual argument remain NULL until bound.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b2_build_source_peer';EXECUTOR='/root/b_capture_actual_post_source'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B55_vs_nativeWarmB2_full_macro_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': 'c50cc000a86989c3d83b51e29cd6f66eff9b24a6c61d2621ab0daf800e97e686', 'size_bytes': 8131, 'identity': [16777229, 50882089, 33188, 1, 8131, 1792066216124311848, 1792066216124311848]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,historical_unsaved_context_recovered=False,SQL_or_pool_or_physical_JSONL_values_decoded=False,old_B2_payload_body_replayed=False,old_gzip_or_original_body_hashed=False,B55_B2_typed_word_comparison_executed=False,B55_B2_tree_or_word_equality_qualified=False,lineage_online_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,files_deleted=False)
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
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh extraction output')
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

def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)

def unique(rows):
 table={}
 for p in rows:
  key=p['path'];need(key not in table or table[key]==p,'one exact PF per metadata path');table[key]=p
 return list(table.values())

def saved_resources(v,roots,history_inputs):
 h=v['original_history'];j=v['complete_joint'];sample=v['actual_PS_return']
 need(v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800 and v['entire_extraction_output_bytes']<256*2**20 and j['resource_roots']==roots,'actual original SELF512/wall and full extraction256/complete77')
 need(sample['argv']==['/bin/ps','-o','rss=','-p',str(v['current_PID'])] and type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']=='' and sample['stdout'].strip().isdigit() and int(sample['stdout'].strip())*1024<512*2**20,'saved actual same-PID PS/RSS facts; PS not repeated')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history96/joint2/cold/meta/free8/external/open-unlinked bounds')
 need(all(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots'])for p in history_inputs),'all nine cold B2 roles in original history, not hidden in ordinary fresh metadata')

def prerequisites(plan):
 bridge=meta(plan['actual_B2_current_epoch_bridge_report_pin']);bridgetools=meta(plan['actual_B2_current_epoch_bridge_Root_tools_pin'])
 bridgepost=meta(plan['actual_B2_current_epoch_bridge_post_pin']);bridgeposttools=meta(plan['actual_B2_current_epoch_bridge_post_tools_pin'])
 genuine(bridgetools,'actual_terminal_return',plan['actual_B2_current_epoch_bridge_report_pin'],'report_pin');genuine(bridgeposttools,'actual_review_return',plan['actual_B2_current_epoch_bridge_post_pin'],'review_pin')
 need(bridge['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and bridge['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bridge['failure']is None and bridge['final_report_resource_check_passed']is True and bridge['original_caps']==CAPS and len(bridge['ordered_role_pairs'])==9,'actual selected9 bridge0; no all4790 or lineage qualification')
 bc=plan['bridge_post_contract'];need(bridgepost['schema']==bc['schema']and bridgepost['status']==bc['status']and bridgepost['failure']is None and bridgepost[bc['Root_report_pin_field']]==plan['actual_B2_current_epoch_bridge_report_pin']and bridgepost[bc['Root_tools_pin_field']]==plan['actual_B2_current_epoch_bridge_Root_tools_pin'],'actual independent bridge post0')
 cold=[r['current_epoch_full_pin']for r in bridge['ordered_role_pairs']]
 need(cold==plan['retained_B2_current_epoch_readonly_pins']and plan['actual_current_epoch_B2_archive_pin']==bridge['current_epoch_B2_archive_pin']and plan['historical_B2_archive_pin']==next(r['historical_full_pin']for r in bridge['ordered_role_pairs']if r['role']=='B2_archive'),'exact separate historical and current B2 roles')
 for r in bridge['ordered_role_pairs']:
  a=r['historical_full_pin'];b=r['current_epoch_full_pin'];need(r['blind_complete_SHA_and_length_equal']is True and r['before_open_EOF_after_current7_stable']is True and a['sha256']==b['sha256']and a['size_bytes']==b['size_bytes']and a['identity'][1:]==b['identity'][1:]and a['identity'][0]==16777234 and b['identity'][0]==16777229,'historical old device preserved; new selected9 device epoch PFs separate');current(b)
 retired=meta(plan['actual_latest_complete_prefix_plan_pin']);receipt=meta(plan['actual_presence_retirement_receipt_pin']);tools=meta(plan['actual_presence_retirement_Root_tools_pin'])
 post=meta(plan['actual_presence_retirement_post_pin']);posttools=meta(plan['actual_presence_retirement_post_tools_pin'])
 genuine(tools,'actual_terminal_return',plan['actual_presence_retirement_receipt_pin'],'receipt_pin');genuine(posttools,'actual_review_return',plan['actual_presence_retirement_post_pin'],'review_pin')
 target=retired['exact_target_pins'];need(retired['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and retired['Source_admission_ready']is True and retired['draft_unready']is False and len(target)==1 and target[0]['size_bytes']==169615994 and target[0]['sha256']=='9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7','only exact presence original retired; no generic missing-role skip')
 need(receipt['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['plan_pin']==plan['actual_latest_complete_prefix_plan_pin']and receipt['actual_released_pins']==receipt['exact_target_pins']==target and receipt['actual_released_bytes']==169615994 and receipt['resources_after_original_classes_forced_fresh']is True and receipt['files_deleted']is True,'actual exact1 Root0 release, same plan and forced fresh resource closure')
 rc=retired['execute_post_report_contract'];need(post['schema']==rc['schema']and post['status']==rc['status']and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==plan['actual_presence_retirement_receipt_pin']and post['actual_Root_tools_pin']==plan['actual_presence_retirement_Root_tools_pin']and post['plan_pin']==plan['actual_latest_complete_prefix_plan_pin']and post['actual_released_pins']==target and post['actual_released_bytes']==169615994 and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['files_deleted_by_post']is False,'actual independent exact1 metadata post0')
 for p in target:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact retired presence absent; original PF remains historical')
 cp=retired['actual_archive_closure_pins'];need(plan['actual_presence_archive_report_pin']==cp['Host']and plan['actual_presence_archive_Root_tools_pin']==cp['Root_tools']and plan['actual_presence_archive_post_pin']==cp['post']and plan['actual_presence_archive_post_tools_pin']==cp['post_tools'],'same exact original presence archive Root0/post0')
 archive=meta(retired['inherited_complete_archive_plan_pin']);apost=meta(cp['post']);genuine(meta(cp['post_tools']),'actual_review_return',cp['post'],'review_pin');genuine(meta(cp['Root_tools']),'actual_terminal_return',cp['Host'],'report_pin')
 need(apost['schema']=='RECORDED_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and apost['status']=='PASS_ACTUAL_SINGLE_BAGG_PRESENCE_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_ORIGINAL_RETAINED'and apost['failure']is None and apost['original_presence_full_pin']==target[0]and apost['compressed_presence_archive_full_pin']==retired['retained_presence_gzip_pins'][0]and apost['presence_entry_pin']==retired['retained_presence_entry_pins'][0]and apost['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True,'complete presence original SHA/length is preserved in permanent exact archive mapping')
 index=meta(cp['index']);entry=meta(retired['retained_presence_entry_pins'][0]);row=index['entries'][0]
 need(index['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and len(index['entries'])==1 and row['entry_pin']==retired['retained_presence_entry_pins'][0]and entry=={k:v for k,v in row.items()if k!='entry_pin'}and row['original_plain_full_pin']==target[0]and row['compression_input_SHA']==row['streamed_decompressed_SHA']==target[0]['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==target[0]['size_bytes']and row['compressed_archive_full_pin']==retired['retained_presence_gzip_pins'][0],'single complete archive/entry/index exact saved byte-proof metadata, no decompression or old body hash')
 roots=plan['complete_joint_roots'];need(len(roots)==77 and len(set(roots))==77 and roots[:-1]==retired['complete_joint_roots']==archive['complete_joint_roots']and roots[-1]==plan['planned_actual_output_root']and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(PACKAGE.is_relative_to(Path(r))for r in roots[:-1]),'complete inherited75/presence76/extraction77 with owning Source counted')
 retained=retired['retained_current7_pins']+retired['retained_presence_gzip_pins']+retired['retained_presence_entry_pins']+[cp['index']]
 need(plan['retained_current7_pins']==retained and not{p['path']for p in target}&{p['path']for p in retained+cold+plan['explicit_cumulative_metadata_file_pins']}and not{p['path']for p in cold}&{p['path']for p in plan['explicit_cumulative_metadata_file_pins']},'all other16 results/native/B4all4 archives/entries/index and cold9 live; cold inputs not fresh metadata')
 lineage=meta(plan['actual_B2_lineage_metadata_audit_pin'])
 return retired,bridge,retained,cold,lineage

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for key in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+key,required=True)
 args=ap.parse_args();need(args.executor_task_name==EXECUTOR and AUTHOR!=EXECUTOR,'independent metadata executor, never Source author');need(EXPECTED_CORE_AUTHOR_FREEZE is not None,'UNREADY until exact whole core author freeze bound')
 ptools=json.loads(args.Root_tools_pin);phost=json.loads(args.Host_pin);raw=meta(ptools);host=meta(phost)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(raw['actual_terminal_return']['exit_code'])is int and raw['original_integer_exit_code']==raw['actual_terminal_return']['exit_code']and raw['actual_terminal_return'].get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'genuine original terminal integer preserved; one Root actual process')
 author=meta(EXPECTED_CORE_AUTHOR_FREEZE);need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'separate core Source author and Root sole GEN/business')
 psf=host['source_freeze_pin'];phf=host['host_freeze_pin'];sf=meta(psf);hf=meta(phf);pp=host['control_plan_pin'];plan=meta(pp)
 need(host['schema']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_GUARDED_ROOT_REPORT_V1'and plan['schema']=='CURRENT_B2_COMPLETE_EXTRACTION_SOURCE_ONLY_PLAN_V1'and plan['actual_business_preconditions_closed']is True and plan['source_role_pin_audit_complete']is True and host['original_caps']==plan['original_caps']==CAPS,'exact actual owning Root and bound complete Source plan')
 need(sf['schema']=='COMPLETE_CURRENT_B2_PHYSICAL_TREE_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False and hf['schema']=='CURRENT_B2_COMPLETE_EXTRACTION_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==psf and sf['control_plan_pin']==pp and sf['complete_source_file_pins']==author['whole_Source_file_pins']and hf['original_caps']==CAPS,'same exact frozen whole Source table and host publication')
 table=sf['complete_source_file_pins'];need(len({p['path']for p in table})==len(table),'complete distinct Source files')
 for p in table:full(p)
 pready=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(pready);need(ready['control_plan_pin']==pp and ready['complete_source_file_pins']==table and ready['host_source_pin']==hf['host_source_pin']and ready['contract_Source_pin']==hf['contract_Source_pin'],'same ready/Source/host exact publication')
 peer=meta(sf['independent_Source_review_pin']);genuine(meta(sf['independent_Source_review_tools_pin']),'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(meta(sf['Root_Source_generation_true_tools_pin']),'actual_Source_preparation_return',pready,'ready_pin')
 need(peer['status']=='PASS_SOURCE_ONLY_CURRENT_B2_COMPLETE_PHYSICAL_EXTRACTION'and peer['source_only']is True and peer['failure']is None and peer['control_plan_pin']==pp and peer['complete_source_file_pins']==table and hf['independent_Source_review_pin']==sf['independent_Source_review_pin']and hf['independent_Source_review_tools_pin']==sf['independent_Source_review_tools_pin'],'separate genuine full-package Source0 and GEN0 preserved')
 pcli=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(pcli);argv=cli['argv'];prefix=plan['original_complete_ENV_Python_B_prefix']
 need(cli['schema']=='CURRENT_B2_COMPLETE_PHYSICAL_EXTRACTION_FINAL_ROOT_CLI_V1'and len(argv)==24 and argv[:len(prefix)]==prefix and argv[len(prefix)]==hf['host_source_pin']['path']and cli['source_freeze_pin']==psf and cli['host_freeze_pin']==phf and cli['command']==shlex.join(argv)==raw['exact_executed_command']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact published original24 command and permission, not reconstructed launch')
 prootclaim=pin(PACKAGE/'ROOT_B2_EXTRACTION_ONCE_CLAIM.json');rootclaim=meta(prootclaim);need(rootclaim['schema']=='ROOT_CURRENT_B2_EXTRACTION_EXCLUSIVE_ONCE_CLAIM_V1'and rootclaim['argv']==argv[len(prefix):]and rootclaim['claim_before_project_import_and_payload_IO']is True and rootclaim['retries']==0,'original exclusive owning Root claim before helper/import/body')
 retired,bridge,retained,cold,lineage=prerequisites(plan);roots=plan['complete_joint_roots'];need(host['complete_joint_roots']==roots and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True and host['comparison_executed']is False,'original owning guard and no comparison stage')
 build=meta(plan['original_guard_build_plan_pin']);extra=unique(hf['explicit_cumulative_metadata_file_pins']+[ptools,phost,EXPECTED_CORE_AUTHOR_FREEZE,psf,phf,pp,pready,pcli,prootclaim])
 need(not{p['path']for p in cold}&{p['path']for p in extra},'nine historical readonly payloads never mislabeled external metadata')
 for _ in range(2):
  for p in retained+cold:current(p)
  for p in extra:current_role(p,build)
 out=Path(plan['planned_actual_output_root']);need(out==Path(roots[-1])and not any(x.is_symlink()for x in(out,*out.parents)),'literal complete current owning output root')
 if raw['original_integer_exit_code']!=0:
  need(host['failure']is not None and host['status']=='FAILED_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_NO_RETRY'and host['complete_physical_tree_extraction_completed']is False,'original real failure retained, never converted to expected child2 success')
  watch=host['actual_watchdog'];code=None if watch is None else watch['returncode'];need(code is None or type(code)is int,'real optional child integer preserved without inventing2')
  need(host['actual_child_integer_exit_code']==code,'Host original real child/watch facts')
  report=dict(schema='RECORDED_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_FAILURE_METADATA_POSTVERIFY_V1',status='PASS_RECORDED_ACTUAL_CURRENT_B2_EXTRACTION_FAILURE_FACTS_METADATA_ONLY',failure=None,actual_Host_report_pin=phost,actual_Root_tools_pin=ptools,actual_Root_integer_exit_code=raw['original_integer_exit_code'],actual_child_integer_exit_code=code,actual_watchdog=watch,original_Host_failure=host['failure'],original_Host_status=host['status'],original_records=host['records'],original_runner_error=host['original_runner_error'],complete_physical_tree_extraction_completed=False,complete_tree_counts=None,Source_author_core_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=pp,complete_joint_roots=roots,original_caps=CAPS,retained_roles_current7_verified_twice=True,actual_B2_lineage_metadata_audit_pin=plan['actual_B2_lineage_metadata_audit_pin'],selected9_current_epoch_role_pairs=bridge['ordered_role_pairs'],no_payload_body_hashed_by_failure_post=True)
  save(report,16*2**20);return
 genuine(raw,'actual_terminal_return',phost,'report_pin');stdout=json.loads(raw['actual_terminal_return']['output'].strip().splitlines()[-1]);need(type(stdout['actual_child_evidence_only_integer_exit_code'])is int and stdout['actual_child_evidence_only_integer_exit_code']==2 and stdout['original_runner_FAILED_record_preserved']is True,'genuine Root0 distinct from original evidence child2')
 need(host['status']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_EVIDENCE_CHILD2_CLOSED_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['actual_intentional_exit2_normal_closure']is True and host['complete_physical_tree_extraction_completed']is True and host['final_report_resource_check_passed']is True and len(host['records'])==1 and host['records'][0]['status']=='FAILED'and host['records'][0]['error']==host['original_runner_error']=='own-child stage failed; no retry','original FAILED/error record preserved for one intentional complete-evidence child2')
 watch=meta(host['actual_watchdog_full_pin']);need(watch==host['actual_watchdog']and type(watch['returncode'])is int and watch['returncode']==host['actual_child_integer_exit_code']==2 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'genuine original private OwnRSS child2/watch/limit facts')
 preq=host['actual_execution_request_pin'];request=meta(preq);rb=request['root_owning_runtime_Source_binding'];childclaim=meta(pin(out/'CHILD_B2_EXTRACTION_ONCE_CLAIM.json'))
 need(request['schema']=='CURRENT_NATIVEWARM_B2_COMPLETE_READONLY_EXTRACTION_REQUEST_V1'and request['owning_host_output_directory']==str(out)and request['child_output_directory']==str(out/'evidence')and rb['source_freeze_pin']==psf and rb['host_freeze_pin']==phf and rb['parent_PID']==rootclaim['PID']and rb['original_guard_class']=='OwnRSSSerialExecutor'and rb['original_guard_MRO_unchanged']is True and rb['owned_bounded_pin']['sha256']==plan['original_bounded_Source_pin']['sha256'],'same actual request, owned bounded copy and original private guard identity')
 need(childclaim['schema']=='CURRENT_B2_COMPLETE_EXTRACTION_CHILD_ONCE_CLAIM_V1'and childclaim['PID']==watch['pid']and childclaim['parent_PID']==rootclaim['PID']and childclaim['claim_before_project_helpers_and_payload_IO']is True and childclaim['retries']==0,'one actual child claim before imports/body under exact owning parent')
 for k in('actual_current_epoch_B2_archive_pin','historical_B2_archive_pin','actual_B2_current_epoch_bridge_report_pin','actual_B2_current_epoch_bridge_post_pin','actual_presence_archive_post_pin','actual_presence_retirement_post_pin','actual_latest_complete_prefix_plan_pin','actual_B2_lineage_metadata_audit_pin'):need(request[k]==plan[k],'same exact actual prerequisite request role '+k)
 need(host['actual_child_receipt']['report_pin']==host['actual_child_report_pin']and host['actual_child_receipt']['status']=='ACTUAL_COMPLETE_NATIVEWARM_B2_EXTRACTION_EVIDENCE_ONLY_EXIT2'and host['actual_child_receipt']['actual_parent_PID']==rootclaim['PID'],'actual full extraction receipt under same direct owning parent')
 childresources=host['actual_child_resources_after'];need(childresources==host['actual_child_receipt']['resources_after']and childresources['current_PID']==watch['pid']and childresources['current_parent_PID']==rootclaim['PID']and 0<=childresources['whole_elapsed_seconds']<600,'actual original child stage600/resource facts and direct owning parent PID preserved');saved_resources(childresources,roots,cold)
 pchild=host['actual_child_report_pin'];facts=meta(pchild);need(pchild['path']==str(out/'evidence/ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_REPORT.json')and facts['schema']=='ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_V1'and facts['status']=='COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_READONLY_EVIDENCE_ONLY'and facts['actual_current_epoch_B2_archive_pin']==plan['actual_current_epoch_B2_archive_pin']and facts['historical_B2_archive_pin']==plan['historical_B2_archive_pin']and facts['actual_B2_current_epoch_bridge_report_pin']==plan['actual_B2_current_epoch_bridge_report_pin']and facts['actual_B2_lineage_metadata_audit_pin']==plan['actual_B2_lineage_metadata_audit_pin'],'actual full physical tree report, never older material or AAA replacement')
 fields=('complete_physical_tree_records','complete_directories','complete_extents','complete_MICROLIB2_list1_MACROLIB_records')
 need(all(type(facts[k])is int and facts[k]>0 for k in fields)and facts['complete_physical_tree_records']>=19620 and facts['complete_MICROLIB2_list1_MACROLIB_records']==19620,'actual tree/directory/extent counts; exactly all19620 MACROLIB typed root records')
 for k in('entire_original_physical_tree_walked','all_original_types_counts_words_and_physical_API_orders_saved','unrelated_original_containers_retained','full_original_scope_not_replaced_by_19249_constructed_fields'):need(facts[k]is True,'complete physical tree scope saved '+k)
 for k in('native_library_or_solver_invoked','ASCII_used_or_invented','original_RAM_bits_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(facts[k]is False,'evidence only; false qualification remains '+k)
 products=facts['all_output_file_pins'];need(products==[facts['paired_SQLite_pin'],facts['paired_original_pool_pin'],facts['complete_physical_directory_slots_pin']]and [p['path']for p in products]==[str(out/'evidence'/name)for name in('complete_native_original_path_index.sqlite','complete_native_original_value_bytes.bin','complete_native_physical_directory_slots.jsonl')],'complete exact SQL/pool/physical-directory index3 products, no values decoded')
 new=all_output_pins(out);by_path={p['path']:p for p in new};need(all(by_path.get(p['path'])==p for p in products+[pchild,preq,host['actual_watchdog_full_pin'],host['actual_log_full_pin'],phost,rb['owned_bounded_pin']]),'all completed new output PFs blind SHA verified twice')
 for v in(host['resources_before'],host['resources_after']):saved_resources(v,roots,cold);need(v['current_PID']==rootclaim['PID'],'same actual owning Root resource PID')
 reservation=host['actual_stage_reservation'];existing=reservation['existing_measured_total_bytes'];before=host['resources_before'];need(existing==before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']and reservation['complete_joint_roots']==roots and reservation['original_caps']==CAPS and reservation['only_current_stage']=='complete_B2_extract'and reservation['stage_output_reservation_bytes']==256*2**20 and reservation['new_Source_metadata_reservation_bytes']==16*2**20 and reservation['comparison_stage_not_reserved']is True and existing+272*2**20<2*2**30,'actual fresh77 full256+Source16 sequential reservation, no comparison admission')
 joint=counted_bytes(roots);external=sum(p['size_bytes']for p in extra if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(external<64*2**20 and joint+external+unlinked<2*2**30 and counted_bytes([str(out)])<256*2**20 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'fresh metadata post complete77/full256/original cold/meta/free and open-unlinked accounting')
 for _ in range(2):
  for p in retained+cold:current(p)
  for p in extra:current_role(p,build)
 report=dict(schema='RECORDED_CURRENT_NATIVEWARM_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_ROOT0_CHILD2_METADATA_ONLY',failure=None,actual_Root_tools_pin=ptools,actual_Host_report_pin=phost,actual_child_report_pin=pchild,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=2,original_records=host['records'],original_runner_error=host['original_runner_error'],original_FAILED_error_and_expected_child2_preserved=True,actual_watchdog=watch,actual_execution_request_pin=preq,actual_source_freeze_pin=psf,actual_host_freeze_pin=phf,control_plan_pin=pp,Source_author_core_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,complete_source_file_pins=table,actual_original_Root_command=raw['exact_executed_command'],actual_original_guard_class=host['original_guard_class'],actual_original_guard_MRO_unchanged=True,actual_stage_reservation=reservation,actual_original_resources_before=host['resources_before'],actual_original_resources_after=host['resources_after'],actual_original_child_resources_after=childresources,complete_joint_roots=roots,original_caps=CAPS,complete_physical_tree_extraction_completed=True,actual_full_physical_tree_counts={k:facts[k]for k in fields},paired_SQLite_pin=facts['paired_SQLite_pin'],paired_original_pool_pin=facts['paired_original_pool_pin'],complete_physical_directory_slots_pin=facts['complete_physical_directory_slots_pin'],new_complete_output_full_pins=new,new_output_blind_fullEOF_SHA_verified_twice=True,no_SQL_pool_physical_JSONL_values_decoded=True,all_original_typed_metadata_original_words_and_physical_API_orders_saved=True,unrelated_original_containers_preserved=True,not_limited_to_constructed19249_fields=True,actual_current_epoch_B2_archive_pin=plan['actual_current_epoch_B2_archive_pin'],historical_B2_archive_pin=plan['historical_B2_archive_pin'],selected9_current_epoch_role_pairs=bridge['ordered_role_pairs'],old_historical_device_PFs_preserved=True,old_B2_payload_current7_only_by_post=True,actual_B2_lineage_metadata_audit_pin=plan['actual_B2_lineage_metadata_audit_pin'],actual_B2_current_epoch_bridge_report_pin=plan['actual_B2_current_epoch_bridge_report_pin'],actual_B2_current_epoch_bridge_post_pin=plan['actual_B2_current_epoch_bridge_post_pin'],actual_presence_retirement_post_pin=plan['actual_presence_retirement_post_pin'],historical_retired_presence_full_pin=retired['exact_target_pins'][0],permanent_presence_gzip_entry_index_pins=retired['retained_presence_gzip_pins']+retired['retained_presence_entry_pins']+[retired['actual_archive_closure_pins']['index']],exact_presence_retirement_not_generic_missing_skip=True,retained_current7_pins=retained,retained_cold_B2_current7_pins=cold,retained_metadata_current7_pins=extra,all_retained_roles_current7_verified_twice=True,comparison_stage_not_executed=True,original_AAA_three_macro_qualification_not_replaced=True,current_joint_bytes=joint,current_external_metadata_bytes=external,current_post_open_unlinked_bytes=unlinked)
 save(report,16*2**20,joint+external+unlinked)

if __name__=='__main__':main()

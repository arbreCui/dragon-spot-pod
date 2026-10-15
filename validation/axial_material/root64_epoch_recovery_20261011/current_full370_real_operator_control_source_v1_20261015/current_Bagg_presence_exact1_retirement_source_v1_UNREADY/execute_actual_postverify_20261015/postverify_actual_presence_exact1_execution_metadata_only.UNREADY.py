"""UNREADY independent metadata post after actual single presence exact1 execution.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Source and plan are checked against the real owning receipt and author freeze; future actual parameters remain NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
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
def complete_archive_metadata(plan,receipt,check_targets_live):
 archiveplan=meta(plan['inherited_complete_archive_plan_pin']);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==plan['actual_archive_complete_prefix']==archiveplan['complete_joint_roots']and plan['no_new_output_root']is True and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'complete original76 prefix, no cleanup data root or resource reset')
 need(plan['original_caps']==archiveplan['original_caps']==CAPS and plan['actual_archive_Root0_child0_complete']is True and plan['actual_archive_independent_post0_complete']is True,'actual single archive Root0/child0/independentpost0 prerequisite and original caps')
 cp = plan['actual_archive_closure_pins']
 host = meta(cp['Host'])
 raw = meta(cp['Root_tools'])
 child = meta(cp['child_report'])
 index = meta(cp['index'])
 post = meta(cp['post'])
 posttools = meta(cp['post_tools'])
 genuine(raw, 'actual_terminal_return', cp['Host'], 'report_pin')
 genuine(posttools, 'actual_review_return', cp['post'], 'review_pin')
 need(raw['actual_execution_permission_mode'] == 'require_escalated' and raw['actual_retried'] is False and (host['schema'] == 'ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1') and (host['status'] == 'ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED') and (host['failure'] is None) and (host['archive_complete'] is True) and (host['final_report_resource_check_passed'] is True) and (host['original_caps'] == plan['original_caps']) and (host['complete_joint_roots'] == roots) and (host['binding_pin'] == plan['inherited_complete_archive_plan_pin']) and (len(host['records']) == 1) and (host['records'][0]['status'] == 'PASS') and (host['actual_child_receipt']['report_pin'] == cp['child_report']) and (host['all1_original_plain_current7_retained'] is True), 'actual single-presence archive Root0 and one complete guarded child report')
 watch = host['actual_watchdog']
 need(type(watch['returncode']) is int and watch['returncode'] == 0 and (watch['limit_failure'] is None) and (watch['rss_cap_mib'] == 512) and (watch['own_child_only'] is True) and (watch['liveness_group_cleanup'] is True) and (0 <= watch['sampled_peak_rss_mib'] < 512) and (0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= 600), 'real original private OwnRSS one-child archive0 guard')
 need(child['schema'] == 'ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1' and child['status'] == 'SINGLE_BAGG_PRESENCE_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED' and (child['failure'] is None) and (child['completed_count'] == 1) and (child['all1_original_plain_current7_retained'] is True) and (child['index_pin'] == cp['index']) and (child['binding_pin'] == plan['inherited_complete_archive_plan_pin']), 'complete single-presence child0 proof')
 targets = plan['exact_target_pins']
 rows = index['entries']
 original = archiveplan['actual_presence_original_pin']
 need(len(targets) == len({p['path'] for p in targets}) == 1 and targets == archiveplan['all1_plain_pins'] == [original] and (original['path'] == plan['exact_presence_original_path']) and (original['sha256'] == '9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7') and (original['size_bytes'] == 169615994 == plan['planned_released_bytes'] == plan['target_total_bytes']), 'only exact complete presence original, never other aggregate output or native role')
 need(index['schema'] == 'CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1' and index['status'] == 'SINGLE_BAGG_PRESENCE_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED' and (index['binding_pin'] == plan['inherited_complete_archive_plan_pin']) and (len(rows) == 1) and (index['ordered_original_plain_count'] == 1) and (index['ordered_original_plain_total_bytes'] == 169615994) and (index['all1_original_plain_retained'] is True) and (index['future_consumer_must_use_exact_single_presence_archive_mapping'] is True) and (index['generic_missing_path_skip_authorized'] is False), 'actual exact ordered index1, generic absent-path skip never authorized')
 row = rows[0]
 need(row['ordinal'] == 0 and row['original_plain_full_pin'] == original and (row['compression_input_SHA'] == row['streamed_decompressed_SHA'] == original['sha256']) and (row['compression_input_length'] == row['streamed_decompressed_length'] == original['size_bytes']) and (row['exact_original_plain_bytes_recoverable'] is True) and (row['original_plain_preserved'] is True) and (row['actual_Bagg_output_role'] == 'COMPLETE_PRESENCE_BRANCH_AND_MISSING_LEDGER'), 'complete original/compressed/decompressed SHA-length proof metadata')
 entry = meta(row['entry_pin'])
 need(entry == {k: v for k, v in row.items() if k != 'entry_pin'} and entry['original_plain_preserved'] is True, 'exact entry creation metadata and original-preserved history retained unchanged')
 archivepins = [row['compressed_archive_full_pin']]
 entrypins = [row['entry_pin']]
 need(archivepins == plan['retained_presence_gzip_pins'] and entrypins == plan['retained_presence_entry_pins'], 'single exact complete archive and entry permanently retained')
 projection = plan['actual_archive_post_key_projection']
 need(post['schema'] == projection['schema'] and post['status'] == projection['status'] and (post['failure'] is None) and (post['metadata_only'] is True) and (post['actual_Host_report_pin'] == cp['Host']) and (post['actual_Root_tools_pin'] == cp['Root_tools']) and (post['actual_archive_index_pin'] == cp['index']) and (post['actual_child_report_pin'] == cp['child_report']) and (post['execution_binding_pin'] == plan['inherited_complete_archive_plan_pin']) and (post['original_presence_full_pin'] == original) and (post['compressed_presence_archive_full_pin'] == archivepins[0]) and (post['presence_entry_pin'] == entrypins[0]) and (post['complete_joint_roots'] == roots), 'actual independent single-presence archive metadata post0 exact scope')
 need(type(post['actual_Root_integer_exit_code']) is int and post['actual_Root_integer_exit_code'] == 0 and (type(post['actual_child_integer_exit_code']) is int) and (post['actual_child_integer_exit_code'] == 0) and (post['Root_actual_streamed_decompression_proof_matched_original_fullPF'] is True) and (post['original_presence_current7_verified_twice_only'] is True) and (post['compressed_presence_fullEOF_SHA_current7_verified_twice'] is True), 'independent actual Root0/child0 complete byte-proof facts; no future successful post inferred')
 prior = meta(archiveplan['latest_complete_plan_pin'])
 life = prior['exact_B4_product_lifecycle_binding']
 need(plan['retained_Bagg_output_current7_pins'] == archiveplan['retained_Bagg_output_current7_pins'] and len(plan['retained_Bagg_output_current7_pins']) == 16 and (original not in plan['retained_Bagg_output_current7_pins']) and (plan['retained_native_current7_pins'] == archiveplan['retained_native_current7_pins']) and (plan['retained_current7_pins'] == archiveplan['retained_current7_pins']) and (archiveplan['retained_native_current7_pins'] == life['ordered_exact4_current_archive_pins'] + life['ordered_exact4_current_entry_pins'] + [life['complete4_archive']['index_pin']] + prior['prospective_worker_live_input_pins']), 'all sixteen other Bagg outputs, original full8pairs/55contexts inputs and B4 all4 gzip/entries/index exact retained')
 bridge = meta(archiveplan['actual_current_epoch_B2_bridge_report_pin'])
 bridgetools = meta(archiveplan['actual_current_epoch_B2_bridge_tools_pin'])
 genuine(bridgetools, 'actual_terminal_return', archiveplan['actual_current_epoch_B2_bridge_report_pin'], 'report_pin')
 need(bridge['schema'] == 'ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1' and bridge['status'] == 'PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY' and (bridge['failure'] is None) and (bridge['complete_joint_roots'] == archiveplan['inherited_latest_complete_joint_roots']) and (bridge['original_caps'] == plan['original_caps']) and (bridge['final_report_resource_check_passed'] is True) and (len(bridge['ordered_role_pairs']) == 9) and (plan['retained_B2_current_epoch_readonly_pins'] == [r['current_epoch_full_pin'] for r in bridge['ordered_role_pairs']]), 'exact nine independently bridged historical readonly roles retained, never deleted or recertified as all4790')
 for r in bridge['ordered_role_pairs']:
     need(r['blind_complete_SHA_and_length_equal'] is True and r['before_open_EOF_after_current7_stable'] is True and (r['current_epoch_full_pin']['sha256'] == r['historical_full_pin']['sha256']) and (r['current_epoch_full_pin']['size_bytes'] == r['historical_full_pin']['size_bytes']), 'genuine recorded bridge equality preserved; no repeated large-body read')
     current(r['current_epoch_full_pin'])
 need(receipt['exact_target_pins']==targets and receipt['actual_archive_closure_pins']==cp and receipt['compressed_result_full_pins']==archivepins and receipt['retained_presence_entry_pins']==entrypins and receipt['original_lookup_index_pin']==cp['index']and receipt['historical_original_PFs_not_current_relabelled']is True and receipt['future_consumer_must_use_exact_single_presence_archive_mapping']is True and receipt['generic_missing_path_skip_authorized']is False and receipt['exact_presence_complete_result_bytes_preserved_in_archive']is True,'one complete archive and exact1 retirement map preserved without generic missing-path skips')
 for k in('retained_Bagg_output_current7_pins','retained_native_current7_pins','retained_current7_pins','retained_B2_current_epoch_readonly_pins','retained_archive_metadata_current7_pins'):need(receipt[k]==plan[k],'same full retainer tables in real receipt and frozen plan')
 ph=meta(archiveplan['actual_Bagg_Host_report_pin']);pt=meta(archiveplan['actual_Bagg_Root_tools_pin']);genuine(pt,'actual_terminal_return',archiveplan['actual_Bagg_Host_report_pin'],'report_pin');need(ph['status']=='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EVIDENCE_CHILD2_CLOSED_ONLY'and ph['failure']is None and type(ph['actual_child_integer_exit_code'])is int and ph['actual_child_integer_exit_code']==2 and ph['records'][0]['status']=='FAILED'and ph['records'][0]['error']==ph['original_runner_error']=='own-child stage failed; no retry'and post['actual_Bagg_originalRoot0_and_engineering_child2_FAILED_retained']is True,'original Bagg Root0/engineeringchild2/FAILED/error retained as historical evidence')
 retained=plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+archivepins+entrypins+[cp['index']]+plan['retained_B2_current_epoch_readonly_pins'];need(not{p['path']for p in targets}&{p['path']for p in retained+plan['explicit_cumulative_metadata_file_pins']},'exact1 target excludes every native/other16 Bagg/cold9/archive/entry/index/document retainer')
 for _ in range(2):
  if check_targets_live:
   for p in targets:current(p)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact presence path absent, immutable original fullPF is historical')
  for p in retained+plan['explicit_cumulative_metadata_file_pins']:current_role(p,build)
 return roots,targets,archivepins,entrypins,cp,None,post
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('execution-receipt-pin','Root-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable single execution post')
 pReceipt=json.loads(a.execution_receipt_pin);pTools=json.loads(a.Root_tools_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];receipt=None if pReceipt is None else meta(pReceipt)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed execution Root integer; no live handle inference')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');author=meta(author_pin);pp=author['whole_plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];ps=next(p for p in author['whole_Source_file_pins']if p['path']==str(PACKAGE/'retire_exact1_archived_Bagg_presence.UNREADY.py'))
 need(source_limit==16*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and plan['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS,'same frozen presence_exact1 Source/PLAN and unchanged original caps/Source16MiB')
 if pReceipt is not None:need(pReceipt['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and receipt['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['source_pin']==ps and receipt['plan_pin']==pp,'actual exact owning execution receipt/schema/mode and Source/plan')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_BAGG_PRESENCE_EXACT1_EXECUTION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=code,actual_receipt_status=None if receipt is None else receipt['status'],actual_receipt_failure=None if receipt is None else receipt['failure'],actual_released_pins=None if receipt is None else receipt['actual_released_pins'],actual_released_bytes=None if receipt is None else receipt['actual_released_bytes'],files_deleted=None if receipt is None else receipt['files_deleted'],source_pin=ps,plan_pin=pp,full_presence_exact1_retirement_success_inferred=False)
  save(result,source_limit);return
 need(receipt is not None,'actual execution Root0 requires emitted exact receipt PF');genuine(tools,'actual_terminal_return',pReceipt,'receipt_pin')
 need(tools['actual_execution_permission_mode']=='require_escalated'and receipt['status']=='RETIRED_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['files_deleted']is True and receipt['all_complete_result_bytes_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True,'actual presence_exact1 execution Root0/retirement/no lost complete result bytes/fresh original resource closure')
 targets=plan['exact_target_pins'];released=receipt['actual_released_pins'];releasedbytes=receipt['actual_released_bytes'];expectedbytes=sum(p['size_bytes']for p in targets)
 need(receipt['exact_target_pins']==released==targets and len(targets)==len({p['path']for p in targets})==1 and type(releasedbytes)is int and releasedbytes==expectedbytes==plan['target_total_bytes']==plan['planned_released_bytes']and json.loads(terminal['output'].strip().splitlines()[-1])['actual_released_bytes']==releasedbytes,'actual precisely ordered one presence fullPF target and exact bytes in receipt/genuine stdout')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only genuinely deleted exact target paths absent; historical fullPF never relabelled current')
 cli_pin=pin(PACKAGE/'ROOT_EXECUTE_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='execute'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'actual exact published execute CLI and same Source/plan/peer identities')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent Source review0 for same exact worker/plan')
 readonly_pin=receipt['actual_readonly_receipt_pin'];readonly_tools_pin=receipt['actual_readonly_tools_pin'];readonly_post_pin=receipt['actual_readonly_post_pin'];readonly_post_tools_pin=receipt['actual_readonly_post_tools_pin']
 need(cli['actual_readonly_receipt_pin']==readonly_pin and cli['actual_readonly_tools_pin']==readonly_tools_pin and cli['actual_readonly_post_pin']==readonly_post_pin and cli['actual_readonly_post_tools_pin']==readonly_post_tools_pin,'actual execute CLI/receipt consumes exact genuine readonly0/post0 PFs')
 readonly=meta(readonly_pin);readonly_tools=meta(readonly_tools_pin);readonly_post=meta(readonly_post_pin);readonly_post_tools=meta(readonly_post_tools_pin);genuine(readonly_tools,'actual_readonly_return',readonly_pin,'receipt_pin');genuine(readonly_post_tools,'actual_review_return',readonly_post_pin,'review_pin')
 need(readonly_pin['path']==str(PACKAGE/'READONLY_RECEIPT.json')and readonly_tools['actual_readonly_permission_mode']=='require_escalated'and readonly['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and readonly['mode']=='check'and readonly['status']=='READONLY_READY_CURRENT_BAGG_PRESENCE_EXACT1_ARCHIVED_ORIGINAL'and readonly['failure']is None and readonly['source_pin']==ps and readonly['plan_pin']==pp and readonly['exact_target_pins']==targets and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False and readonly['resources_after_original_classes_forced_fresh']is True,'actual earlier readonly Root0/no-unlink/fresh resource proof remains historical and unmodified')
 contract=plan['readonly_post_report_contract'];need(readonly_post['schema']==contract['schema']and readonly_post['status']==contract['status']and readonly_post['failure']is None and readonly_post['metadata_only']is True and readonly_post['actual_readonly_receipt_pin']==readonly_pin and readonly_post['actual_readonly_tools_pin']==readonly_tools_pin and readonly_post['source_pin']==ps and readonly_post['plan_pin']==pp and readonly_post['exact_target_pins']==targets and readonly_post['actual_released_pins']==[]and readonly_post['actual_released_bytes']==0 and readonly_post['files_deleted']is False and readonly_post['resources_after_original_classes_forced_fresh']is True and type(readonly_post['actual_readonly_Root_integer_exit_code'])is int and readonly_post['actual_readonly_Root_integer_exit_code']==0,'genuine independent readonly metadata post0 exact execution prerequisite, not self-reexecuted')
 lsof=receipt['actual_lsof_owner_check'];need(lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(lsof['returncode'])is int and lsof['returncode']==1 and lsof['stdout']==lsof['stderr']=='','actual saved original presence_exact1 lsof owner check1/empty only; lsof not repeated by post')
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,False)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved forced-fresh after original resource scans follow before scans, no fabricated final-unlink timestamp')
 need(receipt['exact_presence_complete_result_bytes_preserved_in_archive']is True and receipt['archive_lookup_required_for_future_consumer']is True,'single complete presence byte archive retained and exact archive lookup remains required')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'exact cleanup metadata cannot mint science/physical/goal qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current unchanged original cumulative/free reserve with post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin,readonly_pin,readonly_tools_pin,readonly_post_pin,readonly_post_tools_pin):full(p)
 result=dict(schema='CURRENT_BAGG_PRESENCE_EXACT1_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_BAGG_PRESENCE_EXACT1_RETIRED_COMPLETE_RESULT_BYTES_IN_ARCHIVE_METADATA_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=released,actual_released_bytes=releasedbytes,files_deleted=True,exact_one_target_absent_verified_twice=True,resources_after_original_classes_forced_fresh=True,actual_readonly_receipt_pin=readonly_pin,actual_readonly_tools_pin=readonly_tools_pin,actual_readonly_post_pin=readonly_post_pin,actual_readonly_post_tools_pin=readonly_post_tools_pin,actual_execute_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_saved_lsof_owner_check=lsof,retained_presence_gzip_pins=archives,retained_presence_entry_pins=entries,original_lookup_index_pin=archive_cp['index'],actual_archive_closure_pins=archive_cp,historical_retired_presence_full_pin=targets[0],historical_deleted_fullPF_not_claimed_current=True,retained_Bagg_output_current7_pins=plan['retained_Bagg_output_current7_pins'],retained_prior_native_input_and_gzip_entry_index_current7_pins=plan['retained_native_current7_pins'],retained_all_current7_pins=plan['retained_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],all_retained_roles_current7_verified_twice=True,original_Bagg_Root0_child2_FAILED_preserved=True,future_consumer_must_use_exact_single_presence_archive_mapping=True,generic_missing_path_skip_authorized=False,exact_presence_complete_result_bytes_preserved_in_archive=True,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

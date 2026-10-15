"""UNREADY independent metadata post for an actual single complete Bagg presence byte archive.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. New compressed outputs are blindly hashed; no original payload read, repeat decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_Bagg_single_presence_lossless_archive_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '1a3e71bb930dbb225dbe2b399054708663c0ba0523ecbb6c8714b177fec75fc0', 'size_bytes': 6690, 'identity': [16777229, 50880237, 33188, 1, 6690, 1792064771127114025, 1792064771127114025]}
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
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh single presence archive output')
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
KNOWN_BRIDGE_POST_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmB2_epoch_bridge_source_v1_UNREADY/actual_postverify_20261015/REVIEW.json', 'sha256': 'a8b007cc6975d85539884d47e7d44ce429478f904fc13fec2cfbb6cde97fd69e', 'size_bytes': 526989, 'identity': [16777229, 50880600, 33188, 1, 526989, 1792065158959771817, 1792065158959771817]}
KNOWN_BRIDGE_POST_TOOLS_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmB2_epoch_bridge_source_v1_UNREADY/actual_postverify_20261015/TRUE_TOOL_RETURNS.json', 'sha256': 'fb29d82c1933d77df4b76475a823462e3f8885d60ae0536fcb4b4821a09c0830', 'size_bytes': 3075, 'identity': [16777229, 50880604, 33188, 1, 3075, 1792065167596971527, 1792065167596971527]}
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor, immutable single actual metadata post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);root=meta(pRoot);host=None if pHost is None else meta(pHost);terminal=root['actual_terminal_return']
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==root['original_integer_exit_code']and terminal.get('session_id')is None and root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine original typed closed Root terminal, permission and no retry')
 pb=pin(PACKAGE/'PLAN.json')if host is None else host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];limit=b['bounded_total_output_bytes'];source_limit=b['bounded_Source_metadata_bytes'];code=root['original_integer_exit_code']
 need(b['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_BINDING_V1'and b['original_caps']==CAPS and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and limit==32*2**20 and b['bounded_archive_payload_bytes']==24*2**20 and b['metadata_runtime_headroom_bytes']==8*2**20 and source_limit==16*2**20 and roots[-1]==str(out),'actual single presence full32/24payload8meta/Source16 binding and original caps')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_single_Bagg_presence_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1','exact real owning single presence Host report role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins)
 if code!=0:
  observed=[]
  if host is not None and host['actual_watchdog']is not None:
   need(bool(host['records']),'record-label required for real failed watchdog');w=meta(table[str(out/(host['records'][-1]['label']+'.watchdog.json'))]);need(w==host['actual_watchdog']and type(w['returncode'])is int,'actual failed watchdog only');observed.append(w['returncode'])
  result=dict(schema='SINGLE_BAGG_PRESENCE_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_recorded_child_integer_exit_codes=observed,actual_stage_records=None if host is None else host['records'],absent_child_code_invented=False,archive_success_or_roundtrip_inferred=False,new_partial_output_blind_fullEOF_twice_pins=newpins,execution_binding_pin=pb)
  save(result,source_limit);return
 need(host is not None,'Root0 requires actual emitted Host PF');genuine(root,'actual_terminal_return',pHost,'report_pin')
 need(host['status']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and host['failure']is None and host['secondary_failures']==[]and host['archive_complete']is True and host['retries']==0 and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False and host['independent_archive_post0_required']is True and host['all1_original_plain_current7_retained']is True,'genuine Root0 complete one-file byte archive, original preserved and no retirement/physics qualification')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
 need(author['Source_only_frozen_before_Root_generation']is True and author['whole_Source_file_pins']==sf['complete_source_file_pins']and author['whole_original_archive_one_byte_stream_compression_and_decompression_proof_unchanged']is True and len(sf['complete_source_file_pins'])==5,'exact immutable five Source roles and original48 archive_one wholebytes')
 need(ready['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and sf['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_HOST_FREEZE_V1'and hf['source_only']is True and hf['selected_source_freeze_pin']==host['source_freeze_pin']and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and ready['complete_source_file_pins']==sf['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'same actual single presence READY/Source/Host publication')
 admission=meta(ready['Root_completed_admission_binding_pin']);template=meta(author['whole_NULL_admission_binding_template_pin']);mutable=set(author['Root_final_binding_fields_filled_after_genuine_bridge0']);need(set(admission)==set(template)and all(admission[k]==v for k,v in template.items()if k not in mutable)and all(b[k]==v for k,v in admission.items()),'only explicit future bridge gate fields filled by Root, whole remaining template and final admission retained')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin');need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_SINGLE_BAGG_PRESENCE_LOSSLESS_ARCHIVE'and peer['failure']is None and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'same-round genuine independent complete Source review0 and RootGEN0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin);need(root['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','real original Root CLI.command exact string, whole24argv and frozen Source identities')
 latest=meta(b['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==b['inherited_latest_complete_joint_roots']+[str(out)]and roots[:-1]==latest['complete_joint_roots']and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'whole dynamic then-latest75 plus owning archive76, Source stays counted')
 priorhost=meta(b['actual_Bagg_Host_report_pin']);priorchild=meta(b['actual_Bagg_child_report_pin']);priorpost=meta(b['actual_Bagg_post_pin']);priorroot=meta(b['actual_Bagg_Root_tools_pin']);priorpt=meta(b['actual_Bagg_post_tools_pin']);genuine(priorroot,'actual_terminal_return',b['actual_Bagg_Host_report_pin'],'report_pin');genuine(priorpt,'actual_review_return',b['actual_Bagg_post_pin'],'review_pin')
 need(priorhost['status']=='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EVIDENCE_CHILD2_CLOSED_ONLY'and priorhost['failure']is None and priorhost['actual_child_report_pin']==b['actual_Bagg_child_report_pin']and priorhost['records'][0]['status']=='FAILED'and priorhost['records'][0]['error']==priorhost['original_runner_error']=='own-child stage failed; no retry'and type(priorhost['actual_child_integer_exit_code'])is int and priorhost['actual_child_integer_exit_code']==2 and priorpost['actual_Host_report_pin']==b['actual_Bagg_Host_report_pin']and priorpost['actual_Root_tools_pin']==b['actual_Bagg_Root_tools_pin']and priorpost['actual_child_report_pin']==b['actual_Bagg_child_report_pin']and priorpost['actual_Root_integer_exit_code']==0 and priorpost['actual_child_integer_exit_code']==2,'original Bagg Root0/evidencechild2 and FAILED/error/post0 preserved')
 original=b['actual_presence_original_pin'];need(b['all1_plain_pins']==[original]and original['size_bytes']==b['original_plain_total_bytes']==169615994 and original['path']==str(Path(latest['planned_actual_output_root'])/'evidence/aggregate/B/all_presence_branch_and_missing.jsonl')and original in priorchild['states'][0]['complete_output_file_pins']and original in priorpost['all_new_output_blind_fullEOF_SHA_current7_twice_pins'],'one complete real presence target from immutable actual Bagg state output table, no truncation or subset')
 need(b['retained_Bagg_output_current7_pins']==[p for p in priorpost['all_new_output_blind_fullEOF_SHA_current7_twice_pins']if p!=original]and len(b['retained_Bagg_output_current7_pins'])==16 and original['path']not in{p['path']for p in b['retained_current7_pins']},'all other16 Bagg outputs retained separately from only future retirement candidate')
 bp=meta(b['actual_current_epoch_B2_bridge_report_pin']);bt=meta(b['actual_current_epoch_B2_bridge_tools_pin']);genuine(bt,'actual_terminal_return',b['actual_current_epoch_B2_bridge_report_pin'],'report_pin');bridgepost=meta(KNOWN_BRIDGE_POST_PIN);bridgept=meta(KNOWN_BRIDGE_POST_TOOLS_PIN);genuine(bridgept,'actual_review_return',KNOWN_BRIDGE_POST_PIN,'review_pin');need(bp['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and bp['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bp['failure']is None and bridgepost['actual_bridge_report_pin']==b['actual_current_epoch_B2_bridge_report_pin']and bridgepost['actual_Root_tools_pin']==b['actual_current_epoch_B2_bridge_tools_pin']and bridgepost['actual_Root_integer_exit_code']==0 and bridgepost['actual_child_integer_exit_code']is None and bridgepost['actual_children_started']==0 and bridgepost['metadata_only']is True and bridgepost['failure']is None,'actual bridge Root0 and independent post0, no bridge child0 invented')
 union={}
 for p in b['base_explicit_cumulative_metadata_file_pins']+bp['explicit_cumulative_metadata_file_pins']+[b['actual_current_epoch_B2_bridge_report_pin'],b['actual_current_epoch_B2_bridge_tools_pin']]:need(p['path']not in union or union[p['path']]==p,'one exact metadata fullPF per path');union[p['path']]=p
 need(b['explicit_cumulative_metadata_file_pins']==list(union.values())and bp['complete_joint_roots']==roots[:-1]and bp['original_caps']==CAPS,'all actual bridge external metadata included, no dropped oldHost or body-as-metadata reclassification')
 need(len(host['records'])==1 and host['records'][0]['status']=='PASS','one original guarded archive child0, no retry');record=host['records'][0];wp=table[str(out/(record['label']+'.watchdog.json'))];lp=table[str(out/(record['label']+'.log'))];w=meta(wp);need(w==host['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and lp['sha256']==record['log_sha256'],'genuine original record.label watchdog/log/RSS/wall/liveness child0')
 claim=meta(pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'));command=record['command'];need(len(command)==9 and command[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',str(PACKAGE/'archive_single_Bagg_presence.UNREADY.py'),'--binding-pin']and json.loads(command[4])==pb and command[5]=='--common-source-pin'and json.loads(command[6])==hf['common_source_pin']and command[7:]==['--expected-parent-pid',str(claim['PID'])],'actual original sole owning parent/child command and frozen binding/common')
 log=full(lp);need(lp['size_bytes']<8*2**20,'bounded child receipt metadata');lines=log.read_text().splitlines();need(len(lines)==1,'one complete child receipt without omitted warnings');receipt=json.loads(lines[0]);need(receipt==host['actual_child_receipt'],'same real Host/child receipt')
 childpin=receipt['report_pin'];child=meta(childpin);need(childpin['path']==str(out/'ACTUAL_SINGLE_BAGG_PRESENCE_LOSSLESS_ARCHIVE_REPORT.json')and child['schema']=='ACTUAL_CURRENT_BAGG_SINGLE_PRESENCE_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'and child['status']=='SINGLE_BAGG_PRESENCE_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'and child['failure']is None and child['completed_count']==1 and type(child['completed_count'])is int and child['binding_pin']==pb and child['all1_original_plain_current7_retained']is True and child['all_other_Bagg_outputs_and_native_and_inputs_current7_retained']is True,'complete one-file child byte-proof report, all other results retained')
 indexpin=child['index_pin'];index=meta(indexpin);need(indexpin['path']==str(out/'CURRENT_SINGLE_BAGG_PRESENCE_LOSSLESS_ARCHIVE_INDEX.json')and index['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and index['status']=='SINGLE_BAGG_PRESENCE_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINAL_RETAINED'and index['binding_pin']==pb and len(index['entries'])==index['ordered_original_plain_count']==1 and index['ordered_original_plain_total_bytes']==child['original_plain_total_bytes']==original['size_bytes']and index['compression_ratio_assumed']is False and index['all1_original_plain_retained']is True and index['requires_independent_post0_before_separate_plain_retirement']is True and index['future_consumer_must_use_exact_single_presence_archive_mapping']is True and index['generic_missing_path_skip_authorized']is False,'exact single full presence index and original byte length; future consumer mapping required')
 row=index['entries'][0];need(row['ordinal']==0 and type(row['ordinal'])is int and row['original_plain_full_pin']==original and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True and row['result_values_decoded']is False and row['scientific_values_decoded']is False and row['actual_Bagg_output_role']=='COMPLETE_PRESENCE_BRANCH_AND_MISSING_LEDGER'and row['filename_field']==''and row['mtime']==0 and row['compresslevel']==6,'actual Root-streamed complete input and decompressed SHA/length equal originalPF, without repeated decompression')
 pgz=row['compressed_archive_full_pin'];pe=row['entry_pin'];need(pgz['path']==str(out/'archives/000_all_presence_branch_and_missing.jsonl.gz')and table[pgz['path']]==pgz and pe['path']==str(out/'archive_entry_000.json')and table[pe['path']]==pe and meta(pe)=={k:v for k,v in row.items()if k!='entry_pin'},'complete gzip blindSHA2 and durable entry exactly equals index metadata')
 need(pgz['size_bytes']==index['total_gzip_bytes']==child['total_gzip_bytes']<b['bounded_archive_payload_bytes']and ownbytes<limit and {p['path']for p in newpins if Path(p['path']).suffix=='.gz'}=={pgz['path']},'all and only one complete new gzip under24MiB, whole own32MiB')
 childclaim=meta(table[str(out/'CHILD_ARCHIVE_CLAIM.json')]);need(childclaim['PID']==w['pid']and childclaim['parent_PID']==claim['PID']and childclaim['retries']==0,'actual sole child PID/owning Root and no retry')
 build=meta(b['original_guard_build_plan_pin'])
 for _ in range(2):
  current(original)
  for p in b['retained_current7_pins']:current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  for p in bp['ordered_role_pairs']:current(p['current_epoch_full_pin'])
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 archive_resources(child['resources_after'],roots,600);before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes'];need(existing+limit+source_limit<2*2**30 and before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'real prelaunch complete prefix/actual external metadata plus32 archive16 Source reservation fit original caps')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full cumulative/cold/free reserves include report and post metadata')
 for item in(host,child,index):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(item[key]is False,'complete byte archive cannot mint physics/native/retirement or goal qualifications')
 for p in[pHost,childpin,indexpin,wp,lp,pgz,pe]:need(table[p['path']]==p,'all new complete outputs blindSHA2 matched')
 result=dict(schema='RECORDED_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_SINGLE_BAGG_PRESENCE_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_ORIGINAL_RETAINED',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,actual_child_report_pin=childpin,actual_archive_index_pin=indexpin,execution_binding_pin=pb,original_presence_full_pin=original,compressed_presence_archive_full_pin=pgz,presence_entry_pin=pe,Root_actual_streamed_decompression_proof_matched_original_fullPF=True,original_presence_current7_verified_twice_only=True,compressed_presence_fullEOF_SHA_current7_verified_twice=True,all_retained_current7_verified_twice=True,actual_Bagg_originalRoot0_and_engineering_child2_FAILED_retained=True,actual_Bagg_Host_report_pin=b['actual_Bagg_Host_report_pin'],actual_Bagg_post_pin=b['actual_Bagg_post_pin'],actual_current_epoch_B2_bridge_report_pin=b['actual_current_epoch_B2_bridge_report_pin'],actual_current_epoch_B2_bridge_tools_pin=b['actual_current_epoch_B2_bridge_tools_pin'],actual_current_epoch_B2_bridge_post_pin=KNOWN_BRIDGE_POST_PIN,actual_current_epoch_B2_bridge_post_tools_pin=KNOWN_BRIDGE_POST_TOOLS_PIN,retained_Bagg_other16_output_current7_pins=b['retained_Bagg_output_current7_pins'],retained_prior_native_input_and_gzip_entry_index_current7_pins=b['retained_native_current7_pins'],retained_all_current7_pins=b['retained_current7_pins'],bridge9_cold_readonly_current7_pins=[p['current_epoch_full_pin']for p in bp['ordered_role_pairs']],actual_streamed_original_SHA=row['streamed_decompressed_SHA'],actual_streamed_original_length=row['streamed_decompressed_length'],actual_original_presence_bytes=original['size_bytes'],actual_gzip_bytes=pgz['size_bytes'],actual_entire_archive_output_bytes=ownbytes,actual_original_runner_record=record,actual_original_watchdog=w,actual_watchdog_pin=wp,actual_child_log_pin=lp,actual_index_entry_metadata=row,complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,actual_original_Host_resources_before=host['resources_before'],actual_original_Host_resources_after=host['resources_after'],actual_original_Host_resources_after_including_summary=host['resources_after_including_summary_bytes'],actual_original_child_resources_after=child['resources_after'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_CLI_pin=cli_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,future_consumer_must_use_exact_single_presence_archive_mapping=True,generic_missing_path_skip_authorized=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

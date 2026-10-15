"""UNREADY independent metadata post for actual complete B extraction.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Original Root0 / evidence child2 / FAILED are distinct facts.
The exact separate author core freeze is bound below; actual execution is still NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_complete_extract_host_source_v2_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '78f422143139f70b6f76308ece8ebe499ebdcde8d141abe1ec4fae6a086438e3', 'size_bytes': 12669, 'identity': [16777229, 50870597, 33188, 1, 12669, 1792058062956618374, 1792058062956618374]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,TRANC_semantics_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,B_OVERV_control_completed=False,B_six_phase_construction_completed=False,physics_qualified=False)
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
def saved_resources(v,roots,limit):
 h=v['original_history'];j=v['complete_joint']
 need(v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800 and v['entire_extract_output_bytes']<limit and j['resource_roots']==roots,'actual original SELF/wall/own-stage bound and whole current root scope')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history/cumulative/cold/metadata/free caps')
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
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'same independent executor and immutable once-only post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=meta(pRoot);host=None if pHost is None else meta(pHost);actual=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==raw['original_integer_exit_code']and actual.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'genuine observed closed Root integer and original permission/no retry')
 code=raw['original_integer_exit_code'];plan_pin=pin(PACKAGE/'PLAN.json')if host is None else host['control_plan_pin'];plan=meta(plan_pin);out=Path(plan['planned_actual_output_root']);roots=plan['complete_joint_roots'];limit=plan['bounded_new_extract_output_reservation_bytes'];source_limit=plan['bounded_new_Source_metadata_reservation_bytes']
 need(type(limit)is int and 0<limit<=512*2**20 and source_limit==16*2**20 and plan['original_caps']==CAPS,'stage hard bound read from actual plan, original full caps/Source16 retained')
 need(roots[-1]==str(out)and out.is_absolute(),'literal owning extraction root')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_current_B_complete_extract_summary.json')and host['schema']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_GUARDED_ROOT_REPORT_V1','actual emitted owning Host role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins)
 if code!=0:
  checks=[]
  if host is not None and host['actual_watchdog_full_pin']is not None:
   w=meta(host['actual_watchdog_full_pin']);need(w==host['actual_watchdog']and type(w['returncode'])is int,'only actually recorded child return retained');checks.append(w['returncode'])
  report=dict(schema='CURRENT_B_COMPLETE_EXTRACT_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_recorded_child_integer_exit_codes=checks,absent_child_code_invented=False,child_code_inferred_from_Root_return=False,new_partial_output_blind_fullEOF_twice_pins=newpins,complete_extraction_inferred=False,control_plan_pin=plan_pin)
  save(report,source_limit);return
 need(host is not None,'Root0 requires emitted actual Host report PF')
 genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(actual['output'].strip().splitlines()[-1])
 need(stdout['actual_child_evidence_only_integer_exit_code']==2 and type(stdout['actual_child_evidence_only_integer_exit_code'])is int and stdout['original_runner_FAILED_record_preserved']is True,'actual Root stdout preserves intentional child2 and original FAILED')
 need(host['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['operation']=='extract'and type(host['actual_child_integer_exit_code'])is int and host['actual_child_integer_exit_code']==2 and host['actual_intentional_exit2_normal_closure']is True and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True,'actual Root0 closure only, original worker2 evidence and guard retained')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);core_author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin);cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(core_author['Source_only_frozen_before_Root_generation']is True and core_author['whole_Source_file_pins']==sf['complete_source_file_pins']and core_author['all13_exact_whole_inverse_to_v1_verified']is True and core_author['original_2GiB_512MiB_RSS_600s_1800s_caps_and_math_unchanged']is True and core_author['actual_v1_Root1_child_minus15_wallcap_and_independent_failure_post0_bound']is True and core_author['current_extract_phase_output_hard_bound_bytes']==limit and core_author['Source_metadata_hard_bound_bytes']==source_limit,'same exact pre-GEN v2 author freeze; metadata throttle/new stricter phase bound only; original full extraction and v1 failure facts preserved')
 need(sf['schema']=='COMPLETE_CURRENT_B_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B_COMPLETE_EXTRACT_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==host['source_freeze_pin']and hf['source_only']is True and hf['decoder_executed']is False and sf['control_plan_pin']==plan_pin==ready['control_plan_pin']and sf['complete_source_file_pins']==ready['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['contract_Source_pin']==ready['contract_Source_pin']and hf['original_caps']==CAPS,'same exact author-frozen full Source/host/contract/control publication')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_EXTRACT'and peer['failure']is None and peer['control_plan_pin']==plan_pin and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'real same-round complete independent Source review0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 need(shlex.split(raw['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual original published24 argv and freeze PFs')
 latest=meta(plan['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(out)]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'entire dynamic latest prefix plus one owning stage; Source stays counted, no root ordinal substitution')
 request=meta(host['actual_execution_request_pin']);manifest=meta(host['actual_observation_manifest_pin']);binding=meta(host['current_B_case_input_binding_pin']);state=manifest['states']['B'];build=meta(plan['original_guard_build_plan_pin']);capture=meta(plan['actual_capture_Host_report_pin'])
 need(request['schema']=='CURRENT_B_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'and request['operation']=='extract'and request['state_order']==['B']and request['original_caps']==CAPS and request['complete_source_freeze_pin']==host['source_freeze_pin']and request['joint_archive_roots']==roots and request['output_directory']==str(out/'evidence/extract')and request['owning_host_output_directory']==str(out)and request['actual_observation_manifest_pin']==host['actual_observation_manifest_pin']==plan['actual_observation_manifest_pin']and request['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']==plan['current_B_case_input_binding_pin'],'exact child request/current original B binding/owning output')
 need(manifest['state_order']==['B']and set(manifest['states'])=={'B'}and manifest['actual_B_observation_executed']is True and manifest['actual_A_observation_executed']is False and manifest['library_copy_created']is False and state==dict(capture['actual_B_state'],actual_owning_report_pin=plan['actual_capture_Host_report_pin']),'genuine current B capture, no A relabelling')
 need(len(host['records'])==1,'one genuine extraction child, no retry');record=host['records'][0];w=host['actual_watchdog']
 need(record['status']=='FAILED'and record['error']==host['original_runner_error']=='own-child stage failed; no retry'and 'resource_after'not in record and type(w['returncode'])is int and w['returncode']==2 and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'original actual worker2/FAILED/error, absent resource_after, RSS/wall/liveness preserved')
 need(host['actual_watchdog_full_pin']['path']==str(out/(record['label']+'.watchdog.json'))and host['actual_log_full_pin']['path']==str(out/(record['label']+'.log'))and meta(host['actual_watchdog_full_pin'])==w,'original record.label watchdog/log and exact saved watchdog bytes')
 command=record['command'];claim=meta(pin(PACKAGE/'ROOT_EXECUTION_CLAIM_RECEIPT.json'))
 need(len(command)==10 and command[1:4]==['-B',str(PACKAGE/'current_B_material_lineage_evidence.UNREADY.py'),'extract']and command[4]=='--request-pin'and json.loads(command[5])==host['actual_execution_request_pin']and command[6:9]==['--output-dir',request['output_directory'],'--expected-parent-pid']and command[9]==str(claim['Root_PID']),'same exact actual extract request/sole owning Root parent command')
 logpath=full(host['actual_log_full_pin']);need(logpath.stat().st_size<8*2**20,'one bounded JSON receipt log');lines=logpath.read_text().splitlines();need(len(lines)==1,'one complete evidence receipt without omitted log lines');receipt=json.loads(lines[0]);need(receipt==host['actual_complete_child_receipt']and receipt['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2'and receipt['report']==host['actual_child_report_pin'],'actual sole child receipt binds exact child report')
 reportpin=host['actual_child_report_pin'];child=meta(reportpin)
 need(reportpin['path']==str(out/'evidence/extract/ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_REPORT.json')and child['schema']=='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'and child['status']=='ACTUAL_CURRENT_COMPLETE_CONTEXT_AND_RAW_SNAPSHOT_EVIDENCE_ONLY_EXIT2'and child['state_order']==['B']and set(child['states'])==set(child['context_states'])=={'B'}and child['current_case_spec_pin']==binding['current_case_spec_pin']and child['actual_observation_manifest_pin']==host['actual_observation_manifest_pin']and child['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']and child['original_caps']==CAPS and child['all_complete_state_scope_retained']is True and child['all_handles_closed_between_snapshots']is True and child['all_observed_native_tree_words_and_orders_preserved']is True and child['complete_aggregation_qualified']is False and child['complete_final_construction_qualified']is False and child['new_qualification_sha256']is None,'actual full extraction evidence report; no aggregation or scientific qualification')
 need(type(child['actual_child_PID'])is int and type(child['actual_parent_PID'])is int and child['actual_parent_PID']==claim['Root_PID'],'saved actual extraction PID/owning Root parent')
 events=child['context_states']['B'];snapshots=child['states']['B'];contexts=state['complete_context_pins'];observed=state['complete_state_snapshot_inputs'];headers=state['actual_all_event_headers_in_original_execution_order']
 need(len(events)==len(contexts)==len(headers)==55 and len(snapshots)==len(observed)==8 and [e['event']for e in events]==list(range(1,56))and [e['input']for e in events]==contexts,'all55 complete consecutive original contexts and all8 saved native trees')
 for e,h in zip(events,headers):
  need(all(e[k]==h[k]for k in('event','libmix','label'))and e['all_original_words_preserved']is True and e['old_XSM_extracted_here']is False and type(e['event'])is int and type(e['libmix'])is int,'original event identity/order and complete-word saved claims retained')
 need(events[-1]['label']=='TONDRV_FINAL_AFTER_SHIBA','complete actual final context retained')
 pairs=[];census=[];snapshot_pins=[]
 names={'complete_native_logical_record_inventory.jsonl','complete_native_original_path_index.sqlite','complete_native_original_value_bytes.bin','complete_native_physical_directory_slots.jsonl','complete_native_xsmnxt_export_record_order.jsonl'}
 for row,old in zip(snapshots,observed):
  need(row['state']=='B'and row['event']==old['event']and row['role']==old['role']and row['input_pin']==old['input_pin']and row['root_prefix']==old['logical_prefix']and row['all_original_types_counts_words_and_physical_API_orders_saved']is True and row['ASCII_used_or_invented']is False and row['original_RAM_bits_qualified']is False and row['new_qualification_sha256']is None,'all original saved tree input/role/order/type/word claims, no A counts or RAM qualification transplanted')
  need(all(type(row[k])is int and row[k]>0 for k in('complete_records','complete_directories','complete_extents')),'actual nonempty saved tree census retained')
  folder=out/'evidence/extract/B'/(str(row['event']).zfill(6)+'_'+row['role']);files=row['all_output_file_pins']
  need(len(files)==5 and {Path(p['path']).name for p in files}==names and all(Path(p['path']).parent==folder for p in files)and row['paired_SQLite_pin']in files and row['paired_original_pool_pin']in files and Path(row['paired_SQLite_pin']['path']).name=='complete_native_original_path_index.sqlite'and Path(row['paired_original_pool_pin']['path']).name=='complete_native_original_value_bytes.bin','all5 complete output artifacts for each of8 actual tree pairs')
  for p in files:need(table[p['path']]==p,'whole newly saved tree output PF matches independent blind SHA twice')
  snapshot_pins+=files;pairs.append(dict(event=row['event'],role=row['role'],root_prefix=row['root_prefix'],input_pin=row['input_pin'],sqlite_pin=row['paired_SQLite_pin'],native_pool_pin=row['paired_original_pool_pin']))
  census.append({k:row[k]for k in('state','event','role','root_prefix','complete_records','complete_directories','complete_extents','all_original_types_counts_words_and_physical_API_orders_saved')})
 need(pairs[-1]['role']=='final-complete-micro'and (out/'evidence/extract/B/all_context_words.jsonl').is_file(),'all context word ledger and actual final pair retained')
 for p in [pHost,reportpin,host['actual_execution_request_pin'],host['actual_watchdog_full_pin'],host['actual_log_full_pin']]+snapshot_pins:need(table[p['path']]==p,'all actual fresh extraction controls/whole output artifacts independently blind matched')
 need(child['complete_actual_observation_input_pins']==state['physical_input_pins']+state['complete_observed_file_pins'],'same complete original B physical/native context/tree input list and order')
 for _ in range(2):
  for p in host['fixed_current_pins']+request['complete_input_pins']:current_role(p,build)
  for p in hf['explicit_cumulative_metadata_file_pins']+plan['inherited_metadata_current7_pins']:current_role(p,build)
 need(ownbytes<limit,'entire complete extraction own output under actual plan hard bound')
 saved_resources(host['resources_before'],roots,limit);saved_resources(host['resources_after'],roots,limit)
 before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes'];reservation=host['actual_extract_only_stage_reservation']
 need(existing+limit+source_limit<2*2**30 and reservation==request['stage_reservation_binding']and reservation['complete_joint_roots']==roots and reservation['original_caps']==CAPS and reservation['stage_output_reservations']==dict(extract=limit)and reservation['new_Source_metadata_reservation_bytes']==source_limit and reservation['existing_measured_total_bytes']==existing and reservation['only_current_stage']=='extract'and reservation['future_full_aggregate_and_B_OVERV_deferred_not_reduced']is True,'actual complete extraction-only phase reservation read from plan, no reduced future scope or fixed ledger ordinal')
 joint=counted_bytes(roots);extra=0
 for p in hf['explicit_cumulative_metadata_file_pins']:
  if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
 unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original cumulative/free reserve including exact external metadata and own open-unlinked')
 for item in(host,child,receipt):
  for k in FALSE:
   if k in item:need(item[k]is False,'no unsupported native-RAM/reaction/physics/AAA/ABA qualification')
 need('issue_count'not in child and 'phase_results'not in child,'actual extraction has no synthetic aggregate issue count or six-phase result')
 report=dict(schema='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1',status='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Root_true_tool_return_pin=pRoot,actual_Host_report_pin=pHost,actual_extraction_host_pin=pHost,actual_extraction_report_pin=reportpin,actual_observation_manifest_pin=host['actual_observation_manifest_pin'],current_B_case_input_binding_pin=host['current_B_case_input_binding_pin'],actual_Root_integer_exit_code=0,actual_child_integer_exit_code=2,actual_original_failed_record_preserved=True,actual_record_resource_after_absent_preserved=True,actual_stage_record=record,actual_original_runner_error=host['original_runner_error'],actual_intentional_exit2_normal_closure=True,actual_stage_watchdog_pin=host['actual_watchdog_full_pin'],actual_stage_log_pin=host['actual_log_full_pin'],actual_stage_watchdog=w,all_snapshot_pairs=pairs,complete_context_pins=contexts,all_original_snapshot_and_context_pins_verified=True,actual_context_pin_count=55,actual_snapshot_pair_count=8,actual_context_event_order_complete_1_through55=True,actual_contexts_and_snapshot_original_input_pin_order_preserved=True,actual_snapshot_census=census,actual_complete_output_full_EOF_twice_pins=newpins,actual_new_output_logical_bytes=ownbytes,actual_new_output_pin_count=len(newpins),actual_stage_hard_output_bound_from_plan_bytes=limit,actual_Source_metadata_bound_from_plan_bytes=source_limit,actual_complete_aggregation_qualified=False,actual_complete_final_construction_qualified=False,extract_has_no_issue_count_or_phase_result_field=True,aggregation_and_B_OVERV_not_executed_or_qualified=True,old_SOURCE_CONTEXT_NOT_SAVED_history_not_deleted_or_relabelled=True,current_complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,original_host_resources_before=host['resources_before'],original_host_resources_after=host['resources_after'],control_plan_pin=plan_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_execution_request_pin=host['actual_execution_request_pin'],actual_published_CLI_pin=cli_pin,actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE)
 save(report,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()

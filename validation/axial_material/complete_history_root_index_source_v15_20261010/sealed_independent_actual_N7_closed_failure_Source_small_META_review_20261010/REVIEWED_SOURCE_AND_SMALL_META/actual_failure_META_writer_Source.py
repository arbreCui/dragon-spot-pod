import hashlib,json,os,stat,time
from pathlib import Path

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
H=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-host-20261010'
O=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-runtime-20261010'
C=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-control-20261010'
D=B/'actual_complete_native_observation_BUILD5_AB_v7_sources'
E=B/'actual_complete_native_observation_BUILD5_AB_v7_receipts'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
started=time.monotonic()
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,tool=False):
 i=identity(p);assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2]) and ((i[3]>=1) if tool else (i[3]==1))
 with p.open('rb') as f:
  h=hashlib.sha256()
  while True:
   assert time.monotonic()-started<600
   raw=f.read(2**20)
   if not raw:break
   h.update(raw)
 assert identity(p)==i
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=i[4],identity=i)
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def load(p):
 q=pin(p);v=strict(p.read_bytes());assert pin(p)==q;return v,q
def tree(p):
 assert p.is_dir() and p.resolve()==p
 files=[];dirs={};seen=set()
 for q in [p,*sorted(p.rglob('*'))]:
  i=identity(q);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(q)]=i
  else:
   assert (i[0],i[1]) not in seen;seen.add((i[0],i[1]));files.append(pin(q))
 return dict(root=str(p),files=files,directory_identity=dirs,total_bytes=sum(q['size_bytes'] for q in files))
def main():
 import sys
 assert len(sys.argv)==1 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
 terminal,tp=load(H/'Root_actual_complete_observation_tool_terminal_return.json');tr=terminal['terminal_tool_return']
 assert terminal['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1' and terminal['closed'] is True and terminal['observed_terminal'] is True and terminal['session_repolled_after_close'] is False and terminal['actual_terminal_chunk']==tr['chunk_id']=='d1b354' and type(tr['exit_code']) is int and tr['exit_code']==1 and 'session_id' not in tr
 freeze,fp=load(B/'Root_actual_N7_prelaunch_complete_D_E_Source_freeze.json');request,rp=load(E/'Root_actual_observation_build_binding_request.json');failed,hp=load(H/'failed_host_result.json')
 assert failed['schema']=='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1' and failed['status']=='FAILED_NO_RETRY_NO_QUALIFICATION' and failed['original_caps']==CAPS and all(type(v) is int for v in failed['original_caps'].values()) and failed['full_postfailure_freeze_errors']==[] and failed['full_postfailure_freeze_checked'] is True
 inputs=request['original129_input_pins']+request['additional_actual_evidence_input_pins']+list(request['actual_author_Source_contract'].values())
 assert len(inputs)==154 and failed['complete_input_pins_before']==failed['complete_input_pins_after_failure']==inputs
 tools={p['path'] for p in request['tool_pins'].values()}
 for q in inputs:assert pin(Path(q['path']),tool=q['path'] in tools)==q
 monitor=failed['actual_failure_only_monitor_evidence'];journal=H/'runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl';jp=pin(journal)
 assert jp==monitor['journal_pin'] and jp['size_bytes']<8*2**20
 events=[strict(line) for line in journal.read_bytes().splitlines()]
 assert len(events)==monitor['failure_event_count']==11 and [e['sequence'] for e in events]==list(range(1,12)) and all(e['schema']=='ACTUAL_N7_FAILURE_ONLY_MONITOR_EVENT_V1' for e in events) and monitor['additional_recording_errors']==[] and monitor['unpersisted_complete_events']==[] and monitor['complete_failed_event_journal_persistence_verified'] is True
 first=events[0];assert first['event']=='original_joint_bytes_failure' and first['original_ps']['actual_returncode']==0 and first['original_lsof']['actual_returncode']==1 and first['original_lsof']['streams_complete'] is True
 assert first['original_parent_chain_selected_PIDs']==[51052,51076,51077] and first['original_lsof']['actual_returned_argv']==['/usr/sbin/lsof','-nP','-F','pfnsiDt','-a','-p','51052,51076,51077'] and first['original_lsof']['actual_stderr']=='' and type(first['original_lsof']['actual_stdout']) is str
 headers=[int(line[1:]) for line in first['original_lsof']['actual_stdout'].splitlines() if line.startswith('p') and line[1:].isdigit()];assert headers==[51052,51077]
 cleanup=[e for e in events if e['event']=='original_terminate_group_exception'];assert len(cleanup)==1 and cleanup[0]['actual_cleanup_exception']['type']=='builtins.PermissionError' and cleanup[0]['actual_business_PID']==51076
 watch,wp=load(H/'native/Ganlib/src/compile_cle2000_c.watchdog.json');assert watch['pid']==51076 and watch['returncode']==0 and watch['limit_failure']=="ValueError('full live own process file scan required')"
 live,lp=load(B/'Root_actual_N7_closed_failure_current_process_group_liveness_diagnostic.json');assert live['actual_PS_returncode']==0 and live['current_target_groups_absent'] is True and live['actual_pid_ppid_pgid_matches']==[] and live['no_process_termination_attempted'] is True
 ns={k:tree(p) for k,p in dict(H=H,O=O,C=C,D=D,E=E).items()}
 assert ns['D']==freeze['complete_Source_D'] and ns['E']==freeze['complete_receipt_E'] and len(ns['D']['files'])==186 and len(ns['E']['files'])==5
 assert not any((p/name).exists() for p,name in [(H,'result.json'),(C,'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json'),(O,'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json')])
 for q in inputs:assert pin(Path(q['path']),tool=q['path'] in tools)==q
 assert pin(journal)==jp and pin(H/'failed_host_result.json')==hp and pin(H/'Root_actual_complete_observation_tool_terminal_return.json')==tp
 assert {k:tree(p) for k,p in dict(H=H,O=O,C=C,D=D,E=E).items()}==ns
 manifest=B/'Root_actual_N7_closed_failure_complete_HOCDE_namespace_manifest.json';summary=B/'Root_actual_N7_closed_failure_complete_summary.json';assert not manifest.exists() and not summary.exists()
 mv=dict(schema='ROOT_ACTUAL_N7_CLOSED_FAILURE_COMPLETE_HOCDE_NAMESPACE_MANIFEST_V1',status='ACTUAL_FAILED_NATIVE_DIAGNOSTIC_NAMESPACE_EVIDENCE_ONLY',actual_complete_namespace_views=ns,complete_ordered_protected_inputs=inputs,Root_postclose_full_EOF_all154_inputs_unchanged=True,complete_D_E_source_freeze_unchanged=True,current_closed_failure_groups_absent_evidence_pin=lp,actual_Root_closed_terminal_pin=tp,actual_failed_host_result_pin=hp,actual_failure_journal_pin=jp,original_caps=CAPS,new_runtime_or_native_or_scientific_qualification=False)
 manifest.write_text(json.dumps(mv,indent=2,allow_nan=False)+'\n')
 value=dict(schema='ROOT_ACTUAL_N7_CLOSED_FAILURE_COMPLETE_SUMMARY_V1',status='ACTUAL_NATIVE_DIAGNOSTIC_FAILED_CLOSED_NO_RETRY_NO_QUALIFICATION',actual_Root_terminal_chunk='d1b354',actual_Root_terminal_exit_code=1,actual_Root_terminal_pin=tp,actual_failed_host_result_pin=hp,actual_prelaunch_D_E_freeze_pin=fp,actual_request_pin=rp,actual_complete_failure_namespace_manifest_pin=pin(manifest),complete_D_E_source_freeze_unchanged=True,Root_postclose_full_EOF_all154_inputs_unchanged=True,Root_postclose_revalidation_does_not_replace_original_runtime_failed_monitor=True,actual_failure_journal_pin=jp,actual_failure_journal_rows=11,original_failure_event=dict(actual_PS_returncode=0,actual_PS_selected_PIDs=first['original_parent_chain_selected_PIDs'],actual_lsof_returncode=1,actual_lsof_observed_PID_headers=headers,actual_selected_PIDs_without_lsof_header=[51076],actual_lsof_stderr='',actual_lsof_stdout_UTF8_bytes=len(first['original_lsof']['actual_stdout'].encode()),original_lsof_streams_complete=True),actual_cleanup_error=cleanup[0]['actual_cleanup_exception'],actual_business_compiler_PID=51076,actual_genuine_watchdog_pin=wp,actual_genuine_watchdog=watch,watchdog_elapsed_includes_added_failure_diagnostics_and_cleanup=True,sampled_RSS_zero_is_early_exit_not_native_RSS_qualification=True,actual_host_whole_seconds=failed['whole_seconds'],actual_current_group_liveness_evidence_pin=lp,current_closed_failure_groups_absent=True,original_cleanup_success_not_backfilled=True,original_N6_failed_lsof_raw_and_cause_remain_unknown=True,closed_compiler_process_state_at_original_scan_unknown=True,regular_complete_HOCDE_bytes_after_Root_terminal=sum(v['total_bytes'] for v in ns.values()),failed_original_scan_open_unlinked_bytes_unknown=True,regular_only_snapshot_does_not_repair_failed_resource_gate=True,original_caps=CAPS,whole_five_stage_build_executed=False,actual_AB_observation_manifest_saved=False,new_instrumented_guard_controls_actual=None,native_RSS_verified=False,native_build_qualified=False,complete_context_aggregation_qualified=False,physical_neutron_balance_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,failure_META_writer_pin=pin(Path(__file__)))
 summary.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
 print(json.dumps(dict(status=value['status'],summary_pin=pin(summary),complete_namespace_manifest_pin=pin(manifest),failure_journal_pin=jp,regular_complete_HOCDE_bytes_after_Root_terminal=value['regular_complete_HOCDE_bytes_after_Root_terminal'],complete_D_E_source_freeze_unchanged=True,Root_postclose_full_EOF_all154_inputs_unchanged=True,scientific_qualification_created=False),allow_nan=False))
if __name__=='__main__':main()

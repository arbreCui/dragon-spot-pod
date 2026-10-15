import ast,hashlib,json,math,os,stat
from pathlib import Path
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_native_observation_BUILD5_AB_v6_sources';E=B/'actual_complete_native_observation_BUILD5_AB_v6_receipts'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v6-host-20261010')
O=H.parent/'axial-material-complete-native-observation-BUILD5-AB-v6-runtime-20261010';C=H.parent/'axial-material-complete-native-observation-BUILD5-AB-v6-control-20261010'
F=Path('/private/tmp/axmat_N6_actual_closed_failure_small_META_LIFTx6');PRE=Path('/private/tmp/axmat_N6_actual_bound_Source_prelaunch_hu7F0X/REVIEW.json')
checks=[];blockers=[];pins={};copies={}
def check(name,v):
 assert type(name)is str and name and name not in{c['check']for c in checks}and type(v)is bool
 checks.append(dict(check=name,passed=v))
 if not v:blockers.append(name)
def ident(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=ident(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
 assert ident(p)==i;q=dict(path=str(p),sha256=sha,size_bytes=i[4],identity=i);assert str(p)not in pins or pins[str(p)]==q;pins[str(p)]=q;return q
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def load(p):
 q=pin(p);v=strict(Path(p).read_bytes());assert pin(p)==q;return v
def source(p):
 q=pin(p);v=Path(p).read_text();assert pin(p)==q;ast.parse(v,filename=str(p));return v
def metadata_view(root):
 files=[];dirs={}
 for p in [root,*sorted(root.rglob('*'))]:
  i=ident(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p)]=i
  else:assert stat.S_ISREG(i[2])and i[3]==1;files.append(dict(path=str(p),size_bytes=i[4],identity=i))
 return dict(files=files,directories=dirs)
def identity_only(view):return dict(files=[{k:q[k]for k in('path','size_bytes','identity')}for q in view['files']],directories=view['directories'])
def retained(p,name):
 q=pin(p);dst=F/'FINITE_SAVED_SOURCE_AND_META'/name
 with Path(p).open('rb')as a,dst.open('xb')as b:
  while raw:=a.read(2**20):b.write(raw)
 z=pin(dst);assert pin(p)==q and(z['sha256'],z['size_bytes'])==(q['sha256'],q['size_bytes']);copies[name]=dict(actual_original_pin=q,retained_whole_byte_copy_pin=z)
before=dict(D=metadata_view(D),E=metadata_view(E))
pre=load(PRE);prepin=pin(PRE);check('actual prelaunch Source review SHA and PASS',prepin['sha256']=='c838e3f7daf8f8b905c4a674ea612d380fc9de63b6c1ce28f3438094566d715b'and pre['schema']=='INDEPENDENT_ACTUAL_N6_BOUND_SOURCE_META_PRELAUNCH_REVIEW_V1'and pre['status']=='PASS_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE'and pre['source_only']is True and pre['all_checks_passed']is True and pre['blockers']==[])
failure_path=H/'failed_host_result.json';terminal_path=H/'Root_actual_complete_observation_tool_terminal_return.json';watch_path=H/'native/Ganlib/src/compile_cle2000_c.watchdog.json';stage_path=H/'OBSERVATION_BUILD/stages.json';log_path=H/'native/Ganlib/src/compile_cle2000_c.log'
failure=load(failure_path);terminal=load(terminal_path);watch=load(watch_path);stages=load(stage_path);logpin=pin(log_path)
check('actual failed_host exact SHA and553486B',pin(failure_path)['sha256']=='01280181414adc67c718bba3b463a31f70b19428faaf80be73a51a2b24553096'and pin(failure_path)['size_bytes']==553486)
check('actual watchdog exact f8d8 and732B',pin(watch_path)['sha256']=='f8d8528703d8559b24cee3690743e0cfff706113134414a76f9b34fa2ec85222'and pin(watch_path)['size_bytes']==732)
tr=terminal['terminal_tool_return'];initial=terminal['initial_tool_return'];raw_trace=tr['output']
check('real Root terminal90feb8 exact CLOSED EXIT1',terminal['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1'and terminal['record_producer']=='root'and terminal['closed']is True and terminal['observed_terminal']is True and terminal['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==1 and 'session_id'not in tr and tr['chunk_id']==terminal['actual_terminal_chunk']=='90feb8')
check('actual original live7e927b session72452 then2saved observations only',initial['chunk_id']==terminal['actual_initial_chunk']=='7e927b'and type(initial['session_id'])is int and initial['session_id']==72452 and 'exit_code'not in initial and terminal['all_actual_tool_observations']==[initial,tr])
check('real failure traceback preserves initial ValueError and secondaryPermissionError',"ValueError: full live own process file scan required"in raw_trace and "During handling of the above exception"in raw_trace and "PermissionError: [Errno 1] Operation not permitted"in raw_trace and raw_trace.index('ValueError:')<raw_trace.index('PermissionError:')and 'os.killpg(pgid, signal.SIGTERM)'in raw_trace)
check('failed_host actual honest failure scope only',failure['schema']=='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1'and failure['status']=='FAILED_NO_RETRY_NO_QUALIFICATION'and failure['error']=="PermissionError(1, 'Operation not permitted')"and type(failure['whole_seconds'])in(int,float)and not isinstance(failure['whole_seconds'],bool)and math.isfinite(failure['whole_seconds'])and failure['whole_seconds']==4.421627125004306)
check('all154 saved beforeafter protected input pins unchanged',failure['complete_input_pins_before']==failure['complete_input_pins_after_failure']==pre['actual_ordered_protected_input_pins']and len(failure['complete_input_pins_before'])==154)
expected_freeze=dict(Source=pre['actual_namespace_pins']['D'],receipts=pre['actual_namespace_pins']['E'])
check('actual Root saved D157 E5 whole EOF freezes identicalprelaunch',failure['complete_D_E_freeze_before']==failure['complete_D_E_freeze_after_failure']==expected_freeze and failure['full_postfailure_freeze_errors']==[]and failure['full_postfailure_freeze_checked']is True)
for tag in ('D','E'):
 expected=pre['actual_namespace_pins'][tag];check(tag+' whole current complete namespace identity equals original fullEOF freeze',before[tag]==identity_only(expected))
 for q in expected['files']:check(tag+' current exact original file7ID '+q['path'],ident(Path(q['path']))==q['identity']and Path(q['path']).stat().st_size==q['size_bytes'])
 for p,i in expected['directories'].items():check(tag+' current original entire directory7ID '+p,ident(Path(p))==i)
records=failure['all_stage_records'];check('one recorded compile stage FAILED wholefive stage notcomplete',len(records)==1 and records[0]['status']=='FAILED'and records[0]['label']=='native/Ganlib/src/compile_cle2000_c'and stages['stages']==records)
record=records[0];check('actual same first C compile command saved bothrecordwatch',record['command']==watch['command']and record['command']==['/usr/bin/gcc','-Wall','-fPIC','-DLinux','-DUnix','-O','-g','-c',str(H/'native/Ganlib/src/cle2000_c.c'),'-o',str(H/'native/Ganlib/src/cle2000_c.o')])
check('actual compiler watchdog child47658return0 andfailedlimits',type(watch['pid'])is int and watch['pid']==47658 and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']=="ValueError('full live own process file scan required')"and watch['own_child_only']is True and watch['liveness_group_cleanup']is True)
check('watchdog original limits unchanged noRSSqualification',type(watch['rss_cap_mib'])is int and watch['rss_cap_mib']==512 and type(watch['sampled_peak_rss_mib'])in(int,float)and not isinstance(watch['sampled_peak_rss_mib'],bool)and watch['sampled_peak_rss_mib']==0.0 and type(watch['wall_cap_seconds'])in(int,float)and not isinstance(watch['wall_cap_seconds'],bool)and 0<watch['wall_cap_seconds']<=600)
runtime=source(D/'Root_bound_complete_observation_runtime.py');full=source(D/'GUARD_SOURCE/qualify_refined_AAA_layered_full.py');bounded=source(H/'runtime/run_bounded_dragon.py');prod=source(D/'GUARD_SOURCE/production_runner.py')
check('actual inherited original supervisorSource whole bytes current path',pin(Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py'))['sha256']==pin(D/'GUARD_SOURCE/qualify_refined_AAA_layered_full.py')['sha256'])
check('actual copied bounded guardSource whole bytes equal frozenoriginal',pin(H/'runtime/run_bounded_dragon.py')['sha256']==pin(D/'GUARD_SOURCE/run_bounded_dragon.py')['sha256'])
check('runtime strict live scan nonzero required raises before returned evidence',"observed=subprocess.run([lsof_tool,'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)"in runtime and "require(observed.returncode==0,'full live own process file scan required')"in runtime)
check('original _process terminate_group error can replace resourceValueError',"failure=repr(error);self.bounded.terminate_group(process);raise"in full and "self.resources.check();last_disk=now"in full)
check('original watchdog finally unconditionally wrote cleanupTrue',"finally:\n            self.bounded.finish_liveness_watchdog(write_fd,watchdog)"in full and "own_child_only=True,liveness_group_cleanup=True"in full)
check('original SIGTERM killpg PermissionError not caught atinitial termination',"os.killpg(pgid, signal.SIGTERM)\n    except ProcessLookupError:\n        return"in bounded and "terminate_process_group(process.pid, TERM_GRACE_SECONDS, process)\n    process.wait()"in bounded)
check('whole original serial stage reports FAILED on exception',"record['status'] ="not in prod and 'record["status"] = "FAIL_RESOURCE" if isinstance(error, ResourceFailure) else "FAILED"'in prod)
objects=[p for p in H.rglob('*.o')];archives=[p for p in H.rglob('*.a')];mods=[p for p in H.rglob('*.mod')]
check('actual one object metadata only no archives modules Dragonexe',objects==[H/'native/Ganlib/src/cle2000_c.o']and archives==[]and mods==[]and not os.path.lexists(H/'native/Dragon/src/Dragon'))
object_metadata=[dict(path=str(p),identity=ident(p),size_bytes=p.stat().st_size,body_read=False,Source_object_byte_or_executable_qualification_created=False)for p in objects]
check('actual O and C both complete empty no A B sharedlibrary',O.is_dir()and C.is_dir()and list(O.iterdir())==[]and list(C.iterdir())==[]and not os.path.lexists(O/'A')and not os.path.lexists(O/'B')and not os.path.lexists(O/'shared_input_libraries'))
check('actual no successful build capture products or observationmanifest',failure['actual_observation_manifest_pin_if_saved']is None and not os.path.lexists(C/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json')and not os.path.lexists(O/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json')and not os.path.lexists(H/'result.json'))
check('original terminal honest cleanupFalse materialFalse qualificationFalse',terminal['compiler_process_group_cleanup_verified']is False and terminal['actual_material_A_or_B_completed']is False and terminal['actual_new_scientific_qualification']is False)
future={k:failure[k]for k in('actual_runtime_qualification_sha256','actual_observer_native_controls_run','actual_native_Source_binary_linkage_qualification_sha256','actual_scientific_qualification_sha256','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','native_transport_executed','complete_context_aggregation_qualified')}
for k,v in future.items():check('failed_host no new qualification '+k,v is None if k.startswith('actual_')else v is False)
diag_path=B/'Root_actual_N6_closed_compiler_process_group_liveness_diagnostic.json';diag_tool_path=B/'Root_actual_N6_closed_compiler_process_group_liveness_tool_terminal_return.json';diag=load(diag_path);diagtool=load(diag_tool_path);dt=diagtool['actual_tool_return']
check('actual later process diagnostic truee27f6c CLOSED0',diagtool['schema']=='ROOT_ACTUAL_CLOSED_N6_COMPILER_PROCESS_GROUP_LIVENESS_TOOL_TERMINAL_RETURN_V1'and diagtool['record_producer']=='root'and diagtool['closed_tool_terminal_observed']is True and diagtool['closed_session_not_repolled']is True and type(dt['exit_code'])is int and dt['exit_code']==0 and 'session_id'not in dt and dt['chunk_id']=='e27f6c'and diagtool['actual_scientific_qualification']is False)
raw_diag,raw_saved=dt['output'].split('\nsaved ',1);check('actual later diagnostic rawstdout equals saved fullMETA',strict(raw_diag)==diag and raw_saved.strip()==str(diag_path))
check('actual current PID47658 andPGID matches absent exactPSshape',diag['schema']=='ROOT_ACTUAL_CLOSED_N6_COMPILER_PROCESS_GROUP_LIVENESS_DIAGNOSTIC_V1'and type(diag['actual_closed_compiler_pid'])is int and diag['actual_closed_compiler_pid']==47658 and type(diag['exact_pid_check']['returncode'])is int and diag['exact_pid_check']['returncode']==1 and diag['exact_pid_check']['stdout']==''and diag['exact_pid_check']['stderr']==''and type(diag['all_process_check']['returncode'])is int and diag['all_process_check']['returncode']==0 and diag['current_compiler_or_descendant_or_group_rows']==[]and diag['actual_current_process_group_absent']is True)
check('later absence cannot certify original cleanup or recover lsof',diag['kill_action_performed']is False and diag['original_failure_cleanup_success_inferred']is False and diag['original_failed_lsof_raw_output_recovered']is False and diag['native_or_scientific_qualification']is False)
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0);check('failed_host all original9 caps exact int',failure['original_caps']==caps and all(type(v)is int for v in failure['original_caps'].values()))
resource=failure['actual_resources_after_failure'];check('later saved postfailure resource snapshot scope original caps',type(resource['complete_joint_HOCDE_bytes'])is int and resource['complete_joint_HOCDE_bytes']==20243876 and type(resource['open_unlinked_bytes'])is int and resource['open_unlinked_bytes']==0 and resource['min_free_bytes']==8*2**30 and resource['artifact_budget_bytes']==96*2**30 and resource['all_regular_and_open_unlinked_counted']is True)
after=dict(D=metadata_view(D),E=metadata_view(E));check('whole current frozenD15722 E51 beforeafter thisreview identical',before==after and len(after['D']['files'])==157 and len(after['D']['directories'])==22 and len(after['E']['files'])==5 and len(after['E']['directories'])==1)
for path,q in list(pins.items()):check('all read Source smallMETA fullEOF unchanged '+path,pin(path)==q)
(F/'FINITE_SAVED_SOURCE_AND_META').mkdir()
for p,name in [(failure_path,'failed_host_result.json'),(terminal_path,'Root_actual_complete_observation_tool_terminal_return.json'),(watch_path,'compile_cle2000_c.watchdog.json'),(stage_path,'stages.json'),(log_path,'compile_cle2000_c.log'),(diag_path,diag_path.name),(diag_tool_path,diag_tool_path.name),(D/'Root_bound_complete_observation_runtime.py','Root_bound_complete_observation_runtime.py'),(D/'GUARD_SOURCE/qualify_refined_AAA_layered_full.py','original_qualify_refined_AAA_layered_full.py'),(H/'runtime/run_bounded_dragon.py','actual_original_run_bounded_dragon.py'),(D/'GUARD_SOURCE/production_runner.py','original_production_runner.py')]:retained(p,name)
assert metadata_view(D)==before['D']and metadata_view(E)==before['E']
report=dict(schema='INDEPENDENT_ACTUAL_CLOSED_N6_FAILURE_SOURCE_SMALL_META_REVIEW_V1',status='PASS_SAVED_FAILED_N6_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE'if not blockers else'BLOCKED_SAVED_FAILED_N6_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=not blockers,all_checks_typed_true=not blockers,blockers=blockers,actual_failed_host_result_pin=pin(failure_path),actual_Root_failure_terminal_pin=pin(terminal_path),actual_compile_watchdog_pin=pin(watch_path),actual_compile_stage_records_pin=pin(stage_path),actual_compile_log_pin=logpin,actual_prior_independent_prelaunch_report_pin=prepin,actual_source_namespace_full_pins_from_independent_prelaunch_and_actual_Root_failed_freezes=pre['actual_namespace_pins'],actual_current_namespace_metadata_before=before,actual_current_namespace_metadata_after=after,all_original157_D_and5_E_files_current7ID_and_entire_directory_freeze_preserved=True,original154_actual_input_saved_pin_lists_beforeafter_equal=True,original154_input_payloads_not_reread=True,Source_archive_payload_not_decoded_or_reread_in_this_failure_review=True,actual_failure_initial_chunk='7e927b',actual_original_live_session=72452,actual_failure_terminal_chunk='90feb8',actual_failure_terminal_exit_code=1,original_closed_session_never_repolled_here=True,actual_whole_failed_seconds=failure['whole_seconds'],actual_one_compiler_pid=47658,actual_one_compiler_returncode=0,actual_watchdog_limit_failure=watch['limit_failure'],actual_guard_stage_status='FAILED',all_five_complete_native_build_stages_passed=False,new_actual_executable_or_complete_native_link_qualification_created=False,actual_one_object_metadata_only=object_metadata,actual_native_object_payload_read=False,actual_material_A_started=False,actual_material_B_started=False,actual_material_A_or_B_completed=False,actual_original_failed_lsof_returncode=None,actual_original_failed_lsof_stdout=None,actual_original_failed_lsof_stderr=None,original_failed_lsof_output_not_saved_and_not_recovered=True,precise_reason_for_original_lsof_nonzero_not_established=True,original_watchdog_liveness_group_cleanup_metadata=True,original_watchdog_cleanup_true_is_unconditional_Source_field_not_success_proof=True,actual_original_compiler_process_group_cleanup_verified=False,actual_later_process_absence_diagnostic_pin=pin(diag_path),actual_later_process_absence_tool_receipt_pin=pin(diag_tool_path),actual_later_process_absence_terminal_chunk='e27f6c',actual_current_process_group_absent_at_saved_later_check=True,later_process_absence_does_not_requalify_original_cleanup=True,actual_original_caps=caps,actual_saved_postfailure_resource_joint_bytes=20243876,postfailure_resource_snapshot_does_not_qualify_failed_live_monitor=True,finite_whole_saved_Source_and_small_META_copies=copies,all_read_Source_small_META_pins=list(pins.values()),candidate_guard_API_native_compile_material_or_process_diagnostic_executed_by_reviewer=False,project_or_frozen_Source_namespaces_modified=False,scientific_qualification_created=False,**future)
out=F/'REVIEW.json'
with out.open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps(dict(source_only=True,review_pin=pin(out),check_count=len(checks),all_checks_passed=not blockers,blockers=blockers,actual_saved_root_failure_exit_code=1,actual_original_compiler_group_cleanup_verified=False,actual_saved_later_process_group_absent=True,candidate_guard_API_native_compile_material_or_diagnostic_executed_by_reviewer=False),allow_nan=False))

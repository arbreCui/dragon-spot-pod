"""Bounded stdlib SOURCE/saved-META failure audit. No candidate/API/guard/payload execution."""
import ast,hashlib,json,math,os,stat
from pathlib import Path
P=Path(__file__).parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_native_AB_persisted_XSM_ASCII_v22_sources'
E=B/'actual_complete_native_AB_persisted_XSM_ASCII_v22_receipts'
ART=Path('/Users/wen/spot/validation/artifacts')
H=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v22-20261010'
O=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-output-v22-20261010'
C=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v22-20261010'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CHECKS=[];PINS={}
def check(value,label):
 assert type(value)is bool and value,label
 CHECKS.append(dict(check=label,passed=True))
def identity(path):
 s=path.lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 path=Path(path);before=identity(path)
 check(path.is_absolute() and path.resolve()==path and stat.S_ISREG(before[2]) and before[3]==1,'ordinary complete input '+str(path))
 with path.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 check(identity(path)==before,'fullEOF sevenID stable '+str(path))
 q=dict(path=str(path),sha256=h,size_bytes=before[4],identity=before)
 if str(path)in PINS:check(PINS[str(path)]==q,'repeat complete pin unchanged '+str(path))
 PINS[str(path)]=q
 return q
def duplicate_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate metadata JSON key')
  d[k]=v
 return d
def reject_constant(x):raise ValueError('nonfinite metadata')
def read(path,sha=None):
 q=pin(path)
 if sha is not None:check(q['sha256']==sha,'exact saved SHA '+str(path))
 d=json.loads(Path(path).read_text(),object_pairs_hook=duplicate_pairs,parse_constant=reject_constant)
 check(pin(path)==q,'saved JSON pin unchanged '+str(path))
 return d,q
def expected_pin(q,label):
 got=pin(q['path'])
 check({k:got[k]for k in q}==q,label)
 return got
def view(root):
 if not os.path.lexists(root):return dict(root=str(root),present=False,files={},directories={},symlinks={})
 check(root.is_dir() and not root.is_symlink(),'ordinary reviewed namespace '+str(root))
 files={};dirs={'.':identity(root)}
 for p in sorted(root.rglob('*')):
  i=identity(p);check(not p.is_symlink(),'no namespace symlink '+str(p))
  key=str(p.relative_to(root))
  if stat.S_ISREG(i[2]):files[key]=pin(p)
  else:check(stat.S_ISDIR(i[2]),'no namespace special entry '+str(p));dirs[key]=i
 for k,q in dirs.items():check(identity(root/k)==q,'stable directory identity '+str(root/k))
 return dict(root=str(root),present=True,files=files,directories=dirs,symlinks={})
def bytes_in(views):return sum(q['size_bytes']for v in views for q in v['files'].values())
def write(name,value):
 with (P/name).open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
summary,sp=read(E/'Root_actual_complete_native_postclose_summary.json','2f464d12e72229451fe8203e3ca39b0e2a06a25a44022841ebcb26c432b2d94d')
receipt,rp=read(E/'Root_actual_complete_native_tool_terminal_return.json','dd6d7b78e8118006be63a745d6ec6f6afe9c802027ed582e06c9d2b11c6c5060')
ns,np=read(E/'Root_actual_complete_native_postclose_namespace_manifest.json','722c4f17d7c5212658a794e6d51fa13cfa90bc49590f7d69baf962d31f0507f8')
writer_return,wrp=read(E/'Root_actual_complete_native_postclose_META_writer_tool_return.json','dad973c0bede0a8e520f3006079169f781cdf71a3e6e43984f51ea6fd0be6e0b')
pre,pp=read(E/'Root_actual_native_prelaunch_frozen_D_E.json','4a8c84c2a867d2b492ad7afa5cfbe10651a19641059fcfca5b39eead38586c3f')
freeze,fp=read(E/'Root_complete_native_D_source_freeze.json')
pre_return,prp=read(E/'Root_actual_complete_native_prelaunch_tool_return.json')
watch,watchpin=read(H/'native_run/native_xsm_ascii.watchdog.json')
failed,failedpin=read(H/'failed_host_result.json')
stages,stagepin=read(H/'COMPLETE_NATIVE_XSM_ASCII/stages.json')
controls,controlpin=read(C/'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json')
logpin=pin(H/'native_run/native_xsm_ascii.log');log=(H/'native_run/native_xsm_ascii.log').read_text()
check(receipt['schema']=='ROOT_V22_ACTUAL_COMPLETE_NATIVE_TOOL_TERMINAL_RETURN_V1','real Root native terminal schema')
check(receipt['closed']is True and receipt['observed_terminal']is True and receipt['session_repolled_after_close']is False,'Root closed observed no repoll')
tr=receipt['terminal_tool_return'];initial=receipt['initial_tool_return']
check(type(tr['exit_code'])is int and tr['exit_code']==1 and 'session_id'not in tr,'actual strictint1 terminal/no live session')
check(receipt['actual_terminal_chunk']==tr['chunk_id']=='efc410','actual terminal chunk efc410')
check(initial==tr and receipt['original_session_id']is None and receipt['observations']==[],'one true immediate closed tool result, no observations invented')
check(receipt['merged_external_host_stdout_stderr_saved']is True and receipt['separate_external_host_stderr_saved']is False and receipt['independent_external_host_stderr_empty_verified']is False,'honest Root merged output scope')
check(receipt['native_checker_child_invoked']is True and receipt['complete_material_bits_verified']is False,'child invoked but complete bits not verified')
mergedpin=pin(E/'Root_actual_complete_native_merged_external_host_stdout_stderr.log')
check((E/'Root_actual_complete_native_merged_external_host_stdout_stderr.log').read_text()==tr['output'],'complete exact actual Root merged output retained')
check(summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_POSTCLOSE_SUMMARY_V1' and summary['status']=='ACTUAL_NATIVE_NONZERO_NO_RETRY_NO_QUALIFICATION','honest actual failure summary scope')
check(type(summary['actual_exit_code'])is int and summary['actual_exit_code']==1 and summary['closed']is True,'summary reflects actual strict1')
check(summary['actual_tool_receipt']==rp and summary['actual_prelaunch']==pp and summary['namespace_manifest']==np,'three real summary evidence pins exact')
check(summary['original_caps']==CAPS and pre['original_caps']==CAPS,'all unchanged original caps')
check(summary['native_persisted_XSM_value_bits_verified']is False and summary['all_complete_A_B_scopes_retained_and_verified']is False,'no successful complete A/B comparison inferred')
for key in ('original_XSM_memory_bits_verified','original_native_build_binary_Source_linkage_qualified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete','new_numeric_execution_by_writer','cleanup_performed'):
 check(summary[key]is False,'actual failure scope false '+key)
for key in ('actual_native_byte_qualification_sha256','new_native_walker_controls_actual_run','actual_child_report','actual_host_result'):
 check(summary[key]is None,'failure no qualification/report '+key)
check(summary['actual_failed_host_result']==failedpin and summary['actual_outer_watchdog']==watch,'real failed host and watchdog pins match')
check(summary['outer_tool_output_scope']=='ACTUAL_EXEC_COMMAND_MERGED_EXTERNAL_HOST_STDOUT_STDERR' and summary['separate_external_host_stderr_saved']is False and summary['independent_external_host_stderr_empty_verified']is False,'summary truthful merged streams')

check(type(watch['pid'])is int and watch['pid']==24164,'actual own checker PID')
check(type(watch['returncode'])is int and watch['returncode']==1,'actual child strictint1')
check(watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'genuine no limit failure own child cleanup')
check(type(watch['sampled_peak_rss_mib'])is float and watch['sampled_peak_rss_mib']==0.0,'actual zero sampled RSS recorded only')
check(math.isfinite(watch['elapsed_seconds']) and watch['elapsed_seconds']==0.43268845800776035,'actual short own child elapsed')
check(0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['rss_cap_mib']==512,'original remaining stage budget below600/RSS512')
binding,bindingpin=read(D/'Root_actual_native_SOURCE_binding.json','067838d4d01a2c8509fcf771c4ba2d9c78945780f2041ca691a5f57725fda155')
expected_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'Root_bound_complete_native_checker.py'),'--binding',str(D/'Root_actual_native_SOURCE_binding.json'),'--binding-sha256',bindingpin['sha256'],'--output-dir',str(O),'--expected-parent-pid','24163']
check(watch['command']==expected_command,'exact complete actual child command and parent argv')
check(type(binding['complete_input_pins'])is list and len(binding['complete_input_pins'])==129,'actual binding complete129 list, payloads not read')
check(binding['original_caps']==CAPS and binding['state_order']==['A','B'],'binding all original caps/two state order')
check(len({q['path']for q in binding['complete_input_pins']})==129,'complete unique129 pinned scope preserved metadata')
check('line 755, in main' in log and "require(type(inputs) is list and inputs, 'complete explicit input pins required')"in log and 'ValueError: complete explicit input pins required'in log,'real child merged trace pinpoints exact755 predicate')
checkerpin=pin(D/'Root_bound_complete_native_checker.py')
check(checkerpin['sha256']=='403feaa916159c901f7b4f44c6a7c70798afac7ce5035cdbded90a14a5c96517','exact failed native checker Source pin')
checker=(D/'Root_bound_complete_native_checker.py').read_text();ct=ast.parse(checker);fs={n.name:n for n in ct.body if isinstance(n,ast.FunctionDef)}
check(ast.get_source_segment(checker,fs['require'])=="def require(ok, message):\n    if type(ok) is not bool or not ok:\n        raise ValueError(message)",'strict require implementation unchanged')
check(checker.splitlines()[754].strip()=="require(type(inputs) is list and inputs, 'complete explicit input pins required')",'actual755 second operand returns valid nonempty list rather than bool')
check(checker.index("require(type(inputs) is list and inputs,")<checker.index('for p in inputs:')<checker.index('        exact_pin(p)'),'failure precedes input exact_pin/material operations')
check('output.mkdir()' in checker and not O.exists(),'actual output namespace absent; no full state comparison/output report')
check(not (H/'result.json').exists(),'genuine host successful result absent')
check(failed['status']=='FAILED_COMPLETE_NATIVE_BYTE_CHECK_NO_RETRY_NO_QUALIFICATION' and failed['actual_native_report_pin_if_saved']is None,'failed genuine host no report qualifier')
for key in ('native_persisted_XSM_value_bits_verified','original_native_build_binary_Source_linkage_qualified','actual_protocol_qualified','actual_full_rawrecord_transfer_qualified','original_XSM_memory_bits_verified','reaction_multiplicity_verified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','coupled_370group_reference_qualified','native_transport_executed','whole_combined_build_or_INPUT_qualified'):
 check(failed[key]is False,'failed real host qualification false '+key)
check(failed['new_native_walker_controls_actual_run']is None and failed['actual_native_byte_qualification_sha256']is None and failed['actual_scientific_qualification_sha256']is None,'failed real host future qualification null')
check(type(failed['whole_seconds'])is float and math.isfinite(failed['whole_seconds']) and 0<failed['whole_seconds']<1800,'actual finite failed host whole original cap')
check(stages['stages']==failed['stage_records'] and len(stages['stages'])==1,'complete original failed stage record retained')
stage=stages['stages'][0]
check(stage['command']==expected_command and stage['status']=='FAILED' and stage['wall_cap_seconds']==600.0,'exact one genuine failed stage no retry')
resource=stage['resource_before']
check(resource['min_free_bytes']==8*2**30 and resource['artifact_budget_bytes']==96*2**30,'real unchanged history/free resource caps')
check(resource['artifact_bytes']<96*2**30 and resource['disk_free_bytes']>=8*2**30,'real pre-stage complete resource observation')
check(controls['not_a_protocol_PASS']is True and controls['new_native_walker_controls_actual_run']is None,'new native protocol actually unexecuted')
for key in ('actual_protocol_qualified','actual_full_rawrecord_transfer_qualified','original_XSM_memory_bits_verified','reaction_multiplicity_verified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','coupled_370group_reference_qualified','native_transport_executed','whole_combined_build_or_INPUT_qualified'):
 check(controls[key]is False,'unexecuted controls scope false '+key)

check(pre['schema']=='ROOT_V22_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1' and pre['native_executed']is False,'actual prelaunch metadata-only scope')
check(pre['genuine_guard_MRO_verified']is True and pre['no_runtime_E_append']is True,'actual original guard MRO/frozenE intent')
check(pre['full129_material_payloads_not_rehashed_by_this_preflight']is True and pre['complete129_payloads_will_be_fresh_EOF_verified_by_genuine_host_before_and_after']is True,'preflight honest129 payload rehash boundary')
check(len(pre['complete_D_frozen']['files'])==358 and len(pre['complete_D_frozen']['directories'])==21,'actual frozenD358/rootinclusive21')
check(len(pre['complete_E_frozen_before_actual_launch']['files'])==149 and len(pre['complete_E_frozen_before_actual_launch']['directories'])==10,'actual frozen originalE149/rootinclusive10')
check(freeze['schema']=='ROOT_V22_COMPLETE_NATIVE_D_SOURCE_FREEZE_V1' and freeze['complete_D']==pre['complete_D_frozen'],'real installed pre-freeze and prelaunch completeD identical')
expected_pin(pre['actual_D_source_freeze'],'actual D freeze pin intact')
check(pre['actual_binding']==bindingpin,'actual prelaunch binding exact')
pg=pre['genuine_resources']
check(pg['artifact_budget_bytes']==96*2**30 and pg['min_free_bytes']==8*2**30,'actual preflight original resource caps')
check(pg['artifact_bytes']+2*2**30<96*2**30 and pg['disk_free_bytes']-2*2**30>=8*2**30,'actual full original reserve unchanged')
check(pg['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1','actual inherited dynamic full axial family resource policy')
check(pre_return['schema']=='ROOT_ACTUAL_NATIVE_SOURCE_PREFLIGHT_TOOL_RETURN_V1' and pre_return['closed']is True and pre_return['observed_terminal']is True and pre_return['native_executed_by_preflight']is False,'real preflight tool closed metadata scope')
prtr=pre_return['terminal_tool_return']
check(type(prtr['exit_code'])is int and prtr['exit_code']==0 and 'session_id'not in prtr and prtr['chunk_id']=='91d7be','real preflight typed0 no session')
actual_preflight_output=json.loads(prtr['output'])
check(actual_preflight_output['D_files']==358 and actual_preflight_output['E_files']==149,'actual preflight counts verified against snapshots')
oldprepin=expected_pin(actual_preflight_output['prelaunch'],'actual external prelaunch original SHA7ID retained')
check(oldprepin['sha256']==pp['sha256'] and Path(oldprepin['path']).read_bytes()==(E/'Root_actual_native_prelaunch_frozen_D_E.json').read_bytes(),'postclose E prelaunch copy byteexact with distinct honest7ID')
check(pre_return['saved_only_after_actual_native_terminal']is True,'real Root preflight receipt only appendedE postclose')

check(writer_return['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_POSTCLOSE_METADATA_WRITER_TOOL_RETURN_V1' and writer_return['closed']is True and writer_return['observed_terminal']is True,'real postclose META writer observed closed')
wtr=writer_return['terminal_tool_return']
check(type(wtr['exit_code'])is int and wtr['exit_code']==0 and 'session_id'not in wtr and wtr['chunk_id']==writer_return['actual_terminal_chunk']=='3ba3db','actual postclose META writer strict0')
wout=json.loads(wtr['output'])
check(wout['summary']==sp and wout['status']==summary['status'] and wout['native_actual_exit_code']==1,'true writer actual raw terminal matches complete failure summary')
check(writer_return['new_numeric_executed_by_writer']is False and writer_return['scientific_accuracy_qualified']is False,'writer no new business/science credit')
expected_pin(ns['writer'],'pre-frozen metadata writer exact original Source')
check(ns['writer']['sha256']=='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc','actual reviewed v2 writer Source preinstalled before freeze')
check(ns['schema']=='ROOT_V22_ACTUAL_NATIVE_COMPLETE_POSTCLOSE_NAMESPACES_V1' and [v['root']for v in ns['namespaces']]==list(map(str,(H,O,C,D,E))),'complete actual HOCDE saved namespace order')
check(ns['actual_tool_receipt']==rp and ns['prelaunch']==pp,'saved namespace true Root/prelaunch pins')
check(ns['all_current_files_full_EOF_SHA7ID']is True and ns['complete_D_unchanged']is True and ns['all_original_E_files_unchanged']is True and ns['E_directory_identity_after_postclose_appends_claimed_unchanged']is False,'saved freeze scope honest after postclose appends')
views=[view(p)for p in (H,O,C,D,E)]
for actual,saved in zip(views,ns['namespaces']):
 check(actual['root']==saved['root'] and actual['present']==saved['present'] and actual['symlinks']==saved['symlinks'],'actual saved namespace base '+saved['root'])
 for k,q in saved['files'].items():check(actual['files'][k]==q,'complete saved namespace EOF pin '+saved['root']+'/'+k)
 if actual['root']!=str(E):check(actual==saved,'complete saved namespace exact including dirs '+saved['root'])
 else:
  for k,q in saved['directories'].items():
   if k!='.':check(actual['directories'][k]==q,'original E nested directory sevenID unchanged '+k)
dv=views[3];ev=views[4]
check(dv==pre['complete_D_frozen'],'actual all358/21 D fullSHA7ID unchanged')
for k,q in pre['complete_E_frozen_before_actual_launch']['files'].items():check(ev['files'][k]==q,'original frozenE149 input fullEOF unchanged '+k)
for k,q in pre['complete_E_frozen_before_actual_launch']['directories'].items():
 if k!='.':check(ev['directories'][k]==q,'original E nested directories stable '+k)
postclosed5={'Root_actual_complete_native_merged_external_host_stdout_stderr.log','Root_actual_complete_native_prelaunch_tool_return.json','Root_actual_complete_native_tool_terminal_return.json','Root_actual_native_prelaunch_frozen_D_E.json','Root_actual_native_prelaunch_source.py'}
check(set(ns['namespaces'][4]['files'])-set(pre['complete_E_frozen_before_actual_launch']['files'])==postclosed5,'exact first five honest Root postclose capture appends')
postclosed3={'Root_actual_complete_native_postclose_META_writer_tool_return.json','Root_actual_complete_native_postclose_namespace_manifest.json','Root_actual_complete_native_postclose_summary.json'}
check(set(ev['files'])-set(ns['namespaces'][4]['files'])==postclosed3,'exact later three postclose META appends')
check(len(ev['files'])==157,'current actual E157 after postclose docs only')
original_after_metadata=sum(q['size_bytes']for q in views[0]['files'].values())+sum(q['size_bytes']for q in views[2]['files'].values())+sum(q['size_bytes']for q in dv['files'].values())+sum(q['size_bytes']for k,q in ev['files'].items()if k!='Root_actual_complete_native_postclose_META_writer_tool_return.json')
check(original_after_metadata==wout['joint_bytes_after_metadata_capture']==21242805,'exact original writer captured fullHOCDE archivebytes')
check(bytes_in(views)<2*2**30,'current completeHOCDE uncompressed original2GiB cap')
for name in [x.name for x in P.iterdir() if x.is_file() and x.name!='review_failed_native_saved_META_stdlib.py']:
 if name.startswith('actual_')or name.startswith('Root_'):
  if name.startswith('Root_'):source=E/name
  else:
   source={'actual_failed_native_watchdog.json':H/'native_run/native_xsm_ascii.watchdog.json','actual_failed_native_child_merged.log':H/'native_run/native_xsm_ascii.log','actual_failed_native_stages.json':H/'COMPLETE_NATIVE_XSM_ASCII/stages.json','actual_failed_native_host_result.json':H/'failed_host_result.json','actual_NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json':C/'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json','actual_failed_native_checker_SOURCE.py':D/'Root_bound_complete_native_checker.py','actual_prefrozen_postclose_META_writer_SOURCE.py':D/'Root_native_postclose_META_writer.py'}[name]
  check((P/name).read_bytes()==source.read_bytes(),'complete actual saved Source/META copied byteexact '+name)
for path,q in list(PINS.items()):check(pin(path)==q,'final reviewed saved input fullEOF unchanged '+path)
report=dict(schema='INDEPENDENT_V22_ACTUAL_FAILED_NATIVE_SAVED_SOURCE_META_REVIEW_V1',
 status='PASS_ACTUAL_FAILED_NATIVE_SAVED_EVIDENCE_ONLY',
 all_checks_typed_true=True,blockers=[],check_count=len(CHECKS),checks=CHECKS,
 actual_Root_native_terminal_pin=rp,actual_failed_native_summary_pin=sp,
 actual_complete_postclose_namespace_pin=np,actual_Root_META_writer_terminal_pin=wrp,
 actual_prelaunch_receipt_pin=prp,actual_prelaunch_pin=pp,
 actual_failed_child_watchdog_pin=watchpin,actual_failed_child_merged_log_pin=logpin,
 actual_failed_genuine_host_pin=failedpin,actual_failed_checker_Source_pin=checkerpin,
 full_EOF_reviewed_input_pins=PINS,actual_current_HOCDE_namespace=views,
 actual_frozen_D_files=358,actual_frozen_D_root_inclusive_directories=21,
 actual_prelaunch_E_files=149,actual_current_postclose_E_files=157,
 original129_material_payloads_not_read_or_rehashed_by_reviewer=True,
 actual_root_native_exit_code=1,actual_child_returncode=1,actual_child_PID=24164,
 actual_child_elapsed_seconds=watch['elapsed_seconds'],actual_sampled_RSS_mib=0.0,
 sampled_zero_RSS_is_not_memory_admission=True,native_RSS_verified=False,
 actual_failure_before_full_material_bit_comparison=True,
 failure_is_nonboolean_valid129_list_predicate_not_material_shape_or_physics=True,
 actual_report_and_success_host_result_absent=True,new_native_walker_controls_actual_run=None,
 actual_native_byte_qualification_sha256=None,
 native_persisted_XSM_value_bits_verified=False,original_XSM_memory_bits_verified=False,
 original_native_build_binary_Source_linkage_qualified=False,
 whole_combined_build_qualified=False,whole_combined_INPUT_admitted=False,
 physical_neutron_balance_qualified=False,scientific_accuracy_qualified=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,
 true_Root_native_terminal='efc410',true_Root_postclose_META_terminal='3ba3db',
 no_replication_or_same_family_retry_authorized=True,
 existing_bound89_Source_scientific_review_not_repeated=True,
 reviewer_executed_candidate_guard_native_or_numeric=False,
 canonical_ART_frozen_D_E_written_by_reviewer=False,
 actual_source_and_saved_META_only=True)
write('REVIEW.json',report)
write('COMPLETE_REVIEWED_INPUT_MANIFEST.json',dict(schema='INDEPENDENT_COMPLETE_V22_FAILED_NATIVE_REVIEWED_SOURCE_META_INPUTS_V1',pins=PINS,input_count=len(PINS),material129_payloads_excluded_explicitly=True))
(P/'REPORT.txt').write_text(
 'PASS_ACTUAL_FAILED_NATIVE_SAVED_EVIDENCE_ONLY\n'
 'Actual Root efc410 typedint1 CLOSED without a live session or repoll; genuine child24164 return1, elapsed0.43268845800776035 s, limit_failure=None, own-child cleanup true. Sampled0.0MiB is an unobserved fast-process peak, not memory admission.\n'
 'Complete frozen D358files/21 root-inclusive directories and all original E149 files preserved. Saved postclose namespace E154 and current E157 contain exactly five then three honest postclose capture/metadata appends; root E directory identity is not falsely claimed unchanged.\n'
 'Full H/O/C/D/E SOURCE/savedMETA EOF hashes and directory identities checked. O/report and successful host result absent; checker755 strict require rejects a nonempty129 list returned by type(inputs)islist and inputs before the full material comparison. Whole complete129 payloads were not read or rehashed by this reviewer.\n'
 'Real preflight91d7be0 and prefrozen postclose metadata writer3ba3db0 preserved with truthful merged stdout/stderr. Original1800/600/512/2GiB/history96/free8/1thread/1child/0retry and genuine guard evidence retained. All native bits, build/INPUT, neutron balance, AAA/ABA/science qualification remain false; no actual runtime or scientific successful result implied.\n')
print(json.dumps(dict(status=report['status'],check_count=len(CHECKS),full_EOF_unique_Source_META_files=len(PINS),actual_D_files=358,original_E_files=149,current_E_files=157,joint_current_HOCDE_bytes=bytes_in(views),actual_Root_exit_code=1,report=str(P/'REVIEW.json'),no_candidate_guard_native_numeric_executed=True)))

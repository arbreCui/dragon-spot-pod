"""Read saved Source/META and tiny protocol outputs; never execute reviewed code."""
from pathlib import Path
import ast, hashlib, json, math, os, shutil, stat, tempfile

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_graph_helper_controls_v23_receipts'
D=B/'actual_complete_graph_helper_controls_v23_sources'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-host-v23-20261010')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-v23-20261010')
checks=[];pins={};raws={};seq={}
def check(label,result):
 assert type(result) is bool,label+' not bool'
 assert not any(v['check']==label for v in checks),'duplicate '+label
 checks.append(dict(check=label,passed=result));assert result,label
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p,sha=None):
 p=Path(p);a=ident(p);i=seq.get(str(p),0)+1;seq[str(p)]=i;label=str(p)+'_'+str(i)
 check('regular_noalias_singlelink_'+label,stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink())
 r=p.read_bytes();check('fullEOF_stable7ID_'+label,a==ident(p) and a[4]==len(r))
 digest=hashlib.sha256(r).hexdigest()
 if sha is not None:check('exact_SHA_'+label,digest==sha)
 pin=dict(path=str(p),sha256=digest,size_bytes=len(r),identity=a);pins[str(p)]=pin
 if p==Path(__file__) or p.is_relative_to(H) or p.is_relative_to(O) or p.is_relative_to(E) or p in (D/'pure_helper_controls.py',D/'pure_helper_controls_host.py',D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py'):
  raws[str(p)]=r
 return pin,r
def pairs(values):
 r={}
 for k,v in values:assert k not in r,'duplicate finite META';r[k]=v
 return r
def nonfinite(v):raise AssertionError('nonfinite META '+v)
def read(p,sha=None):
 pin,raw=full(p,sha);return json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite),pin
def repin(pin,label):
 got,_=full(pin['path'],pin['sha256']);check(label,got==pin);return got
def names(root):
 return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def dirs(root):
 return {'.':ident(root),**{p.relative_to(root).as_posix():ident(p) for p in root.rglob('*') if p.is_dir() and not p.is_symlink()}}
def strict_terminal(receipt,expected_exit,expected_chunk,label):
 t=receipt['terminal_tool_return']
 check(label+'_real_strict_terminal',receipt['closed'] is True and receipt['actual_tool_terminal_return_observed'] is True and type(t['exit_code']) is int and t['exit_code']==expected_exit and t['chunk_id']==expected_chunk and t.get('session_id') is None and type(t['output']) is str)
 return t

summary,summarypin=read(E/'Root_actual_complete_qualification_postclose_summary.json','62c08b1e717bf9c09ddb4b1194a62ecc00b30cc5ad27cf2c5d1184ceb03c4f58')
receipt,receiptpin=read(E/'Root_actual_complete_qualification_tool_terminal_return.json','423ca0c05cecec24c3090c9e235c7aaa5345c3e751964fc1c61a9f43a7d1be86')
ns,nspin=read(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json','a0fdccbb135fc4892178c3a9dae6905d94abdbc37eef6eac9aa253a5a9470ec6')
writerreceipt,writerpin=read(E/'Root_actual_complete_qualification_postclose_tool_return.json','2f74c2b05885087aa929b075aa6291ff363e8653e6391854546d6d1b8966dfd1')
terminal=strict_terminal(receipt,1,'437ca4','actual_failed_pure')
wt=strict_terminal(writerreceipt,0,'93e463','actual_postclose_metadata_writer')
check('exact_saved_Root_schemas_scope',receipt['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and summary['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and ns['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_FULL_EOF_NAMESPACE_V1' and all(v['kind']=='pure' for v in [receipt,summary,ns,writerreceipt]))
check('Root_explicit_failed_incomplete_control_status',summary['status']=='ACTUAL_COMPLETE_CONTROLS_CLOSED_FAILURE_NO_RETRY' and summary['actual_closed'] is True and summary['actual_exit_code']==1 and summary['actual_complete_control_success'] is False and summary['actual_host_status'] is None)
observations=receipt['observations'];check('single_real_initial_then_same_handle_terminal_no_repoll',len(observations)==2 and observations[0]['tool']=='exec_command' and observations[0]['actual_tool_return']['chunk_id']=='597f0b' and type(observations[0]['actual_tool_return']['session_id']) is int and observations[0]['actual_tool_return']['session_id']==11505 and observations[1]['tool']=='write_stdin' and observations[1]['session_id']==11505 and observations[1]['actual_tool_return']==terminal)
check('all_streams_honestly_merged_only',receipt['original_outputs_preserved'] is True and receipt['merged_stdout_stderr_only'] is True and receipt['independent_stdout_captured'] is False and receipt['independent_stderr_captured'] is False)
pre,prepin=read(summary['actual_prelaunch']['path'],summary['actual_prelaunch']['sha256']);check('saved_prelaunch_exact4pin',prepin==summary['actual_prelaunch'])
freeze,freezepin=read(pre['source_freeze']['path'],pre['source_freeze']['sha256']);check('original_source_freeze4pin',freezepin==pre['source_freeze'])
check('D509_dirs47_Epre5_dirs1_scope_exact',len(pre['D']['files'])==summary['frozen_D_files']==509 and len(pre['D']['directories'])==summary['frozen_D_directories']==47 and len(pre['E']['files'])==summary['frozen_E_files']==5 and len(pre['E']['directories'])==summary['frozen_E_directories']==1)
check('whole_D_Source_scope_same_in_freeze_prelaunch_postclose',freeze['source_namespace']==pre['D']==ns['views']['D'])
check('all_HODE_roots_and_captured_counts_exact',{k:v['root'] for k,v in ns['views'].items()}=={'H':str(H),'O':str(O),'D':str(D),'E':str(E)} and [len(ns['views'][k]['files']) for k in ('H','O','D','E')]==[5,31,509,9])
for kind,view in ns['views'].items():
 root=Path(view['root']);expected={Path(p['path']).relative_to(root).as_posix() for p in view['files']}
 if kind=='E':expected|={'Root_actual_complete_qualification_postclose_namespace_manifest.json','Root_actual_complete_qualification_postclose_summary.json','Root_actual_complete_qualification_postclose_tool_return.json'}
 check('full_declared_'+kind+'_namespace_unfiltered',names(root)==expected)
 for i,p in enumerate(view['files']):repin(p,'all_'+kind+'_saved_fullpin_'+str(i))
 currentdirs=dirs(root)
 if kind=='E':
  check('E_only_rootmtime_changes_from_real_postclose_append',set(currentdirs)==set(view['directories']) and all(currentdirs[k]==v for k,v in view['directories'].items() if k!='.'))
 else:check('all_'+kind+'_directory_exact7ID',currentdirs==view['directories'])
 if kind!='O':check('no_Source_host_receipt_alias_'+kind,not any(p.is_symlink() for p in root.rglob('*')))
for i,p in enumerate(pre['E']['files']):repin(p,'all_original_Epre5_frozen_pin_'+str(i))
check('E_current12_equals9_declared_plus2_self_outputs_plus_true_writer_receipt',len(names(E))==12)
selfs=ns['E_explicit_self_excluded_current_writer_outputs']
check('only_current_two_writer_self_outputs_excluded',selfs==[str(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json'),str(E/'Root_actual_complete_qualification_postclose_summary.json')])
check('Rootwriter_true_claim_of_before_writer_D_E_compare',ns['original_frozen_D_E_unchanged_before_writer'] is True and summary['whole_frozen_D_E_files_and_directories_unchanged_before_writer'] is True and pre['D']['directories']==dirs(D))
for i,p in enumerate(pre['original_helper_Q_canonical']):repin(p,'all_original_protected_Source_Q_canonical_'+str(i))
repin(pre['installed_helper'],'complete_current_source_only_helper3b18_pin')
check('Source_installed_helper_no_new_control_Q',pre['installed_helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092' and freeze['new_actual_helper_qualification'] is None and freeze['six_future_business_pins']==[None]*6)
aliases=ns['views']['O']['original_fixture_symlinks'];check('two_original_output_file_symlinks_retained',len(aliases)==2 and {Path(a['path']).relative_to(O).as_posix() for a in aliases}=={'fixture/file_alias.txt','fixture/sealed/alias.txt'})
for i,a in enumerate(aliases):
 p=Path(a['path']);check('output_alias_lstat_text_'+str(i),p.is_symlink() and ident(p)==a['identity'] and os.readlink(p)==a['symlink_target_text'])
 check('output_alias_resolved_normal_file_'+str(i),str(p.resolve())==a['actual_resolved_target_full_EOF_pin']['path'])
 repin(a['actual_resolved_target_full_EOF_pin'],'output_alias_target_fullEOF_'+str(i))
check('complete_output_alias_namespace_not_omitted',{str(p) for p in O.rglob('*') if p.is_symlink()}=={a['path'] for a in aliases})
failed,failedpin=read(H/'failed_host_result.json');watch,watchpin=read(H/'run/admit.watchdog.json');report,reportpin=read(O/'ACTUAL_REPORT.json');ledger,_=read(H/'GRAPH_PROTOCOL_CONTROLS/stages.json')
check('no_success_host_result_exists',not os.path.lexists(H/'result.json'))
check('one_genuine_failed_stage_ledger_exact',set(ledger)=={'stages'} and ledger['stages']==failed['stage_records']==summary['actual_failure']['stage_records'] and len(ledger['stages'])==1 and ledger['stages'][0]['status']=='FAILED')
stage=ledger['stages'][0];command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'pure_helper_controls.py'),'--output-dir',str(O)]
check('genuine_actual_watched_command_full_source',watch['command']==stage['command']==command)
check('watch_real_failed_child_and_original_caps_cleanup',type(watch['pid']) is int and watch['pid']==28888 and type(watch['returncode']) is int and watch['returncode']==1 and watch['limit_failure'] is None and watch['rss_cap_mib']==512 and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=60 and math.isfinite(watch['elapsed_seconds']))
check('same_early_failed_resource_measurements_saved',summary['actual_child_seconds']==watch['elapsed_seconds']==0.45666741696186364 and summary['actual_own_child_sampled_peak_RSS_MiB']==watch['sampled_peak_rss_mib']==0.0)
check('actual_root_outer_failure_message_from_genuine_stage',failed['status']=='FAILED_PURE_GRAPH_PROTOCOL_CONTROLS_NO_RETRY' and failed['error']=="RuntimeError('own-child stage failed; no retry')" and 'own-child stage failed; no retry' in terminal['output'])
check('report_original_schema_failed_scope',report['schema']=='AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16' and report['status']=='ACTUAL_PURE_HELPER_CONTROLS_FAIL_NO_ADMISSION' and report['actual_success_pins'] is None)
check('original_caps_unrelaxed_in_saved_partial_report',report['caps']==dict(children=1,json_read_bytes=64*2**20,output_bytes=64*2**20,retries=0,rss_bytes=512*2**20,wall_seconds=60))
check('only_first_original_checkpoint_returned_not_full5',len(report['stages'])==1 and report['stages'][0]['stage']=='real_small_fixture_producer_equivalence_and_rejections')
check('whole_protocol_fulltrace_fullgraph_finalcheck_and_new9field_artifact_not_completed',all(k not in report for k in ['full_new_creation_trace','full_old_saved_graph','saved_input_bytes_identity_after','private_inactive_audit_snapshot_controls','private_inactive_audit_snapshot_controls_order_preserved_artifact']) and not os.path.lexists(O/'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json') and not os.path.lexists(O/'full_new_creation_trace.encoded.json') and not os.path.lexists(O/'full_old_saved_graph.encoded.json'))
message='JSON scalar differs at same_actual_read_duplicate_and_Popen_owned_True/default original complete state/exact_actual_Popen_object_references/0'
check('exact_saved_failure_class_and_tuple_path',report['failure']=={'class':'AssertionError','message':message})
log=raws[str(H/'run/admit.log')].decode();check('actual_log_exact_tuple_comparison_location','line 192, in small_private_snapshot_controls' in log and message in log and 'line 119, in exact_value' in log)
controller=raws[str(D/'pure_helper_controls.py')].decode();small=raws[str(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')].decode()
ct=ast.parse(controller);st=ast.parse(small)
fn=next(n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name=='exact_value')
compare=''.join(controller.splitlines(keepends=True)[fn.lineno-1:fn.end_lineno])
check('JSON_only_comparator_type_order_lists_floatbits_no_tuple_branch','kind is list' in compare and 'kind is dict' in compare and 'kind is float' in compare and 'kind in (str, int, bool, type(None))' in compare and 'tuple' not in compare)
fn=next(n for n in st.body if isinstance(n,ast.FunctionDef) and n.name=='audit_state_pin')
assignment=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets))
check('actual_witness_rows_are_threeitem_tuple_not_Popen_instance',isinstance(assignment.value,ast.ListComp) and isinstance(assignment.value.elt,ast.Tuple) and len(assignment.value.elt.elts)==3 and ast.unparse(assignment.value.elt.elts[2])=='id(value)')
check('Source_actual_same_observation_Popen_map_field_not_rawvalue_reference','exact_actual_Popen_object_references=objects' in small and 'exact_value(before, audit_state_pin(baseline_audit)' in small and 'audit._popen_objects = dict(observed._popen_objects)' in small)
fixture,_=read(O/'small_fixture_controls.json');codec,_=read(O/'small_codec_and_rejection_controls.json')
check('partial_fixture_producer_result_preserved_without_fullprotocol_credit',fixture['producer_full_exact_values_types_order_floatbits'] is True and fixture['caller_full_value_and_mutable_identity_preserved'] is True)
check('partial_completed_codec_61_reject_rows_preserved',len(codec['rejections'])==61 and report['small_codecs']['rejections']==61)
check('all_partial_report_business_science_flags_false',all(report[k] is False for k in ['business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']))
check('all_Root_failed_summary_qualification_fields_false_orNone',summary['new_actual_helper_qualification'] is None and all(summary[k] is False for k in ['actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']))
check('FreshV23_genuine_HOST_OUT_not_executed',not os.path.lexists(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-host-v23-20261010')) and not os.path.lexists(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-v23-20261010')))
actual_writer=json.loads(wt['output'],object_pairs_hook=pairs,parse_constant=nonfinite)
check('real_postclose_writer_stdout_exact_summary_NS_terminal_4pins',actual_writer['summary']==summarypin and actual_writer['namespace_manifest']==nspin and actual_writer['actual_terminal_receipt']==receiptpin and actual_writer['actual_closed_success'] is False and actual_writer['actual_exit_code']==1)
check('true_root_summary_NS_terminal_references',summary['actual_terminal_receipt']==receiptpin and summary['namespace_manifest']==nspin and ns['closed_actual_tool']==receiptpin)
bundle,bundlepin=read(summary['Root_actual_bundle']['path'],summary['Root_actual_bundle']['sha256']);check('original_actual_Root_tool_bundle_exactpin',bundlepin==summary['Root_actual_bundle'] and bundle['terminal_tool_return']==terminal and bundle['observations']==observations and bundle['actual_command']==receipt['actual_command'])
repin(summary['Source_postclose_writer'],'true_current_std_only_postclose_writer_Source_pin')
check('prelaunch_postclose_Source_writers_not_helpers','business_component' not in raws[str(E/'spot_v23_helper_qualification_postclose_ROOT.py')].decode())
def size(root):return sum(p.lstat().st_size for p in root.rglob('*') if stat.S_ISREG(p.lstat().st_mode))
hod=sum(size(r) for r in [H,O,D]);hode=hod+size(E)
check('original_HOD_full_regular_bytes_and_cap',hod==summary['normal_HOD_bytes']==24976999 and hod<64*2**20 and summary['normal_host_archive_scope']=='H+O+D')
check('honest_afterwriter_HODE_receipt_only_increment',summary['complete_HODE_bytes']==26707846 and writerpin['size_bytes']==2328 and hode==26707846+2328)
check('two_self_outputs_actual_bytes_counted_without_alias_doublecount',summary['complete_HODE_bytes_accounting_includes_all_current_writer_outputs'] is True and summary['original_archive_cap_bytes']==64*2**20 and hode<64*2**20)
for path,pin in list(pins.items()):
 r=Path(path).read_bytes();check('final_complete_Source_META_smallOutput_EOF_SHA7ID_'+path,ident(path)==pin['identity'] and len(r)==pin['size_bytes'] and hashlib.sha256(r).hexdigest()==pin['sha256'])
check('final_D_all47dirs_frozen',dirs(D)==pre['D']['directories'])
full(Path(__file__))
out=Path(tempfile.mkdtemp(prefix='axmat_v23_actual_failed_inactive_audit_pure_saved_SOURCE_META_review_',dir='/private/tmp'))
for path,raw in raws.items():
 p=Path(path)
 if p.is_relative_to(O):dst=out/'ACTUAL_COMPLETE_SMALL_OUTPUT'/p.relative_to(O)
 elif p.is_relative_to(H):dst=out/'ACTUAL_FAILED_HOST'/p.relative_to(H)
 elif p.is_relative_to(E):dst=out/'ACTUAL_ROOT_SAVED_META'/p.relative_to(E)
 else:dst=out/'SOURCE_CAUSE_AND_AUDITOR'/p.name
 dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
(out/'FULL_EOF_SOURCE_META_SMALL_OUTPUT_INPUT_PINS.json').write_text(json.dumps(pins,indent=2,allow_nan=False)+'\n')
review=dict(schema='INDEPENDENT_V23_ACTUAL_FAILED_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1',status='PASS_SAVED_ACTUAL_PURE_CONTROLS_FAILURE_EVIDENCE_ONLY',source_and_saved_META_only=True,all_checks_typed_true=True,blockers=[],checks=checks,check_count=len(checks),
 actual_Root_failed_terminal_receipt_pin=receiptpin,actual_Root_postclose_writer_terminal_receipt_pin=writerpin,actual_Root_failed_summary_pin=summarypin,actual_Root_complete_postclose_namespace_manifest_pin=nspin,
 actual_watchdog_pin=watchpin,actual_failed_host_result_pin=failedpin,actual_failed_partial_control_report_pin=reportpin,
 frozen_D_files=509,frozen_D_directories=47,frozen_original_E_files=5,frozen_original_E_directories=1,actual_current_E_files=12,
 namespace_scope=dict(H_files=5,O_regular_files=31,O_original_file_symlinks=2,D_files=509,E_at_namespace_capture=9,E_current=12),
 actual_terminal_exit_code=1,actual_terminal_chunk_id='437ca4',actual_original_session=11505,no_repoll_or_retry_performed_by_reviewer=True,
 actual_child_seconds=watch['elapsed_seconds'],actual_own_child_sampled_RSS_MiB=0.0,
 sampled_zero_RSS_is_an_early_unsampled_failure_not_memory_qualification=True,partial_child_self_reported_peak_RSS_bytes=report['peak_rss_bytes'],
 failure_cause='Checker witness list contains three-item tuples (key, typename, id(value)); original exact_value accepts JSON builtins and rejects tuple at /exact_actual_Popen_object_references/0. This is an oracle representation mismatch, not evidence of helper output mismatch.',
 original_witness_row_does_not_hold_actual_Popen_value_reference=True,whole_original_pure_protocol_completed=False,all_new_5positive13reject3failure_controls_completed=False,new_order_preserving_ninefield_artifact_produced=False,
 actual_pure_protocol_qualified=False,actual_full_current_graph_verifier_qualified=False,FreshV23_executed=False,new_actual_helper_qualification=None,
 actual_complete_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,
 original_HOD_bytes=hod,Root_writer_time_HODE_bytes=26707846,Root_true_postclose_writer_receipt_increment_bytes=2328,current_HODE_bytes=hode,
 reviewer_candidate_helper_guard_API_controller_binder_numeric_or_business_executed=False,original_large_input_graph_trace_or_material_payload_not_replayed_or_rehashed=True)
(out/'REVIEW.json').write_text(json.dumps(review,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('PASS: actual failed genuine pure-control saved Source/META evidence is preserved.\nRoot initial597f0b/session11505 -> terminal437ca4 strictEXIT1 CLOSED; no repoll/retry. Root postclose META writer93e463 strictEXIT0.\nCause: three-item tuple witness meets a JSON-only comparator; no actual Popen value is held in that row.\nFull pure protocol/new5+13+3/ordered9field artifact were not completed; FreshV23 did not run. No new helper/RSS/build/INPUT/native/science qualification.\nH5/O31+2 original symlinks/D509+47dirs/Epre5+1dir all full EOF/7ID checked. HOD24976999; writer-timeHODE26707846; later real writer receipt2328; currentHODE26710174.\nRSS sample0.0 is an early unsampled failure. Only saved Source/META and small protocol outputs were read; no reviewed API or large material payload.\n')
print(json.dumps(dict(source_and_saved_META_only=True,review_dir=str(out),status=review['status'],check_count=len(checks),all_checks_typed_true=True,blockers=[],review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),actual_Root_exit_code=1,new_actual_helper_qualification=None),separators=(',',':')))

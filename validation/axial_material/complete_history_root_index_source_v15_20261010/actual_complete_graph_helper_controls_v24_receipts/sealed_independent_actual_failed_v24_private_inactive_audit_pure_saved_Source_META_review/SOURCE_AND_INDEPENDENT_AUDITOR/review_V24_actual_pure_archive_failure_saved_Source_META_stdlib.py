"""Read saved Source/META and tiny protocol outputs; never execute reviewed code."""
from pathlib import Path
import ast, hashlib, json, math, os, shutil, stat, tempfile, struct, collections

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_graph_helper_controls_v24_receipts'
D=B/'actual_complete_graph_helper_controls_v24_sources'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-host-v24-20261010')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-v24-20261010')
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
 check('no_large_graph_payload_read_'+label,not(p.is_relative_to(O) and a[4]>5*2**20))
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
 check(label+'_real_strict_terminal',receipt['closed'] is True and receipt.get('actual_tool_terminal_return_observed',receipt.get('original_host_exit_code')==1) is True and type(t['exit_code']) is int and t['exit_code']==expected_exit and t['chunk_id']==expected_chunk and t.get('session_id') is None and type(t['output']) is str)
 return t


large_saved={}
def statonly_root_saved(pin,label):
 p=Path(pin['path']);a=ident(p)
 check(label+'_saved_full4pin_and_current7ID',set(pin)=={'path','sha256','size_bytes','identity'}and type(pin['sha256'])is str and len(pin['sha256'])==64 and a==pin['identity']and a[4]==pin['size_bytes']and stat.S_ISREG(a[2])and a[3]==1 and not p.is_symlink())
 large_saved[str(p)]=pin
 return pin
def exact(left,right,where,ordered=True):
 check(where+'_exact_builtin_type',type(left)is type(right))
 if type(left)is dict:
  check(where+'_full_keys_order'if ordered else where+'_full_keys_for_sorted_report',list(left)==list(right)if ordered else set(left)==set(right))
  for k in left:exact(left[k],right[k],where+'/'+k,ordered)
 elif type(left)is list:
  check(where+'_complete_list_count',len(left)==len(right))
  for i,(a,b)in enumerate(zip(left,right)):exact(a,b,where+'/'+str(i),ordered)
 elif type(left)is float:check(where+'_exact_finite_float64_bits',math.isfinite(left)and math.isfinite(right)and struct.pack('>d',left)==struct.pack('>d',right))
 else:check(where+'_exact_scalar_value',type(left)in(str,int,bool,type(None))and left==right)
summary,summarypin=read(E/'Root_actual_complete_qualification_postclose_summary.json','3b37ae88ac9526f92a638f43756211608f54a4d4cdebc065bea86f8a181ac266')
receipt,receiptpin=read(E/'Root_actual_complete_qualification_tool_terminal_return.json','6d4553ecbbf6c28f52c956af284aa2e761b9bd6f81da60924ccff9a0b5bb9cca')
ns,nspin=read(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json','fb9b73ba79ae1cacd13878a302a22e228b418af2c4d92ad247006229b910d471')
writerreceipt,writerpin=read(E/'Root_actual_complete_qualification_postclose_tool_return.json','7b034df40682c8e9f0acb2bc18f16178d35dcc61d32c716cc6fd3926b2402235')
terminal=strict_terminal(receipt,1,'a1dcb2','true_outer_archive_failure')
wt=strict_terminal(writerreceipt,0,'a8d98e','true_postclose_metadata_writer')
check('actual_V24_schemas_and_pure_scope',receipt['schema']=='ROOT_V24_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1'and summary['schema']=='ROOT_V24_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1'and ns['schema']=='ROOT_V24_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_FULL_EOF_NAMESPACE_V1'and all(x['kind']=='pure'for x in [receipt,summary,ns]))
check('whole_host_not_admitted_root_actual_closed1',summary['status']=='ACTUAL_COMPLETE_CONTROLS_CLOSED_FAILURE_NO_RETRY'and summary['actual_closed']is True and type(summary['actual_exit_code'])is int and summary['actual_exit_code']==1 and summary['actual_complete_control_success']is False and summary['actual_host_status']is None)
obs=receipt['observations'];check('single_original_session_all_actual_observations_until_closed',len(obs)==3 and obs[0]['operation']=='exec_command'and obs[0]['actual_tool_return']['chunk_id']=='98a38f'and obs[0]['actual_tool_return']['session_id']==8777 and obs[1]['operation']==obs[2]['operation']=='write_stdin'and obs[1]['arguments']['session_id']==obs[2]['arguments']['session_id']==8777 and obs[1]['actual_tool_return']['session_id']==8777 and obs[-1]['actual_tool_return']==terminal)
check('external_streams_are_honestly_merged',receipt['original_outputs_preserved']is True and receipt['merged_stdout_stderr_only']is True and receipt['independent_stdout_captured']is False and receipt['independent_stderr_captured']is False)
pre,prepin=read(summary['actual_prelaunch']['path'],summary['actual_prelaunch']['sha256']);check('Root_actual_prelaunch_full4pin',prepin==summary['actual_prelaunch'])
freeze,freezepin=read(pre['source_freeze']['path'],pre['source_freeze']['sha256']);check('Root_original_full_freeze4pin',freezepin==pre['source_freeze'])
check('all_original_D353_dirs30_Epre3_dir1',len(pre['D']['files'])==summary['frozen_D_files']==353 and len(pre['D']['directories'])==summary['frozen_D_directories']==30 and len(pre['E']['files'])==summary['frozen_E_files']==3 and len(pre['E']['directories'])==summary['frozen_E_directories']==1)
check('D_full_namespace_before_after_exact',freeze['source_namespace']==pre['D']==ns['views']['D'])
check('full_HODE_scope_root_counts',{k:v['root']for k,v in ns['views'].items()}=={'H':str(H),'O':str(O),'D':str(D),'E':str(E)}and [len(ns['views'][k]['files'])for k in ['H','O','D','E']]==[5,34,353,7])
for kind,view in ns['views'].items():
 root=Path(view['root']);expected={Path(p['path']).relative_to(root).as_posix()for p in view['files']}
 if kind=='E':expected|={'Root_actual_complete_qualification_postclose_namespace_manifest.json','Root_actual_complete_qualification_postclose_summary.json','Root_actual_complete_qualification_postclose_tool_return.json'}
 check('actual_'+kind+'_all_declared_regular_names',names(root)==expected)
 for i,pin in enumerate(view['files']):
  if kind=='O'and pin['size_bytes']>5*2**20:statonly_root_saved(pin,'actual_Root_saved_complete_large_payload_'+str(i))
  else:repin(pin,'actual_'+kind+'_fullEOF_SHA7ID_'+str(i))
 currentdirs=dirs(root)
 if kind=='E':check('E_only_root_identity_timestamp_changes_after_real_append',set(currentdirs)==set(view['directories'])and all(currentdirs[k]==v for k,v in view['directories'].items()if k!='.'))
 else:check('all_'+kind+'_directories_full7ID',currentdirs==view['directories'])
 if kind!='O':check('all_'+kind+'_Source_host_META_alias_absent',not any(p.is_symlink()for p in root.rglob('*')))
check('current_E10_exact7declared_2self_1truewriterreceipt',len(names(E))==10)
check('only_exact_two_writer_selfexcluded_outputs',ns['E_explicit_self_excluded_current_writer_outputs']==[str(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json'),str(E/'Root_actual_complete_qualification_postclose_summary.json')])
for i,pin in enumerate(pre['E']['files']):repin(pin,'original_Epre3_frozen_actual_pin_'+str(i))
check('D_E_original_execution_freeze_honest',ns['original_frozen_D_E_unchanged_before_writer']is True and summary['whole_frozen_D_E_files_and_directories_unchanged_before_writer']is True and pre['D']['directories']==dirs(D))
for i,pin in enumerate(pre['original_helper_Q_canonical']):repin(pin,'protected_actual_old_Source_Q_canonical_'+str(i))
repin(pre['installed_helper'],'installed_helper3b_original_fullpin')
check('helper3b_Source_not_Q',pre['installed_helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'and freeze['new_actual_helper_qualification']is None and freeze['six_future_business_pins']==[None]*6)
aliases=ns['views']['O']['original_fixture_symlinks'];check('all_two_original_fixture_symlinks',len(aliases)==2 and {Path(a['path']).relative_to(O).as_posix()for a in aliases}=={'fixture/file_alias.txt','fixture/sealed/alias.txt'})
for i,a in enumerate(aliases):
 p=Path(a['path']);check('fixture_link_text_full_lstat_'+str(i),p.is_symlink()and ident(p)==a['identity']and os.readlink(p)==a['symlink_target_text']and str(p.resolve())==a['actual_resolved_target_full_EOF_pin']['path'])
 repin(a['actual_resolved_target_full_EOF_pin'],'original_fixture_link_target_fullEOF_'+str(i))
check('original_alias_inventory_full',{str(p)for p in O.rglob('*')if p.is_symlink()}=={a['path']for a in aliases})
failed,failedpin=read(H/'failed_host_result.json');watch,watchpin=read(H/'run/admit.watchdog.json');report,reportpin=read(O/'ACTUAL_REPORT.json');ledger,_=read(H/'GRAPH_PROTOCOL_CONTROLS/stages.json')
check('outer_no_success_host_result',not os.path.lexists(H/'result.json'))
check('genuine_child_one_PASS_stage_with_failed_host',ledger['stages']==failed['stage_records']==summary['actual_failure']['stage_records']and len(ledger['stages'])==1 and ledger['stages'][0]['status']=='PASS')
stage=ledger['stages'][0];command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'pure_helper_controls.py'),'--output-dir',str(O)]
check('whole_watched_child_actual_command',watch['command']==stage['command']==command)
check('real_child0_bounded_watch_PID_cleanup',type(watch['pid'])is int and watch['pid']==30370 and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=60)
check('actual_child_sampled_measurements_exact',summary['actual_child_seconds']==watch['elapsed_seconds']==16.655066707986407 and summary['actual_own_child_sampled_peak_RSS_MiB']==watch['sampled_peak_rss_mib']==396.53125)
check('whole_Root_failure_archive_guard_not_child',failed['status']=='FAILED_PURE_GRAPH_PROTOCOL_CONTROLS_NO_RETRY'and failed['error']=="ValueError('unchanged admission host caps exceeded')"and 'line 118, in main'in terminal['output']and 'unchanged admission host caps exceeded'in terminal['output'])
check('child_report_completed_without_admission',report['schema']=='AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16'and report['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'and report['source_status']=='READY_SOURCE_BOUND_BY_ROOT'and type(report['actual_success_pins'])is dict)
check('child_full_original60_512_64MB_1_0_caps',report['caps']==dict(children=1,json_read_bytes=64*2**20,output_bytes=64*2**20,retries=0,rss_bytes=512*2**20,wall_seconds=60))
labels=['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged']
check('all_five_original_child_protocol_stage_checkpoints',len(report['stages'])==5 and [v['stage']for v in report['stages']]==labels and all(math.isfinite(v['elapsed_seconds'])and 0<=v['elapsed_seconds']<60 and 0<=v['peak_rss_bytes']<512*2**20 and 0<=v['owned_output_bytes']<64*2**20 for v in report['stages']))
logpin,lograw=full(H/'run/admit.log',stage['log_sha256']);stdout=json.loads(lograw,object_pairs_hook=pairs,parse_constant=nonfinite)
check('actual_PASS_child_stdout_whole_report4pin',stdout['status']==report['status']and stdout['report']==reportpin and stdout['peak_rss_bytes']==report['peak_rss_bytes']==415793152 and 0<stdout['elapsed_seconds']<watch['elapsed_seconds'])
check('actual_root_source_3b_helper7ID',report['helper']['path']==pre['installed_helper']['path']and report['helper']['sha256']==pre['installed_helper']['sha256']and report['helper']['identity']==pre['installed_helper']['identity']and report['helper']['source_bytes']==150986 and report['actual_success_pins']['helper']==report['helper'])
for role in ['pure_helper_controls.py','pure_helper_controls_host.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py']:ast.parse(raws[str(D/role)])
controller=raws[str(D/'pure_helper_controls.py')].decode();host=raws[str(D/'pure_helper_controls_host.py')].decode();module=raws[str(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')].decode()
check('host_original_genuine_guard_caps_and_true_archive_gate',all(fragment in host for fragment in ['WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20','helper.modules();helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',"resources.check()",'threads=1,children_at_once=1,retries=0','profile_used=False,supervisor_class_or_MRO_modified=False',"archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))","if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')"]))
check('same_actual_private_Module_d439_source',pins[str(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')]['sha256']=='d439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483')
check('Module_refs_metadata_plus_exact_rawvalue_type_is_Source',"id(value), value)"in module and 'type(lrow[3]) is type(rrow[3]) and lrow[3] is rrow[3]'in module and module.count('complete_audit_state_equal(')==8)
repin(report['private_snapshot_control_Source'],'actual_report_same_Module_full4pin')
private,privatepin=read(O/'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json')
check('whole_order_preserving_control_artifact_actualpin',privatepin==report['private_inactive_audit_snapshot_controls_order_preserved_artifact'])
exact(private,report['private_inactive_audit_snapshot_controls'],'full_artifact_vs_original_sorted_aggregate_report',ordered=False)
fields=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
positives=['empty_owned_True','same_actual_read_duplicate_and_Popen_owned_True','control_only_floatbits_strattrs_owned_True','default_Audit_subclass','default_records_dict_subclass']
rejects=['flag_None','flag_zero','flag_one','flag_string','flag_list','flag_dict','Audit_subclass_True','records_dict_subclass_True','records_list_True','recording_True','stale_active_registry_identity','active_True','active_False']
failures=['invalid_second_row_before_clear','missing_attempt_count_before_clear','nonfinite_clone_after_clear']
check('all5pos13reject3lastuse_actualcomplete_order',[r['case']for r in private['positive_controls']]==positives and [r['case']for r in private['private_guard_rejections']]==rejects and [r['case']for r in private['last_use_failure_controls']]==failures)
for i,c in enumerate(private['positive_controls']):
 expected=c['actual_full_expected_snapshot'];actual=c['actual_full_consumed_snapshot'if i<3 else'actual_full_default_snapshot']
 check('positive_complete9field_order_'+str(i),list(expected)==list(actual)==fields)
 exact(expected,actual,'positive_full_public_types_order_floatbits_'+str(i))
 check('positive_defaultFalse_whole_caller_state_'+str(i),c['default_and_explicitFalse_complete_state_unchanged']is True and c['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default']is True)
 if i<3:check('positive_ownedmap_actualrefs_retained_'+str(i),c['owned_same_builtin_records_map_completely_cleared']is True and c['all_other_audit_state_and_actual_Popen_references_unchanged']is True and c['augmented_control_fields_not_claimed_as_actual_open_trace']is(i==2))
 else:check('default_subclass_privateTrue_not_permitted_'+str(i),c['private_True_not_permitted_for_subclass']is True)
for i,c in enumerate(private['private_guard_rejections']):
 message='private read-open snapshot consume flag must be an exact bool'if i<6 else('end the read-open audit phase before freezing its trace'if i>=11 else'private read-open snapshot consume requires an owned inactive builtin audit')
 check('all_rejection_exactclass_message_fullstate_'+str(i),c['rejected']is True and c['class_name']=='InputGraphError'and c['message']==message and c['complete_audit_state_identity_type_order_value_bits_unchanged']is True)
for i,c in enumerate(private['last_use_failure_controls']):
 after=i==2;check('nontransactional_failure_original_error_order_'+str(i),c['actual_default_error']==c['actual_private_error']and c['original_error_class_and_message_retained']is True and c['no_transactional_private_mode_promise']is True and c['both_callers_unchanged_before_clear_or_default']is(not after)and c['private_clone_failure_after_clear_consumption_observed']is after)
check('one_actual_Popen_observation_order_complete',list(private['actual_single_Popen_observation'])==fields and private['actual_child_returncode']==0 and private['actual_stdout_hex']==b'inactive audit metadata protocol\n'.hex()and private['actual_stderr_hex']==''and len(private['actual_single_Popen_observation']['subprocess_records'])==1)
check('same_actual_capture_metadata_honest_no_normalization',all(private[k]is True for k in ['actual_same_observation_full_record_role_comparison','no_cross_process_PID_FD_inode_normalization','default_original_complete_protocol_preserved','no_new_fixture_or_material_file_created'])and all(private[k]is False for k in ['native_or_numeric_component_executed','helper_qualification_created','business_or_science_qualification_created']))
fixture,_=read(O/'small_fixture_controls.json');codec,_=read(O/'small_codec_and_rejection_controls.json')
check('original_fixture_fullproducer_9categories_2subtypes',fixture['producer_full_exact_values_types_order_floatbits']is True and fixture['caller_full_value_and_mutable_identity_preserved']is True and len(fixture['accepted_str_subclass_equivalence_controls'])==2 and fixture['all_nine_closure_categories']==['capture','code_environment','component_ancestry','component_terminals','dedup_build','memory_build','original92_build','physical_build','source_namespace'])
check('original_codec_all61rejects_bothentrances_defaultnonmutation',len(codec['rejections'])==report['small_codecs']['rejections']==61 and codec['all_default_inputs_unmodified']is True and codec['all_lossless_missing_null_order_type_floatbit_duplicate_controls']is True)
owner=report['private_owner_consume_controls']
check('owner4positive3reject2subtypes2partialcomplete',len(owner['positive_controls'])==4 and {c['case']for c in owner['positive_controls']}=={'default_list','default_tuple','explicit_False_list','owned_builtin_list_True'}and len(owner['private_guard_rejections'])==3 and len(owner['accepted_str_subclass_equivalence_controls'])==2 and len(owner['partial_invalid_second_owner_rejections'])==2)
for i,c in enumerate(owner['positive_controls']+owner['accepted_str_subclass_equivalence_controls']):
 exact(c['expected_complete_descriptor_signature'],c['actual_complete_descriptor_signature'],'original_owner_full_descriptor_signature_'+str(i))
check('owner_original_lastuse_partial_behavior_honest',all(owner[k]is True for k in ['first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created'])and owner['new_helper_qualification_created']is False and owner['business_or_science_qualification_created']is False)
trace=report['full_new_creation_trace'];graph=report['full_old_saved_graph']
check('full63379_trace175886_attempts_sourceorder_roundtrip',trace['full_record_count']==trace['table_rows']==63379 and trace['actual_attempt_count']==175886 and trace['subprocess_record_count']==0 and all(trace[k]is True for k in ['default_source_nonmutation','exact_full_roundtrip','persisted_full_trace_exact_order_type_floatbit_inverse']))
check('all_original_fullgraph_two_strict_entrances_exact',graph['complete_original_metadata']==graph['normal_strict_file_entrance_full_semantics_and_counts']==graph['normal_strict_payload_entrance_full_semantics_and_counts']and all(graph[k]is True for k in ['full_default_roundtrip_exact','no_two_complete_decoded_graphs_between_strict_stages','old_read_trace_not_replaced_by_new_trace','original_legacy_semantic_sha_preserved']))
check('fulloldgraph_counts_legacywire_original_scope',graph['complete_original_metadata']['complete_counts']['canonical_files']==36776 and graph['complete_original_metadata']['complete_counts']['requirements']==237767 and graph['complete_original_metadata']['legacy_semantic_sha256']=='51f051f627181e2b815f0dd4a77d7f40e718c268695c33c5ccfbde74c6b8f1f9'and graph['complete_original_metadata']['wire_content_sha256']=='ee2cabfd7b93d10bb7c5dc17c01a3d190202faf16eb7d2d8f8125d9507671427')
check('two_large_encoded_outputs_Root_savedfullEOF_exact4pins',len(large_saved)==2 and trace['encoded_artifact']==report['actual_success_pins']['encoded_new_trace']==large_saved[str(O/'full_new_creation_trace.encoded.json')]and graph['stored_wholegraph']==report['actual_success_pins']['encoded_wholegraph']==large_saved[str(O/'full_old_saved_graph.encoded.json')])
check('all_original_large_input_saved_before_after_pins',report['saved_input_identity_before']==report['saved_input_bytes_identity_after']and len(report['saved_input_identity_before'])==2 and graph['input']==report['saved_input_identity_before'][0]and trace['input']==report['saved_input_identity_before'][1])
check('report_outer_summary_science_and_Q_credit_remainfalse',summary['new_actual_helper_qualification']is None and all(summary[k]is False for k in ['actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted'])and all(report[k]is False for k in ['business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']))
check('fresh_V24_not_started',not os.path.lexists(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-host-v24-20261010'))and not os.path.lexists(Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-fresh-verifier-v24-20261010')))
actualwriter=json.loads(wt['output'],object_pairs_hook=pairs,parse_constant=nonfinite)
check('Root_postclose_stdout_actualpins_trueexit1',actualwriter['summary']==summarypin and actualwriter['namespace_manifest']==nspin and actualwriter['actual_terminal_receipt']==receiptpin and actualwriter['actual_closed_success']is False and actualwriter['actual_exit_code']==1)
check('Root_summary_complete_namespace_terminal_independentpins',summary['actual_terminal_receipt']==receiptpin and summary['namespace_manifest']==nspin and ns['closed_actual_tool']==receiptpin)
bundle,bundlepin=read(summary['Root_actual_bundle']['path'],summary['Root_actual_bundle']['sha256']);check('true_original_Root_closed_tool_bundle',bundlepin==summary['Root_actual_bundle']and bundle['terminal_tool_return']==terminal and bundle['observations']==obs and bundle['actual_command']==receipt['actual_command'])
repin(summary['Source_postclose_writer'],'true_stdonly_saved_postclose_writer_Source')
def size(root):return sum(p.lstat().st_size for p in root.rglob('*')if stat.S_ISREG(p.lstat().st_mode))
bytes_by_scope={k:size(root)for k,root in [('H',H),('O',O),('D',D),('E',E)]};hod=sum(bytes_by_scope[k]for k in ['H','O','D']);hode=hod+bytes_by_scope['E']
check('complete_HOD80605706_over_original64MB',hod==summary['normal_HOD_bytes']==80605706 and hod>64*2**20 and summary['normal_host_archive_scope']=='H+O+D'and summary['original_archive_cap_bytes']==64*2**20 and summary['original_normal_archive_under_cap']is False)
check('honest_HODE_writer_time81916624_plus_actualreceipt1876',summary['complete_HODE_bytes']==81916624 and writerpin['size_bytes']==1876 and hode==81916624+1876 and summary['Root_separate_conservative_HODE_under_64MiB']is False)
check('archive_already_overcap_before_only_failure_record',hod-failedpin['size_bytes']>64*2**20)
check('child_O_original64MB_not_overcap',bytes_by_scope['O']<64*2**20)
check('failure_outer_elapsed_unknown_no_inventedmeasurement',summary['whole_host_seconds']is None)
check('all_self_outputs_counted_symlinks_not_doublecounted',summary['complete_HODE_bytes_accounting_includes_all_current_writer_outputs']is True)
dhashes=collections.Counter(p['sha256']for p in ns['views']['D']['files']);duplicate_rows=sum(n-1 for n in dhashes.values());check('complete_D_actual_copy_duplicates_observed',duplicate_rows>0)
for path,pin in list(pins.items()):
 r=Path(path).read_bytes();check('final_Source_META_smallOutput_complete_EOF_SHA7ID_'+path,ident(path)==pin['identity']and len(r)==pin['size_bytes']and hashlib.sha256(r).hexdigest()==pin['sha256'])
for path,pin in large_saved.items():check('final_large_payload_stat_only_Root_savedpin_'+path,ident(Path(path))==pin['identity'])
check('final_all_D30dirs_preserved',dirs(D)==pre['D']['directories'])
full(Path(__file__))
out=Path(tempfile.mkdtemp(prefix='axmat_v24_actual_pure_archive_failure_saved_SOURCE_META_review_',dir='/private/tmp'))
for path,raw in raws.items():
 p=Path(path)
 if p.is_relative_to(O):dst=out/'ACTUAL_COMPLETE_SMALL_OUTPUT'/p.relative_to(O)
 elif p.is_relative_to(H):dst=out/'ACTUAL_FAILED_HOST'/p.relative_to(H)
 elif p.is_relative_to(E):dst=out/'ACTUAL_ROOT_SAVED_META'/p.relative_to(E)
 else:dst=out/'SOURCE_AND_INDEPENDENT_AUDITOR'/p.name
 dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
(out/'FULL_EOF_SOURCE_META_SMALL_OUTPUT_INPUT_PINS.json').write_text(json.dumps(pins,indent=2,allow_nan=False)+'\n')
(out/'ROOT_SAVED_COMPLETE_LARGE_GRAPH_TRACE_PINS_NOT_REREAD.json').write_text(json.dumps(dict(source_only=True,Root_original_full_EOF_evidence=large_saved,current_lstat7ID_independently_verified=True,large_rawpayload_rehashed_or_decoded_by_reviewer=False),indent=2,allow_nan=False)+'\n')
review=dict(schema='INDEPENDENT_V24_ACTUAL_FAILED_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1',status='PASS_SAVED_ACTUAL_PURE_CONTROLS_ARCHIVE_FAILURE_EVIDENCE_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,
 actual_Root_failed_terminal_receipt_pin=receiptpin,actual_Root_postclose_writer_terminal_receipt_pin=writerpin,actual_Root_failed_summary_pin=summarypin,actual_Root_complete_postclose_namespace_manifest_pin=nspin,
 actual_watchdog_pin=watchpin,actual_failed_host_result_pin=failedpin,actual_child_complete_control_report_pin=reportpin,actual_complete_order_preserving_snapshot_artifact_pin=privatepin,
 frozen_D_files=353,frozen_D_directories=30,frozen_original_E_files=3,frozen_original_E_directories=1,actual_current_E_files=10,
 namespace_scope=dict(H_files=5,O_regular_files=34,O_original_file_symlinks=2,D_files=353,E_at_namespace_capture=7,E_current=10),
 actual_terminal_exit_code=1,actual_terminal_chunk_id='a1dcb2',actual_original_session=8777,
 actual_child_status='PASS',actual_child_returncode=0,all_original_five_child_protocol_stages_completed=True,all_new_5positive13reject3lastuse_controls_completed=True,
 original_owner_controls=dict(positive=4,reject=3,accepted_str_subtypes=2,partial_reject=2),new_order_preserving_complete_ninefield_artifact_produced=True,
 actual_child_seconds=watch['elapsed_seconds'],actual_own_child_sampled_RSS_MiB=watch['sampled_peak_rss_mib'],actual_child_self_reported_peak_RSS_bytes=report['peak_rss_bytes'],
 failure_cause='Genuine child completed all controls and returned0. Original outer H+O+D archive gate rejected complete Source/output bytes over64MiB. This is whole qualification failure; child PASS does not admit protocol or new helper Q.',
 original_HOD_bytes=hod,complete_scope_regular_bytes=bytes_by_scope,Root_writer_time_HODE_bytes=81916624,Root_true_postclose_writer_receipt_increment_bytes=1876,current_HODE_bytes=hode,
 original_HOD_cap_bytes=64*2**20,archive_gate_bytes_before_failure_record=hod-failedpin['size_bytes'],all353_D_files_exact_fullEOF_SHA7ID_verified=True,complete_D_unique_content_SHA_count=len(dhashes),complete_D_duplicate_content_rows=duplicate_rows,
 two_original_symlinks_lstat_linktext_resolved_target_fullEOF_verified=True,
 Root_saved_complete_large_graph_trace_pins=large_saved,large_graph_or_trace_payload_rehashed_or_decoded_by_reviewer=False,
 entire_pure_protocol_qualified=False,actual_pure_protocol_qualified=False,actual_full_current_graph_verifier_qualified=False,FreshV24_executed=False,new_actual_helper_qualification=None,
 whole_combined_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,
 original_caps_scope=dict(pure_whole_seconds=60,pure_stage_seconds=60,rss_mib=512,HOD_archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
 reviewer_candidate_helper_controller_guard_reader_API_or_business_executed=False,no_numeric_replay_or_material_decode=True,no_repoll_or_retry_performed_by_reviewer=True,
 scope_notes=['Full Source D353 and all declared small H/O/E saved evidence were independently read to EOF and SHA7ID rechecked.',
              'Two complete encoded graph/trace payloads were not reread; their Root fullEOF evidence pins were cross-bound to child report and complete Root namespace; current lstat7ID verified.',
              'Complete original public ninefield insertion order/type/value/floatbits compared from separate order-preserving artifact; only sorted aggregate report correspondence disregards its intentional JSON key sorting.',
              'All genuine child control outcomes are preserved as actual child evidence; whole host failure denies joint protocol/newQ/RSS/build/science qualification.',
              'Outer host elapsed was not saved as a scalar in failure summary; no value invented. Archive exceeds limit independently.',
              'Source duplicates counted honestly, not removed or given an exception to the original cap.'])
(out/'REVIEW.json').write_text(json.dumps(review,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('PASS: saved actual V24 pure archive FAILURE evidence only.\n'+str(len(checks))+' exact independent checks; child0/all5protocol and5positive13reject3lastuse complete; outer actual1/CLOSED, HOD80605706B exceeds unchanged64MiB.\nNo overall protocol/newQ/fresh/RSS/build/INPUT/native/science qualification. Large graph/trace payload not reread.\n')
print(json.dumps(dict(status=review['status'],source_only=True,review_dir=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),check_count=len(checks),all_checks_typed_true=True,blockers=[],actual_child_PASS=True,actual_outer_exit1=True,HOD_bytes=hod,current_HODE_bytes=hode,new_actual_helper_qualification=None),separators=(',',':')))

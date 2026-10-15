"""Independent stdlib saved SOURCE/META review. No reviewed module is imported."""
from pathlib import Path, PurePosixPath
import ast, collections, hashlib, json, math, os, stat, struct, tarfile, tempfile

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_graph_helper_controls_v25_sources';E=B/'actual_complete_graph_helper_controls_v25_receipts'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-host-v25-20261010')
O=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010')
checks=[];pins={};raws={};large_saved={};archive_evidence={}

def check(label,result):
    assert type(result) is bool and label not in {v['check'] for v in checks},label
    checks.append(dict(check=label,passed=result));assert result,label

def identity(path):
    s=Path(path).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def full(path,sha=None):
    p=Path(path);a=identity(p)
    if str(p) in pins:
        got=pins[str(p)];assert a==got['identity'] and (sha is None or sha==got['sha256'])
        return got,raws[str(p)]
    assert stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink(),str(p)
    assert not (p.is_relative_to(O) and a[4]>5*2**20),'large output payload forbidden'
    raw=p.read_bytes();assert identity(p)==a and len(raw)==a[4]
    got=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)
    assert sha is None or got['sha256']==sha,str(p)
    pins[str(p)]=got;raws[str(p)]=raw
    return got,raw

def object_pairs(values):
    out={}
    for k,v in values:assert k not in out;out[k]=v
    return out

def reject_constant(value):raise AssertionError('nonfinite JSON '+value)
def parse(raw):return json.loads(raw,object_pairs_hook=object_pairs,parse_constant=reject_constant)
def read(path,sha=None):
    got,raw=full(path,sha);return parse(raw),got

def repin(expected):
    actual,_=full(expected['path'],expected['sha256'])
    assert expected=={k:actual[k] for k in expected} and set(expected) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'})
    return actual

def stat_only(expected):
    p=Path(expected['path']);a=identity(p)
    assert set(expected) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'}) and a==expected['identity'] and stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink()
    assert len(expected['sha256'])==64 and all(c in '0123456789abcdef' for c in expected['sha256'])
    if 'size_bytes' in expected:assert a[4]==expected['size_bytes']
    large_saved[str(p)]=expected
    return expected

def names(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def directories(root):return {'.':identity(root),**{p.relative_to(root).as_posix():identity(p) for p in root.rglob('*') if p.is_dir() and not p.is_symlink()}}
def exact(a,b,ordered=True):
    if type(a) is not type(b):return False
    if type(a) is dict:return (list(a)==list(b) if ordered else set(a)==set(b)) and all(exact(a[k],b[k],ordered) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y,ordered) for x,y in zip(a,b))
    if type(a) is float:return math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
    return type(a) in (str,int,bool,type(None)) and a==b

def terminal(receipt,chunk):
    t=receipt['terminal_tool_return']
    assert receipt['closed'] is True and type(t['exit_code']) is int and t['exit_code']==0 and t['chunk_id']==chunk and 'session_id' not in t and type(t['output']) is str
    return t

summary,summarypin=read(E/'Root_actual_complete_qualification_postclose_summary.json','782bbb4cc04b07e54fd0e56714093d24b366457ef5127d644db4f36fd8247901')
ns,nspin=read(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json','6ddf0165b0eb2d098e7919a028e90a1902666e93eee02df000c8df2825ff77c0')
receipt,receiptpin=read(E/'Root_actual_complete_qualification_tool_terminal_return.json','e68e11b6601eb4e819033f0e4152a63bafb79d526a0e8ef0f99edab5c6edf00a')
writer,writerpin=read(E/'Root_actual_complete_qualification_postclose_tool_return.json')
t=terminal(receipt,'ca2666');wt=terminal(writer,'28282a')
check('true_Root_pure_outer_and_postclose_writer_closed0',receipt['actual_tool_terminal_return_observed'] is True and writer['original_host_exit_code']==0 and type(writer['original_host_exit_code']) is int)
check('actual_V25_schema_scope_and_success',receipt['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_FULL_EOF_NAMESPACE_V1' and all(x['kind']=='pure' for x in (summary,receipt,ns)) and summary['actual_complete_control_success'] is True and summary['actual_closed'] is True and type(summary['actual_exit_code']) is int and summary['actual_exit_code']==0 and summary['actual_failure'] is None)
obs=receipt['observations']
check('one_original_session35513_true_observations_terminal_no_repoll',len(obs)==3 and obs[0]['operation']=='exec_command' and obs[0]['actual_tool_return']['chunk_id']=='6693a5' and obs[0]['actual_tool_return']['session_id']==35513 and obs[1]['operation']==obs[2]['operation']=='write_stdin' and obs[1]['arguments']['session_id']==obs[2]['arguments']['session_id']==35513 and obs[1]['actual_tool_return']['session_id']==35513 and obs[-1]['actual_tool_return']==t)
check('Root_external_streams_honestly_merged',receipt['original_outputs_preserved'] is True and receipt['merged_stdout_stderr_only'] is True and receipt['independent_stdout_captured'] is False and receipt['independent_stderr_captured'] is False)
pre,prepin=read(summary['actual_prelaunch']['path'],summary['actual_prelaunch']['sha256']);freeze,freezepin=read(pre['source_freeze']['path'],pre['source_freeze']['sha256'])
check('actual_prelaunch_and_original_Source_freeze_full4pins',prepin==summary['actual_prelaunch'] and freezepin==pre['source_freeze'])
check('complete_D9_dir1_Epre3_dir1_frozen_scope',len(pre['D']['files'])==summary['frozen_D_files']==9 and len(pre['D']['directories'])==summary['frozen_D_directories']==1 and len(pre['E']['files'])==summary['frozen_E_files']==3 and len(pre['E']['directories'])==summary['frozen_E_directories']==1 and freeze['source_namespace']==pre['D']==ns['views']['D'])
check('complete_HODE_declared_scope',{k:v['root'] for k,v in ns['views'].items()}==dict(H=str(H),O=str(O),D=str(D),E=str(E)) and [len(ns['views'][k]['files']) for k in ('H','O','D','E')]==[5,34,9,7])
for kind,view in ns['views'].items():
    root=Path(view['root']);expected={Path(v['path']).relative_to(root).as_posix() for v in view['files']}
    if kind=='E':expected|={'Root_actual_complete_qualification_postclose_namespace_manifest.json','Root_actual_complete_qualification_postclose_summary.json','Root_actual_complete_qualification_postclose_tool_return.json'}
    actual_names=names(root);assert actual_names==expected
    for v in view['files']:
        if kind=='O' and v['size_bytes']>5*2**20:stat_only(v)
        else:repin(v)
    current=directories(root)
    assert set(current)==set(view['directories'])
    assert all(current[k]==v for k,v in view['directories'].items() if kind!='E' or k!='.')
    if kind!='O':assert not any(p.is_symlink() for p in root.rglob('*'))
    check('all_'+kind+'_complete_saved_names_dirs_members_SHA7ID_scope',True)
check('only_two_explicit_selfcapture_files_and_true_writer_receipt',ns['E_explicit_self_excluded_current_writer_outputs']==[str(E/'Root_actual_complete_qualification_postclose_namespace_manifest.json'),str(E/'Root_actual_complete_qualification_postclose_summary.json')] and len(names(E))==10)
for v in pre['E']['files']:repin(v)
check('original_D_E_full_before_after_frozen_unchanged',ns['original_frozen_D_E_unchanged_before_writer'] is True and summary['whole_frozen_D_E_files_and_directories_unchanged_before_writer'] is True and directories(D)==pre['D']['directories'])
for v in pre['original_helper_Q_canonical']:repin(v)
repin(pre['installed_helper'])
check('actual_installed3b_and_oldQ_canonical_protected_not_newQ',pre['installed_helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092' and freeze['actual_installed_helper']==pre['installed_helper'] and freeze['new_actual_helper_qualification'] is None and freeze['six_future_business_pins']==[None]*6)

# Independently decode only complete SOURCE tar members. Never extract or execute them.
for role,record in freeze['lossless_complete_Source_archives'].items():
    archivepin=repin(record['compressed_archive']);before=identity(Path(archivepin['path']));original=record['original_complete_package']
    expected={k:dict(size_bytes=v['size_bytes'],sha256=v['sha256']) for k,v in original['members'].items()}
    manifest_rel=Path(original['manifest']['path']).relative_to(original['root']).as_posix()
    expected[manifest_rel]={k:original['manifest'][k] for k in ('size_bytes','sha256')}
    got={};gotdirs=[];python_count=0;selected={}
    with tarfile.open(archivepin['path'],'r|gz') as tar:
        for member in tar:
            name=member.name
            assert name=='.' or (not name.startswith('/') and '..' not in PurePosixPath(name).parts and PurePosixPath(name).as_posix()==name)
            assert name not in got and name not in gotdirs
            if member.isdir():gotdirs.append(name);continue
            assert member.isfile() and not member.issym() and not member.islnk() and name in expected
            stream=tar.extractfile(member);digest=hashlib.sha256();length=0;parts=[]
            for block in iter(lambda:stream.read(2**20),b''):
                digest.update(block);length+=len(block)
                if name.endswith('.py') or name in (manifest_rel,'REVIEW.json'):parts.append(block)
            got[name]=dict(size_bytes=length,sha256=digest.hexdigest());assert length==member.size and got[name]==expected[name]
            if parts:
                raw=b''.join(parts)
                if name.endswith('.py'):ast.parse(raw,filename=name);python_count+=1
                if name==manifest_rel or name=='REVIEW.json' or '/' not in name and name.endswith('.py'):selected[name]=raw
    assert identity(Path(archivepin['path']))==before
    assert got==record['full_decompressed_members']==expected
    assert sorted(gotdirs)==sorted(record['full_decompressed_directories'])==sorted(['.']+list(original['directories']))
    assert len(got)==record['complete_file_count_including_manifest'] and len(gotdirs)==record['complete_directory_count_including_root']
    assert all(record[k] is True for k in ('all_member_bytes_and_SHA_verified_after_decompression','no_original_member_omission','runtime_Source_entrypoints_are_separate_original_bytes'))
    root_manifest=parse(selected[manifest_rel]);root_rows={Path(v['path']).relative_to(original['root']).as_posix():{k:v[k] for k in ('size_bytes','sha256')} for v in root_manifest['members']}
    assert root_rows=={k:v for k,v in expected.items() if k!=manifest_rel}
    assert root_manifest['member_count']==len(root_rows)
    if 'directories' in root_manifest:assert len(root_manifest['directories'])==len(gotdirs)-1
    if role=='sealed_full_ROOT_BOUND_qualification_SOURCE':
        assert len(got)==184 and len(gotdirs)==15 and original==freeze['complete_bound_source']
        for name in ('pure_helper_controls.py','pure_helper_controls_host.py','fresh_verifier_controls.py','fresh_verifier_host.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py'):
            assert selected[name]==raws[str(D/name)]
    else:
        assert len(got)==199 and len(gotdirs)==16 and original==freeze['independent_complete_bound_Source_peer']
        peer=parse(selected['REVIEW.json']);peerpin=freeze['bound_Source_peer_report']
        assert hashlib.sha256(selected['REVIEW.json']).hexdigest()==peerpin['sha256'] and len(selected['REVIEW.json'])==peerpin['size_bytes']
        assert peer['all_checks_typed_true'] is True and peer['blockers']==[] and peer['check_count']==len(peer['checks'])==676 and all(type(v['passed']) is bool and v['passed'] is True for v in peer['checks'])
    archive_evidence[role]=dict(compressed_archive_pin=archivepin,original_complete_manifest_pin=original['manifest'],complete_decompressed_files=len(got),complete_decompressed_directories=len(gotdirs),all_full_bytes_SHA_match_original_Source_and_all_nested_manifests=True,parsed_python_Source_files=python_count,decompressed_members=got,decompressed_directories=sorted(gotdirs),all_five_runtime_entrypoints_original_bytes=(role=='sealed_full_ROOT_BOUND_qualification_SOURCE'))
    check('complete_lossless_Source_archive_'+role,True)
check('both_full_Source184_and_full_peer199_complete_original_directories_preserved',len(archive_evidence)==2)

aliases=ns['views']['O']['original_fixture_symlinks']
assert len(aliases)==2 and {Path(v['path']).relative_to(O).as_posix() for v in aliases}=={'fixture/file_alias.txt','fixture/sealed/alias.txt'}
for v in aliases:
    p=Path(v['path']);assert p.is_symlink() and identity(p)==v['identity'] and os.readlink(p)==v['symlink_target_text'] and str(p.resolve())==v['actual_resolved_target_full_EOF_pin']['path'];repin(v['actual_resolved_target_full_EOF_pin'])
check('all_original_two_symlinks_lstat_text_target_fullEOF',{str(p) for p in O.rglob('*') if p.is_symlink()}=={v['path'] for v in aliases})
host,hostpin=read(H/'result.json');watch,watchpin=read(H/'run/admit.watchdog.json');ledger,_=read(H/'GRAPH_PROTOCOL_CONTROLS/stages.json');report,reportpin=read(O/'ACTUAL_REPORT.json')
check('whole_success_host_saved_and_no_failure_result',host['schema']=='AXMAT_V25_GENUINE_PRIVATE_INACTIVE_AUDIT_PURE_PROTOCOL_CONTROLS_HOST_V1' and host['status']==summary['actual_host_status']=='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' and not os.path.lexists(H/'failed_host_result.json'))
assert ledger['stages']==host['stage_records'] and len(ledger['stages'])==1;stage=ledger['stages'][0]
command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'pure_helper_controls.py'),'--output-dir',str(O)]
check('one_full_genuine_stage_command_and_actual_watch',stage['status']=='PASS' and stage['command']==watch['command']==host['actual_canonical_command']==command and host['watchdog']==watch)
check('true_child_PID31846_return0_original_RSS_time_caps_cleanup',type(watch['pid']) is int and watch['pid']==31846 and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['rss_cap_mib']==512 and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=60 and 0<watch['sampled_peak_rss_mib']<512)
check('actual_child_and_whole_measurements_exact',summary['actual_child_seconds']==watch['elapsed_seconds']==15.438755541923456 and summary['actual_own_child_sampled_peak_RSS_MiB']==watch['sampled_peak_rss_mib']==393.703125 and summary['whole_host_seconds']==host['whole_seconds']==16.95294858305715 and host['whole_seconds']<60)
check('unchanged_host_caps_no_profile_MRO_modification',all(host[k]==v for k,v in dict(whole_wall_cap_seconds=60,stage_wall_cap_seconds=60,rss_cap_mib=512,archive_cap_bytes=64*2**20,threads=1,children_at_once=1,retries=0).items()) and host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False)
for key in ('resources_before','resources_after'):
    r=host[key];assert r['min_free_bytes']==8*2**30 and r['artifact_budget_bytes']==96*2**30 and r['artifact_bytes']+64*2**20<96*2**30 and r['disk_free_bytes']-64*2**20>=8*2**30
check('real_resource_history96_free8_complete_reserve_before_after',True)
for v in host['input_sources']+[host['original_helper'],host['resource_factory']]:
    if Path(v['path']).stat().st_size>5*2**20:stat_only(v)
    else:repin(v)
check('all20_actual_host_ordered_input_sources_and_original_genuine_modules',len(host['input_sources'])==20 and len({v['path'] for v in host['input_sources']+[host['original_helper'],host['resource_factory']]})==20)
for key,actualpin in (('actual_control_report',reportpin),('actual_watchdog',watchpin)):
    assert host[key]=={k:actualpin[k] for k in host[key]}
logpin,lograw=full(H/'run/admit.log',stage['log_sha256']);stdout=parse(lograw)
check('full_child_report_original_complete_protocol_status_and_stdout_pin',report['schema']=='AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16' and report['status']==stdout['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' and report['source_status']=='READY_SOURCE_BOUND_BY_ROOT' and stdout['report']==reportpin and stdout['peak_rss_bytes']==report['peak_rss_bytes']==412827648 and 0<stdout['elapsed_seconds']<watch['elapsed_seconds'])
assert host['actual_admission_stdout']=={k:logpin[k] for k in host['actual_admission_stdout']}
actual_outer=parse(t['output']);check('actual_outer_stdout_true_host_log_pins_external_terminal_required',actual_outer['status']==host['status'] and actual_outer['actual_host_result']=={k:hostpin[k] for k in actual_outer['actual_host_result']} and actual_outer['actual_admission_stdout']=={k:logpin[k] for k in actual_outer['actual_admission_stdout']} and actual_outer['actual_external_Root_terminal_required'] is True)
check('original_child60_512_64MB_onechild_noretry_caps',report['caps']==dict(children=1,json_read_bytes=64*2**20,output_bytes=64*2**20,retries=0,rss_bytes=512*2**20,wall_seconds=60))
labels=['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged']
check('original_all_five_stages_complete_same_scope',len(report['stages'])==5 and [v['stage'] for v in report['stages']]==labels and all(math.isfinite(v['elapsed_seconds']) and 0<=v['elapsed_seconds']<60 and 0<=v['peak_rss_bytes']<512*2**20 and 0<=v['owned_output_bytes']<64*2**20 for v in report['stages']))
check('actual_helper3b_full7ID_Source_current_not_old_Q_credit',report['helper']['path']==pre['installed_helper']['path'] and report['helper']['sha256']==pre['installed_helper']['sha256'] and report['helper']['identity']==pre['installed_helper']['identity'] and report['helper']['source_bytes']==150986 and report['actual_success_pins']['helper']==report['helper'])
for p in D.glob('*.py'):ast.parse(raws[str(p)],filename=str(p))
host_source=raws[str(D/'pure_helper_controls_host.py')].decode();module=raws[str(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')].decode()
check('Source_genuine_619_705_MRO_original_resource_and_archive_logic',all(v in host_source for v in ['WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20','helper.modules();helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)','threads=1,children_at_once=1,retries=0','profile_used=False,supervisor_class_or_MRO_modified=False','archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))',"if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')"]))
check('same_d439_Module_actualref_exacttype_is_complete_state_and_public_contract',pins[str(D/'inactive_audit_snapshot_controls_SOURCE_ONLY.py')]['sha256']=='d439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483' and 'id(value), value)' in module and 'type(lrow[3]) is type(rrow[3]) and lrow[3] is rrow[3]' in module and module.count('complete_audit_state_equal(')==8)
repin(report['private_snapshot_control_Source'])
private,privatepin=read(O/'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json')
check('complete_order_artifact_pin_and_sorted_public_report_content',privatepin==report['private_inactive_audit_snapshot_controls_order_preserved_artifact'] and exact(private,report['private_inactive_audit_snapshot_controls'],ordered=False))
fields=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
positives=['empty_owned_True','same_actual_read_duplicate_and_Popen_owned_True','control_only_floatbits_strattrs_owned_True','default_Audit_subclass','default_records_dict_subclass']
rejects=['flag_None','flag_zero','flag_one','flag_string','flag_list','flag_dict','Audit_subclass_True','records_dict_subclass_True','records_list_True','recording_True','stale_active_registry_identity','active_True','active_False']
failures=['invalid_second_row_before_clear','missing_attempt_count_before_clear','nonfinite_clone_after_clear']
check('all5positive13reject3lastuse_complete_order',[v['case'] for v in private['positive_controls']]==positives and [v['case'] for v in private['private_guard_rejections']]==rejects and [v['case'] for v in private['last_use_failure_controls']]==failures)
for i,c in enumerate(private['positive_controls']):
    a=c['actual_full_expected_snapshot'];b=c['actual_full_consumed_snapshot' if i<3 else 'actual_full_default_snapshot']
    assert list(a)==list(b)==fields and exact(a,b) and c['default_and_explicitFalse_complete_state_unchanged'] is True and c['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default'] is True
    if i<3:assert c['owned_same_builtin_records_map_completely_cleared'] is True and c['all_other_audit_state_and_actual_Popen_references_unchanged'] is True and c['augmented_control_fields_not_claimed_as_actual_open_trace'] is (i==2)
    else:assert c['private_True_not_permitted_for_subclass'] is True
check('all_positive_complete_nested_type_order_values_attrs_floatbits9fields',True)
for i,c in enumerate(private['private_guard_rejections']):
    message='private read-open snapshot consume flag must be an exact bool' if i<6 else ('end the read-open audit phase before freezing its trace' if i>=11 else 'private read-open snapshot consume requires an owned inactive builtin audit')
    assert c['rejected'] is True and c['class_name']=='InputGraphError' and c['message']==message and c['complete_audit_state_identity_type_order_value_bits_unchanged'] is True
check('all13_guard_rejections_exact_errors_and_full_state_unchanged',True)
for i,c in enumerate(private['last_use_failure_controls']):
    after=i==2
    assert c['actual_default_error']==c['actual_private_error'] and c['original_error_class_and_message_retained'] is True and c['no_transactional_private_mode_promise'] is True and c['both_callers_unchanged_before_clear_or_default'] is (not after) and c['private_clone_failure_after_clear_consumption_observed'] is after
check('all3_lastuse_failure_order_and_honest_nontransactional_clone_failure',True)
check('one_true_Popen_observation_complete9field_no_crossrun_normalization',list(private['actual_single_Popen_observation'])==fields and private['actual_child_returncode']==0 and private['actual_stdout_hex']==b'inactive audit metadata protocol\n'.hex() and private['actual_stderr_hex']=='' and len(private['actual_single_Popen_observation']['subprocess_records'])==1 and all(private[k] is True for k in ('actual_same_observation_full_record_role_comparison','no_cross_process_PID_FD_inode_normalization','default_original_complete_protocol_preserved','no_new_fixture_or_material_file_created')) and all(private[k] is False for k in ('native_or_numeric_component_executed','helper_qualification_created','business_or_science_qualification_created')))
fixture,_=read(O/'small_fixture_controls.json');codec,_=read(O/'small_codec_and_rejection_controls.json')
check('whole_original_fixture9categories2subclasses_fullproducer_and_caller',fixture['producer_full_exact_values_types_order_floatbits'] is True and fixture['caller_full_value_and_mutable_identity_preserved'] is True and len(fixture['accepted_str_subclass_equivalence_controls'])==2 and fixture['all_nine_closure_categories']==['capture','code_environment','component_ancestry','component_terminals','dedup_build','memory_build','original92_build','physical_build','source_namespace'])
check('whole_original_codec61rejects_default_nonmutation_all_lossless_cases',len(codec['rejections'])==report['small_codecs']['rejections']==61 and codec['all_default_inputs_unmodified'] is True and codec['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True)
owner=report['private_owner_consume_controls']
assert len(owner['positive_controls'])==4 and {v['case'] for v in owner['positive_controls']}=={'default_list','default_tuple','explicit_False_list','owned_builtin_list_True'} and len(owner['private_guard_rejections'])==3 and len(owner['accepted_str_subclass_equivalence_controls'])==2 and len(owner['partial_invalid_second_owner_rejections'])==2
assert all(exact(c['expected_complete_descriptor_signature'],c['actual_complete_descriptor_signature']) for c in owner['positive_controls']+owner['accepted_str_subclass_equivalence_controls'])
assert all(owner[k] is True for k in ('first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created')) and owner['new_helper_qualification_created'] is False and owner['business_or_science_qualification_created'] is False
check('whole_owner4positive3reject2subtypes2partial_complete_values_types_order_bits',True)
trace=report['full_new_creation_trace'];graph=report['full_old_saved_graph']
check('complete63379_trace175886_attempts_and_all_original_roundtrip_flags',trace['full_record_count']==trace['table_rows']==63379 and trace['actual_attempt_count']==175886 and trace['subprocess_record_count']==0 and all(trace[k] is True for k in ('default_source_nonmutation','exact_full_roundtrip','persisted_full_trace_exact_order_type_floatbit_inverse')))
check('whole_oldgraph_original_two_strict_entrances_full_metadata_equal',exact(graph['complete_original_metadata'],graph['normal_strict_file_entrance_full_semantics_and_counts']) and exact(graph['complete_original_metadata'],graph['normal_strict_payload_entrance_full_semantics_and_counts']) and all(graph[k] is True for k in ('full_default_roundtrip_exact','no_two_complete_decoded_graphs_between_strict_stages','old_read_trace_not_replaced_by_new_trace','original_legacy_semantic_sha_preserved')))
check('oldgraph_complete36776files237767requirements62332trace_counts_original_hashes',graph['complete_original_metadata']['complete_counts']['canonical_files']==36776 and graph['complete_original_metadata']['complete_counts']['requirements']==237767 and graph['complete_original_metadata']['complete_counts']['read_trace_records']==62332 and graph['complete_original_metadata']['legacy_semantic_sha256']=='51f051f627181e2b815f0dd4a77d7f40e718c268695c33c5ccfbde74c6b8f1f9' and graph['complete_original_metadata']['wire_content_sha256']=='ee2cabfd7b93d10bb7c5dc17c01a3d190202faf16eb7d2d8f8125d9507671427')
check('both_large_encoded_outputs_Root_fullEOF_pins_exact_crossbinding_not_reread',trace['encoded_artifact']==report['actual_success_pins']['encoded_new_trace']==large_saved[str(O/'full_new_creation_trace.encoded.json')] and graph['stored_wholegraph']==report['actual_success_pins']['encoded_wholegraph']==large_saved[str(O/'full_old_saved_graph.encoded.json')])
saved=report['saved_input_identity_before'];check('both_large_original_inputs_full_before_after_root_pins_exact',saved==report['saved_input_bytes_identity_after'] and len(saved)==2 and graph['input']==saved[0] and trace['input']==saved[1] and all(v['identity']==large_saved[v['path']]['identity'] and v['sha256']==large_saved[v['path']]['sha256'] for v in saved))
check('all_actual_success_pins_old_defaults_and_new_controls_preserved',report['actual_success_pins']['encoded_wholegraph']==graph['stored_wholegraph'] and report['actual_success_pins']['encoded_new_trace']==trace['encoded_artifact'])
actual_writer=parse(wt['output']);check('true_postclose_writer_stdout_full_independent_summary_namespace_terminal_pins',actual_writer['summary']==summarypin and actual_writer['namespace_manifest']==nspin and actual_writer['actual_terminal_receipt']==receiptpin and actual_writer['actual_closed_success'] is True and type(actual_writer['actual_exit_code']) is int and actual_writer['actual_exit_code']==0)
check('Root_complete_namespace_terminal_summary_crossbound',summary['actual_terminal_receipt']==receiptpin and summary['namespace_manifest']==nspin and ns['closed_actual_tool']==receiptpin)
bundle,bundlepin=read(summary['Root_actual_bundle']['path'],summary['Root_actual_bundle']['sha256']);check('true_original_Root_command_and_closed_observation_bundle',bundlepin==summary['Root_actual_bundle'] and bundle['terminal_tool_return']==t and bundle['observations']==obs and bundle['actual_command']==receipt['actual_command'])
repin(summary['Source_postclose_writer'])
def size(root):return sum(p.lstat().st_size for p in root.rglob('*') if stat.S_ISREG(p.lstat().st_mode))
bytes_by_scope={k:size(p) for k,p in dict(H=H,O=O,D=D,E=E).items()};hod=sum(bytes_by_scope[k] for k in ('H','O','D'));hode=hod+bytes_by_scope['E']
check('whole_HOD62499039_original64MB_cap_no_exception',hod==summary['normal_HOD_bytes']==62499039 and hod<64*2**20 and summary['normal_host_archive_scope']=='H+O+D' and summary['original_archive_cap_bytes']==64*2**20 and summary['original_normal_archive_under_cap'] is True and host['archive_before_result_bytes']==hod-hostpin['size_bytes'])
check('honest_writerHODE63391049_plus_realreceipt1868_all_under64MB',summary['complete_HODE_bytes']==63391049 and writerpin['size_bytes']==1868 and hode==63391049+1868 and hode<64*2**20 and summary['Root_separate_conservative_HODE_under_64MiB'] is True and summary['complete_HODE_bytes_accounting_includes_all_current_writer_outputs'] is True)
check('saved_pure_success_not_newQ_fresh_build_INPUT_native_science',summary['new_actual_helper_qualification'] is None and receipt['new_actual_helper_qualification'] is None and all(summary[k] is False for k in ('actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')) and all(report[k] is False for k in ('business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')) and host['native_RSS_verified'] is False)
for path,pin in pins.items():
    p=Path(path);raw=p.read_bytes();assert identity(p)==pin['identity'] and len(raw)==pin['size_bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
for path,pin in large_saved.items():assert identity(Path(path))==pin['identity']
check('final_all_declared_Source_META_smallOutput_fullEOF_SHA7ID_and_large_stat_only',True)
check('final_D9_Epre3_frozen_namespace_directories_unchanged',directories(D)==pre['D']['directories'] and all(identity(Path(v['path']))==v['identity'] for v in pre['E']['files']))
full(Path(__file__))
out=Path(tempfile.mkdtemp(prefix='axmat_v25_actual_complete_pure_saved_Source_META_review_',dir='/private/tmp'))
for path,raw in raws.items():
    p=Path(path)
    if p.is_relative_to(O):dst=out/'ACTUAL_COMPLETE_SMALL_OUTPUT'/p.relative_to(O)
    elif p.is_relative_to(H):dst=out/'ACTUAL_SUCCESS_HOST'/p.relative_to(H)
    elif p.is_relative_to(E):dst=out/'ACTUAL_ROOT_SAVED_META'/p.relative_to(E)
    elif p.is_relative_to(D):dst=out/'COMPLETE_FROZEN_SOURCE_WITH_LOSSLESS_ARCHIVES'/p.relative_to(D)
    else:continue
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
(out/'review_V25_actual_complete_pure_saved_Source_META_stdlib.py').write_bytes(Path(__file__).read_bytes())
(out/'FULL_SOURCE_ARCHIVE_STREAMED_MEMBER_EVIDENCE.json').write_text(json.dumps(archive_evidence,indent=2,allow_nan=False)+'\n')
(out/'FULL_EOF_Source_META_SMALL_OUTPUT_INPUT_PINS.json').write_text(json.dumps(pins,indent=2,allow_nan=False)+'\n')
(out/'ROOT_SAVED_LARGE_GRAPH_TRACE_PINS_NOT_REREAD.json').write_text(json.dumps(dict(Root_fullEOF_saved_pins=large_saved,independently_lstat7ID_verified=True,largepayload_rehashed_or_decoded=False),indent=2,allow_nan=False)+'\n')
review=dict(schema='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1',status='PASS_SAVED_ACTUAL_PURE_CONTROLS_SOURCE_META_ONLY',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,actual_Root_terminal_receipt_pin=receiptpin,actual_Root_postclose_writer_terminal_receipt_pin=writerpin,actual_Root_pure_summary_pin=summarypin,actual_complete_HODE_namespace_manifest_pin=nspin,actual_host_pin=hostpin,actual_child_watchdog_pin=watchpin,actual_full_control_report_pin=reportpin,actual_full_order_preserving_control_artifact_pin=privatepin,actual_outer_exit_code=0,actual_outer_terminal_chunk='ca2666',actual_original_session=35513,actual_child_returncode=0,actual_child_PID=31846,actual_child_seconds=watch['elapsed_seconds'],actual_child_sampled_RSS_MiB=watch['sampled_peak_rss_mib'],actual_whole_seconds=host['whole_seconds'],full_frozen_D_files=9,full_frozen_D_directories=1,full_original_E_files=3,full_original_E_directories=1,complete_bound_Source_archive_files=184,complete_bound_Source_peer_archive_files=199,full_Source_streamed_bytes_hash_verified=True,all_five_direct_Source_original_bytes_verified=True,original_all5stage_protocol_scope_preserved=True,original_codec_reject_count=61,original_owner_controls=dict(positive=4,reject=3,strsubtypes=2,partialreject=2),new_private_snapshot_controls=dict(positive=5,reject=13,lastusefailure=3),public9fields_complete_nested_types_order_values_floatbits_verified=True,same_actual_Popen_observation_no_crossrun_normalization_verified=True,two_original_symlinks_full_text_lstat_targetEOF_verified=True,original_HOD_bytes=hod,Root_writer_HODE_bytes=summary['complete_HODE_bytes'],current_HODE_bytes=hode,complete_scope_regular_bytes=bytes_by_scope,original_cap_bytes=64*2**20,original_caps=dict(whole_seconds=60,stage_seconds=60,rss_mib=512,HOD_archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),Root_saved_full_large_payload_pins=large_saved,large_graph_trace_payload_rehashed_or_decoded=False,new_actual_helper_qualification=None,actual_full_current_graph_fresh_verifier_qualified=False,whole_combined_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,reviewer_candidate_helper_controller_guard_reader_API_or_business_executed=False,no_numeric_replay_material_or_DB_read=True,no_repoll_or_retry_by_reviewer=True,scope_notes=['Successful complete pure control evidence only; no new joint helper Q or fresh/build/science credit.','Complete Source and complete independent Source peer retained as lossless tar.gz; independently streamed all383 files plus all31 directories, including each original and nested manifest.','Entire nested controls compared without adding one label per tree node; sorted ACTUAL_REPORT dict correspondence alone ignores its intentional sorted JSON keys; separate ordered artifact retains all insertion order.','Two complete original graph/trace inputs and two encoded output payloads were not reread; Root fullEOF saved pins cross-bound to child and namespace with independent current lstat7ID.','Clone failure after clear honestly consumes private map; it has no transactional promise.','No fresh V25 namespace was read or touched.'])
(out/'REVIEW.json').write_text(json.dumps(review,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('PASS: V25 saved actual complete PURE success SOURCE/META only.\nOriginal5stage/fixtures/61reject/owner4+3+2+2 and new5+13+3 complete; actual outer0 and genuine child0.\nAll184+199 Source archive members and original directories lossless; direct5Source bytes unchanged.\nOriginal64MiB cap retained: HOD62499039B and currentHODE63392917B. No new jointQ/fresh/build/INPUT/native/science credit.\nLargegraph/trace payload not reread.\n')
print(json.dumps(dict(status=review['status'],source_only=True,review_dir=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),check_count=len(checks),all_checks_typed_true=True,blockers=[],actual_outer_EXIT0=True,actual_child_EXIT0=True,HOD_bytes=hod,current_HODE_bytes=hode,new_actual_helper_qualification=None),separators=(',',':')))

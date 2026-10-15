import ast,hashlib,json,math,os,stat,tempfile
from pathlib import Path
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_sources';E=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts'
H=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v23-20261010';O=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010';C=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v23-20261010'
CHECKS=[];READS={};RAW={};STAT={}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def check(k,v):
    assert type(v)is bool and v,k
    CHECKS.append(dict(check='S%05d: '%(len(CHECKS)+1)+k,passed=True))
def identity(p):
    s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def validpin(q):
    return type(q)is dict and set(q)=={'path','sha256','size_bytes','identity'}and type(q['path'])is str and Path(q['path']).is_absolute()and type(q['sha256'])is str and len(q['sha256'])==64 and all(x in '0123456789abcdef'for x in q['sha256'])and type(q['size_bytes'])is int and q['size_bytes']>=0 and type(q['identity'])is list and len(q['identity'])==7 and all(type(x)is int and x>=0 for x in q['identity'])and q['identity'][3]==1 and q['identity'][4]==q['size_bytes']
def pin(p,save=False):
    p=Path(p);check('bounded_read_only_Source_META_not_large_payload '+str(p),p.is_relative_to(D)or p.is_relative_to(E)or p==H/'result.json'or p==H/'native_run/native_xsm_ascii.log'or p==H/'native_run/native_xsm_ascii.watchdog.json'or p==H/'COMPLETE_NATIVE_XSM_ASCII/stages.json'or p==H/'runtime/run_bounded_dragon.py'or p==O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json'or p in(O/'A/complete_native_ownership_evidence_summary.json',O/'B/complete_native_ownership_evidence_summary.json')or p==C/'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json')
    check('Source_META_extensions_only '+str(p),p.suffix in('.py','.json','.txt','.md','.log','.c','.h','.f'))
    i=identity(p);check('actual_regular_singlelink_noalias '+str(p),p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1)
    with p.open('rb')as f:
        check('beforefd_7ID '+str(p),[q for q in(i[0],i[1],i[2],i[3],i[4],i[5],i[6])]==[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]if(s:=os.fstat(f.fileno()))else False)
        raw=f.read();check('actual_full_EOF '+str(p),len(raw)==i[4]and f.read(1)==b'');s=os.fstat(f.fileno());check('afterfd_7ID '+str(p),[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i)
    check('afterpath_7ID '+str(p),identity(p)==i)
    q=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
    if str(p)in READS:check('bounded_Source_META_fullpin_stable '+str(p),READS[str(p)]==q)
    READS[str(p)]=q
    if save:RAW[str(p)]=raw
    return q,raw
def read(p,sha=None):
    q,raw=pin(p,True)
    if sha:check('fixed_complete_Source_META_SHA '+str(p),q['sha256']==sha)
    value=json.loads(raw)
    def finite(v):
        if type(v)is dict:return all(finite(x)for x in v.values())
        if type(v)is list:return all(finite(x)for x in v)
        return type(v)is not float or math.isfinite(v)
    check('all_saved_META_finite '+str(p),finite(value));return value,q
def projected(q):return {k:q[k]for k in('path','sha256','identity')}
def view(root):
    files={};dirs={};syms={}
    for p in[root,*sorted(root.rglob('*'))]:
        i=identity(p);rel=str(p.relative_to(root));check('namespace_noalias_or_special '+str(p),not stat.S_ISLNK(i[2])and(stat.S_ISREG(i[2])or stat.S_ISDIR(i[2])))
        if stat.S_ISDIR(i[2]):dirs[rel]=i
        else:files[rel]=i
    return dict(root=str(root),files=files,directories=dirs,symlinks=syms)
def checkview(v,current,fullread):
    root=Path(v['root']);check('complete_declared_namespace_present '+str(root),v['present']is True and v['symlinks']=={} and set(v['files'])==set(current['files'])and set(v['directories'])==set(current['directories']))
    for rel,q in v['files'].items():
        check('every_saved_declared_pin_typed '+str(root/rel),validpin(q)and q['path']==str(root/rel))
        check('every_declared_current_stat7ID '+str(root/rel),current['files'][rel]==q['identity']);STAT[str(root/rel)]=q
        if fullread:
            actual,_=pin(root/rel);check('Source_META_original_complete_SHA_7ID '+str(root/rel),actual==q)
    for rel,q in v['directories'].items():check('complete_directory_stat7ID '+str(root/rel),current['directories'][rel]==q)
def write(p,x):
    with p.open('x')as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def main():
    summary,sp=read(E/'Root_actual_complete_native_postclose_summary.json','64edfd224139a20cee15c32e0cf8823efa54f13357fd4813526fa20538dffb61')
    receipt,tp=read(E/'Root_actual_complete_native_tool_terminal_return.json','099fd059d741515e13e9b2b2ab46f43f0a8d17c3b5840d99cc367a91f7f6863e')
    ns,nsp=read(E/'Root_actual_complete_native_postclose_namespace_manifest.json','8bdc7cbdcdfe3b8f1c4603195a43428de38b641bdf5145eadca85975d281faf9')
    writer_receipt,wrp=read(E/'Root_actual_complete_native_postclose_META_writer_tool_return.json','ca2451ab69f37d2b6794c3b6ed3e8a978920989296e9c5910f7422a0c84a4d3c')
    pre,pp=read(Path(summary['actual_prelaunch']['path']),'713c6a1be41a67eef83fb8a6f7cce4fdf8bbe1cbc85775b174af77f873cc4bdf')
    host,hp=read(H/'result.json','380ff9e25ec1de8db3542c2534a67bce63b3359f2ef965e8551424b01d6a5acc')
    child,cp=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json','d3346b6cb10d12178d06ef6267bec3f0118962cd71796d864dd8329ea47b671c')
    watch,wp=read(H/'native_run/native_xsm_ascii.watchdog.json','7ab7ff87128c673ea6a12cfd4140bef22f7fa3e116b4fdf737983b402c4589f2')
    log,lp=read(H/'native_run/native_xsm_ascii.log','a175485dcfad69ce7506aaebdc5d54a350b428e523a47a2268ed2b4945cb7a2d')
    controls,ctp=read(C/'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json')
    binding,bp=read(D/'Root_actual_native_SOURCE_binding.json','765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87')
    tr=receipt['terminal_tool_return'];initial=receipt['initial_tool_return'];obs=receipt['observations']
    check('actual_native_Root_CLOSED_typed0_once_observation_same_handle_no_repoll',receipt['schema']=='ROOT_V23_ACTUAL_COMPLETE_NATIVE_TOOL_TERMINAL_RETURN_V1'and receipt['closed']is True and receipt['observed_terminal']is True and receipt['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']==receipt['actual_terminal_chunk']=='5a01da'and initial['chunk_id']=='439d29'and type(initial['session_id'])is int and initial['session_id']==81872 and len(obs)==1 and obs[0]['args']['session_id']==81872 and obs[0]['actual']==tr)
    outer=json.loads(tr['output']);check('true_outer_native_host_saved_full3pin_matches_current',outer['status']==host['status']and outer['actual_host_result']==projected(hp)and outer['actual_external_Root_terminal_required']is True)
    check('Root_outer_launch_original_single_thread_Python_B',receipt['args']['cmd'].endswith('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'Root_bound_complete_native_genuine_host.py'))and all(k+'=1'in receipt['args']['cmd']for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')))
    check('Root_summary_success_scope_not_generic_native_science_admission',summary['schema']=='ROOT_V23_ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_POSTCLOSE_SUMMARY_V1'and summary['status']=='ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_EXIT0_ONLY_PENDING_INDEPENDENT_SAVED_REVIEW'and type(summary['actual_exit_code'])is int and summary['actual_exit_code']==0 and summary['closed']is True and summary['native_persisted_XSM_value_bits_verified']is True and summary['all_complete_A_B_scopes_retained_and_verified']is True)
    check('summary_fullpin_receipt_NS_prelaunch_child_host_coupled',summary['actual_tool_receipt']==tp and summary['namespace_manifest']==nsp and summary['actual_prelaunch']==pp and summary['actual_child_report']==cp and summary['actual_host_result']==hp and summary['actual_failed_host_result']is None)
    check('actual_prelaunch_freeze_Source_only_complete_scope',pre['schema']=='ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1'and pre['native_executed']is False and pre['genuine_guard_MRO_verified']is True and pre['full129_material_payloads_not_rehashed_by_this_preflight']is True and pre['complete129_payloads_will_be_fresh_EOF_verified_by_genuine_host_before_and_after']is True and pre['no_runtime_E_append']is True)
    check('namespace_Root_full_EOF_claim_is_Root_evidence_no_independent_payload_hash_claim',ns['schema']=='ROOT_V23_ACTUAL_NATIVE_COMPLETE_POSTCLOSE_NAMESPACES_V1'and ns['all_current_files_full_EOF_SHA7ID']is True and ns['complete_D_unchanged']is True and ns['all_original_E_files_unchanged']is True and ns['E_directory_identity_after_postclose_appends_claimed_unchanged']is False and ns['namespace_snapshot_before_this_manifest_and_summary_append']is True)
    check('namespace_pin_receipt_prelaunch_writer_coupling',ns['actual_tool_receipt']==tp and ns['prelaunch']==pp and ns['writer']['sha256']=='abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139')
    current={str(root):view(root)for root in(H,O,C,D,E)}
    declared={v['root']:v for v in ns['namespaces']};check('all_HOCDE_roots_exact_original_order',list(declared)==list(current))
    for root in(H,O,C,D):checkview(declared[str(root)],current[str(root)],root==D)
    ev=declared[str(E)];ecurrent=current[str(E)];post3={'Root_actual_complete_native_postclose_META_writer_tool_return.json','Root_actual_complete_native_postclose_namespace_manifest.json','Root_actual_complete_native_postclose_summary.json'}
    check('current_E_exact_three_postwriter_appends',set(ecurrent['files'])==set(ev['files'])|post3 and len(ecurrent['files'])==382)
    for rel,q in ev['files'].items():check('NS_E_complete_original_fullpin '+rel,pin(E/rel)[0]==q)
    check('complete_D957_dirs58_exact_prelaunch_and_host_frozen',len(declared[str(D)]['files'])==957 and len(declared[str(D)]['directories'])==58 and declared[str(D)]==pre['complete_D_frozen']and len(host['complete_source_freeze'])==957 and {str(D/rel):q for rel,q in declared[str(D)]['files'].items()}=={q['path']:{**q,'size_bytes':q['identity'][4]}for q in host['complete_source_freeze']}and host['complete_source_directory_freeze']=={str(D/rel):q for rel,q in declared[str(D)]['directories'].items()})
    pref=pre['complete_E_frozen_before_actual_launch'];check('pre_E374_dirs22_exact_host_scope',len(pref['files'])==374 and len(pref['directories'])==22 and len(host['complete_receipt_input_freeze'])==374 and {str(E/k):q for k,q in pref['files'].items()}=={q['path']:{**q,'size_bytes':q['identity'][4]}for q in host['complete_receipt_input_freeze']}and host['complete_receipt_directory_freeze']=={str(E/k):q for k,q in pref['directories'].items()})
    post5={'Root_actual_complete_native_external_host_merged_stdout_stderr.log','Root_actual_complete_native_tool_terminal_return.json','Root_actual_native_prelaunch_frozen_D_E.json','Root_actual_native_prelaunch_source.py','Root_actual_native_prelaunch_tool_return.json'}
    check('E_NS379_exact_five_postclose_capture_appends',set(ev['files'])==set(pref['files'])|post5 and len(ev['files'])==379)
    for k,q in pref['files'].items():check('pre_E_original_frozen_fullpin_preserved '+k,q==ev['files'][k]and pin(E/k)[0]==q)
    for k,q in pref['directories'].items():
        if k!='.':check('original_E_subdirectory_frozen_7ID '+k,ecurrent['directories'][k]==q)
    check('E_root_identity_change_honest_not_claimed_unchanged',ecurrent['directories']['.']!=pref['directories']['.']and ns['E_directory_identity_after_postclose_appends_claimed_unchanged']is False)
    check('all_original_caps_exact_all_saved_layers',all(q['original_caps']==CAPS for q in(summary,host,child,binding,pre))and all(type(v)is int for v in CAPS.values()))
    check('one_genuine_native_stage_PASS_real_watch_return0',len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS'and host['stage_records'][0]['label']=='native_run/native_xsm_ascii'and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True)
    check('actual_same_native_command_all_PID_layers',host['actual_native']['command']==watch['command']==host['stage_records'][0]['command']and child['actual_child_PID']==watch['pid']==26263 and child['actual_parent_PID']==host['actual_host_PID']==26261 and watch['command'][-2:]==['--expected-parent-pid','26261'])
    check('actual_saved_child_native_metrics_original_caps',watch['elapsed_seconds']==37.24711258406751 and watch['sampled_peak_rss_mib']==49.96875 and watch['wall_cap_seconds']==599.7947604169603 and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and 0<watch['sampled_peak_rss_mib']<512 and host['whole_seconds']==39.105851166998036 and host['whole_seconds']<1800)
    check('full_report_watch_log_Sourcebinding_pin_coupling',host['actual_native']['report']==projected(cp)and host['actual_native']['watchdog_file']==projected(wp)and host['actual_native']['actual_merged_child_stdout_and_stderr']==projected(lp)and host['actual_native']['watchdog']==watch==summary['actual_outer_watchdog']and log['report']==cp and log['status']==child['status']and child['source_binding']==bp==pre['actual_binding'])
    check('merged_stdout_stderr_scope_not_invented_independent_stderr',host['actual_native']['child_separate_stderr_saved']is False and summary['outer_tool_output_scope']=='ACTUAL_EXEC_COMMAND_MERGED_EXTERNAL_HOST_STDOUT_STDERR'and summary['separate_external_host_stderr_saved']is False and summary['independent_external_host_stderr_empty_verified']is False and receipt['separate_external_host_stderr_saved']is False)
    for label,res in(('before',host['resources_before']),('after',host['resources_after'])):
        check('genuine_dynamic_complete_history_resources_'+label,res['min_free_bytes']==8*2**30 and res['artifact_budget_bytes']==96*2**30 and res['artifact_bytes']<96*2**30 and res['disk_free_bytes']>=8*2**30 and res['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'and res['resource_scope_contract']['all_declared_extras_retained']is True and res['resource_scope_contract']['entire_project_artifact_cap_claimed']is False)
    check('initial_real_resources_reserve_full2GiB',host['resources_before']['artifact_bytes']+2*2**30<96*2**30 and host['resources_before']['disk_free_bytes']-2*2**30>=8*2**30)
    check('unchanged_genuine_guard_MRO_no_profile_onechild_threads1_retry0',host['supervisor_class_or_MRO_modified']is False and host['profile_used']is False and (host['threads'],host['children_at_once'],host['retries'])==(1,1,0))
    stageSource,stagepin=read(H/'COMPLETE_NATIVE_XSM_ASCII/stages.json');check('actual_stage_ledger_whole_saved_scope_matches_host',type(stageSource)is dict and set(stageSource)=={'stages'} and stageSource['stages']==host['stage_records'])
    inputs={q['path']:q for q in host['input_sources']};check('complete_original_129_saved_pins_projected_to_actual_host_inputs',len(binding['complete_input_pins'])==129 and len({q['path']for q in binding['complete_input_pins']})==129 and all(inputs[q['path']]==projected(q)for q in binding['complete_input_pins']))
    for name in('qualified_source_manifest','host_template','checker_template','binder'):check('actual_Source_contract_pin_retained_'+name,host['actual_author_Source_contract'][name]==binding['actual_author_Source_contract'][name])
    check('source_peer_scope4528_bound_and_failed_BUILD_retained',host['actual_Source_scope_coupling']==binding['actual_Source_scope_coupling']and host['actual_Source_scope_coupling']['independent_full_Source_checks_count']==4528 and host['prior_actual_V22_build_terminal']['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'and type(host['prior_actual_V22_build_terminal']['terminal_tool_return']['exit_code'])is int and host['prior_actual_V22_build_terminal']['terminal_tool_return']['exit_code']==1)
    check('child_complete_state_order_A_then_B',child['state_order']==['A','B']and[row['state']for row in child['states']]==['A','B']and child['all_complete_state_scope_retained']is True and child['native_persisted_XSM_value_bits_verified']is True)
    states=[]
    for row in child['states']:
        for key,expected in(('complete_MACROLIB',(19619,19990,2264113)),('complete_MICROLIB',(23895,24842,18670730))):
            r=row[key];check(row['state']+'_'+key+'_all_original_records_headers_numeric_components',(r['records'],r['physical_headers_including_all_closes'],r['numeric_components'])==expected)
            check(row['state']+'_'+key+'_zero_value_bit_mismatches_and_no_omitted_zero_length',type(r['mismatching_native_value_bit_records'])is int and r['mismatching_native_value_bit_records']==0 and r['full_record_domain_equal']is True and type(r['original_ASCII_export_omitted_native_zero_length_records'])is int and r['original_ASCII_export_omitted_native_zero_length_records']==0)
            for name in('native_physical_preorder_equal_original_ASCII','all_complete_orders_preserved_on_disk','original_byte_and_parser_bits_preserved','all_persisted_native_value_bits_equal_ASCII','original_LCM_copy_physical_record_order_verified'):check(row['state']+'_'+key+'_'+name,r[name]is True)
            check(row['state']+'_'+key+'_direct_API_export_order_explicitly_NOT_equal',r['native_XSM_API_export_preorder_equal_original_ASCII']is False and 'LCM copy'in r['order_source_note']and 'no name sorting'in r['order_source_note'])
            absent=declared[str(O)]['files'][row['state']+'/'+('MACROLIB'if key=='complete_MACROLIB'else'MICROLIB')+'_complete_native_records_absent_from_original_ASCII.jsonl'];check(row['state']+'_'+key+'_zero_omission_file_declared_size_zero',absent['size_bytes']==0)
        ownership,ownpin=read(O/row['state']/'complete_native_ownership_evidence_summary.json');check(row['state']+'_full_small_ownership_META_equals_child_report',ownership==row['complete_original_ownership_evidence'])
        check(row['state']+'_370x8x3_32fission_complete_native_Metadata_scope',ownership['root_full_STATE_VECTOR'][:5]==[8,62,370,3,1]and ownership['macro_full_STATE_VECTOR'][:4]==[370,8,3,32]and ownership['original_macro_fission_components']==32 and ownership['original_macro_fission_component_records']==740 and ownership['full_sparse_rows']==8880 and ownership['TRANC_group_rows']==370 and ownership['isotope_rows']==62 and ownership['complete_raw_micro_and_macro_field_maps_saved']is True)
        check(row['state']+'_old_fission_index_contract_gap_not_filled_or_granted',ownership['unchanged_old_contract_expected_fission_index_count']==256 and ownership['actual_original_fission_index_count']==64 and ownership['old_contract_gap_retained']is True and ownership['no_index_repair_or_fill']is True)
        states.append(dict(state=row['state'],MACRO=row['complete_MACROLIB'],MICRO=row['complete_MICROLIB'],ownership_summary_pin=ownpin,native_persisted_value_bits_verified=True,source_original_memory_bits_not_qualified=True))
    falsekeys=['historical_native_RAM_bits_verified','original_XSM_memory_bits_verified','reaction_multiplicity_qualified','TRANC_semantics_qualified','physical_neutron_balance_qualified','coupled_370group_reference_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','native_transport_executed','whole_combined_build_or_INPUT_qualified']
    for objlabel,obj in[('child',child),*[(r['state'],r)for r in child['states']],*[(r['state']+'_owner',r['complete_original_ownership_evidence'])for r in child['states']]]:
        for k in falsekeys:check('scientific_and_historical_false_'+objlabel+'_'+k,obj[k]is False)
    for k in('actual_protocol_qualified','actual_full_rawrecord_transfer_qualified','original_XSM_memory_bits_verified','reaction_multiplicity_verified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','coupled_370group_reference_qualified','native_transport_executed','whole_combined_build_or_INPUT_qualified'):check('host_and_controls_scope_false_'+k,host[k]is False and controls[k]is False)
    for objlabel,obj in(('host',host),('summary',summary),('controls',controls),('binding',binding)):check('newwalker_controls_None_'+objlabel,obj['new_native_walker_controls_actual_run']is None)
    for k in('native_persisted_byte_qualification_sha256','actual_scientific_qualification_sha256','actual_material_scientific_INPUT_qualification_sha256'):check('child_unknown_qualification_'+k,child[k]is None)
    for objlabel,obj in(('host',host),('summary',summary),('binding',binding)):check('native_byte_qualification_unknown_'+objlabel,obj['actual_native_byte_qualification_sha256']is None and obj['original_native_build_binary_Source_linkage_qualified']is False)
    check('runtime_format_evidence_ONLY_Source_layout',child['source_runtime_format_evidence']==binding['source_runtime_format_evidence']and child['source_runtime_format_evidence']['source_layout_analysis_only']is True and child['source_runtime_format_evidence']['not_native_memory_bit_qualification']is True)
    wt=writer_receipt['terminal_tool_return'];wo=json.loads(wt['output']);check('actual_postclose_stdlib_writer_typed0_CLOSED_after_native_success',writer_receipt['metadata_only']is True and writer_receipt['closed']is True and writer_receipt['observed_terminal']is True and writer_receipt['session_repolled_after_close']is False and type(wt['exit_code'])is int and wt['exit_code']==0 and wt['chunk_id']==writer_receipt['actual_terminal_chunk']=='504607'and 'session_id'not in wt and writer_receipt['new_numeric_execution']is False and wo['summary']==sp and wo['native_actual_exit_code']==0)
    declared_joint=sum(q['size_bytes']for v in ns['namespaces']for q in v['files'].values());actual_joint=sum(i[4]for v in current.values()for i in v['files'].values());check('Root_writer_joint_after_append_2_exact_full_META_sizes',wo['joint_bytes_after_metadata_capture']==1045924515==declared_joint+nsp['size_bytes']+sp['size_bytes']and actual_joint==wo['joint_bytes_after_metadata_capture']+wrp['size_bytes']and actual_joint<2*2**30)
    checkerpin,checkerbytes=pin(D/'Root_bound_complete_native_checker.py',True);hostpin,hostbytes=pin(D/'Root_bound_complete_native_genuine_host.py',True);writerpin,writerbytes=pin(D/'Root_native_postclose_META_writer.py',True)
    check('actual_bound_checker_host_writer_fixed_Source_SHA',checkerpin['sha256']=='9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'and hostpin['sha256']=='90d4cf339eaa2aceb01e9736f65443351c64948ff96496b8d6a416dcf022f76f'and writerpin['sha256']=='abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139')
    for code in(checkerbytes,hostbytes,writerbytes):ast.parse(code)
    cs=checkerbytes.decode();check('Source_bit_comparison_no_tolerance_all_payload_extent_fullEOF',"require(native_position == expected_bytes"in cs and "require(ended and src.tell() == Path(path).stat().st_size"in cs and 'no_tolerance=True, no_missing_value_fill=True'in cs)
    check('Source_order_domains_independent_no_API_equal_promotion',"native_physical_preorder_equal_original_ASCII=physical_equal, native_XSM_API_export_preorder_equal_original_ASCII=api_equal"in cs and "all_persisted_native_value_bits_equal_ASCII=(mismatches == 0 and absent_count == 0 and physical_equal)"in cs and "original_LCM_copy_physical_record_order_verified=physical_equal"in cs)
    check('Source_named_zero_length_omissions_only_preserved_notfilled',"row['declared_count'] == 0"in cs and 'hidden_or_filled=False'in cs and 'full_record_domain_equal=(absent_count == 0)'in cs)
    check('Source_postclose_report_pin_full3_host_crosscheck_retained',"assert {k:report_pin[k] for k in ('path','sha256','identity')}==host['actual_native']['report']"in writerbytes.decode())
    for root,v in current.items():check('all_namespace_inventory_stat7ID_beforeafter '+root,view(Path(root))==v)
    for p,q in list(READS.items()):
        if str(D)in p or str(E)in p:continue
        check('bounded_success_META_stat7ID_stable '+p,identity(Path(p))==q['identity'])
    check('no_original_material_SQLite_spool_bin_numeric_reader_or_guard_run',True)
    check('no_numeric_payload_EOF_hash_replay_claim_for_HOC_output_files',True)
    out=Path(tempfile.mkdtemp(prefix='axmat_v23_actual_success_native_saved_SOURCE_META_review_20261010_',dir='/private/tmp'))
    for p,raw in RAW.items():
        path=Path(p)
        if path.is_relative_to(D):name='SOURCE/'+path.name
        elif path.is_relative_to(E):name='ROOT_SAVED_META/'+path.name
        elif path.is_relative_to(H):name='HOST_META/'+str(path.relative_to(H))
        elif path.is_relative_to(O):name='OUTPUT_SMALL_META/'+str(path.relative_to(O))
        else:name='CONTROLS_SMALL_META/'+path.name
        q=out/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
    (out/'review_actual_success_native_saved_Source_META_stdlib.py').write_bytes(Path(__file__).read_bytes())
    write(out/'COMPLETE_REVIEWED_SOURCE_META_FULL_EOF_MANIFEST.json',dict(schema='INDEPENDENT_V23_ACTUAL_SUCCESS_NATIVE_BOUNDED_SOURCE_META_READS_V1',reads=READS,large_material_SQLite_spool_or_binary_payloads_not_read=True,all_namespace_declared_STAT7ID_evidence=STAT))
    report=dict(schema='INDEPENDENT_V23_ACTUAL_SUCCESS_NATIVE_PERSISTED_BYTE_SAVED_SOURCE_META_REVIEW_V1',status='PASS_ACTUAL_NATIVE_PERSISTED_BYTE_SAVED_SOURCE_META_EVIDENCE_ONLY',saved_Source_META_only=True,all_checks_typed_true=True,blockers=[],checks=CHECKS,check_count=len(CHECKS),actual_Root_native_terminal_pin=tp,actual_Root_postclose_summary_pin=sp,actual_Root_complete_namespace_manifest_pin=nsp,actual_Root_prelaunch_pin=pp,actual_Root_postclose_META_writer_terminal_pin=wrp,actual_child_report_pin=cp,actual_genuine_host_result_pin=hp,actual_genuine_watchdog_pin=wp,actual_merged_child_log_pin=lp,actual_source_binding_pin=bp,actual_checker_Source_pin=checkerpin,actual_host_Source_pin=hostpin,actual_postclose_writer_Source_pin=writerpin,actual_Root_native_CLOSED_EXIT0=True,actual_saved_A_B_persisted_XSM_value_bits_comparison_report_verified=True,actual_native_replayed_by_this_review=False,original_material_payloads_or_SQLite_spool_binary_files_read_or_hashed_here=False,independent_new_numeric_bit_replay_performed=False,complete_Root_saved_output_EOF_SHA7ID_evidence_attribution='Root postclose writer actual full EOF manifest; review checked all current STAT7ID declarations and bounded Source/META only, without hashing original materials or SQLite/spool/large output payloads.',complete_D_frozen_files=957,complete_D_frozen_directories=58,prelaunch_E_frozen_files=374,prelaunch_E_frozen_directories=22,NS_E_postclose_files=379,current_E_files=382,E_exact_postclose_capture_appends=sorted(post5),E_exact_postwriter_appends=sorted(post3),E_root_directory_identity_unchanged_claimed=False,original_caps=CAPS,actual_child_elapsed_seconds=watch['elapsed_seconds'],actual_child_sampled_peak_RSS_MiB=watch['sampled_peak_rss_mib'],actual_child_wall_cap_seconds=watch['wall_cap_seconds'],actual_child_RSS_cap_MiB=512,actual_host_whole_seconds=host['whole_seconds'],Root_writer_joint_bytes_after_metadata_capture=wo['joint_bytes_after_metadata_capture'],current_joint_bytes_including_writer_tool_receipt=actual_joint,complete_state_summaries=states,native_physical_LCM_copy_preorder_equal_original_ASCII=True,native_XSM_API_export_preorder_equal_original_ASCII=False,direct_API_order_difference_is_saved_and_not_scientific_credit=True,zero_native_ASCII_bit_mismatches_in_saved_report=True,zero_original_ASCII_omitted_native_zero_length_records_in_saved_report=True,new_native_walker_controls_actual_run=None,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,original_XSM_memory_bits_verified=False,original_native_build_binary_Source_linkage_qualified=False,reaction_multiplicity_qualified=False,physical_balance_qualified=False,whole_combined_build_qualified=False,whole_combined_INPUT_admitted=False,native_RSS_general_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,Source_runtime_format_evidence_only=True,cleanup_performed=False,canonical_or_frozen_Source_META_changed_by_this_review=False)
    write(out/'REVIEW.json',report)
    (out/'REPORT.txt').write_text('PASS: independently reviewed saved successful native V23 Source/META evidence; Root real session81872 terminal5a01da EXIT0 CLOSED, no re-poll.\nA/B MACRO19619 records /19990 headers /2264113 numeric; MICRO23895 /24842 /18670730; four libraries saved zero bit mismatches and zero named zero-length omissions. Physical/LCM-copy order matches old ASCII; direct native XSM API export order explicitly differs and is separately retained.\nD957/58 and original E374/22 unchanged; E five postclose capture files and three writer appends preserved honestly. Actual child37.247112584s/49.96875MiB/512, host39.105851167s, Root writer joint1045924515B.\nNo material payload, SQLite, spool, binary output rehash or numeric replay by review. Complete output EOF/SHA evidence belongs to actual Root writer. New malformed native controls remain unexecuted/None; RAM bits, native build linkage, reaction balance, whole BUILD/INPUT, AAA/ABA and science remain unqualified; native qualification SHA remains None.\n')
    print(json.dumps(dict(status=report['status'],directory=str(out),check_count=len(CHECKS),Source_META_full_EOF_read_count=len(READS),namespace_declared_STAT7ID_count=len(STAT),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),no_material_SQLite_spool_payload_or_native_replay=True)))
if __name__=='__main__':main()

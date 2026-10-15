"""New installed6a closed-evidence metadata contract. No helper/graph/business execution."""
import hashlib,json,math,os,stat,struct
from pathlib import Path
INPUTS={}
def check(value,message):
    if type(value) is not bool or not value:raise ValueError('new installed6a metadata contract: '+message)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p)
    for q in (p,*p.parents):check(not q.is_symlink(),'ordinary input ancestor '+str(q))
    a=p.lstat();check(stat.S_ISREG(a.st_mode) and a.st_nlink==1,'ordinary single-link full input')
    h=hashlib.sha256();n=0
    with p.open('rb') as f:
        check(identity(os.fstat(f.fileno()))==identity(a),'open identity')
        for b in iter(lambda:f.read(524288),b''):h.update(b);n+=len(b)
        check(identity(os.fstat(f.fileno()))==identity(a),'EOF identity')
    check(identity(p.lstat())==identity(a) and n==a.st_size,'after EOF identity')
    return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=identity(a))
def verify(expected):
    got=pin(expected['path']);wanted=dict(path=expected['path'],sha256=expected['sha256'],size_bytes=expected.get('size_bytes',expected['identity'][4]),identity=expected['identity'])
    check(got==wanted,'exact expected pin '+expected['path'])
    if got['path'] in INPUTS:check(INPUTS[got['path']]==got,'conflicting input pin')
    INPUTS[got['path']]=got
    return got
def pairs(rows):
    d={}
    for k,v in rows:check(k not in d,'duplicate JSON key');d[k]=v
    return d
def finite(v):raise ValueError('nonfinite saved metadata '+v)
def read(p,sha=None):
    before=pin(p)
    if sha is not None:check(before['sha256']==sha,'bound metadata SHA')
    with Path(p).open('rt',encoding='utf8') as f:v=json.load(f,object_pairs_hook=pairs,parse_constant=finite)
    check(pin(p)==before,'saved JSON changed');INPUTS[before['path']]=before
    return v
def exact(a,b,ordered=True):
    if type(a) is not type(b):return False
    if type(a) is dict:return (list(a)==list(b) if ordered else set(a)==set(b)) and all(exact(a[k],b[k],ordered) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y,ordered) for x,y in zip(a,b))
    if type(a) is float:return math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
    return a==b
def closed0(t,chunk):check(type(t) is dict and t['chunk_id']==chunk and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t,'genuine closed integer zero '+chunk)
def compact(p):return {k:p[k] for k in ('path','sha256','identity')}
def full_refs(value):
    if type(value) is dict:
        if 'path' in value and 'sha256' in value and 'identity' in value:
            ids=value['identity'];check(type(ids) is list and len(ids)==7 and all(type(x) is int for x in ids),'exact7ID')
            if stat.S_ISREG(ids[2]):verify(value)
        for v in value.values():full_refs(v)
    elif type(value) is list:
        for v in value:full_refs(v)
def source_only_false(value,keys):
    for k in keys:check(value[k] is False,'no business/science '+k)
def host_contract(host,whole,stage):
    check((host['whole_wall_cap_seconds'],host['stage_wall_cap_seconds'],host['rss_cap_mib'],host['archive_cap_bytes'],host['threads'],host['children_at_once'],host['retries'])==(whole,stage,512,64*2**20,1,1,0),'original host caps')
    source_only_false(host,['profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'])
    w=host['watchdog'];check(type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True,'genuine original OwnRSS and cleanup')
    check(0<host['whole_seconds']<whole and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=stage and 0<=w['sampled_peak_rss_mib']<512,'actual bound measurements')
    check(len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['command']==w['command'],'unique successful stage')
    return w
FIXED_ENDPOINTS={'installed_helper': {'path': '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py', 'size_bytes': 152950, 'sha256': '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3', 'identity': [16777229, 49645417, 33188, 1, 152950, 1791696656438509035, 1791696656438509035]}, 'install_record': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/ACTUAL_SOURCE_INSTALL_WITNESS.json', 'size_bytes': 158516, 'sha256': '8a7ec7765b0ecd4acd43d17d70daeb5b2409daffd9caf301757685d7ec8fff38', 'identity': [16777229, 49645418, 33188, 1, 158516, 1791696656847741398, 1791696656847741398]}, 'install_tools': {'path': '/private/tmp/Root_stable_wire_source_install_actual_tool_returns_20261011.json', 'size_bytes': 1397, 'sha256': '7c8897152c3cb390f30ff0ac6b3acb3669159d06753168c92317d091fd7a7309', 'identity': [16777229, 49645429, 33188, 1, 1397, 1791696674759719679, 1791696674759719679]}, 'pure_binding': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-root-closure-v27-20261011-v3/ROOT_EXTERNAL_CLOSED_BINDING.json', 'size_bytes': 184890, 'sha256': '418da5c9433ee53ed7f2993cbde62bae78fd3ccfb1aa5ad9ddd4d13d5bd966e9', 'identity': [16777229, 49648905, 33188, 1, 184890, 1791698556603299604, 1791698556603299604]}, 'pure_root_tools': {'path': '/private/tmp/Root_v27_pure_external_closure_v3_actual_tool_returns_20261011.json', 'size_bytes': 16911, 'sha256': '192359997ecad586f2e4e5719f623bad329a9006fb13a0d61ec5a3fc938d07de', 'identity': [16777229, 49648958, 33188, 1, 16911, 1791698613695273043, 1791698613695273043]}, 'pure_protocol_tools': {'path': '/private/tmp/Root_v27_pure_protocol_actual_tool_returns_20261011.json', 'size_bytes': 1214, 'sha256': '83cda24cd118a688362eb4f3207d22c459378ca840b2849059ca1a4812cbd45a', 'identity': [16777229, 49648134, 33188, 1, 1214, 1791698103755175345, 1791698103755175345]}, 'fresh_binding': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011/ROOT_EXTERNAL_CLOSED_BINDING.json', 'size_bytes': 277524, 'sha256': 'cf9e3673a78895289c5ad0e9d4a76a4cfc8df1741b58d9c568fce5d91b1a74bb', 'identity': [16777229, 49655508, 33188, 1, 277524, 1791702046691667901, 1791702046691667901]}, 'fresh_root_tools': {'path': '/private/tmp/Root_v28_external_closeout_v2_actual_tool_returns_20261011.json', 'size_bytes': 1023, 'sha256': '2cd5dd00a88ccfa8ce6daebea4eb23aebc30a7ec2631c26e84a33513be6b323b', 'identity': [16777229, 49655530, 33188, 1, 1023, 1791702058970850834, 1791702058970850834]}, 'fresh_protocol_tools': {'path': '/private/tmp/Root_v28_fullfresh_actual_tool_returns_20261011.json', 'size_bytes': 2895, 'sha256': '0e3fb0ab9a80c62455185f7c576a1ae5fa25adb455a9772b81e38e802ea9a519', 'identity': [16777229, 49653305, 33188, 1, 2895, 1791700460887400089, 1791700460887400089]}, 'fresh_root_source_review': {'path': '/private/tmp/Root_v28_external_closeout_v2_independent_Source_review_20261011.json', 'size_bytes': 35068, 'sha256': '20344c3e88a98a93339bf5823daa04e8b0da0df50b80322eb3276c6bc45d7cf0', 'identity': [16777229, 49655418, 33188, 1, 35068, 1791702038873753139, 1791702038873753139]}, 'old_immutable_Q': {'path': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json', 'size_bytes': 689741, 'sha256': 'c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b', 'identity': [16777229, 49455079, 33188, 1, 689741, 1791625657710648236, 1791625657710648236]}, 'old_immutable_factory': {'path': '/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py', 'size_bytes': 224149, 'sha256': '117ec099ce288db10fe86c47d441192a3d697f9cd0a4d48e4dff86600bf5d604', 'identity': [16777229, 49537187, 33188, 1, 224149, 1791657459228915515, 1791657459228915515]}, 'old_Q_writer_Source': {'path': '/private/tmp/spot_write_actual_v25_joint_inactive_audit_helper_Q_ROOT.py', 'size_bytes': 32813, 'sha256': '82a13aca3646491213a787c08ac9d611944f982943f34e4cbc18ec2695c84b71', 'identity': [16777229, 49453134, 33188, 1, 32813, 1791624859374393514, 1791624859374393514]}, 'original_resource_prefix_Source': {'path': '/private/tmp/Root_v28_fullfresh_original_resource_precheck_v2_20261011.py', 'size_bytes': 4771, 'sha256': 'ded9bda107c0c2ac3aad8111b17efe8fee2f27908d86468ecbf8ddd0518abf66', 'identity': [16777229, 49653193, 33188, 1, 4771, 1791700396971599237, 1791700396971599237]}}
RETURN_FIELDS=['schema', 'classification', 'consumer_scope', 'consumer_selected_literal_and_canonical_paths', 'consumer_complete_namespace_root_sequence', 'scope', 'phase', 'graph_content_sha256', 'fresh_reader_contract', 'canonical_files_read', 'actual_bytes_read', 'byte_count_scope', 'logical_owner_requirements', 'exhaustive_namespaces_checked', 'explicit_aliases_checked', 'coverage', 'trace_coverage', 'live_io_scope', 'live_subprocesses_reexecuted', 'declared_absence_inputs_checked_before_and_after_bytes', 'absence_inputs_are_not_regular_bytes_or_science', 'caller_must_recheck_current_OS_identity_and_live_probe_results', 'typed_snapshot', 'science_qualification_created', 'live_resources_verified', 'external_declaration_exit0_verified', 'caller_must_verify_live_environment_modules_PID_time_and_resources']
SNAPSHOT_FIELDS=['schema', 'coverage', 'records', 'subprocess_records', 'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed', 'native_libc_HDF5_loader_and_directory_stat_are_not_traced']
def owner_controls(d):
    check(d['schema'] == 'AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1', 'original owner schema')
    check([len(d[k]) for k in ('positive_controls', 'private_guard_rejections', 'accepted_str_subclass_equivalence_controls', 'partial_invalid_second_owner_rejections')] == [4, 3, 2, 2], 'whole original owner controls')
    for row in d['positive_controls']:
        check(row['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default'] is True and exact(row['expected_complete_descriptor_signature'], row['actual_complete_descriptor_signature']), 'owner whole normalized signature')
        field = 'owned_list_completely_cleared_after_success' if row['case'] == 'owned_builtin_list_True' else 'caller_full_identity_type_order_value_attrs_floatbits_unchanged'
        check(row[field] is True, 'original owner clear/default boundary')
    for row in d['private_guard_rejections']:
        check(row['class'] == 'InputGraphError' and row['message'] == 'private owner consume needs a bool and an exclusively owned builtin list' and row['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True, 'original owner rejects')
    for row in d['accepted_str_subclass_equivalence_controls']:
        check(row['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is True and row['owned_list_completely_cleared_after_success'] is True and row['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default'] is True and exact(row['expected_complete_descriptor_signature'], row['actual_complete_descriptor_signature']), 'whole owner subtype control')
    for row in d['partial_invalid_second_owner_rejections']:
        check(row['class'] == 'InputGraphError' and row['message'] == 'missing file owner', 'original partial second-owner error')
    for key in ('first_valid_slot_None_after_original_validate_and_append', 'invalid_second_slot_original_identity_and_value_unchanged', 'default_partial_caller_unchanged', 'original_owner_rejection_class_order_message_preserved', 'original_protocol_controls_fixtures_and_caps_unchanged', 'no_new_fixture_file_or_IO_created'): check(d[key] is True, key)
    check(d['new_helper_qualification_created'] is False and d['business_or_science_qualification_created'] is False, 'original owner control scope')


def validate_closed_evidence():
    INPUTS.clear()
    for p in FIXED_ENDPOINTS.values():verify(p)
    helper=FIXED_ENDPOINTS['installed_helper']
    check(helper['identity']==[16777229,49645417,33188,1,152950,1791696656438509035,1791696656438509035],'actual installed6a full Source identity')
    install=read(FIXED_ENDPOINTS['install_record']['path']);it=read(FIXED_ENDPOINTS['install_tools']['path'])
    closed0(it['actual_closed'],'52b18a');check(it['actual_initial']['chunk_id']=='a5412e' and it['actual_initial']['session_id']==60214,'actual one Source-only install launch')
    installed_stdout=json.loads(it['actual_closed']['output'],object_pairs_hook=pairs,parse_constant=finite)
    check(installed_stdout['installed_source']==helper and installed_stdout['Q_created'] is False and installed_stdout['production_factory_changed'] is False,'actual install stdout, no runtime admission')
    pb=read(FIXED_ENDPOINTS['pure_binding']['path']);fb=read(FIXED_ENDPOINTS['fresh_binding']['path'])
    check(pb['status']=='ROOT_BOUND_ACTUAL_PURE_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION' and fb['status']=='ROOT_BOUND_ACTUAL_COMPLETE_FULLFRESH_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION','both independent new-family Root closures')
    source_only_false(pb,['new_Q_created','whole_522_to_512_memory_pass','Native_started','AAA_accuracy_qualified','ABA_admitted'])
    source_only_false(fb,['new_Q_created','helper_qualification_created','whole_522_to_512_memory_pass','Native_solver_training_or_PS_started','AAA_accuracy_qualified','ABA_admitted'])
    pt=read(FIXED_ENDPOINTS['pure_protocol_tools']['path']);ft=read(FIXED_ENDPOINTS['fresh_protocol_tools']['path'])
    prt=read(FIXED_ENDPOINTS['pure_root_tools']['path']);frt=read(FIXED_ENDPOINTS['fresh_root_tools']['path'])
    for t,initial,session,closed in ((pt,'68ece3',62042,'3a9510'),(ft,'81e3f4',25973,'98d67b'),(prt,'9ffe85',53728,'afeb52'),(frt,'89d121',29061,'4aa325')):
        check(t['initial']['chunk_id']==initial and type(t['initial']['session_id']) is int and t['initial']['session_id']==session,'one true launch');closed0(t['closed'],closed)
    check(ft['intermediate']['chunk_id']=='23c637' and ft['intermediate']['session_id']==25973,'actual fresh still-live return retained')
    check(prt['closed_output_truncated_by_tool'] is True,'honest old Root pure closeout stdout truncation; never parsed as full JSON')
    fresh_root_stdout=json.loads(frt['closed']['output'],object_pairs_hook=pairs,parse_constant=finite)
    check(fresh_root_stdout['binding_sha256']==FIXED_ENDPOINTS['fresh_binding']['sha256'] and fresh_root_stdout['copied_files']==33 and fresh_root_stdout['new_Q_created'] is False,'actual fresh Root stdout exact permanent binding')
    pstdout=json.loads(pt['closed']['output'],object_pairs_hook=pairs,parse_constant=finite);fstdout=json.loads(ft['closed']['output'],object_pairs_hook=pairs,parse_constant=finite)
    check(pstdout['actual_host_result']==compact(pb['actual_host_result']) and fstdout['actual_host_result']==compact(fb['actual_host_result']),'actual protocol host terminal coupling')
    check(pb['actual_genuine_tool_returns']==FIXED_ENDPOINTS['pure_protocol_tools'] and fb['actual_genuine_launch_intermediate_closed_tool_returns']==FIXED_ENDPOINTS['fresh_protocol_tools'],'actual protocol receipt endpoint binding')
    ph=read(pb['actual_host_result']['path']);fh=read(fb['actual_host_result']['path'])
    pure=read(pb['actual_control_report']['path']);fresh=read(fb['actual_complete_control_report']['path'])
    check(compact(pb['actual_control_report'])==ph['actual_control_report'] and compact(fb['actual_complete_control_report'])==fh['actual_control_report'],'host complete reports exact')
    pw=host_contract(ph,60,60);fw=host_contract(fh,1800,600)
    check(ph['complete_original_pure_controls_retained'] is True and ph['status']=='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED','complete original new6a pure family')
    source_only_false(ph,['helper_admission_created','new_Q_created','whole_family_memory_pass'])
    source_only_false(fh,['new_Q_created','whole_522_to_512_memory_pass','helper_metadata_qualified','whole_business_INPUT_qualified','physical_balance_qualified'])
    check(compact(helper)==fh['installed_helper'],'fresh installed exact6a')
    check(pure['helper']['path']==helper['path'] and pure['helper']['sha256']==helper['sha256'] and pure['helper']['identity']==helper['identity'] and pure['helper']['source_bytes']==152950,'pure same installed6a')
    check(pure['caps']==dict(children=1,json_read_bytes=64*2**20,output_bytes=64*2**20,retries=0,rss_bytes=512*2**20,wall_seconds=60),'original pure direct caps')
    check(pure['saved_input_identity_before']==pure['saved_input_bytes_identity_after'],'full original saved graph/trace input identity beforeafter')
    fixture=read(Path(pb['actual_control_report']['path']).parent/'small_fixture_controls.json')
    small=read(pure['small_codecs']['small_controls_artifact'])
    check(pure['status'] == 'ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' and fixture['producer_full_exact_values_types_order_floatbits'] is True and fixture['caller_full_value_and_mutable_identity_preserved'] is True and len(fixture['rejections']) == 37 and len(fixture['complete_rejected_arguments']) == 18, 'original complete fixture producer/rejects')
    check([s['stage'] for s in pure['stages']] == ['real_small_fixture_producer_equivalence_and_rejections', 'all_new_codecs_and_both_strict_entrances_small_controls', 'full_63379_creation_trace_roundtrip_and_stored_size', 'full_old_saved_graph_codec_and_two_normal_strict_entrances', 'all_original_saved_metadata_bytes_identity_unchanged'], 'five original full stages')
    check(small['all_default_inputs_unmodified'] is True and small['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True and small['ordinary_and_both_storage_strict_dispatches'] is True and len(small['rejections']) == pure['small_codecs']['rejections'] == 61, 'whole codec/type/order/floatbit/reject scope')
    subtypes = pure['small_fixture']['accepted_str_subclass_equivalence_controls']; check(len(subtypes) == 2 and all(x['complete_builtin_output_values_types_order_floatbits_equal'] is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True for x in subtypes), 'original subtype attrs/identity')
    old = pure['full_old_saved_graph']; meta = old['complete_original_metadata']; trace = pure['full_new_creation_trace']
    check(exact(meta, old['normal_strict_file_entrance_full_semantics_and_counts']) and exact(meta, old['normal_strict_payload_entrance_full_semantics_and_counts']) and old['full_default_roundtrip_exact'] is True and old['old_read_trace_not_replaced_by_new_trace'] is True and old['original_legacy_semantic_sha_preserved'] is True, 'whole old graph two normal strict entrances')
    counts = meta['complete_counts']; check(counts['canonical_files'] == 36776 and counts['requirements'] == 237767 and counts['read_trace_records'] == 62332, 'whole original graph counts')
    check(trace['exact_full_roundtrip'] is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse'] is True and trace['default_source_nonmutation'] is True and trace['full_record_count'] == 63379 and trace['actual_attempt_count'] == 175886, 'whole new trace default/order/roundtrip')
    owner_controls(pure['private_owner_consume_controls'])
    snapshot = read(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact']['path']); verify(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact'])
    check(exact(snapshot, pure['private_inactive_audit_snapshot_controls'], ordered=False), 'full ordered artifact and original report same values/types/floatbits')
    check(snapshot['schema'] == 'PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1' and snapshot['status'] == 'ACTUAL_PRIVATE_SNAPSHOT_CONTROLS_RETURNED_METADATA_ONLY' and [len(snapshot[k]) for k in ('positive_controls', 'private_guard_rejections', 'last_use_failure_controls')] == [5, 13, 3], 'complete new snapshot scope')
    for index, row in enumerate(snapshot['positive_controls']):
        check(row['default_and_explicitFalse_complete_state_unchanged'] is True and row['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default'] is True, 'default unchanged and all nine fields')
        if index < 3:
            check(row['owned_same_builtin_records_map_completely_cleared'] is True and row['all_other_audit_state_and_actual_Popen_references_unchanged'] is True and list(row['actual_full_expected_snapshot']) == SNAPSHOT_FIELDS and exact(row['actual_full_expected_snapshot'], row['actual_full_consumed_snapshot']), 'owned full ordered nine fields/Popen/clear')
        else: check(row['private_True_not_permitted_for_subclass'] is True, 'default subtype compatibility retained')
    check(all(r['rejected'] is True and r['class_name'] == 'InputGraphError' and r['complete_audit_state_identity_type_order_value_bits_unchanged'] is True for r in snapshot['private_guard_rejections']), 'all 13 private guards')
    check([r['case'] for r in snapshot['last_use_failure_controls']] == ['invalid_second_row_before_clear', 'missing_attempt_count_before_clear', 'nonfinite_clone_after_clear'], 'original last-use failure order')
    for i, row in enumerate(snapshot['last_use_failure_controls']): check(row['original_error_class_and_message_retained'] is True and row['no_transactional_private_mode_promise'] is True and row['both_callers_unchanged_before_clear_or_default'] is (i < 2) and row['private_clone_failure_after_clear_consumption_observed'] is (i == 2), 'honest before/after-clear failure boundary')
    check(snapshot['actual_child_returncode'] == 0 and snapshot['actual_same_observation_full_record_role_comparison'] is True and snapshot['no_cross_process_PID_FD_inode_normalization'] is True and snapshot['default_original_complete_protocol_preserved'] is True and snapshot['native_or_numeric_component_executed'] is False and snapshot['helper_qualification_created'] is False and snapshot['business_or_science_qualification_created'] is False, 'same genuine Popen and metadata-only control')

    index=read(pure['read_open_short_index_state_controls_order_preserved_artifact']['path'])
    check(exact(index,pure['read_open_short_index_state_controls'],False),'full index ordered artifact unchanged')
    check(index['schema']=='READ_OPEN_SHORT_INDEX_ORIGINAL_PROTOCOL_STATE_SUPPLEMENT_V1' and index['status']=='ACTUAL_SYNTHETIC_INDEX_CONTROLS_PASS_NO_ADMISSION','actual separate index state controls')
    for k in ('all_original_other_audit_state_preserved','control_data_not_real_open_PID_FD_or_Popen_evidence','no_project_or_material_fixture_created','original_canonical_key_bytes_are_oracle','same_map_and_nonempty_set_True_cleared_after_original_capture','same_map_and_nonempty_set_default_and_False_unchanged','standard_and_forced_collision_full_nine_field_snapshot_exact'):check(index[k] is True,'index '+k)
    check((index['actual_attempts'],index['unique_records'],index['exception_count_bearing_markers'])==(35,9,2),'actual complete index counts')
    check(exact(index['complete_default_snapshot'],index['complete_consumed_snapshot']),'full nine-field index default/consume exact')
    check(len(index['all_original_guards_with_nonempty_markers'])==13 and all(r['class_name']=='InputGraphError' and r['same_nonempty_set_map_and_old_state_unchanged'] is True for r in index['all_original_guards_with_nonempty_markers']),'all original marker guards')
    check(len(index['original_last_use_failure_with_nonempty_markers'])==3,'all three original marker failure controls')
    source_only_false(index,['Native_solver_training_or_numerical_component_executed','helper_runtime_input_or_scientific_qualification'])
    wire=read(pure['saved_wire67_complete_fields_order_preserved_artifact']['path'])
    check(exact(wire,pure['saved_wire67_complete_fields_review'],False),'all saved wire67 review fields retained')
    check(wire['schema']=='SPOT_V27_COMPLETE_SAVED_WIRE67_FIELD_REVIEW_V1' and wire['status']=='SAVED_WIRE67_COMPLETE_FIELDS_REVIEWED_NO_NEW_HELPER_ADMISSION' and (wire['fixture_count'],wire['returns'],wire['raises'])==(67,14,53),'all finite actual wire67 counts')
    for k in ('actual_saved_wire_tables_eof_byte_equal','complete_saved_fixture_fields_preserved'):check(wire[k] is True,'wire '+k)
    source_only_false(wire,['Native_solver_training_or_PS_started','fresh_payloads_reexecuted','helper_admission_created','new_Q_created','original_protocol_replaced','whole_family_memory_pass'])
    saved_wire=read(wire['saved_wire_input_pin']['path']);check(exact(saved_wire,wire['complete_saved_wire_control_result'],False),'complete saved wire result, every fixture field')
    check(saved_wire['fixture_case_count']==67 and saved_wire['logical_edges']==238780 and len(saved_wire['fixture_results'])==67 and all(r['old_equals_candidate_complete_return_or_exception'] is True and r['original_complete_evidence']['caller_all_nested_identity_unchanged'] is True for r in saved_wire['fixture_results']),'all wire fixtures and complete real edges')
    for k in ('complete_wire_table_old_candidate_saved_bytes_equal','full_Source_forward_and_inverse_byte_exact','all_input_rows_exact_builtin_tuple_and_strings','caller_complete_row_identity_order_unchanged'):check(saved_wire[k] is True,'complete wire '+k)
    check(wire['actual_fresh_observation_binding']['actual_installed_helper_seven_field_identity']==helper['identity'],'wire observation installed6a Source identity')
    check(fresh['schema']=='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1' and fresh['complete_return_fields_retained']==RETURN_FIELDS and fresh['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is True,'all original 27 current fresh fields')
    check(fresh['actual_complete_trace_counts']==dict(records=37446,attempts=37446,canonical_files=37445,external_graph_reads=1,no_subprocess_reexecuted=True),'new actual full current graph counts')
    pc=fresh['private_trace_controls'];check(len(pc['positive_controls'])==4 and len(pc['rejections'])==3 and all(r['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True for r in pc['positive_controls']) and all(r['rejected'] is True and r['class_name']=='InputGraphError' and r['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for r in pc['rejections']),'original full fresh4+3')
    fc=fresh['private_full_inactive_audit_snapshot_controls']
    for k in ('default_snapshot_full_original_records_unchanged','owned_same_builtin_records_map_completely_cleared','all_other_audit_state_unchanged','all_nine_fields_full_type_order_value_floatbits_and_counts_equal','no_second_graph_or_input_phase_substituted','all37446_actual_reads_from_same_genuine_phase','no_cross_phase_hash_or_stat_cache'):check(fc[k] is True,'fresh same-phase complete snapshot '+k)
    source_only_false(fc,['new_helper_qualification_created','business_or_science_qualification_created'])
    check(exact(fc['default_complete_descriptor_type_order_floatbit_pin'],fc['consumed_complete_descriptor_type_order_floatbit_pin']) and fc['default_complete_descriptor_type_order_floatbit_pin']['complete_node_count']==786385,'full snapshot nested type order IEEE nodes')
    cw=fc['complete_consumed_vs_default_wire'];check(cw['complete_nine_snapshot_fields']==SNAPSHOT_FIELDS and cw['uncompressed_JSON_bytes']==21484485 and cw['every_default_and_consumed_wire_byte_compared'] is True and cw['full_gzip_EOF_verified'] is True and cw['no_fields_or_records_selected'] is True,'entire same-phase default consume wire')
    gzips={k:fresh[k] for k in ('expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace')}
    for k,p in gzips.items():verify(p);check(p['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and p['no_fields_or_records_filtered'] is True,'all three full gzip evidence')
    check(fresh['expected_complete_return_contract']['sha256']==fresh['actual_complete_verifier_return']['sha256'] and fresh['expected_complete_return_contract']['uncompressed_JSON_sha256']==fresh['actual_complete_verifier_return']['uncompressed_JSON_sha256'],'full expected actual 27field gzip bytes equal')
    check(fb['complete_three_lossless_gzip_artifacts']==gzips and fb['full_same_phase_default_consume_snapshot_controls']==fc and fb['complete_actual_read_trace_counts']==fresh['actual_complete_trace_counts'],'actual Root complete fresh controls coupled')
    check(fb['complete27_return_wire']['full_uncompressed_byte_comparison'] is True and fb['complete27_return_wire']['full_both_EOF'] is True and fb['all9_snapshot_fields_and_type_order_value_IEEE_pin_rechecked'] is True and fb['all_original_private_trace_controls_four_positive_three_rejection'] is True,'true Root full byte and private bindings')
    check(fb['original_five_guards_DE_freeze_and_failed_d19_preserved'] is True and fb['original_protocol_archive_before']==fb['original_protocol_archive_after'] and fb['original_protocol_archive_before']['complete_H_O_Source_receipts_regular_bytes']<64*2**20,'original complete archive guards beforeafter')
    check(pb['actual_protocol_archive_bytes']<64*2**20,'original complete pure archive cap')
    check(fb['external_closeout_checkpoint']['Python_process_launch_attempts']==[],'true closeout Python audit scope, no native/C inference')
    for d in (pb,fb,ph,fh,pure,fresh,wire,index,install):full_refs(d)
    original_protocol=dict(original_and_fresh_small_producer_values_types_order_floatbits_exact=True,all_caller_mutable_identity_and_subtype_attributes_unchanged=True,accepted_str_subtype_groups=len(subtypes),small_codec_rejections=pure['small_codecs']['rejections'],complete_original_graph_counts=counts,complete_old_graph_two_normal_strict_entrances_exact=True,complete_old_legacy_semantic_sha256=meta['legacy_semantic_sha256'],complete_old_wire_content_sha256=meta['wire_content_sha256'],complete_new_creation_trace_records=trace['full_record_count'],complete_new_creation_trace_actual_attempts=trace['actual_attempt_count'],new_creation_trace_not_substituted_into_old_graph=True,full_json_types_order_floatbits_and_values_retained=True,default_source_nonmutation=True)
    check(len(original_protocol)==13,'all original13 fields in order')
    complete=dict(helper=helper,actual_SOURCE_install_record=FIXED_ENDPOINTS['install_record'],actual_SOURCE_install_tool_return=FIXED_ENDPOINTS['install_tools'],pure=dict(actual_Root_closed_binding=FIXED_ENDPOINTS['pure_binding'],actual_genuine_protocol_tools=FIXED_ENDPOINTS['pure_protocol_tools'],actual_Root_closeout_tools=FIXED_ENDPOINTS['pure_root_tools'],actual_host_result=pb['actual_host_result'],actual_control_report=pb['actual_control_report'],actual_measurement=dict(whole_seconds=ph['whole_seconds'],child_seconds=pw['elapsed_seconds'],original_OwnRSS_peak_mib=pw['sampled_peak_rss_mib']),full_protocol=original_protocol,complete_original_fixture_artifact=pin(Path(pb['actual_control_report']['path']).parent/'small_fixture_controls.json'),complete_original_codec_artifact=pin(pure['small_codecs']['small_controls_artifact']),private_owner_consume_controls=pure['private_owner_consume_controls'],private_inactive_audit_snapshot_controls=snapshot,read_open_short_index_state_controls=index,complete_wire67_fields_review=wire),fresh=dict(actual_Root_closed_binding=FIXED_ENDPOINTS['fresh_binding'],actual_genuine_protocol_tools=FIXED_ENDPOINTS['fresh_protocol_tools'],actual_Root_closeout_tools=FIXED_ENDPOINTS['fresh_root_tools'],actual_host_result=fb['actual_host_result'],actual_control_report=fb['actual_complete_control_report'],actual_measurement=dict(whole_seconds=fh['whole_seconds'],child_seconds=fw['elapsed_seconds'],original_OwnRSS_peak_mib=fw['sampled_peak_rss_mib']),all27_return_fields=fresh['complete_return_fields_retained'],full_saved_graph_metadata=fresh['independent_full_saved_graph_metadata'],private_trace_controls=pc,private_full_inactive_audit_snapshot_controls=fc,complete_three_gzip_artifacts=gzips,complete_actual_read_counts=fresh['actual_complete_trace_counts']),legacy_Q_authorizes_new_helper=False,whole_522_to_512_memory_pass=False,science_or_BOOT_admitted=False)
    for p in tuple(INPUTS.values()):check(pin(p['path'])==p,'all saved metadata Source EOF7ID after')
    return complete,list(INPUTS.values())

def validate_actual_new_Q(q):
    check(q['schema']=='SPOT_INSTALLED6A_ACTUAL_ORIGINAL_PURE_AND_FULLFRESH_HELPER_METADATA_Q_V29','distinct new Q schema')
    check(q['status']=='QUALIFIED_INSTALLED6A_ORIGINAL_PURE_FULL_CURRENT_GRAPH_METADATA_ONLY','new metadata-only Q status')
    check(q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE','original narrow admission scope')
    for k in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','canonical_wired','science_or_BOOT_admitted','legacy_Q_authorizes_new_helper'):check(q[k] is False,'no new science/business '+k)
    evidence,pins=validate_closed_evidence();check(exact(q['complete_actual_new6a_closed_evidence'],evidence),'all actual new installed6a contracts, no old Q substitution')
    source=verify(q['actual_Source_writer']);declared={p['path']:p for p in q['complete_Root_metadata_EOF7ID_inputs']}
    check(len(declared)==len(q['complete_Root_metadata_EOF7ID_inputs']) and all(declared[p['path']]==p for p in pins+[source]),'complete unique actual Q inputs')
    return {p['path']:p['sha256'] for p in pins+[source]}

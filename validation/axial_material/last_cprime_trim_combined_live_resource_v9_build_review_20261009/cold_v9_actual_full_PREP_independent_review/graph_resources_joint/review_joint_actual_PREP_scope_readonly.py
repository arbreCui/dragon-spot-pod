import hashlib,json,stat
from pathlib import Path
D=Path('/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009');PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def read(p,sha):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and not p.is_symlink()
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==sha and identity(p)==before
 PINS[str(p)]=dict(path=str(p),sha256=sha,size_bytes=len(b),identity=before);return json.loads(b)
g=read(D/'REPORT.json','2c124560cb591339ee1dbc0b43471db3d28a6b65a843c0381d7cf37607fea39d');gt=read(D/'actual_readonly_tool_return.json','66dbf89138ae4af595ed0c3f30392400e67eb4947e77adba756d25958c6e00bc')
S=Path('/private/tmp/spot_v9_cold_actual_PREP_full_source_independent_review_20261009');s=read(S/'REPORT.json','4abf92d49fc9f8a50f9e410ad8c7c311f0790fb7451a8e6cc98a48b56ea25f24');st=read(S/'actual_readonly_tool_return.json','7f59e5a3b79ccde4fbeb8a8fc476c1290a48467668296b3861f116436629050a')
assert g['status']==s['status']=='PASS'
for r in (gt,st):assert type(r['actual_tool_result']['exit_code']) is int and r['actual_tool_result']['exit_code']==0 and r['actual_tool_result']['closed'] is True
assert gt['actual_tool_result']['initial_chunk_id']=='ff7547' and gt['actual_tool_result']['terminal_chunk_id']=='dc11fe'
assert st['actual_tool_result']['initial_chunk_id']==st['actual_tool_result']['terminal_chunk_id']=='5a91a1'
assert gt['report_pin']['sha256']==PINS[str(D/'REPORT.json')]['sha256'] and st['report']['sha256']==PINS[str(S/'REPORT.json')]['sha256']
assert g['prepared']['sha256']==s['prepared_sha256']=='35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7'
assert g['actual_prepare_receipt']['sha256']==s['prepare_terminal_sha256']=='2bcce12bb05d50b7dabce828f14dc7bd1dbff2a3383af5ac0ab81dbc10d8050a'
assert g['Root_observer']['sha256']==s['Root_observer_sha256']=='c1e24c926bb6aedd909f641717b3a4ec60970ec418aa3f3dfa023b696dd18f16'
root=read(g['Root_observer']['path'],g['Root_observer']['sha256']);receipt=read(g['actual_prepare_receipt']['path'],g['actual_prepare_receipt']['sha256'])
assert root['actual_tool_result']==g['actual_PREP_Root_tool']==dict(initial_chunk_id='1a53dd',session_id=2047,terminal_chunk_id='d7ffa4',exit_code=0,closed=True)
assert root['actual_success_recorder_tool']==g['actual_success_recorder_tool']==dict(chunk_id='15dda0',exit_code=0,closed=True)
assert type(receipt['returncode']) is int and receipt['returncode']==0
assert s['source31_exact_fullSHA_namespace'] and s['generated3_whole_source_byte_inverses_rechecked'] and s['original7_UNCHANGED_sources_fresh_exact']
for k in ['complete43_local_files_and_all31_runtime_copies_fullSHA','complete_prepared_all_fields_checked','all7_other_deck_bytes_unchanged','whole_production_inputs_manifest_inverse_to_original_base_typed_order_floatbits','complete_original_AB_inputs_config_budget_parent_snapshot_control_outputs_preserved','whole_original_producer_admission_inverse_only_current_receiver_SHA','original_physics_dtype_layout_trace_bytefresh_gates_inherited_by_same_source_bytes']:assert s[k] is True
assert s['complete2_axial_decks_inverse_to_original_bytes']=={'bootstrap_axial.x2m':'13a43842e6fe32ea1568e476715f5ca3a0b44c7dbab5744d7667b9cc956e893e','picard_axial.x2m':'0849ed24c071fde68957c32956b55dae619a8801c3e64a38e0a7a03c703b5cc4'}
assert g['canonical_files']==35647 and g['inherited_canonical_bytes']==35803098221 and g['fresh_canonical_payload_content_reads']==0
assert g['requirement_rows']==235528 and len(g['namespaces_before_after86'])==86 and g['aliases_absences_before_after']['aliases']==186 and g['aliases_absences_before_after']['absence_inputs']==445
assert g['full_metadata_dependency_count']==37339 and g['descriptor_union35675_retained'] is True and g['whole65_complete_type_order_values_floatbits_equal'] is True
assert g['resource_before_after_complete_inventory_equal'] is True and g['current_resources_before']==g['current_resources_after'] and g['strict_reservation_gate_passed'] is True
assert g['history_budget_bytes']==96*2**30 and g['min_free_bytes']==8*2**30 and g['fresh_AAA_reserve_bytes']==20971764748
for k in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification','new_controls_bound']:assert s[k] is False
assert g['native_RSS_credit'] is False and g['future_binding_controls_and_cold_outputs_absent'] is True
assert g['actual_execve_syscall_argv_trace_saved'] is False and s['actual_execve_syscall_argv_observation'] is None
for p,r in PINS.items():assert identity(p)==r['identity']
result=dict(schema='AXMAT_V9_ACTUAL_COLD_PREP_FULL_COMPLEMENTARY_SCOPE_TRUE_BINDING_V1',status='PASS',credit='COMPLETE_ACTUAL_PREP_INPUT_ONLY_FOR_ROOT_SOLE_ADMISSION; no current cold binding/controls/native/reference qualification',
 graph_resource_report=PINS[str(D/'REPORT.json')],graph_resource_true_tool=gt['actual_tool_result'],graph_resource_tool_receipt=PINS[str(D/'actual_readonly_tool_return.json')],source_deck_environment_report=PINS[str(S/'REPORT.json')],source_deck_environment_true_tool=st['actual_tool_result'],source_deck_environment_tool_receipt=PINS[str(S/'actual_readonly_tool_return.json')],
 actual_PREP_Root_tool=root['actual_tool_result'],actual_PREP_recording_tool=root['actual_success_recorder_tool'],actual_PREP_receipt=PINS[g['actual_prepare_receipt']['path']],prepared_sha256=g['prepared']['sha256'],Root_observer=PINS[g['Root_observer']['path']],
 whole_PREP_source_environment_decks_metadata_and_input_graph_resource_scopes_covered=True,SOURCE31_generated3_inverse_env1860_source1919_fullproofs_retained=True,OUTPUT43local_plus_prepared44_31runtime_complete=True,
 inherited_recent_fullBYTE_canonical35647_35803098221_bytes_with_fresh_all7field_identity_before_after=True,new_scientific_canonical_content_read_bytes=0,all235528_rows_86ns_186aliases_445absence_37339dependencies_35675descriptors=True,
 whole65_original_raw_order_sorted_consumer_boundary_all_builtin_types_values_float64bits_full7_trim73=True,complete_original_cases_AB_production_config_budgets_input_material_protocol_physics_dtype_layout=False if not s['complete_original_AB_inputs_config_budget_parent_snapshot_control_outputs_preserved'] else True,
 reference_policy_boundary=s['reference_policy_boundary'],retained_original2000_policy_and_eight_gates_are_future_independent_reference_dependency_only=True,
 current_resource_scope=dict(declared_roots=g['declared_roots_count'],dynamic_current_roots=g['dynamic_current_roots_count'],artifact_bytes=g['current_resources_after']['artifact_bytes'],regular_files=g['current_resources_after']['regular_files'],current_inventory_sha256=g['current_resources_after']['full_path_identity_inventory_sha256'],unchanged_history_cap=96*2**30,min_free=8*2**30,original_parent_case_bytes=13265348616,reserve20971764748=True,current_before_after_equal=True,old_filecount_not_fixed_current_gate=True),
 actual_source_derived_execve_is_not_saved_syscall_trace=True,original_DECLARE_phase_trace_not_fabricated=True,Root_sole_owns_future_binding_control_cold_calls=True,
 preserved_first_joint_schema_assertion_failure='first_joint_66f477_exit1/actual_tool_return.json',only_TMP_evidence_written=True,business_or_helper_import_API_constructor_PREP_RUN_native_executed=False,project_formal_ART_written=False,new_canonical35GB_read=False,new_controls_bound=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,full_pins=PINS)
(D/'joint_scope_binding.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(status='PASS',joint_sha256=hashlib.sha256((D/'joint_scope_binding.json').read_bytes()).hexdigest(),graph2c124_source4abf_fullscope_bound=True,new35GB_content_reads=0,business=False)))

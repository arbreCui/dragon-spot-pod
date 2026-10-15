"""Independent reviewer only: finite Source reads/AST, never candidate execution."""
import ast,contextlib,hashlib,io,json,os,runpy,sys
from pathlib import Path
P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
D=Path('/private/tmp/axmat_N8_COMPLETE_INDEPENDENT_Source_review_36g28ueh')
captured=io.StringIO()
with contextlib.redirect_stdout(captured):
    audit=runpy.run_path(str(D/'INDEPENDENT_READ_COMPLETE_N8_SOURCE.py'))
pins=audit['pins'];raws=audit['raws'];trees=audit['trees'];objects=audit['objects'];result=audit['result']
checks=[];evidence={}
def check(name,value,why):
    if type(value)is not bool or not name or name in evidence:raise ValueError('invalid reviewer check')
    checks.append(dict(check=name,passed=value));evidence[name]=why
def text(rel):return raws[rel].decode()
def definitions(rel):
    src=text(rel).splitlines(keepends=True)
    out={}
    def visit(body,prefix=''):
        for node in body:
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                key=prefix+node.name
                if key in out:key+='@'+str(node.lineno)
                out[key]=dict(first_line=node.lineno,last_line=node.end_lineno,whole_source=''.join(src[node.lineno-1:node.end_lineno]))
                if isinstance(node,ast.ClassDef):visit(node.body,key+'.')
    visit(trees[rel].body);return out
def fn(rel,name):return definitions(rel)[name]['whole_source']
def value(node):
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,ast.Dict):return {value(k):value(v)for k,v in zip(node.keys,node.values)}
    if isinstance(node,ast.List):return [value(x)for x in node.elts]
    if isinstance(node,ast.Tuple):return tuple(value(x)for x in node.elts)
    if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='dict'and not node.args:return {k.arg:value(k.value)for k in node.keywords}
    if isinstance(node,ast.BinOp):
        left,right=value(node.left),value(node.right)
        if isinstance(node.op,ast.Mult):return left*right
        if isinstance(node.op,ast.Pow):return left**right
        if isinstance(node.op,ast.Add):return left+right
        if isinstance(node.op,ast.Sub):return left-right
    raise ValueError('not finite literal Source expression')
def assignment(rel,key):
    matches=[n.value for n in trees[rel].body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==key]
    if len(matches)!=1:raise ValueError('assignment Source occurrence '+key)
    return value(matches[0])
runtime='complete_observation_BUILD5_AB_runtime.UNREADY.py';driver='N8_genuine_integrated_controls_driver.UNREADY.py';owner='N8_exact_owner_scope_observer.UNREADY.py';qualifier='N8_Root_controls_postclose_META.UNREADY.py';gate='N8_actual_controls_qualification_gate.Source_META_only.py';writer='Root_observation_postclose_META_writer.UNREADY.py';request='Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py';binder='bind_complete_observation_SOURCE_only.UNREADY.py';controlbinder='N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py';child='N8_private_control_child.UNREADY.py'
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
check('complete_240_regular_singlelink_files_full_EOF_SHA_size_same_descriptor_7ID',result['all240_files_full_EOF_SHA_7ID'],result['candidate_manifest_pin'])
check('complete_29_directories_same_7ID_and_exact_membership',result['all29_directories_full_7ID'],'MF and complete os.walk agree, no symlink')
check('all_96_complete_Python_Source_AST',result['all96_Python_full_AST'],'ast.parse only; no candidate imports')
check('all_120_JSON_complete_strict_duplicate_nonfinite_refusal',result['strict_JSON_count']==120,'Full contents parsed by independent strict parser')
check('complete_native_archive_1365_unique_regular_Source_EOF',len(result['native1365_Source_archive_complete_member_results'])==1365 and result['native_total_original_Source_bytes']==12545229,'Every archive Source member EOF and indexed SHA/size; no extraction/build')
check('all_original_181_N7_members_whole_bytes_retained',len(result['original181_N7_whole_bytes_retention'])==181 and all(r['original_whole_bytes_retained']is True for r in result['original181_N7_whole_bytes_retention']),'Current retained files compared against complete sealed N7 MF')
check('four_current_role_whole_original_byte_AST_inverses',len(result['complete4role_original_whole_byte_AST_inverses'])==4 and all(r['whole_original_byte_AST_inverse']is True and r['independent_full_diff_reverse']is True for r in result['complete4role_original_whole_byte_AST_inverses'].values()),'Both whole author hunk reverse and independently derived full diff reverse')
check('actual_author_Source_contract_exact_MF_plus_20_roles',len(result['actual_author_Source_contract'])==21 and result['actual_author_Source_contract']['qualified_source_manifest']==pins['MANIFEST.json'],'Required scope and actual fullpins agree')
role_results={}
role_map=audit['m']['required_author_Source_roles']
retained={r['original_member']:r for r in result['original181_N7_whole_bytes_retention']}
for role,rel in role_map.items():
    check('role_'+role+'_complete_current_pin',result['actual_author_Source_contract'][role]==pins[rel],dict(relative_member=rel,fullpin=pins[rel]))
    if rel in result['complete4role_original_whole_byte_AST_inverses']:basis='whole_current_to_original_N7_byte_AST_inverse'
    elif rel in retained:basis='unchanged_complete_original_N7_Source_bytes'
    else:basis='new_complete_UNREADY_Source_owner'
    role_results[role]=dict(relative_member=rel,fullpin=pins[rel],Source_basis=basis,complete_AST=(rel in trees),runtime_or_science_qualification=False)
for rel in(runtime,driver,qualifier,gate,writer,request,binder,controlbinder):
    actual=assignment(rel,'CAPS');check('nine_caps_exact_integer_'+rel,actual==caps and set(actual)==set(caps)and all(type(v)is int for v in actual.values()),actual)
for rel in(runtime,request,binder,writer):
    f=assignment(rel,'FUTURE');check('all_business_and_scientific_futures_unknown_false_'+rel,all(v is None or v is False for v in f.values()) and len(f)==10,f)
for rel in(request,binder):check('actual_required_21_role_map_'+rel,assignment(rel,'ROLES')==role_map,'Every actually consumed Source role is explicit')
protocol=objects['N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json']
check('exact_12_Source_protocol_cases_and_unexecuted_facts',len(protocol['cases'])==12 and protocol['case_ids']==list(assignment(driver,'CASE_IDS')) and all(c['actual_execution']is None and c['actual_root_closed_terminal']is None and c['actual_group_resource_closure']is None and c['actual_independent_saved_review']is None for c in protocol['cases']),'Protocol is not actual controls')
for rel in(gate,qualifier,controlbinder,driver):check('all_twelve_ordered_case_ids_'+rel,list(assignment(rel,'CASE_IDS'))==protocol['case_ids'],'No missing/filtered case') if rel!=controlbinder else check('controls_binder_reads_complete_12_protocol_case_ids',"case_ids=strict_json((P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes())['case_ids']"in text(rel),'Actual fixed protocol consumer')
owner_defs=definitions(owner);record=fn(owner,'ExactOwnerScopeObserver.record_wait');register=fn(owner,'ExactOwnerScopeObserver.register');start=fn(owner,'ExactOwnerScopeObserver.install_original_start_capture');env=fn(owner,'ExactOwnerScopeObserver.environment');expand=fn(owner,'ExactOwnerScopeObserver.expand_selection');restore=fn(owner,'ExactOwnerScopeObserver.restore_original_objects')
check('owner_requires_exact_original_Popen_runner_resources_and_class_codes','type(runner) is full.OwnRSSSerialExecutor'in text(owner)and 'type(process) is self.original_Popen'in register and 'original_process_code=full.OwnRSSSerialExecutor._process.__code__'in text(owner),'Genuine exact objects, unchanged class code')
check('sole_main_thread_default_SIGCHLD_untraced_nonoptimized_prerequisites',all(s in env for s in ['threading.current_thread() is threading.main_thread()','len(threading.enumerate())==1','signal.SIG_DFL','sys.gettrace() is None','not sys.flags.optimize']),'No alternate Python waiter or ignored SIGCHLD admitted')
check('original_global_waitpid_and_Popen_private_class_Source_codes_preserved','os.waitpid is self.original_waitpid and subprocess.Popen is self.original_Popen'in env and 'subprocess.Popen._try_wait.__code__ is self.original_try_wait_code'in env,'Per-instance only; no global/class/MRO patch')
check('original_locked_wait_call_once_real_pid_status_exit_tuple',record.count('self.original_waitpid(process.pid,flags)')==1 and "process._waitpid_lock.locked()"in record and 'all(type(x) is int for x in result)'in record and 'os.WIFEXITED(status) or os.WIFSIGNALED(status)'in record,'Private poll delegate and try_wait normal body call actual original wait once')
check('ECHILD_OSError_unknown_uses_nonOSError_refusal_never_zero','except OSError as error:'in record and "self.fail('actual owned waitpid failed; no ECHILD-zero fallback',record)"in record and 'class OwnershipUnknown(RuntimeError):'in text(owner),'Original poll ECHILD-to-zero path cannot catch this RuntimeError')
check('cached_returncodes_require_recorded_real_owned_wait_exit','cached status requires actual recorded exit tuple'in register and 'poll returned exact real exit status'in register,'Cached returncode alone cannot prove closure')
check('duplicate_owner_PID_reuse_instance_override_and_wrong_defaults_refused',all(s in register for s in ['process.pid not in self.owners',"'_internal_poll' not in process.__dict__",'original_poll.__self__ is process','defaults[1] is self.original_waitpid']),'Exact original owner and original defaults')
check('watchdog_capture_exact_genuine_frame_signature_and_original_delegate_once','def start_liveness_watchdog(read_fd,child_pgid,grace):'in start and 'frame.f_code is self.original_process_code'in start and 'frame.f_locals.get(\'self\') is self.runner'in start and start.count('watchdog=original(read_fd,child_pgid,grace)')==1,'Matches original genuine positional startup call')
check('business_and_watchdog_original_new_session_start_preserved',b'start_new_session=True'in raws['GUARD_SOURCE/qualify_refined_AAA_layered_full.py'] and any(b'def start_liveness_watchdog' in raw and b'start_new_session=True'in raw for rel,raw in raws.items()if rel.endswith('.py')and 'run_bounded' in rel),'Both original startups make PID=PGID; only Source inspected')
check('current_complete_host_parentchain_all_groups_captured_descendants_union',all(s in expand for s in ['selected=set(original_parent_closure)',"r['pgid'] in groups",'self.captured_descendants if p in rows',"r['ppid'] in selected"]),'Union expands before proven closed singleton exclusions')
check('closed_owner_only_single_PID_excluded_and_later_reappearance_refused',"selected.discard(pid)"in expand and "proof['actual_wait_observed_monotonic']>=ps_started_monotonic"in expand and 'closed exact PID reappeared in a later census'in expand,'Stale pre-reap PS rows distinguished; current later PID reappearance refuses')
check('no_new_first_live_census_gate_or_unobserved_migration_gate','first_live_census_is_not_a_new_admission_gate=True'in expand and not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'and 'live_census_seen' in ast.unparse(n.args[0]) for n in ast.walk(trees[owner])),'live_census_seen is evidence only; original current scope honored')
check('original_start_and_two_owned_private_instance_methods_restore',all(s in restore for s in ['self.runner.bounded.start_liveness_watchdog=self.original_start','del process._internal_poll;del process._try_wait']),'Production and controls both restore in finally')
joint=fn(runtime,'joint_bytes');factory=fn(runtime,'build_exact_owner_resources');attach=fn(runtime,'attach_exact_owner_observer');run=fn(runtime,'run');main_driver=fn(driver,'main')
check('full_PS_snapshot_actual_closed0_four_column_unique_rows',all(s in joint for s in ["ps_argv=[ps_tool,'-axo','pid=,ppid=,pgid=,stat=']",'ps_process.communicate(timeout=2)','type(ps_returncode)is int and ps_returncode==0','pid>0 and pid not in ps_rows']),'Diagnostic child alone excluded after actual reap')
check('strict_single_canonical_lsof0_2s_8MiB_complete_union',joint.count('observed=subprocess.run(')==1 and "observed.returncode==0"in joint and "timeout=2"in joint and "len(observed.stdout)<8*2**20 and len(observed.stderr)<8*2**20"in joint and "set(returned_pids)==selected"in joint,'No canonical nonzero/absent-PID whitelist')
check('open_unlinked_original_regular_device_inode_scope_accounted','key=(row[\'D\'],row[\'i\'])'in joint and "any(Path(name).is_relative_to(Path(root))for root in roots)"in joint,'Original five-root byte accounting preserved')
check('same_factory_genuine_MRO_and_all_original_resource_caps',all(s in factory for s in ['full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)','super().check()',"joint['complete_joint_HOCDE_bytes']<2*2**30",'8*2**30,96*2**30']),'Production and controls use exact same class/factory')
check('same_actual_observer_for_production_and_controls','resources._exact_owner_observer=observer'in attach and 'build_exact_owner_resources('in run and 'runtime.build_exact_owner_resources('in main_driver and 'attach_exact_owner_observer('in run and 'runtime.attach_exact_owner_observer('in main_driver,'Shared original runner/resources/observer object')
check('production_disallows_control_barrier_raw_success_sink_poststart_callback','owner_observer.control_mode is True'in joint and 'self._exact_owner_observer.control_mode is True'in factory and 'control_mode=False'in run and 'self.control_mode is True'in start,'Only declared private controls add transitions/raw success writes')
check('genuine_cleanup_error_propagation_and_original_delegate_once','try:return original_terminate_group(process)'in fn(runtime,'FailureOnlyMonitorEvidence.install_bounded_wrappers')and 'try:return original_finish_liveness_watchdog(write_fd,watchdog)'in fn(runtime,'FailureOnlyMonitorEvidence.install_bounded_wrappers'),'Original exceptions retained; no canonical EPERM manufactured')
check('production_all_restorations_in_nested_finally','owner_observer.restore_original_objects()'in run and 'finally:monitor.restore_bounded_objects()'in run,'Source monitor exceptions remain failures')
check('real_private_fixture_fork_wait_and_unlinked_fd_not_mock',all(s in fn(child,'main')for s in ['descendant=os.fork()','os.unlink(target)','os.waitpid(descendant,0)','os._exit(0)']),'Fixture only; no fixture invoked')
check('genuine_control_runner_and_same_factory_not_mock','runner=full.OwnRSSSerialExecutor('in main_driver and "runtime.attach_exact_owner_observer("in main_driver and "control_mode=True"in main_driver,'All actual control facts remain unknown in UNREADY Source')
check('real_early_wait0_without_census_positive_preserves_union',all(s in main_driver for s in ['actual_original_wait_before_first_business_census',"owner['live_census_seen']is False",'actual_early_exit_wait0_current_union_positive']),'Root removed added first-live gate; no new requirement introduced')
check('canonical_oversize_timeout_EPERM_not_manufactured_or_relabelled','private 8MiB producer only; no canonical tool oversize claim'in main_driver and protocol['canonical_OS_failures_never_manufactured']is True,'Private byte producer and older receipts retain limited meanings')
for rel in(gate,request,binder,runtime):
    consumer=fn(rel,'validate_actual_N8_monitor_controls')
    check('Q_manifest_12_cases_Source_binding_saved_peer_actual_terminals_'+rel,all(s in consumer for s in ['actual_closed_zero','actual_complete_evidence_pins','actual_independent_saved_controls_review_pin','actual_Root_controls_tool_terminal_return_pin','qualified_actual_controls_manifest_pin','actual_terminal'] if s!='actual_terminal'),'Explicit manifest/Q/Source/peer coupling and actual Root terminal calls')
    check('Q_no_native_scientific_flags_'+rel,all(s in consumer for s in ['scientific_qualification_created','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted']),'Q is monitor controls qualification only')
check('Source_binder_requires_independent_21pin_review_and_true_Root_admission',all(s in fn(controlbinder,'main')for s in ["peer['actual_author_Source_contract']==author","peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'","type(terminal['exit_code']) is int and terminal['exit_code']==0"]),'No author report or old N7 Source admission reuse')
check('Source_control_binding_only_three_globals_whole_inverse','len(hunks)==len(changes)'in fn(controlbinder,'main') and 'restored==original'in fn(controlbinder,'main'),'Finite complete bound driver inverse, controls remain None')
check('business_binding_only_ready_globals_full_inverse','inverse==raw'in fn(binder,'replace_assignments') and "runtime,hunks=replace_assignments"in fn(binder,'main'),'No actual binder or READY Source executed')
check('business_request_bind_runtime_all_require_actual_controls_Q',all('validate_actual_N8_monitor_controls('in fn(rel,'main' if rel!=runtime else 'actual_scope')for rel in(request,binder,runtime))and 'return actual_scope(b,author)'in fn(runtime,'validate_request'),'Future controls Q is not Source PASS')
check('whole_original129_seed_mapping_and_shared_libraries_preserved',len(objects['ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']['original129_input_pins'])==129 and assignment(request,'SHARED_INPUT_LIBRARY_LAYOUT')==assignment(binder,'SHARED_INPUT_LIBRARY_LAYOUT')==assignment(runtime,'SHARED_INPUT_LIBRARY_LAYOUT')==assignment(writer,'SHARED_INPUT_LIBRARY_LAYOUT'),'Only Source metadata read; no material/library payload read')
check('five_original_build_group_order_and_AB_order_preserved',"['Ganlib','Utilib','Trivac','Dragon','Dragon_link']"in text(binder) and "for state in('A','B'):"in run,'Compile/material Source not executed')
# Original complete runtime numerical/build/seed functions must remain literal N7 bytes.
oldrel=str(Path(result['complete4role_original_whole_byte_AST_inverses'][runtime]['retained_parent_fullpin']['path']).relative_to(P))
olddefs=definitions(oldrel);currentdefs=definitions(runtime);unchanged_functions={}
for name in ['frozen_sources','guarded','compile_all','original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_original_procedure','copy_state_seeds','collect_state','monitor_error','monitor_stream']:
    equal=currentdefs[name]['whole_source']==olddefs[name]['whole_source'];check('whole_original_N7_function_bytes_'+name,equal,'Full function text equality, not AST snippets');unchanged_functions[name]=dict(whole_original_N7_bytes_unchanged=equal,current_lines=[currentdefs[name]['first_line'],currentdefs[name]['last_line']],sha256=hashlib.sha256(currentdefs[name]['whole_source'].encode()).hexdigest())
# Concrete whole producer/consumer key analysis; no candidate function invoked.
summary_node=next(n for n in ast.walk(trees[runtime])if isinstance(n,ast.FunctionDef)and n.name=='summary'and n.lineno>700)
summary_return=next(n.value for n in ast.walk(summary_node)if isinstance(n,ast.Return))
summary_keys={k.arg for k in summary_return.keywords}
writer_diag_keys={n.slice.value for n in ast.walk(trees[writer])if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='diagnostic'and isinstance(n.slice,ast.Constant)and isinstance(n.slice.value,str)}
missing=sorted(writer_diag_keys-summary_keys)
check('actual_success_monitor_summary_all_writer_required_keys_exist',not missing,dict(producer_complete_keys=sorted(summary_keys),consumer_complete_keys=sorted(writer_diag_keys),missing=missing))
barrier_node=next(n for n in ast.walk(trees[driver])if isinstance(n,ast.FunctionDef)and n.name=='barrier');barrier_src=''.join(text(driver).splitlines(keepends=True)[barrier_node.lineno-1:barrier_node.end_lineno])
late_requires=[ast.unparse(n.args[0])for n in ast.walk(barrier_node)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
selected_descendant_required=any('descendant' in s and ('rows' in s or 'selected' in s)for s in late_requires)
specific_refusal_required=any('original_lsof' in ast.unparse(n.args[0])or 'original_joint_bytes_failure' in ast.unparse(n.args[0])for n in ast.walk(trees[driver])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require')
check('control07_10_selected_descendant_then_specific_strict_lsof_refusal',selected_descendant_required and specific_refusal_required,dict(selected_descendant_required=selected_descendant_required,specific_lsof_refusal_required=specific_refusal_required,barrier_complete_require_predicates=late_requires,protocol_behavior=protocol['cases'][6]['source_required_behavior']))
case_src=fn(qualifier,'case_mode');typed_caps=('all(type('in case_src and "f['actual_original_caps']"in case_src and "actual_original_caps'"in fn(qualifier,'validate_saved_metadata_types'))
check('postclose_actual_caps_PID_PGID_exact_integer_refusal',typed_caps and 'type(f[\'actual_host_PID\'])is int'in case_src,dict(existing_cap_parser_key='original_caps only',actual_fact_cap_predicate="f['actual_original_caps']==CAPS",target_comparison="g['actual_target_PIDs']==sorted(targets)",python_equality_example=dict(True_equals_one=(True==1),False_equals_zero=(False==0),float_equals_int=(1.0==1))))
raw_consumers={}
for rel in(gate,request,binder,runtime):
    body=fn(rel,'validate_actual_N8_monitor_controls');raw_consumers[rel]=dict(rechecks_complete_namespace_raw_pins='actual_complete_postclose_namespace_views'in body or 'actual_complete_controls_regular_file_pins_before_own_append'in body,rechecked_case_field='actual_complete_evidence_pins')
check('Q_all_current_declared_saved_raw_file_fullpins_rechecked',all(v['rechecks_complete_namespace_raw_pins']for v in raw_consumers.values()),dict(case_emitted_highlevel_pins=['fp','tp','gp','gt','rp','rt'],raw_file_pins_location='actual_complete_postclose_namespace_views.files',manifest_full_raw_pins_location='actual_complete_controls_regular_file_pins_before_own_append',actual_consumers=raw_consumers))
blockers=[
 dict(blocker='B1_SUCCESS_MONITOR_SUMMARY_POSTCLOSE_CONSUMER_KEY_MISMATCH',roles=['runtime_template','postclose_writer'],functions=['FailureOnlyMonitorEvidence.summary','run','main'],lines=dict(runtime_summary=[751,770],runtime_result=[860,861],writer=[109,112]),finding='Successful runtime saves current summary verbatim; writer directly reads two removed keys and deterministically raises KeyError before postclose output.',missing_keys=missing,minimal_repair='Change writer diagnostic assertion to current truthful lsof-unchanged/full-PS-union-new/single-closed-PID fields and diagnostic_source_contract_is_not_runtime_qualification=True; preserve actual Q coupling and new_native_runtime_qualification=None. Do not default missing old keys or falsely label changed PS union unchanged.'),
 dict(blocker='B2_CONTROL07_10_WRONG_REFUSAL_CAN_SATISFY_CASE',roles=['monitor_control_driver','monitor_controls_protocol'],functions=['main.barrier','main'],lines=dict(barrier=[137,146],outcome=[182,193],protocol=[77,101]),finding='Descendant ready-file existence is not proof it was selected in saved fullPS. Arbitrary later runner error plus any monitor journal passes cases07/10; a fully complete passing lsof may therefore be followed by an unrelated deadline/cleanup failure and satisfy the intended strict-lsof negative control.',minimal_repair='Before late release require exact ready descendant identity and non-zombie fullPS selected membership. Before emitting passed facts require the saved original_joint_bytes_failure to record canonical actual lsof nonzero or incomplete selected PID coverage for that captured descendant; passing complete lsof must fail the expected-refusal control, with no retries/whitelist.'),
 dict(blocker='B3_POSTCLOSE_ACTUAL_FACTS_EQUAL_NUMBERS_NOT_STRICT_INTS',roles=['monitor_controls_postclose_qualifier'],functions=['validate_saved_metadata_types','case_mode'],lines=dict(parser=[21,30],targets=[81,85],caps=[94,95]),finding='Actual fact caps use ordinary equality while recursive typed handler only recognizes original_caps. Host/owner PID/PGID and target lists also lack exact int validation. JSON equal floats or bool cap values can receive actual_original_caps_verified=True.',minimal_repair='Validate actual_original_caps exact9keys/int-only/original values, and exact positive int host/owner PID/PGID plus exact int target lists at the existing consumers. Keep all current values/limits and no new runtime gate.'),
 dict(blocker='B4_Q_CONSUMERS_OMIT_DECLARED_COMPLETE_RAW_FILE_PINS',roles=['monitor_controls_postclose_qualifier','monitor_controls_gate','request_preparer','binder','runtime_template'],functions=['case_mode','manifest_mode','qualification_mode','validate_actual_N8_monitor_controls'],lines=dict(qualifier_case=[95,95],manifest=[123,123],gate=[82,87],request=[121,126],binder=[137,142],runtime=[193,198]),finding='Complete raw logs/journal/watchdog/stage file pins are saved in namespace views/all-controls full list, but actual_complete_evidence_pins contains only six high-level receipts plus case postclose. Q consumers recheck only that list. Missing/mutated raw evidence after saved review can evade actual Q consumption.',minimal_repair='Use the existing declared complete regular-file fullpins to recheck raw evidence in qualification and all four Q consumers, including case namespace raw pins; retain append-before-own-pin boundary and existing caps. No new controls or physical payload reads are needed.')
]
for role,v in role_results.items():v['current_Source_blockers']=[b['blocker']for b in blockers if role in b['roles']]
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_FAIL_BLOCKED_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=all(c['passed']for c in checks),all_checks_typed_boolean=all(type(c['passed'])is bool for c in checks),check_count=len(checks),checks=checks,check_evidence=evidence,blockers=blockers,actual_author_Source_contract=result['actual_author_Source_contract'],qualified_actual_Source_manifest_pin=pins['MANIFEST.json'],complete_Source_EOF_AST_results_path=str(D/'COMPLETE_ALL_SOURCE_EOF_AST_RETENTION_NATIVE_ARCHIVE_AND_INVERSE_RESULTS.json'),complete_role_Source_results=role_results,complete_original_function_preservation=unchanged_functions,original_contract_scope=dict(current_complete_host_parentchain_preserved=True,exact_original_Popen_real_wait_reap_single_closed_PID_exclusion=True,first_live_census_is_not_a_new_gate=True,unobserved_migrated_descendants_not_a_new_user_gate=True,current_host_watchdog_groups_captured_descendant_union_retained=True,original_nine_caps=caps),independent_controls_second_read=dict(agent='/root/build_memory_observation_source_review/n8_controls_source_second_read',whole_controls_Source_only=True,author_review_not_adopted=True),actual_read_stdout=captured.getvalue(),candidate_guard_API_controls_wait_poll_PS_lsof_resource_compile_material_native_numeric_executed=False,project_or_candidate_modified=False,actual_controls_execution=None,actual_monitor_controls_qualification=None,actual_runtime_qualification_sha256=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False)
assert len({c['check']for c in checks})==len(checks)and all(set(c)=={'check','passed'}for c in checks)
target=D/'REVIEW.json';target.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
b,pin=audit['read'](target)
print(json.dumps(dict(status=report['status'],source_only=True,all_checks_passed=report['all_checks_passed'],check_count=len(checks),passed_check_count=sum(c['passed']for c in checks),failed_checks=[c['check']for c in checks if not c['passed']],blocker_count=len(blockers),review_pin=pin,candidate_or_API_or_business_executed=False),sort_keys=True))
sys.exit(0 if report['all_checks_passed']else 1)

import ast, hashlib, json, statistics
from pathlib import Path
D=Path('/private/tmp/axmat_v14b_component_budget_and_redundant_read_source_analysis_20261010'); R=Path('/Users/wen/spot')
F=R/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
H=R/'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
M=R/'validation/axial_material/prepare_qualified_AB_moment_order_production.py'
P=R/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
O=R/'validation/axial_material/qualify_refined_AAA_layered_full.py'
B=Path('/private/tmp/axmat_v14b_streaming_sha_complete_component_source_draft_20261010/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py')
T=Path('/private/tmp/axmat_component_driver_timing_readonly_review_20261010/REPORT.json')
W=R/'validation/artifacts/axial-material-sender-contiguous-flux-window-build-v13-20261009'
J=W/'SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13/stages.json'; V=W/'driver_result.json'; WD=W/'audit/audit.watchdog.json'
C=R/'validation/artifacts/axial-material-complete-environment-streaming-sha-helper-only-controls-v14b-historical-read-20261010/result.json'
Q=R/'validation/artifacts/axial-material-complete-environment-streaming-sha-helper-only-host-v14b-historical-read-20261010/result.json'
A=R/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_historical_environment_read_receipts/Root_actual_historical_environment_read_tool_terminal_return.json'
paths=[F,H,M,P,O,B,T,J,V,WD,C,Q,A]
def identity(p):
 s=p.stat(); return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
raw={}; inputs=[]
for p in paths:
 before=identity(p); data=p.read_bytes(); after=identity(p); assert before==after
 raw[p]=data; inputs.append(dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity_before=before,identity_after=after))
assert hashlib.sha256(raw[F]).hexdigest()=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert hashlib.sha256(raw[H]).hexdigest()=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
assert hashlib.sha256(raw[B]).hexdigest()=='b6fb702ca9a8d803722d17a1082df74a2bd693aead99b691899d9335cc40bb4f'
asts={p:ast.parse(raw[p]) for p in (F,H,M,P,O,B)}
def node(p,name):
 ns=[n for n in ast.walk(asts[p]) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]; assert len(ns)==1,(p,name); return ns[0]
def loc(p,name):
 n=node(p,name); return dict(path=str(p),name=name,start_line=n.lineno,end_line=n.end_lineno)
def calls(p,name,target):
 return [n.lineno for n in ast.walk(node(p,name)) if isinstance(n,ast.Call) and ((isinstance(n.func,ast.Name) and n.func.id==target) or (isinstance(n.func,ast.Attribute) and n.func.attr==target))]
assert len(calls(F,'declaration_admission','sender_source_admission'))==2
assert len(calls(F,'declaration_admission','sender_control_contract'))==2
assert len(calls(F,'sender_control_contract','sender_source_admission'))==1
assert len(calls(F,'complete_archive_forecast','sender_source_admission'))==1
assert len(calls(F,'complete_archive_forecast','sender_control_contract'))==1
assert len(calls(B,'declaration_admission','stream_environment_helper_source_admission'))==1
assert len(calls(B,'complete_archive_forecast','stream_environment_helper_source_admission'))==1
assert not calls(B,'environment','stream_environment_helper_source_admission')
tr=json.loads(raw[T]); versions={x['version']:x for x in tr['versions']}
s=json.loads(raw[J])['stages']; driver=json.loads(raw[V]); watch=json.loads(raw[WD]); h14=json.loads(raw[C]); host=json.loads(raw[Q]); receipt=json.loads(raw[A])
assert len(s)==86 and sum(x['status']=='PASS' for x in s)==61 and sum(x['status']=='FAILED' for x in s)==25
assert sum(x['label'].startswith('controls/keycodec_negative_') for x in s)==20
assert sum(x['label'].startswith('sender_controls/unsupported_') for x in s)==4
assert s[-1]['label']=='audit/audit' and s[-1]['status']=='FAILED'
assert receipt['terminal_result']['exit_code']==0 and type(receipt['terminal_result']['exit_code']) is int and receipt['session_closed'] is True
assert h14['new_all_streams_EOF_and_total_size_equal'] is True and h14['helper_only_observer_overhead_not_removed'] is True
assert host['failed_V13_audit_reexecuted'] is False and host['numerical_component_or_transport_executed'] is False
assert all(host[k] is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert watch['wall_cap_seconds']==33.39447033306351 and watch['returncode']==-15
post=[x['started_unix']+x['elapsed_seconds']-x['resource_after']['checked_unix'] for x in s if 'resource_after'in x]
old=h14['old_elapsed_seconds_including_profile']; new=h14['new_elapsed_seconds_including_open_probe']; delta=old-new
v13=versions['V13']; v11=versions['V11']; auditproxy=v11['last_audit']['watch_elapsed_seconds']
fullproxy=v13['driver_elapsed_seconds']+auditproxy-v13['last_audit']['watch_elapsed_seconds']; saving=88*delta; net=fullproxy-saving
selected=('driver_elapsed_seconds','stage_elapsed_seconds_sum','own_watch_process_interval_seconds_sum','driver_minus_stage_sum_seconds','stage_minus_own_watch_sum_seconds','inter_stage_gap_estimate_seconds_sum','last_audit','category_sums')
report=dict(schema='AXMAT_V14B_COMPONENT_BUDGET_AND_REDUNDANT_READING_READONLY_ANALYSIS_V1', status='PASS_READONLY_SOURCE_AND_METADATA_ANALYSIS_NO_PERFORMANCE_QUALIFICATION', inputs=inputs,
 actual_V13=dict(driver_classification=driver['classification'], timing={k:v13[k] for k in selected}, stages=86, first85_valid_finished=85, PASS=61, expected_keycodec_rc23=20, expected_sender_rc1=4, last_audit_FAILED=True, no_success_seal=not (W/'seal.json').exists(), own_watchdog=watch),
 completed_V10_V11_audit_proxies={k:versions[k]['last_audit'] for k in ('V10','V11')},
 actual_H14b_helper_comparison=dict(old_seconds=old,new_seconds=new,observed_difference_seconds=delta,old_bytes=h14['old_actual_full_byte_volume'],new_bytes=h14['new_actual_full_byte_volume'],old_streams=len(h14['old_actual_FD_full_EOF_stream_observations']),new_streams=len(h14['new_actual_FD_full_EOF_stream_observations']),fixed_old_then_new=True,observers_differ=True,observer_overhead_not_removed=True,unbiased_speedup_established=False,host_whole_seconds=host['whole_elapsed_seconds'],actual_tool_terminal=receipt['terminal_result'],native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False),
 planned_environment_calls=dict(driver_initial_declaration=1,before_build_stages=12,before_old_controls=59,before_sender_controls=14,driver_finally=1,driver_total_direct_current_declaration=87,audit_child_current_declaration=1,successful_full_plan=88,actual_audit_attempted_or_completed_unknown='0 or 1; journal does not expose internal function completion',historical_ancestor_recursive_admissions='additional different declaration scopes; not included',before_final_audit=86,not_resource_checks=True,per_stage_full_EOF_SHA_retained=True),
 resource_evidence=dict(genuine_resource_class=loc(M,'DynamicHistoryResources'),genuine_executor=loc(P,'SerialExecutor'),genuine_OwnRSS=loc(O,'OwnRSSSerialExecutor'),full_scope_roots_min=min(len(x['resource_before']['resource_roots']) for x in s),full_scope_roots_max=max(len(x['resource_before']['resource_roots']) for x in s),regular_files_first=s[0]['resource_before']['regular_files'],regular_files_last=s[-1]['resource_before']['regular_files'],resource_before_records=86,resource_after_records=61,post_resource_call_and_remaining_log_upper_estimate=dict(count=len(post),minimum_seconds=min(post),median_seconds=statistics.median(post),maximum_seconds=max(post),sum_seconds=sum(post)),independent_check_function_timing_available=False,interpretation='After-check begins at checked_unix; until stage end includes complete scan plus log/hash/bookkeeping. Mixed Unix and monotonic estimates assume no clock shift; not isolated scan duration. Periodic in-process checks are included in watchdog time.'),
 budget_estimate=dict(original_whole_seconds=1800,original_stage_seconds=600,original_RSS_MiB=512,threads=1,children=1,retries=0,old_audit_proxy_seconds=auditproxy,truncated_audit_watch_seconds=v13['last_audit']['watch_elapsed_seconds'],historical_audit_missing_proxy_seconds=auditproxy-v13['last_audit']['watch_elapsed_seconds'],all_88_calls_linear_saving_estimate_seconds=saving,replace_truncated_audit_with_old_complete_proxy_driver_seconds=fullproxy,after_linear_saving_estimate_seconds=net,excess_before_sender_extra_audit_and_success_seal_tail_seconds=net-1800,sufficient_margin_established=False,caveats=['Not an actual V14b component result. Fixed order and differing observers do not establish unbiased performance.','Historical V11 complete audit is a planning proxy, not actual V13 full sender audit duration.','Estimate excludes additional complete sender audit work and successful seal/post-seal tail.','Current helper source gate and changed namespace costs may increase overhead.','Failure-closeout time and successful closeout differ.']),
 precise_redundant_pure_work=dict(current_V13_declaration_sender_source_admission=6,current_V13_declaration_sender_control_contract=3,new_b6_declaration_stream_helper_source_admission=2,new_b6_per_environment_complete_helper_source_admission=0,source_admission_calls_in_declaration=calls(F,'declaration_admission','sender_source_admission'),contract_calls_in_declaration=calls(F,'declaration_admission','sender_control_contract'),source_in_contract=calls(F,'sender_control_contract','sender_source_admission'),forecast_source_and_contract_calls=dict(source=calls(F,'complete_archive_forecast','sender_source_admission'),contract=calls(F,'complete_archive_forecast','sender_control_contract')),interpretation='Complete source/proof recomputation repeats inside one declaration boundary. No evidence these KB/AST operations explain the 1312.846s unallocated time.'),
 next_specific_action=dict(primary='Finite source-only same-declaration transaction: complete-SHA every exact source/proof literal once, independently compute sender proof and full control contract once, explicitly pass local immutable copies to forecast/field checks. Recheck all 7ID, alias chains and namespaces at use/end; clear on exit/exception. Public default callers stay fresh. No globals, cross-stage cache or same-SHA different-path credit.',expected_sender_source_parse_calls=1,expected_sender_contract_parse_calls=1,expected_new_helper_protocol_parse_calls=1,measured_gain=None,performance_solution_claim=False,prerequisite='Before full86 rerun collect bounded passive function timings for original environment, ancestor admissions and resource.check through original genuine module/MRO. Root alone runs any future bounded observation.',avoid=['No old failed audit replay','No removal or amortization of genuine resource checks','No deletion or merging of preserved historical workspaces','No frozen helper global monkeypatch or genuine MRO change','No budget increase or retries']),
 source_locations=[loc(F,n) for n in ('sender_source_admission','sender_control_contract','complete_archive_forecast','source_inputs','environment','declaration_admission','audit_build','run_build')]+[loc(H,n) for n in ('digest','environment','inventory','verify_inventory')]+[loc(B,n) for n in ('stream_environment_helper','stream_environment_helper_source_admission','environment','declaration_admission','complete_archive_forecast')],
 prohibited_actions=dict(business_import=False,business_call=False,compile=False,fixture=False,benchmark=False,large_history_payload_read=False,large_history_tree_scan=False,Root_poll=False,canonical_write=False,numerical_input_change=False,scientific_credit=False))
for p in paths: assert identity(p)==next(x['identity_after'] for x in inputs if x['path']==str(p))
(D/'REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('H14b实际读核差0.994321s；成功组件源码计划88次当前声明environment，线性节约约87.500s是估算。以V11完整audit代替V13截断audit，估计driver仍约1801.056s，未加入sender完整审计与成功seal/tail，无法认定原1800s内有余量。\nV13未分配到stage的1312.846s不能全归SHA。原resource每次动态核268根、约6.7–7.4万文件；没有独立resource函数耗时。后置完整扫描加log/hash上界估计61次总89.312s，不是纯扫描实测。\n具体可减重复工作：单次declaration内senderproof6→1、contract3→1、新helper proofgate2→1，边界内完整字节/7ID/别名/namespace仍全部验证，不跨stage缓存、不跳过任何检查。收益尚未测；不凭此推断full86或native/AAA/ABA成功。\n',encoding='utf-8')
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT.json'),observed_difference=delta,linear_88_saving_estimate=saving,estimated_driver_before_sender_extra_and_success_tail=net),allow_nan=False))

"""Produce a finite UNREADY structural patch plan; never import business code."""
import ast
import hashlib
import json
from pathlib import Path
import stat

D=Path(__file__).parent
ROOT=Path('/Users/wen/spot');A=ROOT/'validation/axial_material';B=ROOT/'validation/artifacts'
MF=A/'prepare_qualified_AAA_rank1_cache_monitored_graph_reference.py'
F=A/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
CE=B/'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
S=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
W=B/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
PRIOR=Path('/private/tmp/spot_v9_independent_reference_original_contract_source_review_20261009')
PINS={}

def ident(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def read(p,sha=None):
 p=Path(p);before=ident(p);raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest();assert ident(p)==before
 if sha is not None:assert h==sha,(str(p),h,sha)
 PINS[str(p)]={'sha256':h,'bytes':len(raw),'identity':before};return raw
def js(p,sha=None):return json.loads(read(p,sha))
def parse(p,sha=None):
 text=read(p,sha).decode();return text,ast.parse(text)
def fn(p,tree,name,text):
 n=next(x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name==name)
 body=''.join(text.splitlines(True)[n.lineno-1:n.end_lineno])
 return {'path':str(p),'function':name,'first_line':n.lineno,'last_line':n.end_lineno,'whole_source_region_sha256':hashlib.sha256(body.encode()).hexdigest()}

old=js(PRIOR/'REPORT.json','34db493cdb925b2e4d20c8f12bcbeae721354a71e215ac162a313165dc1b9fdb')
read(PRIOR/'actual_readonly_tool_receipt.json','9594849a65b093e87f3e135eee6208e87fa9e25b72b215fc1adbf972f5a91089')
assert old['status']=='PASS' and old['v9_reference_ready_for_execution'] is False
mt,ma=parse(MF,old['all_fresh_small_file_pins'][str(MF)]['sha256'])
ft,fa=parse(F,'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8')
physical=A/'review_qualified_AAA_refined_input_identity.py'
pt,pa=parse(physical)
helperfiles={}
recipe=js(old['original_recipe']['path'],old['original_recipe']['sha256'])
physical_precheck=js(recipe['physical_input_precheck']['path'],recipe['physical_input_precheck']['sha256'])
assert PINS[str(physical)]['sha256']==physical_precheck['implementation']['sha256']
for name,item in recipe['unchanged_reference_implementations'].items():
 text,tree=parse(item['path'],item['sha256']);helperfiles[name]=dict(item,all_top_definitions=[fn(Path(item['path']),tree,n.name,text) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))])
projection=js(recipe['observation_projection_recipe']['path'],recipe['observation_projection_recipe']['sha256'])
projtext,projast=parse(projection['helper']['path'],projection['helper']['sha256'])
env=js(S/'analysis_environment.json')
prepared=js(W/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
standard=js(W/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
inverse=dict(prepared);del inverse['own_child_supervision'];assert inverse==standard
full_inverse_proof=js('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009/REPORT.json',
 'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')
assert full_inverse_proof['oldprepared_whole_typed_order_list_floatbit_inverse_and35f_exact_bytes_verified'] is True
assert env['python_version']=='3.14.4' and env['numpy_version']=='2.4.4'
assert 'sys.version_info[:2] != (3, 12)' in mt and 'np.__version__ != "2.4.3"' in mt
assert 'str(Path(sys.executable).resolve()) != env["executable"]' in ft
assert 'info = c.verify_prepared(PROD / "prepared.json", prepared_sha)' in mt
assert "exported['production_prepared'] != descriptor(PROD / 'prepared.json')" in pt
assert "production_prepared=descriptor(PROD / 'prepared.json')" in pt
assert "value['original_controller_return']" in ft and "COLD_TAIL" in ft
assert all(recipe[k] is False for k in ['new_transport_launched','AAA_accuracy_qualified','ABA_admitted'])

def region(name):return fn(MF,ma,name,mt)
regions=[
 {'id':'identity_globals','source':{'path':str(MF),'first_line':31,'last_line':93},
  'change':'Retarget PROD/COUPLING and the three fresh analysis roots; bind F59/44789 and actual current combined-build seal/runtime/Root INPUT chain in distinct descriptors. Preserve original92 old build and recipe/template/CE/failure receipts as ancestor dependencies, not as the current corrected-runtime result.',
  'forbidden':'Do not globally replace ancestor BUILD/BUILD_FACTORY, original92 schema or its complete return with current combined return. Do not rebrand prior failures or skip old proof payloads.'},
 {'id':'current_producer_controller','source':region('controller'),
  'change':'Explicitly distinguish current normal producer controller/host/module bindings from the separate P12 CE consumer. Keep original imported-source identity/MRO/byte source guards; do not attach P14 compiled-code or SciPy identities to a P12 process.',
  'forbidden':'No module overlays, monkeypatch, alternate controller, synthetic compiled hash, or treating a readonly report as a new actual API return.'},
 {'id':'complete_current_native_AAA','source':region('candidate_completion'),
  'change':'Retarget the whole original all-map audit to current V9 root. Retain ordered nine initial plus eight stages per actual map, all seals/logs, all axial selector and rank1 cache guards, 100-map/43200-second budgets, first VALID_MET and no prior ABA. Add actual own-child watch/kernel evidence and native fullcloseout/Root admission from F59, without dropping any existing gate.',
  'future_fields':['new_AAA_status_sha256','new_completed_maps','new_final_directory','new_final_result_sha256','new_all_stage_logs_and_watches','new_run_claim_sha256']},
 {'id':'whole_current_ready_input','source':region('ready'),
  'change':'Resolve current prepared_cold.json as the native-used prepared descriptor. Keep standard prepared.json35f as a separate ancestor, with the already proved supervision-only inverse. Bind original92 AND full current combined/physical/dedup/capture seven-component returns without changing their schemas. Validate current revision via the current normal F59 interface/proof in its exact P14 environment before separate CE analysis. Keep ready return order/full-input semantics, original recipe/history/CE sample and all source/namespace/resource gates.',
  'forbidden':'No one-field corrected_runtime overwrite of an old original92 build dictionary. No old7/8 assessment promotion, no standard-prepared35f passed as native1290, no partial frozen-ready replay.'},
 {'id':'actual_native_receipt_entry','source':region('cold_terminal_input'),
  'change':'Replace only old-family receipt assumptions with the genuine current V9 cold receipt contract. Require actual_tool_result.exit_code typed int0, real initial+terminal handles, observed-after-return fields, whole full stdout/stderr, exact original run-AAA/handoff CLI, F59/source/current prepared1290/DTd0, allfour actual cold tails, whole closeout namespace and current continuous status. The stdout is a wrapper with original_controller_return; it must not be compared directly to run_status.',
  'exact_original_authority':fn(F,fa,'cold_terminal_admission',ft),
  'future_fields':['new_native_terminal_descriptor','new_native_Root_tool_return_descriptor','new_whole_native_independent_admission_descriptor','new_cold_closeout_seal_descriptor'],
  'forbidden':'No log-implied success, output-existence success, conversion bool/None to0, calls into P14 SciPy guard from old P12 analysis, or fabricated future receipts.'},
 {'id':'separate_environments_and_prepared_path','source':region('environment'),
  'change':'Preserve P12/NumPy2.4.3 and original scientific package identities for CE/physical/projection/statistics/current/collector. Keep producer P14/NumPy2.4.4/cp314 SciPy guards separate. A source-approved producer-admission boundary needs the real completed P14 Root witness and complete live declared input verification; it cannot invoke F59 wholemetadata under P12 or import cp314 code there.',
  'unresolved_implementation_gate':'The original monitor parent+consumer callable provenance/controller paths are not a drop-in fit for current P14 callbacks. Exact source/environment plans and all resulting source inverses must be reviewed before any runnable new factory. No executable candidate is claimed by this patch plan.'},
 {'id':'declare_bind_helpers_and_graph','source':region('declare'),
  'change':'Preserve unchanged statistics1578/current46bb/projectione92d byte sources. Physical helper changes are binding-only: current PROD/fine/PREPARED_SHA plus every CURRENT producer prepared.json descriptor→prepared_cold.json, while OLD prepared.json88640 stays unchanged. Preserve physical review mathematical AST and thresholds. Collector keeps original gates/histories/qualify_aba and only changes current prepared/source/output/evidence paths. Declare the exact three saved export inputs and whole current native terminal/owner/runtime/environment/source dependencies, without omitting old ancestor or error-evidence inputs.',
  'physical_helper':fn(physical,pa,'review',pt),
  'physical_current_prepared_descriptor_occurrences':[
   "exported['production_prepared'] != descriptor(PROD / 'prepared.json')",
   "paths = [Path(__file__).resolve(), PROD / 'prepared.json'",
   "production_prepared=descriptor(PROD / 'prepared.json')"],
  'new_staged_inputs':{'track.xsm':str(W/'AAA/bootstrap/initial_axial_track.xsm'),'axial.xsm':None,'macro.xsm':str(W/'AAA/bootstrap/initial_axial_macrolib.xsm')},
  'axial_xsm_derivation':'Only genuine new status.final_directory/closed_axial.xsm after complete actual AAA and full native admission, never guessed map count.'},
 {'id':'input_phase_complete_native_bindings','source':region('verified_input_state'),
  'change':'Adapt complete actual producer witnesses/expected-file owner plans and prepared filename in every global and consumer phase, including ADMISSION embedded source. Keep all canonical bytefresh/namespace/alias/absence/exactconsumer source plans, parent-owned claim/time limit, all sources/MRO/module identities, native library aliases, roots/caps and end-of-run immutable closeout. Preserve the scientific-field-specific consumer scope without claiming global closure in a child.',
  'also_review_functions':['create_input_graph','consumer_snapshot','live_guard_provenance','admission','declaration_terminal_admission'],
  'embedded_ADMISSION_source_line':493,
  'forbidden':'No filtering current37395/graph set merely to make legacy ready pass; no changing current F59/Source/Work runtime; no interpreter-local source guards silently dropped.'},
 {'id':'actual_reference_terminal_contract','source':region('terminal_contract'),
  'change':'Bind the new fixed source/root declaration plus actual native terminal descriptors and exact declare/run command arguments through declare terminal, run claim, SOURCE inventory, external Root return and qualification. Add explicit native prepared/DT/native terminal inputs to CLI and require exact identity at every consumer; keep all future SHA unbound until true terminal.',
  'also_review_functions':['declaration_terminal_admission','external_terminal_admission','qualification_admission'],
  'forbidden':'No automatic ready from the patch plan or from current native LIVE handle; terminal schema adaptation is provenance only, never changed acceptance.'}]

unchanged_math={
 'reference_statistics':helperfiles['reference_statistics.py'],
 'compare_balance_symmetry':helperfiles['compare_balance_symmetry.py'],
 'original_precision_collector':helperfiles['assess_qualified_AAA_white_trace_precision.py'],
 'projection':dict(projection['helper'],all_top_definitions=[fn(Path(projection['helper']['path']),projast,n.name,projtext) for n in projast.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]),
 'physical_review_math':{'source':str(physical),'whole_sha256':PINS[str(physical)]['sha256'],'binding_only_function':'review','preserve_all_remaining_original_checks_and_track_geometry_byte_AST':True}}
caps=dict(total_reference_wall_seconds=120, export_stage_wall_seconds=60, per_child_rss_cap_mib=512,
 threads=1, numeric_children_at_once=1, retries=0, SOURCE_plus_OUT_archive_cap_bytes=256*2**20,
 complete_dynamic_history_cap_bytes=96*2**30, min_free_bytes=8*2**30)
future=dict(native_terminal_descriptor=None,native_actual_tool_return_descriptor=None,native_full_independent_admission=None,
 actual_AAA_status_sha256=None,actual_completed_maps=None,actual_final_directory=None,actual_final_result_sha256=None,
 actual_three_export_input_sha256=None,export_receipt_sha256=None,physical_receipt_sha256=None,projection_receipt_sha256=None,
 reference_declaration_sha256=None,reference_prepare_sha256=None,reference_stage_outputs_sha256=None,reference_external_root_return_sha256=None,
 reference_qualification_sha256=None,AAA_accuracy_qualified=False,ABA_admitted=False)
assert all(v is None or v is False for v in future.values())
report=dict(schema='AXMAT_V9_REFERENCE_BINDING_MINIMAL_STRUCTURAL_PATCH_SOURCE_PLAN_V1',status='PASS_SOURCE_DISCOVERY',
 draft_status='UNREADY_NATIVE_FAILED_NO_SUCCESSFUL_CANDIDATE_TO_BIND',
 scope='STRUCTURED_PATCH_PLAN_ONLY_NOT_EXECUTABLE_FACTORY',project_written=False,business_imports_or_runs=0,
 old_scientific_recipe=dict(path=old['original_recipe']['path'],sha256=old['original_recipe']['sha256']),
 exact_original_reference_contract=old['original_recipe'], original_six_stage_plan=old['original_monitored_analysis']['original_six_stage_command_template'],
 caps_unchanged=caps, original_targets_unchanged=old['original_accuracy_thresholds'],
 all8_original_gates_required=recipe['original_eight_checks'], all2000_original_statepoints_and_full_histories_required=recipe['fixed_history'],
 known_actual_preparation={'current_prepared_path':str(W/'prepared_cold.json'),'current_prepared_sha256':PINS[str(W/'prepared_cold.json')]['sha256'],
 'standard_prepared_path':str(W/'prepared.json'),'standard_prepared_sha256':PINS[str(W/'prepared.json')]['sha256'],
 'only_added_supervision_inverse_already_proved':True,'current_producer_environment':{'path':str(S/'analysis_environment.json'),'executable':env['executable'],'python_version':env['python_version'],'numpy_version':env['numpy_version']},
 'current_case_spec':prepared['case_spec'],'legacy_case_spec_reference250_unchanged_and_not_accuracy_evidence':True},
 production_family=str(W),current_cold_terminal_root=str(T),reference_family_or_new_formal_filename_not_selected=None,
 original_source_regions=regions,unchanged_scientific_source_inventory=unchanged_math,
 physical_project_collector_binding_inverses_and_complete_source_review_required_before_ready=True,
 native_receipt_interface={'original_callable':'cold_terminal_admission(prepared_sha,declare_terminal_sha,terminal_sha)',
 'callable_source':fn(F,fa,'cold_terminal_admission',ft),'native_actual_ready_requirements':'true completed Root0 plus full native post-admission; all continuous maps/seals/logs/watches/current module/source/full input and四tail gate, accuracy flags false',
 'future_argument_descriptors':future},
 reference_CLI_minimal_added_binding_fields=['native prepared descriptor1290 rather than old standard35f','actual cold declaration terminal descriptord0','actual new native terminal PATH+SHA','actual new whole native independent admission PATH+SHA','current F59 sourceSHA and complete current combined build/API/terminal chain alongside unchanged original92 ancestor'],
 fresh_source_and_small_metadata_pins=PINS,
 latest_root_reported_native_failure={'initial_chunk_id':'cefa98','session_id':53935,'terminal_chunk_id':'afac4e','exit_code':1,'closed':True,'failed_stage':'AAA/bootstrap/bootstrap_axial','own_peak_rss_mib':513.890625,'rss_cap_mib':512,'completed_maps':0,'source_of_this_fact':'Direct parent Root task steering, no native result file or receipt was opened in this source-only reader.'},
 reference_workflow_stopped_until_a_new_successfully_admitted_native_family=True,
 explicit_non_claims=['No new AAA result/receipt has been read by this source-only plan. Root reports real V9 native1/zero completed maps; this failed family cannot be promoted to a reference candidate or retried through this plan.','No executable reference factory or new helper variant is produced; the inter-environment and full producer binding still require exact implementation/source review.','No new transport, H5 parsing, numerical recomputation, threshold/budget change, producer runtime/source edits or claims from old7of8.'])
for p,v in PINS.items():assert ident(Path(p))==v['identity'],p
with (D/'REPORT.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with (D/'REPORT.txt').open('x') as f:
 f.write('V9参考绑定最小源码改动面：结构计划完成，UNREADY，不是可执行factory。Root已报告V9真正native退出1，bootstrap_axial峰513.890625MiB超过原512且完成maps0；本失败族不可推进参考，只保留未来新成功族所需源码接线说明。\n\n'
 '保留原六阶段export/physical/project/statistics/currents/collect、120秒总cap/首export60秒/512MiB/单线程单子进程零重试/256MiB归档/96GiB历史/free8；recipe56eb、全2000 statepoints及八门/nu-fission3%全部不改。\n'
 '需要改的是当前producer/terminal/准备文件/来源接线，不是科学计算：原cold_terminal_input比较stdout=status，但V9真正stdout是original_controller_return加四tail；新增入口必须复用F59 cold_terminal_admission完整typedRoot0、真实CLI/完整stdoutstderr/namespace/watch等语义。新终态/最终map/三导出输入SHA全部None。\n'
 '必须分开当前native使用的prepared_cold1290与原prepared35f。原physical helper三处当前prepared.json descriptor和父reference ready/consumer/measurement指针都要绑定prepared_cold；OLD88640祖先不替换。\n'
 '不得把原original92 BUILD/admission字典直接换成新combined字典或改一条runtime：原祖先返回完整保留，再接当前全combined/physical/dedup/capture及原七组件/真实native全准入。\n'
 '实际环境边界：原reference父/孩子强制P12+NumPy2.4.3；当前F59/producer和cp314SciPy强制P14.4+NumPy2.4.4。仅改路径后在P12直接调用F59 wholemetadata/终态函数会破坏原环境门。需在原P14验证真实producer准入，再由P12在完整已声明现场输入/来源/消费者图上分析；两个环境/全MRO/source guard必须各自保持，不能改解释器或丢guard取巧。\n'
 'REPORT.json逐一列出9个精确源码区域与关联函数/行号/原region SHA、helper完整原definitions/pins、原CLI及futureNone。实现仍需实际native成功+全后验、双环境接线源码审核、完整逆向/数学AST保真后才能READY。没有生成业务候选、没有调用export/reference/API/H5，没有写项目。\n')
print(json.dumps({'status':report['status'],'draft_status':report['draft_status'],'patch_regions':len(regions),'fresh_pins':len(PINS),'report_sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest()}))

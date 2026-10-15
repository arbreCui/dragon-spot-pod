"""Finite fixed-file evidence/source reader. No project imports, API calls, or scans."""
import ast, hashlib, json, os, stat
from pathlib import Path
HERE=Path(__file__).parent
ROOT=Path('/Users/wen/spot'); ART=ROOT/'validation/artifacts'
S15=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
R=S15/'actual_component_execution_receipts'
SOURCE=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'
OUT=ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'
TERM=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'
HOST=ART/'axial-material-complete-component-admission-host-v15-20261010'
WHOLE=Path('/private/tmp/axmat_v15_actual_complete86_independent_readonly_review_20261010')
pins={}; checks={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,w=None,capture=False):
 p=Path(p); before=identity(p);assert stat.S_ISREG(before[2]),str(p)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();chunks=[];n=0
 try:
  s=os.fstat(fd);assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
  while b:=os.read(fd,1024*1024):
   h.update(b);n+=len(b)
   if capture:chunks.append(b)
  s=os.fstat(fd);assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
 finally:os.close(fd)
 sha=h.hexdigest();assert n==before[4] and identity(p)==before and (w is None or sha==w),str(p)
 row=dict(path=str(p),sha256=sha,identity=before,size_bytes=n)
 if str(p) in pins:assert pins[str(p)]==row
 pins[str(p)]=row
 return b''.join(chunks) if capture else row
def obj(p,w=None):return json.loads(pin(p,w,True))
def descriptor(p):
 p=str(p)
 if p not in pins:
  assert p in oldpins,'unapproved extra file: '+p
  pin(p,oldpins[p]['sha256'])
 return dict(path=p,sha256=pins[p]['sha256'])
def saved_pin(row):
 current=pin(row['path'],row['sha256'])
 if 'identity' in row:assert row['identity']==current['identity']
 return current
def check(name,predicate):checks[name]=bool(predicate);assert predicate,name
whole=obj(WHOLE/'REPORT.json','3decbb4c2e62082fc6507fbceccd9da4c94e900ab65884a4566416fd74b22f33')
oldpins={x['path']:x for x in whole['all_fresh_full_file_pins']}
whole_receipt=obj(WHOLE/'actual_readonly_tool_terminal_return.json','28430f021c374ac9d17504909c4be3e1aba67a1bc5c7ef7fc49e8bfec0891dae')
check('prior_full86_entire_frozen_SOURCE_OUT_actual_review_bound',whole['all_checks_passed'] is True and len(whole['checks'])==30 and all(whole['checks'].values()) and whole['fresh_SOURCE_OUT_regular_file_count']==7756 and whole_receipt['terminal']['chunk_id']=='67f772' and type(whole_receipt['terminal']['exit_code']) is int and whole_receipt['terminal']['exit_code']==0 and whole_receipt['session_closed'] is True)
binding=obj(S15/'next_combined_READY_source_binding/source_binding_proof.json')
before=pin(binding['source_parent']['path'],'0e4d1e4cbc3daf55b605665e9693a3afa7910b29f4df578d6dcaab812b2026d9',True)
candidate=pin(binding['source_candidate']['path'],'0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382',True)
changes=binding['only_changes'];allowed=['DRAFT_STATUS','TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','SENDER_OBJECT_SHA']
assert [x['name'] for x in changes]==allowed and len(changes)==8
forward=before
for x in reversed(changes):
 old=x['before'].encode();new=x['after'].encode();assert before[x['start']:x['end']]==old
 forward=forward[:x['start']]+new+forward[x['end']:]
check('exact_eight_literal_forward_is_whole_READY_candidate',forward==candidate)
offset=0; positioned=[]
for x in changes:
 old=x['before'].encode();new=x['after'].encode();start=x['start']+offset
 positioned.append((start,start+len(new),old,new));offset+=len(new)-len(old)
reverse=candidate
for start,end,old,new in reversed(positioned):assert reverse[start:end]==new;reverse=reverse[:start]+old+reverse[end:]
check('full_reverse_restores_entire_reviewed_UNREADY_0e4_bytes',reverse==before)
t=ast.parse(candidate);compile(candidate,str(binding['source_candidate']['path']),'exec',dont_inherit=True)
assignments={n.targets[0].id:ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant)}
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('six_future_combined_native_success_pins_still_None',all(assignments[x] is None for x in future))
for name,row in binding['actual_component_success_inputs'].items():
 assert name in allowed[1:];saved_pin(row);assert assignments[name]==row['sha256']
check('all_seven_component_literals_have_genuine_fresh_full_success_file_SHA',set(binding['actual_component_success_inputs'])==set(allowed[1:]))
peer=obj(S15/'independent_next_combined_UNREADY_source_review/REPORT.json','0dbb39d9d5d5a27618b87ce27cd6e3adbaf4a60931e17b274459927cb6b1f11f')
peer_receipt=obj(S15/'independent_next_combined_UNREADY_source_review/actual_readonly_tool_terminal_return.json','8c0683f599e44594b7d5a09cf3ede40658953b50328e825f237c118f9c55c466')
parent_report=obj(S15/'next_combined_UNREADY_source_draft/REPORT.json','310668f0fb5ecbad0802aed53a6015931cf5988547cb273b422b1726b37de939')
pin(S15/'next_combined_UNREADY_source_draft/source_complete_inverse_proof.json','65365088ca669bebd39b0b9eca916f4cca0a3e8fe6cee21c1cc02d60e128ada1')
check('complete_S15_parent_and_actual_sourcepeer_report_chain_bound',peer['all_checks_passed'] is True and len(peer['checks'])==55 and all(peer['checks'].values()) and peer['candidate']['sha256']==binding['source_parent']['sha256']==parent_report['candidate']['sha256'] and peer_receipt['terminal']['chunk_id']=='df6a55' and type(peer_receipt['terminal']['exit_code']) is int and peer_receipt['terminal']['exit_code']==0 and peer_receipt['session_closed'] is True)
root=obj(binding['actual_closed_formal_admission']['path'],'0e203f687a0a5d02e4d3e5a596cf21650333fd98b44549cd1507175502b43b3b')
raw=obj(root['actual_tool_provenance']['Root_actual_raw_tool_terminal_receipt']['path'],root['actual_tool_provenance']['Root_actual_raw_tool_terminal_receipt']['sha256'])
check('genuine_formal_c2b65d_session89358_to9b3290_strict_integer0_CLOSED',raw['initial']['chunk_id']=='c2b65d' and raw['initial']['session_id']==89358 and raw['terminal']['chunk_id']=='9b3290' and type(raw['terminal']['exit_code']) is int and raw['terminal']['exit_code']==0 and 'session_id' not in raw['terminal'] and raw['session_closed'] is True and raw['actual_tool_terminal_return_observed'] is True and raw['record_written_after_actual_terminal_return'] is True and root['actual_tool_provenance']['actual_terminal_return']==raw['terminal'] and type(root['returncode']) is int and root['returncode']==0 and root['actual_tool_provenance']['no_restart'] is True)
source=pin(R/'formal_admission_host.py','95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f',True)
check('real_host_invocation_exact_nonoptimized_single_thread_unprofiled',raw['input']['argv']==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(R/'formal_admission_host.py')] and 'env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1' in raw['input']['cmd'] and b'sys.getprofile() is not None' in source)
host_stdout=obj(root['actual_tool_provenance']['host_full_stdout']['path'],root['actual_tool_provenance']['host_full_stdout']['sha256'])
stderr=pin(root['actual_tool_provenance']['host_full_stderr']['path'],root['actual_tool_provenance']['host_full_stderr']['sha256'],True);assert stderr==b''
h=obj(root['actual_tool_provenance']['actual_genuine_host_result']['path'],root['actual_tool_provenance']['actual_genuine_host_result']['sha256'])
a=obj(root['full_stdout']['path'],root['full_stdout']['sha256'])
w=obj(root['actual_tool_provenance']['actual_child_watchdog']['path'],root['actual_tool_provenance']['actual_child_watchdog']['sha256'])
stages=obj(HOST/'COMPONENT_ADMISSION/stages.json')['stages'];s=stages[0]
for row in [*h['input_sources'],h['original_helper'],h['resource_factory'],h['actual_admission_stdout'],h['actual_watchdog'],host_stdout['actual_host_result'],host_stdout['actual_admission_stdout'],root['actual_tool_provenance']['actual_child_watchdog']]:saved_pin(row)
expected_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'),'admit','--sha256',binding['actual_component_success_inputs']['TRIM_SEAL_SHA']['sha256'],'--terminal-evidence',str(TERM/'terminal_return.json'),'--terminal-evidence-sha256',binding['actual_component_success_inputs']['TRIM_TERMINAL_SHA']['sha256']]
check('true_canonical_three_argument_admit_command_and_all_source_input_identities',h['actual_canonical_command']==root['actual_tool_provenance']['actual_canonical_child_command']==w['command']==s['command']==expected_command and len(h['input_sources'])==4)
check('actual_genuine_single_OwnRSS_child_caps_and_clean_PASS',len(stages)==len(h['stage_records'])==1 and h['stage_records']==stages and h['watchdog']==w and s['label']=='run/admit' and s['status']=='PASS' and type(w['returncode']) is int and w['returncode']==0 and type(w['pid']) is int and w['pid']>0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True and w['rss_cap_mib']==512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<s['elapsed_seconds']<s['wall_cap_seconds']==600 and 0<=w['sampled_peak_rss_mib']==167.375<512)
check('host1800_child600_RSS512_log64MiB_thread1_child1_retry0',tuple(h[k] for k in ['whole_wall_cap_seconds','stage_wall_cap_seconds','rss_cap_mib','archive_cap_bytes','threads','children_at_once','retries'])==(1800,600,512,64*2**20,1,1,0) and h['profile_used'] is False and h['supervisor_class_or_MRO_modified'] is False and 0<h['whole_seconds']==root['whole_host_seconds']==111.36054666701239<1800 and s['log_sha256']==root['full_stdout']['sha256'])
guard_sources={ROOT/'validation/axial_material/prepare_full_ABA_source_factor_transactional_storage_20261006.py':'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'}
# The normal support identifies the exact original class definitions; read its
# constants as syntax, then pin those fixed files, never import the definitions.
support_bytes=pin(h['input_sources'][0]['path'],h['input_sources'][0]['sha256'],True)
supporttree=ast.parse(support_bytes)
check('host_genuine_class_MRO_identity_gate_unchanged_source',b'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)' in source and b'type(runner) is not full.OwnRSSSerialExecutor' in source and b'runner.resources is not resources' in source and h['original_helper']['sha256']=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743' and h['resource_factory']['sha256']=='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')
host_files={};host_dirs={str(HOST):identity(HOST)}
for parent,ds,fs in os.walk(HOST,followlinks=False):
 for name in ds:
  p=Path(parent)/name;assert stat.S_ISDIR(p.lstat().st_mode);host_dirs[str(p)]=identity(p)
 for name in fs:
  p=Path(parent)/name;record=pin(p);host_files[str(p.relative_to(HOST))]=record
check('finite_formal_host_complete5file_namespace_no_failure_and_exact_bounded_runtime',set(host_files)=={'result.json','runtime/run_bounded_dragon.py','run/admit.watchdog.json','run/admit.log','COMPONENT_ADMISSION/stages.json'} and len(host_dirs)==4 and host_files['runtime/run_bounded_dragon.py']['sha256']=='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09' and sum(v['size_bytes'] for k,v in host_files.items() if k!='result.json')==h['archive_before_result_bytes'] and sum(v['size_bytes'] for v in host_files.values())<64*2**20)
d=obj(OUT/'declaration.json',assignments['TRIM_DECL_SHA'])
controls=obj(OUT/'audit/controls.json',oldpins[str(OUT/'audit/controls.json')]['sha256'])
term=obj(TERM/'terminal_return.json',assignments['TRIM_TERMINAL_SHA'])
factory=pin(h['input_sources'][1]['path'],'cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447',True)
ftree=ast.parse(factory);fn=next(n for n in ftree.body if isinstance(n,ast.FunctionDef) and n.name=='production_admission');return_expr=next(n.value for n in reversed(fn.body) if isinstance(n,ast.Return))
terminal=dict(receipt=descriptor(TERM/'terminal_return.json'),full_stdout=dict(path=term['full_stdout']['path'],sha256=term['full_stdout']['sha256']),full_stderr=dict(path=term['full_stderr']['path'],sha256=term['full_stderr']['sha256']),command=term['command'],schema=term['schema'],**{k:term[k] for k in ['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']})
ns=dict(OUT=OUT,SOURCE=SOURCE,build_seal_sha=assignments['TRIM_SEAL_SHA'],d=d,controls=controls,prior=d['inherited_rank1_factor_cache_admission'],stream_admission=d['stream_environment_helper_admission'],terminal=terminal,ROOT_INDEX_RESOURCE_MODULE=Path(h['resource_factory']['path']),ROOT_INDEX_RESOURCE_MODULE_SHA=h['resource_factory']['sha256'],SENDER_OBJECT=Path(a['original_sender_ancestry']['path']),HISTORY_SCOPE_POLICY=d['resource_scope_policy'])
def expression(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name):return ns[n.id]
 if isinstance(n,ast.List):return [expression(x) for x in n.elts]
 if isinstance(n,ast.Tuple):return tuple(expression(x) for x in n.elts)
 if isinstance(n,ast.Dict):return {expression(k):expression(v) for k,v in zip(n.keys,n.values)}
 if isinstance(n,ast.Subscript):return expression(n.value)[expression(n.slice)]
 if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return expression(n.left)/expression(n.right)
 if isinstance(n,ast.Attribute):return expression(n.value)[n.attr]
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
  name=n.func.id
  if name=='dict':assert not n.args and all(x.arg is not None for x in n.keywords);return {x.arg:expression(x.value) for x in n.keywords}
  if name=='str':assert len(n.args)==1 and not n.keywords;return str(expression(n.args[0]))
  if name=='pin':assert len(n.args)==1 and not n.keywords;return descriptor(expression(n.args[0]))
  if name=='parent_factory':assert not n.args and not n.keywords;return dict(PARENT_FACTORY=Path(a['original_factory_ancestry_descriptor']['path']),PARENT_FACTORY_SHA='fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')
  if name=='cache_observer_contract':
   assert not n.args and not n.keywords;cf=next(x for x in ftree.body if isinstance(x,ast.FunctionDef) and x.name==name);assert len(cf.body)==1 and isinstance(cf.body[0],ast.Return);return expression(cf.body[0].value)
 raise AssertionError('unsupported source-expression node '+ast.dump(n)[:200])
expected=expression(return_expr)
check('entire_normal_API_return_body_all_fields_exact_original_source_data_and_fresh_pins',a==expected)
check('full_API_schema_scope_complete68_sender_counts_and_whole_tail_exact',a['schema']=='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15' and a['admission']=='SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_RUNTIME_INPUT_ONLY_V15' and a['original_68_control_counts']==whole['original68_counts'] and a['cache_unit_control_counts']==whole['complete86_counts'] and a['sender_window_control_counts']==whole['sender_counts'] and a['sender_wrapper_raw_controls']==controls['sender_window_controls'] and a['actual_external_terminal_validation']==terminal and a['newly_executed_native_receiver_calls']==2710 and a['sender_wrapper_observer_real_SPOT_credit']==0)
for snapshot in [h['resources_before'],h['resources_after'],s['resource_before'],s['resource_after']]:
 assert snapshot['artifact_budget_bytes']==96*2**30 and snapshot['min_free_bytes']==8*2**30 and 0<snapshot['artifact_bytes']<=96*2**30 and snapshot['disk_free_bytes']>=8*2**30
 assert snapshot['resource_scope_policy']==d['resource_scope_policy'] and snapshot['resource_scope_contract']==d['resource_scope_contract']
 assert {str(HOST),str(SOURCE),str(OUT),str(TERM)}<=set(snapshot['resource_roots']) and set(d['resource_roots'])<=set(snapshot['resource_roots'])
check('actual_saved_before_after_full_history96GiB_free8GiB_scope_caps_original',True)
q=obj(S15/'Root_actual_resource_module_admission.json','5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676')
check('Q_immutable_resource_only_complete_helper_envelopes_unchanged',a['root_index_resource_source_admission']==d['root_index_resource_source_admission'] and a['root_index_resource_source_admission']['complete_actual_resource_module_admission']==q and a['stream_environment_helper_admission']==d['stream_environment_helper_admission'] and a['actual_resource_class_factory']['sha256']==h['resource_factory']['sha256'] and a['original_factory_ancestry_descriptor']['sha256']=='fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')
check('formal_runtime_INPUT_only_no_native_full_FLU_AAA_ABA_or_newcombined_credit',all(a[k] is False for k in ['native_RSS_proof_obtained','actual_full_FLU_entry_executed','full_FLU_entry_execution_proved_by_build','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted','original_accuracy_thresholds_changed']) and all(h[k] is False for k in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']) and all(root[k] is False for k in ['native_RSS_proof_obtained','AAA_accuracy_qualified','ABA_admitted']) and a['future_contract']['require_all_eight_actual_PASS_before_ABA'] is True and all(a['future_contract'][k] is False for k in ['pipeline_prepared','coupled_qualified','AAA_accuracy_qualified','ABA_admitted']) and binding['combined_business_executed'] is False)
shape=pin(R/'Root_postprocessing_shape_assertion_failure.txt',capture=True).decode()
check('Root_evidence_only8e4137_shape_error_preserved_not_business_retry','8e4137' in shape and 'not rerun' in shape and raw['initial']['session_id']==89358 and h['retries']==0)
summary=obj(R/'Root_actual_complete86_and_formal_admission_summary.json')
check('current_Root_complete86_formal_summary_matches_both_actual_closed_runs',summary['formal_runtime_input_admission_completed'] is True and summary['actual_formal_admission']==binding['actual_closed_formal_admission'] and summary['actual_build_seal']==binding['actual_component_success_inputs']['TRIM_SEAL_SHA'] and summary['control_counts']==whole['complete86_counts'] and summary['sender_window_control_counts']==whole['sender_counts'])
check('fixed_files_and_admission_host_namespace_identities_stable_after_read',all(identity(p)==row['identity'] for p,row in pins.items()) and all(identity(p)==ids for p,ids in host_dirs.items()) and {str(Path(parent)/name) for parent,ds,fs in os.walk(HOST,followlinks=False) for name in fs}=={v['path'] for v in host_files.values()})
report=dict(schema='AXMAT_V15_FINAL_READY_BINDING_AND_GENUINE_FORMAL_ADMISSION_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_READY_SOURCE_ONLY_AND_ACTUAL_COMPONENT_RUNTIME_INPUT_ADMISSION',all_checks_passed=True,checks=checks,
 candidate=descriptor(binding['source_candidate']['path']),source_parent=descriptor(binding['source_parent']['path']),eight_byte_exact_literal_changes=changes,six_future_combined_native_pins_None=future,
 actual_full86_report=descriptor(WHOLE/'REPORT.json'),actual_full86_typed_receipt=descriptor(WHOLE/'actual_readonly_tool_terminal_return.json'),entire_full86_report_remains_authoritative_for7756_complete_fresh_files=True,
 actual_formal_Root=descriptor(binding['actual_closed_formal_admission']['path']),actual_formal_raw=descriptor(root['actual_tool_provenance']['Root_actual_raw_tool_terminal_receipt']['path']),actual_formal_stdout=descriptor(root['full_stdout']['path']),actual_formal_complete_API_key_count=len(a),actual_formal_complete_API_full_SHA=root['full_stdout']['sha256'],actual_formal_seconds=h['whole_seconds'],actual_formal_sampled_own_child_RSS_mib=w['sampled_peak_rss_mib'],actual_formal_watchdog=w,
 formal_host_complete_inventory=host_files,sourcepeer_report=descriptor(S15/'independent_next_combined_UNREADY_source_review/REPORT.json'),sourcepeer_typed_receipt=descriptor(S15/'independent_next_combined_UNREADY_source_review/actual_readonly_tool_terminal_return.json'),parent_source_report=descriptor(S15/'next_combined_UNREADY_source_draft/REPORT.json'),all_fresh_fixed_file_pins=list(pins.values()),
 Root_shape_assertion_error_evidence_only_no_business_retry=True,reader_API_evaluation_method='Whitelist AST expression data reconstruction only; no eval/exec of project code or business imports, independent complete equality of all canonical return fields.',
 original_math_stage_guard_threshold_or_Q_changes=False,component_runtime_INPUT_formally_qualified=True,READY_source_review_passed=True,new_combined_runtime_qualified=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 business_imports_or_API_calls=False,numerical_reruns=False,external_resource_scan=False,whole800MB_rehashed=False,Root_session_polled=False,project_files_written=False)
with (HERE/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],checks=len(checks),fixed_file_pins=len(pins),API_full_return_keys=len(a),candidate_sha256=pins[binding['source_candidate']['path']]['sha256'],report_sha256=hashlib.sha256((HERE/'REPORT.json').read_bytes()).hexdigest(),business_executed=False),allow_nan=False))

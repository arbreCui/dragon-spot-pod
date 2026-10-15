"""Finite standard-library SOURCE self-review. Never imports or executes writer/project."""
import ast
import hashlib
import json
from pathlib import Path
import stat
import sys

ROOT=Path(sys.argv[1])
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')
H=Path('/private/tmp/axmat_v21_complete_build_host_actual_SOURCE_binding_20261010_9l6eaiab/combined_build_host.py')
P=B/'actual_complete_combined_prepare_v21_sources/metadata_writer_SOURCE_binding/write_actual_prepare_terminal.py'
OLD=B/'actual_complete_combined_build_v20_sources/combined_build_host.py'
OLDTERM=B/'actual_complete_combined_build_v20_receipts/Root_actual_build_tool_terminal_return.json'
OLDPRE=B/'actual_complete_combined_build_v20_receipts/Root_final_prebuild_sources_prepare_and_resources_check.json'
EXPECTED={
 str(C):'023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',
 str(H):'ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196',
 str(P):'9dc8823bb3c5433d5cac464720e3f8d8da3d631ac0b4eaaef2d6f3bb83ba866d',
 str(OLD):'d5fa7063b8031d5efecd50e157062e7b2faae771788fe105f2d8486d37f19128',
 str(OLDTERM):'50ada42c65a6f7ce2fe33493b5856a5537c261a8070458361f7edffa2e97db3e',
 str(OLDPRE):'0978d39196652f5c18cd75061db6a88931163e82b38f907097cd4a5b6236cbac'}
def identity(path):
 s=path.lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 first=identity(path)
 assert stat.S_ISREG(first[2])
 with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(path)==first
 return dict(path=str(path),sha256=digest,identity=first)
def exact_read(path):
 first=pin(path);raw=path.read_bytes();assert pin(path)==first
 return first,raw
sources={};inputs=[]
for name,sha in EXPECTED.items():
 q,raw=exact_read(Path(name));assert q['sha256']==sha
 inputs.append(q);sources[name]=raw
writer=ROOT/'write_actual_build_postclose_META.py'
wp,raw=exact_read(writer)
tree=ast.parse(raw);canonical=ast.parse(sources[str(C)]);host=ast.parse(sources[str(H)])
defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
cdefs={n.name:n for n in canonical.body if isinstance(n,ast.FunctionDef)}
hassign={target.id:n.value for n in host.body if isinstance(n,ast.Assign) for target in n.targets if isinstance(target,ast.Name)}
wassign={target.id:n.value for n in tree.body if isinstance(n,ast.Assign) for target in n.targets if isinstance(target,ast.Name)}
allowed={'argparse','ast','hashlib','json','math','os','pathlib','stat','time'}
imports=set()
for node in ast.walk(tree):
 if isinstance(node,ast.Import): imports.update(v.name for v in node.names)
 if isinstance(node,ast.ImportFrom): imports.add(node.module)
assert imports<=allowed
for node in ast.walk(tree):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
  assert node.func.id not in {'eval','exec','compile','__import__'}
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
  assert node.func.attr not in {'unlink','rmdir','remove','rmtree','rename','Popen','run','execute','exec_module','setprofile','sleep'}
  if node.func.attr=='replace':
   assert isinstance(node.func.value,ast.Name) and node.func.value.id=='key'
assert {n.name for n in tree.body if isinstance(n,ast.FunctionDef)}=={
 'identity','ordinary','pin','short','exact_pin','pairs','reject_nonfinite','read','bound_read',
 'write_new','copy_exact','snapshot','compact_inventory','namespace_bytes','typed_terminal',
 'compare_source_freeze','finite_number','watch_ok','expected_commands','success_checks','main'}
labels=ast.literal_eval(wassign['LABELS'])
assert labels==ast.literal_eval(cdefs['stage_labels'].body[0].value)
assert labels==ast.literal_eval(hassign['EXPECTED_LABELS'])
hcommands=ast.literal_eval(hassign['EXPECTED_COMMANDS'])
# Evaluate only a restricted AST data grammar; do not execute candidate functions.
def data(node,context):
 if isinstance(node,ast.Constant): return node.value
 if isinstance(node,ast.Name): return context[node.id]
 if isinstance(node,ast.List): return [data(value,context) for value in node.elts]
 if isinstance(node,ast.Tuple): return tuple(data(value,context) for value in node.elts)
 if isinstance(node,ast.Subscript): return data(node.value,context)[data(node.slice,context)]
 if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div): return data(node.left,context)/data(node.right,context)
 if isinstance(node,ast.Call):
  if isinstance(node.func,ast.Name) and node.func.id in {'str','Path','nonzero_sha'}:
   value=data(node.args[0],context)
   return str(value) if node.func.id=='str' else Path(value) if node.func.id=='Path' else value
  if isinstance(node.func,ast.Attribute) and node.func.attr=='resolve' and not node.args:
   return data(node.func.value,context)
 if isinstance(node,ast.Starred): return data(node.value,context)
 raise AssertionError('unsupported SOURCE AST data grammar '+ast.dump(node))
def sequence(node,context):
 if isinstance(node,ast.List):
  answer=[]
  for value in node.elts:
   if isinstance(value,ast.Starred): answer.extend(data(value.value,context))
   elif isinstance(value,ast.List): answer.append(sequence(value,context))
   else: answer.append(data(value,context))
  return answer
 return data(node,context)
art=Path('/Users/wen/spot/validation/artifacts')
out=art/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'
decl={'production_link_command':hcommands[0],'actual_production_objects':hcommands[1][2:],
 'python_command':hcommands[4][0],'actual_prep_terminal_sha256':ast.literal_eval(hassign['PREP_SHA'])}
ctx={'d':decl,'expected':ast.literal_eval(hassign['DECLARATION_SHA']),
 'FACTORY':C,'OUT':out,'O':out,'ART':art,'NM':Path('/usr/bin/nm'),'OTOOL':Path('/usr/bin/otool'),
 'OLD':art/'axial-material-rank1-factor-cache-build-20261007',
 'PHYSICAL':art/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007',
 'DEDUP':art/'axial-material-rank1-factor-cache-memory-dedup-build-20261007',
 'TRIM':art/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010',
 '__file__':str(C),'DECL_SHA':ast.literal_eval(hassign['DECLARATION_SHA']),
 'PREP_SHA':ast.literal_eval(hassign['PREP_SHA'])}
for n in cdefs['stage_commands'].body:
 if isinstance(n,ast.Assign):
  for target in n.targets:
   assert isinstance(target,ast.Name);ctx[target.id]=data(n.value,ctx)
 elif isinstance(n,ast.Return): ccommands=sequence(n.value,ctx)
assert ccommands==hcommands
assert sequence(defs['expected_commands'].body[0].value,ctx)==hcommands
text=raw.decode()
require_fragments=[
 "type(terminal.get('exit_code')) is not int", "'session_id' in terminal",
 "record.get('closed') is not True", "record.get('observed_after_actual_terminal_return') is not True",
 "record.get('session_repolled_after_close') is not False",
 "terminal['exit_code']!=0", "record.get('record_producer')!='root'",
 "original!=fixed_pins", "compare_source_freeze(freeze)", "no_SOURCE_append_after_freeze",
 "set(actual['files'])!=set(seal['files'])|{'seal.json'}",
 "watches!=result['watchdogs']", "watches[:-1]!=audit['previous_stage_watchdogs']",
 "raw['before_binary_identity_gates'] is not True", "raw['complete_raw_tools_and_link_stdout'] is not True",
 "tails!=h['actual_tail_fields']", "independent_child_stderr_empty_verified=False",
 "separate_child_stderr_captured=False", "full_declared_physical_input_prelaunch_7ID_claimed=False",
 "full_declared_physical_input_finalpass_claimed=False", "actual_metadata_writer_source=writer_pin",
 "'ROOT_V21_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1'", "fixed=prelaunch['fixed_input_pins']",
 "namespace_bytes(current)+anticipated+anticipated_metadata_bound",
 "full_stdout=short(T/'actual_build_child_merged_stdout_stderr.json')",
 "full_stderr=short(T/'actual_build_external_host_stderr.txt')",
 "receipt=T/'terminal_return.json'", "receipt=T/'failed_build_terminal_return.json'",
 "source=short(FACTORY)", "command=checks['command']", "build_seal=short(O/'seal.json')",
 "prep_terminal_evidence=short(T/'declaration_terminal_return.json')",
 "if args.mode=='success-if-complete' and terminal['exit_code']==0 and not errors", "checks=success_checks(actual,terminal,prelaunch,fixed)",
 "if args.mode=='failure-only' and terminal['exit_code']==0",
 "Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass=True",
 "if checks is not None:", "original_five_build_stages_executed=checks is not None"]
for part in require_fragments: assert part in text,part
assert ast.literal_eval(wassign['FALSE_FIELDS'])==(
 'whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed',
 'native_RSS_qualified','combined_runtime_native_RSS_proved','mathematical_controls_newly_executed',
 'actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete')
main_text=ast.get_source_segment(text,defs['main'])
assert main_text.index('terminal=typed_terminal(actual)')<main_text.index('copy_exact(paths[key]')
assert main_text.index('checks=success_checks')<main_text.index('receipt=T/')
# True caps are literal Source values and remain the same scope as parent.
caps=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='WHOLE' for target in n.targets for x in ast.walk(target)))
def integer(node):
 if isinstance(node,ast.Constant) and type(node.value) is int: return node.value
 if isinstance(node,ast.BinOp):
  a,b=integer(node.left),integer(node.right)
  if isinstance(node.op,ast.Mult): return a*b
  if isinstance(node.op,ast.Pow): return a**b
 raise AssertionError('invalid literal cap')
assert [integer(value) for value in caps.value.elts]==[1800,600,512,2*2**30,96*2**30,8*2**30]
for q in inputs: assert pin(Path(q['path']))==q
assert pin(writer)==wp
report=dict(schema='AXMAT_V21_COMPLETE_BUILD_POSTCLOSE_META_WRITER_SOURCE_ONLY_SELF_REVIEW_V1',
 status='FINITE_SOURCE_ONLY_DESIGN_SELF_REVIEW_PASS_NOT_EXECUTED',
 candidate=wp,all_read_source_and_saved_old_META_inputs=inputs,
 all_input_full_EOF_SHA7ID_beforeafter_equal=True,standard_library_only=True,AST_parsed_whole_writer=True,
 writer_imported_or_executed=False,project_API_guard_numeric_or_build_executed=False,
 live_ART_files_read=False,closed_sessions_polled=False,
 full_five_stage_commands_Source_AST_data_templates_exact_equal_to_canonical_and_normal_host=True,
 original_genuine_supervisor_mro_or_algorithm_modified=False,
 original_caps=dict(whole1800=1800,stage600=600,rss512MiB=512,joint2GiB=2*2**30,
 history96GiB=96*2**30,free8GiB=8*2**30,threads=1,children=1,retries=0),
 required_actual_Root_inputs=['strict typed integer closed original tool record',
 'prelaunch dynamic complete SOURCE freeze','ordered fixed_input_pins preserving repeated entries',
 'byte-exact actual parent_stdout.log','byte-exact actual parent_stderr.log'],
 complete_saved_namespaces=['HOST','SOURCE','OUT','TERMINAL','D','E_snapshot_before_manifest_and_summary'],
 source_inventory_dynamic=True,expected_installed_D_count_not_hardcoded=True,
 successful_terminal_contract_fields_preserved=True,
 complete_original_five_stages_five_watches_seal_driver_audit_runtime_four_tails_preserved=True,
 complete_declared_physical_inputs_stream_hashed=True,
 physical_postclose_identity_not_pretended_to_be_prelaunch_7ID=True,
 original_fixed_pins_prelaunch_and_postclose_exact_ordered=True,
 merged_child_and_external_host_stderr_scope_honest=True,
 failure_does_not_write_success_terminal=True,partial_records_and_all_existing_namespaces_preserved=True,
 no_existing_file_overwrite_or_cleanup=True,
 retained_joint_archive_includes_H_S_O_T_D_E_factory_and_writer=True,
 prewrite_metadata_budget_bound_original_cap_unchanged=True,
 independent_root_history_resource_or_binary_audit_API_not_reexecuted=True,
 actual_measurement_or_success_predicted=False,
 limits=['Design has not been executed or runtime tested; Root and peer may independently SOURCE review before use.',
 'Writer accepts only the disclosed V21 Root PREP-shaped terminal fields and prelaunch schema; exact future field names must match.',
 'Closed Root tool result is external evidence. Script preserves and checks a Root supplied hash, not an OS tool-attestation service.',
 'Genuine resource and binary audit facts originate in actual normal host and canonical five stages; no project API re-execution by writer.',
 'SOURCE success is not actual full-build/whole INPUT/native/AAA/ABA/physics qualification.',
 'Any future metadata tool failure is preserved as actual metadata failure; never retry original business or overwrite its evidence.'],
 **{key:False for key in ast.literal_eval(wassign['FALSE_FIELDS'])})
(ROOT/'SOURCE_DESIGN.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(ROOT/'SOURCE_DESIGN.txt').write_text(
 'V21 完整五阶段构建关闭后凭证：有限 SOURCE 设计自审通过，脚本未执行。\n'
 '仅 Root 提供真实 strict integer EXIT0 CLOSED 且原完整五阶段/五watch/完整seal/driver/audit/runtime/四tails/全部输入与原上限均通过时写 T/terminal_return.json。\n'
 '非零或保存检查未通过：写真实 failed_build_terminal_return 与失败 summary，完整保存已创建流和 H/S/O/T/D；不写成功凭证，不删除，不重跑构建。\n'
 '正常 host 62条固定输入按实际有序清单保留重复项，不硬编码数量；SOURCE 文件和目录清单动态，当前30文件仅为 Root 告知状态，未读取 LIVE D/ART。\n'
 '完整 d.files 仅按显式路径流式 EOF hash。物理输入 postclose 7ID 是新观察，不伪称未捕获的 prelaunch 7ID。所有原 fixed_input_pins 前后完整 SHA/7ID。\n'
 '完整 child build.log 实际 stdout+stderr 合并；full_stderr 是真实外部 host stderr，独立 child stderr 未捕获也未验证为空。\n'
 '原whole1800s、每stage600s、512MiB、联合2GiB、history96GiB/free8GiB、1线程/1子进程/0retry保持。全部 SOURCE/OUT/HOST/TERMINAL/D/E实际文件计数，E root manifest/summary 后新增条目的时间边界明确。\n'
 '只标准库 SOURCE/META；本次不导入 writer 或项目，不调用 guard/API，不读 live 输出，不授 whole INPUT、native、AAA/ABA 或物理资格。\n'
 '未来必须由 Root 保存该 writer 的真实工具返回，再独立封存/审查成功或失败证据。任何 metadata 异常也保存，不用源码自审替代实际执行。\n')
print(json.dumps(dict(status=report['status'],writer_sha256=wp['sha256'],
 SOURCE_inputs=len(inputs),writer_bytes=wp['identity'][4],all_source_beforeafter_equal=True,
 writer_executed=False,no_business_or_science_credit=True)))

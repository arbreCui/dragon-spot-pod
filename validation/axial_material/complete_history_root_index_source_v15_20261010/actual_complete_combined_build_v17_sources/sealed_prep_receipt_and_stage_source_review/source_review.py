import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
A=Path('/Users/wen/spot/validation/artifacts')
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
H=A/'axial-material-complete-combined-prepare-host-v17-20261010'
O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010'
S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010'
T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010'
E=B/'actual_complete_combined_prepare_v17_receipts'
def pin(path,wanted=None):
 p=Path(path);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 q=p.lstat();assert before==[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
 assert wanted is None or digest==wanted
 return dict(path=str(p),sha256=digest,identity=before)
def read(p):return json.loads(Path(p).read_text())
source=pin(C,'feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c')
summary=pin(E/'Root_actual_complete_combined_prepare_summary.json','07494a308553d0e42f861732f7f2c782bc0f77e7668aa307551fcc82c27bbf3e')
d=read(O/'declaration.json');h=read(H/'result.json');e=read(T/'declaration_terminal_return.json');r=read(E/'Root_actual_prepare_tool_terminal_return.json')
prep=pin(T/'declaration_terminal_return.json','c743c01c3f40ac32e06a4f3371c82dfa4b84314b0c85509aa1710216afe569b2')
assert e['schema']==d['actual_external_prepare_terminal_contract']['schema'] and e['record_producer']=='root'
assert e['source']==dict(path=str(C),sha256=source['sha256'])
assert e['command']==h['watchdog']['command']==[d['python_command'],str(C),'prepare-build']
assert e['declaration']==dict(path=str(O/'declaration.json'),sha256='cb1984ee991230e9b56a9783acafe36bfb9063b4b641ebe64387d3e60c29fb30')
assert e['input_graph']==d['input_graph'] and e['historical_whole_component_body']==d['historical_whole_component_body'] and e['historical_PREP']==d['historical_PREP'] and e['actual_last_cprime_trim_component_INPUT']==d['actual_last_cprime_trim_component_INPUT']
assert all(e[k] is True for k in ('successful_declaration_input_observed','actual_tool_terminal_return_observed','record_written_after_actual_terminal_return','trim_component_API_executed_in_this_PREP'))
assert all(e[k] is False for k in d['actual_external_prepare_terminal_contract']['false_fields'])
assert type(e['returncode']) is int and e['returncode']==0 and type(e['actual_tool_result']['exit_code']) is int and e['actual_tool_result']['exit_code']==0
assert e['actual_tool_result']==r['terminal_tool_return'] and r['terminal_tool_return']['chunk_id']=='e1b00f' and r['closed'] is True and 'session_id' not in r['terminal_tool_return']
assert e['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and e['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR'
assert e['separate_child_stderr_captured'] is False and e['independent_child_stderr_empty_verified'] is False
paths=[T/'declaration_terminal_return.json',Path(e['full_stdout']['path']),Path(e['full_stderr']['path']),Path(e['source_inventory']['path'])]
assert len(set(paths))==4 and all(p.parent==T for p in paths)
proof_pins=[prep]+[pin(e[k]['path'],e[k]['sha256']) for k in ('full_stdout','full_stderr','source_inventory')]
assert Path(e['full_stdout']['path']).read_bytes()==Path(h['actual_prepare_stdout']['path']).read_bytes()
assert read(e['full_stdout']['path'])==dict(declaration=str(O/'declaration.json'),declaration_sha256=e['declaration']['sha256'])
assert Path(e['full_stderr']['path']).read_bytes()==(E/'parent_stderr.log').read_bytes()==b''
observed_files={};dirs=[]
for parent,children,files in os.walk(S,followlinks=False):
 for name in children:
  p=Path(parent)/name;assert not p.is_symlink();dirs.append(str(p.relative_to(S)))
 for name in files:
  p=Path(parent)/name;q=pin(p);observed_files[str(p.relative_to(S))]=q['sha256']
inv=dict(files=observed_files,symlinks={},directories=sorted(dirs))
assert inv==read(e['source_inventory']['path'])==d['source_inventory']
text=C.read_text();tree=ast.parse(text)
def func(name):return next(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
fragments={name:func(name) for name in ('prepare_terminal_contract','prepare_terminal_admission','run_build','stage_labels','stage_commands','external_terminal')}
full=Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py');parent=A/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
support=pin(B/'actual_prepare_sources/prepare_cli_host_v15.py','3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7')
fullpin=pin(full,'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6');parentpin=pin(parent,'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128')
assert 'stderr=subprocess.STDOUT' in full.read_text() and 'stderr=subprocess.STDOUT' in parent.read_text()
reference_pins=[pin(B/'actual_component_execution_receipts/formal_admission_host.py','95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f'),pin(B/'actual_combined_prepare_sources/combined_prepare_host.py','310ddc9d4145060b6f6aa0e250dd470ef05aef43c7d4c2b0c234983351d0b434'),pin(B/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'),pin(B/'actual_component_execution_receipts/Root_actual_run_tool_terminal_return.json')]
command=[d['python_command'],str(C),'run-build','--sha256',e['declaration']['sha256'],'--prep-sha256',prep['sha256']]
objects=d['actual_production_objects']
stage_commands=[d['production_link_command'],['/usr/bin/nm','-g',*objects],['/usr/bin/nm','-g',str(O/'runtime/Dragon')],['/usr/bin/otool','-L',str(O/'runtime/Dragon'),str(A/'axial-material-source-factor-build-20261006/runtime/Dragon'),str(A/'axial-material-physical-source-build-20261007/runtime/Dragon'),str(A/'axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon'),str(A/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/runtime/Dragon')],[d['python_command'],str(C),'audit-build','--sha256',e['declaration']['sha256'],'--prep-sha256',prep['sha256']]]
# The otool dependency path constants below are source-derived, not guessed; inspect literal top-level binding values.
constant_sources={}
for n in tree.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('OLD','PHYSICAL','DEDUP','TRIM'):
  name=n.targets[0].id;value=n.value
  assert isinstance(value,ast.BinOp) and isinstance(value.op,ast.Div) and isinstance(value.left,ast.Name) and value.left.id=='ART' and isinstance(value.right,ast.Constant)
  constant_sources[name]=A/value.right.value
assert set(constant_sources)=={'OLD','PHYSICAL','DEDUP','TRIM'}
stage_commands[3]=['/usr/bin/otool','-L',str(O/'runtime/Dragon')]+[str(constant_sources[k]/'runtime/Dragon') for k in ('OLD','PHYSICAL','DEDUP','TRIM')]
plan=dict(schema='SOURCE_ONLY_FINITE_V17_FIVE_STAGE_RUN_HOST_ADAPTATION_PLAN_V1',status='SOURCE_ONLY_NO_HOST_OR_BUSINESS_EXECUTED',preferred_parent_source=reference_pins[2],immutable_factory=source,actual_prep_receipt=prep,actual_declaration=e['declaration'],next_exact_canonical_command=command,expected_inner_five_stage_labels=d['stages'],expected_inner_five_stage_commands_derived_from_literal_SOURCE_without_API=stage_commands,outer_command_wall_cap_seconds=1800,inner_original_stage_wall_cap_seconds=600,rss_cap_mib=512,archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,min_free_bytes=8*2**30,thread_environment_keys=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'],all_values_one=True,one_original_numeric_stage_child_at_a_time=True,retries=0,future_business_success_pins=None,
 finite_adaptations=[
 'Retarget HOST to a fresh standalone whole-build host; keep prepared SOURCE/OUT and fixed TERMINAL existing. Require no prior OUT/execution_claim.json, seal.json, driver_result.json or closeout_failure.json.',
 'Keep original normal 619 loading, guard_admission(full), exact OwnRSSSerialExecutor bases, full/production paths and genuine ebbb DynamicHistoryResources. No class/MRO/method/module-global override.',
 'Bind exact canonical target source, actual immutable declaration, graph, PREP receipt plus all four terminal proof files, Root closed typed0 receipt and summary; all immutable SOURCE files must stay full-byte/7ID equal before/after.',
 'Use the exact run-build argv with actual declaration/PREP hashes. Genuine outer executor wrapper receives remaining whole1800 cap; inner canonical run_build remains all five original stages each<=600 with its own original deadline and guard.',
 'Keep merged child log as merged output and external host stderr as external stderr, with explicit scopes; do not claim separate child stderr zero. Separate outer host command versus watched canonical command.',
 'Verify all five stage labels/commands/status PASS and watch exact commands/typed0/no-limit/own-child/cleanup/peak<512/wall<=600; verify complete raw metadata receipt, binary audit result, driver result, full OUT seal and all four actual tail fields.',
 'Validate actual whole SOURCE+OUT size equals child actual_archive_bytes and both <2GiB; additionally retain/count fresh Root HOST/TERMINAL/source-review artifacts within the outer same2GiB scope. Preserve dynamic history96/free8.',
 'Keep declaration/SOURCE immutable; allow only original run_build newly created OUT artifacts. Outer post-check must not try to revalidate mutable stages/output as immutable inputs. Root receipt written only after actual external typed0 CLOSED.',
 'Print only exact success evidence bounded by real host tail; no native transport or full FLU call occurs here, so whole INPUT/native RSS/AAA/ABA remain false. No retry after failure.'
 ],source_only_stage_algorithms_unchanged=True)
field_map=dict(schema='V17_PREP_RECEIPT_HONEST_FIELD_SOURCES_V1',source=e['source'],command={'actual_supervised_canonical_argv':e['command'],'actual_external_host_launch_arguments_source':str(E/'Root_actual_prepare_tool_terminal_return.json')},actual_tool_result_source={'path':str(E/'Root_actual_prepare_tool_terminal_return.json'),'field':'terminal_tool_return','chunk_id':'e1b00f','typed_exit_code':0},full_stdout={'scope':e['full_stdout_scope'],'path':e['full_stdout']['path'],'byte_origin':h['actual_prepare_stdout']['path'],'meaning':'Full actual canonical child stdout and stderr merged by unchanged OwnRSS _process.'},full_stderr={'scope':e['full_stderr_scope'],'path':e['full_stderr']['path'],'byte_origin':str(E/'parent_stderr.log'),'meaning':'Full actual external Root host stderr; no separate canonical child stderr claim.'},separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False,source_inventory={'file':e['source_inventory'],'fresh_root_source_file_count':len(inv['files']),'exact_declaration_inventory_equal':True},equality_fields_copied_exact_from_fresh_declaration=['input_graph','historical_whole_component_body','historical_PREP','actual_last_cprime_trim_component_INPUT'],source_and_declaration_only_path_sha_fields=True,all_four_terminal_paths_distinct_and_direct_fixed_TERMINAL_children=True,limitations='This satisfies unchanged reader content/shape facts with explicit original merged-stream provenance; it does not prove that independently captured child stderr is zero bytes.')
for q in [source,summary,support,fullpin,parentpin,*reference_pins,*proof_pins]:assert pin(q['path'],q['sha256'])==q
out=Path(tempfile.mkdtemp(prefix='axmat_v17_prep_receipt_and_five_stage_host_source_review_20261010_',dir='/private/tmp'))
report=dict(schema='FINITE_V17_PREP_RECEIPT_AND_FIVE_STAGE_HOST_SOURCE_REVIEW_V1',status='PASS_SOURCE_AND_ACTUAL_PREP_RECEIPT_SHAPE_ONLY',no_blocking_source_issue=True,actual_prep_receipt=prep,actual_declaration_sha256=e['declaration']['sha256'],honest_original_merged_stream_protocol_accepted=True,separate_child_stderr_empty_proven=False,source_inventory_fresh_file_count=len(inv['files']),actual_root_terminal_exit0_closed=True,canonical_source=source,summary=summary,source_inputs=[support,fullpin,parentpin,*reference_pins,*proof_pins],next_canonical_command=command,source_functions_reviewed=list(fragments),source_or_stage_algorithm_changed=False,business_or_helper_or_module_API_executed=False,five_stage_build_executed=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(out/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(out/'PREP_RECEIPT_FIELD_SOURCES.json').write_text(json.dumps(field_map,indent=2,allow_nan=False)+'\n')
(out/'FIVE_STAGE_HOST_ADAPTATION_PLAN.json').write_text(json.dumps(plan,indent=2,allow_nan=False)+'\n')
(out/'SOURCE_FUNCTIONS.json').write_text(json.dumps(fragments,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('正式 PREP receipt 源码 / 事实形状有限审查通过，无阻塞。\n固定 receipt c743c01… 与声明 cb1984…、Root e1b00f typed EXIT0 CLOSED、11 个 SOURCE 全 EOF 独立清单相符。\n原 canonical 子进程完整合并 stdout+stderr 与实际外部 host stderr 分别 byte-exact 绑定；scope 显式、独立 child stderr 未捕获且不能证明其为空。这样保留原 reader 的有限真实检查含义，没有造空 child stderr 或改 API。\n下一 host 从 genuine V17 PREP host 作有限适配：只新 HOST 需不存在，SOURCE/OUT/TERMINAL 为既有准入材料；目标 run-build 精确绑定声明和 PREP SHA。外层监督完整命令用剩余 whole1800，内层原5stage每项600，RSS512、2GiB、history96/free8、1 numeric child / 0 retry、原类/MRO 均保持。\n五stage命令从 SOURCE literals 和声明字段静态推导，没有调用模块API。host应核验完整5stage/所有watchdog/rawreceipt/audit/seal/四tail与实际Root终态；build输出可增长，原SOURCE/声明/graph/PREP输入保持。\n本轮只读 SOURCE 和 PREP metadata，不运行 build/helper/numeric。原5stage、whole INPUT、native、AAA / ABA 成功尚待实际执行。\n')
print(json.dumps(dict(status=report['status'],directory=str(out),report_sha256=hashlib.sha256((out/'REPORT.json').read_bytes()).hexdigest(),source_inventory_files=len(inv['files']),next_exact_canonical_command=command,outer_whole_seconds=1800,inner_stage_seconds=600,business_executed=False),allow_nan=False))

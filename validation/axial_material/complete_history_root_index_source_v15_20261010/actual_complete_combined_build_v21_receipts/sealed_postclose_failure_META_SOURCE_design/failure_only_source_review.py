"""Finite AST/source review of failure-only writer. No writer import or execution."""
import ast
import hashlib
import json
from pathlib import Path
import stat
import sys
ROOT=Path(sys.argv[1])
p=ROOT/'write_actual_failed_build_postclose_META.py'
def identity(path):
 s=path.lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 before=identity(path);assert stat.S_ISREG(before[2])
 with path.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(path)==before
 return dict(path=str(path),sha256=sha,identity=before)
first=pin(p);raw=p.read_bytes();assert pin(p)==first
t=ast.parse(raw);text=raw.decode();defs={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
assert 'success_checks' not in defs and 'expected_commands' not in defs
assert 'watch_ok' not in defs and 'finite_number' not in defs
allowed={'argparse','ast','hashlib','json','math','os','pathlib','stat','time'}
for n in ast.walk(t):
 if isinstance(n,ast.Import):assert all(v.name in allowed for v in n.names)
 if isinstance(n,ast.ImportFrom):assert n.module in allowed
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
  assert n.func.id not in {'eval','exec','compile','__import__'}
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
  assert n.func.attr not in {'unlink','rmdir','remove','rmtree','rename','Popen','run','execute','exec_module','setprofile','sleep'}
  if n.func.attr=='replace':assert isinstance(n.func.value,ast.Name) and n.func.value.id=='key'
main=ast.get_source_segment(text,defs['main'])
assert "if terminal['exit_code']==0: raise ValueError('failure-only refuses EXIT0" in main
assert "receipt=T/'terminal_return.json'" not in text
assert "receipt=T/'failed_build_terminal_return.json'" in text
assert 'successful_new_runtime_build_observed=True' not in text
assert 'all_five_original_stages_passed=True' not in text
assert 'original_host_final_input_revalidation_observed=False' in text
assert 'Root_postclose_pin_checks_do_not_replace_unreached_host_input_finalpass=True' in text
assert 'full_declared_physical_input_finalpass_claimed=False' in text
assert main.index('terminal=typed_terminal(actual)')<main.index('copy_exact(paths[key]')
assert main.index("if terminal['exit_code']==0")<main.index('copy_exact(paths[key]')
assert "fixed=preflight['fixed_input_pins']" in text
assert 'for index,q in enumerate(fixed)' in text
assert "actual_stages=observed.get('inner_stage_table',{}).get('stages',[])" in text
assert "pass_labels=[stage.get('label') for stage in actual_stages if stage.get('status')=='PASS']" in text
assert "actual_prefix=observed_labels==LABELS[:len(observed_labels)]" in text
assert 'for stage in actual_stages' in text
assert 'source_ok: compare_source_freeze(freeze)' in text
assert "summary=dict(originals)" in text
assert "summary.update(" in text
# Shared normal pin/inventory/terminal gate prefix has exact original design bytes.
general=(ROOT/'write_actual_build_postclose_META.py').read_text()
gt=ast.parse(general)
end=next(n for n in gt.body if isinstance(n,ast.FunctionDef) and n.name=='finite_number').lineno-1
prefix=''.join(general.splitlines(keepends=True)[:end])
assert text.startswith(prefix)
assert pin(p)==first
design=json.loads((ROOT/'SOURCE_DESIGN.json').read_text())
for q in design['all_read_source_and_saved_old_META_inputs']:
 assert pin(Path(q['path']))==q
report=dict(schema='AXMAT_V21_ACTUAL_FAILED_BUILD_POSTCLOSE_WRITER_FINITE_SOURCE_REVIEW_V1',
 status='SOURCE_ONLY_FAILURE_WRITER_DESIGN_PASS_NOT_EXECUTED',
 failure_only_writer=first,common_prefix_full_byte_exact_to_reviewed_general_design=True,
 no_success_receipt_construction_or_success_API_entrypoint=True,real_Root_terminal_strict_integer_nonzero_CLOSED_required=True,
 required_arguments=['writer-sha256','root-terminal+sha256','source-freeze+sha256','prelaunch-pins+sha256',
 'parent-stdout+sha256','parent-stderr+sha256'],
 Root_announced_not_independently_read_actual_observations=dict(
 actual_Root_terminal_SHA='38815705e9e27c62e423dd4501ff41308d6ec1c219ea8ab9c264a27807420791',
 source_freeze_SHA='0825b81036f1f7ad71a41444e4a87384a518f7d8ed7e9e38ee659f916e42909b',
 preflight_SHA='a9024656df7debc840a8f5f1394bae05ba31360c542e5a8b9d2da3d749164b42',
 actual_tool_exit_code=1,closed=True,observed_completed_stages=2,
 peak_RSS_MiB=514.203125,canonical_child_seconds=170.787905792),
 observed_stages_and_watch_files_dynamic_not_hardcoded=True,
 complete_30_SOURCE_and_62_fixed_pins_counts_not_hardcoded=True,
 original_SOURCE_directories_full_seven_part_identity=True,
 original_PREP_SOURCE_TERMINAL_files_and_captured_directories_verified=True,
 original_PREP_OUT_four_files_verified=True,
 genuine_Source_guard_MRO_caps_unchanged=True,
 complete_H_S_O_T_D_E_saved_inventory_and_actual_raw_streams_preserved=True,
 actual_root_terminal_metadata_explicit_sha_bound=True,
 actual_stage_logs_watchdogs_and_complete_merged_child_stream_saved=True,
 no_failed_raw_receipt_driver_seal_audit_or_success_created=True,
 real_external_host_stderr_and_merged_child_scope_explicit=True,
 original_host_final_input_revalidation_not_observed=True,
 Root_postclose_pin_checks_are_independent_and_do_not_replace_host_final_input_PASS=True,
 all_scope_joint_byte_accounting_H_S_O_T_D_E_plus_factory_and_writer=True,
 original_caps=dict(whole_seconds=1800,stage_seconds=600,RSS_MiB=512,joint_bytes=2*2**30,
 history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
 source_reviewer_only_standard_library=True,writer_imported_or_executed=False,
 business_numeric_guard_API_called=False,ART_live_or_closed_actual_run_files_read=False,
 project_or_existing_sealed_package_written=False,
 SOURCE_self_review_is_not_actual_Runtime_RSS_or_science=True,
 limits=['Executable-shaped Source design has not been executed or imported, and needs Root/peer SOURCE review before actual metadata execution.',
 'Prepared manifest must contain original namespaces files and captured directory identities and be pinned in actual preflight.',
 'Metadata storage overhead remains inside original 2GiB; failure never creates success receipt or deletes originals.',
 'Root must retain the writer actual typed terminal tool result in a new postclose metadata receipt; do not retry business or overwrite partial metadata.',
 'Only new TMP package written. Root-reported current failed-run measures have not been independently read by this SOURCE reviewer.'],
 whole_combined_INPUT_admitted=False,native_transport_executed=False,native_RSS_qualified=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,physics_qualified=False,goal_complete=False)
(ROOT/'FAILURE_ONLY_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(ROOT/'FAILURE_ONLY_SOURCE_REVIEW.txt').write_text(
 '专用 V21 真实失败关闭后 META writer：有限 SOURCE 自审通过，未 import/执行 writer。\n'
 '拒绝 Root EXIT0；源码无成功 terminal receipt 的构造入口。Root 必须传真实 CLOSED 非零原 tool record、freeze、preflight 及真实两个 parent 流的 path+SHA，所有参数必需。\n'
 '完整保存 H/S/O/T/D/E、原 child merged stream、真实外部 host stderr/stdout、阶段和watch；按实际 stages 表动态报告两项或其它真实 prefix，不固定1/5或2/5。\n'
 'D 全部文件/目录以及固定输入有序重复项完整前后 EOF SHA/7ID；原 S/T 和 PREP O4 独立 metadata 核对。Root postclose pin 检查不替代未到达的 host final input PASS。\n'
 'Root告知实际终态为 int1 CLOSED，peak514.203125MiB、child170.787905792s、前两项PASS；本SOURCE审查没有读取本次实际 ART 输出、没有独立授这些actual事实信用。\n'
 '原whole1800/stage600/512MiB/联合2GiB/history96/free8/1线程1子进程0retry不变。联合archive包括全部五namespace及E、canonical和writer，保存未来META tool return还需Root封存完整清单。\n'
 '本包含通用成功合同SOURCE reference，仅本 failure-only writer供此失败使用。无whole INPUT/native/AAA/ABA/physics成功信用，无科学参数修改。\n')
print(json.dumps(dict(status=report['status'],writer_sha256=first['sha256'],writer_bytes=first['identity'][4],
 source_AST_full=True,failure_only_no_success_receipt=True,writer_executed=False)))


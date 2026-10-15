import ast
import hashlib
import json
from pathlib import Path
import stat
import tempfile
import time
started=time.monotonic()
base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
d=base/'actual_complete_graph_helper_controls_sources'
proof_path=d/'Root_finite_host_source_inverse.json'
proof=json.loads(proof_path.read_text())
expected={
 Path(proof['parent_path']):'95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f',
 Path(proof['host_path']):'82a17c5704766d884953148bae82a704efdbfe5325f044f3f28689662c03cef9',
 Path(proof['driver_path']):'34ba581aa89b74424c665b46907c3934011df4a0273abd9fe1e53d9fc6f220b2',
 Path(proof['helper_path']):'173fc2da988e1b102080b6c2b5448b9c732934902d5a447160559b3d27a92002',
 base/'actual_prepare_sources/prepare_cli_host_v15.py':'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7',
 Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py'):'619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743',
 Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py'):'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6',
 Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'):'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128',
 Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py'):'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09',
 Path('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'):'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022',
}
def pin(path,wanted=None):
 s=path.lstat();assert stat.S_ISREG(s.st_mode)
 ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 q=path.lstat();assert ident==[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
 assert wanted is None or digest==wanted
 return dict(path=str(path),sha256=digest,identity=ident)
pins=[pin(proof_path)]+[pin(p,s) for p,s in expected.items()]
parent=Path(proof['parent_path']).read_bytes();host=Path(proof['host_path']).read_bytes();driver=Path(proof['driver_path']).read_text()
assert len(proof['changes'])==14
forward=parent;rows=[]
for i,c in enumerate(proof['changes'],1):
 old,new=c['old'].encode(),c['new'].encode();assert forward.count(old)==c['occurrences']
 rows.append(dict(index=i,forward_occurrences=forward.count(old)));forward=forward.replace(old,new)
assert forward==host
inverse=host
for i,c in reversed(list(enumerate(proof['changes'],1))):
 old,new=c['old'].encode(),c['new'].encode();assert inverse.count(new)==c['occurrences']
 rows[i-1]['inverse_occurrences']=inverse.count(new);inverse=inverse.replace(new,old)
assert inverse==parent
assert proof['full_inverse_exact'] is True and proof['business_executed'] is False and proof['actual_success_pins'] is None
text=host.decode();tree=ast.parse(text);ast.parse(driver)
checks={
 'full14_forward_and_inverse_byte_exact':forward==host and inverse==parent,
 'fixed_host_driver_helper_sha':all(proof[k]==expected[Path(proof[p])] for k,p in [('host_sha256','host_path'),('driver_sha256','driver_path'),('helper_sha256','helper_path')]),
 'fixed_original_guard_and_exact_MRO_paths':"full,production=helper.modules();helper.guard_admission(full)" in text and "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in text and "Path(full.__file__).resolve()!=support.FULL" in text and "Path(production.__file__).resolve()!=support.PARENT" in text,
 'genuine_resource_instance_history96_free8':"resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)" in text and "runner.resources is not resources" in text,
 'new_host_out_in_full_history_roots':"roots=resource.history_roots([str(HOST),str(OUT),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)" in text,
 'whole_and_stage60_RSS512_archive64':"WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20" in text,
 'source_out_host_archive_all_twice':text.count('support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))')==2,
 'five_environment_thread_vars_and_normal_python':"any(os.environ.get(k)!='1' for k in support.THREAD_KEYS)" in text and "Path(sys.executable).resolve()!=support.PYTHON" in text,
 'one_child_zero_retry_fresh_out_host':text.count('runner.execute(')==1 and "len(runner.records)!=1" in text and "if os.path.lexists(HOST) or os.path.lexists(OUT)" in text and 'retries=0' in text,
 'no_profiling_optimization_or_supervisor_override':"sys.getprofile() is not None" in text and "sys.flags.optimize" in text and not any(isinstance(n,ast.ClassDef) for n in tree.body),
 'canonical_driver_command_only':"command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT)]" in text,
 'sha7id_full_source_input_before_after':"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]" in text and "for entry in inputs+[hpin,rpin]:" in text and "if support.pin(entry['path'],entry['sha256'])!=entry" in text,
 'watchdog_exact_integer0_command_own_child_cleanup_peak':all(x in text for x in ["type(watch['returncode']) is not int","watch['returncode']!=0","watch['command']!=command","watch['limit_failure'] is not None","watch['own_child_only'] is not True","watch['liveness_group_cleanup'] is not True","not 0<=watch['sampled_peak_rss_mib']<RSS_CAP"]),
 'driver_stdout_status_report_path_sha_matches':"print(json.dumps({\"status\": report[\"status\"], \"report\": report_pin" in driver and "Path(admission['report']['path'])!=OUT/'ACTUAL_REPORT.json'" in text and "report_pin=support.pin(OUT/'ACTUAL_REPORT.json',admission['report']['sha256'])" in text,
 'driver_report_schema_status_matches':all(x in text and x in driver for x in ['AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16','ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION']),
 'correct_original_order_compact_field_matches':"\"original_insertion_order_compact_source\": source_compact" in driver and "['original_insertion_order_compact_source']['size_bytes']!=35211756" in text and 'original_order_compact_pin' not in text,
 'correct_whole_old_graph_nested_count_matches':all(x in driver for x in ['"complete_original_metadata": original_metadata','"complete_counts": {','"read_trace_records": len(graph["read_trace"]["records"])']) and "['complete_original_metadata']['complete_counts']['read_trace_records']!=62332" in text,
 'driver_all_success_pins_after_last_checkpoint':driver.index('report["actual_success_pins"] = {')>driver.index('checkpoint("all_original_saved_metadata_bytes_identity_unchanged")'),
 'driver_original_false_science_boundary_fields':all(('"'+k+'": False') in driver and k in text for k in ['business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']),
 'host_reads_control_report_without_mutation':not any(isinstance(n,(ast.Assign,ast.AnnAssign,ast.AugAssign)) and any(isinstance(q,ast.Subscript) and isinstance(q.value,ast.Name) and q.value.id=='control_report' for t in (n.targets if isinstance(n,ast.Assign) else [n.target]) for q in ast.walk(t)) for n in ast.walk(tree)),
}
assert all(checks.values()), {k:v for k,v in checks.items() if not v}
for q in pins: assert pin(Path(q['path']),q['sha256'])==q
out=Path(tempfile.mkdtemp(prefix='axmat_v16_pure_graph_controls_host_source_review_20261010_',dir='/private/tmp'))
report=dict(schema='AXMAT_INDEPENDENT_FINITE_PURE_CONTROLS_HOST_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_NO_ACTUAL_HELPER_EXECUTION',host_sha256=proof['host_sha256'],driver_sha256=proof['driver_sha256'],helper_sha256=proof['helper_sha256'],finite_changes=14,full_source_forward_inverse_exact=True,whole_inverse_parent_sha256=hashlib.sha256(inverse).hexdigest(),occurrence_checks=rows,checks=checks,source_inputs_full_sha7id_before_after=pins,no_blocking_source_issue_found=True,actual_helper_controls_executed=False,target_module_imported=False,target_host_executed=False,target_driver_executed=False,numerical_payload_read=False,actual_success_pins=None,business_component_executed=False,fresh_runtime_INPUT_qualified=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,source_only_elapsed_seconds=time.monotonic()-started,scope_note='Only source and proof files read; target helper/host/driver never imported or executed. Guard preservation is source evidence. Runtime behavior remains for Root actual controls.',historical_note='Earlier spoken change count 15 was mistaken. First review tool EXIT1 was an overbroad audit assertion: normal report reads were misclassified as override. It was replaced by AST assignment-target check, without executing target programs.')
(out/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('最终 host 源码审查通过，无源级阻塞点。\n\n14 项有限变更正向生成 82a17c… host，逆向完整还原 95fd82… parent。driver 34ba58…、helper 173fc2… 完整核验。\n报告字段 original_insertion_order_compact_source 和 complete_original_metadata.complete_counts.read_trace_records 与 driver 一致。\n原监督程序、正常导入和真实资源对象保持；60 秒、512 MiB、HOST+OUT+SOURCE 64 MiB、历史 96 GiB、余量 8 GiB、单线程、单子进程、零重试保留。\n仅做源码读取和 AST 分析，未导入或运行 helper、host、driver，未读取数值 payload；不授予 INPUT、native RSS 或物理精度资格。\n初次审查工具因过宽审查断言 EXIT1，现改为 AST 检查赋值目标；失败返回将原样保留，不涉及业务重试。\n')
print(json.dumps(dict(status=report['status'],review_dir=str(out),report_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),finite_changes=14,checks=len(checks),target_import_or_execution=False),allow_nan=False))

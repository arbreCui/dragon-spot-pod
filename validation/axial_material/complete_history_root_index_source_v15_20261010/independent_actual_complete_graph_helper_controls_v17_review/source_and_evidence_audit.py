import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import time
started=time.monotonic()
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
A=Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_graph_helper_controls_v17_sources'
E=B/'actual_complete_graph_helper_controls_v17_receipts'
H=A/'axial-material-complete-graph-trace-table-helper-controls-host-v17-20261010'
O=A/'axial-material-complete-graph-trace-table-helper-controls-v17-20261010'
S=D/'sealed_complete_helper_and_driver_source_review'
HELPER=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
expected_helper='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
expected_driver='da4bd8438cb5007e8e7a5817ba9e198237aa93766af769898d971adf9708e68e'
expected_host='de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2'
def identity(path):
 s=Path(path).lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path,wanted=None):
 p=Path(path);before=identity(p);assert stat.S_ISREG(before[2]),str(p)
 with p.open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
 assert identity(p)==before,str(p)
 assert wanted is None or sha==wanted,(str(p),sha,wanted)
 return dict(path=str(p),sha256=sha,identity=before)
def check_record(record):
 found=pin(record['path'],record['sha256'])
 if 'identity' in record:assert found['identity']==record['identity'],record['path']
 if 'size_bytes' in record:assert found['identity'][4]==record['size_bytes']
 return found
def tree(root):
 result=[];pending=[root]
 while pending:
  path=pending.pop();ident=identity(path);mode=ident[2]
  item=dict(relative_path='.' if path==root else str(path.relative_to(root)),identity=ident)
  if stat.S_ISDIR(mode):
   item['kind']='directory';names=sorted(os.listdir(path));item['children']=names
   assert identity(path)==ident
   pending.extend(path/name for name in reversed(names))
  elif stat.S_ISREG(mode):item.update(kind='file',sha256=pin(path)['sha256'])
  elif stat.S_ISLNK(mode):
   item.update(kind='symlink',target=os.readlink(path));item['link_text_sha256']=hashlib.sha256(os.fsencode(item['target'])).hexdigest();assert identity(path)==ident
  else:raise AssertionError('unsupported namespace member '+str(path))
  result.append(item)
 return result
def read(p):return json.loads(Path(p).read_text())
inventories={str(p):tree(p) for p in (H,D,O,E)}
host=read(H/'result.json');report=read(O/'ACTUAL_REPORT.json');watch=read(H/'run/admit.watchdog.json')
initial=read(E/'Root_actual_initial_tool_return.json');terminal=read(E/'Root_actual_tool_terminal_return.json')
assert initial['actual_initial_tool_return']==terminal['actual_initial_tool_return']
assert terminal['actual_initial_tool_return']['chunk_id']=='d1734f' and terminal['actual_initial_tool_return']['session_id']==59994
actual=terminal['actual_terminal_tool_return'];assert actual['chunk_id']=='e2794c' and type(actual['exit_code']) is int and actual['exit_code']==0 and 'session_id' not in actual
assert terminal['terminal_return_observed'] is True and terminal['session_closed'] is True and terminal['retries']==0
assert initial['actual_initial_command']==terminal['actual_initial_command']
assert all(x in terminal['actual_initial_command']['cmd'] for x in ['env -u PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',str(D/'pure_helper_controls_host.py')])
parent_stdout=read(E/'parent_stdout.log');child_stdout=read(H/'run/admit.log')
assert (E/'parent_stderr.log').stat().st_size==0
assert parent_stdout['status']==host['status'] and parent_stdout['actual_external_Root_terminal_required'] is True
source_pins=[]
for q in host['input_sources']+[host['original_helper'],host['resource_factory']]:source_pins.append(check_record(q))
for q in [parent_stdout['actual_host_result'],parent_stdout['actual_admission_stdout'],host['actual_control_report'],host['actual_admission_stdout'],host['actual_watchdog'],child_stdout['report']]:check_record(q)
assert parent_stdout['actual_host_result']['path']==str(H/'result.json')
assert child_stdout['report']['path']==str(O/'ACTUAL_REPORT.json')
assert child_stdout['status']==report['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'
assert report['schema']=='AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16'
check_record(report['helper']);assert report['helper']['sha256']==expected_helper
check_record(report['actual_success_pins']['helper'])
for q in report['saved_input_identity_before']+report['saved_input_bytes_identity_after']:check_record(q)
assert report['saved_input_identity_before']==report['saved_input_bytes_identity_after']
assert len(report['saved_input_identity_before'])==2
assert report['saved_input_identity_before'][0]['sha256']=='4ba5f793ca13018d2d9ac5d29d76827a1503b0368c7e5c9f70ba08e0435f0c9e'
assert report['saved_input_identity_before'][1]['sha256']=='e0a9fc9254bf0b5717498b489d5e1f2e4dbe09ac5fc80983c27af4fefbc92fa0'
trace=report['full_new_creation_trace'];graph=report['full_old_saved_graph']
assert trace['full_record_count']==trace['table_rows']==63379 and trace['subprocess_record_count']==0
assert trace['original_insertion_order_compact_source']==dict(size_bytes=35211756,sha256='3edb2c73250782d107202deaab6192beec269619fe76a39a6e3b645f79e6b422')
assert all(trace[k] is True for k in ['default_source_nonmutation','exact_full_roundtrip','persisted_full_trace_exact_order_type_floatbit_inverse'])
for q in [trace['encoded_artifact'],graph['stored_wholegraph'],report['actual_success_pins']['encoded_new_trace'],report['actual_success_pins']['encoded_wholegraph']]:check_record(q)
assert trace['encoded_artifact']['size_bytes']==8488204 and graph['stored_wholegraph']['size_bytes']==45300566
assert trace['stored_complete_descriptor']['sha256']==trace['encoded_artifact']['sha256']
assert graph['complete_original_metadata']==graph['normal_strict_file_entrance_full_semantics_and_counts']==graph['normal_strict_payload_entrance_full_semantics_and_counts']
counts=graph['complete_original_metadata']['complete_counts']
assert (counts['read_trace_records'],counts['requirements'],counts['canonical_files'])==(62332,237767,36776)
assert sum(counts['category_requirement_rows'].values())==sum(counts['role_requirement_rows'].values())==237767
assert all(graph[k] is True for k in ['full_default_roundtrip_exact','original_legacy_semantic_sha_preserved','no_two_complete_decoded_graphs_between_strict_stages','old_read_trace_not_replaced_by_new_trace'])
accepted=report['small_fixture']['accepted_str_subclass_equivalence_controls']
assert len(accepted)==2 and {q['case'] for q in accepted}=={'plain_accepted_str','accepted_str_with_str_override'}
for case in accepted:
 assert case['complete_builtin_output_values_types_order_floatbits_equal'] is True and case['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True
 old=O/('accepted_subclass_'+case['case']+'_original_wire_graph.json');new=O/('accepted_subclass_'+case['case']+'_fresh_wire_graph.json')
 assert old.read_bytes()==new.read_bytes()
 assert pin(old)['sha256']==case['producer_canonical_pin']['sha256'] and old.stat().st_size==case['producer_canonical_pin']['size_bytes']
assert report['small_fixture']['caller_full_value_and_mutable_identity_preserved'] is True
assert (O/'small_fixture_original_wire_graph.json').read_bytes()==(O/'small_fixture_fresh_wire_graph.json').read_bytes()
assert len(report['stages'])==5
assert [q['stage'] for q in report['stages']]==['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged']
assert all(q['elapsed_seconds']<60 and q['peak_rss_bytes']<=512*2**20 for q in report['stages'])
assert all(report[k] is False for k in ['business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted'])
assert all(host[k] is False for k in ['profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'])
argv=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'pure_helper_controls.py'),'--output-dir',str(O)]
assert host['actual_canonical_command']==watch['command']==argv
assert len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['command']==argv
assert read(H/'GRAPH_PROTOCOL_CONTROLS/stages.json')=={'stages':host['stage_records']}
assert type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=host['stage_records'][0]['wall_cap_seconds']<=60
assert 0<=watch['sampled_peak_rss_mib']<512 and watch['rss_cap_mib']==512
assert (host['whole_wall_cap_seconds'],host['stage_wall_cap_seconds'],host['rss_cap_mib'],host['archive_cap_bytes'],host['threads'],host['children_at_once'],host['retries'])==(60,60,512,67108864,1,1,0)
assert host['whole_seconds']<60 and report['elapsed_seconds']<60 and report['peak_rss_bytes']<=512*2**20
for k in ['resources_before','resources_after']:
 r=host[k];assert r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30
 assert r['artifact_bytes']<96*2**30 and r['disk_free_bytes']>=8*2**30 and r['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
 assert str(H) in r['resource_roots'] and str(O) in r['resource_roots']
 rcontract=r['resource_scope_contract'];assert rcontract['artifact_budget_GiB']==96 and rcontract['min_free_GiB']==8 and rcontract['all_declared_extras_retained'] is True
before=host['resources_before'];assert before['artifact_bytes']+64*2**20<96*2**30 and before['disk_free_bytes']-64*2**20>=8*2**30
archive=sum(q['identity'][4] for p in (H,D,O) for q in inventories[str(p)] if q['kind']=='file')
assert archive<64*2**20 and archive-host['archive_before_result_bytes']==(H/'result.json').stat().st_size
source_paths={q['path'] for q in host['input_sources'] if Path(q['path']).is_relative_to(D)}
assert source_paths=={str(D/q['relative_path']) for q in inventories[str(D)] if q['kind']=='file'}
host_source=(D/'pure_helper_controls_host.py').read_bytes();driver_source=(D/'pure_helper_controls.py').read_bytes()
assert pin(D/'pure_helper_controls_host.py',expected_host) and pin(D/'pure_helper_controls.py',expected_driver) and pin(HELPER,expected_helper)
proof=read(D/'Root_finite_source_binding_and_host_inverse.json');assert len(proof['finite_changes'])==9
parent_path=Path(proof['parent_host_path']);parent=parent_path.read_bytes();assert pin(parent_path,proof['parent_host_sha256'])
def inverse_bytes(child,changes):
 inverse=child
 for c in reversed(changes):
  old,new=c['old'].encode(),c['new'].encode();assert inverse.count(new)==c['occurrences'];inverse=inverse.replace(new,old)
 return inverse
assert inverse_bytes(host_source,proof['finite_changes'])==parent
oldproof=proof['original95_parent_proof'];assert len(oldproof['changes'])==14
assert inverse_bytes(parent,oldproof['changes'])==Path(oldproof['parent_path']).read_bytes()
assert pin(oldproof['parent_path'],oldproof['parent_sha256'])
helper_proof=read(S/'COMPLETE_HELPER_AND_DRIVER_SOURCE_INVERSE_PROOF.json')
new_helper=HELPER.read_bytes();restored=new_helper
for reg in reversed(helper_proof['helper_inverse_regions']):
 if 'old_source' in reg:
  old=(S/Path(reg['old_source']['path']).name).read_bytes();new=(S/Path(reg['new_source']['path']).name).read_bytes()
 elif 'added_source' in reg:old=b'';new=(S/Path(reg['added_source']['path']).name).read_bytes()
 else:old,new=reg['old'].encode(),reg['new'].encode()
 assert restored.count(new)==1;restored=restored.replace(new,old)
assert hashlib.sha256(restored).hexdigest()=='173fc2da988e1b102080b6c2b5448b9c732934902d5a447160559b3d27a92002'
delta=read(S/'DRIVER_SOURCE_DELTA.json');restored_driver=driver_source
newcontrol=(S/Path(delta['new_function_source']).name).read_bytes();assert restored_driver.count(newcontrol)==1;restored_driver=restored_driver.replace(newcontrol,b'')
for k in ['root_report_field','inserted_result_field','inserted_call']:
 c=delta[k];old,new=c['old'].encode(),c['new'].encode();assert restored_driver.count(new)==1;restored_driver=restored_driver.replace(new,old)
for old,new in reversed(delta['replacements']):assert restored_driver.count(new.encode())==1;restored_driver=restored_driver.replace(new.encode(),old.encode())
assert hashlib.sha256(restored_driver).hexdigest()=='34ba581aa89b74424c665b46907c3934011df4a0273abd9fe1e53d9fc6f220b2'
manifest=read(S/'MANIFEST.json')
for q in manifest['files']:assert pin(S/Path(q['path']).name,q['sha256'])['identity'][4]==q['size_bytes']
assert {q['relative_path'] for q in inventories[str(D)] if q['kind']=='file' and q['relative_path'].startswith('sealed_complete_helper_and_driver_source_review/')}=={'sealed_complete_helper_and_driver_source_review/'+Path(q['path']).name for q in manifest['files']}|{'sealed_complete_helper_and_driver_source_review/MANIFEST.json'}
ht=host_source.decode();dt=driver_source.decode();ast.parse(ht);ast.parse(dt);ast.parse(new_helper.decode())
source_assertions={
 'original_guard_and_MRO':"full,production=helper.modules();helper.guard_admission(full)" in ht and "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in ht,
 'real_resource_bound':"resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)" in ht and "runner.resources is not resources" in ht,
 'full_archive_scope_twice':ht.count('support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))')==2,
 'full_graph_roundtrip_exact':"exact_value(graph, restored, \"all_full_saved_graph_values_types_order_floatbits\")" in dt,
 'both_strict_entrances_full_metadata':"exact_value(original_metadata, strict_metadata, \"full_graph_normal_strict_file_metadata\")" in dt and "exact_value(original_metadata, strict_payload_metadata, \"full_graph_normal_strict_payload_metadata\")" in dt,
 'full_trace_roundtrip_and_order_types_bits':"exact_value(trace[\"records\"], restored, \"all_63379_creation_trace_records\")" in dt and "order_type_pin(fresh_trace) == before" in dt,
 'all_accepted_subtype_output_and_caller':"exact_value(original, fresh, name + \"/complete_values_types_order_floatbits\")" in dt and "exact_value(before, caller_integrity_snapshot(arguments), name + \"/caller_after_original\")" in dt and "exact_value(before, caller_integrity_snapshot(arguments), name + \"/caller_after_fresh\")" in dt,
 'source_science_qualifications_never_set_true':all(('"'+k+'": False') in dt for k in ['business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted']),
 'report_pins_only_after_all_stages':dt.index('report["actual_success_pins"] = {')>dt.index('checkpoint("all_original_saved_metadata_bytes_identity_unchanged")'),
}
assert all(source_assertions.values()),source_assertions
full_path=Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py');full_text=full_path.read_text()
assert pin(full_path,'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6')
guard_dir=A/'axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard';guard=read(guard_dir/'guard_controls.json')
guard_pins=[pin(guard_dir/'guard_controls.json','ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454'),pin(guard_dir/'tested_driver_source.py',guard['source_sha256'])]
for name,digest in guard['control_files'].items():guard_pins.append(pin(guard_dir/name,digest))
def cls(t):return next(ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
assert cls(full_text)==cls((guard_dir/'tested_driver_source.py').read_text())
assert guard['positive_child_completed'] is True and guard['actual_oversize_child_rejected'] is True and guard['terminated_own_child_not_live'] is True and guard['rss_cap_mib']==512
assert pin(H/'runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
for p,found in inventories.items():assert tree(Path(p))==found,p
for q in source_pins+guard_pins:assert check_record(q)==q
out=Path(tempfile.mkdtemp(prefix='axmat_v17_actual_pure_graph_controls_evidence_review_20261010_',dir='/private/tmp'))
summary=dict(schema='AXMAT_INDEPENDENT_V17_ACTUAL_PURE_HELPER_CONTROLS_EVIDENCE_REVIEW_V1',status='PASS_ACTUAL_PURE_HELPER_CONTROLS_EVIDENCE_ONLY',no_blocking_issue_found=True,terminal_initial_chunk='d1734f',terminal_final_chunk='e2794c',actual_parent_exit_code=0,session_closed=True,retries=0,helper_sha256=expected_helper,driver_sha256=expected_driver,host_sha256=expected_host,source_host_inverse_deltas=[9,14],whole_source_inverse_exact=True,full_helper_and_driver_finite_inverses_exact=True,source_assertions=source_assertions,complete_original_counts=counts,new_creation_trace_records=63379,new_creation_trace_attempts=trace['actual_attempt_count'],accepted_subtype_cases=[q['case'] for q in accepted],checkpoint_count=5,whole_seconds=host['whole_seconds'],child_seconds=watch['elapsed_seconds'],sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],self_ru_maxrss_bytes=report['peak_rss_bytes'],archive_before_result_bytes=host['archive_before_result_bytes'],fresh_complete_archive_bytes=archive,archive_cap_bytes=64*2**20,archive_scope=[str(H),str(D),str(O)],wholegraph_encoded_bytes=45300566,new_trace_encoded_bytes=8488204,all_original_saved_input_bytes_and7id_unchanged=True,all_current_host_source_output_namespace_entries_fresh_verified=True,full_sha_and7id_host_input_pin_count=len(source_pins),guard_full_source_class_and_control_pin_count=len(guard_pins),source_inputs=source_pins,guard_pins=guard_pins,namespace_inventories=inventories,reviewer_imported_or_executed_helper_or_business=False,reviewer_numeric_payload_read=False,actual_business_component_executed=False,fresh_v17_production_graph_created=False,fresh_runtime_INPUT_qualified=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,actual_success_pins_scope='Pure helper controls and retained original metadata codec artifacts only; not fresh production graph or physics',elapsed_readonly_review_seconds=time.monotonic()-started)
(out/'REVIEW.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('V17 实际纯元数据控制证据审查通过，无阻塞。\n\nRoot 实际 d1734f / session 59994 → e2794c 整数 EXIT0、会话关闭、零重试。5 个完整 checkpoint，两种字符串子类型的全部输出及 caller 完整性，63379 条新 trace、旧图 62332 条 trace / 237767 条 requirements / 36776 个 canonical files，默认完整逆变换与两种 strict 入口均有实际断言和结果一致证据。\n旧图实际压缩存储 45300566 字节、新 trace 8488204 字节，两者均保存；没有用新 trace 替换旧图 trace。\n实际 whole 16.507847333 秒、子进程 15.391886208 秒、峰值 392.140625 MiB；完整 HOST+SOURCE+OUT '+str(archive)+' 字节，低于原 64 MiB。60 秒、512 MiB、历史 96 GiB / 余量 8 GiB、单线程、单子进程、零重试保持。\n独立审查完整重新读取并核验 namespace 所有普通文件的 SHA 和 7 项身份、目录、符号链接与前后不变；所有 host 输入 pin、原 2 个固定 metadata、实际输出 pin 均匹配。9 + 14 个有限 host delta 精确还原原 host；helper / driver 有限源码还原和原 guard class / 控制文件一致。\n这只准入纯 helper 控制证据；没有生成或准入新 production graph、完整 INPUT、native RSS、AAA 精度或 ABA。审查器未导入或运行 helper / business。\n')
print(json.dumps(dict(status=summary['status'],directory=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),archive_bytes=archive,namespace_file_counts={Path(p).name:sum(q['kind']=='file' for q in found) for p,found in inventories.items()},source_pins=len(source_pins),blocked=False),allow_nan=False))

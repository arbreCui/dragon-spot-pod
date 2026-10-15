import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v17-20261010')
h=json.loads((H/'result.json').read_text())
O=Path(h['actual_declaration']['path']).parent;S=Path(h['actual_source_admission']['path']).parent
D=B/'actual_complete_combined_prepare_v17_sources'
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,wanted=None):
 p=Path(p);before=ident(p);assert stat.S_ISREG(before[2])
 with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==before and (wanted is None or sha==wanted)
 return dict(path=str(p),sha256=sha,identity=before)
def check(q):
 p=pin(q['path'],q['sha256']);assert p['identity']==q['identity'];return p
def inventory(root):
 members=[]
 for parent,dirs,files in os.walk(root,followlinks=False):
  p=Path(parent);members.append(dict(path=str(p),kind='directory',identity=ident(p),children=sorted(dirs+files)))
  for name in dirs+files:
   q=p/name;mode=q.lstat().st_mode
   if stat.S_ISLNK(mode):members.append(dict(path=str(q),kind='symlink',identity=ident(q),target=os.readlink(q)))
   elif name in files:members.append(dict(kind='file',**pin(q)))
 return sorted(members,key=lambda q:q['path'])
ns={str(p):inventory(p) for p in (H,S,O,D)}
inputs=[check(q) for q in h['input_sources']+[h['original_helper'],h['resource_factory']]]
outputs=[check(h[k]) for k in ('actual_prepare_stdout','actual_declaration','actual_source_admission','actual_watchdog')]
d=json.loads(Path(h['actual_declaration']['path']).read_text());s=json.loads(Path(h['actual_source_admission']['path']).read_text());w=h['watchdog']
assert (h['whole_wall_cap_seconds'],h['stage_wall_cap_seconds'],h['rss_cap_mib'],h['archive_cap_bytes'],h['threads'],h['children_at_once'],h['retries'])==(1800,600,512,2*2**30,1,1,0)
assert (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'],d['threads'],d['numeric_children_at_once'],d['retries'])==(1800,600,512,2*2**30,1,1,0)
assert type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True
assert w['command']==h['actual_canonical_command'] and len(h['stage_records'])==1 and h['stage_records'][0]['status']=='PASS'
assert w['elapsed_seconds']<w['wall_cap_seconds']<=600 and w['sampled_peak_rss_mib']<512 and h['whole_seconds']<1800
assert all(h[k] is False for k in ('profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert len(d['stages'])==5 and all(d[k] is False for k in ('mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))
assert d['trim_component_API_executed_in_this_PREP'] is True and d['original_component_APIs_executed_now'] is False and d['historical_failed_combined_RUN_promoted'] is False
assert d['input_graph_source_root_inventory_is_exhaustive'] is True
for k in ('resources_before','resources_after'):
 r=h[k];assert r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30 and r['artifact_bytes']<96*2**30 and r['disk_free_bytes']>=8*2**30
p=pin(d['input_graph']['path'],d['input_graph']['sha256']);assert p['identity'][4]==45519289 and p['identity'][4]<64*2**20
encoded=json.loads(Path(p['path']).read_text());g=encoded['graph']
assert encoded['schema']=='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1'
assert g['science_qualification_created'] is False and g['consumer_scope'] is None and g['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
assert g['external_declaration_exit0_verified'] is False and g['live_resources_verified'] is False
assert g['content_sha256']==d['input_graph']['content_sha256']
counts=dict(canonical_files=len(g['canonical_files']['rows']),requirements=g['requirements']['rows']['row_count'],owners=len(g['owners']['rows']),namespaces=len(g['namespaces']),aliases=len(g['aliases']),trace_records=g['read_trace']['records']['row_count'],coverage_categories=len(g['coverage']),all_original_closure_categories=g['closure_categories'],newly_declared_paths=len(g['newly_declared_input_paths']),absence_inputs=len(g['absence_inputs']))
assert counts['coverage_categories']==9 and counts['namespaces']==86
contract=g['fresh_reader_contract'];assert contract['canonical_union_fresh_bytes_required_every_phase'] is True and contract['no_input_scope_or_typed_edge_filtering'] is True and contract['no_persistent_hash_or_stat_cache'] is True and contract['original_requirement_and_owner_tables_lossless_and_unchanged'] is True
historic=g['typed_snapshot']['historical_whole_component_body'];assert d['historical_whole_component_body']['whole_seven_key_body_retained'] is True
assert d['historical_whole_component_body']['original_component_API_execution_claimed'] is False
assert d['historical_whole_component_body']['historical_FAILED_RUN_promoted'] is False
trace_coverage=dict(g['trace_coverage']);del encoded,g
creation_path=O/'input_creation_python_open_trace.json';creation_pin=pin(creation_path);creation=json.loads(creation_path.read_text())
creation_count=len(creation['records']);assert creation_count==counts['trace_records'];del creation
archive=sum(q['identity'][4] for p in (H,S,O,D) for q in ns[str(p)] if q['kind']=='file')
assert archive<2*2**30
for path,entries in ns.items():assert inventory(Path(path))==entries
for q in inputs+outputs+[p,creation_pin]:assert check(q)==q
out=Path(tempfile.mkdtemp(prefix='axmat_v17_combined_prepare_status_readonly_review_20261010_',dir='/private/tmp'))
report=dict(schema='INDEPENDENT_V17_COMPLETE_COMBINED_PREPARE_STATUS_READONLY_REVIEW_V1',status='PASS_PREPARE_INTERNAL_EXECUTION_AND_SAVED_METADATA_ONLY',host_result=pin(H/'result.json'),whole_seconds=h['whole_seconds'],child_seconds=w['elapsed_seconds'],peak_rss_mib=w['sampled_peak_rss_mib'],rss_margin_mib=512-w['sampled_peak_rss_mib'],whole_cap_seconds=1800,stage_cap_seconds=600,rss_cap_mib=512,archive_cap_bytes=2*2**30,archive_before_host_result_bytes=h['archive_before_result_bytes'],fresh_H_SOURCE_OUT_host_sources_archive_bytes=archive,graph_pin=p,declaration_pin=outputs[1],creation_trace_pin=creation_pin,complete_graph_counts=counts,creation_trace_record_count=creation_count,trace_coverage_counts=trace_coverage,host_original_input_full_sha7id_unchanged_count=len(inputs),host_inputs=inputs,outputs=outputs,namespace_inventories=ns,whole_INPUT_fresh_canonical_closure_review_performed=False,complete_metadata_observed=True,all_nine_original_closure_categories_retained=True,whole_seven_key_historical_body_retained=True,original_input_scope_or_threshold_relaxed=False,external_terminal_status='Root reports be9445/session70791 → e1b00f typed integer EXIT0 and closed; this reviewer did not poll or attest the absent external terminal record',source_prepare_only=True,original_five_build_stages_executed=False,whole_INPUT_admitted=False,new_native_transport_executed=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,anomalies=[],material_limit='RSS margin is only 9.828125 MiB; successful Python prepare does not prove subsequent native peak or five-stage build.',reviewer_executed_business_or_helper=False,reviewer_numeric_payload_read=False)
(out/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('V17 combined prepare 内部执行成功，原限制保持。\nwhole '+str(h['whole_seconds'])+' 秒，child '+str(w['elapsed_seconds'])+' 秒，峰值 '+str(w['sampled_peak_rss_mib'])+' MiB，距 512 MiB 仅 '+str(512-w['sampled_peak_rss_mib'])+' MiB。\n完整图 45519289 字节、声明 8613243 字节、creation trace '+str(creation_pin['identity'][4])+' 字节。完整九类闭包、86 个 namespace、historical 七项组件信息和完整 trace 保留；'+str(len(inputs))+' 个 host 原输入全 SHA / 7 项身份前后不变。\n图计数：'+json.dumps(counts,ensure_ascii=False)+'\nRoot 已报告外部 be9445 / session 70791 → e1b00f 整数 EXIT0 会话关闭；本审查未轮询，也不独立代替外部实际终态凭证。\n尚未执行五阶段构建、whole INPUT 或新 native，AAA / ABA 尚无新增成功信用。\n')
print(json.dumps(dict(status=report['status'],directory=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),complete_graph_counts=counts,archive_bytes=archive,host_original_inputs=len(inputs),anomalies=[]),allow_nan=False))

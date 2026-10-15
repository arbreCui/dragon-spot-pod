import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010');A=Path('/Users/wen/spot/validation/artifacts')
H=A/'axial-material-complete-combined-build-host-v17-20261010';S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010';O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010';T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010';D=B/'actual_complete_combined_build_v17_sources';E=B/'actual_complete_combined_build_v17_receipts'
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,wanted=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])
 with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==before and (wanted is None or sha==wanted)
 return dict(path=str(p),sha256=sha,identity=before)
def inventory(root):
 rows=[];pending=[root]
 while pending:
  p=pending.pop();ident=identity(p);mode=ident[2];row=dict(path=str(p),identity=ident)
  if stat.S_ISDIR(mode):
   row['kind']='directory';names=sorted(os.listdir(p));row['children']=names;assert identity(p)==ident;pending.extend(p/n for n in reversed(names))
  elif stat.S_ISREG(mode):row.update(kind='file',sha256=pin(p)['sha256'])
  elif stat.S_ISLNK(mode):row.update(kind='symlink',target=os.readlink(p));assert identity(p)==ident
  else:raise AssertionError('unexpected namespace kind')
  rows.append(row)
 return rows
def read(p):return json.loads(Path(p).read_text())
namespaces={str(p):inventory(p) for p in (H,S,O,T,D)}
failed=read(H/'failed_host_result.json');watch=read(H/'run/build.watchdog.json')
assert failed['status']=='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY' and failed['error']=="RuntimeError('own-child 512 MiB RSS cap reached')"
assert type(watch['returncode']) is int and watch['returncode']==-15 and watch['sampled_peak_rss_mib']==515.078125 and watch['rss_cap_mib']==512
assert watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')" and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=1800
assert watch['command'][2]=='run-build' and len(failed['stage_records'])==1 and failed['stage_records'][0]['status']!='PASS'
family='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V17';stages=read(O/family/'stages.json')['stages']
assert len(stages)==2 and [q['label'] for q in stages]==['build/link','metadata/objects'] and all(q['status']=='PASS' for q in stages)
inner=[]
for q in stages:
 log=O/(q['label']+'.log');w=read(log.with_suffix('.watchdog.json'))
 assert w['command']==q['command'] and type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True
 assert w['rss_cap_mib']==512 and w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=q['wall_cap_seconds']<=600
 assert pin(log,q['log_sha256']);inner.append(dict(label=q['label'],watchdog=w,log=pin(log)))
missing=['driver_result.json','seal.json','audit/result.json','audit/binary_identity.json','raw_metadata_receipt.json','metadata/executable.log','metadata/dependencies.log']
assert all(not os.path.lexists(O/name) for name in missing)
prepare=read(A/'axial-material-complete-combined-prepare-host-v17-20261010/result.json');pins=[]
for q in prepare['input_sources']+[prepare['original_helper'],prepare['resource_factory']]:
 found=pin(q['path'],q['sha256']);assert found['identity']==q['identity'];pins.append(found)
assert len(pins)==17
summary=read(B/'actual_complete_combined_prepare_v17_receipts/Root_actual_complete_combined_prepare_summary.json')
immutable=[]
for name in ('actual_declaration','actual_complete_input_graph','actual_complete_creation_trace'):
 q=summary[name];found=pin(q['path'],q['sha256']);assert found['identity']==q['identity'];immutable.append(found)
pin(T/'declaration_terminal_return.json','c743c01c3f40ac32e06a4f3371c82dfa4b84314b0c85509aa1710216afe569b2')
pin(D/'combined_build_host.py','cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9')
d=read(O/'declaration.json');assert (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'],d['threads'],d['numeric_children_at_once'],d['retries'])==(1800,600,512,2*2**30,1,1,0)
files={str(Path(q['path']).relative_to(S)):q['sha256'] for q in namespaces[str(S)] if q['kind']=='file'};dirs=sorted(str(Path(q['path']).relative_to(S)) for q in namespaces[str(S)] if q['kind']=='directory' and Path(q['path'])!=S)
assert dict(files=files,symlinks={},directories=dirs)==d['source_inventory']
assert all(d[k] is False for k in ('native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))
archive=sum(q['identity'][4] for rows in namespaces.values() for q in rows if q['kind']=='file');assert archive<2*2**30
terminal_record=None
for name in ('Root_actual_build_tool_terminal_return.json','Root_actual_tool_terminal_return.json','Root_actual_run_tool_terminal_return.json'):
 if (E/name).exists():terminal_record=dict(path=str(E/name),sha256=pin(E/name)['sha256'],body=read(E/name));break
for p,rows in namespaces.items():assert inventory(Path(p))==rows
for q in pins+immutable:assert pin(q['path'],q['sha256'])==q
out=Path(tempfile.mkdtemp(prefix='axmat_v17_failed_partial_build_actual_evidence_freeze_review_20261010_',dir='/private/tmp'))
report=dict(schema='INDEPENDENT_FINITE_V17_FAILED_PARTIAL_BUILD_ACTUAL_EVIDENCE_FREEZE_REVIEW_V1',status='PASS_FAILED_NAMESPACE_EVIDENCE_REVIEW_NOT_BUILD_PASS',actual_outcome='FAILED_ORIGINAL_512_MIB_CAP',Root_reported_external_initial_chunk='fa8f3b',Root_reported_external_session=72256,Root_reported_external_terminal_chunk='d03f21',Root_reported_external_integer_exit_code=1,Root_reported_external_session_closed=True,independently_found_root_terminal_record=terminal_record,outer_child_returncode=-15,outer_controller_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],cap_mib=512,elapsed_seconds=watch['elapsed_seconds'],own_child_only=True,liveness_group_cleanup=True,retries=0,inner_partial_pass_stage_count=2,inner_partial_pass_stages=inner,missing_completion_files=missing,inner_third_stage_not_started=True,precise_terminating_source_location_not_observed=True,caps=dict(whole1800=True,inner600=True,rss512=True,archive2GiB=True,history96GiB=True,free8GiB=True,threads=1,numeric_children=1,retries=0),archive_full_H_SOURCE_OUT_TERMINAL_buildSOURCE_bytes=archive,all_five_namespaces_fresh_complete_SHA7ID_and_dirs_links_frozen=True,prepare_original_17_source_pins_unchanged=True,original_17_source_pins=pins,immutable_prepare_graph_declaration_trace_unchanged=immutable,namespace_inventories=namespaces,SOURCE_inventory_equals_immutable_declaration=True,complete_five_stage_build_pass=False,whole_INPUT_admitted=False,new_native_transport_executed=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,no_previous_PREP_component_native_credit_transferred=True,reviewer_imported_or_executed_business_helper_or_numeric=False,reviewer_numeric_payload_read=False,source_memory_observation_only='Full decoded graph plus before/after/verified/path sets and temporary failed_prepare_input descriptors overlap in complete_input_phase. Last-use release is source-only suggestion, not measured causal attribution; all full fresh hash/trace/length/negative predicates must stay.')
(out/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('V17 完整五阶段构建失败，证据有限审查通过，不能记作 build PASS。\nOuter canonical Python controller 原512 MiB上限触发：峰值515.078125 MiB，child -15，耗时'+str(watch['elapsed_seconds'])+'秒，cleanup true；Root已报告 fa8f3b / session72256 → d03f21 整数EXIT1 CLOSED。\n仅 build/link 与 metadata/objects 两个inner stage真实PASS；第三stage未启动，无driver_result、seal、audit、raw closeout。\nH/SOURCE/OUT/TERM/buildSource 全部普通文件完整SHA/7项身份、目录与链接前后冻结；17个原prepare source输入及原完整图/声明/trace保持。完整归档'+str(archive)+'字节<原2GiB。\n该失败不授予完整build、whole INPUT、native、AAA或ABA资格，也不继承PREP或组件RSS信用。下一步只修必要last-use lifetimes、保留全部原fresh验证与阈值，再用新namespace执行；本轮不运行、不profiling、不读numeric。\n')
print(json.dumps(dict(status=report['status'],directory=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),archive_bytes=archive,source_pins=len(pins),inner_partial_pass=2,peak_mib=watch['sampled_peak_rss_mib'],elapsed_seconds=watch['elapsed_seconds'],independent_terminal_record_found=terminal_record is not None),allow_nan=False))

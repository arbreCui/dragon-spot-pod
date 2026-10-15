import pathlib,json,hashlib,stat,ast,gzip,math,struct,tempfile
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_graph_fresh_verifier_v21b_receipts'
D=B/'actual_complete_graph_fresh_verifier_v21b_sources'
H=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21b-20261010')
O=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21b-20261010')
P=pathlib.Path(tempfile.mkdtemp(prefix='axmat_v21b_actual_complete_fresh_verifier_saved_META_independent_review_20261010_',dir='/private/tmp'))
def ident(p):
 s=pathlib.Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);before=ident(p)
 assert stat.S_ISREG(before[2]) and before[3]==1,('ordinary unique regular',str(p))
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for block in iter(lambda:stream.read(2**20),b''):h.update(block)
 assert ident(p)==before,('changed during full EOF hash',str(p))
 return dict(path=str(p),sha256=h.hexdigest(),identity=before)
inputs={}
def verify(r):
 q=pin(r['path']);assert q['sha256']==r['sha256'] and q['identity']==r['identity'],('SHA/7ID mismatch',q['path'])
 if q['path'] in inputs:assert q==inputs[q['path']]
 inputs[q['path']]=q
 if 'size_bytes' in r:assert type(r['size_bytes']) is int and r['size_bytes']==q['identity'][4]
 return q
def pairs(items):
 result={}
 for k,v in items:
  assert k not in result,('duplicate JSON key',k)
  result[k]=v
 return result
def nonfinite(s):raise ValueError('nonfinite JSON constant '+s)
def parse(data):return json.loads(data,object_pairs_hook=pairs,parse_constant=nonfinite)
def saved(name,sha=None):
 p=E/name;q=pin(p)
 if sha:assert q['sha256']==sha,(name,q['sha256'])
 inputs[q['path']]=q;return parse(p.read_bytes())
summary=saved('Root_actual_v21b_full_fresh_verifier_summary.json','0b6d8a5038e81d0e0cc74c30fafdbb7377d19afa108b4daa471b10c21feda733')
manifest=saved('Root_actual_v21b_full_fresh_verifier_finite_saved_manifest.json','7581548c30f8d8121ca264e00871ae6390c227e6013420ffe65dc8a2e9a24fb6')
pre=saved('Root_actual_v21b_fresh_verifier_prelaunch_META.json')
files=manifest['complete_regular_files']
assert len(files)==58 and len({r['path'] for r in files})==58
assert manifest['symlinks']==[] and manifest['joint_cap_bytes']==64*2**20
assert sum(r['identity'][4] for r in files)==manifest['joint_regular_bytes_before_manifest']==1880170
assert manifest['helper_total_qualification'] is None and manifest['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False
assert manifest['mutable_receipts_root']==str(E) and manifest['receipts_root_self_and_later_append_directory7ID_not_claimed_unchanged'] is True
for r in files:verify(r)
verify(manifest['summary'])
dirs=[]
for r in manifest['directory_identities_before_manifest']:
 cur=ident(r['path']);assert stat.S_ISDIR(cur[2])
 if r['full7identity_stable_required'] is True:
  assert cur==r['identity'],('immutable saved directory changed',r['path'])
  dirs.append(dict(path=r['path'],full7ID_equal=True,identity=cur))
 else:
  assert r['path']==str(E) and cur[:3]==r['identity'][:3]
  dirs.append(dict(path=r['path'],full7ID_equal=cur==r['identity'],premanifest_snapshot=r['identity'],current=cur,exception='E root includes manifest and later Root metadata; full seven identity stability not required or claimed'))
assert len(pre['complete_frozen_SOURCE_files'])==pre['SOURCE_count']==33
assert set(r['path'] for r in pre['complete_frozen_SOURCE_files'])==set(r['path'] for r in files if pathlib.Path(r['path']).parent==D)
for r in pre['complete_frozen_SOURCE_files']:verify(r)
assert ident(D)==pre['SOURCE_directory_identity']
for r in pre['bound_pins'].values():verify(r)
verify(pre['complete_SOURCE_freeze']);verify(pre['independent_SOURCE_manifest']);verify(pre['current_complete_graph'])
for r in pre['copied_peer_members']:verify(r)
assert pre['HOST_absent'] is True and pre['OUT_absent'] is True and pre['external_parent_stream_paths_absent'] is True
caps={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_cap_bytes':64*2**20,'history_bytes':96*2**30,'min_free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
assert {k:pre[k] for k in caps}==caps
assert pre['new_helper_Q'] is None and pre['helper_guard_API_business_numeric_executed'] is False and pre['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False
for k in ('actual_closed_receipt','actual_host_result','actual_report','actual_watchdog','actual_merged_child_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr'):verify(summary[k])
receipt=parse(pathlib.Path(summary['actual_closed_receipt']['path']).read_bytes());terminal=receipt['terminal_tool_return']
assert receipt['initial_tool_return']['chunk_id']=='45eca8' and receipt['initial_tool_return']['session_id']==38770 and 'exit_code' not in receipt['initial_tool_return']
assert [x['chunk_id'] for x in receipt['observations']]==['59fbf2']
assert terminal==receipt['observations'][0]==summary['Root_terminal'] and terminal['chunk_id']=='59fbf2'
assert type(terminal['exit_code']) is int and terminal['exit_code']==0 and 'session_id' not in terminal
assert receipt['closed'] is True and receipt['no_closed_session_repoll'] is True and receipt['actual_tool_terminal_return_observed'] is True and receipt['retries']==0
host=parse(pathlib.Path(summary['actual_host_result']['path']).read_bytes())
report=parse(pathlib.Path(summary['actual_report']['path']).read_bytes())
watch=parse(pathlib.Path(summary['actual_watchdog']['path']).read_bytes())
assert host['schema']=='AXMAT_V21_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1' and host['status']=='ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED'
assert report['schema']=='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1' and report['status']=='ACTUAL_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_RETURNED_PENDING_EXTERNAL_ROOT'
assert len(host['stage_records'])==1
stage=host['stage_records'][0]
assert stage['label']=='run/admit' and stage['status']=='PASS' and stage['command']==watch['command']==host['actual_canonical_command'] and stage['wall_cap_seconds']==600
assert type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert watch['elapsed_seconds']==summary['child_seconds']==29.531128833070397 and watch['sampled_peak_rss_mib']==summary['sampled_peak_rss_mib']==340.3125
assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 and watch['rss_cap_mib']==512
assert host['whole_seconds']==summary['whole_seconds']==30.821748542017303 and host['whole_seconds']<1800
hostcaps={'whole_wall_cap_seconds':1800,'stage_wall_cap_seconds':600,'rss_cap_mib':512,'archive_cap_bytes':64*2**20,'threads':1,'children_at_once':1,'retries':0}
assert {k:host[k] for k in hostcaps}==hostcaps
reportcaps={'whole_host_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_HOST_SOURCE_OUT_archive_bytes':64*2**20,'history_bytes':96*2**30,'min_free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
assert {k:report[k] for k in reportcaps}==reportcaps
for resource in (host['resources_before'],host['resources_after']):
 assert resource['artifact_budget_bytes']==96*2**30 and resource['min_free_bytes']==8*2**30
 assert resource['artifact_bytes']<96*2**30 and resource['disk_free_bytes']>8*2**30
assert host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False
assert all(host[k] is False for k in ('helper_metadata_qualified','whole_business_INPUT_qualified','physical_balance_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert host['UNKNOWN_Q'] is None and host['UNKNOWN_BUSINESS_PINS'] is None
scope=('business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified')
assert all(report[k] is False for k in scope) and report['actual_external_genuine_host_and_Root_closed_exit0_required'] is True
assert host['source_namespace_before']==host['source_namespace_after']
source_before=host['source_namespace_before'];assert len(source_before['files'])==33 and source_before['symlinks']==[]
for r in source_before['files']:verify(r)
for r in source_before['directories']:assert ident(r['path'])==r['identity']
assert len(host['input_sources'])==43
for r in host['input_sources']:verify(r)
for k in ('installed_helper','actual_closed_SOURCE_install_witness','source_install_record','original_helper','resource_factory','actual_control_report','actual_merged_child_stdout_stderr','actual_watchdog'):verify(host[k])
assert report['fixed_inputs_before']==report['fixed_inputs_after']
for r in report['fixed_inputs_before'].values():verify(r)
assert summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged']==45
controls=host['actual_full_controls']
for k in ('actual_report','actual_claim','complete_expected_return','complete_actual_return','complete_actual_unfiltered_trace'):verify(controls[k])
assert all(controls[k] is True for k in ('actual_claim_parent_and_watch_PID_match','complete_private_controls','complete_current_graph_verifier_returned','external_Root_closed_terminal_required'))
claim=parse(pathlib.Path(controls['actual_claim']['path']).read_bytes())
child_admission=parse(pathlib.Path(host['actual_merged_child_stdout_stderr']['path']).read_bytes())
parent_stdout=parse(pathlib.Path(summary['actual_external_parent_stdout']['path']).read_bytes())
assert parent_stdout['status']==host['status'] and parent_stdout['actual_external_Root_terminal_required'] is True
verify(parent_stdout['actual_host_result']);verify(parent_stdout['actual_merged_child_stdout_stderr'])
assert parent_stdout['actual_host_result']==summary['actual_host_result']
assert child_admission['status']==report['status']
for pid in (host['actual_host_PID'],watch['pid'],report['PID'],report['parent_PID'],claim['PID'],claim['parent_PID'],child_admission['PID'],child_admission['parent_PID']):
 assert type(pid) is int and pid>0
assert watch['pid']==report['PID']==claim['PID']==child_admission['PID']==summary['actual_child_PID']==6986
assert host['actual_host_PID']==report['parent_PID']==claim['parent_PID']==child_admission['parent_PID']==summary['actual_host_PID']==6985
assert (claim['threads'],claim['children'],claim['retries'])==(1,1,0) and claim['phase']=='helper_complete_fresh_verifier_control'
verify(child_admission['report'])
assert {k:report['fixed_inputs_before']['new_helper'][k] for k in ('path','sha256','identity')}==host['installed_helper']
assert claim['helper']==report['fixed_inputs_before']['new_helper'] and claim['graph']==report['fixed_inputs_before']['stored_graph'] and claim['driver']==report['fixed_inputs_before']['driver']
assert report['actual_success_pins']['helper']==claim['helper'] and report['actual_success_pins']['graph']==claim['graph']
assert report['actual_success_pins']['full_return']==report['actual_complete_verifier_return'] and report['actual_success_pins']['full_trace']==report['actual_complete_ReadOpenAudit_trace']
assert claim['graph']['sha256']==pre['current_complete_graph']['sha256'] and claim['graph']['identity']==pre['current_complete_graph']['identity']
assert all(x['independent_child_stdout_captured'] is False and x['independent_child_stderr_captured'] is False for x in (host,summary,parent_stdout))
source=pathlib.Path(pre['bound_pins']['host']['path']).read_text();tree=ast.parse(source)
constant={}
for n in tree.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try:constant[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError):pass
return_fields=constant['RETURN_FIELDS'];trace_fields=constant['TRACE_FIELDS']
assert len(return_fields)==27 and len(trace_fields)==9 and report['complete_return_fields_retained']==return_fields
expectedcap=ast.parse('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20').body[0]
assert any(ast.dump(n,include_attributes=False)==ast.dump(expectedcap,include_attributes=False) for n in tree.body)
for literal in ("support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","runner.execute(HOST/'run','admit',command,STAGE_CAP)","runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_FRESH_VERIFIER',resources)"):
 assert literal in source
pc=report['private_trace_controls'];pos=pc['positive_controls'];negative=pc['rejections']
assert [x['case'] for x in pos]==['default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True']
assert all(x['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True for x in pos)
assert all(x['caller_full_identity_type_order_value_floatbits_unchanged'] is True for x in pos[:3]) and pos[3]['owned_list_completely_cleared'] is True
assert [x['case'] for x in negative]==['nonbool_consume','tuple_True','list_subclass_True']
assert all(x['rejected'] is True and x['class_name']=='InputGraphError' and x['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for x in negative)
assert pc['old60pure_control_functions_not_changed'] is True and pc['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is True
gzip_checks={}
def full_gzip(key):
 r=report[key];verify(r)
 assert r['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and r['no_fields_or_records_filtered'] is True
 blocks=[];digest=hashlib.sha256();count=0
 with gzip.open(r['path'],'rb') as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   blocks.append(block);digest.update(block);count+=len(block)
 assert count==r['uncompressed_JSON_bytes'] and digest.hexdigest()==r['uncompressed_JSON_sha256']
 verify(r);wire=b''.join(blocks)
 gzip_checks[key]=dict(path=r['path'],compressed_sha256=r['sha256'],uncompressed_bytes=count,uncompressed_sha256=digest.hexdigest(),full_gzip_EOF_and_CRC_verified=True,no_filtering=True)
 return wire,parse(wire)
expected_wire,expected=full_gzip('expected_complete_return_contract')
actual_wire,actual=full_gzip('actual_complete_verifier_return')
assert expected_wire==actual_wire and list(expected)==list(actual)==return_fields
def exact(left,right):
 assert type(left) is type(right)
 if type(left) is dict:
  assert list(left)==list(right)
  for k in left:exact(left[k],right[k])
 elif type(left) is list:
  assert len(left)==len(right)
  for a,b in zip(left,right):exact(a,b)
 elif type(left) is float:
  assert math.isfinite(left) and math.isfinite(right) and struct.pack('>d',left)==struct.pack('>d',right)
 else:assert left==right
exact(expected,actual)
counts={'canonical_files_read':37111,'logical_owner_requirements':238441,'exhaustive_namespaces_checked':86,'explicit_aliases_checked':186,'declared_absence_inputs_checked_before_and_after_bytes':479}
assert all(type(actual[k]) is int and actual[k]==v for k,v in counts.items())
assert actual['schema']=='AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2' and actual['classification']=='FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY'
assert actual['consumer_scope'] is None and actual['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and actual['phase']=='helper_complete_fresh_verifier_control' and len(actual['coverage'])==9 and len(actual['trace_coverage'])==10
assert all(actual[k] is False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified','live_subprocesses_reexecuted'))
assert report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is True
_,trace=full_gzip('actual_complete_ReadOpenAudit_trace')
assert list(trace)==trace_fields and trace['schema']=='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' and trace['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY'
assert trace['subprocess_records']==[] and type(trace['records']) is list and len(trace['records'])==37112
paths=[]
for row in trace['records']:
 assert type(row) is dict and row['event']=='open' and row['kind']=='path' and row['access']=='read' and row['observation']=='OPEN_ATTEMPT' and type(row['attempt_count']) is int and row['attempt_count']==1
 assert type(row['path']) is str
 paths.append(row['path'])
assert len(set(paths))==37112 and paths.count(pre['current_complete_graph']['path'])==1
assert type(trace['unique_records']) is int and trace['unique_records']==37112 and type(trace['actual_read_open_attempts']) is int and trace['actual_read_open_attempts']==37112
assert trace['record_storage']=='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' and trace['success_of_open_attempt_is_not_observed'] is True and trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is True
assert report['actual_complete_trace_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True)
md=report['independent_full_saved_graph_metadata'];wanted=dict(requirement_row_count=238441,requirement_column_count=5,canonical_files=37111,owners=4473,namespaces=86,aliases=186,saved_trace_records=63469,absence_inputs=479,closure_categories=9,scope='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION',consumer_scope=None,newly_declared_input_paths={},newly_declared_input_pins={})
assert all(type(md[k]) is type(v) and md[k]==v for k,v in wanted.items()) and len(md['complete_coverage_fields'])==9
out_names={pathlib.Path(r['path']).name for r in files if pathlib.Path(r['path']).parent==O}
assert out_names=={'ACTUAL_RUN_CLAIM.json','ACTUAL_REPORT.json','private_trace_fixture.txt','EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'}
assert not (H/'failed_host_result.json').exists() and not (O/'FAILED_REPORT.json').exists()
assert summary['complete_Source33_full_EOF_SHA7ID_before_after_unchanged'] is True and summary['complete_current_graph_full_EOF_SHA7ID_before_after_unchanged'] is True and summary['complete_27_fields_and_nested_type_order_value_floatbits_wire_equal'] is True
assert summary['complete_unfiltered_trace_records_and_attempts']==37112 and summary['canonical_files']==37111 and summary['stored_graph_external_reads']==1 and summary['private_positive_controls']==4 and summary['private_reject_controls']==3
assert summary['saved_evidence_independent_review_pending'] is True and summary['helper_total_qualification'] is None and summary['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False
assert report['caps_checkpoint']['elapsed_seconds']<600 and report['caps_checkpoint']['own_peak_rss_bytes']<512*2**20
joint=manifest['joint_regular_bytes_before_manifest']+inputs[str(E/'Root_actual_v21b_full_fresh_verifier_finite_saved_manifest.json')]['identity'][4]
assert joint==1909966 and joint<64*2**20 and host['archive_before_result_bytes']<64*2**20
for r in list(inputs.values()):verify(r)
for r in dirs:
 if r.get('exception') is None:assert ident(r['path'])==r['identity']
review=dict(schema='AXMAT_V21B_ACTUAL_COMPLETE_FRESH_VERIFIER_FINITE_SAVED_META_INDEPENDENT_REVIEW_V1',status='SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED',review_only=True,project_helper_guard_API_business_build_numeric_not_executed=True,closed_session_not_repolled=True,history_or_ART_glob_not_performed=True,finite_saved_files=58,complete_SOURCE_files=33,host_fixed_input_entries=43,additional_original_helper_and_resource_entries=2,all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal=True,current_graph_stream_hashed_only_not_decoded=True,input_pins=list(inputs.values()),directory_checks=dirs,actual_Root_closed_terminal=terminal,actual_host_PID=6985,actual_child_PID=6986,one_genuine_stage_PASS=True,actual_watchdog_child_exit_code=0,whole_seconds=host['whole_seconds'],child_seconds=watch['elapsed_seconds'],watchdog_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],driver_reported_own_peak_rss_mib=report['caps_checkpoint']['own_peak_rss_bytes']/2**20,sample_and_self_peak_are_distinct_observations=True,limit_failure=None,own_child_only=True,liveness_group_cleanup=True,original_caps=caps,genuine_runner_MRO_and_fixed_command_binding_preserved=True,all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal=True,complete_expected_actual_JSON_wire_bytes_equal=True,complete_gzips=gzip_checks,complete_return_counts=counts,complete_actual_unfiltered_trace=dict(records=37112,attempts=37112,unique_paths=37112,canonical_files=37111,external_graph_reads=1,subprocesses=0,all_records_read_path_open_attempt_count1=True,open_success_not_observed=True,native_HDF5_and_directory_stat_not_traced=True),private_positive_controls=4,private_rejections=3,all_source_before_after_and_fixed_driver_inputs_equal=True,all_PID_claim_report_stdout_watch_host_bindings_equal=True,actual_child_output_scope='MERGED_STDOUT_STDERR_BY_ORIGINAL_RUNNER',external_parent_streams_separately_saved=True,independent_child_stdout_captured=False,independent_child_stderr_captured=False,complete_OUT_six_files_retained=True,failed_namespace_v21_not_modified=True,joint_archive_snapshot_plus_manifest_bytes=joint,archive_cap_bytes=64*2**20,E_root_manifest_and_later_metadata_append_exclusion_honest=True,helper_total_qualification=None,helper_admission_not_created_by_this_review=True,business_component_numeric_native_whole_INPUT_AAA_ABA_physics_qualified=False,retries=0,actual_full_fresh_verifier_not_just_Source_or_small_fixture=True,qualification_boundary='Only actual complete current-graph metadata verifier evidence is independently saved-reviewed here. Original 60-second protocol remains a separate actual receipt. Root must admit their joint helper qualification; whole production INPUT/build/native/science remain unqualified.')
(P/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(P/'REPORT.txt').write_text('有限保存 META 独立复核通过，不运行项目、helper、guard、业务、数值或构建，不轮询已关闭会话。\n真实 Root 45eca8/session38770 → 59fbf2，严格整数 EXIT0/CLOSED；一项 genuine child PASS，0 retry，own-child cleanup true，limit_failure null。\nwhole 30.821748542 s / child 29.531128833 s，watchdog 采样峰值 340.3125 MiB，driver 自报自身峰值 350.1875 MiB；两种真实观测都低于原 512 MiB，不能混称同一采样。\n58 个显式保存文件、33 个完整 Source、host 43 固定入口+原 helper/resource 两入口及全部显式 prelaunch pins 的完整 EOF SHA256/七项 identity 前后相同；当前 graph 只 stream hash，不解析其它 ART 或数值。\n完整三 gzip 的解压 EOF/CRC、大小和 SHA 独立检查；expected/actual 完整 27 字段及嵌套 type/order/value/floatbits 逐项相等，完整 JSON wire 字节相等，无删字段。\n当前完整图结果含 37111 canonical / 238441 requirements / 86 namespaces / 186 aliases / 479 absences。\n真实未过滤 trace 37112 条，每条 read/path/open attempt_count=1，37111 canonical + 1 外部完整 graph；无 subprocess reexecute；audit 不观测 open 成功或 native/HDF5/stat。\n4 项私有正控、3 项拒绝、caller 非消费不变/私有消费清空均有完整保存通过证据；实际 PID、claim、report、child stdout、watch 与 host 绑定一致。\n原 whole1800/stage600/RSS512/64MiB/history96GiB/free8GiB/1thread/1child/0retry 保持；Root 有限快照+manifest 1909966 B <64MiB。E 根目录后续保存 META 的条目计数/时间变化明确排除；其它显式目录完整七项一致。\n子输出是原 runner 合并 stdout/stderr，外部 parent 两流单独保存；不声称独立 child stderr 为空。\n这是真实当前完整图 fresh verifier 的成功证据，尚未创建 helper Q：Root 还需与独立原 60 秒协议凭证共同准入。它不授完整生产 INPUT、五阶段构建、native RSS、AAA、ABA 或物理准确性资格。旧 V21 失败证据未修改。\n')
print(json.dumps({'directory':str(P),'review_sha256':pin(P/'REVIEW.json')['sha256'],'status':review['status'],'saved_files':58,'SOURCE_files':33,'unique_input_pins':len(inputs),'whole_seconds':host['whole_seconds'],'child_seconds':watch['elapsed_seconds'],'sampled_peak_rss_mib':watch['sampled_peak_rss_mib'],'full_return_fields':27,'full_trace_records':37112,'Q':None}))

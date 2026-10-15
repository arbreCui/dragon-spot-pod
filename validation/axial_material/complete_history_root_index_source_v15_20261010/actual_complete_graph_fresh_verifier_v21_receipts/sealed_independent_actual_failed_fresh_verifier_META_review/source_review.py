import pathlib,json,hashlib,stat,ast,tempfile
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_graph_fresh_verifier_v21_receipts'
P=pathlib.Path(tempfile.mkdtemp(prefix='axmat_v21_actual_failed_fresh_verifier_saved_META_review_20261010_',dir='/private/tmp'))
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);before=identity(p)
 assert stat.S_ISREG(before[2]) and before[3]==1, ('ordinary unique file',str(p))
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 assert identity(p)==before,('changed during read',str(p))
 return {'path':str(p),'sha256':h.hexdigest(),'identity':before}
inputs={}
def verify(ref):
 q=pin(ref['path'])
 assert q['sha256']==ref['sha256'],('SHA mismatch',q['path'])
 assert q['identity']==ref['identity'],('7ID mismatch',q['path'])
 if q['path'] in inputs:assert inputs[q['path']]==q
 inputs[q['path']]=q
 return q
def saved(name,sha=None):
 q=pin(E/name)
 if sha:assert q['sha256']==sha,(name,q['sha256'])
 inputs[q['path']]=q
 return json.loads(pathlib.Path(q['path']).read_bytes())
summary=saved('Root_actual_failed_complete_fresh_verifier_summary.json','845c86d44aa92be5bb7bec6261fc216c16be69fbae36b60a979f2fde6949ad18')
manifest=saved('Root_actual_failed_fresh_verifier_complete_finite_saved_manifest.json','a7441cc4b1f008301bda87fa517c02fb68c0464acf757023d0cb3ccea0fd2841')
pre=saved('Root_actual_fresh_verifier_prelaunch_META.json','44703169efa136e24ef2de4488d530a2b22393f42368b3eac368c56686032d03')
receipt=saved('Root_actual_fresh_verifier_tool_terminal_return.json','8fc9f9c2ca395fa03febe61732d468bd504290feb763bdb1e2748f75d414c2da')
freezer=saved('Root_actual_failed_fresh_verifier_META_freeze_tool_returns.json','ffe41b8feee1d060bb5e0bf10b90d03b3a13fd53b176e82a90c1ab7817ec742a')
refs=manifest['complete_regular_files']
assert len(refs)==49 and len({r['path'] for r in refs})==49
assert manifest['qualification_granted'] is False and manifest['complete_SOURCE_frozen'] is True
assert manifest['symlinks']==[] and manifest['joint_cap_bytes']==64*2**20
assert sum(r['identity'][4] for r in refs)==manifest['joint_regular_bytes_before_manifest']==695377
for r in refs:verify(r)
D=B/'actual_complete_graph_fresh_verifier_v21_sources'
H=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21-20261010')
O=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21-20261010')
assert set(manifest['roots'])=={str(x) for x in (H,O,D,E)}
assert len(pre['complete_frozen_SOURCE_files'])==pre['SOURCE_file_count']==23
source_refs={r['path']:r for r in pre['complete_frozen_SOURCE_files']}
assert set(source_refs)=={r['path'] for r in refs if pathlib.Path(r['path']).parent==D}
for r in source_refs.values():verify(r)
for r in pre['installed_and_bound_pins'].values():verify(r)
verify(pre['current_complete_graph'])
verify(pre['actual_independent_SOURCE_manifest'])
freeze=saved('Root_generated_full_SOURCE_namespace_freeze.json','e7ef597da8a46cb84627346d1664a6a4d8b2babae32ee9100c8dfd484b724171')
assert len(freeze['complete_files'])==23 and freeze['symlinks']==[] and freeze['subdirectories']==[]
assert freeze['no_SOURCE_append_after_freeze'] is True and freeze['actual_runtime_executed'] is False
for r in freeze['complete_files']:verify(r)
dirs=[]
for r in manifest['directory_identities_before_manifest']:
 cur=identity(pathlib.Path(r['path']))
 assert stat.S_ISDIR(cur[2])
 if r['path']==str(E):
  assert cur[:3]==r['identity'][:3]
 else:
  assert cur[:4]==r['identity'][:4]
 if r['path']==str(E):
  assert manifest['manifest_self_and_later_Root_receipts_excluded_from_self_pin'] is True
  dirs.append(dict(path=r['path'],classification='PRE_MANIFEST_E_ROOT_SNAPSHOT_LATER_ROOT_METADATA_EXPLICITLY_EXCLUDED',before=r['identity'],current=cur,full_7ID_equal=cur==r['identity']))
 else:
  assert cur==r['identity'],('immutable directory changed',r['path'])
  dirs.append(dict(path=r['path'],classification='EXACT_FULL_7ID',identity=cur))
assert identity(D)==pre['SOURCE_directory_identity']
assert pre['HOST_absent'] is True and pre['OUT_absent'] is True and pre['external_parent_stream_paths_absent'] is True
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_cap_bytes=64*2**20,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0)
assert {k:pre[k] for k in caps}==caps
t=receipt['terminal_tool_return'];initial=receipt['initial_tool_return']
assert initial['chunk_id']=='935ded' and initial['session_id']==92323 and 'exit_code' not in initial
assert [r['chunk_id'] for r in receipt['observations']]==['622265','054e28']
assert t==receipt['observations'][-1]==summary['Root_actual_terminal']
assert type(t['exit_code']) is int and t['exit_code']==1 and 'session_id' not in t
assert receipt['closed'] is True and receipt['actual_tool_terminal_return_observed'] is True and receipt['no_closed_session_repoll'] is True and receipt['retries']==0
for k in ('actual_closed_receipt','actual_watchdog','actual_host_failure','actual_driver_failure','actual_merged_child_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr'):verify(summary[k])
watch=json.loads(pathlib.Path(summary['actual_watchdog']['path']).read_bytes())
hf=json.loads(pathlib.Path(summary['actual_host_failure']['path']).read_bytes())
df=json.loads(pathlib.Path(summary['actual_driver_failure']['path']).read_bytes())
log=pathlib.Path(summary['actual_merged_child_stdout_stderr']['path']).read_text()
assert type(watch['returncode']) is int and watch['returncode']==1
assert watch['elapsed_seconds']==summary['child_elapsed_seconds']==29.261444209027104
assert watch['sampled_peak_rss_mib']==summary['sampled_peak_rss_mib']==332.359375
assert watch['limit_failure'] is None and summary['limit_failure'] is None
assert watch['rss_cap_mib']==summary['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert summary['own_child_only'] is True and summary['liveness_group_cleanup'] is True and summary['child_returncode']==1
assert len(hf['stage_records'])==1
stage=hf['stage_records'][0]
assert stage['command']==watch['command'] and stage['label']=='run/admit' and stage['status']=='FAILED' and stage['wall_cap_seconds']==600
assert stage['resource_before']['min_free_bytes']==8*2**30 and stage['resource_before']['artifact_budget_bytes']==96*2**30
assert hf['status']=='FAILED_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_NO_RETRY'
assert df['status']=='FAILED_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_NO_RETRY' and df['actual_success_pins'] is None
dfcaps={'whole_host_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_HOST_SOURCE_OUT_archive_bytes':64*2**20,'history_bytes':96*2**30,'min_free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
assert {k:df[k] for k in dfcaps}==dfcaps
science_keys=('business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified')
assert all(df[k] is False for k in science_keys)
assert all(hf[k] is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
pc=df['private_trace_controls'];pos=pc['positive_controls'];rej=pc['rejections']
assert [r['case'] for r in pos]==['default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True']
assert all(r['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True for r in pos)
assert all(r['caller_full_identity_type_order_value_floatbits_unchanged'] is True for r in pos[:3]) and pos[3]['owned_list_completely_cleared'] is True
assert [r['case'] for r in rej]==['nonbool_consume','tuple_True','list_subclass_True']
assert all(r['class_name']=='InputGraphError' and r['rejected'] is True and r['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for r in rej)
assert pc['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is True and pc['old60pure_control_functions_not_changed'] is True
error='complete return key order changed at complete_actual_fresh_verifier_return/fresh_reader_contract'
assert df['error']=={'class_name':'AssertionError','message':error}
assert error in log and "exact_value(expected,verified,'complete_actual_fresh_verifier_return')" in log
assert summary['actual_child_traceback_shows_verify_graph_returned_before_comparison'] is True
assert all(summary[k] is True for k in ('complete_Source23_before_after_unchanged','installed_bound_pins_before_after_unchanged','complete_current_graph_before_after_unchanged','failed_namespace_frozen_no_reuse'))
assert all(summary[k] is False for k in ('complete_actual_return_trace_saved_or_externally_qualified','expected_complete_return_gzip_created','actual_complete_return_gzip_created','actual_complete_trace_gzip_created','independent_child_stdout_captured','independent_child_stderr_captured','whole_build_INPUT_native_AAA_ABA_physics_qualified'))
assert summary['helper_total_qualification'] is None and summary['retries']==0
host_source=pathlib.Path(pre['installed_and_bound_pins']['host']['path']).read_text()
tree=ast.parse(host_source)
cap_nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Tuple) and [e.id for e in t.elts]==['WHOLE_CAP','STAGE_CAP','RSS_CAP','ARCHIVE_CAP'] for t in n.targets)]
expectedcap=ast.parse('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20').body[0]
assert len(cap_nodes)==1 and ast.dump(cap_nodes[0],include_attributes=False)==ast.dump(expectedcap,include_attributes=False)
assert "support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))" in host_source
assert "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in host_source
assert "runner.execute(HOST/'run','admit',command,STAGE_CAP)" in host_source
assert "runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_FRESH_VERIFIER',resources)" in host_source
driver_source=pathlib.Path(pre['installed_and_bound_pins']['driver']['path']).read_text()
driver_tree=ast.parse(driver_source)
assert "verified=new.verify_graph" in driver_source and "exact_value(expected,verified,'complete_actual_fresh_verifier_return')" in driver_source
gzs=sorted({n.value for n in ast.walk(driver_tree) if isinstance(n,ast.Constant) and type(n.value) is str and n.value.endswith('.gz')})
assert len(gzs)==3
absent=[H/'result.json',O/'ACTUAL_REPORT.json']+[O/n for n in gzs]
assert all(not p.exists() and not p.is_symlink() for p in absent)
assert freezer['closed'] is True and type(freezer['first_terminal']['exit_code']) is int and freezer['first_terminal']['exit_code']==1
assert freezer['first_terminal']['chunk_id']=='9b6117'
assert type(freezer['corrected_terminal']['exit_code']) is int and freezer['corrected_terminal']['exit_code']==0 and 'session_id' not in freezer['corrected_terminal'] and freezer['corrected_terminal']['chunk_id']=='a083cf'
assert 'FAILED_REPORT.json' in freezer['correction'] and 'no Source/host/output/API rerun' in freezer['correction']
after={}
for r in list(inputs.values()):after[r['path']]=verify(r)
assert after==inputs
review=dict(schema='AXMAT_V21_ACTUAL_FAILED_COMPLETE_FRESH_VERIFIER_FINITE_SAVED_META_REVIEW_V1',status='SAVED_FAILURE_EVIDENCE_VERIFIED_NO_QUALIFICATION',project_or_helper_API_imported_or_executed=False,business_numeric_build_or_guard_executed=False,closed_session_repolled=False,history_or_ART_glob_performed=False,manifest_file_count=49,complete_SOURCE_file_count=23,all_enumerated_files_and_explicit_prelaunch_pins_fresh_full_EOF_SHA256_and_7ID_equal=True,current_graph_only_stream_hashed_not_parsed=True,input_pins=list(inputs.values()),directory_checks=dirs,immutable_directory_checks=8,receipt_terminal=t,actual_child=dict(returncode=1,elapsed_seconds=watch['elapsed_seconds'],sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],limit_failure=None,own_child_only=True,liveness_group_cleanup=True),original_caps=caps,original_source_cap_assignment_and_genuine_runner_bindings_preserved=True,watchdog_and_stage_command_exact=True,actual_failure=df['error'],verify_graph_return_before_comparison_supported_by_actual_traceback=True,full_actual_return_type_value_order_floatbits_equivalence=False,complete_actual_return_or_trace_saved=False,small_private_positive_controls=4,small_private_rejections=3,small_private_controls_do_not_qualify_complete_graph=True,merged_child_stdout_stderr_only=True,independent_child_stdout_or_stderr_captured=False,missing_success_outputs=[str(p) for p in absent],helper_total_qualification=None,whole_business_INPUT_native_AAA_ABA_physics_qualification=False,retries=0,failed_namespace_frozen_no_reuse=True,archive=dict(explicit_Root_snapshot49_regular_bytes=695377,manifest_bytes=inputs[str(E/'Root_actual_failed_fresh_verifier_complete_finite_saved_manifest.json')]['identity'][4],later_Root_META_receipt_bytes=inputs[str(E/'Root_actual_failed_fresh_verifier_META_freeze_tool_returns.json')]['identity'][4],explicit_finite_snapshot_plus_manifest_and_META_receipt_bytes=695377+26343+2467,cap_bytes=64*2**20,no_unbounded_current_E_namespace_claim=True),Root_META_freeze_first_actual_exit1_preserved=True,Root_META_only_corrected_actual_exit0_preserved=True,no_actual_runtime_success_created=True,source_only_possible_next_action='Review and correct expected old-parent full return key-order oracle without removing original comparisons; any actual rerun requires a new one-use namespace.')
(P/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(P/'REPORT.txt').write_text('仅有限保存 META 复核，不执行项目、helper、guard、构建或数值，也不轮询已关闭会话。\n49 个显式保存文件、23 个完整 Source、全部显式 prelaunch pins 与当前完整图均 fresh EOF SHA256/七项 OS identity 相同；图只哈希不解码。\n真实 Root 935ded/session92323 → 622265 → 054e28，严格整数 EXIT1，CLOSED，0 retry。\n实际 child 29.261444209 s / 332.359375 MiB，原 600 s / 512 MiB 内，limit_failure null，own-child cleanup true。\n新 verify_graph 已返回，但完整返回比较在 fresh_reader_contract 字典键顺序处失败。未验证完整返回等价，未保存完整实际 return/trace，无 ACTUAL_REPORT、host result 或三项 gzip，无新 helper Q。\n四项小私有 trace 正控、三项拒绝有保存 PASS 证据，不能替代当前完整图资格。\n原 whole1800/stage600/RSS512/64MiB/history96GiB/free8GiB/1 thread/1 child/0 retry 保持。\nRoot 首次 META freeze 9b6117 EXIT1 是 OUT 文件名单少了实际 FAILED_REPORT；保存纠正 a083cf EXIT0，无项目重跑。\nmanifest 是增加自身和后续 Root META 前的有限快照；E 根目录条目计数、大小和时间变化据此明确披露，不声称其前后七项全相等。其余八个显式目录完整七项一致。\n本审查不授完整 INPUT、构建、native、AAA、ABA 或物理准确性资格；下一步只能先源码审查 expected 旧 parent oracle 的顺序，再决定新目录的一次完整验证。\n')
print(json.dumps({'directory':str(P),'review_sha256':pin(P/'REVIEW.json')['sha256'],'status':review['status'],'files':49,'SOURCE_files':23,'pinned_unique_files':len(inputs),'child_seconds':watch['elapsed_seconds'],'peak_MiB':watch['sampled_peak_rss_mib'],'qualification':None},ensure_ascii=False))

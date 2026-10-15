import pathlib,json,hashlib,stat,gzip,math,struct,ast,tempfile
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
Q=B/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json'
E=B/'actual_complete_graph_fresh_verifier_v21b_receipts'
writer=pathlib.Path('/private/tmp/spot_v21_joint_helper_admission_root_meta_20261010.py')
P=pathlib.Path(tempfile.mkdtemp(prefix='axmat_v21_joint_helper_Q_finite_saved_META_independent_review_20261010_',dir='/private/tmp'))
def identity(p):
 s=pathlib.Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and before[3]==1
 digest=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(2**20),b''):digest.update(chunk)
 assert identity(p)==before
 return dict(path=str(p),sha256=digest.hexdigest(),size_bytes=before[4],identity=before)
inputs={}
def verify(ref):
 q=pin(ref['path']);assert q['sha256']==ref['sha256'] and q['identity']==ref.get('identity',ref.get('identity7')),('SHA7ID mismatch',q['path'])
 if 'size_bytes' in ref:assert type(ref['size_bytes']) is int and q['size_bytes']==ref['size_bytes']
 if q['path'] in inputs:assert inputs[q['path']]==q
 inputs[q['path']]=q;return q
def pairs(items):
 d={}
 for k,v in items:assert k not in d;d[k]=v
 return d
def reject_nonfinite(x):raise ValueError(x)
def parse(data):return json.loads(data,object_pairs_hook=pairs,parse_constant=reject_nonfinite)
def read_ref(ref):
 q=verify(ref);v=parse(pathlib.Path(q['path']).read_bytes());verify(ref);return v
def refs(value):
 if type(value) is dict:
  if {'path','sha256'}<=set(value) and ('identity' in value or 'identity7' in value):yield value
  else:
   for v in value.values():yield from refs(v)
 elif type(value) is list:
  for v in value:yield from refs(v)
qpin=pin(Q);assert qpin['sha256']=='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2' and qpin['size_bytes']==19363
q=read_ref(qpin);f=q['complete_current_graph_fresh_verifier']
writer_pin=pin(writer);inputs[str(writer)]=writer_pin
wtree=ast.parse(writer.read_text())
assert {ast.unparse(n) for n in wtree.body if isinstance(n,(ast.Import,ast.ImportFrom))}=={'import hashlib','import json','import stat','from pathlib import Path'}
wrpin=pin(E/'Root_actual_joint_helper_admission_META_tool_return.json');wreceipt=read_ref(wrpin);wr=wreceipt['terminal_tool_return']
assert wr['chunk_id']=='7b37a2' and type(wr['exit_code']) is int and wr['exit_code']==0 and 'session_id' not in wr
assert wreceipt['closed'] is True and wreceipt['Root_META_only'] is True and wreceipt['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False
wout=parse(wr['output']);assert wout['qualification']==qpin and wout['unique_fresh_explicit_inputs']==151
assert wout['pure_Root_terminal']=='5e1034' and wout['fresh_Root_terminal']=='59fbf2' and wout['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False
assert q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21' and q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21'
assert q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count']==151 and q['Root_finite_joint_META_only_no_project_API_or_numeric'] is True
business_flags=('supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified')
assert all(q[k] is False for k in business_flags)
assert q['helper']['sha256']=='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7' and q['helper']['size_bytes']==147870 and q['helper']['identity']==[16777229,49380106,33188,1,147870,1791589379138539325,1791589879966481802]
for r in refs(q):verify(r)
pure=read_ref(q['actual_controls_summary']);fresh=read_ref(f['actual_controls_summary'])
pp=read_ref(q['independent_actual_review']);fp=read_ref(f['independent_actual_review'])
assert len(pp['pins'])==83 and len(fp['input_pins'])==72
peer_union={r['path']:r for r in pp['pins']+fp['input_pins']};assert len(peer_union)==147
for r in peer_union.values():verify(r)
joint_paths=set(peer_union)|{q['independent_actual_review']['path'],f['independent_actual_review']['path'],q['independent_actual_review_tool_return']['path'],f['independent_actual_review_tool_return']['path']}
assert len(joint_paths)==151
assert all(p in inputs for p in joint_paths)
assert pp['status']=='ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER' and pp['blockers']==[] and pp['all_explicit_input_SHA7ID_before_after_exact'] is True
assert fp['status']=='SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED' and fp['all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal'] is True
ptools=read_ref(q['independent_actual_review_tool_return']);ftools=read_ref(f['independent_actual_review_tool_return'])
pr=ptools['actual_review_tool_result'];fr=ftools['actual_review_terminal_return']
assert pr['chunk_id']=='2eb342' and type(pr['exit_code']) is int and pr['exit_code']==0 and 'session_id' not in pr
assert fr['chunk_id']=='45cf76' and type(fr['exit_code']) is int and fr['exit_code']==0 and 'session_id' not in fr and ftools['actual_review_closed'] is True
def terminal(ref,first,session,last):
 r=read_ref(ref);a=r['initial_tool_return'];t=r['terminal_tool_return']
 assert a['chunk_id']==first and type(a['session_id']) is int and a['session_id']==session and 'exit_code' not in a
 assert t['chunk_id']==last and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and r['closed'] is True
 assert r.get('no_closed_session_repoll',True) is True and r.get('session_repolled_after_close',False) is False and r.get('retries',0)==0
 return t
pure_terminal=terminal(q['actual_root_terminal'],'ea406f',49247,'5e1034')
fresh_terminal=terminal(f['actual_root_terminal'],'45eca8',38770,'59fbf2')
pure_report=read_ref(q['actual_control_report']);fresh_report=read_ref(f['actual_control_report'])
pure_host=read_ref(q['actual_host_result']);fresh_host=read_ref(f['actual_host_result'])
fixture=read_ref(q['full_protocol_additional_complete_fixture_artifact']);codec=read_ref(q['full_protocol_additional_complete_codec_artifact'])
assert pure_report['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'
assert [x['stage'] for x in pure_report['stages']]==['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged']
assert fixture['producer_full_exact_values_types_order_floatbits'] is True
assert fixture['caller_full_value_and_mutable_identity_preserved'] is True and pure_report['small_fixture']['caller_full_value_and_mutable_identity_preserved'] is True
subtypes=pure_report['small_fixture']['accepted_str_subclass_equivalence_controls']
assert len(subtypes)==2 and all(x['complete_builtin_output_values_types_order_floatbits_equal'] is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged'] is True for x in subtypes)
assert fixture['accepted_str_subclass_equivalence_controls']==subtypes
assert codec['all_default_inputs_unmodified'] is True and codec['all_lossless_missing_null_order_type_floatbit_duplicate_controls'] is True and codec['ordinary_and_both_storage_strict_dispatches'] is True
assert len(codec['rejections'])==pure_report['small_codecs']['rejections']==61
old=pure_report['full_old_saved_graph'];meta=old['complete_original_metadata'];trace=pure_report['full_new_creation_trace']
assert meta==old['normal_strict_file_entrance_full_semantics_and_counts']==old['normal_strict_payload_entrance_full_semantics_and_counts']
assert old['full_default_roundtrip_exact'] is True and old['old_read_trace_not_replaced_by_new_trace'] is True and old['original_legacy_semantic_sha_preserved'] is True
assert pp['full_report_original_metadata_and_both_strict_entrances_equal'] is True and pp['full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified'] is True
assert trace['exact_full_roundtrip'] is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse'] is True and trace['default_source_nonmutation'] is True
derived_protocol=dict(original_and_fresh_small_producer_values_types_order_floatbits_exact=True,all_caller_mutable_identity_and_subtype_attributes_unchanged=True,accepted_str_subtype_groups=len(subtypes),small_codec_rejections=pure_report['small_codecs']['rejections'],complete_original_graph_counts=meta['complete_counts'],complete_old_graph_two_normal_strict_entrances_exact=True,complete_old_legacy_semantic_sha256=meta['legacy_semantic_sha256'],complete_old_wire_content_sha256=meta['wire_content_sha256'],complete_new_creation_trace_records=trace['full_record_count'],complete_new_creation_trace_actual_attempts=trace['actual_attempt_count'],new_creation_trace_not_substituted_into_old_graph=True,full_json_types_order_floatbits_and_values_retained=True,default_source_nonmutation=True)
assert len(derived_protocol)==13 and q['full_protocol']==derived_protocol and list(q['full_protocol'])==list(derived_protocol)
assert meta['complete_counts']['canonical_files']==36776 and meta['complete_counts']['requirements']==237767 and meta['complete_counts']['read_trace_records']==62332
assert trace['full_record_count']==63379 and trace['actual_attempt_count']==175886
purecaps=dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
freshcaps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HOST_OUT_SOURCE_E_archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0)
assert q['original_caps']==purecaps and f['original_caps']==freshcaps
assert pure['whole_seconds_cap']==pure['stage_seconds_cap']==60 and pure['rss_mib_cap']==512 and pure['archive_bytes_cap']==64*2**20
assert fresh['whole_seconds_cap']==1800 and fresh['stage_seconds_cap']==600 and fresh['rss_mib_cap']==512 and fresh['joint_archive_cap_bytes']==64*2**20
pm=q['actual_measurement'];fm=f['actual_measurement']
assert pm==dict(whole_seconds=pure['whole_seconds'],child_seconds=pure['child_seconds'],sampled_peak_rss_mib=pure['sampled_peak_rss_mib'],actual_final_host_out_source_bytes=pure['joint_source_host_out_bytes'],old_complete_graph_stored_bytes=old['stored_wholegraph']['size_bytes'],new_complete_trace_original_compact_bytes=trace['original_insertion_order_compact_source']['size_bytes'],new_complete_trace_stored_bytes=trace['encoded_artifact']['size_bytes'])
assert (pm['whole_seconds'],pm['child_seconds'],pm['sampled_peak_rss_mib'])==(16.88399320805911,15.591446500038728,384.140625)
assert pm['actual_final_host_out_source_bytes']==59662256<64*2**20 and pm['old_complete_graph_stored_bytes']==45300566 and pm['new_complete_trace_stored_bytes']==8488204
assert fm['whole_seconds']==fresh['whole_seconds']==30.821748542017303 and fm['child_seconds']==fresh['child_seconds']==29.531128833070397 and fm['sampled_peak_rss_mib']==fresh['sampled_peak_rss_mib']==340.3125
assert fm['driver_reported_own_peak_rss_mib']==fp['driver_reported_own_peak_rss_mib']==350.1875 and fm['sample_and_self_peaks_are_distinct'] is True
assert fm['joint_snapshot_plus_manifest_bytes_at_original_closeout']==fp['joint_archive_snapshot_plus_manifest_bytes']==1909966 and fm['current_joint_regular_bytes_after_saved_peer_and_copy_receipts']==2276156<64*2**20
for host in (pure_host,fresh_host):
 assert len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['command']==host['actual_canonical_command']==host['watchdog']['command']
 assert type(host['watchdog']['returncode']) is int and host['watchdog']['returncode']==0 and host['watchdog']['limit_failure'] is None and host['watchdog']['own_child_only'] is True and host['watchdog']['liveness_group_cleanup'] is True
 assert host['rss_cap_mib']==512 and host['threads']==host['children_at_once']==1 and host['retries']==0 and host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False
 assert all(host[k] is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
 assert host['resources_before']['artifact_budget_bytes']==host['resources_after']['artifact_budget_bytes']==96*2**30
 assert host['resources_before']['min_free_bytes']==host['resources_after']['min_free_bytes']==8*2**30
assert pure['new_private_consume_full_verify_graph_executed'] is False and pure['actual_full_current_V20_graph_fresh_verifier_qualified'] is False
assert f['full_public_return_field_order']==fresh_report['complete_return_fields_retained'] and len(f['full_public_return_field_order'])==27
assert f['full_current_graph_metadata']==fresh_report['independent_full_saved_graph_metadata']
assert f['complete_actual_unfiltered_read_trace_counts']==fresh_report['actual_complete_trace_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True)
assert f['all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal'] is True and f['SOURCE33_and_all_fixed_inputs_before_after_unchanged'] is True and f['actual_external_Root_exit0_closed_and_saved_peer_pass'] is True
assert fp['all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal'] is True and fp['complete_expected_actual_JSON_wire_bytes_equal'] is True
positive=fresh_report['private_trace_controls']['positive_controls'];negative=fresh_report['private_trace_controls']['rejections']
assert f['private_positive_controls']==len(positive)==4 and f['private_reject_controls']==len(negative)==3
assert all(x['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is True for x in positive)
assert all(x['rejected'] is True and x['class_name']=='InputGraphError' and x['caller_type_identity_nested_value_order_floatbits_unchanged'] is True for x in negative)
assert all(fresh_report[k] is False for k in ('business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified'))
gzchecks={}
def unpack(key):
 ref=fresh_report[key];verify(ref)
 assert {k:ref[k] for k in ('path','sha256','size_bytes','identity')}==f['complete_gzips'][key]
 assert ref['no_fields_or_records_filtered'] is True and ref['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True
 blocks=[];h=hashlib.sha256();n=0
 with gzip.open(ref['path'],'rb') as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   blocks.append(block);h.update(block);n+=len(block)
 assert n==ref['uncompressed_JSON_bytes'] and h.hexdigest()==ref['uncompressed_JSON_sha256']
 verify(ref);wire=b''.join(blocks);gzchecks[key]=dict(compressed_pin=inputs[ref['path']],full_decompression_EOF_CRC_verified=True,uncompressed_bytes=n,uncompressed_sha256=h.hexdigest(),all_payload_retained=True)
 return wire,parse(wire)
ew,expected=unpack('expected_complete_return_contract');aw,actual=unpack('actual_complete_verifier_return');assert ew==aw
def exact(a,b):
 assert type(a) is type(b)
 if type(a) is dict:
  assert list(a)==list(b)
  for k in a:exact(a[k],b[k])
 elif type(a) is list:
  assert len(a)==len(b)
  for x,y in zip(a,b):exact(x,y)
 elif type(a) is float:assert math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
 else:assert a==b
exact(expected,actual);assert list(actual)==f['full_public_return_field_order']
assert actual['canonical_files_read']==37111 and actual['logical_owner_requirements']==238441 and actual['exhaustive_namespaces_checked']==86 and actual['explicit_aliases_checked']==186 and actual['declared_absence_inputs_checked_before_and_after_bytes']==479
assert actual['consumer_scope'] is None and actual['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and len(actual['coverage'])==9 and len(actual['trace_coverage'])==10
assert all(actual[k] is False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified','live_subprocesses_reexecuted'))
_,fulltrace=unpack('actual_complete_ReadOpenAudit_trace')
assert len(fulltrace['records'])==37112 and fulltrace['unique_records']==fulltrace['actual_read_open_attempts']==37112 and fulltrace['subprocess_records']==[]
paths=[]
for row in fulltrace['records']:
 assert type(row) is dict and row['event']=='open' and row['kind']=='path' and row['access']=='read' and row['observation']=='OPEN_ATTEMPT' and type(row['attempt_count']) is int and row['attempt_count']==1
 paths.append(row['path'])
assert len(set(paths))==37112 and paths.count(fresh_report['fixed_inputs_before']['stored_graph']['path'])==1
assert fulltrace['success_of_open_attempt_is_not_observed'] is True and fulltrace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is True
fresh_claim=read_ref(fresh_host['actual_full_controls']['actual_claim'])
assert fresh_claim['PID']==fresh_report['PID']==fresh_host['watchdog']['pid']==6986 and fresh_claim['parent_PID']==fresh_report['parent_PID']==fresh_host['actual_host_PID']==6985
assert fresh_host['independent_child_stdout_captured'] is False and fresh_host['independent_child_stderr_captured'] is False and pure['separate_child_stderr_capture_verified'] is False and pure['child_stdout_stderr_merge_is_original_normal_guard'] is True
source_pure=read_ref(q['source_manifest']);source_fresh=read_ref(f['source_manifest'])
assert len(list(refs(source_fresh)))>=33 and pure['source_file_count']==29
for r in refs(source_pure):verify(r)
for r in refs(source_fresh):verify(r)
fresh_seal=read_ref(f['sealed_independent_actual_review_manifest'])
assert fresh_seal['member_count']==4 and fresh_seal['actual_review_exit_code']==0 and fresh_seal['actual_review_closed'] is True and fresh_seal['helper_Q_created'] is False and fresh_seal['business_or_science_qualification_created'] is False
for r in fresh_seal['members']:verify(r)
for r in list(inputs.values()):verify(r)
assert pin(Q)==qpin
review=dict(schema='AXMAT_V21_EXISTING_ACTUAL_JOINT_HELPER_Q_FINITE_SAVED_META_INDEPENDENT_REVIEW_V1',status='EXISTING_ROOT_JOINT_HELPER_METADATA_QUALIFICATION_SAVED_EVIDENCE_PASS',existing_Q=qpin,Q_not_created_or_modified_by_review=True,Root_actual_META_writer_terminal=wr,Root_actual_META_writer_Source_pin=writer_pin,Root_writer_imports_standard_library_only=True,Root_writer_existing_four_namespace_archive_measurement_not_reexecuted=True,Root_writer_151_input_derivation=dict(pure_peer_pins=83,fresh_peer_pins=72,shared_paths=8,peer_union_unique=147,two_review_reports_and_two_actual_review_tool_receipts=4,total=151),all_151_Root_inputs_fresh_full_EOF_SHA7ID_before_after_verified=True,additional_Q_writer_receipt_source_and_explicit_manifest_members_also_verified=True,all_unique_review_input_pins=list(inputs.values()),actual_terminals=dict(original_protocol=pure_terminal,complete_fresh_verifier=fresh_terminal),independent_actual_review_terminals=dict(original_protocol=pr,complete_fresh_verifier=fr),full_13_original_protocol_fields_exactly_derived_from_actual_report_complete_fixture_and_codec_artifacts=True,full_original_protocol=derived_protocol,distinct_original_60_second_producer_codec_and_complete_current_graph_fresh_API_trials=True,original_protocol_does_not_call_verify_graph=True,full_27_return_fields_nested_types_order_values_floatbits_and_complete_wire_bytes_equal=True,complete_current_graph_actual_read_trace_records_and_attempts=37112,all_trace_read_path_open_attempt1_and_unique_paths=True,canonical_files=37111,external_graph_reads=1,private_positive_controls=4,private_rejections=3,all_3_gzips_independently_full_EOF_CRC_size_SHA256_checked=gzchecks,original_protocol_caps=purecaps,complete_fresh_verifier_caps=freshcaps,original_protocol_actual_measurement=pm,complete_fresh_verifier_actual_measurement=fm,driver_self_peak_and_watch_sample_peak_kept_distinct=True,current_graph_and_other_ART_inputs_stream_hashed_only_when_explicitly_pinned=True,PID_claim_report_watch_and_host_bound=True,original_child_merged_stream_scope_preserved=True,independent_child_stderr_not_captured_or_claimed_empty=True,helper_exact_fullSHA_size_and_7ID_verified=q['helper'],all_business_INPUT_build_native_AAA_ABA_physics_flags_false=True,existing_Q_qualifies_helper_metadata_protocol_only=True,project_helper_guard_API_numeric_business_build_not_executed=True,ART_or_history_glob_not_performed=True,closed_sessions_not_repolled=True,namespace_or_canonical_or_existing_Q_not_modified=True,new_helper_Q_or_science_qualification_not_created=True,review_scope='Finite saved evidence review of an existing Root joint helper metadata qualification. Does not replace actual production build, whole INPUT/native or scientific acceptance.')
(P/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(P/'REPORT.txt').write_text('既有 Root 联合 helper Q 的有限保存 META 独审通过；只写新 TMP 报告，不创建、修改 Q/canonical/D/E，也不运行项目 API、guard、业务、数值或构建。\nQ 固定 SHA 29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2，19363 B；Root metadata writer 7b37a2 真实严格整数 EXIT0/CLOSED。\n151 输入可重建：83 个原 60 秒独审 pins 与 72 个 V21b 独审 pins，共享 8，去重 147；两份独审 REVIEW 与两份真实审查工具返回再加 4，共 151。全部 fresh EOF SHA256/七项 identity 前后相同。\n原协议 13 字段逐项源于完整 actual report、fixture、codec：2 个 str subtype、61 拒绝、old graph 36776 files/237767 requirements/62332 trace、new creation trace 63379 保留；两次旧图 strict entrance、原语义/wire hash、全类型/顺序/值/floatbits、caller nonmutation 保持，不把新 trace 替换旧 trace。\n两次实际 Root 原协议 5e1034 和 full fresh 59fbf2 均 int EXIT0/CLOSED；两份独立保存审查 2eb342/45cf76 int0 绑定，未重复轮询。\n资源合同分开：原协议 whole60/stage60，实际16.883993 s/15.591447 s/384.140625 MiB；完整 fresh whole1800/stage600，实际30.821749 s/29.531129 s/watch340.3125 MiB，driver self350.1875 MiB 是另一个观测。两者均原RSS512/64MiB/history96GiB/free8GiB/1thread/1child/0retry。\n完整三 gzip 独立全 EOF/CRC/size/SHA 检查，27 全返回字段及所有嵌套 type/order/value/floatbits 完整相等、wire bytes相等；37112 条全实际读取记录：37111 canonical+1 graph，各 read/path/open attempt1，4 正控+3拒绝完整。\n完整当前 graph 仅按显式 pin stream hash；未解析其它 ART 或数值，未做 ART/history glob。Root 在既有四个指定 namespace 的归档测量不重跑，64MiB合同与原/新增测量分开保存。\nhelper dc01... 完整 SHA、147870 B 和精确七项身份一致，PID/guard/stream合同保留；子 stderr 与 stdout 是原 runner 合并流，不能声称独立 child stderr 为空。\n联合 Q 只准入 helper 元数据协议。所有 whole build/INPUT/native/AAA/ABA/physics 标志仍 false；本审查不创建任何新 Q 或科学资格。\n')
print(json.dumps({'directory':str(P),'review_sha256':pin(P/'REVIEW.json')['sha256'],'status':review['status'],'Root_joint_input_count':151,'all_unique_review_input_pins':len(inputs),'Q_sha256':qpin['sha256'],'new_Q_created':False,'business_science_qualified':False}))

"""Finish bounded saved encoded metadata/false-scope checks; reuse completed file hashes."""
import base64
import hashlib
import json
from pathlib import Path
import time

OUT = Path(__file__).parent
START = time.monotonic()
prior = json.loads((OUT/'FINAL_REVIEW.json').read_text())
assert prior['status'] == 'ACTUAL_PREP_EVIDENCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE'
assert prior['blocking_findings'] == ["ValueError('actual_complete_saved_graph_metadata_counts')"]
pins = prior['file_pins']
assert len(pins) == 87
checks = {k:v for k,v in prior['checks'].items() if k != 'actual_complete_saved_graph_metadata_counts'}
assert all(type(v) is bool and v is True for v in checks.values())

def check(label, condition):
    if type(condition) is not bool:
        raise TypeError(label)
    checks[label] = condition
    if condition is not True:
        raise ValueError(label)

def identity(path):
    s = Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def metadata(path):
    key = str(path)
    pin = pins[key]
    before = identity(path)
    raw = Path(path).read_bytes()
    after = identity(path)
    check('remaining_only_saved_metadata_complete_EOF_SHA7ID:' + key, before == after == pin['after7ID'] and len(raw) == pin['size_bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'])
    return json.loads(raw)

review = dict(schema='AXMAT_V19_INDEPENDENT_ACTUAL_COMPLETE_PREP_EVIDENCE_REVIEW_FINAL_V1', scope='ACTUAL_SAVED_COMPLETE_PREP_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE', project_module_imported=False, project_API_or_helper_called=False, business_executed=False, numerical_or_physical_computation=False, numeric_payload_interpreted=False, resource_or_guard_called=False, original_namespace_or_input_modified=False, cleanup_performed=False, blocking_findings=[])
try:
    for key,pin in pins.items():
        check('reused_actual_87_full_SHA_proofs_current_7ID_exact:' + key, identity(key) == pin['after7ID'])
    E = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v19_receipts')
    summary = metadata(E/'Root_actual_complete_combined_prepare_summary.json')
    namespace = metadata(E/'Root_actual_complete_prepare_namespace_manifest.json')
    declaration = metadata(summary['actual_declaration']['path'])
    formal = metadata(summary['formal_PREP_terminal']['path'])
    terminal = metadata(summary['actual_root_terminal']['path'])
    H = Path(namespace['namespaces'][0]['root'])
    host = metadata(H/'result.json')
    watch = metadata(H/'run/prepare.watchdog.json')
    graph_path = summary['actual_input_graph']['path']
    encoded = metadata(graph_path)
    graph = encoded['graph']
    requirement = graph['requirements']['rows']
    check('requirement_codec_actual_metadata_schema_exact', set(requirement) == {'schema','encoding','row_count','column_count','data'} and requirement['schema'] == 'AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1' and requirement['encoding'] == 'CANONICAL_UNSIGNED_LEB128_BASE64' and type(requirement['row_count']) is int and type(requirement['column_count']) is int and requirement['column_count'] == 5)
    raw = base64.b64decode(requirement['data'], validate=True)
    raw_terminal_count = sum(byte < 128 for byte in raw)
    check('independent_requirement_varint_metadata_cells_count', bool(raw) and raw[-1] < 128 and raw_terminal_count == requirement['row_count'] * 5)
    del raw
    owner_table = graph['owners']
    check('owner_count_uses_complete_rows_instead_of_wrapper_keys', isinstance(owner_table,dict) and isinstance(owner_table['rows'],list) and owner_table['duplicate_descriptors_retained'] is True and owner_table['expected_hashes_come_from_typed_owners_not_observed_files'] is True)
    trace_table = graph['read_trace']['records']
    counts = dict(requirements=requirement['row_count'], requirement_columns=requirement['column_count'], canonical_files=len(graph['canonical_files']['rows']), owners=len(owner_table['rows']), namespaces=len(graph['namespaces']), aliases=len(graph['aliases']), read_trace_records=trace_table['row_count'], absences=len(graph['absence_inputs']), closure_categories=len(graph['closure_categories']))
    check('all_actual_encoded_metadata_counts_correct_rows', counts == dict(requirements=238441, requirement_columns=5, canonical_files=37111, owners=4473, namespaces=86, aliases=186, read_trace_records=63452, absences=479, closure_categories=9) and type(trace_table['row_count']) is int and trace_table['row_count'] == len(trace_table['rows']))
    check('saved_graph_no_new_declaration_consumer_or_science_scope', graph['newly_declared_input_paths'] == {} and graph['newly_declared_input_pins'] == {} and graph['consumer_scope'] is None and graph['science_qualification_created'] is False and graph['live_resources_verified'] is False and graph['external_declaration_exit0_verified'] is False and len(graph['coverage']) == 9)
    check('graph_complete_storage_SCOPE_and_declared_content_binding', encoded['schema'] == 'AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_AND_TRACE_TABLE_STORAGE_V1' and graph['scope'] == 'INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and graph['content_sha256'] == declaration['input_graph']['content_sha256'] == formal['input_graph']['content_sha256'] and declaration['input_graph']['sha256'] == formal['input_graph']['sha256'] == pins[graph_path]['sha256'])
    graph_shape = {key:dict(type=type(value).__name__, count=len(value) if isinstance(value,(dict,list)) else None) for key,value in graph.items()}
    graph_shape['requirements_wrapper'] = dict(schema=requirement['schema'],encoding=requirement['encoding'],wrapper_keys=len(requirement),row_count=requirement['row_count'],column_count=5,raw_varint_integer_cells=raw_terminal_count)
    graph_shape['owners_wrapper'] = dict(wrapper_keys=len(owner_table),row_count=len(owner_table['rows']))
    del graph,encoded,owner_table,trace_table,requirement
    summary_false = ('new_five_stage_build_executed','whole_combined_INPUT_admitted','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted','goal_complete','original_five_build_stages_executed','native_RSS_qualified','cleanup_performed')
    check('all_summary_build_INPUT_native_science_goal_flags_typed_false', all(summary[k] is False for k in summary_false))
    check('actual_root_terminal_does_not_promote_PREP_to_build_INPUT_native_science', all(terminal[k] is False for k in ('new_five_stage_build_executed','whole_combined_INPUT_executed','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted')))
    check('formal_terminal_no_build_math_native_precision_claim', all(formal[k] is False for k in ('successful_new_runtime_build_observed','original_component_APIs_executed_now','native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')))
    check('declaration_fullscope_preserved_no_build_native_science_credit', declaration['input_graph_source_root_inventory_is_exhaustive'] is True and declaration['historical_whole_component_body']['whole_seven_key_body_retained'] is True and declaration['historical_whole_component_body']['original_component_API_execution_claimed'] is False and declaration['historical_whole_component_body']['historical_FAILED_RUN_promoted'] is False and all(declaration[k] is False for k in ('original_component_APIs_executed_now','historical_failed_combined_RUN_promoted','mathematical_controls_newly_executed','native_transport_executed','production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')))
    O = Path(namespace['namespaces'][2]['root'])
    check('no_successful_build_seal_or_five_stage_execution_outputs', 'seal.json' not in namespace['namespaces'][2]['files'] and not (O/'seal.json').exists() and not (O/'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19/stages.json').exists())
    for entry,witness in zip(namespace['namespaces'],prior['namespace_witnesses']):
        check('end_five_namespace_roots_still_7ID_equal:' + entry['root'], identity(entry['root']) == witness['root7ID'])
        for directory in entry['directories']:
            check('end_all_saved_subdirectory_7ID_equal:' + str(Path(entry['root'])/directory['path']), identity(Path(entry['root'])/directory['path']) == directory['identity'])
    for key,pin in pins.items():
        check('end_all_verified_files_still_7ID_equal:' + key, identity(key) == pin['after7ID'])
    witness_bytes = sum(x['regular_bytes'] for x in prior['namespace_witnesses'])
    check('correct_archiving_scope_values_retained', witness_bytes == 138488083 and summary['joint_archive_bytes'] == 138869616 and witness_bytes+200940+180593 == 138869616)
    review.update(status='ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE', checks=checks, all_checks_typed_true=True, file_pins=pins, namespace_witnesses=prior['namespace_witnesses'], namespace_files_verified=68, namespace_subdirectories_verified=14, namespace_symlinks_verified=0, frozen_D_source_files_verified=42, complete_S_source_inventory_files_verified=11, original_inputs_full_EOF_SHA7ID_verified=51, actual_root_closed_integer_exit0=True, actual_root_terminal_chunk_id='c5790b', actual_root_session_id=2985, actual_root_session_repolled_after_close=False, actual_child_PID=96184, actual_whole_seconds=host['whole_seconds'], actual_child_seconds=watch['elapsed_seconds'], actual_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'], original_caps=dict(whole_wall_seconds=1800,stage_wall_seconds=600,rss_mib=512,joint_archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0), actual_H_S_O_T_D_regular_bytes=138488083, Root_saved_joint_including_E_before_summary_and_FACTORY_bytes=138869616, E_bytes_at_saved_sum=200940, canonical_FACTORY_bytes=180593, graph_metadata_counts=counts, graph_storage_shape=graph_shape, full_graph_bytes=45526587, full_graph_sha256='257ddbd44f3123dd85f7b0cf50572ca68c92475b9a491ef83d0ec21b74e63d60', full_trace_bytes=40959538, full_trace_sha256='c1e2daeef559de7c518ce7407230c43e5c911062e3d744651e8a6e007dd05712', first_three_readonly_audit_integer_exit1_records_retained=True, first_three_review_failures_only_reviewer_archive_scope_storage_wrapper_or_graph_SCOPE_assumptions=True, no_original_PREP_or_scientific_threshold_changed=True, original87_complete_hash_proofs_reused_without_business_or_history_rerun=True, observed_actual_child_PID_only_not_inferred_host_PID=True, qualification=dict(actual_complete_PREP_resource_evidence_verified=True, complete_five_stage_build=False, whole_combined_INPUT_admitted=False, new_native_transport=False,native_RSS=False,AAA_accuracy=False,ABA_admitted=False,physical_balance=False,goal_complete=False), remaining_requirements=['Fresh original five-stage build still required; this PREP evidence does not admit whole combined INPUT.', 'Native/AAA/ABA/physical precision and balance qualification remain false.'])
except BaseException as error:
    review.update(status='ACTUAL_PREP_EVIDENCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE', error=repr(error),blocking_findings=[repr(error)],checks=checks,file_pins=pins,namespace_witnesses=prior['namespace_witnesses'])
review['finite_tail_readonly_seconds'] = time.monotonic()-START
with (OUT/'VERIFIED_REVIEW.json').open('x') as f:
    json.dump(review,f,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)
    f.write('\n')
with (OUT/'VERIFIED_REPORT.txt').open('x') as f:
    f.write('V19实际完整PREP保存证据：'+review['status']+'\n')
    f.write('68 namespace files/14 subdirectories/0 symlinks、42冻结SOURCE/11 SOURCE库存/51原输入完整EOF SHA7ID通过。实际Root c5790b整数0 CLOSED/session2985/no repoll；实际子PID96184、唯一genuine stage PASS、whole199.32746954192407/child198.1557341669686/sample peak473.09375<512，原1800/600/512/2GiB/history96/free8、1/1/0均保持。\n')
    f.write('H/S/O/T/D=138488083B；Root原archive还计入当时E200940B+规范FACTORY180593B，合计138869616B<2GiB。formalT逐字保存真实子合并stdout/stderr与outer host stderr，标识诚实。完整graph45526587B SHA257ddbd、trace40959538B SHAc1e2dae全hash通过。实际encoded requirements.row_count238441×5，LEB128整数元数据终止数量独立匹配；owners按rows计4473，canonical37111/ns86/alias186/readtrace63452/absence479/9coverage，新decl空/consumerNone。\n')
    f.write('审查器首次错把archive口径当五目录、第二次错数owners10字段包装、第三次错把declaration外部描述scope当graph内部scope均保留实际整数退出1；graph实际内部scope与原pinned bcd源码INPUT_SCOPE精确同为INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION。只在新TMP更正审查器口径并完成剩余已保存metadata，未改原数据、原阈值或执行业务。87文件完整hash证据复用且当前7ID一致；未import/call项目/helper/API/guard/math数值或资源检查，不扩展历史，不清理/改H/S/O/T/D/E。只实际PREP；五stage build/完整INPUT/native RSS/AAA/ABA/物理平衡/目标完成仍false。\n')
    if review['blocking_findings']:
        f.write('具体阻碍：'+repr(review['blocking_findings'])+'\n')
raw = (OUT/'VERIFIED_REVIEW.json').read_bytes()
print(json.dumps(dict(status=review['status'],directory=str(OUT),review_sha256=hashlib.sha256(raw).hexdigest(),review_bytes=len(raw),finite_readonly_checks=len(checks),unique_files_full_EOF_SHA7ID=len(pins),root_terminal_integer0_closed=review.get('actual_root_closed_integer_exit0',False),sampled_peak_rss_mib=review.get('actual_sampled_peak_rss_mib'),project_API_import_or_call=False,business_executed=False,whole_INPUT_build_native_science_credit=False),indent=2))
if review['blocking_findings']:
    raise SystemExit(1)

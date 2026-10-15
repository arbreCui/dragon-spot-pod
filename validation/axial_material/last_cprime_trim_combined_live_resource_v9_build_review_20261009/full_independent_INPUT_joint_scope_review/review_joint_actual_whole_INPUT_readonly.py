import hashlib
import json
import os
import stat
from pathlib import Path

O = Path('/private/tmp/axmat_v9_actual_whole_INPUT_joint_scope_binding_review_20261009')
SP = Path('/private/tmp/spot_v9_actual_bound_INPUT_source_witness_math_independent_review_20261009')
GP = Path('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009')
R9 = Path('/Users/wen/spot/validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009')
D = Path('/Users/wen/spot/validation/artifacts/axial-material-owned-specs-trim-v9-standalone-bounded-runtime-api-intake-evidence-20261009')
R14 = Path('/Users/wen/spot/validation/storage_cleanup_fourteenth_20261009')
PINS = {}


def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]


def pin(p, expected=None):
    p = Path(p)
    before = identity(p)
    assert stat.S_ISREG(before[2]) and before[-1] == 1 and p.resolve() == p
    h = hashlib.sha256()
    with p.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink] == before
        while chunk := stream.read(1024 ** 2):
            h.update(chunk)
    assert identity(p) == before
    result = dict(path=str(p), sha256=h.hexdigest(), size_bytes=before[3], identity=before)
    if expected is not None:
        assert result['sha256'] == expected
    PINS[str(p)] = result
    return result


def pairs(items):
    d = {}
    for k, v in items:
        assert k not in d
        d[k] = v
    return d


def read(p, expected=None):
    bound = pin(p, expected)
    result = json.loads(Path(p).read_text(), object_pairs_hook=pairs)
    assert identity(p) == bound['identity']
    return result


def true0(tool, expected):
    assert tool == expected
    assert type(tool['exit_code']) is int and tool['exit_code'] == 0 and tool['closed'] is True


assert __debug__
s = read(SP / 'REPORT.json', 'c19a572f913f06339e6d8fdb16d143f15eab3b2aa2ae5268e77335b7562a4147')
st = read(SP / 'actual_readonly_tool_return.json', 'd73ea46c5ac23bbe664aba1a80098ca694a4ca7a3bc32431d9a8dd61091a8b78')
g = read(GP / 'complete_graph_and_whole_returned_INPUT_review.json', 'defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')
gt = read(GP / 'actual_readonly_full_INPUT_review_tool_return.json', '7031ba726192399afedb53cd4d58b4a70ae92cbd7e28e19d8358c379e179e41e')
assert s['status'] == g['status'] == 'PASS'
assert st['report']['sha256'] == PINS[str(SP / 'REPORT.json')]['sha256']
assert st['report']['path'] == str(SP / 'REPORT.json')
assert gt['report_pin']['sha256'] == PINS[str(GP / 'complete_graph_and_whole_returned_INPUT_review.json')]['sha256']
assert gt['report_pin']['path'] == str(GP / 'complete_graph_and_whole_returned_INPUT_review.json')
true0(st['actual_tool_result'], dict(chunk_id='dc214c', exit_code=0, closed=True, wall_time_seconds=1.049490708))
true0(gt['actual_tool_result'], dict(initial_chunk_id='e0686e', session_id=9706, terminal_chunk_id='7a5675', exit_code=0, closed=True))
assert st['record_written_after_actual_terminal_return'] is gt['record_written_after_actual_terminal_return'] is True
pin(st['source']['path'], st['source']['sha256'])
pin(g['audit_source_pin']['path'], gt['source_sha256'])
for key in ('full_stdout', 'full_stderr'):
    p = pin(gt[key]['path'], gt[key]['sha256'])
    assert p['size_bytes'] == gt[key]['size_bytes']
assert gt['full_stderr']['size_bytes'] == 0
peer_binding = s['complementary_complete_graph_review']
assert peer_binding['report_path'] == str(GP / 'complete_graph_and_whole_returned_INPUT_review.json')
assert peer_binding['report_sha256'] == PINS[peer_binding['report_path']]['sha256']
assert peer_binding['actual_receipt_path'] == str(GP / 'actual_readonly_full_INPUT_review_tool_return.json')
assert peer_binding['actual_receipt_sha256'] == PINS[peer_binding['actual_receipt_path']]['sha256']
assert peer_binding['actual_tool'] == gt['actual_tool_result']

root = read(D / 'Root_terminal_return.json', '23acbccb31befbba6ae52ffaf80ae119fd3b7341faa263c18a45c0cd239062ba')
host_observation = read(R9 / 'Root_actual_bound_INPUT_host_tool_return.json', 'ed535093a16ab98a897bc3b895189a99a9eff4cb07165ea69d7f720b374a7434')
recorder_observation = read(R9 / 'Root_actual_INPUT_payload_recording_tool_return.json')
host_tool = dict(initial_chunk_id='0a5d42', session_id=11005, terminal_chunk_id='cbbfbe', exit_code=0, closed=True)
recorder_tool = dict(chunk_id='727fd7', exit_code=0, closed=True)
true0(s['Root_host_tool'], host_tool)
true0(s['Root_recorder_tool'], recorder_tool)
true0(host_observation['actual_tool'], host_tool)
true0(recorder_observation['actual_host_tool'], host_tool)
true0(recorder_observation['actual_recorder_tool'], recorder_tool)
assert host_observation['actual_tool_terminal_return_observed'] is True
assert host_observation['written_after_actual_tool_return'] is True
assert recorder_observation['observed_after_actual_recorder_tool_return'] is True
assert recorder_observation['durable_Root_receipt']['sha256'] == PINS[str(D / 'Root_terminal_return.json')]['sha256']
assert recorder_observation['durable_Root_receipt']['path'] == str(D / 'Root_terminal_return.json')
assert root['actual_tool'] == {k: v for k, v in host_tool.items() if k != 'closed'} == g['actual_host_tool_result']
assert type(root['actual_exit_code']) is int and root['actual_exit_code'] == 0
assert root['record_written_after_actual_tool_return'] is root['actual_bounded_runtime_input_admission_observed'] is True
assert g['actual_terminal_int0_closed'] is True
assert s['durable_Root_receipt_sha256'] == g['actual_Root_INPUT_receipt_pin']['sha256'] == PINS[str(D / 'Root_terminal_return.json')]['sha256']
assert g['actual_Root_INPUT_receipt_pin']['identity'] == PINS[str(D / 'Root_terminal_return.json')]['identity']

inventory = root['payload_inventory']
assert len(inventory['files']) == recorder_observation['payload_count'] == s['payload_count'] == 9
assert inventory['symlinks'] == {} and inventory['directories'] == ['STANDALONE_BOUNDED_RUNTIME_API_INTAKE', 'intake', 'runtime']
payload_rows = {row['path']: row for row in recorder_observation['payload_files']}
assert len(payload_rows) == 9
for relative, digest in inventory['files'].items():
    p = D / relative
    fresh = pin(p, digest)
    assert payload_rows[str(p)]['sha256'] == digest and payload_rows[str(p)]['size'] == fresh['size_bytes']
assert sum(PINS[str(D / relative)]['size_bytes'] for relative in inventory['files']) == root['payload_bytes'] == recorder_observation['payload_bytes'] == s['payload_bytes'] == 25886733
log_pin = PINS[str(D / 'intake/admit.log')]
assert log_pin['sha256'] == s['whole_API_log_sha256'] == g['whole_API_return_pin']['sha256'] == '0e5727aee267c24c3a74c387c628b3633a23826e38c41eda1bfe14ecd02872f5'
assert log_pin['size_bytes'] == s['whole_API_log_bytes'] == 25266286
assert log_pin['identity'] == g['whole_API_return_pin']['identity']

summary = host_observation['host_result_summary']
bindings = [('producer', 'factory_sha256', 'original_admitted_factory_pin'),
            ('declaration', 'declaration_sha256', 'declaration_pin'),
            ('actual_PREP', 'PREP_sha256', 'actual_PREP_pin'),
            ('actual_run', 'RUN_sha256', 'actual_RUN_pin'),
            ('build_seal', 'build_seal_sha256', 'build_seal_pin')]
for root_field, source_field, graph_field in bindings:
    bound = summary[root_field]
    assert bound['sha256'] == s[source_field] == g[graph_field]['sha256']
    fresh = pin(bound['path'], bound['sha256'])
    assert fresh['identity'] == g[graph_field]['identity']
assert inventory['files']['host.py'] == s['host_sha256'] == '180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae'
assert inventory['files']['postterminal_recorder.py'] == s['postterminal_recorder_sha256'] == '5bd181e59b3229398ec7725e8513da5cf055791400522935f5ebfc2b9bd0d03e'
for field in ('complete_65key_body_equal_to_all_immutable_original_sources', 'builtin_scalar_container_type_dict_insertion_list_order_and_finite_float64bits_all_preserved', 'all_redundant_inherited_component_bodies_preserved', 'math_FULL_SCOPE_all_fields_retained', 'producer_all65defs_byte_and_AST_exact_to_F8', 'SOURCE11_fresh_fullSHA', 'PREP4_frozen_true0_no_RUN_claim', 'OUT22_whole_seal_and_raw_bytes', 'payload_namespace_and_all_original_copy_fullSHA', 'one_original_9token_3argument_API_once', 'full_hoststdout_result_deeporder_equal', 'hoststderr_truly_empty'):
    assert s[field] is True
assert g['returned_whole_65_field_builtin_type_floatbits_insertion_order_and_values_equal'] is True
assert len(g['field_names']) == len(set(g['field_names'])) == 65
assert s['whole65_semantic_sha256'] == g['actual_whole_return_semantic_sha256'] == g['independent_expected_whole_return_semantic_sha256']
assert s['whole7_semantic_sha256'] == g['whole_seven_original_components_sha256']
assert s['original_trim_key_count'] == g['original_trim_complete_key_count'] == 73
assert s['whole_trim_semantic_sha256'] == g['whole_original_trim_sha256']
assert s['original_parser_unchanged'] is True and s['parser_pooling_not_adopted'] is True
fresh_graph_scope = g['full_fresh_verification']
for key, value in dict(canonical_files_read=35647, actual_bytes_read=35803098221, logical_owner_requirements=235528, exhaustive_namespaces_checked=86, explicit_aliases_checked=186, declared_absence_inputs_checked_before_and_after_bytes=445).items():
    assert fresh_graph_scope[key] == value
assert g['complete_rows'] == 235528 and g['original_graph_canonical_count'] == 35647
assert g['returned_descriptor_files_count'] == 35675
assert len(g['additional_descriptor_endpoints_full_fresh_sha_verified']) == 28
assert g['returned_complete_aliases_count'] == 186
for field in ('complete_descriptor_canonical_union_preserved', 'every_column_symbol_range_canonical_varint_base64_and_order_verified', 'coverage_trace_owner_typed_snapshot_namespace_alias_and_absence_before_after_full_verified', 'all_declared_history_roots_retained', 'current_dynamic_union_independently_derived', 'historical_RUN_file_count_not_reused_as_requirement'):
    assert g[field] is True
assert g['second_saved_full_decoded_row_table_built'] is False
assert g['graph_declared_roots_count'] == 231 and g['current_dynamic_roots_count'] == 232
assert s['current_resource_file_count_not_held_to_old_run_or_host_snapshot'] is True
assert g['full_history_resources']['historical_resource_byte_or_file_count_equality_claimed'] is False
assert g['unchanged_max_json_bytes'] == 67108864
assert s['caps'] == dict(total_wall_cap_seconds=1800, stage_wall_cap_seconds=600, RSS_cap_mib=512, threads=1, children_at_once=1, retries=0)
for key, value in s['caps'].items():
    assert root[key] == value and type(root[key]) is int
assert s['history_budget_bytes'] == g['full_history_resources']['artifact_budget_bytes'] == 103079215104
assert s['minimum_free_bytes'] == g['full_history_resources']['min_free_bytes'] == 8589934592
assert s['reserve_bytes'] == g['full_history_resources']['reserve_bytes'] == 2147483648
for field in ('cold_controller_imported', 'cold_controller_bound', 'cold_prepared', 'physics_or_native_transport_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted'):
    assert root[field] is False
assert s['cold_prepared'] is False and s['new_native_transport_or_fullFLU_or_AAA_or_ABA_qualification'] is False
assert g['cold_prepared'] is False and g['fresh_native_RSS_credit'] is False and g['AAA_accuracy_qualified'] is False and g['ABA_admitted'] is False

storage_post_path = Path('/private/tmp/spot_storage_fourteenth_exact5_actual_post_independent_review_20261009/REPORT.json')
storage_post = read(storage_post_path, 'addcc7bd663cdea4d138c2cf06ba99a5846fbeffc428fef46b96584d37622589')
storage_tool_path = storage_post_path.parent / 'actual_readonly_tool_return.json'
storage_tool = read(storage_tool_path, '3ac07fcd1fa41f0cf7dad6576cfef88fe02650af59b6e244b0aba8f09a3fc8be')
assert storage_post['status'] == 'PASS' and storage_tool['report_pin']['sha256'] == PINS[str(storage_post_path)]['sha256']
true0(storage_tool['actual_tool_result'], dict(initial_chunk_id='cd1a15', session_id=64813, terminal_chunk_id='f90a1d', exit_code=0, closed=True))
assert storage_post['all5_lexists_absent'] is True
assert len(storage_post['metadata_final9_absent_paths']) == 9
assert storage_post['independent_fingerprint_before'] == storage_post['independent_fingerprint_after'] == storage_post['expectedwholebaseline']
assert storage_post['previous_actual_complete_decompression_PASS_fresh_SHA_bound'] is True
assert storage_post['new_scientific_or_native_RSS_credit'] is False
dependency_path = R14 / 'old_runtime_dependency_review/REPORT.json'
dependency = read(dependency_path, '374b4b0fa403d915175a9bde916bc72ffdbaf0ee9cfb9996fd2b4ecb186d3a2f')
assert dependency['status'] == 'PASS'
pin(R14 / 'old_runtime_dependency_review/current_actual_source_readchain_proof.json', 'a8dd52ed6e2a38e7625078f959a3dd957af9a8b0b96f687f439256a9a22ab292')

for path, bound in PINS.items():
    assert identity(path) == bound['identity']
report = dict(
    schema='AXMAT_V9_GENUINE_STANDARD_WHOLE_INPUT_COMPLEMENTARY_JOINT_ACTUAL_SCOPE_BINDING_V1',
    status='PASS', scope='COMPLETE_STANDARD_3ARG_RUNTIME_WHOLE_INPUT_ONLY',
    source_witness_math_report=PINS[str(SP / 'REPORT.json')], source_witness_math_true_tool=st['actual_tool_result'],
    source_witness_math_tool_receipt=PINS[str(SP / 'actual_readonly_tool_return.json')],
    graph_whole_descriptor_report=PINS[str(GP / 'complete_graph_and_whole_returned_INPUT_review.json')],
    graph_whole_descriptor_true_tool=gt['actual_tool_result'],
    graph_whole_descriptor_tool_receipt=PINS[str(GP / 'actual_readonly_full_INPUT_review_tool_return.json')],
    genuine_Root_host_tool=host_tool, genuine_Root_postterminal_recorder_tool=recorder_tool,
    durable_Root_independent_tenth_receipt=PINS[str(D / 'Root_terminal_return.json')],
    nine_payload_current_fullSHA_bound=True, nine_payload_bytes=25886733,
    whole_API_merged_log_fullSHA_bound=log_pin,
    original65_ordinary_fields_all_types_order_values_floatbits_full_equal=True,
    complete7_original_components_full_equal=True, complete_trim73_fields_full_equal=True,
    whole65_semantic_sha256=s['whole65_semantic_sha256'], whole7_semantic_sha256=s['whole7_semantic_sha256'],
    whole_trim_semantic_sha256=s['whole_trim_semantic_sha256'],
    complete_original_SOURCE11_PREP4_OUT22_witness_scope_bound=True,
    original_all65_producer_definitions_MRO_and_parser_identity_bound=True,
    complete_graph_scope=dict(canonical_files=35647, canonical_bytes=35803098221,
                              typed_requirement_rows=235528, exhaustive_namespaces=86,
                              aliases=186, beforeafter_absences=445, returned_descriptors=35675,
                              additional_descriptor_endpoints=28, declared_resource_roots=231),
    full_graph_coverage_trace_rows_owner_namespace_alias_absence_scope_bound=True,
    preserved_caps=s['caps'], preserved_storage_caps=dict(history_budget_bytes=s['history_budget_bytes'], minimum_free_bytes=s['minimum_free_bytes'], reserve_bytes=s['reserve_bytes'], stored_JSON_max_bytes=67108864),
    R14_actual_cleanup_postcheck=PINS[str(storage_post_path)], R14_actual_cleanup_tool=storage_tool['actual_tool_result'],
    R14_fixed5_readchain_exclusion_and_exact_recovery_master_proof_bound=PINS[str(dependency_path)],
    R14_scientific_inputs_and_payloads_preserved=True,
    resource_observation_policy='231 declared roots retained; dynamic union/caps freshly derived at each consuming phase. The earlier INPUT review observed 232 roots and 51701 files, which are historical observations, not required frozen current file counts. This small joint binding derives no new live inventory after R14.',
    duplicate_compiled_runtime_retirement_does_not_promote_old_failed_results=True,
    complementary_reports_full_scope_reused_no_complete_graph_or_35GB_reverification=True,
    joint_reader_business_API_helper_factory_recorder_imported_or_executed=False,
    project_or_ART_written=False, files_deleted_by_joint_reader=0,
    admission_credit='ACTUAL_COMPLETE_STANDARD_WHOLE_INPUT_ONLY',
    cold_prepared=False, native_transport_or_full_FLU_executed=False,
    AAA_accuracy_qualified=False, ABA_admitted=False, combined_native_RSS_or_memory_cause_proved=False,
    full_read_pins=list(PINS.values()), joint_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with (O / 'REPORT.json').open('x') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(dict(status='PASS', report=str(O / 'REPORT.json'), report_sha256=hashlib.sha256((O / 'REPORT.json').read_bytes()).hexdigest(),
                      complete_whole_INPUT_scope=True, canonical_files=35647, returned_descriptors=35675,
                      admission_credit='ACTUAL_COMPLETE_STANDARD_WHOLE_INPUT_ONLY', full_read_pins=len(PINS))))

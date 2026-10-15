# Pure read-only actual-binding graph/independent expected-owner union review.
# No producer or graph helper import; no API/constructor/phase invocation.
import ast, base64, copy, hashlib, json, math, os, stat, shutil, struct, time
from pathlib import Path
TMP = Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
T = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
HELPER = ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
HELPER_SHA = '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
GRAPH_SHA = '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
WIRE_SHA = 'f91b0168754de2d1e207eda794bd5b4ecd143f84c53f58c27fbb7d45e24ff946'
LEGACY_SHA = 'e9634f406032b9872240ae0be7abd28159389146fa020494d03a4787264b05d2'
FACTORY_SHA = '44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
DECL_SHA = '7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0'
PREP_SHA = '0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'
SEAL_SHA = 'ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed'
RUN_SHA = '709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27'
INPUT_SPECS_SHA = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
PREFIX = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V9'
PINS = {}
START = time.monotonic()
def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(path, sha=None):
    path = Path(path)
    before = identity(path)
    assert stat.S_ISREG(before[2]) and path.parent.resolve(strict=True) == path.parent
    h = hashlib.sha256()
    with path.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino] == before[:2]
        while block := stream.read(4 * 1024**2):
            h.update(block)
    assert identity(path) == before
    record = dict(path=str(path), identity=before, size=before[3], sha256=h.hexdigest())
    if sha:
        assert record['sha256'] == sha, str(path)
    PINS[str(path)] = record
    return record

def read_json(path, sha=None):
    record = pin(path, sha)
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, ('duplicate key', str(path), key)
            result[key] = value
        return result
    def floating(text):
        value = float(text)
        assert math.isfinite(value)
        return value
    def reject(text):
        raise ValueError('nonfinite JSON literal: ' + text)
    value = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_float=floating, parse_constant=reject)
    assert identity(path) == record['identity']
    return value

def canonical_pieces(value):
    return json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).iterencode(value)

def digest(value):
    result = hashlib.sha256()
    for text in canonical_pieces(value):
        result.update(text.encode('utf-8'))
    return result.hexdigest()

def main():
    source_dir=Path('/private/tmp/spot_v9_cold_actual_binding_full_source_independent_review_20261009')
    graph=read_json(TMP/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
    greceipt=read_json(TMP/'actual_readonly_tool_return.json','34075c6b3c6f0e4197ab6e5ea93bd16b615ca25a3b38f6b57af87b6d8edaa1dd')
    source=read_json(source_dir/'REPORT.json','bfaf98e2a9038c0b1634f2a49be90fdacb025aed8c2bcf1e6adc3534cfb772f7')
    sreceipt=read_json(source_dir/'actual_readonly_tool_return.json','74b9172fc5e3e111e2314004f353d71bf4744cd73f99f0ef9120bd7ea391a03b')
    assert graph['status']==source['status']=='PASS'
    assert greceipt['actual_tool_result']==dict(initial_chunk_id='9a9803',session_id=71255,terminal_chunk_id='c050ac',exit_code=0,closed=True)
    assert type(greceipt['actual_tool_result']['exit_code']) is int
    assert greceipt['reader_report']['sha256']==PINS[str(TMP/'REPORT.json')]['sha256']
    st=sreceipt['actual_tool_result'];assert st['initial_chunk_id']==st['terminal_chunk_id']=='1fb2f1' and st['session_id'] is None and type(st['exit_code']) is int and st['exit_code']==0 and st['closed'] is True
    assert sreceipt['report']['sha256']==PINS[str(source_dir/'REPORT.json')]['sha256']
    for item in (greceipt['reader_source'],greceipt['full_stdout'],greceipt['full_stderr'],sreceipt['reader_source']):pin(item['path'],item['sha256'])
    assert Path(greceipt['full_stderr']['path']).stat().st_size==0 and sreceipt['actual_stderr']==''
    for item in (graph['Root_observer'],graph['actual_binding_receipt'],graph['prior_full_PREP_admission']):pin(item['path'],item['sha256'])
    obs=read_json(graph['Root_observer']['path'],graph['Root_observer']['sha256'])
    receipt=read_json(graph['actual_binding_receipt']['path'],graph['actual_binding_receipt']['sha256'])
    realtool=dict(initial_chunk_id='ce453a',session_id=31625,terminal_chunk_id='13d167',exit_code=0,closed=True)
    assert graph['actual_binding_Root_tool']==source['actual_binding_tool']==obs['actual_tool_result']==realtool and type(realtool['exit_code']) is int
    assert graph['actual_success_recorder_tool']==obs['actual_success_recorder_tool']==dict(chunk_id='2169ff',exit_code=0,closed=True)
    assert type(receipt['returncode']) is int and receipt['returncode']==0 and receipt['transport_started'] is False and receipt['scientific_qualification'] is False
    assert graph['actual_binding']['sha256']==source['binding_sha256']==obs['actual_binding']['sha256']=='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930'
    assert graph['actual_binding_receipt']['sha256']==source['binding_terminal_sha256']=='d26300e92fc469bc1674f5c788b8806656791da817019d99d12daf6f912af1b1'
    assert source['Root_observer_sha256']==graph['Root_observer']['sha256']=='c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98'
    assert source['qualified_complete_PREP_admission_sha256']==graph['prior_full_PREP_admission']['sha256']=='8fd5bd7965cb61030ce5423b642d5356267818694dc90935ba62f09c0f9e33c3'
    # Cross close the source review's 15 explicitly pending module expected
    # owners with the independently derived complete 37395-map proof. Do not
    # compute arbitrary current source SHA and install it as an expected owner.
    source_root=Path(graph['actual_binding']['path']).parent
    admission_path=Path(next(p for p in graph['additional_expected_files'] if p.endswith('/rank1_factor_cache_admission.json') and '/runtime/' not in p))
    m=read_json(admission_path,graph['additional_expected_files'][str(admission_path)])
    assert len(m['files'])==37339
    expected=dict(m['files']);expected.update(graph['additional_expected_files'])
    assert len(expected)==37395 and digest(expected)==graph['expected_files_whole_sha256']
    extras=source['additional_module_owners_needing_complementary_independent_guard_ownerunion'];assert len(extras)==15
    for row in extras:assert expected[row['path']]==row['sha256'],row['module']
    assert graph['all_module_owners_count']==source['all_recorded_module_owners_fullSHA_and_canonical_paths']==391 and graph['all_module_owners_expected_independent'] is True
    assert graph['expected_files_complete_insertion_order_equal'] is True and graph['binding_self_file_excluded'] is True
    assert graph['no_arbitrary_current_module_fresh_SHA_used_as_expected'] is True
    for flag in ('binding_all24_AST_top_fields_original_order','original_SOURCE31_fullSHA_namespace','full1860_expected_environment_pins_and_whole_environment_body_preserved','original_PREP43_fullSHA_and_new_binding_only_added_to_output','runtime31_exact_flat_namespace_and7_preloads','all6_prior_guard_files_exact_original_order_fullSHA','entire_original_SerialExecutor_class_and_qualifyABA_resource_monitor_bytes_equal','compile_business_source_but_never_exec_or_imported_it','whole_metadata_math_dtype_layout_original_source_contract_unchanged','all_pins_identity_before_after_stable'):assert source[flag] is True,flag
    assert source['producer_compile_python']=='3.14.4' and len(source['all11_compiled_callable_hashes_independently_source_compiled_under_original_Python'])==11
    for flag in ('whole65_complete_type_order_values_floatbits_equal','original_API_raw65_order_unchanged','strict_sorted_consumer_materialization_boundary_exact','new_actual_component_returns7_complete_type_order_floatbits_equal','full_dtype_layout_owner_trace_graph_content_unchanged','resources_before_after_complete_inventory_equal','strict_reservation_gate_passed','future_controls_prepared_cold_and_native_outputs_absent'):assert graph[flag] is True,flag
    assert graph['canonical_files']==35647 and graph['inherited_canonical_bytes']==35803098221 and graph['fresh_canonical_payload_content_reads']==0
    assert graph['requirement_rows']==235528 and len(graph['namespaces_before_after86'])==86 and graph['aliases_absences_before_after']['aliases']==186 and graph['aliases_absences_before_after']['absence_inputs']==445
    assert graph['metadata_dependency_count']==37339 and graph['API_descriptor_union35675_retained'] is True
    assert graph['expected_files_count']==37395 and graph['new_expected_files_count']==56 and graph['dynamic_current_roots_count']==236
    assert graph['history_budget_bytes']==96*2**30 and graph['min_free_bytes']==8*2**30 and graph['fresh_AAA_reserve_bytes']==20971764748
    assert graph['current_resources_before']==graph['current_resources_after']
    # Fresh small metadata identity binding of the complete two evidence sets.
    for p,row in graph['full_read_pins'].items():assert identity(p)==row['identity'],p
    for row in source['all_fresh_pins']:assert identity(row['path'])==row['identity'],row['path']
    for flag in ('new_binding_fixtures_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'):assert source[flag] is False,flag
    assert graph['new_binding_fixtures_executed'] is False and graph['native_RSS_credit'] is False and graph['scientific_qualification'] is False
    assert source['actual_execve_syscall_argv_observation'] is None and graph['actual_execve_syscall_argv_trace_saved'] is False
    for p,row in PINS.items():assert identity(p)==row['identity']
    result=dict(schema='AXMAT_V9_ACTUAL_COLD_BINDING_WHOLE_COMPLEMENTARY_SOURCE_GRAPH_SCOPE_BINDING_V1',status='PASS',
        scope='Both actual readonly complete scopes jointly close genuine canonical binding INPUT only. No control fixture/native/cold/scientific execution or credit.',
        graph_report=PINS[str(TMP/'REPORT.json')],graph_actual_reader_tool=greceipt['actual_tool_result'],graph_actual_reader_receipt=PINS[str(TMP/'actual_readonly_tool_return.json')],source_report=PINS[str(source_dir/'REPORT.json')],source_actual_reader_tool=st,source_actual_reader_receipt=PINS[str(source_dir/'actual_readonly_tool_return.json')],
        actual_Root_binding_tool=realtool,actual_Root_binding_recorder=obs['actual_success_recorder_tool'],actual_binding=graph['actual_binding'],actual_binding_terminal=graph['actual_binding_receipt'],actual_Root_observer=graph['Root_observer'],actual_full_PREP_admission=graph['prior_full_PREP_admission'],
        whole_scope_complementary_reports_pass=True,all24binding_fields_original_order_and_original_caps_pass=True,whole65_original7_and_trim73_plus_new7_complete_source_order_types_floatbits_pass=True,SOURCE31_environment1860_OUTPUT45_runtime31_preload7_guard6_complete=True,complete_expected_files=37395,additional_expected_files=56,all391_module_owners_independently_expected=True,source_peer15_pending_owner_expectations_closed=extras,all11_compiled_originalPython314_callable_hashes_independently_source_equal=True,
        canonical_files=35647,inherited_full_canonical_bytes=35803098221,new_canonical_payload_content_reads=0,all235528rows_86namespaces_186aliases_445absences_complete=True,complete_mfiles37339_API_descriptor35675_retained=True,declared_dynamic_roots=236,review_window_current_resources=graph['current_resources_after'],resource_fresh_counts_are_observations_not_future_frozen_gate=True,history_budget_bytes=96*2**30,min_free_bytes=8*2**30,fresh_AAA_reserve_bytes=20971764748,binding_no_self_file_pin=True,
        new_binding_fixtures_executed=False,native_RSS_verified=False,cold_transport_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,
        source_derived_handoff_not_actual_execve_syscall_trace=True,business_or_graph_helper_imported=False,business_API_constructor_phase_or_native_executed=False,project_formal_ART_written=False,only_TMP_evidence_written=True,elapsed_seconds=time.monotonic()-START,full_small_pins=PINS)
    with(TMP/'joint_scope_binding.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status='PASS',source15_pending_expectations_closed=15,complete_expected_files=37395,module_owners=391,actual_root_binding='ce453a/31625->13d167 true0',scientific_qualification=False),sort_keys=True),flush=True)

if __name__=='__main__':main()

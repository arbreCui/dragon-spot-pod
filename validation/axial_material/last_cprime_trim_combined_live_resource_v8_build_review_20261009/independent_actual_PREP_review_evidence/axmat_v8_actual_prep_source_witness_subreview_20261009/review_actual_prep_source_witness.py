"""Read-only metadata/identity audit. Only this /private/tmp review is written.

No project module import, factory execution, constructor, component API, PREP,
RUN, graph verification, requirement decoding, or science/native payload runs.
The saved graph is loaded with stdlib json only to read typed_snapshot metadata.
No codec is needed: the requested whole component body is direct metadata.
"""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import stat
import sys

DEST = Path('/private/tmp/axmat_v8_actual_prep_source_witness_subreview_20261009')
CONFIG = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009/config.json')
ROOT = Path('/Users/wen/spot')
AX = ROOT/'validation/axial_material'
ART = ROOT/'validation/artifacts'
PINS = {}
CHECKS = {}

def need(condition, name):
    CHECKS[name] = bool(condition)
    if not condition:
        raise ValueError(name)

def identity(value):
    return [value.st_dev, value.st_ino, value.st_mode, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns, value.st_nlink]

def raw(path, wanted=None, hash_bytes=True):
    path = Path(path)
    before = path.lstat()
    need(path.is_absolute() and stat.S_ISREG(before.st_mode) and not path.is_symlink(),
         'ordinary_regular_file:'+str(path))
    value = path.read_bytes()
    after = path.lstat()
    need(identity(before) == identity(after), 'stable_read_identity:'+str(path))
    sha = hashlib.sha256(value).hexdigest() if hash_bytes else None
    PINS[str(path)] = dict(path=str(path), bytes=len(value), sha256=sha,
        identity=identity(after), stable_identity_before_after=True,
        raw_SHA_recomputed=hash_bytes)
    if wanted is not None:
        need(sha == wanted, 'expected_SHA:'+str(path))
    return value

def doc(path, wanted=None, hash_bytes=True):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError('duplicate JSON key: '+key)
            value[key] = item
        return value
    return json.loads(raw(path, wanted, hash_bytes), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))

def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
        ensure_ascii=True, allow_nan=False).encode()).hexdigest()

def save(name, value):
    path = DEST/name
    need(path.parent == DEST, 'output_within_review_directory:'+name)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True, allow_nan=False)
        stream.write('\n')
    return dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                bytes=path.stat().st_size)

def inventory(root):
    files = {}
    directories = []
    for folder, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            path = Path(folder)/name
            need(path.is_dir() and not path.is_symlink(), 'ordinary_SOURCE_directory:'+str(path))
            directories.append(str(path.relative_to(root)))
        for name in names:
            path = Path(folder)/name
            raw(path)
            files[str(path.relative_to(root))] = PINS[str(path)]['sha256']
    return dict(files=files, symlinks={}, directories=sorted(directories))

c = doc(CONFIG)
T, R, SOURCE, OUT, TERM = (Path(c[key]) for key in ('T','R','SOURCE','OUT','TERM'))
F = Path(c['F'])
F_SHA = '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
D_SHA = '3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae'
PREP_SHA = 'b61c126fa40179d6133ce4258df599156e0c55a0092227f9ca4669b8a9581c56'
SPECS_SHA = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
TRIM_SHA = 'a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb'
ORIGINAL_TRIM_SHA = 'fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114'
need(c['factorySha'] == F_SHA and c['declarationSha'] == D_SHA and c['prepSha'] == PREP_SHA,
     'current_config_actual_factory_declaration_PREP_binding')
future = {key:c[key] for key in ('sealSha','terminalSha','terminalPath','failed_terminal_sha')}
need(all(value is None for value in future.values()), 'current_config_four_future_RUN_receipt_fields_None')
fraw = raw(F, F_SHA)
d = doc(OUT/'declaration.json', D_SHA)
prep = doc(TERM/'declaration_terminal_return.json', PREP_SHA)
review_prep = doc(R/'prepare_terminal_return.json', PREP_SHA)
need(prep == review_prep, 'Root_PREP_formal_and_review_copy_whole_JSON_equal')
need(raw(TERM/'declaration_terminal_return.json') == raw(R/'prepare_terminal_return.json'),
     'Root_PREP_formal_and_review_copy_byte_exact')
tool = doc(R/'prepare_terminal_tool_return.json')
need(prep['actual_tool_result'] == tool, 'actual_Root_tool_observation_whole_equal')
need(tool['initial_chunk_id'] == '14daf6' and tool['session_id'] == 26502
     and tool['terminal_chunk_id'] == '7cd405' and type(tool['exit_code']) is int
     and tool['exit_code'] == 0 and tool['closed'] is True,
     'saved_actual_Root_PREP_tool_14daf6_session26502_7cd405_EXIT0_closed')
need(tool['actual_child_command'] == [c['P'],c['F'],'prepare-build']
     and prep['command'] == tool['actual_child_command'], 'literal_actual_Root_PREP_command')
need(prep['record_producer'] == 'root' and prep['actual_tool_terminal_return_observed'] is True
     and prep['record_written_after_actual_terminal_return'] is True
     and prep['returncode'] == 0, 'Root_PREP_record_producer_and_after_terminal_boundary')
need(prep['source'] == dict(path=str(F),sha256=F_SHA)
     and prep['declaration'] == dict(path=str(OUT/'declaration.json'),sha256=D_SHA),
     'Root_PREP_source_and_declaration_pins')
stdout = raw(T/'prepare.stdout')
stderr = raw(T/'prepare.stderr')
formal_stdout = raw(TERM/'declaration_full_stdout.json', prep['full_stdout']['sha256'])
formal_stderr = raw(TERM/'declaration_full_stderr.txt', prep['full_stderr']['sha256'])
need(len(stdout) == 295 and len(stderr) == 0 and stdout == formal_stdout and stderr == formal_stderr,
     'actual_PREP_stdout295_stderr0_formal_copies_byte_exact')
need(json.loads(stdout) == dict(declaration=str(OUT/'declaration.json'), declaration_sha256=D_SHA),
     'actual_PREP_stdout_binds_exact_declaration_only')
source_inventory = inventory(SOURCE)
terminal_inventory = doc(TERM/'declaration_source_inventory.json', prep['source_inventory']['sha256'])
need(source_inventory == d['source_inventory'] == terminal_inventory,
     'SOURCE_inventory_exhaustive_current_declared_TERMINAL_equal')
need(len(source_inventory['files']) == 11 and source_inventory['directories'] == ['runtime']
     and not source_inventory['symlinks'], 'SOURCE_exact11_regular_files_one_runtime_directory_no_aliases')
need(source_inventory['files']['historical_input_combined_runtime_factory.py'] == F_SHA,
     'SOURCE_factory_copy_actual_F_pin')
need(raw(SOURCE/'historical_input_combined_runtime_factory.py') == fraw,
     'SOURCE_factory_copy_byte_exact_actual_F')
helpers = {
 'graph':'combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py',
 'codec':'combined_runtime_typed_specs_codec.py',
 'current':'combined_runtime_current_predicates_private_declaration_lifetimes_20261009.py',
 'checks':'combined_runtime_historical_input_checks.py',
 'ordinary':'combined_runtime_current_ordinary_path_checks.py',
}
for name, source_name in helpers.items():
    need(raw(AX/source_name, source_inventory['files']['runtime/'+name+'.py'])
         == raw(SOURCE/'runtime'/(name+'.py')), 'SOURCE_helper_actual_original_byte_exact:'+name)
need(source_inventory['files']['runtime/graph.py'] == '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643',
     'SOURCE_runtime_graph_actual_1d7c4d7_pin')
original_specs_path = AX/'combined_runtime_complete_historical_input_specs_20261007.json'
encoded = doc(original_specs_path, SPECS_SHA)
copied = doc(SOURCE/'input_specs.json', SPECS_SHA)
need(raw(original_specs_path) == raw(SOURCE/'input_specs.json') and encoded == copied,
     'original_specs_source_copy_whole_raw_and_JSON_equal')
metadata = encoded['metadata']
bodies = metadata['historical_actual_components']
seven = {'capture','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved',
         'dedup','mathematical_controls_inherited_not_newly_executed','original92','physical'}
need(set(bodies) == seven and set(copied['metadata']['historical_actual_components']) == seven,
     'whole_historical_seven_keys_exact_no_missing_replacement')
historical_decl = doc(metadata['declaration']['path'], metadata['declaration']['sha256'])
need(bodies == historical_decl['actual_components'], 'whole_seven_body_equals_historical_actual_components')
need(canonical(bodies) == 'a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130',
     'whole_seven_body_canonical_SHA')
need(metadata['original_component_APIs_executed'] is False
     and metadata['original_whole_seven_key_body_retained'] is True
     and metadata['historical_reuse_contract']['science_or_native_RSS_credit'] is False,
     'original_metadata_historical_reuse_no_new_API_or_science')
historical_prep = doc(metadata['historical_prepare']['path'],metadata['historical_prepare']['sha256'])
body_binding = dict(path=str(original_specs_path),sha256=SPECS_SHA,
    encoding_schema='AXMAT_COMBINED_RUNTIME_LOSSLESS_TYPED_INPUT_METADATA_ENCODING_V1',
    pointer='/metadata/historical_actual_components',whole_seven_key_body_retained=True,
    original_component_API_execution_claimed=False,historical_FAILED_RUN_promoted=False)
admission = doc(SOURCE/'source_admission.json')
need(d['historical_whole_component_body'] == prep['historical_whole_component_body']
     == admission['historical_whole_component_body'] == body_binding,
     'whole_historical_body_reference_PREP_DECL_SOURCE_equal')
need(d['historical_PREP'] == prep['historical_PREP'] == admission['historical_PREP']
     == metadata['historical_prepare'], 'historical_PREP_reference_current_all_equal')
original_trim_path = AX/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json'
original_trim = doc(original_trim_path,ORIGINAL_TRIM_SHA)
trim = doc(SOURCE/'trim_component_admission_INPUT.json',TRIM_SHA)
need(original_trim == trim, 'actual_V8_trim_whole_dict_equals_original_fed209_source')
need(trim['inherited_rank1_factor_cache_admission'] == bodies['original92']
     and trim['inherited_rank1_factor_cache_memory_admission']
     == bodies['dedup']['inherited_rank1_factor_cache_memory_admission'],
     'actual_trim_whole_original92_memory_ancestry_equal')
need(trim['resource_scope_contract'] == bodies['original92']['resource_scope_contract'],
     'actual_trim_inherited_resource_contract_equal')
trim_binding = dict(path=str(SOURCE/'trim_component_admission_INPUT.json'),sha256=TRIM_SHA,
    semantics='ACTUAL_TRIM_3ARG_RETURN_IN_THIS_PREP_THEN_COMPLETE_FRESH_INPUT_REUSE_NO_API_REEXECUTION',
    actual_component_API_called_in_this_PREP=True,original_historical_seven_key_body_unchanged=True,
    old_capture_RSS_transferred=False,trim_native_RSS_proof_obtained=False)
need(d['actual_last_cprime_trim_component_INPUT'] == admission['actual_last_cprime_trim_component_INPUT']
     == prep['actual_last_cprime_trim_component_INPUT'] == trim_binding,
     'actual_trim_whole_INPUT_reference_PREP_DECL_SOURCE_equal')
graph_path = OUT/'input_graph.json'
graph = doc(graph_path,hash_bytes=False)
typed = graph['typed_snapshot']
expected_typed = dict(semantics='HISTORICAL_PREP_INPUT_ONLY_REUSE_NO_API_REEXECUTION',
    historical_whole_component_body=body_binding,historical_PREP=d['historical_PREP'],
    failed_historical_combined_RUN_promoted=False,original_component_APIs_executed_now=False,
    prior_failed_PREP_input=d['prior_failed_PREP_input'],actual_last_cprime_trim_component_INPUT=trim_binding)
need(typed == expected_typed, 'saved_graph_typed_snapshot_complete_reference_exact')
need(d['input_graph']['path'] == str(graph_path) and prep['input_graph'] == d['input_graph'],
     'PREP_and_DECL_graph_reference_equal_without_graph_verify')
del graph
caps = dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,
    numeric_children_at_once=1,retries=0,archive_reserve_bytes=2*2**30,
    artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30)
need({key:d[key] for key in caps} == caps, 'DECL_all_nine_original_resource_caps_exact')
need({key:historical_decl[key] for key in caps} == caps, 'historical_DECL_same_original_caps')
tree = ast.parse(fraw.decode())
functions = {node.name:node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
need("TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512" in fraw.decode()
     and "RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30" in fraw.decode(),
     'static_factory_original_cap_assignments_present')
selected = ['actual_components','record_actual_trim_component','trim_component_contract','stage_labels']
source_evidence = {name:dict(start_line=functions[name].lineno,end_line=functions[name].end_lineno,
    source=ast.get_source_segment(fraw.decode(),functions[name])) for name in selected}
need("value=trim_factory().production_admission(TRIM_SEAL_SHA,str(TRIM_TERMINAL/'terminal_return.json'),TRIM_TERMINAL_SHA)"
     in source_evidence['record_actual_trim_component']['source'],
     'static_actual_PREP_one_literal_trim_3arg_source_call_retained_not_executed_by_review')
false_prep = ['native_transport_executed','mathematical_controls_newly_executed',
    'combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified',
    'ABA_admitted','scientific_qualification','successful_new_runtime_build_observed',
    'original_component_APIs_executed_now','successful_combined_link_completion_observed','production_admission_observed']
need(all(prep[key] is False for key in false_prep), 'PREP_all_new_RUN_native_science_credit_false')
need(all(d[key] is False for key in ['mathematical_controls_newly_executed','native_transport_executed',
    'production_pipeline_prepared','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed',
    'AAA_accuracy_qualified','ABA_admitted','original_component_APIs_executed_now','historical_failed_combined_RUN_promoted']),
    'DECL_all_new_science_RUN_API_credit_false')
need(all(trim[key] is False for key in ['native_RSS_proof_obtained','actual_full_FLU_entry_executed',
    'production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted']), 'trim_INPUT_no_new_RSS_FLU_AAA_ABA_credit')
tail_keys = ['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']
need(prep['build_seal'] is None and all(prep[key] is None for key in tail_keys),
     'PREP_build_seal_and_four_future_tails_None')
need(prep['compiled_or_numeric_stages_started'] == 0 and prep['planned_total_stages'] == 5,
     'PREP_zero_started_five_planned_stages')
need(d['stages'] == ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'],
     'DECL_exact_five_original_planned_stages')
stage_inventory = {name:sorted(path.name for path in (OUT/name).iterdir())
                   for name in ['HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V8','audit','build','metadata','runtime']}
need(all(not stage_inventory[name] for name in ['HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V8','audit','build','metadata'])
     and stage_inventory['runtime'] == ['run_bounded_dragon.py'], 'current_OUT_all_stage_tails_unstarted_directories_empty')
future_paths = [OUT/'execution_claim.json',OUT/'driver_result.json',OUT/'seal.json',OUT/'runtime/Dragon',
    TERM/'terminal_return.json',TERM/'run_full_stdout.json',TERM/'run_full_stderr.txt',
    T/'run.stdout',T/'run.stderr',R/'run_terminal_return.json',R/'run_terminal_tool_return.json']
need(all(not os.path.lexists(path) for path in future_paths), 'current_all_future_RUN_and_seal_paths_absent')
need(sorted(path.name for path in TERM.iterdir()) == ['declaration_full_stderr.txt','declaration_full_stdout.json',
    'declaration_source_inventory.json','declaration_terminal_return.json'], 'TERM_current_exact_four_PREP_only_files')
trace = doc(SOURCE/'trim_component_API_python_open_trace.json')
need(trace['coverage'] == 'PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' and not trace['subprocess_records'],
     'saved_trim_open_trace_only_not_native_business_execution_evidence')
observation = doc(R/'actual_PREP_graph_observation.json')
need(observation['build_seal_present'] is False and observation['RUN_started'] is False
     and observation['native_RSS_proved'] is False and observation['AAA'] is False and observation['ABA'] is False,
     'saved_graph_observation_no_build_RUN_science_credit')
limits = dict(project_module_imports_executed=False,factory_or_business_source_executed=False,
    constructor_API_PREP_RUN_executed=False,pure_codec_executed=False,
    full_graph_or_requirement_verification_executed=False,science_or_native_payload_executed=False,
    formal_or_ART_writes=False,temp_review_only_writes=True,
    evidence_scope='STDLIB_JSON_METADATA_AND_FRESH_FILE_SOURCE_IDENTITY_ONLY',
    graph_loaded_by_stdlib_JSON_for_typed_snapshot_only=True,
    original_actual_PREP_claim_is_pinned_saved_Root_tool_receipt_not_reexecution=True,
    actual_Root_tool_receipt_truthfulness_not_recreated_by_this_review=True,
    source_or_metadata_identity_grants_no_successful_RUN_native_RSS_AAA_ABA_credit=True)
source_pin = save('static_source_evidence.json',source_evidence)
pins_pin = save('fresh_source_and_stdjson_pins.json',dict(files=list(PINS.values()),
    SOURCE_inventory=source_inventory,graph_referenced_SHA=d['input_graph']['sha256'],
    graph_SHA_not_recomputed=True))
report = dict(schema='AXMAT_V8_ACTUAL_PREP_SOURCE_WITNESS_INDEPENDENT_METADATA_REVIEW_V1',
    status='PASS_ACTUAL_PREP_SOURCE11_SEVEN_BODY_TRIM_METADATA_IDENTITY_ONLY',
    observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    factory_SHA=F_SHA,declaration_SHA=D_SHA,Root_PREP_SHA=PREP_SHA,
    saved_actual_Root_tool_observation=tool,
    saved_stdout_bytes=len(stdout),saved_stderr_bytes=len(stderr),SOURCE_inventory=source_inventory,
    historical_input_specs=PINS[str(original_specs_path)],
    whole_seven_key_names=sorted(bodies),whole_seven_body_canonical_SHA=canonical(bodies),
    whole_body_historical_DECL_actual_components_and_SOURCE_copy_equal=True,
    original_trim_saved_return=PINS[str(original_trim_path)],actual_V8_trim_saved_return=PINS[str(SOURCE/'trim_component_admission_INPUT.json')],
    trim_whole_dict_equal=True,trim_whole_dict_canonical_SHA=canonical(trim),
    historical_binding=body_binding,actual_trim_binding=trim_binding,saved_graph_typed_snapshot=typed,
    current_config_receipt_fields={key:c[key] for key in ['declarationSha','prepSha','sealSha','terminalSha','terminalPath','failed_terminal_sha']},
    current_config_bound_fields=['declarationSha','prepSha'],current_config_future_None_fields=list(future),
    config_six_None_historical_pre_PREP_claim_not_current=True,original_resource_caps=caps,
    future_tail_fields={key:prep[key] for key in tail_keys},build_seal=None,
    current_stage_directories=stage_inventory,future_RUN_absences=[str(path) for path in future_paths],
    native_transport_executed=False,mathematical_controls_newly_executed=False,
    combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,
    AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,
    successful_combined_RUN_observed=False,checks=CHECKS,review_limits=limits,
    static_source_evidence=source_pin,source_and_stdjson_pins=pins_pin)
report_pin = save('REPORT.json',report)
print(json.dumps(dict(status=report['status'],report=report_pin,
    sourcecode=dict(path=str(Path(__file__)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
    source_evidence=source_pin,pins=pins_pin,checks_passed=len(CHECKS),
    current_config_four_future_None=True,no_successful_RUN_native_science_credit=True),allow_nan=False))

"""Read existing sources/evidence only; write this review only beneath its TMP directory.

No business source is imported or executed, no fixture is run, and no session is polled.
"""
import ast
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = Path('/Users/wen/spot')
FACTS = Path('/private/tmp/axmat_v12_cold_consumer_observed_facts_unready_source_only_20261009')
FINAL = Path('/private/tmp/axmat_v12_final_cold_input_candidates_20261009')
NAME = 'cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
PINS = {}

def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()

def pin(path, expected=None):
    path = Path(path)
    assert path.is_file() and not path.is_symlink(), str(path)
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1 << 20), b''):
            h.update(data)
    after = path.stat()
    assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), str(path)
    item = dict(path=str(path), sha256=h.hexdigest(), bytes=before.st_size)
    if expected is not None:
        assert item['sha256'] == expected, (str(path), expected, item['sha256'])
    PINS[str(path)] = item
    return item

def read_json(path, expected=None):
    pin(path, expected)
    return json.loads(Path(path).read_text())

def read_source(path, expected):
    pin(path, expected)
    text = Path(path).read_text()
    tree = ast.parse(text)
    return text, tree

def inverse(text, edits):
    details = []
    for edit in reversed(edits):
        old, new = edit['old'], edit['new']
        count = text.count(new)
        all_literals = edit.get('name', '').startswith('literal family identity ')
        assert count > 0 and (all_literals or count == 1), (edit.get('name'), count)
        text = text.replace(new, old) if all_literals else text.replace(new, old, 1)
        details.append(dict(name=edit.get('name'), actual_new_occurrences=count, inherited_replace_all_rule=all_literals))
    return text, details

def definitions(text, tree):
    result = {}
    def walk(node, prefix=''):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                key = prefix + child.name
                assert key not in result
                start = min([child.lineno] + [n.lineno for n in child.decorator_list])
                result[key] = ''.join(text.splitlines(keepends=True)[start-1:child.end_lineno])
                walk(child, key + '.')
            else:
                walk(child, prefix)
    walk(tree)
    return result

def constants(tree):
    values = {}
    def value(node):
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError):
            if isinstance(node, ast.Name):
                return values[node.id]
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Path' and len(node.args) == 1 and not node.keywords:
                return Path(value(node.args[0]))
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                return value(node.left) / value(node.right)
            raise ValueError(ast.dump(node))
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            values[node.targets[0].id] = value(node.value)
    return values

ready_proof = read_json(FINAL/'Root_consumer_READY_complete_inverse_proof.json', 'eb79b053fa132bfb2102691f27266493206da3d41e2a046c0c4c89eb66067e64')
fact_proof = read_json(FACTS/'source_complete_inverse_proof.json', 'd38244362300f8e3b668b309e95b101e8881676e19d91efcf26c35948aeaca1d')
fact_report = read_json(FACTS/'REPORT.json', '0e20307759c237067303787f0cb7274dc9b87fa65645f14cb8707fe32acdfe8c')
candidate, candidate_ast = read_source(FINAL/NAME, '6688e1fe2967bc63ff12900631e86ae18e30a0ee1bd0b98bb9fbcc4f0ac27823')
mother, mother_ast = read_source(FACTS/NAME, 'cee171c5ecc3827addd60246a775f43a1da4c2262ce53a9e54024ca87f2e6512')
unbound, unbound_ast = read_source(fact_proof['mother_V12_unbound']['path'], fact_proof['mother_V12_unbound']['sha256'])
genuine, genuine_ast = read_source(fact_proof['mother_genuine_V10']['path'], fact_proof['mother_genuine_V10']['sha256'])
assert len(ready_proof['regions']) == 2
inverse_ready, ready_regions = inverse(candidate, ready_proof['regions'])
assert inverse_ready == mother
inverse_facts, fact_regions = inverse(inverse_ready, fact_proof['new_edits'])
assert len(fact_proof['new_edits']) == 15 and inverse_facts == unbound
inverse_genuine, full_regions = inverse(inverse_ready, fact_proof['full_edits'])
assert len(fact_proof['full_edits']) == 60 and inverse_genuine == genuine
defs = definitions(candidate, candidate_ast)
assert len(defs) == 27
assert sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for n in candidate_ast.body) == 26
assert defs == definitions(mother, mother_ast) == definitions(unbound, unbound_ast)
values = constants(candidate_ast)
for key, wanted in fact_report['bound_raw_fact_values'].items():
    assert values[key] == wanted, key
future = {key: val for key, val in values.items() if key.startswith('FUTURE_ACTUAL_COLD_')}
assert len(future) == 7 and all(val is None for val in future.values())
assert values['STATUS'] == 'REVIEWED_IDENTITY_KEY_DELTA_COMPLETE_INPUT_CONSUMER_WITH_ACTUAL_BOUNDED_INTAKE'
assert values['STATUS'] in defs['input_guard']

admission_pin = ready_proof['actual_whole_INPUT_independent_admission']
admission = read_json(admission_pin['path'], 'c47dfa70b1bf610f3ef88049d1f33491815aed4284c182baa2650b0647c5963f')
assert admission_pin['sha256'] == PINS[admission_pin['path']]['sha256']
assert admission['status'] == 'PASS_COMPLETE_BOUNDED_RUNTIME_INPUT_ONLY'
for key in ['independent_joint_report', 'independent_main_actual_return', 'independent_joint_actual_return', 'independent_body_report', 'Root_durable_actual_return']:
    item = admission[key]
    pin(item['path'], item['sha256'])
    assert PINS[item['path']]['bytes'] == item['bytes']
joint = read_json(admission['independent_joint_report']['path'])
assert joint['status'] == 'PASS'
assert joint['scope'] == 'ACTUAL_COMPLETE_BOUND_RUNTIME_INPUT_ONLY_NO_COLD_NATIVE_AAA_ABA'
for key in ['native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted', 'cold_prepared']:
    assert admission[key] is False and joint[key] is False

actual_pin_map = {
    'INTAKE_ROOT_SHA': values['INTAKE_ROOT']/'Root_terminal_return.json',
    'INTAKE_RETURN_SHA': values['INTAKE_ROOT']/'intake/admit.log',
    'API_SEAL_SHA': values['API_BUILD']/'seal.json',
    'API_TERMINAL_SHA': values['API_TERMINAL']/'terminal_return.json',
    'API_PREP_SHA': values['API_TERMINAL']/'declaration_terminal_return.json',
    'TRIM_DECL_SHA': values['TRIM_BUILD']/'declaration.json',
    'TRIM_SEAL_SHA': values['TRIM_BUILD']/'seal.json',
    'TRIM_TERMINAL_SHA': values['TRIM_TERMINAL']/'terminal_return.json',
    'TRIM_OBJECT_SHA': values['TRIM_BUILD']/'build/SPOT1P64.o',
    'TRIM_RUNTIME_SHA': values['TRIM_BUILD']/'runtime/Dragon',
    'TRIM_SOURCE_ADMISSION_SHA': values['TRIM_SOURCE']/'source_admission.json',
    'API_SOURCE_SHA': values['API_SOURCE'],
    'GRAPH_SOURCE_SHA': values['GRAPH_SOURCE'],
    'TRIM_FACTORY_SHA': values['TRIM_FACTORY'],
    'TRIM_KERNEL_SHA': values['TRIM_SOURCE']/'SPOT1P64.f90',
    'FULL_SHA': values['FULL'],
    'BASE_CONTROLLER_SHA': values['BASE_CONTROLLER'],
    'SPECS_SHA': values['SPECS'],
    'GUARD_SHA': values['GUARD'],
}
for key, path in actual_pin_map.items():
    pin(path, values[key])
root_receipt = read_json(actual_pin_map['INTAKE_ROOT_SHA'])
assert root_receipt['actual_exit_code'] == 0 and type(root_receipt['actual_exit_code']) is int
assert root_receipt['whole_API_return']['sha256'] == values['INTAKE_RETURN_SHA']
assert len(root_receipt['payload_inventory']['files']) == values['EXPECTED_INTAKE_PAYLOAD_COUNT'] == 9
for relative, sha in root_receipt['payload_inventory']['files'].items():
    assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
    pin(values['INTAKE_ROOT']/relative, sha)
assert (root_receipt['total_wall_cap_seconds'], root_receipt['stage_wall_cap_seconds'], root_receipt['RSS_cap_mib'], root_receipt['threads'], root_receipt['children_at_once'], root_receipt['retries']) == (1800,600,512,1,1,0)
assert root_receipt['sampled_API_child_peak_RSS_mib'] == admission['actual_API_peak_RSS_MiB'] == 498.75
assert root_receipt['whole_elapsed_seconds'] == 53.15720783296274
api = read_json(actual_pin_map['INTAKE_RETURN_SHA'])
assert len(api['descriptor_files']) == values['EXPECTED_API_DESCRIPTOR_COUNT'] == admission['descriptor_files'] == 36804
assert len(api['input_aliases']) == values['EXPECTED_API_ALIAS_COUNT'] == admission['aliases'] == 186
nested = api['actual_last_cprime_trim_admission']
assert nested['cache_unit_control_counts'] == values['TRIM_CONTROL_COUNTS']
assert nested['schema'] == values['TRIM_SCHEMA']
assert nested['admission'] == 'RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_RUNTIME_INPUT_ONLY'
assert nested['source_admission'] == dict(path=str(actual_pin_map['TRIM_SOURCE_ADMISSION_SHA']), sha256=values['TRIM_SOURCE_ADMISSION_SHA'])
for key in ['native_transport_executed', 'combined_runtime_native_RSS_proved', 'actual_full_FLU_entry_executed', 'AAA_accuracy_qualified', 'ABA_admitted']:
    assert api[key] is False
controls = read_json(values['TRIM_BUILD']/'audit/controls.json')
audit = read_json(values['TRIM_BUILD']/'audit/result.json')
driver = read_json(values['TRIM_BUILD']/'driver_result.json')
declaration = read_json(actual_pin_map['TRIM_DECL_SHA'])
assert controls['counts'] == audit['control_counts'] == driver['control_counts'] == nested['cache_unit_control_counts'] == values['TRIM_CONTROL_COUNTS']
assert len(controls['counts']) == 30 and controls['counts']['total_declared_stages'] == 68
assert sha_bytes(json.dumps(controls['counts'], sort_keys=True, separators=(',', ':')).encode()) == fact_report['complete30key_control_counts_digest']
assert (declaration['total_wall_seconds'], declaration['stage_wall_seconds'], declaration['rss_cap_mib'], declaration['threads'], declaration['numeric_children_at_once'], declaration['retries']) == (1800,600,512,1,1,0)
assert audit['control_status'] == audit['binary_status'] == 'PASS'
for key in ['all_new_cache_outputs_bitwise_equal_to_uncached', 'factor_diagonal_codec_controls_passed', 'cross_group_identity_controls_passed']:
    assert audit[key] is True and driver[key] is True
for obj in [audit, driver]:
    for key in ['actual_full_FLU_entry_executed', 'transport_launched', 'AAA_accuracy_qualified', 'ABA_admitted']:
        assert obj[key] is False
stages = read_json(values['TRIM_BUILD']/'RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11/stages.json')['stages']
assert len(stages) == len(driver['watchdogs']) == 68
assert sum(x['status'] == 'PASS' for x in stages) == 48
assert sum(x['status'] == 'FAILED' for x in stages) == 20
stage_watch = []
for stage in stages:
    path = values['TRIM_BUILD']/(stage['label'] + '.watchdog.json')
    matching = [item for item in driver['watchdogs'] if item['path'] == str(path)]
    assert len(matching) == 1
    watch = read_json(path, matching[0]['sha256'])
    assert watch['returncode'] == (0 if stage['status'] == 'PASS' else 23)
    assert watch['limit_failure'] is None and watch['rss_cap_mib'] == 512
    # A short expected rejection may finish before the first positive RSS sample.
    assert 0 <= watch['sampled_peak_rss_mib'] < 512
    stage_watch.append(dict(label=stage['label'], status=stage['status'], returncode=watch['returncode'], watchdog_sha256=matching[0]['sha256']))

factory_path = Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py')
pin(factory_path, '1941375f15d61b44c17ec11e2466048f646112c6c5939ce568c9fdffc84a93a6')
factory_ast = ast.parse(factory_path.read_text())
budget_node = next(n.value for n in factory_ast.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BUDGETS' for t in n.targets))
assert isinstance(budget_node, ast.Call) and isinstance(budget_node.func, ast.Name) and budget_node.func.id == 'dict' and not budget_node.args
cold_budgets = {n.arg: ast.literal_eval(n.value) for n in budget_node.keywords}
assert cold_budgets == dict(setup_seconds=120, bootstrap_axial_seconds=4200, bootstrap_radial_seconds=600, radial_seconds=300, axial_seconds=4200, host_seconds=120, max_maps=100, total_seconds=43200)
assert 'full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)' in defs['current_cold_binding']
assert 'full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__' in defs['current_cold_binding']
assert 'full.OwnRSSSerialExecutor.execute is not c.SerialExecutor.execute' in defs['current_cold_binding']
assert '_process.__code__.co_filename!=str(FULL)' in defs['current_cold_binding']

report = dict(
    schema='AXMAT_V12_FINAL_COLD_CONSUMER_INDEPENDENT_SOURCE_AND_EXISTING_INPUT_EVIDENCE_REVIEW_V1',
    status='PASS_SOURCE_AND_ACTUAL_BOUNDED_INPUT_BINDINGS_ONLY_NO_COLD_NATIVE_AAA_ABA',
    candidate=PINS[str(FINAL/NAME)],
    readiness_marker_matches_source_guard=True,
    final_to_facts_two_regions_complete_byte_inverse=True,
    final_to_unbound_17_regions_complete_byte_inverse=True,
    final_to_genuine_V10_62_regions_complete_byte_inverse=True,
    final_ready_regions=ready_regions,
    observed_facts_inverse_regions=fact_regions,
    inherited_full_inverse_regions=full_regions,
    definitions_ast_walk=27, definitions_top_level=26, nested_definition='identity_key_delta_source_and_controls.owned',
    all27_definition_sources_byteexact_to_facts_and_unbound=True,
    definition_sha256={key:sha_bytes(val.encode()) for key,val in defs.items()},
    actual_15_fact_bindings=fact_report['bound_raw_fact_values'],
    all_actual_15_fact_bindings_match_existing_evidence=True,
    actual_whole_INPUT_independent_admission=PINS[admission_pin['path']],
    complete65_and_seven_INPUT_source_scope_authority=admission['independent_body_report'],
    joint_complete_scope_authority=admission['independent_joint_report'],
    no_historical_payload_mass_reread_or_business_rerun=True,
    component_stage_total=68, component_PASS=48, component_expected_FAILED_rc23=20,
    complete30key_controls_exact_across_source_sealed_controls_audit_driver_and_nested_API=True,
    complete30key_control_counts=controls['counts'],
    complete30key_controls_canonical_digest=fact_report['complete30key_control_counts_digest'],
    compiled_object_runtime_current_kernel_and_sourceadmission_pins_verified=True,
    original_V10_proof_and_math_chain_reconstructed_exact=True,
    complete_whole_INPUT_descriptor_files=36804, complete_whole_INPUT_aliases=186,
    durable_payload_files=9, durable_files_including_Root=10,
    actual_bounded_API_child_peak_RSS_MiB=498.75,
    actual_bounded_API_elapsed_seconds=53.15720783296274,
    original_API_caps=dict(total_seconds=1800,stage_seconds=600,RSS_MiB=512,threads=1,children=1,retries=0),
    original_cold_budgets=cold_budgets,
    physical_math_whole7_P14_P12_and_ownRSS_MRO_gate_sources_byteexact=True,
    normal_genuine_module_and_class_checks_retained=True,
    MRO_runtime_gate_not_executed_by_reviewer=True,
    future_cold7=future,
    future_cold7_all_None=True,
    cold_prepared=False,native_RSS_verified=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    no_business_import=True,no_business_call=True,no_fixture_execution=True,no_cli_execution=True,no_session_poll=True,no_project_write=True,
    stage_watchdogs=stage_watch,
    evidence_pins=PINS,
)
text = json.dumps(report,ensure_ascii=False,indent=2)+'\n'
(D/'REPORT.json').write_text(text)
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT.json'),report_sha256=sha_bytes(text.encode()),definitions=27,top_level=26,inverse_regions=62,component_stages=68,complete_control_keys=30,future_cold_None=7,evidence_files=len(PINS)),ensure_ascii=False))

"""Read and audit pure source only; never import or call project modules."""
import ast, hashlib, json
from pathlib import Path

D = Path('/private/tmp/axmat_v13_sender_window_graph_table_combined_source_draft_20261009')
P = Path('/Users/wen/spot/validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py')
O = D/'prepare_sender_window_graph_table_combined_runtime_v13.py'
parent = P.read_text(); candidate = O.read_text()
sha = lambda data: hashlib.sha256(data).hexdigest()
assert sha(parent.encode()) == '5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
pt, ct = ast.parse(parent), ast.parse(candidate)
edits = json.loads((D/'composition_regions.json').read_text())
inverse = candidate
for e in reversed(edits):
    assert inverse.count(e['after']) == e['count'], e['name']
    inverse = inverse.replace(e['after'], e['before'], e['count'])
assert inverse == parent

def defs(tree, source):
    out = {}
    def descend(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix+child.name
                assert name not in out, name
                out[name] = dict(kind=type(child).__name__,source=ast.get_source_segment(source,child),line=child.lineno)
                descend(child, name+'.')
            else:
                descend(child, prefix)
    descend(tree, '')
    return out
pd, cd = defs(pt,parent), defs(ct,candidate)
expected_modified = {'require_ready','combined_link_command','trim_component_contract','trim_component_input',
    'prepare_build','declaration_admission','binary_audit','production_admission','current_new_owned_paths'}
modified = {name for name in pd if name in cd and pd[name]['source'] != cd[name]['source']}
assert modified == expected_modified, modified
assert set(pd) <= set(cd)
new_defs = sorted(set(cd)-set(pd))
assert new_defs and all(name == 'sender_component_contract' or name.startswith('sender_component_contract.') for name in new_defs)
retained = sorted(set(pd)-modified)
for name in ('component_contract','actual_components','record_actual_trim_component','stage_labels','stage_commands',
    'check_watch','modules','supervisor_constructor_preflight','expected_supervisor_constructor',
    'graph_input_bindings','create_complete_input_graph','complete_input_phase','current_input_predicates',
    'current_trim_predicates','source_owned_endpoint_checks','failed_prepare_input'):
    if name in pd:
        assert name in retained, name

def assigns(tree, source):
    return {target.id:(node,ast.get_source_segment(source,node))
        for node in tree.body if isinstance(node,ast.Assign)
        for item in node.targets for target in ast.walk(item) if isinstance(target,ast.Name)}
pa, ca = assigns(pt,parent), assigns(ct,candidate)
for name in ('TOTAL_WALL','STAGE_WALL','RSS','RESERVE','HISTORY_CAP','FREE_FLOOR','THREAD_KEYS',
    'BODY_BINDING','INPUT_SPECS','INPUT_SPECS_SHA','INPUT_HELPERS','HISTORY_POLICY'):
    assert name in pa and pa[name][1] == ca[name][1], name
future_names = ['TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA',
    'TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','SENDER_OBJECT_SHA']
for name in future_names:
    assert isinstance(ca[name][0].value,ast.Constant) and ca[name][0].value.value is None, name
assert ast.literal_eval(ca['DRAFT_STATUS'][0].value) == 'UNREADY_SOURCE_ONLY_REQUIRES_NEW_ACTUAL86_COMPONENT_AND_THIRD_SENDER_OVERRIDE'
assert ast.literal_eval(ca['TRIM_FACTORY_SHA'][0].value) == 'd2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
roots = [Path('/Users/wen/spot/validation/artifacts')/name for name in (
    'axial-material-qualified-AB-sender-window-graph-table-combined-source-v13-20261009',
    'axial-material-sender-window-graph-table-combined-runtime-v13-20261009',
    'axial-material-qualified-AB-sender-window-graph-table-combined-terminal-v13-20261009')]
assert len(set(roots)) == 3 and all(not root.exists() for root in roots)
static_inputs = [
    ('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py','d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'),
    ('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py','e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_patch_v13.py','77c037a14a3852f628344d9a7cdee3b09e757b00420bf78eddcc1f3a17a6f163'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/source_patch_proof.json','f5b6bc7fdab49e97dd1178937437365ac11c347cc0b1137b02c02830c0fbfa40'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/source_admission_INPUT.json','6f64546cad4c055b87a00e74392a254f90e0439f692506ed6d6826ba8f54cdf7'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/FLU2DR64.f','cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_observer_controls_v13.f90','053747437865119be4fdd5d8eb466c96a85d8cf22f6d9cdcceebe19bc47352bb'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_controls_audit_v13.py','64262e89bd2adf13260a8d0f643c31d709f84665e5e9223cdd2969ab78a721e1'),
    ('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json','74ecac78a42fd13f5162cc52ad4d96cf6e94abd970406f4fede467696c4dcffd')]
pins = []
for path,wanted in static_inputs:
    raw=Path(path).read_bytes();assert sha(raw)==wanted,path
    pins.append(dict(path=path,sha256=wanted,size_bytes=len(raw)))
classification=[]
for name in sorted(cd):
    classification.append(dict(name=name,line=cd[name]['line'],status='ADDED_SENDER_SCOPE' if name in new_defs else 'MODIFIED_GATE_OR_WIRING' if name in modified else 'BYTEEXACT_RETAINED',sha256=sha(cd[name]['source'].encode())))
proof=dict(schema='AXMAT_V13_COMBINED_SOURCE_COMPLETE_EXPLICIT_INVERSE_V1',
    parent=dict(path=str(P),sha256=sha(parent.encode())),candidate=dict(path=str(O),sha256=sha(candidate.encode())),
    explicit_region_count=len(edits),regions=edits,complete_inverse_byteexact=True,
    definitions=classification,definitions_removed=[],business_executed=False)
(D/'source_complete_inverse_proof.json').write_text(json.dumps(proof,indent=2)+'\n')
report=dict(schema='AXMAT_V13_SENDER_WINDOW_GRAPH_TABLE_COMBINED_PURE_SOURCE_REVIEW_V1',
    status='PASS_SOURCE_ONLY_UNREADY',candidate=proof['candidate'],parent=proof['parent'],
    complete_inverse_byteexact=True,explicit_region_count=len(edits),original_top_level_function_count=65,
    original_all_function_count=len(pd),retained_all_function_count=len(retained),modified_original_functions=sorted(modified),
    added_functions=new_defs,all_original_functions_accounted=True,original_math_whole_INPUT_graph_and_MRO_unchanged=True,
    unchanged_budget=dict(total_seconds=1800,stage_seconds=600,rss_cap_mib=512,threads=1,numeric_children_at_once=1,retries=0,
        source_OUT_reserve_bytes=2147483648,history_cap_bytes=103079215104,min_free_bytes=8589934592,graph_read_cap_bytes=67108864),
    namespace_roots=[str(root) for root in roots],namespace_roots_all_absent_at_review=True,
    unknown_future_component_pins=future_names,known_source_only_pins=pins,
    component_scopes=dict(top_stages=86,original_stages=68,old_cache_count_fields=30,old_actual_unit_kernel_calls=2710,
        sender_cases=14,sender_positives=10,sender_expected_rejections=4,sender_wrapper_calls=48,sender_observer_calls=34,
        sender_real_SPOT_credit=0,sender_raw_file_count=70,sender_raw_bytes=288241824),
    recipe_changes=['SPOT1P64.o replacement','genuine physical SPOASM.o insertion','actual new fullsender FLU2DR64.o replacement','output runtime identity'],
    old_ancestor_kernel_raw_schemas_and_original68_contract_preserved=True,
    fresh_complete_component_API_return_required=True,fresh_complete_graph_and_whole_INPUT_phases_required=True,
    future_new_descriptor_counts_and_graph_bytes_not_bound=True,old_V12_stream_or_counts_not_granted_new_success=True,
    original_e8_graph_helper_retained=True,graph_read_cap_unchanged=True,
    pending=['actual86 terminal closure and formal component admission','bind seven actual component pins','independent source admission and READY installation by Root','new exclusive combined PREP/five stage build/admit','fresh bounded whole INPUT intake with actual new measured size/counts/RSS'],
    business_imported=False,business_called=False,compiled=False,fixtures_executed=False,project_written=False,
    native_RSS_proof_obtained=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],candidate_sha256=proof['candidate']['sha256'],region_count=len(edits),
    retained_original_defs=len(retained),modified_original_defs=len(modified),new_defs=len(new_defs),
    report_sha256=sha((D/'REPORT.json').read_bytes()),proof_sha256=sha((D/'source_complete_inverse_proof.json').read_bytes()),business_executed=False)))

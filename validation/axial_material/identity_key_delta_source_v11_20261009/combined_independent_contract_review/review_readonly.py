import ast
import hashlib
import json
import os
from pathlib import Path

ROOT = Path('/Users/wen/spot')
DEST = Path('/private/tmp/axmat_v11_combined_independent_contract_review_20261009')
BASE = Path('/private/tmp/axmat_v11_combined_component_contract_source_draft_20261009')
PINS = Path('/private/tmp/axmat_v11_combined_actual_component_pins_unready_source_draft_20261009')
NAME = 'prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.UNREADY.py'
IDENT = Path('/private/tmp/axmat_v11_minimal_combined_cold_retarget_plan_20261009') / NAME
MOTHER = ROOT / 'validation/axial_material/prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py'
ART = ROOT / 'validation/artifacts'
OUT = ART / 'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
SOURCE = ART / 'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'
TERM = ART / 'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009'
checks = []

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def read(p):
    return json.loads(Path(p).read_text())

def check(name, value, evidence=None):
    checks.append(dict(name=name, passed=bool(value), evidence=evidence))
    if not value:
        raise ValueError(name)

def funcs(text, all_nodes=False):
    tree = ast.parse(text)
    nodes = ast.walk(tree) if all_nodes else tree.body
    return {n.name: ast.get_source_segment(text,n) for n in nodes if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}

def inverse(text, edits):
    for e in reversed(edits):
        check('unique_inverse_' + e['name'], text.count(e['new']) == 1)
        text = text.replace(e['new'],e['old'],1)
    return text

src = (PINS / NAME).read_text()
old = (BASE / NAME).read_text()
check('actual_pin_source_sha', sha(PINS/NAME)=='fbf8118ddcf72ae2009abcbe405a7d57979525a31da37f1853dd4389f1702bf6')
check('six_assignments_only_inverse', inverse(src,read(PINS/'actual_six_pin_region_edits.json')) == old)
check('complete23_region_inverse_to711', inverse(src,read(PINS/'complete_17_plus_6_region_edits.json')) == IDENT.read_text())
top = funcs(src)
full = funcs(src,True)
check('65_top_and70_total_bodies_unchanged_after_actual_pins', len(top)==65 and len(full)==70 and top==funcs(old) and full==funcs(old,True))
mother = funcs(MOTHER.read_text())
changed = [n for n in mother if top.get(n)!=mother[n]]
check('only_two_component_contract_functions_changed_from_v10',changed==['trim_component_contract','trim_component_input'],changed)
tree = ast.parse(src)
const = {}
for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        try: const[n.targets[0].id]=ast.literal_eval(n.value)
        except (ValueError,TypeError): pass
check('source_remains_UNREADY', const['DRAFT_STATUS']=='UNREADY_PENDING_ACTUAL_V11_COMPONENT_BUILD_WITNESSES_AND_SOURCE_REVIEW')
actual_report=read(PINS/'REPORT.json')
for role,row in actual_report['actual_component_pins'].items():
    check('actual_pin_'+role,const[role]==row['sha256']==sha(row['path']),row['path'])

d=read(OUT/'declaration.json');seal=read(OUT/'seal.json');ad=read(SOURCE/'source_admission.json')
v=read(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout')
receipt=read(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/Root_actual_formal_admit_tool_terminal_return.json')
check('actual_genuine_admit_root_typed0',type(receipt['returncode']) is int and receipt['returncode']==0 and receipt['actual_tool_terminal_return_observed'] is True)
check('actual_return_new_schema_compatibility_scope_only',v['schema']==const['TRIM_SCHEMA'] and v['admission']==const['TRIM_ADMISSION'])
expected_descriptors = {
    'compiled_kernel':dict(path=str(OUT/'build/SPOT1P64.o'),sha256=const['TRIM_OBJECT_SHA']),
    'compiled_kernel_source':dict(path=str(SOURCE/'SPOT1P64.f90'),sha256=const['TRIM_KERNEL_SHA']),
    'corrected_runtime':dict(path=str(OUT/'runtime/Dragon'),sha256=const['TRIM_RUNTIME_SHA']),
    'actual_external_terminal_evidence':dict(path=str(TERM/'terminal_return.json'),sha256=const['TRIM_TERMINAL_SHA']),
    'source_admission':dict(path=str(SOURCE/'source_admission.json'),sha256=const['TRIM_SOURCE_ADMISSION_SHA'])}
check('all_actual_component_descriptors_match',all(v[k]==x for k,x in expected_descriptors.items()))
check('proof_descriptor_distinct_from_in_memory_complete_proof',v['source_patch_proof']==v['source_admission'])
check('new_success_seal_schema',seal['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1')
check('new_source_admission_schema',ad['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_SOURCE_ADMISSION_V1')
check('actual_caps_unchanged',(d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['threads'],d['numeric_children_at_once'],d['retries'])==(1800,600,512,1,1,0))
check('actual_storage_caps_unchanged',(d['archive_reserve_bytes'],d['artifact_budget_bytes'],d['min_free_bytes'])==(2*2**30,96*2**30,8*2**30))
factor_parent=read(ROOT/'validation/axial_material/factor_diagonal_trim_source_v10_20261009/complete_c0_source_patch_proof.json')
factor=read(ROOT/'validation/axial_material/factor_diagonal_trim_source_v10_20261009/source_patch_proof.json')
edits=read(ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/region_edits.json')
contract=read(ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/component_source_extension/identity_key_delta_contract.json')
identity=dict(schema='AXMAT_RANK1_CROSS_GROUP_INTEGER_IDENTITY_KEY_DELTA_STORAGE_V1',parent_kernel_sha256=const['TRIM_FACTOR_KERNEL_SHA'],candidate_kernel_sha256=const['TRIM_KERNEL_SHA'],complete_inverse_byteexact=True,edits=edits,retained_whole_source_sha256=const['TRIM_IDENTITY_RETAINED_SOURCE_SHA'],contract=contract,actual_controls_executed=False,actual_native_RSS_passed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
proof=dict(factor_parent)
proof.update(inherited_v10_complete_proof=factor_parent,edits=factor_parent['edits']+edits,cross_group_identity_key_delta=identity,candidate_kernel_sha256=const['TRIM_KERNEL_SHA'],delegated_factor_diagonal_helper=dict(path=str(ROOT/'validation/axial_material/rank1_factor_cache_factor_diagonal_trim_patch.py'),sha256=const['TRIM_FACTOR_PATCH_HELPER_SHA']),scope='ORDINARY_RANK1_LOWER_DICTIONARY_TERMINAL_CPRIME_DEAD_FACTOR_DIAGONAL_AND_CROSS_GROUP_INTEGER_IDENTITY_STORAGE_ONLY')
check('independently_reconstructed_full0800_proof_exact',ad['source_patch_proof']==proof)
check('5e_and343e_ancestors_remain_distinct',factor_parent['candidate_kernel_sha256']==const['TRIM_FACTOR_KERNEL_SHA'] and factor_parent['last_cprime_trim']['candidate_kernel_sha256']==const['TRIM_LAST_CPRIME_KERNEL_SHA'] and factor_parent['factor_diagonal_trim']==factor)
kernel=(SOURCE/'SPOT1P64.f90').read_text()
restored=kernel
for e in reversed(edits):
    check('identity_kernel_inverse_unique',restored.count(e['new'])==1)
    restored=restored.replace(e['new'],e['old'],1)
check('actual_source_whole_inverse0800_to5e',hashlib.sha256(restored.encode()).hexdigest()==const['TRIM_FACTOR_KERNEL_SHA'])
check('whole_source_control_contract_exact',ad['control_contract']==d['control_contract'] and ad['cross_group_identity_key_delta']==contract==d['control_contract']['cross_group_identity_key_delta'])
for rel in ('audit/controls.json','audit/result.json','driver_result.json'):
    check('actual_sealed_bytes_'+rel,sha(OUT/rel)==seal['files'][rel])
controls=read(OUT/'audit/controls.json');audit=read(OUT/'audit/result.json');result=read(OUT/'driver_result.json');kc=controls['keycodec_controls']
check('real_68_count_agreement',controls['counts']==v['cache_unit_control_counts']==audit['control_counts']==result['control_counts'])
check('new_stage_counts',all(controls['counts'][k]==n for k,n in {'total_declared_stages':68,'original_factor_diagonal_45_stages_retained':45,'additional_keycodec_driver_build_stages':2,'additional_keycodec_execute_stages':21,'inherited_last_cprime_stages_retained':40,'factor_codec_positive_fixtures':3,'factor_codec_module_negative_calls':4,'factor_codec_public_factor_calls':6,'factor_codec_public_solve_calls':12}.items()))
check('sealed_schema_actual_codec_fields',controls['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_FULL_RAW_CONTROLS_AUDIT_V1' and kc['schema']=='AXMAT_RANK1_CROSS_GROUP_IDENTITY_KEY_CODEC_CONTROLS_AUDIT_V1')
check('sealed68_success_classifications',controls['status']=='PASS' and audit['classification']=='PASS_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY' and result['classification']=='COMPLETE_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY' and result['error'] is None)
check('actual21_codec_counts_and_bytes',(kc['standalone_control_count'],kc['positive_key_count'],kc['positive_stats_count'],kc['expected_negative_actual_rejection_count'])==(21,27,6,20) and (kc['raw_binary_bytes'],kc['raw_manifest_jsonl_bytes'],kc['raw_xabort_bytes'],kc['raw_total_bytes'])==(70792,26930,1000,98722))
check('actual_codec_required_flags',all(kc[k] is True for k in ('actual_codec_controls_passed','complete_input_encoded_positions_anchor_decoded_wordwise_equal','canonical_strict_cost_fallback_zero_delta_two_phase_lifecycle_and_hits_verified','exact_EOF_verified','all_fresh_seven_identity_before_after_equal')) and all(kc[k] is False for k in ('original45_controls_completion_claimed','full_component_build_admission_claimed','actual_full_FLU_entry_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))
check('no_native_or_science_credit',all(v[k] is False for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted')))
check('schema_and_codec_gate_not_compatibility_label_only',all(token in top['trim_component_contract'] for token in ('controls[\'schema\']','result[\'cross_group_identity_controls_passed\']','sealed[\'files\'][\'audit/result.json\']','p!=expected_proof')))
check('genuine_three_argument_call_preserved',top['record_actual_trim_component']==mother['record_actual_trim_component'] and "production_admission(TRIM_SEAL_SHA,str(TRIM_TERMINAL/'terminal_return.json'),TRIM_TERMINAL_SHA)" in top['record_actual_trim_component'])
protected=('actual_components','create_complete_input_graph','complete_input_phase','graph_input_bindings','classes','supervisor_contract','build','production_admission','input_modules')
present=[x for x in protected if x in top and x in mother]
check('seven_body_graph_mro_math_and_budget_logic_preserved',all(top[x]==mother[x] for x in present),present)
report=dict(schema='AXMAT_V11_COMBINED_ACTUAL_COMPONENT_CONTRACT_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_SOURCE_CONTRACT_WITH_ACTUAL_COMPONENT_DATA_ONLY',candidate=dict(path=str(PINS/NAME),sha256=sha(PINS/NAME)),actual_component_return=dict(path=str(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout'),sha256=sha(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout')),checks=checks,defects=[],required_source_corrections=['Update obsolete module docstring reporting six None pins when Root installs READY; preserve both READY and docstring changes in complete inverse proof.'],limits={'business_imports_or_calls':False,'compiled_or_transport_children':False,'new_combined_PREP_RUN_admitted':False,'AAA_accuracy_qualified':False,'ABA_admitted':False},namespace_review='SOURCE sealed inventory and preserved predecessor namespaces retained; OUT sealed exact files/directories retained; terminal complete inventory added as owned INPUT. Actual whole-graph descriptor and alias counts must be freshly derived at genuine PREP, never copied from V10.')
DEST.mkdir(exist_ok=True)
(DEST/'REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],checks=len(checks),report=str(DEST/'REPORT.json'),sha256=sha(DEST/'REPORT.json')),ensure_ascii=False))

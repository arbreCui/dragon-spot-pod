"""Standard-library source generation only. Never import or call business sources."""
import ast
import hashlib
import json
from pathlib import Path

D = Path('/private/tmp/axmat_v14b_streaming_sha_complete_component_source_draft_20261010')
P = Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/complete_component_factory_UNREADY_receipt_size_fixed_source_draft/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py')
O = D / 'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
P13 = Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
P14_PROOF = P.parent / 'COMPLETE_INVERSE_PROOF.json'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

original_bytes = P.read_bytes()
assert sha(original_bytes) == 'e1cbc96cd7c46dc99b2a0a477b609abf70ea0c4338d5d0ed8840165945e5f35a'
assert sha(P14_PROOF.read_bytes()) == 'ded9d5785c69d6fda3d90a2fb1b8f9e193ef52e724838e5e335afc785d7679cc'
original = original_bytes.decode()
text = original
edits = []

def replace(name, old, new, expected_count):
    global text
    assert old != new and text.count(old) == expected_count, (name, text.count(old), expected_count)
    assert text.count(new) == 0, name
    text = text.replace(old, new, expected_count)
    edits.append(dict(name=name, old=old, new=new, count=expected_count))

replace('source_only_documentation_version', 'Source-only V14 complete sender window component', 'Source-only V14b complete sender window component', 1)
replace('activity_SOURCE_namespace', 'axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-admission-v14-20261010', 'axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-admission-v14b-20261010', 1)
replace('activity_OUT_namespace', 'axial-material-sender-contiguous-flux-window-streaming-sha-build-v14-20261010', 'axial-material-sender-contiguous-flux-window-streaming-sha-build-v14b-20261010', 1)
replace('activity_TERM_namespace', 'axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-terminal-v14-20261010', 'axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-terminal-v14b-20261010', 1)
replace('formal_factory_future_path', 'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py', 'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py', 1)
replace('canonical_helper_and_SOURCE_evidence_name', 'complete_environment_streaming_sha_helper_v14.py', 'complete_environment_streaming_sha_helper_v14b.py', 4)
replace('new_formal_helper_source_root', 'complete_environment_streaming_sha_source_v14_20261010/source_patch_proof.json', 'complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json', 1)
replace('ordinary_private_module_name', 'axmat_streaming_sha_actual_environment_helper_v14', 'axmat_streaming_sha_actual_environment_helper_v14b', 1)
replace('source_only_formal_path_error_version', 'TMP source-only V14 draft', 'TMP source-only V14b draft', 1)

active_literals = {
    'SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_V14': 1,
    'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V14': 1,
    'UNREADY_SOURCE_ONLY_REQUIRES_ROOT_STREAMING_HELPER_SOURCE_AND_ACTUAL_CONTROL_PINS_V14': 1,
    'READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_STREAMING_SHA_COMPONENT_EXECUTION_V14': 1,
    'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_COMPONENT_SOURCE_ADMISSION_V14': 1,
    'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_SOURCE_ADMISSION_V14': 2,
    'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_DECLARATION_V14': 2,
    'DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ONLY_V14': 1,
    'PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14': 3,
    'FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_NO_RETRY_V14': 2,
    'COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14': 2,
    'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_SEAL_V14': 2,
    'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V14': 1,
    'SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_RUNTIME_INPUT_ONLY_V14': 1,
}
for old, count in active_literals.items():
    replace('active_literal_' + old, old, old[:-3] + 'V14B', count)

# Literal whole-source inversion, then complete second inversion through frozen e1.
inverse = text
for edit in reversed(edits):
    assert inverse.count(edit['new']) == edit['count'], edit['name']
    inverse = inverse.replace(edit['new'], edit['old'], edit['count'])
assert inverse.encode() == original_bytes
parent_proof = json.loads(P14_PROOF.read_bytes())
ancestor = inverse
for edit in reversed(parent_proof['edits']):
    assert ancestor.count(edit['new']) == edit['count'], edit['name']
    ancestor = ancestor.replace(edit['new'], edit['old'], edit['count'])
assert ancestor.encode() == P13.read_bytes()
assert sha(ancestor.encode()) == 'd2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'

def function_records(source):
    result = {}
    def walk(node, parents):
        scope = parents
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            scope = parents + (node.name,)
            if isinstance(node, ast.FunctionDef):
                assert scope not in result
                result[scope] = ast.get_source_segment(source, node)
        for child in ast.iter_child_nodes(node):
            walk(child, scope)
    walk(ast.parse(source), ())
    return result

old_defs = function_records(original)
new_defs = function_records(text)
assert set(old_defs) == set(new_defs)
changed = ['.'.join(key) for key in old_defs if old_defs[key] != new_defs[key]]
protected = ('helper', 'DynamicHistoryResources', 'environment', 'source_inputs', 'stage_commands', 'stage_labels', 'archive_forecast', 'sender_source_admission', 'sender_control_contract', 'check_sender_negative_watch', 'keycodec_controls_audit', 'control_audit', 'sender_controls_audit', 'component_controls_audit', 'binary_audit', 'resource_scope_contract', 'production_cache_shape_forecast')
for name in protected:
    assert old_defs[(name,)] == new_defs[(name,)], name
assert len(old_defs) == len(new_defs) == 101
tree = ast.parse(text)
selected = ('SOURCE_STATUS', 'STREAM_ENVIRONMENT_HELPER_SHA', 'STREAM_ENVIRONMENT_SOURCE_PROOF_SHA', 'STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA', 'FUTURE_ACTUAL_BUILD_TERMINAL_SHA', 'FUTURE_ACTUAL_BUILD_SEAL_SHA', 'FUTURE_ACTUAL_NATIVE_TERMINAL_SHA', 'ORIGINAL_STAGE_COUNT', 'COMPLETE_STAGE_COUNT')
values = {target.id: ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign) for target in node.targets if isinstance(target, ast.Name) and target.id in selected}
assert values['SOURCE_STATUS'].startswith('UNREADY') and values['SOURCE_STATUS'].endswith('V14B')
assert values['ORIGINAL_STAGE_COUNT'] == 68 and values['COMPLETE_STAGE_COUNT'] == 86
assert all(value is None for key, value in values.items() if key.endswith('_SHA'))
assert new_defs[('prepare_build',)].count('    h.environment(old)') == 1
assert 'h.environment(d)' not in new_defs[('prepare_build',)]
assert '    environment(d);' in new_defs[('prepare_build',)]
assert 'with private_helper.complete_environment_digest_context(d["native_library_aliases"]):' in new_defs[('environment',)]
for protocol in ('AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_SOURCE_PATCH_V14', 'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14', 'AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1', 'AXMAT_V14_HELPER_ONLY_FIXTURE_RESULT_V1', 'AXMAT_V14_HELPER_ONLY_GENUINE_SUPERVISOR_ACTUAL_HOST_V1'):
    assert text.count(protocol) == original.count(protocol) == 1

D.mkdir(parents=True, exist_ok=True)
assert not O.exists()
O.write_bytes(text.encode())
common = dict(status='UNREADY_SOURCE_ONLY', candidate=dict(path=str(O), sha256=sha(text.encode()), bytes=len(text.encode())), complete_inverse_byteexact=True, ast_parse_only=True, edits=edits, original_all_FunctionDefs_including_nested=len(old_defs), candidate_all_FunctionDefs_including_nested=len(new_defs), byteexact_original_all_FunctionDefs_including_nested=len(old_defs)-len(changed), changed_original_functions=changed, frozen_status_and_future_pins=values, activity_only_namespace_schema_and_new_helper_evidence_paths=True, original_helper619_MRO_math_raw_86stage_92recipe_and_budgets_unchanged=True, helper_source_protocol_V14_preserved=True, helper_control_protocol_V14_preserved=True, actual_H14b_source_proof_controls_pins_bound=False, business_imports=False, business_calls=False, helper_calls=False, fixture_execution=False, compile=False, component_execution=False, project_write=False, native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False)
proof_e1 = dict(common, schema='AXMAT_V14B_COMPLETE_COMPONENT_SOURCE_DRAFT_INVERSE_TO_E1_V1', parent=dict(path=str(P), sha256=sha(original_bytes)), inverse_sha256=sha(inverse.encode()))
proof_d2 = dict(common, schema='AXMAT_V14B_COMPLETE_COMPONENT_SOURCE_DRAFT_COMPLETE_INVERSE_TO_D2_V1', parent=dict(path=str(P13), sha256=sha(ancestor.encode())), intermediate_frozen_e1=dict(path=str(P), sha256=sha(original_bytes)), intermediate_inverse_proof=dict(path=str(P14_PROOF), sha256=sha(P14_PROOF.read_bytes())), edits=parent_proof['edits']+edits, inverse_sha256=sha(ancestor.encode()))
for name, proof in (('COMPLETE_INVERSE_PROOF.json', proof_e1), ('COMPLETE_INVERSE_TO_D2_PROOF.json', proof_d2)):
    dest = D / name
    assert not dest.exists()
    dest.write_text(json.dumps(proof, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
print(json.dumps({key: value for key, value in proof_e1.items() if key != 'edits'}, indent=2, ensure_ascii=False))
for name in (O.name, 'COMPLETE_INVERSE_PROOF.json', 'COMPLETE_INVERSE_TO_D2_PROOF.json'):
    dest = D/name
    print(json.dumps(dict(path=str(dest), sha256=sha(dest.read_bytes()), bytes=dest.stat().st_size)))

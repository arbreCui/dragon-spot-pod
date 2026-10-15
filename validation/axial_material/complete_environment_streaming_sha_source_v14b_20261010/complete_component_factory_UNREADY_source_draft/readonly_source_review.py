"""Finite standard-library source/AST proof review. No business import or calls."""
import ast
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_v14b_streaming_sha_complete_component_source_draft_20261010')
C=D/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
proof=json.loads((D/'COMPLETE_INVERSE_PROOF.json').read_bytes())
proof13=json.loads((D/'COMPLETE_INVERSE_TO_D2_PROOF.json').read_bytes())
raw=C.read_bytes();text=raw.decode()
assert hashlib.sha256(raw).hexdigest()=='b6fb702ca9a8d803722d17a1082df74a2bd693aead99b691899d9335cc40bb4f'
def inverse(document):
    restored=text
    for edit in reversed(document['edits']):
        assert set(edit)=={'name','old','new','count'}
        assert type(edit['count']) is int and edit['count']>0
        assert restored.count(edit['new'])==edit['count']
        restored=restored.replace(edit['new'],edit['old'],edit['count'])
    assert restored.encode()==Path(document['parent']['path']).read_bytes()
    assert hashlib.sha256(restored.encode()).hexdigest()==document['parent']['sha256']
    return restored
mother=inverse(proof)
ancestor=inverse(proof13)
assert proof['parent']['sha256']=='e1cbc96cd7c46dc99b2a0a477b609abf70ea0c4338d5d0ed8840165945e5f35a'
assert proof13['parent']['sha256']=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert proof13['edits'][-len(proof['edits']):]==proof['edits']
def records(source):
    values={}
    def walk(node,parent):
        scope=parent
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            scope=parent+(node.name,)
            if isinstance(node,ast.FunctionDef):
                assert scope not in values
                values[scope]=ast.get_source_segment(source,node)
        for child in ast.iter_child_nodes(node):walk(child,scope)
    walk(ast.parse(source),())
    return values
before=records(mother);after=records(text);d2=records(ancestor)
assert set(before)==set(after) and len(before)==len(after)==101
changed=['.'.join(key)for key in before if before[key]!=after[key]]
assert changed==proof['changed_original_functions'] and len(changed)==9
assert set(d2)<=set(after) and len(d2)==96
changed13=['.'.join(key)for key in d2 if d2[key]!=after[key]]
assert len(changed13)==9
selected=('SOURCE_STATUS','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA','ORIGINAL_STAGE_COUNT','COMPLETE_STAGE_COUNT')
values={target.id:ast.literal_eval(node.value)for node in ast.parse(text).body if isinstance(node,ast.Assign)for target in node.targets if isinstance(target,ast.Name)and target.id in selected}
assert all(value is None for key,value in values.items()if key.endswith('_SHA'))
assert values['SOURCE_STATUS']=='UNREADY_SOURCE_ONLY_REQUIRES_ROOT_STREAMING_HELPER_SOURCE_AND_ACTUAL_CONTROL_PINS_V14B'
assert values['ORIGINAL_STAGE_COUNT']==68 and values['COMPLETE_STAGE_COUNT']==86
protected=('helper','DynamicHistoryResources','environment','source_inputs','stage_commands','stage_labels','archive_forecast','sender_source_admission','sender_control_contract','check_sender_negative_watch','check_keycodec_negative_watch','keycodec_controls_audit','control_audit','sender_controls_audit','component_controls_audit','binary_audit','resource_scope_contract','production_cache_shape_forecast')
for name in protected:assert before[(name,)]==after[(name,)]
for name in ('complete_archive_forecast','stream_environment_helper_source_admission','stream_environment_helper'):
    normalized=after[(name,)]
    for edit in reversed(proof['edits']):normalized=normalized.replace(edit['new'],edit['old'])
    assert normalized==before[(name,)]
parent_assignments={target.id:ast.get_source_segment(text,node)for node in ast.parse(text).body if isinstance(node,ast.Assign)for target in node.targets if isinstance(target,ast.Name)}
assert parent_assignments['STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT']=='STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT = ROOT / "validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py"'
assert parent_assignments['STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA']=='STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA = "d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633"'
assert 'validation/axial_material/complete_environment_streaming_sha_helper_v14b.py' in parent_assignments['STREAM_ENVIRONMENT_HELPER']
assert 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json' in parent_assignments['STREAM_ENVIRONMENT_SOURCE_PROOF']
assert parent_assignments['STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS']=='STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS = STREAM_ENVIRONMENT_SOURCE_PROOF.parent / "Root_actual_helper_controls_admission.json"'
assert text.count('"complete_environment_streaming_sha_helper_v14b.py"')==3
assert 'len(actual_result[\'groups\']) != 21' in after[('stream_environment_helper_source_admission',)]
assert 'proof[\'added_definitions\'] != sorted(set(new_defs)-set(old_defs))' in after[('stream_environment_helper_source_admission',)]
assert 'proof[\'original_definitions\'] != 34 or proof[\'byteexact_original_definitions\'] != 33' in after[('stream_environment_helper_source_admission',)]
assert after[('prepare_build',)].count('    h.environment(old)')==1 and 'h.environment(d)' not in after[('prepare_build',)] and '    environment(d);' in after[('prepare_build',)]
assert 'with private_helper.complete_environment_digest_context(d["native_library_aliases"]):' in after[('environment',)]
assert 'private_helper.environment(d, require_build_interpreter=require_build_interpreter)' in after[('environment',)]
for stream in ('stdout','stderr'):
    gate=after[('stream_environment_helper_source_admission',)]
    assert "{key: receipt[%r][key] for key in ('path', 'sha256')}"%stream in gate
    assert "type(receipt[%r]['size_bytes']) is not int"%stream in gate
    assert "receipt[%r]['size_bytes'] != require(controls[%r]['path'], controls[%r]['sha256']).stat().st_size"%(stream,'actual_full_'+stream,'actual_full_'+stream)in gate
assert 'path.stat().st_nlink != 1' not in after[('stream_environment_helper_source_admission',)]
for schema in ('AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_SOURCE_PATCH_V14','AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14','AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1','AXMAT_V14_HELPER_ONLY_FIXTURE_RESULT_V1','AXMAT_V14_HELPER_ONLY_GENUINE_SUPERVISOR_ACTUAL_HOST_V1'):
    assert text.count(schema)==mother.count(schema)==1
report=dict(status='PASS_SOURCE_TEXT_AST_TWO_COMPLETE_INVERSES_ONLY_UNREADY',candidate=dict(path=str(C),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),inverse_e1_sha256=proof['parent']['sha256'],inverse_d2_sha256=proof13['parent']['sha256'],inverse_regions_e1=len(proof['edits']),inverse_regions_d2=len(proof13['edits']),e1_all_FunctionDefs_including_nested=101,e1_byteexact_FunctionDefs_including_nested=92,e1_changed_functions=changed,d2_all_FunctionDefs_including_nested=96,d2_byteexact_FunctionDefs_including_nested=87,d2_changed_functions=changed13,frozen_status_and_pins=values,helper_physical_source_qualification_parent619_and_d2_unchanged=True,helper_V14_source_and_control_protocols_preserved=True,new_helper_added_definition_inventory_dynamic=True,original34_definitions33_byteexact_required=True,original21_control_group_requirement_preserved=True,ordinary_private_canonical_helper_load_not_SOURCE_copy=True,original86_12build_92recipe_math_raw_MRO_and_budgets_unchanged=True,forecast_code_unchanged_except_new_helper_SOURCE_evidence_filename=True,forecast_three_actual_copy_size_sum_unchanged=True,original2GiB_allowance_and_cap_unchanged=True,old_prepare_h_environment_old_original619_unchanged=True,final_and_per_stage_environment_complete_context_unchanged=True,Root_receipt_projection_and_strict_size_fix_retained=True,ordinary_hardlink_fixture_gate_preserved=True,actual_H14b_helper_proof_controls_read_or_bound=False,business_imports=False,business_calls=False,helper_calls=False,fixture_execution=False,compile=False,component_execution=False,project_write=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'READONLY_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,allow_nan=False))

"""Standard-library source/AST review only; never import or call candidate APIs."""
import ast
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_v14_streaming_sha_component_source_draft_hardlink_and_defs_fix_20261010')
O=D/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py'
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
raw=O.read_bytes();text=raw.decode();old=P.read_text();proof=json.loads((D/'COMPLETE_INVERSE_PROOF.json').read_bytes())
assert hashlib.sha256(raw).hexdigest()=='c505c5637a7027008e30f125ee0b9c949b25de5f2c8a019ae6712f6a5a4d54c0'
inverse=text
for edit in reversed(proof['edits']):
    assert inverse.count(edit['new'])==edit['count']
    inverse=inverse.replace(edit['new'],edit['old'],edit['count'])
assert inverse==old
before=ast.parse(old);after=ast.parse(text)
olddefs={node.name:node for node in before.body if isinstance(node,ast.FunctionDef)}
newdefs={node.name:node for node in after.body if isinstance(node,ast.FunctionDef)}
changed=[name for name,node in olddefs.items() if ast.get_source_segment(old,node)!=ast.get_source_segment(text,newdefs[name])]
assert set(changed)==set(proof['changed_original_functions'])
selected=('SOURCE_STATUS','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA',
    'STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA',
    'FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA','ORIGINAL_STAGE_COUNT','COMPLETE_STAGE_COUNT')
values={target.id:ast.literal_eval(node.value) for node in after.body if isinstance(node,ast.Assign)
    for target in node.targets if isinstance(target,ast.Name) and target.id in selected}
assert all(value is None for key,value in values.items() if key.endswith('_SHA'))
assert values['ORIGINAL_STAGE_COUNT']==68 and values['COMPLETE_STAGE_COUNT']==86 and values['SOURCE_STATUS'].startswith('UNREADY')
prep=ast.get_source_segment(text,newdefs['prepare_build']);env=ast.get_source_segment(text,newdefs['environment'])
assert prep.count('    h.environment(old)')==1 and 'h.environment(d)' not in prep and '    environment(d);' in prep
assert 'with private_helper.complete_environment_digest_context(d["native_library_aliases"]):' in env
assert 'private_helper.environment(d, require_build_interpreter=require_build_interpreter)' in env
retained=('helper','DynamicHistoryResources','stage_commands','stage_labels','archive_forecast','control_audit',
    'sender_controls_audit','sender_source_admission','sender_control_contract','binary_audit','resource_scope_contract',
    'production_cache_shape_forecast','check_sender_negative_watch','check_keycodec_negative_watch','component_controls_audit')
for name in retained:
    assert ast.get_source_segment(old,olddefs[name])==ast.get_source_segment(text,newdefs[name])
puregate=newdefs['stream_environment_helper_source_admission']
assert 'path.stat().st_nlink != 1' not in ast.get_source_segment(text,puregate)
assert not any(isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in
    ('load','helper','parent_factory','stream_environment_helper') for node in ast.walk(puregate))

def definitions(tree):
    records={}
    def visit(node,parents):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            key=(*parents,node.name);assert key not in records;records[key]=node;parents=key
        for child in ast.iter_child_nodes(node):visit(child,parents)
    visit(tree,())
    return records

H=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14.py')
HP=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/source_patch_proof.json')
hr=H.read_bytes();hproof=json.loads(HP.read_bytes());original_helper=Path(hproof['parent_helper']['path']).read_text()
helpertext=hr.decode();helperinverse=helpertext
assert hashlib.sha256(hr).hexdigest()=='839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
assert hashlib.sha256(HP.read_bytes()).hexdigest()=='c7984abe2579399cd6e158a53fe94052e074fec08c03cf596ed859b6fa9321a6'
for edit in reversed(hproof['edits']):
    assert set(edit)=={'name','old','new','count'} and helperinverse.count(edit['new'])==edit['count']
    helperinverse=helperinverse.replace(edit['new'],edit['old'],edit['count'])
assert helperinverse==original_helper and hashlib.sha256(helperinverse.encode()).hexdigest()=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
hold=ast.parse(original_helper);hnew=ast.parse(helpertext);hod=definitions(hold);hnd=definitions(hnew)
assert len(hod)==34 and set(hod)<=set(hnd)
exact=sum(ast.get_source_segment(original_helper,node)==ast.get_source_segment(helpertext,hnd[key]) for key,node in hod.items())
assert exact==33 and [key for key,node in hod.items() if ast.get_source_segment(original_helper,node)!=ast.get_source_segment(helpertext,hnd[key])]==[('digest',)]
for key in ('complete_full_SHA_per_unique_literal_per_environment','same_call_same_literal_memo_only','full_seven_identity_rechecks_required'):
    assert hproof[key] is True
assert hproof['cross_stage_SHA_reuse'] is False and hproof['different_literal_SHA_reuse'] is False and hproof['buffer_bytes']==4194304
for key in ('author_source_review','author_actual_source_terminal_receipt'):
    item=hproof[key];assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
report=dict(status='PASS_SOURCE_TEXT_AST_INVERSE_ONLY_UNREADY',
    candidate=dict(path=str(O),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),
    inverse_parent_sha256=hashlib.sha256(inverse.encode()).hexdigest(),regions=len(proof['edits']),
    original_topdefs=len(olddefs),new_topdefs=len(newdefs),
    original_all_function_defs=sum(isinstance(node,ast.FunctionDef)for node in ast.walk(before)),
    new_all_function_defs=sum(isinstance(node,ast.FunctionDef)for node in ast.walk(after)),
    changed_original_functions=changed,byteexact_original_top_functions=78-len(changed),
    frozen_status_and_future_pins=values,
    actual_helper_source_read_only_pin=dict(path=str(H),sha256=hashlib.sha256(hr).hexdigest()),
    actual_helper_source_proof_read_only_pin=dict(path=str(HP),sha256=hashlib.sha256(HP.read_bytes()).hexdigest()),
    helper_inverse619_exact=True,helper_original_FunctionDef_and_ClassDef_count=34,helper_byteexact_definition_count=exact,
    ordinary_hardlinks_preserved_in_control_gate=True,original86_and12_build_route_unchanged=True,
    original1800_600_512_1thread_1child_0retry_2GiB_96GiB_free8_unchanged=True,
    original_helper_runner_MRO_math_raw_code_byteexact=True,old_prepare_environment_original619_unchanged=True,
    final_and_per_stage_environment_private_context_passes_complete_native_alias_mapping=True,
    unknown_actual_control_receipt_fields_must_be_root_bound=True,
    actual_controls_or_benchmark_read=False,actual_controls_pins_bound=False,
    business_imports=False,helper_calls=False,fixture_execution=False,compile=False,project_write=False,
    native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'READONLY_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))

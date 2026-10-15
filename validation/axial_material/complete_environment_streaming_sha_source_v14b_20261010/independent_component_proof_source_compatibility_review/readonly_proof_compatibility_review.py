"""Read only immutable source/proof inputs; write this separate TMP review only.
Never import/call any business/helper/source gate, fixture, runner or benchmark.
"""
import ast
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_v14b_component_source_admission_proof_compatibility_review_20261010')
C=Path('/private/tmp/axmat_v14b_streaming_sha_complete_component_source_draft_20261010/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py')
P=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json')
H=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14b.py')
G=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_control_sources/helper_only_controls_v14b.py')
def digest(raw):return hashlib.sha256(raw).hexdigest()
craw=C.read_bytes();source=craw.decode();tree=ast.parse(source)
assert digest(craw)=='b6fb702ca9a8d803722d17a1082df74a2bd693aead99b691899d9335cc40bb4f'
proof_raw=P.read_bytes();proof=json.loads(proof_raw)
assert digest(proof_raw)=='1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2'
helper_raw=H.read_bytes();helper_source=helper_raw.decode()
assert digest(helper_raw)=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
old_path=Path(proof['parent_helper']['path']);old_raw=old_path.read_bytes();old_source=old_raw.decode()
assert digest(old_raw)=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
assert proof['parent_helper']==dict(path=str(old_path),sha256=digest(old_raw))
assert proof['candidate_helper']==dict(path=str(H),sha256=digest(helper_raw))
factory_parent=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
assert proof['component_factory_parent']==dict(path=str(factory_parent),sha256='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633')
assert digest(factory_parent.read_bytes())==proof['component_factory_parent']['sha256']

defs={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
gate_node=defs['stream_environment_helper_source_admission'];gate=ast.get_source_segment(source,gate_node)
required_literal_fields=sorted({node.slice.value for node in ast.walk(gate_node)if isinstance(node,ast.Subscript)and isinstance(node.value,ast.Name)and node.value.id=='proof'and isinstance(node.slice,ast.Constant)and isinstance(node.slice.value,str)})
assert all(key in proof for key in required_literal_fields)
semantics_node=next(node for node in gate_node.body if isinstance(node,ast.Assign)and any(isinstance(target,ast.Name)and target.id=='semantics'for target in node.targets))
assert isinstance(semantics_node.value,ast.Call)and isinstance(semantics_node.value.func,ast.Name)and semantics_node.value.func.id=='dict'
semantics={keyword.arg:ast.literal_eval(keyword.value)for keyword in semantics_node.value.keywords}
assert all(proof[key]==value for key,value in semantics.items())
assert proof['schema']=='AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_SOURCE_PATCH_V14'
assert proof['status']=='PASS_COMPLETE_SOURCE_ONLY_NOT_HELPER_CONTROL_OR_COMPONENT_QUALIFICATION'
for key in ('complete_inverse_byteexact','ROOT_binding_unchanged','outside_context_default_digest_behavior_unchanged','native_alias_exit_recheck_required','native_alias_mapping_must_be_explicitly_passed','original_environment_verify_inventory_modules_guard_and_mathematics_byteexact'):
    assert proof[key] is True
for key in ('genuine_supervisor_class_or_MRO_modified','business_imported','business_executed','helper_controls_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):
    assert proof[key] is False
assert proof['original_definitions']==34 and proof['byteexact_original_definitions']==33 and proof['modified_original_definitions']==['digest']
inverse=helper_source
assert isinstance(proof['edits'],list)and len(proof['edits'])==1
for edit in reversed(proof['edits']):
    assert set(edit)=={'name','old','new','count'}and type(edit['count']) is int and edit['count']>0
    assert inverse.count(edit['new'])==edit['count']
    inverse=inverse.replace(edit['new'],edit['old'],edit['count'])
assert inverse.encode()==old_raw
forward=old_source
for edit in proof['edits']:
    assert forward.count(edit['old'])==edit['count']
    forward=forward.replace(edit['old'],edit['new'],edit['count'])
assert forward.encode()==helper_raw
def scope_records(tree):
    records={}
    def walk(node,parent):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            parent=parent+(node.name,)
            assert parent not in records
            records[parent]=node
        for child in ast.iter_child_nodes(node):walk(child,parent)
    walk(tree,())
    return records
old_tree=ast.parse(old_source);helper_tree=ast.parse(helper_source)
old_scope=scope_records(old_tree);new_scope=scope_records(helper_tree)
assert len(old_scope)==34 and set(old_scope)<=set(new_scope)
changed=['.'.join(key)for key,node in old_scope.items()if ast.get_source_segment(old_source,node)!=ast.get_source_segment(helper_source,new_scope[key])]
assert changed==['digest']
old_top={node.name for node in old_tree.body if isinstance(node,ast.FunctionDef)}
new_top={node.name for node in helper_tree.body if isinstance(node,ast.FunctionDef)}
added=sorted(new_top-old_top)
assert added==proof['added_definitions']and len(added)==13
assert '_env_stream_native_alias_path_snapshot' in added
assert "proof['added_definitions'] != sorted(set(new_defs)-set(old_defs))" in gate
assert 'len(old_scope) != 34' in gate
assert "if key != ('digest',)" in gate
for src,parsed in ((old_source,old_tree),(helper_source,helper_tree)):
    root_assignments=[ast.get_source_segment(src,node)for node in parsed.body if isinstance(node,ast.Assign)and any(isinstance(target,ast.Name)and target.id=='ROOT'for target in node.targets)]
    assert root_assignments==['ROOT = Path(__file__).resolve().parents[2]']
source_review_pins={}
for key in ('author_source_review','author_actual_source_terminal_receipt','independent_complete_source_review'):
    descriptor=proof[key]
    assert set(descriptor)=={'path','sha256'}
    raw=Path(descriptor['path']).read_bytes()
    assert digest(raw)==descriptor['sha256']
    source_review_pins[key]=dict(descriptor,bytes=len(raw))

driver_raw=G.read_bytes();driver_source=driver_raw.decode();driver_tree=ast.parse(driver_source)
assert digest(driver_raw)=='a0cd6a7b37d0b9f9cce786d78c1336d0edbe870c44be6be939f1b7ed5e9a0f30'
fixture=next(node for node in driver_tree.body if isinstance(node,ast.FunctionDef)and node.name=='fixture_controls')
literal_groups=[];loop_groups=[]
for statement in fixture.body:
    if isinstance(statement,ast.Expr)and isinstance(statement.value,ast.Call)and isinstance(statement.value.func,ast.Name)and statement.value.func.id=='run':
        literal_groups.append(ast.literal_eval(statement.value.args[0]))
    elif isinstance(statement,ast.For):
        if isinstance(statement.target,ast.Name)and statement.target.id=='mode':
            modes=ast.literal_eval(statement.iter)
            assert modes==['truncate','replace','rewrite']
            assert len(statement.body)==1 and isinstance(statement.body[0],ast.Expr)
            call=statement.body[0].value
            assert isinstance(call,ast.Call)and isinstance(call.func,ast.Name)and call.func.id=='run'
            assert isinstance(call.args[0],ast.BinOp)and isinstance(call.args[0].op,ast.Add)
            assert ast.literal_eval(call.args[0].left)=='during_stream_'and isinstance(call.args[0].right,ast.Name)and call.args[0].right.id=='mode'
            loop_groups=['during_stream_'+mode for mode in modes]
assert len(literal_groups)==18 and len(loop_groups)==3 and len(set(literal_groups+loop_groups))==21
aliases=next(node for node in fixture.body if isinstance(node,ast.FunctionDef)and node.name=='aliases')
alias_text=ast.get_source_segment(driver_source,aliases)
assert len([node for node in ast.walk(aliases)if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='run'])==0
assert "additional_v14b_alias_cases':extra" in alias_text
assert "'legal_three_link_chain'" in alias_text and "'legal_completed_directory_link_repeat_after_dotdot'" in alias_text
assert "[('self_cycle',selflink),('mutual_cycle',a),('growing_cycle',growing)]" in alias_text
assert "len(actual_result['groups']) != 21" in gate
selected=('SOURCE_STATUS','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA','ORIGINAL_STAGE_COUNT','COMPLETE_STAGE_COUNT')
values={target.id:ast.literal_eval(node.value)for node in tree.body if isinstance(node,ast.Assign)for target in node.targets if isinstance(target,ast.Name)and target.id in selected}
assert all(value is None for key,value in values.items()if key.endswith('_SHA'))
assert values['SOURCE_STATUS'].startswith('UNREADY')and values['ORIGINAL_STAGE_COUNT']==68 and values['COMPLETE_STAGE_COUNT']==86
for stream in ('stdout','stderr'):
    assert "{key: receipt[%r][key] for key in ('path', 'sha256')} != controls[%r]"%(stream,'actual_full_'+stream)in gate
    assert "type(receipt[%r]['size_bytes']) is not int"%stream in gate
    assert "receipt[%r]['size_bytes'] != require(controls[%r]['path'], controls[%r]['sha256']).stat().st_size"%(stream,'actual_full_'+stream,'actual_full_'+stream)in gate
assert 'path.stat().st_nlink != 1' not in gate
def line_of(fragment):
    return next(index for index,line in enumerate(source.splitlines(),1)if fragment in line)
positions=dict(unknown_pins_guard=line_of('for wanted in (STREAM_ENVIRONMENT_HELPER_SHA'),proof_protocol=line_of("proof['schema'] != 'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_SOURCE_PATCH_V14'"),old34_and33_definitions=line_of("proof['original_definitions'] != 34"),all_original_nondigest_definitions=line_of('len(old_scope) != 34'),dynamic_all_added_definitions=line_of("proof['added_definitions'] != sorted"),stdout_projection=line_of("{key: receipt['stdout'][key]"),stdout_strict_size=line_of("type(receipt['stdout']['size_bytes'])"),stderr_projection=line_of("{key: receipt['stderr'][key]"),stderr_strict_size=line_of("type(receipt['stderr']['size_bytes'])"),helper21_groups=line_of("len(actual_result['groups']) != 21"))
assert C.read_bytes()==craw
report=dict(status='PASS_STATIC_SOURCE_PROOF_COMPATIBILITY_ONLY_COMPONENT_UNREADY',candidate=dict(path=str(C),sha256=digest(craw),bytes=len(craw)),new_formal_source_proof=dict(path=str(P),sha256=digest(proof_raw),bytes=len(proof_raw)),new_canonical_helper_source=dict(path=str(H),sha256=digest(helper_raw),bytes=len(helper_raw)),proof_required_literal_fields_present=required_literal_fields,proof_metadata_semantics_match_gate=True,proof_single_region_complete_inverse_and_forward619_byteexact=True,original_FunctionDef_ClassDef_including_nested=34,original_byteexact_definitions=33,modified_original_definitions=changed,added_top_FunctionDefs=added,added_top_FunctionDefs_count=len(added),dynamic_added_definition_contract_accepts13=True,helper_physical_source_parent619_component_factory_parent_d2=True,source_review_file_pins_checked=source_review_pins,new_driver_source=dict(path=str(G),sha256=digest(driver_raw),bytes=len(driver_raw)),static_driver_protocol_groups=21,direct_literal_group_count=18,loop_group_count=3,new_alias_subcases_stay_within_original_group=True,original_component_stage_count86_unmodified=True,Root_stdout_stderr_project_only_path_sha256_and_strict_int_actual_file_size=True,ordinary_hardlinks_preserved=True,frozen_status_and_pins=values,source_line_positions=positions,deterministic_source_contract_incompatibilities=[],minimal_fix_required=False,canonical_helper_install_is_not_control_qualification=True,actual_controls_or_benchmark_read=False,business_imports=False,business_calls=False,helper_calls=False,source_gate_invocations=False,fixture_execution=False,benchmark_execution=False,compile=False,component_execution=False,canonical_or_candidate_write=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
D.mkdir(parents=True,exist_ok=True)
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,allow_nan=False))

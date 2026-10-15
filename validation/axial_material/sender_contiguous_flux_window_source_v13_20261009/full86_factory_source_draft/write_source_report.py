"""Pure stdlib AST/text/SHA/inverse report. Never import business modules."""
import ast, difflib, hashlib, json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_full_sender_window_component_source_draft_20261009')
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py')
C=D/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
M=Path('/private/tmp/axmat_v13_flusp64_window_wrapper_control_source_draft_20261009/CONTROL_CONTRACT.json')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(name,body):(D/name).write_text(json.dumps(body,indent=2,allow_nan=False)+'\n')
old=P.read_text();new=C.read_text();ot=ast.parse(old);nt=ast.parse(new)
assert sha(P)=='f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
assert sha(C)=='a6dd0796316aec5b6c16ff73677c689a7e7146697759a0cde9187be962807821'
assert sha(M)=='74ecac78a42fd13f5162cc52ad4d96cf6e94abd970406f4fede467696c4dcffd'
regions=json.loads((D/'composition_regions.json').read_text());restored=new
for e in reversed(regions):
    assert restored.count(e['after'])==e['count'],e['name']
    restored=restored.replace(e['after'],e['before'],e['count'])
assert restored==old
of={n.name:ast.get_source_segment(old,n) for n in ot.body if isinstance(n,ast.FunctionDef)}
nf={n.name:ast.get_source_segment(new,n) for n in nt.body if isinstance(n,ast.FunctionDef)}
assert set(of)<=set(nf)
equal=[name for name in of if of[name]==nf[name]]
changed=[name for name in of if of[name]!=nf[name]]
assert changed==['require_ready','source_inputs','stage_commands','stage_labels','prepare_build','declaration_admission','check_watch','expected_stage_exit','stage_outcome_valid','binary_audit','audit_build','run_build','production_admission'],changed
for name in ('patch_admission','archive_forecast','production_cache_shape_forecast','control_audit',
             'control_source_equivalence','cache_observer_contract','input_fixture_audit','memory_controls_audit',
             'codec_controls_audit','keycodec_controls_audit','check_keycodec_negative_watch','external_terminal_admission',
             'resource_scope_contract','history_roots','resources_for','environment','resource_admission'):
    assert name in equal,name
def assigned(tree):
    return {n.targets[0].id:ast.dump(n.value,include_attributes=False) for n in tree.body
            if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
oa,na=assigned(ot),assigned(nt)
changed_bindings=[name for name in oa if oa[name]!=na[name]]
assert set(changed_bindings)=={'SOURCE','OUT','TERMINAL','FAMILY','TERMINAL_SCHEMA','SOURCE_STATUS'},changed_bindings
unknown=['SENDER_PATCH_HELPER_SHA','CANDIDATE_SENDER_SHA','SENDER_SOURCE_PROOF_SHA','SENDER_SOURCE_INPUT_SHA',
         'SENDER_CONTROL_SOURCE_SHA','SENDER_CONTROL_CONTRACT_SHA','SENDER_CONTROLS_AUDITOR_SHA','SENDER_CONTROL_LAYOUT']
for name in unknown:assert na[name]=='Constant(value=None)',name
assert 'UNREADY' in next(ast.literal_eval(n.value) for n in nt.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_STATUS' for t in n.targets))
for name in ('FUTURE_PIPELINE_FACTORY_SHA','FUTURE_CONTROL_RESULT_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):
    if name in oa:assert oa[name]==na[name]=='Constant(value=None)',name
op=next(n for n in ot.body if isinstance(n,ast.FunctionDef) and n.name=='prepare_build')
np=next(n for n in nt.body if isinstance(n,ast.FunctionDef) and n.name=='prepare_build')
def inner_assignment(fn,name):
    return next(n.value for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
for name in ('common','commands','compiler'):
    assert ast.dump(inner_assignment(op,name),include_attributes=False)==ast.dump(inner_assignment(np,name),include_attributes=False),name
def extends(fn):
    return [n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
            and isinstance(n.func.value,ast.Name) and n.func.value.id=='commands' and n.func.attr=='extend']
oe,ne=extends(op),extends(np)
assert len(oe)==1 and len(ne)==2 and ast.dump(oe[0],include_attributes=False)==ast.dump(ne[0],include_attributes=False)
assert isinstance(ne[1].args[0],ast.List) and len(ne[1].args[0].elts)==3
inserts=[n for n in ast.walk(np) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
         and isinstance(n.func.value,ast.Name) and n.func.value.id=='commands' and n.func.attr=='insert']
assert len(inserts)==1 and ast.literal_eval(inserts[0].args[0])==1
def return_value(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name).body[-1].value
sc0,sc1=return_value(ot,'stage_commands'),return_value(nt,'stage_commands')
assert isinstance(sc0,ast.List) and isinstance(sc1,ast.List)
assert ast.dump(ast.List(elts=sc1.elts[:-2]+[sc1.elts[-1]],ctx=ast.Load()),include_attributes=False)==ast.dump(sc0,include_attributes=False)
def added_terms(n):return added_terms(n.left)+added_terms(n.right) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add) else [n]
sl0,sl1=added_terms(return_value(ot,'stage_labels')),added_terms(return_value(nt,'stage_labels'))
assert len(sl1)==len(sl0)+1
assert [ast.dump(n,include_attributes=False) for n in sl1[:-2]+[sl1[-1]]]==[ast.dump(n,include_attributes=False) for n in sl0]
contract=json.loads(M.read_text());plan=contract['planned_counts_not_actual'];cases=contract['cases']
assert len(cases)==14 and [c['expected_returncode'] for c in cases]==[0]*10+[1]*4
assert sum(len(c['raw_files']) for c in cases)==70
assert sum(r['size_bytes'] for c in cases for r in c['raw_files'])==288241824
assert plan['wrapper_calls_total']==48 and plan['observer_calls_total']==34
positive=[c for c in cases if not c['negative']]
sender_count_expectation=dict(positive_cases=10,expected_guard_rejection_cases=4,positive_steps=22,
    reference_wrapper_calls=24,candidate_wrapper_calls=24,wrapper_calls_total=48,observer_calls_total=34,
    direct_candidate_steps=sum(s['expected_route']==1 for c in positive for s in c['steps']),
    sparse_fallback_steps=sum(s['expected_route']==2 for c in positive for s in c['steps']),
    empty_steps=sum(s['expected_route']==0 for c in positive for s in c['steps']),
    raw_file_count=70,raw_bytes=288241824,
    independently_verified_active_output_scalars=sum(2*c['nun']*s['active_groups'] for c in positive for s in c['steps']))
proof=dict(schema='AXMAT_V13_FULL_SENDER_COMPONENT_SOURCE_COMPOSITION_INVERSE_V1',
    parent=dict(path=str(P),sha256=sha(P)),candidate=dict(path=str(C),sha256=sha(C)),
    regions_file=dict(path=str(D/'composition_regions.json'),sha256=sha(D/'composition_regions.json')),
    region_count=len(regions),reverse_whole_file_byteexact=True,reconstructed_parent_sha256=hashlib.sha256(restored.encode()).hexdigest(),
    changed_original_top_assignments=changed_bindings,original_top_functions=len(of),exact_original_functions=equal,
    changed_original_functions=changed,added_top_functions=sorted(set(nf)-set(of)),
    original_compile_common_and_eight_command_expressions_unchanged=True,
    four_new_builds_one_insert_before_production_link_and_three_appended=True,
    original_stage_command_and_label_expressions_preserved_outside_new_sender_append=True,
    strict_UNREADY_all_new_source_sha_and_complete_layout_None=True,business_imported_or_executed=False)
write('source_complete_inverse_proof.json',proof)
(D/'full_source.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(P),tofile=str(C))))
report=dict(schema='AXMAT_V13_FULL_SENDER_COMPONENT_SOURCE_ONLY_DRAFT_REPORT_V1',
    classification='COMPLETE_UNREADY_SOURCE_DRAFT_NOT_EXECUTED',candidate=proof['candidate'],parent=proof['parent'],
    complete_inverse_proof=dict(path=str(D/'source_complete_inverse_proof.json'),sha256=sha(D/'source_complete_inverse_proof.json')),
    total_declared_stages_plan=86,original_stage_count_plan=68,original_build_commands=8,additional_build_commands=4,
    original_controls=59,new_sender_controls=14,final_audit_stages=1,
    original_control_audit_whole_function_sha256=hashlib.sha256(of['control_audit'].encode()).hexdigest(),
    original_control_audit_function_byteexact=True,all_original_mathematical_models_and_forecast_functions_byteexact=True,
    original_30_count_fields_retained_with_only_top_total86=True,
    sender_counts_scope='Separate actual wrapper observer scope; never added to the original2710 real SPOT receiver calls',
    sender_planned_counts_not_actual=plan,sender_actual_auditor_expected_counts_not_actual=sender_count_expectation,
    sole_new_production_overrides=['SPOT1P64.o','FLU2DR64.o'],
    production_link_inverse='Both objects and runtime output restore exact original92 parent link; real unchanged SPOF64 archive retained',
    wrapper_unit_link='Actual newfullsender object + original FLUSP64_REFERENCE + observerdriver SPOF64 + newSPOT0800 + unchangedwhite + original4libs; no explicit originalSPOF.o',
    sender_raw_receipt_and_all_seven_identity_before_after_gate=True,
    final_source_predecessors_environment_resource_protection_and_four_tail_gates_retained=True,
    sender_release_scope='Raw proves repeated caller carry and active-set transitions; source inverse proves conditional F2 deallocation. No measured nativeRSS saving.',
    additional_archive_forecast='Original cache/raw fields stay exact; newforecast_complete_with_sender_bytes adds exact sender288241824 raw bytes, eight copied sources and22row allowance, using original single1GiBnonraw reservation.',
    budgets=dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,archive_reserve_bytes=2*2**30,
        history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,thread_count=1,serial_child_count=1,retries=0),
    unknown_new_binding_names=unknown,unknown_actual_success_evidence='No new declaration, build, seal, external terminal, runtime, numerical controls, native or scientific success exists.',
    unchanged_sender_ancestor_source_sha256='bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81',
    unchanged_sender_ancestor_object_sha256='74b22d403667e78686aef52b97933478779d4dfeb250b1cd1cb86343c930cfb9',
    AST_and_text_inverse_only=True,project_written=False,business_modules_imported=False,compiler_or_control_execution_performed=False,
    actual_full_FLU_entry_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
write('REPORT.json',report)
print(json.dumps(dict(status='PASS_SOURCE_ONLY_COMPLETE_DRAFT_INVERSE',candidate_sha256=sha(C),
    report_sha256=sha(D/'REPORT.json'),inverse_proof_sha256=sha(D/'source_complete_inverse_proof.json'),
    original_top_functions=len(of),exact_original_functions=len(equal),changed_original_functions=len(changed),
    added_top_functions=len(set(nf)-set(of)),regions=len(regions),business_executed=False)))

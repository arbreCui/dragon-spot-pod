import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path

U=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/next_complete_combined_v18_source_only_review/sealed_complete_UNREADY_candidate/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py')
I=U.parent/'source_inverse_proof.json'
P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
Q=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json')
G=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
D=Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010')
S=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_component_execution_receipts/Root_actual_complete86_and_formal_admission_summary.json')
R=U.parent.parent/'sealed_independent_source_review/REVIEW.json'
M=U.parent.parent/'sealed_independent_source_review/sealed_manifest.json'
RP=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')
I17=Path('/private/tmp/axmat_v17_complete_combined_fresh_wire_trace_table_source_only_FINAL_20261010/source_inverse_proof.json')
O=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py')
D.mkdir()

def pin(path):
    assert path.is_absolute() and '..' not in path.parts
    for parent in [*reversed(path.parents),path]:
        st=parent.lstat()
        assert not stat.S_ISLNK(st.st_mode)
        if parent!=path:assert stat.S_ISDIR(st.st_mode)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd);assert stat.S_ISREG(first.st_mode)and first.st_nlink==1
        h=hashlib.sha256();count=0
        while raw:=os.read(fd,1024*1024):h.update(raw);count+=len(raw)
        last=os.fstat(fd)
        a=[first.st_dev,first.st_ino,first.st_mode,first.st_nlink,first.st_size,first.st_mtime_ns,first.st_ctime_ns]
        b=[last.st_dev,last.st_ino,last.st_mode,last.st_nlink,last.st_size,last.st_mtime_ns,last.st_ctime_ns]
        assert a==b and count==first.st_size
        return {'path':str(path),'sha256':h.hexdigest(),'size_bytes':count,'identity7':a}
    finally:os.close(fd)

def pairs(values):
    result={}
    for key,value in values:
        assert key not in result
        result[key]=value
    return result

def reject(value):raise ValueError('nonfinite JSON constant '+value)
def read(path):return json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=reject)
def write(path,value):
    with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

inputs=[U,I,P,Q,G,S,R,M,RP,I17,O]
before=[pin(path)for path in inputs]
assert before[0]['sha256']=='ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'
assert before[1]['sha256']=='920d4cef7d96e8f0737a82f9e5cad8feb7b7c3387324dc128b66f1c45908f0e4'
assert before[2]['sha256']=='feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'
assert before[3]['sha256']=='d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'
assert before[4]['sha256']=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
q=read(Q)
assert q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_HELPER_ACTUAL_CONTROLS_ADMISSION_V17'
assert q['status']=='QUALIFIED_PURE_COMPLETE_GRAPH_HELPER_METADATA_PROTOCOL_ONLY_V17'
ref_names=['helper','actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest']
references=[]
for name in ref_names:
    record=q[name]
    # This finite SOURCE binding does not re-read ART or numeric payloads.
    # Original actual qualification references remain exactly bound by Q.
    if Path(record['path']).is_relative_to(Path('/Users/wen/spot/validation/artifacts')):
        references.append(dict(name=name,bound_by_actual_Q=record,freshly_read_in_this_source_task=False))
        continue
    actual=pin(Path(record['path']))
    assert actual['sha256']==record['sha256'] and actual['size_bytes']==record['size_bytes'] and actual['identity7']==record['identity']
    references.append(dict(name=name,actual=actual,qualification_metadata_reference_exact=True))
assert q['helper']['path']==str(G) and q['helper']['sha256']==before[4]['sha256']
assert all(q[key]is False for key in ('supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
protocol=q['full_protocol']
assert all(protocol[key]is True for key in ('original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation'))
assert protocol['accepted_str_subtype_groups']==2 and protocol['small_codec_rejections']==61
assert protocol['complete_original_graph_counts']['read_trace_records']==62332
assert protocol['complete_original_graph_counts']['requirements']==237767 and protocol['complete_original_graph_counts']['canonical_files']==36776
assert protocol['complete_new_creation_trace_records']==63379
assert q['original_caps']==dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=67108864,history_bytes=103079215104,free_bytes=8589934592,threads=1,children=1,retries=0)
assert q['actual_measurement']['whole_seconds']<60 and q['actual_measurement']['child_seconds']<60 and q['actual_measurement']['sampled_peak_rss_mib']<512 and q['actual_measurement']['actual_final_host_out_source_bytes']<67108864
terminal=read(Path(q['actual_root_terminal']['path']))
assert terminal['terminal_return_observed']is True and terminal['session_closed']is True and terminal['retries']==0
initial=terminal['actual_initial_tool_return'];last=terminal['actual_terminal_tool_return']
assert initial['chunk_id']=='d1734f'and initial['session_id']==59994
assert last['chunk_id']=='e2794c'and type(last['exit_code'])is int and last['exit_code']==0 and 'session_id'not in last
review=read(Path(q['independent_actual_review']['path']))
assert review['status']=='PASS_ACTUAL_PURE_HELPER_CONTROLS_EVIDENCE_ONLY' and review['no_blocking_issue_found']is True
assert review['helper_sha256']==before[4]['sha256'] and review['whole_source_inverse_exact']is True and review['full_helper_and_driver_finite_inverses_exact']is True
source_review=read(R);source_manifest=read(M)
assert source_review['status']=='PASS_SOURCE_ONLY_UNREADY_RUNTIME_REQUIRED' and source_review['candidate_sha256']==before[0]['sha256']
assert source_review['full_source_inverse_chain_exact']is True and source_review['all_original_phase_If_Assert_Raise_AST_and_order_exact']is True and source_review['future_business_six_pins_None']is True
assert before[5]['sha256']=='ce6353ecefa37cb7211889616b6d71f47638c0ceadc67811b48a9ec50ef20812'
component_summary=read(S)
assert component_summary['status']=='ACTUAL_COMPLETE86_COMPONENT_RUNTIME_INPUT_ADMITTED_ONLY_V15' and component_summary['formal_runtime_input_admission_completed']is True
assert component_summary['stages']==86 and component_summary['ordinary_PASS']==62 and component_summary['expected_rejections']==24 and component_summary['unexpected_failures']==0
assert all(component_summary[k]is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert component_summary['actual_declaration']['sha256']=='6dee0b453ea519beeb85abd834c22939c0f5c49565bcd3c793c6b83bf7e092a7'
assert component_summary['actual_build_seal']['sha256']=='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
assert component_summary['actual_external_terminal']['sha256']=='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
src=U.read_text();original=src;edits=[]
def replace(old,new):
    global src
    assert src.count(old)==1
    src=src.replace(old,new)
    edits.append(dict(old=old,new=new,occurrences=1))
replace(src.splitlines()[0],repr('READY source-bound V18 complete sender/root-index whole-phase caller last-use revision. The exact bcd order-preserved helper and d490 Root pure-metadata admission remain qualified INPUT-only prerequisites. Original V15 complete86 component success and source pins are retained as complete INPUT evidence. All original whole historical bodies, fresh EOF phases, full graph traces, aliases, namespaces, current predicates, failure-length checks, five build stages, physics and budgets remain required. The added same-SHA whole specs reread and all ecfd function bodies remain unchanged. Failed V17 build grants no successful combined/native/science evidence. This new V18 family has not executed prepare/build/whole INPUT/native/AAA/ABA; all six future business success pins remain None.'))
replace("DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED'", "DRAFT_STATUS = 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'")
compile(src,'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py','exec')
reverse=src
for item in reversed(edits):
    assert reverse.count(item['new'])==1
    reverse=reverse.replace(item['new'],item['old'])
assert reverse==original
unready_inverse=read(I);ancestry=reverse
for item in reversed(unready_inverse['edits']):
    assert ancestry.count(item['new'])==item['occurrences']
    ancestry=ancestry.replace(item['new'],item['old'])
assert ancestry==P.read_text()
for layer in (read(RP),read(I17)):
    for item in reversed(layer['edits']):
        assert ancestry.count(item['new'])==item['occurrences']
        ancestry=ancestry.replace(item['new'],item['old'])
assert ancestry==O.read_text()
def definitions(source):return {n.name:ast.get_source_segment(source,n)for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert definitions(src)==definitions(original)
assign=lambda text:{ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,ast.Assign)}
assert assign(src)-assign(original)=={"DRAFT_STATUS = 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'"}
assert assign(original)-assign(src)=={"DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED'"}
assert len(definitions(src))==70
for name,field in (('TRIM_DECL_SHA','actual_declaration'),('TRIM_SEAL_SHA','actual_build_seal'),('TRIM_TERMINAL_SHA','actual_external_terminal')):
    node=next(n for n in ast.parse(src).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    assert node.value.value==component_summary[field]['sha256']

for name in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):
    assert src.count(name+' = None')==1
assert before==[pin(path)for path in inputs]
for record in references:
    if 'actual'in record:assert pin(Path(record['actual']['path']))==record['actual']
C=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'
with C.open('x')as f:f.write(src)
proof={'schema':'AXMAT_V18_READY_COMBINED_TWO_SOURCE_BINDINGS_INVERSE_V1','status':'READY_SOURCE_BOUND_UNINSTALLED_NOT_EXECUTED','inputs':before,'actual_helper_controls_admission':before[3],'actual_helper':before[4],'actual_complete86_component_summary':before[5],'independent_V18_source_review':before[6],'source_qualification_references':references,'SOURCE_references_full_sha_identity7_verified':True,'ART_references_bound_only_by_actual_Q_not_reread':True,'source_inputs_before_after_equal':True,'candidate':pin(C),'edits':edits,'exact_two_source_bindings':True,'all_70_function_class_definitions_byteexact_to_UNREADY_ecfd':True,'READY_complete_inverse_to_ecfd_exact':True,'complete_ancestry_inverse_chain_ecfd_feeb_82_0ea_exact':True,'actual_helper_protocol_qualified_only':True,'actual_root_terminal_typed_exit0_closed_verified':True,'Q_all_production_native_science_claims_false':True,'component_actual_decl_seal_terminal_globals_unchanged':True,'future_combined_native_six_success_pins_None':True,'source_compile_only':True,'installed':False,'project_written':False,'ART_read_or_written':False,'project_module_imported_or_executed':False,'numeric_payload_read':False,'resource_check_called':False,'new_combined_prepare_or_build_or_whole_INPUT_or_native_or_AAA_or_ABA_credit':False}
write(D/'source_binding_inverse_proof.json',proof)
report={'schema':'AXMAT_V18_COMPLETE_COMBINED_READY_SOURCE_BINDING_REPORT_V1','status':'READY_SOURCE_BOUND_UNINSTALLED_ROOT_FRESH_BOUNDED_PREP_REQUIRED','candidate':pin(C),'helper_controls_admission':before[3],'helper':before[4],'component_summary':before[5],'independent_V18_source_review':before[6],'actual_controls_scope':'pure complete metadata protocol only; no new V18 production graph, combined build/INPUT or native/AAA/ABA','source_changes_only':['truthful READY docstring retaining source-only and false business/science scope','DRAFT_STATUS to exact existing require_ready V18 READY string'],'qualified_graph_and_helper_admission_globals_already_actual_unchanged':True,'all_function_bodies_exact_to_ecfd':True,'all_other_globals_and_body_bytes_unchanged':True,'source_inverse_chain_READY_ecfd_feeb_82_0ea_exact':True,'original_V15_component_decl_seal_terminal_source_pins_unchanged':True,'original_budgets_and_physical_inputs_unchanged':True,'fresh_V18_SOURCE_OUT_TERMINAL_HOST_namespaces_unchanged_from_UNREADY':True,'Q_false_production_science_fields':{key:q[key]for key in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')},'actual_new_combined_declaration_sha256':None,'actual_new_combined_prepare_terminal_sha256':None,'actual_new_combined_seal_sha256':None,'actual_new_combined_terminal_sha256':None,'actual_new_combined_runtime_sha256':None,'actual_new_native_terminal_sha256':None,'installed':False,'project_written':False,'ART_read_or_written':False,'project_module_imported_or_called':False,'business_executed':False,'source_level_peak_failure_cause_or_future_RSS_PASS_proved':False,'next_action':'Root review and install the exact READY candidate at its V18 FORMAL_FACTORY, retain this source inverse and actual prerequisite Q bindings, then independently execute a fresh original bounded V18 prepare once; success requires the observed new artifacts and terminal.'}
write(D/'REPORT.json',report)
print(json.dumps({'source_only_READY_binding':True,'installed':False,'business_executed':False,'output_dir':str(D),'candidate':pin(C),'proof':pin(D/'source_binding_inverse_proof.json'),'report':pin(D/'REPORT.json'),'two_edits_only':True,'all_70_function_bodies_unchanged':True,'inverse_ecfd_feeb_82_0ea_exact':True,'no_ART_read_or_write':True},allow_nan=False))

import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path

U=Path('/private/tmp/axmat_v17_complete_combined_fresh_wire_trace_table_source_only_FINAL_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.UNREADY.py')
I=U.parent/'source_inverse_proof.json'
P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py')
Q=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json')
G=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
D=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010')
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

inputs=[U,I,P,Q,G]
before=[pin(path)for path in inputs]
assert before[0]['sha256']=='82b17014f36520dadc77c387d8e53f7cdd9b5ea92f31b3ee9659ac5464c6239e'
assert before[1]['sha256']=='1813f631c996c89a90c0181a5c481c8f07b9a304c65e78d211083d4c98f13155'
assert before[2]['sha256']=='0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382'
assert before[3]['sha256']=='d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'
assert before[4]['sha256']=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
q=read(Q)
assert q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_HELPER_ACTUAL_CONTROLS_ADMISSION_V17'
assert q['status']=='QUALIFIED_PURE_COMPLETE_GRAPH_HELPER_METADATA_PROTOCOL_ONLY_V17'
ref_names=['helper','actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest']
references=[]
for name in ref_names:
    record=q[name];actual=pin(Path(record['path']))
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
src=U.read_text();original=src;edits=[]
def replace(old,new):
    global src
    assert src.count(old)==1
    src=src.replace(old,new)
    edits.append(dict(old=old,new=new,occurrences=1))
replace(src.splitlines()[0],repr('READY source-bound V17 complete sender/root-index fresh-wire and lossless trace-table combined runtime. The exact order-preserved helper has Root-qualified pure complete metadata protocol controls only; its source SHA and actual admission SHA are bound. Original whole seven historical INPUT bodies, literal owners, namespaces, aliases, absence, coverage, read attempts, kernel, sender and original budgets are retained. Qualified V15 complete86 component pins remain INPUT-only; failed V15 combined prepare grants no success. This new V17 combined prepare/build/whole INPUT/native/AAA/ABA has not executed and all future success pins remain None.'))
replace("DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V17_FULL_GRAPH_HELPER_AND_ACTUAL_CONTROLS_BINDING_REQUIRED'", "DRAFT_STATUS = 'READY_REVIEWED_V17_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'")
replace(" 'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py',None),", " 'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py','bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),")
replace('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None', "FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = 'd49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'")
compile(src,'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py','exec')
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
def definitions(source):return {n.name:ast.get_source_segment(source,n)for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert definitions(src)==definitions(original)
for name in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):
    assert src.count(name+' = None')==1
assert before==[pin(path)for path in inputs]
for record in references:assert pin(Path(record['actual']['path']))==record['actual']
C=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py'
with C.open('x')as f:f.write(src)
proof={'schema':'AXMAT_V17_READY_COMBINED_FOUR_SOURCE_BINDINGS_INVERSE_V1','status':'READY_SOURCE_BOUND_NOT_EXECUTED','inputs':before,'actual_helper_controls_admission':before[3],'actual_helper':before[4],'qualification_references_full_sha_identity7_verified':references,'source_inputs_before_after_equal':True,'qualification_references_before_after_equal':True,'candidate':pin(C),'edits':edits,'exact_four_source_bindings':True,'all_70_function_class_definitions_byteexact_to_UNREADY':True,'READY_complete_inverse_to_UNREADY_82b17014_exact':True,'complete_ancestry_inverse_to_parent_0ea1e629_exact':True,'actual_helper_protocol_qualified_only':True,'actual_root_terminal_typed_exit0_closed_verified':True,'Q_all_production_native_science_claims_false':True,'future_combined_native_six_success_pins_None':True,'source_compile_only':True,'project_written':False,'project_module_imported_or_executed':False,'numeric_payload_read':False,'resource_check_called':False,'new_combined_prepare_or_build_or_whole_INPUT_or_native_or_AAA_or_ABA_credit':False}
write(D/'source_binding_inverse_proof.json',proof)
report={'schema':'AXMAT_V17_COMPLETE_COMBINED_READY_SOURCE_BINDING_REPORT_V1','status':'READY_SOURCE_BOUND_ROOT_FRESH_BOUNDED_PREP_REQUIRED','candidate':pin(C),'helper_controls_admission':before[3],'helper':before[4],'actual_controls_scope':'pure complete metadata protocol only; not new production graph, combined build/INPUT or native/AAA/ABA','actual_protocol_counts':dict(old_trace_records=62332,new_trace_records=63379,old_requirement_rows=237767,old_canonical_files=36776,accepted_subtype_groups=2,rejections=61),'source_changes_only':['truthful docstring','DRAFT_STATUS to original require_ready V17 READY string','INPUT_HELPERS graph SHA None to actual qualified helper SHA','actual helper controls admission SHA None to actual Root Q SHA'],'whole_source_inverse_to_82_and_chain_0ea_exact':True,'all_original_function_bodies_exact_to_82':True,'all_remaining_source_and_component_real_pins_exact':True,'original_budgets_and_physical_inputs_unchanged':True,'fresh_V17_SOURCE_OUT_TERMINAL_HOST_namespaces_unchanged_from_UNREADY':True,'Q_false_production_science_fields':{key:q[key]for key in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')},'actual_new_combined_declaration_sha256':None,'actual_new_combined_prepare_terminal_sha256':None,'actual_new_combined_seal_sha256':None,'actual_new_combined_terminal_sha256':None,'actual_new_combined_runtime_sha256':None,'actual_new_native_terminal_sha256':None,'project_written':False,'project_module_imported_or_called':False,'business_executed':False,'next_action':'Root install exact READY candidate, preserve source inverse/Q binding proof, create a distinct original bounded V17 host, execute normal once fresh prepare; all actual combined success requires the new observed terminal and artifacts.'}
write(D/'REPORT.json',report)
print(json.dumps({'source_only_READY_binding':True,'business_executed':False,'output_dir':str(D),'candidate':pin(C),'proof':pin(D/'source_binding_inverse_proof.json'),'report':pin(D/'REPORT.json'),'four_edits_only':True,'all_function_bodies_unchanged':True,'inverse_82_and_0ea_exact':True},allow_nan=False))

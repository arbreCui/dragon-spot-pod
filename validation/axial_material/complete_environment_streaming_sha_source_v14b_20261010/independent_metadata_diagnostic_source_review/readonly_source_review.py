"""AST/text/source-proof read-only review; never import any reviewed module."""
import ast
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_v14b_metadata_timing_final_source_readonly_review_20261010')
S=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_metadata_control_sources')
G=Path('/private/tmp/axmat_v14b_bounded_metadata_timing_source_only_20261010')
T=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read_json(path):return json.loads(Path(path).read_bytes())
def function_records(source):
    records={}
    def walk(node,scope):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            scope=scope+(node.name,)
            if isinstance(node,ast.FunctionDef):records[scope]=ast.get_source_segment(source,node)
        for child in ast.iter_child_nodes(node):walk(child,scope)
    walk(ast.parse(source),())
    return records
binding_path=S/'Root_complete_metadata_source_binding_inverse.json';binding=read_json(binding_path)
sources={};bind_checks={}
for role,pin_expected,count in (('metadata_timing_driver','1dc516eae8ae43bcf94deee222970ad5a3bbf9d1e63b711f2be6874d94da8fae',3),('metadata_timing_host','91630f0d8c4f27e8f093e395b5e1d1cf3bcb6146c5bc253b40790ef7504334af',5)):
    item=binding['bindings'][role];path=Path(item['candidate']['path']);raw=path.read_bytes();source=raw.decode();assert sha(raw)==pin_expected
    assert len(item['edits'])==count
    inverse=source
    for edit in reversed(item['edits']):
        assert type(edit['count'])is int and edit['count']==1 and inverse.count(edit['new'])==1
        inverse=inverse.replace(edit['new'],edit['old'],1)
    original=Path(item['parent']['path']).read_bytes()
    assert inverse.encode()==original and sha(original)==item['parent']['sha256']
    assert function_records(source)==function_records(inverse)
    sources[role]=source
    bind_checks[role]=dict(path=str(path),sha256=pin_expected,bytes=len(raw),exact_binding_regions=count,complete_inverse_to_UNREADY=True,all_definitions_including_nested_byteexact=True)
driver=sources['metadata_timing_driver'];host=sources['metadata_timing_host']
dt=ast.parse(driver);ht=ast.parse(host)
def literal_assignment(tree,name):
    return next(node for node in tree.body if isinstance(node,ast.Assign)and any(isinstance(target,ast.Name)and target.id==name for target in node.targets))
assert literal_assignment(dt,'CANONICAL_TARGET').lineno<literal_assignment(dt,'TARGET_FACTORY').lineno
host_target=literal_assignment(ht,'TARGET_FACTORY');assert isinstance(host_target.value,ast.BinOp)and isinstance(host_target.value.left,ast.Name)and host_target.value.left.id=='ROOT'
assert literal_assignment(ht,'ROOT').lineno<host_target.lineno
host_proof_path=G/'HOST_COMPLETE_SOURCE_INVERSE.json';host_proof=read_json(host_proof_path)
host_unready=Path(binding['bindings']['metadata_timing_host']['parent']['path']).read_text();restored=host_unready
for edit in reversed(host_proof['edits']):
    assert restored.count(edit['new'])==edit['count'];restored=restored.replace(edit['new'],edit['old'],edit['count'])
host_original=Path(host_proof['parent_host']['path']).read_text()
assert restored==host_original and sha(restored.encode())==host_proof['parent_host']['sha256']
original_records=function_records(host_original);host_records=function_records(host)
support=('identity','pin','write_new','load','archive_bytes')
assert all(original_records[(name,)]==host_records[(name,)]for name in support)
assert set(original_records)==set(host_records)and [key for key in original_records if original_records[key]!=host_records[key]]==[('main',)]
raw=T.read_bytes();target=raw.decode();tt=ast.parse(target)
assert sha(raw)=='4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
tf={node.name:node for node in tt.body if isinstance(node,ast.FunctionDef)}
functions=ast.literal_eval(literal_assignment(dt,'FUNCTIONS').value)
support_names=ast.literal_eval(literal_assignment(dt,'SUPPORT').value)
assert functions==('sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs')
assert support_names==('require','read','pin','digest')
allowed=set(functions+support_names);calls={}
for name in allowed:
    calls[name]=sorted({node.func.id for node in ast.walk(tf[name])if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id in tf})
    assert set(calls[name])<=allowed
    assert not any(isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id in ('eval','exec','compile','__import__')for node in ast.walk(tf[name]))
profile_registry=next(node for node in dt.body if isinstance(node,ast.FunctionDef)and node.name=='profile_registry')
registry_source=ast.get_source_segment(driver,profile_registry)
assert 'for item in code.co_consts:'in registry_source and 'isinstance(item,types.CodeType):walk(item)'in registry_source
assert 'walk(fn.__code__)'in registry_source and "code.co_filename!=str(TARGET_FACTORY)"in registry_source
assert 'value.__module__==module.__name__'in registry_source and 'if code not in allowed'in registry_source
run=next(node for node in dt.body if isinstance(node,ast.FunctionDef)and node.name=='run_profile');run_source=ast.get_source_segment(driver,run)
assert "event not in ('call','return')"in run_source and "if code not in allowed:return"in run_source
assert "event=='call' and code in forbidden"in run_source
assert 'stack.append(dict(frame=id(frame)'in run_source and "stack[-1]['frame']!=id(frame)"in run_source
assert "elapsed-row['selected_children']"in run_source and "stack[-1]['selected_children']+=elapsed"in run_source
assert 'finally:\n        sys.setprofile(None)'in run_source
assert 'for name in FUNCTIONS:'in run_source and 'direct[name]+=1;value=getattr(module,name)()'in run_source
assert "row['calls']!=row['returns']"in run_source and "row['exclusive_selected_canonical_ns']<0"in run_source
assert "except BaseException as error:"in driver and "        raise\n"in driver
# Every metadata dependency family comes from its pinned source/JSON owner;
# no reviewed function is called to construct this enumeration.
enumeration=ast.get_source_segment(driver,next(node for node in dt.body if isinstance(node,ast.FunctionDef)and node.name=='source_input_pins'))
expected_assignment=next(node for node in tf['source_inputs'].body if isinstance(node,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='expected'for t in node.targets))
assert isinstance(expected_assignment.value,ast.Dict)and all(isinstance(n,ast.Name)for n in expected_assignment.value.keys+expected_assignment.value.values)
assert "zip(assignment.value.keys,assignment.value.values)"in enumeration
assert "controls['files'].items()"in enumeration and "for key in ('author_source_review','author_actual_source_terminal_receipt')"in enumeration
assert "senderinput['original_receiver']['path']"in enumeration
assert "'FLUSP64.candidate_unit.f',proof['candidate_wrapper_sha256']"in enumeration
assert "'FLUSP64.original_reference_unit.f',proof['reference_wrapper_sha256']"in enumeration
assert "parent=module.PARENT/'declaration.json'"in enumeration and "add(parent,pin(parent)['sha256'])"in enumeration
base=Path('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009')
sender_proof=read_json(base/'source_patch_proof.json');sender_input=read_json(base/'source_admission_INPUT.json')
assert sender_proof['candidate_wrapper_sha256']=='e4f6beac894a62f9dc463b787bfe1d0b9673bc9eb8bebcef9470e3e7e885d2e3'
assert sender_proof['reference_wrapper_sha256']=='52b1db5a5ea73de548e437386798099cdb28b7c28cd98f0de21e949973266043'
assert sender_input['original_receiver']['sha256']=='876eed542d97a368dd40e00ff92b1310cd106b03cbf766b618afda74f8566df2'
for fragment in ("full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)","h.guard_admission(full)","resource_factory.history_roots([str(host_root), str(control_root)], ART)","resource_factory.resources_for(roots, production.ResourceFailure)","type(runner) is not full.OwnRSSSerialExecutor","runner.resources is not resources","runner.execute(host_root / 'run', 'metadata', command, remaining)"):
    assert fragment in host
assert ast.literal_eval(literal_assignment(ht,'WALL_CAP').value)==120 and ast.literal_eval(literal_assignment(ht,'RSS_CAP').value)==512
assert 'ARCHIVE_CAP = 64 * 2**20'in host and '96 * 2**30'in host and '8 * 2**30'in host
assert "'threads':1,'children_at_once':1,'retries':0"in host
assert "Path(runner.bounded.__file__).resolve() != host_root / 'runtime/run_bounded_dragon.py'"in host
assert "old_failed_V13_factory_imported_or_called':False"in host
assert "for entry in inputs:"in host and "pin(entry['path'], entry['sha256']) != entry"in host
assert 'pin(TARGET_FACTORY,TARGET_FACTORY_SHA256)!=source'in driver and "pin(row['path'],row['sha256'])!=row"in driver
assert "plain_return(value)"in driver and "complete_return=pin(path)"in driver
assert 'spec.loader.exec_module(module)'in driver and 'Path(module.__file__)!=CANONICAL_TARGET or module.ROOT!=ROOT'in driver
top_calls=[node for node in tt.body if not isinstance(node,(ast.FunctionDef,ast.ClassDef,ast.Import,ast.ImportFrom))and any(isinstance(x,ast.Call)for x in ast.walk(node))]
assert len(top_calls)==4 and isinstance(top_calls[-1],ast.If)and "__name__ == \"__main__\""in ast.get_source_segment(target,top_calls[-1])
assert all(not isinstance(node,ast.Expr)or isinstance(node.value,ast.Constant)for node in dt.body)
assert all(not isinstance(node,ast.Expr)or isinstance(node.value,ast.Constant)for node in ht.body)
report=dict(status='PASS_FINAL_BOUND_METADATA_DIAGNOSTIC_SOURCE_ONLY_REVIEW',binding_proof=dict(path=str(binding_path),sha256=sha(binding_path.read_bytes())),bound_sources=bind_checks,host_complete_inverse=dict(path=str(host_proof_path),sha256=sha(host_proof_path.read_bytes()),regions=len(host_proof['edits'])),host_original5_support_definitions_byteexact=True,host_only_main_definition_changed=True,final_binding_definition_order_valid=True,canonical_target=dict(path=str(T),sha256=sha(raw)),normal_canonical_import_top_level_stdlib_and_constant_metadata_only=True,no_old_failed_factory_import_or_API_in_the_four_paths=True,allowed_direct_functions=functions,allowed_support_functions=support_names,canonical_global_call_graph=calls,all_actual_nested_code_objects_registered_recursively=True,selected_generator_call_return_events_are_resume_yield_intervals=True,selected_generator_counts_are_profile_events_not_distinct_generator_construction_counts=True,selected_frame_stack_and_exclusive_child_subtraction_valid=True,stdlib_C_and_profiler_cost_not_removed=True,original_metadata_exception_propagates_and_profile_finally_cleared=True,complete_return_serialization_preserves_all_fields=True,source_input_owner_map_entries_statically_enumerated=len(expected_assignment.value.keys),sender_units_receiver_source_proof_control_inventory_and_parent_declaration_dependency_families_covered=True,all_declared_regular_literal_SHA_and7ID_before_after_required=True,genuine_original619_FULL705_parent38de_boundedbc_f136_resource_and_guard_route_preserved=True,original_MRO_120_512_64MiB_96GiB_free8_thread1_child1_retry0_preserved=True,unknown_actual_measurements_not_inferred=True,fresh_ART_namespace_check='Root reported pre-start real readonly afa17e; this review does not require roots to remain absent after Root starts its sole diagnostic.',deterministic_source_blockers=[],source_judgment='Source compatible with Root single bounded read-only metadata diagnostic; actual runtime success remains unknown to this review.',business_modules_imported_by_this_review=False,candidate_or_helper_or_profile_or_gate_executed_by_this_review=False,fixtures_or_benchmark_or_component_executed_by_this_review=False,Root_polled=False,canonical_write=False,old35GB_input_hashing=False,original86_stage_count_increment=0,component_native_AAA_ABA_credit=False)
D.mkdir(parents=True,exist_ok=True);(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,allow_nan=False))

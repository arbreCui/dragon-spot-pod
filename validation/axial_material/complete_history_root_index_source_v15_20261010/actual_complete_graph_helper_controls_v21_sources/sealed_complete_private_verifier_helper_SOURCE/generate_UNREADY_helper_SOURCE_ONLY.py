"""Generate a full private verifier lifetime SOURCE proposal, never execute helper/API."""
import ast
import hashlib
import json
from pathlib import Path
import stat

DEST=Path(__file__).parent
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
PARENT_SHA='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')
FACTORY_SHA='566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3'
CANDIDATE=DEST/'combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.UNREADY.py'

def pin(path,expected):
    if '/validation/artifacts/' in str(path) or path.resolve()!=path:raise ValueError('ordinary SOURCE only; no ART')
    a=path.lstat()
    if not stat.S_ISREG(a.st_mode) or a.st_nlink!=1:raise ValueError('unique regular SOURCE required')
    data=path.read_bytes();b=path.lstat()
    identity=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    if identity(a)!=identity(b) or len(data)!=b.st_size or hashlib.sha256(data).hexdigest()!=expected:raise ValueError('complete fresh SOURCE SHA7ID mismatch')
    return data,dict(path=str(path),sha256=expected,identity=identity(b))

def write_new(path,data):
    with path.open('xb') as f:f.write(data)

def json_bytes(v):return (json.dumps(v,indent=2,allow_nan=False)+'\n').encode()

def main():
    parent,parent_pin=pin(PARENT,PARENT_SHA);factory,factory_pin=pin(FACTORY,FACTORY_SHA)
    source=parent.decode();lines=source.splitlines(keepends=True);tree=ast.parse(source)
    definitions={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    rules={
      'verify_graph':[
        ('    owners = _owners(_expand_owner_table(graph["owners"], graph["requirements"]))\n',
         '    owners = _owners(_expand_owner_table(graph["owners"], graph["requirements"]))\n    if consumer is None:\n        # This graph was freshly parsed or cloned here. Full content/owner gates\n        # above completed; the normalized owners remain whole for the phase.\n        del graph["owners"]\n'),
        ('    namespaces = [_namespace_descriptor(value) for value in graph["namespaces"]]\n',
         '    namespaces = [_namespace_descriptor(value) for value in graph["namespaces"]]\n    if consumer is None:\n        # Every complete descriptor has passed its original clone/validation.\n        # All later namespace checks consume the full normalized local list.\n        del graph["namespaces"]\n'),
        ('    _require(new_pins == frozen_new, "newly declared input bytes changed")\n',
         '    _require(new_pins == frozen_new, "newly declared input bytes changed")\n    if consumer is None:\n        # Original complete rebuilt requirements, every canonical pin and new\n        # pin predicates above all passed in order. Neither saved section has\n        # a later use on this complete branch; fresh requirements/actual stay.\n        del graph["requirements"], graph["canonical_files"]\n'),
        ('_trace_records(graph["read_trace"]["records"] if consumer is not None else graph["read_trace"])',
         '_trace_records(graph["read_trace"]["records"] if consumer is not None else graph["read_trace"],\n                                                   _consume=consumer is None)')],
      '_trace_records':[
        ('def _trace_records(values):\n','def _trace_records(values, *, _consume=False):\n'),
        ('    _require(isinstance(values, (list, tuple)), "read trace must be a list or audit descriptor")\n    result = []\n',
         '    _require(isinstance(values, (list, tuple)), "read trace must be a list or audit descriptor")\n    # Only verify_graph passes True, for its fresh parsed/cloned builtin graph.\n    # Default callers retain the complete original non-consuming behavior.\n    _require(type(_consume) is bool and (not _consume or type(values) is list),\n             "private trace consume needs a bool and an exclusively owned builtin list")\n    result = []\n    consumed_index = 0\n'),
        ('        result.append(record)\n    return result\n',
         '        result.append(record)\n        if _consume:\n            # All original record predicates and the complete clone/append\n            # have finished. Release this one private old row, never a result.\n            values[consumed_index] = None\n        consumed_index += 1\n    if _consume:\n        values.clear()\n    return result\n')],
      '_phase':[
        ('            add(path, digest, owner["owner"], owner["category"], NEW_INPUT_ROLE)\n    for alias in aliases.values():\n',
         '            add(path, digest, owner["owner"], owner["category"], NEW_INPUT_ROLE)\n    # Both owner passes and every add() are complete. The records keep their\n    # full path fields; these local containers/closure pool are no longer read.\n    owner = None\n    del owners, deferred_owner_inputs, literal_paths\n    for alias in aliases.values():\n'),
        ('        ordered_canonical_paths.append(json_canonical)\n    actual = {}\n',
         '        ordered_canonical_paths.append(json_canonical)\n    # Canonical membership and optional parent placement have completed.\n    # Every distinct canonical endpoint remains in the full ordered sequence.\n    del canonical_paths\n    actual = {}\n'),
        ('        if collect_json:\n            fresh_json_payload = payload\n    for path, canonical in resolved_paths.items():\n',
         '        if collect_json:\n            fresh_json_payload = payload\n    # The complete union EOF/SHA checks consumed every expected pin.\n    # Retain actual and resolved paths for all original post-read checks.\n    del expectations, ordered_canonical_paths\n    for path, canonical in resolved_paths.items():\n'),
        ('        new_pins[path] = actual[canonical]["sha256"]\n    # Namespace and alias metadata are checked again after all byte reads.  This\n',
         '        new_pins[path] = actual[canonical]["sha256"]\n    # Literal endpoint checks and every new-pin lookup are complete.\n    del resolved_paths\n    # Namespace and alias metadata are checked again after all byte reads.  This\n')]
    }
    changes=[];replacements={}
    for name,edits in rules.items():
        node=definitions[name];old=''.join(lines[node.lineno-1:node.end_lineno]);new=old
        for before,after in edits:
            if new.count(before)!=1:raise ValueError('exact one local SOURCE edit required: '+name)
            new=new.replace(before,after,1)
            changes.append(dict(function=name,before=before,after=after,count=1))
        replacements[name]=(old,new)
    candidate=source
    for name in sorted(replacements,key=lambda n:definitions[n].lineno,reverse=True):
        old,new=replacements[name]
        if candidate.count(old)!=1:raise ValueError('complete unique function SOURCE replacement required')
        candidate=candidate.replace(old,new,1)
    backward=candidate
    for r in reversed(changes):
        if backward.count(r['after'])!=1:raise ValueError('whole-byte local inverse count required')
        backward=backward.replace(r['after'],r['before'],1)
    if backward.encode()!=parent:raise ValueError('entire new helper inverse to bcd required')
    new_tree=ast.parse(candidate);compile(candidate,str(CANDIDATE),'exec')
    new_defs={n.name:n for n in new_tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    if list(new_defs)!=list(definitions):raise ValueError('all top-level original definitions retained')
    new_lines=candidate.splitlines(keepends=True)
    matrix=[]
    for name,node in definitions.items():
        other=new_defs[name];old=''.join(lines[node.lineno-1:node.end_lineno]);new=''.join(new_lines[other.lineno-1:other.end_lineno])
        changed=old!=new
        if changed!=(name in rules):raise ValueError('only three named functions may change')
        matrix.append(dict(name=name,old_line=node.lineno,new_line=other.lineno,old_sha256=hashlib.sha256(old.encode()).hexdigest(),new_sha256=hashlib.sha256(new.encode()).hexdigest(),byte_unchanged=not changed))
    # Original control/call/return nodes must appear in their original SOURCE AST
    # walk sequence. The one old _trace_records call receives the private flag;
    # other original calls are exact. New private flag guard/clear calls are listed.
    def existing_calls(tree):return [ast.dump(n,include_attributes=False)for n in ast.walk(tree)if isinstance(n,ast.Call)]
    call_proofs=[];control_proofs=[];return_proofs=[]
    for name in rules:
        old_node=definitions[name];new_node=new_defs[name]
        old_calls=existing_calls(old_node)
        if name=='verify_graph':
            normalized=ast.parse(replacements[name][0]).body[0]
            for n in ast.walk(normalized):
                if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='_trace_records':
                    n.keywords.append(ast.keyword(arg='_consume',value=ast.Compare(left=ast.Name(id='consumer',ctx=ast.Load()),ops=[ast.Is()],comparators=[ast.Constant(value=None)])))
            old_calls=existing_calls(normalized)
        new_calls=existing_calls(new_node)
        cursor=0
        for call in new_calls:
            if cursor<len(old_calls)and call==old_calls[cursor]:cursor+=1
        if cursor!=len(old_calls):raise ValueError('original AST call sequence cannot be retained: '+name)
        call_proofs.append(dict(function=name,old_call_count=len(old_calls),new_call_count=len(new_calls),original_calls_in_order=True,only_original_call_signature_change='_trace_records private _consume=consumer is None'if name=='verify_graph'else None))
        old_controls=[ast.dump(n,include_attributes=False)for n in ast.walk(old_node)if isinstance(n,(ast.If,ast.Assert,ast.Raise))]
        # Enclosing If ASTs include their complete bodies; remove only the added
        # lifetime nodes by exact inverse before comparing all old control ASTs.
        restored=ast.parse(backward).body
        restored_node=next(n for n in restored if isinstance(n,ast.FunctionDef)and n.name==name)
        restored_controls=[ast.dump(n,include_attributes=False)for n in ast.walk(restored_node)if isinstance(n,(ast.If,ast.Assert,ast.Raise))]
        if old_controls!=restored_controls:raise ValueError('all original complete control bodies inverse exact required')
        old_raises=[ast.dump(n,include_attributes=False)for n in ast.walk(old_node)if isinstance(n,(ast.Assert,ast.Raise))]
        new_raises=[ast.dump(n,include_attributes=False)for n in ast.walk(new_node)if isinstance(n,(ast.Assert,ast.Raise))]
        if old_raises!=new_raises:raise ValueError('all original Assert/Raise exact required')
        old_tests=[ast.dump(n.test,include_attributes=False)for n in ast.walk(old_node)if isinstance(n,ast.If)]
        new_tests=[ast.dump(n.test,include_attributes=False)for n in ast.walk(new_node)if isinstance(n,ast.If)]
        cursor=0
        for test in new_tests:
            if cursor<len(old_tests)and test==old_tests[cursor]:cursor+=1
        if cursor!=len(old_tests):raise ValueError('original If test sequence retained required')
        control_proofs.append(dict(function=name,old_If_count=len(old_tests),new_If_count=len(new_tests),all_original_If_test_sequence_unchanged=True,all_original_Assert_Raise_exact=True,enclosing_If_AST_not_identical_because_new_last_use_statements_are_in_bodies=True,entire_original_control_body_restored_by_inverse=True))
        returns=lambda node:[ast.dump(n,include_attributes=False)for n in ast.walk(node)if isinstance(n,ast.Return)]
        if returns(old_node)!=returns(new_node):raise ValueError('all complete original return expressions exact required')
        return_proofs.append(dict(function=name,return_count=len(returns(old_node)),all_original_return_expressions_exact=True))
    # No READ/OpenAudit/codecs/parser/limits/constants or consumer helpers change.
    top_nonfunctions=lambda tree:[ast.dump(n,include_attributes=False)for n in tree.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    if top_nonfunctions(tree)!=top_nonfunctions(new_tree):raise ValueError('all globals/classes/imports/nonfunction nodes exact required')
    all_functions=lambda tree:[n for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    if len(all_functions(tree))!=len(all_functions(new_tree)):raise ValueError('complete all nested/method definition count retained')
    for path,expected,ref in [(PARENT,PARENT_SHA,parent_pin),(FACTORY,FACTORY_SHA,factory_pin)]:
        _,again=pin(path,expected)
        if ref!=again:raise ValueError('fresh SOURCE inputs changed')
    candidate_sha=hashlib.sha256(candidate.encode()).hexdigest()
    proof=dict(schema='AXMAT_UNREADY_PRIVATE_VERIFIER_LIFETIME_COMPLETE_SOURCE_INVERSE_V1',status='UNREADY_SOURCE_ONLY_NEW_HELPER_REQUIRES_INDEPENDENT_PURE_PROTOCOL_QUALIFICATION',parent=parent_pin,candidate_path=str(CANDIDATE),candidate_sha256=candidate_sha,changes=changes,local_edit_count=len(changes),changed_top_level_functions=list(rules),all_top_level_definition_count=len(definitions),all_nested_and_method_definition_count=len(all_functions(tree)),complete_definition_matrix=matrix,original_call_sequence_proofs=call_proofs,original_control_sequence_proofs=control_proofs,original_return_proofs=return_proofs,all_module_globals_classes_imports_and_other_statements_exact=True,entire_byte_inverse_to_bcd=True,private_consume_default=False,only_True_callsite='verify_graph, consumer is None, graph freshly strict_json-parsed or _json_clone-owned',consumer_branch_saved_sections_and_nonconsuming_trace_semantics_retained=True,unique_new_semantic_rejection_guard='type(_consume) is bool and (not _consume or type(values) is list)',full_each_record_validation_clone_append_precedes_original_row_clear=True,complete_normalized_trace_return_retained=True,no_new_IO_or_skip_or_memo_or_gc_or_allocator_bypass=True,existing_all_full_phases_roots_original_caps_and_science_flags_retained=True,actual_NEW_helper_qualification_sha256=None,actual_NEW_combined_decl_build_admission_native_pins=None,candidate_imported_or_executed=False,helper_API_guard_resource_or_business_called=False,ART_read_or_written=False,numeric_payload_read=False,actual_peak_source_line_observed=False,actual_build_success_or_science_credit=False)
    factory_source=factory.decode();flines=factory_source.splitlines(keepends=True);fdefs={n.name:n for n in ast.parse(factory_source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    excerpts={name:dict(start_line=fdefs[name].lineno,end_line=fdefs[name].end_lineno,complete_SOURCE=''.join(flines[fdefs[name].lineno-1:fdefs[name].end_lineno]))for name in ('run_build','declaration_admission','environment','verify_inputs','complete_input_phase','prepare_terminal_admission','current_new_owned_paths','current_input_predicates','graph_input_bindings','minimal_live_specs','failed_prepare_input','check_failed_prepare_phase','audit_build','binary_audit','stage_commands','current_trim_predicates','strict_json_bytes','read','component_support_contract','trim_component_contract','actual_components','prepare_build')}
    write_new(CANDIDATE,candidate.encode())
    write_new(DEST/'frozen_parent_complete_helper_bcd.py',parent)
    write_new(DEST/'full_finite_source_inverse_proof.json',json_bytes(proof))
    write_new(DEST/'complete_factory_direct_SOURCE_excerpts.json',json_bytes(dict(factory=factory_pin,read_scope='complete run_build and finite directly reached SOURCE only',functions=excerpts)))
    print(json.dumps(dict(status=proof['status'],candidate=str(CANDIDATE),candidate_sha256=candidate_sha,local_edits=len(changes),changed_functions=list(rules),all_top_level_definitions=len(definitions),all_nested_method_definitions=len(all_functions(tree)),full_inverse_bcd=True,candidate_imported_or_executed=False,business_executed=False,actual_NEW_helper_qualification_sha256=None)))

if __name__=='__main__':main()

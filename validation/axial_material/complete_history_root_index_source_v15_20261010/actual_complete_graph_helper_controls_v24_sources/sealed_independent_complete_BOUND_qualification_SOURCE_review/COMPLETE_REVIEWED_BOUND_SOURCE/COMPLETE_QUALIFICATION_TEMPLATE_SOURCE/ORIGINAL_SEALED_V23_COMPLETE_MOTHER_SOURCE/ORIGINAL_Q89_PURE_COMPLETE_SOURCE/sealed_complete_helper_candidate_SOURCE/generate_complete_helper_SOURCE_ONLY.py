#!/usr/bin/env python3
"""Generate SOURCE only; never import/compile/execute the helper."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import stat

OUT = Path(__file__).resolve().parent
PARENT = Path("/private/tmp/axmat_v22_complete_build_last_use_SOURCE_analysis_20261010_l8q3p/complete_helper.frozen_SOURCE.py")
PARENT_SHA = "dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7"
MATRIX_MANIFEST = Path("/private/tmp/axmat_v22_complete_build_last_use_SOURCE_analysis_20261010_l8q3p/MANIFEST.json")
MATRIX_MANIFEST_SHA = "11dcdd1e07a5e7038835c348951ef3292e25a20b75a59c8a9808a499ce6547b7"
TARGET = OUT / "combined_runtime_complete_input_graph_private_owner_namespace_last_use_v22.UNREADY.py"

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def read_source(p):
    before = p.lstat()
    assert stat.S_ISREG(before.st_mode) and not p.is_symlink()
    value = p.read_bytes()
    after = p.lstat()
    assert identity(before) == identity(after) and len(value) == before.st_size
    return value, {"path":str(p), "sha256":hashlib.sha256(value).hexdigest(),
                   "identity":identity(after), "bytes":len(value)}

def write_json(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")

def dump(n):
    return ast.dump(n, include_attributes=False)

def function_source(text, node):
    return "".join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

parent_bytes, parent_pin = read_source(PARENT)
assert parent_pin["sha256"] == PARENT_SHA
matrix_bytes, matrix_pin = read_source(MATRIX_MANIFEST)
assert matrix_pin["sha256"] == MATRIX_MANIFEST_SHA
old = parent_bytes.decode("utf-8")
edits = [
    {"id":"1_private_keyword_only_owner_flag_default_false",
     "old":"def _owners(values):\n",
     "new":"def _owners(values, *, _consume=False):\n"},
    {"id":"2_private_exclusive_builtin_list_flag_guard",
     "old":'    """Normalize only documented typed fields; never inspect arbitrary strings."""\n    result = []\n',
     "new":'    """Normalize only documented typed fields; never inspect arbitrary strings."""\n'
           '    # Only verify_graph enables this for its fresh expanded complete owner list.\n'
           '    # Every default and consumer caller retains the original non-consuming path.\n'
           '    _require(type(_consume) is bool and (not _consume or type(values) is list),\n'
           '             "private owner consume needs a bool and an exclusively owned builtin list")\n'
           '    result = []\n'
           '    consumed_index = 0\n'},
    {"id":"3_complete_original_owner_validate_normalize_append_then_consume_old_row",
     "old":"        result.append(descriptor)\n    return result\n\n\ndef _new_inputs(values):\n",
     "new":"        result.append(descriptor)\n"
           "        if _consume:\n"
           "            # The complete original validation, normalization and append passed.\n"
           "            # End this private expanded row only; the full result stays intact.\n"
           "            values[consumed_index] = None\n"
           "        consumed_index += 1\n"
           "    if _consume:\n"
           "        values.clear()\n"
           "    return result\n\n\ndef _new_inputs(values):\n"},
    {"id":"4_verify_only_complete_private_owner_list_consumed",
     "old":'    owners = _owners(_expand_owner_table(graph["owners"], graph["requirements"]))\n',
     "new":'    owners = _owners(_expand_owner_table(graph["owners"], graph["requirements"]),\n'
           '                     _consume=consumer is None)\n'},
    {"id":"5_after_complete_phase_and_second_absence_private_namespace_lastuse",
     "old":'    _absence_phase(absent_inputs, aliases, expected=graph["absence_observations"])\n'
           '    rebuilt_requirements = (_wire_requirement_table_compact(requirements) if wire\n',
     "new":'    _absence_phase(absent_inputs, aliases, expected=graph["absence_observations"])\n'
           '    if consumer is None:\n'
           '        # Both full namespace scans and the original second absence check passed.\n'
           '        # Trace coverage only needs canonical_root; the original return needs\n'
           '        # the complete count. Consumer lineage retains all original fields.\n'
           '        for namespace in namespaces:\n'
           '            del namespace["files"], namespace["symlinks"], namespace["directories"]\n'
           '    rebuilt_requirements = (_wire_requirement_table_compact(requirements) if wire\n'},
]
new = old
for e in edits:
    assert new.count(e["old"]) == 1, e["id"]
    new = new.replace(e["old"], e["new"], 1)
candidate = new.encode("utf-8")
assert not TARGET.exists()
TARGET.write_bytes(candidate)
(OUT/"parent_dc01.complete.frozen_SOURCE.py").write_bytes(parent_bytes)

reversed_text = new
for e in reversed(edits):
    assert reversed_text.count(e["new"]) == 1, e["id"]
    reversed_text = reversed_text.replace(e["new"], e["old"], 1)
assert reversed_text.encode("utf-8") == parent_bytes

old_ast, new_ast, restored_ast = ast.parse(old), ast.parse(new), ast.parse(reversed_text)
assert dump(old_ast) == dump(restored_ast)
old_funcs = {n.name:n for n in old_ast.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
new_funcs = {n.name:n for n in new_ast.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
assert list(old_funcs) == list(new_funcs) and len(old_funcs) == 79
all_function_or_method_count = sum(isinstance(n, (ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(new_ast))
assert all_function_or_method_count == 92
changed_names = [name for name in old_funcs if function_source(old,old_funcs[name]) != function_source(new,new_funcs[name])]
assert changed_names == ["_owners","verify_graph"]
unchanged = []
for name in old_funcs:
    if name not in changed_names:
        a, b = function_source(old,old_funcs[name]).encode(),function_source(new,new_funcs[name]).encode()
        assert a == b and dump(old_funcs[name]) == dump(new_funcs[name])
        unchanged.append({"name":name,"sha256":hashlib.sha256(a).hexdigest(),"bytes":len(a)})
old_other = [n for n in old_ast.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
new_other = [n for n in new_ast.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
assert [dump(n) for n in old_other] == [dump(n) for n in new_other]
assert dump(old_funcs["verify_graph"].args) == dump(new_funcs["verify_graph"].args)
owners_args = copy.deepcopy(new_funcs["_owners"].args)
assert len(owners_args.kwonlyargs) == 1 and owners_args.kwonlyargs[0].arg == "_consume"
assert dump(owners_args.kw_defaults[0]) == dump(ast.Constant(value=False))
owners_args.kwonlyargs,owners_args.kw_defaults = [],[]
assert dump(owners_args) == dump(old_funcs["_owners"].args)

def returns(fn):
    return [n for n in ast.walk(fn) if isinstance(n,ast.Return)]
old_ret,new_ret = returns(old_funcs["verify_graph"]),returns(new_funcs["verify_graph"])
assert len(old_ret)==len(new_ret)==1
assert function_source(old,old_ret[0]) == function_source(new,new_ret[0])
assert dump(old_ret[0]) == dump(new_ret[0])
assert isinstance(new_ret[0].value,ast.Dict)
fields = [k.value for k in new_ret[0].value.keys]
assert len(fields)==27

# Exact AST projection discloses every added private control/operation. It is
# stricter than counting original If/Assert/Raise/Call nodes in the larger AST.
projected = copy.deepcopy(new_ast)
pf = {n.name:n for n in projected.body if isinstance(n,ast.FunctionDef)}
po = pf["_owners"]
assert isinstance(po.body[0],ast.Expr) and isinstance(po.body[0].value,ast.Constant)
guard = po.body[1]
assert isinstance(guard,ast.Expr) and isinstance(guard.value,ast.Call)
assert isinstance(guard.value.func,ast.Name) and guard.value.func.id == "_require"
assert isinstance(po.body[3],ast.Assign) and po.body[3].targets[0].id == "consumed_index"
loop = po.body[4]
assert isinstance(loop,ast.For)
private_if,private_aug = loop.body[-2],loop.body[-1]
assert isinstance(private_if,ast.If) and dump(private_if.test)==dump(ast.Name(id="_consume",ctx=ast.Load()))
assert isinstance(private_aug,ast.AugAssign) and private_aug.target.id=="consumed_index"
loop.body=loop.body[:-2]
tail_if = po.body[5]
assert isinstance(tail_if,ast.If) and dump(tail_if.test)==dump(ast.Name(id="_consume",ctx=ast.Load()))
po.body=[po.body[0],po.body[2],loop,po.body[6]]
po.args.kwonlyargs,po.args.kw_defaults=[],[]
pv=pf["verify_graph"]
owner_stmt=next(n for n in pv.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="owners")
owner_call=owner_stmt.value
assert isinstance(owner_call,ast.Call) and isinstance(owner_call.func,ast.Name) and owner_call.func.id=="_owners"
assert len(owner_call.keywords)==1 and owner_call.keywords[0].arg=="_consume"
assert dump(owner_call.keywords[0].value)==dump(ast.parse("consumer is None",mode="eval").body)
owner_call.keywords=[]
ns_candidates=[]
for n in pv.body:
    if isinstance(n,ast.If) and dump(n.test)==dump(ast.parse("consumer is None",mode="eval").body):
        if len(n.body)==1 and isinstance(n.body[0],ast.For) and isinstance(n.body[0].body[0],ast.Delete):
            ns_candidates.append(n)
assert len(ns_candidates)==1
release=ns_candidates[0]
assert len(release.body[0].body[0].targets)==3
assert [t.slice.value for t in release.body[0].body[0].targets]==["files","symlinks","directories"]
release_index = pv.body.index(release)
prior=pv.body[release_index-1]
assert isinstance(prior,ast.Expr) and isinstance(prior.value,ast.Call) and prior.value.func.id=="_absence_phase"
assert any(isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and getattr(n.value.func,"id",None)=="_phase" for n in pv.body[:release_index])
assert getattr(pv.body[release_index+1].targets[0],"id",None)=="rebuilt_requirements"
pv.body.remove(release)
assert dump(projected)==dump(old_ast)

def ordered_control_nodes(fn):
    result=[]
    def walk(n):
        if isinstance(n,(ast.If,ast.Assert,ast.Raise,ast.Call,ast.Return)):
            result.append({"node":type(n).__name__,"AST":dump(n)})
        for child in ast.iter_child_nodes(n):walk(child)
    walk(fn)
    return result
controls={}
for name in changed_names:
    old_seq=ordered_control_nodes(old_funcs[name])
    projected_seq=ordered_control_nodes(pf[name])
    assert old_seq==projected_seq
    controls[name]={"all_original_ordered_If_Assert_Raise_Call_Return_after_explicit_private_projection_equal":True,
                    "original_counts":{k:sum(v["node"]==k for v in old_seq) for k in ["If","Assert","Raise","Call","Return"]},
                    "original_ordered_nodes":old_seq}
# All original _owners calls except this one verifier keyword retain full AST.
old_calls=[dump(n) for n in ast.walk(old_ast) if isinstance(n,ast.Call) and getattr(n.func,"id",None)=="_owners"]
new_calls=[n for n in ast.walk(new_ast) if isinstance(n,ast.Call) and getattr(n.func,"id",None)=="_owners"]
assert len(old_calls)==len(new_calls)
assert sum(any(k.arg=="_consume" for k in n.keywords) for n in new_calls)==1
trace_func = new_funcs["_trace_coverage"]
namespace_comps=[n for n in ast.walk(trace_func) if isinstance(n,ast.ListComp) and any(isinstance(x,ast.Name) and x.id=="namespaces" for x in ast.walk(n))]
assert len(namespace_comps)==1
assert dump(namespace_comps[0])==dump(ast.parse('[entry["canonical_root"] for entry in namespaces]',mode="eval").body)

inverse={"schema":"AXMAT_V22_PRIVATE_OWNER_NAMESPACE_COMPLETE_SOURCE_FINITE_INVERSE_V1",
         "status":"UNREADY_SOURCE_ONLY_NEW_HELPER_Q_REQUIRED",
         "parent":parent_pin,
         "candidate":{"path":str(TARGET),"sha256":hashlib.sha256(candidate).hexdigest(),"bytes":len(candidate)},
         "edits":edits,"edit_count":len(edits),"inverse_all_bytes_to_dc01":True,
         "inverse_full_AST_to_dc01":True,"explicit_private_AST_projection_full_module_to_dc01":True,
         "top_level_definitions":79,"all_function_or_method_definitions":92,
         "original_definition_name_order_exact":True,"changed_functions":changed_names,
         "unchanged_77_function_fullbytes_and_AST":unchanged,
         "all_nonfunction_top_level_nodes_and_globals_AST_exact":True,
         "original_verify_signature_exact":True,
         "original_owner_positional_signature_exact_and_new_private_kwonly_defaultFalse":True,
         "verify_return_full_SOURCE_bytes_and_AST_exact":True,"verify_return_field_count":27,
         "verify_return_field_order":fields,"control_preservation":controls,
         "private_extra_control_scope":[
             "_owners new flag/list guard _require call",
             "_owners private index local plus two private if controls and index update",
             "only verify_graph one _consume=consumer is None keyword",
             "verify_graph consumerNone-only namespace loop deleting three private dead fields"
         ],
         "original_expand_owner_table_namespace_descriptor_phase_trace_coverage_all_bytes_exact":True,
         "tuple_requirements_consumption_included":False}
write_json("COMPLETE_SOURCE_INVERSE.json",inverse)
exact_segments={}
for name in ["_owners","verify_graph","_expand_owner_table","_namespace_descriptor","_phase","_trace_coverage","_consumer_lineage","_json_clone","_path","_label","_trace_records"]:
    exact_segments[name]={"original":function_source(old,old_funcs[name]),"candidate":function_source(new,new_funcs[name])}
write_json("EXACT_FULL_FUNCTION_SOURCE_CONTRACTS.json",exact_segments)
qualification={"schema":"AXMAT_V22_SOURCE_CANDIDATE_FUTURE_REAL_QUALIFICATION_PLAN_V1",
               "status":"UNREADY_NEVER_EXECUTED_NO_OLD_Q_REUSE",
               "new_helper_Q":None,"six_future_business_pins":[None]*6,
               "old_dc01_and_29ac_immutable_not_applied_to_candidate":True,
               "Root_is_only_actual_executor":True,
               "next_requirements":[
                   "independent full SOURCE finiteinverse/public27/default/consumer review",
                   "Root fresh newnamespace actual original full60 bounded protocol, retaining all old accepted subtypes/rejects and full strict types/order/floatbits/default nonmutation",
                   "new private owner _consume opt-in accepted list result/default nonmutation and invalid nonbool/list-subclass/tuple opt-in rejects; exact actual negative receipts, no skipped old controls",
                   "Root fresh complete current graph genuine bounded probe with all27 fields/nestedorder/floatbits, complete allread trace and lossless gzip and Source/graph pins",
                   "independent saved actual protocol and fullcurrentgraph metadata evidence reviews",
                   "Root new joint qualification with actual helper path/fullEOF SHA7ID and both closed real terminals before new canonical binding"
               ],
               "original_caps_not_changed":True,"scientific_or_wholeINPUT_native_AAA_ABA_credit":False,
               "observed_peak_source_line":None,"RSS_prediction":None,"candidate_API_or_guard_run":False}
write_json("FUTURE_REAL_QUALIFICATION_UNREADY.json",qualification)
report=f"""Full V22 helper SOURCE-only candidate: {TARGET}
Parent dc01 SHA {PARENT_SHA}; candidate SHA {hashlib.sha256(candidate).hexdigest()}, {len(candidate)} bytes.
Five finite SOURCE hunks, only two conceptual last-use changes. Full inverse restores every parent byte and complete AST. 79 top-level definitions / 92 including methods and nested functions remain, with only _owners and verify_graph modified. Other 77 top-level functions, all globals/nonfunction nodes and all underlying expansion/namespace/phase/trace/consumer functions remain exact.
Original verify_graph full return SOURCE and ordered 27 fields are exact. All original ordered If/Assert/Raise/Call/Return nodes are exact after explicitly projecting out the disclosed private additions; a raw same-call-count claim is intentionally not made because the private flag guard/list clear are new calls.
Owner consumption only applies to verify_graph's fresh _expand_owner_table builtin list on consumerNone. Every original per-owner predicate, type normalization, new-input list handling and append runs before the old row slot is ended. All default and consumer callers retain original non-consuming semantics; no mutable result map is shared or pruned.
Namespace files/symlinks/directories are private cloned descriptors. Delete them only on consumerNone after the full _phase (both full namespace scans, full canonical EOF/aliases) and original second _absence_phase pass. Remaining trace coverage uses only canonical_root and return keeps whole namespace count. Consumer lineage and root-sequence return retain all fields.
Requirement tuples, complete trace, public fields and whole graph are not pruned. Third tuple consumption deferred. Canonical023abc, installed dc01, qualification29ac, original caps/fullscope/math/physics stay unchanged.
UNREADY: new helper Q and all six future business pins None. Old qualification29ac does not qualify this helper. No helper/API/guard/business/numeric execution, ART payload, history scan, allocator tuning, profiling, peak-line attribution or RSS/pass prediction. Root must perform fresh full original protocol plus complete current graph qualification after independent SOURCE review.
Lifetime matrix already sealed at {MATRIX_MANIFEST} SHA {MATRIX_MANIFEST_SHA}.
"""
(OUT/"REPORT.txt").write_text(report)
_,after=read_source(PARENT)
_,matrix_after=read_source(MATRIX_MANIFEST)
assert after==parent_pin and matrix_after==matrix_pin
write_json("SOURCE_PARENT_AND_MATRIX_FULL_EOF_BEFORE_AFTER.json",{"parent_before":parent_pin,"parent_after":after,
           "matrix_before":matrix_pin,"matrix_after":matrix_after,"equal":True})
print(json.dumps({"candidate":inverse["candidate"],"inverse":str(OUT/"COMPLETE_SOURCE_INVERSE.json"),
                  "defs":79,"all_function_or_method_defs":92,"edits":5,"public_fields":27,
                  "source_inverse_and_original_projection":True,"UNREADY":True,"new_helper_Q":None,"business":False}))


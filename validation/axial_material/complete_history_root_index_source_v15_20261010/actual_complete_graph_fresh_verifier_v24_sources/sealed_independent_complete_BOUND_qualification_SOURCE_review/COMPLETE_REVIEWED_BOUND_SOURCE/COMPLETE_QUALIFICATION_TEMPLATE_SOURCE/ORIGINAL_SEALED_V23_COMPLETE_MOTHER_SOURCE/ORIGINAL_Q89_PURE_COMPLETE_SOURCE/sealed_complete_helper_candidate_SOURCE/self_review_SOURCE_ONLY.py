#!/usr/bin/env python3
"""Independent read-back of SOURCE and proof in this TMP; no project import."""
from pathlib import Path
import ast,hashlib,json,stat
P=Path(__file__).resolve().parent
TARGET=P/"combined_runtime_complete_input_graph_private_owner_namespace_last_use_v22.UNREADY.py"
PARENT=P/"parent_dc01.complete.frozen_SOURCE.py"
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def load(p):
 b=p.lstat();assert stat.S_ISREG(b.st_mode) and not p.is_symlink();r=p.read_bytes();a=p.lstat()
 assert identity(a)==identity(b) and len(r)==a.st_size
 return r,{"path":str(p),"sha256":hashlib.sha256(r).hexdigest(),"bytes":len(r),"identity":identity(a)}
def dump(n):return ast.dump(n,include_attributes=False)
def segment(text,n):return "".join(text.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
checks=[]
def check(name,condition):assert condition,name;checks.append({"name":name,"SOURCE_result":True})
candidate,candidate_pin=load(TARGET);parent,parent_pin=load(PARENT)
proof_raw,proof_pin=load(P/"COMPLETE_SOURCE_INVERSE.json");proof=json.loads(proof_raw)
check("full_parent_bytes_SHA_dc01",parent_pin["sha256"]=="dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7")
check("fixed_candidate_SHA_cf0c",candidate_pin["sha256"]=="cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c")
check("proof_candidate_fullbytes_SHA",candidate_pin["sha256"]==proof["candidate"]["sha256"] and candidate_pin["bytes"]==proof["candidate"]["bytes"])
text,oldtext=candidate.decode("utf-8"),parent.decode("utf-8")
restored=text
for edit in reversed(proof["edits"]):
 check("one_finite_inverse_anchor_"+edit["id"],restored.count(edit["new"])==1)
 restored=restored.replace(edit["new"],edit["old"],1)
check("five_finite_SOURCE_hunks_only",len(proof["edits"])==5)
check("all_restored_bytes_to_dc01",restored.encode()==parent)
a,b,r=ast.parse(oldtext),ast.parse(text),ast.parse(restored)
check("full_inverse_AST_to_dc01",dump(a)==dump(r))
af={n.name:n for n in a.body if isinstance(n,ast.FunctionDef)}
bf={n.name:n for n in b.body if isinstance(n,ast.FunctionDef)}
check("all79_original_top_definitions_names_order",len(af)==len(bf)==79 and list(af)==list(bf))
check("all92_original_including_methods_nested",sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(a))==sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(b))==92)
changed=[n for n in af if segment(oldtext,af[n])!=segment(text,bf[n])]
check("only_two_original_functions_modified",changed==["_owners","verify_graph"])
for name in af:
 if name not in changed:
  check("full_original_function_bytes_AST_"+name,segment(oldtext,af[name])==segment(text,bf[name]) and dump(af[name])==dump(bf[name]))
check("all_original_top_globals_classes_imports_AST_equal",[dump(n) for n in a.body if not isinstance(n,ast.FunctionDef)]==[dump(n) for n in b.body if not isinstance(n,ast.FunctionDef)])
check("verify_graph_original_signature_exact",dump(af["verify_graph"].args)==dump(bf["verify_graph"].args))
owner=bf["_owners"]
check("owner_original_posargs_and_only_new_kwonlyFalse",[dump(n) for n in owner.args.args]==[dump(n) for n in af["_owners"].args.args])
check("owner_privateflag_exactbool_guard_defaultFalse",len(owner.args.kwonlyargs)==1 and owner.args.kwonlyargs[0].arg=="_consume" and owner.args.kw_defaults[0].value is False)
loop=next(n for n in owner.body if isinstance(n,ast.For))
check("original_result_append_immediately_before_privateconsume",isinstance(loop.body[-3],ast.Expr) and isinstance(loop.body[-3].value,ast.Call) and dump(loop.body[-3].value.func)==dump(ast.parse("result.append",mode="eval").body))
check("private_owners_row_release_after_original_append",dump(loop.body[-2].test)==dump(ast.parse("_consume",mode="eval").body) and isinstance(loop.body[-2].body[0],ast.Assign) and loop.body[-2].body[0].value.value is None)
check("private_owner_result_length_order_not_pruned",isinstance(loop.body[-1],ast.AugAssign) and loop.body[-1].target.id=="consumed_index" and loop.body[-1].value.value==1)
calls=[n for n in ast.walk(b) if isinstance(n,ast.Call) and getattr(n.func,"id",None)=="_owners"]
flagcalls=[n for n in calls if any(k.arg=="_consume" for k in n.keywords)]
check("one_new_owner_privatecaller_only",len(flagcalls)==1)
check("new_privatecaller_consumerNone_exact",dump(flagcalls[0].keywords[0].value)==dump(ast.parse("consumer is None",mode="eval").body))
check("original_full_owner_expansion_call_exact",dump(flagcalls[0].args[0])==dump(ast.parse('_expand_owner_table(graph["owners"], graph["requirements"])',mode="eval").body))
v=bf["verify_graph"]
release=[n for n in v.body if isinstance(n,ast.If) and len(n.body)==1 and isinstance(n.body[0],ast.For) and n.body[0].body and isinstance(n.body[0].body[0],ast.Delete)]
check("one_private_namespace_release_consumerNone",len(release)==1 and dump(release[0].test)==dump(ast.parse("consumer is None",mode="eval").body))
idx=v.body.index(release[0])
check("release_after_original_second_absencecheck",isinstance(v.body[idx-1],ast.Expr) and isinstance(v.body[idx-1].value,ast.Call) and getattr(v.body[idx-1].value.func,"id",None)=="_absence_phase")
check("release_before_original_rebuild_requirements",isinstance(v.body[idx+1],ast.Assign) and getattr(v.body[idx+1].targets[0],"id",None)=="rebuilt_requirements")
check("delete_exactly_three_dead_private_fields",[t.slice.value for t in release[0].body[0].body[0].targets]==["files","symlinks","directories"])
check("trace_after_phase_namespace_only_canonicalroot",segment(oldtext,af["_trace_coverage"])==segment(text,bf["_trace_coverage"]) and [n.id for n in ast.walk(bf["_trace_coverage"]) if isinstance(n,ast.Name) and n.id=="namespaces"]==["namespaces"])
tail=ast.Module(body=v.body[idx+1:],type_ignores=[])
namespace_load_context=[]
for n in ast.walk(tail):
 if isinstance(n,(ast.Call,ast.ListComp)):
  if any(isinstance(x,ast.Name) and x.id=="namespaces" for x in ast.walk(n)):
   namespace_load_context.append(dump(n))
check("no_remaining_deletedfield_subscript_in_verifier_tail",not any(isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=="namespace" and isinstance(n.slice,ast.Constant) and n.slice.value in ("files","symlinks","directories") for n in ast.walk(tail)))
oldrets=[n for n in ast.walk(af["verify_graph"]) if isinstance(n,ast.Return)]
newrets=[n for n in ast.walk(v) if isinstance(n,ast.Return)]
check("one_full_return_source_unchanged",len(oldrets)==len(newrets)==1 and segment(oldtext,oldrets[0])==segment(text,newrets[0]) and dump(oldrets[0])==dump(newrets[0]))
check("all27_original_return_fields_order",len(newrets[0].value.keys)==27 and [n.value for n in newrets[0].value.keys]==proof["verify_return_field_order"])
q=json.loads((P/"FUTURE_REAL_QUALIFICATION_UNREADY.json").read_text())
check("newqualification_none_sixbusiness_none",q["new_helper_Q"] is None and q["six_future_business_pins"]==[None]*6)
check("no_oldQreuse_no_qualification_claim",q["old_dc01_and_29ac_immutable_not_applied_to_candidate"] is True and q["scientific_or_wholeINPUT_native_AAA_ABA_credit"] is False)
check("no_tuple_consumption_changed",segment(oldtext,af["_compact_requirement_dicts"])==segment(text,bf["_compact_requirement_dicts"]) and proof["tuple_requirements_consumption_included"] is False)
check("original_expand_namespace_phase_trace_consumer_allbytes_unchanged",all(segment(oldtext,af[n])==segment(text,bf[n]) for n in ["_expand_owner_table","_namespace_descriptor","_phase","_trace_coverage","_consumer_lineage","_trace_records","_path","_label","_json_clone"]))
for path,first in [(TARGET,candidate_pin),(PARENT,parent_pin),(P/"COMPLETE_SOURCE_INVERSE.json",proof_pin)]:
 _,last=load(path);check("SOURCE_fullEOF_SHA7ID_before_after_"+path.name,last==first)
report={"schema":"AXMAT_V22_FULL_PRIVATE_OWNER_NAMESPACE_HELPER_SOURCE_SELF_REVIEW_V1",
        "status":"SOURCE_STATIC_READBACK_ONLY_PASS_NOT_ACTUAL_HELPER_PROTOCOL",
        "checks":checks,"check_count":len(checks),"blockers":[],
        "candidate":candidate_pin,"parent":parent_pin,"proof":proof_pin,
        "remaining_namespace_load_context_complete_AST":namespace_load_context,
        "new_helper_Q":None,"six_future_business_pins":[None]*6,
        "runtime_or_helper_API_or_guard_executed":False,"ART_payload_or_numeric_read":False,
        "observed_peak_source_line":None,"RSS_or_futurepass_prediction":None}
(P/"SOURCE_SELF_REVIEW.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"review":str(P/"SOURCE_SELF_REVIEW.json"),"check_count":len(checks),
                  "blockers":[],"fullinverse":True,"UNREADY":True,"new_helper_Q":None,"business":False}))

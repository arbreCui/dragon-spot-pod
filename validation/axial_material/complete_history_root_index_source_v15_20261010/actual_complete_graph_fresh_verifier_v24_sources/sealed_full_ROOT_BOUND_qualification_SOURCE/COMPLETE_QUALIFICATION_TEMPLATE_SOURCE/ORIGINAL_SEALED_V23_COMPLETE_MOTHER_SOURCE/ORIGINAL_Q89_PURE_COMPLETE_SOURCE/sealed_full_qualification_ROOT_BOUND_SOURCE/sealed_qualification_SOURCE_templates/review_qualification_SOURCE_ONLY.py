#!/usr/bin/env python3
"""Read-back SOURCE/finite actual Source-install META only; no binding execution."""
from pathlib import Path
import ast,hashlib,json,stat
P=Path(__file__).resolve().parent
W=Path("/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v22_receipts/Root_actual_helper_SOURCE_install_tool_return.json")
R=Path("/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v22_sources/Root_helper_SOURCE_install_record.json")
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 b=p.lstat();assert stat.S_ISREG(b.st_mode) and not p.is_symlink();r=p.read_bytes();a=p.lstat();assert ident(a)==ident(b) and len(r)==a.st_size
 return r,{"path":str(p),"sha256":hashlib.sha256(r).hexdigest(),"identity":ident(a),"bytes":len(r)}
def dump(n):return ast.dump(n,include_attributes=False)
def segment(s,n):return "".join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
checks=[]
def check(name,c):assert c,name;checks.append({"name":name,"Source_result":True})
proof_raw,proof_pin=read(P/"ALL_FOUR_FULL_SOURCE_INVERSES.json");proof=json.loads(proof_raw)
for name,t in proof["templates"].items():
 raw,pin=read(P/t["file"]);old,op=read(P/(name+".original_actual_SOURCE.py"));text=raw.decode();restored=text
 check(name+"_fixed_complete_template_SHA_bytes",pin["sha256"]==t["sha256"] and pin["bytes"]==t["bytes"])
 for e in reversed(t["edits"]):
  check(name+"_unique_inverse_"+e["id"],restored.count(e["after"])==1)
  restored=restored.replace(e["after"],e["before"],1)
 check(name+"_whole_original_allbytes_AST_inverse",restored.encode()==old and dump(ast.parse(restored))==dump(ast.parse(old.decode())))
 oldast,newast=ast.parse(old),ast.parse(raw)
 oldfuncs={n.name:n for n in oldast.body if isinstance(n,ast.FunctionDef)}
 newfuncs={n.name:n for n in newast.body if isinstance(n,ast.FunctionDef)}
 if name=="pure_driver":
  check("original22pure_functions_plus_one_control_only",len(oldfuncs)==22 and len(newfuncs)==23 and set(newfuncs)-set(oldfuncs)=={"private_owner_consume_controls"})
  for fn in oldfuncs:
   if fn!="run":check("pure_original_full_function_"+fn,segment(old.decode(),oldfuncs[fn])==segment(text,newfuncs[fn]))
 elif name=="fresh_driver":
  check("all15fresh_original_functions_fullbytes_exact",len(oldfuncs)==len(newfuncs)==15 and all(segment(old.decode(),oldfuncs[n])==segment(text,newfuncs[n]) for n in oldfuncs))
 elif name=="fresh_host":
  check("original8fresh_host_definitions_exact_names",len(oldfuncs)==len(newfuncs)==8 and list(oldfuncs)==list(newfuncs))
 # After exact inverse, every original call/if/assert/raise/return has its full
 # original AST/order. New owner control/host predicates are not hidden.
 _,later=read(P/t["file"]);check(name+"_fullEOF_SHA7ID_before_after",pin==later)

pd_raw,_=read(P/"pure_helper_controls.v22.UNREADY.py");pd=ast.parse(pd_raw)
fn=next(n for n in pd.body if isinstance(n,ast.FunctionDef) and n.name=="private_owner_consume_controls")
calls=[n for n in ast.walk(fn) if isinstance(n,ast.Call)]
attributes=[n for n in calls if isinstance(n.func,ast.Attribute)]
check("new_owner_function_no_file_subprocess_guard_verifygraph_API_calls",not any(n.func.attr in ("open","read_bytes","read_text","write_bytes","write_text","verify_graph","create_wire_graph","execute","guard_admission") for n in attributes))
check("new_owner_fixture_reuses_full_original_expand",any(isinstance(n.func,ast.Attribute) and n.func.attr=="_expand_owner_table" for n in calls))
check("successful_owned_list_asserts_empty",any(isinstance(n,ast.Compare) and isinstance(n.left,ast.Name) and n.left.id=="owned" and any(isinstance(c,ast.List) and len(c.elts)==0 for c in n.comparators) for n in ast.walk(fn)))
check("partial_invalid_second_owner_first_slot_is_None",any(isinstance(n,ast.Compare) and isinstance(n.left,ast.Subscript) and isinstance(n.left.value,ast.Name) and n.left.value.id=="owned_partial" and isinstance(n.left.slice,ast.Constant) and n.left.slice.value==0 and isinstance(n.ops[0],ast.Is) and isinstance(n.comparators[0],ast.Constant) and n.comparators[0].value is None for n in ast.walk(fn)))
check("partial_invalid_second_owner_original_identity_preserved",any(isinstance(n,ast.Compare) and isinstance(n.left,ast.Subscript) and isinstance(n.left.value,ast.Name) and n.left.value.id=="owned_partial" and isinstance(n.left.slice,ast.Constant) and n.left.slice.value==1 and isinstance(n.ops[0],ast.Is) and isinstance(n.comparators[0],ast.Name) and n.comparators[0].id=="invalid" for n in ast.walk(fn)))
check("negative_source_uses_original_exact_InputGraphError_wrapper",sum(isinstance(n.func,ast.Name) and n.func.id=="rejection" for n in calls)==3)
run=next(n for n in pd.body if isinstance(n,ast.FunctionDef) and n.name=="run")
newcalls=[n for n in ast.walk(run) if isinstance(n,ast.Call) and getattr(n.func,"id",None)=="private_owner_consume_controls"]
check("new_owner_report_called_once_original_run",len(newcalls)==1)
wr,wp=read(W);rr,rp=read(R);w,r=json.loads(wr),json.loads(rr)
check("real_installed_Source_witness_fixed_SHA",wp["sha256"]=="914d04b742611749140c5612715887fb4c32f27536867125db4ef15ceb2aca7e")
check("real_installed_Source_record_fixed_SHA",rp["sha256"]=="d1d21ab41c443e09e2305bf75377c69399ebfebff97429c6ea270660054e5d32")
check("real_Source_witness_schema_exact",w["schema"]=="ROOT_V22_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1")
check("real_Source_witness_closed_observed_Sourceonly_typed0",w["closed"] is True and w["actual_tool_terminal_return_observed"] is True and w["source_only"] is True and type(w["terminal_tool_return"]["exit_code"]) is int and w["terminal_tool_return"]["exit_code"]==0 and "session_id" not in w["terminal_tool_return"])
payload=json.loads(w["terminal_tool_return"]["output"])
check("full_actual_stdout_pin_shape_exact_seven_Python_integers",payload["installed_helper"]==w["installed_helper"] and payload["source_install_record"]==w["source_install_record"] and all(type(v) is int for q in ("installed_helper","source_install_record") for v in w[q]["identity"]))
check("witness_record_Source_schema_installedhelper_exact",r["schema"]=="ROOT_V22_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1" and r["installed_helper"]==w["installed_helper"] and r["source_only"] is True)
check("Source_install_is_not_Q_or_business",w["actual_new_helper_qualification_sha256"] is None and r["actual_new_helper_qualification_sha256"] is None and all(w[k] is False for k in ("actual_pure_helper_protocol_qualified","actual_full_current_graph_verifier_qualified","complete_build_qualified","whole_INPUT_admitted","native_RSS_qualified","AAA_accuracy_qualified","ABA_admitted")))
for path,first in [(W,wp),(R,rp)]:
 _,after=read(path);check("actual_Meta_fullEOF_SHA7ID_"+path.name,first==after)
binder_raw,binder_pin=read(P/"bind_qualification_sources_SOURCE_ONLY.py");ba=ast.parse(binder_raw)
check("binder_stdlib_only_imports",all((n.module or "").split(".")[0] in ("pathlib",) for n in ba.body if isinstance(n,ast.ImportFrom)) and all(alias.name in ("argparse","ast","hashlib","json","math","os","stat") for n in ba.body if isinstance(n,ast.Import) for alias in n.names))
check("binder_no_business_dynamic_import",not any(isinstance(n,ast.Call) and (getattr(n.func,"id","") in ("exec","eval","__import__","compile") or getattr(n.func,"attr","") in ("spec_from_file_location","exec_module","verify_graph","guard_admission","execute")) for n in ast.walk(ba)))
check("binder_never_Project_D_E_ART_write",all(s not in binder_raw.decode() for s in ("SOURCES.mkdir","RECEIPTS.mkdir","CANONICAL_HELPER.write","WITNESS_PATH.write","RECORD_PATH.write")))
check("binder_only_fresh_private_TMP_outputs","destination.parent==Path(\"/private/tmp\")" in binder_raw.decode())
check("binder_retains_all_flat_source_members_not_selected","for name,(raw,q) in members.items():write" in binder_raw.decode())
check("binder_Source_record_full_copy_inventory_and_no_fixed_old18_count","len(files)==source_record[\"source_file_count\"]>0" in binder_raw.decode() and "complete_source_file_inventory_from_record" in binder_raw.decode())
check("binder_precise_actual_terminal_stdout_pin_match","typed_pin(output[\"installed_helper\"])==helper" in binder_raw.decode() and "typed_pin(output[\"source_install_record\"])==record" in binder_raw.decode())
check("binder_new_Q_six_future_None","UNKNOWN_Q=None" in binder_raw.decode() and "SIX_FUTURE_BUSINESS_PINS=[None]*6" in binder_raw.decode())
check("prooforiginal66checks_TRUE",proof["check_count"]==66 and all(c["Source_result"] is True for c in proof["SOURCE_checks"]))
report={"schema":"AXMAT_V22_FULL_TWO_QUALIFICATION_SOURCE_SELF_REVIEW_V1","status":"SOURCE_AND_SMALL_REAL_INSTALL_META_ONLY_PASS_NO_HOST_OR_BINDING_EXECUTED","checks":checks,"check_count":len(checks),"original_author_Source_checks":66,"blockers":[],"binder":binder_pin,"actual_Source_install_witness":wp,"actual_Source_install_record":rp,"actual_install_terminal_chunk":w["terminal_tool_return"]["chunk_id"],"full_original_actual_install_stdout_pin_integer_binding":True,"new_Q":None,"six_future_business_pins":[None]*6,"binding_branch_executed":False,"controls_helper_API_guard_business_numeric_executed":False,"ART_graph_numeric_payload_read":False}
(P/"SOURCE_SELF_REVIEW.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"review":str(P/"SOURCE_SELF_REVIEW.json"),"checks":len(checks),"original_author_checks":66,"blockers":[],"binding_branch_executed":False,"business":False,"new_Q":None}))


#!/usr/bin/env python3
"""Read/derive SOURCE and small historical tool receipts only. No helper import."""
from pathlib import Path
import ast,hashlib,json,stat
P=Path(__file__).resolve().parent
B=Path("/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010")
ART=Path("/Users/wen/spot/validation/artifacts")
HELPER=Path("/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py")
HELPER_SHA="cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c"
HELPER_BYTES=148965
PURE_D=B/"actual_complete_graph_helper_controls_v22_sources"
PURE_E=B/"actual_complete_graph_helper_controls_v22_receipts"
PURE_H=ART/"axial-material-complete-graph-private-owner-namespace-helper-controls-host-v22-20261010"
PURE_O=ART/"axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010"
FRESH_D=B/"actual_complete_graph_fresh_verifier_v22_sources"
FRESH_E=B/"actual_complete_graph_fresh_verifier_v22_receipts"
FRESH_H=ART/"axial-material-complete-graph-fresh-verifier-host-v22-20261010"
FRESH_O=ART/"axial-material-complete-graph-fresh-verifier-v22-20261010"
parents={
 "pure_driver":(B/"actual_complete_graph_helper_controls_v21_sources/pure_helper_controls.py","fee784d6e11ba2fe5e272fd4319e4ff29ac800e592207f1114be0263fb434673"),
 "pure_host":(B/"actual_complete_graph_helper_controls_v21_sources/pure_helper_controls_host.py","86dce7b5742f044a08a5f977f48735f363ca95f924a63f2638f9e8830a5649e3"),
 "fresh_driver":(B/"actual_complete_graph_fresh_verifier_v21b_sources/fresh_verifier_controls.py","895c889569507f2b5e28ee1da6efc6c91bbdd30cd05338dd6e039d9591e72f84"),
 "fresh_host":(B/"actual_complete_graph_fresh_verifier_v21b_sources/fresh_verifier_host.py","bb232eb13187013fde74e909aac8d316648a83a63115758ad2f0db200ab2322f"),
}
receipts={
 "original_pure_complete_Root_tool_receipt":(B/"actual_complete_graph_helper_controls_v21_receipts/Root_actual_pure_protocol_tool_terminal_return.json","875bbea8cdbf5bf8815eed73e456e0f18054ba5397bf0194c3921d60d60eb57c"),
 "original_fresh_complete_Root_tool_receipt":(B/"actual_complete_graph_fresh_verifier_v21b_receipts/Root_actual_v21b_fresh_verifier_tool_terminal_return.json","34e031c0985de52168a33a4452837ce4de57c86772bb43a31915a8b88bb9a914"),
}
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p,sha=None):
 before=p.lstat();assert stat.S_ISREG(before.st_mode) and not p.is_symlink();raw=p.read_bytes();after=p.lstat()
 assert identity(before)==identity(after) and len(raw)==before.st_size
 pin={"path":str(p),"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"identity":identity(after)}
 assert sha is None or pin["sha256"]==sha
 return raw,pin
def dump(n):return ast.dump(n,include_attributes=False)
def segment(s,n):return "".join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
def json_write(name,v): (P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def derive(name,old,edits):
 new=old
 for e in edits:
  assert new.count(e["before"])==1,e["id"]
  new=new.replace(e["before"],e["after"],1)
 restored=new
 for e in reversed(edits):
  assert restored.count(e["after"])==1,e["id"]
  restored=restored.replace(e["after"],e["before"],1)
 assert restored==old and dump(ast.parse(restored))==dump(ast.parse(old))
 ast.parse(new)
 file_name={"pure_driver":"pure_helper_controls.v22.UNREADY.py","pure_host":"pure_helper_controls_host.v22.UNREADY.py","fresh_driver":"fresh_verifier_controls.v22.UNREADY.py","fresh_host":"fresh_verifier_host.v22.UNREADY.py"}[name]
 assert not (P/file_name).exists()
 (P/file_name).write_text(new)
 return new,{"name":name,"file":file_name,"sha256":hashlib.sha256(new.encode()).hexdigest(),"bytes":len(new.encode()),"edits":edits,"edit_count":len(edits),"allbytes_inverse_to_actual_parent":True,"full_AST_inverse_to_actual_parent":True}
def edit(i,b,a):return {"id":i,"before":b,"after":a}
raws={};pins={};old={};frozen_receipts={}
for name,(path,sha) in parents.items():
 raw,pin=read(path,sha);raws[name]=raw;pins[name]=pin;old[name]=raw.decode();(P/(name+".original_actual_SOURCE.py")).write_bytes(raw)
for name,(path,sha) in receipts.items():
 raw,pin=read(path,sha);value=json.loads(raw);tr=value["terminal_tool_return"]
 assert value["closed"] is True and type(tr["exit_code"]) is int and tr["exit_code"]==0 and "session_id" not in tr
 (P/(name+".exact.json")).write_bytes(raw)
 frozen_receipts[name]={"pin":pin,"complete_receipt":value}
controls=(P/"private_owner_consume_controls.SOURCE_insert.txt").read_text()
assert len([n for n in ast.parse(controls).body if isinstance(n,ast.FunctionDef)])==1
pure_driver_edits=[
 edit("helperpath_unknown_future_Source_install", 'HELPER_PATH = "/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py"',"HELPER_PATH = None"),
 edit("helperSHA_unknown_future_Source_install",'HELPER_SHA256 = "dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7"',"HELPER_SHA256 = None"),
 edit("helperBYTES_unknown_future_Source_install","HELPER_SOURCE_BYTES = 147870","HELPER_SOURCE_BYTES = None"),
 edit("new_private_owner_full_metadata_control_function_only","def run(output_dir):\n",controls+"def run(output_dir):\n"),
 edit("new_private_owner_report_call_after_all_original_small_codecs",'        report["small_codecs"] = codec_controls(g, small_graph, artifacts)\n','        report["small_codecs"] = codec_controls(g, small_graph, artifacts)\n        report["private_owner_consume_controls"] = private_owner_consume_controls(g, small_graph)\n'),
]
new_pure_driver,pure_driver_proof=derive("pure_driver",old["pure_driver"],pure_driver_edits)
host_control=(
 "        owners_control=control_report['private_owner_consume_controls']\n"
 "        if owners_control['schema']!='AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1' or owners_control['status']!='ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY':raise ValueError('actual new complete private owner controls required')\n"
 "        owner_positive=owners_control['positive_controls'];owner_negative=owners_control['private_guard_rejections'];owner_subtypes=owners_control['accepted_str_subclass_equivalence_controls'];owner_partial=owners_control['partial_invalid_second_owner_rejections']\n"
 "        if len(owner_positive)!=4 or {case['case'] for case in owner_positive}!={'default_list','default_tuple','explicit_False_list','owned_builtin_list_True'} or any(case['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default'] is not True or case['expected_complete_descriptor_signature']!=case['actual_complete_descriptor_signature'] for case in owner_positive):raise ValueError('all new original default and private owner descriptor controls required')\n"
 "        if any(case['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is not True for case in owner_positive if case['case']!='owned_builtin_list_True') or any(case['owned_list_completely_cleared_after_success'] is not True for case in owner_positive if case['case']=='owned_builtin_list_True'):raise ValueError('default caller integrity and complete successful private list clearing required')\n"
 "        if len(owner_negative)!=3 or {case['case'] for case in owner_negative}!={'nonbool_consume','tuple_True','list_subclass_True'} or any(case['class']!='InputGraphError' or case['message']!='private owner consume needs a bool and an exclusively owned builtin list' or case['caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is not True for case in owner_negative):raise ValueError('all private owner flag/list guards and rejection caller integrity required')\n"
 "        if len(owner_subtypes)!=2 or {case['case'] for case in owner_subtypes}!={'plain_accepted_str','accepted_str_with_str_override'} or any(case['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged'] is not True or case['owned_list_completely_cleared_after_success'] is not True or case['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default'] is not True or case['expected_complete_descriptor_signature']!=case['actual_complete_descriptor_signature'] for case in owner_subtypes):raise ValueError('complete accepted owner str subtypes attributes and floatbits required')\n"
 "        if len(owner_partial)!=2 or {case['case'] for case in owner_partial}!={'invalid_second_owner_default','invalid_second_owner_owned_True'} or any(case['class']!='InputGraphError' or case['message']!='missing file owner' for case in owner_partial):raise ValueError('original invalid second owner rejection class and message required')\n"
 "        if any(owners_control[key] is not True for key in ('first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created')) or owners_control['new_helper_qualification_created'] is not False or owners_control['business_or_science_qualification_created'] is not False:raise ValueError('private last-use sequencing and metadata-only scope required')\n")
pure_host_edits=[
 edit("pure_fresh_HOST", "HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-verifier-helper-controls-host-v21-20261010')","HOST=Path("+repr(str(PURE_H))+")"),
 edit("pure_fresh_OUT", "OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-verifier-helper-controls-v21-20261010')","OUT=Path("+repr(str(PURE_O))+")"),
 edit("pure_fresh_SOURCE_ARCHIVE", "SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v21_sources')","SOURCE_ARCHIVE=Path("+repr(str(PURE_D))+")"),
 edit("pure_fresh_TARGET", "TARGET=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v21_sources/pure_helper_controls.py')","TARGET=Path("+repr(str(PURE_D/"pure_helper_controls.py"))+")"),
 edit("pure_actual_new_driverSHA_future", "TARGET_SHA='fee784d6e11ba2fe5e272fd4319e4ff29ac800e592207f1114be0263fb434673'","TARGET_SHA=None"),
 edit("pure_actual_new_helperPATH_SHA_future", "support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py'),'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')","support.pin(Path(None),None)"),
 edit("pure_new_host_receipt_schema", "schema='AXMAT_V21_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1'","schema='AXMAT_V22_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1'"),
 edit("pure_full_new_owner_controls_host_predicates", "        if len(runner.records)!=1 or runner.records[0]['status']!='PASS'",host_control+"        if len(runner.records)!=1 or runner.records[0]['status']!='PASS'"),
]
new_pure_host,pure_host_proof=derive("pure_host",old["pure_host"],pure_host_edits)
fresh_driver_edits=[
 edit("fresh_UNREADY_status","SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'","SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'"),
 edit("fresh_actual_helperPATH_future","NEW_HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py'","NEW_HELPER_PATH = None"),
 edit("fresh_actual_helperSHA_future","NEW_HELPER_SHA256 = 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'","NEW_HELPER_SHA256 = None"),
 edit("fresh_actual_helperBYTES_future","NEW_HELPER_SOURCE_BYTES = 147870","NEW_HELPER_SOURCE_BYTES = None"),
 edit("fresh_actual_helper7ID_future","NEW_HELPER_IDENTITY = [16777229, 49380106, 33188, 1, 147870, 1791589379138539325, 1791589879966481802]","NEW_HELPER_IDENTITY = None"),
 edit("fresh_fresh_OUT","OUTPUT_PATH = '/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21b-20261010'","OUTPUT_PATH = "+repr(str(FRESH_O))),
]
new_fresh_driver,fresh_driver_proof=derive("fresh_driver",old["fresh_driver"],fresh_driver_edits)
fa=ast.parse(old["fresh_host"]);assign={n.targets[0].id:ast.get_source_segment(old["fresh_host"],n) for n in fa.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
fresh_host_edits=[
 edit("fresh_fresh_HOST",assign["HOST"],"HOST=Path("+repr(str(FRESH_H))+")"),
 edit("fresh_fresh_OUT",assign["OUT"],"OUT=Path("+repr(str(FRESH_O))+")"),
 edit("fresh_fresh_SOURCE_ARCHIVE",assign["SOURCE_ARCHIVE"],"SOURCE_ARCHIVE=BASE/"+repr(FRESH_D.name)),
 edit("fresh_fresh_RECEIPTS",assign["RECEIPTS"],"RECEIPTS=BASE/"+repr(FRESH_E.name)),
 edit("fresh_actual_driverSHA_future",assign["TARGET_SHA"],"TARGET_SHA=None"),
 edit("fresh_UNREADY_status",assign["SOURCE_STATUS"],"SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'"),
 edit("fresh_actual_helperfullpin_future",assign["BOUND_HELPER_PIN"],"BOUND_HELPER_PIN=None"),
 edit("fresh_actual_Sourcewitnessfullpin_future",assign["INSTALL_WITNESS_PIN"],"INSTALL_WITNESS_PIN=None"),
 edit("fresh_actual_Sourceinstallrecordfullpin_future",assign["SOURCE_INSTALL_RECORD_PIN"],"SOURCE_INSTALL_RECORD_PIN=None"),
 edit("fresh_new_Source_namespace_schema","schema='AXMAT_V21_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_NAMESPACE_V1'","schema='AXMAT_V22_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_NAMESPACE_V1'"),
 edit("fresh_new_host_receipt_schema","schema='AXMAT_V21_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1'","schema='AXMAT_V22_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1'"),
]
new_fresh_host,fresh_host_proof=derive("fresh_host",old["fresh_host"],fresh_host_edits)

new={"pure_driver":new_pure_driver,"pure_host":new_pure_host,"fresh_driver":new_fresh_driver,"fresh_host":new_fresh_host}
proofs={"pure_driver":pure_driver_proof,"pure_host":pure_host_proof,"fresh_driver":fresh_driver_proof,"fresh_host":fresh_host_proof}
checks=[]
def check(name,c):assert c,name;checks.append({"name":name,"Source_result":True})
for name in new:
 before,after=ast.parse(old[name]),ast.parse(new[name])
 of={n.name:n for n in before.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 nf={n.name:n for n in after.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 expected=list(of)
 if name=="pure_driver":expected.insert(expected.index("run"),"private_owner_consume_controls")
 check(name+"_complete_original_definition_order_and_only_explicit_new",list(nf)==expected)
 allowed={"pure_driver":{"run","private_owner_consume_controls"},"pure_host":{"main"},"fresh_driver":set(),"fresh_host":{"_source_namespace","main"}}[name]
 for fn in of:
  if fn not in allowed:check(name+"_whole_function_class_bytes_AST_"+fn,segment(old[name],of[fn])==segment(new[name],nf[fn]) and dump(of[fn])==dump(nf[fn]))
 check(name+"_original_module_allbytes_fullAST_inverse",proofs[name]["allbytes_inverse_to_actual_parent"] and proofs[name]["full_AST_inverse_to_actual_parent"])
 check(name+"_all_unknown_qualification_business_globals_none",all(dump(n.value)==dump(ast.Constant(value=None)) for n in after.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ("UNKNOWN_Q","UNKNOWN_BUSINESS_PINS","ACTUAL_SUCCESS_PINS")))
 def caps(t):
  result={}
  for n in t.body:
   if isinstance(n,ast.Assign):
    ids=[x.id for x in ast.walk(n.targets[0]) if isinstance(x,ast.Name)]
    if any(x in ("MAX_JSON_BYTES","MAX_OUTPUT_BYTES","RSS_BYTES","WALL_SECONDS","CHILD_LIMIT","RETRIES","WHOLE_CAP","STAGE_CAP","RSS_CAP","ARCHIVE_CAP","HISTORY_BYTES","MIN_FREE_BYTES","STAGE_SECONDS","WHOLE_HOST_SECONDS","RSS_MIB","THREADS","CHILDREN","JOINT_HOST_SOURCE_OUT_ARCHIVE_BYTES","GRAPH_PIN","TRACE_PIN","TRACE_ORIGINAL_ORDER_COMPACT_PIN","GRAPH_PATH","GRAPH_SHA","GRAPH_IDENTITY","OLD_HELPER_PATH","OLD_HELPER_SHA256","OLD_HELPER_SOURCE_BYTES","SEAL_SHA","TERM_SHA","SUPPORT_SHA") for x in ids):
     result[tuple(ids)]=dump(n.value)
  return result
 check(name+"_all_original_caps_original_full_input_pins_oracle_support_exact",caps(before)==caps(after))
check("fresh_original27_return_source_ALL_driver_functions_exact",all(segment(old["fresh_driver"],n)==segment(new_fresh_driver,next(m for m in ast.parse(new_fresh_driver).body if isinstance(m,ast.FunctionDef) and m.name==n.name)) for n in ast.parse(old["fresh_driver"]).body if isinstance(n,ast.FunctionDef)))
for name,(path,sha) in parents.items():
 _,after=read(path,sha);check(name+"_actual_parent_fullEOF_SHA7ID_unchanged",after==pins[name])
for name,(path,sha) in receipts.items():
 _,after=read(path,sha);check(name+"_original_tool_receipt_fullEOF_SHA7ID_unchanged",after==frozen_receipts[name]["pin"])
json_write("ALL_FOUR_FULL_SOURCE_INVERSES.json",{"schema":"AXMAT_V22_TWO_COMPLETE_QUALIFICATION_SOURCE_FINITE_INVERSES_V1","status":"UNREADY_SOURCE_ONLY_NO_QUALIFICATION","parents":pins,"templates":proofs,"new_helper_context":{"path":str(HELPER),"sha256":HELPER_SHA,"bytes":HELPER_BYTES,"identity":None},"new_Q":None,"six_future_business_pins":[None]*6,"original_complete_actual_tool_receipts":frozen_receipts,"new_control_additions_disclosed":"pure driver one new function + run one call; pure host main complete new predicates; original tests retained. Fresh driver all15 defs exact, host only two schema literals changed inside original8 defs, full inverse retains all original checks.","SOURCE_checks":checks,"check_count":len(checks),"controls_or_helper_API_or_guard_executed":False,"ART_graph_numeric_payload_read":False})
plan={"schema":"AXMAT_V22_FULL_PURE_AND_CURRENT_GRAPH_QUALIFICATION_SOURCE_ROUTE_V1","status":"UNREADY_ROOT_REAL_SOURCE_INSTALL_REQUIRED",
 "helper_context":{"path":str(HELPER),"sha256":HELPER_SHA,"bytes":HELPER_BYTES,"identity":None},
 "pure":{"D":str(PURE_D),"E":str(PURE_E),"H":str(PURE_H),"O":str(PURE_O),"driver":str(PURE_D/"pure_helper_controls.py"),"normal_host":str(PURE_D/"pure_helper_controls_host.py"),"whole_seconds":60,"stage_seconds":60,"RSS_MiB":512,"joint_archive_scope":["H","O","D"],"joint_archive_bytes":64*2**20,"original_all_fixtures_negative_fullgraph_fulltrace_kept":True,"new_owner_controls":{"positive":4,"private_guard_negative":3,"accepted_str_subtypes":2,"partial_original_validation_rejections":2}},
 "fresh":{"D":str(FRESH_D),"E":str(FRESH_E),"H":str(FRESH_H),"O":str(FRESH_O),"driver":str(FRESH_D/"fresh_verifier_controls.py"),"normal_host":str(FRESH_D/"fresh_verifier_host.py"),"whole_seconds":1800,"stage_seconds":600,"RSS_MiB":512,"joint_archive_scope":["H","O","D","E"],"joint_archive_bytes":64*2**20,"full_return_fields":27,"canonical_files":37111,"unfiltered_actual_readopens":37112,"full_gzip_results":3,"old_private_trace_positive_negative":[4,3],"full_fixed_graph_Source_literals_unchanged":True},
 "unchanged_resources":{"history_bytes":96*2**30,"free_bytes":8*2**30,"threads":1,"children":1,"retries":0,"genuine_guard_MRO_fullsupport_exact":True,"dynamic_history_five_ART_roots_and_family_union_exact":True},
 "future_install_witness":{"path":str(PURE_E/"Root_actual_helper_SOURCE_install_tool_return.json"),"sha256":None,"schema":"ROOT_V22_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1","source_install_record":str(PURE_D/"Root_helper_SOURCE_install_record.json"),"required":"Root actual typed int0 closed source-only installed_helper/source_install_record full pins; exact 7 Python integers from actual original tool output"},
 "new_Q":None,"six_future_business_pins":[None]*6,"no_old29ac_reuse":True,"helper_API_guard_business_numeric_executed":False,"Root_only_actual_executor":True}
json_write("ROOT_FULL_QUALIFICATION_ROUTE_UNREADY.json",plan)
(P/"REPORT.txt").write_text("UNREADY SOURCE-only V22 qualification entry package. Full original 60/60/512/64MiB pure protocol retained, plus disclosed private owner controls: 4 positives, 3 flag/list negatives, 2 accepted str subtypes with attrs/floatbits, 2 invalid-second-owner original/private rejection receipts. Successful owned list must be empty; malformed second row leaves first valid slot None and second unchanged. Pure normalhost additionally validates the entire new control report. Full fresh original15 functions byteexact; all27 ordered/nested constructor oracle/type/floatbit/37112 reads and three unfiltered gzip results kept. Both genuine guard/MRO/dynamic ART roots/resource classes unchanged. New namespace/schema/global bindings only, all SOURCE byte/AST inverse to actual original entrypoints. Templates have None unknown installed identities/witness/record, no new Q, no science/business success. Root must bind actual Source-only installation evidence, independently Source-review final bound host, install full Source inventory before D freeze, prelaunch all pins/namespace/64MiB/free/H/O absent check, then execute each normalhost once. Source install and prior29ac are not new qualification. No host/helper/API/guard execution, ART payload or history scan by author.\n")
print(json.dumps({"path":str(P),"templates":{k:{"file":v["file"],"sha256":v["sha256"],"bytes":v["bytes"],"finite_hunks":v["edit_count"]} for k,v in proofs.items()},"Source_checks":len(checks),"full_byte_AST_inverse":True,"new_Q":None,"business":False}))


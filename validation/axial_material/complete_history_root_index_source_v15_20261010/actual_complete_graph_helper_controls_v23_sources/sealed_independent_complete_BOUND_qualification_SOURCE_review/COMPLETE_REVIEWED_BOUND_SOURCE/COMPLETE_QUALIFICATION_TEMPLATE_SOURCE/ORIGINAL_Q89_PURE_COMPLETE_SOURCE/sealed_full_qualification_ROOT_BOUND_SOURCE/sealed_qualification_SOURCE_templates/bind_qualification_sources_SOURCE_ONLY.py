#!/usr/bin/env python3
"""Root-only metadata SOURCE binding. Never import/run helper, host or guard."""
from pathlib import Path
import argparse,ast,hashlib,json,math,os,stat
PACKAGE=Path(__file__).resolve().parent
B=Path("/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010")
CANONICAL_HELPER=Path("/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py")
CANDIDATE_SHA="cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c"
CANDIDATE_BYTES=148965
WITNESS_PATH=B/"actual_complete_graph_helper_controls_v22_receipts/Root_actual_helper_SOURCE_install_tool_return.json"
RECORD_PATH=B/"actual_complete_graph_helper_controls_v22_sources/Root_helper_SOURCE_install_record.json"
INSTALL_SCHEMA="ROOT_V22_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1"
RECORD_SCHEMA="ROOT_V22_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1"
UNKNOWN_Q=None
SIX_FUTURE_BUSINESS_PINS=[None]*6

def require(condition,message):
    if type(condition) is not bool or not condition:raise ValueError(message)
def sha(value):return type(value) is str and len(value)==64 and all(c in "0123456789abcdef" for c in value)
def identity(path):
    s=path.lstat();require(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not path.is_symlink(),"normal private single-link SOURCE metadata required")
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path,expected_sha=None,expected_identity=None,max_bytes=10*2**20):
    path=Path(path);before=identity(path);require(before[4]<=max_bytes,"bounded SOURCE metadata required")
    h=hashlib.sha256();count=0
    with path.open("rb") as f:
        for block in iter(lambda:f.read(2**20),b""):h.update(block);count+=len(block)
    require(identity(path)==before and count==before[4],"full SOURCE EOF/7identity changed")
    value={"path":str(path),"sha256":h.hexdigest(),"identity":before}
    if expected_sha is not None:require(sha(expected_sha) and value["sha256"]==expected_sha,"fixed SOURCE SHA mismatch")
    if expected_identity is not None:
        require(type(expected_identity) is list and len(expected_identity)==7 and all(type(v) is int for v in expected_identity) and expected_identity==before,"exact seven Python integers SOURCE identity mismatch")
    return value
def read(path,expected_sha=None,expected_identity=None,max_bytes=10*2**20):
    before=pin(path,expected_sha,expected_identity,max_bytes);raw=Path(path).read_bytes()
    require(len(raw)==before["identity"][4] and pin(path,expected_sha,expected_identity,max_bytes)==before,"full SOURCE bytes changed during read")
    return raw,before
def reject(value):raise ValueError("nonfinite metadata constant: "+value)
def pairs(values):
    result={}
    for key,value in values:
        require(key not in result,"duplicate SOURCE metadata key");result[key]=value
    return result
def obj(raw):
    value=json.loads(raw,parse_constant=reject,object_pairs_hook=pairs)
    require(type(value) is dict,"complete SOURCE metadata object required");return value
def typed_pin(value):
    require(type(value) is dict and set(value)=={"path","sha256","identity"} and type(value["path"]) is str and Path(value["path"]).is_absolute() and sha(value["sha256"]) and type(value["identity"]) is list and len(value["identity"])==7 and all(type(v) is int for v in value["identity"]),"exact SOURCE path/SHA/seven integer pin required")
    return value
def bind(raw,changes):
    text=raw.decode("utf-8");hunks=[]
    for before,after in changes:
        require(text.count(before)==1,"one exact finite SOURCE binding anchor required")
        text=text.replace(before,after,1);hunks.append({"before":before,"after":after})
    restored=text
    for h in reversed(hunks):
        require(restored.count(h["after"])==1,"one exact finite inverse anchor required")
        restored=restored.replace(h["after"],h["before"],1)
    require(restored.encode()==raw,"whole SOURCE bytes inverse required")
    require(ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(raw),include_attributes=False),"whole SOURCE AST inverse required")
    ast.parse(text);return text.encode(),hunks
def write(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return pin(path)
def write_json(path,value):return write(path,(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+"\n").encode())

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--install-tool-return",required=True)
    a.add_argument("--install-tool-return-sha256",required=True)
    a.add_argument("--template-manifest-sha256",required=True)
    a.add_argument("--output-dir",required=True)
    args=a.parse_args()
    destination=Path(args.output_dir)
    require(destination.is_absolute() and destination.parent==Path("/private/tmp") and not os.path.lexists(destination),"fresh direct private/tmp SOURCE output required; never project D/E")
    manifest_raw,manifest_pin=read(PACKAGE/"MANIFEST.json",args.template_manifest_sha256)
    manifest=obj(manifest_raw)
    require(manifest["schema"]=="AXMAT_V22_FULL_PROTOCOL_AND_CURRENT_GRAPH_QUALIFICATION_SOURCE_SEAL_V1" and manifest["source_only"] is True and manifest["new_Q"] is None and manifest["business_executed"] is False,"exact sealed UNREADY SOURCE package required")
    expected={Path(e["path"]).name for e in manifest["members"]}|{"MANIFEST.json"}
    require(set(p.name for p in PACKAGE.iterdir())==expected and len(expected)==len(manifest["members"])+1,"complete flat sealed SOURCE package inventory required")
    members={}
    for e in manifest["members"]:
        name=Path(e["path"]).name
        require(Path(e["path"]).parent==PACKAGE and name not in members,"full Source package member path required")
        raw,p=read(PACKAGE/name,e["sha256"],e["identity"])
        require(len(raw)==e["bytes"],"all SOURCE member full bytes required")
        members[name]=(raw,p)
    witness_path=Path(args.install_tool_return)
    require(witness_path==WITNESS_PATH,"fixed actual Root V22 SOURCE install witness required")
    witness_raw,witness_pin=read(witness_path,args.install_tool_return_sha256,max_bytes=2*2**20)
    w=obj(witness_raw)
    require(w["schema"]==INSTALL_SCHEMA and w["closed"] is True and w["actual_tool_terminal_return_observed"] is True and w["source_only"] is True,"actual observed closed SOURCE-only installation required")
    tr=w["terminal_tool_return"]
    require(type(tr) is dict and type(tr.get("exit_code")) is int and tr["exit_code"]==0 and "session_id" not in tr and type(tr.get("chunk_id")) is str and bool(tr["chunk_id"]) and type(tr.get("original_token_count")) is int and tr["original_token_count"]>=0 and type(tr.get("wall_time_seconds")) in (int,float) and math.isfinite(tr["wall_time_seconds"]) and tr["wall_time_seconds"]>=0 and type(tr.get("output")) is str,"real typed integer0 CLOSED tool terminal required")
    require(w["exact_integer_pins_decoded_from_actual_terminal_output"] is True and w["original_actual_terminal_output_preserved_exact"] is True,"actual original tool output and exact Python integers must be preserved")
    require(all(w[k] is False for k in ("actual_pure_helper_protocol_qualified","actual_full_current_graph_verifier_qualified","complete_build_qualified","whole_INPUT_admitted","native_RSS_qualified","AAA_accuracy_qualified","ABA_admitted")) and w["actual_new_helper_qualification_sha256"] is None,"Source install cannot grant future qualification")
    helper=typed_pin(w["installed_helper"]);record=typed_pin(w["source_install_record"])
    output=obj(tr["output"])
    require(typed_pin(output["installed_helper"])==helper and typed_pin(output["source_install_record"])==record,"full seven integers must match actual original install terminal JSON exactly")
    require(output["new_helper_qualified"] is False,"actual source terminal may not grant helper qualification")
    require(Path(helper["path"])==CANONICAL_HELPER and helper["sha256"]==CANDIDATE_SHA and helper["identity"][4]==CANDIDATE_BYTES and Path(record["path"])==RECORD_PATH,"only independently reviewed cf0c full helper and new fixed record may bind")
    require(pin(CANONICAL_HELPER,CANDIDATE_SHA,helper["identity"],2*2**20)==helper,"actual installed helper full EOF/7identity mismatch")
    record_raw,record_pin=read(RECORD_PATH,record["sha256"],record["identity"],2*2**20)
    source_record=obj(record_raw)
    require(record_pin==record and source_record["schema"]==RECORD_SCHEMA and typed_pin(source_record["installed_helper"])==helper and source_record["source_only"] is True,"actual full SOURCE installation record required")
    require(all(source_record[k] is False for k in ("actual_pure_helper_protocol_qualified","actual_full_current_graph_verifier_qualified","actual_complete_build_qualified","whole_INPUT_admitted","native_RSS_qualified","AAA_accuracy_qualified","ABA_admitted","business_or_guard_or_helper_API_executed")) and source_record["actual_new_helper_qualification_sha256"] is None,"full record Source-only boundaries required")
    # Full copied Source inventory is preserved in the exact record bytes. The
    # normal hosts later pin every dynamic D member, with no fixed member count.
    files=source_record["source_packages"]["complete_copied_files"]
    require(type(files) is dict and type(source_record["source_file_count"]) is int and len(files)==source_record["source_file_count"]>0,"complete recorded Source file inventory required")
    copied_source_pins=[]
    for literal,item in files.items():
        q=typed_pin(item)
        require(q["path"]==literal and Path(literal).is_relative_to(RECORD_PATH.parent),"recorded copied Source must remain in full new D namespace")
        require(pin(q["path"],q["sha256"],q["identity"])==q,"full recorded Source copy unchanged")
        copied_source_pins.append(q)
    pure_driver,pd_hunks=bind(members["pure_helper_controls.v22.UNREADY.py"][0],[
        ("HELPER_PATH = None","HELPER_PATH = "+repr(helper["path"])),
        ("HELPER_SHA256 = None","HELPER_SHA256 = "+repr(helper["sha256"])),
        ("HELPER_SOURCE_BYTES = None","HELPER_SOURCE_BYTES = "+repr(helper["identity"][4]))])
    pure_driver_sha=hashlib.sha256(pure_driver).hexdigest()
    pure_host,ph_hunks=bind(members["pure_helper_controls_host.v22.UNREADY.py"][0],[
        ("TARGET_SHA=None","TARGET_SHA="+repr(pure_driver_sha)),
        ("support.pin(Path(None),None)","support.pin(Path("+repr(helper["path"])+"),"+repr(helper["sha256"])+")")])
    fresh_driver,fd_hunks=bind(members["fresh_verifier_controls.v22.UNREADY.py"][0],[
        ("SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'"),
        ("NEW_HELPER_PATH = None","NEW_HELPER_PATH = "+repr(helper["path"])),
        ("NEW_HELPER_SHA256 = None","NEW_HELPER_SHA256 = "+repr(helper["sha256"])),
        ("NEW_HELPER_SOURCE_BYTES = None","NEW_HELPER_SOURCE_BYTES = "+repr(helper["identity"][4])),
        ("NEW_HELPER_IDENTITY = None","NEW_HELPER_IDENTITY = "+repr(helper["identity"]))])
    fresh_driver_sha=hashlib.sha256(fresh_driver).hexdigest()
    fresh_host,fh_hunks=bind(members["fresh_verifier_host.v22.UNREADY.py"][0],[
        ("SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'"),
        ("TARGET_SHA=None","TARGET_SHA="+repr(fresh_driver_sha)),
        ("BOUND_HELPER_PIN=None","BOUND_HELPER_PIN="+repr(helper)),
        ("INSTALL_WITNESS_PIN=None","INSTALL_WITNESS_PIN="+repr(witness_pin)),
        ("SOURCE_INSTALL_RECORD_PIN=None","SOURCE_INSTALL_RECORD_PIN="+repr(record_pin))])
    for q in [helper,record,witness_pin]+copied_source_pins+[v[1] for v in members.values()]+[manifest_pin]:
        require(pin(q["path"],q["sha256"],q["identity"])==q,"all complete Source/metadata inputs remain unchanged")
    destination.mkdir(mode=0o700)
    for name,(raw,q) in members.items():write(destination/"sealed_qualification_SOURCE_templates"/name,raw)
    write(destination/"sealed_qualification_SOURCE_templates/MANIFEST.json",manifest_raw)
    write(destination/"Root_actual_SOURCE_install_witness.exact.json",witness_raw)
    write(destination/"Root_actual_SOURCE_install_record.exact.json",record_raw)
    bound={}
    for name,raw in [("pure_helper_controls.py",pure_driver),("pure_helper_controls_host.py",pure_host),("fresh_verifier_controls.py",fresh_driver),("fresh_verifier_host.py",fresh_host)]:
        bound[name]=write(destination/name,raw)
    inverse=write_json(destination/"ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json",{"schema":"AXMAT_V22_ROOT_ACTUAL_SOURCE_ONLY_QUALIFICATION_BINDING_INVERSES_V1","status":"SOURCE_READY_BINDING_GENERATED_NOT_EXECUTED","hunks":{"pure_driver":pd_hunks,"pure_host":ph_hunks,"fresh_driver":fd_hunks,"fresh_host":fh_hunks},"all_four_complete_template_bytes_AST_inverse":True,"template_original_actual_entrypoint_finite_inverse":"sealed_qualification_SOURCE_templates/ALL_FOUR_FULL_SOURCE_INVERSES.json","bound_sources":bound,"actual_installed_helper":helper,"actual_Source_install_witness":witness_pin,"actual_Source_install_record":record_pin,"complete_source_file_inventory_from_record":copied_source_pins,"template_manifest":manifest_pin,"new_Q":None,"six_future_business_pins":[None]*6,"actual_original_new_protocol_or_fresh_verifier_qualification":None,"candidate_helper_host_guard_or_business_executed":False})
    for q in [helper,record,witness_pin]+copied_source_pins+[v[1] for v in members.values()]+[manifest_pin]:
        require(pin(q["path"],q["sha256"],q["identity"])==q,"Source binding cannot mutate any existing complete input")
    print(json.dumps({"status":"SOURCE_READY_BINDING_GENERATED_NOT_EXECUTED","bound_SOURCE_root":str(destination),"sources":bound,"inverse":inverse,"all_complete_package_members_copied":len(members)+1,"new_Q":None,"six_future_business_pins":[None]*6,"project_D_E_canonical_or_ART_written":False,"controls_helper_API_guard_business_executed":False},allow_nan=False))

if __name__=="__main__":main()


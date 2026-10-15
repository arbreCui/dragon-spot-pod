"""Finite SOURCE adaptation only; no Root PREP metadata or project code execution."""
import ast
import hashlib
import json
from pathlib import Path
import stat

DEST = Path(__file__).parent
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
PARENT = Path('/private/tmp/axmat_v19_complete_combined_build_host_source_design_20261010/generate_build_host.py')
PARENT_SHA = 'dc48a3c47804359ba483bab74da31df3cd5aebad0a2935c994211ebd76293d39'
WRITER19 = BASE/'actual_complete_combined_prepare_v19_receipts/write_actual_prepare_terminal.py'
WRITER19_SHA = '7c69f1479af9a6527c6db3785f97a790269c3a0069a958391fdd467a3802df32'
WRITER20 = BASE/'actual_complete_combined_prepare_v20_receipts/write_actual_prepare_terminal.py'
WRITER20_SHA = 'af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539'
TARGET19_SHA = '34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b'
TARGET20_SHA = '566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3'
GENERATOR_CHANGES = [('V19','V20',19),('v19','v20',16),(TARGET19_SHA,TARGET20_SHA,1)]
WRITER_CHANGES = [('V19','V20',4),('v19','v20',7),(TARGET19_SHA,TARGET20_SHA,1)]

def pin(path, expected):
    path = Path(path)
    if '/validation/artifacts/' in str(path) or not path.is_absolute() or path.resolve()!=path:
        raise ValueError('ordinary SOURCE path only; no ART reads')
    before=path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1:
        raise ValueError('regular unique SOURCE required')
    data=path.read_bytes(); after=path.lstat()
    fields=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    if fields(before)!=fields(after) or len(data)!=after.st_size or hashlib.sha256(data).hexdigest()!=expected:
        raise ValueError('complete fresh SOURCE SHA7ID pin mismatch')
    return data,dict(path=str(path),sha256=expected,identity=fields(after))

def finite(text, changes):
    records=[]
    for before,after,count in changes:
        if text.count(before)!=count:
            raise ValueError('finite replacement occurrence mismatch')
        text=text.replace(before,after)
        records.append(dict(before=before,after=after,count=count))
    return text,records

def inverse(text, records):
    for record in reversed(records):
        if text.count(record['after'])!=record['count']:
            raise ValueError('whole-byte inverse occurrence mismatch')
        text=text.replace(record['after'],record['before'])
    return text

def write_new(path, data):
    with path.open('xb') as f:f.write(data)

def main():
    old,old_pin=pin(PARENT,PARENT_SHA)
    writer19,w19_pin=pin(WRITER19,WRITER19_SHA)
    writer20,w20_pin=pin(WRITER20,WRITER20_SHA)
    new,changes=finite(old.decode(),GENERATOR_CHANGES)
    if inverse(new,changes).encode()!=old:
        raise ValueError('exact complete generator inverse to dc48 required')
    expected_writer,writer_changes=finite(writer19.decode(),WRITER_CHANGES)
    if expected_writer.encode()!=writer20 or inverse(writer20.decode(),writer_changes).encode()!=writer19:
        raise ValueError('actual af0c writer must have complete inverse to actual 7c69 writer')
    if '7c69f147' in old.decode() or 'WRITER_SHA' in old.decode():
        raise ValueError('unexpected writer binding in frozen parent generator')
    tree=ast.parse(new)
    definitions=[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    parent_definitions=[n.name for n in ast.parse(old.decode()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    if definitions!=parent_definitions:
        raise ValueError('all original generator definitions retained')
    compile(new,str(DEST/'generate_build_host.py'),'exec')
    compile(writer20.decode(),str(WRITER20),'exec')
    # SOURCE AST only: verify direct writer keys and aliases used by the unchanged binding branch.
    writer_tree=ast.parse(writer20.decode())
    main_node=next(n for n in writer_tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    summary_keywords=set()
    for node in ast.walk(main_node):
        if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='summary' for x in node.targets):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='dict':
                summary_keywords.update(x.arg for x in node.value.keywords)
    added_summary={}
    for node in ast.walk(main_node):
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Subscript):
            target=node.targets[0]
            if isinstance(target.value,ast.Name) and target.value.id=='summary' and isinstance(target.slice,ast.Constant):
                added_summary[target.slice.value]=ast.dump(node.value,include_attributes=False)
    required_direct={'actual_root_terminal','formal_PREP_terminal','actual_declaration','actual_input_graph','whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries','whole_seconds','child_seconds','sampled_peak_rss_mib','joint_archive_bytes','whole_combined_INPUT_admitted','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted','goal_complete'}
    required_added={'Root_actual_terminal','actual_complete_input_graph','actual_complete_creation_trace','namespace_manifest','original_caps_preserved','original_five_build_stages_executed','native_RSS_qualified','cleanup_performed'}
    if not required_direct<=summary_keywords or not required_added<=set(added_summary):
        raise ValueError('unchanged actual writer fields must cover generator Root metadata contract')
    for path,expected,ref in [(PARENT,PARENT_SHA,old_pin),(WRITER19,WRITER19_SHA,w19_pin),(WRITER20,WRITER20_SHA,w20_pin)]:
        _,again=pin(path,expected)
        if again!=ref: raise ValueError('fresh SOURCE identity changed')
    proof=dict(schema='AXMAT_V20_FINITE_BUILD_GENERATOR_SOURCE_ADAPTATION_V1',status='UNREADY_SOURCE_TEMPLATE_NO_ACTUAL_V20_PREP_PINS',parent_source=old_pin,generator_path=str(DEST/'generate_build_host.py'),generator_sha256=hashlib.sha256(new.encode()).hexdigest(),finite_change_count=len(changes),changes=changes,complete_byte_inverse_to_dc48=True,unchanged_definitions=definitions,actual_writer19_source=w19_pin,actual_writer20_source=w20_pin,writer_finite_changes=writer_changes,complete_actual_writer_inverse_af0c_to_7c69=True,writer_binding_location='SOURCE proof only; frozen dc48 generator has no writer global or runtime writer interface',writer_required_direct_fields=sorted(required_direct),writer_required_added_fields=sorted(required_added),writer_added_field_source_AST=added_summary,original_cf2c_host_sha256='cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9',original_cf2c_to_37d_full_inverse_proof_sha256='29a05241b38bcd4d878d058dc27b023a07e8356993c53ff033575ed16d50a6d6',original_37d_host_sha256='37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3',previous_normal_v19_host_sha256='f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580',canonical_v20_SOURCE_sha256=TARGET20_SHA,future_actual_Root_PREP_summary_sha256=None,future_actual_Root_PREP_terminal_sha256=None,future_actual_declaration_sha256=None,future_actual_formal_PREP_terminal_sha256=None,future_actual_complete_input_graph_sha256=None,future_actual_complete_creation_trace_sha256=None,parameter_contract=['real_fixed_Root_V20_closed_PREP_summary_path','real_full_summary_sha256'],all_original_five_stages_retained=True,all_four_metadata_tools_seal_and_full_tails_retained=True,genuine_guard_and_MRO_unchanged=True,outer_seconds=1800,inner_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0,archive_scope=['HOST','SOURCE','OUT','TERMINAL','new_SOURCE_ARCHIVE'],host_generated=False,binding_branch_executed=False,business_executed=False,project_API_imported=False,ART_read_or_written=False,numeric_payload_read=False,native_executed=False,whole_combined_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False)
    write_new(DEST/'generate_build_host.py',new.encode())
    write_new(DEST/'frozen_parent_generate_build_host_v19.py',old)
    write_new(DEST/'actual_writer_v19_SOURCE.py',writer19)
    write_new(DEST/'actual_writer_v20_SOURCE.py',writer20)
    proof_path=DEST/'Root_finite_build_generator_source_inverse.json'
    write_new(proof_path,(json.dumps(proof,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps(dict(status=proof['status'],generator=str(DEST/'generate_build_host.py'),generator_sha256=proof['generator_sha256'],proof=str(proof_path),proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),full_inverse_dc48=True,actual_writer_full_inverse=True,host_generated=False,binding_branch_executed=False,business_executed=False)))

if __name__=='__main__':main()

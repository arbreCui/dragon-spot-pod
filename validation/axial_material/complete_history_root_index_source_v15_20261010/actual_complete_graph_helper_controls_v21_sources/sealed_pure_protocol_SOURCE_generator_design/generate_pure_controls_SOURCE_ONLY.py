"""SOURCE-only generation; two real Root installation-record argv required to bind."""
import ast
import hashlib
import json
from pathlib import Path
import re
import stat
import sys

DEST=Path(__file__).parent
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
OLD_D=BASE/'actual_complete_graph_helper_controls_v17_sources'
OLD_DRIVER=OLD_D/'pure_helper_controls.py'
OLD_DRIVER_SHA='da4bd8438cb5007e8e7a5817ba9e198237aa93766af769898d971adf9708e68e'
OLD_HOST=OLD_D/'pure_helper_controls_host.py'
OLD_HOST_SHA='de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2'
OLD_INVERSE=OLD_D/'Root_finite_source_binding_and_host_inverse.json'
HELPER_PATH='/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py'
HELPER_SHA='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
HELPER_BYTES=147870
NEW_D=BASE/'actual_complete_graph_helper_controls_v21_sources'
NEW_E=BASE/'actual_complete_graph_helper_controls_v21_receipts'
ART='/Users/wen/spot/validation/artifacts/'
HOST=ART+'axial-material-complete-graph-private-verifier-helper-controls-host-v21-20261010'
OUT=ART+'axial-material-complete-graph-private-verifier-helper-controls-v21-20261010'
DRAFT_STATUS='UNREADY_SOURCE_DESIGN_AWAIT_REAL_ROOT_CLOSED_HELPER_INSTALL_RECORD'
DRIVER_CHANGES=[
('HELPER_PATH = "/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py"',f'HELPER_PATH = "{HELPER_PATH}"',1),
('HELPER_SHA256 = "bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6"',f'HELPER_SHA256 = "{HELPER_SHA}"',1),
('HELPER_SOURCE_BYTES = 145715',f'HELPER_SOURCE_BYTES = {HELPER_BYTES}',1)]

def pin(path,expected=None):
    path=Path(path)
    if not path.is_absolute()or path.resolve()!=path or '/validation/artifacts/'in str(path):raise ValueError('ordinary SOURCE/Root metadata only; no ART')
    a=path.lstat()
    if not stat.S_ISREG(a.st_mode)or a.st_nlink!=1:raise ValueError('unique regular SOURCE/metadata file required')
    data=path.read_bytes();b=path.lstat();identity=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    digest=hashlib.sha256(data).hexdigest()
    if identity(a)!=identity(b)or len(data)!=b.st_size or(expected is not None and digest!=expected):raise ValueError('complete fresh SHA7ID mismatch')
    return data,dict(path=str(path),sha256=digest,identity=identity(b))

def write_new(path,data):
    with path.open('xb')as f:f.write(data)

def json_bytes(value):return(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()

def changed(text,edits):
    records=[]
    for before,after,count in edits:
        if text.count(before)!=count:raise ValueError('finite SOURCE replacement count mismatch')
        text=text.replace(before,after);records.append(dict(before=before,after=after,count=count))
    return text,records

def inverse(text,records):
    for r in reversed(records):
        if text.count(r['after'])!=r['count']:raise ValueError('full SOURCE inverse occurrence mismatch')
        text=text.replace(r['after'],r['before'])
    return text

def source_design():
    driver,dp=pin(OLD_DRIVER,OLD_DRIVER_SHA);host,hp=pin(OLD_HOST,OLD_HOST_SHA);proof_data,ip=pin(OLD_INVERSE)
    if len(driver)!=58291:raise ValueError('complete original 58291-byte control driver required')
    lineage=json.loads(proof_data);ancestor=host.decode()
    if lineage['host_sha256']!=OLD_HOST_SHA or lineage['driver_sha256']!=OLD_DRIVER_SHA:raise ValueError('complete original template lineage required')
    for r in reversed(lineage['finite_changes']):
        if ancestor.count(r['new'])!=r['occurrences']:raise ValueError('complete original host inverse count required')
        ancestor=ancestor.replace(r['new'],r['old'])
    if hashlib.sha256(ancestor.encode()).hexdigest()!=lineage['parent_host_sha256']:raise ValueError('entire original host inverse to82a required')
    for r in reversed(lineage['original95_parent_proof']['changes']):
        if ancestor.count(r['new'])!=r['occurrences']:raise ValueError('complete genuine95fd ancestor inverse count required')
        ancestor=ancestor.replace(r['new'],r['old'])
    if hashlib.sha256(ancestor.encode()).hexdigest()!='95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f':raise ValueError('entire original genuine95fd host SHA exact required')
    new_driver,driver_records=changed(driver.decode(),DRIVER_CHANGES)
    new_driver_sha=hashlib.sha256(new_driver.encode()).hexdigest()
    host_edits=[
      ('axial-material-complete-graph-trace-table-helper-controls-host-v17-20261010',Path(HOST).name,1),
      ('axial-material-complete-graph-trace-table-helper-controls-v17-20261010',Path(OUT).name,1),
      (f'SOURCE_ARCHIVE=Path(\'{OLD_D}\')',f'SOURCE_ARCHIVE=Path(\'{NEW_D}\')',1),
      (f'TARGET=Path(\'{OLD_DRIVER}\')',f'TARGET=Path(\'{NEW_D}/pure_helper_controls.py\')',1),
      (f'TARGET_SHA=\'{OLD_DRIVER_SHA}\'',f'TARGET_SHA=\'{new_driver_sha}\'',1),
      ('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py',HELPER_PATH,1),
      ('bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',HELPER_SHA,1),
      ('AXMAT_V17_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1','AXMAT_V21_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1',1)]
    new_host,host_records=changed(host.decode(),host_edits)
    if inverse(new_driver,driver_records).encode()!=driver or inverse(new_host,host_records).encode()!=host:raise ValueError('both entire finite SOURCE inverses required')
    old_tree=ast.parse(driver.decode());new_tree=ast.parse(new_driver)
    functions=lambda tree:[ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    if functions(old_tree)!=functions(new_tree):raise ValueError('all complete original driver functions/classes exact')
    for name in ('SOURCE_STATUS','ACTUAL_SUCCESS_PINS','PARENT_HELPER_SHA256','MAX_JSON_BYTES','MAX_OUTPUT_BYTES','RSS_BYTES','WALL_SECONDS','CHILD_LIMIT','RETRIES','GRAPH_PIN','TRACE_PIN','TRACE_ORIGINAL_ORDER_COMPACT_PIN'):
        def value_node(tree):return next(ast.dump(n.value,include_attributes=False)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
        if value_node(old_tree)!=value_node(new_tree):raise ValueError('original driver metadata/caps/control globals exact: '+name)
    compile(new_driver,str(DEST/'pure_helper_controls.py'),'exec');compile(new_host,str(DEST/'pure_helper_controls_host.py'),'exec')
    for ref in (dp,hp,ip):
        _,again=pin(ref['path'],ref['sha256'])
        if ref!=again:raise ValueError('all fixed SOURCE inputs stay fresh exact')
    value=dict(schema='AXMAT_V21_PURE_CONTROLS_FINITE_SOURCE_GENERATOR_DESIGN_V1',status=DRAFT_STATUS,original_driver=dp,original_host=hp,original_whole_host_inverse=ip,reused_original_host_lineage=lineage,driver_finite_changes=driver_records,host_finite_changes=host_records,driver_change_count=3,host_change_count=8,full_driver_inverse_to_da4=True,full_host_inverse_to_de72_and82a_and95fd=True,original_all_driver_functions_classes_controls_and_caps_exact=True,original_SOURCE_STATUS_parent_lineage_GRAPH_TRACE_pins_exact=True,driver_schema_V16_unchanged=True,only_host_result_schema_retargeted_V21=True,designed_driver_SOURCE_sha256=new_driver_sha,designed_host_SOURCE_sha256=hashlib.sha256(new_host.encode()).hexdigest(),designed_sources_not_installed_or_executed=True,helper_canonical_SOURCE_path=HELPER_PATH,helper_canonical_SOURCE_sha256=HELPER_SHA,helper_SOURCE_bytes=HELPER_BYTES,planned_business_namespaces=dict(HOST=HOST,OUT=OUT,D=str(NEW_D),E=str(NEW_E),TARGET=str(NEW_D/'pure_helper_controls.py')),whole_seconds=60,stage_seconds=60,rss_mib=512,strict_JSON_bytes=64*2**20,archive_bytes=64*2**20,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0,archive_scope=['HOST','OUT','SOURCE_ARCHIVE'],normal_guard_MRO_original_support_and_resource_classes_exact=True,actual_Root_helper_install_record=None,actual_Root_closed_install_tool=None,actual_NEW_helper_pure_protocol_qualification=None,actual_NEW_current_graph_fresh_verifier_qualification=None,actual_NEW_combined_decl_build_INPUT_native_science_pins=None,binding_branch_executed=False,business_or_API_or_helper_or_guard_or_control_executed=False,ART_read_or_written=False,numeric_payload_read=False,history_scanned=False)
    return new_driver,new_host,value,[dp,hp,ip]

def main():
    new_driver,new_host,value,sources=source_design()
    if sys.argv[1:]==['--check-source-only']:
        report=DEST/'SOURCE_DESIGN_REPORT.json';write_new(report,json_bytes(value))
        print(json.dumps(dict(status=DRAFT_STATUS,report=str(report),report_sha256=hashlib.sha256(report.read_bytes()).hexdigest(),designed_driver_SOURCE_sha256=value['designed_driver_SOURCE_sha256'],designed_host_SOURCE_sha256=value['designed_host_SOURCE_sha256'],binding_branch_executed=False,driver_or_host_generated=False,business_executed=False)))
        return
    if len(sys.argv)!=3 or re.fullmatch('[0-9a-f]{64}',sys.argv[2])is None:raise ValueError('two argv: actual Root helper installation record path and actual full SHA required')
    record_path=Path(sys.argv[1])
    if not record_path.is_relative_to(BASE):raise ValueError('actual Root installation metadata under fixed complete history SOURCE archive required')
    record_data,record_pin=pin(record_path,sys.argv[2]);record=json.loads(record_data)
    tr=record['terminal_tool_return']
    if record['closed']is not True or type(tr.get('exit_code'))is not int or tr['exit_code']!=0 or 'session_id'in tr or record.get('session_repolled_after_close',False)is not False:raise ValueError('real Root typedEXIT0 closed helper installation witness required')
    installed=record['installed_helper']
    if installed.get('path')!=HELPER_PATH or installed.get('sha256')!=HELPER_SHA:raise ValueError('actual installed helper path and SHA must be the fixed independently reviewed SOURCE')
    installed_identity=installed.get('identity',installed.get('identity7'))
    if not isinstance(installed_identity,list)or len(installed_identity)!=7 or any(type(x)is not int for x in installed_identity)or installed_identity[4]!=HELPER_BYTES:raise ValueError('actual installed complete helper7ID and147870bytes required')
    _,helper_pin=pin(HELPER_PATH,HELPER_SHA)
    if helper_pin['identity']!=installed_identity:raise ValueError('actual Root installed helper complete SOURCE identity differs')
    for ref in sources+[record_pin,helper_pin]:
        _,again=pin(ref['path'],ref['sha256'])
        if ref!=again:raise ValueError('all SOURCE and real installation metadata pins stay fresh exact')
    for p in(DEST/'pure_helper_controls.py',DEST/'pure_helper_controls_host.py',DEST/'Root_finite_bound_controls_source_inverse.json'):
        if p.exists():raise ValueError('all metadata SOURCE candidate outputs must be fresh')
    bound=dict(value,status='SOURCE_ONLY_REAL_INSTALL_RECORD_BOUND_NOT_EXECUTED',actual_Root_helper_install_record=record_pin,actual_Root_closed_install_tool=tr,actual_installed_helper=helper_pin,binding_branch_executed=True,driver_or_host_executed=False)
    write_new(DEST/'pure_helper_controls.py',new_driver.encode());write_new(DEST/'pure_helper_controls_host.py',new_host.encode())
    proof_path=DEST/'Root_finite_bound_controls_source_inverse.json';write_new(proof_path,json_bytes(bound))
    print(json.dumps(dict(status=bound['status'],driver=str(DEST/'pure_helper_controls.py'),driver_sha256=value['designed_driver_SOURCE_sha256'],host=str(DEST/'pure_helper_controls_host.py'),host_sha256=value['designed_host_SOURCE_sha256'],proof=str(proof_path),proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),actual_install_record_sha256=record_pin['sha256'],new_pure_protocol_qualification=None,business_executed=False)))

if __name__=='__main__':main()

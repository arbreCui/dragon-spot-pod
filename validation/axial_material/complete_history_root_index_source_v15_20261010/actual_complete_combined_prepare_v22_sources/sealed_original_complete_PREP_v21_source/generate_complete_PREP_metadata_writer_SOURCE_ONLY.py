"""Generate metadata-writer SOURCE and archive fixed READY SOURCE bytes; execute no project logic."""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

BASE = Path('/private/tmp/axmat_v21_COMPLETE_READY_runtime_genuine_PREP_closed_metadata_SOURCE_20261010_syx41')
OLD_PACKAGE = Path('/private/tmp/axmat_v21_actual_joint_Q_READY_runtime_PREP_SOURCE_binding_20261010_m2r8v')
OLD_MANIFEST_SHA = '5b8653db81265f06eddbe6e9fb9e66c59dacbb8608537a69b4ca58244cbf30d3'
PARENT = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v20_sources/sealed_metadata_writer_source_binding/write_actual_prepare_terminal.py')
PARENT_SHA = 'af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539'
PARENT_IDENTITY = [16777229,49377171,33188,1,9989,1791587008890997641,1791587386238673992]
RUNTIME_SHA = '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
HOST_SHA = '776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405'


def identity(st):
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]


def read_source(path):
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ValueError('Regular single-link SOURCE required')
    if path.resolve() != path:
        raise ValueError('Literal canonical SOURCE path with no symlink required')
    with path.open('rb') as stream:
        if identity(os.fstat(stream.fileno())) != identity(before):
            raise ValueError('SOURCE identity changed before reading')
        data = stream.read()
        if identity(os.fstat(stream.fileno())) != identity(before):
            raise ValueError('SOURCE identity changed during reading')
    if identity(path.lstat()) != identity(before) or len(data) != before.st_size:
        raise ValueError('SOURCE complete EOF or identity changed')
    return data, {'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),
                  'size_bytes':len(data),'identity':identity(before)}


def write(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def write_json(path, value):
    write(path, (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())


def node_source(source, node):
    lines=source.splitlines(keepends=True)
    return ''.join(lines[node.lineno-1:node.end_lineno])


def call_order(node):
    return [ast.dump(call.func,include_attributes=False) for call in ast.walk(node)
            if isinstance(call,ast.Call)]


def main():
    copied = BASE/'sealed_READY_runtime_and_PREP_binding'
    binding = BASE/'metadata_writer_SOURCE_binding'
    if copied.exists() or binding.exists():
        raise ValueError('Writer design output must be fresh')
    manifest_bytes, manifest_pin = read_source(OLD_PACKAGE/'sealed_SOURCE_manifest.json')
    if manifest_pin['sha256'] != OLD_MANIFEST_SHA:
        raise ValueError('Fixed initial complete SOURCE seal differs')
    manifest=json.loads(manifest_bytes)
    original_members=manifest['full_member_inventory']
    actual_members={str(path.relative_to(OLD_PACKAGE)) for path in OLD_PACKAGE.rglob('*')
                    if path.is_file()}
    if actual_members != set(original_members)|{'sealed_SOURCE_manifest.json'}:
        raise ValueError('Original sealed SOURCE member inventory changed')
    original_data={}
    original_pins={}
    for relative, expected in original_members.items():
        data, current=read_source(OLD_PACKAGE/relative)
        if current != expected:
            raise ValueError('Original sealed SOURCE EOF SHA7ID differs')
        original_data[relative]=data
        original_pins[relative]=current
    original_data['sealed_SOURCE_manifest.json']=manifest_bytes
    original_pins['sealed_SOURCE_manifest.json']=manifest_pin
    runtime=original_data['BOUND_READY_SOURCE/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py']
    host=original_data['BOUND_READY_SOURCE/combined_prepare_host.py']
    if hashlib.sha256(runtime).hexdigest()!=RUNTIME_SHA or hashlib.sha256(host).hexdigest()!=HOST_SHA:
        raise ValueError('Fixed READY runtime or genuine normal host differs')
    parent_bytes, parent_pin=read_source(PARENT)
    if parent_pin['sha256']!=PARENT_SHA or parent_pin['identity']!=PARENT_IDENTITY:
        raise ValueError('Fixed full original metadata writer SOURCE differs')
    parent=parent_bytes.decode('utf-8')
    edits=[
      ('docstring','successful V20 PREP tool return.','successful V21 PREP tool return.'),
      ('SOURCE archive',"D=BASE/'actual_complete_combined_prepare_v20_sources'", "D=BASE/'actual_complete_combined_prepare_v21_sources'"),
      ('receipt namespace',"E=BASE/'actual_complete_combined_prepare_v20_receipts'", "E=BASE/'actual_complete_combined_prepare_v21_receipts'"),
      ('HOST namespace',"H=ART/'axial-material-complete-combined-prepare-host-v20-20261010'", "H=ART/'axial-material-complete-combined-prepare-host-v21-20261010'"),
      ('SOURCE namespace',"S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010'", "S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010'"),
      ('OUT namespace',"O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010'", "O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'"),
      ('TERM namespace',"T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010'", "T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010'"),
      ('canonical factory path',"FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')", "FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')"),
      ('canonical factory actual SOURCE SHA',"FACTORY_SHA='566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3'", "FACTORY_SHA='"+RUNTIME_SHA+"'"),
      ('formal PREP schema','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V20_ACTUAL_EXTERNAL_PREP_RETURN_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_ACTUAL_EXTERNAL_PREP_RETURN_V1'),
      ('complete namespace manifest schema','ROOT_V20_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1','ROOT_V21_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1'),
      ('actual summary schema','ROOT_V20_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1','ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'),
    ]
    candidate=parent
    full_edits=[]
    for label,old,new in edits:
        if candidate.count(old)!=1:
            raise ValueError('Each writer SOURCE anchor must occur exactly once: '+label)
        candidate=candidate.replace(old,new,1)
        full_edits.append({'label':label,'old':old,'new':new,'unique_old_anchor_count':1})
    inverse=candidate
    for edit in reversed(full_edits):
        if inverse.count(edit['new'])!=1:
            raise ValueError('Each writer SOURCE inverse anchor must be unique')
        inverse=inverse.replace(edit['new'],edit['old'],1)
    old_tree=ast.parse(parent)
    new_tree=ast.parse(candidate)
    if inverse.encode()!=parent_bytes or ast.dump(ast.parse(inverse),include_attributes=False)!=ast.dump(old_tree,include_attributes=False):
        raise ValueError('Complete writer SOURCE byte or AST inverse differs')
    compile(new_tree, '<V21 SOURCE-only metadata writer>', 'exec')
    old_functions=[node for node in old_tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    new_functions=[node for node in new_tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    checks=[]
    def checked(name, value):
        if value is not True:
            raise ValueError('Writer SOURCE contract: '+name)
        checks.append({'name':name,'value':True})
    checked('all original definitions preserved in original order',[x.name for x in old_functions]==[x.name for x in new_functions])
    for old,new in zip(old_functions,new_functions):
        old_section=node_source(parent,old)
        new_section=node_source(candidate,new)
        restored=new_section
        for edit in reversed(full_edits):
            restored=restored.replace(edit['new'],edit['old'])
        checked('complete definition SOURCE inverse '+old.name,restored==old_section)
        checked('original Call callee order '+old.name,call_order(old)==call_order(new))
        for kind in (ast.If,ast.Raise,ast.Assert,ast.Return):
            checked('complete original '+kind.__name__+' count '+old.name,
                    sum(isinstance(n,kind) for n in ast.walk(old))==sum(isinstance(n,kind) for n in ast.walk(new)))
        if old.name!='main':
            checked('unmodified definition byteexact '+old.name,new_section==old_section)
    for anchor in (
        "actual=json.loads((E/'Root_actual_prepare_tool_terminal_return.json').read_text())",
        "type(observed.get('exit_code')) is not int or observed['exit_code']!=0 or 'session_id' in observed",
        "actual['closed'] is not True",
        "w['limit_failure'] is not None",
        "w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True",
        "(1800,600,512,2*2**30,1,1,0)",
        "h['input_sources']+[h['original_helper'],h['resource_factory']]",
        "if source_inventory!=d['source_inventory']:",
        "for root in (H,S,O,T,D)",
        "for root in (H,S,O,T,D,E)",
        "with Path(p).open('x')",
        "with (T/name).open('xb')",
        "if pin(src)['sha256']!=pin(T/name)['sha256']",
        "for key in cp['false_fields']: value[key]=False",
        "separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False",
        "summary['actual_complete_creation_trace']=pin(O/'input_creation_python_open_trace.json')",
        "summary['native_RSS_qualified']=False",
        "summary['cleanup_performed']=False",
    ):
        checked('whole unchanged SOURCE anchor '+anchor,anchor in parent and anchor in candidate)
    formal='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_ACTUAL_EXTERNAL_PREP_RETURN_V1'
    runtime_tree=ast.parse(runtime.decode())
    runtime_assignments={target.id:node.value for node in runtime_tree.body
                         if isinstance(node,ast.Assign) for target in node.targets
                         if isinstance(target,ast.Name)}
    prefix_node=runtime_assignments['PREFIX']
    prep_schema_node=runtime_assignments['PREP_TERMINAL_SCHEMA']
    checked('formal PREP schema original PREFIX plus suffix SOURCE shape',
            isinstance(prefix_node,ast.Constant) and type(prefix_node.value) is str
            and isinstance(prep_schema_node,ast.BinOp) and isinstance(prep_schema_node.op,ast.Add)
            and isinstance(prep_schema_node.left,ast.Name) and prep_schema_node.left.id=='PREFIX'
            and isinstance(prep_schema_node.right,ast.Constant)
            and type(prep_schema_node.right.value) is str)
    checked('formal PREP schema bound to fixed full READY runtime',
            prefix_node.value+prep_schema_node.right.value==formal)
    checked('no old V20 namespace/schema/SHA remains','v20' not in candidate.lower() and '566939e3' not in candidate)
    checked('whole canonical writer byte inverse exact',inverse.encode()==parent_bytes)
    checked('whole canonical writer AST inverse exact',ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(old_tree,include_attributes=False))
    copied.mkdir()
    binding.mkdir()
    copy_pins={}
    for relative,data in original_data.items():
        destination=copied/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        write(destination,data)
        copied_bytes, copied_pin=read_source(destination)
        checked('complete original SOURCE archive member byteexact '+relative,copied_bytes==data)
        copy_pins[relative]={'original':original_pins[relative],'copy':copied_pin}
    writer=binding/'write_actual_prepare_terminal.py'
    write(writer,candidate.encode())
    write(binding/'original_metadata_writer_full_SOURCE.txt',parent_bytes)
    writer_data,writer_pin=read_source(writer)
    proof={
       'schema':'AXMAT_V21_COMPLETE_GENUINE_PREP_METADATA_WRITER_SOURCE_FULL_INVERSE_V1',
       'source_only':True,'parent':parent_pin,'candidate':writer_pin,
       'finite_edit_count':len(full_edits),'complete_forward_hunks':full_edits,
       'inverse_full_bytes_equal_parent':True,'inverse_full_AST_equal_parent':True,
       'original_definition_sequence':[x.name for x in old_functions],
       'all_original_definitions_complete_inverse':True,'all_non_main_definitions_byteexact':True,
       'all_original_If_Raise_Assert_Return_counts_and_Call_callee_order_retained':True,
       'main_only_changes_original_version_schema_literals':True,
       'runtime_source_SHA':RUNTIME_SHA,'normal_PREP_host_source_SHA':HOST_SHA,
       'unknown_future_PREP_and_build_terminal_graph_trace_declaration_seal_pins_bound':False,
       'writer_API_guard_business_executed':False,'ART_or_numeric_payload_read':False,
       'canonical_or_frozen_namespace_written':False,'installed':False,
    }
    write_json(binding/'full_metadata_writer_SOURCE_inverse.json',proof)
    for relative,pin_before in original_pins.items():
        _,pin_after=read_source(OLD_PACKAGE/relative)
        checked('whole original sealed SOURCE EOF SHA7ID unchanged '+relative,pin_after==pin_before)
    _,parent_after=read_source(PARENT)
    checked('whole original metadata writer EOF SHA7ID unchanged',parent_after==parent_pin)
    report={
      'schema':'AXMAT_V21_COMPLETE_READY_RUNTIME_GENUINE_PREP_METADATA_SOURCE_CLOSURE_V1',
      'status':'SOURCE_READY_UNINSTALLED_ACTUAL_PREP_TERMINAL_REQUIRED_BEFORE_METADATA_WRITER',
      'checks':checks,'all_checks_typed_true':True,'blockers':[],
      'complete_original_sealed_READY_source_package':manifest_pin,
      'complete_original_SOURCE_members_and_copy_pins':copy_pins,
      'original_metadata_writer':parent_pin,'new_metadata_writer':writer_pin,
      'full_writer_retarged_inverse':proof,
      'full_70runtime_definitions_unchanged':True,'full_original_genuine_host_unchanged':True,
      'all_input_SOURCE_inventory_streams_and_namespace_payload_retained':True,
      'future_business_six_pins_all_None':True,
      'original_caps':{'whole_seconds':1800,'stage_seconds':600,'RSS_MiB':512,
        'joint_H_S_O_T_D_E_and_FACTORY_bytes':2147483648,'history_bytes':96*2**30,
        'free_floor_bytes':8*2**30,'threads':1,'children':1,'retries':0},
      'writer_execution_requires_future_true_Root_terminal_integer_EXIT0_closed_no_session':True,
      'writer_execution_must_follow_actual_genuine_guard_host_PASS_and_full_input_fresh_pin_checks':True,
      'writer_must_be_source_archived_before_D_freeze_and_actual_PREP':True,
      'old_V20_writer_must_not_be_used_for_future_V21_PREP':True,
      'actual_business_success_from_SOURCE_claimed':False,
      'writer_API_guard_business_executed':False,'ART_or_numeric_payload_read':False,
      'canonical_or_frozen_namespace_written':False,'installed':False,
    }
    write_json(binding/'SOURCE_REVIEW.json',report)
    print(json.dumps({'status':report['status'],'metadata_writer':writer_pin,
                      'full_original_package_copied_members':len(original_data),
                      'writer_finite_hunks':len(full_edits),'writer_definition_count':len(old_functions),
                      'checks':len(checks),'blockers':[],
                      'API_guard_business_executed':False,'installed':False}))


if __name__=='__main__':
    main()

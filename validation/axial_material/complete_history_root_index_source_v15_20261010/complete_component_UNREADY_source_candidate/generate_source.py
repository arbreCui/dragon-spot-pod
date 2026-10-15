"""Pure text/AST V15 generation; no import or execution of any factory."""
from pathlib import Path
import ast, difflib, hashlib, json

D=Path(__file__).parent
P=Path('/Users/wen/spot/validation/axial_material')
PARENT=P/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
PARENT_SHA='4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
CANONICAL=P/'prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
RESOURCE=P/'moment_order_complete_history_resource_trie_20261010.py'
RESOURCE_SHA='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'
RESOURCE_PARENT=P/'prepare_qualified_AB_moment_order_production.py'
RESOURCE_PARENT_SHA='fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'
ADMISSION=P/'complete_history_root_index_source_v15_20261010/Root_actual_resource_module_admission.json'

def pin(path):
    before=path.lstat()
    with path.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
    after=path.lstat()
    fields=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    ids=[getattr(before,k) for k in fields]
    assert ids==[getattr(after,k) for k in fields]
    return dict(path=str(path),sha256=digest,size_bytes=before.st_size,identity=ids)

def save(name,value):
    with (D/name).open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')

parent_pin=pin(PARENT);assert parent_pin['sha256']==PARENT_SHA
resource_pin=pin(RESOURCE);assert resource_pin['sha256']==RESOURCE_SHA
resource_parent_pin=pin(RESOURCE_PARENT);assert resource_parent_pin['sha256']==RESOURCE_PARENT_SHA
source=PARENT.read_text();new=source;edits=[]
def change(name,old,value,count=1):
    global new
    assert new.count(old)==count,(name,new.count(old),count)
    new=new.replace(old,value,count)
    edits.append(dict(name=name,old=old,new=value,count=count))

doc=ast.get_source_segment(source,ast.parse(source).body[0])
change('module_documentation',doc,repr('Source-only V15 complete sender component with a normally imported, separately qualified root-index resource module.\nAll original86 mathematical stages, original helper H14b protocol, physics inputs, process MRO and original caps remain intact. Historical ancestors are immutable. Only the current component resource constructor and root validator use the new canonical resource module.\nUNREADY: actual Root resource-module admission SHA remains unknown. No declaration, build, controls, native/AAA/ABA qualification is granted by this source draft.'))
for old,value in [
 ('axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-admission-v14b-20261010','axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'),
 ('axial-material-sender-contiguous-flux-window-streaming-sha-build-v14b-20261010','axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'),
 ('axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-terminal-v14b-20261010','axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010')]:
    change('exclusive_root_'+str(len(edits)),old,value)
identities=[
 'SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_V14B',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V14B',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_SOURCE_ADMISSION_V14B',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_DECLARATION_V14B',
 'DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ONLY_V14B',
 'PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14B',
 'FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_NO_RETRY_V14B',
 'COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14B',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_SEAL_V14B',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V14B',
 'SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_RUNTIME_INPUT_ONLY_V14B',
]
for i,value in enumerate(identities):
    change('current_component_identity_'+str(i),value,value.replace('STREAMING_SHA','ROOT_INDEX').replace('V14B','V15'),new.count(value))
change('unready_status_assignment',"SOURCE_STATUS = 'READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_STREAMING_SHA_COMPONENT_EXECUTION_V14B'", "SOURCE_STATUS = 'SOURCE_ONLY_UNREADY_PENDING_ROOT_RESOURCE_MODULE_ADMISSION_V15'")
change('ready_status_guard', 'SOURCE_STATUS != "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_STREAMING_SHA_COMPONENT_EXECUTION_V14B"', 'SOURCE_STATUS != "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_ROOT_INDEX_COMPONENT_EXECUTION_V15"')
change('formal_current_factory_path','FORMAL_STREAM_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py"',
       'FORMAL_STREAM_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py"')
constant_block='''ROOT_INDEX_RESOURCE_MODULE = ROOT / "validation/axial_material/moment_order_complete_history_resource_trie_20261010.py"
ROOT_INDEX_RESOURCE_MODULE_SHA = "ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022"
ROOT_INDEX_RESOURCE_SOURCE_PARENT = ROOT / "validation/axial_material/prepare_qualified_AB_moment_order_production.py"
ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA = "fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41"
ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION = ROOT / "validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_resource_module_admission.json"
ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA = None

'''
change('resource_identity_constants','FUTURE_ACTUAL_BUILD_TERMINAL_SHA = None\n',constant_block+'FUTURE_ACTUAL_BUILD_TERMINAL_SHA = None\n')
change('resource_pin_unready_guard','        raise ValueError("TMP source-only V14b draft is not the formal component factory")\n',
       '        raise ValueError("TMP source-only V15 draft is not the formal component factory")\n'
       '    for value in (ROOT_INDEX_RESOURCE_MODULE_SHA, ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA, ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA):\n'
       '        if not isinstance(value, str) or re.fullmatch("[0-9a-f]{64}", value) is None or value == "0"*64:\n'
       '            raise ValueError("actual separately qualified root-index resource module pins remain unknown")\n')

added_functions='''def root_index_resource_source_admission():
    """Read the Root-qualified resource-only envelope and every full pinned input."""
    if (not isinstance(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA, str)
            or re.fullmatch('[0-9a-f]{64}', ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA) is None
            or ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA == '0'*64):
        raise ValueError('UNREADY: genuine resource-module admission pin is unknown')
    module_pin = dict(path=str(require(ROOT_INDEX_RESOURCE_MODULE, ROOT_INDEX_RESOURCE_MODULE_SHA)),
        sha256=ROOT_INDEX_RESOURCE_MODULE_SHA)
    parent_pin = dict(path=str(require(ROOT_INDEX_RESOURCE_SOURCE_PARENT, ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA)),
        sha256=ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA)
    admission_pin = dict(path=str(require(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION, ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA)),
        sha256=ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA)
    value = read(admission_pin['path'])
    caps = dict(history_bytes=96*2**30, free_floor_bytes=8*2**30, host_wall_seconds=120,
        rss_mib=512, archive_bytes=64*2**20, threads=1, children=1, retries=0)
    if (value['schema'] != 'AXMAT_COMPLETE_HISTORY_ROOT_INDEX_RESOURCE_MODULE_ADMISSION_V15'
            or value['status'] != 'PASS_RESOURCE_MODULE_ONLY'
            or value['canonical_resource_module'] != module_pin or value['source_parent'] != parent_pin
            or type(value['qualified_caps']) is not dict or set(value['qualified_caps']) != set(caps)
            or any(type(value['qualified_caps'][key]) is not int or value['qualified_caps'][key] != expected
                   for key, expected in caps.items())
            or any(value[key] is not True for key in ('original_resource_class_check_init_MRO_source_unchanged',
                'no_old_module_or_class_monkeypatch', 'fresh_complete_history_checks'))
            or any(value[key] is not False for key in ('full86_component_qualified',
                'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted'))):
        raise ValueError('complete resource-only qualification with unchanged original caps and source required')
    files = value['full_input_pins']
    if type(files) is not list or not files:
        raise ValueError('complete resource qualification input pins required')
    expected = {}
    for row in files:
        if (type(row) is not dict or set(row) != {'path','sha256','size_bytes','identity'}
                or type(row['path']) is not str or not Path(row['path']).is_absolute() or '..' in Path(row['path']).parts
                or type(row['sha256']) is not str or re.fullmatch('[0-9a-f]{64}', row['sha256']) is None
                or row['sha256'] == '0'*64 or type(row['size_bytes']) is not int or row['size_bytes'] < 0
                or type(row['identity']) is not list or len(row['identity']) != 7
                or any(type(word) is not int for word in row['identity']) or row['identity'][4] != row['size_bytes']
                or row['path'] in expected):
            raise ValueError('typed distinct full resource qualification literal pins required')
        path = Path(row['path']); before = path.lstat()
        observed = [before.st_dev,before.st_ino,before.st_mode,before.st_nlink,before.st_size,before.st_mtime_ns,before.st_ctime_ns]
        if not stat.S_ISREG(before.st_mode) or observed != row['identity']:
            raise ValueError('resource qualification input full identity differs')
        require(path, row['sha256'])
        after = path.lstat()
        if [after.st_dev,after.st_ino,after.st_mode,after.st_nlink,after.st_size,after.st_mtime_ns,after.st_ctime_ns] != observed:
            raise ValueError('resource qualification input changed during full SHA read')
        expected[row['path']] = row['sha256']
    for key in ('Root_actual_terminal','actual_host_result','actual_control_result'):
        item = value[key]
        if (type(item) is not dict or set(item) != {'path','sha256'}
                or expected.get(item['path']) != item['sha256']):
            raise ValueError('actual Root/host/control document must belong to complete resource input ownership')
    if any(expected.get(item['path']) != item['sha256'] for item in (module_pin,parent_pin)):
        raise ValueError('original and new genuine resource modules must have complete input ownership')
    terminal = read(value['Root_actual_terminal']['path'])
    if type(terminal['terminal_result']['exit_code']) is not int or terminal['terminal_result']['exit_code'] != 0 or terminal['session_closed'] is not True:
        raise ValueError('actual integer0 closed Root resource comparison receipt required')
    # No self-pin cycle: the external frozen admission is added only after its
    # own independently sealed complete input list has been verified.
    if admission_pin['path'] in expected:
        raise ValueError('resource qualification admission may not contain a self-pinning cycle')
    expected[admission_pin['path']] = admission_pin['sha256']
    return dict(schema='AXMAT_ROOT_INDEX_RESOURCE_SOURCE_ADMISSION_V15',
        actual_resource_module_admission=admission_pin, complete_actual_resource_module_admission=value,
        actual_resource_class_factory=dict(path=module_pin['path'], sha256=module_pin['sha256'],
            class_name='DynamicHistoryResources', genuine_class_not_overlay=True),
        original_factory_ancestry_descriptor=dict(path=parent_pin['path'], sha256=parent_pin['sha256'],
            class_name='DynamicHistoryResources', genuine_class_not_overlay=True),
        source_inputs=expected, resource_module_only=True, full86_component_qualified=False,
        native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def root_index_resource_factory():
    """Normally import the qualified immutable new source; no old-module patch."""
    if (not isinstance(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA, str)
            or re.fullmatch('[0-9a-f]{64}', ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA) is None
            or ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA == '0'*64):
        raise ValueError('UNREADY: root-index resource module lacks actual qualification')
    require(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION, ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA)
    return load(require(ROOT_INDEX_RESOURCE_MODULE, ROOT_INDEX_RESOURCE_MODULE_SHA),
        'sender_root_index_actual_resource_module_v15')


'''
change('two_resource_source_functions','def validate_history_roots(values, artifacts_root):\n    return parent_factory().validate_history_roots(values, artifacts_root)\n',
       added_functions+'def validate_history_roots(values, artifacts_root):\n    return root_index_resource_factory().validate_history_roots(values, artifacts_root)\n')
change('genuine_resource_constructor_redirect','    return parent_factory().DynamicHistoryResources(\n        artifacts_root, roots, min_free_bytes, max_bytes, failure_type)\n',
       '    return root_index_resource_factory().DynamicHistoryResources(\n        artifacts_root, roots, min_free_bytes, max_bytes, failure_type)\n')
change('complete_resource_INPUT_owner_union','    for path,wanted in expected.items():\n        require(path,wanted)\n    old = read(require(PARENT / "declaration.json"))\n',
       '    root_index_admission = root_index_resource_source_admission()\n'
       '    for path, wanted in root_index_admission["source_inputs"].items():\n'
       '        existing = expected.get(path, expected.get(Path(path)))\n'
       '        if existing is not None and existing != wanted:\n'
       '            raise ValueError("whole root-index resource INPUT owner conflict")\n'
       '        expected[path] = wanted\n'
       '    for path,wanted in expected.items():\n        require(path,wanted)\n    old = read(require(PARENT / "declaration.json"))\n')
change('prepare_resource_admission_read','    old,originals=source_inputs(); changed,c=patch_admission(patch_sha,controls_sha)\n',
       '    old,originals=source_inputs(); changed,c=patch_admission(patch_sha,controls_sha)\n'
       '    root_index_admission = root_index_resource_source_admission()\n')
change('SOURCE_resource_admission_envelope','        stream_environment_helper_admission=stream_admission,\n        full_component_factory_source_parent=',
       '        stream_environment_helper_admission=stream_admission,\n'
       '        root_index_resource_source_admission=root_index_admission,\n        full_component_factory_source_parent=')
change('declaration_resource_admission_envelope','        files=files,build_commands=commands,production_link_command=commands[2],\n',
       '        files=files,build_commands=commands,production_link_command=commands[2],\n'
       '        root_index_resource_source_admission=root_index_admission,\n')
change('declaration_actual_resource_input_recheck','    if d["stream_environment_helper_admission"] != stream_admission:\n',
       '    root_index_admission = root_index_resource_source_admission()\n'
       '    if d["root_index_resource_source_admission"] != root_index_admission:\n'
       '        raise ValueError("whole actual resource-module qualification changed")\n'
       '    for path, wanted in root_index_admission["source_inputs"].items():\n'
       '        if d["files"].get(path) != wanted:\n'
       '            raise ValueError("complete resource qualification INPUT ownership missing")\n'
       '    if d["stream_environment_helper_admission"] != stream_admission:\n')
change('SOURCE_actual_resource_envelope_recheck','            or source_admission["stream_environment_helper_admission"] != stream_admission):\n',
       '            or source_admission["stream_environment_helper_admission"] != stream_admission\n'
       '            or source_admission["root_index_resource_source_admission"] != root_index_admission):\n')
change('truthful_current_and_original_resource_descriptors','        actual_resource_class_factory=dict(path=str(parent_factory().PARENT_FACTORY), sha256=parent_factory().PARENT_FACTORY_SHA,\n            class_name="DynamicHistoryResources", genuine_class_not_overlay=True),\n',
       '        actual_resource_class_factory=dict(path=str(ROOT_INDEX_RESOURCE_MODULE), sha256=ROOT_INDEX_RESOURCE_MODULE_SHA,\n'
       '            class_name="DynamicHistoryResources", genuine_class_not_overlay=True),\n'
       '        original_factory_ancestry_descriptor=dict(path=str(parent_factory().PARENT_FACTORY), sha256=parent_factory().PARENT_FACTORY_SHA,\n'
       '            class_name="DynamicHistoryResources", genuine_class_not_overlay=True),\n'
       '        root_index_resource_source_admission=d["root_index_resource_source_admission"],\n')

candidate=D/CANONICAL.name
if candidate.exists():
    assert candidate.read_text()==new  # Preserve immutable first generated bytes.
else:
    with candidate.open('x') as stream:stream.write(new)
back=new
for edit in reversed(edits):
    assert back.count(edit['new'])==edit['count'],edit['name']
    back=back.replace(edit['new'],edit['old'],edit['count'])
assert back==source and hashlib.sha256(back.encode()).hexdigest()==PARENT_SHA
old_tree=ast.parse(source);new_tree=ast.parse(new)
def scopes(text,tree):
    result={}
    def visit(node,parents):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            key=(*parents,node.name);assert key not in result
            result[key]=ast.get_source_segment(text,node);parents=key
        for child in ast.iter_child_nodes(node):visit(child,parents)
    visit(tree,());return result
old_defs=scopes(source,old_tree);new_defs=scopes(new,new_tree)
assert set(old_defs)<=set(new_defs)
changed=['.'.join(k) for k,v in old_defs.items() if new_defs[k]!=v]
same=['.'.join(k) for k,v in old_defs.items() if new_defs[k]==v]
added=['.'.join(k) for k in new_defs if k not in old_defs]
for name in ['parent_factory','helper','resource_scope_contract','history_roots','resources_for','control_audit','archive_forecast','stage_labels','stage_commands','terminal_contract','predecessor_admission','memory_predecessor_admission','stream_environment_helper','stream_environment_helper_source_admission','sender_source_admission','sender_control_contract','patch_admission','production_cache_shape_forecast']:
    assert old_defs[(name,)]==new_defs[(name,)],name
assignments=lambda t:{target.id:ast.get_source_segment(new if t is new_tree else source,node) for node in t.body if isinstance(node,ast.Assign) for root_target in node.targets for target in ast.walk(root_target) if isinstance(target,ast.Name)}
oa=assignments(old_tree);na=assignments(new_tree)
for name in ['PARENT_FACTORY','PARENT_FACTORY_SHA','TOTAL_WALL','STAGE_WALL','RSS_CAP','ARCHIVE_RESERVE','HISTORY_CAP','FREE_FLOOR','ORIGINAL_STAGE_COUNT','COMPLETE_STAGE_COUNT','STREAM_ENVIRONMENT_HELPER','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','SENDER_CONTROL_LAYOUT','SENDER_MODES','SENDER_CASES']:
    assert oa[name]==na[name],name
for name in ['FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA','ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA']:
    assert na[name].endswith(' = None'),name
assert 'SOURCE_ONLY_UNREADY_PENDING_ROOT_RESOURCE_MODULE_ADMISSION_V15' in na['SOURCE_STATUS']
proof=dict(schema='AXMAT_V15_ROOT_INDEX_FULL_COMPONENT_SOURCE_INVERSE_V1',status='SOURCE_ONLY_UNREADY',
    parent=parent_pin,candidate=pin(candidate),edits=edits,complete_byte_inverse_exact=True,
    original_function_class_segments=len(old_defs),byteexact_original_segments=same,modified_original_segments=changed,
    added_segments=added,untouched_original_resource_scope_history_helpers_and_math=True,
    no_class_definition_or_MRO_change=True,normal_pinned_new_resource_load_only=True,
    old_parent_ancestry_references_unchanged=True,old86_controls_plus12_buildplan_and92_original_link_recipe_preserved=True,
    no_business_module_import_or_execution=True)
save('source_inverse_proof.json',proof)
with (D/'minimal_full_component.patch').open('x') as stream:
    stream.write(''.join(difflib.unified_diff(source.splitlines(True),new.splitlines(True),fromfile=str(PARENT),tofile=str(CANONICAL))))
assert pin(PARENT)==parent_pin and pin(RESOURCE)==resource_pin and pin(RESOURCE_PARENT)==resource_parent_pin
report=dict(schema='AXMAT_V15_ROOT_INDEX_FULL_COMPONENT_SOURCE_ONLY_REPORT_V1',status='SOURCE_ONLY_UNREADY',
    candidate=pin(candidate),prospective_canonical_path=str(CANONICAL),parent=parent_pin,
    new_resource_module=resource_pin,original_resource_ancestor=resource_parent_pin,
    actual_resource_admission=dict(path=str(ADMISSION),sha256=None,actual_terminal_and_host_control_values_not_invented=True),
    source_inverse_proof=pin(D/'source_inverse_proof.json'),region_count=len(edits),modified_original_segments=changed,
    byteexact_original_segment_count=len(same),original_segment_count=len(old_defs),added_segments=added,
    future_build_seal_terminal_and_native_None=True,source_status_UNREADY=True,
    preserved=dict(whole_original86=True,build_commands12=True,production_original_recipe92=True,realSPOT_kernel2710=True,
        observer_stub_calls48_separate=True,original_math_and_FP_source=True,old68_control_audit_and_archive_forecast=True,
        original_helpers_H7d_proof1809_qualification16d=True,parent_ancestry=True,OwnRSS_source_and_MRO=True,
        caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0)),
    resource_gate_interface=dict(schema='AXMAT_COMPLETE_HISTORY_ROOT_INDEX_RESOURCE_MODULE_ADMISSION_V15',status='PASS_RESOURCE_MODULE_ONLY',
        source_module_and_parent_exact_known_pins=True,qualified_caps_exact_types_and_values=True,
        full_input_pins_exact_path_SHA_size_7identities_and_no_duplicate_no_selfcycle=True,
        actualRoot_host_control_documents_must_have_full_input_owners=True,
        actualRoot_terminal_result_requires_typeint0_and_sessionclosed=True,
        complete_root_only_admission_envelope_and_allowners_propagated_into_SOURCE_declaration_INPUT=True,
        normal_newmodule_import_unique_name='sender_root_index_actual_resource_module_v15',
        only_current_constructor_and_validator_redirected=True,history_roots_resource_scope_contract_old_chain_byteexact=True),
    pending=['Root real resource-module comparison/control qualification SHA must be bound and source-reviewed',
        'Actual admission uses Root_actual_terminal.terminal_result.exit_code and session_closed; if Root chooses different field names, retarget these two receipt accessors by exact source-only edit before READY',
        'Root converts source status only after formal admission and complete source review; no inherited build or native success',
        'No extra resource-module copies are added to SOURCE; full original metadata allowance and actual2GiB archive cap remain. Future preparation must account for the full newly embedded small admission under that unchanged cap'],
    project_written=False,business_imported_or_called=False,controls_compiler_fixture_called=False,
    Root_process_polled=False,actual_full_prepare_or_check_success=False,full86_native_AAA_ABA_credit=False,
    retained_generation_checker_failure=dict(chunk='7ce09f',exit_code=1,closed=True,
        reason='Pure source checker initially omitted tuple-assignment names TOTAL_WALL/STAGE_WALL/RSS_CAP; corrected AST inventory only. First generated candidate bytes preserved unchanged.'))
save('REPORT.json',report)
with (D/'REPORT.txt').open('x') as stream:
    stream.write('V15完整UNREADY源码已从冻结4f工厂生成。新唯一canonical路径、三新root和当前component schema/分类改为root-index-v15；H7d/1809/16d、旧parent ancestry、全部86/12build/原92linkrecipe、68control数学和原预算保持。\n仅当前validator与DynamicHistoryResources正常构造委托新canonical ebbb模块；resource_scope_contract/history_roots/旧parent_factory走原冻结链。actual_resource_class_factory如实新源，另保留original_factory_ancestry_descriptor。没有旧模块global/class monkeypatch。\n正式resource admission SHA未知None，require_ready先拒绝；后续完整门逐份fullSHA/size/7ID验证全部inputpins及Root/host/control所有权、typed整数0/closed、原caps和sciencefalse，将完整新证明与源owner图加入SOURCE及declaration。\n没有业务导入/执行、编译、fixture或项目写；当前仅源码未授真实资源check、full86/native/AAA/ABA资格。\n')
print(json.dumps(dict(status=report['status'],candidate=pin(candidate),REPORT=pin(D/'REPORT.json'),proof=pin(D/'source_inverse_proof.json'),
    regions=len(edits),olddefs=len(old_defs),exactdefs=len(same),modifieddefs=changed,addeddefs=added),indent=2))

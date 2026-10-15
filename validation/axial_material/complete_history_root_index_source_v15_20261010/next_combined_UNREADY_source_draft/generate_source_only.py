import ast
import hashlib
import json
import os
from pathlib import Path

D=Path('/private/tmp/axmat_v15_sender_window_root_index_graph_table_combined_source_only_20261010')
B=Path('/private/tmp/axmat_v13_sender_window_graph_table_combined_source_draft_20261009/prepare_sender_window_graph_table_combined_runtime_v13.py')
V12=Path('/Users/wen/spot/validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py')
V15=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py')
BLUEPRINT_PROOF=B.parent/'source_complete_inverse_proof.json'

def pin(p):
    p=Path(p);s=p.lstat();data=p.read_bytes();after=p.lstat()
    identity=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
    assert identity(s)==identity(after)
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(after))

def write(name,data):
    p=D/name
    with p.open('x') as f:
        if isinstance(data,str):f.write(data)
        else:json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    return pin(p)

before={str(p):pin(p) for p in (B,V12,V15,BLUEPRINT_PROOF)}
assert before[str(B)]['sha256']=='c0644107311d63703d323ad210e32064ad9f4dd5f0517e4db49aa3a072c4f327'
assert before[str(V12)]['sha256']=='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
assert before[str(V15)]['sha256']=='cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447'
base=B.read_text();actual=V15.read_text();s=base;regions=[]
v15tree=ast.parse(actual)
def definition(source,name):
    nodes=[n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
    assert len(nodes)==1,name
    return ast.get_source_segment(source,nodes[0])
def edit(name,old,new,count=1):
    global s
    assert old!=new and s.count(old)==count,(name,s.count(old),count)
    s=s.replace(old,new,count)
    regions.append(dict(name=name,before=old,after=new,count=count))
def function_edit(name,transform):
    old=definition(s,name);new=transform(old)
    edit('function_'+name,old,new)
def assignment(name,new):
    nodes=[n for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    assert len(nodes)==1,name
    edit('constant_'+name,ast.get_source_segment(s,nodes[0]),name+' = '+new)

doc=ast.get_source_segment(s,ast.parse(s).body[0])
edit('module_doc',doc,repr('UNREADY source-only V15 sender/root-index graph-table combined runtime. New actual V15 complete86 component success and seven component pins are compulsory before any action. Entire original68 cache scope and14 sender controls remain independent. Normal qualified root-index resources replace only the current resource constructor/validator; original builder, genuine OwnRSS class/MRO, inherited history policy and caps remain intact. Complete seven historical INPUT bodies, all literal owners/aliases/namespaces/absence/read traces and e8 lossless graph storage remain required. No component/combined/native/AAA/ABA success is claimed.'))
identity={
 'SOURCE':"ART/'axial-material-qualified-AB-sender-window-root-index-graph-table-combined-source-v15-20261010'",
 'OUT':"ART/'axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010'",
 'TERMINAL':"ART/'axial-material-qualified-AB-sender-window-root-index-graph-table-combined-terminal-v15-20261010'",
 'FAMILY':repr('SENDER_WINDOW_ROOT_INDEX_GRAPH_TABLE_COMBINED_RUNTIME_LINK_V15'),
 'PREFIX':repr('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TABLE_COMBINED_RUNTIME_V15'),
 'FORMAL_FACTORY':"ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py'",
 'DRAFT_STATUS':repr('UNREADY_SOURCE_ONLY_REQUIRES_ACTUAL_V15_COMPLETE86_AND_NEW_COMBINED_QUALIFICATION'),
 'TRIM_FACTORY':"ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'",
 'TRIM_FACTORY_SHA':repr(before[str(V15)]['sha256']),
 'TRIM_SOURCE':"ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'",
 'TRIM':"ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'",
 'TRIM_TERMINAL':"ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'",
 'TRIM_SCHEMA':repr('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15'),
 'TRIM_ADMISSION':repr('SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_RUNTIME_INPUT_ONLY_V15')}
for key,value in identity.items():assignment(key,value)

constants=[]
for node in v15tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and (t.id.startswith('STREAM_ENVIRONMENT_') or t.id.startswith('ROOT_INDEX_')) for t in node.targets):
        constants.append(ast.get_source_segment(actual,node))
new_constants='\n'.join(constants)+'''\nFUTURE_ACTUAL_COMBINED_DECLARATION_SHA = None
FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA = None
FUTURE_ACTUAL_COMBINED_SEAL_SHA = None
FUTURE_ACTUAL_COMBINED_TERMINAL_SHA = None
FUTURE_ACTUAL_COMBINED_RUNTIME_SHA = None
FUTURE_ACTUAL_NATIVE_TERMINAL_SHA = None
'''
edit('new_fixed_helper_resource_and_future_constants',"TRIM_INPUT_NAME = 'trim_component_admission_INPUT.json'",new_constants+"\nTRIM_INPUT_NAME = 'trim_component_admission_INPUT.json'")
function_edit('require_ready',lambda old:old.replace('READY_REVIEWED_SENDER_WINDOW_COMPONENT_INPUT_REUSE_FORMAL_FACTORY','READY_REVIEWED_V15_ROOT_INDEX_SENDER_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'))

# These complete source-reading gates are copied byteexact from the frozen V15
# component. They are not imported, executed, simplified, or reimplemented.
stream_gate=definition(actual,'stream_environment_helper_source_admission')
resource_gate=definition(actual,'root_index_resource_source_admission')
factory='''def root_index_resource_factory():
    """Normally load the qualified immutable resource module; no overlay."""
    require_ready()
    require(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION, nonzero_sha(ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA))
    return load(ROOT_INDEX_RESOURCE_MODULE, ROOT_INDEX_RESOURCE_MODULE_SHA,
        'combined_v15_actual_root_index_resource_module')'''
support='''def component_support_contract(value, d, admission, audit=None, result=None):
    """Entire helper/resource SOURCE qualification, never component success credit."""
    stream = stream_environment_helper_source_admission()
    resource = root_index_resource_source_admission()
    for body in (value, d, admission):
        if (body['stream_environment_helper_admission'] != stream
                or body['root_index_resource_source_admission'] != resource):
            raise ValueError('whole immutable helper/resource component INPUT bodies differ')
    for body in (audit, result):
        if body is not None and body['stream_environment_helper_admission'] != stream:
            raise ValueError('sealed audit/result must retain the entire helper admission')
    if (value['actual_resource_class_factory'] != resource['actual_resource_class_factory']
            or value['original_factory_ancestry_descriptor'] != resource['original_factory_ancestry_descriptor']):
        raise ValueError('new genuine resource factory and old ancestry descriptors must remain distinct')
    if not 0 < d['complete_archive_forecast']['forecast_complete_with_sender_and_stream_helper_bytes'] < RESERVE:
        raise ValueError('whole V15 component forecast must retain unchanged2GiB bound')
    sources = {}
    merge_expected(sources, stream['source_inputs'])
    merge_expected(sources, resource['source_inputs'])
    for path, wanted in sources.items():
        if d['files'].get(path) != wanted:
            raise ValueError('every helper/resource ancestor literal requires complete component ownership')
    for original_path, copied_name, wanted in (
            (STREAM_ENVIRONMENT_HELPER, 'complete_environment_streaming_sha_helper_v14b.py', STREAM_ENVIRONMENT_HELPER_SHA),
            (STREAM_ENVIRONMENT_SOURCE_PROOF, 'stream_environment_helper_source_patch_proof.json', STREAM_ENVIRONMENT_SOURCE_PROOF_SHA),
            (STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS, 'stream_environment_helper_controls_admission.json', STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA)):
        if (d['source_inventory']['files'].get(copied_name) != wanted
                or require(TRIM_SOURCE/copied_name, wanted).read_bytes() != require(original_path, wanted).read_bytes()):
            raise ValueError('whole copied helper SOURCE documents differ; copies are never imported')
        merge_expected(sources, {str(TRIM_SOURCE/copied_name): wanted})
    return dict(stream=stream, resource=resource, files=sources,
        owners=[dict(owner='ACTUAL_COMPLETE_HELPER_PROTOCOL_AND_ALL_SOURCE_ANCESTORS_V15',
            category='code_environment', expected_files=dict(stream['source_inputs'])),
            dict(owner='ACTUAL_COMPLETE_ROOT_INDEX_RESOURCE_AND_ALL_SOURCE_ANCESTORS_V15',
            category='code_environment', expected_files=dict(resource['source_inputs']))])'''
insertion='\n\n'.join((stream_gate,resource_gate,factory,support))+'\n\n\n'
edit('complete_fixed_gates_and_normal_resource_loader',definition(s,'DynamicHistoryResources'),insertion+'''def DynamicHistoryResources(art,roots,free,cap,failure_type=None):
    return root_index_resource_factory().DynamicHistoryResources(art,roots,free,cap,failure_type)''')
function_edit('resources_for',lambda old:old.replace('b=builder();values=[str(p) for p in b.validate_history_roots(roots,ART)]','values=[str(p) for p in root_index_resource_factory().validate_history_roots(roots,ART)]'))

component_strings={
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_SEAL_V13':'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_SEAL_V15',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_PRODUCTION_RUNTIME_INPUT_ADMISSION_V13':'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15',
 'SENDER_CONTIGUOUS_FLUX_WINDOW_RUNTIME_INPUT_ONLY_V13':'SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_RUNTIME_INPUT_ONLY_V15',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_DECLARATION_V13':'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_DECLARATION_V15',
 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_SOURCE_ADMISSION_V13':'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_SOURCE_ADMISSION_V15',
 'SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13':'SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_V15',
 'PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY':'PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_CONTROLS_ONLY_V15',
 'COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY':'COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_CONTROLS_ONLY_V15'}
def component_retarget(old):
    for before_value,after_value in component_strings.items():old=old.replace(repr(before_value),repr(after_value))
    return old
function_edit('sender_component_contract',component_retarget)
def trim_contract(old):
    old=component_retarget(old)
    needle='    sender_component_contract(value,d,admission,controls,audit,result,sealed)'
    assert old.count(needle)==1
    old=old.replace(needle,needle+'\n    support=component_support_contract(value,d,admission,audit,result)')
    old+='\n    return support'
    return old
function_edit('trim_component_contract',trim_contract)
def trim_input(old):
    old=component_retarget(old)
    old=old.replace('    trim_component_contract(value,d,admission)','    support=trim_component_contract(value,d,admission)',1)
    old=old.replace('    rows=[]','    merge_expected(files,support[\'files\'])\n    rows=[]',1)
    old=old.replace('    del value,d,seal,admission;gc.collect()','    support_owners=support[\'owners\']\n    del value,d,seal,admission,support;gc.collect()',1)
    old=old.replace('return dict(files=files,namespaces=rows,binding=binding)','return dict(files=files,namespaces=rows,binding=binding,support_owners=support_owners)',1)
    return old
function_edit('trim_component_input',trim_input)

def prepare(old):
    old=old.replace('b.validate_history_roots(b.history_roots(sorted(declared),ART),ART)','root_index_resource_factory().validate_history_roots(b.history_roots(sorted(declared),ART),ART)',1)
    old=old.replace('resource_roots=roots,resource_scope_contract=b.resource_scope_contract(),resource_scope_policy=HISTORY_POLICY,',
        'resource_roots=roots,resource_scope_contract=b.resource_scope_contract(),resource_scope_policy=HISTORY_POLICY,\n        actual_resource_class_factory=dict(path=str(ROOT_INDEX_RESOURCE_MODULE),sha256=ROOT_INDEX_RESOURCE_MODULE_SHA,class_name=\'DynamicHistoryResources\',genuine_class_not_overlay=True),\n        original_factory_ancestry_descriptor=dict(path=str(ROOT_INDEX_RESOURCE_SOURCE_PARENT),sha256=ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA,class_name=\'DynamicHistoryResources\',genuine_class_not_overlay=True),',1)
    return old
function_edit('prepare_build',prepare)
def declaration(old):
    needle="        or d['historical_whole_component_body']!=BODY_BINDING or d['historical_failed_combined_RUN_promoted']is not False"
    assert needle in old
    return old.replace(needle,needle+"\n        or d['actual_resource_class_factory']!=dict(path=str(ROOT_INDEX_RESOURCE_MODULE),sha256=ROOT_INDEX_RESOURCE_MODULE_SHA,class_name='DynamicHistoryResources',genuine_class_not_overlay=True)\n        or d['original_factory_ancestry_descriptor']!=dict(path=str(ROOT_INDEX_RESOURCE_SOURCE_PARENT),sha256=ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA,class_name='DynamicHistoryResources',genuine_class_not_overlay=True)",1)
function_edit('declaration_admission',declaration)
function_edit('external_terminal',lambda old:old.replace("builder().validate_history_roots(s['resource_roots'],ART)","root_index_resource_factory().validate_history_roots(s['resource_roots'],ART)",1))
function_edit('production_admission',lambda old:old.replace("actual_resource_class_factory=bodies['dedup']['actual_resource_class_factory'],", "actual_resource_class_factory=d['actual_resource_class_factory'],\n        original_factory_ancestry_descriptor=d['original_factory_ancestry_descriptor'],\n        stream_environment_helper_admission=trim_body['stream_environment_helper_admission'],\n        root_index_resource_source_admission=trim_body['root_index_resource_source_admission'],",1))
def graph(old):
    old=old.replace('builder().validate_history_roots(roots,ART)','root_index_resource_factory().validate_history_roots(roots,ART)',1)
    old=old.replace("dict(owner='ACTUAL_COMPLETE_TRIM_COMPONENT_INPUT',category='component_ancestry',expected_files=trim['files'])])", "dict(owner='ACTUAL_COMPLETE_TRIM_COMPONENT_INPUT',category='component_ancestry',expected_files=trim['files']),*trim['support_owners']])",1)
    return old
function_edit('create_complete_input_graph',graph)
def current_paths(old):
    needle='    normal(SOURCE);normal(OUT)'
    addition="""    # Recheck the original complete helper/resource namespaces, including
    # deliberate invalid fixture aliases that are not numerical native aliases.
    td=read(require(TRIM/'declaration.json',TRIM_DECL_SHA))
    ta=read(require(TRIM_SOURCE/'source_admission.json',TRIM_SOURCE_ADMISSION_SHA))
    tv=read(require(SOURCE/TRIM_INPUT_NAME,d['actual_last_cprime_trim_component_INPUT']['sha256']))
    support=component_support_contract(tv,td,ta)
    for path,wanted in support['files'].items():
        if d['files'].get(path)!=wanted:
            raise ValueError('whole graph must retain every helper/resource expected literal owner')
    del td,ta,tv,support;gc.collect()
"""
    assert old.count(needle)==1
    return old.replace(needle,needle+'\n'+addition,1)
function_edit('current_new_owned_paths',current_paths)

# Full byte inverses, not AST-normalized approximations.
inverse=s
for row in reversed(regions):
    assert inverse.count(row['after'])==row['count'],row['name']
    inverse=inverse.replace(row['after'],row['before'],row['count'])
assert inverse==base
blueprint=json.loads(BLUEPRINT_PROOF.read_text())
back_to_v12=inverse
for row in reversed(blueprint['regions']):
    assert back_to_v12.count(row['after'])==row['count'],row['name']
    back_to_v12=back_to_v12.replace(row['after'],row['before'],row['count'])
assert back_to_v12==V12.read_text()

def scope(source):
    out={}
    def walk(n,parents=()):
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
            key='/'.join((*parents,n.name));assert key not in out
            out[key]=ast.get_source_segment(source,n);parents=(*parents,n.name)
        for child in ast.iter_child_nodes(n):walk(child,parents)
    walk(ast.parse(source));return out
oldscope=scope(base);newscope=scope(s)
modified=[key for key in oldscope if oldscope[key]!=newscope[key]]
added=sorted(set(newscope)-set(oldscope))
protected=['strict_json_bytes','combined_link_command','component_contract','actual_components',
 'record_actual_trim_component','graph_input_bindings','original_prep_input','minimal_live_specs',
 'current_input_predicates','complete_input_phase','failed_prepare_input','check_failed_prepare_phase',
 'stage_labels','stage_commands','check_watch','binary_audit','audit_build','run_build',
 'modules','supervisor_constructor_preflight','expected_supervisor_constructor']
for name in protected:assert definition(s,name)==definition(base,name),name
assert definition(s,'stream_environment_helper_source_admission')==stream_gate
assert definition(s,'root_index_resource_source_admission')==resource_gate
tree=ast.parse(s)
values={t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
future=['TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','SENDER_OBJECT_SHA',
 'FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA',
 'FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assert all(isinstance(values[key],ast.Constant) and values[key].value is None for key in future)
assert 'UNREADY' in ast.literal_eval(values['DRAFT_STATUS'])
for name in ('TOTAL_WALL','STAGE_WALL','RSS','RESERVE','HISTORY_CAP','FREE_FLOOR','THREAD_KEYS','TAIL_FIELDS','INPUT_HELPERS','BODY_BINDING','INPUT_SPECS','INPUT_SPECS_SHA'):
    oldnode=[n for n in ast.parse(base).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for target in n.targets for t in ast.walk(target))]
    newnode=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for target in n.targets for t in ast.walk(target))]
    assert len(oldnode)==len(newnode)==1 and ast.get_source_segment(base,oldnode[0])==ast.get_source_segment(s,newnode[0]),name

roots=[Path('/Users/wen/spot/validation/artifacts')/name for name in (
 'axial-material-qualified-AB-sender-window-root-index-graph-table-combined-source-v15-20261010',
 'axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010',
 'axial-material-qualified-AB-sender-window-root-index-graph-table-combined-terminal-v15-20261010')]
formal=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py')
absences={str(p):not os.path.lexists(p) for p in [formal,*roots]}
assert all(absences.values())
after={p:pin(p) for p in before};assert before==after
candidate=write('prepare_sender_window_root_index_graph_table_combined_runtime_v15.UNREADY.py',s)
proof=write('source_complete_inverse_proof.json',dict(schema='AXMAT_V15_COMBINED_SOURCE_ONLY_COMPLETE_BYTE_INVERSE_V1',
 candidate=candidate,parent=before[str(B)],regions=regions,region_count=len(regions),
 complete_inverse_to_c064_byteexact=True,ancestor_V12=before[str(V12)],c064_to_V12_proof=before[str(BLUEPRINT_PROOF)],
 whole_chain_to_V12_byteexact=True,original_definition_segments=len(oldscope),byteexact_original_segments=len(oldscope)-len(modified),
 modified_original_segments=modified,added_segments=added,all_protected_math_input_stage_and_supervisor_definitions_byteexact=protected,
 exact_copied_component_source_gates=['stream_environment_helper_source_admission','root_index_resource_source_admission']))
report=write('REPORT.json',dict(schema='AXMAT_V15_ROOT_INDEX_COMBINED_SOURCE_ONLY_DRAFT_REVIEW_V1',status='UNREADY_SOURCE_ONLY',
 candidate=candidate,source_inputs_before=before,source_inputs_after=after,source_identity_before_after_equal=True,source_inverse_proof=proof,
 proposed_formal_factory=str(formal),new_roots=list(map(str,roots)),before_namespace_absent=absences,
 actual_component_source=before[str(V15)],actual_component_execution_success_claimed=False,
 future_bindings={key:None for key in future},full_component_requires_actual_86_and_raw_audit_seal_four_tails_and_Root_int0=True,
 original_68_thirty_field_control_counts_retained=True,sender_14_70raw_288241824_and_48stub_separate_from_2710_kernel_calls=True,
 current_resource_constructor_and_validator_normal_new_module=True,
 actual_resource_class_factory='moment_order_complete_history_resource_trie_20261010.py/ebbb',
 original_resource_factory_ancestry='prepare_qualified_AB_moment_order_production.py/fe811',
 complete_fixed_helper_and_resource_gates_copied_byteexact=True,
 complete_helper_and_resource_expected_maps_added_as_distinct_owner_roles=True,
 invalid_fixture_aliases_preserved_and_rechecked_by_original_helper_namespace_gate=True,
 invalid_fixture_aliases_not_reinterpreted_as_native_numerical_aliases=True,
 entire_original_seven_INPUT_e8_strict_two_readers_and_fresh_trace_scope_preserved=True,
 original_5_stage_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
 API_build_regression_transport_started=False,business_imported_or_called=False,fixtures_run=False,Root_polled=False,
 project_written=False,big35GB_rehashed=False,new_component_86_credit=False,new_combined_success_credit=False,native_RSS_credit=False,AAA_credit=False,ABA_credit=False))
write('REPORT.txt','V15 combined 完整 SOURCE-only 草稿已生成，保持 UNREADY。\n'
    '七项真实组件成功 pin +六项未来 combined/native pin 均为 None。完整86+原68数学计数+14 sender 单位观察分域不变。\n'
    '生产三个 object 和原92 link 全序列逆向保持；whole7/e8两严格入口、原5阶段和1800/600/512/2GiB/96/free8原预算保持。\n'
    '完整 helper/resource 源准入函数逐字复制当前 V15，所有来源文件以两独立 owner 角色合入全图。当前资源类 normal load ebbb，旧 fe811 保留祖先描述；无 class/module overlay。\n'
    '故意无效的 helper 测试 symlink 仍由其原完整 namespace 门复核，未伪装成有效数值 native aliases。\n'
    '只生成 TMP 源码及 byte inverse 证据；未业务导入/调用/fixture/编译/项目写/Root轮询，也未获得86/combined/native/AAA/ABA资格。\n')
print(json.dumps(dict(status='UNREADY_SOURCE_ONLY',candidate=candidate,report=report,proof=proof,region_count=len(regions),
 original_segments=len(oldscope),byteexact_original_segments=len(oldscope)-len(modified),modified=modified,added=len(added)),indent=2))

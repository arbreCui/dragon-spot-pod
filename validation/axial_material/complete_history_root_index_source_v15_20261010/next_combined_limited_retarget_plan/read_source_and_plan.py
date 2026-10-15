"""Pure source/AST retarget plan. No module import, metadata API, or fixture."""
from pathlib import Path
import ast, hashlib, json

D=Path(__file__).parent
P=Path('/Users/wen/spot/validation/axial_material')
V12=P/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
V15=P/'prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
V13=Path('/private/tmp/axmat_v13_sender_window_graph_table_combined_source_draft_20261009/prepare_sender_window_graph_table_combined_runtime_v13.py')
V13_PROOF=V13.parent/'source_complete_inverse_proof.json'
GRAPH=P/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'

def pin(path):
    before=path.lstat()
    with path.open('rb') as stream: value=hashlib.file_digest(stream,'sha256').hexdigest()
    after=path.lstat();names=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    ids=[getattr(before,n) for n in names]
    assert ids==[getattr(after,n) for n in names]
    return dict(path=str(path),sha256=value,size_bytes=before.st_size,identity=ids)

def save(name,data):
    with (D/name).open('x') as stream:json.dump(data,stream,indent=2,allow_nan=False);stream.write('\n')

files={str(p):pin(p) for p in [V12,V15,V13,V13_PROOF,GRAPH]}
assert files[str(V12)]['sha256']=='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
assert files[str(V13)]['sha256']=='c0644107311d63703d323ad210e32064ad9f4dd5f0517e4db49aa3a072c4f327'
assert files[str(GRAPH)]['sha256']=='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
sources={str(p):p.read_text() for p in [V12,V15,V13]}
trees={key:ast.parse(value) for key,value in sources.items()}
tops={key:{n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)} for key,tree in trees.items()}
assignments={key:{target.id:node.value for node in tree.body if isinstance(node,ast.Assign) for root in node.targets for target in ast.walk(root) if isinstance(target,ast.Name)} for key,tree in trees.items()}
def constant(path,name):
    def value(node):
        if isinstance(node,ast.Name):return value(assignments[str(path)][node.id])
        if isinstance(node,ast.Attribute) and node.attr=='parent':
            parent=value(node.value);assert isinstance(parent,Path);return parent.parent
        if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):return value(node.left)/value(node.right)
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='Path':return Path(value(node.args[0]))
        return ast.literal_eval(node)
    return value(assignments[str(path)][name])
def fn(path,name):return ast.get_source_segment(sources[str(path)],tops[str(path)][name])
def location(path,name):
    n=tops[str(path)][name];return dict(path=str(path),line=n.lineno,end_line=n.end_lineno,
        complete_function_sha256=hashlib.sha256(fn(path,name).encode()).hexdigest())
assert constant(V15,'FAMILY')=='SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_V15'
assert constant(V15,'ROOT_INDEX_RESOURCE_MODULE_SHA')=='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'
assert constant(V15,'STREAM_ENVIRONMENT_HELPER_SHA')=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
api=tops[str(V15)]['production_admission']
assert [a.arg for a in api.args.args]==['build_seal_sha','terminal_evidence','terminal_evidence_sha256']
last_return=next(n for n in reversed(api.body) if isinstance(n,ast.Return))
assert isinstance(last_return.value,ast.Call) and isinstance(last_return.value.func,ast.Name) and last_return.value.func.id=='dict'
api_fields=[k.arg for k in last_return.value.keywords]
schema=ast.literal_eval(next(k.value for k in last_return.value.keywords if k.arg=='schema'))
admission=ast.literal_eval(next(k.value for k in last_return.value.keywords if k.arg=='admission'))
assert schema=='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15'
assert admission=='SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_RUNTIME_INPUT_ONLY_V15'
proof=json.loads(V13_PROOF.read_text())
# Read the known full32 inverse in its original schema, without trusting the
# peer's PASS text or importing its draft.
edit_key=next(k for k in ('regions','edits','composition_regions') if k in proof)
regions=proof[edit_key]
if isinstance(regions,dict):regions=list(regions.values())
inverse=sources[str(V13)]
for row in reversed(regions):
    old=row.get('old',row.get('before'));new=row.get('new',row.get('after'));count=row.get('count',1)
    assert isinstance(old,str) and isinstance(new,str) and type(count)is int and count>0
    assert inverse.count(new)==count
    inverse=inverse.replace(new,old,count)
assert inverse==sources[str(V12)]
retained=['strict_json_bytes','actual_components','input_modules','original_input_contract',
    'full_original_metadata','record_actual_trim_component','minimal_live_specs']
# Use actual shared names; do not invent a missing predecessor helper scope.
retained=[name for name in retained if name in tops[str(V12)] and name in tops[str(V13)]]
same={name:fn(V12,name)==fn(V13,name) for name in retained}
assert same.get('actual_components') is True and same.get('strict_json_bytes') is True
component_constants={name:(str(value) if isinstance(value,Path) else value) for name in (
    'SOURCE','OUT','TERMINAL','FAMILY','TERMINAL_SCHEMA','SOURCE_STATUS',
    'ROOT_INDEX_RESOURCE_MODULE','ROOT_INDEX_RESOURCE_MODULE_SHA','ROOT_INDEX_RESOURCE_SOURCE_PARENT','ROOT_INDEX_RESOURCE_SOURCE_PARENT_SHA',
    'ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION','ROOT_INDEX_ACTUAL_RESOURCE_ADMISSION_SHA',
    'STREAM_ENVIRONMENT_HELPER','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA',
    'STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA',
    'CANDIDATE_SENDER_SOURCE','CANDIDATE_SENDER_SHA','SENDER_PATCH_HELPER','SENDER_PATCH_HELPER_SHA',
    'SENDER_CONTROL_SOURCE','SENDER_CONTROL_SOURCE_SHA','SENDER_CONTROL_CONTRACT','SENDER_CONTROL_CONTRACT_SHA',
    'SENDER_CONTROLS_AUDITOR','SENDER_CONTROLS_AUDITOR_SHA') for value in [constant(V15,name)]}
success_pins={
 'TRIM_DECL_SHA':dict(path=str(constant(V15,'OUT')/'declaration.json'),sha256=None),
 'TRIM_SEAL_SHA':dict(path=str(constant(V15,'OUT')/'seal.json'),sha256=None),
 'TRIM_TERMINAL_SHA':dict(path=str(constant(V15,'TERMINAL')/'terminal_return.json'),sha256=None),
 'TRIM_SOURCE_ADMISSION_SHA':dict(path=str(constant(V15,'SOURCE')/'source_admission.json'),sha256=None),
 'TRIM_OBJECT_SHA':dict(path=str(constant(V15,'OUT')/'build/SPOT1P64.o'),sha256=None),
 'TRIM_RUNTIME_SHA':dict(path=str(constant(V15,'OUT')/'runtime/Dragon'),sha256=None),
 'SENDER_OBJECT_SHA':dict(path=str(constant(V15,'OUT')/'build/FLU2DR64.o'),sha256=None),
}
retarget=[
 dict(area='new combined identity',functions=['module constants','require_ready','terminal_contract','prepare_terminal_contract'],
   change='New unique canonical factory/SOURCE/OUT/TERMINAL/FAMILY/PREFIX and UNREADY status; retain old V12 and all executions. Root selects exact new combined names. Do not use V15 component terminal schema for combined receipts.'),
 dict(area='seven actual component success pins',functions=['require_ready','trim_factory','trim_component_contract'],
   change='TRIM_FACTORY points to the fresh V15 canonical source/hash; TRIM_SOURCE/TRIM/TRIM_TERMINAL from its actual constants. All seven success pins below remain None until actual86 success, valid audit, seal, four tails, typed Root0 and production_admission independently qualify. Kernel/helper ancestor pins0800/5e/343e remain unchanged.'),
 dict(area='complete86 and source contracts',functions=['trim_component_contract','sender_component_contract blueprint'],
   change='Use new V15 schema/admission/FAMILY/source and seal schemas. Production command index is2, not V12 index1. Full original68 thirty-field count dict remains exact; top86 changes only total_declared_stages. Independently require all14 sender cases, complete70 raw288241824B, 48 wrapper stubcalls separate from2710 realSPOT unit calls. Cross-check full d/SOURCE/result/audit/control return bodies; compatibility labels alone confer no qualification.'),
 dict(area='production three-object link',functions=['combined_link_command','combined_static_binary_checks','prepare_build','declaration_admission','audit_build','production_admission'],
   change='Relative to original92: replace SPOT1P64.o with V15 object, replace inherited FLU2DR64.o with actual V15 sender object, insert physical SPOASM.o beforelibDragon.a, change output only. Entire ordered inverse must restore original92 recipe. Keep original selector object and all flags/lib tokens. Reject unitreference/SPOFobserver/wrappercontrol objects and symbols from production. Use c064 six sender gate helpers as source blueprint only.'),
 dict(area='H14b whole input qualification',functions=['additional pure metadata contract at trim_component_contract boundary','trim_component_input'],
   change='The entire stream_environment_helper_admission body across V15 d/SOURCE/audit/result/return must be exact, with fixed H7d/1809/16d full root inventories, source/control pins and21 protocol qualification only. Keep its actual V14b helper schema and names; do not globally rename genuine ancestors. Actual SOURCE three copied helper documents match fixed originals; include complete owners without filtered metadata.'),
 dict(area='new resource module qualification',functions=['additional pure metadata contract at trim_component_contract boundary','trim_component_input','DynamicHistoryResources','resources_for'],
   change='Verify entire root_index_resource_source_admission from d/SOURCE/return against actual fixed external Root admission5a0b and fullinputSHA/size/7ID/Root0/caps; actualclass ebbb and original fe811 ancestry descriptor are distinct. Merge every additional absolute owner into graph, not a summarized subset. Prefer current combined resource constructor/root validator to normally delegate through the pinned V15 resource module, retaining builder/helper/OwnRSS MRO and old ancestry/history scope. If left on original builder class, truthfully keep olddescriptor and gain no new root-index efficiency.'),
 dict(area='one genuine component API and whole graph',functions=['record_actual_trim_component','trim_read_capture','trim_component_input','create_complete_input_graph','complete_input_phase','graph_input_bindings'],
   change='Call V15 production_admission(sealSHA,terminalAbsolutePath,terminalSHA) exactly once in fresh combined PREP, preserve complete returned body plus read/absence traces. Current reuse phase performs all fresh original checks and full owner/namespace/alias/resource union; no component API replay. Use unchanged e8 strict two-reader canonical-table storage; preserve every7 INPUT field, old failurePREP owners, alltrace rows and math. Fresh graph/descriptor/namespace/alias/absence/root counts derive after genuine PREP, never copy V12 historical counts.'),
 dict(area='next full combined readiness',functions=['full5 stage source and actual receipts','whole bounded INPUT intake and newcold retarget'],
   change='Component86 success is INPUT-only, followed by one fresh combined PREP +original5stage run +four tails under original1800/600/512/2GiB/96free8/thread1/child1/retry0. Only actualcombineddecl/seal/terminal/runtime/PREP proof can bind new standalone whole3argINPUT intake. Then newcold uses completeproof; no oldAAA0map/cache/accuracy credit.'),
]
report=dict(schema='AXMAT_V15_COMPONENT_TO_COMPLETE_COMBINED_LIMITED_RETARGET_SOURCE_PLAN_V1',status='SOURCE_ONLY_PLAN_UNREADY',
    source_pins=files,actual_V15_source_status=constant(V15,'SOURCE_STATUS'),actual_V15_source_not_a_component_success_receipt=True,
    authoritative_component_constants=component_constants,
    actual_production_admission_signature=['build_seal_sha','terminal_evidence','terminal_evidence_sha256'],
    actual_production_admission_schema=schema,actual_production_admission_scope_label=admission,
    complete_actual_API_return_field_names_in_original_order=api_fields,
    future_component_seven_success_pins=success_pins,
    future_combined_prepare_declaration_seal_terminal_runtime=None,
    old_V13_source_blueprint=dict(path=str(V13),sha256=files[str(V13)]['sha256'],whole32region_inverse_to_V12_verified=True,
        region_count=len(regions),source_only=True,its_failed_or_partial_run_not_used=True,baseline_same_complete_functions=same),
    finite_retarget_items=retarget,
    exact_function_locations=dict(V12={name:location(V12,name) for name in ['trim_component_contract','trim_component_input','record_actual_trim_component','combined_link_command','complete_input_phase','create_complete_input_graph','DynamicHistoryResources','resources_for','production_admission']},
        V15={name:location(V15,name) for name in ['production_admission','root_index_resource_source_admission','root_index_resource_factory','DynamicHistoryResources','validate_history_roots','declaration_admission']},
        V13_source_blueprint={name:location(V13,name) for name in ['sender_component_contract','combined_link_command','trim_component_contract','trim_component_input','production_admission']}),
    unchanged_required=dict(INPUT_SPECS_path=str(constant(V12,'INPUT_SPECS')),INPUT_SPECS_SHA=constant(V12,'INPUT_SPECS_SHA'),
        graph_helper=files[str(GRAPH)],fullseven_typed_order_floatbits_and_alltrace=True,alloriginalcontrols_and_physics=True,
        combined_stages=5,component_stages=86,original68_counts=30,
        budgets=dict(whole_seconds=1800,stage_seconds=600,RSS_MiB=512,archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0)),
    new_source_draft_generated=False,only_plan_generated=True,canonical_project_written=False,
    business_imported_or_called=False,API_build_regression_transport_started=False,Root_polled=False,
    big35GB_rehash=False,new_full86_combined_native_AAA_ABA_credit=False,
    retained_readonly_error=dict(chunk='461064',exit_code=1,closed=True,
        reason='Pure literal reader initially omitted Path.parent; added only that AST path branch. No business execution or source change.'))
for path,wanted in files.items():assert pin(Path(path))==wanted
save('RETARGET_PLAN_AND_REPORT.json',report)
with (D/'REPORT.txt').open('x') as stream:
    stream.write('V15→新combined的有限接入计划，SOURCE_ONLY/UNREADY，未生成或安装业务工厂。\n1. 七个实际组件成功pin继续None：decl/seal/Rootterminal/sourceadmission/SPOTobject/runtime/newsenderobject。V15当前源READY或资源资格5a0b都不是实际86资格。\n2. V12母只接两object/index1/68；新V15必须第三sender override/index2/86。原68完整30counts保留，14sender/70raw/48stub独立核对，不加2710真实SPOT数学调用；完整原92link逆向与生产unitstub排除必需。冻结c064可作这些source-only接线蓝图，完整32逆5af已重核，不借其失败执行。\n3. 新组件确切schema为AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15，原三参数production_admission签名不变。保留H7d/1809/16d整份SOURCE资格，新增root_index完整fullpins/新ebbb实际class源+原fe811祖先；所有额外owner进入完整图。\n4. 原2cad七INPUT/e8两严格losslessreader/所有trace与当前fresh复核保留。新graph/descriptor/root计数由真实执行derive，不借36776旧数量。新combined可正常委托已资格V15资源模块，原builder/helper/OwnRSS MRO及历史祖先不动。\n5. 原5阶段1800/600/512/2GiB/96/free8/1/1/0和四tails继续；component合格后仍需新combined→wholeINPUT→cold真实执行。无项目写、业务导入/调用、构建或数值；没有新86/native/AAA/ABA资格。\n')
print(json.dumps(dict(status=report['status'],REPORT=pin(D/'RETARGET_PLAN_AND_REPORT.json'),source_V15=files[str(V15)],
    exact_retarg_items=len(retarget),future_success_pin_count=len(success_pins)),indent=2))

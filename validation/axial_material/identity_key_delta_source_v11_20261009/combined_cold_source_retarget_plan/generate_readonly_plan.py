import ast
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
AM=ROOT/'validation/axial_material'
D=Path('/private/tmp/axmat_v11_minimal_combined_cold_retarget_plan_20261009')
N='cross_group_identity_key_delta'
sources={
 'combined':(AM/'prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py','c55ca2680d9e1326979649f835d9612a8fd80df5aecee1adc25765c419329efc'),
 'cold_factory':(AM/'prepare_historical_input_owned_specs_physical_factor_diagonal_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak_v10.py','bc8eaa6a72e0e732be5f95ef06fe430a2f8e8848d4edba3bedcd53adc29fecf9'),
 'cold_consumer':(AM/'cold_component_input_consumer_factor_diagonal_trim_own_pid_peak_v10.py','5911db3dec1cf377a47fa90f89add39fe3bcb7d2a206375cb6c07029f20f07b4'),
 'cold_binding':(AM/'cold_owned_specs_factor_diagonal_trim_component_input_intake_binding_v10_20261009.json','14a803e7f230d69fc9a82cdcd325333e7a080eec8117285e8a60c99758d27b48'),
}
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 s=p.lstat();return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
before={str(p):ident(p) for p,h in sources.values()}
payloads={}
for name,(p,h) in sources.items():
 b=p.read_bytes();assert sha(b)==h;payloads[name]=b
parent=payloads['combined'].decode();tree=ast.parse(parent)
lines=parent.splitlines(keepends=True);offsets=[0]
for text in lines:offsets.append(offsets[-1]+len(text))
def span(node):return (offsets[node.lineno-1]+node.col_offset,offsets[node.end_lineno-1]+node.end_col_offset)
assigns={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
replacements={
 'SOURCE':"ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-cross-group-identity-key-delta-live-resource-scopes-v11-20261009'",
 'OUT':"ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-cross-group-identity-key-delta-live-resource-scopes-v11-20261009'",
 'TERMINAL':"ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-cross-group-identity-key-delta-live-resource-scopes-v11-20261009'",
 'FAMILY':repr('HISTORICAL_INPUT_CROSS_GROUP_IDENTITY_KEY_DELTA_COMBINED_RUNTIME_LINK_V11'),
 'PREFIX':repr('AXMAT_HISTORICAL_INPUT_OWNED_SPECS_CROSS_GROUP_IDENTITY_KEY_DELTA_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V11'),
 'FORMAL_FACTORY':"ROOT/'validation/axial_material/prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.py'",
 'DRAFT_STATUS':repr('UNREADY_PENDING_FINAL_V11_COMPONENT_CONTRACT_AND_ACTUAL_BUILD_WITNESSES'),
 'TRIM_FACTORY':"ROOT/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'",
 'TRIM_SOURCE':"ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-20261009'",
 'TRIM':"ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-20261009'",
 'TRIM_TERMINAL':"ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-20261009'",
 'TRIM_KERNEL_SHA':repr('0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'),
 'TRIM_PATCH_HELPER':"ROOT/'validation/axial_material/rank1_factor_cache_cross_group_identity_key_delta_patch.py'",
 'TRIM_CONTROLS_SOURCE':"ROOT/'validation/axial_material/rank1_factor_cache_cross_group_identity_key_delta_controls.f90'",
 'TRIM_COMPLETE_C0_PROOF':"ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/complete_c0_source_patch_proof.json'",
 'TRIM_CODEC_PLAN':"ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/identity_key_delta_control_contract.json'",
}
unknowns=['TRIM_FACTORY_SHA','TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','TRIM_SCHEMA','TRIM_ADMISSION','TRIM_PATCH_HELPER_SHA','TRIM_CONTROLS_SOURCE_SHA','TRIM_COMPLETE_C0_PROOF_SHA','TRIM_CODEC_PLAN_SHA']
for name in unknowns:replacements[name]='None'
edits=[]
for name,value in replacements.items():
 node=assigns[name].value;lo,hi=span(node)
 edits.append(dict(name=name,start=lo,end=hi,old=parent[lo:hi],new=value))
doc=tree.body[0]
assert isinstance(doc,ast.Expr) and isinstance(doc.value,ast.Constant)
lo,hi=span(doc.value)
edits.append(dict(name='source_only_module_docstring',start=lo,end=hi,old=parent[lo:hi],new=repr('UNREADY V11 identity and dependency draft only. Original V10 function bodies remain byte-exact. The selected component schema/proof/count guards still await the final V11 source contract; all actual build pins are None. No business or Root success is represented.')))
draft=parent
for e in sorted(edits,key=lambda x:x['start'],reverse=True):draft=draft[:e['start']]+e['new']+draft[e['end']:]
dtree=ast.parse(draft)
def functions(text,tree):return {(n.name,n.lineno if False else ast.get_source_segment(text,n).splitlines()[0]):ast.get_source_segment(text,n) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
oldfunc=functions(parent,tree);newfunc=functions(draft,dtree);assert oldfunc==newfunc and len(oldfunc)==70
# Independent full inverse applies unique complete assignment lines/doc source.
inverse=draft
for e in sorted(edits,key=lambda x:x['start']):
 if e['name']=='source_only_module_docstring':
  assert inverse.count(e['new'])==1;inverse=inverse.replace(e['new'],e['old'],1)
 else:
  oldline=e['name']+' = '+e['old'];newline=e['name']+' = '+e['new']
  assert inverse.count(newline)==1;inverse=inverse.replace(newline,oldline,1)
assert inverse==parent
draftpath=D/'prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.UNREADY.py'
draftpath.write_text(draft)
assert all(isinstance(n.value,ast.Constant) and n.value.value is None for n in dtree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in unknowns)
planpath=Path('/private/tmp/axmat_v11_combined_cold_retarget_source_plan_independent_review_20261009/source_plan.json')
textpath=planpath.with_name('review.txt')
assert sha(planpath.read_bytes())=='32ff18dada7aa478c3f0d010c51121601bcfe1c3e934c7331a80d1c819d871cb'
assert sha(textpath.read_bytes())=='58aa070220fbb29272f777e6d969f155367ae1c2235ca7a7017227324338e603'
assert before=={str(p):ident(p) for p,h in sources.values()}
report={
 'schema':'axmat_v11_minimal_combined_cold_retarget_source_plan_v1','status':'UNREADY_SOURCE_PLAN_ONLY',
 'source_pins':[{ 'role':name,'path':str(p),'sha256':h,'identity':before[str(p)] } for name,(p,h) in sources.items()],
 'fresh_source_identity_before_after_equal':True,
 'exact_slot_plan':{'path':str(planpath),'sha256':sha(planpath.read_bytes())},
 'independent_source_callsite_report':{'path':str(textpath),'sha256':sha(textpath.read_bytes())},
 'combined_identity_only_unready_draft':{'path':str(draftpath),'sha256':sha(draftpath.read_bytes()),'complete_inverse_byteexact':True,'original65top_and70total_function_bodies_byteexact':True,'unknown_slots_all_None':unknowns,'original_business_function_guards_intentionally_not_retargeted_yet':True,'proposed_new_names_require_Root_confirmation_against_final_component_source':True},
 'edits':edits,
 'minimal_next_changes_after_actual_V11_component_contract':[
   {'file':'combined','functions':['trim_component_contract','trim_component_input'],'change':'Bind new component runtime INPUT schema/admission/source family, successful seal schema, exact actual full stage counters and identity storage/codec controls. Split current0800 complete proof from retained factor-diagonal ancestor5e and last-cprime ancestor343e. No ancestor proof rewrite or old PASS transfer.'},
   {'file':'combined','functions':['record_actual_trim_component'],'change':'Retain one actual complete production_admission(seal_sha,terminal_path,terminal_sha) three-argument call under original read/absence audit. Confirm the new final factory actual signature; retain complete returned body/trace and graph typed owners without pruning.'},
   {'file':'combined','functions':['create_complete_input_graph','complete_input_phase'],'change':'Retain all historical body/source/namespace/alias/absence and all dynamic resource roots. Fresh derive new counts/content, strict canonical row/owner proof and original64MiB file cap; never insert old count or frozen inventory as new expectation.'},
   {'file':'cold_consumer','functions':['last_cprime_trim_return_admission'],'change':'Only the current component identity/schema/new stage+codec flags change to final new contract. Preserve factor storage shape[nstate-1,nstate,nblock], all fields of current returned component and historical7-body/math/alias semantics.'},
   {'file':'cold_factory','functions':['component_return_admission','render_controller','declare'],'change':'Bind new combined whole INPUT metadata/cold schemas; update two exact consumer copied basenames at original637/790. All controller/math/source inverse, real classes/MRO, host/control source files and constructor wrappers stay byte-exact.'},
   {'file':'bounded_intake','functions':['main','postterminal recorder'],'change':'Use V10 frozen host+recorder templates and a fresh independent V11 intake root. Source identity retarget only; actual Combined DECL/PREP/seal/terminal/source admission must be new true pins. Record9payload+Root10 only after genuine bound host0; no old ROOT or old API logfile substitution.'},
   {'file':'cold_binding','functions':[],'change':'Create a new descriptor from actual fresh ten-payload/graph content/SOURCE inventories and alias observation, not the old186 count. No descriptor self-SHA; normal expected owners independently derived rather than fresh-current pseudoexpectations.'},
 ],
 'readiness_sequence':[
   'Final V11 component source admission; all unknown run pins stayNone.',
   'Genuine fresh component PREP+full68stages candidate contract/Root terminal/source admission/object/production Dragon independently approved; exact stage total derives from final source, not this plan.',
   'Bind those actual component pins in reviewed new combined source; fresh newcombined PREP and alloriginal5stages+4tails+Root terminal independently approved under1800/600/512.',
   'Bind reviewed standalone host+recorder only to that new success; unique actual bounded complete INPUT call and durable9+Root10 independently approved.',
   'Bind new cold F/C/B to full qualified INPUT; all cold DECL/PREP/binding/controls/finalization/native future pins stayNone until their actual original stages independently close.',
 ],
 'unchanged_contract':{'whole_seven_INPUT_SHA256':'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa','graph_helper':'1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643','typed_codec':'758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69','current_predicates':'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19','component_and_combined_caps':'1800/600/512MiB/thread1/child1/retry0','cold_caps':'setup120/axial4200/radial600/maps300/4200/host120/max100/whole43200/own512MiB/child1/retry0','history':'96GiB/free8GiB/complete original roots and original reserve','producer':'Python3.14.4 plus original SciPy/NumPy admission; PYTHONDONTWRITEBYTECODE=1 explicitly required','analysis_build_intake':'original Python3.12','no_module_class_overlay':True},
 'actual_new_component':None,'actual_new_combined':None,'actual_new_bounded_intake':None,'actual_new_cold':None,
 'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'business_executed':False,'project_written':False,
}
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('V11 最小接入计划已保存，全部新实际凭据为None，UNREADY。\n'
 'TMP combined身份草稿完整逆回V10 c55，65顶层/70全部函数逐字不改。\n'
 '待新组件完整源合同及真实68stage构建后，改当前schema/codec/计数与0800 proof层；factor5e、last-cprime343e祖先证据保留。\n'
 '随后新combined PREP+5stage+4tail、真实bounded whole INPUT9+Root10、cold F/C/B独立逐阶段接入；不能复用V10成功或FAILED bootstrap。\n'
 '完整物理/角度/快照、原7INPUT与完整owner/alias/ns/absence/resource闭包、原512/4200/43200门和P14/P12分离保持。\n'
 '具体常量与函数行参见source_plan.json绑定报告；当前onlyidentity草稿不具备新的component guard，故不可READY或执行。\n')
print(json.dumps(dict(status=report['status'],report_sha256=sha((D/'REPORT.json').read_bytes()),draft_sha256=sha(draftpath.read_bytes()),full_functions=70,top_functions=65)))

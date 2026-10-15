import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT=Path('/Users/wen/spot')
AM=ROOT/'validation/axial_material'
D=Path('/private/tmp/axmat_v11_combined_component_contract_source_draft_20261009')
BASE=Path('/private/tmp/axmat_v11_minimal_combined_cold_retarget_plan_20261009')
NAME='prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.UNREADY.py'
PINS={
 'identity_draft':(BASE/NAME,'711762b183d81189f4727e237f21e4c0aff30065bf7d58b0932c504fe2f39709'),
 'combined_mother':(AM/'prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py','c55ca2680d9e1326979649f835d9612a8fd80df5aecee1adc25765c419329efc'),
 'component_factory':(AM/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py','f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'),
 'component_helper':(AM/'rank1_factor_cache_cross_group_identity_key_delta_patch.py','733855513a81ead79f797dc0843b061f1604ab61b6db9684613a06a067387300'),
 'component_controls':(AM/'rank1_factor_cache_cross_group_identity_key_delta_controls.f90','eab3a7790e9f499282017cc37581be5acb07f8a4170e8fcaae95b0de47305d52'),
 'keycodec_controls':(AM/'identity_key_delta_source_v11_20261009/keycodec_controls.f90','3f59d94d49c049b206419b49c3a3ac437aa3d980548ab8fb27632ba4dfd472f7'),
 'keycodec_auditor':(AM/'rank1_cross_group_identity_key_codec_controls_audit.py','8ecf321ed137de883160dade3b33f95765d5e5e71c54747ef2e49de8bd150903'),
 'new_kernel':(AM/'identity_key_delta_source_v11_20261009/SPOT1P64.f90','0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'),
 'factor_kernel':(AM/'factor_diagonal_trim_source_v10_20261009/SPOT1P64.f90','5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809'),
 'factor_whole_proof':(AM/'factor_diagonal_trim_source_v10_20261009/complete_c0_source_patch_proof.json','cdc033619d16f89cdd0e284ec87ad09701202bb5131860f39a70f773391214ea'),
 'factor_proof':(AM/'factor_diagonal_trim_source_v10_20261009/source_patch_proof.json','dc1fe76a84e19f5125650423e2c034dc6ed26da906b8ef8aafdfe766bcd608f1'),
 'factor_codec_plan':(AM/'factor_diagonal_trim_source_v10_20261009/factor_codec_control_contract.json','7026f91f2098f9bf9d14f2d34f455473a654000ace6e3864b53d9a20bbb14373'),
 'factor_controls':(AM/'rank1_factor_cache_factor_diagonal_trim_controls.f90','82b19974518f44952f829ef388a9b5fdbf58e2b4b7df2d7f7d61f7839038def4'),
 'identity_contract':(AM/'identity_key_delta_source_v11_20261009/component_source_extension/identity_key_delta_contract.json','4bc48ab443cbd7e9b1253a5cc4e758db2e9a877f2603f0a9833b5b92332ffcfb'),
}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def ident(path):
 s=path.lstat();return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
before={str(path):ident(path) for path,h in PINS.values()}
payload={}
for role,(path,wanted) in PINS.items():
 raw=path.read_bytes();assert sha(raw)==wanted,(role,sha(raw),wanted);payload[role]=raw
old=payload['identity_draft'].decode();mother=payload['combined_mother'].decode();factory=payload['component_factory'].decode();helper=payload['component_helper'].decode()
ft=ast.parse(factory);ht=ast.parse(helper)
fa={n.targets[0].id:n.value for n in ft.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
ha={n.targets[0].id:n.value for n in ht.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
edits_value=ast.literal_eval(ha['IDENTITY_EDITS'])
edits_path=AM/'identity_key_delta_source_v11_20261009/region_edits.json'
raw=edits_path.read_bytes();edits_sha=sha(raw);assert json.loads(raw)==edits_value
before[str(edits_path)]=ident(edits_path);PINS['identity_edits']=(edits_path,edits_sha)
kernel=payload['new_kernel'].decode();factor_kernel=payload['factor_kernel'].decode();inverse=kernel
for row in reversed(edits_value):
 assert inverse.count(row['new'])==1;inverse=inverse.replace(row['new'],row['old'],1)
assert inverse==factor_kernel and len(edits_value)==6
retained={}
for name in ('SPOT1P64_FACTOR64','SPOT1P64_SOLVE64','boundary_solve','rank1_identity'):
 pattern=r'(?ms)^  subroutine '+re.escape(name)+r'\(.*?^  end subroutine '+re.escape(name)+r'\n'
 a=re.findall(pattern,factor_kernel);b=re.findall(pattern,kernel);assert len(a)==1 and a==b;retained[name]=sha(a[0].encode())
prod=next(n for n in ft.body if isinstance(n,ast.FunctionDef) and n.name=='production_admission')
assert [a.arg for a in prod.args.args]==['build_seal_sha','terminal_evidence','terminal_evidence_sha256']
prodsrc=ast.get_source_segment(factory,prod)
for token in ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',
 'RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_RUNTIME_INPUT_ONLY',"audit.get('cross_group_identity_controls_passed') is not True",
 "result.get('cross_group_identity_controls_passed') is not True","controls['keycodec_controls']['status']!='PASS'",
 "controls['counts']['total_declared_stages']!=68",'controls = control_audit(d)','resources_for(d["resource_roots"]).check()'):
 assert token in prodsrc,token
returned=next(n for n in ast.walk(prod) if isinstance(n,ast.Return) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='dict')
assert 'cross_group_identity_controls_passed' not in [kw.arg for kw in returned.value.keywords]
out=old;changes=[]
def change(label,a,b):
 global out
 assert out.count(a)==1,(label,out.count(a));out=out.replace(a,b,1);changes.append(dict(name=label,old=a,new=b))
tree=ast.parse(old)
assigns={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def constant(name,rhs):
 node=assigns[name];change(name,ast.get_source_segment(old,node.value),rhs)
# Use whole assignment regions, since several None/literals recur.
def constant(name,rhs):
 node=assigns[name];change(name,ast.get_source_segment(old,node),name+' = '+rhs)
constant('DRAFT_STATUS',repr('UNREADY_PENDING_ACTUAL_V11_COMPONENT_BUILD_WITNESSES_AND_SOURCE_REVIEW'))
constant('TRIM_FACTORY_SHA',repr(PINS['component_factory'][1]))
constant('TRIM_SOURCE',ast.get_source_segment(factory,fa['SOURCE']))
constant('TRIM',ast.get_source_segment(factory,fa['OUT']))
constant('TRIM_TERMINAL',ast.get_source_segment(factory,fa['TERMINAL']))
constant('TRIM_PATCH_HELPER_SHA',repr(PINS['component_helper'][1]))
constant('TRIM_CONTROLS_SOURCE_SHA',repr(PINS['component_controls'][1]))
constant('TRIM_SCHEMA',repr('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'))
constant('TRIM_ADMISSION',repr('RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_RUNTIME_INPUT_ONLY'))
constant('TRIM_COMPLETE_C0_PROOF',"ROOT/'validation/axial_material/factor_diagonal_trim_source_v10_20261009/complete_c0_source_patch_proof.json'")
constant('TRIM_COMPLETE_C0_PROOF_SHA',repr(PINS['factor_whole_proof'][1]))
constant('TRIM_CODEC_PLAN',"ROOT/'validation/axial_material/factor_diagonal_trim_source_v10_20261009/factor_codec_control_contract.json'")
constant('TRIM_CODEC_PLAN_SHA',repr(PINS['factor_codec_plan'][1]))
old_doc=ast.get_source_segment(old,tree.body[0])
change('module_docstring',old_doc,repr('UNREADY V11 source-only component adapter. All six actual component run pins remain None. The genuine three-argument API and full V11 source/68-stage codec metadata must pass before complete owned INPUT reuse. Original seven INPUT bodies, physics, classes, math, graph scope and budgets remain unchanged.'))
extra="\n# Current0800 identity representation; original5e and343e remain whole ancestor proofs.\n"
extra+="TRIM_FACTOR_KERNEL_SHA = "+repr(PINS['factor_kernel'][1])+"\n"
extra+="TRIM_FACTOR_CONTROLS_SOURCE = ROOT/'validation/axial_material/rank1_factor_cache_factor_diagonal_trim_controls.f90'\n"
extra+="TRIM_FACTOR_CONTROLS_SOURCE_SHA = "+repr(PINS['factor_controls'][1])+"\n"
extra+="TRIM_FACTOR_PATCH_HELPER = ROOT/'validation/axial_material/rank1_factor_cache_factor_diagonal_trim_patch.py'\n"
extra+="TRIM_FACTOR_PATCH_HELPER_SHA = 'd849ebbbe4dd7e59b17bd67e60a07f950aa7a2fc33f22011431c83c46cff1b6e'\n"
extra+="TRIM_IDENTITY_CONTRACT = ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/component_source_extension/identity_key_delta_contract.json'\n"
extra+="TRIM_IDENTITY_CONTRACT_SHA = "+repr(PINS['identity_contract'][1])+"\n"
extra+="TRIM_IDENTITY_EDITS = ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/region_edits.json'\n"
extra+="TRIM_IDENTITY_EDITS_SHA = "+repr(edits_sha)+"\n"
extra+="TRIM_IDENTITY_RETAINED_SOURCE_SHA = "+repr(retained)+"\n"
extra+="TRIM_KEYCODEC_SOURCE = ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/keycodec_controls.f90'\n"
extra+="TRIM_KEYCODEC_SOURCE_SHA = "+repr(PINS['keycodec_controls'][1])+"\n"
extra+="TRIM_KEYCODEC_AUDITOR = ROOT/'validation/axial_material/rank1_cross_group_identity_key_codec_controls_audit.py'\n"
extra+="TRIM_KEYCODEC_AUDITOR_SHA = "+repr(PINS['keycodec_auditor'][1])+"\n"
extra+="TRIM_KEYCODEC_MUTATIONS = ('unchanged_word','difference_word','stored_difference_word','base_word','input_length','load_length','ineligible_existing','corrupt_index_zero','corrupt_index_high','missing_anchor')\n"
extra+="TRIM_KEYCODEC_CASES = tuple(dict(name=mutation+'_p'+str(phase),args=['negative',mutation,str(phase)],expected_returncode=23,expected_message='SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.') for phase in (1,2) for mutation in TRIM_KEYCODEC_MUTATIONS)\n"
anchor="TRIM_INPUT_NAME = 'trim_component_admission_INPUT.json'"
change('new_source_contract_constants',anchor,extra+'\n'+anchor)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='trim_component_contract')
a=ast.get_source_segment(old,node);b=a
def local(x,y):
 global b
 assert b.count(x)==1,(x,b.count(x));b=b.replace(x,y,1)
local("value['cache_unit_control_counts']['total_declared_stages']!=45","value['cache_unit_control_counts']['total_declared_stages']!=68\n        or value['cache_unit_control_counts']['original_factor_diagonal_45_stages_retained']!=45\n        or value['cache_unit_control_counts']['additional_keycodec_driver_build_stages']!=2\n        or value['cache_unit_control_counts']['additional_keycodec_execute_stages']!=21")
local("p=admission['source_patch_proof'];t=p['last_cprime_trim']","p=admission['source_patch_proof'];parent=p['inherited_v10_complete_proof'];t=parent['last_cprime_trim']")
local("admission['schema']!='AXMAT_RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_SOURCE_ADMISSION_V1'","admission['schema']!='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_SOURCE_ADMISSION_V1'")
local("d['family']!='RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_BUILD'","d['family']!='RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11'")
local("factor=p['factor_diagonal_trim'];codec=d['control_contract']['factor_codec_control_contract']","factor=parent['factor_diagonal_trim'];codec=d['control_contract']['factor_codec_control_contract']")
local("p!=read(require(TRIM_COMPLETE_C0_PROOF,TRIM_COMPLETE_C0_PROOF_SHA))","parent!=read(require(TRIM_COMPLETE_C0_PROOF,TRIM_COMPLETE_C0_PROOF_SHA))")
local("factor['candidate_kernel_sha256']!=TRIM_KERNEL_SHA","factor['candidate_kernel_sha256']!=TRIM_FACTOR_KERNEL_SHA")
local("codec['controls_source']!=d['controls_source']","codec['controls_source']!=dict(path=str(TRIM_FACTOR_CONTROLS_SOURCE),sha256=TRIM_FACTOR_CONTROLS_SOURCE_SHA)")
append='''    identity_contract=read(require(TRIM_IDENTITY_CONTRACT,TRIM_IDENTITY_CONTRACT_SHA))
    identity_edits=read(require(TRIM_IDENTITY_EDITS,TRIM_IDENTITY_EDITS_SHA))
    identity=dict(schema='AXMAT_RANK1_CROSS_GROUP_INTEGER_IDENTITY_KEY_DELTA_STORAGE_V1',
        parent_kernel_sha256=TRIM_FACTOR_KERNEL_SHA,candidate_kernel_sha256=TRIM_KERNEL_SHA,
        complete_inverse_byteexact=True,edits=identity_edits,retained_whole_source_sha256=TRIM_IDENTITY_RETAINED_SOURCE_SHA,
        contract=identity_contract,actual_controls_executed=False,actual_native_RSS_passed=False,
        AAA_accuracy_qualified=False,ABA_admitted=False)
    expected_proof=dict(parent)
    expected_proof.update(inherited_v10_complete_proof=parent,edits=parent['edits']+identity_edits,
        cross_group_identity_key_delta=identity,candidate_kernel_sha256=TRIM_KERNEL_SHA,
        delegated_factor_diagonal_helper=dict(path=str(TRIM_FACTOR_PATCH_HELPER),sha256=TRIM_FACTOR_PATCH_HELPER_SHA),
        scope='ORDINARY_RANK1_LOWER_DICTIONARY_TERMINAL_CPRIME_DEAD_FACTOR_DIAGONAL_AND_CROSS_GROUP_INTEGER_IDENTITY_STORAGE_ONLY')
    if (p!=expected_proof or parent['candidate_kernel_sha256']!=TRIM_FACTOR_KERNEL_SHA
        or admission['cross_group_identity_key_delta']!=identity_contract
        or d['control_contract']['cross_group_identity_key_delta']!=identity_contract
        or admission['keycodec_source']!=dict(path=str(TRIM_KEYCODEC_SOURCE),sha256=TRIM_KEYCODEC_SOURCE_SHA)
        or admission['keycodec_auditor']!=dict(path=str(TRIM_KEYCODEC_AUDITOR),sha256=TRIM_KEYCODEC_AUDITOR_SHA)
        or d['control_contract']['keycodec_positive_command_args']!=['positive']
        or d['control_contract']['keycodec_negative_cases']!=list(TRIM_KEYCODEC_CASES)
        or d['control_contract']['original45_required']is not True
        or d['control_contract']['total_planned_stage_count']!=68
        or any(d['files'].get(path)!=wanted for path,wanted in (
            (str(TRIM_IDENTITY_CONTRACT),TRIM_IDENTITY_CONTRACT_SHA),
            (str(TRIM_KEYCODEC_SOURCE),TRIM_KEYCODEC_SOURCE_SHA),
            (str(TRIM_KEYCODEC_AUDITOR),TRIM_KEYCODEC_AUDITOR_SHA)))):
        raise ValueError('entire V11 identity source proof/contract and inherited5e/343e layers differ')
    inverse=require(TRIM_SOURCE/'SPOT1P64.f90',TRIM_KERNEL_SHA).read_text()
    for edit in reversed(identity_edits):
        if inverse.count(edit['new'])!=1:raise ValueError('V11 six-region source inverse is not unique')
        inverse=inverse.replace(edit['new'],edit['old'],1)
    if hashlib.sha256(inverse.encode()).hexdigest()!=TRIM_FACTOR_KERNEL_SHA:
        raise ValueError('complete new kernel inverse must be original5e, not cprime343e')
    sealed=read(require(TRIM/'seal.json',TRIM_SEAL_SHA))
    descriptors=((value['compiled_unit_controls'],'audit/controls.json'),)
    for descriptor,relative in descriptors:
        if descriptor!=dict(path=str(TRIM/relative),sha256=sealed['files'][relative]):
            raise ValueError('new codec evidence must be bound by the actual new successful whole seal')
    controls=read(require(value['compiled_unit_controls']['path'],value['compiled_unit_controls']['sha256']))
    audit=read(require(TRIM/'audit/result.json',sealed['files']['audit/result.json']))
    result=read(require(TRIM/'driver_result.json',sealed['files']['driver_result.json']))
    keycodec=controls['keycodec_controls']
    if (controls['schema']!='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_FULL_RAW_CONTROLS_AUDIT_V1'
        or controls['status']!='PASS' or controls['counts']!=value['cache_unit_control_counts']
        or controls['counts']!=audit['control_counts'] or controls['counts']!=result['control_counts']
        or audit['classification']!='PASS_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY'
        or result['classification']!='COMPLETE_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY'
        or result['error']is not None or audit['cross_group_identity_controls_passed']is not True
        or result['cross_group_identity_controls_passed']is not True
        or controls['all_c017_full_identity_keys_bitwise_equal_to_candidate_decode']is not True
        or keycodec['schema']!='AXMAT_RANK1_CROSS_GROUP_IDENTITY_KEY_CODEC_CONTROLS_AUDIT_V1'
        or keycodec['status']!='PASS' or keycodec['actual_codec_controls_passed']is not True
        or (keycodec['standalone_control_count'],keycodec['positive_key_count'],keycodec['positive_stats_count'],
            keycodec['expected_negative_actual_rejection_count'])!=(21,27,6,20)
        or (keycodec['raw_binary_bytes'],keycodec['raw_manifest_jsonl_bytes'],keycodec['raw_xabort_bytes'],keycodec['raw_total_bytes'])!=(70792,26930,1000,98722)
        or any(keycodec[k]is not True for k in ('complete_input_encoded_positions_anchor_decoded_wordwise_equal',
            'canonical_strict_cost_fallback_zero_delta_two_phase_lifecycle_and_hits_verified','exact_EOF_verified',
            'all_fresh_seven_identity_before_after_equal'))
        or any(keycodec[k]is not False for k in ('original45_controls_completion_claimed','full_component_build_admission_claimed',
            'actual_full_FLU_entry_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('new68 stages and independent21 raw codec controls required; compatibility label grants no new scope')
    del parent,identity,expected_proof,identity_contract,identity_edits,inverse,sealed,controls,audit,result,keycodec
'''
local('    del bodies;gc.collect()',append+'    del bodies;gc.collect()')
change('trim_component_contract',a,b)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='trim_component_input')
a=ast.get_source_segment(old,node);b=a.replace('AXMAT_RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_BUILD_SEAL_V1','AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1')
target="str(TRIM/'runtime/Dragon'):TRIM_RUNTIME_SHA,str(TRIM_TERMINAL/'terminal_return.json'):TRIM_TERMINAL_SHA})"
assert b.count(target)==1
b=b.replace(target,"str(TRIM/'runtime/Dragon'):TRIM_RUNTIME_SHA,str(TRIM_TERMINAL/'terminal_return.json'):TRIM_TERMINAL_SHA,\n        str(TRIM_IDENTITY_EDITS):TRIM_IDENTITY_EDITS_SHA})",1)
change('trim_component_input',a,b)
# Complete source inverse proves no other original byte changed.
fullinverse=out
for row in reversed(changes):
 assert fullinverse.count(row['new'])==1,row['name'];fullinverse=fullinverse.replace(row['new'],row['old'],1)
assert fullinverse==old
ot=ast.parse(out)
def funcs(text):
 t=ast.parse(text);return {n.name:ast.get_source_segment(text,n) for n in t.body if isinstance(n,ast.FunctionDef)}
mf=funcs(mother);of=funcs(out)
assert len(mf)==len(of)==65
assert set(mf)==set(of)
changed=[name for name in mf if mf[name]!=of[name]];assert changed==['trim_component_contract','trim_component_input'],changed
assert len([n for n in ast.walk(ast.parse(mother)) if isinstance(n,ast.FunctionDef)])==len([n for n in ast.walk(ot) if isinstance(n,ast.FunctionDef)])==70
assert mf['record_actual_trim_component']==of['record_actual_trim_component']
assert all(mf[n]==of[n] for n in ('strict_json_bytes','actual_components','component_contract','create_complete_input_graph','complete_input_phase','resources_for','DynamicHistoryResources','audit_build','require_ready'))
oa={n.targets[0].id:n.value for n in ot.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
unknown=['TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA']
assert all(ast.literal_eval(oa[n]) is None for n in unknown)
assert ast.literal_eval(oa['DRAFT_STATUS']).startswith('UNREADY')
assert before=={str(path):ident(path) for path,h in PINS.values()}
assert all(sha(path.read_bytes())==h for path,h in PINS.values())
draft=D/NAME;draft.write_text(out)
(D/'adapter_region_edits.json').write_text(json.dumps(changes,indent=2,allow_nan=False)+'\n')
(D/'adapter.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),out.splitlines(True),fromfile=str(BASE/NAME),tofile=str(draft))))
(D/'component_production_admission_source_snapshot.txt').write_text(prodsrc+'\n')
report=dict(schema='AXMAT_V11_COMBINED_COMPONENT_ADAPTER_SOURCE_ONLY_V1',status='UNREADY_SOURCE_ADAPTER_ONLY',
 draft=dict(path=str(draft),sha256=sha(out.encode())),
 source_pins=[dict(role=role,path=str(path),sha256=h,identity=before[str(path)]) for role,(path,h) in PINS.items()],
 source_identity_and_whole_SHA_before_after_equal=True,complete_inverse_to_identity_only_draft_byteexact=True,
 module_function_inventory=dict(top_level=65,all_including_nested=70,changed_top_level=changed,unchanged_top_level=63),
 genuine_three_argument_component_API_record_body_byteexact=True,
 full_historical_seven_INPUT_and_original_math_classes_graph_cap_and_all_resource_bodies_byteexact=True,
 current_component_interface=dict(factory_sha256=PINS['component_factory'][1],
  schema='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1',
  compatibility_admission_label='RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_RUNTIME_INPUT_ONLY',
  returned_cross_group_flag_exists=False,qualified_by='full actual production_admission gates plus independently pinned source proof/control contract/whole sealed controls+audit+result, never label alone',
  stages=dict(total=68,original_factor_diagonal=45,keycodec_driver_builds=2,keycodec_executions=21),
  source_layers=dict(current0800=PINS['new_kernel'][1],inherited5e=PINS['factor_kernel'][1],last_cprime343e='343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1')),
 all_actual_component_run_bindings_None=unknown,actual_new_component_completed=None,actual_new_combined=None,
 actual_new_bounded_INPUT=None,actual_new_cold=None,
 actual_run_outputs_read=False,component_API_executed=False,compiled=False,business_imported=False,project_written=False,
 no_module_or_class_overlay=True,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 original_caps=dict(total_wall=1800,stage_wall=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_cap_bytes=96*2**30,
  free_floor_bytes=8*2**30,thread=1,child=1,retries=0),
 source_only_limit='No actual component seal/Root terminal/object/runtime qualification; Root must bind genuine success only after full68-stage independent approval and obtain separate complete source admission. No PREP/combined runtime/INPUT/cold/native permission from this draft.')
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('V11 combined组件接口TMP草稿已接线，仍UNREADY。\n'
 '真实f136新schema与兼容旧标签分别核验；不要求返回体不存在的cross_group flag。\n'
 '独立校验新68=原45+2driver+21codec、全部源证明和sealed control/audit/result；不以标签授予新资格。\n'
 'top0800、原5e完整proof、343e旧subproof三层保持；新6region逆回5e，旧全c0 proof逐值不改。\n'
 '65顶层/70全部函数中，仅trim_component_contract与trim_component_input改动，其余63顶层函数逐字保留。\n'
 '原genuine3arg调用/整7INPUT/数学/owner图/namespace/alias/absence/完整动态roots/caps全保留；无module/class overlay。\n'
 '六实际构建凭据仍None，未来combined/INPUT/cold资格均未获得；未读取live作业产物、未导入或执行业务。\n')
print(json.dumps(dict(status=report['status'],draft_sha256=sha(out.encode()),report_sha256=sha((D/'REPORT.json').read_bytes()),regions=len(changes),source_pins=len(PINS),changed_functions=changed,actual_bindings_None=unknown)))

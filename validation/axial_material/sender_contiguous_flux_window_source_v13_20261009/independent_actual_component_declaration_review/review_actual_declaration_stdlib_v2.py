"""Frozen declaration/SOURCE reader only; never read live stages or run business."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import struct

D=Path('/private/tmp/axmat_v13_actual_component_PREP_declaration_independent_review_20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';AM=ROOT/'validation/axial_material'
OUT=ART/'axial-material-sender-contiguous-flux-window-build-v13-20261009'
SOURCE=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009'
TERM=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009'
OLD_OUT=ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
OLD_SOURCE=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'
PARENT=ART/'axial-material-rank1-factor-cache-build-20261007'
FACTORY=AM/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
DECL=OUT/'declaration.json'
PRIOR=Path('/private/tmp/axmat_v13_full86_READY_fact_binding_independent_review_20261009')
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 result={}
 for k,v in pairs:
  if k in result:raise ValueError('duplicate JSON key:'+k)
  result[k]=v
 return result
def load(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def identity(p):
 s=p.stat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def exact(a,b,path='root'):
 assert type(a) is type(b),(path,type(a).__name__,type(b).__name__)
 if isinstance(a,dict):
  assert list(a)==list(b),(path,'order')
  for k in a:exact(a[k],b[k],path+'.'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),path
  for i,(x,y) in enumerate(zip(a,b)):exact(x,y,path+'['+str(i)+']')
 elif isinstance(a,float):assert struct.pack('>d',a)==struct.pack('>d',b),path
 else:assert a==b,path
fixed=[DECL,FACTORY,OLD_OUT/'declaration.json',PARENT/'declaration.json',PRIOR/'REPORT.json',PRIOR/'actual_readonly_tool_return.json',OLD_SOURCE/'SPOT1P64.patch',OLD_OUT/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py']
source_names=sorted(p.name for p in SOURCE.iterdir())
assert len(source_names)==15
source_files=[SOURCE/name for name in source_names]
assert all(not p.is_symlink() and p.is_file() and p.stat().st_nlink==1 for p in source_files)
allfiles=fixed+source_files
before={str(p):identity(p) for p in allfiles};raw={str(p):p.read_bytes() for p in allfiles}
pins={str(p):dict(path=str(p),sha256=sha(raw[str(p)]),size_bytes=len(raw[str(p)]),identity=before[str(p)]) for p in allfiles}
assert pins[str(DECL)]['sha256']=='ccdbad6c0e6d767ee98b9e7287c5f3be8120604f57069730289bbd761b947b0f'
assert pins[str(DECL)]['size_bytes']==6895590
assert pins[str(FACTORY)]['sha256']=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert pins[str(PRIOR/'REPORT.json')]['sha256']=='2277ea49c293d4f04ea6502d840cdda59f69bc4463e622425015405182b4848b'
assert pins[str(PRIOR/'actual_readonly_tool_return.json')]['sha256']=='069b54f91f2dcc1552250d2d8a13c0219093cad943ba0d4fb9a700369023bffe'
d=load(raw[str(DECL)]);old=load(raw[str(OLD_OUT/'declaration.json')]);parent=load(raw[str(PARENT/'declaration.json')])
assert d['schema']=='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_DECLARATION_V13'
assert d['family']=='SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13'
assert d['source_root']==str(SOURCE)
assert d['source_inventory']['symlinks']=={} and d['source_directories']==[]
assert set(source_names)==set(d['source_inventory']['files'])
for name,wanted in d['source_inventory']['files'].items():
 assert pins[str(SOURCE/name)]['sha256']==wanted==d['files'][str(SOURCE/name)],name
caps={'original_stage_count':68,'complete_stage_count':86,'total_wall_seconds':1800,'stage_wall_seconds':600,
 'rss_cap_mib':512,'threads':1,'numeric_children_at_once':1,'retries':0,'archive_reserve_bytes':2*2**30,
 'artifact_budget_bytes':96*2**30,'min_free_bytes':8*2**30,'rank1_factor_cache_budget_bytes':536870912}
for k,v in caps.items():assert type(d[k]) is int and d[k]==v,k
for k in ['control_contract','stored_production_shape_cache_forecast','inherited_rank1_factor_cache_admission',
 'inherited_rank1_factor_cache_memory_admission','actual_failed_compact_memory_native_capture_evidence',
 'actual_failed_cold_AAA_evidence','actual_failed_native_capture_evidence','native_library_aliases',
 'numerical_loader_environment','resource_scope_contract','preserved_predecessors','future_actual_factor_cache_observer_required']:
 exact(d[k],old[k],k)
assert len(d['control_contract'])==61
for k in ['actual_full_FLU_entry_executed','transport_launched','original_accuracy_thresholds_changed',
 'coefficient_fitting','native_RSS_proof_obtained','AAA_accuracy_qualified','ABA_admitted']:
 assert d[k] is False,k
for k in ['white_closure_unchanged','physical_data_unchanged','radial_arithmetic_unchanged','angle_grid_unchanged',
 'fresh_cold_AAA_required','fresh_512MiB_native_capture_required','inherited_selector_source_controls_not_newly_executed']:
 assert d[k] is True,k

# Independently construct all12 arrays from original68 declaration and literal added recipes.
def retarget(token):return token.replace(str(OLD_SOURCE),str(SOURCE)).replace(str(OLD_OUT),str(OUT))
base=[[retarget(t) for t in cmd] for cmd in old['build_commands']]
assert len(base)==8
old_sender=str(PARENT/'build/FLU2DR64.o')
assert base[1].count(old_sender)==1
base[1][base[1].index(old_sender)]=str(OUT/'build/FLU2DR64.o')
common=base[0][:-4]
def compile_recipe(src,obj):return common+['-c',str(SOURCE/src),'-o',str(OUT/'build'/obj)]
libs=[str(ROOT/p) for p in ['lib/Darwin_arm64/libDragon.a','Trivac/lib/Darwin_arm64/libTrivac.a',
 'Utilib/lib/Darwin_arm64/libUtilib.a','Ganlib/lib/Darwin_arm64/libGanlib.a']]
white=str(ART/'axial-material-AAA-white-trace-angular-convergence-20261005/build/axmat_white_trace_model.o')
expected=base[:1]+[compile_recipe('FLU2DR64.f','FLU2DR64.o')]+base[1:]
expected += [compile_recipe('FLUSP64.original_reference_unit.f','FLUSP64.original_reference_unit.o'),
 compile_recipe('sender_window_controls.f90','sender_window_controls.o'),
 [common[0],'-O2','-march=native','-ffp-contract=off','-g',str(OUT/'build/sender_window_controls.o'),
  str(OUT/'build/FLU2DR64.o'),str(OUT/'build/FLUSP64.original_reference_unit.o'),str(OUT/'build/SPOT1P64.o'),
  white,*libs,'-o',str(OUT/'runtime/flusp64_window_observer_controls')]]
exact(d['build_commands'],expected,'all12buildrecipes')
assert d['production_link_command']==expected[2]
inverse=list(expected[2]); inverse[inverse.index(str(OUT/'build/SPOT1P64.o'))]=str(PARENT/'build/SPOT1P64.o')
inverse[inverse.index(str(OUT/'build/FLU2DR64.o'))]=old_sender;inverse[-1]=str(PARENT/'runtime/Dragon')
exact(inverse,parent['build_commands'][2],'original92productionrecipe')
assert str(ART/'axial-material-AAA-white-trace-cold-control-paths-20261004/build/SPOF64.o') in expected[2]
assert all('sender_window_controls.o' not in t and 'reference' not in t for t in expected[2])
assert str(OUT/'build/FLU2DR64.o') in expected[-1] and libs[-1] in expected[-1]
assert all('SPOF64.o' not in t and old_sender!=t for t in expected[-1])

c=d['control_contract'];exe=str(OUT/'runtime/rank1_factor_cache_last_cprime_trim_controls');keyexe=str(OUT/'runtime/keycodec_controls')
original_controls=[('positive',c['positive_command_args'])]
original_controls += [('negative_'+x['name'],x['args']) for x in c['negative_cases']+c['cap_negative_cases']]
for prefix in ['memory','dedup','factor']:
 original_controls.append((prefix+'_positive',c[prefix+'_positive_command_args']))
 original_controls += [(prefix+'_negative_'+x['name'],x['args']) for x in c[prefix+'_negative_cases']]
original_controls.append(('keycodec_positive',c['keycodec_positive_command_args']))
original_controls += [('keycodec_negative_'+x['name'],x['args']) for x in c['keycodec_negative_cases']]
assert len(original_controls)==59
contract=load(raw[str(SOURCE/'sender_control_contract.json')])
exact(contract,d['sender_control_contract'],'whole_sender_control_contract')
steps=[]
for i,cmd in enumerate(expected):steps.append(dict(index=i,label='build/build_'+str(i).zfill(2),command=cmd,expected_returncode=0))
for name,args in original_controls:
 steps.append(dict(index=len(steps),label='controls/'+name+'/execute',command=[keyexe if name.startswith('keycodec_') else exe,*args],expected_returncode=23 if name.startswith('keycodec_negative_') else 0))
for case in contract['cases']:
 steps.append(dict(index=len(steps),label='sender_controls/'+case['name']+'/execute',
 command=[str(OUT/'runtime/flusp64_window_observer_controls'),*case['args']],expected_returncode=case['expected_returncode']))
steps.append(dict(index=len(steps),label='audit/audit',command=[d['build_python_executable'],str(FACTORY),'audit-build','--sha256',pins[str(DECL)]['sha256']],expected_returncode=0))
assert len(steps)==86 and len(set(s['label'] for s in steps))==86
assert [s['expected_returncode'] for s in steps].count(1)==4
assert [s['expected_returncode'] for s in steps].count(23)==20

f=d['complete_archive_forecast'];oldf=old['complete_archive_forecast']
for k,v in oldf.items():exact(f[k],([str(SOURCE),str(OUT)] if k=='complete_scope_roots' else v),'forecast.'+k)
source_sizes={name:pins[str(SOURCE/name)]['size_bytes'] for name in
 ['FLU2DR64.f','FLUSP64.original_reference_unit.f','sender_window_controls.f90','sender_patch_helper.py',
 'sender_source_patch_proof.json','sender_source_only_INPUT.json','sender_control_contract.json','sender_controls_auditor.py']}
exact(f['sender_exact_additional_SOURCE_file_bytes'],source_sizes,'sender_source_sizes')
raw_bytes=sum(r['size_bytes'] for case in contract['cases'] for r in case['raw_files'])
assert raw_bytes==f['sender_exact_additional_control_raw_bytes']==288241824
assert sum(source_sizes.values())==f['sender_exact_additional_SOURCE_bytes']==140877
assert f['sender_manifest_rows']==22 and f['sender_manifest_json_allowance_bytes']==22*2048
assert f['forecast_complete_with_sender_bytes']==f['forecast_complete_bytes']+raw_bytes+sum(source_sizes.values())+22*2048==1847749501
assert f['forecast_complete_with_sender_bytes']<2*2**30 and f['nonraw_binary_diff_watch_log_and_metadata_allowance_bytes']==2**30

sender=d['sender_source_admission'];admission=load(raw[str(SOURCE/'source_admission.json')])
exact(sender,admission['sender_window_source_admission'],'whole_sender_admission')
exact(contract,admission['sender_wrapper_control_contract'],'whole_sender_contract_SOURCE')
assert raw[str(SOURCE/'FLU2DR64.f')]==sender['sender_text'].encode()
assert raw[str(SOURCE/'FLUSP64.original_reference_unit.f')]==sender['reference_wrapper_text'].encode()
assert admission['sole_new_production_objects']==['SPOT1P64.o','FLU2DR64.o']
assert admission['actual_full_FLU_entry_executed'] is False and admission['scientific_qualification'] is False
oldinventory=old['source_inventory']['files']
for name,wanted in oldinventory.items():
 if name not in ('source_admission.json','SPOT1P64.patch'):assert d['source_inventory']['files'][name]==wanted,name
assert raw[str(OLD_SOURCE/'SPOT1P64.patch')].replace(str(OLD_SOURCE).encode(),str(SOURCE).encode())==raw[str(SOURCE/'SPOT1P64.patch')]
assert raw[str(OLD_OUT/'runtime/run_bounded_dragon.py')]==raw[str(OUT/'runtime/run_bounded_dragon.py')]
assert pins[str(OUT/'runtime/run_bounded_dragon.py')]['sha256']==d['files'][str(OUT/'runtime/run_bounded_dragon.py')]
private_replaced={str(OLD_OUT/'runtime/run_bounded_dragon.py')}|{str(OLD_SOURCE/name) for name in oldinventory}
missing={p:sha256 for p,sha256 in old['files'].items() if d['files'].get(p)!=sha256}
assert set(missing)==private_replaced
assert all(d['files'][retarget(p)]==s for p,s in missing.items() if not p.endswith(('/source_admission.json','/SPOT1P64.patch')))
assert d['files'][str(FACTORY)]==pins[str(FACTORY)]['sha256']
for p,s in sender['source_inputs'].items():assert d['files'][p]==s,p
assert set(old['resource_roots']).issubset(d['resource_roots'])
assert {str(SOURCE),str(OUT),str(TERM)}.issubset(d['resource_roots'])
r=d['resources_before'];assert r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30
assert 0<=r['artifact_bytes']<96*2**30 and r['disk_free_bytes']>=8*2**30
assert r['declared_resource_roots']==d['resource_roots']
assert set(d['resource_roots']).issubset(r['resource_roots'])
ext=d['actual_external_terminal_return_contract']
assert ext['record_producer']=='root' and ext['actual_tool_exit_zero_required'] is True
assert ext['actual_run_command']==[d['build_python_executable'],str(FACTORY),'run-build','--sha256','__DECLARATION_SHA256__']
assert ext['tail_fields']==['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']
assert source_names==sorted(p.name for p in SOURCE.iterdir())
assert before=={str(p):identity(p) for p in allfiles}
D.mkdir(parents=True,exist_ok=True)
evidence=dict(schema='AXMAT_V13_ACTUAL_DECLARATION_COMPLETE_STATIC_METADATA_EVIDENCE_V1',
 frozen_file_fullSHA_and_7identity=pins,full86_stage_plan=steps,
 original8_build_mapping=[0,2,3,4,5,6,7,8],original59_controls_complete_order=True,
 dropped_previous_private_paths_and_preserved_new_copies=missing,
 production_complete_recipe_inverse= inverse,complete_actual_forecast=f,
 scope_notes=['This component declaration has the complete original61-key control/input contract and full source provenance; no standalone historical INPUT_SPECS whole7 phase is invoked by this component PREP.',
 'Declaration files12553 is an exact declared fullmap comparison; not a new12553-file or35GB wholehash claim.',
 'Dynamic resource snapshot belongs to PREP; live RUN changing roots are not asserted terminal or remeasured here.'])
with (D/'complete_declaration_stage_recipe_and_source_evidence.json').open('x') as stream:json.dump(evidence,stream,indent=2,allow_nan=False);stream.write('\n')
report=dict(schema='AXMAT_V13_ACTUAL_COMPONENT_PREP_DECLARATION_INDEPENDENT_REVIEW_V1',status='PASS_DECLARATION_PLAN_ONLY',
 declaration=pins[str(DECL)],factory=pins[str(FACTORY)],all12_build_recipes_independently_equal=True,
 all86_stage_labels_commands_planned=True,original68_stage_scope_complete=True,
 complete_original61_key_control_input_contract_type_order_floatbits_equal=True,source15_fullSHA_7identity_stable=True,
 production_realSPOF_and_twoobject_full_inverse=True,unit_observer_isolated_actual_fullsender_and_realGANLIB=True,
 original_caps_environment_physics_shape_budget_unchanged=True,full_forecast_bytes=1847749501,
 original2GiB_margin_bytes=2*2**30-1847749501,declared_file_pin_count=len(d['files']),
 original_nonprivate_input_filepins_all_retained=True,old_declared_roots_all_retained=True,
 actual_prepare_tool_facts_as_supplied_by_Root=dict(initial_chunk_id='16552f',session_id=17322,terminal_chunk_id='cdf07a',exit_code=0,closed=True),
 source_plan_is_not_actual86_stage_success=True,live_RUN_not_polled=True,live_stages_not_read=True,
 standalone_whole7_historical_INPUT_execution_not_claimed=True,
 source_blockers=[],business_imported=False,candidate_called=False,compile_or_fixture_executed=False,project_written=False,
 component_RUN_success=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 evidence_files=['complete_declaration_stage_recipe_and_source_evidence.json'],actual_readonly_tool_terminal_return=None)
with (D/'REPORT.json').open('x') as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
with (D/'REPORT.txt').open('x') as stream:stream.write('真实组件 PREP 声明计划独审通过：完整12条构建、86标签/命令计划与独立原68映射一致；原61字段输入/控制契约、来源、物理与预算完整保持。15 SOURCE文件全SHA/7身份稳定，生产只换两个完整对象和输出并整逆原recipe；真实SPOF与观察器单元链接隔离。完整预测1,847,749,501B在原2GiB内。未读取当前变化阶段，未轮询或执行业务；实际86阶段执行、Root退出、seal与准入仍等待真实终态。此component PREP不声称新whole7历史INPUT阶段执行，不授RSS/native/AAA/ABA信用。\n')
print(json.dumps(dict(status=report['status'],REPORT_path=str(D/'REPORT.json'),REPORT_sha256=sha((D/'REPORT.json').read_bytes()),source15_fullSHA_and_7identity_stable=True,stageplan86=True,source_blockers=[])))

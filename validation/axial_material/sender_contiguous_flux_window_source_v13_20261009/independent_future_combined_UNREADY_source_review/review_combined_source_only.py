"""STDlib AST/byte/read-only audit, no business module or draft calls."""
import ast
import hashlib
import json
from pathlib import Path
import struct

D=Path('/private/tmp/axmat_v13_sender_window_combined_source_independent_review_20261009')
CAND=Path('/private/tmp/axmat_v13_sender_window_graph_table_combined_source_draft_20261009')
AM=Path('/Users/wen/spot/validation/axial_material');ART=Path('/Users/wen/spot/validation/artifacts')
NEW=CAND/'prepare_sender_window_graph_table_combined_runtime_v13.py'
OLD=AM/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
NEW_SHA='c0644107311d63703d323ad210e32064ad9f4dd5f0517e4db49aa3a072c4f327'
OLD_SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
HELPERS={
 'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py':'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28',
 'combined_runtime_typed_specs_codec.py':'758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69',
 'combined_runtime_current_predicates_final_private_last_uses_20261009.py':'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19',
 'combined_runtime_historical_input_checks.py':'86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e',
 'combined_runtime_current_ordinary_path_checks.py':'47e7f9eb2e7ff89e96c30b91f98a25d37d66d82a029dcfbf4845c8f5968482d5'}
OTHER={AM/'combined_runtime_complete_historical_input_specs_20261007.json':'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa',
 AM/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py':'d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'}
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate key: '+k)
  d[k]=v
 return d
def load(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def identity(p):
 s=p.stat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
files=[NEW,OLD,CAND/'composition_regions.json',CAND/'source_complete_inverse_proof.json',CAND/'REPORT.json',
 CAND/'actual_source_tool_terminal_returns.json',CAND/'manifest.json',
 ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009/audit/controls.json',
 ART/'axial-material-rank1-factor-cache-build-20261007/declaration.json',
 AM/'sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json']
files+=list(OTHER)+[AM/name for name in HELPERS]
before={str(p):identity(p) for p in files};raw={str(p):p.read_bytes() for p in files}
pins={str(p):dict(path=str(p),sha256=sha(raw[str(p)]),size_bytes=len(raw[str(p)]),identity=before[str(p)]) for p in files}
assert pins[str(NEW)]['sha256']==NEW_SHA and pins[str(OLD)]['sha256']==OLD_SHA
for p,want in OTHER.items():assert pins[str(p)]['sha256']==want,str(p)
for name,want in HELPERS.items():assert pins[str(AM/name)]['sha256']==want,name
new=raw[str(NEW)].decode();old=raw[str(OLD)].decode();nt=ast.parse(new);ot=ast.parse(old)
def defs(t,s):
 d={};lines=s.splitlines(keepends=True)
 def walk(n,prefix=''):
  for x in ast.iter_child_nodes(n):
   if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
    key=prefix+x.name;d[key]=(x,''.join(lines[x.lineno-1:x.end_lineno]));walk(x,key+'.')
   else:walk(x,prefix)
 walk(t);return d
nd,od=defs(nt,new),defs(ot,old)
assert len(od)==70 and len(nd)==76
changed=sorted(k for k,v in od.items() if nd[k][1]!=v[1])
assert changed==sorted(['require_ready','combined_link_command','trim_component_contract','trim_component_input',
 'prepare_build','declaration_admission','binary_audit','production_admission','current_new_owned_paths'])
unchanged=sorted(set(od)-set(changed));assert len(unchanged)==61
added=sorted(set(nd)-set(od));assert len(added)==6
assert not any(isinstance(x,ast.ClassDef) for x in ast.walk(nt))
required_unchanged=['strict_json_bytes','record_actual_trim_component','graph_input_bindings','original_prep_input',
 'minimal_live_specs','current_input_predicates','create_complete_input_graph','complete_input_phase',
 'failed_prepare_input','check_failed_prepare_phase','modules','DynamicHistoryResources','resources_for',
 'supervisor_constructor_preflight','expected_supervisor_constructor','environment','stage_labels','stage_commands',
 'check_watch','audit_build','run_build','external_terminal','prepare_terminal_admission']
for name in required_unchanged:assert nd[name][1]==od[name][1],name
regions=load(raw[str(CAND/'composition_regions.json')]);assert len(regions)==32
inverse=new;proof=[]
for e in reversed(regions):
 assert inverse.count(e['after'])==e['count'],e['name']
 inverse=inverse.replace(e['after'],e['before'],e['count'])
 proof.append(dict(name=e['name'],count=e['count'],before_sha256=sha(e['before'].encode()),after_sha256=sha(e['after'].encode())))
assert inverse==old
def constants(t):
 d={}
 for x in t.body:
  if isinstance(x,ast.Assign):
   for target in x.targets:
    if isinstance(target,ast.Name):d[target.id]=x.value
    elif isinstance(target,ast.Tuple) and isinstance(x.value,ast.Tuple):
     assert len(target.elts)==len(x.value.elts)
     for a,b in zip(target.elts,x.value.elts):
      assert isinstance(a,ast.Name);d[a.id]=b
 return d
c,oc=constants(nt),constants(ot)
for name in ['INPUT_SPECS','INPUT_SPECS_SHA','INPUT_HELPERS','BODY_BINDING','THREAD_KEYS','TAIL_FIELDS',
 'TOTAL_WALL','STAGE_WALL','RSS','RESERVE','HISTORY_CAP','FREE_FLOOR','HISTORY_POLICY','BOUNDED','BOUNDED_SHA',
 'TRIM_LAST_CPRIME_KERNEL_SHA','TRIM_FACTOR_KERNEL_SHA','TRIM_KERNEL_SHA','TRIM_COMPLETE_C0_PROOF_SHA',
 'TRIM_IDENTITY_CONTRACT_SHA','TRIM_IDENTITY_EDITS_SHA','TRIM_IDENTITY_RETAINED_SOURCE_SHA']:
 assert ast.dump(c[name],include_attributes=False)==ast.dump(oc[name],include_attributes=False),name
unknown=['TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','SENDER_OBJECT_SHA']
for name in unknown:assert ast.literal_eval(c[name]) is None,name
assert ast.literal_eval(c['DRAFT_STATUS']).startswith('UNREADY')
guard=nd['require_ready'][1]
assert all(name in guard for name in unknown) and 'FORMAL_FACTORY' in guard and 'TMP draft cannot perform a business action' in guard
assert ast.literal_eval(c['TRIM_SCHEMA'])=='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_PRODUCTION_RUNTIME_INPUT_ADMISSION_V13'
assert ast.literal_eval(c['TRIM_ADMISSION'])=='SENDER_CONTIGUOUS_FLUX_WINDOW_RUNTIME_INPUT_ONLY_V13'
assert ast.literal_eval(c['TRIM_FACTORY_SHA'])==OTHER[AM/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py']

# Literal30 cache-count body independently compared with sealed trueV11 metadata.
sender_node=nd['sender_component_contract'][0]
literal_counts=next(x.value for x in sender_node.body if isinstance(x,ast.Assign)
 and any(isinstance(t,ast.Name) and t.id=='original68' for t in x.targets))
assert isinstance(literal_counts,ast.Call) and isinstance(literal_counts.func,ast.Name) and literal_counts.func.id=='dict'
counts={k.arg:ast.literal_eval(k.value) for k in literal_counts.keywords}
actual_old=load(raw[str(ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009/audit/controls.json')])
assert len(counts)==30 and counts==actual_old['counts'] and counts['actual_total_unit_kernel_invocations']==2710
contract=load(raw[str(AM/'sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json')])
assert contract['planned_counts_not_actual']['wrapper_calls_total']==48
assert contract['planned_counts_not_actual']['observer_calls_total']==34
assert contract['planned_counts_not_actual']['raw_files_total']==70 and contract['planned_counts_not_actual']['raw_bytes_total']==288241824
gate=nd['sender_component_contract'][1]
mandatory=['original_68_control_counts','expected86','total_declared_stages=86','sender_wrapper_observer_real_SPOT_credit',
 'real_SPOT_receiver_calls_in_this_observer_executable','raw_identity_snapshot','raw_sender_controls_receipt.json',
 'len(labels) != 86','len(negative23) != 20','len(negative1) != 4','liveness_group_cleanup',
 "watch['limit_failure'] is not None","watch['rss_cap_mib'] != 512","stage['wall_cap_seconds'] <= 600", 
 'sealed_path','expected_receipt','reference_wrapper_text','complete_inverse_byteexact','sender_outside_wrapper_byteexact',
 'schema','TRIM_SEAL_SHA','TRIM_SOURCE_ADMISSION_SHA','SENDER_OBJECT_SHA']
assert all(token in gate for token in mandatory)
assert 'sender_component_contract(value,d,admission,controls,audit,result,sealed)' in nd['trim_component_contract'][1]
assert 'sender_window_source_admission' in gate and "value['native_RSS_proof_obtained']" not in gate  # false flags live in shared list

# Independent model shows exactly three genuine changes and exact original92 restoration, no executable run.
parent=load(raw[str(ART/'axial-material-rank1-factor-cache-build-20261007/declaration.json')])
oldlink=parent['build_commands'][2]
kernel=str(ART/'axial-material-rank1-factor-cache-build-20261007/build/SPOT1P64.o')
oldsender=str(ART/'axial-material-rank1-factor-cache-build-20261007/build/FLU2DR64.o')
newkernel=str(ART/'axial-material-sender-contiguous-flux-window-build-v13-20261009/build/SPOT1P64.o')
newsender=str(ART/'axial-material-sender-contiguous-flux-window-build-v13-20261009/build/FLU2DR64.o')
physical=str(ART/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o')
newout=str(ART/'axial-material-sender-window-graph-table-combined-runtime-v13-20261009/runtime/Dragon')
archive='/Users/wen/spot/lib/Darwin_arm64/libDragon.a'
model=list(oldlink);assert model.count(kernel)==model.count(oldsender)==model.count(archive)==1
model[model.index(kernel)]=newkernel;model[model.index(oldsender)]=newsender
model.insert(model.index(archive),physical);model[-1]=newout
restore=list(model);restore.remove(physical);restore[restore.index(newkernel)]=kernel;restore[restore.index(newsender)]=oldsender;restore[-1]=oldlink[-1]
assert restore==oldlink and all(x not in str(model) for x in ['sender_window_controls.o','FLUSP64.original_reference_unit.o','candidate_unit'])
assert any(t.endswith('/SPOF64.o') for t in model)
assert "sole_object_changes=['SPOT1P64.o','SPOASM.o','FLU2DR64.o']" in nd['combined_link_command'][1]
assert "command[command.index(str(old_sender))]=str(SENDER_OBJECT)" in nd['combined_link_command'][1]
assert 'flusp64_reference' in nd['binary_audit'][1] and 'sender_window_controls' in nd['binary_audit'][1]
assert 'flusp64_' in nd['binary_audit'][1] and 'spof64_' in nd['binary_audit'][1]
stages=nd['stage_labels'][0].body[0].value
assert ast.literal_eval(stages)==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
assert before=={str(p):identity(p) for p in files}
D.mkdir(parents=True,exist_ok=True)
evidence=dict(schema='AXMAT_V13_COMBINED_SOURCE_FULL_INVERSE_AND_INTERFACE_EVIDENCE_V1',fresh_pins=pins,
 complete32_inverse_regions=list(reversed(proof)),all76_definition_segments={k:dict(sha256=sha(v[1].encode()),line=v[0].lineno) for k,v in nd.items()},
 original70_modified=changed,original70_byteexact=unchanged,added6=added,
 whole_7_INPUT_graph_strict_tablecode_e8_math_MRO_source_byteexact=required_unchanged,
 original30_cache_count_dict=counts,independently_modeled_combined_link=model,
 modeled_full_inverse=restore,unknown_component_success_pins=unknown,
 limits_and_scope=['No component live stage or Root handle was read or polled.',
 'Entire historical specs19MB was only fullSHA pinned, not run as a whole INPUT phase.',
 'All new component7success pins remainNone and new combinedsourceUNREADY; no future count or kernelobject was inferred.'])
with (D/'complete_static_source_inverse_and_INTERFACE_evidence.json').open('x') as f:json.dump(evidence,f,indent=2,allow_nan=False);f.write('\n')
report=dict(schema='AXMAT_V13_SENDER_WINDOW_GRAPH_TABLE_COMBINED_SOURCE_INDEPENDENT_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY',
 candidate=pins[str(NEW)],mother=pins[str(OLD)],whole32region_inverse=True,
 original_definitions=70,retained_original_byteexact=61,changed_gate_and_interface_definitions=9,added_definitions=6,
 full_historical_7INPUT_and_original5stages_source_retained=True,all5_helpers_e8_and_original2cad_freshSHA=True,
 original64MiB_graph_cap_unchanged=True,third_sender_override_with_physical_and_kernel_full92_inverse=True,
 realSPOF_retained_unit_observer_excluded=True,full86_component_and_original68count_body_required=True,
 original_realSPOT2710_and_wrapper48_credit_distinct=True,full70raw288241824_sealed_source_and_7ID_gate_required=True,
 source_before_after_7identity_equal=True,all7_component_actual_success_pins_None=True,
 original_caps_MRO_physics_math_unchanged=True,source_blockers=[],
 business_imported=False,candidate_called=False,compile_or_fixture_executed=False,Root_job_polled=False,
 project_written=False,component_success_claimed=False,combined_build_success_claimed=False,
 native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 evidence_files=['complete_static_source_inverse_and_INTERFACE_evidence.json'],actual_readonly_tool_return=None)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with (D/'REPORT.txt').open('x') as f:f.write('V13 combined 源稿独审通过，保持 UNREADY。32 区域整逆真实 V12；70 原定义中 61 字节保持、9 为门/接线变化、新增 6 含 nested。完整七历史 INPUT、e8 lossless graph、原 64MiB 读界、5阶段/MRO/物理与原预算保留。新sender为第三生产override，连同kernel/physical与输出整逆原92；真实SPOF保留，observer/reference不进生产。完整86 component、原30字段68计数/2710真kernel与48stub分域及70raw/7身份/seal门保持。7成功pins尚 None，未读正在运行的stage、未poll或执行业务；不授component/combined/RSS/native/AAA/ABA通过信用。\n')
print(json.dumps(dict(status=report['status'],REPORT_path=str(D/'REPORT.json'),REPORT_sha256=sha((D/'REPORT.json').read_bytes()),fullinverse32=True,source_before_after_identity_equal=True,unknown7None=True)))

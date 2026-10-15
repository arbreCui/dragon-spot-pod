import ast
import difflib
import hashlib
import json
import os
import stat
from pathlib import Path

D=Path('/private/tmp/axmat_v12_graph_table_cold_source_only_20261009')
M=Path('/private/tmp/axmat_v11_cold_component_input_consumer_source_only_20261009')
AM=Path('/Users/wen/spot/validation/axial_material');ART=AM.parent/'artifacts'
F12=AM/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
H12=AM/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
FN='prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
CN='cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
BN='cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
MF='prepare_historical_input_owned_specs_physical_cross_group_identity_key_delta_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak_v11.py'
MC='cold_component_input_consumer_cross_group_identity_key_delta_own_pid_peak_v11.py'
MB='cold_owned_specs_cross_group_identity_key_delta_component_input_intake_binding_v11_20261009.json'
PINS={MF:'753abea4ba1b7b914f9f7655a43d99d0e57344388fdb9bb8cc56887805d9ffff',MC:'f5272f02091170a1a6b8b9279cb533271d1fcd2c070101f44e631aabfb60b5e0',MB:'1632c45342b40253a7b10736c481b70c2b515947ffabf9651f79c4d6f3331db7',
 'source_inverse_proof.json':'e6ed4db3f137f7c50a99f7e27184877a14392a9f8af3b321c1418a28e6e1a4c1'}
F12SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
H12SHA='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def ident(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
inputs=[*(M/name for name in PINS),F12,H12]
before={str(p):ident(p) for p in inputs}
texts={name:(M/name).read_text() for name in PINS}
for name,pin in PINS.items():assert sha(texts[name].encode())==pin
f12=F12.read_text();h12=H12.read_text();assert sha(f12.encode())==F12SHA and sha(h12.encode())==H12SHA
def assigns(s):return {n.targets[0].id:n for n in ast.parse(s).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
known={'ROOT':Path('/Users/wen/spot'),'ART':ART}
def literal_path(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name):return known[n.id]
 if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return literal_path(n.left)/literal_path(n.right)
 raise ValueError('not an explicitly permitted source path literal')
fa=assigns(f12)
combined={name:literal_path(fa[name].value) for name in ('SOURCE','OUT','TERMINAL','PREFIX')}
api_schema=combined['PREFIX']+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
intake=ART/'axial-material-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-evidence-20261009'
cold={
 'SOURCE':ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-source-v12-20261009',
 'OUTPUT':ART/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009',
 'COLD_TERMINAL':ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009',
 'CONTROL_TERMINAL':ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-controls-terminal-v12-20261009'}
schema='AXMAT_COLD_COMPLETE_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMPONENT_INPUT_INTAKE_V12'
common_identity=lambda p:repr(str(p))
def edit_python(old,changes,doc,basename_change=False):
 out=old;edits=[]
 def replace(name,a,b):
  nonlocal out
  assert out.count(a)==1,(name,out.count(a));out=out.replace(a,b,1);edits.append(dict(name=name,old=a,new=b))
 tree=ast.parse(old);replace('module source-only description',ast.get_source_segment(old,tree.body[0]),repr(doc))
 table=assigns(old)
 for name,new_rhs in changes.items():
  node=table[name];a=ast.get_source_segment(old,node);replace('identity assignment '+name,a,name+' = '+new_rhs)
 if basename_change:
  # These are the only function-body changes: SOURCE/runtime copies must use
  # the same new consumer basename used by normal_module; no class overlay.
  count=out.count(MC);assert count==3,count
  i=0
  while MC in out:
   offset=out.index(MC);line_start=out.rfind('\n',0,offset)+1;line_end=out.index('\n',offset)
   a=out[line_start:line_end];b=a.replace(MC,CN)
   replace('ordinary new consumer basename site '+str(i),a,b);i+=1
  assert i==2
 inverse=out
 for e in reversed(edits):assert inverse.count(e['new'])==1,(e['name'],inverse.count(e['new']));inverse=inverse.replace(e['new'],e['old'],1)
 assert inverse==old
 return out,edits
consumer_changes={'SCHEMA':repr(schema),'INTAKE_ROOT':common_identity(intake),'GRAPH_SOURCE_SHA':repr(H12SHA),'GRAPH_SOURCE':common_identity(H12),'API_SOURCE':common_identity(F12),'API_SOURCE_SHA':repr(F12SHA),'API_SCHEMA':repr(api_schema),'API_BUILD':common_identity(combined['OUT']),'API_SOURCE_ROOT':common_identity(combined['SOURCE']),'API_TERMINAL':common_identity(combined['TERMINAL'])}
factory_changes={**{name:common_identity(path) for name,path in cold.items()},'EXPERIMENT':repr(cold['SOURCE'].name),'FORMAL_FACTORY':common_identity(AM/FN),'COMBINED_FACTORY':common_identity(F12),'COMBINED_FACTORY_SHA':repr(F12SHA),'COMBINED_BUILD':common_identity(combined['OUT']),'COMBINED_TERMINAL':common_identity(combined['TERMINAL']/'terminal_return.json'),'COMBINED_RUNTIME':repr(str(combined['OUT']/'runtime/Dragon')),'COMBINED_SCHEMA':repr(api_schema),'PRIVATE_INPUT_CONSUMER':common_identity(AM/CN),'COMPONENT_INTAKE_DESCRIPTOR':common_identity(AM/BN),'INPUT_REUSE_SCHEMA':repr(schema),'CALLBACK_METADATA_SCHEMA':repr('AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12'),'SCHEMA':repr('AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_FACTORY_V12'),'DECL_TERMINAL_SCHEMA':repr('AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_DECLARATION_ACTUAL_TERMINAL_V12'),'COLD_TERMINAL_SCHEMA':repr('AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_ACTUAL_TERMINAL_V12')}
# Path constants historically used Path attributes or '/' composition; retain
# their exact Path type, except COMBINED_RUNTIME which is originally str.
consumer_path_keys={'INTAKE_ROOT','GRAPH_SOURCE','API_SOURCE','API_BUILD','API_SOURCE_ROOT','API_TERMINAL'}
factory_path_keys=set(cold)|{'FORMAL_FACTORY','COMBINED_FACTORY','COMBINED_BUILD','COMBINED_TERMINAL','PRIVATE_INPUT_CONSUMER','COMPONENT_INTAKE_DESCRIPTOR'}
for key in consumer_path_keys:consumer_changes[key]='Path('+consumer_changes[key]+')'
for key in factory_path_keys:factory_changes[key]='Path('+factory_changes[key]+')'
c,ce=edit_python(texts[MC],consumer_changes,'UNREADY V12 graph-table complete cold INPUT source-only identity candidate. Both strictly pinned graph readers decode the complete original graph. All genuine seven historical INPUT bodies, producerP14/analysisP12, physics, aliases, namespaces, OwnRSS MRO and budgets remain required. Only existing installed source identities are bound; future runtime/intake/cold success and observed counts remain None. No business or scientific qualification is conferred.')
f,fe=edit_python(texts[MF],factory_changes,'UNREADY V12 graph-table cold source-only identity candidate. The frozen V11 component0800 and5e/343e ancestor contract is retained. Complete historical INPUT, producerP14/analysisP12, physical basis, decks, genuine OwnRSS MRO/constructors, budgets and original closeout gates are unchanged. New combined/intake/cold success and counts are absent. Source identities alone do not authorize declaration or numerical work.',True)
old_binding=json.loads(texts[MB]);binding=json.loads(texts[MB]);binding['schema']=schema;binding['draft_status']='UNREADY_V12_GRAPH_TABLE_SOURCE_ONLY_NO_ACTUAL_NEW_SUCCESS_BINDING'
binding['actual_bounded_api_terminal_evidence']['path']=str(intake/'Root_terminal_return.json');binding['api_return']['path']=str(intake/'intake/admit.log')
binding['helper_sources']['graph']=dict(path=str(H12),sha256=H12SHA)
binding['complete_historical_input_graph']['path']=str(combined['OUT']/'input_graph.json');binding['binding_source']['path']=str(AM/CN)
# This field refers to the frozen V11 component, not the new V12 combined or
# cold runtime; its None value remains unbound rather than renaming ancestry.
assert binding['actual_V11_component_control_counts']is None
binding_edits=[]
new_binding=json.dumps(binding,indent=2)+'\n'
for key in old_binding:
 if old_binding[key]!=binding[key]:binding_edits.append(dict(key=key,old=old_binding[key],new=binding[key]))
inverse_binding=json.loads(new_binding)
for e in binding_edits:inverse_binding[e['key']]=e['old']
assert json.dumps(inverse_binding,indent=2)+'\n'==texts[MB]
outputs={CN:c,FN:f,BN:new_binding}
for name,raw in outputs.items():assert not (D/name).exists();(D/name).write_text(raw)
proofs={}
previous=json.loads(texts['source_inverse_proof.json'])
for name,mother,src,edits in ((CN,MC,c,ce),(FN,MF,f,fe)):
 old=texts[mother];ot=ast.parse(old);nt=ast.parse(src)
 def defs(text,tree):
  result={}
  def walk(nodes,prefix=''):
   for n in nodes:
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
     result[prefix+n.name]=ast.get_source_segment(text,n);walk(n.body,prefix+n.name+'.')
  walk(tree.body);return result
 od=defs(old,ot);nd=defs(src,nt);assert set(od)==set(nd)
 changed=[key for key in od if od[key]!=nd[key]]
 if name==CN:assert changed==[] and len(od)==27
 else:assert set(changed)=={'render_controller','declare'} and len(od)==55
 assert all(od[name]==nd[name] for name in od if name not in changed)
 normalized=src
 for e in reversed(edits):normalized=normalized.replace(e['new'],e['old'],1)
 assert normalized==old
 inherited=normalized
 for e in reversed(previous['proofs'][mother]['edits']):assert inherited.count(e['new'])==1;inherited=inherited.replace(e['new'],e['old'],1)
 assert sha(inherited.encode())==previous['proofs'][mother]['parent_sha256']
 old_assign=assigns(old);new_assign=assigns(src)
 old_none=[k for k,n in old_assign.items() if isinstance(n.value,ast.Constant) and n.value.value is None]
 known_source_fields={'API_SOURCE_SHA'} if name==CN else {'COMBINED_FACTORY_SHA'}
 still_none=[k for k in old_none if k not in known_source_fields]
 assert all(isinstance(new_assign[k].value,ast.Constant) and new_assign[k].value.value is None for k in still_none)
 for prefix in ('TRIM_','FUTURE_','EXPECTED_'):
  assert all(ast.get_source_segment(old,n)==ast.get_source_segment(src,new_assign[k]) for k,n in old_assign.items() if k.startswith(prefix))
 if name==FN:
  for k in ('BUDGETS','CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER','DECK_HOOK','CACHE_BUDGET_BYTES','ORIGINAL_COLD_RESERVE_BYTES','HOST','HOST_SHA','CONTROLS','CONTROLS_SHA','SCIPY_HELPER','SCIPY_HELPER_SHA'):
   assert ast.get_source_segment(old,old_assign[k])==ast.get_source_segment(src,new_assign[k])
 if name==CN:
  for k in ('SPECS','SPECS_SHA','THREADS','PYTHON','CODEC_SOURCE_SHA','CHECK_SOURCE_SHA','HISTORY_POLICY'):
   assert ast.get_source_segment(old,old_assign[k])==ast.get_source_segment(src,new_assign[k])
 proofs[name]=dict(parent_path=str(M/mother),parent_sha256=PINS[mother],candidate_sha256=sha(src.encode()),complete_inverse_byteexact=True,chained_inverse_to_genuine_V10_parent_sha256=sha(inherited.encode()),all_definitions=len(od),changed_definitions=changed,unchanged_definition_count=len(od)-len(changed),function_body_changes_only_new_ordinary_consumer_basename=bool(changed),all_future_success_count_inventory_unknown_None=still_none,known_installed_source_identity_bound_only=list(known_source_fields),edits=edits)
 (D/(name+'.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),src.splitlines(True),fromfile=str(M/mother),tofile=str(D/name))))
proofs[BN]=dict(parent_path=str(M/MB),parent_sha256=PINS[MB],candidate_sha256=sha(new_binding.encode()),complete_inverse_byteexact=True,changed_top_level_fields=binding_edits,all_original_unknown_null_fields_retained=True)
for key in old_binding:
 if old_binding[key]is None:assert binding[key]is None
for key in ('actual_bounded_api_terminal_evidence','api_return','complete_historical_input_graph','binding_source'):
 for subkey,value in old_binding[key].items():
  if value is None:assert binding[key][subkey]is None
helper_ast=ast.parse(h12)
helper_proof={}
for name in ('strict_json','_parse_strict_json_payload'):
 n=next(n for n in helper_ast.body if isinstance(n,ast.FunctionDef) and n.name==name);seg=ast.get_source_segment(h12,n)
 assert 'decode_canonical_file_table_storage(result, _consume=True)' in seg
 helper_proof[name]=dict(line=n.lineno,source_sha256=sha(seg.encode()),schema_gate_and_own_parsed_consume_present=True)
assert before=={str(p):ident(p) for p in inputs}
sourceproof=dict(schema='AXMAT_V12_GRAPH_TABLE_COLD_SOURCE_ONLY_IDENTITY_COMPLETE_INVERSE_V1',status='UNREADY_SOURCE_ONLY',proofs=proofs,known_installed_combined_factory=dict(path=str(F12),sha256=F12SHA,identity=before[str(F12)]),known_installed_graph_helper=dict(path=str(H12),sha256=H12SHA,identity=before[str(H12)],two_strict_decoding_wrappers=helper_proof),no_business_import_or_execution=True,no_project_write=True)
(D/'source_inverse_proof.json').write_text(json.dumps(sourceproof,indent=2)+'\n')
report=dict(schema='AXMAT_V12_GRAPH_TABLE_COLD_SOURCE_ONLY_IDENTITY_REVIEW_V1',status='UNREADY_SOURCE_ONLY_NO_BUSINESS_EXECUTION',files={name:dict(path=str(D/name),sha256=sha(raw.encode())) for name,raw in outputs.items()},source_inverse_proof=dict(path=str(D/'source_inverse_proof.json'),sha256=sha((D/'source_inverse_proof.json').read_bytes())),current_installed_source_identities_only=sourceproof['known_installed_combined_factory'],current_installed_graph_helper=sourceproof['known_installed_graph_helper'],prospective_cold_roots={name:str(path) for name,path in cold.items()},prospective_whole_INPUT_intake_root=str(intake),prospective_combined_roots={name:str(value) for name,value in combined.items()},expected_api_schema=api_schema,unchanged_frozen_V11_component_factory='f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e',unchanged_V11_top0800_and_5e343e_ancestors=True,all_whole_seven_INPUT_specs_math_and_original_budgets_unchanged=True,consumer_all_27_functions_byteexact=True,factory_53_of55_functions_byteexact_remaining_two_only_new_consumer_basename=True,genuine_OwnRSS_MRO_constructor_and_P14_P12_source_contracts_byteexact=True,original_RSS_MiB=512,original_bootstrap_axial_seconds=4200,original_total_cold_seconds=43200,unknown_success_count_inventory_fields_not_bound=True,future_actual_combined_PREP=None,future_actual_combined_seal=None,future_actual_combined_RUN_terminal=None,future_actual_bounded_whole_INPUT=None,future_actual_cold_declaration=None,future_actual_native_or_controls=None,actual_tool_terminal_receipt=None,business_module_imported=False,business_API_called=False,project_written=False,qualification=dict(standalone_whole_INPUT_success=False,native_RSS=False,AAA=False,ABA=False),limits=['Pure source identity retarget only; no live Root handle polled and no future result read.','Old legacy trim metadata and READY guard enum are deliberately inherited; no source label grants runtime qualification.','Only Root may bind actual freshly qualified witnesses/counts, change UNREADY and install these independent prospective paths.'])
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('V12 graph-table冷入口纯SOURCE身份草稿，全部保持UNREADY。\n三件新文件和四个新cold根，完整consumer27函数字节不变；factory55定义中仅render_controller/declare两处普通新consumer文件名传播，其余53原字节。\n新graph helper两个strict入口均可恢复完整原图，未改变任何whole7INPUT、物理、门槛、P14/P12、OwnRSS类/构造、512/4200/43200预算或V11组件0800及5e/343e祖先。\n只绑定已存在installed source5af/helper e8f；全部未来success、intake、cold source/receipt、count/inventory None。\n完整region逆向回冻结V11母本，再逆向到真实V10母函数字节；未导入/执行业务、未写项目、未轮询Root或读取未来产物。\n')
print(json.dumps(dict(status=report['status'],files=report['files'],proof_sha256=report['source_inverse_proof']['sha256'],report_sha256=sha((D/'REPORT.json').read_bytes()))))

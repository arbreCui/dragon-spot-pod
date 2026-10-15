"""Standard-library read-only evidence review. No business module execution."""
import ast
import hashlib
import json
import math
import stat
import struct
from pathlib import Path

D=Path('/private/tmp/axmat_v12_actual_cold_declare_and_prepare_readonly_review_20261009')
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
W=ART/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009'
S=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-source-v12-20261009'
T=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009'
CT=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-controls-terminal-v12-20261009'
R=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
F=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
CAPS=dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,
 control_archive_reserve_bytes=67108864,cold_total_seconds=43200,min_free_bytes=8589934592,
 history_cap_bytes=103079215104,threads=1,children_at_once=1,retries=0)
checked={}
parent_checked=set()

def regular(p):
 p=Path(p)
 assert p.is_absolute() and '..' not in p.parts and str(p)==str(p.resolve()), str(p)
 for q in (p,*p.parents):
  if str(q) not in parent_checked:
   st=q.lstat();assert not stat.S_ISLNK(st.st_mode),str(q)
   assert stat.S_ISREG(st.st_mode) if q==p else stat.S_ISDIR(st.st_mode),str(q)
   parent_checked.add(str(q))
 return p

def pin(p,sha=None):
 p=regular(p)
 if str(p) not in checked:
  with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
  checked[str(p)]={'sha256':h,'size_bytes':p.stat().st_size}
 if sha is not None: assert checked[str(p)]['sha256']==sha,(str(p),checked[str(p)]['sha256'],sha)
 return {'path':str(p),'sha256':checked[str(p)]['sha256']}

def read(p,sha=None):
 pin(p,sha)
 def pairs(rows):
  d={}
  for k,v in rows: assert k not in d;d[k]=v
  return d
 def bad(x):raise AssertionError(x)
 return json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_constant=bad)

def exact(a,b):
 assert type(a) is type(b),(type(a),type(b))
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:exact(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):exact(x,y)
 elif isinstance(a,float):assert struct.pack('!d',a)==struct.pack('!d',b)
 else:assert a==b,(a,b)

def segment(p,name,kind):
 text=Path(p).read_text();nodes=[n for n in ast.parse(text).body if isinstance(n,kind) and n.name==name]
 assert len(nodes)==1
 return ast.get_source_segment(text,nodes[0]),nodes[0]

def desc(d):
 assert set(d)=={'path','sha256'}
 assert isinstance(d['sha256'],str) and len(d['sha256'])==64 and set(d['sha256'])<=set('0123456789abcdef') and d['sha256']!='0'*64
 return pin(d['path'],d['sha256'])

b=read(W/'own_rss_binding.json','ec966407b2a157d762c582241b82cc9c962ca93ae437e48289ef349c01ea4d35')
m=read(S/'rank1_factor_cache_admission.json','1087874e47a9638ce7c77416d045dc364da38a5335d94b6535cd1781b4967520')
p=read(W/'prepared.json','ec3db7fcf10c2fc4b63b6dc89283f29b2067dc97aebb29b67e5aaa1731b5429c')
sd=read(S/'declaration.json','758db9578a8b259afd8da2faf1f50614e6d4f581a0922d22083824350fdfd75d')
ss=read(S/'factory_seal.json','d182259bb17b580bbe45fe1853168c188515ef0b5ef654cfe7a72b668c32f3d5')
decl=read(T/'declaration_terminal_return.json','66c0647d69ba276460a84a09cee6502b272ded07c5b24b5f3509a64ae47d0b2c')
api=read(m['whole_component_body_source']['path'],'65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536')
full_admission=read(R/'Root_actual_bounded_whole_input_independent_admission.json','c47dfa70b1bf610f3ef88049d1f33491815aed4284c182baa2650b0647c5963f')
assert len(api)==65 and len(api['actual_components'])==7
whole=api['actual_components']
seven=dict(original92=whole['original92'],memory438=whole['dedup']['inherited_rank1_factor_cache_memory_admission'],
 physical=whole['physical'],dedup=whole['dedup'],capture=whole['capture'],combined=api,
 last_cprime_trim=api['actual_last_cprime_trim_admission'])
exact(b['actual_component_returns'],seven)
for key,name in (('inherited_rank1_cache_admission','original92'),('inherited_physical_admission','physical'),
 ('inherited_dedup_admission','dedup'),('original_operator_capture_dependency','capture'),
 ('inherited_rank1_factor_cache_memory_admission','memory438')):exact(api[key],seven[name])
assert set(b['actual_component_returns'])=={'original92','memory438','physical','dedup','capture','combined','last_cprime_trim'}
assert api['AAA_accuracy_qualified'] is False and api['ABA_admitted'] is False
assert b['schema']=='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_OWN_RSS_BINDING_V1'
exact(b['caps'],CAPS)
assert b['work_root']==str(W) and b['control_terminal_root']==str(CT)
assert b['scientific_qualification'] is False and b['module_global_or_class_overlay'] is False
assert b['canonical_controller_name']=='production_runner'
exact(b['producer_environment'],read(S/'analysis_environment.json'))
exact(b['resource_info'],{k:p[k] for k in ('artifact_root','resource_roots','case_spec')})
exact(b['input_declaration_terminal_evidence'],pin(T/'declaration_terminal_return.json'))
assert p['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in p
expected=dict(m['files'])
def add(path,sha):
 path=str(path)
 if path in expected:assert expected[path]==sha
 expected[path]=sha
for name,sha in p['local_files'].items():add(W/name,sha)
for name,sha in ss['files'].items():add(S/name,sha)
for path in (S/'factory_seal.json',W/'prepared.json',F,T/'declaration_terminal_return.json'):
 item=pin(path);add(item['path'],item['sha256'])
for key in ('full_stdout','full_stderr'):
 item=desc(decl[key]);add(item['path'],item['sha256'])
exact(b['files'],expected)
assert len(m['files'])==38468 and len(b['files'])==38524
supplement=set(b['files'])-set(m['files']);assert len(supplement)==56
for path,sha in b['files'].items():
 assert Path(path).is_absolute() and '..' not in Path(path).parts
 assert isinstance(sha,str) and len(sha)==64 and set(sha)<=set('0123456789abcdef') and sha!='0'*64
for path in supplement:pin(path,b['files'][path])
for name,sha in ss['files'].items():pin(S/name,sha)
assert len(b['runtime_namespace']['files'])==31 and b['runtime_namespace']['directories']==[]
actual_runtime={q.name:pin(q)['sha256'] for q in (W/'runtime').iterdir()}
exact(actual_runtime,b['runtime_namespace']['files'])
exact(actual_runtime,{Path(name).name:sha for name,sha in p['local_files'].items() if name.startswith('runtime/')})
assert len(b['runtime_module_owners'])==7 and len(b['module_owners'])==391
for owners in (b['runtime_module_owners'],b['module_owners']):
 for name,item in owners.items():
  desc(item);assert b['files'][item['path']]==item['sha256']
  assert Path(item['path']).is_relative_to(ROOT/'validation')
for name,item in b['runtime_module_owners'].items():assert item['path']==str(W/'runtime'/(name+'.py'))
assert b['module_owners']['production_runner']==b['controller']
assert b['module_owners']['qualify_refined_AAA_layered_full']==b['own_rss_source']
assert b['module_owners']['__main__']==b['controls_source']
assert len(b['tested_guard_files'])==6
for item in b['tested_guard_files']:desc(item);assert b['files'][item['path']]==item['sha256']
for key in ('controller','host','controls_source','bounded_helper','serial_baseline','own_rss_source','guard_factory','resource_class_source'):
 desc(b[key]);assert b['files'][b[key]['path']]==b[key]['sha256']
controller=Path(b['controller']['path']);baseline=Path(b['serial_baseline']['path']);own=Path(b['own_rss_source']['path'])
exact(segment(controller,'SerialExecutor',ast.ClassDef)[0],segment(baseline,'SerialExecutor',ast.ClassDef)[0])
for name in ('resource_monitor','qualify_aba'):
 exact(segment(controller,name,ast.FunctionDef)[0],segment(baseline,name,ast.FunctionDef)[0])
ownclass=segment(own,'OwnRSSSerialExecutor',ast.ClassDef)[1]
assert [ast.unparse(n) for n in ownclass.bases]==['SerialExecutor']
assert [n.name for n in ownclass.body if isinstance(n,ast.FunctionDef)]==['_process']
host=Path(b['host']['path']);mrotext=segment(host,'source_mro_proof',ast.FunctionDef)[0]
for literal in ('full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,)',
 'full.SerialExecutor is not c.SerialExecutor','full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__',
 'full.OwnRSSSerialExecutor.execute is not c.SerialExecutor.execute',
 'c.__name__ != \'production_runner\'','actual_original_process_globals_identity=True','module_global_or_class_overlay=False'):
 assert literal in mrotext,literal
for name in ('bind_controller','binding_admission','resource_provenance'):
 assert segment(host,name,ast.FunctionDef)[0]
br=read(R/'Root_actual_cold_prepare_binding_tool_terminal_return.json')
bi=read(R/'Root_actual_cold_prepare_binding_tool_input.json')
for key in ('actual_initial_tool_result','actual_terminal_tool_result'):exact(br[key],bi[key])
exact(br['actual_tool'],dict(initial_chunk_id='82e530',session_id=83082,terminal_chunk_id='796d5b',exit_code=0))
assert br['session_closed'] is True and br['actual_tool_terminal_return_observed'] is True
exact(br['binding'],pin(W/'own_rss_binding.json'))
for key in ('full_stdout','full_stderr'):desc(br[key])
assert Path(br['full_stderr']['path']).stat().st_size==0
binding_output=read(br['full_stdout']['path'])
assert binding_output['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT'
exact(binding_output['binding'],pin(W/'own_rss_binding.json'))
proof=binding_output['actual_source_identity']
assert proof['actual_direct_bases']==['production_runner.SerialExecutor']
for key in ('inherited_original_init','inherited_original_execute','entire_SerialExecutor_source_byte_exact','actual_original_process_globals_identity'):
 assert proof[key] is True
assert proof['module_global_or_class_overlay'] is False and proof['new_binding_fixture_pass_claimed'] is False
assert set(proof['actual_compiled_callable_sha256'])=={'OwnRSS._process','__init__','_process','check_dragon_log','dump_json','execute','qualify_aba','resource_monitor','run','sha256','write_new'}
for sha in proof['actual_compiled_callable_sha256'].values():assert len(sha)==64 and set(sha)<=set('0123456789abcdef')
cr=read(R/'Root_actual_cold_controls_tool_terminal_return.json')
ci=read(R/'Root_actual_cold_controls_tool_input.json')
for key in ('actual_initial_tool_result','actual_terminal_tool_result'):exact(cr[key],ci[key])
tool=dict(initial_chunk_id='45095a',session_id=4925,terminal_chunk_id='1a4690',exit_code=0)
exact(cr['actual_tool'],tool)
assert cr['session_closed'] is True and cr['actual_tool_terminal_return_observed'] is True
ct=read(CT/'terminal_return.json','5acffc484f1f78bc5df6520d98cc97f0234161ae8185b863384679d032a9e583')
assert ct['schema']=='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_ACTUAL_TERMINAL_V1'
assert ct['record_producer']=='root' and ct['returncode']==0 and ct['scientific_qualification'] is False
assert ct['actual_tool_terminal_return_observed'] is True and ct['record_written_after_actual_terminal_return'] is True
exact(ct['actual_tool_result'],tool)
exact(ct['binding'],pin(W/'own_rss_binding.json'))
exact(ct['source'],b['controls_source']);exact(ct['host'],b['host'])
seal=read(W/'binding_controls/seal.json','b90f8a781dc8ad0044b7f30e6e7169077f0124fce3d77b83cbc650781ed9e4e3')
exact(ct['control_seal'],pin(W/'binding_controls/seal.json'))
exact(cr['control_terminal'],pin(CT/'terminal_return.json'));exact(cr['control_seal'],ct['control_seal'])
for key in ('full_stdout','full_stderr'):desc(ct[key]);exact(cr[key],ct[key])
assert Path(ct['full_stderr']['path']).stat().st_size==0
stdout=read(ct['full_stdout']['path'])
exact(stdout,read(R/'cold_run_controls.stdout'))
assert (R/'cold_run_controls.stderr').read_bytes()==b''
tail={k:stdout[k] for k in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')}
exact(tail,cr['actual_tail']);exact(tail,{k:ct[k] for k in tail})
assert tail['actual_tail_check']=='PASS'
assert 0<tail['actual_elapsed_seconds']==92.2777771250112<120
assert tail['actual_archive_bytes']==61965994<67108864
resources=tail['actual_resources']
assert resources['artifact_budget_bytes']==103079215104 and resources['artifact_bytes']<=103079215104
assert resources['min_free_bytes']==8589934592 and resources['disk_free_bytes']>=8589934592
exact(resources['declared_resource_roots'],b['resource_info']['resource_roots'])
actual_archive=sum(q.stat().st_size for q in (W/'binding_controls').rglob('*') if q.is_file())+(W/'own_rss_binding.json').stat().st_size
actual_archive+=sum(Path(b[key]['path']).stat().st_size for key in ('host','controls_source'))
assert actual_archive==61965994,(actual_archive,61965994)
result=read(W/'binding_controls/result.json')
exact(stdout['result'],result);exact(result['source_identity'],proof)
exact(result['binding'],pin(W/'own_rss_binding.json'));exact(result['caps'],CAPS)
assert result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY'
for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted','Dragon_started','transport_started','new_assembly_or_linear_solve'):
 assert result[k] is False
assert result['positive_completed'] and result['short_completed'] and result['actual_oversize_rejected'] and result['own_children_no_longer_live']
files={str(q.relative_to(W/'binding_controls')):pin(q)['sha256'] for q in (W/'binding_controls').rglob('*') if q.is_file() and q.name!='seal.json'}
exact(files,seal['files'])
dirs=sorted(str(q.relative_to(W/'binding_controls')) for q in (W/'binding_controls').rglob('*') if q.is_dir())
exact(dirs,seal['namespace_directories']);assert len(files)==9 and dirs==['oversize','positive','short']
report={'scope':'READONLY_ACTUAL_BINDING_AND_COMPLETE_CONTROLS_TERMINAL_TAIL_PLUS_SOURCE31_PREP43_CONTINUITY',
 'status':'PASS','binding':pin(W/'own_rss_binding.json'),'binding_file_bytes':(W/'own_rss_binding.json').stat().st_size,
 'complete_binding_owner_map_count':len(b['files']),'inherited_metadata_owner_map_count':len(m['files']),
 'independently_derived_new_owner_union_count':len(supplement),'all_complete_map_entries_type_and_SHA_checked':True,
 'inherited_large_payload_union_current_bytes_rehashed':False,
 'inherited_union_authority':pin(R/'Root_actual_bounded_whole_input_independent_admission.json'),
 'all_391_normal_module_owner_current_hashes_verified':True,'runtime_module_owners':7,'runtime_flat_files':31,
 'all_43_prepared_local_and_31_source_current_hashes_verified':True,
 'entire_seven_input_component_returns_exact_to_unique_actual_full_API':True,'external_API_top_keys':65,
 'complete_SerialExecutor_class_and_qualify_aba_and_resource_monitor_byte_exact':True,
 'genuine_OwnRSS_direct_base_only_process_override_source_verified':True,
 'actual_recorded_MRO_callables_proof_equal_in_prepare_binding_and_controls':True,
 'live_MRO_independently_reexecuted':False,'actual_compiled_identity_hashes_independently_recompiled':False,
 'binding_actual_tool':br['actual_tool'],'control_actual_tool':tool,
 'control_terminal':pin(CT/'terminal_return.json'),'control_seal':pin(W/'binding_controls/seal.json'),
 'four_tail_fields_complete_and_exact':True,'controls_seconds':tail['actual_elapsed_seconds'],
 'controls_actual_archive_bytes':tail['actual_archive_bytes'],'caps':CAPS,
 'controls_sealed_files':9,'controls_sealed_directories':dirs,
 'controls_result_and_complete_stdout_exact':True,
 'source31_and_prep43_prior_frozen_reports':{
  'source31':pin(D/'REPORT_SOURCE31.json'),'prep43':pin(D/'REPORT_SOURCE31_PREP43.json')},
 'no_business_import_call_or_execution':True,'no_project_write':True,'no_Root_session_poll':True,
 'native_RSS_verified':False,'actual_full_FLU_entry_executed':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,
 'current_small_scope_current_hash_inventory':checked,
 'exploratory_read_errors_no_business_effect':[{'chunk_id':'447b87','exit_code':1,'reason':'reader incorrectly assumed tested_guard_files list had items()'},
  {'chunk_id':'ee2060','exit_code':1,'reason':'nonexistent controls.json exploratory read; actual result.json used'},
  {'chunk_id':'af88d1','exit_code':1,'reason':'nonexistent optional intake root field exploratory read'}]}
out=D/'REPORT_BINDING_AND_CONTROLS_TAIL.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':'PASS','report':str(out),'report_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'complete_owner_map_count':38524,'module_owners_verified':391,'controls_seconds':tail['actual_elapsed_seconds'],
 'archive_bytes':actual_archive,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False},sort_keys=True))

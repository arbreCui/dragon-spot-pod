from pathlib import Path
import ast,copy,difflib,hashlib,json,math,os,stat,struct,time
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');A=ROOT/'validation/axial_material';B=ROOT/'validation/artifacts'
F=A/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
FS='59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8';pins={};reads=0
def raw(p,wanted=None,retain=True):
 global reads
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode),(str(p),'ordinary file required');h=hashlib.sha256();parts=[]
 with p.open('rb')as f:
  while b:=f.read(1024*1024):
   h.update(b)
   if retain:parts.append(b)
 assert p.lstat()==s
 sha=h.hexdigest()
 if wanted:assert sha==wanted,(str(p),'SHA mismatch',sha,wanted)
 reads+=s.st_size;pins[str(p)]=dict(path=str(p),sha256=sha,bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink])
 if retain:return b''.join(parts)
def obj(p,wanted=None):return json.loads(raw(p,wanted))
def typed(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return list(a)==list(b)and all(typed(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
 if type(a)is float:return math.isfinite(a)and math.isfinite(b)and struct.pack('!d',a)==struct.pack('!d',b)
 return a==b
def restored(candidate,parent,allowed,added=()):
 r=copy.deepcopy(candidate)
 for keys in allowed:
  x,y=r,parent
  for k in keys[:-1]:x,y=x[k],y[k]
  x[keys[-1]]=copy.deepcopy(y[keys[-1]])
 for keys in added:
  x=r
  for k in keys[:-1]:x=x[k]
  del x[keys[-1]]
 assert typed(r,parent),('complete parent metadata inverse',allowed)
 return hashlib.sha256(json.dumps(r,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
ftext=raw(F,FS).decode();ft=ast.parse(ftext);compile(ft,str(F),'exec');assign={n.targets[0].id:n.value for n in ft.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
v=dict(ROOT=ROOT,ART=B)
def literal(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name):return v[n.id]
 if isinstance(n,ast.BinOp)and isinstance(n.op,ast.Div):return literal(n.left)/literal(n.right)
 if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='Path':return Path(literal(n.args[0]))
 if isinstance(n,(ast.Tuple,ast.List)):return tuple(literal(x)for x in n.elts)
 raise ValueError
for k,n in assign.items():
 try:v[k]=literal(n)
 except(ValueError,KeyError):pass
S=v['SOURCE'];T=v['COLD_TERMINAL'];O=v['OUTPUT'];C=v['CONTROL_TERMINAL'];OLD=v['OLD'];BASE=v['BASE_WORK']
decl=obj(S/'declaration.json','6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c');seal=obj(S/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
assert len(seal['files'])==30 and set(p.name for p in S.iterdir())==set(seal['files'])|{'factory_seal.json'}
source={name:raw(S/name,sha)for name,sha in seal['files'].items()}
assert all(p.is_file()and not p.is_symlink()for p in S.iterdir())
eq=json.loads(source['source_equivalence.json']);m=json.loads(source['rank1_factor_cache_admission.json']);env=json.loads(source['analysis_environment.json']);spec=json.loads(source['case_spec.json'])
for name,b in source.items():
 if name.endswith('.py'):compile(ast.parse(b),str(S/name),'exec')
e=obj(T/'declaration_terminal_return.json');assert e['actual_tool_result']==dict(closed=True,exit_code=0,initial_chunk_id='25de2d',session_id=18187,terminal_chunk_id='de668b')and type(e['actual_tool_result']['exit_code'])is int
assert type(e['returncode'])is int and e['returncode']==0 and e['record_producer']=='root'and e['record_written_after_actual_terminal_return']is e['actual_tool_terminal_return_observed']is True
assert e['source']==dict(path=str(F),sha256=FS)and e['command']==[env['executable'],str(F),'declare','--factory-sha256',FS]
assert e['scientific_qualification']is e['transport_started']is False
stdout=obj(e['full_stdout']['path'],e['full_stdout']['sha256']);assert raw(e['full_stderr']['path'],e['full_stderr']['sha256'])==b''
assert stdout==dict(classification='DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY',declaration=e['declaration'],output=str(O),factory_seal=e['factory_seal'],source_equivalence=e['source_equivalence'])
for k in('declaration','factory_seal','source_equivalence'):raw(e[k]['path'],e[k]['sha256'])
rootobs=obj(A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009/Root_actual_V9_cold_declare_tool_return.json')
api=obj(m['whole_component_body_source']['path'],m['whole_component_body_source']['sha256']);original92=api['actual_components']['original92'];runtime=api['corrected_runtime']
hist=obj(A/'combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')['metadata']['historical_actual_components']
assert len(hist)==7 and typed(api['actual_components'],hist)
trim=obj(A/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
assert len(trim)==73 and typed(api['actual_last_cprime_trim_admission'],trim)and typed(spec['rank1_factor_cache_trial']['actual_combined_runtime_admission'],api)
bind=obj(v['COMPONENT_INTAKE_DESCRIPTOR'],v['COMPONENT_INTAKE_DESCRIPTOR_SHA']);expected=copy.deepcopy(bind);expected['binding_descriptor']=dict(path=str(v['COMPONENT_INTAKE_DESCRIPTOR']),sha256=v['COMPONENT_INTAKE_DESCRIPTOR_SHA']);assert typed(m['component_input_intake'],expected)
assert m['whole_component_return_encoding']=='COMPLETE_EXTERNAL_API_JSON_POINTER_MATERIALIZED_AFTER_FRESH_GRAPH'and m['component_API_reexecution_in_cold_process']is False
source_copies=[]
for name,row in eq['unchanged_files'].items():
 assert name in v['UNCHANGED_NAMES'];parent=raw(row['parent']['path'],row['parent']['sha256']);assert parent==source[name]and row['parent']['sha256']==row['candidate']['sha256'];source_copies.append(name)
assert len(source_copies)==7
for key,name in(('HOST','combined_cold_own_rss_host.py'),('CONTROLS','combined_cold_own_rss_controls.py'),('DECK_HELPER','combined_cold_file_snapshot_decks.py'),('PRIVATE_INPUT_CONSUMER','cold_component_input_consumer_last_cprime_trim_own_pid_peak.py'),('PHYSICAL_BASIS_HELPER','physical_common_basis_admission.py'),('SCIPY_HELPER','cold_scipy_environment_admission_namespace_v3_20261008.py')):assert raw(v[key],v[key+'_SHA'])==source[name]
inverse=[]
for name in('production_runner.py','qualified_snapshot_ingestion.py','numerical_layout_admission.py'):
 proof=eq['patches'][name];original=raw(BASE/'runtime'/name,proof['original_sha256']).decode();candidate=source[name].decode();r=candidate
 for before,after in reversed(proof['replacements']):assert r.count(after)==1;r=r.replace(after,before,1)
 assert r==original
 bt=ast.parse(original);at=ast.parse(candidate);bd={n.name:n for n in bt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};ad={n.name:n for n in at.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};assert set(bd)==set(ad)
 allowed={'prepare','run'}if name=='production_runner.py'else({'verify_common_basis'}if name=='numerical_layout_admission.py'else set())
 for k in set(bd)-allowed:assert ast.get_source_segment(original,bd[k])==ast.get_source_segment(candidate,ad[k])and ast.dump(bd[k],include_attributes=False)==ast.dump(ad[k],include_attributes=False)
 if name=='production_runner.py':
  assert len(proof['replacements'])==4 and proof['original_sha256']==v['BASE_CONTROLLER_SHA']
  assert proof['replacements'][0]==['DRAGON_SHA = "'+v['BASE_RUNTIME_SHA']+'"','DRAGON_SHA = "'+runtime['sha256']+'"']
  assert proof['replacements'][2]==['    write_inputs(output / "decks", config)\n','    write_inputs(output / "decks", config)\n'+ast.literal_eval(assign['DECK_HOOK'])]
  assert proof['replacements'][3]==[ast.literal_eval(assign['CONSTRUCTOR_BEFORE']),ast.literal_eval(assign['CONSTRUCTOR_AFTER'])]
  assert ast.get_source_segment(candidate,ad['run']).replace(ast.literal_eval(assign['CONSTRUCTOR_AFTER']),ast.literal_eval(assign['CONSTRUCTOR_BEFORE']),1)==ast.get_source_segment(original,bd['run'])
  assert source[name+'.patch'].decode()==''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True)))
 elif name=='qualified_snapshot_ingestion.py':assert proof['replacements']==[["ONLINE_SHA = '"+v['BASE_RUNTIME_SHA']+"'","ONLINE_SHA = '"+runtime['sha256']+"'"]]
 else:
  dec=next(n for n in ft.body if isinstance(n,ast.FunctionDef)and n.name=='declare');strict=next(ast.literal_eval(n.value)for n in dec.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='strict_basis_function'for t in n.targets))
  assert proof['replacements']==[[ast.get_source_segment(original,bd['verify_common_basis']),strict]]
 if name!='production_runner.py':assert source[name+'.patch'].decode()==''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),fromfile='frozen-actual-production-runtime',tofile='explicit-moment-order-admission'))
 inverse.append(dict(name=name,wholebyte_inverse=True,unchanged_definitions=len(set(bd)-allowed),only_allowed_defs=sorted(allowed)))
template=ast.literal_eval(assign['ADMISSION_HOST']);scope=eq['patches']['rank1_factor_cache_admission_metadata_scope'];assert template.count(scope['old_scope_predicate'])==1;template=template.replace(scope['old_scope_predicate'],scope['new_scope_predicate'],1)
subs={'__BUILD_ROOT__':str(v['BUILD']),'__BUILD_SEAL__':original92['build_seal_sha256'],'__RUNTIME_SHA__':runtime['sha256'],'__RUNTIME_PATH__':runtime['path'],'__FACTORY_DESCRIPTOR__':dict(path=str(F),sha256=FS),'__PREPARED_SHA__':v['PREPARED_SHA'],'__BUILD_FACTORY__':str(v['BUILD_FACTORY']),'__BUILD_FACTORY_SHA__':v['BUILD_FACTORY_SHA'],'__TERMINAL_EVIDENCE__':original92['actual_external_terminal_evidence'],'__TERMINAL_VALIDATION__':original92['actual_external_terminal_validation'],'__TERMINAL_CHAIN__':m['build_terminal_chain'],'__CORRECTION_SCOPE__':v['CORRECTION_SCOPE'],'__RESOURCE_SCOPE_CONTRACT__':original92['resource_scope_contract']}
for token,value in subs.items():assert template.count(token)==1;template=template.replace(token,repr(value),1)
assert template.encode()==source['rank1_factor_cache_admission.py']
old_info=obj(OLD/'prepared.json',v['PREPARED_SHA']);parent_decl=obj(OLD/'declaration.json');parent_variant=obj(OLD/'runtime/conditional_white_receiver_variant.json');parent_receipt=obj(old_info['inputs']['material_results']['path'],old_info['inputs']['material_results']['sha256']);parent_spec=obj(old_info['case_spec']['path'],old_info['case_spec']['sha256']);parent_rank=obj(old_info['rank_addendum']['path'],old_info['rank_addendum']['sha256'])
metadata_inverse={}
metadata_inverse['variant']=restored(json.loads(source['conditional_white_receiver_variant.json']),parent_variant,[('candidate_runtime',),('files',)],[('rank1_factor_cache_revision',)])
metadata_inverse['producer_receipt']=restored(json.loads(source['producer_ingestion_receipt.json']),parent_receipt,[('online_receiver_sha256',),('conditional_white_receiver_variant',),('scope',)],[('rank1_factor_cache_revision',)])
metadata_inverse['case_spec']=restored(spec,parent_spec,[('experiment_id',),('status',),('production','implementation'),('qualified_snapshot_producers','receiver_sha256'),('qualified_snapshot_producers','receipt'),('conditional_white_trace_trial','variant')],[('rank1_factor_cache_trial',)])
metadata_inverse['rank_addendum']=restored(json.loads(source['rank_addendum.json']),parent_rank,[('experiment_id',),('case_spec_sha256',)])
metadata_inverse['declaration']=restored(decl,parent_decl,[('experiment_id',),('case_spec',),('rank_addendum',),('resource_roots',),('conditional_white_receiver_variant',),('helper',),('inputs','material_results')],[('rank1_factor_cache_revision',),('rank1_factor_cache_equivalence',),('rank1_factor_cache_resource_admission',)])
assert typed(decl['production_config'],old_info['production_config'])and typed(decl['budgets'],old_info['budgets'])and typed(m['original_inputs'],old_info['inputs'])
future=original92['future_contract'];assert future['retained_reference']['active_batches']==2000 and future['retained_reference']['active_statepoints']==[f'statepoint.{n:04d}.h5'for n in range(101,2101)]and typed(m['reference_analysis_recipe'],future['reference_analysis_recipe'])
gate=json.loads(source['input_and_gate_equivalence.json']);assert typed(gate['production_config'],old_info['production_config'])and typed(gate['budgets'],old_info['budgets'])and gate['four_thresholds']==dict(radial=2.5e-7,axial=5e-8,MCCG=2.5e-8,coupled_outer=5e-7)
assert all(m[k]is False for k in('collision_self_operator_unchanged','reference_qualification_created','old_moment_closure_numerical_replay_claimed','CE_fitting','AAA_accuracy_qualified','ABA_admitted'))
assert all(m[k]is True for k in('physical_inputs_unchanged','common_training_unchanged','white_closure_unchanged','radial_arithmetic_unchanged','original_scientific_thresholds_unchanged','original_RSS_wall_disk_caps_unchanged','exact_original_basis_and_physical_macro_source_reconstruction_required','genuine_own_pid_wait4_short_child_control_required','reference_reassessment_pending','new_binding_controls_not_yet_executed'))
dep=env['cold_scipy_dependency'];old_env=obj(dep['original_environment']['path'],dep['original_environment']['sha256']);manifest=obj(dep['manifest']['path'],dep['manifest']['sha256']);assert len(old_env['files'])==430 and len(manifest['files'])==1424
expected_env=copy.deepcopy(old_env)
def add(path,wanted):
 key=str(path)
 if key in expected_env['files']:assert expected_env['files'][key]==wanted
 else:expected_env['files'][key]=wanted
for p,wanted in manifest['files'].items():add(p,wanted)
add(dep['manifest']['path'],dep['manifest']['sha256']);add(dep['helper']['path'],dep['helper']['sha256']);expected_env['cold_scipy_dependency']=copy.deepcopy(dep)
for path,wanted in((S/'cold_scipy_environment_admission_namespace_v3_20261008.py',v['SCIPY_HELPER_SHA']),(S/'physical_common_basis_admission.py',v['PHYSICAL_BASIS_HELPER_SHA']),(v['PHYSICAL_BASIS_HELPER'],v['PHYSICAL_BASIS_HELPER_SHA']),(v['OWN_PID_SUPERVISOR'],v['OWN_PID_SUPERVISOR_SHA'])):add(path,wanted)
assert typed(env,expected_env)and len(env['files'])==1860
ns=manifest['target_namespace'];target=Path(ns['root']);expected_target={str(target/k):w for k,w in ns['files'].items()};expected_target[manifest['wheel']['path']]=manifest['wheel']['sha256'];assert expected_target==manifest['files']and typed(dep['whole_target_namespace'],ns)
files=set();dirs=set();links={}
for base,ds,fs2 in os.walk(target,followlinks=False):
 for name in list(ds):
  p=Path(base)/name;rel=str(p.relative_to(target))
  if p.is_symlink():links[rel]=os.readlink(p);ds.remove(name)
  else:dirs.add(rel)
 for name in fs2:
  p=Path(base)/name;rel=str(p.relative_to(target))
  if p.is_symlink():links[rel]=os.readlink(p)
  else:files.add(rel)
assert files==set(ns['files'])and dirs==set(ns['directories'])and links==ns['symlinks']=={}
for p,wanted in env['files'].items():raw(p,wanted,retain=False)
for p,row in pins.items():
 s=Path(p).lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==row['identity']
assert not os.path.lexists(O)and not os.path.lexists(C)and v['FORMAL_FACTORY_SHA']is None and v['BINDING_CONTROLS_ACTUAL']is None
report=dict(status='PASS_ACTUAL_DECLARE_SOURCE_ENVIRONMENT_PARENT_METADATA_SCOPE',schema='AXMAT_V9_COLD_ACTUAL_DECLARE_SOURCE_ENVIRONMENT_INDEPENDENT_REVIEW_V1',actual_declare_tool=e['actual_tool_result'],declaration_sha256=e['declaration']['sha256'],factory_seal_sha256=e['factory_seal']['sha256'],source_equivalence_sha256=e['source_equivalence']['sha256'],actual_ROOT_source_observation_sha256=pins[str(A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009/Root_actual_V9_cold_declare_tool_return.json')]['sha256'],source31_exact_namespace_all_fullSHA=True,expected6_helpers_byteexact=True,original7_UNCHANGED_source_files_byteexact=source_copies,full_generated_controller_ingestion_layout_inverses=inverse,generated_admission_template_all13token_fullbyte_reconstruction=True,whole_parent_metadata_deep_builtin_types_insertion_order_floatbits_inverses=metadata_inverse,whole_original7_body_typed_ordered_floatbits=True,whole_original73_trim_typed_ordered_floatbits=True,whole_actual_combined65_case_nested_API_typed_ordered_floatbits=True,complete_actual_intake_binding_descriptor_typed_same=True,original_config_budget_AB_inputs_and_independent2000_eight_gate_contract_retained=True,strict4456_3716_740_37000_57744_26640_storage1800_source_gate_preserved=True,complete_environment1860_fullSHA=True,original430_dictionary_allfields_and_expected_SHA_retained=True,additional1424_SciPy_whole_file_map_fullSHA=True,whole_SciPy_namespace_exact=True,thread_environment=env['thread_environment'],producer_executable=env['executable'],observed_distinct_file_pin_count=len(pins),observed_fullbyte_read_bytes_including_repeats=reads,all_pins_identity_before_after_stable=True,all_fresh_pins=list(pins.values()),full35GB_canonical_data_reread=False,graph_namespace_alias_absence_endpoint_union_resource_scope='PEER_PENDING_SEPARATE_ACTUAL_FULL_GRAPH_SCOPE_NOT_REPLACED_BY_THIS_REPORT',actual_PREP_tool=None,actual_prepared_json_sha256=None,actual_own_child_controls=None,actual_cold_native_RSS_peak=None,AAA_accuracy_qualified=False,ABA_admitted=False,project_written=False,target_factory_consumer_controller_helper_import_API_constructor_fixture_PREP_RUN_native_executed=False,limits=['PASS covers actual declaration source/parent metadata/environment only; whole canonical graph/descriptor union/current dynamic resources require complementary peer genuine review and joint binding.','Every environment owner is independently wholeSHA read; this is immutable environment INPUT, no new numerical replay/native or science qualification.','No business module imported; AST parses/compiles and pure STDlib template/string/JSON inverse operations only.','Original numeric data content freshness outside metadata/source/environment is peer scope; no35GB content observation is claimed here.'])
with(H/'REPORT.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],source_files=31,environment_files=1860,original_environment=430,Scipy_manifest_owners=1424,distinct_pins=len(pins),fullread_bytes=reads,report_sha256=hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),only_readonly=True)),flush=True)

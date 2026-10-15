"""STDlib-only actual binding audit. Compile pinned source, never execute it."""
from pathlib import Path
import ast,copy,hashlib,json,math,os,platform,stat,struct,sys,time,types
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');A=ROOT/'validation/axial_material';B=ROOT/'validation/artifacts';R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
F=A/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
FS='59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8'
S=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
O=B/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
C=B/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
BS='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930';TS='d26300e92fc469bc1674f5c788b8806656791da817019d99d12daf6f912af1b1';PS='35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7';DTS='d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c'
PINS={};BYTES=0;COMPILED={}
def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,wanted=None,retain=True):
 global BYTES
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]);h=hashlib.sha256();parts=[]
 with p.open('rb')as f:
  while chunk:=f.read(1024*1024):
   h.update(chunk)
   if retain:parts.append(chunk)
 assert identity(p)==before,(str(p),'changed during readonly read')
 sha=h.hexdigest()
 if wanted:assert sha==wanted,(str(p),'fullSHA',sha,wanted)
 BYTES+=before[3];PINS[str(p)]=dict(path=str(p),identity=before,bytes=before[3],sha256=sha)
 return b''.join(parts)if retain else sha
def pairs(items):
 d={}
 for key,value in items:
  if key in d:raise ValueError('duplicate JSON key '+key)
  d[key]=value
 return d
def obj(p,wanted=None):return json.loads(raw(p,wanted),object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def typed(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return list(a)==list(b)and all(typed(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
 if type(a)is float:return math.isfinite(a)and math.isfinite(b)and struct.pack('!d',a)==struct.pack('!d',b)
 return a==b
def literals(text):
 values={'ROOT':ROOT,'ART':B};tree=ast.parse(text)
 def literal(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Name):return values[n.id]
  if isinstance(n,(ast.Tuple,ast.List)):return tuple(literal(x)for x in n.elts)
  if isinstance(n,ast.BinOp)and isinstance(n.op,ast.Div):return literal(n.left)/literal(n.right)
  if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='Path':return Path(literal(n.args[0]))
  raise ValueError
 for n in tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:values[n.targets[0].id]=literal(n.value)
   except(ValueError,KeyError,TypeError):pass
 return values,tree
def canonical_value(value,fields):
 if type(value)is types.CodeType:return['code',[[name,canonical_value(getattr(value,name),fields)]for name in fields]]
 if value is None:return['None']
 if value is Ellipsis:return['Ellipsis']
 if type(value)is bool:return['bool',value]
 if type(value)is int:return['int',str(value)]
 if type(value)is float:return['float',struct.pack('!d',value).hex()]
 if type(value)is complex:return['complex',struct.pack('!d',value.real).hex(),struct.pack('!d',value.imag).hex()]
 if type(value)is str:return['str',value]
 if type(value)is bytes:return['bytes',value.hex()]
 if type(value)is tuple:return['tuple',[canonical_value(v,fields)for v in value]]
 if type(value)is frozenset:
  rows=[canonical_value(v,fields)for v in value];return['frozenset',sorted(rows,key=lambda row:json.dumps(row,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False))]
 if type(value)is slice:return['slice',canonical_value(value.start,fields),canonical_value(value.stop,fields),canonical_value(value.step,fields)]
 raise ValueError('unsupported typed code constant')
def compiled_callable_digest(path,class_name,member,fields,encoding):
 path=Path(path)
 if str(path)not in COMPILED:
  # This returns inert code objects. No exec/eval/import of compiled source.
  COMPILED[str(path)]=compile(raw(path).decode(),str(path),'exec',dont_inherit=True,optimize=0)
 constants=COMPILED[str(path)].co_consts
 if class_name is not None:
  classes=[c for c in constants if type(c)is types.CodeType and c.co_name==class_name];assert len(classes)==1;constants=classes[0].co_consts
 functions=[c for c in constants if type(c)is types.CodeType and c.co_name==member];assert len(functions)==1
 serialized=json.dumps([encoding,canonical_value(functions[0],fields)],ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')
 return hashlib.sha256(serialized).hexdigest()
def namespace(root):
 root=Path(root);files={};dirs=[]
 for base,ds,fs in os.walk(root,followlinks=False):
  for name in ds:
   p=Path(base)/name;assert stat.S_ISDIR(p.lstat().st_mode);dirs.append(str(p.relative_to(root)))
  for name in fs:
   p=Path(base)/name;assert stat.S_ISREG(p.lstat().st_mode);files[str(p.relative_to(root))]=p
 return files,sorted(dirs)
def source_member(text,class_name,member=None):
 tree=ast.parse(text);n=next(n for n in tree.body if isinstance(n,ast.ClassDef if class_name else ast.FunctionDef)and n.name==(class_name or member))
 return ast.get_source_segment(text,n)
def main():
 start=time.monotonic();assert platform.python_version()=='3.14.4'and sys.flags.optimize==0 and 'PYTHONOPTIMIZE'not in os.environ
 e=obj(T/'binding_terminal_return.json',TS);root=obj(R/'Root_actual_V9_cold_binding_tool_return.json','c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98')
 actual={'initial_chunk_id':'ce453a','session_id':31625,'terminal_chunk_id':'13d167','exit_code':0};assert e['actual_tool_result']==actual and type(e['actual_tool_result']['exit_code'])is int and root['actual_tool_result']==dict(actual,closed=True)
 assert root['actual_success_recorder_tool']==dict(chunk_id='2169ff',exit_code=0,closed=True)
 assert type(e['returncode'])is int and e['returncode']==0 and e['record_producer']=='root'and e['actual_tool_terminal_return_observed']is e['record_written_after_actual_terminal_return']is True
 assert e['scientific_qualification']is e['transport_started']is False
 prep_admission=obj(R/'Root_actual_full_V9_cold_PREP_independent_admission.json','8fd5bd7965cb61030ce5423b642d5356267818694dc90935ba62f09c0f9e33c3')
 previous=obj('/private/tmp/spot_v9_cold_actual_PREP_full_source_independent_review_20261009/REPORT.json','4abf92d49fc9f8a50f9e410ad8c7c311f0790fb7451a8e6cc98a48b56ea25f24');assert previous['status']=='PASS'
 for row in previous['all_fresh_pins']:assert identity(row['path'])==row['identity'];raw(row['path'],row['sha256'],False)
 plan=obj(H/'binding_postterminal_readonly_scope_plan.json','c03a739823ebd79a96ba430c7b0b00136463a3795e7a8ac5bfa54733281a3aa3')
 ftext=raw(F,FS).decode();fv,ft=literals(ftext);info=obj(O/'prepared.json',PS);seal=obj(S/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce');env=obj(S/'analysis_environment.json','0fcfa0c95e4909521f1b14860baff7d23ae3f222bb76408ce4d5841234ce2b6d')
 assert str(Path(sys.executable).resolve())==env['executable']and len(env['files'])==1860
 source={name:raw(S/name,sha)for name,sha in seal['files'].items()};assert set(namespace(S)[0])==set(source)|{'factory_seal.json'}and namespace(S)[1]==[]
 b=obj(O/'own_rss_binding.json',BS);assert identity(O/'own_rss_binding.json')[3]==60598579 and list(b)==plan['whole_binding_top_keys_from_actual_F59_AST']
 assert root['actual_binding']==e['binding']=={'path':str(O/'own_rss_binding.json'),'sha256':BS}
 htext=source['combined_cold_own_rss_host.py'].decode();hv,ht=literals(htext)
 assert b['schema']==hv['SCHEMA']=='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_OWN_RSS_BINDING_V1'
 assert typed(b['caps'],dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,control_archive_reserve_bytes=64*2**20,cold_total_seconds=43200,min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0))
 assert b['work_root']==str(O)and b['control_terminal_root']==str(C)and b['scientific_qualification']is b['module_global_or_class_overlay']is False and b['canonical_controller_name']=='production_runner'
 descriptors={'controller':(O/'runtime/production_runner.py',info['local_files']['runtime/production_runner.py']),'host':(O/'runtime/combined_cold_own_rss_host.py',fv['HOST_SHA']),'controls_source':(O/'runtime/combined_cold_own_rss_controls.py',fv['CONTROLS_SHA']),'bounded_helper':(O/'runtime/run_bounded_dragon.py',hv['BOUNDED_SHA']),'serial_baseline':(hv['BASE'],hv['BASE_SHA']),'own_rss_source':(hv['FULL'],hv['FULL_SHA']),'guard_factory':(hv['GUARD_FACTORY'],hv['GUARD_FACTORY_SHA']),'resource_class_source':(hv['RESOURCE_CLASS_SOURCE'],hv['RESOURCE_CLASS_SHA'])}
 for key,(path,sha)in descriptors.items():assert typed(b[key],dict(path=str(path),sha256=sha))and b['files'][str(path)]==sha;raw(path,sha)
 assert typed(b['producer_environment'],env)and typed(b['resource_info'],{k:info[k]for k in('artifact_root','resource_roots','case_spec')})and typed(b['input_declaration_terminal_evidence'],dict(path=str(T/'declaration_terminal_return.json'),sha256=DTS))
 expected_runtime={Path(name).name:sha for name,sha in info['local_files'].items()if name.startswith('runtime/')};assert len(expected_runtime)==31
 assert typed(b['runtime_namespace'],dict(files=dict(sorted(expected_runtime.items())),directories=[]))and namespace(O/'runtime')[1]==[] and set(namespace(O/'runtime')[0])==set(expected_runtime)
 for name,sha in info['local_files'].items():raw(O/name,sha)
 files,dirs=namespace(O);assert set(files)==set(info['local_files'])|{'prepared.json','own_rss_binding.json'}and dirs==['decks','runtime']
 expected_runtime_owners={name:dict(path=str(O/'runtime'/(name+'.py')),sha256=expected_runtime[name+'.py'])for name in hv['PRELOAD_RUNTIME_MODULES']}
 assert len(expected_runtime_owners)==7 and typed(b['runtime_module_owners'],expected_runtime_owners)
 inherited={row['path']:row['sha256']for row in previous['all_fresh_pins']};source_owned_names=[];additional_reported_owners=[]
 for name,row in b['module_owners'].items():
  assert type(name)is str and name and list(row)==['path','sha256'];p=Path(row['path']);assert p.is_absolute()and '..'not in p.parts and p.resolve()==p and p.is_relative_to(ROOT/'validation')and b['files'].get(str(p))==row['sha256'];raw(p,row['sha256'])
  if str(p)in inherited:assert inherited[str(p)]==row['sha256'];source_owned_names.append(name)
  else:additional_reported_owners.append(dict(module=name,**row))
 assert b['module_owners']['__main__']==b['controls_source']and b['module_owners']['production_runner']==b['controller']and b['module_owners']['qualify_refined_AAA_layered_full']==b['own_rss_source']
 for name,row in b['runtime_module_owners'].items():assert b['module_owners'][name]==row
 guard_folder=fv['FULL']/'preflight/live_guard';guard=obj(guard_folder/'guard_controls.json','ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454')
 tested=[dict(path=str(guard_folder/'guard_controls.json'),sha256='ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454'),dict(path=str(guard_folder/'tested_driver_source.py'),sha256=guard['source_sha256']),*[dict(path=str(guard_folder/name),sha256=sha)for name,sha in guard['control_files'].items()]]
 assert typed(b['tested_guard_files'],tested)and len(tested)==6
 for row in tested:assert b['files'].get(row['path'])==row['sha256'];raw(row['path'],row['sha256'])
 baseline=raw(b['serial_baseline']['path'],b['serial_baseline']['sha256']).decode();controller=source['production_runner.py'].decode()
 assert source_member(controller,'SerialExecutor')==source_member(baseline,'SerialExecutor')
 for name in('qualify_aba','resource_monitor'):assert source_member(controller,None,name)==source_member(baseline,None,name)
 stdout=raw(e['full_stdout']['path'],e['full_stdout']['sha256']);stderr=raw(e['full_stderr']['path'],e['full_stderr']['sha256']);assert len(stdout)==2682 and stderr==b'';result=json.loads(stdout,object_pairs_hook=pairs)
 assert typed(result,e['actual_stdout_result'])and typed(result,root['actual_stdout_result'])
 assert result['binding']==e['binding']and result['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT'and result['new_binding_fixtures_executed']is result['scientific_qualification']is False
 proof=result['actual_source_identity'];assert proof['canonical_controller_name']=='production_runner'and proof['actual_direct_bases']==['production_runner.SerialExecutor']
 for key in('inherited_original_init','inherited_original_execute','entire_SerialExecutor_source_byte_exact','actual_original_process_globals_identity','existing_guard_is_prior_proof_only'):assert proof[key]is True
 assert proof['new_binding_fixture_pass_claimed']is proof['module_global_or_class_overlay']is False
 for key in('controller','serial_baseline','own_rss_source'):assert typed(proof[key],b[key])
 functions={name:(O/'runtime/production_runner.py','SerialExecutor',name)for name in('__init__','execute','_process')};functions['OwnRSS._process']=(hv['FULL'],'OwnRSSSerialExecutor','_process');functions['write_new']=(ROOT/'validation/axial_material/probe_refined_AAA_white_odd_response.py',None,'write_new')
 functions.update({name:(O/'runtime/production_runner.py',None,name)for name in('resource_monitor','run','qualify_aba','dump_json','check_dragon_log','sha256')})
 expected_hashes={name:compiled_callable_digest(path,cls,member,hv['CODE_CONSTRUCTOR_FIELDS'],hv['CODE_IDENTITY_ENCODING'])for name,(path,cls,member)in functions.items()}
 assert len(expected_hashes)==11 and proof['actual_compiled_callable_sha256']==expected_hashes
 expected_cli=[env['executable'],str(F),'prepare-binding','--factory-sha256',FS,'--sha256',PS,'--declaration-terminal-sha256',DTS];assert e['command']==root['launch_command']==expected_cli and e['source']==dict(path=str(F),sha256=FS)
 expr='r=f.prepare_binding_in_clean_process('+repr(PS)+','+repr(DTS)+'); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
 program=('import hashlib,sys,os; from pathlib import Path\nif sys.flags.optimize!=0 or "PYTHONOPTIMIZE" in os.environ: raise ValueError("nonoptimized cold source predicates required")\nsys.dont_write_bytecode=True; p=Path('+repr(str(F))+'); assert hashlib.sha256(p.read_bytes()).hexdigest()=='+repr(FS)+'; sys.path.insert(0,str(p.parent)); import '+F.stem+' as f; assert Path(f.__file__).resolve()==p; '+expr)
 assert root['source_derived_handoff_command']==[env['executable'],'-c',program]and root['actual_execve_syscall_argv_trace']is None
 for row in root['copied_pure_Root_provenance']:raw(row['path'],row['sha256'])
 provenance=R/'cold_v9_actual_binding_postterminal_provenance';before=obj(provenance/'Root_phase_config_before_actual_binding_recording.json');after=obj(provenance/'Root_phase_config.json');restored=copy.deepcopy(after);restored['status']=before['status'];restored['future_values']['binding_sha256']=before['future_values']['binding_sha256'];restored['observations']['binding']=before['observations']['binding'];assert typed(restored,before)
 assert after['future_values']['binding_sha256']==BS and after['observations']['binding']['actual_tool_result']==actual
 assert all(after['future_values'][k]is None for k in('control_seal_sha256','control_terminal_sha256','prepared_cold_sha256'))
 assert not os.path.lexists(C)and all(not os.path.lexists(O/name)for name in('prepared_cold.json','AAA','ABA'))
 assert all(identity(row['path'])==row['identity']for row in PINS.values())
 report={'status':'PASS','scope':'ACTUAL_BINDING_COMPLETE_SOURCE_MRO_CODE_ENV_RUNTIME_WITNESS; full ownerunion/canonical/resources/wholeactual7 supplied by complementary peer','actual_binding_tool':dict(actual,closed=True),'binding_sha256':BS,'binding_terminal_sha256':TS,'Root_observer_sha256':'c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98','qualified_complete_PREP_admission_sha256':'8fd5bd7965cb61030ce5423b642d5356267818694dc90935ba62f09c0f9e33c3','inherited_full_PREP_source_deck_math_contract_pins_freshSHA_and_immutable_identity':len(previous['all_fresh_pins']),'binding_all24_AST_top_fields_original_order':True,'original_CAPS_complete_typed_unchanged':b['caps'],'original_SOURCE31_fullSHA_namespace':True,'full1860_expected_environment_pins_and_whole_environment_body_preserved':True,'original_PREP43_fullSHA_and_new_binding_only_added_to_output':True,'runtime31_exact_flat_namespace_and7_preloads':True,'all_recorded_module_owners_fullSHA_and_canonical_paths':len(b['module_owners']),'recorded_modules_independently_expected_from_inherited_PREP_source_pins':source_owned_names,'additional_module_owners_needing_complementary_independent_guard_ownerunion':additional_reported_owners,'all6_prior_guard_files_exact_original_order_fullSHA':True,'entire_original_SerialExecutor_class_and_qualifyABA_resource_monitor_bytes_equal':True,'actual_stdout_MRO_globals_proof_exact_source_contract':proof,'all11_compiled_callable_hashes_independently_source_compiled_under_original_Python':expected_hashes,'producer_compile_python':platform.python_version(),'compile_business_source_but_never_exec_or_imported_it':True,'external_original9token_cli_exact':expected_cli,'source_derived_normal_three_argument_handoff':root['source_derived_handoff_command'],'actual_execve_syscall_argv_observation':None,'reference_policy_boundary':previous['reference_policy_boundary'],'whole_metadata_math_dtype_layout_original_source_contract_unchanged':True,'full_expectedfiles_union_and_actual_component_returns_graph_resources':{'scope':'peer independent binding union required before full joint admission','binding_files_count':len(b['files']),'actual_component_keys':list(b['actual_component_returns'])},'canonical35GB_numerical_content_read':False,'new_binding_fixtures_executed':False,'new_controls_bound':False,'new_control_seal_exists':False,'new_prepared_cold_exists':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'scientific_qualification':False,'all_pins_identity_before_after_stable':True,'all_fresh_pins':list(PINS.values()),'distinct_fullSHA_pins':len(PINS),'fullbytes_read_including_repeats':BYTES,'readonly_review_elapsed_seconds':time.monotonic()-start,'project_written':False,'business_factory_consumer_controller_helper_API_constructor_binding_PREP_RUN_native_executed':False,'limits':['Live MRO/process-global identities are the actual binding source predicate observations, independently corroborated by pinned complete source and11 source-compiled canonical callable hashes; no business reexecution here.','Source-derived handoff is not a captured execve syscall trace.','Complete graph canonical bytes are inherited only from prior completed full DECLARE; peer rechecks current metadata identity, union, wholeactual7 and resources without35GB reread.','No old guard fixture credit is transferred to the new binding; fixtures/controlseal/native/science/AAA/ABA remain pending.']}
 with(H/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps({'status':'PASS','report_path':str(H/'REPORT.json'),'report_sha256':hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),'compiled_callable_hash_count':11,'distinct_pins':len(PINS),'binding_module_owner_count':len(b['module_owners']),'additional_expected_owner_count':len(additional_reported_owners),'business_executed':False}))
if __name__=='__main__':main()

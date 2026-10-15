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
ROOTSHA='8cf6d184e65b25f1f5cc6a7328a35781af68509038617a0d35eba31b17bb7893';FINALSHA='1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e';FTERMSHA='ea33c7159edf82ce4ac1ba3682cc013c013431961a7ef7ad2e6f4dc0efd5bdb4';CS='339f8385c45e4a196dba39cc4c6bf0753acbdc13953179456630bc6735a9f746';CTS='04f61e9377d468730ffd06cd3b511240d48ee881c5177b548c3b86e754c1747e';ADMSHA='f00c085928e047447b974a76d8efc01750e7dd4347bfd9aefadadeed4da14642'
def strict_obj(p,wanted=None):
 def floating(s):
  v=float(s);assert math.isfinite(v);return v
 return json.loads(raw(p,wanted),object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def sorted_value(v):return json.loads(json.dumps(v,sort_keys=True,allow_nan=False))
def descriptor(d):
 assert type(d)is dict and set(d)=={'path','sha256'};p=Path(d['path']);assert p.is_absolute()and p.resolve()==p and '..'not in p.parts
 return raw(p,d['sha256'])
def main():
 start=time.monotonic();prev=strict_obj('/private/tmp/spot_v9_actual_controls_full_source_independent_review_20261009/REPORT.json','9ffb0efce0a65dc8dd452c3e77e8a0475e254e5c1718a307e6a43ffd04a764be');assert prev['status']=='PASS'
 for row in prev['all_fresh_pins']:assert identity(row['path'])==row['identity'];raw(row['path'],row['sha256'],False)
 plan=strict_obj('/private/tmp/spot_v9_actual_finalization_source_scope_20261009/REPORT.json','408a75e17a83499ea35e01fb23fe38ad02bff48b5fd96cc557f1b9ad70219249')
 assert plan['status']=='PASS_SOURCE_ONLY_FINALIZATION_POSTTERMINAL_SCOPE'and all(v is None for v in plan['future_actual'].values())
 for row in plan['all_fresh_small_pins']:assert identity(row['path'])==row['identity'];raw(row['path'],row['sha256'],False)
 assert platform.python_version()=='3.14.4'and sys.flags.optimize==0 and 'PYTHONOPTIMIZE'not in os.environ and 'PYTHONPATH'not in os.environ and os.environ['PYTHONDONTWRITEBYTECODE']=='1'
 assert all(os.environ[k]=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
 root=strict_obj(R/'Root_actual_V9_cold_finalization_tool_return.json',ROOTSHA);e=strict_obj(T/'finalization_terminal_return.json',FTERMSHA)
 actual=dict(initial_chunk_id='a76002',session_id=47736,terminal_chunk_id='195dc5',exit_code=0)
 assert typed(e['actual_tool_result'],actual)and typed(root['actual_tool_result'],dict(actual,closed=True))
 assert typed(root['actual_success_recorder_tool'],dict(chunk_id='53d4ae',exit_code=0,closed=True))
 assert e['schema']=='AXMAT_ROOT_ACTUAL_COLD_FINALIZATION_RETURN_V1'and type(e['returncode'])is int and e['returncode']==0 and e['record_producer']=='root'
 assert e['actual_tool_terminal_return_observed']is e['record_written_after_actual_terminal_return']is True and e['scientific_qualification']is e['transport_started']is False
 admission=strict_obj(R/'Root_actual_full_V9_cold_controls_independent_admission.json',ADMSHA)
 assert admission['schema']=='AXMAT_ROOT_V9_ACTUAL_ORIGINAL_THREE_CONTROLS_FULL_COMPLEMENTARY_ADMISSION_V1'
 assert root['qualified_complete_original_controls']['sha256']==ADMSHA and root['qualified_complete_original_controls']['path']==str(R/'Root_actual_full_V9_cold_controls_independent_admission.json')
 factory=raw(F,FS).decode();fv,_=literals(factory);nodes={n.name:n for n in ast.parse(factory).body if isinstance(n,ast.FunctionDef)}
 lines=factory.splitlines(keepends=True)
 for name,span in plan['finalization_source_function_spans'].items():
  node=nodes[name];assert node.lineno==span['line']and node.end_lineno==span['end_line']
  assert hashlib.sha256(''.join(lines[node.lineno-1:node.end_lineno]).encode()).hexdigest()==span['line_span_sha256']
  assert hashlib.sha256(ast.get_source_segment(factory,node).encode()).hexdigest()==span['AST_segment_sha256']
 source_seal=strict_obj(S/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce');sources={n:raw(S/n,w)for n,w in source_seal['files'].items()}
 assert len(sources)==30 and set(namespace(S)[0])==set(sources)|{'factory_seal.json'}and namespace(S)[1]==[]
 oldraw=raw(O/'prepared.json',PS);old=json.loads(oldraw,object_pairs_hook=pairs);newraw=raw(O/'prepared_cold.json',FINALSHA);new=strict_obj(O/'prepared_cold.json',FINALSHA)
 assert len(newraw)==107746 and len(oldraw)==106577 and list(new)==list(old)+['own_child_supervision']
 assert typed(new['own_child_supervision'],plan['expected_new_field_value_and_insertion_order'])
 inverse=copy.deepcopy(new);del inverse['own_child_supervision'];assert typed(inverse,old)
 assert (json.dumps(inverse,indent=2,allow_nan=False)+'\n').encode()==oldraw
 b=strict_obj(O/'own_rss_binding.json',BS);env=strict_obj(S/'analysis_environment.json','0fcfa0c95e4909521f1b14860baff7d23ae3f222bb76408ce4d5841234ce2b6d')
 assert typed(env,b['producer_environment'])and len(env['files'])==1860 and str(Path(sys.executable).resolve())==env['executable']and env['python_version']=='3.14.4'and env['numpy_version']=='2.4.4'
 for p,w in env['files'].items():assert b['files'][p]==w;raw(p,w,False)
 for n,w in old['local_files'].items():raw(O/n,w,False)
 runtime,dirs=namespace(O/'runtime');assert dirs==[]and len(runtime)==31 and set(runtime)==set(b['runtime_namespace']['files'])
 for n,w in b['runtime_namespace']['files'].items():raw(runtime[n],w,False)
 for group in('module_owners','runtime_module_owners'):
  for n,d in b[group].items():assert b['files'][d['path']]==d['sha256'];descriptor(d)
 assert len(b['module_owners'])==391 and len(b['runtime_module_owners'])==7
 assert typed(b['caps'],prev['actual_recorded_normal_MRO_globals_proof']['controller']if False else strict_obj(O/'binding_controls/result.json')['caps'])
 assert typed(b['resource_info'],{k:old[k]for k in('artifact_root','resource_roots','case_spec')})
 controller=raw(b['controller']['path']).decode();base=raw(b['serial_baseline']['path']).decode()
 assert source_member(controller,'SerialExecutor')==source_member(base,'SerialExecutor')
 for name in('resource_monitor','qualify_aba'):assert source_member(controller,None,name)==source_member(base,None,name)
 controlseal=strict_obj(O/'binding_controls/seal.json',CS)
 for n,w in controlseal['files'].items():raw(O/'binding_controls'/n,w,False)
 ce=strict_obj(C/'terminal_return.json',CTS);controlresult=strict_obj(O/'binding_controls/result.json');assert typed(controlresult['source_identity'],prev['actual_recorded_normal_MRO_globals_proof'])
 for k in('full_stdout','full_stderr'):descriptor(ce[k])
 assert e['input_declaration_terminal_evidence']==b['input_declaration_terminal_evidence']==dict(path=str(T/'declaration_terminal_return.json'),sha256=DTS)
 original_pin=dict(path=str(O/'prepared.json'),sha256=PS);cold_pin=dict(path=str(O/'prepared_cold.json'),sha256=FINALSHA)
 stdout=descriptor(e['full_stdout']);stderr=descriptor(e['full_stderr']);assert len(stdout)==846 and stderr==b''
 assert Path(e['full_stdout']['path']).parent==Path(e['full_stderr']['path']).parent==T and len({Path(e['full_stdout']['path']),Path(e['full_stderr']['path']),T/'finalization_terminal_return.json'})==3
 returned=strict_obj(e['full_stdout']['path'],e['full_stdout']['sha256']);expected=sorted_value(dict(classification='PREPARED_COLD_INPUT_AND_ACTUAL_NEW_BINDING_CONTROLS_ONLY',original_prepared=original_pin,prepared=cold_pin,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False))
 assert typed(returned,expected)and typed(e['actual_stdout_result'],expected)and typed(root['actual_stdout_result'],expected)
 assert e['source']==dict(path=str(F),sha256=FS)and e['prepared_cold']==cold_pin
 assert e['command']==root['launch_command']==plan['expected_original_external15token_CLI']
 assert root['source_derived_handoff_command']==plan['source_derived_handoff3token_not_syscall_observation']and root['actual_execve_syscall_trace']is None
 for d in root['copied_pure_Root_provenance']:raw(d['path'],d['sha256'],False)
 folder=R/'cold_v9_actual_finalization_postterminal_provenance';before=strict_obj(folder/'Root_phase_config_before_actual_finalization_recording.json');after=strict_obj(folder/'Root_phase_config.json');back=copy.deepcopy(after)
 back['status']=before['status'];back['future_values']['prepared_cold_sha256']=before['future_values']['prepared_cold_sha256'];back['observations']['finalization']=before['observations']['finalization'];assert typed(back,before)
 assert after['future_values']['prepared_cold_sha256']==FINALSHA and after['future_values']['control_seal_sha256']==CS and after['future_values']['control_terminal_sha256']==CTS
 assert after['observations']['finalization']['actual_tool_result']==actual and after['observations']['cold']is None
 assert all(not os.path.lexists(O/n)for n in('AAA','ABA'))
 assert all(identity(row['path'])==row['identity']for row in PINS.values())
 report=dict(status='PASS',scope='ACTUAL_FINALIZATION_COMPLETE_SOURCE_ENV_METADATA_INPUT_INVARIANCE_STDIO_ROOT_WITNESS; cold peer independently whole byte inverse and namespace',actual_finalization_tool=dict(actual,closed=True),Root_observer_sha256=ROOTSHA,finalization_terminal_sha256=FTERMSHA,prepared_cold_sha256=FINALSHA,original_prepared_sha256=PS,qualified_controls_admission_sha256=ADMSHA,
 fullSOURCE31_namespace_sourcebytes_unchanged=True,all1860_expected_environment_pins_fullSHA_and1860wholebody_unchanged=True,all391_moduleowners_sourcebytes_unchanged=True,original_runtime31_flat_and7preloads_unchanged=True,all43_preparedlocalfiles_fullSHA_unchanged=True,original_full_SerialExecutor_resource_monitor_qualifyABA_bytes_unchanged=True,inherited_actual_MRO_and11compiled_code_source_proof_fresh_fullSHA=True,new_live_MRO_introspection_or_business_import_performed=False,
 original8_finalization_source_declarations_fullspan_and_AST_segment_pins_unchanged=True,oldprepared_whole_typed_order_list_floatbit_inverse_and35f_exact_bytes_verified=True,only_added_key='own_child_supervision',supervision_all3_real_descriptors_exact=new['own_child_supervision'],actual_entire_stdout_expected_whole_typed_order_floatbits_and_result_keys_exact=expected,full_stdout_bytes=len(stdout),full_stderr_bytes=len(stderr),actual_external15token_CLI=e['command'],source_derived_original5_argument_handoff3token=root['source_derived_handoff_command'],actual_execve_syscall_trace=None,Root_f14_before_after_only_finalization_bind_inverse=True,
 source_only_plan408a_and_allfuture_None_unchanged=True,inherited_controls2079_fullSHA_and7field_identities_preserved=len(prev['all_fresh_pins']),original_caps_complete_unchanged=b['caps'],reference_policy_boundary=prev['reference_policy_boundary'],original_math_physics_AB_layout_dtype_budget_whole_oldbody_invariance=True,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_RSS_verified=False,business_factory_consumer_controller_helper_API_constructor_finalize_native_executed=False,project_written=False,canonical35GB_numerical_bytes_read=0,
 all_pins_beforeafter_seven_identity_stable=True,all_fresh_pins=list(PINS.values()),distinct_fullSHA_pins=len(PINS),fullbytes_read_including_repeats=BYTES,readonly_elapsed_seconds=time.monotonic()-start,
 limits=['No new live MRO proof is returned by finalization; genuine0 original producer executed original normal-module/MRO admission, and prior actual controls11code+MRO source proofs remain fullSHA/identity bound. Reader never imports business modules.','Complete numerical graph35GB byte credit is inherited from qualified original DECLARE/INPUT/controls without reread; complementary immutable graph/owner/resource chains remain required.','Only INPUT and actual controls qualification is finalized; no native/Dragon/transport/solve/2000active sampling/AAA/ABA outcome is present.','Source-derived5argumenthandoff is not an execve syscall capture. Root auxiliary polling syntax1 is independent of genuine business0 and must remain transparently recorded by Root.'])
 with(H/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status='PASS',report=str(H/'REPORT.json'),report_sha256=hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),pins=len(PINS),actual_finalization_tool=actual,business_executed=False)))
if __name__=='__main__':main()

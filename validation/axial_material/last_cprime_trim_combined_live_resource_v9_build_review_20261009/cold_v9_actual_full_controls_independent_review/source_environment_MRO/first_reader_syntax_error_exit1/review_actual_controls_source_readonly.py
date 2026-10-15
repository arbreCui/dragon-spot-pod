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
CTSHA='04f61e9377d468730ffd06cd3b511240d48ee881c5177b548c3b86e754c1747e';ROOTSHA='f37d6f364d520c3f789dd71791d81f1f1e3e414dbfa3b6f88efa9c44439adfa1';SEALSHA='339f8385c45e4a196dba39cc4c6bf0753acbdc13953179456630bc6735a9f746'
ADMISSION='ae1577974abf75e738a3e74cc682ac3449ff3239ae617e1494dbeabeef33b726'
CONTRACT='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1';REASON='own-child 512 MiB RSS cap reached';MARKER='POSITIVE_NEW_CANONICAL_OWN_CHILD_CONTROL_COMPLETE'
CAPS=dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,control_archive_reserve_bytes=64*2**20,cold_total_seconds=43200,min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0)
TAIL=('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
def sorted_value(v):return json.loads(json.dumps(v,sort_keys=True,allow_nan=False))
def desc(d):
 assert type(d)is dict and set(d)=={'path','sha256'}
 p=Path(d['path']);assert p.is_absolute()and p.resolve()==p and '..'not in p.parts
 return raw(p,d['sha256'])
def strict_obj(p,wanted=None):
 def floating(s):
  v=float(s);assert math.isfinite(v);return v
 return json.loads(raw(p,wanted),object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def source_function_spans(scope):
 pins=[]
 for path,row in scope['source_pins'].items():
  b=raw(path,row['sha256']);assert len(b)==row['bytes'];pins.append(path)
 for path,funcs in scope['source_function_line_references'].items():
  lines=raw(path).splitlines(keepends=True)
  for name,row in funcs.items():assert hashlib.sha256(b''.join(lines[row['line']-1:row['end_line']])).hexdigest()==row['source_sha256']
 return pins

def audit_peak(w,mode):
 assert type(w)is dict and w['rss_peak_observation_contract']==CONTRACT and w['rss_cap_mib']==512
 assert type(w['pid'])is int and w['pid']>0 and type(w['returncode'])is int and type(w['own_pid_wait4_observed'])is bool
 sampled=w['sampled_peak_rss_mib'];observed=w['observed_peak_rss_mib'];kernel=w['own_pid_wait4_peak_rss_mib'];count=w['live_rss_sample_count']
 assert all(type(v)in(int,float)and math.isfinite(v)and v>=0 for v in(sampled,observed))and type(count)is int and count>=0
 assert count!=0 or sampled==0
 if w['own_pid_wait4_observed']:
  pid=w['own_pid_wait4_pid'];status=w['own_pid_wait4_status'];rusage=w['own_pid_wait4_ru_maxrss_bytes']
  assert type(pid)is int and pid==w['pid']and type(status)is int and 0<=status<=65535 and (os.WIFEXITED(status)or os.WIFSIGNALED(status))
  assert os.waitstatus_to_exitcode(status)==w['returncode']
  assert type(rusage)in(int,float)and math.isfinite(rusage)and rusage>0 and rusage==int(rusage)
  assert type(kernel)in(int,float)and math.isfinite(kernel)and kernel>0 and kernel==rusage/(1024.*1024.)
 else:assert all(w[k]is None for k in('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'))
 assert observed==max(sampled,kernel if kernel is not None else 0.)
 if mode in('positive','short'):
  assert w['returncode']==0 and w['limit_failure']is None and w['own_pid_wait4_observed']is True and 0<observed<512
  if mode=='short':assert kernel>=16
 else:assert w['returncode']in(-15,-9)and sampled>=512 and observed>=512 and w['limit_failure']==repr(RuntimeError(REASON))
 return {k:w[k]for k in('pid','returncode','live_rss_sample_count','sampled_peak_rss_mib','own_pid_wait4_observed','own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib','observed_peak_rss_mib','limit_failure')}

def main():
 start=time.monotonic();assert platform.python_version()=='3.14.4'and sys.platform=='darwin'and sys.flags.optimize==0
 assert 'PYTHONPATH'not in os.environ and 'PYTHONOPTIMIZE'not in os.environ and os.environ['PYTHONDONTWRITEBYTECODE']=='1'
 assert all(os.environ[k]=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
 previous=strict_obj('/private/tmp/spot_v9_cold_actual_binding_full_source_independent_review_20261009/REPORT.json','bfaf98e2a9038c0b1634f2a49be90fdacb025aed8c2bcf1e6adc3534cfb772f7');assert previous['status']=='PASS'
 for row in previous['all_fresh_pins']:assert identity(row['path'])==row['identity'];raw(row['path'],row['sha256'],False)
 admission=strict_obj(R/'Root_actual_full_V9_cold_binding_independent_admission.json',ADMISSION)
 root=strict_obj(R/'Root_actual_V9_cold_controls_tool_return.json',ROOTSHA)
 e=strict_obj(C/'terminal_return.json',CTSHA)
 actual={'initial_chunk_id':'085698','session_id':92301,'terminal_chunk_id':'5c78de','exit_code':0}
 assert typed(e['actual_tool_result'],actual)and typed(root['actual_tool_result'],dict(actual,closed=True))
 assert typed(root['actual_success_recorder_tool'],dict(chunk_id='0b84d1',exit_code=0,closed=True))
 assert type(e['returncode'])is int and e['returncode']==0 and e['record_producer']=='root'
 assert e['actual_tool_terminal_return_observed']is e['record_written_after_actual_terminal_return']is True
 assert e['scientific_qualification']is e['transport_started']is False
 scope=strict_obj('/private/tmp/axmat_v9_cold_actual_controls_postterminal_scope_20261009/controls_postterminal_reader_scope_and_future_None.json','fc8d6b4bbefd8460719bb5ed8063bc67842acff705c90554ac2d5ede69f8e460')
 assert all(v is None for v in scope['future_actual'].values());sources=source_function_spans(scope)
 source_plan=strict_obj('/private/tmp/spot_v9_actual_controls_source_scope_20261009/REPORT.json','f74635eb387b14c9380630b2bba38063b7856075fc69fa1e9d6cab21d76d7e2c')
 for p in source_plan['all_fresh_pins']:
  expected=p.get('identity',p.get('immutable_identity'));assert identity(p['path'])==expected;raw(p['path'],p['sha256'],False)
 b=strict_obj(O/'own_rss_binding.json',BS);assert b['caps']==CAPS and b['scientific_qualification']is b['module_global_or_class_overlay']is False
 seal=strict_obj(S/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
 src={n:raw(S/n,w)for n,w in seal['files'].items()};assert len(src)==30 and set(namespace(S)[0])==set(src)|{'factory_seal.json'}and namespace(S)[1]==[]
 info=strict_obj(O/'prepared.json',PS);env=strict_obj(S/'analysis_environment.json','0fcfa0c95e4909521f1b14860baff7d23ae3f222bb76408ce4d5841234ce2b6d')
 assert typed(env,b['producer_environment'])and len(env['files'])==1860 and str(Path(sys.executable).resolve())==env['executable']
 assert env['python_version']=='3.14.4'and env['numpy_version']=='2.4.4'
 for p,w in env['files'].items():assert b['files'][p]==w;raw(p,w,False)
 for name,w in info['local_files'].items():raw(O/name,w,False)
 runtime,dirs=namespace(O/'runtime');assert dirs==[] and set(runtime)==set(b['runtime_namespace']['files'])and len(runtime)==31
 for name,w in b['runtime_namespace']['files'].items():raw(runtime[name],w,False)
 for group in('module_owners','runtime_module_owners'):
  for name,d in b[group].items():assert b['files'][d['path']]==d['sha256'];desc(d)
 assert len(b['module_owners'])==391 and len(b['runtime_module_owners'])==7
 hv,_=literals(src['combined_cold_own_rss_host.py'].decode())
 for key in('controller','host','controls_source','bounded_helper','serial_baseline','own_rss_source','guard_factory','resource_class_source'):
  assert b['files'][b[key]['path']]==b[key]['sha256'];desc(b[key])
 for d in b['tested_guard_files']:assert b['files'][d['path']]==d['sha256'];desc(d)
 assert len(b['tested_guard_files'])==6
 assert raw(b['host']['path'])==src['combined_cold_own_rss_host.py']and raw(b['controls_source']['path'])==src['combined_cold_own_rss_controls.py']
 controller=raw(b['controller']['path']).decode();baseline=raw(b['serial_baseline']['path']).decode()
 assert source_member(controller,'SerialExecutor')==source_member(baseline,'SerialExecutor')
 for name in('resource_monitor','qualify_aba'):assert source_member(controller,None,name)==source_member(baseline,None,name)
 control_root=O/'binding_controls';files,dirs=namespace(control_root)
 expected_files={'claim.json','result.json','stages.json','seal.json',*[m+'/'+n for m in('positive','oversize','short')for n in('execute.log','execute.watchdog.json')]}
 assert set(files)==expected_files and dirs==['oversize','positive','short']
 controlseal=strict_obj(control_root/'seal.json',SEALSHA);assert controlseal['schema']==hv['SEAL_SCHEMA']and controlseal['namespace_directories']==dirs and set(controlseal['files'])==expected_files-{'seal.json'}
 for n,w in controlseal['files'].items():raw(files[n],w,False)
 result=strict_obj(control_root/'result.json',root['actual_result_file']['sha256']);claim=strict_obj(control_root/'claim.json');stages=strict_obj(control_root/'stages.json')['stages']
 binding=dict(path=str(O/'own_rss_binding.json'),sha256=BS)
 assert typed(claim,sorted_value(dict(schema=hv['CONTROL_SCHEMA'],pid=claim['pid'],binding=binding,started_unix=claim['started_unix'],retries=0,scientific_qualification=False)))
 assert type(claim['pid'])is int and claim['pid']>0 and type(claim['started_unix'])in(int,float)and math.isfinite(claim['started_unix'])and claim['started_unix']>0
 assert result['schema']==hv['CONTROL_SCHEMA']and result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY'and typed(result['binding'],sorted_value(binding))and typed(result['caps'],sorted_value(CAPS))
 assert all(result[k]is True for k in('positive_completed','actual_oversize_rejected','short_completed','own_children_no_longer_live'))
 assert all(result[k]is False for k in('scientific_qualification','Dragon_started','transport_started','new_assembly_or_linear_solve','AAA_accuracy_qualified','ABA_admitted'))
 assert result['short_allocation_bytes']==16*2**20 and result['rss_peak_observation_contract']==CONTRACT
 proof=result['source_identity'];assert typed(proof,previous['actual_stdout_MRO_globals_proof_exact_source_contract'])
 fn={n:(O/'runtime/production_runner.py','SerialExecutor',n)for n in('__init__','execute','_process')};fn['OwnRSS._process']=(b['own_rss_source']['path'],'OwnRSSSerialExecutor','_process');fn['write_new']=(b['module_owners']['probe_refined_AAA_white_odd_response']['path'],None,'write_new')
 fn.update({n:(O/'runtime/production_runner.py',None,n)for n in('resource_monitor','run','qualify_aba','dump_json','check_dragon_log','sha256')})
 hashes={n:compiled_callable_digest(p,c,f,hv['CODE_CONSTRUCTOR_FIELDS'],hv['CODE_IDENTITY_ENCODING'])for n,(p,c,f)in fn.items()}
 assert len(hashes)==11 and proof['actual_compiled_callable_sha256']==hashes
 helper_hashes={n:compiled_callable_digest(b['bounded_helper']['path'],None,n,hv['CODE_CONSTRUCTOR_FIELDS'],hv['CODE_IDENTITY_ENCODING'])for n in('start_liveness_watchdog','finish_liveness_watchdog','terminate_group','process_group_exists')}
 expected_helper=dict(source=b['bounded_helper'],actual_compiled_callable_sha256=helper_hashes,original_bounded_group_cleanup_code_identity=True,helper_globals_or_callable_overlay=False)
 assert typed(result['actual_bounded_helper'],sorted_value(expected_helper))
 assert typed(result['actual_resource_class'],sorted_value(dict(class_module='rank1_cache_actual_moment_build',class_source=b['resource_class_source'],class_name='DynamicHistoryResources',no_class_or_resource_overlay=True)))
 assert [x['mode']for x in result['observations']]==['positive','oversize','short']and [x['label']for x in stages]==['binding_controls/'+m+'/execute'for m in('positive','oversize','short')]and [x['status']for x in stages]==['PASS','FAILED','PASS']
 peaks=[]
 for stage,observation in zip(stages,result['observations']):
  mode=observation['mode'];wp=Path(observation['watchdog']['path']);lp=Path(observation['raw_log']['path'])
  assert wp==control_root/mode/'execute.watchdog.json'and lp==control_root/mode/'execute.log';desc(observation['raw_log']);desc(observation['watchdog'])
  watch=strict_obj(wp,observation['watchdog']['sha256']);assert typed(watch,observation['watch'])
  cmd=[env['executable'],b['controls_source']['path'],'fixture',mode]
  assert stage['command']==observation['command']==watch['command']==cmd and watch['own_child_only']is watch['liveness_group_cleanup']is observation['actual_group_no_longer_live']is True
  assert 0<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=60 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']and 0<=stage['elapsed_seconds']<stage['wall_cap_seconds']
  lines=raw(lp).decode().splitlines();intent=json.loads(lines[0],object_pairs_hook=pairs)
  assert typed(intent,dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,pid=watch['pid'],requested_bytes=576*2**20 if mode=='oversize'else16*2**20))
  if mode=='oversize':assert stage['error']==observation['actual_expected_rejection']==REASON and stage['log_sha256']==observation['raw_log']['sha256']
  else:assert MARKER in lines and stage['log_sha256']==observation['raw_log']['sha256']and observation['actual_expected_rejection']is None
  peaks.append(dict(mode=mode,**audit_peak(watch,mode)))
 assert C.parent==B and not C.is_relative_to(O)
 assert e['schema']==hv['TERMINAL_SCHEMA']and typed(e['binding'],binding)and typed(e['host'],b['host'])and typed(e['source'],b['controls_source'])
 assert typed(e['input_declaration_terminal_evidence'],b['input_declaration_terminal_evidence'])and typed(e['control_seal'],dict(path=str(control_root/'seal.json'),sha256=SEALSHA))
 stdout=desc(e['full_stdout']);stderr=desc(e['full_stderr']);assert len(stdout)==136307 and stderr==b''
 assert Path(e['full_stdout']['path']).parent==Path(e['full_stderr']['path']).parent==C
 assert set(namespace(C)[0])=={'terminal_return.json','controls.stdout','controls.stderr'}and namespace(C)[1]==[]
 returned=strict_obj(e['full_stdout']['path'],e['full_stdout']['sha256']);tail={k:returned[k]for k in TAIL}
 assert typed(returned,sorted_value(dict(result=result,**tail)))and all(typed(e[k],tail[k])for k in TAIL)
 assert tail['actual_tail_check']=='PASS'and type(tail['actual_elapsed_seconds'])in(int,float)and math.isfinite(tail['actual_elapsed_seconds'])and result['elapsed_before_closeout']<=tail['actual_elapsed_seconds']<120
 archive=sum(identity(p)[3]for p in files.values())+sum(identity(b[k]['path'])[3]for k in('host','controls_source'))+identity(O/'own_rss_binding.json')[3]
 assert type(tail['actual_archive_bytes'])is int and tail['actual_archive_bytes']==archive==61047970 and archive<64*2**20
 internal=[env['executable'],b['controls_source']['path'],'run-controls','--binding',binding['path'],'--binding-sha256',BS]
 external=[env['executable'],str(F),'run-controls','--factory-sha256',FS,'--binding-sha256',BS,'--declaration-terminal-sha256',DTS]
 assert e['command']==root['source_derived_handoff_command']==internal and root['launch_command']==external and root['actual_execve_syscall_trace']is None
 for p in root['copied_pure_Root_provenance']:raw(p['path'],p['sha256'],False)
 provenance=R/'cold_v9_actual_controls_postterminal_provenance';before=strict_obj(provenance/'Root_phase_config_before_actual_controls_recording.json');after=strict_obj(provenance/'Root_phase_config.json');back=copy.deepcopy(after)
 back['status']=before['status'];back['future_values']['control_seal_sha256']=before['future_values']['control_seal_sha256'];back['future_values']['control_terminal_sha256']=before['future_values']['control_terminal_sha256'];back['observations']['control']=before['observations']['control'];assert typed(back,before)
 assert after['future_values']['control_seal_sha256']==SEALSHA and after['future_values']['control_terminal_sha256']==CTSHA and after['future_values']['prepared_cold_sha256']is None
 assert all(not os.path.lexists(O/n)for n in('prepared_cold.json','AAA','ABA'))
 for row in PINS.values():assert identity(row['path'])==row['identity']
 report=dict(status='PASS',scope='ACTUAL_CONTROLS_COMPLETE_SOURCE_ENV_MRO_COMPILED_CODE_RAW_STDIO_ROOT_WITNESS_AND_ALL_THREE_WATCHES; complementary fullgraph/ownerunion/resources required for whole joint admission',actual_controls_tool=dict(actual,closed=True),Root_observer_sha256=ROOTSHA,control_terminal_sha256=CTSHA,control_seal_sha256=SEALSHA,qualified_binding_admission_sha256=ADMISSION,binding_sha256=BS,
 inherited_binding_full_source_pins_freshSHA_and_seven_identities=len(previous['all_fresh_pins']),SOURCE31_fullSHA_namespace=True,environment1860_complete_expected_fullSHA=True,moduleowners391_complete_current_fullSHA=True,runtime31_and7preloads_unchanged=True,prepared43_fullSHA=True,original18_source_functions_and6fullsources_exact=True,original_fullSerialExecutor_andresource_monitor_qualifyABA_source_exact=True,
 actual_recorded_normal_MRO_globals_proof=proof,actual_mro_source_compile11_sha256=hashes,actual_bounded_helper4_sha256=helper_hashes,actual_control_namespace_files=sorted(files),actual_control_namespace_directories=dirs,independent_CT3_exact=True,all_three_exact_watch_stage_log_intent_checks=True,actual_peaks=peaks,actual_four_tail=tail,actual_archive_bytes_full_recount=archive,
 actual_source_derived_internal_cli=internal,actual_external_cli=external,actual_execve_syscall_argv_trace=None,Root_purewriter_exact_control_bind_only_inverse=True,source_only_future_None_plan_preserved=True,
 new_controls_executed=True,controls_only_qualification=True,canonical35GB_numerical_bytes_read=0,large_file_content_scope_inherited_from_fullDECLARE_and_complementary_metadata_only=True,project_written=False,business_API_factory_consumer_controller_helper_constructor_fixture_native_executed=False,
 reference_policy_boundary=previous['reference_policy_boundary'],native_RSS_verified=False,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,all_fresh_pins=list(PINS.values()),distinct_fullSHA_pins=len(PINS),fullbytes_read_including_repeats=BYTES,readonly_elapsed_seconds=time.monotonic()-start,
 limits=['Live MRO/process-global and process-group absence values are retained original control-program predicate observations; reader corroborates them with full source and inert code compilation, without business module introspection or live signal probes.','Oversize expected rejection has no wait4 receipt, so all four kernel fields remain None; sampled596.546875 MiB is an actual failed-cap control, never native performance or memory success.','Short live sample count0/sampled0 is not a zero-memory claim; actual own-PID wait4 kernel36.75 MiB is mandatory.','Whole fullgraph, complete37395 owner expectation and all dynamic resources require complementary independent peer evidence; this report does not alone grant full science scope.','Compiled source code objects are inert, compiled under original3.14.4 only; source modules are never executed or imported.'])
 with(H/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
 print(json.dumps(dict(status='PASS',report=str(H/'REPORT.json'),report_sha256=hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),source_pins=len(PINS),compiled11=len(hashes),helper4=len(helper_hashes),actual_peaks=peaks,business_executed=False)))
if __name__=='__main__':main()

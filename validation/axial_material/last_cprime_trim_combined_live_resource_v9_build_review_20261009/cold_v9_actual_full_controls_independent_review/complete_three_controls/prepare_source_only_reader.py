from pathlib import Path
import ast,hashlib,json,os,stat

O=Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_reader_20261009')
A=Path('/Users/wen/spot/validation/artifacts');V=Path('/Users/wen/spot/validation/axial_material')
W=A/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
CT=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
H=V/'combined_cold_own_rss_host_physical_basis_own_pid_peak_20261008.py'
K=V/'combined_cold_own_rss_controls_own_pid_peak_20261008.py'
F=V/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
scope=Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_scope_20261009/controls_postterminal_reader_scope_and_future_None.json')
bindingsha='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930'
known={H:'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7',K:'d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393',F:'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8',scope:'fc8d6b4bbefd8460719bb5ed8063bc67842acff705c90554ac2d5ede69f8e460',W/'runtime/combined_cold_own_rss_host.py':'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7',W/'runtime/combined_cold_own_rss_controls.py':'d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393'}
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink');pins=[]
def sid(p):
 s=p.lstat();return [getattr(s,'st_'+k) for k in KEYS]
def read(p,w):
 before=sid(p);b=p.read_bytes();assert sid(p)==before and hashlib.sha256(b).hexdigest()==w,(str(p),hashlib.sha256(b).hexdigest());pins.append(dict(path=str(p),sha256=w,bytes=len(b)));return b
for p,w in known.items():read(p,w)
b=json.loads(read(W/'own_rss_binding.json',bindingsha))
assert b['work_root']==str(W) and b['caps']['control_total_seconds']==120 and b['caps']['rss_cap_mib']==512
mapping=dict(b['files'])
for p,w in b['producer_environment']['files'].items():assert p not in mapping or mapping[p]==w;mapping[p]=w
for owners in (b['module_owners'],b['runtime_module_owners']):
 for d in owners.values():assert mapping.get(d['path'])==d['sha256']
def identity_stream():
 h=hashlib.sha256();fm=hashlib.sha256()
 for p,w in sorted(mapping.items()):
  q=Path(p);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink(),p
  h.update(json.dumps([p,w,sid(q)],separators=(',',':'),ensure_ascii=False).encode()+b'\n');fm.update(json.dumps([p,w],separators=(',',':'),ensure_ascii=False).encode()+b'\n')
 return dict(paths=len(mapping),expected_filemap_sha256=fm.hexdigest(),seven_field_identity_sha256=h.hexdigest())
owner=identity_stream();assert identity_stream()==owner
host=H.read_text();tree=ast.parse(host);lines=host.splitlines(keepends=True);pure_names=('compiled_code','canonical_code_value','canonical_code_bytes');parts=[];inverse=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('CODE_IDENTITY_ENCODING','CODE_CONSTRUCTOR_FIELDS') for t in n.targets):parts.append(''.join(lines[n.lineno-1:n.end_lineno]))
for name in pure_names:
 ns=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name];assert len(ns)==1;n=ns[0];body=''.join(lines[n.lineno-1:n.end_lineno]);parts.append(body);inverse.append(dict(name=name,host_line=n.lineno,host_end_line=n.end_lineno,source_sha256=hashlib.sha256(body.encode()).hexdigest(),AST=ast.dump(n,include_attributes=False)))
rp=O/'audit_actual_controls_readonly.py';original=rp.read_text();anchor='# compile() derives code only; no code object or business module is executed.\n';assert original.count(anchor)==1
changed=original.replace(anchor,anchor+'\n'+'\n\n'.join(parts)+'\n',1);assert changed.replace(anchor+'\n'+'\n\n'.join(parts)+'\n',anchor,1)==original
ast.parse(changed);compiled=compile(changed,str(rp),'exec',dont_inherit=True,optimize=0) # Not executed.
rp.write_text(changed);after=ast.parse(changed);outlines=changed.splitlines(keepends=True)
for item in inverse:
 n=next(n for n in after.body if isinstance(n,ast.FunctionDef) and n.name==item['name']);body=''.join(outlines[n.lineno-1:n.end_lineno]);assert hashlib.sha256(body.encode()).hexdigest()==item['source_sha256'] and ast.dump(n,include_attributes=False)==item['AST'];del item['AST'];item['reader_line']=n.lineno;item['byte_AST_exact_from_host']=True
imports=[]
for n in ast.walk(after):
 if isinstance(n,ast.Import):imports.extend(x.name for x in n.names)
 elif isinstance(n,ast.ImportFrom):imports.append(n.module)
 elif isinstance(n,ast.Call):
  if isinstance(n.func,ast.Name):assert n.func.id not in ('exec','eval','__import__')
  elif isinstance(n.func,ast.Attribute):assert n.func.attr not in ('execve','execv','system','Popen','spawn','fork','import_module')
assert set(imports)<={'pathlib','ast','hashlib','json','math','os','shutil','stat','struct','sys','types'}
future={k:None for k in ('Root_explicit_closed_controls_EXIT0_observed','actual_tool_result','qualified_binding_joint_review','binding_stdout','control_seal_sha256','control_result_sha256','control_terminal_sha256')}
config=dict(status='SOURCE_ONLY_UNREADY_ACTUAL_CONTROLS_TERMINAL_NOT_YET_BOUND',work=str(W),control_terminal=str(CT),known_binding_sha256=bindingsha,known_Root_qualified_binding_joint_sha256='ae1577974abf75e738a3e74cc682ac3449ff3239ae617e1494dbeabeef33b726',known_source_pins={str(p):w for p,w in known.items() if p!=scope},immutable_complete_owner_identity=owner,identity_observation_timing='SOURCE_ONLY immutable owner identity capture after Root explicitly supplied genuine closed controls EXIT0; excludes new controls outputs, still not bound to any controls result in this template. Not a pre-launch observation or fullscience byte admission.',future_actual=future,scope_reference=dict(path=str(scope),sha256=known[scope]),actual_source_prep_reader_or_fixture_or_business_executed=False)
def write(name,obj):
 p=O/name;assert not p.exists();p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n');return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
cfg=write('actual_controls_config_SOURCE_ONLY_UNREADY.json',config)
proof=write('reader_source_static_audit_and_complete_scope.json',dict(status='SOURCE_ONLY_READER_PREPARED_NOT_EXECUTED',scope_reference=config['scope_reference'],source_pins=pins,complete_owner_scope=owner,binding_module_owner_count=len(b['module_owners']),runtime_preload_owner_count=len(b['runtime_module_owners']),no_multiMB_owner_baseline_copy=True,no_large_expected_science_bytes_read=True,all_actual_control_future_None=True,known_actual_binding_descriptor=dict(path=str(W/'own_rss_binding.json'),sha256=bindingsha),original_pure_code_derivation_functions_byte_AST_exact=inverse,reader_imports=sorted(set(imports)),no_exec_eval_business_import_or_process_launch=True,AST_parse_and_compile_only_not_execute=True,default_config_guard_precedes_binding_or_controls_read=True,whole_actual_control_archive_and_runtime_byte_pins_required=True,whole_expected_owner_identity_comparison_not_35GB_rehash=True,closed_Root_tool_and_copied_actual_argv_exact_four_keys_required=True,complete_result_three_watch_log_claim_stages_namespace_and_four_tail_required=True,original_caps_preserved=dict(RSS_MiB512=512,whole_seconds120=120,stage_seconds60=60,archive_bytes64MiB=64*2**20,threads1=1,child1=1,retry0=0),only_independent_CT_recordaftertool_root_time_difference_allowed=True,source_only_owner_capture_after_live_not_called_precontrol=True))
report=write('REPORT.txt','''完整三controls只读后验reader模板已SOURCE-ONLY准备，未运行reader。没有业务import/exec/controls/fixture/native/API/Rootwriter或当前LIVE结果读取；只读known actual binding metadata与原已审源码/owner路径身份。future controls EXIT/result/seal/CT/stdout/kernel/RSS/tails无填入；default config UNREADY会在任何binding/control读之前拒绝。

原fc8d6完整scope保留，current copied dd2fad host/d4da controls而非旧双control。whole binding expected owner union全37395路径（实际派生值在JSON），moduleowners/runtimepreload全部保留；只封小expected-map/七field身份流指纹，不复制多MB清单，也不重hash35GB。此owner capture在Root真正closed controls EXIT0消息后执行，明确不是伪造precontrol观测；全部新controls输出排除，source-only配置仍未绑定任何controls实际值。Root已有真正全binding source+graph/joint准入ae157固定source identity；source template future descriptor/stdout仍None，实际读者需另外真实配置。

实际后验将：全runtime及控制archive逐byte SHA与完整seal ns严格相同；claim/result/stages/positive-oversize-short三watch/log/ownPID分配/marker/cleanup；full stdout=result+四tail及独立CT四key genuine builtin-int0/实际copied argv/recordaftertool。正常/short须自身Darwin wait4PID/status/ru_maxrss BYTES，kernelMiB=raw/2**20，observed=max(livePSMiB,kernelMiB)<512；short kernel>=16，缺receipt拒绝不变0。oversize FAILED仅原live>=512的-15/-9预期拒绝，missing kernel四fields真实None；全controls必须Root真0。

normalMRO/完整源callables：通过真正binding stdout和controls source_identity相等，独立静态compile code（不执行module）推导原Py3.14.4 code digests，原typed编码3pure functions与dd2 host byte/AST exact。完整SerialExecutor/resource_monitor/qualify_aba原BASE byte、真实来源描述符/原bounded4functions/dynamic resourceclass同。helper/business全部不调用。

原60/120/512/64MiB/thread1/child1/retry0、96GiB/free8完整资源不变。记录尾dynamic roots全保留，并fresh metadata计数当前原根/动态union和free；只允许有独立Rootreceipt证据的CT在record-after-tool新增造成时点差，不要求旧tail金额等于后写入收据后的新金额，不放宽其它scope/caps。所有读者输出仅固定TMP，后验仅controls-only无science/AAA/ABA/native信用。

可执行只读入口：audit_actual_controls_readonly.py（当前不执行）；Root实际事实绑定到config且真实终态明确后才允许运行。若实际非零，继续UNREADY并审核真实failure，不能把本模板或旧控件当PASS。源准备/AST审/完整scope报告和真实工具收据均保留。
''')
reader=dict(path=str(rp),sha256=hashlib.sha256(rp.read_bytes()).hexdigest(),bytes=rp.stat().st_size)
result=dict(status='SOURCE_ONLY_READER_PREPARED_UNREADY_NOT_EXECUTED',reader=reader,config=cfg,source_static_audit=proof,report=report,controls_future_None=True,reader_executed=False,business_executed=False,project_written=False)
write('source_preparation_result.json',result);print(json.dumps(result,ensure_ascii=False,sort_keys=True))

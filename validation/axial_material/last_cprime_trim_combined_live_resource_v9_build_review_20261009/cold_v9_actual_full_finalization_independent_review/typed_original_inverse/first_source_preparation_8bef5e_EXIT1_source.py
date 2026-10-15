from pathlib import Path
import ast,hashlib,json,os,stat,struct
O=Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009');A=Path('/Users/wen/spot/validation/artifacts');V=Path('/Users/wen/spot/validation/axial_material')
S=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
W=A/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
CT=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
F=V/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py';PREPLAN=Path('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/finalization_original_launch_and_source_derived_handoff.json')
R9=V/'last_cprime_trim_combined_live_resource_v9_build_review_20261009';keys=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink');pins={}
known={F:'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8',W/'prepared.json':'35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7',W/'own_rss_binding.json':'4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930',W/'binding_controls/seal.json':'339f8385c45e4a196dba39cc4c6bf0753acbdc13953179456630bc6735a9f746',CT/'terminal_return.json':'04f61e9377d468730ffd06cd3b511240d48ee881c5177b548c3b86e754c1747e',T/'declaration_terminal_return.json':'d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c',S/'declaration.json':'6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c',W/'runtime/production_runner.py':'67ae4ae465013fd7c7bd5ccb07c9d06c9b7e88dba9ba8481c7e4a506f15147bf',W/'runtime/combined_cold_own_rss_host.py':'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7',W/'runtime/combined_cold_own_rss_controls.py':'d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393'}
def sid(p):
 s=p.lstat();return [getattr(s,'st_'+k) for k in keys]
def read(p,w=None):
 before=sid(p);b=p.read_bytes();h=hashlib.sha256(b).hexdigest();assert sid(p)==before and (w is None or h==w),(str(p),h);pins[str(p)]=h;return b
for p,h in known.items():read(p,h)
oldbytes=read(W/'prepared.json');old=json.loads(oldbytes);assert 'own_child_supervision' not in old and old['classification']=='PREPARED_NO_TRANSPORT';assert (json.dumps(old,indent=2,allow_nan=False)+'\n').encode()==oldbytes
def typed(v):
 if v is None:return ['None']
 if type(v)is bool:return ['bool',v]
 if type(v)is int:return ['int',str(v)]
 if type(v)is float:return ['float64',struct.pack('!d',v).hex()]
 if type(v)is str:return ['str',v]
 if type(v)is list:return ['list',[typed(x) for x in v]]
 if type(v)is dict:return ['dict_ordered',[[typed(k),typed(x)] for k,x in v.items()]]
 raise ValueError('metadata type')
td=hashlib.sha256(json.dumps(typed(old),ensure_ascii=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
pre=json.loads(read(PREPLAN));assert pre['actual_finalization_tool'] is None and pre['prepared_cold_sha256'] is None
assert pre['factory']==dict(path=str(F),sha256=known[F]) and pre['actual_controls_terminal']==dict(path=str(CT/'terminal_return.json'),sha256=known[CT/'terminal_return.json'])
source=F.read_text();tree=ast.parse(source);fn={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};lines=source.splitlines(keepends=True);spans={}
for name in ('write_new','normal_factory_command','final_cold_info','finalize_cold_in_clean_process','finalize_cold','cold_launch_in_clean_process','cold_terminal_admission'):
 n=fn[name];body=''.join(lines[n.lineno-1:n.end_lineno]);spans[name]=dict(line=n.lineno,end_line=n.end_lineno,sha256=hashlib.sha256(body.encode()).hexdigest(),source=body)
for name,h in pre['source_sha256s'].items():
 n=fn[name];assert hashlib.sha256(''.join(lines[n.lineno-1:n.end_lineno]).encode()).hexdigest()==h
supervision=dict(binding=dict(path=str(W/'own_rss_binding.json'),sha256=known[W/'own_rss_binding.json']),controls=dict(seal=dict(path=str(W/'binding_controls/seal.json'),sha256=known[W/'binding_controls/seal.json']),terminal_evidence=dict(path=str(CT/'terminal_return.json'),sha256=known[CT/'terminal_return.json'])))
assert not os.path.lexists(W/'prepared_cold.json'), 'Root actual finalize already advanced; do not invent an earlier baseline'
roots=dict(source=str(S),work=str(W),terminal=str(T),control_terminal=str(CT));namespaces={}
for key,root in roots.items():
 files={};dirs=[];links={}
 for folder,ds,ns in os.walk(root,followlinks=False):
  for name in ds+ns:
   p=Path(folder)/name;r=str(p.relative_to(root));s=p.lstat()
   if stat.S_ISREG(s.st_mode):files[r]=sid(p)
   elif stat.S_ISDIR(s.st_mode):dirs.append(r)
   elif stat.S_ISLNK(s.st_mode):links[r]=os.readlink(p)
   else:raise ValueError('unsupported file type')
 namespaces[key]=dict(files=files,directories=sorted(dirs),symlinks=links)
case=json.loads(read(Path(old['case_spec']['path']),old['case_spec']['sha256']));assert case['reference']['active_batches']==250
for name in ('analysis_environment.json','factory_seal.json','source_equivalence.json'):read(S/name)
for q,w in ((Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_reader_20261009/actual_readonly_REPORT.json'),'58b1d0061948b9d76b9d609114b9c8967b88d1b024f797eb78a2ebb8b12b458a'),(Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_reader_20261009/actual_readonly_postterminal_tool_receipt.json'),'415514b5ca5c6ff179c708e2f3055ef74bde31fc4fca4b0d0e976d574d6458ab')):read(q,w)
future={k:None for k in ('Root_actual_closed_EXIT0_observed','actual_tool_result','prepared_cold_sha256','finalization_Root_receipt','controls_whole_joint_admission','finalization_stdout_sha256','finalization_stderr_sha256')}
cfg=dict(status='SOURCE_ONLY_FINALIZATION_POSTTERMINAL_UNREADY',roots=roots,work=str(W),terminal=str(T),factory=pre['factory'],declaration_terminal=dict(path=str(T/'declaration_terminal_return.json'),sha256=known[T/'declaration_terminal_return.json']),original_prepared_sha256=known[W/'prepared.json'],original_prepared_typed_order_floatbits_sha256=td,original_namespaces=namespaces,known_files=pins,expected_supervision=supervision,launch_command=pre['launch_command'],source_derived_handoff_command=pre['source_derived_handoff_command'],future_actual=future,future_cold_RUN_tool=None,reader_not_executed=True)
reader=O/'audit_actual_finalization_readonly.py';rt=reader.read_text();ast.parse(rt);compile(rt,str(reader),'exec',dont_inherit=True,optimize=0)
assert not any(isinstance(n,ast.Call) and (isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','__import__') or isinstance(n.func,ast.Attribute) and n.func.attr in ('execve','import_module','Popen','system')) for n in ast.walk(ast.parse(rt)))
def write(name,d):
 p=O/name;assert not p.exists();p.write_text(d if isinstance(d,str) else json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n');return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
cp=write('finalization_config_SOURCE_ONLY_UNREADY.json',cfg)
ep=write('source_only_scope_and_original_function_spans.json',dict(status='SOURCE_ONLY_FINALIZATION_READER_PREPARED_NOT_EXECUTED',factory=cfg['factory'],original_prepared=dict(path=str(W/'prepared.json'),sha256=known[W/'prepared.json']),whole_original_typed_order_floatbits_sha256=td,source_spans=spans,exact_required_supervision=supervision,root_namespace_baseline_counts={k:dict(regular_files=len(v['files']),directory_paths=len(v['directories']),symlinks=len(v['symlinks'])) for k,v in namespaces.items()},only_allowed_actual_increments={'work':['prepared_cold.json'],'terminal':['finalization.stdout','finalization.stderr','finalization_terminal_return.json'],'source':[],'control_terminal':[]},all_old_regular_seven_fields_exact_required=True,all_directory_paths_and_symlinks_exact_required=True,original_types_order_float64bits_and_serialized_byte_inverse_required=True,original_all_inputs_spec_math_budgets_config_mfiles_runtime_source_env_caps_unchanged=True,legacy_case_spec_active_batches=case['reference']['active_batches'],separate_original92_reference_contract_2000_and_eight_gates_unchanged=True,cli_handoff_prelaunch_TEMPLATE_not_execution=pre,all_future_actual_None=True,reader_AST_compile_only_not_executed=True,no_business_source_modified=True,prepared_cold_or_finalization_actual_not_read=True))
rp=write('REPORT.txt','''真实finalization后验SOURCE-ONLY scope/reader模板准备完成，未执行reader或business/helper/import/ctor/finalize/native。原F59d0 finalize5args、P14普通导入CLI/handoff按Root0ab源计划完整引用；原模板含future工具/newpreparedcold None，不把source-derived command当syscall trace或已执行。

已存在的原prepared35f、binding4e、controlseal339f、CT04f、DTd0精确绝对路径+SHA固定。唯一预期新增metadata为own_child_supervision={binding,controls:{seal,terminal_evidence}}，descriptor类型/键序/路径/值全exact。删除此字段必须whole原prepared严格type/order/list/value/float64 bit一致（typed-tree全遍历，bool/int不混，float使用!d bits），且按原indent2 JSON再序列化完全恢复原prepared原字节35f。inputs/spec/math/budgets/config/localfiles/runtime/source/env/caps及legacy reference250全部保持；另original92 contract2000active+0101..2100及八门保持，没有override或信用。

完整SOURCE/WORK/TERM/CT既有regular七field和dirs/links路径基线在config：新WORK仅prepared_cold.json，TERM仅finalization.stdout/.stderr/_terminal_return.json三个记录；其它旧regular严格七field全相同，directory paths/link targets保持，不虚称有意新增文件父目录mtime不变。Root真正builtin int0 CLOSED后才可绑定preparedcold实际SHA、完整distinct stdout/stderr和Rootfinalization receipt（AXMAT_ROOT_ACTUAL_COLD_FINALIZATION_RETURN_V1），整个stdout必须原classification/oldnewpins/三个False完全一致；transport_started仍False。futureactual和futurecold全部None，source master不可当PASS。

既有controls完整源后验58b1/真实4155作为已知来源保留，Root全joint仍须实际供给qualified pin；这个模板不重复controls业务。读取范围只有source/小metadata/既有control报告和身份基线，无35GB内容重读。全部输出固定TMP。真finalize只形成冷运行输入，不启动solver，不给予native512或AAA精度/ABA信用。原预算和2000八门不可改变。

准确原函数行/全文引用/expected schema/完整根namespace范围见source_only_scope_and_original_function_spans.json；futureconfig及未执行reader源码同目录，真实源准备工具收据另封存。
''')
res=dict(status='SOURCE_ONLY_FINALIZATION_SCOPE_READER_UNREADY_NOT_EXECUTED',reader=dict(path=str(reader),sha256=hashlib.sha256(reader.read_bytes()).hexdigest(),bytes=reader.stat().st_size),config=cp,scope=ep,report=rp,reader_executed=False,business_executed=False,project_written=False,all_actual_future_None=True)
write('source_preparation_result.json',res);print(json.dumps(res,ensure_ascii=False,sort_keys=True))

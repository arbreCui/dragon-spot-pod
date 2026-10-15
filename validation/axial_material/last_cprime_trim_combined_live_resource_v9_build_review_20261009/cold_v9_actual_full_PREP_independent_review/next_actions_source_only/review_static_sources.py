from pathlib import Path
import ast, hashlib, json, os

OUT=Path('/private/tmp/axmat_v9_cold_next_actions_source_scope_20261009')
ROOT=Path('/Users/wen/spot'); A=ROOT/'validation/artifacts'; V=ROOT/'validation/axial_material'
F=V/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
C=V/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py'
I=V/'cold_owned_specs_last_cprime_trim_component_input_intake_binding_20261009.json'
M=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-input-v5-draft-20261009')
S=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
W=A/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
T=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
CT=A/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-own-rss-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009'
H=V/'combined_cold_own_rss_host_physical_basis_own_pid_peak_20261008.py'
K=V/'combined_cold_own_rss_controls_own_pid_peak_20261008.py'
B=A/'axial-material-production-qualified-AB-rank1-factor-cache-20261007/runtime/production_runner.py'
SUP=V/'cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py'
REC=Path('/private/tmp/axmat_v9_cold_phase_root_recorder_transport_truthful_source_only_20261009/record_actual_phase_terminal.py')
KNOWN={F:'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8',C:'2fa0cb00ec458e9bbbbdf2f15db703a1c0547b08d35f585b6c7e6e6274d06d59',I:'b37b9d5adda1fb4a5ffe0f4a4914d513f38f6f68d480be6145f8d4af041572dc',H:'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7',K:'d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393',B:'844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d',SUP:'ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b',REC:'f14d84493fa81d49b5dfa0749cc72bf4bef96ed8317b99475ed254bd1f0bb3f0',W/'prepared.json':'35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7',S/'declaration.json':'6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c',T/'declaration_terminal_return.json':'d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c',S/'source_equivalence.json':'5dde63576a0d302ebded7b99bbd375637e499817855838342f584c15a1f75dbc',S/'factory_seal.json':'810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce',S/'analysis_environment.json':'0fcfa0c95e4909521f1b14860baff7d23ae3f222bb76408ce4d5841234ce2b6d'}
PINS={}; texts={}; identities={}
def identity(p):
    st=p.lstat(); assert p.is_file() and not p.is_symlink(),str(p)
    return [getattr(st,'st_'+k) for k in ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')]
def pin(p,wanted=None):
    p=Path(p); before=identity(p); data=p.read_bytes(); after=identity(p); assert before==after,str(p)
    sha=hashlib.sha256(data).hexdigest()
    if wanted is not None: assert sha==wanted,(str(p),sha,wanted)
    identities[str(p)]=before; PINS[str(p)]={'path':str(p),'sha256':sha,'bytes':len(data)}
    if p.suffix=='.py': texts[str(p)]=data.decode()
    return data
def read(p):return json.loads(pin(p))
def dump(name,value):
    p=OUT/name; assert not p.exists(); p.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n'); return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def inventory(text,functions_only=False):
    lines=text.splitlines(keepends=True); ans={}
    def walk(nodes,parent=''):
        for n in nodes:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                name=parent+n.name
                start=min([n.lineno]+[d.lineno for d in n.decorator_list]); b=''.join(lines[start-1:n.end_lineno]).encode()
                if not functions_only or isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    ans[name]={'line':start,'end_line':n.end_lineno,'source':b,'ast':ast.dump(n,include_attributes=False)}
                walk(n.body,name+'.')
    walk(ast.parse(text).body); return ans
for p,w in KNOWN.items():pin(p,w)
prepared=read(W/'prepared.json'); decl=read(S/'declaration.json'); env=read(S/'analysis_environment.json')
dt=read(T/'declaration_terminal_return.json'); proof=read(S/'source_equivalence.json')['patches']['production_runner.py']
assert prepared['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in prepared
assert dt['actual_tool_result']['exit_code']==0 and type(dt['actual_tool_result']['exit_code']) is int
assert dt['declaration']==prepared['declaration'] and dt['source']=={'path':str(F),'sha256':KNOWN[F]}
case=read(prepared['case_spec']['path']); assert PINS[prepared['case_spec']['path']]['sha256']==prepared['case_spec']['sha256']
assert case['reference']['active_batches']==250
checks={}; def_proof={}
for p in (F,C):
    mother_sha='76ac45bd9fc22d7a23abea6f46f182207fbea4f34d6be421cd68afbe6fc71a9e' if p==F else '040f3ec2b201eeeba850c5dff72d66604784d99d97bf9f2c6c991e9ceb48d588'
    pin(M/p.name,mother_sha); old=inventory(texts[str(M/p.name)],True); new=inventory(texts[str(p)],True)
    assert old.keys()==new.keys()
    assert all(old[k]['source']==new[k]['source'] and old[k]['ast']==new[k]['ast'] for k in old)
    def_proof[p.name]={'mother':PINS[str(M/p.name)],'candidate':PINS[str(p)],'all_function_source_and_AST_exact':True,'derived_function_count':len(new),'functions':{k:{'line':v['line'],'end_line':v['end_line'],'source_sha256':hashlib.sha256(v['source']).hexdigest()} for k,v in new.items()}}
copied={}
for formal,name,w in ((H,'combined_cold_own_rss_host.py',KNOWN[H]),(K,'combined_cold_own_rss_controls.py',KNOWN[K]),(C,C.name,KNOWN[C])):
    sp=S/name; wp=W/'runtime'/name; pin(sp,w);pin(wp,w); assert sp.read_bytes()==formal.read_bytes()==wp.read_bytes()
    assert prepared['local_files']['runtime/'+name]==w
    copied[name]={'source':PINS[str(formal)],'declaration_copy':PINS[str(sp)],'prepared_runtime_copy':PINS[str(wp)],'prepared_local_file_pin_exact':True}
controller=W/'runtime/production_runner.py';pin(controller,proof['candidate_sha256']);pin(S/'production_runner.py',proof['candidate_sha256'])
assert prepared['local_files']['runtime/production_runner.py']==proof['candidate_sha256']
restored=texts[str(controller)]
for old,new in reversed(proof['replacements']):
    assert restored.count(new)==1;restored=restored.replace(new,old,1)
assert restored==texts[str(B)]
baseinv=inventory(texts[str(B)]); currinv=inventory(texts[str(controller)])
assert baseinv.keys()==currinv.keys()
unchanged=[k for k in baseinv if k not in ('prepare','run')]
assert all(baseinv[k]['source']==currinv[k]['source'] and baseinv[k]['ast']==currinv[k]['ast'] for k in unchanged)
ftext=texts[str(F)]; tree=ast.parse(ftext); const={}
for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        if n.targets[0].id in ('CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER'):const[n.targets[0].id]=ast.literal_eval(n.value)
assert currinv['run']['source'].decode().replace(const['CONSTRUCTOR_AFTER'],const['CONSTRUCTOR_BEFORE'],1).encode()==baseinv['run']['source']
recinv=inventory(texts[str(REC)]); finv=inventory(ftext)
assert recinv['normal_factory_command']['source']==finv['normal_factory_command']['source']
assert recinv['normal_factory_command']['ast']==finv['normal_factory_command']['ast']
assert 'contract["retained_reference"]["active_batches"] != 2000' in ftext
assert 'f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)' in ftext
assert 'original_independent_eight_gates_required' in ftext and 'complete_original_2000_active_reference_batches_required' in ftext
checks.update(factory_consumer_all_80_derived_function_bodies_exact=sum(v['derived_function_count'] for v in def_proof.values())==80,controller_complete_byte_inverse_exact=True,controller_all_non_prepare_run_definitions_byte_AST_exact=True,original_serial_executor_resource_monitor_qualify_aba_exact=all(k in unchanged for k in ('SerialExecutor','resource_monitor','qualify_aba')),run_only_original_constructor_delta_exact=True,copied_host_controls_consumer_sealed_pins_exact=True,pure_Root_recorder_normal_execve_builder_byte_AST_exact=True)
lines={}
for p in (F,H,K,SUP,controller,REC):
    inv=inventory(texts[str(p)]); lines[str(p)]={k:{'line':v['line'],'end_line':v['end_line'],'source_sha256':hashlib.sha256(v['source']).hexdigest()} for k,v in inv.items()}
python=env['executable']; fsha=KNOWN[F]; pr=KNOWN[W/'prepared.json']; dsha=KNOWN[S/'declaration.json']; dtsha=KNOWN[T/'declaration_terminal_return.json']
prefix=('import hashlib,sys,os; from pathlib import Path\n'+'if sys.flags.optimize!=0 or "PYTHONOPTIMIZE" in os.environ: raise ValueError("nonoptimized cold source predicates required")\n'+'sys.dont_write_bytecode=True; '+'p=Path('+repr(str(F))+'); assert hashlib.sha256(p.read_bytes()).hexdigest()=='+repr(fsha)+'; '+'sys.path.insert(0,str(p.parent)); import '+F.stem+' as f; '+'assert Path(f.__file__).resolve()==p; ')
suffix='import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
cli=lambda action:[python,str(F),action,'--factory-sha256',fsha]
templates={
 'prepare-binding':{'launch_argv':cli('prepare-binding')+['--sha256',pr,'--declaration-terminal-sha256',dtsha],'execve_argv':[python,'-c',prefix+'r=f.prepare_binding_in_clean_process('+repr(pr)+','+repr(dtsha)+'); '+suffix],'required_before':[prepared['declaration'],PINS[str(W/'prepared.json')],PINS[str(T/'declaration_terminal_return.json')]],'future_output_sha256':None},
 'run-controls':{'launch_argv_template':cli('run-controls')+['--binding-sha256',None,'--declaration-terminal-sha256',dtsha],'execve_argv_template':[python,str(W/'runtime/combined_cold_own_rss_controls.py'),'run-controls','--binding',str(W/'own_rss_binding.json'),'--binding-sha256',None],'future_binding_sha256':None,'Root_receipt_command_is_actual_copied_controls_argv':True},
 'finalize-cold':{'launch_argv_template':cli('finalize-cold')+['--sha256',pr,'--binding-sha256',None,'--control-seal-sha256',None,'--control-terminal-sha256',None,'--declaration-terminal-sha256',dtsha],'execve_argv_template':[python,'-c',{'prefix':prefix,'call':'r=f.finalize_cold_in_clean_process(','ordered_arguments':[pr,None,None,None,dtsha],'encoding':'comma join repr of each actual SHA string; all null slots require actual qualified pins first','suffix':'); '+suffix}],'complete_future_execve_argv':None},
 'run-AAA':{'launch_argv_template':cli('run-AAA')+['--sha256',None,'--declaration-terminal-sha256',dtsha],'execve_argv_template':[python,'-c',{'prefix':prefix,'call':'r=f.cold_launch_in_clean_process(','ordered_arguments':[None,dtsha],'encoding':'comma join repr of each actual SHA string; null prepared_cold slot requires actual finalized pin first','suffix':'); '+suffix}],'complete_future_execve_argv':None,'actual_controller_call_source':'c.run(OUTPUT/\'prepared_cold.json\',prepared_sha,\'AAA\',None,None)'}
}
unknown={'prepared_Root_receipt_sha256':None,'binding_sha256':None,'binding_Root_receipt_sha256':None,'control_seal_sha256':None,'control_terminal_sha256':None,'prepared_cold_sha256':None,'finalization_Root_receipt_sha256':None,'cold_closeout_seal_sha256':None,'cold_terminal_sha256':None}
future_observation={k:None for k in ('actual_tool_terminal_return_observed','record_written_after_actual_terminal_return','tool_closed','returncode','full_stdout_path','full_stderr_path','stdout_sha256','stderr_sha256','actual_elapsed_seconds','actual_archive_bytes','actual_resources')}
future_observation['actual_tool_result']={k:None for k in ('initial_chunk_id','session_id','terminal_chunk_id','exit_code')}
receipt_rules={'writer_source':PINS[str(REC)],'writer_not_executed':True,'actual_tool_result_exact_keys':['initial_chunk_id','session_id','terminal_chunk_id','exit_code'],'builtin_int_exit_code_required':0,'closed_is_separate_observation_not_actual_tool_key':True,'existing_decl_actual_tool_keys':sorted(dt['actual_tool_result']),'existing_decl_not_cloneable_wholesale_into_controls_actual_tool_result':True,'record_written_only_after_real_native_or_helper_terminal_return':True,'future_observations':{phase:future_observation for phase in ('binding','controls','finalization','cold')},'independent_terminal_roots':{'controls':str(CT),'cold_and_other_phase_records':str(T)},'receipt_names':{'binding':'binding_terminal_return.json','controls':'terminal_return.json','finalization':'finalization_terminal_return.json','cold':'terminal_return.json'},'required_cold_record_fields':['schema','record_producer','actual_tool_terminal_return_observed','record_written_after_actual_terminal_return','actual_tool_result','returncode','command','handoff_command','source','prepared','input_declaration_terminal_evidence','cold_closeout_seal','full_stdout','full_stderr','full_closeout_tail_gate','actual_elapsed_seconds','actual_archive_bytes','actual_resources','scientific_qualification','AAA_accuracy_qualified','ABA_admitted'],'transport_started_only_actual_cold':True,'science_AAA_ABA_credit':False}
controls={'ordered_modes':['positive','oversize','short'],'raw_child_argv_templates':[[python,str(W/'runtime/combined_cold_own_rss_controls.py'),'fixture',m] for m in ('positive','oversize','short')],'allocation_bytes':{'positive':16*2**20,'oversize':576*2**20,'short':16*2**20},'required_stage_statuses':['PASS','FAILED','PASS'],'oversize_required_actual_returncodes':[-15,-9],'oversize_required_actual_error':'own-child 512 MiB RSS cap reached','oversize_live_sampled_peak_min_mib':512,'oversize_not_wall_or_metadata_failure':True,'short_required_own_pid_wait4_peak_min_mib':16,'normal_completion_own_pid_wait4_required':True,'RSS_rule':'observed_peak_rss_mib=max(live ps sample, exact own PID Darwin wait4 ru_maxrss BYTES / 2**20); normal completion 0<peak<512','all_actual_groups_no_longer_live_required':True,'claim_exclusive_and_no_retry':True,'control_tail_fields':['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']}
caps={'rss_cap_mib':512,'control_stage_seconds':60,'control_total_seconds':120,'control_archive_reserve_bytes':64*2**20,'cold_total_seconds':43200,'min_free_bytes':8*2**30,'history_cap_bytes':96*2**30,'threads':1,'children_at_once':1,'retries':0,'production_budgets':prepared['budgets'],'native_and_host_stages_all_real_returncode_zero_required':True,'controls_oversize_is_expected_nonzero_only':True,'no_additional_time_by_execve_or_make_executor':True}
environment={'analysis_environment':PINS[str(S/'analysis_environment.json')],'executable':python,'python_version':env.get('version'),'producer_numpy':{k:env.get(k) for k in ('numpy_version','numpy_root')},'full_environment_and_scipy_target_validation_required':True,'PYTHONPATH':str(A/'axial-material-cold-cp314-scipy-dependency-20261008/target'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE_absent_and_sys_flags_optimize_zero_required':True,'thread_environment':{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}}
for p,before in identities.items(): assert identity(Path(p))==before,p
evidence={'classification':'SOURCE_ONLY_STATIC_NEXT_ACTIONS_NO_FIXTURE_OR_NATIVE_CREDIT','read_only_selected_files_stable_seven_fields':True,'source_checks':checks,'function_body_inverse':def_proof,'controller_complete_inverse':{'baseline':PINS[str(B)],'candidate':PINS[str(controller)],'source_equivalence':PINS[str(S/'source_equivalence.json')],'replacement_count_derived':len(proof['replacements']),'unchanged_definitions':unchanged,'whole_inverse_byte_exact':True},'copied_sources':copied,'source_function_line_references':lines,'known_actual_predecessor_pins':{'declaration':PINS[str(S/'declaration.json')],'declaration_terminal':PINS[str(T/'declaration_terminal_return.json')],'prepared':PINS[str(W/'prepared.json')],'prepared_case_spec':PINS[prepared['case_spec']['path']]},'future_actual':unknown,'root_paths':{'source':str(S),'work':str(W),'cold_terminal':str(T),'control_terminal':str(CT)},'controls':controls,'caps':caps,'environment':environment,'legacy_native_reference_contract':case['reference'],'subsequent_accuracy_policy':{'active_batches':2000,'statepoint_names':'statepoint.0101.h5 through statepoint.2100.h5 inclusive','legacy_case_active_batches_250_not_overridden':True,'gate_keys':['input_equivalence','source_convergence','block_stability','statistical_resolution','keff','scalar_flux','nu_fission','currents_balance_symmetry'],'all_require_new_independent_qualification':True,'old_nu_fission_fail_not_reusable':True,'authoritative_existing_gate_scope_report':'/private/tmp/axmat_v9_cold_and_full_goal_gates_readonly_audit_20261009/REPORT.txt'},'pins':PINS}
evidence['subsequent_accuracy_policy'].update(mandatory_retained_reference_contract_source={'path':str(F),'function':'declare','admitted_component':'original92','field':'future_contract.retained_reference','requirement_source':'active_batches != 2000 or active_statepoints != [f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)] raises ValueError','line_reference':lines[str(F)]['declare']},declaration_explicit_flags=['original_independent_eight_gates_required','complete_original_2000_active_reference_batches_required','reference_reassessment_pending'],inherited_CE_or_accuracy_credit=False)
ev=dump('source_scope_evidence.json',evidence);cmd=dump('next_actions_exact_argv_templates_and_future_None.json',{'classification':'SOURCE_ONLY_NOT_EXECUTABLE_WITH_NULL_SLOTS','normal_factory_command_function_source':finv['normal_factory_command']['source'].decode(),'argv_templates':templates,'future_actual':unknown,'receipt_rules':receipt_rules})
report='''纯源码 next-actions 复核完成；只读源/小 JSON，仅 TMP 写报告。没有执行 factory/helper/import/API/constructor/controls/native/Root writer。本表不提供 fixture、live MRO、RSS 或科学信用。

1 prepare-binding：当前 canonical F59d0、consumer2fa0、bindingb37 与真实 prepared35f / declaration6d937 / Root声明DTd0一致。以精确CLI进入P14普通导入的 -c execve，先copied当前controller再frozen supervisor；完整原prepared/source/INPUT环境/资源/所有expected owners验真，形成own_rss_binding.json及真实MRO/source proof。无需新业务源或新supervisor。成功原返回仍INPUT_ONLY_NO_FIXTURE_CREDIT；Root真实0与全stdout/stderr后记录binding终态，未来bindingSHA仍None。

2 run-controls：F只execve copied controls脚本，实际positive→oversize→short，共3子进程顺序运行。16MiB正例PASS、576MiB原512 RSS分支拒绝FAILED(-15/-9)、16MiB短进程PASS，全部实际group清理、独立PID/原日志/watchdog/完整seal。正常ownPID峰值=max(livePS,kernelwait4)<512MiB；Darwin wait4原BYTES不可拿累积RUSAGE_CHILDREN代替，short ownPID kernel峰值>=16MiB。oversize应liveRSS>=512触原错误，不能墙钟失败冒充；预期拒绝允许kernelreceipt缺失None，不能伪造0。每stage<=60s/whole<120s/archive<64MiB/thread1/child1/retry0，原动态history96GiB/free8及reservation保留。

controls Rootterminal必须在独立CT sibling，不在WORK里；command是实际copied controls argv，另留F启动CLI。actual_tool_result恰四keys(initial_chunk_id,session_id,terminal_chunk_id,exit_code)，builtin int0；closed留独立observation字段。旧DTd0实际5keys含closed不能整包直接克隆到controls receipt。完整stdout=result+四tail exact，seal和全三个实际control/wait4/原budget资源验真后才finalize。

3 finalize-cold：真正qualified binding+control seal+Rootcontrols terminal+declreceipt重新验真；只为原prepared增加own_child_supervision={binding,controls:{seal,terminal_evidence}}。删除这个key必须deep-equal全部原prepared。真实0后Root记录prepared_cold和finalization stdout；所有未来pins仍None。本阶段无AAA精度资格。

4 run-AAA：新prepared_cold实际pin、declreceipt、全新AAA/archives/training不存在guard，P14 canonical normal execve再次完整环境/INPUT/resource/MRO/controls查验，调用原 c.run(prepared_cold.json,sha,'AAA',None,None)。不要用hardcoded prepared.json的host.launch()。setup120/bootstrap axial4200/radial600/maps radial300/axial4200/host120/max100/whole43200保持；所有native/host原ownPID512MiB/thread1/child1/retry0，stage真0、原marker/selector/cache/P0-P2/物理basis和whole sealed namespaces必须实际通过。返回WAITING_REFERENCE/AAA VALID_MET、连续1..N<=100首MET，四tail+完整cold closeout seal；失败冻结no retry并保留真实failedtool/完整输出。

仅真实cold工具EXIT0及原完整门后Root可封外部冷终态（CLI与完整 -c handoff argv都必须exact）。既有f14d纯Rootwriter可沿用，原normal_factory_command字节+AST与F完全一致，transport_started只有实际cold为True，其余False；所有science/AAAaccuracy/ABA仍False。writer未执行，future observations/SHAs全部None。prepared Rootreceipt正由Root完成，本表不预填其未知pin。

静态完整性：factory55个函数(53top+2nested)+consumer25=80全部byte+AST与UNREADY母本exact；copied host/controls/consumer均formal/SOURCE/prepared localfiles同pin。controller67ae4全源码逆向回BASE844fe exact；除prepare/run外全部定义byte+AST exact；run只有真正constructor替换；SerialExecutor/resource_monitor/qualify_aba完整原源码保持。host未来live admission要求canonical production_runner、OwnRSSSerialExecutor继承原SerialExecutor、真实globals/module owners/compiled callable和DynamicHistoryResources，禁止overlay。本审静态未制造这些live通过。

当前case_spec reference.active_batches确为250 legacy原native contract，未override；另F原declare读取components['original92']['future_contract']，强制retained_reference.active_batches==2000及完整statepoints0101..2100，声明原八门及完整2000active required/reference_reassessment_pending，inheritedCE/qualification均False。这是现有actual original92合同层，与legacy native字段分层保持。cold真完成仍WAITING_REFERENCE，独立完整2000active及input_equivalence/source_convergence/block_stability/statistical_resolution/keff/scalar_flux/nu_fission/currents_balance_symmetry八门必须另外真实准入。旧nu-fission3.798223%>3% FAIL不复用；old250/source-only或build INPUT都不提供solver/精度信用。完整权威引用在既有gate report及本次evidence内，35GB未读。

精确argv：next_actions_exact_argv_templates_and_future_None.json。prepare-binding的CLI/-c程序已由真实已有pin完整形成；controls/finalize/cold明确null slots，不能当已运行argv，Root按实际qualified新pin逐项填。源码函数行及全受限来源freshSHA：source_scope_evidence.json。独立terminal根与SOURCE/WORK均distinct。
'''
rp=OUT/'REPORT.txt';assert not rp.exists();rp.write_text(report)
result={'classification':'SOURCE_ONLY_STATIC_REVIEW_PASS','evidence':ev,'argv_templates':cmd,'report':{'path':str(rp),'sha256':hashlib.sha256(rp.read_bytes()).hexdigest()},'checks':checks,'future_actual_all_unknown_None':True,'candidate_business_executed':False,'fixture_executed':False,'project_written':False}
dump('static_source_result.json',result)
print(json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False))

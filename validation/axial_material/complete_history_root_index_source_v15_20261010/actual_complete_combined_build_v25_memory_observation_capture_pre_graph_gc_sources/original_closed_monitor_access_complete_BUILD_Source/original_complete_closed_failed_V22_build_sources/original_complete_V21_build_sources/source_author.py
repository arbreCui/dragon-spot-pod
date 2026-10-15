import pathlib,json,hashlib,stat,ast,tempfile
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_combined_build_v20_sources'
S=D/'sealed_actual_bound_SOURCE_generation'
P=pathlib.Path(tempfile.mkdtemp(prefix='axmat_v21_complete_build_generator_SOURCE_ONLY_design_20261010_',dir='/private/tmp'))
def pin(path,sha=None):
 p=pathlib.Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 data=p.read_bytes();t=p.lstat();assert before==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 h=hashlib.sha256(data).hexdigest()
 if sha:assert h==sha,(str(p),h)
 return data,dict(path=str(p),sha256=h,identity=before)
source_inputs=[]
base,basepin=pin(S/'generate_build_host.py','c8cf1a7c0a3e60c4cfb2edfc88e496e9fedccb25330c11c5bbb7421d23c52f72');source_inputs.append(basepin)
host,hostpin=pin(D/'combined_build_host.py','d5fa7063b8031d5efecd50e157062e7b2faae771788fe105f2d8486d37f19128');source_inputs.append(hostpin)
proof_data,proofpin=pin(S/'Root_finite_build_host_source_inverse.json');source_inputs.append(proofpin);hp=json.loads(proof_data)
cf2,cf2pin=pin(hp['parent_path'],hp['parent_sha256']);source_inputs.append(cf2pin)
ip=hp['original_cf2c_to_37d_thirteen_change_inverse']
ancestor,ancestorpin=pin(ip['parent_path'],ip['parent_sha256']);source_inputs.append(ancestorpin)
inverse=host.decode()
for c in reversed(hp['changes']):assert inverse.count(c['after'])==c['count'];inverse=inverse.replace(c['after'],c['before'])
assert len(hp['changes'])==17 and inverse.encode()==cf2
inverse=cf2.decode()
for c in reversed(ip['changes']):assert inverse.count(c['after'])==c['count'];inverse=inverse.replace(c['after'],c['before'])
assert len(ip['changes'])==13 and inverse.encode()==ancestor
gp_data,gppin=pin(S/'Root_finite_build_generator_source_inverse.json');source_inputs.append(gppin);gp=json.loads(gp_data)
frozen19,p19pin=pin(S/'frozen_parent_generate_build_host_v19.py',gp['parent_source']['sha256']);source_inputs.append(p19pin)
inverse=base.decode()
for c in reversed(gp['changes']):assert inverse.count(c['after'])==c['count'];inverse=inverse.replace(c['after'],c['before'])
assert len(gp['changes'])==3 and inverse.encode()==frozen19
text=base.decode();changes=[]
def change(before,after,count):
 global text
 assert text.count(before)==count,('before count',before[:100],text.count(before),count)
 text=text.replace(before,after);changes.append(dict(before=before,after=after,count=count))
change('V20','V21',19)
change('v20','v21',16)
change('566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3','023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',1)
oldline="TARGET_SHA = '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'\n"
newline=oldline+"""HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
HELPER_SHA = 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
HELPER_Q = BASE/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json'
HELPER_Q_SHA = '29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'
"""
change(oldline,newline,1)
change('# The first eleven mappings are fixed SOURCE bindings; six mappings require actual closed PREP evidence.','# The first fifteen mappings are fixed SOURCE bindings (including four admitted helper/Q literals); six mappings require actual closed PREP evidence.',1)
oldend="('AXMAT_V17_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1','AXMAT_V21_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',1)]"
newend="""('AXMAT_V17_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1','AXMAT_V21_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',1),
('combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py','combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',1),
('bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',HELPER_SHA,1),
('Root_actual_complete_graph_helper_controls_admission_v17.json','Root_actual_complete_graph_private_verifier_helper_admission_v21.json',1),
('d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8',HELPER_Q_SHA,1)]"""
change(oldend,newend,1)
old="    target_data, target_pin = pin(TARGET,TARGET_SHA)\n"
new=old+"""    helper_data, helper_pin = pin(HELPER,HELPER_SHA)
    q_data, q_pin = pin(HELPER_Q,HELPER_Q_SHA)
    q = json.loads(q_data)
    if q['schema']!='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21' or q['status']!='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21':
        raise ValueError('actual admitted V21 helper metadata Q required')
    if {k:q['helper'][k] for k in ('path','sha256','identity')}!=helper_pin or q['helper']['size_bytes']!=147870 or len(helper_data)!=147870:
        raise ValueError('exact installed helper and actual joint Q SOURCE binding required')
    scope=('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','supervisor_class_or_MRO_modified','profile_used')
    if any(q[k] is not False for k in scope):
        raise ValueError('actual helper metadata only Q scope required')
"""
change(old,new,1)
change("    return old,ip,[old_pin,inverse_pin,ancestor_pin,target_pin]","    return old,ip,[old_pin,inverse_pin,ancestor_pin,helper_pin,q_pin,target_pin]",1)
old="            actual_V21_creation_trace_sha256=None,host_generated=False,business_executed=False,\n"
new="""            actual_V21_creation_trace_sha256=None,actual_V21_source_admission_sha256=None,
            actual_V21_Root_terminal_sha256=None,actual_V21_namespace_manifest_sha256=None,
            metadata_binding_parameter_count=9,metadata_only_no_ART_output_read=True,
            host_generated=False,business_executed=False,
"""
change(old,new,1)
old="""    if len(sys.argv)!=3 or Path(sys.argv[1])!=SUMMARY or re.fullmatch('[0-9a-f]{64}',sys.argv[2]) is None:
        raise ValueError('one actual fixed Root closed PREP summary path and full SHA required; no placeholder binding')
"""
new="""    if len(sys.argv)!=10 or Path(sys.argv[1])!=SUMMARY or any(re.fullmatch('[0-9a-f]{64}',value) is None for value in sys.argv[2:]):
        raise ValueError('nine mandatory actual PREP metadata arguments required: summary path, summary SHA, Root terminal SHA, namespace SHA, declaration SHA, source_admission SHA, formal PREP terminal SHA, complete graph SHA, complete creation trace SHA; no placeholder binding')
"""
change(old,new,1)
old="    terminal, terminal_pin = metadata_reference(s['Root_actual_terminal'],ROOT_TERMINAL)\n"
new=old+"""    if terminal_pin['sha256']!=sys.argv[3]:
        raise ValueError('actual Root terminal must equal required argv pin')
"""
change(old,new,1)
old="    namespace, namespace_pin = metadata_reference(s['namespace_manifest'],NAMESPACE)\n"
new=old+"""    if namespace_pin['sha256']!=sys.argv[4]:
        raise ValueError('actual complete namespace must equal required argv pin')
"""
change(old,new,1)
old="""        'actual_prep_terminal':output_reference(s['formal_PREP_terminal'],TERMINAL+'/declaration_terminal_return.json')}
    for key,ref in desired.items():
        folder = TERMINAL if key=='actual_prep_terminal' else OUT
"""
new="""        'actual_prep_terminal':output_reference(s['formal_PREP_terminal'],TERMINAL+'/declaration_terminal_return.json'),
        'actual_source_admission':output_reference(ns[SOURCE]['files']['source_admission.json'],SOURCE+'/source_admission.json')}
    required_output_arg_pins={'actual_declaration':sys.argv[5],'actual_source_admission':sys.argv[6],'actual_prep_terminal':sys.argv[7],'actual_complete_input_graph':sys.argv[8],'actual_complete_creation_trace':sys.argv[9]}
    if any(desired[key]['sha256']!=value for key,value in required_output_arg_pins.items()):
        raise ValueError('all five actual prepared outputs must equal required argv pins')
    if 'actual_source_admission' in s and s['actual_source_admission']!=desired['actual_source_admission']:
        raise ValueError('actual source_admission summary and complete namespace pin differ')
    for key,ref in desired.items():
        folder = TERMINAL if key=='actual_prep_terminal' else SOURCE if key=='actual_source_admission' else OUT
"""
change(old,new,1)
change("            checked_source_pins=sources,fixed_retarget_count=11,closed_actual_binding_retarget_count=6,","            checked_source_pins=sources,fixed_retarget_count=15,closed_actual_binding_retarget_count=6,",1)
old="        checked_source_pins=sources,actual_Root_closed_PREP_summary=summary_pin,\n"
new="""        checked_source_pins=sources,actual_Root_closed_PREP_summary=summary_pin,
        actual_required_metadata_argv=list(sys.argv[1:]),metadata_binding_parameter_count=9,
        actual_source_admission_output_pin_from_complete_namespace=desired['actual_source_admission'],
"""
change(old,new,1)
tree=ast.parse(text)
inverse=text
for c in reversed(changes):assert inverse.count(c['after'])==c['count'],('inverse count',c['after'][:100]);inverse=inverse.replace(c['after'],c['before'])
assert inverse.encode()==base
def topfn(source):return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
a=topfn(base.decode());z=topfn(text)
assert list(a)==list(z)
unchanged=[name for name in a if a[name]==z[name]]
assert set(unchanged)=={'pin','metadata_reference','output_reference','write_new'}
# Static literal substitutions: do not call or evaluate candidate generator APIs.
def constant(name):
 n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets));return n.value
fixed=constant('FIXED');dynamic=constant('DYNAMIC_SOURCE_TOKENS')
assert isinstance(fixed,ast.List) and len(fixed.elts)==15 and isinstance(dynamic,ast.List) and len(dynamic.elts)==6
for node in fixed.elts+dynamic.elts:
 before=ast.literal_eval(node.elts[0]);count=ast.literal_eval(node.elts[2]);assert cf2.decode().count(before)==count
assert "runner.execute(HOST/'run','build',command,WHOLE_CAP)" in host.decode()
assert "support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))" in host.decode()
assert "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in host.decode()
labels=next(ast.literal_eval(n.value) for n in ast.parse(host).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED_LABELS' for t in n.targets))
commands=next(ast.literal_eval(n.value) for n in ast.parse(host).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED_COMMANDS' for t in n.targets))
assert labels==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'] and len(commands)==5
for key in ['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']:assert key in text
copies={'frozen_parent_generate_build_host_v20.py':base,'frozen_parent_combined_build_host_v20.py':host,'frozen_cf2c_combined_build_host_v17.py':cf2,'frozen_cf2c_to_37d_source_inverse.json':json.dumps(ip,ensure_ascii=False,indent=2).encode()+b'\n','frozen_37d_normal_prepare_host.py':ancestor,'frozen_v20_generator_source_inverse.json':gp_data}
for name,data in copies.items():(P/name).write_bytes(data)
(P/'generate_build_host.py').write_text(text)
source_proof=dict(schema='AXMAT_V21_FULL_BUILD_GENERATOR_SOURCE_ONLY_FINITE_INVERSE_V1',status='SOURCE_ONLY_TEMPLATE_NOT_EXECUTED_NOT_BOUND',parent_generator=basepin,candidate_generator=dict(path=str(P/'generate_build_host.py'),sha256=hashlib.sha256(text.encode()).hexdigest(),size_bytes=len(text.encode())),finite_generator_change_count=len(changes),changes=changes,complete_full_byte_inverse_to_c8cf=True,parent_c8cf_three_change_full_byte_inverse_to_dc48_verified=True,V20_bound_host_d5fa_seventeen_change_full_byte_inverse_to_cf2c_verified=True,cf2c_thirteen_change_full_byte_inverse_to_37d_verified=True,actual_future_host_fixed_hunks=15,actual_future_host_dynamic_hunks=6,actual_future_host_total_hunks=21,four_additional_helper_and_Q_literals_only=True,all_original_host_algorithm_and_guard_and_MRO_bytes_retained_by_finite_string_replacement=True,unchanged_generator_functions=unchanged,changed_generator_functions=['original_source_checks','main'],checked_existing_SOURCE_inputs=source_inputs,existing_helper_Q_binding=dict(helper_sha256='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7',Q_sha256='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'),canonical_V21_READY_SHA_supplied_by_Root='023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',candidate_canonical_currently_not_installed_or_executed_by_this_task=True,future_actual_PREP_pins_not_filled=True,source_generator_not_imported_or_executed=True,binding_branch_not_run=True,normal_host_not_generated=True,project_helper_guard_API_business_numeric_build_not_executed=True,ART_payload_not_read=True)
(P/'source_inverse_proof.json').write_text(json.dumps(source_proof,ensure_ascii=False,indent=2)+'\n')
report=dict(schema='AXMAT_V21_COMPLETE_BUILD_GENERATOR_SOURCE_ONLY_DESIGN_V1',status='UNREADY_SOURCE_TEMPLATE_AWAIT_ACTUAL_ROOT_V21_CLOSED_SUCCESSFUL_PREP',candidate_generator=source_proof['candidate_generator'],required_metadata_argument_order=['actual_fixed_Root_V21_PREP_summary_path','actual_full_summary_sha256','actual_Root_closed_terminal_sha256','actual_complete_namespace_manifest_sha256','actual_declaration_sha256','actual_source_admission_sha256','actual_formal_PREP_terminal_sha256','actual_complete_input_graph_sha256','actual_complete_creation_trace_sha256'],required_root_summary_schema='ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1',required_root_summary_status='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD',Root_terminal_must_be_exact_integer0_closed_no_session_no_repoll=True,all_five_prepared_namespaces_required=True,source_admission_pin_taken_from_exact_full_SOURCE_namespace_with_all_seven_integer_OS_fields=True,summary_source_admission_if_present_must_equal_namespace=True,mandatory_future_PREP_argument_values=None,all_original_five_stages=labels,all_five_exact_static_commands_preserved=True,raw_four_stage_logs_before_binary_identity_gate_preserved=True,all_five_inner_watchdogs_and_full_seal_and_four_tails_preserved=True,source_archive_dynamic_inventory_and_prepared_SOURCE_TERMINAL_inventory_preserved=True,fixed_helper_Q_retarget_count=4,future_host_total_finite_hunks=21,caps=dict(outer_whole_seconds=1800,inner_stage_seconds=600,rss_mib=512,joint_HOST_SOURCE_OUT_TERMINAL_SOURCE_ARCHIVE_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0),genuine619_705_production_bounded_resource_guard_and_MRO_unchanged=True,original_component_seal_b6b3_and_terminal_ad1d_unchanged=True,original_support_3c1856_unchanged=True,new_actual_build_SOURCE_root=str(B/'actual_complete_combined_build_v21_sources'),new_actual_build_HOST='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v21-20261010',all_six_future_business_FACTORY_pins_remain_None_before_actual_business_binding=True,failed_V20_namespace_not_reused_or_retried=True,build_success_or_whole_INPUT_or_native_or_science_not_qualified=True,business_executed=False,helper_API_or_guard_called=False,ART_read_or_written=False,canonical_or_D_or_E_written=False,future_BINDING_not_run=True,normal_host_generated=False)
(P/'SOURCE_DESIGN_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
steps='''V21 完整五阶段 build generator 只源码模板接线；本包不是 READY、不是业务或构建结果。

精确基线：
B/actual_complete_combined_build_v20_sources/combined_build_host.py，SHA d5fa7063b8031d5efecd50e157062e7b2faae771788fe105f2d8486d37f19128。
生成器 B/actual_complete_combined_build_v20_sources/sealed_actual_bound_SOURCE_generation/generate_build_host.py，SHA c8cf1a7c0a3e60c4cfb2edfc88e496e9fedccb25330c11c5bbb7421d23c52f72。
新 generator Source 全字节逆回 c8cf；c8cf 3 changes 逆回 dc48；d5fa host 17 changes 逆回 cf2c，再13 changes 逆回37d。原完整 host 算法、检查次序、guard/MRO、资源和stage不会改写。
V21 将原17个 host retarget 增加4个 helper/Q literal substitutions 共21（15 fixed+6真实PREP动态），新helperdc01/newQ29ac。原 component b6b3/ad1d、3c1856 support、真实619/705/production/bounded/resource保持。

必须先完成的真实步骤：
1. 安装并独审 Root固定 READY canonical Source：/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py，SHA023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5。安装 exact Source/7ID、joint helper Q 与六未来业务 pins=None；本包不安装、不执行该 Source。
2. 在 V21 全新 PREP namespace 正常执行一次完整 PREP，取得真实 Root integerEXIT0/CLOSED、正式 declaration_terminal_return、完整 declaration、source_admission、input_graph、creation trace。
3. Root仅META封存完整H/SOURCE/OUT/TERMINAL/PREP_SOURCE五namespace与全部原输入 fullEOF SHA/精确7ID，并保存真实 Root成功terminal、summary/namespace schema V21。必须有 SOURCE/files/source_admission.json 完整真实pin；不能以 Source PASS或helper Q替代PREP0。
4. 独立复核真实 PREP保存证据；从该同一 Root summary/namespace取得九个必需生成器参数。

未来仅标准库 Source render 的参数顺序（这里所有未来实际 SHA 均未填写）：
generate_build_host.py
  B/actual_complete_combined_prepare_v21_receipts/Root_actual_complete_combined_prepare_summary.json
  actual SUMMARY_SHA
  actual ROOT_TERMINAL_SHA
  actual NAMESPACE_SHA
  actual DECLARATION_SHA
  actual SOURCE_ADMISSION_SHA
  actual FORMAL_PREP_TERMINAL_SHA
  actual COMPLETE_GRAPH_SHA
  actual COMPLETE_CREATION_TRACE_SHA

生成器读取 Source 和 Root保存META，拒绝直接读取 ART；五个 prepared输出path/SHA/七项typed identity只从Root真实完整namespace交叉核对，source_admission来自SOURCE而非OUT。真实 Root terminal必须整数0、closed/no live session/no repoll，全部原caps/flags/type完整保留。源候选只有在真实参数全部匹配后才render host和fullinverse；不能填None、零散旧V20成功哈希或预造PREP成功。
请复制本sealed设计包到新的TMP生成位置后才运行该标准库生成器；不要修改本已封存包。

render后的入口候选：新TMP/combined_build_host.py 与 Root_finite_build_host_source_inverse.json。Root需独立有限SOURCE复核后，byte-exact安装到B/actual_complete_combined_build_v21_sources，完整SOURCE inventory前后动态pin并freeze；正常HOST为新 axial-material-complete-combined-build-host-v21-20261010，不能复用旧失败V20。

原host固定输入完整范围：
support、READYcanonical、原v15 component source+seal+terminal；新helper/newQ；所有build SOURCE_ARCHIVE文件；
真实V21 declaration/formalPREPterminal/input_graph/creationtrace；所有 prepared SOURCE（含source_admission）和TERMINAL文件；
真实RootPREP terminal与固定summary；真实original619与resource Module Source。运行前后全部不变。
资源联合范围为HOST+SOURCE+OUT+TERMINAL+buildSOURCE_ARCHIVE（2GiB），正常outerwhole1800，五inner每项600，RSS512/history96GiB/free8GiB/1thread/1child/0retry。
完整五stage：build/link、metadata/objects、metadata/executable、metadata/dependencies、audit/audit。每个原command必须精确且PASS，所有5watch/raw4log-before-identity/fullseal+runtime identity/原4tails完整保留。
正常whole build不代替后续完整INPUT、native RSS、AAA原8项、ABA或物理平衡准入。Q只helper元数据资格。
'''
(P/'ROOT_BINDING_STEPS.txt').write_text(steps)
for ref in source_inputs:
 _,again=pin(ref['path'],ref['sha256']);assert again==ref
print(json.dumps({'directory':str(P),'generator_sha256':hashlib.sha256(text.encode()).hexdigest(),'generator_bytes':len(text.encode()),'finite_generator_changes':len(changes),'future_host_hunks':21,'full_generator_inverse_c8cf':True,'host_d5fa_inverse17_cf2c_inverse13_37d':True,'normal_host_generated':False,'future_actual_PREP_pins':None,'project_API_business_numeric_executed':False}))

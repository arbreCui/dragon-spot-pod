from pathlib import Path
import ast, hashlib, json, os, stat, tempfile
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
HD=Path('/private/tmp/axmat_v18_root_prepare_host_source_20261010')
RD=Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010')
HOST=HD/'combined_prepare_host.py'
READY=RD/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'
UNREADY=BASE/'next_complete_combined_v18_source_only_review/sealed_complete_UNREADY_candidate/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py'
PARENT=BASE/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
ORIGINAL=BASE/'actual_combined_prepare_sources/combined_prepare_host.py'
expected={
HOST:'bc5c6fa1118b84641a5a66232080354074b49ad2c59ac809e28ee99cc6faac98',
READY:'5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240',
UNREADY:'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583',
PARENT:'37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3',
ORIGINAL:'310ddc9d4145060b6f6aa0e250dd470ef05aef43c7d4c2b0c234983351d0b434',
HD/'generate_prepare_host.py':'2d90a91f15a4a0cfd4e31de529703b65e0ad91973966f3c3b94576519f8f999a',
HD/'Root_finite_host_source_inverse.json':'6ee30cbc62a1e2d79f39f9da0b0403ab95b53b0b182d6e13dabc04ba35da94a1',
RD/'source_binding_inverse_proof.json':'36bac8dcf1a640be03fe2e851d231cedfef0f7b06dc65afb8a0fb1bc6a4ae0ad',
BASE/'actual_complete_combined_prepare_v17_sources/Root_finite_host_source_inverse.json':'b7f811379aa40f5f81c4e08e4cfa01a4199a1e78684f0ab118d9150748bec67f',
BASE/'next_complete_combined_v18_source_only_review/sealed_independent_source_review/REVIEW.json':'8710ef186d1df881ced05fa30544e51adef9ee21f45b6045ce508f815ccf95a8',
BASE/'next_complete_combined_v18_source_only_review/sealed_independent_source_review/sealed_manifest.json':'fa490b9ee624129631b0d3c5cac0cf236bfc1c941db0b5cddd2f21b5df8af045',
Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'):'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',
BASE/'Root_actual_complete_graph_helper_controls_admission_v17.json':'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8',
BASE/'actual_prepare_sources/prepare_cli_host_v15.py':'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7',
Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py'):'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6',
Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'):'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128',
Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py'):'619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743',
Path('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'):'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022',
}
data={}
records={}
def read_pin(p, sha=None):
    p=Path(p)
    a=p.lstat()
    assert stat.S_ISREG(a.st_mode),str(p)
    b=p.read_bytes()
    z=p.lstat()
    identity=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert identity(a)==identity(z),(str(p),'identity changed during whole EOF read')
    h=hashlib.sha256(b).hexdigest()
    if sha is not None: assert h==sha,(str(p),'SHA mismatch',h,sha)
    return b,dict(path=str(p),sha256=h,size_bytes=len(b),identity7=identity(a))
for p,h in expected.items():data[p],records[p]=read_pin(p,h)
ht=data[HOST].decode();pt=data[PARENT].decode();ot=data[ORIGINAL].decode()
rt=data[READY].decode();ut=data[UNREADY].decode()
hp=json.loads(data[HD/'Root_finite_host_source_inverse.json'])
pp=json.loads(data[BASE/'actual_complete_combined_prepare_v17_sources/Root_finite_host_source_inverse.json'])
rp=json.loads(data[RD/'source_binding_inverse_proof.json'])
for p in (HOST,READY,UNREADY,PARENT,ORIGINAL,HD/'generate_prepare_host.py'):ast.parse(data[p].decode())
def full_inverse(text, changes, count):
    assert len(changes)==count
    value=text
    for r in reversed(changes):
        assert type(r['occurrences']) is int and r['occurrences']>0
        assert value.count(r['new'])==r['occurrences'],(r['new'],'new count')
        value=value.replace(r['new'],r['old'],r['occurrences'])
    return value
assert full_inverse(ht,hp['changes'],9)==pt
assert full_inverse(pt,pp['changes'],11)==ot
assert full_inverse(rt,rp['edits'],2)==ut
assert hp['host_sha256']==records[HOST]['sha256']
assert hp['parent_host_sha256']==records[PARENT]['sha256']
assert hp['factory_sha256']==records[READY]['sha256']
assert hp['unready_source_sha256']==records[UNREADY]['sha256']
assert hp['factory_candidate']==str(READY) and hp['host_candidate']==str(HOST)
assert hp['parent_host']==str(PARENT) and hp['unready_full_scope_source']==str(UNREADY)
assert pp['parent_host_path']==str(ORIGINAL) and pp['parent_host_sha256']==records[ORIGINAL]['sha256']
assert rp['candidate']['sha256']==records[READY]['sha256']
expected_changes=[
('axial-material-complete-combined-prepare-host-v17-20261010','axial-material-complete-combined-prepare-host-v18-20261010'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'),
('feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c',records[READY]['sha256']),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010'),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010'),
('actual_complete_combined_prepare_v17_sources','actual_complete_combined_prepare_v18_sources'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18_DECLARATION_V1'),
('AXMAT_V17_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V18_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1'),
]
assert [(r['old'],r['new']) for r in hp['changes']]==expected_changes
assert all(r['occurrences']==1 for r in hp['changes'])
gt=ast.parse(data[HD/'generate_prepare_host.py'].decode())
gn=next(n for n in ast.walk(gt) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='changes' for x in n.targets))
generated_changes=[]
for i,n in enumerate(gn.value.elts):
    old=ast.literal_eval(n.elts[0])
    if i==2:
        assert ast.dump(n.elts[1])==ast.dump(ast.parse('sha(source)',mode='eval').body)
        new=records[READY]['sha256']
    else:new=ast.literal_eval(n.elts[1])
    generated_changes.append((old,new))
assert generated_changes==expected_changes
def definitions(t):
    a=ast.parse(t)
    return {n.name:ast.get_source_segment(t,n) for n in a.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
rd=definitions(rt);ud=definitions(ut)
assert len(rd)==70 and rd==ud
def global_nodes(t):
    a=ast.parse(t)
    out=[]
    for i,n in enumerate(a.body):
        if i==0 and isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):continue
        if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='DRAFT_STATUS' for x in n.targets):continue
        out.append(ast.dump(n,include_attributes=False))
    return out
assert global_nodes(rt)==global_nodes(ut)
def safe_value(n):
    if isinstance(n,ast.Constant):return n.value
    if isinstance(n,ast.Tuple):return tuple(safe_value(x) for x in n.elts)
    if isinstance(n,ast.BinOp):
        a,b=safe_value(n.left),safe_value(n.right)
        if isinstance(n.op,ast.Mult):return a*b
        if isinstance(n.op,ast.Pow):return a**b
    raise ValueError('unsupported static expression')
def literals(t):
    values={}
    for n in ast.parse(t).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:values[n.targets[0].id]=safe_value(n.value)
            except ValueError:pass
    return values
rv=literals(rt);uv=literals(ut)
assert rv['DRAFT_STATUS']=='READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
assert uv['DRAFT_STATUS']=='UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED'
future=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
assert all(rv[k] is None for k in future)
assert rv['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']=='d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'
assert 'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6' in rt
def path_globals(t,base):
    values=dict(base)
    def pv(n):
        if isinstance(n,ast.Name):return values[n.id]
        if isinstance(n,ast.Constant):return n.value
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Path' and len(n.args)==1:return Path(pv(n.args[0]))
        if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return pv(n.left)/pv(n.right)
        raise ValueError()
    for n in ast.parse(t).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:values[n.targets[0].id]=pv(n.value)
            except (ValueError,KeyError,TypeError):pass
    return values
hpaths=path_globals(ht,{})
rpaths=path_globals(rt,{})
for k in ('SOURCE','OUT','TERMINAL'):assert hpaths[k]==rpaths[k],k
assert hpaths['TARGET']==rpaths['FORMAL_FACTORY']
assert hp['formal_factory']==str(hpaths['TARGET'])
assert hpaths['SOURCE_ARCHIVE']==BASE/'actual_complete_combined_prepare_v18_sources'
assert hpaths['TARGET_SHA']==records[READY]['sha256']
cap=next(n for n in ast.parse(ht).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Tuple))
assert [x.id for x in cap.targets[0].elts]==['WHOLE_CAP','STAGE_CAP','RSS_CAP','ARCHIVE_CAP']
assert safe_value(cap.value)==(1800,600,512,2*2**30)
for k,v in dict(whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0).items():assert hp[k]==v
checks={
'genuine_guard_called': 'helper.guard_admission(full)',
'genuine_class_base_check': 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
'genuine_module_path_checks': 'Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT',
'genuine_resource_class_and_original_reserves': 'resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',
'genuine_instance_check': 'type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources',
'fixed_single_prepare_child_command': "command=[str(support.PYTHON),str(TARGET),'prepare-build']",
'prepare_child_wall_cap_600': "runner.execute(HOST/'run','prepare',command,STAGE_CAP)",
'outer_original_whole_wall_remaining_1800': 'remaining=WHOLE_CAP-(time.monotonic()-started)',
'archive_input_full_pin': "[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]",
'fresh_namespaces_no_retry': 'if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL))',
'no_prepare_terminal_or_build_seal_fabrication': "if os.path.lexists(TERMINAL) or (OUT/'seal.json').exists()",
'input_sha_identity_recheck': "if support.pin(entry['path'],entry['sha256'])!=entry",
'profile_guard': 'sys.getprofile() is not None',
'original_child_typed_exit0_check': "type(watch['returncode']) is not int or watch['returncode']!=0",
'original_one_record_PASS_check': "len(runner.records)!=1 or runner.records[0]['status']!='PASS'",
'original_own_child_and_cleanup_check': "watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True",
'original_rss_less_than512_check': "not 0<=watch['sampled_peak_rss_mib']<RSS_CAP",
}
for k,v in checks.items():assert v in ht,k
assert ht.count('support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))')==2
assert 'roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)' in ht
assert 'threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False' in ht
assert "full.OwnRSSSerialExecutor(HOST,remaining,'COMBINED_PREPARATION',resources)" in ht
ns={}
for k in ('HOST','SOURCE','OUT','TERMINAL'):
    ns[k]={'path':str(hpaths[k]),'lexists':os.path.lexists(hpaths[k])}
assert not any(v['lexists'] for v in ns.values()),ns
before=list(records.values())
for p,h in expected.items():
    _,after=read_pin(p,h)
    assert after==records[p],(str(p),'source changed before/after')
d=Path(tempfile.mkdtemp(prefix='axmat_v18_READY_prepare_host_finite_source_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V18_READY_AND_GENUINE_PREP_HOST_FINITE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_RUNTIME_REQUIRED',source_inputs=before,all_source_whole_sha_identity7_before_after_equal=True,host_inverse_changes=9,host_full_inverse_bc5c_37d_exact=True,parent_inverse_changes=11,parent_full_inverse_37d_310dd_exact=True,READY_inverse_changes=2,READY_full_inverse_5c4b_ecfd_exact=True,all_70_function_class_definitions_byteexact_to_ecfd=True,other_globals_and_nodes_exact_to_ecfd_except_doc_and_status=True,finite_generator_AST_changes_match_exact_host_proof=True,complete_phase_scope_qualified_only_by_prior_fixed_SOURCE_review=dict(path=str(BASE/'next_complete_combined_v18_source_only_review/sealed_independent_source_review/REVIEW.json'),sha256='8710ef186d1df881ced05fa30544e51adef9ee21f45b6045ce508f815ccf95a8'),family_paths_exact=True,actual_bcd_helper_and_d490_admission_pins_unchanged=True,future_six_business_success_pins_all_None=True,cap=dict(whole_wall_seconds=1800,prepare_child_wall_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0),checks={k:True for k in checks},unchanged_genuine_source_pins=['3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'],archive_scope=dict(full_source_input_pins=True,full_byte_count_both_before_and_after_result=['HOST','SOURCE','OUT','SOURCE_ARCHIVE'],TERMINAL_absent_before_and_after_prepare=True,history_resource_root_exclusions_preserved=['HOST','SOURCE','OUT','TERMINAL']),fresh_namespace_state_at_review=ns,no_blocker=True,project_module_imported_or_executed=False,resource_check_called=False,business_or_numeric_payload_executed_or_read=False,canonical_or_ART_written=False,runtime_PREP_PASS_or_512mib_measurement_not_claimed=True,new_whole_INPUT_or_build_or_native_or_AAA_or_ABA_credit=False)
p=d/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(d/'REPORT.txt').write_text('V18 READY factory 与 genuine PREP host 有限源码审查通过。\n仅 doc/status 两处变化；70 个函数/类逐字节保持 ecfd；其余顶层源码保持。\n最终 host 9 项完整反向还原到 37d，再按 11 项完整反向还原到 310dd。\n原 genuine guard/class/MRO/resource/固定 prepare-build argv/API 全保持。资源仍 whole 1800 秒、prepare child 600 秒、512 MiB、2 GiB、history 96 GiB/free 8 GiB、1 thread/1 child/0 retry。\nSOURCE_ARCHIVE 全输入前后 pin 与 HOST+SOURCE+OUT+SOURCE_ARCHIVE 两次完整计数保留。TERMINAL 准备前后必须不存在。\nbcd/d490 保持原组件 INPUT-only 资格，6 项未来业务成功 pin 全 None。\n本审查只用标准库读取源码/JSON元数据并做 AST、全字节反向还原、全 SHA/7ID 前后检查；不 import 项目模块、不调用 API、不执行准备/构建/数值、不改 canonical/ART。\n没有阻塞；这是源码审查通过，不能视为新的 PREP、whole INPUT、build、native、AAA 或 ABA 成功，也不预测实际 RSS/运行通过。\n',encoding='utf-8')
print(json.dumps({'directory':str(d),'review_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':review['status'],'input_file_count':len(before),'host_inverse_9_then_11_exact':True,'ready_2_inverse_and_70_definitions_exact':True,'business_executed':False,'no_blocker':True}))

from pathlib import Path
import ast,hashlib,json,stat,tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=Path('/private/tmp/axmat_v19_normal_PREP_host_source_binding_20261010')
R=Path('/private/tmp/axmat_v19_complete_combined_READY_source_binding_20261010')
U=Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py')
H=D/'combined_prepare_host.py'
C=R/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py'
P18=B/'actual_complete_combined_prepare_v18_sources/combined_prepare_host.py'
P17=B/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
P15=B/'actual_combined_prepare_sources/combined_prepare_host.py'
G18=Path('/private/tmp/axmat_v18_root_prepare_host_source_20261010/generate_prepare_host.py')
C18=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')
HP=D/'Root_finite_host_source_inverse.json'
HP18=B/'actual_complete_combined_prepare_v18_sources/Root_finite_host_source_inverse.json'
HP17=B/'actual_complete_combined_prepare_v17_sources/Root_finite_host_source_inverse.json'
GP=D/'generator_finite_inverse_proof.json'
hashes={
D/'full_host_ancestry_inverse_proof.json':'2ab2bd271400bc53bfd94414ed5cea6c3c69016797b25ad17a8133fb8d7479fe',
D/'sealed_manifest.json':'303c8316df89f8c0572a670fc90f1d3f48057b7e961536097bc36fff774e8fd8',
R/'sealed_manifest.json':'82b59edb22ac6255c6e869f3c05376af53a1dd981758b0983196f81d344a5848',
H:'f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580',
C:'34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b',
U:'585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50',
P18:'bc5c6fa1118b84641a5a66232080354074b49ad2c59ac809e28ee99cc6faac98',
P17:'37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3',
P15:'310ddc9d4145060b6f6aa0e250dd470ef05aef43c7d4c2b0c234983351d0b434',
D/'generate_prepare_host.py':'2ac3a6a7ae571f2b4d0ae694b0658c16ac6e92707ef2e4c7ebe8974863a6aa02',
G18:'2d90a91f15a4a0cfd4e31de529703b65e0ad91973966f3c3b94576519f8f999a',
HP:'a187bbdfaade47a8a704ff130d821664cd80aab2a5911a7acea2db4315c72615',
HP18:'6ee30cbc62a1e2d79f39f9da0b0403ab95b53b0b182d6e13dabc04ba35da94a1',
HP17:'b7f811379aa40f5f81c4e08e4cfa01a4199a1e78684f0ab118d9150748bec67f',
GP:'20253b9171c611f703a7dd3f3c9237c3af3658e1e322988f74f0cdc7ac6b0f6e',
C18:'5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240',
Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'):'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',
B/'Root_actual_complete_graph_helper_controls_admission_v17.json':'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8',
}
data={};pins={}
def read_pin(p,h):
 a=p.lstat();assert stat.S_ISREG(a.st_mode),str(p)
 b=p.read_bytes();z=p.lstat()
 id7=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert id7(a)==id7(z)
 assert hashlib.sha256(b).hexdigest()==h,(str(p),'fixed SHA mismatch')
 return b,dict(path=str(p),sha256=h,size_bytes=len(b),identity7=id7(a))
for p,h in hashes.items():data[p],pins[p]=read_pin(p,h)
t={p:b.decode() for p,b in data.items() if p.suffix=='.py'}
for p,s in t.items():ast.parse(s)
hp=json.loads(data[HP]);hp18=json.loads(data[HP18]);hp17=json.loads(data[HP17]);gp=json.loads(data[GP])
def inverse(s,edits,count):
 assert len(edits)==count
 for e in reversed(edits):
  assert type(e['occurrences']) is int and e['occurrences']>0
  assert s.count(e['new'])==e['occurrences'],(e['new'],'inverse count')
  s=s.replace(e['new'],e['old'],e['occurrences'])
 return s
assert inverse(t[H],hp['changes'],9)==t[P18]
assert inverse(t[P18],hp18['changes'],9)==t[P17]
assert inverse(t[P17],hp17['changes'],11)==t[P15]
assert inverse(t[D/'generate_prepare_host.py'],gp['edits'],10)==t[G18]
assert hp['factory_candidate']==str(C) and hp['factory_sha256']==hashes[C]
assert hp['host_candidate']==str(H) and hp['host_sha256']==hashes[H]
assert hp['parent_host']==str(P18) and hp['parent_host_sha256']==hashes[P18]
assert hp['unready_full_scope_source']==str(U) and hp['unready_source_sha256']==hashes[U]
assert hp['status']=='SOURCE_ONLY_NOT_EXECUTED'
expected=[
('axial-material-complete-combined-prepare-host-v18-20261010','axial-material-complete-combined-prepare-host-v19-20261010'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py'),
(hashes[C18],hashes[C]),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010'),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010'),
('actual_complete_combined_prepare_v18_sources','actual_complete_combined_prepare_v19_sources'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_DECLARATION_V1'),
('AXMAT_V18_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V19_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1')]
assert [(e['old'],e['new']) for e in hp['changes']]==expected and all(e['occurrences']==1 for e in hp['changes'])
g_ast=ast.parse(t[D/'generate_prepare_host.py'])
gn=next(n for n in ast.walk(g_ast) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='changes' for x in n.targets))
ge=[]
for i,n in enumerate(gn.value.elts):
 old=ast.literal_eval(n.elts[0])
 if i==2:
  assert ast.dump(n.elts[1])==ast.dump(ast.parse('sha(source)',mode='eval').body)
  new=hashes[C]
 else:new=ast.literal_eval(n.elts[1])
 ge.append((old,new))
assert ge==expected
c_ast=ast.parse(t[C]);u_ast=ast.parse(t[U])
defs=lambda s:{n.name:ast.get_source_segment(s,n) for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
assert len(defs(t[C]))==70 and defs(t[C])==defs(t[U])
def non_doc_status(s):
 return [ast.dump(n,include_attributes=False) for i,n in enumerate(ast.parse(s).body) if not(i==0 and isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str)) and not(isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='DRAFT_STATUS' for x in n.targets))]
assert non_doc_status(t[C])==non_doc_status(t[U])
cdoc=ast.get_source_segment(t[C],c_ast.body[0])
udoc=ast.get_source_segment(t[U],u_ast.body[0])
cs=next(ast.get_source_segment(t[C],n) for n in c_ast.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='DRAFT_STATUS' for x in n.targets))
us=next(ast.get_source_segment(t[U],n) for n in u_ast.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='DRAFT_STATUS' for x in n.targets))
ready_inverse=t[C]
for new,old in ((cs,us),(cdoc,udoc)):
 assert ready_inverse.count(new)==1
 ready_inverse=ready_inverse.replace(new,old,1)
assert ready_inverse==t[U]
def vals(s):
 v={}
 for n in ast.parse(s).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:v[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
 return v
cv,uv,ov=vals(t[C]),vals(t[U]),vals(t[C18])
assert cv['DRAFT_STATUS']=='READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assert all(cv[k] is None for k in future)
sha_globals={k:v for k,v in ov.items() if '_SHA' in k}
assert sha_globals and all(k in cv and cv[k]==v for k,v in sha_globals.items())
assert cv['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==hashes[B/'Root_actual_complete_graph_helper_controls_admission_v17.json']
assert hashes[Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')] in t[C]
def paths(s):
 v={}
 def read(n):
  if isinstance(n,ast.Name):return v[n.id]
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Path':return Path(read(n.args[0]))
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return read(n.left)/read(n.right)
  raise ValueError()
 for n in ast.parse(s).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:v[n.targets[0].id]=read(n.value)
   except (ValueError,KeyError,TypeError):pass
 return v
hv,rv=paths(t[H]),paths(t[C])
assert all(hv[k]==rv[k] for k in ('SOURCE','OUT','TERMINAL'))
assert hv['TARGET']==rv['FORMAL_FACTORY'] and str(hv['TARGET'])==hp['formal_factory']
assert hv['TARGET_SHA']==hashes[C]
assert hv['SOURCE_ARCHIVE']==B/'actual_complete_combined_prepare_v19_sources'
assert hp['source_archive']==str(hv['SOURCE_ARCHIVE'])
checks={
'caps_original':"WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30",
'genuine_guard':"helper.guard_admission(full)",
'base_MRO':"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)",
'full_and_production_module_paths':"Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT",
'genuine_resource_original_history_and_free':"resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)",
'genuine_runner_instance':"type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources",
'original_remaining_whole_wall':"remaining=WHOLE_CAP-(time.monotonic()-started)",
'original_600_prepare_callcap':"runner.execute(HOST/'run','prepare',command,STAGE_CAP)",
'fixed_argv':"command=[str(support.PYTHON),str(TARGET),'prepare-build']",
'no_retry_fresh_namespaces':"if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL))",
'no_profile_or_optimization':"if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:",
'full_archive_source_file_pins':"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]",
'original_after_input_pins':"if support.pin(entry['path'],entry['sha256'])!=entry",
'typed_child_exit0':"type(watch['returncode']) is not int or watch['returncode']!=0",
'only1_PASS':"len(runner.records)!=1 or runner.records[0]['status']!='PASS'",
'ownchild_cleanup':"watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True",
'rss_under512':"not 0<=watch['sampled_peak_rss_mib']<RSS_CAP",
'prepare_no_terminal_or_success_seal':"if os.path.lexists(TERMINAL) or (OUT/'seal.json').exists()",
'unchanged_thread_child_retry_claims':"threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False",
'resource_history_roots_scope':"roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)"}
for k,f in checks.items():assert f in t[H],k
assert t[H].count('support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))')==2
caps=dict(whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0)
for k,v in caps.items():assert hp[k]==v
for k in ('genuine_supervisor_class_or_MRO_modified','business_executed','native_executed','AAA_accuracy_qualified','ABA_admitted'):assert hp[k] is False
for p,h in hashes.items():
 _,p2=read_pin(p,h);assert p2==pins[p],(str(p),'before-after input identity')
out=Path(tempfile.mkdtemp(prefix='axmat_v19_normal_PREP_host_finite_SOURCE_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V19_NORMAL_PREP_HOST_FINITE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_RUNTIME_REQUIRED',source_inputs=list(pins.values()),full_source_SHA_identity7_before_after_equal=True,host_f5c_inverse_9_to_bc5_exact=True,bc5_inverse_9_to_37d_exact=True,parent_37d_inverse_11_to_310dd_exact=True,generator_10_inverse_to_prior_2d_exact=True,generator_AST_exact9retarget_matches_host_proof=True,READY_34ef_only_doc_and_status_2_edits_inverse_to_585e_exact=True,all70_READY_defs_byteexact_585e=True,all_other_READY_top_level_nodes_exact_585e=True,qualified_fixed_SHA_globals_unchanged_to_V18=dict(count=len(sha_globals),all_equal=True),six_future_business_pins_None=True,helper_bcd_and_actual_d490_pins_unchanged=True,factory_SOURCE_OUT_TERMINAL_FORMAL_paths_match_host=True,sourcearchive_target_fresh_family19=str(hv['SOURCE_ARCHIVE']),genuine_source_checks={k:True for k in checks},caps=caps,archive_full_pin_and_joint_count=['HOST','SOURCE','OUT','SOURCE_ARCHIVE'],archive_count_occurrences=2,complete_PREP_caller_lifetime_review_not_repeated_here='Root assigned separate independent agent; this host review proves unchanged binding to fixed585e and34ef only',project_module_API_guard_resource_or_numeric_executed=False,ART_live_or_full_history_parsed=False,canonical_or_ART_written=False,new_actual_PREP_or_graph_or_whole_INPUT_or_build_or_native_or_AAA_or_ABA_credit=False,RSS_cause_or_expected_pass_unknown=True,no_blocker=True)
p=out/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(out/'REPORT.txt').write_text('V19 normal PREP host 有限源码复核通过，无 blocker。\n最终 host f5c 9项完整inverse回bc5，再9项回37d，再11项回310dd；generator10项inverse回原2d，全部整字节准确。\nREADY34ef与585e仅doc/status两处绑定差异，70函数/类逐字节一致，其余顶层节点保持；caller lifetime由Root另派独立审查，本次不重复或授业务信用。\n原genuine guard/class/MRO/resource/API/fixedargv保持；1800 whole/600 PREP child秒、512 MiB、2 GiB、history96/free8 GiB、1thread/1child/0retry保持。\n新19 family namespace和factory路径精确匹配；SOURCE_ARCHIVE完整前后pin与HOST+SOURCE+OUT+SOURCE_ARCHIVE两次联计保持。\nbcd/d490及原固定SHA/component输入pins不变，6未来业务成功pins仍None。\n所有本次18个源码/有限proof metadata全SHA/7ID前后一致。仅标准库SOURCE读取/AST/whole inverse，未执行项目/API/guard/resource/业务/数值，未解析ART live/整史，未写canonical/ART。\n实际RSS cause及是否PASS未知，SOURCE PASS不能当新PREP/fullINPUT/build/native/AAA/ABA实际成功。\n',encoding='utf-8')
print(json.dumps(dict(directory=str(out),review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=review['status'],source_file_count=len(pins),no_blocker=True,business_executed=False)))

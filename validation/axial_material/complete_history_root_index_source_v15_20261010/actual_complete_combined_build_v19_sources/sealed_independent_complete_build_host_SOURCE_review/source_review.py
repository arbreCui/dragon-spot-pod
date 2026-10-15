from pathlib import Path
import ast,hashlib,json,os,stat,tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=Path('/private/tmp/axmat_v19_complete_combined_build_host_source_design_20261010')
E=B/'actual_complete_combined_prepare_v19_receipts'
H=D/'combined_build_host.py'
G=D/'generate_build_host.py'
P=B/'actual_complete_combined_build_v17_sources/combined_build_host.py'
A=B/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')
C17=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
Q=B/'Root_actual_complete_graph_helper_controls_admission_v17.json'
helper=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
hashes={
H:'764091435456162cef3335a314acc5e868961ca9f7d28d9616c3d47f53fee5c0',
G:'dc48a3c47804359ba483bab74da31df3cd5aebad0a2935c994211ebd76293d39',
D/'Root_finite_build_host_source_inverse.json':'5d0e10ef21441da49d53822f3a87223df76b59cc89bff60402b4968b864c6e13',
D/'original_cf2c_thirteen_change_inverse.json':'29a05241b38bcd4d878d058dc27b023a07e8356993c53ff033575ed16d50a6d6',
D/'sealed_manifest.json':'98d81874e6b2af4a0a354181ddde0bcad371b059f8b19fe81235222adb0631e8',
D/'generator_source_inverse_proof.json':'c90cb2ffb03bdd77f51ba0bcf59be1e0f3027c224c66bb4ef5d255a7673d420a',
P:'cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9',
B/'actual_complete_combined_build_v17_sources/Root_finite_build_host_source_inverse.json':'29a05241b38bcd4d878d058dc27b023a07e8356993c53ff033575ed16d50a6d6',
A:'37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3',
C:'34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b',
C17:'feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c',
E/'Root_actual_complete_combined_prepare_summary.json':'17992f59e84611b0456e3451f0e6abbdc56baf2a0e985f5e1ad895d24e52c046',
E/'Root_actual_prepare_tool_terminal_return.json':'cedc8d4e51858b3377e54cc9f71489d0db8ff8703049de00e4ab2433c2e432fe',
E/'Root_actual_complete_prepare_namespace_manifest.json':'603ed9d1088b94ac5519d63e03b4b2eacabed27baf013c34906cf925985fc9eb',
Q:'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8',
helper:'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',
}
data={};pins={}
def readpin(p,h):
 assert '/validation/artifacts/' not in str(p),'reviewer only SOURCE and Root_META'
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
 b=p.read_bytes();z=p.lstat()
 ident=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 assert ident(a)==ident(z) and len(b)==a.st_size
 assert hashlib.sha256(b).hexdigest()==h,(str(p),'fixed sha changed')
 return b,dict(path=str(p),sha256=h,identity=ident(a))
for p,h in hashes.items():data[p],pins[p]=readpin(p,h)
s={p:b.decode() for p,b in data.items() if p.suffix=='.py'}
for p,t in s.items():ast.parse(t)
proof=json.loads(data[D/'Root_finite_build_host_source_inverse.json'])
oldproof=json.loads(data[D/'original_cf2c_thirteen_change_inverse.json'])
summary=json.loads(data[E/'Root_actual_complete_combined_prepare_summary.json'])
term=json.loads(data[E/'Root_actual_prepare_tool_terminal_return.json'])
ns=json.loads(data[E/'Root_actual_complete_prepare_namespace_manifest.json'])
def inverse(t,records,n):
 assert len(records)==n
 for r in reversed(records):
  assert type(r['count']) is int and r['count']>0
  assert t.count(r['after'])==r['count'],(r['after'],'inverse count')
  t=t.replace(r['after'],r['before'],r['count'])
 return t
assert proof['finite_change_count']==17 and inverse(s[H],proof['changes'],17)==s[P]
assert oldproof['finite_change_count']==13 and inverse(s[P],oldproof['changes'],13)==s[A]
assert proof['parent_path']==str(P) and proof['parent_sha256']==hashes[P]
assert proof['host_path']==str(H) and proof['host_sha256']==hashes[H]
assert proof['original_cf2c_to_37d_thirteen_change_inverse']==oldproof
for r in proof['checked_source_pins']:
 p=Path(r['path']);assert p in pins and pins[p]==r
assert proof['actual_Root_closed_PREP_summary']==pins[E/'Root_actual_complete_combined_prepare_summary.json']
assert proof['actual_Root_closed_terminal']==pins[E/'Root_actual_prepare_tool_terminal_return.json']
assert proof['actual_Root_complete_namespace_freeze']==pins[E/'Root_actual_complete_prepare_namespace_manifest.json']
assert summary['schema']=='ROOT_V19_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'
assert summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
assert summary['Root_actual_terminal']==summary['actual_root_terminal']==pins[E/'Root_actual_prepare_tool_terminal_return.json']
assert type(term['terminal_tool_return']['exit_code']) is int and term['terminal_tool_return']['exit_code']==0
assert term['terminal_tool_return']['chunk_id']=='c5790b' and 'session_id' not in term['terminal_tool_return']
assert term['closed'] is True and type(term['exit_code']) is int and term['exit_code']==0
assert term['session_repolled_after_close'] is False and term['original_session_id']==2985
cap_fields=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries')
assert tuple(summary[k] for k in cap_fields)==(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)
assert summary['original_caps_preserved'] is True and 0<=summary['sampled_peak_rss_mib']<512
assert 0<summary['child_seconds']<=600 and summary['child_seconds']<=summary['whole_seconds']<1800 and 0<summary['joint_archive_bytes']<2*2**30
for k in ('original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'):assert summary[k] is False
assert ns['schema']=='ROOT_V19_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and ns['no_build_or_native_credit'] is True
assert ns['canonical_factory']==pins[C]
metadata_refs=proof['actual_output_pins_bound_by_closed_Root_metadata_without_ART_read']
assert metadata_refs=={k:summary[f] for k,f in (('actual_declaration','actual_declaration'),('actual_complete_input_graph','actual_complete_input_graph'),('actual_complete_creation_trace','actual_complete_creation_trace'),('actual_prep_terminal','formal_PREP_terminal'))}
nmap={r['root']:r for r in ns['namespaces']};assert len(nmap)==len(ns['namespaces'])==5
for k,r in metadata_refs.items():
 root=str(Path(r['path']).parent);name=Path(r['path']).name
 assert nmap[root]['files'][name]==r
 assert set(r)=={'path','sha256','identity'} and len(r['identity'])==7 and all(type(x) is int for x in r['identity'])
 assert r['identity'][3]==1 and stat.S_ISREG(r['identity'][2]) and r['identity'][4]>0
dynamic={k:r['sha256'] for k,r in metadata_refs.items()}
dynamic.update(actual_root_receipts_directory='actual_complete_combined_prepare_v19_receipts',actual_Root_summary=hashes[E/'Root_actual_complete_combined_prepare_summary.json'])
def evalsource(n,env):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name):return env[n.id]
 if isinstance(n,(ast.List,ast.Tuple)):
  v=[evalsource(x,env) for x in n.elts];return v if isinstance(n,ast.List) else tuple(v)
 raise ValueError('static simple literal only')
ga=ast.parse(s[G]);gassign={n.targets[0].id:n.value for n in ga.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
fixed=evalsource(gassign['FIXED'],{'TARGET_SHA':hashes[C]})
dyn=evalsource(gassign['DYNAMIC_SOURCE_TOKENS'],{})
expected=[dict(before=a,after=b,count=c) for a,b,c in fixed]+[dict(before=a,after=dynamic[k],count=c) for a,k,c in dyn]
assert len(fixed)==11 and len(dyn)==6 and proof['changes']==expected
def pathvals(t):
 vals={}
 def e(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Name):return vals[n.id]
  if isinstance(n,(ast.Tuple,ast.List)):
   z=[e(x) for x in n.elts];return tuple(z) if isinstance(n,ast.Tuple) else z
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return e(n.left)/e(n.right)
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Path':return Path(e(n.args[0]))
  raise ValueError()
 for n in ast.parse(t).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1:
   try:v=e(n.value)
   except (ValueError,KeyError,TypeError):continue
   if isinstance(n.targets[0],ast.Name):vals[n.targets[0].id]=v
   elif isinstance(n.targets[0],ast.Tuple):
    for k,x in zip(n.targets[0].elts,v):
     if isinstance(k,ast.Name):vals[k.id]=x
 return vals
hv=pathvals(s[H]);cv=pathvals(s[C]);pv=pathvals(s[P])
for k in ('SOURCE','OUT','TERMINAL'):assert hv[k]==cv[k]
assert hv['TARGET']==cv['FORMAL_FACTORY'] and hv['TARGET_SHA']==hashes[C]
assert hv['INNER_FAMILY']==cv['FAMILY']
assert hv['SOURCE_ARCHIVE']==B/'actual_complete_combined_build_v19_sources'
assert hv['DECLARATION_SHA']==metadata_refs['actual_declaration']['sha256']
assert hv['PREP_SHA']==metadata_refs['actual_prep_terminal']['sha256']
labels=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
assert hv['EXPECTED_LABELS']==labels
# Compare every source-fixed command token with the original complete cf2c list after the 17 finite retargets.
assert len(hv['EXPECTED_COMMANDS'])==5 and len(pv['EXPECTED_COMMANDS'])==5
assert hv['EXPECTED_COMMANDS'][1]==[str(cv['NM']),'-g',str(cv['TRIM_OBJECT']),str(cv['PHYSICAL_OBJECT']),str(cv['SENDER_OBJECT']),str(cv['ART']/'axial-material-moment-order-build-20261006/build/FLU.o')]
assert hv['EXPECTED_COMMANDS'][2]==[str(cv['NM']),'-g',str(cv['OUT']/'runtime/Dragon')]
assert hv['EXPECTED_COMMANDS'][3]==[str(cv['OTOOL']),'-L',str(cv['OUT']/'runtime/Dragon'),str(cv['OLD']/'runtime/Dragon'),str(cv['PHYSICAL']/'runtime/Dragon'),str(cv['DEDUP']/'runtime/Dragon'),str(cv['TRIM']/'runtime/Dragon')]
assert hv['EXPECTED_COMMANDS'][4]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(C),'audit-build','--sha256',hv['DECLARATION_SHA'],'--prep-sha256',hv['PREP_SHA']]
assert hv['EXPECTED_COMMANDS'][0][-2:]==['-o',str(cv['OUT']/'runtime/Dragon')]
defs=lambda text:{n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
cd,pd=defs(s[C]),defs(s[C17])
for k in ('run_build','stage_commands','declaration_admission','combined_link_command','check_watch','environment','audit_build'):
 assert cd[k]==pd[k],(k,'original stage/source algorithm changed')
cvals={}
for n in ast.parse(s[C]).body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try:cvals[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError):pass
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assert all(cvals[k] is None for k in future)
assert cvals['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==hashes[Q] and hashes[helper] in s[C]
checks={
'genuineguard':'helper.guard_admission(full)',
'genuinebaseMRO':'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
'genuinemodulepaths':'Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT',
'genuineresource':'resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',
'genuineinstance':'type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources',
'caps1800_600_512_2GiB':'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30',
'outerwholebudget':'remaining=WHOLE_CAP-(time.monotonic()-started)',
'outercall1800':"runner.execute(HOST/'run','build',command,WHOLE_CAP)",
'fixedwholeargv':"command=[str(support.PYTHON),str(TARGET),'run-build','--sha256',DECLARATION_SHA,'--prep-sha256',PREP_SHA]",
'1thread1child0retry':'threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False',
'freshhost0retry':"if os.path.lexists(HOST):raise ValueError('fresh one-use whole build host required; no retry')",
'fullsourcearchivepins':"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]",
'allSOURCEandTERMINALpins':"[support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]",
'allinputbeforeafter':"if support.pin(entry['path'],entry['sha256'])!=entry",
'exact5stagegate':"len(inner)!=5 or [s['label'] for s in inner]!=EXPECTED_LABELS or [s['command'] for s in inner]!=EXPECTED_COMMANDS or any(s['status']!='PASS' for s in inner)",
'watchall5agreement':"inner_watches!=result['watchdogs'] or inner_watches[:-1]!=audit['previous_stage_watchdogs']",
'innerstage600':"not 0<iw['wall_cap_seconds']<=stage['wall_cap_seconds']<=600",
'innertypedexit0':"type(iw['returncode']) is not int or iw['returncode']!=0",
'innerowncleanup':"iw['own_child_only'] is not True or iw['liveness_group_cleanup'] is not True",
'innersha':"support.pin(raw_log)['sha256']!=stage['log_sha256']",
'raw4complete':"raw['files']!={label+'.log':support.pin(OUT/(label+'.log'))['sha256'] for label in EXPECTED_LABELS[:4]}",
'rawpreidentity':"raw['before_binary_identity_gates'] is not True or raw['complete_raw_tools_and_link_stdout'] is not True",
'allOUTseal':"seal['symlinks']!={} or seal['directories']!=sorted(directories) or set(files)!=set(seal['files'])|{'seal.json'} or any(files[k]!=v for k,v in seal['files'].items())",
'4actualtailkeys':"set(admission)!=set(('result','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'))",
'all4actualtailcap':"not result['elapsed_seconds']<=admission['actual_elapsed_seconds']<WHOLE_CAP",
'linkidentityonlyscienceboundary':"whole_combined_INPUT_admitted=False",
'originalhistorytailvalidation':"resource.validate_history_roots(tail_resources['resource_roots'],support.ART)",
}
for k,v in checks.items():assert v in s[H],k
assert s[H].count('support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))')==2
assert "commands=stage_commands(d,expected)" in cd['run_build']
assert "runner.execute(OUT/directory,stem,command,STAGE_WALL)" in cd['run_build'] and "runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL" in cd['run_build']
assert 'if sys.flags.optimize' in s[C]
assert not os.path.lexists(hv['HOST']) and not os.path.lexists(hv['SOURCE_ARCHIVE'])
for p,h in hashes.items():
 _,z=readpin(p,h);assert z==pins[p],(str(p),'fresh before-after source/meta')
out=Path(tempfile.mkdtemp(prefix='axmat_v19_complete_5stage_build_host_finite_SOURCE_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V19_COMPLETE_FIVE_STAGE_BUILD_HOST_FINITE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_RUNTIME_REQUIRED',source_and_Root_META_inputs=list(pins.values()),all_full_EOF_SHA7ID_before_after_equal=True,finite_host17_inverse_to_cf2c_exact=True,original_cf2c13_inverse_to37d_exact=True,generator11fixed_plus6_actual_retargets_exact=True,actual_Root_PREP_typed_exit0_closed_metadata=dict(summary=pins[E/'Root_actual_complete_combined_prepare_summary.json'],terminal=pins[E/'Root_actual_prepare_tool_terminal_return.json'],terminal_chunk='c5790b',original_session=2985,scope='Root_METADATA_ONLY_NOT_INDEPENDENT_ART_PAYLOAD_REVIEW'),actual_four_prepared_output_pins_bound_only_to_Root_summary_and_namespace=metadata_refs,ART_four_raw_payloads_not_read=True,canonical_source_34ef_pinned=True,all5_source_EXPECTED_labels_and_commands_original_cf2c_retarget_only=True,last4commands_match_original_canonical_static_paths_and_metadata_pins=True,original7_source_stage_functions_byteexact_to_feeb=['run_build','stage_commands','declaration_admission','combined_link_command','check_watch','environment','audit_build'],dynamic_actual_declaration_production_link_AND_objects_not_reread_here='Original canonical source declaration admission and original runtime exact5 command gates remain mandatory; separate saved-PREP review supplied by Root',genuine_checks={k:True for k in checks},caps=dict(outer_whole_seconds=1800,inner_each_stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0),fullSOURCE_OUT_TERMINAL_sourcearchive_inputs_before_after=True,full_archive_scope_both_checks=['HOST','SOURCE','OUT','TERMINAL','SOURCE_ARCHIVE'],fresh_HOST_and_SOURCE_ARCHIVE_absent_at_review=True,new_sourcearchive=str(hv['SOURCE_ARCHIVE']),helper_bcd_actual_Q_d490_unchanged=True,six_future_business_pins_all_None=True,business_module_API_guard_resource_numeric_executed=False,canonical_or_ART_written=False,new_actual_build_or_wholeINPUT_or_native_or_AAA_or_ABA_credit=False,RSS_cause_or_expected_pass_claimed=False,no_blocker=True)
p=out/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(out/'REPORT.txt').write_text('V19 完整五阶段 build host 有限 SOURCE 复核通过，无 blocker。\n17 项 whole inverse 完整还原至 cf2c，再原 13 项完整还原至 37d；所有变化只是明确 namespace/schema/source SHA/真实 PREP pin 接线。\n真实 Root PREP metadata summary1799 与 terminal c5790b 严格整数0 CLOSED及4真实输出pins、namespace metadata精确一致。4 ART payload未读取，saved PREP另由Root独立审查，不能混成build成功。\n全5 EXPECTED commands和labels保持cf2c完整列表的有限retarget；后4命令与当前canonical静态路径及pins精确一致，原link/declaration/full5实际command gate仍必须执行。7个stage相关canonical函数逐字节同feeb。\n原 genuine guard/class/MRO/API/resource、whole outer1800/inner每项600秒、512 MiB、2 GiB、history96/free8GiB、1thread/1child/0retry保持。\nfull5 watchdog/完整raw前4工具/OUT全seal/4实际tails/all SOURCE+TERMINAL+SOURCE_ARCHIVE输入前后pins与H+S+O+T+SOURCE_ARCHIVE联计保持。\n新HOST和SOURCE_ARCHIVE审查时均不存在。helper bcd、Q d490、6未来成功pins None保持。\n本次16个SOURCE/Root_META文件全SHA7ID前后相同，只标准库AST/整字节inverse；未import项目或执行API/guard/resource/业务/数值，未读ART raw数据，未写canonical/ART。\nSOURCE PASS不代表新build、wholeINPUT、native、AAA、ABA成功；实际RSS cause和是否PASS均未知。\n',encoding='utf-8')
print(json.dumps(dict(directory=str(out),review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=review['status'],source_metadata_file_count=len(pins),no_blocker=True,business_executed=False)))

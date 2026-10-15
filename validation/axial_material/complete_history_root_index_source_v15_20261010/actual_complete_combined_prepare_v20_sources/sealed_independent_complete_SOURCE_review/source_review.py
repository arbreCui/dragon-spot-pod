# Actual initial UNREADY SOURCE audit. The separately executed READY append command and its full actual result are preserved in actual_SOURCE_tool_returns.json.
from pathlib import Path
import ast,hashlib,json,stat,tempfile
D=Path('/private/tmp/axmat_v20_complete_strict_JSON_raw_last_use_source_only_20261010')
C=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.UNREADY.py'
P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
H=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
Q=B/'Root_actual_complete_graph_helper_controls_admission_v17.json'
fixed={
C:'c7cf9e621f92d36e88b0feb7ff578f99c9471c72a201acb88d3ed80714499026',
P:'34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b',
D/'source_inverse_proof.json':'a3ba455364f2a58add09cd8ea7a7c1d1d38f96f950ca29f5018c7b861e1a4aed',
D/'sealed_manifest.json':'d9a284ac18fb82cc7448401721f46a0551c6513f60ae65c5248b8b9bff7123fd',
H:'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6',
Q:'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'}
def pin(p,h):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
 b=p.read_bytes();z=p.lstat()
 id7=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert id7(a)==id7(z) and hashlib.sha256(b).hexdigest()==h
 return b,dict(path=str(p),sha256=h,size_bytes=len(b),identity7=id7(a))
data={};pins={}
for p,h in fixed.items():data[p],pins[p]=pin(p,h)
old=data[P].decode();new=data[C].decode()
oa=ast.parse(old);na=ast.parse(new)
proof=json.loads(data[D/'source_inverse_proof.json'])
manifest=json.loads(data[D/'sealed_manifest.json'])
assert proof['parent']==pins[P] and proof['candidate']==pins[C]
assert manifest['only_parent']==pins[P] and manifest['candidate']==pins[C]
records=proof['edits'];assert len(records)==proof['finite_change_count']==10
inverse=new
for r in reversed(records):
 assert type(r['occurrences']) is int and r['occurrences']==1
 assert inverse.count(r['new'])==1
 inverse=inverse.replace(r['new'],r['old'],1)
assert inverse==old
defs=lambda text:{n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
od,nd=defs(old),defs(new)
assert set(od)==set(nd) and len(nd)==70
changed=[k for k in od if od[k]!=nd[k]]
assert changed==['require_ready','strict_json_bytes']
assert sum(od[k]==nd[k] for k in od)==68
oldstrict=od['strict_json_bytes'];newstrict=nd['strict_json_bytes']
assert newstrict==oldstrict.replace("    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)\n","    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)\n    del raw\n",1)
assert oldstrict.count("value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)")==1
assert nd['require_ready']==od['require_ready'].replace('READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY',1)
def nodes(text,kind):
 return [ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(text)) if isinstance(n,kind)]
for k in nd:
 a=nd[k]
 if k=='require_ready':a=a.replace('READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY','READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
 for typ in (ast.If,ast.Assert,ast.Raise,ast.Call,ast.Return):assert nodes(a,typ)==nodes(od[k],typ),(k,typ.__name__)
sa=ast.parse(newstrict).body[0];so=ast.parse(oldstrict).body[0]
dels=[(i,n) for i,n in enumerate(sa.body) if isinstance(n,ast.Delete)]
assert len(dels)==1
index,delete=dels[0]
assert len(delete.targets)==1 and isinstance(delete.targets[0],ast.Name) and delete.targets[0].id=='raw'
assert isinstance(sa.body[index-1],ast.Assign)
assert ast.dump(sa.body[index-1],include_attributes=False)==ast.dump(so.body[index-1],include_attributes=False)
assert ast.get_source_segment(newstrict,sa.body[index-1])=="value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)"
assert nodes(newstrict,ast.Call)==nodes(oldstrict,ast.Call)
raw_load=[n for n in ast.walk(sa) if isinstance(n,ast.Name) and n.id=='raw' and isinstance(n.ctx,ast.Load)]
assert len(raw_load)==1 and raw_load[0].lineno<delete.lineno
assert not any(isinstance(n,(ast.Global,ast.Nonlocal)) and 'raw' in n.names for n in ast.walk(sa))
for n in sa.body:
 if isinstance(n,ast.FunctionDef):assert not any(isinstance(x,ast.Name) and x.id=='raw' for x in ast.walk(n))
sa.body=[n for n in sa.body if not isinstance(n,ast.Delete)]
assert ast.dump(sa,include_attributes=False)==ast.dump(so,include_attributes=False)
assert nd['read']==od['read']=="def read(path):return strict_json_bytes(require(path).read_bytes())"
ra=ast.parse(nd['read']).body[0]
assert len(ra.body)==1 and isinstance(ra.body[0],ast.Return)
assert not any(isinstance(n,(ast.Assign,ast.AnnAssign,ast.AugAssign,ast.NamedExpr)) for n in ast.walk(ra))
globals_old={};globals_new={}
def globals_ast(a):
 out={}
 for n in a.body:
  if isinstance(n,ast.Assign):
   names=[x.id for t in n.targets for x in ast.walk(t) if isinstance(x,ast.Name)]
   for k in names:out[k]=ast.dump(n.value,include_attributes=False)
 return out
globals_old=globals_ast(oa);globals_new=globals_ast(na)
assert set(globals_old)==set(globals_new)
allowed={'SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY','DRAFT_STATUS'}
globchanged={k for k in globals_old if globals_old[k]!=globals_new[k]}
assert globchanged==allowed
assert all(globals_old[k]==globals_new[k] for k in globals_old if k not in allowed)
vals={}
for n in na.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try:vals[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError):pass
assert vals['DRAFT_STATUS']=='UNREADY_SOURCE_ONLY_V20_STRICT_JSON_RAW_LAST_USE_REVIEW_REQUIRED'
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assert all(vals[k] is None for k in future)
assert vals['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==fixed[Q]
assert fixed[H] in new
def safe(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Tuple):return tuple(safe(x) for x in n.elts)
 if isinstance(n,ast.BinOp):
  a,b=safe(n.left),safe(n.right)
  if isinstance(n.op,ast.Mult):return a*b
  if isinstance(n.op,ast.Pow):return a**b
 raise ValueError()
caps={}
for n in na.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Tuple):
  try:v=safe(n.value)
  except ValueError:continue
  for k,x in zip(n.targets[0].elts,v):
   if isinstance(k,ast.Name):caps[k.id]=x
assert tuple(caps[k] for k in ('TOTAL_WALL','STAGE_WALL','RSS','RESERVE','HISTORY_CAP','FREE_FLOOR'))==(1800,600,512,2*2**30,96*2**30,8*2**30)
for name in ('prepare_build','run_build','environment','complete_input_phase','create_complete_input_graph','modules','resources_for','DynamicHistoryResources','graph_input_bindings','check_failed_prepare_phase','declaration_admission','prepare_terminal_admission'):
 assert nd[name]==od[name],name
assert "if Path(__file__).absolute()!=FORMAL_FACTORY:" in nd['require_ready']
assert 'single-thread environment required before project import' in nd['require_ready']
for p,h in fixed.items():
 _,z=pin(p,h);assert z==pins[p],(str(p),'before-after')
out=Path(tempfile.mkdtemp(prefix='axmat_v20_complete_strict_JSON_raw_last_use_independent_SOURCE_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V20_COMPLETE_STRICT_JSON_RAW_LAST_USE_FINITE_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY_RUNTIME_REQUIRED',source_inputs=list(pins.values()),all_input_full_EOF_SHA7ID_before_after_equal=True,unique_parent_34ef=True,all10_edits_whole_byte_inverse_to_34ef_exact=True,definition_count=70,only_changed_definitions=changed,other68_definitions_byteexact=True,all_original_If_Assert_Raise_Call_Return_AST_order_exact_except_require_ready_version=True,strict_json_only_del_raw_after_original_complete_loads=True,strict_JSON_duplicate_nonfinite_utf8_finite_walk_and_return_unchanged=True,raw_name_Load_count=1,raw_after_del_Load_count=0,no_nested_raw_closure_reference=True,read_path_direct_complete_require_readbytes_call_unchanged=True,no_added_caller_raw_local_or_cache=True,private_raw_reference_lifetime_changed_only=True,Python_caller_interpreter_or_other_live_references_or_RSS_release_not_proved=True,all_static_physical_input_pin_math_graph_trace_alias_namespace_condition_and_call_scope_declarations_unchanged=True,all_unchanged_globals_exact_except_fresh_family_and_UNREADY_status=sorted(allowed),genuine_guard_MRO_resource_API_functions_unchanged=True,caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0),helper_bcd_Qd490_and_original_component_bindings_unchanged=True,physical_payloads_not_reread_or_interpreted=True,six_future_business_pins_None=True,UNREADY_guard_blocks_TMP_or_unbound_business=True,no_project_module_import_API_guard_resource_business_numeric_execution=True,no_canonical_or_ART_writes=True,no_actual_RSS_cause_or_expected_future_PASS_guarantee=True,new_PREP_build_wholeINPUT_native_AAA_ABA_credit=False,no_blocker=True)
p=out/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(out/'REPORT.txt').write_text('完整 V20 c7cf UNREADY 候选有限独立 SOURCE 审查通过，无 blocker。\n唯一父源34ef：全部10项整字节inverse准确，70定义中仅strict_json_bytes及require_ready版本不同，其余68逐字节保持。\n严格JSON函数只在原json.loads完整返回后增加del raw；删除该一条语句后AST完全同原函数。全部原If/Assert/Raise/Call/Return及顺序保持，UTF8/重复key/nonfinite/完整递归finite检查和返回value保持。\nraw只有原decode处一次Load，delete后无Load，嵌套函数无raw闭包引用。read(path)仍直接return strict_json_bytes(require(path).read_bytes())，无新增caller raw变量/缓存。\n静态所有物理输入pin及数学/图/trace/aliases/namespaces/历史/完整阶段检查范围不变。全部globals除fresh20 family及UNREADY状态外精确保持；bcd/d490及原组件bindings保持。\n原genuineguard/MRO/resource/API、1800/600秒/512MiB/2GiB/history96/free8GiB/1thread/1child/0retry保持，6未来业务pinsNone。\n只证明私有raw局部引用last-use调整；不能保证Python caller/interpreter或其他引用已释放，不能证明此前RSS峰值具体因果，不能预测V20实际PASS。\n本次6个SOURCE/有限proof/manifest全SHA7ID前后保持。不读物理数字payload、不import或运行模块/API/guard/resource/业务/数值、不写canonical/ART。\n仍UNREADY；没有新的PREP/build/fullINPUT/native/AAA/ABA实际成功资格。Root随后READY只两项绑定必须另作有限append复核。\n',encoding='utf-8')
print(json.dumps(dict(directory=str(out),review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=review['status'],source_file_count=len(pins),only_changed_definitions=changed,no_blocker=True,business_executed=False)))

from pathlib import Path
import ast, copy, hashlib, json, stat, tempfile

D=Path('/private/tmp/axmat_v20_complete_build_private_verifier_lifetime_SOURCE_ONLY_20261010')
C=D/'combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.UNREADY.py'
P=D/'frozen_parent_complete_helper_bcd.py'
fixed_c='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
fixed_p='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
fixed_m='1066c201012c9d35e8cfa2d3ccdd2ae98071d7a5c557b2e69c8c9a5a7bb86c61'
def sha(b):return hashlib.sha256(b).hexdigest()
def id7(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,want=None,identity=None):
 a=id7(p);raw=p.read_bytes();b=id7(p);assert a==b
 h=sha(raw)
 if want is not None:assert h==want,(str(p),h,want)
 if identity is not None:assert a==identity
 return raw,dict(path=str(p),sha256=h,identity7=a,whole_EOF_read=True)
mr,mp=pin(D/'sealed_manifest.json',fixed_m);m=json.loads(mr)
assert len(m['members'])==7
assert {p.name for p in D.iterdir()}=={Path(x['path']).name for x in m['members']}|{'sealed_manifest.json'}
raws={};before=[mp]
for x in m['members']:
 p=Path(x['path']);assert p.parent==D
 raw,q=pin(p,x['sha256'],x['identity']);raws[p]=raw;before.append(q)
assert sha(raws[C])==fixed_c and sha(raws[P])==fixed_p
proof=json.loads(raws[D/'full_finite_source_inverse_proof.json'])
assert len(proof['changes'])==11 and proof['local_edit_count']==11
assert proof['actual_NEW_helper_qualification_sha256']is None
assert proof['actual_NEW_combined_decl_build_admission_native_pins']is None
old=raws[P].decode();new=raws[C].decode()
forward=old
for c in proof['changes']:
 assert forward.count(c['before'])==c['count']==1
 forward=forward.replace(c['before'],c['after'])
assert forward==new
back=new
for c in reversed(proof['changes']):
 assert back.count(c['after'])==c['count']==1
 back=back.replace(c['after'],c['before'])
assert back.encode()==raws[P]
ot=ast.parse(old);nt=ast.parse(new)
def fs(s,t):
 ls=s.splitlines(True)
 return {x.name:(x,''.join(ls[x.lineno-1:x.end_lineno]))for x in t.body if isinstance(x,ast.FunctionDef)}
of=fs(old,ot);nf=fs(new,nt)
assert len(of)==len(nf)==79
assert sum(isinstance(n,ast.FunctionDef)for n in ast.walk(ot))==sum(isinstance(n,ast.FunctionDef)for n in ast.walk(nt))==92
assert list(of)==list(nf)
changed=[k for k in of if of[k][1]!=nf[k][1]]
assert changed==['_trace_records','_phase','verify_graph']
assert [n.name for n in ast.walk(ot)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]==[n.name for n in ast.walk(nt)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
assert [ast.dump(n,include_attributes=False)for n in ot.body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False)for n in nt.body if not isinstance(n,ast.FunctionDef)]
def consume_name(n):return isinstance(n,ast.Name)and n.id=='_consume'
class StripPrivateLifetime(ast.NodeTransformer):
 def __init__(self,name):self.name=name
 def visit_If(self,n):
  if self.name=='_trace_records'and consume_name(n.test):return None
  if self.name=='verify_graph'and ast.unparse(n.test)=='consumer is None'and len(n.body)==1 and isinstance(n.body[0],ast.Delete):return None
  return self.generic_visit(n)
 def visit_Delete(self,n):
  if self.name=='_phase':return None
  return n
 def visit_Assign(self,n):
  if self.name=='_trace_records'and any(isinstance(x,ast.Name)and x.id=='consumed_index'for x in n.targets):return None
  if self.name=='_phase'and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='owner'and isinstance(n.value,ast.Constant)and n.value.value is None:
   # Preserve original owner=None inside release-owned branch; added one is direct-body.
   if n in self.root.body:return None
  return self.generic_visit(n)
 def visit_AugAssign(self,n):
  if self.name=='_trace_records'and isinstance(n.target,ast.Name)and n.target.id=='consumed_index':return None
  return self.generic_visit(n)
 def visit_Expr(self,n):
  if self.name=='_trace_records'and isinstance(n.value,ast.Call)and any(isinstance(x,ast.Name)and x.id=='_consume'for x in ast.walk(n.value)):return None
  return self.generic_visit(n)
 def visit_Call(self,n):
  if self.name=='verify_graph'and isinstance(n.func,ast.Name)and n.func.id=='_trace_records':n.keywords=[x for x in n.keywords if x.arg!='_consume']
  return self.generic_visit(n)
normalized={}
for name in changed:
 n=copy.deepcopy(nf[name][0]);normal=StripPrivateLifetime(name);normal.root=n
 if name=='_trace_records':
  assert len(n.args.kwonlyargs)==1 and n.args.kwonlyargs[0].arg=='_consume'
  assert len(n.args.kw_defaults)==1 and isinstance(n.args.kw_defaults[0],ast.Constant)and n.args.kw_defaults[0].value is False
  n.args.kwonlyargs=[];n.args.kw_defaults=[]
 n=normal.visit(n)
 assert ast.dump(n,include_attributes=False)==ast.dump(of[name][0],include_attributes=False),name
 normalized[name]=True
# No post-delete uses of private phase containers, and no later calls to add().
phase=nf['_phase'][0];phase_lastuse=[]
for n in ast.walk(phase):
 if isinstance(n,ast.Delete):
  for target in n.targets:
   assert isinstance(target,ast.Name)
   assert not any(isinstance(x,ast.Name)and isinstance(x.ctx,ast.Load)and x.id==target.id and x.lineno>n.lineno for x in ast.walk(phase)),target.id
   phase_lastuse.append(dict(name=target.id,line=n.lineno))
owner_delete=next(n for n in ast.walk(phase)if isinstance(n,ast.Delete)and any(isinstance(x,ast.Name)and x.id=='owners'for x in n.targets))
assert all(x.lineno<owner_delete.lineno for x in ast.walk(phase)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='add')
assert ast.dump(next(x for x in phase.body if isinstance(x,ast.Return)),include_attributes=False)==ast.dump(next(x for x in of['_phase'][0].body if isinstance(x,ast.Return)),include_attributes=False)
trace=nf['_trace_records'][0]
private_calls=[]
all_trace_calls=[]
for fn,(n,src)in nf.items():
 for x in ast.walk(n):
  if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='_trace_records':
   all_trace_calls.append(dict(function=fn,line=x.lineno,source=ast.unparse(x)))
   kws=[v for v in x.keywords if v.arg=='_consume']
   if kws:
    assert fn=='verify_graph'and len(kws)==1 and ast.unparse(kws[0].value)=='consumer is None';private_calls.append(fn)
assert private_calls==['verify_graph']and len(all_trace_calls)==3
source_trace=nf['_trace_records'][1]
assert 'type(_consume) is bool and (not _consume or type(values) is list)'in source_trace
assert source_trace.index('result.append(record)')<source_trace.index('values[consumed_index] = None')<source_trace.index('values.clear()')<source_trace.index('return result')
verify=nf['verify_graph'][0]
assert ast.dump(next(x for x in verify.body if isinstance(x,ast.Return)),include_attributes=False)==ast.dump(next(x for x in of['verify_graph'][0].body if isinstance(x,ast.Return)),include_attributes=False)
# All deleted graph fields' complete-branch later uses are either absent or consumer-only.
vsrc=nf['verify_graph'][1]
assert vsrc.index('_content_digest(graph)')<vsrc.index('del graph["owners"]')
assert vsrc.index('_wire_semantic_content_digest(graph)')<vsrc.index('del graph["owners"]')
assert vsrc.index('_owners(_expand_owner_table')<vsrc.index('del graph["owners"]')
assert vsrc.index('namespaces = [_namespace_descriptor')<vsrc.index('del graph["namespaces"]')
assert vsrc.index('del rebuilt_requirements')<vsrc.index('_require([actual[path]')<vsrc.index('_require(new_pins == frozen_new')<vsrc.index('del graph["requirements"], graph["canonical_files"]')
assert '_subprocess_records(graph["read_trace"])'in vsrc
assert '"records"'not in nf['_subprocess_records'][1]
assert 'graph = _json_clone(graph)'in vsrc and 'graph = strict_json(graph' in vsrc
assert 'return _json_clone(value)'in nf['_namespace_descriptor'][1]
assert 'return {key: clone(item[key]) for key in sorted(item)}'in nf['_json_clone'][1]
assert 'return [clone(part) for part in item]'in nf['_json_clone'][1]
plan=json.loads(raws[D/'SOURCE_ANALYSIS_AND_QUALIFICATION_PLAN.json'])
assert plan['actual_NEW_helper_qualification_SHA']is None
assert plan['actual_NEW_combined_declaration_build_seal_terminal_INPUT_native_pins']is None
assert plan['original_caps']==dict(whole_seconds=1800,stage_seconds=600,RSS_MiB=512,whole_SOURCE_OUT_archive_bytes=2147483648,strict_helper_JSON_bytes=67108864,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children=1,retries=0)
after=[]
for q in before:
 _,z=pin(Path(q['path']),q['sha256'],q['identity7']);after.append(z)
assert before==after
assert {p.name for p in D.iterdir()}=={Path(x['path']).name for x in m['members']}|{'sealed_manifest.json'}
O=Path(tempfile.mkdtemp(prefix='axmat_private_complete_verifier_helper_independent_SOURCE_review_20261010_',dir='/private/tmp'))
report=dict(schema='FINITE_FULL_HELPER_LIFETIME_INDEPENDENT_SOURCE_REVIEW_V1',status='SOURCE_ONLY_NO_BLOCKER_FOUND_QUALIFICATION_PENDING',source_blockers=[],candidate=dict(path=str(C),sha256=fixed_c,size_bytes=len(raws[C])),parent=dict(path=str(P),sha256=fixed_p),input_sealed_manifest=dict(path=str(D/'sealed_manifest.json'),sha256=fixed_m,seven_members_all_SHA7ID_exact=True),finite_inverse=dict(edits=11,functions=changed,complete_forward_and_inverse_exact=True,all_top_functions=79,all_nested_method_functions=92,remaining_76_top_function_bytes_exact=True,all_module_nonfunction_AST_exact=True,all_three_original_function_AST_exact_after_removing_only_private_lifetime_edits=True),phase_private_name_lastuses=phase_lastuse,trace_calls=all_trace_calls,
confirmed=[
'Every original predicate, call ordering structure, loop, and complete return in the three changed functions is preserved when only the independently identified lifetime additions/private keyword are removed; no original return field or complete collection is filtered.',
'verify_graph always fresh-parses a pinned path or deep JSON-clones a mapping before the private field deletions. Every builtin mutable dict/list in the mapping clone is independently rebuilt; external mutable input is not consumed.',
'Graph owners are removed only after the original full content/wire-content/owner gates. Full normalized owners remain for all original phase requirements.',
'Graph namespaces are removed only after every original descriptor validation and deep clone. The normalized complete namespace list remains for all before/after and trace checks.',
'Graph requirements and canonical_files are removed only after original full rebuilt requirement equality, complete canonical pin equality, and frozen-new pin equality. Fresh complete requirements and actual canonical pins remain for coverage and return counts.',
'Consumer branches retain original graph sections, owner maps, fresh complete parent-lineage checks, selected literal/canonical paths, namespace root sequence and complete return semantics.',
'The private trace keyword is exact bool; consume=True additionally requires exact builtin list. Only the verifier supplies it, and consumer is None evaluates to a real bool. This guard checks shape, not ownership itself; ownership follows the parse/clone call chain.',
'Default _consume=False accepts the same original list/tuple/mapping trace inputs, performs every original record predicate/clone/path/descriptor check in order, appends all records in order, and never assigns or clears source records.',
'Private consume releases each old row only after every original row check, deep clone and full append. The final full normalized records are passed unchanged to original trace coverage; later subprocess normalization reads its separate subprocess_records field.',
'_phase deletes only private local indexes and ownership references after every original add/expected union/end-point/new-pin use. No external owner/input container is cleared or modified. The original four complete return items remain identical.',
'There is no exception handler in these changed functions that subsequently depends on a deleted container. Original rejection predicates/messages remain; the explicit private bool/list guard is the one added rejection.'
],
qualification_pending=[
'Original complete 60-second /512 MiB /64 MiB pure-control protocol must be executed once in its own fresh namespace with all existing accepted mapping subclasses, malformed cases, default nonmutation, consumer lineage, two entrances, complete graph codec/trace/value/type/order/float-bit controls retained.',
'A separate real full current V20 graph fresh verifier run covering the complete current canonical file union is additionally required, with unchanged stage600/whole1800/RSS512 and ordinary 1thread/1child/0retry semantics. Existing small-fixture verifier receipt does not prove this scale.',
'Neither qualification has been run by this reviewer. The new helper qualification and all future combined/native pins remain None.',
'No actual RSS contribution or peak source line was observed; SOURCE-only acceptance is not RSS PASS, complete build, whole INPUT admission, native, AAA or ABA success.'
],source_pins_before_after=before,all_source_and_metadata_SHA7ID_before_after_exact=True,scope=dict(helper_imported_or_executed=False,project_API_guard_resource_business_called=False,numeric_payload_read=False,ART_read_or_modified=False,canonical_or_input_package_changed=False))
(O/'REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(O/'REPORT.txt').write_text('完整 helper 有限独立 SOURCE 审查：未发现 SOURCE blocker；新资格仍待实际运行。\n\n新候选 dc01d8 的 11 项完整 inverse 精确回 bcd692。79 顶层函数、92 含 nested/method 函数原名称/数量保持；仅 _phase/_trace_records/verify_graph 改动，其余 76 顶层函数逐字节相同。移除所识别的新增生命周期语句和私有 keyword 后，三函数完整原 AST 相同，包括全部谓词、调用、循环、返回。\n\n所有 graph 字段删除仅在 fresh parse/deep clone 的独占完整图、consumer None 分支，并在原完整 gate 完成后。原 consumer 输入、默认 trace 输入、外部 mutable graph/owner 不被消费。_consume 是实际 bool，仅 True 要求 exact builtin list；形状 guard 本身不证明独占，独占来自唯一 verifier parse/clone 调用链。每条 trace 原验证/深 clone/完整 append 在旧行清除之前，完整记录和 attempt counts 保持；独立 subprocess_records 后续未删除。\n\n原 guard/caps/global/class/算法不变，Source 封存 7 members+manifest 全 SHA/7ID 前后保持。未 import/execute helper/API/guard/resource/业务/数值，未读 ART payload，未改 canonical 或作者封存包。\n\n仍必须以原 60s/512MiB/64MiB 控制协议实际资格，再独立执行一次当前完整全图 fresh verifier（stage600s/whole1800s/512MiB；1thread/1child/0retry）。不能把已有小 fixture verifier 的 392MiB 结果当当前全图 RSS 资格。新 qualification 和 future business/native pins 均 None；实际峰值源码行未观测，本包不授 RSS PASS/build/native/AAA/ABA 信用。\n')
(O/'source_review.py').write_text("from pathlib import Path\nimport ast, copy, hashlib, json, stat, tempfile\n\nD=Path('/private/tmp/axmat_v20_complete_build_private_verifier_lifetime_SOURCE_ONLY_20261010')\nC=D/'combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.UNREADY.py'\nP=D/'frozen_parent_complete_helper_bcd.py'\nfixed_c='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'\nfixed_p='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'\nfixed_m='1066c201012c9d35e8cfa2d3ccdd2ae98071d7a5c557b2e69c8c9a5a7bb86c61'\ndef sha(b):return hashlib.sha256(b).hexdigest()\ndef id7(p):\n s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()\n return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]\ndef pin(p,want=None,identity=None):\n a=id7(p);raw=p.read_bytes();b=id7(p);assert a==b\n h=sha(raw)\n if want is not None:assert h==want,(str(p),h,want)\n if identity is not None:assert a==identity\n return raw,dict(path=str(p),sha256=h,identity7=a,whole_EOF_read=True)\nmr,mp=pin(D/'sealed_manifest.json',fixed_m);m=json.loads(mr)\nassert len(m['members'])==7\nassert {p.name for p in D.iterdir()}=={Path(x['path']).name for x in m['members']}|{'sealed_manifest.json'}\nraws={};before=[mp]\nfor x in m['members']:\n p=Path(x['path']);assert p.parent==D\n raw,q=pin(p,x['sha256'],x['identity']);raws[p]=raw;before.append(q)\nassert sha(raws[C])==fixed_c and sha(raws[P])==fixed_p\nproof=json.loads(raws[D/'full_finite_source_inverse_proof.json'])\nassert len(proof['changes'])==11 and proof['local_edit_count']==11\nassert proof['actual_NEW_helper_qualification_sha256']is None\nassert proof['actual_NEW_combined_decl_build_admission_native_pins']is None\nold=raws[P].decode();new=raws[C].decode()\nforward=old\nfor c in proof['changes']:\n assert forward.count(c['before'])==c['count']==1\n forward=forward.replace(c['before'],c['after'])\nassert forward==new\nback=new\nfor c in reversed(proof['changes']):\n assert back.count(c['after'])==c['count']==1\n back=back.replace(c['after'],c['before'])\nassert back.encode()==raws[P]\not=ast.parse(old);nt=ast.parse(new)\ndef fs(s,t):\n ls=s.splitlines(True)\n return {x.name:(x,''.join(ls[x.lineno-1:x.end_lineno]))for x in t.body if isinstance(x,ast.FunctionDef)}\nof=fs(old,ot);nf=fs(new,nt)\nassert len(of)==len(nf)==79\nassert sum(isinstance(n,ast.FunctionDef)for n in ast.walk(ot))==sum(isinstance(n,ast.FunctionDef)for n in ast.walk(nt))==92\nassert list(of)==list(nf)\nchanged=[k for k in of if of[k][1]!=nf[k][1]]\nassert changed==['_trace_records','_phase','verify_graph']\nassert [n.name for n in ast.walk(ot)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]==[n.name for n in ast.walk(nt)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]\nassert [ast.dump(n,include_attributes=False)for n in ot.body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False)for n in nt.body if not isinstance(n,ast.FunctionDef)]\ndef consume_name(n):return isinstance(n,ast.Name)and n.id=='_consume'\nclass StripPrivateLifetime(ast.NodeTransformer):\n def __init__(self,name):self.name=name\n def visit_If(self,n):\n  if self.name=='_trace_records'and consume_name(n.test):return None\n  if self.name=='verify_graph'and ast.unparse(n.test)=='consumer is None'and len(n.body)==1 and isinstance(n.body[0],ast.Delete):return None\n  return self.generic_visit(n)\n def visit_Delete(self,n):\n  if self.name=='_phase':return None\n  return n\n def visit_Assign(self,n):\n  if self.name=='_trace_records'and any(isinstance(x,ast.Name)and x.id=='consumed_index'for x in n.targets):return None\n  if self.name=='_phase'and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='owner'and isinstance(n.value,ast.Constant)and n.value.value is None:\n   # Preserve original owner=None inside release-owned branch; added one is direct-body.\n   if n in self.root.body:return None\n  return self.generic_visit(n)\n def visit_AugAssign(self,n):\n  if self.name=='_trace_records'and isinstance(n.target,ast.Name)and n.target.id=='consumed_index':return None\n  return self.generic_visit(n)\n def visit_Expr(self,n):\n  if self.name=='_trace_records'and isinstance(n.value,ast.Call)and any(isinstance(x,ast.Name)and x.id=='_consume'for x in ast.walk(n.value)):return None\n  return self.generic_visit(n)\n def visit_Call(self,n):\n  if self.name=='verify_graph'and isinstance(n.func,ast.Name)and n.func.id=='_trace_records':n.keywords=[x for x in n.keywords if x.arg!='_consume']\n  return self.generic_visit(n)\nnormalized={}\nfor name in changed:\n n=copy.deepcopy(nf[name][0]);normal=StripPrivateLifetime(name);normal.root=n\n if name=='_trace_records':\n  assert len(n.args.kwonlyargs)==1 and n.args.kwonlyargs[0].arg=='_consume'\n  assert len(n.args.kw_defaults)==1 and isinstance(n.args.kw_defaults[0],ast.Constant)and n.args.kw_defaults[0].value is False\n  n.args.kwonlyargs=[];n.args.kw_defaults=[]\n n=normal.visit(n)\n assert ast.dump(n,include_attributes=False)==ast.dump(of[name][0],include_attributes=False),name\n normalized[name]=True\n# No post-delete uses of private phase containers, and no later calls to add().\nphase=nf['_phase'][0];phase_lastuse=[]\nfor n in ast.walk(phase):\n if isinstance(n,ast.Delete):\n  for target in n.targets:\n   assert isinstance(target,ast.Name)\n   assert not any(isinstance(x,ast.Name)and isinstance(x.ctx,ast.Load)and x.id==target.id and x.lineno>n.lineno for x in ast.walk(phase)),target.id\n   phase_lastuse.append(dict(name=target.id,line=n.lineno))\nowner_delete=next(n for n in ast.walk(phase)if isinstance(n,ast.Delete)and any(isinstance(x,ast.Name)and x.id=='owners'for x in n.targets))\nassert all(x.lineno<owner_delete.lineno for x in ast.walk(phase)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='add')\nassert ast.dump(next(x for x in phase.body if isinstance(x,ast.Return)),include_attributes=False)==ast.dump(next(x for x in of['_phase'][0].body if isinstance(x,ast.Return)),include_attributes=False)\ntrace=nf['_trace_records'][0]\nprivate_calls=[]\nall_trace_calls=[]\nfor fn,(n,src)in nf.items():\n for x in ast.walk(n):\n  if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='_trace_records':\n   all_trace_calls.append(dict(function=fn,line=x.lineno,source=ast.unparse(x)))\n   kws=[v for v in x.keywords if v.arg=='_consume']\n   if kws:\n    assert fn=='verify_graph'and len(kws)==1 and ast.unparse(kws[0].value)=='consumer is None';private_calls.append(fn)\nassert private_calls==['verify_graph']and len(all_trace_calls)==3\nsource_trace=nf['_trace_records'][1]\nassert 'type(_consume) is bool and (not _consume or type(values) is list)'in source_trace\nassert source_trace.index('result.append(record)')<source_trace.index('values[consumed_index] = None')<source_trace.index('values.clear()')<source_trace.index('return result')\nverify=nf['verify_graph'][0]\nassert ast.dump(next(x for x in verify.body if isinstance(x,ast.Return)),include_attributes=False)==ast.dump(next(x for x in of['verify_graph'][0].body if isinstance(x,ast.Return)),include_attributes=False)\n# All deleted graph fields' complete-branch later uses are either absent or consumer-only.\nvsrc=nf['verify_graph'][1]\nassert vsrc.index('_content_digest(graph)')<vsrc.index('del graph[\"owners\"]')\nassert vsrc.index('_wire_semantic_content_digest(graph)')<vsrc.index('del graph[\"owners\"]')\nassert vsrc.index('_owners(_expand_owner_table')<vsrc.index('del graph[\"owners\"]')\nassert vsrc.index('namespaces = [_namespace_descriptor')<vsrc.index('del graph[\"namespaces\"]')\nassert vsrc.index('del rebuilt_requirements')<vsrc.index('_require([actual[path]')<vsrc.index('_require(new_pins == frozen_new')<vsrc.index('del graph[\"requirements\"], graph[\"canonical_files\"]')\nassert '_subprocess_records(graph[\"read_trace\"])'in vsrc\nassert '\"records\"'not in nf['_subprocess_records'][1]\nassert 'graph = _json_clone(graph)'in vsrc and 'graph = strict_json(graph' in vsrc\nassert 'return _json_clone(value)'in nf['_namespace_descriptor'][1]\nassert 'return {key: clone(item[key]) for key in sorted(item)}'in nf['_json_clone'][1]\nassert 'return [clone(part) for part in item]'in nf['_json_clone'][1]\nplan=json.loads(raws[D/'SOURCE_ANALYSIS_AND_QUALIFICATION_PLAN.json'])\nassert plan['actual_NEW_helper_qualification_SHA']is None\nassert plan['actual_NEW_combined_declaration_build_seal_terminal_INPUT_native_pins']is None\nassert plan['original_caps']==dict(whole_seconds=1800,stage_seconds=600,RSS_MiB=512,whole_SOURCE_OUT_archive_bytes=2147483648,strict_helper_JSON_bytes=67108864,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children=1,retries=0)\nafter=[]\nfor q in before:\n _,z=pin(Path(q['path']),q['sha256'],q['identity7']);after.append(z)\nassert before==after\nassert {p.name for p in D.iterdir()}=={Path(x['path']).name for x in m['members']}|{'sealed_manifest.json'}\nO=Path(tempfile.mkdtemp(prefix='axmat_private_complete_verifier_helper_independent_SOURCE_review_20261010_',dir='/private/tmp'))\nreport=dict(schema='FINITE_FULL_HELPER_LIFETIME_INDEPENDENT_SOURCE_REVIEW_V1',status='SOURCE_ONLY_NO_BLOCKER_FOUND_QUALIFICATION_PENDING',source_blockers=[],candidate=dict(path=str(C),sha256=fixed_c,size_bytes=len(raws[C])),parent=dict(path=str(P),sha256=fixed_p),input_sealed_manifest=dict(path=str(D/'sealed_manifest.json'),sha256=fixed_m,seven_members_all_SHA7ID_exact=True),finite_inverse=dict(edits=11,functions=changed,complete_forward_and_inverse_exact=True,all_top_functions=79,all_nested_method_functions=92,remaining_76_top_function_bytes_exact=True,all_module_nonfunction_AST_exact=True,all_three_original_function_AST_exact_after_removing_only_private_lifetime_edits=True),phase_private_name_lastuses=phase_lastuse,trace_calls=all_trace_calls,\nconfirmed=[\n'Every original predicate, call ordering structure, loop, and complete return in the three changed functions is preserved when only the independently identified lifetime additions/private keyword are removed; no original return field or complete collection is filtered.',\n'verify_graph always fresh-parses a pinned path or deep JSON-clones a mapping before the private field deletions. Every builtin mutable dict/list in the mapping clone is independently rebuilt; external mutable input is not consumed.',\n'Graph owners are removed only after the original full content/wire-content/owner gates. Full normalized owners remain for all original phase requirements.',\n'Graph namespaces are removed only after every original descriptor validation and deep clone. The normalized complete namespace list remains for all before/after and trace checks.',\n'Graph requirements and canonical_files are removed only after original full rebuilt requirement equality, complete canonical pin equality, and frozen-new pin equality. Fresh complete requirements and actual canonical pins remain for coverage and return counts.',\n'Consumer branches retain original graph sections, owner maps, fresh complete parent-lineage checks, selected literal/canonical paths, namespace root sequence and complete return semantics.',\n'The private trace keyword is exact bool; consume=True additionally requires exact builtin list. Only the verifier supplies it, and consumer is None evaluates to a real bool. This guard checks shape, not ownership itself; ownership follows the parse/clone call chain.',\n'Default _consume=False accepts the same original list/tuple/mapping trace inputs, performs every original record predicate/clone/path/descriptor check in order, appends all records in order, and never assigns or clears source records.',\n'Private consume releases each old row only after every original row check, deep clone and full append. The final full normalized records are passed unchanged to original trace coverage; later subprocess normalization reads its separate subprocess_records field.',\n'_phase deletes only private local indexes and ownership references after every original add/expected union/end-point/new-pin use. No external owner/input container is cleared or modified. The original four complete return items remain identical.',\n'There is no exception handler in these changed functions that subsequently depends on a deleted container. Original rejection predicates/messages remain; the explicit private bool/list guard is the one added rejection.'\n],\nqualification_pending=[\n'Original complete 60-second /512 MiB /64 MiB pure-control protocol must be executed once in its own fresh namespace with all existing accepted mapping subclasses, malformed cases, default nonmutation, consumer lineage, two entrances, complete graph codec/trace/value/type/order/float-bit controls retained.',\n'A separate real full current V20 graph fresh verifier run covering the complete current canonical file union is additionally required, with unchanged stage600/whole1800/RSS512 and ordinary 1thread/1child/0retry semantics. Existing small-fixture verifier receipt does not prove this scale.',\n'Neither qualification has been run by this reviewer. The new helper qualification and all future combined/native pins remain None.',\n'No actual RSS contribution or peak source line was observed; SOURCE-only acceptance is not RSS PASS, complete build, whole INPUT admission, native, AAA or ABA success.'\n],source_pins_before_after=before,all_source_and_metadata_SHA7ID_before_after_exact=True,scope=dict(helper_imported_or_executed=False,project_API_guard_resource_business_called=False,numeric_payload_read=False,ART_read_or_modified=False,canonical_or_input_package_changed=False))\n(O/'REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\\n')\n(O/'REPORT.txt').write_text('完整 helper 有限独立 SOURCE 审查：未发现 SOURCE blocker；新资格仍待实际运行。\\n\\n新候选 dc01d8 的 11 项完整 inverse 精确回 bcd692。79 顶层函数、92 含 nested/method 函数原名称/数量保持；仅 _phase/_trace_records/verify_graph 改动，其余 76 顶层函数逐字节相同。移除所识别的新增生命周期语句和私有 keyword 后，三函数完整原 AST 相同，包括全部谓词、调用、循环、返回。\\n\\n所有 graph 字段删除仅在 fresh parse/deep clone 的独占完整图、consumer None 分支，并在原完整 gate 完成后。原 consumer 输入、默认 trace 输入、外部 mutable graph/owner 不被消费。_consume 是实际 bool，仅 True 要求 exact builtin list；形状 guard 本身不证明独占，独占来自唯一 verifier parse/clone 调用链。每条 trace 原验证/深 clone/完整 append 在旧行清除之前，完整记录和 attempt counts 保持；独立 subprocess_records 后续未删除。\\n\\n原 guard/caps/global/class/算法不变，Source 封存 7 members+manifest 全 SHA/7ID 前后保持。未 import/execute helper/API/guard/resource/业务/数值，未读 ART payload，未改 canonical 或作者封存包。\\n\\n仍必须以原 60s/512MiB/64MiB 控制协议实际资格，再独立执行一次当前完整全图 fresh verifier（stage600s/whole1800s/512MiB；1thread/1child/0retry）。不能把已有小 fixture verifier 的 392MiB 结果当当前全图 RSS 资格。新 qualification 和 future business/native pins 均 None；实际峰值源码行未观测，本包不授 RSS PASS/build/native/AAA/ABA 信用。\\n')\n(O/'source_review.py').write_text(__SOURCE_AUDIT__)\nprint(json.dumps(dict(directory=str(O),status=report['status'],candidate_sha256=fixed_c,review_sha256=sha((O/'REVIEW.json').read_bytes()),input_manifest_sha256=fixed_m,source_blockers=0),ensure_ascii=False))\n")
print(json.dumps(dict(directory=str(O),status=report['status'],candidate_sha256=fixed_c,review_sha256=sha((O/'REVIEW.json').read_bytes()),input_manifest_sha256=fixed_m,source_blockers=0),ensure_ascii=False))

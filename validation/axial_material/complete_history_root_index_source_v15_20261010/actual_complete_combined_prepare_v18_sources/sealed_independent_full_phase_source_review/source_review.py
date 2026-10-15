import ast
import hashlib
import json
from pathlib import Path
import stat
import tempfile
D=Path('/private/tmp/axmat_v18_complete_combined_full_phase_last_use_source_only_20261010')
C=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py'
P=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
def pin(p,wanted=None):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 q=p.lstat();assert before==[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns] and (wanted is None or sha==wanted)
 return dict(path=str(p),sha256=sha,identity7=before)
proof=json.loads((D/'source_inverse_proof.json').read_text());report=json.loads((D/'REPORT.json').read_text())
pins=[pin(C,'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'),pin(D/'source_inverse_proof.json','920d4cef7d96e8f0737a82f9e5cad8feb7b7c3387324dc128b66f1c45908f0e4'),pin(D/'REPORT.json','b5641ec5da5925450dec6775cc0a4f4e01eb4c91c289c2dec4dcd4da4df9b2c3'),pin(D/'sealed_manifest.json','f17d49472828c20a48a3b4c983847aa6f1f1789d434e5ab980e5c80213a1254c')]
for q in proof['inputs']:
 found=pin(q['path'],q['sha256']);assert found['identity7']==q['identity7'];pins.append(found)
new=C.read_bytes();old=P.read_bytes()
def inverse(child,edits):
 v=child
 for c in reversed(edits):
  a,b=c['old'].encode(),c['new'].encode();assert v.count(b)==c['occurrences'];v=v.replace(b,a)
 return v
restored=inverse(new,proof['edits']);assert restored==old and len(proof['edits'])==10
bindpath=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json');binding=json.loads(bindpath.read_text())
ancestor82=inverse(restored,binding['edits']);assert hashlib.sha256(ancestor82).hexdigest()=='82b17014f36520dadc77c387d8e53f7cdd9b5ea92f31b3ee9659ac5464c6239e'
ancestorproof=json.loads(Path('/private/tmp/axmat_v17_complete_combined_fresh_wire_trace_table_source_only_FINAL_20261010/source_inverse_proof.json').read_text())
ancestor0ea=inverse(ancestor82,ancestorproof['edits']);assert hashlib.sha256(ancestor0ea).hexdigest()=='0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382'
nt=new.decode();ot=old.decode();n_tree=ast.parse(nt);o_tree=ast.parse(ot)
def funcs(text,tree):return {n.name:(n,ast.get_source_segment(text,n)) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=funcs(ot,o_tree);b=funcs(nt,n_tree);assert set(a)==set(b)
changed=[name for name in a if a[name][1]!=b[name][1]];assert changed==['require_ready','complete_input_phase']
oldphase=a['complete_input_phase'][0];newphase=b['complete_input_phase'][0]
def calls(f,name):return [n for n in ast.walk(f) if isinstance(n,ast.Call) and ((isinstance(n.func,ast.Name) and n.func.id==name) or (isinstance(n.func,ast.Attribute) and n.func.attr==name))]
def predicates(f):return [ast.dump(n,include_attributes=False) for n in ast.walk(f) if isinstance(n,(ast.If,ast.Assert,ast.Raise))]
assert predicates(oldphase)==predicates(newphase)
phase=b['complete_input_phase'][1]
assert len(calls(oldphase,'current_input_predicates'))==len(calls(newphase,'current_input_predicates'))==2
assert len(calls(oldphase,'current_new_owned_paths'))==len(calls(newphase,'current_new_owned_paths'))==2
assert len(calls(oldphase,'verify_graph'))==len(calls(newphase,'verify_graph'))==1
assert len(calls(oldphase,'failed_prepare_input'))==len(calls(newphase,'failed_prepare_input'))==2
assert len(calls(oldphase,'collect'))==len(calls(newphase,'collect'))==3
old_specs_reads=[n for n in calls(oldphase,'strict_json') if isinstance(n.args[0],ast.Call) and isinstance(n.args[0].func,ast.Name) and n.args[0].func.id=='str' and ast.dump(n.args[0].args[0])=="Name(id='INPUT_SPECS', ctx=Load())"]
new_specs_reads=[n for n in calls(newphase,'strict_json') if isinstance(n.args[0],ast.Call) and isinstance(n.args[0].func,ast.Name) and n.args[0].func.id=='str' and ast.dump(n.args[0].args[0])=="Name(id='INPUT_SPECS', ctx=Load())"]
assert len(old_specs_reads)==1 and len(new_specs_reads)==2 and all(ast.dump(n.args[1])=="Name(id='INPUT_SPECS_SHA', ctx=Load())" for n in new_specs_reads)
assert phase.count("graph=g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])")==1
assert phase.index('del specs,original_aliases')<phase.index('with g.ReadOpenAudit()as audit:')<phase.index('trace_digest=g._content_digest(trace)')<phase.index('fresh_counts=(')<phase.index('del verified')<phase.index('after=current_input_predicates')<phase.index('length_specs=')<phase.index("graph=g.strict_json(d['input_graph']['path']")<phase.index('del files,complete_aliases,paths,expected_snapshot')<phase.index('pins=')
length_source=Path('/Users/wen/spot/validation/axial_material/combined_runtime_historical_input_checks.py').read_text();lt=ast.parse(length_source)
lf=next(n for n in lt.body if isinstance(n,ast.FunctionDef) and n.name=='check_failed_lengths_and_owned_negative_bytes')
access=[n for n in ast.walk(lf) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='specs']
assert len(access)==1 and isinstance(access[0].slice,ast.Constant) and access[0].slice.value=='remaining_source_owned_requirements'
assert "length_specs={'remaining_source_owned_requirements':specs['remaining_source_owned_requirements']}" in phase
assert not any(isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='specs' and isinstance(n.ctx,ast.Store) for n in ast.walk(lf))
for name in ('environment','declaration_admission','run_build','prepare_build','create_complete_input_graph','graph_input_bindings','current_input_predicates','check_failed_prepare_phase','DynamicHistoryResources','resources_for','modules'):
 assert a[name][1]==b[name][1]
old_return=next(n for n in ast.walk(oldphase) if isinstance(n,ast.Return));new_return=next(n for n in ast.walk(newphase) if isinstance(n,ast.Return))
assert [k.arg for k in old_return.value.keywords]==[k.arg for k in new_return.value.keywords]
keys=['canonical_files_read','actual_bytes_read','logical_owner_requirements','exhaustive_namespaces_checked']
for key,i in zip(keys,range(4)):
 assert "verified['"+key+"']" in phase and 'fresh_counts['+str(i)+']' in phase
future_names=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assignments={n.targets[0].id:n.value for n in n_tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
assert all(isinstance(assignments[k],ast.Constant) and assignments[k].value is None for k in future_names)
assert "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED'" in nt and "if Path(__file__).absolute()!=FORMAL_FACTORY" in b['require_ready'][1]
assert "TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512" in nt and "RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30" in nt
assert len([name for name in a if a[name][1]==b[name][1]])==68
for q in pins:assert pin(q['path'],q['sha256'])==q
out=Path(tempfile.mkdtemp(prefix='axmat_v18_independent_full_phase_last_use_source_review_20261010_',dir='/private/tmp'))
review=dict(schema='INDEPENDENT_FINITE_V18_FULL_PHASE_CALLER_LAST_USE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY_RUNTIME_REQUIRED',candidate_sha256=pins[0]['sha256'],final_candidate_manifest_sha256=pins[3]['sha256'],source_full_byte_inverse_chain=['ecfdff36','feebcbb5','82b17014','0ea1e629'],source_inverse_edit_counts=[10,len(binding['edits']),len(ancestorproof['edits'])],changed_definitions=changed,unchanged_definitions=68,full_source_inverse_chain_exact=True,all_original_phase_If_Assert_Raise_AST_and_order_exact=True,current_before_after_and_owned_path_calls_all_retained=True,full_verify_graph_plus_second_strict_graph_retained=True,both_failed_input_reads_and_checks_retained=True,all_alias_namespace_full_graph_trace_checks_retained=True,original_gc_calls_3_no_new_gc=True,whole_same_SHA_specs_fresh_strict_reread_added=1,private_length_specs_complete_original_single_field_preserved=True,public_and_caller_dictionary_mutation_introduced=False,return_field_names_order_and_immutable_count_sources_preserved=True,entire_seven_historical_body_and_create_graph_unchanged=True,genuine_guard_MRO_resources_rootindex_caps_unchanged=True,future_business_six_pins_None=True,source_inputs_full_sha7id_before_after=pins,no_blocking_source_issue_found=True,business_or_helper_or_module_API_executed=False,numeric_payload_read=False,source_only_no_v18_runtime_admission=True,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,observable_side_effect_difference='One additional full pinned specs EOF/SHA/strict parse. It may fail earlier if those bytes change between before/after; no cross-phase cache or skipped original read/check.',runtime_equivalence_limit='Immutable metadata values and private count origins are preserved by source. Live current/resource facts remain freshly measured and their timestamps may differ. Deleting private views does not promise that all referenced nested objects are freed.',causality_limit='No profiling; original515 MiB source cause is unobserved. No predicted RSS, timing, success or physics PASS claim.')
(out/'REVIEW.json').write_text(json.dumps(review,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('V18 ecfdff… 有限独立 SOURCE 审查通过，无源码阻塞。\n10 + 4 + 13 项变更逆向整字节还原 ecfdff→feeb→82→0ea，70 项函数/类名称不变，仅 require_ready 与 complete_input_phase 改变，68 项其余定义完整不变。\n原 If/Assert/Raise AST和顺序、两 current predicates/owned-path检查、完整verify + 第二strict graph、两failed输入/length/negative检查、原完整图/trace/alias/namespace、whole七项和资源/guard/caps均保留。原gc3次，不新增。\n新增同SHA完整specs fresh读取/解析1次，发生在audit之后/current-after之前；length_specs保留原checker唯一使用字段完整对象。输出字段/顺序和计数来源保持，不修改caller。\n实际I/O副作用多一次完整读取/解析，可能更早拒绝中途变化；live事实时间戳仍实时测量。不能据源码证明所有深层对象释放、515峰值原因、V18预计RSS或PASS。\n候选仍UNREADY，未来6项business pins均None。本轮只读SOURCE/TMP，不导入/调用API、不business/numeric、不改canonical。\n')
print(json.dumps(dict(status=review['status'],directory=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),inverse_chain_exact=True,changed_definitions=changed,no_blocker=True,business_executed=False),allow_nan=False))

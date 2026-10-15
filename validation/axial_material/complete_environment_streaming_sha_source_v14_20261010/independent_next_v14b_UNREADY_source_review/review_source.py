"""Pure AST/text source audit; does not load helper or create fixtures."""
from pathlib import Path
import ast,hashlib,json,stat
D=Path('/private/tmp/axmat_v14b_manual_alias_helper_source_independent_review_20261010')
C=Path('/private/tmp/axmat_v14b_manual_file_alias_streaming_sha_helper_source_draft_20261010')
H=C/'complete_environment_streaming_sha_helper_v14b.py'
pins=[]
def identity(p):
 x=p.lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
def pin(p,w=None):
 p=Path(p);i=identity(p);assert stat.S_ISREG(i[2]);b=p.read_bytes();h=hashlib.sha256(b).hexdigest();assert identity(p)==i
 if w:assert h==w
 r={'path':str(p),'sha256':h,'identity':i};pins.append(r);return b.decode()
def read(p,w=None):return json.loads(pin(p,w))
def scopes(t):
 d={}
 def visit(n,parents):
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
   key=parents+(n.name,);assert key not in d;d[key]=ast.get_source_segment(t,n);parents=key
  for child in ast.iter_child_nodes(n):visit(child,parents)
 visit(ast.parse(t),());return d
ct=pin(H,'7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3')
p619=read(C/'source_complete_inverse_619.json','0a4a389511d952cef3e5e7318a266a851cf851d5ef5358346748760fd2882e94')
p839=read(C/'source_finite_inverse_839.json','452e6d51f166ec3234055871291d3d4cc44b79d740cc0340814b5fad2e5b6380')
original=pin(p619['parent']['path'],p619['parent']['sha256']);older=pin(p839['parent']['path'],p839['parent']['sha256'])
assert len(p619['regions'])==1 and len(p839['regions'])==3
for proof,old,keys in [(p619,original,('before','after')),(p839,older,('old','new'))]:
 inv=ct
 for e in reversed(proof['regions']):
  assert inv.count(e[keys[1]])==e['count'];inv=inv.replace(e[keys[1]],e[keys[0]],e['count'])
 assert inv==old
 forward=old
 for e in proof['regions']:
  assert forward.count(e[keys[0]])==e['count'];forward=forward.replace(e[keys[0]],e[keys[1]],e['count'])
 assert forward==ct
scope619=scopes(original);scope839=scopes(older);scope=scopes(ct)
assert len(scope619)==34 and all(scope[k]==v for k,v in scope619.items() if k!=('digest',))
changed=[k for k,v in scope839.items() if scope[k]!=v];assert changed==[('_env_stream_path_snapshot',)]
added=set(scope)-set(scope839);assert added=={('_env_stream_native_alias_path_snapshot',)}
old=scope839[('_env_stream_path_snapshot',)];native=scope[('_env_stream_native_alias_path_snapshot',)]
assert native.replace('def _env_stream_native_alias_path_snapshot(', 'def _env_stream_path_snapshot(',1)==old
filewalk=scope[('_env_stream_path_snapshot',)]
assert '.resolve(' not in filewalk
assert 'if not require_regular:\n        return _env_stream_native_alias_path_snapshot(literal, require_regular=require_regular)' in filewalk
assert 'remaining_components = len(pending)' in filewalk
assert 'remaining_components -= 1' in filewalk and 'remaining_components += len(target_parts)' in filewalk
assert "if part == '..':\n            current = current.parent\n            continue" in filewalk
assert 'if alias_literal in active_links:' in filewalk and 'active_links.add(alias_literal)' in filewalk
assert 'active_links.remove(part)' in filewalk
assert "pending = ([(False, item) for item in target_parts]\n                       + [(True, alias_literal)] + pending)" in filewalk
assert 'if remaining_components and not _env_stream_stat.S_ISDIR(info.st_mode):' in filewalk
assert 'if active_links or remaining_components != 0:' in filewalk
assert 'if alias_hops > _ENV_STREAM_MAX_FILE_ALIAS_HOPS:' in filewalk
assert '_env_stream_identity7(os.lstat(candidate)) != link_id' in filewalk and 'os.readlink(candidate) != link_text' in filewalk
assert 'target_identity=_env_stream_identity7(info)' in filewalk
assert '_env_stream_directory_identity(info)' in filewalk
tree=ast.parse(ct);values={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
assert ast.literal_eval(values['_ENV_STREAM_MAX_FILE_ALIAS_HOPS'])==64
assert ast.literal_eval(values['_ENV_STREAM_SOURCE_STATUS']).startswith('UNREADY')
sdk=Path('/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/param.h');sdkt=pin(sdk,'10d7a9553d341c5bc0b473444802920a7ec2e6222281eeaeb61b32dfff29c4b4')
assert '#define MAXSYMLINKS     32' in sdkt
author=read(C/'REPORT.json','b620498d907932d823019f1672e89175ed3d39d0179b1c8b5e8541e70a1419d4')
read(C/'actual_source_tool_terminal_returns.json','a8ed8061f32c6cb581985b55f0fe412f452b4ac8ad7300309326bc959de76960')
read(C/'manifest.json','a77bbcdc89ac0438b4216e15cf046a02223b3044ee1b4620e2cdb0c850b50c9c')
for r in author['source_identities']:
 assert identity(Path(r['path']))==r['path_before']==r['fd_before']==r['fd_after']==r['path_after']
pin(author['current_complete_graph_helper_actual_pin']['path'],author['current_complete_graph_helper_actual_pin']['sha256'])
conditions=[
 {'name':'unchanged21groups','required':'Replay the complete original21 meaningful helper groups against the new pinned canonical v14b module and fresh namespaces. Old839 control0 is not v14b operational qualification.'},
 {'name':'legal_short_relative_chain','required':'Inside the existing alias group, use two or three genuine relative file symlinks and prove independently full SHA/EOF, actual descriptor target, and separate literal full reads.'},
 {'name':'legitimate_repeated_link_after_dotdot','required':'Create directory link repeat.link->real/nested; open repeat.link/../nested/../../repeat.link/../input.bin where every intermediate directory exists, compare original OS file_digest, require two completed visits of the same link without a false cycle.'},
 {'name':'direct_and_mutual_cycle','required':'Self link and two-link mutual loop must be refused, retain original exception and empty memo/buffer/lock; no file bytes may be accepted.'},
 {'name':'growing_cycle','required':'A link whose target prepends its own link plus additional components must fail within the bounded active-chain logic, not recurse unboundedly.'},
 {'name':'directory_ancestor_is_file','required':'An ordinary file used before a remaining .. or leaf component must refuse under original Path.open semantics; directory-only3ID and FD7ID endpoint proof remain separate.'},
 {'name':'native_alias_preservation','required':'The require_regular=False native branch must retain the full original839 resolution behavior; do not subject native-only namespace chains to the new64 file-hop policy.'},
 {'name':'actual_terminal_and_performance','required':'Root alone must execute new controls under original120/512/64MiB/1child/1thread/0retry and full96/free8 history. Any timed comparison must be a distinct actual invocation; source cannot confer benefit or full86/native/AAA/ABA.'}
]
reasoning={
 'finite_work':'Each actual component decreases remaining_components. A link adds only finite readlink components and one noncomponent exit marker. Up to64 link expansions are permitted. Maximum literal/readlink component lengths are bounded by OS string/path limits; markers do not masquerade as remaining path components.',
 'cycle_and_repeat':'An absolute link path is active only while its target components are expanded. Re-entering it then is a genuine active expansion loop and refuses. Its exit marker removes it before original suffix components are walked, so a later legitimate revisit through .. is permitted. This is distinct from an ever-seen-links blacklist.',
 'dotdot':'Relative targets are prepended at the actual containing directory. Absolute targets reset current to /. .. operates on the resolved current directory after prior target expansion, preserving symlink-dir/../file semantics. The initial literal remains the memo and open key.',
 'FD_endpoint':'The actual original unbuffered Path open, complete readinto EOF bytecount, fstat before/after7ID, and path snapshot after are byteexact839. The manual endpoint7ID must equal the genuine opened file descriptor7ID. No decoded SHA or alias proof is borrowed across files or calls.',
 'file_hop_limit':'The local SDK declares MAXSYMLINKS32. The file-only64 manual limit is above the documented native actual-open limit; actual open remains authoritative and may refuse earlier. This static header observation does not claim a measured or portable runtime limit.',
 'native_aliases':'require_regular=False immediately delegates to a renamed whole-byte original839 snapshot; no new64 bound is imposed on native-only aliases.',
 'ordinary_directories':'Directory dev/ino/mode bindings preserve resolution identity without inventing immutable child timestamps; each actual symlink has full7ID and repeated readlink, and regular endpoint has7ID. Before/after equality checks remain original839.',
 'no_performance_credit':'Removing repeated strict resolution is a source design only. It requires new actual controls and a separately observed complete environment comparison; the839 old/new near-equal result is not evidence of v14b acceleration.'}
for r in pins:assert identity(Path(r['path']))==r['identity'] and hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
e={'schema':'AXMAT_V14B_MANUAL_ALIAS_SOURCE_INDEPENDENT_EVIDENCE_V1','pins':pins,'complete_inverse619':True,'complete_inverse839':True,'all_original33_nondigest_functions_byteexact':True,'only_old839_changed_function':changed,'native_branch_complete_name_inverse':True,'all_other_support_functions_byteexact839':True,'source_dataflow_reasoning':reasoning,'future_required_controls':conditions,'initial_readonly_display_error':{'chunk_id':'c63b5e','exit_code':1,'reason':'The two source proofs use before/after versus old/new region field names; an inspection guessed old/new for both. Final reader uses each actual schema; no helper execution or source changes.'}}
(D/'EVIDENCE.json').write_text(json.dumps(e,indent=2)+'\n')
report={'schema':'AXMAT_V14B_MANUAL_ALIAS_HELPER_INDEPENDENT_SOURCE_REVIEW_V1','status':'PASS_SOURCE_ONLY_UNREADY','helper_source_sha256':hashlib.sha256(H.read_bytes()).hexdigest(),'full_inverse_to_619_regions':1,'full_inverse_to_839_regions':3,'original_definition_count':34,'original33_nondigest_byteexact':True,'original839_FD_EOF_cleanup_owner_nativealias_semantics_byteexact':True,'file_manual_resolution_dataflow_reviewed':True,'native_only_alias_body_byteexact_after_function_name_restore':True,'file_hop_limit':64,'local_SDK_MAXSYMLINKS_macro':32,'source_blockers':[],'necessary_future_controls':conditions,'helper_loaded_or_called':False,'fixture_or_performance_executed':False,'project_written':False,'graph_or_mathematics_changed':False,'actual_control_qualification':False,'actual_speedup_proven':False,'full86_component_qualified':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'evidence_sha256':hashlib.sha256((D/'EVIDENCE.json').read_bytes()).hexdigest()}
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('H14b独立源码审查通过，仅SOURCE_ONLY/UNREADY。完整1区域逆619、3区域逆839；原33非digest定义与11其余辅助定义、实际FD7ID/完整EOF/作用域清理全部保持。native-only别名保留839完整body；文件路径采用有限active-link展开栈，已结束链接允许后续..合法再访，活动重复拒绝循环。\n本机SDK MAXSYMLINKS=32是静态头文件证据；文件walk上限64未取代真实open。必须新跑原21项并扩展循环/短链接/重复链接dotdot对照；未导入helper或执行fixture/perf，未证明提速、86/native/AAA/ABA。\n')
print(json.dumps({'status':report['status'],'REPORT_sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),'EVIDENCE_sha256':report['evidence_sha256'],'full_pins':len(pins)},indent=2))

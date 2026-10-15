"""Fresh standard-library SOURCE proof, never import/run candidate or helper."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT=Path(__file__).parent
G=ROOT/'BOUND_READY_SOURCE'
checks=[]
pins=[]
def check(name,value):
 if type(value)is not bool or not value:raise AssertionError(name)
 checks.append(dict(name=name,value=value))
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p,sha=None,identity=None):
 before=ident(p);check('regular private SOURCE '+str(p),stat.S_ISREG(before[2])and before[3]==1 and not p.is_symlink())
 raw=p.read_bytes();after=ident(p)
 check('complete SOURCE EOF SHA7ID beforeafter '+str(p),before==after and len(raw)==before[4])
 actual=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
 if sha is not None:check('exact fixed SOURCE SHA '+str(p),actual['sha256']==sha)
 if identity is not None:check('exact fixed SOURCE7ID '+str(p),actual['identity']==identity)
 pins.append(actual);return raw,actual
def defs(raw):
 s=raw.decode();return {n.name:ast.get_source_segment(s,n)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def inverse(raw,hunks,parent,label):
 text=raw.decode()
 for h in reversed(hunks):
  check(label+' unique exact inverse anchor',text.count(h['after'])==1)
  text=text.replace(h['after'],h['before'],1)
 check(label+' entire byteinverse',text.encode()==parent)
 check(label+' entire ASTinverse',ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
def assigned(raw):return {n.targets[0].id:n.value for n in ast.parse(raw).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
manifest_raw,mp=read(G/'generated_SOURCE_manifest.json','45124504c1a259a2b863245211dd3202060998fc5ec07dc1d6221ad353834ed2')
m=json.loads(manifest_raw);before_dir=ident(G)
check('complete generated Source8member + manifest inventory',m['member_count']==8 and sorted(x.name for x in G.iterdir())==sorted([e['relative']for e in m['members']]+['generated_SOURCE_manifest.json']))
raws={}
for e in m['members']:
 raw,p=read(G/e['relative'],e['sha256'],e['identity']);raws[e['relative']]=raw
 check('exact source manifest bytecount '+e['relative'],p['size_bytes']==e['size_bytes'])
runtime=raws['prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py'];host=raws['combined_prepare_host.py']
parent=raws['UNREADY_parent_exact_source.txt'];hparent=raws['genuine_PREP_parent_exact_source.txt']
proof=json.loads(raws['full_READY_runtime_and_genuine_PREP_SOURCE_inverse.json']);report=json.loads(raws['SOURCE_REPORT.json']);q=json.loads(raws['actual_joint_Q_exact_METADATA_copy.json'])
check('final runtime023abc fixed',hashlib.sha256(runtime).hexdigest()=='023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'and len(runtime)==180893)
check('final host776b fixed',hashlib.sha256(host).hexdigest()=='776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405'and len(host)==8685)
check('canonical original75969 complete parent',hashlib.sha256(parent).hexdigest()=='75969eafb9e1eead11e25d8838c6e3be13ea64babdc56ee222252a5e11bded62')
check('host originala9d4 complete parent',hashlib.sha256(hparent).hexdigest()=='a9d4a1eadae7f6f346138029ea4bbd5e9a5c26c0b5efbb8d256c08b06e757de1')
check('joint actualQexact complete19363 bytes',hashlib.sha256(raws['actual_joint_Q_exact_METADATA_copy.json']).hexdigest()=='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'and len(raws['actual_joint_Q_exact_METADATA_copy.json'])==19363)
check('exact4runtime and11host hunks',len(proof['runtime_ordered_hunks'])==4 and len(proof['host_ordered_hunks'])==11)
inverse(runtime,proof['runtime_ordered_hunks'],parent,'fullcanonical→75969')
inverse(host,proof['host_ordered_hunks'],hparent,'fullnormalhost→a9d4')
rd,pd=defs(runtime),defs(parent)
check('all70 complete definition bodies exact',len(rd)==70 and rd==pd)
ga,gp=assigned(runtime),assigned(parent)
changed=[k for k in gp if ast.dump(ga[k],include_attributes=False)!=ast.dump(gp[k],include_attributes=False)]
check('only required3 globals graph/Q/status changed',changed==['DRAFT_STATUS','INPUT_HELPERS','FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])
check('all other module/body Source restored by inverse',set(ga)==set(gp))
for name,node in rd.items():check('entire original function exact '+name,node==pd[name])
check('strict decode last-use function unchanged from reviewed75969',rd['strict_json_bytes']==pd['strict_json_bytes'])
for name in ('prepare_build','run_build','declaration_admission','environment','complete_input_phase','minimal_live_specs','input_modules','require_ready'):
 check('original fullscope stage/gate intact '+name,rd[name]==pd[name])
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('all six future businesspinsNone',all(ast.literal_eval(ga[n])is None for n in future))
check('actual helperQsha bound correctly',ast.literal_eval(ga['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])=='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2')
graph=dict(zip([k.value for k in ga['INPUT_HELPERS'].keys],ga['INPUT_HELPERS'].values))['graph']
check('actual dc01 helperSHA correct',graph.elts[1].value=='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')
rt=ast.parse(runtime);ht=ast.parse(host);hpt=ast.parse(hparent)
hcalls=[ast.unparse(n.func)for n in ast.walk(ht)if isinstance(n,ast.Call)];hpcalls=[ast.unparse(n.func)for n in ast.walk(hpt)if isinstance(n,ast.Call)]
check('all original host Call function order retained',hcalls==hpcalls)
check('all original host If/Raise/Assert counts retained',all(sum(isinstance(n,kind)for n in ast.walk(ht))==sum(isinstance(n,kind)for n in ast.walk(hpt))for kind in (ast.If,ast.Raise,ast.Assert)))
htxt=host.decode()
for token in ('full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','helper.guard_admission(full)','runner=full.OwnRSSSerialExecutor','resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30',"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]"):
 check('exact fullgenuine budget/dynamicSOURCES Source '+token,token in htxt)
check('exact genuine original history roots retained',"resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)"in htxt)
check('HOSTSOURCEOUTarchive joint2GiB original checks retained',htxt.count('support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))')==2)
check('newQ metadataonly futurebusiness flagsfalse',all(q[k]is False for k in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified')))
check('all binder2840 static Meta checks typedtrue',len(report['checks'])==2840 and all(type(c['value'])is bool and c['value']is True for c in report['checks']))
check('noART was read or current business executed',proof['current_ART_graph_numeric_or_history_read']is False and proof['business_API_guard_helper_called']is False and proof['installed']is False and report['ART_payload_read']is False)
for p in proof['all_SOURCE_Q_meta_references_full_EOF_SHA7ID_before_after']:
 path=Path(p['path']);check('only SOURCE/META actualbinder pin reread',not path.is_relative_to(Path('/Users/wen/spot/validation/artifacts')))
 _,current=read(path,p['sha256'],p['identity']);check('actual complete QandSource Meta pin unchanged',current==p)
for p in proof['ART_references_bound_by_actual_Q_only_never_read']:
 check('completeARTreference pins only bound byQ',Path(p['path']).is_relative_to(Path('/Users/wen/spot/validation/artifacts'))and set(p)=={'path','sha256','size_bytes','identity'}and len(p['identity'])==7 and all(type(v)is int for v in p['identity']))
for path in (ROOT/'generate_READY_runtime_and_PREP_SOURCE_ONLY.py',):
 raw,p=read(path);tree=ast.parse(raw)
 check('binder imports only standard library',all((n.module.split('.')[0]if isinstance(n,ast.ImportFrom)else a.name.split('.')[0])in {'argparse','ast','hashlib','json','math','os','pathlib','stat'}for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))for a in (n.names if isinstance(n,ast.Import)else [None])))
 check('binder no eval/exec/importlib/guard/helperload',not any(isinstance(n,ast.Call)and ast.unparse(n.func)in ('eval','exec','__import__','importlib.import_module','spec.loader.exec_module','helper.guard_admission')for n in ast.walk(tree)))
for p in list(pins):
 _,after=read(Path(p['path']),p['sha256'],p['identity']);check('all SOURCE/META finite beforeafter unchanged',after==p)
check('full generated namespace unchanged',ident(G)==before_dir and sorted(p.name for p in G.iterdir())==sorted([e['relative']for e in m['members']]+['generated_SOURCE_manifest.json']))
result=dict(schema='AXMAT_V21_ACTUAL_JOINT_Q_READY_FULL_RUNTIME_PREP_SOURCE_SELF_REVIEW_V1',status='SOURCE_PASS_UNINSTALLED_NOT_BUSINESS_QUALIFICATION',checks=checks,all_checks_typed_true=True,blockers=[],complete_runtime_4hunk_inverse_to75969=True,all70definition_bodies_byteexact=True,complete_genuine_host11hunk_inverse_toa9d4=True,complete_host_Call_If_Raise_Assert_sequence_contract_retained=True,all_actual_Q_SOURCE_META_full_EOF_SHA7ID_beforeafter_equal=True,ART_only_bound_by_actual_Q_not_read=True,all_SOURCE_member_inventory_retained=True,future_business_six_pins={n:None for n in future},complete_input_scope_original_math_physics_caps_and_five_stages_unchanged=True,generated_Source_manifest=mp,all_actual_input_pins=pins[:len(pins)//2],installed=False,helper_API_guard_business_executed=False,ART_graph_numeric_payload_read=False,source_level_RSS_failure_cause_or_future_PASS_claimed=False)
with(ROOT/'SELF_REVIEW.json').open('x')as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
print(json.dumps(dict(status=result['status'],checks=len(checks),blockers=[],report=str(ROOT/'SELF_REVIEW.json'),report_sha256=hashlib.sha256((ROOT/'SELF_REVIEW.json').read_bytes()).hexdigest(),all70defs=True,fourcanonical_elevenhost_inverse=True,API_executed=False,installed=False)))

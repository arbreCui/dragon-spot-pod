import ast,gzip,hashlib,json,os,re,stat,tarfile
from pathlib import Path
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_native_observation_BUILD5_AB_v7_sources'
E=B/'actual_complete_native_observation_BUILD5_AB_v7_receipts'
P=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
PEER=Path('/private/tmp/axmat_N7_complete_Source_independent_xxd8yrrc')
F=Path('/private/tmp/axmat_N7_actual_bound_Source_prelaunch_V2_im4o9o48')
checks=[];blockers=[];readpins={};source={}
def check(name,value):
 assert type(name)is str and name and name not in {v['check']for v in checks}and type(value)is bool
 checks.append(dict(check=name,passed=value))
 if not value:blockers.append(name)
def ident(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=ident(p);assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as stream:
  assert ident_from_stat(os.fstat(stream.fileno()))==i;sha=hashlib.file_digest(stream,'sha256').hexdigest();assert ident_from_stat(os.fstat(stream.fileno()))==i
 assert ident(p)==i;q=dict(path=str(p),sha256=sha,size_bytes=i[4],identity=i);assert str(p)not in readpins or readpins[str(p)]==q;readpins[str(p)]=q;return q
def ident_from_stat(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def strict(raw):
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def load(p):
 q=pin(p);d=strict(Path(p).read_bytes());assert pin(p)==q;return d
def text(p):
 q=pin(p);s=Path(p).read_text();assert pin(p)==q;source[str(p)]=s
 if Path(p).suffix=='.py':ast.parse(s,filename=str(p))
 return s
def tree(root):
 dirs={};files=[]
 for p in [root,*sorted(root.rglob('*'))]:
  i=ident(p);assert not stat.S_ISLNK(i[2])
  if stat.S_ISDIR(i[2]):dirs[str(p)]=i
  else:files.append(pin(p))
 return dict(files=files,directories=dirs)
def pinshape(p,tool_role=None):
 if not(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}):return False
 if not(type(p['path'])is str and Path(p['path']).is_absolute()and '..'not in Path(p['path']).parts and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int and v>=0 for v in p['identity'])and p['identity'][4]==p['size_bytes']and stat.S_ISREG(p['identity'][2])):return False
 return p['identity'][3]==1 if tool_role is None else p['path']==tools_expected[tool_role]and p['identity'][3]>=1
def lit(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.List):return[lit(v)for v in n.elts]
 if isinstance(n,ast.Tuple):return tuple(lit(v)for v in n.elts)
 if isinstance(n,ast.Dict):return{lit(k):lit(v)for k,v in zip(n.keys,n.values)}
 if isinstance(n,ast.BinOp):
  a,b=lit(n.left),lit(n.right)
  if isinstance(n.op,ast.Pow):return a**b
  if isinstance(n.op,ast.Mult):return a*b
 if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and not n.args:return{k.arg:lit(k.value)for k in n.keywords}
 raise ValueError('not Source literal')
def glob(s):
 v={}
 for n in ast.parse(s).body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:v[n.targets[0].id]=lit(n.value)
   except ValueError:pass
 return v
def defs(s):return{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
# Only the reviewer's actual closed Source/META pinset is accepted here; no future pins.
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--actual-facts',required=True);args=ap.parse_args()
facts_path=Path(args.actual_facts);assert facts_path.parent==F and facts_path.name=='ACTUAL_ROOT_CLOSED_N7_BOUND_SOURCE_FACTS.json'
facts=load(facts_path)
assert facts['schema']=='ACTUAL_ROOT_CLOSED_N7_BOUND_SOURCE_META_EXPECTATIONS_V1'and facts['source_only']is True and facts['closed_source_operations_only']is True
assert set(facts['bound_outputs'])=={'Root_bound_complete_observation_genuine_host.py','Root_bound_complete_observation_runtime.py','Root_actual_observation_SOURCE_binding.json','Root_actual_observation_bound_Source_full_inverse.json'}
assert set(facts['actual_tools'])=={'Root_actual_observation_Source_admission_tool_terminal_return.json','Root_actual_observation_REQUEST_tool_terminal_return.json','Root_actual_observation_SOURCE_binding_tool_terminal_return.json'}
for name,row in facts['actual_tools'].items():
 assert set(row)=={'actual_terminal_chunk','actual_saved_tool_receipt_pin'}and type(row['actual_terminal_chunk'])is str and row['actual_terminal_chunk']and pin(row['actual_saved_tool_receipt_pin']['path'])==row['actual_saved_tool_receipt_pin']and row['actual_saved_tool_receipt_pin']['path']==str(E/name)
assert pin(facts['actual_Root_request_pin']['path'])==facts['actual_Root_request_pin']and pin(facts['actual_Root_Source_admission_pin']['path'])==facts['actual_Root_Source_admission_pin']
for name,q in facts['bound_outputs'].items():assert pin(q['path'])==q and q['path']==str(D/name)
before=dict(D=tree(D),E=tree(E))
check('actual complete E five SourceMETA roles exact before', {str(Path(q['path']).relative_to(E))for q in before['E']['files']}=={'Root_actual_complete_native_observation_N7_Source_admission.json','Root_actual_observation_build_binding_request.json',*facts['actual_tools']}and set(before['E']['directories'])=={str(E)})
for tag,root in [('D',D),('E',E)]:
 for q in before[tag]['files']:
  p=Path(q['path']);check(tag+' actual Source META fullEOF '+str(p.relative_to(root)),pinshape(q)and pin(p)==q)
  if p.suffix=='.py':text(p);check(tag+' complete Python AST '+str(p.relative_to(root)),True)
  elif p.suffix=='.json':load(p);check(tag+' complete strict META '+str(p.relative_to(root)),True)
mf=load(P/'MANIFEST.json');mp=pin(P/'MANIFEST.json');check('actual author manifest full SHA',mp['sha256']=='178b885f37bf7c65cdd3375f9be29bd53c7b7e408aa61011894d25bb23cee928')
expected={r['relative_path']:r['fullpin']for r in mf['members']};check('actual complete author copied and only4 bound outputs',len(expected)==mf['member_count'] and {str(p.relative_to(D))for p in D.rglob('*')if p.is_file()}==set(expected)|{'MANIFEST.json','Root_bound_complete_observation_genuine_host.py','Root_bound_complete_observation_runtime.py','Root_actual_observation_SOURCE_binding.json','Root_actual_observation_bound_Source_full_inverse.json'})
check('actual bound D complete Source directory owner set',{str(Path(v).relative_to(D))for v in before['D']['directories']}=={str(Path(v).relative_to(P))for v in mf['complete_directory_identity']})
check('actual full counts derived from complete original owner manifest',len(before['D']['files'])==len(expected)+5 and len(before['D']['directories'])==len(mf['complete_directory_identity']))
check('retained author complete MF whole bytes',(pin(D/'MANIFEST.json')['sha256'],pin(D/'MANIFEST.json')['size_bytes'])==(mp['sha256'],mp['size_bytes']))
for rel,q in expected.items():
 check('actual author Source mother fullEOF '+rel,pin(Path(q['path']))==q)
 z=pin(D/rel);check('D retained whole original member '+rel,(z['sha256'],z['size_bytes'])==(q['sha256'],q['size_bytes']))
check('whole original author namespace unchanged',mf['complete_directory_identity']=={str(p):ident(p)for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}and {str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}==set(expected)|{'MANIFEST.json'})
inv=load(D/'Root_actual_observation_bound_Source_full_inverse.json');boundfacts={}
for role,original,derived,hunks,count in [('host','host_original_Source_pin','bound_host_pin','host_complete_inverse_hunks',11),('runtime','runtime_original_Source_pin','bound_runtime_pin','runtime_complete_inverse_hunks',1)]:
 op=inv[original];dp=inv[derived];check(role+' original and bound fullpins exact',pin(op['path'])==op and pin(dp['path'])==dp)
 old=text(op['path']);new=text(dp['path']);lines=new.splitlines(keepends=True)
 for number,h in enumerate(inv[hunks]):
  i=h['line']-1;check(role+' inverse actual original line '+str(number),type(h['line'])is int and lines[i]==h['new']);lines[i]=h['old']
 restored=''.join(lines);check(role+' entire byte and AST inverse motherSource',len(inv[hunks])==count and restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
 od,nd=defs(old),defs(new);check(role+' all complete defs exactly byte AST unchanged',set(od)==set(nd)and all(od[k]==nd[k]and ast.dump(ast.parse(od[k]),include_attributes=False)==ast.dump(ast.parse(nd[k]),include_attributes=False)for k in od))
 for k in od:check(role+' entire preserved definition '+k,od[k]==nd[k])
 boundfacts[role]=dict(actual_original_Source_pin=op,actual_bound_Source_pin=dp,actual_full_inverse_hunk_count=count,all_original_function_class_Source_bytes_preserved=True,whole_byte_AST_inverse_verified=True)
host=text(inv['bound_host_pin']['path']);runtime=text(inv['bound_runtime_pin']['path']);hg,rg=glob(host),glob(runtime);rd=defs(runtime)
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
future=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
tools_expected={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
request=load(E/'Root_actual_observation_build_binding_request.json');request_pin=pin(E/'Root_actual_observation_build_binding_request.json');binding=load(D/'Root_actual_observation_SOURCE_binding.json');binding_pin=pin(D/'Root_actual_observation_SOURCE_binding.json');ad=load(E/'Root_actual_complete_native_observation_N7_Source_admission.json');adpin=pin(E/'Root_actual_complete_native_observation_N7_Source_admission.json')
check('actual Root request exact fullpin from closed facts',request_pin==facts['actual_Root_request_pin'])
check('actual Root Sourcead exact fullpin from closed facts',adpin==facts['actual_Root_Source_admission_pin'])
check('actual4 Rootbound outputs exact fullpins from closed facts',{name:pin(D/name)for name in facts['bound_outputs']}==facts['bound_outputs'])
expected_binding=dict(request,schema='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_V1',actual_original_Root_request_pin=request_pin,bound_runtime_pin=inv['bound_runtime_pin'],actual_observer_native_execution=None)
check('binding whole META exact original request only declared additions',binding==expected_binding)
scope=load(D/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json');roles={k:pin(P/rel)for k,rel in scope['required_author_Source_roles'].items()}
peer=load(PEER/'REVIEW.json');peer_pin=pin(PEER/'REVIEW.json')
check('current Sourcepeer5213 exact common contract',peer_pin['sha256']=='356496012ce1f3a3d3d154a375321a905b31bb94f4c6f3c355f850a9ff57ba0b'and peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['all_checks_passed']is True and peer['blockers']==[]and peer['check_count']==len(peer['checks'])==5213 and len({c['check']for c in peer['checks']})==5213 and all(set(c)=={'check','passed'}and type(c['passed'])is bool and c['passed']is True for c in peer['checks']))
check('all14 actual fullSource ownerpins coupled everywhere',len(roles)==14 and roles==request['actual_author_Source_contract']==binding['actual_author_Source_contract']==ad['actual_author_Source_contract']==peer['actual_author_Source_contract'])
check('actual Root Sourcead strict scope',ad['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and ad['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and ad['source_only']is True and ad['scientific_qualification_created']is False and ad['independent_Source_review_pin']==peer_pin and ad['native_build_or_API_or_material_execution']is False)
for role,q in roles.items():check('author14 full Sourcepin '+role,pinshape(q)and pin(q['path'])==q)
tool_truth={}
for name,schema in [('Root_actual_observation_Source_admission_tool_terminal_return.json','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'),('Root_actual_observation_REQUEST_tool_terminal_return.json','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_REQUEST_TOOL_TERMINAL_RETURN_V1'),('Root_actual_observation_SOURCE_binding_tool_terminal_return.json','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BINDING_TOOL_TERMINAL_RETURN_V1')]:
 row=facts['actual_tools'][name];chunk=row['actual_terminal_chunk'];q=pin(E/name);v=load(E/name);t=v['terminal_tool_return'];out=strict(t['output']);check(name+' actual CLOSED strict0 no session',q==row['actual_saved_tool_receipt_pin']and v['schema']==schema and v['source_only']is True and v['closed']is True and v['observed_terminal']is True and v['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==chunk and v['scientific_qualification_created']is False)
 check(name+' actual operation SourceMETA only',v.get('native_or_API_or_material_executed',v.get('native_build_or_API_or_material_execution'))is False)
 if name=='Root_actual_observation_Source_admission_tool_terminal_return.json':check('actual Sourcead terminal stdout fullpin coupled',out['source_admission_pin']==adpin and out['status']=='ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'and out['actual_runtime_or_science_qualified']is False and v['actual_terminal_chunk']==chunk)
 elif name=='Root_actual_observation_REQUEST_tool_terminal_return.json':check('actual request terminal stdout fullpin coupled',out['actual_request_pin']==request_pin and out['status']=='ACTUAL_ROOT_OBSERVATION_REQUEST_META_ONLY_NO_BUILD_OR_MATERIAL_RUN'and out['native_build_or_API_or_material_execution']is False)
 else:check('actual binder terminal stdout four outputs coupled',out['bound_host_pin']==inv['bound_host_pin']and out['bound_runtime_pin']==inv['bound_runtime_pin']and out['binding_pin']==binding_pin and out['wholeSourcefullinverse_pin']==pin(D/'Root_actual_observation_bound_Source_full_inverse.json')and out['status']=='BOUND_COMPLETE_OBSERVATION_SOURCE_ONLY_NOT_EXECUTED')
 tool_truth[chunk]=dict(actual_saved_tool_receipt_pin=q,actual_terminal_chunk=chunk,actual_exit_code=t['exit_code'],closed=True,observed_terminal=True)
seed=load(D/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json');rows=request['original129_input_pins'];extras=request['additional_actual_evidence_input_pins'];allinputs=rows+extras+list(roles.values());tools=request['tool_pins'];tool_roles={q['path']:role for role,q in tools.items()}
check('all actual154 protected inputs complete ordered12911and14',len(rows)==129 and len(extras)==11 and len(allinputs)==154 and rows==seed['original129_input_pins']and len({q['path']for q in allinputs})==154)
check('actual six canonical tools exact positive nlink contracts',set(tools)==set(tools_expected)and rg['CANONICAL_OS_TOOL_PATHS']==tools_expected==hg['CANONICAL_OS_TOOL_PATHS'])
for i,q in enumerate(allinputs):check('actual protected input shape only '+str(i),pinshape(q,tool_roles.get(q['path'])))
protected={q['path']:q for q in rows+extras}
for key in ('independent_observation_Source_review_pin','independent_observation_Source_admission_pin','actual_Root_observation_Source_admission_tool_return_pin'):
 q=request[key];check('actual protected Source admission evidence '+key,protected.get(q['path'])==q and pin(q['path'])==q)
for role,q in tools.items():check('actual canonical tool included '+role,protected.get(q['path'])==q and pinshape(q,role))
check('request actual Source review and Sourcead pins exact',request['independent_observation_Source_review_pin']==peer_pin and request['independent_observation_Source_admission_pin']==adpin and request['actual_Root_observation_Source_admission_tool_return_pin']==pin(E/'Root_actual_observation_Source_admission_tool_terminal_return.json'))
layout=rg['SHARED_INPUT_LIBRARY_LAYOUT'];namespace=rg['REQUIRED_N7_FRESH_NAMESPACES'];ns=request['namespaces'];check('bound fixed v7 complete namespace identity',ns==namespace and ns['source']==str(D)and ns['receipts']==str(E)and len(set(ns.values()))==5)
check('bound host all actual paths andSHA coupled',hg['SOURCE_ARCHIVE']==str(D)and hg['RECEIPTS']==str(E)and hg['HOST']==ns['host']and hg['OUT']==ns['output']and hg['CONTROL']==ns['control']and hg['TARGET']==inv['bound_runtime_pin']['path']and hg['TARGET_SHA']==inv['bound_runtime_pin']['sha256']and hg['BINDING']==binding_pin['path']and hg['BINDING_SHA']==binding_pin['sha256']and hg['SOURCE_ADMISSION_SHA']==adpin['sha256'])
check('all HOC absent before allowed future runtime',all(not os.path.lexists(ns[k])for k in ('host','output','control')))
for label,g in [('host',hg),('runtime',rg),('request',request),('binding',binding),('admission',ad)]:
 actual=g['CAPS']if label in ('host','runtime')else g['original_caps'];check(label+' original nine strict integercaps',actual==caps and all(type(v)is int for v in actual.values()))
for label,g in [('runtime',rg['FUTURE']),('request',request),('binding',binding),('admission',ad),('inverse',inv)]:
 for k,v in future.items():check(label+' no future native/science fact '+k,g[k]is v)
check('actual request original five stages A B retained',request['build_stage_order']==['Ganlib','Utilib','Trivac','Dragon','Dragon_link']and request['state_order']==['A','B']and list(request['states'])==['A','B']and request['material_input_layout']==layout)
for state in ('A','B'):
 seeds=request['states'][state]['native_stage_inputs'];check(state+' all7 original seed roles exact ordered',len(seeds)==7 and [q['destination']for q in seeds]==layout['seed_destination_order'])
 for row in seeds:
  name=row['destination'];q=row['input_pin'];match=seed['states'][state].get(name)
  if match is None:match=dict(path=seed['libraries'][name]['path'],sha256=seed['libraries'][name]['generation_sha256'])
  check(state+' actual original full seed mapping '+name,set(row)=={'destination','input_pin'}and pinshape(q)and protected[q['path']]==q and all(q[k]==v for k,v in match.items()))
 check(state+' actual original deck fullpin',request['states'][state]['original_material_deck_pin']==seeds[0]['input_pin'])
for name in ('DLIB_ACTUAL','DLIB8R1_370'):check(name+' actual same original library pin A B',next(v['input_pin']for v in request['states']['A']['native_stage_inputs']if v['destination']==name)==next(v['input_pin']for v in request['states']['B']['native_stage_inputs']if v['destination']==name))
check('actual complete154 ordered runtime listSource',"inputs=b['original129_input_pins']+b['additional_actual_evidence_input_pins']+list(author.values())"in rd['run'])
check('original whole genuine module classes MRO and ownchild guard intact',"full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)"in rd['run']and "helper.guard_admission(full)"in rd['run']and "resources=JointHistoryResources(support.ART,history,8*2**30,96*2**30,production.ResourceFailure)"in rd['run'])
check('actual bound N7 joint_bytes complete original reviewed body byteexact',rd['joint_bytes']==defs(text(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py'))['joint_bytes'])
check('instrumented failure evidence class and wrapper lifecycle complete bound Source byteexact',all(rd[k]==defs(text(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py'))[k]for k in ('FailureOnlyMonitorEvidence','run'))and peer['N7_wrapper_both_original_callable_objects_single_delegate_bare_raise_and_finally_restore_Source_verified']is True and peer['N7_original_PS_lsof_full_argv_timeout8MiB_and_parentchain_scope_preserved']is True)
four_inverse=load(D/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json');four_inverse_facts=[]
for row in four_inverse['roles']:
 role=row['role_basename'];original=row['parent_original_fullpin'];derived=row['new_complete_Source_pin'];old=text(original['path']);new=text(D/role);check(role+' N7 original complete mother pin unchanged',pin(original['path'])==original);check(role+' N7 actual D Source whole original authored bytes',pin(D/role)['sha256']==derived['sha256']and pin(D/role)['size_bytes']==derived['size_bytes']and pin(derived['path'])==derived)
 lines=new.splitlines(keepends=True)
 for i,h in reversed(list(enumerate(row['hunks']))):
  check(role+' N7 full inverse hunk '+str(i),''.join(lines[h['new_start_line0']:h['new_end_line0']])==h['new_text']);lines[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
 restored=''.join(lines);check(role+' N7 whole byte AST inverse to exact N6 mother',restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
 four_inverse_facts.append(dict(role_basename=role,actual_original_Source_pin=original,actual_author_Source_pin=derived,actual_D_Source_pin=pin(D/role),whole_byte_AST_inverse_verified=restored==old))
check('N7 complete four changed Source roles reviewed to mother',len(four_inverse_facts)==4 and len({r['role_basename']for r in four_inverse_facts})==4)
future_interface=load(D/'N7_FAILURE_ONLY_MONITOR_FUTURE_ROOT_INTERFACE.UNREADY.json');check('original N7 interface all new runtime and instrumented controls unknown',all(v is None for k,v in future_interface.items()if k.startswith('actual_'))and future_interface['original_N6_lsof_raw']is None and future_interface['original_N6_failure_cause_unknown']is True)

check('guard initial resources before any HOC orcompile material',rd['run'].index('before=resources.check()')<rd['run'].index('host.mkdir()')<rd['run'].index('ep,build=compile_all')<rd['run'].index('for state in'))
check('entire D E frozen and exact joint2GiB resource scope',"tree(archive)==dfreeze and tree(receipts)==efreeze"in rd['run']and "joint['complete_joint_HOCDE_bytes']<2*2**30"in rd['run']and "tree(archive)==dfreeze and tree(receipts)==efreeze"in rd['run']and "for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))"in rd['run'])
check('all shared beforeafter EOF and no handle closure A beforeB retained',"shared_before=recheck_shared_libraries(shared,budget)"in rd['run']and "shared_after=recheck_shared_libraries(shared,budget)"in rd['run']and "require(shared_before==shared_after"in rd['run']and "Path(v).is_relative_to(Path(shared['shared_library_directory']))"in rd['run'])
# Read every original native Source member to EOF and verify CRC, never DB/material payload.
index=load(D/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');indexed={r['relative_path']:r['full_original_Source_pin']for r in index['members']};raw_source={}
with tarfile.open(D/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as archive:
 entries=archive.getmembers();check('actual complete1365 indexed Source archive no omissions',len(entries)==1365==len(indexed)and {m.name for m in entries}==set(indexed)and len({m.name for m in entries})==1365)
 for m in entries:
  check('nativeSource ordinary indexed '+m.name,m.isfile()and not Path(m.name).is_absolute()and '..'not in Path(m.name).parts)
  with archive.extractfile(m)as stream:raw=stream.read()
  q=indexed[m.name];check('nativeSource fullEOF '+m.name,len(raw)==q['size_bytes']and hashlib.sha256(raw).hexdigest()==q['sha256']);raw_source[m.name]=raw
with gzip.open(D/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','rb')as stream:
 while stream.read(2**20):pass
check('whole Source gzip CRC completed no material data read',True)
physics=load(D/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json');ph_hunks=0
for row in physics['derivations']:
 original=raw_source[row['original_archive_member']];derived=(D/row['derived_Source_member']).read_bytes();lines=derived.decode().splitlines(keepends=True);ph_hunks+=len(row['complete_insert_only_hunks'])
 for i,h in reversed(list(enumerate(row['complete_insert_only_hunks']))):
  check(row['derived_Source_member']+' insert-only physics actualhunk '+str(i),h['tag']=='insert'and h['old_start0']==h['old_end0']and h['old_full_lines']==[]and lines[h['new_start0']:h['new_end0']]==h['new_full_lines']);lines[h['new_start0']:h['new_end0']]=[]
 check(row['derived_Source_member']+' entire original physical byteinverse', ''.join(lines).encode()==original and hashlib.sha256(derived).hexdigest()==row['derived_sha256']and hashlib.sha256(original).hexdigest()==row['original_sha256'])
check('entire four physics14 insert-only retained',ph_hunks==14 and len(physics['derivations'])==4)
check('original full selected four recipes equal reviewed actual Source',rg['ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES']==peer['original_selected_recipes'])
for component in ('Ganlib','Utilib','Trivac','Dragon'):
 make=raw_source[component+'/src/Makefile'].decode();check(component+' original entire Makefile recipe flagar namespace retained',"ar rcs $@ $(OBJC) $(OBJ90) $(OBJ77) $(OBJF77)"in make and "ifneq (,$(filter $(ARCH),aarch64 arm64))\n  nbit ="in make)
# Root finite N7 Source-only admission is the whole N6 V3 Source with declared literal replacements.
writerfacts=[];wi=load('/private/tmp/spot_ROOT_complete_N7_Source_admission_V1_whole_Source_inverse_20261010.json');op=wi['mother_source_pin'];np=wi['new_source_pin'];old=text(op['path']);new=text(np['path'])
check('Root N7 admission entire original and derived Source exact pins',pin(op['path'])==op and pin(np['path'])==np)
forward=old
for i,h in enumerate(wi['complete_replacements']):
 check('Root N7 admission original literal exact count '+str(i),type(h['occurrences'])is int and h['occurrences']>0 and forward.count(h['before'])==h['occurrences']);forward=forward.replace(h['before'],h['after'])
check('Root N7 admission whole original Source forward transform matches entire derived',forward==new)
restored=new
for i,h in reversed(list(enumerate(wi['complete_replacements']))):
 check('Root N7 admission reverse literal exact count '+str(i),restored.count(h['after'])==h['occurrences']);restored=restored.replace(h['after'],h['before'])
check('Root N7 admission whole byte AST inverse',restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
od,nd=defs(old),defs(new);check('Root N7 admission all complete nonmain defs byte AST unchanged',set(od)==set(nd)and all(od[k]==nd[k]for k in od if k!='main'))
writerfacts.append(dict(actual_inverse_pin=pin('/private/tmp/spot_ROOT_complete_N7_Source_admission_V1_whole_Source_inverse_20261010.json'),actual_original_Source_pin=op,actual_derived_Source_pin=np,whole_byte_AST_inverse_verified=restored==old))
check('actual Rootad records exact N7 V1 complete Source pin',ad['Source_admission_writer_pin']==np)
check('Root absolute all Source dir keys only lossless interface',ad['author_declared_absolute_Source_directory_identity']==mf['complete_directory_identity']and ad['complete_Source_directory_identity']=={str(Path(k).relative_to(P)):v for k,v in mf['complete_directory_identity'].items()})
failed_interfaces=[]
after=dict(D=tree(D),E=tree(E));check('actual complete D E beforeafter frozen fullpins alldirs',before==after)
check('all HOC still absent after review',all(not os.path.lexists(ns[k])for k in ('host','output','control')))
for path,q in list(readpins.items()):check('final Source META immutable '+path,pin(path)==q)
report=dict(schema='INDEPENDENT_ACTUAL_N7_BOUND_SOURCE_META_PRELAUNCH_REVIEW_V1',status='PASS_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE'if not blockers else'BLOCKED_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=blockers==[],all_checks_typed_true=blockers==[],blockers=blockers,actual_namespace_pins=after,actual_namespace_pins_before=before,actual_namespace_pins_after=after,actual_author_Source_contract=roles,actual_four_Root_bound_output_pins={k:pin(D/k)for k in ('Root_bound_complete_observation_genuine_host.py','Root_bound_complete_observation_runtime.py','Root_actual_observation_SOURCE_binding.json','Root_actual_observation_bound_Source_full_inverse.json')},actual_Root_request_pin=request_pin,actual_Root_Source_admission_pin=adpin,actual_Root_Source_only_tool_truth=tool_truth,actual_full_source_inverse=boundfacts,actual_ordered_protected_input_pins=allinputs,actual_ordered_protected_input_count=154,actual_original129_input_count=129,actual_additional_input_count=11,actual_bound_author_role_count=14,protected_original_payload_and_native_tool_bodies_not_reread_by_this_review=True,actual_full_D_file_count=len(after['D']['files']),actual_full_D_directory_count=len(after['D']['directories']),actual_full_E_file_count=len(after['E']['files']),actual_full_E_directory_count=len(after['E']['directories']),actual_N7_complete_four_author_role_inverse_facts=four_inverse_facts,actual_N7_instrumented_Source_limits=peer['N7_diagnostic_scope_precise_limits'],actual_closed_Root_Source_facts_pin=pin(facts_path),actual_Root_Source_admission_writer_inverse_facts=writerfacts,actual_prior_Root_interface_failure_receipts=failed_interfaces,actual_complete_Read_Source_small_META_pins=list(readpins.values()),actual_complete_native_Source_archive_members_EOF=1365,actual_Source_gzip_CRC_verified=True,actual_physics14_whole_insert_only_inverse_verified=True,complete_shared_layout=layout,actual_shared_relative_names_lengths={r['derived'].split("'")[1]:len(r['derived'].split("'")[1])for r in layout['literal_replacements']},all_runtime_HOC_namespaces_absent_before_and_after_review=True,no_candidate_host_runtime_request_binder_postclose_guard_API_native_compile_material_executed=True,actual_N7_runtime_terminal=None,actual_N7_disk_RSS_result=None,actual_instrumented_guard_controls=None,actual_new_native_Source_object_archive_executable_qualification=None,scientific_qualification_created=False,project_D_E_or_parent_Source_modified=False,**future)
out=F/'REVIEW.json'
with out.open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps(dict(source_only=True,review_pin=pin(out),check_count=len(checks),all_checks_passed=blockers==[],blockers=blockers,actual_namespace_file_counts={k:len(v['files'])for k,v in after.items()},actual_namespace_directory_counts={k:len(v['directories'])for k,v in after.items()},actual_HOC_all_absent=True,candidate_guard_API_compile_native_or_material_executed=False),allow_nan=False))

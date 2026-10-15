"""Independent full Source/META review. No candidate imports/calls, native or material work."""
import ast,gzip,hashlib,json,os,re,stat,tarfile
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
N6=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
F=Path('/private/tmp/axmat_N7_complete_Source_independent_xxd8yrrc')
MF_SHA='178b885f37bf7c65cdd3375f9be29bd53c7b7e408aa61011894d25bb23cee928'
checks=[];blockers=[];pins={};source_bytes={};asts={};archive_bytes={};proofs={}
def check(label,passed):
 assert type(label) is str and label and label not in {c['check']for c in checks}
 assert type(passed) is bool
 checks.append(dict(check=label,passed=passed))
 if not passed:blockers.append(label)
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);i=identity(p);assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==i
 q=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i);pins[str(p)]=q;return q
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:assert k not in d;d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
def load(p):
 q=pin(p);raw=Path(p).read_bytes();assert pin(p)==q;return strict(raw)
def text(p):
 q=pin(p);raw=Path(p).read_bytes();assert pin(p)==q
 source_bytes[str(p)]=raw
 if Path(p).suffix=='.py':asts[str(p)]=ast.parse(raw,filename=str(p))
 return raw.decode('utf-8')
def checkpin(q,label):
 check(label+' exact four-field types',set(q)=={'path','sha256','size_bytes','identity'}and type(q['size_bytes'])is int and len(q['identity'])==7 and all(type(i)is int for i in q['identity'])and type(q['sha256'])is str and re.fullmatch('[0-9a-f]{64}',q['sha256'])is not None)
 check(label+' full EOF SHA7ID',pin(q['path'])==q)
def literal(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Dict):return {literal(k):literal(v)for k,v in zip(n.keys,n.values)}
 if isinstance(n,ast.List):return [literal(v)for v in n.elts]
 if isinstance(n,ast.Tuple):return tuple(literal(v)for v in n.elts)
 if isinstance(n,ast.UnaryOp)and isinstance(n.op,ast.USub):return -literal(n.operand)
 if isinstance(n,ast.BinOp):
  a,b=literal(n.left),literal(n.right)
  if isinstance(n.op,ast.Mult):return a*b
  if isinstance(n.op,ast.Pow):return a**b
  if isinstance(n.op,ast.Add):return a+b
 if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and not n.args:return {q.arg:literal(q.value)for q in n.keywords}
 raise ValueError('nonliteral Source expression')
def globals_of(s):
 d={}
 for n in ast.parse(s).body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:d[n.targets[0].id]=literal(n.value)
   except ValueError:pass
 return d
def defs(s):
 d={}
 for n in ast.parse(s).body:
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
   assert n.name not in d;d[n.name]=ast.get_source_segment(s,n)
 return d

assert F.exists() and list(F.iterdir())==[Path(__file__)]
mp=pin(P/'MANIFEST.json');m=load(P/'MANIFEST.json');members={r['relative_path']:r['fullpin']for r in m['members']}
check('N7 fixed exact actual manifest',mp['sha256']==MF_SHA and mp['size_bytes']==123400)
check('N7 full181 unique members and actual182 file set',m['source_only']is True and m['status']=='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW' and type(m['member_count'])is int and len(m['members'])==len(members)==m['member_count']==181 and {str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}==set(members)|{'MANIFEST.json'})
dirs={str(p):identity(p)for p in [P,*sorted(P.rglob('*'))]if p.is_dir()};check('N7 full24 directory7ID freeze',len(dirs)==24 and dirs==m['complete_directory_identity'])
for rel,q in members.items():
 check('N7 exact member path '+rel,Path(q['path'])==P/rel and not Path(rel).is_absolute()and '..'not in Path(rel).parts);checkpin(q,'N7 member '+rel)
 if Path(rel).suffix=='.py':text(P/rel);check('N7 complete AST '+rel,True)
 elif Path(rel).suffix=='.json':load(P/rel)
 elif Path(rel).suffix in('.f','.F','.f90','.h','.c','.c2m','.x2m','.txt'):text(P/rel)
ar=load(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json')
check('N7 author76 strict unique true onlySource',ar['source_only']is True and ar['all_checks_typed_true']is True and ar['blockers']==[] and type(ar['check_count'])is int and ar['check_count']==len(ar['checks'])==76 and len({q['check']for q in ar['checks']})==76 and all(set(q)=={'check','passed'}and type(q['passed'])is bool and q['passed']is True for q in ar['checks'])and ar['candidate_or_helper_or_guard_or_API_or_native_or_material_executed']is False)
author_tools={}
for name,chunk in [('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ab3a49'),('ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','145c82')]:
 r=load(Path(str(P)+'_seal_receipt')/name);t=r['terminal_tool_return'];out=strict(t['output']);author_tools[name]=dict(receipt_pin=pin(Path(str(P)+'_seal_receipt')/name),output=out)
 check('N7 author '+name+' actual strict CLOSED0',r['source_only']is True and r['closed']is True and r['observed_terminal']is True and r['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==r['actual_terminal_chunk']==chunk)
 check('N7 author '+name+' full actual MF/report coupling',out['manifest_pin']==mp and out['report_pin']==pin(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json')and out['member_count']==181 and out['directory_count']==24 and out['candidate_or_helper_or_guard_or_API_or_native_or_material_executed']is False)
truth=load(P/'ACTUAL_AUTHOR_N7_COMPLETE_SOURCE_TOOL_RETURNS.json');tools={r['actual_tool_return']['chunk_id']:r['actual_tool_return']for r in truth['actual_tool_returns']}
check('N7 actual first checker error848512 retained',type(tools['848512']['exit_code'])is int and tools['848512']['exit_code']==1 and 'session_id'not in tools['848512']and "KeyError: 'derive_shared_library_procedure'"in tools['848512']['output'])
check('N7 actual corrected author checkc1413e closedzero',type(tools['c1413e']['exit_code'])is int and tools['c1413e']['exit_code']==0 and 'session_id'not in tools['c1413e']and strict(tools['c1413e']['output'])['report_pin']==pin(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json'))
first=text(P/'AUTHOR_N7_FIRST_FAILED_SOURCE_CHECK.py');correct=text(P/'AUTHOR_EXECUTED_N7_COMPLETE_SOURCE_CHECK.py')
check('author Source checker correction only actual function name',first.replace('derive_shared_library_procedure','derive_original_procedure')==correct)
n6mp=pin(N6/'MANIFEST.json');n6m=load(N6/'MANIFEST.json');check('N7 complete N6 mother actualpin',n6mp==m['original_frozen_N6_manifest_pin']and n6mp['sha256']=='6b743dbb801efa359929b5c2bd409b337fdaf65d417a8e08debaeb917eba392f')
n6members={q['relative_path']:q['fullpin']for q in n6m['members']}
for rel,q in n6members.items():checkpin(q,'N6 whole mother member '+rel)
check('N6 mother153 full file set and22 dir freeze',{str(p.relative_to(N6))for p in N6.rglob('*')if p.is_file()}==set(n6members)|{'MANIFEST.json'}and {str(p):identity(p)for p in [N6,*sorted(N6.rglob('*'))]if p.is_dir()}==n6m['complete_directory_identity'])
n7inv=load(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json');changed={r['role_basename']for r in n7inv['roles']};four={'complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py'}
check('N7 exactly4 changed complete roles',len(n7inv['roles'])==len(changed)==4 and changed==four)
for rel,q in n6members.items():
 if rel not in changed:check('N7 all148 complete N6 member byteidentity '+rel,(pin(P/rel)['sha256'],pin(P/rel)['size_bytes'])==(q['sha256'],q['size_bytes']))
n7inverse_facts={};newroles={};n6roles={}
for row in n7inv['roles']:
 rel=row['role_basename'];checkpin(row['parent_original_fullpin'],'N7 inverse whole mother '+rel);checkpin(row['new_complete_Source_pin'],'N7 inverse whole new '+rel)
 original=text(N6/rel);new=text(P/rel);lines=new.splitlines(keepends=True)
 for number,h in reversed(list(enumerate(row['hunks']))):
  a,z=h['new_start_line0'],h['new_end_line0'];check('N7 '+rel+' whole inverse hunk '+str(number),''.join(lines[a:z])==h['new_text']);lines[a:z]=h['old_text'].splitlines(keepends=True)
 recovered=''.join(lines);check('N7 '+rel+' whole EOF byte AST inverse',recovered==original and ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
 check('N7 retained mother role full Source '+rel,text(P/'PREVIOUS_SEALED_N6_SOURCE_PROVENANCE'/rel)==original)
 n7inverse_facts[rel]=dict(parent_original_fullpin=row['parent_original_fullpin'],new_complete_Source_pin=row['new_complete_Source_pin'],whole_byte_and_AST_inverse=True,hunk_count=len(row['hunks']))
 od,nd=defs(original),defs(new);check('N7 '+rel+' all original definitions retained',set(od)<=set(nd))
 n6roles[rel]=original;newroles[rel]=new
 og,ng=globals_of(original),globals_of(new);check('N7 '+rel+' all9 original caps and future unknownfalse',og['CAPS']==ng['CAPS']and og['FUTURE']==ng['FUTURE'])
 for name in od:
  if name not in ({'joint_bytes','guarded','run','validate_request'}if rel=='complete_observation_BUILD5_AB_runtime.UNREADY.py'else {'main','verify_complete_shared_library_and_procedure_evidence'}):check('N7 '+rel+' complete original definition unchanged '+name,od[name]==nd[name])
N7runtime=newroles['complete_observation_BUILD5_AB_runtime.UNREADY.py'];N7tree=ast.parse(N7runtime);N7nodes={n.name:n for n in N7tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};N6runtime=n6roles['complete_observation_BUILD5_AB_runtime.UNREADY.py'];N6nodes={n.name:n for n in ast.parse(N6runtime).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def dump(n):return ast.dump(n,include_attributes=False)
def module_dump(rows):return dump(ast.Module(body=rows,type_ignores=[]))
def unnamespace(s):return s.replace('REQUIRED_N7_FRESH_NAMESPACES','REQUIRED_N6_FRESH_NAMESPACES').replace('-AB-v7-','-AB-v6-').replace('_AB_v7_','_AB_v6_').replace('fixed v7','fixed v6')
for rel in changed-{'complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py'}:check('N7 '+rel+' only finite namespace Source change',unnamespace(newroles[rel])==n6roles[rel])
check('N7 runtime validate_request only actual fresh namespace change',dump({n.name:n for n in ast.parse(unnamespace(N7runtime)).body if isinstance(n,ast.FunctionDef)}['validate_request'])==dump(N6nodes['validate_request']))
jn=N7nodes['joint_bytes'];jo=N6nodes['joint_bytes'];check('N7 entire joint original body and return preserved AST',len(jn.body)==2 and isinstance(jn.body[1],ast.Try)and module_dump(jn.body[1].body[:-2]+[jn.body[1].body[-1]])==module_dump(jo.body))
check('N7 joint failure bare reraises original',jn.body[1].handlers[0].body[-1].exc is None and isinstance(jn.body[1].handlers[0].body[-1],ast.Raise))
gn=N7nodes['guarded'];check('N7 entire guarded original complete body preserved AST',isinstance(gn.body[-1],ast.Try)and module_dump(gn.body[-1].body)==module_dump(N6nodes['guarded'].body))
mon=N7nodes['FailureOnlyMonitorEvidence'];methods={n.name:n for n in mon.body if isinstance(n,ast.FunctionDef)};install=methods['install_bounded_wrappers'];wrappers={n.name:n for n in install.body if isinstance(n,ast.FunctionDef)}
check('N7 only2 bounded objects wrapped',set(wrappers)=={'terminate_group','finish_liveness_watchdog'})
for name,args in [('terminate_group',['process']),('finish_liveness_watchdog',['write_fd','watchdog'])]:
 w=wrappers[name];tr=next(n for n in w.body if isinstance(n,ast.Try));delegate=tr.body[0].value
 check('N7 '+name+' single unchanged captured original delegate args',isinstance(tr.body[0],ast.Return)and isinstance(delegate,ast.Call)and isinstance(delegate.func,ast.Name)and delegate.func.id=='original_'+name and [ast.unparse(n)for n in delegate.args]==args and not delegate.keywords and len([n for n in ast.walk(w)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='original_'+name])==1)
 check('N7 '+name+' cleanup exception bare raise',isinstance(tr.handlers[0].body[-1],ast.Raise)and tr.handlers[0].body[-1].exc is None)
check('N7 wrappers do not poll wait kill reap signal or bypass original',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in {'poll','wait','kill','terminate','send_signal','killpg','setsid'}for n in ast.walk(install)))
it=ast.get_source_segment(N7runtime,install);restore=ast.get_source_segment(N7runtime,methods['restore_bounded_objects']);run=ast.get_source_segment(N7runtime,N7nodes['run'])
check('N7 captures original2 callableobjects before wrapper assignment',it.index('original_terminate_group=bounded.terminate_group')<it.index('bounded.terminate_group=terminate_group')and it.index('original_finish_liveness_watchdog=bounded.finish_liveness_watchdog')<it.index('bounded.finish_liveness_watchdog=finish_liveness_watchdog'))
check('N7 original2 callableobjects restored in run finally',all(x in restore for x in ['bounded.terminate_group=original_terminate_group','bounded.finish_liveness_watchdog=original_finish_liveness_watchdog'])and isinstance(N7nodes['run'].body[-1],ast.Try)and ast.unparse(N7nodes['run'].body[-1].finalbody[0])=='monitor.restore_bounded_objects()')
check('N7 no success record append or failure PS call',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in {'record','failure_ps'}for n in ast.walk(methods['remember_successful_scan'])))
check('N7 one successful raw observation overwritten only memory',"self.latest_original_scan=dict("in ast.get_source_segment(N7runtime,methods['remember_successful_scan'])and 'not_new_liveness_at_cleanup_time=True'in N7runtime)
check('N7 originalactive and cleanup two exceptions separate full trace',all(x in N7runtime for x in ['original_active_exception','actual_cleanup_exception',"complete_traceback=''.join(traceback.format_exception"]))
check('N7 original failure record before extra PS',N7runtime.index("self.record(dict(event='original_joint_bytes_failure'")<N7runtime.index("self.failure_ps('after_original_failed_joint_scan')"))
check('N7 original raw text not striptruncate and timeout bytes explicit partial',all(x in N7runtime for x in ['no_strip_or_stream_truncation=True','original_text_mode_unchanged=True','actual_stdout=monitor_stream(lsof_stdout)','actual_stderr=monitor_stream(lsof_stderr)',"original_type='bytes'",'streams_complete=observed is not None','streams_complete=False']))
check('N7 additional PS evidence only min2 actual whole/stage remaining',all(x in ast.get_source_segment(N7runtime,methods['failure_ps'])for x in ["argv=[self.tools['ps']['path'],'-axo','pid=,ppid=,pgid=']",'timeout=min(2,remaining)','original_selection_not_changed=True','used_to_accept_original_failure=False',"require(remaining>0,'no additional diagnostic query after original whole/stage deadline')"]))
check('N7 strict original PS/lsof args timeouts8MiB from complete AST inverse',all(x in ast.get_source_segment(N7runtime,jn)for x in ["ps_argv=[ps_tool,'-axo','pid=,ppid=']",'communicate(timeout=2)',"subprocess.run([lsof_tool,'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)","require(observed.returncode==0,'full live own process file scan required')","require(len(observed.stdout)<8*2**20,'finite complete lsof output; never truncated')",'selected.discard(ps_diagnostic_pid)']))
check('N7 disk accounting allHOCDE unchanged joint/history/free and frozenD/E',all(x in ast.get_source_segment(N7runtime,methods['disk_account'])for x in ["tree(self.roots[3])==self.dfreeze and tree(self.roots[4])==self.efreeze","total+previous_unlinked+increment<CAPS['joint_archive_bytes']","history['artifact_bytes']+external+previous_unlinked+increment<=CAPS['history_bytes']","history['disk_free_bytes']-increment>=CAPS['free_floor_bytes']",'current_open_unlinked_verified=False','failed_scan_never_replaced_by_this_account=True']))
check('N7 original basehistory check avoids recursive new failed scan',"history=self.base_history_check(self.resources)"in N7runtime and 'resource.DynamicHistoryResources.check,dfreeze,efreeze'in run)
check('N7 failurejournal H-only fullsmallMETA noalias fsync counted',all(x in ast.get_source_segment(N7runtime,methods['record'])for x in ["target=folder/'ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'",'s.st_nlink==1','self.disk_account(len(raw))',"with target.open('ab')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())",'self.recording_errors.append']))
check('N7 complete failed result originalbytes budget no truncated surrogate',all(x in ast.get_source_segment(N7runtime,methods['write_failure_result'])for x in ['json.dumps(value,indent=2,allow_nan=False)','self.disk_account(len(raw))','write_new(path,value)','complete_original_failure_result_retained_in_memory_only=True']))
check('N7 original genuine classes MRO Source guardcaps retained',all(x in run for x in ['full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)','helper.guard_admission(full)','type(runner)is full.OwnRSSSerialExecutor',"fullpin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA"]))
post=newroles['Root_observation_postclose_META_writer.UNREADY.py']
check('N7 success postclose rejects any failure recording hidden partial',all(x in post for x in ["diagnostic['failure_event_count']==0","diagnostic['journal_pin']is None","diagnostic['additional_recording_errors']==[]","diagnostic['unpersisted_complete_events']==[]"]))
check('N7 legacy watchdogcleanup flag never new actual cleanup proof',"original_watchdog_cleanup_flag_not_actual_cleanup_proof=True"in N7runtime and "diagnostic['original_watchdog_cleanup_flag_not_actual_cleanup_proof']is True"in post)
interface=load(P/'N7_FAILURE_ONLY_MONITOR_FUTURE_ROOT_INTERFACE.UNREADY.json');ng=globals_of(N7runtime)
for rel,s in newroles.items():check('N7 '+rel+' fixednew7 namespace and futureNonefalse',globals_of(s)['REQUIRED_N7_FRESH_NAMESPACES']==interface['namespaces']and globals_of(s)['CAPS']==globals_of(N6runtime)['CAPS']and globals_of(s)['FUTURE']==globals_of(N6runtime)['FUTURE'])
check('N7 futurebusiness unknown None/source false',all(v is None for k,v in interface.items()if k.startswith('actual_'))and interface['original_N6_lsof_raw']is None and interface['original_N6_failure_cause_unknown']is True)
prov=load(P/'N7_ACTUAL_N6_FAILED_MONITOR_AND_SOURCE_PROVENANCE.json')
for row in prov['actual_original_files']:
 checkpin(row['actual_original_fullpin'],'N7 original actual N6 small SourceMETA '+Path(row['actual_original_fullpin']['path']).name);checkpin(row['complete_byte_copy_fullpin'],'N7 retained N6 actual SourceMETA '+Path(row['complete_byte_copy_fullpin']['path']).name)
 check('N7 actual N6 SourceMETA full bytecopy '+Path(row['actual_original_fullpin']['path']).name,(row['actual_original_fullpin']['sha256'],row['actual_original_fullpin']['size_bytes'])==(row['complete_byte_copy_fullpin']['sha256'],row['complete_byte_copy_fullpin']['size_bytes']))
check('N7 historical original N6 raw notrecovered',prov['original_N6_failed_lsof_raw']is None)
# Re-read full original ancestors and all native Source archive/physics proofs.
new_m=m;m=n6m
# Every complete N5 Source/META member is genuinely reread, not reduced to a hunk list.
parent_pin=m['original_frozen_N5_manifest_pin'];checkpin(parent_pin,'complete N5 parent manifest');N5=Path(parent_pin['path']).parent;pm=load(parent_pin['path']);p_members={q['relative_path']:q['fullpin']for q in pm['members']}
inv=load(P/'COMPLETE_N6_FOUR_ROLE_WHOLE_BYTE_AST_SOURCE_INVERSE.json');changed=set(inv['roles']);check('all and only four changed N6 roles',changed=={'complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py'})
for rel,q in p_members.items():
 checkpin(q,'N5 mother member '+rel)
 if Path(rel).suffix=='.py':text(N5/rel)
 if rel not in changed:check('complete retained unchanged N5 member '+rel,(pin(P/rel)['sha256'],pin(P/rel)['size_bytes'])==(q['sha256'],q['size_bytes']))
restored_roles={};whole_inverse_facts={}
for rel,row in inv['roles'].items():
 checkpin(row['original_Source_pin'],'N6 inverse mother '+rel);checkpin(row['derived_Source_pin'],'N6 inverse derived '+rel)
 original=text(row['original_Source_pin']['path']);derived=text(row['derived_Source_pin']['path']);restored=derived.splitlines(keepends=True)
 for number,h in reversed(list(enumerate(row['whole_byte_inverse_hunks']))):
  a,b=h['derived_start_line_0'],h['derived_end_line_0'];check(rel+' whole inverse exact hunk '+str(number),''.join(restored[a:b])==h['derived_complete_hunk']);restored[a:b]=h['original_complete_hunk'].splitlines(keepends=True)
 restored=''.join(restored);od,dd=defs(original),defs(derived);proof=inv['definition_proof'][rel]
 check(rel+' whole byte inverse EOF',restored==original and hashlib.sha256(restored.encode()).hexdigest()==row['whole_restored_original_sha256'])
 check(rel+' whole original AST exact',ast.dump(ast.parse(restored),include_attributes=False)==row['whole_original_AST_dump'])
 check(rel+' whole derived AST exact',ast.dump(ast.parse(derived),include_attributes=False)==row['whole_derived_AST_dump'])
 check(rel+' original complete defs retained',set(od)<=set(dd)and set(dd)-set(od)==set(proof['added_definition_names']))
 for name in proof['unchanged_original_definition_names']:
  check(rel+' unchanged whole definition '+name,od[name]==dd[name]and ast.dump(ast.parse(od[name]),include_attributes=False)==ast.dump(ast.parse(dd[name]),include_attributes=False))
 actual_changed={n for n in od if od[n]!=dd[n]};check(rel+' complete definition difference scope',actual_changed==set(proof['changed_original_definition_names']))
 restored_roles[rel]=original;whole_inverse_facts[rel]=dict(original_complete_Source_pin=row['original_Source_pin'],derived_complete_Source_pin=row['derived_Source_pin'],whole_original_source_byte_size=len(original.encode()),whole_derived_source_byte_size=len(derived.encode()),all_original_definition_names=list(od),actual_changed_definition_names=sorted(actual_changed),added_definition_names=list(proof['added_definition_names']),full_byte_and_AST_inverse_verified=True)
runtime=text(N6/'complete_observation_BUILD5_AB_runtime.UNREADY.py');rtdefs=defs(runtime);rglobals=globals_of(runtime)
host=text(P/'complete_observation_genuine_host.UNREADY.py');check('entire genuine host equals complete mother Source',host==text(N5/'complete_observation_genuine_host.UNREADY.py'))
# N5's full actual closed PS fix and untouched original lsof tail remain complete.
n5inv=load(P/'COMPLETE_N5_SINGLE_JOINT_BYTES_SOURCE_INVERSE.json');n4=Path(n5inv['original_runtime_pin']['path']);checkpin(n5inv['original_runtime_pin'],'complete N4 runtime mother');n4text=text(n4);n5text=restored_roles['complete_observation_BUILD5_AB_runtime.UNREADY.py'];restored=n5text
for x in reversed(n5inv['exact_finite_transforms']):
 check('N5 entire original finite transform '+x['label'],restored.count(x['new'])==1);restored=restored.replace(x['new'],x['old'],1)
check('N5 full runtime byte and AST inverse',restored==n4text and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(n4text),include_attributes=False))
check('N6 mother complete joint_bytes equals real N5 Source',rtdefs['joint_bytes']==defs(n5text)['joint_bytes'])
check('N5 excludes only actual reaped diagnostic PS PID',"selected.discard(ps_diagnostic_pid)"in rtdefs['joint_bytes']and "ps_returncode==0"in rtdefs['joint_bytes']and "observed.returncode==0"in rtdefs['joint_bytes'])
# Complete five N4->N3 role Source inverses, then the full original 12-hunk genuine host inverse.
n4inv=load(P/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json');n3_sources={}
for rel,hunks in n4inv['five_role_complete_inverse_hunks'].items():
 pf=n4inv['five_role_full_definition_proof'][rel];checkpin(pf['original_pin'],'complete N3 mother '+rel);checkpin(pf['derived_pin'],'complete N4 mother '+rel)
 old=text(pf['original_pin']['path']);new=text(pf['derived_pin']['path']);lines=new.splitlines(keepends=True)
 for number,h in reversed(list(enumerate(hunks))):
  a,b=h['derived_start0'],h['derived_stop0'];check('N4 '+rel+' complete inverse hunk '+str(number),''.join(lines[a:b])==h['derived']);lines[a:b]=h['original'].splitlines(keepends=True)
 restored=''.join(lines);check('N4 '+rel+' full byte AST inverse',restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False));n3_sources[rel]=old
hinv=load(P/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json');restored=n3_sources['complete_observation_genuine_host.UNREADY.py']
for number,h in reversed(list(enumerate(hinv['complete_full_inverse_hunks']))):
 new=''.join(h['new_full_lines']);old=''.join(h['old_full_lines']);check('genuine original host unique complete hunk '+str(number),restored.count(new)==1);restored=restored.replace(new,old,1)
original_host=text(P/'PARENT_SOURCE/Root_bound_complete_native_genuine_host.py');check('original genuine host whole12 byte AST inverse',len(hinv['complete_full_inverse_hunks'])==12 and restored==original_host and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original_host),include_attributes=False))
# Whole original compile Source archive: every native Source member reaches EOF, then gzip CRC/trailer reaches EOF too.
index=load(P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');indexed={q['relative_path']:q['full_original_Source_pin']for q in index['members']};archive_pin=pin(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz')
with tarfile.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as archive:
 info=archive.getmembers();check('exact1365 complete original Source archive entries',len(info)==len(indexed)==1365 and len({q.name for q in info})==1365 and {q.name for q in info}==set(indexed))
 for member in info:
  check('native archive regular noalias '+member.name,member.isfile()and not Path(member.name).is_absolute()and '..'not in Path(member.name).parts)
  with archive.extractfile(member)as stream:raw=stream.read()
  expected=indexed[member.name];check('native archive complete EOF '+member.name,len(raw)==expected['size_bytes']and hashlib.sha256(raw).hexdigest()==expected['sha256']);archive_bytes[member.name]=raw
with gzip.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','rb')as stream:
 while stream.read(2**20):pass
check('original Source gzip complete EOF CRC frozen',pin(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz')==archive_pin)
physical=load(P/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json');physical_facts={};total_insert_hunks=0
for row in physical['derivations']:
 original=archive_bytes[row['original_archive_member']];derived=(P/row['derived_Source_member']).read_bytes();lines=derived.decode().splitlines(keepends=True);total_insert_hunks+=len(row['complete_insert_only_hunks'])
 for number,h in reversed(list(enumerate(row['complete_insert_only_hunks']))):
  check(row['derived_Source_member']+' actual insert-only hunk '+str(number),h['tag']=='insert'and h['old_start0']==h['old_end0']and h['old_full_lines']==[]and lines[h['new_start0']:h['new_end0']]==h['new_full_lines']);lines[h['new_start0']:h['new_end0']]=[]
 restored=''.join(lines).encode();check(row['derived_Source_member']+' full original physics bytes inverse',restored==original and hashlib.sha256(original).hexdigest()==row['original_sha256']and hashlib.sha256(derived).hexdigest()==row['derived_sha256']);physical_facts[row['original_archive_member']]=dict(original_sha256=hashlib.sha256(original).hexdigest(),derived_sha256=hashlib.sha256(derived).hexdigest(),all_original_physical_bytes_recovered=True,observer_insert_hunks=len(row['complete_insert_only_hunks']))
check('all original physics14 insert-only hunks complete',total_insert_hunks==14 and len(physical_facts)==4)
provenance=load(P/'FULL_NECESSARY_PARENT_SOURCE_PROVENANCE.json')
for row in provenance['parents']:
 checkpin(row['full_original_Source_pin'],'necessary original full Source '+row['role']);q=pin(P/row['retained_copy']);check('necessary Source complete byte copy '+row['role'],q['sha256']==row['full_original_Source_pin']['sha256']and q['size_bytes']==row['full_original_Source_pin']['size_bytes'])
 if Path(row['full_original_Source_pin']['path']).suffix=='.py':text(row['full_original_Source_pin']['path'])
# Original Makefiles were read complete. These selected Darwin/arm64 values are independently derived from their exact branches.
expected_recipes={
 'Ganlib':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=['-DLinux','-DUnix'],F90='fortran',FFLAGS=['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=[],PREPRO='cpp',FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Ganlib/lib/Darwin_arm64/modules',module_copy=True),
 'Utilib':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=[],F90='fortran',FFLAGS=['-fPIC','-Wall','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=[],PREPRO=None,FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Utilib/lib/Darwin_arm64/modules',module_copy=True),
 'Trivac':dict(C=None,CFLAGS=[],FLAGS=[],F90='fortran',FFLAGS=['-fPIC','-ffpe-summary=none'],FFLAG77=['-fPIC','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=['-I../../Ganlib/lib/Darwin_arm64/modules/'],PREPRO=None,FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module=None,module_copy=False),
 'Dragon':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=['-DLinux','-DUnix'],F90='fortran',FFLAGS=['-fPIC','-Wall','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=['-I../../Ganlib/lib/Darwin_arm64/modules/'],PREPRO='cpp',FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Dragon/lib/Darwin_arm64/modules',module_copy=True)}
check('complete original selected recipes all four variables',rglobals['ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES']==expected_recipes)
for component,recipe in expected_recipes.items():
 makefile=archive_bytes[component+'/src/Makefile'].decode();check(component+' completeMakefile selected arm64 blank nbit',"ifneq (,$(filter $(ARCH),aarch64 arm64))\n  nbit ="in makefile and 'ifeq ($(OS),Darwin)'in makefile)
 check(component+' original Darwin ar suffix group order',"ar rcs $@ $(OBJC) $(OBJ90) $(OBJ77) $(OBJF77)"in makefile)
 for flag,actual in recipe.items():check(component+' independently selected recipe '+flag,rglobals['ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES'][component][flag]==actual)
check('whole compile_all Source byteexact N5 mother',rtdefs['compile_all']==defs(n5text)['compile_all'])
check('all five library link phases unchanged ordered',"for component in ('Ganlib','Utilib','Trivac','Dragon')"in rtdefs['compile_all']and "('Dragon','Trivac','Utilib','Ganlib')"in rtdefs['compile_all']and "stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link']"in rtdefs['compile_all'])
# All four active Source roles carry the same fixed N6 layout/namespaces and original caps/future boundaries.
expected_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
future=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
contract=load(P/'N6_FUTURE_ROOT_NAMESPACE_AND_SHARED_LIBRARY_CONTRACT.UNREADY.json');layout=contract['material_input_layout'];namespaces=contract['required_new_v6_namespaces'];role_sources={rel:text(N6/rel)for rel in changed}
for rel,s in role_sources.items():
 g=globals_of(s);check(rel+' all9 original integercaps',g['CAPS']==expected_caps and all(type(v)is int for v in g['CAPS'].values()));check(rel+' all future qualifications unknownfalse',g['FUTURE']==future and all(g['FUTURE'][k]is v for k,v in future.items()));check(rel+' exactshared layout',g['SHARED_INPUT_LIBRARY_LAYOUT']==layout);check(rel+' fixed new6 namespaces only',g['REQUIRED_N6_FRESH_NAMESPACES']==namespaces)
check('genuine host all9 original caps exact',globals_of(host)['CAPS']==expected_caps)
check('new original129 still unchanged trueSource',"b['original129_input_pins']==seed_contract['original129_input_pins']"in rtdefs['validate_request']and "len(rows)==129"in rtdefs['validate_request'])
check('exact A B and seven seed roles no omission',layout['state_order']==['A','B']and layout['seed_destination_order']==['material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'])
shared_copy_calls=[ast.unparse(n.func)for n in ast.walk(ast.parse(rtdefs['prepare_shared_libraries']))if isinstance(n,ast.Call)]
check('shared original libs each copied once no alias calls fullpin',"for name,p in originals.items():"in rtdefs['prepare_shared_libraries']and "dest.open('xb')"in rtdefs['prepare_shared_libraries']and "actual['sha256']==p['sha256']"in rtdefs['prepare_shared_libraries']and "actual['size_bytes']==p['size_bytes']"in rtdefs['prepare_shared_libraries']and not any(c.split('.')[-1]in('symlink','link','symlink_to','hardlink_to')for c in shared_copy_calls))
check('A B same original library pins sourcechecked',"previous is None or previous==row['input_pin']"in rtdefs['original_shared_libraries'])
check('all streams scope close before state closure',"with Path(p['path']).open('rb')as src"in rtdefs['copy_state_seeds']and 'with'in rtdefs['prepare_shared_libraries'])
check('libraries originalandshared full EOF before after both',"shared_before=recheck_shared_libraries(shared,budget)"in rtdefs['run']and "shared_after=recheck_shared_libraries(shared,budget)"in rtdefs['run']and "require(shared_before==shared_after"in rtdefs['run'])
check('A closes state andshared handles before B',"for state in('A','B')"in rtdefs['run']and "Path(v).is_relative_to(Path(shared['shared_library_directory']))"in rtdefs['run']and "'actual_no_open_state_handles_observation'"in rtdefs['run'])
postdefs=defs(role_sources['Root_observation_postclose_META_writer.UNREADY.py']);verify=postdefs['verify_complete_shared_library_and_procedure_evidence']
check('postclose full originalshared EOF four observations',"for state in ('A','B')"in verify and "before_actual_material_stage=expected,after_actual_material_stage=expected"in verify and "check(originals[name]);check(copies[name])"in verify)
check('postclose exact7 mappings plus retained original c2m',"len(mapping)==7"in verify and "retained_original_procedure_pin"in verify and "row['actual_material_seed_copy_pins']==[item['actual_consumed_pin']for item in mapping]+[mapping[1]['retained_original_procedure_pin']]"in verify)
check('postclose complete c2m ASCII byte inverse Source contract',"derived==expected_derived"in verify and "inverse==original"in verify and "retained==original"in verify and "ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal"in verify)
smallpins=load(P/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE/ACTUAL_ORIGINAL_SMALL_DECK_AND_PROCEDURE_SOURCE_PINS.json');procedure_facts={}
for state in ('A','B'):
 for name,q in smallpins[state].items():
  checkpin(q,state+' actual original small Source '+name);copy=P/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE'/state/name;check(state+' full small Source copy '+name,(pin(copy)['sha256'],pin(copy)['size_bytes'])==(q['sha256'],q['size_bytes']))
 original=(P/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE'/state/'AxMatTone.c2m').read_bytes();derived=original
 for row in layout['literal_replacements']:
  old,new=row['original'].encode(),row['derived'].encode();check(state+' original exact FIL Source occurrences '+row['original'],type(row['count'])is int and original.count(old)==row['count']and original.count(new)==0);derived=derived.replace(old,new)
 restored=derived
 for row in layout['literal_replacements']:restored=restored.replace(row['derived'].encode(),row['original'].encode())
 check(state+' full c2m allnonFIL numeric bytes inverse',restored==original)
 original_lines=original.splitlines(keepends=True);derived_lines=derived.splitlines(keepends=True);changedlines=[i+1 for i,(a,b)in enumerate(zip(original_lines,derived_lines))if a!=b]
 check(state+' exactly3 full Source lines changed',len(original_lines)==len(derived_lines)and len(changedlines)==3)
 procedure_facts[state]=dict(original_Source_pin=smallpins[state]['AxMatTone.c2m'],original_whole_SHA256=hashlib.sha256(original).hexdigest(),derived_whole_SHA256=hashlib.sha256(derived).hexdigest(),original_bytes=len(original),derived_bytes=len(derived),all_non_FIL_bytes_exact=True,exact_changed_original_line_numbers=changedlines,relative_names=[row['derived'].split("'")[1]for row in layout['literal_replacements']],whole_Source_inverse_verified=True,derived_Source_was_not_installed_or_executed=True)
names=[row['derived'].split("'")[1]for row in layout['literal_replacements']]
check('actual both relative library strings37 fit original NAMFIL64',all(len(s)==37 and len(s)<=64 for s in names))
libinp=archive_bytes['Dragon/src/LIBINP.f'].decode();check('actual original NAMFIL64 and ILIBRARYNAME64 branch',"NAMFIL*64"in libinp and "CALL REDGET(INDIC,NITMA,FLOTT,NAMFIL,DBLINP)"in libinp and "CALL LCMPTC(IPLIB,'ILIBRARYNAME',64,NLIB,HNAME)"in libinp and "HNAME(NLIB)=NAMFIL"in libinp)
filename_sources={}
for p in sorted((P/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE/ACTUAL_ORIGINAL_LIBRARY_FILENAME_SOURCE').iterdir()):
 raw=p.read_bytes();key=next(k for k,v in archive_bytes.items()if Path(k).name==p.name and v==raw);check('original filename entire Source retained '+p.name,archive_bytes[key]==raw);filename_sources[p.name]=dict(archive_member=key,Source_pin=pin(p))
check('honest actual ILIBRARYNAME metadata changes retained',"ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal=True"in rtdefs['copy_state_seeds']and contract['ILIBRARYNAME_filename_Source_metadata_changes_are_saved_not_normalized']is True)
capacity=load(P/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE/Root_actual_duplicate_library_copy_layout_META_budget_20261010.json')
check('186b capacity onlyplanning no N6 diskRSSPASS',capacity['status']=='SAVED_INPUT_META_EXTENTS_AND_LAYOUT_PLANNING_ONLY_NOT_NEW_RUNTIME_ADMISSION'and capacity['new_shared_layout_actual_runtime_bytes']is None and capacity['new_actual_material_product_sizes']is None and capacity['new_actual_native_object_archive_executable_sizes']is None and capacity['new_runtime_storage_or_RSS_or_physical_qualification_created']is False and capacity['compiler_material_candidate_guard_or_business_executed']is False)
check('all future contract facts remain unknownfalse',all(contract[k]is None for k in ('actual_independent_N6_Source_peer','actual_N6_Source_admission','actual_N6_Root_Source_admission_terminal','actual_N6_request','actual_N6_Source_binding','actual_N6_runtime_terminal','actual_N6_observation_manifest','actual_N6_storage_RSS_and_physical_qualification'))and contract['shared_new_layout_storage_or_RSS_or_science_PASS_created']is False)

m=new_m
scope=load(P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json');actual_roles={role:pin(P/rel)for role,rel in scope['required_author_Source_roles'].items()}
check('N7 all14 independent fullactual Sourcepins',len(actual_roles)==14 and actual_roles['qualified_source_manifest']==mp and actual_roles==author_tools['ACTUAL_SOURCE_SEAL_TOOL_RETURN.json']['output']['actual_author_Source_contract'])
for path,q in list(pins.items()):check('N7 final immutable full read pin '+path,pin(path)==q)
check('N7 wholeSource tree originalfreeze noappend',dirs=={str(p):identity(p)for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}and {str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}==set(members)|{'MANIFEST.json'})
report=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'if blockers==[]else'BLOCKED_SOURCE_ONLY_NO_EXECUTION_OR_SCIENCE',source_only=True,actual_author_Source_contract=actual_roles,checks=checks,check_count=len(checks),all_checks_passed=blockers==[],all_checks_typed_true=blockers==[],blockers=blockers,complete_full_EOF_Source_small_META_pins=list(pins.values()),complete_N7_source_files=182,complete_N7_source_directories_including_root=24,complete_py_AST_count=len(asts),whole_native_Source_archive_members=1365,whole_native_Source_gzip_EOF_CRC_verified=True,full_N7_four_role_byte_AST_inverses=n7inverse_facts,full_N6_mother_four_role_byte_AST_inverses=whole_inverse_facts,full_original_four_physics14_insert_inverses=physical_facts,full_original_host12_byte_AST_inverse_verified=True,original_selected_recipes=expected_recipes,shared_original_libraries_layout=layout,full_original_small_procedure_source_transform_proofs=procedure_facts,ILIBRARYNAME_actual_filename_metadata_changes_expected_not_claimed_byte_equal=True,original_N5_closed_PS_only_fix_preserved_by_complete_original_joint_body_AST=True,N7_wrapper_both_original_callable_objects_single_delegate_bare_raise_and_finally_restore_Source_verified=True,N7_original_PS_lsof_full_argv_timeout8MiB_and_parentchain_scope_preserved=True,N7_actual_failure_raw_and_dual_exception_lifecycle_Source_verified=True,N7_successful_scan_raw_not_persisted_single_memory_cache_only=True,N7_original_history_joint_free_caps_unchanged=True,N7_diagnostic_scope_precise_limits=dict(failed_current_open_unlinked_scan_remains_unverified=True,regular_joint_plus_previous_unlinked_is_failed_diagnostic_storage_account_only=True,journal_records_include_current_whole_and_stage_clock=True,added_PS_requires_positive_original_whole_stage_remaining_and_timeout_at_most2seconds=True,failure_housekeeping_and_journal_postwrite_clock_may_be_expired_and_never_grants_PASS=True,failure_record_append_error_is_retained_not_replaced_with_complete_persistence=True,latest_prior_successful_raw_is_prior_evidence_not_cleanup_current_liveness=True,original_legacy_cleanup_true_is_not_cleanup_proof=True,original_N6_lsof_raw_not_recovered=True),author_first848512_KeyError_and_correctedc1413e_tooltruth_preserved=True,actual_instrumented_guard_controls=None,actual_Root_N7_Source_admission=None,actual_N7_request=None,actual_N7_Source_binding=None,actual_N7_runtime_terminal=None,actual_N7_storage_RSS_result=None,actual_new_native_source_objects_executable_qualification=None,actual_material_DB_or_XSM_SQL_numeric_payload_read=False,actual_native_binary_executed=False,candidate_binder_request_host_runtime_postclose_guard_API_compiler_material_execution=False,project_or_author_Source_namespace_modified=False,**future)
out=F/'REVIEW.json'
with out.open('x')as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
print(json.dumps(dict(review_pin=pin(out),check_count=len(checks),all_checks_passed=blockers==[],blockers=blockers,actual_author_Source_contract=actual_roles,source_only=True,candidate_guard_API_compile_native_material_executed=False),allow_nan=False))

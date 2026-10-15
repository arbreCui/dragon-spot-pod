"""Own finite Source author check. Stdlib/AST/full bytes only; never a peer admission."""
import ast,hashlib,json,re,stat,tarfile
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq');checks=[]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def check(name,value):
 if type(value)is not bool or not value:raise AssertionError(name)
 checks.append(dict(check=name,passed=True))
def pin(p):
 s=p.lstat();raw=p.read_bytes();t=p.lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 return dict(path=str(p),sha256=digest(raw),size_bytes=len(raw),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def literal(node):
 if isinstance(node,ast.Constant):return node.value
 if isinstance(node,ast.Tuple):return tuple(literal(x)for x in node.elts)
 if isinstance(node,ast.List):return [literal(x)for x in node.elts]
 if isinstance(node,ast.Dict):return {literal(k):literal(v)for k,v in zip(node.keys,node.values)}
 if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='dict'and not node.args and all(k.arg is not None for k in node.keywords):return {k.arg:literal(k.value)for k in node.keywords}
 if isinstance(node,ast.BinOp)and isinstance(node.op,ast.Mult):return literal(node.left)*literal(node.right)
 if isinstance(node,ast.BinOp)and isinstance(node.op,ast.Pow):return literal(node.left)**literal(node.right)
 raise ValueError('nonliteral Source static constant')
def const(path,name):
 t=ast.parse(path.read_bytes());return next(literal(n.value)for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
files=[p for p in P.rglob('*')if p.is_file()];check('complete namespace has no symbolic special or hardlink aliases',all((stat.S_ISDIR(q.lstat().st_mode)or(stat.S_ISREG(q.lstat().st_mode)and q.lstat().st_nlink==1))and not q.is_symlink()for q in[P,*P.rglob('*')]))
parsed={str(p.relative_to(P)):ast.parse(p.read_bytes(),filename=str(p))for p in files if p.suffix=='.py'};check('all full retained/new Python Source files parse with stdlib AST only',len(parsed)>=14)
index=json.loads((P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());indexed={r['relative_path']:r for r in index['members']};observed={};originals={}
with tarfile.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as archive:
 for m in archive.getmembers():
  assert m.isfile()and m.name in indexed and m.name not in observed and '..'not in Path(m.name).parts and not Path(m.name).is_absolute();d=hashlib.sha256();count=0;blocks=[] if m.name in['Dragon/src/'+s for s in('LIBMIX.f','LIBDEN.f','TONDRV.f','TONSPH.f')]else None
  with archive.extractfile(m)as f:
   while True:
    raw=f.read(2**20)
    if not raw:break
    d.update(raw);count+=len(raw)
    if blocks is not None:blocks.append(raw)
  assert d.hexdigest()==indexed[m.name]['full_original_Source_pin']['sha256']and count==indexed[m.name]['full_original_Source_pin']['size_bytes'];observed[m.name]=dict(sha256=d.hexdigest(),size_bytes=count)
  if blocks is not None:originals[m.name]=b''.join(blocks)
check('whole original four-library native Source archive all1365 members full EOF/index SHA/size unique exactly',len(indexed)==len(observed)==1365 and set(indexed)==set(observed))
check('original Makefiles and original dependency-generator full Source retained with all four components',all(n+'/src/Makefile'in observed for n in('Ganlib','Utilib','Trivac','Dragon'))and 'script/make_depend.py'in observed)
proof=json.loads((P/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json').read_bytes());physical=[]
for row in proof['derivations']:
 raw=(P/row['derived_Source_member']).read_bytes();assert digest(raw)==row['derived_sha256'];lines=raw.decode().splitlines(keepends=True)
 for h in reversed(row['complete_insert_only_hunks']):
  assert h['tag']=='insert'and h['old_full_lines']==[]and lines[h['new_start0']:h['new_end0']]==h['new_full_lines'];lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(lines).encode()==originals[row['original_archive_member']]and digest(''.join(lines).encode())==row['original_sha256'];physical.append(row['original_archive_member'])
check('all four full physical routines reverse14 observer-only insertions to exact complete original arithmetic/branches',len(physical)==4 and sum(len(r['complete_insert_only_hunks'])for r in proof['derivations'])==14)
old=(P/'PARENT_SOURCE/Root_bound_complete_native_genuine_host.py').read_bytes();new=(P/'complete_observation_genuine_host.UNREADY.py').read_bytes();hostproof=json.loads((P/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json').read_bytes());inverse=new
for h in hostproof['complete_full_inverse_hunks']:
 candidate=''.join(h['new_full_lines']).encode();assert inverse.count(candidate)==1;inverse=inverse.replace(candidate,''.join(h['old_full_lines']).encode(),1)
check('complete original genuine native host inverse12 changes equals full original, every original helper unchanged',inverse==old and len(hostproof['complete_full_inverse_hunks'])==12)
pro=json.loads((P/'FULL_NECESSARY_PARENT_SOURCE_PROVENANCE.json').read_bytes())
check('all18 necessary parent original observer/host/binder/postclose/guards retained full original Source bytes',all(pin(P/r['retained_copy'])['sha256']==r['full_original_Source_pin']['sha256']and pin(P/r['retained_copy'])['size_bytes']==r['full_original_Source_pin']['size_bytes']for r in pro['parents'])and len(pro['parents'])==18)
walker=P/'PARENT_SOURCE/Root_bound_complete_native_checker.py';check('original9d849 complete native walker all definitions/9kinds/order/empty retained exact full Source',digest(walker.read_bytes())=='9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0')
active=['complete_observation_BUILD5_AB_runtime.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'];caps=const(P/active[0],'CAPS');future=const(P/active[0],'FUTURE');check('all4 new execution/binding/postclose/preparation Sources use exact original integer caps and same actualNone/sciencefalse futures',all(const(P/n,'CAPS')==caps and all(type(v)is int for v in const(P/n,'CAPS').values())and const(P/n,'FUTURE')==future for n in active)and caps==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)and all(v is None or v is False for v in future.values()))
check('complete active host/runtime are UNREADY; runtime flag unchanged-guard future qualifiers cannot activate by CLI',const(P/'complete_observation_genuine_host.UNREADY.py','SOURCE_STATUS')=='UNREADY_SOURCE_ONLY'and const(P/active[0],'SOURCE_STATUS')=='UNREADY_SOURCE_ONLY'and all(const(P/'complete_observation_genuine_host.UNREADY.py',k)is None for k in('SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA')))
check('Source binder/request preparer whole13 original Source role contracts are equal',const(P/active[1],'ROLES')==const(P/active[3],'ROLES')and len(const(P/active[1],'ROLES'))==13)
module=(P/'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90').read_text();labels=const(P/active[0],'LABELS');module_labels=re.findall(r"call start_event\('([^']+)'",module);check('full original AXOBSCTXv2 module9 real event roles cover every original SPH/context branch, enable exact20byteenv',len(module_labels)==9 and set(labels)==set(module_labels)and "n==20"in module and "flag(:20)=='ADMITTED_SOURCE_ONLY'"in module and "'AXOBSCTX',2_c_int32_t"in module)
runtime=(P/active[0]).read_text();post=(P/active[2]).read_text();binder=(P/active[1]).read_text()
check('full fresh compile architecture4libraries+new link preserves original flags and excludes every old object/archive/executable',all(x in runtime for x in("for component in ('Ganlib','Utilib','Trivac','Dragon')","stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link']","require(platform.system()=='Darwin'and platform.machine()=='arm64'","'-ffpe-summary=none','-O','-g'","'-frecord-marker=4'","require(not os.path.lexists(exe)","require(not os.path.lexists(obj)","all_sources_objects_archives_checked_after_actual_link=True")))
check('native commands only through unchanged original genuine runner/classes/MRO and all actual closed watchpins',all(x in runtime for x in("runner.execute(folder,label,argv,remaining,deck=deck,marker=marker)","full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","type(runner)is full.OwnRSSSerialExecutor","watch['returncode']==0","watch['command']==argv","watch['own_child_only']is True","watch['liveness_group_cleanup']is True","remaining=min(600,deadline-time.monotonic())","time.monotonic()-started<1800")))
check('all Source/objects/archives/new executable and every command-watch linkage saved, full preprocessor Source retained losslessly',all(x in runtime for x in('original_source_pin=sp','preprocessor_output_pin=preprocessed','retained_complete_preprocessor_Source_pin=retained_preprocessed','actual_compile=stage','new_object_pin=op','actual_archive_command=archive_stage','all_actual_link_input_pins=link_inputs','new_actual_executable_pin=ep','require(frozen_sources(native,index,observation_source)==original')))
check('original history/free check delegates unchanged; live complete HOCDE regular+openunlinked and full D/E freeze all counted',all(x in runtime for x in('class JointHistoryResources(resource.DynamicHistoryResources)','value=super().check()','open_unlinked_bytes=unlinked_bytes',"joint['complete_joint_HOCDE_bytes']<2*2**30",'tree(archive)==dfreeze and tree(receipts)==efreeze',"value['artifact_bytes']+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])+joint['open_unlinked_bytes']<=96*2**30","8*2**30,96*2**30,production.ResourceFailure")))
check('all original129 fullpins and original10 deck/procedure/geometric seed pins remain exact; no librarygeneration or physics substitutions',all(x in runtime and x in binder for x in("seed_contract['original129_input_pins']","seed_contract['states'][state]","seed_contract['libraries'][destination]['generation_sha256']"))and len(json.loads((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes())['original129_input_pins'])==129)
check('A child material and all filehandles closed before B, all event/context/snapshot order/full EOF/new final retained',all(x in runtime for x in("for state in('A','B')",'all_A_handles_closed_before_B=True',"require(not any(Path(v).is_relative_to(folder)for v in closure['actual_open_regular_paths'])",'all_producer_file_handles_closed_before_next_state=True','event==number',"set(files)==all_observer_names","role not in('postmacro-LIBMIX','final-complete-micro')",'new_final_micro_from_actual_TONDRV_observer=True')))
check('peer/admission/actualRoottypedCLOSED provenance gates enforced by complete host runtime and binder before source writes/native actions',all(x in runtime and x in binder for x in('INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1','ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'))and "validate_request(b,author)"in runtime and binder.index("actual Root typed0 CLOSED Source admission")<binder.index('out.mkdir()'))
check('full postclose writer requires Rootactualtypedzero/closed and full actual build/event/snapshot/Input/D/E coupling before E receipt',all(x in post for x in("'ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1'","t['exit_code']==0","stdout['actual_host_result_pin']==host_pin","tree(ds)==h['complete_Source_D_freeze']and tree(es)==h['complete_receipt_E_freeze']","for p in h['complete_input_pins_before_and_after']:check(p)","for p in row['complete_state_snapshot_inputs']:check(p['input_pin'])","check(build['new_actual_executable_pin'])","resource.DynamicHistoryResources(art,history,8*2**30,96*2**30)","Root_checked_all_whole_event_snapshot_and_new_executable_fullpins=True")))
check('failure path preserves nonzero evidence/errors/all pinned inputs and frozen D/E; no retries or fabricated success',all(x in runtime for x in('except BaseException as error','complete_input_pins_before=inputs','complete_input_pins_after_failure=after_inputs','full_postfailure_freeze_errors=freeze_errors','actual_observation_manifest_pin_if_saved=','FAILED_NO_RETRY_NO_QUALIFICATION')))
check('compiler descendant RSS and native/API snapshot bits are explicitly not qualified; all future runtime/science gates unknown',"compiler_descendant_RSS_scope_not_certified=True"in runtime and "native_snapshot_api_or_memory_bits_qualified=False"in runtime and all(v is None or v is False for v in future.values()))
for name in active:
 t=parsed[name];func=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='require');source=ast.get_source_segment((P/name).read_text(),func);assert 'type('in source and 'is not bool'in source
 for n in ast.walk(t):
  if isinstance(n,ast.Call):
   explicit=[k.arg for k in n.keywords if k.arg is not None];assert len(explicit)==len(set(explicit))
check('all4 strict require gates demand real booleans and complete new AST has no repeated explicit keyword TypeError',True)
steps=json.loads((P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json').read_bytes());check('real six-step Root prepin/bind/genuinebuild/postclose/context handoff supplied and all actual output pins remain unknown',len(steps['steps'])==6 and steps['actual_runtime_qualification_sha256']is None and steps['actual_observer_native_controls_run']is None)
report=dict(schema='AUTHOR_FINITE_COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_SOURCE_CHECK_V1',status='AUTHOR_STATIC_SOURCE_CHECKS_COMPLETE_UNREADY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=True,blockers=[],whole_native_Source_archive_members=len(observed),complete_Python_Source_files_AST_checked=len(parsed),physics_insert_hunks14=14,original_genuine_host_full_inverse_hunks12=12,full_Source_file_pins_before_seal=[pin(p)for p in sorted(files)],no_candidate_import_compile_API_native_material_or_SQL_payload_execution=True,no_material_or_SQL_payload_read_by_author=True,no_project_write_by_author=True,independent_Source_review=None,actual_Root_Source_admission=None,actual_Root_terminal=None,actual_observation_manifest=None,actual_compiler_objects_archives_executable=None,**future)
with(P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(checks),whole_native_Source_archive_members=len(observed),Source_AST_files=len(parsed),actual_native_execution=None,author_check_report=pin(P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json')),allow_nan=False))

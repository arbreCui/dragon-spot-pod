"""Own finite Source author check. Stdlib/AST/full bytes only; never a peer admission."""
import ast,hashlib,json,re,stat,tarfile,posixpath,fnmatch
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac');O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq');checks=[]
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
check('Source binder/request preparer whole14 necessary Source role contracts are equal',const(P/active[1],'ROLES')==const(P/active[3],'ROLES')and len(const(P/active[1],'ROLES'))==14)
module=(P/'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90').read_text();labels=const(P/active[0],'LABELS');module_labels=re.findall(r"call start_event\('([^']+)'",module);check('full original AXOBSCTXv2 module9 real event roles cover every original SPH/context branch, enable exact20byteenv',len(module_labels)==9 and set(labels)==set(module_labels)and "n==20"in module and "flag(:20)=='ADMITTED_SOURCE_ONLY'"in module and "'AXOBSCTX',2_c_int32_t"in module)
runtime=(P/active[0]).read_text();post=(P/active[2]).read_text();binder=(P/active[1]).read_text()
check('full fresh compile architecture4libraries+new link preserves original flags and excludes every old object/archive/executable',all(x in runtime for x in("for component in ('Ganlib','Utilib','Trivac','Dragon')","stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link']","require(platform.system()=='Darwin'and platform.machine()=='arm64'","'FFLAGS':['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none']","'FFLAG77':['-fPIC','-frecord-marker=4','-ffpe-summary=none']","require(not os.path.lexists(exe)","require(not os.path.lexists(obj)","all_sources_objects_archives_checked_after_actual_link=True")))
check('native commands only through unchanged original genuine runner/classes/MRO and all actual closed watchpins',all(x in runtime for x in("runner.execute(folder,label,argv,remaining,deck=deck,marker=marker)","full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","type(runner)is full.OwnRSSSerialExecutor","watch['returncode']==0","watch['command']==argv","watch['own_child_only']is True","watch['liveness_group_cleanup']is True","remaining=min(600,deadline-time.monotonic())","time.monotonic()-started<1800")))
check('all Source/objects/archives/new executable and every command-watch linkage saved, full preprocessor Source retained losslessly',all(x in runtime for x in('original_source_pin=sp','preprocessor_output_pin=preprocessed','retained_complete_preprocessor_Source_pin=retained_preprocessed','actual_compile=stage','new_object_pin=op','actual_archive_command=archive_stage','all_actual_link_input_pins=link_inputs','new_actual_executable_pin=ep','require(frozen_sources(native,index,observation_source)==original')))
check('original history/free check delegates unchanged; live complete HOCDE regular+openunlinked and full D/E freeze all counted',all(x in runtime for x in('class JointHistoryResources(resource.DynamicHistoryResources)','value=super().check()','open_unlinked_bytes=unlinked_bytes',"joint['complete_joint_HOCDE_bytes']<2*2**30",'tree(archive)==dfreeze and tree(receipts)==efreeze',"value['artifact_bytes']+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])+joint['open_unlinked_bytes']<=96*2**30","8*2**30,96*2**30,production.ResourceFailure")))
check('all original129 fullpins and original10 deck/procedure/geometric seed pins remain exact; no librarygeneration or physics substitutions',all(x in runtime and x in binder for x in("seed_contract['original129_input_pins']","seed_contract['states'][state]","seed_contract['libraries'][destination]['generation_sha256']"))and len(json.loads((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes())['original129_input_pins'])==129)
check('A child material and all filehandles closed before B, all event/context/snapshot order/full EOF/new final retained',all(x in runtime for x in("for state in('A','B')",'all_A_handles_closed_before_B=True',"require(not any(Path(v).is_relative_to(folder)for v in closure['actual_open_regular_paths'])",'all_producer_file_handles_closed_before_next_state=True','event==number',"set(files)==all_observer_names","role not in('postmacro-LIBMIX','final-complete-micro')",'new_final_micro_from_actual_TONDRV_observer=True')))
check('peer/admission/actualRoottypedCLOSED provenance gates enforced by complete host runtime and binder before source writes/native actions',all(x in runtime and x in binder for x in('INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1','ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'))and "validate_request(b,author)"in runtime and binder.index("actual Root typed0 CLOSED Source admission")<binder.index('out.mkdir()'))
check('full postclose writer requires Rootactualtypedzero/closed and full actual build/event/snapshot/Input/D/E coupling before E receipt',all(x in post for x in("'ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1'","t['exit_code']==0","stdout['actual_host_result_pin']==host_pin","tree(ds)==h['complete_Source_D_freeze']and tree(es)==h['complete_receipt_E_freeze']","for p in h['complete_input_pins_before_and_after']:check(p)","for p in row['complete_state_snapshot_inputs']:","check(build['new_actual_executable_pin'])","resource.DynamicHistoryResources(art,history,8*2**30,96*2**30)","Root_checked_all_whole_event_snapshot_and_new_executable_fullpins=True")))
check('failure path preserves nonzero evidence/errors/all pinned inputs and frozen D/E; no retries or fabricated success',all(x in runtime for x in('except BaseException as error','complete_input_pins_before=inputs','complete_input_pins_after_failure=after_inputs','full_postfailure_freeze_errors=freeze_errors','actual_observation_manifest_pin_if_saved=','FAILED_NO_RETRY_NO_QUALIFICATION')))
check('compiler descendant RSS and native/API snapshot bits are explicitly not qualified; all future runtime/science gates unknown',"compiler_descendant_RSS_scope_not_certified=True"in runtime and "native_snapshot_api_or_memory_bits_qualified=False"in runtime and all(v is None or v is False for v in future.values()))
for name in active:
 t=parsed[name];func=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='require');source=ast.get_source_segment((P/name).read_text(),func);assert 'type('in source and 'is not bool'in source
 for n in ast.walk(t):
  if isinstance(n,ast.Call):
   explicit=[k.arg for k in n.keywords if k.arg is not None];assert len(explicit)==len(set(explicit))
check('all4 strict require gates demand real booleans and complete new AST has no repeated explicit keyword TypeError',True)
steps=json.loads((P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json').read_bytes());check('real six-step Root prepin/bind/genuinebuild/postclose/context handoff supplied and all actual output pins remain unknown',len(steps['steps'])==6 and steps['actual_runtime_qualification_sha256']is None and steps['actual_observer_native_controls_run']is None)

# Restricted interpretation of original selected Makefile variable and
# conditional Source. It never invokes make, shell, native, or Source imports.
def selected_original_variables(text):
 variables=dict(ARCH='arm64',OS='Darwin',DIRNAME='Darwin_arm64',openmp='0',intel='0',nvidia='0',llvm='0',mpi='0',hdf5='0');stack=[];active=True
 def expand(value):
  while '$('in value:
   start=value.index('$(');depth=1;end=start+2
   while depth:
    if value.startswith('$(',end):depth+=1;end+=2;continue
    if value[end]==')':depth-=1
    end+=1
   expression=expand(value[start+2:end-1])
   if expression.startswith('filter '):
    patterns,words=expression[7:].split(',',1);replacement=' '.join(w for w in words.split()if any(fnmatch.fnmatchcase(w,p.replace('%','*'))for p in patterns.split()))
   elif expression.startswith('shell '):raise AssertionError('unrecognized active shell Source expression; never execute')
   else:replacement=expand(variables.get(expression,''))
   value=value[:start]+replacement+value[end:]
  return value
 def pair(value):
  depth=0
  for i,c in enumerate(value):
   if c=='(':depth+=1
   if c==')':depth-=1
   if c==','and depth==0:return value[:i],value[i+1:]
  raise AssertionError('complete original conditional comma')
 for full in text.splitlines():
  line=full.strip()
  if line.startswith('SRCC ='):break
  if line.startswith(('ifeq ','ifneq ')):
   kind,args=line.split(None,1);left,right=pair(args[1:-1]);condition=(expand(left).strip()==expand(right).strip());condition=condition if kind=='ifeq'else not condition;stack.append((active,condition));active=active and condition;continue
  if line=='else':parent,condition=stack[-1];stack[-1]=(parent,not condition);active=parent and not condition;continue
  if line=='endif':parent,condition=stack.pop();active=parent;continue
  if not active or not line or line.startswith('#'):continue
  match=re.fullmatch(r'([A-Za-z_][A-Za-z_0-9]*)\s*(\+=|:=|=)\s*(.*)',line)
  if not match:continue
  name,op,value=match.groups()
  if name in('ARCH','OS','DIRNAME'):continue
  if name=='PY'and value.startswith('$(shell '):value='python3'
  if op=='+=':variables[name]=variables.get(name,'')+' '+value
  else:variables[name]=expand(value)if op==':='else value
 assert not stack
 return {key:expand(value).split()for key,value in variables.items()}
make_sources={};native_counts={}
with tarfile.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as archive:
 for component in('Ganlib','Utilib','Trivac','Dragon'):
  name=component+'/src/Makefile';make_sources[component]=archive.extractfile(name).read().decode();native_counts[component]={suffix:sum(Path(name).parent==Path(component+'/src')and Path(name).suffix==suffix for name in observed)for suffix in('.c','.f90','.F90','.f','.F')}
recipes=const(P/active[0],'ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES');selected={};native_namespace={}
for component,text in make_sources.items():
 values=selected_original_variables(text);selected[component]=values;recipe=recipes[component]
 for key in('CFLAGS','FLAGS','FFLAGS','FFLAG77','INCLUDE','FMPI','opt','COMP','LFLAGS'):assert recipe[key]==values.get(key,[]),(component,key,recipe[key],values.get(key,[]))
 assert values['F90']==['gfortran']and recipe['F90']=='fortran'
 assert recipe['C']==('c'if values.get('C')==['gcc']else None)
 assert recipe['PREPRO']==('cpp'if values.get('PREPRO')==['cpp']else None)
 module=values.get('lib_module');expected=None if not module else posixpath.normpath(component+'/src/'+module[0]);assert recipe['lib_module']==expected
 assert recipe['module_copy']==('cp *.mod $(lib_module)'in text)
 assert posixpath.normpath(component+'/src/'+values['lib'][0])==component+'/lib/Darwin_arm64'
 assert 'ar rcs $@ $(OBJC) $(OBJ90) $(OBJ77) $(OBJF77)'in text and 'cp $@ $(lib)/$@'in text
 assert 'SRC90 = $(shell $(PY) ../../script/make_depend.py *.f90 *.F90 2>/dev/null)'in text
 native_namespace[component]=dict(module_path=expected,include=recipe['INCLUDE'],archive_path=component+'/lib/Darwin_arm64/lib'+component+'.a')
check('complete original selected Darwin arm64 GNU per-library compiler variable flags tools empty flags exactly match original full Makefile conditional Source',True)
check('all actual suffix commands preserve each original recipe argument dispatch without Ganlib/Utilib invented include or common Trivac Wall',all(x in runtime for x in("*recipe['CFLAGS'],*recipe['FLAGS'],*recipe['opt'],*recipe['COMP']","flags=recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']","*flags,*recipe['opt'],*recipe['COMP'],*recipe['INCLUDE']","*recipe['FLAGS']","if p.suffix=='.F':argv+=recipe['FMPI']"))and native_counts['Utilib']['.c']==16 and recipes['Utilib']['FLAGS']==[]and recipes['Ganlib']['INCLUDE']==recipes['Utilib']['INCLUDE']==[]and '-Wno-maybe-uninitialized'in recipes['Ganlib']['FFLAGS']and '-Wall'not in recipes['Trivac']['FFLAGS']and '-Wall'not in recipes['Trivac']['FFLAG77'])
check('original archive OBJC OBJ90 OBJ77 OBJF77 suffix group order and original f90 F90 generator argument group order retained',all(x in runtime for x in("f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))]","f77_lower=sorted(folder.glob('*.f'));f77_upper=sorted(folder.glob('*.F'));f77=[*f77_lower,*f77_upper]","generator.build_dependency_order([str(p)for p in f90])","objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]","argv=[tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)]"))and native_counts['Ganlib']['.F']==3 and native_counts['Dragon']['.F']==7)
check('per-library original module namespaces and includes preserved with Trivac no module copy and Utilib original unguarded copy condition',recipes['Ganlib']['lib_module']=='Ganlib/lib/Darwin_arm64/modules'and recipes['Utilib']['lib_module']=='Utilib/lib/Darwin_arm64/modules'and recipes['Dragon']['lib_module']=='Dragon/lib/Darwin_arm64/modules'and recipes['Trivac']['lib_module']is None and recipes['Trivac']['module_copy']is False and all(x in runtime for x in("modules=native/recipe['lib_module']","require(component!='Utilib'or bool(generated_modules)","shutil.copy2(p,target)","archives[component]=library_copy_pin")))
check('original final-link archive copies now use each original per-library lib directory in original Dragon Trivac Utilib Ganlib order',all(x in runtime for x in("library_copy=library_dir/archive.name","library_copy_pin['sha256']==ap['sha256']","archives[k]for k in('Dragon','Trivac','Utilib','Ganlib')","*link_recipe['opt'],*link_recipe['COMP']","*link_recipe['LFLAGS']"))and "check(stage['original_recipe_library_copy_pin'])"in post and "check(module['original_recipe_module_copy_pin'])"in post)
fix=json.loads((P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json').read_bytes());oldmf=json.loads((P/'ORIGINAL_BLOCKED_COMPLETE_SOURCE_MANIFEST.json').read_bytes());oldpins=[]
for row in oldmf['members']:
 original=Path(row['fullpin']['path']);assert pin(original)==row['fullpin'];oldpins.append(row['relative_path'])
check('immutable complete original frozen39file4dir package whole manifest all38member full EOF 7ID preserved exactly',len(oldpins)==38 and digest((O/'MANIFEST.json').read_bytes())==fix['original_frozen_manifest_sha256']=='2a1c950bcf036e1534901333af2f50c2f53ab12105502e247445e9a8fe9c066a')
fixed={}
for row in fix['source_derivations']:
 raw=(P/row['source_member']).read_bytes();original=(O/row['source_member']).read_bytes();assert digest(raw)==row['fixed_sha256']and digest(original)==row['original_sha256'];lines=raw.decode().splitlines(keepends=True)
 for h in reversed(row['complete_full_inverse_hunks']):assert lines[h['new_start0']:h['new_end0']]==h['new_full_lines'];lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(lines).encode()==original;fixed[row['source_member']]=row
check('eight complete finite Source META changes reverse all30 full hunks to exact original frozen full bytes',len(fixed)==8 and sum(len(r['complete_full_inverse_hunks'])for r in fixed.values())==30)
unchanged=[]
for name in oldpins:
 if name in fixed or name=='AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json':continue
 assert (P/name).read_bytes()==(O/name).read_bytes();unchanged.append(name)
assert (P/'ORIGINAL_AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').read_bytes()==(O/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').read_bytes()
check('all remaining30 original Source META members losslessly preserved including original author report and native1365 archive physical observers and genuine MRO',len(unchanged)==29 and digest((P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz').read_bytes())==digest((O/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz').read_bytes()))
legacy=(P/'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py').read_text();legacy_origin=Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox/complete_observed_old_post_final_XSM_extractor.UNREADY.py')
check('existing complete qualified context oldXSM extractor retained whole byte unchanged; walker begins actual native.root and prefix only emits logical pool paths',legacy_origin.read_bytes()==legacy.encode()and 'native.walk_table(native.root,tuple(prefix),())'in legacy and "set(item)=={'event','role','root_prefix','input_pin'}"in legacy and "['MACROLIB']"in legacy)
check('new snapshot canonical exact native root[] explicit logical_prefix and legacy exact4keys mapping preserves original macro logical paths',all(x in runtime for x in("root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB']","dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])","legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup'"))and all(x in post for x in("set(p)=={'event','role','root_prefix','logical_prefix','input_pin'}","p['root_prefix']==[]","root_prefix=p['logical_prefix']"))and fix['snapshot_prefix_old_runtime_failure_claim_withdrawn']is True)
scope=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes());roles=const(P/active[1],'ROLES');check('all14 whole Source roles identical in binder preparer independent scope and request admission template, including full legacy context extractor',scope['required_author_Source_roles']==roles and set(json.loads((P/'ROOT_OBSERVATION_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())['actual_author_Source_contract'])==set(roles)and set(json.loads((P/'ROOT_OBSERVATION_SOURCE_ADMISSION_TEMPLATE.UNREADY.json').read_bytes())['actual_author_Source_contract'])==set(roles))
check('postclose output embeds all five actual complete dirs and all regular files full EOF SHA size 7ID views including previously omitted H outputs',all(x in post for x in("namespace_keys=('host','output','control','source','receipts')","namespace_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}","Root_complete_postclose_HOCDE_namespace_views=namespace_views","all_regular_file_full_EOF_sha256_size_and_7_identity_saved=True","files.append(fullpin(q))")))
check('complete E view explicitly predates own manifest append, D never appended and all five namespace fullpins checked after own single append',all(x in post for x in("E_view_before_this_manifest_append=True","D_namespace_never_appended=True","after_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}","after_views[key]==namespace_views[key]for key in namespace_keys[:-1]","[*namespace_views['receipts']['files'],out_pin]","current[:3]==identity[:3]","this_manifest_actual_fullpin_is_in_actual_Root_stdout=True")))
check('postclose receipt own complete bytes count in joint2GiB history96GiB free8GiB caps after append and actual manifest fullpin emitted to Root stdout',all(x in post for x in("sum(p['size_bytes']for view in after_views.values()for p in view['files'])","resource_after['artifact_bytes']+outside_after<96*2**30","joint_after<2*2**30","actual_observation_manifest_pin=out_pin","Root_postclose_joint_HOCDE_bytes_including_own_manifest=joint_after")))
ret=json.loads((P/'ORIGINAL_BLOCKED_INDEPENDENT_SOURCE_REVIEW/FULL_ORIGINAL_BLOCKED_REVIEW_FINITE_RETENTION_PROVENANCE.json').read_bytes())
for row in ret['complete_retained_small_META_and_true_tool_receipts']:assert digest((P/row['retained_member']).read_bytes())==row['sha256']and len((P/row['retained_member']).read_bytes())==row['size_bytes']
review=json.loads((P/'ORIGINAL_BLOCKED_INDEPENDENT_SOURCE_REVIEW/REVIEW.json').read_bytes());check('final independent old Source BLOCKED report and real review seal postseal truths retained losslessly; no peer PASS reused for fixed Source',ret['original_review_is_BLOCKED_not_candidate_PASS']is True and review['all_checks_passed']is False and len(review['checks'])==49 and sum(x['passed']is False for x in review['checks'])==4 and ret['actual_fixed_Source_independent_review']is None)

check('postclose E append parent allows actual Darwin directory nlink size timestamps change while dev inode mode and all namespace files remain exact',"current[:3]==identity[:3]"in post and "current[:4]==identity[:4]"not in post and "E gains exactly own manifest"in post)
check('postclose E actual and expected complete fullpins share exact full string path sort key without changing original tree or snapshot order',"sorted(after_views['receipts']['files'],key=lambda p:p['path'])==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])"in post)
report=dict(schema='AUTHOR_FINITE_COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_SOURCE_CHECK_V1',status='AUTHOR_STATIC_SOURCE_CHECKS_COMPLETE_UNREADY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=True,blockers=[],whole_native_Source_archive_members=len(observed),complete_Python_Source_files_AST_checked=len(parsed),physics_insert_hunks14=14,original_genuine_host_full_inverse_hunks12=12,full_Source_file_pins_before_seal=[pin(p)for p in sorted(files)],original_recipe_selected_Source_variable_evidence=selected,complete_original_native_Source_suffix_counts=native_counts,original_per_component_module_include_archive_namespace=native_namespace,finite_full_Source_fix_changed_members=len(fixed),finite_full_Source_fix_inverse_hunks=sum(len(r['complete_full_inverse_hunks'])for r in fixed.values()),old_independent_review_is_BLOCKED=True,snapshot_prefix_naming_clarification_is_not_old_runtime_failure=True,no_candidate_import_compile_API_native_material_or_SQL_payload_execution=True,no_material_or_SQL_payload_read_by_author=True,no_project_write_by_author=True,independent_Source_review=None,actual_Root_Source_admission=None,actual_Root_terminal=None,actual_observation_manifest=None,actual_compiler_objects_archives_executable=None,**future)
with(P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(checks),whole_native_Source_archive_members=len(observed),Source_AST_files=len(parsed),actual_native_execution=None,author_check_report=pin(P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json')),allow_nan=False))

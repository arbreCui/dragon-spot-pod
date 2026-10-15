from pathlib import Path
import ast,hashlib,json,os,stat,time,resource
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';OLD=REC/'aaa_three_plane_streaming_pipeline_source_v10';NEW=REC/'aaa_three_plane_streaming_pipeline_source_v11';D=REC/'independent_pipeline_v11_closed_metadata_source_review_20261013';D.mkdir(exist_ok=True);start=time.monotonic();checks=[];full={};read_bytes=0
HF=NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json';CLI=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json';MEM=REC/'independent_v10_parent_memory_lifetime_review_20261013/REVIEW.json'
def req(v,s):assert type(v)is bool and v,s;checks.append(s)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 global read_bytes
 p=Path(p);before=ident(p.lstat());req(p.is_absolute()and stat.S_ISREG(before[2])and not p.is_symlink(),'actual regular wholeEOF '+str(p))
 with p.open('rb')as f:
  req(ident(os.fstat(f.fileno()))==before,'same opened7ID '+str(p));h=hashlib.sha256();size=0
  while True:
   b=f.read(2**20)
   if not b:break
   size+=len(b);h.update(b)
  req(ident(os.fstat(f.fileno()))==before,'same wholeEOF fd7ID '+str(p))
 req(ident(p.lstat())==before and size==before[4],'same final path7ID/whole size '+str(p));read_bytes+=size
 v=dict(path=str(p),sha256=h.hexdigest(),size_bytes=size,identity=before)
 if str(p)in full:req(full[str(p)]==v,'one actual current PF '+str(p))
 full[str(p)]=v;return v

def verify(p):
 if p['path']not in full:req(pin(p['path'])==p,'exact all four wholePF fields '+p['path'])
 else:req(full[p['path']]==p,'same known wholePF '+p['path'])
def load(p):return json.loads(Path(p).read_bytes())
def pin_key(p):
 if isinstance(p,dict)and all(k in p for k in('path','sha256','size_bytes','identity'))and isinstance(p['identity'],list):return p['path'],p['sha256'],p['size_bytes'],tuple(p['identity'])
 return None
hfp=pin(HF);clip=pin(CLI);memp=pin(MEM)
req(hfp['sha256']=='2597f653ebb8d24e454d0f129efb1db1f623073e4524b9ce0b560d54ade56736'and hfp['identity']==[16777229,50017634,33188,1,163351,1791873144732798330,1791873144732798330],'Root-selected actual v11HF SHA/all7ID')
req(clip['sha256']=='5a00c302d82b76ff7cb8776aa2bfc7db5aa126c9c4845e495f74ce5c776507d1'and clip['identity']==[16777229,50017635,33188,1,13380,1791873144733698750,1791873144733698750],'Root-selected actual v11CLI SHA/all7ID')
req(memp['sha256']=='e3f5ab935b81d8b2e5a6f59bcce903b6edcb12d898973469a097be15903018b5','actual readonly memory evidence exact SHA')
hf=load(HF);oldhf=load(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');cli=load(CLI);inverse=load(NEW/'COMPLETE_V10_TO_V11_CLOSED_METADATA_LIFETIME_BYTE_INVERSE.json')
req(hf['schema']=='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11'and len(hf['dependencies'])==308 and len(oldhf['dependencies'])==278,'exact308 current v11 Source dependencies derived original278')
for p in [hf['host_source']]+hf['dependencies']:verify(p)
verify(hf['predecessor_host_freeze']);req(hf['predecessor_host_freeze']['path']==str(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),'exact unmodified v10 predecessorSourceHF retained')
for p in oldhf['dependencies']:
 oldpath=Path(p['path'])
 if oldpath.parent==OLD and (NEW/oldpath.name).exists():q=pin(NEW/oldpath.name)
 else:q=p
 req(q in hf['dependencies'],'whole correct current derivation retains old278 dependency '+p['path'])
# Compile/admission/math/caps/rawrecords are immutable, only exact9 changes.
verify(inverse['old_host_source_pin']);verify(inverse['new_host_source_pin']);a=(OLD/'run_actual_three_plane_pipeline.py').read_text();b=(NEW/'run_actual_three_plane_pipeline.py').read_text();forward=a;back=b
req(len(inverse['exact_ordered_changes'])==9,'exact nine ordered lifecycle/namespace/schema changes')
for change in inverse['exact_ordered_changes']:
 req(forward.count(change['old_block'])==change['count'],'exact forward old block count '+change['label']);forward=forward.replace(change['old_block'],change['new_block'])
for change in reversed(inverse['exact_ordered_changes']):
 req(back.count(change['new_block'])==change['count'],'exact reverse new block count '+change['label']);back=back.replace(change['new_block'],change['old_block'])
req(forward==b and back==a,'entire forward and reverse source bytes exactly oldv10/newv11')
for name in('actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90'):
 req((OLD/name).read_bytes()==(NEW/name).read_bytes(),'whole original helper bytes unchanged '+name)
for name in('actual_inputs_and_readback.py','run_actual_three_plane_pipeline.py'):ast.parse((NEW/name).read_bytes());checks.append('whole candidate AST read without import '+name)
ta=ast.parse(a);tb=ast.parse(b)
def functions(raw,t):return{n.name:ast.get_source_segment(raw,n)for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
fa=functions(a,ta);fb=functions(b,tb)
for name in fa:
 if name!='main':req(fa[name]==fb[name],'all non-main original class/function whole bytes '+name)
# Complete main after admitted lifetimes is recovered exactly. All original
# guards, code/deck/oracles and raw records publication are covered by inverse.
main=next(n for n in tb.body if isinstance(n,ast.FunctionDef)and n.name=='main');deletes=[n for n in main.body if isinstance(n,ast.Delete)];req(len(deletes)==2,'exact two explicit main metadata lifetime deletion statements')
del_names=[n.id for d in deletes for n in d.targets];req(del_names==inverse['exact_deleted_names'],'exact declared closed report names no unrelated deletion')
endline=deletes[-1].end_lineno
for n in ast.walk(main):
 if isinstance(n,ast.Name)and isinstance(n.ctx,ast.Load)and n.id in del_names and n.id!='row':req(n.lineno<=endline,'no deleted non-row report futureload '+n.id+' '+str(n.lineno))
# Row has lexical-local names; no access to deleted last producer dict.
for fn in(n for n in main.body if isinstance(n,ast.FunctionDef)):
 rows=[n for n in ast.walk(fn)if isinstance(n,ast.Name)and n.id=='row'and isinstance(n.ctx,ast.Load)]
 if rows:
  req('row'in[f.arg for f in fn.args.args]or any(isinstance(n,ast.Name)and n.id=='row'and isinstance(n.ctx,ast.Store)for n in ast.walk(fn)),'future inner row has own lexical binding '+fn.name)
req('for i,row in enumerate(plan[\'producers\'],1)'in b,'future main row is explicitly rebound to small plan producer')
# Exact completed fullpin union before deleting parent JSON containers.
old_fixed=next(ast.get_source_segment(a,n)for n in ast.walk(ta)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='fixed'for x in n.targets)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='unique')
new_fixed=next(ast.get_source_segment(b,n)for n in ast.walk(tb)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='fixed'for x in n.targets)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='unique')
req(old_fixed==new_fixed,'entire fixed merge pins/dependencies/source/originalrecords union source unchanged')
verifyline=next(n.lineno for n in main.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and ast.unparse(n.value)=='c.verify_rows(fixed)')
req(verifyline<deletes[0].lineno and all(n.lineno>endline for n in ast.walk(main)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='mkdir'),'all immutable admissions+wholeEOF precede delete and all mkdir/business follow')
gc_calls=[n for n in ast.walk(tb)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='gc'and n.func.attr=='collect'];req(len(gc_calls)==1 and gc_calls[0].lineno>endline,'one standard cyclicGC strictly after metadata closures before business')
# Compiler/inc/archive/runtime are real existing authority values, all argv
# lists equal original constructors when unpacked tuples preserve ordering.
auth=inverse['actual_cached_command_authority'];verify(auth['actual_closed_build70_pin']);build=load(auth['actual_closed_build70_pin']['path'])
req(build['schema']=='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2'and build['status']=='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'and build['failure']is None and build['after_check_error']is None and build['final_report_resource_check_passed']is True and len(build['records'])==3,'cache authority actual current70 real3stage closure')
cmd=build['records'][0]['command'];link=build['records'][-1]['command'];compiler=cmd[0];includes=tuple(x for x in cmd if x.startswith('-I'));archives=tuple(x for x in link if x.endswith('.a'));exe=next(p for p in build['output_pins']if Path(p['path']).name=='Dragon')
req(auth['exact_compiler']==compiler and auth['exact_ordered_includes']==list(includes)and auth['exact_ordered_archives']==list(archives)and auth['exact_runtime_executable_pin']==exe,'all four cached small fields real exact runtime/command authority')
req(auth['original_full_compile_command']==cmd and auth['original_full_ordered70_link_command']==link,'exact original full compile and ordered70 link command')
req("link_command=build['records'][-1]['command']"in b and 'probe_link=[*link_command[:3],*probe_inputs' in b,'original full linkcommand retained and exact3 header unchanged')
for k in('compiler','includes','archives','exe','bounded_sha256'):
 assigns=[n for n in ast.walk(main)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id==k for x in n.targets)]
 req(len(assigns)==1 and verifyline<assigns[0].lineno<deletes[0].lineno,'cache'+k+' exactly once only after fullfixed EOF and before closure')
req("owned[1]['sha256']!=bounded_sha256"in b and "bounded_sha256=binding['original_bounded']['sha256']"in b,'original full bounded SHA comparison uses exact cachedvalue')
# Actual current Common and complete catalog are externally frozen, exact
# old->current JSON views never modify source or fake old physical files.
verify(hf['current_Common_Source_freeze_pin']);verify(hf['current_Common_binding_pin']);verify(hf['current_mount_full_identity_catalog_pin']);binding=load(hf['current_Common_binding_pin']['path']);cat=load(hf['current_mount_full_identity_catalog_pin']['path'])
req(len(binding['fixed_current_pins'])==2012 and len(cat['rows'])==3040,'complete current Common2012/catalog3040 allmandatory scope')
for p in binding['fixed_current_pins']+[r['current_pin']for r in cat['rows']]:verify(p)
maptable={pin_key(r['historical_pin']):r['current_pin']for r in cat['rows']}
def view(v):
 if isinstance(v,dict):
  key=pin_key(v);d={k:view(x)for k,x in v.items()}
  if key in maptable:d.update(maptable[key])
  return d
 if isinstance(v,list):return[view(x)for x in v]
 return v
# Seven external real report/source pin argv arguments strictly preserved.
argv=cli['argv'];req(argv[:12]==['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(NEW/'run_actual_three_plane_pipeline.py')],'CLI originalenv/rootPython/unoptimized singlethread only newnamespace')
for prefix in('a1','a2','a3','build70','seventeen','source-freeze','host-freeze'):
 pp=Path(argv[argv.index('--'+prefix+'-summary')+1]);sha=argv[argv.index('--'+prefix+'-sha256')+1];seven=json.loads(argv[argv.index('--'+prefix+'-seven-id')+1]);p=pin(pp)
 req(p['sha256']==sha and p['identity']==seven,'all external CLI '+prefix+' SHA and all7ID exact')
 d=view(load(pp))
 if prefix in('a1','a2','a3','build70','seventeen'):
  for x in d['fixed_current_pins']+d['output_pins']:verify(x)
  req(d['failure']is None and d.get('after_check_error')is None,'external'+prefix+' actual failure fields match unchanged original Common.closed_report protocol')
 if prefix=='source-freeze':
  for x in d['files']:verify(x)
oldargv=load(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V10_ARGV_20261013.json')['argv'];diff=[i for i,(x,y)in enumerate(zip(oldargv,argv))if x!=y];req(len(oldargv)==len(argv)and len(diff)==4,'CLI precisely four ownhost/freeze path/SHA/all7ID changes')
compilerpin=binding['compiler'];verify(compilerpin);req(compilerpin['path']==compiler and compilerpin['identity'][3]==2,'actual original compiler exactly pinned immutable2links role')
# Failed v10 and readonly fixtures cannot be promoted to real v11 closure.
verify(hf['actual_closed_v10_original_SELF_failure_cause_pin']);verify(hf['actual_closed_v10_true_tool_returns_pin']);verify(hf['readonly_parent_metadata_memory_measurement_pin']);verify(hf['readonly_production_scope_bounded_reader_memory_measurement_pin'])
req(hf['readonly_measurement_not_full_50_stage_runtime_proof']is True and hf['actual_pipeline_executed_by_this_prepare']is False and hf['AAA_qualified']is False and hf['ABA_admitted']is False and hf['goal_complete']is False,'Source/readonly evidence not actual50stage or physics qualification')
# All repeated domains: decks, rows, tolerances, physics sources, release,
# raw runner.records and resources snapshots body identity under exactinverse.
req('len(runner.records)!=50'in b and "sum(x['status']=='PASS'for x in runner.records)!=17"in b and "sum(x['status']=='FAILED'for x in runner.records)!=33"in b,'same required all50/17/33 actual stages')
req('ru_maxrss' in b and not any(x in b for x in('setrlimit','setprofile','malloc_trim'))and '536870912'not in b,'no guard/SELF peak reset or libc reclaim assumption introduced')
for p in sorted(NEW.rglob('*')):
 if p.is_file():pin(p)
req(not (R/'validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11').exists(),'future actualv11 output absent at independentSource review')
result=dict(schema='INDEPENDENT_PIPELINE_V11_CLOSED_ADMISSION_METADATA_COMPLETE_SOURCE_REVIEW_V1',status='INDEPENDENT_SOURCE_ONLY_REVIEW_PASS_NO_ACTUAL_PIPELINE_OR_PHYSICS_QUALIFICATION',check_count=len(checks),unique_current_full_EOF_files=len(full),unique_current_bytes=sum(p['size_bytes']for p in full.values()),total_EOF_read_bytes=read_bytes,original_current_catalog_rows=3040,original_current_Common_fixed_rows=2012,v10_dependencies=278,v11_dependencies=308,actual_SourceHF_pin=hfp,actual_CLI_pin=clip,complete_byte_inverse_pin=pin(NEW/'COMPLETE_V10_TO_V11_CLOSED_METADATA_LIFETIME_BYTE_INVERSE.json'),actual_memory_measurement_pin=memp,deleted_names=del_names,no_future_deleted_report_loads=True,main_row_subscope_and_reassignment_proved=True,all_exact_cached_argv_values_and_order_preserved=True,complete_fixedpin_union_and_wholeEOF_gate_preserved=True,whole_existing_guard_math_oracle_deck_rawrecords_publication_body_preserved=True,three_helpers_whole_byte_equal=True,one_gc_after_closed_admission_beforebusiness=True,compiler_original_exact_immutable_nlink2_pin=compilerpin,all_checks=checks,candidate_imported_or_executed=False,compiler_or_CLE_or_physics_or_business_started=False,author_Source_modified=False,actual_50_17_33_closed0_still_required=True,resource_reclaim_or_original_SELF512_success_not_inferred=True,wall_seconds=time.monotonic()-start,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with(D/'REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],checks=len(checks),unique_EOF_current_files=len(full),unique_current_bytes=result['unique_current_bytes'],SELF_peak_bytes=result['SELF_peak_bytes'],wall_seconds=result['wall_seconds'],review=pin(D/'REVIEW.json'))))

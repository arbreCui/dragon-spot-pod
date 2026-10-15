"""Independent Source and metadata audit; no Host/freezer imports or build calls."""
import ast,copy,hashlib,json,os,shlex,stat,types
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'native_rank1_cache336_build_host_source_v1_20261014'
OUT=R/'independent_native_rank1_cache336_Driver_build_Host_Source_review_20261014'
checks=[];observed={};seven_reobserved=set()
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);a=p.lstat();i=ids(a);assert stat.S_ISREG(a.st_mode)
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==i;raw=f.read();assert ids(os.fstat(f.fileno()))==i
    assert ids(p.lstat())==i
    pf=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i);observed[str(p)]=(pf,raw);return pf,raw
def read(path):
    p,b=pin(path);return json.loads(b),p
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def current7(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and ids(s)==p['identity'],str(q);seven_reobserved.add(str(q))
def funcs(raw):
    text=raw.decode();return {n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
def proof0(t,p):
    a=t['actual_review_return'];return t['observed_closed']is True and type(a['exit_code'])is int and a['exit_code']==0 and a.get('session_id')is None and norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])==p

ready,pready=read(P/'SOURCE_ONLY_READY.json');plan,pplan=read(P/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json');inv,pinv=read(P/'COMPLETE_COMPACT_BUILD4_TO_CACHE336_DRIVER_HOST_BYTE_INVERSE.json');tools,ptools=read(P/'TRUE_TOOL_RETURNS.json')
host,raw=pin(ready['Host_pin']['path']);prep,prepraw=pin(ready['preparer_pin']['path'])
freezer_path=P/'freeze_driver_cache336_build_host_source_only_v2.py'
freezer,fr=pin(freezer_path);oldfreezer,oldfr=pin(P/'freeze_driver_cache336_build_host_source_only.py')
freezer_inverse_path=P/'COMPLETE_DRIVER336_FREEZER_V1_TO_V2_CLI_GATE_BYTE_INVERSE.json'
freezer_inverse,pfi=read(freezer_inverse_path)
helper,hraw=pin(R/'prepare_native_rank1_cache336_source_v1_20261014.py')
for source in (raw,prepraw,fr,oldfr,hraw):ast.parse(source)
check('exact ready/plan/host/inverse/preparer roles',ready['Host_pin']==host and ready['plan_pin']==pplan and ready['whole_byte_inverse_pin']==pinv and ready['preparer_pin']==prep and plan['Source_Host_pin']==host and plan['Source_inverse_pin']==pinv and plan['preparer_pin']==prep)
check('explicit future plan/ready absence',all(plan[k]is None for k in ('actual_new_Driver_object_pin','actual_new_Dragon_pin','actual_new_build_report_pin'))and ready['final_Host_freeze_pin']is None and ready['actual_new_build_report_pin']is None)
check('no actual output/HF/CLI yet',not Path(plan['planned_output_root']).exists()and not (P/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json').exists()and not (P/'ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json').exists())
check('actual Source preparation terminal0',tools['observed_closed']is True and type(tools['actual_corrected_source_preparation_return']['exit_code'])is int and tools['actual_corrected_source_preparation_return']['exit_code']==0 and tools['actual_corrected_source_preparation_return'].get('session_id')is None)
recovered=raw.decode().splitlines(keepends=True)
for block in reversed(inv['blocks']):
    i=block['new_start_line'];b=block['new'].splitlines(keepends=True);check('exact inverse Host block '+str(i),recovered[i:i+len(b)]==b);recovered[i:i+len(b)]=block['old'].splitlines(keepends=True)
original,originalraw=pin(inv['original_host_pin']['path']);check('Host whole byte inverse exact old build4',original==inv['original_host_pin']and ''.join(recovered).encode()==originalraw and inv['candidate_host_pin']==host)
# Reverse the exact comparison gate and block move; never import either freezer.
frecovered=fr.decode();check('freezer exact new gate once',frecovered.count(freezer_inverse['gate_new'])==1)
frecovered=frecovered.replace(freezer_inverse['gate_new'],freezer_inverse['gate_old'])
block=freezer_inverse['moved_exact_block'];anchor=freezer_inverse['original_block_anchor']
check('freezer moved block exact once',frecovered.count(block)==1 and frecovered.count(anchor)==1)
frecovered=frecovered.replace(block,'').replace(anchor,anchor+block)
check('freezer whole inverse exact original v1',frecovered.encode()==oldfr and freezer_inverse['original_freezer_pin']==oldfreezer and freezer_inverse['new_freezer_pin']==freezer)
hfuns=funcs(raw);ofuns=funcs(originalraw)
for n in ('load_common','unique','rewrite_summary'):check('unchanged whole function '+n,hfuns[n]==ofuns[n])
check('same firstfailure capture and publication protection',raw[raw.index(b'    failure = None\n'):].replace(b"zip(('compile_Driver','link_Dragon'),planned)",b"zip(('compile_BOOTQ','link_Dragon'),planned)").count(b'raise failure.with_traceback(failure_tb)')==1 and b'summary = None\n    try:\n        summary = dict'in raw and b"secondary.append(dict(where='failed_report_publication'"in raw)
check('original resource supervisor Common and guards kept',b"c.initialize(OUT,start)"in raw and b"type(runner) is not full.OwnRSSSerialExecutor"in raw and b"runner.resources is not resources"in raw and b"600)"in raw and b"1800-(time.monotonic()-start)"in raw and b"before['artifact_bytes']+20971764748+64*2**20+2*2**30 >= 96*2**30"in raw)
base,pbase=read(plan['original_actual_complete70_report_pin']['path']);oldhf,poldhf=read(plan['selected_previous_complete70_Host_freeze_pin']['path']);oldsf,poldsf=read(plan['selected_previous_compact_Fortran_Source_freeze_pin']['path']);oldcli,poldcli=read(R/'bq64_compact_expected_build_host_source_v4_20261013/ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json')
rt,prt=read(R/'ROOT_ACTUAL_COMPACT_BQ_BUILD_V4_TRUE_TOOL_RETURNS_20261013.json');post,ppost=read(R/'independent_bq64_compact_build_v4_actual_postverify_20261013/REVIEW.json');postt,ppostt=read(R/'independent_bq64_compact_build_v4_actual_postverify_20261013/TRUE_TOOL_RETURNS.json')
check('real predecessor current bound fullPF',pbase==plan['original_actual_complete70_report_pin']and poldhf==plan['selected_previous_complete70_Host_freeze_pin']and poldsf==plan['selected_previous_compact_Fortran_Source_freeze_pin']and poldcli==post['actual_build_CLI_pin']and post['actual_build_report_pin']==pbase and post['actual_build_true_tool_return_pin']==prt and proof0(postt,ppost))
t=rt['actual_terminal_return'];check('actual compact70 genuine closed2 and Source/HF',type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and post['actual_genuine_terminal_integer_exit_code']==0 and len(base['records'])==2 and all(x['status']=='PASS'for x in base['records'])and base['failure']is None and base['after_check_error']is None and base['actual_host_Source_freeze_pin']==poldhf and base['actual_new_Source_freeze_pin']==poldsf and base['final_report_resource_check_passed']is True)
check('whole original2565 complete closure current7 inherited',len(oldhf['dependencies'])==2565)
allrows=oldhf['dependencies']+base['fixed_current_pins']+base['output_pins']+plan['original_ordered70_input_pins']+plan['current_nine_core_object_pins']+plan['historical_original_nine_core_object_pins']
table={}
for p in allrows:
    p=norm(p)
    if p['path']in table:assert table[p['path']]==p,'inconsistent repeated selected PF '+p['path']
    else:table[p['path']]=p;current7(p)
old70=plan['original_ordered70_input_pins'];current9=plan['current_nine_core_object_pins'];historical9=plan['historical_original_nine_core_object_pins']
check('exact70/current9/old9 and source roles',len(old70)==70 and len({x['path']for x in old70})==70 and len(current9)==len(historical9)==9 and current9[:5]+current9[6:]==historical9[:5]+historical9[6:]and current9[5]==plan['retained_current_BOOTQ_object_pin']==old70[40]and old70[37]==plan['original_Driver_object_pin']and old70[57]==plan['unchanged_SPOT1P64_object_pin']and [p['path']for p in old70]==base['actual_complete70_link_inputs'])
for key in ('original_Driver_Source_pin','unchanged_SPOT1P64_Source_pin'):current7(plan[key])
common,pcommon=read(plan['selected_new_Common_Source_freeze_pin']['path']);check('exact new Common Source freeze',pcommon==plan['selected_new_Common_Source_freeze_pin']and pcommon['sha256']=='e2b380b7acf9d0d550adf260420454f2a08f16380e41f1d66bd6b7f678aae5d9')
for p in common['files']+common['original_source_metadata_pins']:current7(p)
ns={'Path':Path,'OUT':Path(plan['planned_output_root']),'SOURCE':Path(plan['selected_new_Fortran_Source_freeze_path']).parent}
node=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)and n.name=='commands');exec(compile(ast.Module(body=[node],type_ignores=[]),'<extracted-real-commands-Source>','exec'),ns)
c=types.SimpleNamespace(FLAGS=plan['original_compile_flags']);positive=ns['commands'](c,base,plan)
check('real extracted pure commands one compile/one link only',len(positive)==2 and positive[0][-4:]==['-c',str(ns['SOURCE']/'SPOT_GLOBAL_NATIVE_DRIVER64.f'),'-o',str(ns['OUT']/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')]and positive[1][3:-2][:37]+positive[1][3:-2][38:]==[x['path']for x in old70[:37]+old70[38:]]and positive[1][3:-2][37]==str(ns['OUT']/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'))
rejected=[]
for name in ('orderedinput','Driverindex','compiler','flags','includes','linkprefix','inputcount','archive'):
    b=copy.deepcopy(base);p=copy.deepcopy(plan)
    if name=='orderedinput':p['original_ordered70_input_pins'][0],p['original_ordered70_input_pins'][1]=p['original_ordered70_input_pins'][1],p['original_ordered70_input_pins'][0]
    elif name=='Driverindex':p['original_Driver_object_pin']['path']='wrong.o'
    elif name=='compiler':p['original_compiler_pin']['path']='wrong-compiler'
    elif name=='flags':p['original_compile_flags'][0]='wrong-flag'
    elif name=='includes':p['original_compile_include_arguments'][0]='-Iwrong'
    elif name=='linkprefix':b['records'][-1]['command'][1]='-O3';p['original_complete70_link_command']=copy.deepcopy(b['records'][-1]['command'])
    elif name=='inputcount':p['original_ordered70_input_pins'].pop()
    elif name=='archive':b['records'][-1]['command'][-3]='wrong.o';p['original_complete70_link_command']=copy.deepcopy(b['records'][-1]['command']);p['original_ordered70_input_pins'][-1]['path']='wrong.o'
    try:ns['commands'](c,b,p)
    except RuntimeError:rejected.append(name)
    else:raise AssertionError('pure commands must reject '+name)
check('all eight pure Source command refusals',len(rejected)==8)
check('freezer complete own and inherited/current Source closure',b"rows=oldhf['dependencies']+"in fr and b"+old['fixed_current_pins']+old['output_pins']+own+[pr,pt,psf,pcommon]"in fr and b"sf['exact_source_evidence_pins']"in fr and b"common['original_source_metadata_pins']"in fr and b"s.identity(st)!=row['identity']"in fr)
check('freezer strict peer typed0/exactstdoutPF and ownfile inclusion',b"type(actual.get('exit_code')) is int"in fr and b"actual.get('session_id') is None"in fr and b"json.loads(lines[-1]).get('review_pin')!=review_pin"in fr and b"if not found(review,row)"in fr)
check('freezer v2 actual oldCLI exact PF prewrite',fr.index(b"oldpost['actual_build_CLI_pin']")<fr.index(b'phf=s.put(HF,data)')and fr.index(b"argv[:9]!=")<fr.index(b'phf=s.put(HF,data)'))
check('Source helper import has no module-level operations',all(not isinstance(n,ast.Expr)or isinstance(n.value,ast.Constant)for n in ast.parse(hraw).body))
argv=list(oldcli['argv'][:12]);argv[-1]=host['path']
check('exact original12 env/interpreter prefix except Host',len(argv)==12 and argv[:-1]==oldcli['argv'][:11]and argv[:9]==['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1'])
for p,_ in observed.values():current7(p)
OUT.mkdir(exist_ok=False)
report=dict(schema='INDEPENDENT_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_REVIEW_V1',status='PASS_CACHE336_DRIVER_ONLY_BUILD_HOST_AND_V2_FREEZER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,Host_imported=False,Host_main_executed=False,freezer_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,manifest_prepared=False,current_host_pin=host,actual_plan_pin=pplan,actual_ready_pin=pready,actual_host_inverse_pin=pinv,actual_preparer_pin=prep,actual_Source_preparation_true_tools_pin=ptools,actual_final_freezer_pin=freezer,historical_freezer_v1_pin=oldfreezer,actual_freezer_inverse_pin=pfi,actual_Source_helper_pin=helper,selected_original_host_pin=original,selected_actual_complete70_report_pin=pbase,selected_original_Host_freeze_pin=poldhf,selected_original_compact_Fortran_Source_freeze_pin=poldsf,selected_original_CLI_pin=poldcli,selected_actual_Root_tools_pin=prt,selected_independent_actual_postreview_pin=ppost,selected_independent_actual_posttools_pin=ppostt,selected_new_Common_Source_freeze_pin=pcommon,base_dependency_count=2565,current_unique_complete_base_rows=len(table),all_inherited_seven_fields_current=True,science_fullEOF_not_repeated=True,exact_driver_replacement_index=37,retained_BOOTQ_index=40,retained_SPOT1P64_index=57,retained_other_input_count=69,current9_all_retained=True,historical9_retained_as_history=True,archives_retained=4,original_resources_unchanged=plan['original_caps'],Host_whole_byte_inverse_blocks=len(inv['blocks']),original_FirstFailure_capture_and_publication_retained=True,pure_real_command_fixture_positive=1,pure_real_command_fixture_rejections=rejected,pure_fixture_is_not_compiler_or_actual_qualification=True,planned_compile_and_link_commands=positive,planned_exact_original_env_prefix=argv,future_new_Fortran_Source_freeze_pin=None,future_own_Host_freeze_pin=None,future_own_CLI_pin=None,future_actual_build_report_pin=None,all_file_descriptors_closed=True,checks=checks)
path=OUT/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
with os.fdopen(fd,'w')as f:json.dump(report,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
pf,_=pin(path);print(json.dumps(dict(status=report['status'],review_pin=pf,failure=None,source_only=True,compiler_executed=False,numerical_executed=False),ensure_ascii=False))

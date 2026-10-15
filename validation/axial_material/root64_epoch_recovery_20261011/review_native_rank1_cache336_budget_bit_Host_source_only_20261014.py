"""Read Source/metadata and extract finite pure functions; never import or run Hosts."""
import argparse,ast,copy,hashlib,json,os,stat,types
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'native_rank1_cache336_budget_bit_control_host_source_v1_20261014'
OUT=R/'independent_native_rank1_cache336_budget_bit_Host_Source_review_20261014'
checks=[];observed={};seven=set()
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);s=p.lstat();i=ids(s);assert stat.S_ISREG(s.st_mode)
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==i;b=f.read();assert ids(os.fstat(f.fileno()))==i
    assert ids(p.lstat())==i;v=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i);observed[str(p)]=(v,b);return v,b
def read(path):
    p,b=pin(path);return json.loads(b),p
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def current7(p):
    s=Path(p['path']).lstat();assert stat.S_ISREG(s.st_mode)and ids(s)==p['identity'],p['path'];seven.add(p['path'])
def check(n,v):
    if not v:raise AssertionError(n)
    checks.append(n)
def segments(raw):
    text=raw.decode();return{n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--freezer',required=True);a=ap.parse_args()
    ready,pr=read(P/'SOURCE_ONLY_READY.json');plan,pp=read(P/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json');inv,pi=read(P/'COMPLETE_MODEL5_TO_CACHE336_BUDGET_BIT_HOST_WHOLE_BYTE_INVERSE.json');tools,pt=read(P/'TRUE_TOOL_RETURNS.json')
    host,raw=pin(ready['Host_pin']['path']);prep,praw=pin(ready['preparer_pin']['path']);freezer,fraw=pin(a.freezer)
    oldfreezer,oldfraw=pin(P/'freeze_cache336_budget_bit_control_host_source_only.py');syntax,psyntax=read(P/'COMPLETE_CACHE336_BIT_FREEZER_V1_TO_V2_AST_SYNTAX_BYTE_INVERSE.json')
    recovered_freezer=fraw.decode()
    for b in reversed(syntax['blocks']):
        check('freezer exact syntax inverse block once',recovered_freezer.count(b['new'])==1);recovered_freezer=recovered_freezer.replace(b['new'],b['old'])
    check('freezer whole syntax inverse v1 retained',recovered_freezer.encode()==oldfraw and syntax['old_freezer_pin']==oldfreezer and syntax['new_freezer_pin']==freezer)
    try:ast.parse(oldfraw)
    except SyntaxError:check('historical v1 Source syntax failure never execution',True)
    else:raise AssertionError('historical v1 expected parse failure')
    for b in (raw,praw,fraw):ast.parse(b)
    check('all own ready/plan/Host/inverse/preparer PF exact',host==ready['Host_pin']==plan['Source_Host_pin']and pp==ready['plan_pin']and pi==ready['inverse_pin']==plan['Source_inverse_pin']and prep==ready['preparer_pin']==plan['preparer_pin'])
    t=tools['actual_source_preparation_return'];check('Source preparation genuine integer0 closed',tools['observed_closed']is True and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None)
    rec=raw.decode().splitlines(keepends=True)
    for b in reversed(inv['blocks']):
        i=b['new_start_line'];n=b['new'].splitlines(keepends=True);check('exact whole inverse block '+str(i),rec[i:i+len(n)]==n);rec[i:i+len(n)]=b['old'].splitlines(keepends=True)
    oldhost,oldraw=pin(inv['original_host_pin']['path']);check('whole Model5 Source inverse exact',oldhost==inv['original_host_pin']and inv['candidate_host_pin']==host and ''.join(rec).encode()==oldraw)
    fs=segments(raw);osrc=segments(oldraw)
    same_names=['load_common','rewrite_summary','unique','safe_repr','FirstFailure','direct_aux_inventory','ControlsResources','log_rows','public_oracle']
    for n in same_names:check('unchanged whole low-level Source '+n,fs[n]==osrc[n])
    check('immutable KIND cache336 and unchanged aux128+8',b"KIND='cache336'"in raw and b'AUX_CAP=128*2**20'in raw and b'AUX_PENDING=8*2**20'in raw)
    check('phase directory before real supervisor',raw.index(b"(OUT/('compact-'+KIND+'-controls')).mkdir()")<raw.index(b'runner=full.OwnRSSSerialExecutor'))
    check('compile only control.o no module rebuild',b"sorted(p.name for p in (OUT/'build').iterdir())!=['control.o']"in raw and b"expected_count=3 if KIND=='cache336'else 11"in raw and b"record=run(cwd,'run_budget_bits',[exe])"in raw)
    check('exact old resource acceptance and dynamic reserve retained',b"before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30"in raw and b"whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20"in raw and b"run(cwd,label,command)"in raw and b'runner.execute(cwd,label,command,600)'in raw)
    check('both selected ownHF top-level PF same dependencies and base fixed',b"hf.get('selected_new_build_Host_freeze_pin')"in raw and b"hf.get('selected_new_Fortran_Source_freeze_pin')"in raw and b"selected.get('path')!=plan[key+'_path']"in raw and b"hf_table.get(selected['path'])!=selected"in raw and b"base_fixed_table.get(row['path'])!=row"in raw and b'psf!=selected_fortran_sf'in raw)
    check('strict closed2 Driver37 premise and retained9/69 flags',b"c.closed_report(base,helper,Path(pbase['path']).parent,2)"in raw and b"replacement_zero_based_complete70_input_index')!=37"in raw and b"'current_nine_core_objects_identical_and_retained'"in raw and b"'new_cache_budget_component_control_qualification'"in raw)
    check('all first failures preserved through report publication',b"except BaseException as error:first.capture(error,'execute_or_oracle')"in raw and b"except BaseException as error:first.capture(error,'after_check')"in raw and b"first.capture(error,'publication')"in raw and b"first.capture(late,'failed_report_publication')"in raw and b'first.reraise()'in raw and b'summary=None\n    try:\n        summary=dict'in raw)
    check('future planned actual pins explicit None',all(plan[k]is None for k in ('future_actual_new_build70_report_pin','future_actual_control_object_pin','future_actual_control_executable_pin','future_actual_control_report_pin'))and all(ready[k]is None for k in ('future_own_HF_pin','future_own_CLI_pin','future_actual_control_report_pin')))
    check('planned selected buildHF/SF two unique namespaces',plan['selected_new_build_Host_freeze_pin_path']==str(R/'native_rank1_cache336_build_host_source_v1_20261014/COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json')and plan['selected_new_Fortran_Source_freeze_pin_path']==plan['selected_control_Source_freeze_path']==str(R/'native_rank1_exact_cache336_source_v1_20261014/COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'))
    check('counts stages scopes exactly Source plan',plan['guarded_stages']==3 and plan['expected_actual_assertions']==338 and plan['expected_actual_SPOT1P64_calls']==121 and plan['original_assertions']==301 and plan['additional_assertions']==37 and plan['original_math_module_recompiled']is False and plan['component_only']is True and plan['reader_qualified']is False and plan['physics_qualified']is False)
    check('actual OUT and ownHFCLI remain absent',not Path(plan['planned_output_root']).exists()and not (P/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json').exists()and not (P/'DECLARED_EXECUTION_INTERFACE.json').exists())
    buildplan,pbp=read(plan['current_predecessor_build_plan_pin']['path']);check('exact predecessor Source build PLAN',pbp==plan['current_predecessor_build_plan_pin'])
    check('retained math57/current9/compiler includes/archive authority',plan['unchanged_math_object_pin']==buildplan['original_ordered70_input_pins'][57]and plan['unchanged_math_Source_pin']==buildplan['unchanged_SPOT1P64_Source_pin']and plan['current_nine_core_pins']==buildplan['current_nine_core_object_pins']and plan['original_ordered70_paths']==[x['path']for x in buildplan['original_ordered70_input_pins']]and plan['original_four_archive_paths']==[x['path']for x in buildplan['original_ordered70_input_pins']if x['path'].endswith('.a')]and plan['original_compile_flags']==buildplan['original_compile_flags']and plan['original_compile_include_arguments']==buildplan['original_compile_include_arguments']and plan['original_caps']==buildplan['original_caps'])
    for p in buildplan['original_ordered70_input_pins']+buildplan['current_nine_core_object_pins']+[plan['control_Source_pin'],plan['production_Source_pin'],plan['unchanged_math_Source_pin']]:current7(p)
    model,pmodel=read(plan['current_unchanged_model5_Host_freeze_pin']['path']);check('original model5 HF selected exact',pmodel==plan['current_unchanged_model5_Host_freeze_pin']and len(model['dependencies'])==2597)
    for p in model['dependencies']+[model['host_source']]:current7(p)
    common,pcommon=read(plan['selected_new_Common_Source_freeze_pin']['path']);check('selected Common SF exact',pcommon==plan['selected_new_Common_Source_freeze_pin'])
    for p in common['files']+common['original_source_metadata_pins']:current7(p)
    # Only these real functions/classes are evaluated. All supplied observations are synthetic dictionaries.
    ns={'Path':Path,'OUT':Path(plan['planned_output_root']),'KIND':'cache336'}
    selected=[n for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name in ('safe_repr','FirstFailure','model_oracle','make_commands')]
    exec(compile(ast.Module(body=selected,type_ignores=[]),'<real-Source-finite-contract-functions>','exec'),ns)
    seen_calls=[]
    def fake_same(path,p):
        if path!=plan['unchanged_math_object_pin']['path']or p!=plan['unchanged_math_object_pin']:raise RuntimeError('fake exact math identity')
        seen_calls.append((path,p))
    c=types.SimpleNamespace(FLAGS=plan['original_compile_flags'],same_pin=fake_same)
    fake_new=list(plan['original_ordered70_paths']);fake_new[37]=plan['new_build_expected_Driver_object_path']
    fake_compile=[plan['original_compiler_pin']['path'],*c.FLAGS,*plan['new_build_compile_include_arguments'],'-J'+plan['new_build_expected_build_directory'],'-c',plan['production_Source_pin']['path'],'-o',plan['new_build_expected_Driver_object_path']]
    fake_base={'records':[{'command':fake_compile},{'command':[plan['original_compiler_pin']['path'],'-O2','-ffp-contract=off',*fake_new,'-o',plan['new_build_expected_Dragon_path']]}],'actual_complete70_link_inputs':fake_new}
    commands=ns['make_commands'](c,fake_base,plan,plan['control_Source_pin'])
    check('real pure commands compile/link exactly one retained math plus original four libraries',commands[0][-4:]==['-c',plan['control_Source_pin']['path'],'-o',str(ns['OUT']/'build/control.o')]and commands[1][3:-2]==[str(ns['OUT']/'build/control.o'),plan['unchanged_math_object_pin']['path'],*plan['original_four_archive_paths']]and commands[3]==[plan['unchanged_math_object_pin']['path']]and seen_calls)
    refused=[]
    for name in ('Driverindex','compileflags','compileSource','linkorder','linkoutput','mathindex','mathidentity','inputcount'):
        b=copy.deepcopy(fake_base);p=copy.deepcopy(plan)
        if name=='Driverindex':b['actual_complete70_link_inputs'][37]='wrong.o'
        elif name=='compileflags':b['records'][0]['command'][1]='-O3'
        elif name=='compileSource':b['records'][0]['command'][-3]='wrong.f'
        elif name=='linkorder':b['records'][1]['command'][3:5]=reversed(b['records'][1]['command'][3:5])
        elif name=='linkoutput':b['records'][1]['command'][-1]='wrongDragon'
        elif name=='mathindex':p['unchanged_math_object_pin']['path']='wrongmath.o'
        elif name=='mathidentity':p['unchanged_math_object_pin']['sha256']='0'*64
        else:b['actual_complete70_link_inputs'].pop()
        try:ns['make_commands'](c,b,p,p['control_Source_pin'])
        except RuntimeError:refused.append(name)
        else:raise AssertionError('expected pure command refusal '+name)
    scope=('formal_SN32_quadrature_equivalence','genuine_solver_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete')
    legal=dict(status='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY',actual_assertions=338,actual_SPOT1P64_calls=121,**{k:False for k in scope})
    def oracle(rows):
        ns['log_rows']=lambda c,root,record:(rows,{'path':'fake-memory-log'})
        return ns['model_oracle'](c,Path('/fake-memory-only'),{},Path('/fake-memory-only'))
    check('pure Source oracle accepts exact338/121 false scopes',oracle([legal])['actual_assertions']==338)
    oracle_reject=[]
    variants=[]
    for key,value in [('actual_assertions',337),('actual_assertions',True),('actual_assertions',338.0),('actual_SPOT1P64_calls',120),('actual_SPOT1P64_calls','121')]+[(k,True)for k in scope]:
        d=copy.deepcopy(legal);d[key]=value;variants.append((key+':'+str(value),[d]))
    missing=copy.deepcopy(legal);del missing['goal_complete'];variants+=[('missing false field',[missing]),('duplicate terminal',[legal,legal]),('no terminal',[])]
    for name,rows in variants:
        try:oracle(rows)
        except RuntimeError:oracle_reject.append(name)
        else:raise AssertionError('expected pure oracle refusal '+name)
    first=ns['FirstFailure']();primary=RuntimeError('fake primary');secondary=RuntimeError('fake secondary')
    try:raise primary
    except RuntimeError as e:first.capture(e,'first');saved=first.traceback
    first.capture(secondary,'after');check('pure FirstFailure keeps exact first object/tb',first.error is primary and first.traceback is saved and len(first.secondary)==1)
    try:first.reraise()
    except RuntimeError as e:check('pure FirstFailure raises original object',e is primary)
    else:raise AssertionError('FirstFailure must raise')
    # Freezer static contract: no generated authority or execution is accepted here.
    check('freezer strict peer typed0/no session/closedtrue/exactstdoutPF and all own7',b"type(actual.get('exit_code')) is not int"in fraw and b"actual.get('session_id') is not None"in fraw and b"receipt.get('observed_closed') is not True"in fraw and b"json.loads(lines[-1]).get('review_pin')!=pr"in fraw and b"if not found(review,row)"in fraw)
    check('freezer future actual build/report pins explicit None before publication',b"if key not in plan or plan[key] is not None"in fraw and b"future_actual_new_build70_report_pin=None"in fraw and b"future_actual_control_report_pin=None"in fraw)
    check('freezer full DriverHF and model5 dependencies+shared SF+Common closure current7',b"rows=(bhf['dependencies']+predecessor['dependencies']+"in fraw and b"sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins']+common['files']+common['original_source_metadata_pins']"in fraw and b"s.identity(st)!=row['identity']"in fraw)
    check('freezer selected DriverHF itself binds exact shared SF',b"bhf['selected_new_Fortran_Source_freeze_pin']!=psf"in fraw and b"if psf not in bhf['dependencies']"in fraw and b"plan['control_Source_pin'] not in sf['files']"in fraw and b"plan['production_Source_pin'] not in sf['files']"in fraw and b"sf['new_control_expected_assertions']!=338"in fraw and b"sf['new_control_expected_calls']!=121"in fraw)
    check('freezer Source CLI retains30 argv and requires future actual report externally',b"planned_total_argv_count=30"in fraw and b"required_external_prefixes=['new-build70','source-freeze','host-freeze']"in fraw and b"mandatory_source_bindings=dict(source_freeze=psf,host_freeze=phf)"in fraw and b"initial_fullfresh2_cold_meta_history96_reserve_required=True"in fraw)
    for p,_ in observed.values():current7(p)
    OUT.mkdir(exist_ok=False)
    report=dict(schema='INDEPENDENT_CACHE336_BUDGET_BIT_HOST_SOURCE_ONLY_REVIEW_V1',status='PASS_CACHE336_THREE_STAGE_BUDGET_BIT_HOST_AND_FREEZER_SOURCE_REVIEW',failure=None,source_only=True,business_executed=False,Host_imported=False,Host_main_executed=False,freezer_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,science_fullEOF_repeated=False,all_file_descriptors_closed=True,current_host_pin=host,actual_plan_pin=pp,actual_ready_pin=pr,actual_inverse_pin=pi,actual_preparer_pin=prep,actual_Source_preparation_true_tools_pin=pt,actual_final_freezer_pin=freezer,historical_freezer_v1_pin=oldfreezer,actual_freezer_v1_to_v2_inverse_pin=psyntax,historical_model5_host_pin=oldhost,selected_predecessor_build_plan_pin=pbp,selected_model5_HF_pin=pmodel,selected_new_Common_Source_freeze_pin=pcommon,all_selected_current7_count=len(seven),whole_byte_inverse_block_count=len(inv['blocks']),whole_low_level_methods_same=same_names,original_resources_and_aux_caps=plan['original_caps'],aux_bytes=128*2**20,pending_bytes=8*2**20,planned_stages=3,actual_control_Source_pin=plan['control_Source_pin'],actual_production_Source_pin=plan['production_Source_pin'],retained_math_object_pin=plan['unchanged_math_object_pin'],retained_math_Source_pin=plan['unchanged_math_Source_pin'],retained_four_archive_paths=plan['original_four_archive_paths'],finite_functions_extracted_from_exact_Host_Source=True,pure_fake_memory_fixture_is_not_actual_control_or_qualification=True,pure_command_positive=1,pure_command_rejections=refused,pure_oracle_positive=1,pure_oracle_rejections=oracle_reject,pure_FirstFailure_original_object_and_tb=True,future_actual_build_report_pin=None,future_actual_control_report_pin=None,future_own_HF_pin=None,future_own_CLI_pin=None,original301_and110_math_control_not_reaudited_here=True,expected_actual_assertions=338,expected_actual_SPOT1P64_calls=121,checks=checks)
    path=OUT/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'w')as f:json.dump(report,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    review,_=pin(path);print(json.dumps(dict(status=report['status'],review_pin=review,failure=None,source_only=True,compiler_executed=False,numerical_executed=False),ensure_ascii=False))
if __name__=='__main__':main()

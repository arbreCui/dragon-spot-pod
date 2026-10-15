"""Author the exact three-file cleanup Source only; never import candidates or prepare a MF."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
A=Path('/Users/wen/spot/validation/artifacts')
OLD=R/'storage_release_literal5_closed_failed_v15_private_source_v1_20261014'
OUT=R/'storage_release_literal3_closed_failed_v15_private_source_v1_20261014'

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata only')
    b=p.read_bytes()
    if identity(p.lstat())!=identity(s)or len(b)!=s.st_size:raise RuntimeError('Source/metadata changed')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def write(p,b):
    if isinstance(b,str):b=b.encode()
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def dump(p,v):write(p,json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def inventory(root):
    files={};dirs={};links={};stack=[root]
    while stack:
        p=stack.pop();s=p.lstat();before=identity(s)
        if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary existing owner root')
        dirs[str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=before:raise RuntimeError('owner directory opened7')
            with os.scandir(fd)as it:
                for e in it:
                    q=p/e.name;z=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(z.st_mode):stack.append(q)
                    elif stat.S_ISREG(z.st_mode):files[str(q)]=identity(z)
                    elif stat.S_ISLNK(z.st_mode):links[str(q)]=dict(identity=identity(z),target=os.readlink(q))
                    else:raise RuntimeError('owner special entry')
            if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('owner directory changed')
        finally:os.close(fd)
    return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)

def main():
    if OUT.exists():raise RuntimeError('unique Source namespace, no retry/overwrite')
    oldsf=read(OLD/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json')
    oldtext=(OLD/'literal5_release_common.py').read_text();tree=ast.parse(oldtext);constants={}
    for n in tree.body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:constants[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    for p in oldsf['Source_pins']:
        if pin(p['path'])!=p:raise RuntimeError('old strict three-script Source authority')
    v15=constants['CLOSED_V15'];v15summary=read(v15['summary_pin']['path']);v15root=Path(v15['actual_output_root'])
    targets=[next(p for p in v15summary['output_pins']if p['path']==str(v15root/'AAA'/n))for n in('global.xsm','BOOT-GLOBAL64-STAGE.xsm','initial_pack.xsm')]
    if sum(p['size_bytes']for p in targets)!=1504027360:raise RuntimeError('exact original literal3 bytes')
    for p in targets:
        s=Path(p['path']).lstat()
        if identity(s)!=p['identity']or not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('exact current target all7 UID singlelink')
    previous=read(OLD/'EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json');indices=[4465,4471,4496]
    if len(previous['current_protected_full_EOF_pins'])!=7567 or {previous['current_protected_full_EOF_pins'][i]['path']:previous['current_protected_full_EOF_pins'][i]for i in indices}!={p['path']:p for p in targets}:raise RuntimeError('only exact literal3 old MF rows')
    postpath=R/'independent_v16_actual_full50_BOOT_failure_postverify_20261014/REVIEW.json';post=read(postpath)
    if post['schema']!='READONLY_ACTUAL_V16_FULL50_ENGINEERING_POSTVERIFICATION_V1'or post['status']!='REPORTED_ACTUAL_V16_FAILURE_UNQUALIFIED'or post['actual_Root_exit_code']!=1:raise RuntimeError('real failed-v16 post metadata')
    v16=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=pin(postpath),independent_posttools_pin=pin(postpath.parent/'TRUE_TOOL_RETURNS.json'),full_raw_records_pin=post['raw_execution_records_pin'],stages_pin=post['actual_stages_pin'],actual_output_root=str(Path(post['actual_report_pin']['path']).parent),actual_status='FAILED_UNQUALIFIED_NO_RETRY',actual_failure=post['failure'],actual_record_count=50,actual_PASS_records=16,exact_expected_refusal_records=33,actual_fixed_count=3129,actual_output_count=296,actual_physical_scene_count=297,actual_owned_count=187,actual_HF_dependency_count=2920)
    vt=read(v16['Root_true_tool_pin']['path']);pt=read(v16['independent_posttools_pin']['path']);vs=read(v16['summary_pin']['path'])
    if type(vt['actual_terminal_return']['exit_code'])is not int or vt['actual_terminal_return']['exit_code']!=1 or vt['actual_terminal_return'].get('session_id')is not None or vt['observed_closed']is not True:raise RuntimeError('genuine failed closed Root terminal')
    if type(pt['actual_review_return']['exit_code'])is not int or pt['actual_review_return']['exit_code']!=0 or pt['actual_review_return'].get('session_id')is not None or pt['observed_closed']is not True:raise RuntimeError('genuine independent readonly failed post0')
    if len(vs['fixed_current_pins'])!=3129 or len(vs['output_pins'])!=296 or len(vs['owned_runtime_pins'])!=187 or vs['engineering_three_plane_closed0']is not False:raise RuntimeError('actual failed v16 counts only')
    historical=dict(constants['HISTORICAL_PINS'])
    historical.update(previous_literal5_Source_freeze=pin(OLD/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json'),previous7567_manifest=pin(OLD/'EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json'),completed_actual_literal5_release=pin(R/'storage_release_literal5_closed_failed_v15_private_actual_receipts_20261014/ACTUAL_EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_OLD_PRIVATE_RELEASE_RECEIPT.json'),completed_independent_literal5_postreview=pin(R/'independent_literal5_actual_exact_release_postverify_20261014/REVIEW.json'),completed_independent_literal5_posttools=pin(R/'independent_literal5_actual_exact_release_postverify_20261014/TRUE_TOOL_RETURNS.json'),literal3_role_survey_tools=pin(R/'ACTUAL_OLD_FAILED_V15_LITERAL3_ROLE_SURVEY_TRUE_TOOL_RETURN_20261014.json'),literal3_budget_survey=pin(R/'readonly_post_v16_initial_fullfresh2_budget_and_literal3_roles_20261014/REVIEW.json'),literal3_budget_survey_tools=pin(R/'readonly_post_v16_initial_fullfresh2_budget_and_literal3_roles_20261014/TRUE_TOOL_RETURNS.json'))
    historical.update({'closed_v16_'+k:v for k,v in v16.items()if isinstance(v,dict)and 'path'in v})
    selections=[x for x in constants['CURRENT_SELECTIONS']if x['role']!='public5_failed']
    for role,folder,reportpath,hfname in [('Driver2','native_rank1_cache336_build_host_source_v2_20261014',A/'axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v2/Root_actual_build_only_summary.json','COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json'),('bit2','native_rank1_cache336_budget_bit_control_host_source_v2_20261014',A/'axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v2/Root_actual_control_summary.json','COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')]:
        d=read(reportpath);hp=pin(R/folder/hfname);h=read(hp['path']);cp=pin(R/folder/('ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json'if role=='Driver2'else'DECLARED_EXECUTION_INTERFACE.json'))
        selections.append(dict(role=role,Host_freeze_pin=hp,actual_report_pin=pin(reportpath),exact_cli_pin=cp,expected_dependency_count=len(h['dependencies']),actual_fixed_count=len(d['fixed_current_pins']),actual_output_count=len(d['output_pins']),actual_status=d['status'],actual_failure=d['failure'],actual_output_root=str(reportpath.parent)))
    before=inventory(v15root)
    if len(before['ordinary_file_identities'])!=192 or before['symlinks']:raise RuntimeError('actual current failed v15 complete192')
    current=oldtext;changes=[]
    def change(old,new):
        nonlocal current
        if current.count(old)!=1:raise RuntimeError('exact unique Source splice')
        current=current.replace(old,new,1);changes.append(dict(before=old,after=new))
    def assignment(name,value):
        n=next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
        change(ast.get_source_segment(current,n),name+'='+repr(value))
    assignment('HISTORICAL_PINS',historical);assignment('CURRENT_SELECTIONS',selections);assignment('TARGET_SELECTED_PINS',targets);assignment('HISTORICAL_TARGET_INDICES',indices);assignment('BASELINE_OWNED_INVENTORIES',before)
    change("BRANCHES=[Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14'),Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5')]",'BRANCHES=[Path('+repr(str(v15root))+')]')
    change('BYTES=1478165640','BYTES=1504027360')
    change("SOURCE_NAMES=('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py')","SOURCE_NAMES=('literal3_release_common.py','prepare_literal3_manifest.py','verify_or_execute_literal3.py')")
    change("SF=PKG/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json';FINAL=PKG/'EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json';RECEIPTS=REC/'storage_release_literal5_closed_failed_v15_private_actual_receipts_20261014'","SF=PKG/'COMPLETE_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json';FINAL=PKG/'EXACT_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json';RECEIPTS=REC/'storage_release_literal3_closed_failed_v15_private_actual_receipts_20261014'\nCLOSED_V16="+repr(v16))
    oldfn=ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name=='source_gate'))
    newfn=oldfn.replace('literal5','literal3').replace('LITERAL5','LITERAL3').replace('immutable5','immutable3').replace('len(TARGETS)!=5','len(TARGETS)!=3').replace('len(TARGET_PATHS)!=5','len(TARGET_PATHS)!=3').replace("f['closed_failed_v15_authority']!=CLOSED_V15","f['closed_failed_v15_authority']!=CLOSED_V15 or f['closed_failed_v16_authority']!=CLOSED_V16")
    change(oldfn,newfn)
    oldreturn='    return [OWNER,CLOSED_V15]'
    newreturn="""    v=read(CLOSED_V16['summary_pin']);t=read(CLOSED_V16['Root_true_tool_pin']);a=read(CLOSED_V16['Root_exact_argv_pin']);post=read(CLOSED_V16['independent_postreview_pin']);pt=read(CLOSED_V16['independent_posttools_pin']);terminal=t['actual_terminal_return'];pa=pt['actual_review_return']
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['argv']or len(a['argv'])!=90:raise RuntimeError('genuine failed v16 exact90 terminal1 required')
    if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or b.norm(json.loads(pa['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_V16['independent_postreview_pin']:raise RuntimeError('genuine independent failed-v16 readonly post0 required')
    if post['schema']!='READONLY_ACTUAL_V16_FULL50_ENGINEERING_POSTVERIFICATION_V1'or post['status']!='REPORTED_ACTUAL_V16_FAILURE_UNQUALIFIED'or post['failure']!=CLOSED_V16['actual_failure']or post['actual_report_pin']!=CLOSED_V16['summary_pin']or post['actual_Root_true_tool_return_pin']!=CLOSED_V16['Root_true_tool_pin']or post['actual_Root_argv_pin']!=CLOSED_V16['Root_exact_argv_pin']or post['actual_Host_freeze_pin']!=CLOSED_V16['Host_freeze_pin']or post['actual_Root_exit_code']!=1 or post['actual_stage_count']!=50 or post['actual_positive_count']!=16 or post['actual_exact_refusal_count']!=33 or post['actual_fixed_current_count']!=3129 or post['all_fixed_HF2802_377_current7_reobserved_twice']is not True or post['all_current_output_pins_full_EOF_SHA_all7']is not True or post['all_actual_child_watch_limit_failures_absent']is not True or post['actual_unexpected_failed_record_indices']!=[49]or post['actual_engineering_three_plane_closed0']is not False:raise RuntimeError('exact genuine BOOT failure post authority, never engineering PASS')
    if any(post[k]is not False for k in('independent_business_executed','independent_compiler_executed','independent_numerical_executed','independent_deletion_executed')):raise RuntimeError('readonly independent post only')
    if v['status']!='FAILED_UNQUALIFIED_NO_RETRY'or v['failure']!=CLOSED_V16['actual_failure']or v['engineering_three_plane_closed0']is not False or v['actual_terminal']is not None or v['AAA_qualified']is not False or v['ABA_admitted']is not False or len(v['records'])!=50 or len(v['fixed_current_pins'])!=3129 or len(v['output_pins'])!=296 or len(v['owned_runtime_pins'])!=187:raise RuntimeError('failed v16 remains unqualified')
    vr=read(CLOSED_V16['full_raw_records_pin']);vs=read(CLOSED_V16['stages_pin'])
    if compact(v['records'])!=compact(vr['records'])or vs!={'stages':vr['records']}:raise RuntimeError('full actual50 records unchanged')
    return [OWNER,CLOSED_V15,CLOSED_V16]"""
    change(oldreturn,newreturn)
    oldfn=ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name=='current_protection'))
    newfn=oldfn.replace("old=read(HISTORICAL_PINS['previous7251_manifest']);done=read(HISTORICAL_PINS['completed_actual_literal2_release']);post=read(HISTORICAL_PINS['completed_independent_literal2_postreview'])","old=read(HISTORICAL_PINS['previous7567_manifest']);done=read(HISTORICAL_PINS['completed_actual_literal5_release']);post=read(HISTORICAL_PINS['completed_independent_literal5_postreview'])")
    newfn=newfn.replace("done['deleted_files']!=2 or done['logical_bytes_released']!=528482632 or done['manifest_pin']!=HISTORICAL_PINS['previous7251_manifest']","done['deleted_files']!=5 or done['logical_bytes_released']!=1478165640 or done['manifest_pin']!=HISTORICAL_PINS['previous7567_manifest']").replace("HISTORICAL_PINS['completed_actual_literal2_release']","HISTORICAL_PINS['completed_actual_literal5_release']").replace('completed prior literal2','completed prior literal5').replace('len(oldrows)!=7251','len(oldrows)!=7567').replace('only exact5 previous7251','only exact3 previous7567').replace('previous7246_rows','previous7564_rows')
    newfn=newfn.replace("len(before['ordinary_file_identities'])!=328","len(before['ordinary_file_identities'])!=192").replace('exact v14 remaining297 plus failedpub5 entire31 inventory','exact closed failed v15 entire192 inventory').replace('all_other323_v14_and_failedpublic5_files_retained','all_other189_v15_files_retained')
    newfn=newfn.replace("                if selected['role']!='public5_failed'or b.norm(p)not in TARGET_SELECTED_PINS:raise RuntimeError('only exact failedpublic5 target output/owned historical rows')","                raise RuntimeError('no current selected Host/report body may alias these v15 targets')")
    newfn=newfn.replace("+v['fixed_current_pins']+v['output_pins']+v['owned_runtime_pins']:add(p,'closed_failed_v15_all3011_fixed119_owned192_scene_and_HF')","+v['fixed_current_pins']+v['output_pins']+v['owned_runtime_pins']:\n        if p['path']in TARGET_PATHS:\n            if b.norm(p)not in TARGET_SELECTED_PINS:raise RuntimeError('only exact v15 body PF historical declarations')\n        else:add(p,'closed_failed_v15_all3011_fixed119_owned189_retained_scene_and_HF')")
    marker="    for origin in DOWNSTREAM_ORIGINS:"
    insert="""    hf16=read(CLOSED_V16['Host_freeze_pin']);v16=read(CLOSED_V16['summary_pin'])
    if len(hf16['dependencies'])!=2920:raise RuntimeError('exact current v16 HF2920')
    for p in [CLOSED_V16['Host_freeze_pin'],CLOSED_V16['summary_pin'],CLOSED_V16['exact_cli_pin'],hf16['host_source']]+hf16['dependencies']+v16['fixed_current_pins']+v16['output_pins']+v16['owned_runtime_pins']:add(p,'closed_failed_v16_all3129_fixed187_owned297_scene_and_HF2920')
    actual_v16=inventory([Path(CLOSED_V16['actual_output_root'])])
    if set(actual_v16['ordinary_file_identities'])!={p['path']for p in v16['output_pins']}|{CLOSED_V16['summary_pin']['path']}or len(actual_v16['ordinary_file_identities'])!=297 or actual_v16['symlinks']:raise RuntimeError('failed v16 complete297 physical scene')
"""
    if newfn.count(marker)!=1:raise RuntimeError('one protection insert')
    newfn=newfn.replace(marker,insert+marker,1)
    newfn=newfn.replace('previous_protected_count=7251','previous_protected_count=7567').replace('only_exact_five_original_indices','only_exact_three_original_indices').replace('all_original_other7246','all_original_other7564').replace('old7251_manifest','old7567_manifest').replace('current_v14_and_failedpublic5_complete_inventory=before','current_v15_target_owner_complete_inventory=before').replace('current_v15_complete_inventory=actual_v15','current_v15_complete_inventory=actual_v15,current_v16_complete_inventory=actual_v16').replace('closed_failed_v15_is_not_engineering_or_physics_PASS=True','closed_failed_v15_and_v16_are_not_engineering_or_physics_PASS=True').replace('eight_v14_private_aliases_and_SPOASM_retained=True','prior_completed_literal5_roles_retained_as_history_without_reopening_released_targets=True')
    change(oldfn,newfn)
    oldfn=ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name=='disjoint'))
    change(oldfn,oldfn.replace('!=5','!=3').replace('exact5','exact3').replace('literal5','literal3'))
    change('BRANCHES+[V12_OUT,Path(CLOSED_V15[\'actual_output_root\'])]','BRANCHES+[V12_OUT,Path(CLOSED_V16[\'actual_output_root\'])]')
    ast.parse(current)
    other=[]
    for oldname,newname in [('prepare_literal5_manifest.py','prepare_literal3_manifest.py'),('verify_or_execute_literal5.py','verify_or_execute_literal3.py')]:
        src=(OLD/oldname).read_text();new=src.replace('literal5','literal3').replace('LITERAL5','LITERAL3').replace('target_count=5','target_count=3').replace("m['target_count']!=5","m['target_count']!=3").replace('!=5 or after','!=3 or after').replace('deleted_files=5','deleted_files=3').replace('exact5','exact3').replace('family5','family3').replace('unlink5','unlink3').replace('v14 difference','v15 difference').replace('v14/public5 inventory','v15 inventory').replace('all_other_v14_and_failedpublic5','all_other_v15').replace('retained_all_other_v14_and_failedpublic5','retained_all_other_v15').replace('actual_closed_failed_v14_and_v15_owner_proofs','actual_closed_failed_v14_v15_v16_owner_proofs')
        ast.parse(new);other.append((oldname,newname,src,new))
    # Preserve the seven proven methods and the exact sequential syscall/receipt/fsync/error body.
    def funcs(src):
        tr=ast.parse(src);return{n.name:ast.get_source_segment(src,n)for n in tr.body if isinstance(n,ast.FunctionDef)}
    frozen=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
    oldfunc=funcs(oldtext);newfunc=funcs(current)
    if any(oldfunc[n]!=newfunc[n]for n in frozen):raise RuntimeError('original low-level method changed')
    execold=other[1][2];execnew=other[1][3];start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)"
    if execold[execold.index(start):execold.index(end)]!=execnew[execnew.index(start):execnew.index(end)]:raise RuntimeError('unlink first-return receipt/fsync/firstexception changed')
    OUT.mkdir();write(OUT/'literal3_release_common.py',current)
    for _,newname,_,new in other:write(OUT/newname,new)
    plan=dict(schema='EXACT_LITERAL3_CLOSED_FAILED_V15_CURRENT_PROTECTION_ROLE_SOURCE_PLAN_V1',source_only=True,source_preparer_pin=pin(Path(__file__).absolute()),predecessor_Source_freeze_pin=pin(OLD/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json'),original_caps=constants['CAPS'],literal3_fullpins=targets,target_count=3,target_bytes=1504027360,previous7567_manifest_pin=historical['previous7567_manifest'],exact_indices_migrated_to_historical=indices,remaining7564_PF_rows_data_unchanged=True,current_closed_failed_v15_authority=v15,current_closed_failed_v16_authority=v16,current_actual_selections=selections,old_v15_complete192_inventory=before,old_v15_other189_full_EOF_authority_pins=[p for p in v15summary['output_pins']+[v15['summary_pin']]if p['path']not in{p['path']for p in targets}],new_closed_v16_all296_published_outputs_plus_summary297_full_EOF_authority_pins=vs['output_pins']+[v16['summary_pin']],new_closed_v16_fixed_count3129=len(vs['fixed_current_pins']),new_closed_v16_owned_count187=len(vs['owned_runtime_pins']),new_closed_v16_HF_dependency_count2920=2920,all_old_MF_reports_raw_logs_Source_science_proofs_immutable=True,only_private_exact_path_replay_would_be_lost=True,no_catalog_BIND_change=True,no_generic_missing_pin_skip=True,complete_original_low_level_methods_unchanged=frozen,all_numeric_physics_and_acceptance_thresholds_unchanged=True,future_actual_manifest_pin=None,future_actual_readonly_receipt_pin=None,future_actual_release_receipt_pin=None,future_actual_postrelease_pin=None,future_original_current_fullfresh2_budget_admission=None,manifest_prepared=False,deletion_executed=False,numerical_executed=False,business_executed=False)
    planpath=OUT/'EXACT_LITERAL3_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json';dump(planpath,plan)
    inverse=OUT/'COMPLETE_LITERAL5_TO_LITERAL3_SOURCE_BLOCK_BYTE_INVERSE.json'
    entries=[dict(predecessor_pin=pin(OLD/'literal5_release_common.py'),candidate_pin=pin(OUT/'literal3_release_common.py'),changes=changes)]
    for oldname,newname,src,new in other:entries.append(dict(predecessor_pin=pin(OLD/oldname),candidate_pin=pin(OUT/newname),changes=[dict(before=src,after=new)]))
    for e in entries:
        back=Path(e['candidate_pin']['path']).read_text()
        for ch in reversed(e['changes']):
            if back.count(ch['after'])!=1:raise RuntimeError('exact inverse unique after')
            back=back.replace(ch['after'],ch['before'],1)
        if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('whole predecessor byte inverse')
    dump(inverse,dict(schema='COMPLETE_LITERAL5_TO_LITERAL3_SOURCE_BLOCK_BYTE_INVERSE_V1',whole_original_three_scripts_exact=True,entries=entries,seven_low_level_methods_whole_bytes_equal=frozen,sequential_unlink_return_receipt_target_dir_fsync_FirstFailure_whole_bytes_equal=True,Source_only=True,manifest_prepared=False,deletion_executed=False))
    sf=dict(schema='COMPLETE_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,original_caps=constants['CAPS'],literal3_fullpins=targets,historical_evidence_pins=historical,current_actual_selections=selections,closed_failed_v15_authority=v15,closed_failed_v16_authority=v16,Source_pins=[pin(OUT/n)for n in('literal3_release_common.py','prepare_literal3_manifest.py','verify_or_execute_literal3.py')],exact_role_plan_pin=pin(planpath),strict_low_level_Source_provenance_pin=pin(inverse),Source_preparer_pin=pin(Path(__file__).absolute()),original_resource_factory_pin=oldsf['original_resource_factory_pin'],predecessor_Source_freeze_pin=pin(OLD/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json'),future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_original_current_fullfresh2_budget_admission=None)
    sfpath=OUT/'COMPLETE_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json';dump(sfpath,sf)
    print(json.dumps(dict(status='LITERAL3_SOURCE_ONLY_READY_NO_MANIFEST_NO_DELETION',failure=None,Source_freeze_pin=pin(sfpath),Source_pins=sf['Source_pins'],plan_pin=pin(planpath),inverse_pin=pin(inverse),preparer_pin=pin(Path(__file__).absolute()),target_bytes=1504027360,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False),ensure_ascii=False))
if __name__=='__main__':main()

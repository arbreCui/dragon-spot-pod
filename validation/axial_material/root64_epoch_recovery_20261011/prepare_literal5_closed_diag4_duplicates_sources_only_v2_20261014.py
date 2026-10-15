"""Prepare exact five-file retirement Source; no MF, unlink, compiler or solver."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal3_closed_failed_v15_private_source_v1_20261014'
OUT=R/'storage_release_literal5_closed_diag4_duplicates_source_v2_20261014'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata only')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        b=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('FD Source7')
    if identity(p.lstat())!=identity(s)or len(b)!=s.st_size:raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def write(p,b):
    if isinstance(b,str):b=b.encode()
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def dump(p,d):write(p,json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def metadata_inventory(roots):
    files={};dirs={};links={};stack=list(roots)
    while stack:
        p=stack.pop();z=p.lstat();before=identity(z)
        if not stat.S_ISDIR(z.st_mode):raise RuntimeError('ordinary existing owner root')
        dirs[str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=before:raise RuntimeError('directory opened7')
            with os.scandir(fd)as it:
                for e in it:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('owner special entry')
            if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('directory after7')
        finally:os.close(fd)
    return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)

PROTECTION=r'''def current_protection(sfpin,reviews):
    f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous7999_manifest']);done=read(HISTORICAL_PINS['completed_actual_literal3_release']);priorpost=read(HISTORICAL_PINS['completed_independent_literal3_postreview']);table={};roles={};cache={};historical=[]
    if done['deleted_files']!=3 or done['logical_bytes_released']!=1504027360 or done['manifest_pin']!=HISTORICAL_PINS['previous7999_manifest']or priorpost['failure']is not None or priorpost['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_actual_literal3_release']:raise RuntimeError('genuine completed prior literal3 retained immutable')
    oldrows=old['current_protected_full_EOF_pins']
    if len(oldrows)!=7999 or HISTORICAL_TARGET_INDICES!=[4654,4655]or [b.norm(oldrows[i])for i in [4655,4654]]!=TARGET_SELECTED_PINS[:2]or {p['path']for p in oldrows}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[:2]}:raise RuntimeError('only exact two MF7999 rows migrate; other7997 preserved')
    def add(p,role):
        p=b.norm(p);path=p['path']
        if path in TARGET_PATHS:
            if p!=next(x for x in TARGET_SELECTED_PINS if x['path']==path):raise RuntimeError('historical body requires exact selected PF')
            historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_FIVE_SELECTED_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return
        actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected PF changed or aliases exact target')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):add(p,'previous7999_exact_index_'+str(i))
    before=inventory()
    if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']:raise RuntimeError('three exact owner inventories, no aliases')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:
            p=pin(path);add(p,'all_other_owner_files_retained');retained.append(p)
    current12=inventory([V12_OUT])
    if current12!=V12_BASELINE:raise RuntimeError('current v12 namespace unchanged')
    for selected in CURRENT_SELECTIONS:
        hf=read(selected['Host_freeze_pin']);a=read(selected['actual_report_pin']);read(selected['exact_cli_pin'])
        if len(hf['dependencies'])!=selected['expected_dependency_count']or len(a['fixed_current_pins'])!=selected['actual_fixed_count']or len(a['output_pins'])!=selected['actual_output_count']or a['status']!=selected['actual_status']or a['failure']!=selected['actual_failure']or a['actual_host_Source_freeze_pin']!=selected['Host_freeze_pin']:raise RuntimeError('selected exact current authority')
        for p in [selected['Host_freeze_pin'],selected['actual_report_pin'],selected['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']+a.get('owned_runtime_pins',[]):add(p,'current_'+selected['role'])
    v16=read(CLOSED_V16['summary_pin']);h16=read(CLOSED_V16['Host_freeze_pin'])
    if len(h16['dependencies'])!=2920 or len(v16['fixed_current_pins'])!=3129 or len(v16['output_pins'])!=296:raise RuntimeError('exact v16 counts')
    for p in [CLOSED_V16['summary_pin'],CLOSED_V16['Host_freeze_pin'],CLOSED_V16['exact_cli_pin'],h16['host_source']]+h16['dependencies']+v16['fixed_current_pins']+v16['output_pins']+v16['owned_runtime_pins']:add(p,'closed_v16_retained_exact2_body_history')
    d=read(CLOSED_DIAG4['summary_pin']);h=read(CLOSED_DIAG4['Host_freeze_pin'])
    if len(h['dependencies'])!=3451 or len(d['fixed_current_pins'])!=3452 or len(d['owned_runtime_pins'])!=13:raise RuntimeError('exact diag4 counts')
    if [b.norm(h['dependencies'][i])for i in [1722,1721]]!=TARGET_SELECTED_PINS[:2]:raise RuntimeError('only exact two diagHF rows history')
    for p in [CLOSED_DIAG4['summary_pin'],CLOSED_DIAG4['Host_freeze_pin'],CLOSED_DIAG4['exact_cli_pin'],h['host_source']]+h['dependencies']+d['fixed_current_pins']+d['output_pins']+d['owned_runtime_pins']:add(p,'diag4_current_except_exact_four_generated_body_history')
    sfB=read(HISTORICAL_PINS['BOOTB_new_Fortran_SF'])
    for p in sfB['files']+sfB['current_actual_diag4_ordered70_input_pins']+[sfB['retained_actual_diagnostic_BOXX68_pin'],sfB['retained_actual_BOXX68_Source_freeze_pin']]:add(p,'new_BOOTB_Fortran_Source_and_current_actual70')
    for authority in (CLOSED_V16,CLOSED_DIAG4):
        a=read(authority['summary_pin']);root=Path(authority['actual_output_root']);scene=inventory([root])
        if set(scene['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{authority['summary_pin']['path']}or scene['symlinks']:raise RuntimeError('complete actual owner scene unchanged')
    for origin in DOWNSTREAM_ORIGINS:
        d=read(origin['metadata_pin'])
        if [b.norm(x['current_pin'])for x in d['rows']]!=origin['current_pins']or len(d['rows'])!=origin['current_row_count']:raise RuntimeError('material33 GENDF51 rows unchanged')
        add(origin['metadata_pin'],'downstream_metadata')
        for p in origin['current_pins']:add(p,'original_downstream_science_current')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_and_historical_proof_files_current')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_Source_tools0')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=7999,only_exact_two_original_indices_migrated_to_historical=[4654,4655],all_original_other7997_PF_rows_data_retained=True,explicit_exact_five_historical_body_declarations=historical,old_SFs_MFs_reports_logs_seals_raw_science_unchanged=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True),retained,before'''

def main():
    if OUT.exists():raise RuntimeError('unique Source package only')
    osf=read(OLD/'COMPLETE_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json')
    for p in osf['Source_pins']:
        if pin(p['path'])!=p:raise RuntimeError('old Source exactPF')
    old=(OLD/'literal3_release_common.py').read_text();tree=ast.parse(old);const={}
    for n in tree.body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:const[n.targets[0].id]=ast.literal_eval(n.value)
            except(ValueError,TypeError):pass
    rolepath=R/'readonly_exact5_Q_MAC_and_SPOASM_private_retirement_current_role_review_20261014/REVIEW.json';role=read(rolepath);rtp=pin(rolepath.parent/'TRUE_TOOL_RETURNS.json');rt=read(rtp['path']);ret=rt['actual_review_return']
    if role['failure']is not None or role['target_count']!=5 or role['target_total_bytes']!=1323735516 or type(ret['exit_code'])is not int or ret['exit_code']!=0 or ret.get('session_id')is not None or rt['observed_closed']is not True or json.loads(ret['output'].strip().splitlines()[-1])['review_pin']!=pin(rolepath):raise RuntimeError('genuine exact5 role Source0')
    targets=[role['targets_in_literal_order'][i]for i in [1,0,3,2,4]];paths={p['path']for p in targets}
    for p in targets:
        s=Path(p['path']).lstat()
        if identity(s)!=p['identity']or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or s.st_uid!=os.getuid():raise RuntimeError('five current exact identities')
    previous=read(role['previous_literal3_manifest_pin']['path'])
    if len(previous['current_protected_full_EOF_pins'])!=7999 or [previous['current_protected_full_EOF_pins'][i]for i in [4655,4654]]!=targets[:2]:raise RuntimeError('MF7999 exact two index data')
    postpath=R/'independent_one_BOOT_exact_status_diagnostic_v4_actual_failure_postverify_20261014/REVIEW.json';post=read(postpath);diag=read(post['actual_report_pin']['path'])
    cd=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_exact_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=pin(postpath),independent_posttools_pin=pin(postpath.parent/'TRUE_TOOL_RETURNS.json'),actual_output_root=str(Path(post['actual_report_pin']['path']).parent))
    if post['actual_Root_exit_code']!=1 or post['actual_BOOT_return_status']!=1 or post['actual_BOOT_plane']!=1 or post['actual_stage_count']!=3 or post['current_fixed_count']!=3452 or post['actual_output_file_count']!=27 or diag['actual_outcome']is not None:raise RuntimeError('actual failed diagnostic fixed facts')
    roots=[Path(const['CLOSED_V16']['actual_output_root']),Path(cd['actual_output_root']),Path(targets[4]['path']).parents[2]]
    before=metadata_inventory(roots)
    if before['symlinks']:raise RuntimeError('ordinary target owner roots')
    hist=dict(const['HISTORICAL_PINS']);hist.update(previous7999_manifest=role['previous_literal3_manifest_pin'],completed_actual_literal3_release=pin(R/'storage_release_literal3_closed_failed_v15_private_actual_receipts_20261014/ACTUAL_EXACT_LITERAL3_CLOSED_FAILED_V15_PRIVATE_OLD_PRIVATE_RELEASE_RECEIPT.json'),completed_independent_literal3_postreview=pin(R/'independent_literal3_actual_exact_release_postverify_20261014/REVIEW.json'),completed_independent_literal3_posttools=pin(R/'independent_literal3_actual_exact_release_postverify_20261014/TRUE_TOOL_RETURNS.json'),exact5_role_review=pin(rolepath),exact5_role_tools=rtp,BOOTB_new_Fortran_SF=role['selected_BOOTB_first_admission_FortranSF_pin'],SPOASM_original_owner_role_review=role['SPOASM_independent_current_source_owner_role_review_pin'],SPOASM_original_owner_role_tools=role['SPOASM_independent_current_source_owner_role_true_tools_pin'])
    hist.update({'closed_diag4_'+k:v for k,v in cd.items()if isinstance(v,dict)and 'path'in v})
    draft=R/'boot_v16_BOOTB_first_admission_predicate_diagnostic_host_source_draft_v1_20261014'
    for name in ('COMPLETE_DIAG4_HOST_TO_BOOTB49_DRAFT_SOURCE_WHOLE_BYTE_INVERSE.json', 'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json', 'SOURCE_ONLY_DRAFT_READY.json', 'TRUE_SOURCE_PREPARATION_TOOL_RETURNS.json', 'run_guarded_one_BOOT_first_predicate_diagnostic.py'):
        hist['BOOTB_current_probe_draft_'+name]=pin(draft/name)
    core=R/'independent_BOOTB_first_predicate_Host_core_draft_Source_review_20261014'
    hist['BOOTB_current_probe_core_Source_review']=pin(core/'REVIEW.json');hist['BOOTB_current_probe_core_Source_tools']=pin(core/'TRUE_TOOL_RETURNS.json')

    current=old;changes=[]
    def change(before,after):
        nonlocal current
        if current.count(before)!=1:raise RuntimeError('exact unique splice')
        current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
    def assignment(name,value):
        n=next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name);change(ast.get_source_segment(current,n),name+'='+repr(value))
    for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[4654,4655]),('BASELINE_OWNED_INVENTORIES',before),('BRANCHES',roots),('BYTES',1323735516),('SOURCE_NAMES',('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py'))]:
        assignment(k,v) if k!='BRANCHES'else change(ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==k)),"BRANCHES=[Path(p)for p in "+repr([str(p)for p in roots])+"]")
    for k,name in [('SF','COMPLETE_LITERAL5_CLOSED_DIAG4_DUPLICATES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL5_CLOSED_DIAG4_DUPLICATES_MANIFEST.json')]:
        n=next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==k);change(ast.get_source_segment(current,n),k+"=PKG/"+repr(name))
    n=next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='RECEIPTS');change(ast.get_source_segment(current,n),"RECEIPTS=REC/'storage_release_literal5_closed_diag4_duplicates_actual_receipts_20261014'\nCLOSED_DIAG4="+repr(cd))
    def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
    gate=fn('source_gate');new=gate.replace('literal3','literal5').replace('LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE','LITERAL5_CLOSED_DIAG4_DUPLICATES').replace('immutable3','immutable5').replace('!=3','!=5').replace("or f['closed_failed_v16_authority']!=CLOSED_V16","or f['closed_failed_v16_authority']!=CLOSED_V16 or f['closed_diag4_authority']!=CLOSED_DIAG4");change(gate,new)
    dis=fn('disjoint');change(dis,dis.replace('!=3','!=5').replace('exact3','exact5').replace('literal3','literal5'))
    change(fn('current_protection'),PROTECTION)
    tail="    return [OWNER,CLOSED_V15,CLOSED_V16]"
    add="""    d=read(CLOSED_DIAG4['summary_pin']);t=read(CLOSED_DIAG4['Root_true_tool_pin']);a=read(CLOSED_DIAG4['Root_exact_argv_pin']);post=read(CLOSED_DIAG4['independent_postreview_pin']);pt=read(CLOSED_DIAG4['independent_posttools_pin']);terminal=t['actual_terminal_return'];pr=pt['actual_review_return']
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['argv']or len(a['argv'])!=48:raise RuntimeError('genuine diagnosticRoot48 failed terminal1')
    if pt['observed_closed']is not True or type(pr['exit_code'])is not int or pr['exit_code']!=0 or pr.get('session_id')is not None or b.norm(json.loads(pr['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_DIAG4['independent_postreview_pin']:raise RuntimeError('genuine independent diagnostic post0')
    if post['actual_report_pin']!=CLOSED_DIAG4['summary_pin']or post['actual_Root_true_tool_return_pin']!=CLOSED_DIAG4['Root_true_tool_pin']or post['actual_Host_freeze_pin']!=CLOSED_DIAG4['Host_freeze_pin']or post['actual_Root_exit_code']!=1 or post['actual_BOOT_plane']!=1 or post['actual_BOOT_return_status']!=1 or post['actual_stage_count']!=3 or post['actual_stage_statuses']!=['PASS','PASS','FAILED']or post['current_fixed_count']!=3452 or post['actual_output_file_count']!=27 or post['all_three_watches_closed_without_limit_failure']is not True or post['actual_engineering_closed0']is not False or post['actual_completion_marker_only_unexecuted_input_deck_listing']is not True:raise RuntimeError('genuine failed admission diagnostic, not solver0')
    if d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!="RuntimeError('own-child stage failed; no retry')"or d['actual_outcome']is not None or len(d['records'])!=3 or len(d['fixed_current_pins'])!=3452 or len(d['owned_runtime_pins'])!=13:raise RuntimeError('sealed diagnostic failure unchanged')
    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4]"""
    change(tail,add);ast.parse(current)
    other=[]
    for oldname,newname in [('prepare_literal3_manifest.py','prepare_literal5_manifest.py'),('verify_or_execute_literal3.py','verify_or_execute_literal5.py')]:
        src=(OLD/oldname).read_text();new=src.replace('literal3','literal5').replace('LITERAL3_CLOSED_FAILED_V15_PRIVATE','LITERAL5_CLOSED_DIAG4_DUPLICATES').replace('target_count=3','target_count=5').replace("m['target_count']!=3","m['target_count']!=5").replace('!=3 or after','!=5 or after').replace('deleted_files=3','deleted_files=5').replace('unlink3','unlink5').replace('family3','family5');ast.parse(new);other.append((oldname,newname,src,new))
    def funcs(src):return{n.name:ast.get_source_segment(src,n)for n in ast.parse(src).body if isinstance(n,ast.FunctionDef)}
    frozen=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate'];a=funcs(old);z=funcs(current)
    if any(a[k]!=z[k]for k in frozen):raise RuntimeError('seven frozen methods changed')
    start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";x=other[1][2];y=other[1][3]
    if x[x.index(start):x.index(end)]!=y[y.index(start):y.index(end)]:raise RuntimeError('exact syscall-returnreceipt-dirfsync-firsterror body changed')
    OUT.mkdir();write(OUT/'literal5_release_common.py',current)
    for _,name,_,src in other:write(OUT/name,src)
    plan=dict(schema='EXACT_LITERAL5_CLOSED_DIAG4_DUPLICATES_ROLE_SOURCE_PLAN_V1',source_only=True,literal5_fullpins=targets,target_count=5,target_bytes=1323735516,previous7999_manifest_pin=role['previous_literal3_manifest_pin'],exact_previous_MF_indices_migrated_to_historical=[4654,4655],other7997_rows_unchanged=True,exact_diag4_HF_indices_migrated_to_historical=[1721,1722],explicit_only_five_body_historical_roles=True,all18_source_and_owned_input_copies_kept=True,all_current70_and_four_archives_kept=True,BOOTB_new_Source_freeze_pin=hist['BOOTB_new_Fortran_SF'],all_science_original_four_SPOASM_kept=True,all_old_SFs_MFs_reports_logs_raw_seals_kept=True,closed_diag4_authority=cd,current_target_owner_inventory=before,original_caps=const['CAPS'],source_preparer_pin=pin(__file__),exact_role_survey_pin=pin(rolepath),exact_role_survey_tools_pin=rtp,exact_survey_to_authoritative_target_order_permutation=[1,0,3,2,4],authoritative_target_order=['old_v16_Q','old_v16_MAC','diag4_Q','diag4_MAC','SPOASM_private_input'],no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_postrelease_pin=None,future_original_fullfresh2_admission=None,future_probe_Host_freeze_pin=None,manifest_prepared=False,deletion_executed=False,business_executed=False,numerical_executed=False)
    pp=OUT/'EXACT_LITERAL5_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json';dump(pp,plan)
    entries=[dict(predecessor_pin=pin(OLD/'literal3_release_common.py'),candidate_pin=pin(OUT/'literal5_release_common.py'),changes=changes)]
    for on,nn,src,new in other:entries.append(dict(predecessor_pin=pin(OLD/on),candidate_pin=pin(OUT/nn),changes=[dict(before=src,after=new)]))
    for e in entries:
        back=Path(e['candidate_pin']['path']).read_text()
        for c in reversed(e['changes']):
            if back.count(c['after'])!=1:raise RuntimeError('exact inverse unique')
            back=back.replace(c['after'],c['before'],1)
        if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('whole predecessor inverse')
    ip=OUT/'COMPLETE_LITERAL3_TO_NEW_LITERAL5_SOURCE_BLOCK_BYTE_INVERSE.json';dump(ip,dict(schema='COMPLETE_LITERAL3_TO_NEW_LITERAL5_SOURCE_BLOCK_BYTE_INVERSE_V1',entries=entries,seven_low_level_methods_whole_bytes_equal=frozen,sequential_syscall_returnreceipt_dirfsync_FirstFailure_whole_bytes_equal=True,source_only=True,manifest_prepared=False,deletion_executed=False))
    sf=dict(schema='COMPLETE_LITERAL5_CLOSED_DIAG4_DUPLICATES_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,original_caps=const['CAPS'],literal5_fullpins=targets,historical_evidence_pins=hist,current_actual_selections=const['CURRENT_SELECTIONS'],closed_failed_v15_authority=const['CLOSED_V15'],closed_failed_v16_authority=const['CLOSED_V16'],closed_diag4_authority=cd,Source_pins=[pin(OUT/n)for n in('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py')],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),original_resource_factory_pin=osf['original_resource_factory_pin'],predecessor_Source_freeze_pin=pin(OLD/'COMPLETE_LITERAL3_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json'),future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None)
    sp=OUT/'COMPLETE_LITERAL5_CLOSED_DIAG4_DUPLICATES_SOURCE_FREEZE.json';dump(sp,sf)
    fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status='NEW_LITERAL5_SOURCE_ONLY_READY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),target_bytes=1323735516,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)))
if __name__=='__main__':main()

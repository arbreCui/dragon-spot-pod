"""Prepare three exact private-body retirement Sources. Never prepare MF or unlink."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal5_closed_diag4_duplicates_source_v3_20261014'
OUT=R/'storage_release_literal3_next_BOOT_BIND_duplicates_source_v1_20261014'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        data=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('FD Source7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def write(p,data):
    if isinstance(data,dict):data=(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    elif isinstance(data,str):data=data.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
def inventory(roots):
    out=dict(ordinary_file_identities={},directory_identities={},symlinks={});stack=list(roots)
    while stack:
        p=stack.pop();s=p.lstat();before=identity(s)
        if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary owner directory')
        out['directory_identities'][str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=before:raise RuntimeError('directory opened7')
            with os.scandir(fd)as it:
                for e in it:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):out['ordinary_file_identities'][str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):out['symlinks'][str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('ordinary owner entries')
            if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('directory after7')
        finally:os.close(fd)
    return out

PROTECT=r'''def current_protection(sfpin,reviews):
    f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8262_manifest']);table={};roles={};cache={};historical=[]
    done=read(HISTORICAL_PINS['completed_exact5_release']);post=read(HISTORICAL_PINS['completed_exact5_postreview'])
    if done['manifest_pin']!=HISTORICAL_PINS['previous8262_manifest']or done['deleted_files']!=5 or done['logical_bytes_released']!=1323735516 or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_exact5_release']:raise RuntimeError('genuine prior exact5 release retained as history')
    oldrows=old['current_protected_full_EOF_pins']
    if len(oldrows)!=8262 or HISTORICAL_TARGET_INDICES!=[5618]or b.norm(oldrows[5618])!=TARGET_SELECTED_PINS[2]or {p['path']for p in oldrows}&TARGET_PATHS!={TARGET_SELECTED_PINS[2]['path']}:raise RuntimeError('only one exact MF8262 PROJECT row history; other8261 unchanged')
    def add(p,role):
        p=b.norm(p);path=p['path']
        if path in TARGET_PATHS:
            if p!=next(x for x in TARGET_SELECTED_PINS if x['path']==path):raise RuntimeError('only exact selected three historical PFs')
            historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_THREE_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return
        actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected PF or physical alias changed')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):add(p,'previous8262_exact_index_'+str(i))
    before=inventory()
    if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']:raise RuntimeError('two complete ordinary closed owner inventories unchanged')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_two_closed_owner_files');retained.append(p)
    current12=inventory([V12_OUT])
    if current12!=V12_BASELINE:raise RuntimeError('current v12 namespace unchanged')
    a=read(CLOSED_PROBE['summary_pin']);hf=read(CLOSED_PROBE['Host_freeze_pin'])
    if len(hf['dependencies'])!=3512 or len(a['fixed_current_pins'])!=3513 or len(a['output_pins'])!=27:raise RuntimeError('exact current probe3512/3513/27')
    if b.norm(hf['dependencies'][2578])!=TARGET_SELECTED_PINS[2]or {p['path']for p in hf['dependencies']}&TARGET_PATHS!={TARGET_SELECTED_PINS[2]['path']}:raise RuntimeError('only exact currentHF2578 PROJECT history')
    for p in [CLOSED_PROBE['summary_pin'],CLOSED_PROBE['Host_freeze_pin'],CLOSED_PROBE['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']+a['owned_runtime_pins']:add(p,'current_probe_exact3_history_only')
    scene=inventory([Path(CLOSED_PROBE['actual_output_root'])])
    if set(scene['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{CLOSED_PROBE['summary_pin']['path']}or scene['symlinks']:raise RuntimeError('current28 scene complete')
    for p in ROLE_KEEP_PINS:add(p,'original9_old8_new9_current70_modules_science_kept')
    for p in BIND_NEW_SOURCE_PINS:add(p,'new_BIND82_Source_and_proof_kept')
    for origin in DOWNSTREAM_ORIGINS:
        d=read(origin['metadata_pin'])
        if [b.norm(x['current_pin'])for x in d['rows']]!=origin['current_pins']or len(d['rows'])!=origin['current_row_count']:raise RuntimeError('original material33 GENDF51 unchanged')
        add(origin['metadata_pin'],'downstream_metadata')
        for p in origin['current_pins']:add(p,'downstream_science_current')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_history_proofs_kept')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_Source_tools0')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8262,only_exact_original_indices_migrated_to_historical=[5618],all_original_other8261_PF_rows_data_retained=True,exact_current_HF3512_indices_migrated_to_historical=[2578],explicit_exact_three_historical_body_declarations=historical,current28_scene_other26_kept=True,old_diag4_remaining24_kept=True,all_original9_old8_new9_and_current70_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True),retained,before'''

def main():
    if OUT.exists():raise RuntimeError('unique Source namespace')
    oldsf=read(OLD/'COMPLETE_LITERAL5_CLOSED_DIAG4_DUPLICATES_SOURCE_FREEZE.json')
    for p in oldsf['Source_pins']:
        if pin(p['path'])!=p:raise RuntimeError('old Source exactPF')
    old=(OLD/'literal5_release_common.py').read_text();current=old;changes=[];const={}
    for n in ast.parse(old).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:const[n.targets[0].id]=ast.literal_eval(n.value)
            except(ValueError,TypeError):pass
    rolepath=R/'readonly_next_BOOT_BIND_probe_exact3_private_role_and_current_budget_survey_20261014/REVIEW.json';role=read(rolepath);rtp=pin(rolepath.with_name('TRUE_TOOL_RETURNS.json'));rt=read(rtp['path']);rr=rt['actual_survey_return']
    if pin(rolepath)['sha256']!='406b90fe42ca75338d8162fe1b916d8ce2677ffc37ea73e4ff879554059691e7'or role['failure']is not None or role['target_count']!=3 or role['target_total_bytes']!=1277838584 or type(rr['exit_code'])is not int or rr['exit_code']!=0 or rr.get('session_id')is not None or rt['observed_closed']is not True or json.loads(rr['output'].strip().splitlines()[-1])['review_pin']!=pin(rolepath):raise RuntimeError('genuine exact3 readonly role0')
    targets=role['targets_in_literal_order'];paths={p['path']for p in targets}
    for p in targets:
        s=Path(p['path']).lstat()
        if identity(s)!=p['identity']or not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('three current owned singlelink target identities')
    postpath=R/'independent_BOOTB_first_predicate_diagnostic_v1_actual_failure_postverify_20261014/REVIEW.json';post=read(postpath);probe=read(post['actual_report_pin']['path'])
    cp=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_exact_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=pin(postpath),independent_posttools_pin=pin(postpath.with_name('TRUE_TOOL_RETURNS.json')),actual_output_root=str(Path(post['actual_report_pin']['path']).parent))
    if post['actual_Root_exit_code']!=1 or post['verification_failure']is not None or post['actual_original_predicate_source_line']!=466 or post['actual_BOOT_return_status']!=1 or post['current_fixed_count']!=3513 or post['actual_output_file_count']!=28:raise RuntimeError('exact observed BOOTB466 failure facts only')
    roots=[Path(cp['actual_output_root']),Path(const['CLOSED_DIAG4']['actual_output_root'])];baseline=inventory(roots)
    previous=role['current_MF8262_pin'];rows=read(previous['path'])['current_protected_full_EOF_pins']
    if len(rows)!=8262 or rows[5618]!=targets[2]:raise RuntimeError('exact previous MF PROJECT singleton')
    hist=dict(const['HISTORICAL_PINS']);hist.update(previous8262_manifest=previous,completed_exact5_release=pin(R/'storage_release_literal5_closed_diag4_duplicates_actual_receipts_20261014/ACTUAL_EXACT_LITERAL5_CLOSED_DIAG4_DUPLICATES_OLD_PRIVATE_RELEASE_RECEIPT.json'),completed_exact5_postreview=pin(R/'independent_literal5_diag4_v3_actual_exact_release_postverify_20261014/REVIEW.json'),completed_exact5_posttools=pin(R/'independent_literal5_diag4_v3_actual_exact_release_postverify_20261014/TRUE_TOOL_RETURNS.json'),exact3_role_review=pin(rolepath),exact3_role_tools=rtp,completed_exact5_Root_tools=pin(R/'ROOT_LITERAL5_DIAG4_V3_ACTUAL_EXECUTE_TRUE_TOOL_RETURNS_20261014.json'))
    hist.update({'closed_current_probe_'+k:v for k,v in cp.items()if isinstance(v,dict)and'path'in v})
    bdir=R/'boot_v16_BIND64_82_explicit_return_diagnostic_source_v1_20261014';bindpins=[pin(p)for p in sorted(bdir.iterdir())if p.is_file()]
    for i,p in enumerate(bindpins):hist['BIND82_current_Source_'+str(i)]=p
    keep=role['current_next_newprobe9_ordinary_input_copy_pins']+role['original_v16_scientific_nine_input_pins']+role['old_diag4_remaining8_copy_pins_retained']
    def change(before,after):
        nonlocal current
        if current.count(before)!=1:raise RuntimeError('unique Source splice')
        current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
    def node(name):return next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    def assignment(name,value):change(ast.get_source_segment(current,node(name)),name+'='+repr(value))
    for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',[5618]),('BASELINE_OWNED_INVENTORIES',baseline),('BYTES',1277838584),('SOURCE_NAMES',('literal3_release_common.py','prepare_literal3_manifest.py','verify_or_execute_literal3.py'))]:assignment(k,v)
    change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
    change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal3_next_BOOT_BIND_duplicates_actual_receipts_20261014'\nCLOSED_PROBE="+repr(cp)+'\nROLE_KEEP_PINS='+repr(keep)+'\nBIND_NEW_SOURCE_PINS='+repr(bindpins))
    for k,name in [('SF','COMPLETE_LITERAL3_NEXT_BOOT_BIND_DUPLICATES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL3_NEXT_BOOT_BIND_DUPLICATES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(name))
    def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
    gate=fn('source_gate');change(gate,gate.replace('literal5','literal3').replace('LITERAL5_CLOSED_DIAG4_DUPLICATES','LITERAL3_NEXT_BOOT_BIND_DUPLICATES').replace('immutable5','immutable3').replace('!=5','!=3').replace("or f['closed_diag4_authority']!=CLOSED_DIAG4","or f['closed_diag4_authority']!=CLOSED_DIAG4 or f['closed_current_BOOTB_probe_authority']!=CLOSED_PROBE"))
    d=fn('disjoint');change(d,d.replace('!=5','!=3').replace('exact5','exact3').replace('literal5','literal3'))
    change(fn('current_protection'),PROTECT)
    tail='    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4]'
    extra=r'''    d=read(CLOSED_PROBE['summary_pin']);t=read(CLOSED_PROBE['Root_true_tool_pin']);a=read(CLOSED_PROBE['Root_exact_argv_pin']);post=read(CLOSED_PROBE['independent_postreview_pin']);pt=read(CLOSED_PROBE['independent_posttools_pin']);terminal=t['actual_terminal_return'];pr=pt['actual_review_return']
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['argv']or len(a['argv'])!=42:raise RuntimeError('genuine closed Root42 probe1')
    if pt['observed_closed']is not True or type(pr['exit_code'])is not int or pr['exit_code']!=0 or pr.get('session_id')is not None or b.norm(json.loads(pr['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_PROBE['independent_postreview_pin']:raise RuntimeError('genuine independent probe post0')
    if post['verification_failure']is not None or post['failure']is not None or post['actual_report_pin']!=CLOSED_PROBE['summary_pin']or post['actual_Root_true_tool_return_pin']!=CLOSED_PROBE['Root_true_tool_pin']or post['actual_Host_freeze_pin']!=CLOSED_PROBE['Host_freeze_pin']or post['actual_Root_exit_code']!=1 or post['actual_original_predicate_source_line']!=466 or post['actual_BOOT_return_status']!=1 or post['current_fixed_count']!=3513 or post['actual_output_file_count']!=28 or post['all_three_watches_closed_without_limit_failure']is not True or post['current_fixed_all7_twice_verified']is not True or post['whole_scene_inventory_equals_exact_summary_output_pins_plus_summary']is not True or post['engineering_qualified']is not False:raise RuntimeError('exact observed failed BOOTB466 and genuine full EOF/current7 post facts')
    if any(post[k]is not False for k in('independent_business_executed','independent_compiler_executed','independent_numerical_executed','independent_files_deleted')):raise RuntimeError('independent readonly actualpost')
    if d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!="RuntimeError('own-child stage failed; no retry')"or len(d['records'])!=3 or [r['status']for r in d['records']]!=['PASS','PASS','FAILED']or d['actual_outcome']['actual_first_admission_predicate']['predicate_id']!='BOOTB_INGRESS_RETURN_L0466'or len(d['fixed_current_pins'])!=3513 or d['engineering_qualified']is not False:raise RuntimeError('sealed failed probe unchanged; never solver qualification')
    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE]'''
    change(tail,extra);ast.parse(current)
    other=[]
    for oldname,newname in [('prepare_literal5_manifest.py','prepare_literal3_manifest.py'),('verify_or_execute_literal5.py','verify_or_execute_literal3.py')]:
        src=(OLD/oldname).read_text();new=src.replace('literal5','literal3').replace('LITERAL5_CLOSED_DIAG4_DUPLICATES','LITERAL3_NEXT_BOOT_BIND_DUPLICATES').replace('target_count=5','target_count=3').replace("m['target_count']!=5","m['target_count']!=3").replace('!=5 or after','!=3 or after').replace('deleted_files=5','deleted_files=3').replace('unlink5','unlink3');ast.parse(new);other.append((oldname,newname,src,new))
    def funcs(src):return{n.name:ast.get_source_segment(src,n)for n in ast.parse(src).body if isinstance(n,ast.FunctionDef)}
    names=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate'];f1=funcs(old);f2=funcs(current)
    if any(f1[n]!=f2[n]for n in names):raise RuntimeError('seven frozen lowlevel methods changed')
    start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";oldexe=other[1][2];newexe=other[1][3]
    if oldexe[oldexe.index(start):oldexe.index(end)]!=newexe[newexe.index(start):newexe.index(end)]:raise RuntimeError('whole truthful unlink receipt dirfsync FirstFailure body changed')
    OUT.mkdir();write(OUT/'literal3_release_common.py',current)
    for _,name,_,s in other:write(OUT/name,s)
    pp=OUT/'EXACT_LITERAL3_NEXT_BOOT_BIND_ROLE_SOURCE_PLAN.json'
    plan=dict(schema='EXACT_LITERAL3_NEXT_BOOT_BIND_DUPLICATES_ROLE_SOURCE_PLAN_V1',source_only=True,literal3_fullpins=targets,target_count=3,target_bytes=1277838584,previous8262_manifest_pin=previous,exact_previous_MF_indices_migrated_to_historical=[5618],other8261_rows_unchanged=True,exact_current_HF3512_indices_migrated_to_historical=[2578],newprobe_scene_other26_current=True,old_diag4_remaining24_current=True,next_input_source_is_actual_newprobe9=role['current_next_newprobe9_ordinary_input_copy_pins'],original_v16_nine_current=role['original_v16_scientific_nine_input_pins'],old_diag4_other8_current=role['old_diag4_remaining8_copy_pins_retained'],explicit_only_three_historical_bodies=True,current_newprobe_authority=cp,current_target_owner_inventory=baseline,current_BIND82_Source_pins=bindpins,current_fortran_future_compile_object_and_HF_not_claimed=True,source_preparer_pin=pin(__file__),exact_role_survey_pin=pin(rolepath),exact_role_survey_tools_pin=rtp,original_caps=const['CAPS'],no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,old_Source_MF_HF_summary_logs_science_never_rewritten=True,legacy_v15_named_fields_describe_the_explicit_two_current_owner_roots_and_not_new_v15_deletions=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_postrelease_budget_admission=None,future_probe_Host_freeze_pin=None,manifest_prepared=False,deletion_executed=False,business_executed=False,numerical_executed=False)
    write(pp,plan);entries=[dict(predecessor_pin=pin(OLD/'literal5_release_common.py'),candidate_pin=pin(OUT/'literal3_release_common.py'),changes=changes)]
    for oldname,newname,src,new in other:entries.append(dict(predecessor_pin=pin(OLD/oldname),candidate_pin=pin(OUT/newname),changes=[dict(before=src,after=new)]))
    for e in entries:
        back=Path(e['candidate_pin']['path']).read_text()
        for c in reversed(e['changes']):
            if back.count(c['after'])!=1:raise RuntimeError('unique wholeinverse splice')
            back=back.replace(c['after'],c['before'],1)
        if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('whole predecessor inverse')
    ip=OUT/'COMPLETE_LITERAL5_TO_NEXT_LITERAL3_SOURCE_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_LITERAL5_TO_NEXT_LITERAL3_SOURCE_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=names,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True,manifest_prepared=False,deletion_executed=False))
    sf=dict(schema='COMPLETE_LITERAL3_NEXT_BOOT_BIND_DUPLICATES_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,original_caps=const['CAPS'],literal3_fullpins=targets,historical_evidence_pins=hist,current_actual_selections=const['CURRENT_SELECTIONS'],closed_failed_v15_authority=const['CLOSED_V15'],closed_failed_v16_authority=const['CLOSED_V16'],closed_diag4_authority=const['CLOSED_DIAG4'],closed_current_BOOTB_probe_authority=cp,Source_pins=[pin(OUT/n)for n in('literal3_release_common.py','prepare_literal3_manifest.py','verify_or_execute_literal3.py')],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),original_resource_factory_pin=oldsf['original_resource_factory_pin'],predecessor_Source_freeze_pin=pin(OLD/'COMPLETE_LITERAL5_CLOSED_DIAG4_DUPLICATES_SOURCE_FREEZE.json'),future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None)
    sp=OUT/'COMPLETE_LITERAL3_NEXT_BOOT_BIND_DUPLICATES_SOURCE_FREEZE.json';write(sp,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);os.fsync(fd);os.close(fd)
    print(json.dumps(dict(status='NEXT_LITERAL3_SOURCE_ONLY_READY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),target_bytes=1277838584,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)))
if __name__=='__main__':main()

"""Prepare exact11 next A8 cleanup Source only. No MF, compiler, solver or unlink."""
import ast, hashlib, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal11_next_A8_core_duplicates_source_v1_20261014'
OUT=R/'storage_release_literal11_next_MCCGF_lifetime_duplicates_source_v1_20261014'
ROLE=R/'readonly_next_MCCGF_lifetime_exact11_role_budget_survey_20261014/REVIEW.json'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
TOTAL=1330716816
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata EOF only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('Source opened7')
        data=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('Source FD7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('Source after7')
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact Source/metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
def write(p,data):
    if isinstance(data,dict):data=(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    elif isinstance(data,str):data=data.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:
        f.write(data);f.flush();os.fsync(f.fileno())
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
                    else:raise RuntimeError('ordinary owner entry')
            if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('directory after7')
        finally:os.close(fd)
    return out
def closed0(t,key,review):
    a=t[key]
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(a['exit_code'])is not int or a['exit_code']!=0 or a.get('session_id')is not None or norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=review:raise RuntimeError('actual typed closed review0')

A8_CLOSED="    d=read(CLOSED_LATEST_A8['summary_pin']);t=read(CLOSED_LATEST_A8['Root_true_tool_pin']);a=read(CLOSED_LATEST_A8['Root_exact_argv_pin']);post=read(CLOSED_LATEST_A8['independent_postreview_pin']);pt=read(CLOSED_LATEST_A8['independent_posttools_pin']);terminal=t['actual_terminal_return'];pr=pt['actual_review_return']\n    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or len(a['exact_argv'])!=42 or a['exact_command']!=t['exact_executed_command']:raise RuntimeError('genuine latest A8 Root42 terminal1')\n    if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(pr['exit_code'])is not int or pr['exit_code']!=0 or pr.get('session_id')is not None or b.norm(json.loads(pr['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_LATEST_A8['independent_postreview_pin']:raise RuntimeError('genuine latest A8 independent post0')\n    event={'schema':'ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1','scope':'FLU2DR64_CORE','predicate_id':'A9_FLU2DR64_CORE_RETURN_L0233','original_return_source_line':233,'actual_boolean_status_integer':0}\n    e8={'schema':'ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1','scope':'MCCGF64','predicate_id':'A8_MCCGF64_RETURN_L0442','original_return_source_line':442,'actual_boolean_status_integer':0};e8door={'schema':'ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1','scope':'DOORFV64','predicate_id':'A8_DOORFV64_RETURN_L0359','original_return_source_line':359,'actual_boolean_status_integer':0}\n    if post['schema']!='INDEPENDENT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_A8_247_FALSE_RETURN_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['verification_failure']is not None or post['actual_report_pin']!=CLOSED_LATEST_A8['summary_pin']or post['actual_Root_true_tool_return_pin']!=CLOSED_LATEST_A8['Root_true_tool_pin']or post['actual_Root_exact_argv_pin']!=CLOSED_LATEST_A8['Root_exact_argv_pin']or post['actual_Host_freeze_pin']!=CLOSED_LATEST_A8['Host_freeze_pin']or post['actual_CLI_pin']!=CLOSED_LATEST_A8['exact_cli_pin']or post['actual_Root_exit_code']!=1 or post['actual_Root_closed']is not True or post['actual_BOOT_plane']!=1 or post['actual_BOOT_return_status']!=2 or post['actual_original_status_symbol']!='SPOR64_BOOTB64_CORE_FAILED'or post['actual_A9_failed_return_chain']!=[event]or post['actual_A9_first_false_return']!=event or post['actual_A8_failed_return_chain']!=[e8,e8door]or post['actual_A8_first_false_return']!=e8 or post['internal_nbmix_state_vector_values_captured']is not False or post['geometry_or_dimension_mismatch_inferred']is not False or post['storage_lifetime_root_cause_proved']is not False or post['actual_no_admission_BIND_native_rejection_inventory_or_seal_events']is not True or post['current_fixed_count']!=3788 or post['current_HF_dependency_count']!=3787 or post['actual_output_file_count']!=28 or post['all_three_watches_closed_without_limit_failure']is not True or post['current_fixed_all7_twice_verified']is not True or post['current_HF_all7_twice_verified']is not True or post['whole_scene_inventory_equals_exact_summary_output_pins_plus_summary']is not True or post['actual_original_first_failure_object_traceback_preserved']is not True or post['only_ordered70_index1_changed']is not True or post['actual_module6092_fullSHA_matches_original']is not True or post['engineering_qualified']is not False:raise RuntimeError('actual latest A8 failure CORE233 facts only; MCCGF nbmix<=0 only; buffer lifetime root cause unknown')\n    if any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('readonly latest A8 reviewer')\n    outcome=d['actual_outcome'];diag=outcome['actual_diagnostic']\n    if d['schema']!='ACTUAL_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1'or d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!=post['actual_summary_failure']or d['first_failure_secondary_errors']!=[]or outcome!=post['actual_summary_outcome_metadata']or diag!={'schema':'ACTUAL_BOOT_EXACT_FAILURE_STATUS_DIAGNOSTIC_V1','boot_plane':1,'actual_return_status':2,'required_committed_status':8}or outcome['actual_A9_failed_return_chain']!=[event]or outcome['actual_A8_failed_return_chain']!=[e8,e8door]or outcome['actual_A8_first_false_return']!=e8 or outcome['actual_BIND_failed_return_chain']!=[]or outcome['actual_first_admission_predicate']is not None or outcome['actual_native17_rejection']is not None or outcome['actual_failed_PHYS_group_inventory']['actual_inventory_header_events_observed']is not False or len(d['records'])!=3 or [x['status']for x in d['records']]!=['PASS','PASS','FAILED']or len(d['fixed_current_pins'])!=3788 or len(d['output_pins'])!=27 or d['engineering_qualified']is not False or d['full50_executed']is not False:raise RuntimeError('sealed A9 CORE233 status2/firstTB exact, no guessed mapped values or lifetime root cause')\n    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9,CLOSED_LATEST_A8]"

PROTECT=r'''def current_protection(sfpin,reviews):
    f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8608_manifest']);table={};roles={};cache={};historical=[]
    done=read(HISTORICAL_PINS['completed_A8_exact11_release']);post=read(HISTORICAL_PINS['completed_A8_exact11_postreview'])
    if done['manifest_pin']!=HISTORICAL_PINS['previous8608_manifest']or done['deleted_files']!=11 or done['logical_bytes_released']!=1330716816 or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_A8_exact11_release']:raise RuntimeError('previous genuine exact11 release immutable history')
    oldrows=old['current_protected_full_EOF_pins'];indices=HISTORICAL_TARGET_INDICES
    if len(oldrows)!=8608 or len(indices)!=9 or [b.norm(oldrows[i])for i in indices]!=TARGET_SELECTED_PINS[2:]or {p['path']for p in oldrows}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[2:]}:raise RuntimeError('MF8608 exact9 historical, all other8599 retained')
    def add(p,role):
        p=b.norm(p);path=p['path']
        if path in TARGET_PATHS:
            if p!=next(x for x in TARGET_SELECTED_PINS if x['path']==path):raise RuntimeError('only exact selected11 historical PFs')
            historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_ELEVEN_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return
        actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected PF or physical target alias changed')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):add(p,'previous8608_exact_index_'+str(i))
    before=inventory()
    if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=OWNER_FILE_COUNT or len(before['directory_identities'])!=OWNER_DIRECTORY_COUNT:raise RuntimeError('two exact complete closed owners unchanged')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_two_closed_owner_files');retained.append(p)
    if len(retained)!=OWNER_FILE_COUNT-11:raise RuntimeError('only exact11 removed from two owners')
    current12=inventory([V12_OUT])
    if current12!=V12_BASELINE:raise RuntimeError('current v12 unchanged')
    a=read(CLOSED_LATEST_A8['summary_pin']);hf=read(CLOSED_LATEST_A8['Host_freeze_pin']);hi=HISTORICAL_HF_TARGET_INDICES
    if len(hf['dependencies'])!=3787 or len(a['fixed_current_pins'])!=3788 or len(a['output_pins'])!=27:raise RuntimeError('exact current A8 3787/3788/27')
    if len(hi)!=9 or [b.norm(hf['dependencies'][i])for i in hi]!=TARGET_SELECTED_PINS[2:]or {p['path']for p in hf['dependencies']}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[2:]}:raise RuntimeError('HF3787 only exact9 old input rows historical')
    for p in [CLOSED_LATEST_A8['summary_pin'],CLOSED_LATEST_A8['Host_freeze_pin'],CLOSED_LATEST_A8['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']+a['owned_runtime_pins']:add(p,'latest_A8_exact11_history_only')
    scene=inventory([Path(CLOSED_LATEST_A8['actual_output_root'])])
    if set(scene['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{CLOSED_LATEST_A8['summary_pin']['path']}or scene['symlinks']or len(scene['ordinary_file_identities'])!=28:raise RuntimeError('latest A8 28 scene complete')
    for p in ROLE_KEEP_PINS:add(p,'original9_latestA8nine_current18_inputs_kept')
    for p in BIND_NEW_SOURCE_PINS:add(p,'all_existing_Fortran_and_A8_diagnostic_current_Source_proofs_kept')
    for origin in DOWNSTREAM_ORIGINS:
        d=read(origin['metadata_pin'])
        if [b.norm(x['current_pin'])for x in d['rows']]!=origin['current_pins']or len(d['rows'])!=origin['current_row_count']:raise RuntimeError('material33 GENDF51 unchanged')
        add(origin['metadata_pin'],'downstream_metadata')
        for p in origin['current_pins']:add(p,'downstream_science_current')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'Source_docs_history_proofs_kept')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_Source_tools0')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8608,only_exact_original_indices_migrated_to_historical=indices,all_original_other8599_PF_rows_data_retained=True,exact_current_HF3787_indices_migrated_to_historical=hi,explicit_exact11_historical_body_declarations=historical,two_owner_file_count=OWNER_FILE_COUNT,retained_other_file_count=len(retained),all_owner_directory_nodes_kept=True,all_original9_latestA8nine_current18_and_current70_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True),retained,before'''

 # Actual A8 442 predicate facts only; no claimed buffer lifetime root cause.
def main():
    if OUT.exists():raise RuntimeError('unique new Source namespace')
    rolepin=pin(ROLE);role=read(rolepin);rtp=pin(ROLE.with_name('TRUE_TOOL_RETURNS.json'));closed0(read(rtp),'actual_survey_return',rolepin)
    if role['schema']!='READONLY_NEXT_A8_CORE_EXACT11_PRIVATE_ROLE_AND_CURRENT_BUDGET_SURVEY_V1'or role['status']!='PASS_READONLY_EXACT11_CURRENT_ROLES_ORIGINAL_BUDGET_ONLY_NO_DELETION'or role['failure']is not None or role['candidate_count']!=11 or role['candidate_logical_bytes']!=TOTAL:raise RuntimeError('exact Root11 A8 role Source0')
    targets=[norm(x['target_pin'])for x in role['ordered_literal_candidate_role_rows']];keep=[norm(x)for x in role['retained_current18_original9_latest_A8_nine_input_pins']];next9=[norm(x)for x in role['next_exact_nine_source_input_copy_pins']]
    if len(targets)!=11 or len({p['path']for p in targets})!=11 or sum(p['size_bytes']for p in targets)!=TOTAL or len(keep)!=18 or len({p['path']for p in keep})!=18 or len(next9)!=9 or set(p['path']for p in keep)&set(p['path']for p in targets)or not set(p['path']for p in next9)<=set(p['path']for p in keep)or len({tuple(p['identity'][:2])for p in targets+keep})!=29:raise RuntimeError('exact11 and18 distinct current nodes')
    for p in targets+keep:
        s=Path(p['path']).lstat()
        if identity(s)!=p['identity']or not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('actual UID/regular/singlelink seven; original modes retained')
    oldsfpath=OLD/'COMPLETE_LITERAL11_NEXT_A8_CORE_DUPLICATES_SOURCE_FREEZE.json';oldsf=read(oldsfpath)
    for p in oldsf['Source_pins']:
        if pin(p['path'])!=p:raise RuntimeError('old Source PF')
    old=(OLD/'literal11_release_common.py').read_text();current=old;changes=[];const={}
    for n in ast.parse(old).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:const[n.targets[0].id]=ast.literal_eval(n.value)
            except(ValueError,TypeError):pass
    postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);posttools=role['genuine_latest_actual_post_true_tool_pin'];closed0(read(posttools),'actual_review_return',postpin)
    if post['schema']!='INDEPENDENT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_A8_247_FALSE_RETURN_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['verification_failure']is not None:raise RuntimeError('exact genuine current A8 post contract')
    latest=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_exact_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=postpin,independent_posttools_pin=posttools,actual_output_root=str(Path(post['actual_report_pin']['path']).parent))
    roots=[Path(x['root'])for x in role['current_owner_complete_inventory_scope']];baseline=inventory(roots);ownerfiles=sum(len(x['regular_files'])for x in role['current_owner_complete_inventory_scope']);ownerdirs=sum(len(x['directories'])for x in role['current_owner_complete_inventory_scope'])+len(roots)
    if len(roots)!=2 or baseline['symlinks']or len(baseline['ordinary_file_identities'])!=ownerfiles or len(baseline['directory_identities'])!=ownerdirs or len(set(baseline['ordinary_file_identities'])-set(p['path']for p in targets))!=ownerfiles-11:raise RuntimeError('exact survey two owners/counts')
    for x in role['current_owner_complete_inventory_scope']:
        got=inventory([Path(x['root'])])
        if got['ordinary_file_identities']!={p['path']:p['identity']for p in x['regular_files']}or set(got['directory_identities'])!=set(x['directories'])|{x['root']}:raise RuntimeError('survey complete owner identities unchanged')
    previous=role['current_MF8608_pin'];indices=role['current_MF8608_exact9_candidate_indices'];hi=role['current_HF3787_exact9_candidate_indices'];rows=read(previous)['current_protected_full_EOF_pins'];hf=read(latest['Host_freeze_pin'])
    if len(rows)!=8608 or len(indices)!=9 or [norm(rows[i])for i in indices]!=targets[2:]or len(hf['dependencies'])!=3787 or len(hi)!=9 or [norm(hf['dependencies'][i])for i in hi]!=targets[2:]:raise RuntimeError('only exact current MF/HF9 rows')
    completed=R/'independent_literal11_next_A8_core_actual_exact_release_postverify_20261014/REVIEW.json';completedpost=read(completed)
    hist=dict(const['HISTORICAL_PINS']);hist.update(previous8608_manifest=previous,previous_literal11_Source_freeze=pin(oldsfpath),completed_A8_exact11_release=completedpost['actual_release_receipt_pin'],completed_A8_exact11_postreview=pin(completed),completed_A8_exact11_posttools=pin(completed.with_name('TRUE_TOOL_RETURNS.json')),completed_A8_exact11_Root_tools=completedpost['actual_Root_true_tool_pin'],next_MCCGF_lifetime_exact11_role_review=rolepin,next_MCCGF_lifetime_exact11_role_tools=rtp,current_A8_Host_PLAN=role['current_Host_PLAN_pin'],current_A8_HF=role['current_HF3787_pin'],current_CAT3030=role['current_CAT3030_pin'],current_BIND2012=role['current_BIND2012_pin'])
    hist.update({'latest_A8_probe_'+k:v for k,v in latest.items()if isinstance(v,dict)and'path'in v})
    sourcepins=list(const['BIND_NEW_SOURCE_PINS']);a8dir=R/'boot_v16_A8_247_false_return_diagnostic_source_v1_20261014'
    a8sf=pin(a8dir/'COMPLETE_A8_247_FALSE_RETURN_DIAGNOSTIC_SOURCE_FREEZE.json');a8=read(a8sf)
    if a8['schema']!='COMPLETE_SPOR64_A8_247_FALSE_RETURN_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'or a8['source_only']is not True or a8['compiled']is not False or a8['numerical_executed']is not False:raise RuntimeError('actual A8 Source-only SF, never future compile success')
    for p in sorted(a8dir.iterdir()):
        if p.is_file():sourcepins.append(pin(p))
    for p in [R/'prepare_A8_247_false_return_diagnostic_source_only_v1_20261014.py',R/'prepare_A8_247_false_return_diagnostic_source_only_v2_20261014.py',R/'independent_A8_247_false_return_diagnostic_Fortran_Source_review_20261014/REVIEW.json',R/'independent_A8_247_false_return_diagnostic_Fortran_Source_review_20261014/TRUE_TOOL_RETURNS.json',R/'ACTUAL_A8_247_FALSE_RETURN_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json']:
        sourcepins.append(pin(p))
    sourcepins=list({p['path']:p for p in sourcepins}.values())
    for i,p in enumerate(sourcepins):hist['all_current_A8_Fortran_Source_'+str(i)]=p
    def change(before,after):
        nonlocal current
        if current.count(before)!=1:raise RuntimeError('unique exact Source splice')
        current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
    def node(name):return next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    def assign(name,value):change(ast.get_source_segment(current,node(name)),name+'='+repr(value))
    for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',indices),('BASELINE_OWNED_INVENTORIES',baseline),('ROLE_KEEP_PINS',keep),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('SOURCE_NAMES',NAMES)]:assign(k,v)
    change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
    change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal11_next_MCCGF_lifetime_duplicates_actual_receipts_20261014'\nCLOSED_LATEST_A8="+repr(latest))
    for k,n in [('HISTORICAL_HF_TARGET_INDICES',hi),('OWNER_FILE_COUNT',ownerfiles),('OWNER_DIRECTORY_COUNT',ownerdirs)]:assign(k,n)
    for k,n in [('SF','COMPLETE_LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(n))
    def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
    gate=fn('source_gate');change(gate,gate.replace('LITERAL11_NEXT_A8_CORE_DUPLICATES','LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES').replace("f['closed_latest_A9_probe_authority']!=CLOSED_LATEST_A9","f['closed_latest_A9_probe_authority']!=CLOSED_LATEST_A9 or f['closed_latest_A8_probe_authority']!=CLOSED_LATEST_A8"))
    disjoint=fn('disjoint');change(disjoint,disjoint)
    change(fn('current_protection'),PROTECT)
    change('    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY,CLOSED_LATEST_NATIVE,CLOSED_LATEST_A9]',A8_CLOSED)
    ast.parse(current);other=[]
    for oldname,newname in [('prepare_literal11_manifest.py',NAMES[1]),('verify_or_execute_literal11.py',NAMES[2])]:
        src=(OLD/oldname).read_text();new=src.replace('LITERAL11_NEXT_A8_CORE_DUPLICATES','LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES')
        ast.parse(new);other.append((oldname,newname,src,new))
    def funcs(s):return{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
    seven=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate'];f1=funcs(old);f2=funcs(current)
    if any(f1[n]!=f2[n]for n in seven):raise RuntimeError('seven lowlevel methods changed')
    start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";oldexe=other[1][2];newexe=other[1][3]
    if oldexe[oldexe.index(start):oldexe.index(end)]!=newexe[newexe.index(start):newexe.index(end)]:raise RuntimeError('unlink truth receipt dirfsync FirstFailure changed')
    for p in targets+keep:
        if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('target/input7 changed')
    if inventory(roots)!=baseline:raise RuntimeError('complete owner7 changed')
    OUT.mkdir();write(OUT/NAMES[0],current)
    for _,name,_,text in other:write(OUT/name,text)
    pp=OUT/'EXACT_LITERAL11_NEXT_MCCGF_LIFETIME_ROLE_SOURCE_PLAN.json';plan=dict(schema='EXACT_LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES_ROLE_SOURCE_PLAN_V1',source_only=True,literal11_fullpins=targets,target_count=11,target_bytes=TOTAL,previous8608_manifest_pin=previous,exact_previous_MF_indices_migrated_to_historical=indices,other8599_rows_unchanged=True,exact_current_HF3787_indices_migrated_to_historical=hi,current18_original9_latestA8nine_input_pins=keep,next_input_source_is_actual_latest_A8_nine=next9,current_two_owner_inventory=baseline,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_file_count=ownerfiles-11,explicit_only11_historical_bodies=True,current_latest_A8_probe_authority=latest,current_Fortran_Source_proof_pins=sourcepins,source_preparer_pin=pin(__file__),exact_role_survey_pin=rolepin,exact_role_survey_tools_pin=rtp,original_caps=const['CAPS'],no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,old_Source_MF_HF_summary_logs_science_never_rewritten=True,predicted_margin_is_not_actual_admission=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_release_tools_pin=None,future_actual_postrelease_review_pin=None,future_actual_postrelease_tools_pin=None,future_actual_postrelease_budget_admission=None,future_probe_Host_freeze_pin=None,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)
    write(pp,plan);entries=[dict(predecessor_pin=pin(OLD/'literal11_release_common.py'),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]
    for oldname,name,src,new in other:entries.append(dict(predecessor_pin=pin(OLD/oldname),candidate_pin=pin(OUT/name),changes=[dict(before=src,after=new)]))
    for e in entries:
        back=Path(e['candidate_pin']['path']).read_text()
        for c in reversed(e['changes']):
            if back.count(c['after'])!=1:raise RuntimeError('unique inverse splice')
            back=back.replace(c['after'],c['before'],1)
        if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('whole predecessor inverse')
    ip=OUT/'COMPLETE_LITERAL11_A8_TO_NEXT_MCCGF_LIFETIME_LITERAL11_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_LITERAL11_A8_TO_NEXT_MCCGF_LIFETIME_LITERAL11_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=seven,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True,manifest_prepared=False,deletion_executed=False))
    sf=dict(schema='COMPLETE_LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,original_caps=const['CAPS'],literal11_fullpins=targets,historical_evidence_pins=hist,current_actual_selections=const['CURRENT_SELECTIONS'],closed_failed_v15_authority=const['CLOSED_V15'],closed_failed_v16_authority=const['CLOSED_V16'],closed_diag4_authority=const['CLOSED_DIAG4'],closed_current_BOOTB_probe_authority=const['CLOSED_PROBE'],closed_latest_BIND_probe_authority=const['CLOSED_LATEST_BIND'],closed_latest_inventory_probe_authority=const['CLOSED_LATEST_INVENTORY'],closed_latest_native_probe_authority=const['CLOSED_LATEST_NATIVE'],closed_latest_A9_probe_authority=const['CLOSED_LATEST_A9'],closed_latest_A8_probe_authority=latest,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),original_resource_factory_pin=oldsf['original_resource_factory_pin'],predecessor_Source_freeze_pin=pin(oldsfpath),future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None)
    sp=OUT/'COMPLETE_LITERAL11_NEXT_MCCGF_LIFETIME_DUPLICATES_SOURCE_FREEZE.json';write(sp,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);os.fsync(fd);os.close(fd)
    print(json.dumps(dict(status='NEXT_MCCGF_LIFETIME_LITERAL11_SOURCE_ONLY_READY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),Source_preparer_pin=pin(__file__),target_count=11,target_bytes=TOTAL,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_count=ownerfiles-11,seven_lowlevel_methods_wholebytes_equal=True,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)))
if __name__=='__main__':main()

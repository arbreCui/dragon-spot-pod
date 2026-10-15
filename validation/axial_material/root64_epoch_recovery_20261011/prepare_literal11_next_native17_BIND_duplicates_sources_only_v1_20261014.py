"""Create exact eleven cleanup Sources only; never prepare MF, import cleanup, or delete."""
import ast, hashlib, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal3_next_BIND_inventory_duplicates_source_v1_20261014'
OUT=R/'storage_release_literal11_next_native17_BIND_duplicates_source_v1_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
MF_INDICES=[5618,5611,5613,5617,5612,5616,5619,5620,5621]
HF_INDICES=[2578,2571,2573,2577,2572,2576,2579,2580,2581]
TOTAL=1330716816
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata EOF only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        data=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('FD Source7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
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
def closed0(t,key,review):
    a=t[key]
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(a['exit_code'])is not int or a['exit_code']!=0 or a.get('session_id')is not None or norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=review:raise RuntimeError('genuine closed metadata reviewer0')

LATEST_CLOSED=r'''    d=read(CLOSED_LATEST_INVENTORY['summary_pin']);t=read(CLOSED_LATEST_INVENTORY['Root_true_tool_pin']);a=read(CLOSED_LATEST_INVENTORY['Root_exact_argv_pin']);post=read(CLOSED_LATEST_INVENTORY['independent_postreview_pin']);pt=read(CLOSED_LATEST_INVENTORY['independent_posttools_pin']);terminal=t['actual_terminal_return'];pr=pt['actual_review_return']
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['argv']or len(a['argv'])!=42:raise RuntimeError('genuine closed latest inventory Root42 terminal1')
    if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(pr['exit_code'])is not int or pr['exit_code']!=0 or pr.get('session_id')is not None or b.norm(json.loads(pr['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_LATEST_INVENTORY['independent_postreview_pin']:raise RuntimeError('genuine independent latest inventory actualpost0')
    if post['schema']!='INDEPENDENT_BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_BIND47_FAILED_PHYS_INVENTORY_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['verification_failure']is not None or post['failure']is not None or post['actual_report_pin']!=CLOSED_LATEST_INVENTORY['summary_pin']or post['actual_Root_true_tool_return_pin']!=CLOSED_LATEST_INVENTORY['Root_true_tool_pin']or post['actual_Root_exact_argv_pin']!=CLOSED_LATEST_INVENTORY['Root_exact_argv_pin']or post['actual_Host_freeze_pin']!=CLOSED_LATEST_INVENTORY['Host_freeze_pin']or post['actual_CLI_pin']!=CLOSED_LATEST_INVENTORY['exact_cli_pin']or post['actual_Root_exit_code']!=1 or post['actual_Root_closed']is not True or post['current_fixed_count']!=3640 or post['current_HF_dependency_count']!=3639 or post['actual_output_file_count']!=28 or post['all_three_watches_closed_without_limit_failure']is not True or post['current_fixed_all7_twice_verified']is not True or post['current_HF_all7_twice_verified']is not True or post['whole_scene_inventory_equals_exact_summary_output_pins_plus_summary']is not True or post['actual_original_first_failure_object_traceback_preserved']is not True or post['engineering_qualified']is not False:raise RuntimeError('exact latest failed inventory post; no engineering or physics qualification')
    if any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('independent readonly latest inventory actualpost')
    chain=post['actual_unique_BIND_failed_return_chain']
    if len(chain)!=3 or [x['predicate_id']for x in chain]!=['BIND64_RESPONSE_RETURN_L0236','BIND64_SYSTEM_RETURN_L0168','BIND64_READ_RETURN_L0097']or any(type(x['actual_boolean_status_integer'])is not int or x['actual_boolean_status_integer']!=0 for x in chain):raise RuntimeError('actual236 then168 then97 chain unchanged')
    inv=post['actual_failed_PHYS_complete_header_inventory'];begin=inv['actual_inventory_begin'];end=inv['actual_inventory_end'];caller=inv['actual_caller'];rows=inv['actual_inventory_records']
    if inv['actual_complete_header_inventory_observed']is not True or inv['actual_inventory_header_events_observed']is not True or inv['actual_record_payload_not_read_or_dumped']is not True or begin['schema']!='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1'or begin['event']!='begin'or begin['original_return_source_line']!=236 or begin['maximum_records']!=64 or begin['expected_schema']!='SCHEMA_RESPONSE_GROUP_PHYS'or begin['expected_count']!=15 or end['schema']!=begin['schema']or end['event']!='end'or end['original_return_source_line']!=236 or type(end['complete_integer'])is not int or end['complete_integer']!=1 or type(end['truncated_integer'])is not int or end['truncated_integer']!=0 or end['record_count']!=17 or len(rows)!=17 or [r['ordinal']for r in rows]!=list(range(1,18))or caller['schema']!=begin['schema']or caller['event']!='caller'or caller['original_return_source_line']!=168 or caller['group_index']!=1 or caller['plane_index']!=1 or post['actual_missing_expected_PHYS15_names']!=[]or post['inventory_data_is_only_group1_plane1_headers_not_payload_finiteness_or_full370_pass']is not True:raise RuntimeError('complete bounded group1 plane1 headers only, no payload/370 claim')
    extras=post['actual_only_two_native_extra_headers']
    if [(r['name_bytes_hex'],r['length'],r['type'])for r in extras]!=[('41584D41542D563634202020',14,4),('504A4A3634244D4343472020',8,4)]or any(r not in rows for r in extras):raise RuntimeError('exact observed two native headers, not arbitrary inventory extras')
    if d['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or d['failure']!="RuntimeError('own-child stage failed; no retry')"or d['first_failure_secondary_errors']!=[]or d['actual_outcome']!=post['actual_summary_outcome_metadata']or len(d['records'])!=3 or [x['status']for x in d['records']]!=['PASS','PASS','FAILED']or len(d['fixed_current_pins'])!=3640 or len(d['output_pins'])!=27 or d['engineering_qualified']is not False or d['full50_executed']is not False:raise RuntimeError('sealed latest failed inventory firstTB and real bounded headers retained')
    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND,CLOSED_LATEST_INVENTORY]'''

PROTECT=r'''def current_protection(sfpin,reviews):
    f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous8404_manifest']);table={};roles={};cache={};historical=[]
    done=read(HISTORICAL_PINS['completed_inventory_exact3_release']);post=read(HISTORICAL_PINS['completed_inventory_exact3_postreview'])
    if done['manifest_pin']!=HISTORICAL_PINS['previous8404_manifest']or done['deleted_files']!=3 or done['logical_bytes_released']!=1277838584 or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_inventory_exact3_release']:raise RuntimeError('previous exact3 actual release immutable history retained')
    oldrows=old['current_protected_full_EOF_pins'];indices=[5618,5611,5613,5617,5612,5616,5619,5620,5621]
    if len(oldrows)!=8404 or HISTORICAL_TARGET_INDICES!=indices or [b.norm(oldrows[i])for i in indices]!=TARGET_SELECTED_PINS[2:]or {p['path']for p in oldrows}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[2:]}:raise RuntimeError('MF8404 only exact nine input indices history; other8395 unchanged')
    def add(p,role):
        p=b.norm(p);path=p['path']
        if path in TARGET_PATHS:
            if p!=next(x for x in TARGET_SELECTED_PINS if x['path']==path):raise RuntimeError('only exact selected eleven historical PFs')
            historical.append(dict(original_body_pin=p,original_live_role=role,planned_next_role='EXACT_ELEVEN_PRIVATE_BODY_HISTORICAL',actual_retirement_not_yet_claimed=True));return
        actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected PF or physical target alias changed')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):add(p,'previous8404_exact_index_'+str(i))
    before=inventory()
    if before!=BASELINE_OWNED_INVENTORIES or before['symlinks']or len(before['ordinary_file_identities'])!=54 or len(before['directory_identities'])!=10:raise RuntimeError('two complete ordinary closed owners54files10dirs unchanged')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:p=pin(path);add(p,'all_other_latest_inventory_and_prior_BIND_closed_owner_files');retained.append(p)
    if len(retained)!=43:raise RuntimeError('exact eleven removal leaves43 other files')
    current12=inventory([V12_OUT])
    if current12!=V12_BASELINE:raise RuntimeError('current v12 namespace unchanged')
    a=read(CLOSED_LATEST_INVENTORY['summary_pin']);hf=read(CLOSED_LATEST_INVENTORY['Host_freeze_pin']);hi=[2578,2571,2573,2577,2572,2576,2579,2580,2581]
    if len(hf['dependencies'])!=3639 or len(a['fixed_current_pins'])!=3640 or len(a['output_pins'])!=27:raise RuntimeError('exact current inventory3639/3640/27')
    if [b.norm(hf['dependencies'][i])for i in hi]!=TARGET_SELECTED_PINS[2:]or {p['path']for p in hf['dependencies']}&TARGET_PATHS!={p['path']for p in TARGET_SELECTED_PINS[2:]}:raise RuntimeError('HF3639 only exact nine prior input indices history')
    for p in [CLOSED_LATEST_INVENTORY['summary_pin'],CLOSED_LATEST_INVENTORY['Host_freeze_pin'],CLOSED_LATEST_INVENTORY['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']+a['owned_runtime_pins']:add(p,'latest_inventory_exact11_history_only')
    scene=inventory([Path(CLOSED_LATEST_INVENTORY['actual_output_root'])])
    if set(scene['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{CLOSED_LATEST_INVENTORY['summary_pin']['path']}or scene['symlinks']or len(scene['ordinary_file_identities'])!=28:raise RuntimeError('latest28 scene complete')
    prior=inventory([Path(CLOSED_LATEST_BIND['actual_output_root'])])
    if len(prior['ordinary_file_identities'])!=26 or prior['symlinks']:raise RuntimeError('prior26 scene complete after previous exact3')
    for p in ROLE_KEEP_PINS:add(p,'original9_oldDiag8_oldBOOTB8_latestInventory9_current34_inputs_kept')
    for p in BIND_NEW_SOURCE_PINS:add(p,'inventory_Fortran_and_strict_native17_current_Source_proofs_kept')
    for origin in DOWNSTREAM_ORIGINS:
        d=read(origin['metadata_pin'])
        if [b.norm(x['current_pin'])for x in d['rows']]!=origin['current_pins']or len(d['rows'])!=origin['current_row_count']:raise RuntimeError('original material33 GENDF51 unchanged')
        add(origin['metadata_pin'],'downstream_metadata')
        for p in origin['current_pins']:add(p,'downstream_science_current')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'all_Source_docs_history_proofs_kept')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_Source0');add(t,who+'_Source_tools0')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=8404,only_exact_original_indices_migrated_to_historical=indices,all_original_other8395_PF_rows_data_retained=True,exact_current_HF3639_indices_migrated_to_historical=hi,explicit_exact_eleven_historical_body_declarations=historical,latest_inventory28_scene_other26_kept=True,prior_BIND26_scene_other17_kept=True,all43_other_files_and10_directory_nodes_kept=True,all_original9_oldDiag8_oldBOOTB8_latestInventory9_current34_and_current70_kept=True,old_SFs_MFs_reports_logs_raw_science_unchanged=True,current_target_owner_complete_inventory=before,current_v12_complete_inventory=current12,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True),retained,before'''

def main():
    if OUT.exists():raise RuntimeError('unique Source namespace')
    oldsfpath=OLD/'COMPLETE_LITERAL3_NEXT_BIND_INVENTORY_DUPLICATES_SOURCE_FREEZE.json';oldsf=read(oldsfpath)
    for p in oldsf['Source_pins']:
        if pin(p['path'])!=p:raise RuntimeError('old Source exactPF')
    old=(OLD/'literal3_release_common.py').read_text();current=old;changes=[];const={}
    for n in ast.parse(old).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:const[n.targets[0].id]=ast.literal_eval(n.value)
            except(ValueError,TypeError):pass
    rolepath=R/'readonly_next_native17_BIND_probe_exact11_private_role_and_current_budget_survey_20261014/REVIEW.json';role=read(rolepath);rolepin=pin(rolepath);rtp=pin(rolepath.with_name('TRUE_TOOL_RETURNS.json'));rt=read(rtp);closed0(rt,'actual_survey_return',rolepin)
    if role['schema']!='READONLY_NEXT_NATIVE17_BIND_PROBE_EXACT11_PRIVATE_ROLES_AND_CURRENT_BUDGET_SURVEY_V1'or role['status']!='PASS_READONLY_EXACT11_ROLE_AND_CURRENT_BUDGET_SURVEY_NOT_RELEASE_AUTHORIZATION'or role['failure']is not None or role['candidate_count']!=11 or role['candidate_logical_bytes']!=TOTAL or role['current_MF8404_exact9_candidate_indices']!=MF_INDICES or role['current_HF3639_exact9_candidate_indices']!=HF_INDICES:raise RuntimeError('genuine exact11 readonly role0, no release authorization')
    targets=[norm(x['pin'])for x in role['ordered_literal_candidate_role_rows']]
    if len(targets)!=11 or len({p['path']for p in targets})!=11 or sum(p['size_bytes']for p in targets)!=TOTAL:raise RuntimeError('eleven literal scope and bytes')
    for p in targets:
        s=Path(p['path']).lstat()
        if identity(s)!=p['identity']or not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('eleven current owned singlelink identities')
    postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);ptp=role['genuine_latest_actual_post_true_tool_pin'];closed0(read(ptp),'actual_review_return',postpin);probe=read(post['actual_report_pin'])
    latest=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_exact_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=postpin,independent_posttools_pin=ptp,actual_output_root=str(Path(post['actual_report_pin']['path']).parent))
    if post['actual_Root_exit_code']!=1 or post['verification_failure']is not None or post['failure']is not None or post['current_fixed_count']!=3640 or post['current_HF_dependency_count']!=3639 or post['actual_output_file_count']!=28:raise RuntimeError('exact actual closed latest inventory failure facts only')
    roots=[Path(latest['actual_output_root']),Path(const['CLOSED_LATEST_BIND']['actual_output_root'])];baseline=inventory(roots)
    if baseline['symlinks']or len(baseline['ordinary_file_identities'])!=54 or len(baseline['directory_identities'])!=10 or len(set(baseline['ordinary_file_identities'])-set(p['path']for p in targets))!=43:raise RuntimeError('two owners54 files10dirs exact11 removal43keep')
    for x in role['current_two_owner_complete_inventory_scope']:
        got=inventory([Path(x['owner_root'])])
        if got['ordinary_file_identities']!={p['path']:p['identity']for p in x['current_all_files']}or len(got['ordinary_file_identities'])!=x['current_regular_file_count']:raise RuntimeError('survey complete current owner files unchanged')
        for p in x['current_all_dirs']:
            if got['directory_identities'][p['path']]!=p['identity']:raise RuntimeError('survey directory7 unchanged')
    previous=role['current_MF8404_pin'];rows=read(previous)['current_protected_full_EOF_pins'];hf=read(latest['Host_freeze_pin'])
    if len(rows)!=8404 or [norm(rows[i])for i in MF_INDICES]!=targets[2:]or len(hf['dependencies'])!=3639 or [norm(hf['dependencies'][i])for i in HF_INDICES]!=targets[2:]:raise RuntimeError('only exact MF/HF nine input rows')
    completed=R/'independent_literal3_next_BIND_inventory_actual_exact_release_postverify_20261014/REVIEW.json';completedpost=read(completed)
    hist=dict(const['HISTORICAL_PINS']);hist.update(previous_inventory_literal3_Source_freeze=pin(oldsfpath),previous8404_manifest=previous,completed_inventory_exact3_release=completedpost['actual_release_receipt_pin'],completed_inventory_exact3_postreview=pin(completed),completed_inventory_exact3_posttools=pin(completed.with_name('TRUE_TOOL_RETURNS.json')),completed_inventory_exact3_Root_tools=completedpost['actual_Root_true_tool_pin'],next_native17_exact11_role_review=rolepin,next_native17_exact11_role_tools=rtp,current_inventory_Host_PLAN=role['current_Host_PLAN_pin'],current_inventory_HF=role['current_HF3639_pin'],current_CAT3030=role['current_CAT3030_pin'],current_BIND2012=role['current_BIND2012_pin'])
    hist.update({'latest_inventory_probe_'+k:v for k,v in latest.items()if isinstance(v,dict)and'path'in v})
    native=R/'boot_v16_BIND64_strict_native17_consumer_source_v1_20261014';expected=('SPOR64_BOOT_BIND64.f90','COMPLETE_NATIVE17_CONSUMER_SOURCE_WHOLE_BYTE_INVERSE.json','SOURCE_ONLY_STRICT_NATIVE17_CONSUMER_PLAN.json','READY.json','TRUE_TOOL_RETURNS.json');nativepins=[pin(native/n)for n in expected]
    bindtable={p['path']:p for p in const['BIND_NEW_SOURCE_PINS']}
    for i,p in enumerate(nativepins):bindtable[p['path']]=p;hist['strict_native17_current_Source_'+str(i)]=p
    bindpins=sorted(bindtable.values(),key=lambda p:p['path']);keep=[norm(p)for p in role['current34_original9_oldDiag8_oldBOOTB8_newest_inventory9_preserved_input_pins']];nextnine=[norm(p)for p in role['next_exact_nine_source_input_copy_pins']]
    if len(keep)!=34 or len({p['path']for p in keep})!=34 or len(nextnine)!=9 or set(p['path']for p in keep)&set(p['path']for p in targets)or not set(p['path']for p in nextnine)<=set(p['path']for p in keep):raise RuntimeError('truthful34 current and exactlatest9 next inputs disjoint targets')
    for p in keep:
        if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('kept input7 changed; no body EOF repeat')
    def change(before,after):
        nonlocal current
        if current.count(before)!=1:raise RuntimeError('unique Source splice')
        current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
    def node(name):return next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    def assignment(name,value):change(ast.get_source_segment(current,node(name)),name+'='+repr(value))
    for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',MF_INDICES),('BASELINE_OWNED_INVENTORIES',baseline),('ROLE_KEEP_PINS',keep),('BIND_NEW_SOURCE_PINS',bindpins),('BYTES',TOTAL),('SOURCE_NAMES',NAMES)]:assignment(k,v)
    change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(p)for p in roots])+']')
    change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal11_next_native17_BIND_duplicates_actual_receipts_20261014'\nCLOSED_LATEST_INVENTORY="+repr(latest))
    for k,name in [('SF','COMPLETE_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(name))
    def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
    gate=fn('source_gate');newgate=gate.replace('LITERAL3_NEXT_BIND_INVENTORY_DUPLICATES','LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES').replace('literal3_fullpins','literal11_fullpins').replace("or f['closed_latest_BIND_probe_authority']!=CLOSED_LATEST_BIND", "or f['closed_latest_BIND_probe_authority']!=CLOSED_LATEST_BIND or f['closed_latest_inventory_probe_authority']!=CLOSED_LATEST_INVENTORY").replace('len(TARGETS)!=3 or len(TARGET_PATHS)!=3','len(TARGETS)!=11 or len(TARGET_PATHS)!=11');change(gate,newgate)
    change(fn('current_protection'),PROTECT)
    change('    return [OWNER,CLOSED_V15,CLOSED_V16,CLOSED_DIAG4,CLOSED_PROBE,CLOSED_LATEST_BIND]',LATEST_CLOSED)
    ast.parse(current)
    other=[]
    for oldname,newname in [('prepare_literal3_manifest.py',NAMES[1]),('verify_or_execute_literal3.py',NAMES[2])]:
        src=(OLD/oldname).read_text();new=src.replace('LITERAL3_NEXT_BIND_INVENTORY_DUPLICATES','LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES').replace('import literal3_release_common as s','import literal11_release_common as s').replace('selected_literal3_Source_reviews','selected_literal11_Source_reviews').replace('target_count=3','target_count=11').replace("m['target_count']!=3","m['target_count']!=11").replace('deleted_files=3','deleted_files=11').replace("before['regular_files']-after['regular_files']!=3","before['regular_files']-after['regular_files']!=11")
        ast.parse(new);other.append((oldname,newname,src,new))
    def funcs(src):return{n.name:ast.get_source_segment(src,n)for n in ast.parse(src).body if isinstance(n,ast.FunctionDef)}
    names=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate'];f1=funcs(old);f2=funcs(current)
    if any(f1[n]!=f2[n]for n in names):raise RuntimeError('seven frozen lowlevel methods changed')
    start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";oldexe=other[1][2];newexe=other[1][3]
    if oldexe[oldexe.index(start):oldexe.index(end)]!=newexe[newexe.index(start):newexe.index(end)]:raise RuntimeError('whole truthful unlink receipt dirfsync FirstFailure body changed')
    for p in targets+keep:
        if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('final target/input7 unchanged')
    if inventory(roots)!=baseline:raise RuntimeError('complete owner7 unchanged before Source publication')
    OUT.mkdir();write(OUT/NAMES[0],current)
    for _,name,_,s in other:write(OUT/name,s)
    pp=OUT/'EXACT_LITERAL11_NEXT_NATIVE17_BIND_ROLE_SOURCE_PLAN.json'
    plan=dict(schema='EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_ROLE_SOURCE_PLAN_V1',source_only=True,literal11_fullpins=targets,target_count=11,target_bytes=TOTAL,previous8404_manifest_pin=previous,exact_previous_MF_indices_migrated_to_historical=MF_INDICES,other8395_rows_unchanged=True,exact_current_HF3639_indices_migrated_to_historical=HF_INDICES,latest_inventory_scene28_to26_current=True,prior_BIND_scene26_to17_current=True,all43_other_files_and10_directory_nodes_kept=True,current34_original9_oldDiag8_oldBOOTB8_latestInventory9_input_pins=keep,next_input_source_is_actual_latest_inventory9=nextnine,explicit_only_eleven_historical_bodies=True,current_latest_inventory_probe_authority=latest,current_target_owner_inventory=baseline,current_inventory_and_native17_Fortran_Source_pins=bindpins,native17_current_five_Source_pins=nativepins,native17_future_Source_freeze_pin=None,current_fortran_future_compile_object_and_HF_not_claimed=True,source_preparer_pin=pin(__file__),exact_role_survey_pin=rolepin,exact_role_survey_tools_pin=rtp,original_caps=const['CAPS'],no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,old_Source_MF_HF_summary_logs_science_never_rewritten=True,legacy_v15_named_fields_describe_explicit_current_owner_roots_not_new_v15_deletions=True,predicted_margin_is_not_actual_admission=True,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_release_tools_pin=None,future_actual_postrelease_review_pin=None,future_actual_postrelease_tools_pin=None,future_actual_postrelease_budget_admission=None,future_probe_Host_freeze_pin=None,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)
    write(pp,plan);entries=[dict(predecessor_pin=pin(OLD/'literal3_release_common.py'),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]
    for oldname,name,src,new in other:entries.append(dict(predecessor_pin=pin(OLD/oldname),candidate_pin=pin(OUT/name),changes=[dict(before=src,after=new)]))
    for e in entries:
        back=Path(e['candidate_pin']['path']).read_text()
        for c in reversed(e['changes']):
            if back.count(c['after'])!=1:raise RuntimeError('unique wholeinverse splice')
            back=back.replace(c['after'],c['before'],1)
        if back.encode()!=Path(e['predecessor_pin']['path']).read_bytes():raise RuntimeError('whole predecessor inverse')
    ip=OUT/'COMPLETE_PREVIOUS_LITERAL3_TO_NEXT_NATIVE17_BIND_LITERAL11_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_PREVIOUS_LITERAL3_TO_NEXT_NATIVE17_BIND_LITERAL11_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=names,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True,manifest_prepared=False,deletion_executed=False))
    sf=dict(schema='COMPLETE_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,original_caps=const['CAPS'],literal11_fullpins=targets,historical_evidence_pins=hist,current_actual_selections=const['CURRENT_SELECTIONS'],closed_failed_v15_authority=const['CLOSED_V15'],closed_failed_v16_authority=const['CLOSED_V16'],closed_diag4_authority=const['CLOSED_DIAG4'],closed_current_BOOTB_probe_authority=const['CLOSED_PROBE'],closed_latest_BIND_probe_authority=const['CLOSED_LATEST_BIND'],closed_latest_inventory_probe_authority=latest,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pin(pp),strict_low_level_Source_provenance_pin=pin(ip),Source_preparer_pin=pin(__file__),original_resource_factory_pin=oldsf['original_resource_factory_pin'],predecessor_Source_freeze_pin=pin(oldsfpath),future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_native17_Fortran_Source_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None)
    sp=OUT/'COMPLETE_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_SOURCE_FREEZE.json';write(sp,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);os.fsync(fd);os.close(fd)
    print(json.dumps(dict(status='NEXT_NATIVE17_BIND_LITERAL11_SOURCE_ONLY_READY_NO_MF_NO_DELETE',Source_freeze_pin=pin(sp),Source_pins=sf['Source_pins'],plan_pin=pin(pp),inverse_pin=pin(ip),Source_preparer_pin=pin(__file__),target_count=11,target_bytes=TOTAL,seven_lowlevel_methods_wholebytes_equal=True,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False)))
if __name__=='__main__':main()

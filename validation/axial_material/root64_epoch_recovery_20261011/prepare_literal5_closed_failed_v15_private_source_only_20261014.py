"""Prepare only new exact5 Source and metadata; never import candidates or release files."""
import ast, copy, difflib, hashlib, json, os, shlex, stat
from pathlib import Path

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'storage_release_literal2_old_v14_BQ_source_v2_20261014'
OUT=REC/'storage_release_literal5_closed_failed_v15_private_source_v1_20261014'
seen={}
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);s=p.lstat();i=ids(s)
    assert p.is_absolute() and stat.S_ISREG(s.st_mode)
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        assert ids(os.fstat(f.fileno()))==i;raw=f.read();assert ids(os.fstat(f.fileno()))==i
    assert ids(p.lstat())==i
    pf=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
    seen[str(p)]=(pf,raw);return pf,raw
def read(path):
    pf,raw=pin(path);return json.loads(raw),pf
def write(name,value):
    raw=value.encode()if isinstance(value,str)else(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    fd=os.open(OUT/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return pin(OUT/name)[0]
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def actual7(p):
    s=Path(p['path']).lstat();assert stat.S_ISREG(s.st_mode) and ids(s)==p['identity']
def inventory(roots):
    files={};dirs={};links={};stack=list(map(Path,roots))
    while stack:
        p=stack.pop();before=ids(p.lstat());assert stat.S_ISDIR(before[2]);dirs[str(p)]=before
        with os.scandir(p)as entries:
            for e in entries:
                q=p/e.name;s=e.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):stack.append(q)
                elif stat.S_ISREG(s.st_mode):files[str(q)]=ids(s)
                elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=ids(s),target=os.readlink(q))
                else:raise RuntimeError('special owner entry')
        assert ids(p.lstat())==before
    return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)
def closed_review(d,p,t):
    a=t['actual_review_return']
    assert d['failure']is None and t['observed_closed']is True
    if 'original_integer_exit_code'in t:assert type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0
    assert type(a['exit_code'])is int and a['exit_code']==0 and a.get('session_id')is None and norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])==p

assert not OUT.exists()
oldsf,oldsfpf=read(OLD/'COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json')
oldmf,oldmfpf=read(OLD/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json')
done,donepf=read(REC/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014/ACTUAL_EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_OLD_PRIVATE_RELEASE_RECEIPT.json')
oldpost,oldpostpf=read(REC/'independent_literal2_old_v14_BQ_v2_actual_postverify_20261014/REVIEW.json')
oldtools,oldtoolpf=read(REC/'independent_literal2_old_v14_BQ_v2_actual_postverify_20261014/TRUE_TOOL_RETURNS.json')
closed_review(oldpost,oldpostpf,oldtools)
assert done['manifest_pin']==oldmfpf and done['deleted_files']==2 and done['logical_bytes_released']==528482632 and oldpost['actual_release_receipt_pin']==donepf
vs,vspf=read(REC/'post_v15_failed_v14_private_storage_literal_role_readonly_survey_20261014/REVIEW.json')
vt,vtpf=read(REC/'post_v15_failed_v14_private_storage_literal_role_readonly_survey_20261014/TRUE_TOOL_RETURNS.json');closed_review(vs,vspf,vt)
ps,pspf=read(REC/'independent_failed_public5_literal2_bundle_storage_role_survey_20261014/REVIEW.json')
pt,ptpf=read(REC/'independent_failed_public5_literal2_bundle_storage_role_survey_20261014/TRUE_TOOL_RETURNS.json');closed_review(ps,pspf,pt)
targets=vs['principal_exact3_pins']+ps['exact_target_full_EOF_pins'];targetpaths={p['path']for p in targets}
indices=[4160,4161,4294,4607,4612]
assert len(targets)==len(targetpaths)==5 and sum(p['size_bytes']for p in targets)==1478165640
assert {oldmf['current_protected_full_EOF_pins'][i]['path']:norm(oldmf['current_protected_full_EOF_pins'][i])for i in indices}=={p['path']:norm(p)for p in targets}
for p in targets:
    actual7(p);s=Path(p['path']).lstat();assert s.st_uid==os.getuid() and s.st_nlink==1
assert len({tuple(p['identity'][:2])for p in targets})==5

vpost,vpostpf=read(REC/'independent_v15_GLOBAL_own_child512_failure_postverify_20261014/REVIEW.json')
vtools,vtoolpf=read(REC/'independent_v15_GLOBAL_own_child512_failure_postverify_20261014/TRUE_TOOL_RETURNS.json');closed_review(vpost,vpostpf,vtools)
summary,sumpf=read(vpost['summary_pin']['path']);roottool,roottoolpf=read(vpost['genuine_closed_actual_Root_tool_pin']['path']);argv,argpf=read(vpost['Root_exact_argv_pin']['path'])
assert roottoolpf==vpost['genuine_closed_actual_Root_tool_pin'] and sumpf==vpost['summary_pin'] and argpf==vpost['Root_exact_argv_pin']
assert roottool['observed_closed']is True and type(roottool['original_integer_exit_code'])is int and roottool['original_integer_exit_code']==1
terminal=roottool['actual_terminal_return'];assert type(terminal['exit_code'])is int and terminal['exit_code']==1 and terminal.get('session_id')is None
assert shlex.split(roottool['exact_executed_command'])==argv['argv'] and len(argv['argv'])==78
assert summary['status']=='FAILED_UNQUALIFIED_NO_RETRY' and summary['failure']=='RuntimeError: own-child 512 MiB RSS cap reached'
assert len(summary['records'])==33 and len(summary['fixed_current_pins'])==3011 and len(summary['output_pins'])==191 and len(summary['owned_runtime_pins'])==119
assert vpost['actual_pipeline_tool_exit_code']==1 and vpost['actual_record_count']==33 and vpost['actual_PASS_records']==13 and vpost['exact_expected_refusal_records']==19 and vpost['genuine_unexpected_global_failure_records']==1
assert vpost['all3011_fixed_seven_id_before_after_equal']is True and vpost['complete_actual_OUT_inventory_equal_published_outputs_plus_summary']is True
assert not summary['engineering_three_plane_closed0'] and not summary['AAA_qualified'] and not summary['ABA_admitted']
closed_v15=dict(summary_pin=sumpf,Root_true_tool_pin=roottoolpf,Root_exact_argv_pin=argpf,independent_postreview_pin=vpostpf,independent_posttools_pin=vtoolpf,Host_freeze_pin=vpost['host_freeze_pin'],exact_cli_pin=vpost['CLI_pin'],full_raw_records_pin=vpost['full_raw_records_pin'],stages_pin=vpost['stages_pin'],actual_output_root=str(Path(sumpf['path']).parent),actual_status=summary['status'],actual_failure=summary['failure'],actual_records=33,actual_PASS=13,actual_expected_refusals=19,actual_unexpected_GLOBAL_failure=1,actual_fixed_count=3011,actual_output_count=191,actual_owned_count=119,actual_Root_exit_code=1,AAA_qualified=False,ABA_admitted=False)

oldcommonpf,oldraw=pin(OLD/'literal2_release_common.py');oldtext=oldraw.decode();oldtree=ast.parse(oldtext)
assigns={n.targets[0].id:ast.literal_eval(n.value)for n in oldtree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ('BASE_PIN','CAPS','HISTORICAL_PINS','CURRENT_SELECTIONS','OWNER')}
functions={n.name:ast.get_source_segment(oldtext,n)for n in oldtree.body if isinstance(n,ast.FunctionDef)}
current=copy.deepcopy(assigns['CURRENT_SELECTIONS'])
public7hf,public7hpf=read(REC/'public_read_compact_bq_admission_control_host_source_v7_20261014/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')
public7,public7pf=read('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7/Root_actual_control_summary.json')
_,public7cli=read(REC/'public_read_compact_bq_admission_control_host_source_v7_20261014/ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json')
current.append(dict(role='public7',Host_freeze_pin=public7hpf,actual_report_pin=public7pf,exact_cli_pin=public7cli,actual_output_root=str(Path(public7pf['path']).parent),actual_status=public7['status'],actual_failure=public7['failure'],expected_dependency_count=len(public7hf['dependencies']),actual_fixed_count=len(public7['fixed_current_pins']),actual_output_count=len(public7['output_pins'])))
assert public7['failure']is None and public7['actual_seven_genuine_public_READ_controls_passed']is True
retainedrows=oldmf['current_protected_full_EOF_pins'];assert len(retainedrows)==7251
for i,p in enumerate(retainedrows):
    if i not in indices:actual7(p)
for selection in current:
    hf,hpf=read(selection['Host_freeze_pin']['path']);report,rpf=read(selection['actual_report_pin']['path'])
    assert hpf==selection['Host_freeze_pin'] and rpf==selection['actual_report_pin']
    for p in [hf['host_source']]+hf['dependencies']+report['fixed_current_pins']+report['output_pins']+report.get('owned_runtime_pins',[]):
        if p['path']in targetpaths:
            assert selection['role']=='public5_failed' and norm(p)in targets
        else:actual7(p)
v15hf,v15hpf=read(closed_v15['Host_freeze_pin']['path']);assert v15hpf==closed_v15['Host_freeze_pin'] and len(v15hf['dependencies'])==2802
for p in [v15hf['host_source']]+v15hf['dependencies']+summary['fixed_current_pins']+summary['output_pins']+summary['owned_runtime_pins']:
    assert p['path']not in targetpaths;actual7(p)

origins=[]
for name,count in [('current_formal_material_authority_exact_cache70_source_v7/EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json',33),('current_eleven_saved_gendf_current_mount_host_source_v4/COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json',51)]:
    d,pf=read(REC/name);assert len(d['rows'])==count
    rows=[norm(x['current_pin'])for x in d['rows']]
    for p in rows:assert p['path']not in targetpaths;actual7(p)
    origins.append(dict(metadata_pin=pf,current_row_count=count,current_pins=rows))

v14=Path(targets[0]['path']).parents[1];pub5=Path(targets[3]['path']).parents[1]
baseline=inventory([v14,pub5]);assert not baseline['symlinks'] and len(baseline['ordinary_file_identities'])==328
expected=copy.deepcopy(oldmf['complete_before_inventory'])
for p in done['deletion_records']:del expected['ordinary_file_identities'][p['original_fullpin']['path']]
for p in done['affected_parent_changes']:expected['directory_identities'][p['path']]=p['after']
assert inventory([v14])==expected
pub5inv=inventory([pub5]);assert pub5inv['ordinary_file_identities']==ps['failed_public5_current31_file_inventory'] and {p:i for p,i in pub5inv['directory_identities'].items()if p!=str(pub5)}==ps['failed_public5_directory_inventory'] and not pub5inv['symlinks']
v12=oldmf['Source_DAG_provenance']['current_v12_complete_inventory'];assert inventory(['/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12'])==v12
hist=copy.deepcopy(assigns['HISTORICAL_PINS'])
hist.update(previous_literal2_Source_freeze=oldsfpf,previous7251_manifest=oldmfpf,completed_actual_literal2_release=donepf,completed_independent_literal2_postreview=oldpostpf,completed_independent_literal2_posttools=oldtoolpf,v14_principal_and_alias_survey=vspf,v14_principal_and_alias_survey_tools=vtpf,failed_public5_exact2_survey=pspf,failed_public5_exact2_survey_tools=ptpf)
hist.update({k:p for k,p in closed_v15.items()if k.endswith('_pin')})
for x in origins:hist['downstream_origin_'+str(x['current_row_count'])]=x['metadata_pin']

custom=r'''
def source_gate(sfpin):
    if sfpin['path']!=str(SF):raise RuntimeError('exact literal5 Source namespace')
    f=read(sfpin)
    if f['schema']!='COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_ONLY_FREEZE_V1'or f['source_only']is not True or f['manifest_prepared']is not False or f['deletion_executed']is not False or f['compiler_or_business_executed']is not False or f['original_caps']!=CAPS or f['literal5_fullpins']!=TARGET_SELECTED_PINS or f['historical_evidence_pins']!=HISTORICAL_PINS or f['current_actual_selections']!=CURRENT_SELECTIONS or f['closed_failed_v15_authority']!=CLOSED_V15:raise RuntimeError('exact immutable5 scope/caps/roles')
    if [p['path']for p in f['Source_pins']]!=[str(PKG/n)for n in SOURCE_NAMES]:raise RuntimeError('three exact Source files')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:same(p)
    same(f['original_resource_factory_pin'])
    if f['original_resource_factory_pin']['path']!=str(b.FACTORY):raise RuntimeError('original exact resource factory')
    if len(TARGETS)!=5 or len(TARGET_PATHS)!=5 or sum(p['size_bytes']for p in TARGET_SELECTED_PINS)!=BYTES:raise RuntimeError('no expanded target selector')
    return f

def closed_proofs():
    s=read(OWNER['summary_pin']);raw=read(OWNER['complete_raw_pin']);stages=read(OWNER['stages_pin']);w=read(OWNER['last_watchdog_pin'])
    compact=lambda rs:[{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in rs]
    if s['failure']!=OWNER['actual_failure']or s['engineering_three_plane_closed0']is not False or s['actual_terminal']is not None or s['AAA_qualified']is not False or compact(s['records'])!=compact(raw['records'])or stages!={'stages':raw['records']}or len(s['records'])!=OWNER['actual_record_count']or type(w['returncode'])is not int or w['returncode']!=OWNER['actual_last_child_integer_returncode']or w['own_child_only']is not True or w['liveness_group_cleanup']is not True:raise RuntimeError('exact historical failed v14 closed owner')
    v=read(CLOSED_V15['summary_pin']);t=read(CLOSED_V15['Root_true_tool_pin']);a=read(CLOSED_V15['Root_exact_argv_pin']);post=read(CLOSED_V15['independent_postreview_pin']);pt=read(CLOSED_V15['independent_posttools_pin']);terminal=t['actual_terminal_return'];pa=pt['actual_review_return']
    if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['argv']or len(a['argv'])!=78:raise RuntimeError('genuine closed exactargv Root failed terminal1 required')
    if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0 or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or b.norm(json.loads(pa['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_V15['independent_postreview_pin']:raise RuntimeError('genuine independent failed-v15 post0 required')
    if post['failure']is not None or post['summary_pin']!=CLOSED_V15['summary_pin']or post['genuine_closed_actual_Root_tool_pin']!=CLOSED_V15['Root_true_tool_pin']or post['Root_exact_argv_pin']!=CLOSED_V15['Root_exact_argv_pin']or post['host_freeze_pin']!=CLOSED_V15['Host_freeze_pin']or post['actual_pipeline_tool_exit_code']!=1 or post['actual_record_count']!=33 or post['actual_PASS_records']!=13 or post['exact_expected_refusal_records']!=19 or post['genuine_unexpected_global_failure_records']!=1 or post['all3011_fixed_seven_id_before_after_equal']is not True or post['complete_actual_OUT_inventory_equal_published_outputs_plus_summary']is not True:raise RuntimeError('exact independent actual failure authority')
    if v['status']!=CLOSED_V15['actual_status']or v['failure']!=CLOSED_V15['actual_failure']or v['engineering_three_plane_closed0']is not False or v['actual_terminal']is not None or v['AAA_qualified']is not False or v['ABA_admitted']is not False or len(v['records'])!=33 or len(v['fixed_current_pins'])!=3011 or len(v['output_pins'])!=191 or len(v['owned_runtime_pins'])!=119:raise RuntimeError('failed v15 remains unqualified')
    vr=read(CLOSED_V15['full_raw_records_pin']);vs=read(CLOSED_V15['stages_pin'])
    if compact(v['records'])!=compact(vr['records'])or vs!={'stages':vr['records']}:raise RuntimeError('full actual33 records unchanged')
    return [OWNER,CLOSED_V15]

def current_protection(sfpin,reviews):
    f=source_gate(sfpin);closed_proofs();old=read(HISTORICAL_PINS['previous7251_manifest']);done=read(HISTORICAL_PINS['completed_actual_literal2_release']);post=read(HISTORICAL_PINS['completed_independent_literal2_postreview']);table={};roles={};cache={}
    if done['deleted_files']!=2 or done['logical_bytes_released']!=528482632 or done['manifest_pin']!=HISTORICAL_PINS['previous7251_manifest']or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_actual_literal2_release']:raise RuntimeError('completed prior literal2 immutable evidence')
    oldrows=old['current_protected_full_EOF_pins']
    if len(oldrows)!=7251 or {oldrows[i]['path']:b.norm(oldrows[i])for i in HISTORICAL_TARGET_INDICES}!={p['path']:p for p in TARGET_SELECTED_PINS}or {p['path']for p in oldrows}&TARGET_PATHS!=TARGET_PATHS:raise RuntimeError('only exact5 previous7251 declarations may migrate')
    def add(p,role):
        p=b.norm(p);path=p['path'];actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or path in TARGET_PATHS or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected exactPF changed or aliases target')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):
        if i not in HISTORICAL_TARGET_INDICES:add(p,'previous7246_rows_unmodified_current')
    before=inventory()
    if before!=BASELINE_OWNED_INVENTORIES or len(before['ordinary_file_identities'])!=328 or before['symlinks']:raise RuntimeError('exact v14 remaining297 plus failedpub5 entire31 inventory')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:
            actual=pin(path);add(actual,'all_other323_v14_and_failedpublic5_files_retained');retained.append(actual)
    current12=inventory([V12_OUT])
    if current12!=V12_BASELINE:raise RuntimeError('whole v12 current namespace unchanged')
    for selected in CURRENT_SELECTIONS:
        hf=read(selected['Host_freeze_pin']);a=read(selected['actual_report_pin']);read(selected['exact_cli_pin'])
        if len(hf['dependencies'])!=selected['expected_dependency_count']or len(a['fixed_current_pins'])!=selected['actual_fixed_count']or len(a['output_pins'])!=selected['actual_output_count']or a['status']!=selected['actual_status']or a['failure']!=selected['actual_failure']or a['actual_host_Source_freeze_pin']!=selected['Host_freeze_pin']:raise RuntimeError('selected current Host/report identity and counts/status')
        rows=[selected['Host_freeze_pin'],selected['actual_report_pin'],selected['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']+a.get('owned_runtime_pins',[])
        for p in rows:
            if p['path']in TARGET_PATHS:
                if selected['role']!='public5_failed'or b.norm(p)not in TARGET_SELECTED_PINS:raise RuntimeError('only exact failedpublic5 target output/owned historical rows')
            else:add(p,'current_'+selected['role']+'_entire_HF_ownHost_actual_fixed_output_owned_summary')
        actual_inventory=inventory([Path(selected['actual_output_root'])])
        if set(actual_inventory['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{selected['actual_report_pin']['path']}or actual_inventory['symlinks']:raise RuntimeError('complete selected actual output scene')
    hf=read(CLOSED_V15['Host_freeze_pin']);v=read(CLOSED_V15['summary_pin'])
    if len(hf['dependencies'])!=2802:raise RuntimeError('exact v15 HF2802')
    for p in [CLOSED_V15['Host_freeze_pin'],CLOSED_V15['summary_pin'],CLOSED_V15['exact_cli_pin'],hf['host_source']]+hf['dependencies']+v['fixed_current_pins']+v['output_pins']+v['owned_runtime_pins']:add(p,'closed_failed_v15_all3011_fixed119_owned192_scene_and_HF')
    actual_v15=inventory([Path(CLOSED_V15['actual_output_root'])])
    if set(actual_v15['ordinary_file_identities'])!={p['path']for p in v['output_pins']}|{CLOSED_V15['summary_pin']['path']}or len(actual_v15['ordinary_file_identities'])!=192 or actual_v15['symlinks']:raise RuntimeError('failed v15 complete192 physical scene')
    for origin in DOWNSTREAM_ORIGINS:
        d=read(origin['metadata_pin'])
        if [b.norm(x['current_pin'])for x in d['rows']]!=origin['current_pins']or len(d['rows'])!=origin['current_row_count']:raise RuntimeError('exact downstream material33 GENDF51 current authority')
        add(origin['metadata_pin'],'downstream_current_origin_metadata')
        for p in origin['current_pins']:add(p,'downstream_current_science_Source_kept')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin,f['exact_role_plan_pin'],f['strict_low_level_Source_provenance_pin'],f['Source_preparer_pin']]:add(p,'Source_and_completed_historical_metadata_retained_as_files')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_actual_source0');add(t,who+'_actual_source0_tools')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=7251,only_exact_five_original_indices_migrated_to_historical=HISTORICAL_TARGET_INDICES,all_original_other7246_PF_rows_data_retained=True,old7251_manifest_and_all_historical_reports_unmodified=True,current_v14_and_failedpublic5_complete_inventory=before,current_v12_complete_inventory=current12,current_v15_complete_inventory=actual_v15,closed_failed_v15_is_not_engineering_or_physics_PASS=True,eight_v14_private_aliases_and_SPOASM_retained=True,no_catalog_or_BIND_change=True,no_generic_missing_pin_skip=True),retained,before
'''
header='''"""Exact5 obsolete failed-run private files; readonly default, no retry."""
import ast,hashlib,importlib.util,json,os,shlex,stat,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';PKG=Path(__file__).absolute().parent
'''
constants='\n'.join(f'{k}={v!r}'for k,v in dict(BASE_PIN=assigns['BASE_PIN'],CAPS=assigns['CAPS'],HISTORICAL_PINS=hist,CURRENT_SELECTIONS=current,OWNER=assigns['OWNER'],CLOSED_V15=closed_v15,TARGET_SELECTED_PINS=targets,HISTORICAL_TARGET_INDICES=indices,BASELINE_OWNED_INVENTORIES=baseline,V12_BASELINE=v12,DOWNSTREAM_ORIGINS=origins).items())
constants+='\n'+f'BRANCHES=[Path({str(v14)!r}),Path({str(pub5)!r})]\nV14_OUT=BRANCHES[0]\nV12_OUT=Path('+repr('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12')+')\n'
constants+="TARGETS=[Path(r['path'])for r in TARGET_SELECTED_PINS];TARGET_PATHS={str(p)for p in TARGETS};BYTES=1478165640\nSOURCE_NAMES=('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py')\nSF=PKG/'COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json';FINAL=PKG/'EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json';RECEIPTS=REC/'storage_release_literal5_closed_failed_v15_private_actual_receipts_20261014'\n"
shared='\n\n'.join(functions[n]for n in ('external','inventory','receipt_pin','update_owned','budget','review_gate'))
disjoint=functions['disjoint'].replace('!=2','!=5').replace('exact2','exact5').replace('literal2','literal5')
writer=functions['writer_gate']
writer=writer.replace("BRANCHES+[V12_OUT]+[Path(s['actual_output_root'])for s in CURRENT_SELECTIONS]","BRANCHES+[V12_OUT,Path(CLOSED_V15['actual_output_root'])]+[Path(s['actual_output_root'])for s in CURRENT_SELECTIONS]")
common=header+constants+'\n'+functions['_base']+"\nb=_base();pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new\n\n"+shared+'\n\n'+custom+'\n'+disjoint+'\n\n'+writer+'\n'
_,oldprepare=pin(OLD/'prepare_literal2_manifest.py');_,oldverify=pin(OLD/'verify_or_execute_literal2.py')
prepare=oldprepare.decode().replace('literal2','literal5').replace('LITERAL2_OLD_V14_PRIVATE_BQ','LITERAL5_CLOSED_FAILED_V15_PRIVATE').replace('target_count=2','target_count=5').replace('retained_all_other_v14_files','retained_all_other_v14_and_failedpublic5_files').replace('actual_closed_failed_v14_owner','actual_closed_failed_v14_and_v15_owner').replace('all_other_v14_Q1_MAC1_PROJECT','all_other_v14_and_failedpublic5').replace('old12 v14 inventory','v14/public5 inventory')
verify=oldverify.decode().replace('literal2','literal5').replace('LITERAL2_OLD_V14_PRIVATE_BQ','LITERAL5_CLOSED_FAILED_V15_PRIVATE').replace("m['target_count']!=2","m['target_count']!=5").replace('retained_all_other_v14_files','retained_all_other_v14_and_failedpublic5_files').replace('actual_closed_failed_v14_owner','actual_closed_failed_v14_and_v15_owner').replace('deleted_files=2','deleted_files=5').replace('family2','family5').replace('unlink2','unlink5').replace('exact2','exact5').replace("before['regular_files']-after['regular_files']!=2","before['regular_files']-after['regular_files']!=5").replace('all_other_v14_Q1_MAC1_PROJECT','all_other_v14_and_failedpublic5')
# Keep the complete original v2 syscall/fsync/FirstFailure block byte-identical.
unlink_marker='                os.unlink(target.name,dir_fd=fd)';end_marker='        for r in protected+'
oldblock=oldverify.decode()[oldverify.decode().index(unlink_marker):oldverify.decode().index(end_marker)]
assert verify[verify.index(unlink_marker):verify.index(end_marker)]==oldblock
for body in (common,prepare,verify):ast.parse(body)
for n in ('_base','external','inventory','receipt_pin','update_owned','budget','review_gate'):
    newn=next(n0 for n0 in ast.parse(common).body if isinstance(n0,ast.FunctionDef)and n0.name==n)
    assert ast.get_source_segment(common,newn)==functions[n]
assert "before['regular_files']-after['regular_files']!=5"in verify and 'deleted_files=5'in verify
for p,_ in seen.values():actual7(p)
inverses=[]
for oldname,newname,oldbytes,newbody in zip(('literal2_release_common.py','prepare_literal2_manifest.py','verify_or_execute_literal2.py'),('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py'),(oldraw,oldprepare,oldverify),(common,prepare,verify)):
    ol=oldbytes.decode().splitlines(keepends=True);nl=newbody.splitlines(keepends=True);blocks=[]
    for tag,oi,oj,ni,nj in difflib.SequenceMatcher(a=ol,b=nl,autojunk=False).get_opcodes():
        if tag!='equal':blocks.append(dict(old_start_line0=oi,old_end_line0=oj,new_start_line0=ni,new_end_line0=nj,old_exact_bytes=''.join(ol[oi:oj]),new_exact_bytes=''.join(nl[ni:nj])))
    restored=list(nl)
    for x in reversed(blocks):
        assert ''.join(restored[x['new_start_line0']:x['new_end_line0']])==x['new_exact_bytes']
        restored[x['new_start_line0']:x['new_end_line0']]=x['old_exact_bytes'].splitlines(keepends=True)
    assert ''.join(restored).encode()==oldbytes
    inverses.append(dict(old_name=oldname,new_name=newname,exact_change_blocks=blocks,whole_byte_inverse_matches_old_source=True,old_sha256=hashlib.sha256(oldbytes).hexdigest(),new_sha256=hashlib.sha256(newbody.encode()).hexdigest()))
OUT.mkdir()
sourcepins=[write(n,b)for n,b in zip(('literal5_release_common.py','prepare_literal5_manifest.py','verify_or_execute_literal5.py'),(common,prepare,verify))]
proof=write('COMPLETE_LITERAL2_V2_TO_LITERAL5_SOURCE_BLOCK_BYTE_INVERSE.json',dict(schema='EXACT_LITERAL5_WHOLE_SOURCE_BYTE_INVERSE_AND_LOW_LEVEL_PROVENANCE_V1',old_common_source_pin=oldcommonpf,old_prepare_source_pin=seen[str(OLD/'prepare_literal2_manifest.py')][0],old_verify_source_pin=seen[str(OLD/'verify_or_execute_literal2.py')][0],new_source_pins=sourcepins,whole_source_inverse_records=inverses,unchanged_shared_functions=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate'],shared_function_SHA256={n:hashlib.sha256(functions[n].encode()).hexdigest()for n in ('_base','external','inventory','receipt_pin','update_owned','budget','review_gate')},literal2_v2_complete_unlink_fsync_FirstFailure_block_SHA256=hashlib.sha256(oldblock.encode()).hexdigest(),unlink_block_wholebytes_identical=True,only_scope_authority_currentDAG_and_fixed_count_names_changed=True,compiler_business_manifest_or_delete_executed=False))
role=write('EXACT_LITERAL5_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_CURRENT_PROTECTION_ROLE_SOURCE_PLAN_V1',source_only=True,target_count=5,target_bytes=1478165640,literal5_target_fullpins=targets,previous_manifest_pin=oldmfpf,previous_protected_count=7251,only_exact_migrated_indices=indices,retained_previous_protected_count=7246,eight_v14_alias_candidates_retained=vs['consumed_private_alias_candidate_pins'],SPOASM_retained=True,old_manifest_and_reports_not_rewritten=True,no_catalog_or_BIND_changes=True,no_generic_missing_pin_skip=True,closed_failed_v15_authority=closed_v15,current_actual_selections=current,downstream_current_origin_authorities=origins,current_owned_complete_inventory=baseline,remaining_owned_file_count_after_future_exact5=323,original_budget_caps=assigns['CAPS'],actual_budget_required_after_future_release=True,reference_family_bytes=81260703839,reference_next_fullfresh2_reserve_deficit=1367845995,reference_predicted_reserve_remaining=110319645,reference_budget_prediction_is_not_admission=True,future_manifest_pin=None,future_readonly_receipt_pin=None,future_actual_release_receipt_pin=None,manifest_prepared=False,deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,AAA_qualified=False,ABA_admitted=False))
sf=write('COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_FREEZE.json',dict(schema='COMPLETE_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,Source_pins=sourcepins,original_caps=assigns['CAPS'],literal5_fullpins=targets,historical_evidence_pins=hist,current_actual_selections=current,closed_failed_v15_authority=closed_v15,original_readonly_helper_pin=assigns['BASE_PIN'],original_resource_factory_pin=oldsf['original_resource_factory_pin'],strict_low_level_Source_provenance_pin=proof,exact_role_plan_pin=role,Source_preparer_pin=pin(Path(__file__).absolute())[0],target_fullEOF_in_prior_actual_survey=True,target_current7_reverified_at_Source_prep=True,target_fullEOF_not_repeated_at_Source_prep=True,all_selected_direct_current_PF_reverified_current7=True,default_readonly=True,execute_requires_one_literal_flag=True,no_retry_or_overwrite=True,future_manifest_pin=None,future_readonly_receipt_pin=None,future_actual_release_receipt_pin=None,qualification_promoted=False))
assert not (OUT/'EXACT_LITERAL5_CLOSED_FAILED_V15_PRIVATE_RELEASE_MANIFEST.json').exists()
for p,_ in seen.values():actual7(p)
print(json.dumps(dict(status='SOURCE_ONLY_EXACT_LITERAL5_PACKAGE_PREPARED_NO_IMPORT_MANIFEST_OR_DELETION',Source_freeze_pin=sf,source_pins=sourcepins,role_plan_pin=role,inverse_pin=proof,literal_target_count=5,target_bytes=1478165640,manifest_prepared=False,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False),ensure_ascii=False))

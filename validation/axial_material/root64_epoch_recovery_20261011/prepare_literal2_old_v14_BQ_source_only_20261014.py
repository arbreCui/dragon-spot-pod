"""Only prepare auditable Source/role metadata. No candidate import or cleanup."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=R/'storage_release_literal2_old_v14_BQ_source_v1_20261014'
OLD=R/'storage_release_curated66_old_private_copies_source_v3_20261013'
seen={}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path);i=ids(p.lstat());assert stat.S_ISREG(i[2]);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==i;raw=f.read();assert ids(os.fstat(f.fileno()))==i
 assert ids(p.lstat())==i;x=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i);seen[str(p)]=(x,raw);return x,raw
def read(path):p,raw=pin(path);return json.loads(raw),p
def write(name,data):
 raw=data.encode()if isinstance(data,str)else(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();p=OUT/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)[0]

assert not OUT.exists()
oldmf,oldmfpf=read(OLD/'EXACT_CURATED66_OLD_PRIVATE_RELEASE_MANIFEST.json');oldsf,oldsfpf=read(OLD/'COMPLETE_CURATED66_OLD_PRIVATE_RELEASE_SOURCE_FREEZE.json')
target=[oldmf['current_protected_full_EOF_pins'][i]for i in (4166,4167)]
assert [Path(x['path']).name for x in target]==['BQ64-MAC-ST','BQ64-SRC-ST']and sum(x['size_bytes']for x in target)==528482632
for x in target:
 s=Path(x['path']).lstat();assert ids(s)==x['identity']and s.st_uid==os.getuid()and s.st_nlink==1
evidence=[]
for name in ['storage_release_curated66_old_private_copies_actual_receipts_20261013/ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT.json','independent_curated66_actual_postrelease_review_20261013/REVIEW.json','independent_curated66_actual_postrelease_review_20261013/TRUE_TOOL_RETURNS.json','independent_literal2_failed_v14_BQ_storage_role_survey_20261013/REVIEW.json','independent_literal2_failed_v14_BQ_storage_role_survey_20261013/TRUE_TOOL_RETURNS.json']:
 x,p=read(R/name);evidence.append(p)
historical_pin_map=dict(previous_curated66_Source_freeze=oldsfpf,previous7030_manifest=oldmfpf,completed_actual_curated66_release=evidence[0],completed_independent_curated66_postreview=evidence[1],completed_independent_curated66_post_tools=evidence[2],literal2_source_survey=evidence[3],literal2_source_survey_tools=evidence[4])
current=[]
for role,dirname,summary in [('build4','bq64_compact_expected_build_host_source_v4_20261013','/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4/Root_actual_build_only_summary.json'),('fresh17','bq64_compact_expected_connected17_host_source_v2_20261013','/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v2/Root_actual_connected17_summary.json'),('model5','bq64_private_GANLIB_model_control_host_source_v5_20261013','/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5/Root_actual_control_summary.json'),('public5_failed','public_read_compact_bq_admission_control_host_source_v5_20261013','/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5/Root_actual_control_summary.json')]:
 hf_name={'build4':'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json','fresh17':'COMPLETE_FRESH17_NEW_BOOTQ_HOST_SOURCE_FREEZE.json'}.get(role,'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')
 hf,hpf=read(R/dirname/hf_name);a,ap=read(summary)
 rows=hf['dependencies']+[hf['host_source']]+a['fixed_current_pins']+a['output_pins']+[ap,hpf]
 assert all(x['path']not in{t['path']for t in target}for x in rows)
 for x in rows:assert ids(Path(x['path']).lstat())==x['identity']
 cli_name='ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json'if role=='build4'else'ROOT_REVIEWABLE_EXACT_FRESH17_ARGV.json'if role=='fresh17'else'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json'
 _,cli=read(R/dirname/cli_name)
 current.append(dict(role=role,Host_freeze_pin=hpf,actual_report_pin=ap,exact_cli_pin=cli,actual_output_root=str(Path(summary).parent),actual_status=a['status'],actual_failure=a['failure'],expected_dependency_count=len(hf['dependencies']),actual_fixed_count=len(a['fixed_current_pins']),actual_output_count=len(a['output_pins'])))
public=json.loads(seen[current[-1]['actual_report_pin']['path']][1]);bundles=[p for p in public['output_pins']if Path(p['path']).name=='coherent_complete_context.xsm'];assert len(bundles)==2 and all(p['size_bytes']==100163528 for p in bundles)
v14=Path(target[0]['path']).parents[1];s,sp=read(v14/'Root_actual_three_plane_engineering_summary.json');raw,rp=read(v14/'Root_actual_complete_execution_record_before_final_publication.json');stage,stp=read(v14/'AAA3-streaming/stages.json');watch,wp=read(v14/(s['records'][-1]['label']+'.watchdog.json'))
assert s['failure']=='RuntimeError: remaining runtime/context/log/meta storage planning bound128MiB'and s['engineering_three_plane_closed0']is False and s['actual_terminal']is None and s['AAA_qualified']is False and watch['own_child_only']is True and watch['liveness_group_cleanup']is True
compact=lambda rows:[{k:v for k,v in x.items()if k not in('resource_before','resource_after')}for x in rows]
assert compact(s['records'])==compact(raw['records'])and stage=={'stages':raw['records']}
owner=dict(root=str(v14),summary_pin=sp,complete_raw_pin=rp,stages_pin=stp,last_watchdog_pin=wp,actual_failure=s['failure'],actual_record_count=len(s['records']),actual_last_child_integer_returncode=watch['returncode'],engineering_closed0=False,AAA_qualified=False)
original_common,origraw=pin(OLD/'curated66_release_common.py');tree=ast.parse(origraw);methods={n.name:ast.get_source_segment(origraw.decode(),n)for n in tree.body if isinstance(n,ast.FunctionDef)}
base=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='BASE_PIN'))
shared='\n\n'.join(methods[name]for name in ('_base','external','inventory','receipt_pin','update_owned','budget'))
header='''"""Literal2 old failedv14 private BQ files only; default readonly, no retry."""
import ast,hashlib,importlib.util,json,os,stat,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';PKG=Path(__file__).absolute().parent
'''
caps=oldsf['original_caps']
constants='\n'.join([f'BASE_PIN={base!r}',f'CAPS={caps!r}',f'HISTORICAL_PINS={historical_pin_map!r}',f'CURRENT_SELECTIONS={current!r}',f'OWNER={owner!r}',f'TARGET_SELECTED_PINS={target!r}',f'PUBLIC5_FAILED_BUNDLES={bundles!r}',f'BRANCHES=[Path({str(v14)!r})]',"V14_OUT=BRANCHES[0]",f"V12_OUT=Path({str(R.parent.parent/'artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12')!r})",'TARGETS=[Path(r[\'path\'])for r in TARGET_SELECTED_PINS];TARGET_PATHS={str(p)for p in TARGETS};BYTES=528482632',"SOURCE_NAMES=('literal2_release_common.py','prepare_literal2_manifest.py','verify_or_execute_literal2.py')","SF=PKG/'COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json';FINAL=PKG/'EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json';RECEIPTS=REC/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014'"])
base_method=methods['_base'];rest_shared='\n\n'.join(methods[name]for name in ('external','inventory','receipt_pin','update_owned','budget'))
custom='''
def source_gate(sfpin):
    if sfpin['path']!=str(SF):raise RuntimeError('exact literal2 Source namespace')
    f=read(sfpin)
    if f['schema']!='COMPLETE_LITERAL2_OLD_FAILED_V14_PRIVATE_BQ_RELEASE_SOURCE_ONLY_FREEZE_V1'or f['source_only']is not True or f['manifest_prepared']is not False or f['deletion_executed']is not False or f['compiler_or_business_executed']is not False or f['original_caps']!=CAPS or f['literal2_fullpins']!=TARGET_SELECTED_PINS or f['historical_evidence_pins']!=HISTORICAL_PINS or f['current_actual_selections']!=CURRENT_SELECTIONS or f['literal_failed_owner_proof']!=OWNER:raise RuntimeError('exact immutable2 Source scope/caps/roles')
    if [p['path']for p in f['Source_pins']]!=[str(PKG/n)for n in SOURCE_NAMES]:raise RuntimeError('three exact Source files')
    for p in f['Source_pins']+list(HISTORICAL_PINS.values()):same(p)
    same(f['original_resource_factory_pin'])
    if f['original_resource_factory_pin']['path']!=str(b.FACTORY):raise RuntimeError('original exact resource factory')
    survey=read(HISTORICAL_PINS['literal2_source_survey']);tool=read(HISTORICAL_PINS['literal2_source_survey_tools']);closed=tool['actual_review_return']
    if type(closed['exit_code'])is not int or closed['exit_code']!=0 or closed.get('session_id')is not None or b.norm(json.loads(closed['output'].strip().splitlines()[-1])['review_pin'])!=HISTORICAL_PINS['literal2_source_survey']or survey['failure']is not None or survey['exact_literal_target_count']!=2 or survey['total_logical_bytes']!=BYTES:raise RuntimeError('real literal2 source survey0')
    return f

def review_gate(sfpin,reviewpin,toolpin):
    d=read(reviewpin);t=read(toolpin);a=t.get('actual_review_return')
    if d.get('Source_freeze_pin')!=sfpin or d.get('failure')is not None or d.get('business_executed')is not False or t.get('observed_closed')is not True or type(t.get('original_integer_exit_code'))is not int or t['original_integer_exit_code']!=0 or not isinstance(a,dict)or type(a.get('exit_code'))is not int or a['exit_code']!=0 or a.get('session_id')is not None or b.norm(json.loads(a['output'].strip().splitlines()[-1])['review_pin'])!=reviewpin:raise RuntimeError('genuine exact owning Source review0')

def closed_proofs():
    s=read(OWNER['summary_pin']);raw=read(OWNER['complete_raw_pin']);stages=read(OWNER['stages_pin']);w=read(OWNER['last_watchdog_pin'])
    compact=lambda rs:[{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in rs]
    if s['failure']!=OWNER['actual_failure']or s['engineering_three_plane_closed0']is not False or s['actual_terminal']is not None or s['AAA_qualified']is not False or compact(s['records'])!=compact(raw['records'])or stages!={'stages':raw['records']}or len(s['records'])!=OWNER['actual_record_count']or type(w['returncode'])is not int or w['returncode']!=OWNER['actual_last_child_integer_returncode']or w['own_child_only']is not True or w['liveness_group_cleanup']is not True:raise RuntimeError('exact actual failed-unqualified v14 owner closed proof')
    return [OWNER]

def disjoint(protected):
    if len(TARGETS)!=2 or len(TARGET_PATHS)!=2 or sum(p['size_bytes']for p in TARGET_SELECTED_PINS)!=BYTES or len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=2:raise RuntimeError('exact2 paths/physicalnodes/bytes')
    paths={p['path']for p in protected};nodes={tuple(p['identity'][:2])for p in protected}
    for path,p in zip(TARGETS,TARGET_SELECTED_PINS):
        b.ancestors(path);s=path.lstat()
        if str(path)!=p['path']or identity(s)!=p['identity']or s.st_uid!=os.getuid()or s.st_nlink!=1 or not stat.S_ISREG(s.st_mode)or str(path)in paths or tuple(p['identity'][:2])in nodes:raise RuntimeError('owned literal2 UID/all7/nlink1/nonsymlink/disjoint')
        same(p)

def current_protection(sfpin,reviews):
    f=source_gate(sfpin);old=read(HISTORICAL_PINS['previous7030_manifest']);done=read(HISTORICAL_PINS['completed_actual_curated66_release']);post=read(HISTORICAL_PINS['completed_independent_curated66_postreview']);table={};roles={};cache={}
    if done['status']!='EXACT_CURATED66_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'or done['deleted_files']!=66 or done['logical_bytes_released']!=1751559764 or done['manifest_pin']!=HISTORICAL_PINS['previous7030_manifest']or post['failure']is not None or post['actual_release_receipt_pin']!=HISTORICAL_PINS['completed_actual_curated66_release']:raise RuntimeError('immutable completed curated66 historical facts')
    oldrows=old['current_protected_full_EOF_pins']
    if len(oldrows)!=7030 or [oldrows[i]for i in (4166,4167)]!=TARGET_SELECTED_PINS or {p['path']for p in oldrows}&TARGET_PATHS!=TARGET_PATHS:raise RuntimeError('only exact2 prior7030 historical protected declarations')
    def add(p,role):
        p=b.norm(p);path=p['path'];actual=cache.get(path)
        if actual is None:actual=pin(path);cache[path]=actual
        elif identity(Path(path).lstat())!=actual['identity']:raise RuntimeError('protected current7 changed')
        if actual!=p or path in TARGET_PATHS or tuple(p['identity'][:2])in{tuple(x['identity'][:2])for x in TARGET_SELECTED_PINS}:raise RuntimeError('protected exactPF changed or aliases target')
        if path in table and table[path]!=p:raise RuntimeError('inconsistent protected PF')
        table[path]=p;roles.setdefault(role,set()).add(path)
    for i,p in enumerate(oldrows):
        if i not in(4166,4167):add(p,'original7028_protected_every_other_row_retained')
    before=inventory();oldinv=old['Source_DAG_provenance']['current_v14_complete_inventory']
    if before!=oldinv or len(before['ordinary_file_identities'])!=299 or before['symlinks']:raise RuntimeError('whole latestfailedv14 original299/36 inventory changed')
    retained=[]
    for path in sorted(before['ordinary_file_identities']):
        if path not in TARGET_PATHS:
            actual=pin(path);add(actual,'all_other297_v14_Q1_MAC1_PROJECT_science_results_logs_summary_sources_retained');retained.append(actual)
    current12=inventory([V12_OUT])
    if current12!=old['Source_DAG_provenance']['current_v12_complete_inventory']:raise RuntimeError('entire v12 namespace changed')
    for selected in CURRENT_SELECTIONS:
        hf=read(selected['Host_freeze_pin']);a=read(selected['actual_report_pin']);cli=read(selected['exact_cli_pin'])
        if len(hf['dependencies'])!=selected['expected_dependency_count']or len(a['fixed_current_pins'])!=selected['actual_fixed_count']or len(a['output_pins'])!=selected['actual_output_count']or a['status']!=selected['actual_status']or a['failure']!=selected['actual_failure']or a['actual_host_Source_freeze_pin']!=selected['Host_freeze_pin']:raise RuntimeError('exact current selected Host/actual report pins and role counts/status')
        if selected['role']=='public5_failed'and(a['status']!='ACTUAL_CONTROL_FAILED_UNQUALIFIED'or a['actual_seven_genuine_public_READ_controls_passed']is not False):raise RuntimeError('failed public5 scene is retained unqualified evidence')
        rows=[selected['Host_freeze_pin'],selected['actual_report_pin'],selected['exact_cli_pin'],hf['host_source']]+hf['dependencies']+a['fixed_current_pins']+a['output_pins']
        # Only direct current PF lists are live. Nested historical JSON is never promoted.
        for p in rows:add(p,'current_'+selected['role']+'_entire_HF_ownHost_actual_fixed_output_summary_retained')
        actual_inventory=inventory([Path(selected['actual_output_root'])])
        if set(actual_inventory['ordinary_file_identities'])!={p['path']for p in a['output_pins']}|{selected['actual_report_pin']['path']}or actual_inventory['symlinks']:raise RuntimeError('full selected actual output scene contains unregistered/aliased file')
        for p in PUBLIC5_FAILED_BUNDLES:
            if selected['role']=='public5_failed':same(p)
    for p in f['Source_pins']+list(HISTORICAL_PINS.values())+[sfpin]:add(p,'own_Source_and_completed_historical_metadata_retained_as_files')
    for who,r,t in reviews:review_gate(sfpin,r,t);add(r,who+'_actual_source0');add(t,who+'_actual_source0_tools')
    return sorted(table.values(),key=lambda p:p['path']),dict(roles={k:sorted(v)for k,v in roles.items()},previous_protected_count=7030,only_two_original_indices_migrated_to_historical=[4166,4167],all_original_other7028_PF_rows_data_retained=True,historical_original7030_and_v14_299_attestation_not_rewritten=True,current_v14_complete_inventory=before,current_v12_complete_inventory=current12,protected_all_current_success_and_failed_public5_actual_outputs=True,old_nested_JSON_historical_PF_not_live_dependencies=True),retained,before

def writer_gate(protected):
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],capture_output=True,text=True,timeout=20)
    if proc.returncode!=0 or proc.stderr.strip():raise RuntimeError('real process metadata unavailable')
    owners=[str(REC/('aaa_three_plane_streaming_pipeline_source_v'+str(v))/'run_actual_three_plane_pipeline.py')for v in range(1,16)]+[p['path']for p in protected if Path(p['path']).suffix=='.py'and any(w in Path(p['path']).name for w in('run_','prepare_','finalize_','freeze_','write_'))]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)!=2 or int(fields[0])==os.getpid():continue
        command=fields[1]
        if int(fields[0])==os.getppid()and Path(command.split(None,1)[0]).name in('zsh','bash','sh')and str(Path(sys.argv[0]).absolute())in command:continue
        if any(p in command for p in owners+[str(PKG)])or(str(ART)in command and('/runtime/Dragon'in command or'run_bounded_dragon.py'in command)):raise RuntimeError('active protected writer or owned business')
    for branch in BRANCHES+[V12_OUT]+[Path(s['actual_output_root'])for s in CURRENT_SELECTIONS]:
        opened=subprocess.run(['/usr/sbin/lsof','-nP','+D',str(branch)],capture_output=True,text=True,timeout=30)
        if opened.returncode not in(0,1)or opened.stdout.strip()or opened.stderr.strip():raise RuntimeError('protected/target namespace open handle or real lsof unavailable')
    guard()
'''
common=header+constants+'\n\n'+base_method+"\nb=_base();pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new\n\n"+rest_shared+'\n\n'+custom
prepare=(OLD/'prepare_curated66_manifest.py').read_text().replace('curated66_release_common','literal2_release_common').replace('CURATED66','LITERAL2_OLD_V14_PRIVATE_BQ').replace('curated_Source','literal2_Source').replace('target_count=66','target_count=2').replace('failed12_owner','failed_v14_owner').replace('all_other12_old','all_other_v14').replace('inventory changed before MF','v14 inventory changed before MF').replace('LITERAL66','LITERAL2').replace('all_latest_v14_v12_v3PACK_old_ax_current_retained=True','all_other_v14_Q1_MAC1_PROJECT_science_and_current_success_failed_outputs_retained=True')
verify=(OLD/'verify_or_execute_curated66.py').read_text().replace('curated66_release_common','literal2_release_common').replace('CURATED66','LITERAL2_OLD_V14_PRIVATE_BQ').replace('curated_Source','literal2_Source').replace("m['target_count']!=66","m['target_count']!=2").replace('failed12_owner','failed_v14_owner').replace('all_other12_old','all_other_v14').replace('literal66','literal2').replace('LITERAL66','LITERAL2').replace('unlink66','unlink2').replace('exact66','exact2').replace("!=66 or after","!=2 or after").replace('deleted_files=66','deleted_files=2').replace('family66','family2').replace('old12','v14')
verify=verify.replace("if s.inventory([s.V14_OUT])!=dag['current_v14_complete_inventory']or s.inventory([s.V12_OUT])!=dag['current_v12_complete_inventory']:raise RuntimeError('latestv14/allv12 inventory changed')","if s.inventory([s.V12_OUT])!=dag['current_v12_complete_inventory']:raise RuntimeError('allv12 inventory changed')")
verify=verify.replace('all_latest_v14_v12_v3PACK_old_ax_current_other_science_Source_logs_retained=True','all_other_v14_Q1_MAC1_PROJECT_science_and_current_success_failed_public_outputs_retained=True')
OUT.mkdir()
sourcepins=[]
for name,body in [('literal2_release_common.py',common),('prepare_literal2_manifest.py',prepare),('verify_or_execute_literal2.py',verify)]:ast.parse(body);sourcepins.append(write(name,body))
_,factory=read(R/'storage_release_curated66_old_private_copies_source_v3_20261013/COMPLETE_CURATED66_OLD_PRIVATE_RELEASE_SOURCE_FREEZE.json')
lowlevel=write('ORIGINAL_CURATED66_V3_LOW_LEVEL_METHOD_BYTE_PROVENANCE.json',dict(schema='LITERAL2_ORIGINAL_CURATED66_V3_LOW_LEVEL_METHOD_BYTE_PROVENANCE_V1',original_common_source_pin=original_common,mechanically_cloned_method_names=['_base','external','inventory','receipt_pin','update_owned','budget'],method_source_SHA256={n:hashlib.sha256(methods[n].encode()).hexdigest()for n in ['_base','external','inventory','receipt_pin','update_owned','budget']},syscall_and_fsync_and_parent_delta_execute_body_mechanically_retained=True,no_candidate_import_or_manifest_or_delete=True))
role=write('EXACT_LITERAL2_CURRENT_PROTECTION_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL2_OLD_V14_BQ_CURRENT_PROTECTION_ROLE_SOURCE_PLAN_V1',source_only=True,literal2_target_pins=target,target_count=2,target_bytes=528482632,previous_curated66_manifest_pin=oldmfpf,original_protected_indices=[4166,4167],new_original_protected_count=7028,old7030_and_original299_are_completed_historical_attestation_unchanged=True,new_live_v14_retained_file_count=297,all_other_v14_Q1_MAC1_PROJECT_science_results_logs_summary_Source_retained=True,current_actual_selections=current,failed_public5_both_bundles_remain_current_pins=bundles,catalog_and_BIND_changes_required=False,generic_missing_pin_skip=False,manifest_prepared=False,deletion_executed=False))
sf=write('COMPLETE_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_SOURCE_FREEZE.json',dict(schema='COMPLETE_LITERAL2_OLD_FAILED_V14_PRIVATE_BQ_RELEASE_SOURCE_ONLY_FREEZE_V1',source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False,Source_pins=sourcepins,original_caps=caps,literal2_fullpins=target,literal_failed_owner_proof=owner,historical_evidence_pins=historical_pin_map,current_actual_selections=current,original_readonly_helper_pin=base,original_resource_factory_pin=oldsf['original_resource_factory_pin'],strict_low_level_Source_provenance_pin=lowlevel,exact_role_plan_pin=role,target_last_fullEOF_observation_in_previous_manifest_and_actual_post0=True,target_current7_reverified_at_Source_prep=True,target_fullEOF_not_repeated_during_Source_prep=True,all_current_HF_direct_PF_and_actual_outputs_current7_reverified_at_Source_prep=True,default_readonly=True,execute_requires_one_literal_flag=True,no_retry_or_overwrite=True,future_manifest_pin=None,future_readonly_receipt_pin=None,future_actual_release_receipt_pin=None,qualification_promoted=False))
for p,raw in seen.values():assert ids(Path(p['path']).lstat())==p['identity']
print(json.dumps(dict(status='SOURCE_ONLY_EXACT_LITERAL2_OLD_V14_BQ_RELEASE_PACKAGE_PREPARED_NO_IMPORT_OR_MANIFEST_OR_DELETION',Source_freeze_pin=sf,source_pins=sourcepins,exact_role_plan_pin=role,literal_target_count=2,target_bytes=528482632,manifest_prepared=False,business_executed=False,deletion_executed=False),ensure_ascii=False))

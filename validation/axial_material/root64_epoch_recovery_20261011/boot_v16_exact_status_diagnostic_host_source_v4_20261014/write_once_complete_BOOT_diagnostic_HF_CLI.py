"""One owning HF/CLI publication after genuine same-round Source0; no business execution."""
import argparse,ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=Path(__file__).absolute().parent
HF=HERE/'COMPLETE_GUARDED_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_FREEZE.json'
CLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def seven(p):
    p=norm(p);s=Path(p['path']).lstat()
    # Original compiler legitimately has nlink2; keep all original all7.
    if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']or s.st_size!=p['size_bytes']:raise RuntimeError('inherited original current7 changed '+p['path'])
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata only')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('metadata opened7 changed')
        b=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('metadata FD changed')
    if identity(p.lstat())!=identity(s)or len(b)!=s.st_size:raise RuntimeError('metadata after7 changed')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def unique(rows):
    t={}
    for row in rows:
        p=norm(row)
        if p['path']in t and t[p['path']]!=p:raise RuntimeError('inconsistent selected PF')
        t[p['path']]=p
    return sorted(t.values(),key=lambda p:p['path'])
def contains(v,p):
    if isinstance(v,dict):
        if all(k in v for k in p)and all(v[k]==p[k]for k in p):return True
        return any(contains(x,p)for x in v.values())
    if isinstance(v,list):return any(contains(x,p)for x in v)
    return False
def explicit_false(d,names):
    present=[d[k]for k in names if k in d]
    if not present or any(v is not False for v in present):raise RuntimeError('explicit Source-only false field '+str(names))
def write_new(p,d):
    b=(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    if len(b)>64*2**20:raise RuntimeError('Source metadata64MiB cap')
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for role in('peer-review','peer-tools'):
        for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
    a=ap.parse_args()
    if HF.exists()or HF.is_symlink()or CLI.exists()or CLI.is_symlink():raise RuntimeError('own HF/CLI once, no overwrite/retry')
    def external(role):
        name=role.replace('-','_');p=pin(getattr(a,name+'_summary'))
        if p['sha256']!=getattr(a,name+'_sha256')or p['identity']!=json.loads(getattr(a,name+'_seven_id')):raise RuntimeError('exact owning peer external PF')
        return p
    rp=external('peer-review');tp=external('peer-tools');review=read(rp['path']);tools=read(tp['path']);ret=tools['actual_review_return']
    if review['failure']is not None or not review['status'].startswith('PASS')or tools['observed_closed']is not True or type(ret['exit_code'])is not int or ret['exit_code']!=0 or ret.get('session_id')is not None or norm(json.loads(ret['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('genuine closed same-round independent Source0')
    for names in [('business_executed','independent_business_executed'),('compiler_executed','independent_compiler_executed'),('numerical_executed','numeric','independent_numerical_executed'),('files_deleted','deletion_executed','independent_deletion_executed')]:explicit_false(review,names)
    hp=pin(HERE/'run_guarded_one_BOOT_status_diagnostic.py');pp=pin(HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json');ready=pin(HERE/'SOURCE_ONLY_READY.json');inverse=pin(HERE/'COMPLETE_DIAGNOSTIC_HOST_V3_TO_V4_TRUTHFUL_PRESERVATION_BYTE_INVERSE.json');writer=pin(Path(__file__).absolute());plan=read(pp['path']);sf=pin(plan['selected_diag_Fortran_Source_freeze_path']);sfd=read(sf['path'])
    for p in(hp,pp,ready,inverse,sf,writer):
        if not contains(review,p):raise RuntimeError('peer Source review lacks one of exact Host/PLAN/READY/inverse/FortranSF/writer six PFs')
    d2p=plan['selected_Driver2_Host_freeze_pin'];v16p=plan['selected_closed_v16_Host_freeze_pin'];d2=read(d2p['path']);v16=read(v16p['path'])
    if pin(d2p['path'])!=d2p or pin(v16p['path'])!=v16p or len(d2['dependencies'])!=2627 or len(v16['dependencies'])!=2920:raise RuntimeError('entire original Driver2HF2627/v16HF2920 inheritance')
    releasepath=R/'storage_release_literal3_closed_failed_v15_private_actual_receipts_20261014/ACTUAL_EXACT_LITERAL3_CLOSED_FAILED_V15_PRIVATE_OLD_PRIVATE_RELEASE_RECEIPT.json';releasepin=pin(releasepath);release=read(releasepath)
    rootpin=pin(R/'ROOT_LITERAL3_ACTUAL_EXECUTE_TRUE_TOOL_RETURNS_20261014.json');root=read(rootpin['path']);terminal=root['actual_execute_return']
    postpin=pin(R/'independent_literal3_actual_exact_release_postverify_20261014/REVIEW.json');post=read(postpin['path']);posttoolpin=pin(Path(postpin['path']).parent/'TRUE_TOOL_RETURNS.json');posttools=read(posttoolpin['path']);postret=posttools['actual_review_return']
    if type(terminal['exit_code'])is not int or terminal['exit_code']!=0 or terminal.get('session_id')is not None or root['observed_closed']is not True or type(postret['exit_code'])is not int or postret['exit_code']!=0 or postret.get('session_id')is not None or posttools['observed_closed']is not True or norm(json.loads(postret['output'].strip().splitlines()[-1])['review_pin'])!=postpin:raise RuntimeError('actual literal3 Root0 and genuine independent post0 required')
    if release['deleted_files']!=3 or release['logical_bytes_released']!=1504027360 or release['original_budget_after']['original_initial_reserve_admitted']is not True or post['failure']is not None or post['actual_release_receipt_pin']!=releasepin or post['all_three_targets_absent']is not True or post['actual_original_initial_reserve_admitted']is not True:raise RuntimeError('exact actual release and original fullfresh2 reserve, no prediction')
    selected=dict(selected_Driver2_Host_freeze_pin=d2p,selected_diag_Fortran_Source_freeze_pin=sf,selected_closed_v16_Host_freeze_pin=v16p,selected_closed_v16_Root_tool_pin=plan['selected_closed_v16_Root_tool_pin'],selected_closed_v16_actual_post_review_pin=plan['selected_closed_v16_actual_post_review_pin'],selected_closed_v16_actual_post_tools_pin=plan['selected_closed_v16_actual_post_tools_pin'],selected_literal3_actual_release_pin=releasepin,selected_literal3_actual_Root_tool_pin=rootpin,selected_literal3_actual_post_review_pin=postpin,selected_literal3_actual_post_tools_pin=posttoolpin)
    base=read(plan['actual_Driver2_report_pin']['path']);failure=read(plan['actual_closed_v16_report_pin']['path'])
    # Explicit data rows only. Nested historical PF facts in sealed reports are
    # preserved as metadata; no recursive reinterpretation as live body PFs.
    own=[pin(p)for p in sorted(HERE.iterdir())if p.is_file()]
    metadata=[d2p,v16p,plan['actual_Driver2_report_pin'],plan['actual_closed_v16_report_pin'],sf,plan['selected_diag_Fortran_Source_creation_tool_pin'],rp,tp]+list(selected.values())+own
    metadata+=sfd['files']+sfd['original_source_pins']+[sfd['diagnostic_source_pin'],sfd['complete_byte_inverse_pin'],sfd['diagnostic_plan_pin']]
    for p in(v16p,d2p):
        folder=Path(p['path']).parent
        name='DECLARED_EXECUTION_INTERFACE.json'if p==v16p else'ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json'
        metadata.append(pin(folder/name))
    rows=unique(v16['dependencies']+d2['dependencies']+metadata+base['fixed_current_pins']+base['output_pins']+base['owned_runtime_pins']+failure['fixed_current_pins']+failure['output_pins']+failure['owned_runtime_pins']+plan['current_ordered70_input_pins']+plan['current_nine_core_object_pins']+[r['target_pin']for r in plan['owned_readonly_input_rows']]+[plan['original_BOOT_deck_pin'],plan['readonly_pair_helper_pin']])
    for p in rows:seven(p)
    for p in unique(metadata):
        if pin(p['path'])!=norm(p):raise RuntimeError('own Source/metadata complete EOF exactPF')
    for p in rows:seven(p)
    h=dict(schema='COMPLETE_GUARDED_ONE_BOOT_EXACT_STATUS_DIAGNOSTIC_HOST_SOURCE_ONLY_FREEZE_V1',host_source=hp,dependencies=rows,diagnostic_host_plan_pin=pp,**selected,selected_diag_Fortran_Source_creation_tool_pin=plan['selected_diag_Fortran_Source_creation_tool_pin'],peer_Source_review_pin=rp,peer_Source_true_tools_pin=tp,once_HF_CLI_writer_Source_pin=writer,complete_original_v16_HF2920_dependencies_retained=True,complete_original_Driver2_HF2627_dependencies_retained=True,original_dependencies_current7_only_scientific_EOF_not_repeated=True,metadata_and_Source_full_EOF_exact=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_diagnostic_object_pin=None,future_actual_Dragon_pin=None,future_actual_owned9_input_copy_pins=None,future_actual_BOOT_report_pin=None,full50_executed=False,engineering_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False)
    write_new(HF,h);hfp=pin(HF)
    bindings={'driver-build':plan['actual_Driver2_report_pin'],'v16-failure':plan['actual_closed_v16_report_pin'],'diag-source-freeze':sf,'host-freeze':hfp,'literal3-release':releasepin,'literal3-Root-tools':rootpin}
    argv=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hp['path']]
    for k,p in bindings.items():argv+=['--'+k+'-summary',p['path'],'--'+k+'-sha256',p['sha256'],'--'+k+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
    if len(argv)!=48:raise RuntimeError('exact12env plus six fullpin triplets =48argv')
    interface=dict(schema='DECLARED_GUARDED_ONE_BOOT_DIAGNOSTIC_EXECUTION_INTERFACE_V1',selected_own_Host_freeze_pin=hfp,output_root=plan['planned_output_root'],mandatory_external_prefixes=list(bindings),mandatory_external_fullpin_bindings=bindings,exact_reviewable_argv=argv,planned_stage_count=3,one_object_only_zero_based68=True,other69_Driver37_BOOTQ40_math57_current9_archives_unchanged=True,exact9_ordinary_owned_input_copies=True,original_BOOT_deck_whole_bytes_unchanged=True,original_caps=plan['original_caps'],compiler_executed=False,numerical_executed=False,business_executed=False,future_actual_object_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,physics_qualified=False,engineering_qualified=False)
    write_new(CLI,interface)
    fd=os.open(HERE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    for p in rows:seven(p)
    print(json.dumps(dict(status='ACTUAL_ONCE_DIAGNOSTIC_HOST_HF_CLI_SOURCE_PUBLICATION_NO_EXECUTION',Host_freeze_pin=hfp,CLI_pin=pin(CLI),dependency_count=len(rows),exact_argv_count=48,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()

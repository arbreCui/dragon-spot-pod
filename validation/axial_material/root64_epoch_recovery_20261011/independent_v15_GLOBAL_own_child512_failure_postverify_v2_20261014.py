import os, stat, pathlib, json, hashlib, shlex, collections

R = pathlib.Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART = pathlib.Path('/Users/wen/spot/validation/artifacts')
OUT = ART / 'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261014-v15'
HERE = R / 'independent_v15_GLOBAL_own_child512_failure_postverify_20261014'

def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def norm(p):
    return {k:p[k] for k in ('path','sha256','size_bytes','identity')}

def current(p):
    s=os.lstat(p['path'])
    assert seven(s)==p['identity'] and stat.S_ISREG(s.st_mode) and s.st_size==p['size_bytes'],p['path']

def eof(path, expected=None, retain=False):
    path=pathlib.Path(path); before=seven(path.lstat())
    assert stat.S_ISREG(before[2])
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW); h=hashlib.sha256(); n=0; pieces=[]
    try:
        assert seven(os.fstat(fd))==before
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            h.update(b); n+=len(b)
            if retain:pieces.append(b)
        assert seven(os.fstat(fd))==before
    finally:os.close(fd)
    assert seven(path.lstat())==before and n==before[4]
    p={'path':str(path),'sha256':h.hexdigest(),'size_bytes':n,'identity':before}
    if expected is not None:assert p==norm(expected),(str(path),'full EOF mismatch')
    return p,b''.join(pieces) if retain else None

def load(path, expected=None):
    p,b=eof(path,expected,True);return p,json.loads(b)

def inventory(root):
    files={};dirs={};symlinks=[]
    for parent,children,names in os.walk(root,followlinks=False):
        dirs[str(pathlib.Path(parent))]=seven(os.lstat(parent))
        for name in children+names:
            p=pathlib.Path(parent)/name;s=p.lstat()
            if stat.S_ISLNK(s.st_mode):symlinks.append(str(p))
            elif stat.S_ISREG(s.st_mode):files[str(p)]=seven(s)
    return files,dirs,symlinks

sp,summary=load(OUT/'Root_actual_three_plane_engineering_summary.json')
assert sp['sha256']=='01967b1964d527c60ba70ba0fdf2677b3de182938bcca41142440aad38e64c81' and sp['size_bytes']==2083098
tp,tool=load(R/'ROOT_ACTUAL_V15_GLOBAL_OWN_CHILD_RSS512_FAILURE_TRUE_TOOL_RETURNS_20261014.json')
terminal=tool['actual_terminal_return'];initial=tool['actual_initial_return']
assert tool['observed_closed'] is True and type(terminal['exit_code']) is int and terminal['exit_code']==1 and terminal.get('session_id') is None
assert tool['original_integer_exit_code']==1 and initial['session_id']==77078 and initial.get('exit_code') is None
hp,hf=load(R/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
cp,cli=load(pathlib.Path(hp['path']).parent/'DECLARED_EXECUTION_INTERFACE.json')
ap,argv=load(R/'ROOT_EXACT_V15_FULL50_ACTUAL_COMPACT_PREREQUISITES_ARGV_20261014.json')
assert hp['sha256']=='30ddc6c4fd2c029b52a15cd966d755804255be05ca5468923486983d75a77da7'
assert cp['sha256']=='e6d6ef18091a3f55b57f245d1d5817e3ef28b3a80c42f15f21642fe3baa0111e'
assert ap['sha256']=='97eed3147a4463e45186ea58f176fc6410340a1a127b1042b8e0e04513649746'
assert shlex.split(tool['exact_executed_command'])==argv['argv']==cli['exact_reviewable_argv'] and len(argv['argv'])==78
hostpin,_=eof(hf['host_source']['path'],hf['host_source']);assert hostpin['sha256']=='b104643ec979c438ccc638e4e5278bc7e0a7279540dd567e9411090d8496f365'
rp,raw=load(summary['complete_unmodified_execution_records_pin']['path'],summary['complete_unmodified_execution_records_pin'])
stp,stages=load(OUT/'AAA3-streaming/stages.json')
records=raw['records'];assert len(records)==33 and records==stages['stages']
compact=[{k:v for k,v in x.items() if k not in ('resource_before','resource_after')} for x in records]
assert summary['records']==compact
assert collections.Counter(x['status'] for x in records)=={'PASS':13,'FAILED':20}
assert records[-1]['label']=='AAA/global_positive' and records[-1]['status']=='FAILED'
assert records[-1]['error']=='own-child 512 MiB RSS cap reached'
assert summary['failure']==raw['failure']=='RuntimeError: own-child 512 MiB RSS cap reached'
assert summary['after_check_error'] is None and raw['after_check_error'] is None
assert summary['first_failure_secondary_errors']==raw['first_failure_secondary_errors']==[]
traceback=terminal['output'][terminal['output'].index('Traceback (most recent call last):'):]
assert "raise RuntimeError('own-child 512 MiB RSS cap reached')" in traceback and 'qualify_refined_AAA_layered_full.py' in traceback and 'global_positive' in traceback
assert traceback.rstrip().endswith('RuntimeError: own-child 512 MiB RSS cap reached')
late=[]
for line in terminal['output'].splitlines():
    if line.startswith('{'):
        try:obj=json.loads(line)
        except json.JSONDecodeError:continue
        if obj.get('schema')=='ACTUAL_PARENT_MEMORY_COMPACT_LATE_TAIL_V1':late.append(obj)
assert late and late[-1]['original_exception_not_replaced'] is True and late[-1]['first_observation_error'] is None
fixed=summary['fixed_current_pins'];owned=summary['owned_runtime_pins'];outputs=summary['output_pins']
assert len(fixed)==3011 and len({p['path'] for p in fixed})==3011
assert len(outputs)==191 and len({p['path'] for p in outputs})==191
assert len(owned)==119 and len({p['path'] for p in owned})==119
for p in fixed:current(p)
fixed_by={p['path']:norm(p) for p in fixed};out_by={p['path']:norm(p) for p in outputs}
for p in hf['dependencies']+[hf['host_source']]:assert fixed_by[p['path']]==norm(p)
assert len(hf['dependencies'])==2802
for p in owned:assert out_by[p['path']]==norm(p)
before_files,before_dirs,before_syms=inventory(OUT)
assert not before_syms and set(before_files)==set(out_by)|{sp['path']}
checked_outputs=[]
for p in outputs:checked_outputs.append(eof(p['path'],p)[0])
eof(sp['path'],sp)
critical_source=[]
for p in fixed:
    suffix=pathlib.Path(p['path']).suffix.lower()
    if suffix in {'.py','.f','.f90','.c','.h','.o','.a'} or p['path'] in {hp['path'],cp['path'],ap['path']}:
        critical_source.append(eof(p['path'],p)[0])
refusals=summary['actual_operator_refusals'];assert len(refusals)==19
refusal_by={x['original_execution_record_index']:x for x in refusals}
assert len(refusal_by)==19
expected_initial=[x for x in refusals if x['case'].startswith('initial_')]
expected_pack=[x for x in refusals if x['case'].startswith('pack_')]
assert len(expected_initial)==14 and len(expected_pack)==5
watch_rows=[]
for i,record in enumerate(records):
    group,label=record['label'].split('/')
    lp,lb=eof(OUT/group/(label+'.log'),out_by[str(OUT/group/(label+'.log'))],True)
    wp,watch=load(OUT/group/(label+'.watchdog.json'),out_by[str(OUT/group/(label+'.watchdog.json'))])
    assert watch['command']==record['command'] and watch['rss_cap_mib']==512
    if i==32:
        assert watch['returncode']==-15 and watch['sampled_peak_rss_mib']==512.203125
        assert watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"
        assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
        assert b'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE' in lb and b'normal end of execution' not in lb and b'FLU2DR-TERM' not in lb
    elif i in refusal_by:
        ref=refusal_by[i];assert record['status']=='FAILED' and watch['returncode']==1 and watch['limit_failure'] is None
        assert ref['original_execution_record_label']==record['label'] and ref['actual_exit_code']==1
        for k in ['actual_abort_message_exact','pre_transport_abort_at_frozen_validation_branch','no_positive_solver_or_seal_trace','all_actual_assertions_completed']:assert ref[k] is True
        assert norm(ref['actual_log_pin'])==lp and norm(ref['actual_watchdog_pin'])==wp
        assert ref['expected_abort'].encode() in lb
    else:
        assert record['status']=='PASS' and watch['returncode']==0 and watch['limit_failure'] is None
        assert record['log_sha256']==lp['sha256']
    watch_rows.append({'index':i,'label':record['label'],'record_status':record['status'],'expected_refusal':i in refusal_by,'log_pin':lp,'watch_pin':wp,'watch':watch})
assert not any('project' in x['label'].lower() or 'boot' in x['label'].lower() for x in records)
assert not any(pathlib.Path(p['path']).name in {'projected_boot.xsm','final_boot.xsm','BOOT-Q-1.xsm','BOOT-MAC-1.xsm','BQ64-SRC-ST','BQ64-MAC-ST'} for p in outputs)
assert summary['actual_terminal'] is None and raw['actual_terminal'] is None
for k in ['engineering_three_plane_closed0','independent_reference_physics_assessment_executed','all_new_storage_entry_controls_closed','three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete']:assert summary[k] is False
assert summary['SELF_peak_bytes']==306331648 and summary['SELF_peak_bytes']<536870912 and summary['wall_seconds']<1800
assert summary['original_guard_class']=='OwnRSSSerialExecutor' and summary['original_guard_MRO_unchanged'] is True
jp,journal=load(summary['parent_memory_observation']['journal_pin']['path'],summary['parent_memory_observation']['journal_pin'])
assert len(journal['records'])==1487==summary['parent_memory_observation']['records'] and journal['first_observation_error'] is None
assert summary['parent_memory_observation']['first_observation_error'] is None
assert summary['actual_fresh_peaks_by_phase']['GLOBAL']==1599904612<2147483648
assert summary['resources_after']['storage_inventory']['aux_bytes']==95877252<134217728 and summary['after_check_error'] is None
v14=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14'
v14sp,v14s=load(v14/'Root_actual_three_plane_engineering_summary.json')
comparison_mf_pin,comparison_mf=load(R/'storage_release_literal2_old_v14_BQ_source_v2_20261014/EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json')
assert comparison_mf_pin['sha256']=='2d9ea9a1c7dace6c79cbc23f360f9e020d85b488a2a0f19d4f5272fd477c435a'
v14outs={p['path']:norm(p) for p in comparison_mf['retained_all_other_v14_files_full_EOF_pins']}
v14wp,v14w=load(v14/'AAA/global_positive.watchdog.json',v14outs[str(v14/'AAA/global_positive.watchdog.json')])
v14lp,v14lb=eof(v14/'AAA/global_positive.log',v14outs[str(v14/'AAA/global_positive.log')],True)
v14r=[x for x in v14s['records'] if x['label']=='AAA/global_positive'];assert len(v14r)==1 and v14r[0]['status']=='PASS'
assert v14w['returncode']==0 and v14w['limit_failure'] is None and v14w['sampled_peak_rss_mib']==507.09375 and v14w['rss_cap_mib']==512
assert b'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE' in v14lb and b'normal end of execution' in v14lb and b'FLU2DR-TERM' in v14lb
v14fixed={p['path']:norm(p) for p in v14s['fixed_current_pins']}
global_math=[]
for p in fixed:
    if pathlib.Path(p['path']).name in {'FLUGLOBAL64.f','FLUGLOBAL64.o'}:
        assert v14fixed[p['path']]==norm(p);global_math.append(norm(p))
assert len(global_math)==2
after_files,after_dirs,after_syms=inventory(OUT)
assert after_files==before_files and after_dirs==before_dirs and not after_syms
for p in fixed:current(p)
for p in outputs+[sp,hp,cp,ap,tp,rp,jp,v14sp,v14lp,v14wp]:current(p)
roots=set(summary['resources_after']['declared_resource_roots'])
for p in ART.iterdir():
    if p.name.startswith('axial-material-') and p.is_dir() and not p.is_symlink():roots.add(str(p))
assert roots==set(summary['resources_after']['resource_roots'])
family_bytes=family_files=0
for root in sorted(roots):
    for parent,dirs,names in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if not pathlib.Path(parent,d).is_symlink()]
        for n in names:
            s=os.lstat(pathlib.Path(parent,n))
            if stat.S_ISREG(s.st_mode):family_bytes+=s.st_size;family_files+=1
out_bytes=sum(x[4] for x in after_files.values());out_files=len(after_files)
assert out_files==192 and out_bytes==1601987710
caps=cli['original_limits'];reserve=caps['history_bytes']-family_bytes-caps['cold_reserve_bytes']-caps['metadata_reserve_bytes']-caps['fresh_bytes']
assert family_bytes==summary['resources_after']['artifact_bytes']+sp['size_bytes']
assert family_files==summary['resources_after']['regular_files']+1
assert family_bytes-summary['resources_before']['artifact_bytes']==out_bytes
assert family_files-summary['resources_before']['regular_files']==out_files
assert reserve<0
free=os.statvfs(ART).f_bavail*os.statvfs(ART).f_frsize
report={'schema':'INDEPENDENT_ACTUAL_V15_GLOBAL_OWN_CHILD512_FAILURE_POSTVERIFY_V1','status':'PASS_POSTVERIFY_OF_GENUINE_FAILED_UNQUALIFIED_V15_NO_RETRY','failure':None,'business_failure':summary['failure'],'actual_pipeline_tool_exit_code':1,'genuine_closed_actual_Root_tool_pin':tp,'actual_initial_return':initial,'actual_terminal_return':terminal,'summary_pin':sp,'full_raw_records_pin':rp,'stages_pin':stp,'summary_compact_resources_removed_only_and_raw_equal_full_stages':True,'actual_record_count':33,'actual_PASS_records':13,'actual_FAILED_records':20,'exact_expected_refusal_records':19,'original_initial_expected_refusals':14,'pack_storage_expected_refusals':5,'genuine_unexpected_global_failure_records':1,'watch_and_log_rows':watch_rows,'first_error_object_and_traceback_preserved':True,'first_original_traceback':traceback,'after_check_error':None,'first_failure_secondary_errors':[],'late_exception_preserved_observation':late[-1],'fixed_current_count':3011,'all3011_fixed_seven_id_before_after_equal':True,'critical_Source_object_archive_full_EOF_count':len(critical_source),'critical_Source_object_archive_full_EOF_pins':critical_source,'all2802_HF_dependencies_and_host_exact_in_actual_fixed':True,'host_freeze_pin':hp,'CLI_pin':cp,'Root_exact_argv_pin':ap,'host_source_pin':hostpin,'owned_runtime_count':119,'all119_owned_fullpins_in_outputs':True,'physical_output_full_EOF_count_including_summary':192,'physical_output_bytes_including_summary':out_bytes,'all191_published_outputs_physical_full_EOF_SHA_seven_id':checked_outputs,'output_directory_count':len(after_dirs),'output_symlink_count':0,'complete_actual_OUT_inventory_equal_published_outputs_plus_summary':True,'parent_journal_pin':jp,'parent_journal_records':1487,'parent_observation_error':None,'SELF_peak_bytes':summary['SELF_peak_bytes'],'SELF_peak_MiB':summary['SELF_peak_bytes']/1048576,'summary_wall_seconds':summary['wall_seconds'],'GLOBAL_watch':watch_rows[-1]['watch'],'GLOBAL_own_child_failure_is_not_auxiliary128_failure':True,'GLOBAL_fresh_peak_bytes':1599904612,'GLOBAL_aux_bytes':95877252,'original_caps':caps,'v14_GLOBAL_comparison':{'retained_inventory_manifest_pin':comparison_mf_pin,'summary_pin':v14sp,'log_pin':v14lp,'watch_pin':v14wp,'record':v14r[0],'watch':v14w,'same_FLUGLOBAL_Source_and_object_fullpins':global_math,'inference_limit':'Both use the original512 MiB guard; this comparison establishes observed pass/failure and unchanged GLOBAL Source/object, not a causal attribution of RSS variation.'},'resources_before_snapshot':{k:summary['resources_before'][k] for k in ['artifact_bytes','regular_files','disk_free_bytes','min_free_bytes','artifact_budget_bytes']},'resources_after_before_summary_snapshot':{k:summary['resources_after'][k] for k in ['artifact_bytes','regular_files','disk_free_bytes','min_free_bytes','artifact_budget_bytes']},'current_actual_declared_plus_dynamic_axial_family_scope_root_count':len(roots),'current_actual_family_bytes':family_bytes,'current_actual_family_regular_files':family_files,'current_filesystem_free_bytes':free,'original_cold_metadata_fullfresh2G_next_run_reserve_bytes':reserve,'original_initial_reserve_admitted_for_next_full_fresh_run':False,'PROJECT_started':False,'online_BOOT_started':False,'actual_terminal':None,'full50_completed':False,'three_plane_qualified':False,'GLOBAL_qualified':False,'rank_qualified':False,'online_BOOT_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'physics_qualification':False,'goal_complete':False,'independent_business_executed':False,'independent_compiler_executed':False,'independent_numerical_executed':False,'independent_deletion_executed':False,'Source_modified':False,'science_large_full_EOF_repeated':False,'all_file_descriptors_closed':True,'reviewer_initial_metadata_lookup_failure_preserved':'23eff3 EXIT1 KeyError from treating v14 failed-summary empty output_pins as complete inventory; v2 uses the previously verified immutable literal2 retained297 manifest fullpins. No business or Source failure is inferred.','limitation':'Postverification passes while the actual pipeline failed. The3011 fixed rows were independently reobserved by exact seven-id twice; critical Source/object/archive bytes and all192 new physical output files were full EOF verified. No numerical rerun or qualification is claimed.'}
HERE.mkdir();path=HERE/'REVIEW.json';b=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
try:
    v=memoryview(b)
    while v:v=v[os.write(fd,v):]
    os.fsync(fd)
finally:os.close(fd)
dfd=os.open(HERE,os.O_RDONLY|os.O_DIRECTORY)
try:os.fsync(dfd)
finally:os.close(dfd)
review_pin,_=eof(path)
print(json.dumps({'status':report['status'],'review_pin':review_pin,'actual_pipeline_exit_code':1,'actual_counts':{'records':33,'PASS':13,'expected_refusal':19,'unexpected_GLOBAL_failure':1},'outputs_full_EOF_count':192,'fixed_current_count':3011,'next_full_run_reserve_bytes':reserve,'failure':None,'business_failure':summary['failure']},ensure_ascii=False))

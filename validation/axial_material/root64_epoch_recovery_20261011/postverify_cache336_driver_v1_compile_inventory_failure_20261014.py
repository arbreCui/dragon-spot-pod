"""Independent read-only postverify of one successful compile and failed Host admission."""
import hashlib,json,os,resource,shlex,stat,time
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=R/'independent_cache336_driver_v1_compile_inventory_failure_postverify_20261014'
ROOT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1')
seen={};start=time.monotonic()
def guard():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-start>=1800:raise RuntimeError('original independent512/1800 guard')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in ('path','sha256','size_bytes','identity')}
def pin(path):
    p=Path(path);a=p.lstat();i=ids(a);assert stat.S_ISREG(a.st_mode);h=hashlib.sha256();n=0;fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert ids(os.fstat(fd))==i
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            h.update(b);n+=len(b);guard()
        assert ids(os.fstat(fd))==i
    finally:os.close(fd)
    assert ids(p.lstat())==i and n==i[4];v=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);seen[str(p)]=v;return v
def read(path):
    p=pin(path);d=json.loads(Path(path).read_text());assert ids(Path(path).lstat())==p['identity'];return d,p
def seven(p):assert stat.S_ISREG(Path(p['path']).lstat().st_mode)and ids(Path(p['path']).lstat())==p['identity']
def verify(p):assert pin(p['path'])==norm(p)
def inventory():
    files={};dirs={}
    for q,ns,fs in os.walk(ROOT,followlinks=False):
        p=Path(q);assert stat.S_ISDIR(p.lstat().st_mode);dirs[str(p)]=ids(p.lstat())
        for n in ns:assert stat.S_ISDIR((p/n).lstat().st_mode)
        for n in fs:
            x=p/n;s=x.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid();files[str(x)]=ids(s)
    return dict(files=files,dirs=dirs)
assert not OUT.exists()
d,pd=read(ROOT/'Root_actual_build_only_summary.json');t,pt=read(R/'ROOT_ACTUAL_CACHE336_DRIVER_BUILD_V1_FAILURE_TRUE_TOOL_RETURNS_20261014.json')
hf,phf=read(R/'native_rank1_cache336_build_host_source_v1_20261014/COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json')
sf,psf=read(R/'native_rank1_exact_cache336_source_v1_20261014/COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json')
cli,pcli=read(R/'native_rank1_cache336_build_host_source_v1_20261014/ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json');plan,pplan=read(R/'native_rank1_cache336_build_host_source_v1_20261014/EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json')
failure="RuntimeError('Driver-only compile must create exactly one object, no module or other outputs')"
term=t['actual_build_return'];assert t['observed_closed']is True and type(term['exit_code'])is int and term['exit_code']==1 and term.get('session_id')is None and t['original_integer_exit_code']==1
assert shlex.split(t['exact_executed_command'])==cli['argv'] and 'raise failure.with_traceback(failure_tb)'in term['output']and 'Driver-only compile must create exactly one object'in term['output']
assert d['status']=='ACTUAL_BUILD_FAILED_UNQUALIFIED'and d['failure']==failure and d['after_check_error']is None and d['secondary_failures']==[]and d['Dragon_linked']is False and d['final_report_resource_check_passed']is True
assert len(d['records'])==1 and len(d['fixed_current_pins'])==2605 and len(d['output_pins'])==6 and len(d['owned_runtime_pins'])==1
assert d['actual_host_Source_freeze_pin']==phf and d['actual_new_Source_freeze_pin']==psf and len(hf['dependencies'])==2604 and d['original_caps']==plan['original_caps']
fixed={p['path']:norm(p)for p in d['fixed_current_pins']};assert len(fixed)==2605
for p in hf['dependencies']+[hf['host_source'],phf,psf]+sf['files']+sf['original_source_pins']:
    assert fixed.get(p['path'])==norm(p)
for p in fixed.values():seven(p)
inv=inventory();assert set(inv['files'])=={p['path']for p in d['output_pins']}|{pd['path']}and len(inv['files'])==7
for p in d['output_pins']+[pd]:verify(p)
buildfiles=sorted(q.name for q in (ROOT/'build').iterdir());assert buildfiles==['SPOT_GLOBAL_NATIVE_DRIVER64.o','compile_Driver.log','compile_Driver.watchdog.json']
assert not (ROOT/'runtime/Dragon').exists()and not (ROOT/'build/link_Dragon.log').exists()and not (ROOT/'build/link_Dragon.watchdog.json').exists()
rec=d['records'][0];assert rec['label']=='build/compile_Driver'and rec['status']=='PASS'and rec['wall_cap_seconds']==600 and 0<rec['elapsed_seconds']<600
original70=plan['original_ordered70_input_pins'];expected=[plan['original_compiler_pin']['path'],*plan['original_compile_flags'],'-I'+str(ROOT/'build'),*plan['original_compile_include_arguments'],'-J'+str(ROOT/'build'),'-c',str(R/'native_rank1_exact_cache336_source_v1_20261014/SPOT_GLOBAL_NATIVE_DRIVER64.f'),'-o',str(ROOT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')]
assert rec['command']==expected
watch,pwatch=read(ROOT/'build/compile_Driver.watchdog.json');plog=pin(ROOT/'build/compile_Driver.log')
assert watch['command']==expected and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<600
assert plog['sha256']==rec['log_sha256']
stages,pstages=read(ROOT/'cache336-driver-build/stages.json');assert stages=={'stages':d['records']}
for p in original70+plan['current_nine_core_object_pins']+plan['historical_original_nine_core_object_pins']:verify(p)
for p in [hf['host_source']]+sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins']:verify(p)
assert type(d['SELF_peak_bytes'])is int and 0<=d['SELF_peak_bytes']<512*2**20 and 0<d['wall_seconds']<1800
reserve=96*2**30-d['resources_before']['artifact_bytes']-20971764748-64*2**20-2*2**30;assert reserve>0
for k in ('resources_before','resources_after','resources_after_including_summary_bytes'):
    s=d[k];assert s['artifact_budget_bytes']==96*2**30 and s['min_free_bytes']==8*2**30 and s['artifact_bytes']<=96*2**30 and s['disk_free_bytes']>=8*2**30
    f=s['fresh_output'];assert f['artifact_budget_bytes']==2*2**30 and f['resource_roots']==[str(ROOT)]and f['artifact_bytes']<=2*2**30
for p in fixed.values():seven(p)
for p in seen.values():seven(p)
assert inventory()==inv
obj=pin(ROOT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')
OUT.mkdir()
v=dict(schema='INDEPENDENT_CACHE336_DRIVER_V1_COMPILE_INVENTORY_HOST_FAILURE_POSTVERIFY_V1',status='PASS_POSTVERIFY_GENUINE_DRIVER_V1_HOST_FILE_ENUMERATION_FAILURE_UNQUALIFIED',failure=None,business_failure=failure,role='build_failure',actual_report_pin=pd,actual_Root_true_tool_return_pin=pt,actual_Root_terminal_return_field='actual_build_return',actual_Root_initial_return=t['actual_initial_return'],actual_Root_terminal_return=term,actual_Host_freeze_pin=phf,actual_Source_freeze_pin=psf,actual_CLI_pin=pcli,actual_PLAN_pin=pplan,actual_compiler_command=expected,actual_stage_count=1,actual_compiler_stage_PASS=True,actual_compiler_integer_returncode=0,actual_compiler_watch_pin=pwatch,actual_compiler_log_pin=plog,actual_stages_pin=pstages,actual_compile_created_Driver_object_pin=obj,actual_physical_build_file_names=buildfiles,host_expected_one_file_but_ordinary_supervisor_logs_make_three=True,link_started=False,Dragon_linked=False,no_Module_output=True,mathematical_failure_not_inferred=True,all2605_fixed_current7_reobserved_twice=True,all2604_HF_dependencies_exact_in_fixed=True,actual_all7_output_full_EOF_pins=d['output_pins']+[pd],actual_output_inventory=inv,original70_objects_archives_full_EOF_unchanged=original70,actual_caps_unchanged=d['original_caps'],initial_fullfresh2_cold_meta_reserve_remaining_bytes=reserve,first_original_traceback_preserved=term['output'],no_secondary_errors=True,independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,independent_deletion_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,large_scientific_EOF_not_repeated=True,readonly=True,source_only=True,all_file_descriptors_closed=True,compile_qualified=False,new_cache_budget_control_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
p=OUT/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
with os.fdopen(fd,'w')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=v['status'],review_pin=pin(p),failure=None,business_failure=failure,actual_Root_exit_code=1),ensure_ascii=False))

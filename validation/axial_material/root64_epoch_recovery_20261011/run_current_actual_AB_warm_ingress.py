#!/usr/bin/env python3
"""Actual compile/link and full current A/B readonly typed ingress; no transport or old qualification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import sys
import time
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=ART/'axmat-native-real64-warm-ingress-20261011'
CONTROL_BIND=REC/'native_warm_ingress_source_v1/CURRENT_ACTUAL_AB_WARM_INGRESS_SOURCE_BINDING.json'
SUPPORT=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
OLD_BIND=ART/'axial-material-ROOT64-connected-typed-fixture-original-guard-20261011/Root_fixed_source_and_exact_command_binding.json'
COMPILER=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def main():
    start=time.monotonic()
    if OUT.exists()or OUT.is_symlink():raise RuntimeError('fresh output; one attempt no overwrite')
    if any(os.environ.get(k)!='1'for k in THREADS)or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:raise RuntimeError('original one-thread nonoptimized unprofiled environment')
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7':raise RuntimeError('original support Source bytes')
    sp=importlib.util.spec_from_file_location('boot_compile_original_support',SUPPORT)
    support=importlib.util.module_from_spec(sp);sp.loader.exec_module(support)
    if Path(sys.executable).resolve()!=support.PYTHON:raise RuntimeError('original exact Python')
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'boot_compile_original_helper')
    factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'boot_compile_original_resources')
    full,production=helper.modules();guard_files=helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:raise RuntimeError('original supervisor MRO and genuine source paths')
    def pin(p):
        p=Path(p);before=support.identity(p)
        with p.open('rb')as f:
            s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
            if opened!=before:raise RuntimeError('input opened7ID')
            sha=hashlib.file_digest(f,'sha256').hexdigest()
            s=os.fstat(f.fileno());eof=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        if eof!=before or support.identity(p)!=before:raise RuntimeError('input EOF/after7ID')
        return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
    if hashlib.sha256(CONTROL_BIND.read_bytes()).hexdigest()!='d69b9be915c0275099ae12e868353435db81ee214b89f7089961699850a6030c':raise RuntimeError('full current control binding bytes')
    control=json.loads(CONTROL_BIND.read_text())
    sources=[REC/'native_warm_ingress_source_v1/test_actual_AB_warm_ingress64.f90']
    control_dependencies=[Path(p['path'])for p in control['actual_current_full_EOF_dependency_pins']]
    includes=[ART/'axial-material-new-REAL64-producer-compile-only-20261011/build',
              ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build',
              ART/'axial-material-r64-system-normalization-20261003/build',
              ROOT/'lib/Darwin_arm64/modules',ROOT/'Ganlib/lib/Darwin_arm64/modules']
    module_files=sorted({p for folder in includes for p in folder.glob('*.mod')})
    fixed=[pin(p)for p in sources+module_files+guard_files+[CONTROL_BIND,*control_dependencies,SUPPORT,support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT,support.BOUNDED,COMPILER,Path(__file__).resolve(),OLD_BIND]]
    reviewed_new_sources={str(sources[0]):'dc356915621b5d0138776c4af52b2424902b20c019835b9b85709706279b68ee'}
    for p in control['actual_current_full_EOF_dependency_pins']:
        if pin(p['path'])!=p:raise RuntimeError('frozen complete control dependency changed')
    for p in fixed:
        if p['path']in reviewed_new_sources and p['sha256']!=reviewed_new_sources[p['path']]:raise RuntimeError('independently reviewed new Source changed')
    original_runtime_sources={str(support.PARENT):support.PARENT_SHA,str(support.BOUNDED):support.BOUNDED_SHA,str(support.FULL):support.FULL_SHA}
    for p in fixed:
        if p['path']in original_runtime_sources and p['sha256']!=original_runtime_sources[p['path']]:raise RuntimeError('original runtime Source bytes changed')
    old=json.loads(OLD_BIND.read_text())
    expected={p['path']:p['sha256']for p in old['fixed']}
    for p in fixed:
        if p['path']in expected and p['sha256']!=expected[p['path']]:raise RuntimeError('original immutable byte input differs')
    if fixed[-3]['sha256']!='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492':raise RuntimeError('original compiler bytes')
    history=factory.DynamicHistoryResources(ART,factory.history_roots([str(OUT)],ART),8*2**30,96*2**30,production.ResourceFailure)
    fresh=production.DiskResources(ART,[str(OUT)],8*2**30,2*2**30)
    class Resources:
        def check(self):
            h=history.check();f=fresh.check()
            if h['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB original cold reserve')
            if f['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('filesystem8GiB original reserves')
            return dict(h,fresh_output=f)
    resources=Resources();before=resources.check()
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir();(OUT/'ROOT64_COMPILE_ONLY').mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    build=OUT/'build';runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'ROOT64_COMPILE_ONLY',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('genuine current runner binding')
    flags=old['compile_commands'][0][1:10]
    if flags!=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']:raise RuntimeError('original complete compiler flags')
    commands=control['planned_commands']
    if commands[0][1:10]!=flags or commands[1][1:3]!=old['compile_commands'][-1][1:3] or control['planned_output_root']!=str(OUT) or control['planned_working_directory']!=str(OUT) or len(commands)!=4:raise RuntimeError('original flags/exact fresh command binding')
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    write(OUT/'Root_current_compile_only_binding.json',dict(fixed_current_pins=fixed,actual_commands=commands,original_flags=flags,scope='compile/link/full actual A/B type4 readonly ingress; no transport or old qualification'))
    failure=None;watchdog_checks=[];after=None;after_check_error=None;actual_cases=[];actual_control_summary=None
    try:
        for index,command in enumerate(commands):
            for p in fixed:
                if pin(p['path'])!=p:raise RuntimeError('current fixed input changed')
            runner.execute(OUT,'compile_'+str(index),command,600)
            watchdog_checks.append(helper.check_watch(OUT,runner.records[-1]))
        for p in fixed:
            if pin(p['path'])!=p:raise RuntimeError('current fixed input changed at close')
        rows=[]
        for index in (2,3):
            lines=(OUT/('compile_'+str(index)+'.log')).read_text().splitlines()
            if len(lines)!=1:raise RuntimeError('exact one actual ingress JSON per A/B case')
            rows.append(json.loads(lines[0]))
        actual_cases=rows
        if [p['case']for p in rows]!=control['expected_cases']:raise RuntimeError('exact actual A/B order')
        for p in rows:
            if p['schema']!='ACTUAL_NEW_REAL64_WARM_INGRESS_V1' or p['status']!='PASS':raise RuntimeError('actual ingress status')
            if (p['groups'],p['unknowns'],p['scalar_regions'],p['flux_values'])!=(370,14,8,5180):raise RuntimeError('complete actual dimensions')
            if any(p[k]is not True for k in ('native_flux_bits_equal','native_keff_bits_equal','archive_read_only')):raise RuntimeError('actual native bit equality')
            if p['flux_non32_roundtrip_count']<=0 or p['source_non32_roundtrip_count']<0:raise RuntimeError('actual REAL32 round-trip distinction')
            if any(p[k]is not False for k in ('transport_executed','producer_qualified','online_BOOT_qualified','original_seventeen_controls_qualified','goal_complete')):raise RuntimeError('actual scope boundary')
        actual_control_summary=dict(status='TWO_ACTUAL_READONLY_AB_INGRESS_CHECKS_COMPLETED',cases=2,groups_each=370,flux_values_each=5180,transport_executed=False,producer_qualified=False,online_BOOT_qualified=False,original_seventeen_controls_qualified=False,goal_complete=False)
        after=resources.check()
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-start>=1800:raise RuntimeError('original SELF RSS or whole wall cap')
    except BaseException as error:
        failure=repr(error)
        try:after=resources.check()
        except BaseException as after_error:after_check_error=repr(after_error)
    report=dict(schema='ACTUAL_NEW_REAL64_AB_WARM_INGRESS_ROOT_V1',
        status='ACTUAL_AB_WARM_INGRESS_CLOSED0_ONLY'if failure is None else 'FAILED_CURRENT_AB_WARM_INGRESS_NO_RETRY',
        failure=failure,after_check_error=after_check_error,records=runner.records,fixed_current_pins=fixed,
        actual_cases=actual_cases,actual_control_summary=actual_control_summary,synthetic_fixture=False,
        actual_A_B_archives_readonly=True,external_input_full_EOF_SHA_and_7ID_stable=failure is None,
        actual_watchdog_checks=watchdog_checks,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_pins=[pin(p)for p in sorted(list(build.iterdir())+list(OUT.glob('*.log'))+list(OUT.glob('*.watchdog.json')))if p.is_file()],
        original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
        resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
        complete_native_build_qualified=False,Dragon_linked=False,transport_executed=False,
        original_seventeen_controls_executed=False,continuous_REAL64_producer_qualified=False,
        online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    write(OUT/'Root_actual_compile_only_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records),wall_seconds=report['wall_seconds'])))
    return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Five complete global native64 caller compiles against actual v2 publisher; no transport."""
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
OUT=ART/'axial-material-new-global-native64-caller-compile-only-20261012'
BOOT=REC/'global_native64_caller_source_v1'
MANIFEST=REC/'GLOBAL_NATIVE64_CALLER_NEW_PUBLISHER_DEPENDENCY_BINDING_20261012.json'
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
    manifest=json.loads(MANIFEST.read_text())
    sources=[BOOT/name for name in ['SPOT_GLOBAL_CALLER_CARRIERS.f90','SPOT_GLOBAL_CALLER_API.f90','FLUGPG64.f','FLUDRVG64.f','FLUGLOBAL64.f']]
    includes=[ART/'axial-material-new-bootstrap-global-projection-v2-compile-only-20261012/build',
              ART/'axial-material-new-SPOT-global-native64-dependencies-compile-only-20261011/build',
              ART/'axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012/build',
              ART/'axial-material-new-REAL64-producer-compile-only-20261011/build',
              ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build',
              ART/'axial-material-r64-system-normalization-20261003/build',
              ROOT/'lib/Darwin_arm64/modules',ROOT/'Ganlib/lib/Darwin_arm64/modules']
    module_files=sorted({p for folder in includes for p in folder.glob('*.mod')})
    declared=manifest['source_pins']+manifest['actual_dependency_pins']
    all_paths=list(dict.fromkeys([Path(p['path'])for p in declared]+sources+module_files+[MANIFEST]+guard_files))
    fixed=[pin(p)for p in all_paths+[SUPPORT,support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT,support.BOUNDED,COMPILER,Path(__file__).resolve(),OLD_BIND]]
    current_by_path={p['path']:p for p in fixed}
    for p in declared:
        expected_pin=dict(path=p['path'],sha256=p['sha256'],size_bytes=p['bytes'],identity=p['seven_id'])
        if current_by_path[p['path']]!=expected_pin:raise RuntimeError('complete frozen bootstrap Source or dependency full EOF/identity changed')
    reviewed_new_sources={'/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/global_native64_caller_source_v1/SPOT_GLOBAL_CALLER_CARRIERS.f90': '3d05dc9888cb9b2d40fc15e9bb997b752f17e74e550c389bc13fdbca583f931d', '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/global_native64_caller_source_v1/SPOT_GLOBAL_CALLER_API.f90': '82cd1831b2fde7db507365e988cc692162ec8693d8380e09f0cc7d3f943c178d', '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/global_native64_caller_source_v1/FLUGPG64.f': 'c0bbea6ddbd83c0c0f8a9b7188fcfc9dc316380dcde3f3857ea11ec6c667c83a', '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/global_native64_caller_source_v1/FLUDRVG64.f': '9c5ade26cc35ac43b1e735a499e07e4d1118ed230ea30546ae55349261b0b74b', '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/global_native64_caller_source_v1/FLUGLOBAL64.f': '574360e6a4e02dbe133286eca21a25983c6d2a7f69de5256dcd23285667b78c7'}
    for p,sha in reviewed_new_sources.items():
        if current_by_path[p]['sha256']!=sha:raise RuntimeError('independently reviewed bootstrap v2 Source bytes')
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
    commands=[[str(COMPILER),*flags,'-I'+str(build),*['-I'+str(p)for p in includes],'-J'+str(build),'-c',str(p),'-o',str(build/(p.stem+'.o'))]for p in sources]
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    write(OUT/'Root_current_compile_only_binding.json',dict(fixed_current_pins=fixed,actual_commands=commands,original_flags=flags,scope='five unchanged full frozen global native64 caller Sources compiled against the actually compiled new v2 canonical/context/publisher and full global native64 dependencies; no link, global solve, online BOOT or control/physics qualification'))
    failure=None;watchdog_checks=[];after=None;after_check_error=None
    try:
        for index,command in enumerate(commands):
            for p in fixed:
                if pin(p['path'])!=p:raise RuntimeError('current fixed input changed')
            runner.execute(build,'compile_'+str(index),command,600)
            watchdog_checks.append(helper.check_watch(OUT,runner.records[-1]))
        for p in fixed:
            if pin(p['path'])!=p:raise RuntimeError('current fixed input changed at close')
        after=resources.check()
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-start>=1800:raise RuntimeError('original SELF RSS or whole wall cap')
    except BaseException as error:
        failure=repr(error)
        try:after=resources.check()
        except BaseException as after_error:after_check_error=repr(after_error)
    report=dict(schema='ACTUAL_GLOBAL_NATIVE64_CALLER_FIVE_COMPILE_ONLY_V2_DEPENDENCIES',
        status='FIVE_GLOBAL_NATIVE64_CALLER_COMPILE_STEPS_CLOSED0_ONLY'if failure is None else 'FAILED_COMPILE_ONLY_NO_RETRY',
        failure=failure,after_check_error=after_check_error,records=runner.records,fixed_current_pins=fixed,
        actual_watchdog_checks=watchdog_checks,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_pins=[pin(p)for p in sorted(build.iterdir())if p.is_file()],
        original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
        resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
        complete_native_build_qualified=False,Dragon_linked=False,transport_executed=False,
        original_seventeen_controls_executed=False,continuous_REAL64_producer_qualified=False,
        online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    write(OUT/'Root_actual_compile_only_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records),wall_seconds=report['wall_seconds'])))
    return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())

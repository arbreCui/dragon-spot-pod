#!/usr/bin/env python3
"""Root full connected17 controls with the complete frozen package pinned at every stage."""
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
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-CTX-expected-three-planes-compile-only-20261012')
CONTROL_BIND=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_connected17_compile_namespace_repair_v3/CURRENT_FULL_CONNECTED17_NAMESPACE_V3_CORRECTED_DEPENDENCY_BINDING.json')
CONTROL_FREEZE=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_connected17_compile_namespace_repair_v3/COMPLETE_NAMESPACE_REPAIR_V3_CORRECTED_PACKAGE_FREEZE.json')
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
    if hashlib.sha256(CONTROL_BIND.read_bytes()).hexdigest()!='bb9b735f6baf8b5cc7cdea0d584284903177e1da6ef98e15e479e4b66d15fd52':raise RuntimeError('full current control binding bytes')
    control=json.loads(CONTROL_BIND.read_text())
    if pin(CONTROL_FREEZE) != {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_connected17_compile_namespace_repair_v3/COMPLETE_NAMESPACE_REPAIR_V3_CORRECTED_PACKAGE_FREEZE.json', 'size_bytes': 64668, 'sha256': 'e94403e33c0387f2c852f2706e9e27ba6884a3223d0cc132be7aab7a78f82557', 'identity': [16777234, 49770345, 33188, 1, 64668, 1791740369045538704, 1791740369045538704]}:raise RuntimeError('Root exact complete package freeze binding')
    complete_freeze=json.loads(CONTROL_FREEZE.read_text())
    package_pins=complete_freeze['complete_package_file_pins_before_manifest']
    if len(package_pins)!=33 or complete_freeze['actual_dependency_full_EOF_pins']!=control['actual_current_full_EOF_dependency_pins']:raise RuntimeError('Root complete package and dependencies')
    for p in package_pins:
        if pin(p['path'])!=p:raise RuntimeError('Root complete frozen package changed')
    package_files=[Path(p['path'])for p in package_pins]
    sources=[Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bootstrap_context_expected_planes_source_v3/SPOR64_BOOT_CONTEXT64.f90')]
    control_dependencies=[Path(p['path'])for p in control['actual_current_full_EOF_dependency_pins']]
    includes=[Path('/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-global-projection-v2-compile-only-20261012/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-BOOT-compile-only-20261011/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build'), Path('/Users/wen/spot/lib/Darwin_arm64/modules'), Path('/Users/wen/spot/Ganlib/lib/Darwin_arm64/modules')]
    module_files=sorted({p for folder in includes for p in folder.glob('*.mod')})
    diagnostic_fixed=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-full-connected17-namespace-repair-v3-20261012/build/test_ROOT64_full_connected17_v2.o', 'size_bytes': 159616, 'sha256': '8b3e7cd0fff432f53cc3a756bbe8e75abbfd939df1e25c9b85b46a194b157b2c', 'identity': [16777234, 49770375, 33188, 1, 159616, 1791740379297447092, 1791740379297447092]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-full-connected17-namespace-repair-v3-20261012/Root_actual_compile_only_summary.json', 'size_bytes': 1332061, 'sha256': 'b510b4a3b54a11b20dfe76be9ace99b52bf3fe50314d4141d33f90d0ef7e8840', 'identity': [16777234, 49770390, 33188, 1, 1332061, 1791740382610349447, 1791740382610349447]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-full-connected17-namespace-repair-v3-20261012/build/compile_2.log', 'size_bytes': 238, 'sha256': 'b39cd7ae32de3044bb2cbf1e9c80b568fa4d4e1541d8b605f602b81feeae8675', 'identity': [16777234, 49770386, 33188, 1, 238, 1791740382073778856, 1791740382073778856]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_pub_first_reject_diagnostic_root_v1/COMPLETE_PUB_DIAGNOSTIC_WHOLE_BYTE_INVERSE.json', 'size_bytes': 34390, 'sha256': '174200c44be8e2dbbbcd0d1e3f9b4423b80caaa58a8885753e755fce81c8ef48', 'identity': [16777234, 49771822, 33188, 1, 34390, 1791741259319096527, 1791741259319096527]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_pub_first_reject_diagnostic_root_v1/CURRENT_DIAGNOSTIC_COMMAND_AND_FULL_INPUT_BINDING.json', 'size_bytes': 7312, 'sha256': '094bea0d1ac989d3c9ec4c866fb0673cd7e31d638ddc2c14e4937893778cc169', 'identity': [16777234, 49771823, 33188, 1, 7312, 1791741259323624742, 1791741259323624742]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bootstrap_context_expected_planes_source_v3/COMPLETE_EXPECTED_THREE_PLANES_NAMESPACE_REPAIR_BYTE_INVERSE.json', 'size_bytes': 2301, 'sha256': '894897e50a8e3e507097f6a51ba8a08f8cad467588e6f500e92a875ee784d9f9', 'identity': [16777234, 49772223, 33188, 1, 2301, 1791741759696796036, 1791741759696796036]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bootstrap_context_expected_planes_source_v3/CURRENT_CONTEXT_PRODUCTION_COMPILE_ONLY_BINDING.json', 'size_bytes': 2443, 'sha256': '2fd7cc0e68aee1d8bcb17797a80fdc806d10f3039e1dafbac2d21dee4b8c0496', 'identity': [16777234, 49772224, 33188, 1, 2443, 1791741759697143495, 1791741759697143495]}]
    for p in diagnostic_fixed:
        if pin(p['path'])!=p:raise RuntimeError('Root diagnostic actual input binding changed')
    fixed=[pin(p)for p in sources+module_files+guard_files+[CONTROL_BIND,*control_dependencies,CONTROL_FREEZE,*package_files,*[Path(p['path'])for p in diagnostic_fixed],SUPPORT,support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT,support.BOUNDED,COMPILER,Path(__file__).resolve(),OLD_BIND]]
    reviewed_new_sources={str(sources[0]):'298ba1fe8d96b960d867786d9324a9062f10fb5f16b6217fa8b96c7ec8f24300'}
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
    commands=[['/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', '-O2', '-march=native', '-ffp-contract=off', '-fcheck=all', '-fbacktrace', '-g', '-fPIC', '-frecord-marker=4', '-ffixed-line-length-none', '-I/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-global-projection-v2-compile-only-20261012/build', '-I/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012/build', '-I/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-BOOT-compile-only-20261011/build', '-I/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build', '-I/Users/wen/spot/lib/Darwin_arm64/modules', '-I/Users/wen/spot/Ganlib/lib/Darwin_arm64/modules', '-J/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-CTX-expected-three-planes-compile-only-20261012/build', '-c', '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/bootstrap_context_expected_planes_source_v3/SPOR64_BOOT_CONTEXT64.f90', '-o', '/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-CTX-expected-three-planes-compile-only-20261012/build/SPOR64_BOOT_CONTEXT64.o']]
    if len(commands)!=1 or commands[0][1:10]!=flags:
        raise RuntimeError('original complete flags and one exact context compile')
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    write(OUT/'Root_current_compile_only_binding.json',dict(fixed_current_pins=fixed,actual_commands=commands,original_flags=flags,scope='compile complete repaired Context only; fixed three planes; no solver/control PASS/physics qualification'))
    failure=None;watchdog_checks=[];after=None;after_check_error=None;actual_cases=[]
    coherent_baseline=None;coherent_after=None;coherent_manifest_pin=None;external_refusal=None
    try:
        for index,command in enumerate(commands):
            for p in fixed:
                if pin(p['path'])!=p:raise RuntimeError('current fixed input changed')
            if index==19:
                if coherent_baseline is None or coherent_manifest_pin is None:
                    raise RuntimeError('independent coherent baseline missing before actual rewrite')
                if pin(coherent_manifest_pin['path'])!=coherent_manifest_pin:
                    raise RuntimeError('independent coherent baseline manifest changed before rewrite')
                if pin(build/'coherent_complete_context.xsm')!=coherent_baseline:
                    raise RuntimeError('baseline full EOF and7ID changed before intended rewrite')
            runner.execute(build,'compile_'+str(index),command,600)
            watchdog_checks.append(helper.check_watch(OUT,runner.records[-1]))
            if index==18:
                coherent_baseline=pin(build/'coherent_complete_context.xsm')
                external_manifest=OUT/'Host_independent_coherent_baseline_full_EOF_SHA_7ID.json'
                write(external_manifest,dict(schema='INDEPENDENT_HOST_COHERENT_BASELINE_FULL_FILE_BINDING_V1',
                    actual_before_pin=coherent_baseline,expected_case='coherent_source_tamper',
                    Source_or_internal_labels_are_not_authority=True))
                coherent_manifest_pin=pin(external_manifest)
            if index==19:
                coherent_after=pin(build/'coherent_complete_context.xsm')
                if pin(coherent_manifest_pin['path'])!=coherent_manifest_pin:
                    raise RuntimeError('independent host baseline manifest changed')
                if coherent_after['sha256']==coherent_baseline['sha256']:
                    raise RuntimeError('no actual coherent full-file byte mutation occurred')
                if coherent_after['identity']==coherent_baseline['identity']:
                    raise RuntimeError('actual coherent rewrite lacks changed7ID')
                external_refusal=dict(case='coherent_source_tamper',
                    assertion='independent host exact fullEOF SHA and7ID binding',
                    before=coherent_baseline,after=coherent_after,
                    actual_SHA_matches=False,actual_seven_ID_matches=False,
                    actual_refused=True,Fortran_internal_refusal_claimed=False)
        for p in fixed:
            if pin(p['path'])!=p:raise RuntimeError('current fixed input changed at close')
        # Diagnostic does not parse or certify any of the seventeen controls.
        after=resources.check()
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-start>=1800:raise RuntimeError('original SELF RSS or whole wall cap')
    except BaseException as error:
        failure=repr(error)
        try:after=resources.check()
        except BaseException as after_error:after_check_error=repr(after_error)
    report=dict(schema='ACTUAL_CURRENT_REPAIRED_EXPECTED_THREE_PLANES_CONTEXT_COMPILE_ROOT_V3',
        status='ONE_REPAIRED_CONTEXT_COMPILE_STEP_CLOSED0_ONLY'if failure is None else 'FAILED_CURRENT_CONTEXT_COMPILE_NO_RETRY',
        failure=failure,after_check_error=after_check_error,records=runner.records,fixed_current_pins=fixed,
        actual_cases=actual_cases,actual_logical_control_count=None,
        actual_run_phase_count=len(actual_cases),actual_independent_host_coherent_refusal=external_refusal,
        independent_coherent_baseline_manifest_pin=coherent_manifest_pin,
        actual_watchdog_checks=watchdog_checks,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_pins=[pin(p)for p in sorted(build.iterdir())if p.is_file()],
        original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
        resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
        all17_original_names_exercised=False,
        lost_old17_fixture_bytes_or_exact_old_data_reexecuted=False,
        old_seventeen_PASS_inherited=False,synthetic_fixture=True,
        complete_native_build_qualified=False,Dragon_linked=False,transport_executed=False,
        continuous_REAL64_producer_qualified=False,online_BOOT_qualified=False,
        AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    write(OUT/'Root_actual_compile_only_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records),wall_seconds=report['wall_seconds'])))
    return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())

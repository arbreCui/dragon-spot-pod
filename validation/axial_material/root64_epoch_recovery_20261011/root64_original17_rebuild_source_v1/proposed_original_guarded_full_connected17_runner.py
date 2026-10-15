#!/usr/bin/env python3
"""Proposed original guarded full connected17 controls; never a solver or old PASS."""
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
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-full-connected17-controls-20261012')
CONTROL_BIND=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_original17_rebuild_source_v1/CURRENT_FULL_CONNECTED17_SOURCE_ORACLE_AND_COMMAND_BINDING.json')
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
    if hashlib.sha256(CONTROL_BIND.read_bytes()).hexdigest()!='c8b353dda86bafc16654a0ba7bead65c4c72caeada661ac4872807f49ef36633':raise RuntimeError('full current control binding bytes')
    control=json.loads(CONTROL_BIND.read_text())
    sources=[Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/root64_original17_rebuild_source_v1/test_ROOT64_full_connected17_v1.f90')]
    control_dependencies=[Path(p['path'])for p in control['actual_current_full_EOF_dependency_pins']]
    includes=[Path('/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-global-projection-v2-compile-only-20261012/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-new-ROOT64-BOOT-compile-only-20261011/build'), Path('/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build'), Path('/Users/wen/spot/lib/Darwin_arm64/modules'), Path('/Users/wen/spot/Ganlib/lib/Darwin_arm64/modules')]
    module_files=sorted({p for folder in includes for p in folder.glob('*.mod')})
    fixed=[pin(p)for p in sources+module_files+guard_files+[CONTROL_BIND,*control_dependencies,SUPPORT,support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT,support.BOUNDED,COMPILER,Path(__file__).resolve(),OLD_BIND]]
    reviewed_new_sources={str(sources[0]):'80a38a86e467e0b6595f28001e191ec56fe7143fd25e6000bcbb4e4fb038d312'}
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
    commands=[control['planned_compile_command'],control['planned_link_command']]+control['planned_run_commands']
    old_case_names=[command[-1]for command in old['control_commands']]
    if control['original_case_names']!=old_case_names or len(old_case_names)!=17 or len(commands)!=20:
        raise RuntimeError('all17 original names and18 actual run phases required')
    if [command[1]for command in control['planned_run_commands'][:16]]!=old_case_names[:16]:
        raise RuntimeError('exact originally declared first16 case order')
    if [command[1:]for command in control['planned_run_commands'][16:]]!=[
        ['coherent_source_tamper','prepare'],['coherent_source_tamper','rewrite']]:
        raise RuntimeError('explicit independent external binding phases')
    if commands[0][1:10]!=flags or commands[1][1:3]!=old['compile_commands'][-1][1:3] or control['planned_output_root']!=str(OUT):raise RuntimeError('original flags/exact fresh command binding')
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    write(OUT/'Root_current_compile_only_binding.json',dict(fixed_current_pins=fixed,actual_commands=commands,original_flags=flags,scope='compile/link/current full17 connected synthetic protocol controls; no solver/old PASS/physics qualification'))
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
        for phase_index,command in enumerate(control['planned_run_commands']):
            rows=[json.loads(line)for line in (build/('compile_'+str(phase_index+2)+'.log')).read_text().splitlines()]
            if len(rows)!=2:raise RuntimeError('exact actual assertion row and actual call-status row required')
            actual,counts=rows
            name=command[1];phase=command[2]if len(command)==3 else 'single'
            oracle=next(p for p in control['declared_case_oracles']if p['case']==name)
            if actual.get('case')!=name or actual.get('phase')!=phase or counts.get('case')!=name or counts.get('phase')!=phase:
                raise RuntimeError('actual case/phase differs from independently declared oracle')
            if actual.get('all_actual_assertions_completed')is not True or actual.get('synthetic_fixture')is not True:
                raise RuntimeError('actual complete Source assertions missing')
            if any(actual.get(k)is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
                raise RuntimeError('synthetic component scope must remain explicit')
            for key in ('actual_native_read_status','actual_q_read_status','actual_global_checks','actual_project_checks',
                        'explicit_q_build_calls','explicit_q_read_calls','explicit_native_publish_calls'):
                if counts.get(key)!=oracle['expected_'+key]:
                    raise RuntimeError('actual module status/count differs from independently declared oracle '+name+' '+key)
            actual_cases.append(dict(case=name,phase=phase,assertions=actual,actual_statuses_and_call_counts=counts))
        if len(actual_cases)!=18 or [p['case']for p in actual_cases[:16]]!=control['original_case_names'][:16]:
            raise RuntimeError('all17 semantic controls, including two true coherent phases, required')
        if external_refusal is None or external_refusal['actual_refused']is not True:
            raise RuntimeError('actual independent host full-file coherent rejection required')
        after=resources.check()
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-start>=1800:raise RuntimeError('original SELF RSS or whole wall cap')
    except BaseException as error:
        failure=repr(error)
        try:after=resources.check()
        except BaseException as after_error:after_check_error=repr(after_error)
    report=dict(schema='ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V1',
        status='ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY'if failure is None else 'FAILED_CURRENT17_COMPONENT_CONTROLS_NO_RETRY',
        failure=failure,after_check_error=after_check_error,records=runner.records,fixed_current_pins=fixed,
        actual_cases=actual_cases,actual_logical_control_count=17 if failure is None else None,
        actual_run_phase_count=len(actual_cases),actual_independent_host_coherent_refusal=external_refusal,
        independent_coherent_baseline_manifest_pin=coherent_manifest_pin,
        actual_watchdog_checks=watchdog_checks,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        output_pins=[pin(p)for p in sorted(build.iterdir())if p.is_file()],
        original_guard_class=full.OwnRSSSerialExecutor.__name__,original_guard_MRO_unchanged=True,
        resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
        all17_original_names_exercised=failure is None,
        lost_old17_fixture_bytes_or_exact_old_data_reexecuted=False,
        old_seventeen_PASS_inherited=False,synthetic_fixture=True,
        complete_native_build_qualified=False,Dragon_linked=False,transport_executed=False,
        continuous_REAL64_producer_qualified=False,online_BOOT_qualified=False,
        AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    write(OUT/'Root_actual_compile_only_summary.json',report)
    print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records),wall_seconds=report['wall_seconds'])))
    return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())

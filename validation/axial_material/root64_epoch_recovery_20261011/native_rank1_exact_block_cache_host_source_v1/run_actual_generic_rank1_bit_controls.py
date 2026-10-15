#!/usr/bin/env python3
"""Four genuine component stages; synthetic cache bits confer no physics admission."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
BASE = Path(__file__).resolve().parent
OUT = ART/'axial-material-new-generic-rank1-exact-cache-bit-controls-20261012-v1'
SUPPORT = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
PLAN = BASE/'CURRENT_ACTUAL_GENERIC_RANK1_BIT_HOST_BINDING.json'
HF_SCHEMA = 'COMPLETE_GENERIC_RANK1_EXACT_CACHE_BIT_HOST_SOURCE_FREEZE_V1'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FLAGS = ['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']
CAPS = dict(stage_seconds=600, whole_seconds=1800, SELF_and_child_RSS_bytes=512*2**20,
    fresh_bytes=2*2**30, history_bytes=96*2**30, cold_reserve_bytes=20971764748,
    metadata_reserve_bytes=64*2**20, free_floor_bytes=8*2**30,
    threads=1, children_at_once=1, retries=0)


def identity(value):
    return [value.st_dev,value.st_ino,value.st_mode,value.st_nlink,value.st_size,
            value.st_mtime_ns,value.st_ctime_ns]


def pin(path, owned=False):
    path = Path(path)
    before = identity(path.lstat())
    if not path.is_absolute() or not stat.S_ISREG(before[2]) or (owned and before[3] != 1):
        raise RuntimeError('real regular Source or separately owned nlink1 output required: '+str(path))
    fd = os.open(path, os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != before:
            raise RuntimeError('opened full7ID differs: '+str(path))
        sha = hashlib.sha256()
        count = 0
        while raw := os.read(fd,1024*1024):
            sha.update(raw)
            count += len(raw)
        if count != before[4] or identity(os.fstat(fd)) != before:
            raise RuntimeError('fullEOF size or seven identity fields differ: '+str(path))
    finally:
        os.close(fd)
    if identity(path.lstat()) != before:
        raise RuntimeError('postEOF full7ID differs: '+str(path))
    return dict(path=str(path),sha256=sha.hexdigest(),size_bytes=count,identity=before)


def same(wanted, owned=False):
    actual = pin(wanted['path'],owned)
    if actual != wanted:
        raise RuntimeError('complete current pin changed: '+wanted['path'])
    return actual


def unique(rows):
    table = {}
    for row in rows:
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('contradictory complete pins for '+row['path'])
        table[row['path']] = row
    return list(table.values())


def strict_json(raw):
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result:
                raise RuntimeError('duplicate JSON key: '+key)
            result[key] = value
        return result
    def invalid(value):
        raise RuntimeError('nonfinite JSON constant: '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid)


def write_new(path,value):
    raw = (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    fd = os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        with os.fdopen(fd,'wb',closefd=False) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(fd)
    finally:
        os.close(fd)
    return pin(path,True)


def replace_own_failed_summary(path,old_pin,value):
    # Only the just-written, separately owned summary may change after a late
    # check fails. Never overwrite Source, fixed inputs, or another run's file.
    same(old_pin,True)
    raw = (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    fd = os.open(path,os.O_RDWR|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != old_pin['identity']:
            raise RuntimeError('late failure summary ownership/opened7ID differs')
        os.ftruncate(fd,0)
        with os.fdopen(fd,'wb',closefd=False) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(fd)
    finally:
        os.close(fd)
    return pin(path,True)


def scope():
    return dict(formal_SN32_quadrature_equivalence=False,full370_qualified=False,
      genuine_solver_qualified=False,physics_qualified=False,three_plane_qualified=False,
      GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,
      ABA_admitted=False,goal_complete=False)


def historical_device_comparison(old,current):
    # This describes historical provenance only. Actual admissions always use
    # current all-seven-field pins; neither device nor the OS is substituted.
    if old['path'] != current['path'] or old['sha256'] != current['sha256'] or \
       old['size_bytes'] != current['size_bytes'] or old['identity'][1:] != current['identity'][1:]:
        raise RuntimeError('historical Source/compiler/library differs beyond the observed device field')
    return dict(historical_pin=old,current_pin=current,
      complete_SHA_and_remaining_six_fields_equal=True,
      full_seven_fields_equal=old['identity']==current['identity'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host-freeze-summary',required=True)
    parser.add_argument('--host-freeze-sha256',required=True)
    parser.add_argument('--host-freeze-seven-id',required=True)
    args = parser.parse_args()
    started = time.monotonic()
    if os.path.lexists(OUT) or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or \
       sys.getprofile() is not None or any(os.environ.get(k) != '1' for k in THREADS) or \
       os.environ.get('PYTHONDONTWRITEBYTECODE') != '1':
        raise RuntimeError('fresh once-only namespace and genuine unprofiled one-thread environment required')
    hf_pin = pin(args.host_freeze_summary)
    if hf_pin['sha256'] != args.host_freeze_sha256 or \
       hf_pin['identity'] != strict_json(args.host_freeze_seven_id):
        raise RuntimeError('mandatory external exact current Host freeze fullpin differs')
    hf = strict_json(Path(hf_pin['path']).read_text())
    if hf['schema'] != HF_SCHEMA or hf['compiler_executed'] is not False or \
       hf['component_controls_executed'] is not False or hf['planned_output_root'] != str(OUT) or \
       hf['original_caps'] != CAPS or hf['host_source']['path'] != str(Path(__file__).resolve()):
        raise RuntimeError('complete unexecuted own Host Source freeze required')
    fixed = unique([hf_pin,hf['host_source'],*hf['dependencies']])
    for row in fixed:
        same(row)
    table = {row['path']:row for row in fixed}
    if table.get(str(SUPPORT),{}).get('sha256') != SUPPORT_SHA or str(PLAN) not in table:
        raise RuntimeError('exact unchanged original support and own complete binding required')
    binding = strict_json(PLAN.read_text())
    if binding['schema'] != 'CURRENT_FULL7ID_GENERIC_RANK1_BIT_HOST_BINDING_V1' or \
       binding['Source_only'] is not True or binding['original_caps'] != CAPS or \
       binding['future_objects_runtime_and_result_pins'] is not None:
        raise RuntimeError('own unexecuted binding cannot predict future runtime pins')
    for row in binding['actual_current_input_pins']:
        if table.get(row['path']) != row:
            raise RuntimeError('every current dependency must be in mandatory Host freeze')
    comparisons = [historical_device_comparison(row['historical_pin'],row['current_pin'])
                   for row in binding['historical_device_only_provenance_comparisons']]
    spec = importlib.util.spec_from_file_location('generic_rank1_original_support',SUPPORT)
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    same(table[str(SUPPORT)])
    if Path(sys.executable).resolve() != support.PYTHON:
        raise RuntimeError('genuine original Python path required')
    helper,_ = support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'generic_rank1_original_helper')
    factory,_ = support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'generic_rank1_original_resources')
    full,production = helper.modules()
    guard_files = helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,) or \
       Path(full.__file__).resolve() != support.FULL or Path(production.__file__).resolve() != support.PARENT:
        raise RuntimeError('genuine original OwnRSS supervisor MRO and paths required')
    original = [(support.OLD_HELPER,support.OLD_HELPER_SHA),
      (support.RESOURCE_FACTORY,support.RESOURCE_SHA),(support.FULL,support.FULL_SHA),
      (support.PARENT,support.PARENT_SHA),(support.BOUNDED,support.BOUNDED_SHA)]
    for path,sha in original:
        if str(path) not in table or table[str(path)]['sha256'] != sha:
            raise RuntimeError('complete unchanged original guard Source hashes required')
        same(table[str(path)])
    for path in guard_files:
        if str(path) not in table:
            raise RuntimeError('complete genuine live guard evidence must be frozen')
        same(table[str(path)])
    original_sf = strict_json(Path(binding['historical_Fortran_Source_freeze_current_pin']['path']).read_text())
    original_plan = strict_json(Path(binding['historical_control_plan_current_pin']['path']).read_text())
    module_pin = binding['actual_module_Source_pin']
    control_pin = binding['actual_derived_control_Source_pin']
    old_control_pin = binding['actual_original_control_Source_pin']
    expected_sf_module = next(row for row in original_sf['files'] if row['path']==module_pin['path'])
    historical_device_comparison(expected_sf_module,module_pin)
    historical_device_comparison(original_plan['control_source_pin'],old_control_pin)
    derived = Path(control_pin['path']).read_bytes()
    original_control = Path(old_control_pin['path']).read_bytes()
    if derived != original_control+binding['explicit_control_XABORT_append'].encode() or \
       original_plan['expected_original_SPOT1P64_call_count'] != 110 or \
       original_plan['operator_field_mutation_count'] != 18:
        raise RuntimeError('unchanged original numerical control plus explicit failure-only abort routine required')
    history = factory.DynamicHistoryResources(ART,factory.history_roots([str(OUT)],ART),
                                             8*2**30,96*2**30,production.ResourceFailure)
    fresh = production.DiskResources(ART,[str(OUT)],8*2**30,2*2**30)
    class Resources:
        def check(self):
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= CAPS['SELF_and_child_RSS_bytes'] or \
               not 0 <= time.monotonic()-started < CAPS['whole_seconds']:
                raise RuntimeError('original SELF512 or whole1800 limit reached')
            h = history.check()
            f = fresh.check()
            if h['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes'] >= CAPS['history_bytes'] or \
               f['disk_free_bytes']-CAPS['cold_reserve_bytes']-CAPS['fresh_bytes'] < CAPS['free_floor_bytes']:
                raise RuntimeError('original history/free/cold/metadata reserve exceeded')
            return dict(h,fresh_output=f)
    resources = Resources()
    before = resources.check()
    if before['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']+CAPS['fresh_bytes'] >= CAPS['history_bytes']:
        raise RuntimeError('initial history reserves the full fresh2GiB plus original cold and metadata')
    compiler = binding['actual_compiler_pin']['path']
    library = binding['actual_Utilib_archive_pin']['path']
    module_object = str(OUT/'build/SPOT1P64.o')
    control_object = str(OUT/'build/test_generic_rank1_exact_cache_bits.o')
    executable = str(OUT/'runtime/test_generic_rank1_exact_cache_bits')
    commands = [[compiler,*FLAGS,'-I'+str(OUT/'build'),'-J'+str(OUT/'build'),
                 '-c',module_pin['path'],'-o',module_object],
      [compiler,*FLAGS,'-I'+str(OUT/'build'),'-J'+str(OUT/'build'),
                 '-c',control_pin['path'],'-o',control_object],
      [compiler,'-O2','-ffp-contract=off',module_object,control_object,library,'-o',executable],
      [executable]]
    if commands != binding['planned_four_stage_commands'] or FLAGS != binding['original_nine_compile_flags']:
        raise RuntimeError('exact original flags and four-stage dependency order required')
    OUT.mkdir()
    for name in ('build','runtime','controls'):
        (OUT/name).mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned = [pin(OUT/'runtime/run_bounded_dragon.py',True)]
    if owned[0]['sha256'] != support.BOUNDED_SHA:
        raise RuntimeError('copied genuine unchanged bounded Source required')
    runner = full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-started),'controls',resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve() != OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('genuine original executor and owned bounded Source required')
    owned.append(write_new(OUT/'Root_planned_component_binding.json',dict(
      actual_commands=commands,fixed_current_pins=fixed,original_caps=CAPS,
      historical_device_only_provenance_comparisons=comparisons,**scope())))
    failure = None
    after_error = None
    after = None
    actual_control = None
    watches = []
    def check_current():
        for row in fixed:
            same(row)
        for row in owned:
            same(row,True)
        return resources.check()
    try:
        for label,command in zip(('compile_module','compile_control','link_component','run_component'),commands):
            after = check_current()
            text = runner.execute(OUT/'controls',label,command,600)
            watches.append(helper.check_watch(OUT,runner.records[-1]))
            if label == 'compile_module':
                actual_names = sorted(p.name for p in (OUT/'build').iterdir())
                if actual_names != ['SPOT1P64.o','spot1p64_cache_mod.mod','spot1p64_r1_generic_cache_mod.mod']:
                    raise RuntimeError('actual compiled module output namespace differs')
                owned.extend(pin(p,True) for p in sorted((OUT/'build').iterdir()))
            elif label == 'compile_control':
                owned.append(pin(control_object,True))
            elif label == 'link_component':
                owned.append(pin(executable,True))
            else:
                lines = [line for line in text.splitlines() if line.startswith('{')]
                if len(lines) != 1:
                    raise RuntimeError('one actual complete control JSON record required')
                actual_control = strict_json(lines[0])
                expected = dict(status='ACTUAL_GENERIC_RANK1_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY',
                  actual_SPOT1P64_calls=original_plan['expected_original_SPOT1P64_call_count'],
                  formal_SN32_quadrature_equivalence=False,genuine_solver_qualified=False,
                  physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
                if set(actual_control) != set(expected)|{'actual_assertions'} or \
                   any(type(actual_control.get(k)) is not type(value) or actual_control.get(k) != value
                       for k,value in expected.items()) or \
                   type(actual_control['actual_SPOT1P64_calls']) is not int or \
                   type(actual_control['actual_assertions']) is not int or actual_control['actual_assertions'] != 301:
                    raise RuntimeError('actual emitted assertions/counts or synthetic scope differs')
                owned.append(write_new(OUT/'actual_control_stdout_record.json',actual_control))
            after = check_current()
    except BaseException as exc:
        failure = type(exc).__name__+': '+str(exc)
    finally:
        try:
            after = check_current()
        except BaseException as exc:
            after_error = type(exc).__name__+': '+str(exc)
    outputs = [pin(p,True) for p in sorted(OUT.rglob('*')) if p.is_file()]
    good = failure is None and after_error is None and len(runner.records)==4 and \
      all(row['status']=='PASS' for row in runner.records) and actual_control is not None
    summary = dict(schema='ACTUAL_GENERIC_RANK1_EXACT_CACHE_COMPONENT_BIT_CONTROLS_V1',
      status='ACTUAL_FOUR_COMPONENT_STAGES_CLOSED0_ONLY' if good else 'ACTUAL_COMPONENT_FAILED_UNQUALIFIED_NO_RETRY',
      failure=failure,after_check_error=after_error,records=runner.records,
      actual_control_stdout_record=actual_control,fixed_current_pins=fixed,
      output_pins=outputs,owned_runtime_and_component_pins=owned,
      actual_host_Source_freeze_pin=hf_pin,actual_watchdog_checks=watches,
      original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
      SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      resources_before=before,resources_after=after,wall_seconds=time.monotonic()-started,
      original_caps=CAPS,transport_executed=False,component_controls_executed=actual_control is not None,
      actual_external_Root_closed0_receipt_required=True,**scope())
    summary_path = OUT/'Root_actual_component_bit_summary.json'
    summary_pin = write_new(summary_path,summary)
    try:
        same(summary_pin,True)
        after = check_current()  # Includes the complete just-written summary bytes.
    except BaseException as exc:
        summary['status'] = 'ACTUAL_COMPONENT_FAILED_UNQUALIFIED_NO_RETRY'
        summary['after_check_error'] = 'FINAL_SUMMARY_CHECK: '+type(exc).__name__+': '+str(exc)
        summary['wall_seconds'] = time.monotonic()-started
        replace_own_failed_summary(summary_path,summary_pin,summary)
        raise
    if not good:
        raise RuntimeError(failure or after_error or 'actual component stages incomplete')
    print(json.dumps(dict(status=summary['status'],actual_report_pin=summary_pin,
      actual_SPOT1P64_calls=actual_control['actual_SPOT1P64_calls'],
      actual_assertions=actual_control['actual_assertions'],**scope()),allow_nan=False),flush=True)


if __name__ == '__main__':
    main()

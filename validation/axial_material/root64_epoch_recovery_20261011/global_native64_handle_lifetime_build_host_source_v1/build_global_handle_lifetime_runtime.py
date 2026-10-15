#!/usr/bin/env python3
"""Build one frozen handle-lifetime driver and relink the actual ordered 69.

Source draft only until Root supplies both complete exact Source freezes.
Two genuine stages use the unchanged OwnRSSSerialExecutor; no transport,
controls, GLOBAL, rank, BOOT, AAA, or ABA qualification is granted here.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import time

R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE = Path(__file__).resolve().parent
COMMON = REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'
COMMON_SHA = 'e9273410d444e5c7d587cf0586e379491e441554e5601eca40e53eeac2b1e5eb'
PLAN = BASE/'CURRENT_ORIGINAL_COMPLETE69_REBIND_PLAN.json'
PLAN_SHA = '1f68c78cf3dc634879a5fff0ecc6fe1e441da71454c2e20c44aaf4cda03e41c3'
OUT = R/'validation/artifacts/axial-material-new-AAA3-global-native64-handle-lifetime-complete69-build-only-20261012-v1'
CASE = 'global-handle-build'
NEW_DRIVER = REC/'global_native64_handle_lifetime_source_v1/SPOT_GLOBAL_NATIVE_DRIVER64.f'
NEW_SOURCE_FREEZE = NEW_DRIVER.parent/'COMPLETE_GLOBAL_NATIVE64_HANDLE_LIFETIME_SOURCE_FREEZE.json'
HOST_SCHEMA = 'COMPLETE_GLOBAL_NATIVE64_HANDLE_LIFETIME_BUILD_HOST_SOURCE_FREEZE_V1'
SOURCE_SCHEMA = 'COMPLETE_GLOBAL_NATIVE64_HANDLE_LIFETIME_SOURCE_FREEZE_V1'
REPORT_SCHEMA = 'ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1'
PASS_STATUS = 'ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY'


def load_common():
    # Pin the genuine unchanged common Source before importing its definitions.
    def identity(s):
        return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                s.st_mtime_ns, s.st_ctime_ns]
    before = identity(COMMON.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('original common must be a regular non-symlink Source')
    with COMMON.open('rb') as f:
        if identity(os.fstat(f.fileno())) != before:
            raise RuntimeError('original common opened7ID differs')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        if identity(os.fstat(f.fileno())) != before:
            raise RuntimeError('original common EOF7ID differs')
    if identity(COMMON.lstat()) != before or digest != COMMON_SHA:
        raise RuntimeError('original common Source fullEOF SHA/7ID differs')
    spec = importlib.util.spec_from_file_location('global_handle_original_common', COMMON)
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    return common


def load_external(c, args, prefix):
    return c.load_json_exact(getattr(args, prefix+'_summary'),
                             getattr(args, prefix+'_sha256'),
                             getattr(args, prefix+'_seven_id'))


def unique_rows(rows):
    table = {}
    for row in rows:
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('inconsistent complete input path pins')
        table[row['path']] = row
    return list(table.values())


def commands(c, base, plan):
    """No sorting: replace exactly original input37, preserve all other tokens."""
    first = base['records'][0]['command']
    original = base['records'][-1]['command']
    pins = plan['original_complete69_ordered_input_pins']
    ordered = [x for x in original if x.endswith(('.o', '.a'))]
    if original != plan['original_complete69_link_command'] or \
       ordered != [r['path'] for r in pins] or len(ordered) != 69 or \
       len(set(ordered)) != 69 or sum(p.endswith('.o') for p in ordered) != 65 or \
       sum(p.endswith('.a') for p in ordered) != 4:
        raise RuntimeError('actual complete65 objects plus4 archives in original69 order required')
    if first[1:10] != c.FLAGS or c.FLAGS != plan['original_compile_flags'] or \
       first[0] != plan['original_compiler_pin']['path'] or \
       [x for x in first if x.startswith('-I')] != plan['original_compile_include_arguments']:
        raise RuntimeError('exact original compiler, nine flags and include order required')
    old = plan['original_driver_object_pin']['path']
    indices = [i for i, x in enumerate(ordered) if Path(x).name == 'SPOT_GLOBAL_NATIVE_DRIVER64.o']
    if indices != [37] or ordered[37] != old or \
       pins[37] != plan['original_driver_object_pin'] or \
       plan['replacement_zero_based_input_index'] != 37 or \
       original[:3] != [first[0], '-O2', '-ffp-contract=off'] or original[-2] != '-o' or \
       original[3:-2] != ordered:
        raise RuntimeError('exact original direct69 link structure and single driver slot required')
    new_object = str(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')
    includes = ['-I'+str(OUT/'build')]+plan['original_compile_include_arguments']
    compile_driver = [first[0], *c.FLAGS, *includes, '-J'+str(OUT/'build'),
                      '-c', str(NEW_DRIVER), '-o', new_object]
    link = list(original)
    link[3+37] = new_object
    link[-1] = str(OUT/'runtime/Dragon')
    new_ordered = [x for x in link if x.endswith(('.o', '.a'))]
    if len(new_ordered) != 69 or \
       [(i, a, b) for i, (a, b) in enumerate(zip(ordered, new_ordered)) if a != b] != [(37, old, new_object)] or \
       link[:3] != original[:3] or link[-2] != '-o':
        raise RuntimeError('only original driver slot may change in complete69 link')
    return [compile_driver, link]


def main():
    parser = argparse.ArgumentParser()
    for prefix in ('current69', 'seventeen', 'driver-source-freeze', 'host-freeze'):
        for suffix in ('summary', 'sha256', 'seven-id'):
            parser.add_argument('--'+prefix+'-'+suffix, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    c = load_common()
    plan_pin = c.pin(PLAN)
    if plan_pin['sha256'] != PLAN_SHA:
        raise RuntimeError('exact original69 Source-only rebind plan required')
    plan = json.loads(PLAN.read_text())
    if plan['schema'] != 'SOURCE_ONLY_GLOBAL_NATIVE64_HANDLE_LIFETIME_COMPLETE69_REBIND_PLAN_V1' or \
       plan['Source_only'] is not True or plan['compiler_executed'] is not False or \
       plan['transport_executed'] is not False or plan['planned_output_root'] != str(OUT) or \
       any(plan[k] is not None for k in ('new_driver_Source_pin', 'new_driver_object_pin', 'new_Dragon_runtime_pin')):
        raise RuntimeError('unexecuted original69 plan must not contain future pins')
    hf, phf = load_external(c, args, 'host_freeze')
    if hf['schema'] != HOST_SCHEMA or hf['compiler_executed'] is not False or \
       hf['transport_executed'] is not False or \
       Path(hf['host_source']['path']).resolve() != Path(__file__).resolve():
        raise RuntimeError('complete exact own Host Source-only freeze required')
    c.same_pin(__file__, hf['host_source'])
    c.verify_rows(hf['dependencies'])
    hf_table = {r['path']: r for r in unique_rows(hf['dependencies'])}
    if hf_table.get(str(PLAN)) != plan_pin or \
       hf_table.get(str(COMMON)) != plan['original_common_Source_pin']:
        raise RuntimeError('Host freeze must bind exact plan and original common')
    binding, fixed, support, helper, full, resources, before = c.initialize(OUT, start)
    expected_caps = dict(original_stage_wall_cap_seconds=600, whole_wall_cap_seconds=1800,
      SELF_and_each_own_child_RSS_cap_bytes=512*2**20, threads=1, children_at_once=1,
      retries=0, fresh_output_cap_bytes=2*2**30, history_cap_bytes=96*2**30,
      filesystem_floor_bytes=8*2**30, original_cold_reserve_bytes=20971764748)
    if plan['original_caps'] != expected_caps or any(binding[k] != v for k, v in expected_caps.items()):
        raise RuntimeError('original complete resource contract must remain exact')
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30 >= 96*2**30:
        raise RuntimeError('initial history96GiB reserves fullfresh2GiB, originalcold and metadata')
    base, pbase = load_external(c, args, 'current69')
    if pbase != plan['original_actual69_v4_report_pin'] or \
       base['schema'] != 'ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       base['status'] != 'ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       base['failure'] is not None or base['after_check_error'] is not None or \
       base['Dragon_linked'] is not True or base['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('exact genuine current69v4 ten-stage closed0 prerequisite required')
    c.closed_report(base, helper, Path(pbase['path']).parent, 10)
    premise = {k: base[k] for k in plan['original_actual69_v4_closed_scalar_premise']}
    if premise != plan['original_actual69_v4_closed_scalar_premise'] or \
       len(base['records']) != 10 or sum(r['status'] == 'PASS' for r in base['records']) != 10:
        raise RuntimeError('original69 premise is its actual closed ten-PASS scalar fact only')
    seventeen, p17 = c.admit17(args.seventeen_summary, args.seventeen_sha256,
                              args.seventeen_seven_id, helper)
    if p17 != plan['selected_actual_current17_report_pin']:
        raise RuntimeError('exact original current17 prerequisite fullpin required')
    sf, psf = load_external(c, args, 'driver_source_freeze')
    if Path(psf['path']) != NEW_SOURCE_FREEZE or sf['schema'] != SOURCE_SCHEMA or \
       sf['compiler_executed'] is not False or sf['transport_executed'] is not False or \
       sf['original_driver_Source_pin'] != plan['original_driver_Source_pin']:
        raise RuntimeError('new frozen driver must bind the exact original driver Source')
    sf_rows = unique_rows(sf['files']+sf['dependencies'])
    c.verify_rows(sf_rows)
    source_matches = [r for r in sf['files'] if Path(r['path']) == NEW_DRIVER]
    sf_table = {r['path']: r for r in sf_rows}
    ganlib = [R/'Ganlib/src'/name for name in ('LCMAUX.f90', 'lcm_c.c', 'xsm_c.c', 'xsm.h')]
    old_sf = REC/'global_native64_dependency_source_v2/COMPLETE_GLOBAL_NATIVE64_DEPENDENCY_SOURCE_FREEZE.json'
    if len(source_matches) != 1 or \
       sf_table.get(plan['original_driver_Source_pin']['path']) != plan['original_driver_Source_pin'] or \
       any(str(p) not in sf_table for p in [old_sf, *ganlib]) or \
       hf_table.get(str(NEW_SOURCE_FREEZE)) != psf or hf_table.get(pbase['path']) != pbase:
        raise RuntimeError('complete driver and Host Source freezes must bind actual old Source/mechanism and current69')
    planned = commands(c, base, plan)
    actual_table = {r['path']: r for r in unique_rows(base['fixed_current_pins']+base['output_pins'])}
    old69 = plan['original_complete69_ordered_input_pins']
    old9 = binding['seventeen_required_same_production_object_pins']
    if old9 != plan['original_nine_core_object_pins'] or len(old9) != 9:
        raise RuntimeError('exact original nine core object pins required')
    for row in old69+old9:
        if actual_table.get(row['path']) != row or row['path'] not in base['records'][-1]['command']:
            raise RuntimeError('original69 and originalnine complete pins must match actual link')
        c.same_pin(row['path'], row)
    for row in old9:
        if row['path'] not in planned[-1]:
            raise RuntimeError('each of the nine old core objects must remain in new link')
    c.same_pin(plan['original_nine_Fortran_Source_freeze_pin']['path'], plan['original_nine_Fortran_Source_freeze_pin'])
    fixed = unique_rows(fixed+[phf, hf['host_source'], plan_pin, pbase, p17, psf]+hf['dependencies']+
      sf_rows+old69+old9+base['fixed_current_pins']+base['output_pins']+
      seventeen['fixed_current_pins']+seventeen['output_pins'])
    c.verify_rows(fixed)
    OUT.mkdir()
    (OUT/'runtime').mkdir()
    (OUT/'build').mkdir()
    (OUT/CASE).mkdir()  # The genuine executor writes its case stages before launch.
    shutil.copy2(support.BOUNDED, OUT/'runtime/run_bounded_dragon.py')
    owned = [c.pin(OUT/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256'] != binding['original_bounded']['sha256'] or \
       owned[0]['size_bytes'] != binding['original_bounded']['size_bytes']:
        raise RuntimeError('exact original bounded Source copy required')
    runner = full.OwnRSSSerialExecutor(OUT, 1800-(time.monotonic()-start), CASE, resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve() != OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('unchanged genuine OwnRSS executor and owned bounded Source required')
    c.write(OUT/'Root_planned_build_binding.json', dict(
      fixed_current_pins=fixed, actual_commands=planned,
      original_complete69_ordered_input_pins=old69, original_nine_unchanged_objects=old9,
      original_actual69_v4_report_pin=pbase, new_driver_Source_pin=source_matches[0],
      replacement_zero_based_input_index=37, original_caps=expected_caps, **c.scope()))
    failure = None
    after_error = None
    after = None
    watches = []
    old9_after = False
    old69_after = False

    def check_current():
        c.check_full_current(fixed, owned)
        value = resources.check()
        if not 0 < time.monotonic()-start < 1800:
            raise RuntimeError('original whole1800 including admission and closeout')
        return value

    try:
        for label, command in zip(('compile_driver', 'link_Dragon'), planned):
            after = check_current()
            runner.execute(OUT/'build', label, command, 600)
            watches.append(helper.check_watch(OUT, runner.records[-1]))
            if label == 'compile_driver':
                owned.append(c.pin(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'))
            else:
                owned.append(c.pin(OUT/'runtime/Dragon'))
            after = check_current()
    except BaseException as exc:
        failure = type(exc).__name__+': '+str(exc)
    finally:
        try:
            after = check_current()
            c.verify_rows(old69)
            old69_after = True
            c.verify_rows(old9)
            old9_after = True
        except BaseException as exc:
            after_error = type(exc).__name__+': '+str(exc)
    outputs = [c.pin(p) for p in sorted(OUT.rglob('*')) if p.is_file()]
    good = failure is None and after_error is None and old69_after and old9_after and \
      len(runner.records) == 2 and all(r['status'] == 'PASS' for r in runner.records)
    c.write(OUT/'Root_actual_build_only_summary.json', dict(
      schema=REPORT_SCHEMA, status=PASS_STATUS if good else 'ACTUAL_BUILD_FAILED_UNQUALIFIED',
      failure=failure, after_check_error=after_error, records=runner.records,
      fixed_current_pins=fixed, output_pins=outputs, owned_runtime_pins=owned,
      original_actual69_v4_report_pin=pbase, original_actual69_v4_closed_scalar_premise=dict(
        premise, actual_stage_count=10, actual_PASS_count=10),
      actual_driver_Source_freeze_pin=psf, actual_driver_Source_pin=source_matches[0],
      actual_host_Source_freeze_pin=phf, original_nine_Fortran_Source_freeze_pin=plan['original_nine_Fortran_Source_freeze_pin'],
      original_complete69_ordered_input_pins=old69,
      actual_complete69_link_inputs=[x for x in planned[-1] if x.endswith(('.o', '.a'))],
      replacement_zero_based_input_index=37,
      original69_inputs_identical_and_retained=old69_after,
      remaining68_link_inputs_identical_and_retained=old69_after,
      actual_watchdog_checks=watches, old_nine_objects_identical_and_retained=old9_after,
      original_guard_class='OwnRSSSerialExecutor', original_guard_MRO_unchanged=True,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      resources_before=before, resources_after=after, wall_seconds=time.monotonic()-start,
      original_caps=expected_caps, Dragon_linked=good, transport_executed=False,
      new_entry_controls_executed=False, terminal_receipt_required_for_qualification=True,
      **c.scope()))
    # The final summary itself also counts toward the original fresh/history
    # limits; any late failure gives a genuine nonzero Root terminal, no retry.
    check_current()
    if not good:
        raise RuntimeError(failure or after_error or 'actual incomplete two-stage build')


if __name__ == '__main__':
    main()

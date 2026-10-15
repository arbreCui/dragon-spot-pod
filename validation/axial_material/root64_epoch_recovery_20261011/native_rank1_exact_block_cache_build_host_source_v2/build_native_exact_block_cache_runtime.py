#!/usr/bin/env python3
"""Frozen current mount Source-only Host: module, driver, ordered complete70.

Root supplies actual current Fortran and own Host freezes before execution.
The original69 inputs are retained: replace only driver37 and insert the module
before the first archive. No cache effect, GLOBAL, BOOT or science is qualified.
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
COMMON = REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'
COMMON_SHA = 'baed0ead3b1159b7874c5f606bf97978673e11074ef131131c402bec50982454'
COMMON_PIN = {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_mount_full_identity_common_source_v1/guarded_warm_A_common.py', 'sha256': 'baed0ead3b1159b7874c5f606bf97978673e11074ef131131c402bec50982454', 'size_bytes': 20521, 'identity': [16777229, 49923959, 33188, 1, 20521, 1791804997861817826, 1791804997861817826]}
PLAN = BASE/'CURRENT_ORIGINAL69_TO_COMPLETE70_BUILD_PLAN.json'
PLAN_SHA = 'cb7f670b67d487861c8fd8a7b3975217ebc64c1bd14f1a9573c13e97235e4964'
SOURCE = REC/'native_rank1_exact_block_cache_source_v1'
SF_PATH = SOURCE/'COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_FREEZE.json'
SF_SCHEMA = 'COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_ONLY_FREEZE_V1'
HF_SCHEMA = 'COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_BUILD_HOST_SOURCE_ONLY_FREEZE_V2'
OUT = R/'validation/artifacts/axial-material-new-native-rank1-exact-block-cache-complete70-build-only-20261012-v2'
CASE = 'exact-cache-build'
SOURCE_ORDER = ['SPOT1P64.f90', 'SPOT_GLOBAL_NATIVE_DRIVER64.f']
REPORT_SCHEMA = 'ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2'
PASS_STATUS = 'ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'


def load_common():
    def identity(s):
        return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                s.st_mtime_ns, s.st_ctime_ns]
    before = identity(COMMON.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('regular unchanged original common Source required')
    with COMMON.open('rb') as stream:
        if identity(os.fstat(stream.fileno())) != before:
            raise RuntimeError('original common opened7ID differs')
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if identity(os.fstat(stream.fileno())) != before:
            raise RuntimeError('original common EOF7ID differs')
    if identity(COMMON.lstat()) != before or digest != COMMON_SHA or \
       dict(path=str(COMMON), sha256=digest, size_bytes=before[4], identity=before) != COMMON_PIN:
        raise RuntimeError('exact original common fullEOF SHA/7ID')
    spec = importlib.util.spec_from_file_location('exact_cache_current_mount_common', COMMON)
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    return c


def unique_rows(rows):
    table = {}
    for row in rows:
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('inconsistent complete input pins')
        table[row['path']] = row
    return list(table.values())


def rewrite_owned_summary(c, path, previous, summary):
    if previous['identity'][3] != 1 or Path(previous['path']) != path:
        raise RuntimeError('only this new singly linked owned summary may be rewritten')
    c.same_pin(path, previous)
    descriptor = os.open(path, os.O_WRONLY | os.O_NOFOLLOW)
    try:
        item = os.fstat(descriptor)
        actual = [item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
                  item.st_size, item.st_mtime_ns, item.st_ctime_ns]
        if actual != previous['identity']:
            raise RuntimeError('owned summary opened7ID changed before controlled rewrite')
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            descriptor = None
            stream.seek(0)
            stream.truncate(0)
            json.dump(summary, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if c.identity(path)[:4] != previous['identity'][:4]:
        raise RuntimeError('owned summary inode/role changed after controlled rewrite')


def commands(c, base, plan):
    original = base['records'][-1]['command']
    old = original[3:-2]
    first = base['records'][0]['command']
    if original != plan['original_current69_link_command'] or \
       old != [r['path'] for r in plan['original_current69_ordered_input_pins']] or \
       len(old) != 69 or len(set(old)) != 69 or \
       sum(p.endswith('.o') for p in old) != 65 or sum(p.endswith('.a') for p in old) != 4 or \
       original[:3] != [first[0], '-O2', '-ffp-contract=off'] or original[-2] != '-o':
        raise RuntimeError('exact actual65 objects and4 archives in direct69 order')
    if first[1:10] != c.FLAGS or c.FLAGS != plan['original_compile_flags'] or \
       first[0] != plan['original_compiler_pin']['path'] or \
       [x for x in first if x.startswith('-I')] != plan['original_compile_include_arguments']:
        raise RuntimeError('exact original compiler/flags/include order')
    if [i for i, p in enumerate(old) if Path(p).name == 'SPOT_GLOBAL_NATIVE_DRIVER64.o'] != [37] or \
       old[37] != plan['original_current_driver_object_pin']['path'] or \
       plan['replacement_zero_based_current69_input_index'] != 37:
        raise RuntimeError('single genuine current driver input37')
    includes = ['-I'+str(OUT/'build')]+plan['original_compile_include_arguments']
    result = [[first[0], *c.FLAGS, *includes, '-J'+str(OUT/'build'),
               '-c', str(SOURCE/name), '-o', str(OUT/'build'/(Path(name).stem+'.o'))]
              for name in SOURCE_ORDER]
    replaced = list(old)
    driver = str(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')
    module = str(OUT/'build/SPOT1P64.o')
    if any(Path(p).name == 'SPOT1P64.o' for p in old):
        raise RuntimeError('new module object must not alias an existing explicit input')
    replaced[37] = driver
    at = next(i for i, p in enumerate(old) if p.endswith('.a'))
    if at != plan['module_insertion_current69_before_archive_index']:
        raise RuntimeError('exact original first archive insertion position')
    new70 = replaced[:at]+[module]+replaced[at:]
    if len(new70) != 70 or [p for p in new70 if p != module] != replaced or \
       [(i, a, b) for i, (a, b) in enumerate(zip(old, replaced)) if a != b] != [(37, old[37], driver)] or \
       [p for p in new70 if p.endswith('.a')] != [p for p in old if p.endswith('.a')]:
        raise RuntimeError('one module insertion, only driver37 replacement, all original relative order')
    result.append([*original[:3], *new70, '-o', str(OUT/'runtime/Dragon')])
    return result


def main():
    parser = argparse.ArgumentParser()
    for prefix in ('current69', 'original69', 'source-freeze', 'host-freeze'):
        for suffix in ('summary', 'sha256', 'seven-id'):
            parser.add_argument('--'+prefix+'-'+suffix, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    c = load_common()
    plan_pin = c.pin(PLAN)
    if plan_pin['sha256'] != PLAN_SHA:
        raise RuntimeError('exact complete69-to70 current mount Source-only plan required')
    plan, confirmed_plan_pin = c.read_bound_json_current(PLAN, plan_pin)
    if confirmed_plan_pin != plan_pin:
        raise RuntimeError('exact actual current plan read required')
    future = ('actual_new_SPOT1P64_object_pin',
              'actual_new_driver_object_pin', 'actual_new_Dragon_pin', 'actual_new_build_report_pin')
    if plan['source_only'] is not True or plan['compiler_executed'] is not False or \
       plan['transport_executed'] is not False or plan['planned_output_root'] != str(OUT) or \
       any(plan[k] is not None for k in future):
        raise RuntimeError('Source plan contains no predicted object/runtime/report pins')

    def load(prefix):
        return c.load_json_exact(getattr(args, prefix+'_summary'),
                                 getattr(args, prefix+'_sha256'),
                                 getattr(args, prefix+'_seven_id'))

    hf, phf = load('host_freeze')
    if hf['schema'] != HF_SCHEMA or hf['compiler_executed'] is not False or \
       hf['transport_executed'] is not False or \
       Path(hf['host_source']['path']).resolve() != Path(__file__).resolve():
        raise RuntimeError('real independently reviewed complete own Host Source freeze required')
    c.same_pin(__file__, hf['host_source'])
    c.verify_rows(hf['dependencies'])
    hf_table = {r['path']: r for r in unique_rows(hf['dependencies'])}
    if hf_table.get(str(PLAN)) != plan_pin or \
       hf_table.get(str(COMMON)) != plan['selected_current_common_Source_pin'] or \
       hf_table.get(plan['selected_current_mount_catalog_pin']['path']) != plan['selected_current_mount_catalog_pin']:
        raise RuntimeError('Host freeze must bind exact current plan/common')
    binding, fixed, support, helper, full, resources, before = c.initialize(OUT, start)
    caps = dict(original_stage_wall_cap_seconds=600, whole_wall_cap_seconds=1800,
      SELF_and_each_own_child_RSS_cap_bytes=512*2**20, threads=1, children_at_once=1,
      retries=0, fresh_output_cap_bytes=2*2**30, history_cap_bytes=96*2**30,
      filesystem_floor_bytes=8*2**30, original_cold_reserve_bytes=20971764748)
    if plan['original_caps'] != caps or any(binding[k] != v for k, v in caps.items()):
        raise RuntimeError('exact unchanged original resource contract')
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30 >= 96*2**30:
        raise RuntimeError('initial original fullfresh2/cold/metadata/history96 reserve')
    base, pbase = load('current69')
    previous, pprevious = load('original69')
    if pbase != plan['original_actual69_handle_lifetime_report_pin'] or \
       pprevious != plan['original_actual69_v4_report_pin'] or \
       base['original_actual69_v4_report_pin'] != pprevious or \
       base['schema'] != 'ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1' or \
       base['status'] != 'ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       previous['schema'] != 'ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       previous['status'] != 'ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       base['Dragon_linked'] is not True or previous['Dragon_linked'] is not True:
        raise RuntimeError('exact actual current2 and separate original10 complete69 origins required')
    c.closed_report(base, helper, Path(pbase['path']).parent, 2)
    c.closed_report(previous, helper, Path(pprevious['path']).parent, 10)
    old69 = previous['records'][-1]['command'][3:-2]
    current69 = base['records'][-1]['command'][3:-2]
    if len(old69) != 69 or len(current69) != 69 or \
       [i for i in range(69) if old69[i] != current69[i]] != [37] or \
       base['remaining68_link_inputs_identical_and_retained'] is not True or \
       base['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('actual current69 retains old68 and originalnine')
    sf, psf = load('source_freeze')
    if Path(psf['path']) != SF_PATH or psf != plan['actual_new_Source_freeze_pin'] or \
       sf['schema'] != SF_SCHEMA or sf['candidate_imported_or_executed'] is not False or sf['compiled'] is not False:
        raise RuntimeError('real complete two-new-Source freeze required; no future SF prediction')
    sf_rows = unique_rows(sf['files']+sf['original_source_pins']+sf['control_sources']+
      [sf['complete_byte_inverse_pin'], sf['control_plan_pin'], sf['logical_memory_key_contract_pin']])
    c.verify_rows(sf_rows)
    new_sources = []
    for name in SOURCE_ORDER:
        matches = [r for r in sf['files'] if Path(r['path']) == SOURCE/name]
        if len(matches) != 1:
            raise RuntimeError('exact complete new module and driver Source paths')
        new_sources.append(matches[0])
    original_table = {r['path']: r for r in unique_rows(sf['original_source_pins'])}
    if original_table.get(plan['original_SPOT1P64_Source_pin']['path']) != plan['original_SPOT1P64_Source_pin'] or \
       original_table.get(plan['original_current_driver_Source_pin']['path']) != plan['original_current_driver_Source_pin'] or \
       hf_table.get(str(SF_PATH)) != psf or hf_table.get(pbase['path']) != pbase or \
       hf_table.get(pprevious['path']) != pprevious:
        raise RuntimeError('new Sources and Host must bind exact current original Source and both real69 reports')
    bit, pbit = c.read_bound_json_current(plan['actual_component_bit_control_report_pin']['path'],
                                         plan['actual_component_bit_control_report_pin'])
    bit_review, pbit_review = c.read_bound_json_current(plan['actual_component_bit_control_Root_review_pin']['path'],
                                                     plan['actual_component_bit_control_Root_review_pin'])
    if bit['schema'] != 'ACTUAL_GENERIC_RANK1_EXACT_CACHE_COMPONENT_BIT_CONTROLS_V1' or \
       bit['status'] != 'ACTUAL_FOUR_COMPONENT_STAGES_CLOSED0_ONLY' or \
       bit_review['actual_report_pin'] != pbit or bit_review['actual_SPOT1P64_calls'] != 110 or \
       bit_review['actual_assertions'] != 301 or bit_review['all_four_actual_watches_closed0_original_caps'] is not True or \
       hf_table.get(pbit['path']) != pbit or hf_table.get(pbit_review['path']) != pbit_review:
        raise RuntimeError('actual independent four-stage bit controls and Root closed0 review required')
    c.closed_report(bit, helper, Path(pbit['path']).parent, 4)
    original69_pins = plan['original_current69_ordered_input_pins']
    old9 = binding['seventeen_required_same_production_object_pins']
    if old9 != plan['original_nine_core_object_pins'] or len(old9) != 9:
        raise RuntimeError('exact oldnine object pins')
    table = {r['path']: r for r in unique_rows(base['fixed_current_pins']+base['output_pins'])}
    for row in original69_pins+old9:
        if table.get(row['path']) != row or row['path'] not in current69:
            raise RuntimeError('each original69 and oldnine object must equal genuine current input')
        c.same_pin(row['path'], row)
    planned = commands(c, base, plan)
    if any(row['path'] not in planned[-1] for row in old9):
        raise RuntimeError('all oldnine remain in ordered70 link')
    fixed = unique_rows(fixed+[plan_pin, phf, hf['host_source'], psf, pbase, pprevious]+
      hf['dependencies']+sf_rows+base['fixed_current_pins']+base['output_pins']+
      previous['fixed_current_pins']+previous['output_pins']+bit['fixed_current_pins']+
      bit['output_pins']+[pbit, pbit_review]+original69_pins+old9)
    c.verify_rows(fixed)
    OUT.mkdir()
    (OUT/'build').mkdir()
    (OUT/'runtime').mkdir()
    (OUT/CASE).mkdir()
    shutil.copy2(support.BOUNDED, OUT/'runtime/run_bounded_dragon.py')
    owned = [c.pin(OUT/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256'] != binding['original_bounded']['sha256'] or \
       owned[0]['size_bytes'] != binding['original_bounded']['size_bytes']:
        raise RuntimeError('exact unchanged original owned bounded Source')
    runner = full.OwnRSSSerialExecutor(OUT, 1800-(time.monotonic()-start), CASE, resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve() != OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('genuine unchanged OwnRSS class/MRO/resources and bounded Source')
    c.write(OUT/'Root_planned_build_binding.json', dict(
      fixed_current_pins=fixed, actual_commands=planned, new_Source_pins=new_sources,
      original_current69_ordered_input_pins=original69_pins, original_nine_objects=old9,
      original_actual69_handle_lifetime_report_pin=pbase, original_actual69_v4_report_pin=pprevious,
      replacement_zero_based_current69_input_index=37,
      module_insertion_current69_before_archive_index=plan['module_insertion_current69_before_archive_index'],
      original_caps=caps, actual_component_bit_control_report_pin=pbit,
      actual_component_bit_control_Root_review_pin=pbit_review,
      current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),
      historical_source_and_predecessor_reports_unmodified=True,
      prior_business_stages_reexecuted_by_metadata_view=False,
      requires_host_process_metadata_access=True, **c.scope()))
    failure = None
    after_error = None
    after = None
    watches = []
    retained = False

    def check_current():
        c.check_full_current(fixed, owned)
        value = resources.check()
        if not 0 < time.monotonic()-start < 1800:
            raise RuntimeError('original whole1800 including admission and final closeout')
        return value

    try:
        for label, command in zip(('compile_module', 'compile_driver', 'link_Dragon'), planned):
            after = check_current()
            runner.execute(OUT/'build', label, command, 600)
            watches.append(helper.check_watch(OUT, runner.records[-1]))
            if label == 'compile_module':
                owned.append(c.pin(OUT/'build/SPOT1P64.o'))
                owned.extend(c.pin(p) for p in sorted((OUT/'build').glob('*.mod')))
            elif label == 'compile_driver':
                owned.append(c.pin(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'))
            else:
                owned.append(c.pin(OUT/'runtime/Dragon'))
            after = check_current()
    except BaseException as error:
        failure = type(error).__name__+': '+str(error)
    finally:
        try:
            after = check_current()
            c.verify_rows(original69_pins)
            c.verify_rows(old9)
            retained = True
        except BaseException as error:
            after_error = type(error).__name__+': '+str(error)
    outputs = [c.pin(p) for p in sorted(OUT.rglob('*')) if p.is_file()]
    good = failure is None and after_error is None and retained and \
      len(runner.records) == 3 and all(r['status'] == 'PASS' for r in runner.records)
    summary_path = OUT/'Root_actual_build_only_summary.json'
    summary = dict(
      schema=REPORT_SCHEMA, status=PASS_STATUS if good else 'ACTUAL_BUILD_FAILED_UNQUALIFIED',
      failure=failure, after_check_error=after_error, records=runner.records,
      fixed_current_pins=fixed, output_pins=outputs, owned_runtime_pins=owned,
      actual_watchdog_checks=watches, actual_new_Source_freeze_pin=psf,
      actual_new_Source_pins=new_sources, actual_host_Source_freeze_pin=phf,
      original_actual69_handle_lifetime_report_pin=pbase, original_actual69_v4_report_pin=pprevious,
      original_current69_ordered_input_pins=original69_pins,
      actual_complete70_link_inputs=planned[-1][3:-2],
      replacement_zero_based_current69_input_index=37,
      module_insertion_current69_before_archive_index=plan['module_insertion_current69_before_archive_index'],
      old69_inputs_identical_and_retained=retained, remaining68_original_inputs_identical_and_retained=retained,
      old_nine_objects_identical_and_retained=retained,
      original_guard_class='OwnRSSSerialExecutor', original_guard_MRO_unchanged=True,
      resources_before=before, resources_after=after, original_caps=caps,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      wall_seconds=time.monotonic()-start, Dragon_linked=good,
      transport_executed=False, new_entry_controls_executed=False,
      requires_host_process_metadata_access=True, terminal_receipt_required_for_qualification=True,
      actual_component_bit_control_report_pin=pbit,
      actual_component_bit_control_Root_review_pin=pbit_review,
      current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),
      historical_source_and_predecessor_reports_unmodified=True,
      prior_business_stages_reexecuted_by_metadata_view=False,
      cache_effect_or_memory_improvement_qualified=False, **c.scope())
    c.write(summary_path, summary)
    try:
        summary['resources_after_including_summary_bytes'] = check_current()
        summary['final_report_resource_check_passed'] = True
        summary['SELF_peak_bytes'] = c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        summary['wall_seconds'] = time.monotonic()-start
        rewrite_owned_summary(c, summary_path, c.pin(summary_path), summary)
        check_current()
    except BaseException as error:
        good = False
        after_error = type(error).__name__+': '+str(error)
        summary.update(status='ACTUAL_BUILD_FAILED_UNQUALIFIED', after_check_error=after_error,
          final_report_resource_check_passed=False, Dragon_linked=False)
        rewrite_owned_summary(c, summary_path, c.pin(summary_path), summary)
        try:
            check_current()
        except BaseException:
            pass
        raise RuntimeError(after_error) from error
    if not good:
        raise RuntimeError(failure or after_error or 'actual incomplete three-stage build')


if __name__ == '__main__':
    main()

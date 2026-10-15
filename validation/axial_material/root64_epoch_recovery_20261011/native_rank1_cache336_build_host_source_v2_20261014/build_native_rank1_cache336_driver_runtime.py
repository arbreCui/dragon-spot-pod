#!/usr/bin/env python3
"""One internal cache-bound Driver compile and exact ordered70 relink.

The genuine compact BOOTQ build remains the premise. Only Driver at index37
is replaced; all69 other ordered inputs, current9 core and four archives
remain exact. Component bit controls and a future guarded full50 are separate.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import shutil
import time

R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE = Path(__file__).resolve().parent
PLAN = HERE/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json'
COMMON = REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py'
COMMON_SHA = 'a5b774a6b62e229f8f6360a284354e2f0af8ff3860602b061de376b2624fc040'
SOURCE = REC/'native_rank1_exact_cache336_source_v1_20261014'
SF = SOURCE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'
OUT = R/'validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v2'
HF_SCHEMA = 'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'
SF_SCHEMA = 'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1'
REPORT_SCHEMA = 'ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'
PASS_STATUS = 'ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'


def load_common():
    def identity(s):
        return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    before = identity(COMMON.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('regular exact Common Source required')
    fd = os.open(COMMON,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != before:
            raise RuntimeError('Common opened7ID changed')
        with os.fdopen(fd,'rb') as stream:
            fd = None
            sha = hashlib.file_digest(stream,'sha256').hexdigest()
            if identity(os.fstat(stream.fileno())) != before:
                raise RuntimeError('Common EOF7ID changed')
    finally:
        if fd is not None:
            os.close(fd)
    if identity(COMMON.lstat()) != before or sha != COMMON_SHA:
        raise RuntimeError('Common fullEOF/after7ID/SHA differs')
    spec = importlib.util.spec_from_file_location('compact_bq_build_original_common',COMMON)
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    return c


def unique(rows):
    table = {}
    for row in rows:
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('inconsistent complete input pins')
        table[row['path']] = row
    return list(table.values())


def commands(c,base,plan):
    original = base['records'][-1]['command']
    old = original[3:-2]
    first = base['records'][0]['command']
    if original != plan['original_complete70_link_command'] or \
       old != [p['path'] for p in plan['original_ordered70_input_pins']] or \
       len(old) != 70 or len(set(old)) != 70 or \
       sum(p.endswith('.o') for p in old) != 66 or sum(p.endswith('.a') for p in old) != 4 or \
       original[:3] != [first[0],'-O2','-ffp-contract=off'] or original[-2] != '-o' or \
       [i for i,p in enumerate(old) if Path(p).name == 'SPOT_GLOBAL_NATIVE_DRIVER64.o'] != [37] or \
       old[37] != plan['original_Driver_object_pin']['path']:
        raise RuntimeError('exact compact70/one Driver input37/original order')
    if first[1:10] != c.FLAGS or c.FLAGS != plan['original_compile_flags'] or \
       first[0] != plan['original_compiler_pin']['path'] or \
       [v for v in first if v.startswith('-I')] != plan['original_compile_include_arguments']:
        raise RuntimeError('exact original compiler/flags/ordered includes')
    includes = ['-I'+str(OUT/'build')]+plan['original_compile_include_arguments']
    obj = str(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')
    compile_cmd = [first[0],*c.FLAGS,*includes,'-J'+str(OUT/'build'),
                   '-c',str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f'),'-o',obj]
    new = list(old)
    new[37] = obj
    if len(new) != 70 or len(set(new)) != 70 or \
       [(i,a,b) for i,(a,b) in enumerate(zip(old,new)) if a != b] != [(37,old[37],obj)] or \
       [p for p in new if p.endswith('.a')] != [p for p in old if p.endswith('.a')]:
        raise RuntimeError('only Driver37 replacement;69 retained inputs including BOOTQ40;four exact archives')
    return [compile_cmd,[*original[:3],*new,'-o',str(OUT/'runtime/Dragon')]]


def rewrite_summary(c,path,previous,data):
    if previous['identity'][3] != 1 or previous['path'] != str(path):
        raise RuntimeError('only owning single-link summary can be rewritten')
    c.same_pin(path,previous)
    fd = os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] != previous['identity']:
            raise RuntimeError('owned summary opened7ID changed')
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            fd = None
            stream.seek(0)
            stream.truncate(0)
            json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if fd is not None:
            os.close(fd)
    if c.identity(path)[:4] != previous['identity'][:4]:
        raise RuntimeError('own summary physical role changed')


def main():
    p = argparse.ArgumentParser()
    for prefix in ('original70','source-freeze','host-freeze'):
        for suffix in ('summary','sha256','seven-id'):
            p.add_argument('--'+prefix+'-'+suffix,required=True)
    args = p.parse_args()
    start = time.monotonic()
    c = load_common()
    def load(prefix):
        return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),
                                 getattr(args,prefix+'_seven_id'))
    hf,phf = load('host_freeze')
    if hf['schema'] != HF_SCHEMA or hf['compiler_executed'] is not False or \
       hf['numerical_executed'] is not False or Path(hf['host_source']['path']).resolve() != Path(__file__).resolve():
        raise RuntimeError('exact source-only owning complete Host freeze')
    c.same_pin(__file__,hf['host_source'])
    c.verify_rows(hf['dependencies'])
    hf_table = {r['path']:r for r in unique(hf['dependencies'])}
    plan_pin = hf['build_plan_pin']
    if plan_pin['path'] != str(PLAN) or hf_table.get(str(PLAN)) != plan_pin:
        raise RuntimeError('exact owning Source-only build plan in Host freeze')
    plan,checked = c.read_bound_json_current(PLAN,plan_pin)
    if checked != plan_pin or plan['source_only'] is not True or plan['compiler_executed'] is not False or \
       plan['numerical_executed'] is not False or plan['planned_output_root'] != str(OUT) or \
       any(plan[k] is not None for k in ('actual_new_Driver_object_pin','actual_new_Dragon_pin','actual_new_build_report_pin')):
        raise RuntimeError('no predicted actual outputs in Source plan')
    binding,fixed,support,helper,full,resources,before = c.initialize(OUT,start)
    caps = dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,
      SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,
      retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,
      filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748)
    if plan['original_caps'] != caps or any(binding[k] != v for k,v in caps.items()):
        raise RuntimeError('exact unchanged original resource contract')
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30 >= 96*2**30:
        raise RuntimeError('original initial fullfresh2/cold/metadata/history96 reserve')
    base,pbase = load('original70')
    if pbase != plan['original_actual_complete70_report_pin'] or hf_table.get(pbase['path']) != pbase or \
       base['schema'] != 'ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1' or \
       base['status'] != 'ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       base['Dragon_linked'] is not True or base['failure'] is not None or base['after_check_error'] is not None or \
       base['final_report_resource_check_passed'] is not True or \
       base['original69_other_inputs_identical_and_retained'] is not True or \
       base['original_four_archives_identical_and_retained'] is not True or \
       base['original_eight_unchanged_core_objects_identical_and_retained'] is not True or \
       base['replacement_zero_based_complete70_input_index'] != 40 or \
       base['actual_host_Source_freeze_pin'] != plan['selected_previous_complete70_Host_freeze_pin'] or \
       base['actual_new_Source_freeze_pin'] != plan['selected_previous_compact_Fortran_Source_freeze_pin']:
        raise RuntimeError('exact genuine compact BOOTQ closed2 build premise, selected previous freezes')
    c.closed_report(base,helper,Path(pbase['path']).parent,2)
    c.verify_rows(base['fixed_current_pins'])
    c.verify_rows(base['output_pins'])
    sf,psf = load('source_freeze')
    if Path(psf['path']) != SF or hf_table.get(str(SF)) != psf or sf['schema'] != SF_SCHEMA or \
       sf['source_only'] is not True or sf['compiled'] is not False or sf['numerical_executed'] is not False:
        raise RuntimeError('exact one-new-cache336 Driver Source-only complete freeze')
    sf_rows = unique(sf['files']+sf['original_source_pins']+[sf['complete_byte_inverse_pin'],sf['control_plan_pin']])
    c.verify_rows(sf_rows)
    matches = [r for r in sf['files'] if r['path'] == str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f')]
    if len(matches) != 1:
        raise RuntimeError('single exact new Driver Fortran Source')
    new_source = matches[0]
    if plan['original_Driver_Source_pin'] not in sf['original_source_pins'] or \
       plan['unchanged_SPOT1P64_Source_pin'] not in sf['original_source_pins'] or \
       sf['Driver_single_literal_368_to336'] is not True or sf['public_Driver_ABI_unchanged'] is not True or \
       sf['original_math_modified'] is not False or sf['internal_exact_cache_working_set_bytes'] != 336*2**20:
        raise RuntimeError('one cache-bound literal, whole original Driver/math and public ABI retained')
    old70 = plan['original_ordered70_input_pins']
    historical9 = binding['seventeen_required_same_production_object_pins']
    if historical9 != plan['historical_original_nine_core_object_pins'] or len(historical9) != 9:
        raise RuntimeError('historical original9 remain exact; not current new9 qualification')
    old9 = plan['current_nine_core_object_pins']
    if len(old9) != 9 or old9[:5]+old9[6:] != historical9[:5]+historical9[6:] or \
       old9[5] != plan['retained_current_BOOTQ_object_pin'] or old70[40] != old9[5] or \
       old70[37] != plan['original_Driver_object_pin']:
        raise RuntimeError('exact current9 unchanged; BOOTQ core6 link40 retained, Driver link37 outside core9')
    table = {r['path']:r for r in unique(base['fixed_current_pins']+base['output_pins'])}
    for row in old70+old9+historical9:
        if table.get(row['path']) != row or (row not in historical9 and row['path'] not in base['actual_complete70_link_inputs']):
            raise RuntimeError('every original input is exact actual70 authority')
        c.same_pin(row['path'],row)
    planned = commands(c,base,plan)
    fixed = unique(fixed+[phf,hf['host_source'],plan_pin,psf,pbase]+hf['dependencies']+sf_rows+
                   base['fixed_current_pins']+base['output_pins']+old70+old9+historical9)
    c.verify_rows(fixed)
    del base,sf,table,binding,hf_table
    OUT.mkdir()
    for name in ('build','runtime','cache336-driver-build'):
        (OUT/name).mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned = [c.pin(OUT/'runtime/run_bounded_dragon.py')]
    runner = full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'cache336-driver-build',resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve() != OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('original owning supervisor/MRO/resource/guard binding')
    c.write(OUT/'Root_planned_build_binding.json',dict(fixed_current_pins=fixed,actual_commands=planned,
      new_Source_pin=new_source,original_ordered70_input_pins=old70,original_nine_core_objects=old9,
      replacement_zero_based_complete70_input_index=37,original_caps=caps,
      original_actual_complete70_report_pin=pbase,**c.scope()))
    failure = None
    failure_tb = None
    secondary = []
    after = None
    watches = []
    retained = False
    def check():
        c.check_full_current(fixed,owned)
        result = resources.check()
        if not 0 < time.monotonic()-start < 1800:
            raise RuntimeError('original whole1800 includes admission/final closeout')
        return result
    try:
        for label,command in zip(('compile_Driver','link_Dragon'),planned):
            check()
            runner.execute(OUT/'build',label,command,600)
            watches.append(helper.check_watch(OUT,runner.records[-1]))
            if label == 'compile_Driver':
                expected_compile_files = ['SPOT_GLOBAL_NATIVE_DRIVER64.o','compile_Driver.log','compile_Driver.watchdog.json']
                if sorted(p.name for p in (OUT/'build').iterdir()) != expected_compile_files:
                    raise RuntimeError('Driver-only compile requires exact object/log/watch, no module or other outputs')
                for name in expected_compile_files:
                    path = OUT/'build'/name
                    state = path.lstat()
                    if not stat.S_ISREG(state.st_mode) or state.st_nlink != 1 or state.st_uid != os.getuid():
                        raise RuntimeError('own compile object/log/watch ordinary UID/single-link files')
                    actual_pin = c.pin(path)
                    if actual_pin['identity'] != [state.st_dev,state.st_ino,state.st_mode,state.st_nlink,state.st_size,state.st_mtime_ns,state.st_ctime_ns]:
                        raise RuntimeError('compile object/log/watch fullEOF all7 unchanged')
                owned.append(c.pin(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'))
            else:
                owned.append(c.pin(OUT/'runtime/Dragon'))
            after = check()
        c.verify_rows(old70)
        c.verify_rows(old9)
        retained = True
    except BaseException as error:
        failure = error
        failure_tb = error.__traceback__
    try:
        after = check()
    except BaseException as error:
        if failure is None:
            failure = error
            failure_tb = error.__traceback__
        else:
            secondary.append(dict(where='after_check',error=repr(error)))
    good = failure is None and retained and len(runner.records) == 2 and all(r['status'] == 'PASS' for r in runner.records)
    target = OUT/'Root_actual_build_only_summary.json'
    summary = None
    try:
        summary = dict(schema=REPORT_SCHEMA,status=PASS_STATUS if good else 'ACTUAL_BUILD_FAILED_UNQUALIFIED',
          failure=None if failure is None else repr(failure),after_check_error=None if not secondary else secondary[0]['error'],
          secondary_failures=secondary,records=runner.records,fixed_current_pins=fixed,
          output_pins=[c.pin(p) for p in sorted(OUT.rglob('*')) if p.is_file()],owned_runtime_pins=owned,
          actual_watchdog_checks=watches,actual_new_Source_freeze_pin=psf,actual_new_Source_pin=new_source,
          actual_host_Source_freeze_pin=phf,original_actual_complete70_report_pin=pbase,
          original_ordered70_input_pins=old70,actual_complete70_link_inputs=planned[-1][3:-2],
          replacement_zero_based_complete70_input_index=37,original_nine_core_object_pins=old9,
          original69_other_inputs_identical_and_retained=retained,original_four_archives_identical_and_retained=retained,
          current_nine_core_objects_identical_and_retained=retained,
          historical_original_nine_core_object_pins=historical9,
          selected_previous_complete70_Host_freeze_pin=plan['selected_previous_complete70_Host_freeze_pin'],
          selected_previous_compact_Fortran_Source_freeze_pin=plan['selected_previous_compact_Fortran_Source_freeze_pin'],
          retained_current_BOOTQ_object_pin=plan['retained_current_BOOTQ_object_pin'],
          unchanged_SPOT1P64_Source_pin=plan['unchanged_SPOT1P64_Source_pin'],
          internal_R1_exact_cache_working_set_bytes=336*2**20,original_RSS_acceptance_cap_bytes=512*2**20,
          new_cache_budget_component_control_qualification=False,new_reader_control_qualification=False,
          original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=caps,
          resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
          wall_seconds=time.monotonic()-start,Dragon_linked=good,transport_executed=False,
          new_entry_controls_executed=False,requires_host_process_metadata_access=True,
          terminal_receipt_required_for_qualification=True,final_report_resource_check_passed=False,**c.scope())
        c.write(target,summary)
        summary['resources_after_including_summary_bytes'] = check()
        summary['final_report_resource_check_passed'] = True
        summary['SELF_peak_bytes'] = c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        summary['wall_seconds'] = time.monotonic()-start
        rewrite_summary(c,target,c.pin(target),summary)
        check()
    except BaseException as error:
        if failure is None:
            failure = error
            failure_tb = error.__traceback__
        else:
            secondary.append(dict(where='publication',error=repr(error)))
        try:
            if summary is not None:
                summary.update(status='ACTUAL_BUILD_FAILED_UNQUALIFIED',Dragon_linked=False,
                  final_report_resource_check_passed=False,failure=repr(failure),secondary_failures=secondary)
                if target.exists():
                    rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as late:
            secondary.append(dict(where='failed_report_publication',error=repr(late)))
            try:
                os.write(2,('secondary publication: '+repr(late)+'\n').encode())
            except BaseException:
                pass
    if failure is not None:
        raise failure.with_traceback(failure_tb)
    if not good:
        raise RuntimeError('incomplete two-stage one-object ordered70 build')


if __name__ == '__main__':
    main()

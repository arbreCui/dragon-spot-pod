#!/usr/bin/env python3
"""New current-case observation runtime; compile/link only, no material job.

All complete70 inputs remain in order. Five original-math observation objects
are inserted before the first of the same four archives. Actual output origins
come from this guarded execution, never from a Source-time prediction.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import time

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v5'
COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'
ORDER=['AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','LIBMIX.observe.UNREADY.f',
       'LIBDEN.observe.UNREADY.f','TONDRV.context_observe.UNREADY.f','TONSPH.observe.UNREADY.f']
spec=importlib.util.spec_from_file_location('current_observation_original_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
from current_material_prerequisite_admission import admit_prerequisites,replace_owned_failure_summary,check_original_host_limits


def commands(base,out):
    original=base['records'][0]['command']
    if original[1:10]!=c.FLAGS:
        raise RuntimeError('exact original nine compiler flags')
    includes=['-I'+str(out/'build')]+[x for x in original if x.startswith('-I')]
    result=[[original[0],*c.FLAGS,*includes,'-J'+str(out/'build'),'-c',str(SOURCE/name),
             '-o',str(out/'build'/(Path(name).stem+'.o'))]for name in ORDER]
    link=list(base['records'][-1]['command'])
    old=[x for x in link if x.endswith(('.o','.a'))]
    if len(old)!=70 or sum(x.endswith('.a')for x in old)!=4 or link[-2]!='-o':
        raise RuntimeError('complete70 actual ordered link with four archives')
    if any(Path(x).stem in {Path(n).stem for n in ORDER}for x in old if x.endswith('.o')):
        raise RuntimeError('new observation objects cannot alias old inputs')
    at=next(i for i,x in enumerate(link)if x.endswith('.a'))
    added=[str(out/'build'/(Path(n).stem+'.o'))for n in ORDER]
    link[at:at]=added;link[-1]=str(out/'runtime/Dragon')
    actual=[x for x in link if x.endswith(('.o','.a'))]
    if len(actual)!=75 or [x for x in actual if x not in added]!=old:
        raise RuntimeError('all70 original inputs and order must remain')
    result.append(link)
    return result


def main():
    parser=argparse.ArgumentParser()
    for prefix in ['current70','source-freeze','host-freeze','aaa3','saved-audit']:
        for suffix in ['summary','sha256','seven-id']:
            parser.add_argument('--'+prefix+'-'+suffix,required=True)
    parser.add_argument('--output-dir',required=True)
    args=parser.parse_args();start=time.monotonic()
    out=Path(args.output_dir)
    if not out.is_absolute()or out.parent!=c.ART or os.path.lexists(out):
        raise RuntimeError('literal fresh artifact output, no overwrite or retry')
    def load(prefix):
        return c.load_json_exact(getattr(args,prefix+'_summary'),
          getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    hf,phf=load('host_freeze')
    if hf['schema']!='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_ONLY_FREEZE_V3' or \
       hf['compiler_executed']is not False or hf['transport_executed']is not False:
        raise RuntimeError('external actual Source-only host freeze')
    if hf['host_source']['path']!=str(Path(__file__).absolute()):
        raise RuntimeError('own complete host Source identity')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,resources,before=c.initialize(out,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('initial history96 reserves fresh2/cold/meta')
    build,pbuild=load('current70')
    if pbuild!=hf['selected_actual_build70_report']:raise RuntimeError('exact external selected actual70 report pin required')
    if build['schema']!='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2' or \
       build['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       build['failure'] is not None or build['after_check_error'] is not None or \
       build['Dragon_linked'] is not True or len(build['records'])!=3 or \
       build['final_report_resource_check_passed']is not True or \
       build['old69_inputs_identical_and_retained'] is not True or \
       build['remaining68_original_inputs_identical_and_retained'] is not True or \
       build['old_nine_objects_identical_and_retained'] is not True or \
       [record['label'].rsplit('/',1)[-1]for record in build['records']]!=['compile_module','compile_driver','link_Dragon']:
        raise RuntimeError('actual cache-module/driver compile and complete70 link required')
    c.closed_report(build,helper,Path(pbuild['path']).parent,3)
    c.verify_rows(build['fixed_current_pins']);c.verify_rows(build['output_pins'])
    current69_pin=build['original_actual69_handle_lifetime_report_pin']
    current69,checked_current69_pin=c.load_json_exact(current69_pin['path'],current69_pin['sha256'],json.dumps(current69_pin['identity']))
    if checked_current69_pin!=current69_pin or \
       current69_pin!=hf['selected_original_actual69_handle_lifetime_report'] or \
       current69['schema']!='ACTUAL_AAA3_NATIVE_GLOBAL_HANDLE_LIFETIME_COMPLETE69_BUILD_ONLY_V1' or \
       current69['status']!='ACTUAL_ONE_NATIVE_DRIVER_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       current69['failure'] is not None or current69['after_check_error'] is not None or \
       current69['Dragon_linked'] is not True or len(current69['records'])!=2 or \
       current69['remaining68_link_inputs_identical_and_retained'] is not True or \
       current69['old_nine_objects_identical_and_retained'] is not True:
        raise RuntimeError('separate actual native-handle complete69 two-stage premise required')
    c.closed_report(current69,helper,Path(current69_pin['path']).parent,2)
    c.verify_rows(current69['fixed_current_pins']);c.verify_rows(current69['output_pins'])
    original69_pin=build['original_actual69_v4_report_pin']
    original69,checked_original69_pin=c.load_json_exact(original69_pin['path'],original69_pin['sha256'],json.dumps(original69_pin['identity']))
    if checked_original69_pin!=original69_pin or \
       current69['original_actual69_v4_report_pin']!=original69_pin or \
       original69_pin!=hf['selected_original_actual69_v4_report'] or \
       original69['schema']!='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1' or \
       original69['status']!='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY' or \
       original69['failure'] is not None or original69['after_check_error'] is not None or \
       original69['Dragon_linked'] is not True or len(original69['records'])!=10:
        raise RuntimeError('original actual nine-alias complete69 ten-stage premise required')
    c.closed_report(original69,helper,Path(original69_pin['path']).parent,10)
    c.verify_rows(original69['fixed_current_pins']);c.verify_rows(original69['output_pins'])
    original69_link=original69['records'][-1]['command'][3:-2]
    current69_link=current69['records'][-1]['command'][3:-2]
    current70_link=build['records'][-1]['command'][3:-2]
    if len(original69_link)!=69 or len(current69_link)!=69 or \
       [i for i,(old_path,new_path)in enumerate(zip(original69_link,current69_link))if old_path!=new_path]!=[37] or \
       Path(original69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       Path(current69_link[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o':
        raise RuntimeError('only actual native-driver object position37 changed in the separate complete69 premise')
    module_positions=[i for i,path in enumerate(current70_link)if Path(path).name=='SPOT1P64.o']
    first_archive=next(i for i,path in enumerate(current69_link)if path.endswith('.a'))
    if len(current70_link)!=70 or len(set(current70_link))!=70 or module_positions!=[first_archive] or \
       build['actual_complete70_link_inputs']!=current70_link or \
       build['replacement_zero_based_current69_input_index']!=37 or \
       build['module_insertion_current69_before_archive_index']!=first_archive or \
       [row['path']for row in build['original_current69_ordered_input_pins']]!=current69_link:
        raise RuntimeError('one genuine cache module inserted immediately before the original first archive')
    stripped70=current70_link[:first_archive]+current70_link[first_archive+1:]
    if [i for i,(old_path,new_path)in enumerate(zip(current69_link,stripped70))if old_path!=new_path]!=[37] or \
       Path(stripped70[37]).name!='SPOT_GLOBAL_NATIVE_DRIVER64.o' or \
       [path for path in current70_link if path.endswith('.a')]!=[path for path in current69_link if path.endswith('.a')]:
        raise RuntimeError('removing the new cache helper and restoring only driver37 must recover exact original69 order')
    native_freeze_pin=hf['selected_native_exact_block_cache_source_freeze']
    native_sf,checked_native_freeze_pin=c.read_bound_json_current(native_freeze_pin['path'],native_freeze_pin)
    if checked_native_freeze_pin!=native_freeze_pin or build['actual_new_Source_freeze_pin']!=native_freeze_pin or \
       native_sf['schema']!='COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_ONLY_FREEZE_V1' or \
       native_sf['candidate_imported_or_executed']is not False or native_sf['compiled']is not False:
        raise RuntimeError('actual complete70 must bind the exact two-Fortran cache Source freeze')
    native_sf_rows=native_sf['files']+native_sf['original_source_pins']+native_sf['control_sources']+\
                   [native_sf['complete_byte_inverse_pin'],native_sf['control_plan_pin'],native_sf['logical_memory_key_contract_pin']]
    c.verify_rows(native_sf_rows)
    actual_new_sources=build['actual_new_Source_pins']
    if len(actual_new_sources)!=2 or \
       [Path(row['path']).name for row in actual_new_sources]!=['SPOT1P64.f90','SPOT_GLOBAL_NATIVE_DRIVER64.f'] or \
       any(row not in native_sf['files']for row in actual_new_sources) or \
       native_freeze_pin not in build['fixed_current_pins'] or \
       current69_pin not in build['fixed_current_pins'] or original69_pin not in build['fixed_current_pins']:
        raise RuntimeError('actual complete70 fixed pins must retain exact Sources and both genuine69 premises')
    c.verify_rows(build['original_current69_ordered_input_pins'])
    old9=binding['seventeen_required_same_production_object_pins']
    if len(old9)!=9 or any(row['path']not in current70_link for row in old9) or \
       any(row not in build['fixed_current_pins']for row in old9):
        raise RuntimeError('all original nine core objects remain exact current fixed inputs in complete70')
    base=build;pbase=pbuild
    gate_fixed,gate_receipts=admit_prerequisites(c,args,hf,helper)
    fixed+=gate_fixed+current69['fixed_current_pins']+current69['output_pins']+[current69_pin]+original69['fixed_current_pins']+original69['output_pins']+[original69_pin]+native_sf_rows
    sf,psf=load('source_freeze')
    if sf['schema']!='COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE_V1'or \
       sf['compiler_executed']is not False or sf['material_job_executed']is not False:
        raise RuntimeError('complete original-math observation Source freeze')
    c.verify_rows(sf['files']);c.verify_rows(sf['original_math_sources'])
    if hf['selected_source_freeze_pin']!=psf:
        raise RuntimeError('own host freeze exact selected complete math Source freeze')
    actual_source_pins=[]
    for name in ORDER:
        matches=[p for p in sf['files']if p['path']==str(SOURCE/name)]
        if len(matches)!=1:
            raise RuntimeError('exact unique complete Source path consumed by compiler')
        c.same_pin(SOURCE/name,matches[0]);actual_source_pins.append(matches[0])
    c.same_pin(sf['current_plan_pin']['path'],sf['current_plan_pin'])
    plan=json.loads(Path(sf['current_plan_pin']['path']).read_text())
    if plan['current_actual70_build_report_pin']!=pbase:
        raise RuntimeError('current math Source plan exact actual complete70 origin')
    if plan['current_case_spec_pin']['sha256']!='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16':
        raise RuntimeError('formal current case, no historical CASE transplant')
    fixed+=base['fixed_current_pins']+base['output_pins']+[pbase,psf,phf,hf['host_source'],sf['current_plan_pin']]
    fixed+=hf['dependencies']+sf['files']+sf['original_math_sources']
    fixed+=actual_source_pins
    by_path={}
    for row in fixed:
        if row['path']in by_path and row!=by_path[row['path']]:
            raise RuntimeError('conflicting full current input identity')
        by_path[row['path']]=row
    fixed=list(by_path.values());c.verify_rows(fixed)
    planned=commands(base,out)
    out.mkdir();(out/'build').mkdir();(out/'runtime').mkdir();(out/'observer-build').mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py')
    owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=binding['original_bounded']['sha256']:
        raise RuntimeError('original genuine bounded Source copy')
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'observer-build',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:
        raise RuntimeError('original executor class and resource binding')
    c.write(out/'Root_planned_build_binding.json',dict(fixed_current_pins=fixed,
      actual_commands=planned,ordered_complete70_inputs=[x for x in base['records'][-1]['command']if x.endswith(('.o','.a'))],
      observation_source_order=ORDER,requires_host_process_metadata_access=True,**c.scope()))
    failure=None;after_error=None;after=None;watch=[]
    try:
        for i,command in enumerate(planned):
            c.check_full_current(fixed,owned)
            runner.execute(out/'build','compile_'+str(i)if i<5 else'link_Dragon',command,600)
            watch.append(helper.check_watch(out,runner.records[-1]))
        c.check_full_current(fixed,owned);after=resources.check()
    except BaseException as error:failure=type(error).__name__+': '+str(error)
    finally:
        try:c.check_full_current(fixed,owned);after=resources.check()
        except BaseException as error:after_error=type(error).__name__+': '+str(error)
    outputs=[c.pin(p)for d in('build','runtime')for p in(out/d).iterdir()if p.is_file()]
    good=failure is None and after_error is None and len(runner.records)==6 and all(x['status']=='PASS'for x in runner.records)
    summary=out/'Root_actual_observation_build_summary.json'
    report=dict(
      schema='ACTUAL_CURRENT_FORMAL_FIVE_OBSERVATION_SOURCE_COMPLETE75_BUILD_ONLY_V1',
      status='ACTUAL_FIVE_COMPILE_COMPLETE75_LINK_CLOSED0_ONLY'if good else'ACTUAL_OBSERVATION_BUILD_FAILED_UNQUALIFIED',
      failure=failure,after_check_error=after_error,records=runner.records,
      fixed_current_pins=fixed,output_pins=outputs,actual_watchdog_checks=watch,
      current70_actual_origin=pbase,current_case_spec_pin=plan['current_case_spec_pin'],
      actual_prerequisite_receipts=gate_receipts,current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),
      all70_original_link_inputs_order_preserved=True,original_guard_class='OwnRSSSerialExecutor',
      original_guard_MRO_unchanged=True,
      resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      Dragon_linked=good,compiler_executed=bool(runner.records),material_job_executed=False,
      observation_context_produced=False,requires_host_process_metadata_access=True,final_report_bytes_in_original_resources=True,**c.scope())
    c.write(summary,report);sp=c.pin(summary)
    try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)
    except BaseException as error:
        report['status']='ACTUAL_OBSERVATION_BUILD_FAILED_UNQUALIFIED';report['failure']=type(error).__name__+': '+str(error)
        report['after_check_error']=report['failure'];report['wall_seconds']=time.monotonic()-start
        report['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        replace_owned_failure_summary(c,summary,sp,report);good=False
    if not good:raise RuntimeError(failure or after_error or'incomplete actual six-stage build')


if __name__=='__main__':main()

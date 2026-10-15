#!/usr/bin/env python3
"""New current-case observation runtime; compile/link only, no material job.

All complete69 inputs remain in order. Five original-math observation objects
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
SOURCE=REC/'current_formal_material_authority_source_v1'
COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'
ORDER=['AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','LIBMIX.observe.UNREADY.f',
       'LIBDEN.observe.UNREADY.f','TONDRV.context_observe.UNREADY.f','TONSPH.observe.UNREADY.f']
spec=importlib.util.spec_from_file_location('current_observation_original_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)


def commands(base,out):
    original=base['records'][0]['command']
    if original[1:10]!=c.FLAGS:
        raise RuntimeError('exact original nine compiler flags')
    includes=['-I'+str(out/'build')]+[x for x in original if x.startswith('-I')]
    result=[[original[0],*c.FLAGS,*includes,'-J'+str(out/'build'),'-c',str(SOURCE/name),
             '-o',str(out/'build'/(Path(name).stem+'.o'))]for name in ORDER]
    link=list(base['records'][-1]['command'])
    old=[x for x in link if x.endswith(('.o','.a'))]
    if len(old)!=69 or sum(x.endswith('.a')for x in old)!=4 or link[-2]!='-o':
        raise RuntimeError('complete69 actual ordered link with four archives')
    if any(Path(x).stem in {Path(n).stem for n in ORDER}for x in old if x.endswith('.o')):
        raise RuntimeError('new observation objects cannot alias old inputs')
    at=next(i for i,x in enumerate(link)if x.endswith('.a'))
    added=[str(out/'build'/(Path(n).stem+'.o'))for n in ORDER]
    link[at:at]=added;link[-1]=str(out/'runtime/Dragon')
    actual=[x for x in link if x.endswith(('.o','.a'))]
    if len(actual)!=74 or [x for x in actual if x not in added]!=old:
        raise RuntimeError('all69 original inputs and order must remain')
    result.append(link)
    return result


def main():
    parser=argparse.ArgumentParser()
    for prefix in ['current69','source-freeze','host-freeze']:
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
    if hf['schema']!='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_ONLY_FREEZE_V1' or \
       hf['compiler_executed']is not False or hf['transport_executed']is not False:
        raise RuntimeError('external actual Source-only host freeze')
    if hf['host_source']['path']!=str(Path(__file__).absolute()):
        raise RuntimeError('own complete host Source identity')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,resources,before=c.initialize(out,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('initial history96 reserves fresh2/cold/meta')
    base,pbase=load('current69')
    if base['schema']!='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1'or \
       base['status']!='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY'or \
       base['Dragon_linked']is not True or base['failure']is not None or base['after_check_error']is not None:
        raise RuntimeError('explicit actual complete69 successful origin')
    c.closed_report(base,helper,Path(pbase['path']).parent,10)
    c.verify_rows(base['fixed_current_pins']);c.verify_rows(base['output_pins'])
    if hf['selected_actual69_report_pin']!=pbase:
        raise RuntimeError('own host freeze exact selected actual complete69 report')
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
    if plan['current_actual69_build_report_pin']!=pbase:
        raise RuntimeError('current math Source plan exact actual complete69 origin')
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
      actual_commands=planned,ordered_complete69_inputs=[x for x in base['records'][-1]['command']if x.endswith(('.o','.a'))],
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
    c.write(out/'Root_actual_observation_build_summary.json',dict(
      schema='ACTUAL_CURRENT_FORMAL_FIVE_OBSERVATION_SOURCE_COMPLETE74_BUILD_ONLY_V1',
      status='ACTUAL_FIVE_COMPILE_COMPLETE74_LINK_CLOSED0_ONLY'if good else'ACTUAL_OBSERVATION_BUILD_FAILED_UNQUALIFIED',
      failure=failure,after_check_error=after_error,records=runner.records,
      fixed_current_pins=fixed,output_pins=outputs,actual_watchdog_checks=watch,
      current69_actual_origin=pbase,current_case_spec_pin=plan['current_case_spec_pin'],
      all69_original_link_inputs_order_preserved=True,original_guard_class='OwnRSSSerialExecutor',
      original_guard_MRO_unchanged=True,
      resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      Dragon_linked=good,compiler_executed=bool(runner.records),material_job_executed=False,
      observation_context_produced=False,requires_host_process_metadata_access=True,**c.scope()))
    if not good:raise RuntimeError(failure or after_error or'incomplete actual six-stage build')


if __name__=='__main__':main()

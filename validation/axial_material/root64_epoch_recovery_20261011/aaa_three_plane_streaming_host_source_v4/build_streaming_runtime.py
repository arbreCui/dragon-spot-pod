#!/usr/bin/env python3
"""Build-only new aliases alongside every unchanged old complete61 object.

No transport or new control/physics qualification. Mandatory external complete61,
original current17 and complete new Fortran Source freezes have full EOF/7ID pins.
The original supervisor class, flags, resource roots and all limits are reused.
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
COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'
spec=importlib.util.spec_from_file_location('streaming_build_original_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
SOURCE=REC/'aaa_three_plane_streaming_source_v2'
OUT=c.ART/'axial-material-new-AAA3-streaming-aliases-build-only-20261012-v4'
ORDER=['SPOR64_XSM_STORE64.f90','SPOR64_XSM_RB64.f90','SPOR64_B2IX.f90',
       'SPOR64_BOOT_PROJECTX64.f90','APACKX64.f90','BPROJX64.f90',
       'SPOBOOX64.f90','SPOBVX64.f90','KDRDRV.F']

def load_external(args,prefix):
    return c.load_json_exact(getattr(args,prefix+'_summary'),
                            getattr(args,prefix+'_sha256'),
                            getattr(args,prefix+'_seven_id'))

def commands(base,out):
    original=base['records'][0]['command']
    if original[1:10]!=c.FLAGS:
        raise RuntimeError('exact original nine compiler flags required')
    includes=[x for x in original if x.startswith('-I')]
    includes=['-I'+str(out/'build')]+includes
    compiler=original[0]
    result=[]
    for name in ORDER:
        result.append([compiler,*c.FLAGS,*includes,'-J'+str(out/'build'),
                       '-c',str(SOURCE/name),'-o',str(out/'build'/(Path(name).stem+'.o'))])
    link=list(base['records'][-1]['command'])
    old_link_inputs=[x for x in link if x.endswith(('.o','.a'))]
    if len(old_link_inputs)!=61 or sum(x.endswith('.o')for x in old_link_inputs)!=57 or sum(x.endswith('.a')for x in old_link_inputs)!=4:
        raise RuntimeError('actual original57 objects plus4 archives required')
    old=[i for i,x in enumerate(link)if Path(x).name=='KDRDRV.o']
    if len(old)!=1 or link[-2]!='-o':raise RuntimeError('exact complete61 link structure')
    link[old[0]]=str(out/'build/KDRDRV.o')
    # Every old math/storage object is retained. Distinct new module aliases
    # cannot substitute an old original module or its symbol.
    link[-2:]=[str(out/'build'/(Path(n).stem+'.o'))for n in ORDER[:-1]]+['-o',str(out/'runtime/Dragon')]
    expected_inputs=[str(out/'build/KDRDRV.o')if Path(x).name=='KDRDRV.o'else x for x in old_link_inputs]
    expected_inputs+=[str(out/'build'/(Path(n).stem+'.o'))for n in ORDER[:-1]]
    actual_inputs=[x for x in link if x.endswith(('.o','.a'))]
    if actual_inputs!=expected_inputs or len(actual_inputs)!=69:
        raise RuntimeError('exact complete69 input count and original61 plus8 order required')
    result.append(link)
    return result

def main():
    parser=argparse.ArgumentParser()
    for prefix in ['current61','seventeen','source-freeze','host-freeze']:
        for suffix in ['summary','sha256','seven-id']:
            parser.add_argument('--'+prefix+'-'+suffix,required=True)
    args=parser.parse_args();start=time.monotonic()
    hf,phf=load_external(args,'host_freeze')
    if hf['schema']!='COMPLETE_AAA3_NEW_ALIAS_BUILD_HOST_SOURCE_ONLY_FREEZE_V4' or \
       hf['compiler_executed'] is not False or hf['transport_executed'] is not False:
        raise RuntimeError('complete external exact own Host Source freeze required')
    if Path(hf['host_source']['path']).resolve()!=Path(__file__).resolve():
        raise RuntimeError('independent Host freeze must bind this exact file')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,resources,before=c.initialize(OUT,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('initial history96GiB must reserve fullfresh2GiB plus originalcold and metadata')
    fixed+=[phf,hf['host_source']]+hf['dependencies']
    base,pbase=load_external(args,'current61')
    if base['schema']!='ACTUAL_COMPLETE_NATIVE_A23_FIVE_SOURCE_COMPLETE61_BUILD_ONLY_V1' or \
       base['status']!='ACTUAL_A23_FIVE_COMPILE_AND_COMPLETE61_DRAGON_LINK_CLOSED0_ONLY' or \
       base['failure'] is not None or base['after_check_error'] is not None or \
       base['Dragon_linked'] is not True or len(base['records'])!=6:
        raise RuntimeError('complete actual six-stage current61 build required')
    c.closed_report(base,helper,Path(pbase['path']).parent,6)
    c.verify_rows(base['fixed_current_pins']);c.verify_rows(base['output_pins'])
    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)
    sf,psf=load_external(args,'source_freeze')
    if sf['schema']!='COMPLETE_NEW_FORTRAN_STORAGE_SOURCE_FROZEN_V1' or \
       sf['compiler_executed'] is not False or sf['transport_executed'] is not False:
        raise RuntimeError('new complete Fortran Source-only freeze required')
    c.verify_rows(sf['files']);c.same_pin(sf['formal_and_actual_input_plan']['path'],sf['formal_and_actual_input_plan'])
    if {Path(x['path']).name for x in sf['files']}!=set(ORDER):
        raise RuntimeError('complete exact nine new Source files')
    for row in sf['original_sources_still_unchanged']:
        actual=c.pin(row['path'])
        if actual['sha256']!=row['sha256'] or actual['size_bytes']!=row['size_bytes']:
            raise RuntimeError('frozen predecessor Source changed')
    required=binding['seventeen_required_same_production_object_pins']
    link=commands(base,OUT)[-1]
    actual_table={x['path']:x for x in base['fixed_current_pins']}
    for row in required:
        c.same_pin(row['path'],row)
        if row['path'] not in link or actual_table.get(row['path'])!=row:
            raise RuntimeError('old nine genuine same objects must remain in new link')
    fixed+=base['fixed_current_pins']+base['output_pins']+[pbase,p17,psf,c.pin(COMMON)]+sf['files']+[sf['formal_and_actual_input_plan']]
    fixed+=seventeen['fixed_current_pins']+seventeen['output_pins']
    # Deduplicate complete pins without losing any independent path identity.
    unique={}
    for row in fixed:
        if row['path']in unique and unique[row['path']]!=row:
            raise RuntimeError('inconsistent input pins')
        unique[row['path']]=row
    fixed=list(unique.values());c.verify_rows(fixed)
    planned=commands(base,OUT)
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir()
    (OUT/'AAA3-build').mkdir()  # Original execute dumps its per-case stages here before launching.
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned=[c.pin(OUT/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=binding['original_bounded']['sha256']:
        raise RuntimeError('exact original bounded Source copy')
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'AAA3-build',resources)
    if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:
        raise RuntimeError('unchanged original executor binding')
    c.write(OUT/'Root_planned_build_binding.json',dict(
      fixed_current_pins=fixed,actual_commands=planned,original_nine_unchanged_objects=required,
      original_stage600_whole1800_SELFchild512MiB=True,**c.scope()))
    failure=None;after_error=None;watchdogs=[];after=None
    try:
        for i,command in enumerate(planned):
            c.check_full_current(fixed,owned)
            runner.execute(OUT/'build','compile_'+str(i)if i<9 else 'link_Dragon',command,600)
            watchdogs.append(helper.check_watch(OUT,runner.records[-1]))
        c.check_full_current(fixed,owned);after=resources.check()
    except BaseException as exc:
        failure=type(exc).__name__+': '+str(exc)
    finally:
        try:c.check_full_current(fixed,owned);after=resources.check()
        except BaseException as exc:after_error=type(exc).__name__+': '+str(exc)
    outputs=[c.pin(p)for directory in ['build','runtime']for p in (OUT/directory).iterdir()if p.is_file()]
    good=failure is None and after_error is None and len(runner.records)==10 and all(x['status']=='PASS'for x in runner.records)
    c.write(OUT/'Root_actual_build_only_summary.json',dict(
      schema='ACTUAL_AAA3_STREAMING_NINE_ALIAS_COMPLETE69_BUILD_ONLY_V1',
      status='ACTUAL_NINE_NEW_SOURCE_COMPILE_COMPLETE69_LINK_CLOSED0_ONLY'if good else 'ACTUAL_BUILD_FAILED_UNQUALIFIED',
      failure=failure,after_check_error=after_error,records=runner.records,
      fixed_current_pins=fixed,output_pins=outputs,owned_runtime_pins=owned,
      actual_watchdog_checks=watchdogs,old_nine_objects_identical_and_retained=True,
      original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
      Dragon_linked=good,transport_executed=False,new_entry_controls_executed=False,
      **c.scope()))
    if not good:raise RuntimeError(failure or after_error or 'actual incomplete build')

if __name__=='__main__':main()

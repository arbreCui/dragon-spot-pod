#!/usr/bin/env python3
"""Rerun the exact current17 Source/oracles with the one new production BOOTQ.

Old17 is independently admitted as an old-reader premise. Its PASS is never
inherited by the new reader. Extra genuine READ and model controls are separate.
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

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
COMMON=REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/guarded_warm_A_common.py'
COMMON_SHA='2298894dd9316cecece0762c03fa11f296aedda11475184bb54b6665f6eef961'
OUT=R/'validation/artifacts/axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v1'
HF_SCHEMA='COMPLETE_BQ64_COMPACT_EXPECTED_CONNECTED17_HOST_SOURCE_ONLY_FREEZE_V1'
REPORT_SCHEMA='ACTUAL_BQ64_COMPACT_EXPECTED_FRESH_CONNECTED17_COMPONENT_CONTROLS_V1'
PASS_STATUS='ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY'

def load_common():
    fields=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    before=fields(COMMON.lstat())
    if not stat.S_ISREG(before[2]):raise RuntimeError('regular exact Common Source')
    fd=os.open(COMMON,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if fields(os.fstat(fd))!=before:raise RuntimeError('Common opened7ID changed')
        with os.fdopen(fd,'rb')as stream:
            fd=None;sha=hashlib.file_digest(stream,'sha256').hexdigest()
            if fields(os.fstat(stream.fileno()))!=before:raise RuntimeError('Common EOF7ID changed')
    finally:
        if fd is not None:os.close(fd)
    if fields(COMMON.lstat())!=before or sha!=COMMON_SHA:raise RuntimeError('exact Common EOF/after7ID/SHA')
    spec=importlib.util.spec_from_file_location('compact_bq_connected17_original_common',COMMON)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    return c

def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent complete pins')
        table[row['path']]=row
    return list(table.values())

def rewrite_summary(c,path,previous,data):
    if previous['path']!=str(path)or previous['identity'][3]!=1:
        raise RuntimeError('only owning single-link summary can be rewritten')
    c.same_pin(path,previous)
    fd=os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd)
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=previous['identity']:
            raise RuntimeError('own summary opened7ID changed')
        with os.fdopen(fd,'w',encoding='utf-8')as stream:
            fd=None;stream.seek(0);stream.truncate(0)
            json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False)
            stream.write('\n');stream.flush();os.fsync(stream.fileno())
    finally:
        if fd is not None:os.close(fd)
    if c.identity(path)[:4]!=previous['identity'][:4]:raise RuntimeError('own summary physical role changed')

def make_commands(c,old_oracle,new_build,new_object):
    compile_cmd=list(old_oracle['planned_compile_command'])
    old_compile=list(compile_cmd)
    old_out=old_oracle['planned_output_root']
    new_obj=str(OUT/'build/test_ROOT64_full_connected17.o')
    new_exe=str(OUT/'build/full_connected17_unqualified')
    if compile_cmd[1:10]!=c.FLAGS or compile_cmd[-4:-2]!=['-c',old_oracle['source_pin']['path']]:
        raise RuntimeError('exact original full17 Source and compile flags')
    include_at=next(i for i,v in enumerate(compile_cmd)if v.startswith('-I'))
    compile_cmd.insert(include_at,'-I'+str(Path(new_object['path']).parent))
    compile_cmd=[('-J'+str(OUT/'build'))if v=='-J'+old_out+'/build'else v for v in compile_cmd]
    if compile_cmd[-2]!='-o':raise RuntimeError('original compile output role')
    old_test_obj=compile_cmd[-1];compile_cmd[-1]=new_obj
    old_link=list(old_oracle['planned_link_command'])
    old_inputs=old_link[3:-2]
    if len(old_inputs)!=14 or old_inputs[0]!=old_test_obj or len(set(old_inputs))!=14 or \
       sum(v.endswith('.o')for v in old_inputs)!=10 or sum(v.endswith('.a')for v in old_inputs)!=4:
        raise RuntimeError('original connected17 main plus9 production objects and4 archives')
    positions=[i for i,v in enumerate(old_inputs)if Path(v).name=='SPOR64_BOOTQ64.o']
    if positions!=[3]:raise RuntimeError('original connected17 BOOTQ exact input3')
    new_inputs=list(old_inputs);new_inputs[0]=new_obj;new_inputs[3]=new_object['path']
    if [i for i,(a,b)in enumerate(zip(old_inputs,new_inputs))if a!=b]!=[0,3] or \
       any(v not in new_build['actual_complete70_link_inputs']for v in new_inputs[1:]):
        raise RuntimeError('all9 exact current production core objects/four archives')
    link=[*old_link[:3],*new_inputs,'-o',new_exe]
    runs=[[new_exe,*cmd[1:]]for cmd in old_oracle['planned_run_commands']]
    if len(runs)!=18 or [cmd[1]for cmd in runs[:16]]!=old_oracle['original_case_names'][:16] or \
       [cmd[1:]for cmd in runs[16:]]!=[['coherent_source_tamper','prepare'],['coherent_source_tamper','rewrite']]:
        raise RuntimeError('all17 original exact names and18 phases')
    return [compile_cmd,link,*runs]

def main():
    p=argparse.ArgumentParser()
    for prefix in ('build70','original17','host-freeze'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    args=p.parse_args();start=time.monotonic();c=load_common()
    def load(prefix):
        return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    hf,phf=load('host_freeze')
    if hf['schema']!=HF_SCHEMA or hf['compiler_executed']is not False or hf['controls_executed']is not False or \
       hf['host_source']['path']!=str(Path(__file__).resolve()):raise RuntimeError('exact owning Source-only Host freeze')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    binding,fixed,support,helper,full,resources,before=c.initialize(OUT,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('original initial cold/meta/fullfresh2/history96 reserve')
    old17,pold17=c.admit17(args.original17_summary,args.original17_sha256,args.original17_seven_id,helper)
    if pold17!=hf['selected_original17_report_pin']:raise RuntimeError('exact old17 historical reader premise')
    build,pbuild=load('build70')
    if pbuild!=hf['selected_actual_new_build70_report_pin']or \
       build['schema']!='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'or \
       build['status']!='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
       build['Dragon_linked']is not True or build['final_report_resource_check_passed']is not True or \
       build['original69_other_inputs_identical_and_retained']is not True or \
       build['original_eight_unchanged_core_objects_identical_and_retained']is not True or \
       build['replacement_zero_based_complete70_input_index']!=40:
        raise RuntimeError('new exact single BOOTQ compile/ordered70 relink premise')
    c.closed_report(build,helper,Path(pbuild['path']).parent,2)
    hf_table={r['path']:r for r in unique(hf['dependencies'])}
    for report_field,selected_field in [('actual_host_Source_freeze_pin','selected_new_build_Host_freeze_pin'),
                                       ('actual_new_Source_freeze_pin','selected_new_Fortran_Source_freeze_pin')]:
        chosen=hf[selected_field]
        if build[report_field]!=chosen or chosen not in build['fixed_current_pins']or hf_table.get(chosen['path'])!=chosen:
            raise RuntimeError('exact new build Host/Fortran freezes in both owning fixed closures')
        c.same_pin(chosen['path'],chosen)
    new_objects=[r for r in build['output_pins']if Path(r['path']).name=='SPOR64_BOOTQ64.o']
    if len(new_objects)!=1:raise RuntimeError('one genuine new BOOTQ production object')
    new_object=new_objects[0]
    old9=binding['seventeen_required_same_production_object_pins']
    if build['original_nine_core_object_pins']!=old9 or len(old9)!=9 or \
       build['original_ordered70_input_pins'][40]!=old9[5]or build['actual_complete70_link_inputs'][40]!=new_object['path']:
        raise RuntimeError('one core6/complete70 slot40 replacement')
    oracle_pin=old17['actual_current_control_binding_pin']
    oracle,checked=c.read_bound_json_current(oracle_pin['path'],oracle_pin)
    if checked!=oracle_pin or oracle['source_pin']!=old17['actual_current_control_source_pin']or \
       oracle['source_pin']['sha256']!='1b782030e20d4a254052937fd37ff6ef0e145969604e6ef6d365957ea29a9af3':
        raise RuntimeError('actual current expected-three-planes factory/full17 Source')
    planned=make_commands(c,oracle,build,new_object)
    fixed=unique(fixed+[phf,hf['host_source'],pold17,pbuild,oracle_pin]+hf['dependencies']+
      old17['fixed_current_pins']+old17['output_pins']+build['fixed_current_pins']+build['output_pins'])
    c.verify_rows(fixed)
    del binding,build
    OUT.mkdir()
    for name in ('runtime','build','connected17'):(OUT/name).mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned=[c.pin(OUT/'runtime/run_bounded_dragon.py')]
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'connected17',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('original exact owning supervisor')
    c.write(OUT/'Root_actual_control_binding.json',dict(schema='EXACT_FRESH_COMPACT_BQ_CONNECTED17_COMMAND_ORACLES_V1',
      actual_commands=planned,actual_current_control_source_pin=oracle['source_pin'],original_oracle_pin=oracle_pin,
      declared_case_oracles=oracle['declared_case_oracles'],original_case_names=oracle['original_case_names'],
      genuine_production_new_BOOTQ_object_pin=new_object,old_core_object_pins=old9,
      fixed_current_pins=fixed,old_seventeen_PASS_inherited=False,**c.scope()))
    failure=None;failure_tb=None;secondary=[];after=None;watches=[];cases=[]
    baseline=None;final_coherent=None;baseline_manifest=None;refusal=None
    def check():
        c.check_full_current(fixed,owned);value=resources.check()
        if not 0<time.monotonic()-start<1800:raise RuntimeError('original whole1800 includes final publication')
        return value
    try:
        for index,command in enumerate(planned):
            check()
            if index==19:
                c.same_pin(OUT/'build/coherent_complete_context.xsm',baseline)
                c.same_pin(baseline_manifest['path'],baseline_manifest)
            runner.execute(OUT/'build','control_'+str(index),command,600)
            watches.append(helper.check_watch(OUT,runner.records[-1]))
            if index==0:
                owned.append(c.pin(OUT/'build/test_ROOT64_full_connected17.o'))
            if index==1:owned.append(c.pin(OUT/'build/full_connected17_unqualified'))
            if index>=2:
                rows=[json.loads(line)for line in (OUT/'build'/('control_'+str(index)+'.log')).read_text().splitlines()]
                if len(rows)!=2:raise RuntimeError('exact assertion and actual call status rows')
                assertion,counts=rows;name=command[1];phase=command[2]if len(command)==3 else 'single'
                if any(row.get('case')!=name or row.get('phase')!=phase for row in rows)or \
                   assertion.get('all_actual_assertions_completed')is not True or assertion.get('synthetic_fixture')is not True or \
                   any(assertion.get(k)is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
                    raise RuntimeError('current exact synthetic assertion scope/name/phase')
                declared=next(o for o in oracle['declared_case_oracles']if o['case']==name)
                for key,value in declared.items():
                    if key.startswith(('expected_actual_','expected_explicit_'))and counts.get(key[9:])!=value:
                        raise RuntimeError('original full17 actual call/status oracle: '+name+' '+key)
                cases.append(dict(case=name,phase=phase,assertions=assertion,actual_statuses_and_call_counts=counts))
            if index==18:
                baseline=c.pin(OUT/'build/coherent_complete_context.xsm')
                path=OUT/'Host_independent_coherent_baseline_full_EOF_SHA_7ID.json'
                c.write(path,dict(schema='INDEPENDENT_HOST_COHERENT_BASELINE_FULL_FILE_BINDING_V1',actual_before_pin=baseline))
                baseline_manifest=c.pin(path);owned.append(baseline_manifest)
            if index==19:
                final_coherent=c.pin(OUT/'build/coherent_complete_context.xsm')
                if final_coherent['sha256']==baseline['sha256']or final_coherent['identity']==baseline['identity']:
                    raise RuntimeError('actual coherent rewrite must change complete bytes/identity')
                try:
                    c.same_pin(OUT/'build/coherent_complete_context.xsm',baseline)
                except RuntimeError as refusal_error:
                    c.same_pin(OUT/'build/coherent_complete_context.xsm',final_coherent)
                    refusal=dict(actual_refused=True,Fortran_internal_refusal_claimed=False,before=baseline,after=final_coherent,
                      actual_original_Host_gate='same_pin',actual_refusal_error=repr(refusal_error))
                else:
                    raise RuntimeError('original owning immutable Host gate did not actually refuse coherent rewrite')
            after=check()
        if len(cases)!=18 or refusal is None:raise RuntimeError('all17/18phases and actual independent coherent refusal required')
    except BaseException as error:failure=error;failure_tb=error.__traceback__
    target=OUT/'Root_actual_connected17_summary.json';summary=None
    try:
        after=check();good=failure is None and len(runner.records)==20 and len(cases)==18 and refusal is not None
        summary=dict(schema=REPORT_SCHEMA,status=PASS_STATUS if good else 'FAILED_FRESH_CURRENT17_NO_RETRY',
          failure=None if failure is None else repr(failure),after_check_error=None,secondary_failures=secondary,
          records=runner.records,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],
          actual_watchdog_checks=watches,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
          resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
          wall_seconds=time.monotonic()-start,actual_cases=cases,actual_logical_control_count=17 if good else None,
          actual_run_phase_count=len(cases),all17_original_names_exercised=good,old_seventeen_PASS_inherited=False,
          original_current17_report_pin=pold17,original_current17_oracle_pin=oracle_pin,
          actual_current_control_source_pin=oracle['source_pin'],actual_host_Source_freeze_pin=phf,
          actual_new_build70_report_pin=pbuild,genuine_production_new_BOOTQ_object_pin=new_object,
          actual_independent_host_coherent_refusal=refusal,independent_coherent_baseline_manifest_pin=baseline_manifest,
          other_eight_core_objects_and_original_oracles_unchanged=True,
          new_private_model_controls_qualified=False,new_extra_public_READ_controls_qualified=False,
          production_reader_admitted=False,final_report_resource_check_passed=False,**c.scope())
        c.write(target,summary)
        summary['resources_after_including_summary_bytes']=check()
        summary['final_report_resource_check_passed']=True
        summary['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        summary['wall_seconds']=time.monotonic()-start
        rewrite_summary(c,target,c.pin(target),summary);check()
    except BaseException as error:
        if failure is None:failure=error;failure_tb=error.__traceback__
        else:secondary.append(dict(where='final_check_or_publication',error=repr(error)))
        try:
            if summary is not None and target.exists():
                summary.update(status='FAILED_FRESH_CURRENT17_NO_RETRY',failure=repr(failure),
                  final_report_resource_check_passed=False,secondary_failures=secondary)
                rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as late:
            try:os.write(2,('secondary failed report publication: '+repr(late)+'\n').encode())
            except BaseException:pass
    if failure is not None:raise failure.with_traceback(failure_tb)

if __name__=='__main__':main()

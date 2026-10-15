#!/usr/bin/env python3
"""Guarded model controls; Source-only until a genuine closed2 build is supplied."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

sys.dont_write_bytecode=True
R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
PLAN=HERE/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json'
OUT=R/'validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5'
KIND='model'
COMMON=REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py'
COMMON_SHA='a5b774a6b62e229f8f6360a284354e2f0af8ff3860602b061de376b2624fc040'
HF_SCHEMA='COMPLETE_BQ64_PRIVATE_GANLIB_MODEL_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'
SF_SCHEMA='COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'
REPORT_SCHEMA='ACTUAL_BQ64_PRIVATE_GANLIB_MODEL_GUARDED_CONTROL_REPORT_V1'
PASS_STATUS='ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY'
AUX_CAP=128*2**20
AUX_PENDING=8*2**20

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



def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:
            raise RuntimeError('inconsistent complete PF for same input path')
        table[row['path']]=row
    return list(table.values())


def safe_repr(error):
    try:return repr(error)
    except BaseException:return '<exception repr unavailable>'


class FirstFailure:
    def __init__(self):
        self.error=None;self.traceback=None;self.secondary=[]
    def capture(self,error,where):
        if self.error is None:
            self.error=error;self.traceback=error.__traceback__
        else:self.secondary.append(dict(where=where,error=safe_repr(error)))
    def reraise(self):
        if self.error is not None:raise self.error.with_traceback(self.traceback)


def direct_aux_inventory(root):
    total=0;count=0
    if root.exists():
        for directory,dirs,files in os.walk(root,followlinks=False):
            for name in dirs:
                mode=(Path(directory)/name).lstat().st_mode
                if not stat.S_ISDIR(mode):raise RuntimeError('owned control directory symlink/non-directory')
            for name in files:
                path=Path(directory)/name;s=path.lstat()
                if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:
                    raise RuntimeError('owned controls auxiliary ordinary single-link file required')
                total+=s.st_size;count+=1
    if total+AUX_PENDING>AUX_CAP:
        raise RuntimeError('original remaining runtime/context/log/meta storage planning bound128MiB')
    return dict(auxiliary_bytes=total,auxiliary_files=count,pending_bytes=AUX_PENDING,cap_bytes=AUX_CAP)


class ControlsResources:
    def __init__(self,base,root):self.base=base;self.root=root
    def check(self):
        result=self.base.check()
        # A direct separate OUT pass; no subtraction across different snapshots.
        result['control_direct_auxiliary']=direct_aux_inventory(self.root)
        return result


def log_rows(c,root,record):
    path=root/(record['label']+'.log')
    pf=c.pin(path)
    if pf['sha256']!=record['log_sha256']:raise RuntimeError('actual closed stage full log SHA')
    rows=[]
    with path.open('r',encoding='utf-8',errors='strict')as stream:
        for line in stream:
            if len(line)>65536:raise RuntimeError('control JSON/log line bound')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                value=json.loads(line)
                if isinstance(value,dict):rows.append(value)
    c.same_pin(path,pf)
    return rows,pf


def model_oracle(c,root,record,cwd):
    rows,log_pin=log_rows(c,root,record)
    matches=[row for row in rows if row.get('status')=='ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY']
    if len(matches)!=1:raise RuntimeError('one genuine private GANLIB model terminal JSON')
    actual=matches[0]
    if type(actual.get('assertions'))is not int or actual['assertions']!=36 or \
       any(actual.get(k)is not False for k in ('physics_qualified','reader_qualified','AAA_qualified')):
        raise RuntimeError('actual36 private model assertions and precise unqualified scope')
    models=[]
    for name in ('C64-EXP','C64-ACT'):
        p=cwd/name;row=c.pin(p)
        if row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2]):
            raise RuntimeError('retained actual model ordinary single-link file')
        models.append(row)
    if models[0]['size_bytes']!=948232 or models[0]['size_bytes']>32*2**20 or \
       models[1]['size_bytes']<=models[0]['size_bytes'] or models[1]['size_bytes']>32*2**20 or \
       models[0]['sha256']==models[1]['sha256']:
        raise RuntimeError('actual compact948232 and independent full-model physical bound')
    return dict(actual_model_assertions=actual['assertions'],actual_terminal=actual,
                actual_retained_model_file_pins=models,actual_log_pin=log_pin)


def public_oracle(c,root,record,declared):
    rows,log_pin=log_rows(c,root,record)
    matches=[row for row in rows if row.get('schema')=='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1']
    if len(matches)!=1:raise RuntimeError('one genuine public READ terminal JSON per phase')
    actual=matches[0]
    if(actual.get('case'),actual.get('phase'))!=(declared['case'],declared['phase'])or \
       actual.get('all_actual_assertions_completed')is not True or actual.get('synthetic_fixture')is not True or \
       any(actual.get(k)is not False for k in ('private_matcher_used_as_assertion_oracle',
        'physics_qualified','reader_qualified','AAA_qualified','ABA_admitted')):
        raise RuntimeError('actual exact public READ case/phase/assertions/scope')
    for key,value in declared.items():
        if key.startswith('expected_'):
            observed=actual.get(key[len('expected_'):])
            if type(observed)is not int or observed!=value:
                raise RuntimeError('actual genuine public READ status/call-count '+key)
    return dict(case=actual['case'],phase=actual['phase'],actual_terminal=actual,actual_log_pin=log_pin)


def make_commands(c,base,plan,source):
    compiler=plan['original_compiler_pin']['path']
    actual_compile=base['records'][0]['command'];actual_link=base['records'][1]['command']
    old=plan['original_ordered70_paths'];new=base['actual_complete70_link_inputs']
    expected_new=list(old);expected_new[40]=plan['new_build_expected_BOOTQ_object_path']
    expected_compile=[compiler,*c.FLAGS,*plan['new_build_compile_include_arguments'],
      '-J'+plan['new_build_expected_build_directory'],'-c',plan['production_Source_pin']['path'],
      '-o',plan['new_build_expected_BOOTQ_object_path']]
    if len(new)!=70 or new!=expected_new or actual_link!=[compiler,'-O2','-ffp-contract=off',*new,'-o',plan['new_build_expected_Dragon_path']]or \
       actual_compile!=expected_compile or c.FLAGS!=plan['original_compile_flags']or \
       [x for x in actual_compile if x.startswith('-I')]!=plan['new_build_compile_include_arguments']:
        raise RuntimeError('exact genuine new one-object70 build flags/order/compile/link commands')
    obj=str(OUT/'build/control.o');exe=str(OUT/'runtime/control_unqualified')
    includes=['-I'+str(OUT/'build'),'-I'+plan['new_build_expected_build_directory'],*plan['original_compile_include_arguments']]
    compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(OUT/'build'),'-c',source['path'],'-o',obj]
    libraries=plan['original_four_archive_paths']
    core=[]
    if KIND=='public':
        core=list(plan['original_nine_core_paths']);core[5]=new[40]
        if len(core)!=9 or core[5]!=new[40]or len(set(core))!=9:
            raise RuntimeError('exact new9 core6 with unchanged other8')
    link_cmd=[compiler,'-O2','-ffp-contract=off',obj,*core,*libraries,'-o',exe]
    return compile_cmd,link_cmd,exe,core


def main():
    parser=argparse.ArgumentParser()
    for prefix in ('new-build70','source-freeze','host-freeze'):
        for suffix in ('summary','sha256','seven-id'):parser.add_argument('--'+prefix+'-'+suffix,required=True)
    args=parser.parse_args();start=time.monotonic();c=load_common()
    def load(prefix):
        prefix=prefix.replace('-','_')
        return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    hf,phf=load('host-freeze')
    if hf.get('schema')!=HF_SCHEMA or hf.get('compiler_executed')is not False or hf.get('numerical_executed')is not False or \
       Path(hf['host_source']['path']).resolve()!=Path(__file__).resolve():
        raise RuntimeError('exact Source-only owning control Host complete freeze')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies'])
    hf_table={row['path']:row for row in unique(hf['dependencies'])}
    plan_pin=hf['control_host_plan_pin']
    if plan_pin['path']!=str(PLAN)or hf_table.get(str(PLAN))!=plan_pin:
        raise RuntimeError('exact owning control Host plan')
    plan,checked=c.read_bound_json_current(PLAN,plan_pin)
    if checked!=plan_pin or plan['kind']!=KIND or plan['planned_output_root']!=str(OUT)or \
       plan['source_only']is not True or plan['compiler_executed']is not False or plan['numerical_executed']is not False or \
       any(plan[k]is not None for k in ('future_actual_new_build70_report_pin','future_actual_control_object_pin',
        'future_actual_control_executable_pin','future_actual_control_report_pin')):
        raise RuntimeError('Source-only plan has no future actual pins')
    selected_build_hf=hf.get('selected_new_build_Host_freeze_pin')
    selected_fortran_sf=hf.get('selected_new_Fortran_Source_freeze_pin')
    for selected,key in ((selected_build_hf,'selected_new_build_Host_freeze_pin'),
                         (selected_fortran_sf,'selected_new_Fortran_Source_freeze_pin')):
        if selected!=plan.get(key)or not isinstance(selected,dict)or hf_table.get(selected['path'])!=selected:
            raise RuntimeError('own Host freeze selects exact newbuild HostHF and FortranSF dependencies')
    c.verify_rows([selected_build_hf,selected_fortran_sf])
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    caps=plan['original_caps']
    if any(binding[k]!=v for k,v in caps.items())or caps!=dict(original_stage_wall_cap_seconds=600,
      whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,
      retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,
      filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748):
        raise RuntimeError('unchanged original one-thread600/1800/512/fresh2/history96/free8/cold caps')
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('initial fullfresh2 cold metadata history96 reservation')
    sf,psf=load('source-freeze')
    if psf!=plan['selected_control_Source_freeze_pin']or hf_table.get(psf['path'])!=psf or \
       sf.get('schema')!=SF_SCHEMA or sf.get('source_only')is not True or \
       sf.get('compiled')is not False or sf.get('numerical_executed')is not False:
        raise RuntimeError('exact complete control Source-only freeze')
    sf_rows=unique(sf['files']+sf['original_source_pins']+sf.get('dependencies',[]))
    c.verify_rows(sf_rows)
    source=plan['control_Source_pin']
    if source not in sf['files']:raise RuntimeError('exact control Source in selected SF')
    production_sf=psf if KIND=='model'else sf['candidate_fortran_source_freeze_pin']
    if production_sf!=selected_fortran_sf:raise RuntimeError('control SF and ownHF select identical production FortranSF')
    base,pbase=load('new-build70')
    if pbase['path']!=plan['new_build_expected_report_path']or base.get('schema')!='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'or \
       base.get('status')!='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
       base.get('Dragon_linked')is not True or base.get('final_report_resource_check_passed')is not True or \
       base.get('actual_new_Source_freeze_pin')!=production_sf or base.get('actual_new_Source_pin')!=plan['production_Source_pin']or \
       base.get('actual_host_Source_freeze_pin')!=selected_build_hf or \
       base.get('original_caps')!=caps or \
       base.get('replacement_zero_based_complete70_input_index')!=40 or \
       any(base.get(k)is not True for k in ('original69_other_inputs_identical_and_retained',
        'original_four_archives_identical_and_retained','original_eight_unchanged_core_objects_identical_and_retained'))or \
       any(base.get(k)is not False for k in ('transport_executed','new_entry_controls_executed','new_reader_control_qualification')):
        raise RuntimeError('genuine selected new closed2 one-object70 build premise')
    base_fixed_table={row['path']:row for row in unique(base['fixed_current_pins'])}
    if any(base_fixed_table.get(row['path'])!=row for row in (selected_build_hf,selected_fortran_sf)):
        raise RuntimeError('newbuild itself fixed both exact owning HostHF and FortranSF')
    c.closed_report(base,helper,Path(pbase['path']).parent,2)
    compile_cmd,link_cmd,exe,core=make_commands(c,base,plan,source)
    new_object=c.pin(plan['new_build_expected_BOOTQ_object_path'])
    if new_object not in base['output_pins']:raise RuntimeError('new BOOTQ genuine actual build output PF')
    for row in plan['original_nine_core_pins'][:5]+plan['original_nine_core_pins'][6:]:
        c.same_pin(row['path'],row)
    fixed=unique(fixed+[phf,hf['host_source'],plan_pin,psf,pbase,new_object]+hf['dependencies']+sf_rows+
                 base['fixed_current_pins']+base['output_pins'])
    c.verify_rows(fixed)
    resources=ControlsResources(base_resources,OUT)
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'build').mkdir()
    (OUT/('compact-'+KIND+'-controls')).mkdir()
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py')
    owned=[c.pin(OUT/'runtime/run_bounded_dragon.py')]
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'compact-'+KIND+'-controls',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or \
       Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':
        raise RuntimeError('original OwnRSS/MRO/own supervisor binding')
    first=FirstFailure();watches=[];actual=[];stale=[];after=None;verified=False
    def check():
        c.check_full_current(fixed,owned);result=resources.check()
        if not 0<time.monotonic()-start<1800:raise RuntimeError('original whole1800 includes admission/report closeout')
        return result
    def run(cwd,label,command):
        nonlocal after
        check();runner.execute(cwd,label,command,600)
        watches.append(helper.check_watch(OUT,runner.records[-1]));after=check()
        return runner.records[-1]
    try:
        c.write(OUT/'Root_planned_control_binding.json',dict(fixed_current_pins=fixed,actual_compile_command=compile_cmd,
          actual_link_command=link_cmd,actual_new_build70_report_pin=pbase,actual_new_BOOTQ_object_pin=new_object,
          control_Source_pin=source,actual_Source_freeze_pin=psf,planned_run_phases=plan['planned_run_phases'],
          original_caps=caps,original_aux_cap_bytes=AUX_CAP,original_pending_metadata_bytes=AUX_PENDING,**c.scope()))
        run(OUT/'build','compile_control',compile_cmd)
        owned.append(c.pin(OUT/'build/control.o'));owned.extend(c.pin(p)for p in sorted((OUT/'build').glob('*.mod')))
        run(OUT/'build','link_control',link_cmd);owned.append(c.pin(exe))
        if KIND=='model':
            cwd=OUT/'model';cwd.mkdir();record=run(cwd,'run_model',[exe])
            actual.append(model_oracle(c,OUT,record,cwd))
            owned.extend(actual[-1]['actual_retained_model_file_pins'])
        else:
            case_dirs={};manifests={}
            for decl in plan['planned_run_phases']:
                name,phase=decl['case'],decl['phase']
                cwd=OUT/name
                if name not in case_dirs:cwd.mkdir();case_dirs[name]=cwd
                is_stale=phase in ('prepare','read')
                selected='BQ64-SRC-ST'if name=='public_read_stale_BQ_SRC'else'BQ64-MAC-ST'
                other='BQ64-MAC-ST'if selected=='BQ64-SRC-ST'else'BQ64-SRC-ST'
                if is_stale and phase=='read':
                    state=manifests[name]
                    c.verify_rows([state['manifest_pin'],state['bundle_pin'],state['stale_pin']])
                    value,pf=c.read_bound_json_current(state['manifest_pin']['path'],state['manifest_pin'])
                    if value['actual_bundle_pin']!=state['bundle_pin']or value['actual_stale_pin']!=state['stale_pin']or \
                      (cwd/other).exists()or(cwd/other).is_symlink():
                        raise RuntimeError('exact fsynced actual stale baseline before genuine public READ')
                command=[exe,name]+([phase]if is_stale else[])
                record=run(cwd,'control_'+phase,command)
                actual.append(public_oracle(c,OUT,record,decl))
                if is_stale and phase=='prepare':
                    bundle_pin=c.pin(cwd/'coherent_complete_context.xsm');stale_pin=c.pin(cwd/selected)
                    if bundle_pin['identity'][3]!=1 or stale_pin['identity'][3]!=1 or(cwd/other).exists()or(cwd/other).is_symlink():
                        raise RuntimeError('closed prepare ordinary single-link files and other stage absent')
                    mf=cwd/'Host_independent_stale_before_full_EOF_SHA_all7.json'
                    c.write(mf,dict(schema='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1',case=name,
                      actual_bundle_pin=bundle_pin,actual_stale_pin=stale_pin,other_BQ_absent=True,
                      genuine_prepare_child_closed0=True,actual_prepare_record=record))
                    state=dict(case=name,manifest_pin=c.pin(mf),bundle_pin=bundle_pin,stale_pin=stale_pin)
                    manifests[name]=state;owned.extend([state['manifest_pin'],bundle_pin,stale_pin])
                    c.verify_rows([state['manifest_pin'],bundle_pin,stale_pin])
                elif is_stale:
                    state=manifests[name]
                    c.verify_rows([state['manifest_pin'],state['bundle_pin'],state['stale_pin']])
                    if(cwd/other).exists()or(cwd/other).is_symlink():raise RuntimeError('other BQ stage created during stale READ')
                    stale.append(dict(case=name,actual_before_manifest_pin=state['manifest_pin'],
                      actual_bundle_before_pin=state['bundle_pin'],actual_bundle_after_pin=c.pin(state['bundle_pin']['path']),
                      actual_stale_before_pin=state['stale_pin'],actual_stale_after_pin=c.pin(state['stale_pin']['path']),
                      actual_two_files_full_EOF_SHA_all7_unchanged=True,actual_other_BQ_absent=True,
                      genuine_read_child_closed0=True,actual_read_record=record))
        expected_count=3 if KIND=='model'else 11
        if len(runner.records)!=expected_count or any(row['status']!='PASS'for row in runner.records):
            raise RuntimeError('complete exact guarded control stage count')
        if KIND=='public'and(len(actual)!=9 or len(stale)!=2):raise RuntimeError('seven public controls/nine phases/two independent stale manifests')
        check();verified=True
    except BaseException as error:first.capture(error,'execute_or_oracle')
    try:after=check()
    except BaseException as error:first.capture(error,'after_check')
    good=first.error is None and verified
    target=OUT/'Root_actual_control_summary.json';summary=None
    try:
        summary=dict(schema=REPORT_SCHEMA,status=PASS_STATUS if good else'ACTUAL_CONTROL_FAILED_UNQUALIFIED',
          failure=None if first.error is None else safe_repr(first.error),after_check_error=None if not first.secondary else first.secondary[0]['error'],
          secondary_failures=first.secondary,records=runner.records,fixed_current_pins=fixed,
          output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],owned_runtime_pins=owned,
          actual_watchdog_checks=watches,actual_control_results=actual,actual_stale_host_evidence=stale,
          actual_new_build70_report_pin=pbase,actual_new_BOOTQ_object_pin=new_object,
          actual_control_Source_pin=source,actual_Source_freeze_pin=psf,actual_host_Source_freeze_pin=phf,
          actual_compile_command=compile_cmd,actual_link_command=link_cmd,actual_link_core_paths=core,
          logical_control_count=1 if KIND=='model'else 7,actual_run_phase_count=1 if KIND=='model'else 9,
          private_model_does_not_independently_qualify_public_reader=True,old17_PASS_inherited=False,
          actual_model_controls_passed=good if KIND=='model'else False,
          actual_seven_genuine_public_READ_controls_passed=good if KIND=='public'else False,
          original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=caps,
          original_aux_cap_bytes=AUX_CAP,original_pending_metadata_bytes=AUX_PENDING,
          resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
          wall_seconds=time.monotonic()-start,terminal_receipt_required_for_qualification=True,
          final_report_resource_check_passed=False,compiler_executed=True,synthetic_protocol_fixture_only=True,
          physics_qualified=False,new_reader_qualified=False,**c.scope())
        c.write(target,summary)
        summary['resources_after_including_summary_bytes']=check()
        summary['final_report_resource_check_passed']=True
        summary['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        summary['wall_seconds']=time.monotonic()-start
        rewrite_summary(c,target,c.pin(target),summary)
        check()
    except BaseException as error:
        first.capture(error,'publication')
        try:
            if summary is not None:
                summary.update(status='ACTUAL_CONTROL_FAILED_UNQUALIFIED',failure=safe_repr(first.error),
                  secondary_failures=first.secondary,final_report_resource_check_passed=False,
                  actual_model_controls_passed=False,actual_seven_genuine_public_READ_controls_passed=False)
                if target.exists():rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as late:
            first.capture(late,'failed_report_publication')
            try:os.write(2,('secondary publication: '+safe_repr(late)+'\n').encode())
            except BaseException:pass
    first.reraise()
    if not good:raise RuntimeError('incomplete actual guarded controls')


if __name__=='__main__':main()

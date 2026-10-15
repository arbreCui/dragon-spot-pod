#!/usr/bin/env python3
"""Original OwnRSS single-child host for eleven saved GENDF evidence inputs.

Only Root executes after true AAA3/BOOT, saved full370 diagnostic and the first
actual current A material capture. Those future report hashes are not predicted
here. The actual capture report is a required explicit full-file argument.
Original600/1800/SELF+child512/fresh2/history96/cold/free8 and no-retry remain.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
COMMON=REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/guarded_warm_A_common.py'
spec=importlib.util.spec_from_file_location('current_gendf_original_guard',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
  history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
  free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(DRAGR_packed_raw_words_replayed=False,current_SPH_MASK_context_applied=False,
  three_current_raw_MACRO_comparisons_performed=False,complete_reaction_authority_qualified=False,
  physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,
  scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
CASE='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'


def main():
    p=argparse.ArgumentParser()
    for prefix in('source-freeze','host-freeze','material-observation-report'):
        for suffix in('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    p.add_argument('--output-dir',required=True);args=p.parse_args();start=time.monotonic()
    def load(prefix):return c.load_json_exact(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    sf,psf=load('source_freeze');hf,phf=load('host_freeze');observed,pobserved=load('material_observation_report')
    if sf['schema']!='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4'or sf['candidate_executed']is not False or \
       hf['schema']!='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4'or hf['candidate_executed']is not False or \
       hf['selected_source_freeze_pin']!=psf or hf['host_source']['path']!=str(Path(__file__).absolute()):
        raise RuntimeError('complete exact immutable executing Source/host package')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies']);c.verify_rows(sf['complete_source_file_pins'])
    out=Path(args.output_dir);childout=out.with_name(out.name+'-evidence')
    if not out.is_absolute()or out.parent!=c.ART or os.path.lexists(out)or os.path.lexists(childout):
        raise RuntimeError('two literal fresh sibling host/child outputs, once')
    binding,fixed,support,helper,full,oldresources,before=c.initialize(out,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('original full initial fresh2/cold/meta/history96 reservation')
    if observed['schema']!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or \
       observed['status']!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'or \
       observed['actual_full_A_observation_executed']is not True or observed['actual_B_observation_executed']is not False or \
       observed['three_recaptured_plane_histories_claimed']is not False or observed['current_case_spec_pin']['sha256']!=CASE:
        raise RuntimeError('actual first same-physical current A capture required, no Source-only report or retag')
    c.closed_report(observed,helper,Path(pobserved['path']).parent,1)
    release=observed['actual_closed_owned_library_copy_release_pin'];c.same_pin(release['path'],release)
    released=json.loads(Path(release['path']).read_text())
    if released['schema']!='ACTUAL_CLOSED_PRIVATE_MATERIAL_INPUT_COPY_RELEASE_V1'or \
       released['total_owned_bytes_released']!=979740136 or released['all_owned_copy_paths_absent_after_release']is not True or \
       released['all_results_contexts_native_observations_retained']is not True:
        raise RuntimeError('actual closed shared-copy lifecycle required')
    for row in released['owned_copy_pins_before_release']:
        if os.path.lexists(row['path']):raise RuntimeError('historical closed consumed copy is not a current live input')
    planpin=sf['selected_genDF_source_plan_pin'];c.same_pin(planpin['path'],planpin)
    plan=json.loads(Path(planpin['path']).read_text());casepin=observed['current_case_spec_pin']
    if plan['schema']!='READONLY_CURRENT_NONZERO_NX_GENDF_SOURCE_PLAN_V1'or plan['current_formal_case_sha256']!=CASE or \
       plan['extractor_executed']is not False or len(plan['inputs'])!=11 or sf['original_caps']!=CAPS or hf['original_caps']!=CAPS:
        raise RuntimeError('complete current eleven saved-reaction plan and unchanged original caps')
    if sf['original_immutable_compiler_role_pin']!=binding['compiler']:
        raise RuntimeError('single exact original immutable compiler role, no generic hardlink relaxation')
    artifact_roots=[str(out),str(childout),str(Path(pobserved['path']).parent)]+sf['cumulative_artifact_root_paths'][3:]
    source_root_paths=[str(BASE),str(Path(planpin['path']).parent)]
    roots=artifact_roots[:3]+source_root_paths+artifact_roots[3:]
    if artifact_roots!=sf['cumulative_artifact_root_paths'] or source_root_paths!=sf['cumulative_Source_root_paths'] or len(artifact_roots)!=8 or len(source_root_paths)!=2 or len(set(roots))!=10 or any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b):
        raise RuntimeError('ten disjoint cumulative original2GiB roles: original five plus capture/extract/aggregate')
    if observed['completion_only_existing_closed_stage']is not True or observed['Dragon_or_compiler_or_material_child_launched_by_continuation']is not False or str(Path(observed['actual_prior_A_cwd']).parent)!=artifact_roots[3] or Path(observed['original_failed_phase_pin']['path']).parent!=Path(artifact_roots[3]):
        raise RuntimeError('exact retained captured physical owner and distinct completion phase')
    if sf['selected_actual_aggregation_report_pin']is None or sf['selected_actual_aggregation_post_pin']is None:
        raise RuntimeError('actual closed aggregation and independent post required; unknown future not executable')
    for actual_pin in(sf['selected_actual_aggregation_report_pin'],sf['selected_actual_aggregation_post_pin']):c.same_pin(actual_pin['path'],actual_pin)
    parent=sys.modules[full.OwnRSSSerialExecutor.__bases__[0].__module__]
    if Path(parent.__file__).resolve()!=support.PARENT:raise RuntimeError('genuine original DiskResources Source')
    joined=parent.DiskResources(c.ART,artifact_roots,8*2**30,2*2**30)
    source_roots=[Path(value)for value in source_root_paths]
    def source_tree_bytes():
        total=0;count=0
        for root in source_roots:
            if any(p.is_symlink()for p in(root,*root.parents))or not root.is_dir():
                raise RuntimeError('complete ordinary Source roles, no ancestor aliases')
            stack=[root]
            while stack:
                directory=stack.pop()
                fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
                try:
                    with os.scandir(fd)as entries:
                        for entry in entries:
                            item=entry.stat(follow_symlinks=False)
                            if stat.S_ISDIR(item.st_mode):stack.append(directory/entry.name)
                            elif stat.S_ISREG(item.st_mode):total+=item.st_size;count+=1
                            else:raise RuntimeError('complete joint Source trees may not contain aliases/special files')
                finally:os.close(fd)
        return total,count
    def host_open_unlinked_bytes():
        table={}
        for value in os.listdir('/dev/fd'):
            try:item=os.fstat(int(value))
            except(ValueError,OSError):continue
            if stat.S_ISREG(item.st_mode)and item.st_nlink==0:table[item.st_dev,item.st_ino]=item.st_size
        return sum(table.values())
    class Resources:
        def check(self):
            def host_guard():
                peak=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
                if sys.platform!='darwin':peak*=1024
                if peak>=512*2**20 or time.monotonic()-start>=1800:
                    raise RuntimeError('original owning host SELF512/whole1800')
                return peak
            host_guard();history=oldresources.check();fresh=joined.check()
            source_bytes,source_files=source_tree_bytes();unlinked=host_open_unlinked_bytes()
            joint=fresh['artifact_bytes']+source_bytes+unlinked
            if joint>=2*2**30:raise RuntimeError('original joint fresh2GiB: eight cumulative ART roles plus two full Source trees and host open-unlinked')
            peak=host_guard()
            return dict(original_history_cold_free=history,complete_joint_fresh=fresh,
              complete_Source_roots=[str(p)for p in source_roots],complete_Source_bytes=source_bytes,
              complete_Source_regular_files=source_files,host_open_unlinked_bytes=unlinked,
              complete_ten_role_joint_bytes=joint,host_SELF_peak_bytes=peak,
              host_whole_elapsed_seconds=time.monotonic()-start)
    resources=Resources();resources.check()
    fixed+=[psf,phf,pobserved,planpin,casepin,release,hf['host_source']]+hf['dependencies']+sf['complete_source_file_pins']
    fixed+=observed['fixed_current_pins']+observed['output_pins']+sf['static_input_pins']
    fixed+=[v for row in plan['inputs']for key,v in row.items()if key.endswith('_pin')]
    unique={}
    for row in fixed:
        if row['path']in unique and unique[row['path']]!=row:raise RuntimeError('ambiguous current full-file identity')
        unique[row['path']]=row
    fixed=list(unique.values());c.verify_rows(fixed)
    actual_child=BASE/'extract_current_eleven_saved_gendf.py'
    if str(actual_child)not in unique or plan['source_pin']['path']not in unique or unique[plan['source_pin']['path']]!=plan['source_pin']:
        raise RuntimeError('all actual whole child and parser Sources protected')
    out.mkdir();(out/'runtime').mkdir();(out/'gendf-stage').mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=binding['original_bounded']['sha256']:raise RuntimeError('whole genuine original bounded Source')
    actual=out/'CURRENT_ACTUAL_ELEVEN_GENDF_EXECUTION_BINDING.json'
    c.write(actual,dict(schema='CURRENT_ELEVEN_SAVED_GENDF_EXPLICIT_EXECUTION_BINDING_V1',source_freeze_pin=psf,
      selected_genDF_source_plan_pin=planpin,current_case_spec_pin=casepin,actual_material_observation_report_pin=pobserved,
      requested_mts=[5],joint_archive_roots=roots,output_directory=str(childout),fixed_current_pins=fixed,
      original_immutable_compiler_role_pin=binding['compiler'],original_caps=CAPS,**FALSE))
    pact=c.pin(actual);owned.append(pact)
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'gendf-stage',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise RuntimeError('original guard class/MRO')
    command=[str(support.PYTHON),str(actual_child),'--binding-pin',json.dumps(pact,separators=(',',':')),
      '--expected-parent-pid',str(os.getpid())]
    failure=None;after_error=None;after=None;checks=[];receipt=None
    try:
        c.check_full_current(fixed,owned);resources.check()
        runner.execute(out/'gendf-stage','all_eleven_saved_MT5',command,600)
        checks.append(helper.check_watch(out,runner.records[-1]))
        record=runner.records[-1];log=out/(record['label']+'.log');lines=log.read_text().splitlines()
        if len(lines)!=1:raise RuntimeError('one full actual completion receipt, no omitted warning/error')
        receipt=json.loads(lines[0])
        if receipt['status']!='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY'or \
           any(receipt[k]is not False for k in FALSE):raise RuntimeError('actual extraction-only scope')
        pchild=receipt['report'];c.same_pin(pchild['path'],pchild)
        value=json.loads(Path(pchild['path']).read_text())
        if Path(pchild['path']).parent!=childout or value['execution_binding_pin']!=pact or \
           len(value['actual_extractions'])!=11 or value['actual_material_observation_report_pin']!=pobserved or \
           any(value[k]is not False for k in FALSE):raise RuntimeError('exact actual all-eleven report origin, not qualification')
        c.check_full_current(fixed,owned);after=resources.check()
    except BaseException as error:failure=type(error).__name__+': '+str(error)
    finally:
        try:c.check_full_current(fixed,owned);after=resources.check()
        except BaseException as error:after_error=type(error).__name__+': '+str(error)
    good=failure is None and after_error is None and len(runner.records)==1 and runner.records[0]['status']=='PASS'and receipt is not None
    summary_path=out/'Root_actual_eleven_saved_gendf_extraction_summary.json'
    summary=dict(
      schema='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_GUARDED_ROOT_V1',
      status='ACTUAL_ELEVEN_SAVED_MT5_EXTRACTION_CLOSED0_ONLY'if good else'FAILED_GENDF_EXTRACTION_NO_RETRY',
      failure=failure,after_check_error=after_error,records=runner.records,actual_watchdog_checks=checks,
      actual_child_receipt=receipt,fixed_current_pins=fixed,owned_input_pins=owned,
      complete_output_pins=[c.pin(p)for root in(out,childout)for p in sorted(root.rglob('*'))if p.is_file()],
      actual_material_observation_report_pin=pobserved,selected_genDF_source_plan_pin=planpin,source_freeze_pin=psf,
      original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,
      resources_before=before,resources_after=after,original_caps=CAPS,requires_host_process_metadata_access=True,
      native_engines_started=0,original_input_or_library_writes=0,
      explicit_current_mount_input_reattestation_provenance=c.current_metadata_reattestation_provenance(),
      current_input_reattestation_source_pin=sf['explicit_current_input_reattestation_pin'],**FALSE)
    c.write(summary_path,summary)
    summary_first_pin=c.pin(summary_path)
    try:resources.check()
    except BaseException as error:
        good=False;after_error=type(error).__name__+': '+str(error)
        summary.update(status='FAILED_GENDF_EXTRACTION_NO_RETRY',after_check_error=after_error,
          final_report_resource_check_failed=True)
        c.same_pin(summary_path,summary_first_pin)
        descriptor=os.open(summary_path,os.O_WRONLY|os.O_NOFOLLOW)
        try:
            item=os.fstat(descriptor)
            actual_identity=[item.st_dev,item.st_ino,item.st_mode,item.st_nlink,item.st_size,item.st_mtime_ns,item.st_ctime_ns]
            if actual_identity!=summary_first_pin['identity']:
                raise RuntimeError('new owned summary changed before controlled failure rewrite')
            with os.fdopen(descriptor,'w',encoding='utf-8')as stream:
                descriptor=None;stream.seek(0);stream.truncate(0)
                json.dump(summary,stream,indent=2,ensure_ascii=False,allow_nan=False)
                stream.write('\n');stream.flush();os.fsync(stream.fileno())
        finally:
            if descriptor is not None:os.close(descriptor)
        if c.identity(summary_path)[:4]!=summary_first_pin['identity'][:4]:
            raise RuntimeError('new owned summary inode/role changed after failure rewrite')
        resources.check()
    if not good:raise RuntimeError(failure or after_error or'incomplete genuine all-eleven extraction')


if __name__=='__main__':main()

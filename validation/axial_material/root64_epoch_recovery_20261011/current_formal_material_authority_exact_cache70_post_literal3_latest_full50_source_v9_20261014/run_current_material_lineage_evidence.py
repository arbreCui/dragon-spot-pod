#!/usr/bin/env python3
"""One original-guard evidence stage, with intentional exit2 preserved.

All bound evidence namespaces share the original 2GiB ceiling, including the
original five roles and retained outputs from previous evidence stages. The actual
watchdog's exit2 is accepted only alongside the exact complete stdout receipt,
full output pin, original command/caps and no resource failure. It remains a
FAILED original runner record, never a forged PASS or a physics admission.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
COMMON=REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/guarded_warm_A_common.py'
spec=importlib.util.spec_from_file_location('current_lineage_original_guard',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
from current_material_prerequisite_admission import replace_owned_failure_summary,check_original_host_limits


def main():
    parser=argparse.ArgumentParser()
    for prefix in['request','source-freeze','host-freeze']:
        for suffix in['summary','sha256','seven-id']:
            parser.add_argument('--'+prefix+'-'+suffix,required=True)
    args=parser.parse_args();start=time.monotonic()
    def load(prefix):
        return c.load_json_exact(getattr(args,prefix+'_summary'),
          getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    request,prequest=load('request');sf,psf=load('source_freeze');hf,phf=load('host_freeze')
    if request['schema']!='CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'or \
       request['operation']not in('extract','aggregate','compare-three')or \
       request['complete_source_freeze_pin']!=psf:
        raise RuntimeError('explicit actual request and complete exact executing Source freeze')
    if sf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'or sf['candidate_executed']is not False:
        raise RuntimeError('external immutable complete Source-only package')
    if hf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_ONLY_FREEZE_V1'or \
       hf['candidate_executed']is not False or hf['host_source']['path']!=str(Path(__file__).absolute()):
        raise RuntimeError('external whole own host Source freeze')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(hf['dependencies']);c.verify_rows(sf['complete_source_file_pins'])
    out=Path(request['owning_host_output_directory']);childout=Path(request['output_directory'])
    if not out.is_absolute()or out.parent!=c.ART or os.path.lexists(out)or \
       childout!=out.with_name(out.name+'-evidence')or os.path.lexists(childout):
        raise RuntimeError('one fresh literal owning artifact namespace and exact child output')
    binding,fixed,support,helper,full,oldresources,before=c.initialize(out,start)
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('original initial fullfresh2/cold/meta/history96 reserve')
    roots=request['joint_archive_roots']
    if type(roots)is not list or len(roots)<5 or len(set(roots))!=len(roots) or \
       str(childout)not in roots or str(out)not in roots or \
       any(not Path(p).is_absolute()for p in roots)or \
       any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b):
        raise RuntimeError('all five roles and retained previous-stage outputs counted without overlap')
    # A completed observer root is still part of the original joint evidence
    # transaction. Counting it only as an unrelated old input would narrow 2GiB.
    original_parent=sys.modules[full.OwnRSSSerialExecutor.__bases__[0].__module__]
    if Path(original_parent.__file__).resolve()!=support.PARENT:
        raise RuntimeError('genuine original DiskResources Source path')
    joined=original_parent.DiskResources(c.ART,roots,8*2**30,2*2**30)
    class Resources:
        def check(self):
            return dict(original_history_cold_free=oldresources.check(),complete_joint_five_root_fresh=joined.check())
    resources=Resources();resources.check()
    fixed+=[prequest,psf,phf,hf['host_source']]+hf['dependencies']+sf['complete_source_file_pins']+request['complete_input_pins']
    table={}
    for p in fixed:
        if p['path']in table and table[p['path']]!=p:raise RuntimeError('ambiguous fixed full-file pin')
        table[p['path']]=p
    fixed=list(table.values());c.verify_rows(fixed)
    child=BASE/'current_material_lineage_evidence.py'
    if str(child)not in table:raise RuntimeError('complete actual child Source in protected inputs')
    out.mkdir();(out/'runtime').mkdir();(out/'evidence-stage').mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py')
    owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
    if owned[0]['sha256']!=binding['original_bounded']['sha256']:raise RuntimeError('original bounded Source exact copy')
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'evidence-stage',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources:
        raise RuntimeError('original guard class/MRO unchanged')
    command=[str(support.PYTHON),str(child),request['operation'],'--request-pin',
      json.dumps(prequest,separators=(',',':')),'--output-dir',str(childout),'--expected-parent-pid',str(os.getpid())]
    error=None;failure=None;after_error=None;receipt=None;watchpin=None;logpin=None;after=None
    try:
        c.check_full_current(fixed,owned);resources.check()
        try:runner.execute(out/'evidence-stage','complete_evidence',command,600)
        except RuntimeError as exc:error=str(exc)
        if len(runner.records)!=1:raise RuntimeError('one genuine actual stage')
        record=runner.records[0];watchpath=out/(record['label']+'.watchdog.json');logpath=out/(record['label']+'.log')
        watchpin=c.pin(watchpath);logpin=c.pin(logpath);watch=json.loads(watchpath.read_text())
        if error!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           type(watch['returncode'])is not int or watch['returncode']!=2 or watch['limit_failure']is not None or \
           watch['command']!=command or watch['rss_cap_mib']!=512 or \
           watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True or \
           not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 or \
           not 0<=watch['sampled_peak_rss_mib']<512:
            raise RuntimeError('actual intentional evidence exit2 requires full normal resource closure')
        lines=logpath.read_text().splitlines()
        if len(lines)!=1:raise RuntimeError('exact one complete actual JSON receipt, no dropped warning or exception')
        receipt=json.loads(lines[0])
        if receipt['status']!='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2':raise RuntimeError('actual evidence completion receipt')
        reportpin=receipt['report'];c.same_pin(reportpin['path'],reportpin)
        if Path(reportpin['path']).parent!=childout:raise RuntimeError('actual report outside fresh child output')
        value=json.loads(Path(reportpin['path']).read_text())
        if value['current_case_spec_pin']!=request['current_case_spec_pin']:
            raise RuntimeError('actual evidence case authority changed')
        for key in('reaction_multiplicity_qualified','physical_neutron_balance_qualified',
                   'coupled_370group_reference_qualified','scientific_accuracy_qualified','goal_complete'):
            if receipt[key]is not False or value[key]is not False:raise RuntimeError('evidence must not mint qualification')
        c.check_full_current(fixed,owned);after=resources.check()
    except BaseException as exc:failure=type(exc).__name__+': '+str(exc)
    finally:
        try:c.check_full_current(fixed,owned);after=resources.check()
        except BaseException as exc:after_error=type(exc).__name__+': '+str(exc)
    good=failure is None and after_error is None and receipt is not None
    summary=out/'Root_actual_current_material_evidence_summary.json'
    report=dict(
      schema='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1',
      status='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'if good else'ACTUAL_CURRENT_EVIDENCE_FAILED_NO_RETRY',
      operation=request['operation'],failure=failure,after_check_error=after_error,records=runner.records,
      actual_intentional_exit2_normal_closure=good,actual_complete_child_receipt=receipt,
      actual_watchdog_full_pin=watchpin,actual_log_full_pin=logpin,fixed_current_pins=fixed,
      complete_output_pins=[c.pin(p)for root in(out,childout)for p in sorted(root.rglob('*'))if p.is_file()],
      original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
      SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,
      resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,
      requires_host_process_metadata_access=True,current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),physical_neutron_balance_qualified=False,
      coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,final_report_bytes_in_original_resources=True,**c.scope())
    c.write(summary,report);sp=c.pin(summary)
    try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)
    except BaseException as error:
        report['status']='ACTUAL_CURRENT_EVIDENCE_FAILED_NO_RETRY';report['failure']=type(error).__name__+': '+str(error)
        report['after_check_error']=report['failure'];report['wall_seconds']=time.monotonic()-start
        report['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss
        replace_owned_failure_summary(c,summary,sp,report);good=False
    if not good:raise RuntimeError(failure or after_error or'incomplete actual evidence')


if __name__=='__main__':main()

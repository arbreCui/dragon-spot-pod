#!/usr/bin/env python3
"""Finalize reviewed Source-only Host HFs; never imports or executes a Host."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

REC=Path(__file__).resolve().parent


def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pf(path):
    p=Path(path);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert ids(os.fstat(fd))==ids(s);parts=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            parts.append(b)
        data=b''.join(parts);assert len(data)==s.st_size and ids(os.fstat(fd))==ids(s)
    finally:os.close(fd)
    assert ids(p.lstat())==ids(s)
    return data,dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=ids(s))


def normalized(row):return{k:row[k]for k in ('path','sha256','size_bytes','identity')}


def rows(value):
    found=[]
    if isinstance(value,dict):
        if all(k in value for k in ('path','sha256','size_bytes','identity')):found.append(normalized(value))
        for v in value.values():found.extend(rows(v))
    elif isinstance(value,list):
        for v in value:found.extend(rows(v))
    return found


def unique(entries):
    table={}
    for row in entries:
        row=normalized(row)
        assert row['path']not in table or table[row['path']]==row
        table[row['path']]=row
    return list(table.values())


def write(folder,name,value):
    p=folder/name;data=(json.dumps(value,indent=2)+'\n').encode()
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:assert os.write(fd,data)==len(data);os.fsync(fd)
    finally:os.close(fd)
    return pf(p)[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--peer-review-json',required=True)
    parser.add_argument('--peer-review-sha256',required=True)
    parser.add_argument('--peer-review-seven-id',required=True)
    parser.add_argument('--peer-true-tool-json',required=True)
    args=parser.parse_args()
    peerbytes,peerpin=pf(args.peer_review_json);peer=json.loads(peerbytes)
    assert peerpin['sha256']==args.peer_review_sha256 and peerpin['identity']==json.loads(args.peer_review_seven_id)
    assert peer['failure']is None and str(peer['status']).startswith('PASS')
    assert peer.get('source_only')is True and peer.get('compiler_executed',peer.get('compiled'))is False and peer['numerical_executed']is False
    receiptbytes,receiptpin=pf(args.peer_true_tool_json);receipt=json.loads(receiptbytes)
    actual=receipt['actual_review_return']
    assert receipt.get('observed_closed')is True
    assert isinstance(actual,dict)and type(actual['exit_code'])is int and actual['exit_code']==0 and not actual.get('session_id')
    output=actual['output'];line=next(line for line in reversed(output.splitlines())if line.strip().startswith('{'))
    observed=json.loads(line);assert normalized(observed['review_pin'])==peerpin
    peerrows=rows(peer)
    complete=[]
    for kind,stem,hfschema in [
      ('public','public_read_compact_bq_admission_control_host','COMPLETE_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1')]:
        folder=REC/(stem+'_source_v7_20261014');readybytes,readypin=pf(folder/'HOST_SOURCE_REVIEW_READY.json');ready=json.loads(readybytes)
        hostpin=ready['host_source'];planpin=ready['control_host_plan_pin']
        assert hostpin in peerrows and planpin in peerrows
        assert pf(hostpin['path'])[1]==hostpin
        planbytes,actualplanpin=pf(planpin['path']);assert actualplanpin==planpin;plan=json.loads(planbytes)
        assert plan['compiler_executed']is False and plan['numerical_executed']is False
        bhfbytes,bhfpin=pf(plan['selected_new_build_Host_freeze_pin']['path']);assert bhfpin==plan['selected_new_build_Host_freeze_pin'];bhf=json.loads(bhfbytes)
        sfbytes,sfpin=pf(plan['selected_control_Source_freeze_pin']['path']);assert sfpin==plan['selected_control_Source_freeze_pin'];sf=json.loads(sfbytes)
        csfbytes,csfpin=pf(plan['selected_post_release_Common_Source_freeze_pin']['path'])
        csf=json.loads(csfbytes);assert csfpin==plan['selected_post_release_Common_Source_freeze_pin']
        assert csf['schema']=='COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_ONLY_FREEZE_V1'
        assert csf['source_only']is True and csf['compiled']is False and csf['numerical_executed']is False
        assert plan['selected_post_release_Common_Source_pin']==csf['new_Common_Source_pin']
        assert plan['actual_exact_release_receipt_pin']==csf['actual_release_receipt_pin']
        assert plan['actual_independent_postrelease_review_pin']==csf['actual_independent_postrelease_review_pin']
        oldfolder=REC/(stem+'_source_v5_20261013')
        oldhfbytes,oldhfpin=pf(ready['predecessor_Host_source_freeze_pin']['path']);oldhf=json.loads(oldhfbytes)
        assert oldhfpin==ready['predecessor_Host_source_freeze_pin']
        lifetimebytes,lifetimepin=pf(ready['lifetime_Source_plan_pin']['path']);lifetime=json.loads(lifetimebytes)
        assert lifetimepin==ready['lifetime_Source_plan_pin']==plan['completed_first_SRC_bundle_lifetime_Source_plan_pin']
        assert lifetime['exact_retirement_case']=='public_read_stale_BQ_SRC'
        assert lifetime['exact_bundle_relative_path']=='public_read_stale_BQ_SRC/coherent_complete_context.xsm'
        assert lifetime['original_aux_bytes']==128*2**20 and lifetime['pending_bytes']==8*2**20
        assert lifetime['maximum_live_synthetic_context_bundles']==1 and lifetime['intent_parent_entry_fsync_before_unlink']is True
        assert lifetime['future_actual_retirement_receipt_pin']is None and lifetime['future_actual_public7_report_pin']is None
        ownfiles=[readypin,planpin,ready['complete_Host_plan_inverse_pin'],lifetimepin,
          ready['private_retirement_helper_Source_pin'],oldhfpin,ready['predecessor_argv_Source_template_pin'],
          ready['actual_failed_public5_summary_pin'],ready['actual_failed_public5_true_tool_return_pin'],
          ready['actual_failed_public5_independent_postverification_pin'],ready['actual_failed_public5_independent_true_tool_pin'],
          ready['predecessor_unfrozen_public6_Source_pin']]
        ownfiles.append(pf(folder/'COMPLETE_PUBLIC_HOST_V6_TO_V7_APFS_INTENT_SYNC_WHOLE_BYTE_INVERSE.json')[1])
        workflow=[]
        for path in [Path(__file__),REC/'prepare_public_read_control_host_completed_bundle_lifetime_source_v7_source_only_20261014.py',
          REC/'ACTUAL_PUBLIC7_COMPLETED_FIRST_SRC_BUNDLE_LIFETIME_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json',
          REC/'ACTUAL_PUBLIC7_V6_TO_V7_APFS_INTENT_SYNC_SOURCE_INVERSE_TRUE_TOOL_RETURNS_20261014.json']:
            workflow.append(pf(path)[1])
        deps=unique(bhf['dependencies']+oldhf['dependencies']+[bhfpin,bhf['host_source'],plan['selected_new_Fortran_Source_freeze_pin'],
          sfpin,peerpin,receiptpin,csfpin]+csf['files']+csf['original_source_metadata_pins']+sf['files']+sf['original_source_pins']+sf.get('dependencies',[])+ownfiles+workflow)
        # Original 2532 complete Source-admitted dependency rows are inherited,
        # with exact seven identities rechecked. No science qualification or
        # repeated full scientific EOF is claimed by this Source-only step.
        for row in deps:
            p=Path(row['path']);s=p.lstat()
            assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and ids(s)==row['identity']
        table={row['path']:row for row in deps}
        for selected in (plan['selected_new_build_Host_freeze_pin'],plan['selected_new_Fortran_Source_freeze_pin'],csfpin,
                         csf['new_Common_Source_pin'],csf['new_catalog_pin'],csf['new_binding_pin'],
                         csf['actual_release_receipt_pin'],csf['actual_release_true_tool_return_pin'],
                         csf['actual_independent_postrelease_review_pin'],csf['actual_independent_postrelease_true_tool_return_pin']):
            assert table[selected['path']]==selected
        assert all(table[row['path']]==normalized(row)for row in bhf['dependencies'])
        assert all(table[row['path']]==normalized(row)for row in oldhf['dependencies'])
        hf=write(folder,'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json',dict(schema=hfschema,
          status='FROZEN_REVIEWED_SOURCE_ONLY_UNIMPORTED_UNEXECUTED',compiler_executed=False,numerical_executed=False,
          Host_imported_or_executed=False,host_source=hostpin,control_host_plan_pin=planpin,dependencies=deps,
          selected_new_build_Host_freeze_pin=plan['selected_new_build_Host_freeze_pin'],
          selected_new_Fortran_Source_freeze_pin=plan['selected_new_Fortran_Source_freeze_pin'],
          predecessor_Host_source_freeze_pin=oldhfpin,
          actual_failed_public5_summary_pin=ready['actual_failed_public5_summary_pin'],
          actual_failed_public5_true_tool_return_pin=ready['actual_failed_public5_true_tool_return_pin'],
          selected_completed_first_SRC_bundle_lifetime_Source_plan_pin=lifetimepin,
          exact_completed_first_SRC_bundle_retirement_scope_only=True,
          retired_bundle_is_historical_not_current_no_generic_missing_skip=True,
          original_Fortran_math_7controls_9phases_11commands_unchanged=True,
          exact_original_SerialExecutor_stages_parent_precreated=True,
          selected_control_Source_freeze_pin=sfpin,selected_post_release_Common_Source_freeze_pin=csfpin,
          selected_post_release_Common_Source_pin=csf['new_Common_Source_pin'],
          selected_post_release_current_catalog_pin=csf['new_catalog_pin'],
          selected_post_release_current_binding_pin=csf['new_binding_pin'],
          actual_exact_release_receipt_pin=csf['actual_release_receipt_pin'],
          actual_exact_release_true_tool_return_pin=csf['actual_release_true_tool_return_pin'],
          actual_independent_postrelease_review_pin=csf['actual_independent_postrelease_review_pin'],
          actual_independent_postrelease_true_tool_return_pin=csf['actual_independent_postrelease_true_tool_return_pin'],
          independent_Host_Source_review_pin=peerpin,
          independent_Host_Source_true_tool_return_pin=receiptpin,actual_independent_Source_review_return=0,
          original_caps=plan['original_caps'],original_aux_cap_bytes=128*2**20,original_pending_metadata_bytes=8*2**20,
          planned_output_root=plan['planned_output_root'],planned_guarded_stage_count=plan['planned_total_guarded_stages'],
          inherited_original_new_build_HF_dependency_count=len(bhf['dependencies']),all_inherited_dependency_rows_exact=True,
          inherited_dependency_fullEOF_provenance_not_new_scientific_EOF=True,all_active_dependency_identities_reobserved=True,
          actual_future_new_build70_report_pin=None,actual_future_control_object_pin=None,
          actual_future_control_executable_pin=None,actual_future_control_report_pin=None,
          actual_future_stale_Host_manifest_pins=None,actual_future_completed_bundle_retirement_receipt_pin=None,
          compile_qualified=False,reader_qualified=False,
          private_model_not_independent_reader_qualification=True,old17_PASS_inherited=False,AAA_qualified=False,ABA_admitted=False))
        descriptor=write(folder,'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json',dict(
          schema='COMPACT_BQ_CONTROL_HOST_NINE_EXTERNAL_ARGUMENT_SOURCE_TEMPLATE_V1',kind=kind,
          source_only=True,compiler_executed=False,numerical_executed=False,host_source_pin=hostpin,
          host_freeze_pin=hf,Source_freeze_pin=sfpin,
          required_new_build70_parameters=dict(summary=plan['new_build_expected_report_path'],sha256=None,seven_id=None),
          actual_source_freeze_parameters=dict(summary=sfpin['path'],sha256=sfpin['sha256'],seven_id=sfpin['identity']),
          actual_host_freeze_parameters=dict(summary=hf['path'],sha256=hf['sha256'],seven_id=hf['identity']),
          command_entry=hostpin['path'],mandatory_exact_argument_prefixes=['new-build70','source-freeze','host-freeze'],
          original_exact_python_executable='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',
          argv_template=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',hostpin['path'],
            '--new-build70-summary',plan['new_build_expected_report_path'],'--new-build70-sha256',None,
            '--new-build70-seven-id',None,'--source-freeze-summary',sfpin['path'],
            '--source-freeze-sha256',sfpin['sha256'],'--source-freeze-seven-id',json.dumps(sfpin['identity'],separators=(',',':')),
            '--host-freeze-summary',hf['path'],'--host-freeze-sha256',hf['sha256'],
            '--host-freeze-seven-id',json.dumps(hf['identity'],separators=(',',':'))],
          all_three_require_summary_sha256_seven_id=True,planned_environment=bhf.get('planned_environment',
            dict(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')),
          runnable_before_genuine_new_build70_actual_external_PF=False,future_actual_control_report_pin=None))
        complete.append(dict(kind=kind,host_freeze_pin=hf,argv_Source_template_pin=descriptor,
          host_source_pin=hostpin,dependency_count=len(deps)))
    print(json.dumps({'status':'PUBLIC7_REVIEWED_LIFETIME_HOST_SOURCE_ONLY_HF_FROZEN_UNEXECUTED',
      'packages':complete,'actual_peer_Source_review_return':0,'compiler_executed':False,'numerical_executed':False,'Host_imported_or_executed':False}))


if __name__=='__main__':main()

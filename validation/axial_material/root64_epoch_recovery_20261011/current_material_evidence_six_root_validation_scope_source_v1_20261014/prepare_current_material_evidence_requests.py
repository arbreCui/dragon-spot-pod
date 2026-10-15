#!/usr/bin/env python3
"""Derive explicit evidence requests from actual current receipts, no engine.

Extraction may be prepared after a real closed observation. Aggregation needs
a separate actual extraction review, not a Source-only label. New requests and
coverage metadata remain unqualified even when every pin is valid.
"""
import argparse
import json
import os
from pathlib import Path
from current_material_lineage_evidence import (CASE_SHA,CAPS,FALSE,check,pin,
    read,require,strict,write,admit_owning_stage)


def unique(pins):
    result={}
    for p in pins:
        require(p['path']not in result or result[p['path']]==p,'same path has one complete identity')
        result[p['path']]=p
    return list(result.values())


def admit_evidence_host(expected):
    value=read(expected,lambda:None)
    require(value['schema']=='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'and
      value['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'and
      value['failure']is None and value['after_check_error']is None and
      value['actual_intentional_exit2_normal_closure']is True and len(value['records'])==1,
      'real independently closed evidence-only host')
    record=value['records'][0];watch=read(value['actual_watchdog_full_pin'],lambda:None)
    require(record['status']=='FAILED'and record['error']=='own-child stage failed; no retry'and
      type(watch['returncode'])is int and watch['returncode']==2 and watch['limit_failure']is None and
      watch['command']==record['command']and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and
      watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and
      0<=watch['sampled_peak_rss_mib']<512,'actual intentional exit2, not failed capture')
    check(value['actual_log_full_pin'],lambda:None)
    receipt=value['actual_complete_child_receipt']
    lines=Path(value['actual_log_full_pin']['path']).read_text().splitlines()
    require(len(lines)==1 and strict(lines[0])==receipt,'full actual one-line receipt')
    for p in value['fixed_current_pins']+value['complete_output_pins']:check(p,lambda:None)
    require(type(value['SELF_peak_bytes'])is int and value['SELF_peak_bytes']<512*2**20 and
      0<value['wall_seconds']<1800,'real original own host limits')
    return value,read(receipt['report'],lambda:None),receipt['report']


def base_request(operation,sfpin,casepin,out,observedroot,requestroot,fixed):
    require(casepin['sha256']==CASE_SHA,'formal current case')
    require(out.is_absolute()and out.parent==Path('/Users/wen/spot/validation/artifacts')and
      not os.path.lexists(out)and not os.path.lexists(out.with_name(out.name+'-evidence')),'fresh literal future host/child output')
    source_root=Path(sfpin['path']).parent
    roots=[str(out),str(out.with_name(out.name+'-evidence')),str(observedroot),str(source_root),str(requestroot)]
    require(len(set(roots))==5 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),
      'five complete disjoint original2GiB evidence roots')
    return dict(schema='CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1',operation=operation,
      current_case_spec_pin=casepin,complete_source_freeze_pin=sfpin,
      complete_input_pins=unique([sfpin,casepin]+fixed),original_caps=CAPS,
      owning_host_output_directory=str(out),output_directory=str(out.with_name(out.name+'-evidence')),
      joint_archive_roots=roots,request_preparation_only=True,actual_stage_executed=False,**FALSE)


def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['extract','aggregate','compare-three'])
    p.add_argument('--source-freeze-pin',required=True);p.add_argument('--observation-manifest-pin',required=True)
    p.add_argument('--request-output-dir',required=True);p.add_argument('--future-host-output-dir',required=True)
    p.add_argument('--extraction-host-pin');p.add_argument('--independent-extraction-review-pin')
    p.add_argument('--formal-producer-plan-pin');args=p.parse_args()
    sfpin=strict(args.source_freeze_pin);sf=read(sfpin,lambda:None)
    require(sf['schema']=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False,
      'complete immutable Source-only evidence package')
    for pinrow in sf['complete_source_file_pins']:check(pinrow,lambda:None)
    mpin=strict(args.observation_manifest_pin);m=read(mpin,lambda:None)
    require(m['schema']=='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1'and m['state_order']==['A']and
      m['observation_scope']=='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',
      'actual one same-physical A observation, no retagged plane history')
    state=m['states']['A'];actual=admit_owning_stage(state['actual_owning_report_pin'],state['actual_stage_label'],
      state['actual_command'],lambda:None)
    require(actual['schema']=='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'and
      actual['status']=='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'and len(actual['records'])==1 and
      actual['actual_B_observation_executed']is False and actual['three_recaptured_plane_histories_claimed']is False,
      'actual one complete current A capture only')
    releasepin=m['actual_closed_owned_library_copy_release_pin'];release=read(releasepin,lambda:None)
    require(release['schema']=='ACTUAL_CLOSED_PRIVATE_MATERIAL_INPUT_COPY_RELEASE_V1'and
      release['all_owned_copy_paths_absent_after_release']is True and release['total_owned_bytes_released']==979740136 and
      release['all_results_contexts_native_observations_retained']is True,'actual closed redundant copy lifecycle')
    for v in release['original_live_input_pins'].values():check(v,lambda:None)
    for v in release['owned_copy_pins_before_release']:require(not os.path.lexists(v['path']),'released copy is historical consumption only')
    fixed=actual['fixed_current_pins']+actual['output_pins']+[mpin,state['actual_owning_report_pin'],releasepin]
    fixed+=state['complete_observed_file_pins']+state['physical_input_pins']
    for v in unique(fixed):check(v,lambda:None)
    observedroot=Path(state['actual_cwd']).parent;completionroot=Path(mpin['path']).parent
    priorpin=actual['original_failed_phase_pin'];prior=read(priorpin,lambda:None)
    require(actual['completion_only_existing_closed_stage']is True and
      actual['Dragon_or_compiler_or_material_child_launched_by_continuation']is False and
      actual['original_capture_collector_not_reexecuted']is True and
      actual['actual_prior_material_stage_record_reused_wholebytes']is True and
      actual['original_Root_exit_code_retained']==1 and
      prior['status']=='FAILED_CURRENT_OBSERVATION_NO_RETRY'and
      prior['failure']=='RuntimeError: both real process metadata tools fully pinned'and
      actual['original_Root_failure_retained']==prior['failure']and
      actual['records']==prior['records']and
      observedroot==Path(priorpin['path']).parent and
      state['actual_cwd']==str(observedroot/'A')and
      actual['actual_prior_A_cwd']==state['actual_cwd']and
      actual['original_release_owner_output_root']==str(observedroot)and
      Path(state['actual_owning_report_pin']['path']).parent==completionroot and
      m['completion_only_original_Root1_preserved']is True and
      m['original_failed_phase_pin']==priorpin and
      m['original_Root_true_tool_pin']==actual['original_Root_true_tool_pin']and
      observedroot!=completionroot and
      not observedroot.is_relative_to(completionroot)and
      not completionroot.is_relative_to(observedroot),
      'only exact completion report and retained original captured physical owner')
    root=Path(args.request_output_dir);require(root.is_absolute()and not os.path.lexists(root),'fresh metadata request namespace')
    root.mkdir();out=Path(args.future_host_output_dir)
    request=base_request(args.operation,sfpin,m['current_case_spec_pin'],out,observedroot,root,fixed)
    request['original_five_role_roots']=list(request['joint_archive_roots'])
    request['joint_archive_roots'].append(str(completionroot))
    require(len(request['joint_archive_roots'])==6 and len(set(request['joint_archive_roots']))==6 and
      not any(Path(a).is_relative_to(Path(b))for a in request['joint_archive_roots']for b in request['joint_archive_roots']if a!=b),
      'five original roles plus exact retained completion metadata sixth root; same2GiB')
    request['exact_retained_original_observed_root']=str(observedroot)
    request['exact_retained_completion_metadata_root']=str(completionroot)
    request['completion_original_failed_phase_pin']=priorpin
    request['actual_observation_manifest_pin']=mpin
    if args.operation!='extract':
        require(args.extraction_host_pin is not None,'real previous full extraction host pin')
        ehpin=strict(args.extraction_host_pin);eh,er,erpin=admit_evidence_host(ehpin)
        require(eh['operation']=='extract'and er['actual_observation_manifest_pin']==mpin and
          er['schema']=='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'and
          er['all_complete_state_scope_retained']is True and er['state_order']==['A'], 'same actual complete extraction')
        # Retained original capture and complete previous extraction spools
        # share the same unchanged2GiB ceiling with the next operation. There
        # is no per-stage reset that hides an earlier large evidence pool.
        for prior in (str(Path(ehpin['path']).parent),str(Path(erpin['path']).parent)):
            if prior not in request['joint_archive_roots']:request['joint_archive_roots'].append(prior)
        require(not any(Path(a).is_relative_to(Path(b))for a in request['joint_archive_roots']
          for b in request['joint_archive_roots']if a!=b),'complete retained evidence roots disjoint')
        pairs=[dict(event=r['event'],role=r['role'],root_prefix=r['root_prefix'],input_pin=r['input_pin'],
          sqlite_pin=r['paired_SQLite_pin'],native_pool_pin=r['paired_original_pool_pin'])for r in er['states']['A']]
        require(pairs and pairs[-1]['role']=='final-complete-micro','genuine last original full final micro')
        for pair in pairs:
            for key in('input_pin','sqlite_pin','native_pool_pin'):check(pair[key],lambda:None)
        request['complete_input_pins']=unique(request['complete_input_pins']+[ehpin,erpin]+eh['fixed_current_pins']+eh['complete_output_pins'])
        if args.operation=='aggregate':
            require(args.independent_extraction_review_pin is not None,'separate actual complete extraction review')
            irpin=strict(args.independent_extraction_review_pin);review=read(irpin,lambda:None)
            require(review['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and
              review['actual_extraction_report_pin']==erpin and review['actual_extraction_host_pin']==ehpin and
              review['actual_observation_manifest_pin']==mpin and review['all_snapshot_pairs']==pairs and
              review['complete_context_pins']==state['complete_context_pins']and
              review['all_original_snapshot_and_context_pins_verified']is True,
              'independent actual saved full-prefix/tree/context review, no Source-only substitute')
            cov=dict(schema='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1',
              all_original_snapshot_pairs_saved=True,actual_extraction_report_pin=erpin,
              actual_observation_manifest_pin=mpin,actual_closed_extraction_receipt_independently_reviewed=True,
              independent_actual_review_pin=irpin,states=dict(A=dict(all_snapshot_pairs=pairs,
                complete_context_pins=state['complete_context_pins'])),new_qualification_sha256=None,**FALSE)
            cp=root/'CURRENT_ACTUAL_COMPLETE_CONTEXT_EXTRACTION_COVERAGE.json';write(cp,cov);cpin=pin(cp,lambda:None)
            # The prior independent review binds every actual snapshot pair
            # and context. This newly derived coverage pins that exact review;
            # it does not invent a review of a not-yet-existing file identity.
            final=pairs[-1]
            request['aggregation_binding']=dict(state_order=['A'],Source_route=dict(ITSTMP=0,historical_call_proved=False),
              states=dict(A=dict(sqlite_pin=final['sqlite_pin'],native_pool_pin=final['native_pool_pin'])),
              actual_context_states=dict(A=dict(complete_context_pins=state['complete_context_pins'],all_snapshot_pairs=pairs,
                actual_extraction_report_pin=erpin,actual_observation_manifest_pin=mpin,
                selected_last_libmix_number=state['selected_last_libmix_number'],actual_extraction_coverage_contract_pin=cpin)))
            request['actual_extraction_independent_review_pin']=irpin
            request['complete_input_pins']=unique(request['complete_input_pins']+[irpin,cpin])
        else:
            require(args.formal_producer_plan_pin is not None,'exact protected current three actual producer plan')
            fpin=strict(args.formal_producer_plan_pin);formal=read(fpin,lambda:None)
            require(m['current_case_spec_pin']in formal['formal_inputs']and len(formal['producers'])==3,'same current formal case and three independent physical producers')
            producers=[]
            for plane,row in enumerate(formal['producers'],1):
                report=read(row['report'],lambda:None)
                require(len(report['records'])==4 and report['failure']is None and report['after_check_error']is None and
                  report['actual_native_terminal']==row['native_readback']and row['native_readback']['plane']==plane,
                  'own true four-stage current single-plane solve/full readback')
                solves=[s for s in report['records']if s['label'].endswith('/solve')]
                require(len(solves)==1,'one actual single-plane solve Source stage')
                for stage in report['records']:admit_owning_stage(row['report'],stage['label'],stage['command'],lambda:None)
                check(row['archive'],lambda:None)
                producers.append(dict(plane=plane,archive_pin=row['archive'],actual_report_pin=row['report'],
                  actual_solve_label=solves[0]['label'],actual_solve_command=solves[0]['command']))
                request['complete_input_pins']=unique(request['complete_input_pins']+[row['report'],row['archive']]+
                  report['fixed_current_pins']+report['output_pins'])
            request['observed_final_A_pair']=pairs[-1];request['actual_native_producers']=producers
            request['complete_input_pins']=unique(request['complete_input_pins']+[fpin])
    target=root/'CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json';write(target,request)
    print(json.dumps(dict(status='CURRENT_ACTUAL_EVIDENCE_REQUEST_PREPARED_NO_BUSINESS_EXECUTION',
      request=pin(target,lambda:None),**FALSE),allow_nan=False))


if __name__=='__main__':main()

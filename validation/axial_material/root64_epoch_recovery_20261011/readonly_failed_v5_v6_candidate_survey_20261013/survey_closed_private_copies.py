"""Candidate investigation only. No unlink, compiler, business, or release manifest."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
ART=ROOT/'validation/artifacts'
OUT=Path(__file__).absolute().parent
HELPER=REC/'storage_release_closed_v7_v8_project_pair_20261013/independent_postverify_20261013/verify_exact_two_postrelease_v2.py'
spec=importlib.util.spec_from_file_location('independent_readonly_full_EOF_helpers',HELPER)
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
START=time.monotonic()

def walk_pins(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('sha256'),str):
            yield value
            return
        for item in value.values():yield from walk_pins(item)
    elif isinstance(value,list):
        for item in value:yield from walk_pins(item)

def main():
    pk=REC/'storage_release_closed_v7_v8_project_pair_20261013'
    mp=dict(path=str(pk/'EXACT_TWO_CLOSED_FAILED_RUN_PROJECT_PRIVATE_COPY_MANIFEST.json'),sha256='cd9959328b0f12ff88f5b858a9ffb41ae6221ca0da760e2b293a3b999b4d6c19',size_bytes=3861469,identity=[16777229,49980346,33188,1,3861469,1791847142031341032,1791847142031341032])
    manifest=s.exact_json(mp)
    protected=manifest['current_protected_full_EOF_pins']
    s.check(len(protected)==4390,'complete prior current protected fullpins')
    table={}
    for row in protected:
        s.same(row);table[row['path']]=row
    # Current70 material namespace was created after that frozen protection union.
    material=REC/'current_formal_material_authority_exact_cache70_source_v3'
    material_files=[];material_origins=[];explicit_device_events=[];absent_referenced_paths=[]
    material_paths=sorted(str(p) for p in material.rglob('*') if p.is_file())
    for name in material_paths:
        row=s.pin(name);s.same(row);table[name]=row;material_files.append(row)
        if Path(name).suffix!='.json':continue
        value=s.exact_json(row)
        for wanted in walk_pins(value):
            path=Path(wanted['path'])
            s.check(path.is_absolute() and '..' not in path.parts,'material reference canonical path')
            if not os.path.lexists(path):
                # Still exclude a candidate path if ever mentioned; do not fabricate a live pin.
                absent_referenced_paths.append(str(path));continue
            actual=s.pin(path)
            s.check(actual['sha256']==wanted['sha256'],'new material referenced full EOF SHA unchanged')
            n=wanted.get('size_bytes',wanted.get('bytes'))
            if n is not None:s.check(actual['size_bytes']==n,'new material referenced complete byte size')
            identity=wanted.get('identity',wanted.get('seven_id'))
            if identity is not None and identity!=actual['identity']:
                s.check(identity[0]==16777234 and actual['identity'][0]==16777229 and identity[1:]==actual['identity'][1:],'explicit only device34to29 material reattestation')
                explicit_device_events.append(dict(historical_pin=wanted,current_pin=actual))
            s.same(actual);table[actual['path']]=actual;material_origins.append(actual)
    s.check(sorted(str(p) for p in material.rglob('*') if p.is_file())==material_paths,'new material namespace stable during finite readonly survey')
    catalog=s.exact_json(table[str(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')])
    common=s.exact_json(table[str(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')])
    science=s.exact_json(table[str(REC/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')])
    hf=s.exact_json(table[str(REC/'aaa_three_plane_streaming_pipeline_source_v9/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')])
    s.check(len(catalog['rows'])==3040 and len(common['fixed_current_pins'])==2012 and len(science['fixed_current_pins'])==3315 and len(science['science_original_input_pins'])==1129 and len(hf['dependencies'])==257,'original all row counts')
    for wanted in [r['current_pin'] for r in catalog['rows']]+common['fixed_current_pins']+science['fixed_current_pins']+science['science_original_input_pins']+hf['dependencies']:
        s.check(table[wanted['path']]==wanted,'every original current row fullpin protected')
    protected_paths=set(table)|set(absent_referenced_paths)
    protected_inodes={tuple(row['identity'][:2]) for row in table.values()}
    formal=s.exact_json(table[str(REC/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json')])
    originals={Path(p['path']).name:table[p['path']] for p in formal['formal_inputs']}
    copy_origin_names={'axial_macro.xsm':'initial_axial_macrolib.xsm','axial_track.xsm':'initial_axial_track.xsm','basis.xsm':'basis_reference.xsm'}
    names=['initial_pack.xsm','axial_macro.xsm','axial_track.xsm','basis.xsm']
    candidates=[];proofs=[];retained_causes=[]
    for version in ('v5','v6'):
        branch=ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+version)
        sp=s.pin(branch/'Root_actual_three_plane_engineering_summary.json');summary=s.exact_json(sp)
        s.check(summary['status']=='FAILED_UNQUALIFIED_NO_RETRY' and summary['failure']=='RuntimeError: only genuine completed guarded Dragon permits scratch archival' and summary['after_check_error'] is None and summary['actual_terminal'] is None and len(summary['records'])==33 and summary['engineering_three_plane_closed0'] is False,'actual failed aggregate unchanged')
        records={r['label']:r for r in summary['records']}
        s.check(records['AAA/pack']['status']=='PASS' and records['AAA/initial_positive']['status']=='PASS' and summary['records'][-1]['label']=='AAA/global_positive' and summary['records'][-1]['status']=='FAILED','PACK INITIAL individually pass, GLOBAL failed')
        tp=s.pin(REC/('ACTUAL_AAA3_PIPELINE_'+version.upper()+'_TRUE_TOOL_RETURNS_20261012.json'));tool=s.exact_json(tp)
        if version=='v5':
            terminal=tool['final'];s.check(tool['initial']['chunk_id']=='ce7fcf' and tool['session_id']==59834 and terminal['chunk_id']=='4e9522' and terminal['exit_code']==1,'v5 Root genuine closed exit1')
        else:
            terminal=tool['terminal'];s.check(tool['closed_observed'] is True and tool['original_integer_exit_code']==1 and tool['initial']['chunk_id']=='dd5093' and terminal['chunk_id']=='834ef7' and terminal['exit_code']==1,'v6 Root genuine closed exit1')
        watchdogs=[]
        for record in summary['records']:
            wp=s.pin(branch/(record['label']+'.watchdog.json'));w=s.exact_json(wp)
            lp=s.pin(branch/(record['label']+'.log'));s.same(lp)
            s.check(w['liveness_group_cleanup'] is True and w['own_child_only'] is True and w['command']==record['command'] and w['rss_cap_mib']==512,'old ownchild closure and original RSS cap evidence')
            if record['label']=='AAA/global_positive':
                reason="RuntimeError('own-child 512 MiB RSS cap reached')" if version=='v5' else "RuntimeError('own-child wall cap reached')"
                s.check(w['returncode']==-15 and w['limit_failure']==reason,'true stopped ownchild limit reason retained')
            else:
                s.check(w['returncode']==(0 if record['status']=='PASS' else 1) and w['limit_failure'] is None and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512,'preceding stages genuinely complete under original caps')
            watchdogs.append(dict(label=record['label'],status=record['status'],watchdog_pin=wp,log_pin=lp,actual_returncode=w['returncode'],limit_failure=w['limit_failure']))
        owner=s.pin(REC/('aaa_three_plane_streaming_pipeline_source_'+version)/'run_actual_three_plane_pipeline.py');s.same(owner)
        source=Path(owner['path']).read_text()
        s.check("('initial_axial_track.xsm','axial_track.xsm')" in source and "('initial_axial_macrolib.xsm','axial_macro.xsm')" in source and "('basis_reference.xsm','basis.xsm')" in source and "retain(WORK/n)" in source and "packed_readback(WORK/'initial_pack.xsm',plan)" in source,'literal own copy and own PACK production provenance')
        proof=s.pin(branch/'Root_actual_independent_three_plane_pack_readback.json');s.same(proof)
        old_outputs={p['path']:p for p in summary['output_pins']}
        for name in names:
            path=str(branch/'AAA'/name);actual=s.pin(path);old=old_outputs[path]
            s.check(actual['path']==old['path'] and actual['sha256']==old['sha256'] and actual['size_bytes']==old['size_bytes'] and actual['identity'][1:]==old['identity'][1:] and old['identity'][0] in (16777234,16777229) and actual['identity'][0]==16777229,'candidate exact saved output fullEOF and only historical device transition')
            s.check(actual['identity'][3]==1 and path not in protected_paths and tuple(actual['identity'][:2]) not in protected_inodes,'candidate owned nlink1 disjoint from every current input path/inode')
            s.same(actual)
            origin=None
            if name in copy_origin_names:
                origin=originals[copy_origin_names[name]]
                s.check(actual['sha256']==origin['sha256'] and actual['size_bytes']==origin['size_bytes'] and actual['identity'][:2]!=origin['identity'][:2],'private full byte copy distinct from still protected original producer')
            candidates.append(dict(current_fullpin=actual,historical_failed_summary_output_pin=old,private_role='CLOSED_FAILED_OVERALL_RUN_INITIAL_PACK_PRODUCED_FROM_INDEPENDENT_NATIVE_INPUTS' if name=='initial_pack.xsm' else 'CLOSED_FAILED_OVERALL_RUN_PRIVATE_FORMAL_INPUT_BYTE_COPY',original_protected_fullpin=origin,all_current_protected_paths_and_inodes_disjoint=True,release_recommendation='ELIGIBLE_ONLY_AFTER_ROOT_RECHECKS_CURRENT_DAG_AND_V9_TRUE_TERMINAL_NO_EXECUTION_AUTHORIZATION_HERE',old_raw_replay_unavailable_after_future_release=True,individual_PACK_INITIAL_PASS_not_reclassified_as_invalid=True))
        for name in ['global.xsm','ax_current.xsm','initial_system.xsm']:
            row=s.pin(branch/'AAA'/name);s.same(row);retained_causes.append(dict(current_fullpin=row,decision='KEEP_CAUSAL_FAILED_GLOBAL_OR_INITIAL_STATE_EVIDENCE'))
        proofs.append(dict(version=version,failed_overall_summary_pin=sp,Root_true_closed_exit1_tool_pin=tp,actual_owning_Source_pin=owner,independent_native_PACK_readback_pin=proof,all33_actual_child_closure_and_log_pins=watchdogs,PACK_INITIAL_individual_PASS_preserved=True,GLOBAL_FAILED_under_original_ownchild_caps=True,producer_math_or_input_invalidity_not_inferred=True))
    total=sum(p['current_fullpin']['size_bytes'] for p in candidates)
    s.check(total==998909696 and len(candidates)==8,'exact finite eight recommendation bytes')
    release=s.exact_json(s.pin(pk/'ACTUAL_EXACT_TWO_PROJECT_PRIVATE_COPY_RELEASE_RECEIPT.json'))
    baseline=release['original_budget_after']['remaining_after_original_initial_reserves_bytes']
    s.check(baseline==1251926357,'actual previous release original admission baseline')
    current=s.budget_snapshot()
    projected_worst=baseline-2*2**30+total
    s.check(projected_worst==103352405,'original full fresh bounded maximum forecast arithmetic')
    for row in s.VERIFIED.values():s.check(s.seven(Path(row['path']).lstat())==row['identity'],'all fullEOF files remained stable at terminal audit')
    result=dict(schema='READONLY_FINITE_FAILED_V5_V6_PRIVATE_COPY_CANDIDATE_SURVEY_V1',status='CURRENT_FULL_EOF_CANDIDATES_DISJOINT_PROVISIONAL_NO_RELEASE',deletion_executed=False,compiler_or_numerical_business_executed=False,final_release_manifest_published=False,v9_terminal_claimed_or_prefilled=False,goal_complete=False,
        prior_actual_current_protection_manifest_pin=mp,helper_readonly_Source_pin=s.pin(HELPER),reviewer_Source_pin=s.pin(Path(__file__).absolute()),all_prior4390_protected_pins_fullEOF_reverified=True,
        current_protected_union_unique_files=len(table),current_catalog_rows=3040,current_catalog_unique_paths=len({r['current_pin']['path'] for r in catalog['rows']}),current_Common_rows=2012,saved_science_current_rows=3315,saved_science_original_inputs=1129,current_v9_HF_dependencies=257,
        new_current70_material_Source_files=material_files,new_current70_material_live_dependency_fullpins=sorted({p['path']:p for p in material_origins}.values(),key=lambda p:p['path']),explicit_material_only_device_reattestations=explicit_device_events,absent_material_referenced_paths_not_claimed_live=sorted(set(absent_referenced_paths)),
        candidates=candidates,candidate_count=8,total_candidate_logical_bytes=total,closed_failed_v5_v6_proofs=proofs,causal_small_outputs_kept=retained_causes,
        original_case_math_caps_thresholds_and_results_preserved=True,sourcefactor005006_not_needed_or_reclassified_as_failed=True,
        next_savedscience_fullfresh_forecast=dict(actual_previous_release_after_initial_reserves_bytes=baseline,v9_unchanged_fullfresh_retained_upper_bound_bytes=2*2**30,candidate_eight_logical_bytes=total,worst_case_remaining_bytes_after_v9_max_and_candidates=projected_worst,only_two_PACK_bytes=941282016,only_two_PACK_worst_remaining_bytes=45724725,next_savedscience_fullfresh2GiB_already_in_original_reserve=True,condition='NO_OTHER_ART_HISTORY_GROWTH_AFTER_BASELINE_AND_V9_FRESH_2GIB_CAP_RETAINS_NO_MORE_THAN_THIS_BOUND',not_actual_future_admission=True,Root_must_measure_real_history_and_v9_terminal_before_any_manifest_or_release=True,current_concurrent_history_observation=current),
        full_EOF_unique_verified_files=len(s.VERIFIED),full_EOF_unique_verified_bytes=sum(p['size_bytes'] for p in s.VERIFIED.values()),checks=s.CHECKS,elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path=OUT/'FINITE_EIGHT_FAILED_PRIVATE_COPY_CANDIDATE_REVIEW.json'
    raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],report_pin=s.pin(path),candidate_count=8,candidate_logical_bytes=total,protected_union_files=len(table),full_EOF_unique_files=len(s.VERIFIED),full_EOF_unique_bytes=result['full_EOF_unique_verified_bytes'],checks=result['checks'],bounded_worst_case_remaining_bytes=projected_worst,deletion_executed=False)))

if __name__=='__main__':main()

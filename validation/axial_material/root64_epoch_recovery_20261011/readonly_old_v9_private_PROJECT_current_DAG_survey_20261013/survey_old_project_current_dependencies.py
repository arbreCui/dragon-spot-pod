"""One candidate survey only. Historical output lists are not live input DAGs."""
import importlib.util
import json
import os
from pathlib import Path
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';OUT=Path(__file__).absolute().parent
H=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
spec=importlib.util.spec_from_file_location('fixed_original_readonly_pin_and_budget_helpers',H);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
V9=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9';V10=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10';TARGET=V9/'AAA/projected_boot.xsm';START=time.monotonic()
TABLE={};ROLES={};EVENTS=[];ORIGINS=[]

def add(row,role):
    old=s.norm(row);actual=s.pin(old['path'])
    if old!=actual:
        if old['sha256']!=actual['sha256'] or old['size_bytes']!=actual['size_bytes'] or old['identity'][0]!=16777234 or actual['identity'][0]!=16777229 or old['identity'][1:]!=actual['identity'][1:]:raise RuntimeError('live input changed beyond exact declared current device')
        EVENTS.append(dict(historical_pin=old,current_pin=actual,only_device_field_changed=True))
    known=TABLE.get(actual['path'])
    if known is not None and known!=actual:raise RuntimeError('ambiguous current input fullpin')
    TABLE[actual['path']]=actual;ROLES.setdefault(role,set()).add(actual['path']);return actual

def metadata(path,role):
    pin=add(s.pin(path),role);value=s.read(pin);ORIGINS.append(dict(role=role,pin=pin));return value

def fixed(values,role):
    for row in s.nested(values):add(row,role)

def Source_package(path,role):
    entries=sorted(str(p) for p in path.rglob('*') if p.is_file())
    for name in entries:
        pin=add(s.pin(name),role)
        if Path(name).suffix=='.json':
            # These are source packages/frozen input plans, not old numerical
            # run summaries. Their declared input/source fullpins stay live.
            value=s.read(pin);fixed(value,role+'_declared_actual_Source_input_pins')
    if entries!=sorted(str(p) for p in path.rglob('*') if p.is_file()):raise RuntimeError('current Source package still changing')

def main():
    cat=metadata(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json','current_catalog_file')
    if len(cat['rows'])!=3040:raise RuntimeError('all current3040 catalog rows')
    for row in cat['rows']:add(row['current_pin'],'all3040_current_catalog_rows')
    common=metadata(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json','current_Common_BIND')
    if len(common['fixed_current_pins'])!=2012:raise RuntimeError('all current2012 Common pins')
    fixed(common['fixed_current_pins'],'all2012_Common_pins')
    science=metadata(REC/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json','saved_science_current_BIND')
    if len(science['fixed_current_pins'])!=3315 or len(science['science_original_input_pins'])!=1129:raise RuntimeError('all current science3315/1129')
    fixed(science['fixed_current_pins'],'saved_science3315');fixed(science['science_original_input_pins'],'saved_science1129')
    hf=metadata(REC/'aaa_three_plane_streaming_pipeline_source_v10/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json','current_v10_HF')
    if len(hf['dependencies'])!=278:raise RuntimeError('all278 current v10 dependencies')
    fixed([hf['host_source']]+hf['dependencies'],'current_v10_HF278_and_host')
    build=s.read(add(hf['selected_actual_build70_report'],'current_actual70_report'))
    fixed(build['fixed_current_pins'],'current70_fixed_inputs');fixed(build['output_pins'],'current70_actual_outputs')
    Source_package(REC/'current_formal_material_authority_exact_cache70_source_v6','current_material_v6_full_Source')
    Source_package(REC/'current_eleven_saved_gendf_current_mount_host_source_v4','current_GENDF_v4_full_Source')
    Source_package(REC/'reaction_genDF_current_mount_stream_source_v2','current_GENDF_parser_v2_full_Source')
    ref=REC/'full370_unreduced_eigen_reference_source_v2'
    for p in sorted(ref.iterdir()):add(s.pin(p),'independent_reference_v2_complete_Source')
    plan=metadata(ref/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json','independent_reference_actual_fixed_input_plan')
    fixed([plan[k] for k in ('protected_formal_and_producer_plan_pin','current_case_spec_pin','current_prepared_pin','current_axial_track_pin','additional_current_input_pins')],'independent_reference_actual_fixed_inputs')
    formal=s.read(add(plan['protected_formal_and_producer_plan_pin'],'protected_formal_producer_input_plan'))
    fixed(formal['formal_inputs'],'all_formal_original_inputs')
    for producer in formal['producers']:
        fixed([producer[k] for k in ('report','archive','radial_binary_track')],'all_three_native_producer_actual_inputs')
    # Do not recurse either old failure summary.output_pins into current DAG.
    sp=s.pin(V9/'Root_actual_three_plane_engineering_summary.json');summary=s.read(sp)
    tp=s.pin(REC/'ACTUAL_PIPELINE_V9_AFTER_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS_20261013.json');tool=s.read(tp)
    if summary['status']!='FAILED_UNQUALIFIED_NO_RETRY' or summary['engineering_three_plane_closed0'] is not False or summary['after_check_error'] is not None or len(summary['records'])!=42 or tool['observed_closed'] is not True or tool['original_integer_exit_code']!=1 or tool['terminal']['exit_code']!=1:raise RuntimeError('true oldv9 failed overall closure required')
    selected={r['label']:r for r in summary['records']}
    if selected['AAA/global_positive']['status']!='PASS' or selected['AAA/project_positive']['status']!='PASS' or summary['records'][-1]['label']!='AAA/view_memory_output':raise RuntimeError('preserve v9 GLOBAL PROJECT PASS vs failedBOOT')
    closures=[]
    for record in summary['records']:
        wp=s.pin(V9/(record['label']+'.watchdog.json'));w=s.read(wp);lp=s.pin(V9/(record['label']+'.log'))
        if w['liveness_group_cleanup'] is not True or w['own_child_only'] is not True or type(w['returncode']) is not int or w['command']!=record['command']:raise RuntimeError('all oldv9 owned children true terminal')
        if record['status']=='PASS' and (w['returncode']!=0 or w['limit_failure'] is not None or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512):raise RuntimeError('v9 successful stages original caps')
        closures.append(dict(label=record['label'],status=record['status'],watchdog_pin=wp,log_pin=lp,actual_exit_code=w['returncode']))
    target=s.pin(TARGET);declared=next(p for p in summary['output_pins'] if p['path']==str(TARGET))
    if target!=declared or target['identity'][3]!=1 or target['size_bytes']!=749355952:raise RuntimeError('exact owned private projected artifact authority')
    paths=[role for role,values in ROLES.items() if str(TARGET) in values]
    aliases=[p for p in TABLE.values() if tuple(p['identity'][:2])==tuple(target['identity'][:2])]
    direct_role_absence=not paths and not aliases
    # Pin old documents/other outputs as retained survey evidence; classification
    # is retained history, not a reason to classify PROJECT as mandatory input.
    retained=[s.pin(p) for p in sorted(V9.rglob('*')) if p.is_file() and p!=TARGET]
    v10sp=s.pin(V10/'Root_actual_three_plane_engineering_summary.json');v10=s.read(v10sp);v10tp=s.pin(REC/'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json');v10t=s.read(v10tp)
    if v10t['observed_closed'] is not True or v10t['original_integer_exit_code']!=1 or v10t['terminal']['exit_code']!=1 or v10['engineering_three_plane_closed0'] is not False or v10['output_pins']!=[]:raise RuntimeError('v10 actual SELFcap failed unqualified closure remains intact')
    budget=s.budget();conditional=budget['remaining_after_original_initial_reserves_bytes']+749355952
    host=Path(hf['host_source']['path']).read_text()
    if str(TARGET) in host:raise RuntimeError('current owning host directly refers to old absolute project')
    for needle in ["WORK=OUT/'AAA'","'projected_boot.xsm'","data.transfer_readback(WORK/'projected_boot.xsm'","copy(row['archive'],'native_A'"]:
        if needle not in host:raise RuntimeError('actual current own fresh workspace/input path Source proof absent '+needle)
    for row in list(TABLE.values())+[target,sp,tp,v10sp,v10tp]+retained:s.same(row)
    result=dict(schema='READONLY_SINGLE_OLD_V9_PROJECT_CURRENT_MANDATORY_DAG_SURVEY_V1',status='SINGLE_PRIVATE_CANDIDATE_DISJOINT_CURRENT_INPUT_DAG_NO_RELEASE' if direct_role_absence else 'CANDIDATE_PROTECTED_CURRENT_INPUT_NOT_ELIGIBLE',candidate_current_full_EOF_pin=target,candidate_original_failed_v9_summary_output_pin=declared,current_mandatory_path_roles_for_candidate=paths,current_mandatory_same_inode_pins=aliases,current_mandatory_unique_files=len(TABLE),all3040_catalog_rows_all2012_Common_all3315_science_1129_original_inputs_and_current_v10_HF278_included=True,current_material_v6_GENDF_v4_parser_v2_reference_fixed_inputs_all_included=True,current_mandatory_complete_pins=sorted(TABLE.values(),key=lambda p:p['path']),selected_current_metadata_origins=ORIGINS,roles={k:sorted(v) for k,v in ROLES.items()},explicit_current_device_only_events=EVENTS,old_v9_true_failed_overall_summary_pin=sp,old_v9_true_Root_exit1_tool_pin=tp,all42_oldv9_actual_closed_stage_proofs=closures,GLOBAL_PROJECT_individual_PASS_preserved=True,old_BOOT_not_qualified=True,current_v10_true_failed_summary_pin=v10sp,current_v10_true_Root_exit1_tool_pin=v10tp,v10_failed_SELFcap_outputs_not_promoted=True,all_other_v9_ordinary_file_pins_retained=retained,old_exact8_manifest_protected_outputs_were_historical_cleanup_snapshot_not_permanent_current_inputs=True,old_closed_summaries_fulloutput_pins_not_recursively_promoted_to_current_DAG=True,release_would_remove_old_v9_full_PROJECT_and_retained_GLOBAL_tree_raw_replay=True,producer_and_formal_current_final_raws_retained=True,current_budget=budget,conditional_original_full_initial_reserve_after_one_release_bytes=conditional,conditional_is_not_actual_release_result=True,v11_future_current_DAG_must_be_rechecked_after_real_freeze=True,v11_future_Source_or_PF_not_predicted=True,deletion_executed=False,final_manifest_frozen_or_published=False,compiler_or_business_executed=False,goal_complete=False,elapsed_seconds=time.monotonic()-START,reviewer_Source_pin=s.pin(Path(__file__).absolute()))
    path=OUT/'SINGLE_V9_PROJECT_CURRENT_DAG_AND_BUDGET_READONLY_REVIEW.json';s.write_new(path,result)
    print(json.dumps(dict(status=result['status'],review_pin=s.pin(path),candidate_pin=target,current_mandatory_unique_files=len(TABLE),current_ART_bytes=budget['artifact_bytes'],current_regular_files=budget['regular_files'],current_original_initial_reserve_bytes=budget['remaining_after_original_initial_reserves_bytes'],conditional_after_single_release_reserve_bytes=conditional,deletion_executed=False,final_manifest_published=False)))

if __name__=='__main__':main()

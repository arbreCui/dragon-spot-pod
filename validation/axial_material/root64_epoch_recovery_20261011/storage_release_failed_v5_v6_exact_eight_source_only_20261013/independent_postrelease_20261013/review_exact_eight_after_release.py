"""Postrelease readonly audit. No cleanup/preparation imports or candidate reads."""
import importlib.util
import json
import os
from pathlib import Path
import resource
import time

PKG=Path(__file__).absolute().parent.parent;OUT=Path(__file__).absolute().parent
REVIEW_HELPER=PKG/'independent_final_manifest_review_20261013/review_full_current_manifest.py'
spec=importlib.util.spec_from_file_location('own_readonly_inventory_helpers',REVIEW_HELPER);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
s=h.s;REC=h.REC;ART=h.ART;TARGETS=h.PATHS;START=time.monotonic()

def main():
    mp=dict(path=str(PKG/'EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_MANIFEST.json'),sha256='ff41720ece425f35ad1a19e788d5c95354e94e5c3f3804421958a24198519ee4',size_bytes=4365208,identity=[16777229,50013100,33188,1,4365208,1791870085838502446,1791870085838502446])
    m=s.exact_json(mp)
    tp=s.pin(PKG/'ROOT_ACTUAL_EXACT_EIGHT_RELEASE_TRUE_TOOL_RETURNS.json');tool=s.exact_json(tp)
    s.check(tool['observed_closed'] is True and tool['original_integer_exit_code']==0 and tool['terminal']['exit_code']==0 and tool['initial']['chunk_id']=='53b61f' and tool['initial']['session_id']==59401 and tool['terminal']['chunk_id']=='3ce611','genuine Root exact8 closed exit0')
    printed=json.loads(tool['terminal']['output']);rp=printed['receipt_pin']
    s.check(rp['path']==str(PKG/'ACTUAL_EXACT_EIGHT_RELEASE_RECEIPT.json') and rp['sha256']=='bbcc9a7ecaddb95f49b050a4f4a79fc45ab41afba682d6d14111b791ae35788e' and rp['identity']==[16777229,50013549,33188,1,363033,1791870263257314745,1791870263257761413],'actual terminal externally selected release fullPF')
    r=s.exact_json(rp)
    s.check(r['status']=='EXACT_EIGHT_PRIVATE_COPY_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED' and r['manifest_pin']==mp and r['execute_requested'] is True and r['deleted_files']==8 and r['logical_bytes_released']==998909696,'true exacteight successful cleanup receipt')
    s.check(r['compiler_or_numerical_business_executed'] is False and r['goal_complete'] is False and tool['no_numerical_business_executed'] is True,'no science/goal success inferred from cleanup')
    targets=m['target_full_EOF_pins'];s.check([p['path'] for p in targets]==TARGETS and sum(p['size_bytes'] for p in targets)==998909696,'literal eight declared original identities')
    s.check(r['deletion_records']==[dict(original_fullpin=p,confirmed_absent=True) for p in targets],'exact actual eight persistent action records')
    for path in TARGETS:s.check(not os.path.lexists(path),'released target remains absent')
    protected=m['current_protected_full_EOF_pins'];retained=m['retained_ordinary_full_EOF_pins'];table={p['path']:p for p in protected}
    s.check(len(protected)==4769 and len(table)==4769 and len(retained)==372,'complete final protected/retained cardinalities')
    inodes={tuple(p['identity'][:2]) for p in protected}
    s.check(all(p['identity'][3]==1 and p['path'] not in table and tuple(p['identity'][:2]) not in inodes for p in targets),'target original private identities disjoint from full current union')
    for row in protected+retained+m['Source_pins']+[m['selected_complete_Source_only_freeze_pin']]:s.same(row)
    sf=s.exact_json(m['selected_complete_Source_only_freeze_pin'])
    s.check(sf['Source_pins']==m['Source_pins'],'frozen3 Source identical and unchanged')
    for row in [sf['external_readonly_helper_pin'],sf['readonly_candidate_survey_pin'],sf['required_interface_source_only_pin'],sf['actual_Source_only_protection_preflight_tool_pin']]:s.same(row)
    before=m['complete_before_inventory'];after=h.old_inventory();expected={p:i for p,i in before['ordinary_file_identities'].items() if p not in TARGETS}
    s.check(len(before['ordinary_file_identities'])==380 and after['ordinary_file_identities']==expected and len(expected)==372,'complete old branch exact eight regular entry delta')
    s.check(after['symlinks']==before['symlinks'] and set(after['directory_identities'])==set(before['directory_identities']),'all link entries and every directory presence unchanged')
    changes={p['path']:p for p in r['observed_parent_directory_changes']};parents={str(Path(p).parent) for p in TARGETS}
    s.check(set(changes)==parents,'exact two affected parent directories')
    for path,old in before['directory_identities'].items():
        new=after['directory_identities'][path]
        if path in parents:
            observed=changes[path]
            s.check(old==observed['before_seven_id'] and new==observed['after_seven_id'] and new[:3]==old[:3] and observed['ordinary_entry_delta']==-4 and observed['all_other_file_link_entries_exact'] is True,'parent native metadata exact real receipt not an assumed APFS rule')
        else:s.check(new==old,'unaffected directory all7ID unchanged')
    for branch in h.BRANCHES:
        for name in ['global.xsm','ax_current.xsm','initial_system.xsm']:s.check(str(branch/'AAA'/name) in expected,'all failed GLOBAL/INITIAL small causal raw retained')
    v9=s.exact_json(m['selected_actual_v9_summary_pin']);v9t=s.exact_json(m['selected_actual_v9_true_tool_receipt_pin'])
    s.check(v9t['observed_closed'] is True and v9t['original_integer_exit_code']==1 and v9t['terminal']['exit_code']==1 and v9['status']=='FAILED_UNQUALIFIED_NO_RETRY' and v9['engineering_three_plane_closed0'] is False and len(v9['records'])==42,'actual v9 failedBOOT scope and true closure retained')
    selected={p['label']:p for p in v9['records']};s.check(selected['AAA/global_positive']['status']=='PASS' and selected['AAA/project_positive']['status']=='PASS' and v9['records'][-1]['label']=='AAA/view_memory_output','v9 GLOBAL PROJECT pass and final lexical failure remain distinct')
    for row in v9['output_pins']:s.check(table[row['path']]==row,'every actual v9 output exactly protected and verified EOF')
    closure=m['Source_DAG_provenance']['actual_closed_v9_protection'];s.check(len(closure['all_actual_v9_stage_closures'])==42,'all42 real v9 child records retained')
    for row in closure['all_actual_v9_stage_closures']:
        w=s.exact_json(row['watchdog_pin']);s.same(row['log_pin']);s.check(w['liveness_group_cleanup'] is True and w['own_child_only'] is True and w['returncode']==row['actual_returncode'],'v9 true own child closures unchanged')
    for proof in m['closed_failed_overall_v5_v6_run_proofs']:
        d=s.exact_json(proof['failed_overall_summary_pin']);t=s.exact_json(proof['Root_true_closed_exit1_tool_pin']);terminal=t['final'] if proof['version']=='v5' else t['terminal']
        s.check(terminal['exit_code']==1 and d['status']=='FAILED_UNQUALIFIED_NO_RETRY' and d['engineering_three_plane_closed0'] is False and len(d['records'])==33,'old failed aggregate remains truthful historical evidence after private raws unavailable')
        records={row['label']:row for row in d['records']};s.check(records['AAA/pack']['status']=='PASS' and records['AAA/initial_positive']['status']=='PASS','old individual PACK INITIAL pass retained')
        for row in proof['all33_actual_child_closure_and_log_pins']:
            w=s.exact_json(row['watchdog_pin']);s.same(row['log_pin']);s.check(w['liveness_group_cleanup'] is True and w['own_child_only'] is True and w['returncode']==row['actual_returncode'] and w['limit_failure']==row['limit_failure'],'all66 historical ownchild closures and actual stops unchanged')
    for ns in m['Source_DAG_provenance']['additional_exact_current_source_namespaces']:
        entries=sorted(str(p) for p in Path(ns['namespace']).rglob('*') if p.is_file());wanted=ns['all_current_Source_and_metadata_full_EOF_pins']
        s.check(entries==sorted(p['path'] for p in wanted),'entire actual current material/GENDF Source directory remains unchanged')
        for row in wanted:s.check(table[row['path']]==row,'every current Source file protected EOF')
    previous,current=r['original_budget_before'],r['original_budget_after']
    s.check(previous['artifact_bytes']-current['artifact_bytes']==998909696 and previous['regular_files']-current['regular_files']==8,'actual true logical history delta exact8/998909696B')
    for budget in (previous,current):
        reserve=96*2**30-budget['artifact_bytes']-20971764748-64*2**20-2*2**30
        s.check(budget['artifact_budget_bytes']==96*2**30 and budget['min_free_bytes']==8*2**30 and budget['disk_free_bytes']>=8*2**30 and budget['remaining_after_original_initial_reserves_bytes']==reserve and budget['original_initial_reserve_admitted']==(reserve>0),'original fresh/cold/metadata/history/free budget unchanged arithmetic')
    s.check(current['remaining_after_original_initial_reserves_bytes']==1400568829,'actual original complete reserve postrelease value')
    observation=s.budget_snapshot();observation['v9_output_retained_exists']=observation.pop('concurrent_v9_output_exists');observation['v10_output_namespace_exists_at_observation']=os.path.lexists(ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10');observation['interpretation']='CURRENT_HISTORY_OBSERVATION_NOT_A_CLEANUP_EXACT_DELTA_AUTHORITY_NEW_BUSINESS_OUTPUT_IF_ANY_IS_CONCURRENT_GROWTH'
    for row in s.VERIFIED.values():s.check(s.seven(Path(row['path']).lstat())==row['identity'],'all EOF files exact at audit terminal')
    result=dict(schema='INDEPENDENT_READONLY_EXACT_EIGHT_POSTRELEASE_FULL_EOF_REVIEW_V1',status='ALL4769_PROTECTED372_RETAINED_EXACT8_ABSENT_POSTRELEASE_PASS',manifest_pin=mp,Root_true_actual_closed0_tool_pin=tp,actual_release_receipt_pin=rp,protected_count=4769,retained_count=372,targets_absent=TARGETS,deleted_count=8,deleted_logical_bytes=998909696,complete_old_branch_directory_count=len(after['directory_identities']),all_other_file_link_directory_entries_exact=True,parent_APFS_metadata_matches_real_receipt=True,all_actual_v9_outputs_preserved=True,old_individual_PACK_INITIAL_and_v9_GLOBAL_PROJECT_PASS_preserved=True,old_failed_aggregate_and_BOOT_nonqualification_preserved=True,old_private_v5_v6_raw_replay_unavailable=True,original_caps_physics_inputs_math_thresholds_unchanged=True,actual_original_budget_after_reserve_bytes=1400568829,current_history_observation=observation,deletion_or_preparation_host_called=False,compiler_or_numerical_business_executed=False,goal_complete=False,full_EOF_unique_verified_files=len(s.VERIFIED),full_EOF_unique_verified_bytes=sum(p['size_bytes'] for p in s.VERIFIED.values()),full_EOF_verified_pins=sorted(s.VERIFIED.values(),key=lambda p:p['path']),checks=s.CHECKS,elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,reviewer_Source_pin=s.pin(Path(__file__).absolute()))
    path=OUT/'INDEPENDENT_EXACT_EIGHT_POSTRELEASE_FULL_EOF_REVIEW.json';raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=s.pin(path),protected_count=4769,retained_count=372,full_EOF_files=result['full_EOF_unique_verified_files'],full_EOF_bytes=result['full_EOF_unique_verified_bytes'],checks=result['checks'],original_actual_reserve_after_bytes=1400568829,deletion_executed_by_review=False)))

if __name__=='__main__':main()

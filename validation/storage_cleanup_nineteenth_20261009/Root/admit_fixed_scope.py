from pathlib import Path
import json, hashlib, runpy

OUT = Path('/private/tmp/spot_storage_nineteenth_root_20261009')
helpers = runpy.run_path(str(OUT/'prepare_review.py'), run_name='pure_metadata_helpers_only')
sha, identity = helpers['sha'], helpers['identity']
G = Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009')
S = Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009')
P = Path('/private/tmp/spot_storage_nineteenth_AAA_early_snapshots_preservation_review_20261009')

def load(path, expected=None):
    if expected:
        assert sha(path) == expected, str(path)
    return json.loads(path.read_text())

def zero(r, outer_closed=False):
    a = r['actual_tool_result']
    assert type(a['exit_code']) is int and a['exit_code'] == 0
    assert a.get('closed') is True or r.get('closed') is True or (outer_closed and r.get('status') == 'CLOSED')
    return a

def main():
    plan_sha = 'b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
    plan = load(OUT/'fixed_candidate_plan.json', plan_sha)
    graph = load(G/'REPORT.json', '0473a770f97ecd65ef066aef12729478932d784c7aa4f22e42b138e46491e960')
    full = load(G/'EXACT_FIXED_PLAN_FULLSHA_REPORT.json', '055ce01dc5fb246996171a49e10a808f52d9116cc75add05f6c938c8d9a8e462')
    source = load(S/'REPORT.json', 'f055e095769fe065a11b24cf3b29693d8bc887c485da39495964ff2f7af7d6cf')
    preserve = load(P/'REPORT.json', '5d37e70f47df6065539721a9ca3f432afe7283fc797dc1e7cff5777ff8e13ae9')
    receipts = {
        'current_graph': zero(load(G/'CURRENT_INDEX_READONLY_ACTUAL_TOOL_RETURN.json')),
        'fixed_fullSHA': zero(load(G/'EXACT_PLAN_FULLSHA_ACTUAL_TOOL_RETURN.json', '8f35e5f1b7020f6b25248176dc17628ccef588dff7fe71bbb33e781563592229')),
        'current_native_source': zero(load(S/'actual_readonly_tool_return.json', '49d955a57998d043c225e3023ae691a79de37585bd43f0b06400120c3bdff1bb'), True),
        'old_result_preservation': zero(load(P/'actual_readonly_tool_return.json', '7a29d23591ee68c25432e5892ded97c15a7252e2bb21694507a347b0d734e58c')),
    }
    assert not graph['current_blockers'] and not graph['unknown_family_incoming_symlinks']
    assert graph['resource_membership_is_live_capacity_gate_not_frozen_payload_inventory'] is True
    for key in ['fresh_candidate_fullSHA_original_SEALED_STAGE_OUTPUTS_equal', 'full_candidate_seven_identity_before_after_equal', 'related_symlink_literal_identity_and_target_exact', 'current37395_canon35647_ns86_alias186_absence445_exact_excluded', 'last_three_closed_states_unchanged']:
        assert full[key] is True
    assert source['status'] == preserve['status'] == 'PASS'
    assert source['fixed_candidate_plan']['sha256'] == preserve['plan']['sha256'] == plan_sha
    selected = {x['path'] for x in plan['regular']+plan['symlinks']}
    assert set(source['candidate_paths']) == selected
    assert not source['candidate_specific_blockers'] and not source['resolved_candidate_alias_hits'] and not source['candidate_regular_device_inode_hits']
    assert all(not value['exact_candidate_path_hits'] for value in source['exact_path_checks'].values())
    assert source['fresh_native_parent_induction']['historical_candidate_result_seals_read_by_current_run'] is False
    assert set(preserve['fixed_regular_paths']) == {x['path'] for x in plan['regular']}
    assert set(preserve['fixed_symlink_paths']) == {x['path'] for x in plan['symlinks']}
    assert not preserve['prior_exact_copy_restore_master_intersections']
    assert preserve['all_map_results_and_logs_fullSHA_checked'] is True
    assert preserve['independent_accuracy_pass_inferred'] is False
    pins = list(graph['full_small_metadata_and_source_pins'].values()) + list(source['full_metadata_and_source_pins'].values()) + preserve['all_fresh_small_metadata_and_source_pins']
    unique = {}
    for row in pins:
        path = Path(row['path'])
        assert sha(path) == row['sha256'], ('source or metadata changed', str(path))
        if 'identity' in row:
            assert identity(path) == row['identity'], ('source or metadata identity changed', str(path))
        unique[str(path)] = row['sha256']
    result = {'status': 'READY_FOR_EXACT_18_OLD_STATES_AND_18_LINK_RETIREMENT_ONLY', 'plan_sha256': plan_sha, 'independent_actual_closed_exit0_tools': receipts, 'distinct_fresh_source_metadata_SHA_count': len(unique), 'current_explicit_namespace_alias_native_source_dependencies_excluded': True, 'global_incoming_symlinks_exactly_fixed_18': True, 'old_result_logs_and_prior_copy_restore_master_preservation_proven': True, 'historical_full_seals_not_asserted_currently_complete': True, 'scientific_source_inputs_thresholds_progress_modified': False, 'business_executed': False, 'scientific_qualification': False}
    (OUT/'Root_pre_retirement_joint_review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()

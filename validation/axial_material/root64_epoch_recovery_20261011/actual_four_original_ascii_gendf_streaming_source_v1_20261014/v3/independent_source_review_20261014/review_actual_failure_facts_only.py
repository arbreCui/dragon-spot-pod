"""Sole post-review of retained failed runtime facts; no payload read or rerun."""
import json
import os
from pathlib import Path
from review_source_only import BASE, CAPS, FLAGS, current, full, new, pin, read, require


def main():
    p_tools = pin(BASE / 'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')
    tools = read(p_tools)
    raw = tools['actual_terminal_return']
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int
            and tools['original_integer_exit_code'] == 1 and type(raw['exit_code']) is int and raw['exit_code'] == 1
            and raw.get('session_id') is None and tools['actual_initial_return']['session_id'] == 53817
            and 'RuntimeError: own-child stage failed; no retry' in raw['output'], 'original Root session53817 actual typed closed1 retained')
    ready = read(pin(BASE / 'SOURCE_REVIEW_READY.json'))
    plan = read(ready['control_plan_pin'])
    cli = read(pin(BASE / 'FINAL_ROOT_REVIEWABLE_CLI.json'))
    out = Path(plan['planned_actual_output_root'])
    p_summary = pin(out / 'Root_actual_four_original_ASCII_GENDF_summary.json')
    summary = read(p_summary)
    require(summary['schema'] == 'ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_GUARDED_REPORT_V1'
            and summary['status'] == 'FAILED_FOUR_ORIGINAL_ASCII_NO_RETRY'
            and summary['failure'] == "RuntimeError('own-child stage failed; no retry')"
            and summary['secondary_failures'] == [] and summary['actual_child_receipt'] is None
            and summary['actual_evidence'] is None and summary['actual_watchdog_checks'] == []
            and summary['original_caps'] == CAPS and summary['original_guard_MRO_unchanged'] is True
            and summary['source_freeze_pin'] == cli['source_freeze_pin']
            and summary['host_freeze_pin'] == cli['host_freeze_pin']
            and summary['actual_precise_retirement_receipt_pin'] == plan['actual_precise_retirement_receipt_pin']
            and summary['final_report_resource_check_passed'] is True
            and summary['native_engines_started'] == 0 and summary['original_ASCII_files_written'] == 0,
            'actual failed owning report exact final bindings, no actual completed science evidence')
    for p in summary['fixed_current_pins'] + summary['complete_output_pins']:
        full(p)
    require(len(summary['fixed_current_pins']) == 161 and len(summary['complete_output_pins']) == 5
            and {str(p) for p in out.rglob('*') if p.is_file()}
                == {p['path'] for p in summary['complete_output_pins']} | {p_summary['path']}, 'all actual six output files EOF/current7 accounted')
    require(len(summary['records']) == 1 and summary['records'][0]['status'] == 'FAILED', 'one failed actual child, no retry')
    record = summary['records'][0]
    require(record['label'] == 'gendf-stage/four_original_ASCII_fullEOF_inventory'
            and len(record['command']) == 7 and record['command'][:4]
                == ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '-B',
                    str(BASE / 'stream_four_original_ascii_gendf.py'), '--binding-pin']
            and record['command'][5:] == ['--expected-parent-pid', '86903']
            and 0 < record['wall_cap_seconds'] <= 600, 'original actual failed child argv and cap')
    p_binding = json.loads(record['command'][4])
    binding = read(p_binding)
    require(p_binding in summary['complete_output_pins'] and binding['control_plan_pin'] == ready['control_plan_pin']
            and binding['source_freeze_pin'] == cli['source_freeze_pin']
            and binding['complete_joint_roots'] == plan['complete_joint_roots']
            and binding['original_caps'] == CAPS, 'actual once execution binding exactPF/current43/originalcaps')
    logpath = out / (record['label'] + '.log')
    p_log = pin(logpath)
    log = logpath.read_text()
    require(p_log in summary['complete_output_pins'] and p_log['sha256'] not in ('', record.get('log_sha256', ''))
            and "if mf==3:require(ng2==2,'original MF3 flux/reaction layout')" in log
            and 'line 88, in extract' in log and 'RuntimeError: original MF3 flux/reaction layout' in log,
            'actual complete failed child traceback, not completed stdout receipt')
    p_watch = pin(logpath.with_suffix('.watchdog.json'))
    watch = read(p_watch)
    require(p_watch in summary['complete_output_pins'] and type(watch['returncode']) is int
            and watch['returncode'] == 1 and watch['command'] == record['command']
            and type(watch['pid']) is int and watch['pid'] == 86906
            and watch['limit_failure'] is None and watch['rss_cap_mib'] == 512
            and 0 <= watch['sampled_peak_rss_mib'] < 512
            and 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= record['wall_cap_seconds'] <= 600
            and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True,
            'actual typed failed owning watchdog, no limit failure, original caps and cleanup')
    require(not any((out / 'inventories').iterdir()), 'no published complete inventories or child evidence')
    for snapshot in (summary['resources_before'], summary['resources_after'], summary['resources_after_including_summary_bytes']):
        require(snapshot['host_SELF_peak_bytes'] < 512 * 2**20 and snapshot['whole_elapsed_seconds'] < 1800
                and snapshot['complete_joint']['artifact_bytes'] + snapshot['explicit_external_metadata_bytes']
                    + snapshot['host_open_unlinked_bytes'] < 2 * 2**30
                and snapshot['original_history']['artifact_bytes'] + CAPS['cold_reserve_bytes']
                    + CAPS['metadata_reserve_bytes'] < CAPS['history_bytes'], 'retained actual failure resource checks fit original limits')
    require(all(summary[k] is False for k in ('scientific_accuracy_qualified', 'physics_qualified',
            'complete_reaction_authority_qualified', 'physical_neutron_balance_qualified', 'full_reference_qualified',
            'unreduced_reference_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete')), 'all actual failure qualifications false')
    for row in plan['inputs']:
        current(row['gzip_primary_current_full_pin'])
    retirement = read(plan['actual_precise_retirement_receipt_pin'])
    require(all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']), 'only precise original retired four spool paths absent')
    for p in summary['complete_output_pins'] + [p_summary, p_tools]:
        current(p)
    report = dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_FAILED_RUNTIME_FACTS_POSTREVIEW_V1',
                  status='CLOSED0_INDEPENDENT_REVIEW_OF_ACTUAL_RUNTIME_CLOSED1_FAILURE_FACTS_ONLY',
                  metadata_only=True, failure=None, original_Runtime_integer_exit_code=1,
                  original_Runtime_status=summary['status'], original_Runtime_failure=summary['failure'],
                  Root_actual_runtime_true_tools_pin=p_tools, actual_failed_Root_summary_pin=p_summary,
                  all_five_pre_summary_output_full_pins=summary['complete_output_pins'],
                  actual_failed_child_log_pin=p_log, actual_failed_watchdog_pin=p_watch,
                  actual_execution_binding_pin=p_binding, complete_fixed_current_pin_count=161,
                  original_caps=CAPS, complete_joint_roots=plan['complete_joint_roots'],
                  actual_child_runtime_integer_exit_code=1, actual_child_pid=watch['pid'],
                  actual_child_failure_from_complete_traceback='RuntimeError: original MF3 flux/reaction layout',
                  exact_failed_Source_statement="if mf==3:require(ng2==2,'original MF3 flux/reaction layout')",
                  failed_Source_line_one_based=88, actual_watchdog_limit_failure=watch['limit_failure'],
                  actual_child_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
                  actual_child_positive_RSS_measurement_available=watch['sampled_peak_rss_mib'] > 0,
                  actual_child_elapsed_seconds=watch['elapsed_seconds'], actual_root_report_wall_seconds=summary['wall_seconds'],
                  actual_complete_inventory_count=0, actual_complete_child_evidence_available=False,
                  original_gzip_payload_fullEOF_completion_claimed=False,
                  actual_failure_outputs_independently_whole_EOF_current7_checked=True,
                  actual_output_qualifications_false_verified=True, failed_invocation_preserved=True,
                  gzip_payload_read_by_peer=False, sciencebody_imported_or_executed=False,
                  business_rerun_by_peer=False, native_engines_started_by_peer=0, **FLAGS)
    target = BASE / 'independent_source_review_20261014/ACTUAL_RUNTIME_FAILURE_FACTS_POSTREVIEW.json'
    new(target, report)
    print(json.dumps(dict(status=report['status'], review_pin=pin(target), original_Runtime_integer_exit_code=1, **FLAGS)), flush=True)


if __name__ == '__main__':
    main()

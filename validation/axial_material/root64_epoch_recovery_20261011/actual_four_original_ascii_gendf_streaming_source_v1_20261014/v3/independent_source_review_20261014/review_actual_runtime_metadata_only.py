"""Independent post-runtime metadata/EOF review; never rerun any science body."""
import argparse
import json
import os
from pathlib import Path
from review_source_only import BASE, CAPS, FLAGS, current, full, new, pin, read, require


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--root-tools', required=True)
    ap.add_argument('--tool-return-key', required=True)
    args = ap.parse_args()
    p_tools = pin(Path(args.root_tools))
    tools = read(p_tools)
    raw = tools[args.tool_return_key]
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int
            and tools['original_integer_exit_code'] == 0 and type(raw['exit_code']) is int and raw['exit_code'] == 0
            and raw.get('session_id') is None and type(raw['output']) is str, 'genuine retained Root runtime typed closed0')
    stdout = json.loads(raw['output'].strip().splitlines()[-1])
    require(stdout['status'] == 'ACTUAL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY'
            and all(stdout[k] is False for k in ('physics_qualified', 'scientific_accuracy_qualified',
                     'complete_reaction_authority_qualified', 'physical_neutron_balance_qualified', 'AAA_qualified',
                     'ABA_admitted', 'goal_complete')), 'actual Root stdout completion and false qualifications')
    p_ready = pin(BASE / 'SOURCE_REVIEW_READY.json')
    ready = read(p_ready)
    plan = read(ready['control_plan_pin'])
    cli = read(pin(BASE / 'FINAL_ROOT_REVIEWABLE_CLI.json'))
    p_summary = stdout['report_pin']
    require(p_summary['path'] == str(Path(plan['planned_actual_output_root']) / 'Root_actual_four_original_ASCII_GENDF_summary.json'),
            'exact newly bound actual output report path')
    summary = read(p_summary)
    require(summary['schema'] == 'ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_GUARDED_REPORT_V1'
            and summary['status'] == stdout['status'] and summary['failure'] is None
            and summary['secondary_failures'] == [] and summary['source_freeze_pin'] == cli['source_freeze_pin']
            and summary['host_freeze_pin'] == cli['host_freeze_pin']
            and summary['actual_precise_retirement_receipt_pin'] == plan['actual_precise_retirement_receipt_pin']
            and summary['original_caps'] == CAPS and summary['original_guard_MRO_unchanged'] is True
            and summary['final_report_resource_check_passed'] is True
            and summary['native_engines_started'] == 0 and summary['original_ASCII_files_written'] == 0
            and all(summary[k] is False for k in ('physics_qualified', 'scientific_accuracy_qualified',
                       'complete_reaction_authority_qualified', 'physical_neutron_balance_qualified', 'AAA_qualified',
                       'ABA_admitted', 'goal_complete')), 'actual guarded report exact provenance and limited scope')
    output_pins = summary['complete_output_pins']
    require(len({p['path'] for p in output_pins}) == len(output_pins), 'unique complete actual output paths')
    for p in output_pins + summary['fixed_current_pins'] + [cli['source_freeze_pin'], cli['host_freeze_pin']]:
        full(p)
    out = Path(plan['planned_actual_output_root'])
    require({str(p) for p in out.rglob('*') if p.is_file()} == {p['path'] for p in output_pins} | {p_summary['path']},
            'every actual output file accounted by complete EOF/current7 pin')
    records = summary['records']
    require(len(records) == 1 and records[0]['status'] == 'PASS'
            and records[0]['label'] == 'gendf-stage/four_original_ASCII_fullEOF_inventory'
            and 0 < records[0]['wall_cap_seconds'] <= 600, 'one actual original child PASS, no retry')
    record = records[0]
    logpath = out / (record['label'] + '.log')
    logpin = pin(logpath)
    require(logpin['sha256'] == record['log_sha256'] and logpin in output_pins, 'actual child complete stdout log hash')
    lines = logpath.read_text().splitlines()
    require(len(lines) == 1, 'one complete child stdout receipt')
    child = json.loads(lines[0])
    require(child == summary['actual_child_receipt']
            and child['status'] == 'ACTUAL_ALL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY', 'exact actual child stdout receipt')
    p_watch = pin(logpath.with_suffix('.watchdog.json'))
    watch = read(p_watch)
    require(p_watch in output_pins and type(watch['returncode']) is int and watch['returncode'] == 0
            and watch['limit_failure'] is None and watch['command'] == record['command']
            and type(watch['pid']) is int and watch['pid'] > 0
            and watch['rss_cap_mib'] == 512 and 0 <= watch['sampled_peak_rss_mib'] < 512
            and 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= record['wall_cap_seconds'] <= 600
            and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True,
            'actual owning watchdog typed0, live ownRSS, wall, and own-group cleanup')
    expected_command = ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '-B',
                        str(BASE / 'stream_four_original_ascii_gendf.py'), '--binding-pin', record['command'][4],
                        '--expected-parent-pid', record['command'][6]]
    require(record['command'] == expected_command and int(record['command'][6]) > 0, 'actual exact original child argv and parent role')
    p_binding = json.loads(record['command'][4])
    binding = read(p_binding)
    require(p_binding in output_pins and binding['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_EXECUTION_BINDING_V1'
            and binding['control_plan_pin'] == ready['control_plan_pin']
            and binding['source_freeze_pin'] == cli['source_freeze_pin']
            and binding['original_caps'] == CAPS and binding['complete_joint_roots'] == plan['complete_joint_roots'],
            'actual once binding fullPF/current7/43 original cumulative roots')
    p_evidence = child['report_pin']
    evidence = read(p_evidence)
    require(p_evidence in output_pins and evidence == summary['actual_evidence']
            and evidence['schema'] == 'ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_STREAM_EVIDENCE_V1'
            and evidence['status'] == child['status'] and evidence['execution_binding_pin'] == p_binding
            and evidence['control_plan_pin'] == ready['control_plan_pin']
            and evidence['source_freeze_pin'] == cli['source_freeze_pin']
            and evidence['original_caps'] == CAPS and evidence['native_engines_started'] == 0
            and evidence['original_inputs_written'] == 0 and evidence['original_ASCII_files_written'] == 0,
            'complete actual child evidence/report binding')
    rows = evidence['actual_extractions']
    require(len(rows) == 4 and [r['nuclide'] for r in rows] == [r['nuclide'] for r in plan['inputs']]
            and sum(r['actual_decompressed_bytes'] for r in rows) == 284814387, 'allfour actual original EOF bytes')
    inventories = []
    for row, expected in zip(rows, plan['inputs']):
        p = row['complete_inventory_pin']
        value = read(p)
        require(p in output_pins and p['path'] == str(out / 'inventories' / (expected['nuclide'] + '_original_ASCII_GENDF_inventory.json'))
                and value['nuclide'] == expected['nuclide'] and value['mat'] == expected['mat']
                and value['current_gzip_primary_full_pin'] == expected['gzip_primary_current_full_pin']
                and value['historical_original_ASCII_path'] == expected['historical_original_ASCII_path']
                and value['actual_decompressed_SHA256'] == row['actual_decompressed_SHA256'] == expected['historical_original_ASCII_sha256']
                and value['actual_decompressed_bytes'] == row['actual_decompressed_bytes'] == expected['historical_original_ASCII_size_bytes']
                and value['full_current_compressed_SHA256'] == expected['gzip_primary_current_full_pin']['sha256']
                and value['original_ASCII_fullEOF_validated'] is True and value['gzip_CRC_and_ISIZE_validated'] is True
                and value['original_ASCII_not_written'] is True and value['current_original_inode_not_invented'] is True
                and value['second_quantization_performed'] is False and value['original_formatter_already_applied'] is True
                and value['original_receipt_and_deck_proof'] == expected['historical_proof'],
                'actual dual hashes, no unpack, historical lineage exact, no second quantization')
        current(expected['gzip_primary_current_full_pin'])
        grids = value['original8_MF1_grids']
        require(len(grids) == row['MF1_grids'] == 8 and len({g['temperature_K'] for g in grids}) == 8
                and [g['source_deck_temperature_K'] for g in grids] == expected['original_source_deck_temperatures_K']
                and all(len(g['sigma0_barn']) == 10 and len(g['ascending_energy_eV']) == 371 for g in grids),
                'actual eight decoded MF1 temperatures, original deck grid, ten dilution and 370 energy groups')
        sections = value['actual_sections']
        require(len(sections) == row['MF3_MF6_sections'] and len(sections) > 0 and {s['mf'] for s in sections} == {3, 6}
                and all(s['energy_groups'] == 370 and 1 <= s['nl'] <= 8 and s['nz'] in (1, 10)
                        and s['temperature_K'] in {g['temperature_K'] for g in grids} and s['LIST_records'] > 0 for s in sections),
                'actual original reaction dimensions and precise decoded temperature membership')
        require(all(value[k] is False for k in ('physics_qualified', 'scientific_accuracy_qualified',
                    'complete_reaction_authority_qualified', 'physical_neutron_balance_qualified', 'full_reference_qualified',
                    'unreduced_reference_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete',
                    'DRAGR_packed_raw_words_replayed', 'SCAT_constructed', 'current_SPH_MASK_context_applied',
                    'historical_machine_bit_replay')), 'every actual inventory qualification false')
        inventories.append(dict(nuclide=value['nuclide'], inventory_pin=p, decompressed_bytes=value['actual_decompressed_bytes'],
                                decompressed_sha256=value['actual_decompressed_SHA256'], decoded_temperatures_K=[g['temperature_K'] for g in grids],
                                source_deck_temperatures_K=[g['source_deck_temperature_K'] for g in grids],
                                MF3_MF6_section_count=len(sections)))
    require(0 < summary['wall_seconds'] < 1800, 'original whole runtime cap')
    snapshots = [summary['resources_before'], summary['resources_after'], summary['resources_after_including_summary_bytes']]
    for snapshot in snapshots:
        require(0 <= snapshot['host_SELF_peak_bytes'] < 512 * 2**20
                and snapshot['whole_elapsed_seconds'] < 1800
                and snapshot['complete_joint']['artifact_bytes'] + snapshot['explicit_external_metadata_bytes']
                    + snapshot['host_open_unlinked_bytes'] < 2 * 2**30
                and snapshot['original_history']['artifact_bytes'] + CAPS['cold_reserve_bytes']
                    + CAPS['metadata_reserve_bytes'] < CAPS['history_bytes'], 'actual complete caps/reservations snapshots')
    retirement = read(plan['actual_precise_retirement_receipt_pin'])
    require(all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']), 'allfour exact retired spool paths remain absent')
    for p in output_pins + [p_summary, p_tools]:
        current(p)
    result = dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_ACTUAL_RUNTIME_METADATA_POSTVERIFY_V1',
                  status='PASS_ACTUAL_FOUR_ORIGINAL_ASCII_RUNTIME_CLOSED0_OUTPUT_EOF_CURRENT7_ONLY',
                  failure=None, metadata_only=True, Root_actual_runtime_true_tools_pin=p_tools,
                  Root_actual_report_pin=p_summary, actual_child_evidence_pin=p_evidence,
                  actual_execution_binding_pin=p_binding, actual_watchdog_pin=p_watch,
                  all_actual_output_full_pins=output_pins, actual_inventory_summaries=inventories,
                  original_caps=CAPS, complete_joint_roots=plan['complete_joint_roots'],
                  actual_original_decompressed_payload_bytes=284814387,
                  actual_original_child_count=1, actual_watchdog_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
                  actual_whole_wall_seconds=summary['wall_seconds'],
                  all_output_bytes_independently_EOF_current7_checked=True,
                  gzip_payload_read_by_peer=False, sciencebody_imported_or_executed=False,
                  business_rerun_by_peer=False, native_engines_started_by_peer=0, **FLAGS)
    target = BASE / 'independent_source_review_20261014/ACTUAL_RUNTIME_POSTVERIFY_REVIEW.json'
    new(target, result)
    print(json.dumps(dict(status=result['status'], review_pin=pin(target), **FLAGS)), flush=True)


if __name__ == '__main__':
    main()

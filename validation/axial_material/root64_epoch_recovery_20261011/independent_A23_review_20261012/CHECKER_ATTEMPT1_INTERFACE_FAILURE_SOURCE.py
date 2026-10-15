"""Readonly saved A2/A3 evidence check. No candidate imports, child or resource API."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
REC = ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE = REC/'native_warm_A2_A3_bounded_host_source_v2'
SCOPE = ('three_plane_qualified', 'GLOBAL_qualified', 'rank_qualified',
         'online_BOOT_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete')


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def fullpin(path, keep=False):
    path = Path(path)
    before = identity(path.lstat())
    assert stat.S_ISREG(before[2])
    digest = hashlib.sha256()
    count = 0
    parts = []
    if keep:
        assert before[4] <= 16*2**20
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb', buffering=0) as stream:
        assert identity(os.fstat(stream.fileno())) == before
        while True:
            block = stream.read(65536)
            if not block:
                break
            digest.update(block)
            count += len(block)
            if keep:
                assert count <= 16*2**20
                parts.append(block)
        assert count == before[4] and identity(os.fstat(stream.fileno())) == before
    assert identity(path.lstat()) == before
    return dict(path=str(path), sha256=digest.hexdigest(), size_bytes=count, identity=before), b''.join(parts)


def normalize(row):
    return {key: row[key] for key in ('path', 'sha256', 'size_bytes', 'identity')}


def document(path, sha=None, seven=None):
    pin, data = fullpin(path, True)
    if sha is not None:
        assert pin['sha256'] == sha and pin['identity'] == json.loads(seven)
    return json.loads(data), pin


def closed(report, expected, count):
    assert report['status'] == expected and report['failure'] is None
    assert report.get('after_check_error') is None and len(report['records']) == count
    assert report['original_guard_class'] == 'OwnRSSSerialExecutor'
    assert report['original_guard_MRO_unchanged'] is True
    assert type(report['SELF_peak_bytes']) is int and 0 <= report['SELF_peak_bytes'] < 512*2**20
    assert type(report['wall_seconds']) in (int, float) and 0 < report['wall_seconds'] < 1800


def saved_resources(report, root):
    before = report['resources_before']
    after = report['resources_after']
    for value in (before, after):
        fresh = value['fresh_output']
        assert value['min_free_bytes'] == fresh['min_free_bytes'] == 8*2**30
        assert value['artifact_budget_bytes'] == 96*2**30
        assert fresh['artifact_budget_bytes'] == 2*2**30
        assert fresh['resource_roots'] == [str(root)]
        assert 0 <= fresh['artifact_bytes'] < 2*2**30
        assert value['artifact_bytes'] + 20971764748 + 64*2**20 < 96*2**30
        assert fresh['disk_free_bytes'] - 20971764748 - 2*2**30 >= 8*2**30
        assert value['resource_scope_policy'] == 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
        assert value['resource_scope_contract']['artifact_budget_GiB'] == 96
        assert value['resource_scope_contract']['min_free_GiB'] == 8
    assert before['fresh_output']['artifact_bytes'] == before['fresh_output']['regular_files'] == 0
    assert before['artifact_bytes'] + 20971764748 + 64*2**20 + 2*2**30 < 96*2**30
    assert before['checked_unix'] < after['checked_unix']


def all_rows(reports):
    table = {}
    occurrence_count = 0
    for report in reports:
        for key in ('fixed_current_pins', 'owned_runtime_pins', 'output_pins'):
            for row in report.get(key, []):
                row = normalize(row)
                occurrence_count += 1
                old = table.get(row['path'])
                assert old is None or old == row
                table[row['path']] = row
    for row in table.values():
        assert fullpin(row['path'])[0] == row
    return table, occurrence_count


def watch(root, record, table, success=True):
    path = root/(record['label']+'.watchdog.json')
    value, pin = document(path)
    assert table[str(path)] == pin
    assert record['status'] == ('PASS' if success else 'FAILED')
    assert value['command'] == record['command'] and type(value['returncode']) is int
    assert (value['returncode'] == 0) if success else (value['returncode'] != 0)
    assert value['limit_failure'] is None and value['rss_cap_mib'] == 512
    assert value['own_child_only'] is True and value['liveness_group_cleanup'] is True
    assert 0 < value['wall_cap_seconds'] <= record['wall_cap_seconds'] <= 600
    assert 0 <= value['elapsed_seconds'] < value['wall_cap_seconds']
    assert 0 <= value['sampled_peak_rss_mib'] < 512
    log = root/(record['label']+'.log')
    assert table[str(log)]['sha256'] == record['log_sha256']
    return value, pin


def main():
    start = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('A2', 'A3'), required=True)
    for prefix in ('summary', 'entry', 'root-tools'):
        parser.add_argument('--'+prefix, required=True)
        parser.add_argument('--'+prefix+'-sha256', required=True)
        parser.add_argument('--'+prefix+'-seven-id', required=True)
    parser.add_argument('--terminal-key', required=True)
    parser.add_argument('--entry-terminal-key', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    case = args.case
    plane = int(case[1])
    root = ART/('axial-material-new-REAL64-native-warm-'+case+'-20261012-v1')
    entry_root = ART/('axial-material-current-warm-'+case+'-CLE-entry-controls-20261012-v1')
    assert Path(args.summary) == root/('Root_actual_single_plane_warm_'+case+'_summary.json')
    assert Path(args.entry) == entry_root/'Root_actual_entry_controls_summary.json'
    report, summary_pin = document(args.summary, args.summary_sha256, args.summary_seven_id)
    entry, entry_pin = document(args.entry, args.entry_sha256, args.entry_seven_id)
    tools, tools_pin = document(args.root_tools, args.root_tools_sha256, args.root_tools_seven_id)
    terminal = tools[args.terminal_key]
    entry_terminal = tools[args.entry_terminal_key]
    for item in (terminal, entry_terminal):
        assert type(item['exit_code']) is int and item['exit_code'] == 0
        assert 'session_id' not in item and 'truncated' not in item['output'].lower()
    actual_stdout = json.loads(terminal['output'])
    actual_entry_stdout = json.loads(entry_terminal['output'])
    expected_status = 'ACTUAL_SINGLE_PLANE'+str(plane)+'_E0_WARM_'+case+'_NATIVE_PRODUCER_CLOSED0_ONLY'
    expected_entry = 'ACTUAL_CURRENT_WARM_'+case+'_CLE_ENTRY_CONTROLS_CLOSED0_ONLY'
    closed(report, expected_status, 4)
    closed(entry, expected_entry, 17)
    saved_resources(report, root)
    saved_resources(entry, entry_root)
    assert report['schema'] == 'ACTUAL_CURRENT_SINGLE_PLANE_WARM_'+case+'_NATIVE_PRODUCER_ROOT_V1'
    assert entry['schema'] == 'ACTUAL_CURRENT_WARM_'+case+'_CLE_ENTRY_CONTROLS_ROOT_V1'
    assert actual_stdout == dict(status=expected_status, failure=None, records=4)
    assert actual_entry_stdout == dict(status=expected_entry, failure=None, records=17)
    table, occurrences = all_rows((report, entry))
    for owner, owner_root, own_summary in ((report, root, args.summary), (entry, entry_root, args.entry)):
        reported = {row['path'] for row in owner['output_pins']}
        current = {str(p) for p in owner_root.rglob('*') if p.is_file()}
        assert current == reported | {own_summary}
    binding, binding_pin = document(BASE/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json')
    freeze, freeze_pin = document(BASE/'COMPLETE_A23_BOUNDED_HOST_SOURCE_FREEZE.json')
    selected = binding['cases'][case]
    assert (selected['case'], selected['plane'], selected['epoch']) == (case, plane, 0)
    assert table[str(BASE/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json')] == binding_pin
    assert table[str(BASE/'COMPLETE_A23_BOUNDED_HOST_SOURCE_FREEZE.json')] == freeze_pin
    assert freeze['schema'] == 'COMPLETE_CURRENT_A23_BOUNDED_HOST_SOURCE_FREEZE_ONLY_V1'
    for row in freeze['fixed_source_files']+freeze['fixed_external_source_files']:
        assert table.get(row['path']) == normalize(row)
    for row in binding['fixed_current_pins']:
        assert table.get(row['path']) == normalize(row)
    flags = binding['original_nine_flags']
    compiler = binding['compiler']['path']
    probe_name = 'verify_native_'+case+'_archive64'
    commands = [
        [compiler, *flags, *['-I'+p for p in binding['probe_include_directories']],
         '-J'+str(root/'build'), '-c', selected['probe_source_pin']['path'],
         '-o', str(root/'build'/(probe_name+'.o'))],
        [compiler, '-O2', '-ffp-contract=off', str(root/'build'/(probe_name+'.o')),
         *[p['path'] for p in binding['probe_link_dependencies']], '-o', str(root/'runtime'/probe_name)],
        [str(root/'runtime/Dragon')],
        [str(root/'runtime'/probe_name), 'native', 'new_native_'+case+'.xsm']]
    assert [r['label'] for r in report['records']] == ['build/compile_0', 'build/compile_1', case+'/solve', case+'/native_readback']
    assert [r['command'] for r in report['records']] == commands
    guards = []
    for index, record in enumerate(report['records']):
        value, pin = watch(root, record, table)
        saved = report['actual_watchdog_checks'][index]
        assert saved == dict(path=pin['path'], sha256=pin['sha256'],
                             peak_rss_mib=value['sampled_peak_rss_mib'], elapsed_seconds=value['elapsed_seconds'])
        guards.append(dict(label=record['label'], peak_rss_mib=value['sampled_peak_rss_mib'],
                           elapsed_seconds=value['elapsed_seconds'], watchdog_pin=pin))
    actual_native, native_log_pin = document(root/case/'native_readback.log')
    assert actual_native == report['actual_native_terminal']
    assert actual_native['schema'] == 'ACTUAL_NEW_WARM_'+case+'_COMPLETE_NATIVE_TERMINAL_READBACK_V1'
    assert actual_native['status'] == 'PASS'
    assert (actual_native['plane'], actual_native['epoch'], actual_native['groups'],
            actual_native['unknowns'], actual_native['scalar_regions']) == (plane, 0, 370, 14, 8)
    assert actual_native['full_native_read_status'] == 3
    for key in ('all370_ROOT_FLUX64_FLUX64_REF_bits_equal',
                'full_source64_type4_finite_and_exact_mirror', 'archive_read_only', 'strict_terminal_gate_passed'):
        assert actual_native[key] is True
    assert math.isfinite(actual_native['keff64']) and len(actual_native['keff64_bits']) == 16
    assert len(actual_native['residual64']) == 3 and all(math.isfinite(x) and x >= 0 for x in actual_native['residual64'])
    assert 2 <= actual_native['outer_iterations'] <= 500 and 1 <= actual_native['inner_iterations'] <= 740
    for key in ('flux_non32_roundtrip_count', 'source_non32_roundtrip_count'):
        assert type(actual_native[key]) is int and 0 <= actual_native[key] <= 5180
    assert report['transport_executed'] is True and report['single_plane_native_producer_closed'] is True
    assert report['all3_original_native_producer_inputs_qualified'] is False and report['old_wholeInput_or_Q_inherited'] is False
    assert all(report[key] is False and actual_native[key] is False and entry[key] is False for key in SCOPE)
    assert entry['transport_executed'] is False and entry['physical_producer_qualified'] is False
    assert entry['old_seventeen_PASS_inherited'] is False
    assert len(entry['declared_control_oracles']) == len(entry['actual_refusal_cases']) == 12
    for record in entry['records'][:5]:
        watch(entry_root, record, table)
    for wanted, actual, record in zip(entry['declared_control_oracles'], entry['actual_refusal_cases'], entry['records'][5:]):
        assert actual['case'] == wanted['case'] and actual['expected_abort'] == wanted['expected_abort']
        assert actual['actual_abort_message_exact'] is True and actual['all_actual_assertions_completed'] is True
        assert actual['transport_executed'] is False and actual['record'] == record
        w, _ = watch(entry_root, record, table, False)
        assert actual['actual_exit_code'] == w['returncode']
        log = (entry_root/(record['label']+'.log')).read_text()
        assert log.count(wanted['expected_abort']) == 1
    assert entry['actual_positive_readbacks'][0]['case_name'] == selected['case_name_json']
    assert entry['actual_positive_readbacks'][1]['actual_loader_calls'] == 8
    assert entry['actual_positive_readbacks'][1]['actual_refusals'] == 7
    assert all(x['all_actual_assertions_completed'] is True for x in entry['actual_positive_readbacks'])
    closure, closure_pin = document(root/'Host_actual_producer_terminal_output_fullEOF_binding.json')
    assert closure['actual_solver_record'] == report['records'][2]
    assert closure['actual_watchdog'] == report['actual_watchdog_checks'][2]
    assert closure['actual_output_pin'] == report['actual_output_pin'] == table[str(root/case/('new_native_'+case+'.xsm'))]
    assert closure['actual_SALT_binary_track_pin'] == report['actual_SALT_binary_track_pin'] == table[str(root/case/'radial_track.bin')]
    assert closure['independent_full_Source_tool_input_pins'] == report['fixed_current_pins']
    assert closure['internal_ROOT_REF_is_not_external_authority'] is True
    reference = next(x['pin'] for x in selected['physical_inputs'] if x['role'] == 'readonly_rays_reference')
    assert closure['readonly_original_rays_reference'] == reference
    assert all(closure['actual_SALT_binary_track_pin'][key] == reference[key] for key in ('sha256', 'size_bytes'))
    assert table[str(root/'runtime/Dragon')]['sha256'] == entry['owned_runtime_pins'][1]['sha256']
    for name in ('original_guard_Source', 'original_support', 'original_bounded'):
        row = binding[name]
        assert table.get(row['path']) == row
    for row in table.values():
        assert identity(Path(row['path']).lstat()) == row['identity']
    assert fullpin(args.summary)[0] == summary_pin and fullpin(args.entry)[0] == entry_pin
    assert fullpin(args.root_tools)[0] == tools_pin
    result = dict(schema='INDEPENDENT_CLOSED_ACTUAL_A23_SINGLE_PLANE_SAVED_REPORT_REVIEW_V1',
                  status='PASS_ACTUAL_'+case+'_FOUR_STAGE_SAVED_PRODUCER_ONLY',
                  actual_summary_pin=summary_pin, actual_entry_summary_pin=entry_pin,
                  actual_Root_terminal_receipt_pin=tools_pin,
                  actual_Root_terminal_chunk=terminal['chunk_id'],
                  complete_current_unique_EOF_SHA_7ID_pins=len(table), current_pin_occurrences=occurrences,
                  streamed_input_bytes=sum(r['size_bytes'] for r in table.values()),
                  four_actual_guard_stages=guards, actual_native_terminal=actual_native,
                  closure_pin=closure_pin, native_log_pin=native_log_pin,
                  original_guard_MRO_and_caps_saved_evidence_valid=True,
                  saved_history96_fresh2_free8_and_initial_reserves_valid=True,
                  whole370_readback_and_own_plane_e0_saved_evidence_valid=True,
                  physical_payload_read_only_for_complete_SHA_not_numerical_replay=True,
                  SELF_ru_maxrss_is_historical_highwater_not_current_RSS=True,
                  zero_sample_short_compile_stages_grant_no_RSS_qualification=True,
                  elapsed_readonly_review_seconds=time.monotonic()-start,
                  candidate_or_guard_or_compiler_or_transport_executed_by_reviewer=False,
                  new_science_qualification=False, **{key: False for key in SCOPE})
    with Path(args.output).open('x') as f:
        json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'], review_pin=fullpin(args.output)[0],
                         complete_unique_pins=len(table), guard_solve_peak_mib=guards[2]['peak_rss_mib'],
                         elapsed_readonly_review_seconds=result['elapsed_readonly_review_seconds'],
                         new_science_qualification=False), ensure_ascii=False))


if __name__ == '__main__':
    main()

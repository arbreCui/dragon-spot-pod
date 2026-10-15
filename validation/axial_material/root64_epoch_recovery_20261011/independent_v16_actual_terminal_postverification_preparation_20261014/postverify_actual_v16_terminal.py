"""Read-only postverification after Root's genuine closed v16 terminal.

This file is prepared before the terminal; preparation is no actual PASS.
Never import the pipeline Host, compile, execute a subprocess, or delete.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import os
import shlex
import stat
import sys

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART = Path('/Users/wen/spot/validation/artifacts')
HERE = Path(__file__).parent
CONTRACT = HERE / 'TERMINAL_POSTVERIFICATION_SOURCE_CONTRACT.json'
FORBIDDEN = ['SPOR64_BOOTB64-CENSUS:', 'ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
             'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE', 'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
             'SPOT-R64 B2I BOOTSTRAP COMMITTED', 'SPOT-X-REAL64-TERMINAL']


def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def full_pin(path, capture=False):
    path = Path(path)
    before = seven(path.lstat())
    if path.is_symlink() or not stat.S_ISREG(before[2]):
        raise RuntimeError('regular exact physical EOF required: ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    pieces = [] if capture else None
    h = hashlib.sha256()
    with os.fdopen(fd, 'rb') as stream:
        if seven(os.fstat(stream.fileno())) != before:
            raise RuntimeError('opened exact7 changed')
        count = 0
        while True:
            part = stream.read(1024 * 1024)
            if not part:
                break
            h.update(part)
            count += len(part)
            if capture:
                pieces.append(part)
        if count != before[4] or seven(os.fstat(stream.fileno())) != before:
            raise RuntimeError('complete same-fd physical EOF changed')
    if seven(path.lstat()) != before:
        raise RuntimeError('complete EOF current path changed')
    row = dict(path=str(path), sha256=h.hexdigest(), size_bytes=count, identity=before)
    return (b''.join(pieces), row) if capture else row


def read_bound(row):
    raw, current = full_pin(row['path'], True)
    if current != row:
        raise RuntimeError('exact full PF changed: ' + row['path'])
    return json.loads(raw)


def unique(rows):
    table = {}
    for row in rows:
        if set(row) != {'path', 'sha256', 'size_bytes', 'identity'}:
            raise RuntimeError('canonical full PF required')
        if row['path'] in table and table[row['path']] != row:
            raise RuntimeError('conflicting exact PF')
        table[row['path']] = row
    return table


def current7(rows):
    for row in unique(rows).values():
        p = Path(row['path'])
        if p.is_symlink() or seven(p.lstat()) != row['identity']:
            raise RuntimeError('fixed/current exact7 changed: ' + str(p))


def external(args, key):
    raw, row = full_pin(getattr(args, key), True)
    if row['sha256'] != getattr(args, key + '_sha256') or row['identity'] != json.loads(getattr(args, key + '_seven_id')):
        raise RuntimeError('Root external actual PF mismatch')
    return json.loads(raw), row


def family_measure(before):
    # Same explicit declared plus dynamic axial-family scope as original Source.
    roots = {Path(x) for x in before['declared_resource_roots']}
    roots.update(p for p in ART.iterdir() if p.name.startswith('axial-material-') and p.is_dir())
    total = count = 0
    for root in sorted(roots):
        if root.is_symlink() or not root.exists():
            raise RuntimeError('family root missing/symlink')
        entries = [root] if root.is_file() else root.rglob('*')
        for path in entries:
            s = path.lstat()
            if stat.S_ISLNK(s.st_mode):
                raise RuntimeError('family scope symlink')
            if stat.S_ISREG(s.st_mode):
                total += s.st_size
                count += 1
    v = os.statvfs(ART)
    reserve = 96 * 2**30 - total - 20971764748 - 64 * 2**20 - 2 * 2**30
    return dict(resource_roots=[str(x) for x in sorted(roots)], artifact_bytes=total,
                regular_files=count, disk_free_bytes=v.f_bavail * v.f_frsize,
                original_cold_metadata_fullfresh2G_next_run_reserve_bytes=reserve,
                original_initial_reserve_admitted_for_next_full_fresh_run=reserve > 0)


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    for key in ('summary', 'root-tools'):
        p.add_argument('--' + key, required=True)
        p.add_argument('--' + key + '-sha256', required=True)
        p.add_argument('--' + key + '-seven-id', required=True)
    p.add_argument('--root-terminal-key', default='actual_terminal_return')
    p.add_argument('--output-directory', required=True)
    args = p.parse_args()
    contract_raw, contract_pin = full_pin(CONTRACT, True)
    contract = json.loads(contract_raw)
    summary, summary_pin = external(args, 'summary')
    root, root_pin = external(args, 'root_tools')
    terminal = root[args.root_terminal_key]
    if root['observed_closed'] is not True or type(terminal.get('exit_code')) is not int or terminal.get('session_id') is not None or \
       type(root['original_integer_exit_code']) is not int or root['original_integer_exit_code'] != terminal['exit_code'] or terminal['exit_code'] not in (0, 1):
        raise RuntimeError('genuine Root closed integer terminal0/1 required before any review')
    launch = read_bound(contract['Root_exact_argv_pin'])
    if shlex.split(root['exact_executed_command']) != launch['argv'] or len(launch['argv']) != 90:
        raise RuntimeError('genuine exact frozen90 command differs')
    out = Path(contract['output_root'])
    if summary_pin['path'] != str(out / 'Root_actual_three_plane_engineering_summary.json') or \
       summary['schema'] != 'ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1':
        raise RuntimeError('exact actual output report/schema')
    hf = read_bound(contract['host_freeze_pin'])
    cli = read_bound(contract['CLI_pin'])
    if hf['host_source'] != contract['host_source_pin'] or cli['exact_reviewable_argv'] != launch['argv']:
        raise RuntimeError('final Source/HF/CLI identity changed')
    if full_pin(hf['host_source']['path']) != hf['host_source']:
        raise RuntimeError('actual Host Source changed')
    fixed = summary['fixed_current_pins']
    current7(fixed)
    if any(x not in fixed for x in hf['dependencies'] + [contract['host_freeze_pin'], hf['host_source']]):
        raise RuntimeError('complete owning2920 Source closure absent from actual fixed authority')
    raw_pin = summary['complete_unmodified_execution_records_pin']
    raw = read_bound(raw_pin)
    if raw['schema'] != 'ACTUAL_AAA3_COMPLETE_EXECUTION_PREPUBLICATION_RECORD_V1':
        raise RuntimeError('actual full raw publication record schema')
    stages_path = out / 'AAA3-streaming/stages.json'
    stages_raw, stages_pin = full_pin(stages_path, True)
    records = raw['records']
    if records != json.loads(stages_raw)['stages'] or \
       summary['records'] != [{k: v for k, v in x.items() if k not in ('resource_before', 'resource_after')} for x in records]:
        raise RuntimeError('raw full records, actual stages and compact records differ')
    if raw['fixed_current_pins'] != fixed or raw['owned_runtime_pins'] != summary['owned_runtime_pins']:
        raise RuntimeError('raw/compact current authority differs')
    expected_labels = contract['original50_ordered_labels']
    if len(records) > 50 or [x['label'] for x in records] != expected_labels[:len(records)]:
        raise RuntimeError('no-retry original stage sequence differs')
    cases = raw['actual_operator_refusals']
    if summary['actual_operator_refusals'] != [{k: v for k, v in x.items() if k != 'record'} for x in cases]:
        raise RuntimeError('raw/compact exact refusal evidence differs')
    case_table = {x['case']: x for x in cases}
    if len(case_table) != len(cases):
        raise RuntimeError('refusal retry/duplicate')
    physical = {}
    directories = []
    for path in sorted(out.rglob('*')):
        s = path.lstat()
        if stat.S_ISLNK(s.st_mode):
            raise RuntimeError('actual output symlink')
        if stat.S_ISREG(s.st_mode):
            if s.st_uid != os.getuid() or s.st_nlink != 1:
                raise RuntimeError('new actual output must be owned single-link regular')
            physical[str(path)] = full_pin(path)
        elif stat.S_ISDIR(s.st_mode):
            directories.append(dict(path=str(path), identity=seven(s)))
        else:
            raise RuntimeError('nonregular actual output')
    if physical.get(summary_pin['path']) != summary_pin:
        raise RuntimeError('actual summary not current in own physical output')
    published = unique(summary['output_pins'])
    for row in published.values():
        if physical.get(row['path']) != row:
            raise RuntimeError('published output fullEOF differs')
    for row in unique(summary['owned_runtime_pins']).values():
        if physical.get(row['path']) != row:
            raise RuntimeError('all current owned fullEOF differs')
    watch_rows = []
    unexpected = []
    for index, record in enumerate(records):
        wp = out / (record['label'] + '.watchdog.json')
        lp = out / (record['label'] + '.log')
        watch = read_bound(physical[str(wp)])
        log_raw, log_pin = full_pin(lp, True)
        text = log_raw.decode('utf-8', errors='replace')
        if log_pin != physical[str(lp)] or record['log_sha256'] != log_pin['sha256'] or watch['command'] != record['command'] or \
           type(watch['returncode']) is not int or watch['rss_cap_mib'] != 512 or watch['own_child_only'] is not True or \
           watch['liveness_group_cleanup'] is not True or not 0 < watch['wall_cap_seconds'] <= record['wall_cap_seconds'] <= 600:
            raise RuntimeError('genuine record/log/watch command and original guard identity')
        case_name = record['label'].rsplit('/', 1)[-1]
        case = case_table.get(case_name)
        exact = case is not None
        if exact:
            expected_abort = contract['exact33_refusal_messages'][case_name]
            if case['expected_abort'] != expected_abort or type(case['actual_exit_code']) is not int or case['actual_exit_code'] != 1 or \
               case['original_execution_record_index'] != index or case['original_execution_record_label'] != record['label'] or \
               'record' in case or case['actual_log_pin'] != log_pin or case['actual_watchdog_pin'] != physical[str(wp)] or \
               any(case[k] is not True for k in ('actual_abort_message_exact', 'pre_transport_abort_at_frozen_validation_branch',
                   'no_positive_solver_or_seal_trace', 'all_actual_assertions_completed')) or record['status'] != 'FAILED' or \
               watch['returncode'] != 1 or watch['limit_failure'] is not None or text.count(expected_abort) != 1 or \
               any(mark in text for mark in FORBIDDEN) or not 0 <= watch['sampled_peak_rss_mib'] < 512 or \
               not 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds']:
                raise RuntimeError('precise actual expected exit1 refusal failed postverification')
        elif record['status'] != 'PASS' or watch['returncode'] != 0 or watch['limit_failure'] is not None:
            unexpected.append(dict(index=index, label=record['label'], actual_watch=watch, log_pin=log_pin))
        else:
            if not 0 <= watch['sampled_peak_rss_mib'] < 512 or not 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds']:
                raise RuntimeError('actual passed child original cap violated')
        watch_rows.append(dict(index=index, label=record['label'], expected_refusal=exact,
                               actual_watch=watch, watch_pin=physical[str(wp)], log_pin=log_pin))
    success = terminal['exit_code'] == 0
    independently_read_terminal = None
    if success:
        if len(records) != 50 or len(cases) != 33 or set(case_table) != set(contract['exact33_refusal_messages']) or \
           sum(x['status'] == 'PASS' for x in records) != 17 or sum(x['status'] == 'FAILED' for x in records) != 33 or unexpected or \
           summary['status'] != 'ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY' or summary['engineering_three_plane_closed0'] is not True or \
           summary['failure'] is not None or summary['after_check_error'] is not None or summary['first_failure_secondary_errors'] != []:
            raise RuntimeError('Root0 requires genuinely complete50/17PASS/33exact refusions and no fatal guard')
        if set(physical) != set(published) | {summary_pin['path']} or raw['actual_terminal'] != summary['actual_terminal']:
            raise RuntimeError('completed physical inventory/current terminal differs')
        result = summary['actual_terminal']
        ax = result['AX_full_pin']
        archive = result['ARCHIVE_full_pin']
        if physical.get(ax['path']) != ax or physical.get(archive['path']) != archive:
            raise RuntimeError('final sealed pair complete physical PF differs')
        log = (out / 'AAA/BOOT_positive.log').read_text()
        readings = [json.loads(x) for x in log.splitlines() if x.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"')]
        if len(readings) != 1 or readings[0]['status'] != 'PASS' or readings[0]['all_payload_bits_equal'] is not True or \
           readings[0] != result['actual_Fortran_complete_copy_readback']:
            raise RuntimeError('unique genuine complete sealed payload bit readback')
        # Only the already-reviewed read-only file parser is loaded, after Root0.
        sys.dont_write_bytecode = True
        reader = contract['readonly_data_helper_pin']
        if full_pin(reader['path']) != reader:
            raise RuntimeError('frozen read-only data helper changed')
        spec = importlib.util.spec_from_file_location('independent_v16_readonly_data', reader['path'])
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)
        independently_read_terminal = json.loads(json.dumps(
            data.final_readback(Path(ax['path']), Path(archive['path'])), allow_nan=False))
        if independently_read_terminal != result['actual_terminal']:
            raise RuntimeError('independent final physical full-tree typed readback differs')
        if summary['SELF_peak_bytes'] >= 512 * 2**20 or summary['wall_seconds'] >= 1800 or \
           sum(x['size_bytes'] for x in physical.values()) >= 2 * 2**30 or summary['parent_memory_observation']['first_observation_error'] is not None:
            raise RuntimeError('actual parent/wall/fresh/observation original guard violated')
    else:
        if 'Traceback (most recent call last)' not in terminal['output']:
            raise RuntimeError('genuine closed failure missing original terminal traceback')
        if summary['failure'] is not None and summary['failure'] not in terminal['output']:
            raise RuntimeError('first summary error absent from genuine original terminal traceback')
    # Fixed science is observed by all7; every owned/new physical output was EOF.
    current7(fixed)
    family = family_measure(summary['resources_before'])
    output = Path(args.output_directory)
    if output.parent != REC or not output.name.startswith('independent_v16_actual_') or output.exists() or output.is_symlink():
        raise RuntimeError('one fresh own postverification metadata directory')
    report = dict(schema='INDEPENDENT_V16_GENUINE_TERMINAL_POSTVERIFICATION_V1',
                  status='PASS_ACTUAL_V16_ENGINEERING_CLOSED0_POSTVERIFIED_ONLY' if success else 'PASS_ACTUAL_V16_CLOSED_FAILURE_POSTVERIFIED_NO_QUALIFICATION',
                  failure=None, business_failure=not success, actual_pipeline_tool_exit_code=terminal['exit_code'],
                  genuine_closed_actual_Root_tool_pin=root_pin, actual_terminal_return=terminal,
                  summary_pin=summary_pin, full_raw_records_pin=raw_pin, stages_pin=stages_pin,
                  host_freeze_pin=contract['host_freeze_pin'], CLI_pin=contract['CLI_pin'],
                  Root_exact_argv_pin=contract['Root_exact_argv_pin'], preparation_contract_pin=contract_pin,
                  actual_record_count=len(records), actual_PASS_records=sum(x['status'] == 'PASS' for x in records),
                  actual_FAILED_records=sum(x['status'] == 'FAILED' for x in records), exact_expected_refusal_records=len(cases),
                  genuine_unexpected_failure_records=unexpected, watch_and_log_rows=watch_rows,
                  raw_equal_actual_stages_compact_only_resource_fields_removed=True,
                  fixed_current_count=len(fixed), all_fixed_seven_id_before_after_equal=True,
                  owned_runtime_count=len(summary['owned_runtime_pins']),
                  physical_output_full_EOF_count_including_summary=len(physical),
                  physical_output_bytes_including_summary=sum(x['size_bytes'] for x in physical.values()),
                  physical_output_full_EOF_pins=list(physical.values()), directory_inventory=directories,
                  published_current_output_count=len(published), failure_field=summary['failure'],
                  after_check_error=summary['after_check_error'], first_failure_secondary_errors=summary['first_failure_secondary_errors'],
                  original_terminal_traceback=terminal['output'] if not success else None,
                  parent_memory_observation=summary['parent_memory_observation'], SELF_peak_bytes=summary['SELF_peak_bytes'],
                  wall_seconds=summary['wall_seconds'], actual_fresh_peaks_by_phase=summary['actual_fresh_peaks_by_phase'],
                  actual_terminal=summary['actual_terminal'], independent_final_physical_readback=independently_read_terminal,
                  actual_compact_expected_reader_admission=summary['actual_compact_expected_reader_admission'],
                  actual_cache336_driver_and_budget_bit_admission=summary['actual_cache336_driver_and_budget_bit_admission'],
                  full50_engineering_completed=success, physics_qualification=False, AAA_qualified=False,
                  ABA_admitted=False, goal_complete=False, resources_before_snapshot=summary['resources_before'],
                  resources_after_before_summary_snapshot=summary['resources_after'], current_actual_family_scope=family,
                  independent_business_executed=False, independent_compiler_executed=False,
                  independent_numerical_executed=False, independent_deletion_executed=False,
                  Source_modified=False, science_large_full_EOF_repeated=False, all_file_descriptors_closed=True)
    output.mkdir()
    with (output / 'REVIEW.json').open('x') as f:
        json.dump(report, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps(dict(review_pin=full_pin(output / 'REVIEW.json'), business_failure=not success,
                          actual_pipeline_tool_exit_code=terminal['exit_code'], failure=None)))


if __name__ == '__main__':
    main()

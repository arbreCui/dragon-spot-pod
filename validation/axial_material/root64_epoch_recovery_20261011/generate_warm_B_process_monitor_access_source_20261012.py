"""Prepare Source only. Never import candidate code or launch a child."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART = Path('/Users/wen/spot/validation/artifacts')
OLD = REC/'native_warm_B_initial_storage_reserve_source_v2'
NEW = REC/'native_warm_B_process_monitor_host_source_v3'
NAMES = ('guarded_warm_B_common.py', 'run_current_native_warm_B.py',
         'run_current_warm_B_entry_controls.py', 'verify_native_B_archive64.f90')
OLD_OUT = 'axial-material-new-REAL64-native-warm-B-20261012-v2-initial-storage-reserve'
NEW_OUT = 'axial-material-new-REAL64-native-warm-B-20261012-v3-process-monitor-access'
FREEZE = 'COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json'
PROOF = 'COMPLETE_INITIAL_STORAGE_HOST_SOURCE_BYTE_INVERSE.json'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def read(p, bound=16*2**20):
    p = Path(p)
    before = identity(p.lstat())
    assert stat.S_ISREG(before[2]) and before[3] == 1 and before[4] <= bound, str(p)
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb', buffering=0) as f:
        assert identity(os.fstat(f.fileno())) == before
        parts = []
        total = 0
        while True:
            block = f.read(min(65536, bound+1-total))
            if not block:
                break
            parts.append(block)
            total += len(block)
            assert total <= bound
        data = b''.join(parts)
        assert total == before[4] and identity(os.fstat(f.fileno())) == before
    assert identity(p.lstat()) == before
    return data, dict(path=str(p), sha256=hashlib.sha256(data).hexdigest(),
                     size_bytes=len(data), identity=before)


def save(p, data):
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    with Path(p).open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    return read(p)[1]


def main():
    assert not NEW.exists() and not NEW.is_symlink()
    assert not (ART/NEW_OUT).exists() and not (ART/NEW_OUT).is_symlink()
    old_freeze_bytes, old_freeze_pin = read(OLD/FREEZE)
    old_freeze = json.loads(old_freeze_bytes)
    assert old_freeze['schema'] == 'CURRENT_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE_ONLY_V2'
    original_rows = old_freeze['fixed_source_files']
    original_table = {Path(r['path']).name: r for r in original_rows}
    assert len(original_table) == len(original_rows) == 6
    for row in original_rows:
        assert read(row['path'])[1] == row
    binding_pin = old_freeze['unchanged_complete_runtime_and_physical_binding_pin']
    binding_bytes, actual_binding_pin = read(binding_pin['path'])
    assert actual_binding_pin == binding_pin
    binding = json.loads(binding_bytes)
    selected17 = binding['selected_actual_current17_report']
    seventeen_bytes, p17 = read(selected17['path'])
    assert p17 == selected17
    pentry_path = ART/'axial-material-current-warm-B-CLE-entry-controls-20261012-v1/Root_actual_entry_controls_summary.json'
    entry_bytes, pentry = read(pentry_path)
    seventeen = json.loads(seventeen_bytes)
    entry = json.loads(entry_bytes)
    assert seventeen['status'] == 'ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY'
    assert entry['status'] == 'ACTUAL_CURRENT_WARM_B_CLE_ENTRY_CONTROLS_CLOSED0_ONLY'
    assert seventeen['transport_executed'] is False and entry['transport_executed'] is False
    failed_path = ART/OLD_OUT/'Root_actual_single_plane_warm_B_summary.json'
    failed_bytes, failed_pin = read(failed_path)
    failed = json.loads(failed_bytes)
    watch_bytes, watch_pin = read(failed_path.parent/'build/compile_0.watchdog.json')
    watch = json.loads(watch_bytes)
    assert failed['status'] == 'FAILED_WARM_B_NATIVE_PRODUCER_NO_RETRY'
    assert failed['transport_executed'] is False and len(failed['records']) == 1
    assert failed['failure'] == "PermissionError(1, 'Operation not permitted')"
    assert watch['returncode'] == 0 and watch['sampled_peak_rss_mib'] == 0
    assert watch['limit_failure'] == failed['failure']
    originals = {n: read(OLD/n) for n in NAMES}
    NEW.mkdir()
    sources = []
    checks = []
    for n, (original, original_pin) in originals.items():
        changes = []
        current = original
        if n == 'run_current_native_warm_B.py':
            before, after = OLD_OUT.encode(), NEW_OUT.encode()
            assert original.count(before) == 1 and original.count(after) == 0
            offset = original.index(before)
            current = original.replace(before, after, 1)
            assert current.count(after) == 1 and current.replace(after, before, 1) == original
            changes = [dict(old=OLD_OUT, new=NEW_OUT, count=1,
                            before_byte_offsets=[offset], after_byte_offsets=[offset])]
        current_pin = save(NEW/n, current)
        reverse = current
        for change in reversed(changes):
            assert reverse.count(change['new'].encode()) == change['count']
            reverse = reverse.replace(change['new'].encode(), change['old'].encode(), change['count'])
        assert reverse == original and original_pin == original_table[n]
        ast_equal = None
        if n.endswith('.py'):
            ast.parse(current.decode(), filename=str(NEW/n))
            ast_equal = ast.dump(ast.parse(reverse), include_attributes=False) == ast.dump(ast.parse(original), include_attributes=False)
            assert ast_equal
        sources.append(dict(original_source=original_pin, new_source=current_pin,
                            literal_changes=changes, full_byte_forward_and_inverse_equal=True,
                            reversed_full_AST_equal=ast_equal))
        checks.append(dict(name=n+'_complete_forward_inverse_bytes_and_current_fullpin', passed=True))
    environment = dict(
        process_monitor_access_required=True,
        required_operation='Unchanged original OwnRSSSerialExecutor must be allowed to launch /bin/ps and sample its own compiler and solver child.',
        permission_failure_is_failure=True,
        no_monitor_bypass_or_zero_peak_qualification=True,
        original_guard_or_MRO_patched=False,
        original_caps_or_formulas_patched=False,
        original_liveness_cleanup_and_genuine_wait_required=True,
        Root_separately_selects_authorized_execution_environment=True,
        this_Source_preparation_tests_monitor_permissions=False)
    scopes = dict(source_only=True, transport_executed=False, B_producer_qualified=False,
                  three_plane_qualified=False, GLOBAL_qualified=False, rank_qualified=False,
                  online_BOOT_qualified=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False)
    proof = dict(schema='INITIAL_FRESH_OUTPUT_HISTORY_RESERVE_SOURCE_ONLY_V2',
                 derivation='V2_TO_V3_PROCESS_MONITOR_ACCESS_NAMESPACE_ONLY', sources=sources,
                 unchanged_runtime_and_physical_binding_pin=binding_pin,
                 old_frozen_V2_Source_freeze_pin=old_freeze_pin,
                 old_V2_fixed_Source_package_pins=original_rows,
                 history_cap_bytes=96*2**30, cold_reserve_bytes=20971764748,
                 metadata_reserve_bytes=64*2**20, fresh_output_cap_bytes=2*2**30,
                 initial_fresh_reservation_once=True, unchanged_actual_growth_monitor_during_execution=True,
                 initial_admission_before_runtime_directory_or_business_child=True,
                 old_B_failure_preserved=True, automatic_business_retry=False,
                 execution_environment_contract=environment,
                 actual_V2_failure_evidence=dict(summary_pin=failed_pin, watchdog_pin=watch_pin,
                                                original_tool_initial_chunk='f58cab', original_session=72971,
                                                original_tool_terminal_chunk='6f7617', original_tool_exit_code=1,
                                                compiler_returncode=0, sampled_peak_rss_mib=0.0,
                                                transport_executed=False, qualification_inherited=False), **scopes)
    proof_pin = save(NEW/PROOF, proof)
    checks.extend([dict(name=n, passed=True) for n in (
        'four_original_sources_read_to_EOF_and_match_frozen_V2_rows',
        'three_support_sources_literal_byteexact_V2',
        'main_one_OUT_literal_only_and_complete_inverse_AST',
        'full_V2_package_and_freeze_current_fullpins_unchanged',
        'V2_compile_monitor_failure_and_no_transport_accurately_retained',
        'same_V2_Source_freeze_schema_filename_and_required_five_members',
        'original_guard_resources_threads_no_retry_and_physics_byteexact',
        'fresh_v3_business_output_absent_at_Source_preparation',
        'external_actual17_and_entry_reports_current_fullpins_saved_not_requalified')])
    receipt = dict(schema='WARM_B_PROCESS_MONITOR_ACCESS_SOURCE_PREPARATION_RECEIPT_V1',
                   status='AUTHOR_SOURCE_ONLY_STATIC_PREPARATION_NO_RUNTIME_CREDIT',
                   checks=checks, all_checks_typed_true=True, determinate_source_blockers=[],
                   reviewed_new_source_pins=[s['new_source'] for s in sources],
                   reviewed_full_byte_inverse_proof_pin=proof_pin,
                   execution_environment_contract=environment,
                   actual_independent_Source_review=None, candidate_imported=False,
                   compiler_or_solver_or_OS_monitor_executed=False, **scopes)
    receipt_pin = save(NEW/'SOURCE_STATIC_PREPARATION_RECEIPT.json', receipt)
    rows = [proof_pin, receipt_pin]+[s['new_source'] for s in sources]
    required = set(NAMES) | {PROOF}
    assert len(rows) == 6 and len({r['path'] for r in rows}) == 6
    assert required <= {Path(r['path']).name for r in rows}
    assert all(Path(r['path']).parent == NEW for r in rows)
    freeze = dict(schema=old_freeze['schema'], fixed_source_files=rows,
                  source_writer_pin=read(Path(__file__))[1],
                  unchanged_complete_runtime_and_physical_binding_pin=binding_pin,
                  old_V2_Source_freeze_pin=old_freeze_pin,
                  actual_writer_tool=None, actual_root_Source_replay=None,
                  actual_independent_Source_review=None,
                  execution_environment_contract=environment,
                  exact_external_prerequisite_CLI_report_pins=dict(seventeen=p17, entry_controls=pentry),
                  initial_reservation_before_any_business_child=True,
                  automatic_solver_retry=False, requires_original_budget_space=True,
                  physical_solver_or_threshold_change=False, **scopes)
    freeze_pin = save(NEW/FREEZE, freeze)
    argv = ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '-B', str(NEW/NAMES[1])]
    for prefix, row in [('seventeen', p17), ('entry-controls', pentry), ('source-freeze', freeze_pin)]:
        argv += ['--'+prefix+'-summary', row['path'], '--'+prefix+'-sha256', row['sha256'],
                 '--'+prefix+'-seven-id', json.dumps(row['identity'], separators=(',', ':'))]
    for row in rows+[freeze_pin]+original_rows+[old_freeze_pin, binding_pin, p17, pentry, failed_pin, watch_pin]:
        assert read(row['path'])[1] == row
    assert not (ART/NEW_OUT).exists() and not (ART/NEW_OUT).is_symlink()
    print(json.dumps(dict(status='SOURCE_ONLY_V3_PACKAGE_PREPARED_NO_EXECUTION',
                         package=str(NEW), source_rows=rows, source_freeze_pin=freeze_pin,
                         exact_future_Root_argv=argv, check_count=len(checks),
                         actual_independent_Source_review=None,
                         monitor_permissions_tested_here=False, **scopes), ensure_ascii=False))


if __name__ == '__main__':
    main()

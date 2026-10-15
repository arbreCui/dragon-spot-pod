from pathlib import Path
import json, hashlib, shutil, datetime, os, stat

T = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009')
c = json.loads((T / 'config.json').read_text())
R, OUT, TERM = (Path(c[k]) for k in ('R', 'OUT', 'TERM'))

def pin(path):
    path = Path(path)
    before = path.lstat()
    assert path.is_absolute() and stat.S_ISREG(before.st_mode) and before.st_nlink == 1
    h = hashlib.sha256()
    with path.open('rb') as f:
        while raw := f.read(1024 * 1024):
            h.update(raw)
    after = path.lstat()
    assert before == after
    return dict(path=str(path), sha256=h.hexdigest())

def write_new(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

tool = json.loads((R / 'run_terminal_tool_return.json').read_text())
assert type(tool['exit_code']) is int and tool['exit_code'] == 1 and tool['closed'] is True
assert tool['initial_chunk_id'] == 'd68fa5' and tool['terminal_chunk_id'] == 'c5f80c'
assert tool['success_recorder_called'] is False
assert pin(c['F'])['sha256'] == c['factorySha'] == '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
decl = pin(OUT / 'declaration.json')
prep = pin(TERM / 'declaration_terminal_return.json')
assert decl['sha256'] == c['declarationSha'] and prep['sha256'] == c['prepSha']
assert all(c[k] is None for k in ('sealSha', 'terminalSha', 'terminalPath', 'failed_terminal_sha'))
assert not (OUT / 'seal.json').exists() and not (OUT / 'audit/result.json').exists()
result = json.loads((OUT / 'driver_result.json').read_text())
stages_path = OUT / 'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V8/stages.json'
stages = json.loads(stages_path.read_text())['stages']
watch_path = OUT / 'audit/audit.watchdog.json'
w = json.loads(watch_path.read_text())
assert result['classification'] == 'FAILED_COMBINED_RUNTIME_LINK_NO_RETRY'
assert result['error'] == w['limit_failure'] == "RuntimeError('own-child 512 MiB RSS cap reached')"
assert len(stages) == 5 and [s['status'] for s in stages] == ['PASS'] * 4 + ['FAILED']
assert w['returncode'] == -15 and w['rss_cap_mib'] == 512 and w['sampled_peak_rss_mib'] == 516.46875
assert w['liveness_group_cleanup'] is True and w['own_child_only'] is True
assert (T / 'run.stdout').stat().st_size == 0 and (T / 'run.stderr').stat().st_size == 1212
stdout = TERM / 'failed_run_full_stdout.txt'
stderr = TERM / 'failed_run_full_stderr.txt'
for source, target in ((T / 'run.stdout', stdout), (T / 'run.stderr', stderr)):
    assert not target.exists()
    shutil.copy2(source, target)
    assert pin(source)['sha256'] == pin(target)['sha256']
e = dict(
    schema='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V8_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1',
    record_producer='root', actual_tool_terminal_return_observed=True,
    record_written_after_actual_terminal_return=True, returncode=1, actual_tool_result=tool,
    observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), source=pin(c['F']),
    declaration=decl, prep_terminal_evidence=prep, command=tool['actual_child_command'],
    full_stdout=pin(stdout), full_stderr=pin(stderr), build_seal=None,
    driver_result=pin(OUT / 'driver_result.json'), stages=pin(stages_path),
    failed_python_audit_watch=pin(watch_path), failed_python_audit_log=pin(OUT / 'audit/audit.log'),
    failed_python_audit_pid=w['pid'], failed_python_audit_peak_rss_mib=w['sampled_peak_rss_mib'],
    failed_python_audit_elapsed_seconds=w['elapsed_seconds'], failed_stage_elapsed_seconds=stages[-1]['elapsed_seconds'],
    failed_driver_elapsed_seconds=result['elapsed_seconds'],
    failed_archive_bytes_before_closeout=result['archive_bytes_before_closeout'],
    failed_driver_resource_observation=result['resources'], failed_python_audit_cleanup=True,
    failure_scope='PYTHON_AUDIT_CHILD_RSS_CAP_NO_COMBINED_RUNTIME_OR_NATIVE_PHYSICS_ELIGIBILITY',
    actual_original_failure_line_or_function_not_localized=True,
    successful_combined_link_completion_observed=False, successful_new_runtime_build_observed=False,
    production_admission_observed=False, native_transport_executed=False,
    mathematical_controls_newly_executed=False, combined_runtime_native_RSS_proved=False,
    actual_full_FLU_entry_executed=False, AAA_accuracy_qualified=False, ABA_admitted=False,
    scientific_qualification=False, actual_tail_check=None, actual_elapsed_seconds=None,
    actual_archive_bytes=None, actual_resources=None)
old = Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/terminal_return.json')
assert set(e) == set(json.loads(old.read_text()))
receipt = TERM / 'terminal_return.json'
write_new(receipt, e)
shutil.copy2(receipt, R / 'run_terminal_return.json')
c['failed_terminal_sha'] = pin(receipt)['sha256']
(T / 'config.json').write_text(json.dumps(c, indent=2) + '\n')
print(json.dumps(dict(status='ACTUAL_FAILED_RUN_RECORDED_NO_SUCCESS_CREDIT', receipt=pin(receipt), root_exit_code=1,
    actual_RSS_MiB=w['sampled_peak_rss_mib'], seal=None, four_tails=None), allow_nan=False))

"""Exercise the real static entry and prerequisite refusals once, without transport."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
SOURCE = ROOT / 'validation/axial_material/prepare_qualified_ABA_ce_white_trace_precision.py'
PARENT = ROOT / 'validation/artifacts/axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
DIRECTORY = PARENT / 'aba_measurement'
DECLARATION = DIRECTORY / 'ce_entry_declaration.json'
OUTPUT = DIRECTORY / 'ce_entry_guard_verification.json'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python')


def main():
    if OUTPUT.exists():
        raise ValueError('existing conditional-entry verification: no overwrite or retry')
    spec = importlib.util.spec_from_file_location('aba_conditional_precision_entry_audit', SOURCE)
    entry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entry)
    expected = entry.base.sha256(DECLARATION)
    declaration = json.loads(DECLARATION.read_text())
    if declaration['files'].get(str(Path(__file__).resolve())) != entry.base.sha256(Path(__file__).resolve()):
        raise ValueError('actual verification implementation is not frozen')
    future = entry.OUT
    aba = entry.PROD / 'ABA'
    if future.exists() or aba.exists():
        raise ValueError('these static/refusal controls require no actual ABA execution directory')
    native_claim = entry.AAA_CE / 'AAA/run_claim.json'
    original_paths = [entry.PROD / 'AAA/run_status.json', entry.PROD / 'runtime/production_runner.py',
        entry.AAA_CE / 'AAA/execution.json', entry.AAA_CE / 'runtime/ce_execution.py', native_claim]
    before = {str(p):entry.base.sha256(p) for p in original_paths}
    common = [str(PYTHON), '-B', str(SOURCE)]
    args = [str(DECLARATION), '--sha256', expected]
    actual_unqualified = PARENT / 'reference_assessment.json'
    commands = [
        ('static_preflight', [*common, 'preflight', *args], 0, 'STATIC_ABA_REFERENCE_ENTRY_READY_ACTUAL_AAA_AND_ABA_EVIDENCE_PENDING'),
        ('missing_qualification', [*common, 'prepare', *args], 1, 'explicit actual AAA qualified receipt and SHA256 required'),
        ('actual_unqualified_reference', [*common, 'prepare', *args, '--reference-qualification', str(actual_unqualified),
            '--reference-sha256', entry.base.sha256(actual_unqualified)], 1, 'only the frozen full precision reference can qualify this ABA attempt'),
    ]
    result = dict(schema='AXMAT_ABA_CONDITIONAL_PRECISION_ENTRY_ACTUAL_PREFLIGHT_V1', status='FAILED',
        case='ABA', error=None, transport_launched=False, ABA_measurement_admitted=False,
        independent_ABA_accuracy_qualified=False, controls=[], files={})
    started = time.monotonic()
    environment = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    try:
        for name, command, returncode, marker in commands:
            log = DIRECTORY / ('ce_entry_' + name + '.log')
            with log.open('xb') as stream:
                process = subprocess.run(command, cwd=ROOT, env=environment,
                    stdout=stream, stderr=subprocess.STDOUT, timeout=60, check=False)
            content = log.read_text()
            if process.returncode != returncode or marker not in content:
                raise ValueError('actual conditional entry control failed: ' + name)
            if future.exists() or aba.exists():
                raise ValueError('static/refused entry created an ABA execution directory')
            result['controls'].append(dict(name=name, status='PASS', returncode=process.returncode,
                command=command, log=entry.pin(log), required_marker=marker))
        entry.verify_files(declaration['files'])
        entry.verify_files(before)
        entry.render_native()
        entry.render_collector('0'*64)
        entry.render_driver()
        result.update(status='PASS_STATIC_ENTRY_AND_TWO_ACTUAL_REFUSALS', future_reference_root_created=False,
            actual_ABA_directory_created=False, original_native_lifecycle_AST_unchanged=True,
            original_complete_history_and_eight_gate_decision_AST_unchanged=True,
            original_statistical_and_current_source_reused_by_byte_identity=True,
            positive_actual_ABA_preparation_exercised=False,
            limitations=['Static and refusal evidence only. The positive branch awaits actual AAA qualification and sealed ABA evidence.',
                'No independent ABA accuracy, physical receipt, transport completion, or full neutron-balance claim.'])
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic() - started
        result['files'] = {**declaration['files'], **before, str(DECLARATION):expected,
            str(actual_unqualified):entry.base.sha256(actual_unqualified),
            **{str(p):entry.base.sha256(p) for p in DIRECTORY.glob('ce_entry_*.log')}}
        entry.write_new(OUTPUT, result)
    print(json.dumps(dict(status=result['status'], verification=entry.pin(OUTPUT),
        future_reference_root_created=False, native_transport_launched=False)))


if __name__ == '__main__':
    main()

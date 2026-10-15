"""Versioned mesh/angle study: adapt only fixed-package storage metadata.

The first study's successful cold baseline and rejected 24-cell assembly are
retained. Neither the native FIXB guard nor the radial package is changed.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import struct
import time

import frozen_AAA_axial_sensitivities as base

ART = base.ART
PRIOR = ART / 'axial-material-AAA-frozen-axial-sensitivities-20261004'
OUT = ART / 'axial-material-AAA-frozen-axial-metadata-20261004'
base.OUT = OUT
NEW_CASES = base.CASES[1:]


def adapt_bytes(original, entry, target):
    """Replace one declared integer word; all remaining archive bytes identical."""
    offset, length, kind = entry
    if (length, kind) != (40, 1) or target <= 0:
        raise ValueError('invalid storage metadata adaptation')
    state = struct.unpack_from('<40i', original, 4 * offset)
    if state[7:11] != (370, 456, 24, 3):
        raise ValueError('unexpected original fixed-basis dimensions')
    changed = bytearray(original)
    position = 4 * (offset + 8)
    struct.pack_into('<i', changed, position, target)
    if changed[:position] != original[:position] or changed[position+4:] != original[position+4:]:
        raise ValueError('change outside the one permitted word')
    restored = bytearray(changed)
    struct.pack_into('<i', restored, position, state[8])
    if restored != original:
        raise ValueError('full-file restoration failed')
    return bytes(changed), dict(byte_offset=position, field='root/STATE-VECTOR(9)',
        previous=state[8], actual=target, unchanged_remainder_bytes=len(original)-4,
        all_other_archive_bytes_identical=True, native_guard_changed=False)


def prepare():
    info, final = base.prepared()
    prior = json.loads((PRIOR / 'result.json').read_text())
    if prior['classification'] != 'FAILED_FROZEN_SENSITIVITY_NO_RETRY' or prior['completed_cases'] != ['cold12_sn8']:
        raise ValueError('expected preserved baseline and failed assembly required')
    if 'FIXED-BASIS SYSTEM DIMENSION MISMATCH' not in (PRIOR / 'cold24_sn8/assembly.log').read_text():
        raise ValueError('the previous failure was not the packaging dimension check')
    for name, wanted in prior['outputs'].items():
        base.require_file(PRIOR / name, wanted)
    OUT.mkdir(exist_ok=False)
    for name in ('inputs', 'runtime', 'AAA'):
        (OUT / name).mkdir()
    shutil.copy2(base.PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    (OUT / 'cold12_sn8').symlink_to((PRIOR / 'cold12_sn8').resolve(), target_is_directory=True)
    inputs = {name: Path(value['path']) for name, value in json.loads((PRIOR / 'execution.json').read_text())['inputs'].items()}
    for name, path in inputs.items():
        (OUT / 'inputs' / (name + '.xsm')).symlink_to(path.resolve())
    original = inputs['basis'].read_bytes()
    with base._open_xsm(inputs['basis']) as archive:
        entry = archive.root['STATE-VECTOR']
    receipts = {}
    for case, nz, sn in NEW_CASES:
        folder = OUT / case
        folder.mkdir()
        # SPOT.f:310, for the retained IELEM=1, ISCAT=3, NREG2D=8.
        target = 8 * (3 * nz + nz + 1 + sn)
        adapted, receipt = adapt_bytes(original, entry, target)
        with (folder / 'basis.xsm').open('xb') as stream:
            stream.write(adapted)
        receipts[case] = dict(**receipt, original=base.pin(inputs['basis']), adapted=base.pin(folder / 'basis.xsm'))
        (folder / 'build.x2m').write_text(base.build_deck(nz, sn).replace("FILE '../inputs/basis.xsm'", "FILE './basis.xsm'"))
        (folder / 'solve.x2m').write_text(base.SOLVE)
    base.write_new(OUT / 'metadata_admission.json', dict(status='PASS_ONE_STORAGE_WORD_ONLY', cases=receipts,
        scope='Reference package reused only for its fixed radial trial space. Storage word now describes the declared new axial layout. All other archive bytes are identical. Native FIXB guard remains active; actual tracking and every frozen radial record must pass before any FLU solve.',
        original_failure=base.pin(PRIOR / 'result.json'), baseline_reused_without_transport=base.pin(PRIOR / 'cold12_sn8/observables.summary.txt')))
    sources = [Path(__file__).resolve(), Path(base.__file__).resolve(), ART / 'axial-material-tools-20261003/export_observables',
        OUT / 'runtime/run_bounded_dragon.py', base.PROD / 'runtime/Dragon', base.PROD / 'prepared.json',
        base.PROD / 'AAA/run_status.json', OUT / 'metadata_admission.json', PRIOR / 'execution.json', PRIOR / 'result.json',
        ART / 'iterative-rank2-h2-r64dp-radialop64-kernel/src-snapshot/SPOASM.f', base.ROOT / 'src/SPOT.f',
        *inputs.values(), *[OUT / case / name for case, _, _ in NEW_CASES for name in ('basis.xsm', 'build.x2m', 'solve.x2m')],
        *[PRIOR / name for name in prior['outputs'] if name.startswith('cold12_sn8/')],
        *[Path(__import__(module).__file__) for module in ('production_runner', 'snapshot_control_preflight', 'qualified_snapshot_ingestion')]]
    charged = math.ceil(prior['elapsed_seconds'])
    base.write_new(OUT / 'execution.json', dict(schema='AXMAT_FROZEN_AXIAL_METADATA_ADAPTATION_V1', declared_unix=time.time(),
        files={str(p.resolve()): base.digest(p) for p in sources}, implementation=base.pin(__file__),
        metadata_admission=base.pin(OUT / 'metadata_admission.json'), original_failed_attempt=base.pin(PRIOR / 'result.json'),
        cases=[dict(name=c, axial_cells=nz, sn=sn) for c, nz, sn in NEW_CASES],
        original_study_wall_seconds=1440, prior_wall_charge_seconds=charged, remaining_wall_seconds=1440-charged,
        stage_caps=dict(assembly=120, axial=300, export=60), threads=1, numeric_children_at_once=1, automatic_retries=0,
        artifact_budget_bytes=24*2**30, min_free_bytes=8*2**30,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        scope='Continue the predeclared two one-factor studies under a fresh packaging declaration. Reuse the original successful cold12_sn8 baseline; never repeat a transport solve. No new radial solve, training, coupled map or CE fitting.',
        unchanged='Same actual native Dragon, original inner/outer controls, physical inputs, all radial/basis bytes except reference root storage word, comparison rules and accuracy gates.',
        success='Native actual TRACK NUNKN equals adapted STATE-VECTOR(9); all 3330 radial/basis records exact; original terminal, positivity, vacuum currents and saved REAL64 authority checks pass. Sensitivity only, no AAA/ABA qualification.'))
    print(json.dumps(dict(execution=base.pin(OUT / 'execution.json'), metadata_admission=base.pin(OUT / 'metadata_admission.json')), indent=2))


def run(expected):
    base.require_file(OUT / 'execution.json', expected)
    declaration = json.loads((OUT / 'execution.json').read_text())
    for name, wanted in declaration['files'].items():
        base.require_file(Path(name), wanted)
    base.prepared()
    native = json.loads((base.CE / 'native_result.json').read_text())
    if native['returncode'] is None or native['status'] == 'RUNNING':
        raise ValueError('CE process is still live')
    if (OUT / 'run_claim.json').exists():
        raise ValueError('no repeat or retry')
    base.write_new(OUT / 'run_claim.json', dict(execution_sha256=expected, started_unix=time.time(), retries=0))
    resources = base.DiskResources(ART, declaration['resource_roots'], declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    runner = base.SerialExecutor(OUT, declaration['remaining_wall_seconds'], 'AAA', resources)
    result = dict(classification='FAILED_METADATA_FROZEN_SENSITIVITY_NO_RETRY', completed_cases=['cold12_sn8'],
        baseline_reused=True, new_completed_cases=[], error=None, independent_accuracy_qualified=False)
    started = time.monotonic()
    try:
        for case, nz, sn in NEW_CASES:
            folder = OUT / case
            runner.execute(folder, 'assembly', [str(base.PROD / 'runtime/Dragon')], 120, 'AXMAT-FROZEN-ASSEMBLY-COMPLETE', 'build.x2m')
            checks = base.structure(folder, nz, sn)
            with base._open_xsm(folder / 'track.xsm') as tr, base._open_xsm(folder / 'basis.xsm') as basis:
                track_state = base.field(tr, tr.root, 'STATE-VECTOR', '<i4')
                basis_state = base.field(basis, basis.root, 'STATE-VECTOR', '<i4')
                if track_state[1] != basis_state[8] or basis_state[8] != 8 * (4*nz+1+sn):
                    raise ValueError('metadata does not match actual native TRACK layout')
                checks.update(actual_track_nunk=int(track_state[1]), adapted_basis_nunk=int(basis_state[8]))
            base.write_new(folder / 'structure.json', checks)
            text = runner.execute(folder, 'solve', [str(base.PROD / 'runtime/Dragon')], 300, 'AXMAT-FROZEN-AXIAL-COMPLETE', 'solve.x2m')
            base.check_terminal(text)
            runner.execute(folder, 'export', [str(ART / 'axial-material-tools-20261003/export_observables'),
                'track.xsm', 'axial.xsm', '../inputs/macro.xsm', 'observables'], 60)
            if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in (folder / 'export.log').read_text().splitlines()):
                raise ValueError('native REAL64 export missing')
            with base._open_xsm(folder / 'axial.xsm') as state:
                k = base.field(state, state.root, 'SPOT-KEFF64', '<f8')
                tag = base.field(state, state.root, 'SPOT-X-KEFF', '<f8')
                if k.size != 1 or k[0] <= 0 or not (k == tag).all():
                    raise ValueError('saved REAL64 eigenvalue authority mismatch')
            result['completed_cases'].append(case)
            result['new_completed_cases'].append(case)
        result['comparisons'] = base.compare()
        result['classification'] = 'COMPLETE_METADATA_FROZEN_AXIAL_SENSITIVITY_ONLY'
    except BaseException as exc:
        result['error'] = repr(exc)
        raise
    finally:
        for name, wanted in declaration['files'].items():
            if base.digest(name) != wanted:
                result.update(classification='INPUT_CHANGED', error='changed: '+name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['total_with_prior_charge_seconds'] = result['elapsed_seconds'] + declaration['prior_wall_charge_seconds']
        result['resources'] = resources.check()
        result['outputs'] = {str(p.relative_to(OUT)):base.digest(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()
            and p.name not in ('execution.json', 'run_claim.json', 'result.json')}
        base.write_new(OUT / 'result.json', result)
    print(json.dumps({key:value for key,value in result.items() if key not in ('outputs','resources')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)

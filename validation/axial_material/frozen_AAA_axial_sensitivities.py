"""Prepare/run one bounded frozen-radial AAA mesh and angular sensitivity study.

No coupled map, new radial solve, common-basis training, CE fitting or promotion.
The cold baseline is required before reporting either one-factor difference.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-compensated-20261004'
OUT = ART / 'axial-material-AAA-frozen-axial-sensitivities-20261004'
CE = ART / 'axial-material-ce-qualified-AAA-ufs-20261004/AAA'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import DiskResources, SerialExecutor, verify_prepared, verify_sealed_directory, require_file
from snapshot_control_preflight import _open_xsm
from qualified_snapshot_ingestion import list_handles

SHA = '2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7'
CASES = [('cold12_sn8', 12, 8), ('cold24_sn8', 24, 8), ('cold12_sn16', 12, 16)]
RECORDS = ['NREG2D', 'NSNAP', 'POD-NMODE', 'VOL2D', 'POD-BASIS',
    'RADIAL-OP', 'RADIAL-OP64', 'DRAGON-TXSC', 'DRAGON-S0XSC']


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(path):
    return dict(path=str(Path(path).resolve()), sha256=digest(path))


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def build_deck(nz, sn):
    mesh = [150 * i / nz for i in range(nz + 1)]
    rows = [' '.join(f'{x:.8E}' for x in mesh[i:i+5]) for i in range(0, nz+1, 5)]
    mixtures = [(i // (nz // 3)) + 1 for i in range(nz)]
    mixrows = [' '.join(map(str, mixtures[i:i+12])) for i in range(0, nz, 12)]
    return f'''* Independently rebuild tracking; frozen radial records must match before FLU.
XSM_FILE SNAP :: FILE '../inputs/radial.xsm' ;
XSM_FILE BASIS_REF :: FILE '../inputs/basis.xsm' ;
XSM_FILE MACRO :: FILE '../inputs/macro.xsm' ;
XSM_FILE SYS_OUT :: FILE './system.xsm' ;
XSM_FILE TRK_OUT :: FILE './track.xsm' ;
LINKED_LIST GEOM TRACK SYSTEM ;
MODULE GEO: SPOT: ASM: END: ;
GEOM := GEO: :: CAR1D {nz}
  X- VOID X+ VOID
  MESHX
  ''' + '\n  '.join(rows) + '''
  MIX
  ''' + '\n  '.join(mixrows) + f''' ;
TRACK := SPOT: GEOM SNAP ::
  EDIT 1 MAXR 2500 TITL 'AAA frozen radial sensitivity'
  ALLG DIAM 0 SN {sn} SCAT 3 ;
SYSTEM := ASM: MACRO TRACK SNAP BASIS_REF :: EDIT 1 SPOD 1 FIXB ;
SYS_OUT := SYSTEM ;
TRK_OUT := TRACK ;
ECHO "AXMAT-FROZEN-ASSEMBLY-COMPLETE" ;
END: ;
QUIT "LIST" .
'''


SOLVE = '''* Cold solve: original axial controls; no warm start or radial update.
XSM_FILE SYSTEM :: FILE './system.xsm' ;
XSM_FILE TRACK :: FILE './track.xsm' ;
XSM_FILE MACRO :: FILE '../inputs/macro.xsm' ;
XSM_FILE AX_OUT :: FILE './axial.xsm' ;
LINKED_LIST AX ;
MODULE FLU: SPOGBAL: SPOSTATE: END: ;
AX := FLU: MACRO TRACK SYSTEM ::
  EDIT -3 TYPE K B1 SIGS EXTE 500 5.00000000E-08 REBA OFF
  ACCE 3 0 UNKT 5.00000000E-08 THER 740 5.00000000E-08 ;
AX := SPOGBAL: AX TRACK SYSTEM MACRO :: ;
AX := SPOSTATE: AX TRACK SYSTEM MACRO :: ;
AX_OUT := AX ;
ECHO "AXMAT-FROZEN-AXIAL-COMPLETE" ;
END: ;
QUIT "LIST" .
'''


def prepared():
    info = verify_prepared(PROD / 'prepared.json', SHA)
    status = json.loads((PROD / 'AAA/run_status.json').read_text())
    if status['classification'] != 'WAITING_REFERENCE' or status['cases']['AAA']['classification'] != 'VALID_MET':
        raise ValueError('same saved numerical fixed point required')
    final = Path(status['cases']['AAA']['final_directory'])
    verify_sealed_directory(final)
    verify_sealed_directory(PROD / 'AAA/bootstrap')
    return info, final


def prepare():
    info, final = prepared()
    OUT.mkdir(exist_ok=False)
    (OUT / 'runtime').mkdir(); (OUT / 'inputs').mkdir(); (OUT / 'AAA').mkdir()
    for name in ('run_bounded_dragon.py',):
        shutil.copy2(PROD / 'runtime' / name, OUT / 'runtime' / name)
    inputs = dict(radial=final / 'candidate_radial.xsm', system=final / 'candidate_system.xsm',
        basis=PROD / 'AAA/bootstrap/basis_reference.xsm', macro=PROD / 'AAA/bootstrap/initial_axial_macrolib.xsm',
        original_track=PROD / 'AAA/bootstrap/initial_axial_track.xsm')
    for name, path in inputs.items():
        (OUT / 'inputs' / (name + '.xsm')).symlink_to(path.resolve())
    for case, nz, sn in CASES:
        folder = OUT / case; folder.mkdir()
        (folder / 'build.x2m').write_text(build_deck(nz, sn))
        (folder / 'solve.x2m').write_text(SOLVE)
    exporter = ART / 'axial-material-tools-20261003/export_observables'
    require_file(exporter, '81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524', True)
    source_files = [Path(__file__).resolve(), Path(sys.modules['production_runner'].__file__),
        Path(sys.modules['snapshot_control_preflight'].__file__), Path(sys.modules['qualified_snapshot_ingestion'].__file__),
        OUT / 'runtime/run_bounded_dragon.py', exporter,
        ROOT / 'validation/axial_material/export_observables.f90', PROD / 'prepared.json', PROD / 'AAA/run_status.json', final / 'result.json',
        Path(info['case_spec']['path']), PROD / 'runtime/Dragon', *inputs.values(),
        *[OUT / case / name for case, _, _ in CASES for name in ('build.x2m', 'solve.x2m')]]
    rules = dict(schema='AXMAT_FROZEN_AAA_AXIAL_ONE_FACTOR_STUDY_V1', declared_unix=time.time(),
        production=pin(PROD / 'prepared.json'), implementation=pin(__file__), files={str(p.resolve()): digest(p) for p in source_files},
        inputs={name: pin(path) for name, path in inputs.items()}, cases=[dict(name=case, axial_cells=nz, sn=sn) for case, nz, sn in CASES],
        threads=1, numeric_children_at_once=1, automatic_retries=0, total_wall_seconds=1440,
        stage_caps=dict(assembly=120, axial=300, observation=60), original_inner_gates_changed=False,
        artifact_budget_bytes=24*2**30, min_free_bytes=8*2**30,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        source_gate='Run only after the UFS native process has ended; never run transport children concurrently.',
        transport_scope='Three cold axial FLU solves only. Frozen final AAA radial operator and common basis; no new radial transport, training or coupled map.',
        structural_admission='All nine physical radial/basis records word-identical in each of 370 groups, vacuum boundaries unchanged, three zones each 50 cm, eight radial regions. Native terminals, saved k and finite positive scalar fields required.',
        comparison='Each state uses its own single global nu-fission normalization. Compare 24-cell flux after conservative two-to-one aggregation onto 12 cells. Report actual k, signed currents and rates without clipping.',
        baseline_admission='The cold12_sn8 result must finish at the original 5e-8 inner gates. Report its difference from the saved map4 state; no redefinition of that state.',
        decision='Sensitivity only, never an additive error attribution or an AAA/ABA qualification. Keep every failed or incomplete case, no repeats. No mesh/angle choice selected to match CE.')
    write_new(OUT / 'execution.json', rules)
    print(json.dumps(dict(classification='FROZEN_AXIAL_STUDY_PREDECLARED_NO_TRANSPORT', execution=pin(OUT / 'execution.json')), indent=2))


def field(a, directory, name, dtype):
    entry = directory[name]
    expected = {'<i4': 1, '<f4': 2, '<f8': 4}[dtype]
    if entry[2] != expected or entry[1] <= 0:
        raise ValueError('invalid record type: ' + name)
    import numpy as np
    return np.frombuffer(a.read(entry[0], entry[1]), dtype=dtype).copy()


def structure(folder, nz, sn):
    count = 0
    with _open_xsm(OUT / 'inputs/system.xsm') as old, _open_xsm(folder / 'system.xsm') as new:
        for previous, actual in zip(list_handles(old, old.root, 'GROUP', 370), list_handles(new, new.root, 'GROUP', 370), strict=True):
            dp = old.directory(previous[0]); dn = new.directory(actual[0])
            for name in RECORDS:
                p = dp[name]; n = dn[name]
                if p[1:] != n[1:] or old.read(p[0], p[1]) != new.read(n[0], n[1]):
                    raise ValueError('frozen radial/basis coefficient changed: ' + name)
                count += 1
    with _open_xsm(folder / 'track.xsm') as tr, _open_xsm(OUT / 'inputs/original_track.xsm') as prior:
        state = field(tr, tr.root, 'STATE-VECTOR', '<i4')
        if state[5] != 8 or state[6] != nz or state[7] != 3:
            raise ValueError('unexpected radial/axial/snapshot track dimensions')
        if field(tr, tr.root, 'U', '<f4').size != sn:
            raise ValueError('unexpected actual polar count')
        zone = field(tr, tr.root, 'MAT1D', '<i4')
        height = field(tr, tr.root, 'VOL1D', '<f4')
        if zone.tolist() != [i // (nz // 3) + 1 for i in range(nz)] or any(height != 150 / nz):
            raise ValueError('physical zone geometry changed')
        for name in ('NCODE', 'ICODE', 'ZCODE', 'AREA2D'):
            p = prior.root[name]; n = tr.root[name]
            if p[1:] != n[1:] or prior.read(p[0], p[1]) != tr.read(n[0], n[1]):
                raise ValueError('physical boundary/radial area changed: ' + name)
    return dict(status='PASS_FROZEN_RADIAL_AND_PHYSICAL_GEOMETRY', records_verified=count,
        axial_cells=nz, sn=sn, new_radial_transport=False)


def check_terminal(text):
    outer = re.findall(r'^\s*FLU2DR-TERM OUTER-GATE=PASS .*EUNK-VALID=1\s*$', text, re.M)
    inner = re.findall(r'^\s*FLU2DR-TERM INNER-TERMINAL .*IGDEB=\s*371 STATE=1 NGRP=\s*370\s*$', text, re.M)
    if len(outer) != 1 or len(inner) != 1:
        raise ValueError('all original native outer/active-inner terminals required')


def compare():
    import numpy as np
    sets = {}
    for case, nz, sn in CASES:
        folder = OUT / case
        rows = list(csv.DictReader((folder / 'observables.regions.csv').open()))
        if len(rows) != 8 * nz or any(int(r['nonpositive_group_flux_count']) != 0 for r in rows):
            raise ValueError('complete positive saved scalar field required')
        summary = {line.split('=', 1)[0]: float(line.split('=', 1)[1]) for line in (folder / 'observables.summary.txt').read_text().splitlines() if '=' in line}
        sets[case] = dict(rows=rows, k=summary['k64'], escape=summary['escape_per_nufission'], nuf=summary['global_nufission'])
    baseline = sets[CASES[0][0]]
    result = {}
    for case, nz, sn in CASES[1:]:
        actual = sets[case]
        values, weights, reference, p_nuf, c_nuf = [], [], [], [], []
        for b in baseline['rows']:
            region = int(b['radial_region']); z = int(b['axial_cell'])
            selected = [r for r in actual['rows'] if int(r['radial_region']) == region and (int(r['axial_cell'])-1) // (nz // 12) + 1 == z]
            if len(selected) != nz // 12:
                raise ValueError('nonconservative nested mesh mapping')
            volume = sum(float(r['volume_cm3']) for r in selected)
            if abs(volume / float(b['volume_cm3']) - 1) > 5e-6:
                raise ValueError('mapped physical volumes changed')
            weights.append(volume)
            values.append(sum(float(r['flux_per_global_nufission']) for r in selected) / volume)
            reference.append(float(b['flux_per_global_nufission']) / float(b['volume_cm3']))
            if region in (4, 5, 6, 7):
                p_nuf.append(float(b['nufission_fraction']))
                c_nuf.append(sum(float(r['nufission_fraction']) for r in selected))
        values=np.array(values); reference=np.array(reference); weights=np.array(weights)
        result[case] = dict(k=actual['k'], signed_reactivity_increment_pcm=1e5*(1/baseline['k']-1/actual['k']),
            signed_escape_per_nufission=actual['escape'], escape_difference=actual['escape']-baseline['escape'],
            scalar_flux_global_normalized_volume_L2=float(np.sqrt(np.dot(weights, (values-reference)**2)/np.dot(weights,reference**2))),
            fuel_fraction_max_relative_change=float(np.max(abs(np.array(c_nuf)/np.array(p_nuf)-1))),
            independently_qualified_coupled_accuracy=False)
    saved = json.loads((ART / 'axial-material-AAA-compensated-closeout-20261004/reference_diagnostics.json').read_text())
    result['cold_baseline'] = dict(k=baseline['k'], signed_escape_per_nufission=baseline['escape'],
        saved_map4_k=1.356393154471719, signed_cold_vs_saved_reactivity_pcm=1e5*(1/1.356393154471719-1/baseline['k']))
    return result


def run(expected):
    require_file(OUT / 'execution.json', expected)
    declaration = json.loads((OUT / 'execution.json').read_text())
    for name, wanted in declaration['files'].items():
        require_file(Path(name), wanted)
    prepared()
    native = json.loads((CE / 'native_result.json').read_text())
    if native['returncode'] is None or native['status'] == 'RUNNING':
        raise ValueError('CE child still active')
    if (OUT / 'run_claim.json').exists():
        raise ValueError('no repeat or retry')
    write_new(OUT / 'run_claim.json', dict(execution_sha256=expected, started_unix=time.time(), retries=0))
    resources = DiskResources(ART, declaration['resource_roots'], declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    runner = SerialExecutor(OUT, 1440, 'AAA', resources)
    result = dict(classification='FAILED_FROZEN_SENSITIVITY_NO_RETRY', completed_cases=[], error=None, independent_accuracy_qualified=False)
    started = time.monotonic()
    try:
        for case, nz, sn in CASES:
            folder = OUT / case
            runner.execute(folder, 'assembly', [str(PROD / 'runtime/Dragon')], 120, 'AXMAT-FROZEN-ASSEMBLY-COMPLETE', 'build.x2m')
            write_new(folder / 'structure.json', structure(folder, nz, sn))
            text = runner.execute(folder, 'solve', [str(PROD / 'runtime/Dragon')], 300, 'AXMAT-FROZEN-AXIAL-COMPLETE', 'solve.x2m')
            check_terminal(text)
            runner.execute(folder, 'export', [str(ART / 'axial-material-tools-20261003/export_observables'),
                'track.xsm', 'axial.xsm', '../inputs/macro.xsm', 'observables'], 60)
            if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in (folder / 'export.log').read_text().splitlines()):
                raise ValueError('saved native REAL64 export failed')
            with _open_xsm(folder / 'axial.xsm') as state:
                k = field(state, state.root, 'SPOT-KEFF64', '<f8')
                tagged = field(state, state.root, 'SPOT-X-KEFF', '<f8')
                if k.size != 1 or k[0] <= 0 or not (k == tagged).all():
                    raise ValueError('saved REAL64 eigenvalue authority mismatch')
            result['completed_cases'].append(case)
        result['comparisons'] = compare()
        result['classification'] = 'COMPLETE_FROZEN_AXIAL_SENSITIVITY_ONLY'
    except BaseException as exc:
        result['error'] = repr(exc)
        raise
    finally:
        for name, wanted in declaration['files'].items():
            if digest(name) != wanted:
                result.update(classification='INPUT_CHANGED', error='changed: ' + name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        result['outputs'] = {str(p.relative_to(OUT)): digest(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()
            and p.name not in ('execution.json', 'run_claim.json', 'result.json')}
        write_new(OUT / 'result.json', result)
    print(json.dumps({key:value for key,value in result.items() if key not in ('outputs','resources')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','run'))
    parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else run(args.sha256)

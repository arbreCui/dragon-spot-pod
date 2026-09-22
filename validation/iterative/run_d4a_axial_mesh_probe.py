#!/usr/bin/env python3
"""One isolated 3/6/12-cell experiment; 30 s per solve, no retry/feedback.

Links one replacement SPOASM object ahead of the existing static libraries.
Never invokes make or changes the canonical executable, archives, or modules.
This is a frozen-radial sensitivity test, not a coupled convergence claim.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

from run_bounded_dragon import run

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / 'bin/Darwin_arm64/Dragon'
CANONICAL_SHA = '2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db'
MAP8 = ROOT / 'validation/artifacts/d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable'
INPUTS = {'radial.xsm': 'candidate_radial.xsm', 'basis.xsm': 'basis_reference.xsm',
          'macro.xsm': 'initial_axial_macrolib.xsm', 'reference.xsm': 'candidate_system.xsm'}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: run_d4a_axial_mesh_probe.py FRESH_OUTPUT_DIRECTORY')
    out = Path(sys.argv[1]).resolve()
    if out.exists():
        raise SystemExit('output already exists; no overwrite or retry')
    if sha(CANONICAL) != CANONICAL_SHA:
        raise SystemExit('canonical identity changed')
    expected = dict((str(Path(line.split()[1].lstrip('*'))), line.split()[0])
                    for line in (MAP8 / 'result.sha256').read_text().splitlines())
    for source in INPUTS.values():
        if sha(MAP8 / source) != expected[source]:
            raise SystemExit('map8 input manifest mismatch: ' + source)
    out.mkdir(parents=True)
    (out / 'inputs').mkdir()
    for target, source in INPUTS.items():
        shutil.copyfile(MAP8 / source, out / 'inputs' / target)
    gan = ROOT / 'Ganlib/lib/Darwin_arm64'
    lib = ROOT / 'lib/Darwin_arm64'
    util = ROOT / 'Utilib/lib/Darwin_arm64/libUtilib.a'
    triv = ROOT / 'Trivac/lib/Darwin_arm64/libTrivac.a'
    libs = [lib / 'libDragon.a', triv, util, gan / 'libGanlib.a']
    sources = [ROOT / 'src/SPOASM.f', Path(__file__).resolve(),
               ROOT / 'validation/iterative/d4a_axial_mesh_probe.x2m',
               ROOT / 'validation/iterative/check_d4a_axial_mesh_probe.f90',
               ROOT / 'src/DRAGON.o', *libs, CANONICAL]
    identities = {str(p): sha(p) for p in sources}
    (out / 'input_identity.json').write_text(json.dumps(identities, indent=2) + '\n')
    commands = [
        ['gfortran', '-O2', '-march=native', '-ffp-contract=off', '-g', '-fPIC',
         '-frecord-marker=4', '-I'+str(gan/'modules'), '-I'+str(lib/'modules'),
         '-c', str(ROOT/'src/SPOASM.f'), '-o', str(out/'SPOASM.o')],
        ['gfortran', '-O2', '-march=native', '-ffp-contract=off', '-g',
         str(ROOT/'src/DRAGON.o'), str(out/'SPOASM.o'), *map(str, libs),
         '-o', str(out/'Dragon_mesh_probe')],
        ['gfortran', '-O0', '-g', '-fcheck=all', '-ffp-contract=off',
         '-I'+str(gan/'modules'), str(sources[3]), str(gan/'libGanlib.a'),
         '-lstdc++', '-o', str(out/'check_mesh')],
    ]
    with (out/'build.log').open('x') as log:
        for command in commands:
            log.write(' '.join(command)+'\n')
            log.flush()
            subprocess.run(command, cwd=out, stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=30)
    template = sources[2].read_text()
    os.environ['OMP_NUM_THREADS'] = '1'
    rows = []
    for label, nf, binary in [('canonical3', 3, CANONICAL),
                              ('candidate3', 3, out/'Dragon_mesh_probe'),
                              ('candidate6', 6, out/'Dragon_mesh_probe'),
                              ('candidate12', 12, out/'Dragon_mesh_probe')]:
        case = out / label
        case.mkdir()
        deck = template.replace('@NFLOOR@', str(nf))
        deck = deck.replace('@MESH@', ' '.join(f'{i*150/nf:.1f}' for i in range(nf+1)))
        deck = deck.replace('@MIX@', ' '.join(str(i//(nf//3)+1) for i in range(nf)))
        for name in INPUTS:
            deck = deck.replace('./'+name, '../inputs/'+name)
        (case/'probe.x2m').write_text(deck)
        start = time.monotonic()
        run(binary, case/'probe.x2m', case/'solve.log', timeout_seconds=30)
        elapsed = time.monotonic()-start
        log = (case/'solve.log').read_text()
        if log.count('>|D4A-AXIAL-MESH-DIAGNOSTIC-COMPLETE') != 1:
            raise SystemExit('deck incomplete: '+label)
        check = subprocess.run([str(out/'check_mesh'), '../inputs/reference.xsm',
                                'system.xsm', 'track.xsm', 'axial.xsm'],
                               cwd=case, capture_output=True, text=True, timeout=10)
        (case/'check.log').write_text(check.stdout+check.stderr)
        check.check_returncode()
        k = float(re.search(r'K64=\s*(\S+)', check.stdout).group(1))
        rates = re.findall(r'^SPORATE NU-FISSION-FRACTIONS (.*)$', log, re.M)
        if len(rates) != 1:
            raise SystemExit('missing/duplicate zone rate')
        row = {'case': label, 'nfloor': nf, 'k64': k, 'seconds': elapsed,
               'zone_nufission_fractions': list(map(float, rates[0].split())),
               'radial_package': 'WORDWISE_UNCHANGED'}
        rows.append(row)
        if label == 'candidate3' and (k != rows[0]['k64'] or
                row['zone_nufission_fractions'] != rows[0]['zone_nufission_fractions']):
            raise SystemExit('candidate/canonical coarse baseline mismatch; no refinement')
        (out/'results.json').write_text(json.dumps({'status': 'DIAGNOSTIC_ONLY',
                                                   'cases': rows}, indent=2)+'\n')
        print(label, f'k={k:.17g}', f'seconds={elapsed:.2f}', flush=True)
    for p in sources:
        if sha(p) != identities[str(p)]:
            raise SystemExit('build input or canonical changed: '+str(p))
    for target, source in INPUTS.items():
        if sha(out/'inputs'/target) != expected[source] or sha(MAP8/source) != expected[source]:
            raise SystemExit('frozen input changed')
    with (out/'result.sha256').open('x') as manifest:
        for path in sorted(out.rglob('*')):
            if path.is_file() and path != out/'result.sha256':
                manifest.write(f'{sha(path)}  {path.relative_to(out)}\n')
    print('D4A AXIAL MESH DIAGNOSTIC COMPLETE; NOT A COUPLED FIXED POINT', flush=True)


if __name__ == '__main__':
    main()

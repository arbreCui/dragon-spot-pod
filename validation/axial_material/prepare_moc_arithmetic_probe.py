"""Build a declared arithmetic contrast in an isolated diagnostic executable.

Each variant stops after its first group solve and two fresh residual reads.
No shared source, library, executable, snapshot controls or tolerance is changed.
"""
import argparse
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256

BASE = ROOT / 'validation/artifacts/axial-material-true-residual-probe-20261003'
BASE_MANIFEST = 'ea43f8e16ed9b0dcef0f3b94442f30838a3caaa04e370a9be449c40ebefb23d3'


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('source anchor is not unique: ' + old[:70])
    return text.replace(old, new)


def candidate(source, variant):
    if variant == 'rhs64':
        source = replace_once(source, ' :: R, G, C, S, FLOUT', ' :: R, G, C, S, FLOUT\n      DOUBLE PRECISION, ALLOCATABLE :: RHS64(:,:)')
        source = replace_once(source, '      ALLOCATE(DENOM', '      ALLOCATE(RHS64(NUN,NGEFF))\n      ALLOCATE(DENOM')
        source = replace_once(source, 'IF(NCONV(II)) RHS(:,II)=REAL(FLOUT(:,II))', 'IF(NCONV(II)) RHS64(:,II)=FLOUT(:,II)')
        source = replace_once(source, 'V(:,:,K+1)=V(:,:,K)-FLOUT(:,:)+RHS(:,:)', 'V(:,:,K+1)=V(:,:,K)-FLOUT(:,:)+RHS64(:,:)')
    else:
        begin = source.index('        IF(RHSFLG) THEN')
        end = source.index('*---\n*   GMRES(1) iteration', begin)
        source = source[:begin] + '        RHS(:,:)=0.0\n' + source[end:]
        source = replace_once(source, 'NFUNL,KEYFLX,KEYCUR,QFR,GAR(1,1)', 'NFUNL,KEYFLX,KEYCUR,RHS,GAR(1,1)')
        source = replace_once(source, 'V(:,:,K+1)=V(:,:,K)-FLOUT(:,:)+RHS(:,:)', 'V(:,:,K+1)=V(:,:,K)-FLOUT(:,:)')
        if variant == 'homogeneous_single_round':
            source = replace_once(source,
                '          DO J=1,K\n            PHIIN(:,II)=PHIIN(:,II)+REAL(G(J,II)*V(:,II,J))\n          ENDDO',
                '          R(:,II)=DBLE(PHIIN(:,II))\n          DO J=1,K\n            R(:,II)=R(:,II)+G(J,II)*V(:,II,J)\n          ENDDO\n          PHIIN(:,II)=REAL(R(:,II))')
    for line in source.splitlines():
        if line and line[0] not in '*cC!' and len(line) > 72:
            raise ValueError('fixed form line too long: ' + line)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('variant', choices=['rhs64', 'homogeneous', 'homogeneous_single_round'])
    args = parser.parse_args()
    base = json.loads(require_file(BASE / 'execution.json', BASE_MANIFEST).read_text())
    for name, digest in base['files'].items():
        require_file(Path(name), digest)
    work = ROOT / ('validation/artifacts/axial-material-moc-' + args.variant.replace('_', '-') + '-20261003')
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'A'):
        (work / name).mkdir()
    for name in ('SPOASM.o', 'FLU.o', 'FLU2DR.o', 'FLU2DR64.o'):
        shutil.copy2(BASE / 'build' / name, work / 'build' / name)
    for name in ('production_runner.py', 'production_inputs.py', 'run_bounded_dragon.py', 'run_probe.py'):
        shutil.copy2(BASE / 'runtime' / name, work / 'runtime' / name)
    for name in ('snapshot.x2m', 'geometry.dat', 'material.xsm'):
        shutil.copy2(BASE / 'A' / name, work / 'A' / name)
    source = (BASE / 'build/MCGMRE_probe.f').read_text()
    changed = candidate(source, args.variant)
    target = work / 'build/MCGMRE_probe.f'
    target.write_text(changed)
    (work / 'build/contrast.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True), changed.splitlines(True), fromfile='original_probe', tofile=args.variant)))
    commands = json.loads((BASE / 'build/include_path_fix.json').read_text())['commands']
    commands = [[part.replace(str(BASE), str(work)) for part in command] for command in commands]
    protected = json.loads((BASE / 'protocol.json').read_text())['protected_base']
    protocol = dict(schema='AXMAT_MOC_ARITHMETIC_CONTRAST_V1', declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        user_authorization='可以 继续', variant=args.variant, wall_seconds=60, automatic_retries=0, threads=1,
        scope='First native group solve and two identical fresh applications, then deliberate STOP. Same material, map used for the residual, controls, and tolerances as the original probe. No snapshot or physics acceptance.',
        changes={'rhs64':'Retain F(0) in binary64 before affine subtraction; everything else unchanged.',
                 'homogeneous':'Apply the native map with zero source to each Krylov direction; avoid affine subtraction. Original source retained for residual and solution.',
                 'homogeneous_single_round':'Homogeneous direction application plus accumulate the complete correction in binary64, then round the returned vector once.'}[args.variant],
        base_execution_sha256=BASE_MANIFEST, build_commands=commands, build_wall_seconds_per_command=60,
        source_sha256=sha256(target), protected_base=protected,
        promotion_policy='Diagnostic candidate only; a recurrence estimate cannot authorize promotion. Physical and returned-vector gates remain unchanged.')
    dump_json(work / 'protocol.json', protocol)
    with (work / 'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=60)
    for name, digest in base['files'].items():
        require_file(Path(name), digest)
    roots = sorted(str(p.resolve()) for p in (ROOT / 'validation/artifacts').glob('axial-material-*') if p.is_dir())
    files = {str(p.resolve()):sha256(p) for p in work.rglob('*') if p.is_file()}
    files.update(protected)
    files[str(Path(__file__).resolve())] = sha256(Path(__file__))
    manifest = dict(schema='AXMAT_POSTUPDATE_RESIDUAL_EXECUTION_V1', wall_seconds=60, automatic_retries=0,
                    artifact_root=str(ROOT / 'validation/artifacts'), resource_roots=roots, files=files,
                    scope=protocol['scope'])
    dump_json(work / 'execution.json', manifest)
    print(json.dumps(dict(path=str(work / 'execution.json'), sha256=sha256(work / 'execution.json'))))


if __name__ == '__main__':
    main()

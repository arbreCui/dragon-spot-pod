"""Derive source isolation from the exact coefficient used by native MCGSCA."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-pjj64-ilufix-20261003'
    manifest = json.loads(require_file(base / 'execution.json',
        '2e4413bf91a583501ded51df9f1e5fb3b20ad46c08dd722ce234e1ae0e515aba').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    observed = json.loads((base / 'audit_initialized/observations.json').read_text())
    if observed['classification'] != 'R64_SNAPSHOT_TERMINAL_AUDIT_FAIL':
        raise ValueError('preserved unchanged-threshold failure required')
    work = ROOT / 'validation/artifacts/axial-material-r64-kernel-consistency-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'audit_build'):
        shutil.copytree(base / name, work / name,
            ignore=shutil.ignore_patterns('__pycache__', 'build.log', 'build_readonly_memory.log'))
    (work / 'A').mkdir()
    for name in ('material.xsm', 'geometry.dat', 'seed_A.xsm', 'snapshot.x2m'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    original = (ROOT / 'src/MCGDSCA.f').read_text()
    source = original.replace('DOUBLE PRECISION W,H(NSUB),PJJ(NREG,NPJJM)',
        'DOUBLE PRECISION W,H(NSEG),PJJ(NREG,NPJJM)', 1)
    start = source.index('            IF(TAUD.LE.TAUDMIN) THEN')
    stop = source.index('            EXPTD=EXPTD*W*HID', start)
    source = source[:start] + '''*           Match the native flight coefficient MCGSCA exactly:
*           B=H*(E0+E1*TAUD), with the same index and arithmetic.
*           Its complementary isolated source is (H-B)/TRI.
            IF(TRI.EQ.0.D0) THEN
              EXPTD=0.5D0*HID
            ELSE IF(REAL(TAUD).GE.XLIM1) THEN
              EXPTD=(1.D0-1.D0/TAUD)/TRI
            ELSE
              LAU=INT(TAUD*PAS1)
              EXPTD=(1.D0-(E0(LAU)+E1(LAU)*TAUD))/TRI
            ENDIF
''' + source[stop:]
    p = work / 'build/MCGDSCA.f'
    p.write_text(source)
    p.with_suffix('.f.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), source.splitlines(True),
        fromfile='MCGDSCA.f', tofile=str(p))))
    old = json.loads((base / 'protocol.json').read_text())
    commands = [[arg.replace(str(base), str(work)) for arg in command]
                for command in old['build_commands']]
    compile_command = list(commands[0])
    compile_command[compile_command.index('-c') + 1] = str(p)
    compile_command[compile_command.index('-o') + 1] = str(p.with_suffix('.o'))
    link = commands[2]
    link.insert(link.index(str(ROOT / 'lib/Darwin_arm64/libDragon.a')), str(p.with_suffix('.o')))
    commands.insert(2, compile_command)
    if not all(commands[3].count(str(work / 'build' / name)) == 1
               for name in ('MCGASM.o', 'MCGFST.o', 'MCGDSCA.o')):
        raise ValueError('all new objects must be explicitly linked')
    protocol = dict(old, schema='AXMAT_PJJ64_NATIVE_KERNEL_CONSISTENCY_V5',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        kernel_correction='Derive the isolated source coefficient from the identical '
        'tabulated flight coefficient used by unchanged native MCGSCA. Remove its '
        'separate small-tau Taylor approximation and rounded interpolation argument. '
        'Correct the legacy H(NSUB) declaration to its actual H(NSEG) extent. '
        'Keep input physical model, native flight kernel, original acceptance and work targets.',
        build_commands=commands, predecessor_audit_sha256=sha256(base / 'audit_initialized/observations.json'),
        source_inputs={**old['source_inputs'],
            str(ROOT / 'src/MCGDSCA.f'): sha256(ROOT / 'src/MCGDSCA.f'),
            str(ROOT / 'src/MCGSCA.f'): sha256(ROOT / 'src/MCGSCA.f')})
    dump_json(work / 'protocol.json', protocol)
    with (work / 'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command, cwd=work / 'build', check=True,
                           stdout=log, stderr=subprocess.STDOUT, timeout=60)
    dump_json(work / 'audit_build/build_command.json', commands[-1])
    (work / 'audit_build/build_readonly_memory.log').write_bytes((work / 'build/build.log').read_bytes())
    files = dict(manifest['files'])
    files.update(protocol['source_inputs'])
    files.update({str(p): sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base / 'audit_initialized/observations.json', Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    dump_json(work / 'execution.json', dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',
        mode='snapshot_A', wall_seconds=600, automatic_retries=0,
        artifact_root=str(ROOT / 'validation/artifacts'),
        resource_roots=sorted(str(p.resolve()) for p in
            (ROOT / 'validation/artifacts').glob('axial-material-*') if p.is_dir()), files=files))
    print(sha256(work / 'execution.json'))


if __name__ == '__main__':
    main()

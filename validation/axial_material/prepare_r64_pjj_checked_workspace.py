"""Keep runtime checks and allocate unused LPS=0 interface workspaces."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-pjj64-linkfix-20261003'
    manifest = json.loads(require_file(base / 'execution.json',
        '4cb96506a56e440846943ed45d3518e644d4f5e9aebba011f50d9783a10a7b1b').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    status = json.loads((base / 'run_status.json').read_text())
    if status['classification'] != 'FAILED_NO_RETRY' or not status['frozen_inputs_unchanged']:
        raise ValueError('preserved checked-runtime rejection required')
    if "actual argument 'psj' is not allocated" not in (base / 'A/solve.log').read_text():
        raise ValueError('unexpected predecessor failure')
    work = ROOT / 'validation/artifacts/axial-material-r64-pjj64-workspacefix-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'audit_build'):
        shutil.copytree(base / name, work / name,
            ignore=shutil.ignore_patterns('__pycache__', 'build.log', 'build_readonly_memory.log'))
    (work / 'A').mkdir()
    for name in ('material.xsm', 'geometry.dat', 'seed_A.xsm', 'snapshot.x2m'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    p = work / 'build/MCGASM.f'
    source = p.read_text()
    before = '            PSJZ(:LPS*NGEFF)=0.0\n         ENDIF'
    after = '''            PSJZ(:LPS*NGEFF)=0.0
         ELSE
*           The native fixed-shape interface still receives these arrays
*           when LPS=0, although its surface-source branch is inactive.
            ALLOCATE(PSJ(1),PSJX(1),PSJY(1),PSJZ(1))
            PSJ=0.0
            PSJX=0.0
            PSJY=0.0
            PSJZ=0.0
         ENDIF'''
    if source.count(before) != 1:
        raise ValueError('unexpected allocation anchor')
    source = source.replace(before, after, 1)
    before = '         IF(LPS.GT.0) DEALLOCATE(PSJ,PSJX,PSJY,PSJZ)'
    if source.count(before) != 1:
        raise ValueError('unexpected deallocation anchor')
    source = source.replace(before, '         DEALLOCATE(PSJ,PSJX,PSJY,PSJZ)', 1)
    p.write_text(source)
    p.with_suffix('.f.patch').write_text(''.join(difflib.unified_diff(
        (ROOT / 'src/MCGASM.f').read_text().splitlines(True), source.splitlines(True),
        fromfile='MCGASM.f', tofile=str(p))))
    old = json.loads((base / 'protocol.json').read_text())
    commands = [[arg.replace(str(base), str(work)) for arg in command]
                for command in old['build_commands']]
    if not all(commands[2].count(str(work / 'build' / name)) == 1
               for name in ('MCGASM.o', 'MCGFST.o')):
        raise ValueError('new objects must be explicitly linked')
    protocol = dict(old, schema='AXMAT_PJJ64_CHECKED_WORKSPACE_V3',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        interface_correction='With all runtime checks retained, allocate initialized one-element '
        'unused surface-source workspaces for the native LPS=0 fixed-shape interface. '
        'No active coefficient, geometry, material, work tolerance or acceptance change.',
        build_commands=commands, predecessor_status_sha256=sha256(base / 'run_status.json'))
    dump_json(work / 'protocol.json', protocol)
    with (work / 'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command, cwd=work / 'build', check=True,
                           stdout=log, stderr=subprocess.STDOUT, timeout=60)
    dump_json(work / 'audit_build/build_command.json', commands[-1])
    (work / 'audit_build/build_readonly_memory.log').write_bytes((work / 'build/build.log').read_bytes())
    files = dict(manifest['files'])
    files.update({str(p): sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base / 'run_status.json', base / 'A/solve.log', Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    dump_json(work / 'execution.json', dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',
        mode='snapshot_A', wall_seconds=600, automatic_retries=0,
        artifact_root=str(ROOT / 'validation/artifacts'),
        resource_roots=sorted(str(p.resolve()) for p in
            (ROOT / 'validation/artifacts').glob('axial-material-*') if p.is_dir()), files=files))
    print(sha256(work / 'execution.json'))


if __name__ == '__main__':
    main()

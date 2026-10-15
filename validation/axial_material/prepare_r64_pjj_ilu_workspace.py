"""Preserve both checked interface rejections; allocate inactive ILU storage."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-pjj64-workspacefix-20261003'
    manifest = json.loads(require_file(base / 'execution.json',
        'abac10504412c0e506e6c6181fbc658d4aca838fb8f901ce0a77631e2e802548').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    status = json.loads((base / 'run_status.json').read_text())
    if status['classification'] != 'FAILED_NO_RETRY' or not status['frozen_inputs_unchanged']:
        raise ValueError('preserved checked-runtime rejection required')
    if "actual argument 'lucf' is not allocated" not in (base / 'A/solve.log').read_text():
        raise ValueError('unexpected predecessor failure')
    work = ROOT / 'validation/artifacts/axial-material-r64-pjj64-ilufix-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'audit_build'):
        shutil.copytree(base / name, work / name,
            ignore=shutil.ignore_patterns('__pycache__', 'build.log', 'build_readonly_memory.log'))
    (work / 'A').mkdir()
    for name in ('material.xsm', 'geometry.dat', 'seed_A.xsm', 'snapshot.x2m'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    p = work / 'build/MCGASM.f'
    source = p.read_text()
    before = '            IF(LC0.GT.0) ALLOCATE(LUCF(LC0))'
    after = '''*           LC0=0 disables this branch; a valid empty-interface owner
*           is still needed by the native fixed-shape argument list.
            ALLOCATE(LUCF(MAX(1,LC0)))
            LUCF=0.0'''
    if source.count(before) != 1:
        raise ValueError('unexpected ILU allocation anchor')
    source = source.replace(before, after, 1)
    before = '            IF(LC0.GT.0) DEALLOCATE(LUCF)'
    if source.count(before) != 1:
        raise ValueError('unexpected ILU deallocation anchor')
    source = source.replace(before, '            DEALLOCATE(LUCF)', 1)
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
    protocol = dict(old, schema='AXMAT_PJJ64_CHECKED_ILU_WORKSPACE_V4',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        ilu_interface_correction='Allocate one initialized unused LUCF value for LC0=0. '
        'Retain full runtime checks, prior PSJ correction, unchanged active coefficients '
        'and all physical inputs and acceptance thresholds.',
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

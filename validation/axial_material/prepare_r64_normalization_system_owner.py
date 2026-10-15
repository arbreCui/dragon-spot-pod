"""Retain the native read-only TRACK contract; store normalization on SYSTEM."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-track-normalization-20261003'
    manifest = json.loads(require_file(base / 'execution.json',
        'b4e7d76b2c85f9c08724d31d0f52c49ad1422c28f7fb6bf17aa2d71c03812bfe').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    status = json.loads((base / 'run_status.json').read_text())
    if status['classification'] != 'FAILED_NO_RETRY' or not status['frozen_inputs_unchanged']:
        raise ValueError('preserved owner rejection required')
    if "THE OBJECT 'TRACK' IS OPEN IN READ-ONLY MODE" not in (base / 'A/solve.log').read_text():
        raise ValueError('unexpected predecessor failure')
    work = ROOT / 'validation/artifacts/axial-material-r64-system-normalization-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'audit_build'):
        shutil.copytree(base / name, work / name,
            ignore=shutil.ignore_patterns('__pycache__', 'build.log', 'build_readonly_memory.log'))
    (work / 'A').mkdir()
    for name in ('material.xsm', 'geometry.dat', 'seed_A.xsm', 'snapshot.x2m'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    p = work / 'build/MCGASM.f'
    source = p.read_text()
    anchor = "      CALL LCMPUT(IPTRK,'AXMAT-V64',14,4,AXV64)\n"
    if source.count(anchor) != 1:
        raise ValueError('unexpected read-only owner mutation')
    p.write_text(source.replace(anchor, '', 1))
    p = work / 'audit_build/audit_r64_snapshot.f90'
    source = p.read_text()
    anchor = "  call require(track,'AXMAT-V64',nu,4);call LCMGET(track,'AXMAT-V64',volume64)"
    if source.count(anchor) != 1:
        raise ValueError('unexpected auditor owner')
    source = source.replace(anchor, "  g=LCMGIL(sg,1)\n  call require(g,'AXMAT-V64',nu,4);call LCMGET(g,'AXMAT-V64',volume64)", 1)
    p.write_text(source.replace('group/track volume64 mismatch', 'group volume64 mismatch'))
    old = json.loads((base / 'protocol.json').read_text())
    commands = [[arg.replace(str(base), str(work)) for arg in command]
                for command in old['build_commands']]
    protocol = dict(old, schema='AXMAT_BINARY64_SYSTEM_NORMALIZATION_V7',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        owner_correction='Native ASM receives TRACK read-only. Keep this contract: '
        'save AXMAT-V64 only under each writable SYSTEM group. Auditor requires '
        'all 370 copies to agree bit-for-bit and independently replays the original '
        'track file and quadrature. No numerical formula or acceptance change.',
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

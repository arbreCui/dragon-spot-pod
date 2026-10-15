"""Prepare B using the exact certified A runtime and original sealed B material."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess

from export_r64_tracking_moments import SOURCE as MOMENT_SOURCE
from production_runner import ROOT, DiskResources, dump_json, require_file, sha256


def main():
    art = ROOT / 'validation/artifacts'
    base = art / 'axial-material-r64-system-normalization-20261003'
    qualified = art / 'axial-material-r64-A-qualified-20261003'
    require_file(qualified / 'result.sha256', '74fbca143d0a4909e21e40a4ec9227990e6c6f13956f595e17bc94ed010868bf')
    for line in (qualified / 'result.sha256').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require_file(qualified / name, wanted)
    receipt = json.loads((qualified / 'producer_receipt.json').read_text())
    if not receipt['snapshot_A_binary64_qualified'] or receipt['production_qualified']:
        raise ValueError('qualified offline A producer required')
    for name in ('producer_runtime', 'snapshot', 'execution', 'audit_status', 'qualification'):
        item = receipt[name]
        require_file(Path(item['path']), item['sha256'])
    manifest = json.loads((base / 'execution.json').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    material = art / 'axial-material-inputs-20261003'
    inputs = json.loads(require_file(material / 'material_inputs.json',
        '935223ea827afe403a1ad5cdc8198fc38f9276d487839d7efa4a159f5c374916').read_text())
    results = json.loads((material / 'material_results.json').read_text())
    config = inputs['config']
    if tuple(config[k] for k in ('pu_B','u_B','fuel_C','clad_C','sodium_C')) != (.2436,.7564,750.,620.,475.):
        raise ValueError('B composition or temperature differs from the agreed case')
    require_file(material / 'B/material.xsm', '6a533b9ee07fbd58f48c1bd0d0c6d587bbff7c2764f00679a2fd7ea519f7c6be')
    require_file(material / 'B/material_audit.json', results['states']['B']['material_audit_sha256'])
    require_file(material / 'B/snapshot_B.xsm', results['states']['B']['archive_sha256'])
    if sha256(material / 'B/geometry.dat') != sha256(base / 'A/geometry.dat'):
        raise ValueError('A/B geometry differs')
    work = art / 'axial-material-r64-snapshot-B-20261004'
    resource_roots = sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir()) + [str(work)]
    resources = DiskResources(art, resource_roots, 8*2**30, 12*2**30)
    resources_before = resources.check()
    work.mkdir(exist_ok=False)
    runtime = work / 'runtime'; runtime.mkdir()
    shutil.copy2(base / 'runtime/Dragon', runtime / 'Dragon')
    for name in ('production_runner.py','production_inputs.py','run_r64_material_snapshot.py',
                 'run_r64_material_snapshot_audit.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
                 'check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
        shutil.copy2(Path(__file__).with_name(name), runtime / name)
    (work / 'B').mkdir()
    for name in ('material.xsm','geometry.dat'):
        shutil.copy2(material / 'B' / name, work / 'B' / name)
    shutil.copy2(material / 'B/snapshot_B.xsm', work / 'B/seed_B.xsm')
    deck = (base / 'A/snapshot.x2m').read_text().replace('seed_A.xsm','seed_B.xsm').replace('snapshot_A.xsm','snapshot_B.xsm').replace('AXMAT-SNAPSHOT-A-COMPLETE','AXMAT-SNAPSHOT-B-COMPLETE')
    (work / 'B/snapshot.x2m').write_text(deck)
    built = work / 'audit_build'; built.mkdir()
    source = built / 'audit_r64_snapshot.f90'
    source.write_text((base / 'audit_initialized/audit_r64_snapshot.f90').read_text().replace('snapshot_A.xsm','snapshot_B.xsm'))
    moment = built / 'export_tracking.f90'
    moment.write_text(MOMENT_SOURCE.replace('snapshot_A.xsm','snapshot_B.xsm'))
    original_command = json.loads((base / 'audit_initialized/build_command.json').read_text())
    commands = []
    for program, executable in ((source, 'audit_snapshot'), (moment, 'export_tracking')):
        command = [str(program) if x.endswith('/audit_r64_snapshot.f90') else
            '-J'+str(built) if x.startswith('-J') else x for x in original_command]
        command[command.index('-o') + 1] = str(built / executable)
        commands.append(command)
    dump_json(built / 'build_commands.json', commands)
    protocol = dict(schema='AXMAT_R64_B_WITH_CERTIFIED_A_PRODUCER_V1', state='B',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        wall_seconds=600, automatic_retries=0, threads=1,
        scope='Fresh B TYPE-K solve from the original separately sealed B TONE material. '
              'Use the exact certified A runtime; original B binary32 snapshot is only an initial guess. '
              'No new nuclear-data processing, material recipe, geometry, temperature or gate change.',
        producer_runtime_sha256=receipt['producer_runtime']['sha256'],
        composition={'pu':.2436,'u':.7564}, temperatures_C={'fuel_and_hole':750,'clad_and_gap':620,'sodium':475},
        acceptance='Original bare saved-state/source/balance/geometry and mirror gates, plus '
                   'independent track normalization replay and all rejection controls.',
        work_targets={'radial':2.5e-10,'thermal':2.5e-9},
        declared_controls={'outer':2.5e-7,'mccg':2.5e-8},
        material_limit=json.loads((material / 'B/material_audit.json').read_text())['limits'],
        build_commands=commands, resources_before=resources_before)
    dump_json(work / 'protocol.json', protocol)
    with (built / 'build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command, cwd=built, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=60)
    files = dict(manifest['files'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (qualified / 'result.sha256', qualified / 'producer_receipt.json', qualified / 'verification.json',
              material / 'material_inputs.json', material / 'material_results.json', material / 'B/material_audit.json',
              material / 'B/material.xsm', material / 'B/snapshot_B.xsm', Path(__file__).resolve(),
              Path(__file__).with_name('export_r64_tracking_moments.py')):
        files[str(p)] = sha256(p)
    dump_json(work / 'execution.json', dict(schema='AXMAT_R64_MATERIAL_SNAPSHOT_V1', state='B',
        wall_seconds=600, automatic_retries=0, threads=1, artifact_root=str(art),
        resource_roots=resource_roots, files=files))
    print(json.dumps({'execution':str(work / 'execution.json'), 'sha256':sha256(work / 'execution.json'),
                      'producer_runtime_unchanged':sha256(runtime / 'Dragon') == receipt['producer_runtime']['sha256']}, indent=2))


if __name__ == '__main__':
    main()

"""Audit an actual saved A/B state and independently replay normalization owners."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import time

from analyze_r64_snapshot import analyze
from analyze_r64_tracking_moments import analyze as analyze_moments
from check_r64_audit_rejections import check as check_snapshot
from check_r64_normalization_rejections import check as check_normalization
from production_runner import DiskResources, SerialExecutor, dump_json, require_file, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('execution', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    execution = args.execution.resolve()
    work = execution.parent
    c = json.loads(require_file(execution, args.sha256).read_text())
    if c['schema'] != 'AXMAT_R64_MATERIAL_SNAPSHOT_V1' or c['state'] not in ('A', 'B'):
        raise ValueError('undeclared audit state')
    for name, wanted in c['files'].items():
        require_file(Path(name), wanted)
    state = c['state']
    status = json.loads((work / 'run_status.json').read_text())
    if status['classification'] != 'R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT' or not status['frozen_inputs_unchanged']:
        raise ValueError('immutable completed snapshot required')
    for name, wanted in status['outputs'].items():
        require_file(work / state / name, wanted)
    out = work / 'audit_initialized'
    out.mkdir(exist_ok=False)
    for name in (f'snapshot_{state}.xsm', 'radial_track.bin'):
        shutil.copy2(work / state / name, out / name)
    built = work / 'audit_build'
    for name in ('audit_snapshot', 'export_tracking', 'audit_r64_snapshot.f90', 'export_tracking.f90', 'build_commands.json'):
        shutil.copy2(built / name, out / name)
    files = {str(p): sha256(p) for p in out.iterdir() if p.is_file()}
    files.update({str(execution): args.sha256, str(work / 'run_status.json'): sha256(work / 'run_status.json')})
    protocol = dict(schema='AXMAT_R64_STATE_AND_NORMALIZATION_AUDIT_V1', state=state,
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        audit_wall_seconds=60, owner_export_wall_seconds=60, automatic_retries=0, threads=1,
        scope='Same standalone initialized native bare-image audit as qualified A. '
              'Also require all PJJ mirrors, 370 identical volume64 owners, actual '
              'saved quadrature export, independent track replay and rejection controls.',
        acceptance={'scalar_image_defect':2.5e-7,'full_image_defect':2.5e-7,
                    'balance_keff_relative_defect':2.5e-7,'geometry_relative_error':5e-6,
                    'volume64_independent_replay_relative_error':2e-12}, files=files)
    dump_json(out / 'protocol.json', protocol)
    protocol_sha = sha256(out / 'protocol.json')
    with (out / 'claim.json').open('x') as stream:
        json.dump(dict(started_unix=time.time(), protocol_sha256=protocol_sha), stream)
    resources = DiskResources(Path(c['artifact_root']), c['resource_roots'], 8*2**30, 12*2**30)
    runner = SerialExecutor(work, 120, state, resources)
    result = dict(classification='AUDIT_FAILED_NO_RETRY', state=state, snapshot_qualified=False,
        production_qualified=False, protocol_sha256=protocol_sha, resources_before=resources.check())
    start = time.monotonic()
    try:
        for executable, log in (('audit_snapshot', 'audit.log'), ('export_tracking', 'tracking_export.log')):
            with (out / log).open('xb') as stream:
                runner._process([str(out / executable)], out, subprocess.DEVNULL, stream, 60)
        if (out / 'audit.log').read_text().count('AXMAT-R64-SNAPSHOT-AUDIT-EXPORTED') != 1:
            raise ValueError('incomplete numerical audit export')
        if (out / 'tracking_export.log').read_text().count('AXMAT-TRACKING-MOMENTS-EXPORTED') != 1:
            raise ValueError('incomplete tracking owner export')
        observed = analyze(out / 'audit.bin')
        normalization = analyze_moments(out / 'radial_track.bin', out / 'moments.bin', out / 'volume64.bin')
        rejected = check_snapshot(out / 'audit.bin')
        normalization_rejected = check_normalization(out / 'radial_track.bin', out / 'moments.bin', out / 'volume64.bin')
        for name, value in (('observations.json', observed), ('volume_normalization_check.json', normalization),
                            ('negative_controls.json', rejected), ('normalization_negative_controls.json', normalization_rejected)):
            dump_json(out / name, value)
        result['classification'] = observed['classification']
        result['snapshot_qualified'] = observed['classification'] == 'R64_SNAPSHOT_TERMINAL_AUDIT_PASS'
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic() - start
        try:
            require_file(out / 'protocol.json', protocol_sha)
            for name, wanted in {**c['files'], **files}.items():
                require_file(Path(name), wanted)
            result['frozen_inputs_unchanged'] = True
        except BaseException as error:
            result.update(classification='INPUT_IDENTITY_FAILURE', identity_error=repr(error), snapshot_qualified=False)
        result['outputs'] = {p.name: sha256(p) for p in out.iterdir() if p.is_file() and
            p.name != 'run_status.json' and str(p) not in files}
        result['resources_after'] = resources.check()
        dump_json(out / 'run_status.json', result)
    print(json.dumps({k: v for k, v in result.items() if not k.startswith('resources')}, indent=2))


if __name__ == '__main__':
    main()

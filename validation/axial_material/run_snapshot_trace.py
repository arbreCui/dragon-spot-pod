#!/usr/bin/env python3
"""One freshly declared, bounded A-state residual observation; no retries."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from production_runner import DiskResources, SerialExecutor, dump_json, require_file, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    work = manifest.parent
    contract = json.loads(require_file(manifest, args.sha256).read_text())
    if (contract['schema'] != 'AXMAT_A_RESIDUAL_TRACE_V1' or
            contract['wall_seconds'] != 600 or contract['state'] != 'A' or
            contract['automatic_retries'] != 0):
        raise RuntimeError('undeclared diagnostic scope')

    def verify():
        require_file(manifest, args.sha256)
        for path, expected in contract['files'].items():
            require_file(Path(path), expected)

    verify()
    resources = DiskResources(Path(contract['artifact_root']), contract['resource_roots'],
                              8 * 2**30, 12 * 2**30)
    resources.check()
    folder = work / 'A'
    for name in ('snapshot.log', 'snapshot_A.xsm', 'radial_track.bin', 'stages.json'):
        if (folder / name).exists():
            raise RuntimeError('existing output; no retry: ' + name)
    with (work / 'run_claim.json').open('x') as stream:
        json.dump(dict(manifest_sha256=args.sha256, pid=os.getpid(),
                       started_unix=time.time(), automatic_retries=0), stream, indent=2)
    previous = {sig: signal.signal(sig, signal.default_int_handler)
                for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    result = dict(classification='RUNNING', scientific_accuracy_accepted=False,
                  material_recomputed=False, manifest_sha256=args.sha256)
    runner = SerialExecutor(work, 600, 'A', resources)
    runner.env['GFORTRAN_UNBUFFERED_ALL'] = '1'
    try:
        runner.execute(folder, 'snapshot', [str(work / 'runtime/Dragon')], 600,
                       'AXMAT-SNAPSHOT-A-COMPLETE', 'snapshot.x2m')
        result['classification'] = 'NATIVE_COMPLETE_PENDING_INDEPENDENT_AUDIT'
    except subprocess.TimeoutExpired as error:
        result.update(classification='DIAGNOSTIC_TIME_LIMIT', error=str(error))
    except BaseException as error:
        result.update(classification='FAILED_NO_RETRY', error=repr(error))
        raise
    finally:
        result['finished_unix'] = time.time()
        result['stages'] = runner.records
        result['output_hashes'] = {p.name: sha256(p) for p in folder.iterdir()
                                   if p.is_file() and p.name not in ('material.xsm', 'geometry.dat', 'snapshot.x2m')}
        try:
            verify()
            result['frozen_inputs_unchanged'] = True
        except BaseException as error:
            result.update(classification='INPUT_IDENTITY_FAILURE', identity_error=repr(error))
        dump_json(work / 'run_status.json', result)
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

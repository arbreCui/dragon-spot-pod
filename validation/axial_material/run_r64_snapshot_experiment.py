"""Execute one immutable, bounded double-precision snapshot experiment."""
import argparse
import json
import os
from pathlib import Path
import signal
import time

from production_runner import DiskResources, SerialExecutor, dump_json, require_file, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    work = manifest.parent
    c = json.loads(require_file(manifest, args.sha256).read_text())
    if c['schema'] != 'AXMAT_R64_SNAPSHOT_EXPERIMENT_V1' or c['automatic_retries'] != 0:
        raise ValueError('undeclared scope')
    if (c['mode'], c['wall_seconds']) not in (('first_call_probe', 60), ('snapshot_A', 600)):
        raise ValueError('undeclared mode/budget')
    def verify():
        require_file(manifest, args.sha256)
        for name, wanted in c['files'].items():
            require_file(Path(name), wanted)
    verify()
    resources = DiskResources(Path(c['artifact_root']), c['resource_roots'], 8*2**30, 12*2**30)
    result = dict(classification='FAILED_NO_RETRY', mode=c['mode'], snapshot_qualified=False,
                  scientific_accuracy_accepted=False, resources_before=resources.check())
    with (work / 'run_claim.json').open('x') as stream:
        json.dump(dict(pid=os.getpid(), started_unix=time.time(), manifest_sha256=args.sha256), stream)
    handlers = {s:signal.signal(s, signal.default_int_handler)
                for s in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    runner = SerialExecutor(work, c['wall_seconds'], 'A', resources)
    runner.env['GFORTRAN_UNBUFFERED_ALL'] = '1'
    start = time.monotonic()
    try:
        with (work / 'A/snapshot.x2m').open('rb') as source, (work / 'A/solve.log').open('xb') as log:
            runner._process([str(work / 'runtime/Dragon')], work / 'A', source, log, c['wall_seconds'])
        text = (work / 'A/solve.log').read_text(errors='replace')
        marker = 'AXMAT-R64-FIRST-CALL-PROBE-COMPLETE' if c['mode'] == 'first_call_probe' else 'AXMAT-SNAPSHOT-A-COMPLETE'
        if text.count(marker) != 1:
            raise RuntimeError('completion marker missing or repeated')
        if c['mode'] == 'first_call_probe':
            if sum(x.startswith('AXMAT-R64 GROUP=') for x in text.splitlines()) != 370:
                raise RuntimeError('incomplete group observations')
            if sum(x.startswith('AXMAT-R64-VECTOR ') for x in text.splitlines()) != 5180:
                raise RuntimeError('incomplete vector observations')
            if (work / 'A/snapshot_A.xsm').exists():
                raise RuntimeError('probe must never publish a snapshot')
            result['classification'] = 'R64_FIRST_CALL_OBSERVATIONS_COMPLETE'
        else:
            from production_runner import check_dragon_log
            check_dragon_log(text, marker)
            if not (work / 'A/snapshot_A.xsm').is_file():
                raise RuntimeError('snapshot missing')
            result['classification'] = 'R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT'
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic()-start
        try:
            verify()
            result['frozen_inputs_unchanged'] = True
        except BaseException as error:
            result.update(classification='INPUT_IDENTITY_FAILURE', identity_error=repr(error))
        result['outputs'] = {p.name:sha256(p) for p in (work / 'A').iterdir()
                             if p.is_file() and p.name not in ('snapshot.x2m', 'material.xsm', 'geometry.dat')}
        result['resources_after'] = resources.check()
        dump_json(work / 'run_status.json', result)
        for s, handler in handlers.items():
            signal.signal(s, handler)
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('resources')}))


if __name__ == '__main__':
    main()

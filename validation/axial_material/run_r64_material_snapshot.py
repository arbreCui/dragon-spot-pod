"""Run one declared A/B REAL64 snapshot with immutable inputs and bounded execution."""
import argparse
import json
import os
from pathlib import Path
import signal
import time

from production_runner import DiskResources, SerialExecutor, check_dragon_log, dump_json, require_file, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('execution', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    manifest_path = args.execution.resolve()
    work = manifest_path.parent
    c = json.loads(require_file(manifest_path, args.sha256).read_text())
    if c['schema'] != 'AXMAT_R64_MATERIAL_SNAPSHOT_V1' or c['state'] not in ('A', 'B'):
        raise ValueError('undeclared snapshot scope')
    if c['wall_seconds'] != 600 or c['automatic_retries'] != 0 or c['threads'] != 1:
        raise ValueError('undeclared snapshot budget')
    state = c['state']
    directory = work / state
    def verify():
        require_file(manifest_path, args.sha256)
        for name, wanted in c['files'].items():
            require_file(Path(name), wanted)
    verify()
    resources = DiskResources(Path(c['artifact_root']), c['resource_roots'], 8*2**30, 12*2**30)
    result = dict(classification='FAILED_NO_RETRY', state=state,
        snapshot_qualified=False, production_qualified=False, scientific_accuracy_accepted=False,
        resources_before=resources.check())
    with (work / 'run_claim.json').open('x') as stream:
        json.dump(dict(pid=os.getpid(), started_unix=time.time(), execution_sha256=args.sha256), stream)
    handlers = {s: signal.signal(s, signal.default_int_handler) for s in
                (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    runner = SerialExecutor(work, 600, state, resources)
    runner.env['GFORTRAN_UNBUFFERED_ALL'] = '1'
    start = time.monotonic()
    try:
        with (directory / 'snapshot.x2m').open('rb') as source, (directory / 'solve.log').open('xb') as log:
            runner._process([str(work / 'runtime/Dragon')], directory, source, log, 600)
        text = (directory / 'solve.log').read_text(errors='replace')
        check_dragon_log(text, f'AXMAT-SNAPSHOT-{state}-COMPLETE')
        if not (directory / f'snapshot_{state}.xsm').is_file():
            raise ValueError('completed snapshot missing')
        result['classification'] = 'R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT'
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic() - start
        try:
            verify()
            result['frozen_inputs_unchanged'] = True
        except BaseException as error:
            result.update(classification='INPUT_IDENTITY_FAILURE', identity_error=repr(error))
        result['outputs'] = {p.name: sha256(p) for p in directory.iterdir() if p.is_file()
            and p.name not in ('snapshot.x2m', 'material.xsm', 'geometry.dat')}
        result['resources_after'] = resources.check()
        dump_json(work / 'run_status.json', result)
        for s, handler in handlers.items():
            signal.signal(s, handler)
    print(json.dumps({k: v for k, v in result.items() if not k.startswith('resources')}, indent=2))


if __name__ == '__main__':
    main()

"""Prepare or explicitly authorize the one-shot 24-nuclide reference batch.

Preparation and saved-output review never start native engines. Run mode needs
a separate approval receipt, a frozen runtime manifest and fresh directories.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess as sp
import sys
import time
import traceback

import remaining_temperature_batch as batch

API = batch.API
sha,verify,dump,require,bounded = (API[k] for k in ('sha','verify','dump','require','bounded'))


def manifest(folder):
    with (folder/'result.sha256').open('x') as stream:
        for path in sorted(folder.rglob('*')):
            if path.is_file() and not path.is_symlink() and path.name != 'result.sha256':
                stream.write(f'{sha(path)}  {path.relative_to(folder)}\n')


def pins_from_manifest(folder):
    mf = folder/'result.sha256'
    pins = {str(mf):sha(mf)}
    for line in mf.read_text().splitlines():
        digest,name = line.split(maxsplit=1)
        path = folder/name
        require(path.resolve().is_relative_to(folder.resolve()), 'manifest escapes directory')
        require(str(path) not in pins, 'duplicate manifest path')
        pins[str(path)] = digest
    return pins


def prepare(folder):
    require(not folder.exists(), 'runtime directory already exists')
    rows = batch.cases()
    graph = batch.validate_graph(rows,Path('/private/tmp/NOT_AN_ACTIVE_D4A_RUN'))
    pins = json.loads((batch.PREP/'inputs.json').read_text())
    pins[str(batch.PREP/'prepared.sha256')] = batch.PREP_SHA
    for line in (batch.PREP/'prepared.sha256').read_text().splitlines():
        digest,name = line.split(maxsplit=1)
        pins[str(batch.PREP/name)] = digest
    paths = [Path(__file__),Path(batch.__file__),Path(batch.mt51.__file__),batch.API_PATH,batch.COMPARE_PATH,
             batch.ART/'d4a-fe56-actual-temperature-run-20260929/compare.py',
             batch.ROOT/'validation/d4_reference/audit_fe56_temperature_interpolation.py',
             batch.ROOT/'validation/d4_reference/audit_fe56_candidate_scope.py',
             batch.ROOT/'validation/d4_reference/test_remaining_temperature_batch.py']
    paths += [Path(API[name].__file__) for name in ('bounded','nr','adapter','sr')]
    pins.update({str(p):sha(p) for p in paths})
    pins[str(batch.EXE)] = 'ae19f454f38bd629ed44610bd545ccd889e5d5af013961e193a8f2886819619d'
    pins[str(batch.PAIR/'candidate/build/source/libnjoy.dylib')] = '273289f99805076af17ecdb5bfbd304f36326119f3241c1a34722451c9b5cc24'
    verify(pins)
    folder.mkdir(parents=True)
    dump(folder/'inputs.json',pins)
    started = time.monotonic()
    with (folder/'self_test.log').open('xb') as log:
        tested = sp.run([sys.executable,'-B',str(batch.ROOT/'validation/d4_reference/test_remaining_temperature_batch.py'),'-v'],
                        stdout=log,stderr=sp.STDOUT,timeout=60)
    dump(folder/'self_test.json',dict(returncode=tested.returncode,elapsed_s=time.monotonic()-started,
                                    native_engines_started=0))
    require(tested.returncode == 0, 'short preparation tests failed')
    verify(pins)
    dump(folder/'plan.json',dict(status='PREPARED_NOT_AUTHORIZED_NOT_RUN',native_engines_started=0,
         total_seconds=batch.BUDGET,review_reserve_seconds=batch.RESERVE,native_stages=len(graph),
         stage_labels=[s['label'] for s in graph],nuclides=[r['nuclide'] for r in rows],
         forbid=['retry','TONE','transport','Picard','CE','production replacement'],
         limits=['No approval is created by preparation.',
                 'Missing original low GENDF is explicitly reported; no claimed comparison to it.',
                 'Eight hours is a hard ceiling, not a runtime guarantee.']))
    manifest(folder)
    print('PREPARED_NOT_AUTHORIZED',sha(folder/'result.sha256'),flush=True)


def read_runtime(runtime):
    pins = pins_from_manifest(runtime)
    pins.update(json.loads((runtime/'inputs.json').read_text()))
    verify(pins)
    plan = json.loads((runtime/'plan.json').read_text())
    require(plan['status'] == 'PREPARED_NOT_AUTHORIZED_NOT_RUN' and plan['native_stages'] == 138,
            'wrong runtime plan')
    return pins


def approval(receipt,runtime):
    auth = json.loads(receipt.read_text())
    require(auth.get('status') == 'EXPLICIT_USER_APPROVAL', 'explicit approval is missing')
    require(auth.get('runtime_manifest_sha256') == sha(runtime/'result.sha256'), 'approval/runtime mismatch')
    require(auth.get('total_seconds') == batch.BUDGET and auth.get('review_reserve_seconds') == batch.RESERVE,
            'approval budget differs')
    require(auth.get('attempts') == 1 and auth.get('retry') is False and auth.get('native_stages') == 138,
            'approval scope differs')
    require(auth.get('scope') == '24_NUCLIDES_55_ACTUAL_TEMPERATURES_REFERENCE_ONLY', 'wrong approval scope')
    require(isinstance(auth.get('user_approval_text'),str) and auth['user_approval_text'].strip(),
            'missing human approval record')
    return auth


def native_terminal(text):
    require('njoy' in text.lower() and 'error in' not in text.lower(), 'native error marker')
    require(re.search(r'\n\s*\d+(?:\.\d+)?s\s*\n\s*\*{10,}\s*\Z',text), 'missing NJOY terminal')


def worker(runtime,work,control,deadline):
    pins = read_runtime(runtime)
    authorization = control/'authorization.json'
    approval(authorization,runtime)
    pins[str(authorization)] = sha(authorization)
    dump(work/'inputs.json',pins)
    rows = batch.cases()
    batch.validate_graph(rows,work)
    staged,produced = {},{}
    count = 0
    def stage(item):
        nonlocal count
        folder = item['output'].parent
        folder.mkdir(parents=True)
        local_inputs = {}
        for target,source in dict(item['inputs'],**{'input.in':item['deck']}).items():
            expected = produced.get(str(source),pins.get(str(source)))
            require(expected is not None and sha(source) == expected, 'input lineage changed: '+str(source))
            dest = folder/target
            shutil.copyfile(source,dest)
            require(sha(dest) == expected, 'staging copy changed')
            local_inputs[str(dest)] = expected
        staged.update(local_inputs)
        dump(folder/'input_hashes.json',local_inputs)
        verify({str(batch.EXE):pins[str(batch.EXE)],
                str(batch.PAIR/'candidate/build/source/libnjoy.dylib'):pins[str(batch.PAIR/'candidate/build/source/libnjoy.dylib')]})
        remaining = deadline-time.monotonic()
        require(remaining > 0, 'native/first-check budget exhausted')
        print('START',item['label'],dt.datetime.now(dt.timezone.utc).isoformat(),flush=True)
        started = time.monotonic()
        bounded.run(batch.EXE,folder/'input.in',folder/'native.log',remaining)
        native_terminal((folder/'native.log').read_text())
        require(item['output'].is_file() and item['output'].stat().st_size > 0, 'missing native output')
        verify(local_inputs)
        digest = sha(item['output'])
        produced[str(item['output'])] = digest
        dump(folder/'receipt.json',dict(returncode=0,elapsed_s=time.monotonic()-started,output_sha256=digest))
        count += 1
        print('END',item['label'],flush=True)
    try:
        for row in rows:
            graph = batch.stages(row,work)
            for item in (s for s in graph if s['control']):
                stage(item)
            if row['nsigz'] > 1:
                dump(work/row['nuclide']/'control_check.json',batch.control_check(row,work))
            require(time.monotonic() < deadline, 'control check budget exhausted')
            for item in (s for s in graph if not s['control']):
                stage(item)
            dump(work/row['nuclide']/'comparison.json',batch.expanded_check(row,work))
            verify(pins)
            require(time.monotonic() < deadline, 'first-check budget exhausted')
            print('CASE_PASS',row['nuclide'],flush=True)
        require(count == 138, 'incomplete native batch')
        verify(staged); verify(produced); verify(pins)
        dump(work/'completed.json',dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',native_stages=count,
             finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),production_replaced=False))
    finally:
        dump(work/'staged_inputs.json',staged)
        dump(work/'output_hashes.json',produced)
        manifest(work)


def review(runtime,work,destination,deadline):
    require(not destination.exists(), 'review directory already exists')
    require(time.monotonic() < deadline, 'review deadline expired')
    pins = read_runtime(runtime)
    pins.update(pins_from_manifest(work))
    for name in ('inputs.json','staged_inputs.json','output_hashes.json'):
        pins.update(json.loads((work/name).read_text()))
    verify(pins)
    complete = json.loads((work/'completed.json').read_text())
    require(complete['status'] == 'COMPLETE_PENDING_INDEPENDENT_REVIEW' and complete['native_stages'] == 138,
            'native worker incomplete')
    results = []
    for row in batch.cases():
        name = row['nuclide']
        if row['nsigz'] > 1:
            result = batch.control_check(row,work)
            require(result == json.loads((work/name/'control_check.json').read_text()), 'control replay differs')
        result = batch.expanded_check(row,work)
        require(result == json.loads((work/name/'comparison.json').read_text()), 'expanded replay differs')
        for item in batch.stages(row,work):
            folder = item['output'].parent
            receipt = json.loads((folder/'receipt.json').read_text())
            require(receipt['returncode'] == 0 and receipt['output_sha256'] == sha(item['output']), 'stage receipt differs')
            native_terminal((folder/'native.log').read_text())
        results.append(dict(nuclide=name,status=result['status'],controls_exact_records=result['controls_exact_records']))
        require(time.monotonic() < deadline, 'independent review exceeded total budget')
    verify(pins)
    require(time.monotonic() < deadline, 'final identities exceeded total budget')
    destination.mkdir(parents=True)
    dump(destination/'inputs.json',pins)
    dump(destination/'review.json',dict(status='PASS_24_NUCLIDE_REFERENCE_ONLY',cases=results,
         finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),native_engines_started=0,
         production_accepted=False,original_result_manifest_sha256=sha(work/'result.sha256')))
    manifest(destination)


def supervised(command,log,deadline):
    """Reuse the existing process-group watchdog; no new scheduler or retries."""
    env = {k:v for k,v in os.environ.items() if not k.startswith('DYLD_')}
    env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    child = watchdog = None
    write_fd = None
    with log.open('xb') as stream:
        try:
            child = sp.Popen(command,stdout=stream,stderr=sp.STDOUT,start_new_session=True,env=env)
            read_fd,write_fd = os.pipe()
            watchdog = bounded.start_liveness_watchdog(read_fd,child.pid,5)
            os.close(read_fd)
            timeout = deadline-time.monotonic()
            require(timeout > 0, 'supervised deadline expired')
            return child.wait(timeout=timeout)
        except BaseException:
            if child is not None:
                bounded.terminate_group(child)
            raise
        finally:
            if watchdog is not None:
                bounded.finish_liveness_watchdog(write_fd,watchdog)


def controller(runtime,work,receipt):
    auth = approval(receipt,runtime)
    read_runtime(runtime)
    control = work.with_name(work.name+'-control')
    output = work.with_name(work.name+'-review')
    require(all(not p.exists() for p in (work,control,output)), 'fresh one-shot directories required')
    start,utc = time.monotonic(),dt.datetime.now(dt.timezone.utc)
    control.mkdir(parents=True); work.mkdir()
    dump(control/'authorization.json',auth)
    state = dict(status='RUNNING',supervisor_pid=os.getpid(),started_utc=utc.isoformat(),
                 deadline_utc=(utc+dt.timedelta(seconds=batch.BUDGET)).isoformat(),
                 total_seconds=batch.BUDGET,review_reserve_seconds=batch.RESERVE,retries=0)
    dump(control/'run_status.json',state)
    for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):
        signal.signal(sig,signal.default_int_handler)
    command = [sys.executable,'-B',str(Path(__file__).resolve())]
    try:
        native_deadline = start+batch.BUDGET-batch.RESERVE
        rc = supervised(command+['--worker',str(runtime),str(work),str(control),str(native_deadline)],
                        control/'controller.log',native_deadline)
        require(rc == 0, 'worker refused/failed; no retry')
        state['status'] = 'PENDING_INDEPENDENT_REVIEW'
        (control/'run_status.json').write_text(json.dumps(state,indent=2)+'\n')
        rc = supervised(command+['--review',str(runtime),str(work),str(output),str(start+batch.BUDGET)],
                        control/'review.log',start+batch.BUDGET)
        require(rc == 0, 'independent review refused/failed; no retry')
        state['status'] = 'PASS_24_NUCLIDE_REFERENCE_ONLY'
    except sp.TimeoutExpired:
        state['status'] = 'TIMEOUT_NO_RETRY'
        traceback.print_exc()
    except BaseException:
        state['status'] = 'FAILED_NO_RETRY'
        traceback.print_exc()
    finally:
        state.update(finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                     elapsed_s_including_cleanup=time.monotonic()-start)
        (control/'run_status.json').write_text(json.dumps(state,indent=2)+'\n')
        manifest(control)
    print(json.dumps(state),flush=True)
    if state['status'] != 'PASS_24_NUCLIDE_REFERENCE_ONLY':
        raise SystemExit(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--prepare',type=Path)
    modes.add_argument('--run',nargs=3,type=Path,metavar=('RUNTIME','FRESH_WORK','APPROVAL_JSON'))
    modes.add_argument('--worker',nargs=4)
    modes.add_argument('--review',nargs=4)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.prepare.resolve())
    elif args.run:
        controller(*(p.resolve() for p in args.run))
    elif args.worker:
        worker(*(Path(p).resolve() for p in args.worker[:3]),float(args.worker[3]))
    else:
        review(*(Path(p).resolve() for p in args.review[:3]),float(args.review[3]))

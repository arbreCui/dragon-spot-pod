"""One separately approved final-four batch; reuse five Pu241 stages, no retries."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

import prepare_final_four_fuel_temperatures as prep

c, b = prep.c, prep.b
require, sha, verify, dump = prep.require, prep.sha, prep.verify, prep.dump
SEAL = 'ced38db2a36f66d42887c2a507c1cce4d02c85e19a0b5c2964f437fc4704de32'
WORK = prep.WORK
CONTROL = WORK.with_name(WORK.name+'-control')
REVIEW = WORK.with_name(WORK.name+'-review')
TOTAL, RESERVE = 21600, 600
SCOPE = 'FOUR_FUELS_12_ACTUAL_TEMPERATURE_PAIRS_REFERENCE_ONLY'


def load():
    require(sha(prep.DEST/'result.sha256') == SEAL, 'prepared seal changed')
    pins = c.pins_from_manifest(prep.DEST)
    prep.merge(pins,json.loads((prep.DEST/'inputs.json').read_text()))
    prep.merge(pins,{str(Path(__file__).resolve()):sha(Path(__file__))})
    verify(pins)
    plan = json.loads((prep.DEST/'plan.json').read_text())
    require(plan['status'] == 'PREPARED_NOT_AUTHORIZED_NO_NATIVE_EXECUTION' and
            plan['scope'] == SCOPE and plan['future_work'] == str(WORK), 'wrong prepared scope')
    require(plan['proposed_total_seconds'] == TOTAL and plan['proposed_review_reserve_seconds'] == RESERVE
            and plan['native_stages'] == 39 and plan['cached_stages'] == 5, 'budget/stage drift')
    require(plan['cases'] == prep.rows(), 'case declarations changed')
    require(plan['checker_module'] == str(Path(b.mt51.__file__).resolve()), 'checker identity changed')
    retained = json.loads((prep.DEST/'retained_review.json').read_text())
    require(retained['status'] == 'PASS_FOUR_SAVED_FUEL_REFERENCES_ONLY' and
            [r['nuclide'] for r in retained['cases']] == prep.RETAIN, 'retained four not reviewed')
    prep.validate_graph(WORK,plan['stages'],plan['reused_stages'],pins)
    return plan,pins


def authorization(path):
    auth = json.loads(path.read_text())
    require(auth.get('status') == 'EXPLICIT_USER_APPROVAL' and
            isinstance(auth.get('user_approval_text'),str) and auth['user_approval_text'].strip(),
            'explicit approval missing')
    require(auth.get('prepared_manifest_sha256') == SEAL and
            auth.get('driver_sha256') == sha(Path(__file__)), 'approval identity mismatch')
    require(auth.get('scope') == SCOPE and auth.get('native_stages') == 39 and
            auth.get('cached_stages') == 5 and auth.get('total_seconds') == TOTAL and
            auth.get('review_reserve_seconds') == RESERVE and auth.get('attempts') == 1 and
            auth.get('retry') is False, 'approval scope mismatch')
    return auth


def worker(deadline):
    plan,pins = load()
    authorization(CONTROL/'authorization.json')
    prep.merge(pins,{str(CONTROL/'authorization.json'):sha(CONTROL/'authorization.json')})
    dump(WORK/'inputs.json',pins)
    staged,produced,cached = {},{},{}
    count = 0

    def stage(item):
        nonlocal count
        output = Path(item['output'])
        folder = output.parent
        folder.mkdir(parents=True)
        local = {}
        for name,source in dict(item['inputs'],**{'input.in':item['deck']}).items():
            expected = produced.get(source,pins.get(source))
            require(expected is not None and sha(source) == expected, 'input lineage changed')
            target = folder/name
            shutil.copyfile(source,target)
            require(sha(target) == expected, 'staged copy differs')
            local[str(target)] = expected
        staged.update(local)
        dump(folder/'input_hashes.json',local)
        verify({path:pins[path] for path in (plan['candidate_executable'],plan['candidate_dylib'])})
        remaining = deadline-time.monotonic()
        require(remaining > 0, 'native budget expired')
        print('START',item['label'],dt.datetime.now(dt.timezone.utc).isoformat(),flush=True)
        started = time.monotonic()
        c.bounded.run(Path(plan['candidate_executable']),folder/'input.in',folder/'native.log',remaining)
        c.native_terminal((folder/'native.log').read_text())
        verify(local)
        require(output.is_file() and output.stat().st_size > 0, 'native output missing')
        produced[str(output)] = sha(output)
        dump(folder/'receipt.json',dict(returncode=0,elapsed_s=time.monotonic()-started,
                                      output_sha256=produced[str(output)]))
        count += 1
        print('END',item['label'],flush=True)

    try:
        for item in plan['reused_stages']:
            folder = Path(item['output']).parent
            folder.mkdir(parents=True)
            for name in item['copy_files']:
                source,target = Path(item['source_directory'])/name,folder/name
                require(sha(source) == pins[str(source)], 'cached source changed')
                shutil.copyfile(source,target)
                require(sha(target) == pins[str(source)], 'cached copy differs')
                cached[str(target)] = pins[str(source)]
            produced[item['output']] = cached[item['output']]
        dump(WORK/'cached_lineage.json',plan['reused_stages'])
        for row in plan['cases']:
            name = row['nuclide']
            group = [s for s in plan['stages'] if s['label'].split('/')[0] == name]
            for item in (s for s in group if s['control']):
                stage(item)
            control = b.control_check(row,WORK)
            if name == 'Pu241':
                accepted = json.loads((prep.FIX/'Pu241_control_check.json').read_text())
                require(control == accepted, 'reused Pu241 control differs')
            dump(WORK/name/'control_check.json',control)
            require(time.monotonic() < deadline, 'control check deadline expired')
            for item in (s for s in group if not s['control']):
                stage(item)
            dump(WORK/name/'comparison.json',b.expanded_check(row,WORK))
            verify(pins)
            require(time.monotonic() < deadline, 'first-check deadline expired')
            print('CASE_PASS',name,flush=True)
        require(count == 39 and len(produced) == 44, 'incomplete fuel batch')
        verify(staged); verify(cached); verify(produced); verify(pins)
        dump(WORK/'completed.json',dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',
            native_stages=39,cached_stages=5,production_replaced=False))
    finally:
        dump(WORK/'staged_inputs.json',staged)
        dump(WORK/'cached_inputs.json',cached)
        dump(WORK/'output_hashes.json',produced)
        c.manifest(WORK)


def review(deadline):
    plan,pins = load()
    authorization(CONTROL/'authorization.json')
    prep.merge(pins,c.pins_from_manifest(WORK))
    for name in ('inputs.json','staged_inputs.json','cached_inputs.json','output_hashes.json'):
        prep.merge(pins,json.loads((WORK/name).read_text()))
    verify(pins)
    require(json.loads((WORK/'completed.json').read_text()) ==
            dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',native_stages=39,cached_stages=5,
                 production_replaced=False), 'worker incomplete')
    require(json.loads((WORK/'cached_lineage.json').read_text()) == plan['reused_stages'], 'cached lineage differs')
    results = []
    for row in plan['cases']:
        name = row['nuclide']
        control = b.control_check(row,WORK)
        require(control == json.loads((WORK/name/'control_check.json').read_text()), 'control replay differs')
        result = b.expanded_check(row,WORK)
        require(result == json.loads((WORK/name/'comparison.json').read_text()), 'expanded replay differs')
        for item in (s for s in plan['stages']+plan['reused_stages'] if s['label'].split('/')[0] == name):
            folder = Path(item['output']).parent
            receipt = json.loads((folder/'receipt.json').read_text())
            require(receipt['returncode'] == 0 and receipt['output_sha256'] == sha(Path(item['output'])),
                    'stage receipt differs')
            c.native_terminal((folder/'native.log').read_text())
        results.append(dict(nuclide=name,status=result['status'],controls_exact_records=result['controls_exact_records']))
        require(time.monotonic() < deadline, 'independent review deadline expired')
    verify(pins)
    require(time.monotonic() < deadline, 'final identity deadline expired')
    REVIEW.mkdir()
    dump(REVIEW/'inputs.json',pins)
    dump(REVIEW/'review.json',dict(status='PASS_FINAL_FOUR_FUEL_REFERENCES_ONLY',cases=results,
        retained_sixteen_identities_unchanged=True,retained_four_fuel_identities_unchanged=True,
        native_engines_started=0,production_accepted=False,
        finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        original_result_manifest_sha256=sha(WORK/'result.sha256')))
    c.manifest(REVIEW)


def controller(path):
    auth = authorization(path)
    load()
    require(all(not p.exists() for p in (WORK,CONTROL,REVIEW)), 'fresh one-shot directories required')
    start,utc = time.monotonic(),dt.datetime.now(dt.timezone.utc)
    CONTROL.mkdir(); WORK.mkdir()
    dump(CONTROL/'authorization.json',auth)
    state = dict(status='RUNNING',supervisor_pid=os.getpid(),started_utc=utc.isoformat(),
        deadline_utc=(utc+dt.timedelta(seconds=TOTAL)).isoformat(),total_seconds=TOTAL,
        review_reserve_seconds=RESERVE,retries=0)
    dump(CONTROL/'run_status.json',state)
    for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):
        signal.signal(sig,signal.default_int_handler)
    command = [sys.executable,'-B',str(Path(__file__).resolve())]
    try:
        rc = c.supervised(command+['--worker',str(start+TOTAL-RESERVE)],
                          CONTROL/'controller.log',start+TOTAL-RESERVE)
        require(rc == 0, 'worker refused/failed; no retry')
        state['status'] = 'PENDING_INDEPENDENT_REVIEW'
        (CONTROL/'run_status.json').write_text(json.dumps(state,indent=2)+'\n')
        deadline = min(start+TOTAL,time.monotonic()+RESERVE)
        rc = c.supervised(command+['--review',str(deadline)],CONTROL/'review.log',deadline)
        require(rc == 0, 'independent review refused/failed; no retry')
        state['status'] = 'PASS_FINAL_FOUR_FUEL_REFERENCES_ONLY'
    except subprocess.TimeoutExpired:
        state['status'] = 'TIMEOUT_NO_RETRY'
        traceback.print_exc()
    except BaseException:
        state['status'] = 'FAILED_NO_RETRY'
        traceback.print_exc()
    finally:
        state.update(finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                     elapsed_s_including_cleanup=time.monotonic()-start)
        (CONTROL/'run_status.json').write_text(json.dumps(state,indent=2)+'\n')
        c.manifest(CONTROL)
    print(json.dumps(state),flush=True)
    if state['status'] != 'PASS_FINAL_FOUR_FUEL_REFERENCES_ONLY':
        raise SystemExit(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--run',type=Path)
    mode.add_argument('--worker',type=float)
    mode.add_argument('--review',type=float)
    args = parser.parse_args()
    if args.check:
        plan,pins = load()
        require(all(not p.exists() for p in (WORK,CONTROL,REVIEW)), 'future work not fresh')
        print('PREFLIGHT_PASS',len(pins),'identities; 39 native + 5 cached; no engine started')
    elif args.run:
        controller(args.run)
    elif args.worker is not None:
        worker(args.worker)
    else:
        review(args.review)

"""One authorized four-stage Am241 control, reusing existing bounded runners."""
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

import run_remaining_temperature_batch as common

b = common.batch
PREP = b.ART/'d4a-mt51-mf6-control-prepared-20261001'
PREP_SHA = '04542c7ffed3810825d0336d04d8748cc7c434474ae430ac4313c87f273eada5'
PRIOR = b.ART/'d4a-remaining-temperature-run-20261001'
WORK = b.ART/'d4a-mt51-mf6-control-run-20261001'
CONTROL = WORK.with_name(WORK.name+'-control')
REVIEW = WORK.with_name(WORK.name+'-review')
SCOPE = 'AM241_FIVE_TEMPERATURE_LOW_HIGH_MT51_MFD8_CONTROL_ONLY'
TOTAL, RESERVE = 600, 120
require, sha, verify, dump = common.require, common.sha, common.verify, common.dump


def load():
    require(sha(PREP/'result.sha256') == PREP_SHA, 'prepared seal changed')
    pins = common.read_runtime(b.ART/'d4a-remaining-temperature-runtime-prepared-20261001')
    for extra in (common.pins_from_manifest(PREP),json.loads((PREP/'inputs.json').read_text())):
        for path,digest in extra.items():
            require(path not in pins or pins[path] == digest, 'conflicting input pin')
            pins[path] = digest
    pins[str(Path(__file__).resolve())] = sha(Path(__file__))
    verify(pins)
    plan = json.loads((PREP/'plan.json').read_text())
    require(plan['scope'] == SCOPE and plan['future_work'] == str(WORK), 'wrong scope/work')
    require(plan['proposal']['total_seconds'] == TOTAL and
            plan['proposal']['review_reserve_seconds'] == RESERVE, 'wrong budget')
    row = next(r for r in b.cases() if r['nuclide'] == 'Am241')
    expected = []
    missing = WORK/'Am241/control/low/pendf/tape30'
    saved = PRIOR/'Am241/control/low/pendf/tape30'
    for s in b.stages(row,WORK):
        if not s['control'] or s['kind'] == 'pendf':
            continue
        inputs = {k:str(saved if v == missing else v) for k,v in s['inputs'].items()}
        inputs['input.in'] = str(s['deck'])
        expected.append(dict(label=s['label'],inputs=inputs,output=str(s['output'])))
    require(plan['stages'] == expected and len(expected) == 4, 'four-stage graph drift')
    return plan,pins,row


def authorization(path):
    auth = json.loads(path.read_text())
    require(auth.get('status') == 'EXPLICIT_USER_APPROVAL' and
            auth.get('user_approval_text') == '批准', 'explicit approval missing')
    require(auth.get('prepared_manifest_sha256') == PREP_SHA and
            auth.get('driver_sha256') == sha(Path(__file__)), 'approval identity mismatch')
    require(auth.get('scope') == SCOPE and auth.get('native_stages') == 4 and
            auth.get('total_seconds') == TOTAL and auth.get('review_reserve_seconds') == RESERVE and
            auth.get('attempts') == 1 and auth.get('retry') is False, 'approval scope mismatch')
    return auth


def check(row):
    result = b.control_check(row,WORK)
    old_low = (PRIOR/'Am241/control/low/groupr/tape30').read_bytes()
    new_low = (WORK/'Am241/control/low/groupr/tape30').read_bytes()
    result['regenerated_low_GENDF_scope'] = b.mt51.gendf_scope(old_low,new_low,row['mat'])
    result['limits'] = ['Original historical low GENDF was not retained; low comparison uses the sealed regenerated control.',
                        'Five-temperature Am241 control only: no actual-temperature expansion or full-batch acceptance.',
                        'No material, transport, Picard, CE or production replacement.']
    return result


def worker(deadline):
    plan,pins,row = load()
    authorization(CONTROL/'authorization.json')
    pins[str(CONTROL/'authorization.json')] = sha(CONTROL/'authorization.json')
    dump(WORK/'inputs.json',pins)
    staged,outputs = {},{}
    try:
        for item in plan['stages']:
            output = Path(item['output'])
            folder = output.parent
            folder.mkdir(parents=True)
            local = {}
            for name,source in item['inputs'].items():
                source = Path(source)
                expected = outputs.get(str(source),pins.get(str(source)))
                require(expected is not None and sha(source) == expected, 'input lineage changed')
                target = folder/name
                shutil.copyfile(source,target)
                require(sha(target) == expected, 'staged copy changed')
                local[str(target)] = expected
            staged.update(local)
            dump(folder/'input_hashes.json',local)
            verify({name:pins[name] for name in (plan['candidate_executable'],plan['candidate_dylib'])})
            remaining = deadline-time.monotonic()
            require(remaining > 0, 'native deadline expired')
            print('START',item['label'],dt.datetime.now(dt.timezone.utc).isoformat(),flush=True)
            started = time.monotonic()
            common.bounded.run(Path(plan['candidate_executable']),folder/'input.in',folder/'native.log',remaining)
            common.native_terminal((folder/'native.log').read_text())
            verify(local)
            require(output.is_file() and output.stat().st_size > 0, 'missing output')
            outputs[str(output)] = sha(output)
            dump(folder/'receipt.json',dict(returncode=0,elapsed_s=time.monotonic()-started,
                                            output_sha256=outputs[str(output)]))
            print('END',item['label'],flush=True)
        require(len(outputs) == 4, 'incomplete stages')
        dump(WORK/'control_check.json',check(row))
        verify(pins); verify(staged); verify(outputs)
        require(time.monotonic() < deadline, 'first-check deadline exceeded')
        dump(WORK/'completed.json',dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',native_stages=4))
    finally:
        dump(WORK/'staged_inputs.json',staged)
        dump(WORK/'output_hashes.json',outputs)
        common.manifest(WORK)


def review(deadline):
    plan,pins,row = load()
    authorization(CONTROL/'authorization.json')
    pins.update(common.pins_from_manifest(WORK))
    for name in ('inputs.json','staged_inputs.json','output_hashes.json'):
        pins.update(json.loads((WORK/name).read_text()))
    verify(pins)
    require(json.loads((WORK/'completed.json').read_text()) ==
            dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',native_stages=4), 'worker incomplete')
    for item in plan['stages']:
        folder = Path(item['output']).parent
        receipt = json.loads((folder/'receipt.json').read_text())
        require(receipt['returncode'] == 0 and receipt['output_sha256'] == sha(Path(item['output'])),
                'native receipt mismatch')
        common.native_terminal((folder/'native.log').read_text())
    result = check(row)
    require(result == json.loads((WORK/'control_check.json').read_text()), 'independent replay differs')
    verify(pins)
    require(time.monotonic() < deadline, 'review deadline expired')
    REVIEW.mkdir()
    dump(REVIEW/'inputs.json',pins)
    dump(REVIEW/'review.json',dict(status='PASS_AM241_CONTROL_ONLY',native_engines_started=0,
        finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),result=result,
        production_accepted=False,original_result_manifest_sha256=sha(WORK/'result.sha256')))
    common.manifest(REVIEW)


def controller(receipt):
    auth = authorization(receipt)
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
    cmd = [sys.executable,'-B',str(Path(__file__).resolve())]
    try:
        rc = common.supervised(cmd+['--worker',str(start+TOTAL-RESERVE)],
                               CONTROL/'controller.log',start+TOTAL-RESERVE)
        require(rc == 0, 'native/first-check failed; no retry')
        state['status'] = 'PENDING_INDEPENDENT_REVIEW'
        (CONTROL/'run_status.json').write_text(json.dumps(state,indent=2)+'\n')
        rc = common.supervised(cmd+['--review',str(start+TOTAL)],CONTROL/'review.log',start+TOTAL)
        require(rc == 0, 'independent review failed; no retry')
        state['status'] = 'PASS_AM241_CONTROL_ONLY'
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
        common.manifest(CONTROL)
    print(json.dumps(state),flush=True)
    if state['status'] != 'PASS_AM241_CONTROL_ONLY':
        raise SystemExit(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check',action='store_true')
    group.add_argument('--run',type=Path)
    group.add_argument('--worker',type=float)
    group.add_argument('--review',type=float)
    args = parser.parse_args()
    if args.check:
        plan,pins,_ = load()
        require(all(not p.exists() for p in (WORK,CONTROL,REVIEW)), 'not fresh')
        print('PREFLIGHT_PASS',len(pins),'identities; four stages; no native engine started')
    elif args.run:
        controller(args.run)
    elif args.worker is not None:
        worker(args.worker)
    else:
        review(args.review)

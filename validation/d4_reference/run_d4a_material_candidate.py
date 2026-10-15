"""Default-off three-material-state experiment; explicit new budget required."""
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

import run_d4a_material_candidate_library as lib
import check_d4a_material_candidate as check

c, p = lib.c, lib.p
sha, verify, require, dump, join = c.sha, c.verify, c.require, c.dump, lib.join
RUNTIME = p.ART/'d4a-actual-temperature-material-runtime-20261003'
WORK = p.ART/'d4a-actual-temperature-material-run-20261003'
CONTROL, REVIEW = Path(str(WORK)+'-control'), Path(str(WORK)+'-review')
TOTAL, RESERVE = 1800, 300
SCOPE = 'THREE_D4_ACTUAL_TEMPERATURE_MATERIAL_STATES_ONLY'
PASS = 'PASS_THREE_MATERIAL_DATA_CHECKS_ONLY'
BINARY = lib.WORK/'import/DLIB_370_bin'
BINARY_SHA = 'e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc'


def source_plan():
    plan, pins, _ = lib.load()
    seals = ((lib.WORK, '32143c799d9c6d80a7ae46476d006aa9a12607d67099d271ba53f6d8b366ce42'),
             (lib.CONTROL, 'e2c0527f50be91d945e6b7ae7d706a1dc6940009a5d9205e91aa58623388be04'),
             (lib.REVIEW, '3263d73fa4df8111bbfdf03bb6d85f974c29fffe400b687f95934238da96aa9e'))
    for folder, expected in seals:
        require(sha(folder/'result.sha256') == expected, 'library result seal changed')
        join(pins, {str(folder/'result.sha256'): expected})
        # The saved library review already covers the whole concatenation graph.
        # This experiment consumes the binary and preserved approval/result only.
        if folder != lib.WORK:
            join(pins, c.pins_from_manifest(folder))
    reviewed = json.loads((lib.REVIEW/'review.json').read_text())
    require(reviewed['status'] == lib.PASS and reviewed['result']['complete_subtrees'] == 28 and
            reviewed['original_result_manifest_sha256'] == seals[0][1], 'private library not reviewed')
    require(json.loads((lib.CONTROL/'run_status.json').read_text())['status'] == lib.PASS, 'library controller not passed')
    join(pins, {str(BINARY): BINARY_SHA})
    references = {r['nuclide']: r['path'] for r in plan['sources']}
    prior = p.ART/'d4a-saved-temperature-and-scalar-audit-20260930'
    require(sha(prior/'result.sha256') == 'bec1508302b7efebe1dffaefcf82718fbe989a4b403697d635fb378ab9df97da', 'Mo provenance changed')
    audit_pins = c.pins_from_manifest(prior)
    verify(audit_pins)
    join(pins, audit_pins)
    old = json.loads((prior/'inputs.json').read_text())
    for name in sorted(p.MO):
        path = Path(plan['assets']['full_library']['path']).parent/name/'draglibshem370_endfb8r1_v5p1'
        join(pins, {str(path): old[str(path)]})
        references[name] = str(path)
    require(len(references) == 35, 'reference membership')
    paths = [Path(__file__), Path(check.__file__),
             p.ROOT/'validation/d4_reference/test_d4a_material_candidate.py']
    paths += [p.ROOT/'src'/name for name in ('LIBDEN.f', 'LIBMIX.f', 'LIBDRA.f', 'LIBDRB.f', 'TONDRV.f')]
    join(pins, {str(path): sha(path) for path in paths})
    require((lib.PREP/'D4ActualTone.c2m').read_text() ==
            p.candidate_procedure((p.ROOT/'data/SpotD4Tone.c2m').read_text())[0], 'material physics changed')
    for temperature in check.TEMPERATURES:
        require((lib.PREP/f'material{temperature}.x2m').read_text() == p.material_deck(temperature), 'material deck changed')
    verify(pins)
    return plan, pins, references


def runtime_plan():
    return dict(status='PREPARED_NOT_AUTHORIZED', scope=SCOPE,
        temperatures_C=list(check.TEMPERATURES), total_seconds=TOTAL,
        review_reserve_seconds=RESERVE, native_stages=3, retries=0,
        candidate_binary_sha256=BINARY_SHA, free_space_required_bytes=8*1024**3,
        limits=['Three original-setting TONE material states only; no transport/Picard/CE.',
                'Separate new explicit authorization required. No production replacement.',
                '177 microscopic entries and 18 mixtures; original criteria and closure unchanged.',
                'All artifacts preserved on first failure; no retry or continuation.',
                '1800 seconds is a hard cap, not a runtime guarantee. Storage reserve is not a physics parameter.'])


def prepare():
    require(not RUNTIME.exists(), 'runtime already exists')
    _, pins, references = source_plan()
    RUNTIME.mkdir()
    for name in ['D4ActualTone.c2m']+[f'material{t}.x2m' for t in check.TEMPERATURES]:
        shutil.copyfile(lib.PREP/name, RUNTIME/name)
    dump(RUNTIME/'inputs.json', pins)
    dump(RUNTIME/'references.json', references)
    dump(RUNTIME/'plan.json', runtime_plan())
    verify(pins)
    c.manifest(RUNTIME)
    print('PREPARED_NOT_AUTHORIZED', sha(RUNTIME/'result.sha256'), flush=True)


def load():
    plan, pins, refs = source_plan()
    runtime_pins = c.pins_from_manifest(RUNTIME)
    verify(runtime_pins)
    require(json.loads((RUNTIME/'inputs.json').read_text()) == pins, 'runtime inputs changed')
    require(json.loads((RUNTIME/'references.json').read_text()) == refs, 'reference routes changed')
    require(json.loads((RUNTIME/'plan.json').read_text()) == runtime_plan(), 'runtime scope changed')
    for name in ['D4ActualTone.c2m']+[f'material{t}.x2m' for t in check.TEMPERATURES]:
        require(sha(RUNTIME/name) == pins[str(lib.PREP/name)], 'staged deck differs')
    join(pins, runtime_pins)
    return plan, pins, refs


def authorization(path):
    a = json.loads(path.read_text())
    expected = dict(status='EXPLICIT_USER_APPROVAL', user_approval_text='批准', scope=SCOPE,
        runtime_manifest_sha256=sha(RUNTIME/'result.sha256'), driver_sha256=sha(__file__),
        candidate_binary_sha256=BINARY_SHA, total_seconds=TOTAL, review_reserve_seconds=RESERVE,
        native_stages=3, temperatures_C=list(check.TEMPERATURES), attempts=1, retry=False)
    require(all(a.get(k) == v for k, v in expected.items()), 'missing or mismatched new approval')
    return a


def stage_inputs(plan, temperature):
    result = {'material.x2m': RUNTIME/f'material{temperature}.x2m',
              'D4ActualTone.c2m': RUNTIME/'D4ActualTone.c2m', 'DLIB_ACTUAL': BINARY,
              'DLIB8R1_370': Path(plan['assets']['full_library']['path'])}
    for name in ('rnr_cc.c2m', 'rnr_interpol.c2m', 'geometry.dat'):
        result[name] = Path(plan['assets'][name]['path'])
    return result


def check_all(plan, refs):
    return [check.analyze(WORK/f'material{t}', i, plan, refs)
            for i, t in enumerate(check.TEMPERATURES, 1)]


def worker(deadline):
    plan, pins, refs = load()
    authorization(CONTROL/'authorization.json')
    join(pins, {str(CONTROL/'authorization.json'): sha(CONTROL/'authorization.json')})
    dump(WORK/'inputs.json', pins)
    staged, outputs, receipts, results = {}, {}, [], []
    try:
        for plane, temperature in enumerate(check.TEMPERATURES, 1):
            folder = WORK/f'material{temperature}'
            folder.mkdir()
            stage_pins = {}
            for name, source in stage_inputs(plan, temperature).items():
                require(sha(source) == pins[str(source)], 'stage source changed')
                target = folder/name
                shutil.copyfile(source, target)
                stage_pins[str(target)] = pins[str(source)]
            verify(stage_pins)
            join(staged, stage_pins)
            dump(folder/'input_hashes.json', stage_pins)
            verify({plan['assets']['Dragon']['path']: plan['assets']['Dragon']['sha256']})
            remaining = deadline-time.monotonic()
            require(remaining > 0, 'material/first-check budget exhausted')
            print('START', temperature, dt.datetime.now(dt.timezone.utc).isoformat(), flush=True)
            start = time.monotonic()
            c.bounded.run(Path(plan['assets']['Dragon']['path']), folder/'material.x2m', folder/'material.log', remaining)
            terminal = check.terminal((folder/'material.log').read_text(), temperature)
            verify(stage_pins)
            produced = {name: sha(folder/name) for name in ('microlib.ascii', 'macro.ascii', 'metadata.ascii')}
            join(outputs, {str(folder/name): h for name, h in produced.items()})
            receipt = dict(temperature_C=temperature, returncode=0, elapsed_s=time.monotonic()-start,
                           outputs=produced, terminal=terminal)
            dump(folder/'receipt.json', receipt)
            receipts.append(receipt)
            # Refuse immediately if any state's data checks fail; no next state.
            result = check.analyze(folder, plane, plan, refs)
            dump(folder/'material_check.json', result)
            results.append(result)
            require(time.monotonic() < deadline, 'material/first-check budget exhausted')
            print('MATERIAL_DATA_CHECKED', temperature, flush=True)
        verify(pins); verify(staged); verify(outputs)
        dump(WORK/'material_checks.json', results)
        dump(WORK/'completed.json', dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW', material_solves=3,
            microscopic_entries=177, mixtures=18, transport_solves=0, production_replaced=False))
    finally:
        dump(WORK/'staged_inputs.json', staged)
        dump(WORK/'output_hashes.json', outputs)
        dump(WORK/'receipts.json', receipts)
        c.manifest(WORK)


def review(deadline):
    plan, pins, refs = load()
    authorization(CONTROL/'authorization.json')
    join(pins, c.pins_from_manifest(WORK))
    for name in ('inputs.json', 'staged_inputs.json', 'output_hashes.json'):
        join(pins, json.loads((WORK/name).read_text()))
    verify(pins)
    require(json.loads((WORK/'completed.json').read_text()) == dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',
        material_solves=3, microscopic_entries=177, mixtures=18, transport_solves=0, production_replaced=False), 'incomplete material batch')
    receipts = json.loads((WORK/'receipts.json').read_text())
    require([r['temperature_C'] for r in receipts] == list(check.TEMPERATURES), 'material order differs')
    for temperature, receipt in zip(check.TEMPERATURES, receipts):
        folder = WORK/f'material{temperature}'
        require(receipt == json.loads((folder/'receipt.json').read_text()) and receipt['returncode'] == 0, 'material receipt differs')
        expected = {str(folder/name): pins[str(source)] for name, source in stage_inputs(plan, temperature).items()}
        require(json.loads((folder/'input_hashes.json').read_text()) == expected, 'material lineage differs')
        verify({str(folder/name): h for name, h in receipt['outputs'].items()})
    results = check_all(plan, refs)
    require(results == json.loads((WORK/'material_checks.json').read_text()), 'independent replay differs')
    for temperature, result in zip(check.TEMPERATURES, results):
        require(result == json.loads((WORK/f'material{temperature}/material_check.json').read_text()), 'per-state check differs')
    verify(pins)
    require(time.monotonic() < deadline, 'review exceeded budget')
    REVIEW.mkdir()
    dump(REVIEW/'inputs.json', pins)
    dump(REVIEW/'review.json', dict(status=PASS, native_engines_started=0, cases=results,
        original_result_manifest_sha256=sha(WORK/'result.sha256'), production_accepted=False))
    c.manifest(REVIEW)


def controller(path):
    a = authorization(path)
    load()
    require(all(not path.exists() for path in (WORK, CONTROL, REVIEW)), 'fresh directories required')
    require(shutil.disk_usage(p.ROOT).free >= runtime_plan()['free_space_required_bytes'], 'insufficient storage')
    start, utc = time.monotonic(), dt.datetime.now(dt.timezone.utc)
    CONTROL.mkdir(); WORK.mkdir()
    dump(CONTROL/'authorization.json', a)
    state = dict(status='RUNNING', supervisor_pid=os.getpid(), started_utc=utc.isoformat(),
        deadline_utc=(utc+dt.timedelta(seconds=TOTAL)).isoformat(), total_seconds=TOTAL,
        review_reserve_seconds=RESERVE, retries=0)
    dump(CONTROL/'run_status.json', state)
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, signal.default_int_handler)
    cmd = [sys.executable, '-B', str(Path(__file__).resolve())]
    try:
        rc = c.supervised(cmd+['--worker', str(start+TOTAL-RESERVE)], CONTROL/'controller.log', start+TOTAL-RESERVE)
        require(rc == 0, 'material worker failed; no retry')
        state['status'] = 'PENDING_INDEPENDENT_REVIEW'
        (CONTROL/'run_status.json').write_text(json.dumps(state, indent=2)+'\n')
        end = min(start+TOTAL, time.monotonic()+RESERVE)
        rc = c.supervised(cmd+['--review', str(end)], CONTROL/'review.log', end)
        require(rc == 0, 'independent material review failed; no retry')
        state['status'] = PASS
    except subprocess.TimeoutExpired:
        state['status'] = 'TIMEOUT_NO_RETRY'; traceback.print_exc()
    except BaseException:
        state['status'] = 'FAILED_NO_RETRY'; traceback.print_exc()
    finally:
        state.update(finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(), elapsed_s_including_cleanup=time.monotonic()-start)
        (CONTROL/'run_status.json').write_text(json.dumps(state, indent=2)+'\n')
        c.manifest(CONTROL)
    print(json.dumps(state), flush=True)
    if state['status'] != PASS:
        raise SystemExit(2)


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--run', type=Path)
    mode.add_argument('--worker', type=float)
    mode.add_argument('--review', type=float)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.check:
        _, pins, _ = load()
        require(all(not path.exists() for path in (WORK, CONTROL, REVIEW)), 'not fresh')
        print('PREFLIGHT_PASS', len(pins), 'identities; native engines started: 0')
    elif args.run:
        controller(args.run)
    elif args.worker is not None:
        worker(args.worker)
    else:
        review(args.review)

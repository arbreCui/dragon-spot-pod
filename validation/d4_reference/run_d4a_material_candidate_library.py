"""One separately authorized private concatenation/format roundtrip, no TONE.

Use the existing process-group watchdog, manifest and native terminal helpers.
No nuclear-data processing modules are invoked: all five DRAGR data units are 0.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback

import numpy as np
import prepare_d4a_material_candidate as p
import run_remaining_temperature_batch as c

require, sha, verify, dump = c.require, c.sha, c.verify, c.dump
PREP = p.ART/'d4a-actual-temperature-material-prepared-20261003'
SEAL = '563fcab14bb523ec934455ad539fb091b0c95d32b4acaf59e0aa75eecb0d84c0'
RUNTIME = p.ART/'d4a-actual-temperature-library-runtime-20261003'
WORK = p.ART/'d4a-actual-temperature-library-run-20261003'
CONTROL, REVIEW = Path(str(WORK)+'-control'), Path(str(WORK)+'-review')
CANDIDATE = p.ART/'d4a-mt51-mf6-control-prepared-20261001/candidate/build'
EXE, DYLIB = CANDIDATE/'fe56_njoy', CANDIDATE/'source/libnjoy.dylib'
TOTAL, RESERVE = 900, 180
SCOPE = '28_REVIEWED_REFERENCES_PRIVATE_CONCATENATION_AND_FORMAT_ONLY'
MERGE = 'dragr\n0 0 0 0 0 29 30 0 /\nstop\n'
PASS = 'PASS_PRIVATE_LIBRARY_ROUNDTRIP_ONLY'


def join(pins, extra):
    for path, digest in extra.items():
        require(path not in pins or pins[path] == digest, 'conflicting input identity')
        pins[path] = digest


def source_plan():
    require(sha(PREP/'result.sha256') == SEAL, 'source preparation changed')
    pins = c.pins_from_manifest(PREP)
    verify(pins)
    plan = json.loads((PREP/'preparation.json').read_text())
    require(plan['status'] == 'STATIC_MATERIAL_CANDIDATE_PREPARED_NOT_AUTHORIZED', 'wrong source plan')
    rows = plan['sources']
    require(len(rows) == 28 and len({r['nuclide'] for r in rows}) == 28 and
            not p.MO.intersection(r['nuclide'] for r in rows), 'candidate membership differs')
    require(rows == sorted(rows, key=lambda r: r['nuclide']), 'source order drift')
    join(pins, plan['inputs'])
    for row in rows:
        require(pins.get(row['path']) == row['sha256'], 'unsealed reference')
    join(pins, {str(EXE): 'd467eade84888532df6a42b2559cee1b738da9130ed6433a1c7226eae0354ec0',
                str(DYLIB): 'aa97ae6ff1a3779f4cd9ea98ea30dd61f2de7c40e44e68e77730be3dc530bdb4'})
    paths = [Path(__file__), Path(p.__file__), Path(c.__file__), Path(c.batch.__file__),
             c.batch.API_PATH, c.batch.COMPARE_PATH,
             Path(c.batch.mt51.__file__),
             p.ROOT/'validation/d4_reference/audit_fe56_candidate_scope.py',
             p.ROOT/'validation/d4_reference/test_d4a_material_candidate_library.py']
    paths += [Path(c.API[name].__file__) for name in ('nr', 'sr', 'adapter', 'bounded')]
    paths += [CANDIDATE.parent/'source/src'/name for name in ('dragr.f90', 'xsmm.f90')]
    for path in paths:
        join(pins, {str(path): sha(path)})
    verify(pins)
    require((PREP/'merge.inp').read_text() == MERGE, 'not the pure concatenation card')
    return plan, pins


def export_deck(rows):
    # Reopen the XSM in a different Dragon process. Export each subtree separately
    # so the independent Python replay does not hold an entire 839 MB ASCII library.
    lines = ["XSM_FILE LIB :: FILE './DLIB_370_bin' ;", 'LINKED_LIST META ;',
             "SEQ_ASCII ROOT :: FILE './root.ascii' ;", 'MODULE UTL: DELETE: END: ;']
    for index, row in enumerate(rows, 1):
        lines.append(f"SEQ_ASCII N{index:02d} :: FILE './{row['nuclide']}.ascii' ;")
    for index, row in enumerate(rows, 1):
        lines.append(f"N{index:02d} := LIB :: STEP UP {row['nuclide']} ;")
    lines += ['META := LIB ;', 'META := UTL: META :: EDIT 0']
    lines += [f"  DEL {row['nuclide']}" for row in rows]
    lines += [';', 'ROOT := META ;', 'META := DELETE: META ;',
              'ECHO "D4A-PRIVATE-LIBRARY-REOPEN-COMPLETE" ;', 'END: ;']
    return '\n'.join(lines)+'\n'


def merge_roots(existing, incoming):
    """Model xsmequ's union, refusing any conflicting physical root record.

README is file provenance text, not physics. Its final value must equal the
last source in the declared copy order; it is not dropped from comparison.
"""
    for key, value in incoming.items():
        require(len(key) == 1 and value[0] not in (0, 10), 'non-scalar root record')
        if key in existing and key != ('README',):
            c.API['equal_records']({key: existing[key]}, {key: value})
        if key == ('README',):
            require(value[0] == 3, 'README must remain provenance text')
        existing[key] = value


def reference_roots(plan):
    combined = {}
    for row in plan['sources']:
        data = c.API['decode'](Path(row['path']), True)
        root = {k: v for k, v in data.items() if len(k) == 1 and k[0] != row['nuclide']}
        merge_roots(combined, root)
    return combined


def prepare():
    require(not RUNTIME.exists(), 'runtime preparation already exists')
    plan, pins = source_plan()
    roots = reference_roots(plan)
    verify(pins)
    RUNTIME.mkdir()
    (RUNTIME/'merge.inp').write_text(MERGE)
    (RUNTIME/'import.x2m').write_text('''* Private candidate format import only; EXPORT is a retained input copy.
XSM_FILE DLIB_370_bin :: FILE './DLIB_370_bin' ;
SEQ_ASCII EXPORT :: FILE './EXPORT' ;
MODULE END: ;
DLIB_370_bin := EXPORT :: EDIT 0 ;
ECHO "D4A-PRIVATE-LIBRARY-IMPORT-COMPLETE" ;
END: ;
''')
    (RUNTIME/'export.x2m').write_text(export_deck(plan['sources']))
    # Native replay can retain a growing ASCII and its binary scratch at each
    # stage. This is a storage estimate/check, not a physical acceptance parameter.
    sizes = [Path(r['path']).stat().st_size for r in plan['sources']]
    cumulative = sum(sum(sizes[:i]) for i in range(1, len(sizes)+1))
    dump(RUNTIME/'inputs.json', pins)
    dump(RUNTIME/'plan.json', dict(status='PREPARED_NOT_AUTHORIZED', scope=SCOPE,
        prepared_manifest_sha256=SEAL, total_seconds=TOTAL, review_reserve_seconds=RESERVE,
        native_stages=30, merge_stages=28, dragon_format_stages=2, retries=0,
        source_bytes=sum(sizes), cumulative_ascii_output_bytes_estimate=cumulative,
        root_records=list(k[0] for k in roots), root_typed_sha256=p.tree_digest(roots),
        root_policy='Union of all physical root records; all repeated physical values must be bit-exact. README remains the exact last-source provenance string, per xsmequ copy order.',
        free_space_required_bytes=2*cumulative+4*sum(sizes)+1024**3,
        limits=['The storage estimate is conservative bookkeeping, not a guaranteed native peak.',
                '28 pure DRAGR concatenations and 2 Dragon format operations only.',
                'No PENDF/GROUPR/TONE/ASM/FLU/Picard/CE or production replacement.',
                'Exact complete subtree and root metadata comparisons; no new numerical tolerance.']))
    c.manifest(RUNTIME)
    print('PREPARED_NOT_AUTHORIZED', sha(RUNTIME/'result.sha256'), flush=True)


def load():
    plan, pins = source_plan()
    runtime_pins = c.pins_from_manifest(RUNTIME)
    verify(runtime_pins)
    stored = json.loads((RUNTIME/'inputs.json').read_text())
    require(stored == pins, 'runtime/source or helper identity changed')
    join(pins, runtime_pins)
    runtime = json.loads((RUNTIME/'plan.json').read_text())
    require(runtime['status'] == 'PREPARED_NOT_AUTHORIZED' and runtime['scope'] == SCOPE and
            runtime['prepared_manifest_sha256'] == SEAL and runtime['native_stages'] == 30 and
            runtime['total_seconds'] == TOTAL and runtime['review_reserve_seconds'] == RESERVE,
            'runtime scope changed')
    require((RUNTIME/'merge.inp').read_text() == MERGE, 'wrong native module')
    require((RUNTIME/'export.x2m').read_text() == export_deck(plan['sources']), 'export scope changed')
    verify(pins)
    return plan, pins, runtime


def authorization(path):
    auth = json.loads(path.read_text())
    require(auth.get('status') == 'EXPLICIT_USER_APPROVAL' and auth.get('user_approval_text') == '批准',
            'explicit new approval missing')
    expected = dict(scope=SCOPE, prepared_manifest_sha256=SEAL,
        runtime_manifest_sha256=sha(RUNTIME/'result.sha256'), driver_sha256=sha(__file__),
        total_seconds=TOTAL, review_reserve_seconds=RESERVE, native_stages=30,
        attempts=1, retry=False)
    require(all(auth.get(k) == v for k, v in expected.items()), 'approval scope/identity differs')
    return auth


def dragon_terminal(log, marker):
    text = log.read_text()
    require('normal end of execution for dragon' in text.lower() and marker in text, 'Dragon did not finish')
    modules = re.findall(r'->@BEGIN MODULE\s*:\s*(\S+)', text)
    require(not set(modules) - {'EQU:', 'UTL:', 'DELETE:', 'END:'}, 'non-format Dragon module')


def check_saved(plan):
    nr, decode, equal = c.API['nr'], c.API['decode'], c.API['equal_records']
    root = decode(WORK/'export/root.ascii')
    require(all(len(k) == 1 and v[0] not in (0, 10) for k, v in root.items()), 'unexpected leftover subtree')
    require(nr.data(root, ('SIGNATURE',)) == 'L_DRAGLIB', 'wrong candidate signature')
    e = np.asarray(nr.data(root, ('ENERGY',)), dtype='<f4')
    import hashlib
    require(hashlib.sha256(e.tobytes()).hexdigest() == plan['energy_float32_sha256'], 'energy differs')
    results, combined = [], {}
    for row in plan['sources']:
        source = decode(Path(row['path']), True)
        prefix = row['nuclide']
        original = {k[1:]: v for k, v in source.items() if k[0] == prefix and len(k) > 1}
        exported = decode(WORK/'export'/f'{prefix}.ascii')
        equal(original, exported)
        wrapped = {(prefix,): source[(prefix,)]}
        wrapped.update({(prefix,)+k: v for k, v in exported.items()})
        require(p.tree_digest(wrapped) == row['typed_subtree_sha256'], 'prepared subtree image differs')
        global_records = {k: v for k, v in source.items() if len(k) == 1 and k[0] != prefix}
        merge_roots(combined, global_records)
        results.append(dict(nuclide=prefix, exact_subtree_records=len(original),
                            typed_subtree_sha256=row['typed_subtree_sha256']))
    equal(combined, root)
    runtime = json.loads((RUNTIME/'plan.json').read_text())
    require(p.tree_digest(root) == runtime['root_typed_sha256'], 'prepared root image differs')
    return dict(status='EXACT_PRIVATE_LIBRARY_ROUNDTRIP', cases=results,
        complete_subtrees=28, unchanged_production_Mo=True, material_accepted=False)


def worker(deadline):
    plan, pins, _ = load()
    authorization(CONTROL/'authorization.json')
    join(pins, {str(CONTROL/'authorization.json'): sha(CONTROL/'authorization.json')})
    dump(WORK/'inputs.json', pins)
    staged, outputs, receipts = {}, {}, []

    def stage(label, executable, deck, inputs, output_names, mutable=()):
        folder = WORK/label
        folder.mkdir(parents=True)
        before = {}
        for name, source in dict(inputs, **{'input.in': str(deck)}).items():
            expected = outputs.get(str(source), pins.get(str(source)))
            require(expected is not None and sha(source) == expected, 'stage lineage changed')
            target = folder/name
            shutil.copyfile(source, target)
            require(sha(target) == expected, 'staging copy differs')
            before[str(target)] = expected
            if name not in mutable:
                staged[str(target)] = expected
        dump(folder/'input_hashes.json', before)
        verify({str(executable): pins[str(executable)], str(DYLIB): pins[str(DYLIB)]})
        remaining = deadline-time.monotonic()
        require(remaining > 0, 'native budget exhausted')
        print('START', label, dt.datetime.now(dt.timezone.utc).isoformat(), flush=True)
        started = time.monotonic()
        c.bounded.run(executable, folder/'input.in', folder/'native.log', remaining)
        if executable == EXE:
            c.native_terminal((folder/'native.log').read_text())
        else:
            dragon_terminal(folder/'native.log', 'D4A-PRIVATE-LIBRARY-'+('IMPORT' if label == 'import' else 'REOPEN')+'-COMPLETE')
        verify({path: digest for path, digest in before.items() if Path(path).name not in mutable})
        produced = {}
        for name in output_names:
            path = folder/name
            require(path.is_file() and path.stat().st_size > 0, 'missing stage output')
            outputs[str(path)] = produced[name] = sha(path)
        receipt = dict(label=label, returncode=0, elapsed_s=time.monotonic()-started,
            mutable_input_preimages={Path(path).name: digest for path, digest in before.items() if Path(path).name in mutable},
            outputs=produced)
        dump(folder/'receipt.json', receipt)
        receipts.append(receipt)
        print('END', label, flush=True)
        return folder

    try:
        previous = None
        for index, row in enumerate(plan['sources'], 1):
            inputs = {'tape29': row['path']}
            if previous is not None:
                inputs['tape30'] = str(previous/'tape30')
            previous = stage(f'merge/{index:02d}-{row["nuclide"]}', EXE, RUNTIME/'merge.inp',
                             inputs, ['tape30'], mutable=('tape30',))
        dragon = Path(plan['assets']['Dragon']['path'])
        imported = stage('import', dragon, RUNTIME/'import.x2m',
                         {'EXPORT': str(previous/'tape30')}, ['DLIB_370_bin'])
        stage('export', dragon, RUNTIME/'export.x2m', {'DLIB_370_bin': str(imported/'DLIB_370_bin')},
              ['root.ascii']+[row['nuclide']+'.ascii' for row in plan['sources']])
        require(len(receipts) == 30, 'incomplete stage graph')
        dump(WORK/'roundtrip_check.json', check_saved(plan))
        verify(pins); verify(staged); verify(outputs)
        require(time.monotonic() < deadline, 'first-check budget exhausted')
        dump(WORK/'completed.json', dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',
             native_stages=30, nuclear_processing_stages=0, material_solves=0, production_replaced=False))
    finally:
        dump(WORK/'staged_inputs.json', staged)
        dump(WORK/'output_hashes.json', outputs)
        dump(WORK/'receipts.json', receipts)
        c.manifest(WORK)


def review(deadline):
    plan, pins, _ = load()
    authorization(CONTROL/'authorization.json')
    join(pins, c.pins_from_manifest(WORK))
    for name in ('inputs.json', 'staged_inputs.json', 'output_hashes.json'):
        join(pins, json.loads((WORK/name).read_text()))
    verify(pins)
    require(json.loads((WORK/'completed.json').read_text()) == dict(status='COMPLETE_PENDING_INDEPENDENT_REVIEW',
            native_stages=30, nuclear_processing_stages=0, material_solves=0, production_replaced=False), 'incomplete worker')
    receipts = json.loads((WORK/'receipts.json').read_text())
    expected = [f'merge/{i:02d}-{r["nuclide"]}' for i, r in enumerate(plan['sources'], 1)]+['import', 'export']
    require([r['label'] for r in receipts] == expected, 'stage sequence differs')
    previous = None
    for row, receipt in zip(plan['sources'], receipts[:28]):
        folder = WORK/receipt['label']
        inputs = json.loads((folder/'input_hashes.json').read_text())
        require(inputs[str(folder/'tape29')] == row['sha256'], 'reference input differs')
        require(receipt['mutable_input_preimages'] == ({} if previous is None else {'tape30': previous}), 'merge parent differs')
        if previous is not None:
            require(inputs[str(folder/'tape30')] == previous, 'merge preimage differs')
        previous = receipt['outputs']['tape30']
    require(json.loads((WORK/'import/input_hashes.json').read_text())[str(WORK/'import/EXPORT')] == previous, 'import not linked to final merge')
    require(json.loads((WORK/'export/input_hashes.json').read_text())[str(WORK/'export/DLIB_370_bin')] == receipts[28]['outputs']['DLIB_370_bin'], 'reopen not linked to import')
    for receipt in receipts:
        folder = WORK/receipt['label']
        require(receipt == json.loads((folder/'receipt.json').read_text()) and receipt['returncode'] == 0, 'stage receipt differs')
        verify({str(folder/name): digest for name, digest in receipt['outputs'].items()})
        if receipt['label'].startswith('merge/'):
            c.native_terminal((folder/'native.log').read_text())
        else:
            dragon_terminal(folder/'native.log', 'D4A-PRIVATE-LIBRARY-'+('IMPORT' if receipt['label'] == 'import' else 'REOPEN')+'-COMPLETE')
    result = check_saved(plan)
    require(result == json.loads((WORK/'roundtrip_check.json').read_text()), 'independent saved replay differs')
    verify(pins)
    require(time.monotonic() < deadline, 'independent review budget exhausted')
    REVIEW.mkdir()
    dump(REVIEW/'inputs.json', pins)
    dump(REVIEW/'review.json', dict(status=PASS, native_engines_started=0, result=result,
         production_accepted=False, original_result_manifest_sha256=sha(WORK/'result.sha256')))
    c.manifest(REVIEW)


def controller(path):
    auth = authorization(path)
    _, _, runtime = load()
    require(all(not path.exists() for path in (WORK, CONTROL, REVIEW)), 'fresh one-shot directories required')
    require(shutil.disk_usage(p.ROOT).free >= runtime['free_space_required_bytes'], 'insufficient free storage')
    start, utc = time.monotonic(), dt.datetime.now(dt.timezone.utc)
    CONTROL.mkdir(); WORK.mkdir()
    dump(CONTROL/'authorization.json', auth)
    state = dict(status='RUNNING', supervisor_pid=os.getpid(), started_utc=utc.isoformat(),
        deadline_utc=(utc+dt.timedelta(seconds=TOTAL)).isoformat(), total_seconds=TOTAL,
        review_reserve_seconds=RESERVE, retries=0)
    dump(CONTROL/'run_status.json', state)
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, signal.default_int_handler)
    cmd = [sys.executable, '-B', str(Path(__file__).resolve())]
    try:
        rc = c.supervised(cmd+['--worker', str(start+TOTAL-RESERVE)], CONTROL/'controller.log', start+TOTAL-RESERVE)
        require(rc == 0, 'worker failed; no retry')
        state['status'] = 'PENDING_INDEPENDENT_REVIEW'
        (CONTROL/'run_status.json').write_text(json.dumps(state, indent=2)+'\n')
        deadline = min(start+TOTAL, time.monotonic()+RESERVE)
        rc = c.supervised(cmd+['--review', str(deadline)], CONTROL/'review.log', deadline)
        require(rc == 0, 'independent review failed; no retry')
        state['status'] = PASS
    except subprocess.TimeoutExpired:
        state['status'] = 'TIMEOUT_NO_RETRY'
        traceback.print_exc()
    except BaseException:
        state['status'] = 'FAILED_NO_RETRY'
        traceback.print_exc()
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
        plan, pins, runtime = load()
        require(all(not path.exists() for path in (WORK, CONTROL, REVIEW)), 'not fresh')
        print('PREFLIGHT_PASS', len(pins), 'identities; native engines started: 0')
    elif args.run:
        controller(args.run)
    elif args.worker is not None:
        worker(args.worker)
    else:
        review(args.review)

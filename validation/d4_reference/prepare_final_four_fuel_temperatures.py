"""Saved-output review and the exact final-four input graph. No run mode."""
import copy
import json
from pathlib import Path
import shutil
import signal
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'validation/artifacts'
FIX = ART/'d4a-pu241-mixed-order-checker-20261002'
FIX_SHA = '720617bcb23d7746730c63cbdf160e6478aff267ad0549e8f168f01572f94b2b'
PRIOR = ART/'d4a-remaining-fuel-temperature-run-20261001'
OLD_PREP = ART/'d4a-remaining-fuel-temperature-prepared-20261001'
DEST = ART/'d4a-final-four-fuel-temperature-prepared-20261002'
WORK = ART/'d4a-final-four-fuel-temperature-run-20261002'
FUELS = ['Pu241', 'Pu242', 'U235', 'U238']
RETAIN = ['Am241', 'Pu238', 'Pu239', 'Pu240']
sys.path.insert(0, str(FIX))
import run_remaining_temperature_batch as c

b = c.batch
require, sha, verify, dump = c.require, c.sha, c.verify, c.dump


def merge(pins, extra):
    for path, digest in extra.items():
        require(path not in pins or pins[path] == digest, 'conflicting source identity')
        pins[path] = digest


def rows():
    return [r for r in b.cases() if r['nuclide'] in FUELS]


def graph(work):
    native, cached = [], []
    for row in rows():
        for s in b.stages(row, work):
            item = dict(label=s['label'], kind=s['kind'], control=s['control'],
                        deck=str(s['deck']), inputs={k:str(v) for k,v in s['inputs'].items()},
                        output=str(s['output']))
            if row['nuclide'] == 'Pu241' and s['control']:
                item.update(source_directory=str(PRIOR/s['label']),
                            copy_files=['tape30', 'native.log', 'receipt.json'])
                cached.append(item)
            else:
                native.append(item)
    require(len(native) == 39 and len(cached) == 5, 'final-four stage count')
    return native, cached


def validate_graph(work, native, cached, pins):
    require((native, cached) == graph(work), 'fixed final-four graph changed')
    available = set()
    for item in cached:
        for name in item['copy_files']:
            require(str(Path(item['source_directory'])/name) in pins, 'unsealed cached stage')
        available.add(item['output'])
    for item in native:
        require(item['deck'] in pins, 'unsealed deck')
        require(item['output'] not in available, 'duplicate output')
        for path in item['inputs'].values():
            require(path in available if Path(path).is_relative_to(work) else path in pins,
                    'future or unsealed input')
        available.add(item['output'])
    require(len(available) == 44, 'incomplete final-four graph')


def stage_check(stage, pins):
    folder = Path(stage['output']).parent
    for name in ('tape30', 'native.log', 'receipt.json'):
        require(str(folder/name) in pins, 'stage outside sealed evidence')
    receipt = json.loads((folder/'receipt.json').read_text())
    require(receipt['returncode'] == 0 and receipt['output_sha256'] == pins[str(folder/'tape30')],
            'stage receipt differs')
    c.native_terminal((folder/'native.log').read_text())
    return dict(label=stage['label'], elapsed_s=receipt['elapsed_s'],
                output_sha256=receipt['output_sha256'])


def prepare():
    started = time.monotonic()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('180s saved preparation limit')))
    signal.alarm(180)
    require(not DEST.exists(), 'preparation already exists')
    require(all(not p.exists() for p in (WORK, Path(str(WORK)+'-control'), Path(str(WORK)+'-review'))),
            'future work already exists')
    require(sha(FIX/'result.sha256') == FIX_SHA, 'checker review changed')
    require(Path(b.mt51.__file__).resolve() == FIX/'check_mt51_repair.py', 'wrong checker loaded')
    pins = json.loads((FIX/'inputs.json').read_text())
    merge(pins, c.pins_from_manifest(FIX))
    merge(pins, {str(Path(__file__).resolve()):sha(Path(__file__))})
    verify(pins)
    require(json.loads((Path(str(PRIOR)+'-control')/'run_status.json').read_text())['status'] == 'FAILED_NO_RETRY',
            'prior batch not stopped')
    require(json.loads((FIX/'replay.json').read_text())['status'] == 'ISOLATED_MIXED_ORDER_CHECKER_VALIDATED',
            'mixed-order checker not validated')
    old = json.loads((OLD_PREP/'plan.json').read_text())
    all_rows = {r['nuclide']:r for r in old['cases']}
    require(set(all_rows) == set(RETAIN+FUELS), 'fuel partition differs')
    native, cached = graph(WORK)
    validate_graph(WORK, native, cached, pins)
    # Small negative tests exercise the real graph checker, never a solver.
    bad = copy.deepcopy(native)
    next(s for s in bad if s['label'].endswith('high/dragr'))['inputs']['tape29'] = all_rows['Pu241']['original_library']
    missing_pin = dict(pins)
    del missing_pin[str(Path(cached[0]['source_directory'])/'tape30')]
    for ns, cs, ps in ((native[:-1], cached, pins), (bad, cached, pins), (native, cached, missing_pin)):
        try:
            validate_graph(WORK, ns, cs, ps)
        except ValueError:
            pass
        else:
            raise ValueError('negative graph test unexpectedly accepted')
    DEST.mkdir()
    retained, receipts = [], []
    for name in RETAIN:
        control = b.control_check(all_rows[name], PRIOR)
        expanded = b.expanded_check(all_rows[name], PRIOR)
        require(control == json.loads((PRIOR/name/'control_check.json').read_text()), 'saved control differs')
        require(expanded == json.loads((PRIOR/name/'comparison.json').read_text()), 'saved expansion differs')
        for stage in b.stages(all_rows[name], PRIOR):
            receipts.append(stage_check(stage, pins))
        dump(DEST/(name+'_control_check.json'), control)
        dump(DEST/(name+'_comparison.json'), expanded)
        library = PRIOR/name/'expanded/high/dragr/tape30'
        retained.append(dict(nuclide=name, library=str(library), sha256=pins[str(library)],
            status=expanded['status'], controls_exact_records=expanded['controls_exact_records'],
            finite_weighted_tables=len(expanded['finite_weighted_tables'])))
        print('SAVED_REFERENCE_REPLAY_PASS', name, flush=True)
    pu241_receipts = [stage_check(s, pins) for s in b.stages(all_rows['Pu241'], PRIOR) if s['control']]
    verify(pins)
    dump(DEST/'retained_review.json', dict(status='PASS_FOUR_SAVED_FUEL_REFERENCES_ONLY',
        cases=retained, native_engines_started=0, historical_new_stages=39, historical_cached_stages=5,
        receipts=receipts, prior_batch_status_unchanged='FAILED_NO_RETRY',
        review_scope='Separate saved-state review, not the failed batch review or a native retry',
        historical_low_GENDF_available=False, production_accepted=False))
    dump(DEST/'inputs.json', pins)
    dump(DEST/'plan.json', dict(status='PREPARED_NOT_AUTHORIZED_NO_NATIVE_EXECUTION',
        scope='FOUR_FUELS_12_ACTUAL_TEMPERATURE_PAIRS_REFERENCE_ONLY', future_work=str(WORK),
        native_stages=39, cached_stages=5, nuclides=FUELS, actual_temperature_pairs=12,
        cases=rows(), stages=native, reused_stages=cached, retained_completed_libraries=retained,
        retained_sixteen_libraries=old['retained_completed_libraries'],
        candidate_executable=old['candidate_executable'], candidate_dylib=old['candidate_dylib'],
        checker_module=str(FIX/'check_mt51_repair.py'), checker_review_manifest_sha256=FIX_SHA,
        pu241_saved_control=str(FIX/'Pu241_control_check.json'), pu241_saved_stage_receipts=pu241_receipts,
        proposed_total_seconds=21600, proposed_review_reserve_seconds=600, attempts=1, retry=False,
        original_cost_logs=[r for r in old['original_cost_logs'] if r['nuclide'] in FUELS],
        disk_free_bytes_at_preparation=shutil.disk_usage(ROOT).free,
        driver_status='NOT_IMPLEMENTED_NOT_AUTHORIZED',
        limits=['Six hours is a proposed wall-clock cap, not a runtime guarantee or a physics parameter.',
                'Old CPU logs do not include full DRAGR processing; disk capacity must be checked before launch.',
                'Five cached Pu241 control stages must be rechecked, not rerun.',
                'Keep original five temperatures, 18 finite dilutions, signed P1 and exact storage checks.',
                'No comparison is claimed to missing historical low GENDF.',
                'No material/TONE/transport/Picard/CE, production replacement or new k.',
                'Never resume the failed eight-fuel batch or spend its unused budget.']))
    dump(DEST/'preflight.json', dict(status='SAVED_REVIEW_AND_FIXED_GRAPH_PASS',
        native_engines_started=0, retained_references=4, graph_negative_tests=3,
        source_identities_unchanged=len(pins), elapsed_s=time.monotonic()-started))
    c.manifest(DEST)
    signal.alarm(0)
    print('PREPARED_NOT_AUTHORIZED', sha(DEST/'result.sha256'), flush=True)


if __name__ == '__main__':
    # Importing existing helpers does not authorize their native entry points.
    with patch('subprocess.Popen', side_effect=AssertionError('native launch forbidden in preparation')):
        prepare()

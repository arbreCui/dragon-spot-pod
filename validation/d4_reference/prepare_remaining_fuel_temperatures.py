"""Seal only the unfinished fuel input graph. This file has no run mode."""
import argparse
import json
from pathlib import Path
import re
import time

import run_mt51_mf6_control as am

c, b = am.common, am.b
require, sha, verify, dump = am.require, am.sha, am.verify, am.dump
DEST = b.ART/'d4a-remaining-fuel-temperature-prepared-20261001'
WORK = b.ART/'d4a-remaining-fuel-temperature-run-20261001'
PARTIAL = b.ART/'d4a-completed16-temperature-review-20261001'
FUELS = ['Am241','Pu238','Pu239','Pu240','Pu241','Pu242','U235','U238']
SEALS = {
    am.WORK: 'df477bf4790bc08b20d87b523608a26dac7c192f65c8f27b47c79a98b100ff94',
    am.CONTROL: '8844e1a1478fbee22bda431fd11e5bbd51955e04941bb95a2bb6d5ba0c74244e',
    am.REVIEW: 'a34f33befde7386cb4e4fcf4bc0c9700459b3fd7a6d16f8df2151a3a5e4fe1aa',
    PARTIAL: '33daf827f7f6b8e5a2e97064469fa99254e6d98f6b66717a5d0ff1d21dc8bc9c',
}


def merge(pins, extra):
    for path, digest in extra.items():
        require(path not in pins or pins[path] == digest, 'conflicting input identity')
        pins[path] = digest


def rows():
    selected = [r for r in b.cases() if r['route'] == 'ORIGINAL_LOW_THEN_HIGH_TWO_PASS']
    require([r['nuclide'] for r in selected] == FUELS, 'fuel coverage changed')
    require(all(len(r['actual_temperatures_K']) == 3 and len(r['all_temperatures_K']) == 8
                and r['expected_finite_dilutions'] == 18 for r in selected), 'temperature/dilution coverage')
    return selected


def graph(work):
    native, cached = [], []
    for row in rows():
        for s in b.stages(row, work):
            item = dict(label=s['label'], kind=s['kind'], control=s['control'],
                        deck=str(s['deck']), inputs={k:str(v) for k,v in s['inputs'].items()},
                        output=str(s['output']))
            if row['nuclide'] == 'Am241' and s['control']:
                source = am.PRIOR if s['kind'] == 'pendf' else am.WORK
                item['source_directory'] = str(source/s['label'])
                item['copy_files'] = ['tape30','native.log','receipt.json']
                cached.append(item)
            else:
                native.append(item)
    require(len(native) == 83 and len(cached) == 5, 'remaining/cached stage count')
    return native, cached


def validate_graph(work, native, cached, pins):
    require((native,cached) == graph(work), 'fixed stage graph changed')
    available = set()
    for item in cached:
        for name in item['copy_files']:
            require(str(Path(item['source_directory'])/name) in pins, 'unsealed reused stage')
        available.add(item['output'])
    for item in native:
        require(item['deck'] in pins, 'unsealed input deck')
        require(item['output'] not in available, 'duplicate output')
        for path in item['inputs'].values():
            require(path in available if Path(path).is_relative_to(work) else path in pins,
                    'future/missing input')
        available.add(item['output'])
    require(len(available) == 88, 'incomplete fuel graph')


def load_inputs():
    candidate, pins, _ = am.load()
    for folder, expected in SEALS.items():
        require(sha(folder/'result.sha256') == expected, 'reused result seal changed')
        merge(pins,c.pins_from_manifest(folder))
    merge(pins,json.loads((am.REVIEW/'inputs.json').read_text()))
    ar = json.loads((am.REVIEW/'review.json').read_text())
    require(ar['status'] == 'PASS_AM241_CONTROL_ONLY' and not ar['production_accepted'], 'Am241 control not accepted')
    partial = json.loads((PARTIAL/'review.json').read_text())
    require(partial['status'] == 'PARTIAL_REFERENCE_REPLAY_PASS' and partial['completed_cases'] == 16,
            'sixteen-case review missing')
    require({r['nuclide'] for r in partial['cases']} | set(FUELS) == {r['nuclide'] for r in b.cases()}
            and not ({r['nuclide'] for r in partial['cases']} & set(FUELS)), 'completed/remaining partition')
    prior_pins = json.loads((PARTIAL/'inputs.json').read_text())
    retained = []
    for row in partial['cases']:
        path = am.PRIOR/row['nuclide']/'expanded/dragr/tape30'
        require(str(path) in prior_pins, 'retained library not in independent review')
        merge(pins,{str(path):prior_pins[str(path)]})
        retained.append(dict(nuclide=row['nuclide'],library=str(path),sha256=prior_pins[str(path)]))
    # Cached receipts/logs, as well as their output, stay traceable to the old run.
    _, cached = graph(WORK)
    for item in cached:
        for name in item['copy_files']:
            path = Path(item['source_directory'])/name
            if item['kind'] == 'pendf':
                require(str(path) in prior_pins, 'old low-PENDF receipt outside sealed review')
                merge(pins,{str(path):prior_pins[str(path)]})
            require(str(path) in pins, 'cached input absent from accepted lineage')
        receipt = json.loads((Path(item['source_directory'])/'receipt.json').read_text())
        require(receipt['returncode'] == 0 and receipt['output_sha256'] ==
                pins[str(Path(item['source_directory'])/'tape30')], 'cached receipt differs')
        c.native_terminal((Path(item['source_directory'])/'native.log').read_text())
    merge(pins,{str(Path(__file__).resolve()):sha(Path(__file__)),
                str(Path(__file__).with_name('test_remaining_fuel_preparation.py')):
                sha(Path(__file__).with_name('test_remaining_fuel_preparation.py'))})
    verify(pins)
    return candidate,pins,retained


def cost_evidence(pins):
    result = []
    for row in rows():
        root = Path(row['original_library']).parent
        costs = {}
        for kind, filename in [('pendf','out_pendf_'),('groupr','out_gendf_'),('concat_only','out_draglibcat')]:
            path = root/(filename+row['nuclide'])
            with path.open('rb') as stream:
                stream.seek(max(0,path.stat().st_size-4096))
                tail = stream.read().decode('ascii')
            matched = re.search(r'\n\s*(\d+(?:\.\d+)?)s\s*\n\s*\*{10,}\s*\Z',tail)
            require(matched is not None, 'old cost log missing terminal')
            costs[kind] = dict(path=str(path),old_reported_seconds=float(matched[1]))
            merge(pins,{str(path):sha(path)})
        result.append(dict(nuclide=row['nuclide'],costs=costs))
    return result


def prepare(destination=DEST):
    start = time.monotonic()
    require(not destination.exists(), 'preparation already exists')
    require(all(not p.exists() for p in (WORK,WORK.with_name(WORK.name+'-control'),
                                         WORK.with_name(WORK.name+'-review'))), 'future work not fresh')
    candidate,pins,retained = load_inputs()
    native,cached = graph(WORK)
    validate_graph(WORK,native,cached,pins)
    costs = cost_evidence(pins)
    verify(pins)
    plan = dict(status='PREPARED_NOT_AUTHORIZED_NO_NATIVE_EXECUTION',native_engines_started=0,
        future_work=str(WORK),scope='EIGHT_FUELS_24_ACTUAL_TEMPERATURE_PAIRS_REFERENCE_ONLY',
        nuclides=FUELS,actual_temperature_pairs=24,native_stages=83,cached_stages=5,
        candidate_executable=candidate['candidate_executable'],candidate_dylib=candidate['candidate_dylib'],
        cases=rows(),stages=native,reused_stages=cached,retained_completed_libraries=retained,
        proposed_total_seconds=28800,proposed_review_reserve_seconds=600,attempts=1,retry=False,
        original_cost_logs=costs,
        cost_limits=['Old CPU log times are not a wall-clock guarantee.',
                     'The old concat-only DRAGR log excludes full processing; do not use it as DRAGR cost.',
                     'Am241 new five-temperature low/high GROUPR/DRAGR measured 221.875 seconds in total.',
                     'Am241 retained low-PENDF took 635.153 seconds. New eight-temperature PENDFs still required.',
                     'Eight hours is a proposed shared hard cap, including ten minutes review, not permission to run.'],
        checks=['Each of seven new five-temperature controls before its expanded processing.',
                'Reused Am241 control rechecked without native recomputation.',
                'Original control grids and non-MT51 data exact; all non-scatter records exact.',
                'Low/high source-driven scatter replay; all 18 finite points and signed P1 retained.',
                'Eight-temperature old control subtrees exact and direct P0 nonnegative.',
                'Independent saved-output replay of all eight results, plus retained sixteen identities.'],
        forbidden=['retry','recompute completed sixteen','native rerun of accepted Am241 control',
                   'TONE','material solve','transport','Picard','CE','production replacement'],
        limits=['No claim of comparison to missing historical low GENDF.',
                'No new k, precision acceptance or IRENA full-core validation.',
                'A bounded executor must be bound to this manifest and separately approved before launch.'])
    destination.mkdir()
    dump(destination/'inputs.json',pins)
    dump(destination/'plan.json',plan)
    dump(destination/'preflight.json',dict(status='STATIC_GRAPH_PASS',input_identities=len(pins),
        native_stages=83,cached_stages=5,retained_completed_cases=len(retained),
        elapsed_seconds=time.monotonic()-start,native_engines_started=0))
    c.manifest(destination)
    print('PREPARED_NOT_AUTHORIZED',sha(destination/'result.sha256'),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true',required=True)
    parser.parse_args()
    prepare()

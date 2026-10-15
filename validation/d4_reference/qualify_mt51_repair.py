"""Qualify the storage checker using frozen Fe56 data, without native solves."""
import argparse
import json
from pathlib import Path
import re
import runpy
import time

import numpy as np
import check_mt51_repair as check

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT/'validation/artifacts/d4a-fe56-mt51-control-candidate-20260929'
PAIR_SHA = 'a81fb4504793e40d86567ba70b4c13c30d5093bd5a79b5ebc132ce52af586843'
API_PATH = ROOT/'validation/artifacts/d4a-fe56-ganlib-tone650-run-20260929/run_once.py'
API = runpy.run_path(str(API_PATH), run_name='read_only')
EXPAND_PATH = ROOT/'validation/d4_reference/audit_fe56_candidate_scope.py'
EXPAND = runpy.run_path(str(EXPAND_PATH), run_name='read_only')['expand']


def refused(fn, text):
    try:
        fn()
    except ValueError as error:
        check.require(text in str(error), f'wrong refusal: {error}')
        return str(error)
    raise AssertionError('invalid input accepted')


def mutate_record(records, key):
    out = dict(records)
    v = np.asarray(records[key][1], dtype='f4').copy()
    i = int(np.argmax(abs(v)))
    v[i] = np.nextafter(v[i], np.float32(np.inf))
    out[key] = (2, tuple(float(x) for x in v))
    return out


def dense(records, prefix, order, finite):
    suffix = f'{order:02d}'
    data = lambda field: records[prefix+(field+suffix,)][1]
    return EXPAND(data('NJJS'), data('IJJS'), data('SCAT'), 370,
                  (25,281) if finite else None)[0].T


def trace_changes(raw, records):
    """Classify stored differences against pre-packing arithmetic, not a mask."""
    parsed = {side: check.parse(value,2631) for side,value in raw.items()}
    groups = {key: set() for key in ('infinite','finite','storage_only')}
    counts = {key: 0 for key in groups}
    signed = 0
    for it,t in enumerate(check.OLD_T,1):
        prefix = ('Fe56',f'SUBTMP{it:04d}')
        state = {side: check.accumulated_scattering(parsed[side][0],t,85)
                 for side in raw}
        sigma = np.asarray(parsed['control'][1][t]['sigma0'],dtype='f4')
        ds = np.asarray(records['control'][prefix+('DILUTION',)][1],dtype='f4')
        for z in range(len(sigma)):
            sub = prefix
            if z:
                sub += (f'SUBMAT{int(np.flatnonzero(ds == sigma[z])[0])+1:04d}',)
            for order in (0,1):
                prepack, stored = {}, {}
                for side in raw:
                    total,flux = state[side]
                    value = total[0,order]
                    if z:
                        ratio = flux[z,order].copy()
                        hit = flux[0,order] != 0
                        ratio[hit] /= flux[0,order,hit]
                        value = total[z,order]*ratio[:,None]-value
                    prepack[side] = value
                    stored[side] = dense(records[side],sub,order,bool(z))
                changed = stored['control'] != stored['candidate']
                family = 'finite' if z else 'infinite'
                counts[family] += int(changed.sum())
                groups[family].update((np.flatnonzero(changed.any(axis=1))+1).tolist())
                same_input = prepack['control'] == prepack['candidate']
                storage_only = changed & same_input
                counts['storage_only'] += int(storage_only.sum())
                groups['storage_only'].update((np.flatnonzero(storage_only.any(axis=1))+1).tolist())
                if order == 1:
                    signed += int((stored['candidate'] < 0).sum())
    return dict(changed_dense_entries=counts,
                changed_primary_groups={k: sorted(v) for k,v in groups.items()},
                signed_P1_stored_entries_retained=signed,
                interpretation='Both libraries are exactly replayed. Storage-only entries have identical pre-packing values; original DRAGR support/tail packing causes their stored difference. Infinite changes originate in MF6/MT51, not other reactions.',
                limitation='This proves data lineage/storage arithmetic, not that all MT51 quadrature values are exact or that SPOD accuracy passes.')


def qualify(output):
    start = time.monotonic()
    check.require(not output.exists(), 'output directory already exists')
    check.require(API['sha'](PAIR/'result.sha256') == PAIR_SHA, 'paired evidence seal changed')
    manifest = {name: digest for digest,name in
                (line.split(maxsplit=1) for line in (PAIR/'result.sha256').read_text().splitlines())}
    sources = [Path(__file__),Path(check.__file__),API_PATH,EXPAND_PATH,PAIR/'result.sha256']
    for module in ('nr','adapter','sr'):
        sources.append(Path(API[module].__file__))
    def frozen(relative):
        path = PAIR/relative
        check.require(API['sha'](path) == manifest[relative], f'frozen input changed: {relative}')
        sources.append(path)
        return path
    raw, records = {}, {}
    for side in ('control','candidate'):
        raw[side] = frozen(f'{side}/groupr/tape30').read_bytes()
        records[side] = API['decode'](frozen(f'{side}/dragr/tape30'), True)
        log = frozen(f'{side}/dragr/output').read_text()
        for pattern,value in ((r'number of thermal groups\s*\.+\s*(\d+)',85),
                              (r'first group of unresolved resonance xs data\s*\.\s*(\d+)',25),
                              (r'last group of resolved resonance xs data\s*\.+\s*(\d+)',281)):
            check.require([int(x) for x in re.findall(pattern,log)] == [value], 'DRAGR settings changed')
        frozen(f'{side}/source/src/dragr.f90')
        frozen(f'{side}/source/src/groupr.f90')
    protected = {
        ROOT/'validation/artifacts/d4a-scattering-mesh12-picard-runtime-20260925/Dragon':
            '873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef',
        Path('/Users/wen/draglib_output/shem370_endfb8r1_v5p1/draglibshem370_endfb8r1_v5p1.xsm'):
            '66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9',
    }
    API['verify'](protected)
    pins = {str(path): API['sha'](path) for path in sources}
    for path in sources:
        if path.is_relative_to(PAIR) and path.name != 'result.sha256':
            pins[str(path)] = manifest[str(path.relative_to(PAIR))]
    pins[str(PAIR/'result.sha256')] = PAIR_SHA
    pins.update({str(path): digest for path,digest in protected.items()})
    API['verify'](pins)
    scope = check.gendf_scope(raw['control'],raw['candidate'],2631)
    replay = {side: check.replay(raw[side],records[side],'Fe56',2631,(25,281),85)
              for side in raw}
    non_scatter = check.non_scatter_records_exact(records['control'],records['candidate'])
    negatives = {}
    for suffix in ('SCAT00','SCAT01'):
        key = ('Fe56','SUBTMP0001','SUBMAT0001',suffix)
        bad = mutate_record(records['candidate'],key)
        negatives[f'one_ulp_{suffix}'] = refused(
            lambda: check.replay(raw['candidate'],bad,'Fe56',2631,(25,281),85), 'storage replay differs')
    bad = mutate_record(records['candidate'],('Fe56','SUBTMP0001','NTOT0'))
    negatives['one_ulp_non_scatter'] = refused(
        lambda: check.non_scatter_records_exact(records['control'],bad), 'non-scattering real record changed')
    negatives['wrong_material'] = refused(lambda: check.parse(raw['candidate'],2632), 'wrong GENDF material')
    negatives['wrong_temperature'] = refused(
        lambda: check.gendf_scope(raw['control'],raw['candidate'],2631,(293.,550.,901.,1200.,2000.)), 'temperature drift')
    lines = raw['candidate'].decode('ascii').splitlines()
    i = next(i for i,line in enumerate(lines) if check.identity(line)[1:] == (3,51))
    lines[i] = ' 2.605700+4'+lines[i][11:]  # Valid field; forbidden MF3 header change.
    mutated = ('\n'.join(lines)+'\n').encode('ascii')
    negatives['non_MT51_mutation'] = refused(
        lambda: check.gendf_scope(raw['control'],mutated,2631), 'non-MF6/MT51 content changed')
    missing = dict(records['candidate'])
    key = ('Fe56','SUBTMP0001','DILUTION')
    missing[key] = (2,missing[key][1][1:])
    negatives['missing_dilution'] = refused(
        lambda: check.replay(raw['candidate'],missing,'Fe56',2631,(25,281),85), 'missing/duplicated')
    changes = trace_changes(raw,records)
    API['verify'](pins)
    result = dict(status='FE56_MT51_STORAGE_CHECKER_QUALIFIED_SAVED_DATA_ONLY',
                  elapsed_seconds=time.monotonic()-start, scope=scope, replay=replay,
                  non_scatter_records_exact=non_scatter, negative_tests=negatives,
                  numerical_change_trace=changes, native_engines_started=0,
                  protected_production_files_unchanged=True, remaining_24_batch_qualified=False,
                  limitations=['No NJOY, DRAGR, TONE, transport, Picard or CE run.',
                               'Fuel two-pass outputs and all remaining nuclides still require their own checks.',
                               'No empirical coefficient or new acceptance tolerance.',
                               'No new k result or SPOD accuracy acceptance.'])
    output.mkdir(parents=True)
    API['dump'](output/'inputs.json',pins)
    API['dump'](output/'review.json',result)
    with (output/'result.sha256').open('x') as stream:
        for path in sorted(output.iterdir()):
            if path.name != 'result.sha256':
                stream.write(f'{API["sha"](path)}  {path.name}\n')
    print(json.dumps(dict(status=result['status'],elapsed_seconds=result['elapsed_seconds'],
                         records_replayed=sum(x['records_checked'] for x in replay.values()),
                         non_scatter_records_exact=non_scatter,negative_tests=len(negatives),
                         numerical_change_trace=changes),indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    qualify(parser.parse_args().output)

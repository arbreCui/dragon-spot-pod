"""The fixed 24-nuclide input graph and read-only numerical gates.

No subprocesses or native processing are started by this module.
"""
import json
from pathlib import Path
import re
import runpy

import numpy as np
import check_mt51_repair as mt51
from audit_fe56_candidate_scope import expand

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'validation/artifacts'
PREP = ART/'d4a-remaining-temperature-twopass-prepared-20261001'
PREP_SHA = '94c5373cfce61979fe0270c1b0a0fb386907fea1c9c40a9642a92c0bb1dda656'
PAIR = ART/'d4a-fe56-mt51-control-candidate-20260929'
API_PATH = ART/'d4a-fe56-ganlib-tone650-run-20260929/run_once.py'
COMPARE_PATH = ART/'d4a-light-nuclide-actual-temperature-run-20261001/compare.py'
API = runpy.run_path(str(API_PATH),run_name='read_only')
COMPARE = runpy.run_path(str(COMPARE_PATH),run_name='read_only')['compare_records']
require, decode, equal, sha = (API[k] for k in ('require','decode','equal_records','sha'))
EXE = PAIR/'candidate/build/fe56_njoy'
BUDGET, RESERVE = 28800, 600


def cases():
    require(sha(PREP/'prepared.sha256') == PREP_SHA, 'prepared input seal changed')
    rows = json.loads((PREP/'preflight.json').read_text())['cases']
    require(len(rows) == 24 and sum(r['expected_native_stages'] for r in rows) == 138,
            'fixed batch inventory changed')
    # Independent cases: cheap single-pass gates precede the two-pass fuels.
    # This changes only execution order, never inputs or numerical parameters.
    return sorted(rows,key=lambda r:(r['expected_native_stages'],r['nuclide']))


def stages(row, work):
    """Each output is a new tape30. High DRAGR imports the matching low result."""
    name = row['nuclide']
    base, decks = work/name, PREP/name
    endf = Path(row['endf'])
    result = []
    def lane(relative, deck_relative, control=False, low_import=None):
        folder, source = base/relative, decks/deck_relative
        regenerate = not control or relative == 'control/low'
        pendf = folder/'pendf/tape30' if regenerate else Path(row['control_pendf'])
        def add(kind, inputs):
            result.append(dict(label=str((folder/kind).relative_to(work)), kind=kind,
                               control=control, deck=source/(kind+'.in'),
                               inputs=dict(inputs), output=folder/kind/'tape30'))
        if regenerate:
            add('pendf', [('tape20',endf)])
        add('groupr',[('tape20',endf),('tape29',pendf)])
        inputs = [('tape20',endf),('tape24',folder/'groupr/tape30')]
        if row['nsigz'] > 1:
            inputs.append(('tape22',pendf))
        if low_import is not None:
            inputs.append(('tape29',low_import))
        add('dragr',inputs)
    if row['route'] == 'ORIGINAL_LOW_THEN_HIGH_TWO_PASS':
        for group in ('control','expanded'):
            lane(group+'/low',group+'/low',control=group == 'control')
            lane(group+'/high',group+'/high',control=group == 'control',
                 low_import=base/group/'low/dragr/tape30')
    else:
        require(row['route'] == 'SINGLE_PASS', 'unknown route')
        if row['nsigz'] > 1:
            lane('control','control',control=True)
        lane('expanded','')
    require(len(result) == row['expected_native_stages'], 'stage coverage differs')
    return result


def validate_graph(rows,work):
    all_stages = [s for row in rows for s in stages(row,work)]
    outputs, labels, decks = set(), set(), set()
    for stage in all_stages:
        require(stage['label'] not in labels, 'duplicate stage')
        require(stage['deck'].is_file(), 'missing prepared deck')
        labels.add(stage['label']); decks.add(stage['deck'])
        for path in stage['inputs'].values():
            if path.is_relative_to(work):
                require(path in outputs, 'stage reads a future/missing output')
            else:
                require(path.is_file(), 'missing original input')
        outputs.add(stage['output'])
    require(len(outputs) == len(decks) == 138, 'stage/deck count')
    return all_stages


def dragr_limits(deck,raw,mat):
    """Reproduce dragr's existing energy-boundary indexing, not new tolerances."""
    lines = [line.strip() for line in deck.read_text().splitlines() if line.strip()]
    card = lines[lines.index('dragr')+1].rstrip('/').split()
    require(len(card) == 11 and int(card[7]) == 0, 'unsupported scattering lumping')
    matches = [i for i,line in enumerate(lines) if re.fullmatch(
        r'[+\-\d.Ee]+\s+[+\-\d.Ee]+\s*/',line) and 'E' in line.upper()]
    require(len(matches) == 1, 'ambiguous self-shielding energy card')
    i = matches[0]
    lo,hi = map(float,lines[i].rstrip('/').split())
    thermal = float(lines[i+1].rstrip('/').strip())
    _,grids = mt51.parse(raw,mat)
    energy = next(iter(grids.values()))['ascending_energy'][::-1]
    require(all(g['ascending_energy'][::-1] == energy for g in grids.values()), 'energy grid changed')
    ng, first,last = len(energy)-1,1,len(energy)-1
    lo = lo or energy[-1]
    hi = hi or energy[0]
    for ig in range(1,ng+1):
        if hi <= 1.001*energy[ig]:
            first = ig+1
    for ig in range(ng+1,1,-1):
        if lo >= .999*energy[ig-1]:
            last = ig-1
    thermal_groups = sum(thermal >= .999*energy[ig-1] for ig in range(ng,1,-1))
    require(1 <= first <= last <= ng, 'invalid self-shielding group interval')
    return (first,last),int(thermal_groups)


def replay_lane(row,work,group,lane=''):
    prefix = work/row['nuclide']/group/lane
    deck = PREP/row['nuclide']/((group+'/'+lane) if lane else ('control' if group == 'control' else ''))/'dragr.in'
    raw = (prefix/'groupr/tape30').read_bytes()
    lib = decode(prefix/'dragr/tape30',True)
    ss,thermal = dragr_limits(deck,raw,row['mat'])
    report = mt51.replay(raw,lib,row['nuclide'],row['mat'],ss,thermal)
    return raw,lib,report,ss


def low_records_preserved(low,high,name):
    selected = {k:v for k,v in low.items() if len(k) >= 3 and k[0] == name and
                str(k[1]).startswith('SUBTMP') and str(k[2]).startswith('SUBMAT')}
    require(selected, 'empty low-pass finite records')
    equal(selected,{k:high[k] for k in selected})
    return len(selected)


def finite_signs(name,records,expected_count,ss,expected_dilutions=None):
    """Weighted table observations, not a new normalized material state."""
    rows = []
    temps = records[(name,'TEMPERATURE')][1]
    for it,t in enumerate(temps,1):
        p = (name,f'SUBTMP{it:04d}')
        ds = np.asarray(records[p+('DILUTION',)][1],dtype='f4')
        require(len(ds) == expected_count and bool(np.all(np.diff(ds) > 0)), 'finite dilution coverage')
        if expected_dilutions is not None:
            require(ds.tobytes() == np.asarray(expected_dilutions,dtype='f4').tobytes(), 'finite dilution values')
        submat = {k[2] for k in records if len(k) >= 3 and k[:2] == p and str(k[2]).startswith('SUBMAT')}
        require(submat == {f'SUBMAT{j:04d}' for j in range(1,expected_count+1)}, 'finite subtree coverage')
        def matrix(prefix,order,finite=False):
            suffix = f'{order:02d}'
            data = lambda field: records[prefix+(field+suffix,)][1]
            return expand(data('NJJS'),data('IJJS'),data('SCAT'),370,ss if finite else None)[0]
        base = [matrix(p,order) for order in (0,1)]
        for iz,dilution in enumerate(ds,1):
            sub = p+(f'SUBMAT{iz:04d}',)
            full = [base[order]+matrix(sub,order,True) for order in (0,1)]
            require(all(np.isfinite(a).all() for a in full), 'nonfinite reconstructed matrix')
            require(not np.any(full[0] < 0), 'negative direct finite weighted P0')
            rows.append(dict(temperature_K=float(t),sigma0_b=float(dilution),
                             P0_minimum=float(full[0].min()),signed_P1_negative=int((full[1] < 0).sum())))
    return rows


def control_check(row,work):
    name = row['nuclide']
    require(row['nsigz'] > 1, 'single-dilution cases use the original control')
    fuel = row['route'] == 'ORIGINAL_LOW_THEN_HIGH_TWO_PASS'
    raw,lib,replayed,ss = replay_lane(row,work,'control','high' if fuel else '')
    old = decode(Path(row['original_library']),True)
    scope = mt51.gendf_scope((Path(row['original_library']).parent/('gendf_neutron_'+name)).read_bytes(),raw,row['mat'])
    non_scatter = mt51.non_scatter_records_exact(old,lib)
    result = dict(status='REPAIRED_FIVE_POINT_CONTROL_PASS',high_or_single_replay=replayed,
                  retained_high_GENDF_scope=scope,non_scatter_records_exact=non_scatter)
    if fuel:
        _,low,low_replay,_ = replay_lane(row,work,'control','low')
        result.update(low_replay=low_replay,low_records_retained=low_records_preserved(low,lib,name),
                      historical_low_GENDF_available=False,
                      limitation='Original low GENDF was not retained; low scatter is replayed from regenerated original-input control. Non-scatter records are compared to the full original 18-point library. This is not a byte comparison to a missing old low GENDF.')
    result['finite_weighted_tables'] = finite_signs(name,lib,row['expected_finite_dilutions'],ss,row.get('finite_dilutions_b'))
    return result


def expanded_check(row,work):
    name = row['nuclide']
    fuel = row['route'] == 'ORIGINAL_LOW_THEN_HIGH_TWO_PASS'
    base = work/name
    final = base/'expanded'/('high' if fuel else '')/'dragr/tape30'
    control = base/'control'/('high' if fuel else '')/'dragr/tape30' if row['nsigz'] > 1 else Path(row['original_library'])
    old,new = decode(control,True),decode(final,True)
    result = COMPARE(name,old,new,row['all_temperatures_K'])
    require(result['status'] == 'DIRECT_TEMPERATURE_REFERENCE_COMPLETE', 'new nodes or old controls refused: '+name)
    if row['nsigz'] > 1:
        _,_,report,ss = replay_lane(row,work,'expanded','high' if fuel else '')
        result['high_or_single_replay'] = report
        result['finite_weighted_tables'] = finite_signs(name,new,row['expected_finite_dilutions'],ss,row.get('finite_dilutions_b'))
        if fuel:
            _,low,report,_ = replay_lane(row,work,'expanded','low')
            result.update(low_replay=report,low_records_retained=low_records_preserved(low,new,name))
    return result

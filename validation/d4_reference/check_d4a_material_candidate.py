"""Read-only checks of the three actual-temperature material states.

No tolerance is fitted. P0 must be nonnegative; signed P1 is retained. The
known high-energy SIGS lifecycle is replayed, not overwritten or equated to a
scattering column sum. These are data checks, not a transport accuracy claim.
"""
import hashlib
import re

import numpy as np

import run_remaining_temperature_batch as c
from audit_fe56_candidate_scope import expand
from audit_fe56_temperature_interpolation import weights, mix_nodes

require = c.require
decode, nr, equal = (c.API[k] for k in ('decode', 'nr', 'equal_records'))
F = np.float32
TEMPERATURES = (650, 750, 850)


def exact(a, b):
    a, b = np.asarray(a, dtype=F), np.asarray(b, dtype=F)
    return a.shape == b.shape and a.tobytes() == b.tobytes()


def terminal(text, temperature):
    found = re.findall(r'CONVERGENCE REACHED AT TONE ITERATION\s*=\s*(\d+)\s+ERROR\s*=\s*([\d.E+\-]+)', text)
    require(len(found) == 1, 'one TONE terminal required')
    iteration, error = int(found[0][0]), float(found[0][1])
    require(1 <= iteration <= 20 and 0 <= error <= 1e-5, 'original TONE criterion not met')
    require('normal end of execution for dragon' in text.lower() and
            f'D4A-ACTUAL-MATERIAL{temperature}-COMPLETE' in text, 'material export did not finish')
    modules = re.findall(r'->@BEGIN MODULE\s*:\s*(\S+)', text)
    require(modules.count('TONE:') == modules.count('LIB:') == modules.count('SALT:') == 1,
            'wrong material module sequence')
    require(set(modules) <= {'LIB:', 'SALT:', 'TONE:', 'EQU:', 'UTL:', 'DELETE:', 'END:'},
            'unexpected native module')
    return dict(tone_iteration=iteration, tone_error=error, original_tone_epsilon=1e-5)


def fields(records, prefix):
    return {k[-1]: v[1] for k, v in records.items() if k[:-1] == prefix}


def matrix(row, order, groups=370):
    suffix = f'{order:02d}'
    keys = [n + suffix for n in ('NJJS', 'IJJS', 'SCAT', 'SIGS')]
    # LIBDEN skips an isotope/order when SIGS is absent. A wholly absent higher
    # moment therefore contributes zero, never the P0 matrix. Partial records
    # are corrupt and must not silently become a lower-order isotope.
    if order > 0 and not any(key in row for key in keys):
        require(all(n + '00' in row for n in ('NJJS', 'IJJS', 'SCAT')), 'missing P0 isotope')
        return np.zeros((groups, groups), dtype=F)
    require(all(n + suffix in row for n in ('NJJS', 'IJJS', 'SCAT')), 'partial scattering moment')
    a = nr.cpo_scatter(row, order, groups).astype(F)
    counts, tops, values = (row[n + suffix] for n in ('NJJS', 'IJJS', 'SCAT'))
    if len(values):
        b, omitted = expand(counts, tops, values, groups)
        require(omitted == 0 and exact(a, b), 'two scatter expanders disagree')
    else:
        require(sum(counts) == 0 and not np.any(a), 'invalid empty scattering moment')
    return a


def density_mix(values, densities, mixtures, nmix=6):
    values = np.asarray(values, dtype=F)
    require(len(values) == len(densities) == len(mixtures), 'density dimensions')
    out = np.zeros((nmix,) + values.shape[1:], dtype=F)
    for a, density, mix in zip(values, densities, mixtures):
        require(1 <= mix <= nmix and np.isfinite(density) and density >= 0, 'invalid material mixture')
        out[mix - 1] = np.add(out[mix - 1], np.multiply(a, density, dtype=F), dtype=F)
    return out


def nonnegative_p0(matrices, scope):
    for index, a in enumerate(matrices, 1):
        require(np.isfinite(a).all(), f'nonfinite {scope} P0 at index {index}')
        require(np.min(a) >= 0, f'negative {scope} P0 at index {index}: min={float(np.min(a))}, count={int(np.sum(a < 0))}')


def masked_scalar(initial, returned, densities, mixtures, first=25, last=281):
    """TONDRV/LIBDEN preserve initial scalar outside the update interval."""
    out = density_mix(initial, densities, mixtures)
    out[:, first - 1:last] = density_mix(returned, densities, mixtures)[:, first - 1:last]
    return out


def route_check(metadata, baseline, plan, plane):
    for key in ('ISOTOPESUSED', 'ISOTOPERNAME', 'ISOTOPESMIX', 'ISOTOPESDENS', 'ISOTOPESTEMP', 'ENERGY'):
        equal({(key,): metadata[(key,)]}, {(key,): baseline[(key,)]})
    for key in ('STATE-VECTOR', 'EPS-SHIBA', 'TCEPS-SHIBA'):
        path = ('SHIBA', key)
        equal({path: metadata[path]}, {path: baseline[path]})
    require(nr.data(metadata, ('SHIBA', 'STATE-VECTOR'))[:3] == (25, 281, 20), 'self-shielding update range changed')
    get = lambda key: nr.data(metadata, (key,))
    names = get('ILIBRARYNAME')
    libs = [names[i:i + 64].strip() for i in range(0, len(names), 64)]
    require(len(libs) == 2 and set(libs) == {'DLIB_ACTUAL', 'DLIB8R1_370'}, 'unexpected material libraries')
    indices = get('ILIBRARYINDX')
    refs = get('ISOTOPERNAME').ljust(59 * 12)
    refs = [refs[12 * i:12 * i + 12].strip() for i in range(59)]
    require(len(indices) == 59, 'library index count')
    routes = {}
    for row in plan['temperature_routes']:
        for place in row['locations']:
            if place['plane'] == plane:
                require(place['index'] not in routes, 'duplicate material location')
                routes[place['index']] = row
    require(set(routes) == set(range(1, 60)), 'incomplete material locations')
    for i, ref in enumerate(refs):
        row = routes[i + 1]
        require(ref == row['nuclide'] and exact(get('ISOTOPESTEMP')[i], row['temperature_K']), 'material temperature route differs')
        expected = 'DLIB8R1_370' if ref.startswith('Mo') else 'DLIB_ACTUAL'
        require(1 <= indices[i] <= 2 and libs[indices[i] - 1] == expected, 'material library route differs')
    require(sum(ref.startswith('Mo') for ref in refs) == 14, 'expected 14 original-Mo entries')
    return refs


def analyze(folder, plane, plan, references):
    require(1 <= plane <= 3, 'wrong plane')
    result = terminal((folder/'material.log').read_text(), TEMPERATURES[plane - 1])
    full, meta, macro_records = (decode(folder/name) for name in ('microlib.ascii', 'metadata.ascii', 'macro.ascii'))
    for kind, value in full.values():
        if kind in (1, 2, 4):
            require(np.isfinite(value).all(), 'nonfinite material record')
    require(nr.data(full, ('ISOTOPESLIST',), 10) == 59, '59 complete microscopic entries required')
    equal({k: v for k, v in full.items() if k[0] not in ('ISOTOPESLIST', 'MACROLIB')}, meta)
    equal({k[1:]: v for k, v in full.items() if k[0] == 'MACROLIB' and len(k) > 1}, macro_records)
    get = lambda key: nr.data(meta, (key,))
    energy = np.asarray(get('ENERGY'), dtype='<f4')
    require(hashlib.sha256(energy.tobytes()).hexdigest() == plan['energy_float32_sha256'], 'energy grid differs')
    baseline = decode(c.batch.ART/'d4a-fe56-library-path-audit-20260929'/f'meta{plane}.ascii')
    refs = route_check(meta, baseline, plan, plane)
    densities, mixtures, temperatures = get('ISOTOPESDENS'), get('ISOTOPESMIX'), get('ISOTOPESTEMP')
    dsn = np.asarray(get('ISOTOPESDSN'), dtype=F).reshape(59, 370)
    require(np.all(dsn[:, :24] >= F(1e10)), 'unexpected high-energy shielding')
    micros = [fields(full, ('ISOTOPESLIST', i)) for i in range(1, 60)]
    mats = [[matrix(row, order) for row in micros] for order in (0, 1)]
    nonnegative_p0(mats[0], 'microscopic')
    totals = np.asarray([row['NTOT0'] for row in micros], dtype=F)
    require(totals.shape == (59, 370) and np.min(totals) >= 0, 'invalid microscopic total')
    returned = np.asarray([row['SIGS00'] for row in micros], dtype=F)
    initial = np.zeros_like(returned)
    rows = []
    for ref in sorted(set(refs)):
        source = decode(references[ref], True)
        require(exact(nr.data(source, ('ENERGY',)), energy), 'reference energy differs')
        table = nr.data(source, (ref, 'TEMPERATURE'))
        node_fields = [fields(source, (ref, f'SUBTMP{j:04d}')) for j in range(1, len(table) + 1)]
        nodes = [[matrix(row, order) for row in node_fields] for order in (0, 1)]
        scalars, capped = [], []
        for j, row in enumerate(node_fields, 1):
            scalar = np.asarray(row.get('SIGS00', np.add.accumulate(nodes[0][j - 1].astype('f8'), axis=0)[-1]), dtype=F)
            prefix = (ref, f'SUBTMP{j:04d}')
            subkeys = [k[-1] for k in source if k[:2] == prefix and len(k) == 4 and k[2].startswith('SUBMAT')]
            branch = 'SCAT00' in subkeys and 'SIGS00' not in subkeys
            scalars.append(scalar)
            capped.append(np.minimum(scalar, np.asarray(row['NTOT0'], dtype=F)) if branch else scalar)
        for i in [i for i, name in enumerate(refs) if name == ref]:
            w = weights(table, temperatures[i], 3)
            if not ref.startswith('Mo'):
                require(np.count_nonzero(w) == 1 and np.max(w) == 1 and
                        any(exact(t, temperatures[i]) for t in table), 'candidate not at exact temperature node')
            for order in (0, 1):
                replay = mix_nodes(nodes[order], w)
                require(exact(replay[:, 281:], mats[order][i][:, 281:]), 'thermal moment replay differs')
            initial[i] = mix_nodes(scalars, w)
            high = mix_nodes(capped if np.any(dsn[i] < F(1e10)) else scalars, w)
            require(exact(high[:24], returned[i, :24]), 'high-energy scalar lifecycle differs')
            rows.append(dict(index=i + 1, nuclide=ref, temperature_K=float(F(temperatures[i])),
                direct_node=not ref.startswith('Mo'), thermal_P0_P1_exact=True,
                high_energy_scalar_replay_exact=True, P0_negative_entries=0,
                signed_P1_negative_entries=int(np.sum(mats[1][i] < 0))))
    parsed = nr.macro((folder/'macro.ascii').read_bytes(), 370, 6)
    macro_rows = []
    for order in (0, 1):
        saved = nr.scatter(parsed, order).astype(F)
        require(exact(density_mix(mats[order], densities, mixtures), saved), 'macro density/matrix replay differs')
        if order == 0:
            nonnegative_p0(saved, 'macroscopic')
        scalar = nr.field(parsed, f'SIGS{order:02d}').astype(F)
        if order == 0:
            require(exact(masked_scalar(initial, returned, densities, mixtures), scalar), 'macro scalar lifecycle differs')
        macro_rows.append(dict(order=order, density_matrix_replay_exact=True,
            negative_entries=int(np.sum(saved < 0)),
            max_abs_column_sum_minus_scalar=float(np.max(abs(saved.astype('f8').sum(axis=1) - scalar))),
            column_sum_gap_status='DIAGNOSTIC_ONLY_NOT_A_NEW_TOLERANCE'))
    return dict(status='THREE_PLANE_MEMBER_MATERIAL_DATA_CHECKED', plane=plane, temperature_C=TEMPERATURES[plane - 1],
        **result, microscopic_entries=59, mixtures=6, full_microlib_records=len(full),
        microscopic=sorted(rows, key=lambda r: r['index']), macroscopic=macro_rows,
        production_accepted=False, transport_solves=0,
        limits=['Data checks only; not k/flux, angular positivity, mesh/rank or whole-core acceptance.',
                'Original Mo interpolation is unchanged. Its separately pinned historical ASCII is used for replay, not substituted into the runtime library.',
                'The existing finite-dilution scalar MIN and macro update interval are reproduced, not promoted to a universal physical rule.',
                'P0 column sums need not equal totals when neutron-producing reactions contribute.'])

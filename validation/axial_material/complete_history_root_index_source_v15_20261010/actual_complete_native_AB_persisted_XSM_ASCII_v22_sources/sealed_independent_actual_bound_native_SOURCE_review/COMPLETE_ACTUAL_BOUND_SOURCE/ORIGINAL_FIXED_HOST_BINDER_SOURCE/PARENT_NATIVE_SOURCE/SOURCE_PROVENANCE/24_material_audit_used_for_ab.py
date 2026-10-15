"""Read saved pin material records; never run a native engine.

The native ASCII format is decoded by two established independent parsers.
This is a material-data qualification, not a transport accuracy certificate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'validation/d4_reference'))
import check_d4a_material_candidate as core

F = np.float32
require = core.require
DEFAULT_REFERENCES = ROOT / 'validation/artifacts/d4a-actual-temperature-material-runtime-20261003/references.json'
BASELINE = ROOT / 'validation/artifacts/d4a-fe56-library-path-audit-20260929/meta2.ascii'
LIBIPS = Path('/Users/wen/dragon-5.1/Dragon/src/LIBIPS.f')
LIFECYCLE = [LIBIPS.parent / name for name in ('TONDRV.f', 'TONSPH.f', 'TONCMI.f', 'LIBDEN.f', 'LIBDRB.f')]
FUEL = {'U235', 'U238', 'Pu238', 'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Am241', 'O16'}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fuel_densities(pu, uranium):
    """Independent REAL32 arithmetic reconstruction of corrected density law.

    Operation ordering follows CLE arithmetic semantics, including the
    right-associated isotope mass sum. No saved density is used in this law.
    """
    add = lambda a, b: F(F(a) + F(b))
    sub = lambda a, b: F(F(a) - F(b))
    mul = lambda a, b: F(F(a) * F(b))
    div = lambda a, b: F(F(a) / F(b))
    fractions = [.0259, .552, .2585, .0727, .0787, .0122]
    masses = [238.0495534, 239.0521565, 240.0538075, 241.0568453, 242.0587368, 241.0568229]
    terms = [mul(f, m) for f, m in zip(fractions, masses)]
    mpu = terms[-1]
    for term in reversed(terms[:-1]):
        mpu = add(term, mpu)
    mu = add(mul(.002, 235.0439231), mul(.998, 238.0507826))
    slope = div(sub(1.0888e-5, 1.0803e-5), 100)
    intercept = div(sub(mul(800, 1.0803e-5), mul(700, 1.0888e-5)), 100)
    expansion = add(mul(slope, 750), intercept)
    linear = add(mul(sub(750, 20), expansion), 1)
    volume = mul(mul(linear, linear), linear)
    rho = div(mul(11.46, .955), volume)
    oxygen = add(1, mul(mul(1.98, 15.9949), add(div(uranium, mu), div(pu, mpu))))
    hm = div(rho, oxygen)
    npu = div(mul(mul(hm, pu), .6022094), mpu)
    nu = div(mul(mul(hm, uranium), .6022094), mu)
    result = dict(zip(('Pu238', 'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Am241'),
                      [mul(f, npu) for f in fractions]))
    result.update(U235=mul(.002, nu), U238=mul(.998, nu), O16=add(mul(1.98, nu), mul(1.98, npu)))
    return result


def names(record, count, width=12):
    require(len(record) <= count * width, 'overlong isotope name record')
    record = record.ljust(count * width)
    values = [record[i * width:(i + 1) * width].strip() for i in range(count)]
    require(all(values), 'blank isotope identity')
    return values


def resolve_isotope_rows(rows, aliases, refs, temperatures):
    """Replay LIBIPS: an empty item may alias an earlier complete isotope.

    Full ISOTOPESUSED aliases are compared, including their four mixture-name
    characters. This is required for COMB-copied nonshielded oxygen records.
    """
    require(len(rows) == len(aliases) == len(refs) == len(temperatures), 'isotope pointer dimensions')
    resolved, indices = [], []
    for i, row in enumerate(rows):
        if row:
            resolved.append(row)
            indices.append(i + 1)
            continue
        matches = [j for j in range(i) if aliases[j] == aliases[i]]
        require(bool(matches), f'unresolved native isotope alias at {i + 1}')
        j = matches[0]
        require(refs[j] == refs[i] and core.exact(temperatures[j], temperatures[i]), 'alias identity/temperature differs')
        resolved.append(resolved[j])
        indices.append(indices[j])
    return resolved, indices


def metadata_check(meta, baseline, state):
    require(state in ('A', 'B'), 'unknown material state')
    get = lambda key: core.nr.data(meta, (key,))
    vector = get('STATE-VECTOR')
    require(vector[:5] == (8, 62, 370, 3, 1), 'wrong material dimensions/anisotropy/transport correction')
    refs = names(get('ISOTOPERNAME'), 62)
    mixtures, densities, temperatures = (get(k) for k in ('ISOTOPESMIX', 'ISOTOPESDENS', 'ISOTOPESTEMP'))
    require(len(mixtures) == len(densities) == len(temperatures) == 62, 'material metadata dimensions')
    by_mix = {m: [r for r, mix in zip(refs, mixtures) if mix == m] for m in range(1, 9)}
    require(by_mix[1] == ['Na23'] and by_mix[3] == by_mix[8] == ['He4'], 'nonfuel region order')
    require(len(by_mix[2]) == 23 and len(set(by_mix[2])) == 23, 'clad inventory')
    require(all(len(by_mix[m]) == 9 and set(by_mix[m]) == FUEL for m in (4, 5, 6, 7)), 'four fuel rings')
    require(len(set(refs)) == 34 and sum(r.startswith('Mo') for r in refs) == 7, 'pin isotope inventory')
    base_refs = names(core.nr.data(baseline, ('ISOTOPERNAME',)), 59)
    base_mix = core.nr.data(baseline, ('ISOTOPESMIX',))
    base_dens = core.nr.data(baseline, ('ISOTOPESDENS',))
    base_temp = core.nr.data(baseline, ('ISOTOPESTEMP',))
    base = {(m, r): (d, t) for r, m, d, t in zip(base_refs, base_mix, base_dens, base_temp)}
    expected = fuel_densities(.21, .79) if state == 'A' else fuel_densities(.2436, .7564)
    libraries = names(get('ILIBRARYNAME'), 2, 64)
    require(set(libraries) == {'DLIB_ACTUAL', 'DLIB8R1_370'}, 'unexpected library set')
    indices = get('ILIBRARYINDX')
    require(len(indices) == 62, 'library index count')
    for i, (ref, mix, density, temperature) in enumerate(zip(refs, mixtures, densities, temperatures)):
        baseline_mix = 4 if mix in (4, 5, 6, 7) else 5 if mix == 8 else mix
        old_density, old_temperature = base[(baseline_mix, ref)]
        require(core.exact(temperature, old_temperature), 'temperature differs from corrected physical state')
        expected_density = expected[ref] if mix in (4, 5, 6, 7) else old_density
        require(core.exact(density, expected_density), f'density law differs: {state} mixture {mix} {ref}')
        if state == 'A':
            require(core.exact(density, old_density), 'A differs from corrected original density')
        require(1 <= indices[i] <= 2, 'invalid library index')
        route = 'DLIB8R1_370' if ref.startswith('Mo') else 'DLIB_ACTUAL'
        require(libraries[indices[i] - 1] == route, 'candidate/original Mo boundary changed')
    for key in ('STATE-VECTOR', 'EPS-SHIBA', 'TCEPS-SHIBA'):
        path = ('SHIBA', key)
        core.equal({path: meta[path]}, {path: baseline[path]})
    require(core.nr.data(meta, ('SHIBA', 'STATE-VECTOR'))[:3] == (25, 281, 20), 'TONE update interval')
    core.equal({('ENERGY',): meta[('ENERGY',)]}, {('ENERGY',): baseline[('ENERGY',)]})
    return refs, mixtures, densities, temperatures


def terminal(text, state, stage='MATERIAL'):
    require(state in ('A', 'B') and stage in ('MATERIAL', 'SNAPSHOT'), 'invalid log scope')
    marker = f'AXMAT-{stage}-{state}-COMPLETE'
    marker_suffix = r'\s+([\d.Ee+\-]+)' if stage == 'SNAPSHOT' else ''
    marker_matches = re.findall(r'^>\|' + marker + marker_suffix + r'\s*\|>\d+\s*$', text, re.M)
    require(len(marker_matches) == 1,
            'one executed completion marker required; deck echo is insufficient')
    require(text.lower().count('normal end of execution for dragon') == 1, 'normal native termination absent/duplicated')
    modules = re.findall(r'->@BEGIN MODULE\s*:\s*(\S+)', text)
    if stage == 'MATERIAL':
        found = re.findall(r'CONVERGENCE REACHED AT TONE ITERATION\s*=\s*(\d+)\s+ERROR\s*=\s*([\d.E+\-]+)', text)
        require(len(found) == 1, 'one actual TONE convergence report required')
        iteration, error = int(found[0][0]), float(found[0][1])
        require(1 <= iteration <= 20 and np.isfinite(error) and error >= 0, 'invalid TONE terminal')
        require('MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED' not in text, 'TONE iteration limit reached')
        # TONDRV's NOCONV is sticky: once false, later YMAX cannot reactivate
        # it. The printed ZZMAX includes all mixtures, while ICOUNT controls
        # stopping. Thus printed ERROR can exceed EPS after native convergence.
        require(re.search(r'^\s*EPS\s+1\.0E-05\s+\(STOPING CRITERION\)', text, re.M), 'wrong native TONE EPS')
        require(all(modules.count(m) == 1 for m in ('TONE:', 'LIB:', 'SALT:')), 'material module count')
        require(modules.count('GREP:') == 3, 'three native material dimension assertions required')
        require(set(modules) <= {'LIB:', 'SALT:', 'TONE:', 'EQU:', 'UTL:', 'GREP:', 'DELETE:', 'END:'}, 'unexpected material native module')
        return dict(tone_iteration=iteration, tone_printed_error=error, tone_epsilon=1e-5,
                    native_masked_convergence=True, printed_global_error_within_epsilon=error <= 1e-5,
                    convergence_semantics='TONDRV sticky NOCONV/ICOUNT termination; printed ZZMAX is not the remaining-mask stop predicate.')
    require(all(modules.count(m) == 1 for m in ('SALT:', 'MCCG:', 'ASM:', 'FLU:')), 'snapshot native module count')
    require(modules.count('BACKUP:') == 4, 'four separate archive objects required')
    require('TONE:' not in modules and 'LIB:' not in modules, 'snapshot rebuilt material')
    k = float(marker_matches[0])
    require(np.isfinite(k) and k > 0, 'invalid printed snapshot k')
    return dict(status='NORMAL_COMPLETED_SNAPSHOT_LOG_ONLY', printed_keff=k,
                archive_dimensions='REQUIRE_INDEPENDENT_ARCHIVE_READER; log/deck text is not a dimension proof')


def analyze(folder, state, references_path=DEFAULT_REFERENCES):
    folder = Path(folder)
    evidence = [folder / n for n in ('material.log', 'microlib.ascii', 'metadata.ascii', 'macro.ascii', 'material.xsm')]
    evidence += [BASELINE, references_path, Path(__file__), Path(core.__file__), LIBIPS] + LIFECYCLE
    protected = {str(p.resolve()): sha(p) for p in evidence}
    result = terminal((folder / 'material.log').read_text(), state)
    full, meta, macro = (core.decode(folder / n) for n in ('microlib.ascii', 'metadata.ascii', 'macro.ascii'))
    for kind, value in full.values():
        if kind in (1, 2, 4):
            require(np.isfinite(value).all(), 'nonfinite native material record')
    require(core.nr.data(full, ('ISOTOPESLIST',), 10) == 62, '62 microscopic entries required')
    core.equal({k: v for k, v in full.items() if k[0] not in ('ISOTOPESLIST', 'MACROLIB')}, meta)
    core.equal({k[1:]: v for k, v in full.items() if k[0] == 'MACROLIB' and len(k) > 1}, macro)
    require(core.nr.data(macro, ('STATE-VECTOR',))[:4] == (370, 8, 3, 32), 'macro group/mixture/moment/fission dimensions')
    refs, mixtures, densities, temperatures = metadata_check(meta, core.decode(BASELINE), state)
    references = json.loads(Path(references_path).read_text())
    dsn = np.asarray(core.nr.data(meta, ('ISOTOPESDSN',)), dtype=F).reshape(62, 370)
    require(np.all(dsn[:, :24] >= F(1e10)), 'unexpected high-energy shielding')
    rows = [core.fields(full, ('ISOTOPESLIST', i)) for i in range(1, 63)]
    rows, record_indices = resolve_isotope_rows(rows, names(core.nr.data(meta, ('ISOTOPESUSED',)), 62), refs, temperatures)
    mats = [[core.matrix(row, order) for row in rows] for order in (0, 1)]
    core.nonnegative_p0(mats[0], 'microscopic')
    totals = np.asarray([row['NTOT0'] for row in rows], dtype=F)
    require(totals.shape == (62, 370) and np.min(totals) >= 0, 'invalid microscopic total')
    returned = np.asarray([row['SIGS00'] for row in rows], dtype=F)
    initial = np.zeros_like(returned)
    energy = core.nr.data(meta, ('ENERGY',))
    checks = []
    sph_records = [str(k) for k in full if any(isinstance(part, str) and 'SPH' in part for part in k)]
    require(not sph_records, 'new saved SPH evidence exists: extend independent factor replay before proceeding')
    for ref in sorted(set(refs)):
        path = Path(references[ref])
        evidence.append(path)
        protected[str(path.resolve())] = sha(path)
        source = core.decode(path, True)
        require(core.exact(core.nr.data(source, ('ENERGY',)), energy), 'reference energy differs')
        table = core.nr.data(source, (ref, 'TEMPERATURE'))
        node_fields = [core.fields(source, (ref, f'SUBTMP{j:04d}')) for j in range(1, len(table) + 1)]
        nodes = [[core.matrix(row, order) for row in node_fields] for order in (0, 1)]
        scalars, capped = [], []
        for j, row in enumerate(node_fields, 1):
            scalar = np.asarray(row.get('SIGS00', np.add.accumulate(nodes[0][j - 1].astype('f8'), axis=0)[-1]), dtype=F)
            prefix = (ref, f'SUBTMP{j:04d}')
            subkeys = [k[-1] for k in source if k[:2] == prefix and len(k) == 4 and k[2].startswith('SUBMAT')]
            branch = 'SCAT00' in subkeys and 'SIGS00' not in subkeys
            scalars.append(scalar)
            capped.append(np.minimum(scalar, np.asarray(row['NTOT0'], dtype=F)) if branch else scalar)
        for i in [i for i, name in enumerate(refs) if name == ref]:
            w = core.weights(table, temperatures[i], 3)
            if not ref.startswith('Mo'):
                require(np.count_nonzero(w) == 1 and np.max(w) == 1 and any(core.exact(t, temperatures[i]) for t in table), 'not an actual-temperature node')
            boundary = []
            for order in (0, 1):
                replay_full = core.mix_nodes(nodes[order], w)
                # TONCMI P0 uses the incoming-group SPH; P1 uses the outgoing
                # group. The thermal-to-resonance P1 band is therefore not an
                # invariant of four-ring TONE/SPH, unlike the old D4 one-ring
                # state. No tolerance is added to make that band match.
                replay = replay_full[:, 281:] if order == 0 else replay_full[281:, 281:]
                actual = mats[order][i][:, 281:] if order == 0 else mats[order][i][281:, 281:]
                require(core.exact(replay, actual),
                        f'thermal moment replay differs: index={i + 1} nuclide={ref} order={order} '
                        f'count={int(np.sum(replay != actual))} max_abs={float(np.max(abs(replay.astype("f8") - actual)))}')
                if order == 1:
                    reference_band, actual_band = replay_full[:281, 281:], mats[order][i][:281, 281:]
                    for target, source_group in np.argwhere(reference_band != actual_band):
                        old = F(reference_band[target, source_group])
                        new = F(actual_band[target, source_group])
                        oldbits, newbits = int(old.view(np.uint32)), int(new.view(np.uint32))
                        require(target >= 24, 'unexpected P1 change outside resonant outgoing band')
                        boundary.append(dict(to_group=int(target + 1), from_group=int(source_group + 282),
                            reference_float32=float(old), returned_float32=float(new),
                            reference_bits=f'{oldbits:08x}', returned_bits=f'{newbits:08x}',
                            ulp_distance_same_sign=abs(oldbits - newbits) if np.signbit(old) == np.signbit(new) else None,
                            status='TONCMI_OUTGOING_SPH_BAND_NOT_INDEPENDENT_FACTOR_REPLAYED'))
            initial[i] = core.mix_nodes(scalars, w)
            high = core.mix_nodes(capped if np.any(dsn[i] < F(1e10)) else scalars, w)
            require(core.exact(high[:24], returned[i, :24]), 'high-energy scalar lifecycle differs')
            checks.append(dict(index=i + 1, native_record_index=record_indices[i], mixture=mixtures[i], nuclide=ref, temperature_K=float(F(temperatures[i])),
                density=float(F(densities[i])), exact_temperature_node=not ref.startswith('Mo'),
                thermal_P0_incoming_columns_282_370_exact=True,
                thermal_P1_thermal_to_thermal_block_282_370_exact=True,
                thermal_P1_into_resonance_changes=boundary,
                high_energy_scalar_replay_exact=True,
                P0_negative_entries=0, signed_P1_negative_entries=int(np.sum(mats[1][i] < 0))))
    parsed = core.nr.macro((folder / 'macro.ascii').read_bytes(), 370, 8)
    macro_checks = []
    for order in (0, 1):
        saved = core.nr.scatter(parsed, order).astype(F)
        require(core.exact(core.density_mix(mats[order], densities, mixtures, 8), saved), 'macro density/matrix replay differs')
        if order == 0:
            core.nonnegative_p0(saved, 'macroscopic')
        scalar = core.nr.field(parsed, f'SIGS{order:02d}').astype(F)
        if order == 0:
            replay = core.density_mix(initial, densities, mixtures, 8)
            replay[:, 24:281] = core.density_mix(returned, densities, mixtures, 8)[:, 24:281]
            require(core.exact(replay, scalar), 'macro scalar lifecycle differs')
        macro_checks.append(dict(order=order, density_matrix_replay_exact=True, negative_entries=int(np.sum(saved < 0)),
            max_abs_column_sum_minus_scalar=float(np.max(abs(saved.astype('f8').sum(axis=1) - scalar))),
            column_sum_gap_status='DIAGNOSTIC_ONLY_NOT_A_NEW_TOLERANCE'))
    for path, digest in protected.items():
        require(sha(path) == digest, f'evidence changed during read-only audit: {path}')
    return dict(status='PIN_MATERIAL_DATA_CHECKED_WITH_DECLARED_SPH_REPLAY_LIMIT', state=state, **result, microscopic_entries=62, mixtures=8,
                fission_components=32, distinct_native_microscopic_records=len(set(record_indices)),
                microscopic=sorted(checks, key=lambda row: row['index']), macroscopic=macro_checks,
                source_sha256=protected, native_engines_started=0,
                production_accuracy_accepted=False, limits=['Material records only; no transport accuracy claim.',
                'P1 signs and original Mo interpolation retained.', 'Column-sum diagnostics do not change physical gates.',
                'No SPH factor record is saved. Thermal-incoming to resonant-outgoing P1 changes have finite/signed and full macro-density checks, plus source lifecycle justification, but no independent SPH factor replay.',
                'The TONE native masked convergence gate is preserved; printed global error is reported separately and may exceed EPS.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('state', choices=['A', 'B'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'refuse overwrite of existing audit')
    result = analyze(args.folder, args.state)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(result['status'], args.state, flush=True)


if __name__ == '__main__':
    main()

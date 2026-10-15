#!/usr/bin/env python3
"""Verify composition evidence, replay, preserved failures and raw ledgers."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from native_segment_composition import read_native, exact_coefficients, input_patterns, preservation, scaled_error
from qualify_native_directional import load_native


def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()


def load(path):
    with np.load(path) as f: return {k: f[k] for k in f.files}


def main(root, a):
    counts = dict(protected_files=0, initial_inputs=0, copied_inputs=0, prior_artifacts=0,
        prior_manifest_entries=0, byte_identical_analysis_files=0, checked_numeric_arrays=0,
        original_native_segments=0, unique_native_records=0, prior_partial_arrays_recovered=0)
    for name, base, key in [('protected_inputs_before.json', root, 'protected_files'),
                           ('initial_inputs.json', root, 'initial_inputs'), ('copied_inputs.json', a, 'copied_inputs')]:
        for path, expected in json.loads((a/name).read_text()).items():
            assert digest(base/path) == expected, path; counts[key] += 1
    for name, expected in json.loads((a/'prior_artifacts.json').read_text()).items():
        folder = root/'validation/artifacts'/name; assert digest(folder/'result.sha256') == expected, name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected, path = line.split(maxsplit=1); assert digest(folder/path) == expected, (name, path)
            counts['prior_manifest_entries'] += 1
        counts['prior_artifacts'] += 1
    for name in ['native_segment_composition.py', 'qualify_native_segment_composition.py', 'test_native_segment_composition.py',
                 'verify_native_segment_composition.py', 'probe_native_segment_composition.f90',
                 'axial_cell_characteristic.py', 'qualify_native_directional.py', 'summarize_native_segment_composition.py']:
        assert digest(a/'build'/name) == digest(root/'validation/iterative'/name), name
    for folder in [a/'runs', a/'replay/runs']:
        for name in ['source_tests.log', 'archived_tests.log'] if folder == a/'runs' else ['archived_tests.log']:
            text = (folder/name).read_text(); assert 'Ran 10 tests' in text and '\nOK\n' in text and 'skipped=' not in text
    primary_files = sorted(p.relative_to(a/'analysis') for p in (a/'analysis').rglob('*') if p.is_file())
    replay_files = sorted(p.relative_to(a/'replay/analysis') for p in (a/'replay/analysis').rglob('*') if p.is_file())
    assert primary_files == replay_files
    for name in primary_files:
        assert digest(a/'analysis'/name) == digest(a/'replay/analysis'/name), str(name)
        counts['byte_identical_analysis_files'] += 1
    plan = json.loads((a/'plan.json').read_text()); lim = plan['limits']; fractions = plan['coefficient_fractions']
    fixture = load_native(a/'inputs/track_data.bin'); mapping = load(a/'inputs/segment_map.npz')
    mask = (fixture['region'] > 0) & (np.arange(fixture['nmax'])[None, :] < fixture['length'][:, None]-1)
    lines, steps = np.nonzero(mask)
    np.testing.assert_array_equal(mapping['line'], lines); np.testing.assert_array_equal(mapping['step'], steps)
    for key, expected in [('track', fixture['track'][lines]), ('polar', fixture['polar'][lines]),
        ('region', fixture['region'][mask]-1), ('weights', fixture['weight'][lines]),
        ('zmu', fixture['zmu']), ('mu', np.sqrt(1-1/fixture['zmu']**2))]:
        np.testing.assert_array_equal(mapping[key], expected)
    for g in fixture['group_data']:
        records = load(a/f"inputs/group{g['group']}.npz")
        expanded = records['unique'][records['inverse']]
        expected = np.column_stack([g['total'][mapping['region']], fixture['h'][mask], g['b'][mask], g['self_d'][mask]])
        np.testing.assert_array_equal(expanded, expected)
        assert np.all(np.bincount(records['inverse']) > 0)
    del fixture, mapping, records, expanded, expected
    resources = {}; fixture_results = []
    for label in ['controls', 'group51', 'group61', 'group98']:
        assert digest(a/f'runs/{label}.native') == digest(a/f'replay/runs/{label}.native'), label
        if label == 'controls':
            with (a/'inputs/controls.request').open('rb') as f:
                np.fromfile(f, '<i4', 2); unique = np.fromfile(f, '<f8').reshape(-1, 2)
            multiplicity = np.ones(len(unique), dtype=int)
        else:
            original = load(a/f'inputs/{label}.npz'); unique = original['unique']; multiplicity = np.bincount(original['inverse'])
            counts['original_native_segments'] += len(original['inverse']); counts['unique_native_records'] += len(unique)
            assert len(original['inverse']) == 439344 and len(unique) == 244233
        native = read_native(a/f'runs/{label}.native')
        coeff = load(a/f'analysis/{label}/coefficients.npz')
        np.testing.assert_array_equal(coeff['native'], native)
        np.testing.assert_array_equal(coeff['multiplicity'], multiplicity)
        np.testing.assert_array_equal(coeff['native_minus_exact'], native-coeff['exact'])
        for start in range(0, len(unique), plan['chunk_records']):
            sl = slice(start, min(start+plan['chunk_records'], len(unique)))
            np.testing.assert_array_equal(coeff['exact'][sl], exact_coefficients(unique[sl, 1, None]*fractions, unique[sl, 0, None]))
        summary = json.loads((a/f'analysis/{label}/result.json').read_text())
        if label != 'controls':
            np.testing.assert_array_equal(native[:, 0, 1:], unique[:, 2:])
            assert summary['native_calibration_bitwise_equal'] and summary['native_calibration_passed']
            fixture_results.append(summary)
        else: assert summary['native_void_supported'] == bool(np.array_equal(native[0], coeff['exact'][0]))
        assert min(summary['native_minimum_coefficients']) >= 0 and min(summary['exact_minimum_coefficients']) >= 0
        for row in summary['partitions']:
            part = row['partition']; parts = plan['partitions'][part]; index = [fractions.index(p) for p in parts]
            boundary, source = input_patterns(len(parts)); accumulated = {}
            for kind in ['exact', 'native']:
                accumulated[kind] = dict(maximum=np.zeros(4), failed_unique=0, failed_original=0, global_balance=0., local_balance=0., min_angle=1., min_integral=1.)
            matrix_max = 0.; covered = 0
            for start in range(0, len(unique), plan['chunk_records']):
                f = load(a/f'analysis/{label}/{part}_{start:06d}.npz'); n = len(f['record_indices']); sl = slice(start, start+n)
                np.testing.assert_array_equal(f['record_indices'], np.arange(start, start+n))
                np.testing.assert_array_equal(f['lengths'], unique[sl, 1, None]*parts)
                np.testing.assert_array_equal(f['totals'], unique[sl, 0]); np.testing.assert_array_equal(f['multiplicity'], multiplicity[sl])
                np.testing.assert_array_equal(f['boundary'], boundary); np.testing.assert_array_equal(f['source'], source)
                for k, v in f.items(): assert np.isfinite(v).all(), (label, part, start, k)
                counts['checked_numeric_arrays'] += len(f); covered += n
                supplied = boundary[None, :]+f['lengths']@source
                for kind in ['exact', 'native']:
                    np.testing.assert_array_equal(f[kind+'_kernel'], coeff[kind][sl][:, index])
                    stat = accumulated[kind]
                    for direction in ['forward', 'reverse']:
                        prefix = kind+'_'+direction+'_'
                        fields = {k[len(prefix):]: v for k, v in f.items() if k.startswith(prefix)}
                        birth = np.zeros_like(fields['outgoing'])
                        for i in range(len(parts)) if direction == 'forward' else range(len(parts)-1, -1, -1):
                            birth += f['lengths'][:, i, None]*source[i][None, :]
                        supplied = boundary[None, :]+birth
                        error = preservation(fields, coeff[kind][sl, 0], unique[sl, 1])
                        np.testing.assert_array_equal(error, fields['preservation_relative'])
                        # Independently combine endpoint escape, material collision
                        # and prescribed birth; summation order differs from the sweep.
                        raw = fields['outgoing']-boundary+f['totals'][:, None]*fields['integral']-f['lengths']@source
                        assert np.max(scaled_error(raw-fields['global_defect'], supplied)) < lim['direct_matrix_relative']
                        np.testing.assert_array_equal(fields['global_balance_relative'], scaled_error(fields['global_defect'], supplied))
                        np.testing.assert_array_equal(fields['matrix_outgoing_relative'], scaled_error(fields['outgoing']-fields['matrix_outgoing'], supplied))
                        np.testing.assert_array_equal(fields['matrix_integral_relative'], scaled_error(fields['integral']-fields['matrix_integral'], f['lengths'].sum(axis=1)[:, None]*supplied))
                        failed = np.max(error, axis=1) >= lim[kind+'_partition_relative']
                        stat['maximum'] = np.maximum(stat['maximum'], error.max(axis=0))
                        stat['failed_unique'] += int(failed.sum()); stat['failed_original'] += int(np.dot(failed.astype(int), multiplicity[sl]))
                        stat['global_balance'] = max(stat['global_balance'], float(fields['global_balance_relative'].max()))
                        stat['local_balance'] = max(stat['local_balance'], float(fields['maximum_local_balance_relative'].max()))
                        stat['min_angle'] = min(stat['min_angle'], float(fields['minimum_angle'].min()))
                        stat['min_integral'] = min(stat['min_integral'], float(fields['minimum_integral'].min()))
                        matrix_max = max(matrix_max, float(fields['matrix_outgoing_relative'].max()), float(fields['matrix_integral_relative'].max()))
            assert covered == len(unique)
            for kind, stat in accumulated.items():
                np.testing.assert_array_equal(stat['maximum'], row[kind+'_preservation_maximum_relative'])
                for source_key, target_key in [('failed_unique', 'failing_unique_orders'), ('failed_original', 'failing_original_orders'),
                    ('global_balance', 'maximum_global_balance_relative'), ('local_balance', 'maximum_local_balance_relative'),
                    ('min_angle', 'minimum_angle'), ('min_integral', 'minimum_integral')]:
                    assert stat[source_key] == row[kind+'_'+target_key]
                assert row[kind+'_partition_passed'] == (stat['failed_unique'] == 0)
            assert matrix_max == row['maximum_direct_matrix_relative']
            assert row['direct_matrix_passed'] == (matrix_max < lim['direct_matrix_relative'])
            assert row['exact_balance_passed'] == (row['exact_maximum_global_balance_relative'] < lim['exact_raw_balance_relative'])
            assert row['native_balance_context_passed'] == (row['native_maximum_global_balance_relative'] < lim['native_balance_context_relative'])
            assert row['positive_responses_passed'] == (min(row[k] for k in ['native_minimum_angle', 'native_minimum_integral', 'exact_minimum_angle', 'exact_minimum_integral']) >= 0)
            witness = load(a/f'analysis/{label}/{part}_witnesses.npz')
            for kind in ['exact', 'native']:
                for direction in ['forward', 'reverse']:
                    prefix = kind+'_'+direction+'_'; trace = witness[prefix+'trace']; order = witness[prefix+'trace_piece_index']
                    for j, i in enumerate(order):
                        inc, out, integral, defect = (trace[:, j, :, k] for k in range(4))
                        t, b, d = (witness[kind+'_kernel'][:, i, k, None] for k in range(3))
                        q = source[i][None, :]; sigma = witness['totals'][:, None]; h = witness['lengths'][:, i, None]
                        np.testing.assert_array_equal(inc, np.broadcast_to(boundary, inc.shape) if j == 0 else trace[:, j-1, :, 1])
                        np.testing.assert_array_equal(out, inc+b*(q-sigma*inc) if kind == 'native' else t*inc+b*q)
                        np.testing.assert_array_equal(integral, b*inc+d*q)
                        np.testing.assert_array_equal(defect, out-inc+sigma*integral-h*q)
                    np.testing.assert_array_equal(trace[:, -1, :, 1], witness[prefix+'outgoing'])
                    np.testing.assert_allclose(trace[:, :, :, 2].sum(axis=1), witness[prefix+'integral'], rtol=5e-15, atol=0)
            counts['checked_numeric_arrays'] += len(witness)
        assert summary['exact_controls_passed'] == all(r['exact_partition_passed'] and r['exact_balance_passed'] and r['direct_matrix_passed'] and r['positive_responses_passed'] for r in summary['partitions'])
        assert summary['native_partition_qualified'] == all(r['native_partition_passed'] for r in summary['partitions'])
        assert summary['native_mesh_convergence_qualified'] is False and summary['coupled_eigenreference_qualified'] is False
        for folder in ['runs', 'replay/runs']:
            u = json.loads((a/f'{folder}/{label}_analysis_resources.json').read_text()); resources[folder+'/'+label] = u
            assert u['peak_rss_mib'] <= plan['peak_rss_limit_mib'] and u['elapsed_seconds'] <= plan['elapsed_limit_seconds_per_process']
    # Recover every available failed-attempt response without changing that archive.
    prior = root/'validation/artifacts'/plan['predecessor_incomplete_artifact']
    for path in (prior/'analysis/group51').glob('*.npz'):
        if not path.stem.split('_')[-1].isdigit(): continue
        previous = load(path); part, _ = path.stem.rsplit('_', 1)
        first = int(previous['record_indices'][0]); last = int(previous['record_indices'][-1])+1
        chunks = [load(a/f'analysis/group51/{part}_{i:06d}.npz') for i in range(first, last, plan['chunk_records'])]
        for key, expected in previous.items():
            recovered = chunks[0][key] if key in ['boundary', 'source'] else np.concatenate([x[key] for x in chunks], axis=0)
            np.testing.assert_array_equal(expected, recovered); counts['prior_partial_arrays_recovered'] += 1
    extraction = json.loads((a/'replay/runs/extraction.json').read_text())
    assert len(extraction) == 4 and all(x['exit_code'] == 0 and x['elapsed_seconds'] <= 600 and x['child_high_water_rss_mib'] <= 512 for x in extraction)
    combined = json.loads((a/'analysis/result.json').read_text())
    assert combined['original_native_segments'] == counts['original_native_segments']
    assert combined['unique_native_records'] == counts['unique_native_records']
    rows = [r for g in fixture_results for r in g['partitions']]
    assert combined['native_failed_original_partition_directions'] == sum(r['native_failing_original_orders'] for r in rows)
    assert combined['native_failed_unique_partition_directions'] == sum(r['native_failing_unique_orders'] for r in rows)
    assert combined['maximum_native_preservation_relative'] == max(max(r['native_preservation_maximum_relative']) for r in rows)
    assert combined['maximum_exact_preservation_relative'] == max(max(r['exact_preservation_maximum_relative']) for r in rows)
    assert combined['native_partition_invariance_qualified'] == all(g['native_partition_qualified'] for g in fixture_results)
    counts.update(source_tests=10, archived_tests=10, independent_replay_tests=10, resources=resources,
        native_unsplit_recovered=True, exact_composition_qualified=all(x['exact_controls_passed'] for x in fixture_results),
        native_partition_qualified=all(x['native_partition_qualified'] for x in fixture_results),
        native_mesh_convergence_qualified=False, coupled_eigenreference_qualified=False, all_verification_checks_passed=True)
    with (a/'verification.json').open('x') as f: json.dump(counts, f, indent=2); f.write('\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('root', type=Path); p.add_argument('artifact', type=Path)
    args = p.parse_args(); main(args.root, args.artifact)

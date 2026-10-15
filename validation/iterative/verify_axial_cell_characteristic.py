#!/usr/bin/env python3
"""Verify frozen slab evidence, raw equations, exact replay and protected inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from analytic_axial_slab import errors_against_reference, adjacent_errors
from axial_cell_characteristic import diagnostics
from qualify_axial_cell_characteristic import summarize, controls_pass


def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()


def main(root, a):
    counts = dict(protected_files=0, initial_inputs=0, copied_inputs=0, prior_artifacts=0,
                  prior_manifest_entries=0, byte_identical_analysis_files=0, exact_numeric_arrays=0)
    for filename, key, base in [('protected_inputs_before.json', 'protected_files', root),
                                ('initial_inputs.json', 'initial_inputs', root),
                                ('copied_inputs.json', 'copied_inputs', a)]:
        for path, expected in json.loads((a/filename).read_text()).items():
            assert digest(base/path) == expected, path; counts[key] += 1
    for name, expected in json.loads((a/'prior_artifacts.json').read_text()).items():
        folder = root/'validation/artifacts'/name
        assert digest(folder/'result.sha256') == expected, name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected, path = line.split(maxsplit=1)
            assert digest(folder/path) == expected, f'{name}/{path}'; counts['prior_manifest_entries'] += 1
        counts['prior_artifacts'] += 1
    for f in (a/'build').glob('*.py'):
        assert digest(f) == digest(root/'validation/iterative'/f.name), f.name
    for log in ['source_tests.log', 'reference_tests.log', 'archived_tests.log', 'archived_reference_tests.log']:
        text = (a/'runs'/log).read_text()
        assert 'Ran 11 tests' in text and '\nOK\n' in text and 'skipped=' not in text, log
    files = sorted((a/'analysis').iterdir())
    assert [p.name for p in files] == sorted(p.name for p in (a/'replay/analysis').iterdir())
    for p in files:
        q = a/'replay/analysis'/p.name
        assert digest(p) == digest(q), p.name; counts['byte_identical_analysis_files'] += 1
        if p.suffix == '.npz':
            with np.load(p) as x, np.load(q) as y:
                assert x.files == y.files
                for key in x.files:
                    np.testing.assert_array_equal(x[key], y[key]); counts['exact_numeric_arrays'] += 1
    plan = json.loads((a/'plan.json').read_text()); limits = plan['limits']; mu = 1/np.sqrt(3)
    data = json.loads((a/'analysis/result.json').read_text())
    assert len(data['cases']) == 78 and len(data['adjacent']) == 65 and len(data['finest']) == 13
    assert {(r['case'], r['n']) for r in data['cases']} == {(c['id'], n) for c in plan['cases'] for n in plan['meshes']}
    assert len(data['periodic']) == 78
    field_keys = ['phi', 'angular', 'current', 'faces', 'face_current', 'face_second_moment',
                  'escape', 'source', 'incoming', 'rhs', 'matrix_residual']
    for row in data['cases']:
        n = row['n']; h = plan['height_cm']/n; t = row['total']; s = row['scattering']
        with np.load(a/f"analysis/{row['case']}_{n}.npz") as f:
            assert all(np.isfinite(f[k]).all() for k in f.files)
            for k, v in errors_against_reference(f).items(): np.testing.assert_array_equal(row[k], v)
            system = dict(widths=np.full(n, h), total=np.full(n, t), scattering=np.full(n, s), mu=mu,
                          periodic=False, **{k: f[k] for k in ['T', 'B', 'D', 'matrix']})
            for prefix in ['', 'basis_']:
                fields = {k: f[prefix+k] if prefix else f[k][..., None] for k in field_keys}
                metrics, raw = diagnostics(system, fields)
                record = row['basis'] if prefix else row
                for k, v in summarize(metrics).items(): assert record[k] == v, (row['case'], n, prefix+k)
                for k, v in raw.items():
                    np.testing.assert_array_equal(f[prefix+k], v if prefix else v[..., 0])
                np.testing.assert_array_equal(system['matrix'] @ fields['phi'] - fields['rhs'], fields['matrix_residual'])
                # Direct directional finite-volume equations, independent of the
                # stored moment defects and the analytic-reference comparisons.
                faces = fields['faces']; angles = fields['angular']; q = fields['source'] + s*fields['phi']
                incoming = np.stack([faces[0, :-1], faces[1, 1:]])
                outgoing = np.stack([faces[0, 1:], faces[1, :-1]])
                residual = mu*(outgoing-incoming) + h*(t*angles-q)
                scale = mu*abs(incoming) + h*(abs(q)+t*abs(angles))
                assert np.all(abs(residual) <= limits['characteristic_consistency_relative']*scale)
                if prefix:
                    for k, v in metrics.items(): np.testing.assert_array_equal(f['basis_metric_'+k], v)
                    assert fields['source'].shape == (2, n, 2*n+2)
                    np.testing.assert_array_equal(fields['source'][:, :, :2*n].reshape(2*n, 2*n), np.eye(2*n))
                    assert np.count_nonzero(fields['source'][:, :, -2:]) == 0
                    np.testing.assert_array_equal(fields['incoming'][:, -2:], np.eye(2))
                    assert np.count_nonzero(fields['incoming'][:, :-2]) == 0
                else:
                    np.testing.assert_array_equal(fields['source'], plan['source_per_direction'])
                    assert np.count_nonzero(fields['incoming']) == 0
            assert row['physical_controls_passed'] == controls_pass(row, limits)
            assert row['basis_controls_passed'] == controls_pass(row['basis'], limits)
            assert row['minimum_local_denominator'] == float(f['local_denominator'].min())
            np.testing.assert_array_equal(f['local_denominator'], 1-s*f['D']/(h/mu))
            assert row['minimum_local_denominator'] > limits['minimum_local_denominator']
            assert row['segment_identity_relative'] == max(float(np.max(abs(f['T']+t*f['B']-1))), float(np.max(abs(f['B']+t*f['D']-h/mu)/(h/mu))))
            assert row['segment_identity_relative'] < limits['segment_identity_relative']
            assert row['exact_absorption_void_control'] == (s == 0)
            face_error = float(np.max(abs(f['faces']-f['reference_faces']))/np.max(abs(f['reference_faces'])))
            assert row['face_true_relative_max'] == face_error
            if s == 0:
                assert row['exact_absorption_void_passed'] == (max(row['angular_true_relative'], face_error) < limits['absorption_void_exact_relative'])
            else: assert row['exact_absorption_void_passed'] is None
            periodic = next(p for p in data['periodic'] if p['case'] == row['case'] and p['n'] == n)
            if t > s:
                ps = {**system, 'periodic': True, 'matrix': f['periodic_matrix']}
                pf = {k: f['periodic_'+k][..., None] for k in field_keys}
                pm, pr = diagnostics(ps, pf)
                for k, v in summarize(pm).items(): assert periodic[k] == v
                for k, v in pr.items(): np.testing.assert_array_equal(f['periodic_'+k], v[..., 0])
                np.testing.assert_array_equal(ps['matrix']@pf['phi']-pf['rhs'], pf['matrix_residual'])
                expected = plan['source_per_direction']/(t-s)
                error = max(float(np.max(abs(pf[k]-expected))/expected) for k in ['phi', 'angular', 'faces'])
                assert periodic['constant_mode_relative'] == error
                assert periodic['passed'] == (controls_pass(periodic, limits) and error < limits['periodic_constant_relative'])
            else: assert periodic['rejected'] and periodic['passed'] and 'integrated balance' in periodic['reason']
            with np.load(a/f"inputs/upwind/{row['case']}_{n}.npz") as old:
                for k in old.files:
                    if k.startswith('reference_'): np.testing.assert_array_equal(f[k], old[k])
                for k, v in errors_against_reference(old).items(): np.testing.assert_array_equal(row['upwind'][k], v)
        analytic = all(row['analytic'][k] < limits['analytic_identities_relative'] for k in ['even_identity_relative', 'odd_identity_relative', 'boundary_relative', 'global_balance_relative', 'cell_quadrature_relative'])
        assert row['analytic_passed'] == analytic
        passed = row['physical_controls_passed'] and row['basis_controls_passed'] and analytic and row['exact_absorption_void_passed'] is not False and periodic['passed']
        assert row['implementation_passed'] == passed
        assert row['accuracy_target_passed'] == (max(row['scalar_true_relative'], row['total_escape_true_relative']) < limits['finest_scalar_escape_relative'])
    for pair in data['adjacent']:
        with np.load(a/f"analysis/{pair['case']}_{pair['coarse_n']}.npz") as c, np.load(a/f"analysis/{pair['case']}_{pair['fine_n']}.npz") as f:
            for k, v in adjacent_errors(c, f).items(): np.testing.assert_array_equal(pair[k], v)
            fine = errors_against_reference(f); coarse = errors_against_reference(c)
            for k in ['scalar', 'angular', 'total_escape']:
                error = fine[k+'_true_relative']; old = coarse[k+'_true_relative']
                assert pair[k+'_true_fine_relative'] == error
                order = float(np.log2(old/error)) if min(old, error) > plan['order_noise_floor'] else None
                assert pair[k+'_observed_true_order'] == order
        below = max(pair['scalar_adjacent_relative'], pair['total_escape_adjacent_relative']) < plan['diagnostic_threshold']
        accurate = max(fine['scalar_true_relative'], fine['total_escape_true_relative']) < limits['finest_scalar_escape_relative']
        assert pair['adjacent_pair_below_one_percent'] == below and pair['false_admission'] == (below and not accurate)
    assert data['finest'] == [r for r in data['cases'] if r['n'] == max(plan['meshes'])]
    assert data['implementation_qualified'] == all(r['implementation_passed'] for r in data['cases'])
    assert data['finest_accuracy_target_passed'] == all(r['accuracy_target_passed'] for r in data['finest'])
    assert data['slab_candidate_qualified'] == (data['implementation_qualified'] and data['finest_accuracy_target_passed'])
    assert data['basis_response_columns'] == sum(r['basis_columns'] for r in data['cases']) == 13260
    assert data['false_admission_count'] == sum(p['false_admission'] for p in data['adjacent'])
    assert not data['native_mesh_convergence_qualified'] and not data['coupled_eigenreference_qualified']
    resource_usage = {}
    for directory in ['runs', 'replay/runs']:
        u = json.loads((a/directory/'resource_usage.json').read_text()); resource_usage[directory] = u
        assert u['elapsed_seconds'] <= plan['elapsed_limit_seconds'] and u['peak_rss_mib'] <= plan['peak_rss_limit_mib']
        cost = json.loads((a/directory/'costs.json').read_text())
        assert len(cost) == 78 and {(r['case'], r['n']) for r in cost} == {(r['case'], r['n']) for r in data['cases']}
        assert all(np.isfinite(r[k]) and r[k] >= 0 for r in cost for k in ['candidate_physical_seconds', 'candidate_basis_seconds', 'upwind_physical_seconds'])
    counts.update(prescribed_slab_solves=78, directional_volume_unit_responses=13104,
                  boundary_unit_responses=156, periodic_absorbing_controls=54, periodic_incompatible_rejections=24,
                  source_tests=22, archived_tests=22, resource_usage=resource_usage,
                  all_verification_checks_passed=True, slab_candidate_qualified=data['slab_candidate_qualified'],
                  native_mesh_convergence_qualified=False, coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f: json.dump(counts, f, indent=2); f.write('\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('root', type=Path); p.add_argument('artifact', type=Path)
    args = p.parse_args(); main(args.root, args.artifact)

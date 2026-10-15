#!/usr/bin/env python3
"""Run frozen slab comparisons, every source-basis column, and periodic controls."""
import argparse
import json
import resource
import sys
import time
from pathlib import Path
import numpy as np
from axial_cell_characteristic import assemble, solve, diagnostics, unit_inputs
from analytic_axial_slab import (analytic_checks, analytic_points, errors_against_reference,
                                adjacent_errors, discrete_slab)


def save(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2, allow_nan=False); f.write('\n')


def summarize(metrics):
    return {k: float(v.min() if k.startswith('minimum_') else v.max()) for k, v in metrics.items()}


def controls_pass(row, limits):
    return (row['matrix_residual_relative'] < limits['matrix_residual_relative']
            and all(row[k] < limits['characteristic_consistency_relative'] for k in [
                'characteristic_consistency_relative', 'scalar_consistency_relative', 'boundary_consistency_relative'])
            and row['raw_global_balance_relative'] < limits['raw_global_balance_relative']
            and min(row['minimum_angular'], row['minimum_face']) >= limits['minimum_flux'])


def main(root):
    plan = json.loads((root/'plan.json').read_text()); limits = plan['limits']; start = time.perf_counter()
    mu = 1/np.sqrt(3); height = plan['height_cm']; source = plan['source_per_direction']
    result = dict(scope=plan['scope'], cases=[], adjacent=[], finest=[], periodic=[]); costs = []

    def usage():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform == 'darwin' else 1024)
        return dict(elapsed_seconds=time.perf_counter()-start, peak_rss_mib=rss)

    try:
        for case in plan['cases']:
            previous = None; previous_row = None
            for n in plan['meshes']:
                total = case['total']; scatter = case['scattering']; h = height/n
                args = total, scatter, height, mu, source, n
                analytic, fresh_reference = analytic_checks(*args)
                with np.load(root/f"inputs/upwind/{case['id']}_{n}.npz") as old:
                    reference = {k: old[k].copy() for k in fresh_reference}
                    for k in reference: np.testing.assert_array_equal(reference[k], fresh_reference[k])
                    tick = time.perf_counter(); _, upwind = discrete_slab(*args)
                    upwind_seconds = time.perf_counter()-tick
                    for k in upwind: np.testing.assert_array_equal(upwind[k], old[k])
                    upwind.update(reference); upwind_error = errors_against_reference(upwind)
                tick = time.perf_counter()
                system = assemble(np.full(n, h), total, scatter, mu)
                f = solve(system, np.full((2, n, 1), source), np.zeros((2, 1)))
                physical_seconds = time.perf_counter()-tick
                metrics, raw = diagnostics(system, f)
                fields = {k: v[..., 0] for k, v in f.items()}
                fields.update({k: v[..., 0] for k, v in raw.items()})
                fields.update(reference, edges=np.linspace(0, height, n+1), matrix=system['matrix'])
                fields.update({k: system[k] for k in ['T', 'B', 'D', 'local_denominator']})
                tick = time.perf_counter(); basis = solve(system, *unit_inputs(n))
                basis_seconds = time.perf_counter()-tick
                basis_metrics, basis_raw = diagnostics(system, basis)
                for prefix, data in [('basis_', basis), ('basis_', basis_raw), ('basis_metric_', basis_metrics)]:
                    fields.update({prefix+k: v for k, v in data.items()})
                row = dict(case=case['id'], n=n, total=total, scattering=scatter, analytic=analytic,
                           **summarize(metrics), basis=summarize(basis_metrics), basis_columns=2*n+2,
                           **errors_against_reference(fields), upwind=upwind_error)
                row['minimum_local_denominator'] = float(system['local_denominator'].min())
                row['segment_identity_relative'] = max(float(np.max(abs(system['T']+total*system['B']-1))),
                    float(np.max(abs(system['B']+total*system['D']-h/mu)/(h/mu))))
                row['physical_controls_passed'] = controls_pass(row, limits)
                row['basis_controls_passed'] = controls_pass(row['basis'], limits)
                row['analytic_passed'] = all(analytic[k] < limits['analytic_identities_relative'] for k in [
                    'even_identity_relative', 'odd_identity_relative', 'boundary_relative', 'global_balance_relative', 'cell_quadrature_relative'])
                p, j = analytic_points(fields['edges'], total, scatter, height, mu, source)
                fields['reference_faces'] = np.stack([p+j/mu, p-j/mu])
                row['face_true_relative_max'] = float(np.max(abs(fields['faces']-fields['reference_faces']))/np.max(abs(fields['reference_faces'])))
                row['exact_absorption_void_control'] = scatter == 0
                row['exact_absorption_void_passed'] = (max(row['angular_true_relative'], row['face_true_relative_max']) < limits['absorption_void_exact_relative']) if scatter == 0 else None
                periodic = dict(case=case['id'], n=n)
                if total > scatter:
                    ps = assemble(np.full(n, h), total, scatter, mu, periodic=True)
                    pf = solve(ps, np.full((2, n, 1), source), np.zeros((2, 1)))
                    pm, pr = diagnostics(ps, pf); periodic.update(summarize(pm))
                    expected = source/(total-scatter)
                    periodic['constant_mode_relative'] = max(float(np.max(abs(pf[k]-expected))/expected) for k in ['phi', 'angular', 'faces'])
                    periodic['passed'] = controls_pass(periodic, limits) and periodic['constant_mode_relative'] < limits['periodic_constant_relative']
                    for k, v in {**pf, **pr}.items(): fields['periodic_'+k] = v[..., 0]
                    fields['periodic_matrix'] = ps['matrix']
                else:
                    try: assemble(np.full(n, h), total, scatter, mu, periodic=True)
                    except ValueError as exc:
                        periodic.update(rejected=True, reason=str(exc), passed='integrated balance' in str(exc))
                    else: periodic.update(rejected=False, passed=False)
                result['periodic'].append(periodic)
                row['implementation_passed'] = (row['physical_controls_passed'] and row['basis_controls_passed']
                    and row['analytic_passed'] and row['minimum_local_denominator'] > limits['minimum_local_denominator']
                    and row['segment_identity_relative'] < limits['segment_identity_relative']
                    and row['exact_absorption_void_passed'] is not False and periodic['passed'])
                row['accuracy_target_passed'] = max(row['scalar_true_relative'], row['total_escape_true_relative']) < limits['finest_scalar_escape_relative']
                np.savez_compressed(root/f"analysis/{case['id']}_{n}.npz", **fields)
                costs.append(dict(case=case['id'], n=n, candidate_physical_seconds=physical_seconds,
                                  candidate_basis_seconds=basis_seconds, upwind_physical_seconds=upwind_seconds))
                if previous is not None:
                    pair = dict(case=case['id'], coarse_n=n//2, fine_n=n, **adjacent_errors(previous, fields))
                    for key in ['scalar', 'angular', 'total_escape']:
                        error = row[key+'_true_relative']; old_error = previous_row[key+'_true_relative']
                        pair[key+'_true_fine_relative'] = error
                        pair[key+'_observed_true_order'] = float(np.log2(old_error/error)) if min(error, old_error) > plan['order_noise_floor'] else None
                    below = max(pair['scalar_adjacent_relative'], pair['total_escape_adjacent_relative']) < plan['diagnostic_threshold']
                    pair['adjacent_pair_below_one_percent'] = below
                    pair['false_admission'] = below and not row['accuracy_target_passed']
                    result['adjacent'].append(pair)
                result['cases'].append(row); previous = fields; previous_row = row
                u = usage()
                if u['elapsed_seconds'] > plan['elapsed_limit_seconds'] or u['peak_rss_mib'] > plan['peak_rss_limit_mib']:
                    raise RuntimeError(f'Predeclared resource cap exceeded: {u}')
            result['finest'].append(row)
            print(case['id'], 'scalar', row['scalar_true_relative'], 'escape', row['total_escape_true_relative'],
                  'implementation', row['implementation_passed'], flush=True)
        result['implementation_qualified'] = all(r['implementation_passed'] for r in result['cases'])
        result['finest_accuracy_target_passed'] = all(r['accuracy_target_passed'] for r in result['finest'])
        result['slab_candidate_qualified'] = result['implementation_qualified'] and result['finest_accuracy_target_passed']
        result['basis_response_columns'] = sum(r['basis_columns'] for r in result['cases'])
        result['false_admission_count'] = sum(r['false_admission'] for r in result['adjacent'])
        result['native_mesh_convergence_qualified'] = False; result['coupled_eigenreference_qualified'] = False
        save(root/'analysis/result.json', result)
        print(json.dumps({k: v for k, v in result.items() if isinstance(v, (bool, int))}, indent=2))
    finally:
        save(root/'runs/costs.json', costs); save(root/'runs/resource_usage.json', usage())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('artifact', type=Path)
    main(parser.parse_args().artifact)

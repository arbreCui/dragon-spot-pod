#!/usr/bin/env python3
"""Bounded full-fixture composition audit, preserving failures and all endpoints."""
import argparse
import json
import resource
import sys
import time
from pathlib import Path
import numpy as np
from native_segment_composition import read_native, exact_coefficients, input_patterns, flight, preservation


def save(path, value):
    with path.open('x') as f: json.dump(value, f, indent=2, allow_nan=False); f.write('\n')


def main(root, group):
    plan = json.loads((root/'plan.json').read_text()); limits = plan['limits']; tick = time.perf_counter()
    label = 'controls' if group == 'controls' else 'group'+group
    output = root/'analysis'/label; output.mkdir()
    if group == 'controls':
        with (root/'inputs/controls.request').open('rb') as f:
            np.fromfile(f, '<i4', 2); unique = np.fromfile(f, '<f8').reshape(-1, 2)
        multiplicity = np.ones(len(unique), dtype=int); original_count = len(unique)
    else:
        with np.load(root/f'inputs/{label}.npz') as f:
            unique = f['unique']; multiplicity = np.bincount(f['inverse']); original_count = len(f['inverse'])
    total, length = unique[:, 0], unique[:, 1]
    fractions = np.asarray(plan['coefficient_fractions'])
    native = read_native(root/f'runs/{label}.native')
    exact = np.empty_like(native)
    for start in range(0, len(unique), plan['chunk_records']):
        sl = slice(start, min(start+plan['chunk_records'], len(unique)))
        exact[sl] = exact_coefficients(length[sl, None]*fractions, total[sl, None])
    coefficient_fields = dict(exact=exact, native=native,
        native_minus_exact=native-exact, multiplicity=multiplicity,
        native_boundary_balance=native[:, :, 0]-1+total[:, None]*native[:, :, 1],
        native_source_balance=native[:, :, 1]+total[:, None]*native[:, :, 2]-length[:, None]*fractions)
    summary = dict(label=label, unique_records=len(unique), original_records=original_count,
                   native_minimum_coefficients=native.min(axis=(0, 1)).tolist(),
                   exact_minimum_coefficients=exact.min(axis=(0, 1)).tolist(), partitions=[])
    if group != 'controls':
        calibration = abs(native[:, 0, 1:]-unique[:, 2:])/unique[:, 2:]
        coefficient_fields['native_calibration_relative'] = calibration
        summary['native_calibration_maximum_relative'] = calibration.max(axis=0).tolist()
        summary['native_calibration_bitwise_equal'] = bool(np.array_equal(native[:, 0, 1:], unique[:, 2:]))
        summary['native_calibration_passed'] = bool(calibration.max() < limits['unsplit_native_relative'])
    else:
        summary['native_void_supported'] = bool(np.array_equal(native[0], exact[0]))
    np.savez_compressed(output/'coefficients.npz', **coefficient_fields)
    del coefficient_fields

    def usage():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform == 'darwin' else 1024)
        return dict(elapsed_seconds=time.perf_counter()-tick, peak_rss_mib=rss)

    try:
        for name, parts in plan['partitions'].items():
            n = len(parts); index = [list(fractions).index(x) for x in parts]
            boundary, sources = input_patterns(n)
            row = dict(partition=name, pieces=n, input_columns=n+3, orders=2,
                       native_preservation_maximum_relative=[0.]*4, exact_preservation_maximum_relative=[0.]*4,
                       native_failing_unique_orders=0, native_failing_original_orders=0,
                       exact_failing_unique_orders=0, exact_failing_original_orders=0,
                       native_maximum_global_balance_relative=0., exact_maximum_global_balance_relative=0.,
                       native_maximum_local_balance_relative=0., exact_maximum_local_balance_relative=0.,
                       maximum_direct_matrix_relative=0., native_minimum_angle=1., native_minimum_integral=1.,
                       exact_minimum_angle=1., exact_minimum_integral=1.,
                       worst_preservation=dict(value=-1., record=-1, order=-1),
                       worst_balance=dict(value=-1., record=-1, order=-1, column=-1))
            for start in range(0, len(unique), plan['chunk_records']):
                end = min(start+plan['chunk_records'], len(unique)); sl = slice(start, end)
                h = length[sl, None]*np.asarray(parts); sigma = total[sl, None]
                fields = dict(record_indices=np.arange(start, end), lengths=h, totals=total[sl],
                              boundary=boundary, source=sources, multiplicity=multiplicity[sl])
                for kind, all_coefficients in [('exact', exact), ('native', native)]:
                    kernel = all_coefficients[sl][:, index]; fields[kind+'_kernel'] = kernel
                    for direction, reverse in [('forward', False), ('reverse', True)]:
                        result = flight(h, sigma, kernel, boundary, sources, reverse=reverse, native=kind == 'native')
                        error = preservation(result, all_coefficients[sl, 0], length[sl])
                        prefix = kind+'_'+direction+'_'
                        fields.update({prefix+k: v for k, v in result.items()}); fields[prefix+'preservation_relative'] = error
                        row[kind+'_preservation_maximum_relative'] = np.maximum(row[kind+'_preservation_maximum_relative'], error.max(axis=0)).tolist()
                        failed = np.max(error, axis=1) >= limits[kind+'_partition_relative']
                        row[kind+'_failing_unique_orders'] += int(failed.sum())
                        row[kind+'_failing_original_orders'] += int(np.dot(failed.astype(int), multiplicity[sl]))
                        for location in ['global', 'local']:
                            key = 'global_balance_relative' if location == 'global' else 'maximum_local_balance_relative'
                            metric = kind+'_maximum_'+location+'_balance_relative'
                            row[metric] = max(row[metric], float(result[key].max()))
                        row['maximum_direct_matrix_relative'] = max(row['maximum_direct_matrix_relative'],
                            float(result['matrix_outgoing_relative'].max()), float(result['matrix_integral_relative'].max()))
                        row[kind+'_minimum_angle'] = min(row[kind+'_minimum_angle'], float(result['minimum_angle'].min()))
                        row[kind+'_minimum_integral'] = min(row[kind+'_minimum_integral'], float(result['minimum_integral'].min()))
                        if kind == 'native':
                            worst = int(np.argmax(error.max(axis=1))); value = float(error[worst].max())
                            if value > row['worst_preservation']['value']:
                                row['worst_preservation'] = dict(value=value, record=start+worst, order=int(reverse))
                            ir, ic = np.unravel_index(np.argmax(result['global_balance_relative']), result['global_balance_relative'].shape)
                            value = float(result['global_balance_relative'][ir, ic])
                            if value > row['worst_balance']['value']:
                                row['worst_balance'] = dict(value=value, record=start+int(ir), order=int(reverse), column=int(ic))
                np.savez_compressed(output/f'{name}_{start:06d}.npz', **fields)
                u = usage()
                if u['elapsed_seconds'] > plan['elapsed_limit_seconds_per_process'] or u['peak_rss_mib'] > plan['peak_rss_limit_mib']:
                    raise RuntimeError(f'Predeclared process resource limit exceeded: {u}')
            witnesses = sorted({row['worst_preservation']['record'], row['worst_balance']['record']})
            h = length[witnesses, None]*np.asarray(parts); sigma = total[witnesses, None]
            witness = dict(record_indices=np.array(witnesses), lengths=h, totals=total[witnesses], boundary=boundary, source=sources)
            for kind, all_coefficients in [('exact', exact), ('native', native)]:
                kernel = all_coefficients[witnesses][:, index]; witness[kind+'_kernel'] = kernel
                for direction, reverse in [('forward', False), ('reverse', True)]:
                    f = flight(h, sigma, kernel, boundary, sources, reverse=reverse, native=kind == 'native', trace=True)
                    witness.update({kind+'_'+direction+'_'+k: v for k, v in f.items()})
            np.savez_compressed(output/f'{name}_witnesses.npz', **witness)
            row['exact_partition_passed'] = row['exact_failing_unique_orders'] == 0
            row['native_partition_passed'] = row['native_failing_unique_orders'] == 0
            row['exact_balance_passed'] = row['exact_maximum_global_balance_relative'] < limits['exact_raw_balance_relative']
            row['native_balance_context_passed'] = row['native_maximum_global_balance_relative'] < limits['native_balance_context_relative']
            row['direct_matrix_passed'] = row['maximum_direct_matrix_relative'] < limits['direct_matrix_relative']
            row['positive_responses_passed'] = min(row[k] for k in ['native_minimum_angle', 'native_minimum_integral', 'exact_minimum_angle', 'exact_minimum_integral']) >= limits['minimum_kernel_response']
            summary['partitions'].append(row)
            print(label, name, 'native preservation', max(row['native_preservation_maximum_relative']),
                  'exact', max(row['exact_preservation_maximum_relative']), 'native balance', row['native_maximum_global_balance_relative'], flush=True)
        summary['exact_controls_passed'] = all(r['exact_partition_passed'] and r['exact_balance_passed'] and r['direct_matrix_passed'] and r['positive_responses_passed'] for r in summary['partitions'])
        summary['native_partition_qualified'] = all(r['native_partition_passed'] for r in summary['partitions'])
        summary['native_mesh_convergence_qualified'] = False; summary['coupled_eigenreference_qualified'] = False
        save(output/'result.json', summary)
    finally: save(root/f'runs/{label}_analysis_resources.json', usage())


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path)
    p.add_argument('group', choices=['51', '61', '98', 'controls']); args = p.parse_args()
    main(args.artifact, args.group)

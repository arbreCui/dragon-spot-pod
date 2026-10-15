#!/usr/bin/env python3
"""Summarize native/exact composition outcomes without changing their gates."""
import argparse
import json
from pathlib import Path
import numpy as np


def main(root):
    groups = [json.loads((root/f'analysis/group{g}/result.json').read_text()) for g in [51, 61, 98]]
    controls = json.loads((root/'analysis/controls/result.json').read_text())
    rows = [r for g in groups for r in g['partitions']]
    result = dict(original_native_segments=sum(g['original_records'] for g in groups),
        unique_native_records=sum(g['unique_records'] for g in groups),
        original_partition_direction_comparisons=8*sum(g['original_records'] for g in groups),
        unique_partition_direction_comparisons=8*sum(g['unique_records'] for g in groups),
        native_failed_original_partition_directions=sum(r['native_failing_original_orders'] for r in rows),
        native_failed_unique_partition_directions=sum(r['native_failing_unique_orders'] for r in rows),
        maximum_native_preservation_relative=max(max(r['native_preservation_maximum_relative']) for r in rows),
        maximum_exact_preservation_relative=max(max(r['exact_preservation_maximum_relative']) for r in rows),
        maximum_native_global_balance_relative=max(r['native_maximum_global_balance_relative'] for r in rows),
        maximum_exact_global_balance_relative=max(r['exact_maximum_global_balance_relative'] for r in rows),
        maximum_direct_matrix_relative=max(r['maximum_direct_matrix_relative'] for r in rows),
        native_unsplit_recovered=all(g['native_calibration_passed'] and g['native_calibration_bitwise_equal'] for g in groups),
        exact_composition_qualified=all(g['exact_controls_passed'] for g in groups+[controls]),
        native_partition_invariance_qualified=all(g['native_partition_qualified'] for g in groups),
        native_void_supported=controls['native_void_supported'],
        controls_maximum_native_preservation_relative=max(max(r['native_preservation_maximum_relative']) for r in controls['partitions']),
        controls_maximum_exact_preservation_relative=max(max(r['exact_preservation_maximum_relative']) for r in controls['partitions']),
        native_mesh_convergence_qualified=False, coupled_eigenreference_qualified=False, groups=[])
    for group, g in zip([51, 61, 98], groups):
        row = max(g['partitions'], key=lambda r: r['worst_preservation']['value'])
        record = row['worst_preservation']['record']
        with np.load(root/f'inputs/group{group}.npz') as f: total, length = f['unique'][record, :2]
        with np.load(root/f'analysis/group{group}/coefficients.npz') as f:
            difference = np.max(abs(f['native'][:, 0]-f['exact'][:, 0])/f['exact'][:, 0], axis=0)
        result['groups'].append(dict(group=group,
            native_preservation_T_Bout_Bintegral_D_relative=np.max([r['native_preservation_maximum_relative'] for r in g['partitions']], axis=0).tolist(),
            whole_native_vs_exact_T_B_D_relative=difference.tolist(),
            worst_partition=row['partition'], worst_record=record, worst_total=float(total), worst_length=float(length),
            worst_optical_length=float(total*length), worst_metric=row['worst_preservation']['value']))
    with (root/'analysis/result.json').open('x') as f: json.dump(result, f, indent=2); f.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path); main(p.parse_args().artifact)

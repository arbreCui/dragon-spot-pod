#!/usr/bin/env python3
"""Summarize full-flight qualification and measured native-kernel changes."""
import argparse
import json
from pathlib import Path


def main(root):
    phases = [json.loads(p.read_text()) for p in sorted((root/'analysis').glob('*/result.json'))]
    exact = [r for r in phases if r['phase'] != 'native']; partitions = [r for r in exact if r['phase'] != 'whole']
    result = dict(phases=len(phases), native_fixed_input_cases=648, exact_fixed_input_evaluations=3240,
        exact_reclosed_positive_evaluations=1005, exact_partition_case_comparisons=3396,
        native_calibration_maximum_relative=max(max(r['native_recovery'].values()) for r in phases if r['phase']=='native'),
        exact_partition_maximum_induced_relative=max(v['maximum'] for r in partitions for name in ['fixed_partition','white_partition'] for k,v in r[name].items() if 'induced_relative' in k),
        exact_piece_balance_maximum_relative=max(r['maximum_piece_balance_relative'] for r in exact),
        exact_track_balance_maximum_relative=max(r['maximum_track_balance_relative'] for r in exact),
        white_solve_maximum_relative=max(r['white_solve_relative'] for r in exact),
        white_closure_maximum_relative=max(r['white_closure_relative'] for r in exact),
        native_calibration_qualified=all(r['phase_qualified'] for r in phases if r['phase']=='native'),
        exact_full_flight_companion_qualified=all(r['phase_qualified'] for r in phases),
        native_partition_invariance_qualified=False, native_mesh_convergence_qualified=False,
        coupled_eigenreference_qualified=False, groups=[])
    for g in [51,61,98]:
        r=next(r for r in phases if r['group']==g and r['phase']=='whole')
        result['groups'].append(dict(group=g, **{k:r[k] for k in ['fixed_vs_native','white_vs_native','reclosure_effect',
            'white_geometric_net_current_max','white_stored_net_current_max']}))
    with (root/'analysis/result.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)

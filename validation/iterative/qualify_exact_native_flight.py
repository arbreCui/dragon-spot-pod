#!/usr/bin/env python3
"""Evaluate the frozen complete radial flight and reclosed common boundary."""
import argparse
import json
import resource
import sys
import time
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native
from exact_native_flight import green_sweep, evaluate, compare, close_white, ratio


def save(path, value):
    with path.open('x') as f: json.dump(value, f, indent=2, allow_nan=False); f.write('\n')


def read(path):
    with np.load(path) as f: return {k: f[k] for k in f.files}


def metrics_summary(metrics, tags):
    summary = {}
    for key, value in metrics.items():
        if key.endswith('_valid'): continue
        if key.endswith('_weighted_net_relative'):
            valid = metrics[key.replace('_weighted_net_relative', '_net_relative_valid')]
            if not valid.any():
                summary[key] = dict(maximum=None, case=None, tag=None); continue
            value = np.where(valid, value, -1.)
        i = int(np.argmax(value)); summary[key] = dict(maximum=float(value[i]), case=i, tag=tags[i])
    return summary


def compare_gate(metrics, limit):
    return all(np.max(v) < limit for k, v in metrics.items() if 'induced_relative' in k)


def action_error(value, reference):
    axes = tuple(range(value.ndim-1))
    return float(np.max(ratio(np.max(abs(value-reference), axis=axes), np.max(abs(reference), axis=axes))))


def main(root, group, phase):
    plan = json.loads((root/'plan.json').read_text()); lim = plan['limits']; tick = time.perf_counter()
    label = f'{group}_{phase}'; target = root/'analysis'/label; target.mkdir()
    def usage():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform == 'darwin' else 1024)
        return dict(elapsed_seconds=time.perf_counter()-tick, peak_rss_mib=rss)
    try:
        d = load_native(root/'inputs/track_data.bin'); a = next(a for a in d['group_data'] if a['group'] == group)
        old = read(root/f'inputs/prepared_{group}.npz'); old_result = read(root/f'inputs/result_{group}.npz')
        tags = json.loads((root/f'inputs/cases_{group}.json').read_text())
        positive = (old['q'].min(axis=(0, 1, 2)) >= 0) & (old['inflow'].min(axis=(0, 1, 2)) >= 0)
        assert len(tags) == 216 and positive.sum() == 214
        native = phase == 'native'; fractions = [1.] if native else plan['partitions'][phase]
        start = time.perf_counter(); green = green_sweep(d, a, fractions, native=native, chunk=plan['record_chunk'])
        green_seconds = time.perf_counter()-start
        fields = evaluate(d, a, green, old['q'], old['inflow'])
        white = close_white(d, a, green, fields, tags)
        targets = white['target_indices']; white_tags = [tags[i] for i in targets]
        assert len(targets) == 67
        track_balance = ratio(green['track_defect'], green['track_scale'])
        matrix = np.eye(d['nb'])-white['tbb']
        row = dict(group=group, phase=phase, fixed_cases=216, positive_fixed_cases=214,
            reclosed_cases=67, minimum_track_angle=float(green['track_minimum_angle'].min()),
            minimum_track_integral=float(green['track_minimum_integral'].min()),
            maximum_piece_balance_relative=float(green['track_maximum_local_balance'].max()),
            maximum_track_balance_relative=float(track_balance.max()),
            minimum_white_inverse=float(white['boundary_inverse'].min()),
            inverse_identity_relative=float(np.max(abs(matrix@white['boundary_inverse']-np.eye(d['nb'])))),
            white_solve_relative=float(np.max(ratio(abs(white['white_matrix_residual']).max(axis=0), abs(white['white_rhs']).max(axis=0)))),
            white_closure_relative=float(np.max(ratio(abs(white['white_closure_defect']).max(axis=0), abs(white['white_amplitudes']).max(axis=0)))),
            minimum_reclosed_inflow=float(white['inflow'].min()),
            fixed_even_balance_relative=float(fields['even_relative'].max()), fixed_odd_balance_relative=float(fields['odd_relative'].max()),
            white_even_balance_relative=float(white['even_relative'].max()), white_odd_balance_relative=float(white['odd_relative'].max()),
            white_stored_net_current_max=float(abs(white['stored_white_net_current']).max()),
            white_geometric_net_current_max=float(abs(white['even_incoming']-white['even_outgoing']).max()),
            signed_control_minimum_integral=float((fields['iso']+fields['own'])[..., ~positive].min()),
            signed_control_minimum_outgoing=float(fields['boundary'][..., ~positive].min()))
        row['positive_responses_passed'] = (row['minimum_track_angle'] >= 0 and row['minimum_track_integral'] >= 0
            and row['minimum_white_inverse'] >= 0 and row['minimum_reclosed_inflow'] >= 0
            and np.min((fields['iso']+fields['own'])[..., positive]) >= 0 and np.min(fields['boundary'][..., positive]) >= 0
            and np.min(white['iso']+white['own']) >= 0 and np.min(white['boundary']) >= 0)
        row['positive_responses_passed'] = bool(row['positive_responses_passed'])
        row['white_algebra_passed'] = max(row['inverse_identity_relative'], row['white_solve_relative'], row['white_closure_relative']) < lim['white_residual_relative']
        row['assembled_balance_context_passed'] = max(row[k] for k in ['fixed_even_balance_relative', 'fixed_odd_balance_relative', 'white_even_balance_relative', 'white_odd_balance_relative']) < lim['assembled_global_balance_context_relative']
        comparison = {}
        if native:
            recovery = dict(iso=action_error(fields['iso'], old['iso']), own=action_error(fields['own'], old['own']),
                boundary=action_error(fields['boundary'], old['boundary']),
                native_half_integrals=action_error(fields['iso']+fields['own'], old_result['native_half_integrals']),
                native_half_outgoing=action_error(fields['boundary'], old_result['native_half_outgoing']),
                phi=float(np.max(ratio(fields['phi']-old_result['native_phi'], fields['phi_scale']))),
                jz=float(np.max(ratio(fields['jz']-old_result['native_jz'], fields['jz_scale']))))
            delta = a['pjj']-2*a['pjsum']/d['weights'][:d['nr']]
            fields['pjj_completion_legacy'] = delta[:, None]*old['legacy'][:d['nr']]
            fields['p0_completed_legacy'] = fields['phi'][:, :31]+fields['pjj_completion_legacy']
            recovery['p0_completed'] = action_error(np.r_[fields['p0_completed_legacy'], fields['outgoing'][:, :31]], old_result['old_native'])
            recovery['reclosed_native_inflow'] = action_error(white['inflow'], old['inflow'][..., targets])
            row['native_recovery'] = recovery; row['native_calibration_passed'] = max(recovery.values()) < lim['native_action_relative']
            row['exact_internal_balance_passed'] = None
        else:
            baseline = read(root/f'analysis/{group}_native/fixed.npz'); baseline_white = read(root/f'analysis/{group}_native/white.npz')
            for label_, current, ref, labels in [('fixed_vs_native', fields, baseline, tags), ('white_vs_native', white, baseline_white, white_tags),
                ('reclosure_effect', white, {k: fields[k][..., targets] for k in ['phi','jx','jz','outgoing','phi_scale','jx_scale','jz_scale','outgoing_scale']}, white_tags)]:
                metric = compare(d, current, ref); comparison.update({label_+'_'+k: v for k, v in metric.items()})
                row[label_] = metrics_summary(metric, labels)
            fields['native_pjj_completion_legacy'] = baseline['pjj_completion_legacy']
            fields['kernel_only_phi_change_legacy'] = fields['phi'][:, :31]-baseline['phi'][:, :31]
            fields['change_from_completed_native_legacy'] = fields['phi'][:, :31]-baseline['p0_completed_legacy']
            row['exact_internal_balance_passed'] = max(row['maximum_piece_balance_relative'], row['maximum_track_balance_relative']) < lim['exact_piece_track_balance_relative']
            if phase != 'whole':
                for category, value, refpath, labels in [('fixed', fields, 'fixed.npz', tags), ('white', white, 'white.npz', white_tags)]:
                    ref = read(root/f'analysis/{group}_whole'/refpath); metric = compare(d, value, ref)
                    comparison.update({category+'_partition_'+k: v for k, v in metric.items()})
                    row[category+'_partition'] = metrics_summary(metric, labels)
                    row[category+'_partition_passed'] = compare_gate(metric, lim['exact_partition_relative'])
                    row[category+'_half_integrals_partition_relative'] = action_error(value['iso']+value['own'], ref['iso']+ref['own'])
                    row[category+'_half_boundary_partition_relative'] = action_error(value['boundary'], ref['boundary'])
                    row[category+'_partition_passed'] &= max(row[category+'_half_integrals_partition_relative'], row[category+'_half_boundary_partition_relative']) < lim['exact_partition_relative']
        row['phase_qualified'] = bool(row['positive_responses_passed'] and row['white_algebra_passed'] and row['assembled_balance_context_passed']
            and (row['native_calibration_passed'] if native else row['exact_internal_balance_passed'])
            and row.get('fixed_partition_passed', True) and row.get('white_partition_passed', True))
        for name, values in [('green', green), ('fixed', fields), ('white', white), ('comparison', comparison)]:
            if values: np.savez_compressed(target/f'{name}.npz', **values)
        row['native_partition_invariance_qualified'] = False; row['native_mesh_convergence_qualified'] = False
        row['coupled_eigenreference_qualified'] = False
        u = usage()
        if u['elapsed_seconds'] > plan['elapsed_limit_seconds_per_process'] or u['peak_rss_mib'] > plan['peak_rss_limit_mib']:
            raise RuntimeError(f'Predeclared process resource cap exceeded: {u}')
        save(target/'result.json', row); print(label, 'qualified', row['phase_qualified'], 'balance', row['maximum_track_balance_relative'], flush=True)
    finally:
        telemetry = usage(); telemetry['green_sweep_seconds'] = locals().get('green_seconds')
        save(root/f'runs/{label}_resources.json', telemetry)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path); p.add_argument('group', type=int, choices=[51, 61, 98])
    p.add_argument('phase', choices=['native', 'whole', 'equal2', 'equal4', 'equal8', 'thirds']); args = p.parse_args()
    main(args.artifact, args.group, args.phase)

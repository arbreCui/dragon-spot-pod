"""Final full-response verification, including an independent small-matrix action."""
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from calibrate_native_oblique_streaming import read, save
from run_native_oblique_streaming_calibration import digest


def relative(error, scale):
    error, scale = np.broadcast_arrays(abs(error), scale)
    assert np.all(scale >= 0) and np.isfinite(error).all() and np.isfinite(scale).all()
    answer = np.divide(error, scale, out=np.zeros_like(error), where=scale > 0)
    answer[(scale == 0) & (error != 0)] = np.inf
    return float(answer.max())


def measures(d):
    """Build geometry measures from original records, without the action ledger."""
    volume = np.zeros((4, 8)); surface = np.zeros((4, 6))
    for p in range(4):
        weight = d['wei'] * d['wzmu'][p]
        for seg in range(15):
            ix = np.flatnonzero(seg < d['nseg'] - 2)
            np.add.at(volume[p], d['nom'][ix, seg + 1] - 1,
                      weight[ix] * d['planar_widths'][ix, seg] * d['zmu'][p])
        for name in ['entry_surface', 'exit_surface']:
            np.add.at(surface[p], d[name], weight / 2)
    return volume, surface


def explicit_action(d, green, fields, weights, vw, sw, totals):
    """Use explicit sign/polar/orientation matrix products, not the evaluator."""
    q, incoming = fields['q'], fields['inflow']
    x = np.concatenate([q, incoming], axis=2); nc = x.shape[-1]
    value = np.zeros((2, 4, 8, nc)); boundary = np.zeros((2, 4, 6, nc))
    amplitude = np.zeros_like(value); outscale = np.zeros_like(boundary)
    jx = np.zeros((8, nc)); jxscale = np.zeros_like(jx)
    for sign in range(2):
        for p in range(4):
            for o in range(2):
                g = green['volume'][sign, o, p]
                b = green['boundary'][sign, o, p]
                value[sign, p] += g @ x[sign, p]
                amplitude[sign, p] += g @ abs(x[sign, p])
                boundary[sign, p] += b @ x[sign, p]
                outscale[sign, p] += b @ abs(x[sign, p])
                jx += green['jx'][sign, o, p] @ x[sign, p]
                jxscale += green['abs_jx'][sign, o, p] @ abs(x[sign, p])
    vol = weights[:8, None]; surf = weights[8:, None]
    mu = np.sqrt(1 - 1 / d['zmu']**2)
    signed_mu = np.array([1., -1.])[:, None] * mu
    expected = dict(integral=value, boundary=boundary,
                    phi=value.sum(axis=(0, 1)) / vol,
                    jx=jx / vol,
                    jz=(value * signed_mu[:, :, None, None]).sum(axis=(0, 1)) / vol,
                    outgoing=boundary.sum(axis=(0, 1)) / surf)
    scales = dict(integral=amplitude, boundary=outscale,
                  phi=amplitude.sum(axis=(0, 1)) / vol, jx=jxscale / vol,
                  jz=(amplitude * mu[None, :, None, None]).sum(axis=(0, 1)) / vol,
                  outgoing=outscale.sum(axis=(0, 1)) / surf)
    errors = {key: relative(fields[key] - val, scales[key]) for key, val in expected.items()}
    assert max(errors.values()) < 5e-12, errors
    for key in ['phi', 'jx', 'jz', 'outgoing']:
        errors[key + '_scale'] = relative(fields[key + '_scale'] - scales[key], scales[key])
    for name, angle in [('even', np.ones((2, 4))), ('odd', signed_mu)]:
        born = (q * vw[None, :, :, None] * angle[:, :, None, None]).sum(axis=(0, 1, 2))
        inc = (incoming * sw[None, :, :, None] * angle[:, :, None, None]).sum(axis=(0, 1, 2))
        collision = (value * totals[None, None, :, None] * angle[:, :, None, None]).sum(axis=(0, 1, 2))
        out = (boundary * angle[:, :, None, None]).sum(axis=(0, 1, 2))
        scale = (abs(q) * vw[None, :, :, None] * abs(angle[:, :, None, None])).sum(axis=(0, 1, 2))
        scale += (abs(incoming) * sw[None, :, :, None] * abs(angle[:, :, None, None])).sum(axis=(0, 1, 2))
        for key, val in [('birth', born), ('incoming', inc), ('collision', collision), ('outgoing', out), ('defect', born + inc - collision - out)]:
            errors[name + '_' + key] = relative(fields[name + '_' + key] - val, scale)
        errors[name + '_raw_balance'] = relative(born + inc - collision - out, scale)
        assert errors[name + '_raw_balance'] < 1e-10
    assert max(v for k, v in errors.items() if not k.endswith('_raw_balance')) < 5e-12, errors
    positive = (q >= 0).all(axis=(0, 1, 2)) & (incoming >= 0).all(axis=(0, 1, 2))
    assert (fields['integral'][..., positive] >= 0).all() and (fields['boundary'][..., positive] >= 0).all()
    return errors


def compare_reference(fields, reference, weights):
    result = {}
    for key in ['phi', 'jx', 'jz', 'outgoing']:
        error = fields[key] - reference[key]; scale = reference[key + '_scale']
        weight = weights[8:] if key == 'outgoing' else weights[:8]
        result[key + '_component'] = relative(error, scale)
        norm = lambda x: np.sqrt((weight[:, None] * x*x).sum(axis=0))
        result[key + '_weighted'] = relative(norm(error), norm(scale))
    assert max(result.values()) < 5e-12, result
    return result


def probe(root):
    """Calibrate the independent action audit on all frozen exact cases."""
    d = read(root/'inputs/inventory.npz')
    from qualify_native_directional import load_native
    weights = load_native(root/'inputs/track_data.bin')['weights']
    vw, sw = measures(d); rows = []
    for gi, group in enumerate([51, 61, 98]):
        with np.load(root/f'inputs/green_{group}.npz') as f:
            g = {k: f[k] for k in ['iso', 'own', 'jx', 'abs_jx', 'boundary']}
        g['volume'] = g.pop('iso') + g.pop('own')
        green = {k: np.broadcast_to(v, (2, *v.shape)) for k, v in g.items()}
        for phase in ['fixed', 'white']:
            fields = read(root/f'inputs/{phase}_{group}.npz')
            fields['integral'] = fields['iso'] + fields['own']
            errors = explicit_action(d, green, fields, weights, vw, sw, d['group_totals'][gi])
            rows.append(dict(group=group, phase=phase, cases=fields['q'].shape[-1], errors=errors))
    save(root/'verification/verifier_probe.json', dict(rows=rows, all_checks_passed=True))
    print('Independent assembled-action audit: all 648 fixed and 201 white exact cases pass.')


def verify_actions(root):
    d = read(root/'inputs/inventory.npz')
    # The frozen original binary is read only to obtain its stored normalizers.
    from qualify_native_directional import load_native
    weights = load_native(root/'inputs/track_data.bin')['weights']
    vw, sw = measures(d); rows = []
    for H in [1, 20]:
        for nz in [1, 2, 4]:
            family = f'h{H}_n{nz}'
            report = json.loads((root/f'recovery/{family}/result.json').read_text())
            closure = json.loads((root/f'white/{family}/result.json').read_text())
            assert report['order16_recovery_passed'] and closure['order16_white_passed']
            with np.load(root/f'recovery/{family}/coverage.npz') as f:
                np.testing.assert_array_equal(f['multiplicity'], 1)
                np.testing.assert_array_equal(f['original_tracks'], np.arange(11364))
            for q in [8, 16]:
                for gi, group in enumerate([51, 61, 98]):
                    folder = root/f'recovery/{family}/q{q}_g{group}'
                    summary = json.loads((folder/'result.json').read_text())
                    green = read(folder/'green.npz'); fixed = read(folder/'fixed.npz')
                    original = read(root/f'inputs/prepared_{group}.npz')
                    for key in ['q', 'inflow']: np.testing.assert_array_equal(fixed[key], original[key])
                    np.testing.assert_array_equal(green['volume'], green['cell_volume'].sum(axis=-2))
                    assert green['volume'].shape == (2, 2, 4, 8, 14)
                    assert green['cell_volume'].shape == (2, 2, 4, 8, nz, 14)
                    errors = explicit_action(d, green, fixed, weights, vw, sw, d['group_totals'][gi])
                    row = dict(family=family, order=q, group=group, fixed_action=errors,
                               recovery_passed=summary['recovery_passed'])
                    if q == 16:
                        row['fixed_reference'] = compare_reference(fixed, read(root/f'inputs/fixed_{group}.npz'), weights)
                    if summary['recovery_passed']:
                        white = read(root/f'white/{family}/q{q}_g{group}/fields.npz')
                        tags = np.array(json.loads((root/f'inputs/cases_{group}.json').read_text()))
                        ix = np.flatnonzero((tags == 'angular_volume_white') | (tags == 'pair_white'))
                        np.testing.assert_array_equal(white['target_indices'], ix)
                        np.testing.assert_array_equal(white['q'], original['q'][..., ix])
                        assert len(ix) == 67
                        for sign in range(2):
                            for p in range(4): np.testing.assert_array_equal(white['inflow'][sign, p], white['white_amplitudes'])
                        # Assemble the common six-surface return and volume RHS
                        # directly from all original Green coordinates.
                        tbb = green['boundary'][..., 8:].sum(axis=(0, 1, 2)) / weights[8:, None]
                        rhs = np.zeros((6, 67))
                        for sign in range(2):
                            for p in range(4):
                                for o in range(2): rhs += green['boundary'][sign, o, p, :, :8] @ white['q'][sign, p]
                        rhs /= weights[8:, None]
                        matrix = np.eye(6) - tbb
                        amp = white['white_amplitudes']; scale = abs(rhs).max(axis=0)
                        algebra = dict(return_matrix=relative(white['tbb'] - tbb, abs(tbb).max()),
                                       rhs=relative(white['white_rhs'] - rhs, scale),
                                       inverse=relative(matrix @ white['boundary_inverse'] - np.eye(6), 1.),
                                       solve=relative(matrix @ amp - rhs, scale),
                                       closure=relative(white['outgoing'] - amp, abs(amp).max(axis=0)))
                        assert max(algebra.values()) < 5e-12 and white['boundary_inverse'].min() >= 0
                        row['white_algebra'] = algebra
                        row['white_action'] = explicit_action(d, green, white, weights, vw, sw, d['group_totals'][gi])
                        if q == 16: row['white_reference'] = compare_reference(white, read(root/f'inputs/white_{group}.npz'), weights)
                    else:
                        assert q == 8
                        row['white_not_run'] = 'order-8 recovery failed; retained as diagnostic'
                    rows.append(row)
    save(root/'verification/assembled_action_audit.json', dict(rows=rows,
         geometric_volume_vs_stored_relative=relative(2*vw.sum(axis=0)-weights[:8], weights[:8]),
         geometric_surface_vs_stored_relative=relative(2*sw.sum(axis=0)-weights[8:], weights[8:]),
         all_checks_passed=True))
    return rows


def main(root, project):
    tick = time.perf_counter(); plan = json.loads((root/'plan.json').read_text())
    assert plan['execution_admitted'] and len(plan['processes']) == 552
    reference_max = 0.; track_configs = 0; native_evaluations = 0; maxima = {8: {}, 16: {}}
    coverage = np.zeros((4, 2, 3, 11364), np.uint8)
    for p in range(4):
        report = json.loads((root/f'reference/p{p}.json').read_text()); assert report['passed']
        with np.load(root/f'reference/p{p}.npz') as f:
            np.testing.assert_array_equal(f['original_tracks'], np.arange(11364)); np.testing.assert_array_equal(f['multiplicity'], 1)
            assert f['errors'].shape == (11364, 2, 3, 2) and np.isfinite(f['errors']).all()
            assert f['errors'].max() == report['independent_reference_relative'] < 5e-12
            reference_max = max(reference_max, float(f['errors'].max()))
    expected_jobs = ['test_kernel', 'test_action'] + [f'reference_p{p}' for p in range(4)]
    for c in plan['processes']:
        folder = root/'analysis'/c['id']; r = json.loads((folder/'result.json').read_text())
        assert r['case'] == c and r['all_gates_passed'] and not (folder/'failed.json').exists()
        n = c['stop'] - c['first']; assert n == r['original_index_count'] and 0 < n <= 512
        coverage[c['polar'], [1., 20.].index(c['H']), [1, 2, 4].index(c['nz']), c['first']:c['stop']] += 1
        labels = {f'o{o}_m{s}_q{q}' for o in [1, -1] for s in [-1, 1] for q in [8, 16]}
        assert {x['label'] for x in r['configurations']} == labels and len(r['configurations']) == 8
        for row in r['configurations']:
            assert row['passed'] and row['finite'] and row['original_records'] == n
            assert min(row['minimum_angle'], row['minimum_integral']) >= 0 and row['shared_face_abs_error'] == 0
            for key, value in row.items():
                if key.endswith('_relative'): maxima[row['order']][key] = max(maxima[row['order']].get(key, 0.), value)
            track_configs += n*3; native_evaluations += n*3*14
        expected_jobs.append(c['id'])
    np.testing.assert_array_equal(coverage, 1)
    assert track_configs == plan['scientific_track_group_configurations'] == 6545664
    assert native_evaluations == plan['native_input_evaluations'] == 91639296
    expected_jobs += [f'{phase}_h{H}_n{n}' for phase in ['recover', 'white'] for H in [1, 20] for n in [1, 2, 4]]
    usage = []; watchdogs = []
    for base in [root, root/'replay']:
        commands = json.loads((base/'runs/commands.json').read_text())
        assert [x[0] for x in commands['commands']] == expected_jobs
        assert all(v == '1' for v in commands['environment'].values())
        for job in expected_jobs:
            w = json.loads((base/f'runs/{job}_watchdog.json').read_text()); watchdogs.append(w)
            assert w['returncode'] == 0 and w['limit_failure'] is None
            assert w['elapsed_seconds'] < 600 and w['sampled_peak_rss_mib'] < 512
            if not job.startswith('test_'):
                u = json.loads((base/f'runs/{job}_resources.json').read_text()); usage.append(u)
                assert u['elapsed_seconds'] < 600 and u['peak_rss_mib'] < 512
        for name, count in [('test_kernel', 8), ('test_action', 3)]:
            log = (base/f'runs/{name}.log').read_text()
            assert f'Ran {count} tests' in log and log.rstrip().endswith('OK')
    byte_files = {}; scientific = []
    for folder in ['reference', 'analysis', 'recovery', 'white']:
        scientific += sorted(str(p.relative_to(root)) for p in (root/folder).rglob('*') if p.is_file())
    receipts = sorted((root/'replay/receipts').glob('*.json')); assert len(receipts) == len(expected_jobs)-2
    for file in receipts:
        r = json.loads(file.read_text()); assert r['all_byte_identical']
        for path, info in r['files'].items():
            assert path not in byte_files
            assert digest(root/path) == digest(root/'replay'/path) == info['sha256']
            assert (root/path).stat().st_size == (root/'replay'/path).stat().st_size == info['bytes']
            byte_files[path] = info
    assert sorted(byte_files) == sorted(scientific)
    audits = []
    for H in [1, 20]:
        for n in [1, 2, 4]:
            family = f'h{H}_n{n}'; r = json.loads((root/f'verification/{family}/result.json').read_text())
            assert r['all_checks_passed'] and r['all_original_records_once'] and r['raw_files'] == 736
            assert r['elapsed_seconds'] < 600 and r['peak_rss_mib'] < 512
            w = json.loads((root/f'runs/audit_{family}_watchdog.json').read_text())
            assert w['returncode'] == 0 and w['limit_failure'] is None and w['sampled_peak_rss_mib'] < 512 and w['elapsed_seconds'] < 600
            audits.append(r); watchdogs.append(w)
    assert sum(r['track_group_configurations'] for r in audits) == track_configs
    assert sum(r['input_evaluations'] for r in audits) == plan['total_input_evaluations_with_controls'] == 104730624
    actions = verify_actions(root)
    identities = {}
    for name, base in [('protected_inputs_before.json', project), ('prepared_inputs.json', root),
                       ('execution_inputs.json', root), ('audit_source_inputs.json', root),
                       ('audit_runner_inputs.json', root), ('verification_source_inputs.json', root),
                       ('replay_inputs.json', root)]:
        items = json.loads((root/name).read_text())
        for path, sha in items.items(): assert digest(base/path) == sha, (name, path)
        identities[name] = len(items)
    assert json.loads((root/'preparation_changes.json').read_text()) == []
    prior = json.loads((root/'prior_artifacts.json').read_text()); entries = 0
    for name, sha in prior.items():
        folder = project/'validation/artifacts'/name; assert digest(folder/'result.sha256') == sha
        for line in (folder/'result.sha256').read_text().splitlines():
            h, path = line.split('  ', 1); assert digest(folder/path) == h, (name, path); entries += 1
    result = dict(original_tracks=11364, batch_processes=552, track_group_configurations=track_configs,
        native_input_evaluations=native_evaluations, input_evaluations_with_controls=104730624,
        raw_response_files=sum(r['raw_files'] for r in audits), byte_identical_scientific_files=len(byte_files),
        tests_per_pass=11, independent_reference_relative=reference_max, gates_by_order=maxima,
        maximum_worker_rss_mib=max(u['peak_rss_mib'] for u in usage), maximum_worker_seconds=max(u['elapsed_seconds'] for u in usage),
        maximum_audit_rss_mib=max(r['peak_rss_mib'] for r in audits), maximum_audit_seconds=max(r['elapsed_seconds'] for r in audits),
        maximum_watchdog_seconds=max(w['elapsed_seconds'] for w in watchdogs),
        independent_primitive_relative=max(r['independent_worst_primitive_relative'] for r in audits),
        independent_literal_track_relative=max(r['worst_literal_track_relative'] for r in audits),
        independent_source_assembly_relative=max(r['whole_track_source_assembly_relative'] for r in audits),
        original_coordinate_recovery_passed=True, common_white_algebra_passed=True,
        assembled_action_rows=len(actions), identities=identities, prior_artifacts=len(prior), prior_manifest_entries=entries,
        manufactured_zero_gradient_operator_qualified=True, original_native_table_partition_equality_qualified=False,
        physical_axial_boundary_qualified=False, full_axial_source_space_qualified=False,
        coupled_scattering_fission_eigenproblem_qualified=False, production_changed=False,
        elapsed_seconds=time.perf_counter()-tick, peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    assert result['elapsed_seconds'] < 600 and result['peak_rss_mib'] < 512
    save(root/'verification/result.json', result); print(json.dumps(result, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path); p.add_argument('project', type=Path)
    p.add_argument('--probe', action='store_true')
    a = p.parse_args()
    if a.probe: probe(a.artifact.resolve())
    else: main(a.artifact.resolve(), a.project.resolve())

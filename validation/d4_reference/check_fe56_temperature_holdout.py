"""Offline leave-one-temperature-out check; no material or transport solve."""
import argparse
import json
from pathlib import Path
import runpy
import numpy as np
from audit_fe56_temperature_interpolation import ROOT, RUN, PAIR, weights, mix_nodes


def check():
    audit_file = ROOT/'validation/artifacts/d4a-fe56-temperature-interpolation-audit-20260929/analysis.json'
    api = runpy.run_path(str(RUN/'run_once.py'), run_name='read_only')
    sha, verify, decode, nr = (api[k] for k in ('sha', 'verify', 'decode', 'nr'))
    assert sha(audit_file) == '842368cd41de84110a0297c52078135ab8d8e2be41414d37e6404cb93d29490f'
    pins = json.loads(audit_file.read_text())['sources']
    verify(pins)
    lib = decode(PAIR/'candidate/dragr/tape30', True)
    temperatures = nr.data(lib, ('Fe56', 'TEMPERATURE'))
    matrices, totals = [], []
    for index in range(1, 6):
        prefix = ('Fe56', f'SUBTMP{index:04d}')
        fields = {k[2]: v[1] for k, v in lib.items() if len(k) == 3 and k[:2] == prefix}
        matrices.append(nr.cpo_scatter(fields, 0, 370).astype('f4'))
        totals.append(np.asarray(fields['NTOT0'], dtype='f4'))
    rows = []
    # Interior nodes only: neither candidate method is extrapolating.
    for held in (1, 2, 3):
        indices = [i for i in range(5) if i != held]
        table = [temperatures[i] for i in indices]
        truth = matrices[held].astype('f8')
        for order in (1, 3):
            w = weights(table, temperatures[held], order)
            guess = mix_nodes([matrices[i] for i in indices], w).astype('f8')
            total = mix_nodes([totals[i] for i in indices], w).astype('f8')
            error = np.abs(guess - truth)
            scope = {}
            for name, columns in (('all_370', slice(None)), ('G282_370', slice(281, 370))):
                reference = truth[:, columns]
                difference = error[:, columns]
                norm = np.abs(reference).sum(axis=0)
                assert np.all(norm > 0)
                scope[name] = dict(
                    unweighted_matrix_relative_l1=float(difference.sum()/np.abs(reference).sum()),
                    maximum_column_relative_l1=float((difference.sum(axis=0)/norm).max()),
                    maximum_element_absolute_error_barn=float(difference.max()),
                    negative_elements=int((guess[:, columns] < 0).sum()))
            target = totals[held].astype('f8')
            assert np.all(target > 0)
            rows.append(dict(held_temperature_K=temperatures[held], order_in_sqrt_T=order,
                retained_temperatures_K=table, weights=[float(v) for v in w], scopes=scope,
                maximum_total_relative_error=float((abs(total-target)/target).max())))
    verify(pins)
    return dict(status='DIAGNOSTIC_ONLY_NO_ACCURACY_ACCEPTANCE', rows=rows,
        source_audit_sha256=sha(audit_file), script_sha256=sha(__file__),
        native_engines_started=0, production_files_modified=0,
        limits=['Held-out intervals are wider than the original table intervals.',
                'These errors are not bounds for the actual 748.15/893.15 K interpolations.',
                'Matrix norms are unweighted, not flux/importance weighted, and not a k estimate.',
                'Infinite-dilution Fe56 only; no new self-shielding or other isotope validation.',
                'No empirical threshold, clipping or production method selection is made.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    result = check()
    with parser.parse_args().output.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(result, indent=2))

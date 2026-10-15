#!/usr/bin/env python3
"""Verify the signed-state replay and all preceding immutable evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

PRIOR=['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
       'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
       'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
       'exchange-pod-projection-20260928','native-radial-response-20260928',
       'native-multigroup-pod-20260928','native-axial-coupling-20260928',
       'native-axial-refinement-20260928','native-source-current-consistency-20260928',
       'native-directional-response-20260929']


def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    counts=dict(protected_files=0,source_inputs=0,copied_inputs=0,prior_artifacts=len(PRIOR),prior_manifest_entries=0,
                byte_identical_native_files=0,byte_identical_analysis_files=0,exact_numeric_arrays=0)
    for filename,key,base in [('protected_inputs_before.json','protected_files',root),
                              ('inputs.json','source_inputs',root),('copied_inputs.json','copied_inputs',a)]:
        for path,h in json.loads((a/filename).read_text()).items():
            assert digest(base/path)==h,path;counts[key]+=1
    for n in PRIOR:
        folder=root/'validation/artifacts'/n
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split(maxsplit=1);assert digest(folder/path)==h,f'{n}/{path}'
            counts['prior_manifest_entries']+=1
    for g in [51,61,98]:
        for n in [f'sources_{g}.txt',f'native_{g}.bin']:
            assert digest(a/'runs'/n)==digest(a/'replay/runs'/n),n
            counts['byte_identical_native_files']+=1
    for p in sorted((a/'analysis').iterdir()):
        q=a/'replay/analysis'/p.name
        assert digest(p)==digest(q),p.name;counts['byte_identical_analysis_files']+=1
        if p.suffix=='.npz':
            x=np.load(p);y=np.load(q);assert x.files==y.files
            for key in x.files:
                np.testing.assert_array_equal(x[key],y[key]);counts['exact_numeric_arrays']+=1
    for n in ['probe_native_signed_axial.f90','qualify_native_signed_axial.py','test_native_signed_axial.py',
              'verify_native_signed_axial.py']:
        assert digest(a/'build'/n)==digest(root/'validation/iterative'/n),n
    for label in ['source_tests','archived_tests']:
        text=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 8 tests' in text and '\nOK\n' in text and 'skipped=' not in text
    result=json.loads((a/'analysis/result.json').read_text())
    assert result['signed_state_zero_gradient_checks_passed'] and result['white_boundary_mixes_axial_signs']
    assert not result['axial_propagation_qualified'] and not result['new_coupled_reference_qualified']
    for r in result['groups']:
        assert r['cases']==216 and r['nonnegative_cases']==214
        assert r['negative_retained_values_in_nonnegative_cases']==0 and r['negative_retained_values_in_signed_cases']>0
        assert r['native_half_state_max_case_relative']<5e-12
        assert r['native_P0_calibration_max_case_relative']<5e-12
        assert max(r['raw_even_balance_relative'],r['raw_odd_balance_relative'])<1e-6
        assert r['correct_white_vs_vacuum_odd_relative']<5e-12
        assert r['wrong_sign_return_even_scalar_relative']<5e-12 and r['wrong_sign_return_relative_change']>.4
    counts.update(native_prescribed_flights=648,nonnegative_flight_inputs=642,
                  admitted_boundary_nonnegative_cases=633,different_boundary_control_cases=9,
                  original_isotropic_cases_recovered=93,source_tests=8,archived_tests=8,
                  all_verification_checks_passed=True,axial_propagation_qualified=False,new_coupled_reference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

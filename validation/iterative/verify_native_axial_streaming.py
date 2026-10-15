#!/usr/bin/env python3
"""Verify immutable inputs, exact replay and reported streaming gate outcomes."""
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
       'native-directional-response-20260929','native-signed-axial-state-20260929']
SOURCES=['native_axial_streaming.py','qualify_native_axial_streaming.py',
         'test_native_axial_streaming.py','audit_native_axial_streaming_segments.py',
         'verify_native_axial_streaming.py']


def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,artifact):
    root=Path(root);a=Path(artifact)
    counts=dict(protected_files=0,source_inputs=0,copied_inputs=0,prior_artifacts=len(PRIOR),
                prior_manifest_entries=0,byte_identical_analysis_files=0,exact_numeric_arrays=0)
    for filename,key,base in [('protected_inputs_before.json','protected_files',root),
                              ('inputs.json','source_inputs',root),('copied_inputs.json','copied_inputs',a)]:
        for path,h in json.loads((a/filename).read_text()).items():
            assert digest(base/path)==h,path;counts[key]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split(maxsplit=1);assert digest(folder/path)==h,f'{name}/{path}'
            counts['prior_manifest_entries']+=1
    for p in sorted((a/'analysis').iterdir()):
        q=a/'replay/analysis'/p.name
        assert digest(p)==digest(q),p.name;counts['byte_identical_analysis_files']+=1
        if p.suffix=='.npz':
            with np.load(p) as x,np.load(q) as y:
                assert x.files==y.files
                for key in x.files:
                    np.testing.assert_array_equal(x[key],y[key]);counts['exact_numeric_arrays']+=1
    for name in SOURCES:
        assert digest(a/'build'/name)==digest(root/'validation/iterative'/name),name
    for label in ['source_tests','archived_tests']:
        text=(a/'runs'/f'{label}.log').read_text()
        assert 'Ran 13 tests' in text and '\nOK\n' in text and 'skipped=' not in text
    plan=json.loads((a/'plan.json').read_text());limits=plan['limits']
    result=json.loads((a/'analysis/result.json').read_text())
    assert len(result['primitive_controls'])==384 and len(result['zero_gradient'])==6
    primitive=all(max(r['dense_relative'],r['native_periodic_constant_relative'])<limits['dense_primitive_relative']
                  for r in result['primitive_controls'])
    assert result['primitive_controls_passed']==primitive
    for r in result['zero_gradient']:
        passed=max(r['half_state_max_relative'],r['P0_max_case_relative'])<limits['native_action_relative']
        assert r['native_action_passed']==passed
    zero=all(r['native_action_passed'] for r in result['zero_gradient'] if r['kernel']=='native')
    assert result['native_zero_gradient_passed']==zero
    assert len(result['cases'])==48
    expected={(g,k,n,b) for g in [51,61,98] for k in ['exact','native'] for n in [1,2,4,8] for b in ['vacuum','white']}
    assert {(r['group'],r['kernel'],r['n'],r['boundary']) for r in result['cases']}==expected
    for r in result['cases']:
        assert r['cases']==14*r['n']+18
        with np.load(a/f"analysis/{r['kernel']}_{r['group']}_{r['n']}_{r['boundary']}.npz") as f:
            assert all(np.isfinite(f[k]).all() for k in f.files)
            for name,key in [('even_global_balance_relative','even_global_relative'),('odd_global_balance_relative','odd_global_relative'),
                             ('even_cell_balance_relative','even_cell_relative'),('odd_cell_balance_relative','odd_cell_relative')]:
                assert r[name]==float(f[key].max()),name
            for name,key in [('min_white_inverse','white_inverse'),('min_incoming','incoming'),
                             ('min_half_flux','half_flux'),('min_half_outgoing','half_outgoing')]:
                assert r[name]==float(f[key].min()),name
            positive=all(float(f[k].min())>=0 for k in ['green','white_inverse','incoming','half_flux','half_outgoing'])
        positive=positive and all(x>=0 for x in r['primitive_minima'].values()) and r['min_response']>=0
        global_limit=limits['exact_raw_balance_relative'] if r['kernel']=='exact' else limits['lifted_global_balance_relative']
        cell_limit=limits['exact_raw_balance_relative'] if r['kernel']=='exact' else limits['lifted_cell_balance_relative']
        assert r['positivity_passed']==positive
        assert r['global_balance_passed']==(max(r['even_global_balance_relative'],r['odd_global_balance_relative'])<global_limit)
        assert r['cell_balance_passed']==(max(r['even_cell_balance_relative'],r['odd_cell_balance_relative'])<cell_limit)
        assert r['face_and_boundary_passed']==(r['face_streaming_consistency_absolute']<limits['face_continuity_absolute'] and r['radial_boundary_relative']<5e-12)
    finite=all(all(r[k] for k in ['positivity_passed','global_balance_passed','cell_balance_passed','face_and_boundary_passed'])
               for r in result['cases'] if r['kernel']=='native')
    assert result['native_finite_mesh_response_passed']==finite
    assert len(result['mesh_checks'])==6
    for r in result['mesh_checks']:
        assert r['coarse_n']==4 and r['fine_n']==8
        assert r['passed']==(max(*r['flux_relative'],*r['axial_escape_relative'])<limits['last_mesh_flux_and_axial_escape_relative'])
    mesh=all(r['passed'] for r in result['mesh_checks'] if r['kernel']=='native')
    assert result['mesh_convergence_passed']==mesh
    assert result['new_coupled_eigenreference_qualified'] is False
    segment=json.loads((a/'analysis/segment_balance.json').read_text())
    assert len(segment['records'])==24
    assert all(r['segment_polar_samples']==439344 for r in segment['records'])
    counts.update(prescribed_finite_mesh_cases=sum(r['cases'] for r in result['cases']),
                  native_zero_gradient_replayed_cases=648,exact_zero_gradient_companion_cases=648,
                  dense_primitive_controls=384,source_tests=13,archived_tests=13,
                  all_verification_checks_passed=True,primitive_controls_passed=primitive,
                  native_zero_gradient_passed=zero,native_finite_mesh_response_passed=finite,
                  mesh_convergence_passed=mesh,new_coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

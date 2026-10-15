#!/usr/bin/env python3
"""Verify the bounded refinement evidence without turning failed gates into passes."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native,relative
from native_axial_streaming_refinement import mesh_difference

PRIOR=['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
       'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
       'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
       'exchange-pod-projection-20260928','native-radial-response-20260928',
       'native-multigroup-pod-20260928','native-axial-coupling-20260928',
       'native-axial-refinement-20260928','native-source-current-consistency-20260928',
       'native-directional-response-20260929','native-signed-axial-state-20260929',
       'native-axial-streaming-20260929','native-axial-streaming-refinement-20260929']
SOURCES=['native_axial_streaming_refinement.py','qualify_native_streaming_refinement.py',
         'test_native_streaming_refinement.py','verify_native_streaming_refinement.py']


def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,a):
    counts=dict(protected_files=0,source_inputs=0,copied_inputs=0,prior_artifacts=len(PRIOR),
                prior_manifest_entries=0,byte_identical_analysis_files=0,exact_numeric_arrays=0)
    for name,key,base in [('protected_inputs_before.json','protected_files',root),
                          ('inputs.json','source_inputs',root),('copied_inputs.json','copied_inputs',a)]:
        for path,h in json.loads((a/name).read_text()).items():
            assert digest(base/path)==h,path;counts[key]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split(maxsplit=1);assert digest(folder/path)==h,f'{name}/{path}'
            counts['prior_manifest_entries']+=1
    files=sorted(p for p in (a/'analysis').iterdir() if p.is_file())
    assert [p.name for p in files]==sorted(p.name for p in (a/'replay/analysis').iterdir() if p.is_file())
    for p in files:
        q=a/'replay/analysis'/p.name;assert digest(p)==digest(q),p.name
        counts['byte_identical_analysis_files']+=1
        if p.suffix=='.npz':
            with np.load(p) as x,np.load(q) as y:
                assert x.files==y.files
                for k in x.files:
                    np.testing.assert_array_equal(x[k],y[k]);counts['exact_numeric_arrays']+=1
    for name in SOURCES:assert digest(a/'build'/name)==digest(root/'validation/iterative'/name)
    for label,n in [('source_tests',6),('archived_tests',6),('primitive_tests',13)]:
        log=(a/'runs'/f'{label}.log').read_text()
        assert f'Ran {n} tests' in log and '\nOK\n' in log and 'skipped=' not in log
    plan=json.loads((a/'plan.json').read_text());lim=plan['limits']
    result=json.loads((a/'analysis/result.json').read_text());d=load_native(a/'inputs/track_data.bin')
    # A separately implemented expanded-matrix path completed all 16/32
    # fields and one 64-cell field before its resource cap. Its partial
    # scientific state is retained and provides an additional code-path check.
    previous=root/plan['preceding_incomplete_attempt']/'analysis'
    crosschecked=0;cross_error=0.
    for p in sorted(previous.glob('*.npz')):
        with np.load(p) as old,np.load(a/'analysis'/p.name) as new:
            for key in ['green','phi','jz','half_flux','half_outgoing','incoming','face_current','face_second_moment','white_inverse','axial_escape']:
                error=relative(new[key],old[key]);cross_error=max(cross_error,error)
                assert error<plan['calibration_limit'],(p.name,key,error)
        crosschecked+=1
    counts.update(expanded_matrix_partial_fields_crosschecked=crosschecked,
                  expanded_matrix_crosscheck_max_relative=cross_error)
    assert len(result['calibration'])==48 and len(result['cases'])==84
    expected={(g,k,n,b) for g in plan['groups'] for k in plan['kernels']
              for n in plan['calibration_meshes']+plan['refinement_meshes'] for b in plan['radial_boundaries']}
    assert {(r['group'],r['kernel'],r['n'],r['boundary']) for r in result['cases']}==expected
    def filename(r,n=None):return f"{r['kernel']}_{r['group']}_{r['n'] if n is None else n}_{r['boundary']}.npz"
    for r in result['calibration']:
        with np.load(a/'analysis'/filename(r)) as f,np.load(a/'inputs/coarse'/filename(r)) as old:
            for key,value in r['errors'].items():
                expected=old[key] if key in ['green','white_inverse'] else old[key][...,-2:]
                assert relative(f[key],expected)==value,key
        assert r['passed']==(max(r['errors'].values())<plan['calibration_limit'])
    assert result['coarse_calibration_passed']==all(r['passed'] for r in result['calibration'])
    for r in result['cases']:
        assert r['cases']==2
        with np.load(a/'analysis'/filename(r)) as f:
            assert all(np.isfinite(f[k]).all() for k in f.files)
            for report,key in [('even_global_balance_relative','even_global_relative'),('odd_global_balance_relative','odd_global_relative'),
                               ('even_cell_balance_relative','even_cell_relative'),('odd_cell_balance_relative','odd_cell_relative'),
                               ('min_white_inverse','white_inverse'),('min_incoming','incoming'),('min_half_flux','half_flux'),('min_half_outgoing','half_outgoing')]:
                observed=float(f[key].min()) if report.startswith('min_') else float(f[key].max())
                assert r[report]==observed,report
            np.testing.assert_array_equal(r['axial_escape'],f['axial_escape'])
            positive=all(float(f[k].min())>=0 for k in ['green','white_inverse','incoming','half_flux','half_outgoing'])
        positive=positive and r['min_response']>=0 and all(x>=0 for x in r['primitive_minima'].values())
        assert r['positivity_passed']==positive
        gl=lim['exact_raw_balance_relative'] if r['kernel']=='exact' else lim['lifted_global_balance_relative']
        cl=lim['exact_raw_balance_relative'] if r['kernel']=='exact' else lim['lifted_cell_balance_relative']
        assert r['global_balance_passed']==(max(r['even_global_balance_relative'],r['odd_global_balance_relative'])<gl)
        assert r['cell_balance_passed']==(max(r['even_cell_balance_relative'],r['odd_cell_balance_relative'])<cl)
        assert r['face_and_boundary_passed']==(r['face_streaming_consistency_absolute']<lim['face_continuity_absolute'] and r['radial_boundary_relative']<5e-12)
    assert len(result['mesh_checks'])==48
    for r in result['mesh_checks']:
        with np.load(a/'analysis'/filename(r,r['coarse_n'])) as c,np.load(a/'analysis'/filename(r,r['fine_n'])) as f:
            flux,escape=mesh_difference(c,f,d['weights'][:8],plan['height_cm'])
        np.testing.assert_array_equal(r['flux_relative'],flux);np.testing.assert_array_equal(r['axial_escape_relative'],escape)
        assert r['passed']==(max(*flux,*escape)<lim['last_mesh_flux_and_axial_escape_relative'])
    finite=all(all(r[k] for k in ['positivity_passed','global_balance_passed','cell_balance_passed','face_and_boundary_passed']) for r in result['cases'])
    mesh=all(r['passed'] for r in result['mesh_checks'] if r['fine_n']==64)
    assert result['finite_mesh_response_passed']==finite and result['final_mesh_convergence_passed']==mesh
    assert result['prescribed_source_refinement_passed']==(result['coarse_calibration_passed'] and finite and mesh)
    assert result['new_coupled_eigenreference_qualified'] is False
    assert len(result['segment_balance'])==42
    assert all(r['segment_polar_samples']==439344 for r in result['segment_balance'])
    resources={}
    for folder in ['runs','replay/runs']:
        usage=json.loads((a/folder/'resource_usage.json').read_text());resources[folder]=usage
        assert usage['peak_rss_mib']<=plan['peak_rss_limit_mib'] and usage['elapsed_seconds']<=plan['elapsed_limit_seconds_per_execution']
    counts.update(coarse_calibration_comparisons=48,coarse_heldout_solves=96,new_refined_solves=72,
                  source_tests=6,archived_tests=6,frozen_primitive_tests=13,resource_usage=resources,
                  all_verification_checks_passed=True,coarse_calibration_passed=result['coarse_calibration_passed'],
                  finite_mesh_response_passed=finite,final_mesh_convergence_passed=mesh,
                  prescribed_source_refinement_passed=result['prescribed_source_refinement_passed'],
                  new_coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as out:json.dump(counts,out,indent=2);out.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

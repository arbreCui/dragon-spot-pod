#!/usr/bin/env python3
"""Check analytic-slab evidence, exact replay and unchanged prior artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from analytic_axial_slab import errors_against_reference,adjacent_errors

PRIOR=['d4a-map6-axial-repeatability-20260928','d4a-map6-axial-mesh24-20260928',
       'd4a-map6-frozen-physical-basis-20260928','d4a-map6-physical-column-trace-20260928',
       'coupled-reference-nullspace-20260928','coupled-reference-heterogeneous-20260928',
       'exchange-pod-projection-20260928','native-radial-response-20260928',
       'native-multigroup-pod-20260928','native-axial-coupling-20260928',
       'native-axial-refinement-20260928','native-source-current-consistency-20260928',
       'native-directional-response-20260929','native-signed-axial-state-20260929',
       'native-axial-streaming-20260929','native-axial-streaming-refinement-20260929',
       'native-axial-streaming-refinement-compact-20260929']
SOURCES=['analytic_axial_slab.py','qualify_analytic_axial_slab.py','test_analytic_axial_slab.py',
         'analyze_analytic_axial_slab.py','plot_analytic_axial_slab.py','verify_analytic_axial_slab.py']


def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,a):
    counts=dict(protected_files=0,source_inputs=0,copied_inputs=0,prior_artifacts=len(PRIOR),prior_manifest_entries=0,
                byte_identical_analysis_files=0,exact_numeric_arrays=0)
    for name,key,base in [('protected_inputs_before.json','protected_files',root),('inputs.json','source_inputs',root),('copied_inputs.json','copied_inputs',a)]:
        for path,h in json.loads((a/name).read_text()).items():assert digest(base/path)==h,path;counts[key]+=1
    for name in PRIOR:
        folder=root/'validation/artifacts'/name
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split(maxsplit=1);assert digest(folder/path)==h,f'{name}/{path}';counts['prior_manifest_entries']+=1
    files=sorted((a/'analysis').iterdir())
    assert [p.name for p in files]==sorted(p.name for p in (a/'replay/analysis').iterdir())
    for p in files:
        q=a/'replay/analysis'/p.name;assert digest(p)==digest(q),p.name;counts['byte_identical_analysis_files']+=1
        if p.suffix=='.npz':
            with np.load(p) as x,np.load(q) as y:
                assert x.files==y.files
                for key in x.files:
                    np.testing.assert_array_equal(x[key],y[key]);counts['exact_numeric_arrays']+=1
    for name in SOURCES:assert digest(root/'validation/iterative'/name)==digest(a/'build'/name),name
    for label in ['source_tests','archived_tests']:
        log=(a/'runs'/f'{label}.log').read_text();assert 'Ran 11 tests' in log and '\nOK\n' in log and 'skipped=' not in log
    plan=json.loads((a/'plan.json').read_text());lim=plan['limits'];data=json.loads((a/'analysis/result.json').read_text())
    assert len(data['cases'])==78 and len(data['adjacent'])==65 and len(data['finest'])==13
    assert {(r['case'],r['n']) for r in data['cases']}=={(r['id'],n) for r in plan['cases'] for n in plan['meshes']}
    for row in data['cases']:
        with np.load(a/f"analysis/{row['case']}_{row['n']}.npz") as f:
            assert all(np.isfinite(f[k]).all() for k in f.files)
            for key,value in errors_against_reference(f).items():np.testing.assert_array_equal(row[key],value)
            assert row['minimum_angular']==float(f['angular'].min())
            assert row['matrix_residual_relative']==float(np.max(abs(f['matrix_residual']))/plan['source_per_direction'])
            # Independently confirm the saved solve and global current ledger.
            np.testing.assert_array_equal(f['matrix']@f['angular'].ravel()-plan['source_per_direction'],f['matrix_residual'])
            total=row['total'];scatter=next(c['scattering'] for c in plan['cases'] if c['id']==row['case'])
            balance=abs(f['escape'].sum()+(total-scatter)*plan['height_cm']/row['n']*f['phi'].sum()-plan['source_per_direction']*plan['height_cm'])/(plan['source_per_direction']*plan['height_cm'])
            assert row['raw_global_balance_relative']==float(balance)
        assert row['matrix_passed']==(row['matrix_residual_relative']<lim['matrix_residual_relative'])
        assert row['balance_passed']==(row['raw_global_balance_relative']<lim['raw_global_balance_relative'])
        assert row['positivity_passed']==(row['minimum_angular']>=lim['minimum_flux'])
        assert row['analytic_passed']==all(row['analytic'][k]<lim['analytic_identities_relative'] for k in ['even_identity_relative','odd_identity_relative','boundary_relative','global_balance_relative','cell_quadrature_relative'])
    for row in data['adjacent']:
        with np.load(a/f"analysis/{row['case']}_{row['coarse_n']}.npz") as c,np.load(a/f"analysis/{row['case']}_{row['fine_n']}.npz") as f:
            for key,value in adjacent_errors(c,f).items():np.testing.assert_array_equal(row[key],value)
            true=errors_against_reference(f)
        adjacent=max(row['scalar_adjacent_relative'],row['total_escape_adjacent_relative'])<plan['diagnostic_threshold']
        accurate=max(true['scalar_true_relative'],true['total_escape_true_relative'])<plan['diagnostic_threshold']
        assert row['adjacent_pair_below_one_percent']==adjacent and row['true_fine_below_one_percent']==accurate
        assert row['false_admission']==(adjacent and not accurate)
    assert data['false_admission_count']==sum(r['false_admission'] for r in data['adjacent'])
    analytic=all(r['analytic_passed'] for r in data['cases'])
    discrete=all(r['matrix_passed'] and r['balance_passed'] and r['positivity_passed'] for r in data['cases'])
    assert data['analytic_reference_checks_passed']==analytic and data['discrete_algebra_balance_positivity_passed']==discrete
    assert data['manufactured_implementation_qualified']==(analytic and discrete)
    assert data['native_mesh_convergence_qualified'] is False and data['coupled_eigenreference_qualified'] is False
    identity=json.loads((a/'analysis/interior_identity.json').read_text());assert len(identity['records'])==78
    resource_usage={}
    for directory in ['runs','replay/runs']:
        u=json.loads((a/directory/'resource_usage.json').read_text());resource_usage[directory]=u
        assert u['peak_rss_mib']<=plan['peak_rss_limit_mib'] and u['elapsed_seconds']<=plan['elapsed_limit_seconds']
    counts.update(prescribed_slab_cases=13,discrete_mesh_solves=78,adjacent_comparisons=65,
                  source_tests=11,archived_tests=11,false_admission_count=data['false_admission_count'],
                  resource_usage=resource_usage,all_verification_checks_passed=True,
                  manufactured_implementation_qualified=analytic and discrete,
                  native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

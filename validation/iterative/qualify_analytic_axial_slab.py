#!/usr/bin/env python3
"""Compare true slab errors with adjacent-grid changes, preserving all outcomes."""
import argparse
import json
import resource
import sys
import time
from pathlib import Path
import numpy as np
from analytic_axial_slab import analytic_checks,discrete_slab,errors_against_reference,adjacent_errors


def save(path,data):
    with path.open('x') as out:json.dump(data,out,indent=2,allow_nan=False);out.write('\n')


def main(root):
    plan=json.loads((root/'plan.json').read_text());start=time.perf_counter();mu=1/np.sqrt(3);limits=plan['limits']
    result=dict(scope=plan['scope'],cases=[],adjacent=[],finest=[])
    def usage():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024**2 if sys.platform=='darwin' else 1024)
        return dict(elapsed_seconds=time.perf_counter()-start,peak_rss_mib=rss)
    try:
        for case in plan['cases']:
            previous=None;previous_row=None
            for n in plan['meshes']:
                args=(case['total'],case['scattering'],plan['height_cm'],mu,plan['source_per_direction'],n)
                analytic,reference=analytic_checks(*args);row,fields=discrete_slab(*args);fields.update(reference)
                row.update(case=case['id'],n=n,total=case['total'],scattering_fraction=case['scattering_fraction'],analytic=analytic,
                           **errors_against_reference(fields))
                row['matrix_passed']=row['matrix_residual_relative']<limits['matrix_residual_relative']
                row['balance_passed']=row['raw_global_balance_relative']<limits['raw_global_balance_relative']
                row['positivity_passed']=row['minimum_angular']>=limits['minimum_flux']
                row['analytic_passed']=all(analytic[k]<limits['analytic_identities_relative'] for k in ['even_identity_relative','odd_identity_relative','boundary_relative','global_balance_relative','cell_quadrature_relative'])
                np.savez_compressed(root/f"analysis/{case['id']}_{n}.npz",**fields)
                result['cases'].append(row)
                if previous is not None:
                    comparison=dict(case=case['id'],coarse_n=n//2,fine_n=n,**adjacent_errors(previous,fields))
                    for key in ['scalar','angular','total_escape']:
                        error=row[f'{key}_true_relative'];old=previous_row[f'{key}_true_relative'];change=comparison[f'{key}_adjacent_relative']
                        comparison[f'{key}_true_fine_relative']=error
                        comparison[f'{key}_observed_true_order']=float(np.log2(old/error)) if min(old,error)>plan['order_noise_floor'] else None
                        comparison[f'{key}_true_over_adjacent']=float(error/change) if change>plan['order_noise_floor'] else None
                    threshold=plan['diagnostic_threshold']
                    comparison['adjacent_pair_below_one_percent']=max(comparison['scalar_adjacent_relative'],comparison['total_escape_adjacent_relative'])<threshold
                    comparison['true_fine_below_one_percent']=max(row['scalar_true_relative'],row['total_escape_true_relative'])<threshold
                    comparison['false_admission']=comparison['adjacent_pair_below_one_percent'] and not comparison['true_fine_below_one_percent']
                    result['adjacent'].append(comparison)
                previous=fields;previous_row=row
                u=usage()
                if u['elapsed_seconds']>plan['elapsed_limit_seconds'] or u['peak_rss_mib']>plan['peak_rss_limit_mib']:
                    raise RuntimeError(f'Predeclared resource cap exceeded: {u}')
            result['finest'].append(row)
            print(case['id'],'finest scalar error',row['scalar_true_relative'],'escape error',row['total_escape_true_relative'],flush=True)
        result['analytic_reference_checks_passed']=all(r['analytic_passed'] for r in result['cases'])
        result['discrete_algebra_balance_positivity_passed']=all(r['matrix_passed'] and r['balance_passed'] and r['positivity_passed'] for r in result['cases'])
        result['manufactured_implementation_qualified']=result['analytic_reference_checks_passed'] and result['discrete_algebra_balance_positivity_passed']
        result['false_admission_count']=sum(r['false_admission'] for r in result['adjacent'])
        result['native_mesh_convergence_qualified']=False;result['coupled_eigenreference_qualified']=False
        save(root/'analysis/result.json',result)
        print(json.dumps({k:v for k,v in result.items() if isinstance(v,(bool,int))},indent=2))
    finally:save(root/'runs/resource_usage.json',usage())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)

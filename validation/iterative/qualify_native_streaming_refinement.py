#!/usr/bin/env python3
"""Calibrate the bounded sweep, then refine exactly the predeclared sources."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native,relative,save_json
from native_axial_streaming_refinement import Budget,batched_green,heldout_boundary,mesh_difference


def path(root,kind,g,n,b):return root/f'analysis/{kind}_{g}_{n}_{b}.npz'


def main(root):
    plan=json.loads((root/'plan.json').read_text());lim=plan['limits']
    budget=Budget(plan['peak_rss_limit_mib'],plan['elapsed_limit_seconds_per_execution'])
    d=load_native(root/'inputs/track_data.bin')
    result=dict(scope=plan['scope'],calibration=[],cases=[],segment_balance=[],mesh_checks=[],kernel_comparisons=[])
    def run_mesh(a,kind,n,calibration):
        g=a['group'];green,stats,defects=batched_green(d,a,n,plan['height_cm'],kind,plan['batch_lines'],budget)
        result['segment_balance'].append(dict(group=g,kernel=kind,n=n,**defects))
        for b in plan['radial_boundaries']:
            row,fields=heldout_boundary(d,a,green,n,plan['height_cm'],b)
            row.update(group=g,kernel=kind,primitive_minima=stats)
            row['positivity_passed']=all(x>=0 for x in stats.values()) and all(row[k]>=0 for k in ['min_response','min_white_inverse','min_incoming','min_half_flux','min_half_outgoing'])
            gl=lim['exact_raw_balance_relative'] if kind=='exact' else lim['lifted_global_balance_relative']
            cl=lim['exact_raw_balance_relative'] if kind=='exact' else lim['lifted_cell_balance_relative']
            row['global_balance_passed']=max(row['even_global_balance_relative'],row['odd_global_balance_relative'])<gl
            row['cell_balance_passed']=max(row['even_cell_balance_relative'],row['odd_cell_balance_relative'])<cl
            row['face_and_boundary_passed']=row['face_streaming_consistency_absolute']<lim['face_continuity_absolute'] and row['radial_boundary_relative']<5e-12
            result['cases'].append(row)
            np.savez_compressed(path(root,kind,g,n,b),green=green,**fields)
            if calibration:
                with np.load(root/f'inputs/coarse/{kind}_{g}_{n}_{b}.npz') as old:
                    errors=dict(green=relative(green,old['green']))
                    for k in ['phi','jz','half_flux','half_outgoing','incoming','face_current','face_second_moment']:
                        errors[k]=relative(fields[k],old[k][...,-2:])
                    errors['white_inverse']=relative(fields['white_inverse'],old['white_inverse'])
                result['calibration'].append(dict(group=g,kernel=kind,n=n,boundary=b,errors=errors,
                                                 passed=bool(max(errors.values())<plan['calibration_limit'])))
            budget.check()
        print('calibration' if calibration else 'refined','mesh',n,'group',g,kind,flush=True)
    try:
        for n in plan['calibration_meshes']:
            for a in d['group_data']:
                for kind in plan['kernels']:run_mesh(a,kind,n,True)
        result['coarse_calibration_passed']=all(r['passed'] for r in result['calibration'])
        save_json(root/'analysis/calibration.json',dict(cases=result['calibration'],passed=result['coarse_calibration_passed']))
        if not result['coarse_calibration_passed']:raise RuntimeError('Coarse calibration failed; no refined mesh admitted')
        for n in plan['refinement_meshes']:
            for a in d['group_data']:
                for kind in plan['kernels']:run_mesh(a,kind,n,False)
        for a in d['group_data']:
            g=a['group']
            for kind in plan['kernels']:
                for b in plan['radial_boundaries']:
                    prior_delta=None
                    for c,f in [(4,8),(8,16),(16,32),(32,64)]:
                        with np.load(path(root,kind,g,c,b)) as coarse,np.load(path(root,kind,g,f,b)) as fine:
                            flux,escape=mesh_difference(coarse,fine,d['weights'][:8],plan['height_cm'])
                            delta=coarse['axial_escape']-fine['axial_escape']
                        order=[None,None] if prior_delta is None else [float(np.log2(abs(x/y))) if x*y!=0 else None for x,y in zip(prior_delta,delta)]
                        monotone=[None,None] if prior_delta is None else [bool(x*y>0) for x,y in zip(prior_delta,delta)]
                        prior_delta=delta
                        result['mesh_checks'].append(dict(group=g,kernel=kind,boundary=b,coarse_n=c,fine_n=f,
                            flux_relative=flux.tolist(),axial_escape_relative=escape.tolist(),signed_escape_change=delta.tolist(),
                            observed_escape_order=order,same_sign_as_previous_change=monotone,
                            passed=bool(max(*flux,*escape)<lim['last_mesh_flux_and_axial_escape_relative'])))
            for n in plan['calibration_meshes']+plan['refinement_meshes']:
                for b in plan['radial_boundaries']:
                    with np.load(path(root,'exact',g,n,b)) as x,np.load(path(root,'native',g,n,b)) as y:
                        result['kernel_comparisons'].append(dict(group=g,n=n,boundary=b,
                            scalar_relative=relative(y['phi'],x['phi']),face_current_relative=relative(y['face_current'],x['face_current']),
                            escape_relative=(abs(y['axial_escape']-x['axial_escape'])/x['axial_escape']).tolist()))
        result['finite_mesh_response_passed']=all(all(r[k] for k in ['positivity_passed','global_balance_passed','cell_balance_passed','face_and_boundary_passed']) for r in result['cases'])
        result['final_mesh_convergence_passed']=all(r['passed'] for r in result['mesh_checks'] if r['fine_n']==64)
        result['prescribed_source_refinement_passed']=result['coarse_calibration_passed'] and result['finite_mesh_response_passed'] and result['final_mesh_convergence_passed']
        result['new_coupled_eigenreference_qualified']=False
        save_json(root/'analysis/result.json',result)
        print(json.dumps({k:v for k,v in result.items() if isinstance(v,bool)},indent=2),flush=True)
    finally:
        save_json(root/'runs/resource_usage.json',budget.snapshot())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path)
    main(p.parse_args().artifact)

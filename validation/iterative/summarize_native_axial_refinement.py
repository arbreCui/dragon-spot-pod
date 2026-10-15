#!/usr/bin/env python3
"""Mesh differences are diagnostics, not an extrapolated reference truth."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_multigroup_pod import load_data
from qualify_native_axial_coupling import save


def restrict_uniform(phi):
    ng,nz,nr=phi.shape
    if nz%2:raise ValueError('uniform dyadic refinement required')
    return phi.reshape(ng,nz//2,2,nr).mean(axis=2)


def main(artifact):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text());d=load_data(a/'inputs/multigroup_data.bin')
    result={'scope':plan['scope'],'meshes':[],'refinements':[]}
    fields={};rows={}
    for n in plan['meshes']:
        case={1:'one_cell',2:'two_equal'}.get(n,str(n))
        rows[n]=json.loads((a/f'analysis/case_{case}.json').read_text())
        fields[n]=np.load(a/f'analysis/case_{case}.npz')['phi']
        result['meshes'].append({'cells':n,**rows[n]})
    gate=plan['mesh_stopping_claim'];streak=0
    for old,n in zip(plan['meshes'][:-1],plan['meshes'][1:]):
        assert n==old*2
        fine=restrict_uniform(fields[n]);ref=fields[old]
        change={'from_cells':old,'to_cells':n,'relative_k_change':abs(rows[n]['k']/rows[old]['k']-1),
                'delta_rho_pcm':1e5*(rows[n]['rho']-rows[old]['rho']),
                'restricted_flux_relative_l2':float(np.sqrt(np.sum(d['v']*(fine-ref)**2)/np.sum(d['v']*fine**2))),
                'relative_axial_current_change':abs(rows[n]['axial_outgoing_current']/rows[old]['axial_outgoing_current']-1)}
        passed=all(change[k]<=gate[k] for k in ['relative_k_change','restricted_flux_relative_l2','relative_axial_current_change'])
        change['numerical_change_thresholds_passed']=passed
        change['both_full_references_admitted']=rows[old]['admitted'] and rows[n]['admitted']
        streak=streak+1 if passed and change['both_full_references_admitted'] else 0
        result['refinements'].append(change)
    result['consecutive_passing_final_refinements']=streak
    result['mesh_gate_passed']=streak>=gate['required_successive_refinements']
    result['all_full_references_admitted']=all(r['admitted'] for r in rows.values())
    result['calibration_max_relative_phi']=max(json.loads((a/f'analysis/case_{c}.json').read_text())['calibration_relative_phi'] for c in plan['calibration'])
    result['max_angular_equation_residual']=max(r['full_angular_residual_relative'] for r in rows.values())
    result['max_raw_balance_relative']=max(abs(r['raw_balance_relative_to_birth']) for r in rows.values())
    result['note']='Mesh differences only; no extrapolated truth, no full 3D or production validation.'
    save(a/'analysis/result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='meshes'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)

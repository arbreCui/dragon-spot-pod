#!/usr/bin/env python3
"""Descriptive interior moment identity and diffusion-scale cost interpretation."""
import argparse
import json
from pathlib import Path
import numpy as np


def main(root):
    plan=json.loads((root/'plan.json').read_text());result=json.loads((root/'analysis/result.json').read_text())
    mu=1/np.sqrt(3);records=[]
    for case in plan['cases']:
        for n in plan['meshes']:
            with np.load(root/f"analysis/{case['id']}_{n}.npz") as f:
                h=plan['height_cm']/n;p=f['phi'];j=f['current'];r=f['matrix_residual'].reshape(2,n)
                centered=lambda x:(x[2:]-x[:-2])/(2*h)
                laplacian=lambda x:(x[2:]-2*x[1:-1]+x[:-2])/h**2
                even=centered(j)-mu*h/2*laplacian(p)+(case['total']-case['scattering'])*p[1:-1]-plan['source_per_direction']
                odd=mu**2*centered(p)-mu*h/2*laplacian(j)+case['total']*j[1:-1]
                identity=max(float(np.max(abs(even-r[:,1:-1].sum(axis=0)/2))),
                             float(np.max(abs(odd-mu*(r[0,1:-1]-r[1,1:-1])/2))))/plan['source_per_direction']
            records.append(dict(case=case['id'],n=n,interior_identity_source_scaled_defect=identity,
                                diffusion_scale_ratio=case['total']*h/(2*mu)))
    out=dict(scope='Postprocessing algebraic identity and formal slow-variation interpretation; no new acceptance gate and no change to the numerical solution.',
             exact_interior_even='D_center J - mu*h/2*Laplace(phi) + sigma_a*phi = q',
             exact_interior_odd='mu^2*D_center phi - mu*h/2*Laplace(J) + sigma_t*J = 0',
             diffusion_limit='If J approximates -mu^2/sigma_t*dphi/dz, the leading diffusion coefficient becomes mu^2/sigma_t + mu*h/2. This is an interior slow-variation interpretation, not an exact boundary-error formula.',
             ratio='eta = sigma_t*h/(2*mu)',records=records,
             strongest_case_256_eta=2*20/(256*2*mu),
             cells_for_eta_below_one_percent=2*20/(2*mu*.01),
             estimate_limitation='The eta target is a diffusion-scale cost indicator, not a claim that this many cells guarantees 1% scalar or leakage error. It is not transferable to native radial white-return transport.',
             measured_false_admissions=[r for r in result['adjacent'] if r['false_admission']])
    with (root/'analysis/interior_identity.json').open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(max_interior_identity_defect=max(r['interior_identity_source_scaled_defect'] for r in records),
                         strongest_case_eta=out['strongest_case_256_eta'],cells_for_eta=out['cells_for_eta_below_one_percent']),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)

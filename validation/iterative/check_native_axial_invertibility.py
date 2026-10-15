#!/usr/bin/env python3
"""Supplementary full removal-matrix conditioning check (not a POD fit).

Explicit inverse norms are acceptable here only for the three small frozen
diagnostic matrices. No production matrix or factorization is changed.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_multigroup_pod import load_data
from qualify_native_axial_coupling import assemble,fission_data,save


def main(artifact):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text())
    d=load_data(a/'inputs/multigroup_data.bin')
    for g in range(370):d['scatter'][g,g]=d['physical_r'][g]
    nuf,chi=fission_data(a/'analysis/fission.bin')
    closure=np.load(a/'inputs/operator_fields.npz')['loss'].copy()
    for g in range(370):closure[g]-=np.diag(d['total_r'][g])
    identity=np.broadcast_to(np.eye(8),(370,8,8))
    for name,h in plan['meshes_cm'].items():
        matrix,*_=assemble(d['total_r'],d['scatter'],closure,nuf,chi,d['v'],identity,h)
        inverse=np.linalg.inv(matrix)
        norm=float(np.linalg.norm(matrix,np.inf));invnorm=float(np.linalg.norm(inverse,np.inf))
        # Compute every inverse residual column in bounded blocks.
        maxerr=0.;rows=np.zeros(len(matrix))
        for start in range(0,len(matrix),128):
            stop=min(start+128,len(matrix))
            residual=matrix@inverse[:,start:stop]
            residual[np.arange(start,stop),np.arange(stop-start)]-=1
            maxerr=max(maxerr,float(np.max(abs(residual))))
            rows+=np.sum(abs(residual),axis=1)
        result={'name':name,'size':len(matrix),'condition_inf':norm*invnorm,
                'inverse_residual_max':maxerr,'inverse_residual_inf':float(rows.max()),
                'condition_times_binary64_epsilon':norm*invnorm*np.finfo(float).eps}
        save(a/f'analysis/invertibility_{name}.json',result)
        print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path)
    main(p.parse_args().artifact)

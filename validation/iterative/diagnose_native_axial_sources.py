#!/usr/bin/env python3
"""Retain the signed DD numerator and its original three source terms."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_multigroup_pod import load_data
from qualify_native_axial_coupling import fission_data,MU,save


def signed_source_audit(total,heights,phi,faces,scatter_source,fission_source,radial_term):
    q=scatter_source+fission_source-radial_term
    incoming=np.zeros_like(faces)
    incoming[:,0,1:]=faces[:,0,:-1];incoming[:,1,:-1]=faces[:,1,1:]
    h=np.asarray(heights)[None,None,:,None]
    attenuation=MU/h-total[:,None,None,:]/2
    denom=MU/h+total[:,None,None,:]/2
    predicted=(q[:,None,:,:]/2+attenuation*incoming)/denom
    negative=faces<0
    thin_seed=negative&(incoming>=0)&(attenuation>=0)
    vacuum=np.zeros_like(negative);vacuum[:,0,0]=True;vacuum[:,1,-1]=True
    vacuum_negative=negative&vacuum
    # This is a signed equality check, not a positivity repair.
    loc=np.unravel_index(np.argmin(faces),faces.shape);g,d,z,i=loc
    result={'negative_scalar_count':int(np.sum(phi<0)),'negative_angle_count':int(negative.sum()),
            'negative_effective_source_count':int(np.sum(q<0)),
            'thin_nonnegative_inflow_negative_outflow_count':int(thin_seed.sum()),
            'thin_seed_with_nonnegative_q_count':int(np.sum(thin_seed&(q[:,None,:,:]>=0))),
            'vacuum_negative_outflow_count':int(vacuum_negative.sum()),
            'negative_outflow_with_negative_attenuation_count':int(np.sum(negative&(attenuation<0))),
            'dd_reconstruction_max_abs_error':float(np.max(abs(predicted-faces))),
            'dd_reconstruction_relative_error':float(np.max(abs(predicted-faces))/np.max(abs(faces))),
            'worst':{'group':int(g+1),'direction':['plus','minus'][d],'cell':int(z+1),'region':int(i+1),
                     'outgoing':float(faces[loc]),'incoming':float(incoming[loc]),
                     'effective_source':float(q[g,z,i]),'scatter_source':float(scatter_source[g,z,i]),
                     'fission_source_divided_by_k':float(fission_source[g,z,i]),
                     'radial_term':float(radial_term[g,z,i]),'total':float(total[g,i]),
                     'optical_ratio_total_h_over_2mu':float(total[g,i]*heights[z]/(2*MU)),
                     'predicted_outgoing':float(predicted[loc])}}
    return result,q


def main(artifact):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text());d=load_data(a/'inputs/multigroup_data.bin')
    nuf,chi=fission_data(a/'inputs/fission.bin');c=np.load(a/'inputs/operator_fields.npz')['loss'].copy()
    for g in range(370):d['scatter'][g,g]=d['physical_r'][g];c[g]-=np.diag(d['total_r'][g])
    results=[]
    for n in plan['meshes']:
        case={1:'one_cell',2:'two_equal'}.get(n,str(n))
        result=json.loads((a/f'analysis/case_{case}.json').read_text())
        fields=np.load(a/f'analysis/case_{case}.npz');phi,faces=fields['phi'],fields['faces']
        scatter=np.einsum('ghi,hzi->gzi',d['scatter'],phi,optimize=True)
        fiss=np.einsum('gic,zic->gzi',chi,np.einsum('gic,gzi->zic',nuf,phi,optimize=True),optimize=True)/result['k']
        radial=np.einsum('gij,gzj->gzi',c,phi,optimize=True)
        audit,q=signed_source_audit(d['total_r'],result['heights_cm'],phi,faces,scatter,fiss,radial)
        audit['cells']=n;results.append(audit)
        np.savez_compressed(a/f'analysis/source_{n}.npz',effective=q,scatter=scatter,fission_over_k=fiss,radial=radial)
    save(a/'analysis/source_audit.json',results)
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)

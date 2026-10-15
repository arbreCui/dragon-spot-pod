"""Analytical cyclic white enclosure and open-boundary conservation checks."""
import argparse
from pathlib import Path
import numpy as np
from native_layered_full_action import evaluate,solve_white,validate_white,compare_actions,measures
from calibrate_native_oblique_streaming import save


def main(root):
    nz=1;ns=2;nv=8;nb=6;k=24
    op=np.zeros((ns,30,k));perm=np.roll(np.eye(nb),1,axis=0)
    for s in range(ns):
        for r in range(nv):
            op[s,r,r]=.8;op[s,nv+r%nb,r]=.2
            op[s,r,nv+nb+r]=.6;op[s,nv+nb+r,nv+nb+r]=.4
        op[s,nv:nv+nb,nv:nv+nb]=.25*perm
        op[s,:nv,nv:nv+nb]=.75/nv
    jx=op[:,:nv]*np.array([.3,-.3])[:,None,None];aj=abs(jx)
    m=dict(volume=np.ones((ns,nv)),radial=np.ones((ns,nb)),axial=np.ones((ns,8)),mu=np.array([-.4,.4]))
    q=np.eye(ns*nv).reshape(ns,nv,ns*nv);sigma=np.ones(8);vol=np.ones(nv)
    f=solve_white(op,jx,aj,q,sigma,m,vol,nz);checks=validate_white(f)
    rhs=np.zeros((nb,ns*nv))
    for s in range(ns):
        for r in range(nv):rhs[r%nb,s*nv+r]=.1
    geometric_inverse=sum((.25**j)*np.linalg.matrix_power(perm,j) for j in range(nb))/(1-.25**nb)
    np.testing.assert_allclose(f['amplitudes'],geometric_inverse@rhs,rtol=2e-15,atol=0)
    np.testing.assert_allclose(f['inverse'],geometric_inverse,rtol=2e-15,atol=0)
    np.testing.assert_allclose(f['collision'],1,rtol=2e-15,atol=0)
    # Every open volume, radial and axial source obeys the same independent ledger.
    x=np.zeros((ns,k,ns*(k-2)));x[:,:k-2]=np.eye(ns*(k-2)).reshape(ns,k-2,ns*(k-2))
    open_fields=evaluate(op,jx,aj,x,sigma,m,vol,nz)
    assert abs(open_fields['global_defect']).max()<1e-15
    np.testing.assert_allclose(open_fields['jz'][:,:nv],-.4*open_fields['phi'][:,:nv],rtol=2e-15,atol=0)
    np.testing.assert_allclose(open_fields['jx'][:,:nv],.3*open_fields['phi'][:,:nv],rtol=2e-15,atol=0)
    stored=solve_white(op,jx,aj,q,sigma,m,vol,nz,normalizer=np.full(nb,2.02))
    validate_white(stored,physical=False)
    assert abs(stored['physical_defect']).max()>1e-3
    rejected=False
    try:validate_white(stored,physical=True)
    except AssertionError:rejected=True
    assert rejected,'different surface normalization must not claim geometric conservation'
    np.testing.assert_allclose(stored['physical_defect'],stored['geometric_face_defect'].sum(axis=0),rtol=2e-13,atol=0)
    compare_actions(f,f)
    missing=False
    try:solve_white(op,jx,aj,q,sigma,m,vol,nz,normalizer=np.zeros(nb))
    except ValueError:missing=True
    assert missing
    # A two-segment inventory with known directed measures; two planar directions
    # contribute volume/axial area, each radial endpoint contributes once.
    d=dict(nseg=np.array([4]),planar_widths=np.array([[2.,3.]]),nom=np.array([[0,1,3,0]]),
        zmu=np.array([1.25]),wei=np.array([4.]),wzmu=np.array([.2]),entry_surface=np.array([1]),exit_surface=np.array([4]))
    geo=measures(d,10,2,polars=[0]);v=np.zeros(8);v[[0,2]]=[10,15];b=np.zeros(6);b[[1,4]]=2;a=np.zeros(8);a[[0,2]]=[1.2,1.8]
    np.testing.assert_allclose(geo['volume'],np.tile(np.repeat(v,2),(2,1)),rtol=2e-15,atol=0)
    np.testing.assert_allclose(geo['radial'],np.tile(np.repeat(b,2),(2,1)),rtol=2e-15,atol=0)
    np.testing.assert_allclose(geo['axial'],np.tile(a,(2,1)),rtol=2e-15,atol=0)
    np.testing.assert_allclose(geo['mu'],[-.6,.6],rtol=2e-15,atol=0)
    save(root/'preflight/action_test.json',dict(analytical_cyclic_white=True,all_open_coordinates_conserved=True,
        axial_and_planar_current_signs=True,stored_normalizer_false_conservation_rejected=True,missing_white_measure_rejected=True,
        directed_geometric_measure=True,checks=checks,passed=True))
    print('native layered full action analytical tests passed',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();main(a.root.resolve())

"""Manufactured complete six-surface ray bundle, not a native-track subset."""
import numpy as np
from native_layered_transport import transport,aggregate
from native_layered_reference import RectangleReference,packed
from native_oblique_streaming import ratio


def bundle(library,H,nz,total,order,reference=False):
    """Three equal-weight transverse chords joining surface pairs 0/1, 2/3, 4/5.

    All eight signed polar states and both planar orientations are retained.
    This fully defines a small manufactured discrete transport model. It is
    not a geometric approximation claiming to cover the native fixture.
    """
    S=.8;mu=np.array([.2,.5,.8,.95]);pw=np.array([1.,2.,3.,4.])/10
    sig=np.full(8,total);nr=14*nz+8;operator=np.zeros((14*nz+16,nr));moment=np.zeros((8*nz,nr))
    incoming=np.zeros(6*nz);birth=np.zeros(8*nz);minimum=np.inf
    for p in range(4):
        for sign in [1,-1]:
            for o in [1,-1]:
                # One geometry/solution can be relabelled to all three pairs;
                # permutation preserves every named source/surface coordinate.
                entry,exit_surface=(0,1) if o==1 else (1,0)
                result=transport(library,[S],[0],sig,entry,H,nz,sign*mu[p],o,order)
                a=aggregate(result['fields'],np.array([0]),nz,o,exit_surface)
                x=packed(a)[:,:nr]
                if reference:
                    ref=RectangleReference([S],[0],sig,entry,exit_surface,H,nz,sign*mu[p],o,
                        result['q'],result['radial_input'],result['axial_input'])
                    x=ref.fixed(order)[:,:nr]
                minimum=min(minimum,float(x.min()))
                for pair in range(3):
                    perm=np.arange(nr);rowperm=np.arange(14*nz+16)
                    if pair:
                        first=np.arange(2*nz)+8*nz;other=np.arange(2*nz)+(8+2*pair)*nz
                        perm[first],perm[other]=perm[other].copy(),perm[first].copy()
                        rowperm[first],rowperm[other]=rowperm[other].copy(),rowperm[first].copy()
                    weight=pw[p]/12
                    operator[np.ix_(rowperm,perm)]+=weight*x
                    moment[:,perm]+=weight*sign*mu[p]*x[:8*nz]
                    incoming[(2*pair+entry)*nz:(2*pair+entry+1)*nz]+=weight*H/nz
                    birth[:nz]+=weight*S*H/nz
    return dict(operator=operator,jz=moment,radial_incoming_measure=incoming,volume_measure=birth,
                minimum_response=minimum,height=H,nz=nz,total=total)


def close(bundle):
    nz=bundle['nz'];nv=8*nz;nb=6*nz;g=bundle['operator'];measure=bundle['radial_incoming_measure']
    assert np.all(measure>0) and g.min()>=0
    tbb=g[nv:nv+nb,nv:nv+nb]/measure[:,None];matrix=np.eye(nb)-tbb
    inverse=np.linalg.solve(matrix,np.eye(nb));q=np.zeros((nv,nz+2));q[:nz,:nz]=np.eye(nz)
    q[:nz,nz]=np.arange(1,nz+1)/(nz+1);q[:nz,nz+1]=1.
    rhs=(g[nv:nv+nb,:nv]@q)/measure[:,None];amp=np.linalg.solve(matrix,rhs)
    inputs=np.concatenate([q,amp,np.zeros((8,nz+2))]);out=g@inputs
    born=bundle['volume_measure']@q;collision=bundle['total']*out[:nv].sum(axis=0)
    escape=out[nv+nb:].sum(axis=0);radout=out[nv:nv+nb];radin=measure[:,None]*amp
    r=dict(q=q,inflow=amp,fields=out,jz=bundle['jz']@inputs,tbb=tbb,inverse=inverse,
        birth=born,collision=collision,axial_escape=escape,radial_incoming=radin,radial_outgoing=radout,
        matrix_residual=matrix@amp-rhs,closure_defect=radout-radin,
        raw_balance=born+radin.sum(axis=0)-collision-radout.sum(axis=0)-escape)
    checks=dict(inverse_identity=float(abs(matrix@inverse-np.eye(nb)).max()),
        solve=float(ratio(r['matrix_residual'],abs(rhs).max(axis=0)).max()),
        closure=float(ratio(r['closure_defect'],radin.max(axis=0)).max()),
        raw_balance=float(ratio(r['raw_balance'],born+radin.sum(axis=0)).max()),
        source_collision_escape=float(ratio(born-collision-escape,born).max()),
        minimum_inverse=float(inverse.min()),minimum_response=float(out.min()),
        minimum_inflow=float(amp.min()),minimum_axial_escape=float(escape.min()),
        spectral_radius=float(max(abs(np.linalg.eigvals(tbb)))))
    checks['passed']=bool(max(checks[k] for k in ['inverse_identity','solve','closure'])<5e-12 and
        max(checks[k] for k in ['raw_balance','source_collision_escape'])<1e-10 and
        min(checks[k] for k in ['minimum_inverse','minimum_response','minimum_inflow'])>=0
        and checks['minimum_axial_escape']>0 and checks['spectral_radius']<1)
    return r,checks

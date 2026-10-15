"""Evaluate independently recovered axial-sign operators on frozen inputs."""
import numpy as np
from qualify_native_signed_axial import axial_mu,angular_measures,ledger


def evaluate(d,a,green,q,inflow):
    x=np.concatenate([q,inflow],axis=2)
    if x.shape[:3]!=(2,4,14):raise ValueError('all original axial-sign/polar/source coordinates required')
    integral=np.einsum('zopru,zpuc->zprc',green['volume'],x)
    boundary=np.einsum('zopsu,zpuc->zpsc',green['boundary'],x)
    vol=d['weights'][:8,None];surface=d['weights'][8:,None];mu=axial_mu(d)
    f=dict(integral=integral,boundary=boundary,phi=integral.sum(axis=(0,1))/vol,
        jz=np.einsum('prc,p->rc',integral[0]-integral[1],mu)/vol,
        jx=np.einsum('zopru,zpuc->rc',green['jx'],x)/vol,
        outgoing=boundary.sum(axis=(0,1))/surface,q=q,inflow=inflow)
    absolute=np.einsum('zopru,zpuc->zprc',green['volume'],abs(x))
    f.update(phi_scale=absolute.sum(axis=(0,1))/vol,
        jz_scale=np.einsum('zprc,p->rc',absolute,mu)/vol,
        jx_scale=np.einsum('zopru,zpuc->rc',green['abs_jx'],abs(x))/vol,
        outgoing_scale=np.einsum('zopsu,zpuc->sc',green['boundary'],abs(x))/surface)
    f.update(ledger(d,a,q,inflow,integral,boundary))
    vw,sw=angular_measures(d)
    f['stored_volume_birth']=np.einsum('zprc,pr,r->c',q,vw,vol[:,0]/(2*vw.sum(axis=0)))
    f['stored_surface_incoming']=np.einsum('zpsc,ps,s->c',inflow,sw,surface[:,0]/(2*sw.sum(axis=0)))
    return f


def close_white(d,a,green,fixed,tags):
    tags=np.asarray(tags);volume=np.flatnonzero(tags=='angular_volume_vacuum');boundary=np.flatnonzero(tags=='angular_boundary_open')
    targets=np.flatnonzero((tags=='angular_volume_white')|(tags=='pair_white'))
    common_map=np.tile(np.eye(6),(8,1));tbb=fixed['outgoing'][:,boundary]@common_map;matrix=np.eye(6)-tbb
    inverse=np.linalg.solve(matrix,np.eye(6));q=fixed['q'][...,targets]
    rhs=fixed['outgoing'][:,volume]@q.reshape(64,-1);amplitudes=np.linalg.solve(matrix,rhs)
    incoming=np.broadcast_to(amplitudes,(2,4,*amplitudes.shape)).copy();f=evaluate(d,a,green,q,incoming)
    f.update(tbb=tbb,boundary_inverse=inverse,white_rhs=rhs,white_amplitudes=amplitudes,
        white_matrix_residual=matrix@amplitudes-rhs,white_closure_defect=f['outgoing']-amplitudes,
        target_indices=targets,stored_white_net_current=(d['weights'][8:,None]*(f['outgoing']-amplitudes)).sum(axis=0))
    return f

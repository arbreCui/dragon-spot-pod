#!/usr/bin/env python3
"""Independent native radial P0 / axial S2-DD candidate. Never edits live data.

Project the ANGULAR equations before forming their exact scalar Schur complement.
Fission remains the original sum of component-wise chi times nu-sigma-f.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_multigroup_pod import load_data

MU = 1 / np.sqrt(3.)


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def fission_data(path):
    with Path(path).open('rb') as f:
        head = np.fromfile(f, '<i4', 5)
        if len(head) != 5 or tuple(head[:3]) != (8, 370, 32) or head[4] != 3330:
            raise ValueError('unqualified original fission export')
        fields = [np.fromfile(f, '<f4', 8*32*370).reshape((8,32,370), order='F')
                  .transpose(2,0,1).astype(float) for _ in range(2)]
        if f.read() or any(not np.isfinite(x).all() or np.any(x < 0) for x in fields):
            raise ValueError('invalid fission export')
    return fields


def axial_map(total, volume, basis, heights):
    """Return G^-1, face-from-source map D, and cell scalar extractor E.

    Faces are ordered [plus cell outflows, minus cell outflows]. Vacuum
    inflows are omitted. Source entries are B^T W q, including radial closure.
    """
    nz, rank = len(heights), basis.shape[1]
    mass = basis.T @ (volume[:,None] * basis)
    collision = basis.T @ ((volume*total)[:,None] * basis)
    t = np.zeros((2*nz*rank, 2*nz*rank))
    q = np.zeros((2*nz*rank, nz*rank))
    e = np.zeros((nz*rank, 2*nz*rank))
    for direction in range(2):
        for z, h in enumerate(heights):
            row = slice((direction*nz+z)*rank,(direction*nz+z+1)*rank)
            cell = slice(z*rank,(z+1)*rank)
            t[row,row] = MU/h*mass + collision/2
            q[row,cell] = np.eye(rank)/2
            e[cell,row] = np.eye(rank)/2
            upstream = z-1 if direction == 0 else z+1
            if 0 <= upstream < nz:
                col = slice((direction*nz+upstream)*rank,(direction*nz+upstream+1)*rank)
                t[row,col] = -MU/h*mass + collision/2
                e[cell,col] = np.eye(rank)/2
    d = np.linalg.solve(t,q)
    g = e @ d
    return np.linalg.solve(g,np.eye(nz*rank)), d, e


def assemble(total, scatter, closure, nuf, chi, volume, basis, heights):
    ng,nr,rank = basis.shape; nz = len(heights); n = ng*nz*rank
    s = np.einsum('gia,ghi,hib,i->gahb',basis,scatter,basis,volume,optimize=True)
    a = np.zeros((ng,nz,rank,ng,nz,rank))
    for z in range(nz):
        a[:,z,:,:,z,:] = -s
    inverses=[]; faces=[]
    for g in range(ng):
        inv,d,_ = axial_map(total[g],volume,basis[g],heights)
        inverses.append(inv);faces.append(d)
        block = inv.reshape(nz,rank,nz,rank).copy()
        c = basis[g].T @ (volume[:,None]*closure[g]) @ basis[g]
        for z in range(nz):
            block[z,:,z,:] += c
        a[g,:,:,g,:,:] += block
    # Keep distinct fission components even when some spectra coincide.
    active = np.argwhere(np.any(nuf > 0,axis=0))
    nm = len(active); u = np.zeros((ng,nz,rank,nz,nm)); v = np.zeros((nz,nm,ng,nz,rank))
    weights = np.empty((nz,nm))
    for z,h in enumerate(heights):
        for j,(i,c) in enumerate(active):
            u[:,z,:,z,j] = (volume[i]*chi[:,i,c])[:,None]*basis[:,i,:]
            v[z,j,:,z,:] = nuf[:,i,c,None]*basis[:,i,:]
            weights[z,j] = h*volume[i]
    return a.reshape(n,n),u.reshape(n,nz*nm),v.reshape(nz*nm,n),weights.ravel(),np.array(inverses),np.array(faces)


def normalized_eigen(a,u,v,weights):
    p = np.linalg.solve(a,u)
    kernel = v @ p
    values,vectors = np.linalg.eig(kernel)
    selected = int(np.argmax(values.real))
    value = values[selected]
    k = float(value.real)
    if not np.isfinite(k) or k <= 0 or abs(value.imag) > 1e-11*abs(k):
        raise ValueError('largest-real-part mode is not a positive real eigenvalue')
    y = vectors[:,selected].real
    normrow = weights @ kernel
    y /= normrow@y
    modal = p@y
    residual = a@modal-u@(v@modal)/k
    gap = float(np.min(abs(np.delete(values,selected)-value))/abs(value)) if len(values)>1 else 1.
    j = np.block([[kernel-k*np.eye(len(y)),-y[:,None]], [normrow[None,:],np.zeros((1,1))]])
    # Row/column equilibration affects conditioning, not exact rank.
    j /= np.maximum(np.max(abs(j),axis=1),np.finfo(float).tiny)[:,None]
    j /= np.maximum(np.max(abs(j),axis=0),np.finfo(float).tiny)[None,:]
    singular = np.linalg.svd(j,compute_uv=False)
    powers=[]
    for seed in (np.ones(len(y)),np.arange(1,len(y)+1,dtype=float)):
        x = seed/np.linalg.norm(seed)
        converged = False
        for step in range(1,1001):
            updated=kernel@x; updated/=np.linalg.norm(updated)
            if np.dot(updated,x)<0: updated=-updated
            x=updated
            estimate=float(x@(kernel@x))
            err=float(np.linalg.norm(kernel@x-estimate*x)/max(abs(estimate),np.finfo(float).tiny))
            if err<1e-11:
                converged=True;break
        field=p@(x/(normrow@x))
        powers.append({'steps':step,'converged':converged,'k':estimate,'eigen_residual':err,
                       'relative_flux_difference':float(np.linalg.norm(field-modal)/np.linalg.norm(modal))})
    return modal,{'k':k,'rho':1/k,'eigen_imag_relative':float(abs(value.imag)/abs(k)),
                 'dominant_magnitude':bool(abs(value)>=np.max(abs(values))*(1-1e-11)),
                 'relative_spectral_separation':gap,
                 'schur_residual_relative':float(np.max(abs(residual))/np.max(abs(u@(v@modal)/k))),
                 'normalization':float(weights@(v@modal)),
                 'bordered_jacobian_size':len(y)+1,
                 'bordered_jacobian_rank':int(np.sum(singular>singular[0]*1e-11)),
                 'bordered_jacobian_relative_smin':float(singular[-1]/singular[0]),
                 'power_starts':powers}


def reconstruct(basis,modal,inverses,face_maps,nz):
    ng,nr,rank=basis.shape
    coeff=modal.reshape(ng,nz,rank)
    phi=np.einsum('gia,gza->gzi',basis,coeff)
    fc=np.empty((ng,2,nz,rank))
    for g in range(ng):
        fc[g]=(face_maps[g]@(inverses[g]@coeff[g].ravel())).reshape(2,nz,rank)
    faces=np.einsum('gia,gdza->gdzi',basis,fc)
    return phi,faces


def diagnostics(total,scatter,closure,nuf,chi,volume,basis,heights,phi,faces,k):
    h=np.asarray(heights);nz=len(h)
    scatter_phi=np.einsum('ghi,hzi->gzi',scatter,phi,optimize=True)
    production=np.einsum('gic,gzi->zic',nuf,phi,optimize=True)
    fission=np.einsum('gic,zic->gzi',chi,production,optimize=True)
    radial=np.einsum('gij,gzj->gzi',closure,phi,optimize=True)
    q=scatter_phi+fission/k-radial
    residual=np.empty_like(faces); scalar=np.zeros_like(phi); divergence=np.zeros_like(phi)
    for direction in range(2):
        for z in range(nz):
            up=z-1 if direction==0 else z+1
            incoming=faces[:,direction,up] if 0<=up<nz else np.zeros_like(phi[:,z])
            outgoing=faces[:,direction,z]
            avg=(incoming+outgoing)/2
            stream=MU/h[z]*(outgoing-incoming)
            residual[:,direction,z]=stream+total*avg-q[:,z]/2
            scalar[:,z]+=avg;divergence[:,z]+=stream
    scale=np.max(abs(fission/k))/2
    projected=np.einsum('gia,i,gdzi->gdza',basis,volume,residual)
    projected_scale=np.max(abs(np.einsum('gia,i,gzi->gza',basis,volume,fission/k)))/2
    weight=h[None,:,None]*volume[None,None,:]
    birth=float(np.sum(weight*fission/k))
    raw=float(np.sum(weight*(total[:,None,:]*phi-scatter_phi+divergence-fission/k)))
    defect=float(np.sum(weight*radial))
    weighted=float(np.sum(weight*np.sum(residual,axis=1)))
    outgoing_current=float(MU*np.sum(volume*(faces[:,0,-1]+faces[:,1,0])))
    return {'full_angular_residual_relative':float(np.max(abs(residual))/scale),
            'projected_angular_residual_relative':float(np.max(abs(projected))/projected_scale),
            'scalar_face_consistency_relative':float(np.max(abs(scalar-phi))/np.max(abs(phi))),
            'minimum_scalar_flux':float(phi.min()),'negative_scalar_count':int(np.sum(phi<0)),
            'minimum_outgoing_angular_flux':float(faces.min()),'negative_angular_count':int(np.sum(faces<0)),
            'global_nufission':float(np.sum(production*h[:,None,None]*volume[None,:,None])),
            'birth_divided_by_k':birth,'axial_outgoing_current':outgoing_current,
            'axial_telescope_error':float(np.sum(weight*divergence)-outgoing_current),
            'raw_balance':raw,'raw_balance_relative_to_birth':raw/birth,
            'native_radial_balance_defect':defect,'weighted_angular_residual':weighted,
            'balance_identity_error':raw-(weighted-defect)}


def admission(result,thresholds):
    failures=[]
    for key in ('full_angular_residual_relative','schur_residual_relative','scalar_face_consistency_relative'):
        if result[key]>thresholds['equation_residual']:failures.append(key)
    if result['minimum_scalar_flux']<=0:failures.append('nonpositive_scalar_flux')
    if result['minimum_outgoing_angular_flux']<=0:failures.append('nonpositive_outgoing_angular_flux')
    if not result['dominant_magnitude']:failures.append('not_dominant_magnitude')
    if result['relative_spectral_separation']<=thresholds['spectral_gap_relative_min']:failures.append('not_simple_separated_mode')
    if result['bordered_jacobian_rank']!=result['bordered_jacobian_size']:failures.append('normalized_jacobian_rank')
    if abs(result['normalization']-1)>thresholds['equation_residual']:failures.append('normalization')
    if abs(result['raw_balance_relative_to_birth'])>thresholds['raw_balance_relative']:failures.append('raw_balance')
    for i,p in enumerate(result['power_starts']):
        if not p['converged'] or p['relative_flux_difference']>thresholds['power_solution_agreement']:
            failures.append(f'power_start_{i}')
    return failures


def solve(data,loss,nuf,chi,basis,heights):
    closure=loss.copy()
    for g in range(len(loss)):
        closure[g]-=np.diag(data['total_r'][g])
    a,u,v,w,inv,faces=assemble(data['total_r'],data['scatter'],closure,nuf,chi,data['v'],basis,heights)
    modal,result=normalized_eigen(a,u,v,w)
    phi,angular=reconstruct(basis,modal,inv,faces,len(heights))
    result.update(diagnostics(data['total_r'],data['scatter'],closure,nuf,chi,data['v'],basis,heights,phi,angular,result['k']))
    return result,phi,angular


def main(artifact,phase):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text());d=load_data(a/'inputs/multigroup_data.bin')
    for g in range(370):d['scatter'][g,g]=d['physical_r'][g]
    nuf,chi=fission_data(a/'analysis/fission.bin')
    loss=np.load(a/'inputs/operator_fields.npz')['loss']
    if phase=='references':
        identity=np.broadcast_to(np.eye(8),(370,8,8))
        for name,heights in plan['meshes_cm'].items():
            result,phi,faces=solve(d,loss,nuf,chi,identity,heights)
            result.update(name=name,heights_cm=heights)
            result['failed_gates']=admission(result,plan['thresholds'])
            result['admitted']=not result['failed_gates']
            save(a/f'analysis/reference_{name}.json',result)
            np.savez_compressed(a/f'analysis/reference_{name}.npz',phi=phi,faces=faces)
            print(json.dumps(result),flush=True)
    else:
        bases=np.load(a/'inputs/projection_fields.npz')
        for name,heights in plan['meshes_cm'].items():
            reference=json.loads((a/f'analysis/reference_{name}.json').read_text())
            if not reference['admitted']:
                print(f'SKIP POD for rejected reference: {name}',flush=True);continue
            ref=np.load(a/f'analysis/reference_{name}.npz')['phi']
            for family in ('plain','enriched'):
                for rank in range(1,9):
                    b=bases[family+'_basis'][:,:,:rank]
                    result,phi,faces=solve(d,loss,nuf,chi,b,heights)
                    w=np.array(heights)[None,:,None]*d['v']
                    result.update(name=name,family=family,rank=rank,
                                  relative_flux_l2=float(np.sqrt(np.sum(w*(phi-ref)**2)/np.sum(w*ref**2))),
                                  delta_rho_pcm=1e5*(result['rho']-reference['rho']))
                    if rank in (3,8):
                        transform=np.eye(rank)+np.diag(np.full(rank-1,.23),1)
                        oblique,oflux,_=solve(d,loss,nuf,chi,b@transform,heights)
                        result['oblique_k_difference']=abs(oblique['k']-result['k'])/abs(result['k'])
                        result['oblique_flux_difference']=float(np.sqrt(np.sum(w*(oflux-phi)**2)/np.sum(w*phi**2)))
                    save(a/f'analysis/pod_{name}_{family}_{rank}.json',result)
                    np.savez_compressed(a/f'analysis/pod_{name}_{family}_{rank}.npz',phi=phi,faces=faces)
                    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact',type=Path);parser.add_argument('phase',choices=['references','pod'])
    args=parser.parse_args();main(args.artifact,args.phase)

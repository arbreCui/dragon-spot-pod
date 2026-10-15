#!/usr/bin/env python3
"""Prescribed-source qualification of full directional axial-cell transport."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native,relative,save_json
from qualify_native_signed_axial import axial_mu,angular_measures
from native_axial_streaming import (green_sweep,expand_green,upwind,scalar_integrals,
                                    dense_coefficients,polynomial_coefficients,shift_matrix)


def zero_gradient(a_root,d,a,kind):
    g=a['group'];green,stats=green_sweep(d,a,0,20.,kind)
    p=np.load(a_root/f'inputs/prepared_{g}.npz');old=np.load(a_root/f'inputs/result_{g}.npz')
    src=np.concatenate([p['q'],p['inflow']],axis=2)
    actual=np.einsum('poi,zpic->zpoc',green[:,0],src)
    expected=np.concatenate([old['native_half_integrals'],old['native_half_outgoing']],axis=2)
    errors=[relative(actual[...,i],expected[...,i]) for i in range(src.shape[-1])]
    scalar=actual[:,:,:8].sum(axis=(0,1))/d['weights'][:8,None]
    delta=a['pjj']-2*a['pjsum']/d['weights'][:8]
    scalar[:,:31]+=delta[:,None]*p['legacy'][:8]
    calibration=max(relative(np.r_[scalar[:,i],actual[:,:,8:,i].sum(axis=(0,1))/d['weights'][8:]],old['old_native'][:,i]) for i in range(31))
    jz=np.einsum('prc,p->rc',actual[0,:,:8]-actual[1,:,:8],axial_mu(d))/d['weights'][:8,None]
    measured=(jz[:,212]-jz[:,210])/2
    np.savez_compressed(a_root/f'analysis/zero_{kind}_{g}.npz',green=green,native_companion=actual,
                        half_state_errors=errors,scalar=scalar,jz=jz,odd_response=measured)
    return dict(group=g,kernel=kind,half_state_max_relative=max(errors),P0_max_case_relative=calibration,
                odd_response_relative=relative(measured,old['white_odd']),native_action_passed=max(max(errors),calibration)<5e-12,
                minima=stats)


def primitive_controls(d,a):
    mu=axial_mu(d);records=[]
    for p in range(d['nmu']):
        for r in range(8):
            candidates=np.argwhere((d['region']==r+1)&(d['polar'][:,None]==p))
            line,seg=candidates[len(candidates)//2]
            l=d['h'][line,seg];s=a['total'][r];bn=a['b'][line,seg];dn=a['self_d'][line,seg]
            for n in [1,2,4,8]:
                dense=dense_coefficients(l,s,mu[p],[20/n]*n)
                poly=polynomial_coefficients(l,s,mu[p]*n/20,n)
                error=max(relative(shift_matrix(x),y) for x,y in zip(poly,dense[:3]))
                t,b,own,_=dense_coefficients(l,s,mu[p],[20/n]*n,periodic=True,native_b=bn,native_d=dn)
                constant=max(relative(t@np.ones(n),(1-s*bn)*np.ones(n)),relative(b@np.ones(n),bn*np.ones(n)),
                             relative(own@np.ones(n),dn*np.ones(n)))
                records.append(dict(group=a['group'],polar=p,region=r+1,n=n,dense_relative=error,
                                    native_periodic_constant_relative=constant))
    return records


def run_boundary(d,a,green,n,height,radial_boundary):
    nr,nb,npole=8,6,d['nmu'];nv=nr*n;ns=(nr+nb)*n;nc=ns+18;h=height/n
    response=expand_green(d,green);mu=axial_mu(d);vw,sw=angular_measures(d)
    iso=np.zeros((ns,nc));iso[:,:ns]=np.eye(ns)
    iso[:nv,-2]=1.;iso[:nv,-1]=np.repeat(np.arange(1,9)/8,n)
    qext=iso[:nv].reshape(nr,n,nc);bext=iso[nv:].reshape(nb,n,nc)
    axial_in=np.zeros((2,nr,nc))
    for z in range(2):
        axial_in[z,np.arange(nr),ns+z*nr+np.arange(nr)]=1
    source=np.broadcast_to(iso[:nv],(2,npole,nv,nc)).copy()
    for z in range(2):
        cell=0 if z==0 else n-1
        for p in range(npole):source[z,p,np.arange(nr)*n+cell]+=mu[p]/h*axial_in[z]
    births=np.einsum('zpoi,zpic->zpoc',response[:,:,:,:nv],source)
    common_matrix=response.sum(axis=(0,1));tbb=common_matrix[nv:,nv:]
    if radial_boundary=='white':
        inverse=np.linalg.solve(np.eye(nb*n)-tbb,np.eye(nb*n))
        incoming=inverse@(births[:,:,nv:].sum(axis=(0,1))+iso[nv:])
    else:
        inverse=np.eye(nb*n);incoming=iso[nv:].copy()
    half=births+np.einsum('zpoi,ic->zpoc',response[:,:,:,nv:],incoming)
    phi_half=half[:,:,:nv].reshape(2,npole,nr,n,nc)
    out_half=half[:,:,nv:].reshape(2,npole,nb,n,nc)
    phi=phi_half.sum(axis=(0,1));jz=np.einsum('pric,p->ric',phi_half[0]-phi_half[1],mu)
    outgoing=out_half.sum(axis=(0,1));incoming=incoming.reshape(nb,n,nc)
    fp=np.zeros((npole,nr,n+1,nc));fm=np.zeros_like(fp)
    fp[:,:,1:]=phi_half[0];fm[:,:,:-1]=phi_half[1]
    fraction=vw/d['weights'][:nr][None,:]
    fp[:,:,0]=fraction[:,:,None]*axial_in[0][None,:,:]
    fm[:,:,-1]=fraction[:,:,None]*axial_in[1][None,:,:]
    faces=np.einsum('pric,p->ric',fp-fm,mu)
    faces2=np.einsum('pric,p->ric',fp+fm,mu**2)
    v=d['weights'][:nr];surface=d['weights'][nr:]
    born=h*np.einsum('ric,r->ic',qext,2*vw.sum(axis=0))
    r_in=h*np.einsum('sic,s->ic',incoming,2*sw.sum(axis=0))
    r_out=h*np.einsum('sic,s->ic',outgoing,surface)
    collision=h*np.einsum('ric,r->ic',phi,v*a['total'])
    axial_loss=np.einsum('ric,r->ic',faces[:,1:]-faces[:,:-1],v)
    residual=born+r_in-r_out-collision-axial_loss
    r_out_odd=h*np.einsum('psic,p,s->ic',out_half[0]-out_half[1],mu,surface)
    odd_collision=h*np.einsum('ric,r->ic',jz,v*a['total'])
    odd_loss=np.einsum('ric,r->ic',faces2[:,1:]-faces2[:,:-1],v)
    odd_residual=-r_out_odd-odd_collision-odd_loss
    ax_enter=np.einsum('pric,p,r->ic',fp[:,:,:-1]+fm[:,:,1:],mu,v)
    ax_enter_odd=np.einsum('pric,p,r->ic',fp[:,:,:-1]+fm[:,:,1:],mu**2,v)
    source_odd_abs=h*np.einsum('ric,pr,p->ic',qext,2*vw,mu)
    radial_odd_abs=h*np.einsum('sic,ps,p->ic',incoming,2*sw,mu)
    cellscale=born+r_in+ax_enter;oddscale=source_odd_abs+radial_odd_abs+ax_enter_odd
    external_radial=h*np.einsum('sic,s->ic',bext,2*sw.sum(axis=0))
    external_radial_odd=h*np.einsum('sic,ps,p->ic',bext,2*sw,mu)
    axial_birth=np.einsum('prc,p,r->c',fp[:,:,0]+fm[:,:,-1],mu,v)
    axial_birth_odd=np.einsum('prc,p,r->c',fp[:,:,0]+fm[:,:,-1],mu**2,v)
    global_scale=born.sum(axis=0)+external_radial.sum(axis=0)+axial_birth
    odd_global_scale=source_odd_abs.sum(axis=0)+external_radial_odd.sum(axis=0)+axial_birth_odd
    even_global=abs(residual.sum(axis=0))/np.maximum(global_scale,1e-300)
    odd_global=abs(odd_residual.sum(axis=0))/np.maximum(odd_global_scale,1e-300)
    even_cell=abs(residual)/np.maximum(cellscale,1e-300);odd_cell=abs(odd_residual)/np.maximum(oddscale,1e-300)
    # Independently evaluate the axial streaming matrices, including inflow RHS.
    stream_even=np.zeros((n,nc));stream_odd=np.zeros_like(stream_even)
    for z,sign in enumerate([1,-1]):
        du=upwind([h]*n,sign)
        for p in range(npole):
            action=np.einsum('ij,rjc->ric',du,phi_half[z,p])
            action[:,0 if z==0 else -1]-=fraction[p,:,None]*axial_in[z]/h
            term=h*mu[p]*np.einsum('ric,r->ic',action,v)
            stream_even+=term;stream_odd+=sign*mu[p]*term
    face_error=max(float(np.max(abs(stream_even-axial_loss))),float(np.max(abs(stream_odd-odd_loss))))
    closure=relative(incoming,bext+outgoing) if radial_boundary=='white' else relative(incoming,bext)
    row=dict(n=n,boundary=radial_boundary,cases=nc,min_response=float(response.min()),min_white_inverse=float(inverse.min()),
             min_incoming=float(incoming.min()),min_half_flux=float(phi_half.min()),min_half_outgoing=float(out_half.min()),
             even_global_balance_relative=float(even_global.max()),odd_global_balance_relative=float(odd_global.max()),
             even_cell_balance_relative=float(even_cell.max()),odd_cell_balance_relative=float(odd_cell.max()),
             face_streaming_consistency_absolute=face_error,radial_boundary_relative=closure,
             heldout_axial_escape=np.einsum('prc,p,r->c',fp[:,:,-1,-2:]+fm[:,:,0,-2:],mu,v).tolist())
    fields=dict(phi=phi,jz=jz,half_flux=phi_half,half_outgoing=out_half,incoming=incoming,
                face_current=faces,face_second_moment=faces2,volume_source=qext,radial_external=bext,axial_incoming=axial_in,
                even_cell_defect=residual,odd_cell_defect=odd_residual,even_cell_relative=even_cell,odd_cell_relative=odd_cell,
                even_global_relative=even_global,odd_global_relative=odd_global,white_inverse=inverse)
    return row,fields


def main(root):
    plan=json.loads((root/'plan.json').read_text());limits=plan['limits'];d=load_native(root/'inputs/track_data.bin')
    result=dict(scope=plan['scope'],zero_gradient=[],primitive_controls=[],cases=[],mesh_checks=[],kernel_comparisons=[])
    for a in d['group_data']:
        g=a['group'];controls=primitive_controls(d,a);result['primitive_controls']+=controls
        for kind in ['exact','native']:
            z=zero_gradient(root,d,a,kind);result['zero_gradient'].append(z)
            print('zero gradient',g,kind,z['half_state_max_relative'],flush=True)
            for n in plan['meshes']:
                green,stats=green_sweep(d,a,n,plan['height_cm'],kind)
                for boundary in ['vacuum','white']:
                    row,fields=run_boundary(d,a,green,n,plan['height_cm'],boundary)
                    row.update(group=g,kernel=kind,primitive_minima=stats)
                    global_limit=limits['exact_raw_balance_relative'] if kind=='exact' else limits['lifted_global_balance_relative']
                    cell_limit=limits['exact_raw_balance_relative'] if kind=='exact' else limits['lifted_cell_balance_relative']
                    row['positivity_passed']=all(x>=0 for x in stats.values()) and all(row[k]>=0 for k in ['min_response','min_white_inverse','min_incoming','min_half_flux','min_half_outgoing'])
                    row['global_balance_passed']=max(row['even_global_balance_relative'],row['odd_global_balance_relative'])<global_limit
                    row['cell_balance_passed']=max(row['even_cell_balance_relative'],row['odd_cell_balance_relative'])<cell_limit
                    row['face_and_boundary_passed']=row['face_streaming_consistency_absolute']<limits['face_continuity_absolute'] and row['radial_boundary_relative']<5e-12
                    np.savez_compressed(root/f'analysis/{kind}_{g}_{n}_{boundary}.npz',green=green,**fields)
                    result['cases'].append(row)
                print('mesh complete',g,kind,n,flush=True)
        for kind in ['exact','native']:
            coarse=np.load(root/f'analysis/{kind}_{g}_4_white.npz')['phi'][...,-2:]
            fine=np.load(root/f'analysis/{kind}_{g}_8_white.npz')['phi'][...,-2:]
            restricted=fine.reshape(8,4,2,2).mean(axis=2)
            weight=d['weights'][:8,None,None]*plan['height_cm']/4
            flux=np.sqrt(np.sum(weight*(coarse-restricted)**2,axis=(0,1))/np.sum(weight*restricted**2,axis=(0,1)))
            rows=[r for r in result['cases'] if r['group']==g and r['kernel']==kind and r['boundary']=='white']
            c=next(r for r in rows if r['n']==4);f=next(r for r in rows if r['n']==8)
            escape=abs(np.array(c['heldout_axial_escape'])-f['heldout_axial_escape'])/np.array(f['heldout_axial_escape'])
            result['mesh_checks'].append(dict(group=g,kernel=kind,coarse_n=4,fine_n=8,flux_relative=flux.tolist(),
                                                axial_escape_relative=escape.tolist(),passed=bool(max(*flux,*escape)<.01)))
        for n in plan['meshes']:
            for boundary in ['vacuum','white']:
                x=np.load(root/f'analysis/exact_{g}_{n}_{boundary}.npz');y=np.load(root/f'analysis/native_{g}_{n}_{boundary}.npz')
                result['kernel_comparisons'].append(dict(group=g,n=n,boundary=boundary,
                    scalar_max_case_relative=max(relative(y['phi'][...,i],x['phi'][...,i]) for i in range(x['phi'].shape[-1])),
                    face_current_relative=relative(y['face_current'],x['face_current'])))
    result['primitive_controls_passed']=all(max(r['dense_relative'],r['native_periodic_constant_relative'])<5e-12 for r in result['primitive_controls'])
    native=[r for r in result['cases'] if r['kernel']=='native']
    result['native_zero_gradient_passed']=all(r['native_action_passed'] for r in result['zero_gradient'] if r['kernel']=='native')
    result['native_finite_mesh_response_passed']=all(all(r[k] for k in ['positivity_passed','global_balance_passed','cell_balance_passed','face_and_boundary_passed']) for r in native)
    result['mesh_convergence_passed']=all(r['passed'] for r in result['mesh_checks'] if r['kernel']=='native')
    result['new_coupled_eigenreference_qualified']=False
    save_json(root/'analysis/result.json',result)
    print(json.dumps({k:v for k,v in result.items() if isinstance(v,bool)},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.artifact)

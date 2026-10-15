"""Native layer-local white closure using independently measured incoming area."""
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from native_oblique_streaming import ratio
from calibrate_native_oblique_streaming import read,save


def measures(d,H,nz,tracks=None,polars=range(4)):
    tracks=np.arange(len(d['nseg'])) if tracks is None else np.asarray(tracks)
    volume=[];radial=[];axial=[];mus=[]
    for p in polars:
        v=np.zeros(8);b=np.zeros(6);a=np.zeros(8)
        mu=np.sqrt(1-1/d['zmu'][p]**2)
        for track in tracks:
            nr=int(d['nseg'][track]-2);width=d['planar_widths'][track,:nr]*d['zmu'][p]
            reg=d['nom'][track,1:nr+1]-1;weight=d['wei'][track]*d['wzmu'][p]/2
            np.add.at(v,reg,2*weight*width*(H/nz))
            np.add.at(a,reg,2*weight*width*mu)
            b[d['entry_surface'][track]]+=weight*(H/nz)
            b[d['exit_surface'][track]]+=weight*(H/nz)
        for sign in [-1,1]:
            volume.append(np.repeat(v,nz));radial.append(np.repeat(b,nz));axial.append(a.copy());mus.append(sign*mu)
    return dict(volume=np.array(volume),radial=np.array(radial),axial=np.array(axial),mu=np.array(mus))


def evaluate(operator,jx,abs_jx,x,sigma,measure,stored_volume,nz):
    nv,nb=8*nz,6*nz
    y=np.einsum('srk,skc->src',operator,x,optimize=True)
    positive=np.einsum('srk,skc->src',operator,abs(x),optimize=True)
    integ=y[:,:nv];out=y[:,nv:];vol=stored_volume[:,None]
    birth=np.einsum('sr,src->c',measure['volume'],x[:,:nv])
    rin=np.einsum('sr,src->c',measure['radial'],x[:,nv:nv+nb])
    ain=np.einsum('sr,src->c',measure['axial'],x[:,nv+nb:nv+nb+8])
    collision=(integ*np.repeat(sigma,nz)[None,:,None]).sum(axis=(0,1))
    radial=out[:,:nb].sum(axis=0);axial=out[:,nb:].sum(axis=0)
    f=dict(phi=integ.sum(axis=0)/vol,jz=np.einsum('s,src->rc',measure['mu'],integ)/vol,
        jx=np.einsum('srk,skc->rc',jx,x,optimize=True)/vol,
        phi_scale=positive[:,:nv].sum(axis=0)/vol,
        jz_scale=np.einsum('s,src->rc',abs(measure['mu']),positive[:,:nv])/vol,
        jx_scale=np.einsum('srk,skc->rc',abs_jx,abs(x),optimize=True)/vol,
        radial=radial,axial=axial,birth=birth,radial_incoming=rin,axial_incoming=ain,collision=collision,
        global_defect=birth+rin+ain-collision-radial.sum(axis=0)-axial.sum(axis=0),
        global_scale=birth+rin+ain)
    return f


def solve_white(operator,jx,abs_jx,q,sigma,measure,stored_volume,nz,normalizer=None):
    ns=operator.shape[0];nv,nb=8*nz,6*nz;k=operator.shape[-1]
    geometric=measure['radial'].sum(axis=0)
    norm=geometric if normalizer is None else np.asarray(normalizer)
    if (norm<=0).any():raise ValueError('positive incoming measure required on every white face')
    transfer=operator[:,nv:nv+nb,nv:nv+nb].sum(axis=0)/norm[:,None]
    rhs=np.einsum('srk,skc->rc',operator[:,nv:nv+nb,:nv],q,optimize=True)/norm[:,None]
    matrix=np.eye(nb)-transfer
    inverse=np.linalg.solve(matrix,np.eye(nb));amplitudes=np.linalg.solve(matrix,rhs)
    x=np.zeros((ns,k,q.shape[-1]));x[:,:nv]=q;x[:,nv:nv+nb]=amplitudes
    f=evaluate(operator,jx,abs_jx,x,sigma,measure,stored_volume,nz)
    f.update(amplitudes=amplitudes,transfer=transfer,inverse=inverse,normalizer=norm,
        rho=float(max(abs(np.linalg.eigvals(transfer)))),matrix_residual=matrix@amplitudes-rhs,
        closure_defect=f['radial']-norm[:,None]*amplitudes,
        geometric_face_defect=f['radial']-geometric[:,None]*amplitudes,
        physical_defect=f['birth']-f['collision']-f['axial'].sum(axis=0),
        scalar_scale=abs(amplitudes).max(axis=0),rhs_scale=abs(rhs).max(axis=0))
    return f


def validate_white(f,physical=True):
    checks=dict(matrix=float(ratio(f['matrix_residual'],f['rhs_scale']).max()),
        closure=float(ratio(f['closure_defect'],abs(f['radial']).max(axis=0)).max()),
        physical=float(ratio(f['physical_defect'],f['birth']).max()),rho=f['rho'],
        minimum_amplitude=float(f['amplitudes'].min()),minimum_inverse=float(f['inverse'].min()),
        minimum_flux=float(f['phi'].min()),minimum_outgoing=float(min(f['radial'].min(),f['axial'].min())))
    assert max(checks['matrix'],checks['closure'])<5e-12 and checks['rho']<1,checks
    assert min(checks['minimum_amplitude'],checks['minimum_inverse'],checks['minimum_flux'],checks['minimum_outgoing'])>=0,checks
    if physical:assert checks['physical']<1e-10,checks
    return checks


def compare_actions(a,b):
    error={}
    for name in ['phi','jx','jz']:
        error[name]=float(ratio(a[name]-b[name],b[name+'_scale'].max(axis=0)).max())
    for name in ['radial','axial']:
        error[name]=float(ratio(a[name]-b[name],abs(b[name]).max(axis=0)).max())
    assert max(error.values())<5e-12,error
    return error


def main(root,family):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text())
    cases=[c for c in plan['batches'] if not c['preflight'] and c['id'].split('_b')[0][3:]==family]
    assert len(cases)==180
    H,nz=cases[0]['height'],cases[0]['nz'];nv,nb=8*nz,6*nz;k=14*nz+10
    d=read(root/'inputs/inventory.npz');measure=measures(d,H,nz)
    bypolar=[]
    for p in range(4):
        folder=root/'verification'/f'p{p}_{family}';r=json.loads((folder/'result.json').read_text())
        assert r['all_original_indices_once'] and r['original_tracks']==11364 and r['all_checks_passed']
        z=read(folder/'operators.npz');np.testing.assert_array_equal(z['coverage'],1);bypolar.append(z)
    # State order is polar-major, with independent negative and positive axial signs.
    op=np.concatenate([z['operators'].sum(axis=3) for z in bypolar],axis=2)
    jx=np.concatenate([z['jx'].sum(axis=3) for z in bypolar],axis=2)
    aj=np.concatenate([z['abs_jx'].sum(axis=3) for z in bypolar],axis=2)
    stored_volume=np.repeat(d['weights'][:8]*(H/nz),nz)
    stored_surface=np.repeat(d['weights'][8:]*(H/nz),nz)
    q=np.zeros((8,nv,8*nv+2));q[:,:,:8*nv]=np.eye(8*nv).reshape(8,nv,8*nv)
    q[:,:,-2]=np.arange(1,8*nv+1).reshape(8,nv)/(8*nv+1);q[:,:,-1]=1
    # All independent angular volume, radial and axial input coordinates.
    nbase=k-2;x=np.zeros((8,k,8*nbase));x[:,:nbase]=np.eye(8*nbase).reshape(8,nbase,8*nbase)
    folder=root/'white'/family;folder.mkdir();reports=[]
    for gi,sigma in enumerate(d['group_totals']):
        fixed=[];white=[];stored=[];checks=[]
        for qi,order in enumerate([16,32]):
            f=evaluate(op[qi,gi],jx[qi,gi],aj[qi,gi],x,sigma,measure,stored_volume,nz)
            fe=float(ratio(f['global_defect'],f['global_scale']).max());assert fe<1e-10
            fixed.append(f)
            w=solve_white(op[qi,gi],jx[qi,gi],aj[qi,gi],q,sigma,measure,stored_volume,nz)
            wc=validate_white(w);white.append(w)
            s=solve_white(op[qi,gi],jx[qi,gi],aj[qi,gi],q,sigma,measure,stored_volume,nz,stored_surface)
            sc=validate_white(s,physical=False);stored.append(s)
            assembly={}
            coeff=np.stack([q[:,:,-2].ravel(),q[:,:,-1].ravel()],axis=1)
            for name in ['phi','jx','jz','radial','axial','amplitudes']:
                scale=w.get(name+'_scale',abs(w[name]))[:,-2:].max(axis=0)
                assembly[name]=float(ratio(w[name][:,:-2]@coeff-w[name][:,-2:],scale).max())
            assert max(assembly.values())<5e-12,assembly
            checks.append(dict(order=order,fixed_balance=fe,geometric_white=wc,stored_normalizer_comparison=sc,source_assembly=assembly))
            np.savez_compressed(folder/f'g{[51,61,98][gi]}_q{order}.npz',**{'fixed_'+key:value for key,value in f.items()},
                **{'white_'+key:value for key,value in w.items()},**{'stored_'+key:value for key,value in s.items()})
        reports.append(dict(group=[51,61,98][gi],orders=checks,fixed_order_agreement=compare_actions(*fixed),white_order_agreement=compare_actions(*white)))
    np.savez_compressed(folder/'geometry.npz',**measure,stored_volume=stored_volume,stored_surface=stored_surface,q=q)
    result=dict(family=family,original_tracks=11364,independent_angular_states=8,white_source_coordinates=8*nv,
        physical_axial_incoming_zero=True,geometric_normalizer_used=True,stored_normalizer_is_separate_model=True,
        relative_volume_normalizer_difference=float(ratio(measure['volume'].sum(axis=0)-stored_volume,stored_volume).max()),
        relative_surface_normalizer_difference=float(ratio(measure['radial'].sum(axis=0)-stored_surface,stored_surface).max()),
        groups=reports,all_checks_passed=True,elapsed_seconds=time.perf_counter()-tick,
        peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(folder/'result.json',result);assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    print(family,'native white passed',round(result['elapsed_seconds'],2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('family');a=p.parse_args();main(a.root.resolve(),a.family)

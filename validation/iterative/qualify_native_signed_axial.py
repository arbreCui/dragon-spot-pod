#!/usr/bin/env python3
"""Zero-gradient signed axial-state experiment using frozen native B/D flights."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native, segment_step, cases_for_group, relative, save_json


def axial_mu(d):
    z=np.asarray(d['zmu'],float)
    if np.any(z<1) or not np.isfinite(z).all():raise ValueError('invalid native path scale')
    return np.sqrt(1-1/z**2)


def angular_measures(d):
    """Per-axial-sign geometric volumes/surface measures, retaining native error."""
    v=np.zeros((d['nmu'],d['nr']));s=np.zeros((d['nmu'],d['nb']))
    for step in range(1,d['nmax']-1):
        lines=np.flatnonzero(step<d['length']-1);reg=d['region'][lines,step]-1
        # Two planar directions cancel the 1/2 weight of a single axial sign.
        np.add.at(v,(d['polar'][lines],reg),d['weight'][lines]*d['h'][lines,step])
    for end in [np.zeros(len(d['track']),dtype=int),d['length']-1]:
        surface=-d['region'][np.arange(len(end)),end]-1
        np.add.at(s,(d['polar'],surface),d['weight']/2)
    return v,s


def signed_sweep(d,a,q,inflow,batch=24):
    """q[z,polar,region,case]; inflow[z,polar,surface,case].

    Both planar orientations use the same independently supplied axial sign.
    Returned iso/own/boundary are native weighted integrals before normalization.
    """
    nr,nb,nmu=d['nr'],d['nb'],d['nmu'];nc=q.shape[-1];nl=len(d['track'])
    assert q.shape==(2,nmu,nr,nc) and inflow.shape==(2,nmu,nb,nc)
    if not np.isfinite(q).all() or not np.isfinite(inflow).all():raise ValueError('nonfinite input')
    result=dict(iso=np.zeros((2,nmu,nr,nc)),own=np.zeros((2,nmu,nr,nc)),
                boundary=np.zeros((2,nmu,nb,nc)),minima=np.full((3,nc),np.inf),negative_counts=np.zeros((3,nc),int))
    for start in range(0,nc,batch):
        stop=min(nc,start+batch);block=slice(start,stop)
        for z in range(2):
            for orientation in [1,-1]:
                entrance=np.zeros(nl,dtype=int) if orientation==1 else d['length']-1
                surface=-d['region'][np.arange(nl),entrance]-1
                incoming=inflow[z,d['polar'],surface,block].copy()
                for step in range(1,d['nmax']-1):
                    lines=np.flatnonzero(step<d['length']-1)
                    seg=np.full(len(lines),step) if orientation==1 else d['length'][lines]-1-step
                    reg=d['region'][lines,seg]-1;polar=d['polar'][lines]
                    src=q[z,polar,reg,block];inc=incoming[lines]
                    out,f0,fs=segment_step(inc,src,a['total'][reg,None],a['b'][lines,seg,None],a['self_d'][lines,seg,None])
                    weight=d['weight'][lines,None]/2
                    np.add.at(result['iso'][z,:,:,block],(polar,reg),f0*weight)
                    np.add.at(result['own'][z,:,:,block],(polar,reg),fs*weight)
                    for index,x in enumerate([inc,out,f0+fs]):
                        result['minima'][index,block]=np.minimum(result['minima'][index,block],x.min(axis=0))
                        result['negative_counts'][index,block]+=np.sum(x<0,axis=0)
                    incoming[lines]=out
                end=d['length']-1 if orientation==1 else np.zeros(nl,dtype=int)
                surface=-d['region'][np.arange(nl),end]-1
                np.add.at(result['boundary'][z,:,:,block],(d['polar'],surface),incoming*d['weight'][:,None]/2)
    return result


def moments(d,integrals,boundary):
    v=d['weights'][:d['nr']];surf=d['weights'][d['nr']:]
    return (integrals.sum(axis=(0,1))/v[:,None],
            np.einsum('prc,p->rc',integrals[0]-integrals[1],axial_mu(d))/v[:,None],
            boundary.sum(axis=(0,1))/surf[:,None])


def common_white(tbb,source_out,nmu):
    b=np.linalg.solve(np.eye(len(tbb))-tbb,source_out)
    return np.broadcast_to(b,(2,nmu,*b.shape)).copy()


def ledger(d,a,q,inflow,integrals,boundary):
    vw,sw=angular_measures(d);mu=np.array([1.,-1.])[:,None]*axial_mu(d)[None,:]
    data={}
    for name,weight in [('even',np.ones_like(mu)),('odd',mu)]:
        born=np.einsum('zprc,pr,zp->c',q,vw,weight)
        jin=np.einsum('zpsc,ps,zp->c',inflow,sw,weight)
        collision=np.einsum('zprc,r,zp->c',integrals,a['total'],weight)
        jout=np.einsum('zpsc,zp->c',boundary,weight)
        scale=np.einsum('zprc,pr,zp->c',abs(q),vw,abs(weight))+np.einsum('zpsc,ps,zp->c',abs(inflow),sw,abs(weight))
        data[name+'_birth']=born;data[name+'_incoming']=jin;data[name+'_collision']=collision;data[name+'_outgoing']=jout
        data[name+'_defect']=born+jin-collision-jout
        data[name+'_relative']=abs(data[name+'_defect'])/np.maximum(scale,1e-300)
    return data


def load_fixture(aroot):
    return load_native(aroot/'inputs/track_data.bin')


def prepare(aroot):
    d=load_fixture(aroot);op=np.load(aroot/'inputs/operator_fields.npz')
    previous=np.loadtxt(aroot/'inputs/previous_flight_sources.txt',skiprows=1)
    mu=axial_mu(d);nr,nb,npole=d['nr'],d['nb'],d['nmu'];nv=2*npole*nr;ns=2*npole*nb
    geom=dict(axial_signs=[1,-1],axial_direction_magnitude=mu.tolist(),native_cpo=d['cpo'].tolist(),
              max_mu_vs_abs_cpo_difference=float(np.max(abs(mu-abs(d['cpo'])))),
              oriented_states=4*len(d['track']),signed_axial_extension=True,
              native_original_axial_sign_available=False)
    norm=d['azx'][d['azimuth']]**2/d['zmu'][d['polar']]**2+d['azy'][d['azimuth']]**2/d['zmu'][d['polar']]**2+mu[d['polar']]**2
    geom['unit_direction_max_error']=float(np.max(abs(norm-1)));assert geom['unit_direction_max_error']<1e-14
    save_json(aroot/'analysis/geometry.json',geom)
    for a in d['group_data']:
        g=a['group'];legacy=cases_for_group(d,op,previous,g)
        nlegacy=legacy.shape[1]
        qleg=np.broadcast_to(legacy[:nr],(2,npole,nr,nlegacy)).copy()
        ileg=np.broadcast_to(legacy[nr:],(2,npole,nb,nlegacy)).copy()
        qunit=np.eye(nv).reshape(2,npole,nr,nv);iunit=np.eye(ns).reshape(2,npole,nb,ns)
        q=np.concatenate([qleg,qunit,np.zeros((2,npole,nr,ns))],axis=-1)
        inc=np.concatenate([ileg,np.zeros((2,npole,nb,nv)),iunit],axis=-1)
        tags=['legacy_isotropic']*nlegacy+['angular_volume_vacuum']*nv+['angular_boundary_open']*ns
        x=signed_sweep(d,a,q,inc);surf=d['weights'][nr:]
        volidx=slice(nlegacy,nlegacy+nv);bidx=slice(nlegacy+nv,nlegacy+nv+ns)
        # Source-to-outgoing response measured at the actual retained angles.
        oq=x['boundary'][...,volidx].sum(axis=(0,1))/surf[:,None]
        ob=x['boundary'][...,bidx].sum(axis=(0,1))/surf[:,None]
        common_map=np.tile(np.eye(nb),(2*npole,1))
        tbb=ob@common_map
        assert relative(tbb,op['flight'][g-1,nr:,nr:])<5e-12
        iw=common_white(tbb,oq,npole)
        profile=np.arange(1,nr+1)/16
        odd=np.array([1.,-1.])[:,None,None]*mu[None,:,None]*profile[None,None,:]
        qp=1+odd[:,:,:,None]*np.array([-1.,0.,1.])[None,None,None,:]
        jp=oq@qp.reshape(nv,3);ip=common_white(tbb,jp,npole)
        # Deliberately different boundary model: each sign returns independently.
        wrong=np.zeros_like(ip);bad_tbb=[]
        for z in range(2):
            ozb=2*x['boundary'][z,...,bidx].sum(axis=0)/surf[:,None]
            select=np.zeros((ns,nb));select[z*npole*nb:(z+1)*npole*nb]=np.tile(np.eye(nb),(npole,1))
            tz=ozb@select;bad_tbb.append(tz)
            ozq=2*x['boundary'][z,...,volidx].sum(axis=0)/surf[:,None]
            bz=np.linalg.solve(np.eye(nb)-tz,ozq@qp.reshape(nv,3))
            wrong[z]=np.broadcast_to(bz,(npole,nb,3))
        extraq=np.concatenate([qunit,qp,qp,qp],axis=-1)
        extrai=np.concatenate([iw,np.zeros_like(ip),ip,wrong],axis=-1)
        y=signed_sweep(d,a,extraq,extrai)
        q=np.concatenate([q,extraq],axis=-1);inc=np.concatenate([inc,extrai],axis=-1)
        tags+=['angular_volume_white']*nv+['pair_vacuum']*3+['pair_white']*3+['pair_wrong_sign_return']*3
        fields={k:np.concatenate([x[k],y[k]],axis=-1) for k in x}
        assert len(tags)==216 and q.shape[-1]==216
        np.savez_compressed(aroot/f'analysis/prepared_{g}.npz',q=q,inflow=inc,tbb=tbb,bad_tbb=np.array(bad_tbb),legacy=legacy,**fields)
        save_json(aroot/f'analysis/cases_{g}.json',tags)
        with (aroot/f'runs/sources_{g}.txt').open('x') as f:
            f.write(str(len(tags))+'\n')
            for c in range(len(tags)):
                values=np.r_[q[...,c].ravel(),inc[...,c].ravel()]
                f.write(str(g)+' '+' '.join(format(float(v),'.17e') for v in values)+'\n')
        print('Prepared group',g,len(tags),'prescribed flights',flush=True)


def read_native(path):
    with Path(path).open('rb') as f:
        magic,nr,nb,nmu,ncase=np.fromfile(f,'<i4',count=5)
        assert magic==290902
        meta=np.fromfile(f,'<f4',count=nr+nb+3*nmu)
        assert np.isfinite(meta).all()
        iso=[];own=[];groups=[]
        for c in range(ncase):
            g,index=np.fromfile(f,'<i4',count=2);assert index==c+1
            iso.append(np.fromfile(f,'<f8',count=2*nmu*(nr+nb)).reshape(2,nmu,nr+nb))
            own.append(np.fromfile(f,'<f8',count=2*nmu*nr).reshape(2,nmu,nr))
            groups.append(g)
        assert not f.read(1)
    return np.stack(iso,axis=-1),np.stack(own,axis=-1),np.array(groups),meta


def finish(aroot):
    d=load_fixture(aroot);mu=axial_mu(d);v=d['weights'][:8];surface=d['weights'][8:]
    old=np.genfromtxt(aroot/'inputs/scalar.csv',delimiter=',',names=True)
    result=dict(scope='Explicit axial-sign extension at zero axial variation only',groups=[])
    for a in d['group_data']:
        g=a['group'];p=np.load(aroot/f'analysis/prepared_{g}.npz');tags=np.array(json.loads((aroot/f'analysis/cases_{g}.json').read_text()))
        nf,ns,ng,meta=read_native(aroot/f'runs/native_{g}.bin');assert np.all(ng==g)
        np.testing.assert_array_equal(meta[:14],d['weights'])
        np.testing.assert_array_equal(meta[14:],np.r_[d['cpo'],d['zmu'],d['wzmu']])
        raw=p['iso']+p['own'];native=nf[:,:,:8]+ns
        nc=p['q'].shape[-1]
        per_case=[relative(np.r_[raw[...,i].ravel(),p['boundary'][...,i].ravel()],
                           np.r_[native[...,i].ravel(),nf[:,:,8:,i].ravel()]) for i in range(nc)]
        assert max(per_case)<5e-12
        assert relative(p['iso'],nf[:,:,:8])<5e-12 and relative(p['own'],ns)<5e-12
        phi,jz,outgoing=moments(d,raw,p['boundary'])
        native_phi,native_jz,native_out=moments(d,native,nf[:,:,8:])
        assert relative(jz,native_jz)<5e-12
        positive=(p['q'].min(axis=(0,1,2))>=0)&(p['inflow'].min(axis=(0,1,2))>=0)
        assert np.all(p['minima'][:,positive]>=0) and np.all(p['negative_counts'][:,positive]==0)
        assert np.all(native[...,positive]>=0) and np.all(nf[:,:,8:,positive]>=0)
        # The only stored rounding completion used is that measured for P0.
        delta=a['pjj']-2*a['pjsum']/v
        completed=phi[:,:31]+delta[:,None]*p['legacy'][:8]
        previous=old[old['group']==g]['response'].reshape(31,14).T
        calibration=max(relative(np.r_[completed[:,i],outgoing[:,i]],previous[:,i]) for i in range(31))
        assert calibration<5e-12
        np.testing.assert_allclose(jz[:,:31],0,atol=5e-14)
        audit=ledger(d,a,p['q'],p['inflow'],raw,p['boundary'])
        assert max(audit['even_relative'].max(),audit['odd_relative'].max())<1e-6
        pair={tag:np.flatnonzero(tags==tag) for tag in ['pair_vacuum','pair_white','pair_wrong_sign_return']}
        parity={}
        for tag,idx in pair.items():
            parity[tag+'_scalar']=relative((phi[:,idx[0]]+phi[:,idx[2]])/2,phi[:,idx[1]])
            parity[tag+'_current']=float(np.max(abs(jz[:,idx[0]]+jz[:,idx[2]]))/max(float(np.max(abs(phi[:,idx]))),1e-300))
        assert max(parity.values())<5e-12
        vac=pair['pair_vacuum'];white=pair['pair_white'];wrong=pair['pair_wrong_sign_return']
        odd_vac=(jz[:,vac[2]]-jz[:,vac[0]])/2
        odd_white=(jz[:,white[2]]-jz[:,white[0]])/2
        odd_wrong=(jz[:,wrong[2]]-jz[:,wrong[0]])/2
        correct_identity=relative(odd_white,odd_vac);assert correct_identity<5e-12
        assert np.max(abs(odd_white))>1e-6
        admitted_white=(tags=='angular_volume_white')|(tags=='pair_white')
        common=p['inflow'][0,0,:,admitted_white].T
        closure=relative(outgoing[:,admitted_white],common);assert closure<5e-12
        assert np.max(abs(audit['odd_incoming'][admitted_white]))<5e-13
        maskwrong=tags=='pair_wrong_sign_return'
        wrong_even=relative(phi[:,wrong],phi[:,white])
        wrong_change=relative(odd_wrong,odd_white);assert wrong_change>1e-3
        vw,sw=angular_measures(d)
        incoming_native=np.einsum('sc,s->c',outgoing[:,admitted_white],surface)
        # This is the native surface-weight ledger; geometric incoming is separately retained.
        white_stored_defect=incoming_native-np.sum(p['boundary'][...,admitted_white],axis=(0,1,2))
        record=dict(group=g,cases=nc,nonnegative_cases=int(positive.sum()),
                    negative_retained_values_in_nonnegative_cases=int(p['negative_counts'][:,positive].sum()),
                    negative_retained_values_in_signed_cases=int(p['negative_counts'][:,~positive].sum()),
                    native_half_state_max_case_relative=max(per_case),native_Jz_relative=relative(jz,native_jz),
                    native_P0_calibration_max_case_relative=calibration,
                    raw_even_balance_relative=float(audit['even_relative'].max()),raw_odd_balance_relative=float(audit['odd_relative'].max()),
                    white_closure_relative=closure,white_stored_current_defect_max=float(np.max(abs(white_stored_defect))),
                    white_geometric_current_defect_max=float(np.max(abs(audit['even_incoming'][admitted_white]-audit['even_outgoing'][admitted_white]))),
                    white_incoming_axial_moment_max=float(np.max(abs(audit['odd_incoming'][admitted_white]))),
                    correct_white_vs_vacuum_odd_relative=correct_identity,measured_axial_odd_current=odd_white.tolist(),
                    wrong_sign_return_odd_current=odd_wrong.tolist(),wrong_sign_return_relative_change=wrong_change,
                    wrong_sign_return_even_scalar_relative=wrong_even,
                    wrong_sign_return_incoming_axial_moment_max=float(np.max(abs(audit['odd_incoming'][maskwrong]))),
                    pair_parity=parity,axial_propagation_qualified=False)
        result['groups'].append(record)
        np.savez_compressed(aroot/f'analysis/result_{g}.npz',phi=phi,jz=jz,outgoing=outgoing,
                            native_half_integrals=native,native_half_outgoing=nf[:,:,8:],native_phi=native_phi,
                            native_jz=native_jz,p0_completed=completed,old_native=previous,
                            white_odd=odd_white,vacuum_odd=odd_vac,wrong_sign_odd=odd_wrong,**audit)
    result.update(signed_state_zero_gradient_checks_passed=True,white_boundary_mixes_axial_signs=True,
                  original_P0_identifies_unique_axial_law=False,axial_propagation_qualified=False,new_coupled_reference_qualified=False)
    save_json(aroot/'analysis/result.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('artifact',type=Path)
    parser.add_argument('--phase',choices=['prepare','finish'],required=True)
    args=parser.parse_args();globals()[args.phase](args.artifact)

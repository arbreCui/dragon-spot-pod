#!/usr/bin/env python3
"""Retain native track response as a recurrence; audit its scalar and planar moments.

No axial sign is attached to an in-plane track orientation. Native PJJ rounding
is a separate scalar ledger, never fitted into an angular bin.
"""
import argparse
import json
from pathlib import Path
import numpy as np


def save_json(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False); f.write('\n')


def relative(x, y):
    return float(np.max(np.abs(x-y))/max(float(np.max(np.abs(y))), 1e-300))


def load_native(path):
    with Path(path).open('rb') as f:
        def read(dtype, shape):
            if isinstance(shape, int): shape=(shape,)
            x=np.fromfile(f, dtype=dtype, count=int(np.prod(shape)))
            assert x.size==np.prod(shape), 'short native binary'
            return x.reshape(shape, order='F')
        magic,nr,nb,ng,nt,nmax,nmu,na,m=read('<i4',9).tolist()
        assert magic==290901 and (nr,nb,ng)==(8,6,3)
        d=dict(nr=nr,nb=nb,ng=ng,nt=nt,nmax=nmax,nmu=nmu,na=na)
        d['groups']=read('<i4',ng);d['zone']=read('<i4',nr+nb)
        for k,n in [('weights',nr+nb),('cpo',nmu),('zmu',nmu),('wzmu',nmu)]:
            d[k]=read('<f4',n).astype(float)
        d['azx']=read('<f8',na);d['azy']=read('<f8',na)
        d['harm']=read('<f4',(nmu,3,na)).astype(float)
        d['nseg']=read('<i4',nt);d['angle']=read('<i4',nt)-1
        d['nom']=read('<i4',(nmax,nt)).T
        d['h2']=read('<f8',(nmax,nt)).T;d['wei']=read('<f8',nt)
        d['group_data']=[]
        for g in d['groups']:
            a=dict(group=int(g))
            for k in ['total','pjj','pjj_rebuilt']: a[k]=read('<f4',nr).astype(float)
            a['pjsum']=read('<f8',nr)
            for k in ['b','self_d']:
                a[k]=read('<f8',(nmax,nmu,nt)).transpose(2,1,0).reshape(nt*nmu,nmax)
            controls=[]
            for _ in range(3): controls.append((read('<f8',2*nr+nb),read('<f8',2*nr)))
            a['controls']=controls;d['group_data'].append(a)
        d['single_segment']=[read('<f8',3+2*nr+nb) for _ in range(3)]
        assert not f.read(1), 'trailing native data'
    d['track']=np.repeat(np.arange(nt),nmu)
    d['polar']=np.tile(np.arange(nmu),nt)
    d['region']=d['nom'][d['track']]
    d['length']=d['nseg'][d['track']]
    d['azimuth']=d['angle'][d['track']]
    d['bin']=d['azimuth']*nmu+d['polar']
    d['weight']=d['wei'][d['track']]*d['wzmu'][d['polar']]
    d['h']=d['h2'][d['track']]*d['zmu'][d['polar'],None]
    d['mx']=d['harm'][d['polar'],2,d['azimuth']]
    d['my']=d['harm'][d['polar'],1,d['azimuth']]
    return d


def segment_step(incoming, source, total, b, own):
    """Native MCGFFIR operation order, full integral with native own-source D."""
    outgoing=incoming+b*(source-total*incoming)
    isolated=b*incoming
    return outgoing,isolated,own*source


def sweep(d, a, even, inflow, odd=None, trace_column=None):
    """Source profiles have shape (region/surface, case); odd multiplies native x.

    Exported B/D/geometry retain the source-to-segment map without materializing
    a very large dense angular matrix. Fields in bins are weighted integrals,
    not local flux samples. The optional trace stores actual segment amplitudes.
    """
    nr,nb=d['nr'],d['nb'];nc=even.shape[1];nl=len(d['track']);nm=d['nmax']
    if odd is None: odd=np.zeros_like(even)
    assert even.shape==odd.shape and inflow.shape==(nb,nc)
    iso=np.zeros((2,d['na']*d['nmu'],nr,nc));own=np.zeros_like(iso)
    boundary=np.zeros((2,d['na']*d['nmu'],nb,nc));birth=np.zeros(nc)
    extrema={'incoming_min':1e300,'outgoing_min':1e300,'integral_min':1e300,
             'negative_incoming_count':0,'negative_outgoing_count':0,'negative_integral_count':0}
    trace={k:np.zeros((2,nl,nm)) for k in ['incoming','outgoing','source']} if trace_column is not None else {}
    for direction,sign in enumerate([1,-1]):
        entrance=np.zeros(nl,dtype=int) if sign==1 else d['length']-1
        surface=-d['region'][np.arange(nl),entrance]-1
        incoming=inflow[surface].copy()
        for step in range(1,nm-1):
            lines=np.flatnonzero(step<d['length']-1)
            seg=np.full(len(lines),step) if sign==1 else d['length'][lines]-1-step
            reg=d['region'][lines,seg]-1
            q=even[reg]+sign*d['mx'][lines,None]*odd[reg]
            inc=incoming[lines]
            out,f0,fs=segment_step(inc,q,a['total'][reg,None],a['b'][lines,seg,None],a['self_d'][lines,seg,None])
            for label,x in [('incoming',inc),('outgoing',out),('integral',f0+fs)]:
                extrema[label+'_min']=min(extrema[label+'_min'],float(x.min()))
                extrema['negative_'+label+'_count']+=int(np.sum(x<0))
            weight=d['weight'][lines,None]
            np.add.at(iso[direction],(d['bin'][lines],reg),f0*weight)
            np.add.at(own[direction],(d['bin'][lines],reg),fs*weight)
            birth+=np.sum(q*(d['h'][lines,seg,None]*weight),axis=0)
            if trace_column is not None:
                for k,x in [('incoming',inc),('outgoing',out),('source',q)]:
                    trace[k][direction,lines,seg]=x[:,trace_column]
            incoming[lines]=out
        exit_seg=d['length']-1 if sign==1 else np.zeros(nl,dtype=int)
        surface=-d['region'][np.arange(nl),exit_seg]-1
        np.add.at(boundary[direction],(d['bin'],surface),incoming*d['weight'][:,None])
    v=d['weights'][:nr]
    full=(iso+own).sum(axis=(0,1))/v[:,None]
    raw_iso=iso.sum(axis=(0,1))/v[:,None]
    pjj_defect=a['pjj']-2*a['pjsum']/v
    # The source pair is +x/-x: its local even source is exactly `even`.
    completion=pjj_defect[:,None]*even
    scalar=full+completion
    outgoing=boundary.sum(axis=(0,1))/d['weights'][nr:,None]
    # Native harmonic values are constant in every (azimuth,polar) bin.
    mx=d['harm'][:,2,:].T.reshape(-1)
    current=((iso[0]+own[0])-(iso[1]+own[1]))
    current=np.einsum('arc,a->rc',current,mx)/v[:,None]
    return dict(iso=iso,own=own,boundary=boundary,full=full,scalar=scalar,raw_iso=raw_iso,
                current=current,outgoing=outgoing,completion=completion,birth=birth,
                extrema=extrema,trace=trace)


def check_single_segments(d):
    rows=[]
    for raw in d['single_segment']:
        h,b,own=raw[:3];native=raw[3:];sigma=2.
        exact_b=-np.expm1(-sigma*h)/sigma
        exact_d=(h-exact_b)/sigma
        inp=np.array([.7,1.1]);q=np.array([1.3,.4])
        out,f0,fs=segment_step(inp,q,sigma,b,own)
        exact_out=inp*np.exp(-sigma*h)+q*exact_b
        exact_int=exact_b*inp+exact_d*q
        np.testing.assert_allclose(native[[17,16]],out,rtol=5e-15,atol=1e-15)
        np.testing.assert_allclose(native[[0,8]],[sum(f0),f0[0]-f0[1]],rtol=5e-15,atol=1e-15)
        row=dict(optical_length=float(sigma*h),outgoing_relative=relative(out,exact_out),
                 integral_relative=relative(f0+fs,exact_int),b_relative=abs(b-exact_b)/exact_b,
                 own_relative=abs(own-exact_d)/exact_d)
        assert row['outgoing_relative']<2e-6 and row['integral_relative']<2e-6
        rows.append(row)
    return rows


def cases_for_group(d, operator, previous, g):
    # Original four held-out open-flight patterns are retained verbatim.
    base=previous[:18,1:].T
    q=np.column_stack([np.eye(8),np.ones(8),np.arange(1,9),np.eye(8)[0],
                       np.eye(8)[-1],(-1.)**np.arange(8)*np.arange(1,9)])
    q[:,8:]/=d['weights'][:8]@abs(q[:,8:])
    t=operator['flight'][g-1]
    jout=np.linalg.solve(np.eye(6)-t[8:,8:],t[8:,:8])@q
    return np.column_stack([base,np.vstack([q,jout])])


def main(artifact, output=None):
    aroot=Path(artifact);out=Path(output) if output else aroot/'analysis';out.mkdir(exist_ok=True)
    d=load_native(aroot/'runs/track_data.bin')
    operator=np.load(aroot/'inputs/operator_fields.npz')
    previous=np.loadtxt(aroot/'inputs/previous_flight_sources.txt',skiprows=1)
    native=np.genfromtxt(aroot/'runs/scalar.csv',delimiter=',',names=True)
    geometry={k:d[k] for k in ['groups','zone','weights','cpo','zmu','wzmu','azx','azy','harm','nseg','angle','nom','h2','wei']}
    np.savez_compressed(out/'geometry.npz',**geometry)
    v=d['weights'][:8];surface=d['weights'][8:]
    h=d['h'];mask=(np.arange(d['nmax'])[None,:]>0)&(np.arange(d['nmax'])[None,:]<d['length'][:,None]-1)
    angle_err=float(np.max(abs(d['azx']**2+d['azy']**2-1)))
    sin_from_cpo=np.sqrt(1-d['cpo']**2)
    mu_geom=d['azx'][d['azimuth']]/d['zmu'][d['polar']]
    geom=dict(tracks=d['nt'],polar_angles=d['nmu'],azimuthal_angles=d['na'],
              oriented_track_polar_pairs=2*len(d['track']),physical_segments=int(np.sum(d['nseg']-2)),
              oriented_segment_samples=int(2*np.sum(mask)),azimuth_unit_norm_max_error=angle_err,
              sin_from_cpo_vs_inverse_zmu_max_difference=float(np.max(abs(sin_from_cpo-1/d['zmu']))),
              native_harmonic_x_vs_flight_geometry_max_difference=float(np.max(abs(d['mx']-mu_geom))),
              native_polar_nodes=d['cpo'].tolist(),native_polar_weights_times_sin=d['wzmu'].tolist(),
              inferred_polar_weight_sum=float(np.sum(d['wzmu']*d['zmu'])),
              axial_odd_harmonic_available=False)
    quadrature_vol=np.zeros(8);quadrature_surface=np.zeros(6)
    np.add.at(quadrature_vol,d['region'][mask]-1,(2*d['weight'][:,None]*h)[mask])
    for end in [np.zeros(len(d['track']),dtype=int),d['length']-1]:
        np.add.at(quadrature_surface,-d['region'][np.arange(len(end)),end]-1,d['weight'])
    geom['reintegrated_volume_relative']=relative(quadrature_vol,v)
    geom['reintegrated_surface_relative']=relative(quadrature_surface,surface)
    assert max(geom['reintegrated_volume_relative'],geom['reintegrated_surface_relative'])<1e-6
    assert angle_err<1e-12 and np.all(d['weight']>0)
    report=dict(scope='Native planar directional response; no axial/coupled reference admitted',
                geometry=geom,single_segment_controls=check_single_segments(d),groups=[])
    for ga in d['group_data']:
        g=ga['group'];s=cases_for_group(d,operator,previous,g)
        n=s.shape[1];rows=native[native['group']==g]
        actual=rows['response'].reshape(n,14).T
        np.testing.assert_array_equal(rows['source'].reshape(n,14).T,s)
        x=sweep(d,ga,s[:8],s[8:],trace_column=18)
        predicted=operator['flight'][g-1]@s
        raw_completion=x['raw_iso']+ga['pjj'][:,None]*s[:8]
        completed=np.vstack([x['scalar'],x['outgoing']])
        errors=dict(retained_action_relative=relative(completed,actual),
                    retained_action_max_case_relative=max(relative(completed[:,i],actual[:,i]) for i in range(n)),
                    isolated_plus_stored_pjj_relative=relative(np.vstack([raw_completion,x['outgoing']]),actual),
                    previous_flight_matrix_relative=relative(predicted,actual),
                    directional_full_before_rounding_relative=relative(np.vstack([x['full'],x['outgoing']]),actual))
        assert max(errors[k] for k in errors if k!='directional_full_before_rounding_relative')<5e-12
        np.testing.assert_array_equal(ga['pjj'],ga['pjj_rebuilt'])
        direct_r=actual[:8,18:26];direct_j=actual[8:,18:26]
        errors['white_unit_response_relative']=relative(direct_r,operator['response'][g-1])
        errors['white_unit_outgoing_relative']=relative(direct_j,operator['outgoing'][g-1])
        assert errors['white_unit_response_relative']<5e-12 and errors['white_unit_outgoing_relative']<5e-12
        # Isotropic scalar ledger keeps the historical physical source normalization.
        balance=v@s[:8]+surface@s[8:]-(v*ga['total'])@x['scalar']-surface@x['outgoing']
        scale=v@abs(s[:8])+surface@abs(s[8:])
        raw_balance=float(np.max(abs(balance)/scale))
        assert raw_balance<1e-6
        positive=(np.min(s,axis=0)>=0)
        xp=sweep(d,ga,s[:8,positive],s[8:,positive])
        # No coefficient or amplitude is clipped. Report roundoff signs exactly.
        transmission=1-ga['b'][mask]*ga['total'][(d['region'][mask]-1)]
        table_d_balance=(h[mask]-ga['b'][mask])/ga['total'][d['region'][mask]-1]
        pjj_defect=ga['pjj']-2*ga['pjsum']/v
        assert np.isfinite(ga['b']).all() and np.isfinite(ga['self_d']).all()
        assert np.all(ga['b'][mask]>=0) and np.all(transmission>=0) and np.all(ga['self_d'][mask]>=0)
        assert all(xp['extrema'][k]>=0 for k in ['incoming_min','outgoing_min','integral_min'])
        # Odd profile is separate prescribed angular input to the native callback.
        even=np.ones((8,3));odd=np.arange(1,9)[:,None]/16*np.array([-1.,0.,1.])[None,:]
        directional=sweep(d,ga,even,np.zeros((6,3)),odd)
        af=np.column_stack([c[0] for c in ga['controls']]);sf=np.column_stack([c[1] for c in ga['controls']])
        native_scalar=(af[:8]+sf[:8])/v[:,None]
        native_current=(af[8:16]+sf[8:16])/v[:,None]
        native_outgoing=af[16:]/surface[:,None]
        pair_errors=dict(scalar_relative=relative(directional['full'],native_scalar),
                         current_relative=relative(directional['current'],native_current),
                         outgoing_relative=relative(directional['outgoing'],native_outgoing),
                         equal_even_response_midpoint_relative=relative((directional['full'][:,0]+directional['full'][:,2])/2,directional['full'][:,1]),
                         current_midpoint_relative=relative((directional['current'][:,0]+directional['current'][:,2])/2,directional['current'][:,1]))
        # The zero-odd current may vanish by symmetry; compare midpoint in total field units.
        pair_errors['current_midpoint_relative']=float(np.max(abs((directional['current'][:,0]+directional['current'][:,2])/2-directional['current'][:,1]))/np.max(abs(directional['full'])))
        assert max(pair_errors.values())<5e-12
        delta=(directional['current'][:,2]-directional['current'][:,0])/2
        assert np.max(abs(delta))>1e-6
        assert directional['extrema']['integral_min']>=0
        pair_balance=v@even-(v*ga['total'])@directional['scalar']-surface@directional['outgoing']
        pair_balance_relative=float(np.max(abs(pair_balance)/(v@even)))
        assert pair_balance_relative<1e-6
        record=dict(group=g,cases=n,positive_cases=int(positive.sum()),errors=errors,
                    pjj_binary32_exact=True,pjj_rounding_ledger=pjj_defect.tolist(),
                    max_raw_balance_relative=raw_balance,positive_input_extrema=xp['extrema'],
                    min_transmission=float(transmission.min()),negative_transmissions=int(np.sum(transmission<0)),
                    minimum_native_self_integral=float(ga['self_d'][mask].min()),
                    max_native_self_vs_balance_integral_absolute=float(np.max(abs(ga['self_d'][mask]-table_d_balance))),
                    directional_pair_errors=pair_errors,directional_pair_extrema=directional['extrema'],
                    directional_pair_raw_balance_relative=pair_balance_relative,
                    measured_x_odd_current=delta.tolist(),measured_x_odd_current_inf=float(np.max(abs(delta))),
                    axial_odd_response_identified=False)
        report['groups'].append(record)
        np.savez_compressed(out/f'coefficients_{g}.npz',b=ga['b'],self_d=ga['self_d'],total=ga['total'],pjj=ga['pjj'],
                            pjsum=ga['pjsum'],pjj_rounding_ledger=pjj_defect)
        np.savez_compressed(out/f'fields_{g}.npz',sources=s,native=actual,retained=completed,
                            isolated=x['iso'],self_source=x['own'],boundary=x['boundary'],
                            scalar_rounding_completion=x['completion'],raw_balance=balance,
                            directional_scalar=directional['full'],directional_current=directional['current'],
                            directional_outgoing=directional['outgoing'],directional_odd_source_profile=odd,
                            directional_pair_raw_balance=pair_balance,
                            directional_native_scalar=native_scalar,directional_native_current=native_current,
                            **{'trace_'+k:value for k,value in x['trace'].items()})
    report['native_planar_aggregation_passed']=True
    report['directional_scalar_rounding_ledger_required']=True
    report['axial_odd_response_identified']=False
    report['new_coupled_reference_qualified']=False
    save_json(out/'result.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();main(args.artifact,args.output)

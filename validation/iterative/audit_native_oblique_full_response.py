"""Bounded raw-witness and independent reference audit for one full H/Nz family."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from native_oblique_streaming import independent_flight,checks,ratio
from audit_native_oblique_streaming_calibration import audit_fields
from calibrate_native_oblique_streaming import read,save
from native_oblique_track_geometry import geometry
from native_oblique_track_pilot import direct_flight,transport as literal


def track_regional_reference(refs,counts,regions,H,nz):
    nt=len(counts);value=np.zeros((nt,3,8,nz,14))
    for i in range(15):
        ix=np.flatnonzero(i<counts)
        if not len(ix):continue
        for group in range(3):
            for z in range(nz):value[ix,group,regions[ix,i],z]+=refs['integral'][group,ix,i]*(H/nz)
    return value


def literal_witness(root,d,where,target):
    c=where['case'];track=where['track'];group=where['group_index'];col=where['input'];o=where['orientation'];sign=where['sign'];q=where['order'];p=c['polar'];nz=c['nz']
    nr=int(d['nseg'][track]-2);width=d['planar_widths'][track,:nr]*d['zmu'][p];regions=d['nom'][track,1:nr+1]-1;totals=d['group_totals'][group,regions]
    entry=d['entry_surface'][track] if o==1 else d['exit_surface'][track]
    g=geometry(width,c['H'],nz,sign*np.sqrt(1-1/d['zmu'][p]**2),o,q)
    f=read(root/'analysis'/c['id']/f'o{o}_m{sign}_q{q}.npz');m=f['metrics'][track-c['first'],group,col];piece=int(m[3])
    i=int(g['cell'][piece]//nz);src=float(regions[i]==col) if col<14 else ((regions[i]+1)/8 if col==14 else totals[i])
    np.testing.assert_array_equal(m[9:12],[g['length'][piece],totals[i],src])
    flight=direct_flight(width,totals,regions,int(entry),o);old=literal(g,totals,regions,flight,1.,float(d['harm'][p,2,d['angle'][track]]),o)
    u=int(old['units']);alpha=np.r_[np.arange(1,9)/8,np.arange(1,7)/6]
    actual={}
    for key in ['integral','face_in','face_out']:
        if col<14:v=old[key][...,u+2+col]
        elif col==14:v=old[key][...,u+2:u+16]@alpha
        else:v=old[key][...,u]
        actual[key]=v
    whole=actual['integral'].sum();end=nr-1 if o==1 else 0
    outgoing=actual['face_out'].reshape(nr,nz,4)[end,:,1 if o==1 else 0].sum()
    error=max(float(ratio(m[32]-whole,max(whole,m[32]))),float(ratio(m[33]-outgoing,max(outgoing,m[33]))))
    assert error<5e-12,error
    np.savez_compressed(target,**{'geometry_'+k:v for k,v in g.items()},**actual,streaming_metrics=m)
    return error


def main(root,H,nz):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text());d=read(root/'inputs/inventory.npz')
    cases=[c for c in plan['processes'] if c['H']==H and c['nz']==nz];target=root/'verification'/f'h{int(H)}_n{nz}';target.mkdir()
    worst={};witness=linear=0.;configurations=inputs=files=0;maxima={};coverage=np.zeros((2,2,2,4,11364),np.uint8)
    for case in cases:
        tracks=np.arange(case['first'],case['stop']);p=case['polar'];counts=d['nseg'][tracks]-2;regions=d['nom'][tracks,1:16]-1
        widths=d['planar_widths'][tracks]*d['zmu'][p];half=d['wei'][tracks]*d['wzmu'][p]/(2*H)
        geometry_counts=read(root/'inputs'/f"counts_{case['geometry_case']}.npz")['counts'];folder=root/'analysis'/case['id'];report=json.loads((folder/'result.json').read_text())
        assert report['all_gates_passed']
        for oi,o in enumerate([1,-1]):
            entry=d['entry_surface'][tracks] if o==1 else d['exit_surface'][tracks];exits=d['exit_surface'][tracks] if o==1 else d['entry_surface'][tracks]
            refs=independent_flight(widths,counts,regions,d['group_totals'],entry,o);refregional=track_regional_reference(refs,counts,regions,H,nz)
            for si,sign in enumerate([-1,1]):
                for qi,q in enumerate([8,16]):
                    label=f'o{o}_m{sign}_q{q}';f=read(folder/(label+'.npz'));m=f['metrics']
                    np.testing.assert_array_equal(f['original_tracks'],tracks);np.testing.assert_array_equal(f['multiplicity'],1)
                    np.testing.assert_array_equal(f['geometry'][:,:3],geometry_counts[si,oi,qi,tracks]);coverage[qi,si,oi,p,tracks]+=1
                    # The reusable raw audit now compares track totals with an
                    # independently reconstructed 1D regional reference, rather
                    # than pretending per-track regional fields were stored.
                    a,b,n=audit_fields(dict(metrics=m,regional=refregional),d['group_totals']);witness=max(witness,a);linear=max(linear,b);inputs+=n
                    row=checks(dict(geometry=f['geometry'],metrics=m,regional=refregional),q);assert row['passed']
                    reported=next(r for r in report['configurations'] if r['label']==label)
                    for key,val in row.items():assert reported[key]==val,(case['id'],label,key)
                    cell=m[...,13].astype(int);seg=cell//nz;cols=np.arange(16)[None,None,:]
                    assert np.all(cell>=0) and np.all(cell<counts[:,None,None]*nz)
                    zone=regions[np.arange(len(tracks))[:,None,None],seg]
                    sigma=d['group_totals'][np.arange(3)[None,:,None],zone]
                    source=np.where(cols<14,cols==zone,np.where(cols==14,(zone+1)/8,sigma))
                    birth=widths[np.arange(len(tracks))[:,None,None],seg]*(H/nz)*source
                    np.testing.assert_array_equal(m[...,14],birth)
                    assert np.all(m[...,3]>=0) and np.all(m[...,3]<f['geometry'][:,None,None,2])
                    boundary=np.zeros((3,6,14))
                    for group in range(3):np.add.at(boundary[group],exits,m[:,group,:14,33]*half[:,None])
                    np.testing.assert_array_equal(boundary,f['boundary'])
                    mx=d['harm'][p,2,d['angle'][tracks]]
                    for key,factor in [('volume',np.ones(len(tracks))),('jx',o*mx),('abs_jx',abs(mx))]:
                        reference=(refregional*(half*factor)[:,None,None,None,None]).sum(axis=0)
                        scale=(refregional*(half*abs(factor))[:,None,None,None,None]).sum(axis=0).max(axis=(1,2),keepdims=True)
                        referr=float(ratio(f['reference_'+key]-reference,scale).max());assert referr<5e-12
                        err=float(ratio(f[key]-reference,scale).max());maxima['independent_batch_'+key]=max(maxima.get('independent_batch_'+key,0.),err)
                        if q==16:assert err<5e-12
                    values=dict(primitive=m[...,2],cell=m[...,12],global_balance=ratio(m[...,24],m[...,25]),
                        point=ratio(m[...,26],m[...,27]),integral=ratio(m[...,28],m[...,29]),outface=ratio(m[...,30],m[...,31]),assembly=m[...,46])
                    for key,v in values.items():
                        loc=np.unravel_index(v.argmax(),v.shape);value=float(v[loc]);maxima[key]=max(maxima.get(key,0.),value)
                        if key not in worst or value>worst[key]['relative']:
                            tr,gi,col=loc;worst[key]=dict(relative=value,case=case,track=int(tracks[tr]),group_index=int(gi),group=[51,61,98][gi],input=int(col),orientation=o,sign=sign,order=q)
                    configurations+=len(tracks)*3;files+=1
    np.testing.assert_array_equal(coverage,1);literal_max=0.
    for key,where in worst.items():literal_max=max(literal_max,literal_witness(root,d,where,target/(key+'_literal.npz')))
    save(target/'worst.json',worst)
    result=dict(height=H,nz=nz,raw_files=files,track_group_configurations=configurations,input_evaluations=inputs,
        independent_worst_primitive_relative=witness,whole_track_source_assembly_relative=linear,
        worst_literal_track_relative=literal_max,maxima=maxima,all_original_records_once=True,all_checks_passed=True,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(target/'result.json',result);assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('height',type=float);p.add_argument('nz',type=int);a=p.parse_args();main(a.artifact.resolve(),a.height,a.nz)

"""Reconstruct physical balances from saved responses and independent inputs."""
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from calibrate_native_oblique_streaming import read,save
from native_layered_transport import basis,checks,aggregate
from native_layered_reference import RectangleReference,packed
from native_oblique_streaming import ratio
from native_layered_storage import pack


def main(root,case_id):
    tick=time.perf_counter();plan=json.loads((root/'calibration_plan.json').read_text())
    case=next(c for c in plan['cases'] if c['id']==case_id);p,H,nz=case['polar'],case['H'],case['nz']
    d=read(root/'inputs/inventory.npz');folder=root/'verification'/case_id;folder.mkdir()
    maxima=dict(global_balance=0.,saved_global_values=0.,primitive_quadrature=0.,positive_control_assembly=0.)
    files=0;states=0;compact_bytes=0;dense_bytes=0;gn,gw=leggauss(64)
    for mode in ['ranked','batch']:
        source=root/'primary'/mode/case_id;summary=json.loads((source/'result.json').read_text())
        expected=case['ranked_tracks'] if mode=='ranked' else list(range(case['batch_first'],case['batch_stop']))
        assert summary['original_tracks']==expected and summary['raw_checks_passed']
        if mode=='ranked':assert summary['independent_accuracy_passed']
        for gi,group in enumerate([51,61,98]):
            sigma=d['group_totals'][gi];q,rad,ax=basis(nz,sigma);n=14*nz+8
            alpha=(np.arange(n)+1)/(n+1);constant=np.r_[np.repeat(sigma,nz),np.ones(6*nz+8)]
            for o in [1,-1]:
                for sign in [-1,1]:
                    data=read(source/f'g{group}_o{o}_m{sign}.npz');files+=1
                    np.testing.assert_array_equal(data['original_tracks'],expected)
                    mu=sign*np.sqrt(1-1/d['zmu'][p]**2)
                    for track in expected:
                        nr=int(d['nseg'][track]-2);w=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
                        entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track])
                        exit_surface=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
                        np.testing.assert_array_equal(data[f't{track}_widths'],w);np.testing.assert_array_equal(data[f't{track}_regions'],reg)
                        born=(np.repeat(w,nz)[:,None]*(H/nz)*q[np.repeat(reg,nz)*nz+np.tile(np.arange(nz),nr)]).sum(axis=0)
                        incoming=(H/nz)*rad[entry*nz:(entry+1)*nz].sum(axis=0)+(abs(mu)*w[:,None]*ax[reg]).sum(axis=0)
                        assert np.max(incoming[:8*nz])==0
                        for order in [8,16,32]:
                            prefix=f't{track}_q{order}';a=data[prefix+'_response'];m=data[prefix+'_metrics'];states+=1
                            assert a.shape==(14*nz+16,14*nz+10) and m.shape==(14*nz+10,27)
                            compact=pack(a,m,reg,nz,entry,exit_surface,sign)
                            compact_bytes+=sum(v.nbytes for v in compact.values());dense_bytes+=a.nbytes+m.nbytes
                            assert np.isfinite(a).all() and a.min()>=0 and np.max(m[:,26])==0
                            collision=(np.repeat(sigma,nz)[:,None]*a[:8*nz]).sum(axis=0);out=a[8*nz:].sum(axis=0)
                            maxima['global_balance']=max(maxima['global_balance'],float(ratio(born+incoming-collision-out,born+incoming).max()))
                            values=np.stack([born,incoming,out,collision],axis=1)
                            maxima['saved_global_values']=max(maxima['saved_global_values'],float(ratio(values-m[:,20:24],(born+incoming)[:,None]).max()))
                            assembled=a[:,:n]@np.stack([alpha,constant],axis=1)
                            maxima['positive_control_assembly']=max(maxima['positive_control_assembly'],float(ratio(assembled-a[:,n:],abs(a[:,n:]).max(axis=0)).max()))
                            l=m[:,9];sig=m[:,10];src=m[:,11];t=l[:,None]*(gn+1)/2;weight=l[:,None]*gw/2;ex=np.exp(-sig[:,None]*t)
                            B=(ex*weight).sum(axis=1);D=(ex*(l[:,None]-t)*weight).sum(axis=1)
                            vals=np.stack([np.exp(-sig*l)*m[:,4]+B*src,B*m[:,4]+D*src],axis=1)
                            maxima['primitive_quadrature']=max(maxima['primitive_quadrature'],float(ratio(vals-m[:,5:7],np.maximum(vals,m[:,5:7])).max()))
                            if mode=='ranked':
                                f=dict(fields=data[prefix+'_fields'],metrics=m,geometry=data[prefix+'_geometry'],q=q,radial_input=rad,axial_input=ax)
                                assert checks(f,w,reg,sigma,H,nz,mu)['passed']
                                np.testing.assert_array_equal(packed(aggregate(f['fields'],reg,nz,o,exit_surface)),a)
                                reference=data[f't{track}_reference96']
                                if order==32:
                                    ref=RectangleReference(w,reg,sigma,entry,exit_surface,H,nz,mu,o,q,rad,ax)
                                    assert float(ratio(a-reference,ref.scale(reference)).max())<5e-12
    # Independently adaptive whole-line integration of the worst ranked GL32
    # state in this predeclared family, selected by its recorded response error.
    rows=json.loads((root/'primary/ranked'/case_id/'result.json').read_text())['rows']
    worst=max((r for r in rows if r['order']==32),key=lambda r:r['independent_response_relative'])
    track,group,o,sign=[worst[k] for k in ['track','group','orientation','sign']]
    sigma=d['group_totals'][[51,61,98].index(group)];nr=int(d['nseg'][track]-2)
    w=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
    entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track]);exit_surface=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
    mu=sign*np.sqrt(1-1/d['zmu'][p]**2);q,rad,ax=basis(nz,sigma)
    ref=RectangleReference(w,reg,sigma,entry,exit_surface,H,nz,mu,o,q,rad,ax)
    data=read(root/'primary/ranked'/case_id/f'g{group}_o{o}_m{sign}.npz');high=data[f't{track}_reference96']
    adaptive,report=ref.adaptive(high);agreement=float(ratio(adaptive-high,ref.scale(adaptive)).max())
    np.savez_compressed(folder/'adaptive_reference.npz',adaptive=adaptive,reference96=high,worker32=data[f't{track}_q32_response'])
    assert report['estimated_normalized_error']<2e-13 and agreement<2e-13,(report,agreement)
    assert maxima['global_balance']<1e-10
    assert max(v for k,v in maxima.items() if k!='global_balance')<5e-12,maxima
    save(folder/'result.json',dict(case=case_id,raw_files=files,transport_states=states,maxima=maxima,
        adaptive_selected_state=worst,adaptive_report=report,adaptive_agreement=agreement,all_checks_passed=True,
        lossless_storage_roundtrips=states,compact_array_bytes=compact_bytes,dense_array_bytes=dense_bytes))
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/'runs'/f'audit_{case_id}_resources.json',usage)
    assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512
    print(case_id,usage,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('case')
    a=p.parse_args();main(a.root.resolve(),a.case)

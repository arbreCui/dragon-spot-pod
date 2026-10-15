"""Frozen physical-input calibration on declared original-record samples."""
import argparse
import json
from pathlib import Path
import resource
import time
import numpy as np
from native_layered_transport import transport,aggregate,checks
from native_layered_reference import RectangleReference,packed
from native_oblique_streaming import ratio
from calibrate_native_oblique_streaming import read,save


def main(root,case_id,mode,pass_name):
    tick=time.perf_counter();plan=json.loads((root/'calibration_plan.json').read_text())
    c=next(c for c in plan['cases'] if c['id']==case_id)
    p,H,nz=c['polar'],c['H'],c['nz'];d=read(root/'inputs/inventory.npz')
    tracks=c['ranked_tracks'] if mode=='ranked' else list(range(c['batch_first'],c['batch_stop']))
    folder=root/pass_name/mode/case_id;folder.mkdir(parents=True)
    counts=read(root/f'inputs/counts_{case_id}.npz')['counts'];rows=[];timings=[]
    for gi,group in enumerate([51,61,98]):
        sig=d['group_totals'][gi]
        for oi,o in enumerate([1,-1]):
            for si,sign in enumerate([-1,1]):
                label=f'g{group}_o{o}_m{sign}';outputs={};mu=sign*np.sqrt(1-1/d['zmu'][p]**2)
                for track in tracks:
                    nr=int(d['nseg'][track]-2);w=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
                    entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track])
                    exit_surface=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
                    results={};reference=None
                    for order in plan['worker_orders']:
                        start=time.perf_counter()
                        f=transport(root/'build/layered.dylib',w,reg,sig,entry,H,nz,mu,o,order)
                        seconds=time.perf_counter()-start
                        a=packed(aggregate(f['fields'],reg,nz,o,exit_surface));results[order]=(f,a)
                        expected=counts[si,oi,1,track].copy();expected[1:]*=order//16 if order>=16 else 1
                        if order==8:expected=counts[si,oi,0,track]
                        np.testing.assert_array_equal(f['geometry'][:3],expected)
                        row=checks(f,w,reg,sig,H,nz,mu);row.update(track=int(track),group=group,orientation=o,sign=sign,order=order)
                        rows.append(row);timings.append(dict(order=order,seconds=seconds,updates=int(f['geometry'][2])*(14*nz+10)))
                        if not row['passed']:
                            save(folder/'failure.json',row);raise RuntimeError('raw physical-input checks failed')
                        prefix=f't{track}_q{order}'
                        outputs[prefix+'_geometry']=f['geometry'];outputs[prefix+'_metrics']=f['metrics'];outputs[prefix+'_response']=a
                        if mode=='ranked':outputs[prefix+'_fields']=f['fields']
                    if mode=='ranked':
                        f=results[32][0];ref=RectangleReference(w,reg,sig,entry,exit_surface,H,nz,mu,o,f['q'],f['radial_input'],f['axial_input'])
                        low=ref.fixed(64);high=ref.fixed(96);scale=ref.scale(high)
                        reference_accuracy=float(ratio(low-high,scale).max())
                        outputs[f't{track}_reference64']=low;outputs[f't{track}_reference96']=high
                        for row in rows[-3:]:
                            row['reference_accuracy']=reference_accuracy
                            row['independent_response_relative']=float(ratio(results[row['order']][1]-high,scale).max())
                            row['independent_accuracy_passed']=bool(reference_accuracy<2e-13 and row['independent_response_relative']<5e-12)
                    outputs[f't{track}_widths']=w;outputs[f't{track}_regions']=reg
                np.savez_compressed(folder/(label+'.npz'),original_tracks=np.asarray(tracks),**outputs)
    summary=dict(case=c,mode=mode,original_tracks=tracks,rows=rows,
        raw_checks_passed=all(r['passed'] for r in rows),full_native_geometry_qualified=False,
        independent_accuracy_passed=(all(r['independent_accuracy_passed'] for r in rows if r['order']==32) if mode=='ranked' else None))
    save(folder/'result.json',summary)
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2,timing=timings)
    save(root/'runs'/f'{pass_name}_{mode}_{case_id}_resources.json',usage)
    if summary['independent_accuracy_passed'] is False:raise RuntimeError('order-32 independent accuracy gate failed')
    assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512
    print(case_id,mode,'seconds',round(usage['elapsed_seconds'],2),'RSS',round(usage['peak_rss_mib'],2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('case')
    p.add_argument('mode',choices=['ranked','batch']);p.add_argument('pass_name',choices=['primary','replay'])
    a=p.parse_args();main(a.root.resolve(),a.case,a.mode,a.pass_name)

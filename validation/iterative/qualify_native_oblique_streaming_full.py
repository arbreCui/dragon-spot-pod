"""Complete original-index response batches; same qualified streaming kernel."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from native_oblique_streaming import independent_flight,transport,checks,ratio
from calibrate_native_oblique_streaming import read,save,compare_reference


def reference_calibration(root,p):
    tick=time.perf_counter();d=read(root/'inputs/inventory.npz');nt=len(d['nseg']);errors=np.zeros((nt,2,3,2))
    for first in range(0,nt,512):
        tracks=np.arange(first,min(first+512,nt));n=d['nseg'][tracks]-2;w=d['planar_widths'][tracks]*d['zmu'][p];r=d['nom'][tracks,1:16]-1
        for oi,o in enumerate([1,-1]):
            entry=d['entry_surface'][tracks] if o==1 else d['exit_surface'][tracks]
            refs=independent_flight(w,n,r,d['group_totals'],entry,o)
            assert all(np.isfinite(v).all() and v.min()>=0 for v in refs.values())
            errors[tracks,oi]=compare_reference(root,refs,tracks,p,o)
    np.savez_compressed(root/f'reference/p{p}.npz',original_tracks=np.arange(nt),multiplicity=np.ones(nt,np.uint8),errors=errors)
    result=dict(polar=p,original_tracks=nt,orientations=2,groups=3,independent_reference_relative=float(errors.max()),passed=bool(errors.max()<5e-12))
    save(root/f'reference/p{p}.json',result)
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/f'runs/reference_p{p}_resources.json',usage)
    assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512


def batch(root,pid):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text());case=next(c for c in plan['processes'] if c['id']==pid)
    # Entire original reference calibration must have completed before any
    # full oblique batch, not merely before this batch's own records.
    for pole in range(4):assert json.loads((root/f'reference/p{pole}.json').read_text())['passed']
    p,H,nz=case['polar'],case['H'],case['nz'];tracks=np.arange(case['first'],case['stop'])
    d=read(root/'inputs/inventory.npz');n=d['nseg'][tracks]-2;w=d['planar_widths'][tracks]*d['zmu'][p];r=d['nom'][tracks,1:16]-1
    counts=read(root/'inputs'/f"counts_{case['geometry_case']}.npz")['counts']
    folder=root/'analysis'/pid;folder.mkdir();rows=[]
    half=d['wei'][tracks]*d['wzmu'][p]/2/H;mx=d['harm'][p,2,d['angle'][tracks]]
    for oi,o in enumerate([1,-1]):
        entry=d['entry_surface'][tracks] if o==1 else d['exit_surface'][tracks]
        exits=d['exit_surface'][tracks] if o==1 else d['entry_surface'][tracks]
        refs=independent_flight(w,n,r,d['group_totals'],entry,o)
        reference_errors=compare_reference(root,refs,tracks,p,o)
        expected={key:np.zeros((3,8,nz,14)) for key in ['volume','jx','abs_jx']};expected['boundary']=np.zeros((3,6,14))
        for gi in range(3):
            for seg in range(15):
                ix=np.flatnonzero(seg<n)
                if not len(ix):continue
                values=refs['integral'][gi,ix,seg]*half[ix,None]*(H/nz)
                for z in range(nz):
                    for key,factor in [('volume',np.ones(len(ix))),('jx',o*mx[ix]),('abs_jx',abs(mx[ix]))]:
                        np.add.at(expected[key][gi,:,z],r[ix,seg],values*factor[:,None])
            end=n-1 if o==1 else np.zeros(len(n),int)
            np.add.at(expected['boundary'][gi],exits,refs['outgoing'][gi,np.arange(len(n)),end]*H*half[:,None])
        for si,sign in enumerate([-1,1]):
            for qi,order in enumerate([8,16]):
                label=f'o{o}_m{sign}_q{order}'
                result=transport(root/'build/streaming.dylib',w,n,r,d['group_totals'],refs,H,nz,sign*np.sqrt(1-1/d['zmu'][p]**2),o,order)
                np.testing.assert_array_equal(result['geometry'][:,:3],counts[si,oi,qi,tracks])
                row=checks(result,order);row.update(label=label,original_records=len(tracks))
                region=result.pop('regional');ww=half[:,None,None,None,None]
                # Within each frozen batch, NumPy's reduction order is fixed.
                # Aggregate batches in increasing original-index order later.
                volume=(region*ww).sum(axis=0)
                jx=(region*(ww*(o*mx)[:,None,None,None,None])).sum(axis=0)
                abs_jx=(region*(ww*abs(mx)[:,None,None,None,None])).sum(axis=0)
                boundary=np.zeros((3,6,14));out=result['metrics'][:,:,:14,33]
                for gi in range(3):np.add.at(boundary[gi],exits,out[:,gi]*half[:,None])
                actual=dict(volume=volume,jx=jx,abs_jx=abs_jx,boundary=boundary)
                for key in actual:
                    scale=expected['abs_jx'] if key=='jx' else abs(expected[key])
                    axes=tuple(range(1,scale.ndim-1));sc=scale.max(axis=axes,keepdims=True)
                    row['independent_batch_'+key+'_relative']=float(ratio(actual[key]-expected[key],sc).max())
                if order==16:row['passed'] &= max(row['independent_batch_'+key+'_relative'] for key in actual)<5e-12
                np.savez_compressed(folder/(label+'.npz'),original_tracks=tracks,multiplicity=np.ones(len(tracks),np.uint8),
                    reference_calibration=reference_errors,**result,**actual,**{'reference_'+key:value for key,value in expected.items()})
                rows.append(row)
                if not row['passed']:
                    save(folder/'failed.json',row);raise RuntimeError('full original-index response batch failed frozen gates')
    save(folder/'result.json',dict(case=case,configurations=rows,all_gates_passed=all(r['passed'] for r in rows),
        original_index_count=len(tracks),full_operator_qualified=False))
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/'runs'/(pid+'_resources.json'),usage)
    if usage['elapsed_seconds']>600 or usage['peak_rss_mib']>512:raise RuntimeError('full batch resource cap exceeded')
    print(pid,'seconds',round(usage['elapsed_seconds'],2),'RSS',round(usage['peak_rss_mib'],2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('case');a=p.parse_args();root=a.artifact.resolve()
    if a.case.startswith('reference_p'):reference_calibration(root,int(a.case.removeprefix('reference_p')))
    else:batch(root,a.case)

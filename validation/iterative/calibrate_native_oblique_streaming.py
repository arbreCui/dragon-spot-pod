"""Frozen full-coordinate worker calibration, not full native qualification."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from native_oblique_streaming import independent_flight,transport,checks,ratio


def save(path,data):
    with Path(path).open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def read(path):
    with np.load(path) as f:return {k:f[k] for k in f.files}


def compare_reference(root,refs,tracks,p,orientation):
    errors=[];oi=0 if orientation==1 else 1;lines=np.asarray(tracks)*4+p
    for gi,group in enumerate([51,61,98]):
        with np.load(root/f'inputs/green_{group}.npz') as f:
            target=f['track_integral'][oi,lines]
            actual=refs['integral'][gi].sum(axis=1);scale=abs(target).max(axis=1)
            ei=ratio(abs(actual-target).max(axis=1),scale)
            target=f['track_outgoing'][oi,lines]
        counts=read(root/'inputs/inventory.npz')['nseg'][tracks]-2
        end=counts-1 if orientation==1 else np.zeros(len(tracks),int)
        actual=refs['outgoing'][gi,np.arange(len(tracks)),end]
        eo=ratio(abs(actual-target).max(axis=1),abs(target).max(axis=1))
        errors.append(np.c_[ei,eo])
    result=np.stack(errors,axis=1)
    if np.max(result)>=5e-12:raise RuntimeError('independent full-flight calibration failed')
    return result


def main(root,pid):
    tick=time.perf_counter();plan=json.loads((root/'calibration_plan.json').read_text())
    case=next(c for c in plan['cases'] if c['id']==pid);p,H,nz=case['polar'],case['H'],case['nz']
    d=read(root/'inputs/inventory.npz');folder=root/'calibration'/pid;folder.mkdir()
    receipts=read(root/'inputs'/f'counts_{pid}.npz');rows=[];timing=[];refmax=0.
    for block,tracks in [('ranked',case['ranked_tracks']),('largest_batch',list(range(case['batch_first'],case['batch_stop'])))]:
        tracks=np.asarray(tracks);n=d['nseg'][tracks]-2;w=d['planar_widths'][tracks]*d['zmu'][p];r=d['nom'][tracks,1:16]-1;t=d['group_totals']
        for oi,o in enumerate([1,-1]):
            start=time.perf_counter();entrance=d['entry_surface'][tracks] if o==1 else d['exit_surface'][tracks]
            ref=independent_flight(w,n,r,t,entrance,o);referrors=compare_reference(root,ref,tracks,p,o)
            refmax=max(refmax,float(referrors.max()));reference_seconds=time.perf_counter()-start
            for si,sign in enumerate([-1,1]):
                for qi,order in enumerate([8,16]):
                    label=f'{block}_o{o}_m{sign}_q{order}';start=time.perf_counter()
                    result=transport(root/'build/streaming.dylib',w,n,r,t,ref,H,nz,sign*np.sqrt(1-1/d['zmu'][p]**2),o,order)
                    kernel_seconds=time.perf_counter()-start
                    np.testing.assert_array_equal(result['geometry'][:,:3],receipts['counts'][si,oi,qi,tracks])
                    row=checks(result,order);row.update(label=label,original_tracks=len(tracks),primitive_column_updates=int(result['geometry'][:,2].sum())*3*16)
                    start=time.perf_counter()
                    np.savez_compressed(folder/(label+'.npz'),original_tracks=tracks,reference_calibration=referrors,**result)
                    timing.append(dict(label=label,kernel_seconds=kernel_seconds,write_seconds=time.perf_counter()-start,
                        reference_seconds_per_orientation=reference_seconds,primitive_column_updates=row['primitive_column_updates']))
                    rows.append(row)
                    if not row['passed']:
                        save(folder/'failed.json',row);raise RuntimeError('frozen streaming checks failed; preserve outputs')
    summary=dict(case=case,configurations=rows,reference_calibration_relative=refmax,
        implementation_calibration_passed=all(r['passed'] for r in rows),whole_native_operator_qualified=False)
    save(folder/'result.json',summary)
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2,timing=timing)
    save(root/'runs'/(pid+'_resources.json'),usage)
    if usage['elapsed_seconds']>600 or usage['peak_rss_mib']>512:raise RuntimeError('calibration resource cap exceeded')
    print(pid,'seconds',round(usage['elapsed_seconds'],2),'RSS',round(usage['peak_rss_mib'],2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('case');a=p.parse_args();main(a.artifact.resolve(),a.case)

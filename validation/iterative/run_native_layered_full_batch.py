"""Complete physical response and sealed-kernel regression for original indices."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import numpy as np
from native_layered_cached import transport,basis,checks,aggregate
from native_layered_reference import packed
from native_oblique_streaming import independent_flight,transport as previous_transport,ratio
from native_layered_batch_storage import Collector,scientific
from calibrate_native_oblique_streaming import read,save

CHECK_KEYS=['primitive_relative','cell_relative','global_relative','minimum_angle','minimum_integral',
 'shared_face_absolute','geometry_relative','represented_width_relative','source_assembly_relative',
 'constant_relative','vacuum_axial_incoming_absolute']


def scales(x,nz):
    s=np.empty_like(x)
    for lo,hi in [(0,8*nz),(8*nz,14*nz),(14*nz,14*nz+16)]:s[lo:hi]=abs(x[lo:hi]).max(axis=0)
    return s


def main(root,case_id,phase):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text());case=next(c for c in plan['batches'] if c['id']==case_id)
    if not case.get('preflight',False):
        admission=json.loads((root/'admission.json').read_text())
        assert admission['full_execution_admitted'] and admission['plan_sha256']==hashlib.sha256((root/'plan.json').read_bytes()).hexdigest()
    p,H,nz=case['polar'],case['height'],case['nz'];tracks=np.arange(case['first'],case['stop']);nt=len(tracks)
    d=read(root/'inputs/inventory.npz');counts=read(root/f'inputs/counts_p{p}_h{int(H)}_n{nz}.npz')['counts']
    n=d['nseg'][tracks]-2;w=d['planar_widths'][tracks]*d['zmu'][p];reg=d['nom'][tracks,1:16]-1
    # Full analytic one-dimensional references, calibrated against every sealed
    # original track/group coordinate before they are used as matched inflow.
    refs=[];ref_errors=np.zeros((nt,2,3,2));old_green=[]
    for group in [51,61,98]:
        with np.load(root/f'inputs/green_{group}.npz') as z:
            old_green.append((z['track_integral'][:,tracks*4+p].copy(),z['track_outgoing'][:,tracks*4+p].copy()))
    for oi,o in enumerate([1,-1]):
        entry=d['entry_surface'][tracks] if o==1 else d['exit_surface'][tracks]
        ref=independent_flight(w,n,reg,d['group_totals'],entry,o);refs.append(ref)
        end=n-1 if o==1 else np.zeros(nt,int)
        for gi,(integ,out) in enumerate(old_green):
            a=ref['integral'][gi].sum(axis=1);b=ref['outgoing'][gi,np.arange(nt),end]
            ref_errors[:,oi,gi,0]=ratio(abs(a-integ[oi]).max(axis=1),abs(integ[oi]).max(axis=1))
            ref_errors[:,oi,gi,1]=ratio(abs(b-out[oi]).max(axis=1),abs(out[oi]).max(axis=1))
    assert ref_errors.max()<5e-12
    del old_green
    k=14*nz+10;nout=14*nz+16
    collectors={(gi,oi,si):Collector() for gi in range(3) for oi in range(2) for si in range(2)}
    check_values=np.zeros((nt,3,2,2,2,len(CHECK_KEYS)))
    convergence=np.zeros((nt,3,2,2,3));regression_hashes=np.zeros((nt,3,2,2,2),dtype='S32')
    old_recovery=np.zeros((nt,3,2,2,2,2))
    operators=np.zeros((2,3,2,2,nout,k));jx=np.zeros((2,3,2,2,8*nz,k));abs_jx=np.zeros_like(jx)
    counts_actual=np.zeros((nt,2,2,2,3),np.int64)
    qreg=np.repeat(np.eye(14)[:8],nz,axis=0);rreg=np.repeat(np.eye(14)[8:],nz,axis=0);areg=np.zeros((8,14))
    defaults=[basis(nz,s) for s in d['group_totals']]
    physical_seconds=regression_seconds=0.;updates=0
    for ti,track in enumerate(tracks):
        nr=int(n[ti]);width=w[ti,:nr];regions=reg[ti,:nr]
        weight=d['wei'][track]*d['wzmu'][p]/2;mx=d['harm'][p,2,d['angle'][track]]
        for oi,o in enumerate([1,-1]):
            entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track]);ex=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
            for si,sign in enumerate([-1,1]):
                mu=sign*np.sqrt(1-1/d['zmu'][p]**2);low=[]
                for qi,order in enumerate([16,32]):
                    for gi,sigma in enumerate(d['group_totals']):
                        start=time.perf_counter();f=transport(root/'build/cached.dylib',width,regions,sigma,entry,H,nz,mu,o,order,*defaults[gi]);physical_seconds+=time.perf_counter()-start
                        expected=counts[si,oi,1,track].copy();expected[1:]*=order//16
                        np.testing.assert_array_equal(f['geometry'][:3],expected)
                        counts_actual[ti,oi,si,qi]=f['geometry'][:3]
                        row=checks(f,width,regions,sigma,H,nz,mu)
                        if not row['passed']:
                            save(root/'runs'/f'{phase}_{case_id}_failed.json',dict(track=int(track),group=gi,orientation=o,sign=sign,order=order,checks=row));raise RuntimeError('physical gate')
                        check_values[ti,gi,oi,si,qi]=[row[key] for key in CHECK_KEYS]
                        a=packed(aggregate(f['fields'],regions,nz,o,ex));updates+=int(f['geometry'][2])*k
                        operators[qi,gi,si,oi]+=weight*a;jx[qi,gi,si,oi]+=weight*o*mx*a[:8*nz];abs_jx[qi,gi,si,oi]+=weight*abs(mx)*a[:8*nz]
                        if order==16:low.append(a)
                        else:
                            error=ratio(a-low[gi],scales(a,nz))
                            convergence[ti,gi,oi,si]=[error[:8*nz].max(),error[8*nz:14*nz].max(),error[14*nz:].max()]
                            collectors[gi,oi,si].add(int(track),f,a,regions,nz,entry,ex,sign)
                # Compare the entire local cell/face matrix against the sealed
                # implementation, not merely scalar averages or a source sum.
                reference={name:value[:,ti:ti+1] for name,value in refs[oi].items()}
                for qi,order in enumerate([8,16]):
                    start=time.perf_counter()
                    previous=previous_transport(root/'build/zero_gradient.dylib',w[ti:ti+1],n[ti:ti+1],reg[ti:ti+1],d['group_totals'],reference,H,nz,mu,o,order,True)
                    for gi,sigma in enumerate(d['group_totals']):
                        f=transport(root/'build/cached.dylib',width,regions,sigma,entry,H,nz,mu,o,order,qreg,rreg,areg,reference['incoming'][gi,0,:nr])
                        target=previous['fields'][0,gi,:nr*nz,:,:14].copy()
                        assert f['fields'].tobytes()==target.tobytes(),('matched regression',int(track),gi,o,sign,order)
                        regression_hashes[ti,gi,oi,si,qi]=hashlib.sha256(target.tobytes()).digest()
                        a=packed(aggregate(f['fields'],regions,nz,o,ex))
                        iv=reference['integral'][gi,0].sum(axis=0)*H;ov=reference['outgoing'][gi,0,nr-1 if o==1 else 0]*H
                        old_recovery[ti,gi,oi,si,qi]=[ratio(a[:8*nz].sum(axis=0)-iv,abs(iv).max()).max(),ratio(a[8*nz:14*nz].sum(axis=0)-ov,abs(ov).max()).max()]
                    regression_seconds+=time.perf_counter()-start
    receipt={}
    for (gi,oi,si),collector in collectors.items():
        scientific(root,phase,case_id,f'raw_g{[51,61,98][gi]}_o{[1,-1][oi]}_m{[-1,1][si]}.npz',collector.arrays(),receipt)
    scientific(root,phase,case_id,'operators.npz',dict(original_tracks=tracks,operators=operators,jx=jx,abs_jx=abs_jx),receipt)
    scientific(root,phase,case_id,'controls.npz',dict(original_tracks=tracks,checks=check_values,convergence=convergence,
        regression_hashes=regression_hashes,old_recovery=old_recovery,reference_errors=ref_errors,geometry_counts=counts_actual),receipt)
    summary=dict(case=case,original_records=nt,physical_states=nt*3*4*2,physical_coordinate_evaluations=nt*3*4*2*k,
        physical_piece_column_updates=updates,matched_regression_states=nt*3*4*2,matched_regression_input_evaluations=nt*3*4*2*14,
        full_cell_face_regression_byte_exact=True,physical_gate_maxima={key:float(check_values[...,i].max()) for i,key in enumerate(CHECK_KEYS) if not key.startswith('minimum')},
        minimum_angle=float(check_values[...,3].min()),minimum_integral=float(check_values[...,4].min()),
        full_coordinate_order16_order32_relative=float(convergence.max()),independent_wholeflight_relative=float(ref_errors.max()),
        matched_order16_recovery_relative=float(old_recovery[...,1,:].max()),all_checks_passed=bool(convergence.max()<5e-12 and old_recovery[...,1,:].max()<5e-12))
    scientific(root,phase,case_id,'result.json',summary,receipt)
    folder=root/'receipts'/phase;folder.mkdir(parents=True,exist_ok=True);save(folder/(case_id+'.json'),dict(files=receipt,all_scientific_bytes_identical=phase=='replay'))
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2,
        physical_kernel_seconds=physical_seconds,matched_regression_seconds=regression_seconds,output_bytes=sum(f['bytes'] for f in receipt.values()))
    save(root/'runs'/f'{phase}_{case_id}_resources.json',usage)
    assert summary['all_checks_passed'],summary
    assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512,usage
    print(case_id,phase,usage,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('case');p.add_argument('phase',choices=['primary','replay'])
    a=p.parse_args();main(a.root.resolve(),a.case,a.phase)

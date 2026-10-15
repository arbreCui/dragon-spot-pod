"""Current-data full-family audit, preserving the original physical checks.

The original prior-data zero-gradient regression assertion is omitted. No
current zero-gradient regression claim is made; physical source coordinates,
raw ledgers, independent assembly and whole-field references are retained.
"""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"validation/iterative"))
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_layered_batch_storage import records
from native_layered_transport import basis,transport,aggregate
from native_layered_reference import RectangleReference,packed
from native_oblique_streaming import ratio
from calibrate_native_oblique_streaming import read,save


def main(root,family,probe=False):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text())
    cases=[c for c in plan['batches'] if (c['preflight'] and c['id']==family if probe else not c['preflight'] and c['id'].rsplit('_b',1)[0]==family)]
    if probe:assert len(cases)==1
    else:assert len(cases)==45 and cases[0]['first']==0 and cases[-1]['stop']==11364
    expected_tracks=np.concatenate([np.arange(c['first'],c['stop']) for c in cases])
    assert len(np.unique(expected_tracks))==len(expected_tracks)
    p,H,nz=cases[0]['polar'],cases[0]['height'],cases[0]['nz'];d=read(root/'inputs/inventory.npz');k=14*nz+10;nout=14*nz+16
    result_dir=root/('preflight' if probe else 'verification')/(family+'_audit' if probe else family);result_dir.mkdir();coverage=np.zeros((3,2,2,11364),np.uint8)
    # Preserve order-16 and order-32 global operators separately.
    op=np.zeros((2,3,2,2,nout,k));jx=np.zeros((2,3,2,2,8*nz,k));abs_jx=np.zeros_like(jx)
    maximum={name:0. for name in ['global_balance','saved_global_values','primitive_witness','cell_witness_birth','primitive_witness_defect','cell_witness_defect','control_assembly','batch_operator','batch_jx','batch_abs_jx']}
    references=[];worst={(gi,oi,si):(-1.,None) for gi in range(3) for oi in range(2) for si in range(2)}
    gn,gw=leggauss(64);files=states=coords=0
    for case in cases:
        folder=root/'primary'/case['id'];summary=json.loads((folder/'result.json').read_text());assert summary['all_checks_passed'] and summary['current_totals_used']
        ctl=read(folder/'controls.npz');ops=read(folder/'operators.npz');tracks=np.arange(case['first'],case['stop'])
        np.testing.assert_array_equal(ctl['original_tracks'],tracks);np.testing.assert_array_equal(ops['original_tracks'],tracks)
        for gi,sigma in enumerate(d['group_totals']):
            q,rad,ax=basis(nz,sigma);alpha=(np.arange(14*nz+8)+1)/(14*nz+9)
            combinations=np.stack([alpha,np.r_[np.repeat(sigma,nz),np.ones(6*nz+8)]],axis=1)
            for oi,o in enumerate([1,-1]):
                for si,sign in enumerate([-1,1]):
                    raw=read(folder/f'raw_g{[51,61,98][gi]}_o{o}_m{sign}.npz');np.testing.assert_array_equal(raw['original_tracks'],tracks)
                    files+=1;values=[];mu=sign*np.sqrt(1-1/d['zmu'][p]**2)
                    for ti,(track,geo,a,m) in enumerate(records(raw)):
                        assert track==tracks[ti];coverage[gi,oi,si,track]+=1;states+=1;coords+=k
                        assert np.isfinite(a).all() and a.min()>=0 and np.max(m[:,26])==0 and np.isfinite(m).all()
                        nr=int(d['nseg'][track]-2);width=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
                        entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track])
                        source=q[np.repeat(reg,nz)*nz+np.tile(np.arange(nz),nr)]
                        born=(np.repeat(width,nz)[:,None]*(H/nz)*source).sum(axis=0)
                        incoming=(H/nz)*rad[entry*nz:(entry+1)*nz].sum(axis=0)+(abs(mu)*width[:,None]*ax[reg]).sum(axis=0)
                        assert incoming[:8*nz].max()==0
                        collision=(np.repeat(sigma,nz)[:,None]*a[:8*nz]).sum(axis=0);out=a[8*nz:].sum(axis=0)
                        maximum['global_balance']=max(maximum['global_balance'],float(ratio(born+incoming-collision-out,born+incoming).max()))
                        stored=np.stack([born,incoming,out,collision],axis=1)
                        maximum['saved_global_values']=max(maximum['saved_global_values'],float(ratio(stored-m[:,20:24],(born+incoming)[:,None]).max()))
                        cell=m[:,13].astype(int);assert np.array_equal(cell,m[:,13]) and ((cell>=0)&(cell<nr*nz)).all()
                        cb=width[cell//nz]*(H/nz)*q[reg[cell//nz]*nz+cell%nz,np.arange(k)]
                        maximum['cell_witness_birth']=max(maximum['cell_witness_birth'],float(ratio(cb-m[:,14],m[:,19]).max()))
                        cd=m[:,14]+m[:,15]-m[:,16]-m[:,17]
                        maximum['cell_witness_defect']=max(maximum['cell_witness_defect'],float(ratio(cd-m[:,18],m[:,19]).max()))
                        l=m[:,9];sig=m[:,10];src=m[:,11];t=l[:,None]*(gn+1)/2;ww=l[:,None]*gw/2;ex=np.exp(-sig[:,None]*t)
                        B=(ex*ww).sum(axis=1);D=(ex*(l[:,None]-t)*ww).sum(axis=1)
                        actual=np.stack([np.exp(-sig*l)*m[:,4]+B*src,B*m[:,4]+D*src],axis=1)
                        maximum['primitive_witness']=max(maximum['primitive_witness'],float(ratio(actual-m[:,5:7],np.maximum(actual,m[:,5:7])).max()))
                        pd=m[:,5]-m[:,4]+sig*m[:,6]-l*src
                        maximum['primitive_witness_defect']=max(maximum['primitive_witness_defect'],float(ratio(pd-m[:,7],m[:,8]).max()))
                        maximum['control_assembly']=max(maximum['control_assembly'],float(ratio(a[:,:-2]@combinations-a[:,-2:],abs(a[:,-2:]).max(axis=0)).max()))
                        values.append(a)
                        err=max(float(ctl['convergence'][ti,gi,oi,si].max()),float(ctl['full_field_convergence'][ti,gi,oi,si]))
                        if err>worst[gi,oi,si][0]:worst[gi,oi,si]=(err,(track,a.copy()))
                    # Different reduction path from the worker's record-wise
                    # accumulation. Includes every source/control coordinate.
                    values=np.stack(values);weight=d['wei'][tracks]*d['wzmu'][p]/2
                    independent=np.tensordot(weight,values,axes=1)
                    mx=d['harm'][p,2,d['angle'][tracks]]
                    ji=np.tensordot(weight*o*mx,values[:,:8*nz],axes=1)
                    aj=np.tensordot(weight*abs(mx),values[:,:8*nz],axes=1)
                    for name,actual,target,scale in [('batch_operator',independent,ops['operators'][1,gi,si,oi],abs(independent).max(axis=0)),
                        ('batch_jx',ji,ops['jx'][1,gi,si,oi],aj.max(axis=0)),('batch_abs_jx',aj,ops['abs_jx'][1,gi,si,oi],aj.max(axis=0))]:
                        maximum[name]=max(maximum[name],float(ratio(actual-target,scale).max()))
        op+=ops['operators'];jx+=ops['jx'];abs_jx+=ops['abs_jx']
    expected_coverage=np.zeros_like(coverage);expected_coverage[...,expected_tracks]=1
    np.testing.assert_array_equal(coverage,expected_coverage)
    for (gi,oi,si),(error,(track,saved)) in worst.items():
        o=[1,-1][oi];sign=[-1,1][si];sigma=d['group_totals'][gi];nr=int(d['nseg'][track]-2)
        width=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
        entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track]);exit_surface=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
        mu=sign*np.sqrt(1-1/d['zmu'][p]**2);q,rad,ax=basis(nz,sigma)
        ref=RectangleReference(width,reg,sigma,entry,exit_surface,H,nz,mu,o,q,rad,ax)
        high=ref.fixed(96);adaptive,ar=ref.adaptive(high)
        agreement=float(ratio(adaptive-high,ref.scale(adaptive)).max());worker_error=float(ratio(saved-adaptive,ref.scale(adaptive)).max())
        # Whole local cell/face traces are regenerated and independently clipped.
        f=transport(root/'runtime/cached.dylib',width,reg,sigma,entry,H,nz,mu,o,32)
        np.testing.assert_array_equal(packed(aggregate(f['fields'],reg,nz,o,exit_surface)),saved)
        literal=ref.fixed(96,full=True);field_error=float(ratio(f['fields']-literal,abs(literal).max(axis=(0,1))).max())
        label=f'g{[51,61,98][gi]}_o{o}_m{sign}'
        np.savez_compressed(result_dir/(label+'.npz'),saved=saved,independent96=high,adaptive=adaptive,fields=f['fields'],literal_fields=literal)
        references.append(dict(track=track,group=[51,61,98][gi],orientation=o,sign=sign,offset_disagreement=error,
            adaptive_report=ar,adaptive_agreement=agreement,independent_response_error=worker_error,independent_full_field_error=field_error))
        assert ar['estimated_normalized_error']<2e-13 and agreement<2e-13 and max(worker_error,field_error)<5e-12,references[-1]
    assert maximum['global_balance']<1e-10
    assert max(v for key,v in maximum.items() if key!='global_balance')<5e-12,maximum
    np.savez_compressed(result_dir/'operators.npz',operators=op,jx=jx,abs_jx=abs_jx,coverage=coverage)
    result=dict(family=family,scope='preflight subset' if probe else 'complete original inventory',original_tracks=len(expected_tracks),raw_files=files,physical_states=states,source_coordinates=coords,
        all_original_indices_once=not probe,all_declared_indices_once=True,independent_maxima=maximum,independent_traces=references,all_checks_passed=True,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(result_dir/'result.json',result);assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    print(family,'audited',states,'states',round(result['elapsed_seconds'],2),'seconds',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('family');p.add_argument('--probe',action='store_true');a=p.parse_args();main(a.root.resolve(),a.family,a.probe)

"""Physical axial vacuum plus layer-local white closure in a defined toy model."""
import argparse
from pathlib import Path
import numpy as np
from calibrate_native_oblique_streaming import save
from native_layered_white import bundle,close
from native_oblique_streaming import ratio


def main(root,pass_name):
    folder=root/pass_name/'white';folder.mkdir(parents=True);rows=[]
    for H in [1.,20.]:
        for nz in [1,2,4]:
            for total in [0.,.4,4.]:
                name=f'h{int(H)}_n{nz}_s{total}';b=bundle(root/'build/layered.dylib',H,nz,total,32)
                ref=bundle(root/'build/layered.dylib',H,nz,total,96,True)
                scale=np.empty_like(ref['operator'])
                for lo,hi in [(0,8*nz),(8*nz,14*nz),(14*nz,14*nz+16)]:
                    scale[lo:hi]=abs(ref['operator'][lo:hi]).max(axis=0)
                open_error=float(ratio(b['operator']-ref['operator'],scale).max())
                supply=np.r_[b['volume_measure'],b['radial_incoming_measure'],.8*np.dot([.1,.2,.3,.4],[.2,.5,.8,.95]),np.zeros(7)]
                g=b['operator'];defect=supply-total*g[:8*nz].sum(axis=0)-g[8*nz:].sum(axis=0)
                open_balance=float(ratio(defect,supply).max())
                assert open_error<5e-12 and open_balance<1e-10 and g.min()>=0
                # Closure is admitted only after the complete common-source
                # open operator of this manufactured model passes.
                r,check=close(b);rr,rc=close(ref)
                errors={k:float(ratio(r[k]-rr[k],abs(rr[k]).max(axis=0)).max()) for k in ['fields','inflow','axial_escape']}
                # Jz vanishes in symmetric cases; normalize by the positive
                # scalar volume response, never by the cancelling moment.
                errors['jz']=float(ratio(r['jz']-rr['jz'],rr['fields'][:8*nz].max(axis=0)).max())
                row=dict(height=H,nz=nz,total=total,checks=check,independent_checks=rc,independent_errors=errors,
                    open_operator_relative=open_error,open_balance_relative=open_balance)
                row['passed']=bool(check['passed'] and rc['passed'] and max(errors.values())<5e-12)
                rows.append(row)
                np.savez_compressed(folder/(name+'.npz'),**r,operator=b['operator'],jz_operator=b['jz'],
                    radial_measure=b['radial_incoming_measure'],volume_measure=b['volume_measure'],
                    reference_operator=ref['operator'],reference_fields=rr['fields'],reference_jz=rr['jz'])
    save(folder/'result.json',dict(model='Manufactured complete three-chord six-surface model; not native geometry',
        angular_rule='Four polars, independent +/- axial sign, both planar orientations, three equal-weight chord pairs',
        closure='6*Nz layer-local common white amplitudes, exact geometric incoming measure; top and bottom vacuum',
        rows=rows,all_checks_passed=all(r['passed'] for r in rows),full_native_white_qualified=False))
    assert all(r['passed'] for r in rows),rows
    print('18 manufactured physical-white cases passed',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('pass_name',choices=['primary','replay'])
    a=p.parse_args();main(a.root.resolve(),a.pass_name)

"""Byte-exact cache qualification against every sealed calibration response."""
import argparse
import json
from pathlib import Path
import numpy as np
from calibrate_native_oblique_streaming import read,save
from native_layered_cached import transport,aggregate
from native_layered_reference import packed


def main(root,case_id):
    old=Path(json.loads((root/'plan.json').read_text())['calibration_root'])
    plan=json.loads((old/'calibration_plan.json').read_text());case=next(c for c in plan['cases'] if c['id']==case_id)
    p,H,nz=case['polar'],case['H'],case['nz'];d=read(root/'inputs/inventory.npz');states=0
    for mode in ['ranked','batch']:
        path=old/'primary'/mode/case_id;expected=json.loads((path/'result.json').read_text())['original_tracks']
        for o in [1,-1]:
            for sign in [-1,1]:
                snapshots=[read(path/f'g{g}_o{o}_m{sign}.npz') for g in [51,61,98]]
                mu=sign*np.sqrt(1-1/d['zmu'][p]**2)
                for track in expected:
                    nr=int(d['nseg'][track]-2);w=d['planar_widths'][track,:nr]*d['zmu'][p];reg=d['nom'][track,1:nr+1]-1
                    entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track]);ex=int(d['exit_surface'][track] if o==1 else d['entry_surface'][track])
                    for order in [8,16,32]:
                        for gi,sigma in enumerate(d['group_totals']):
                            f=transport(root/'build/cached.dylib',w,reg,sigma,entry,H,nz,mu,o,order)
                            actual=dict(geometry=f['geometry'],metrics=f['metrics'],response=packed(aggregate(f['fields'],reg,nz,o,ex)))
                            if mode=='ranked':actual['fields']=f['fields']
                            for key,value in actual.items():
                                target=snapshots[gi][f't{track}_q{order}_{key}']
                                assert value.shape==target.shape and value.tobytes()==target.tobytes(),(case_id,mode,track,gi,o,sign,order,key)
                            states+=1
    save(root/'preflight'/f'cache_{case_id}.json',dict(case=case_id,states=states,all_fields_metrics_geometry_byte_exact=True))
    print(case_id,states,'all byte-exact',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('case');a=p.parse_args();main(a.root.resolve(),a.case)

"""Full original-index geometry inventory; no source response is evaluated."""
import argparse
import ctypes
import hashlib
import json
import resource
import time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

METRICS = ['intervals','chords','pieces','minimum_piece_length','minimum_weight',
    'volume_relative','incoming_relative','outgoing_relative','represented_width_relative',
    'worst_kind','worst_cell','worst_side','worst_actual','worst_expected',
    'zero_piece_count','rounded_endpoint_nodes','minimum_break_width']


def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def read(path):
    with np.load(path) as f:return {k:f[k] for k in f.files}


def scan(library, widths, counts, zmu,H,nz,mu,orientation,order):
    """Materialize only this geometry block's counts and raw local measures."""
    widths=np.ascontiguousarray(widths,dtype=np.float64);counts=np.ascontiguousarray(counts,dtype=np.int32)
    gn,gw=leggauss(order);nt=len(counts)
    metrics=np.zeros((nt,len(METRICS)));raw=np.zeros((nt,15*nz,9))
    kernel=ctypes.CDLL(str(library)).geometry_count
    ptr=ctypes.c_void_p
    kernel.argtypes=[ctypes.c_int,ctypes.c_int,ptr,ptr,ctypes.c_double,ctypes.c_double,
                    ctypes.c_int,ctypes.c_double,ctypes.c_int,ctypes.c_int,ptr,ptr,ptr,ptr]
    kernel.restype=ctypes.c_int
    rc=kernel(nt,widths.shape[1],counts.ctypes.data,widths.ctypes.data,zmu,H,nz,mu,orientation,order,
        gn.ctypes.data,gw.ctypes.data,metrics.ctypes.data,raw.ctypes.data)
    if rc:raise RuntimeError(f'geometry topology failed, code {rc}; no response admission')
    return metrics,raw


def main(root,case):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text())
    spec=next(c for c in plan['preflight_processes'] if c['id']==case)
    d=read(root/'inputs/inventory.npz');p,H,nz=spec['polar'],spec['H'],spec['nz']
    folder=root/'analysis'/case;folder.mkdir();summaries=[]
    counts=d['nseg']-2;mu0=float(np.sqrt(1-1/d['zmu'][p]**2))
    for sign in [-1,1]:
        for orientation in [1,-1]:
            for order in [8,16]:
                label=f'm{sign}_o{orientation}_q{order}'
                metrics,raw=scan(root/'build/geometry_count.dylib',d['planar_widths'],counts,
                    float(d['zmu'][p]),H,nz,sign*mu0,orientation,order)
                assert np.isfinite(raw).all() and np.min(raw)>=0
                # Every original record has one receipt; physical reflections
                # are absent. Retain raw local measures, including zero faces.
                np.savez_compressed(folder/(label+'.npz'),original_track=d['original_track'],
                    multiplicity=np.ones(len(counts),np.uint8),metrics=metrics,raw_measures=raw)
                err=metrics[:,5:8].max(axis=1);worst=int(np.argmax(err))
                summaries.append(dict(label=label,sign=sign,orientation=orientation,order=order,
                    original_records=len(counts),intervals=int(metrics[:,0].sum()),chords=int(metrics[:,1].sum()),
                    pieces=int(metrics[:,2].sum()),maximum_pieces=int(metrics[:,2].max()),
                    geometry_relative=float(err.max()),failed_tracks=int(np.sum(err>=5e-12)),
                    worst_track=worst,worst_metrics=dict(zip(METRICS,metrics[worst].tolist())),
                    rounded_endpoint_nodes=int(metrics[:,15].sum()),zero_piece_count=int(metrics[:,14].sum())))
                del raw,metrics
    save(folder/'result.json',dict(case=spec,configurations=summaries,
        geometry_count_complete=True,source_responses_computed=False))
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=rss)
    save(root/'runs'/(case+'_resources.json'),usage)
    if rss>512 or usage['elapsed_seconds']>600:raise RuntimeError('preflight resource cap exceeded')
    print(case,'max geometry',max(s['geometry_relative'] for s in summaries),'seconds',round(usage['elapsed_seconds'],2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('artifact',type=Path);parser.add_argument('case')
    args=parser.parse_args();main(args.artifact.resolve(),args.case)

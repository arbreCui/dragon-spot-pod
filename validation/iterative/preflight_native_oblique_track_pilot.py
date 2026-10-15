"""Freeze all-path inventory, deterministic selection, and bounded pilot costs."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from qualify_native_directional import load_native
from native_oblique_track_geometry import geometry


def save(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def selection(metrics):
    selected=[];ranks=[]
    for name,values in metrics.items():
        median=np.sort(values)[(len(values)-1)//2]
        for rank,value in [('minimum',values.min()),('lower_median',median),('maximum',values.max())]:
            index=int(np.flatnonzero(values==value)[0])
            selected.append(index);ranks.append(dict(metric=name,rank=rank,value=float(value),track=index))
    return sorted(set(selected)),ranks


def main(a):
    for p,h in json.loads((a/'initial_inputs.json').read_text()).items():assert digest(a/p)==h,p
    d=load_native(a/'inputs/track_data.bin');nt=d['nt'];idx=np.arange(d['nmax'])
    inside=(idx[None,:]>0)&(idx[None,:]<d['nseg'][:,None]-1)
    planar=(d['h2']*inside).sum(axis=1);metrics=dict(physical_length_order=planar,interior_segment_count=d['nseg']-2)
    optical=[];segment_min=[];segment_max=[]
    for material in d['group_data']:
        tau=np.zeros_like(d['h2']);tau[inside]=d['h2'][inside]*material['total'][d['nom'][inside]-1]
        total=tau.sum(axis=1);metrics['optical_'+str(material['group'])]=total
        optical.append(total[:,None]*d['zmu']);segment_max.append(tau.max(axis=1)[:,None]*d['zmu'])
        segment_min.append(np.min(np.where(inside,tau,np.inf),axis=1)[:,None]*d['zmu'])
    selected,ranks=selection(metrics)
    inv={k:d[k] for k in ['nseg','angle','nom','h2','wei','zmu','wzmu','weights','harm','groups']}
    inv.update(original_track=np.arange(nt),original_record_multiplicity=np.ones(nt,int),
        entry_surface=-d['nom'][:,0]-1,exit_surface=-d['nom'][np.arange(nt),d['nseg']-1]-1,
        physical_length=planar[:,None]*d['zmu'],optical_length=np.array(optical),
        minimum_segment_optical=np.array(segment_min),maximum_segment_optical=np.array(segment_max),
        original_half_weight=d['wei'][:,None]*d['wzmu']/2,selected=np.array(selected))
    np.savez_compressed(a/'preflight/inventory.npz',**inv)
    exact={}
    for group in d['groups']:
        with np.load(a/f'inputs/green_{group}.npz') as f:
            lines=(np.array(selected)[:,None]*d['nmu']+np.arange(d['nmu'])).ravel()
            exact[int(group)]={k:f['track_'+k][:,lines].reshape(2,len(selected),d['nmu'],14) for k in ['integral','outgoing']}
    coverage=[]
    for k,track in enumerate(selected):
        count=int(d['nseg'][track]-2);reg=d['nom'][track,1:count+1]-1
        fields=dict(track=np.array(track),segment_index=np.arange(1,count+1),regions=reg,
            planar_widths=d['h2'][track,1:count+1],zmu=d['zmu'],wzmu=d['wzmu'],wei=np.array(d['wei'][track]),
            half_weight=d['wei'][track]*d['wzmu']/2,azimuth=np.array(d['angle'][track]),
            mx=d['harm'][:,2,d['angle'][track]],my=d['harm'][:,1,d['angle'][track]],
            entry_surface=np.array(-d['nom'][track,0]-1),exit_surface=np.array(-d['nom'][track,count+1]-1),
            group_totals=np.array([m['total'] for m in d['group_data']]),groups=d['groups'],stored_native_normalizers=d['weights'],
            exact_track_integral=np.array([exact[int(g)]['integral'][:,k] for g in d['groups']]),
            exact_track_outgoing=np.array([exact[int(g)]['outgoing'][:,k] for g in d['groups']]))
        np.savez_compressed(a/f'inputs/track_{track}.npz',**fields)
        coverage.append(dict(track=track,segments=count,regions=sorted(set(reg.tolist())),
            entry_surface=int(fields['entry_surface']),exit_surface=int(fields['exit_surface'])))
    save(a/'preflight/selection.json',dict(original_tracks=nt,polar_nodes=d['nmu'],selected_tracks=selected,rankings=ranks,coverage=coverage,
        rule='Minimum, lower-median value and maximum of planar length, segment count and each group optical length; every value tie uses the lowest original zero-based track index. Multiplying by any fixed positive ZMU does not change these ranks. Original records are never merged or reweighted.'))
    processes=[];costs=[]
    # A conservative throughput assumption, not a measured native benchmark.
    # Enforcement remains the runtime memory and elapsed-time watchdog.
    throughput=1_000_000.;fixed_seconds=20.;base_bytes=192*1024**2
    for track in selected:
        count=int(d['nseg'][track]-2);base=d['h2'][track,1:count+1]
        for pole in range(d['nmu']):
            widths=base*d['zmu'][pole];mu0=float(np.sqrt(1-1/d['zmu'][pole]**2))
            for H in [1.,20.]:
                for nz in [1,2,4,8]:
                    pid=f't{track}_p{pole}_h{int(H)}_n{nz}';processes.append(dict(id=pid,track=track,polar=pole,H=H,nz=nz))
                    work=0;size=0;peak=0;rows=[]
                    for layout in [0,1]:
                        w=widths if layout==0 else widths[::-1]
                        for sign in [-1,1]:
                            for orientation in [1,-1]:
                                for order in [8,16]:
                                    g=geometry(w,H,nz,sign*mu0,orientation,order)
                                    cells=count*nz;units=cells+nz+count;columns=units+16
                                    nodes=len(g['u']);pieces=len(g['ray']);geom_bytes=sum(v.nbytes for v in g.values())
                                    # Full assembled responses, input coordinates, primitive
                                    # extrema/witnesses and 14 matched endpoint amplitudes.
                                    response_bytes=8*(14*cells*columns+12*pieces+4*nodes*14+32*columns+8*nz*8*nz)
                                    working=base_bytes+geom_bytes+response_bytes+8*(12*nodes*16+5*pieces+4*nodes*columns)
                                    peak=max(peak,working);size+=geom_bytes+3*response_bytes;work+=3*pieces*columns
                                    rows.append(dict(layout=layout,sign=sign,orientation=orientation,order=order,
                                        intervals=len(g['breaks'])-1,nodes=nodes,pieces=pieces,source_units=units,columns=columns,
                                        geometry_bytes=geom_bytes,response_bound_bytes_per_group=response_bytes))
                    estimate=fixed_seconds+work/throughput
                    costs.append(dict(id=pid,piece_column_updates=work,uncompressed_output_bound_bytes=size,
                        estimated_peak_rss_mib=peak/1024**2,estimated_seconds=estimate,rows=rows))
    admitted=all(c['estimated_peak_rss_mib']<512 and c['estimated_seconds']<600 for c in costs)
    save(a/'preflight/costs.json',dict(processes=costs,assumed_piece_columns_per_second=throughput,fixed_seconds_per_process=fixed_seconds,
        maximum_estimated_peak_rss_mib=max(c['estimated_peak_rss_mib'] for c in costs),
        maximum_estimated_seconds=max(c['estimated_seconds'] for c in costs),
        total_piece_column_updates=sum(c['piece_column_updates'] for c in costs),
        total_uncompressed_output_bound_bytes=sum(c['uncompressed_output_bound_bytes'] for c in costs),admitted=admitted,
        interpretation='Conservative structural memory estimate and declared work-rate assumption; actual bounded runs must still meet both caps. No response was computed to select tracks or choose this matrix.'))
    if not admitted:raise RuntimeError('preflight exceeds cap; preserve it without running responses')
    plan=dict(declared_at=datetime.now(timezone.utc).isoformat(),selected_tracks=selected,groups=d['groups'].tolist(),polar_nodes=list(range(d['nmu'])),
        heights=[1.,20.],axial_cells=[1,2,4,8],orders=[8,16],mu_signs=[-1,1],orientations=[1,-1],layouts=[0,1],process_cases=processes,
        source_column_batch=16,numerical_threads=1,peak_rss_limit_mib=512,elapsed_limit_seconds_per_process=600,
        inputs='All segment/axial-cell units, all incoming radial axial-cell units, all incoming axial segment units. Then constant q=sigma/inflow=1, regional-weighted alternating axial source (region+1)/8*(j mod 2), and all original 8 regional-source plus 6 surface-inflow coordinates with exact matched axial inflow. Layout 1 reverses widths/regions and swaps original endpoint surfaces; planar orientation and axial sign remain independent.',
        scales='Geometry relative to original width times height/axial width and physical face measures; exact zero requires exact zero. Primitive balance incoming+length*source; cell/global source birth+incoming. Algebra/region assembly and reflection use maximum positive response per input column. Matched integrated/outgoing errors use maximum positive independent reference per native input coordinate; pointwise uses maximum reference amplitude over endpoints per coordinate. Frozen native track recovery compares maximum positive reference over original 14 coordinates for each track/observable. No fitted floor or clipping.',
        limits=dict(geometry_point_shared_reflection=5e-12,balance=1e-10,native_track_calibration=5e-12,matched_order16=5e-12,assembly=5e-12,minimum_response=0.),
        gate_orders='Geometry, pointwise matched recovery, source-coordinate assembly, positivity, raw balance and both reflections at orders 8 and 16. Matched integrated and outgoing-native-action gate at order16. Preserve order8 errors and alternating 8-to-16 changes; neither proves heterogeneous true error or axial mesh convergence.',
        weights='Retain original wei*wzmu/2 for each independent axial sign. Store partial geometric regional integrals and Jx/Jz with their declared native directional factors; divide matched extruded integrals by H only for comparison to original 1D track response. Do not normalize selected tracks to stored whole-native volume/surface weights. No PJJ correction.',
        scope='All original coordinates on deterministic selected paths only. No full native aggregation, common white return, native mesh convergence, eigenproblem, POD or production modification.')
    save(a/'plan.json',plan)
    print(json.dumps(dict(selected_tracks=selected,processes=len(processes),response_configurations=len(processes)*48,
        maximum_estimated_seconds=max(c['estimated_seconds'] for c in costs),maximum_estimated_peak_rss_mib=max(c['estimated_peak_rss_mib'] for c in costs),
        uncompressed_primary_output_bound_gib=sum(c['uncompressed_output_bound_bytes'] for c in costs)/1024**3,admitted=admitted),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);args=p.parse_args();main(args.artifact)

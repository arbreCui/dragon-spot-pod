"""Independent raw-measure/count audit and complete response cost accounting."""
import argparse
import json
import math
import resource
import shutil
import time
from pathlib import Path
import numpy as np
from native_oblique_full_preflight import read,save,METRICS
from native_oblique_track_geometry import geometry


def topology_count(widths,nz,H,mu,orientation):
    """Count intersections by offset-interval incidence, without tracing chords.

    Each open topology interval contributes one base piece and one extra
    piece for each internal plane it crosses. This is independent of GL order
    when no quadrature node rounds onto an interval endpoint.
    """
    x=np.c_[np.zeros(len(widths)),np.cumsum(widths,axis=1)];S=x[:,-1]
    se=x if orientation==1 else S[:,None]-x[:,::-1]
    z=np.linspace(0,H,nz+1)
    br=np.sort((z[None,:,None]-mu*se[:,None,:]).reshape(len(widths),-1),axis=1)
    left=br[:,:-1];valid=np.diff(br,axis=1)>0;intervals=valid.sum(axis=1)
    pieces=intervals.copy()
    for s in se[:,1:-1].T:
        lo=-mu*s;hi=H-mu*s
        pieces+=(valid&(left>=lo[:,None])&(left<hi[:,None])).sum(axis=1)
    for zv in z[1:-1]:
        end=zv-mu*S;lo=np.minimum(zv,end);hi=np.maximum(zv,end)
        pieces+=(valid&(left>=lo[:,None])&(left<hi[:,None])).sum(axis=1)
    return intervals,pieces


def main(root):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text());d=read(root/'inputs/inventory.npz')
    nt=plan['original_tracks'];counts=d['nseg']-2
    costs=json.loads((root/'inputs/pilot_costs.json').read_text())['processes']
    telemetry=json.loads((root/'inputs/pilot_telemetry.json').read_text())
    rates=[];pilot_work=0;pilot_time=0
    for c in costs:
        for key in [c['id'],'replay/'+c['id']]:
            t=telemetry[key]['elapsed_seconds'];work=c['piece_column_updates']
            rates.append((work/t,key));pilot_work+=work;pilot_time+=t
    slow,slow_id=min(rates);pooled=pilot_work/pilot_time
    pilot_verify=json.loads((root/'inputs/pilot_verification.json').read_text())
    rss_baseline=max(pilot_verify['verification_peak_rss_mib'],max(t['peak_rss_mib'] for t in telemetry.values()))
    totals=dict(geometry_configurations=0,topology_intervals=0,chords=0,pieces=0,geometry_failed_records=0)
    worst=None;files=0;max_piece=0;max_nodes=0;batches=[];whole_seconds=0.;ledger={};groups=3;columns=14
    for case in plan['preflight_processes']:
        p,H,nz=case['polar'],case['H'],case['nz'];mu0=float(np.sqrt(1-1/d['zmu'][p]**2));dz=np.diff(np.linspace(0,H,nz+1))
        folder=root/'analysis'/case['id'];summary=json.loads((folder/'result.json').read_text());case_work=np.zeros(nt,np.int64)
        for sign in [-1,1]:
            for orientation in [1,-1]:
                independent=np.zeros((nt,2),np.int64)
                for nr in np.unique(counts):
                    indices=np.flatnonzero(counts==nr)
                    for first in range(0,len(indices),512):
                        ix=indices[first:first+512];w=d['planar_widths'][ix,:nr]*d['zmu'][p]
                        a,b=topology_count(w,nz,H,sign*mu0,orientation);independent[ix]=np.c_[a,b]
                for order in [8,16]:
                    label=f'm{sign}_o{orientation}_q{order}';f=read(folder/(label+'.npz'));m=f['metrics'];raw=f['raw_measures']
                    np.testing.assert_array_equal(f['original_track'],np.arange(nt));np.testing.assert_array_equal(f['multiplicity'],1)
                    assert raw.shape==(nt,15*nz,9) and np.isfinite(raw).all() and raw.min()>=0
                    np.testing.assert_array_equal(m[:,:3],np.c_[independent[:,0],independent[:,0]*order,independent[:,1]*order])
                    np.testing.assert_array_equal(m[:,14:16],0)
                    actual_error=np.zeros((nt,3));regvol=np.zeros((8,nz));refvol=regvol.copy();surface_in=np.zeros(6);surface_out=surface_in.copy()
                    weight=d['wei']*d['wzmu'][p]/2/H
                    for nr in np.unique(counts):
                        indices=np.flatnonzero(counts==nr)
                        for first in range(0,len(indices),512):
                            ix=indices[first:first+512];w=d['planar_widths'][ix,:nr]*d['zmu'][p]
                            v=raw[ix,:nr*nz].reshape(len(ix),nr,nz,9);expected=np.zeros_like(v)
                            expected[:,:,:,0]=w[:,:,None]*dz
                            for kind,xi,zi in [(1,0 if orientation==1 else 1,2 if sign==1 else 3),
                                               (5,1 if orientation==1 else 0,3 if sign==1 else 2)]:
                                expected[:,:,:,kind+xi]=dz
                                expected[:,:,:,kind+zi]=mu0*w[:,:,None]
                            err=np.divide(abs(v-expected),expected,out=np.zeros_like(v),where=expected>0)
                            assert not np.any((expected==0)&(v!=0))
                            actual_error[ix]=np.c_[err[:,:,:,0].max(axis=(1,2)),err[:,:,:,1:5].max(axis=(1,2,3)),err[:,:,:,5:].max(axis=(1,2,3))]
                            assert np.all(raw[ix,nr*nz:]==0)
                    # Original track first, physical segment second, axial
                    # cell third; preserve every repeated region visit.
                    valid=np.arange(15)[None,:]<counts[:,None]
                    regions=d['nom'][:,1:16][valid]-1
                    full=raw.reshape(nt,15,nz,9)
                    ww=np.broadcast_to(weight[:,None],valid.shape)[valid,None]
                    np.add.at(regvol,regions,full[:,:,:,0][valid]*ww)
                    area=(d['planar_widths']*d['zmu'][p])[:,:,None]*dz
                    np.add.at(refvol,regions,area[valid]*ww)
                    tracks=np.arange(nt);start=np.zeros(nt,int);end=counts-1
                    istart,iend=(start,end) if orientation==1 else (end,start)
                    es=d['entry_surface'] if orientation==1 else d['exit_surface']
                    xs=d['exit_surface'] if orientation==1 else d['entry_surface']
                    np.add.at(surface_in,es,full[tracks,istart,:,1+(0 if orientation==1 else 1)].sum(axis=1)*weight)
                    np.add.at(surface_out,xs,full[tracks,iend,:,5+(1 if orientation==1 else 0)].sum(axis=1)*weight)
                    np.testing.assert_array_equal(actual_error,m[:,5:8])
                    error=actual_error.max(axis=1);at=int(error.argmax());row=next(r for r in summary['configurations'] if r['label']==label)
                    assert float(error[at])==row['geometry_relative'] and at==row['worst_track']
                    if worst is None or error[at]>worst['error']:
                        worst=dict(case=case,label=label,sign=sign,orientation=orientation,order=order,track=at,error=float(error[at]),metrics=dict(zip(METRICS,m[at].tolist())))
                    max_piece=max(max_piece,int(m[:,2].max()));max_nodes=max(max_nodes,int(m[:,1].max()))
                    totals['geometry_configurations']+=nt;totals['topology_intervals']+=int(m[:,0].sum());totals['chords']+=int(m[:,1].sum());totals['pieces']+=int(m[:,2].sum());totals['geometry_failed_records']+=int(np.sum(error>=5e-12))
                    case_work+=m[:,2].astype(np.int64)*groups*columns
                    key=f'h{int(H)}_n{nz}_q{order}'
                    if key not in ledger:ledger[key]={k:np.zeros((2,2,4,*( (8,nz) if 'volume' in k else (6,) )) ) for k in ['volume','reference_volume','surface_in','surface_out']}
                    si=0 if sign==1 else 1;oi=0 if orientation==1 else 1
                    for name,val in [('volume',regvol),('reference_volume',refvol),('surface_in',surface_in),('surface_out',surface_out)]:ledger[key][name][si,oi,p]=val
                    # These are views of this whole input block. In particular
                    # `full` must not keep the previous NPZ alive while the next
                    # block and its validation temporaries are allocated.
                    files+=1
                    del raw,f,full,expected,err,v,actual_error,area,ww
        # Complete conservative batch plan, retaining every coordinate and
        # contiguous original indices. The pilot's startup-limited slowest
        # rate deliberately produces a pessimistic scheduling bound.
        first=0;work=0;cap=(600.-20.)*slow/2
        for tr,w in enumerate(case_work):
            if work and work+int(w)>cap:
                sec=20+2*work/slow;batches.append(dict(case=case['id'],first=first,stop=tr,piece_column_updates=work,estimated_seconds=sec));whole_seconds+=sec;first=tr;work=0
            if int(w)>cap:raise RuntimeError('single record exceeds frozen scheduling cap; retain failure')
            work+=int(w)
        sec=20+2*work/slow;batches.append(dict(case=case['id'],first=first,stop=nt,piece_column_updates=work,estimated_seconds=sec));whole_seconds+=sec
    expected_configs=nt*4*2*3*2*2*2
    assert totals['geometry_configurations']==expected_configs and files==192
    all_ledgers={};normalizers=[]
    for key,values in sorted(ledger.items()):
        volume=values['volume'].sum(axis=(0,1,2,4));refvolume=values['reference_volume'].sum(axis=(0,1,2,4))
        incoming=values['surface_in'].sum(axis=(0,1,2));outgoing=values['surface_out'].sum(axis=(0,1,2))
        normalizers.append(dict(case=key,geometric_volume=volume.tolist(),original_length_volume=refvolume.tolist(),
            stored_volume=d['weights'][:8].tolist(),geometric_surface_in=incoming.tolist(),geometric_surface_out=outgoing.tolist(),stored_surface=d['weights'][8:].tolist(),
            volume_assembly_relative=float(np.max(abs(volume-refvolume)/refvolume)),
            stored_volume_relative=float(np.max(abs(volume-d['weights'][:8])/d['weights'][:8])),
            stored_surface_relative=float(np.max(abs(outgoing-d['weights'][8:])/d['weights'][8:]))))
        all_ledgers.update({key+'_'+k:v for k,v in values.items()})
    np.savez_compressed(root/'preflight/geometric_ledgers.npz',**all_ledgers)
    save(root/'preflight/normalizer_ledgers.json',normalizers)
    # Independently materialize the complete worst original geometry.
    c=worst['case'];tr=worst['track'];nr=counts[tr];p=c['polar'];w=d['planar_widths'][tr,:nr]*d['zmu'][p]
    g=geometry(w,c['H'],c['nz'],worst['sign']*np.sqrt(1-1/d['zmu'][p]**2),worst['orientation'],worst['order'])
    f=read(root/'analysis'/c['id']/(worst['label']+'.npz'));raw=f['raw_measures'][tr,:nr*c['nz']]
    np.testing.assert_array_equal(raw[:,0],g['volume']);np.testing.assert_array_equal(raw[:,1:5],g['face_in_measure']);np.testing.assert_array_equal(raw[:,5:],g['face_out_measure'])
    np.savez_compressed(root/'preflight/worst_literal_geometry.npz',**g)
    save(root/'preflight/worst_geometry.json',worst)
    # Conservative future response-output schema: at most 32 float64 values
    # per original source coordinate/track case, plus 1 MiB per aggregate batch.
    configurations=totals['geometry_configurations']*groups;work=totals['pieces']*groups*columns
    response_bytes=configurations*columns*32*8+len(batches)*1024**2
    # Keep the observed 379.7 MiB base, add actual maximum bounded geometry and
    # 14-column primitive temporaries; output accumulators are streamed.
    extra=8*(max_piece*(12+columns*12)+max_nodes*columns*4)+8*15*4*9*columns
    memory=rss_baseline+extra/1024**2
    schedule=dict(processes=batches,original_track_configurations=configurations,source_coordinate_evaluations=configurations*columns,
        piece_column_updates=work,slowest_observed_pilot_rate=slow,slowest_rate_case=slow_id,pooled_observed_pilot_rate=pooled,
        conservative_primary_plus_replay_seconds=2*whole_seconds,
        pooled_rate_primary_plus_replay_seconds=2*work/pooled,
        timing_interpretation='The conservative plan includes twice the slowest observed pilot work time plus 20 seconds per batch. That slow rate includes startup on a one-segment path; it is deliberately pessimistic, not a forecast of the unimplemented streaming worker. The pooled extrapolation is context only, not an admission rate.',
        observed_rss_baseline_mib=rss_baseline,estimated_peak_rss_mib=memory,
        maximum_batch_estimated_seconds=max(b['estimated_seconds'] for b in batches),
        response_primary_output_bound_bytes=response_bytes,response_primary_plus_replay_output_bound_bytes=2*response_bytes,
        disk_reserve_bytes=1024**3,free_bytes_at_summary=shutil.disk_usage(root).free,
        full_primitive_trace_bytes_at_five_float64_values=work*5*8,
        process_estimates_within_caps=bool(memory<512 and max(b['estimated_seconds'] for b in batches)<600),
        storage_estimate_admitted=bool(shutil.disk_usage(root).free>2*response_bytes+1024**3),
        response_execution_admitted=False,
        pending='Implement and independently qualify bounded 14-column streaming worker; benchmark whole primary-plus-replay cost before source-response execution. Preflight contains zero response solves.')
    save(root/'preflight/response_costs_and_batches.json',schedule)
    totals.update(geometry_files_audited=files,maximum_piece_count_per_geometry=max_piece,maximum_chords_per_geometry=max_nodes,
        maximum_geometry_relative=worst['error'],geometry_measure_audit_passed=bool(totals['geometry_failed_records']==0),
        original_index_and_independent_topology_counts_passed=True,
        whole_native_zero_gradient_operator_qualified=False,common_white_recovery_qualified=False,physical_axial_escape_qualified=False,
        source_responses_computed=0,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/'preflight/result.json',totals)
    if totals['peak_rss_mib']>512 or totals['elapsed_seconds']>600:
        raise RuntimeError('audit resource cap exceeded; preserve the failed audit')
    print(json.dumps(totals,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);a=p.parse_args();main(a.artifact.resolve())

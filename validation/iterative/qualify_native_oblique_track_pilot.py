"""Frozen native-path pilot: full source cone and independent matched flight."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from native_oblique_track_geometry import geometry
from native_oblique_track_pilot import direct_flight,transport,matched_fields,column_error,reflections
from oblique_strip_geometry import relative
from qualify_oblique_strip_geometry import geometry_metrics,read,save
from native_oblique_track_storage import pack_geometry,pack_responses,unpack_geometry,unpack_responses


def label(layout,sign,orientation,order,group):
    return f'l{layout}_m{sign}_o{orientation}_q{order}_g{group}'


def diagnostic(g,f,flight,expected_int,expected_out,limits):
    u=int(f['units']);refint,refface=matched_fields(g,flight);geom,ei,eo=geometry_metrics(g)
    nr,nz=int(g['nr']),int(g['nz']);H=float(g['H'])
    exitcell=nr-1 if g['orientation']==1 else 0;exitside=1 if g['orientation']==1 else 0
    radial=f['face_out'].reshape(nr,nz,4,-1)[exitcell,:,exitside,u+2:].sum(axis=0)/H
    whole=f['integral'][:,u+2:].sum(axis=0)/H
    native_error=max(float(relative(flight['track_integral']-expected_int,abs(expected_int).max()).max()),
                     float(relative(flight['track_outgoing']-expected_out,abs(expected_out).max()).max()))
    row=dict(geometry_relative=geom,
        original_segment_length_relative=float(relative(g['represented_widths']-g['original_widths'],g['original_widths']).max()),
        constant_relative=max(float(relative(f['integral'][:,u]-g['area'],g['area']).max()),
            float(relative(f['face_in'][...,u]-ei,ei).max()),float(relative(f['face_out'][...,u]-eo,eo).max())),
        piece_balance_relative=float(f['maximum_piece_relative'].max()),
        cell_balance_relative=float(relative(f['cell_defect'],f['cell_scale']).max()),
        global_balance_relative=float(relative(f['global_defect'],f['global_scale']).max()),
        shared_face_relative=float(relative(f['shared_defect'],f['shared_scale']).max(initial=0)),
        matched_point_relative=float(relative(f['matched_endpoint_defect'],f['matched_endpoint_scale']).max()),
        matched_integral_relative=column_error(f['integral'][:,u+2:],refint),
        matched_current_relative=column_error(f['face_out'][...,u+2:],refface),
        frozen_native_track_calibration_relative=native_error,
        matched_native_integral_relative=float(relative(whole-expected_int,abs(expected_int).max()).max()),
        matched_native_outgoing_relative=float(relative(radial-expected_out,abs(expected_out).max()).max()),
        source_assembly_relative=float(f['source_assembly_relative'].max()),
        minimum_angle=float(min(f['minimum_piece_angle'].min(),f['matched_exit_angle'].min())),
        minimum_integral=float(min(f['minimum_piece_integral'].min(),f['integral'].min())),
        minimum_current=float(min(f['face_in'].min(),f['face_out'].min())),
        finite=all(np.isfinite(v).all() for v in f.values()),source_units=u,total_inputs=f['q'].shape[1])
    row['all_order_gates_passed']=bool(row['finite'] and min(row[k] for k in ['minimum_angle','minimum_integral','minimum_current'])>=0
        and max(row[k] for k in ['geometry_relative','original_segment_length_relative','constant_relative','shared_face_relative','matched_point_relative'])<limits['geometry_point_shared_reflection']
        and max(row[k] for k in ['piece_balance_relative','cell_balance_relative','global_balance_relative'])<limits['balance']
        and row['frozen_native_track_calibration_relative']<limits['native_track_calibration'] and row['source_assembly_relative']<limits['assembly'])
    row['integrated_gates_passed']=None if int(g['order'])!=16 else bool(max(row[k] for k in [
        'matched_integral_relative','matched_current_relative','matched_native_integral_relative','matched_native_outgoing_relative'])<limits['matched_order16'])
    return row,dict(matched_integral=refint,matched_current=refface,matched_native_integral=whole,
                   matched_native_outgoing=radial,expected_native_integral=expected_int,expected_native_outgoing=expected_out)


def run(a,pid):
    plan=json.loads((a/'plan.json').read_text());case=next(c for c in plan['process_cases'] if c['id']==pid)
    data=read(a/f'inputs/track_{case["track"]}.npz');pole=case['polar'];H=case['H'];nz=case['nz']
    widths0=data['planar_widths']*data['zmu'][pole];mu0=np.sqrt(1-1/data['zmu'][pole]**2)
    folder=a/'analysis'/pid;folder.mkdir();rows=[]
    for layout in plan['layouts']:
        widths=widths0 if layout==0 else widths0[::-1]
        regions=data['regions'] if layout==0 else data['regions'][::-1]
        for sign in plan['mu_signs']:
            for orientation in plan['orientations']:
                effective=orientation*(1 if layout==0 else -1);oi=0 if effective==1 else 1
                entry=int(data['entry_surface'] if effective==1 else data['exit_surface'])
                flights={int(group):direct_flight(widths,data['group_totals'][gi,regions],regions,entry,orientation) for gi,group in enumerate(data['groups'])}
                for order in plan['orders']:
                    g=geometry(widths,H,nz,sign*mu0,orientation,order)
                    g.update(original_track=data['track'],polar=np.array(pole),regions=regions,layout=np.array(layout),
                        effective_orientation=np.array(effective),native_half_weight=data['half_weight'][pole],native_mx=data['mx'][pole])
                    np.savez_compressed(folder/f'geometry_l{layout}_m{sign}_o{orientation}_q{order}.npz',**pack_geometry(g))
                    for gi,group in enumerate(data['groups']):
                        flight=flights[int(group)];total=data['group_totals'][gi,regions]
                        f=transport(g,total,regions,flight,float(data['half_weight'][pole]),float(data['mx'][pole]),effective,plan['source_column_batch'])
                        row,ref=diagnostic(g,f,flight,data['exact_track_integral'][gi,oi,pole],data['exact_track_outgoing'][gi,oi,pole],plan['limits'])
                        name=label(layout,sign,orientation,order,int(group));row.update(case=pid,label=name,layout=layout,sign=sign,orientation=orientation,order=order,group=int(group))
                        np.savez_compressed(folder/(name+'.npz'),**pack_responses(g,f))
                        np.savez_compressed(folder/(name+'_reference.npz'),**{k:v for k,v in ref.items() if k not in ['matched_integral','matched_current']},**{'flight_'+k:v for k,v in flight.items()})
                        rows.append(row)
    checks=[];changes=[];nr=len(widths0)
    for row in rows:
        layout,sign,orientation,order,group=[row[k] for k in ['layout','sign','orientation','order','group']]
        g=unpack_geometry(read(folder/f'geometry_l{layout}_m{sign}_o{orientation}_q{order}.npz'))
        f=unpack_responses(g,read(folder/(row['label']+'.npz')))
        if sign==-1:
            rg=unpack_geometry(read(folder/f'geometry_l{layout}_m1_o{orientation}_q{order}.npz'))
            ref=unpack_responses(rg,read(folder/(label(layout,1,orientation,order,group)+'.npz')))
            checks.append(dict(label=row['label'],axis='z',relative=reflections(f,ref,nr,nz,'z')))
        if layout==1:
            rg=unpack_geometry(read(folder/f'geometry_l0_m{sign}_o{-orientation}_q{order}.npz'))
            ref=unpack_responses(rg,read(folder/(label(0,sign,-orientation,order,group)+'.npz')))
            checks.append(dict(label=row['label'],axis='x',relative=reflections(f,ref,nr,nz,'x')))
        if order==8:
            rg=unpack_geometry(read(folder/f'geometry_l{layout}_m{sign}_o{orientation}_q16.npz'))
            ref=unpack_responses(rg,read(folder/(label(layout,sign,orientation,16,group)+'.npz')));u=int(f['units']);change={}
            for key in ['integral','face_out']:
                value=ref[key][...,u+1];change[key]=float(relative(f[key][...,u+1]-value,abs(value).max()).max())
            changes.append(dict(label=row['label'],**change))
    result=dict(case=case,rows=rows,reflections=checks,alternating_order8_to16=changes,
        selected_track_pilot_qualified=bool(all(r['all_order_gates_passed'] and r['integrated_gates_passed'] is not False for r in rows)
            and all(r['relative']<plan['limits']['geometry_point_shared_reflection'] for r in checks)),
        whole_native_geometry_qualified=False,native_axial_white_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    save(folder/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','reflections','alternating_order8_to16']},indent=2))


def summarize(a):
    plan=json.loads((a/'plan.json').read_text());parts=[json.loads((a/'analysis'/c['id']/'result.json').read_text()) for c in plan['process_cases']]
    rows=[r for p in parts for r in p['rows']];checks=[dict(case=p['case']['id'],**r) for p in parts for r in p['reflections']]
    changes=[dict(case=p['case']['id'],**r) for p in parts for r in p['alternating_order8_to16']]
    keys=[k for k in rows[0] if k.endswith('_relative')];orders={}
    for order in plan['orders']:
        group=[r for r in rows if r['order']==order];orders[str(order)]={}
        for key in keys:
            witness=max(group,key=lambda r:r[key]);orders[str(order)][key]=dict(value=witness[key],case=witness['case'],label=witness['label'])
    result=dict(selected_tracks=plan['selected_tracks'],process_cases=len(parts),response_configurations=len(rows),
        source_unit_evaluations=sum(r['source_units'] for r in rows),total_input_evaluations=sum(r['total_inputs'] for r in rows),
        order_maxima=orders,reflection_comparisons=len(checks),maximum_reflection=max(checks,key=lambda x:x['relative']),
        maximum_alternating_integral_change=max(changes,key=lambda x:x['integral']),maximum_alternating_current_change=max(changes,key=lambda x:x['face_out']),
        failed_all_order_rows=[dict(case=r['case'],label=r['label']) for r in rows if not r['all_order_gates_passed']],
        failed_integrated_rows=[dict(case=r['case'],label=r['label']) for r in rows if r['integrated_gates_passed'] is False],
        selected_track_pilot_qualified=all(p['selected_track_pilot_qualified'] for p in parts),
        whole_native_geometry_qualified=False,native_axial_white_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    save(a/'analysis/result.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('case');args=p.parse_args();start=time.monotonic()
    summarize(args.artifact) if args.case=='summary' else run(args.artifact,args.case)
    usage=dict(elapsed_seconds=time.monotonic()-start,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(args.artifact/'runs'/(args.case+'_resources.json'),usage)
    if usage['elapsed_seconds']>600 or usage['peak_rss_mib']>512:raise RuntimeError('frozen resource cap exceeded')

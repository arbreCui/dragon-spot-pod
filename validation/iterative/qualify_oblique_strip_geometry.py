"""Run the frozen manufactured geometry matrix and retain every gate."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from oblique_strip_geometry import geometry, sweep, relative
from oblique_strip_reference import one_d, homogeneous, matched


def read(path):
    with np.load(path) as z:return {k:z[k] for k in z.files}


def save(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def label(sign,orientation,order,profile):
    return f'm{sign}_o{orientation}_q{order}_p{profile}'


def geometry_metrics(g):
    expected_in=np.zeros_like(g['face_measure']);expected_out=expected_in.copy()
    xi,xo=(0,1) if g['orientation']==1 else (1,0)
    expected_in[:,xi]=g['face_measure'][:,xi];expected_out[:,xo]=g['face_measure'][:,xo]
    if g['mu']:
        zi,zo=(2,3) if g['mu']>0 else (3,2)
        expected_in[:,zi]=g['face_measure'][:,zi];expected_out[:,zo]=g['face_measure'][:,zo]
    error=max(float(relative(g['volume']-g['area'],g['area']).max()),
              float(relative(g['face_in_measure']-expected_in,expected_in).max()),
              float(relative(g['face_out_measure']-expected_out,expected_out).max()))
    return error,expected_in,expected_out


def diagnostics(g,f,reference,lim):
    u=int(f['units']);geom,ei,eo=geometry_metrics(g)
    constant=max(float(relative(f['integral'][:,u]-g['area'],g['area']).max()),
                 float(relative(f['face_in'][...,u]-ei,ei).max()),float(relative(f['face_out'][...,u]-eo,eo).max()))
    row=dict(geometry_relative=geom,constant_relative=constant,
        piece_balance_relative=float(f['maximum_piece_relative'].max()),
        cell_balance_relative=float(relative(f['cell_defect'],f['cell_scale']).max()),
        global_balance_relative=float(relative(f['global_defect'],f['global_scale']).max()),
        shared_face_relative=float(relative(f['shared_defect'],f['shared_scale']).max(initial=0)),
        matched_point_relative=float(f['matched_point_relative']),
        matched_integral_relative=float(relative(f['integral'][:,u+2]-reference['matched_integral'],reference['matched_integral']).max()),
        matched_current_relative=float(relative(f['face_out'][...,u+2]-reference['matched_current'],reference['matched_current']).max()),
        minimum_angle=float(min(f['minimum_piece_angle'].min(),f['exit_angle'].min())),
        minimum_integral=float(min(f['minimum_piece_integral'].min(),f['integral'].min())),
        minimum_current=float(min(f['face_in'].min(),f['face_out'].min())),
        source_units=u,total_inputs=f['q'].shape[1],finite=all(np.isfinite(v).all() for v in f.values()))
    if 'analytic_integral' in reference:
        row['analytic_mean_relative']=float(relative(f['integral'][:,u+1]-reference['analytic_integral'],reference['analytic_integral']).max())
        row['analytic_current_relative']=float(relative(f['face_out'][...,u+1]-reference['analytic_current'],reference['analytic_current']).max())
    row['all_order_gates_passed']=bool(row['finite'] and min(row[k] for k in ['minimum_angle','minimum_integral','minimum_current'])>=0
        and max(row[k] for k in ['geometry_relative','constant_relative','shared_face_relative'])<lim['geometry_constant_reflection_shared']
        and row['matched_point_relative']<lim['matched_1d']
        and max(row[k] for k in ['piece_balance_relative','cell_balance_relative','global_balance_relative'])<lim['balance'])
    row['integrated_gates_applicable']=int(g['order'])==16
    row['integrated_gates_passed']=None if not row['integrated_gates_applicable'] else bool(
        max(row['matched_integral_relative'],row['matched_current_relative'])<lim['matched_1d']
        and max(row.get('analytic_mean_relative',0),row.get('analytic_current_relative',0))<lim['analytic_order16'])
    return row


def reflection_error(target,reference,nr,nz,mu,axis):
    n=nr*nz;u=int(target['units']);cells=np.arange(n).reshape(nr,nz)
    perm=(cells[:,::-1] if axis=='z' else cells[::-1,:]).ravel()
    radial=np.arange(n,n+nz);axial=np.arange(n+nz,u)
    if axis=='z':radial=radial[::-1]
    else:axial=axial[::-1]
    # Matched radial source is fixed in physical coordinates and need not be
    # invariant under planar reflection. It has its own independent 1D test.
    controls=3 if axis=='z' else 2
    cols=np.r_[perm,radial,axial,np.arange(u,u+controls)]
    sides=[0,1,3,2] if axis=='z' else [1,0,2,3]
    error=0.
    for key in ['integral','face_in','face_out']:
        ref=reference[key][perm]
        if ref.ndim==3:ref=ref[:,sides]
        ref=ref[...,cols];actual=target[key][...,:u+controls]
        scale=np.max(abs(ref),axis=tuple(range(ref.ndim-1)))
        error=max(error,float(relative(actual-ref,scale).max()))
    return error


def run(a,case_id):
    plan=json.loads((a/'plan.json').read_text());case=next(x for x in plan['process_cases'] if x['id']==case_id)
    folder=a/'analysis'/case_id;folder.mkdir();S,H,nz=case['S'],case['H'],case['nz'];rows=[]
    profiles=plan['material_profiles'];lim=plan['limits'];geometries={};references={}
    for sign in plan['mu_signs']:
        mu=sign*plan['mu_magnitude']
        for orientation in plan['orientations']:
            for order in plan['orders']:
                for pi,profile in enumerate(profiles):
                    nr=len(profile);key=(sign,orientation,order,nr)
                    if key not in geometries:
                        g=geometry(S,H,nr,nz,mu,orientation,order);geometries[key]=g
                        np.savez_compressed(folder/f'geometry_m{sign}_o{orientation}_q{order}_r{nr}.npz',**g)
                    g=geometries[key];rkey=(sign,orientation,pi)
                    if rkey not in references:
                        mi,mc=matched(S,H,nr,nz,mu,orientation,np.array(profile))
                        ref=dict(matched_integral=mi,matched_current=mc)
                        if len(set(profile))==1:
                            ai,ac=homogeneous(S,H,nr,nz,mu,orientation,profile[0]);ref.update(analytic_integral=ai,analytic_current=ac)
                        references[rkey]=ref
                        np.savez_compressed(folder/f'reference_m{sign}_o{orientation}_p{pi}.npz',**ref)
                    ref=references[rkey];f=sweep(g,np.array(profile),one_d)
                    name=label(sign,orientation,order,pi);np.savez_compressed(folder/(name+'.npz'),**f)
                    row=diagnostics(g,f,ref,lim);row.update(case=case_id,sign=sign,orientation=orientation,order=order,profile=pi,label=name)
                    rows.append(row)
    reflections=[];changes=[]
    for row in rows:
        sign,orientation,order,pi=[row[k] for k in ['sign','orientation','order','profile']]
        f=read(folder/(row['label']+'.npz'));nr=len(profiles[pi])
        if sign==-1:
            ref=read(folder/(label(1,orientation,order,pi)+'.npz'))
            reflections.append(dict(label=row['label'],axis='z',relative=reflection_error(f,ref,nr,nz,-plan['mu_magnitude'],'z')))
        if orientation==-1:
            reverse=profiles.index(profiles[pi][::-1]);ref=read(folder/(label(sign,1,order,reverse)+'.npz'))
            reflections.append(dict(label=row['label'],axis='x',relative=reflection_error(f,ref,nr,nz,sign*plan['mu_magnitude'],'x')))
        if order==8 and len(set(profiles[pi]))>1:
            ref=read(folder/(label(sign,orientation,16,pi)+'.npz'));u=int(f['units']);change={}
            for key in ['integral','face_out']:
                v=ref[key][...,u+3];delta=f[key][...,u+3]-v
                change[key]=float(relative(delta,np.max(abs(v))).max())
            changes.append(dict(label=row['label'],**change))
    result=dict(case=case,rows=rows,reflections=reflections,alternating_order8_to16=changes,
        prototype_qualified=bool(all(r['all_order_gates_passed'] and r['integrated_gates_passed'] is not False for r in rows)
            and all(r['relative']<lim['geometry_constant_reflection_shared'] for r in reflections)),
        native_bridge_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    save(folder/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','reflections','alternating_order8_to16']},indent=2))


def summarize(a):
    plan=json.loads((a/'plan.json').read_text());parts=[json.loads((a/'analysis'/c['id']/'result.json').read_text()) for c in plan['process_cases']]
    rows=[r for p in parts for r in p['rows']];by_order={}
    keys=['geometry_relative','constant_relative','piece_balance_relative','cell_balance_relative','global_balance_relative',
          'shared_face_relative','matched_point_relative','matched_integral_relative','matched_current_relative','analytic_mean_relative','analytic_current_relative']
    for order in plan['orders']:
        group=[r for r in rows if r['order']==order];by_order[str(order)]={}
        for key in keys:
            witness=max((r for r in group if key in r),key=lambda r:r[key])
            by_order[str(order)][key]=dict(value=witness[key],case=witness['case'],label=witness['label'])
    reflections=[dict(case=p['case']['id'],**r) for p in parts for r in p['reflections']]
    changes=[dict(case=p['case']['id'],**r) for p in parts for r in p['alternating_order8_to16']]
    result=dict(process_cases=len(parts),material_direction_order_cases=len(rows),source_unit_evaluations=sum(r['source_units'] for r in rows),
        total_input_evaluations=sum(r['total_inputs'] for r in rows),order_maxima=by_order,
        reflection_comparisons=len(reflections),maximum_reflection=max(reflections,key=lambda r:r['relative']),
        alternating_maximum_integral_change=max(changes,key=lambda r:r['integral']),
        alternating_maximum_current_change=max(changes,key=lambda r:r['face_out']),
        minimum_response=min(r[k] for r in rows for k in ['minimum_angle','minimum_integral','minimum_current']),
        failed_all_order_rows=[dict(case=r['case'],label=r['label']) for r in rows if not r['all_order_gates_passed']],
        failed_integrated_rows=[dict(case=r['case'],label=r['label']) for r in rows if r['integrated_gates_passed'] is False],
        prototype_qualified=all(p['prototype_qualified'] for p in parts),native_bridge_qualified=False,
        native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    save(a/'analysis/result.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('case')
    args=p.parse_args();start=time.monotonic()
    summarize(args.artifact) if args.case=='summary' else run(args.artifact,args.case)
    usage=dict(elapsed_seconds=time.monotonic()-start,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(args.artifact/'runs'/(args.case+'_resources.json'),usage)
    if usage['elapsed_seconds']>600 or usage['peak_rss_mib']>512:raise RuntimeError('frozen resource cap exceeded')

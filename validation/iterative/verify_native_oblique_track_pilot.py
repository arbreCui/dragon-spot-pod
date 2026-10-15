"""Independent raw-field, native-input, primitive-witness and replay audit."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from scipy.integrate import quad
from qualify_native_directional import load_native
from qualify_oblique_strip_geometry import read,geometry_metrics
from native_oblique_track_storage import unpack_geometry,unpack_responses
from native_oblique_track_pilot import matched_fields,column_error,reflections
from qualify_native_oblique_track_pilot import label


def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def ratio(d,s):
    d,s=np.broadcast_arrays(abs(d),s);assert not np.any((s==0)&(d!=0))
    return np.divide(d,s,out=np.zeros_like(d),where=s>0)


def audit_native_inputs(a):
    d=load_native(a/'inputs/track_data.bin');selection=json.loads((a/'preflight/selection.json').read_text())
    inventory=read(a/'preflight/inventory.npz');mask=(np.arange(d['nmax'])[None,:]>0)&(np.arange(d['nmax'])[None,:]<d['nseg'][:,None]-1)
    length=(d['h2']*mask).sum(axis=1);metrics=dict(physical_length_order=length,interior_segment_count=d['nseg']-2)
    for gi,m in enumerate(d['group_data']):
        tau=np.zeros_like(d['h2']);tau[mask]=d['h2'][mask]*m['total'][d['nom'][mask]-1]
        metrics['optical_'+str(m['group'])]=tau.sum(axis=1)
        np.testing.assert_array_equal(inventory['optical_length'][gi],tau.sum(axis=1)[:,None]*d['zmu'])
    chosen=[]
    for row in selection['rankings']:
        v=metrics[row['metric']];value={'minimum':min(v),'maximum':max(v),'lower_median':sorted(v)[(len(v)-1)//2]}[row['rank']]
        index=next(i for i,x in enumerate(v) if x==value);assert index==row['track'] and value==row['value'];chosen.append(index)
    assert sorted(set(chosen))==selection['selected_tracks']
    for track in selection['selected_tracks']:
        data=read(a/f'inputs/track_{track}.npz');n=int(d['nseg'][track]-2)
        np.testing.assert_array_equal(data['planar_widths'],d['h2'][track,1:n+1])
        np.testing.assert_array_equal(data['regions'],d['nom'][track,1:n+1]-1)
        np.testing.assert_array_equal(data['half_weight'],d['wei'][track]*d['wzmu']/2)
        np.testing.assert_array_equal(data['mx'],d['harm'][:,2,d['angle'][track]])
        np.testing.assert_array_equal(data['group_totals'],[g['total'] for g in d['group_data']])
        assert int(data['entry_surface'])==-int(d['nom'][track,0])-1
        assert int(data['exit_surface'])==-int(d['nom'][track,n+1])-1
        lines=track*d['nmu']+np.arange(d['nmu'])
        for gi,group in enumerate(d['groups']):
            with np.load(a/f'inputs/green_{group}.npz') as green:
                np.testing.assert_array_equal(data['exact_track_integral'][gi],green['track_integral'][:,lines])
                np.testing.assert_array_equal(data['exact_track_outgoing'][gi],green['track_outgoing'][:,lines])
    return len(selection['selected_tracks'])


def geometry_audit(g):
    assert all(np.isfinite(v).all() for v in g.values())
    ray=g['ray'];cell=g['cell'];mid=(g['s0']+g['s1'])/2
    assert np.min(g['length'])>0 and np.min(g['weight'])>0
    x=mid if g['orientation']==1 else float(g['S'])-mid;z=g['u'][ray]+float(g['mu'])*mid
    i=np.searchsorted(g['x'],x,side='right')-1;j=np.searchsorted(g['z'],z,side='right')-1
    np.testing.assert_array_equal(cell,i*int(g['nz'])+j)
    first=np.r_[True,np.diff(ray)!=0];last=np.r_[np.diff(ray)!=0,True]
    np.testing.assert_array_equal(g['s0'][~first],g['s1'][~last])
    np.testing.assert_array_equal(g['in_side'][~first],g['out_side'][~last]^1)
    for s,side in [(g['s0'][first],g['in_side'][first]),(g['s1'][last],g['out_side'][last])]:
        xp=s if g['orientation']==1 else float(g['S'])-s;zp=g['u']+float(g['mu'])*s
        dist=np.choose(side,[xp,xp-float(g['S']),zp,zp-float(g['H'])])
        assert abs(dist).max()<5e-12*max(float(g['S']),float(g['H']))


def raw_audit(g,p,ref,total,row):
    nr,nz=int(g['nr']),int(g['nz']);c=nr*nz;u=int(p['units']);k=u+16
    assert u==c+nz+nr and p['integral'].shape==(c,k)
    assert all(np.isfinite(v).all() for v in p.values())
    for key in ['integral','radial_face','axial_face','minimum_input_angle','minimum_input_integral']:assert p[key].min()>=0
    f=unpack_responses(g,p);fi,fo=f['face_in'],f['face_out'];q=np.zeros((c,k));q[:,:c]=np.eye(c)
    sigma=np.repeat(total,nz);q[:,u]=sigma
    q[:,u+1]=np.repeat((g['regions']+1)/8,nz)*np.tile(np.arange(nz)%2,nr)
    q[:,u+2:]=np.repeat(np.eye(14)[g['regions']],nz,axis=0)
    A=np.zeros((c,8*nz));A[np.arange(c),np.repeat(g['regions'],nz)*nz+np.tile(np.arange(nz),nr)]=1
    np.testing.assert_array_equal(A@np.repeat(np.eye(8),nz,axis=0),q[:,u+2:u+10])
    birth=g['area'][:,None]*q;collision=sigma[:,None]*f['integral']
    cell_defect=birth+fi.sum(axis=1)-fo.sum(axis=1)-collision
    cell_error=float(ratio(cell_defect,birth+fi.sum(axis=1)).max());assert cell_error==row['cell_balance_relative']
    inf=fi.reshape(nr,nz,4,k);out=fo.reshape(nr,nz,4,k)
    incoming=sum(v.sum(axis=0) for v in [inf[0,:,0],inf[-1,:,1],inf[:,0,2],inf[:,-1,3]])
    outgoing=sum(v.sum(axis=0) for v in [out[0,:,0],out[-1,:,1],out[:,0,2],out[:,-1,3]])
    supplied=birth.sum(axis=0)+incoming
    global_error=float(ratio(supplied-outgoing-collision.sum(axis=0),supplied).max());assert global_error<1e-10
    geom,ei,eo=geometry_metrics(g)
    constant=max(float(ratio(f['integral'][:,u]-g['area'],g['area']).max()),float(ratio(fi[...,u]-ei,ei).max()),float(ratio(fo[...,u]-eo,eo).max()))
    assert geom==row['geometry_relative'] and constant==row['constant_relative']
    # The archived unit action must assemble both a regional/axial source and
    # the constant solution without fitting the actual separately swept controls.
    assembly=[]
    alt=np.repeat(np.arange(1,9)/8,nz)*np.tile(np.arange(nz)%2,8)
    for v in [f['integral'],fi,fo]:
        assembly.extend([float(ratio(v[...,:c]@(A@alt)-v[...,u+1],abs(v[...,u+1]).max()).max()),
                         float(ratio(v[...,:c]@sigma+v[...,c:u].sum(axis=-1)-v[...,u],abs(v[...,u]).max()).max())])
    np.testing.assert_array_equal(assembly,p['source_assembly_relative']);assert max(assembly)==row['source_assembly_relative']
    # Recheck each input's worst actual primitive using independent scalar
    # quadrature. These witnesses supplement, not replace, complete replay.
    ids=p['worst_input_piece'].astype(int);w=p['worst_input_witness'];source=q[g['cell'][ids],np.arange(k)]
    lengths=g['length'][ids];sig=sigma[g['cell'][ids]]
    np.testing.assert_array_equal(w[:,4],w[:,0]+lengths*source)
    np.testing.assert_array_equal(w[:,3],w[:,1]-w[:,0]+sig*w[:,2]-lengths*source)
    np.testing.assert_array_equal(ratio(w[:,3],w[:,4]),p['maximum_piece_relative'])
    primitive=float(p['maximum_piece_relative'].max());assert primitive==row['piece_balance_relative']
    cache={};quad_out=np.empty(k);quad_int=np.empty(k)
    for j,(l,s) in enumerate(zip(lengths,sig)):
        key=(float(l),float(s))
        if key not in cache:
            cache[key]=(math.exp(-s*l),quad(lambda x:math.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0],
                        quad(lambda x:(l-x)*math.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0])
        t,b,d=cache[key];quad_out[j]=t*w[j,0]+b*source[j];quad_int[j]=b*w[j,0]+d*source[j]
    witness_error=max(float(ratio(w[:,1]-quad_out,w[:,4]).max()),float(ratio(w[:,2]-quad_int,lengths*w[:,4]).max()))
    assert witness_error<5e-12
    flight={key.removeprefix('flight_'):v for key,v in ref.items() if key.startswith('flight_')}
    ri,rf=matched_fields(g,flight)
    assert column_error(f['integral'][:,u+2:],ri)==row['matched_integral_relative']
    assert column_error(fo[...,u+2:],rf)==row['matched_current_relative']
    endpoint=float(ratio(p['matched_endpoint_defect'],p['matched_endpoint_scale']).max());assert endpoint==row['matched_point_relative']
    whole=f['integral'][:,u+2:].sum(axis=0)/float(g['H'])
    side=1 if g['orientation']==1 else 0;cell=nr-1 if g['orientation']==1 else 0
    radial=out[cell,:,side,u+2:].sum(axis=0)/float(g['H'])
    np.testing.assert_array_equal(whole,ref['matched_native_integral']);np.testing.assert_array_equal(radial,ref['matched_native_outgoing'])
    assert float(ratio(whole-ref['expected_native_integral'],abs(ref['expected_native_integral']).max()).max())==row['matched_native_integral_relative']
    assert float(ratio(radial-ref['expected_native_outgoing'],abs(ref['expected_native_outgoing']).max()).max())==row['matched_native_outgoing_relative']
    assert float(p['native_half_weight'])==float(g['native_half_weight'])>0
    return dict(cell=cell_error,global_balance=global_error,primitive=primitive,witness=witness_error,arrays=len(p)+len(ref))


def main(root,a):
    start=time.monotonic();counts={};plan=json.loads((a/'plan.json').read_text())
    for name,base in [('protected_inputs_before.json',root),('source_inputs.json',root),('initial_inputs.json',a),('copied_inputs.json',a),('verification_inputs.json',a)]:
        data=json.loads((a/name).read_text())
        for p,h in data.items():assert digest(base/p)==h,(name,p)
        counts[name]=len(data)
    prior=json.loads((a/'prior_artifacts.json').read_text());entries=0
    for name,h in prior.items():
        folder=root/'validation/artifacts'/name;assert digest(folder/'result.sha256')==h
        for line in (folder/'result.sha256').read_text().splitlines():
            expected,p=line.split(maxsplit=1);assert digest(folder/p)==expected,(name,p);entries+=1
    counts.update(prior_artifacts=len(prior),prior_manifest_entries=entries,selected_native_paths_audited=audit_native_inputs(a))
    for p in (a/'build').glob('*.py'):assert digest(p)==digest(root/'validation/iterative'/p.name),p.name
    for name,n in [('test_native_oblique_track_pilot',12),('test_oblique_strip_geometry',8),('test_axial_cell_characteristic',11)]:
        for p in [a/'runs'/('source_'+name+'.py.log'),a/'runs'/(name+'.log'),a/'replay/runs'/(name+'.log')]:
            log=p.read_text();assert f'Ran {n} tests' in log and '\nOK\n' in log
    arrays=0;geometries=0;files=0;rows=[];maxima=dict(cell=0.,global_balance=0.,primitive=0.,witness=0.);resources=[];reflections_count=0
    for case in plan['process_cases']:
        pid=case['id'];folder=a/'analysis'/pid;data=read(a/f'inputs/track_{case["track"]}.npz')
        receipt=json.loads((a/'replay/receipts'/(pid+'.json')).read_text());assert receipt['all_files_byte_identical']
        assert sorted(receipt['files'])==sorted(p.name for p in folder.iterdir() if p.is_file())
        for name,expected in receipt['files'].items():
            assert digest(folder/name)==expected['sha256'] and (folder/name).stat().st_size==expected['bytes'];files+=1
        assert sorted(p.name for p in (a/'replay/analysis'/pid).iterdir())==['result.json']
        assert digest(folder/'result.json')==digest(a/'replay/analysis'/pid/'result.json')
        result=json.loads((folder/'result.json').read_text());cache={}
        for p in folder.glob('geometry_*.npz'):
            g=unpack_geometry(read(p));geometry_audit(g);cache[p.name]=g;geometries+=1;arrays+=len(g)
            widths=data['planar_widths']*data['zmu'][case['polar']]
            if int(g['layout'])==1:widths=widths[::-1]
            np.testing.assert_array_equal(g['original_widths'],widths)
            assert float(g['native_half_weight'])==float(data['half_weight'][case['polar']])
            assert float(g['native_mx'])==float(data['mx'][case['polar']])
        for row in result['rows']:
            layout,sign,o,order,group=[row[k] for k in ['layout','sign','orientation','order','group']]
            g=cache[f'geometry_l{layout}_m{sign}_o{o}_q{order}.npz'];p=read(folder/(row['label']+'.npz'));ref=read(folder/(row['label']+'_reference.npz'))
            gi=list(data['groups']).index(group);total=data['group_totals'][gi,g['regions']]
            oi=0 if int(g['effective_orientation'])==1 else 1
            np.testing.assert_array_equal(ref['expected_native_integral'],data['exact_track_integral'][gi,oi,case['polar']])
            np.testing.assert_array_equal(ref['expected_native_outgoing'],data['exact_track_outgoing'][gi,oi,case['polar']])
            stats=raw_audit(g,p,ref,total,row);arrays+=stats.pop('arrays')
            for key,value in stats.items():maxima[key]=max(maxima[key],value)
            assert row['all_order_gates_passed'] and row['integrated_gates_passed'] is not False;rows.append(row)
        for item in result['reflections']:
            row=next(r for r in result['rows'] if r['label']==item['label']);layout,sign,o,order,group=[row[k] for k in ['layout','sign','orientation','order','group']]
            g=cache[f'geometry_l{layout}_m{sign}_o{o}_q{order}.npz'];f=unpack_responses(g,read(folder/(row['label']+'.npz')))
            lr,sr,orr=(layout,1,o) if item['axis']=='z' else (0,sign,-o)
            gr=cache[f'geometry_l{lr}_m{sr}_o{orr}_q{order}.npz'];fr=unpack_responses(gr,read(folder/(label(lr,sr,orr,order,group)+'.npz')))
            error=reflections(f,fr,int(g['nr']),int(g['nz']),item['axis']);assert error==item['relative']<5e-12;reflections_count+=1
        assert result['selected_track_pilot_qualified'] and not result['whole_native_geometry_qualified']
        for run in [a/'runs',a/'replay/runs']:
            usage=json.loads((run/(pid+'_resources.json')).read_text());watch=json.loads((run/(pid+'_watchdog.json')).read_text())
            assert usage['peak_rss_mib']<=512 and usage['elapsed_seconds']<=600
            assert watch['returncode']==0 and watch['limit_failure'] is None and watch['free_bytes_after']>=1024**3
            resources.append(usage)
    assert digest(a/'analysis/result.json')==digest(a/'replay/analysis/result.json');files+=1
    summary=json.loads((a/'analysis/result.json').read_text());assert summary['selected_track_pilot_qualified']
    assert len(rows)==summary['response_configurations']==16896
    for order,metrics in summary['order_maxima'].items():
        for key,witness in metrics.items():assert witness['value']==max(r[key] for r in rows if r['order']==int(order))
    assert sum(r['source_units'] for r in rows)==summary['source_unit_evaluations']
    counts.update(byte_identical_replayed_files=files,replay_receipts=len(plan['process_cases']),geometry_files_audited=geometries,
        numeric_arrays_audited=arrays,response_configurations=len(rows),source_unit_evaluations=summary['source_unit_evaluations'],
        total_input_evaluations=summary['total_input_evaluations'],reflection_comparisons=reflections_count,
        independent_raw_maxima=maxima,source_tests=31,archived_tests=31,replay_tests=31,
        peak_numerical_rss_mib=max(v['peak_rss_mib'] for v in resources),maximum_numerical_process_seconds=max(v['elapsed_seconds'] for v in resources),
        verification_elapsed_seconds=time.monotonic()-start,verification_peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2,
        all_verification_checks_passed=True,selected_track_pilot_qualified=True,whole_native_geometry_qualified=False,
        native_axial_white_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

"""Audit archived coordinates, unmodified inputs, raw ledgers and full replay."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from qualify_oblique_strip_geometry import read,diagnostics,reflection_error,label


def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def ratio(d,s):
    d,s=np.broadcast_arrays(abs(d),s)
    assert not np.any((s==0)&(d!=0))
    return np.divide(d,s,out=np.zeros_like(d),where=s>0)


def check_geometry(g):
    assert all(np.isfinite(v).all() for v in g.values())
    nr,nz=int(g['nr']),int(g['nz']);mu=float(g['mu']);o=int(g['orientation'])
    ray=g['ray'];cell=g['cell'];w=g['weight'][ray];mid=(g['s0']+g['s1'])/2
    assert np.all(g['weight']>0) and np.all(g['length']>0)
    np.testing.assert_array_equal(g['length'],g['s1']-g['s0'])
    x=mid if o==1 else float(g['S'])-mid;z=g['u'][ray]+mu*mid
    i=np.searchsorted(g['x'],x,side='right')-1;j=np.searchsorted(g['z'],z,side='right')-1
    np.testing.assert_array_equal(cell,i*nz+j)
    np.testing.assert_array_equal(g['volume'],np.bincount(cell,weights=w*g['length'],minlength=nr*nz))
    # Independent per-ray continuity and physical entry/exit checks.
    first=np.r_[True,np.diff(ray)!=0];last=np.r_[np.diff(ray)!=0,True]
    np.testing.assert_array_equal(g['s0'][~first],g['s1'][~last])
    np.testing.assert_array_equal(g['entry_s'],g['s0'][first])
    np.testing.assert_array_equal(g['entry_cell'],cell[first])
    np.testing.assert_array_equal(g['entry_side'],g['in_side'][first])
    np.testing.assert_array_equal(g['in_side'][~first],g['out_side'][~last]^1)
    for endpoint,side in [(g['s0'][first],g['in_side'][first]),(g['s1'][last],g['out_side'][last])]:
        xp=endpoint if o==1 else float(g['S'])-endpoint;zp=g['u']+mu*endpoint
        dist=np.choose(side,[xp,xp-float(g['S']),zp,zp-float(g['H'])])
        assert np.max(abs(dist))<5e-12*max(float(g['S']),float(g['H']))


def main(root,a):
    counts={};plan=json.loads((a/'plan.json').read_text())
    for name,base in [('protected_inputs_before.json',root),('initial_inputs.json',a),('copied_inputs.json',a),('verification_inputs.json',a)]:
        data=json.loads((a/name).read_text())
        for p,h in data.items():assert digest(base/p)==h,(name,p)
        counts[name]=len(data)
    prior=json.loads((a/'prior_artifacts.json').read_text());entries=0
    for name,h in prior.items():
        folder=root/'validation/artifacts'/name;assert digest(folder/'result.sha256')==h,name
        for line in (folder/'result.sha256').read_text().splitlines():
            expected,p=line.split(maxsplit=1);assert digest(folder/p)==expected,(name,p);entries+=1
    counts.update(prior_artifacts=len(prior),prior_manifest_entries=entries)
    for p in (a/'build').glob('*.py'):assert digest(p)==digest(root/'validation/iterative'/p.name),p.name
    for where in [a/'runs',a/'replay/runs']:
        for name,n in [('tests.log',8),('reference_tests.log',11)]:
            log=(where/name).read_text();assert f'Ran {n} tests' in log and '\nOK\n' in log
    for name,n in [('source_test_oblique_strip_geometry.py.log',8),('source_test_axial_cell_characteristic.py.log',11)]:
        log=(a/'runs'/name).read_text();assert f'Ran {n} tests' in log and '\nOK\n' in log
    files=sorted(p.relative_to(a/'analysis') for p in (a/'analysis').rglob('*') if p.is_file())
    assert files==sorted(p.relative_to(a/'replay/analysis') for p in (a/'replay/analysis').rglob('*') if p.is_file())
    for p in files:assert digest(a/'analysis'/p)==digest(a/'replay/analysis'/p),p
    counts['byte_identical_analysis_files']=len(files)
    arrays=0;geometries=0;rows=[];reflections=[];max_cell=0.;max_global=0.;max_primitive=0.;resources=[]
    for case in plan['process_cases']:
        folder=a/'analysis'/case['id'];saved=json.loads((folder/'result.json').read_text());cache={}
        for p in folder.glob('geometry_*.npz'):
            g=read(p);check_geometry(g);geometries+=1;arrays+=len(g);cache[p.name]=g
        for p in folder.glob('reference_*.npz'):
            ref=read(p);arrays+=len(ref)
            assert all(np.isfinite(v).all() and np.min(v)>=0 for v in ref.values())
        for row in saved['rows']:
            sign,o,order,pi=[row[k] for k in ['sign','orientation','order','profile']];profile=plan['material_profiles'][pi]
            nr,nz=len(profile),case['nz'];n=nr*nz
            g=cache[f'geometry_m{sign}_o{o}_q{order}_r{nr}.npz'];f=read(folder/(row['label']+'.npz'))
            ref=read(folder/f'reference_m{sign}_o{o}_p{pi}.npz');arrays+=len(f)
            assert all(np.isfinite(v).all() for v in f.values())
            u=int(f['units']);assert u==n+nz+(nr if sign else 0)
            np.testing.assert_array_equal(f['q'][:,:n],np.eye(n));assert not f['q'][:,n:u].any()
            np.testing.assert_array_equal(f['total'],np.repeat(profile,nz))
            expected=np.zeros((len(g['u']),u));radial=g['entry_side']<2
            columns=np.where(radial,n+g['entry_cell']%nz,n+nz+g['entry_cell']//nz)
            expected[np.arange(len(expected)),columns]=1
            np.testing.assert_array_equal(f['incoming'][:,:u],expected)
            np.testing.assert_array_equal(f['q'][:,u],f['total']);assert np.all(f['q'][:,u+1]==1)
            np.testing.assert_array_equal(f['q'][:,u+2],np.repeat([1.] if nr==1 else [1.,.3],nz))
            np.testing.assert_array_equal(f['q'][:,u+3],np.tile(np.arange(nz)%2,nr))
            assert np.all(f['incoming'][:,u]==1) and not f['incoming'][:,[u+1,u+3]].any()
            for k in ['integral','face_in','face_out','incoming','exit_angle','q','minimum_piece_angle','minimum_piece_integral','T','B','D']:
                assert np.min(f[k])>=0,(row['label'],k)
            np.testing.assert_array_equal(f['cell_birth'],g['area'][:,None]*f['q'])
            # Reconstruct ledgers from physical input and accumulated fields,
            # independently of the saved defect/scale and reported gates.
            residual=g['area'][:,None]*f['q']+f['face_in'].sum(axis=1)-f['face_out'].sum(axis=1)-f['total'][:,None]*f['integral']
            np.testing.assert_array_equal(residual,f['cell_defect'])
            np.testing.assert_array_equal(f['cell_scale'],f['cell_birth']+f['face_in'].sum(axis=1))
            max_cell=max(max_cell,float(ratio(residual,f['cell_scale']).max()))
            fi=f['face_in'].reshape(nr,nz,4,-1);fo=f['face_out'].reshape(nr,nz,4,-1)
            if o==1:np.testing.assert_array_equal(fo[:-1,:,1],fi[1:,:,0])
            else:np.testing.assert_array_equal(fo[1:,:,0],fi[:-1,:,1])
            if sign>=0:np.testing.assert_array_equal(fo[:,:-1,3],fi[:,1:,2])
            else:np.testing.assert_array_equal(fo[:,1:,2],fi[:,:-1,3])
            incoming=sum(v.sum(axis=0) for v in [fi[0,:,0],fi[-1,:,1],fi[:,0,2],fi[:,-1,3]])
            outgoing=sum(v.sum(axis=0) for v in [fo[0,:,0],fo[-1,:,1],fo[:,0,2],fo[:,-1,3]])
            birth=(g['area'][:,None]*f['q']).sum(axis=0)
            collision=(f['total'][:,None]*f['integral']).sum(axis=0)
            max_global=max(max_global,float(ratio(birth+incoming-outgoing-collision,birth+incoming).max()))
            primitive=float(ratio(f['worst_piece_signed_defect'],f['worst_piece_scale']).max())
            assert primitive==float(f['maximum_piece_relative'].max());max_primitive=max(max_primitive,primitive)
            values=diagnostics(g,f,ref,plan['limits'])
            for k,v in values.items():assert row[k]==v,(case['id'],row['label'],k)
            assert row['all_order_gates_passed'] and row['integrated_gates_passed'] is not False
            rows.append(row)
        for reflection in saved['reflections']:
            row=next(r for r in saved['rows'] if r['label']==reflection['label']);sign,o,order,pi=[row[k] for k in ['sign','orientation','order','profile']]
            nr=len(plan['material_profiles'][pi]);f=read(folder/(row['label']+'.npz'))
            if reflection['axis']=='z':ref=read(folder/(label(1,o,order,pi)+'.npz'))
            else:
                reverse=plan['material_profiles'].index(plan['material_profiles'][pi][::-1]);ref=read(folder/(label(sign,1,order,reverse)+'.npz'))
            e=reflection_error(f,ref,nr,case['nz'],sign*plan['mu_magnitude'],reflection['axis'])
            assert e==reflection['relative'];reflections.append(e)
        assert saved['prototype_qualified'] and not saved['native_bridge_qualified'] and not saved['coupled_eigenreference_qualified']
        for path in [a/'runs',a/'replay/runs']:
            usage=json.loads((path/(case['id']+'_resources.json')).read_text())
            watchdog=json.loads((path/(case['id']+'_watchdog.json')).read_text())
            assert usage['elapsed_seconds']<=600 and usage['peak_rss_mib']<=512
            assert watchdog['returncode']==0 and watchdog['limit_failure'] is None
            resources.append(usage)
    assert max_cell<1e-10 and max_global<1e-10 and max_primitive<1e-10 and max(reflections)<5e-12
    summary=json.loads((a/'analysis/result.json').read_text())
    assert summary['prototype_qualified'] and not summary['failed_all_order_rows'] and not summary['failed_integrated_rows']
    assert len(rows)==summary['material_direction_order_cases']==5760
    assert sum(r['source_units'] for r in rows)==summary['source_unit_evaluations']==101632
    for order,metrics in summary['order_maxima'].items():
        for key,witness in metrics.items():assert witness['value']==max(r[key] for r in rows if r['order']==int(order) and key in r)
    counts.update(geometry_files_checked=geometries,numeric_arrays_checked=arrays,material_direction_order_cases=len(rows),
        source_unit_evaluations=summary['source_unit_evaluations'],total_input_evaluations=summary['total_input_evaluations'],
        reflection_comparisons=len(reflections),independent_cell_balance_relative=max_cell,
        independent_global_balance_relative=max_global,primitive_balance_relative=max_primitive,
        source_tests=19,archived_tests=19,replay_tests=19,peak_rss_mib=max(u['peak_rss_mib'] for u in resources),
        maximum_process_seconds=max(u['elapsed_seconds'] for u in resources),all_verification_checks_passed=True,
        prototype_qualified=True,native_bridge_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)

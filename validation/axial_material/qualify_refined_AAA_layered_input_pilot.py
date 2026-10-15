"""Bounded current-data interface pilot for the sealed finite-height kernel.

The old physical operator cannot be reused: its cross sections differ. Match
every current ray against the old geometric inventory, then use current totals
in fresh physical-source flights on a preselected 16-record sample. This does
not qualify the full inventory, a zero-gradient inverse propagation rule,
scattering/fission, white closure, or coupled AAA/ABA accuracy.
"""
import argparse
import json
from pathlib import Path
import shutil
import struct
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'validation/axial_material'))
import measure_refined_AAA_native_angular_response as measured
from probe_refined_AAA_white_odd_response import (
    ART, GROUPS, DiskResources, SerialExecutor, digest, read, write_new, verify, require_file,
)
sys.path.insert(0,str(ROOT/'validation/iterative'))
from native_layered_cached import transport, checks
from native_layered_reference import RectangleReference, packed
from native_layered_cached import aggregate
from native_oblique_streaming import ratio

OLD=ART/'native-layered-full-20261001'
ANGULAR=measured.OUT
OUT=ART/'axial-material-AAA-white-trace-refined-layered-input-pilot-20261005'
ANGULAR_SEAL='8862154f1fb3458676460f8a4074a1a52070322332dd08e66c2773b0e4345540'
OLD_SEAL='6ab0927cb9570715607c260873e907d6b6a429327773909ceb4b2e4f0af3ac2d'
TRACKS=[i*11363//15 for i in range(16)]
H,NZ=20.,4


def verify_angular():
    require_file(ANGULAR/'seal.json',ANGULAR_SEAL)
    verify({str(ANGULAR/n):h for n,h in read(ANGULAR/'seal.json')['files'].items()})
    verify(read(ANGULAR/'declaration.json')['files'])
    measured.verify_previous()


def geometry():
    """Validate all original geometric records, including unused record bytes."""
    import numpy as np
    with np.load(OLD/'inputs/inventory.npz') as z:
        d={n:z[n].copy() for n in z.files}
    with (ANGULAR/'inputs/rays.bin').open('rb') as f:
        def record():
            raw=f.read(4)
            if len(raw)!=4:raise ValueError('missing ray record')
            n=struct.unpack('<i',raw)[0];body=f.read(n)
            if len(body)!=n or f.read(4)!=raw:raise ValueError('bad ray record')
            return body
        magic,ncom,ntr,fmt=struct.unpack('<4siii',record())
        if magic!=b'$TRK' or (ncom,ntr,fmt)!=(5,11364,1):raise ValueError('current original-ray layout required')
        for i in range(ncom):record()
        st=np.frombuffer(record(),'<i4')
        if st.tolist()!=[2,0,8,6,6,1,96,1,17]:raise ValueError('current track dimensions differ')
        for i in range(6):record()
        for track in range(ntr):
            raw=record();nsub,nseg=struct.unpack_from('<ii',raw)
            wei=struct.unpack_from('<d',raw,8)[0];angle=struct.unpack_from('<i',raw,16)[0]
            if nsub!=1 or nseg<3 or nseg>17 or len(raw)!=20+12*nseg+32:
                raise ValueError('full current ray bytes/layout differ')
            nom=np.frombuffer(raw,'<i4',nseg,20)
            h2=np.frombuffer(raw,'<f8',nseg,20+4*nseg)
            if (nseg!=d['nseg'][track] or wei!=d['wei'][track] or angle-1!=d['angle'][track]
                    or nom.tobytes()!=d['nom'][track,:nseg].astype('<i4').tobytes()
                    or h2.tobytes()!=d['h2'][track,:nseg].astype('<f8').tobytes()
                    or np.any(d['nom'][track,nseg:]!=0) or np.any(d['h2'][track,nseg:]!=0)
                    or h2[1:-1].tobytes()!=d['planar_widths'][track,:nseg-2].tobytes()
                    or np.any(d['planar_widths'][track,nseg-2:]!=0)
                    or -nom[0]-1!=d['entry_surface'][track] or -nom[-1]-1!=d['exit_surface'][track]):
                raise ValueError('geometric record differs at original index '+str(track))
            # Read the format-1 four integer and two double tags; neither is
            # used as a fitted geometry input by this extrusion kernel.
            tags=struct.unpack_from('<4i2d',raw,20+12*nseg)
            if not np.isfinite(tags).all():raise ValueError('invalid format-1 tags')
        if f.read(1):raise ValueError('extra original ray bytes')
    current=measured.previous.data()
    for key,value in [('weights',current['vol']),('zmu',current['z']),('wzmu',current['wz'])]:
        if not np.array_equal(d[key],value):raise ValueError('geometric normalization or polar rule differs')
    if (not np.array_equal(d['original_track'],np.arange(11364))
            or not np.array_equal(d['original_record_multiplicity'],np.ones(11364,dtype='u1'))
            or d['groups'].tolist()!=GROUPS):raise ValueError('original record/group identity differs')
    old_totals=d['group_totals'].copy()
    d['group_totals']=np.array([current['totals'][g] for g in GROUPS])
    return d,dict(all_11364_geometric_records_byte_exact=True,all_format1_record_bytes_consumed=True,
        current_totals_used=True,old_totals_reused=False,
        maximum_total_difference_by_group=[float(np.max(abs(a-b))) for a,b in zip(d['group_totals'],old_totals,strict=True)])


def prepare():
    import numpy as np
    import scipy
    verify_angular();require_file(OLD/'result.sha256',OLD_SEAL)
    manifest={n.lstrip('*'):h for h,n in (line.split(None,1) for line in (OLD/'result.sha256').read_text().splitlines())}
    selected=['build/cached.dylib','build/native_layered_cached.cpp','build/native_layered_geometry.hpp',
        'build/native_oblique_geometry_core.hpp','inputs/inventory.npz','verification/result.json','plan.json']
    verify({str(OLD/n):manifest[n] for n in selected})
    v=read(OLD/'verification/result.json')
    if not v['full_native_physical_operator_qualified'] or not v['full_native_white_qualified']:
        raise ValueError('sealed prior kernel qualification required')
    d,admission=geometry()
    OUT.mkdir(exist_ok=False)
    for n in ['runtime','inputs','AAA']:(OUT/n).mkdir()
    shutil.copy2(OLD/'build/cached.dylib',OUT/'runtime/cached.dylib')
    shutil.copy2(ANGULAR/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py')
    with (OUT/'inputs/current_inventory.npz').open('xb') as handle:np.savez_compressed(handle,**d)
    write_new(OUT/'input_identity.json',admission)
    longest=max(TRACKS,key=lambda i:int(d['nseg'][i]))
    audits=[dict(track=TRACKS[0],group=51,polar=0,orientation=1,sign=1),
            dict(track=longest,group=98,polar=3,orientation=-1,sign=-1)]
    files=dict(read(ANGULAR/'declaration.json')['files'])
    paths=[Path(__file__).resolve(),Path(sys.executable).resolve(),ANGULAR/'seal.json',OLD/'result.sha256',*[OLD/n for n in selected],
           OUT/'runtime/cached.dylib',OUT/'runtime/run_bounded_dragon.py',OUT/'inputs/current_inventory.npz',OUT/'input_identity.json']
    paths += [Path(sys.modules[n].__file__).resolve() for n in ['measure_refined_AAA_native_angular_response',
        'native_layered_cached','native_layered_reference','native_oblique_streaming']]
    paths += [p for p in Path(scipy.__file__).parent.rglob('*') if p.is_file() and p.suffix in ['.py','.so','.dylib']]
    paths += [p for p in Path(np.__file__).parent.rglob('*') if p.is_file() and p.suffix in ['.py','.so','.dylib']]
    files.update({str(p.resolve()):digest(p) for p in paths});verify(files)
    roots=sorted(set(read(ANGULAR/'declaration.json')['resource_roots'])|{str(OUT)})
    resource=DiskResources(ART,roots,8*2**30,96*2**30)
    write_new(OUT/'declaration.json',dict(schema='AXMAT_CURRENT_LAYERED_INPUT_PILOT_V1',files=files,
        resource_roots=roots,min_free_bytes=8*2**30,artifact_budget_bytes=96*2**30,resources_before=resource.check(),
        total_wall_seconds=300,worker_wall_seconds=120,audit_wall_seconds=120,
        threads=1,numeric_children_at_once=1,retries=0,
        numeric_environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
        original_record_sample=TRACKS,record_selection='16 equally spaced original inventory indices including both endpoints; no outcome selection.',
        height=H,axial_cells=NZ,groups=GROUPS,polars=[0,1,2,3],orientations=[1,-1],axial_signs=[-1,1],
        worker_orders=[16,32],independent_audits=audits,independent_orders=[64,96],
        kernel='Byte-exact sealed exact-exponential finite-height physical-source kernel. '
               'No matched reference inflow, tabulated-native/PJJ completion or fitted normalizer.',
        raw_physical_balance_relative_limit=1e-10,geometry_and_action_relative_limit=5e-12,
        independent_reference_order_relative_limit=2e-13,
        decision='Current-data interface and selected whole-field pilots only. '
                 'No full-inventory or common-white closure qualification and no inverse propagation rule. '
                 'If every check passes, prepare a separately declared full-inventory current-data response.',
        original_physical_inputs_changed=False,production_solver_changed=False,CE_data_used=False,
        physical_accuracy_qualified=False,axial_model_qualified=False,ABA_admitted=False))
    print(json.dumps(dict(declaration_sha256=digest(OUT/'declaration.json'))))


def load():
    import numpy as np
    with np.load(OUT/'inputs/current_inventory.npz') as z:return {n:z[n].copy() for n in z.files}


def ray(d,track,polar,orientation,sign):
    import numpy as np
    n=int(d['nseg'][track]-2)
    return (d['planar_widths'][track,:n]*d['zmu'][polar],d['nom'][track,1:n+1]-1,
        int(d['entry_surface'][track] if orientation==1 else d['exit_surface'][track]),
        int(d['exit_surface'][track] if orientation==1 else d['entry_surface'][track]),
        float(sign*np.sqrt(1-1/d['zmu'][polar]**2)))


def worker():
    import numpy as np
    d=load();declaration=read(OUT/'declaration.json');rows=[];fields={}
    for track in TRACKS:
        for polar in range(4):
            for orientation in [1,-1]:
                for sign in [-1,1]:
                    w,r,entry,exit_surface,mu=ray(d,track,polar,orientation,sign)
                    for gi,g in enumerate(GROUPS):
                        sigma=d['group_totals'][gi];low=None
                        for order in [16,32]:
                            f=transport(OUT/'runtime/cached.dylib',w,r,sigma,entry,H,NZ,mu,orientation,order)
                            check=checks(f,w,r,sigma,H,NZ,mu)
                            if not check['passed']:raise ValueError('original physical coordinate checks failed')
                            if low is None:low=f['fields'].copy()
                            else:
                                error=float(ratio(f['fields']-low,abs(f['fields']).max(axis=(0,1))).max())
                                if error>5e-12:raise ValueError('original offset-order convergence gate failed')
                                label=f't{track}_p{polar}_o{orientation}_s{sign}_g{g}'
                                rows.append(dict(label=label,order_relative=error,**check))
                                if any(a==dict(track=track,group=g,polar=polar,orientation=orientation,sign=sign) for a in declaration['independent_audits']):
                                    fields[label]=f['fields'];fields[label+'_response']=packed(aggregate(f['fields'],r,NZ,orientation,exit_surface))
    with (OUT/'pilot_fields.npz').open('xb') as handle:np.savez_compressed(handle,**fields)
    write_new(OUT/'pilot_checks.json',dict(records=TRACKS,states_per_order=len(rows),offset_orders=[16,32],
        physical_coordinate_cases_per_state=14*NZ+10,rows=rows,all_checks_passed=True))
    print('AXMAT-CURRENT-LAYERED-PILOT-PASSED')


def audit():
    import numpy as np
    d=load();declaration=read(OUT/'declaration.json');rows=[];references={}
    with np.load(OUT/'pilot_fields.npz') as z:saved={n:z[n].copy() for n in z.files}
    for a in declaration['independent_audits']:
        w,r,entry,exit_surface,mu=ray(d,a['track'],a['polar'],a['orientation'],a['sign'])
        sigma=d['group_totals'][GROUPS.index(a['group'])]
        f=transport(OUT/'runtime/cached.dylib',w,r,sigma,entry,H,NZ,mu,a['orientation'],32)
        label=f"t{a['track']}_p{a['polar']}_o{a['orientation']}_s{a['sign']}_g{a['group']}"
        if not np.array_equal(f['fields'],saved[label]):raise ValueError('saved whole-field replay differs')
        ref=RectangleReference(w,r,sigma,entry,exit_surface,H,NZ,mu,a['orientation'],f['q'],f['radial_input'],f['axial_input'])
        low=ref.fixed(64,full=True);high=ref.fixed(96,full=True)
        scale=abs(high).max(axis=(0,1))
        convergence=float(ratio(low-high,scale).max());error=float(ratio(saved[label]-high,scale).max())
        if convergence>2e-13 or error>5e-12:raise ValueError('independent rectangle whole-field gate failed')
        rows.append(dict(**a,reference_64_96_relative=convergence,independent_full_field_relative=error,
                         saved_full_field_replay_byte_exact=True))
        references[label+'_64']=low;references[label+'_96']=high
    with (OUT/'independent_fields.npz').open('xb') as handle:np.savez_compressed(handle,**references)
    write_new(OUT/'result.json',dict(classification='COMPLETE_CURRENT_DATA_FINITE_HEIGHT_INPUT_PILOT_ONLY',
        geometric_identity=read(OUT/'input_identity.json'),original_records_sampled=16,all_original_tracks=11364,
        worker_states=16*4*2*2*3*2,independent_audits=rows,all_selected_physical_checks_passed=True,
        full_inventory_qualified=False,common_white_return_qualified=False,
        local_inverse_propagation_qualified=False,scattering_fission_iteration_qualified=False,
        AAA_accuracy_qualified=False,ABA_admitted=False))
    checks_result=read(OUT/'pilot_checks.json')
    with (OUT/'REPORT.txt').open('x') as handle:
        handle.write('AAA 当前数据有限高度输入试验（2026-10-05）\n\n')
        handle.write('全部 11,364 条原始径向轨迹的几何记录与原已核验库存逐字节一致。\n')
        handle.write('旧截面与当前截面不一致，旧响应没有复用；新试验使用当前三个预选能群的实际总截面。\n')
        handle.write('16 个预选原始记录，20 cm 高度、4 层，全部原生极点及正负方向；共 1536 个新物理状态。\n')
        handle.write(f"每状态保留完整输入坐标；16/32 阶积分最大整字段变化 {max(r['order_relative'] for r in checks_result['rows']):.3e}。\n")
        for a in rows:handle.write(f"独立矩形参考：群 {a['group']}、原始记录 {a['track']}，整字段差 {a['independent_full_field_relative']:.3e}。\n")
        handle.write('\n完成当前数据接口与所选记录的有限高度试验，尚未完成全轨迹白返回、传播闭合或耦合精度验收。\n')
        handle.write('AAA 原裂变率门槛仍 FAIL；ABA 未准入。下一步须另行声明全库存当前数据响应。\n')
    print('AXMAT-CURRENT-LAYERED-INDEPENDENT-AUDIT-PASSED')


def run(expected):
    declaration=read(require_file(OUT/'declaration.json',expected));verify(declaration['files']);verify_angular()
    resource=DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    write_new(OUT/'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    started=time.monotonic();runner=SerialExecutor(OUT,declaration['total_wall_seconds'],'AAA',resource)
    result=dict(classification='FAILED_CURRENT_LAYERED_INPUT_PILOT_NO_RETRY',error=None)
    try:
        runner.execute(OUT,'pilot',[sys.executable,str(Path(__file__).resolve()),'worker'],120,'AXMAT-CURRENT-LAYERED-PILOT-PASSED')
        runner.execute(OUT,'audit',[sys.executable,str(Path(__file__).resolve()),'audit'],120,'AXMAT-CURRENT-LAYERED-INDEPENDENT-AUDIT-PASSED')
        result.update(classification='COMPLETE_BOUNDED_CURRENT_LAYERED_INPUT_PILOT_ONLY',ABA_admitted=False)
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        verify(declaration['files']);verify_angular()
        result.update(elapsed_seconds=time.monotonic()-started,resources=resource.check())
        write_new(OUT/'driver_result.json',result)
    write_new(OUT/'seal.json',dict(schema='AXMAT_CURRENT_LAYERED_INPUT_PILOT_SEAL_V1',
        files={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file()}))
    print(json.dumps(dict(classification=read(OUT/'result.json')['classification'],elapsed_seconds=result['elapsed_seconds'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','run','worker','audit'])
    parser.add_argument('--sha256');a=parser.parse_args()
    dict(prepare=prepare,run=lambda:run(a.sha256),worker=worker,audit=audit)[a.action]()

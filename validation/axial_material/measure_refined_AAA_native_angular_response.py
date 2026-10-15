"""Measure the complete current-data zero-gradient angular collision response.

All 64 angular/region source coordinates are measured before white return.
Fresh native flights independently check every white source column and six
positive holdouts. Projection is applied only after retaining the full fields.
This is neither an axial propagation law nor a coupled eigenvalue solver.
"""
import argparse
import csv
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'validation/axial_material'))
import probe_refined_AAA_white_odd_response as previous
from probe_refined_AAA_white_odd_response import (
    ART, PROD, FINAL, GROUPS, DiskResources, SerialExecutor, require_file,
    digest, read, write_new, verify, verify_sealed_directory, trace_exchange,
)

OLD = previous.OUT
OUT = ART / 'axial-material-AAA-white-trace-refined-native-angular-response-20261005'
OLD_SEAL = '66fc103662c24d4bceafb653e579da6a12d662baa2436e457628d44a268b4d7c'
NV, NB, NH = 64, 6, 6
PRIMARY, WHITE = NV + NB + NH, NV + NH


def verify_previous():
    require_file(OLD / 'seal.json', OLD_SEAL)
    verify({str(OLD / n):h for n,h in read(OLD / 'seal.json')['files'].items()})
    verify(read(OLD / 'declaration.json')['files'])
    if read(OLD / 'result.json')['classification'] != 'COMPLETE_SAME_DATA_ZERO_GRADIENT_NATIVE_ODD_RESPONSE_ONLY':
        raise ValueError('complete current-data native diagnostic required')
    verify_sealed_directory(FINAL)


def prepare():
    verify_previous()
    import numpy as np
    OUT.mkdir(exist_ok=False)
    for name in ['runtime', 'inputs', 'AAA']:
        (OUT / name).mkdir()
    for name in ['run_bounded_dragon.py', 'probe_signed']:
        shutil.copy2(OLD / 'runtime' / name, OUT / 'runtime' / name)
    for name in ['track.xsm', 'system.xsm', 'rays.bin']:
        shutil.copy2(OLD / 'inputs' / name, OUT / 'inputs' / name)
    paths = [Path(__file__).resolve(), Path(sys.executable).resolve(),
             Path(previous.__file__).resolve(), OLD / 'seal.json',
             *[OUT / 'runtime' / n for n in ['run_bounded_dragon.py', 'probe_signed']],
             *[OUT / 'inputs' / n for n in ['track.xsm', 'system.xsm', 'rays.bin']]]
    paths += [p for p in Path(np.__file__).parent.rglob('*')
              if p.is_file() and p.suffix in ['.py', '.so', '.dylib']]
    files = dict(read(OLD / 'declaration.json')['files'])
    files.update({str(p.resolve()):digest(p) for p in paths})
    verify(files)
    roots = sorted(set(read(OLD / 'declaration.json')['resource_roots']) | {str(OUT)})
    resource = DiskResources(ART, roots, 8 * 2**30, 96 * 2**30)
    write_new(OUT / 'declaration.json', dict(
        schema='AXMAT_CURRENT_FULL_ANGULAR_RESPONSE_V1', files=files,
        total_wall_seconds=300, stage_caps=dict(prepare=30, primary=120, white_prepare=30, white=120, analysis=60),
        groups=GROUPS, primary_per_group=PRIMARY, white_per_group=WHITE,
        expected_native_flights=3*(PRIMARY+WHITE),
        angular_order='Independent axial sign +,-; four original polar nodes; region 1..8.',
        full_source_coordinates=64, common_boundary_coordinates=6,
        holdouts=['uniform source', 'collision equilibrium with unit boundary',
                  'fixed basis isotropic', 'fixed basis positive odd pair +',
                  'fixed basis positive odd pair -', 'positive mixed region/angle and face source'],
        white='Measure Tbb on six common face amplitudes. Solve (I-Tbb)j=Tbs*q. '
              'Execute fresh native flights for every one of the 64 white volume source columns and all holdouts.',
        projection='Preserve all native angular-region fields first. Use the unchanged fixed rank1 basis, '
                   'native volumes and exact nonunit Gram to construct an 8-by-8 projected source response. '
                   'Retain discarded radial fields for every angular coordinate; no rank selection.',
        comparisons='Compare the declared conditional white trace at the identical native angular grid. '
                    'Report response and discarded-field discrepancies. Any inverse is algebraic zero-gradient '
                    'response only; it supplies no unique axial transport generator.',
        action_relative_limit=5e-12, raw_native_balance_relative_limit=1e-6,
        resource_roots=roots, resources_before=resource.check(),
        min_free_bytes=8*2**30, artifact_budget_bytes=96*2**30,
        threads=1, numeric_children_at_once=1, retries=0,
        physical_inputs_changed=False, original_accuracy_thresholds_changed=False,
        CE_data_used=False, coefficient_fitting=False, axial_propagation_admitted=False,
        scattering_fission_iteration_admitted=False, ABA_admitted=False))
    print(json.dumps(dict(declaration_sha256=digest(OUT / 'declaration.json'))))


def inputs(g, d):
    import numpy as np
    b, sigma = d['basis'][g], d['totals'][g]
    mu = np.array([1., -1.])[:, None] * d['mu'][None, :]
    unit = np.eye(NV).reshape(2, 4, 8, NV)
    boundary = np.zeros((2, 4, 6, NV))
    hold_q = np.stack([
        np.ones((2,4,8)), np.broadcast_to(sigma, (2,4,8)),
        np.broadcast_to(b, (2,4,8)), b[None,None,:]*(1+.5*mu[:,:,None]),
        b[None,None,:]*(1-.5*mu[:,:,None]),
        (1+np.arange(1,9)/8)[None,None,:]*(1+.25*mu[:,:,None]+.1*(3*mu[:,:,None]**2-1)/2),
    ], axis=-1)
    hold_in = np.zeros((2,4,6,NH))
    hold_in[:,:,:,1] = 1.
    hold_in[:,:,:,5] = np.arange(1,7)[None,None,:]/7
    q = np.concatenate([unit, np.zeros((2,4,8,6)), hold_q], axis=-1)
    incoming = np.concatenate([boundary, np.broadcast_to(np.eye(6), (2,4,6,6)), hold_in], axis=-1)
    return q, incoming


def prepare_sources():
    import numpy as np
    d = previous.data()
    for n in ['track.xsm', 'system.xsm', 'rays.bin']:
        if digest(OUT / 'inputs' / n) != digest(OLD / 'inputs' / n):
            raise ValueError('copied native inputs differ')
    records=[]
    for g in GROUPS:
        q, inc = inputs(g,d)
        if q.shape != (2,4,8,PRIMARY) or min(q.min(),inc.min()) < 0:
            raise ValueError('complete positive source coordinate layout required')
        records += [(g, q[...,c], inc[...,c]) for c in range(PRIMARY)]
    previous.sources(OUT / 'inputs/primary.txt', records)
    print('AXMAT-FULL-ANGULAR-SOURCES-READY')


def load_native(path, counts):
    import numpy as np
    f, own, groups, meta = previous.native(path)
    if groups != sum(([g]*counts for g in GROUPS), []):
        raise ValueError('incomplete native group/source coordinates')
    d = previous.data()
    if (meta[:14].tobytes() != d['vol'].astype('<f4').tobytes()
            or meta[18:22].tobytes() != d['z'].astype('<f4').tobytes()
            or meta[22:26].tobytes() != d['wz'].astype('<f4').tobytes()):
        raise ValueError('native response quadrature or normalization differs')
    return (f[:,:,:8] + own).reshape(64,-1), f[:,:,8:].reshape(48,-1)


def relative(actual, expected):
    import numpy as np
    scale = np.max(abs(expected),axis=0)
    if np.any(scale <= 0):
        raise ValueError('positive reference scale required for every coordinate')
    return float(np.max(abs(actual-expected)/scale))


def response_parts(gi, d, fields, outgoing):
    import numpy as np
    block=slice(gi*PRIMARY,(gi+1)*PRIMARY)
    raw, out = fields[:,block], outgoing[:,block]
    summed=out.reshape(2,4,6,PRIMARY).sum(axis=(0,1))
    tq=summed[:,:NV]/d['vol'][8:,None]
    tb=summed[:,NV:NV+NB]/d['vol'][8:,None]
    matrix=np.eye(NB)-tb
    inverse=np.linalg.solve(matrix,np.eye(NB))
    inflow=np.linalg.solve(matrix,tq)
    rho=float(max(abs(np.linalg.eigvals(tb))))
    if rho >= 1 or min(inverse.min(),inflow.min()) < 0:
        raise ValueError('positive subcritical white return required')
    if relative(matrix@inflow,tq) > 5e-12:
        raise ValueError('white solve failed original residual screen')
    return raw, out, tb, inflow, rho


def prepare_white():
    import numpy as np
    d=previous.data();fields,outgoing=load_native(OUT/'inputs/primary.bin',PRIMARY)
    records=[];metadata=[]
    for gi,g in enumerate(GROUPS):
        raw,out,tb,inflow,rho=response_parts(gi,d,fields,outgoing)
        q,inc=inputs(g,d)
        white_q=np.concatenate([q[...,:NV],q[...,NV+NB:]],axis=-1)
        all_q=white_q.reshape(NV,WHITE)
        amplitude=inflow@all_q
        all_inc=np.broadcast_to(amplitude,(2,4,NB,WHITE)).copy()
        records += [(g,white_q[...,c],all_inc[...,c]) for c in range(WHITE)]
        metadata.append(dict(group=g,white_spectral_radius=rho))
        with (OUT/f'inputs/white_prepared_g{g}.npz').open('xb') as handle:
            np.savez_compressed(handle,q=white_q,incoming=all_inc,amplitudes=amplitude)
    previous.sources(OUT/'inputs/white.txt',records)
    write_new(OUT/'white_preparation.json',metadata)
    print('AXMAT-FULL-ANGULAR-WHITE-READY')


def analyze():
    import numpy as np
    d=previous.data();geom=previous.geometric_volumes(d)
    fields,outgoing=load_native(OUT/'inputs/primary.bin',PRIMARY)
    fresh,fresh_out=load_native(OUT/'inputs/white.bin',WHITE)
    native_mu=(np.array([1.,-1.])[:,None]*d['mu'][None,:]).ravel()
    omega=np.tile(d['angular']/2,2)
    normalization=np.repeat(omega,8)*np.tile(d['vol'][:8],8)
    reports=[];offrows=[]
    for gi,g in enumerate(GROUPS):
        raw,out,tb,inflow,rho=response_parts(gi,d,fields,outgoing)
        sw=slice(gi*WHITE,(gi+1)*WHITE)
        actual,actual_out=fresh[:,sw],fresh_out[:,sw]
        with np.load(OUT/f'inputs/white_prepared_g{g}.npz') as z:
            q=z['q'].copy();incoming=z['incoming'].copy();amplitude=z['amplitudes'].copy()
        if min(raw.min(),out.min(),actual.min(),actual_out.min()) < 0:
            raise ValueError('positive native source response became negative')
        vacuum=raw[:,:NV];boundary=raw[:,NV:NV+NB]
        white=vacuum+boundary@inflow
        white_out=out[:,:NV]+out[:,NV:NV+NB]@inflow
        assembly=max(relative(actual,white@q.reshape(NV,WHITE)),
                     relative(actual_out,white_out@q.reshape(NV,WHITE)))
        # Fresh holdouts independently verify all pre-white coordinates too.
        primary_q,primary_in=inputs(g,d)
        qh=primary_q[...,NV+NB:].reshape(NV,NH)
        ih=primary_in[...,NV+NB:][0,0]
        primary_hold=max(relative(raw[:,NV+NB:],vacuum@qh+boundary@ih),
                         relative(out[:,NV+NB:],out[:,:NV]@qh+out[:,NV:NV+NB]@ih))
        actual_integral=actual.reshape(2,4,8,WHITE)
        actual_boundary=actual_out.reshape(2,4,6,WHITE)
        closure=relative(actual_boundary.sum(axis=(0,1)),d['vol'][8:,None]*amplitude)
        birth=np.einsum('zprc,pr->c',q,geom)
        surface=(d['vol'][8:,None]*amplitude).sum(axis=0)
        collision=np.einsum('zprc,r->c',actual_integral,d['totals'][g])
        defect=birth+surface-collision-actual_boundary.sum(axis=(0,1,2))
        balance=float(np.max(abs(defect)/(birth+surface)))
        # Preserve the complete angular mean matrix; no radial redistribution.
        mean_white=white/normalization[:,None]
        lifting=np.kron(np.eye(8),d['basis'][g][:,None])
        gram=0.
        for weight,value in zip(d['weights'],d['basis'][g],strict=True):
            gram+=float(weight)*float(value)*float(value)
        testing=np.kron(np.eye(8),(d['weights']*d['basis'][g]/gram)[None,:])
        reduced=testing@mean_white@lifting
        projected_fields=mean_white@lifting
        discarded=projected_fields-lifting@reduced
        norm_weight=np.repeat(omega,8)*np.tile(d['weights'],8)
        norms=np.sqrt(np.einsum('rc,r,rc->c',discarded,norm_weight,discarded)
                      /np.einsum('rc,r,rc->c',projected_fields,norm_weight,projected_fields))
        for state,value in enumerate(norms):
            offrows.append(dict(group=g,angular_source_state=state+1,axial_mu=float(native_mu[state]),
                                weighted_full_field_offspace_relative=float(value)))
        inverse=np.linalg.solve(reduced,np.eye(8))
        inverse_error=float(np.max(abs(inverse@reduced-np.eye(8))))
        swap=np.r_[np.arange(4,8),np.arange(4)]
        parity=float(np.max(abs(reduced-reduced[swap][:,swap]))/np.max(abs(reduced)))
        tau=0.
        for weight,value,total in zip(d['weights'],d['basis'][g],d['totals'][g],strict=True):
            tau+=float(weight)*float(value)*float(value)*float(total)
        trace=trace_exchange(native_mu,2*omega,6*.61776479,float(sum(d['vol'][:8])))
        conditional=np.linalg.solve(tau*np.eye(8)+d['basis'][g][0]**2*trace,gram*np.eye(8))
        h=np.stack([np.ones(8),1+.5*native_mu,1-.5*native_mu,
                    1+.25*native_mu+.1*(3*native_mu**2-1)/2,native_mu],axis=1)
        compare=reduced@h;old=conditional@h
        response_error=relative(old,compare)
        odd_native=float(gram*np.dot(omega*native_mu,reduced@native_mu))
        old_odd=next(r for r in read(OLD/'result.json')['comparisons'] if r['group']==g)['projected_native_white_odd_current']
        odd_error=abs(odd_native-old_odd)/abs(old_odd)
        offdiagonal=inverse.copy();np.fill_diagonal(offdiagonal,0)
        if max(assembly,primary_hold,closure,parity,inverse_error,odd_error)>5e-12 or balance>1e-6:
            raise ValueError('original native action/parity/white/balance screen failed')
        with (OUT/f'angular_response_g{g}.npz').open('xb') as handle:
            np.savez_compressed(handle,vacuum_integrals=vacuum,boundary_integrals=boundary,
                white_integrals=white,white_outgoing=white_out,white_amplitudes=inflow,
                white_angular_means=mean_white,source_lifting=lifting,testing=testing,gram=gram,
                projected_response=reduced,projected_inverse=inverse,
                projected_source_full_fields=projected_fields,discarded_fields=discarded,
                conditional_response=conditional,native_mu=native_mu,omega=omega,
                source_holdouts=h,actual_fresh_white_integrals=actual,
                actual_fresh_white_outgoing=actual_out,raw_balance_defect=defect,
                raw_balance_scale=birth+surface)
        reports.append(dict(group=g,white_spectral_radius=rho,
            all_64_white_columns_and_6_holdouts_native_action_relative=assembly,
            vacuum_positive_holdout_action_relative=primary_hold,
            white_closure_relative=closure,raw_native_balance_relative=balance,
            signed_angular_parity_relative=parity,projected_inverse_algebra_relative=inverse_error,
            prior_odd_response_relative=odd_error,complete_response_minimum=float(mean_white.min()),
            projected_response_minimum=float(reduced.min()),
            projected_inverse_largest_offdiagonal=float(offdiagonal.max()),
            projected_inverse_minimum_row_sum=float(inverse.sum(axis=1).min()),
            projected_inverse_condition_number=float(np.linalg.cond(reduced)),
            angular_source_offspace_min=float(norms.min()),angular_source_offspace_max=float(norms.max()),
            conditional_five_source_response_relative=response_error,
            conditional_odd_current_signed_relative=float(gram*np.dot(omega*native_mu,conditional@native_mu)/odd_native-1)))
    with (OUT/'angular_source_offspace.csv').open('x') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(offrows[0]));writer.writeheader();writer.writerows(offrows)
    write_new(OUT/'result.json',dict(
        classification='COMPLETE_CURRENT_DATA_FULL_ANGULAR_COLLISION_RESPONSE_ONLY',
        groups=reports,actual_native_flights=3*(PRIMARY+WHITE),full_coordinates_per_group=NV,
        fresh_white_coordinates_per_group=WHITE,all_original_tracks=11364,
        complete_angular_region_fields_retained=True,projection_after_full_response=True,
        CE_data_used=False,source_or_operator_fitted=False,physical_accuracy_qualified=False,
        axial_propagation_qualified=False,scattering_fission_iteration_qualified=False,ABA_admitted=False))
    with (OUT/'REPORT.txt').open('x') as handle:
        handle.write('AAA 同数据完整角向碰撞响应（2026-10-05）\n\n')
        handle.write(f'三个预选能群，全部 64 个区域/角向源坐标、6 个公共边界坐标；实际 {3*(PRIMARY+WHITE)} 次原生飞行。\n')
        handle.write('每个白返回坐标及六个正源用新原生飞行独立验证；完整字段先保留，再投影。\n')
        for row in reports:
            handle.write(f"群 {row['group']}：独立响应误差 {row['all_64_white_columns_and_6_holdouts_native_action_relative']:.3e}；原始平衡缺陷 {row['raw_native_balance_relative']:.3e}；\n")
            handle.write(f"固定基底在角向源响应中的字段舍弃量 {100*row['angular_source_offspace_min']:.4f}%–{100*row['angular_source_offspace_max']:.4f}%。\n")
        handle.write('\n仅完成零梯度、碰撞与公共白返回响应测量；代数逆矩阵不是轴向传播律。\n')
        handle.write('没有散射/裂变迭代、CE 拟合、基底增广或完整精度验收。AAA 原裂变率门槛仍 FAIL；ABA 未准入。\n')
    print('AXMAT-FULL-ANGULAR-RESPONSE-ANALYZED')


def run(expected):
    declaration=read(require_file(OUT/'declaration.json',expected));verify(declaration['files']);verify_previous()
    resource=DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    write_new(OUT/'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    started=time.monotonic();runner=SerialExecutor(OUT,declaration['total_wall_seconds'],'AAA',resource)
    result=dict(classification='FAILED_CURRENT_FULL_ANGULAR_RESPONSE_NO_RETRY',error=None)
    try:
        runner.execute(OUT,'prepare',[sys.executable,str(Path(__file__).resolve()),'prepare-sources'],30,'AXMAT-FULL-ANGULAR-SOURCES-READY')
        runner.execute(OUT/'inputs','primary',[str(OUT/'runtime/probe_signed'),'primary.txt','primary.bin'],120)
        runner.execute(OUT,'white-prepare',[sys.executable,str(Path(__file__).resolve()),'prepare-white'],30,'AXMAT-FULL-ANGULAR-WHITE-READY')
        runner.execute(OUT/'inputs','white',[str(OUT/'runtime/probe_signed'),'white.txt','white.bin'],120)
        runner.execute(OUT,'analysis',[sys.executable,str(Path(__file__).resolve()),'analyze'],60,'AXMAT-FULL-ANGULAR-RESPONSE-ANALYZED')
        result.update(classification='COMPLETE_BOUNDED_CURRENT_FULL_ANGULAR_RESPONSE_ONLY',ABA_admitted=False)
    except BaseException as error:
        result['error']=repr(error)
        raise
    finally:
        verify(declaration['files']);verify_previous()
        result.update(resources=resource.check(),elapsed_seconds=time.monotonic()-started)
        write_new(OUT/'driver_result.json',result)
    write_new(OUT/'seal.json',dict(schema='AXMAT_CURRENT_FULL_ANGULAR_RESPONSE_SEAL_V1',
        files={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file()}))
    print(json.dumps(dict(classification=read(OUT/'result.json')['classification'],elapsed_seconds=result['elapsed_seconds'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','prepare-sources','prepare-white','analyze'])
    parser.add_argument('--sha256');args=parser.parse_args()
    dict(prepare=prepare,run=lambda:run(args.sha256),
         **{'prepare-sources':prepare_sources,'prepare-white':prepare_white,'analyze':analyze})[args.action]()

"""Diagnose the actual returned radial fields in the frozen rank-one space.

Never self-project the reconstructed axial field or use SPOT-X-PERP as an
online radial error. No transport, enrichment, fitting or accuracy admission.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
FINAL = PROD / 'AAA/map012'
CLOSE = ART / 'axial-material-AAA-white-trace-refined-closeout-20261005'
OUT = ART / 'axial-material-AAA-white-trace-refined-radial-offspace-canonical-20261005'
PREPARED_SHA = '024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import (DiskResources, SerialExecutor, verify_prepared,
                               verify_sealed_directory, require_file)
from snapshot_control_preflight import _open_xsm
from qualified_snapshot_ingestion import list_handles


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, data):
    with Path(path).open('x') as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write('\n')


def verify(files):
    for path, wanted in files.items():
        require_file(Path(path), wanted)


def prepare():
    import numpy as np
    require_file(ROOT / 'validation/axial_material/audit_refined_AAA_radial_offspace.py', '268775e795add365ae6ab3fc523ff147a2e620f0cf1e1b846f8b8f1931d6a7ff')
    require_file(ART / 'axial-material-AAA-white-trace-refined-radial-offspace-20261005/declaration.json', '8fa23799e4478a54758581f52a70c0e7400ab8272ca9ff672c897aa73252754c')
    require_file(ART / 'axial-material-AAA-white-trace-refined-radial-offspace-20261005/input_admission_failure.json', 'b9c95eab22d08481dd23383d1251a2a813fb367795b92a56492f35d64fc4fa4a')
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    require_file(CLOSE / 'seal.json', '7e92cb10c8303d71f7ead901674391f4c36c31af0041daa5145e51366280994d')
    verify({str(CLOSE / n):h for n,h in read(CLOSE / 'seal.json')['files'].items()})
    if read(CLOSE / 'result.json')['classification'] != 'COMPLETE_REFINED_AAA_CLOSEOUT_UNQUALIFIED':
        raise ValueError('actual unqualified full refined closeout required')
    verify_sealed_directory(FINAL)
    OUT.mkdir(exist_ok=False)
    (OUT / 'runtime').mkdir()
    (OUT / 'AAA').mkdir()
    import shutil
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    paths = [Path(__file__).resolve(), Path(sys.executable).resolve(), Path(info['rank_addendum']['path']),
        PROD / 'prepared.json', PROD / 'AAA/run_status.json', FINAL / 'result.json',
        FINAL / 'basis_reference.xsm', FINAL / 'candidate_radial.xsm',
        FINAL / 'closed_snapshots.xsm', FINAL / 'closed_axial.xsm',
        CLOSE / 'seal.json', CLOSE / 'result.json', ROOT / 'src/SPOSTATE.f90',
        ROOT / 'src/SPOPOD.f90', ROOT / 'validation/iterative/diagnose_d4a_radial_offspace.f90',
        OUT / 'runtime/run_bounded_dragon.py',
        *[Path(sys.modules[n].__file__).resolve() for n in ('production_runner','snapshot_control_preflight','qualified_snapshot_ingestion')]]
    paths += [ROOT / 'validation/axial_material/audit_refined_AAA_radial_offspace.py', ART / 'axial-material-AAA-white-trace-refined-radial-offspace-20261005/declaration.json', ART / 'axial-material-AAA-white-trace-refined-radial-offspace-20261005/input_admission_failure.json']
    numpy_root = Path(np.__file__).parent
    paths += sorted(p for p in numpy_root.rglob('*') if p.is_file() and p.suffix in ('.py','.so','.dylib'))
    roots = sorted(set(read(CLOSE / 'declaration.json')['resource_roots']) | {str(OUT)})
    resources = DiskResources(ART, roots, 8*2**30, 96*2**30)
    write_new(OUT / 'declaration.json', dict(schema='AXMAT_REFINED_RADIAL_OFFSPACE_DIAGNOSTIC_V1',
        files={str(p.resolve()):digest(p) for p in paths}, resource_roots=roots, min_free_bytes=8*2**30,
        artifact_budget_bytes=96*2**30, resources_before=resources.check(),
        total_wall_seconds=120, child_wall_seconds=60, threads=1, retries=0,
        epoch=12, regions=8, radial_unknowns=14, groups=370, planes=3, rank=1,
        reference_numpy_version=np.__version__, transport_launched=False,
        formula='W=VOL2D/sum(VOL2D); G=B^T W B; a=G^-1 B^T W u; '
                'e=u-Ba; overall=sqrt(sum_pg H[p]*e^T W e/sum_pg H[p]*u^T W u). '
                'B is stored REAL32 promoted once; u is actual RETURNED REAL64 radial authority.',
        checks='All 1110 authority fields equal CLOSED byte for byte, exact REAL32 mirrors, '
               'KEYFLX/volume/lifecycle/epoch, stored Gram and common-basis bytes. '
               'Independent analytic projection fixtures; in-space, off-space, scaling, zero, '
               'non-unit Gram and malformed inputs. All three singular values per group.',
        scope='Diagnostic only. No numerical residual acceptance or truncation accuracy bound. '
              'No reconstructed axial field/SPOT-X-PERP is projected. No per-field normalization '
              'or CE fitting, transport, new training, rank selection, source change or ABA admission.'))
    print(json.dumps(dict(declaration_sha256=digest(OUT / 'declaration.json'))))


def field(a, directory, name, dtype, count):
    import numpy as np
    kind = {'<i4':1, '<f4':2, '<f8':4}[dtype]
    words = count*(2 if dtype == '<f8' else 1)
    return np.frombuffer(a.record(directory,name,words,kind), dtype).copy()


def label(a, directory, name, wanted):
    text = a.record(directory,name,3,3).decode('ascii').rstrip(' \x00')
    if text != wanted:
        raise ValueError('wrong lifecycle/signature: '+name)


def project(weights, basis, gram, values):
    import numpy as np
    if (weights.shape != basis.shape or values.shape != basis.shape
            or np.any(weights <= 0) or not np.isfinite(weights).all()
            or not np.isfinite(basis).all() or not np.isfinite(values).all()
            or not np.isfinite(gram) or gram <= 0):
        raise ValueError('invalid rank-one projection inputs')
    calculated = sum(float(w)*float(b)*float(b) for w,b in zip(weights,basis,strict=True))
    if calculated != gram:
        raise ValueError('Gram must be actual non-unit B^T W B')
    coefficient = sum(float(w)*float(b)*float(u) for w,b,u in zip(weights,basis,values,strict=True))/gram
    residual = values-basis*coefficient
    norm2 = sum(float(w)*float(u)**2 for w,u in zip(weights,values,strict=True))
    error2 = sum(float(w)*float(e)**2 for w,e in zip(weights,residual,strict=True))
    return coefficient, norm2, error2


def fixtures():
    import numpy as np
    w=np.array([.25,.25,.5]); b=np.array([2.,0.,0.]); u=np.array([2.,4.,3.])
    tests = [(b,1.,u,(1.,9.5,8.5)), (b,1.,2*b,(2.,4.,0.)),
             (b,1.,8*u,(8.,608.,544.)), (b,1.,0*u,(0.,0.,0.)),
             (2*b,4.,u,(.5,9.5,8.5))]
    for basis,gram,values,wanted in tests:
        if project(w,basis,gram,values) != wanted:
            raise ValueError('independent analytic projection fixture failed')
    bad = [(w,b,0.,u), (w,b,2.,u), (-w,b,1.,u), (w,b,1.,u[:2]),
           (w,b,1.,np.array([2.,float('nan'),3.]))]
    for args in bad:
        try:
            project(*args)
        except ValueError:
            pass
        else:
            raise ValueError('malformed projection accepted')
    return dict(analytic_fixtures_passed=len(tests), malformed_inputs_rejected=len(bad))


def child(expected):
    import numpy as np
    d=read(require_file(OUT / 'declaration.json',expected)); verify(d['files'])
    tests=fixtures()
    weights=[]; bases=[]; spectra=[]; records=[]
    with _open_xsm(FINAL / 'basis_reference.xsm') as basis, _open_xsm(FINAL / 'closed_axial.xsm') as axial:
        label(axial,axial.root,'SPOT-X-STATE','CLOSED')
        if field(axial,axial.root,'SPOT-X-EPOCH','<i4',1).tolist() != [12]:
            raise ValueError('wrong completed epoch')
        if field(basis,basis.root,'POD-RANK-G','<i4',370).tolist() != [1]*370:
            raise ValueError('not the actual frozen common rank one')
        stored_basis=field(axial,axial.root,'SPOT-X-BASIS','<f4',2960).reshape(370,8)
        gram=field(axial,axial.root,'SPOT-X-GRAM','<f8',370)
        heights=field(axial,axial.root,'SPOT-X-H','<f8',3)
        if heights.tolist() != [50.,50.,50.]:
            raise ValueError('original three physical zones changed')
        root_sigma=field(basis,basis.root,'POD-SIGMA-G','<f8',1110).reshape(370,3)
        volume=None
        for g,handle in enumerate(list_handles(basis,basis.root,'GROUP',370)):
            group=basis.directory(handle[0])
            if field(basis,group,'POD-NMODE','<i4',1).tolist() != [1]:
                raise ValueError('wrong group rank')
            v=field(basis,group,'VOL2D','<f4',8)
            if volume is None: volume=v
            if v.tobytes() != volume.tobytes() or np.any(v<=0):
                raise ValueError('physical volume changed')
            b=field(basis,group,'POD-BASIS','<f4',8)
            if b.tobytes() != stored_basis[g].tobytes():
                raise ValueError('closed axial common basis changed')
            sigma=field(basis,group,'POD-SIGMA','<f8',3)
            if sigma.tobytes() != root_sigma[g].tobytes() or not np.isfinite(sigma).all() or sigma[0]<=0:
                raise ValueError('invalid or changed complete group spectrum')
            weights.append(v.astype(float)/sum(float(x) for x in v))
            bases.append(b.astype(float));spectra.append(sigma)
    with _open_xsm(FINAL / 'candidate_radial.xsm') as returned, _open_xsm(FINAL / 'closed_snapshots.xsm') as closed:
        for a,state in [(returned,'RETURNED'),(closed,'CLOSED')]:
            label(a,a.root,'SIGNATURE','L_ARCHIVE')
            auth=a.directory(a.root['SPOT-R64'][0]); label(a,auth,'STATE',state)
            if field(a,auth,'EPOCH','<i4',1).tolist() != [12]:
                raise ValueError('wrong radial archive epoch')
        trackers=[list_handles(a,a.root,'TRACK',3) for a in (returned,closed)]
        fluxes=[list_handles(a,a.root,'FLUX',3) for a in (returned,closed)]
        for plane in range(3):
            dirs=[]; keys=[]; authorities=[]; mirrors=[]
            for i,a in enumerate((returned,closed)):
                tr=a.directory(trackers[i][plane][0]); fd=a.directory(fluxes[i][plane][0])
                k=field(a,tr,'KEYFLX','<i4',8)
                if len(set(k.tolist()))!=8 or np.any(k<1) or np.any(k>14):
                    raise ValueError('invalid scalar keys')
                if field(a,tr,'VOLUME','<f4',8).tobytes() != volume.tobytes():
                    raise ValueError('TRACK/POD volumes differ')
                if field(a,fd,'KEYFLX','<i4',8).tobytes() != k.tobytes():
                    raise ValueError('TRACK/flux keys differ')
                if field(a,fd,'SPOT-FS-EQN','<i4',1).tolist() != [1]:
                    raise ValueError('not an actual online fixed-source return')
                authority=a.directory(fd['SPOT-R64'][0]);label(a,authority,'STATE','SOLVED')
                if field(a,authority,'EPOCH','<i4',1).tolist() != [12]:
                    raise ValueError('wrong authority epoch')
                authorities.append(list_handles(a,authority,'FLUX',370));mirrors.append(list_handles(a,fd,'FLUX',370))
                dirs.append(fd);keys.append(k)
            if keys[0].tobytes()!=keys[1].tobytes():
                raise ValueError('closure changed scalar keys')
            for g in range(370):
                raw=[]
                for i,a in enumerate((returned,closed)):
                    item=authorities[i][g];mirror=mirrors[i][g]
                    if item[1:]!=(28,4) or mirror[1:]!=(14,2):
                        raise ValueError('incomplete REAL64 radial authority/mirror')
                    data=a.read(item[0],item[1]);values=np.frombuffer(data,'<f8').copy()
                    if not np.isfinite(values).all() or np.any(values[keys[i]-1]<=0):
                        raise ValueError('invalid active REAL64 flux')
                    if values.astype('<f4').tobytes()!=a.read(mirror[0],mirror[1]):
                        raise ValueError('REAL32 mirror differs from authority')
                    raw.append(data)
                if raw[0]!=raw[1]:
                    raise ValueError('closure changed actual radial authority')
                values=np.frombuffer(raw[0],'<f8')[keys[0]-1]
                coefficient,norm2,error2=project(weights[g],bases[g],gram[g],values)
                records.append(dict(plane=plane+1,group=g+1,weighted_norm2=norm2,offspace_norm2=error2,
                    relative_offspace=(error2/norm2)**.5 if norm2>0 else None,
                    coefficient=coefficient,sigma2_over_sigma1=float(spectra[g][1]/spectra[g][0]),
                    sigma3_over_sigma1=float(spectra[g][2]/spectra[g][0])))
    overall_norm=sum(heights[r['plane']-1]*r['weighted_norm2'] for r in records)
    overall_error=sum(heights[r['plane']-1]*r['offspace_norm2'] for r in records)
    for r in records:
        r['overall_norm_fraction']=float(heights[r['plane']-1]*r['weighted_norm2']/overall_norm)
    maximum=max(records,key=lambda r:r['relative_offspace'])
    planes=[]
    for plane in range(1,4):
        rows=[r for r in records if r['plane']==plane]
        n=sum(r['weighted_norm2'] for r in rows);e=sum(r['offspace_norm2'] for r in rows)
        planes.append(dict(plane=plane,relative_offspace=(e/n)**.5))
    with (OUT / 'radial_group_offspace.csv').open('x') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    spectrum=[dict(group=g+1,sigma1=float(s[0]),sigma2=float(s[1]),sigma3=float(s[2]),
        sigma2_over_sigma1=float(s[1]/s[0]),sigma3_over_sigma1=float(s[2]/s[0]),
        second_direction_REAL32_resolved=bool(s[1]>8*2**-23*s[0])) for g,s in enumerate(spectra)]
    with (OUT / 'common_basis_spectrum.csv').open('x') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(spectrum[0]));writer.writeheader();writer.writerows(spectrum)
    unresolved=[r['group'] for r in spectrum if not r['second_direction_REAL32_resolved']]
    result=dict(classification='COMPLETE_ACTUAL_RADIAL_OFFSPACE_DIAGNOSTIC_ONLY',
        complete_fields=1110, authority_closure_byte_exact=True, mirrors_byte_exact=True,
        fixtures=tests, overall_relative_offspace=float((overall_error/overall_norm)**.5),
        planes=planes, maximum_group=maximum, resolved_second_directions=370-len(unresolved),
        unresolved_second_direction_groups=unresolved,
        sigma2_over_sigma1_range=[min(r['sigma2_over_sigma1'] for r in spectrum),max(r['sigma2_over_sigma1'] for r in spectrum)],
        all_original_input_and_accuracy_gates_unchanged=True, transport_launched=False,
        truncation_accuracy_qualified=False, causal_explanation_established=False, ABA_admitted=False,
        scope=d['scope'])
    verify(d['files'])
    write_new(OUT / 'result.json',result)
    with (OUT / 'REPORT.txt').open('x') as stream:
        stream.write(f'''最终 AAA 实际径向通量的降阶空间诊断（2026-10-05）

读取最终 map012 RETURNED 径向计算的三平面、370 群、全部 1110 个 REAL64 权威场。
这些场与 CLOSED 归档逐字节一致，REAL32 镜像和区域映射也一致。
采用冻结公共基底和实际非单位 Gram 矩阵，未读取轴向 SPOT-X-PERP 作为径向误差。
投影是 W=VOL2D/sum(VOL2D) 的最佳 rank1 表示，不做局部归一化。

当前全部群积分通量的区域面积/平面高度加权相对空间外范数：{100*result['overall_relative_offspace']:.6f}%。
三平面分别为 {', '.join(f"{100*p['relative_offspace']:.6f}%" for p in planes)}。
最大单群比例位于群 {maximum['group']}、平面 {maximum['plane']}：{100*maximum['relative_offspace']:.6f}%，
该群占整体通量平方范数 {100*maximum['overall_norm_fraction']:.6f}%。
全部群/平面数据保留在 radial_group_offspace.csv。

原公共基底中 {370-len(unresolved)} 群的第二奇异方向超过原 REAL32 输入分辨率门槛；
未分辨群为 {unresolved}。全部三奇异值保留在 common_basis_spectrum.csv。
输入分辨率门槛是 8*epsilon(REAL32)*sigma1，未改动。没有选择新 rank 或重训。

这是当前径向场的表示误差，范数不是裂变率误差或 CE 误差上界。
它不能单独解释端部偏差，也不能估计新 rank 的完整耦合结果。
实际 AAA 独立裂变率门槛仍 FAIL；没有准入 ABA。所有冻结输入和源代码保持不变。
''')
    print('AXMAT-REFINED-RADIAL-OFFSPACE-COMPLETE')


def run(expected):
    d=read(require_file(OUT / 'declaration.json',expected));verify(d['files'])
    resources=DiskResources(ART,d['resource_roots'],d['min_free_bytes'],d['artifact_budget_bytes'])
    write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    executor=SerialExecutor(OUT,d['total_wall_seconds'],'AAA',resources)
    executor.execute(OUT / 'AAA','offspace',[sys.executable,str(Path(__file__).resolve()),'child','--sha256',expected],
                     d['child_wall_seconds'],'AXMAT-REFINED-RADIAL-OFFSPACE-COMPLETE')
    verify(d['files']);verify_sealed_directory(FINAL)
    write_new(OUT / 'driver_result.json',dict(classification='COMPLETE_BOUNDED_RADIAL_OFFSPACE_DIAGNOSTIC_ONLY',
        declaration_sha256=expected,resources=resources.check(),transport_launched=False,ABA_admitted=False))
    write_new(OUT / 'seal.json',dict(schema='AXMAT_RADIAL_OFFSPACE_SEAL_V1',
        files={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file()}))
    result=read(OUT / 'result.json')
    print(json.dumps({k:result[k] for k in ('classification','complete_fields','overall_relative_offspace',
        'planes','maximum_group','resolved_second_directions','unresolved_second_direction_groups')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run','child'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else (run(args.sha256) if args.action=='run' else child(args.sha256))

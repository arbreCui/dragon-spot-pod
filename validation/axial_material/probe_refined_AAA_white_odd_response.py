"""Same-data zero-gradient native odd response versus the conditional trace.

Read the actual final AAA radial inputs. Reuse the sealed signed native host.
No scattering/fission iteration, axial propagation, transport-data correction,
POD enrichment, fitted coefficient or AAA/ABA accuracy claim follows.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import time

sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'validation/artifacts'
PROD=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
FINAL=PROD/'AAA/map012'
OLD=ART/'native-signed-axial-state-20260929'
CLOSE=ART/'axial-material-AAA-white-trace-refined-closeout-20261005'
OUT=ART/'axial-material-AAA-white-trace-refined-native-odd-response-20261005'
PREPARED_SHA='024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'
GROUPS=[51,61,98]
sys.path.insert(0,str(PROD/'runtime'))
from production_runner import DiskResources,SerialExecutor,verify_prepared,verify_sealed_directory,require_file
from snapshot_control_preflight import _open_xsm
from qualified_snapshot_ingestion import list_handles
sys.path.insert(0,str(ROOT/'validation/axial_material'))
from white_side_trace_kernel import trace_exchange


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def read(path):return json.loads(Path(path).read_text())


def write_new(path,data):
    with Path(path).open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def verify(files):
    for path,wanted in files.items():require_file(Path(path),wanted)


def field(a,d,name,dtype,count):
    import numpy as np
    kind={'<i4':1,'<f4':2,'<f8':4}[dtype]
    return np.frombuffer(a.record(d,name,count*(2 if dtype=='<f8' else 1),kind),dtype).copy()


def same_object(a,previous,b,actual):
    names=lambda d:set(d)-{'***DEL***'}
    if names(previous)!=names(actual):raise ValueError('copied native record names differ')
    for name in names(previous):
        p,n=previous[name],actual[name]
        if p[1:]!=n[1:]:raise ValueError('copied native record layout differs')
        if p[2]==0:same_object(a,a.directory(p[0]),b,b.directory(n[0]))
        elif p[2]==10:
            for x,y in zip(a.integers(p[0],p[1]),b.integers(n[0],n[1]),strict=True):
                same_object(a,a.directory(x),b,b.directory(y))
        elif a.read(p[0],p[1])!=b.read(n[0],n[1]):raise ValueError('copied native words differ: '+name)


def prepare():
    import numpy as np
    info=verify_prepared(PROD/'prepared.json',PREPARED_SHA)
    verify_sealed_directory(FINAL)
    require_file(CLOSE/'seal.json','7e92cb10c8303d71f7ead901674391f4c36c31af0041daa5145e51366280994d')
    verify({str(CLOSE/n):h for n,h in read(CLOSE/'seal.json')['files'].items()})
    if read(CLOSE/'result.json')['classification']!='COMPLETE_REFINED_AAA_CLOSEOUT_UNQUALIFIED':
        raise ValueError('complete actual refined AAA failure required')
    # The original numerical host and libraries must still match their own seal.
    manifest={}
    for line in (OLD/'result.sha256').read_text().splitlines():
        h,n=line.split(None,1);manifest[n.lstrip('*')]=h
    selected=['build/probe_signed','build/probe_native_signed_axial.f90','build/ganlib.mod',
              'build/libDragon.a','build/libTrivac.a','build/libUtilib.a','build/libGanlib.a']
    verify({str(OLD/n):manifest[n] for n in selected})
    OUT.mkdir(exist_ok=False)
    for n in ['runtime','build','inputs','AAA']:(OUT/n).mkdir()
    shutil.copy2(PROD/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py')
    shutil.copy2(OLD/'build/probe_signed',OUT/'runtime/probe_signed')
    shutil.copy2(FINAL/'candidate_radial.xsm',OUT/'inputs/archive.xsm')
    shutil.copy2(FINAL/'initial_radial_track.bin',OUT/'inputs/rays.bin')
    compiler=Path(shutil.which('gfortran')).resolve()
    source=ROOT/'validation/axial_material/extract_radial_collision_inputs.f90'
    command=[str(compiler),'-O2','-ffp-contract=off','-fcheck=all','-I'+str(OLD/'build'),
        '-J'+str(OUT/'build'),str(source),str(OLD/'build/libUtilib.a'),str(OLD/'build/libGanlib.a'),
        '-o',str(OUT/'runtime/extract')]
    paths=[Path(__file__).resolve(),Path(sys.executable).resolve(),compiler,source,
        PROD/'prepared.json',PROD/'AAA/run_status.json',FINAL/'result.json',
        FINAL/'candidate_radial.xsm',FINAL/'basis_reference.xsm',FINAL/'initial_radial_track.bin',
        PROD/'AAA/bootstrap/initial_axial_track.xsm',CLOSE/'seal.json',CLOSE/'result.json',
        Path(info['case_spec']['path']),OLD/'result.sha256',OLD/'plan.json',OLD/'verification.json',
        *[OLD/n for n in selected],ROOT/'src/MCGFFAR.f',ROOT/'src/MCGSCA.f',ROOT/'src/MCGDSCA.f',
        ROOT/'src/MCGFST.f',ROOT/'src/MCCGT.f',ROOT/'src/NXTTNS.f',ROOT/'src/SPOT1P64.f90',
        ROOT/'validation/iterative/qualify_native_signed_axial.py',
        *[Path(sys.modules[n].__file__).resolve() for n in ['production_runner','snapshot_control_preflight','qualified_snapshot_ingestion','white_side_trace_kernel']],
        OUT/'runtime/run_bounded_dragon.py',OUT/'runtime/probe_signed',OUT/'inputs/archive.xsm',OUT/'inputs/rays.bin']
    paths += [p for p in (OLD/'build').glob('*.mod')]
    paths += [p for p in Path(np.__file__).parent.rglob('*') if p.is_file() and p.suffix in ['.py','.so','.dylib']]
    files={str(p.resolve()):digest(p) for p in paths};verify(files)
    roots=sorted(set(read(CLOSE/'declaration.json')['resource_roots'])|{str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()}|{str(OUT)})
    resource=DiskResources(ART,roots,8*2**30,96*2**30)
    write_new(OUT/'declaration.json',dict(schema='AXMAT_REFINED_NATIVE_ODD_RESPONSE_V1',files=files,
        build_command=command,groups=GROUPS,total_wall_seconds=300,
        stage_caps=dict(build=60,extract=30,prepare=30,primary_flights=120,white_prepare=30,white_flights=120,analysis=60),
        resource_roots=roots,min_free_bytes=8*2**30,artifact_budget_bytes=96*2**30,
        resources_before=resource.check(),threads=1,numeric_children_at_once=1,retries=0,
        primary_cases_per_group=10,independent_white_cases_per_group=3,pair_amplitude=.5,
        native_action_relative_limit=5e-12,raw_native_balance_relative_limit=1e-6,
        source='Frozen rank1 basis, oriented positive without changing its space; '
               'q=b*(1+s*0.5*mu), s=-1,0,+1, plus q=b*mu and six common boundary coordinates. '
               'Groups 51/61/98 retain the previous native directional diagnostic selection.',
        quadrature='Actual four native polar nodes with independent axial signs; mu=sqrt(1-ZMU^-2). '
                   'Conditional model is evaluated on these same nodes/derived weights. '
                   'The actual production SN32 quadrature is reported separately, never equated to this probe.',
        collision_model='Projected total tau=sum W*b^2*Sigma_t; Gram G=sum W*b^2. '
                        'Conditional weak operator tau*I+b_Na^2*K, source G*mu. '
                        'Projected current G*sum(w*mu*a)/2. No scattering or fission iteration.',
        white='Measure the full six-surface native return block, solve common white return, '
              'then execute fresh native positive paired sources at those inflows. '
              'Preserve native surface weights and report raw physical balance; no rebalance.',
        decision='Report local same-data angular-response discrepancy only. No CE fit, '
                 'new coefficient, propagation law, reduced eigenmode or coupled accuracy admission.',
        original_physical_inputs_changed=False,original_accuracy_thresholds_changed=False,ABA_admitted=False))
    print(json.dumps(dict(declaration_sha256=digest(OUT/'declaration.json'))))


def data():
    import numpy as np
    with _open_xsm(OUT/'inputs/track.xsm') as a:
        st=field(a,a.root,'STATE-VECTOR','<i4',40);mc=field(a,a.root,'MCCG-STATE','<i4',40)
        if st[:6].tolist()!=[8,14,1,8,6,1] or mc[[1,14,15,19]].tolist()!=[4,1,1,1]:
            raise ValueError('outside original signed-host scope')
        keys=field(a,a.root,'KEYFLX','<i4',8);cur=field(a,a.root,'KEYCUR$MCCG','<i4',6)
        if keys.tolist()!=list(range(1,9)) or cur.tolist()!=list(range(9,15)):
            raise ValueError('original identity key layout required')
        if field(a,a.root,'BC-REFL+TRAN','<i4',6).tolist()!=list(range(1,7)) or field(a,a.root,'ALBEDO','<f4',6).tolist()!=[1]*6:
            raise ValueError('same unit white identity return required')
        vol=field(a,a.root,'V$MCCG','<f4',14).astype(float)
        z=field(a,a.root,'ZMU$MCCG','<f4',4).astype(float);wz=field(a,a.root,'WZMU$MCCG','<f4',4).astype(float)
        mu=np.sqrt(1-1/z**2);angular=wz*z
        mat=field(a,a.root,'MATCOD','<i4',8)
    weights=vol[:8]/sum(float(x) for x in vol[:8]);basis={};totals={}
    with _open_xsm(FINAL/'basis_reference.xsm') as a:
        hs=list_handles(a,a.root,'GROUP',370)
        for g in GROUPS:
            d=a.directory(hs[g-1][0]);b=field(a,d,'POD-BASIS','<f4',8).astype(float)
            if b[0]<0:b=-b
            if np.any(b<=0) or field(a,d,'VOL2D','<f4',8).astype(float).tobytes()!=vol[:8].tobytes():
                raise ValueError('positive first-mode source and original volumes required')
            basis[g]=b
    with _open_xsm(OUT/'inputs/system.xsm') as a:
        hs=list_handles(a,a.root,'GROUP',370)
        for g in GROUPS:
            x=field(a,a.directory(hs[g-1][0]),'DRAGON-TXSC','<f4',9).astype(float)[mat]
            if np.any(x<=0):raise ValueError('positive actual collision totals required')
            totals[g]=x
    return dict(vol=vol,z=z,wz=wz,mu=mu,angular=angular,weights=weights,basis=basis,totals=totals)


def sources(path,records):
    with Path(path).open('x') as f:
        f.write(str(len(records))+'\n')
        for g,q,incoming in records:
            f.write(str(g)+' '+' '.join(format(float(v),'.17e') for v in [*q.ravel(),*incoming.ravel()])+'\n')


def prepare_sources():
    import numpy as np
    d=data();records=[]
    with _open_xsm(OUT/'inputs/archive.xsm') as archive:
        for name,output in [('TRACK','track.xsm'),('SYSTEM','system.xsm')]:
            previous=archive.directory(list_handles(archive,archive.root,name,3)[0][0])
            with _open_xsm(OUT/'inputs'/output) as copy:same_object(archive,previous,copy,copy.root)
    signed=np.array([1.,-1.])[:,None,None]*d['mu'][None,:,None]
    for g in GROUPS:
        b=d['basis'][g];zero=np.zeros((2,4,6))
        for s in [-1.,0.,1.]:records.append((g,b[None,None,:]*(1+s*.5*signed),zero))
        records.append((g,b[None,None,:]*signed,zero))
        for face in range(6):
            inc=zero.copy();inc[:,:,face]=1
            records.append((g,np.zeros((2,4,8)),inc))
    sources(OUT/'inputs/primary.txt',records)
    write_new(OUT/'input_copy_admission.json',dict(status='BYTE_EXACT_CURRENT_TRACK_AND_SYSTEM',
        actual_archive_sha256=digest(OUT/'inputs/archive.xsm'),groups=GROUPS,primary_cases=30,
        zero_gradient_only=True,shared_source_changed=False))
    print('AXMAT-ODD-PROBE-SOURCES-READY')


def native(path):
    import numpy as np
    with Path(path).open('rb') as f:
        header=np.fromfile(f,'<i4',5)
        if header[:4].tolist()!=[290902,8,6,4]:raise ValueError('wrong unchanged native host layout')
        meta=np.fromfile(f,'<f4',26);iso=[];own=[];groups=[]
        for c in range(int(header[4])):
            g,index=np.fromfile(f,'<i4',2)
            if index!=c+1:raise ValueError('native case sequence differs')
            iso.append(np.fromfile(f,'<f8',112).reshape(2,4,14));own.append(np.fromfile(f,'<f8',64).reshape(2,4,8));groups.append(int(g))
        if f.read(1):raise ValueError('extra native bytes')
    return np.stack(iso,axis=-1),np.stack(own,axis=-1),groups,meta


def prepare_white():
    import numpy as np
    d=data();f,own,groups,meta=native(OUT/'inputs/primary.bin');records=[];closure=[]
    if groups!=sum(([g]*10 for g in GROUPS),[]):raise ValueError('incomplete primary flights')
    signed=np.array([1.,-1.])[:,None,None]*d['mu'][None,:,None]
    for gi,g in enumerate(GROUPS):
        off=10*gi;out=f[:,:,8:,off:off+10].sum(axis=(0,1))
        transfer=out[:,4:10]/d['vol'][8:,None]
        matrix=np.eye(6)-transfer;rhs=out[:,1]/d['vol'][8:]
        amplitude=np.linalg.solve(matrix,rhs);inverse=np.linalg.solve(matrix,np.eye(6))
        rho=float(max(abs(np.linalg.eigvals(transfer))))
        if rho>=1 or amplitude.min()<0 or inverse.min()<0:raise ValueError('native common white return not admissible')
        if np.max(abs(matrix@amplitude-rhs))/np.max(abs(rhs))>5e-12:raise ValueError('native white solve residual failed')
        for s in [-1.,0.,1.]:records.append((g,d['basis'][g][None,None,:]*(1+s*.5*signed),np.broadcast_to(amplitude,(2,4,6)).copy()))
        closure.append(dict(group=g,amplitude=amplitude.tolist(),transfer=transfer.tolist(),rho=rho))
    sources(OUT/'inputs/white.txt',records);write_new(OUT/'white_closure.json',closure)
    print('AXMAT-ODD-PROBE-WHITE-READY')


def geometric_volumes(d):
    import numpy as np
    widths=np.zeros(8)
    with (OUT/'inputs/rays.bin').open('rb') as f:
        def record():
            raw=f.read(4)
            if len(raw)!=4:raise ValueError('missing ray record')
            n=struct.unpack('<i',raw)[0];body=f.read(n)
            if len(body)!=n or f.read(4)!=raw:raise ValueError('bad ray record')
            return body
        magic,ncom,ntr,fmt=struct.unpack('<4siii',record())
        for _ in range(ncom):record()
        layout=struct.unpack('<9i',record())
        if layout[0]!=2 or layout[2:4]!=(8,6) or layout[-2]!=1:raise ValueError('actual native ray layout differs')
        for _ in range(6):record()
        for _ in range(ntr):
            body=record();nsub,nseg,weight=struct.unpack_from('<iid',body)
            # NXT format 1 also stores four integer and ndim*nsub real tags.
            extra=16+8*layout[0]*nsub if fmt==1 else 0
            if nsub!=1 or len(body)!=16+4*nsub+12*nseg+extra:raise ValueError('ray sample incomplete')
            region=np.frombuffer(body,'<i4',nseg,16+4*nsub);h=np.frombuffer(body,'<f8',nseg,16+4*nsub+4*nseg)
            np.add.at(widths,region[1:-1]-1,weight*h[1:-1])
        if f.read(1):raise ValueError('unexpected extra ray record')
    return d['angular'][:,None]*widths[None,:]


def analyze():
    import numpy as np
    d=data();pf,po,pg,pm=native(OUT/'inputs/primary.bin');wf,wo,wg,wm=native(OUT/'inputs/white.bin')
    if pg!=sum(([g]*10 for g in GROUPS),[]) or wg!=sum(([g]*3 for g in GROUPS),[]):raise ValueError('all declared native flights required')
    if pm.tobytes()!=wm.tobytes() or not np.isfinite(pf).all() or not np.isfinite(po).all() or not np.isfinite(wf).all() or not np.isfinite(wo).all():raise ValueError('native metadata or finite field admission failed')
    if not np.array_equal(pm[:14].astype(float),d['vol']):raise ValueError('actual native weights differ')
    geom=geometric_volumes(d);rows=[];checks=[]
    state_mu=np.array([1.,-1.])[:,None]*d['mu'][None,:]
    c=read(OUT/'white_closure.json');native_mu=np.r_[d['mu'],-d['mu']];native_w=np.r_[d['angular'],d['angular']]
    with _open_xsm(PROD/'AAA/bootstrap/initial_axial_track.xsm') as a:
        prod_mu=field(a,a.root,'U','<f4',32).astype(float);prod_w=field(a,a.root,'W','<f4',32).astype(float)
    def relative(a,b):
        scale=float(np.max(abs(b)))
        if scale<=0:raise ValueError('undefined diagnostic norm')
        return float(np.max(abs(a-b))/scale)
    for gi,g in enumerate(GROUPS):
        p=slice(gi*10,gi*10+10);w=slice(gi*3,gi*3+3);b=d['basis'][g];sigma=d['totals'][g]
        pi=pf[:,:,:8,p]+po[:,:,:,p];wi=wf[:,:,:8,w]+wo[:,:,:,w]
        pb=pf[:,:,8:,p];wb=wf[:,:,8:,w]
        if min(pi[:,:,:,:3].min(),pi[:,:,:,4:].min(),wi.min(),pb[:,:,:,:3].min(),pb[:,:,:,4:].min(),wb.min())<0:
            raise ValueError('positive native source response became negative')
        expected_i=pi[:,:,:,:3]+np.einsum('zprk,k->zpr',pi[:,:,:,4:10],np.array(c[gi]['amplitude']))[:,:,:,None]
        expected_b=pb[:,:,:,:3]+np.einsum('zpsk,k->zps',pb[:,:,:,4:10],np.array(c[gi]['amplitude']))[:,:,:,None]
        assembly=max(relative(wi,expected_i),relative(wb,expected_b))
        parity=max(relative(pi[:,:,:,0]+pi[:,:,:,2],2*pi[:,:,:,1]),relative(pb[:,:,:,0]+pb[:,:,:,2],2*pb[:,:,:,1]))
        pj=np.einsum('zp,zprc->rc',state_mu,pi)/d['vol'][:8,None]
        wj=np.einsum('zp,zprc->rc',state_mu,wi)/d['vol'][:8,None]
        odd_vac=pj[:,2]-pj[:,0];odd_white=wj[:,2]-wj[:,0]
        odd_identity=max(relative(odd_vac,pj[:,3]),relative(odd_white,pj[:,3]))
        closure=float(np.max(abs(wb.sum(axis=(0,1))-d['vol'][8:,None]*np.array(c[gi]['amplitude'])[:,None]))/np.max(abs(wb.sum(axis=(0,1)))))
        signed=np.array([1.,-1.])[:,None,None]*d['mu'][None,:,None]
        q=b[None,None,:,None]*(1+.5*signed[:,:,:,None]*np.array([-1.,0.,1.]))
        incoming=np.array(c[gi]['amplitude'])
        surface_in=(incoming*d['vol'][8:]).sum()
        born=np.einsum('zprc,pr->c',q,geom)
        collision=np.einsum('zprc,r->c',wi,sigma);out=wb.sum(axis=(0,1,2))
        ledger=float(np.max(abs(born+surface_in-collision-out)/(born+surface_in)))
        if max(assembly,parity,odd_identity,closure)>5e-12 or ledger>1e-6:raise ValueError('original native action/white/parity/balance screen failed')
        gram=sum(float(v)*float(x)*float(x) for v,x in zip(d['weights'],b,strict=True))
        tau=sum(float(v)*float(x)*float(x)*float(t) for v,x,t in zip(d['weights'],b,sigma,strict=True))
        projected_native=float(np.dot(d['weights']*b,pj[:,3]))
        def model(mu,weight):
            kernel=trace_exchange(mu,weight,6*.61776479,sum(float(x) for x in d['vol'][:8]))
            matrix=tau*np.eye(len(mu))+b[0]**2*kernel
            solution=np.linalg.solve(matrix,gram*mu)
            if relative(matrix@solution,gram*mu)>5e-12:raise ValueError('conditional response solve failed')
            return float(gram*np.dot(weight*mu,solution)/2)
        matched=model(native_mu,native_w);sn32=model(prod_mu,prod_w)
        rows.append(dict(group=g,projected_native_white_odd_current=projected_native,
            conditional_same_native_grid=matched,conditional_production_SN32=sn32,
            same_grid_signed_relative_difference=matched/projected_native-1,
            conditional_SN32_vs_native_grid_relative=sn32/matched-1))
        checks.append(dict(group=g,independent_white_native_action=assembly,source_pair_parity=parity,
            white_odd_equals_vacuum_and_direct_source=odd_identity,white_closure=closure,
            raw_native_even_balance=ledger,native_white_spectral_radius=c[gi]['rho']))
    with (OUT/'response_comparison.csv').open('x') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result=dict(classification='COMPLETE_SAME_DATA_ZERO_GRADIENT_NATIVE_ODD_RESPONSE_ONLY',groups=GROUPS,
        actual_native_flights=39,checks=checks,comparisons=rows,source_or_operator_fitted=False,
        physical_accuracy_qualified=False,axial_propagation_qualified=False,ABA_admitted=False,
        scope=read(OUT/'declaration.json')['decision'])
    write_new(OUT/'result.json',result)
    with (OUT/'REPORT.txt').open('x') as f:
        f.write('AAA 同数据白边界角向响应诊断（2026-10-05）\n\n')
        f.write('实际本轮 AAA 截面、轨迹、固定 rank1 基底；原生有符号角向核未改变。\n')
        f.write('零轴向梯度、碰撞响应，使用原生四极点及独立轴向正负号。\n')
        f.write('全部 39 次声明的原生飞行完成；正源、线性装配、源对称、白返回闭合与原始平衡通过。\n')
        for row in rows:
            f.write(f"群 {row['group']}：当前条件白迹模型的投影奇响应，相对同网格原生白返回值差 {100*row['same_grid_signed_relative_difference']:.4f}%；\n")
            f.write(f"同一条件模型 SN32 与原生匹配网格之差 {100*row['conditional_SN32_vs_native_grid_relative']:.4f}%。\n")
        f.write('\n没有散射/裂变迭代或轴向传播；此诊断不能解释全部 CE 误差或替代完整耦合验收。\n')
        f.write('未拟合或修改白迹系数，未建立新求解器或准入 ABA。原 AAA 裂变率门槛仍 FAIL。\n')
    print('AXMAT-NATIVE-ODD-RESPONSE-ANALYZED')


def run(expected):
    d=read(require_file(OUT/'declaration.json',expected));verify(d['files'])
    resource=DiskResources(ART,d['resource_roots'],d['min_free_bytes'],d['artifact_budget_bytes'])
    write_new(OUT/'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    started=time.monotonic()
    runner=SerialExecutor(OUT,d['total_wall_seconds'],'AAA',resource)
    result=dict(classification='FAILED_SAME_DATA_ODD_PROBE_NO_RETRY',error=None)
    try:
        runner.execute(OUT/'build','build',d['build_command'],d['stage_caps']['build'])
        runner.execute(OUT/'inputs','extract',[str(OUT/'runtime/extract')],d['stage_caps']['extract'],'AXMAT-RADIAL-COLLISION-INPUTS-COPIED')
        runner.execute(OUT,'prepare',[sys.executable,str(Path(__file__).resolve()),'prepare-sources'],d['stage_caps']['prepare'],'AXMAT-ODD-PROBE-SOURCES-READY')
        runner.execute(OUT/'inputs','primary',[str(OUT/'runtime/probe_signed'),'primary.txt','primary.bin'],d['stage_caps']['primary_flights'])
        runner.execute(OUT,'white-prepare',[sys.executable,str(Path(__file__).resolve()),'prepare-white'],d['stage_caps']['white_prepare'],'AXMAT-ODD-PROBE-WHITE-READY')
        runner.execute(OUT/'inputs','white',[str(OUT/'runtime/probe_signed'),'white.txt','white.bin'],d['stage_caps']['white_flights'])
        runner.execute(OUT,'analysis',[sys.executable,str(Path(__file__).resolve()),'analyze'],d['stage_caps']['analysis'],'AXMAT-NATIVE-ODD-RESPONSE-ANALYZED')
        result.update(classification='COMPLETE_BOUNDED_NATIVE_ODD_RESPONSE_DIAGNOSTIC_ONLY',ABA_admitted=False)
    except BaseException as error:result['error']=repr(error);raise
    finally:
        verify(d['files']);verify_sealed_directory(FINAL)
        result['resources']=resource.check();result['elapsed_seconds']=time.monotonic()-started
        write_new(OUT/'driver_result.json',result)
    write_new(OUT/'seal.json',dict(schema='AXMAT_NATIVE_ODD_RESPONSE_SEAL_V1',files={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file()}))
    print(json.dumps(read(OUT/'result.json'),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run','prepare-sources','prepare-white','analyze']);parser.add_argument('--sha256');a=parser.parse_args()
    {'prepare':prepare,'run':lambda:run(a.sha256),'prepare-sources':prepare_sources,'prepare-white':prepare_white,'analyze':analyze}[a.action]()

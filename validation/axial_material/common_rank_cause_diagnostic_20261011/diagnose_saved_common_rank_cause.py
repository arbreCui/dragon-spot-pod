"""One pure Python saved-data diagnostic, with no training/SVD/Native child.

Original 512 MiB / 600 s stage / 1800 s whole upper caps remain. This single
stage tightens whole execution to 600 s. Child creation is dynamically refused.
Original complete-history 96 GiB/free 8 GiB accounting is reused unmodified;
this user-requested metadata directory outside artifacts is added explicitly.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import stat
import struct
import sys
import time

ROOT=Path('/Users/wen/spot')
V=ROOT/'validation/axial_material'
ART=ROOT/'validation/artifacts'
OUT=V/'common_rank_cause_diagnostic_20261011'
REVIEW=ART/'axial-material-original-controls-new-AB-common-rank2-root-review-20261011-v1'
NEW=ART/'axial-material-original-controls-terminal-stability-rank2-20261011-v1-after-actual-reentry-output/archives'
OLD=ART/'axial-material-real64-common-rank2-training-20261011'
DIAG=ART/'axial-material-real64-rank2-saved-weak-direction-diagnostic-20261011-a3cdi73t'
ENV=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
GATE=9.5367431640625e-7
START=time.monotonic()

def budget(*_):
    raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    value=int(raw if sys.platform=='darwin' else raw*1024)
    if time.monotonic()-START>=600 or value>=512*2**20:
        raise RuntimeError('original pure review 600-second/512-MiB cap reached')
    return value

def audit(event,arguments):
    if event in ('subprocess.Popen','os.system','os.posix_spawn','os.posix_spawnp','os.fork','os.forkpty') or event.startswith('os.exec') or event.startswith('os.spawn'):
        raise RuntimeError('pure diagnostic cannot launch child')
    if event=='open':
        path,mode,flags=arguments
        writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing and (not isinstance(path,(str,bytes,os.PathLike)) or not Path(os.fsdecode(path)).absolute().is_relative_to(OUT)):
            raise RuntimeError('only new explicit diagnostic metadata may be written')

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path,expected=None):
    path=Path(path)
    for p in (path,*path.parents):
        if p.is_symlink():raise ValueError('no input alias: '+str(p))
    before=path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1:raise ValueError('regular single-link input required')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=identity(before):raise ValueError('opened identity differs')
        h=hashlib.sha256();n=0
        while True:
            block=os.read(fd,2**20)
            if not block:break
            n+=len(block);h.update(block);budget()
        if n!=before.st_size or identity(os.fstat(fd))!=identity(before):raise ValueError('full EOF/fd identity differs')
    finally:os.close(fd)
    if identity(path.lstat())!=identity(before):raise ValueError('entry changed')
    value={'path':str(path),'size_bytes':n,'sha256':h.hexdigest(),'identity':identity(before)}
    if expected is not None and value['sha256']!=expected:raise ValueError('saved authority SHA differs: '+str(path))
    return value

def load(p):return json.loads(Path(p).read_bytes())

def save(name,value):
    with (OUT/name).open('xb') as f:
        f.write((json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
    return pin(OUT/name)

def listdirs(a,d,name,count):
    offsets=struct.unpack('<'+str(count)+'i',a.record(d,name,count,10));ans=[]
    for o in offsets:
        item=a.directory(o);handle=item['***HANDLE***']
        if handle[1:]!=(-1,0):raise ValueError('directory-valued slot required')
        ans.append(a.directory(handle[0]))
    return ans

def fields(a,d,name,kind):
    offsets=struct.unpack('<370i',a.record(d,name,370,10))
    return [a.record(a.directory(o),'***HANDLE***',28 if kind==4 else 14,kind) for o in offsets]

def packed(path):
    with _open_xsm(path) as a:
        if struct.unpack('<i',a.record(a.root,'LISTDIM',1,1))[0]!=3:raise ValueError('three A/B/A slots required')
        tracks=listdirs(a,a.root,'TRACK',3);fluxes=listdirs(a,a.root,'FLUX',3)
        phi=[];mirror=[];raw=[];raw32=[];keys=[];vol=[];mats=[]
        for t,f in zip(tracks,fluxes):
            k=struct.unpack('<8i',a.record(t,'KEYFLX',8,1))
            if len(set(k))!=8 or any(x<1 or x>14 for x in k):raise ValueError('complete unique scalar keys required')
            v=a.record(t,'VOLUME',8,2);m=a.record(t,'MATCOD',8,1)
            z=fields(a,f,'FLUX64',4);z32=fields(a,f,'FLUX',2)
            full=[struct.unpack('<14d',x) for x in z];full32=[struct.unpack('<14f',x) for x in z32]
            for x,y,yraw in zip(full,full32,z32):
                if not all(math.isfinite(q) for q in (*x,*y)):raise ValueError('nonfinite full field')
                if struct.pack('<14f',*x)!=yraw:raise ValueError('mirror is not exact native demotion')
                if any(x[i-1]<=0 for i in k):raise ValueError('nonpositive scalar flux')
            phi.append([tuple(x[i-1] for i in k) for x in full]);mirror.append([tuple(x[i-1] for i in k) for x in full32])
            raw.append(z);raw32.append(z32);keys.append(k);vol.append(v);mats.append(m)
    if raw[0]!=raw[2] or raw32[0]!=raw32[2]:raise ValueError('repeated A fields differ')
    if len(set(vol))!=1 or len(set(mats))!=1 or len(set(keys))!=1:raise ValueError('shared original metric/maps differ')
    return {'phi':phi,'mirror':mirror,'raw':raw,'raw32':raw32,'keys':keys,'volume_raw':vol[0],'materials_raw':mats[0]}

def snapshot(path):
    with _open_xsm(path) as a:
        t=a.object('TRACK');f=a.object('FLUX');micro=a.object('MICROLIB2')
        return {'raw':fields(a,f,'FLUX64',4),'raw32':fields(a,f,'FLUX',2),'volume_raw':a.record(t,'VOLUME',8,2),
                'keys':struct.unpack('<8i',a.record(t,'KEYFLX',8,1)),'energy_raw':a.record(micro,'ENERGY',371,2)}

def dot(a,b):return math.fsum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(dot(a,a))
def shaped(p,w):
    mean=dot(p,w)
    if not mean>0 or not math.isfinite(mean):raise ValueError('invalid column mean')
    q=[x/mean for x in p];x=[math.sqrt(z)*y for z,y in zip(w,q)]
    return q,x,mean

def two_vectors(a,b,repeat=2):
    aa=dot(a,a);bb=dot(b,b);na=math.sqrt(aa);unit=[x/na for x in a]
    proj=dot(unit,b);orth=[y-proj*x for x,y in zip(unit,b)];rn=norm(orth)
    trace=repeat*aa+bb;det=repeat*aa*rn*rn
    root=math.sqrt(max(0.0,trace*trace-4.0*det));small=2.0*det/(trace+root)
    s1=math.sqrt(trace-small);s2=math.sqrt(small)
    return {'sigma1':s1,'sigma2':s2,'ratio':s2/s1,'orth':orth,'orthnorm':rn,'angle':math.atan2(rn,proj),'difference_norm':norm([y-x for x,y in zip(a,b)]),'A_norm':na}

def span(rows,key):return {'min':min(x[key] for x in rows),'max':max(x[key] for x in rows)}

def main():
    if not sys.dont_write_bytecode or sys.flags.optimize or any(os.environ.get(k)!='1' for k in ENV):raise ValueError('Python-B/no-O/five thread caps1 required')
    if {p.name for p in OUT.iterdir()}!={Path(__file__).name}:raise ValueError('fresh permanent attempt only; no retry/overwrite')
    sys.addaudithook(audit);signal.signal(signal.SIGALRM,budget);signal.setitimer(signal.ITIMER_REAL,.1,.1)
    sys.path.insert(0,str(V))
    global _open_xsm
    from snapshot_control_preflight import _open_xsm
    from moment_order_complete_history_resource_trie_20261010 import DynamicHistoryResources
    oldcfg=load(DIAG/'inputs.json')
    result=load(ART/'axial-material-original-controls-terminal-stability-rank2-20261011-v1-after-actual-reentry-host/result.json')
    receipt=load(result['new_terminal_receipt']['path'])
    declared=[str(REVIEW),str(NEW.parent),str(OLD),str(ART/'axial-material-real64-pod-runtime-build-20261011'),str(ART/'axmat-native-real64-warm-ingress-20261011')]
    resources=DynamicHistoryResources(ART,declared,8*2**30,96*2**30)
    def account():
        record=resources.check();size=sum(x.stat().st_size for x in OUT.iterdir() if x.is_file())
        if size>=2*2**30 or record['artifact_bytes']+size>96*2**30 or record['disk_free_bytes']-size<8*2**30:raise ValueError('original history/free plus supplemental metadata output cap')
        return {'original_complete_history_guard':record,'supplemental_requested_metadata_bytes':size,'actual_SELF_peak_bytes':budget()}
    before_resources=account()
    selected=[(REVIEW/'REPORT.txt','0155c767f20826fd023e102f7f2ae523e54312604b4e6a2e940ebe79adfb2b65'),
              (REVIEW/'rank_admission_actual_original_gate.json','04bd1b9e2cceb40c2fa9ac97c15634b0c798b8ac57bae67a57bd66724eb1d593'),
              (REVIEW/'all370_sigma_ratio_original_vs_new.json','8f97b5616e8fcf3faaf6bf5b21b57eb4f193e39738eb894ebe157673b923b84c'),
              (ART/'axial-material-original-controls-terminal-stability-rank2-20261011-v1-after-actual-reentry-host/result.json','0d067b9b0cb89e534ad9fb133c930ecfcdbdd5ada9bc7aa5dd799bdf1f3eeac7'),
              (DIAG/'inputs.json','2891b5e81ae3ce40d7333b103aba858acf9241fbe098736f09e52e4705395cd7')]
    selected+=[(Path(x['path']),x['sha256']) for x in result['all_actual_archive_stage_files'] if Path(x['path']).name in ['training_snapshots.xsm','snapshot_A.xsm','snapshot_B.xsm','common_basis.xsm','common_basis.x2m','rank_precision.x2m']]
    selected.append((Path(result['new_terminal_receipt']['path']),result['new_terminal_receipt']['sha256']))
    for s in receipt['states'].values():selected.append((Path(s['archive']['path']),s['archive']['sha256']))
    for p in [OLD/'archives/training_snapshots.xsm',OLD/'training/common_basis.xsm',OLD/'training/rank_admission_saved_replay.json']:
        selected.append((p,oldcfg['full_input_sha256'][str(p)]))
    for p in [V/'run_real64_common_rank2_training.py',V/'production_runner.py',V/'snapshot_control_preflight.py',V/'moment_order_complete_history_resource_trie_20261010.py',V/'case_spec.json',V/'case_spec_rank_addendum.json',
              ART/'axial-material-real64-pod-runtime-build-20261011/actual_executed_source/SPOPOD.f90',ART/'axial-material-real64-pod-runtime-build-20261011/actual_executed_source/SPOASM.f',
              ART/'axmat-native-real64-warm-ingress-20261011/Root_actual_compile_only_summary.json',Path(__file__).absolute()]:selected.append((p,None))
    selected=list(dict((str(p),expected) for p,expected in selected).items())
    inputs_before=[pin(p,expected) for p,expected in selected]
    saved=load(REVIEW/'rank_admission_actual_original_gate.json');comparison=load(REVIEW/'all370_sigma_ratio_original_vs_new.json')
    if saved['sigma2_over_sigma1_strict_min']!=GATE or saved['requested_rank']!=2 or len(saved['groups'])!=370:raise ValueError('original gate/rank/full370 required')
    data=packed(NEW/'training_snapshots.xsm');old=packed(OLD/'archives/training_snapshots.xsm')
    if (data['volume_raw'],data['materials_raw'],data['keys'])!=(old['volume_raw'],old['materials_raw'],old['keys']):raise ValueError('old/new metric/maps differ')
    source=[]
    for slot,letter in enumerate(('A','B','A')):
        s=snapshot(NEW/f'snapshot_{letter}.xsm');original=snapshot(receipt['states'][letter]['archive']['path'])
        if s!=original or data['raw'][slot]!=s['raw'] or data['raw32'][slot]!=s['raw32'] or data['volume_raw']!=s['volume_raw'] or data['keys'][slot]!=s['keys']:raise ValueError('actual packed/producer complete native inputs differ')
        source.append(s)
    if source[0]['energy_raw']!=source[1]['energy_raw']:raise ValueError('A/B energy grids differ')
    energy=struct.unpack('<371f',source[0]['energy_raw']);vol=list(struct.unpack('<8f',data['volume_raw']))
    if not all(math.isfinite(x) and x>0 for x in vol):raise ValueError('original positive volume required')
    total=math.fsum(vol);weights=[x/total for x in vol]
    with _open_xsm(NEW/'common_basis.xsm') as a:
        if struct.unpack('<i',a.record(a.root,'POD-INPUT-TY',1,1))[0]!=4 or a.record(a.root,'POD-IN-SRC',3,3).decode().rstrip(' \0')!='ROOT-FLUX64':raise ValueError('native actual origin differs')
        rawsig=struct.unpack('<1110d',a.record(a.root,'POD-SIGMA-G',2220,4));ranks=struct.unpack('<370i',a.record(a.root,'POD-RANK-G',370,1))
    rows=[]
    for g in range(370):
        budget();qa,a,ma=shaped(data['phi'][0][g],weights);qb,b,mb=shaped(data['phi'][1][g],weights)
        _,ar,_=shaped(data['mirror'][0][g],weights);_,br,_=shaped(data['mirror'][1][g],weights)
        _,ao,_=shaped(old['phi'][0][g],weights);_,bo,_=shaped(old['phi'][1][g],weights)
        pair=two_vectors(a,b,1);aba=two_vectors(a,b,2);rounding=two_vectors(ar,br,2)
        sig=list(rawsig[3*g:3*g+3]);printed=saved['groups'][g]
        tol=64*8*sys.float_info.epsilon*sig[0]
        if ranks[g]!=2 or any(abs(sig[i]-printed['sigma'][i])>2e-15*sig[i]+2e-30 for i in range(3)):raise ValueError('complete saved spectrum mismatch')
        if max(abs(aba['sigma1']-sig[0]),abs(aba['sigma2']-sig[1]))>tol:raise ValueError('analytic duplicate-column spectrum disagrees with saved actual SVD')
        original=comparison['groups'][g]
        if printed['pass']!=(sig[1]>GATE*sig[0]) or abs(original['new_sigma2_over_sigma1']-sig[1]/sig[0])>2e-15*sig[1]/sig[0]+2e-30:raise ValueError('original actual decision differs')
        delta=[y-x for x,y in zip(a,b)];delta32=[y-x for x,y in zip(ar,br)]
        perturb=math.sqrt(2*norm([x-y for x,y in zip(a,ao)])**2+norm([x-y for x,y in zip(b,bo)])**2)
        contributions=[weights[i]*(qb[i]-qa[i])**2 for i in range(8)];cscale=math.fsum(contributions)
        rows.append({'group':g+1,'energy_high_eV':energy[g],'energy_low_eV':energy[g+1],'actual_sigma':sig,'sigma2_over_sigma1':sig[1]/sig[0],
          'original_gate_pass':printed['pass'],'sigma2_over_gate_floor':sig[1]/(GATE*sig[0]),'remaining_ratio_gap':GATE-sig[1]/sig[0],
          'second_direction_to_binary64_algorithm_tolerance':sig[1]/(8*sys.float_info.epsilon*sig[0]),'weighted_AB_angle_rad':aba['angle'],
          'weighted_AB_difference_norm':aba['difference_norm'],'weighted_AB_orthogonal_norm':aba['orthnorm'],
          'weighted_AB_relative_difference':aba['difference_norm']/aba['A_norm'],'weighted_AB_means':[ma,mb],
          'raw_B_over_A_mean':mb/ma,'normalized_AB_shapes':[qa,qb],'weighted_difference_contribution_fraction':[x/cscale for x in contributions],
          'analytic_ABA_sigma':[aba['sigma1'],aba['sigma2'],0.0],'analytic_vs_saved_sigma_max_abs_error':max(abs(aba['sigma1']-sig[0]),abs(aba['sigma2']-sig[1])),
          'two_unique_columns_AB_ratio_diagnostic_only':pair['ratio'],'AB_ratio_over_ABA_ratio':pair['ratio']/aba['ratio'],
          'two_unique_columns_AB_original_gate_shadow_pass':pair['ratio']>GATE,
          'same_state_REAL32_mirror_analytic_ratio':rounding['ratio'],'same_state_REAL32_mirror_ratio_over_native':rounding['ratio']/aba['ratio'],
          'same_state_REAL32_difference_error_over_native_direction':norm([x-y for x,y in zip(delta32,delta)])/norm(delta),
          'old_to_new_original_actual_ratio_change':original['actual_ratio_change'],'old_to_new_normalized_matrix_Frobenius_perturbation':perturb,
          'necessary_spectral_matrix_perturbation_for_gate_with_moving_sigma1_bound':max(0.0,(GATE*sig[0]-sig[1])/(1.0+GATE)),
          'failed_gap_to_observed_ratio_change':(GATE-sig[1]/sig[0])/abs(original['actual_ratio_change']) if original['actual_ratio_change'] and not printed['pass'] else None})
    failed=[x['group'] for x in rows if not x['original_gate_pass']]
    if failed!=list(range(1,18)):raise ValueError('original failed groups changed')
    first=rows[:17];summary={k:span(first,k) for k in ['sigma2_over_sigma1','sigma2_over_gate_floor','second_direction_to_binary64_algorithm_tolerance','weighted_AB_angle_rad','weighted_AB_relative_difference','AB_ratio_over_ABA_ratio','same_state_REAL32_difference_error_over_native_direction','same_state_REAL32_mirror_ratio_over_native','remaining_ratio_gap','old_to_new_normalized_matrix_Frobenius_perturbation','necessary_spectral_matrix_perturbation_for_gate_with_moving_sigma1_bound','failed_gap_to_observed_ratio_change']}
    inputs_after=[pin(x['path'],x['sha256']) for x in inputs_before]
    if inputs_before!=inputs_after:raise ValueError('current full EOF/SHA/7IDs changed')
    report={'schema':'spot_actual_saved_common_rank_cause_diagnostic_v1','classification':'SAVED_INPUT_CAUSE_RANGE_DIAGNOSTIC_ONLY',
      'scope':'Current once-reentered same-control A/B/A saved native fields; independent stable two-vector analytic identities only. No SVD call, new training, snapshot choice, threshold/rank/weight change, compile, transport or Native child.',
      'caps':{'SELF_rss_mib':512,'single_stage_seconds':600,'whole_upper_seconds':1800,'effective_one_stage_whole_seconds':600,'threads_configured':1,'automatic_retries':0,'business_children_started':0},
      'original_guard_reused':'Unmodified DynamicHistoryResources complete-history96GiB/free8GiB; original pure Root review no-child/write-scope audit and recurring SELF budget policy retained; user-requested metadata output separately counted.',
      'current_input_fullEOF_pins_before_after':inputs_before,'current_input_fullEOF_pins_unchanged':True,'historical_7ID_scope':'Historical files were pinned on a prior device namespace; current full SHA is matched and current exact 7IDs are measured before/after. Historical device/inode equality is not claimed.',
      'layout':{'group_count':370,'full_unknowns_per_snapshot_group':14,'radial_scalar_rows':8,'columns':['A','B','A'],'Fortran_PHI_layout':'NREG2D,NSNAP,NGRP; each group is 8x3; saved POD-SIGMA-G is NSNAP,NGRP and three contiguous real64 values per group.',
                'actual_scalar_KEYS':data['keys'],'actual_MATCOD':list(struct.unpack('<8i',data['materials_raw'])),'all370_full_native_producer_copy_to_pack_bits_match':True,'all370_type2_mirrors_exact_native_demotions':True,'duplicate_A_all370_full_14_fields_bitexact':True},
      'volume_and_normalization':{'original_VOLUME_real32_bytes_sha256':hashlib.sha256(data['volume_raw']).hexdigest(),'volume':vol,'total_volume':total,'weights':weights,'all3_and_old_new_VOLUME_keys_materials_bitexact':True,'algorithm':'w=V/sum(V); each column phi divided by sum(w*phi); X=sqrt(w)*shape. Raw scalar amplitude differences are intentionally removed by the original algorithm. Diagnostic fsum may differ at roundoff from native reduction; agreement bound is reported.'},
      'stable_analytic_identity':'For X=[a,b,a], decompose b onto a and an orthogonal residual r. trace=2*||a||^2+||b||^2; determinant=2*||a||^2*||r||^2. lambda2=2*det/(trace+sqrt(trace^2-4*det)); no subtracting nearly equal eigenvalues and no SVD/training.',
      'maximum_analytic_vs_actual_saved_sigma_absolute_error':max(x['analytic_vs_saved_sigma_max_abs_error'] for x in rows),
      'original_gate':GATE,'original_pass_count':353,'original_failed_groups':failed,'all_two_unique_AB_shadow_failed_groups':[x['group'] for x in rows if not x['two_unique_columns_AB_original_gate_shadow_pass']],
      'failed_energy_span_eV':[energy[17],energy[0]],'first17_summary':summary,'closest_group15':rows[14],'first_passing_group18':rows[17],'all370_groups':rows,
      'deductions':['The first17 nonzero second directions are far above the original binary64 numerical-rank tolerance, yet below the unchanged conservative 8*epsilon(REAL32) admission gate. They are resolved in saved double data but are not admitted by this model contract.',
                    'Current full layout, scalar extraction, volume metric, independent column normalization, producer-to-pack transfer and repeated A are checked directly. Their implementation corruption is excluded for these saved inputs.',
                    'The A/B/A duplicate creates no third independent direction. Removing that repetition in a shadow analytic diagnostic changes weighting mildly and does not make any of the original failed17 pass; this is not a changed training basis or new admission.',
                    'Observed same-control re-entry changes are much smaller than each failed gate gap. Wiring double arrays alone cannot enlarge the span of these already preserved saved columns. A later fresh complete global computation can change physical fields; its outcome is not predicted or qualified here.',
                    'The failed groups are high-energy bins. Normalized A/B radial shape contrasts in them are extremely small. This identifies the saved-input cause range, not a proof that exact transport solutions have the same tiny contrast or that their observable importance is negligible.'],
      'limitations':['No independent transport error bound or conditioned residual-to-flux bound is available here. Nonzero stored second directions could include producer iteration/discretization error. Tiny same-control re-entry differences are reproducibility evidence, not an a posteriori error bound.',
                    'The original basis and coefficient outputs in SPOPOD64 remain REAL32; continuous double flux/B1 wiring by itself does not replace the conservative original rank gate or fully change that basis representation.',
                    'High-energy classification comes from saved ENERGY bits; reaction/response importance and physics accuracy are not inferred from rank spectra alone. No new material-processing result is created.',
                    'The old private temporary input-eligibility receipt path named in the historical host result is absent. Actual copied snapshots, their present producer terminal receipt, packed archive and current source bytes are independently pinned; no new current qualification of that missing historical prerequisite is claimed.'],
      'next_discriminating_scientific_check':'Under the same frozen states/geometry/material/library and unchanged gates, obtain an independent groupwise residual-to-flux or higher-accuracy same-operator reference bound on the A/B shape contrast, normalized with the original weights. Compare this bound directly with the observed orthogonal direction and minimum gate-crossing perturbation; also obtain same-origin reaction/response weights to judge the failed fast-bin importance. Predeclare any actual new solve separately; do not select replacement snapshots from the observed spectrum.',
      'new_training_executed':False,'new_SVD_executed':False,'transport_executed':False,'common_rank2_admitted':False,'scientific_qualification':False,'AAA_qualified':False,'ABA_admitted':False,'goal_complete':False,
      'resources_before':before_resources,'resources_before_report':account(),'elapsed_seconds_before_report':time.monotonic()-START,'actual_SELF_peak_bytes':budget(),'actual_native_threads_measured':False}
    report_pin=save('REPORT.json',report)
    text=('当前一次同控制新 A/B 共同 rank2 的保存数据诊断\n\n'
          '370 个 8×3 体积加权、逐列归一化矩阵已核对，完整 14 元素 type4 字段及 type2 镜像与生产副本逐位相同；重复 A 完全相同。原权重、映射和训练门均未改变。\n'
          f'原结果仍为353通过、1–17群失败；这些群能量覆盖{energy[17]/1e6:.6g}–{energy[0]/1e6:.6g} MeV。稳定两向量解析式与实际保存 SVD 的最大绝对差为{report["maximum_analytic_vs_actual_saved_sigma_absolute_error"]:.6g}。\n'
          f'前17群第二方向/原门槛为{summary["sigma2_over_gate_floor"]["min"]:.6g}–{summary["sigma2_over_gate_floor"]["max"]:.6g}；它们高于double数值rank容差{summary["second_direction_to_binary64_algorithm_tolerance"]["min"]:.6g}–{summary["second_direction_to_binary64_algorithm_tolerance"]["max"]:.6g}倍，仍未满足原保守准入。\n'
          f'去掉重复A的影子解析对照使比值约增{summary["AB_ratio_over_ABA_ratio"]["min"]:.6g}–{summary["AB_ratio_over_ABA_ratio"]["max"]:.6g}倍；原17群仍全部失败，未实际改训。\n'
          f'g15 ratio={rows[14]["sigma2_over_sigma1"]:.17g}，剩余gap={rows[14]["remaining_ratio_gap"]:.17g}，是同控制重入已观测ratio变化的{rows[14]["failed_gap_to_observed_ratio_change"]:.6g}倍。\n'
          '连续double接线不能单凭保存精度增加现有训练列的独立形状信息。可排除当前布局/映射/原权重/复制破坏，但尚不能排除生产求解误差，也不授物理资格。下一步应对同冻结算子的A/B归一化形状差取得独立误差界，再用同源反应权重判断快群的重要性。\n')
    with (OUT/'REPORT.txt').open('xb') as f:f.write(text.encode())
    witness=save('ACTUAL_DIAGNOSTIC_CLOSEOUT.json',{'report':report_pin,'text_report':pin(OUT/'REPORT.txt'),'resources_after_saved_report':account(),'elapsed_seconds':time.monotonic()-START,'actual_SELF_peak_bytes':budget(),'business_children_started':0,'no_retry':True,'current_fullEOF_pins_unchanged':True,'no_scientific_qualification':True})
    print(json.dumps({'report_pin':report_pin,'closeout_pin':witness,'first17_summary':summary,'g15_ratio':rows[14]['sigma2_over_sigma1'],'g15_gap_to_observed_change':rows[14]['failed_gap_to_observed_ratio_change'],'analytic_max_abs_error':report['maximum_analytic_vs_actual_saved_sigma_absolute_error'],'failed_shadow_AB':[x['group'] for x in rows if not x['two_unique_columns_AB_original_gate_shadow_pass']],'actual_SELF_peak_bytes':budget(),'elapsed_seconds':time.monotonic()-START,'business_children_started':0,'new_training_or_transport_or_SVD':False},ensure_ascii=False))
    signal.setitimer(signal.ITIMER_REAL,0)

if __name__=='__main__':main()

"""Bounded closeout for the declared full long-generation AAA reference.

Every scientific state is copied from the original-threshold analyses. This
report and its plots neither refit profiles nor admit a failed AAA to ABA.
"""
import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode=True
import frozen_AAA_axial_sensitivities as base

ROOT,ART,PROD=base.ROOT,base.ART,base.PROD
CE=ART / 'axial-material-ce-qualified-AAA-long-generations-20261004'
OUT=ART / 'axial-material-AAA-long-generations-closeout-20261004'
OBS=ART / 'axial-material-qualified-AAA-observables-20261004'
PRIOR=[('Original CE, 1 generation/batch',ART / 'axial-material-ce-qualified-AB-compensated-20261004'),
       ('Weighted UFS CE, 1 generation/batch',ART / 'axial-material-ce-qualified-AAA-ufs-20261004')]
CE_SHA='ac11a8edc48d0a288a41a37fe0f0c7ebdbec66317d49c63203f18e37c75337c6'
ANALYSIS_SHA='10f8d9aba24d8f85827436e3143fd25e2378e9c553b7607d30e8e0823600114f'


def prepare():
    base.prepared()
    base.require_file(CE / 'AAA/execution.json',CE_SHA)
    base.require_file(CE / 'analysis_collection_declaration_v2.json',ANALYSIS_SHA)
    OUT.mkdir(exist_ok=False)
    for name in ('runtime','AAA','source_record'):(OUT / name).mkdir()
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py',OUT / 'runtime/run_bounded_dragon.py')
    files=[Path(__file__).resolve(),Path(base.__file__),Path(sys.executable).resolve(),
        PROD / 'prepared.json',PROD / 'AAA/run_status.json',PROD / 'runtime/production_runner.py',
        OUT / 'runtime/run_bounded_dragon.py',CE / 'AAA/execution.json',CE / 'AAA/run_claim.json',
        CE / 'declaration.json',CE / 'input_sampling_review.json',CE / 'resource_addendum.json',
        CE / 'smoke_activation_receipt.json',CE / 'analysis_collection_declaration_v2.json',
        CE / 'analysis_preparation_path_rejection.json',CE / 'input_equivalence_AAA.json',
        *[OBS / ('observables.'+suffix) for suffix in ('summary.txt','regions.csv','faces.csv')],
        *[r / ('AAA/'+name) for _,r in PRIOR for name in ('statistics.json','reference_assessment.json','reference_contract.json')]]
    base.write_new(OUT / 'declaration.json',dict(schema='AXMAT_LONG_GENERATIONS_AAA_CLOSEOUT_V1',declared_unix=time.time(),
        files={str(p.resolve()):base.digest(p) for p in files},ce_manifest_sha256=CE_SHA,
        analysis_collection_sha256=ANALYSIS_SHA,wall_seconds=120,threads=1,retries=0,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        min_free_bytes=8*2**30,artifact_budget_bytes=24*2**30,
        source_gate='Only complete native rc0 and complete v2 reference analysis. Both current analyses must pin exactly all 250 active statepoints. Actual ABA guard tested against the final original-rule assessment.',
        figures='Fuel nu-fission by axial cell uses explicit sorted (radial region, axial cell) mapping and one global normalization. Source lag axis uses declared batches; labels distinguish generation counts. Means are diagnostic profiles, never confidence bands.',
        success='Verified report, complete input/output pins, all 3500 raw generation histories retained and exact consecutive ten-to-one batch means. Actual original-rule AAA classification is unchanged. PNG requires subsequent visual inspection.',
        engineering_thresholds_changed=False,goal_complete=False,shared_solver_promoted=False))
    print(json.dumps(dict(status='PREPARED_PENDING_FULL_REFERENCE_ANALYSIS',declaration=base.pin(OUT / 'declaration.json')),indent=2))


def check(expected):
    base.require_file(OUT / 'declaration.json',expected)
    declaration=json.loads((OUT / 'declaration.json').read_text())
    for name,sha in declaration['files'].items():base.require_file(Path(name),sha)
    native=json.loads((CE / 'AAA/native_result.json').read_text())
    analysis=json.loads((CE / 'AAA/analysis_result.json').read_text())
    if native['returncode']!=0 or native['error'] is not None or analysis['classification']!='COMPLETE_REFERENCE_ANALYSIS':
        raise ValueError('complete native and v2 analysis required')
    base.require_file(CE / 'AAA/reference_assessment.json',analysis['reference_assessment_sha256'])
    return declaration,native,analysis


def summarize(stats):
    blocks=[]
    for row in stats['block_reports']:
        checks=row['source_stationarity']['checks']
        blocks.append(dict(batches=row['block_length'],blocks=row['blocks'],
            failed_channels=[name for name,v in checks.items() if not v['passed']],
            max_abs_lag1=max(abs(v['lag1']) for v in checks.values()),
            reference_only_error_upper_95=row['reference_only_error_upper_95'],resolution_passed=row['resolution_passed']))
    return dict(classification=stats['classification'],checks=stats['checks'],k=stats['k'],
        point_discrepancies=stats['point_discrepancies'],conservative_upper_95=stats['conservative_upper_95'],
        conservative_lower_05=stats['conservative_lower_05'],inconclusive_reasons=stats['inconclusive_reasons'],
        history_bridges=stats['history_bridges'],blocks=blocks)


def child(expected):
    declaration,native,analysis=check(expected)
    import numpy as np
    os.environ.setdefault('MPLCONFIGDIR',str(OUT / 'runtime/mpl_cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    assessment_path=CE / 'AAA/reference_assessment.json'
    assessment=json.loads(assessment_path.read_text())
    current=json.loads((CE / 'AAA/statistics.json').read_text())
    currents=json.loads((CE / 'AAA/currents_balance_symmetry.json').read_text())
    for report in (current,currents):
        if len(report['statepoint_identities'])!=250:raise ValueError('incomplete active reference')
        if sorted(int(Path(v['path']).name.split('.')[1]) for v in report['statepoint_identities'])!=list(range(101,351)):
            raise ValueError('wrong active batches')
        for name,sha in report['input_identities'].items():base.require_file(Path(name),sha)
        for item in report['statepoint_identities']:base.require_file(Path(item['path']),item['sha256'])
    for item in assessment['evidence'].values():base.require_file(Path(item['path']),item['sha256'])
    history=current['source_generation_history']
    for raw_key,batch_key in [('raw_k_generation','k_generation'),('raw_entropy','entropy')]:
        raw=np.asarray(history[raw_key],float);batch=np.asarray(history[batch_key],float)
        if raw.shape!=(3500,) or batch.shape!=(350,) or not np.isfinite(raw).all() or not np.array_equal(raw.reshape(350,10).mean(axis=1),batch):
            raise ValueError('declared complete generation history differs')
    info,_=base.prepared()
    from production_runner import qualify_aba,Refusal
    if assessment['ABA_admitted']:
        qualification=CE / 'AAA/reference_qualification.json'
        admitted=qualify_aba(info,PROD,base.SHA,qualification,base.digest(qualification))
        guard=dict(status='PASS_ACTUAL_ABA_GUARD_ADMITS_QUALIFIED_AAA',qualification=admitted,ABA_started=False)
    else:
        try:qualify_aba(info,PROD,base.SHA,assessment_path,base.digest(assessment_path))
        except Refusal as error:guard=dict(status='PASS_ACTUAL_ABA_GUARD_REJECTS_UNQUALIFIED_AAA',message=str(error),ABA_started=False)
        else:raise ValueError('actual ABA guard admitted unqualified assessment')
        if (PROD / 'ABA/run_claim.json').exists():raise ValueError('ABA started from unqualified AAA')
    guard.update(assessment=base.pin(assessment_path),runtime=base.pin(PROD / 'runtime/production_runner.py'),goal_complete=False)
    base.write_new(OUT / 'aba_guard.json',guard)
    references=[(label,json.loads((r / 'AAA/statistics.json').read_text()),r) for label,r in PRIOR]
    references.append(('Ordinary CE, 10 generations/batch',current,CE))
    rows=list(csv.DictReader((OBS / 'observables.regions.csv').open()))
    keys=sorted((int(r['radial_region']),int(r['axial_cell'])) for r in rows)
    if len(keys)!=96 or len(set(keys))!=96:raise ValueError('incomplete production plotting grid')
    production=[sum(float(r['nufission_fraction']) for r in rows if int(r['axial_cell'])==z and int(r['radial_region']) in (4,5,6,7)) for z in range(1,13)]
    profiles={}
    for label,stats,folder in references:
        contract=json.loads((folder / 'AAA/reference_contract.json').read_text());mapped={key:[] for key in keys}
        for row in contract['region_layer_bins']:mapped[(row['region'],row['production_axial_cell'])].append(row)
        if any(len(v)!=1 for v in mapped.values()):raise ValueError('nonunique reference plotting grid')
        order=[mapped[key][0] for key in keys]
        values=[sum(stats['reference_nufission_fraction'][i] for i,row in enumerate(order) if row['region'] in (4,5,6,7) and row['production_axial_cell']==z) for z in range(1,13)]
        if abs(sum(values)-1)>1e-12:raise ValueError('reference profile global normalization changed')
        profiles[label]=values
    if abs(sum(production)-1)>1e-12:raise ValueError('production global normalization changed')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(12,8.5));z=np.arange(6.25,150,12.5)
    axes[0,0].plot(z,production,'o-',label='SPOT saved REAL64')
    colors=['#ad793c','#367c99','#8b4b95']
    for index,(label,stats,folder) in enumerate(references):
        axes[0,0].plot(z,profiles[label],'s--',label=label,color=colors[index])
        s=summarize(stats)
        axes[0,1].plot([5,10],[b['max_abs_lag1'] for b in s['blocks']],'o-',label=label,color=colors[index])
        axes[1,0].plot(np.linspace(0,150,13),stats['currents']['net_plus_z_per_nufission'],'o-',label=label,color=colors[index])
        axes[1,1].errorbar(index,stats['k']['reactivity_difference_pcm'],yerr=3*stats['k']['sigma_pcm'],fmt='o',color=colors[index],capsize=5)
    axes[0,0].set(title='Fuel nu-fission per axial cell',xlabel='z (cm)',ylabel='Fraction of global nu-fission');axes[0,0].legend(fontsize=7)
    axes[0,1].axhline(.5,color='#555',linestyle='--',label='Original lag gate')
    axes[0,1].set(title='Largest source-proxy block correlation',xlabel='Declared batches per block',ylabel='Absolute lag-one correlation',xticks=[5,10]);axes[0,1].legend(fontsize=7)
    faces=list(csv.DictReader((OBS / 'observables.faces.csv').open()))
    pcurrent=[sum(float(r['current_per_global_nufission']) for r in faces if int(r['face'])==i) for i in range(13)]
    axes[1,0].plot(np.linspace(0,150,13),pcurrent,'o-',label='SPOT saved REAL64')
    axes[1,0].set(title='Signed axial current',xlabel='z (cm)',ylabel='Net +z current / global nu-fission');axes[1,0].legend(fontsize=7)
    axes[1,1].axhspan(-500,500,color='#777',alpha=.12)
    axes[1,1].set(title='SPOT minus CE reactivity',ylabel='pcm; bars: 3 statistical sigma',xticks=[0,1,2],xticklabels=['Original','UFS','Long generations'])
    for a in axes.flat:a.grid(axis='y',alpha=.18)
    fig.suptitle('AAA long-generation reference: '+assessment['classification'].replace('_',' '),fontsize=13)
    fig.text(.06,.02,'All original numerical gates retained. Curves are sample means, not pointwise confidence bands.\nBatch histories contain different numbers of generations. Source proxies and current telescoping do not certify full neutron balance.',fontsize=8)
    fig.tight_layout(rect=(0,.07,1,.94));fig.savefig(OUT / 'comparison.png',dpi=180);fig.savefig(OUT / 'comparison.svg');plt.close(fig)
    evidence=[CE / 'AAA/native_result.json',CE / 'AAA/analysis_result.json',CE / 'AAA/analysis_execution.json',
        CE / 'AAA/statistics.json',CE / 'AAA/currents_balance_symmetry.json',assessment_path,
        CE / 'AAA/measurement_admission.json',CE / 'AAA/reference_contract.json',OUT / 'aba_guard.json']
    verification=dict(schema='AXMAT_LONG_GENERATIONS_AAA_CLOSEOUT_RESULT_V1',classification=assessment['classification'],
        current=summarize(current),previous={label:summarize(stats) for label,stats,_ in references[:-1]},
        full_source_generations=3500,batches=350,active_batches=250,generations_per_batch=10,
        physical_inputs_changed=False,sampling_protocol_changed=True,original_thresholds_changed=False,
        ABA_admitted=assessment['ABA_admitted'],ABA_started=False,goal_complete=False,shared_solver_promoted=False,
        figure_mapping='Explicit sorted radial-region/axial-cell keys; each fuel profile sums to one global nu-fission fraction.',
        visual_inspection='PENDING_SEPARATE_IMAGE_INSPECTION',input_records={str(p):base.digest(p) for p in evidence})
    base.write_new(OUT / 'verification.json',verification)
    lines=['2026-10-04：AAA 长源历史独立参考','','同温 A/B 快照及 AAA 数值固定点保留；完整材料对照 goal 尚未完成。',
        '判定：'+assessment['classification'],'ABA：'+('已取得原准入门槛；尚未启动。' if assessment['ABA_admitted'] else '未准入，未启动。'),'',
        '普通独立特征值采样，10000 粒子/代，10 代/批，100 批预热 + 250 批统计。全部 3500 代原始 k/熵历史保留。',
        '物理输入及每个数值验收门槛不变；采样协议与历史聚合方式显式改变。没有按层、按群拟合或归一化。',
        f'完整运行耗时 {native["elapsed_seconds"]:.3f} 秒；单线程，单次执行。','']
    for label,stats,_ in references:
        s=summarize(stats);k=s['k']
        lines += [label+': '+stats['classification'],f'  k={k["reference"]:.12f} +/- {k["sigma_k"]:.9f}；差异 {k["reactivity_difference_pcm"]:.3f} pcm；原额度 {k["allowance_pcm"]:.3f} pcm。',
            f'  通量 L2 点估计/95%上限：{s["point_discrepancies"][0]*100:.4f}% / {s["conservative_upper_95"][0]*100:.4f}%；原目标 1%。',
            f'  燃料 nu-fission 最大相对差异点估计/95%上限：{s["point_discrepancies"][1]*100:.4f}% / {s["conservative_upper_95"][1]*100:.4f}%；原目标 3%。',
            '  未确认项：'+(', '.join(s['inconclusive_reasons']) or '无')]
        for b in s['blocks']:lines.append(f'  {b["batches"]} 批区块：源代理未通过 {len(b["failed_channels"])} 项；最大相邻相关 {b["max_abs_lag1"]:.6f}；参考分辨率 '+('PASS' if b['resolution_passed'] else '未确认'))
        for name,b in s['history_bridges'].items():lines.append(f'  预热/有效统计桥接 {name}: '+('PASS' if b['passed'] else '未通过')+f'；Welch z={b["welch_z"]:.6f}。')
    lines += ['','本轮全部验收：',*[f'  {k}: {v}' for k,v in assessment['checks'].items()],'',
        '源历史或分辨率未确认时，形状差异仍只能作诊断；即便统计项通过，物理精度失败也不能放行 ABA。',
        '电流符号及端面账目不等同于完整吸收/源项中子平衡；没有独立吸收测量。',
        '保持原目标：解决 AAA 尚未通过的项，取得独立准入后再执行 ABA。白反射角度模型诊断属于另一个已声明的近似模型，不由本报告准入。',
        'comparison.png 使用实际保存的均值和已核对映射。图片的视觉核验单独记录；原失败记录保留。']
    with (OUT / 'REPORT.txt').open('x') as f:f.write('\n'.join(lines)+'\n')
    shutil.copy2(Path(__file__),OUT / 'source_record' / Path(__file__).name)
    shutil.copy2(CE / 'runtime/assess_qualified_AAA_reference_long_generations_v2.py',OUT / 'source_record/collector.py')
    shutil.copy2(CE / 'runtime/reference_statistics.py',OUT / 'source_record/reference_statistics.py')
    with (OUT / 'report.sha256').open('x') as f:
        for p in sorted(OUT.rglob('*')):
            if p.is_file() and p.name not in ('report.sha256','stages.json') and p.suffix!='.log' and 'mpl_cache' not in p.parts:
                f.write(f'{base.digest(p)}  {p.relative_to(OUT)}\n')
    for line in (OUT / 'report.sha256').read_text().splitlines():
        wanted,name=line.split('  ',1);base.require_file(OUT / name,wanted)
    print('AXMAT-LONG-GENERATIONS-CLOSEOUT-COMPLETE')


def run(expected):
    declaration,_,_=check(expected)
    if (OUT / 'run_claim.json').exists():raise ValueError('no repeat or retry')
    base.write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    resources=base.DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    runner=base.SerialExecutor(OUT,120,'AAA',resources)
    runner.execute(OUT / 'AAA','closeout',[sys.executable,str(Path(__file__).resolve()),'child','--sha256',expected],120,'AXMAT-LONG-GENERATIONS-CLOSEOUT-COMPLETE')
    for name,sha in declaration['files'].items():base.require_file(Path(name),sha)
    base.write_new(OUT / 'driver_result.json',dict(status='COMPLETE_BOUNDED_REFERENCE_REPORT',declaration_sha256=expected,
        verification=base.pin(OUT / 'verification.json'),report_seal=base.pin(OUT / 'report.sha256'),resources=resources.check(),
        visual_inspection='PENDING_SEPARATE_IMAGE_INSPECTION',goal_complete=False))
    print(json.dumps(dict(status='COMPLETE_BOUNDED_REFERENCE_REPORT',report=str(OUT / 'REPORT.txt')),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run','child'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else (run(args.sha256) if args.action=='run' else child(args.sha256))

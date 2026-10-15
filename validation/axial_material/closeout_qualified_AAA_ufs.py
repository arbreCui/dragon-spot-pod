"""Seal UFS and auxiliary AAA diagnoses without relabeling scientific failures."""
import csv
import hashlib
import json
from pathlib import Path
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'validation/artifacts'
CE=ART/'axial-material-ce-qualified-AAA-ufs-20261004'
PARENT=ART/'axial-material-ce-qualified-AB-compensated-20261004'
OUT=ART/'axial-material-AAA-ufs-closeout-20261004'
TOOLS=ROOT/'validation/axial_material'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write_new(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')


def summary(stats):
    blocks=[]
    for row in stats['block_reports']:
        checks=row['source_stationarity']['checks']
        blocks.append(dict(length=row['block_length'],blocks=row['blocks'],
            failed_channels=[name for name,result in checks.items() if not result['passed']],
            max_abs_lag1=max(abs(result['lag1']) for result in checks.values()),
            reference_only_error_upper_95=row['reference_only_error_upper_95'],resolution_passed=row['resolution_passed']))
    return dict(classification=stats['classification'],checks=stats['checks'],k=stats['k'],
        point_discrepancies=stats['point_discrepancies'],upper_95=stats['conservative_upper_95'],
        lower_05=stats['conservative_lower_05'],inconclusive_reasons=stats['inconclusive_reasons'],
        history_bridges=stats['history_bridges'],blocks=blocks)


def main():
    old=json.loads((PARENT/'AAA/statistics.json').read_text())
    new=json.loads((CE/'AAA/statistics.json').read_text())
    assessment=json.loads((CE/'AAA/reference_assessment.json').read_text())
    analysis=json.loads((CE/'AAA/analysis_result.json').read_text())
    native=json.loads((CE/'AAA/native_result.json').read_text())
    frozen_root=ART/'axial-material-AAA-frozen-axial-sensitivities-20261004'
    metadata_root=ART/'axial-material-AAA-frozen-axial-metadata-20261004'
    balance_root=ART/'axial-material-AAA-global-transverse-balance-20261004'
    frozen=json.loads((frozen_root/'result.json').read_text())
    adapted=json.loads((metadata_root/'result.json').read_text())
    balance=json.loads((balance_root/'result.json').read_text())
    if analysis['classification']!='COMPLETE_REFERENCE_ANALYSIS' or analysis['reference_assessment_sha256']!=digest(CE/'AAA/reference_assessment.json'):
        raise ValueError('complete original-rule assessment required')
    if native['returncode']!=0 or native['error'] is not None:
        raise ValueError('native diagnostic incomplete')
    if len(new['statepoint_identities'])!=250:
        raise ValueError('all active batches required')
    if not assessment['ABA_admitted'] and (ART/'axial-material-production-qualified-AB-compensated-20261004/ABA/run_claim.json').exists():
        raise ValueError('ABA cannot start from an unqualified AAA assessment')
    scope_review=json.loads((CE/'white_axial_source_scope_review.json').read_text())
    for name,wanted in scope_review['files'].items():
        if digest(name)!=wanted:raise ValueError('boundary source-scope review input changed')
    evidence=[PARENT/'AAA/statistics.json',PARENT/'AAA/reference_assessment.json',
        CE/'declaration.json',CE/'input_sampling_review.json',CE/'smoke_activation_receipt.json',CE/'input_equivalence_AAA.json',
        CE/'analysis_collection_declaration.json',CE/'white_axial_source_scope_review.json',CE/'AAA/execution.json',CE/'AAA/measurement_admission.json',
        CE/'AAA/native_result.json',CE/'AAA/statistics.json',CE/'AAA/currents_balance_symmetry.json',
        CE/'AAA/reference_assessment.json',CE/'AAA/analysis_result.json',CE/'AAA/aba_guard_rejection.json',
        frozen_root/'execution.json',frozen_root/'result.json',metadata_root/'execution.json',metadata_root/'metadata_admission.json',metadata_root/'result.json',
        balance_root/'declaration.json',balance_root/'result.json',balance_root/'driver_claim.json',balance_root/'AAA/stages.json']
    for report in (new,json.loads((CE/'AAA/currents_balance_symmetry.json').read_text())):
        for name,wanted in report['input_identities'].items():
            if digest(name)!=wanted:raise ValueError('analysis input changed')
        for item in report['statepoint_identities']:
            if digest(item['path'])!=item['sha256']:raise ValueError('statepoint changed')
    for key,item in assessment['evidence'].items():
        if digest(item['path'])!=item['sha256']:raise ValueError('assessment evidence changed')
    for name,wanted in balance['input_identities'].items():
        if digest(name)!=wanted:raise ValueError('transverse diagnostic input changed')
    for name,wanted in frozen['outputs'].items():
        if digest(frozen_root/name)!=wanted:raise ValueError('frozen sensitivity output changed')
    for name,wanted in adapted['outputs'].items():
        if digest(metadata_root/name)!=wanted:raise ValueError('adapted sensitivity output changed')
    for name,wanted in json.loads((metadata_root/'execution.json').read_text())['files'].items():
        if digest(name)!=wanted:raise ValueError('metadata study input changed')
    guard=json.loads((CE/'AAA/aba_guard_rejection.json').read_text())
    if guard['status']!='PASS_ACTUAL_ABA_GUARD_REJECTS_UNQUALIFIED_AAA' or guard['ABA_started']:
        raise ValueError('actual ABA refusal evidence required')
    for item in (guard['assessment'],guard['runtime']):
        if digest(item['path'])!=item['sha256']:raise ValueError('ABA guard evidence changed')
    OUT.mkdir(exist_ok=False);(OUT/'source_record').mkdir()
    sources=['prepare_qualified_AAA_ce_ufs.py','prepare_qualified_AAA_ufs_analysis.py',
        'assess_qualified_AAA_reference_ufs.py','run_qualified_AAA_reference_analysis_ufs.py',
        'frozen_AAA_axial_sensitivities.py','frozen_AAA_axial_sensitivities_metadata.py',
        'audit_AAA_global_transverse_balance.py','run_AAA_global_balance_bounded.py','review_AAA_white_axial_scope.py',
        'reference_statistics.py','compare_balance_symmetry.py',Path(__file__).name]
    for name in sources:shutil.copy2(TOOLS/name,OUT/'source_record'/name)
    rows=list(csv.DictReader((ART/'axial-material-qualified-AAA-observables-20261004/observables.regions.csv').open()))
    keys=sorted((int(row['radial_region']),int(row['axial_cell'])) for row in rows)
    profiles={}
    for label,stats,contract_path in [('Original CE',old,PARENT/'AAA/reference_contract.json'),('Weighted UFS CE',new,CE/'AAA/reference_contract.json')]:
        contract=json.loads(contract_path.read_text())
        grouped={key:[] for key in keys}
        for row in contract['region_layer_bins']:grouped[(row['region'],row['production_axial_cell'])].append(row)
        if any(len(value)!=1 for value in grouped.values()):raise ValueError('one-to-one 12-cell figure mapping required')
        mapped=[grouped[key][0] for key in keys]
        profiles[label]=[sum(stats['reference_nufission_fraction'][i] for i,row in enumerate(mapped)
            if row['production_axial_cell']==z and row['region'] in (4,5,6,7)) for z in range(1,13)]
        if abs(sum(profiles[label])-1)>1e-12:raise ValueError('plot global normalization mapping failed')
    production=[sum(float(row['nufission_fraction']) for row in rows if int(row['axial_cell'])==z and int(row['radial_region']) in (4,5,6,7)) for z in range(1,13)]
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(11,8))
    z=np.arange(6.25,150,12.5)
    axes[0,0].plot(z,production,'o-',label='SPOT saved REAL64')
    for label,values in profiles.items():axes[0,0].plot(z,values,'s--',label=label)
    axes[0,0].set(title='Fuel nu-fission per axial cell',xlabel='z (cm)',ylabel='Fraction of global nu-fission');axes[0,0].legend(fontsize=8)
    colors=['#d1873e','#367b98']
    for index,(label,stats) in enumerate([('Original CE',old),('Weighted UFS CE',new)]):
        diag=summary(stats)
        axes[0,1].plot([5,10],[row['max_abs_lag1'] for row in diag['blocks']],'o-',label=label,color=colors[index])
        axes[1,0].plot(np.linspace(0,150,13),stats['currents']['net_plus_z_per_nufission'],'o-',label=label,color=colors[index])
        axes[1,1].errorbar(index,stats['k']['reactivity_difference_pcm'],yerr=3*stats['k']['sigma_pcm'],fmt='o',color=colors[index],capsize=5)
    axes[0,1].axhline(.5,color='#555',linestyle='--',label='Original lag gate')
    axes[0,1].set(title='Largest source-proxy block correlation',xlabel='Generations per block',ylabel='Absolute lag-one correlation',xticks=[5,10]);axes[0,1].legend(fontsize=8)
    p_faces=list(csv.DictReader((ART/'axial-material-qualified-AAA-observables-20261004/observables.faces.csv').open()))
    p_current=[sum(float(row['current_per_global_nufission']) for row in p_faces if int(row['face'])==face) for face in range(13)]
    axes[1,0].plot(np.linspace(0,150,13),p_current,'o-',label='SPOT saved REAL64')
    axes[1,0].set(title='Signed axial current',xlabel='z (cm)',ylabel='Net +z current / global nu-fission');axes[1,0].legend(fontsize=8)
    axes[1,1].axhspan(-500,500,color='#777',alpha=.12)
    axes[1,1].set(title='SPOT minus CE reactivity',ylabel='pcm; bars: 3 statistical sigma',xticks=[0,1],xticklabels=['Original CE','Weighted UFS CE'])
    for ax in axes.flat:ax.grid(axis='y',alpha=.18)
    fig.suptitle('AAA source-sampling diagnostic: '+assessment['classification'].replace('_',' '),fontsize=13)
    fig.text(.06,.02,'All original gates retained. Profiles are sample means, not pointwise confidence bands.\nSource proxies are not source-bank histories. Current telescoping does not certify full neutron balance.',fontsize=8)
    fig.tight_layout(rect=(0,.07,1,.94));fig.savefig(OUT/'comparison.png',dpi=180);fig.savefig(OUT/'comparison.svg');plt.close(fig)
    combined=dict(schema='AXMAT_UFS_AAA_DIAGNOSIS_CLOSEOUT_V1',classification=assessment['classification'],
        original=summary(old),weighted_UFS=summary(new),frozen_axial=adapted.get('comparisons',{}),
        frozen_axial_classification=frozen['classification'],frozen_axial_error=frozen['error'],
        metadata_study_classification=adapted['classification'],metadata_study_error=adapted['error'],
        metadata_study_total_with_prior_charge_seconds=adapted['total_with_prior_charge_seconds'],
        transverse_balance=balance['normalized_by_fission_source'],ABA_admitted=assessment['ABA_admitted'],
        goal_complete=False,shared_solver_promoted=False,physical_inputs_changed=False,original_thresholds_changed=False,
        input_records={str(p):digest(p) for p in evidence})
    write_new(OUT/'verification.json',combined)
    lines=['2026-10-04：AAA 带权源采样及轴向诊断','',
        'A/B 快照及 AAA 四轮数值收敛结果保留。完整材料对照 goal 尚未完成。',
        '本轮独立参考判定：'+assessment['classification'],
        'ABA：'+('已准入，需查看实际执行记录。' if assessment['ABA_admitted'] else '未准入，未启动。'),'',
        '带权采样只增加固定的 1x1x12 UFS 网格；正式样本、独立初始源、物理材料、温度、几何、边界、核数据及原门槛均不变。',
        '小样本实际返回非单位正源权重，12 个轴向区都有源粒子。它只证明功能启用，不证明统计或物理精度。',
        f'完整独立参考耗时 {native["elapsed_seconds"]:.3f} 秒，100 批预热 + 250 批统计，每批 50000 粒子，单线程，无重复尝试。','']
    for label,stats in [('原参考',old),('带权参考',new)]:
        s=summary(stats);k=s['k']
        lines += [f'{label}：k={k["reference"]:.12f} +/- {k["sigma_k"]:.9f}；差异 {k["reactivity_difference_pcm"]:.3f} pcm，额度 {k["allowance_pcm"]:.3f} pcm。',
            f'  通量 L2 点估计/95%上限：{stats["point_discrepancies"][0]*100:.4f}% / {stats["conservative_upper_95"][0]*100:.4f}%；原目标 1%。',
            f'  燃料 nu-fission 最大差异点估计/95%上限：{stats["point_discrepancies"][1]*100:.4f}% / {stats["conservative_upper_95"][1]*100:.4f}%；原目标 3%。',
            '  判定：'+stats['classification']+'；未确认项：'+(', '.join(stats['inconclusive_reasons']) or '无')]
        for b in s['blocks']:lines.append(f'  区块 {b["length"]}：{len(b["failed_channels"])} 个源代理通道未通过；最大相邻相关 {b["max_abs_lag1"]:.6f}；参考分辨率 '+('PASS' if b['resolution_passed'] else '未确认'))
        for name,b in s['history_bridges'].items():
            lines.append(f'  预热/统计桥接 {name}：'+('PASS' if b['passed'] else '未通过')+f'；Welch z={b["welch_z"]:.6f}，原额度 3.29。')
    lines += ['', '完整 AAA 检查：', *[f'  {key}: {value}' for key,value in assessment['checks'].items()], '',
        '统计未确认时，差异只作诊断，不能宣称通过物理精度验收。没有按层/按群拟合或归一化。', '',
        '固定径向状态的轴向对照：'+frozen['classification']]
    if frozen['error']:lines.append('  未完成原因：'+frozen['error'])
    lines += ['  原尝试完成冷启动基线，24 格在求解前被固定基底的旧轴向存储尺寸拦住。该记录保留。',
        '  新版本只适配每份参考包 STATE-VECTOR(9)，其余整个文件字节完全一致；原生尺寸检查和每群基底/径向系数检查保留。',
        '  不重复基线求解，原尝试耗时计入 1440 秒总上限。',
        '  新版本判定：'+adapted['classification']]
    if adapted['error']:lines.append('  新版本未完成原因：'+adapted['error'])
    for label,values in adapted.get('comparisons',{}).items():lines.append('  '+label+': '+json.dumps(values,ensure_ascii=False))
    lines += ['  这些是独立的固定径向敏感性，未运行新的径向输运或耦合迭代；不能逐项相减归因，也不能放行 ABA。', '',
        '保存的双精度 P0 整体账目（相对于裂变源）：',
        *[f'  {name}: {value:.12e}' for name,value in balance['normalized_by_fission_source'].items()],
        '  这项使用原多群传递及输运修正系数，单独报告闭合项的净贡献；不是独立连续能吸收测量。','',
        '下一步继续处理 AAA 源历史与未通过的物理精度，再完成独立准入，最后运行 ABA。',
        '源码核对记录了白边界角度重分布与轴向标量径向项的结构差别。这只是后续对照线索，未确认它定量解释本轮差异。',
        'verification.json 保存所有实际输入及结果摘要；comparison.png 使用已核对的径向/轴向映射。旧记录未覆盖。']
    with (OUT/'REPORT.txt').open('x') as stream:stream.write('\n'.join(lines)+'\n')
    with (OUT/'result.sha256').open('x') as stream:
        for p in sorted(OUT.rglob('*')):
            if p.is_file() and p.name!='result.sha256':stream.write(f'{digest(p)}  {p.relative_to(OUT)}\n')
    for line in (OUT/'result.sha256').read_text().splitlines():
        expected,name=line.split('  ',1)
        if digest(OUT/name)!=expected:raise ValueError('closeout seal verification failed')
    print(json.dumps(dict(classification=assessment['classification'],report=str(OUT/'REPORT.txt'),seal_sha256=digest(OUT/'result.sha256')),ensure_ascii=False,indent=2))


if __name__=='__main__':main()

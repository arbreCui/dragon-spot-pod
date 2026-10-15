"""Keep the multiplicative saved-mean rate/flux identity as a diagnostic.

No new per-cell normalization or statistical admission is introduced. The
effective coefficient includes spectrum and reaction data; it is not a bare
microscopic cross-section comparison or an additive error attribution.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
ANA = ART / 'axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
CLOSE = ART / 'axial-material-AAA-white-trace-refined-closeout-20261005'
OUT = ART / 'axial-material-AAA-white-trace-refined-rate-flux-diagnostic-20261005'


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_new(path, data):
    with Path(path).open('x') as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write('\n')


def verify(files):
    for name, wanted in files.items():
        if digest(name) != wanted:
            raise ValueError('input identity changed: '+name)


def prepare():
    if digest(CLOSE / 'seal.json') != '7e92cb10c8303d71f7ead901674391f4c36c31af0041daa5145e51366280994d':
        raise ValueError('actual complete unqualified refined closeout required')
    verify({str(CLOSE / n):h for n,h in read(CLOSE / 'seal.json')['files'].items()})
    stats=ANA / 'AAA/statistics.json'
    if digest(stats) != '81133cecbee02f715e5b8f457c378152d3d69d597fbc59637d141213c3f74e36':
        raise ValueError('actual complete original-gate statistics required')
    paths=[Path(__file__).resolve(),Path(sys.executable).resolve(),stats,
        ANA / 'AAA/reference_assessment.json', ANA / 'declaration.json',
        ANA / 'observation/observables.regions.csv', ANA / 'observation/projection_receipt.json',
        CE / 'AAA/reference_contract.json', CLOSE / 'seal.json', CLOSE / 'result.json']
    files={str(p):digest(p) for p in paths};verify(files)
    OUT.mkdir(exist_ok=False)
    write_new(OUT / 'declaration.json',dict(schema='AXMAT_REFINED_RATE_FLUX_IDENTITY_DIAGNOSTIC_V1',
        files=files, total_wall_seconds=60, threads=1, retries=0, transport_launched=False,
        formula='Existing globally nu-fission-normalized integral flux F and rate N: '
                'N_p/N_r = (F_p/F_r) * [(N_p/F_p)/(N_r/F_r)]. '
                'The reference integral flux is reference_flux * original analytic volume.',
        scope='All 96 original cells retained; 48 fuel-cell factors. Saved sample means only. '
              'No confidence intervals for these new factors or new acceptance thresholds. '
              'The effective coefficient mixes spectral and reaction-data effects. '
              'No local flux normalization, fit, transport, causal attribution or ABA admission.'))
    print(json.dumps(dict(declaration_sha256=digest(OUT / 'declaration.json'))))


def run(expected):
    if digest(OUT / 'declaration.json') != expected:
        raise ValueError('wrong declaration')
    d=read(OUT / 'declaration.json');verify(d['files'])
    write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    started=time.monotonic();s=read(ANA / 'AAA/statistics.json')
    if s['classification']!='STATISTICAL_COMPARISON_FAIL' or not s['reference_statistics_adequate']:
        raise ValueError('actual resolved failed comparison required')
    volume=collections.defaultdict(float)
    for item in read(CE / 'AAA/reference_contract.json')['region_layer_bins']:
        volume[(item['region'],item['production_axial_cell'])]+=item['volume_cm3']
    with (ANA / 'observation/observables.regions.csv').open() as stream:
        source=sorted(csv.DictReader(stream),key=lambda r:(int(r['radial_region']),int(r['axial_cell'])))
    keys=[(int(r['radial_region']),int(r['axial_cell'])) for r in source]
    if keys!=[(r,z) for r in range(1,9) for z in range(1,13)] or set(volume)!=set(keys):
        raise ValueError('complete original region/cell mapping required')
    if len(s['reference_flux'])!=96 or len(s['reference_nufission_fraction'])!=96:
        raise ValueError('complete original reference means required')
    rows=[]
    for i,(key,item) in enumerate(zip(keys,source,strict=True)):
        pf=float(item['flux_per_global_nufission']);rf=s['reference_flux'][i]*volume[key]
        pn=float(item['nufission_fraction']);rn=s['reference_nufission_fraction'][i]
        if not all(math.isfinite(v) for v in (pf,rf,pn,rn)) or min(pf,rf)<=0:
            raise ValueError('invalid unaltered point observations')
        ratio=pf/rf;nr=sr=None
        if key[0] in (4,5,6,7):
            if min(pn,rn)<=0:raise ValueError('fuel rate must be positive')
            nr=pn/rn;sr=nr/ratio
            if abs(ratio*sr-nr)>8*sys.float_info.epsilon*abs(nr):
                raise ValueError('multiplicative identity failed')
        rows.append(dict(region=key[0],cell=key[1],production_integral_flux=pf,reference_integral_flux=rf,
            production_nufission_fraction=pn,reference_nufission_fraction=rn,
            integral_flux_relative=ratio-1,nu_relative=nr-1 if nr is not None else None,
            effective_nuXS_relative=sr-1 if sr is not None else None))
    fuel=[r for r in rows if r['nu_relative'] is not None]
    if abs(max(abs(r['nu_relative']) for r in fuel)-s['point_discrepancies'][1])>1e-14:
        raise ValueError('original failed fuel metric changed')
    ends=[r for r in fuel if r['cell'] in (1,12)]
    interior=[r for r in fuel if r['cell'] not in (1,12)]
    metrics=('nu_relative','integral_flux_relative','effective_nuXS_relative')
    ranges=lambda group:{k:[min(r[k] for r in group),max(r[k] for r in group)] for k in metrics}
    result=dict(classification='COMPLETE_SAVED_MEAN_RATE_FLUX_DIAGNOSTIC_ONLY',
        cells=96,fuel_cells=48,end_ranges=ranges(ends),interior_ranges=ranges(interior),
        worst=max(fuel,key=lambda r:abs(r['nu_relative'])),elapsed_seconds=time.monotonic()-started,
        original_nu_fission_gate='FAIL',factor_confidence_intervals_assessed=False,
        original_thresholds_changed=False,causal_attribution=False,ABA_admitted=False,scope=d['scope'])
    if result['elapsed_seconds']>d['total_wall_seconds']:
        raise ValueError('read-only time cap exceeded')
    with (OUT / 'region_cell_factors.csv').open('x') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    verify(d['files']);write_new(OUT / 'result.json',result)
    with (OUT / 'REPORT.txt').open('x') as stream:
        stream.write(f'''AAA 端部裂变率与通量的保存均值诊断（2026-10-05）

原 96 个观察单元全部保留，48 个燃料单元有有效裂变率。
沿用原全局裂变率归一化；恒等式是 Np/Nr=(Fp/Fr)*[(Np/Fp)/(Nr/Fr)]。
后一个因子是谱平均有效裂变加权系数，包含能谱与反应数据效应。
全部 96 单元见 region_cell_factors.csv；这是保存均值的诊断，没有新增逐格置信区间。

燃料首尾单元：裂变率偏差 {100*result['end_ranges']['nu_relative'][0]:.4f}%–{100*result['end_ranges']['nu_relative'][1]:.4f}%；
积分通量偏差 {100*result['end_ranges']['integral_flux_relative'][0]:.4f}%–{100*result['end_ranges']['integral_flux_relative'][1]:.4f}%；
有效裂变加权系数偏差 {100*result['end_ranges']['effective_nuXS_relative'][0]:.4f}%–{100*result['end_ranges']['effective_nuXS_relative'][1]:.4f}%。
原始端部通量本身已显示偏高，应继续核查端部通量与白边界闭合。
这不是将 CE 误差加法分配给某一模型，也不证明反应数据或降阶误差已经排除。

原 AAA 独立 nu_fission 门槛仍 FAIL，原阈值、统计规则和物理输入不变。
未重新计算通量、增加历史、选 rank、拟合或准入 ABA。
''')
    write_new(OUT / 'seal.json',dict(schema='AXMAT_RATE_FLUX_DIAGNOSTIC_SEAL_V1',
        files={p.name:digest(p) for p in OUT.iterdir() if p.is_file()}))
    print(json.dumps({k:result[k] for k in ('classification','end_ranges','elapsed_seconds')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('prepare','run'))
    parser.add_argument('--sha256');args=parser.parse_args()
    prepare() if args.action=='prepare' else run(args.sha256)

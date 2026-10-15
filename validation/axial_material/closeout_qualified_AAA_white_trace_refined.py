"""Close the actual refined AAA result without transport or altered gates.

All original observation bins remain. Localization is evidence of where the
failed comparison occurs, not a causal attribution or an accuracy admission.
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
ANA = ART / 'axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OUT = ART / 'axial-material-AAA-white-trace-refined-closeout-20261005'
PREPARED_SHA = '024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'
ASSESSMENT_SHA = '6485fb7f162c0e769ec87cae4626bd5dd0d432ad914baa10be0de79d52da0462'
ANALYSIS_SHA = '4fe593551b9c7a4a9ae385bec6414a3ab6869e4f0f671c71815b8fd2c6bddbad'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import (DiskResources, Refusal, qualify_aba, require_file,
                               verify_prepared, verify_sealed_directory)


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
    for name, wanted in files.items():
        require_file(Path(name), wanted)


def guard():
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    if (PROD / 'ABA').exists() or (ANA / 'AAA/reference_qualification.json').exists():
        raise ValueError('unexpected ABA or qualification before closeout')
    try:
        qualify_aba(info, PROD, PREPARED_SHA,
                    ANA / 'AAA/reference_assessment.json', ASSESSMENT_SHA)
    except Refusal as error:
        if str(error) != 'independent AAA reference qualification is not valid':
            raise ValueError('unexpected actual qualification refusal') from error
        result = dict(status='REJECTED_ACTUAL_REFINED_UNQUALIFIED_AAA', reason=str(error))
    else:
        raise ValueError('failed AAA was admitted')
    if (PROD / 'ABA').exists():
        raise ValueError('read-only qualification created an ABA directory')
    return result


def prepare():
    require_file(ANA / 'AAA/analysis_result.json', ANALYSIS_SHA)
    require_file(ANA / 'AAA/reference_assessment.json', ASSESSMENT_SHA)
    original = read(ANA / 'declaration.json')
    analysis = read(ANA / 'AAA/analysis_result.json')
    files = dict(original['files'])
    files.update({str(ANA / name): wanted for name, wanted in analysis['outputs'].items()})
    extra = [Path(__file__).resolve(), ANA / 'declaration.json',
             ANA / 'AAA/analysis_result.json', PROD / 'AAA/numerical_fixed_point_closeout.json',
             PROD / 'AAA/run_status.json', PROD / 'prepared.json',
             ANA / 'observation/observables.regions.csv',
             ANA / 'observation/observables.faces.csv', ANA / 'observation/observables.summary.txt',
             ANA / 'observation/projection_receipt.json', ANA / 'input_equivalence_AAA.json',
             ANA / 'measurement_admission.json', CE / 'AAA/native_result.json']
    files.update({str(path): digest(path) for path in extra})
    verify(files)
    actual_guard = guard()
    roots = sorted(set(original['resource_roots']) | {str(OUT)})
    resources = DiskResources(ART, roots, original['min_free_bytes'], original['artifact_budget_bytes'])
    before = resources.check()
    OUT.mkdir(exist_ok=False)
    write_new(OUT / 'declaration.json', dict(schema='AXMAT_REFINED_AAA_CLOSEOUT_V1',
        files=files, resource_roots=roots, min_free_bytes=original['min_free_bytes'],
        artifact_budget_bytes=original['artifact_budget_bytes'], total_wall_seconds=60,
        threads=1, retries=0, transport_launched=False, resources_before=before,
        scope='Verify complete refined fixed point, complete original-gate reference analysis, '
              'all 96 observation bins and unchanged ABA refusal. No causal attribution.'))
    write_new(OUT / 'ABA_admission_precheck.json', actual_guard)
    print(json.dumps(dict(declaration_sha256=digest(OUT / 'declaration.json'))))


def run(expected):
    declaration = read(require_file(OUT / 'declaration.json', expected))
    verify(declaration['files'])
    resources = DiskResources(ART, declaration['resource_roots'],
                              declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    resources.check()
    write_new(OUT / 'run_claim.json', dict(declaration_sha256=expected, started_unix=time.time()))
    started = time.monotonic()
    result = dict(classification='CLOSEOUT_FAILED_NO_RETRY', error=None, transport_launched=False,
                  AAA_accuracy_qualified=False, ABA_admitted=False, ABA_started=False)
    try:
        numerical = read(PROD / 'AAA/numerical_fixed_point_closeout.json')
        analysis = read(ANA / 'AAA/analysis_result.json')
        assessment = read(ANA / 'AAA/reference_assessment.json')
        stats = read(ANA / 'AAA/statistics.json')
        currents = read(ANA / 'AAA/currents_balance_symmetry.json')
        projection = read(ANA / 'observation/projection_receipt.json')
        native = read(CE / 'AAA/native_result.json')
        checks = dict(source_convergence='PASS', block_stability='PASS', statistical_resolution='PASS',
                      keff='PASS', scalar_flux='PASS', nu_fission='FAIL', input_equivalence='PASS',
                      currents_balance_symmetry='PASS')
        if (assessment['classification'] != 'AAA_REFERENCE_NOT_QUALIFIED'
                or assessment['checks'] != checks or assessment['ABA_admitted']
                or assessment['original_scientific_thresholds_changed']):
            raise ValueError('actual original eight-gate result differs')
        if (numerical['classification'] != 'PASS_COMPLETE_REFINED_NATIVE_FIXED_POINT_ONLY'
                or numerical['maps'] != 12 or numerical['stages'] != 105
                or numerical['elapsed_seconds'] > 43200 or not numerical['all_original_stages_PASS']
                or any(numerical['original_defects'][k] > 5e-7 for k in ('RA', 'RLEAK', 'RRHO'))):
            raise ValueError('bounded complete refined numerical fixed point required')
        folders = [PROD / 'archives', PROD / 'training', PROD / 'AAA/bootstrap']
        folders += [PROD / 'AAA' / f'map{i:03d}' for i in range(1, 13)]
        for folder in folders:
            verify_sealed_directory(folder)
        if (analysis['classification'] != 'COMPLETE_REFINED_ORIGINAL_GATE_REFERENCE_ANALYSIS'
                or analysis['completed_commands'] != 3 or analysis['error'] is not None
                or analysis['elapsed_seconds'] > 120):
            raise ValueError('complete bounded saved-reference analysis required')
        stages = read(ANA / 'AAA/stages.json')['stages']
        if len(stages) != 3 or any(stage['status'] != 'PASS' for stage in stages):
            raise ValueError('all original analysis commands must pass')
        if not stats['reference_statistics_adequate'] or stats['inconclusive_reasons']:
            raise ValueError('complete statistically resolved comparison required')
        if stats['targets'] != [.01, .03] or stats['shape_status'] != ['PASS', 'FAIL']:
            raise ValueError('original shape gates changed')
        if ([b['block_length'] for b in stats['block_reports']] != [5, 10]
                or any(b['lower_05'][1] <= .03 or not b['resolution_passed'] for b in stats['block_reports'])):
            raise ValueError('both original block results must substantiate the failed fuel gate')
        identities = [dict(path=str(CE / 'AAA' / f'statepoint.{i:04d}.h5'),
                           sha256=native['outputs'][f'statepoint.{i:04d}.h5']) for i in range(101, 2101)]
        if stats['statepoint_identities'] != identities or currents['statepoint_identities'] != identities:
            raise ValueError('both original reports must retain all 2000 active statepoints')
        lengths = {k:len(v) for k,v in stats['source_generation_history'].items()}
        if lengths != dict(raw_k_generation=21000, k_generation=2100, raw_entropy=21000, entropy=2100):
            raise ValueError('complete original raw and batch histories required')
        if (projection['classification'] != 'PASS_COMPLETE_FINE_AND_CONSERVATIVE_ORIGINAL_OBSERVATION_VIEW'
                or projection['native_axial_cells'] != 48 or projection['observation_cells'] != 12
                or len(projection['mapping']) != 96 or len(projection['face_map']) != 13
                or projection['local_or_binwise_normalization'] or projection['bins_removed']):
            raise ValueError('complete unchanged observation contract required')
        for key in ('original_checks_on_all_fine_entries', 'original_checks_on_observation_view'):
            if any(v != 'PASS' for v in projection[key]['checks'].values()):
                raise ValueError('fine or observation checks failed')
        with (ANA / 'observation/observables.regions.csv').open() as stream:
            rows = sorted(csv.DictReader(stream), key=lambda r:(int(r['radial_region']),int(r['axial_cell'])))
        if [(int(r['radial_region']), int(r['axial_cell'])) for r in rows] != [(r,z) for r in range(1,9) for z in range(1,13)]:
            raise ValueError('all 96 original comparison cells required')
        locations = []
        for row, reference in zip(rows, stats['reference_nufission_fraction'], strict=True):
            region, cell = int(row['radial_region']), int(row['axial_cell'])
            production = float(row['nufission_fraction'])
            locations.append(dict(radial_region=region, axial_cell=cell, z_lower_cm=(cell-1)*12.5,
                z_upper_cm=cell*12.5, production_nufission_fraction=production,
                reference_nufission_fraction=reference,
                signed_relative_difference=production/reference-1 if region in (4,5,6,7) else None))
        fuel = [r for r in locations if r['signed_relative_difference'] is not None]
        worst = max(fuel, key=lambda r:abs(r['signed_relative_difference']))
        if abs(abs(worst['signed_relative_difference'])-stats['point_discrepancies'][1]) > 1e-14:
            raise ValueError('location mapping does not reproduce original fuel metric')
        ends = [r for r in fuel if r['axial_cell'] in (1,12)]
        interior = [r for r in fuel if r['axial_cell'] not in (1,12)]
        with (OUT / 'region_cell_differences.csv').open('x') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(locations[0]))
            writer.writeheader()
            writer.writerows(locations)
        result.update(classification='COMPLETE_REFINED_AAA_CLOSEOUT_UNQUALIFIED',
            checks=checks, numerical_maps=12, numerical_stages=105, sealed_directories_verified=15,
            numerical_elapsed_seconds=numerical['elapsed_seconds'], original_defects=numerical['original_defects'],
            analysis_elapsed_seconds=analysis['elapsed_seconds'], active_batches=2000, raw_generations=21000,
            all_original_thresholds_unchanged=True, point_discrepancies=stats['point_discrepancies'],
            lower_05=stats['conservative_lower_05'], upper_95=stats['conservative_upper_95'], k=stats['k'],
            worst_fuel_cell=worst,
            fuel_end_signed_relative_range=[min(r['signed_relative_difference'] for r in ends),
                                           max(r['signed_relative_difference'] for r in ends)],
            fuel_interior_max_absolute_relative=max(abs(r['signed_relative_difference']) for r in interior),
            leakage_report_only=currents['comparison']['escape'], ABA_guard=guard(),
            full_neutron_balance=assessment['full_neutron_balance'],
            model_scope='Constant outer-Na white trace with uniform transverse azimuth; '
                        'numerical refinement and coupling do not qualify this approximation.',
            causation_established=False)
        report = f'''48-cell / SN32 AAA 完整耦合与原门槛独立精度报告（2026-10-05）

完整耦合达到数值 MET：12 个 map，105 个步骤 PASS，15 个阶段目录封存核验通过。
耦合计算 {numerical['elapsed_seconds']:.3f} 秒，原 43200 秒上限未改变。
原三项收敛残差均低于 5e-7。这是数值收敛凭证。
完整原生细网格先核验，再将每四个细单元保守合并到原 96 个观察单元，
保持原 13 个电流截面、全局归一化和全部原验收阈值；无删格或局部拟合。

实际独立分析 {analysis['elapsed_seconds']:.3f} 秒，三个步骤完成。全部 2000 个有效批次、
21000 代原始历史保留。源收敛、块稳定性和统计分辨率通过。
原八项门槛 7 PASS、nu_fission FAIL；AAA_REFERENCE_NOT_QUALIFIED。
k 偏差 {stats['k']['reactivity_difference_pcm']:.3f} pcm，通过原允许值 {stats['k']['allowance_pcm']:.3f} pcm。
通量 L2 点估计 {100*stats['point_discrepancies'][0]:.4f}%，95% 上界 {100*stats['conservative_upper_95'][0]:.4f}%，原标准 1%。
燃料裂变率份额最大偏差 {100*stats['point_discrepancies'][1]:.4f}%，
保守区间 [{100*stats['conservative_lower_05'][1]:.4f}%，{100*stats['conservative_upper_95'][1]:.4f}%]，原标准 3%。
两个预定分块方案的 5% 下界均超过 3%，这是统计充分条件下的未通过项。

最大点估计位于径向区域 {worst['radial_region']}、轴向单元 {worst['axial_cell']}。
燃料首尾单元偏差范围 [{100*result['fuel_end_signed_relative_range'][0]:.4f}%，{100*result['fuel_end_signed_relative_range'][1]:.4f}%]；
内部单元最大绝对偏差 {100*result['fuel_interior_max_absolute_relative']:.4f}%。全部 96 个单元见 CSV。
网格、角向细化及完整耦合仍未消除此偏差；空间分布不能单独证明原因。
白边界模型仍采用外层钠常量迹与均匀横向方位近似。下一步排查模型、
降阶与反应数据一致性；不能通过调门槛、拟合、删格或降分辨率准入。
跨方法电流误差仅作诊断，没有完整吸收/源中子平衡凭证。

实际原 ABA 准入检查拒绝本次未合格评估：{result['ABA_guard']['reason']}。
没有 AAA 合格凭证，没有 ABA 目录或计算。总目标仍未完成。
最初分析构造的路径错误保留在原目录；新目录仅纠正执行器路径，原科学分析不变。
'''
        with (OUT / 'REPORT.txt').open('x') as stream:
            stream.write(report)
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        verify(declaration['files'])
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        if result['elapsed_seconds'] > declaration['total_wall_seconds']:
            result.update(classification='CLOSEOUT_WALL_LIMIT_EXCEEDED', error='read-only wall cap exceeded')
        write_new(OUT / 'result.json', result)
    write_new(OUT / 'seal.json', dict(schema='AXMAT_REFINED_AAA_CLOSEOUT_SEAL_V1',
        files={p.name:digest(p) for p in OUT.iterdir() if p.is_file()}))
    print(json.dumps({k:result[k] for k in ('classification','elapsed_seconds','worst_fuel_cell',
        'fuel_end_signed_relative_range','fuel_interior_max_absolute_relative','ABA_guard','ABA_started')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)

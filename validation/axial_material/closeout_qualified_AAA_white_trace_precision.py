"""Seal the complete precision-reference result and locate its saved shape error.

This is a read-only closeout. It never changes thresholds, normalizes locally,
repeats transport or produces an AAA qualification from failed evidence.
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
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
CASE = CE / 'AAA'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
OBS = ART / 'axial-material-qualified-AAA-white-trace-observables-20261004'
OUT = ART / 'axial-material-AAA-white-trace-precision-closeout-20261005'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import DiskResources, Refusal, qualify_aba, require_file, verify_prepared

PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
FIXED_PINS = {
    CASE / 'execution.json': '17c4e48d4de450bc5e3232caf3238da519f23c3836bd54f0a91d122d300ae52c',
    CASE / 'native_result.json': 'ed608b5048e57571941a2cd3eb83d33e596024e85ab6a4bd31bb91d3668f4e92',
    CASE / 'reference_assessment.json': '5fa0435dff49977ab0b0ae3e8e50af1482467cfae22df3b6effd83ce3b2228f0',
    CASE / 'statistics.json': '20e4fef8a4b083ca3f7c516c936395e3a060b386c053bb8844cdc52bd9db30ba',
    CASE / 'currents_balance_symmetry.json': 'd5b06b33e50e2817d77a0466336db62c8512ff47a97e353f00ed9d5f404d1329',
}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def prepare():
    for path, expected in FIXED_PINS.items():
        require_file(path, expected)
    execution = read(CASE / 'execution.json')
    analysis = read(CASE / 'analysis_execution.json')
    files = {**execution['files'], **analysis['files'],
             **{str(path): expected for path, expected in FIXED_PINS.items()}}
    extra = [Path(__file__).resolve(), Path(sys.modules['production_runner'].__file__),
             CASE / 'analysis_result.json', CASE / 'analysis_execution.json',
             CASE / 'run_claim.json', CASE / 'analysis_claim.json',
             CASE / 'reference_contract.json', PROD / 'prepared.json',
             PROD / 'AAA/run_status.json', OBS / 'observables.regions.csv',
             OBS / 'observables.faces.csv', OBS / 'observables.summary.txt']
    files.update({str(path): digest(path) for path in extra})
    for path, expected in files.items():
        require_file(Path(path), expected)
    OUT.mkdir(exist_ok=False)
    roots = sorted(set(execution['resource_roots']) | {str(OUT)})
    resources = DiskResources(ART, roots, 8 * 2**30, 40 * 2**30)
    before = resources.check()
    declaration = dict(schema='AXMAT_COMPLETE_AAA_PRECISION_CLOSEOUT_V1',
        files=files, resource_roots=roots, artifact_budget_bytes=40 * 2**30,
        min_free_bytes=8 * 2**30, total_wall_seconds=60, threads=1, retries=0,
        transport_launched=False, resources_before=before,
        scope='Verify the actual native completion and all original analysis outputs. '
              'Reproduce saved point metrics and region/cell mapping, call the unchanged '
              'ABA qualification guard with the actual unqualified assessment, and '
              'seal the result without changing any scientific classification. '
              'Spatial localization is diagnostic, not proof of error causation.')
    write_new(OUT / 'declaration.json', declaration)
    print(json.dumps(dict(declaration=str(OUT / 'declaration.json'), sha256=digest(OUT / 'declaration.json'))))


def run(expected):
    require_file(OUT / 'declaration.json', expected)
    declaration = read(OUT / 'declaration.json')
    for path, wanted in declaration['files'].items():
        require_file(Path(path), wanted)
    if (OUT / 'run_claim.json').exists():
        raise ValueError('closeout already claimed; no retry')
    resources = DiskResources(ART, declaration['resource_roots'],
        declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    resources.check()
    write_new(OUT / 'run_claim.json', dict(declaration_sha256=expected, started_unix=time.time()))
    started = time.monotonic()
    result = dict(classification='CLOSEOUT_FAILED_NO_RETRY', error=None,
                  transport_launched=False, independent_accuracy_qualified=False)
    try:
        native = read(CASE / 'native_result.json')
        analysis = read(CASE / 'analysis_result.json')
        assessment = read(CASE / 'reference_assessment.json')
        stats = read(CASE / 'statistics.json')
        currents = read(CASE / 'currents_balance_symmetry.json')
        if (native['status'] != 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
                or native['returncode'] != 0 or native['error'] is not None
                or native['elapsed_seconds'] > 64800):
            raise ValueError('complete bounded native reference required')
        require_file(CASE / 'openmc.log', native['log_sha256'])
        for name, wanted in native['outputs'].items():
            require_file(CASE / name, wanted)
        if (analysis['classification'] != 'COMPLETE_REFERENCE_ANALYSIS'
                or analysis['completed_commands'] != 3 or analysis['error'] is not None
                or analysis['elapsed_seconds'] > 120):
            raise ValueError('complete bounded original analysis required')
        for name, wanted in analysis['outputs'].items():
            require_file(CASE / name, wanted)
        if assessment['classification'] != 'AAA_REFERENCE_NOT_QUALIFIED' or assessment['ABA_admitted']:
            raise ValueError('this closeout requires the actual unqualified assessment')
        expected_checks = dict(source_convergence='PASS', block_stability='PASS',
            statistical_resolution='PASS', keff='PASS', scalar_flux='PASS',
            nu_fission='FAIL', input_equivalence='PASS', currents_balance_symmetry='PASS')
        if assessment['checks'] != expected_checks or not stats['reference_statistics_adequate']:
            raise ValueError('original eight-gate result differs from observed evidence')
        pins = [dict(path=str(CASE / f'statepoint.{i:04d}.h5'),
                     sha256=native['outputs'][f'statepoint.{i:04d}.h5']) for i in range(101, 2101)]
        if stats['statepoint_identities'] != pins or currents['statepoint_identities'] != pins:
            raise ValueError('both analyses must bind all 2000 consecutive active statepoints')
        if (CASE / 'reference_qualification.json').exists() or (PROD / 'ABA').exists():
            raise ValueError('unexpected qualification or ABA execution')
        info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
        try:
            qualify_aba(info, PROD, PREPARED_SHA, CASE / 'reference_assessment.json',
                        digest(CASE / 'reference_assessment.json'))
        except Refusal as error:
            guard = dict(status='REJECTED_ACTUAL_UNQUALIFIED_AAA', reason=str(error))
        else:
            raise ValueError('unchanged ABA guard accepted failed AAA evidence')
        if (PROD / 'ABA').exists():
            raise ValueError('ABA guard created an execution directory')
        with (OBS / 'observables.regions.csv').open() as stream:
            rows = sorted(csv.DictReader(stream), key=lambda r:(int(r['radial_region']), int(r['axial_cell'])))
        keys = [(int(r['radial_region']), int(r['axial_cell'])) for r in rows]
        if keys != [(r, z) for r in range(1, 9) for z in range(1, 13)]:
            raise ValueError('complete original 8 by 12 comparison cells required')
        locations = []
        for row, reference in zip(rows, stats['reference_nufission_fraction'], strict=True):
            region, cell = int(row['radial_region']), int(row['axial_cell'])
            production = float(row['nufission_fraction'])
            relative = production/reference-1 if region in (4, 5, 6, 7) else None
            locations.append(dict(radial_region=region, axial_cell=cell,
                z_lower_cm=(cell-1)*12.5, z_upper_cm=cell*12.5,
                production_nufission_fraction=production,
                reference_nufission_fraction=reference, signed_relative_difference=relative))
        fuel = [r for r in locations if r['signed_relative_difference'] is not None]
        worst = max(fuel, key=lambda r:abs(r['signed_relative_difference']))
        if abs(abs(worst['signed_relative_difference'])-stats['point_discrepancies'][1]) > 1e-14:
            raise ValueError('saved region mapping does not reproduce the original maximum metric')
        ends = [r for r in fuel if r['axial_cell'] in (1, 12)]
        interior = [r for r in fuel if r['axial_cell'] not in (1, 12)]
        with (OUT / 'region_cell_differences.csv').open('x') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(locations[0]))
            writer.writeheader(); writer.writerows(locations)
        result.update(classification='COMPLETE_AAA_PRECISION_CLOSEOUT_UNQUALIFIED',
            native_result_sha256=digest(CASE / 'native_result.json'),
            analysis_result_sha256=digest(CASE / 'analysis_result.json'),
            reference_assessment_sha256=digest(CASE / 'reference_assessment.json'),
            AAA_classification=assessment['classification'], checks=assessment['checks'],
            all_original_thresholds_unchanged=True, active_batches=2000,
            raw_generations=21000, native_elapsed_seconds=native['elapsed_seconds'],
            k=stats['k'], point_discrepancies=stats['point_discrepancies'],
            lower_05=stats['conservative_lower_05'], upper_95=stats['conservative_upper_95'],
            worst_fuel_cell=worst,
            fuel_end_signed_relative_range=[min(r['signed_relative_difference'] for r in ends),
                                           max(r['signed_relative_difference'] for r in ends)],
            fuel_interior_max_absolute_relative=max(abs(r['signed_relative_difference']) for r in interior),
            leakage_report_only=currents['comparison']['escape'], ABA_guard=guard,
            ABA_started=False, full_particle_balance=assessment['full_neutron_balance'],
            scope='Full original AAA accuracy assessment failed the fuel nu-fission gate. '
                  'End-cell localization is a diagnostic pattern; axial discretization '
                  'and angular-model errors require independent convergence studies.')
        text = f'''AAA 完整精度参考阶段报告（2026-10-05）

全部 2000 个有效批次、21000 代历史已完成并绑定。原生计算正常结束，
计时器用时 {native['elapsed_seconds']:.2f} 秒，原 64800 秒上限未改变。
原分析用时 {analysis['elapsed_seconds']:.2f} 秒，全部 3 个分析步骤完成。

原验收结果：{assessment['classification']}。8 项中 7 项 PASS，nu_fission FAIL。
参考源收敛、块稳定性、统计分辨率、k、标量通量、物理输入等价和
有符号电流/望远镜记账/镜像对称性通过。没有完整吸收/源中子平衡凭证。

k：SPOT {stats['k']['production']:.12f}，CE {stats['k']['reference']:.12f}。
反应性偏差 {stats['k']['reactivity_difference_pcm']:.3f} pcm，
原允许值 {stats['k']['allowance_pcm']:.3f} pcm。
归一化通量 L2：{100*stats['point_discrepancies'][0]:.4f}%，95% 上界
{100*stats['conservative_upper_95'][0]:.4f}%，原标准 1%。
燃料裂变份额最大相对偏差：{100*stats['point_discrepancies'][1]:.4f}%。
原块自助法保守区间：[{100*stats['conservative_lower_05'][1]:.4f}%，
{100*stats['conservative_upper_95'][1]:.4f}%]，原标准 3%。

最大点估计位于径向区域 {worst['radial_region']}、轴向单元 {worst['axial_cell']}。
四个燃料径向区域的首尾单元均偏高；内部单元最大点估计偏差
{100*result['fuel_interior_max_absolute_relative']:.4f}%。这说明偏差的空间位置，
不能单独证明轴向离散或白边界角向近似是原因。逐区域数据见 CSV。

实际原 ABA 准入函数拒绝了这份不合格评估：{guard['reason']}。
没有 AAA 合格凭证，也没有启动 ABA。此前静态准备文件不构成 ABA 结果。

下一步：同一物理输入、原验收阈值下核验轴向/角向数值收敛；
任何诊断通过都仍需要完整耦合固定点和独立精度核验。
总目标仍未完成。本报告不改变冻结输入、历史结果或共享求解器。
'''
        with (OUT / 'REPORT.txt').open('x') as stream:
            stream.write(text)
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        for path, wanted in declaration['files'].items():
            require_file(Path(path), wanted)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        if result['elapsed_seconds'] > declaration['total_wall_seconds']:
            result.update(classification='CLOSEOUT_WALL_LIMIT_EXCEEDED', error='declared read-only wall cap exceeded')
        result['outputs'] = {p.name:digest(p) for p in OUT.iterdir()
            if p.is_file() and p.name not in ('result.json', 'seal.json')}
        write_new(OUT / 'result.json', result)
    write_new(OUT / 'seal.json', dict(schema='AXMAT_IMMUTABLE_PRECISION_CLOSEOUT_SEAL_V1',
        files={p.name:digest(p) for p in OUT.iterdir() if p.is_file()}))
    print(json.dumps({k:v for k,v in result.items() if k not in ('resources','outputs')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)

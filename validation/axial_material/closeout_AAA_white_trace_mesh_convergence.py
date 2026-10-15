"""Read-only closeout of the completed cold axial mesh convergence study."""
import argparse
import csv
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import prepare_AAA_white_trace_mesh_convergence as mesh

OUT = mesh.ART / 'axial-material-AAA-white-trace-mesh-closeout-20261005'
MESH_SHA = '821d500a67fbff6acac4a1f0d9ec604157b3f21fb14436357b6c126da5cefdcc'
DECLARATION_SHA = '6861ecb416bb1277c53a77deeddbba8577b1808974781d7247c74a5e2a67ac7c'


def read(path):
    return json.loads(Path(path).read_text())


def verify():
    mesh.require_file(mesh.OUT / 'result.json', MESH_SHA)
    mesh.require_file(mesh.OUT / 'declaration.json', DECLARATION_SHA)
    declaration = read(mesh.OUT / 'declaration.json')
    result = read(mesh.OUT / 'result.json')
    files = dict(declaration['files'])
    files.update({str(mesh.OUT / name): wanted for name, wanted in result['outputs'].items()})
    files.update({str(mesh.OUT / name): mesh.base.digest(mesh.OUT / name)
                  for name in ('declaration.json', 'run_claim.json', 'result.json')})
    for name, wanted in files.items():
        mesh.require_file(Path(name), wanted)
    mesh.ready()
    if (result['classification'] != 'COMPLETE_WHITE_TRACE_FROZEN_MESH_SENSITIVITY_ONLY'
            or result['error'] is not None or result['completed_cases'] != [x[0] for x in mesh.CASES]
            or result['elapsed_seconds'] > declaration['total_wall_seconds']
            or any(result[k] for k in ('AAA_accuracy_qualified', 'ABA_admitted', 'shared_solver_promoted'))):
        raise ValueError('complete bounded cold-only mesh result required')
    stages = read(mesh.OUT / 'AAA/stages.json')['stages']
    if len(stages) != 20 or any(x['status'] != 'PASS' or x['elapsed_seconds'] > x['wall_cap_seconds'] for x in stages):
        raise ValueError('all twenty original bounded stages must pass')
    return files, declaration, result


def prepare():
    files, declaration, result = verify()
    files.update({str(Path(__file__).resolve()): mesh.base.digest(__file__),
                  str(Path(mesh.__file__).resolve()): mesh.base.digest(mesh.__file__)})
    OUT.mkdir(exist_ok=False)
    roots = sorted(set(declaration['resource_roots']) | {str(OUT)})
    resources = mesh.DiskResources(mesh.ART, roots, 8*2**30, 40*2**30)
    mesh.base.write_new(OUT / 'declaration.json', dict(
        schema='AXMAT_WHITE_TRACE_FROZEN_MESH_CLOSEOUT_V1', files=files,
        resource_roots=roots, min_free_bytes=8*2**30, artifact_budget_bytes=40*2**30,
        resources_before=resources.check(), total_wall_seconds=60,
        numeric_children_at_once=0, retries=0, transport_launched=False,
        scope='Recheck sealed inputs, outputs, original inner gates and saved accounting. '
              'Verify conservative original-cell sums and report numerical changes only. '
              'No cold-state qualification, extrapolated accuracy, CE fitting or shared promotion.'))
    print(json.dumps(mesh.base.pin(OUT / 'declaration.json')))


def run(expected):
    mesh.require_file(OUT / 'declaration.json', expected)
    declaration = read(OUT / 'declaration.json')
    for name, wanted in declaration['files'].items():
        mesh.require_file(Path(name), wanted)
    resources = mesh.DiskResources(mesh.ART, declaration['resource_roots'],
        declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    resources.check()
    mesh.base.write_new(OUT / 'run_claim.json', dict(declaration_sha256=expected,
        started_unix=time.time(), retries=0))
    started = time.monotonic()
    result = dict(classification='FAILED_MESH_CLOSEOUT_NO_RETRY', error=None,
        transport_launched=False, independent_accuracy_qualified=False, ABA_admitted=False)
    try:
        _, _, previous = verify()
        mesh.base.OUT = mesh.OUT
        sys.path.insert(0, str(mesh.CE / 'runtime'))
        balance = mesh.load_module('mesh_closeout_original_balance', mesh.CE / 'runtime/compare_balance_symmetry.py')
        rows = list(csv.DictReader((mesh.OUT / 'original_cell_comparison.csv').open()))
        if len(rows) != 288:
            raise ValueError('complete three by ninety-six conservative comparison required')
        locations = {}
        for case, nz, cap in mesh.CASES:
            folder = mesh.OUT / case
            mesh.base.check_terminal((folder / 'solve.log').read_text())
            actual = mesh.saved_state(folder, nz, balance)
            saved = read(folder / 'saved_state_admission.json')
            if any(actual[k] != saved[k] for k in actual):
                raise ValueError('saved admission differs from original-rule reevaluation')
            structure = mesh.base.structure(folder, nz, 8)
            if structure['records_verified'] != 3330:
                raise ValueError('incomplete frozen radial/basis verification')
            fine = list(csv.DictReader((folder / 'observables.regions.csv').open()))
            mapped = [x for x in rows if x['case'] == case]
            keys = {(int(x['radial_region']), int(x['axial_cell'])) for x in mapped}
            if len(mapped) != 96 or keys != {(r,c) for r in range(1,9) for c in range(1,13)}:
                raise ValueError('missing or duplicate original-cell key')
            for row in mapped:
                selected = [x for x in fine if x['radial_region'] == row['radial_region']
                    and (int(x['axial_cell'])-1)//(nz//12)+1 == int(row['axial_cell'])]
                if len(selected) != nz//12:
                    raise ValueError('incomplete fine-cell mapping')
                for key in ('volume_cm3', 'flux_per_global_nufission', 'nufission_fraction'):
                    if sum(float(x[key]) for x in selected) != float(row[key]):
                        raise ValueError('conservative saved sum differs: '+key)
            fuel = [x for x in mapped if int(x['radial_region']) in (4,5,6,7)]
            worst = max(fuel, key=lambda x: abs(float(x['signed_fuel_relative_difference'])))
            end = [float(x['signed_fuel_relative_difference']) for x in fuel if int(x['axial_cell']) in (1,12)]
            interior = [abs(float(x['signed_fuel_relative_difference'])) for x in fuel if 2 <= int(x['axial_cell']) <= 11]
            locations[case] = dict(worst_radial_region=int(worst['radial_region']),
                worst_original_axial_cell=int(worst['axial_cell']),
                worst_signed_relative=float(worst['signed_fuel_relative_difference']),
                end_cell_signed_range=[min(end), max(end)], interior_max_absolute=max(interior),
                all_original_saved_checks=actual['checks'], scalar_entries=actual['saved_scalar_entries'])
        mesh.require_file(mesh.CE / 'AAA/reference_assessment.json', mesh.ASSESSMENT_SHA)
        if time.monotonic()-started > declaration['total_wall_seconds']:
            raise ValueError('read-only closeout exceeded sixty-second limit')
        result.update(classification='COMPLETE_COLD_MESH_CLOSEOUT_UNQUALIFIED',
            mesh_result_sha256=MESH_SHA, stages_passed=20, locations=locations,
            comparisons=previous['comparisons'], original_AAA_reference='AAA_REFERENCE_NOT_QUALIFIED',
            next_step='Cold angular-order convergence at fixed 48-cell mesh, followed by '
                      'complete coupled validation and all unchanged original independent accuracy gates. '
                      'Mesh changes alone have not established a qualified candidate.')
        changes = previous['comparisons']['mesh_changes']
        points = previous['comparisons']['diagnostic_CE_saved_mean_comparisons']
        lines = ['AAA 轴向网格细化阶段报告', '',
            '12、24、48 层冷态轴向试验完成；20 个有界阶段全部通过，耗时 %.3f 秒。' % previous['elapsed_seconds'],
            '三者沿用同一完整 AAA 最终径向算子、公共基底和物理材料输入；没有新增径向或耦合计算。',
            '每次核对 3330 个径向/基底记录，370 群真实保存标量均为正；原内外迭代、端面电流符号、消去求和和镜像检查通过。', '',
            '内部网格变化（所有细网格完整积分保守映射回原 12 层）：']
        for label, values in changes.items():
            lines.append('%s：反应性 %+.6f pcm，通量 L2 %.6f%%，燃料份额最大相对变化 %.6f%%。' %
                (label, values['reactivity_change_pcm'], 100*values['normalized_flux_l2'], 100*values['max_fuel_fraction_relative']))
        lines += ['', '与已完成独立参考的保存均值对照，仅用于诊断：']
        for case, values in points.items():
            lines.append('%s：通量 L2 %.6f%%，燃料份额最大相对差异 %.6f%%，最差位置为径向区 %d、原轴向层 %d。' %
                (case, 100*values['CE_saved_mean_flux_l2'], 100*values['CE_saved_mean_max_fuel_relative'],
                 locations[case]['worst_radial_region'], locations[case]['worst_original_axial_cell']))
        lines += ['', '网格细化变化减小，但这些是固定径向算子的冷态结果，不能证明完整耦合解或外推极限已达到物理精度门槛。',
            '完整 AAA 原八项独立评估仍为七项通过、燃料份额一项失败；原 3% 门槛不变，ABA 未准入。',
            '端部偏差集中仅为位置诊断，不能由单因素试验认定误差原因。电流消去求和不等于完整吸收/源粒子平衡证明。',
            '下一步在固定 48 层下检查角度阶数收敛；不拟合独立参考，不局部归一化，不删去端部。随后仍需完整耦合和原独立精度检查。']
        with (OUT / 'REPORT.txt').open('x') as stream:
            stream.write('\n'.join(lines)+'\n')
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        for name, wanted in declaration['files'].items():
            if mesh.base.digest(name) != wanted:
                result.update(classification='INPUT_CHANGED', error='changed: '+name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        mesh.base.write_new(OUT / 'result.json', result)
        mesh.base.write_new(OUT / 'seal.json', dict(schema='AXMAT_IMMUTABLE_COLD_MESH_CLOSEOUT_V1',
            files={str(p.relative_to(OUT)):mesh.base.digest(p) for p in OUT.rglob('*')
                   if p.is_file() and p.name != 'seal.json'}))
    print(json.dumps({k:v for k,v in result.items() if k not in ('resources','comparisons','locations')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)

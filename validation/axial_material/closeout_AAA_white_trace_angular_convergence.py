"""Seal the complete cold angular study without qualifying physical accuracy."""
import argparse
import csv
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import prepare_AAA_white_trace_angular_convergence as angular

OUT = angular.ART / 'axial-material-AAA-white-trace-angular-closeout-20261005'
RESULT_SHA = '275b542018d35940159777b57f5f5269b206c3b2f685d0e46e181564b386e0df'
DECLARATION_SHA = 'aec1389e18a009a09fd1919e5e8291b23be1122136b0dbc301afd19d46ee91a8'


def verify():
    angular.mesh.require_file(angular.OUT / 'result.json', RESULT_SHA)
    angular.mesh.require_file(angular.OUT / 'declaration.json', DECLARATION_SHA)
    declaration = angular.read(angular.OUT / 'declaration.json')
    result = angular.read(angular.OUT / 'result.json')
    files = dict(declaration['files'])
    files.update({str(angular.OUT / name):wanted for name,wanted in result['outputs'].items()})
    files.update({str(angular.OUT / name):angular.mesh.base.digest(angular.OUT / name)
                  for name in ('declaration.json','run_claim.json','result.json')})
    for name,wanted in files.items():
        angular.mesh.require_file(Path(name),wanted)
    angular.ready()
    if (result['classification'] != 'COMPLETE_WHITE_TRACE_FROZEN_ANGULAR_SENSITIVITY_ONLY'
            or result['error'] is not None or result['completed_new_cases'] != [x[0] for x in angular.CASES]
            or result['reused_baseline'] != 'cold48_sn8'
            or result['elapsed_seconds'] > declaration['total_wall_seconds']
            or any(result[k] for k in ('AAA_accuracy_qualified','ABA_admitted','shared_solver_promoted'))):
        raise ValueError('complete bounded cold-only angular result required')
    stages = angular.read(angular.OUT / 'AAA/stages.json')['stages']
    if len(stages) != 18 or any(x['status'] != 'PASS' or x['elapsed_seconds'] > x['wall_cap_seconds'] for x in stages):
        raise ValueError('all eighteen original bounded stages must pass')
    return files,declaration,result


def prepare():
    files,declaration,result = verify()
    files.update({str(Path(__file__).resolve()):angular.mesh.base.digest(__file__),
                  str(Path(angular.__file__).resolve()):angular.mesh.base.digest(angular.__file__)})
    OUT.mkdir(exist_ok=False)
    roots = sorted(set(declaration['resource_roots']) | {str(OUT)})
    resources = angular.mesh.DiskResources(angular.ART,roots,8*2**30,40*2**30)
    angular.mesh.base.write_new(OUT / 'declaration.json',dict(
        schema='AXMAT_WHITE_TRACE_FROZEN_ANGULAR_CLOSEOUT_V1',files=files,
        resource_roots=roots,min_free_bytes=8*2**30,artifact_budget_bytes=40*2**30,
        resources_before=resources.check(),total_wall_seconds=60,
        numeric_children_at_once=0,retries=0,transport_launched=False,
        scope='Recheck all frozen input/output pins, compiled analytic kernels and controls, '
              'original native terminals, saved accounting and conservative original-cell sums. '
              'Report the internal angular convergence and CE means diagnostically only. '
              'The original AAA accuracy assessment remains unqualified.'))
    print(json.dumps(angular.mesh.base.pin(OUT / 'declaration.json')))


def run(expected):
    angular.mesh.require_file(OUT / 'declaration.json',expected)
    declaration = angular.read(OUT / 'declaration.json')
    for name,wanted in declaration['files'].items():
        angular.mesh.require_file(Path(name),wanted)
    resources = angular.mesh.DiskResources(angular.ART,declaration['resource_roots'],
        declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    resources.check()
    angular.mesh.base.write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,
        started_unix=time.time(),retries=0))
    started = time.monotonic()
    result = dict(classification='FAILED_ANGULAR_CLOSEOUT_NO_RETRY',error=None,
        transport_launched=False,independent_accuracy_qualified=False,ABA_admitted=False)
    try:
        _,_,previous = verify()
        sys.path.insert(0,str(angular.CE / 'runtime'))
        balance = angular.mesh.load_module('angular_closeout_original_balance',angular.CE / 'runtime/compare_balance_symmetry.py')
        saved_verifier = angular.mesh.load_module('angular_closeout_saved_fields',angular.OUT / 'runtime/saved_field_verifier.py')
        angular.mesh.base.OUT = angular.OUT
        kernels = {'SN8':angular.compiled_kernel(angular.OUT / 'unit',angular.inputs_path('original_track'),8,True)}
        rows = list(csv.DictReader((angular.OUT / 'original_cell_comparison.csv').open()))
        if len(rows) != 288:
            raise ValueError('complete three by ninety-six conservative comparison required')
        locations = {}
        folders = [('cold48_sn8',angular.MESH / 'cold48_sn8',8),
            *[(c,angular.OUT/c,sn) for c,nz,sn,cap in angular.CASES]]
        for case,folder,sn in folders:
            angular.mesh.base.check_terminal((folder / 'solve.log').read_text())
            saved = angular.read(folder / 'saved_state_admission.json')
            actual = saved_verifier.saved_state(folder,48,sn,balance)
            if any(actual[k] != saved[k] for k in actual):
                raise ValueError('saved original-rule admission differs on reevaluation')
            if angular.mesh.base.structure(folder,48,sn)['records_verified'] != 3330:
                raise ValueError('incomplete frozen radial/basis verification')
            if sn != 8:
                kernels['SN'+str(sn)] = angular.compiled_kernel(folder / 'unit',folder / 'track.xsm',sn)
            fine = list(csv.DictReader((folder / 'observables.regions.csv').open()))
            mapped = [x for x in rows if x['case'] == case]
            if len(mapped) != 96 or {(int(x['radial_region']),int(x['axial_cell'])) for x in mapped} != {(r,c) for r in range(1,9) for c in range(1,13)}:
                raise ValueError('missing or duplicate original-cell key')
            for row in mapped:
                selected = [x for x in fine if x['radial_region'] == row['radial_region']
                    and (int(x['axial_cell'])-1)//4+1 == int(row['axial_cell'])]
                if len(selected) != 4:
                    raise ValueError('incomplete four-cell integral mapping')
                for key in ('volume_cm3','flux_per_global_nufission','nufission_fraction'):
                    if sum(float(x[key]) for x in selected) != float(row[key]):
                        raise ValueError('conservative saved sum differs: '+key)
            fuel = [x for x in mapped if int(x['radial_region']) in (4,5,6,7)]
            worst = max(fuel,key=lambda x:abs(float(x['signed_fuel_relative_difference'])))
            locations[case] = dict(worst_radial_region=int(worst['radial_region']),
                worst_original_axial_cell=int(worst['axial_cell']),
                worst_signed_relative=float(worst['signed_fuel_relative_difference']),
                original_saved_checks=actual['checks'],scalar_entries=actual['saved_scalar_entries'])
        if time.monotonic()-started > declaration['total_wall_seconds']:
            raise ValueError('read-only closeout exceeded sixty-second limit')
        result.update(classification='COMPLETE_COLD_ANGULAR_CLOSEOUT_UNQUALIFIED',
            angular_result_sha256=RESULT_SHA,stages_passed=18,locations=locations,kernels=kernels,
            comparisons=previous['comparisons'],original_AAA_reference='AAA_REFERENCE_NOT_QUALIFIED',
            next_step='Fresh complete coupled AAA validation at the finest studied 48-cell/SN32 '
                      'setting, with the same physical inputs and all original gates. '
                      'The cold result does not qualify AAA or admit ABA.')
        changes = previous['comparisons']['angular_changes']
        points = previous['comparisons']['diagnostic_CE_saved_mean_comparisons']
        lines = ['AAA 角度细化阶段报告','',
            '固定 48 层，8/16/32 阶冷态对照完成。8 阶复用已完成保存结果；只新增两项求解。',
            '18 个有界阶段全部通过，总耗时 %.3f 秒；16/32 阶原内外迭代、真实标量正值、电流符号、消去求和及镜像检查通过。' % previous['elapsed_seconds'],
            '三者的 3330 个径向/基底记录逐项相同；物理材料、几何和原验收阈值不变。',
            '8 阶编译算子逐字节等同原版本；各阶编译算子与同一解析公式一致，并通过守恒与半正定检查。',
            '该边界模型仍采用常数外钠区边界迹和均匀横向方位角近似，不等于精确三维非均匀边界算子。','',
            '内部角度变化（保守映射回原 12 层，并各用一个全局 ν 裂变归一化）：']
        for label,values in changes.items():
            lines.append('%s：反应性 %+.6f pcm，通量 L2 %.6f%%，燃料份额最大相对变化 %.6f%%。' %
                (label,values['reactivity_change_pcm'],100*values['normalized_flux_l2'],100*values['max_fuel_fraction_relative']))
        lines += ['','与已完成独立参考的保存均值对照，仅用于诊断：']
        for case,values in points.items():
            lines.append('%s：通量 L2 %.6f%%，燃料份额最大相对差异 %.6f%%，最差位置为径向区 %d、原轴向层 %d。' %
                (case,100*values['CE_saved_mean_flux_l2'],100*values['CE_saved_mean_max_fuel_relative'],
                 locations[case]['worst_radial_region'],locations[case]['worst_original_axial_cell']))
        lines += ['','角度细化变化减小，但与参考的燃料分布诊断差异增大；不能选择更粗设置来拟合参考。',
            '这些是固定最终径向算子的冷态数值结果，没有新增完整耦合解，也没有新的独立原八项精度分类。',
            '原完整 AAA 评估仍为七项通过、燃料份额一项失败，3% 门槛保持不变，ABA 未准入。',
            '下一步在已研究的最细 48 层/32 阶设置下执行新完整耦合控制，随后重新执行全部原精度检查。',
            '没有局部归一化、删去端部、拟合修正系数或精度资格提升；消去求和仍不等于完整吸收/源粒子平衡证明。']
        with (OUT / 'REPORT.txt').open('x') as stream:
            stream.write('\n'.join(lines)+'\n')
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        for name,wanted in declaration['files'].items():
            if angular.mesh.base.digest(name) != wanted:
                result.update(classification='INPUT_CHANGED',error='changed: '+name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        angular.mesh.base.write_new(OUT / 'result.json',result)
        angular.mesh.base.write_new(OUT / 'seal.json',dict(schema='AXMAT_IMMUTABLE_COLD_ANGULAR_CLOSEOUT_V1',
            files={str(p.relative_to(OUT)):angular.mesh.base.digest(p) for p in OUT.rglob('*')
                   if p.is_file() and p.name != 'seal.json'}))
    print(json.dumps({k:v for k,v in result.items() if k not in ('resources','comparisons','locations','kernels')},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)

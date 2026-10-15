"""Read-only source/metadata route review; no business imports or execution."""
import ast
import hashlib
import json
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/wen/spot')
AM = ROOT / 'validation/axial_material'
ART = ROOT / 'validation/artifacts'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OLD_SOURCE = ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005'
F = Path('/private/tmp/axmat_v12_final_cold_input_candidates_20261009/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py')
PEER = Path('/private/tmp/axmat_AAA_to_ABA_original_gate_route_readonly_20261009')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def identity(path):
    s = path.lstat()
    assert path.is_file() and not path.is_symlink(), str(path)
    return {k: getattr(s, k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}

def put(name, value):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')

files = [
    F,
    ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py',
    AM / 'prepare_qualified_AAA_source_factor_reference_analysis.py',
    AM / 'prepare_qualified_AAA_rank1_cache_monitored_graph_reference.py',
    AM / 'review_qualified_AAA_refined_input_identity.py',
    AM / 'prepare_qualified_AAA_refined_reference_analysis.py',
    AM / 'prepare_qualified_ABA_rank1_cache_execution.py',
    AM / 'prepare_qualified_ABA_rank1_cache_ce_reference.py',
    OLD_SOURCE / 'refined_reference_analysis_recipe.json',
    ART / 'axial-material-AAA-white-trace-refined-closeout-20261005/REPORT.txt',
    ART / 'axial-material-AAA-source-factor-closeout-20261006/REPORT.txt',
    CE / 'AAA/execution.json', CE / 'AAA/native_result.json',
    CE / 'AAA/measurement_admission.json', CE / 'statistical_rules.json',
    CE / 'balance_symmetry_rules.json', CE / 'AAA/reference_contract.json',
    PEER / 'REPORT.json', PEER / 'actual_readonly_tool_return.json',
]
recipe = json.loads((OLD_SOURCE / 'refined_reference_analysis_recipe.json').read_bytes())
files += [Path(v['path']) for v in recipe['unchanged_reference_implementations'].values()]
before = {str(p): identity(p) for p in files}
payloads = {str(p): p.read_bytes() for p in files}
pins = {str(p): dict(path=str(p), sha256=sha(payloads[str(p)]), size_bytes=len(payloads[str(p)]), identity=before[str(p)]) for p in files}

assert pins[str(F)]['sha256'] == '7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71'
controller = files[1]
assert pins[str(controller)]['sha256'] == '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
assert pins[str(OLD_SOURCE / 'refined_reference_analysis_recipe.json')]['sha256'] == '56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806'
for item in recipe['unchanged_reference_implementations'].values():
    assert pins[item['path']]['sha256'] == item['sha256']
for key in ('reference_execution', 'complete_independent_native_sample'):
    assert pins[recipe[key]['path']]['sha256'] == recipe[key]['sha256']
assert pins[str(PEER / 'REPORT.json')]['sha256'] == '3a58817cfacc687e27c65a77d075ad953ab7428b8d7a6ddf0742f76c663b882c'
assert pins[str(PEER / 'actual_readonly_tool_return.json')]['sha256'] == '3c012c509da8bbe096039ca2b386926187fff5d554a30eabc027e2a9205af426'

gates = ['input_equivalence','source_convergence','block_stability','statistical_resolution','keff','scalar_flux','nu_fission','currents_balance_symmetry']
assert recipe['original_eight_checks'] == gates
assert recipe['fixed_history'] == dict(inactive_batches=100, active_batches=2000, particles_per_generation=10000,
    generations_per_batch=10, first_active=101, last_active=2100, raw_generation_entries=21000, batched_generation_entries=2100)
assert recipe['original_analysis_total_wall_seconds'] == 120

def inventory(path):
    t = ast.parse(payloads[str(path)])
    result = {}
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[n.name] = {'line':n.lineno,'end_line':n.end_lineno}
    return result

source_lines = {str(p): inventory(p) for p in files if p.suffix == '.py'}
ft = ast.parse(payloads[str(F)])
constants = {}
for n in ft.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        try:
            constants[n.targets[0].id] = ast.literal_eval(n.value)
        except (ValueError, TypeError):
            pass
assert 'choices' not in constants
ftext = payloads[str(F)].decode()
assert "p=require(expected_prepared['path'],prepared_sha)" in ftext
assert "expected_prepared=dict(path=str(OUTPUT/'prepared_cold.json')" in ftext
assert 'mandatory_original2000_eight_gate_and120_reference_closeout_pending=True' in ftext
assert "choices=('declare','prepare','prepare-binding','run-controls','finalize-cold','run-AAA')" in ftext
assert 'run-ABA' not in ftext
raw_stat = Path(recipe['unchanged_reference_implementations']['reference_statistics.py']['path'])
stat_text = payloads[str(raw_stat)].decode()
assert 'active_batches=2000' in stat_text and 'particles=10000, generations_per_batch=10' in stat_text
rules = json.loads(payloads[str(CE / 'statistical_rules.json')])
assert rules['active_batches'] == 2000 and rules['generations_per_batch'] == 10
assert rules['flux_l2_target'] == .01 and rules['fuel_fission_max_target'] == .03
assert rules['block_lengths'] == [5,10] and rules['bootstrap_replicates'] == 4000
assert rules['k_base_allowance_pcm'] == 500.0 and rules['k_sigma_multiplier'] == 3.0 and rules['k_sigma_pcm_max'] == 50
native = json.loads(payloads[str(CE / 'AAA/native_result.json')])
assert native['status'] == 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS' and type(native['returncode']) is int and native['returncode'] == 0 and native['error'] is None
names = [f'statepoint.{i:04d}.h5' for i in range(101,2101)]
assert {x for x in native['outputs'] if x.startswith('statepoint.') and x.endswith('.h5')} == set(names)
statepoints = [CE / 'AAA' / n for n in names]
sample_before = {str(p): identity(p) for p in statepoints}
assert len(sample_before) == 2000
sample_digest = sha(json.dumps(sample_before, sort_keys=True, separators=(',',':')).encode())
sample_bytes = sum(x['st_size'] for x in sample_before.values())
contract = json.loads(payloads[str(CE / 'AAA/reference_contract.json')])
assert contract['case'] == 'AAA' and len(contract['region_layer_bins']) == 96 and len(contract['plane_bins']) == 13

monitored = AM / 'prepare_qualified_AAA_rank1_cache_monitored_graph_reference.py'
mt = payloads[str(monitored)].decode()
assert 'TOTAL_WALL, RSS_CAP, RESERVE = 120, 512, 256 * 2**20' in mt
run_segment = ast.get_source_segment(mt, next(n for n in ast.parse(mt).body if isinstance(n, ast.FunctionDef) and n.name == 'run'))
assert run_segment.index('started = time.monotonic()') < run_segment.index('d, actual = admission(')
assert 'total_wall_scope="Run entry through actual complete closeout tail; all six stages and native export included"' in mt

after = {str(p): identity(p) for p in files}
assert before == after
assert sample_before == {str(p): identity(p) for p in statepoints}

report = dict(
    schema='SPOT_V12_ORIGINAL_AAA_REFERENCE_TO_ABA_SOURCE_ROUTE_READONLY_V1',
    status='PASS_SOURCE_ROUTE_ONLY',
    current_numerical_reference_ready=False,
    scientific_qualification=False, AAA_accuracy_qualified=False, ABA_admitted=False,
    business_imports=0, business_calls=0, numerical_children=0, fixtures_run=0, root_polling=0, project_written=False,
    reviewed_small_file_count=len(files), reviewed_small_bytes=sum(len(v) for v in payloads.values()),
    source_and_metadata_pins=pins,
    source_function_line_inventory=source_lines,
    immutable_identities_before_after_equal=True,
    child_ABA_route=dict(report=pins[str(PEER/'REPORT.json')], actual_receipt=pins[str(PEER/'actual_readonly_tool_return.json')]),
    reference_dependency=dict(recipe=pins[str(OLD_SOURCE/'refined_reference_analysis_recipe.json')],
       CE_root=str(CE), fixed_history=recipe['fixed_history'], original_eight_checks=gates,
       statepoint_paths_count=2000, statepoint_logical_bytes=sample_bytes, statepoint_seven_identity_set_sha256=sample_digest,
       statepoint_metadata_before_after_equal=True, statepoint_payload_byte_hashes_reverified_in_this_review=False,
       original_native_result=pins[str(CE/'AAA/native_result.json')], original_execution=pins[str(CE/'AAA/execution.json')],
       statistical_rules=pins[str(CE/'statistical_rules.json')], contract=pins[str(CE/'AAA/reference_contract.json')],
       immutable_statistics_implementation=recipe['unchanged_reference_implementations']['reference_statistics.py'],
       note='原sample可作为待核依赖。当前仅2000文件元数据fresh完整；未来实际分析须全SHA与完整历史重验，当前不替代该门。'),
    required_current_parameter_sources=[
       dict(parameter='CURRENT_PREPARED_PATH/SHA', source='actual V12 WORK/prepared_cold.json and successful run-AAA Root terminal prepared descriptor', rule='AAA status.prepared_sha256与collector/physical/qualify_aba全处必须一致；不改原standard prepared.json冒充coldSHA'),
       dict(parameter='CURRENT_STATUS_PATH/SHA', source='actual V12 WORK/AAA/run_status.json after genuine run-AAA exit0', rule='WAITING_REFERENCE/caseAAA/VALID_MET/连续maps至首次MET/全部stage+seals+ownPID512/原43200完整尾'),
       dict(parameter='CURRENT_FINAL', source='status.cases.AAA.final_directory', rule='必须是WORK/AAA/mapNNN；所有archives/training/bootstrap/maps封存。读该final/closed_axial.xsm，不指定旧map012'),
       dict(parameter='CURRENT_SPEC/RANK/BASIS/EXPERIMENT', source='actual prepared.case_spec/rank_addendum/experiment_id; WORK/training/common_basis.xsm', rule='完整typed源值/SHA，不借旧experiment或固定k/nu_fission结果'),
       dict(parameter='CURRENT_BUILD_AND_FULL_INPUT_CHAIN', source='actual V11 component seal5517/source admission/object/runtime + actual V12 combined seal1f0/TERM3966/PREPf431/whole INPUT durable ten-member Root449d and Rootadmissionc47dfa', rule='新component仅INPUT资格；analysis需精确source/current runtime/whole65七body/current owner图/物理字段；不能调用旧92d build资格给新kernel'),
       dict(parameter='CURRENT_COLD_SOURCE/DECL/PREP/BINDING/CONTROL/FINALIZATION/TERMINAL', source='genuine actual V12阶段 Root receipt与SOURCE/WORK/TERM/CT小proof', rule='future未取得保持None；currentcoldterminal完整封存+4tails不可以源码READY代替'),
       dict(parameter='STAGED_EXPORT_INPUTS', source='WORK/AAA/bootstrap/initial_axial_track.xsm; currentfinal/closed_axial.xsm; WORK/AAA/bootstrap/initial_axial_macrolib.xsm', rule='每源实际SHA/不可变stage receipt；track/axial/macro独立副本，原exporter81da2+fdfb unchanged'),
       dict(parameter='COLLECTOR_RECEIPT', source='fresh exported/physical/projection/statistics/currents/measurement bindings; generated collector actual declarationSHA', rule='formal新receipt须由原collector派生，whole2000/21000/2100/type等完整，不能手填8PASS'),
    ],
    analysis_execution_source_template=dict(
       primary=str(monitored), scientific_ancestor=str(AM/'prepare_qualified_AAA_source_factor_reference_analysis.py'),
       cli_declare=['ANALYSIS_P12','NEW_REVIEWED_REFERENCE_FACTORY','declare','--prepared-sha256','ACTUAL_V12_COLD_PREPARED_SHA','--status-sha256','ACTUAL_V12_AAA_STATUS_SHA','--build-seal-sha256','ACTUAL_V11_COMPONENT_SEAL','--build-terminal-evidence','ACTUAL_V11_COMPONENT_ROOT_TERMINAL_PATH','--build-terminal-evidence-sha256','ACTUAL_V11_COMPONENT_ROOT_TERMINAL_SHA'],
       cli_prepare=['ANALYSIS_P12','NEW_REVIEWED_REFERENCE_FACTORY','prepare','--sha256','ACTUAL_NEW_REFERENCE_DECL_SHA','--input-terminal-evidence-sha256','ACTUAL_NEW_REFERENCE_DECL_ROOT_RECEIPT_SHA'],
       cli_run=['ANALYSIS_P12','NEW_REVIEWED_REFERENCE_FACTORY','run','--sha256','ACTUAL_NEW_REFERENCE_DECL_SHA','--input-terminal-evidence-sha256','ACTUAL_NEW_REFERENCE_DECL_ROOT_RECEIPT_SHA'],
       cli_qualification=['ANALYSIS_P12','NEW_REVIEWED_REFERENCE_FACTORY','admit-qualification','--sha256','ACTUAL_NEW_REFERENCE_SEAL_SHA','--qualification-sha256','ACTUAL_NEW_FORMAL_QUALIFICATION_SHA','--terminal-evidence','ACTUAL_NEW_REFERENCE_ROOT_EXIT0_RECEIPT_PATH','--terminal-evidence-sha256','ACTUAL_NEW_REFERENCE_ROOT_EXIT0_RECEIPT_SHA'],
       all_cli_templates_not_executed=True,
       no_as_is_v12_ready_claim='旧factory PROD/BUILD/controller身份、prepared.json字面、coupling schema/cache observer与旧source图写死；需新独立roots+精确身份/source/完整当前输入接线及inverse审，不可直接运行旧脚本。V12新coldF没有run-ABA CLI。'),
    six_analysis_stages=[
       dict(label='fine/export',source='原export_observables executable',arguments=['track.xsm','axial.xsm','macro.xsm','observables'],cwd='NEW_REFERENCE_OUT/fine',max_seconds=60),
       dict(label='fine/physical',source='原review_qualified_AAA_refined_input_identity.py仅当前来源路径/SHA与prepared_cold basename接线',arguments=['ANALYSIS_P12','NEW_OUT/runtime/current_physical_identity.py']),
       dict(label='AAA/project',source='原完整fine checks + 固定48→12 conservative projection',arguments=['ANALYSIS_P12','NEW_FACTORY','project-worker','--sha256','ACTUAL_DECL_SHA']),
       dict(label='AAA/statistics',source=recipe['unchanged_reference_implementations']['reference_statistics.py'],arguments=['ANALYSIS_P12','NEW_OUT/runtime/reference_statistics.py','analyze','--rules','NEW_OUT/statistical_rules.json','--case-spec','NEW_OUT/observation_case_spec.json','--contract',str(CE/'AAA/reference_contract.json'),'--statepoints',str(CE/'AAA'),'--production-regions','NEW_OUT/observation/observables.regions.csv','--production-summary','NEW_OUT/observation/observables.summary.txt','--output','NEW_OUT/AAA/statistics.json']),
       dict(label='AAA/currents',source=recipe['unchanged_reference_implementations']['compare_balance_symmetry.py'],arguments=['ANALYSIS_P12','NEW_OUT/runtime/compare_balance_symmetry.py','compare','--rules','NEW_OUT/balance_symmetry_rules.json','--statistics-rules','NEW_OUT/statistical_rules.json','SAME_COMMON_SPEC_CONTRACT_STATEPOINT_REGION_SUMMARY_ARGS','--production-faces','NEW_OUT/observation/observables.faces.csv','--output','NEW_OUT/AAA/currents_balance_symmetry.json']),
       dict(label='AAA/collect',source=recipe['unchanged_reference_implementations']['assess_qualified_AAA_white_trace_precision.py'],arguments=['ANALYSIS_P12','NEW_OUT/runtime/current_reference_collector.py','ACTUAL_DECL_SHA'],output='assessment + only all8PASS pending receipt, publication/terminal eligibility separate'),
    ],
    preserved_budgets=dict(analysis_whole_seconds=120, analysis_clock='run entry includes initial admission, all6 stages, final fullINPUT/immutable/resource checks, publication/hash/seal and four tail fields', native_export_seconds=60, own_pid_rss_mib=512, children=1,threads=1,retries=0,archive_source_plus_out_bytes=256*2**20,history_bytes=96*2**30,min_disk_free_bytes=8*2**30,producer='original P14 separately pinned',analysis='original P12/OpenMC/Numpy separately pinned', no_work_moved_outside_timer=True),
    all_eight_gates=gates,
    scientific_thresholds=dict(flux_volume_weighted_global_normalized_l2=.01, fuel_normalized_nu_fission_max=.03, block_lengths=[5,10], bootstrap_replicates=4000, quantiles=[.05,.95],keff_abs_reactivity_pcm='500+3*sigma_pcm', keff_sigma_pcm_max=50, z_max=3.29,lag1_abs_max=.5, physical_volume_relative_tolerance=5e-6, independent_current_full_neutron_balance='NOT_ASSESSED without independent absorption/source tally; keep original current/symmetry gate, no invented threshold'),
    reusable_old_sample_conditions=[
       '新实际AAA完整MET/WAITING_REFERENCE与原whole输入/所有源/原物理参数匹配；新saved fine字段完整export原REAL64/SN32而非旧观测拷贝。',
       '新archives所有AAA材料槽MICROLIB2同A snapshot的名称、混合编号、密度、温度、使用/体积、ENERGY字节；TRACK radial/white/vacuum/material/geometry/boundary与原匹配。',
       '实际48单元各3.125cm、3区各50cm，原12观测单元12.5cm；384完整volume→96bins/13planes，原5e-6volume tolerance与全global nu-fission normalization；所有finechecks先PASS，不删bin/fit。',
       'CE execution/native/log/model/libraries/sampling/source proofs fullSHA及2000连续statepoints全SHA保持，原k_generation/entropy各21000raw、2100batched、10代聚合及所有统计充分门完整。',
       'recipe与旧measurement/inputphysical仅dependency，当前newphysical/export/projection/measurement/collector receipt重新绑定actualnewprepared/status/final/spec/rank/basis/currentruntime。',
    ],
    actual_new_reference_transport_required_if=[
       '当前物理材料组分/密度/温度/核数据源、几何/边界/参考模型或tally契约有改变，原样本不再覆盖目标物理状态；需先新独立采样声明与源审，不能直接借AAA旧sample。',
       '完整2000statepoints/history/provenance或original reference model/library/executable identity不能验证；若精确恢复不可行需新独立参考计算，不得截短原样本。',
       '原统计规则判reference统计不足或source/history不稳定：保持INCONCLUSIVE；追加/重算采样必须新预声明并独立审查，不是本recipe授权，不能事后调block/门槛或偷偷拼样本。',
       '进入真正ABA后材料槽为ABA，AAA样本不能证明ABA；原ABA CE入口要求新ABA物理/观测/完整独立sample与资格。',
    ],
    not_automatic_new_transport_reason='仅storage/缓存/运行时/source身份变更且新物理匹配PASS，不自动要求另跑AAA CE；nu_fission确定FAIL也不能靠重抽样/拟合掩盖。当前V12物理匹配尚未来，不能预先断言样本已可消费。',
    current_qualification_blockers=[
       '当前V12真正冷AAA成功/WAITING_REFERENCE与当前observables/physical/collector/qualification均未来，不允许填成功。',
       '旧refined/source-factor 7PASS+nu_fissionFAIL；后续rank1 monitored参考虽6stages完成，仍nu_fissionFAIL且120s fullcloseout失败。旧qualification不能转移。',
       '原120秒预算已有真实entry重复准入/最终closeout耗时失败；新参考接线必须以完整原INPUT/科学体等价保持降低重复驻留/重读成本，不能移计时、减范围、信stat代替fullSHA或加时。',
       '新V12独立reference factory及ABA ownPID-bound wrapper尚未实现/审查，旧脚本硬绑定旧身份；不授新当前CLI READY。',
    ],
    actual_readonly_tool_terminal=None,
)
put('REPORT.json',report)
put('small_source_evidence_manifest.json',{'schema':'READONLY_ROUTE_SMALL_SOURCE_EVIDENCE_MANIFEST_V1','pins':pins,'function_line_inventory':source_lines})
text = '''V12 AAA 独立精度验收 → ABA 原路线（只读源码准备，尚未运行）

结论：先完成新的冷 AAA，真实退出 0、完整 ownPID512/阶段封存/四尾门通过且 WAITING_REFERENCE/VALID_MET，才能做独立参考复核。旧 refined/source-factor 的七通过一失败不是新 V12 资格。

1. 当前身份从哪取
用真正 WORK/prepared_cold.json（其 SHA 是冷 AAA status 和 Root terminal 绑定的 SHA），不能错用旧标准 prepared.json 的 SHA。真实 status.cases.AAA.final_directory 决定导出 closed_axial；bootstrap 的 initial_axial_track / initial_axial_macrolib 另两项按实际封存绑定。当前 prepared 中的完整 case_spec/rank_addendum、training/common_basis、current runtime、V11 component/V12 full INPUT/cold 真实来源链均重新接入。

2. 完整参考与旧数据复用条件
原 recipe56ebbf 固定 100 inactive +2000 active（0101..2100）、10000 particles/10代；k/entropy 每项保留21000 raw+2100 batch。原 CE sample metadata 2000 文件仍在（439558000字节），本次没有重哈H5内容。未来真正复核须全SHA+模型/核数据/日志来源与完整历史。必须新导出全部48单元实数观测、新核材料/温度/密度/核数据、radial/white/vacuum/geometry，384 fine volume完整合并96观察bins并保留13planes。只有这些新物理等价检查通过，旧独立样本才能用于新结果；不能借旧 assessment/qualification。若物理/参考契约变更或原完整证据无法恢复验证，才需要新独立参考输运。统计不足必须INCONCLUSIVE，追加采样另行预声明，不能重抽样掩盖确定FAIL。

3. 可复用的原执行接口
原 prepare_qualified_AAA_rank1_cache_monitored_graph_reference.py 的 declare/prepare/run/admit-qualification 是完整有界接口祖先。必须另建当前身份 source/OUT/TERM 并 source inverse审查：旧PROD/BUILD/controller/schema/observer/旧图与prepared.json路径不能原样调用V12。参考分析用原P12环境，生产仍P14。尤其复制 recipe冻结 reference_statistics.py（1578b8…；active2000/10代），不要换成AM通用默认250/1代版本。
六个原stage：fine/export、fine/physical、AAA/project、AAA/statistics、AAA/currents、AAA/collect。参数模板和精确源行号见机器报告。原120秒从run入口完整覆盖准入、导出、六stage、最终全输入核验和发布/hash/seal/四尾；export60秒、ownRSS512、1线程/1子/0retry、SOURCE+OUT256MiB、history96GiB/free8全部保留。前次实际120秒失败是落实路线风险，不能调整门槛或挪出计时。

4. 八门及资格发布
input_equivalence/source_convergence/block_stability/statistical_resolution/keff/scalar_flux/nu_fission/currents_balance_symmetry 必须全PASS。原通量全局体积加权L2 1%、燃料nu-fission最大差3%、keff允许500+3sigma pcm且sigma<=50；block5/10与4000bootstrap/完整entropy等不变。原collector从当前证据派生prepared/spec/rank/basis/status和三份独立报告receipt。pending不准入；正式receipt+完整科学seal+真实Root0/完整stdout+最终四尾+原qualify_aba全部通过，才允许下一阶段。

5. ABA 入口
等价原入口是当前 production_runner run CURRENT_PREPARED --sha256 CURRENT_SHA --case ABA --reference-qualification CURRENT_FORMAL_Q --reference-sha256 CURRENT_Q_SHA；原qualify_aba先于创建ABA。新V12 coldF目前没有run-ABA，下一步须从原guarded ABA execution祖先精确接线保持ownPID512/原预算，不直接裸跑旧wrapper。ABA重新bootstrap/mapping，数值MET后仍WAITING_REFERENCE；AAA旧sample不能证明ABA，需后续独立ABA参考。

当前仅源路线PASS，future reference/AAA/ABA全部未知。所有读取证据保持七项身份前后相同。无业务import/call、CLI执行、fixture、Root轮询、数值子进程或项目写；实际只读工具终态另存回执。
'''
with (OUT / 'REPORT.txt').open('x', encoding='utf-8') as f:
    f.write(text)
print(json.dumps({'status':report['status'],'report_sha256':sha((OUT/'REPORT.json').read_bytes()),'small_files':len(files),'small_bytes':report['reviewed_small_bytes'],'statepoint_metadata_count':2000,'project_written':False,'business_calls':0},ensure_ascii=False))

"""Finite source/metadata review; no business module is loaded or executed."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

D = Path(__file__).parent
ROOT = Path('/Users/wen/spot')
A = ROOT / 'validation/axial_material'
B = ROOT / 'validation/artifacts'
CE = B / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OLD_SOURCE = B / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005'
F = A / 'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
WORK = B / 'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
MF = A / 'prepare_qualified_AAA_rank1_cache_monitored_graph_reference.py'
P12 = '/Users/wen/miniforge3/envs/openmc-dev/bin/python'
PINS = {}

def identity(path):
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode), str(path)
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def read(path, wanted=None):
    path = Path(path)
    before = identity(path)
    raw = path.read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    assert before == identity(path), str(path)
    if wanted is not None:
        assert observed == wanted, (str(path), observed, wanted)
    PINS[str(path)] = dict(sha256=observed, bytes=len(raw), identity=before)
    return raw

def js(path, wanted=None):
    return json.loads(read(path, wanted))

def source(path, wanted=None):
    text = read(path, wanted).decode('utf-8')
    return text, ast.parse(text)

def anchor(path, tree, name):
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    assert len(nodes) == 1, name
    n = nodes[0]
    return dict(path=str(path), function=name, first_line=n.lineno, last_line=n.end_lineno)

recipe_path = OLD_SOURCE / 'refined_reference_analysis_recipe.json'
recipe = js(recipe_path, '56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806')
gates = ['input_equivalence', 'source_convergence', 'block_stability', 'statistical_resolution',
         'keff', 'scalar_flux', 'nu_fission', 'currents_balance_symmetry']
history = dict(inactive_batches=100, active_batches=2000, particles_per_generation=10000,
    generations_per_batch=10, first_active=101, last_active=2100,
    raw_generation_entries=21000, batched_generation_entries=2100)
assert recipe['original_eight_checks'] == gates
assert recipe['fixed_history'] == history
assert recipe['original_analysis_total_wall_seconds'] == 120
assert recipe['reference_analysis_threads'] == 1 and recipe['retries'] == 0
assert recipe['aggregate_history_cap_bytes'] == 96 * 2**30
assert recipe['min_free_bytes'] == 8 * 2**30
assert all(recipe[k] is False for k in ['AAA_accuracy_qualified', 'ABA_admitted', 'new_transport_launched', 'analysis_executed'])
for k in ['refined_prepared', 'reference_execution', 'complete_independent_native_sample',
          'original_candidate_assessment', 'observation_projection_recipe', 'projection_precheck',
          'native_export_source_proof', 'physical_input_precheck']:
    item = recipe[k]
    read(item['path'], item['sha256'])
for item in recipe['unchanged_reference_implementations'].values():
    read(item['path'], item['sha256'])
projection = js(recipe['observation_projection_recipe']['path'])
read(projection['helper']['path'], projection['helper']['sha256'])
assert projection['native_axial_cells'] == 48 and projection['original_observation_cells'] == 12
assert projection['local_fitting_or_normalization'] is False and projection['bins_removed'] is False
assert projection['complete_fine_admission_required_first'] is True

execution = js(CE / 'AAA/execution.json', recipe['reference_execution']['sha256'])
native = js(CE / 'AAA/native_result.json', recipe['complete_independent_native_sample']['sha256'])
assessment = js(CE / 'AAA/reference_assessment.json', recipe['original_candidate_assessment']['sha256'])
assert native['status'] == 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
assert type(native['returncode']) is int and native['returncode'] == 0 and native['error'] is None
assert native['scientific_acceptance'] is False
assert assessment['classification'] == 'AAA_REFERENCE_NOT_QUALIFIED'
assert assessment['checks']['nu_fission'] == 'FAIL'
assert assessment['ABA_admitted'] is False
expected_statepoints = [f'statepoint.{batch:04d}.h5' for batch in range(101, 2101)]
assert sorted(k for k in native['outputs'] if k.startswith('statepoint.') and k.endswith('.h5')) == expected_statepoints
statepoint_records = []
for name in expected_statepoints:
    path = CE / 'AAA' / name
    statepoint_records.append([str(path), identity(path), native['outputs'][name]])
statepoint_identity_digest = hashlib.sha256(json.dumps(statepoint_records, separators=(',', ':')).encode()).hexdigest()
statepoint_logical_bytes = sum(row[1][3] for row in statepoint_records)
del statepoint_records
contract = js(CE / 'AAA/reference_contract.json', execution['files'][str(CE / 'AAA/reference_contract.json')])
assert contract['statepoint_batches'] == list(range(101, 2101))
assert contract['statepoint_every_active_batch'] is True
assert contract['config']['active'] == 2000 and contract['config']['inactive'] == 100
assert contract['config']['particles'] == 10000 and contract['config']['generations_per_batch'] == 10
assert contract['config']['seed'] == 310031
sampling = js(CE / 'declaration.json', execution['files'][str(CE / 'declaration.json')])
rules = js(CE / 'statistical_rules.json', execution['files'][str(CE / 'statistical_rules.json')])
currents_rules = js(CE / 'balance_symmetry_rules.json', execution['files'][str(CE / 'balance_symmetry_rules.json')])
sampling_review = js(CE / 'input_sampling_review.json', execution['files'][str(CE / 'input_sampling_review.json')])
transport_resource = js(CE / 'resource_addendum.json', execution['files'][str(CE / 'resource_addendum.json')])
assert sampling['formal']['active_batches'] == 2000 and sampling['formal']['total_histories'] == 210000000
assert sampling['original_numerical_acceptance_thresholds_changed'] is False
assert sampling_review['all_numerical_acceptance_thresholds_unchanged'] is True
assert rules['active_batches'] == 2000 and currents_rules['active_batches'] == 2000
assert rules['fuel_fission_max_target'] == 0.03 and rules['flux_l2_target'] == 0.01
assert rules['block_lengths'] == [5, 10] and rules['bootstrap_replicates'] == 4000
assert rules['lower_quantile'] == 0.05 and rules['upper_quantile'] == 0.95
assert transport_resource['formal_ce_wall_seconds_per_case'] == 64800
assert execution['wall_seconds'] == 64800 and execution['threads'] == 1

producer_path = A / 'prepare_qualified_AAA_ce_white_trace_precision_specpin.py'
producer, producer_ast = source(producer_path, execution['files'][str(producer_path)])
prior_rejected_path = A / 'prepare_qualified_AAA_ce_white_trace_precision.py'
source(prior_rejected_path, execution['files'][str(prior_rejected_path)])
executor_path = CE / 'runtime/ce_execution.py'
executor, executor_ast = source(executor_path, execution['files'][str(executor_path)])
stats_path = Path(recipe['unchanged_reference_implementations']['reference_statistics.py']['path'])
stats, stats_ast = source(stats_path)
collector_path = Path(recipe['unchanged_reference_implementations']['assess_qualified_AAA_white_trace_precision.py']['path'])
collector, collector_ast = source(collector_path)
monitor, monitor_ast = source(MF)
ftext, fast = source(F, '59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8')
for text, tokens in [(producer, ['ACTIVE, INACTIVE, GPB, NP, WALL = 2000, 100, 10, 10000, 64800', "range(INACTIVE+1,INACTIVE+ACTIVE+1)"]),
    (executor, ["[contract['executable'], '-s', '1']", 'start_new_session=True']),
    (stats, ["for current in range(inactive+1,inactive+active+1)", "raw_generation_history" if 'raw_generation_history' in stats else "raw_k_generation", "uppers[:,index].max()<=targets[index]", "lowers[:,index].min()>targets[index]"]),
    (collector, ['range(101, 2101)', '(21000,)', '(2100,)', 'all(value == "PASS" for value in checks.values())']),
    (monitor, ['TOTAL_WALL, RSS_CAP, RESERVE = 120, 512, 256 * 2**20', 'old_assessment_or_qualification_inherited=False', 'actual_new_candidate_receipt_required=True', 'numeric_children_at_once=1', 'native_export_stage_wall_seconds=60']),
    (ftext, ['contract["retained_reference"]["active_batches"] != 2000', 'range(101, 2101)'])]:
    for token in tokens:
        assert token in text, token
prepared = js(WORK / 'prepared_cold.json', '1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
case = js(prepared['case_spec']['path'], prepared['case_spec']['sha256'])
assert case['reference']['active_batches'] == 250
assert prepared['production_config']['cells_per_zone'] == 16 and prepared['production_config']['sn'] == 32
legacy_policy = js('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009/REPORT.json',
                   'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')['reference_policy_boundary']
assert legacy_policy['source_recipe_sha256'] == PINS[str(recipe_path)]['sha256']
assert legacy_policy['unchanged_legacy_case_spec_active_batches'] == 250
assert legacy_policy['separate_frozen_recipe_fixed_history_active_batches'] == 2000

anchors = {
    'original_CE_preparation': anchor(producer_path, producer_ast, 'main'),
    'original_CE_transport': anchor(executor_path, executor_ast, 'execute'),
    'original_CE_cli': anchor(executor_path, executor_ast, 'main'),
    'complete_consecutive_history': anchor(stats_path, stats_ast, 'extract_statepoints'),
    'all_statistical_gates': anchor(stats_path, stats_ast, 'analyze_batches'),
    'original_unanimous_collector': anchor(collector_path, collector_ast, 'main'),
    **{name: anchor(MF, monitor_ast, name) for name in ['candidate_completion', 'ready', 'declare', 'prepare',
       'project_worker', 'run', 'external_terminal_admission', 'qualification_admission']},
    'V9_preserved_reference_policy': anchor(F, fast, 'declare')}
common = ['--case-spec', '<NEW_ANALYSIS_OUT>/observation_case_spec.json', '--contract', str(CE / 'AAA/reference_contract.json'),
    '--statepoints', str(CE / 'AAA'), '--production-regions', '<NEW_ANALYSIS_OUT>/observation/observables.regions.csv',
    '--production-summary', '<NEW_ANALYSIS_OUT>/observation/observables.summary.txt']
plan = [
    dict(label='fine/export', cwd='<NEW_ANALYSIS_OUT>/fine', argv=[str(B/'axial-material-tools-20261003/export_observables'), 'track.xsm', 'axial.xsm', 'macro.xsm', 'observables']),
    dict(label='fine/physical', cwd='<NEW_ANALYSIS_OUT>/fine', argv=[P12, '<NEW_ANALYSIS_OUT>/runtime/rank1_factor_cache_physical_identity.py']),
    dict(label='AAA/project', cwd='<NEW_ANALYSIS_OUT>/AAA', argv=[P12, '<NEW_SOURCE_APPROVED_REFERENCE_FACTORY>', 'project-worker', '--sha256', '<NEW_REFERENCE_DECL_SHA>']),
    dict(label='AAA/statistics', cwd='<NEW_ANALYSIS_OUT>/AAA', argv=[P12, '<NEW_ANALYSIS_OUT>/runtime/reference_statistics.py', 'analyze', '--rules', '<NEW_ANALYSIS_OUT>/statistical_rules.json', *common, '--output', '<NEW_ANALYSIS_OUT>/AAA/statistics.json']),
    dict(label='AAA/currents', cwd='<NEW_ANALYSIS_OUT>/AAA', argv=[P12, '<NEW_ANALYSIS_OUT>/runtime/compare_balance_symmetry.py', 'compare', '--rules', '<NEW_ANALYSIS_OUT>/balance_symmetry_rules.json', '--statistics-rules', '<NEW_ANALYSIS_OUT>/statistical_rules.json', *common, '--production-faces', '<NEW_ANALYSIS_OUT>/observation/observables.faces.csv', '--output', '<NEW_ANALYSIS_OUT>/AAA/currents_balance_symmetry.json']),
    dict(label='AAA/collect', cwd='<NEW_ANALYSIS_OUT>/AAA', argv=[P12, '<NEW_ANALYSIS_OUT>/runtime/rank1_factor_cache_reference_collector.py', '<NEW_REFERENCE_DECL_SHA>'])]

report = dict(schema='AXMAT_V9_ORIGINAL_COMPLETE_REFERENCE_NEXT_STEP_SOURCE_CONTRACT_REVIEW_V1',
    status='PASS', scope='SOURCE_AND_SMALL_METADATA_ONLY_NOT_EXECUTION_OR_ACCURACY_ADMISSION',
    project_written=False, business_imports_or_runs=0, numerical_recomputations=0,
    statepoint_numerical_bytes_read=0, canonical_35GB_bytes_read=0,
    original_producer_exists=True, source_approved_V9_reference_producer_or_analysis_binding_provided=False,
    v9_reference_ready_for_execution=False,
    original_recipe=dict(path=str(recipe_path), sha256=PINS[str(recipe_path)]['sha256'], fixed_history=history,
        original_eight_checks=gates, policies={k: recipe[k] for k in ['existing_sample_policy', 'comparison_policy', 'rule_policy', 'prerequisites', 'collection_policy']}),
    old_CE=dict(root=str(CE), execution=recipe['reference_execution'], native=recipe['complete_independent_native_sample'],
        status=native['status'], returncode=native['returncode'], scientific_acceptance=False,
        statepoint_count=2000, statepoint_names_exact=True, statepoint_present_regular_count=2000,
        statepoint_metadata_identity_digest=statepoint_identity_digest, statepoint_logical_bytes=statepoint_logical_bytes,
        fresh_payload_SHA_or_H5_schema_not_rechecked_in_this_source_scope=True,
        old_assessment_classification=assessment['classification'], old_checks=assessment['checks'], old_accuracy_not_inherited=True),
    original_transport_cli=dict(preparation=[P12, str(producer_path)],
        bounded_launch=[P12, str(executor_path), str(CE/'AAA/execution.json'), '--sha256', recipe['reference_execution']['sha256']],
        child_argv=[execution['executable'], '-s', '1'], cwd=str(CE/'AAA'),
        original_transport_wall_seconds=64800, original_transport_threads=1,
        currently_retained_complete_sample_no_rerun_authorized_by_recipe=True,
        old_roots_exist_no_overwrite_no_retry=True),
    original_monitored_analysis=dict(factory=str(MF), factory_sha256=PINS[str(MF)]['sha256'],
        old_factory_fixed_production_root=str(B/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'),
        direct_old_factory_not_a_V9_binder=True, original_six_stage_command_template=plan,
        template_placeholders_unbound_not_executable=True, total_wall_seconds=120, native_export_stage_wall_seconds=60,
        per_child_rss_cap_mib=512, threads=1, numeric_children_at_once=1, retries=0,
        archive_cap_bytes=256*2**20, complete_dynamic_history_cap_bytes=96*2**30, min_free_bytes=8*2**30,
        exact_CLI_actions_and_flags={
            'declare':['declare','--prepared-sha256','<NEW_V9_ACTUAL_PREPARED_SHA>','--status-sha256','<NEW_V9_ACTUAL_AAA_STATUS_SHA>','--build-seal-sha256','<NEW_V9_BUILD_SEAL_SHA>','--build-terminal-evidence','<NEW_V9_REAL_BUILD_TERMINAL_PATH>','--build-terminal-evidence-sha256','<NEW_V9_REAL_BUILD_TERMINAL_SHA>'],
            'prepare':['prepare','--sha256','<NEW_REFERENCE_DECL_SHA>','--input-terminal-evidence-sha256','<REAL_REFERENCE_DECLARE_ROOT_TERMINAL_SHA>'],
            'run':['run','--sha256','<NEW_REFERENCE_DECL_SHA>','--input-terminal-evidence-sha256','<REAL_REFERENCE_DECLARE_ROOT_TERMINAL_SHA>'],
            'qualification':['admit-qualification','--sha256','<NEW_REFERENCE_SEAL_SHA>','--qualification-sha256','<NEW_UNANIMOUS_QUALIFICATION_SHA>','--terminal-evidence','<REAL_REFERENCE_ROOT_RETURN_PATH>','--terminal-evidence-sha256','<REAL_REFERENCE_ROOT_RETURN_SHA>']}),
    physical_projection=dict(actual_solver_cells=48, actual_solver_SN=32, original_observation_cells=12,
        fixed_four_complete_cells_to_one_original_cell=True, every_radial_region_and_13_original_planes=True,
        original_96_region_cell_bins=True, all_fine_checks_mandatory_before_projection=True,
        global_exporter_nufission_normalization_once=True, fitting_or_removed_bins=False),
    original_accuracy_thresholds=dict(nu_fission_max_fuel_normalized_relative=0.03, scalar_flux_volume_weighted_normalized_l2=0.01,
        pass_rule='Both fixed block lengths: conservative upper95 <= respective original target; all adequacy/source/block/keff/current/input gates must also PASS.',
        fail_rule='Both-block conservative lower05 > respective target gives FAIL; interval crossing target or inadequate evidence remains INCONCLUSIVE.',
        no_point_estimate_or_7_of_8_shortcut=True, original_rule_dictionaries_unchanged=True,
        statistical_rules_path=str(CE/'statistical_rules.json'), statistical_rules_sha256=PINS[str(CE/'statistical_rules.json')]['sha256'],
        currents_rules_path=str(CE/'balance_symmetry_rules.json'), currents_rules_sha256=PINS[str(CE/'balance_symmetry_rules.json')]['sha256']),
    V9_binding_requirements=[
        'After real native AAA ends, require its genuine external Root int0 and full post-admission, current prepared_cold/standard prepared relationship, VALID_MET/WAITING_REFERENCE, common basis, new run-status and all current full stage logs/seals.',
        'Original ready/candidate_completion is hardwired to OLD rank1 roots and checks every stage seal. Source-approved new binding must consume current V9 full completion rather than an old AAA assessment or newly missing old snapshots.',
        'Fresh V9 fine export inputs must be current AAA/bootstrap/initial_axial_track.xsm, current final_directory/closed_axial.xsm, current AAA/bootstrap/initial_axial_macrolib.xsm; bind SHA to new producer and runtime/source identities.',
        'New physical review, native fine export, complete-fine admission and fixed projection receipt must identify this actual V9 candidate. Old refined prechecks are immutable dependencies, not current equivalence evidence.',
        'Retain whole recipe56eb and original CE sample/implementation identities; actual analysis must full-SHA and load all 2000 statepoints and full21000 raw/2100 batched k and entropy histories.',
        'Source-equivalent collector must bind current experiment/prepared/spec/rank/common_basis/run-status plus NEW statistics/input_equivalence/currents_balance_symmetry reports, never CE old prepared88640 nor old rank1 prepared/status.',
        'Preserve full current graph/namespace/alias/owner/resources/terminal admission, source guards, complete six stages, original120/60/512/256MiB/96GiB/free8/thread1/child1/retry0 bounds and actual whole closeout/typed external Root0.',
        'Only unanimous original8 PASS and fresh typed real Root success may publish pending→formal reference qualification and invoke unchanged qualify_aba. FAIL/INCONCLUSIVE produces truthful assessment, no qualification.'],
    current_reference_policy_boundary=legacy_policy,
    future_actual=dict(new_native_root_return=None, new_native_status_sha256=None, new_native_final_stage_sha256=None,
        new_reference_factory_sha256=None, new_reference_declaration_sha256=None, new_reference_output_sha256=None,
        new_statistics=None, new_input_equivalence=None, new_currents_balance_symmetry=None,
        AAA_accuracy_qualified=False, ABA_admitted=False),
    source_anchors=anchors, all_fresh_small_file_pins=PINS,
    limitation='Source-contract discovery only; no new V9/native/reference execution, no API/constructor, no H5 parse/fullSHA, no numerical result or threshold change. New binding is a concrete pending prerequisite, not an invented reduced recipe.')
for path, item in PINS.items():
    assert identity(Path(path)) == item['identity'], path
with (D/'REPORT.json').open('x') as f:
    json.dump(report, f, ensure_ascii=False, indent=2, allow_nan=False); f.write('\n')
with (D/'REPORT.txt').open('x') as f:
    f.write('原完整独立参考契约只读审查：PASS（仅源码与小元数据，不是精度准入）。\n\n'
        '2000活跃批次的原producer、完整CE样本和分析入口均存在。固定100 inactive、2000 active、10000粒子/代、10代/批；statepoint.0101.h5至statepoint.2100.h5全部2000文件当前存在。这里只核文件身份与原manifest，没有读取H5数值或重验其全文SHA。\n'
        '保留recipe56eb：重新读取整个原样本及全部历史，不追加transport、不选子样本、不换阈值；48细格全部先验通过，再按固定4格归并到12观察格/96区域格，保留13平面，仅一次全局nu-fission归一化。\n'
        '原nu-fission阈值3%，scalar flux阈值1%；两个固定block长度都需保守upper95不超原阈值，同时完整八门一致PASS。跨线仍INCONCLUSIVE，不能用点估计或7/8代替。旧assessment恰nu_fission FAIL，其余7门PASS，必须原样保留。\n'
        '原CE生成入口：prepare_qualified_AAA_ce_white_trace_precision_specpin.py；有界执行runtime/ce_execution.py EXECUTION --sha256 17c4…，实际native命令openmc -s 1，原transport cap64800秒。已有完整样本，此recipe不授权重跑transport。\n'
        '原monitored reference factory固定旧rank1目录，不能直接拿来绑定V9；原六阶段export/physical/project/statistics/currents/collect与120秒总cap、首export60秒、512MiB/256MiB归档/96GiB历史/free8/单线程单子进程零重试均须保留。\n'
        '下一步缺项：真实新V9 AAA完成及全后验、当前final_directory/三份导出输入、针对V9源码审过的完整reference绑定、新物理等价/投影/三独立报告及全部八门collect。全部未来SHA仍None。完整CLI/绝对路径/源码行号/当前小pin见REPORT.json。\n'
        '当前case_spec仍250诊断批次；与独立2000批recipe是两个原边界，不修改250、不据此取得精度信用。新native0或VALID_MET也不等于独立accuracy PASS。\n'
        '未import业务、未启动任何参考/native/API、未写项目、未改数值/预算/门。\n')
print(json.dumps(dict(status='PASS', scope=report['scope'], fresh_small_file_pins=len(PINS), statepoint_metadata_count=2000,
    V9_reference_ready_for_execution=False, report_sha256=hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest()), sort_keys=True))

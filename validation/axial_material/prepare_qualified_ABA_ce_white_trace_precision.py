"""Prepare a bounded independent ABA reference only after real prerequisites.

Static preflight never creates the future transport directory. Statistical and
current implementations are byte-identical to the frozen AAA precision run;
the native process lifecycle is unchanged. This is conditional preparation,
not a physical-input, convergence, or independent-accuracy result.
"""
import argparse
import ast
import copy
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
PARENT = ART / 'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
MEASUREMENT = PARENT / 'aba_measurement'
STAGED = PARENT / 'aba_reference_inputs'
AAA_CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OUT = ART / 'axial-material-ce-qualified-ABA-white-trace-precision-20261004'
DECLARATION = MEASUREMENT / 'ce_entry_declaration.json'
EXPORT = ROOT / 'validation/axial_material/export_qualified_ABA_observables_white_trace.py'
EXPORT_SHA = 'e711ce8e52539039185620ccc60631e7944f3f0efb58aeb1afb9c546ad5c4794'
EXPORT_DECL_SHA = 'bde75f434ba237509357fbb2de9bf3fea8e3f0377cf1ea3bb0111ecfc00f8229'
PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
AAA_EXEC_SHA = '17c4e48d4de450bc5e3232caf3238da519f23c3836bd54f0a91d122d300ae52c'
sys.path.insert(0, str(PROD / 'runtime'))
import production_runner as base


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=base.sha256(path))


def imported(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def once(text, previous, actual):
    if text.count(previous) != 1:
        raise base.Refusal('nonunique frozen-source anchor: ' + previous)
    return text.replace(previous, actual)


def verify_files(files):
    for name, wanted in files.items():
        base.require_file(Path(name), wanted)


def load(declaration, expected):
    if declaration.resolve() != DECLARATION:
        raise base.Refusal('only the declared conditional ABA precision entry is accepted')
    data = json.loads(base.require_file(declaration, expected).read_text())
    if data.get('schema') != 'AXMAT_ABA_CONDITIONAL_CE_PRECISION_ENTRY_V1' or data.get('case') != 'ABA':
        raise base.Refusal('explicit conditional ABA precision declaration required')
    verify_files(data['files'])
    if data['files'].get(str(Path(__file__).resolve())) != base.sha256(Path(__file__).resolve()):
        raise base.Refusal('actual conditional preparation implementation must be frozen')
    base.require_file(EXPORT, EXPORT_SHA)
    export = imported(EXPORT, 'aba_ce_actual_saved_measurement_guard')
    _, storage, info, guard, snapshot = export.load(MEASUREMENT / 'declaration.json', EXPORT_DECL_SHA)
    staged = json.loads((STAGED / 'declaration.json').read_text())
    if (staged.get('schema') != 'AXMAT_ABA_INDEPENDENT_REFERENCE_INPUT_STAGING_V1'
            or staged.get('case') != 'ABA' or staged.get('native_transport_started') is not False):
        raise base.Refusal('unchanged staged independent ABA physical inputs required')
    verify_files(staged['files'])
    verify_files(staged['inherited_physical_source_pins'])
    if staged['sampling'] != dict(particles_per_generation=10000, generations_per_batch=10,
            inactive_batches=100, active_batches=2000, total_histories=210000000, seed=310033):
        raise base.Refusal('exact predeclared ABA sampling required')
    if data.get('sampling') != staged['sampling']:
        raise base.Refusal('conditional entry must retain the exact staged sampling')
    if str(OUT) not in storage['resource_roots']:
        raise base.Refusal('future reference output must be covered by the frozen ABA storage scope')
    return data, export, storage, info, guard, snapshot


def evidence_ready(export, storage, info, guard, qualification, expected):
    status_path, claim_path, stages_path, bootstrap, final = export.ready(
        storage, info, guard, qualification, expected)
    physical_path = MEASUREMENT / 'input_equivalence_ABA.json'
    physical = json.loads(base.require_file(physical_path).read_text())
    if (physical.get('status') != 'PASS' or physical.get('case') != 'ABA'
            or physical.get('experiment_id') != info['experiment_id']
            or physical.get('case_spec_sha256') != info['case_spec']['sha256']
            or physical.get('exact_initial_ABA_physical_records') != 48
            or len(physical.get('actual_track_record_identity', {})) != 14
            or physical.get('AAA_qualification') != pin(qualification)
            or physical.get('ABA_status') != pin(status_path)
            or physical.get('final_stage_seal') != pin(final / 'result.json')
            or physical.get('actual_axial_track') != pin(bootstrap / 'initial_axial_track.xsm')):
        raise base.Refusal('actual frozen same-study ABA physical review required')
    if (physical.get('implementation') != pin(ROOT / 'validation/axial_material/review_qualified_ABA_input_identity_white_trace.py')
            or physical.get('review_declaration') != pin(MEASUREMENT / 'input_review_declaration.json')
            or physical.get('production_prepared') != pin(PROD / 'prepared.json')):
        raise base.Refusal('actual input review must bind its frozen implementation and declaration')
    verify_files(physical['input_identities'])
    for name in ('materials.xml', 'geometry.xml', 'tallies.xml', 'settings.xml', 'reference_contract.json'):
        if physical['CE_inputs'][name] != pin(STAGED / name):
            raise base.Refusal('physical review does not bind the staged ABA reference: ' + name)
    observations = MEASUREMENT / 'observables'
    receipt_path = observations / 'export_receipt.json'
    receipt = json.loads(base.require_file(receipt_path).read_text())
    if (receipt.get('classification') != 'SAVED_ABA_MET_REAL64_OBSERVABLES_EXPORTED'
            or receipt.get('case') != 'ABA' or receipt.get('error') is not None
            or receipt.get('inputs_unchanged') is not True
            or receipt.get('new_transport_launched') is not False):
        raise base.Refusal('actual bounded saved REAL64 ABA export required')
    protocol_path = observations / 'protocol.json'
    if receipt['protocol'] != pin(protocol_path):
        raise base.Refusal('actual saved export protocol identity differs')
    protocol = json.loads(protocol_path.read_text())
    if (protocol.get('AAA_qualification') != pin(qualification)
            or protocol.get('prepared') != pin(PROD / 'prepared.json')
            or protocol.get('ABA_status') != pin(status_path)
            or protocol.get('final_stage_seal') != pin(final / 'result.json')
            or protocol.get('wall_seconds') != 60 or protocol.get('threads') != 1
            or protocol.get('retries') != 0):
        raise base.Refusal('export must bind the actual guarded ABA final state')
    verify_files(protocol['files'])
    required_outputs = {'observables.regions.csv', 'observables.faces.csv', 'observables.summary.txt'}
    if not required_outputs.issubset(receipt['outputs']):
        raise base.Refusal('complete saved ABA observable files required')
    for name, wanted in receipt['outputs'].items():
        if Path(name).name != name:
            raise base.Refusal('saved-export output must be a direct file')
        base.require_file(observations / name, wanted)
    return status_path, claim_path, stages_path, bootstrap, final, physical_path, receipt_path


def validate_native(manifest, expected):
    """Recheck actual eligibility immediately before a bounded native child."""
    if Path(manifest).resolve() != OUT / 'ABA/execution.json':
        raise base.Refusal('only the declared independent ABA native execution is accepted')
    execution = json.loads(base.require_file(Path(manifest), expected).read_text())
    entry = execution['conditional_entry']
    _, export, storage, info, guard, _ = load(Path(entry['path']), entry['sha256'])
    admission_path = Path(manifest).parent / 'measurement_admission.json'
    admission = json.loads(admission_path.read_text())
    qualification = admission['AAA_qualification']
    state = evidence_ready(export, storage, info, guard,
        Path(qualification['path']), qualification['sha256'])
    if (admission.get('case') != 'ABA'
            or admission.get('classification') != 'FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE'
            or admission.get('CE_manifest') != pin(manifest)
            or admission.get('ABA_status') != pin(state[0])):
        raise base.Refusal('actual ABA measurement admission must bind this execution')
    for key in ('prepared', 'ABA_status', 'final_seal', 'input_equivalence', 'production_checks',
            'CE_manifest', 'implementation', 'sampling_declaration', 'sampling_review', 'smoke_activation'):
        item = admission[key]
        base.require_file(Path(item['path']), item['sha256'])
    checks = json.loads(Path(admission['production_checks']['path']).read_text())
    if checks.get('status') != 'PASS' or not checks.get('checks') or any(v != 'PASS' for v in checks['checks'].values()):
        raise base.Refusal('unchanged original saved-state checks must pass before native ABA reference')
    return admission


def render_native():
    old = (AAA_CE / 'runtime/ce_execution.py').read_text()
    new = old.replace("admission.get('case') != 'AAA'", "admission.get('case') != 'ABA'")
    new = once(new, "status_pin = admission['AAA_status']", "status_pin = admission['ABA_status']")
    new = once(new, "saved['cases']['AAA']['classification']", "saved['cases']['ABA']['classification']")
    new = once(new, "production / 'AAA/bootstrap', Path(saved['cases']['AAA']['final_directory'])",
        "production / 'ABA/bootstrap', Path(saved['cases']['ABA']['final_directory'])")
    new = new.replace('AXMAT_WHITE_TRACE_PRECISION_ORIGINAL_THRESHOLD_ANALYSIS_V1', 'AXMAT_ABA_WHITE_TRACE_PRECISION_ORIGINAL_THRESHOLD_ANALYSIS_V1')
    new = new.replace('AXMAT_CE_WHITE_TRACE_PRECISION_RESOURCE_ADDENDUM_V1', 'AXMAT_ABA_CE_WHITE_TRACE_PRECISION_RESOURCE_ADDENDUM_V1')
    new = once(new, "    case_spec = json.loads(case_path.read_text())", '''    entry_pin = contract['conditional_entry']
    if entry_pin['path'] not in files or files[entry_pin['path']] != entry_pin['sha256']:
        raise RuntimeError('conditional ABA entry must be frozen')
    entry = importlib.util.spec_from_file_location('aba_precision_actual_native_guard', contract['conditional_implementation'])
    actual = importlib.util.module_from_spec(entry)
    entry.loader.exec_module(actual)
    actual.validate_native(manifest, expected_sha256)
    case_spec = json.loads(case_path.read_text())''')
    new = once(new, "or supplement.get('formal_active_batches') != 2000):",
        "or supplement.get('formal_active_batches') != 2000\n                or supplement.get('artifact_budget_bytes') != 64*2**30\n                or supplement.get('min_free_bytes') != 8*2**30):")
    new = once(new, "int(caps['new_case_artifact_budget_GiB']*2**30))", "supplement['artifact_budget_bytes'])")
    before = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(old).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    after = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(new).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    if set(before) != set(after) or any(before[n] != after[n] for n in before if n != 'load_contract'):
        raise base.Refusal('native lifecycle changed beyond actual admission/resource loader')
    return old, new


def render_collector(execution_sha):
    old = (AAA_CE / 'runtime/assess_qualified_AAA_white_trace_precision.py').read_text()
    new = old.replace('AAA', 'ABA').replace('aaa_run_status_sha256', 'aba_run_status_sha256')
    new = once(new, AAA_CE.name.replace('AAA', 'ABA'), OUT.name)
    new = once(new, AAA_EXEC_SHA, execution_sha)
    new = once(new, '    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)', '''    import importlib.util
    execution_path = case_dir / 'execution.json'
    native_contract = json.loads(require_file(execution_path, CE_SHA).read_text())
    implementation = Path(native_contract['conditional_implementation'])
    require_file(implementation, native_contract['files'][str(implementation)])
    entry_spec = importlib.util.spec_from_file_location('aba_precision_completed_measurement_guard', implementation)
    entry = importlib.util.module_from_spec(entry_spec)
    entry_spec.loader.exec_module(entry)
    admission = entry.validate_native(execution_path, CE_SHA)
    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)''')
    new = once(new, 'for key in ("sampling_declaration", "sampling_review", "smoke_activation", "parent_measurement_admission"):',
        'for key in ("sampling_declaration", "sampling_review", "smoke_activation", "AAA_qualification", "saved_export"):')
    new = once(new, 'implementation=descriptor(Path(__file__).resolve()), ABA_admitted=qualified,',
        'implementation=descriptor(Path(__file__).resolve()), ABA_independent_accuracy_qualified=qualified, AAA_qualification=admission["AAA_qualification"],')
    new = once(new, '        qualify_aba(prepared, PRODUCTION, PREPARED_SHA, target, sha256(target))',
        '        # ABA accuracy is collected here; the unchanged AAA admission guard was already applied above.')
    new = once(new, 'checks=checks, ABA_admitted=qualified,', 'checks=checks, ABA_independent_accuracy_qualified=qualified,')
    new = once(new, 'Only unanimous original checks produce an ABA admission receipt.',
        'Only unanimous original checks produce an independent ABA accuracy receipt.')
    # The entire eight-check numerical decision, including complete statepoint
    # identities and raw-history aggregation, must be exactly the AAA code.
    def decision(source):
        main = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        names = [n.targets[0].id if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) else None for n in main.body]
        begin, end = names.index('expected_statepoints'), names.index('qualified')
        return ast.dump(ast.Module(body=main.body[begin:end+1], type_ignores=[]), include_attributes=False)
    if decision(old) != decision(new):
        raise base.Refusal('original complete-history and eight-gate qualification decision changed')
    compile(new, 'conditional_ABA_collector', 'exec')
    return old, new


def render_driver():
    old = (AAA_CE / 'runtime/run_qualified_AAA_white_trace_precision_analysis.py').read_text()
    new = old.replace('AAA', 'ABA')
    new = once(new, AAA_CE.name.replace('AAA', 'ABA'), OUT.name)
    new = once(new, 'OBS = ART / "axial-material-qualified-ABA-white-trace-observables-20261004"',
        'OBS = ART / "axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004/aba_measurement/observables"')
    new = new.replace('ABA_admitted', 'ABA_independent_accuracy_qualified')
    compile(new, 'conditional_ABA_driver', 'exec')
    return old, new


def source_copy(path, pair):
    old, new = pair
    with path.open('x') as stream:
        stream.write(new)
    with path.with_suffix(path.suffix + '.patch').open('x') as stream:
        stream.write(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='frozen_AAA', tofile=str(path))))


def prepare(declaration, expected, qualification, qualification_sha):
    data, export, storage, info, guard, _ = load(declaration, expected)
    state = evidence_ready(export, storage, info, guard, qualification, qualification_sha)
    status_path, claim_path, stages_path, bootstrap, final, physical_path, receipt_path = state
    status = json.loads(status_path.read_text())
    previous = json.loads(base.require_file(AAA_CE / 'AAA/execution.json', AAA_EXEC_SHA).read_text())
    verify_files(previous['files'])
    # Original read-only producer checks are evaluated before creating a CE root.
    rs = imported(AAA_CE / 'runtime/reference_statistics.py', 'reference_statistics')
    sys.modules['reference_statistics'] = rs
    cb = imported(AAA_CE / 'runtime/compare_balance_symmetry.py', 'aba_precision_original_producer_checks')
    spec = Path(info['case_spec']['path'])
    rules = cb.predeclared_rules(spec)
    obs = MEASUREMENT / 'observables'
    production = cb.read_production(obs / 'observables.regions.csv', obs / 'observables.faces.csv', obs / 'observables.summary.txt', rules)
    checks = cb.evaluate_production(production, rules)
    if not checks['checks'] or any(v != 'PASS' for v in checks['checks'].values()):
        raise base.Refusal('original actual ABA producer checks did not pass')
    resources = base.DiskResources(ART, storage['resource_roots'], 8*2**30, 64*2**30)
    resources.check()
    OUT.mkdir(exist_ok=False)
    case = OUT / 'ABA'
    case.mkdir()
    (OUT / 'runtime').mkdir()
    write_new(OUT / 'prepare_claim.json', dict(entry=pin(declaration), implementation=pin(Path(__file__).resolve()),
        AAA_qualification=pin(qualification), actual_ABA_status=pin(status_path), started_unix=time.time(), retries=0, transport_started=False))
    result = dict(status='PREPARATION_FAILED_NO_RETRY', case='ABA', error=None, native_transport_started=False)
    try:
        for path in (PROD / 'runtime').iterdir():
            if path.is_file():
                shutil.copy2(path, OUT / 'runtime' / path.name)
        for name in ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json'):
            shutil.copy2(STAGED / name, case / name)
        for name in ('reference_statistics.py', 'compare_balance_symmetry.py'):
            shutil.copy2(AAA_CE / 'runtime' / name, OUT / 'runtime' / name)
        for name in ('statistical_rules.json', 'balance_symmetry_rules.json'):
            shutil.copy2(AAA_CE / name, OUT / name)
        source_copy(OUT / 'runtime/ce_execution.py', render_native())
        new_rs = imported(OUT / 'runtime/reference_statistics.py', 'reference_statistics')
        sys.modules['reference_statistics'] = new_rs
        new_cb = imported(OUT / 'runtime/compare_balance_symmetry.py', 'aba_precision_copied_current_rules')
        if (new_rs.predeclared_rules(spec) != json.loads((OUT / 'statistical_rules.json').read_text())
                or new_cb.predeclared_rules(spec) != json.loads((OUT / 'balance_symmetry_rules.json').read_text())):
            raise base.Refusal('original statistical/current rules must remain exact')
        write_new(OUT / 'declaration.json', dict(schema='AXMAT_ABA_CE_WHITE_TRACE_PRECISION_SAMPLING_V1', case='ABA',
            status='PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT', conditional_entry=pin(declaration),
            actual_AAA_qualification=pin(qualification), actual_ABA_status=pin(status_path),
            physical_source_staging=pin(STAGED / 'declaration.json'), formal=data['sampling'],
            source_policy='Original ordinary sampler, independently declared ABA seed 310033 and fresh initial source; no imported bank, UFS, feedback, combined old samples or discarded active batch.',
            physical_inputs_changed=False, original_numerical_acceptance_thresholds_changed=False))
        write_new(OUT / 'resource_addendum.json', dict(schema='AXMAT_ABA_CE_WHITE_TRACE_PRECISION_RESOURCE_ADDENDUM_V1',
            status='PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT', case_spec_sha256=info['case_spec']['sha256'],
            formal_ce_wall_seconds_per_case=64800, formal_particles_per_generation=10000, formal_generations_per_batch=10,
            formal_particles_per_batch=100000, formal_inactive_batches=100, formal_active_batches=2000,
            formal_total_histories=210000000, automatic_retries=0, threads=1, new_numeric_children_at_once=1,
            artifact_budget_bytes=64*2**30, min_free_bytes=8*2**30, storage_scope=pin(MEASUREMENT.parent / 'aba_budget/declaration.json')))
        checks.update(status='PASS', case='ABA', implementation=pin(AAA_CE / 'runtime/compare_balance_symmetry.py'),
            input_identities={str(p):base.sha256(p) for p in [AAA_CE / 'runtime/compare_balance_symmetry.py', AAA_CE / 'balance_symmetry_rules.json',
                *[obs / ('observables.' + n) for n in ('regions.csv', 'faces.csv', 'summary.txt')]]})
        write_new(OUT / 'production_checks.json', checks)
        original_inputs = json.loads(physical_path.read_text())
        inputs = copy.deepcopy(original_inputs)
        inputs.update(parent_actual_input_equivalence=pin(physical_path), CE_inputs={name:pin(case / name) for name in
            ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json')})
        inputs['input_identities'].update({str(p):base.sha256(p) for p in [physical_path, OUT / 'declaration.json',
            *[case / n for n in ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json')]]})
        write_new(OUT / 'input_equivalence_ABA.json', inputs)
        reviewed = [Path(__file__).resolve(), declaration, qualification, status_path, claim_path, stages_path,
            bootstrap / 'result.json', final / 'result.json', receipt_path, obs / 'protocol.json', physical_path,
            PROD / 'prepared.json', spec, *[obs / ('observables.' + n) for n in ('regions.csv', 'faces.csv', 'summary.txt')]]
        review_files = {**data['files'], **{str(p.resolve()):base.sha256(p) for p in reviewed},
            **{str(p.resolve()):base.sha256(p) for p in OUT.rglob('*') if p.is_file()}}
        write_new(OUT / 'input_sampling_review.json', dict(status='PASS', case='ABA', all_numerical_acceptance_thresholds_unchanged=True,
            physical_and_tally_XML_identical=True, original_ABA_seed_source_and_temperature_unchanged=True,
            statistical_and_current_implementations_byte_identical_to_AAA=True, files=review_files))
        execution = copy.deepcopy(previous)
        execution.update(case_spec=info['case_spec'], wall_seconds=64800, resource_roots=storage['resource_roots'],
            resource_addendum=str(OUT / 'resource_addendum.json'), sampling_addendum=str(OUT / 'declaration.json'),
            conditional_entry=pin(declaration), conditional_implementation=str(Path(__file__).resolve()),
            scope='Actual qualified AAA followed by actual sealed ABA fixed point and unchanged saved-state checks; independent ABA reference, no accuracy claim before complete analysis.')
        execution['files'].update(review_files)
        execution['files'].update({str(p.resolve()):base.sha256(p) for p in OUT.rglob('*') if p.is_file()})
        write_new(case / 'execution.json', execution)
        write_new(case / 'measurement_admission.json', dict(schema='AXMAT_ABA_CE_MEASUREMENT_ADMISSION_V1', case='ABA',
            classification='FIXED_POINT_AND_INPUTS_ADMITTED_TO_REFERENCE', independent_accuracy_qualified=False,
            prepared=pin(PROD / 'prepared.json'), AAA_qualification=pin(qualification), ABA_status=pin(status_path),
            final_seal=pin(final / 'result.json'), common_basis_sha256=status['common_basis_sha256'],
            input_equivalence=pin(OUT / 'input_equivalence_ABA.json'), production_checks=pin(OUT / 'production_checks.json'),
            CE_manifest=pin(case / 'execution.json'), implementation=pin(Path(__file__).resolve()),
            sampling_declaration=pin(OUT / 'declaration.json'), sampling_review=pin(OUT / 'input_sampling_review.json'),
            smoke_activation=pin(ART / 'axial-material-ce-qualified-AAA-long-generations-20261004/smoke_activation_receipt.json'),
            saved_export=pin(receipt_path), completed_maps=status['cases']['ABA']['completed_maps'],
            defects=status['cases']['ABA']['maps'][-1]['defects']))
        source_copy(OUT / 'runtime/assess_qualified_ABA_white_trace_precision.py', render_collector(base.sha256(case / 'execution.json')))
        source_copy(OUT / 'runtime/run_qualified_ABA_white_trace_precision_analysis.py', render_driver())
        analysis_files = {**review_files, **{str(p.resolve()):base.sha256(p) for p in OUT.rglob('*') if p.is_file()}}
        write_new(OUT / 'analysis_collection_declaration.json', dict(schema='AXMAT_ABA_WHITE_TRACE_PRECISION_ORIGINAL_THRESHOLD_ANALYSIS_V1',
            status='FROZEN_BEFORE_FORMAL_TRANSPORT', declared_unix=time.time(), files=analysis_files,
            analysis_wall_seconds=120, threads=1, retries=0, transport_launched=False,
            engineering_or_statistical_numerical_thresholds_changed=False,
            qualification='All original eight same-case scientific requirements must pass. No qualification from sampling size or numerical convergence alone.'))
        validate_native(case / 'execution.json', base.sha256(case / 'execution.json'))
        executor = imported(OUT / 'runtime/ce_execution.py', 'aba_precision_preflight_only')
        executor.load_contract(case / 'execution.json', base.sha256(case / 'execution.json'))
        result.update(status='ABA_INDEPENDENT_REFERENCE_PREPARED_NO_TRANSPORT', execution=pin(case / 'execution.json'),
            collector=pin(OUT / 'runtime/assess_qualified_ABA_white_trace_precision.py'),
            driver=pin(OUT / 'runtime/run_qualified_ABA_white_trace_precision_analysis.py'), resources=resources.check())
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        write_new(OUT / 'prepare_result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'prepare'])
    parser.add_argument('declaration', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--reference-qualification', type=Path)
    parser.add_argument('--reference-sha256')
    args = parser.parse_args()
    if args.action == 'preflight':
        _, _, _, _, _, snapshot = load(args.declaration, args.sha256)
        render_native()
        render_collector('0'*64)
        render_driver()
        print(json.dumps(dict(status='STATIC_ABA_REFERENCE_ENTRY_READY_ACTUAL_AAA_AND_ABA_EVIDENCE_PENDING',
            future_reference_root_created=False, native_transport_launched=False,
            actual_ABA_measurement_admitted=False, independent_ABA_accuracy_qualified=False, resources=snapshot)))
        return
    print(json.dumps(prepare(args.declaration, args.sha256, args.reference_qualification, args.reference_sha256), indent=2))


if __name__ == '__main__':
    main()

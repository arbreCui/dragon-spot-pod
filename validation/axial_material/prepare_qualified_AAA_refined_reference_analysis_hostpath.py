"""Prepare and run the complete original-gate saved-reference analysis once.

Actual fresh coupled MET, sealed data and physical equivalence are mandatory
before any output. Complete fine checks precede the fixed observation view.
The original CE statistics/current code and qualification conditions remain.
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
PROD = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OBS = ART / 'axial-material-qualified-AAA-white-trace-refined-observables-20261005'
SOURCE = ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005'
OUT = ART / 'axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python')
PREPARED_SHA = '024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'
RECIPE_SHA = '56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import (verify_prepared, verify_sealed_directory, require_file,
    sha256, SerialExecutor, DiskResources)


def read(path):
    return json.loads(Path(path).read_text())


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=sha256(path))


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def verify(files):
    for name, wanted in files.items():
        require_file(Path(name), wanted)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def ready():
    require_file(ROOT / 'validation/axial_material/prepare_qualified_AAA_refined_reference_analysis.py',
        '12261e2812b695c839fcde0dd837f2b4c7d0f46a20b999b4da60cdfd015be302')
    require_file(ART / 'axial-material-qualified-AAA-white-trace-refined-reference-20261005/declaration.json',
        '484817c8ba0c8dab1d16610a6b9c3cc4d6c6b8c6c8691a5a2f555b8c8b2c4f28')
    require_file(ART / 'axial-material-qualified-AAA-white-trace-refined-reference-20261005/AAA/analysis_construction_failure.json',
        'fa42f8d67753b4dcb9f14a3dbbfb1dfe13a9c49f35f3cfeae4892f00a5f4f48b')
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    status = read(PROD / 'AAA/run_status.json')
    if (status['classification'] != 'WAITING_REFERENCE'
            or status['cases'].get('AAA', {}).get('classification') != 'VALID_MET'):
        raise ValueError('actual complete fresh coupled AAA required before saved-reference analysis')
    final = Path(status['cases']['AAA']['final_directory'])
    for folder in (PROD / 'archives', PROD / 'training', PROD / 'AAA/bootstrap', final):
        verify_sealed_directory(folder)
    recipe = read(require_file(SOURCE / 'refined_reference_analysis_recipe.json', RECIPE_SHA))
    pins = [recipe[k] for k in ('refined_prepared', 'reference_execution',
        'complete_independent_native_sample', 'original_candidate_assessment',
        'observation_projection_recipe', 'projection_precheck',
        'native_export_source_proof', 'physical_input_precheck')]
    pins += list(recipe['unchanged_reference_implementations'].values())
    for item in pins:
        require_file(Path(item['path']), item['sha256'])
    native = read(recipe['complete_independent_native_sample']['path'])
    if (native['status'] != 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
            or native['returncode'] != 0 or native['error'] is not None):
        raise ValueError('complete unchanged independent CE sample required')
    require_file(CE / 'AAA/openmc.log', native['log_sha256'])
    for name, wanted in native['outputs'].items():
        require_file(CE / 'AAA' / name, wanted)
    execution = read(recipe['reference_execution']['path'])
    verify(execution['files'])
    physical = read(OBS / 'input_equivalence_AAA.json')
    if (physical['status'] != 'PASS' or physical['case'] != 'AAA'
            or physical['production_prepared'] != pin(PROD / 'prepared.json')
            or physical['AAA_status'] != pin(PROD / 'AAA/run_status.json')
            or physical['case_spec_sha256'] != info['case_spec']['sha256']
            or not physical['original_physical_and_independent_scientific_definitions_unchanged']):
        raise ValueError('actual refined physical/original-bin identity report required')
    verify(physical['input_identities'])
    review_source = read(recipe['physical_input_precheck']['path'])['implementation']
    require_file(Path(review_source['path']), review_source['sha256'])
    if physical['input_identities'].get(review_source['path']) != review_source['sha256']:
        raise ValueError('physical identity implementation differs from its precheck')
    return info, status, final, recipe, native, execution


ADMISSION_HOST = '''"""Require actual fixed-point, full fine admission and frozen sample reuse."""
import json
from pathlib import Path
import sys
ROOT=Path("/Users/wen/spot")
ART=ROOT/"validation/artifacts"
OUT=ART/"axial-material-qualified-AAA-white-trace-refined-reference-hostpath-20261005"
PROD=ART/"axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
sys.path.insert(0,str(PROD/"runtime"))
from production_runner import require_file,sha256,verify_sealed_directory


def verify_measurement_admission(prepared, expected):
    status=json.loads((PROD/"AAA/run_status.json").read_text())
    if (status["classification"]!="WAITING_REFERENCE"
            or status["cases"].get("AAA",{}).get("classification")!="VALID_MET"):
        raise ValueError("actual complete fresh coupled AAA required before reference collection")
    decl=require_file(OUT/"declaration.json",expected)
    d=json.loads(decl.read_text())
    if d["schema"]!="AXMAT_REFINED_FULL_ORIGINAL_GATE_REFERENCE_ANALYSIS_V1":
        raise ValueError("complete frozen reference collection declaration required")
    for name,wanted in d["files"].items():
        require_file(Path(name),wanted)
    claim=json.loads((OUT/"AAA/analysis_claim.json").read_text())
    if claim["declaration_sha256"]!=expected:
        raise ValueError("reference collection does not bind the actual bounded analysis")
    m=json.loads((OUT/"measurement_admission.json").read_text())
    if (m["classification"]!="FIXED_POINT_INPUTS_AND_COMPLETE_FINE_OBSERVATIONS_ADMITTED_TO_SAVED_REFERENCE"
            or m["case"]!="AAA" or m["production_prepared"]!=d["production_prepared"]
            or m["production_prepared"]["sha256"]!="024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53"
            or m["AAA_status"]["sha256"]!=sha256(PROD/"AAA/run_status.json")
            or m["case_spec"]!=prepared["case_spec"]):
        raise ValueError("fresh refined measurement binding differs")
    for name,wanted in m["files"].items():
        require_file(Path(name),wanted)
    for folder in (PROD/"archives",PROD/"training",PROD/"AAA/bootstrap",Path(status["cases"]["AAA"]["final_directory"])):
        verify_sealed_directory(folder)
    projection=json.loads((OUT/"observation/projection_receipt.json").read_text())
    if (projection["classification"]!="PASS_COMPLETE_FINE_AND_CONSERVATIVE_ORIGINAL_OBSERVATION_VIEW"
            or projection["native_axial_cells"]!=48 or projection["observation_cells"]!=12
            or len(projection["mapping"])!=96 or len(projection["face_map"])!=13
            or projection["local_or_binwise_normalization"] or projection["bins_removed"]):
        raise ValueError("complete fixed original observation projection required")
    for key in ("original_checks_on_all_fine_entries","original_checks_on_observation_view"):
        if any(value!="PASS" for value in projection[key]["checks"].values()):
            raise ValueError("original complete fine/view numerical checks failed")
    physical=json.loads((OUT/"input_equivalence_AAA.json").read_text())
    if (physical["status"]!="PASS" or physical["production_prepared"]!=m["production_prepared"]
            or physical["AAA_status"]!=m["AAA_status"]
            or physical["case_spec_sha256"]!=prepared["case_spec"]["sha256"]):
        raise ValueError("fresh physical identity report differs")
    return m
'''


def collector_source(original):
    changes = [
        ('axial-material-production-qualified-AB-white-trace-20261004', PROD.name),
        ('88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf', PREPARED_SHA),
        ('    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)',
         '    prepared = verify_prepared(PRODUCTION / "prepared.json", PREPARED_SHA)\n'
         '    from refined_reference_admission import verify_measurement_admission\n'
         '    if len(sys.argv) != 2:\n        raise ValueError("explicit analysis declaration SHA256 required")\n'
         '    refined_measurement = verify_measurement_admission(prepared, sys.argv[1])\n'
         '    analysis = art / "'+OUT.name+'"'),
        ('    stats_path = case_dir / "statistics.json"', '    stats_path = analysis / "AAA/statistics.json"'),
        ('    currents_path = case_dir / "currents_balance_symmetry.json"',
         '    currents_path = analysis / "AAA/currents_balance_symmetry.json"'),
        ('    inputs_path = ce / "input_equivalence_AAA.json"', '    inputs_path = analysis / "input_equivalence_AAA.json"'),
        ('        measurement_admission=descriptor(case_dir / "measurement_admission.json"),',
         '        measurement_admission=descriptor(case_dir / "measurement_admission.json"),\n'
         '        refined_measurement_admission=descriptor(analysis / "measurement_admission.json"),\n'
         '        complete_fine_observation_projection=descriptor(analysis / "observation/projection_receipt.json"),'),
        ('    write_new(case_dir / "reference_assessment.json", receipt)',
         '    write_new(analysis / "AAA/reference_assessment.json", receipt)'),
        ('        target = case_dir / "reference_qualification.json"',
         '        target = analysis / "AAA/reference_qualification.json"'),
        ('        assessment=descriptor(case_dir / "reference_assessment.json")), indent=2))',
         '        assessment=descriptor(analysis / "AAA/reference_assessment.json")), indent=2))')]
    text = original
    for old, new in changes:
        if text.count(old) != 1:
            raise ValueError('nonunique original collector anchor: ' + old)
        text = text.replace(old, new, 1)
    restored = text
    for old, new in reversed(changes):
        if restored.count(new) != 1:
            raise ValueError('nonunique restored collector anchor')
        restored = restored.replace(new, old, 1)
    if restored != original:
        raise ValueError('original scientific qualification conditions changed')
    before = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(original).body if isinstance(n, ast.FunctionDef)}
    after = {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}
    if before.keys() != after.keys() or any(before[k] != after[k] for k in before if k != 'main'):
        raise ValueError('original report verification changed')
    return text, dict(original_collector_restored_byte_exact=True,
        original_functions_other_than_main_AST_exact=True,
        original_scientific_conditions_and_complete_statepoint_history_checks_retained=True)


def prepare():
    info, status, final, recipe, native, execution = ready()
    OUT.mkdir(exist_ok=False)
    runtime = OUT / 'runtime'
    runtime.mkdir()
    (OUT / 'AAA').mkdir()
    for name in ('reference_statistics.py', 'compare_balance_symmetry.py'):
        item = recipe['unchanged_reference_implementations'][name]
        shutil.copy2(item['path'], runtime / name)
        require_file(runtime / name, item['sha256'])
    projection_recipe = read(recipe['observation_projection_recipe']['path'])
    helper = projection_recipe['helper']
    require_file(Path(helper['path']), helper['sha256'])
    shutil.copy2(helper['path'], runtime / 'project_refined_observables.py')
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', runtime / 'run_bounded_dragon.py')
    collector_item = recipe['unchanged_reference_implementations']['assess_qualified_AAA_white_trace_precision.py']
    original = Path(collector_item['path']).read_text()
    text, equivalence = collector_source(original)
    (runtime / 'refined_reference_collector.py').write_text(text)
    (runtime / 'refined_reference_collector.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), text.splitlines(True), fromfile='original-collector', tofile='same-gates-refined-binding')))
    (runtime / 'refined_reference_admission.py').write_text(ADMISSION_HOST)
    write_new(OUT / 'collector_source_equivalence.json', equivalence)
    rs = module(runtime / 'reference_statistics.py', 'reference_statistics')
    sys.modules['reference_statistics'] = rs
    cb = module(runtime / 'compare_balance_symmetry.py', 'refined_current_checker')
    native_spec_path = Path(info['case_spec']['path'])
    native_spec = read(native_spec_path)
    view_spec = copy.deepcopy(native_spec)
    view_spec['geometry']['cells_per_zone'] = 4
    view_spec['observation_projection_view'] = dict(native_case_spec=pin(native_spec_path),
        native_cells=48, original_observation_cells=12, solver_not_changed_by_this_view=True,
        fixed_projection_recipe=recipe['observation_projection_recipe'])
    view_spec_path = OUT / 'observation_case_spec.json'
    write_new(view_spec_path, view_spec)
    stat_rules = rs.predeclared_rules(view_spec_path)
    view_rules = cb.predeclared_rules(view_spec_path)
    fine_rules = cb.predeclared_rules(native_spec_path)
    for actual, prior_path in ((stat_rules, CE / 'statistical_rules.json'), (view_rules, CE / 'balance_symmetry_rules.json')):
        prior = read(prior_path)
        if {k:v for k,v in actual.items() if k != 'case_spec_sha256'} != {k:v for k,v in prior.items() if k != 'case_spec_sha256'}:
            raise ValueError('original independent scientific rules changed')
    if (fine_rules['axial_cells'] != 48 or view_rules['axial_cells'] != 12
            or {k:v for k,v in fine_rules.items() if k not in ('axial_cells','case_spec_sha256')}
               != {k:v for k,v in view_rules.items() if k not in ('axial_cells','case_spec_sha256')}):
        raise ValueError('fine numerical admission rules changed beyond exact cell count')
    write_new(OUT / 'statistical_rules.json', stat_rules)
    write_new(OUT / 'balance_symmetry_rules.json', view_rules)
    write_new(OUT / 'fine_balance_symmetry_rules.json', fine_rules)
    project = module(runtime / 'project_refined_observables.py', 'refined_projection')
    projection = project.project(OBS, OUT / 'observation', cb, fine_rules)
    checks = projection['original_checks_on_all_fine_entries']
    checks['input_identities'] = {str(p):sha256(p) for p in [native_spec_path, *[OBS / ('observables.'+s) for s in ('regions.csv','faces.csv','summary.txt')]]}
    write_new(OUT / 'complete_fine_production_checks.json', checks)
    physical = read(OBS / 'input_equivalence_AAA.json')
    physical['refined_observation_projection'] = pin(OUT / 'observation/projection_receipt.json')
    physical['input_identities'].update({str(p):sha256(p) for p in [OUT / 'observation/projection_receipt.json', OUT / 'complete_fine_production_checks.json', view_spec_path]})
    write_new(OUT / 'input_equivalence_AAA.json', physical)
    sources = [ROOT / 'validation/axial_material/prepare_qualified_AAA_refined_reference_analysis.py',
        ART / 'axial-material-qualified-AAA-white-trace-refined-reference-20261005/declaration.json',
        ART / 'axial-material-qualified-AAA-white-trace-refined-reference-20261005/AAA/analysis_construction_failure.json',
        Path(__file__).resolve(), SOURCE / 'refined_reference_analysis_recipe.json',
        OBS / 'input_equivalence_AAA.json', OBS / 'export_receipt.json', PROD / 'prepared.json',
        PROD / 'AAA/run_status.json', final / 'result.json', native_spec_path,
        CE / 'AAA/native_result.json', CE / 'AAA/execution.json', CE / 'AAA/measurement_admission.json',
        CE / 'AAA/reference_contract.json', PYTHON.resolve(),
        *[p for p in OUT.rglob('*') if p.is_file()],
        *[OBS / ('observables.'+s) for s in ('regions.csv','faces.csv','summary.txt')]]
    files = {str(p.resolve()):sha256(p) for p in sources}
    files.update(execution['files'])
    files.update({str(CE / 'AAA' / name):h for name,h in native['outputs'].items()})
    files.update(physical['input_identities'])
    measurement = dict(classification='FIXED_POINT_INPUTS_AND_COMPLETE_FINE_OBSERVATIONS_ADMITTED_TO_SAVED_REFERENCE',
        case='AAA', production_prepared=pin(PROD / 'prepared.json'), AAA_status=pin(PROD / 'AAA/run_status.json'),
        final_stage_seal=pin(final / 'result.json'), case_spec=info['case_spec'],
        common_basis_sha256=status['common_basis_sha256'], original_reference_execution=recipe['reference_execution'],
        original_reference_native=recipe['complete_independent_native_sample'],
        complete_fine_checks=pin(OUT / 'complete_fine_production_checks.json'),
        observation_projection=pin(OUT / 'observation/projection_receipt.json'),
        physical_input_equivalence=pin(OUT / 'input_equivalence_AAA.json'), files=files,
        AAA_accuracy_qualified=False, ABA_admitted=False, transport_launched=False)
    write_new(OUT / 'measurement_admission.json', measurement)
    files[str(OUT / 'measurement_admission.json')] = sha256(OUT / 'measurement_admission.json')
    regions = OUT / 'observation/observables.regions.csv'
    summary = OUT / 'observation/observables.summary.txt'
    common = ['--case-spec', str(view_spec_path), '--contract', str(CE / 'AAA/reference_contract.json'),
        '--statepoints', str(CE / 'AAA'), '--production-regions', str(regions), '--production-summary', str(summary)]
    commands = [
        [str(PYTHON), str(runtime / 'reference_statistics.py'), 'analyze', '--rules', str(OUT / 'statistical_rules.json'),
         *common, '--output', str(OUT / 'AAA/statistics.json')],
        [str(PYTHON), str(runtime / 'compare_balance_symmetry.py'), 'compare', '--rules', str(OUT / 'balance_symmetry_rules.json'),
         '--statistics-rules', str(OUT / 'statistical_rules.json'), *common,
         '--production-faces', str(OUT / 'observation/observables.faces.csv'), '--output', str(OUT / 'AAA/currents_balance_symmetry.json')],
        [str(PYTHON), str(runtime / 'refined_reference_collector.py'), '__DECLARATION_SHA256__']]
    roots = sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    resources = DiskResources(ART, roots, 8*2**30, 96*2**30)
    before = resources.check()
    declaration = dict(schema='AXMAT_REFINED_FULL_ORIGINAL_GATE_REFERENCE_ANALYSIS_V1',
        declared_unix=time.time(), recipe=pin(SOURCE / 'refined_reference_analysis_recipe.json'),
        files=files, commands=commands, production_prepared=pin(PROD / 'prepared.json'),
        total_wall_seconds=120, threads=1, retries=0, resource_roots=roots,
        min_free_bytes=8*2**30, artifact_budget_bytes=96*2**30, resources_before=before,
        transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        command_binding='Replace only __DECLARATION_SHA256__ with the verified CLI declaration digest when invoking the original-gate collector.',
        scope='Complete retained independent sample reanalysis at original scientific rules. All fine observations remain admitted and saved; compare conservative original-bin integrals with one global normalization. All original gates are mandatory for qualification.')
    write_new(OUT / 'declaration.json', declaration)
    verify(files)
    print(json.dumps(dict(classification='PREPARED_COMPLETE_ORIGINAL_GATE_ANALYSIS_NOT_RUN', declaration=pin(OUT / 'declaration.json')), indent=2))


def run(expected):
    declaration = require_file(OUT / 'declaration.json', expected)
    d = read(declaration)
    if d['schema'] != 'AXMAT_REFINED_FULL_ORIGINAL_GATE_REFERENCE_ANALYSIS_V1' or d['total_wall_seconds'] != 120 or d['threads'] != 1 or d['retries'] != 0:
        raise ValueError('original bounded analysis protocol differs')
    verify(d['files'])
    ready()
    write_new(OUT / 'AAA/analysis_claim.json', dict(declaration_sha256=expected, started_unix=time.time()))
    resources = DiskResources(ART, d['resource_roots'], d['min_free_bytes'], d['artifact_budget_bytes'])
    executor = SerialExecutor(OUT, 120, 'AAA', resources)
    result = dict(classification='ANALYSIS_FAILED_NO_RETRY', completed_commands=0, error=None,
                  transport_launched=False, ABA_admitted=False)
    started = time.monotonic()
    try:
        for index, cmd in enumerate(d['commands'], 1):
            command = [expected if arg == '__DECLARATION_SHA256__' else arg for arg in cmd]
            executor.execute(OUT / 'AAA', 'analysis_'+str(index), command, 120)
            result['completed_commands'] = index
        assessment = read(OUT / 'AAA/reference_assessment.json')
        result.update(classification='COMPLETE_REFINED_ORIGINAL_GATE_REFERENCE_ANALYSIS',
            AAA_classification=assessment['classification'], ABA_admitted=assessment['ABA_admitted'],
            reference_assessment=pin(OUT / 'AAA/reference_assessment.json'))
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        try:
            verify(d['files'])
            verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
        except BaseException as error:
            result.update(classification='ANALYSIS_INPUT_CHANGED', error=repr(error), ABA_admitted=False)
        result['elapsed_seconds'] = time.monotonic()-started
        result['outputs'] = {str(p.relative_to(OUT)):sha256(p) for p in (OUT / 'AAA').iterdir() if p.is_file() and p.name != 'analysis_result.json'}
        write_new(OUT / 'AAA/analysis_result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--sha256')
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    elif args.sha256:
        run(args.sha256)
    else:
        parser.error('--sha256 required for run')

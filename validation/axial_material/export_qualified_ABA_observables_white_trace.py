"""Export a real sealed ABA fixed point after the actual full AAA qualification.

Reuse the frozen REAL64 exporter and bounded process helper. This produces
saved-state observations only, never independent ABA accuracy qualification.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
PARENT = ART / 'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
STORAGE = PARENT / 'aba_budget/declaration.json'
STORAGE_SHA = '7b7f40f9d568a84f746a6821022c6cf9819e68bf0c125c41ff59115623923498'
DECLARATION = PARENT / 'aba_measurement/declaration.json'
GUARD = ROOT / 'validation/axial_material/run_qualified_ABA_white_trace_budget.py'
GUARD_SHA = '614c50a65c1f837e7f9b5718f1b094609debf25eb1c35b85fafa87d9d9e35062'
sys.path.insert(0, str(PROD / 'runtime'))
import production_runner as base


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=base.sha256(path))


def load(declaration, expected):
    if declaration.resolve() != DECLARATION:
        raise base.Refusal('only the declared ABA saved-measurement entry is accepted')
    data = json.loads(base.require_file(declaration, expected).read_text())
    if data.get('schema') != 'AXMAT_ABA_SAVED_MEASUREMENT_ENTRY_V1' or data.get('case') != 'ABA':
        raise base.Refusal('explicit ABA saved-measurement declaration required')
    for name, wanted in data['files'].items():
        base.require_file(Path(name), wanted)
    if data['files'].get(str(Path(__file__).resolve())) != base.sha256(Path(__file__).resolve()):
        raise base.Refusal('actual saved-measurement entry is not frozen')
    base.require_file(GUARD, GUARD_SHA)
    module_spec = importlib.util.spec_from_file_location('aba_measurement_qualification_guard', GUARD)
    guard = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(guard)
    storage, info, _, snapshot = guard.load(STORAGE, STORAGE_SHA)
    return data, storage, info, guard, snapshot


def ready(storage, info, guard, qualification, expected):
    # This calls the unchanged original qualification guard and also requires
    # the completed native precision run, all 2000 statepoints and its analysis.
    guard.reference_ready(storage, info, qualification, expected)
    required_qualification = dict(path=str(qualification.resolve()), sha256=expected)
    claim_path = STORAGE.parent / 'execution_claim.json'
    claim = json.loads(base.require_file(claim_path).read_text())
    if claim.get('declaration_sha256') != STORAGE_SHA or claim.get('case') != 'ABA' or claim.get('retries') != 0:
        raise base.Refusal('actual guarded ABA execution claim required')
    status_path = PROD / 'ABA/run_status.json'
    status = json.loads(base.require_file(status_path).read_text())
    case_status = status.get('cases', {}).get('ABA', {})
    if (status.get('classification') != 'WAITING_REFERENCE' or status.get('case') != 'ABA'
            or status.get('prepared_sha256') != PREPARED_SHA
            or case_status.get('classification') != 'VALID_MET'
            or status.get('reference_qualification') != required_qualification):
        raise base.Refusal('actual same-study qualified ABA fixed point required')
    if status.get('alpha') != 1 or status.get('outer_gate') != 5e-7 or status.get('wall_cap_seconds_per_case') != 18860 or status.get('max_maps_per_case') != 100:
        raise base.Refusal('original ABA iteration controls required')
    final = Path(case_status['final_directory'])
    if final.parent != PROD / 'ABA' or final.is_symlink():
        raise base.Refusal('actual ABA final state must remain in its case directory')
    bootstrap = PROD / 'ABA/bootstrap'
    for path in (PROD / 'archives', PROD / 'training', bootstrap, final):
        base.verify_sealed_directory(path)
    stages_path = PROD / 'ABA/stages.json'
    stages = json.loads(base.require_file(stages_path).read_text())['stages']
    if not stages or any(row['status'] != 'PASS' for row in stages):
        raise base.Refusal('all actual bounded ABA stages must pass')
    gate = base.parse_gate((final / 'check_convergence_gate.log').read_text())
    if gate['classification'] != 'VALID_MET' or gate['defects'] != case_status['maps'][-1]['defects']:
        raise base.Refusal('actual sealed native convergence gate differs from status')
    common_sha = base.sha256(PROD / 'training/common_basis.xsm')
    if status.get('common_basis_sha256') != common_sha:
        raise base.Refusal('ABA must retain the same once-built common basis')
    base.require_file(bootstrap / 'basis_reference.xsm', common_sha)
    return status_path, claim_path, stages_path, bootstrap, final


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'run'])
    parser.add_argument('declaration', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--reference-qualification', type=Path)
    parser.add_argument('--reference-sha256')
    args = parser.parse_args()
    _, storage, info, guard, snapshot = load(args.declaration, args.sha256)
    if args.action == 'preflight':
        print(json.dumps(dict(status='STATIC_EXPORT_INPUTS_READY_ACTUAL_AAA_AND_ABA_RESULTS_PENDING',
            numeric_child_launched=False, ABA_reference_measurement_admitted=False,
            independent_ABA_accuracy_qualified=False, resources=snapshot)))
        return
    status_path, claim_path, stages_path, bootstrap, final = ready(
        storage, info, guard, args.reference_qualification, args.reference_sha256)
    exporter = ART / 'axial-material-tools-20261003/export_observables'
    base.require_file(exporter, '81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524', True)
    inputs = {'track.xsm': bootstrap / 'initial_axial_track.xsm',
        'axial.xsm': final / 'closed_axial.xsm', 'macro.xsm': bootstrap / 'initial_axial_macrolib.xsm'}
    resources = base.DiskResources(ART, storage['resource_roots'], 8 * 2**30, 64 * 2**30)
    before = resources.check()
    out = DECLARATION.parent / 'observables'
    out.mkdir(exist_ok=False)
    (out / 'runtime').mkdir()
    (out / 'ABA').mkdir()
    bounded = PROD / 'runtime/run_bounded_dragon.py'
    shutil.copy2(bounded, out / 'runtime/run_bounded_dragon.py')
    for name, path in inputs.items():
        (out / name).symlink_to(path)
    paths = [Path(__file__).resolve(), args.declaration, GUARD, STORAGE,
        Path(args.reference_qualification), status_path, claim_path, stages_path,
        PROD / 'prepared.json', Path(info['case_spec']['path']), PROD / 'runtime/production_runner.py',
        PROD / 'runtime/production_inputs.py', bounded, out / 'runtime/run_bounded_dragon.py',
        bootstrap / 'result.json', final / 'result.json', PROD / 'training/common_basis.xsm',
        exporter, ROOT / 'validation/axial_material/export_observables.f90', *inputs.values()]
    protocol = dict(schema='AXMAT_SAVED_MET_REAL64_ABA_OBSERVABLE_EXPORT_V1', case='ABA',
        implementation=pin(Path(__file__).resolve()), prepared=pin(PROD / 'prepared.json'),
        AAA_qualification=pin(args.reference_qualification), ABA_status=pin(status_path),
        ABA_execution_claim=pin(claim_path), final_stage_seal=pin(final / 'result.json'),
        exporter=pin(exporter), execution_resource_addendum=pin(STORAGE),
        files={str(path.resolve()): base.sha256(path) for path in paths},
        wall_seconds=60, threads=1, retries=0, resource_roots=storage['resource_roots'],
        artifact_budget_bytes=64 * 2**30, min_free_bytes=8 * 2**30,
        scope='Saved ABA fixed-point observables only. Physical input review and independent ABA CE accuracy still required.')
    base.dump_json(out / 'protocol.json', protocol)
    result = dict(classification='EXPORT_FAILED_NO_RETRY', case='ABA', error=None,
        independent_ABA_accuracy_qualified=False, new_transport_launched=False)
    try:
        runner = base.SerialExecutor(out, 60, 'ABA', resources)
        text = runner.execute(out, 'export', [str(exporter), 'track.xsm', 'axial.xsm', 'macro.xsm', 'observables'], 60)
        if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in text.splitlines()):
            raise base.Refusal('actual native REAL64 export completion marker required')
        for name, wanted in protocol['files'].items():
            base.require_file(Path(name), wanted)
        base.verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
        for path in (PROD / 'archives', PROD / 'training', bootstrap, final):
            base.verify_sealed_directory(path)
        result.update(classification='SAVED_ABA_MET_REAL64_OBSERVABLES_EXPORTED',
            protocol=pin(out / 'protocol.json'), inputs_unchanged=True, resources_before=before,
            resources_after=resources.check(), outputs={p.name: base.sha256(p) for p in out.glob('observables.*')})
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        base.dump_json(out / 'export_receipt.json', result)
    print(json.dumps(dict(classification=result['classification'], receipt=pin(out / 'export_receipt.json'))))


if __name__ == '__main__':
    main()

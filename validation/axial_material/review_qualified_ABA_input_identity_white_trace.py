"""Check a real qualified ABA bootstrap against the sealed physical definitions.

Only the actual guarded ABA fixed point permits a physical-input receipt.
Independent CE accuracy and a neutron-balance proof remain separate results.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
DIAG = ART / 'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004'
DECLARATION = DIAG / 'aba_measurement/input_review_declaration.json'
EXPORT_ENTRY = ROOT / 'validation/axial_material/export_qualified_ABA_observables_white_trace.py'
EXPORT_SHA = 'e711ce8e52539039185620ccc60631e7944f3f0efb58aeb1afb9c546ad5c4794'
EXPORT_DECL_SHA = 'bde75f434ba237509357fbb2de9bf3fea8e3f0377cf1ea3bb0111ecfc00f8229'
sys.path.insert(0, str(PROD / 'runtime'))
import production_runner as base
from snapshot_control_preflight import _open_xsm
from white_receiver_tracking import verify_white_tracking_copy


def pin(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=base.sha256(path))


def imported(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'review'])
    parser.add_argument('declaration', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--reference-qualification', type=Path)
    parser.add_argument('--reference-sha256')
    args = parser.parse_args()
    if args.declaration.resolve() != DECLARATION:
        raise base.Refusal('only the frozen ABA physical-review declaration is accepted')
    declaration = json.loads(base.require_file(args.declaration, args.sha256).read_text())
    if declaration.get('schema') != 'AXMAT_ABA_ACTUAL_PHYSICAL_INPUT_REVIEW_ENTRY_V1':
        raise base.Refusal('explicit ABA actual-input-review entry required')
    for name, wanted in declaration['files'].items():
        base.require_file(Path(name), wanted)
    if declaration['files'].get(str(Path(__file__).resolve())) != base.sha256(Path(__file__).resolve()):
        raise base.Refusal('actual physical-review entry is not frozen')
    base.require_file(EXPORT_ENTRY, EXPORT_SHA)
    export = imported(EXPORT_ENTRY, 'aba_input_review_saved_state_guard')
    _, storage, info, guard, _ = export.load(DIAG / 'aba_measurement/declaration.json', EXPORT_DECL_SHA)
    if args.action == 'preflight':
        print(json.dumps(dict(status='STATIC_PHYSICAL_REVIEW_READY_ACTUAL_AAA_AND_ABA_EVIDENCE_PENDING',
            actual_ABA_track_checked=False, physical_equivalence_receipt_created=False,
            new_numeric_child_launched=False, independent_ABA_accuracy_qualified=False)))
        return
    status_path, claim_path, stages_path, bootstrap, final = export.ready(
        storage, info, guard, args.reference_qualification, args.reference_sha256)
    old_helper_path = ROOT / 'validation/axial_material/review_qualified_AB_input_identity_white_trace.py'
    old_helper = imported(old_helper_path, 'original_scalar_tracking_record_reader')
    definition_path = ART / 'axial-material-tools-20261003/input_equivalence.json'
    definition = json.loads(definition_path.read_text())
    if definition['status'] != 'PHYSICAL_INPUT_DEFINITION_AND_CE_MAPPING_CHECKED_PENDING_SPOT_AXIAL_RECORDS':
        raise base.Refusal('original physical-definition-only proof scope differs')
    for name, wanted in definition['input_sha256'].items():
        base.require_file(Path(name), wanted)
    physical = definition['cases']['ABA']
    if physical['composition_by_physical_zone'] != list('ABA') or physical['white_side_surfaces'] != 6 or physical['axial_end_vacuum_planes'] != [0, 150]:
        raise base.Refusal('original ABA composition/boundary declaration differs')
    staged = DIAG / 'aba_reference_inputs'
    archive_review = json.loads((staged / 'initial_archive_review.json').read_text())
    if archive_review['status'] != 'PASS_48_INITIAL_ABA_MATERIAL_AND_GEOMETRY_RECORDS_EXACT' or len(archive_review['records']) != 48:
        raise base.Refusal('sealed exact initial A/B/A material/geometry proof required')
    archive = PROD / 'archives/aba_snapshots.xsm'
    base.require_file(archive, archive_review['archive']['sha256'])
    used = bootstrap / 'case_snapshots.xsm'
    if used.resolve(strict=True) != archive:
        raise base.Refusal('actual ABA bootstrap must consume the declared A/B/A archive')
    base.require_file(used, archive_review['archive']['sha256'])
    markers = verify_white_tracking_copy(bootstrap / 'initial_axial_track_unmarked.xsm', bootstrap / 'initial_axial_track.xsm')
    # The frozen case_setup deck uses the same geometric construction for
    # AAA and ABA. Composition differs in the bound source archive, whose
    # 48 physical records were independently checked above by exact identity.
    baseline = PROD / 'AAA/bootstrap/initial_axial_track_unmarked.xsm'
    actual = bootstrap / 'initial_axial_track_unmarked.xsm'
    records = {}
    names = ('STATE-VECTOR', 'MAT1D', 'MATCOD', 'KEYFLX', 'AREA2D', 'VOL1D', 'VOLUME',
        'NCODE', 'ICODE', 'ZCODE', 'U', 'W', 'PL', 'KEYFLX$ANIS')
    dynamic = [status_path, claim_path, stages_path, bootstrap / 'result.json', final / 'result.json',
        used, archive, baseline, actual, bootstrap / 'initial_axial_track.xsm', Path(args.reference_qualification)]
    before = {str(path.resolve()): base.sha256(path) for path in dynamic}
    with _open_xsm(actual) as new, _open_xsm(baseline) as old:
        for name in names:
            value = old_helper.scalar(new, new.root, name)
            if value != old_helper.scalar(old, old.root, name):
                raise base.Refusal('actual ABA geometric/mapping record differs: ' + name)
            records[name] = dict(length_words=value[0][0], type=value[0][1],
                sha256=hashlib.sha256(value[1]).hexdigest())
    identities = {**declaration['files'], **definition['input_sha256'], **before}
    for name, wanted in identities.items():
        base.require_file(Path(name), wanted)
    result = dict(schema_version=1, status='PASS', case='ABA', experiment_id=info['experiment_id'],
        case_spec_sha256=info['case_spec']['sha256'], production_prepared=pin(PROD / 'prepared.json'),
        implementation=pin(Path(__file__).resolve()), review_declaration=pin(args.declaration),
        AAA_qualification=pin(args.reference_qualification), ABA_status=pin(status_path),
        actual_ABA_execution_claim=pin(claim_path), final_stage_seal=pin(final / 'result.json'),
        previous_physical_definition=pin(definition_path), initial_archive_review=pin(staged / 'initial_archive_review.json'),
        actual_archive=pin(archive), actual_bootstrap_source_archive=pin(used),
        actual_axial_track=pin(bootstrap / 'initial_axial_track.xsm'), conditional_marker_review=markers,
        actual_track_record_identity=records, exact_initial_ABA_physical_records=48,
        CE_inputs={name: pin(staged / name) for name in ('materials.xml', 'geometry.xml', 'settings.xml', 'tallies.xml', 'reference_contract.json')},
        input_identities=identities, original_density_formula_and_XML_audit_reused_by_identity=True,
        independent_ABA_accuracy_qualified=False, new_transport_launched=False,
        limits=['Actual physical input mapping only; no independent ABA accuracy or neutron-balance claim.',
            'The staged CE inputs require separately bound native execution and analysis declarations before transport.'])
    output = DIAG / 'aba_measurement/input_equivalence_ABA.json'
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=result['status'], case='ABA', output=pin(output))))


if __name__ == '__main__':
    main()

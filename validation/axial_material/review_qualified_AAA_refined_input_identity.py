"""Read-only physical input and original observation-bin audit for refined AAA.

The complete fresh fixed point and native observable export must exist first.
Same physical inputs permit reuse of the retained independent CE sample; they
do not establish its statistics, coupled accuracy, or ABA admission.
"""
import csv
import json
import math
from pathlib import Path
import sys

import numpy as np

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
OLD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OBS = ART / 'axial-material-qualified-AAA-white-trace-refined-observables-20261005'
ADMISSION = ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005'
PREPARED_SHA = '024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'
OLD_PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import require_file, sha256, verify_prepared, verify_sealed_directory
from white_receiver_tracking import verify_white_tracking_copy
from qualified_snapshot_ingestion import descriptor, list_handles
from snapshot_control_preflight import _open_xsm


def read(path):
    return json.loads(Path(path).read_text())


def scalar(archive, directory, name):
    item = directory[name]
    if item[2] not in (1, 2, 3, 4) or item[1] <= 0:
        raise ValueError('invalid scalar physical record: ' + name)
    return item[1:], archive.read(item[0], item[1])


def record(archive, name, count, kind, dtype):
    return np.frombuffer(archive.record(archive.root, name, count, kind), dtype=dtype)


def track_geometry(new_path, old_path):
    """Check complete materials, real volumes, vacuum and exact admitted grid."""
    cold = ART / 'axial-material-AAA-white-trace-angular-convergence-20261005/cold48_sn32/track.xsm'
    with _open_xsm(new_path) as new, _open_xsm(old_path) as old, _open_xsm(cold) as admitted:
        for name in ('AREA2D', 'NCODE', 'ICODE', 'ZCODE'):
            if scalar(new, new.root, name) != scalar(old, old.root, name):
                raise ValueError('original physical cross-section or vacuum changed: ' + name)
        for name in ('U', 'W', 'PL'):
            if scalar(new, new.root, name) != scalar(admitted, admitted.root, name):
                raise ValueError('actual angular grid differs from admitted SN32: ' + name)
        old_material = record(old, 'MAT1D', 12, 1, '<i4')
        new_material = record(new, 'MAT1D', 48, 1, '<i4')
        if not np.array_equal(new_material, np.repeat(old_material, 4)):
            raise ValueError('fine-cell physical-zone material owners changed')
        # TRACK stores all axial cells of radial region 1 first, then region 2.
        old_mix = record(old, 'MATCOD', 96, 1, '<i4').reshape(8, 12)
        new_mix = record(new, 'MATCOD', 384, 1, '<i4').reshape(8, 48)
        if not np.array_equal(new_mix, np.repeat(old_mix, 4, axis=1)):
            raise ValueError('fine-cell radial material owners changed')
        heights = record(new, 'VOL1D', 48, 2, '<f4').astype(float)
        old_heights = record(old, 'VOL1D', 12, 2, '<f4').astype(float)
        if (not np.array_equal(heights, np.full(48, 3.125))
                or not np.array_equal(heights.reshape(12, 4).sum(axis=1), old_heights)
                or any(math.fsum(heights[z*16:(z+1)*16]) != 50 for z in range(3))):
            raise ValueError('physical heights or original observation edges changed')
        volumes = record(new, 'VOLUME', 384, 2, '<f4').astype(float).reshape(8, 48)
        old_volumes = record(old, 'VOLUME', 96, 2, '<f4').astype(float).reshape(8, 12)
        summed = volumes.reshape(8, 12, 4).sum(axis=2)
        error = float(np.max(abs(summed-old_volumes)/old_volumes))
        if not np.isfinite(volumes).all() or np.any(volumes <= 0) or error > 5e-6:
            raise ValueError('physical volume mapping failed original tolerance')
        return dict(status='PASS_ORIGINAL_PHYSICAL_GEOMETRY_WITH_DECLARED_REFINEMENT',
            complete_material_owners_exact=True, original_radial_area_and_vacuum_words_exact=True,
            SN32_quadrature_words_exact_to_admitted_grid=True,
            native_cells=48, observation_cells=12, physical_zone_heights_cm=[50, 50, 50],
            original_cell_volume_max_relative_difference=error,
            original_volume_tolerance=5e-6)


def review():
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    status_path = PROD / 'AAA/run_status.json'
    status = read(status_path)
    if status['classification'] != 'WAITING_REFERENCE' or status['cases'].get('AAA', {}).get('classification') != 'VALID_MET':
        raise ValueError('actual complete fresh coupled AAA fixed point required')
    final = Path(status['cases']['AAA']['final_directory'])
    for folder in (PROD / 'archives', PROD / 'training', PROD / 'AAA/bootstrap', final):
        verify_sealed_directory(folder)
    export = read(OBS / 'export_receipt.json')
    if (export['classification'] != 'SAVED_MET_REAL64_OBSERVABLES_EXPORTED'
            or not export['inputs_unchanged'] or not export['implementation_unchanged']):
        raise ValueError('actual complete immutable native fine observable export required')
    for name, wanted in export['outputs'].items():
        require_file(OBS / name, wanted)
    protocol = export['protocol']
    require_file(Path(protocol['path']), protocol['sha256'])
    exported = read(protocol['path'])
    if exported['production_prepared'] != descriptor(PROD / 'prepared.json') or exported['AAA_status'] != descriptor(status_path):
        raise ValueError('fine observables do not bind this final coupled state')
    for name, wanted in exported['source_inputs'].items():
        require_file(Path(name), wanted)
    old_info = read(require_file(OLD / 'prepared.json', OLD_PREPARED_SHA))
    spec = read(Path(info['case_spec']['path']))
    parent_spec = read(require_file(Path(old_info['case_spec']['path']), old_info['case_spec']['sha256']))
    geometry = dict(spec['geometry'], cells_per_zone=4)
    if geometry != parent_spec['geometry'] or any(spec[k] != parent_spec[k] for k in ('materials', 'cases', 'reference', 'predeclared_decisions')):
        raise ValueError('physical, reference or independent scientific definitions changed')
    prior_equivalence = CE / 'input_equivalence_AAA.json'
    require_file(prior_equivalence, '7758243c80bdfae56ded546079d18379a19bbc605fd0a7b7f3646eaab6653a34')
    prior = read(prior_equivalence)
    if prior['status'] != 'PASS':
        raise ValueError('prior full physical/reference proof is not PASS')
    for name, wanted in prior['input_identities'].items():
        require_file(Path(name), wanted)
    tools = ART / 'axial-material-tools-20261003'
    base_review = read(tools / 'input_equivalence_rank1_AAA.json')
    for proof in (read(tools / 'input_equivalence_rank1_AAA_receipt.json')['files'], base_review['input_sha256']):
        for name, wanted in proof.items():
            require_file(Path(name), wanted)
    tracked = PROD / 'AAA/bootstrap/initial_axial_track.xsm'
    marker = verify_white_tracking_copy(PROD / 'AAA/bootstrap/initial_axial_track_unmarked.xsm', tracked)
    geometry_check = track_geometry(tracked, OLD / 'AAA/bootstrap/initial_axial_track.xsm')
    checked = ('ISOTOPERNAME', 'ISOTOPESMIX', 'ISOTOPESDENS', 'ISOTOPESTEMP',
               'ISOTOPESUSED', 'ISOTOPESVOL', 'MIXTURESVOL', 'ENERGY')
    radial = ('MATCOD', 'KEYFLX', 'VOLUME', 'NZON$MCCG', 'V$MCCG', 'ZMU$MCCG', 'WZMU$MCCG', 'XMU$MCCG')
    original_snapshot = ART / 'axial-material-inputs-20261003/A/snapshot_A.xsm'
    archive = PROD / 'archives/aaa_snapshots.xsm'
    with _open_xsm(archive) as new, _open_xsm(original_snapshot) as old:
        for obj, names in (('MICROLIB2', checked), ('TRACK', radial)):
            old_dir = old.object(obj)
            handles = list_handles(new, new.root, obj, 3)
            if any(h[1:] != (-1, 0) for h in handles):
                raise ValueError('all three archive slots must be real object directories')
            for slot, handle in enumerate(handles, 1):
                new_dir = new.directory(handle[0])
                for name in names:
                    if scalar(new, new_dir, name) != scalar(old, old_dir, name):
                        raise ValueError(f'actual AAA material/radial input changed: {obj}/{slot}/{name}')
    contract_path = CE / 'AAA/reference_contract.json'
    for item in prior['CE_inputs'].values():
        require_file(Path(item['path']), item['sha256'])
    contract = read(contract_path)
    if contract['case'] != 'AAA' or len(contract['region_layer_bins']) != 96 or len(contract['plane_bins']) != 13:
        raise ValueError('same complete independent original observation contract required')
    with (OBS / 'observables.regions.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    by_key = {(int(row['radial_region']), int(row['axial_cell'])): row for row in rows}
    if len(by_key) != 384 or len(rows) != 384 or set(by_key) != {(r, c) for r in range(1, 9) for c in range(1, 49)}:
        raise ValueError('complete native fine volume map required')
    bin_errors = []
    for row in contract['region_layer_bins']:
        region, cell = row['region'], row['production_axial_cell']
        if (row['composition'] != 'A' or row['physical_zone'] != (cell-1)//4+1
                or row['z_low_cm'] != 12.5*(cell-1) or row['z_high_cm'] != 12.5*cell):
            raise ValueError('independent physical observation bin changed')
        volume = math.fsum(float(by_key[region, c]['volume_cm3']) for c in range(4*(cell-1)+1, 4*cell+1))
        error = abs(volume-row['volume_cm3'])/row['volume_cm3']
        if error > 5e-6:
            raise ValueError('fine/independent original-bin physical volume mismatch')
        bin_errors.append(error)
    paths = [Path(__file__).resolve(), PROD / 'prepared.json', status_path, final / 'result.json',
             OBS / 'export_receipt.json', Path(protocol['path']), tracked, archive,
             original_snapshot, prior_equivalence, contract_path,
             Path(info['case_spec']['path']), Path(old_info['case_spec']['path']),
             *[OBS / ('observables.'+s) for s in ('regions.csv', 'faces.csv', 'summary.txt')]]
    return dict(schema_version=1, case='AAA', status='PASS', experiment_id=info['experiment_id'],
        case_spec_sha256=info['case_spec']['sha256'], production_prepared=descriptor(PROD / 'prepared.json'),
        AAA_status=descriptor(status_path), actual_archives=descriptor(archive), actual_axial_track=descriptor(tracked),
        inherited_full_physical_proof=descriptor(prior_equivalence),
        previous_sealed_audit_inputs_reverified=len(base_review['input_sha256']),
        material_records_exact_in_all_AAA_slots=list(checked), radial_tracking_records_exact=list(radial),
        conditional_marker_review=marker, refined_geometry_review=geometry_check,
        original_observation_bin_count=96, original_observation_plane_count=13,
        original_bin_CE_volume_max_relative_difference=max(bin_errors), original_volume_tolerance=5e-6,
        original_physical_and_independent_scientific_definitions_unchanged=True,
        CE_inputs=prior['CE_inputs'], input_identities={str(p): sha256(p) for p in paths},
        reference_sample_reused_by_identity=True, AAA_accuracy_qualified=False, ABA_admitted=False,
        limits='Physical equivalence and original observation mapping only. Complete source, '
               'statistical, shape/keff and current/symmetry analyses remain mandatory; no full neutron balance claim.')


if __name__ == '__main__':
    result = review()
    with (OBS / 'input_equivalence_AAA.json').open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=result['status'], case=result['case'], ABA_admitted=False)))

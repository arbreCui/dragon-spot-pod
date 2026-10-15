"""Conservative 48-to-12 observation view, after complete fine-data admission.

This reads saved observables only. It cannot qualify a coupled calculation or
launch transport. Four whole cells form each unchanged physical observation
bin; each observation plane is an existing fine face, with its original sign.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np


def write_csv(path, rows):
    with Path(path).open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def project(source, output, current_checker, fine_rules):
    source, output = Path(source), Path(output)
    if (fine_rules['radial_regions'], fine_rules['axial_cells'],
            fine_rules['groups'], fine_rules['height_cm']) != (8, 48, 370, 150):
        raise ValueError('exact admitted 8-region/48-cell/370-group/150-cm layout required')
    paths = [source / ('observables.' + s) for s in ('regions.csv', 'faces.csv', 'summary.txt')]
    fine = current_checker.read_production(*paths, fine_rules)
    fine_checks = current_checker.evaluate_production(fine, fine_rules)
    if any(v != 'PASS' for v in fine_checks['checks'].values()):
        raise ValueError('complete fine positivity/sign/accounting/symmetry checks must pass')
    rows = current_checker.rows_from_csv(paths[0])
    faces = current_checker.rows_from_csv(paths[1])
    lookup = {(int(x['radial_region']), int(x['axial_cell'])): x for x in rows}
    face_lookup = {(int(x['radial_region']), int(x['face'])): x for x in faces}
    denominator = float(fine['summary']['global_nufission'])
    coarse, mapping = [], []
    for region in range(1, 9):
        for cell in range(1, 13):
            fine_cells = list(range(4 * (cell - 1) + 1, 4 * cell + 1))
            members = [lookup[region, index] for index in fine_cells]
            if ({int(x['physical_zone']) for x in members} != {(cell - 1) // 4 + 1}
                    or len({int(x['material']) for x in members}) != 1):
                raise ValueError('observation bin crosses a physical material or zone boundary')
            row = dict(members[0], axial_cell=str(cell))
            for field in ('volume_cm3', 'integrated_flux', 'integrated_nufission'):
                row[field] = format(math.fsum(float(x[field]) for x in members), '.17e')
            row['flux_per_global_nufission'] = format(float(row['integrated_flux']) / denominator, '.17e')
            row['nufission_fraction'] = format(float(row['integrated_nufission']) / denominator, '.17e')
            # These witnesses preserve every fine entry; they do not claim an
            # independently solved or locally normalized coarse group field.
            row['minimum_group_flux'] = format(min(float(x['minimum_group_flux']) for x in members), '.17e')
            row['nonpositive_group_flux_count'] = str(sum(int(x['nonpositive_group_flux_count']) for x in members))
            coarse.append(row)
            mapping.append(dict(radial_region=region, observation_cell=cell,
                fine_cells=fine_cells, physical_zone=int(row['physical_zone']),
                volume_cm3=float(row['volume_cm3']),
                integrated_flux=float(row['integrated_flux']),
                integrated_nufission=float(row['integrated_nufission'])))
    coarse_faces = [dict(face_lookup[region, 4 * face], face=str(face))
                    for region in range(1, 9) for face in range(13)]
    for region in range(1, 9):
        for face in range(13):
            original = face_lookup[region, 4 * face]
            if float(original['z_cm']) != 12.5 * face:
                raise ValueError('original observation plane has no exact fine face')
    conservation = {}
    for field in ('volume_cm3', 'integrated_flux', 'integrated_nufission'):
        before = math.fsum(float(x[field]) for x in rows)
        after = math.fsum(float(x[field]) for x in coarse)
        bound = current_checker.gamma(len(rows) + len(coarse) + 2, fine_rules['epsilon64']) * abs(before)
        if abs(after - before) > bound:
            raise ValueError('complete integral conservation failed: ' + field)
        conservation[field] = dict(fine_sum=before, observation_sum=after,
                                   absolute_difference=abs(after - before), roundoff_bound=bound)
    j = np.array([[float(face_lookup[r, 4 * f]['integrated_net_current_plus_z'])
                   for f in range(13)] for r in range(1, 9)])
    escape = math.fsum(j[:, -1]) - math.fsum(j[:, 0])
    residual = math.fsum(np.diff(j, axis=1).ravel()) - escape
    summary = dict(fine['summary'], axial_cells='12',
        current_telescoping_difference=format(residual / denominator, '.17e'))
    coarse_rules = dict(fine_rules, axial_cells=12)
    output.mkdir(exist_ok=False)
    write_csv(output / 'observables.regions.csv', coarse)
    write_csv(output / 'observables.faces.csv', coarse_faces)
    with (output / 'observables.summary.txt').open('x') as stream:
        stream.write('CONSERVATIVE OBSERVATION VIEW OF ADMITTED SAVED 48-CELL REAL64 DATA\n')
        for key, value in summary.items():
            stream.write(key + '=' + str(value) + '\n')
    view = current_checker.read_production(
        *[output / ('observables.' + s) for s in ('regions.csv', 'faces.csv', 'summary.txt')], coarse_rules)
    view_checks = current_checker.evaluate_production(view, coarse_rules)
    if any(v != 'PASS' for v in view_checks['checks'].values()):
        raise ValueError('derived observation view failed original checks')
    receipt = dict(classification='PASS_COMPLETE_FINE_AND_CONSERVATIVE_ORIGINAL_OBSERVATION_VIEW',
        native_axial_cells=48, observation_cells=12, radial_regions=8,
        original_checks_on_all_fine_entries=fine_checks,
        original_checks_on_observation_view=view_checks,
        complete_integral_conservation=conservation, mapping=mapping,
        face_map=[dict(observation_face=f, fine_face=4*f, z_cm=12.5*f) for f in range(13)],
        single_exporter_global_nufission=denominator,
        local_or_binwise_normalization=False, bins_removed=False,
        transport_launched=False, coupled_accuracy_qualified=False,
        scope='All 384 fine region/cell rows and 392 fine region/face rows are admitted first. '
              'All 96 observation integrals are exact fixed four-cell sums, using the same '
              'one exporter denominator. All 13 observation faces preserve existing fine '
              'currents and signs. Coarse telescoping is recomputed for this observation '
              'view; the separate full fine accounting result remains mandatory.')
    with (output / 'projection_receipt.json').open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    return receipt

#!/usr/bin/env python3
"""Construct independent CE AAA/ABA pin inputs; never launch transport."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

import openmc

ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / 'data/rnr_0burn_spot_proc/irena_pincell.dat'
MATERIAL_BUILDER = ROOT / 'validation/d4_reference/build_d4a_ce_reference.py'
SIDE = 0.61776479
RADII = (0.11, 0.308712, 0.381084, 0.412536, 0.4225, 0.435, 0.485)
ZONE_EDGES = (0.0, 50.0, 100.0, 150.0)
COMPOSITIONS = {'A': (0.21, 0.79), 'B': (0.2436, 0.7564)}
REGION_MATERIAL = {1: 'coolant', 2: 'clad', 3: 'he_gap', 4: 'fuel',
                   5: 'fuel', 6: 'fuel', 7: 'fuel', 8: 'he_hole'}


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


@dataclass(frozen=True)
class ReferenceConfig:
    # Four per material zone matches the production twelve-cell output map.
    tally_cells_per_zone: int = 4
    particles: int = 50000
    inactive: int = 100
    active: int = 250
    seed: int = 917031
    statepoint_every_active_batch: bool = True

    def validate(self):
        for name in ['tally_cells_per_zone', 'particles', 'active', 'seed']:
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f'{name} must be a positive integer')
        if self.tally_cells_per_zone % 4:
            raise ValueError('fine tally cells per zone must be a multiple of four')
        if type(self.inactive) is not int or self.inactive < 0:
            raise ValueError('inactive must be a nonnegative integer')
        if type(self.statepoint_every_active_batch) is not bool:
            raise ValueError('statepoint flag must be boolean')


def boundary_evidence():
    """Read the actual pin file and SALT route, rather than legacy CE defaults."""
    text = PIN.read_text()
    header = re.search(r'\* typge[^\n]*\n([^\n]+)', text)
    if header is None or [int(x) for x in header[1].split(',')][:6] != [0, 0, 8, 13, 1, 8]:
        raise ValueError('pin topology changed')
    circles = []
    for match in re.finditer(r'\* ELEM\s+\d+\s+circle\s*\n([^\n]+)\n\*\s*\n([^\n]+)', text):
        tag = [int(x) for x in match[1].split(',')]
        values = [float(x) for x in match[2].split(',')]
        circles.append((values[2], tag[1], tag[2]))
    if sorted(circles) != [(radius, 8-i, 7-i) for i, radius in enumerate(RADII)]:
        raise ValueError('pin radial region/interface map changed')
    segments = []
    for match in re.finditer(r'\* ELEM\s+\d+\s+line segment\s*\n([^\n]+)\n\*\s*\n([^\n]+)', text):
        tag = [int(x) for x in match[1].split(',')]
        x, y, dx, dy = [float(x) for x in match[2].split(',')]
        if tag != [1,0,1]:
            raise ValueError('outer surface/region adjacency changed')
        segments.append(((x,y),(x+dx,y+dy)))
    vertices = [(SIDE*math.cos(i*math.pi/3), SIDE*math.sin(i*math.pi/3)) for i in range(6)]
    if len(segments) != 6 or any(min(math.dist(point,v) for v in vertices)>2e-8
                                 for segment in segments for point in segment):
        raise ValueError('nominal outer hexagonal dimensions changed')
    if not re.search(r'\* boundaries conditions:[^\n]*\n\s*0,\s*0,\s*0\s*\n\* albedo\s*\n\s*1\.0\s*\n', text):
        raise ValueError('pin isotropic unit-albedo boundary changed')
    route = ROOT / 'data/SpotSnapBld.c2m'
    if route.read_text().count('TISO 48 100.0 LONG') != 2:
        raise ValueError('pin SALT tracking route changed')
    source = ROOT / 'src/SAL_GEOMETRY_MOD.f90'
    if '0 = all external surfaces are isotropically reflected' not in source.read_text():
        raise ValueError('SALT default-boundary meaning unavailable')
    return dict(boundary_type='white', albedo=1.0, tracking='TISO 48 100.0 LONG',
                explanation='DEFAUL=0: isotropic return on each external surface; not specular.',
                evidence={str(p.relative_to(ROOT)): digest(p) for p in [PIN, route, source]})


def density_builder():
    spec = importlib.util.spec_from_file_location('axmat_corrected_density_builder', MATERIAL_BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for relative, expected in module.CORRECTED_SOURCE_SHA256.items():
        if Path(relative).name in ['rnr_cc.c2m', 'rnr_interpol.c2m']:
            module.require_hash(ROOT / relative, expected, 'corrected density source')
    return module


def composition_base(builder, composition):
    if composition not in COMPOSITIONS:
        raise ValueError('composition must be A or B')
    # A fresh module is loaded per composition: no shared p_Pu/p_U mutation and
    # no reuse of density values evaluated in the audited module at import time.
    base = builder.load_audited_base(builder.DEFAULT_BASE)
    base.p_Pu, base.p_U = COMPOSITIONS[composition]
    return base


def atom_density_records(materials):
    return {name: dict(temperature_K=material.temperature,
                      atom_density_barn_cm=dict(material.get_nuclide_atom_densities()))
            for name, material in materials.items()}


def region_areas():
    result = {1: 3 * math.sqrt(3) * SIDE**2 / 2 - math.pi * RADII[-1]**2}
    for region in range(2, 9):
        outer_index = 8 - region
        inner = RADII[outer_index - 1] if outer_index else 0.0
        result[region] = math.pi * (RADII[outer_index]**2 - inner**2)
    return result


def build_model(case='AAA', config=ReferenceConfig(), cross_sections=None, energy_edges_ev=None):
    config.validate()
    if case not in ['AAA', 'ABA']:
        raise ValueError('case must be AAA or ABA')
    boundary = boundary_evidence()
    builder = density_builder()
    material_sets = {}
    numbers = {}
    for composition in sorted(set(case)):
        base = composition_base(builder, composition)
        _, mapping, _ = builder.make_floor_materials(base, 1 if composition == 'A' else 2, 750.0)
        # There is no wrapper in the eight-region pin.
        mapping.pop('em10')
        for name, material in mapping.items():
            material.name = f'AXMAT_{composition}_{name}'
        material_sets[composition] = mapping
        numbers[composition] = builder.material_numbers(base, 750.0)
    materials = openmc.Materials([m for group in material_sets.values() for m in group.values()])
    if cross_sections is not None:
        path = Path(cross_sections).resolve(strict=True)
        materials.cross_sections = str(path)
    cylinders = [openmc.ZCylinder(r=radius) for radius in RADII]
    hexagon = openmc.model.HexagonalPrism(edge_length=SIDE, orientation='x', boundary_type='white')
    n = 3 * config.tally_cells_per_zone
    edges = [150.0 * index / n for index in range(n + 1)]
    planes = [openmc.ZPlane(z0=z, boundary_type='vacuum' if i in [0, n] else 'transmission')
              for i, z in enumerate(edges)]
    area = region_areas()
    roots, leaves, bins, layer_bins = [], [], [], []
    for layer in range(n):
        zone = layer // config.tally_cells_per_zone
        composition = case[zone]
        dz = edges[layer + 1] - edges[layer]
        cells = []
        for region in range(1, 9):
            if region == 1:
                radial = +cylinders[-1]
            else:
                index = 8 - region
                radial = -cylinders[index]
                if index:
                    radial &= +cylinders[index - 1]
            material = material_sets[composition][REGION_MATERIAL[region]]
            cell = openmc.Cell(name=f'L{layer+1:03d}_R{region}', fill=material, region=radial)
            cell.volume = area[region] * dz
            cells.append(cell)
            leaves.append(cell)
            bins.append(dict(bin=len(bins), cell_id=cell.id, region=region, material_role=REGION_MATERIAL[region],
                             layer=layer+1, physical_zone=zone+1, composition=composition,
                             production_axial_cell=zone*4+(layer % config.tally_cells_per_zone)*4//config.tally_cells_per_zone+1,
                             z_low_cm=edges[layer], z_high_cm=edges[layer+1], volume_cm3=cell.volume))
        parent = openmc.Cell(name=f'Layer_{layer+1:03d}', fill=openmc.Universe(cells=cells),
                             region=-hexagon & +planes[layer] & -planes[layer+1])
        parent.volume = sum(area.values()) * dz
        roots.append(parent)
        layer_bins.append(dict(bin=layer, cell_id=parent.id, layer=layer+1, physical_zone=zone+1,
                               composition=composition, volume_cm3=parent.volume,
                               region_tally_bins=list(range(layer*8, (layer+1)*8))))
    geometry = openmc.Geometry(openmc.Universe(cells=roots))
    tallies = []
    region_filter = openmc.CellFilter(leaves)
    for name, cell_filter in [('region_layer_rates', region_filter), ('layer_rates', openmc.CellFilter(roots))]:
        tally = openmc.Tally(name=name)
        tally.filters = [cell_filter]
        tally.scores = ['flux', 'nu-fission']
        tally.estimator = 'tracklength'
        tallies.append(tally)
    if energy_edges_ev is not None:
        edges_ev = [float(value) for value in energy_edges_ev]
        if len(edges_ev) < 2 or any(not math.isfinite(v) or v < 0 for v in edges_ev) or any(b <= a for a, b in zip(edges_ev, edges_ev[1:])):
            raise ValueError('energy boundaries must be finite, nonnegative and strictly increasing')
        tally = openmc.Tally(name='region_layer_energy_rates')
        tally.filters = [region_filter, openmc.EnergyFilter(edges_ev)]
        tally.scores = ['flux', 'nu-fission']
        tally.estimator = 'tracklength'
        tallies.append(tally)
    net = openmc.Tally(name='axial_plane_net_current')
    plane_filter = openmc.SurfaceFilter(planes)
    net.filters = [plane_filter]
    net.scores = ['current']
    partial = openmc.Tally(name='axial_plane_directional_current')
    # Global polar angle keeps the +z/-z direction fixed. MuSurfaceFilter
    # flips its normal with the crossed side and cannot separate these signs.
    partial.filters = [plane_filter, openmc.PolarFilter([0.0, math.pi/2, math.pi])]
    partial.scores = ['current']
    tallies += [net, partial]
    settings = openmc.Settings()
    settings.run_mode = 'eigenvalue'
    settings.energy_mode = 'continuous-energy'
    settings.particles = config.particles
    settings.inactive = config.inactive
    settings.batches = config.inactive + config.active
    settings.seed = config.seed
    settings.generations_per_batch = 1
    settings.temperature = {'method': 'interpolation'}
    entropy_mesh = openmc.RegularMesh()
    entropy_mesh.dimension = (4, 4, 12)
    entropy_mesh.lower_left = (-SIDE, -SIDE, 0.0)
    entropy_mesh.upper_right = (SIDE, SIDE, 150.0)
    settings.entropy_mesh = entropy_mesh
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box([-SIDE, -SIDE, 0], [SIDE, SIDE, 150]),
        constraints={'fissionable': True})
    statepoint_batches = (list(range(config.inactive+1, settings.batches+1))
                          if config.statepoint_every_active_batch else [settings.batches])
    settings.statepoint = {'batches': statepoint_batches}
    settings.sourcepoint = {'write': False}
    model = openmc.Model(geometry=geometry, materials=materials, settings=settings, tallies=openmc.Tallies(tallies))
    manifest = dict(schema='AXMAT_CE_INPUT_V2', case=case, transport_executed=False,
                    material_B_status='Declared comparison recipe from a commented alternative; not an asserted IRENA design.',
                    material_B_origin='/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/rnr_0burn.x2m:29',
                    config=asdict(config), required_execution_threads=1,
                    source_entropy_mesh=dict(dimension=[4,4,12], lower_left=[-SIDE,-SIDE,0.0],
                                             upper_right=[SIDE,SIDE,150.0]),
                    statepoint_batches=statepoint_batches, statepoint_every_active_batch=config.statepoint_every_active_batch,
                    batch_statistics='Use cumulative tally sums and n_realizations differences; do not treat cumulative means as independent batches.',
                    temperatures_C=dict(fuel=750.0, clad=620.0, sodium=475.0),
                    compositions={k:dict(p_Pu=v[0], p_U=v[1]) for k,v in COMPOSITIONS.items()},
                    density_values=numbers, materials={k:atom_density_records(v) for k,v in material_sets.items()},
                    boundary=boundary, hex_orientation='x', hex_side_cm=SIDE, radii_cm=RADII,
                    physical_zone_edges_cm=ZONE_EDGES, tally_z_edges_cm=edges,
                    region_layer_bins=bins, layer_bins=layer_bins,
                    plane_bins=[dict(bin=i, surface_id=p.id, z_cm=edges[i], positive_normal='+z',
                                     role='bottom_vacuum' if i==0 else 'top_vacuum' if i==n else 'physical_interface' if edges[i] in [50,100] else 'tally_interface')
                                for i,p in enumerate(planes)],
                    tally_ids={t.name:t.id for t in tallies},
                    current_scope='Full hexagonal cross-section per plane, not region-resolved current; global polar bins retain signed +z current.',
                    directional_current_filter=dict(type='polar', axis='+z',
                        angle_edges_rad=[0.0,math.pi/2,math.pi],
                        raw_bin_order=['positive_z','negative_z'],
                        signed_score=True,
                        note='SurfaceFilter current uses fixed ZPlane +z normal; PolarFilter uses the global direction, not a side-flipped surface normal.'),
                    flux_units='Cell-integrated tracklength per source particle; divide by recorded physical cell volume for scalar flux.',
                    fission_units='Cell-integrated nu-fission production per source particle; never substitute for flux.',
                    source_identity={str(MATERIAL_BUILDER.relative_to(ROOT)):digest(MATERIAL_BUILDER),
                                     str(builder.DEFAULT_BASE.relative_to(ROOT)):digest(builder.DEFAULT_BASE),
                                     str(Path(__file__).resolve().relative_to(ROOT)):digest(Path(__file__)),
                                     **{relative:digest(ROOT/relative) for relative in builder.CORRECTED_SOURCE_SHA256
                                        if Path(relative).name in ['rnr_cc.c2m','rnr_interpol.c2m']}},
                    cross_sections=None if cross_sections is None else dict(path=str(path),sha256=digest(path)),
                    energy_edges_ev=None if energy_edges_ev is None else edges_ev)
    static_check(model, manifest)
    return model, manifest


def static_check(model, manifest):
    """Check physical sample points and boundary/tally topology without tracking."""
    surfaces = model.geometry.get_all_surfaces()
    if sum(surface.boundary_type == 'white' for surface in surfaces.values()) != 6:
        raise ValueError('six white radial planes required')
    if sum(surface.boundary_type == 'vacuum' for surface in surfaces.values()) != 2:
        raise ValueError('only top and bottom may be vacuum')
    sample_radii = {1:(RADII[-1]+math.sqrt(3)*SIDE/2)/2}
    for region in range(2,9):
        index = 8-region
        sample_radii[region] = (RADII[index] + (RADII[index-1] if index else 0.0))/2
    for record in manifest['region_layer_bins']:
        radius = sample_radii[record['region']]
        z = (record['z_low_cm']+record['z_high_cm'])/2
        for angle in [0, math.pi/3, math.pi, 4*math.pi/3]:
            path = model.geometry.find((radius*math.cos(angle), radius*math.sin(angle), z))
            if not path or path[-1].id != record['cell_id']:
                raise ValueError(f'cell mapping failed: {record}')
    if not math.isclose(sum(row['volume_cm3'] for row in manifest['region_layer_bins']),
                        150*3*math.sqrt(3)*SIDE**2/2, rel_tol=1e-13):
        raise ValueError('pin volume partition failed')


def export_inputs(output, case='AAA', config=ReferenceConfig(), cross_sections=None, energy_edges_ev=None):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('input export requires a new or empty directory')
    model, manifest = build_model(case, config, cross_sections, energy_edges_ev)
    output.mkdir(parents=True, exist_ok=True)
    model.export_to_xml(directory=output)
    manifest['input_hashes'] = {path.name:digest(path) for path in sorted(output.glob('*.xml'))}
    with (output/'reference_contract.json').open('x') as stream:
        json.dump(manifest, stream, indent=2, allow_nan=False)
        stream.write('\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--case', choices=['AAA','ABA'], default='AAA')
    parser.add_argument('--cross-sections', type=Path)
    parser.add_argument('--energy-edges-json', type=Path)
    parser.add_argument('--tally-cells-per-zone', type=int, default=4)
    parser.add_argument('--particles', type=int, default=50000)
    parser.add_argument('--inactive', type=int, default=100)
    parser.add_argument('--active', type=int, default=250)
    parser.add_argument('--seed', type=int, default=917031)
    parser.add_argument('--final-statepoint-only', action='store_true')
    args = parser.parse_args()
    config = ReferenceConfig(args.tally_cells_per_zone,args.particles,args.inactive,args.active,args.seed,not args.final_statepoint_only)
    energy = json.loads(args.energy_edges_json.read_text()) if args.energy_edges_json else None
    manifest = export_inputs(args.output,args.case,config,args.cross_sections,energy)
    print(json.dumps(dict(case=args.case,output=str(args.output),transport_executed=False,
                          radial_boundary=manifest['boundary']['boundary_type'],
                          region_layer_bins=len(manifest['region_layer_bins']))))


if __name__ == '__main__':
    main()

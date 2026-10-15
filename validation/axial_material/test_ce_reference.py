"""Static scientific-contract tests; no OpenMC particle transport."""
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import ce_reference as ce


class ReferenceInputs(unittest.TestCase):
    def test_actual_pin_is_white_and_region_order_is_external_first(self):
        evidence = ce.boundary_evidence()
        self.assertEqual(evidence['boundary_type'], 'white')
        self.assertEqual(evidence['albedo'], 1)
        self.assertEqual(ce.REGION_MATERIAL[1], 'coolant')
        self.assertEqual(ce.REGION_MATERIAL[8], 'he_hole')
        self.assertEqual([r for r in ce.REGION_MATERIAL if ce.REGION_MATERIAL[r]=='fuel'], [4,5,6,7])

    def test_density_clones_have_no_A_B_global_contamination(self):
        builder = ce.density_builder()
        a = ce.composition_base(builder, 'A')
        before = builder.material_numbers(a, 750)
        b = ce.composition_base(builder, 'B')
        after_b = builder.material_numbers(b, 750)
        self.assertEqual(builder.material_numbers(a, 750), before)
        self.assertEqual(builder.material_numbers(ce.composition_base(builder, 'A'), 750), before)
        self.assertNotEqual(before['N_Pu39'], after_b['N_Pu39'])
        self.assertEqual(before['N_Na'], after_b['N_Na'])
        self.assertEqual(before['N_He_1'], after_b['N_He_1'])
        for base, values in [(a,before),(b,after_b)]:
            u = values['N_U5']+values['N_U8']
            pu = sum(values[k] for k in ['N_Pu38','N_Pu39','N_Pu40','N_Pu41','N_Pu42','N_Am'])
            self.assertAlmostEqual(pu/u, (base.p_Pu/base.M_Pu_HM)/(base.p_U/base.M_U_HM), places=13)
            self.assertAlmostEqual(values['N_O']/(u+pu),1.98, places=13)
            mass = (u*base.M_U_HM+pu*base.M_Pu_HM+values['N_O']*15.9949)/base.A_AVOGADRO
            coefficient = 1+base._interp(750,base._TABLE_comb)*(750-20)
            self.assertAlmostEqual(mass,11.46*0.955/coefficient**3,places=12)

    def test_ABA_material_and_temperature_assignment(self):
        model, manifest = ce.build_model('ABA')
        cells = model.geometry.get_all_material_cells()
        for record in manifest['region_layer_bins']:
            self.assertEqual(record['composition'], 'B' if record['physical_zone']==2 else 'A')
            role = record['material_role']
            expected = 1023.15 if role in ['fuel','he_hole'] else 748.15 if role=='coolant' else 893.15
            self.assertAlmostEqual(cells[record['cell_id']].fill.temperature, expected)
        self.assertEqual(len(manifest['region_layer_bins']),96)
        self.assertEqual(len(manifest['layer_bins']),12)
        self.assertEqual(len(manifest['plane_bins']),13)

    def test_AAA_uses_only_A_and_symmetry_samples_agree(self):
        model, manifest = ce.build_model('AAA')
        self.assertEqual(set(manifest['materials']), {'A'})
        for radius in [0,0.2,0.35,0.4,0.42,0.43,0.46,0.51]:
            left=model.geometry.find((radius,0,25))[-1].fill
            right=model.geometry.find((-radius,0,125))[-1].fill
            self.assertEqual(left.id,right.id)
        for point in [(0,0,-0.1),(0,0,150.1),(0.7,0,75),(0,0.6,75)]:
            self.assertFalse(model.geometry.find(point))

    def test_exact_physical_volumes_and_fine_bin_mapping(self):
        _, manifest = ce.build_model('ABA',ce.ReferenceConfig(tally_cells_per_zone=8))
        area=ce.region_areas()
        self.assertAlmostEqual(sum(area.values()),3*math.sqrt(3)*ce.SIDE**2/2,places=14)
        self.assertAlmostEqual(sum(area[r] for r in [4,5,6,7]),math.pi*(0.4225**2-0.11**2),places=14)
        for region in range(1,9):
            for coarse in range(1,13):
                records=[r for r in manifest['region_layer_bins'] if r['region']==region and r['production_axial_cell']==coarse]
                self.assertEqual(len(records),2)
                self.assertAlmostEqual(sum(r['volume_cm3'] for r in records),area[region]*12.5,places=13)

    def test_flux_and_fission_are_distinct_scores_and_currents_are_planes(self):
        model, manifest = ce.build_model('AAA',energy_edges_ev=[0,1e5,2e7])
        byname={t.name:t for t in model.tallies}
        self.assertEqual(byname['region_layer_rates'].scores,['flux','nu-fission'])
        self.assertEqual(byname['region_layer_rates'].filters[0].num_bins,96)
        self.assertEqual(byname['layer_rates'].filters[0].num_bins,12)
        self.assertEqual(byname['axial_plane_net_current'].filters[0].num_bins,13)
        partial=byname['axial_plane_directional_current']
        self.assertIsInstance(partial.filters[1],ce.openmc.PolarFilter)
        self.assertEqual(partial.filters[1].num_bins,2)
        self.assertEqual(partial.filters[1].bins.tolist(),[[0,math.pi/2],[math.pi/2,math.pi]])
        self.assertEqual(partial.scores,['current'])
        self.assertEqual(manifest['directional_current_filter']['raw_bin_order'],['positive_z','negative_z'])
        self.assertEqual(manifest['schema'],'AXMAT_CE_INPUT_V2')
        self.assertIn('not region-resolved',manifest['current_scope'])
        self.assertEqual([row['z_cm'] for row in manifest['plane_bins'] if row['role']=='physical_interface'],[50,100])

    def test_export_is_input_only_with_every_active_statepoint(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(ce.openmc,'run',side_effect=AssertionError('transport forbidden')), patch.object(ce.openmc.Model,'run',side_effect=AssertionError('transport forbidden')):
            output=Path(temporary)/'AAA'
            result=ce.export_inputs(output)
            settings=ET.parse(output/'settings.xml').getroot()
            self.assertEqual(int(settings.findtext('particles')),50000)
            self.assertEqual(int(settings.findtext('batches')),350)
            self.assertEqual(int(settings.findtext('inactive')),100)
            entropy_id=settings.findtext('entropy_mesh')
            self.assertIsNotNone(entropy_id)
            entropy=settings.find(f"mesh[@id='{entropy_id}']")
            self.assertEqual(entropy.findtext('dimension'),'4 4 12')
            self.assertEqual(result['source_entropy_mesh']['dimension'],[4,4,12])
            self.assertEqual([int(v) for v in settings.findtext('state_point/batches').split()],list(range(101,351)))
            self.assertFalse(result['transport_executed'])
            self.assertTrue(result['statepoint_every_active_batch'])
            self.assertIsNone(result['cross_sections'])
            self.assertEqual(set(result['input_hashes']),{'geometry.xml','materials.xml','settings.xml','tallies.xml'})
            geometry=ET.parse(output/'geometry.xml').getroot()
            self.assertEqual(sum(s.get('boundary')=='white' for s in geometry.findall('surface')),6)
            self.assertEqual(sum(s.get('boundary')=='vacuum' for s in geometry.findall('surface')),2)
            tally_root=ET.parse(output/'tallies.xml').getroot()
            self.assertEqual(len(tally_root.findall("filter[@type='polar']")),1)
            self.assertFalse(tally_root.findall("filter[@type='musurface']"))
            self.assertEqual({t.get('name'):t.findtext('scores') for t in tally_root.findall('tally')},
                             {'region_layer_rates':'flux nu-fission','layer_rates':'flux nu-fission',
                              'axial_plane_net_current':'current','axial_plane_directional_current':'current'})
            with self.assertRaises(FileExistsError):ce.export_inputs(output)

    def test_bad_or_incomparable_input_is_refused(self):
        for config in [ce.ReferenceConfig(tally_cells_per_zone=5),ce.ReferenceConfig(particles=0),ce.ReferenceConfig(inactive=-1)]:
            with self.assertRaises(ValueError):ce.build_model('AAA',config)
        with self.assertRaises(ValueError):ce.build_model('BBB')
        with self.assertRaises(ValueError):ce.build_model('AAA',energy_edges_ev=[0,1,1])


if __name__=='__main__':unittest.main()

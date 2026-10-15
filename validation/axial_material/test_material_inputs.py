"""Bounded input-contract tests; no NJOY, Dragon or transport invocation."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import material_inputs as m


class MaterialInputsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = m.load_sources()
        cls.decks = m.build_decks(source_text=cls.text)

    def test_density_formula_provenance_and_parameterized_composition(self):
        procedure = self.decks['A/AxMatTone.c2m']
        self.assertEqual(procedure, self.decks['B/AxMatTone.c2m'])
        self.assertIn(':: >>p_Pu<< >>p_U<< >>T_comb<< >>T_clad<< >>T_Na<< ;', procedure)
        original = self.text['current_snapshot']
        block = original[original.index('REAL p_Pu38'):original.index('ECHO "SpotD4Snap: T_comb=')]
        self.assertIn(block, procedure)
        self.assertIn('0.2100 0.7900 750.0 620.0 475.0', self.decks['A/material.x2m'])
        self.assertIn('0.2436 0.7564 750.0 620.0 475.0', self.decks['B/material.x2m'])
        for forbidden in ('4.1347E-05', '2.0632E-02', '2.8916E-02', '5.2271E-02'):
            self.assertNotIn(forbidden, procedure)

    def test_mo_only_library_routing_and_fuel_ring_identity(self):
        library = None
        route = {}
        procedure = self.decks['A/AxMatTone.c2m']
        for line in procedure.splitlines():
            if 'MIXS LIB:' in line:
                library = line.split("'")[1]
            elif " = '" in line and '<<N_' in line:
                nuclide = line.split("'")[1]
                route[nuclide] = library
        self.assertEqual({n for n, lib in route.items() if lib == 'DLIB8R1_370'},
                         {'Mo92', 'Mo94', 'Mo95', 'Mo96', 'Mo97', 'Mo98', 'Mo100'})
        self.assertTrue(all(lib == 'DLIB_ACTUAL' for n, lib in route.items() if not n.startswith('Mo')))
        for mixture in (6, 5, 4):
            self.assertIn(f'MIX {mixture} COMB 7 1.0', procedure)
        self.assertIn('MIX 8 (*He central hole*)', procedure)
        self.assertIn('MIX 3 (*He pellet-clad gap*)', procedure)
        self.assertIn('NMIX 8 CTRA APOL ANIS 3', procedure)
        self.assertEqual(len(route), 34)  # D4 private library has C12, unused by this pin.

    def test_material_only_stops_before_transport(self):
        proc = self.decks['A/AxMatTone.c2m']
        self.assertIn('MXIT 20 EPS 1.0E-5 TRAN PIJ', proc)
        self.assertIn('MERGMIX', proc)
        self.assertNotIn('FLU:', proc)
        self.assertNotIn('ASM:', proc)
        for state in ('A', 'B'):
            deck = self.decks[f'{state}/material.x2m']
            self.assertIn("FILE './material.xsm'", deck)
            self.assertIn('MICRO_OUT := MICROLIB2', deck)
            self.assertIn(f'AXMAT-MATERIAL-{state}-COMPLETE', deck)
            self.assertNotIn('FLU:', deck)

    def test_fresh_snapshot_uses_qualified_material_not_an_old_flux(self):
        for state in ('A', 'B'):
            deck = self.decks[f'{state}/snapshot.x2m']
            self.assertIn('MICROLIB2 := MAT_IN', deck)
            self.assertNotIn('TONE:', deck)
            self.assertNotIn('RECOVER:', deck)
            self.assertNotIn('FLUX := FLU: FLUX', deck)
            self.assertIn('TYPE K EXTE', deck)
            self.assertIn('SNAP := BACKUP: TRACK :: LIST 1 ITEM 1', deck)
            for obj in ('MICROLIB2', 'SYSTEM', 'FLUX'):
                self.assertIn(f'SNAP := BACKUP: SNAP {obj} :: ITEM 1', deck)
            self.assertIn(f"FILE './snapshot_{state}.xsm'", deck)
            self.assertIn("FILE './radial_track.bin'", deck)
            self.assertIn('IF nfis 32 <> THEN', deck)

    def test_undeclared_compositions_temperatures_and_invalid_controls_refused(self):
        for config in (replace(m.MaterialConfig(), pu_B=0.25),
                       replace(m.MaterialConfig(), fuel_C=650),
                       replace(m.MaterialConfig(), snapshot_eps=float('nan')),
                       replace(m.MaterialConfig(), maxout=0),
                       replace(m.MaterialConfig(), track_angles=True)):
            with self.subTest(config=config), self.assertRaises(ValueError):
                m.build_decks(config, self.text)

    def test_source_anchor_drift_refused(self):
        for altered in (self.text['current_snapshot'].replace('273.15 +', '273.16 +'),
                        self.text['current_snapshot'].replace("Mo92_AIM1 = 'Mo92'", "Mo92_AIM1 = 'Mo94'")):
            with self.assertRaises(ValueError):
                m.material_procedure(altered)

    def test_preparation_is_fresh_and_content_sealed(self):
        # Tiny libraries exercise staging metadata only; no physics engine exists here.
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            candidate, production = folder/'candidate', folder/'original'
            candidate.write_bytes(b'synthetic candidate')
            production.write_bytes(b'synthetic original')
            output = folder/'inputs'
            with patch.object(m, 'CANDIDATE_SHA256', m.digest(candidate)), \
                 patch.object(m, 'PRODUCTION_SHA256', m.digest(production)):
                manifest = m.write_inputs(output, candidate=candidate, production=production)
                with self.assertRaises(FileExistsError):
                    m.write_inputs(output, candidate=candidate, production=production)
            self.assertEqual(manifest['classification'], 'PREPARED_INPUTS_ONLY_NO_NATIVE_EXECUTION')
            self.assertEqual(manifest['fission_components_expected'], 32)
            for state in ('A', 'B'):
                self.assertFalse((output/f'{state}/material.xsm').exists())
                self.assertFalse((output/f'{state}/snapshot_{state}.xsm').exists())
                self.assertFalse((output/f'{state}/DLIB_ACTUAL').exists())
            for name, digest in manifest['generated_sha256'].items():
                self.assertEqual(m.digest(output/name), digest)

    def test_unreviewed_library_refused_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            library = folder/'wrong-library'
            library.write_bytes(b'unreviewed data')
            with self.assertRaises(ValueError):
                m.write_inputs(folder/'output', candidate=library, production=library)
            self.assertFalse((folder/'output').exists())
            with patch.object(m, 'CANDIDATE_SHA256', m.digest(library)), self.assertRaises(ValueError):
                m.write_inputs(folder/'output', candidate=library, production=library)
            self.assertFalse((folder/'output').exists())


if __name__ == '__main__':
    unittest.main()

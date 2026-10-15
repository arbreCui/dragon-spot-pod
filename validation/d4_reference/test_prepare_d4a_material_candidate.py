"""Short synthetic/static checks; no engine execution or scientific run."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_d4a_material_candidate import candidate_procedure, material_deck, tree_digest


class PreparationTest(unittest.TestCase):
    def test_original_physics_and_mo_route(self):
        original = (Path(__file__).resolve().parents[2]/'data/SpotD4Tone.c2m').read_text()
        candidate, route = candidate_procedure(original)
        self.assertEqual(len(route), 59)
        self.assertEqual(sum(r['library'] == 'DLIB8R1_370' for r in route), 14)
        self.assertIn('EDIT 1 MXIT 20 EPS 1.0E-5 TRAN PIJ', candidate)
        self.assertIn('CTRA APOL', candidate)
        with self.assertRaises(ValueError):
            candidate_procedure(original.replace("Mo100_AIM1 = 'Mo100'", "Mo100_AIM1 = 'U238'"))

    def test_missing_anchor_refused(self):
        with self.assertRaises(ValueError):
            candidate_procedure('STRING Library := "OTHER" ;')

    def test_typed_subtree_image(self):
        a = {('X',): (0, -1), ('X', 'A'): (2, (1.0, -0.0)), ('X', 'B'): (1, (2, 3))}
        self.assertEqual(tree_digest(a), tree_digest(dict(reversed(list(a.items())))))
        self.assertNotEqual(tree_digest(a), tree_digest({**a, ('X', 'A'): (2, (1.0, 0.0))}))
        self.assertNotEqual(tree_digest(a), tree_digest({**a, ('X', 'B'): (2, (2.0, 3.0))}))
        with self.assertRaises(ValueError):
            tree_digest({('X',): (2, (float('nan'),))})

    def test_material_export_scope(self):
        for temp in (650, 750, 850):
            deck = material_deck(temp)
            self.assertIn(f'REAL T_comb := {temp}.0 ;', deck)
            self.assertIn('REAL T_clad := 620.0 ;', deck)
            self.assertIn('REAL T_Na := 475.0 ;', deck)
            self.assertIn('MICRO := MICROLIB2 ;', deck)
            self.assertNotIn('FLU:', deck)
            self.assertNotIn('ASM:', deck)
        with self.assertRaises(ValueError):
            material_deck(900)


if __name__ == '__main__':
    unittest.main()

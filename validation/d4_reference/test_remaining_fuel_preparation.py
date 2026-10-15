"""Short saved-state/graph tests: no native engines are allowed."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

import prepare_remaining_fuel_temperatures as p


class FuelPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with patch.object(p.c.sp,'Popen',side_effect=AssertionError('native execution forbidden')):
            cls.candidate,cls.pins,cls.retained = p.load_inputs()
        cls.native,cls.cached = p.graph(p.WORK)

    def test_fixed_partition_and_lineage(self):
        p.validate_graph(p.WORK,self.native,self.cached,self.pins)
        self.assertEqual(len(self.retained),16)
        self.assertEqual(sum(s['control'] for s in self.native),35)
        self.assertEqual(sum(not s['control'] for s in self.native),48)
        self.assertEqual(sum(s['kind']=='pendf' for s in self.native),23)
        self.assertEqual(sum(s['kind']=='groupr' for s in self.native),30)
        self.assertEqual(sum(s['kind']=='dragr' for s in self.native),30)
        self.assertTrue(all(s['label'].startswith('Am241/control/') for s in self.cached))
        self.assertFalse(any(s['label'].startswith('Am241/control/') for s in self.native))

    def test_high_pass_imports_its_own_new_low(self):
        for s in self.native:
            if s['label'].endswith('high/dragr'):
                root = Path(s['output']).parents[2]
                self.assertEqual(Path(s['inputs']['tape29']),root/'low/dragr/tape30')

    def test_missing_stage_refused(self):
        with self.assertRaisesRegex(ValueError,'stage graph changed'):
            p.validate_graph(p.WORK,self.native[:-1],self.cached,self.pins)

    def test_wrong_parent_refused(self):
        changed = copy.deepcopy(self.native)
        high = next(s for s in changed if s['label'].endswith('high/dragr'))
        high['inputs']['tape29'] = p.rows()[0]['original_library']
        with self.assertRaisesRegex(ValueError,'stage graph changed'):
            p.validate_graph(p.WORK,changed,self.cached,self.pins)

    def test_missing_cache_identity_refused(self):
        pins = dict(self.pins)
        del pins[str(Path(self.cached[0]['source_directory'])/'tape30')]
        with self.assertRaisesRegex(ValueError,'unsealed reused stage'):
            p.validate_graph(p.WORK,self.native,self.cached,pins)

    def test_conflicting_pin_refused(self):
        with self.assertRaisesRegex(ValueError,'conflicting input identity'):
            p.merge({'sample':'a'},{'sample':'b'})


if __name__ == '__main__':
    unittest.main()

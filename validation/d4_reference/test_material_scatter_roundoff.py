import unittest
import numpy as np
from check_material_scatter_roundoff import diagnose_column, rounding_interval


class RoundingIntervals(unittest.TestCase):
    def test_exact_conservation(self):
        r = diagnose_column(3, [1, 2, 0])
        self.assertEqual(r['exact_gap'], 0)
        self.assertTrue(r['one_final_rounding_intervals_overlap'])

    def test_real_mismatch_is_not_excused(self):
        self.assertFalse(diagnose_column(3, [1, 1])['one_final_rounding_intervals_overlap'])

    def test_sub_ulp_difference_can_be_compatible(self):
        r = diagnose_column(1, [1, 2**-25])
        self.assertNotEqual(r['exact_gap'], 0)
        self.assertTrue(r['one_final_rounding_intervals_overlap'])

    def test_order_match_is_not_assumed(self):
        r = diagnose_column(1, [1, 2**-24, 2**-24])
        self.assertNotEqual(r['ascending_binary32_sum'], r['descending_binary32_sum'])

    def test_asymmetric_spacing_at_power_of_two(self):
        lo, hi = rounding_interval(1)
        self.assertEqual(1-lo, 2**-25)
        self.assertEqual(hi-1, 2**-24)

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):
            diagnose_column(np.nan, [1])


if __name__ == '__main__':
    unittest.main()

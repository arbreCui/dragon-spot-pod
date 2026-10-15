"""Sparse orientation, signed corrections and fail-closed tail checks."""
import unittest
import numpy as np
from audit_fe56_candidate_scope import expand

class MatrixTests(unittest.TestCase):
    def test_primary_group_is_column(self):
        a,tail=expand([1,2,1],[1,3,3],[1.,2.,3.,4.],3)
        np.testing.assert_array_equal(a,[[1,0,0],[0,3,2],[0,0,4]])
        np.testing.assert_array_equal(a.sum(axis=0),[1,3,6])
        self.assertEqual(tail,0)

    def test_only_proved_outside_range_tail_is_zero(self):
        a,tail=expand([1,2,1],[1,3,3],[1.,2.,3.],3,(1,2))
        self.assertEqual(tail,1)
        self.assertEqual(a[2,2],0)

    def test_finite_signed_correction_is_preserved(self):
        a,_=expand([1,1],[1,2],[-1.,2.],2,(1,2))
        self.assertEqual(a[0,0],-1.)

    def test_infinite_truncation_refused(self):
        with self.assertRaises(AssertionError):expand([1,1],[1,2],[1.],2)

    def test_self_shielded_truncation_refused(self):
        with self.assertRaises(AssertionError):expand([1,1],[1,2],[1.],2,(1,2))

    def test_nonfinite_refused(self):
        with self.assertRaises(AssertionError):expand([1],[1],[float('nan')],1)

    def test_index_outside_geometry_refused(self):
        with self.assertRaises(AssertionError):expand([1],[2],[1.],1)

    def test_extra_payload_refused(self):
        with self.assertRaises(AssertionError):expand([1],[1],[1.,2.],1)

if __name__=='__main__':unittest.main()

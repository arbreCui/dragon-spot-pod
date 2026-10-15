"""Conservation, moment splitting, and positive-response generator controls."""
import unittest
import numpy as np
from scipy.linalg import expm
from audit_native_source_current import (angular_moments,scalar_generator_audit,
                                         conservative_counterexample,MU)


class SourceCurrentTests(unittest.TestCase):
    def test_angular_moments_and_internal_current_telescope(self):
        faces=np.arange(1,13,dtype=float).reshape(1,2,3,2)/9
        h=np.array([.3,.7,.5]);phi,j,div,incoming=angular_moments(faces,h)
        expected_phi=np.zeros((1,3,2));expected_j=np.zeros_like(expected_phi)
        for z in range(3):
            left=faces[0,0,z-1] if z>0 else np.zeros(2)
            right=faces[0,1,z+1] if z<2 else np.zeros(2)
            plus=(left+faces[0,0,z])/2;minus=(right+faces[0,1,z])/2
            expected_phi[0,z]=plus+minus;expected_j[0,z]=MU*(plus-minus)
        np.testing.assert_allclose(phi,expected_phi,atol=1e-15)
        np.testing.assert_allclose(j,expected_j,atol=1e-15)
        np.testing.assert_allclose(np.sum(div*h[None,:,None],axis=1),MU*(faces[:,0,-1]+faces[:,1,0]),atol=1e-15)

    def test_directionwise_lift_changes_odd_channel_but_preserves_even_sum(self):
        c=np.array([[.2,-.2],[-.1,.1]]);plus=np.array([2.,1.]);minus=np.array([.5,1.5])
        phi=plus+minus;j=MU*(plus-minus)
        np.testing.assert_allclose(c@plus,c@phi/2+c@j/(2*MU),atol=1e-15)
        np.testing.assert_allclose(c@minus,c@phi/2-c@j/(2*MU),atol=1e-15)
        np.testing.assert_allclose(c@(plus+minus),c@phi,atol=1e-15)
        self.assertGreater(np.linalg.norm(c@j),.1)

    def test_positive_steady_response_and_exact_balance_do_not_imply_generator_positivity(self):
        toy=conservative_counterexample();r=np.array(toy['steady_response']);h=np.array(toy['inverse'])
        self.assertTrue(np.all(r>0));self.assertTrue(np.all(np.array(toy['positive_total'])>0))
        np.testing.assert_allclose(toy['column_balance_defect'],0,atol=1e-15)
        np.testing.assert_allclose(toy['constant_radial_action'],0,atol=1e-15)
        self.assertGreater(h[0,2],0)
        self.assertLess(expm(-1e-3*h)[0,2],0)
        self.assertLess(np.linalg.solve(np.eye(3)+1e-3*h,np.eye(3))[0,2],0)

    def test_metzler_control_retains_positive_propagators(self):
        h=np.array([[2.,-1.],[-.5,1.5]]);r=np.linalg.inv(h)
        rows,exact,implicit=scalar_generator_audit(h[None],r[None],np.array([1.,2.]),
                                                  np.array([[1.,1.]]),[1e-6,1e-3,.1,1.])
        self.assertEqual(rows[0]['positive_offdiagonal_count'],0)
        self.assertNotIn('certified_witness',rows[0])
        self.assertTrue(np.all(exact>=0));self.assertTrue(np.all(implicit>=0))

    def test_finite_bounds_dominate_actual_negative_witness(self):
        witness=conservative_counterexample()['audit']['certified_witness']
        self.assertLess(witness['exponential_upper_bound'],0)
        self.assertLess(witness['implicit_upper_bound'],0)
        self.assertLessEqual(witness['exponential_entry'],witness['exponential_upper_bound']+1e-16)
        self.assertLessEqual(witness['implicit_entry'],witness['implicit_upper_bound']+1e-16)

    def test_positive_steady_source_can_be_tested_column_by_column(self):
        toy=conservative_counterexample();r=np.array(toy['steady_response']);h=np.array(toy['inverse'])
        for j in range(3):
            source=np.eye(3)[:,j];flux=r@source
            self.assertTrue(np.all(flux>0));np.testing.assert_allclose(h@flux,source,atol=3e-16)

    def test_signed_source_cone_is_not_the_positive_flux_orthant(self):
        h=np.array(conservative_counterexample()['inverse'])
        phi=np.array([1e-4,1.,1e-4])
        self.assertTrue(np.all(phi>0));self.assertTrue(np.any(h@phi<0))

    def test_small_step_derivative_has_opposite_offdiagonal_sign(self):
        h=np.array(conservative_counterexample()['inverse']);eps=1e-7
        derivative=(expm(-eps*h)-np.eye(3))/eps
        np.testing.assert_allclose(derivative,-h,rtol=3e-7,atol=3e-7)


if __name__=='__main__':unittest.main()

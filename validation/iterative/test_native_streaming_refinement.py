"""Independent controls for batching, two-source application and refinement norms."""
import unittest
import numpy as np
from native_axial_streaming import green_sweep,scalar_integrals,polynomial_coefficients,dense_coefficients,shift_matrix
from native_axial_streaming_refinement import batched_green,heldout_boundary,mesh_difference,Budget
from qualify_native_axial_streaming import run_boundary
from qualify_native_signed_axial import angular_measures
from qualify_native_directional import relative


def fixture():
    d=dict(nr=8,nb=6,nmu=2,nmax=5,track=np.array([0,0,1,1]),
           polar=np.array([0,1,0,1]),length=np.array([4,4,5,5]),
           region=np.array([[-1,1,2,-2,0],[-1,1,2,-2,0],[-2,3,1,4,-3],[-2,3,1,4,-3]]),
           zmu=np.array([1.25,2.]),weight=np.array([.3,.8,.2,.7]),weights=np.linspace(.8,1.5,14))
    d['h']=d['zmu'][d['polar'],None]*np.array([[0,.4,.7,0,0],[0,.4,.7,0,0],[0,.2,.3,.6,0],[0,.2,.3,.6,0]])
    a=dict(total=np.linspace(.7,1.2,8),b=np.zeros((4,5)),self_d=np.zeros((4,5)))
    for line,seg in zip(*np.where(d['region']>0)):
        b,own=scalar_integrals(d['h'][line,seg],a['total'][d['region'][line,seg]-1])
        a['b'][line,seg]=b*(1+1e-7);a['self_d'][line,seg]=own*(1-2e-7)
    return d,a


class RefinementTests(unittest.TestCase):
    def test_batched_green_equals_unbatched_including_short_tracks(self):
        d,a=fixture()
        for n in [1,3,8]:
            for kind in ['exact','native']:
                expected,old_stats=green_sweep(d,a,n,20.,kind)
                for size in [1,3,8]:
                    actual,stats,defects=batched_green(d,a,n,20.,kind,size)
                    np.testing.assert_allclose(actual,expected,rtol=5e-15,atol=2e-17)
                    self.assertEqual(stats,old_stats)
                    self.assertEqual(defects['segment_polar_samples'],10)

    def test_two_source_application_matches_all_source_solver(self):
        d,a=fixture()
        for n in [1,3]:
            for kind in ['exact','native']:
                green,_,_=batched_green(d,a,n,20.,kind,3)
                for b in ['vacuum','white']:
                    row,fields=heldout_boundary(d,a,green,n,20.,b)
                    old,expected=run_boundary(d,a,green,n,20.,b)
                    for key in ['phi','jz','half_flux','half_outgoing','incoming','face_current','face_second_moment','volume_source']:
                        np.testing.assert_allclose(fields[key],expected[key][...,-2:],rtol=5e-13,atol=1e-15,err_msg=key)
                    # Raw balances are cancellations; compare their roundoff
                    # against incoming/source scale, not the near-zero defect.
                    vw,sw=angular_measures(d)
                    scale=max(1.,float(np.max(20/n*(np.einsum('ric,r->ic',fields['volume_source'],2*vw.sum(axis=0))+
                                                        np.einsum('sic,s->ic',fields['incoming'],2*sw.sum(axis=0))))))
                    for key in ['even_cell_defect','odd_cell_defect']:
                        np.testing.assert_allclose(fields[key],expected[key][...,-2:],rtol=0,atol=64*np.finfo(float).eps*scale)
                    for key in ['even_cell_relative','odd_cell_relative','even_global_relative','odd_global_relative']:
                        np.testing.assert_allclose(fields[key],expected[key][...,-2:],rtol=0,atol=64*np.finfo(float).eps)
                    np.testing.assert_allclose(fields['axial_escape'],old['heldout_axial_escape'],rtol=5e-15)

    def test_64_cell_primitive_against_dense_block_and_both_signs(self):
        for sigma,length,mu in [(0.,.01,.18),(.0125,2.4,.96),(4.,.8,.53)]:
            coeff=polynomial_coefficients(length,sigma,mu*64/20,64)
            for sign in [1,-1]:
                dense=dense_coefficients(length,sigma,mu,[20/64]*64,sign)
                for x,y in zip(coeff,dense):
                    np.testing.assert_allclose(shift_matrix(x,sign),y,rtol=3e-12,atol=3e-15)
                    self.assertGreaterEqual(x.min(),0.)

    def test_restriction_averages_pairs_with_volume_weight(self):
        fine=dict(phi=np.array([[[1.,2.],[3.,4.],[5.,6.],[7.,8.]]]),axial_escape=np.array([2.,4.]))
        coarse=dict(phi=np.array([[[2.,3.],[6.,7.]]]),axial_escape=np.array([2.2,3.6]))
        flux,escape=mesh_difference(coarse,fine,np.array([3.]),20.)
        np.testing.assert_array_equal(flux,0.)
        np.testing.assert_allclose(escape,[.1,.1])

    def test_symmetry_preserves_axial_sign_mirror(self):
        d,a=fixture();green,_,_=batched_green(d,a,8,20.,'native',2)
        _,f=heldout_boundary(d,a,green,8,20.,'white')
        np.testing.assert_allclose(f['half_flux'][0],f['half_flux'][1,:, :,::-1],rtol=5e-14,atol=1e-16)
        # The declared field norm remains meaningful at an almost-zero Jz.
        self.assertLess(relative(f['jz'],-f['jz'][:,::-1]),5e-14)

    def test_invalid_batch_and_budget_fail_closed(self):
        d,a=fixture()
        with self.assertRaises(ValueError):batched_green(d,a,1,20.,'exact',0)
        with self.assertRaises(RuntimeError):Budget(0,1).check()


if __name__=='__main__':unittest.main()

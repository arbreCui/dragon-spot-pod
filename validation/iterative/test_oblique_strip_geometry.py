"""Independent geometry, elementary solution and source-basis regression tests."""
import unittest
import numpy as np
from oblique_strip_geometry import geometry,sweep,relative
from oblique_strip_reference import one_d,homogeneous,matched,integrate
from qualify_oblique_strip_geometry import geometry_metrics,reflection_error


class GeometryTests(unittest.TestCase):
    def test_all_cell_and_face_measures(self):
        for mu in [-1/3**.5,0,1/3**.5]:
            for o in [-1,1]:
                g=geometry(3,1,2,8,mu,o,2)
                self.assertLess(geometry_metrics(g)[0],5e-14)
                self.assertTrue(np.all(g['weight']>0));self.assertTrue(np.all(g['length']>0))

    def test_constant_with_void_material(self):
        for mu in [-.7,0,.7]:
            g=geometry(3,1,2,4,mu,-1,4);f=sweep(g,np.array([0.,2.]),one_d);u=int(f['units'])
            np.testing.assert_allclose(f['integral'][:,u],g['area'],rtol=1e-14)
            self.assertLess(relative(f['cell_defect'],f['cell_scale']).max(),1e-13)

    def test_void_analytic_triangle(self):
        # On the unit square with mu=1, psi=min(s,z). Integral=1/3;
        # each outgoing side integrates to 1/2 independently of ray geometry.
        v,face=homogeneous(1,1,1,1,1,1,0)
        self.assertAlmostEqual(v[0],1/3,14)
        np.testing.assert_allclose(face,[[0,.5,0,.5]],atol=1e-15)
        g=geometry(1,1,1,1,1,1,2);f=sweep(g,np.array([0.]),one_d);u=int(f['units'])
        np.testing.assert_allclose(f['integral'][:,u+1],v,rtol=1e-14)
        np.testing.assert_allclose(f['face_out'][...,u+1],face,atol=1e-15)

    def test_absorbing_square_independent_integrals(self):
        # Integral of the tail distribution of min(s,z): int exp(-sigma*t)*(1-t)^2 dt.
        sigma=2.;v,face=homogeneous(1,1,1,1,1,1,sigma)
        expected=integrate(lambda t:np.exp(-sigma*t)*(1-t)**2,0,1)
        self.assertAlmostEqual(v[0],expected,14)
        g=geometry(1,1,1,1,1,1,16);f=sweep(g,np.array([sigma]),one_d);u=int(f['units'])
        np.testing.assert_allclose(f['integral'][:,u+1],v,rtol=1e-13)
        np.testing.assert_allclose(f['face_out'][...,u+1],face,atol=1e-14)

    def test_zero_mu_literal_1d_void(self):
        g=geometry(3,2,2,4,0,1,2);f=sweep(g,np.array([0.,0.]),one_d);u=int(f['units'])
        expected=np.repeat([.75,2.25],4)
        np.testing.assert_allclose(f['integral'][:,u+1]/g['area'],expected,rtol=1e-14)
        self.assertEqual(np.max(f['face_out'][:,2:]),0)

    def test_positive_full_cone_shared_faces(self):
        g=geometry(3,1,2,8,-.7,-1,8);f=sweep(g,np.array([.2,2.]),one_d)
        self.assertGreaterEqual(f['minimum_piece_angle'].min(),0)
        self.assertGreaterEqual(f['minimum_piece_integral'].min(),0)
        self.assertEqual(abs(f['shared_defect']).max(),0)
        self.assertLess(relative(f['global_defect'],f['global_scale']).max(),1e-13)

    def test_both_reflections(self):
        p=np.array([.2,2.]);g=geometry(3,1,2,4,-.7,-1,8);a=sweep(g,p,one_d)
        b=sweep(geometry(3,1,2,4,.7,-1,8),p,one_d)
        c=sweep(geometry(3,1,2,4,-.7,1,8),p[::-1],one_d)
        self.assertLess(reflection_error(a,b,2,4,-.7,'z'),1e-13)
        self.assertLess(reflection_error(a,c,2,4,-.7,'x'),1e-13)

    def test_matched_top_and_bottom(self):
        for mu in [-.7,.7]:
            for o in [-1,1]:
                p=np.array([0.,2.]);g=geometry(3,1,2,4,mu,o,16);f=sweep(g,p,one_d);u=int(f['units'])
                v,face=matched(3,1,2,4,mu,o,p)
                np.testing.assert_allclose(f['integral'][:,u+2],v,rtol=1e-13)
                np.testing.assert_allclose(f['face_out'][...,u+2],face,rtol=1e-13,atol=1e-15)
                self.assertLess(float(f['matched_point_relative']),1e-13)


if __name__=='__main__':unittest.main()

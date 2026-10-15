"""Independent analytic, transport and finite-volume checks for the S2 slab."""
import unittest
import numpy as np
from scipy.linalg import expm
from native_axial_streaming import upwind
from analytic_axial_slab import (analytic_points,analytic_cell_averages,analytic_checks,
                                discrete_slab,errors_against_reference,adjacent_errors)


class SlabTests(unittest.TestCase):
    mu=1/np.sqrt(3);height=20.

    def test_void_point_and_cell_solution(self):
        z=np.array([0.,3.,11.,20.]);phi,j=analytic_points(z,0.,0.,20.,self.mu)
        np.testing.assert_allclose(phi+j/self.mu,z/self.mu,atol=5e-15)
        np.testing.assert_allclose(phi-j/self.mu,(20-z)/self.mu,atol=5e-15)
        edges=np.array([0.,1.,7.,20.]);p,c,a=analytic_cell_averages(edges,0.,0.,20.,self.mu)
        mid=(edges[:-1]+edges[1:])/2
        np.testing.assert_allclose(a,np.array([mid,20-mid])/self.mu,rtol=3e-15)

    def test_pure_absorption_independent_directional_exponentials(self):
        z=np.linspace(0,20,17)
        for total in [.02,.2,2.]:
            p,j=analytic_points(z,total,0.,20.,self.mu)
            expected=-np.expm1(-total*np.array([z,20-z])/self.mu)/total
            np.testing.assert_allclose(np.array([p+j/self.mu,p-j/self.mu]),expected,rtol=2e-14,atol=6e-15)

    def test_zero_absorption_polynomial_cell_integral(self):
        edges=np.array([0.,.2,7.,12.,20.]);left,right=edges[:-1],edges[1:]
        p,j,_=analytic_cell_averages(edges,2.,2.,20.,self.mu)
        primitive=lambda z:20*z/(2*self.mu)+2/(2*self.mu**2)*(10*z*z-z**3/3)
        expected=(primitive(right)-primitive(left))/(right-left)
        np.testing.assert_allclose(p,expected,rtol=3e-15)

    def test_nonuniform_analytic_cell_averages_against_quadrature(self):
        edges=np.array([0.,.001,.08,.2,1.,7.,12.,19.99,20.]);mid=(edges[:-1]+edges[1:])/2;h=np.diff(edges)
        x,w=np.polynomial.legendre.leggauss(64)
        for total,scatter in [(.02,.0198),(.2,.18),(2.,0.)]:
            p,j,_=analytic_cell_averages(edges,total,scatter,20.,self.mu)
            q,r=analytic_points(mid[:,None]+h[:,None]*x/2,total,scatter,20.,self.mu)
            np.testing.assert_allclose(p,q@w/2,rtol=5e-14,atol=2e-14)
            np.testing.assert_allclose(j,r@w/2,rtol=5e-14,atol=2e-14)

    def test_transfer_matrix_independent_boundary_solution(self):
        for total,scatter in [(.02,0.),(.2,.18),(.2,.2)]:
            u=(total-scatter/2)/self.mu;v=scatter/(2*self.mu)
            generator=np.array([[-u,v,1/self.mu],[-v,u,-1/self.mu],[0.,0.,0.]])
            end=expm(20*generator);initial=np.array([0.,-end[1,2]/end[1,1],1.])
            for z in [0.,.4,7.,13.,20.]:
                expected=(expm(z*generator)@initial)[:2]
                p,j=analytic_points(z,total,scatter,20.,self.mu)
                np.testing.assert_allclose([p+j/self.mu,p-j/self.mu],expected,rtol=5e-12,atol=3e-13)

    def test_pure_absorption_discrete_sweep_recurrence(self):
        for total in [0.,.02,2.]:
            _,f=discrete_slab(total,0.,20.,self.mu,1.,17)
            expected=[];incoming=0.;rate=self.mu/(20/17)
            for _ in range(17):incoming=(1+rate*incoming)/(total+rate);expected.append(incoming)
            np.testing.assert_allclose(f['angular'][0],expected,rtol=4e-15)
            np.testing.assert_allclose(f['angular'][1],expected[::-1],rtol=4e-15)

    def test_void_escape_is_exact_but_scalar_error_is_one_over_n(self):
        for n in [8,32,256]:
            row,f=discrete_slab(0.,0.,20.,self.mu,1.,n)
            _,ref=analytic_checks(0.,0.,20.,self.mu,1.,n);f.update(ref)
            error=errors_against_reference(f)
            np.testing.assert_allclose(row['total_escape'],20.,rtol=3e-14)
            np.testing.assert_allclose(error['scalar_true_relative'],1/n,rtol=3e-12)
            self.assertGreater(row['minimum_angular'],0.)

    def test_strong_scattering_conserves_and_preserves_mirror_sign(self):
        row,f=discrete_slab(2.,2.,20.,self.mu,1.,64)
        self.assertLess(row['matrix_residual_relative'],5e-12)
        self.assertLess(row['raw_global_balance_relative'],1e-10)
        self.assertGreater(f['angular'].min(),0.)
        np.testing.assert_allclose(f['angular'][0],f['angular'][1,::-1],rtol=2e-13)
        np.testing.assert_allclose(f['face_current'],-f['face_current'][::-1],rtol=2e-13,atol=2e-13)

    def test_near_zero_absorption_uses_continuous_positive_limit(self):
        edges=np.linspace(0,20,257)
        a=analytic_cell_averages(edges,.2,.2*(1-1e-12),20.,self.mu)
        b=analytic_cell_averages(edges,.2,.2,20.,self.mu)
        for x,y in zip(a,b):np.testing.assert_allclose(x,y,rtol=2e-10,atol=1e-12)

    def test_restriction_and_invalid_parameters(self):
        coarse=dict(phi=np.array([2.,6.]),angular=np.array([[1.,3.],[3.,9.]]),escape=np.array([2.,2.]),edges=np.array([0.,10.,20.]))
        fine=dict(phi=np.array([1.,3.,5.,7.]),angular=np.array([[.5,1.5,2.5,3.5],[1.5,4.5,7.5,10.5]]),escape=np.array([2.,2.]),edges=np.linspace(0,20,5))
        result=adjacent_errors(coarse,fine)
        self.assertEqual(result['scalar_adjacent_relative'],0.)
        self.assertEqual(result['angular_adjacent_relative'],0.)
        with self.assertRaises(ValueError):analytic_points(1.,.2,.3,20.,self.mu)
        with self.assertRaises(ValueError):analytic_cell_averages([1.,0.],.2,0.,20.,self.mu)

    def test_exact_interior_moment_identity_exposes_upwind_diffusion(self):
        n=9;h=20/n;z=(np.arange(n)+.5)*h;total=.7;scatter=.63
        phi=2.+np.sin(z/9);j=.1*np.cos(z/7);angular=np.array([phi+j/self.mu,phi-j/self.mu])
        plus=self.mu*upwind([h]*n,1)@angular[0]+total*angular[0]-scatter*phi-1
        minus=self.mu*upwind([h]*n,-1)@angular[1]+total*angular[1]-scatter*phi-1
        centered=lambda x:(x[2:]-x[:-2])/(2*h)
        laplacian=lambda x:(x[2:]-2*x[1:-1]+x[:-2])/h**2
        even=centered(j)-self.mu*h/2*laplacian(phi)+(total-scatter)*phi[1:-1]-1
        odd=self.mu**2*centered(phi)-self.mu*h/2*laplacian(j)+total*j[1:-1]
        np.testing.assert_allclose(even,(plus[1:-1]+minus[1:-1])/2,rtol=0,atol=5e-16)
        np.testing.assert_allclose(odd,self.mu*(plus[1:-1]-minus[1:-1])/2,rtol=0,atol=3e-16)


if __name__=='__main__':unittest.main()

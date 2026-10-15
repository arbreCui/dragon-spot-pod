"""Analytical and independent ODE controls for retained-state axial streaming."""
import unittest
import numpy as np
from scipy.integrate import solve_ivp
from native_axial_streaming import (upwind,scalar_integrals,polynomial_coefficients,
                                    dense_coefficients,shift_matrix,green_sweep,expand_green)


class StreamingTests(unittest.TestCase):
    def test_scalar_exponential(self):
        l,s=.7,.9;b0=-np.expm1(-l*s)/s;d0=(l-b0)/s
        t,b,d=polynomial_coefficients(l,s,0,1)
        np.testing.assert_allclose([t[0],b[0],d[0]],[np.exp(-l*s),b0,d0],rtol=3e-15)

    def test_void_limit(self):
        t,b,d=polynomial_coefficients(.7,0,0,4)
        np.testing.assert_allclose(t,[1,0,0,0]);np.testing.assert_allclose(b,[.7,0,0,0])
        np.testing.assert_allclose(d,[.245,0,0,0])

    def test_zero_length(self):
        t,b,d=polynomial_coefficients(0.,2.,3.,8)
        np.testing.assert_array_equal(t,np.r_[1.,np.zeros(7)])
        np.testing.assert_array_equal(b,0.);np.testing.assert_array_equal(d,0.)

    def test_gamma_coefficients_match_independent_dense_blocks(self):
        for n in [1,2,4,8]:
            for total in [0.,.0125,4.]:
                for sign in [1,-1]:
                    dense=dense_coefficients(2.4,total,.96,[20/n]*n,sign)
                    poly=polynomial_coefficients(2.4,total,.96*n/20,n)
                    for a,b in zip(poly,dense[:3]):
                        np.testing.assert_allclose(shift_matrix(a,sign),b,rtol=2e-12,atol=1e-14)

    def test_dense_void_periodic_is_well_defined(self):
        t,b,d,a=dense_coefficients(.8,0.,.5,[.3,.7],periodic=True)
        np.testing.assert_allclose(a@np.ones(2),0,atol=2e-16)
        np.testing.assert_allclose(t@np.ones(2),1,atol=2e-16)
        np.testing.assert_allclose(b@np.ones(2),.8,atol=2e-16)
        np.testing.assert_allclose(d@np.ones(2),.32,atol=2e-16)

    def test_native_periodic_constant_mode(self):
        b0,d0=scalar_integrals(.7,.9);bn=b0*(1+1e-7);dn=d0*(1-2e-7)
        t,b,d,_=dense_coefficients(.7,.9,.6,[.2,.3,.5],periodic=True,native_b=bn,native_d=dn)
        np.testing.assert_allclose(t@np.ones(3),1-.9*bn,rtol=5e-15)
        np.testing.assert_allclose(b@np.ones(3),bn,rtol=5e-15)
        np.testing.assert_allclose(d@np.ones(3),dn,rtol=5e-15)

    def test_native_zero_streaming_coefficients(self):
        b0,d0=scalar_integrals(.7,.9);bn=b0*(1+1e-7);dn=d0*(1-2e-7)
        t,b,d=polynomial_coefficients(.7,.9,0,4,'native',bn,dn)
        np.testing.assert_allclose([t[0],b[0],d[0]],[1-.9*bn,bn,dn],rtol=2e-16)
        np.testing.assert_array_equal(t[1:],0.);np.testing.assert_array_equal(b[1:],0.)

    def test_incoming_and_source_segment_balance(self):
        t,b,d,a=dense_coefficients(.7,.9,.6,[.2,.3,.5])
        np.testing.assert_allclose(np.eye(3)-t,a@b,atol=4e-16)
        np.testing.assert_allclose(.7*np.eye(3)-b,a@d,atol=4e-16)

    def test_two_region_evolution_against_independent_ode(self):
        value=np.array([.4,.8,.2]);integrals=[]
        for total,length,source in [(1.2,.3,np.array([.2,1.,.7])),(.4,.7,np.array([.3,.1,2.]))]:
            t,b,d,a=dense_coefficients(length,total,.6,[.2,.3,.5],sign=-1)
            direct=solve_ivp(lambda x,y:np.r_[source-a@y[:3],y[:3]],(0,length),np.r_[value,np.zeros(3)],
                             method='DOP853',rtol=2e-13,atol=1e-14)
            np.testing.assert_allclose(t@value+b@source,direct.y[:3,-1],rtol=1e-12,atol=1e-14)
            np.testing.assert_allclose(b@value+d@source,direct.y[3:,-1],rtol=1e-12,atol=1e-14)
            integrals.append(b@value+d@source);value=t@value+b@source
        self.assertTrue(np.all(value>0) and np.all(np.array(integrals)>0))

    def test_opposite_sign_selects_opposite_neighbor(self):
        plus=upwind([1,1,1],1);minus=upwind([1,1,1],-1)
        np.testing.assert_array_equal(plus,minus.T)
        p=shift_matrix([.7,.2,.05],1);m=shift_matrix([.7,.2,.05],-1)
        np.testing.assert_array_equal(p,m.T)
        np.testing.assert_array_equal(p@np.array([0,0,1]),[0,0,.7])

    def test_positive_native_lift_and_its_raw_defect_are_not_rebalanced(self):
        b0,d0=scalar_integrals(.7,.9);bn=b0*(1+1e-6);dn=d0*(1-1e-6)
        t,b,d,a=dense_coefficients(.7,.9,.6,[.2,.3,.5],native_b=bn,native_d=dn)
        self.assertTrue(np.all(t>=0) and np.all(b>=0) and np.all(d>=0))
        self.assertGreater(np.max(abs(np.eye(3)-t-a@b)),1e-8)

    def test_full_green_sweep_against_dense_two_material_tracks(self):
        # Independently assemble every cell/source column, both planar orders
        # and both axial signs. This checks aggregation and indexing as well
        # as the primitive coefficient controls above.
        d=dict(nr=2,nb=2,nmu=2,nmax=4,track=np.array([0,0]),
               polar=np.array([0,1]),length=np.array([4,4]),
               region=np.tile([-1,1,2,-2],(2,1)),zmu=np.array([1.25,2.]),
               weight=np.array([.3,.8]),weights=np.array([.9,1.4,.7,.7]))
        d['h']=d['zmu'][:,None]*np.array([0.,.4,.7,0.])[None,:]
        a=dict(total=np.array([.7,1.2]),b=np.zeros((2,4)),self_d=np.zeros((2,4)))
        for p in range(2):
            for seg in [1,2]:
                b,own=scalar_integrals(d['h'][p,seg],a['total'][seg-1])
                a['b'][p,seg]=b*(1+1e-7);a['self_d'][p,seg]=own*(1-2e-7)
        for n in [1,3]:
            for kind in ['exact','native']:
                green,_=green_sweep(d,a,n,2.,kind);actual=expand_green(d,green)
                expected=np.zeros_like(actual);identity=np.eye(n)
                for z,sign in enumerate([1,-1]):
                    for p in range(2):
                        mu=np.sqrt(1-1/d['zmu'][p]**2)
                        for order,entry,exit_surface in [([1,2],2,3),([2,1],3,2)]:
                            value=np.zeros((n,4*n));value[:,entry*n:(entry+1)*n]=identity
                            for seg in order:
                                r=seg-1;kw={} if kind=='exact' else dict(native_b=a['b'][p,seg],native_d=a['self_d'][p,seg])
                                t,b,own,_=dense_coefficients(d['h'][p,seg],a['total'][r],mu,[2/n]*n,sign,**kw)
                                q=np.zeros_like(value);q[:,r*n:(r+1)*n]=identity
                                expected[z,p,r*n:(r+1)*n]+=(b@value+own@q)*d['weight'][p]/(2*d['weights'][r])
                                value=t@value+b@q
                            expected[z,p,exit_surface*n:(exit_surface+1)*n]+=value*d['weight'][p]/(2*d['weights'][exit_surface])
                np.testing.assert_allclose(actual,expected,rtol=3e-13,atol=2e-16)

    def test_rejects_negative_total_and_negative_native_transmission(self):
        with self.assertRaises(ValueError):polynomial_coefficients(1.,-1.,1.,2)
        with self.assertRaises(ValueError):polynomial_coefficients(1.,1.,1.,2,'native',2.,.5)


if __name__=='__main__':unittest.main()

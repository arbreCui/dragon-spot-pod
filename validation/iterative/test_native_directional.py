"""Analytical controls for the directional interface, independent of pin data."""
import unittest
import numpy as np
from qualify_native_directional import segment_step, sweep


def fixture():
    lengths=np.array([0.,.3,.7,0.]);sigma=np.array([1.2,.8])
    b=np.zeros((1,4));own=np.zeros((1,4))
    b[0,1:3]=-np.expm1(-sigma*lengths[1:3])/sigma
    own[0,1:3]=(lengths[1:3]-b[0,1:3])/sigma
    v=2*lengths[1:3]
    d=dict(nr=2,nb=2,na=1,nmu=1,nmax=4,track=np.array([0]),
           region=np.array([[-1,1,2,-2]]),length=np.array([4]),bin=np.array([0]),
           weight=np.ones(1),weights=np.r_[v,1.,1.],h=lengths[None,:],
           mx=np.array([.6]),harm=np.array([[[1.],[.8],[.6]]]))
    a=dict(total=sigma,b=b,self_d=own,pjsum=own[0,1:3].copy(),pjj=2*own[0,1:3]/v)
    return d,a


class DirectionalTests(unittest.TestCase):
    def test_segment_matches_exact_solution_and_balance(self):
        sigma=.9;h=.7;inc=1.1;q=.3
        b=-np.expm1(-sigma*h)/sigma;own=(h-b)/sigma
        out,f0,fs=segment_step(inc,q,sigma,b,own)
        self.assertAlmostEqual(out,inc*np.exp(-sigma*h)+q*b)
        self.assertAlmostEqual(out-inc,sigma*(-f0-fs)+q*h)

    def test_void_segment_limit(self):
        out,f0,fs=segment_step(.4,2.,0.,.7,.7**2/2)
        self.assertAlmostEqual(out,1.8)
        self.assertAlmostEqual(f0+fs,.77)

    def test_opposite_entrances_and_segment_order(self):
        d,a=fixture();x=sweep(d,a,np.zeros((2,1)),np.array([[3.],[7.]]),trace_column=0)
        tr=x['trace'];atten=np.exp(-a['total']*d['h'][0,1:3])
        self.assertEqual(tr['incoming'][0,0,1],3.)
        self.assertEqual(tr['incoming'][1,0,2],7.)
        self.assertAlmostEqual(tr['incoming'][0,0,2],3*atten[0])
        self.assertAlmostEqual(tr['incoming'][1,0,1],7*atten[1])
        np.testing.assert_allclose(x['outgoing'][:,0],np.array([7,3])*np.prod(atten))

    def test_own_source_is_essential_for_balance(self):
        d,a=fixture();q=np.array([[2.],[3.]]);x=sweep(d,a,q,np.zeros((2,1)))
        v=d['weights'][:2]
        birth=float(v@q[:,0]);collision=float((v*a['total'])@x['scalar'][:,0])
        self.assertAlmostEqual(birth,collision+sum(x['outgoing'][:,0]))
        isolated_collision=float((v*a['total'])@x['raw_iso'][:,0])
        self.assertGreater(birth-isolated_collision-sum(x['outgoing'][:,0]),.1)

    def test_rounding_ledger_is_not_placed_in_directional_bins(self):
        d,a=fixture();q=np.ones((2,1));x=sweep(d,a,q,np.zeros((2,1)))
        a['pjj']=a['pjj']+np.array([1e-7,-2e-7]);y=sweep(d,a,q,np.zeros((2,1)))
        np.testing.assert_array_equal(x['own'],y['own'])
        np.testing.assert_allclose(y['scalar']-x['scalar'],[[1e-7],[-2e-7]],atol=2e-16)
        np.testing.assert_array_equal(x['current'],y['current'])

    def test_equal_even_sources_and_opposite_odd_input_are_linear(self):
        d,a=fixture();even=np.ones((2,3));odd=np.array([[.2],[.3]])*np.array([-1,0,1])
        x=sweep(d,a,even,np.zeros((2,3)),odd)
        for k in ['full','current','outgoing']:
            np.testing.assert_allclose((x[k][:,0]+x[k][:,2])/2,x[k][:,1],atol=2e-16)
        self.assertGreater(np.max(abs(x['current'][:,2]-x['current'][:,0])),.01)

    def test_weight_and_normalizer_scaling(self):
        d,a=fixture();q=np.array([[2.],[3.]]);inc=np.array([[.7],[.9]])
        x=sweep(d,a,q,inc)
        d['weight']*=3;d['weights']*=3;a['pjsum']*=3
        y=sweep(d,a,q,inc)
        for k in ['scalar','current','outgoing']:
            np.testing.assert_allclose(x[k],y[k],rtol=2e-15,atol=1e-16)

    def test_signed_sources_are_not_clipped(self):
        d,a=fixture();q=np.array([[2.],[3.]]);inc=np.zeros((2,1))
        x=sweep(d,a,q,inc);y=sweep(d,a,-q,inc)
        np.testing.assert_allclose(x['scalar'],-y['scalar'],rtol=2e-15)
        self.assertLess(y['extrema']['integral_min'],0.)


if __name__=='__main__': unittest.main()

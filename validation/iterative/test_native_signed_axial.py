"""Independent small transport controls for axial signs and diffuse return."""
import unittest
import numpy as np
from qualify_native_signed_axial import axial_mu, angular_measures, signed_sweep, moments, common_white, ledger
from qualify_native_directional import sweep as planar_sweep


def fixture():
    lengths=np.array([0.,.3,.7,0.]);total=np.array([1.2,.8]);v=2*lengths[1:3]
    b=np.zeros((1,4));own=np.zeros((1,4))
    b[0,1:3]=-np.expm1(-total*lengths[1:3])/total
    own[0,1:3]=(lengths[1:3]-b[0,1:3])/total
    d=dict(nr=2,nb=2,nmu=1,na=1,nmax=4,track=np.array([0]),polar=np.array([0]),
           region=np.array([[-1,1,2,-2]]),length=np.array([4]),weight=np.ones(1),
           weights=np.r_[v,1.,1.],h=lengths[None,:],zmu=np.array([1.25]),
           bin=np.array([0]),mx=np.array([.8]),harm=np.array([[[1.],[0.],[.8]]]))
    a=dict(total=total,b=b,self_d=own,pjsum=own[0,1:3].copy(),pjj=2*own[0,1:3]/v)
    return d,a


def boundary_matrix(d,a):
    q=np.zeros((2,1,2,2));b=np.broadcast_to(np.eye(2),(2,1,2,2)).copy()
    x=signed_sweep(d,a,q,b)
    return moments(d,x['iso']+x['own'],x['boundary'])[2]


class SignedAxialTests(unittest.TestCase):
    def test_direction_uses_native_path_scale(self):
        d,a=fixture();mu=axial_mu(d)
        np.testing.assert_allclose(mu,[.6]);np.testing.assert_allclose(mu**2+1/d['zmu']**2,1.)
        d['zmu'][0]=.9
        with self.assertRaises(ValueError):axial_mu(d)

    def test_two_axial_signs_recover_planar_response_without_double_weight(self):
        d,a=fixture();q=np.array([[2.],[3.]]);inc=np.array([[.7],[.9]])
        expected=planar_sweep(d,a,q,inc)
        x=signed_sweep(d,a,np.broadcast_to(q,(2,1,2,1)),np.broadcast_to(inc,(2,1,2,1)))
        phi,jz,out=moments(d,x['iso']+x['own'],x['boundary'])
        np.testing.assert_allclose(phi,expected['full']);np.testing.assert_allclose(out,expected['outgoing'])
        np.testing.assert_array_equal(jz,0.)

    def test_planar_reversal_does_not_flip_axial_sign(self):
        d,a=fixture();q=np.zeros((2,1,2,1));q[0]=1
        x=signed_sweep(d,a,q,np.zeros((2,1,2,1)))
        self.assertTrue(np.all(x['boundary'][0]>0))  # Both planar exit surfaces.
        self.assertTrue(np.all(x['own'][0]>0))
        np.testing.assert_array_equal(x['boundary'][1],0.)
        np.testing.assert_array_equal(x['iso'][1]+x['own'][1],0.)

    def test_geometric_measures_sum_to_full_volume_and_surface(self):
        d,a=fixture();v,s=angular_measures(d)
        np.testing.assert_allclose(2*v.sum(axis=0),d['weights'][:2])
        np.testing.assert_allclose(2*s.sum(axis=0),d['weights'][2:])

    def test_even_and_odd_balance_for_asymmetric_angular_source(self):
        d,a=fixture();q=np.array([[[[2.],[.3]]],[[[.1],[3.]]]])
        inc=np.array([[[[.7],[.2]]],[[[.4],[1.1]]]])
        x=signed_sweep(d,a,q,inc)
        audit=ledger(d,a,q,inc,x['iso']+x['own'],x['boundary'])
        self.assertLess(max(audit['even_relative'].max(),audit['odd_relative'].max()),1e-15)
        self.assertTrue(np.all(x['minima']>=0))

    def test_white_return_erases_incoming_odd_moment(self):
        d,a=fixture();tbb=boundary_matrix(d,a)
        inc=common_white(tbb,np.array([[.1],[.9]]),1)
        np.testing.assert_array_equal(inc[0],inc[1])
        _,s=angular_measures(d)
        self.assertEqual(float(np.sum(s*(inc[0,:,:,0]-inc[1,:,:,0]))),0.)
        amp=inc[0,0];np.testing.assert_allclose(amp-tbb@amp,[[.1],[.9]])

    def test_wrong_separate_return_changes_odd_current_with_same_scalar(self):
        d,a=fixture();tbb=boundary_matrix(d,a)
        q=np.ones((2,1,2,1));q[0]+=np.array([[[.2],[.3]]]);q[1]-=np.array([[[.2],[.3]]])
        vacuum=signed_sweep(d,a,q,np.zeros((2,1,2,1)))
        _,jvac,ov=moments(d,vacuum['iso']+vacuum['own'],vacuum['boundary'])
        good=common_white(tbb,ov,1)
        wrong=np.zeros_like(good)
        for z in range(2):
            wrong[z,0]=np.linalg.solve(np.eye(2)-tbb,2*vacuum['boundary'][z,0])
        x=signed_sweep(d,a,q,good);y=signed_sweep(d,a,q,wrong)
        phix,jx,_=moments(d,x['iso']+x['own'],x['boundary'])
        phiy,jy,_=moments(d,y['iso']+y['own'],y['boundary'])
        np.testing.assert_allclose(phix,phiy,rtol=2e-15)
        np.testing.assert_allclose(jx,jvac,rtol=5e-15,atol=1e-16)
        self.assertGreater(np.max(abs(jx-jy)),.01)

    def test_signed_diagnostics_and_batch_independence(self):
        d,a=fixture();q=np.arange(1,13,dtype=float).reshape(2,1,2,3);q[...,2]*=-1
        inc=np.zeros((2,1,2,3));x=signed_sweep(d,a,q,inc,batch=1);y=signed_sweep(d,a,q,inc,batch=3)
        for k in x:np.testing.assert_array_equal(x[k],y[k])
        self.assertGreater(x['negative_counts'][:,2].sum(),0)


if __name__=='__main__':unittest.main()

"""Physical boundary, complete-coordinate and independent-reference controls."""
import sys
import unittest
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_layered_transport import transport,basis,aggregate,checks
from native_layered_reference import RectangleReference,homogeneous_source,packed
from native_oblique_streaming import ratio,independent_flight,transport as old_transport
from native_layered_white import bundle,close

ROOT=Path(sys.argv.pop(1)).resolve();LIB=ROOT/'build/layered.dylib'


class LayeredTests(unittest.TestCase):
    def physical(self,w,reg,s,H,nz,mu,o,order=32,entry=0):
        f=transport(LIB,w,reg,s,entry,H,nz,mu,o,order)
        row=checks(f,np.array(w),np.array(reg),np.array(s),H,nz,mu)
        self.assertTrue(row['passed'],row);return f

    def test_homogeneous_analytic_vacuum_escape(self):
        for total in [0.,1e-12,.4,4.]:
            for S,H,nz,mu,o in [(.007,1.,1,.2,1),(.8,1.,4,-.73,-1),(5.,20.,2,.95,1)]:
                f=self.physical([S],[0],np.full(8,total),H,nz,mu,o)
                a=aggregate(f['fields'],np.array([0]),nz,o,1)
                actual=np.array([a[k][...,:nz].sum() for k in ['volume','radial','axial']])
                expected=homogeneous_source(S,H,mu,total)
                self.assertLess(float(ratio(actual-expected,expected).max()),5e-12)
                self.assertGreater(actual[2],0.)

    def test_all_layered_coordinates_against_rectangle_reference(self):
        w=[.13,.7,.29];reg=np.array([0,1,0]);s=np.array([.7,3.9,0,0,0,0,0,0])
        for o in [1,-1]:
            for sign in [1,-1]:
                f=self.physical(w,reg,s,1.,4,sign*.73,o)
                ref=RectangleReference(w,reg,s,0,1,1.,4,sign*.73,o,f['q'],f['radial_input'],f['axial_input'])
                exact=ref.fixed(64,full=True)
                self.assertLess(float(ratio(f['fields']-exact,abs(exact).max(axis=(0,1))).max()),5e-12)

    def test_adaptive_reference_accuracy(self):
        w=[.13,.7,.29];reg=np.array([0,1,0]);s=np.array([.7,3.9,0,0,0,0,0,0])
        f=self.physical(w,reg,s,1.,4,-.73,-1)
        ref=RectangleReference(w,reg,s,0,1,1.,4,-.73,-1,f['q'],f['radial_input'],f['axial_input'])
        high=ref.fixed(64);adaptive,report=ref.adaptive(high)
        self.assertLess(report['estimated_normalized_error'],2e-13)
        self.assertLess(float(ratio(adaptive-high,ref.scale(adaptive)).max()),2e-13)
        actual=packed(aggregate(f['fields'],reg,4,-1,1))
        self.assertLess(float(ratio(actual-adaptive,ref.scale(adaptive)).max()),5e-12)

    def test_axial_reflection_full_basis(self):
        w=[.13,.7,.29];reg=np.array([0,1,0]);s=np.array([.7,3.9,0,0,0,0,0,0]);nz=4
        q,rad,ax=basis(nz,s,False)
        a=transport(LIB,w,reg,s,0,1.,nz,.73,1,32,q,rad,ax)
        b=transport(LIB,w,reg,s,0,1.,nz,-.73,1,32,q,rad,ax)
        a=aggregate(a['fields'],reg,nz,1,1);b=aggregate(b['fields'],reg,nz,1,1)
        perm=np.r_[np.arange(8*nz).reshape(8,nz)[:,::-1].ravel(),8*nz+np.arange(6*nz).reshape(6,nz)[:,::-1].ravel(),14*nz+np.arange(8)]
        for key in a:
            mirror=b[key][::-1] if key=='axial' else b[key][:,::-1]
            mirror=mirror[...,perm]
            self.assertLess(float(ratio(a[key]-mirror,abs(a[key]).max(axis=(0,1))).max()),5e-12)

    def test_planar_reflection_repeated_regions(self):
        w=np.array([.13,.7,.29]);reg=np.array([0,1,0]);s=np.array([.7,3.9,0,0,0,0,0,0])
        a=self.physical(w,reg,s,1.,4,.73,1);b=self.physical(w[::-1],reg[::-1],s,1.,4,.73,-1)
        a=aggregate(a['fields'],reg,4,1,1);b=aggregate(b['fields'],reg[::-1],4,-1,1)
        for k in a:self.assertLess(float(ratio(a[k]-b[k],abs(a[k]).max(axis=(0,1))).max()),5e-12)

    def test_matched_mode_regresses_sealed_kernel(self):
        with np.load(ROOT/'inputs/inventory.npz') as z:d={k:z[k] for k in z.files}
        for track,p,H,nz,o,sign in [(43,0,20.,1,1,-1),(8561,0,20.,1,-1,-1),(3922,3,1.,4,1,1),(5888,1,20.,2,-1,1)]:
            n=d['nseg'][track:track+1]-2;w=d['planar_widths'][track:track+1]*d['zmu'][p];reg=d['nom'][track:track+1,1:16]-1
            entry=int(d['entry_surface'][track] if o==1 else d['exit_surface'][track]);totals=d['group_totals']
            ref=independent_flight(w,n,reg,totals,[entry],o);mu=sign*np.sqrt(1-1/d['zmu'][p]**2)
            for order in [8,16]:
                old=old_transport(ROOT/'build/zero_gradient.dylib',w,n,reg,totals,ref,H,nz,mu,o,order,True)
                q=np.repeat(np.eye(14)[:8],nz,axis=0);rad=np.repeat(np.eye(14)[8:],nz,axis=0);ax=np.zeros((8,14))
                for gi in range(3):
                    result=transport(LIB,w[0,:n[0]],reg[0,:n[0]],totals[gi],entry,H,nz,mu,o,order,q,rad,ax,ref['incoming'][gi,0,:n[0]])
                    np.testing.assert_array_equal(result['fields'],old['fields'][0,gi,:n[0]*nz,:,:14])

    def test_primitive_witness_quadrature(self):
        s=np.array([0.,1e-12,.4,4,0,0,0,0]);f=self.physical([.007,.3,.9,1.4],np.arange(4),s,1.,4,-.73,-1)
        m=f['metrics'];gn,gw=leggauss(64);l=m[:,9];sig=m[:,10];src=m[:,11];t=l[:,None]*(gn+1)/2;w=l[:,None]*gw/2
        ex=np.exp(-sig[:,None]*t);B=(ex*w).sum(axis=1);D=(ex*(l[:,None]-t)*w).sum(axis=1)
        out=np.exp(-sig*l)*m[:,4]+B*src;integ=B*m[:,4]+D*src
        self.assertLess(float(ratio(m[:,5]-out,np.maximum(out,m[:,5])).max()),5e-12)
        self.assertLess(float(ratio(m[:,6]-integ,np.maximum(integ,m[:,6])).max()),5e-12)
        np.testing.assert_array_equal(m[:,7],m[:,5]-m[:,4]+sig*m[:,6]-l*src)

    def test_layered_sources_are_not_tied_together(self):
        f=self.physical([.8],[0],np.full(8,.4),1.,4,.73,1)
        a=aggregate(f['fields'],np.array([0]),4,1,1)
        self.assertGreater(float(abs(a['volume'][0,:,0]-a['volume'][0,:,3]).max()),1e-3)
        self.assertEqual(float(a['axial'][0].max()),0.)
        self.assertGreater(float(a['axial'][1,0,3]),0.)

    def test_bad_inputs_rejected(self):
        q,rad,ax=basis(2,np.ones(8));q[0,0]=-1
        with self.assertRaises(ValueError):transport(LIB,[1.],[0],np.ones(8),0,1.,2,.5,1,16,q,rad,ax)

    def test_physical_white_void_escape_and_independent_operator(self):
        for total in [0.,.4]:
            b=bundle(LIB,1.,2,total,32);f,row=close(b);self.assertTrue(row['passed'],row)
            exact=bundle(LIB,1.,2,total,64,True);rf,rr=close(exact);self.assertTrue(rr['passed'],rr)
            for k in ['fields','inflow','axial_escape']:
                self.assertLess(float(ratio(f[k]-rf[k],abs(rf[k]).max(axis=0)).max()),5e-12)
            if total==0:self.assertLess(float(ratio(f['axial_escape']-f['birth'],f['birth']).max()),1e-10)


if __name__=='__main__':unittest.main()

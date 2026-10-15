"""Cross-language preflight checked against the qualified literal geometry."""
import sys
import unittest
from pathlib import Path
import numpy as np
from native_oblique_full_preflight import scan,read
from native_oblique_track_geometry import geometry

ROOT=Path(sys.argv.pop(1)).resolve() if len(sys.argv)>1 else None


class PreflightTests(unittest.TestCase):
    def check(self,widths,H,nz,mu,orientation,order):
        w=np.zeros((1,15));w[0,:len(widths)]=widths
        m,r=scan(ROOT/'build/geometry_count.dylib',w,[len(widths)],1.,H,nz,mu,orientation,order)
        g=geometry(widths,H,nz,mu,orientation,order);n=len(widths)*nz
        np.testing.assert_array_equal(r[0,:n,0],g['volume'])
        np.testing.assert_array_equal(r[0,:n,1:5],g['face_in_measure'])
        np.testing.assert_array_equal(r[0,:n,5:9],g['face_out_measure'])
        np.testing.assert_array_equal(r[0,n:],0)
        np.testing.assert_array_equal(m[0,:3],[len(g['breaks'])-1,len(g['u']),len(g['ray'])])
        self.assertEqual(m[0,3],g['length'].min());self.assertEqual(m[0,4],g['weight'].min())

    def test_nonuniform_all_states(self):
        for h in [1.,20.]:
            for nz in [1,2,4]:
                for mu in [-.31,.31]:
                    for o in [-1,1]:
                        for q in [8,16]:self.check([.007,.41,2.3,.013],h,nz,mu,o,q)

    def test_corner_coincidences(self):
        for mu in [-.5,.5]:
            for o in [-1,1]:self.check([1.,1.,2.],2.,4,mu,o,16)

    def test_single_segment(self):
        for mu in [-.96,.96]:
            for o in [-1,1]:self.check([.002],20.,1,mu,o,8)

    def test_complete_original_order(self):
        d=read(ROOT/'inputs/inventory.npz')
        np.testing.assert_array_equal(d['original_track'],np.arange(11364))
        np.testing.assert_array_equal(d['original_record_multiplicity'],np.ones(11364))
        self.assertEqual(set(d['nom'][d['nom']>0]),set(range(1,9)))
        self.assertEqual(set(d['entry_surface'])|set(d['exit_surface']),set(range(6)))

    def test_native_critical_records(self):
        d=read(ROOT/'inputs/inventory.npz')
        for track in [0,43,3922,4009,5888,7575,7747]:
            nr=int(d['nseg'][track]-2)
            for p in range(4):
                w=d['planar_widths'][track,:nr]*d['zmu'][p];mu=np.sqrt(1-1/d['zmu'][p]**2)
                for o in [-1,1]:
                    self.check(w,20.,1,-mu,o,16)
                    self.check(w,1.,4,mu,o,8)

    def test_batch_independence(self):
        w=np.zeros((3,15));w[0,:2]=[1,2];w[1,:3]=[.1,.2,.3];w[2,0]=4
        counts=[2,3,1];lib=ROOT/'build/geometry_count.dylib'
        m,r=scan(lib,w,counts,1.2,1.,4,-.7,-1,16)
        for i in range(3):
            a,b=scan(lib,w[i:i+1],counts[i:i+1],1.2,1.,4,-.7,-1,16)
            np.testing.assert_array_equal(m[i],a[0]);np.testing.assert_array_equal(r[i],b[0])

    def test_reject_zero_mu(self):
        with self.assertRaises(RuntimeError):scan(ROOT/'build/geometry_count.dylib',np.ones((1,15)),[2],1.,1.,1,0.,1,8)


if __name__=='__main__':unittest.main()

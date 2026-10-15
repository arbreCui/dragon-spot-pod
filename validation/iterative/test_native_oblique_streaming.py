"""Independent recurrence, source mapping and raw-witness checks for streaming."""
import sys
import unittest
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from native_oblique_streaming import independent_flight,transport,checks,ratio
from native_oblique_track_geometry import geometry
from native_oblique_track_pilot import direct_flight,transport as literal,column_error

ROOT=Path(sys.argv.pop(1)).resolve()
with np.load(ROOT/'inputs/inventory.npz') as z:D={k:z[k] for k in z.files}
LIB=ROOT/'build/streaming.dylib'


def native_inputs(tracks,p,orientation):
    tracks=np.asarray(tracks);counts=D['nseg'][tracks]-2
    widths=D['planar_widths'][tracks]*D['zmu'][p];regions=D['nom'][tracks,1:16]-1
    entry=D['entry_surface'][tracks] if orientation==1 else D['exit_surface'][tracks]
    return widths,counts,regions,D['group_totals'],entry


class StreamingTests(unittest.TestCase):
    def run_case(self,tracks,p,H,nz,sign,o,q,debug=True):
        w,n,r,t,e=native_inputs(tracks,p,o);ref=independent_flight(w,n,r,t,e,o)
        result=transport(LIB,w,n,r,t,ref,H,nz,sign*np.sqrt(1-1/D['zmu'][p]**2),o,q,debug)
        self.assertTrue(checks(result,q)['passed'],checks(result,q))
        return result,ref,(w,n,r,t,e)

    def test_native_literal_recurrence(self):
        for track,p,H,nz,sign,o,q in [(43,0,20.,1,-1,1,16),(8561,0,20.,1,-1,-1,16),
              (3922,3,1.,4,1,1,8),(5888,1,20.,2,1,-1,16),(7575,2,1.,4,-1,1,16)]:
            result,ref,(w,n,r,t,e)=self.run_case([track],p,H,nz,sign,o,q)
            nr=int(n[0]);g=geometry(w[0,:nr],H,nz,sign*np.sqrt(1-1/D['zmu'][p]**2),o,q)
            np.testing.assert_array_equal(result['geometry'][0,:3],[len(g['breaks'])-1,len(g['u']),len(g['ray'])])
            for group in range(3):
                sig=t[group,r[0,:nr]];flight=direct_flight(w[0,:nr],sig,r[0,:nr],int(e[0]),o)
                old=literal(g,sig,r[0,:nr],flight,1.,.7,o)
                u=int(old['units']);fields=result['fields'][0,group,:nr*nz]
                for key,actual in [('integral',fields[:,0,:14]),('face_in',fields[:,1:5,:14]),('face_out',fields[:,5:,:14])]:
                    self.assertLess(column_error(actual,old[key][...,u+2:]),5e-12)
                self.assertLess(column_error(fields[:,0,15:16],old['integral'][:,u:u+1]),5e-12)

    def test_every_sign_orientation_order(self):
        for sign in [-1,1]:
            for o in [-1,1]:
                for q in [8,16]:self.run_case([0,7747],2,1.,4,sign,o,q)

    def test_batch_independence(self):
        tracks=[0,43,3922,8561];result,_,_=self.run_case(tracks,0,20.,2,-1,-1,16)
        for i,track in enumerate(tracks):
            alone,_,_=self.run_case([track],0,20.,2,-1,-1,16)
            for key in result:np.testing.assert_array_equal(result[key][i],alone[key][0])

    def test_repeated_region_assembly(self):
        result,_,(w,n,r,t,e)=self.run_case([43],1,20.,4,1,1,16)
        for group in range(3):
            expected=np.zeros((8,4,14));raw=result['fields'][0,group,:n[0]*4,0,:14].reshape(n[0],4,14)
            for i in range(n[0]):expected[r[0,i]]+=raw[i]
            np.testing.assert_array_equal(result['regional'][0,group],expected)
        self.assertLess(len(set(r[0,:n[0]])),n[0])

    def test_primitive_witness_independent_quadrature(self):
        result,_,_=self.run_case([8561,5888],3,1.,4,-1,-1,16)
        for m in result['metrics'].reshape(-1,48):
            l,s,src=m[9:12];b=quad(lambda x:np.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0]
            d=quad(lambda x:(l-x)*np.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0]
            out=np.exp(-s*l)*m[4]+b*src;integ=b*m[4]+d*src
            self.assertLess(float(ratio(m[5]-out,max(m[5],out))),5e-12)
            self.assertLess(float(ratio(m[6]-integ,max(m[6],integ))),5e-12)
            self.assertEqual(m[7],m[5]-m[4]+s*m[6]-l*src)

    def test_void_and_optically_thin(self):
        w=np.zeros((1,15));w[0,:3]=[.007,.3,1.2];n=np.array([3]);r=np.zeros((1,15),int);r[0,:3]=[0,1,0]
        t=np.array([[0.,0.,0,0,0,0,0,0],[1e-12,.5,0,0,0,0,0,0]])
        for o in [-1,1]:
            ref=independent_flight(w,n,r,t,[2],o)
            result=transport(LIB,w,n,r,t,ref,1.,4,-.73,o,16,True)
            self.assertTrue(checks(result,16)['passed'],checks(result,16))

    def test_reference_against_scalar_quadrature(self):
        w,n,r,t,e=native_inputs([43,3922,8561],3,-1);ref=independent_flight(w,n,r,t,e,-1)
        for tr in range(3):
            nr=n[tr]
            for group in range(3):
                flight=direct_flight(w[tr,:nr],t[group,r[tr,:nr]],r[tr,:nr],int(e[tr]),-1)
                for key in ['incoming','outgoing','integral']:
                    self.assertLess(column_error(ref[key][group,tr,:nr],flight[key]),5e-12)

    def test_reject_missing_coordinate(self):
        w,n,r,t,e=native_inputs([0],0,1);ref=independent_flight(w,n,r,t,e,1);ref['incoming']=ref['incoming'][...,:13]
        with self.assertRaises(ValueError):transport(LIB,w,n,r,t,ref,1.,1,.5,1,8)


if __name__=='__main__':unittest.main()

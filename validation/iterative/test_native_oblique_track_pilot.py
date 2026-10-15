"""Nonuniform native path controls, repeated regions and complete source assembly."""
import unittest
import numpy as np
from native_oblique_track_geometry import geometry
from native_oblique_track_pilot import direct_flight,transport,matched_fields,reflections,column_error,reference_at
from oblique_strip_geometry import geometry as uniform_geometry,relative
from qualify_oblique_strip_geometry import geometry_metrics
from preflight_native_oblique_track_pilot import selection
from native_oblique_track_storage import pack_geometry,unpack_geometry,pack_responses,unpack_responses


class NativePilotTests(unittest.TestCase):
    widths=np.array([.07,.6,.02]);regions=np.array([2,5,2]);totals=np.array([.2,2.,.2])

    def solve(self,mu=.7,o=1,layout=0,batch=16,order=16,nz=4):
        w=self.widths if layout==0 else self.widths[::-1]
        r=self.regions if layout==0 else self.regions[::-1]
        t=self.totals if layout==0 else self.totals[::-1]
        g=geometry(w,1,nz,mu,o,order);effective=o*(1 if layout==0 else -1)
        flight=direct_flight(w,t,r,0 if effective==1 else 3,o)
        f=transport(g,t,r,flight,.03,.6,effective,batch)
        return g,f,flight

    def test_rank_ties_are_lowest_original_index(self):
        chosen,ranks=selection({'x':np.array([5.,1.,3.,3.,5.,1.])})
        self.assertEqual(chosen,[0,1,2]);self.assertEqual([x['track'] for x in ranks],[1,2,0])

    def test_uniform_geometry_reduces_to_qualified_strip(self):
        a=geometry(np.array([.5,.5]),1,4,.7,-1,8);b=uniform_geometry(1,1,2,4,.7,-1,8)
        for k in b:np.testing.assert_array_equal(a[k],b[k])

    def test_nonuniform_original_measure_both_directions(self):
        for mu in [-.7,.7]:
            for o in [-1,1]:
                g=geometry(self.widths,20,8,mu,o,8)
                self.assertLess(geometry_metrics(g)[0],5e-13)
                np.testing.assert_array_equal(g['original_widths'],self.widths)

    def test_literal_void_regional_flight(self):
        w=np.array([.25,.5,.25]);r=np.array([2,5,2]);f=direct_flight(w,np.zeros(3),r,0,1)
        self.assertAlmostEqual(f['track_outgoing'][2],.5,15)
        self.assertAlmostEqual(f['track_outgoing'][5],.5,15)
        self.assertAlmostEqual(f['track_integral'][2],.25,15)
        self.assertAlmostEqual(f['track_integral'][5],.25,15)
        self.assertEqual(f['track_outgoing'][8],1)

    def test_literal_homogeneous_unity_source(self):
        w=self.widths;s=.8;f=direct_flight(w,np.full(3,s),self.regions,0,1);L=w.sum()
        B=-np.expm1(-s*L)/s;D=(L-B)/s
        self.assertAlmostEqual(f['track_outgoing'][:8].sum(),B,14)
        self.assertAlmostEqual(f['track_integral'][:8].sum(),D,14)
        self.assertAlmostEqual(f['track_integral'][8],B,14)

    def test_all_source_columns_batch_invariant(self):
        _,a,_=self.solve(batch=3);_,b,_=self.solve(batch=1000)
        for key in a:np.testing.assert_array_equal(a[key],b[key])

    def test_repeated_region_and_axial_mapping(self):
        g,f,flight=self.solve();u=int(f['units']);A=f['source_assembly'];nz=int(g['nz'])
        collapse=np.repeat(np.eye(8),nz,axis=0)
        np.testing.assert_array_equal(A@collapse,f['q'][:,u+2:u+10])
        self.assertEqual(int(A[:,2*nz].sum()),2)
        self.assertLess(f['source_assembly_relative'].max(),2e-14)

    def test_all_native_coordinates_matched(self):
        for mu in [-.7,.7]:
            for o in [-1,1]:
                g,f,flight=self.solve(mu=mu,o=o);u=int(f['units']);v,face=matched_fields(g,flight)
                self.assertLess(column_error(f['integral'][:,u+2:],v),1e-12)
                self.assertLess(column_error(f['face_out'][...,u+2:],face),1e-12)
                self.assertLess(relative(f['matched_endpoint_defect'],f['matched_endpoint_scale']).max(),1e-12)

    def test_source_cone_shared_faces_and_raw_balance(self):
        _,f,_=self.solve(mu=-.7,o=-1)
        self.assertGreaterEqual(f['minimum_piece_angle'].min(),0);self.assertGreaterEqual(f['minimum_piece_integral'].min(),0)
        self.assertEqual(abs(f['shared_defect']).max(),0)
        self.assertLess(relative(f['cell_defect'],f['cell_scale']).max(),1e-12)
        self.assertLess(relative(f['global_defect'],f['global_scale']).max(),1e-12)

    def test_reflections_and_native_weighted_moments(self):
        g,a,_=self.solve(mu=-.7,o=1);_,b,_=self.solve(mu=.7,o=1);_,c,_=self.solve(mu=-.7,o=-1,layout=1)
        self.assertLess(reflections(a,b,3,4,'z'),1e-12);self.assertLess(reflections(a,c,3,4,'x'),1e-12)
        np.testing.assert_array_equal(a['partial_regional_jx'],a['partial_regional_integral']*.6)
        np.testing.assert_array_equal(a['partial_regional_jz'],a['partial_regional_integral']*(-.7))
        np.testing.assert_array_equal(a['partial_regional_integral'].reshape(32,-1),a['source_assembly'].T@a['integral']*.03)

    def test_compact_geometry_and_all_response_entries_are_exact(self):
        g,f,_=self.solve(mu=-.7,o=-1);gp=pack_geometry(g);gr=unpack_geometry(gp)
        for key in g:np.testing.assert_array_equal(g[key],gr[key])
        fp=pack_responses(g,f);fr=unpack_responses(g,fp)
        for key in ['integral','face_in','face_out']:np.testing.assert_array_equal(f[key],fr[key])
        witness=fp['worst_input_witness']
        np.testing.assert_array_equal(relative(witness[:,3],witness[:,4]),f['maximum_piece_relative'])

    def test_packing_refuses_unequal_shared_face(self):
        g,f,_=self.solve();f['face_in'][4,0,0]+=1e-8
        with self.assertRaises(AssertionError):pack_responses(g,f)


if __name__=='__main__':unittest.main()

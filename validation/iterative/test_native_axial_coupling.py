"""Small independent controls for angular projection and fission eigenanalysis."""
import unittest
import json
from pathlib import Path
import numpy as np
from qualify_native_axial_coupling import (MU,axial_map,assemble,normalized_eigen,
                                         reconstruct,diagnostics,admission)


class CouplingTests(unittest.TestCase):
    def fixture(self):
        total=np.array([[1.,1.2],[.7,.8]])
        scatter=np.zeros((2,2,2));scatter[0,0]=.3;scatter[1,1]=.2
        scatter[1,0]=[.12,.09];scatter[0,1]=[.01,.02]
        volume=np.array([1.,2.])
        closure=np.array([[[.12,-.12],[-.06,.06]],[[.08,-.08],[-.04,.04]]])
        nuf=np.zeros((2,2,2));nuf[:,0,0]=[.1,.4];nuf[:,1,1]=[.15,.3]
        chi=np.zeros_like(nuf);chi[0,:,0]=1;chi[:,1,1]=[.7,.3]
        return total,scatter,closure,nuf,chi,volume

    def test_one_cell_has_exact_streaming_removal(self):
        total,_,_,_,_,w=self.fixture();b=np.array([[1.,.3],[.2,1.]])
        inv,d,e=axial_map(total[0],w,b,[7.])
        expect=b.T@((w*(total[0]+2*MU/7))[:,None]*b)
        np.testing.assert_allclose(inv,expect,rtol=2e-15,atol=2e-15)
        np.testing.assert_allclose(e@d@inv,np.eye(2),atol=1e-15)

    def test_two_cell_scalar_map_matches_explicit_physical_sweeps(self):
        total=np.array([.4,.7]);w=np.array([1.,2.]);h=[.3,.5]
        inv,d,e=axial_map(total,w,np.eye(2),h)
        source=np.array([[1.,3.],[2.,4.]])
        expected=np.zeros((2,2,2))
        for direction in range(2):
            incoming=np.zeros(2)
            for z in ([0,1] if direction==0 else [1,0]):
                out=(source[z]/2+(MU/h[z]-total/2)*incoming)/(MU/h[z]+total/2)
                expected[direction,z]=out;incoming=out
        actual=d@(source*w).ravel()
        np.testing.assert_allclose(actual.reshape(2,2,2),expected,atol=2e-15)
        np.testing.assert_allclose(inv@(e@actual),(source*w).ravel(),atol=2e-15)

    def test_project_angular_before_elimination(self):
        total=np.array([.1,4.]);w=np.array([1.,2.]);b=np.array([[1.],[2.]])
        inv,_,_=axial_map(total,w,b,[.5,.8])
        full,_,_=axial_map(total,w,np.eye(2),[.5,.8])
        lift=np.kron(np.eye(2),b)
        # Scalar projection after angle elimination is generally different.
        self.assertGreater(np.linalg.norm(inv-lift.T@full@lift),.01)

    def test_component_fission_and_scatter_orientation(self):
        t,s,c,nuf,chi,w=self.fixture();b=np.broadcast_to(np.eye(2),(2,2,2));h=[.2,.3]
        a,u,v,weights,inv,d=assemble(t,s,c,nuf,chi,w,b,h)
        phi=np.arange(1,9,dtype=float).reshape(2,2,2)
        prod=np.einsum('gic,gzi->zic',nuf,phi)
        birth=np.einsum('gic,zic->gzi',chi,prod)
        np.testing.assert_allclose(u@(v@phi.ravel()),(birth*w).ravel(),atol=2e-15)
        self.assertAlmostEqual(weights@(v@phi.ravel()),np.sum(prod*np.array(h)[:,None,None]*w[None,:,None]))
        expected=np.empty_like(phi)
        for g in range(2):
            expected[g]=(inv[g]@phi[g].ravel()).reshape(2,2)
            for z in range(2):
                expected[g,z]+=w*(c[g]@phi[g,z]-sum(s[g,j]*phi[j,z] for j in range(2)))
        np.testing.assert_allclose(a@phi.ravel(),expected.ravel(),atol=8e-15)

    def solve_fixture(self,b,h):
        t,s,c,nuf,chi,w=self.fixture()
        a,u,v,weight,inv,d=assemble(t,s,c,nuf,chi,w,b,h)
        modal,result=normalized_eigen(a,u,v,weight)
        phi,faces=reconstruct(b,modal,inv,d,len(h))
        result.update(diagnostics(t,s,c,nuf,chi,w,b,h,phi,faces,result['k']))
        return result,phi

    def test_full_eigen_balance_normalization_and_coordinate_invariance(self):
        b=np.broadcast_to(np.eye(2),(2,2,2));h=[.3,.5]
        result,phi=self.solve_fixture(b,h)
        other,field=self.solve_fixture(b@np.array([[2.,.3],[.1,.8]]),h)
        self.assertAlmostEqual(result['k'],other['k'],places=14)
        np.testing.assert_allclose(phi,field,rtol=2e-14,atol=2e-14)
        self.assertLess(result['full_angular_residual_relative'],1e-13)
        self.assertLess(abs(result['raw_balance']),1e-13)
        self.assertLess(abs(result['axial_telescope_error']),1e-13)
        self.assertAlmostEqual(result['global_nufission'],1.)
        self.assertEqual(result['bordered_jacobian_rank'],result['bordered_jacobian_size'])
        self.assertTrue(all(p['converged'] for p in result['power_starts']))

    def test_retains_and_rejects_negative_diamond_faces(self):
        # Large optical thickness can give negative downwind DD outflows.
        inv,d,e=axial_map(np.array([10.]),np.ones(1),np.ones((1,1)),[10.,10.])
        face=d@np.array([1.,0.]);self.assertLess(face.min(),0)
        np.testing.assert_allclose(inv@(e@face),[1.,0.],atol=2e-16)

    def test_negative_reference_cannot_enter_pod(self):
        result,_=self.solve_fixture(np.broadcast_to(np.eye(2),(2,2,2)),[.3,.5])
        thresholds=dict(equation_residual=1e-10,spectral_gap_relative_min=1e-8,
                        power_solution_agreement=1e-9,raw_balance_relative=1e-4)
        self.assertEqual(admission(result,thresholds),[])
        result['minimum_outgoing_angular_flux']=-1e-14
        self.assertEqual(admission(result,thresholds),['nonpositive_outgoing_angular_flux'])

    def test_enriched_weighted_balance_identity(self):
        b=np.ones((2,2,1));result,_=self.solve_fixture(b,[.3,.5])
        self.assertLess(result['projected_angular_residual_relative'],1e-13)
        self.assertLess(abs(result['weighted_angular_residual']),1e-13)
        self.assertLess(abs(result['balance_identity_error']),1e-13)

    def test_two_fission_components_match_analytic_one_group_eigenvalue(self):
        total=np.array([[1.2]]);scatter=np.array([[[.3]]]);closure=np.zeros((1,1,1))
        nuf=np.array([[[.2,.3]]]);chi=np.ones_like(nuf);w=np.array([2.]);b=np.ones((1,1,1))
        a,u,v,weight,inv,d=assemble(total,scatter,closure,nuf,chi,w,b,[4.])
        modal,result=normalized_eigen(a,u,v,weight)
        self.assertAlmostEqual(result['k'],.5/(.9+2*MU/4),places=14)
        self.assertAlmostEqual(modal[0],1/(4*2*.5),places=14)
        self.assertEqual(result['bordered_jacobian_rank'],3)

    def test_archived_full_and_projected_evidence(self):
        a=Path(__file__).resolve().parents[1]/'artifacts/native-axial-coupling-20260928'
        if not (a/'analysis/result.json').exists():
            a=Path(__file__).resolve().parents[1]  # Copied artifact build directory.
        if not (a/'analysis/result.json').exists():
            self.skipTest('sealed-data regression requires the local prepared artifact')
        result=json.loads((a/'analysis/result.json').read_text())
        self.assertEqual(len(result['references']),3)
        self.assertTrue(all(r['admitted'] for r in result['references']))
        self.assertLess(result['max_full_rank_flux_error'],1e-9)
        self.assertLess(result['max_oblique_flux_difference'],1e-9)
        self.assertEqual(result['negative_scalar_cases'],3)
        self.assertEqual(result['negative_angular_cases'],25)
        self.assertLess(result['max_enriched_weighted_residual'],1e-10)
        self.assertGreater(result['max_plain_abs_raw_balance_relative'],.09)
        self.assertTrue(all(r['inverse_residual_inf']<1e-10 for r in result['conditioning']))


if __name__=='__main__':unittest.main()

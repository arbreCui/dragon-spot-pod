"""Independent moment, dense-angle and conservation controls for refinement."""
import unittest
import numpy as np
from qualify_native_axial_refinement import NodalProblem,axial_elements,energy_fission,MU
from qualify_native_axial_coupling import solve as dense_solve
from diagnose_native_axial_sources import signed_source_audit
from summarize_native_axial_refinement import restrict_uniform


def fixture(heights):
    total=np.array([[1.,1.2],[.7,.8]]);scatter=np.zeros((2,2,2))
    scatter[0,0]=.3;scatter[1,1]=.2;scatter[1,0]=[.12,.09];scatter[0,1]=[.01,.02]
    volume=np.array([1.,2.]);loss=np.array([[[.12,-.12],[-.06,.06]],[[.08,-.08],[-.04,.04]]])
    for g in range(2):loss[g]+=np.diag(total[g])
    nuf=np.zeros((2,2,2));nuf[:,0,0]=[.1,.4];nuf[:,1,1]=[.15,.3]
    chi=np.zeros_like(nuf);chi[0,:,0]=1;chi[:,1,1]=[.7,.3]
    controls=dict(inner_rtol=2e-13,inner_restart=60,inner_restart_cycles=20,eigen_modes=2,
                  eigen_tolerance=5e-12,eigen_maxiter=500,full_angular_residual_relative=1e-9,
                  initial_solution_agreement=1e-8,eigen_residual_relative=1e-10,
                  raw_balance_relative_to_birth=1e-4)
    return NodalProblem(total,scatter,loss,nuf,chi,volume,heights,controls)


class RefinementTests(unittest.TestCase):
    def test_midpoint_mass_retains_alternating_nullspace(self):
        m,l=axial_elements([.3,.7,.5]);alt=(-1.)**np.arange(4)
        np.testing.assert_allclose(m@alt,0,atol=1e-16)
        np.testing.assert_allclose(l@np.ones(4),0,atol=1e-15)
        self.assertGreater(alt@l@alt,1.)
        self.assertAlmostEqual(np.ones(4)@m@np.ones(4),1.5)

    def test_invalid_mesh_rejected(self):
        for h in [[],[0.],[-1.],[np.nan]]:
            with self.assertRaises(ValueError):axial_elements(h)

    def test_nodal_operator_is_independent_current_continuity(self):
        p=fixture([.3,.7,.5]);x=np.arange(1,17,dtype=float).reshape(4,4)/7
        rho=2.7;cell=(x[:-1]+x[1:])/2
        collision=(p.k@cell.T-rho*p.f@cell.T).T
        avg=-p.d*np.diff(x,axis=0)/p.heights[:,None]
        left=avg+p.heights[:,None]*collision/2;right=avg-p.heights[:,None]*collision/2
        expect=np.vstack([left[0]+MU*x[0],left[1:]-right[:-1],-right[-1]+MU*x[-1]])
        np.testing.assert_allclose((p.removal(x)-rho*p.birth(x)).reshape(4,4),expect,rtol=2e-14,atol=2e-14)

    def test_every_preconditioner_mode_recovers_declared_robin_operator(self):
        p=fixture([.3,.7,.5]);x=np.arange(1,17,dtype=float).reshape(4,4)/7
        rhs=p.removal(x).reshape(4,4);rhs[[0,-1]]-=MU*x[[0,-1]]
        rhs[[0,-1]]+=p.preconditioner_alpha*x[[0,-1]]*p.d
        np.testing.assert_allclose(p.base_precondition(rhs).reshape(4,4),x,rtol=2e-13,atol=2e-13)
        self.assertEqual(len(p.factors),4)

    def test_boundary_correction_recovers_full_vacuum_operator(self):
        for heights in [[.3,.3,.3],[.3,.7,.5]]:
            p=fixture(heights);x=np.arange(1,17,dtype=float).reshape(4,4)/7
            np.testing.assert_allclose(p.precondition(p.removal(x)).reshape(4,4),x,rtol=2e-13,atol=2e-13)

    def test_inverse_matches_explicit_nodal_matrix(self):
        p=fixture([.3,.7,.5]);eye=np.eye(p.shape[0]);a=np.column_stack([p.removal(x) for x in eye])
        rhs=np.arange(1,len(eye)+1,dtype=float)
        np.testing.assert_allclose(p.inverse(rhs),np.linalg.solve(a,rhs),rtol=2e-12,atol=2e-12)

    def test_component_fission_has_correct_group_and_region_orientation(self):
        p=fixture([.3]);phi=np.arange(1,5,dtype=float).reshape(2,2)
        expected=np.einsum('gic,ic->gi',p.chi,np.einsum('hic,hi->ic',p.nuf,phi))
        np.testing.assert_allclose(p.f@phi.ravel(),expected.ravel(),atol=1e-15)

    def test_full_nodal_eigen_matches_dense_angular_form_for_three_meshes(self):
        for heights in [[.5],[.3,.7],[.3,.7,.5,.6]]:
            p=fixture(heights);result,phi,faces,nodal=p.solve()
            d=dict(total_r=p.total,scatter=p.scatter,v=p.volume)
            b=np.broadcast_to(np.eye(2),(2,2,2))
            reference,refphi,reffaces=dense_solve(d,p.loss,p.nuf,p.chi,b,heights)
            self.assertLess(abs(result['k']/reference['k']-1),1e-11)
            np.testing.assert_allclose(phi,refphi,rtol=1e-11,atol=1e-11)
            np.testing.assert_allclose(faces,reffaces,rtol=1e-11,atol=1e-11)
            self.assertTrue(result['admitted'])
            self.assertLess(result['full_angular_residual_relative'],1e-11)
            self.assertLess(abs(result['raw_balance']),1e-11)

    def test_global_normalization_uses_cell_integral_with_unequal_heights(self):
        p=fixture([.3,.7]);x=np.arange(1,13,dtype=float).reshape(3,4);y=p.normalize(x)
        cell=(y[:-1]+y[1:])/2
        self.assertAlmostEqual(np.sum(cell*p.nuf.sum(axis=2).ravel()*np.tile(p.volume,2)*p.heights[:,None]),1.)

    def test_conservative_restriction_preserves_uniform_cell_integral(self):
        phi=np.arange(24,dtype=float).reshape(2,6,2)
        coarse=restrict_uniform(phi)
        np.testing.assert_array_equal(2*coarse.sum(axis=1),phi.sum(axis=1))
        with self.assertRaises(ValueError):restrict_uniform(phi[:,:3])

    def test_negative_source_is_detected_with_nonnegative_attenuation(self):
        total=np.array([[.1]]);q=np.array([[[-2.]]]);h=[1.]
        out=-1/(MU+.05);faces=np.full((1,2,1,1),out)
        audit,_=signed_source_audit(total,h,np.ones((1,1,1)),faces,0*q,0*q,-q)
        self.assertEqual(audit['thin_nonnegative_inflow_negative_outflow_count'],2)
        self.assertEqual(audit['vacuum_negative_outflow_count'],2)
        self.assertEqual(audit['negative_outflow_with_negative_attenuation_count'],0)
        self.assertLess(audit['dd_reconstruction_max_abs_error'],1e-15)

    def test_positive_source_negative_attenuation_is_not_misattributed(self):
        total=np.array([[10.]]);h=[10.,10.];q=np.array([[[1.],[0.]]]);faces=np.zeros((1,2,2,1))
        for direction in range(2):
            incoming=0.
            for z in ([0,1] if direction==0 else [1,0]):
                outgoing=(q[0,z,0]/2+(MU/10-5)*incoming)/(MU/10+5)
                faces[0,direction,z,0]=outgoing;incoming=outgoing
        audit,_=signed_source_audit(total,h,np.ones((1,2,1)),faces,q,0*q,0*q)
        self.assertEqual(audit['thin_nonnegative_inflow_negative_outflow_count'],0)
        self.assertEqual(audit['negative_outflow_with_negative_attenuation_count'],1)
        self.assertEqual(audit['negative_effective_source_count'],0)


if __name__=='__main__':unittest.main()

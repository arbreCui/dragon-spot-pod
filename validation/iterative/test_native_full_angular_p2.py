"""Independent angular-integral controls; future bounded execution only.

Usage: python -B test_native_full_angular_p2.py --report /fresh/REPORT.json -v
These full370 algebra controls do not admit any actual A/B material payload.
"""
import argparse
import json
from pathlib import Path
import sys
import unittest
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_full_angular_p2 import (
    GROUPS,FISSION_COMPONENTS,DEGREES,real_harmonics_p2,
    angular_states_from_native,layer_material_ids,build_source_coefficients,
    reconstruct_source,iter_source_chunks,source_for_zonal_group,P2MomentAccumulator,
    current150_material_status,current150_source_coefficients,ReferenceInputUnready,
)

OBSERVATIONS = []


def sphere_rule():
    z,w = leggauss(8)
    azimuth = 2*np.pi*(np.arange(16)+.5)/16
    zz,az = np.meshgrid(z,azimuth,indexing='ij')
    transverse = np.sqrt(1-zz*zz)
    directions = np.stack([transverse*np.cos(az),transverse*np.sin(az),zz],axis=-1).reshape(-1,3)
    return directions,np.repeat(w/2/16,16)


def native_rule(distinct_geometry=False):
    x,w = leggauss(4)
    xmu = -(x+1)/2
    zmu = 1/np.sqrt(1-xmu*xmu)
    if distinct_geometry: zmu = zmu*(1+1e-7)
    az = np.pi*(np.arange(8)+.5)/8
    native = np.stack([np.ones((4,8)),np.sqrt(1-xmu*xmu)[:,None]*np.sin(az),
                       np.sqrt(1-xmu*xmu)[:,None]*np.cos(az)],axis=1).astype('f4')
    states = angular_states_from_native(xmu,zmu,w/2,np.cos(az),np.sin(az),native)
    return states,np.full(len(states.keys),1/16)


class AngularP2Tests(unittest.TestCase):
    def test_independent_legendre_addition_theorem_and_sphere_integrals(self):
        direction,weights = sphere_rule()
        R = real_harmonics_p2(direction)
        cosine = direction@direction.T
        independent = (np.ones_like(cosine),cosine,(3*cosine*cosine-1)/2)
        addition_error = 0.
        for degree,legendre in enumerate(independent):
            part = R[:,DEGREES == degree]
            difference = part@part.T-legendre
            addition_error = max(addition_error,float(np.max(np.abs(difference))))
            np.testing.assert_allclose(part@part.T,legendre,rtol=0,atol=2e-14)
        gram = R.T@(weights[:,None]*R)
        target = np.diag(1/(2*DEGREES+1))
        np.testing.assert_allclose(gram,target,rtol=0,atol=2e-14)
        OBSERVATIONS.append(dict(control='independent_Legendre_addition_and_sphere_integrals',
            addition_absolute=addition_error,gram_absolute=float(np.max(np.abs(gram-target)))))

    def test_all_native_angle_indices_parities_and_distinct_geometry_retained(self):
        states,track_weights = native_rule(distinct_geometry=True)
        self.assertEqual(len(states.keys),4*2*2*8)
        for index,(polar,sign,orientation,azimuth) in enumerate(states.keys):
            self.assertEqual(int(states.indices(polar,sign,orientation,azimuth)),index)
        inverse = states.indices(states.keys[:,0],-states.keys[:,1],-states.keys[:,2],states.keys[:,3])
        np.testing.assert_allclose(states.harmonics[inverse],states.harmonics*((-1.)**DEGREES),
                                   rtol=0,atol=2e-14)
        # XMU is preserved independently: deliberately inconsistent rounded
        # ZMU geometry must not overwrite the angular direction/harmonics.
        self.assertGreater(float(np.max(np.abs(states.directions-states.streaming_directions))),1e-9)
        np.testing.assert_array_equal(states.native_in_plane.astype('f4'),
            np.stack([np.ones((4,8)),
                states.directions[states.indices(np.arange(4)[:,None],1,1,np.arange(8)[None,:]),1],
                states.directions[states.indices(np.arange(4)[:,None],1,1,np.arange(8)[None,:]),0]],axis=1).astype('f4'))
        weights = states.ray_weights(np.arange(len(states.keys)),track_weights)
        self.assertAlmostEqual(float(weights.sum()),1.,places=14)
        # yz and xz retain independent orientation and axial-sign changes.
        for moment in (5,7):
            self.assertLess(float(states.harmonics[:,moment].min()),0.)
            self.assertGreater(float(states.harmonics[:,moment].max()),0.)
        OBSERVATIONS.append(dict(control='all_polar_sign_orientation_azimuth_states_retained',
            states=len(states.keys),explicit_z_signs=[-1,1],orientations=[1,-1],
            geometry_harmonic_difference=float(np.max(np.abs(states.directions-states.streaming_directions)))))

    def test_signed_full370_source_and_chunked_volume_moments(self):
        states,track_weights = native_rule()
        coefficient = np.sin(np.arange(8*3*GROUPS*9)).reshape(8,3,GROUPS,9)
        coefficient[:,:,:,0] = 0
        volume = (np.arange(24)+1).reshape(8,3)/24*50
        accumulator = P2MomentAccumulator(states,3)
        covered = []
        minimum = float('inf')
        for indices,source in iter_source_chunks(coefficient,states,max_states=7):
            covered.extend(indices.tolist())
            minimum = min(minimum,float(source.min()))
            accumulator.add(indices,source*volume[None,:,:,None],track_weights[indices])
            if indices[0] == 0:
                # Every group is directly consumable by the zonal kernel ABI,
                # without flattening or summing away the retained angular key.
                for group in range(GROUPS):
                    local = source_for_zonal_group(coefficient,states,0,group)
                    self.assertEqual(local.shape,(8*3,1))
                    self.assertTrue(local.flags.c_contiguous)
                    np.testing.assert_allclose(local[:,0],source[0,:,:,group].ravel(),rtol=0,atol=2e-14)
        self.assertEqual(covered,list(range(len(states.keys))))
        self.assertLess(minimum,0.)
        # Analytic angular integrals of R_lm^2 are 1/(2l+1).
        expected = coefficient/(2*DEGREES+1)
        actual = accumulator.flux_moments(volume)
        np.testing.assert_allclose(actual,expected,rtol=0,atol=4e-14)
        OBSERVATIONS.append(dict(control='signed_full370_source_and_chunked_moments',
            groups=GROUPS,minimum_source=minimum,
            angular_integral_absolute=float(np.max(np.abs(actual-expected)))))

    def test_full370_ABA_raw_scatter_against_direct_angular_convolution_all32_fissions(self):
        direction,weight = sphere_rule()
        R = real_harmonics_p2(direction)
        ids = layer_material_ids(np.arange(8),np.arange(8,16),'ABA',3)
        group_scale = (np.arange(GROUPS)+1)/GROUPS
        spatial = (np.arange(8)+1)[:,None]/8*np.array([1.,2.,1.])[None,:]
        # Incoming angular flux is an independent Cartesian polynomial.
        x,y,z = direction.T
        psi = (.4+.05*group_scale[None,:]+(.2*x-.1*y+.3*z)[:,None]*group_scale[None,:]+
               (.5*(z*z-1/3)+.2*x*y+.3*y*z+.1*x*z+.12*(x*x-y*y))[:,None])
        phi = np.zeros((8,3,GROUPS,9))
        phi[:,:,:,0] = spatial[:,:,None]*(.4+.05*group_scale)
        for moment,value in ((1,-.1*group_scale/3),(2,.3*group_scale/3),(3,.2*group_scale/3),
                             (4,.2/(5*np.sqrt(3))),(5,.3/(5*np.sqrt(3))),
                             (6,1/15),(7,.1/(5*np.sqrt(3))),(8,.24/(5*np.sqrt(3)))):
            phi[:,:,:,moment] = spatial[:,:,None]*value
        # Independently verify these analytic flux moments by sphere integration.
        direct_phi = np.einsum('a,am,ag->gm',weight,R,psi)
        np.testing.assert_allclose(phi,spatial[:,:,None,None]*direct_phi[None,None],rtol=0,atol=3e-14)
        scatter = np.zeros((16,3,GROUPS,GROUPS))
        nusigf = np.zeros((16,FISSION_COMPONENTS,GROUPS));chi = np.zeros_like(nusigf)
        source_group = np.arange(GROUPS)
        for material in range(16):
            for degree in range(3):
                destination = (source_group+(material+1)*(degree+1))%GROUPS
                strength = (.08+.01*material+.02*degree)*(1+group_scale/5)
                if degree: strength = strength*np.where(source_group%2,1.,-1.)
                scatter[material,degree,destination,source_group] = strength
            for component in range(FISSION_COMPONENTS):
                nusigf[material,component,(11*component+material)%GROUPS] = .01+material/1000+component/10000
                chi[material,component,(7*component+2*material)%GROUPS] = 1.
        eigenvalue = 1.07
        support = build_source_coefficients(phi,scatter,ids,nusigf,chi,eigenvalue)
        actual = reconstruct_source(support['coefficients'],R)
        expected = np.zeros_like(actual)
        cosine = direction@direction.T
        legendre = (np.ones_like(cosine),cosine,(3*cosine*cosine-1)/2)
        convolution = [P@(weight[:,None]*psi) for P in legendre]
        expected_rates = np.zeros((8,3,FISSION_COMPONENTS))
        for region in range(8):
            for layer in range(3):
                material = ids[region,layer]
                for degree in range(3):
                    destination = (source_group+(material+1)*(degree+1))%GROUPS
                    strength = scatter[material,degree,destination,source_group]
                    expected[:,region,layer,destination] += (
                        (2*degree+1)*spatial[region,layer]*convolution[degree]*strength[None,:])
                for component in range(FISSION_COMPONENTS):
                    src = (11*component+material)%GROUPS
                    dst = (7*component+2*material)%GROUPS
                    rate = phi[region,layer,src,0]*nusigf[material,component,src]
                    expected_rates[region,layer,component] = rate
                    expected[:,region,layer,dst] += rate/eigenvalue
        np.testing.assert_allclose(actual,expected,rtol=0,atol=2e-13)
        np.testing.assert_allclose(support['fission_component_rates'],expected_rates,rtol=0,atol=2e-15)
        np.testing.assert_allclose(actual[:,:,0],actual[:,:,2],rtol=0,atol=0)
        self.assertGreater(float(np.max(np.abs(actual[:,:,1]-2*actual[:,:,0]))),1e-5)
        self.assertFalse(support['full_reference_qualified'])
        OBSERVATIONS.append(dict(control='full370_ABA_direct_Legendre_convolution_and_all32_fissions',
            groups=GROUPS,fission_components=FISSION_COMPONENTS,
            source_absolute=float(np.max(np.abs(actual-expected))),
            component_rate_absolute=float(np.max(np.abs(support['fission_component_rates']-expected_rates)))))

    def test_incomplete_states_invalid_shape_and_nonfinite_values_refused(self):
        states,track_weights = native_rule()
        accumulator = P2MomentAccumulator(states,3)
        accumulator.add(np.array([0]),np.ones((1,8,3,GROUPS)),track_weights[:1])
        with self.assertRaises(ValueError): accumulator.flux_moments(np.ones((8,3)))
        with self.assertRaises(ValueError): reconstruct_source(np.ones((8,3,3,9)),states.harmonics)
        with self.assertRaises(ValueError): reconstruct_source(np.ones((8,3,GROUPS,3)),states.harmonics)
        bad = np.zeros((8,3,GROUPS,9));bad[0,0,0,8] = np.nan
        with self.assertRaises(ValueError): reconstruct_source(bad,states.harmonics)
        with self.assertRaises(ValueError): layer_material_ids(np.arange(8),None,'ABA',3)
        with self.assertRaises(ValueError): states.indices(0,0,1,0)
        with self.assertRaises(ValueError): states.indices(0,-1,1,8)
        with self.assertRaises(ValueError): real_harmonics_p2(np.array([[.9,0.,0.]]))

    def test_actual_current150_material_and_angular_context_remain_UNREADY(self):
        status = current150_material_status(None)
        self.assertEqual(status['status'],'UNREADY')
        for name in ('actual_A_B_raw_transfer','TRANC_semantics','reaction_multiplicity',
                     'SPH_MASK_context','complete_angular_input'):
            self.assertIn(name,status['missing'])
        self.assertFalse(status['full_reference_qualified'])
        with self.assertRaises(ReferenceInputUnready): current150_source_coefficients()
        OBSERVATIONS.append(dict(control='actual_material_context_explicit_UNREADY',missing=status['missing']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    args,remaining = parser.parse_known_args()
    result = unittest.main(argv=[sys.argv[0],*remaining],exit=False).result
    with args.report.open('x') as stream:
        json.dump(dict(schema='FULL370_P2_ANGULAR_SOURCE_COMPONENT_CONTROLS_V1',
            tests_run=result.testsRun,passed=result.wasSuccessful(),full_reference_qualified=False,
            actual_A_B_material_admitted=False,observations=OBSERVATIONS,
            failures=[str(name) for name,_ in result.failures],
            errors=[str(name) for name,_ in result.errors]),stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write('\n')
    sys.exit(0 if result.wasSuccessful() else 1)

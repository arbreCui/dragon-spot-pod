"""Controls for actual layer crossings; no multigroup qualification claim."""
import sys
import json
import unittest
from pathlib import Path
import numpy as np
from native_layered_transport import transport, basis, METRICS
from native_layered_zonal import transport_zonal
from native_layered_reference import RectangleReference
from native_oblique_streaming import independent_flight

LIB = Path(sys.argv.pop(1)).resolve()
REPORT = Path(sys.argv.pop(1)).resolve()
OBSERVATIONS = []


class ZonalRectangleReference(RectangleReference):
    """Independent rectangle intersections and exprel/hyp1f1 integration."""
    def __init__(self, widths, regions, total, entry, exit_surface, H, nz, mu,
                 orientation, q, radial, axial):
        super().__init__(widths, regions, total[:, 0], entry, exit_surface,
                         H, nz, mu, orientation, q, radial, axial)
        self.sigma = total[self.region, self.layer]


class ZonalTests(unittest.TestCase):
    def assert_ledger(self, result, widths, regions, total, H, nz):
        fields = result['fields']
        indices = np.repeat(regions, nz)*nz + np.tile(np.arange(nz), len(regions))
        born = np.repeat(widths, nz)[:, None]*(H/nz)*result['q'][indices]
        sigma = total[np.repeat(regions, nz), np.tile(np.arange(nz), len(regions))]
        collision = sigma[:, None]*fields[:, 0]
        incoming = fields[:, 1:5].sum(axis=1)
        outgoing = fields[:, 5:9].sum(axis=1)
        defect = born+incoming-outgoing-collision
        scale = np.maximum((abs(born)+abs(fields[:, 1:5]).sum(axis=1)).max(axis=0), 1e-100)
        self.assertLess(float((abs(defect)/scale).max()), 1e-10)
        metrics = result['metrics']
        np.testing.assert_allclose(metrics[:, METRICS.index('global_collision')],
                                   collision.sum(axis=0), rtol=5e-12, atol=1e-14)
        self.assertLess(float((abs(metrics[:, 24])/np.maximum(metrics[:, 25], 1e-100)).max()), 1e-10)
        self.assertEqual(float(metrics[:, 26].max()), 0.)
        # Check every shared radial and axial face, independently of metrics.
        cells = fields.reshape(len(regions), nz, 9, -1)
        for outgoing_face, incoming_face in (
                (cells[:-1, :, 6], cells[1:, :, 1]),
                (cells[1:, :, 5], cells[:-1, :, 2]),
                (cells[:, :-1, 8], cells[:, 1:, 3]),
                (cells[:, 1:, 7], cells[:, :-1, 4])):
            np.testing.assert_array_equal(outgoing_face, incoming_face)
        OBSERVATIONS.append(dict(control='independent_cell_and_global_ledger',
            primitive_relative=float(metrics[:, 2].max()),
            cell_relative=float((abs(defect)/scale).max()),
            global_relative=float((abs(metrics[:, 24])/np.maximum(metrics[:, 25], 1e-100)).max()),
            shared_face_absolute=float(metrics[:, 26].max())))

    def test_homogeneous_zonal_preserves_original_physical_fields(self):
        widths = np.array([.13, .7, .29]); regions = np.array([0, 1, 0])
        total = np.array([.7, 3.9, 0., 1e-12, 0., 0., 0., 0.])
        for orientation in (1, -1):
            for mu in (.73, -.73):
                old = transport(LIB, widths, regions, total, 0, 1., 3, mu, orientation, 32)
                new = transport_zonal(LIB, widths, regions, np.repeat(total[:, None], 3, axis=1),
                                      0, 1., 3, mu, orientation, 32)
                np.testing.assert_array_equal(new['fields'], old['fields'])
                np.testing.assert_array_equal(new['geometry'], old['geometry'])
                OBSERVATIONS.append(dict(control='homogeneous_old_physical_bit_equal',
                    orientation=orientation,mu=mu,field_absolute=0.,geometry_absolute=0.))

    def test_original_matched_ABI_retains_constant_material_regression(self):
        widths=np.array([.13,.7,.29]);regions=np.array([0,1,0]);nz=3;H=1.
        total=np.array([.7,3.9,0.,0.,0.,0.,0.,0.])
        padded_widths=np.zeros((1,15));padded_widths[0,:3]=widths
        padded_regions=np.zeros((1,15),dtype=int);padded_regions[0,:3]=regions
        q=np.repeat(np.eye(14)[:8],nz,axis=0)
        radial=np.repeat(np.eye(14)[8:],nz,axis=0);axial=np.zeros((8,14))
        for orientation in (1,-1):
            reference=independent_flight(padded_widths,np.array([3]),padded_regions,
                                         total[None,:],[0],orientation)
            for mu in (.73,-.73):
                result=transport(LIB,widths,regions,total,0,H,nz,mu,orientation,32,
                    q,radial,axial,reference['incoming'][0,0,:3])
                integrals=result['fields'].reshape(3,nz,9,14)[:,:,0].sum(axis=1)
                np.testing.assert_allclose(integrals,reference['integral'][0,0,:3]*H,
                                           rtol=5e-12,atol=1e-14)
                OBSERVATIONS.append(dict(control='legacy_matched_constant_material',
                    orientation=orientation,mu=mu,
                    absolute=float(abs(integrals-reference['integral'][0,0,:3]*H).max())))

    def test_ABA_profile_against_independent_whole_ray_reference(self):
        widths = np.array([.13,.7,.29,.31,.17,.22,.19,.23,.27])
        regions = np.array([0,1,0,2,3,4,5,6,7]); nz = 3
        total = np.array([[.7, 3.9, .7], [0., .4, 0.], [1., 2., 1.],
                          [0., 0., 0.], [.2, .8, .2], [3., .5, 3.],
                          [.9, 1.9, .9], [1e-12, 0., 1e-12]])
        for orientation in (1, -1):
            for mu in (.73, -.73):
                result = transport_zonal(LIB, widths, regions, total, 0, 1., nz, mu, orientation, 32)
                reference = ZonalRectangleReference(widths, regions, total, 0, 1, 1., nz,
                    mu, orientation, result['q'], result['radial_input'], result['axial_input'])
                exact = reference.fixed(64, full=True)
                scale = np.maximum(abs(exact).max(axis=(0, 1)), 1e-100)
                self.assertLess(float((abs(result['fields']-exact)/scale).max()), 5e-12)
                OBSERVATIONS.append(dict(control='all8_ABA_independent_rectangle_reference',
                    orientation=orientation,mu=mu,
                    relative=float((abs(result['fields']-exact)/scale).max()),
                    totals_shape=list(total.shape)))
                self.assert_ledger(result, widths, regions, total, 1., nz)
                # Constant psi=1 remains exact with q=local sigma, all inflows=1.
                np.testing.assert_allclose(result['fields'][:, 0, -1],
                                           np.repeat(widths, nz)/nz, rtol=5e-12, atol=1e-14)

    def test_independent_analytic_three_layer_crossing_including_void(self):
        # A long horizontal extent supplies a complete bottom-to-top ray at u=-.2.
        # Its independently clipped path crosses all three different sigma layers.
        nz=3; mu=.5; total=np.zeros((8,nz)); total[0]=[.7, 0., 2.3]
        q=np.zeros((8*nz,1)); q[:nz,0]=[.4, .8, .2]
        radial=np.zeros((6*nz,1)); axial=np.full((8,1),.6)
        ref=ZonalRectangleReference([4.],np.array([0]),total,0,1,1.,nz,mu,1,q,radial,axial)
        cells=ref.ray(-.2,full=True)
        incoming=.6
        for layer in range(nz):
            length=1/(nz*mu); sigma=total[0,layer]; source=q[layer,0]
            attenuation=np.exp(-sigma*length)
            B=length if sigma==0 else -np.expm1(-sigma*length)/sigma
            D=length*length/2 if sigma==0 else (length-B)/sigma
            integral=B*incoming+D*source; outgoing=attenuation*incoming+B*source
            np.testing.assert_allclose(cells[layer,0,0],integral,rtol=5e-12,atol=1e-14)
            np.testing.assert_allclose(cells[layer,8,0],outgoing,rtol=5e-12,atol=1e-14)
            incoming=outgoing
        result=transport_zonal(LIB,[4.],[0],total,0,1.,nz,mu,1,32,q,radial,axial)
        exact=ref.fixed(64,full=True)
        np.testing.assert_allclose(result['fields'],exact,rtol=5e-12,atol=1e-14)
        OBSERVATIONS.append(dict(control='three_distinct_layers_with_void_analytic_ray',
            layer_path_lengths=[1/(nz*mu)]*nz,
            rectangle_absolute=float(abs(result['fields']-exact).max())))
        self.assert_ledger(result,np.array([4.]),np.array([0]),total,1.,nz)

    def test_signed_sources_are_applied_without_clipping(self):
        nz=3;total=np.repeat(np.arange(8)[:,None]/4,nz,axis=1);total[:,1]*=2
        q,radial,axial=basis(nz,total[:,0],False)
        complete=transport_zonal(LIB,[.3,.4],[0,1],total,0,1.,nz,-.61,-1,32,q,radial,axial)
        coefficients=np.linspace(-1.,1.,q.shape[1])[:,None]
        signed=transport_zonal(LIB,[.3,.4],[0,1],total,0,1.,nz,-.61,-1,32,
                               q@coefficients,radial@coefficients,axial@coefficients)
        self.assertLess(float(signed['fields'].min()),0.)
        np.testing.assert_allclose(signed['fields'],complete['fields']@coefficients,rtol=5e-12,atol=1e-14)
        OBSERVATIONS.append(dict(control='signed_source_linear_superposition',
            minimum_field=float(signed['fields'].min()),
            absolute=float(abs(signed['fields']-complete['fields']@coefficients).max())))
        self.assert_ledger(signed,np.array([.3,.4]),np.array([0,1]),total,1.,nz)

    def test_transpose_and_nonfinite_inputs_rejected(self):
        arguments=(LIB,[.3],[0],np.ones((8,3)),0,1.,3,.5,1,16)
        for bad in (np.ones(8),np.ones((3,8)),np.full((8,3),np.nan),np.full((8,3),np.inf),-np.ones((8,3))):
            with self.assertRaises(ValueError):
                transport_zonal(*arguments[:3],bad,*arguments[4:])
        q,radial,axial=basis(3,np.ones(8),False)
        q[0,0]=np.inf
        with self.assertRaises(ValueError):transport_zonal(*arguments,q,radial,axial)
        q,radial,axial=basis(3,np.ones(8),False)
        radial[0,0]=np.nan
        with self.assertRaises(ValueError):transport_zonal(*arguments,q,radial,axial)
        q,radial,axial=basis(3,np.ones(8),False)
        axial[0,0]=np.inf
        with self.assertRaises(ValueError):transport_zonal(*arguments,q,radial,axial)
        with self.assertRaises(TypeError):transport_zonal(*arguments,matched_reference=np.ones((1,1)))


if __name__=='__main__':
    result=unittest.main(exit=False).result
    with REPORT.open('x') as stream:
        json.dump(dict(schema='LAYERED_ZONAL_COMPONENT_CONTROLS_V1',
            component_only=True,full370_reference_qualified=False,
            tests_run=result.testsRun,passed=result.wasSuccessful(),
            failures=[str(name) for name,_ in result.failures],
            errors=[str(name) for name,_ in result.errors],
            observations=OBSERVATIONS),stream,sort_keys=True,indent=2,allow_nan=False)
        stream.write('\n')
    sys.exit(0 if result.wasSuccessful() else 1)

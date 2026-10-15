"""Six fixed-source component controls; no actual A/B or reference admission.

Run only under the coordinating owner's bounded guard after compiling the
new Source. --old-library is the independently saved original zonal library.
"""
import argparse
import json
import sys
import time
import unittest
from pathlib import Path
import numpy as np
from native_layered_multigroup import transport_multigroup
from native_layered_zonal import transport_zonal
from native_layered_transport import transport, METRICS
from native_layered_reference import RectangleReference

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--library', type=Path, required=True)
PARSER.add_argument('--old-library', type=Path, required=True)
PARSER.add_argument('--report', type=Path, required=True)
ARGS, REMAINING = PARSER.parse_known_args()
sys.argv = [sys.argv[0], *REMAINING]
LIB, OLD = ARGS.library.resolve(), ARGS.old_library.resolve()
OBSERVATIONS = []


class ZonalRectangleReference(RectangleReference):
    """Separate decimal rectangle clipping and exprel/hyp1f1 recurrence."""
    def __init__(self, widths, regions, total, entry, H, nz, mu, orientation,
                 q, radial, axial):
        super().__init__(widths, regions, total[:, 0], entry, 1, H, nz, mu,
                         orientation, q, radial, axial)
        self.sigma = total[self.region, self.layer]


def fixture(nz, columns, case='AAA'):
    r = np.arange(8)[:, None]
    group = np.arange(columns)[None, :]
    a = .03 + (r+1)*.11 + group*.002
    total = np.repeat(a[:, None, :], nz, axis=1)
    if case == 'ABA':
        total[:, nz//3:2*nz//3] = (.05+(r+1)*.19+group*.003)[:, None, :]
    # Zero and optically thin columns are retained alongside all positive ones.
    total[:, :, 0] = 0.
    if columns > 1: total[:, :, 1] = 1e-12
    q = (.003 + np.arange(8*nz)[:, None]*.0001 + group*.000003)
    radial = (.2 + np.arange(6*nz)[:, None]*.001 + group*.00001)
    axial = np.zeros((8, columns))
    return total, q, radial, axial


class MultigroupTests(unittest.TestCase):
    def ledger(self, result, widths, regions, H, nz):
        fields, total = result['fields'], result['total']
        r, z = np.repeat(regions, nz), np.tile(np.arange(nz), len(regions))
        born = np.repeat(widths, nz)[:, None]*(H/nz)*result['q'][r*nz+z]
        collision = total[r, z]*fields[:, 0]
        incoming, outgoing = fields[:, 1:5].sum(axis=1), fields[:, 5:9].sum(axis=1)
        defect = born+incoming-outgoing-collision
        scale = np.maximum((abs(born)+abs(fields[:, 1:5]).sum(axis=1)).max(axis=0), 1e-100)
        relative = float((abs(defect)/scale).max())
        self.assertLess(relative, 1e-10)
        m = result['metrics']
        np.testing.assert_allclose(m[:, METRICS.index('global_collision')],
                                   collision.sum(axis=0), rtol=5e-12, atol=1e-14)
        self.assertLess(float(m[:, 2].max()), 1e-10)
        self.assertLess(float((abs(m[:, 24])/np.maximum(m[:, 25], 1e-100)).max()), 1e-10)
        self.assertEqual(float(m[:, 26].max()), 0.)
        cells = fields.reshape(len(regions), nz, 9, -1)
        for out, inc in ((cells[:-1, :, 6], cells[1:, :, 1]),
                         (cells[1:, :, 5], cells[:-1, :, 2]),
                         (cells[:, :-1, 8], cells[:, 1:, 3]),
                         (cells[:, 1:, 7], cells[:, :-1, 4])):
            np.testing.assert_array_equal(out, inc)
        return relative

    def test_all370_columns_original_zonal_bit_exact(self):
        # Small geometry bounds the 370 separate legacy calls. Each group has
        # a different total; no equivalence to the full150 reference is claimed.
        widths, regions = np.array([.01, .02]), np.array([0, 7])
        total, q, radial, axial = fixture(1, 370)
        new = transport_multigroup(LIB, widths, regions, total, 0, 1., 1,
                                   .61, 1, 16, q, radial, axial)
        for c in range(370):
            old = transport_zonal(OLD, widths, regions, total[:, :, c], 0,
                                  1., 1, .61, 1, 16, q[:, c:c+1],
                                  radial[:, c:c+1], axial[:, c:c+1])
            np.testing.assert_array_equal(new['fields'][:, :, c:c+1], old['fields'])
            np.testing.assert_array_equal(new['geometry'], old['geometry'])
            np.testing.assert_array_equal(new['metrics'][c], old['metrics'][0])
            if c in (0, 1, 184, 369):
                old_export = transport_zonal(LIB, widths, regions, total[:, :, c],
                    0, 1., 1, .61, 1, 16, q[:, c:c+1],
                    radial[:, c:c+1], axial[:, c:c+1])
                for field in ('fields', 'geometry', 'metrics'):
                    np.testing.assert_array_equal(old_export[field], old[field])
        # Also exercise the old constant-total ABI against its saved provider.
        constant = transport(OLD, widths, regions, total[:, 0, 184], 0,
                             1., 1, .61, 1, 16, q[:, 184:185],
                             radial[:, 184:185], axial[:, 184:185])
        np.testing.assert_array_equal(new['fields'][:, :, 184:185], constant['fields'])
        np.testing.assert_array_equal(new['geometry'], constant['geometry'])
        constant_export = transport(LIB, widths, regions, total[:, 0, 184], 0,
            1., 1, .61, 1, 16, q[:, 184:185], radial[:, 184:185], axial[:, 184:185])
        for field in ('fields', 'geometry', 'metrics'):
            np.testing.assert_array_equal(constant_export[field], constant[field])
        OBSERVATIONS.append(dict(control='all370_distinct_totals_old_zonal_bit_exact',
            columns=370, field_absolute=0., metric_absolute=0., geometry_absolute=0.,
            preserved_old_zonal_columns=[0, 1, 184, 369],
            preserved_old_constant_column=184, independent_physical_reference=False))

    def test_all8_all370_AAA_ABA_150cm_cell_and_global_ledger(self):
        widths = np.array([.13, .7, .29, .31, .17, .22, .19, .23, .27])
        regions = np.array([0, 1, 0, 2, 3, 4, 5, 6, 7]); H, nz = 150., 3
        for case in ('AAA', 'ABA'):
            total, q, radial, axial = fixture(nz, 370, case)
            for orientation in (1, -1):
                for mu in (.73, -.73):
                    result = transport_multigroup(LIB, widths, regions, total, 0,
                        H, nz, mu, orientation, 32, q, radial, axial)
                    error = self.ledger(result, widths, regions, H, nz)
                    cells = result['fields'].reshape(len(widths), nz, 9, 370)
                    incoming_face = 3 if mu > 0 else 4
                    entering_layer = 0 if mu > 0 else nz-1
                    self.assertEqual(float(abs(cells[:, entering_layer, incoming_face]).max()), 0.)
                    self.assertFalse(result['full_reference_qualified'])
                    self.assertFalse(result['physical_balance_qualified'])
                    OBSERVATIONS.append(dict(control='synthetic_all8_full370_three_zone_ledger',
                        case_profile=case, H=H, nz=nz, orientation=orientation,
                        mu=mu, cell_relative=error, shared_face_absolute=0.,
                        physical_axial_incoming_absolute=0.))

    def test_selected_groups_independent_150cm_three_layer_analytic_crossing(self):
        H, nz, mu = 150., 3, .5
        widths, regions = np.array([400.]), np.array([0])
        total = np.zeros((8, nz, 3))
        total[0] = np.array([[.007, .014, .021], [0., .003, 0.], [.023, .011, .004]])
        q = np.zeros((8*nz, 3)); q[:nz] = np.array([[.004, -.002, .003],
            [.008, .001, -.004], [.002, .006, .001]])
        radial = np.zeros((6*nz, 3)); axial = np.full((8, 3), .6)
        result = transport_multigroup(LIB, widths, regions, total, 0, H, nz,
                                     mu, 1, 32, q, radial, axial)
        maximum = 0.
        for c in range(3):
            ref = ZonalRectangleReference(widths, regions, total[:, :, c], 0,
                H, nz, mu, 1, q[:, c:c+1], radial[:, c:c+1], axial[:, c:c+1])
            # u=-20 enters the bottom at s=40 and exits the top at s=340.
            # Three independent length100 recurrences include a void layer.
            trace = ref.ray(-20., full=True); incoming = .6
            for layer in range(nz):
                length, sigma, source = H/(nz*mu), total[0, layer, c], q[layer, c]
                t = np.exp(-sigma*length)
                b = length if sigma == 0 else -np.expm1(-sigma*length)/sigma
                d = length*length/2 if sigma == 0 else (length-b)/sigma
                integral, out = b*incoming+d*source, t*incoming+b*source
                np.testing.assert_allclose(trace[layer, 0, 0], integral, rtol=5e-12, atol=1e-14)
                np.testing.assert_allclose(trace[layer, 8, 0], out, rtol=5e-12, atol=1e-14)
                incoming = out
            exact = ref.fixed(64, full=True)
            scale = max(float(abs(exact).max()), 1e-100)
            error = float(abs(result['fields'][:, :, c:c+1]-exact).max()/scale)
            self.assertLess(error, 5e-12); maximum = max(maximum, error)
        self.ledger(result, widths, regions, H, nz)
        OBSERVATIONS.append(dict(control='independent_rectangle_and_literal_three_layer_ray',
            synthetic_group_columns=3, H=H, physical_zone_edges_cm=[0, 50, 100, 150],
            relative=maximum, void_layer_retained=True, signed_source_retained=True))

    def test_signed_superposition_with_distinct_group_totals(self):
        nz, H = 3, 150.; total, q, radial, axial = fixture(nz, 7, 'ABA')
        widths, regions = np.array([.3, .4, .2]), np.array([0, 2, 0])
        q *= -1.; radial *= -1.; axial[:] = -.2
        a = transport_multigroup(LIB, widths, regions, total, 2, H, nz,
                                 -.61, -1, 32, q, radial, axial)
        q2, r2, a2 = q[::-1].copy()*.7, radial[::-1].copy()*.3, axial.copy()*.5
        b = transport_multigroup(LIB, widths, regions, total, 2, H, nz,
                                 -.61, -1, 32, q2, r2, a2)
        mix = transport_multigroup(LIB, widths, regions, total, 2, H, nz,
            -.61, -1, 32, -.7*q+1.3*q2, -.7*radial+1.3*r2, -.7*axial+1.3*a2)
        target = -.7*a['fields']+1.3*b['fields']
        np.testing.assert_allclose(mix['fields'], target, rtol=5e-12, atol=1e-14)
        self.assertLess(float(a['fields'].min()), 0.)
        self.ledger(mix, widths, regions, H, nz)
        OBSERVATIONS.append(dict(control='signed_no_clipping_linear_superposition',
            minimum_field=float(a['fields'].min()),
            absolute=float(abs(mix['fields']-target).max())))

    def test_void_constant_signed_inflow_all_cell_and_face_fields(self):
        nz, H, mu, orientation = 3, 150., -.61, -1
        widths, regions = np.array([.13, .7, .29]), np.array([0, 1, 0])
        amplitude = np.array([-1., 0., .25, 1., 2.])
        total, q = np.zeros((8, nz, 5)), np.zeros((8*nz, 5))
        radial = np.repeat(amplitude[None, :], 6*nz, axis=0)
        axial = np.repeat(amplitude[None, :], 8, axis=0)
        result = transport_multigroup(LIB, widths, regions, total, 0, H, nz,
                                     mu, orientation, 32, q, radial, axial)
        expected = np.zeros_like(result['fields'])
        expected[:, 0] = np.repeat(widths, nz)[:, None]*(H/nz)*amplitude
        expected[:, 2] = expected[:, 5] = (H/nz)*amplitude
        expected[:, 4] = expected[:, 7] = abs(mu)*np.repeat(widths, nz)[:, None]*amplitude
        np.testing.assert_allclose(result['fields'], expected, rtol=5e-12, atol=1e-14)
        np.testing.assert_array_equal(result['fields'][:, :, 1], np.zeros_like(expected[:, :, 1]))
        self.ledger(result, widths, regions, H, nz)
        OBSERVATIONS.append(dict(control='void_analytic_signed_constant_all_faces',
            absolute=float(abs(result['fields']-expected).max()), zero_column_absolute=0.))

    def test_invalid_shapes_nonfinite_and_matched_inflow_rejected(self):
        total, q, radial, axial = fixture(3, 3, 'ABA')
        arguments = [LIB, [.3], [0], total, 0, 150., 3, .5, 1, 16, q, radial, axial]
        bad_inputs = [(3, np.ones((8, 3))), (3, total.transpose(2, 1, 0)),
            (3, -np.ones_like(total)), (3, np.full_like(total, np.nan)),
            (10, np.zeros((24, 0))), (10, np.zeros((24, 371))),
            (10, np.zeros((3, 24))), (11, np.zeros((6, 3))),
            (12, np.zeros((3, 8))), (2, [.5]), (2, [8]), (1, [0.]),
            (6, 2.5), (7, 1.), (8, 0), (9, 1)]
        for index in (10, 11, 12):
            bad = arguments[index].copy(); bad[-1, -1] = np.inf
            bad_inputs.append((index, bad))
        for index, value in bad_inputs:
            trial = arguments.copy(); trial[index] = value
            with self.assertRaises(ValueError): transport_multigroup(*trial)
        with self.assertRaises(TypeError):
            transport_multigroup(*arguments, matched_reference=np.ones((1, 3)))
        OBSERVATIONS.append(dict(control='complete_input_rejection',
                                 invalid_cases=len(bad_inputs)+1))


if __name__ == '__main__':
    started = time.perf_counter()
    result = unittest.main(exit=False).result
    with ARGS.report.open('x') as stream:
        json.dump(dict(schema='LAYERED_MULTIGROUP_COMPONENT_CONTROLS_V1',
            component_only=True, synthetic_fixtures_only=True,
            full_reference_qualified=False, coupled_370group_reference_qualified=False,
            physical_balance_qualified=False, scientific_accuracy_qualified=False,
            actual_A_B_input_qualified=False, AAA_qualified=False, ABA_admitted=False,
            tests_run=result.testsRun, passed=result.wasSuccessful(),
            failures=[str(name) for name, _ in result.failures],
            errors=[str(name) for name, _ in result.errors],
            observations=OBSERVATIONS, elapsed_seconds=time.perf_counter()-started),
            stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')
    sys.exit(0 if result.wasSuccessful() else 1)

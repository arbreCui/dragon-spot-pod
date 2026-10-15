"""Independent literal flights and full-coordinate/white-return controls."""
import unittest
import numpy as np
from scipy.integrate import quad
from test_native_signed_axial import fixture
from qualify_native_signed_axial import signed_sweep, moments
from exact_native_flight import green_sweep, evaluate, compare, ratio


def literal(d, a, q, inflow, fractions):
    """Small-fixture direct physical source flights; coefficients by quadrature."""
    nr, nb, nc = d['nr'], d['nb'], q.shape[-1]
    integrals = np.zeros((2, d['nmu'], nr, nc)); boundary = np.zeros((2, d['nmu'], nb, nc))
    for z in range(2):
        for orientation in [1, -1]:
            for line in range(len(d['track'])):
                n = d['length'][line]; p = d['polar'][line]
                entry = 0 if orientation == 1 else n-1; exit_ = n-1 if orientation == 1 else 0
                inc = inflow[z, p, -d['region'][line, entry]-1].copy()
                for i in range(1, n-1) if orientation == 1 else range(n-2, 0, -1):
                    r = d['region'][line, i]-1; total = a['total'][r]
                    for fraction in fractions if orientation == 1 else fractions[::-1]:
                        h = d['h'][line, i]*fraction; t = np.exp(-total*h)
                        b = quad(lambda x: np.exp(-total*x), 0, h)[0]
                        own = quad(lambda x: (h-x)*np.exp(-total*x), 0, h)[0]
                        integrals[z, p, r] += (b*inc+own*q[z, p, r])*d['weight'][line]/2
                        inc = t*inc+b*q[z, p, r]
                boundary[z, p, -d['region'][line, exit_]-1] += inc*d['weight'][line]/2
    return integrals, boundary


class ExactFlightTests(unittest.TestCase):
    def inputs(self, d):
        q = np.arange(1., 13.).reshape(2, 1, 2, 3); q[..., 2] *= -1
        inc = np.arange(12., 24.).reshape(2, 1, 2, 3)/10; inc[..., 2] *= -1
        return q, inc

    def test_native_green_recovers_literal_all_source_coordinates(self):
        d, a = fixture(); q, inc = self.inputs(d)
        g = green_sweep(d, a, native=True, chunk=1); f = evaluate(d, a, g, q, inc)
        old = signed_sweep(d, a, q, inc, batch=1)
        for k in ['iso', 'own', 'boundary']: np.testing.assert_allclose(f[k], old[k], rtol=3e-15)
        p, j, o = moments(d, old['iso']+old['own'], old['boundary'])
        for k, v in [('phi', p), ('jz', j), ('outgoing', o)]: np.testing.assert_allclose(f[k], v, rtol=4e-15)

    def test_all_partitions_against_independent_quadrature_flights(self):
        d, a = fixture(); q, inc = self.inputs(d)
        for fractions in [(1.,), (.5, .5), (.25,)*4, (.125,)*8, (1/3, 2/3)]:
            f = evaluate(d, a, green_sweep(d, a, fractions), q, inc)
            integral, boundary = literal(d, a, q, inc, fractions)
            np.testing.assert_allclose(f['iso']+f['own'], integral, rtol=5e-15)
            np.testing.assert_allclose(f['boundary'], boundary, rtol=5e-15)

    def test_partition_preserves_original_segment_source_isolation(self):
        d, a = fixture(); q, inc = self.inputs(d)
        whole = evaluate(d, a, green_sweep(d, a), q, inc)
        split = evaluate(d, a, green_sweep(d, a, (.125,)*8), q, inc)
        for k in ['iso', 'own', 'boundary', 'phi', 'jx', 'jz']:
            np.testing.assert_allclose(split[k], whole[k], rtol=6e-15, atol=2e-15)

    def test_positive_basis_and_signed_controls_are_not_clipped(self):
        d, a = fixture(); g = green_sweep(d, a, (.5, .5)); q, inc = self.inputs(d)
        f = evaluate(d, a, g, q, inc)
        self.assertGreaterEqual(g['track_minimum_angle'].min(), 0.)
        self.assertGreaterEqual(g['track_minimum_integral'].min(), 0.)
        self.assertTrue(np.all(f['phi'][:, 2] < 0))

    def test_piece_track_and_directional_ledgers(self):
        d, a = fixture(); g = green_sweep(d, a, (1/3, 2/3)); q, inc = self.inputs(d)
        f = evaluate(d, a, g, q, inc)
        self.assertLess(ratio(g['track_defect'], g['track_scale']).max(), 2e-15)
        self.assertLess(g['track_maximum_local_balance'].max(), 2e-15)
        self.assertLess(max(f['even_relative'].max(), f['odd_relative'].max()), 2e-15)

    def test_common_white_inverse_recloses_actual_directional_flights(self):
        d, a = fixture(); g = green_sweep(d, a)
        bc = np.broadcast_to(np.eye(2), (2, 1, 2, 2)).copy()
        f = evaluate(d, a, g, np.zeros_like(bc), bc); tbb = f['outgoing']
        inverse = np.linalg.solve(np.eye(2)-tbb, np.eye(2)); self.assertGreaterEqual(inverse.min(), 0.)
        q = np.ones((2, 1, 2, 1)); q[0] += .2; q[1] -= .2
        v = evaluate(d, a, g, q, np.zeros_like(q)); common = inverse@v['outgoing']
        white = evaluate(d, a, g, q, np.broadcast_to(common, (2, 1, 2, 1)))
        np.testing.assert_allclose(white['outgoing'], common, rtol=3e-15)
        np.testing.assert_allclose(white['jz'], v['jz'], rtol=5e-15)

    def test_void_path_and_induced_zero_current_scale(self):
        d, a = fixture(); a['total'][:] = 0
        q = np.ones((2, 1, 2, 1)); inc = np.zeros_like(q)
        f = evaluate(d, a, green_sweep(d, a), q, inc)
        np.testing.assert_array_equal(f['jz'], 0.)
        metrics = compare(d, f, f)
        self.assertFalse(metrics['jz_net_relative_valid'][0])
        np.testing.assert_array_equal(metrics['jz_weighted_induced_relative'], 0.)
        with self.assertRaises(ValueError): green_sweep(d, a, (.5,), native=False)

    def test_weighted_geometry_ledger_uses_polar_measures(self):
        d, a = fixture(); q, inc = self.inputs(d)
        f = evaluate(d, a, green_sweep(d, a), q, inc)
        np.testing.assert_allclose(f['stored_volume_birth'], f['even_birth'], rtol=2e-15)
        np.testing.assert_allclose(f['stored_surface_incoming'], f['even_incoming'], rtol=2e-15)


if __name__ == '__main__': unittest.main()

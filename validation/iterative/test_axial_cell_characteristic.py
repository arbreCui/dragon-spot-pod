"""Independent characteristic equations, limits and source-response controls."""
import unittest
import numpy as np
from scipy.integrate import quad
from axial_cell_characteristic import coefficients, assemble, solve, diagnostics, unit_inputs
from analytic_axial_slab import analytic_cell_averages, analytic_points


def expanded_solve(widths, total, scattering, mu, source, incoming, periodic=False):
    """Independent 3n+2 face/mean equations; integrals from quadrature."""
    n = len(widths); matrix = np.zeros((3*n+2, 3*n+2)); rhs = np.zeros(3*n+2)
    minus = n+1; scalar = 2*n+2
    matrix[0, 0] = 1; matrix[1, minus+n] = 1
    if periodic:
        matrix[0, n] = -1; matrix[1, minus] = -1
    else:
        rhs[:2] = incoming
    for i, h in enumerate(widths):
        length = h/mu; t = np.exp(-total[i]*length)
        b = quad(lambda s: np.exp(-total[i]*s), 0, length, epsabs=1e-13)[0]
        d = quad(lambda s: (length-s)*np.exp(-total[i]*s), 0, length, epsabs=1e-13)[0]
        p, m, a = 2+3*i, 3+3*i, 4+3*i
        matrix[p, i+1] = 1; matrix[p, i] = -t; matrix[p, scalar+i] = -b*scattering[i]
        matrix[m, minus+i] = 1; matrix[m, minus+i+1] = -t; matrix[m, scalar+i] = -b*scattering[i]
        rhs[p] = b*source[0, i]; rhs[m] = b*source[1, i]
        matrix[a, scalar+i] = 1-d*scattering[i]/length
        matrix[a, i] = -b/(2*length); matrix[a, minus+i+1] = -b/(2*length)
        rhs[a] = d*source[:, i].sum()/(2*length)
    x = np.linalg.solve(matrix, rhs)
    return x[scalar:], np.stack([x[:n+1], x[minus:scalar]])


class CharacteristicTests(unittest.TestCase):
    mu = 1/np.sqrt(3)

    def test_integrals_independent_quadrature_thin_void_thick(self):
        for tau in [0., 1e-16, 1e-10, .01, .499, .501, 1., 10., 1000.]:
            t, b, d = coefficients(3., tau/3)
            qb = 3*quad(lambda u: np.exp(-tau*u), 0, 1, epsabs=1e-13)[0]
            qd = 9*quad(lambda u: (1-u)*np.exp(-tau*u), 0, 1, epsabs=1e-13)[0]
            np.testing.assert_allclose([b, d], [qb, qd], rtol=4e-14, atol=0)
            self.assertGreaterEqual(float(t), 0.)

    def test_segment_identities_and_local_denominator(self):
        length = np.logspace(-14, 3, 100); total = 2.
        t, b, d = coefficients(length, total)
        np.testing.assert_allclose(t+total*b, 1., rtol=4e-16)
        np.testing.assert_allclose((b+total*d)/length, 1., rtol=4e-16)
        self.assertGreater(float(np.min(1-total*d/length)), 0.)

    def test_expanded_face_equations_nonuniform_heterogeneous(self):
        h = np.array([.03, .2, 1., 3., .7]); t = np.array([0., .2, 2., .4, .03]); s = t*np.array([0., .9, 1., .3, .99])
        q = np.array([[1., 0., 2., .3, 0.], [0., .5, 0., 1., 2.]])
        incoming = np.array([.4, 1.3]); system = assemble(h, t, s, self.mu)
        f = solve(system, q[:, :, None], incoming[:, None])
        p, faces = expanded_solve(h, t, s, self.mu, q, incoming)
        np.testing.assert_allclose(f['phi'][:, 0], p, rtol=2e-13)
        np.testing.assert_allclose(f['faces'][:, :, 0], faces, rtol=2e-13, atol=1e-14)

    def test_expanded_periodic_face_equations(self):
        h = np.array([.2, 1., 3.]); t = np.array([.2, 2., .4]); s = .8*t
        q = np.array([[1., 0., .2], [0., .3, 1.]])
        f = solve(assemble(h, t, s, self.mu, True), q[:, :, None], np.zeros((2, 1)))
        p, faces = expanded_solve(h, t, s, self.mu, q, np.zeros(2), True)
        np.testing.assert_allclose(f['phi'][:, 0], p, rtol=2e-13)
        np.testing.assert_allclose(f['faces'][:, :, 0], faces, rtol=2e-13)

    def test_pure_absorption_exact_means_and_faces(self):
        edges = np.array([0., .001, .08, 1., 7., 12., 20.]); h = np.diff(edges)
        for total in [.02, .2, 2.]:
            f = solve(assemble(h, total, 0., self.mu), np.ones((2, len(h), 1)), np.zeros((2, 1)))
            phi, current, angular = analytic_cell_averages(edges, total, 0., 20., self.mu)
            np.testing.assert_allclose(f['angular'][:, :, 0], angular, rtol=5e-12, atol=3e-14)
            expected = -np.expm1(-total*np.stack([edges, 20-edges])/self.mu)/total
            np.testing.assert_allclose(f['faces'][:, :, 0], expected, rtol=3e-15, atol=0)

    def test_void_exact_directional_linear_solution(self):
        h = np.array([.01, .4, 3., 6.]); z = np.r_[0., np.cumsum(h)]; mid = (z[1:]+z[:-1])/2
        f = solve(assemble(h, 0., 0., self.mu), np.ones((2, len(h), 1)), np.array([[2.], [3.]]))
        expected = np.stack([2.+mid/self.mu, 3.+(z[-1]-mid)/self.mu])
        np.testing.assert_allclose(f['angular'][:, :, 0], expected, rtol=3e-15)

    def test_periodic_constant_mode(self):
        for n in [1, 7, 32]:
            for total, fraction in [(.02, 0.), (.2, .9), (2., .99)]:
                f = solve(assemble(np.full(n, 20/n), total, total*fraction, self.mu, True), np.ones((2, n, 1)), np.zeros((2, 1)))
                np.testing.assert_allclose(f['angular'], 1/(total*(1-fraction)), rtol=5e-12)
                np.testing.assert_allclose(f['faces'], 1/(total*(1-fraction)), rtol=5e-12)

    def test_conservative_periodic_positive_source_is_rejected(self):
        for total in [0., .02, .2, 2.]:
            with self.assertRaisesRegex(ValueError, 'integrated balance'):
                assemble(np.ones(4), total, total, self.mu, True)

    def test_all_independent_unit_sources_positive_and_conservative(self):
        h = np.array([.02, .1, 1., 3., .5]); total = np.array([0., .2, 2., .4, .03])
        system = assemble(h, total, total, self.mu); f = solve(system, *unit_inputs(len(h)))
        row, _ = diagnostics(system, f)
        self.assertGreaterEqual(f['angular'].min(), 0.)
        self.assertGreaterEqual(f['faces'].min(), 0.)
        self.assertLess(row['raw_global_balance_relative'].max(), 1e-12)
        self.assertLess(row['even_cell_balance_relative'].max(), 1e-12)
        self.assertLess(row['odd_cell_balance_relative'].max(), 1e-12)

    def test_directional_mirror_symmetry_with_asymmetric_sources(self):
        h = np.array([.02, .1, 1., 3., .5]); total = np.array([0., .2, 2., .4, .03])
        q = np.arange(10.).reshape(2, 5, 1); incoming = np.array([[.3], [.7]])
        f = solve(assemble(h, total, .9*total, self.mu), q, incoming)
        g = solve(assemble(h[::-1], total[::-1], .9*total[::-1], self.mu), q[::-1, ::-1], incoming[::-1])
        np.testing.assert_allclose(f['angular'], g['angular'][::-1, ::-1], rtol=3e-14)
        np.testing.assert_allclose(f['faces'], g['faces'][::-1, ::-1], rtol=3e-14)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): coefficients(0., 1.)
        with self.assertRaises(ValueError): assemble([1.], 1., 1.1, self.mu)
        with self.assertRaises(ValueError): assemble([1.], 1., .5, 0.)
        with self.assertRaises(ValueError): solve(assemble([1.], 1., .5, self.mu), np.ones((1, 1)), np.ones((2, 1)))


if __name__ == '__main__': unittest.main()

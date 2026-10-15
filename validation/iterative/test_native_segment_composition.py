"""Mathematical composition, direction, precision-limit and failure controls."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from native_segment_composition import (read_native, exact_coefficients, input_patterns,
                                       flight, preservation, scaled_error)


class CompositionTests(unittest.TestCase):
    def test_exact_integrals_against_quadrature(self):
        for tau in [0., 1e-12, 1e-6, .001, .7, 10., 100.]:
            t, b, d = exact_coefficients(1., tau)
            reference = [np.exp(-tau), quad(lambda x: np.exp(-tau*x), 0, 1)[0],
                         quad(lambda x: (1-x)*np.exp(-tau*x), 0, 1)[0]]
            np.testing.assert_allclose([t, b, d], reference, rtol=2e-14)

    def test_exact_partition_and_matrix_all_declared_optical_controls(self):
        total = np.array([0., 1e-12, 1e-6, .001, .7, 10., 100.])
        for fractions in [[.5]*2, [.25]*4, [.125]*8, [1/3, 2/3]]:
            length = np.broadcast_to(fractions, (len(total), len(fractions)))
            kernel = exact_coefficients(length, total[:, None])
            for reverse in [False, True]:
                f = flight(length, total[:, None], kernel, *input_patterns(len(fractions)), reverse=reverse)
                self.assertLess(preservation(f, exact_coefficients(np.ones(len(total)), total), np.ones(len(total))).max(), 5e-12)
                self.assertLess(f['global_balance_relative'].max(), 1e-10)
                self.assertLess(f['matrix_integral_relative'].max(), 5e-12)
                self.assertGreaterEqual(f['minimum_angle'].min(), 0.)

    def test_heterogeneous_matrix_direct_calibration(self):
        lengths = np.array([[.1, .8, .3], [.01, 2., .7]])
        total = np.array([[0., .2, 3.], [1., .03, 2.]])
        for reverse in [False, True]:
            f = flight(lengths, total, exact_coefficients(lengths, total), *input_patterns(3), reverse=reverse)
            self.assertLess(f['matrix_outgoing_relative'].max(), 1e-14)
            self.assertLess(f['matrix_integral_relative'].max(), 1e-14)
            self.assertLess(f['global_balance_relative'].max(), 1e-14)

    def test_reversing_order_preserves_physical_source_index(self):
        lengths = np.array([[.2, .8]]); total = np.ones_like(lengths)
        kernel = exact_coefficients(lengths, total); f = flight(lengths, total, kernel, *input_patterns(2))
        g = flight(lengths, total, kernel, *input_patterns(2), reverse=True)
        self.assertAlmostEqual(f['outgoing'][0, 2], kernel[0, 0, 1]*kernel[0, 1, 0])
        self.assertAlmostEqual(g['outgoing'][0, 2], kernel[0, 0, 1])
        self.assertGreater(g['outgoing'][0, 2], f['outgoing'][0, 2])

    def test_native_recurrence_retains_signed_negative_output(self):
        lengths = np.array([[1.]])
        kernel = np.array([[[-.2, 1.2, .5]]])
        f = flight(lengths, np.array([[1.]]), kernel, *input_patterns(1), native=True)
        self.assertLess(f['outgoing'][0, 0], 0.)
        self.assertLess(f['minimum_angle'].min(), 0.)

    def test_changed_own_source_integral_is_not_reconstructed_from_balance(self):
        lengths = np.array([[.5, .5]]); total = np.ones_like(lengths)
        exact = exact_coefficients(lengths, total); changed = exact.copy(); changed[:, :, 2] *= 1.01
        f = flight(lengths, total, changed, *input_patterns(2), native=True)
        g = flight(lengths, total, exact, *input_patterns(2), native=True)
        np.testing.assert_array_equal(f['outgoing'], g['outgoing'])
        self.assertGreater(f['integral'][0, 1], g['integral'][0, 1])
        self.assertGreater(f['global_defect'][0, 1], 0.)
        self.assertGreater(preservation(f, exact_coefficients(np.array([1.]), np.array([1.])), np.array([1.])).max(), 1e-3)

    def test_void_integral_and_local_balance(self):
        lengths = np.array([[.2, .8]]); total = np.zeros_like(lengths)
        f = flight(lengths, total, exact_coefficients(lengths, total), *input_patterns(2), trace=True)
        np.testing.assert_allclose(f['outgoing'][0, :2], [1., 1.], rtol=0, atol=1e-15)
        np.testing.assert_allclose(f['integral'][0, :2], [1., .5], rtol=0, atol=1e-15)
        self.assertLess(f['maximum_local_balance_relative'].max(), 1e-14)
        self.assertEqual(f['trace'].shape, (1, 2, 5, 4))

    def test_augmented_map_source_superposition(self):
        lengths = np.array([[.3, .4, .7]])
        f = flight(lengths, np.ones_like(lengths), exact_coefficients(lengths, 1.), *input_patterns(3))
        for key in ['outgoing', 'integral']:
            np.testing.assert_allclose(f[key][:, 1], f[key][:, 2:5].sum(axis=1), rtol=2e-15)

    def test_zero_scale_is_exact_not_a_floor(self):
        np.testing.assert_array_equal(scaled_error([0., 1.], [0., 2.]), [0., .5])
        self.assertTrue(np.isinf(scaled_error([1.], [0.]))[0])

    def test_binary_protocol_shape_and_invalid_header(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/'probe.bin'; values = np.arange(36.).reshape(2, 6, 3)
            with p.open('wb') as f:
                np.array([290930, 2, 6], dtype='<i4').tofile(f); values.astype('<f8').tofile(f)
            np.testing.assert_array_equal(read_native(p), values)
            p.write_bytes(b'bad')
            with self.assertRaises(ValueError): read_native(p)


if __name__ == '__main__': unittest.main()

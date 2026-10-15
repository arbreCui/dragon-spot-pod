"""Small operator qualification checks. Requires NumPy; never invokes Dragon."""
from fractions import Fraction as Q
import unittest

import numpy as np

from qualify_coupled_reference import Slab, jacobian
from qualify_coupled_reference_extended import (
    cases, complex_jacobian, direct_reference, exact_one_cell,
    solve_ratio, boundary_root_diagnostic,
)


class HeterogeneousReferenceQualification(unittest.TestCase):
    def test_one_group_residual_and_derivatives_match_previous_exact_model(self):
        network = cases()[0]
        slab = Slab(2, Q(2))
        x = slab.positive_family(Q(1, 4))
        x[0] += Q(1, 100); x[7] -= Q(1, 200); x[-1] += Q(1, 10)
        for model in ("ratio", "explicit_exchange"):
            residual, j = jacobian(slab, x, model)
            observed = network.residual(np.array(x, dtype=float), model)
            np.testing.assert_allclose(observed, np.array(residual, dtype=float), atol=1e-14, rtol=0)
            np.testing.assert_allclose(complex_jacobian(network, np.array(x, dtype=float), model),
                                       np.array(j, dtype=float), atol=1e-13, rtol=0)

    def test_group_transfer_and_radial_exchange_conserve_neutron_balance(self):
        for network in cases():
            x, _ = direct_reference(network)
            x *= np.linspace(0.85, 1.15, len(x))  # Deliberately off-solution.
            for model in ("ratio", "explicit_exchange"):
                b = network.balance(x, model)
                self.assertAlmostEqual(sum(network.angular_residual(x, model)),
                                       b["closed_equation_balance_defect"], places=13)
                if model == "explicit_exchange":
                    self.assertAlmostEqual(b["net_transverse_term"], 0, places=14)

    def test_all_explicit_references_are_positive_normalized_regular_and_balanced(self):
        for network in cases():
            with self.subTest(case=network.name):
                x, _ = direct_reference(network)
                self.assertTrue(network.positive(x))
                _, plus, minus, phi, _, _ = network.fields(x)
                self.assertTrue(np.all(plus[:, :, 0] == 0))
                self.assertTrue(np.all(minus[:, :, -1] == 0))
                self.assertAlmostEqual(float(np.sum(network.nuf*phi)), 1, places=13)
                self.assertLess(np.max(np.abs(network.residual(x, "explicit_exchange"))), 1e-12)
                self.assertLess(abs(network.balance(x, "explicit_exchange")["relative_physical_balance_defect"]), 1e-12)
                singular = np.linalg.svd(complex_jacobian(network, x, "explicit_exchange"), compute_uv=False)
                self.assertGreater(singular[-1]/singular[0], 1e-3)

    def test_asymmetric_two_group_exact_family_and_independent_linear_reference(self):
        network = cases()[3]
        exact = exact_one_cell(network)
        self.assertEqual(exact["explicit_exchange_rank"], network.unknowns)
        x, _ = direct_reference(network)
        np.testing.assert_allclose(x, [float(Q(v)) for v in exact["explicit_exchange_state"]], atol=2e-14, rtol=0)
        for row in exact["family"]:
            self.assertEqual(Q(row["k"]), Q(7797115, 27866694))
            self.assertEqual(row["jacobian_rank"], network.unknowns-1)
            self.assertEqual(set(row["residual"]), {"0"})
            self.assertEqual(len(row["nullspace"]), 1)
            state = np.array([float(Q(v)) for v in row["state"]])
            np.testing.assert_allclose(complex_jacobian(network, state),
                                       [[float(Q(v)) for v in j] for j in row["jacobian"]], atol=2e-14, rtol=0)
            if row["reflector_scale"] != "1":
                self.assertNotEqual(Q(row["balance"]["physical_balance_defect"]), 0)

    def test_heterogeneous_multigroup_jacobian_against_central_differences(self):
        network = cases()[-1]
        x, _ = direct_reference(network)
        x *= np.linspace(0.95, 1.05, len(x))
        step = 1e-6
        for model in ("ratio", "explicit_exchange"):
            j = complex_jacobian(network, x, model)
            for col in range(len(x)):
                plus, minus = x.copy(), x.copy()
                plus[col] += step; minus[col] -= step
                derivative = (network.residual(plus, model)-network.residual(minus, model))/(2*step)
                np.testing.assert_allclose(derivative, j[:, col], atol=2e-8, rtol=0)

    def test_axial_material_variation_retains_a_positive_amplitude_family(self):
        network = cases()[1]
        ref, _ = direct_reference(network)
        x, status, _ = solve_ratio(network, ref)
        self.assertEqual(status, "RESIDUAL_MET")
        leakage = network.fields(x)[4]
        for scale in (0.5, 2.0):
            trial = x.copy(); trial[2*network.radial_size:-1] *= scale
            self.assertTrue(network.positive(trial))
            self.assertLess(np.max(np.abs(network.residual(trial))), 1e-12)
            np.testing.assert_allclose(network.fields(trial)[4], leakage, atol=1e-13, rtol=0)
            self.assertGreater(abs(network.balance(trial, "ratio")["relative_physical_balance_defect"]), 0.05)

    def test_full_rank_residual_stops_can_approach_an_inadmissible_boundary(self):
        for network in (cases()[2], cases()[4], cases()[5]):
            with self.subTest(case=network.name):
                ref, _ = direct_reference(network)
                x, status, _ = solve_ratio(network, ref)
                self.assertEqual(status, "RESIDUAL_MET")
                self.assertLess(np.max(network.fields(x)[3][:, 1, :]), 1e-7)
                boundary = boundary_root_diagnostic(network, x)
                zero_state = np.array(boundary["state"])
                self.assertFalse(boundary["admissible_active_domain"])
                self.assertFalse(network.positive(zero_state))
                self.assertTrue(np.all(network.fields(zero_state)[3][:, 1, :] == 0))
                self.assertGreater(boundary["minimum_radial_flux"], 0.01)
                self.assertLess(boundary["max_abs_residual"], 1e-13)
                self.assertEqual(set(boundary["rank_at_relative_threshold"].values()), {network.unknowns})
                self.assertGreater(abs(boundary["balance"]["relative_physical_balance_defect"]), 0.1)
                np.testing.assert_allclose(x, zero_state, atol=1e-7, rtol=0)

    def test_invalid_materials_and_nonpositive_seeds_are_rejected(self):
        from dataclasses import replace
        network = cases()[3]
        with self.assertRaises(ValueError):
            replace(network, total=np.zeros_like(network.total))
        ref, _ = direct_reference(network)
        ref[2*network.radial_size] = 0
        with self.assertRaises(ValueError):
            solve_ratio(network, ref)


if __name__ == "__main__":
    unittest.main(verbosity=2)

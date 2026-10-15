"""Weighted exchange/Galerkin verification; standalone NumPy, no production runs."""
from dataclasses import replace
import unittest

import numpy as np

from qualify_coupled_reference_extended import cases as previous_cases
from qualify_exchange_projection import (
    networks, snapshots, spaces, lifts, projected_eigenpair, run,
)


class ExchangeProjectionQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.networks = networks()
        cls.results = run()

    def test_original_six_operators_and_references_are_recovered(self):
        for net, old, record in zip(self.networks, previous_cases(), self.results["cases"]):
            angular = np.linspace(.05, .9, net.size)
            x = np.ones(old.unknowns); x[old.radial_size:-1] = angular; x[-1] = 1.7
            np.testing.assert_allclose(net.residual(angular, 1.7),
                                       old.angular_residual(x, "explicit_exchange"), atol=1e-14, rtol=0)
            self.assertLess(record["previous_reference_recovery"]["absolute_k_error"], 1e-12)
            self.assertLess(record["previous_reference_recovery"]["max_angular_error"], 1e-12)

    def test_nonuniform_weights_conserve_transfer_and_global_balance_off_solution(self):
        for net in self.networks[-2:]:
            angular = np.linspace(.05, .9, net.size)
            for matrix in net.transfer.reshape(-1, net.regions, net.regions):
                np.testing.assert_allclose(net.weights@matrix, 0, atol=1e-14, rtol=0)
                # An unweighted sum is not the correct balance for these volumes.
                self.assertGreater(np.linalg.norm(np.ones(net.regions)@matrix), .01)
            balance = net.balance(angular, 1.7)
            self.assertAlmostEqual(net.row_weights()@net.residual(angular, 1.7),
                                   balance["physical_balance_defect"]+balance["net_radial_transfer"], places=12)

    def test_snapshots_have_one_global_normalization_and_independent_sources(self):
        for net in self.networks:
            training, receipts = snapshots(net)
            self.assertTrue(np.all(training > 0))
            for col, row in enumerate(receipts):
                self.assertLess(row["max_fixed_source_residual"], 1e-12)
                self.assertAlmostEqual(row["source_integral"], 1, places=14)
                self.assertAlmostEqual(float(np.sum(net.weights[:, None]*net.nuf[row["plane"]]*training[:, :, col])), 1, places=13)
            families, _ = spaces(net, training)
            for bases in families.values():
                for b in bases:
                    np.testing.assert_allclose(b.T@(net.weights[:, None]*b), np.eye(net.regions), atol=3e-13, rtol=0)

    def test_constant_test_space_represents_the_balance_functional(self):
        for net in self.networks[-2:]:
            training, _ = snapshots(net)
            families, _ = spaces(net, training)
            basis = [b[:, :2] for b in families["constant_enriched_pod"]]
            _, q = lifts(net, basis)
            coefficients = np.linalg.lstsq(q, np.ones(net.size), rcond=None)[0]
            np.testing.assert_allclose(q@coefficients, 1, atol=1e-13, rtol=0)
            arbitrary_residual = np.linspace(-.2, .7, net.size)
            self.assertAlmostEqual(net.row_weights()@arbitrary_residual,
                                   coefficients@(q.T@(net.row_weights()*arbitrary_residual)), places=12)

    def test_all_full_spaces_and_nonorthogonal_coordinates_recover_reference(self):
        for record in self.results["cases"]:
            entries = [a for a in record["approximations"] if a["radial_rank_per_group"] == record["regions"]]
            entries.append(record["nonorthogonal_full_control"])
            for entry in entries:
                self.assertLess(abs(entry["k"]-record["reference"]["k"]), 1e-12)
                self.assertLess(entry["normalized_weighted_flux_error"], 2e-11)
                self.assertLess(entry["max_full_local_residual"], 1e-11)

    def test_nonorthogonal_reduced_coordinates_preserve_the_physical_solution(self):
        for net in self.networks[-2:]:
            loss, birth = net.operators()
            training, _ = snapshots(net); families, _ = spaces(net, training)
            for complete in families.values():
                basis = [b[:, :2] for b in complete]
                changed = [b@np.array([[2., .3], [0., .5]]) for b in basis]
                original = projected_eigenpair(net, loss, birth, basis)
                reexpressed = projected_eigenpair(net, loss, birth, changed)
                np.testing.assert_allclose(original[0], reexpressed[0], atol=2e-12, rtol=0)
                self.assertAlmostEqual(original[1], reexpressed[1], places=12)

    def test_projected_residual_positivity_and_enriched_conservation(self):
        self.assertEqual(sum(len(c["approximations"]) for c in self.results["cases"]), 40)
        for record in self.results["cases"]:
            for entry in record["approximations"]:
                self.assertLess(entry["max_projected_residual"], 1e-11)
                self.assertTrue(entry["positive_scalar"])
                self.assertTrue(entry["positive_nonvacuum_angular"])
                self.assertLess(abs(entry["weighted_residual_balance_identity_error"]), 1e-12)
                if entry["family"] == "constant_enriched_pod":
                    self.assertLess(abs(entry["balance"]["relative_physical_balance_defect"]), 1e-11)
                    self.assertLess(max(entry["constant_space_defect_by_group"]), 1e-12)

    def test_conservation_accuracy_and_projection_residual_are_distinct(self):
        record = self.results["cases"][-1]
        entries = {(a["family"], a["radial_rank_per_group"]): a for a in record["approximations"]}
        plain = entries["plain_pod", 3]
        coarse = entries["constant_enriched_pod", 1]
        enriched = entries["constant_enriched_pod", 3]
        self.assertLess(plain["normalized_weighted_flux_error"], .001)
        self.assertGreater(abs(plain["balance"]["relative_physical_balance_defect"]), 1e-5)
        self.assertGreater(coarse["normalized_weighted_flux_error"], .5)
        self.assertLess(abs(coarse["balance"]["relative_physical_balance_defect"]), 1e-11)
        self.assertLess(enriched["normalized_weighted_flux_error"], .002)
        self.assertLess(abs(enriched["balance"]["relative_physical_balance_defect"]), 1e-11)
        self.assertGreater(enriched["max_full_local_residual"], 1e-5)

    def test_invalid_exchange_and_dependent_spaces_are_rejected(self):
        net = self.networks[-1]
        bad = net.transfer.copy(); bad[0, 0, 0, 0] += .1
        with self.assertRaises(ValueError):
            replace(net, transfer=bad)
        with self.assertRaises(ValueError):
            replace(net, weights=-net.weights)
        with self.assertRaises(ValueError):
            lifts(net, [np.ones((net.regions, 2)) for _ in range(net.groups)])


if __name__ == "__main__":
    unittest.main(verbosity=2)

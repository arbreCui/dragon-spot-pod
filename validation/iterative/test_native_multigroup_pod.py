"""Standalone independent algebra and archived native multigroup checks."""
import json
from pathlib import Path
import unittest

import numpy as np

from qualify_native_multigroup_pod import (
    bases, diagnostics, full_operator, lift, load_data, projected_operator,
    project_source, scatter_action,
)


class SmallOperatorTests(unittest.TestCase):
    def setUp(self):
        self.h = np.array([[[3., -.4, -.1], [-.2, 2., -.1], [-.1, -.3, 2.5]],
                           [[2., -.1, -.2], [-.3, 3., -.1], [-.2, -.1, 2.8]]])
        self.s = np.array([[[.4, .3, .2], [.07, .09, .06]],
                           [[.12, .13, .15], [.2, .4, .3]]])
        self.v = np.array([1., 2., 3.])
        self.b = np.array([[[1., .2], [.3, 1.], [.5, -.4]],
                           [[.9, .3], [.2, 1.1], [.6, -.2]]])

    def test_destination_source_order_and_single_self_term(self):
        scatter = np.array([[[.2, .4], [.3, .5]], [[.7, .6], [.1, .2]]])
        phi = np.array([[2., 3.], [5., 7.]])
        np.testing.assert_allclose(scatter_action(scatter, phi), [[1.9, 4.7], [1.9, 3.2]], atol=1e-15)

    def test_projected_blocks_match_explicit_global_projection(self):
        ng, nr, rank = self.b.shape
        p = np.zeros((ng*nr, ng*rank))
        for g in range(ng):
            p[g*nr:(g+1)*nr, g*rank:(g+1)*rank] = self.b[g]
        a = full_operator(self.h, self.s, .137)
        expected = p.T @ (np.tile(self.v, ng)[:, None] * a) @ p
        actual = projected_operator(self.h, self.s, self.v, self.b, .137)
        np.testing.assert_allclose(actual, expected, rtol=1e-14, atol=1e-14)

    def test_nonorthogonal_mass_is_retained(self):
        difference = projected_operator(self.h, self.s, self.v, self.b, 1) - projected_operator(self.h, self.s, self.v, self.b, 0)
        expected = np.zeros((4, 4))
        for g in range(2):
            expected[2*g:2*g+2, 2*g:2*g+2] = self.b[g].T @ (self.v[:, None] * self.b[g])
        np.testing.assert_allclose(difference, expected, atol=1e-14)
        self.assertGreater(np.linalg.norm(expected - np.eye(4)), 1)

    def test_oblique_coordinates_preserve_physical_field(self):
        q = np.arange(1, 7, dtype=float).reshape(2, 3)
        change = np.array([[1.7, .2], [0., .8]])
        fields = []
        for b in (self.b, self.b @ change):
            reduced = np.linalg.solve(projected_operator(self.h, self.s, self.v, b, .04), project_source(self.v, b, q))
            fields.append(lift(b, reduced))
        np.testing.assert_allclose(*fields, atol=2e-15, rtol=2e-15)

    def test_constant_projection_does_not_erase_native_balance_defect(self):
        b = np.ones((2, 3, 1))
        q = np.arange(1, 7, dtype=float).reshape(2, 3)
        phi = lift(b, np.linalg.solve(projected_operator(self.h, self.s, self.v, b), project_source(self.v, b, q)))
        d = {"v": self.v, "scatter": self.s, "total_r": np.full((2, 3), 2.)}
        result = diagnostics(d, self.h, phi, q, 0)
        self.assertLess(abs(result["weighted_operator_residual"]), 2e-14)
        self.assertGreater(abs(result["raw_collision_scattering_leakage_balance"]), .1)
        self.assertLess(abs(result["balance_identity_error"]), 2e-14)

    def test_weighted_training_basis_spans_constant_and_full_space(self):
        samples = np.random.default_rng(8401).normal(size=(9, 2, 3))
        plain, enriched, _ = bases(samples, self.v)
        for family in (plain, enriched):
            for b in family:
                np.testing.assert_allclose(b.T @ (self.v[:, None]*b), np.eye(3), atol=1e-14)
        for b in enriched:
            c = b[:, :1]
            np.testing.assert_allclose(c @ (c.T @ self.v), np.ones(3), atol=1e-14)


class NativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = Path(__file__).resolve().parent.parent / "artifacts/native-multigroup-pod-20260928"
        if not cls.a.is_dir():
            cls.a = Path(__file__).resolve().parent.parent
        cls.result = json.loads((cls.a / "analysis/result.json").read_text())
        cls.data = load_data(cls.a / "analysis/data.bin")

    def test_legacy_leakage_applied_once_and_signed_data_retained(self):
        d = self.data
        for g in range(370):
            np.testing.assert_array_equal(d["scatter"][g, g], d["used_r"][g])
        np.testing.assert_array_equal(d["used"][1:], d["physical"][1:] - d["leak"])
        self.assertTrue(np.any(d["scatter"] < 0))
        self.assertTrue(np.any(d["physical_r"] - d["used_r"] != d["leak"][:, None]))

    def test_saved_transport_correction_reconciles_macro_and_system(self):
        correction = np.fromfile(self.a / "runs/tranc.bin", dtype="<f4").reshape(370, 8).T
        d = self.data
        np.testing.assert_array_equal(d["total"][1:], d["macro_total"] - correction)
        np.testing.assert_array_equal(d["physical"][1:], d["sigw"] - correction)

    def test_full_references_and_fresh_native_sources(self):
        self.assertEqual(len(self.result["references"]), 4)
        for r in self.result["references"]:
            self.assertGreater(r["minimum_flux"], 0)
            self.assertLess(r["full_residual_relative"], 1e-10)
        for r in self.result["native_replays"]:
            self.assertLess(r["matrix_vs_fresh_native_relative"], 5e-10)
            if "fixed_source_relative" in r:
                self.assertLess(r["fixed_source_relative"], 5e-10)
                self.assertLess(r["fixed_source_max_group_relative"], 5e-10)
        self.assertLess(self.result["metrics"]["max_source_constructor_relative"], 5e-12)

    def test_full_spaces_and_oblique_coordinates_recover_reference(self):
        self.assertEqual(len(self.result["projection"]), 64)
        for r in self.result["projection"]:
            self.assertLess(r["projected_residual_relative"], 1e-10)
            if r["rank"] == 8:
                self.assertLess(r["relative_flux_l2"], 1e-9)
        for r in self.result["coordinate_checks"]:
            self.assertLess(r["relative_flux"], 1e-9)

    def test_conservation_and_positivity_remain_separate(self):
        fields = np.load(self.a / "analysis/projection_fields.npz")["reduced_fields"]
        for r, phi in zip(self.result["projection"], fields):
            self.assertEqual(r["negative_flux_count"], int(np.sum(phi < 0)))
            if r["family"] == "constant_enriched":
                self.assertLess(abs(r["weighted_operator_residual"]), 1e-10)
            self.assertAlmostEqual(r["raw_collision_scattering_leakage_balance"],
                                   r["weighted_operator_residual"] - r["native_radial_balance_defect"], places=12)
        self.assertTrue(any(r["negative_flux_count"] > 0 for r in self.result["projection"]))


if __name__ == "__main__":
    unittest.main()

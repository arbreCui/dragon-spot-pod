"""Standalone algebra and saved-native evidence tests (NumPy required)."""
import json
from pathlib import Path
import unittest

import numpy as np

from qualify_native_radial_response import (
    BOUNDARIES, GROUPS, NR, close_boundary, current_balance, load_metadata,
    load_runs, prescribed_sources, relative,
)


class BoundaryAlgebraTests(unittest.TestCase):
    def test_elimination_matches_joint_equations_with_noncommuting_return(self):
        t = np.array([[.3, .1, .2, .05], [.1, .4, .08, .15],
                      [.2, .03, .1, .25], [.04, .15, .05, .3]])
        b = np.array([[0, .7], [.2, 0]])
        q = np.array([1.2, -.3])
        # Unknowns are phi1, phi2, jout1, jout2, jin1, jin2.
        joint = np.zeros((6, 6))
        joint[:4, :4] = np.eye(4)
        joint[:4, 4:] = -t[:, 2:]
        joint[4:, 2:4] = -b
        joint[4:, 4:] = np.eye(2)
        full = np.linalg.solve(joint, np.r_[t[:, :2] @ q, np.zeros(2)])
        r, j = close_boundary(t, b, 2)
        np.testing.assert_allclose(np.r_[r @ q, j @ q, b @ j @ q], full, atol=1e-15)

    def test_vacuum_keeps_outgoing_current_without_return(self):
        t = np.arange(1, 17, dtype=float).reshape(4, 4) / 40
        r, j = close_boundary(t, np.zeros((2, 2)), 2)
        np.testing.assert_array_equal(r, t[:2, :2])
        np.testing.assert_array_equal(j, t[2:, :2])

    def test_balance_uses_net_boundary_current_and_unequal_weights(self):
        ledger = current_balance(np.array([3., 4., .2, .4]),
                                 np.array([2., 2., 1.2, 1.]),
                                 np.array([2., 1., 3., 5.]), np.array([.5, 1.]), 2)
        self.assertAlmostEqual(ledger["signed_defect"], 0, places=14)
        self.assertAlmostEqual(ledger["net_outflow"], 6)
        self.assertAlmostEqual(ledger["total_collision"], 4)
        self.assertAlmostEqual(ledger["outgoing_current"], 8.6)

    def test_signed_zero_integrated_source_has_defined_balance_scale(self):
        ledger = current_balance(np.array([1., -2., 0.]), np.array([0., 0., 1.]),
                                 np.array([2., 1., 1.]), np.array([1., 1.]), 2)
        self.assertEqual(ledger["volume_source"], 0)
        self.assertEqual(ledger["relative_to_volume_source"], .25)

    def test_sources_have_one_absolute_volume_normalization(self):
        w = np.arange(1, NR + 1, dtype=float)
        q = prescribed_sources(w)
        for source in q.values():
            self.assertAlmostEqual(w @ abs(source), 1)
        self.assertTrue(np.any(q["signed_perturbation"] < 0))
        self.assertTrue(np.all(q["positive_ramp"] > 0))


class SavedNativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = Path(__file__).resolve().parent.parent / "artifacts/native-radial-response-20260928"
        # Archived tests live in artifact/inputs; use the containing artifact.
        if not cls.artifact.is_dir():
            cls.artifact = Path(__file__).resolve().parent.parent
        cls.result = json.loads((cls.artifact / "analysis/result.json").read_text())

    def test_independent_native_probes_recover_matrix_action(self):
        runs = load_runs(self.artifact / "runs/flight.csv")
        self.assertEqual(len(runs), 54)
        for g in self.result["groups"]:
            t = np.array(g["flight_matrix"])
            cases = [r for (group, _), r in runs.items() if group == g["group"]]
            for s, y in cases[14:]:
                self.assertLess(relative(t @ s, y), 5e-12)

    def test_closed_sources_checked_by_fresh_native_calls(self):
        runs = load_runs(self.artifact / "runs/closed.csv")
        meta = load_metadata(self.artifact / "runs/closed_metadata.csv")
        self.assertEqual(len(runs), 45)
        self.assertEqual(len(self.result["closure_cases"]), len(GROUPS) * len(BOUNDARIES))
        for c in self.result["closure_cases"]:
            b = np.array(c["boundary_matrix"])
            for p in c["source_cases"]:
                s, y = runs[c["group"], p["probe"]]
                self.assertLess(relative(y, np.array(p["expected_response"])), 5e-12)
                np.testing.assert_allclose(s[NR:], b @ y[NR:], atol=1e-12, rtol=5e-12)
                m = meta[c["group"]]
                ledger = current_balance(s, y, m["weight"], m["total"][:NR], NR)
                self.assertLess(ledger["relative_to_all_inflow"], 1e-6)
                if p["source_name"] != "signed_perturbation":
                    self.assertTrue(np.all(y[:NR] > 0))

    def test_no_rebalance_or_diagonal_repair_hidden_in_evidence(self):
        # Raw native defects are retained, not rounded to a manufactured zero.
        self.assertGreater(self.result["metrics"]["max_raw_current_balance_relative"], 0)
        for c in self.result["closure_cases"]:
            h, radial = np.array(c["loss_operator"]), np.array(c["radial_operator"])
            m = next(g["metadata"] for g in self.result["groups"] if g["group"] == c["group"])
            np.testing.assert_array_equal(radial, h - np.diag(m["total"][:NR]))
            anchor = c["source_cases"][0]
            self.assertLess(anchor["diagonal_flux_relative"], 1e-12)
            ramp = c["source_cases"][1]
            q = np.array(ramp["source"])
            diagonal_phi = q / np.array(c["anchor_diagonal"])
            self.assertGreater(relative(h @ diagonal_phi, q), 5e-12)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Synthetic-only tests for the diagnostic comparator; no production CE run."""
import copy
import csv
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

import compare_d4a_pin_rates as comparator


def fixture():
    bins = []
    for floor in (1, 2, 3):
        for pin in range(217):
            mean = float(2 * floor + pin % 13) if (floor, pin) != (1, 0) else 0.0
            bins.append({"floor": floor, "pin_index": pin, "ring_from_center": 0 if pin == 216 else 8,
                         "fuel_cell_id": (floor - 1) * 217 + pin + 1,
                         "nu_fission": mean, "nu_fission_std_dev": mean / 10,
                         "global_fraction": 0.0})
    total = math.fsum(row["nu_fission"] for row in bins)
    for row in bins:
        row["global_fraction"] = row["nu_fission"] / total
    ce = {"schema": "D4A_CORRECTED_CE_RESULT_V1", "keff": 1.03,
          "keff_standard_deviation": 0.0001, "global_nu_fission": total,
          "floor_nu_fission_fractions": [
              math.fsum(row["nu_fission"] for row in bins if row["floor"] == floor) / total
              for floor in (1, 2, 3)], "bins": bins}
    spot = [{"floor": row["floor"], "pin_index": row["pin_index"],
             "nu_fission_rate": row["nu_fission"], "global_fraction": row["global_fraction"]}
            for row in bins]
    return spot, ce


class SyntheticComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="d4a_compare_synthetic_")
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name)
        self.spot, self.ce = fixture()

    def compare(self):
        spot_path, ce_path = self.path / "pin_rates.csv", self.path / "reference_result.json"
        with spot_path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(self.spot[0]))
            writer.writeheader()
            writer.writerows(self.spot)
        ce_path.write_text(json.dumps(self.ce))
        return comparator.compare(spot_path, ce_path)

    def test_complete_identity_with_independent_row_shuffles_and_zero_bin(self):
        random.Random(11).shuffle(self.spot)
        random.Random(22).shuffle(self.ce["bins"])
        rows, summary = self.compare()
        self.assertEqual(len(rows), 651)
        self.assertEqual([(row["floor"], row["pin_index"]) for row in rows], sorted(comparator.KEYS))
        self.assertEqual(summary["maximum_absolute_difference"], 0.0)
        self.assertEqual(summary["rms_difference"], 0.0)
        self.assertEqual(summary["status"], "DIAGNOSTIC_ONLY")
        self.assertEqual(summary["accuracy_assessment"], "REPORTED_ONLY")

    def test_known_difference_is_reported_without_repair(self):
        row = self.spot[100]
        row["global_fraction"] = 0.75
        rows, summary = self.compare()
        expected = 0.75 - self.ce["bins"][100]["global_fraction"]
        self.assertEqual(summary["maximum_absolute_difference"], expected)
        self.assertEqual(summary["maximum_absolute_difference_position"], {"floor": 1, "pin_index": 100})
        self.assertEqual(rows[100]["spot_global_fraction"], 0.75)
        self.assertGreater(summary["spot_global_fraction_sum"], 1.0)

    def test_raw_standard_deviation_is_not_fraction_sigma(self):
        _, before = self.compare()
        for row in self.ce["bins"]:
            row["nu_fission_std_dev"] = 1e100
        rows, after = self.compare()
        self.assertEqual(before["maximum_absolute_difference"], after["maximum_absolute_difference"])
        self.assertNotIn("sigma", rows[0])
        self.assertIn("covariance is unavailable", after["uncertainty"])

    def test_missing_spot_id_is_rejected(self):
        self.spot.pop()
        with self.assertRaisesRegex(ValueError, "SPOT must cover"):
            self.compare()

    def test_duplicate_spot_id_is_rejected(self):
        self.spot[-1] = copy.deepcopy(self.spot[0])
        with self.assertRaisesRegex(ValueError, "duplicate SPOT"):
            self.compare()

    def test_missing_ce_id_is_rejected(self):
        self.ce["bins"].pop()
        with self.assertRaisesRegex(ValueError, "CE must cover"):
            self.compare()

    def test_duplicate_ce_id_is_rejected(self):
        self.ce["bins"][-1]["floor"] = 1
        self.ce["bins"][-1]["pin_index"] = 0
        with self.assertRaisesRegex(ValueError, "duplicate CE"):
            self.compare()

    def test_wrong_total_is_rejected(self):
        self.ce["global_nu_fission"] *= 2
        for row in self.ce["bins"]:
            row["global_fraction"] = row["nu_fission"] / self.ce["global_nu_fission"]
        with self.assertRaisesRegex(ValueError, "global_nu_fission disagrees"):
            self.compare()

    def test_one_ulp_changed_bin_fraction_is_rejected_without_epsilon(self):
        row = self.ce["bins"][100]
        row["global_fraction"] = math.nextafter(row["global_fraction"], math.inf)
        with self.assertRaisesRegex(ValueError, "bin global_fraction disagrees"):
            self.compare()

    def test_wrong_floor_fraction_is_rejected(self):
        self.ce["floor_nu_fission_fractions"][0] = 0.0
        with self.assertRaisesRegex(ValueError, "floor fraction disagrees"):
            self.compare()

    def test_nonfinite_and_negative_inputs_are_rejected(self):
        for field, value in (("nu_fission_rate", math.inf), ("global_fraction", -1.0)):
            with self.subTest(field=field, value=value):
                self.spot, self.ce = fixture()
                self.spot[10][field] = value
                with self.assertRaisesRegex(ValueError, "nonfinite or negative"):
                    self.compare()
        self.spot, self.ce = fixture()
        self.ce["bins"][10]["nu_fission_std_dev"] = float("nan")
        with self.assertRaisesRegex(ValueError, "nonfinite JSON"):
            self.compare()

    def test_invalid_schema_is_rejected(self):
        self.ce["schema"] = "UNRELATED"
        with self.assertRaisesRegex(ValueError, "wrong CE schema"):
            self.compare()

    def test_noninteger_ce_id_is_rejected(self):
        self.ce["bins"][10]["pin_index"] = 10.0
        with self.assertRaisesRegex(ValueError, "noninteger"):
            self.compare()

    def test_cli_writes_diagnostics_and_refuses_overwrite(self):
        self.compare()
        output = self.path / "comparison"
        command = [sys.executable, str(Path(comparator.__file__)),
                   str(self.path / "pin_rates.csv"), str(self.path / "reference_result.json"), str(output)]
        result = subprocess.run(command, timeout=10, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DIAGNOSTIC_ONLY / REPORTED_ONLY", result.stdout)
        summary_path = output / "comparison_summary.json"
        original = summary_path.read_bytes()
        summary = json.loads(original)
        self.assertEqual(summary["rows"], 651)
        with (output / "pin_comparison.csv").open(newline="") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 651)
        result = subprocess.run(command, timeout=10, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(summary_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Small synthetic tests of the diagnostic orbit-to-pin expansion."""

import copy
import csv
import math
from pathlib import Path
import tempfile
import unittest

from expand_d4a_pin_rates import expand


class ExpansionTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.pins, self.rates = [], []
        pin = 0
        for region, count in zip(range(4, 125, 5), [12] * 12 + [6] * 12 + [1]):
            for _ in range(count):
                self.pins.append(dict(radial_region=region, pin_index=pin,
                                      x_index=pin, alpha_index=0,
                                      orbit_multiplicity=count,
                                      orbit_area=float(count), per_pin_area=1.0))
                pin += 1
            for floor in (1, 2, 3):
                factor = 2 if floor == 2 else 1
                self.rates.append(dict(radial_region=region, floor=floor,
                                       material=4 + 6 * (floor - 1), volume=50.0 * count,
                                       nu_fission_rate=float(count * factor),
                                       global_fraction=count * factor / 868.0))

    def tearDown(self):
        self.temporary.cleanup()

    def check(self, pins, rates):
        paths = (self.root / "pins.csv", self.root / "rates.csv")
        for path, records in zip(paths, (pins, rates)):
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
        return expand(*paths)

    def test_conservation_and_no_renormalization(self):
        output, summary = self.check(self.pins, self.rates)
        self.assertEqual(len(output), 651)
        self.assertEqual(summary["status"], "DIAGNOSTIC_ONLY")
        for row in output:
            factor = 2 if row["floor"] == 2 else 1
            self.assertEqual(row["nu_fission_rate"], factor)
            self.assertEqual(row["volume"], 50.0)
        self.assertEqual(math.fsum(row["global_fraction"] for row in output), 1.0)
        for check in summary["conservation"]:
            self.assertLessEqual(check["absolute_difference"], check["division_roundoff_bound"])

    def test_input_scale_is_preserved(self):
        rates = copy.deepcopy(self.rates)
        for row in rates:
            row["nu_fission_rate"] *= 2
            row["global_fraction"] *= 2
        output, summary = self.check(self.pins, rates)
        self.assertEqual(summary["global_fraction_sum"], 2.0)
        for row in output:
            self.assertEqual(row["nu_fission_rate"], 4 if row["floor"] == 2 else 2)

    def test_bad_inputs_refused(self):
        cases = [
            ("pins", 1, "pin_index", 0),
            ("pins", 1, "x_index", 0),
            ("pins", 0, "orbit_multiplicity", 6),
            ("pins", 0, "per_pin_area", 12.0),
            ("pins", 0, "orbit_area", 13.0),
            ("rates", 0, "radial_region", 1),
            ("rates", 0, "floor", 2),
            ("rates", 0, "material", 2),
            ("rates", 0, "volume", 601.0),
            ("rates", 0, "nu_fission_rate", -1.0),
            ("rates", 0, "global_fraction", "nan"),
        ]
        for which, index, key, value in cases:
            with self.subTest(which=which, key=key):
                pins, rates = copy.deepcopy(self.pins), copy.deepcopy(self.rates)
                (pins if which == "pins" else rates)[index][key] = value
                with self.assertRaises(ValueError):
                    self.check(pins, rates)
        with self.assertRaises(ValueError):
            self.check(self.pins[:-1], self.rates)
        with self.assertRaises(ValueError):
            self.check(self.pins, self.rates[:-1])


if __name__ == "__main__":
    unittest.main()

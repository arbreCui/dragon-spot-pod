#!/usr/bin/env python3
"""Bounded static positive/negative checks; no tracking or transport."""
import argparse
import copy
from pathlib import Path
import unittest

import build_d4a_pin_crosswalk as crosswalk

FIXTURE = None


class AdmissionTests(unittest.TestCase):
    def test_outside_resolution_is_rejected(self):
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "0 admitted"):
            crosswalk.unique_lattice_center(1.0, 0.0, {(0, 0): {"sal_x": 0.0, "sal_y": 0.0}}, 1e-5)

    def test_ambiguous_admission_is_rejected(self):
        candidates = {(0, 0): {"sal_x": 0.0, "sal_y": 0.0},
                      (1, 0): {"sal_x": 0.0, "sal_y": 0.0}}
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "2 admitted"):
            crosswalk.unique_lattice_center(0.0, 0.0, candidates, 1e-5)

    def test_modified_geometry_source_is_rejected(self):
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "hash mismatch"):
            crosswalk.reference_and_resolution(Path(__file__))


class SavedTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if FIXTURE is None:
            raise unittest.SkipTest("pass --geometry-export for saved-XSM fixture tests")
        cls.snapshot = crosswalk.read_saved(FIXTURE)
        cls.reference, cls.resolution = crosswalk.reference_and_resolution()

    def build(self, snapshot):
        return crosswalk.build_crosswalk(snapshot, self.reference, self.resolution)

    def test_real_saved_geometry(self):
        rows, checks = self.build(self.snapshot)
        self.assertEqual(len(rows), 217)
        self.assertEqual(len({r["pin_index"] for r in rows}), 217)
        self.assertEqual(len({r["radial_region"] for r in rows}), 25)
        self.assertEqual(checks["track_fuel_orbit_area_sum"], checks["expanded_pin_area_sum"])
        self.assertTrue(checks["independent_surface_area_reproduces_track_real32"])

    def test_moved_saved_center_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        for index, part in enumerate(snapshot["elements"]):
            if part[1] == 2 and snapshot["regions"][part[2]][0] == 4:
                changed = list(part)
                changed[4] += 2 * self.resolution
                snapshot["elements"][index] = tuple(changed)
                break
        else:
            self.fail("fixture has no full-circle fuel boundary")
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "0 admitted"):
            self.build(snapshot)

    def test_missing_arc_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        for index, part in enumerate(snapshot["elements"]):
            if part[1] == 3 and snapshot["regions"][part[2]][0] == 4:
                del snapshot["elements"][index]
                break
        with self.assertRaises(crosswalk.CrosswalkFailure):
            self.build(snapshot)

    def test_duplicate_circle_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        for part in snapshot["elements"]:
            if part[1] == 2 and snapshot["regions"][part[2]][0] == 4:
                snapshot["elements"].append(part)
                break
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "duplicate full circle"):
            self.build(snapshot)

    def test_spurious_times_twelve_area_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        for region, values in snapshot["regions"].items():
            if values[0] == 4:
                material, merge, area, node, merged = values
                snapshot["regions"][region] = (material, merge, 12 * area, node, merged)
        with self.assertRaisesRegex(crosswalk.CrosswalkFailure, "independent saved-boundary area"):
            self.build(snapshot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-export", type=Path)
    args, remainder = parser.parse_known_args()
    FIXTURE = args.geometry_export
    unittest.main(argv=[__file__, *remainder])

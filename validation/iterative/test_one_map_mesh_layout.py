#!/usr/bin/env python3
"""TEST ONLY: seconds-scale synthetic layout checks, never physical map evidence.

Builds the actual read-only checker and this fixture in a temporary directory,
using existing Ganlib only. No Dragon/SPOT build, transport, archived input, or
runtime executable is used or modified. Run directly with Python unittest.
"""

from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import time
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FLAGS = ("-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror "
         "-Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math").split()
FILES = ("basis.xsm", "system.xsm", "previous.xsm", "current.xsm", "snapshots.xsm")


class OneMapMeshLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.started = time.monotonic()
        compiler = shutil.which("gfortran")
        ganlib = ROOT / "Ganlib/lib" / f"{platform.system()}_{platform.machine()}"
        if not compiler or not (ganlib / "libGanlib.a").is_file():
            raise unittest.SkipTest("gfortran and an existing Ganlib build are required")
        cls.temporary = tempfile.TemporaryDirectory(prefix="one-map-mesh-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.work = Path(cls.temporary.name)
        cls.checker = cls.work / "checker"
        cls.fixture = cls.work / "fixture"
        for source, output in (("check_one_map_xsm.f90", cls.checker),
                               ("one_map_mesh_fixture.f90", cls.fixture)):
            result = subprocess.run(
                [compiler, *FLAGS, "-I", str(ganlib / "modules"), str(HERE / source),
                 str(ganlib / "libGanlib.a"), "-lstdc++", "-o", str(output)],
                cwd=cls.work, timeout=20, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)

    def run_case(self, mutation, route="reencoded", expected=None, directions=False):
        # Each mutation gets a fresh directory; short relative XSM arguments
        # also respect Ganlib's 72-character object-name limit.
        self.assertLess(time.monotonic() - self.started, 55, "synthetic suite exceeded time budget")
        with tempfile.TemporaryDirectory(prefix="case-", dir=self.work) as temporary:
            case = Path(temporary)
            fixture = subprocess.run([str(self.fixture), mutation, route], cwd=case,
                                     timeout=5, capture_output=True, text=True)
            self.assertEqual(fixture.returncode, 0, fixture.stdout + fixture.stderr)
            self.assertIn("TEST ONLY SYNTHETIC", fixture.stdout)
            before = {path.name: path.read_bytes() for path in case.glob("*.xsm")}
            arguments = (["--directions", "previous.xsm", "current.xsm", "third.xsm"]
                         if directions else ["--" + route, *FILES])
            result = subprocess.run([str(self.checker), *arguments], cwd=case,
                                    timeout=5, capture_output=True, text=True)
            output = result.stdout + result.stderr
            after = {path.name: path.read_bytes() for path in case.glob("*.xsm")}
            self.assertEqual(before, after, "read-only checker changed an XSM fixture")
            if expected is None:
                self.assertEqual(result.returncode, 0, output)
                self.assertIn("PICARD-DIRECTION COMPLETE" if directions else "ONE-MAP-XSM COMPLETE", output)
            else:
                self.assertNotEqual(result.returncode, 0, output)
                self.assertIn(expected, output)
                self.assertNotIn("ONE-MAP-XSM COMPLETE", output)

    def test_valid_layouts(self):
        for route in ("reencoded", "continued"):
            for mutation in ("good", "same_size", "no_flux64"):
                with self.subTest(route=route, mutation=mutation):
                    self.run_case(mutation, route)

    def test_axial_dimensions_must_match_current_system(self):
        for route in ("reencoded", "continued"):
            for mutation in ("old_parent", "current_mismatch", "system_mismatch",
                             "previous_zero", "previous_negative", "current_zero", "current_negative"):
                with self.subTest(route=route, mutation=mutation):
                    self.run_case(mutation, route, "MAP AXIAL STORAGE DIMENSIONS DIFFER")

    def test_system_dimensions_are_positive_and_other_state_entries_fixed(self):
        for mutation in ("reference_zero", "reference_negative", "system_zero", "system_negative"):
            with self.subTest(mutation=mutation):
                self.run_case(mutation, expected="INVALID SPOD STATE-VECTOR")
        for mutation in ("state_1", "state_40"):
            with self.subTest(mutation=mutation):
                self.run_case(mutation, expected="SYSTEM STATE-VECTOR RECORDS DIFFER")

    def test_basis_still_bitwise_fixed(self):
        self.run_case("basis_bit", expected="GROUP 370 POD-BASIS RECORDS DIFFER BITWISE")

    def test_raw_flux_lists_are_validated_on_both_states(self):
        for owner in ("previous", "current"):
            for record in ("flux", "flux64"):
                for mutation in ("length", "type", "groups", "record"):
                    with self.subTest(owner=owner, record=record, mutation=mutation):
                        diagnostic = (owner.upper() + " STATE " + record.upper() +
                                      " LIST ITEM CONTRACT FAILED" if mutation in ("length", "type")
                                      else owner.upper() + " STATE INVALID RECORD " + record.upper())
                        # Item mutations are exclusively at group 370, not group 1.
                        self.run_case(f"{owner}_{record}_{mutation}", expected=diagnostic)
            self.run_case(f"{owner}_flux_missing", expected="INVALID RECORD FLUX")
            self.run_case(f"{owner}_flux64_directory", expected="INVALID RECORD FLUX64")

    def test_lying_parent_dimensions_do_not_hide_coarse_flux(self):
        self.run_case("forged_parent", expected="PREVIOUS STATE FLUX LIST ITEM CONTRACT FAILED")

    def test_directions_only_need_canonical_records(self):
        self.run_case("directions", route="continued", directions=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)

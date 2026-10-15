#!/usr/bin/env python3
"""Standalone-copy/replay/export tests with synthetic XSM and fake checkers.

Reuse the small repaired-lineage fixtures. No Dragon or OpenMC solve is run.
Only private copies replace production epoch hashes for synthetic positives.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_d4a_repaired_acceptance as fixture


HERE = Path(__file__).resolve().parent
FREEZER = HERE / "freeze_d4a_corrected_map.sh"
EXPORTER = HERE / "export_d4a_corrected_result.py"
FULL_CHECK = (
    "ONE-MAP-XSM POD-PACKAGE BITWISE PASS\n"
    "ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS\n"
    "ONE-MAP-XSM RAW-RADIAL-POSITIVITY PASS\n"
    "ONE-MAP-XSM CANONICAL-LAYOUT BITWISE PASS\n"
    "ONE-MAP-XSM RAW-DEFECT BITWISE PASS\n"
    "ONE-MAP-XSM RESTART-ARCHIVE BITWISE PASS\nONE-MAP-XSM COMPLETE\n"
)
LINKS = {
    "parent_axial_closed.xsm": "closed_axial.xsm",
    "parent_snapshots_closed.xsm": "closed_snapshots.xsm",
    **{name: name for name in fixture.INPUTS[2:-1]},
}


def full_gate(met):
    return fixture.gate(met).replace("SPOT-GATE COMPLETE\n",
        "SPOT-GATE DLEAK 0.0 NOT-GATED\n"
        f"GATE=(Rrho,RL,Ra) ALL <= 5.0e-7 : {'MET' if met else 'NOT MET'}\n"
        "SPOT-GATE COMPLETE\n")


class RepairedPackagingTest(unittest.TestCase):
    def setUp(self):
        self.case = fixture.RepairedAcceptanceTest()
        with patch.object(fixture, "CHECK_LOG", FULL_CHECK), patch.object(
            fixture, "RECORDS", fixture.RECORDS.replace("E+00\n", "E+00 |>0011\n")
        ):
            self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.root = self.case.root
        self.source = self.case.map1
        self.output = self.root / "portable"
        self.script = self.case.tools / FREEZER.name
        shutil.copy2(FREEZER, self.script)
        fixture.substitute_epoch_hashes(self.script, self.case.runtime, self.case.bootstrap)
        for name, target in LINKS.items():
            (self.source / name).unlink()
            (self.source / name).symlink_to(self.case.bootstrap / target)
        with (self.source / "prepare.log").open("a") as stream:
            stream.write("SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT\n")
        self.set_gate(True)
        # Match final observables to the now-complete synthetic state.
        self.case.set_observables(self.source)
        log = self.case.observables / "observables.log"
        log.write_text(log.read_text().replace("E+00\n", "E+00 |>0011\n"))
        fixture.seal(self.case.observables, "observables.sha256")
        self.environment = dict(os.environ, TEST_CHECKER_MARKER=str(self.case.check_marker),
                                TEST_DRAGON_MARKER=str(self.case.dragon_marker))

    def set_gate(self, met):
        for name in ("closed_axial.xsm", "gate.log"):
            (self.source / name).write_text(full_gate(met))
        self.case.seal_map(self.source)

    def run_freezer(self):
        result = subprocess.run(
            ["/bin/sh", str(self.script), "--repaired-runtime", str(self.case.runtime),
             str(self.case.bootstrap), str(self.source), str(self.output)],
            env=self.environment, capture_output=True, text=True, timeout=15)
        self.assertFalse(self.case.dragon_marker.exists(), "packaging launched Dragon")
        return result

    def packaged(self):
        result = self.run_freezer()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any(p.is_symlink() for p in self.output.rglob("*")))
        return self.output

    def refused(self):
        result = self.run_freezer()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.output.exists())
        return result

    def export(self, directory):
        return subprocess.run(
            [sys.executable, str(EXPORTER), str(directory), str(self.case.observables),
             str(self.root / "export")], capture_output=True, text=True, timeout=10)

    def test_copy_relocate_replay_and_export_with_originals_unavailable(self):
        before = {p: fixture.sha(p) for base in (self.source, self.case.bootstrap, self.case.runtime)
                  for p in base.rglob("*") if p.is_file()}
        original_receipt = (self.source / "result.sha256").read_bytes()
        self.packaged()
        self.assertEqual(before, {p: fixture.sha(p) for p in before})
        self.assertEqual((self.output / "source_result.sha256").read_bytes(), original_receipt)
        for name in LINKS:
            self.assertNotEqual((self.source / name).stat().st_ino, (self.output / name).stat().st_ino)
        moved = self.root / "moved-package"
        self.output.rename(moved)
        for original in (self.source, self.case.bootstrap, self.case.runtime):
            original.rename(original.with_name(original.name + "-unavailable"))
        for executable, arguments, log in (
            ("check_one_map_xsm", ["--reencoded", "basis_reference.xsm", "candidate_system.xsm",
              "parent_for_checker.xsm", "candidate_axial.xsm", "candidate_snapshots.xsm"], "independent_check.log"),
            ("check_convergence_gate", ["closed_axial.xsm"], "gate.log"),
        ):
            result = subprocess.run([str(moved / "runtime" / executable), *arguments], cwd=moved,
                env=self.environment, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, (moved / log).read_text())
        result = self.export(moved)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("map_source_result_receipt_sha256", (self.root / "export/result.json").read_text())

    def test_mesh12_copy_relocate_replay_and_export(self):
        fixture.substitute_epoch_hashes(self.script, self.case.runtime, self.case.bootstrap,
                                       "MESH12", "MESH12")
        self.test_copy_relocate_replay_and_export_with_originals_unavailable()

    def test_cross_epoch_pairs_are_refused_before_replay(self):
        for runtime_epoch, bootstrap_epoch in (("REPAIRED", "MESH12"), ("MESH12", "REPAIRED")):
            with self.subTest(runtime=runtime_epoch, bootstrap=bootstrap_epoch):
                fixture.substitute_epoch_hashes(self.script, self.case.runtime, self.case.bootstrap,
                                               runtime_epoch, bootstrap_epoch)
                result = self.refused()
                self.assertIn("repaired bootstrap identity differs", result.stderr)
                self.assertFalse(self.case.check_marker.exists())

    def test_mesh12_not_met_package_cannot_be_exported_as_final(self):
        fixture.substitute_epoch_hashes(self.script, self.case.runtime, self.case.bootstrap,
                                       "MESH12", "MESH12")
        self.test_not_met_package_cannot_be_exported_as_final()

    def test_mesh12_resealed_other_runtime_is_refused(self):
        fixture.substitute_epoch_hashes(self.script, self.case.runtime, self.case.bootstrap,
                                       "MESH12", "MESH12")
        (self.case.runtime / "check_one_map_xsm").write_text("bad checker\n")
        fixture.seal(self.case.runtime, "runtime.sha256")
        result = self.refused()
        self.assertIn("repaired runtime manifest identity differs", result.stderr)
        self.assertFalse(self.case.check_marker.exists())

    def test_not_met_package_cannot_be_exported_as_final(self):
        self.set_gate(False)
        self.packaged()
        role = (self.output / "portable_classification.txt").read_text()
        self.assertIn("NEXT_MAP_PARENT_ONLY", role)
        self.assertIn("FINAL_CONVERGENCE=NOT_CLAIMED", role)
        result = self.export(self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "export").exists())

    def test_production_freezer_rejects_synthetic_epoch(self):
        shutil.copy2(FREEZER, self.script)
        self.refused()

    def test_legacy_flat_packaging_entry_is_preserved(self):
        for name in ("check_one_map_xsm", "check_convergence_gate"):
            shutil.copy2(self.case.runtime / name, self.case.tools)
        names = ("d4a_seed_axial.xsm", "d4a_seed_snapshots.xsm", "initial_radial_track.bin",
                 "initial_axial_track.xsm", "initial_axial_macrolib.xsm", "basis_reference.xsm",
                 "route_contract.xsm", "d4a_refreshed_snapshots.xsm", "closed_axial.xsm",
                 "closed_snapshots.xsm", "d4a_axial_seed.log", "d4a_refresh_r64.log",
                 "route_contract.log", "b2i_bootstrap.log")
        for name in names:
            if not (self.case.bootstrap / name).exists():
                (self.case.bootstrap / name).write_text("synthetic legacy record\n")
        fixture.seal(self.case.bootstrap, "d4a_bootstrap_result.sha256", names)
        (self.source / "result.sha256").unlink()
        shutil.rmtree(self.source / "runtime")
        result = subprocess.run(["/bin/sh", str(self.script), str(self.case.bootstrap),
            str(self.source), str(self.output)], env=self.environment, capture_output=True,
            text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(all(p.is_file() and not p.is_symlink() for p in self.output.iterdir()))
        self.assertFalse(self.case.dragon_marker.exists())

    def test_unsealed_source_file_is_refused(self):
        (self.source / "extra.txt").write_text("unsealed\n")
        self.refused()

    def test_extra_empty_directory_is_refused(self):
        (self.source / "extra").mkdir()
        self.refused()

    def test_forged_saved_gate_is_refused_after_resealing(self):
        (self.source / "gate.log").write_text(full_gate(False))
        self.case.seal_map(self.source)
        self.refused()

    def test_resealed_wrong_fixed_input_is_refused(self):
        wrong = self.root / "wrong-track"
        wrong.write_text("wrong track\n")
        (self.source / "initial_axial_track.xsm").unlink()
        (self.source / "initial_axial_track.xsm").symlink_to(wrong)
        self.case.seal_map(self.source)
        self.refused()

    def test_destination_inside_input_is_refused_without_creating_parents(self):
        self.output = self.source / "new-parent" / "bad-output"
        self.refused()
        self.assertFalse((self.source / "new-parent").exists())

    def test_existing_output_is_not_modified(self):
        self.output.mkdir()
        marker = self.output / "keep"
        marker.write_text("unchanged\n")
        result = self.run_freezer()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(), "unchanged\n")

    def test_unsealed_nested_runtime_file_is_refused_by_exporter(self):
        self.packaged()
        (self.output / "runtime/extra.py").write_text("unsealed\n")
        self.assertNotEqual(self.export(self.output).returncode, 0)
        self.assertFalse((self.root / "export").exists())

    def test_resealed_extra_directory_is_refused_by_exporter(self):
        self.packaged()
        (self.output / "other").mkdir()
        (self.output / "other/file").write_text("unexpected nested data\n")
        fixture.seal(self.output, "result.sha256")
        self.assertNotEqual(self.export(self.output).returncode, 0)

    def test_missing_retained_source_receipt_is_refused_by_exporter(self):
        self.packaged()
        (self.output / "source_result.sha256").unlink()
        fixture.seal(self.output, "result.sha256")
        self.assertNotEqual(self.export(self.output).returncode, 0)


if __name__ == "__main__":
    unittest.main()

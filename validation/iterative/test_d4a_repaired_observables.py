#!/usr/bin/env python3
"""Transport-free tests of the repaired final-observables entry.

Positive fixtures substitute hashes only in a private copy of the shell
script and use a tiny fake executable. The production script is also tested
unchanged: it must reject that same synthetic runtime.
"""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from test_d4a_repaired_acceptance import substitute_epoch_hashes


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "run_d4a_corrected_final_observables.sh"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root, name, names):
    (root / name).write_text("".join(
        f"{digest(root / entry)}  {entry}\n" for entry in names))


class RepairedObservablesTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="d4a-repaired-observables-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.tools = self.root / "validation/iterative"
        self.tools.mkdir(parents=True)
        self.script = self.tools / SCRIPT.name
        shutil.copy2(SCRIPT, self.script)
        self.deck = self.tools / "d4a_corrected_final_observables.x2m"
        shutil.copy2(HERE / self.deck.name, self.deck)
        self.runtime = self.root / "runtime"
        self.runtime.mkdir()
        dragon = self.runtime / "Dragon"
        dragon.write_text(
            '#!/bin/sh\ncat >/dev/null\nprintf called > "$TEST_DRAGON_MARKER"\n'
            "printf '%s\\n' "
            "'>|D4A-CORRECTED-K-EFFECTIVE 1.234567890123456E+00' "
            "'SPORATE NU-FISSION-FRACTIONS 0.2 0.3 0.5' "
            "' normal end of execution for dragon'\n")
        dragon.chmod(0o755)
        shutil.copy2(HERE / "run_bounded_dragon.py", self.runtime)
        manifest(self.runtime, "runtime.sha256", ["Dragon", "run_bounded_dragon.py"])
        self.build = self.root / "bootstrap"
        self.build.mkdir()
        self.final = self.root / "final"
        self.final.mkdir()
        self.shared = ["basis_reference.xsm", "route_contract.xsm",
                       "initial_axial_track.xsm", "initial_axial_macrolib.xsm"]
        for name in self.shared:
            (self.build / name).write_text(f"synthetic {name}\n")
            shutil.copy2(self.build / name, self.final)
        manifest(self.build, "result.sha256", self.shared)
        (self.final / "closed_axial.xsm").write_text("synthetic final state\n")
        (self.final / "independent_check.log").write_text("ONE-MAP-XSM COMPLETE\n")
        self.write_gate("VALID_MET")
        manifest(self.final, "input_manifest.sha256", self.shared)
        manifest(self.final, "output_manifest.sha256", ["closed_axial.xsm"])
        shutil.copytree(self.runtime, self.final / "runtime")
        self.seal_final()
        # No real Dragon is present in these fixtures, even if launch guards fail.
        substitute_epoch_hashes(self.script, self.runtime, self.build)
        self.output = self.root / "observables"
        self.marker = self.root / "dragon-called"

    def write_gate(self, classification):
        (self.final / "gate.log").write_text(
            f"CLASSIFICATION={classification}\nSPOT-GATE COMPLETE\n" +
            "".join(f"SPOT-GATE {name} 1.0E-8 PASS \n"
                    for name in ("RRHO", "RLEAK", "RA")))

    def seal_final(self):
        names = [path.relative_to(self.final).as_posix()
                 for path in sorted(self.final.rglob("*"))
                 if path.is_file() and path != self.final / "result.sha256"]
        manifest(self.final, "result.sha256", names)

    def run_extract(self, **overrides):
        env = dict(os.environ, TIMEOUT_SECONDS="5",
                   TEST_DRAGON_MARKER=str(self.marker))
        env.pop("DRAGON_BIN", None)
        env.update(overrides)
        return subprocess.run(
            ["/bin/sh", str(self.script), "--repaired-runtime", str(self.runtime),
             str(self.build), str(self.final), str(self.output)],
            env=env, capture_output=True, text=True, timeout=15)

    def refused(self, message, **overrides):
        result = self.run_extract(**overrides)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)
        self.assertFalse(self.marker.exists(), "refusal happened after launching")
        self.assertFalse(self.output.exists(), "refusal created output")

    def test_synthetic_full_roundtrip_preserves_inputs(self):
        before = {p: digest(p) for base in (self.runtime, self.build, self.final)
                  for p in base.rglob("*") if p.is_file()}
        result = self.run_extract()
        log = self.output / "observables.log"
        detail = result.stdout + result.stderr + (log.read_text() if log.exists() else "")
        self.assertEqual(result.returncode, 0, detail)
        self.assertIn("D4A CORRECTED FINAL OBSERVABLES PASS", result.stdout)
        self.assertTrue(self.marker.exists())
        self.assertEqual(len((self.output / "observables.sha256").read_text().splitlines()), 5)
        self.assertEqual(before, {p: digest(p) for p in before})

    def test_mesh12_full_roundtrip_preserves_inputs(self):
        substitute_epoch_hashes(self.script, self.runtime, self.build, "MESH12", "MESH12")
        self.test_synthetic_full_roundtrip_preserves_inputs()

    def test_cross_epoch_pairs_are_refused_before_launch(self):
        for runtime_epoch, bootstrap_epoch in (("REPAIRED", "MESH12"), ("MESH12", "REPAIRED")):
            with self.subTest(runtime=runtime_epoch, bootstrap=bootstrap_epoch):
                substitute_epoch_hashes(self.script, self.runtime, self.build,
                                        runtime_epoch, bootstrap_epoch)
                self.refused("repaired bootstrap identity differs")

    def test_mesh12_not_met_is_refused_before_launch(self):
        substitute_epoch_hashes(self.script, self.runtime, self.build, "MESH12", "MESH12")
        self.test_not_met_is_refused_before_launch()

    def test_mesh12_resealed_other_runtime_is_refused(self):
        substitute_epoch_hashes(self.script, self.runtime, self.build, "MESH12", "MESH12")
        self.test_resealed_other_runtime_is_refused()

    def test_production_script_rejects_synthetic_runtime(self):
        shutil.copy2(SCRIPT, self.script)
        self.refused("repaired Dragon identity differs")

    def test_not_met_is_refused_before_launch(self):
        self.write_gate("VALID_NOT_MET")
        self.seal_final()
        self.refused("final map is not VALID_MET")

    def test_old_bootstrap_is_refused(self):
        (self.build / "result.sha256").write_text("old bootstrap\n")
        self.refused("repaired bootstrap identity differs")

    def test_resealed_other_runtime_is_refused(self):
        (self.runtime / "runtime.sha256").write_text("different runtime\n")
        self.refused("repaired runtime manifest identity differs")

    def test_tampered_saved_gate_is_refused(self):
        self.write_gate("VALID_NOT_MET")
        self.refused("final repaired result does not verify")

    def test_resealed_final_using_other_dragon_is_refused(self):
        (self.final / "runtime/Dragon").write_text("wrong executable\n")
        self.seal_final()
        self.refused("final result belongs to a different runtime")

    def test_unmanifested_gate_is_refused(self):
        receipt = self.final / "result.sha256"
        receipt.write_text("".join(line for line in receipt.read_text().splitlines(True)
                                   if not line.endswith("  gate.log\n")))
        self.refused("final repaired result does not manifest gate.log")

    def test_lookalike_manifest_name_cannot_replace_gate(self):
        shutil.copy2(self.final / "gate.log", self.final / "gateXlog")
        receipt = self.final / "result.sha256"
        receipt.write_text(receipt.read_text().replace("  gate.log\n", "  gateXlog\n"))
        self.refused("final repaired result does not manifest gate.log")

    def test_runtime_override_is_refused(self):
        self.refused("DRAGON_BIN override is not allowed", DRAGON_BIN="/tmp/not-dragon")

    def test_changed_deck_is_refused(self):
        with self.deck.open("a") as stream:
            stream.write("* changed deck\n")
        self.refused("read-only observables deck identity differs")

    def test_dangling_output_symlink_is_refused(self):
        self.output.symlink_to(self.root / "absent")
        self.refused("output directory must be fresh")


if __name__ == "__main__":
    unittest.main()

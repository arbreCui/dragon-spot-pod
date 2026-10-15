#!/usr/bin/env python3
"""Transport-free repaired-lineage tests; all scientific executables are fake.

Only private fixture copies substitute the registered epoch hash constants.
An unchanged production copy must reject the synthetic package.
"""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "check_d4a_corrected_acceptance.sh"
RECORDS = (">|D4A-CORRECTED-K-EFFECTIVE 1.234567890123456E+00\n"
           "SPORATE NU-FISSION-FRACTIONS 0.2 0.3 0.5\n"
           " normal end of execution for dragon\n")
CHECK_LOG = ("ONE-MAP-XSM POD-PACKAGE BITWISE PASS\n"
             "ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS\n"
             "ONE-MAP-XSM RAW-DEFECT BITWISE PASS\n"
             "ONE-MAP-XSM COMPLETE\n")
INPUTS = ("parent_axial_closed.xsm", "parent_snapshots_closed.xsm",
          "initial_radial_track.bin", "initial_axial_track.xsm",
          "initial_axial_macrolib.xsm", "basis_reference.xsm",
          "route_contract.xsm", "projected_proposal.xsm")
OUTPUTS = ("candidate_system.xsm", "candidate_radial.xsm", "candidate_axial.xsm",
           "candidate_snapshots.xsm", "closed_axial.xsm", "closed_snapshots.xsm")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(root, receipt, names=None):
    if names is None:
        names = [p.relative_to(root).as_posix() for p in sorted(root.rglob("*"))
                 if p.is_file() and p != root / receipt]
    (root / receipt).write_text("".join(f"{sha(root / n)}  {n}\n" for n in names))


def executable(path, text):
    path.write_text("#!/bin/sh\n" + text)
    path.chmod(0o755)


def substitute_epoch_hashes(script, runtime, bootstrap,
                            runtime_epoch="REPAIRED", bootstrap_epoch="REPAIRED"):
    """Give synthetic bytes either registered identity, only in a private copy."""
    replacements = {
        f"{epoch}_{kind}_SHA": hashlib.sha256(f"unused-{epoch}-{kind}".encode()).hexdigest()
        for epoch in ("REPAIRED", "MESH12") for kind in ("RUNTIME", "BOOTSTRAP")
    }
    replacements.update({
        "REPAIRED_DRAGON_SHA": sha(runtime / "Dragon"),
        f"{runtime_epoch}_RUNTIME_SHA": sha(runtime / "runtime.sha256"),
        f"{bootstrap_epoch}_BOOTSTRAP_SHA": sha(bootstrap / "result.sha256"),
    })
    lines = script.read_text().splitlines(True)
    assert all(sum(line.startswith(key + "=") for line in lines) == 1
               for key in replacements), "fixture expected explicit epoch constants"
    script.write_text("".join(
        f"{line.split('=', 1)[0]}={replacements[line.split('=', 1)[0]]}\n"
        if line.split("=", 1)[0] in replacements else line for line in lines))


def gate(met):
    status = "PASS" if met else "NOT MET"
    return ("SPOT-GATE THRESHOLD        4.9999999999999998E-07\n" +
            "".join(f"SPOT-GATE {name} 1.0E-{'8' if met else '4'} {status} \n"
                    for name in ("RRHO", "RLEAK", "RA")) +
            f"CLASSIFICATION=VALID_{'MET' if met else 'NOT_MET'}\nSPOT-GATE COMPLETE\n")


class RepairedAcceptanceTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="d4a-repaired-acceptance-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.tools = self.root / "validation/iterative"
        self.tools.mkdir(parents=True)
        self.script = self.tools / SOURCE.name
        for name in (SOURCE.name, "verify_d4a_corrected_observables.sh",
                     "d4a_corrected_final_observables.x2m", "run_bounded_dragon.py"):
            shutil.copy2(HERE / name, self.tools)
        audit = self.root / "validation/d4_reference"
        audit.mkdir()
        shutil.copy2(ROOT / "validation/d4_reference/material_epoch_audit_result.md", audit)
        self.runtime = self.root / "runtime"
        self.runtime.mkdir()
        executable(self.runtime / "Dragon",
                   'printf called > "$TEST_DRAGON_MARKER"\n'
                   + "printf '%s\\n' " + " ".join(repr(s) for s in RECORDS.splitlines()) + "\n")
        executable(self.runtime / "check_one_map_xsm",
                   'printf checked > "$TEST_CHECKER_MARKER"\nprintf "MODE=%s\\n" "$1"\n'
                   + "printf '%s\\n' " + " ".join(repr(s) for s in CHECK_LOG.splitlines()) + "\n")
        executable(self.runtime / "check_convergence_gate", 'cat "$1"\n')
        shutil.copy2(HERE / "run_bounded_dragon.py", self.runtime)
        seal(self.runtime, "runtime.sha256")
        self.build = self.root / "snapshot-build"
        self.build.mkdir()
        for name in ("rnr_cc.c2m", "rnr_interpol.c2m"):
            shutil.copy2(ROOT / "data/rnr_0burn_spot_proc" / name, self.build)
        (self.build / "frozen_repository_inputs.sha256").write_text("".join(
            f"{sha(self.build / n)}  data/rnr_0burn_spot_proc/{n}\n"
            for n in ("rnr_cc.c2m", "rnr_interpol.c2m")))
        snapshot_names = ("d4a_snapshots.xsm", "d4a_three_snapshots.log", "snapshot_check.log",
                          "snapshot_check.err", "run_contract.txt", "executed_inputs.sha256",
                          "frozen_repository_inputs.sha256", "snapshot_build_result.sha256",
                          "dragon_executable.sha256")
        for name in snapshot_names:
            if not (self.build / name).exists():
                (self.build / name).write_text("synthetic snapshot record\n")
        (self.build / "d4a_three_snapshots.log").write_text(" FLU2DR-TERM OUTER-GATE=PASS \n" * 3)
        (self.build / "snapshot_check.log").write_text(
            "D4A-SNAPSHOT TUPLE NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144\n"
            "D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS\n")
        (self.build / "snapshot_check.err").write_text("")
        seal(self.build, "admitted_snapshot_archive.sha256", snapshot_names)
        rank_names = ("d4a_snapshots.xsm", "d4a_rank2_basis.xsm", "d4a_axial_track.xsm",
                      "d4a_axial_macrolib.xsm", "d4a_rank2_check.log", "d4a_rank2_check.err")
        for name in rank_names[1:]:
            (self.build / name).write_text(f"synthetic {name}\n")
        (self.build / "d4a_rank2_check.log").write_text(
            "D4A-RANK2 DIMENSIONS NGRP=370 NREG2D=132 NSNAP=3 NMODE=2\n"
            "D4A-RANK2 STORED-DIAGNOSTICS BITWISE PASS\nD4A-RANK2 GANLIB-ONLY PASS\n")
        (self.build / "d4a_rank2_check.err").write_text("")
        seal(self.build, "d4a_rank2_admitted.sha256", rank_names)
        self.bootstrap = self.root / "bootstrap"
        self.bootstrap.mkdir()
        for name in ("route_contract.xsm", "initial_radial_track.bin"):
            (self.build / name).write_text(f"synthetic {name}\n")
            shutil.copy2(self.build / name, self.bootstrap)
        for source, dest in (("d4a_snapshots.xsm", "d4a_snapshots.xsm"),
                             ("d4a_rank2_basis.xsm", "basis_reference.xsm"),
                             ("d4a_axial_macrolib.xsm", "initial_axial_macrolib.xsm")):
            shutil.copy2(self.build / source, self.bootstrap / dest)
        for name in ("closed_axial.xsm", "closed_snapshots.xsm", "initial_axial_track.xsm",
                     "d4a_refreshed_snapshots.xsm"):
            (self.bootstrap / name).write_text(f"synthetic repaired {name}\n")
        (self.bootstrap / "b2i_seal_bootstrap.log").write_text(
            "SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0\n")
        (self.bootstrap / "radial.log").write_text(
            "".join(f">|SPOT-REFRESH-R64-RESULT {n}\n" for n in (1, 2, 3)) +
            ">|D4A-R64-REFRESH-COMPLETE\n")
        seal(self.bootstrap, "result.sha256")
        substitute_epoch_hashes(self.script, self.runtime, self.bootstrap)
        self.map1 = self.make_map(self.bootstrap, 1, True)
        self.observables = self.root / "observables"
        self.observables.mkdir()
        self.set_observables(self.map1)
        self.check_marker = self.root / "checker-called"
        self.dragon_marker = self.root / "dragon-called"

    def make_map(self, parent, index, met):
        directory = self.root / f"map-{index}"
        directory.mkdir()
        for name in INPUTS[2:-1]:
            shutil.copy2(parent / name, directory)
        for source, target in (("closed_axial.xsm", "parent_axial_closed.xsm"),
                               ("closed_snapshots.xsm", "parent_snapshots_closed.xsm")):
            shutil.copy2(parent / source, directory / target)
        for name in (*OUTPUTS, "projected_proposal.xsm", "parent_for_checker.xsm"):
            (directory / name).write_text(f"synthetic map {index} {name}\n")
        (directory / "closed_axial.xsm").write_text(gate(met))
        (directory / "gate.log").write_text(gate(met))
        (directory / "prepare.log").write_text(
            f"SPOT-R64 B2J CLOSED/{index - 1} -> PROJECTED/{index}\n")
        (directory / "admission.log").write_text("H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3\n")
        (directory / "close.log").write_text("SPOT-R64 B2W CLOSE PASS STATUS=2\n"
                                             f"SPOT-R64 CLOSED/{index} COMPLETE NO-TRANSPORT\n")
        mode = "--reencoded" if index == 1 else "--continued"
        (directory / "independent_check.log").write_text(f"MODE={mode}\n" + CHECK_LOG)
        shutil.copytree(self.runtime, directory / "runtime")
        self.seal_map(directory)
        return directory

    def seal_map(self, directory):
        seal(directory, "input_manifest.sha256", INPUTS)
        seal(directory, "parent_inputs.sha256", INPUTS)
        seal(directory, "output_manifest.sha256", OUTPUTS)
        seal(directory, "result.sha256")

    def set_observables(self, final):
        for name in ("closed_axial.xsm", "initial_axial_track.xsm", "initial_axial_macrolib.xsm"):
            shutil.copy2(final / name, self.observables)
        shutil.copy2(self.tools / "d4a_corrected_final_observables.x2m", self.observables / "observables.x2m")
        (self.observables / "observables.log").write_text(RECORDS)
        seal(self.observables, "observables.sha256")

    def run_check(self, maps=None, options=None):
        env = dict(os.environ, D4A_OBSERVABLES_DIR=str(self.observables),
                   TEST_CHECKER_MARKER=str(self.check_marker),
                   TEST_DRAGON_MARKER=str(self.dragon_marker))
        for name in ("CHECKER_DIR", "DRAGON_BIN"):
            env.pop(name, None)
        if options is None:
            options = ["--repaired-runtime", str(self.runtime),
                       "--repaired-bootstrap", str(self.bootstrap)]
        return subprocess.run(["/bin/sh", str(self.script), *options, str(self.build),
                               *(str(p) for p in (maps or [self.map1]))],
                              env=env, capture_output=True, text=True, timeout=20)

    def refused(self, **kwargs):
        result = self.run_check(**kwargs)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("D4A-CORRECTED-ACCEPT OVERALL PASS", result.stdout)
        return result

    def test_synthetic_met_chain_replays_and_preserves_inputs(self):
        before = {p: sha(p) for base in (self.runtime, self.bootstrap, self.build, self.map1)
                  for p in base.rglob("*") if p.is_file()}
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("D4A-CORRECTED-ACCEPT OVERALL PASS", result.stdout)
        self.assertTrue(self.check_marker.exists())
        self.assertTrue(self.dragon_marker.exists())
        self.assertEqual(before, {p: sha(p) for p in before})

    def test_mesh12_met_chain_replays_and_preserves_inputs(self):
        substitute_epoch_hashes(self.script, self.runtime, self.bootstrap, "MESH12", "MESH12")
        self.test_synthetic_met_chain_replays_and_preserves_inputs()

    def test_cross_epoch_pairs_are_refused_before_replay(self):
        for runtime_epoch, bootstrap_epoch in (("REPAIRED", "MESH12"), ("MESH12", "REPAIRED")):
            with self.subTest(runtime=runtime_epoch, bootstrap=bootstrap_epoch):
                substitute_epoch_hashes(self.script, self.runtime, self.bootstrap,
                                        runtime_epoch, bootstrap_epoch)
                result = self.refused()
                self.assertIn("REPAIR-EPOCH", result.stdout)
                self.assertFalse(self.check_marker.exists())
                self.assertFalse(self.dragon_marker.exists())

    def test_mesh12_not_met_remains_not_final(self):
        substitute_epoch_hashes(self.script, self.runtime, self.bootstrap, "MESH12", "MESH12")
        self.test_valid_not_met_remains_not_final()

    def test_mesh12_resealed_other_runtime_is_refused(self):
        substitute_epoch_hashes(self.script, self.runtime, self.bootstrap, "MESH12", "MESH12")
        self.test_resealed_other_runtime_is_refused()

    def test_actual_production_entry_refuses_fake_epoch(self):
        shutil.copy2(SOURCE, self.script)
        self.refused()
        self.assertFalse(self.check_marker.exists())
        self.assertFalse(self.dragon_marker.exists())

    def test_repaired_options_required_together(self):
        for options in (["--repaired-runtime", str(self.runtime)],
                        ["--repaired-bootstrap", str(self.bootstrap)]):
            with self.subTest(options=options):
                result = self.refused(options=options)
                self.assertIn("required together", result.stderr)

    def test_valid_not_met_remains_not_final(self):
        for name in ("closed_axial.xsm", "gate.log"):
            (self.map1 / name).write_text(gate(False))
        self.seal_map(self.map1)
        result = self.refused()
        self.assertIn("MAP-REPLAY PASS: CLOSED/1", result.stdout)
        self.assertFalse(self.dragon_marker.exists())

    def test_resealed_forged_gate_is_refused_by_live_replay(self):
        (self.map1 / "closed_axial.xsm").write_text(gate(False))
        self.seal_map(self.map1)
        self.refused()
        self.assertTrue(self.check_marker.exists())
        self.assertFalse(self.dragon_marker.exists())

    def test_resealed_wrong_parent_is_refused(self):
        (self.map1 / "parent_axial_closed.xsm").write_text("different parent\n")
        self.seal_map(self.map1)
        self.refused()

    def test_resealed_wrong_repaired_track_is_refused(self):
        shutil.copy2(self.build / "d4a_axial_track.xsm", self.map1 / "initial_axial_track.xsm")
        self.seal_map(self.map1)
        self.refused()

    def test_resealed_altered_bootstrap_is_refused(self):
        (self.bootstrap / "closed_axial.xsm").write_text("altered CLOSED/0\n")
        seal(self.bootstrap, "result.sha256")
        self.refused()
        self.assertFalse(self.check_marker.exists())

    def test_resealed_other_runtime_is_refused(self):
        (self.runtime / "check_one_map_xsm").write_text("bad checker\n")
        seal(self.runtime, "runtime.sha256")
        self.refused()
        self.assertFalse(self.check_marker.exists())

    def test_unsealed_lookalike_gate_is_refused(self):
        shutil.copy2(self.map1 / "gate.log", self.map1 / "gateXlog")
        receipt = self.map1 / "result.sha256"
        receipt.write_text(receipt.read_text().replace("  gate.log\n", "  gateXlog\n"))
        self.refused()
        self.assertFalse(self.check_marker.exists())

    def test_resealed_forged_observables_are_refused(self):
        (self.observables / "observables.log").write_text(RECORDS.replace("1.234567890123456", "1.7"))
        seal(self.observables, "observables.sha256")
        self.refused()
        self.assertTrue(self.dragon_marker.exists())

    def test_continued_map_uses_original_order_and_modes(self):
        for name in ("closed_axial.xsm", "gate.log"):
            (self.map1 / name).write_text(gate(False))
        self.seal_map(self.map1)
        map2 = self.make_map(self.map1, 2, True)
        self.set_observables(map2)
        result = self.run_check(maps=[self.map1, map2])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.refused(maps=[map2, self.map1])

    def test_maps_after_first_met_are_refused(self):
        map2 = self.make_map(self.map1, 2, True)
        self.set_observables(map2)
        self.refused(maps=[self.map1, map2])

    def test_changed_material_is_refused(self):
        (self.build / "rnr_cc.c2m").write_text("not the reviewed material model\n")
        result = self.refused()
        self.assertIn("MATERIAL FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Isolated preflight regression checks; never compile or execute Dragon."""

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CANONICAL = ROOT / "bin/Darwin_arm64/Dragon"
EXPECTED_SHA = "2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db"
REPAIRED = ROOT / "validation/artifacts/d4a-scattering-bootstrap-run-20260924/Dragon"
REPAIRED_SHA = "873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef"
INPUTS = (
    "closed_axial.xsm", "closed_snapshots.xsm", "initial_radial_track.bin",
    "initial_axial_track.xsm", "initial_axial_macrolib.xsm",
    "basis_reference.xsm", "route_contract.xsm",
)
HOSTS = (
    "prepare_r64_next_projected", "admit_candidate_radial", "close_r64_returned",
    "check_one_map_xsm", "check_convergence_gate",
)


def executable(path, text):
    path.write_text(text, encoding="ascii")
    path.chmod(0o755)


class MapPreflightTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hashlib.sha256(CANONICAL.read_bytes()).hexdigest() != EXPECTED_SHA:
            raise RuntimeError("Test requires the already-restored canonical binary; will not rebuild it")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="d4a-map-preflight-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.tools = self.root / "validation/iterative"
        self.tools.mkdir(parents=True)
        self.runner = self.tools / "run_d4a_rank2_picard_map.sh"
        shutil.copy2(HERE / self.runner.name, self.runner)
        self.dragon = self.root / "bin/Darwin_arm64/Dragon"
        self.dragon.parent.mkdir(parents=True)
        shutil.copy2(CANONICAL, self.dragon)
        self.parent = self.root / "parent"
        self.parent.mkdir()
        for name in INPUTS:
            (self.parent / name).write_text("synthetic input; never read by Dragon\n")
        (self.root / "data").mkdir()
        shutil.copy2(ROOT / "data/SpotStepR64.c2m", self.root / "data/SpotStepR64.c2m")
        for name in ("d4a_rank2_picard_radial.x2m", "d4a_rank2_picard_axial.x2m",
                     "d4a_rank2_checker_parent.x2m"):
            shutil.copy2(HERE / name, self.tools / name)
        for name in HOSTS:
            executable(self.tools / name,
                       '#!/bin/sh\nprintf called > "$OTHER_HOST_MARKER"\nexit 97\n')
        executable(self.tools / HOSTS[0],
                   '#!/bin/sh\nprintf prepared > "$PREPARE_MARKER"\nexit 19\n')
        # Independent safety barrier: even a regression ignoring exit 19
        # cannot proceed from the copied shell runner to a real Dragon launch.
        (self.tools / "run_bounded_dragon.py").write_text(
            'import os\nfrom pathlib import Path\n'
            'Path(os.environ["BOUNDED_MARKER"]).write_text("unexpected")\n'
            'raise SystemExit(98)\n', encoding="ascii")
        self.fake_path = self.root / "fake-path"
        self.fake_path.mkdir()
        executable(self.fake_path / "make",
                   '#!/bin/sh\nprintf called > "$MAKE_MARKER"\nexit 99\n')
        self.markers = {name: self.root / name.lower() for name in (
            "PREPARE_MARKER", "MAKE_MARKER", "OTHER_HOST_MARKER", "BOUNDED_MARKER")}
        self.output = self.root / "fresh-map"

    def run_map(self, options=(), with_budget=True, *, parent=None, runner=None):
        environment = dict(os.environ, RADIAL_TIMEOUT_SECONDS="1", AXIAL_TIMEOUT_SECONDS="1",
                           PATH=str(self.fake_path) + os.pathsep + os.environ["PATH"])
        environment.update({name: str(path) for name, path in self.markers.items()})
        if not with_budget:
            environment.pop("RADIAL_TIMEOUT_SECONDS")
            environment.pop("AXIAL_TIMEOUT_SECONDS")
        result = subprocess.run(
            ["sh", str(runner or self.runner), *options,
             str(parent or self.parent), str(self.output)],
            cwd=self.root, env=environment, timeout=10, capture_output=True, text=True)
        for name in ("MAKE_MARKER", "OTHER_HOST_MARKER", "BOUNDED_MARKER"):
            self.assertFalse(self.markers[name].exists(), f"unexpected action: {name}")
        return result

    def require_rejected(self, options=(), *, parent=None, runner=None):
        result = self.run_map(options, parent=parent, runner=runner)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.output.exists(), result.stdout + result.stderr)
        self.assertFalse(self.markers["PREPARE_MARKER"].exists())
        return result

    def test_valid_preflight_reaches_prepare_without_compilation(self):
        result = self.run_map()
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        self.assertTrue(self.output.is_dir())
        self.assertEqual(self.markers["PREPARE_MARKER"].read_text(), "prepared")
        self.assertEqual(hashlib.sha256(self.dragon.read_bytes()).hexdigest(), EXPECTED_SHA)

    def test_missing_binary_is_rejected_before_output(self):
        self.dragon.unlink()
        self.require_rejected()

    def test_tampered_binary_is_rejected_before_output(self):
        self.dragon.write_bytes(b"invalid binary; must never execute\n")
        self.require_rejected()

    def test_nonexecutable_binary_is_rejected_before_output(self):
        self.dragon.chmod(0o644)
        self.require_rejected()

    def test_symlink_binary_is_rejected_before_output(self):
        target = self.dragon.with_name("Dragon.target")
        self.dragon.rename(target)
        self.dragon.symlink_to(target.name)
        self.require_rejected()

    def test_each_missing_host_is_rejected_before_output(self):
        for name in HOSTS:
            with self.subTest(host=name):
                path = self.tools / name
                saved = path.read_bytes()
                path.unlink()
                self.require_rejected()
                path.write_bytes(saved)
                path.chmod(0o755)

    def test_each_missing_parent_input_is_rejected_before_output(self):
        for name in INPUTS:
            with self.subTest(input=name):
                path = self.parent / name
                saved = path.read_bytes()
                path.unlink()
                self.require_rejected()
                path.write_bytes(saved)

    def register_fixture(self, runtime, *, epoch="REPAIRED", parent=None):
        """Register synthetic identities in the private script, never production."""
        parent = parent or self.parent
        values = {
            f"{epoch}_RUNTIME_SHA": runtime / "runtime.sha256",
            f"{epoch}_BOOTSTRAP_SHA": parent / "result.sha256",
            f"{epoch}_TRACK_SHA": parent / "initial_axial_track.xsm",
        }
        text = self.runner.read_text()
        for name, path in values.items():
            value = hashlib.sha256(path.read_bytes()).hexdigest()
            text, count = re.subn(rf"^{name}=[0-9a-f]{{64}}$",
                                  f"{name}={value}", text, flags=re.MULTILINE)
            self.assertEqual(count, 1, f"missing unique private-script pin: {name}")
        self.runner.write_text(text, encoding="ascii")

    def repaired_fixture(self, *, epoch="REPAIRED", parent=None):
        # Real pinned executable, but both the prepare and bounded-run stubs
        # independently prevent any solver invocation during these tests.
        self.assertEqual(hashlib.sha256(REPAIRED.read_bytes()).hexdigest(), REPAIRED_SHA)
        parent = parent or self.parent
        if parent != self.parent:
            parent.mkdir()
            for name in INPUTS:
                shutil.copy2(self.parent / name, parent / name)
        (parent / "initial_axial_track.xsm").write_text(
            f"synthetic {epoch} track; never read by Dragon\n", encoding="ascii")
        runtime = self.root / f"{epoch.lower()}-runtime"
        runtime.mkdir()
        shutil.copy2(REPAIRED, runtime / "Dragon")
        shutil.copy2(REPAIRED, parent / "Dragon")
        for name in (*HOSTS, "run_bounded_dragon.py", "d4a_rank2_picard_radial.x2m",
                     "d4a_rank2_picard_axial.x2m", "d4a_rank2_checker_parent.x2m"):
            shutil.copy2(self.tools / name, runtime / name)
        shutil.copy2(self.root / "data/SpotStepR64.c2m", runtime / "SpotStepR64.c2m")
        # Distinct registered runtimes are essential to test cross-epoch refusal.
        with (runtime / "check_one_map_xsm").open("a", encoding="ascii") as stream:
            stream.write(f"# synthetic {epoch} checker identity\n")
        self.write_manifest(runtime, "runtime.sha256")
        self.write_manifest(parent, "result.sha256")
        self.register_fixture(runtime, epoch=epoch, parent=parent)
        return runtime, ("--repaired-runtime", str(runtime))

    @staticmethod
    def write_manifest(directory, name):
        receipt = directory / name
        entries = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
                   f"{path.relative_to(directory).as_posix()}\n"
                   for path in sorted(directory.rglob("*"))
                   if path.is_file() and path != receipt]
        (directory / name).write_text("".join(entries), encoding="ascii")

    def continued_parent(self, runtime):
        # A continuation must carry the registered runtime receipt in its own
        # fully verified result, rather than being registered as a bootstrap.
        (self.parent / "runtime").mkdir()
        shutil.copy2(runtime / "runtime.sha256",
                     self.parent / "runtime/runtime.sha256")
        self.write_manifest(self.parent, "result.sha256")

    def test_repaired_preflight_creates_nothing_without_budget(self):
        _, options = self.repaired_fixture()
        result = self.run_map((*options, "--preflight-only"), with_budget=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NO-TRANSPORT NO-OUTPUT", result.stdout)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.markers["PREPARE_MARKER"].exists())

    def test_registered_coarse_fine_pairs_and_cross_pair_refusal(self):
        _, coarse_options = self.repaired_fixture()
        fine_parent = self.root / "fine-parent"
        _, fine_options = self.repaired_fixture(epoch="MESH12", parent=fine_parent)
        for label, options, parent, accepted in (
            ("coarse", coarse_options, self.parent, True),
            ("fine", fine_options, fine_parent, True),
            ("coarse-runtime-fine-parent", coarse_options, fine_parent, False),
            ("fine-runtime-coarse-parent", fine_options, self.parent, False),
        ):
            with self.subTest(pair=label):
                result = self.run_map((*options, "--preflight-only"),
                                      with_budget=False, parent=parent)
                self.assertEqual(result.returncode == 0, accepted,
                                 result.stdout + result.stderr)
                if not accepted:
                    self.assertIn("parent axial mesh differs", result.stderr)
                self.assertFalse(self.output.exists())
                self.assertFalse(self.markers["PREPARE_MARKER"].exists())

    def test_registered_continuation_preflight_creates_nothing(self):
        runtime, options = self.repaired_fixture(epoch="MESH12")
        self.continued_parent(runtime)
        result = self.run_map((*options, "--preflight-only"), with_budget=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.markers["PREPARE_MARKER"].exists())

    def test_continuation_wrong_track_refused_despite_resealed_result(self):
        runtime, options = self.repaired_fixture(epoch="MESH12")
        self.continued_parent(runtime)
        (self.parent / "initial_axial_track.xsm").write_text("wrong mesh track\n")
        self.write_manifest(self.parent, "result.sha256")
        result = self.require_rejected((*options, "--preflight-only"))
        self.assertIn("parent axial mesh differs", result.stderr)

    def test_continuation_wrong_runtime_refused_despite_resealed_result(self):
        runtime, options = self.repaired_fixture(epoch="MESH12")
        self.continued_parent(runtime)
        (self.parent / "runtime/runtime.sha256").write_text("wrong runtime receipt\n")
        self.write_manifest(self.parent, "result.sha256")
        result = self.require_rejected((*options, "--preflight-only"))
        self.assertIn("neither the selected bootstrap nor its runtime continuation",
                      result.stderr)

    def test_continuation_other_registered_runtime_refused(self):
        runtime, options = self.repaired_fixture(epoch="MESH12")
        coarse, _ = self.repaired_fixture(parent=self.root / "coarse-parent")
        self.continued_parent(runtime)
        shutil.copy2(coarse / "runtime.sha256",
                     self.parent / "runtime/runtime.sha256")
        self.write_manifest(self.parent, "result.sha256")
        result = self.require_rejected((*options, "--preflight-only"))
        self.assertIn("neither the selected bootstrap nor its runtime continuation",
                      result.stderr)

    def test_unregistered_bootstrap_refused_despite_resealed_result(self):
        _, options = self.repaired_fixture(epoch="MESH12")
        (self.parent / "closed_axial.xsm").write_text("different synthetic state\n")
        self.write_manifest(self.parent, "result.sha256")
        result = self.require_rejected((*options, "--preflight-only"))
        self.assertIn("neither the selected bootstrap nor its runtime continuation",
                      result.stderr)

    def test_unregistered_runtime_refused_despite_resealed_manifest(self):
        runtime, options = self.repaired_fixture(epoch="MESH12")
        with (runtime / "check_one_map_xsm").open("a") as stream:
            stream.write("# changed identity\n")
        self.write_manifest(runtime, "runtime.sha256")
        result = self.require_rejected((*options, "--preflight-only"))
        self.assertIn("unregistered repaired runtime", result.stderr)

    def test_production_script_refuses_synthetic_registration(self):
        _, options = self.repaired_fixture(epoch="MESH12")
        result = self.require_rejected((*options, "--preflight-only"),
                                       runner=HERE / self.runner.name)
        self.assertIn("unregistered repaired runtime", result.stderr)

    def test_repaired_execution_requires_explicit_caps(self):
        _, options = self.repaired_fixture()
        result = self.run_map(options, with_budget=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_repaired_reaches_prepare_with_private_runtime(self):
        runtime, options = self.repaired_fixture()
        result = self.run_map(options)
        self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
        copied = self.output / "runtime/Dragon"
        self.assertFalse(os.path.samefile(copied, runtime / "Dragon"))
        self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(), REPAIRED_SHA)

    def test_repaired_tampered_host_rejected_before_output(self):
        runtime, options = self.repaired_fixture()
        (runtime / "close_r64_returned").write_text("tampered\n")
        self.require_rejected(options)

    def test_repaired_missing_manifest_entry_rejected(self):
        runtime, options = self.repaired_fixture()
        manifest = runtime / "runtime.sha256"
        manifest.write_text("".join(line for line in manifest.read_text().splitlines(True)
                                    if not line.endswith("  SpotStepR64.c2m\n")))
        self.require_rejected(options)

    def test_repaired_tampered_parent_rejected_before_output(self):
        _, options = self.repaired_fixture()
        (self.parent / "closed_axial.xsm").write_text("tampered\n")
        self.require_rejected(options)

    def test_repaired_old_runtime_parent_rejected(self):
        _, options = self.repaired_fixture()
        shutil.copy2(CANONICAL, self.parent / "Dragon")
        self.write_manifest(self.parent, "result.sha256")
        self.require_rejected(options)

    def test_repaired_synthetic_full_route_seals_only_one_map(self):
        runtime, options = self.repaired_fixture()
        # This fixture replaces EVERY host and the transport runner. It tests
        # orchestration/receipts only; no scientific result or Dragon execution.
        executable(runtime / HOSTS[0], '#!/bin/sh\n'
                   'printf synthetic > projected_proposal.xsm\n'
                   'echo "SPOT-R64 B2J CLOSED/0 -> PROJECTED/1"\n')
        executable(runtime / "admit_candidate_radial", '#!/bin/sh\nexit 0\n')
        executable(runtime / "close_r64_returned", '#!/bin/sh\n'
                   'cp candidate_axial.xsm closed_axial.xsm\n'
                   'cp candidate_snapshots.xsm closed_snapshots.xsm\n')
        executable(runtime / "check_one_map_xsm", '#!/bin/sh\nexit 0\n')
        executable(runtime / "check_convergence_gate", '#!/bin/sh\n'
                   'echo CLASSIFICATION=VALID_NOT_MET\necho "SPOT-GATE COMPLETE"\n')
        (runtime / "run_bounded_dragon.py").write_text(
            'from pathlib import Path\nimport sys\n'
            'deck = Path(sys.argv[2]).name\n'
            'outputs = {"radial.x2m": ["candidate_system.xsm", "candidate_radial.xsm"],'
            ' "axial.x2m": ["candidate_axial.xsm", "candidate_snapshots.xsm"],'
            ' "checker_parent.x2m": ["parent_for_checker.xsm"]}[deck]\n'
            'for name in outputs: Path(name).write_text("synthetic fixture only")\n'
            'Path(sys.argv[3]).write_text("synthetic fixture only")\n'
            'with Path("synthetic_calls.log").open("a") as log: log.write(deck + "\\n")\n')
        self.write_manifest(runtime, "runtime.sha256")
        # This one positive orchestration fixture deliberately changed all
        # stubs above. Register that new identity only here; negative tests
        # must not automatically bless a resealed mutation.
        self.register_fixture(runtime)
        result = self.run_map(options)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.output / "synthetic_calls.log").read_text().splitlines(),
                         ["radial.x2m", "axial.x2m", "checker_parent.x2m"])
        verify = subprocess.run(["shasum", "-a", "256", "-c", "result.sha256"],
                                cwd=self.output, capture_output=True, text=True, timeout=10)
        self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
        next_output = self.root / "unstarted-next-map"
        check = subprocess.run(["sh", str(self.runner), *options, "--preflight-only",
                                str(self.output), str(next_output)],
                               capture_output=True, text=True, timeout=10)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertFalse(next_output.exists())


if __name__ == "__main__":
    unittest.main()

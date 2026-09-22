#!/usr/bin/env python3
"""Isolated preflight regression checks; never compile or execute Dragon."""

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CANONICAL = ROOT / "bin/Darwin_arm64/Dragon"
EXPECTED_SHA = "2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db"
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

    def run_map(self):
        environment = dict(os.environ, RADIAL_TIMEOUT_SECONDS="1", AXIAL_TIMEOUT_SECONDS="1",
                           PATH=str(self.fake_path) + os.pathsep + os.environ["PATH"])
        environment.update({name: str(path) for name, path in self.markers.items()})
        result = subprocess.run(
            ["sh", str(self.runner), str(self.parent), str(self.output)],
            cwd=self.root, env=environment, timeout=10, capture_output=True, text=True)
        for name in ("MAKE_MARKER", "OTHER_HOST_MARKER", "BOUNDED_MARKER"):
            self.assertFalse(self.markers[name].exists(), f"unexpected action: {name}")
        return result

    def require_rejected(self):
        result = self.run_map()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.output.exists(), result.stdout + result.stderr)
        self.assertFalse(self.markers["PREPARE_MARKER"].exists())

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


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Fast no-Dragon tests for the B2n standalone-helper limiter."""

from __future__ import annotations

from contextlib import contextmanager
import copy
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import run_bounded_b2n as bounded


class BoundedB2NTest(unittest.TestCase):
    def make_executable(self, root: Path, body: str, name: str = "helper") -> Path:
        path = root / name
        path.write_text("#!/bin/sh\nset -eu\n" + body, encoding="ascii")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    @contextmanager
    def patched_profile(self, name: str, **updates: int | float):
        profiles = copy.deepcopy(bounded.PROFILES)
        profiles[name].update(updates)
        with mock.patch.object(bounded, "PROFILES", profiles):
            yield

    def assert_process_gone(self, pid: int) -> None:
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.02)
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        self.fail(f"test found a surviving child process: {pid}")

    def test_success_with_input_argument_and_sanitized_environment(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(
                root,
                "test \"${DYLD_INSERT_LIBRARIES+x}\" != x\n"
                "test \"${LD_PRELOAD+x}\" != x\n"
                "test \"${PYTHONPATH+x}\" != x\n"
                "read value\n"
                "printf '%s %s %s %s %s\\n' \"$value\" \"$1\" "
                "\"$OMP_NUM_THREADS\" \"$OPENBLAS_NUM_THREADS\" "
                "\"$VECLIB_MAXIMUM_THREADS\"\n",
            )
            input_file = root / "input.txt"
            input_file.write_text("frozen-source\n", encoding="ascii")
            log = root / "run.log"
            poisoned = {
                "DYLD_INSERT_LIBRARIES": "/untrusted/inject.dylib",
                "LD_PRELOAD": "/untrusted/preload.so",
                "PYTHONPATH": "/untrusted/python",
                "OMP_NUM_THREADS": "99",
            }
            with mock.patch.dict(os.environ, poisoned, clear=False):
                elapsed = bounded.run(
                    "prepare", executable, input_file, log, ["argument"]
                )
            self.assertGreaterEqual(elapsed, 0.0)
            self.assertEqual(
                log.read_text(encoding="ascii"),
                "frozen-source argument 1 1 1\n",
            )

    def test_success_without_input(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "printf 'ok\\n'\n")
            log = root / "run.log"
            bounded.run("posterior", executable, None, log, [])
            self.assertEqual(log.read_bytes(), b"ok\n")

    def test_cli_rejects_too_few_arguments(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            bounded.main([])
        self.assertIn("expected PROFILE", str(caught.exception))

    def test_unknown_profile_is_rejected_without_creating_log(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "exit 0\n")
            log = root / "run.log"
            with self.assertRaises(SystemExit) as caught:
                bounded.run("dragon", executable, None, log, [])
            self.assertIn("unknown profile", str(caught.exception))
            self.assertFalse(log.exists())

    def test_refuses_existing_log_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "exit 0\n")
            log = root / "run.log"
            log.write_text("sentinel\n", encoding="ascii")
            with self.assertRaises(SystemExit):
                bounded.run("build", executable, None, log, [])
            self.assertEqual(log.read_text(encoding="ascii"), "sentinel\n")

    def test_refuses_symlink_executable_input_and_log(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "exit 0\n")
            executable_alias = root / "helper-alias"
            executable_alias.symlink_to(executable)
            with self.assertRaises(SystemExit):
                bounded.run(
                    "build", executable_alias, None, root / "a.log", []
                )

            input_file = root / "input"
            input_file.write_text("value\n", encoding="ascii")
            input_alias = root / "input-alias"
            input_alias.symlink_to(input_file)
            with self.assertRaises(SystemExit):
                bounded.run(
                    "prepare", executable, input_alias, root / "b.log", []
                )

            target = root / "target.log"
            log_alias = root / "c.log"
            log_alias.symlink_to(target)
            with self.assertRaises(SystemExit):
                bounded.run("posterior", executable, None, log_alias, [])
            self.assertFalse(target.exists())

    def test_nonzero_exit_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "exit 7\n")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(
                    "posterior", executable, None, root / "run.log", []
                )
            self.assertIn("exit status 7", str(caught.exception))
            self.assertIn(
                "INVALID-NO-SCIENTIFIC-RESULT", str(caught.exception)
            )

    def test_wall_timeout_terminates_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "sleep 30\n")
            with self.patched_profile("build", wall_seconds=0.15):
                start = time.monotonic()
                with self.assertRaises(SystemExit) as caught:
                    bounded.run(
                        "build", executable, None, root / "run.log", []
                    )
            self.assertLess(time.monotonic() - start, 2.0)
            self.assertIn("wall timeout", str(caught.exception))

    def test_file_size_limit_is_inherited(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(
                root,
                "dd if=/dev/zero of=oversized.bin bs=4096 count=1 "
                "2>/dev/null\n",
            )
            with self.patched_profile(
                "build", file_bytes=1024, log_bytes=16 * 1024
            ):
                with self.assertRaises(SystemExit) as caught:
                    bounded.run(
                        "build", executable, None, root / "run.log", []
                    )
            self.assertIn(
                "INVALID-NO-SCIENTIFIC-RESULT", str(caught.exception)
            )
            payload = root / "oversized.bin"
            self.assertTrue(payload.exists())
            self.assertLessEqual(payload.stat().st_size, 1024)

    def test_live_log_limit_terminates_writer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(
                root,
                "while :; do printf '0123456789abcdef0123456789abcdef\\n'; "
                "done\n",
            )
            with self.patched_profile(
                "build",
                wall_seconds=2,
                file_bytes=1024 * 1024,
                log_bytes=256,
            ):
                start = time.monotonic()
                with self.assertRaises(SystemExit) as caught:
                    bounded.run(
                        "build", executable, None, root / "run.log", []
                    )
            self.assertLess(time.monotonic() - start, 2.0)
            self.assertIn("live log cap exceeded", str(caught.exception))

    def test_successful_leader_with_lingering_child_is_cleaned_and_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(
                root,
                "sleep 30 &\n"
                "descendant=$!\n"
                "printf '%s\\n' \"$descendant\" > descendant.pid\n"
                "exit 0\n",
            )
            with self.assertRaises(SystemExit) as caught:
                bounded.run(
                    "posterior", executable, None, root / "run.log", []
                )
            self.assertIn("lingering process-group member", str(caught.exception))
            descendant_pid = int(
                (root / "descendant.pid").read_text(encoding="ascii").strip()
            )
            self.assert_process_gone(descendant_pid)

    def test_external_signal_cleans_child_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(
                root,
                "printf '%s\\n' \"$$\" > signal-child.pid\n"
                "while :; do sleep 1; done\n",
            )
            runner = Path(bounded.__file__).resolve()
            wrapper = subprocess.Popen(
                [
                    sys.executable,
                    str(runner),
                    "build",
                    str(executable),
                    "-",
                    str(root / "run.log"),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            marker = root / "signal-child.pid"
            deadline = time.monotonic() + 2.0
            while not marker.exists() and time.monotonic() < deadline:
                if wrapper.poll() is not None:
                    break
                time.sleep(0.02)
            self.assertTrue(marker.exists(), "wrapper child did not start")
            child_pid = int(marker.read_text(encoding="ascii").strip())
            wrapper.send_signal(signal.SIGTERM)
            output, _ = wrapper.communicate(timeout=3.0)
            self.assertNotEqual(wrapper.returncode, 0)
            self.assertIn("received SIGTERM", output)
            self.assert_process_gone(child_pid)

    def test_profiles_and_leader_rss_semantics_are_frozen(self) -> None:
        mib = 1024**2
        gib = 1024**3
        self.assertEqual(
            bounded.PROFILES,
            {
                "prepare": {
                    "wall_seconds": 30,
                    "cpu_seconds": 20,
                    "rss_bytes": 2 * gib,
                    "file_bytes": 512 * mib,
                    "log_bytes": 16 * mib,
                },
                "build": {
                    "wall_seconds": 30,
                    "cpu_seconds": 20,
                    "rss_bytes": 2 * gib,
                    "file_bytes": 128 * mib,
                    "log_bytes": 16 * mib,
                },
                "posterior": {
                    "wall_seconds": 30,
                    "cpu_seconds": 20,
                    "rss_bytes": 2 * gib,
                    "file_bytes": 16 * mib,
                    "log_bytes": 16 * mib,
                },
            },
        )
        self.assertEqual(bounded.RSS_SAMPLE_SECONDS, 0.05)
        self.assertEqual(bounded.TERM_GRACE_SECONDS, 5.0)
        self.assertNotIn("dragon", bounded.PROFILES)


if __name__ == "__main__":
    unittest.main()

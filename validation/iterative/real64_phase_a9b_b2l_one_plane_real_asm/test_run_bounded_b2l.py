#!/usr/bin/env python3
"""No-Dragon tests for the B2l process-group and resource wrapper."""

from __future__ import annotations

from pathlib import Path
import stat
import tempfile
import unittest

import run_bounded_b2l as bounded


class BoundedB2LTest(unittest.TestCase):
    def make_executable(self, root: Path, body: str) -> Path:
        path = root / "fake-executable"
        path.write_text("#!/bin/sh\nset -eu\n" + body, encoding="ascii")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def test_success_without_input(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root, "printf 'ok\\n'\n")
            log = root / "run.log"
            elapsed = bounded.run("asm",executable,None,log,[])
            self.assertGreaterEqual(elapsed,0.0)
            self.assertEqual(log.read_bytes(),b"ok\n")

    def test_success_with_input_and_argument(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root,"read value\nprintf '%s %s\\n' \"$value\" \"$1\"\n")
            deck = root / "deck.x2m"
            log = root / "run.log"
            deck.write_text("deck-value\n",encoding="ascii")
            bounded.run("asm",executable,deck,log,["argument"])
            self.assertEqual(
                log.read_text(encoding="ascii"), "deck-value argument\n"
            )

    def test_completed_child_wins_rss_exit_race(self) -> None:
        class CompletedChild:
            pid = 31415

            def poll(self):
                return None

            def wait(self,timeout=None):
                self.timeout = timeout
                return 0

        child = CompletedChild()
        original = bounded.process_rss_bytes

        def vanished_process(_pid: int) -> int:
            raise ProcessLookupError("child already exited")

        bounded.process_rss_bytes = vanished_process
        try:
            return_code = bounded.wait_bounded(
                child,bounded.PROFILES["asm"]
            )
        finally:
            bounded.process_rss_bytes = original
        self.assertEqual(return_code,0)
        self.assertEqual(child.timeout,bounded.EXIT_CENSUS_GRACE_SECONDS)

    def test_timeout_terminates_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root,"sleep 30\n")
            log = root / "run.log"
            original = bounded.PROFILES["asm"]["wall_seconds"]
            bounded.PROFILES["asm"]["wall_seconds"] = 0.1
            try:
                with self.assertRaises(SystemExit) as caught:
                    bounded.run("asm",executable,None,log,[])
            finally:
                bounded.PROFILES["asm"]["wall_seconds"] = original
            self.assertIn(
                "INVALID-NO-SCIENTIFIC-RESULT", str(caught.exception)
            )

    def test_refuses_existing_log(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            executable = self.make_executable(root,"exit 0\n")
            log = root / "run.log"
            log.write_text("sentinel\n",encoding="ascii")
            with self.assertRaises(SystemExit):
                bounded.run("asm",executable,None,log,[])
            self.assertEqual(log.read_text(encoding="ascii"),"sentinel\n")

    def test_profiles_are_frozen(self) -> None:
        self.assertEqual(bounded.PROFILES["prepare"]["wall_seconds"],30)
        self.assertEqual(bounded.PROFILES["prepare"]["cpu_seconds"],20)
        self.assertEqual(bounded.PROFILES["asm"]["wall_seconds"],15)
        self.assertEqual(bounded.PROFILES["asm"]["cpu_seconds"],10)
        self.assertEqual(bounded.TERM_GRACE_SECONDS,5)
        self.assertEqual(bounded.EXIT_CENSUS_GRACE_SECONDS,0.1)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""No-Dragon tests for the Stage-4 v2 bounded process wrapper."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import stat
import tempfile
import unittest

import run_inner_sensitivity_v2_process as bounded


class BoundedProcessTest(unittest.TestCase):
    def executable(self, root: Path, body: str) -> Path:
        path = root / "fake-dragon"
        path.write_text("#!/bin/sh\nset -eu\n" + body, encoding="ascii")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def test_success(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.executable(root, "printf 'ok\\n'\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            (root / "tmp").mkdir()
            self.assertEqual(
                bounded.run(dragon, deck, root, log, 2.0),
                0,
            )
            self.assertEqual(log.read_bytes(), b"ok\n")

    def test_timeout_kills_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.executable(root, "sleep 10\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            (root / "tmp").mkdir()
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit):
                    bounded.run(dragon, deck, root, log, 0.1)
            self.assertIn("INVALID-NO-SCIENTIFIC-RESULT", stderr.getvalue())

    def test_timeout_cannot_exceed_frozen_bound(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.executable(root, "exit 0\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            (root / "tmp").mkdir()
            with self.assertRaises(SystemExit):
                bounded.run(dragon, deck, root, log, 120.001)
            self.assertFalse(log.exists())

    def test_refuses_existing_log(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.executable(root, "exit 0\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            log.write_text("sentinel\n", encoding="ascii")
            (root / "tmp").mkdir()
            with self.assertRaises(SystemExit):
                bounded.run(dragon, deck, root, log, 2.0)
            self.assertEqual(log.read_text(encoding="ascii"), "sentinel\n")

    def test_log_must_be_inside_work_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            work = root / "work"
            work.mkdir()
            (work / "tmp").mkdir()
            dragon = self.executable(root, "exit 0\n")
            deck = work / "case.x2m"
            deck.write_text("ignored\n", encoding="ascii")
            with self.assertRaises(SystemExit):
                bounded.run(dragon, deck, work, root / "case.log", 2.0)


if __name__ == "__main__":
    unittest.main()

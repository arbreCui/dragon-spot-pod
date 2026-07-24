#!/usr/bin/env python3
"""No-Dragon unit tests for the bounded process wrapper."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import stat
import tempfile
import unittest

import run_bounded_dragon as bounded


class BoundedDragonTest(unittest.TestCase):
    def make_executable(self, root: Path, body: str) -> Path:
        path = root / "fake-dragon"
        path.write_text("#!/bin/sh\nset -eu\n" + body, encoding="ascii")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def test_success(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.make_executable(root, "printf 'ok\\n'\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            self.assertEqual(bounded.run(dragon, deck, log, 2.0), 0)
            self.assertEqual(log.read_bytes(), b"ok\n")

    def test_timeout_kills_exact_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.make_executable(root, "sleep 10\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, log, 0.1)
            self.assertIn("no scientific result", str(caught.exception))

    def test_refuses_existing_log(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dragon = self.make_executable(root, "exit 0\n")
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            log.write_text("sentinel\n", encoding="ascii")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, log, 2.0)
            self.assertIn("refusing to overwrite", str(caught.exception))
            self.assertEqual(log.read_text(encoding="ascii"), "sentinel\n")

    def test_cli_text_is_stable(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            with self.assertRaises(SystemExit):
                bounded.fail("sentinel")
        self.assertEqual(stream.getvalue(), "")


if __name__ == "__main__":
    unittest.main()

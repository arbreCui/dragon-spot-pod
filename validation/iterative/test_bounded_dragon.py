#!/usr/bin/env python3
"""No-Dragon unit tests for the bounded process wrapper."""

from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
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

    def test_sigterm_cleans_child_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            group_file = root / "group.pgid"
            descendant_file = root / "descendant.pid"
            stopped = root / "stopped"
            dragon = self.make_executable(
                root,
                "trap 'printf stopped > \"$STOP_FILE\"; exit 0' "
                "HUP INT TERM\n"
                "sh -c 'trap \"\" HUP INT TERM; "
                "while :; do sleep 1; done' &\n"
                "descendant=$!\n"
                'printf "%s\\n" "$$" > "$GROUP_FILE"\n'
                'printf "%s\\n" "$descendant" > "$DESCENDANT_FILE"\n'
                'wait "$descendant"\n',
            )
            deck = root / "case.x2m"
            log = root / "case.log"
            deck.write_text("ignored\n", encoding="ascii")
            code = (
                "import sys; from pathlib import Path; "
                "import run_bounded_dragon as bounded; "
                "bounded.TERM_GRACE_SECONDS = 0.1; "
                "bounded.run(Path(sys.argv[1]), Path(sys.argv[2]), "
                "Path(sys.argv[3]), 10.0)"
            )
            environment = os.environ.copy()
            module_dir = str(Path(bounded.__file__).resolve().parent)
            old_pythonpath = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = module_dir + (
                os.pathsep + old_pythonpath if old_pythonpath else ""
            )
            environment["GROUP_FILE"] = str(group_file)
            environment["DESCENDANT_FILE"] = str(descendant_file)
            environment["STOP_FILE"] = str(stopped)
            wrapper = subprocess.Popen(
                [sys.executable, "-c", code, str(dragon), str(deck), str(log)],
                env=environment,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            pgid = None
            try:
                deadline = time.monotonic() + 2.0
                while not (group_file.is_file() and descendant_file.is_file()):
                    if wrapper.poll() is not None:
                        self.fail("bounded wrapper exited before child startup")
                    if time.monotonic() >= deadline:
                        self.fail("fake child did not start")
                    time.sleep(0.01)
                pgid = int(group_file.read_text())
                descendant = int(descendant_file.read_text())
                self.assertEqual(os.getpgid(descendant), pgid)
                os.kill(wrapper.pid, signal.SIGTERM)
                self.assertNotEqual(wrapper.wait(timeout=2.0), 0)
                self.assertTrue(stopped.is_file())
                deadline = time.monotonic() + 1.0
                while bounded.process_group_exists(pgid):
                    if time.monotonic() >= deadline:
                        self.fail("fake child process group survived cleanup")
                    time.sleep(0.01)
            finally:
                if wrapper.poll() is None:
                    wrapper.kill()
                    wrapper.wait(timeout=2.0)
                if pgid is None and group_file.is_file():
                    pgid = int(group_file.read_text())
                if pgid is not None:
                    try:
                        os.killpg(pgid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_cli_text_is_stable(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            with self.assertRaises(SystemExit):
                bounded.fail("sentinel")
        self.assertEqual(stream.getvalue(), "")


if __name__ == "__main__":
    unittest.main()

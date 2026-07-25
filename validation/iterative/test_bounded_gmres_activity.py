#!/usr/bin/env python3
"""Synthetic-only tests for the bounded GMRES-activity process wrapper."""

from __future__ import annotations

import ast
import os
from pathlib import Path
import shlex
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import run_bounded_gmres_activity as bounded


HERE = Path(__file__).resolve().parent
WRAPPER = HERE / "run_bounded_gmres_activity.py"


class BoundedGmresActivityTests(unittest.TestCase):
    def make_executable(self, root: Path, body: str) -> Path:
        path = root / "fake-dragon"
        path.write_bytes(
            ("#!/bin/sh\nset -eu\n" + body).encode("ascii"),
        )
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path.resolve()

    def make_case(self, root: Path) -> tuple[Path, Path]:
        case = root / "case"
        case.mkdir()
        deck = case / "deck.x2m"
        deck.write_bytes(b"frozen-deck\n")
        (case / "tmp").mkdir(mode=0o700)
        return case, deck

    def test_success_uses_exact_sanitized_process_contract(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            dragon = self.make_executable(
                root,
                """
printf 'stdout-record\\n'
printf 'stderr-record\\n' >&2
printf 'cwd=%s\\n' "$PWD"
IFS= read -r input
printf 'stdin=%s\\n' "$input"
printf 'LC_ALL=%s\\n' "$LC_ALL"
printf 'PATH=%s\\n' "$PATH"
printf 'TMPDIR=%s\\n' "$TMPDIR"
if [ "${SPOT_PARENT_SENTINEL+x}" = x ]; then
  printf 'parent-environment=present\\n'
else
  printf 'parent-environment=absent\\n'
fi
""",
            )
            log = case / "run.log"
            with mock.patch.dict(
                os.environ,
                {"SPOT_PARENT_SENTINEL": "must-not-leak"},
                clear=False,
            ):
                self.assertEqual(bounded.run(dragon, deck, log), 0)

            text = log.read_text(encoding="ascii")
            self.assertIn("stdout-record\n", text)
            self.assertIn("stderr-record\n", text)
            self.assertIn(f"cwd={case.resolve()}\n", text)
            self.assertIn("stdin=frozen-deck\n", text)
            self.assertIn("LC_ALL=C\n", text)
            self.assertIn("PATH=/usr/bin:/bin\n", text)
            self.assertIn(f"TMPDIR={case.resolve() / 'tmp'}\n", text)
            self.assertIn("parent-environment=absent\n", text)
            self.assertNotIn("must-not-leak", text)
            self.assertTrue((case / "tmp").is_dir())
            self.assertEqual(stat.S_IMODE(log.stat().st_mode), 0o600)

    def test_timeout_terminates_only_spawned_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            parent_path = shlex.quote(str(case / "parent.pid"))
            child_path = shlex.quote(str(case / "child.pid"))
            dragon = self.make_executable(
                root,
                f"""
printf '%s\\n' "$$" > {parent_path}
/bin/sleep 30 &
child=$!
printf '%s\\n' "$child" > {child_path}
wait "$child"
""",
            )
            log = case / "run.log"
            with mock.patch.object(
                bounded,
                "TIMEOUT_SECONDS",
                2.0,
            ), mock.patch.object(
                bounded,
                "TERM_GRACE_SECONDS",
                0.25,
            ):
                with self.assertRaises(SystemExit) as caught:
                    bounded.run(dragon, deck, log)
            self.assertIn("no scientific result", str(caught.exception))

            parent_file = case / "parent.pid"
            child_file = case / "child.pid"
            self.assertTrue(parent_file.is_file())
            self.assertTrue(child_file.is_file())
            process_ids = (
                int(parent_file.read_text(encoding="ascii")),
                int(child_file.read_text(encoding="ascii")),
            )
            for process_id in process_ids:
                deadline = time.monotonic() + 2.0
                while time.monotonic() < deadline:
                    try:
                        os.kill(process_id, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.02)
                else:
                    self.fail(
                        f"spawned process {process_id} survived timeout cleanup"
                    )

    def test_nonzero_exit_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            dragon = self.make_executable(root, "exit 7\n")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, case / "run.log")
            self.assertIn("exit status 7", str(caught.exception))
            self.assertIn("no scientific result", str(caught.exception))

    def test_sigterm_terminates_spawned_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            parent_path = shlex.quote(str(case / "parent.pid"))
            child_path = shlex.quote(str(case / "child.pid"))
            dragon = self.make_executable(
                root,
                f"""
printf '%s\\n' "$$" > {parent_path}
/bin/sleep 30 &
child=$!
printf '%s\\n' "$child" > {child_path}
wait "$child"
""",
            )
            log = case / "run.log"
            wrapper = subprocess.Popen(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(dragon),
                    str(deck),
                    str(log),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            parent_file = case / "parent.pid"
            child_file = case / "child.pid"
            deadline = time.monotonic() + 5.0
            while time.monotonic() < deadline:
                if parent_file.is_file() and child_file.is_file():
                    break
                if wrapper.poll() is not None:
                    self.fail("wrapper exited before the signal fixture started")
                time.sleep(0.02)
            else:
                wrapper.kill()
                wrapper.wait()
                self.fail("signal fixture did not publish process IDs")

            process_ids = (
                int(parent_file.read_text(encoding="ascii")),
                int(child_file.read_text(encoding="ascii")),
            )
            os.kill(wrapper.pid, signal.SIGTERM)
            stdout, stderr = wrapper.communicate(timeout=10.0)
            self.assertNotEqual(wrapper.returncode, 0)
            self.assertEqual(stdout, "")
            self.assertIn("received SIGTERM", stderr)
            self.assertIn("no scientific result", stderr)

            for process_id in process_ids:
                deadline = time.monotonic() + 2.0
                while time.monotonic() < deadline:
                    try:
                        os.kill(process_id, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.02)
                else:
                    self.fail(
                        f"spawned process {process_id} survived SIGTERM cleanup"
                    )

    def test_existing_log_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            dragon = self.make_executable(root, "exit 0\n")
            log = case / "run.log"
            log.write_text("sentinel\n", encoding="ascii")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, log)
            self.assertIn("refusing to overwrite", str(caught.exception))
            self.assertEqual(log.read_text(encoding="ascii"), "sentinel\n")
            self.assertTrue((case / "tmp").is_dir())

    def test_case_local_tmp_must_be_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            dragon = self.make_executable(root, "exit 0\n")
            (case / "tmp" / "sentinel").write_bytes(b"not-fresh\n")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, case / "run.log")
            self.assertIn("not fresh and empty", str(caught.exception))
            self.assertFalse((case / "run.log").exists())

    def test_inputs_and_case_directory_reject_symlinks(self) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        cases = ("dragon", "deck", "case")
        for target in cases:
            with self.subTest(target=target):
                with tempfile.TemporaryDirectory() as raw:
                    root = Path(raw)
                    real_case, real_deck = self.make_case(root)
                    real_dragon = self.make_executable(root, "exit 0\n")
                    dragon = real_dragon
                    deck = real_deck
                    log = real_case / "run.log"
                    if target == "dragon":
                        dragon = root / "dragon-link"
                        dragon.symlink_to(real_dragon)
                    elif target == "deck":
                        deck = real_case / "deck-link.x2m"
                        deck.symlink_to(real_deck)
                    else:
                        linked_case = root / "case-link"
                        linked_case.symlink_to(real_case, target_is_directory=True)
                        deck = linked_case / "deck.x2m"
                        log = linked_case / "run.log"
                    with self.assertRaises(SystemExit):
                        bounded.run(dragon, deck, log)

    def test_log_must_share_deck_case_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _case, deck = self.make_case(root)
            other = root / "other"
            other.mkdir()
            dragon = self.make_executable(root, "exit 0\n")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(dragon, deck, other / "run.log")
            self.assertIn("share one isolated case", str(caught.exception))

    def test_executable_path_must_be_absolute(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            case, deck = self.make_case(root)
            self.make_executable(root, "exit 0\n")
            with self.assertRaises(SystemExit) as caught:
                bounded.run(
                    Path("fake-dragon"),
                    deck,
                    case / "run.log",
                )
            self.assertIn("must be absolute", str(caught.exception))

    def test_cli_has_no_timeout_or_retry_override(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER),
                "dragon",
                "deck",
                "log",
                "31",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("expected exactly DRAGON DECK LOG", result.stderr)

    def test_source_has_one_popen_call_and_frozen_controls(self) -> None:
        source = WRAPPER.read_text(encoding="ascii")
        tree = ast.parse(source)
        popen_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "subprocess"
            and node.func.attr == "Popen"
        ]
        self.assertEqual(len(popen_calls), 1)
        keywords = {item.arg: item.value for item in popen_calls[0].keywords}
        self.assertIsInstance(keywords["shell"], ast.Constant)
        self.assertIs(keywords["shell"].value, False)
        self.assertIsInstance(keywords["start_new_session"], ast.Constant)
        self.assertIs(keywords["start_new_session"].value, True)
        self.assertIn("env", keywords)
        self.assertEqual(bounded.TIMEOUT_SECONDS, 30)
        self.assertEqual(bounded.TERM_GRACE_SECONDS, 5)
        self.assertEqual(
            bounded.MANAGED_SIGNALS,
            (signal.SIGHUP, signal.SIGINT, signal.SIGTERM),
        )
        self.assertNotIn("subprocess.run(", source)
        self.assertNotIn("killall", source)
        run_signature = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "run"
        )
        self.assertEqual(
            [argument.arg for argument in run_signature.args.args],
            ["dragon_path", "deck_path", "log_path"],
        )


if __name__ == "__main__":
    unittest.main()

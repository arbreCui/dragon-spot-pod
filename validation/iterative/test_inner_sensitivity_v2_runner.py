#!/usr/bin/env python3
"""No-Dragon state-machine tests for the Stage-4 v2 runner."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

import run_inner_sensitivity_v2 as runner


class LedgerTest(unittest.TestCase):
    def test_capture_and_replay_are_each_one_shot(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            capture = runner.Ledger(root, "capture", "a" * 64)
            capture.reserve()
            capture.finish("PENDING-REPLAY")
            capture.close()

            duplicate = runner.Ledger(root, "capture", "a" * 64)
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    duplicate.reserve()
            duplicate.close()

            replay = runner.Ledger(
                root,
                "replay",
                "b" * 64,
                "a" * 64,
            )
            replay.reserve()
            replay.finish("QUALIFIED-ON-2H-TO-H-SCALE")
            replay.close()

            duplicate_replay = runner.Ledger(
                root,
                "replay",
                "b" * 64,
                "a" * 64,
            )
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    duplicate_replay.reserve()
            duplicate_replay.close()

    def test_unresolved_capture_forbids_replay(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            capture = runner.Ledger(root, "capture", "a" * 64)
            capture.reserve()
            capture.finish("UNRESOLVED")
            capture.close()

            replay = runner.Ledger(
                root,
                "replay",
                "b" * 64,
                "a" * 64,
            )
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    replay.reserve()
            replay.close()
            self.assertFalse((root / "replay-spent.json").exists())

    def test_replay_rejects_tampered_capture_budget_record(self) -> None:
        valid = {
            "schema": "spot-inner-sensitivity-v2-budget-1",
            "mode": "capture",
            "authorization_sha256": "a" * 64,
            "dragon_processes": 1,
            "status": "PENDING-REPLAY",
        }
        mutations = (
            ("schema", "wrong"),
            ("mode", "replay"),
            ("authorization_sha256", "c" * 64),
            ("dragon_processes", 2),
            ("status", "PROCESS-RESERVED"),
        )
        for key, value in mutations:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                data = dict(valid)
                data[key] = value
                (root / "capture-spent.json").write_bytes(
                    runner.canonical_json(data)
                )
                replay = runner.Ledger(
                    root,
                    "replay",
                    "b" * 64,
                    "a" * 64,
                )
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        replay.reserve()
                replay.close()
                self.assertFalse((root / "replay-spent.json").exists())

    def test_lock_release_failure_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            ledger = runner.Ledger(root, "capture", "a" * 64)
            obstruction = ledger.lock / "obstruction"
            obstruction.write_text("x\n", encoding="ascii")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    ledger.close()
            self.assertTrue(ledger.lock.is_dir())
            obstruction.unlink()
            ledger.close()

    def test_scientific_manifest_is_exactly_five_ordered_files(self) -> None:
        rows = []
        for name in runner.SCIENCE_FILES:
            digest = runner.FINE_HASHES.get(name, "1" * 64)
            rows.append(f"{digest}  {name}")
        raw = ("\n".join(rows) + "\n").encode("ascii")
        parsed = runner.parse_science_manifest(raw)
        self.assertEqual(tuple(parsed), runner.SCIENCE_FILES)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.parse_science_manifest(
                    raw + b"2" * 64 + b"  extra.xsm\n"
                )

    def test_artifact_manifest_detects_post_publish_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "a.log").write_text("a\n", encoding="ascii")
            (root / "b.json").write_text("{}\n", encoding="ascii")
            runner.write_artifact_manifest(root)
            runner.verify_artifact_manifest(root)
            (root / "a.log").write_text("tampered\n", encoding="ascii")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    runner.verify_artifact_manifest(root)

    def test_atomic_publication_never_replaces_an_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            (source / "owned").write_text("source\n", encoding="ascii")
            target.mkdir()
            (target / "foreign").write_text("target\n", encoding="ascii")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    runner.rename_no_replace(source, target)
            self.assertTrue((source / "owned").is_file())
            self.assertTrue((target / "foreign").is_file())

    def test_atomic_publication_moves_to_an_absent_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            (source / "owned").write_text("source\n", encoding="ascii")
            runner.rename_no_replace(source, target)
            self.assertFalse(source.exists())
            self.assertEqual(
                (target / "owned").read_text(encoding="ascii"),
                "source\n",
            )

    def test_output_namespace_rejects_nested_or_ledger_paths(self) -> None:
        artifact_root = runner.ROOT / "validation" / "artifacts"
        fine = artifact_root / "iterative-map1"
        seed = artifact_root / "iterative-seed"
        nested = fine / "inner-sensitivity-v2-capture-nested"
        ledger = runner.ROOT / runner.LEDGER_RELATIVE
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.validate_output_path(
                    nested,
                    "capture",
                    fine,
                    seed,
                    None,
                )
            with self.assertRaises(SystemExit):
                runner.validate_output_path(
                    ledger,
                    "capture",
                    fine,
                    seed,
                    None,
                )

    def test_old_ancestor_cannot_authorize_current_implementation(self) -> None:
        root_commit = subprocess.run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=runner.ROOT,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.splitlines()[0]
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.verify_authorized_implementation(root_commit)

    def test_runner_has_no_caller_selectable_ledger(self) -> None:
        source = Path(runner.__file__).read_text(encoding="ascii")
        self.assertNotIn("--ledger-dir", source)
        self.assertIn("LEDGER_RELATIVE", source)


if __name__ == "__main__":
    unittest.main()

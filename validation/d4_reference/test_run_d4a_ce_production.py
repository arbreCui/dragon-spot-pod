#!/usr/bin/env python3
"""Transport-free tests for the frozen D4-A CE production wrapper."""

from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import signal
import stat
import sys
import tempfile
import time
import unittest
from unittest import mock

import run_d4a_ce_production as production


class ProductionWrapperTest(unittest.TestCase):
    def make_builder(self, root: Path, body: str) -> Path:
        path = root / "fake_builder.py"
        path.write_text(body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def inputs(self, root: Path) -> tuple[Path, Path, Path]:
        output = root / "result"
        cross_sections = root / "cross_sections.xml"
        openmc_exec = root / "openmc"
        cross_sections.write_text("<cross_sections/>\n", encoding="ascii")
        openmc_exec.write_text("synthetic; never executed\n", encoding="ascii")
        return output, cross_sections, openmc_exec

    def test_exact_frozen_command(self) -> None:
        output = Path("/tmp/fresh-d4a-ce")
        cross_sections = Path("/tmp/cross_sections.xml")
        openmc_exec = Path("/tmp/openmc")
        builder = Path("/repo/validation/d4_reference/build_d4a_ce_reference.py")
        self.assertEqual(
            production.build_command(
                output, cross_sections, openmc_exec, builder
            ),
            [
                sys.executable,
                str(builder),
                "--output", str(output),
                "--cross-sections", str(cross_sections),
                "--run",
                "--particles", "20000",
                "--batches", "300",
                "--inactive", "100",
                "--seed", "731942",
                "--threads", "18",
                "--openmc-exec", str(openmc_exec),
            ],
        )

    def test_cli_rejects_statistical_overrides(self) -> None:
        argv = [
            "run_d4a_ce_production.py",
            "--output", "/tmp/fresh-d4a-ce",
            "--cross-sections", "/tmp/cross_sections.xml",
            "--openmc-exec", "/tmp/openmc",
            "--particles", "1",
        ]
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    production.parse_args()

    def test_success_preserves_builder_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output, cross_sections, openmc_exec = self.inputs(root)
            builder = self.make_builder(
                root,
                """from pathlib import Path
import sys
output = Path(sys.argv[sys.argv.index('--output') + 1])
output.mkdir()
(output / 'argv.txt').write_text('\\n'.join(sys.argv[1:]) + '\\n')
(output / 'result_receipt.sha256').write_text('synthetic receipt\\n')
""",
            )
            production.run_production(
                output, cross_sections, openmc_exec, builder=builder,
                timeout_seconds=2.0,
            )
            self.assertTrue((output / production.SUCCESS_RECEIPT).is_file())
            self.assertFalse((output / production.INCOMPLETE_MARKER).exists())
            self.assertEqual(
                (output / "argv.txt").read_text().splitlines(),
                production.build_command(
                    output.absolute(), cross_sections.absolute(),
                    openmc_exec.absolute(), builder,
                )[2:],
            )

    def test_nonzero_removes_success_receipt_and_marks_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output, cross_sections, openmc_exec = self.inputs(root)
            builder = self.make_builder(
                root,
                """from pathlib import Path
import sys
output = Path(sys.argv[sys.argv.index('--output') + 1])
output.mkdir()
(output / 'result_receipt.sha256').write_text('must be removed\\n')
raise SystemExit(7)
""",
            )
            with self.assertRaisesRegex(
                production.ProductionFailure, "builder exit status 7"
            ):
                production.run_production(
                    output, cross_sections, openmc_exec, builder=builder,
                    timeout_seconds=2.0,
                )
            self.assertFalse((output / production.SUCCESS_RECEIPT).exists())
            self.assertEqual(
                (output / production.INCOMPLETE_MARKER).read_text(),
                "INCOMPLETE: builder exit status 7\n",
            )

    def test_timeout_kills_group_and_removes_success_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output, cross_sections, openmc_exec = self.inputs(root)
            builder = self.make_builder(
                root,
                """from pathlib import Path
import os
import signal
import subprocess
import sys
import time
output = Path(sys.argv[sys.argv.index('--output') + 1])
output.mkdir()
(output / 'result_receipt.sha256').write_text('must be removed\\n')
child = subprocess.Popen([
    sys.executable, '-c',
    'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)'
])
(output / 'pgid.txt').write_text(str(os.getpgrp()))
(output / 'child.pid').write_text(str(child.pid))
signal.signal(signal.SIGTERM, signal.SIG_IGN)
time.sleep(30)
""",
            )
            with self.assertRaisesRegex(
                production.ProductionFailure, "wall cap exceeded"
            ):
                production.run_production(
                    output, cross_sections, openmc_exec, builder=builder,
                    timeout_seconds=0.2, term_grace_seconds=0.1,
                )
            pgid = int((output / "pgid.txt").read_text())
            child = int((output / "child.pid").read_text())
            self.assertFalse((output / production.SUCCESS_RECEIPT).exists())
            self.assertIn(
                "INCOMPLETE: 900-second process-group wall cap exceeded",
                (output / production.INCOMPLETE_MARKER).read_text(),
            )
            deadline = time.monotonic() + 1.0
            while production.process_group_exists(pgid):
                if time.monotonic() >= deadline:
                    self.fail("timed-out process group survived cleanup")
                time.sleep(0.01)
            with self.assertRaises(ProcessLookupError):
                os.kill(child, 0)


if __name__ == "__main__":
    unittest.main()

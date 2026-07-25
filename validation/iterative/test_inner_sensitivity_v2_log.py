#!/usr/bin/env python3
"""Synthetic no-Dragon tests for the Stage-4 v2 raw-log checker."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import check_inner_sensitivity_v2_log as checker


EPS = "9.99999997E-07"


def echo(payload: str, source: int) -> str:
    return f">|{payload}|>{source:04d}"


def terminal(keff: str = "1.0", *, state: int = 1, maxout: int = 500) -> list[str]:
    return [
        "FLU2DR-TERM OUTER-GATE=PASS "
        f"IEXTF= 3 MAXOUT= {maxout} KEFF= {keff} "
        f"EEXT= 0.0 EPSOUT= {EPS} "
        f"EUNK= 0.0 EPSUNK= {EPS} EUNK-VALID=1",
        "FLU2DR-TERM INNER-TERMINAL "
        "ITERF= 4 MAXINR= 740 "
        f"EINR= 0.0 EPSINR= {EPS} "
        f"IGDEB= 371 STATE={state} NGRP= 370",
    ]


def valid_log() -> str:
    lines = [
        echo("STAGE4V2-COARSE-BEGIN", 1),
        echo("STAGE4V2-COARSE-RANK 1", 2),
        echo("STAGE4V2-COARSE-TOLERANCE 1.000000E-06", 3),
        echo("STAGE4V2-COARSE-X0-REUSED", 4),
        echo("STAGE4V2-COARSE-STATE0 1.20", 5),
        "SPOLEAK DIRECT ERROR/MIN/MAX 0.0 0.0 1.0",
        echo("STAGE4V2-COARSE-LEAKAGE0 0.0", 6),
        echo("STAGE4V2-COARSE-RADIAL-BEGIN", 7),
    ]
    for plane in range(1, 4):
        lines.append(echo(f"SPOT-REFRESH-FS-PLANE {plane} OF 3", 20))
        lines.extend(terminal())
        lines.append(
            echo(f"SPOT-REFRESH-FS-RESULT {plane} 1.0 0.0", 30)
        )
    lines.extend(
        [
            echo("STAGE4V2-COARSE-RADIAL-END", 8),
            echo(
                "STAGE4V2-COARSE-RADIAL-CONTRACT 1 3 0.0 1.0 1.0",
                9,
            ),
            echo("STAGE4V2-COARSE-AXIAL-BEGIN", 10),
            *terminal("1.21"),
            echo("STAGE4V2-COARSE-AXIAL-END", 11),
            echo("STAGE4V2-COARSE-DOUT-2H 0.1 0.2 0.3 0.4", 12),
            echo("STAGE4V2-COARSE-STATE1 1.21", 13),
            "SPOLEAK DIRECT ERROR/MIN/MAX 0.3 0.0 1.0",
            echo("STAGE4V2-COARSE-LEAKAGE1 0.3", 14),
            echo("STAGE4V2-COARSE-COMPLETE", 15),
            "normal end of execution for dragon",
            "check for warning in listing",
            "before assuming your run was successful",
        ]
    )
    return "\n".join(lines) + "\n"


class RawLogTest(unittest.TestCase):
    def run_checker(self, text: str) -> tuple[int, str, str]:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "dragon.log"
            path.write_text(text, encoding="ascii")
            stdout = io.StringIO()
            stderr = io.StringIO()
            code = 0
            with mock.patch("sys.argv", ["checker", str(path)]):
                with contextlib.redirect_stdout(stdout):
                    with contextlib.redirect_stderr(stderr):
                        try:
                            checker.main()
                        except SystemExit as exc:
                            code = int(exc.code)
            return code, stdout.getvalue(), stderr.getvalue()

    def assert_invalid(self, text: str, message: str) -> None:
        code, stdout, stderr = self.run_checker(text)
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn(message, stderr)

    def test_valid_three_plus_one_log(self) -> None:
        code, stdout, stderr = self.run_checker(valid_log())
        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("3 radial + 1 axial", stdout)

    def test_missing_terminal_pair_is_invalid(self) -> None:
        text = valid_log().replace(
            "FLU2DR-TERM INNER-TERMINAL "
            "ITERF= 4 MAXINR= 740 "
            f"EINR= 0.0 EPSINR= {EPS} "
            "IGDEB= 371 STATE=1 NGRP= 370\n",
            "",
            1,
        )
        self.assert_invalid(text, "four paired FLU terminal")

    def test_nonterminal_state_is_invalid(self) -> None:
        text = valid_log().replace("STATE=1", "STATE=0", 1)
        self.assert_invalid(text, "lacks a strict terminal state")

    def test_changed_maxout_is_invalid(self) -> None:
        text = valid_log().replace("MAXOUT= 500", "MAXOUT= 501", 1)
        self.assert_invalid(text, "changed an iteration cap")

    def test_changed_tolerance_is_invalid(self) -> None:
        text = valid_log().replace(EPS, "2.00000000E-06", 1)
        self.assert_invalid(text, "tolerance differs")

    def test_extra_solve_is_invalid(self) -> None:
        insertion = "\n".join(terminal()) + "\n"
        text = valid_log().replace(
            echo("STAGE4V2-COARSE-AXIAL-END", 11),
            insertion + echo("STAGE4V2-COARSE-AXIAL-END", 11),
        )
        self.assert_invalid(text, "four paired FLU terminal")

    def test_abnormal_marker_is_invalid(self) -> None:
        text = valid_log().replace(
            echo("STAGE4V2-COARSE-COMPLETE", 15),
            "XABORT sentinel\n" + echo("STAGE4V2-COARSE-COMPLETE", 15),
        )
        self.assert_invalid(text, "abnormal termination")

    def test_spogbal_call_is_invalid(self) -> None:
        text = valid_log().replace(
            echo("STAGE4V2-COARSE-AXIAL-END", 11),
            echo("STAGE4V2-COARSE-AXIAL-END", 11)
            + "\nSPOGBAL GLOBAL/MAX-GROUP 0.0 0.0",
        )
        self.assert_invalid(text, "unsafe production SPOGBAL")


if __name__ == "__main__":
    unittest.main()

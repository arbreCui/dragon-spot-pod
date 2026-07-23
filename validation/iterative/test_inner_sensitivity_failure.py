#!/usr/bin/env python3
"""Synthetic fail-closed tests for check_inner_sensitivity_failure.py."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_inner_sensitivity_failure.py"
PROTOCOL = HERE / "inner_sensitivity_protocol.json"


def echo(payload: str, source_line: int) -> str:
    return f">|{payload:<100}|>{source_line:04d}"


def pass_pair(eps: str, iextf: int, eunk: str) -> list[str]:
    return [
        (
            " FLU2DR-TERM OUTER-GATE=PASS "
            f"IEXTF={iextf:6d} MAXOUT={500:6d} "
            "KEFF=  1.3641711346919385E+00 "
            f"EEXT=  1.00000000E-09 EPSOUT=  {eps} "
            f"EUNK=  {eunk} EPSUNK=  {eps} EUNK-VALID=1"
        ),
        (
            " FLU2DR-TERM INNER-TERMINAL "
            f"ITERF={1:6d} MAXINR={740:6d} "
            f"EINR=  {eunk} EPSINR=  {eps} "
            f"IGDEB={371:6d} STATE=1 NGRP={370:6d}"
        ),
    ]


def failure_pair(plane: int) -> list[str]:
    eunk = (
        "5.03026570E-07",
        "5.29328702E-07",
        "6.19920286E-07",
    )[plane - 1]
    igdeb = (50, 47, 29)[plane - 1]
    return [
        (
            " FLU2DR-DIAG OUTER "
            f"IEXTF={500:6d} MAXOUT={500:6d} "
            "KEFF=  1.0000000000000000E+00 "
            "EEXT=  0.00000000E+00 EPSOUT=  2.49999999E-07 "
            f"EUNK=  {eunk} EPSUNK=  2.49999999E-07 EUNK-VALID=1"
        ),
        (
            " FLU2DR-DIAG INNER "
            f"ITERF={1:6d} MAXINR={740:6d} "
            f"EINR=  {eunk} EPSINR=  2.49999999E-07 "
            f"IGDEB={igdeb:6d} STATE=2 NGRP={370:6d}"
        ),
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
    ]


def valid_log() -> str:
    rows = [
        echo("ITERATIVE-MAP-BEGIN", 29),
        echo("ITERATIVE-MAP-RANK 1", 30),
        echo("ITERATIVE-MAP-INIT-TOLERANCE 5.000000e-07", 31),
        echo("ITERATIVE-MAP-MAP-TOLERANCE 2.500000e-07", 32),
        echo("ITERATIVE-MAP-BASIS-BUILT", 40),
        *pass_pair("4.99999999E-07", 134, "4.89227034E-07"),
        echo("ITERATIVE-MAP-STATE0 1.364171e+00", 50),
        echo("ITERATIVE-MAP-LEAKAGE0 1.466176e-03", 53),
        echo("ITERATIVE-MAP-RADIAL-BEGIN", 60),
    ]
    for plane in range(1, 4):
        rows.extend(
            [
                echo(f"SPOT-REFRESH-FS-PLANE {plane} OF 3", 23),
                *failure_pair(plane),
                echo(
                    (
                        f"SPOT-REFRESH-FS-RESULT {plane} "
                        "7.000000e-05 3.000000e-07"
                    ),
                    33,
                ),
            ]
        )
    rows.extend(
        [
            echo("ITERATIVE-MAP-RADIAL-END", 63),
            echo(
                (
                    "ITERATIVE-MAP-RADIAL-CONTRACT 1 3 "
                    "3.000000E-07 2.000000E-07 3.000000E-07"
                ),
                72,
            ),
            *pass_pair("2.49999999E-07", 193, "2.46326749E-07"),
            echo(
                (
                    "ITERATIVE-MAP-RAW-DEFECT-X0 "
                    "1.0E-06 8.0E-04 1.2E-06 1.5E-05"
                ),
                90,
            ),
            echo("ITERATIVE-MAP-STATE1 1.364174e+00 4.0e-09 3.2e-03", 91),
            echo("ITERATIVE-MAP-LEAKAGE1 1.2e-06", 94),
            echo("ITERATIVE-MAP-COMPLETE", 98),
            "<|END: ;                                                                 |<0099",
            "cle2000_c: cpu time= 1.000 second",
            "normal end of execution for dragon",
            "check for warning in listing",
            "before assuming your run was successful",
        ]
    )
    return "\n".join(rows) + "\n"


class FailureReceiptTest(unittest.TestCase):
    maxDiff = None

    def run_checker(
        self,
        log_text: str,
        protocol: Path = PROTOCOL,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".log",
        ) as stream:
            stream.write(log_text)
            stream.flush()
            return subprocess.run(
                [sys.executable, str(CHECKER), stream.name, str(protocol)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_valid_failure_receipt(self) -> None:
        result = self.run_checker(valid_log())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "CAPTURE INVALID-INNER-NONCONVERGENCE",
                (
                    "PLANE 1 IEXTF=500 IGDEB=50 "
                    "EUNK=5.03026570E-07 EPS=2.49999999E-07"
                ),
                (
                    "PLANE 2 IEXTF=500 IGDEB=47 "
                    "EUNK=5.29328702E-07 EPS=2.49999999E-07"
                ),
                (
                    "PLANE 3 IEXTF=500 IGDEB=29 "
                    "EUNK=6.19920286E-07 EPS=2.49999999E-07"
                ),
                "STAGE4 INVALID",
                "STAGE5 NOT-AUTHORIZED",
                "OUTER-CONVERGENCE NOT-EVALUATED",
            ],
        )

    def test_log_tampering_fails_closed(self) -> None:
        valid = valid_log()
        tampered = {
            "missing warning": valid.replace(
                " *** FLU2DR: CONVERGENCE NOT REACHED ***\n",
                "",
                1,
            ),
            "radial did not exhaust": valid.replace(
                "IEXTF=   500 MAXOUT=   500",
                "IEXTF=   499 MAXOUT=   500",
                1,
            ),
            "radial state pass": valid.replace(
                "IGDEB=    50 STATE=2",
                "IGDEB=    50 STATE=1",
                1,
            ),
            "radial all groups": valid.replace(
                "IGDEB=    50 STATE=2",
                "IGDEB=   371 STATE=2",
                1,
            ),
            "EUNK below EPS": valid.replace(
                "EUNK=  5.03026570E-07",
                "EUNK=  2.00000000E-07",
                1,
            ),
            "EINR below EPS": valid.replace(
                "EINR=  5.03026570E-07",
                "EINR=  2.00000000E-07",
                1,
            ),
            "initializer not pass": valid.replace(
                "FLU2DR-TERM OUTER-GATE=PASS",
                "FLU2DR-DIAG OUTER             ",
                1,
            ),
            "returned axial not pass": valid.replace(
                "IEXTF=   193 MAXOUT=   500",
                "IEXTF=   500 MAXOUT=   500",
                1,
            ),
            "missing completion": valid.replace(
                echo("ITERATIVE-MAP-COMPLETE", 98) + "\n",
                "",
            ),
            "scientific qualification claim": valid.replace(
                "normal end of execution for dragon",
                "STAGE4 QUALIFIED\nnormal end of execution for dragon",
            ),
        }
        for name, log_text in tampered.items():
            with self.subTest(name=name):
                result = self.run_checker(log_text)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(
                    result.stderr.startswith(
                        "INNER-SENSITIVITY FAILURE FAIL:"
                    ),
                    result.stderr,
                )
                self.assertEqual(result.stdout, "")

    def test_protocol_tampering_fails_closed(self) -> None:
        protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        protocol["refined_map_solver_eps_f32_bits"] = "0x348637bc"
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json",
        ) as stream:
            json.dump(protocol, stream)
            stream.flush()
            result = self.run_checker(valid_log(), Path(stream.name))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "protocol differs from the frozen Stage-4 contract",
            result.stderr,
        )
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()

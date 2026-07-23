#!/usr/bin/env python3
"""Synthetic tests for the bounded radial-floor status machine."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_radial_floor_status.py"
PROTOCOL = HERE / "radial_floor_protocol.json"
NORMAL_END = " normal end of execution for dragon 5  Version 5.1.0"


def echo(payload: str, source_line: int) -> str:
    return f">|{payload:<100}|>{source_line:04d}"


def terminal_pair(
    kind: str,
    iextf: int,
    maxout: int,
    eunk: str,
    einr: str,
    igdeb: int,
    state: int,
) -> list[str]:
    outer_label = "OUTER-GATE=PASS" if kind == "TERM" else "OUTER"
    inner_label = "INNER-TERMINAL" if kind == "TERM" else "INNER"
    return [
        (
            f" FLU2DR-{kind} {outer_label} "
            f"IEXTF={iextf:6d} MAXOUT={maxout:6d} "
            "KEFF=  1.0000000000000000E+00 "
            "EEXT=  0.00000000E+00 EPSOUT=  2.49999999E-07 "
            f"EUNK=  {eunk} EPSUNK=  2.49999999E-07 EUNK-VALID=1"
        ),
        (
            f" FLU2DR-{kind} {inner_label} "
            f"ITERF={1:6d} MAXINR={740:6d} "
            f"EINR=  {einr} EPSINR=  2.49999999E-07 "
            f"IGDEB={igdeb:6d} STATE={state} NGRP={370:6d}"
        ),
    ]


def header(maxout: int, free_steps: int, accelerated_steps: int) -> list[str]:
    return [
        " CALCULATION TYPE            =    SOURCE",
        " FLUX SOLUTION DOOR          = ** MCCG **",
        " NB. OF GROUPS               =       370",
        f" MAX. OUTER ITERATIONS       ={maxout:10d}",
        f" MAX. THERMAL ITERATIONS     ={740:10d}",
        (
            " ACCELERATION SCHEME         =("
            f"{free_steps:2d} FREE,{accelerated_steps:2d} ACCELERATED)"
        ),
        " REBALANCING OPTION          = ON ",
    ]


def history(
    steps: int,
    free_steps: int,
    accelerated_steps: int,
    final_eunk: str,
    final_einr: str,
    final_igdeb: int,
) -> list[str]:
    rows: list[str] = []
    for step in range(1, steps + 1):
        is_final = step == steps
        einr = final_einr if is_final else "7.00E-07"
        eunk = final_eunk if is_final else "8.00E-07"
        igdeb = final_igdeb if is_final else 20
        # Inner counters restart in each outer iteration.  Its first free
        # iteration and every stationary iteration must print ZMU=1.
        rows.append(
            f"          IN({1:3d}) FLX: PRC= {einr} "
            "TAR= 2.50E-07 "
            f"IGDEB={igdeb:13d} ACCE={1.0:12.5f}"
        )
        zmu = 1.0
        if accelerated_steps > 0 and step > free_steps:
            zmu = 0.75
        rows.append(
            f" OUT({step:3d}) FLX: PRC= {eunk} "
            "TAR= 2.50E-07 FNOR= 1.000000E+00 "
            f"ACCE={zmu:12.5f}"
        )
    return rows


def main_arm_log(
    arm_id: str,
    state: str,
    strict_step: int = 4,
) -> str:
    free_steps, accelerated_steps = (
        (3, 3) if arm_id == "NATIVE" else (1, 0)
    )
    if state == "STRICT":
        steps = strict_step
        kind = "TERM"
        eunk = "2.00000000E-07"
        einr = "1.50000000E-07"
        igdeb = 371
        inner_state = 1
        warnings: list[str] = []
    elif state == "CAP":
        steps = 6
        kind = "DIAG"
        eunk = "3.00000000E-07"
        einr = "3.20000000E-07"
        igdeb = 50
        inner_state = 2
        warnings = [
            " *** FLU2DR: CONVERGENCE NOT REACHED ***",
            " *** FLU2DR: CONVERGENCE NOT REACHED ***",
            " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        ]
    else:
        raise ValueError(state)
    rows = [
        echo(f"RADIAL-FLOOR-ARM-BEGIN {arm_id}", 20),
        echo("RADIAL-FLOOR-ARM-HISTORY RESET", 21),
        echo(
            (
                "RADIAL-FLOOR-ARM-CONTROLS 6 740 2.500000E-07 "
                f"{free_steps} {accelerated_steps}"
            ),
            22,
        ),
        *header(6, free_steps, accelerated_steps),
        *history(
            steps,
            free_steps,
            accelerated_steps,
            eunk,
            einr,
            igdeb,
        ),
        *terminal_pair(
            kind, steps, 6, eunk, einr, igdeb, inner_state
        ),
        *warnings,
        echo(f"RADIAL-FLOOR-ARM-COMPLETE {arm_id}", 40),
        "cle2000_c: cpu time= 1.000 second",
        NORMAL_END,
    ]
    return "\n".join(rows) + "\n"


def probe_log(arm_id: str) -> str:
    rows = [
        echo(f"RADIAL-FLOOR-PROBE-BEGIN {arm_id}", 20),
        echo("RADIAL-FLOOR-PROBE-HISTORY RESET", 21),
        echo(
            "RADIAL-FLOOR-PROBE-CONTROLS 1 740 2.500000E-07 1 0",
            22,
        ),
        *header(1, 1, 0),
        *history(
            1,
            1,
            0,
            "1.00000000E-07",
            "1.10000000E-07",
            371,
        ),
        *terminal_pair(
            "DIAG",
            1,
            1,
            "1.00000000E-07",
            "1.10000000E-07",
            371,
            1,
        ),
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        echo(f"RADIAL-FLOOR-PROBE-COMPLETE {arm_id}", 40),
        "cle2000_c: cpu time= 1.000 second",
        NORMAL_END,
    ]
    return "\n".join(rows) + "\n"


class RadialFloorStatusTests(unittest.TestCase):
    maxDiff = None

    def run_checker(
        self,
        native_arm: str,
        stationary_arm: str,
        native_probe: str | None = None,
        stationary_probe: str | None = None,
        protocol: Path = PROTOCOL,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                root / "native_arm.log",
                root / "stationary_arm.log",
                root / "native_probe.log",
                root / "stationary_probe.log",
            ]
            contents = [
                native_arm,
                stationary_arm,
                native_probe
                if native_probe is not None
                else probe_log("NATIVE"),
                stationary_probe
                if stationary_probe is not None
                else probe_log("STATIONARY"),
            ]
            for path, content in zip(paths, contents, strict=True):
                path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(CHECKER),
                    *(str(path) for path in paths),
                    str(protocol),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_strict_and_cap_comparison_states(self) -> None:
        fixtures = [
            ("STRICT", 4, "STRICT", 3, "BOTH-STRICT"),
            (
                "STRICT",
                4,
                "CAP",
                4,
                "NATIVE-ONLY-STRICT",
            ),
            (
                "CAP",
                4,
                "STRICT",
                3,
                "STATIONARY-ONLY-STRICT",
            ),
            ("CAP", 4, "CAP", 4, "BOTH-CAP"),
        ]
        for native_state, native_step, stationary_state, stationary_step, \
                expected in fixtures:
            with self.subTest(expected=expected):
                result = self.run_checker(
                    main_arm_log(
                        "NATIVE", native_state, strict_step=native_step
                    ),
                    main_arm_log(
                        "STATIONARY",
                        stationary_state,
                        strict_step=stationary_step,
                    ),
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(
                    f"RADIAL-FLOOR STATUS COMPARISON {expected}",
                    result.stdout,
                )
                self.assertIn("STATUS STAGE4 INVALID", result.stdout)
                self.assertIn(
                    "STATUS STAGE5 NOT-AUTHORIZED", result.stdout
                )

    def test_strict_before_outer_acceleration_is_inconclusive(self) -> None:
        result = self.run_checker(
            main_arm_log("NATIVE", "STRICT", strict_step=3),
            main_arm_log("STATIONARY", "CAP"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "STATUS COMPARISON INCONCLUSIVE-NO-OUTER-ACCELERATION",
            result.stdout,
        )

    def test_probe_is_a_predeclared_one_step_diagnostic(self) -> None:
        result = self.run_checker(
            main_arm_log("NATIVE", "CAP"),
            main_arm_log("STATIONARY", "CAP"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "STATUS PROBE NATIVE ONE-STEP-DIAGNOSTIC IEXTF=1",
            result.stdout,
        )
        self.assertIn(
            "FIXED-POINT-DEFECT NOT-A-PHI-MINUS-Q-RESIDUAL",
            result.stdout,
        )
        self.assertIn("STATUS THRESHOLD NONE", result.stdout)

    def test_cap_and_probe_contract_tamper_fails_closed(self) -> None:
        native = main_arm_log("NATIVE", "CAP")
        stationary = main_arm_log("STATIONARY", "CAP")
        native_probe = probe_log("NATIVE")
        tampered = {
            "cap missing warning": (
                native.replace(
                    " *** FLU2DR: CONVERGENCE NOT REACHED ***\n",
                    "",
                    1,
                ),
                stationary,
                native_probe,
            ),
            "cap false pass residual": (
                native.replace(
                    "EUNK=  3.00000000E-07",
                    "EUNK=  2.00000000E-07",
                    1,
                ).replace(
                    "EINR=  3.20000000E-07",
                    "EINR=  2.00000000E-07",
                    1,
                ).replace(
                    "IGDEB=    50 STATE=2",
                    "IGDEB=   371 STATE=1",
                    1,
                ),
                stationary,
                native_probe,
            ),
            "probe maxout marker": (
                native,
                stationary,
                native_probe.replace(
                    "RADIAL-FLOOR-PROBE-CONTROLS 1 740",
                    "RADIAL-FLOOR-PROBE-CONTROLS 2 740",
                    1,
                ),
            ),
            "probe false term": (
                native,
                stationary,
                native_probe.replace(
                    "FLU2DR-DIAG OUTER",
                    "FLU2DR-TERM OUTER-GATE=PASS",
                    1,
                ),
            ),
        }
        for name, (arm_a, arm_b, probe_a) in tampered.items():
            with self.subTest(name=name):
                result = self.run_checker(
                    arm_a, arm_b, native_probe=probe_a
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(
                    result.stderr.startswith(
                        "RADIAL-FLOOR STATUS FAIL:"
                    ),
                    result.stderr,
                )
                self.assertEqual(result.stdout, "")

    def test_iteration_and_envelope_tamper_fails_closed(self) -> None:
        native = main_arm_log("NATIVE", "CAP")
        stationary = main_arm_log("STATIONARY", "CAP")
        tampered = {
            "missing history reset": native.replace(
                echo("RADIAL-FLOOR-ARM-HISTORY RESET", 21) + "\n",
                "",
            ),
            "wrong production door": native.replace(
                "** MCCG **", "** SPOT **", 1
            ),
            "missing outer record": native.replace(
                (
                    " OUT(  3) FLX: PRC= 8.00E-07 TAR= 2.50E-07 "
                    "FNOR= 1.000000E+00 ACCE=     1.00000\n"
                ),
                "",
            ),
            "nonunit free ZMU": native.replace(
                "ACCE=     1.00000",
                "ACCE=     0.90000",
                1,
            ),
            "stationary ZMU": stationary.replace(
                "ACCE=     1.00000",
                "ACCE=     0.90000",
                1,
            ),
            "scientific claim": native.replace(
                NORMAL_END,
                "STAGE5 AUTHORIZED\n" + NORMAL_END,
            ),
            "duplicate footer": native + NORMAL_END + "\n",
            "forged footer suffix": native.replace(
                NORMAL_END,
                NORMAL_END + " FORGED",
            ),
        }
        for name, arm_a in tampered.items():
            with self.subTest(name=name):
                result = self.run_checker(arm_a, stationary)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(
                    result.stderr.startswith(
                        "RADIAL-FLOOR STATUS FAIL:"
                    ),
                    result.stderr,
                )

    def test_native_inner_cycle_history_and_tamper(self) -> None:
        native = main_arm_log("NATIVE", "CAP")
        first_inner = (
            "          IN(  1) FLX: PRC= 7.00E-07 "
            "TAR= 2.50E-07 IGDEB=           20 "
            "ACCE=     1.00000"
        )
        expanded_rows = []
        for iteration in range(1, 8):
            zmu = (
                1.0
                if (iteration - 1) % 6 < 3
                else 0.75
            )
            expanded_rows.append(
                f"          IN({iteration:3d}) FLX: PRC= 7.00E-07 "
                "TAR= 2.50E-07 IGDEB=           20 "
                f"ACCE={zmu:12.5f}"
            )
        expanded = native.replace(
            first_inner, "\n".join(expanded_rows), 1
        )
        result = self.run_checker(
            expanded,
            main_arm_log("STATIONARY", "CAP"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        tampered = expanded.replace(
            (
                "          IN(  7) FLX: PRC= 7.00E-07 "
                "TAR= 2.50E-07 IGDEB=           20 "
                "ACCE=     1.00000"
            ),
            (
                "          IN(  7) FLX: PRC= 7.00E-07 "
                "TAR= 2.50E-07 IGDEB=           20 "
                "ACCE=     0.90000"
            ),
            1,
        )
        result = self.run_checker(
            tampered,
            main_arm_log("STATIONARY", "CAP"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "non-unit ACCE during a free or stationary iteration",
            result.stderr,
        )

    def test_protocol_tamper_fails_closed(self) -> None:
        protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        protocol["threshold"] = 1.0e-6
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json",
        ) as stream:
            json.dump(protocol, stream)
            stream.flush()
            result = self.run_checker(
                main_arm_log("NATIVE", "CAP"),
                main_arm_log("STATIONARY", "CAP"),
                protocol=Path(stream.name),
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "protocol differs from the frozen radial-floor contract",
            result.stderr,
        )
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()

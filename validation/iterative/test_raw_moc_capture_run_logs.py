#!/usr/bin/env python3
"""Synthetic tests for the four-log raw-MOC production-run checker."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_raw_moc_capture_run_logs.py"
PASS_LINE = "RAW-MOC-CAPTURE RUN-LOGS PASS"
NORMAL_END = " normal end of execution for dragon 5  Version 5.1.0"


def listing_line(payload: str, number: int) -> str:
    return f"{payload:<120}{number:04d}"


def trace_line(payload: str, number: int) -> str:
    return f"<|{payload:<116}|<{number:04d}"


def scientific_block(
    arm: str,
    internal_cpu: str,
    external_cpu: str,
) -> list[str]:
    if arm == "NATIVE":
        change = "1.20336585E-06"
        printed = "1.20E-06"
        first = "3.17E-07"
        igdeb = 68
    elif arm == "STATIONARY":
        change = "8.03127307E-07"
        printed = "8.03E-07"
        first = "2.60E-07"
        igdeb = 59
    else:
        raise ValueError(arm)
    return [
        " P. I. M.    SOLUTION TO TRANSPORT EQUATION",
        "",
        " CALCULATION TYPE            =    SOURCE",
        " FORWARD/BACKWARD OPTION     =    DIRECT",
        " (AN)ISOTROPY OPTION         = ISOTROPIC",
        " FLUX SOLUTION DOOR          = ** MCCG   **",
        " NB. OF GROUPS               =       370",
        " NB. OF REGIONS              =         8",
        " NB. OF UNKNOWNS PER GROUP   =        14",
        " NB. OF LEAKAGE ZONES        =         1",
        " MAX. OUTER ITERATIONS       =         1",
        " MAX. THERMAL ITERATIONS     =       740",
        " ACCELERATION SCHEME         =( 1 FREE, 0 ACCELERATED)",
        " REBALANCING OPTION          = ON ",
        " SELF-SCATTERING REDUCTION   = ON ",
        " FUNDAMENTAL MODE            = ON ",
        " EIGENVALUE TOLERANCE        =  2.500E-07",
        " UNKNOWN OUTER TOLERANCE     =  2.500E-07",
        " UNKNOWN INNER TOLERANCE     =  2.500E-07",
        "",
        " USE TRANSPORT CORRECTED CROSS-SECTIONS",
        (
            " OUT(  0) EIG: PRC= 1.00E+00 TAR= 2.50E-07 "
            "KEFF= 1.000000E+00 BUCK= 0.00000E+00"
        ),
        (
            "          M O C PARAMETERS:  NON CYCLIC - STIS 1 "
            "- SC SCHEME - TABULATED EXP"
        ),
        (
            f"          IN(  1) FLX: PRC= {printed} "
            f"TAR= 2.50E-07 IGDEB={igdeb:13d} ACCE=     1.00000"
        ),
        f"                  FIRST UNCONVERGED GROUP PRC= {first}",
        " FLU2DR: NO LEAKAGE-> REBALANCING ON",
        (
            f" FLU2DR: CPU TIME={internal_cpu:>9}. "
            "INTERNAL CONVERGENCE *NEARLY* REACHED AFTER"
            "     1 ITERATIONS."
        ),
        (
            " OUT(  1) EIG: PRC= 0.00E+00 TAR= 2.50E-07 "
            "KEFF= 1.000000E+00 BUCK= 0.00000E+00"
        ),
        (
            f" OUT(  1) FLX: PRC= {printed} TAR= 2.50E-07 "
            "FNOR= 1.000000E+00 ACCE=     1.00000"
        ),
        (
            " FLU2DR-DIAG OUTER IEXTF=     1 MAXOUT=     1 "
            "KEFF=  1.0000000000000000E+00 "
            "EEXT=  0.00000000E+00 EPSOUT=  2.49999999E-07 "
            f"EUNK=  {change} EPSUNK=  2.49999999E-07 "
            "EUNK-VALID=1"
        ),
        (
            " FLU2DR-DIAG INNER ITERF=     1 MAXINR=   740 "
            f"EINR=  {change} EPSINR=  2.49999999E-07 "
            f"IGDEB={igdeb:6d} STATE=2 NGRP=   370"
        ),
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        (
            f" FLU2DR: CPU TIME={external_cpu:>9}. "
            "EXTERNAL CONVERGENCE    *NOT* REACHED AFTER"
            "     1 ITERATIONS."
        ),
        "",
        " ++ TRACKING CALLED=   1 TIMES PRECISION= 0.00E+00",
        " ++ TOTAL NUMBER OF FLUX CALCULATIONS=       370",
    ]


def probe_log(
    arm: str,
    mode: str,
    internal_cpu: str = "0",
    external_cpu: str = "0",
) -> str:
    arm_code = 1 if arm == "NATIVE" else 2
    audit_control = f"MOCA {arm_code}" if mode == "ON" else ""
    source_rows = [
        "* CLE-2000 VERS 3.0 * TEST SOURCE * LINE",
        listing_line(
            "FLUX := FLU: FLUX MACRO0 TRACK TRACK_f SYSTEM FSOURCE ::",
            24,
        ),
        listing_line("EDIT 1 TYPE S INIT ON REBA", 25),
        listing_line("EXTE <<outer_cap>> <<solver_eps>>", 26),
        listing_line("UNKT <<solver_eps>>", 27),
        listing_line("THER <<inner_cap>> <<solver_eps>>", 28),
    ]
    source_control = (
        "ACCE <<free_steps>> <<acc_steps>>"
        + (f" {audit_control}" if audit_control else "")
        + " ;"
    )
    source_rows.append(
        listing_line(source_control, 30)
    )
    trace_rows = [
        trace_line(
            "FLUX := FLU: FLUX MACRO0 TRACK TRACK_f SYSTEM FSOURCE ::",
            24,
        ),
        trace_line("EDIT 1 TYPE S INIT ON REBA", 25),
        trace_line("EXTE <<outer_cap>> <<solver_eps>>", 26),
        trace_line("UNKT <<solver_eps>>", 27),
        trace_line("THER <<inner_cap>> <<solver_eps>>", 28),
    ]
    trace_control = (
        "ACCE <<free_steps>> <<acc_steps>>"
        + (f" {audit_control}" if audit_control else "")
        + " ;"
    )
    trace_rows.append(
        trace_line(trace_control, 30)
    )
    rows = [
        *source_rows,
        "",
        *trace_rows,
        "->@BEGIN MODULE : FLU:",
        *scientific_block(
            arm,
            internal_cpu=internal_cpu,
            external_cpu=external_cpu,
        ),
        "->@END MODULE   : FLU:",
        (
            "-->>MODULE FLU: : TIME SPENT= 0.000 "
            "MEMORY USAGE= 2.248E+07"
        ),
        "cle2000_c: cpu time= 0.00 second",
        "",
        NORMAL_END,
        " check for warning in listing",
        " before assuming your run was successful",
    ]
    return "\n".join(rows) + "\n"


def valid_logs() -> list[str]:
    return [
        probe_log("NATIVE", "OFF", "0", "0"),
        probe_log("NATIVE", "ON", "0.125", "0.250"),
        probe_log("STATIONARY", "OFF", "1.0", "2.0"),
        probe_log("STATIONARY", "ON", "9.5", "12.75"),
    ]


class RawMocRunLogTests(unittest.TestCase):
    maxDiff = None

    def run_checker(
        self,
        logs: list[str],
    ) -> subprocess.CompletedProcess[str]:
        self.assertEqual(len(logs), 4)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                root / "native_off.log",
                root / "native_on.log",
                root / "stationary_off.log",
                root / "stationary_on.log",
            ]
            for path, content in zip(paths, logs, strict=True):
                path.write_text(content, encoding="ascii", newline="\n")
            return subprocess.run(
                [
                    sys.executable,
                    str(CHECKER),
                    *(str(path) for path in paths),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

    def assert_fails(self, logs: list[str], expected: str) -> None:
        result = self.run_checker(logs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertTrue(
            result.stderr.startswith(
                "RAW-MOC-CAPTURE RUN-LOGS FAIL:"
            ),
            result.stderr,
        )
        self.assertIn(expected, result.stderr)

    def test_valid_logs_and_cpu_telemetry_narrowing(self) -> None:
        result = self.run_checker(valid_logs())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, PASS_LINE + "\n")
        self.assertEqual(result.stderr, "")

    def test_envelope_and_abnormal_tamper_fail_closed(self) -> None:
        cases = {
            "duplicate normal end": (
                0,
                lambda text: text + NORMAL_END + "\n",
                "normal Dragon termination",
            ),
            "missing normal end": (
                1,
                lambda text: text.replace(NORMAL_END + "\n", "", 1),
                "normal Dragon termination",
            ),
            "XABORT": (
                2,
                lambda text: text.replace(
                    NORMAL_END, "XABORT synthetic\n" + NORMAL_END, 1
                ),
                "abnormal XABORT",
            ),
            "nonfinite text": (
                3,
                lambda text: text.replace(
                    NORMAL_END, "NaN\n" + NORMAL_END, 1
                ),
                "non-finite text",
            ),
            "unresolved template token": (
                0,
                lambda text: text.replace(
                    "ACCE <<free_steps>>",
                    "@AUDIT_CONTROL@\nACCE <<free_steps>>",
                    1,
                ),
                "unresolved audit-control token",
            ),
        }
        for name, (index, mutate, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[index] = mutate(logs[index])
                self.assert_fails(logs, expected)

    def test_moca_listing_and_execution_trace_tamper(self) -> None:
        active_native = listing_line(
            "ACCE <<free_steps>> <<acc_steps>> MOCA 1 ;", 30
        ) + "\n"
        trace_native = trace_line(
            "ACCE <<free_steps>> <<acc_steps>> MOCA 1 ;", 30
        ) + "\n"
        cases = {
            "wrong native code": (
                1,
                lambda text: text.replace("MOCA 1", "MOCA 2"),
                "MOCA 1 line",
            ),
            "missing source line": (
                1,
                lambda text: text.replace(active_native, "", 1),
                "source listing",
            ),
            "missing trace line": (
                1,
                lambda text: text.replace(trace_native, "", 1),
                "execution trace",
            ),
            "duplicate trace line": (
                1,
                lambda text: text.replace(
                    trace_native, trace_native + trace_native, 1
                ),
                "execution trace",
            ),
            "MOCA in OFF source": (
                0,
                lambda text: text.replace(
                    listing_line(
                        "ACCE <<free_steps>> <<acc_steps>> ;", 30
                    ),
                    listing_line("MOCA 1", 29)
                    + "\n"
                    + listing_line(
                        "ACCE <<free_steps>> <<acc_steps>> ;", 30
                    ),
                    1,
                ),
                "OFF log contains an active MOCA control",
            ),
            "MOCA in OFF trace": (
                2,
                lambda text: text.replace(
                    trace_line(
                        "ACCE <<free_steps>> <<acc_steps>> ;", 30
                    ),
                    trace_line("MOCA 2", 29)
                    + "\n"
                    + trace_line(
                        "ACCE <<free_steps>> <<acc_steps>> ;", 30
                    ),
                    1,
                ),
                "OFF log contains an active MOCA control",
            ),
        }
        for name, (index, mutate, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[index] = mutate(logs[index])
                self.assert_fails(logs, expected)

    def test_locked_controls_and_counts_tamper(self) -> None:
        cases = {
            "wrong groups": (
                0,
                "NB. OF GROUPS               =       370",
                "NB. OF GROUPS               =       369",
                "group count",
            ),
            "wrong regions": (
                1,
                "NB. OF REGIONS              =         8",
                "NB. OF REGIONS              =         9",
                "region count",
            ),
            "wrong unknowns": (
                2,
                "NB. OF UNKNOWNS PER GROUP   =        14",
                "NB. OF UNKNOWNS PER GROUP   =        13",
                "unknown count",
            ),
            "wrong MAXOUT": (
                3,
                "MAX. OUTER ITERATIONS       =         1",
                "MAX. OUTER ITERATIONS       =         2",
                "outer cap",
            ),
            "wrong ACCE": (
                0,
                "ACCELERATION SCHEME         =( 1 FREE, 0 ACCELERATED)",
                "ACCELERATION SCHEME         =( 1 FREE, 1 ACCELERATED)",
                "stationary acceleration",
            ),
            "tracking calls": (
                1,
                "++ TRACKING CALLED=   1",
                "++ TRACKING CALLED=   2",
                "tracking-call count",
            ),
            "flux calculations": (
                2,
                "++ TOTAL NUMBER OF FLUX CALCULATIONS=       370",
                "++ TOTAL NUMBER OF FLUX CALCULATIONS=       369",
                "flux-calculation count",
            ),
        }
        for name, (index, old, new, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[index] = logs[index].replace(old, new, 1)
                self.assert_fails(logs, expected)

    def test_one_step_and_warning_tamper(self) -> None:
        cases = {
            "second inner step": (
                0,
                lambda text: text.replace(
                    "          IN(  1) FLX:",
                    "          IN(  2) FLX:",
                    1,
                ),
                "one printed FLU update",
            ),
            "second outer step": (
                1,
                lambda text: text.replace(
                    " OUT(  1) FLX:", " OUT(  2) FLX:", 1
                ),
                "one printed FLU update",
            ),
            "missing warning": (
                2,
                lambda text: text.replace(
                    " *** FLU2DR: CONVERGENCE NOT REACHED ***\n",
                    "",
                    1,
                ),
                "three one-step warnings",
            ),
            "strict-terminal claim": (
                3,
                lambda text: text.replace(
                    "FLU2DR-DIAG OUTER", "FLU2DR-TERM OUTER", 1
                ),
                "one-step outer diagnostic",
            ),
        }
        for name, (index, mutate, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[index] = mutate(logs[index])
                self.assert_fails(logs, expected)

    def test_nontelemetry_scientific_difference_fails(self) -> None:
        logs = valid_logs()
        logs[1] = logs[1].replace(
            "EUNK=  1.20336585E-06",
            "EUNK=  1.20336586E-06",
            1,
        )
        self.assert_fails(
            logs, "NATIVE OFF/ON scientific FLU blocks differ"
        )

        logs = valid_logs()
        logs[3] = logs[3].replace(
            "FIRST UNCONVERGED GROUP PRC= 2.60E-07",
            "FIRST UNCONVERGED GROUP PRC= 2.61E-07",
            1,
        )
        self.assert_fails(
            logs, "STATIONARY OFF/ON scientific FLU blocks differ"
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Synthetic tests for strict five-log GMRES-activity closure."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from typing import Sequence, Union


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_gmres_activity_run_logs.py"
TEMPLATE = HERE / "gmres_activity_probe.x2m.in"
RAW_TEMPLATE = HERE / "raw_moc_capture_probe.x2m.in"
ARTIFACTS = HERE.parent / "artifacts" / "raw-moc-capture"
PASS_LINE = "GMRES-ACTIVITY RUN-LOGS PASS"
NORMAL_END = " normal end of execution for dragon 5  Version 5.1.0"


def source_line(payload: str, number: int) -> str:
    return f"{payload:<123}{number:04d}"


def trace_line(payload: str, number: int) -> str:
    return f"<|{payload:<120}|<{number:04d}"


def probe_log(
    mode: str,
    *,
    gmra: bool,
    internal_cpu: str = "0",
    external_cpu: str = "0",
) -> str:
    if mode not in {"OFF", "ON"}:
        raise ValueError(mode)
    if mode == "OFF":
        control = "ACCE <<free_steps>> <<acc_steps>>  ;"
    elif gmra:
        control = "ACCE <<free_steps>> <<acc_steps>> MOCA 2 GMRA ;"
    else:
        control = "ACCE <<free_steps>> <<acc_steps>> MOCA 2 ;"
    rows = [
        'ECHO "RAW-MOC-CAPTURE-BEGIN" "STATIONARY" '
        f'"{mode}" ; 0019',
        source_line(control, 28),
        'ECHO "RAW-MOC-CAPTURE-COMPLETE" "STATIONARY" '
        f'"{mode}" ; 0029',
        f">|RAW-MOC-CAPTURE-BEGIN STATIONARY {mode}|>0019",
        trace_line(control, 28),
        "->@BEGIN MODULE : FLU:",
        " P. I. M.    SOLUTION TO TRANSPORT EQUATION",
        (
            "          M O C PARAMETERS:  NON CYCLIC - STIS 1 "
            "- SC SCHEME - TABULATED EXP"
        ),
        (
            "          IN(  1) FLX: PRC= 8.03E-07 "
            "TAR= 2.50E-07 IGDEB=           59 ACCE=     1.00000"
        ),
        (
            f" FLU2DR: CPU TIME={internal_cpu:>9}. "
            "INTERNAL CONVERGENCE *NEARLY* REACHED AFTER"
            "     1 ITERATIONS."
        ),
        (
            " OUT(  1) FLX: PRC= 8.03E-07 TAR= 2.50E-07 "
            "FNOR= 1.000000E+00 ACCE=     1.00000"
        ),
        (
            " FLU2DR-DIAG OUTER IEXTF=     1 MAXOUT=     1 "
            "KEFF=  1.0000000000000000E+00 "
            "EEXT=  0.00000000E+00 EPSOUT=  2.49999999E-07 "
            "EUNK=  8.03127307E-07 EPSUNK=  2.49999999E-07 "
            "EUNK-VALID=1"
        ),
        (
            " FLU2DR-DIAG INNER ITERF=     1 MAXINR=   740 "
            "EINR=  8.03127307E-07 EPSINR=  2.49999999E-07 "
            "IGDEB=    59 STATE=2 NGRP=   370"
        ),
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        " *** FLU2DR: CONVERGENCE NOT REACHED ***",
        (
            f" FLU2DR: CPU TIME={external_cpu:>9}. "
            "EXTERNAL CONVERGENCE    *NOT* REACHED AFTER"
            "     1 ITERATIONS."
        ),
        " ++ TRACKING CALLED=   1 TIMES PRECISION= 0.00E+00",
        " ++ TOTAL NUMBER OF FLUX CALCULATIONS=       370",
        "->@END MODULE   : FLU:",
        f">|RAW-MOC-CAPTURE-COMPLETE STATIONARY {mode}|>0029",
        "cle2000_c: cpu time= 0.00 second",
        "",
        NORMAL_END,
        " check for warning in listing",
        " before assuming your run was successful",
    ]
    return "\n".join(rows) + "\n"


def valid_logs() -> list[str]:
    return [
        probe_log("OFF", gmra=False, internal_cpu="0", external_cpu="0"),
        probe_log("ON", gmra=False, internal_cpu="0", external_cpu="0"),
        probe_log("OFF", gmra=False, internal_cpu="1.25", external_cpu="2.5"),
        probe_log("ON", gmra=True, internal_cpu="3.75", external_cpu="4.0"),
        probe_log("ON", gmra=True, internal_cpu="8.5", external_cpu="9.25"),
    ]


def swap_cpu_lines(text: str) -> str:
    lines = text.splitlines(keepends=True)
    internal = next(
        index
        for index, line in enumerate(lines)
        if "INTERNAL CONVERGENCE" in line
    )
    external = next(
        index
        for index, line in enumerate(lines)
        if "EXTERNAL CONVERGENCE" in line
    )
    lines[internal], lines[external] = lines[external], lines[internal]
    return "".join(lines)


class GmresActivityRunLogTests(unittest.TestCase):
    maxDiff = None

    def write_logs(
        self,
        root: Path,
        logs: Sequence[Union[str, bytes]],
    ) -> list[Path]:
        names = (
            "legacy_off.log",
            "legacy_on.log",
            "actual_off.log",
            "actual_on_a.log",
            "actual_on_b.log",
        )
        paths = [root / name for name in names]
        for path, content in zip(paths, logs):
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_bytes(content.encode("ascii"))
        return paths

    def invoke(self, paths: list[Path]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), *(str(path) for path in paths)],
            check=False,
            capture_output=True,
            text=True,
        )

    def run_logs(
        self,
        logs: Sequence[Union[str, bytes]],
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw:
            paths = self.write_logs(Path(raw), logs)
            return self.invoke(paths)

    def assert_fails(
        self,
        logs: Sequence[Union[str, bytes]],
        expected: str,
    ) -> None:
        result = self.run_logs(logs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertTrue(
            result.stderr.startswith("GMRES-ACTIVITY RUN-LOGS FAIL:"),
            result.stderr,
        )
        self.assertIn(expected, result.stderr)

    def test_valid_full_log_closure_and_fixed_width_normalization(self) -> None:
        result = self.run_logs(valid_logs())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, PASS_LINE + "\n")
        self.assertEqual(result.stderr, "")
        on = valid_logs()[3].splitlines()
        source = next(line for line in on if line.startswith("ACCE "))
        trace = next(line for line in on if line.startswith("<|ACCE "))
        self.assertEqual(len(source), 127)
        self.assertEqual(len(trace), 128)

    def test_probe_template_is_exact_raw_template_reuse(self) -> None:
        self.assertEqual(TEMPLATE.read_bytes(), RAW_TEMPLATE.read_bytes())
        template = TEMPLATE.read_text(encoding="ascii")
        self.assertEqual(template.count("@ARM@"), 2)
        self.assertEqual(template.count("@MODE@"), 2)
        self.assertEqual(template.count("@AUDIT_CONTROL@"), 1)

        off = (
            template.replace("@ARM@", "STATIONARY")
            .replace("@MODE@", "OFF")
            .replace("@AUDIT_CONTROL@", "")
        )
        legacy_off = (
            ARTIFACTS / "stationary_off" / "probe.x2m"
        ).read_text(encoding="ascii")
        self.assertEqual(off, legacy_off)

        on = (
            template.replace("@ARM@", "STATIONARY")
            .replace("@MODE@", "ON")
            .replace("@AUDIT_CONTROL@", "MOCA 2 GMRA")
        )
        legacy_on = (
            ARTIFACTS / "stationary_on" / "probe.x2m"
        ).read_text(encoding="ascii")
        self.assertEqual(on.count(" GMRA"), 1)
        self.assertEqual(on.replace(" GMRA", "", 1), legacy_on)

    def test_gmra_control_tampering_fails_closed(self) -> None:
        cases = {
            "missing GMRA": (
                lambda text: text.replace(" GMRA", "", 1),
                "control census",
            ),
            "third GMRA": (
                lambda text: text.replace(
                    NORMAL_END,
                    "GMRA\n" + NORMAL_END,
                    1,
                ),
                "control census",
            ),
            "wrong MOCA code": (
                lambda text: text.replace("MOCA 2", "MOCA 1"),
                "source line 0028",
            ),
            "wrong GMRA case": (
                lambda text: text.replace("GMRA", "gmra"),
                "control census",
            ),
            "wrong token order": (
                lambda text: text.replace("MOCA 2 GMRA", "GMRA MOCA 2"),
                "source line 0028",
            ),
            "GMRA numeric argument": (
                lambda text: text.replace(
                    "MOCA 2 GMRA ;",
                    "MOCA 2 GMRA 1 ;",
                ),
                "source line 0028",
            ),
            "wrong source number": (
                lambda text: text.replace("0028", "0027", 1),
                "source line 0028",
            ),
            "wrong trace number": (
                lambda text: text.replace("|<0028", "|<0027", 1),
                "execution echo line 0028",
            ),
        }
        for name, (mutation, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[3] = mutation(logs[3])
                self.assert_fails(logs, expected)

    def test_source_and_trace_width_tampering_fails_closed(self) -> None:
        cases = {
            "source minus one": (
                "MOCA 2 GMRA ; ",
                "MOCA 2 GMRA ;",
                "fixed-width line length",
            ),
            "source plus one": (
                "MOCA 2 GMRA ; ",
                "MOCA 2 GMRA ;  ",
                "fixed-width line length",
            ),
            "trace minus one": (
                " ;" + " " * 73 + "|<0028",
                " ;" + " " * 72 + "|<0028",
                "fixed-width line length",
            ),
            "trace plus one": (
                " ;" + " " * 73 + "|<0028",
                " ;" + " " * 74 + "|<0028",
                "fixed-width line length",
            ),
        }
        for name, (old, new, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                if name.startswith("source"):
                    line = next(
                        item
                        for item in logs[3].splitlines()
                        if item.startswith("ACCE ")
                    )
                    changed = (
                        line[:-5].replace(old, new, 1) + line[-5:]
                    )
                else:
                    line = next(
                        item
                        for item in logs[3].splitlines()
                        if item.startswith("<|ACCE ")
                    )
                    changed = line.replace(old, new, 1)
                logs[3] = logs[3].replace(line, changed, 1)
                self.assert_fails(logs, expected)

    def test_off_and_legacy_control_tampering_fails_closed(self) -> None:
        cases = {
            "actual OFF MOCA": (
                2,
                lambda text: text.replace(
                    "ACCE <<free_steps>> <<acc_steps>>  ;",
                    "ACCE <<free_steps>> <<acc_steps>> MOCA 2 ;",
                    1,
                ),
                "OFF log contains",
            ),
            "legacy ON GMRA": (
                1,
                lambda text: text.replace("MOCA 2 ;", "MOCA 2 GMRA ;"),
                "legacy ON control census",
            ),
            "ON-A marker": (
                3,
                lambda text: text.replace("STATIONARY ON", "STATIONARY ON-A"),
                "execution BEGIN marker",
            ),
        }
        for name, (index, mutation, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[index] = mutation(logs[index])
                self.assert_fails(logs, expected)

    def test_cpu_telemetry_tampering_fails_closed(self) -> None:
        cases = {
            "missing": (
                lambda text: text.replace(
                    next(
                        line
                        for line in text.splitlines()
                        if "INTERNAL CONVERGENCE" in line
                    )
                    + "\n",
                    "",
                    1,
                ),
                "internal CPU telemetry",
            ),
            "malformed": (
                lambda text: text.replace(
                    "CPU TIME=     3.75.",
                    "CPU TIME=        x.",
                    1,
                ),
                "internal CPU telemetry",
            ),
            "duplicate internal role": (
                lambda text: text.replace(
                    "EXTERNAL CONVERGENCE    *NOT*",
                    "INTERNAL CONVERGENCE *NEARLY*",
                ),
                "internal CPU telemetry",
            ),
            "reordered": (
                swap_cpu_lines,
                "CPU telemetry",
            ),
        }
        for name, (mutation, expected) in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[3] = mutation(logs[3])
                self.assert_fails(logs, expected)

    def test_nontelemetry_full_log_difference_is_rejected(self) -> None:
        cases = {
            "one numeric digit": lambda text: text.replace(
                "EUNK=  8.03127307E-07",
                "EUNK=  8.03127308E-07",
                1,
            ),
            "debug line": lambda text: text.replace(
                NORMAL_END,
                "debug\n" + NORMAL_END,
                1,
            ),
            "blank line": lambda text: text.replace(
                "->@END MODULE   : FLU:\n",
                "->@END MODULE   : FLU:\n\n",
                1,
            ),
            "trailing space": lambda text: text.replace(
                "->@END MODULE   : FLU:",
                "->@END MODULE   : FLU: ",
                1,
            ),
        }
        for name, mutation in cases.items():
            with self.subTest(name=name):
                logs = valid_logs()
                logs[3] = mutation(logs[3])
                self.assert_fails(logs, "normalized full log differs")

    def test_two_sided_on_tamper_still_fails_legacy_identity(self) -> None:
        logs = valid_logs()
        for index in (3, 4):
            logs[index] = logs[index].replace(
                "EUNK=  8.03127307E-07",
                "EUNK=  8.03127308E-07",
                1,
            )
        self.assert_fails(logs, "differs from LEGACY_ON")

    def test_required_runtime_records_fail_closed(self) -> None:
        needles = {
            "normal termination": NORMAL_END,
            "PIM": " P. I. M.    SOLUTION TO TRANSPORT EQUATION",
            "MCCG": "          M O C PARAMETERS:",
            "inner": "          IN(  1) FLX:",
            "outer": " OUT(  1) FLX:",
            "outer diagnostic": " FLU2DR-DIAG OUTER",
            "inner diagnostic": " FLU2DR-DIAG INNER",
            "tracking": " ++ TRACKING CALLED=",
            "flux count": " ++ TOTAL NUMBER OF FLUX CALCULATIONS=",
        }
        for name, needle in needles.items():
            with self.subTest(name=name):
                logs = valid_logs()
                line = next(
                    item
                    for item in logs[3].splitlines()
                    if item.startswith(needle)
                )
                logs[3] = logs[3].replace(line + "\n", "", 1)
                self.assert_fails(logs, "expected one record")

    def test_warning_and_strict_terminal_fail_closed(self) -> None:
        logs = valid_logs()
        logs[3] = logs[3].replace(
            " *** FLU2DR: CONVERGENCE NOT REACHED ***\n",
            "",
            1,
        )
        self.assert_fails(logs, "three one-step warnings")
        logs = valid_logs()
        logs[3] = logs[3].replace(
            NORMAL_END,
            " FLU2DR-TERM STRICT\n" + NORMAL_END,
            1,
        )
        self.assert_fails(logs, "strict-terminal claim")

    def test_abnormal_text_fails_closed(self) -> None:
        for token in (
            "XABORT",
            "segmentation fault",
            "floating invalid",
            "bus error",
            "illegal instruction",
            "NaN",
            "Infinity",
        ):
            with self.subTest(token=token):
                logs = valid_logs()
                logs[3] = logs[3].replace(
                    NORMAL_END,
                    token + "\n" + NORMAL_END,
                    1,
                )
                self.assert_fails(logs, "abnormal")

    def test_canonical_text_failures(self) -> None:
        cases = {
            "CR": (
                lambda raw: raw.replace(b"\n", b"\r\n", 1),
                "canonical LF",
            ),
            "NUL": (
                lambda raw: raw.replace(b"\n", b"\0\n", 1),
                "NUL byte",
            ),
            "non-ASCII": (
                lambda raw: raw.replace(b"\n", b"\xff\n", 1),
                "not ASCII",
            ),
            "no final LF": (
                lambda raw: raw[:-1],
                "final newline",
            ),
        }
        for name, (mutation, expected) in cases.items():
            with self.subTest(name=name):
                logs = [item.encode("ascii") for item in valid_logs()]
                logs[3] = mutation(logs[3])
                self.assert_fails(logs, expected)

    def test_symlink_hardlink_and_duplicate_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            paths = self.write_logs(root, valid_logs())
            link = root / "on_b_link.log"
            link.symlink_to(paths[4])
            linked_paths = [*paths[:4], link]
            result = self.invoke(linked_paths)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-symlink", result.stderr)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            paths = self.write_logs(root, valid_logs())
            hardlink = root / "on_b_hardlink.log"
            os.link(paths[4], hardlink)
            hardlinked_paths = [*paths[:3], paths[4], hardlink]
            result = self.invoke(hardlinked_paths)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("distinct inodes", result.stderr)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            paths = self.write_logs(root, valid_logs())
            duplicate_paths = [*paths[:4], paths[3]]
            result = self.invoke(duplicate_paths)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("resolve distinctly", result.stderr)

    def test_cli_argument_census_is_fixed(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("expected exactly LEGACY_OFF", result.stderr)


if __name__ == "__main__":
    unittest.main()

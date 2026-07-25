#!/usr/bin/env python3
"""Apply the frozen, non-scientific GMRES-activity log normalizations."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


CPU_TIME_RE = re.compile(
    r"(FLU2DR: CPU TIME=)[ \t]*"
    r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
    r"(?=\.[ \t]+(?:INTERNAL|EXTERNAL))"
)
MODULE_RECEIPT_RE = re.compile(
    r"^(?P<prefix>-->>MODULE FLU:        : TIME SPENT=)"
    r"(?P<time>.{13})"
    r"(?P<middle> MEMORY USAGE=)"
    r"(?P<memory>.{10})$",
    re.MULTILINE,
)
MODULE_TIME_RE = re.compile(r" *(?:0|[1-9][0-9]*)\.[0-9]{3}")
MODULE_MEMORY_RE = re.compile(r" [0-9]\.[0-9]{3}E[+-][0-9]{2}")
MODULE_TIME_MARKER = "<MODULE-TIME>"
MODULE_MEMORY_MARKER = "<MEM-TELE>"
CLE_CPU_RE = re.compile(
    r"^(?P<prefix>cle2000_c: cpu time= )"
    r"(?P<value>(?:0|[1-9][0-9]*)\.[0-9]{2})"
    r"(?P<suffix> second)$",
    re.MULTILINE,
)
CLE_CPU_MARKER = "<CLE-CPU>"
SOURCE_GMRA_RE = re.compile(
    r"^ACCE[^\n]* MOCA 2 GMRA ;[ \t]+0028[ \t]*$",
    re.MULTILINE,
)
TRACE_GMRA_RE = re.compile(
    r"^<\|ACCE[^\n]* MOCA 2 GMRA ;[^\n]*\|<0028[ \t]*$",
    re.MULTILINE,
)
GMRA_REPLACEMENT_FROM = " MOCA 2 GMRA ;"
# CLE-2000 prints source and execution lines in a fixed 120-column field.
# Removing the five GMRA characters must therefore restore the five padding
# columns so that a normalized real run can equal the frozen legacy log.
GMRA_REPLACEMENT_TO = " MOCA 2 ;     "


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY-LOG FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def replace_exact_gmra_line(
    text: str,
    pattern: re.Pattern[str],
    description: str,
) -> str:
    matches = list(pattern.finditer(text))
    require(len(matches) == 1, f"{description} census differs")
    match = matches[0]
    line = match.group(0)
    require(
        line.count(GMRA_REPLACEMENT_FROM) == 1,
        f"{description} token grammar differs",
    )
    normalized = line.replace(
        GMRA_REPLACEMENT_FROM,
        GMRA_REPLACEMENT_TO,
        1,
    )
    return text[: match.start()] + normalized + text[match.end() :]


def replace_exact_module_receipt(text: str) -> str:
    require(
        MODULE_TIME_MARKER not in text and MODULE_MEMORY_MARKER not in text,
        "log contains a forged module telemetry marker",
    )
    require(
        len(re.findall(r"^-->>MODULE ", text, re.MULTILINE)) == 1,
        "module receipt census differs",
    )
    matches = list(MODULE_RECEIPT_RE.finditer(text))
    require(len(matches) == 1, "FLU module telemetry census differs")
    match = matches[0]
    time_field = match.group("time")
    memory_field = match.group("memory")
    require(
        MODULE_TIME_RE.fullmatch(time_field) is not None,
        "FLU module time telemetry grammar differs",
    )
    require(
        MODULE_MEMORY_RE.fullmatch(memory_field) is not None,
        "FLU module memory telemetry grammar differs",
    )
    replacement = (
        match.group("prefix")
        + MODULE_TIME_MARKER
        + match.group("middle")
        + MODULE_MEMORY_MARKER
    )
    require(
        len(replacement) == len(match.group(0)),
        "FLU module telemetry normalization changed line width",
    )
    normalized = text[: match.start()] + replacement + text[match.end() :]
    require(
        normalized.count(MODULE_TIME_MARKER) == 1
        and normalized.count(MODULE_MEMORY_MARKER) == 1,
        "normalized module telemetry marker census differs",
    )
    return normalized


def replace_exact_cle_cpu_receipt(text: str) -> str:
    require(CLE_CPU_MARKER not in text, "log contains a forged CLE CPU marker")
    matches = list(CLE_CPU_RE.finditer(text))
    require(len(matches) == 1, "CLE CPU telemetry census differs")
    match = matches[0]
    normalized = (
        text[: match.start()]
        + match.group("prefix")
        + CLE_CPU_MARKER
        + match.group("suffix")
        + text[match.end() :]
    )
    require(
        normalized.count(CLE_CPU_MARKER) == 1,
        "normalized CLE CPU marker census differs",
    )
    return normalized


def normalize(text: str, mode: str) -> str:
    require("\r" not in text, "carriage return is not canonical")
    require(text.endswith("\n"), "log lacks final newline")
    if mode == "legacy":
        require("GMRA" not in text, "legacy log contains GMRA")
    else:
        require(text.count("GMRA") == 2, "GMRA token census differs")
        text = replace_exact_gmra_line(
            text,
            SOURCE_GMRA_RE,
            "source line 0028",
        )
        text = replace_exact_gmra_line(
            text,
            TRACE_GMRA_RE,
            "execution echo line 0028",
        )
        require("GMRA" not in text, "GMRA remained after exact normalization")

    normalized, substitutions = CPU_TIME_RE.subn(
        r"\1<CPU-TELEMETRY>",
        text,
    )
    require(substitutions == 2, "CPU telemetry census differs")
    require(
        normalized.count("<CPU-TELEMETRY>") == 2,
        "normalized CPU marker census differs",
    )
    normalized = replace_exact_module_receipt(normalized)
    return replace_exact_cle_cpu_receipt(normalized)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("legacy", "gmra"), required=True)
    parser.add_argument("log", type=Path)
    arguments = parser.parse_args()

    path = arguments.log
    require(path.is_file() and not path.is_symlink(), "invalid input log")
    try:
        text = path.read_bytes().decode("ascii")
    except UnicodeDecodeError:
        fail("log is not ASCII")
    sys.stdout.write(normalize(text, arguments.mode))


if __name__ == "__main__":
    main()

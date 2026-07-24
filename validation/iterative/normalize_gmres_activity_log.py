#!/usr/bin/env python3
"""Apply the two frozen, non-scientific GMRA log normalizations."""

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
SOURCE_GMRA_RE = re.compile(
    r"^ACCE[^\n]* MOCA 2 GMRA ;[ \t]+0028[ \t]*$",
    re.MULTILINE,
)
TRACE_GMRA_RE = re.compile(
    r"^<\|ACCE[^\n]* MOCA 2 GMRA ;[^\n]*\|<0028[ \t]*$",
    re.MULTILINE,
)
GMRA_REPLACEMENT_FROM = " MOCA 2 GMRA ;"
GMRA_REPLACEMENT_TO = " MOCA 2 ;"


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
    return normalized


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

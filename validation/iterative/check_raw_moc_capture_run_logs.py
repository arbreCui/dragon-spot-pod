#!/usr/bin/env python3
"""Fail-closed comparison of the four raw-MOC production probe logs.

The checker validates the locked one-step FLU/MCCG branch and compares the
OFF and ON scientific FLU blocks for each terminal.  The only normalized
fields are the two printed FLU2DR CPU-time values; convergence text and every
other byte in the scientific block remain significant.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


PASS_LINE = "RAW-MOC-CAPTURE RUN-LOGS PASS"
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
NORMAL_END_RE = re.compile(
    r"^ normal end of execution for dragon 5  Version 5\.1\.0[ \t]*$",
    re.MULTILINE,
)
SCIENCE_START_RE = re.compile(
    r"^[ \t]*P\. I\. M\.[ \t]+SOLUTION TO TRANSPORT EQUATION[ \t]*$",
    re.MULTILINE,
)
SCIENCE_END_RE = re.compile(
    r"^[ \t]*\+\+ TOTAL NUMBER OF FLUX CALCULATIONS=[ \t]*370[ \t]*$",
    re.MULTILINE,
)
CPU_TIME_RE = re.compile(
    r"(FLU2DR: CPU TIME=)[ \t]*"
    r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[EeDd][+-]?\d+)?"
    r"(?=\.[ \t]+(?:INTERNAL|EXTERNAL))"
)
SOURCE_MOCA_RE = re.compile(r"\bMOCA +([12])(?=[ \t;])")
TRACE_MOCA_RE = re.compile(
    r"^<\|[^\n]*\bMOCA +([12])(?:[ \t;]|\|<)"
)


CONTROL_LINES = (
    (
        "calculation type",
        r"^[ \t]*CALCULATION TYPE[ \t]*=[ \t]*SOURCE[ \t]*$",
    ),
    (
        "direct option",
        r"^[ \t]*FORWARD/BACKWARD OPTION[ \t]*=[ \t]*DIRECT[ \t]*$",
    ),
    (
        "isotropy option",
        r"^[ \t]*\(AN\)ISOTROPY OPTION[ \t]*="
        r"[ \t]*ISOTROPIC[ \t]*$",
    ),
    (
        "MCCG door",
        r"^[ \t]*FLUX SOLUTION DOOR[ \t]*="
        r"[ \t]*\*\*[ \t]*MCCG[ \t]*\*\*[ \t]*$",
    ),
    (
        "group count",
        r"^[ \t]*NB\. OF GROUPS[ \t]*=[ \t]*370[ \t]*$",
    ),
    (
        "region count",
        r"^[ \t]*NB\. OF REGIONS[ \t]*=[ \t]*8[ \t]*$",
    ),
    (
        "unknown count",
        r"^[ \t]*NB\. OF UNKNOWNS PER GROUP[ \t]*="
        r"[ \t]*14[ \t]*$",
    ),
    (
        "leakage-zone count",
        r"^[ \t]*NB\. OF LEAKAGE ZONES[ \t]*=[ \t]*1[ \t]*$",
    ),
    (
        "outer cap",
        r"^[ \t]*MAX\. OUTER ITERATIONS[ \t]*=[ \t]*1[ \t]*$",
    ),
    (
        "inner cap",
        r"^[ \t]*MAX\. THERMAL ITERATIONS[ \t]*=[ \t]*740[ \t]*$",
    ),
    (
        "stationary acceleration",
        r"^[ \t]*ACCELERATION SCHEME[ \t]*=[ \t]*"
        r"\([ \t]*1[ \t]+FREE,[ \t]*0[ \t]+ACCELERATED\)[ \t]*$",
    ),
    (
        "rebalancing",
        r"^[ \t]*REBALANCING OPTION[ \t]*=[ \t]*ON[ \t]*$",
    ),
    (
        "self-scattering reduction",
        r"^[ \t]*SELF-SCATTERING REDUCTION[ \t]*="
        r"[ \t]*ON[ \t]*$",
    ),
    (
        "fundamental mode",
        r"^[ \t]*FUNDAMENTAL MODE[ \t]*=[ \t]*ON[ \t]*$",
    ),
    (
        "eigenvalue tolerance",
        r"^[ \t]*EIGENVALUE TOLERANCE[ \t]*="
        r"[ \t]*2\.500E-07[ \t]*$",
    ),
    (
        "outer unknown tolerance",
        r"^[ \t]*UNKNOWN OUTER TOLERANCE[ \t]*="
        r"[ \t]*2\.500E-07[ \t]*$",
    ),
    (
        "inner unknown tolerance",
        r"^[ \t]*UNKNOWN INNER TOLERANCE[ \t]*="
        r"[ \t]*2\.500E-07[ \t]*$",
    ),
    (
        "transport-corrected cross sections",
        r"^[ \t]*USE TRANSPORT CORRECTED CROSS-SECTIONS[ \t]*$",
    ),
    (
        "MOC branch",
        r"^[ \t]*M O C PARAMETERS:[ \t]+NON CYCLIC[ \t]+"
        r"-[ \t]+STIS 1[ \t]+-[ \t]+SC SCHEME[ \t]+"
        r"-[ \t]+TABULATED EXP[ \t]*$",
    ),
)


def fail(message: str) -> None:
    raise SystemExit("RAW-MOC-CAPTURE RUN-LOGS FAIL: " + message)


def require_one(
    pattern: str | re.Pattern[str],
    text: str,
    description: str,
) -> re.Match[str]:
    compiled = (
        pattern
        if isinstance(pattern, re.Pattern)
        else re.compile(pattern, re.MULTILINE)
    )
    matches = list(compiled.finditer(text))
    if len(matches) != 1:
        fail(f"{description}: expected one record, found {len(matches)}")
    return matches[0]


def load_text(path: Path, description: str) -> str:
    if path.is_symlink():
        fail(f"{description} is a symlink")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read {description}: {exc}")
    if not raw:
        fail(f"{description} is empty")
    if b"\0" in raw:
        fail(f"{description} contains a NUL byte")
    if b"\r" in raw:
        fail(f"{description} does not use canonical LF line endings")
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError as exc:
        fail(f"{description} is not ASCII: {exc}")


def validate_envelope(text: str, description: str) -> int:
    normal_ends = list(NORMAL_END_RE.finditer(text))
    if (
        len(normal_ends) != 1
        or text.count("normal end of execution for dragon") != 1
    ):
        fail(f"{description} lacks one normal Dragon termination")
    if len(re.findall(r"^cle2000_c:\s*cpu time=", text, re.MULTILINE)) != 1:
        fail(f"{description} lacks one CLE-2000 CPU receipt")
    for pattern, label in (
        (r"\bXABORT\b", "XABORT"),
        (r"segmentation fault", "segmentation fault"),
        (r"floating invalid", "floating invalid"),
        (r"bus error", "bus error"),
        (r"illegal instruction", "illegal instruction"),
        (r"\b(?:NaN|Inf(?:inity)?)\b", "non-finite text"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            fail(f"{description} contains abnormal {label}")
    if text.count("@AUDIT_CONTROL@") != 0:
        fail(f"{description} contains an unresolved audit-control token")
    return normal_ends[0].start()


def active_source_moca_lines(listing: str) -> list[tuple[str, int | None]]:
    records: list[tuple[str, int | None]] = []
    for line in listing.splitlines():
        if re.search(r"\bMOCA\b", line) is None:
            continue
        if line.lstrip().startswith("*"):
            continue
        matches = list(SOURCE_MOCA_RE.finditer(line))
        has_source_number = (
            re.search(r"[ \t][0-9]{4}[ \t]*$", line) is not None
        )
        code = (
            int(matches[0].group(1))
            if len(matches) == 1 and has_source_number
            else None
        )
        records.append((line, code))
    return records


def execution_moca_lines(text: str) -> list[tuple[str, int | None]]:
    records: list[tuple[str, int | None]] = []
    for line in text.splitlines():
        if not line.startswith("<|") or re.search(r"\bMOCA\b", line) is None:
            continue
        match = TRACE_MOCA_RE.match(line)
        records.append((line, int(match.group(1)) if match else None))
    return records


def validate_moca(
    text: str,
    expected_arm: int | None,
    description: str,
) -> None:
    trace_start = re.search(r"^<\|", text, re.MULTILINE)
    if trace_start is None:
        fail(f"{description} lacks a CLE execution trace")
    listing = text[: trace_start.start()]
    source_records = active_source_moca_lines(listing)
    trace_records = execution_moca_lines(text)
    if expected_arm is None:
        if source_records or trace_records:
            fail(f"{description} OFF log contains an active MOCA control")
        return
    if len(source_records) != 1 or source_records[0][1] != expected_arm:
        fail(
            f"{description} source listing lacks exactly one active "
            f"MOCA {expected_arm} line"
        )
    if len(trace_records) != 1 or trace_records[0][1] != expected_arm:
        fail(
            f"{description} execution trace lacks exactly one "
            f"MOCA {expected_arm} line"
        )


def extract_science(text: str, description: str) -> bytes:
    start = require_one(
        SCIENCE_START_RE, text, description + " scientific-block start"
    )
    end = require_one(
        SCIENCE_END_RE, text, description + " scientific-block end"
    )
    if start.start() >= end.start():
        fail(f"{description} scientific block is reordered")
    end_position = text.find("\n", end.end())
    if end_position == -1:
        end_position = len(text)
    else:
        end_position += 1
    block = text[start.start() : end_position]
    if block.count("FLU2DR: CPU TIME=") != 2:
        fail(f"{description} scientific block lacks two CPU records")
    normalized, substitutions = CPU_TIME_RE.subn(
        r"\1<CPU-TELEMETRY>", block
    )
    if substitutions != 2:
        fail(f"{description} has malformed FLU2DR CPU telemetry")
    return normalized.encode("ascii")


def validate_locked_science(
    text: str,
    description: str,
    normal_end_position: int,
) -> bytes:
    for label, pattern in CONTROL_LINES:
        require_one(pattern, text, f"{description} {label}")

    outer = require_one(
        r"^[ \t]*FLU2DR-DIAG OUTER IEXTF=[ \t]*1 "
        r"MAXOUT=[ \t]*1\b.*$",
        text,
        description + " one-step outer diagnostic",
    )
    inner = require_one(
        r"^[ \t]*FLU2DR-DIAG INNER ITERF=[ \t]*1 "
        r"MAXINR=[ \t]*740\b.*NGRP=[ \t]*370[ \t]*$",
        text,
        description + " one-step inner diagnostic",
    )
    if re.search(r"^[ \t]*FLU2DR-TERM\b", text, re.MULTILINE):
        fail(f"{description} contains a strict-terminal claim")
    if outer.start() >= inner.start() or inner.start() >= normal_end_position:
        fail(f"{description} terminal records are reordered")

    inner_steps = re.findall(
        r"^[ \t]*IN\([ \t]*(\d+)\)[ \t]+FLX:", text, re.MULTILINE
    )
    outer_steps = re.findall(
        r"^[ \t]*OUT\([ \t]*(\d+)\)[ \t]+FLX:", text, re.MULTILINE
    )
    if inner_steps != ["1"] or outer_steps != ["1"]:
        fail(f"{description} is not exactly one printed FLU update")

    warning_count = len(
        re.findall(
            r"^[ \t]*\*\*\* FLU2DR: CONVERGENCE NOT REACHED "
            r"\*\*\*[ \t]*$",
            text,
            re.MULTILINE,
        )
    )
    if warning_count != 3:
        fail(f"{description} lacks exactly three one-step warnings")
    require_one(
        r"^[ \t]*FLU2DR: CPU TIME=[ \t]*"
        rf"{NUMBER}\.?"
        r"[ \t]+INTERNAL CONVERGENCE \*NEARLY\* REACHED AFTER"
        r"[ \t]+1 ITERATIONS\.[ \t]*$",
        text,
        description + " internal one-step record",
    )
    require_one(
        r"^[ \t]*FLU2DR: CPU TIME=[ \t]*"
        rf"{NUMBER}\.?"
        r"[ \t]+EXTERNAL CONVERGENCE[ \t]+\*NOT\* REACHED AFTER"
        r"[ \t]+1 ITERATIONS\.[ \t]*$",
        text,
        description + " external one-step record",
    )
    tracking = require_one(
        r"^[ \t]*\+\+ TRACKING CALLED=[ \t]*1 TIMES "
        r"PRECISION=[ \t]*0\.00E\+00[ \t]*$",
        text,
        description + " tracking-call count",
    )
    total = require_one(
        SCIENCE_END_RE,
        text,
        description + " flux-calculation count",
    )
    if not (inner.start() < tracking.start() < total.start()):
        fail(f"{description} call-count records are reordered")
    return extract_science(text, description)


@dataclass(frozen=True)
class ParsedLog:
    arm: str
    mode: str
    science: bytes


def parse_log(
    path: Path,
    arm: str,
    mode: str,
    arm_code: int,
) -> ParsedLog:
    description = f"{arm} {mode}"
    text = load_text(path, description)
    normal_end_position = validate_envelope(text, description)
    validate_moca(
        text,
        arm_code if mode == "ON" else None,
        description,
    )
    science = validate_locked_science(
        text, description, normal_end_position
    )
    return ParsedLog(arm=arm, mode=mode, science=science)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("native_off_log", type=Path)
    parser.add_argument("native_on_log", type=Path)
    parser.add_argument("stationary_off_log", type=Path)
    parser.add_argument("stationary_on_log", type=Path)
    args = parser.parse_args()

    paths = (
        args.native_off_log,
        args.native_on_log,
        args.stationary_off_log,
        args.stationary_on_log,
    )
    if len({str(path.resolve()) for path in paths}) != 4:
        fail("the four log paths must be distinct")

    native_off = parse_log(paths[0], "NATIVE", "OFF", 1)
    native_on = parse_log(paths[1], "NATIVE", "ON", 1)
    stationary_off = parse_log(paths[2], "STATIONARY", "OFF", 2)
    stationary_on = parse_log(paths[3], "STATIONARY", "ON", 2)

    if native_off.science != native_on.science:
        fail("NATIVE OFF/ON scientific FLU blocks differ")
    if stationary_off.science != stationary_on.science:
        fail("STATIONARY OFF/ON scientific FLU blocks differ")
    print(PASS_LINE)


if __name__ == "__main__":
    main()

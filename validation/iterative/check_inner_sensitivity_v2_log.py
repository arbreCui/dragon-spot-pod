#!/usr/bin/env python3
"""Fail-closed raw-log audit for one Stage-4 v2 coarse map.

This parser reads the unmodified Dragon log.  It verifies the exact 3+1 solve
structure, strict FLU terminal records, frozen binary32 tolerance, iteration
caps, map markers, and normal process completion.  It does not classify the
four scientific components; that decision comes only from the Ganlib XSM
checker.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path
import re
import struct
import sys


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
ECHO_PATTERN = re.compile(r"^>\|(.*?)\|>(\d{4})\s*$")
EXPECTED_TOLERANCE_BITS = 0x358637BD
EXPECTED_MAXOUT = 500
EXPECTED_MAXINR = 740
EXPECTED_GROUPS = 370


def fail(message: str) -> None:
    print("INNER-SENSITIVITY-V2 LOG FAIL: " + message, file=sys.stderr)
    raise SystemExit(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def as_float(token: str) -> float:
    try:
        value = float(token.replace("D", "E").replace("d", "e"))
    except ValueError:
        fail(f"invalid number: {token}")
    require(math.isfinite(value), f"non-finite number: {token}")
    return value


def f32(value: float) -> float:
    try:
        return struct.unpack(">f", struct.pack(">f", value))[0]
    except OverflowError:
        fail(f"value is outside binary32: {value}")


def f32_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


def line_of(text: str, match: re.Match[str]) -> int:
    return text.count("\n", 0, match.start()) + 1


@dataclass(frozen=True)
class Echo:
    payload: str
    source_line: int
    log_line: int


def parse_echoes(lines: list[str]) -> list[Echo]:
    echoes: list[Echo] = []
    previous_log_line = -1
    for log_line, line in enumerate(lines, 1):
        match = ECHO_PATTERN.fullmatch(line)
        if match is None:
            require(
                not line.lstrip().startswith(">|"),
                f"malformed ECHO at log line {log_line}",
            )
            continue
        payload = match.group(1).strip()
        source_line = int(match.group(2))
        if (
            echoes
            and echoes[-1].source_line == source_line
            and log_line == previous_log_line + 1
            and echoes[-1].payload.startswith(
                "STAGE4V2-COARSE-DOUT-2H"
            )
        ):
            prior = echoes[-1]
            echoes[-1] = Echo(
                payload=(prior.payload + " " + payload).strip(),
                source_line=source_line,
                log_line=prior.log_line,
            )
        else:
            echoes.append(Echo(payload, source_line, log_line))
        previous_log_line = log_line
    return echoes


def one_echo(echoes: list[Echo], marker: str) -> Echo:
    matches = [item for item in echoes if item.payload.startswith(marker)]
    require(len(matches) == 1, f"expected one {marker}, found {len(matches)}")
    return matches[0]


def marker_numbers(
    echoes: list[Echo],
    marker: str,
    count: int,
) -> tuple[float, ...]:
    fields = one_echo(echoes, marker).payload.split()
    require(
        len(fields) == count + 1 and fields[0] == marker,
        f"invalid fields for {marker}",
    )
    return tuple(as_float(token) for token in fields[1:])


OUTER = re.compile(
    rf"^\s*FLU2DR-TERM OUTER-GATE=PASS "
    rf"IEXTF=\s*(\d+) MAXOUT=\s*(\d+) KEFF=\s*({NUMBER}) "
    rf"EEXT=\s*({NUMBER}) EPSOUT=\s*({NUMBER}) "
    rf"EUNK=\s*({NUMBER}) EPSUNK=\s*({NUMBER}) "
    rf"EUNK-VALID=(\d+)\s*$",
    re.MULTILINE,
)
INNER = re.compile(
    rf"^\s*FLU2DR-TERM INNER-TERMINAL "
    rf"ITERF=\s*(\d+) MAXINR=\s*(\d+) "
    rf"EINR=\s*({NUMBER}) EPSINR=\s*({NUMBER}) "
    rf"IGDEB=\s*(\d+) STATE=(\d+) NGRP=\s*(\d+)\s*$",
    re.MULTILINE,
)


def verify_terminal_records(
    text: str,
    echoes: list[Echo],
    tolerance: float,
) -> None:
    outer = list(OUTER.finditer(text))
    inner = list(INNER.finditer(text))
    outer_total = len(
        re.findall(r"^\s*FLU2DR-TERM OUTER-GATE=", text, re.MULTILINE)
    )
    inner_total = len(
        re.findall(r"^\s*FLU2DR-TERM INNER-TERMINAL\b", text, re.MULTILINE)
    )
    require(
        len(outer) == len(inner) == outer_total == inner_total == 4,
        "expected exactly four paired FLU terminal records",
    )
    for index in range(4):
        require(
            outer[index].start() < inner[index].start(),
            f"solve {index + 1} terminal order differs",
        )
        if index < 3:
            require(
                inner[index].start() < outer[index + 1].start(),
                f"solve {index + 1} terminal records interleave",
            )

    outer_lines = [line_of(text, item) for item in outer]
    radial_begin = one_echo(
        echoes, "STAGE4V2-COARSE-RADIAL-BEGIN"
    ).log_line
    radial_end = one_echo(
        echoes, "STAGE4V2-COARSE-RADIAL-END"
    ).log_line
    axial_begin = one_echo(
        echoes, "STAGE4V2-COARSE-AXIAL-BEGIN"
    ).log_line
    axial_end = one_echo(
        echoes, "STAGE4V2-COARSE-AXIAL-END"
    ).log_line
    require(
        all(radial_begin < line < radial_end for line in outer_lines[:3]),
        "three radial terminals are not inside the radial block",
    )
    require(
        radial_end < axial_begin < outer_lines[3] < axial_end,
        "returned axial terminal is not inside the axial block",
    )

    printed_tolerance = float(f"{f32(tolerance):.8E}")
    for index, (outer_match, inner_match) in enumerate(
        zip(outer, inner, strict=True),
        1,
    ):
        iextf = int(outer_match.group(1))
        maxout = int(outer_match.group(2))
        keff = as_float(outer_match.group(3))
        eext = as_float(outer_match.group(4))
        epsout = as_float(outer_match.group(5))
        eunk = as_float(outer_match.group(6))
        epsunk = as_float(outer_match.group(7))
        eunk_valid = int(outer_match.group(8))
        iterf = int(inner_match.group(1))
        maxinr = int(inner_match.group(2))
        einr = as_float(inner_match.group(3))
        epsinr = as_float(inner_match.group(4))
        igdeb = int(inner_match.group(5))
        state = int(inner_match.group(6))
        ngrp = int(inner_match.group(7))
        require(
            maxout == EXPECTED_MAXOUT
            and maxinr == EXPECTED_MAXINR
            and 0 <= iextf < maxout
            and 0 <= iterf < maxinr,
            f"solve {index} reached or changed an iteration cap",
        )
        require(
            keff > 0.0 and eunk_valid == 1 and state == 1,
            f"solve {index} lacks a strict terminal state",
        )
        if index <= 3:
            require(keff == 1.0, f"radial solve {index} is multiplying")
        require(
            0.0 <= eext <= epsout
            and 0.0 <= eunk <= epsunk
            and 0.0 <= einr <= epsinr,
            f"solve {index} residual exceeds its declared control",
        )
        require(
            epsout == epsunk == epsinr == printed_tolerance,
            f"solve {index} tolerance differs from coarse 2h",
        )
        require(
            ngrp == EXPECTED_GROUPS and igdeb == ngrp + 1,
            f"solve {index} did not finish all energy groups",
        )


def verify_markers(text: str, echoes: list[Echo]) -> None:
    own = [
        "STAGE4V2-COARSE-BEGIN",
        "STAGE4V2-COARSE-RANK",
        "STAGE4V2-COARSE-TOLERANCE",
        "STAGE4V2-COARSE-X0-REUSED",
        "STAGE4V2-COARSE-STATE0",
        "STAGE4V2-COARSE-LEAKAGE0",
        "STAGE4V2-COARSE-RADIAL-BEGIN",
        "STAGE4V2-COARSE-RADIAL-END",
        "STAGE4V2-COARSE-RADIAL-CONTRACT",
        "STAGE4V2-COARSE-AXIAL-BEGIN",
        "STAGE4V2-COARSE-AXIAL-END",
        "STAGE4V2-COARSE-DOUT-2H",
        "STAGE4V2-COARSE-STATE1",
        "STAGE4V2-COARSE-LEAKAGE1",
        "STAGE4V2-COARSE-COMPLETE",
    ]
    for marker in own:
        one_echo(echoes, marker)
    lines = [one_echo(echoes, marker).log_line for marker in own]
    require(
        lines == sorted(lines) and len(lines) == len(set(lines)),
        "coarse-map markers are not in strict order",
    )
    for marker in (
        "STAGE4V2-COARSE-BEGIN",
        "STAGE4V2-COARSE-X0-REUSED",
        "STAGE4V2-COARSE-RADIAL-BEGIN",
        "STAGE4V2-COARSE-RADIAL-END",
        "STAGE4V2-COARSE-AXIAL-BEGIN",
        "STAGE4V2-COARSE-AXIAL-END",
        "STAGE4V2-COARSE-COMPLETE",
    ):
        require(
            one_echo(echoes, marker).payload == marker,
            f"{marker} has unexpected fields",
        )
    require(
        marker_numbers(echoes, "STAGE4V2-COARSE-RANK", 1) == (1.0,),
        "rank differs from one",
    )
    tolerance = marker_numbers(
        echoes, "STAGE4V2-COARSE-TOLERANCE", 1
    )[0]
    require(
        f32_bits(tolerance) == EXPECTED_TOLERANCE_BITS,
        "coarse tolerance bits differ from 0x358637bd",
    )
    state0 = marker_numbers(echoes, "STAGE4V2-COARSE-STATE0", 1)
    state1 = marker_numbers(echoes, "STAGE4V2-COARSE-STATE1", 1)
    leak0 = marker_numbers(echoes, "STAGE4V2-COARSE-LEAKAGE0", 1)
    leak1 = marker_numbers(echoes, "STAGE4V2-COARSE-LEAKAGE1", 1)
    defect = marker_numbers(echoes, "STAGE4V2-COARSE-DOUT-2H", 4)
    require(
        state0[0] > 0.0 and state1[0] > 0.0,
        "state marker is nonphysical",
    )
    require(
        leak0[0] >= 0.0
        and leak1[0] >= 0.0
        and all(value >= 0.0 for value in defect),
        "leakage or defect marker is negative",
    )

    plane_pattern = re.compile(r"SPOT-REFRESH-FS-PLANE (\d+) OF (\d+)")
    plane_items = [
        item
        for item in echoes
        if item.payload.startswith("SPOT-REFRESH-FS-PLANE")
    ]
    planes = []
    for item in plane_items:
        match = plane_pattern.fullmatch(item.payload)
        require(match is not None, "malformed radial-plane marker")
        planes.append((int(match.group(1)), int(match.group(2))))
    require(
        planes == [(1, 3), (2, 3), (3, 3)],
        "radial planes are not exactly 1,2,3",
    )

    result_pattern = re.compile(
        rf"SPOT-REFRESH-FS-RESULT\s+(\d+)\s+"
        rf"({NUMBER})\s+({NUMBER})"
    )
    result_items = [
        item
        for item in echoes
        if item.payload.startswith("SPOT-REFRESH-FS-RESULT")
    ]
    require(len(result_items) == 3, "expected three radial result markers")
    for expected_plane, item in enumerate(result_items, 1):
        match = result_pattern.fullmatch(item.payload)
        require(match is not None, "malformed radial result marker")
        require(
            int(match.group(1)) == expected_plane,
            "radial result order differs",
        )
        require(
            as_float(match.group(2)) >= 0.0
            and as_float(match.group(3)) >= 0.0,
            "negative radial result diagnostic",
        )

    contract = one_echo(
        echoes, "STAGE4V2-COARSE-RADIAL-CONTRACT"
    ).payload.split()
    require(len(contract) == 6, "invalid radial contract fields")
    require(
        int(contract[1]) == 1 and int(contract[2]) == 3,
        "fixed-basis or radial-solve census marker differs",
    )
    require(
        all(as_float(token) >= 0.0 for token in contract[3:]),
        "negative radial contract diagnostic",
    )
    require(
        len(echoes) == 21,
        f"expected exactly 21 ECHO records, found {len(echoes)}",
    )
    verify_terminal_records(text, echoes, tolerance)

    require(
        "SPOGBAL" not in text,
        "coarse deck entered the unsafe production SPOGBAL path",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    args = parser.parse_args()

    raw = args.log.read_bytes()
    require(raw and b"\0" not in raw, "log is empty or contains NUL")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail("log is not UTF-8/ASCII")
    require(
        re.search(
            r"\bXABORT\b|\bABORT\b|ERROR STOP|\bFATAL\b|"
            r"floating point exception|segmentation fault|bus error|"
            r"illegal instruction|fortran runtime error|"
            r"\b(?:SIGSEGV|SIGFPE|SIGBUS|SIGILL|SIGABRT)\b|"
            r"\bbacktrace\b|error termination|core dumped|"
            r"^\s*ERROR\s*:",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        is None,
        "abnormal termination marker is present",
    )
    require(
        re.search(
            r"(?<![A-Za-z])(?:NAN|[+-]?INF(?:INITY)?)(?![A-Za-z])",
            text,
            re.IGNORECASE,
        )
        is None,
        "non-finite token is present",
    )
    require(
        re.search(
            r"^[ \t]*FLU2DR-DIAG[ \t]+(?:OUTER|INNER)\b",
            text,
            re.MULTILINE,
        )
        is None,
        "one or more FLU solves lacked strict termination",
    )
    require(
        re.search(
            r"^\*{3}\s*FLU2DR:\s*CONVERGENCE NOT REACHED\s*\*{3}$",
            text,
            re.MULTILINE,
        )
        is None,
        "FLU convergence warning is present",
    )
    normal = list(
        re.finditer(
            r"^[ \t]*normal end of execution for dragon\b.*$",
            text,
            re.MULTILINE,
        )
    )
    require(len(normal) == 1, "expected one Dragon normal-end marker")
    lines = text.splitlines()
    normal_line = line_of(text, normal[0])
    footer = [line.strip() for line in lines[normal_line:] if line.strip()]
    require(
        footer
        == [
            "check for warning in listing",
            "before assuming your run was successful",
        ],
        "unexpected text follows Dragon normal end",
    )
    echoes = parse_echoes(lines)
    verify_markers(text, echoes)
    require(
        one_echo(echoes, "STAGE4V2-COARSE-COMPLETE").log_line
        < normal_line,
        "normal end precedes coarse-map completion",
    )
    print("INNER-SENSITIVITY-V2 LOG STRUCTURE PASS")
    print("INNER-SENSITIVITY-V2 LOG TOLERANCE PASS: 2h=0x358637bd")
    print("INNER-SENSITIVITY-V2 LOG INNER SOLVES PASS: 3 radial + 1 axial")
    print("INNER-SENSITIVITY-V2 LOG OUTER CONVERGENCE NOT EVALUATED")
    print("INNER-SENSITIVITY-V2 LOG COMPLETE")


if __name__ == "__main__":
    main()

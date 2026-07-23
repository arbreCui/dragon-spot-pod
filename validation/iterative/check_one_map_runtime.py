#!/usr/bin/env python3
"""Independent structural check of one fixed-space SPOT map log.

This checker verifies only execution structure, declared inner-solver
termination, positivity diagnostics, and the presence of the raw map defect.
It deliberately does not turn that one defect into an outer-convergence
decision.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path
import re
import struct


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
OUTPUT_ECHO_PATTERN = re.compile(r"^>\|(.*?)\|>(\d{4})\s*$")


def as_float(token: str) -> float:
    value = float(token.replace("D", "E").replace("d", "e"))
    if not math.isfinite(value):
        fail(f"non-finite numeric field: {token}")
    return value


def f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def fail(message: str) -> None:
    raise SystemExit("ONE-MAP RUNTIME FAIL: " + message)


def exactly_one(pattern: str, text: str, description: str) -> re.Match[str]:
    matches = list(re.finditer(pattern, text, re.MULTILINE))
    if len(matches) != 1:
        fail(f"expected one {description}, found {len(matches)}")
    return matches[0]


def line_of(text: str, match: re.Match[str]) -> int:
    return text.count("\n", 0, match.start()) + 1


def normalized_exponent(token: str) -> str:
    return token.replace("d", "E").replace("e", "E")


def require_strict_order(events: list[tuple[str, int]], description: str) -> None:
    lines = [line for _, line in events]
    if lines != sorted(lines) or len(lines) != len(set(lines)):
        rendered = ", ".join(f"{name}@{line}" for name, line in events)
        fail(f"{description} is not in strict order: {rendered}")


@dataclass(frozen=True)
class Echo:
    payload: str
    source_line: int
    log_line: int


def parse_echoes(lines: list[str]) -> list[Echo]:
    echoes: list[Echo] = []
    previous_echo_log_line = -1
    for log_line, line in enumerate(lines, 1):
        match = OUTPUT_ECHO_PATTERN.fullmatch(line)
        if match is None:
            continue
        payload = match.group(1).strip()
        source_line = int(match.group(2))
        if (
            echoes
            and echoes[-1].source_line == source_line
            and log_line == previous_echo_log_line + 1
            and echoes[-1].payload.startswith(
                "ITERATIVE-MAP-RAW-DEFECT-X0"
            )
        ):
            previous = echoes[-1]
            echoes[-1] = Echo(
                (previous.payload + " " + payload).strip(),
                source_line,
                previous.log_line,
            )
        else:
            echoes.append(Echo(payload, source_line, log_line))
        previous_echo_log_line = log_line
    return echoes


def one_echo(echoes: list[Echo], marker: str) -> Echo:
    matches = [item for item in echoes if item.payload.startswith(marker)]
    if len(matches) != 1:
        fail(f"expected one output marker {marker}, found {len(matches)}")
    return matches[0]


def marker_numbers(echoes: list[Echo], marker: str, count: int) -> list[float]:
    fields = one_echo(echoes, marker).payload.split()
    if len(fields) != count + 1 or fields[0] != marker:
        fail(f"invalid fields for output marker {marker}")
    return [as_float(token) for token in fields[1:]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    args = parser.parse_args()

    raw = args.log.read_bytes()
    if not raw or b"\0" in raw:
        fail("log is empty or contains NUL bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"log is not strict UTF-8/ASCII: {exc}")
    lines = text.splitlines()
    for log_line, line in enumerate(lines, 1):
        if line.lstrip().startswith(">|") and not (
            OUTPUT_ECHO_PATTERN.fullmatch(line)
        ):
            fail(f"malformed output marker at log line {log_line}")
    echoes = parse_echoes(lines)
    init_tolerance_echoes = [
        item
        for item in echoes
        if item.payload.startswith("ITERATIVE-MAP-INIT-TOLERANCE")
    ]
    map_tolerance_echoes = [
        item
        for item in echoes
        if item.payload.startswith("ITERATIVE-MAP-MAP-TOLERANCE")
    ]
    legacy_tolerance_echoes = [
        item
        for item in echoes
        if item.payload.startswith("ITERATIVE-MAP-INNER-TOLERANCE")
    ]
    split_tolerance = bool(
        init_tolerance_echoes or map_tolerance_echoes
    )
    if split_tolerance:
        if (
            len(init_tolerance_echoes) != 1
            or len(map_tolerance_echoes) != 1
            or legacy_tolerance_echoes
        ):
            fail("invalid split initializer/map tolerance markers")
        expected_echo_count = 20
        tolerance_markers = [
            "ITERATIVE-MAP-INIT-TOLERANCE",
            "ITERATIVE-MAP-MAP-TOLERANCE",
        ]
    else:
        if (
            len(legacy_tolerance_echoes) != 1
            or init_tolerance_echoes
            or map_tolerance_echoes
        ):
            fail("invalid one-map tolerance marker")
        expected_echo_count = 19
        tolerance_markers = ["ITERATIVE-MAP-INNER-TOLERANCE"]
    if len(echoes) != expected_echo_count:
        fail(
            f"expected exactly {expected_echo_count} output markers, "
            f"found {len(echoes)}"
        )

    if re.search(
        r"\bXABORT\b|\bABORT\b|ERROR STOP|\bFATAL\b|"
        r"floating point exception|segmentation fault|bus error|"
        r"illegal instruction|fortran runtime error|"
        r"\b(?:SIGSEGV|SIGFPE|SIGBUS|SIGILL|SIGABRT)\b|"
        r"\bbacktrace\b|error termination|core dumped|"
        r"^\s*ERROR\s*:",
        text,
        re.IGNORECASE | re.MULTILINE,
    ):
        fail("abnormal termination marker is present")
    if re.search(
        r"(?<![A-Za-z])(?:NAN|[+-]?INF(?:INITY)?)(?![A-Za-z])",
        text,
        re.IGNORECASE,
    ):
        fail("non-finite token is present")
    normal_end = exactly_one(
        r"^[ \t]*normal end of execution for dragon\b.*$",
        text,
        "Dragon normal-end marker",
    )
    normal_end_line = line_of(text, normal_end)
    footer = [line.strip() for line in lines[normal_end_line:] if line.strip()]
    if footer != [
        "check for warning in listing",
        "before assuming your run was successful",
    ]:
        fail(f"unexpected text after Dragon normal end: {footer}")
    if re.search(
        r"^.*\bCONVERG(?:ED|ENCE)\b.*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    ):
        # The frozen Dragon protocol emits no outer-convergence statement,
        # including a negated one. The checker reports that boundary itself.
        fail("log contains an unauthorized outer-convergence claim")

    ordered = [
        "ITERATIVE-MAP-BEGIN",
        "ITERATIVE-MAP-RANK",
        *tolerance_markers,
        "ITERATIVE-MAP-BASIS-BUILT",
        "ITERATIVE-MAP-STATE0",
        "ITERATIVE-MAP-LEAKAGE0",
        "ITERATIVE-MAP-RADIAL-BEGIN",
        "ITERATIVE-MAP-RADIAL-END",
        "ITERATIVE-MAP-RADIAL-CONTRACT",
        "ITERATIVE-MAP-RAW-DEFECT-X0",
        "ITERATIVE-MAP-STATE1",
        "ITERATIVE-MAP-LEAKAGE1",
        "ITERATIVE-MAP-COMPLETE",
    ]
    marker_lines = [one_echo(echoes, marker).log_line for marker in ordered]
    if marker_lines != sorted(marker_lines) or len(set(marker_lines)) != len(
        marker_lines
    ):
        fail("ITERATIVE-MAP output markers are not in strict order")
    for marker in (
        "ITERATIVE-MAP-BEGIN",
        "ITERATIVE-MAP-BASIS-BUILT",
        "ITERATIVE-MAP-RADIAL-BEGIN",
        "ITERATIVE-MAP-RADIAL-END",
        "ITERATIVE-MAP-COMPLETE",
    ):
        if one_echo(echoes, marker).payload != marker:
            fail(f"output marker {marker} has unexpected fields")
    if normal_end_line <= one_echo(
        echoes, "ITERATIVE-MAP-COMPLETE"
    ).log_line:
        fail("Dragon normal end precedes map completion")
    complete_line = one_echo(
        echoes, "ITERATIVE-MAP-COMPLETE"
    ).log_line
    expected_end_source = (
        one_echo(echoes, "ITERATIVE-MAP-COMPLETE").source_line + 1
    )
    interlude = [
        line.strip()
        for line in lines[complete_line : normal_end_line - 1]
        if line.strip()
    ]
    if (
        len(interlude) != 2
        or re.fullmatch(
            rf"<\|END: ;[ \t]*\|<{expected_end_source:04d}",
            interlude[0],
        )
        is None
        or re.fullmatch(
            rf"cle2000_c: cpu time=[ \t]*{NUMBER} second",
            interlude[1],
        )
        is None
    ):
        fail(f"unexpected text between map completion and normal end: {interlude}")

    rank_values = marker_numbers(echoes, "ITERATIVE-MAP-RANK", 1)
    rank = int(rank_values[0])
    if rank_values[0] != rank or rank != 1:
        fail("the frozen one-map fixture must use rank 1")
    if split_tolerance:
        init_eps = marker_numbers(
            echoes, "ITERATIVE-MAP-INIT-TOLERANCE", 1
        )[0]
        solver_eps = marker_numbers(
            echoes, "ITERATIVE-MAP-MAP-TOLERANCE", 1
        )[0]
    else:
        solver_eps = marker_numbers(
            echoes, "ITERATIVE-MAP-INNER-TOLERANCE", 1
        )[0]
        init_eps = solver_eps
    if init_eps <= 0.0 or solver_eps <= 0.0:
        fail("declared solver tolerance is not positive")
    init_eps_bits = struct.unpack(">I", struct.pack(">f", init_eps))[0]
    solver_eps_bits = struct.unpack(">I", struct.pack(">f", solver_eps))[0]
    if init_eps_bits != 0x350637BD:
        fail("initializer tolerance differs from the frozen protocol")
    if split_tolerance:
        if solver_eps_bits != 0x348637BD:
            fail("map tolerance differs from the frozen h/2 protocol")
        if f32(2.0 * f32(solver_eps)) != f32(init_eps):
            fail("map tolerance is not the exact binary32 half")
    elif solver_eps_bits != 0x350637BD:
        fail("solver tolerance differs from the frozen one-map protocol")
    state0_echo = one_echo(echoes, "ITERATIVE-MAP-STATE0")
    leakage0_echo = one_echo(echoes, "ITERATIVE-MAP-LEAKAGE0")
    leakage1_echo = one_echo(echoes, "ITERATIVE-MAP-LEAKAGE1")
    state0 = marker_numbers(echoes, "ITERATIVE-MAP-STATE0", 1)
    leakage0 = marker_numbers(echoes, "ITERATIVE-MAP-LEAKAGE0", 1)
    leakage1 = marker_numbers(echoes, "ITERATIVE-MAP-LEAKAGE1", 1)
    if state0[0] <= 0.0 or leakage0[0] < 0.0 or leakage1[0] < 0.0:
        fail("initial state or direct leakage marker is invalid")

    outer_pattern = re.compile(
        rf"^\s*FLU2DR-TERM OUTER-GATE=PASS "
        rf"IEXTF=\s*(\d+) MAXOUT=\s*(\d+) KEFF=\s*({NUMBER}) "
        rf"EEXT=\s*({NUMBER}) EPSOUT=\s*({NUMBER}) "
        rf"EUNK=\s*({NUMBER}) EPSUNK=\s*({NUMBER}) "
        rf"EUNK-VALID=(\d+)\s*$",
        re.MULTILINE,
    )
    inner_pattern = re.compile(
        rf"^\s*FLU2DR-TERM INNER-TERMINAL "
        rf"ITERF=\s*(\d+) MAXINR=\s*(\d+) "
        rf"EINR=\s*({NUMBER}) EPSINR=\s*({NUMBER}) "
        rf"IGDEB=\s*(\d+) STATE=(\d+) NGRP=\s*(\d+)\s*$",
        re.MULTILINE,
    )
    outer = list(outer_pattern.finditer(text))
    inner = list(inner_pattern.finditer(text))
    outer_total = len(
        re.findall(r"^\s*FLU2DR-TERM OUTER-GATE=", text, re.MULTILINE)
    )
    inner_total = len(
        re.findall(r"^\s*FLU2DR-TERM INNER-TERMINAL\b", text, re.MULTILINE)
    )
    if (
        len(outer) != 5
        or len(inner) != 5
        or outer_total != 5
        or inner_total != 5
    ):
        fail(
            "expected five paired FLU terminal records "
            f"(pass={len(outer)}/{len(inner)}, "
            f"total={outer_total}/{inner_total})"
        )
    for index in range(5):
        if outer[index].start() >= inner[index].start():
            fail(f"solve {index + 1} inner terminal precedes its outer record")
        if index < 4 and inner[index].start() >= outer[index + 1].start():
            fail(f"solve {index + 1} terminal records are interleaved")
    outer_lines = [line_of(text, match) for match in outer]
    inner_lines = [line_of(text, match) for match in inner]
    radial_begin_line = one_echo(
        echoes, "ITERATIVE-MAP-RADIAL-BEGIN"
    ).log_line
    radial_end_line = one_echo(echoes, "ITERATIVE-MAP-RADIAL-END").log_line
    if not (
        outer_lines[0] < radial_begin_line
        and all(
            radial_begin_line < line < radial_end_line
            for line in outer_lines[1:4]
        )
        and radial_end_line < outer_lines[4]
    ):
        fail("the five FLU solves are not one axial, three radial, one axial")
    for index, (outer_match, inner_match) in enumerate(zip(outer, inner), 1):
        iextf, maxout = (int(outer_match.group(i)) for i in (1, 2))
        keff = as_float(outer_match.group(3))
        eext = as_float(outer_match.group(4))
        epsout = as_float(outer_match.group(5))
        eunk = as_float(outer_match.group(6))
        epsunk = as_float(outer_match.group(7))
        eunk_valid = int(outer_match.group(8))
        iterf, maxinr = (int(inner_match.group(i)) for i in (1, 2))
        einr = as_float(inner_match.group(3))
        epsinr = as_float(inner_match.group(4))
        igdeb, state, ngrp = (
            int(inner_match.group(i)) for i in (5, 6, 7)
        )

        if (
            maxout != 500
            or maxinr != 740
            or not (0 <= iextf < maxout)
            or not (0 <= iterf < maxinr)
        ):
            fail(f"solve {index} reached or exceeded an iteration limit")
        if keff <= 0.0 or eunk_valid != 1 or state != 1:
            fail(f"solve {index} has an invalid terminal state")
        if index in (2, 3, 4) and keff != 1.0:
            fail(f"radial fixed-source solve {index - 1} is not nonmultiplying")
        if (
            eext < 0.0
            or eunk < 0.0
            or einr < 0.0
            or eext > epsout
            or eunk > epsunk
            or einr > epsinr
        ):
            fail(f"solve {index} does not satisfy its declared tolerance")
        for label, actual in (
            ("EPSOUT", epsout),
            ("EPSUNK", epsunk),
            ("EPSINR", epsinr),
        ):
            # The solver prints binary32 controls with eight digits after the
            # decimal. This is a representation check, not a physics margin.
            expected_eps = init_eps if index == 1 else solver_eps
            printed_declared = float(f"{f32(expected_eps):.8E}")
            if actual != printed_declared:
                fail(
                    f"solve {index} {label} differs from the deck's "
                    "binary32 tolerance"
                )
        if igdeb != ngrp + 1 or ngrp != 370:
            fail(f"solve {index} did not finish all 370 energy groups")

    plane_pattern = re.compile(r"^SPOT-REFRESH-FS-PLANE (\d+) OF (\d+)$")
    plane_items = [
        item
        for item in echoes
        if item.payload.startswith("SPOT-REFRESH-FS-PLANE")
    ]
    plane_echoes = [plane_pattern.match(item.payload) for item in plane_items]
    if any(match is None for match in plane_echoes):
        fail("invalid fixed-source plane marker")
    planes = [
        (int(match.group(1)), int(match.group(2)))
        for match in plane_echoes
        if match is not None
    ]
    if planes != [(1, 3), (2, 3), (3, 3)]:
        fail(f"fixed-source planes are not exactly 1,2,3: {planes}")

    result_pattern = re.compile(
        rf"^SPOT-REFRESH-FS-RESULT\s+(\d+)\s+"
        rf"({NUMBER})\s+({NUMBER})$"
    )
    result_items = [
        item
        for item in echoes
        if item.payload.startswith("SPOT-REFRESH-FS-RESULT")
    ]
    result_echoes = [result_pattern.match(item.payload) for item in result_items]
    if len(result_echoes) != 3 or any(
        match is None for match in result_echoes
    ):
        fail("expected one fixed-source result for each of three planes")
    for expected_plane, match in enumerate(result_echoes, 1):
        assert match is not None
        if int(match.group(1)) != expected_plane:
            fail("fixed-source result order differs from plane order")
        response_l2 = as_float(match.group(2))
        radial_balance = as_float(match.group(3))
        if response_l2 < 0.0 or radial_balance < 0.0:
            fail("negative radial response or balance diagnostic")

    contract = one_echo(echoes, "ITERATIVE-MAP-RADIAL-CONTRACT").payload.split()
    if len(contract) != 6:
        fail("invalid radial-contract marker")
    fixed_marker, fs_count = int(contract[1]), int(contract[2])
    contract_values = [as_float(token) for token in contract[3:]]
    if fixed_marker != 1 or fs_count != 3:
        fail("fixed-basis or fixed-source-count contract is false")
    if any(value < 0.0 for value in contract_values):
        fail("negative radial contract diagnostic")

    source_pattern = re.compile(
        rf"^SPOFSRC KEFF/QSUM/QMIN/QMAX\s+"
        rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    sources = list(source_pattern.finditer(text))
    if len(sources) != 3:
        fail(f"expected three frozen-source records, found {len(sources)}")
    for index, match in enumerate(sources, 1):
        keff, qsum, qmin, qmax = (
            as_float(match.group(i)) for i in range(1, 5)
        )
        if (
            keff <= 0.0
            or qsum <= 0.0
            or qmin < 0.0
            or qmax <= 0.0
            or qmin > qmax
        ):
            fail(f"plane {index} has a nonphysical frozen source")

    radial_pattern = re.compile(
        rf"^SPOFCHK L2/MAX/RBAL/MIN/QSUM\s+"
        rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+"
        rf"({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    radial = list(radial_pattern.finditer(text))
    if len(radial) != 3:
        fail(f"expected three radial audits, found {len(radial)}")
    for index, match in enumerate(radial, 1):
        response_l2, response_max, balance, minimum, qsum = (
            as_float(match.group(i)) for i in range(1, 6)
        )
        if (
            response_l2 < 0.0
            or response_max < 0.0
            or balance < 0.0
            or minimum <= 0.0
            or qsum <= 0.0
        ):
            fail(f"plane {index} radial audit is nonphysical")

    rank_pattern = re.compile(
        r"^\s*SPOASM: modal ranks across\s+370 groups: "
        r"min=\s*(\d+), max=\s*(\d+) \(snapshot count=\s*(\d+)\)$",
        re.MULTILINE,
    )
    rank_records = list(rank_pattern.finditer(text))
    if len(rank_records) != 2 or any(
        tuple(int(match.group(i)) for i in range(1, 4)) != (rank, rank, 3)
        for match in rank_records
    ):
        fail("offline and returned systems do not use the frozen rank")
    physical_s0_record = exactly_one(
        r"^\s*SPOASM: physical S0 recovered for\s+1110 "
        r"snapshot-group systems$",
        text,
        "physical fixed-source census",
    )
    reuse_record = exactly_one(
        r"^\s*SPOASM: reused fixed POD basis with requested rank=\s*1$",
        text,
        "fixed-basis reuse marker",
    )
    removal_pattern = re.compile(
        rf"^\s*SPOASM: min effective removal=\s*({NUMBER}) "
        r"at snapshot/group/mixture=\s*\d+\s+\d+\s+\d+$",
        re.MULTILINE,
    )
    removal_records = list(removal_pattern.finditer(text))
    if len(removal_records) != 2 or any(
        as_float(match.group(1)) <= 0.0 for match in removal_records
    ):
        fail("effective removal is not strictly positive")

    gbal_pattern = re.compile(
        rf"^SPOGBAL GLOBAL/MAX-GROUP\s+({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    gbal_records = list(gbal_pattern.finditer(text))
    if len(gbal_records) != 2:
        fail("expected two axial global-balance audits")
    if any(
        as_float(match.group(index)) < 0.0
        for match in gbal_records
        for index in (1, 2)
    ):
        fail("negative axial balance norm")
    galerkin_pattern = re.compile(
        rf"^SPOGBAL GALERKIN-MAX G/M/F SIGNED/RATIO\s+"
        rf"(\d+)\s+(\d+)\s+(\d+)\s+"
        rf"({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    galerkin_records = list(galerkin_pattern.finditer(text))
    if len(galerkin_records) != 2:
        fail("expected two axial Galerkin diagnostics")
    for index, match in enumerate(galerkin_records):
        group, mode, floor = (
            int(match.group(i)) for i in (1, 2, 3)
        )
        signed = as_float(match.group(4))
        ratio = as_float(match.group(5))
        if (
            not (1 <= group <= 370)
            or mode != rank
            or not (1 <= floor <= 60)
            or ratio < 0.0
            or abs(signed) != ratio
        ):
            fail(f"axial Galerkin diagnostic {index} is invalid")
    phi_pattern = re.compile(
        rf"^SPOGBAL PHI MIN/MAX/WORST-RATIO NONPOS/WORST-G/WORST-R\s+"
        rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+"
        rf"(\d+)\s+(\d+)\s+(\d+)$",
        re.MULTILINE,
    )
    phi_records = list(phi_pattern.finditer(text))
    if len(phi_records) != 2:
        fail("expected two axial positivity audits")
    for index, match in enumerate(phi_records):
        minimum, maximum, worst_ratio = (
            as_float(match.group(i)) for i in (1, 2, 3)
        )
        nonpositive, worst_group, worst_region = (
            int(match.group(i)) for i in (4, 5, 6)
        )
        if (
            minimum <= 0.0
            or maximum < minimum
            or worst_ratio < 0.0
            or nonpositive != 0
            or not (1 <= worst_group <= 370)
            or not (1 <= worst_region <= 360)
        ):
            fail(f"axial positivity audit {index} is invalid")

    state_pattern = re.compile(
        rf"^SPOSTATE NCOEF/RHO/NORM/PERP/GERR\s+"
        rf"(\d+)\s+({NUMBER})\s+({NUMBER})\s+"
        rf"({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    states = list(state_pattern.finditer(text))
    if len(states) != 2:
        fail("expected two canonical-state records")
    for index, match in enumerate(states):
        ncoef = int(match.group(1))
        rho, norm, offspace, gram_error = (
            as_float(match.group(i)) for i in range(2, 6)
        )
        if (
            ncoef != 1110
            or rho <= 0.0
            or norm <= 0.0
            or offspace < 0.0
            or gram_error < 0.0
        ):
            fail(f"canonical state {index} is invalid")

    defect_match = exactly_one(
        rf"^SPOXCONV RRHO/RLEAK/DLEAK/RA\s+"
        rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})$",
        text,
        "raw map defect",
    )
    defect = [as_float(defect_match.group(i)) for i in range(1, 5)]
    if any(value < 0.0 for value in defect):
        fail("raw map defect contains a negative norm")
    marker_defect_echo = one_echo(
        echoes, "ITERATIVE-MAP-RAW-DEFECT-X0"
    ).payload.split()
    if len(marker_defect_echo) != 5:
        fail("invalid raw-defect output marker")
    for token in marker_defect_echo[1:]:
        as_float(token)
    expected_marker_tokens = [f"{value:.15E}" for value in defect]
    if [
        token.replace("d", "E").replace("e", "E")
        for token in marker_defect_echo[1:]
    ] != expected_marker_tokens:
        fail("raw-defect marker differs from SPOXCONV output")

    leakage_pattern = re.compile(
        rf"^SPOLEAK DIRECT ERROR/MIN/MAX\s+"
        rf"({NUMBER})\s+({NUMBER})\s+({NUMBER})$",
        re.MULTILINE,
    )
    leakage_records = list(leakage_pattern.finditer(text))
    if len(leakage_records) != 2:
        fail("expected two direct leakage-return audits")
    for index, match in enumerate(leakage_records):
        error, minimum, maximum = (
            as_float(match.group(i)) for i in (1, 2, 3)
        )
        if error < 0.0 or maximum < minimum:
            fail(f"direct leakage-return audit {index} is invalid")
    leakage0_error = as_float(leakage_records[0].group(1))
    leakage1_error = as_float(leakage_records[1].group(1))
    if leakage1_error != defect[2]:
        fail("returned state leakage change differs from absolute DLEAK")
    leakage0_token = leakage0_echo.payload.split()[1]
    leakage1_token = leakage1_echo.payload.split()[1]
    if leakage0_token.lower() != f"{f32(leakage0_error):.6e}":
        fail("initial leakage marker differs from direct leakage return")
    if leakage1_token.lower() != f"{f32(defect[2]):.6e}":
        fail("returned leakage marker differs from absolute DLEAK")

    state1_echo = one_echo(echoes, "ITERATIVE-MAP-STATE1")
    state1 = marker_numbers(echoes, "ITERATIVE-MAP-STATE1", 3)
    if state1[0] <= 0.0 or state1[1] < 0.0 or state1[2] < 0.0:
        fail("returned eigenvalue or balance marker is invalid")

    state0_token = state0_echo.payload.split()[1]
    state1_tokens = state1_echo.payload.split()[1:]
    if state0_token.lower() != f"{f32(as_float(outer[0].group(3))):.6e}":
        fail("initial-state marker differs from first axial eigenvalue")
    if state1_tokens[0].lower() != (
        f"{f32(as_float(outer[4].group(3))):.6e}"
    ):
        fail("returned-state marker differs from second axial eigenvalue")
    if f"{state1[1]:.5E}" != normalized_exponent(
        gbal_records[1].group(1)
    ):
        fail("returned-state global balance differs from SPOGBAL")
    if f"{state1[2]:.5E}" != normalized_exponent(
        gbal_records[1].group(2)
    ):
        fail("returned-state group balance differs from SPOGBAL")

    first_axial_keff = f"{f32(as_float(outer[0].group(3))):.5E}"
    for index, (source, audit, result) in enumerate(
        zip(sources, radial, result_echoes), 1
    ):
        assert result is not None
        if normalized_exponent(source.group(1)) != first_axial_keff:
            fail(f"plane {index} source eigenvalue differs from state x0")
        if normalized_exponent(source.group(2)) != normalized_exponent(
            audit.group(5)
        ):
            fail(f"plane {index} source and radial QSUM differ")
        if f"{as_float(result.group(2)):.5E}" != normalized_exponent(
            audit.group(1)
        ):
            fail(f"plane {index} result and radial L2 differ")
        if f"{as_float(result.group(3)):.5E}" != normalized_exponent(
            audit.group(3)
        ):
            fail(f"plane {index} result and radial balance differ")

    require_strict_order(
        [
            ("offline modal rank", line_of(text, rank_records[0])),
            ("offline removal", line_of(text, removal_records[0])),
            (
                "basis-built",
                one_echo(echoes, "ITERATIVE-MAP-BASIS-BUILT").log_line,
            ),
            ("axial-0 outer", outer_lines[0]),
            ("axial-0 inner", inner_lines[0]),
            ("axial-0 balance", line_of(text, gbal_records[0])),
            (
                "axial-0 Galerkin diagnostic",
                line_of(text, galerkin_records[0]),
            ),
            ("axial-0 positivity", line_of(text, phi_records[0])),
            ("state x0", line_of(text, states[0])),
            ("state0 marker", state0_echo.log_line),
            ("leakage x0", line_of(text, leakage_records[0])),
            ("leakage0 marker", leakage0_echo.log_line),
            (
                "radial begin",
                one_echo(echoes, "ITERATIVE-MAP-RADIAL-BEGIN").log_line,
            ),
        ],
        "initial axial-state event sequence",
    )
    for index in range(3):
        next_boundary = (
            plane_items[index + 1].log_line
            if index < 2
            else one_echo(echoes, "ITERATIVE-MAP-RADIAL-END").log_line
        )
        require_strict_order(
            [
                (f"plane {index + 1}", plane_items[index].log_line),
                (
                    f"plane {index + 1} source",
                    line_of(text, sources[index]),
                ),
                (f"plane {index + 1} outer", outer_lines[index + 1]),
                (f"plane {index + 1} inner", inner_lines[index + 1]),
                (
                    f"plane {index + 1} audit",
                    line_of(text, radial[index]),
                ),
                (
                    f"plane {index + 1} result",
                    result_items[index].log_line,
                ),
                (f"plane {index + 1} boundary", next_boundary),
            ],
            f"radial plane {index + 1} event sequence",
        )
    require_strict_order(
        [
            (
                "radial end",
                one_echo(echoes, "ITERATIVE-MAP-RADIAL-END").log_line,
            ),
            ("returned modal rank", line_of(text, rank_records[1])),
            ("fixed-source census", line_of(text, physical_s0_record)),
            ("fixed-basis reuse", line_of(text, reuse_record)),
            ("returned removal", line_of(text, removal_records[1])),
            (
                "radial contract",
                one_echo(
                    echoes, "ITERATIVE-MAP-RADIAL-CONTRACT"
                ).log_line,
            ),
            ("axial-1 outer", outer_lines[4]),
            ("axial-1 inner", inner_lines[4]),
            ("axial-1 balance", line_of(text, gbal_records[1])),
            (
                "axial-1 Galerkin diagnostic",
                line_of(text, galerkin_records[1]),
            ),
            ("axial-1 positivity", line_of(text, phi_records[1])),
            ("state x1", line_of(text, states[1])),
            ("raw defect", line_of(text, defect_match)),
            (
                "raw-defect marker",
                one_echo(
                    echoes, "ITERATIVE-MAP-RAW-DEFECT-X0"
                ).log_line,
            ),
            ("state1 marker", state1_echo.log_line),
            ("leakage x1", line_of(text, leakage_records[1])),
            ("leakage1 marker", leakage1_echo.log_line),
            (
                "map complete",
                one_echo(echoes, "ITERATIVE-MAP-COMPLETE").log_line,
            ),
            ("Dragon normal end", normal_end_line),
        ],
        "returned axial-state event sequence",
    )

    print("ONE-MAP RUNTIME STRUCTURE PASS")
    if split_tolerance:
        print(
            "ONE-MAP RUNTIME TOLERANCE SCHEDULE PASS: "
            "initializer=h; map=h/2"
        )
    print("ONE-MAP RUNTIME INNER SOLVES PASS: 2 axial + 3 radial")
    print("ONE-MAP RUNTIME FIXED-SPACE RADIAL UPDATE PASS: 3 planes")
    print(
        "ONE-MAP RUNTIME RETURNED GALERKIN DIAGNOSTIC "
        + f"{as_float(galerkin_records[1].group(5)):.5E}"
    )
    print(
        "ONE-MAP RUNTIME RAW DEFECT "
        + " ".join(f"{value:.16E}" for value in defect)
    )
    print("ONE-MAP RUNTIME OUTER CONVERGENCE NOT EVALUATED")
    print("ONE-MAP RUNTIME COMPLETE")


if __name__ == "__main__":
    main()

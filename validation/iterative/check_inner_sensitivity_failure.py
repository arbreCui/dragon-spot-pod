#!/usr/bin/env python3
"""Issue a fail-closed receipt for the frozen Stage-4 h/2 failure.

This checker recognizes one specific execution outcome: the initializer and
returned axial solves terminate normally, while each of the three radial
fixed-source solves exhausts MAXOUT before satisfying the h/2 unknown and
inner residual controls.  That outcome is an absorbing provenance failure.
Consequently, state1 and the raw defect may prove that the deck completed,
but they are never reported or classified as scientific results here.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import struct
from typing import Any


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
OUTPUT_ECHO_PATTERN = re.compile(r"^>\|(.*?)\|>(\d{4})\s*$")
WARNING = "*** FLU2DR: CONVERGENCE NOT REACHED ***"

EXPECTED_PROTOCOL: dict[str, Any] = {
    "schema": "spot-inner-sensitivity-v1",
    "method": "fixed-space Galerkin-SPOD inner-tolerance sensitivity",
    "groups": 370,
    "planes": 3,
    "rank": 1,
    "initializer_solver_eps_f32_bits": "0x350637bd",
    "baseline_map_solver_eps_f32_bits": "0x350637bd",
    "refined_map_solver_eps_f32_bits": "0x348637bd",
    "refinement_identity": (
        "2 * refined_map_solver_eps == baseline_map_solver_eps in binary32"
    ),
    "maxout": 500,
    "maxinr": 740,
    "initializer_axial_solves": 1,
    "map_radial_solves": 3,
    "map_axial_solves": 1,
    "outer_updates": 1,
    "same_x0_evidence": [
        (
            "identical Dragon executable, procedures, seed archives, rank "
            "and initializer controls"
        ),
        "byte-identical basis_reference.xsm",
        "byte-identical state0_axial.xsm",
        (
            "bitwise-identical canonical a, rho, L, basis, Gram matrix, "
            "plane heights and normalization"
        ),
        (
            "bitwise-identical radial SPOT-LEAK1D, SPOT-QFISS and SPOT-FS-K "
            "inputs"
        ),
    ],
    "reported_vectors": [
        "D_out_h = D(x1_h, x0)",
        "D_out_h2 = D(x1_h2, x0)",
        "D_in = D(x1_h2, x1_h)",
    ],
    "components": ["R_rho", "R_L", "D_L", "R_a"],
    "component_rule": {
        "positive_outer": "RESOLVED iff D_in < D_out_h",
        "zero_outer": "RESOLVED iff D_in == 0 at stored precision",
        "otherwise": "UNRESOLVED",
    },
    "aggregation": None,
    "relaxation": None,
    "fitting": None,
    "outer_convergence": "not_evaluated",
    "h2_replay": "required before final Stage-4 qualification",
    "stage4_state_rule": {
        "any_component_unresolved": "UNRESOLVED",
        "all_components_resolved_without_h2_replay": "PENDING-REPLAY",
        "all_components_resolved_with_h2_replay": "QUALIFIED",
    },
    "stage5_authorization": (
        "only if all four components are RESOLVED and both lanes pass every "
        "physical and execution contract"
    ),
}


def fail(message: str) -> None:
    raise SystemExit("INNER-SENSITIVITY FAILURE FAIL: " + message)


def read_strict_text(path: Path, description: str) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        fail(f"cannot read {description}: {exc}")
    if not raw or b"\0" in raw:
        fail(f"{description} is empty or contains NUL bytes")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{description} is not strict UTF-8/ASCII: {exc}")


def reject_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"protocol contains duplicate key {key!r}")
        result[key] = value
    return result


def load_protocol(path: Path) -> dict[str, Any]:
    text = read_strict_text(path, "protocol")
    try:
        protocol = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except (json.JSONDecodeError, RecursionError) as exc:
        fail(f"protocol is not strict JSON: {exc}")
    if not isinstance(protocol, dict) or protocol != EXPECTED_PROTOCOL:
        fail("protocol differs from the frozen Stage-4 contract")
    return protocol


def as_float(token: str) -> float:
    try:
        value = float(token.replace("D", "E").replace("d", "e"))
    except ValueError:
        fail(f"invalid numeric field: {token}")
    if not math.isfinite(value):
        fail(f"non-finite numeric field: {token}")
    return value


def f32_bits(value: float) -> int:
    try:
        return struct.unpack(">I", struct.pack(">f", value))[0]
    except OverflowError:
        fail(f"numeric field is outside binary32: {value}")


def line_of(text: str, match: re.Match[str]) -> int:
    return text.count("\n", 0, match.start()) + 1


def exactly_one(
    pattern: re.Pattern[str],
    text: str,
    description: str,
) -> re.Match[str]:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        fail(f"expected one {description}, found {len(matches)}")
    return matches[0]


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
            if line.lstrip().startswith(">|"):
                fail(f"malformed output marker at log line {log_line}")
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
                payload=(previous.payload + " " + payload).strip(),
                source_line=source_line,
                log_line=previous.log_line,
            )
        else:
            echoes.append(Echo(payload, source_line, log_line))
        previous_echo_log_line = log_line
    return echoes


def one_echo(echoes: list[Echo], marker: str) -> Echo:
    matches = [echo for echo in echoes if echo.payload.startswith(marker)]
    if len(matches) != 1:
        fail(f"expected one output marker {marker}, found {len(matches)}")
    return matches[0]


def parse_marker_numbers(
    echo: Echo,
    marker: str,
    count: int,
) -> tuple[float, ...]:
    fields = echo.payload.split()
    if len(fields) != count + 1 or fields[0] != marker:
        fail(f"invalid fields for output marker {marker}")
    return tuple(as_float(token) for token in fields[1:])


@dataclass(frozen=True)
class Outer:
    kind: str
    iextf: int
    maxout: int
    keff: float
    eext: float
    epsout: float
    eunk: float
    epsunk: float
    eunk_valid: int
    start: int
    end: int


@dataclass(frozen=True)
class Inner:
    kind: str
    iterf: int
    maxinr: int
    einr: float
    epsinr: float
    igdeb: int
    state: int
    ngrp: int
    start: int
    end: int


OUTER_PATTERN = re.compile(
    rf"^[ \t]*FLU2DR-(TERM|DIAG) "
    rf"(?:OUTER-GATE=PASS|OUTER) "
    rf"IEXTF=[ \t]*(\d+) MAXOUT=[ \t]*(\d+) "
    rf"KEFF=[ \t]*({NUMBER}) EEXT=[ \t]*({NUMBER}) "
    rf"EPSOUT=[ \t]*({NUMBER}) EUNK=[ \t]*({NUMBER}) "
    rf"EPSUNK=[ \t]*({NUMBER}) EUNK-VALID=(\d+)[ \t]*$",
    re.MULTILINE,
)
INNER_PATTERN = re.compile(
    rf"^[ \t]*FLU2DR-(TERM|DIAG) "
    rf"(?:INNER-TERMINAL|INNER) "
    rf"ITERF=[ \t]*(\d+) MAXINR=[ \t]*(\d+) "
    rf"EINR=[ \t]*({NUMBER}) EPSINR=[ \t]*({NUMBER}) "
    rf"IGDEB=[ \t]*(\d+) STATE=(\d+) NGRP=[ \t]*(\d+)[ \t]*$",
    re.MULTILINE,
)


def parse_outer(match: re.Match[str]) -> Outer:
    kind = match.group(1)
    prefix = match.group(0)
    if kind == "TERM" and "OUTER-GATE=PASS" not in prefix:
        fail("TERM outer record lacks OUTER-GATE=PASS")
    if kind == "DIAG" and "OUTER-GATE=PASS" in prefix:
        fail("DIAG outer record uses a terminal-pass label")
    return Outer(
        kind=kind,
        iextf=int(match.group(2)),
        maxout=int(match.group(3)),
        keff=as_float(match.group(4)),
        eext=as_float(match.group(5)),
        epsout=as_float(match.group(6)),
        eunk=as_float(match.group(7)),
        epsunk=as_float(match.group(8)),
        eunk_valid=int(match.group(9)),
        start=match.start(),
        end=match.end(),
    )


def parse_inner(match: re.Match[str]) -> Inner:
    kind = match.group(1)
    prefix = match.group(0)
    if kind == "TERM" and "INNER-TERMINAL" not in prefix:
        fail("TERM inner record lacks INNER-TERMINAL")
    if kind == "DIAG" and "INNER-TERMINAL" in prefix:
        fail("DIAG inner record uses a terminal-pass label")
    return Inner(
        kind=kind,
        iterf=int(match.group(2)),
        maxinr=int(match.group(3)),
        einr=as_float(match.group(4)),
        epsinr=as_float(match.group(5)),
        igdeb=int(match.group(6)),
        state=int(match.group(7)),
        ngrp=int(match.group(8)),
        start=match.start(),
        end=match.end(),
    )


def validate_common(
    outer: Outer,
    inner: Inner,
    expected_eps_bits: int,
    description: str,
) -> None:
    if outer.maxout != 500 or inner.maxinr != 740:
        fail(f"{description} iteration controls differ from the protocol")
    if outer.eunk_valid != 1 or outer.keff <= 0.0:
        fail(f"{description} has an invalid eigenvalue/unknown record")
    if outer.eext < 0.0 or outer.eunk < 0.0 or inner.einr < 0.0:
        fail(f"{description} has a negative residual")
    if (
        f32_bits(outer.epsout) != expected_eps_bits
        or f32_bits(outer.epsunk) != expected_eps_bits
        or f32_bits(inner.epsinr) != expected_eps_bits
    ):
        fail(f"{description} tolerances differ from the protocol")
    if inner.ngrp != 370:
        fail(f"{description} does not use 370 energy groups")
    if outer.start >= inner.start:
        fail(f"{description} inner record precedes its outer record")


def validate_pass(
    outer: Outer,
    inner: Inner,
    expected_eps_bits: int,
    description: str,
) -> None:
    validate_common(outer, inner, expected_eps_bits, description)
    if outer.kind != "TERM" or inner.kind != "TERM":
        fail(f"{description} is not a terminal PASS pair")
    if not (0 <= outer.iextf < outer.maxout):
        fail(f"{description} reached the outer iteration limit")
    if not (0 <= inner.iterf < inner.maxinr):
        fail(f"{description} reached the inner iteration limit")
    if inner.state != 1 or inner.igdeb != 371:
        fail(f"{description} did not finish all 370 groups")
    if (
        outer.eext > outer.epsout
        or outer.eunk > outer.epsunk
        or inner.einr > inner.epsinr
    ):
        fail(f"{description} exceeds a declared tolerance")


def validate_radial_failure(
    outer: Outer,
    inner: Inner,
    plane: int,
) -> None:
    description = f"radial plane {plane}"
    validate_common(outer, inner, 0x348637BD, description)
    if outer.kind != "DIAG" or inner.kind != "DIAG":
        fail(f"{description} is not a diagnostic failure pair")
    if outer.iextf != outer.maxout or outer.maxout != 500:
        fail(f"{description} did not exhaust MAXOUT=500")
    if inner.state != 2:
        fail(f"{description} does not have STATE=2")
    if not (1 <= inner.igdeb < 371):
        fail(f"{description} IGDEB does not identify an unfinished group")
    if outer.keff != 1.0:
        fail(f"{description} is not a nonmultiplying fixed-source solve")
    if outer.eunk <= outer.epsunk or inner.einr <= inner.epsinr:
        fail(f"{description} does not prove EUNK/EINR > EPS")


def validate_echoes(
    text: str,
    lines: list[str],
) -> tuple[list[Echo], list[Echo], list[Echo]]:
    echoes = parse_echoes(lines)
    if len(echoes) != 20:
        fail(f"expected exactly 20 output markers, found {len(echoes)}")

    expected_sequence = [
        "ITERATIVE-MAP-BEGIN",
        "ITERATIVE-MAP-RANK",
        "ITERATIVE-MAP-INIT-TOLERANCE",
        "ITERATIVE-MAP-MAP-TOLERANCE",
        "ITERATIVE-MAP-BASIS-BUILT",
        "ITERATIVE-MAP-STATE0",
        "ITERATIVE-MAP-LEAKAGE0",
        "ITERATIVE-MAP-RADIAL-BEGIN",
        "SPOT-REFRESH-FS-PLANE",
        "SPOT-REFRESH-FS-RESULT",
        "SPOT-REFRESH-FS-PLANE",
        "SPOT-REFRESH-FS-RESULT",
        "SPOT-REFRESH-FS-PLANE",
        "SPOT-REFRESH-FS-RESULT",
        "ITERATIVE-MAP-RADIAL-END",
        "ITERATIVE-MAP-RADIAL-CONTRACT",
        "ITERATIVE-MAP-RAW-DEFECT-X0",
        "ITERATIVE-MAP-STATE1",
        "ITERATIVE-MAP-LEAKAGE1",
        "ITERATIVE-MAP-COMPLETE",
    ]
    for index, (echo, marker) in enumerate(
        zip(echoes, expected_sequence, strict=True),
        1,
    ):
        if not echo.payload.startswith(marker):
            fail(
                f"output marker {index} is {echo.payload!r}, "
                f"expected {marker}"
            )

    for marker in (
        "ITERATIVE-MAP-BEGIN",
        "ITERATIVE-MAP-BASIS-BUILT",
        "ITERATIVE-MAP-RADIAL-BEGIN",
        "ITERATIVE-MAP-RADIAL-END",
        "ITERATIVE-MAP-COMPLETE",
    ):
        if one_echo(echoes, marker).payload != marker:
            fail(f"output marker {marker} has unexpected fields")

    rank = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-RANK"),
        "ITERATIVE-MAP-RANK",
        1,
    )[0]
    init_eps = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-INIT-TOLERANCE"),
        "ITERATIVE-MAP-INIT-TOLERANCE",
        1,
    )[0]
    map_eps = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-MAP-TOLERANCE"),
        "ITERATIVE-MAP-MAP-TOLERANCE",
        1,
    )[0]
    if rank != 1.0:
        fail("deck rank marker differs from rank 1")
    if f32_bits(init_eps) != 0x350637BD:
        fail("initializer tolerance marker differs from h")
    if f32_bits(map_eps) != 0x348637BD:
        fail("map tolerance marker differs from h/2")
    if struct.unpack(">f", struct.pack(">I", 0x348637BD))[0] * 2.0 != (
        struct.unpack(">f", struct.pack(">I", 0x350637BD))[0]
    ):
        fail("frozen binary32 h/2 identity is false")

    state0 = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-STATE0"),
        "ITERATIVE-MAP-STATE0",
        1,
    )
    leakage0 = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-LEAKAGE0"),
        "ITERATIVE-MAP-LEAKAGE0",
        1,
    )
    leakage1 = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-LEAKAGE1"),
        "ITERATIVE-MAP-LEAKAGE1",
        1,
    )
    if state0[0] <= 0.0 or leakage0[0] < 0.0 or leakage1[0] < 0.0:
        fail("state0 or leakage completion marker is invalid")

    plane_echoes = [
        echo
        for echo in echoes
        if echo.payload.startswith("SPOT-REFRESH-FS-PLANE")
    ]
    result_echoes = [
        echo
        for echo in echoes
        if echo.payload.startswith("SPOT-REFRESH-FS-RESULT")
    ]
    plane_pattern = re.compile(
        r"SPOT-REFRESH-FS-PLANE\s+(\d+)\s+OF\s+(\d+)"
    )
    result_pattern = re.compile(
        rf"SPOT-REFRESH-FS-RESULT\s+(\d+)\s+({NUMBER})\s+({NUMBER})"
    )
    for plane, (plane_echo, result_echo) in enumerate(
        zip(plane_echoes, result_echoes, strict=True),
        1,
    ):
        plane_match = plane_pattern.fullmatch(plane_echo.payload)
        result_match = result_pattern.fullmatch(result_echo.payload)
        if (
            plane_match is None
            or (int(plane_match.group(1)), int(plane_match.group(2)))
            != (plane, 3)
        ):
            fail(f"invalid plane marker for radial plane {plane}")
        if result_match is None or int(result_match.group(1)) != plane:
            fail(f"invalid result marker for radial plane {plane}")
        if (
            as_float(result_match.group(2)) < 0.0
            or as_float(result_match.group(3)) < 0.0
        ):
            fail(f"negative radial completion diagnostic for plane {plane}")

    contract = one_echo(
        echoes, "ITERATIVE-MAP-RADIAL-CONTRACT"
    ).payload.split()
    if len(contract) != 6 or contract[:3] != [
        "ITERATIVE-MAP-RADIAL-CONTRACT",
        "1",
        "3",
    ]:
        fail("invalid radial-contract marker")
    if any(as_float(token) < 0.0 for token in contract[3:]):
        fail("negative radial-contract diagnostic")

    # These two rows prove only that the deck reached its tail.  Their values
    # are deliberately not returned by this function or printed by main().
    raw_defect = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-RAW-DEFECT-X0"),
        "ITERATIVE-MAP-RAW-DEFECT-X0",
        4,
    )
    state1 = parse_marker_numbers(
        one_echo(echoes, "ITERATIVE-MAP-STATE1"),
        "ITERATIVE-MAP-STATE1",
        3,
    )
    if any(value < 0.0 for value in raw_defect):
        fail("raw defect completion marker is malformed")
    if state1[0] <= 0.0 or any(value < 0.0 for value in state1[1:]):
        fail("state1 completion marker is malformed")

    if any(
        line.lstrip().startswith(">|")
        and OUTPUT_ECHO_PATTERN.fullmatch(line) is None
        for line in lines
    ):
        fail("malformed output marker is present")
    return echoes, plane_echoes, result_echoes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("h2_log", type=Path)
    parser.add_argument("protocol", type=Path)
    args = parser.parse_args()

    load_protocol(args.protocol)
    text = read_strict_text(args.h2_log, "h/2 log")
    lines = text.splitlines()

    if re.search(
        r"\bXABORT\b|\bABORT\b|ERROR STOP|\bFATAL\b|"
        r"floating point exception|segmentation fault|bus error|"
        r"illegal instruction|fortran runtime error|"
        r"\b(?:SIGSEGV|SIGFPE|SIGBUS|SIGILL|SIGABRT)\b|"
        r"\bbacktrace\b|error termination|core dumped|"
        r"^[ \t]*ERROR[ \t]*:",
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
    convergence_lines = [
        line.strip()
        for line in lines
        if re.search(r"\bCONVERG", line, re.IGNORECASE)
    ]
    if convergence_lines != [WARNING] * 9:
        fail(
            "expected exactly three convergence-not-reached warnings "
            "for each of three radial solves"
        )

    echoes, plane_echoes, result_echoes = validate_echoes(text, lines)

    normal_end = exactly_one(
        re.compile(
            r"^[ \t]*normal end of execution for dragon\b.*$",
            re.IGNORECASE | re.MULTILINE,
        ),
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
    complete = one_echo(echoes, "ITERATIVE-MAP-COMPLETE")
    if complete.log_line >= normal_end_line:
        fail("Dragon normal end precedes map completion")
    expected_end_source = complete.source_line + 1
    interlude = [
        line.strip()
        for line in lines[complete.log_line : normal_end_line - 1]
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
        fail(f"unexpected text between deck completion and normal end: {interlude}")

    outer_matches = list(OUTER_PATTERN.finditer(text))
    inner_matches = list(INNER_PATTERN.finditer(text))
    outer_total = len(
        re.findall(
            r"^[ \t]*FLU2DR-(?:TERM|DIAG)[ \t]+",
            text,
            re.MULTILINE,
        )
    )
    if len(outer_matches) != 5 or len(inner_matches) != 5:
        fail(
            "expected five recognized outer and inner FLU records, "
            f"found {len(outer_matches)}/{len(inner_matches)}"
        )
    if outer_total != 10:
        fail("unrecognized or extra FLU terminal/diagnostic record is present")
    outers = [parse_outer(match) for match in outer_matches]
    inners = [parse_inner(match) for match in inner_matches]
    for solve, (outer, inner) in enumerate(
        zip(outers, inners, strict=True),
        1,
    ):
        if outer.start >= inner.start:
            fail(f"solve {solve} inner record precedes its outer record")
        if solve < 5 and inner.end >= outers[solve].start:
            fail(f"solve {solve} terminal records are interleaved")

    validate_pass(outers[0], inners[0], 0x350637BD, "initializer solve")
    for plane in range(1, 4):
        validate_radial_failure(outers[plane], inners[plane], plane)
    validate_pass(outers[4], inners[4], 0x348637BD, "returned axial solve")

    line_offsets: list[int] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        line_offsets.append(offset)
        offset += len(line)

    def echo_offset(echo: Echo) -> int:
        return line_offsets[echo.log_line - 1]

    basis_pos = echo_offset(
        one_echo(echoes, "ITERATIVE-MAP-BASIS-BUILT")
    )
    state0_pos = echo_offset(one_echo(echoes, "ITERATIVE-MAP-STATE0"))
    radial_begin_pos = echo_offset(
        one_echo(echoes, "ITERATIVE-MAP-RADIAL-BEGIN")
    )
    radial_end_pos = echo_offset(
        one_echo(echoes, "ITERATIVE-MAP-RADIAL-END")
    )
    contract_pos = echo_offset(
        one_echo(echoes, "ITERATIVE-MAP-RADIAL-CONTRACT")
    )
    raw_defect_pos = echo_offset(
        one_echo(echoes, "ITERATIVE-MAP-RAW-DEFECT-X0")
    )
    if not (
        basis_pos < outers[0].start < inners[0].start < state0_pos
        < radial_begin_pos
    ):
        fail("initializer PASS pair is outside the initializer interval")

    warning_pattern = re.compile(
        r"^[ \t]*\*\*\* FLU2DR: CONVERGENCE NOT REACHED \*\*\*[ \t]*$",
        re.MULTILINE,
    )
    warning_matches = list(warning_pattern.finditer(text))
    for plane in range(1, 4):
        outer = outers[plane]
        inner = inners[plane]
        plane_start = echo_offset(plane_echoes[plane - 1])
        result_start = echo_offset(result_echoes[plane - 1])
        warnings = warning_matches[(plane - 1) * 3 : plane * 3]
        if len(warnings) != 3:
            fail(f"radial plane {plane} does not have one warning block")
        if not (
            plane_start < outer.start < inner.start
            < warnings[0].start() < warnings[1].start()
            < warnings[2].start() < result_start
        ):
            fail(
                f"radial plane {plane} DIAG and warning block do not "
                "correspond to its plane/result markers"
            )
        between = text[inner.end : result_start]
        if len(warning_pattern.findall(between)) != 3:
            fail(
                f"radial plane {plane} has an extra or missing "
                "convergence-not-reached warning"
            )
    if not (
        inners[3].end < radial_end_pos < contract_pos
        < outers[4].start < inners[4].start < raw_defect_pos
    ):
        fail("returned axial PASS pair is outside the returned-axial interval")

    print("CAPTURE INVALID-INNER-NONCONVERGENCE")
    for plane in range(1, 4):
        outer = outers[plane]
        inner = inners[plane]
        print(
            f"PLANE {plane} IEXTF={outer.iextf} IGDEB={inner.igdeb} "
            f"EUNK={outer.eunk:.8E} EPS={outer.epsunk:.8E}"
        )
    print("STAGE4 INVALID")
    print("STAGE5 NOT-AUTHORIZED")
    print("OUTER-CONVERGENCE NOT-EVALUATED")


if __name__ == "__main__":
    main()

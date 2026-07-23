#!/usr/bin/env python3
"""Fail-closed status machine for the bounded radial-floor diagnostic.

The checker consumes four independent Dragon logs.  It validates production
FLU2DR termination records and the complete printed IN/OUT iteration history;
it does not infer an equation residual or qualify the failed Stage-4 map.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import struct


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
EPS_BITS = 0x348637BD
ARM_IDS = ("NATIVE", "STATIONARY")

EXPECTED_PROTOCOL = {
    "schema": "spot-radial-floor-diagnostic-v1",
    "purpose": (
        "bounded plane-1 numerical diagnostic after the invalid "
        "Stage-4 h/2 capture"
    ),
    "scientific_scope": (
        "diagnostic only; it neither repairs nor qualifies the failed "
        "Stage-4 map"
    ),
    "plane": 1,
    "groups": 370,
    "production_solver": {
        "module": "FLU:",
        "implementation": "FLU2DR",
        "source_modification": False,
        "calculation_type": "S",
        "door": "MCCG",
        "rebalancing": "ON and identical in both arms and both probes",
        "solver_eps_f32_bits": "0x348637bd",
        "maxinr": 740,
        "strict_gate": (
            "EEXT < EPSOUT and EUNK < EPSUNK and EINR < EPSINR "
            "and inner STATE == 1 and IEXTF >= 2"
        ),
    },
    "common_restart": {
        "source": (
            "preserved plane-1 terminal flux from the invalid h/2 "
            "MAXOUT=500 capture"
        ),
        "arm_input_bytes": "identical",
        "physical_inputs": (
            "bitwise-identical operator, fixed source, system, track, "
            "tolerance and rebalancing"
        ),
        "cycle_history": (
            "reset independently on entry to each fresh FLU2DR "
            "invocation; no AKEEP or ZMU history is transferred"
        ),
    },
    "acce_coupling": (
        "one ACCE pair controls both the inner and outer FLU2DR "
        "acceleration schedules within an invocation; their counters are "
        "distinct, both restart at one, and they may not be tuned "
        "independently"
    ),
    "main_arms": [
        {
            "id": "NATIVE",
            "maxout": 6,
            "free_steps": 3,
            "accelerated_steps": 3,
            "termination": (
                "normal strict early exit at IEXTF 2 through 6, "
                "otherwise a diagnostic cap at IEXTF 6"
            ),
        },
        {
            "id": "STATIONARY",
            "maxout": 6,
            "free_steps": 1,
            "accelerated_steps": 0,
            "termination": (
                "normal strict early exit at IEXTF 2 through 6, "
                "otherwise a diagnostic cap at IEXTF 6"
            ),
        },
    ],
    "terminal_probes": {
        "count": 2,
        "input": "the corresponding main-arm terminal flux",
        "maxout": 1,
        "free_steps": 1,
        "accelerated_steps": 0,
        "cycle_history": (
            "reset on entry to the fresh probe FLU2DR invocation"
        ),
        "termination": (
            "diagnostic cap at IEXTF 1 because the production strict "
            "gate requires IEXTF >= 2"
        ),
        "quantity": (
            "one stationary production-map step; a Ganlib-only checker "
            "reports its post-minus-pre fixed-point defect"
        ),
    },
    "raw_log_contract": {
        "main_arm_terminal_states": ["STRICT", "CAP"],
        "record_every_inner_iteration": (
            "EINR and ZMU from each IN(n) FLX record"
        ),
        "record_every_outer_iteration": (
            "EUNK and ZMU from each OUT(n) FLX record"
        ),
        "probe_state": "ONE-STEP-DIAGNOSTIC",
        "comparison_states": [
            "BOTH-STRICT",
            "NATIVE-ONLY-STRICT",
            "STATIONARY-ONLY-STRICT",
            "BOTH-CAP",
            "INCONCLUSIVE-NO-OUTER-ACCELERATION",
        ],
    },
    "fixed_point_defect": (
        "the Ganlib-only post-minus-pre stationary production-map "
        "fixed-point defect is not an independently assembled A*phi-q "
        "equation residual, a transport error bound, or a convergence "
        "proof; a NATIVE strict exit before IEXTF 4 is inconclusive "
        "because no outer accelerated step occurred"
    ),
    "threshold": None,
    "aggregation": None,
    "relaxation": None,
    "fitting": None,
    "causal_claim": None,
    "stage4_status": "INVALID",
    "stage5_status": "NOT-AUTHORIZED",
    "outer_convergence": "NOT-EVALUATED",
}


def fail(message: str) -> None:
    raise SystemExit("RADIAL-FLOOR STATUS FAIL: " + message)


def as_float(token: str, description: str) -> float:
    try:
        value = float(token.replace("D", "E").replace("d", "e"))
    except ValueError:
        fail(f"{description} is not a number")
    if not math.isfinite(value):
        fail(f"{description} is not finite")
    return value


def f32_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


@dataclass(frozen=True)
class TerminalOuter:
    kind: str
    iextf: int
    maxout: int
    keff: float
    eext: float
    epsout: float
    eunk: float
    epsunk: float
    eunk_valid: int
    position: int


@dataclass(frozen=True)
class TerminalInner:
    kind: str
    iterf: int
    maxinr: int
    einr: float
    epsinr: float
    igdeb: int
    state: int
    ngrp: int
    position: int


@dataclass(frozen=True)
class Iteration:
    kind: str
    index: int
    change: float
    target: float
    zmu: float
    igdeb: int | None
    position: int


@dataclass(frozen=True)
class ParsedRun:
    role: str
    arm_id: str
    free_steps: int
    accelerated_steps: int
    outer: TerminalOuter
    inner: TerminalInner
    inner_iterations: tuple[Iteration, ...]
    outer_iterations: tuple[Iteration, ...]
    state: str


OUTER_TERMINAL_RE = re.compile(
    rf"^[ \t]*FLU2DR-(TERM|DIAG) "
    rf"(?:OUTER-GATE=PASS|OUTER) "
    rf"IEXTF=[ \t]*(\d+) MAXOUT=[ \t]*(\d+) "
    rf"KEFF=[ \t]*({NUMBER}) EEXT=[ \t]*({NUMBER}) "
    rf"EPSOUT=[ \t]*({NUMBER}) EUNK=[ \t]*({NUMBER}) "
    rf"EPSUNK=[ \t]*({NUMBER}) EUNK-VALID=(\d+)[ \t]*$",
    re.MULTILINE,
)
INNER_TERMINAL_RE = re.compile(
    rf"^[ \t]*FLU2DR-(TERM|DIAG) "
    rf"(?:INNER-TERMINAL|INNER) "
    rf"ITERF=[ \t]*(\d+) MAXINR=[ \t]*(\d+) "
    rf"EINR=[ \t]*({NUMBER}) EPSINR=[ \t]*({NUMBER}) "
    rf"IGDEB=[ \t]*(\d+) STATE=(\d+) NGRP=[ \t]*(\d+)[ \t]*$",
    re.MULTILINE,
)
INNER_ITER_RE = re.compile(
    rf"^[ \t]*IN\([ \t]*(\d+)\)[ \t]+FLX:"
    rf"[ \t]*PRC=[ \t]*({NUMBER})[ \t]+TAR=[ \t]*({NUMBER})"
    rf"[ \t]+IGDEB=[ \t]*(\d+)[ \t]+ACCE=[ \t]*({NUMBER})[ \t]*$",
    re.MULTILINE,
)
OUTER_ITER_RE = re.compile(
    rf"^[ \t]*OUT\([ \t]*(\d+)\)[ \t]+FLX:"
    rf"[ \t]*PRC=[ \t]*({NUMBER})[ \t]+TAR=[ \t]*({NUMBER})"
    rf"[ \t]+FNOR=[ \t]*({NUMBER})[ \t]+ACCE=[ \t]*({NUMBER})[ \t]*$",
    re.MULTILINE,
)
ECHO_RE = re.compile(r"^[ \t]*>\|(.*?)\|>\d+[ \t]*$", re.MULTILINE)


def one_match(
    pattern: re.Pattern[str],
    text: str,
    description: str,
) -> re.Match[str]:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        fail(f"{description}: expected one record, found {len(matches)}")
    return matches[0]


def parse_terminal_outer(text: str, description: str) -> TerminalOuter:
    match = one_match(OUTER_TERMINAL_RE, text, description + " outer")
    kind = match.group(1)
    line = match.group(0)
    if kind == "TERM" and "OUTER-GATE=PASS" not in line:
        fail(f"{description} TERM record lacks OUTER-GATE=PASS")
    if kind == "DIAG" and "OUTER-GATE=PASS" in line:
        fail(f"{description} DIAG record carries a PASS label")
    return TerminalOuter(
        kind=kind,
        iextf=int(match.group(2)),
        maxout=int(match.group(3)),
        keff=as_float(match.group(4), description + " KEFF"),
        eext=as_float(match.group(5), description + " EEXT"),
        epsout=as_float(match.group(6), description + " EPSOUT"),
        eunk=as_float(match.group(7), description + " EUNK"),
        epsunk=as_float(match.group(8), description + " EPSUNK"),
        eunk_valid=int(match.group(9)),
        position=match.start(),
    )


def parse_terminal_inner(text: str, description: str) -> TerminalInner:
    match = one_match(INNER_TERMINAL_RE, text, description + " inner")
    kind = match.group(1)
    line = match.group(0)
    if kind == "TERM" and "INNER-TERMINAL" not in line:
        fail(f"{description} TERM record lacks INNER-TERMINAL")
    if kind == "DIAG" and "INNER-TERMINAL" in line:
        fail(f"{description} DIAG record carries a terminal label")
    return TerminalInner(
        kind=kind,
        iterf=int(match.group(2)),
        maxinr=int(match.group(3)),
        einr=as_float(match.group(4), description + " EINR"),
        epsinr=as_float(match.group(5), description + " EPSINR"),
        igdeb=int(match.group(6)),
        state=int(match.group(7)),
        ngrp=int(match.group(8)),
        position=match.start(),
    )


def parse_iterations(text: str, description: str) -> tuple[Iteration, ...]:
    records: list[Iteration] = []
    for match in INNER_ITER_RE.finditer(text):
        records.append(
            Iteration(
                kind="INNER",
                index=int(match.group(1)),
                change=as_float(match.group(2), description + " inner PRC"),
                target=as_float(match.group(3), description + " inner TAR"),
                igdeb=int(match.group(4)),
                zmu=as_float(match.group(5), description + " inner ACCE"),
                position=match.start(),
            )
        )
    for match in OUTER_ITER_RE.finditer(text):
        fnor = as_float(match.group(4), description + " outer FNOR")
        if fnor <= 0.0:
            fail(f"{description} outer FNOR is not positive")
        records.append(
            Iteration(
                kind="OUTER",
                index=int(match.group(1)),
                change=as_float(match.group(2), description + " outer PRC"),
                target=as_float(match.group(3), description + " outer TAR"),
                igdeb=None,
                zmu=as_float(match.group(5), description + " outer ACCE"),
                position=match.start(),
            )
        )
    records.sort(key=lambda record: record.position)
    if not records:
        fail(f"{description} has no printed IN/OUT iteration history")
    return tuple(records)


def parse_controls(
    payload: str,
    marker: str,
    description: str,
) -> tuple[int, int, float, int, int]:
    fields = payload.split()
    if len(fields) != 6 or fields[0] != marker:
        fail(f"{description} has malformed controls marker")
    try:
        maxout = int(fields[1])
        maxinr = int(fields[2])
        free_steps = int(fields[4])
        accelerated_steps = int(fields[5])
    except ValueError:
        fail(f"{description} controls contain a non-integer field")
    eps = as_float(fields[3], description + " marker epsilon")
    return maxout, maxinr, eps, free_steps, accelerated_steps


def validate_log_envelope(text: str, description: str) -> None:
    if text.count("normal end of execution for dragon") != 1:
        fail(f"{description} lacks one normal Dragon termination")
    if len(re.findall(r"cle2000_c:\s*cpu time=", text)) != 1:
        fail(f"{description} lacks one CLE-2000 CPU receipt")
    for pattern, label in (
        (r"\bXABORT\b", "XABORT"),
        (r"segmentation fault", "segmentation fault"),
        (r"\b(?:NaN|Inf(?:inity)?)\b", "non-finite text"),
        (r"\bSTAGE4\s+QUALIFIED\b", "Stage-4 qualification claim"),
        (r"\bSTAGE5\s+AUTHORIZED\b", "Stage-5 authorization claim"),
        (
            r"\bOUTER-CONVERGENCE\s+(?:PASS|CONVERGED)\b",
            "outer-convergence claim",
        ),
        (r"A\s*\*?\s*PHI\s*-\s*Q\s+RESIDUAL", "A*phi-q residual claim"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            fail(f"{description} contains unauthorized {label}")
    header_patterns = (
        r"FLUX SOLUTION DOOR[ \t]*=[ \t]*\*\*[ \t]*MCCG[ \t]*\*\*",
        r"NB\. OF GROUPS[ \t]*=[ \t]*370\b",
        r"REBALANCING OPTION[ \t]*=[ \t]*ON\b",
        r"CALCULATION TYPE[ \t]*=[ \t]*SOURCE\b",
    )
    for pattern in header_patterns:
        if len(re.findall(pattern, text)) != 1:
            fail(f"{description} lacks one production header: {pattern}")


def validate_history(
    iterations: tuple[Iteration, ...],
    terminal: TerminalInner,
    iextf: int,
    free_steps: int,
    accelerated_steps: int,
    description: str,
) -> tuple[tuple[Iteration, ...], tuple[Iteration, ...]]:
    inner_records: list[Iteration] = []
    outer_records: list[Iteration] = []
    segment: list[Iteration] = []
    expected_outer = 1
    for record in iterations:
        if record.change < 0.0:
            fail(f"{description} has a negative printed change")
        if f32_bits(record.target) != EPS_BITS:
            fail(f"{description} has a printed target other than h/2")
        if record.kind == "INNER":
            expected_inner = len(segment) + 1
            if record.index != expected_inner:
                fail(
                    f"{description} inner history is not 1..N inside "
                    f"outer step {expected_outer}"
                )
            if not 1 <= record.igdeb <= 371:
                fail(f"{description} has invalid printed IGDEB")
            if record.index > 740:
                fail(f"{description} exceeds MAXINR=740")
            segment.append(record)
            inner_records.append(record)
            continue
        if record.index != expected_outer:
            fail(f"{description} outer history is not exactly 1..IEXTF")
        if not segment:
            fail(f"{description} outer step has no printed inner history")
        outer_records.append(record)
        segment = []
        expected_outer += 1
    if segment:
        fail(f"{description} has inner history after its final OUT record")
    if len(outer_records) != iextf:
        fail(
            f"{description} prints {len(outer_records)} outer steps "
            f"but terminal IEXTF={iextf}"
        )
    # The last event is an OUT record, so count the final segment directly.
    final_outer_position = outer_records[-2].position if iextf > 1 else -1
    final_segment = [
        record
        for record in inner_records
        if final_outer_position < record.position < outer_records[-1].position
    ]
    if not final_segment or final_segment[-1].index != terminal.iterf:
        fail(f"{description} terminal ITERF does not match final history")

    stationary = accelerated_steps == 0
    cycle_length = free_steps + accelerated_steps
    for record in iterations:
        in_free_phase = (
            (record.index - 1) % cycle_length < free_steps
        )
        if (stationary or in_free_phase) and record.zmu != 1.0:
            fail(
                f"{description} has non-unit ACCE during a free or "
                "stationary iteration"
            )
    return tuple(inner_records), tuple(outer_records)


def validate_terminal_common(
    outer: TerminalOuter,
    inner: TerminalInner,
    maxout: int,
    description: str,
) -> None:
    if outer.position >= inner.position:
        fail(f"{description} inner terminal precedes outer terminal")
    if outer.maxout != maxout or inner.maxinr != 740:
        fail(f"{description} terminal controls differ from the protocol")
    if outer.eunk_valid != 1:
        fail(f"{description} does not contain a valid EUNK")
    if outer.keff != 1.0 or outer.eext != 0.0:
        fail(f"{description} is not a nonmultiplying fixed-source solve")
    if (
        outer.eunk < 0.0
        or inner.einr < 0.0
        or f32_bits(outer.epsout) != EPS_BITS
        or f32_bits(outer.epsunk) != EPS_BITS
        or f32_bits(inner.epsinr) != EPS_BITS
    ):
        fail(f"{description} terminal residual fields are invalid")
    if inner.ngrp != 370 or not 1 <= inner.igdeb <= 371:
        fail(f"{description} terminal group state is invalid")
    if inner.state not in (1, 2, 3):
        fail(f"{description} terminal inner STATE is invalid")


def strict_gate(outer: TerminalOuter, inner: TerminalInner) -> bool:
    return (
        outer.eext < outer.epsout
        and outer.eunk < outer.epsunk
        and inner.einr < inner.epsinr
        and inner.state == 1
        and inner.igdeb == 371
        and outer.iextf >= 2
    )


def parse_run(
    path: Path,
    role: str,
    arm_id: str,
    expected_free: int,
    expected_accelerated: int,
) -> ParsedRun:
    raw = path.read_bytes()
    if not raw or b"\0" in raw:
        fail(f"{path.name} is empty or contains NUL bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path.name} is not strict UTF-8/ASCII: {exc}")
    description = f"{role.lower()} {arm_id}"
    validate_log_envelope(text, description)

    marker_prefix = f"RADIAL-FLOOR-{role}"
    echo_matches = [
        match
        for match in ECHO_RE.finditer(text)
        if match.group(1).lstrip().startswith("RADIAL-FLOOR-")
    ]
    echoes = [match.group(1).rstrip() for match in echo_matches]
    if role == "ARM":
        marker_names = [
            f"{marker_prefix}-BEGIN",
            f"{marker_prefix}-HISTORY",
            f"{marker_prefix}-CONTROLS",
            f"{marker_prefix}-COMPLETE",
        ]
    else:
        marker_names = [
            f"{marker_prefix}-BEGIN",
            f"{marker_prefix}-HISTORY",
            f"{marker_prefix}-CONTROLS",
            f"{marker_prefix}-COMPLETE",
        ]
    if len(echoes) != len(marker_names):
        fail(
            f"{description} expected {len(marker_names)} diagnostic "
            f"markers, found {len(echoes)}"
        )
    for payload, marker in zip(echoes, marker_names, strict=True):
        if not payload.startswith(marker):
            fail(f"{description} markers are missing, extra, or reordered")
    if echoes[0] != f"{marker_prefix}-BEGIN {arm_id}":
        fail(f"{description} has an invalid begin marker")
    if echoes[1] != f"{marker_prefix}-HISTORY RESET":
        fail(f"{description} does not declare a fresh cycle-history reset")
    if echoes[-1] != f"{marker_prefix}-COMPLETE {arm_id}":
        fail(f"{description} has an invalid completion marker")

    controls_index = 2
    controls = parse_controls(
        echoes[controls_index],
        f"{marker_prefix}-CONTROLS",
        description,
    )
    expected_maxout = 6 if role == "ARM" else 1
    if controls != (
        expected_maxout,
        740,
        controls[2],
        expected_free,
        expected_accelerated,
    ) or f32_bits(controls[2]) != EPS_BITS:
        fail(f"{description} marker controls differ from the protocol")

    header = re.findall(
        r"MAX\. OUTER ITERATIONS[ \t]*=[ \t]*(\d+).*?"
        r"MAX\. THERMAL ITERATIONS[ \t]*=[ \t]*(\d+).*?"
        r"ACCELERATION SCHEME[ \t]*=\([ \t]*(\d+)[ \t]+FREE,"
        r"[ \t]*(\d+)[ \t]+ACCELERATED\)",
        text,
        re.DOTALL,
    )
    if header != [
        (
            str(expected_maxout),
            "740",
            str(expected_free),
            str(expected_accelerated),
        )
    ]:
        fail(f"{description} FLU header controls differ from its markers")

    outer = parse_terminal_outer(text, description)
    inner = parse_terminal_inner(text, description)
    validate_terminal_common(outer, inner, expected_maxout, description)
    iterations = parse_iterations(text, description)
    controls_position = echo_matches[controls_index].start()
    complete_position = echo_matches[-1].start()
    if not (
        controls_position
        < min(record.position for record in iterations)
        < max(record.position for record in iterations)
        < outer.position
        < inner.position
        < complete_position
        < text.index("normal end of execution for dragon")
    ):
        fail(
            f"{description} marker, history, terminal, or normal-end "
            "records are reordered"
        )
    inner_history, outer_history = validate_history(
        iterations,
        inner,
        outer.iextf,
        expected_free,
        expected_accelerated,
        description,
    )
    warning_count = len(
        re.findall(
            r"^\s*\*\*\* FLU2DR: CONVERGENCE NOT REACHED \*\*\*\s*$",
            text,
            re.MULTILINE,
        )
    )

    if role == "ARM":
        if outer.kind == "TERM" and inner.kind == "TERM":
            if not 2 <= outer.iextf <= 6 or not strict_gate(outer, inner):
                fail(f"{description} has a false strict terminal")
            if warning_count != 0:
                fail(f"{description} strict exit carries failure warnings")
            state = "STRICT"
        elif outer.kind == "DIAG" and inner.kind == "DIAG":
            if outer.iextf != 6 or strict_gate(outer, inner):
                fail(f"{description} is not a genuine six-step cap")
            if warning_count != 3:
                fail(f"{description} cap lacks exactly three FLU warnings")
            state = "CAP"
        else:
            fail(f"{description} mixes TERM and DIAG terminal records")
    else:
        if (
            outer.kind != "DIAG"
            or inner.kind != "DIAG"
            or outer.iextf != 1
            or warning_count != 3
        ):
            fail(f"{description} is not the required one-step probe cap")
        state = "ONE-STEP-DIAGNOSTIC"

    return ParsedRun(
        role=role,
        arm_id=arm_id,
        free_steps=expected_free,
        accelerated_steps=expected_accelerated,
        outer=outer,
        inner=inner,
        inner_iterations=inner_history,
        outer_iterations=outer_history,
        state=state,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("native_arm_log", type=Path)
    parser.add_argument("stationary_arm_log", type=Path)
    parser.add_argument("native_probe_log", type=Path)
    parser.add_argument("stationary_probe_log", type=Path)
    parser.add_argument("protocol", type=Path)
    args = parser.parse_args()

    try:
        protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read protocol: {exc}")
    if protocol != EXPECTED_PROTOCOL:
        fail("protocol differs from the frozen radial-floor contract")

    native = parse_run(
        args.native_arm_log, "ARM", "NATIVE", 3, 3
    )
    stationary = parse_run(
        args.stationary_arm_log, "ARM", "STATIONARY", 1, 0
    )
    native_probe = parse_run(
        args.native_probe_log, "PROBE", "NATIVE", 1, 0
    )
    stationary_probe = parse_run(
        args.stationary_probe_log, "PROBE", "STATIONARY", 1, 0
    )
    strict_ids = {
        run.arm_id for run in (native, stationary) if run.state == "STRICT"
    }
    if native.state == "STRICT" and native.outer.iextf < 4:
        comparison = "INCONCLUSIVE-NO-OUTER-ACCELERATION"
    else:
        comparison = {
            frozenset(ARM_IDS): "BOTH-STRICT",
            frozenset(("NATIVE",)): "NATIVE-ONLY-STRICT",
            frozenset(("STATIONARY",)): "STATIONARY-ONLY-STRICT",
            frozenset(): "BOTH-CAP",
        }[frozenset(strict_ids)]

    print("RADIAL-FLOOR CAPTURE VALID-DIAGNOSTIC")
    for run in (native, stationary):
        print(
            f"RADIAL-FLOOR STATUS ARM {run.arm_id} {run.state} "
            f"IEXTF={run.outer.iextf} "
            f"INNER-RECORDS={len(run.inner_iterations)} "
            f"OUTER-RECORDS={len(run.outer_iterations)}"
        )
    for run in (native_probe, stationary_probe):
        print(
            f"RADIAL-FLOOR STATUS PROBE {run.arm_id} "
            "ONE-STEP-DIAGNOSTIC IEXTF=1"
        )
    print(f"RADIAL-FLOOR STATUS COMPARISON {comparison}")
    print(
        "RADIAL-FLOOR STATUS FIXED-POINT-DEFECT "
        "NOT-A-PHI-MINUS-Q-RESIDUAL"
    )
    print("RADIAL-FLOOR STATUS THRESHOLD NONE")
    print("RADIAL-FLOOR STATUS STAGE4 INVALID")
    print("RADIAL-FLOOR STATUS STAGE5 NOT-AUTHORIZED")
    print("RADIAL-FLOOR STATUS OUTER-CONVERGENCE NOT-EVALUATED")
    print("RADIAL-FLOOR STATUS COMPLETE")


if __name__ == "__main__":
    main()

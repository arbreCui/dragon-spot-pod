#!/usr/bin/env python3
"""Classify Stage-4 scale ordering without an empirical threshold."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re


NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
COMPONENTS = ("RRHO", "RLEAK", "DLEAK", "RA")


def fail(message: str) -> None:
    raise SystemExit("INNER-SENSITIVITY STATUS FAIL: " + message)


def relation(left: float, right: float) -> str:
    if left < right:
        return "LESS"
    if left > right:
        return "GREATER"
    return "EQUAL"


def parse_vector(line: str, label: str) -> tuple[float, ...]:
    match = re.fullmatch(
        rf"{re.escape(label)}(?:\s+({NUMBER}))"
        rf"(?:\s+({NUMBER}))(?:\s+({NUMBER}))(?:\s+({NUMBER}))",
        line,
    )
    if match is None:
        fail(f"invalid {label} row")
    values = tuple(
        float(token.replace("D", "E").replace("d", "e"))
        for token in match.groups()
    )
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        fail(f"{label} contains a non-finite or negative value")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("checker_log", type=Path)
    parser.add_argument("protocol", type=Path)
    parser.add_argument(
        "--replay",
        action="store_true",
        help="the strict five-file h/2 replay manifest has passed",
    )
    args = parser.parse_args()

    raw = args.checker_log.read_bytes()
    if not raw or b"\0" in raw:
        fail("checker log is empty or contains NUL bytes")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"checker log is not strict UTF-8/ASCII: {exc}")
    if len(lines) != 12:
        fail(f"expected exactly 12 checker rows, found {len(lines)}")

    expected_prefix = [
        "INNER-SENSITIVITY X0 CANONICAL BITWISE IDENTICAL",
        "INNER-SENSITIVITY TRIAL-SPACE BITWISE IDENTICAL",
        "INNER-SENSITIVITY RADIAL-INPUTS BITWISE IDENTICAL",
        "INNER-SENSITIVITY ORDER RRHO RLEAK DLEAK RA",
    ]
    if lines[:4] != expected_prefix:
        fail("checker evidence prefix differs from the frozen schema")
    if lines[11] != "INNER-SENSITIVITY COMPLETE":
        fail("checker completion row is missing")

    dout_h = parse_vector(lines[4], "INNER-SENSITIVITY DOUT-H")
    dout_h2 = parse_vector(lines[5], "INNER-SENSITIVITY DOUT-H2")
    din = parse_vector(lines[6], "INNER-SENSITIVITY DIN")

    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    if (
        protocol.get("schema") != "spot-inner-sensitivity-v1"
        or protocol.get("components") != ["R_rho", "R_L", "D_L", "R_a"]
        or protocol.get("component_rule")
        != {
            "positive_outer": "RESOLVED iff D_in < D_out_h",
            "zero_outer": "RESOLVED iff D_in == 0 at stored precision",
            "otherwise": "UNRESOLVED",
        }
        or protocol.get("h2_replay")
        != "required before final Stage-4 qualification"
        or protocol.get("stage4_state_rule")
        != {
            "any_component_unresolved": "UNRESOLVED",
            "all_components_resolved_without_h2_replay": "PENDING-REPLAY",
            "all_components_resolved_with_h2_replay": "QUALIFIED",
        }
        or protocol.get("outer_convergence") != "not_evaluated"
    ):
        fail("protocol does not contain the frozen classification contract")

    statuses: list[str] = []
    for index, component in enumerate(COMPONENTS):
        expected_h = relation(din[index], dout_h[index])
        expected_h2 = relation(din[index], dout_h2[index])
        expected_line = (
            f"INNER-SENSITIVITY COMPONENT {component} "
            f"DIN-VS-DOUT-H {expected_h} "
            f"DIN-VS-DOUT-H2 {expected_h2}"
        )
        if lines[7 + index] != expected_line:
            fail(f"{component} relation row differs from numeric ordering")

        if dout_h[index] > 0.0:
            status = "RESOLVED" if din[index] < dout_h[index] else "UNRESOLVED"
        else:
            status = "RESOLVED" if din[index] == 0.0 else "UNRESOLVED"
        statuses.append(status)
        print(
            "INNER-SENSITIVITY STATUS COMPONENT "
            f"{component} {status}"
        )

    all_resolved = all(status == "RESOLVED" for status in statuses)
    if not all_resolved:
        stage4 = "UNRESOLVED"
    elif args.replay:
        stage4 = "QUALIFIED"
    else:
        stage4 = "PENDING-REPLAY"

    print("INNER-SENSITIVITY STATUS OUTER-CONVERGENCE NOT-EVALUATED")
    print(f"INNER-SENSITIVITY STATUS STAGE4 {stage4}")
    print(
        "INNER-SENSITIVITY STATUS STAGE5 "
        + ("AUTHORIZED" if stage4 == "QUALIFIED" else "NOT-AUTHORIZED")
    )
    print("INNER-SENSITIVITY STATUS COMPLETE")


if __name__ == "__main__":
    main()

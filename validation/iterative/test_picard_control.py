#!/usr/bin/env python3
"""Seconds-scale tests for direct SPOT Picard control."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class State:
    a: tuple[float, ...]
    rho: float
    leakage: tuple[float, ...]


@dataclass(frozen=True)
class Defects:
    rho: float
    leakage: float
    coordinates: float


def defects(current: State, previous: State) -> Defects:
    delta = tuple(
        left - right for left, right in zip(current.a, previous.a, strict=True)
    )
    denominator = sum(value * value for value in current.a)
    if denominator <= 0.0:
        raise ValueError("nonpositive coordinate norm")
    leakage_delta = max(
        abs(left - right)
        for left, right in zip(current.leakage, previous.leakage, strict=True)
    )
    leakage_scale = max(
        max(map(abs, current.leakage)), max(map(abs, previous.leakage))
    )
    leakage_defect = (
        0.0 if leakage_scale == 0.0 else leakage_delta / leakage_scale
    )
    return Defects(
        rho=abs(current.rho - previous.rho),
        leakage=leakage_defect,
        coordinates=math.sqrt(sum(value * value for value in delta) / denominator),
    )


def direct_picard(initial, map_function, max_iterations, tolerance):
    if max_iterations <= 0 or tolerance < 0.0:
        raise ValueError("invalid Picard control")
    trace = [initial]
    current = initial
    last_defects = None
    for _ in range(max_iterations):
        candidate = map_function(current)
        last_defects = defects(candidate, current)
        trace.append(candidate)
        current = candidate
        if all(
            value <= tolerance
            for value in (
                last_defects.rho,
                last_defects.leakage,
                last_defects.coordinates,
            )
        ):
            return trace, last_defects, True
    return trace, last_defects, False


class PicardControlTests(unittest.TestCase):
    def test_direct_trace_and_three_component_stop(self) -> None:
        calls = 0

        def manufactured(state: State) -> State:
            nonlocal calls
            calls += 1
            return State(
                a=(state.a[1], 2.0),
                rho=1.0,
                leakage=(state.leakage[1], 0.0),
            )

        x0 = State(a=(0.0, 1.0), rho=2.0, leakage=(1.0, 1.0))
        x1 = State(a=(1.0, 2.0), rho=1.0, leakage=(1.0, 0.0))
        x2 = State(a=(2.0, 2.0), rho=1.0, leakage=(0.0, 0.0))
        trace, residual, converged = direct_picard(x0, manufactured, 8, 0.0)

        self.assertEqual(trace, [x0, x1, x2, x2])
        self.assertEqual(calls, 3)
        self.assertTrue(converged)
        self.assertEqual(residual, Defects(0.0, 0.0, 0.0))
        second = defects(x2, x1)
        self.assertEqual(second.rho, 0.0)
        self.assertGreater(second.leakage, 0.0)
        self.assertGreater(second.coordinates, 0.0)

    def test_iteration_limit_returns_not_converged(self) -> None:
        calls = 0

        def translating(state: State) -> State:
            nonlocal calls
            calls += 1
            return State(
                a=(state.a[0] + 1.0, state.a[1]),
                rho=state.rho + 1.0,
                leakage=(state.leakage[0] + 1.0, state.leakage[1]),
            )

        initial = State(a=(1.0, 1.0), rho=1.0, leakage=(1.0, 0.0))
        trace, _, converged = direct_picard(initial, translating, 2, 0.0)
        self.assertFalse(converged)
        self.assertEqual(calls, 2)
        self.assertEqual(trace[-1], State((3.0, 1.0), 3.0, (3.0, 0.0)))

    def test_production_procedure_is_direct_and_unmixed(self) -> None:
        text = (ROOT / "data/SpotPicard.c2m").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", text.upper())
        for token in (
            "SPOPROJ: SNAP AX TRACK_AX :: FIXB",
            "SPOTREFFS SNAP TRACK TRACK_F",
            "SPOD <<RANK>> FIXB",
            "AX_NEXT := SPOSTATE:",
            "AX_NEXT := SPOGBAL: AX_NEXT TRACK_AX SYSTEM_NEXT MACROLIB3 ::",
            "AX_NEXT := SPOXCONV: AX_NEXT AX",
            "SNAP := SPOLEAK: SNAP AX_NEXT TRACK_AX",
            "AX := AX_NEXT",
        ):
            self.assertIn(token, compact)
        self.assertIn(
            "RRHO OUTER_EPS <= RLEAK OUTER_EPS <= * RA OUTER_EPS <= *",
            compact,
        )
        self.assertEqual(compact.count("REPEAT"), 1)
        self.assertEqual(compact.count("UNTIL"), 1)
        self.assertEqual(compact.count("AX_NEXT := SPOGBAL:"), 1)
        self.assertLess(
            compact.index("AX_NEXT := FLU:"),
            compact.index("AX_NEXT := SPOGBAL:"),
        )
        self.assertLess(
            compact.index("AX_NEXT := SPOGBAL:"),
            compact.index("AX_NEXT := SPOSTATE:"),
        )
        for forbidden in (" RELA ", " ALPHA ", " ANDERSON ", " CMFD ", " CLIP "):
            self.assertNotIn(forbidden, compact)

if __name__ == "__main__":
    unittest.main()

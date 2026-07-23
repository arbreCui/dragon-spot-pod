#!/usr/bin/env python3
"""Static contract for the first corrected fixed-space map deck."""

from __future__ import annotations

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
deck_path = root / "validation/iterative/one_corrected_map.x2m"
deck = deck_path.read_text(errors="strict")
violations: list[str] = []


def require(pattern: str, description: str) -> None:
    if re.search(pattern, deck, re.IGNORECASE | re.DOTALL) is None:
        violations.append("missing " + description)


require(
    r"BASIS_REF\s*:=\s*ASM:.*?SPOD\s*<<spod_rank>>\s*;",
    "single offline basis construction",
)
require(
    r"AX_PREVIOUS\s*:=\s*SPOSTATE:.*?BASIS_REF\s+MACROLIB3",
    "canonical initial state",
)
require(
    r"SNAP\s*:=\s*SPOLEAK:\s*SNAP\s+AX_PREVIOUS\s+TRACK_AX",
    "undamped initial leakage return",
)
require(
    r"SNAP\s*:=\s*SPOPROJ:.*?AX_PREVIOUS.*?::\s*FIXB\s*;",
    "explicit B*a feedback reconstruction",
)
require(
    r"SNAP\s*:=\s*SpotRefFS.*?<<k0>>\s*<<solver_eps>>",
    "online frozen-fission radial solves",
)
require(
    r"SYSTEM_NEXT\s*:=\s*ASM:.*?SNAP\s+BASIS_REF.*?SPOD.*?FIXB",
    "live radial response with fixed basis",
)
require(
    r"AX_CURRENT\s*:=\s*SPOSTATE:.*?SYSTEM_NEXT\s+MACROLIB3",
    "canonical returned state",
)
if len(
    re.findall(
        r":=\s*SPOGBAL:.*?\s+MACROLIB3\s*::\s*;",
        deck,
        re.IGNORECASE | re.DOTALL,
    )
) != 2:
    violations.append("both axial balance audits must receive MACROLIB3")
require(
    r"AX_CURRENT\s*:=\s*SPOXCONV:\s*AX_CURRENT\s+AX_PREVIOUS",
    "raw map defect at x0",
)
require(
    r"ITERATIVE-MAP-RAW-DEFECT-X0",
    "unambiguous defect marker",
)

if len(re.findall(r":=\s*FLU:", deck)) != 2:
    violations.append("deck must contain one initializer and one returned axial solve")
if len(re.findall(r"SNAP\s*:=\s*SpotRefFS\b", deck)) != 1:
    violations.append("deck must contain exactly one online radial map")
active_deck = "\n".join(
    line for line in deck.splitlines() if not line.lstrip().startswith("*")
)
if re.search(
    r"\bWHILE\b|\bRELA(?:X|XATION)?\b|\bCMFD\b|\bALPHA\b",
    active_deck,
    re.I,
):
    violations.append("deck contains iteration, relaxation, or empirical stabilization")

declared = re.findall(
    r"^\s*(?:INTEGER|REAL|DOUBLE|LINKED_LIST|XSM_FILE|SEQ_BINARY)\s+"
    r"([^;:]+)",
    deck,
    re.MULTILINE,
)
for declaration in declared:
    for name in re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", declaration):
        if len(name) > 12:
            violations.append(f"CLE-2000 identifier exceeds 12 characters: {name}")

if violations:
    raise SystemExit("ONE-MAP CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "ONE-MAP CONTRACT PASS: one initializer plus one raw fixed-B Picard map; "
    "online radial solves and leakage feedback are present, with no relaxation "
    "or empirical model factor."
)

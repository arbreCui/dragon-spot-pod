#!/usr/bin/env python3
"""Static contract for the published fixed-space iterative SPOT method."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

required_tokens = {
    "validation/iterative/one_corrected_map.x2m": (
        "SPOPROJ:",
        "FIXB",
        "SpotRefFS",
        "SPOXCONV:",
        "SPOLEAK:",
    ),
    "data/SpotPlaneFS.c2m": (
        "SPOFSRC:",
        "TYPE S",
        "SPOFCHK:",
    ),
    "data/SpotRefFS.c2m": (
        "SpotPlaneFS",
        "FLUX_OLD",
    ),
    "src/SPOASM.f": (
        "SPOT-QFISS",
        "CALL SPOQFS",
        "RADIAL-OP",
    ),
    "src/SPOPROJ.f90": (
        "FIXB",
        "SPOT-X-BASIS",
    ),
    "src/SPOSTATE.f90": (
        "SPOT-X-A",
        "SPOT-X-RHO",
        "SPOT-X-L",
    ),
    "src/SPOXCONV.f90": (
        "SPOT-X-RRHO",
        "SPOT-X-RLEAK",
        "SPOT-X-RA",
    ),
}

violations: list[str] = []
texts: dict[str, str] = {}
for relative, tokens in required_tokens.items():
    path = ROOT / relative
    if not path.is_file():
        violations.append(f"{relative}: missing")
        continue
    text = path.read_text(errors="replace")
    texts[relative] = text
    for token in tokens:
        if token not in text:
            violations.append(f"{relative}: missing {token!r}")

map_text = texts.get("validation/iterative/one_corrected_map.x2m", "")
if map_text.count("SpotRefFS SNAP TRACK TRACK_f") != 1:
    violations.append("one_corrected_map.x2m: expected one radial refresh")
if map_text.count("SPOPROJ: SNAP AX_PREVIOUS TRACK_AX :: FIXB") != 1:
    violations.append("one_corrected_map.x2m: feedback is not explicitly B*a")
if re.search(r"\b(?:WHILE|REPEAT)\b", map_text, re.IGNORECASE):
    violations.append("one_corrected_map.x2m: one-map fixture contains a loop")

formal_inputs = (
    "validation/iterative/one_corrected_map.x2m",
    "data/SpotPlaneFS.c2m",
    "data/SpotRefFS.c2m",
)
for relative in formal_inputs:
    text = texts.get(relative, "")
    for pattern, description in (
        (r"\bRELA\b", "adjustable relaxation"),
        (r"\bANDERSON\b", "nonlinear mixing"),
        (r"\bCMFD\b", "extra closure model"),
        (r"\bFLU_FLOOR\b", "flux floor"),
        (r"\bSVDE\b", "fitted POD cutoff"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(f"{relative}: contains {description}")

if violations:
    raise SystemExit("METHOD CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "METHOD CONTRACT PASS: one fixed-space Galerkin-SPOD map has online "
    "radial fixed-source solves, direct leakage feedback, a complete raw "
    "state defect, and no empirical stabilization parameter."
)

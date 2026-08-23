#!/usr/bin/env python3
"""Static contract for the published fixed-space iterative SPOT method."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

required_tokens = {
    "data/SpotPicard.c2m": (
        "SPOPROJ:",
        "FIXB",
        "SpotRefFS",
        "SPOGBAL:",
        "SPOSTATE:",
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
    "data/SpotStepR64.c2m": (
        "SYSTEM1 := ASM:",
        "SYSTEM2 := ASM:",
        "SYSTEM3 := ASM:",
        "RETURNED := SPOR64T:",
    ),
    "validation/iterative/rank2_h2_r64_aa1_x4_radial.x2m": (
        "PROCEDURE SpotStepR64",
        "INTEGER spod_rank := 2 ;",
        "SPOD <<spod_rank>> FIXB",
    ),
    "validation/iterative/rank2_h2_r64_aa1_x4_axial.x2m": (
        "REAL solver_eps := 5.0E-8 ;",
        "REBA OFF ACCE 3 0",
        "SPOSTATE:",
        "SPOXCONV:",
        "SPOLEAK:",
    ),
    "src/SPOASM.f": (
        "SPOT-QFISS",
        "CALL SPOQFS",
        "RADIAL-OP",
        "LEAK1D64(IGR)",
    ),
    "src/SPOR64_B2C.f90": (
        "leak1d_input64",
        "call LCMPUT(ipflux,'LEAK1D64',NGRP,4,leak1d_input64)",
    ),
    "src/SPOR64_B2R.f90": (
        "RECORD_MATCHES(solved,'LEAK1D64',NGRP,4)",
        "SAME_REAL32_BITS(leakage,real(leakage64,real32))",
    ),
    "src/SPOR64_B2W.f90": (
        "RECORD_MATCHES(child,'LEAK1D64',NGRP,4)",
        "REAL32_PROJECTION_MATCHES(leakage32,leakage64)",
        "allow_fresh_leakage=.true.",
        "REAL32_PROJECTION_MATCHES(system_leakage32(:,ip)",
        "child_leakage64(:,ip)",
    ),
    "src/SPOR64_SCHEMA.f90": (
        "SCHEMA_SOLVED_ROOT(14)",
        "SCHEMA_RETURNED_CHILD_ROOT(17)",
    ),
    "src/SPOT_LEAKAGE.f90": (
        "double precision, intent(in) :: qfixed,phi,leak1d",
        "qfixed/phi-leak1d",
    ),
    "validation/iterative/check_one_map_xsm.f90": (
        "expected_iter_keff",
        "RADIAL L0 AUTHORITY CHANGED",
        "checked_l1_error",
    ),
    "validation/iterative/check_convergence_gate.f90": (
        "REPRESENTATION DIAGNOSTIC-NOT-GATED",
        "NOT COMPARABLE TO OUTER DEFECTS WITHOUT A COMMON NORM",
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
    "src/FLU2DR.f": (
        "CXDOOR.EQ.'MCCG'",
        "SPOT-LEAK1D",
        "SPOT-FROZEN",
        "SPOT TYPE-S STRICT TERMINATION REQUIRED",
        "SPOT TYPE-K STRICT TERMINATION REQUIRED",
    ),
    "src/FLU2DR64.f": (
        "FLU2DR64: USE REBA OFF.",
        "FLU2DR64: USE ACCE N 0.",
        "FLU2DR64: REBALANCE UNSUPPORTED.",
        "FLU2DR64: ACCELERATION UNSUPPORTED.",
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

map_text = texts.get("data/SpotPicard.c2m", "")
if map_text.count("SpotRefFS SNAP TRACK TRACK_f") != 1:
    violations.append("SpotPicard.c2m: expected one radial refresh per iteration")
if map_text.count("SPOPROJ: SNAP AX TRACK_AX :: FIXB") != 1:
    violations.append("SpotPicard.c2m: feedback is not explicitly B*a")
if len(re.findall(r"\bREPEAT\b", map_text, re.IGNORECASE)) != 1:
    violations.append("SpotPicard.c2m: expected one direct Picard loop")
if "AX := AX_NEXT" not in map_text:
    violations.append("SpotPicard.c2m: missing direct state substitution")
if not re.search(
    r"rrho\s+outer_eps\s+<=\s+rleak\s+outer_eps\s+<=\s+\*\s+"
    r"ra\s+outer_eps\s+<=\s+\*",
    map_text,
    re.IGNORECASE,
):
    violations.append("SpotPicard.c2m: three residuals are not joined by AND")

formal_inputs = (
    "data/SpotPicard.c2m",
    "data/SpotPlaneFS.c2m",
    "data/SpotRefFS.c2m",
    "data/SpotStepR64.c2m",
    "validation/iterative/rank2_h2_r64_aa1_x4_radial.x2m",
    "validation/iterative/rank2_h2_r64_aa1_x4_axial.x2m",
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

gate_checker = texts.get("validation/iterative/check_convergence_gate.f90", "")
for token in ("GATED/REPRESENTATION", "SUBSPACE-LIMITED"):
    if token in gate_checker:
        violations.append(
            "check_convergence_gate.f90: compares diagnostics with different "
            f"norms via {token!r}"
        )

if violations:
    raise SystemExit("METHOD CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "METHOD CONTRACT PASS: direct fixed-space Galerkin-SPOD Picard has "
    "online radial solves, strict inner termination, end-to-end REAL64 "
    "leakage authority, three separate raw defects, and no empirical "
    "stabilization parameter."
)

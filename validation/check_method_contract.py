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
        "RCONTRACT",
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
        "state_vector(11) = contract%flu_maxinr",
        "state_vector(12) = contract%flu_maxout",
    ),
    "src/FLU.f": (
        "RCONTRACT is a control operand",
        "CALL SPOR64_B2B_INGRESS(NENTRY-1,HENTRY(1:NENTRY-1)",
        "KENTRY(1:NENTRY-1)",
    ),
    "src/SPOR64_B2B.f90": (
        "A raw TYPE-K snapshot is admitted only as the numerical initial",
        "if (flux_state(6) /= 0 .and. flux_state(6) /= 2) return",
        "if (itypec /= 0 .or. maxout /= contract%flu_maxout",
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
        "LSTRICTK",
        "EEXT=REAL(ABS(AKEFF-AKEEP(2))/AKEFF)",
        "Accept only the unmodified Picard image",
        "SPOT TYPE-S STRICT TERMINATION REQUIRED",
        "SPOT TYPE-K STRICT TERMINATION REQUIRED",
    ),
    "src/FLU2DR64.f": (
        "FLU2DR64: USE REBA OFF.",
        "USE SPOR64_A9, ONLY: FLU2AC64",
        "FLU2DR64: INVALID ACCELERATION CYCLE.",
        "FLU2DR64: REBALANCE UNSUPPORTED.",
        "FLU2DR64: INNER FLU2AC64 FAILED.",
        "FLU2DR64: OUTER FLU2AC64 FAILED.",
        "EEXT=ABS(AKEFF-AKEEP(2))/AKEFF",
        "Only an unmodified raw Picard image may pass",
        "CALL B1HOM64",
        "CALL SPOT1P64_CACHE_BEGIN",
        "'SPOT-PHYS'",
    ),
    "src/SPOT1P64.f90": (
        "SPOT1P64_CACHE_PREPARE",
        "(.not.translation).and.diagonal_basis.and.mode_separable",
        "SPOT1P64_FACTOR64",
        "SPOT1P64_SOLVE64",
    ),
    "src/B1HOM64.f90": (
        "double precision, intent(inout) :: flux(nunkno,ngro,2)",
        "real, intent(inout) :: dhom(ngro),gamma(ngro)",
        "call B1HXS1",
        "call B1HXS2",
        "call B1DIF",
        "flux(:,i,2)=flux(:,i,2)+",
        "flux(:,i,:)=flux(:,i,:)*caet",
    ),
    "src/SPOR64_RCONTRACT.f90": (
        "if (.not. all(ieee_is_finite(eps32))) return",
        "if (any(eps32 <= 0.0_real32)) return",
        "if (len_trim(option4) == 0) return",
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

runtime_geometry_sources = (
    "src/SPOR64_A8.f90",
    "src/SPOR64_A9.f90",
    "src/SPOR64_B2B.f90",
    "src/SPOR64_B2H.f90",
    "src/SPOR64_B2I.f90",
    "src/SPOR64_B2J.f90",
    "src/SPOR64_B2K.f90",
    "src/SPOR64_B2N.f90",
    "src/SPOR64_B2R.f90",
    "src/SPOR64_B2S.f90",
    "src/SPOR64_B2W.f90",
)
for relative in runtime_geometry_sources:
    text = (ROOT / relative).read_text(errors="replace")
    for pattern, description in (
        (r"\bNREG\s*=\s*8\b", "fixed pin region count"),
        (r"\bNMAT\s*=\s*8\b", "fixed pin material count"),
        (r"\bNUNKNO\s*=\s*14\b", "fixed pin unknown count"),
        (r"\bNSOUT\s*=\s*6\b", "fixed numerical surface count"),
        (r"mccg_state\(5\)\s*/=\s*17\b", "fixed pin MXSEG"),
        (r"mccg_state\(6\)\s*/=\s*32\b", "fixed pin ACA LC"),
        (r"\[NIFIS\s*,\s*nunkno\s*,\s*NIFIS", "NIFIS used as ACA LC"),
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

r64_driver = texts.get("src/FLU2DR64.f", "")
flu_driver = texts.get("src/FLU.f", "")
if re.search(
    r"ELSE IF\(CXDOOR\.EQ\.'SPOT'\) THEN\s*"
    r"(?:\*[^\n]*\n\s*)?NLF=ISTATE\(15\)\s*"
    r"NANI=MAX\(1,ISTATE\(16\)\)\s*NANIS=MIN\(NANIS,NANI-1\)",
    flu_driver,
) is None:
    violations.append("FLU.f: SPOT angular orders must come from TRACK 15/16")
if re.search(r"CALL\s+B1HOM\s*\(", r64_driver, re.IGNORECASE):
    violations.append(
        "FLU2DR64.f: live B1 flux/source pair falls through the REAL32 B1HOM ABI"
    )
raw_gate = r64_driver.find("Only an unmodified raw Picard image may pass")
outer_acceleration = r64_driver.find(
    "CALL FLU2AC64(NGRP,NUNKNO,1,FLUX(:,:,1:3)"
)
if raw_gate < 0 or outer_acceleration < 0 or raw_gate > outer_acceleration:
    violations.append(
        "FLU2DR64.f: outer acceleration precedes the raw Picard terminal gate"
    )

legacy_driver = texts.get("src/FLU2DR.f", "")
legacy_raw_gate = legacy_driver.find("Accept only the unmodified Picard image")
legacy_outer_acceleration = legacy_driver.find(
    "CALL FLU2AC(NGRP,NUNKNO,1,FLUX(1,1,1),AKEEP(1),ZMU)"
)
if (
    legacy_raw_gate < 0
    or legacy_outer_acceleration < 0
    or legacy_raw_gate > legacy_outer_acceleration
):
    violations.append(
        "FLU2DR.f: outer acceleration precedes the raw Picard terminal gate"
    )

a9_driver = (ROOT / "src/SPOR64_A9.f90").read_text(errors="replace")
a9_raw_gate = a9_driver.find("Accept only the unmodified fixed-point image")
a9_outer_acceleration = a9_driver.find(
    "call FLU2AC64(NGRP,nunkno,1,flux64(:,:,1:3)"
)
if (
    a9_raw_gate < 0
    or a9_outer_acceleration < 0
    or a9_raw_gate > a9_outer_acceleration
):
    violations.append(
        "SPOR64_A9.f90: outer acceleration precedes the raw fixed-point gate"
    )

if violations:
    raise SystemExit("METHOD CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "METHOD CONTRACT PASS: direct fixed-space Galerkin-SPOD Picard has "
    "online radial solves, strict inner termination, end-to-end REAL64 "
    "leakage authority, three separate raw defects, and no empirical "
    "stabilization parameter."
)

#!/usr/bin/env python3
"""Static and directed checks for the scoped SPOT inner-iteration rule."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
raw = (ROOT / "src/FLU2DR.f").read_text(errors="strict")
# Fixed-form columns 1:5 are labels and column 6 is the continuation mark.
# Join only the source fields so continuation digits cannot enter a match.
fields = [
    line[6:]
    for line in raw.splitlines()
    if line and line[0] not in "cC*!" and len(line) > 6
]
flat = re.sub(r"\s+", "", "".join(fields).upper())
violations: list[str] = []

# The REAL64 flight solver owns a second, deeper terminal.  A8 must reject
# any group that remains marked unconverged after its final GMRES update.
a8_raw = (ROOT / "src/SPOR64_A8.f90").read_text(errors="strict")
a8_all_flat = re.sub(r"\s+", "", a8_raw.upper())
aca_all_flat = re.sub(
    r"\s+", "", (ROOT / "src/SPOR64_A8_ACA.f90").read_text(errors="strict").upper()
)
b2b_all_flat = re.sub(
    r"\s+", "", (ROOT / "src/SPOR64_B2B.f90").read_text(errors="strict").upper()
)
a8_match = re.search(
    r"subroutine\s+MCGMRE64\b.*?end\s+subroutine\s+MCGMRE64",
    a8_raw,
    flags=re.IGNORECASE | re.DOTALL,
)
if a8_match is None:
    violations.append("SPOR64_A8.f90: MCGMRE64 not found")
    a8_flat = ""
else:
    a8_flat = re.sub(r"\s+", "", a8_match.group(0).upper())


def require(token: str, description: str) -> None:
    if token not in flat:
        violations.append(f"missing {description}")


require("LSPOTFS=.FALSE.", "default-off SPOT scope")
require(
    "IF((CXDOOR.EQ.'MCCG').AND.(ITYPEC.EQ.0).AND."
    "C_ASSOCIATED(IPSYS).AND.C_ASSOCIATED(IPSOU))THEN",
    "fixed-source MCCG entry scope",
)
require("LCMLEN(IPSYS,'SPOT-LEAK1D',ILONG,ITYLCM)", "SPOT leakage lookup")
require("LCMLEN(IPSOU,'SPOT-FROZEN',ILEN,ITYLCM)", "frozen-source lookup")
require("IF(IFROZEN.NE.1)CALLXABORT", "frozen-source value gate")
require("LSPOTFS=.TRUE.", "positive SPOT radial identity")
require(
    "LSTRICTK=(CXDOOR.EQ.'MCCG').AND.(ITYPEC.GE.2).AND.(ITYPEC.LE.3)",
    "strict MCCG TYPE-K identity",
)
strict = "IF(EINN.LT.EPSINR)THEN"
near = (
    "IF((.NOT.LSPOTFS).AND.(.NOT.LSTRICTK).AND.(IGDEB.GT.1).AND."
    "(EINN.LT.10.*EPSINR))THEN"
)
terminal = (
    "IF((EEXT.LT.EPSOUT).AND.(EINN.LT.EPSUNK).AND."
    "(EINR_LAST.LT.EPSINR).AND.(IINR_STATE.EQ.1).AND."
    "(IT.GE.2))THEN"
)
require(strict, "strict inner threshold")
require(near, "legacy-only near-inner guard")
require(terminal, "unchanged strict terminal predicate")
require(
    "EEXT=REAL(ABS(AKEFF-AKEEP(2))/AKEFF)",
    "actual-input/raw-output k defect",
)
raw_gate = terminal
outer_acceleration = "CALLFLU2AC(NGRP,NUNKNO,1,FLUX(1,1,1),AKEEP(1),ZMU)"
require(outer_acceleration, "nonterminal outer FLU2AC call")
require(
    "IF(LSPOTFS)THENCALLXABORT("
    "'FLU2DR:SPOTTYPE-SSTRICTTERMINATIONREQUIRED.')",
    "shared SPOT identity at the iteration-cap failure gate",
)

if flat.count("10.*EPSINR") != 1:
    violations.append("expected exactly one legacy 10*EPSINR expression")
if flat.count("LSPOTFS=.FALSE.") != 1 or flat.count("LSPOTFS=.TRUE.") != 1:
    violations.append("SPOT radial identity must have one default and one setter")
if strict in flat and near in flat and flat.index(strict) > flat.index(near):
    violations.append("strict threshold must be tested before the legacy shortcut")
if (
    raw_gate in flat
    and outer_acceleration in flat
    and flat.index(raw_gate) > flat.index(outer_acceleration)
):
    violations.append("outer acceleration must follow the raw Picard gate")
for earlier, later, description in (
    ("LSPOTFS=.TRUE.", "DO400IT=1,MAXOUT", "identity before iteration"),
    (near, "IF(LSPOTFS)THEN", "near branch before shared cap gate"),
):
    if earlier not in flat or later not in flat or flat.index(earlier) > flat.index(later):
        violations.append(f"invalid order: {description}")

if a8_flat:
    if "STRICT_EPSMAX64=EPSILON(1.0_REAL64)" not in aca_all_flat:
        violations.append(
            "SPOR64_A8_ACA.f90: REAL64 ACA machine-zero threshold is missing"
        )
    if "INHERITED_EPSMAX64" in aca_all_flat:
        violations.append(
            "SPOR64_A8_ACA.f90: promoted REAL32 ACA threshold remains active"
        )
    if aca_all_flat.count("STRICT_EPSMAX64*") != 3:
        violations.append(
            "SPOR64_A8_ACA.f90: expected three REAL64 ACA threshold uses"
        )
    for token, description in (
        ("REPLACEMENT_LOOP:DO", "ACA true-residual replacement loop"),
        (
            "BICGSTAB_LOOP:DOWHILE(MAXM-ITER>=2)",
            "ACA pair-wise work-cap guard",
        ),
        (
            "IF(EPS64<=EPSM64)CYCLEREPLACEMENT_LOOP",
            "recursive-to-true ACA residual replacement",
        ),
        (
            "IF(MAXM-ITER<2)EXITREPLACEMENT_LOOP",
            "ACA final true check before work-cap failure",
        ),
        (
            "ACAISACORRECTIVEACCELERATOR,NOTTHEACCEPTEDTRANSPORTSOLVE.",
            "ACA capped-correction boundary",
        ),
    ):
        if token not in aca_all_flat:
            violations.append(f"SPOR64_A8_ACA.f90: missing {description}")
    aca_true_residual = "RI64(I)=RHS64(I)-RI64(I)"
    aca_true_accept = "IF(EPS64<=EPSM64)THENOK=.TRUE.RETURNENDIF"
    aca_pair = "BICGSTAB_LOOP:DOWHILE(MAXM-ITER>=2)"
    true_pos = aca_all_flat.find(aca_true_residual)
    accept_pos = aca_all_flat.find(aca_true_accept, true_pos)
    cap_pos = aca_all_flat.find("IF(MAXM-ITER<2)EXITREPLACEMENT_LOOP", accept_pos)
    pair_pos = aca_all_flat.find(aca_pair, cap_pos)
    if not (0 <= true_pos < accept_pos < cap_pos < pair_pos):
        violations.append(
            "SPOR64_A8_ACA.f90: ACA must recompute/accept TRUE residual "
            "before admitting another bounded BiCGSTAB pair"
        )
    if "IF(.NOT.ALL(IEEE_IS_FINITE(F64)))RETURNOK=.TRUE." not in aca_all_flat:
        violations.append(
            "SPOR64_A8_ACA.f90: finite MAXM-capped ACA correction is not returned"
        )
    if "MCGABG64:TRUETERMINALFAILED" in aca_all_flat:
        violations.append(
            "SPOR64_A8_ACA.f90: ACA cap is incorrectly treated as physical failure"
        )
    for token, description in (
        (
            "HISTORY_CAPACITY=2*MAXI+1",
            "derived mixed-history capacity",
        ),
        (
            "SIZE(REPS64,1)/=HISTORY_CAPACITY",
            "history-array capacity guard",
        ),
        (
            "RESTART_DIMENSION=KRYL",
            "tracked GMRES restart dimension",
        ),
        (
            "NARNOLDI<MAXI",
            "tracked Arnoldi-work cap",
        ),
        (
            "IF(NARNOLDI>=MAXI)EXIT",
            "final-TRUE-before-cap exit",
        ),
    ):
        if token not in a8_flat:
            violations.append(f"SPOR64_A8.f90: missing {description}")
    if "INTEGER,PARAMETER::MAXIT" in a8_all_flat:
        violations.append("SPOR64_A8.f90: fixed MAXIT work cap remains")
    if "INTEGER,PARAMETER::NSTART" in a8_all_flat:
        violations.append("SPOR64_A8.f90: obsolete NSTART restart remains")
    if "DP_MCCG_EPSI64=1.0E-13_REAL64" not in a8_all_flat:
        violations.append("SPOR64_A8.f90: strict REAL64 residual terminal changed")
    if "ALLOCATE(REPS64(HISTORY_CAPACITY,NGEFF)" not in a8_all_flat:
        violations.append("SPOR64_A8.f90: history is not allocated to its capacity")
    if a8_flat.count("IF(ITER>=HISTORY_CAPACITY)RETURN") != 2:
        violations.append(
            "SPOR64_A8.f90: expected TRUE and Arnoldi history bounds"
        )
    if a8_flat.count("NARNOLDI=NARNOLDI+1") != 1:
        violations.append("SPOR64_A8.f90: Arnoldi work counter must advance once")
    for token, description in (
        ("MCCGF64-CENSUS:BEGINTITLE=", "per-plane census begin marker"),
        ("MCCGF64-CENSUS:ENDTITLE=", "per-plane census end marker"),
        ("MCGMRE64-CENSUS:TRUEITER=", "true-residual census marker"),
        ("MAXVAL(REPS64(ITER,:))", "reported stored true residual"),
    ):
        if token not in a8_all_flat:
            violations.append(f"SPOR64_A8.f90: missing {description}")
    if a8_flat.count("FLUSH(6)") < 2:
        violations.append("SPOR64_A8.f90: census/failure output is not flushed")
    census_marker = "MCGMRE64-CENSUS:TRUEITER="
    census_pos = a8_flat.find(census_marker)
    census_count = a8_flat.rfind("LNCONV=COUNT(NCONV)", 0, census_pos)
    census_flush = a8_flat.find("FLUSH(6)", census_pos)
    census_exit = a8_flat.find("IF(LNCONV==0)EXIT", census_pos)
    if a8_flat.count(census_marker) != 1:
        violations.append("SPOR64_A8.f90: true-residual census site must be unique")
    if not (0 <= census_count < census_pos < census_flush < census_exit):
        violations.append(
            "SPOR64_A8.f90: census must follow the outer residual count, flush, "
            "then test the zero-group exit"
        )
    elif "MASK=NCONV" in a8_flat[census_pos:census_exit]:
        violations.append("SPOR64_A8.f90: census must include newly converged groups")

    active_decl = "LOGICAL,ALLOCATABLE::KRYLOV_ACTIVE(:)"
    active_alloc = "ALLOCATE(KRYLOV_ACTIVE(NGEFF))"
    arnoldi_cap = a8_flat.find("IF(NARNOLDI>=MAXI)EXIT", census_exit)
    active_seed = a8_flat.find("KRYLOV_ACTIVE=NCONV", arnoldi_cap)
    krylov_guard = a8_flat.find("DOWHILE(ANY(KRYLOV_ACTIVE).AND.", active_seed)
    givens_begin = a8_flat.find("RHO64(II)=ABS(G64(K+1,II))", krylov_guard)
    active_retire = a8_flat.find(
        "KRYLOV_ACTIVE(II)=KRYLOV_ACTIVE(II).AND.&"
        "RHO64(II)>=EPSI64*DENOM64(II)",
        givens_begin,
    )
    flux_update = a8_flat.find("PHIIN64(:,II)=PHIIN64(:,II)+", active_retire)
    true_recount = a8_flat.find("LNCONV=COUNT(NCONV)", flux_update)
    if active_decl not in a8_flat or active_alloc not in a8_flat:
        violations.append("SPOR64_A8.f90: missing independent Krylov work mask")
    if a8_flat.count("KRYLOV_ACTIVE=NCONV") != 1:
        violations.append("SPOR64_A8.f90: Krylov work mask must be seeded once")
    if a8_flat.count("DOWHILE(ANY(KRYLOV_ACTIVE).AND.") != 1:
        violations.append("SPOR64_A8.f90: Krylov loop must use its work mask")
    if "K<RESTART_DIMENSION" not in a8_flat:
        violations.append("SPOR64_A8.f90: Krylov loop ignores tracked restart")
    if a8_flat.count("FLOUT64,KRYLOV_ACTIVE,EPSINTO64") != 2:
        violations.append("SPOR64_A8.f90: Krylov operator calls must use work mask")
    if a8_flat.count("NCONV(II)=NCONV(II).AND.") != 2:
        violations.append("SPOR64_A8.f90: nconv must change only at TRUE gates")
    if not (
        0
        <= census_exit
        < arnoldi_cap
        < active_seed
        < krylov_guard
        < givens_begin
        < active_retire
        < flux_update
        < true_recount
    ):
        violations.append(
            "SPOR64_A8.f90: Krylov retirement must be followed by flux update "
            "while TRUE convergence state remains authoritative"
        )
    elif "NCONV(II)=" in a8_flat[active_seed:true_recount]:
        violations.append("SPOR64_A8.f90: Givens path must not retire TRUE groups")
    elif "LNCONV=COUNT(KRYLOV_ACTIVE)" in a8_flat[active_seed:true_recount]:
        violations.append("SPOR64_A8.f90: Krylov count must not drive outer success")

    plane_census = (
        "IF(R64_MODE==SPOR64_B2B_CONT)THEN"
        "CALLLCMGET(IPSYS,'SPOT-L1-SNAP',PLANE_INDEX)"
        "WRITE(6,'(A,I0)')'SPOR64_B2B-CENSUS:PLANE=',PLANE_INDEX"
        "FLUSH(6)"
    )
    if plane_census not in b2b_all_flat:
        violations.append("SPOR64_B2B.f90: missing sealed CONT plane census")

    final_count = a8_flat.rfind("LNCONV=COUNT(NCONV)")
    terminal_guard = a8_flat.find("IF(LNCONV/=0)THEN", final_count)
    final_success = a8_flat.rfind("OK=.TRUE.")
    if final_count < 0:
        violations.append("SPOR64_A8.f90: final unconverged-group count missing")
    if terminal_guard < 0:
        violations.append("SPOR64_A8.f90: strict GMRES fail-closed guard missing")
    elif "RETURN" not in a8_flat[terminal_guard:final_success]:
        violations.append("SPOR64_A8.f90: strict GMRES guard does not reject")
    if not (0 <= final_count < terminal_guard < final_success):
        violations.append(
            "SPOR64_A8.f90: strict GMRES guard must precede final success"
        )

# Bind the selector to the existing production records and actual TYPE-S call.
deck = re.sub(
    r"\s+", " ", (ROOT / "data/SpotPlaneFS.c2m").read_text().upper()
)
producer = re.sub(
    r"\s+", "", (ROOT / "src/SPOFSRC.f90").read_text().upper()
)
assembler = re.sub(
    r"\s+", "", (ROOT / "src/ASMDRV.f").read_text().upper()
)
for condition, description in (
    ("MACRO0 FSOURCE := SPOFSRC:" in deck, "SPOFSRC production call"),
    ("SYSTEM := ASM:" in deck and "ARM LK1D" in deck, "LK1D SYSTEM assembly"),
    (
        "FLUX := FLU: MACRO0 TRACK TRACK_F SYSTEM FSOURCE ::" in deck
        and "TYPE S" in deck,
        "TYPE-S FLU call with SYSTEM and FSOURCE",
    ),
    (
        "LCMPUT(KENTRY(2),'SPOT-FROZEN',1,1,(/1/))" in producer,
        "SPOFSRC frozen-source marker",
    ),
    (
        "LCMPUT(IPSYS,'SPOT-LEAK1D',NGROUP,2,LEAK1D)" in assembler,
        "ASMDRV SPOT leakage marker",
    ),
):
    if not condition:
        violations.append(f"missing production binding: {description}")


def inner_action(
    *, spot_radial: bool, strict_k: bool, igdeb: int, ratio: float
) -> str:
    """Mirror the two ordered FLU2DR decisions for a tiny truth table."""
    if ratio < 1.0:
        return "STRICT"
    if (not spot_radial) and (not strict_k) and igdeb > 1 and ratio < 10.0:
        return "NEAR"
    return "CONTINUE"


cases = {
    (True, False, 2, 0.5): "STRICT",
    (False, True, 2, 0.5): "STRICT",
    (True, False, 2, 5.0): "CONTINUE",
    (False, True, 2, 5.0): "CONTINUE",
    (False, False, 2, 5.0): "NEAR",
    (False, False, 1, 5.0): "CONTINUE",
    (True, False, 2, 10.0): "CONTINUE",
}
for (spot_radial, strict_k, igdeb, ratio), expected in cases.items():
    actual = inner_action(
        spot_radial=spot_radial,
        strict_k=strict_k,
        igdeb=igdeb,
        ratio=ratio,
    )
    if actual != expected:
        violations.append(
            f"truth table mismatch for {(spot_radial, strict_k, igdeb, ratio)}: "
            f"{actual} != {expected}"
        )

if violations:
    raise SystemExit("SPOT STRICT-INNER FAIL:\n" + "\n".join(violations))

print(
    "SPOT STRICT-INNER PASS: frozen-source TYPE-S MCCG solves use EPSINR "
    "directly; MCCG TYPE-K removes the 10*EPSINR restart and gates the raw "
    "Picard image before FLU2AC; unrelated paths retain the legacy schedule."
)

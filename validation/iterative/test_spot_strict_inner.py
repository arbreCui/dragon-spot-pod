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
strict = "IF(EINN.LT.EPSINR)THEN"
near = (
    "IF((.NOT.LSPOTFS).AND.(IGDEB.GT.1).AND."
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
for earlier, later, description in (
    ("LSPOTFS=.TRUE.", "DO400IT=1,MAXOUT", "identity before iteration"),
    (near, "IF(LSPOTFS)THEN", "near branch before shared cap gate"),
):
    if earlier not in flat or later not in flat or flat.index(earlier) > flat.index(later):
        violations.append(f"invalid order: {description}")

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


def inner_action(*, spot_radial: bool, igdeb: int, ratio: float) -> str:
    """Mirror the two ordered FLU2DR decisions for a tiny truth table."""
    if ratio < 1.0:
        return "STRICT"
    if (not spot_radial) and igdeb > 1 and ratio < 10.0:
        return "NEAR"
    return "CONTINUE"


cases = {
    (True, 2, 0.5): "STRICT",
    (False, 2, 0.5): "STRICT",
    (True, 2, 5.0): "CONTINUE",
    (False, 2, 5.0): "NEAR",
    (False, 1, 5.0): "CONTINUE",
    (True, 2, 10.0): "CONTINUE",
}
for (spot_radial, igdeb, ratio), expected in cases.items():
    actual = inner_action(spot_radial=spot_radial, igdeb=igdeb, ratio=ratio)
    if actual != expected:
        violations.append(
            f"truth table mismatch for {(spot_radial, igdeb, ratio)}: "
            f"{actual} != {expected}"
        )

if violations:
    raise SystemExit("SPOT STRICT-INNER FAIL:\n" + "\n".join(violations))

print(
    "SPOT STRICT-INNER PASS: frozen-source TYPE-S MCCG solves use EPSINR "
    "directly; unrelated FLU paths retain the legacy near-inner schedule."
)

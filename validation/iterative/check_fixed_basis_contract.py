#!/usr/bin/env python3
"""Static contract for a fixed POD trial space with a live radial response."""

from __future__ import annotations

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
asm_path = root / "src/ASM.f"
spoasm_path = root / "src/SPOASM.f"
state_path = root / "src/SPOSTATE.f90"
b2i_path = root / "src/SPOR64_B2I.f90"
b2j_path = root / "src/SPOR64_B2J.f90"
b2w_path = root / "src/SPOR64_B2W.f90"

contract_paths = (asm_path, spoasm_path, state_path, b2i_path, b2j_path, b2w_path)
if not all(path.is_file() for path in contract_paths):
    raise SystemExit("FIXED-BASIS CONTRACT FAIL: required source is missing")

asm = asm_path.read_text(errors="strict")
spoasm = spoasm_path.read_text(errors="strict")
state = state_path.read_text(errors="strict")
b2i = b2i_path.read_text(errors="strict")
b2j = b2j_path.read_text(errors="strict")
b2w = b2w_path.read_text(errors="strict")
violations: list[str] = []


def require(text: str, pattern: str, description: str) -> None:
    if re.search(pattern, text, re.IGNORECASE | re.DOTALL) is None:
        violations.append("missing " + description)


require(asm, r"HSIGN\.EQ\.'L_ARCHIVE'.*HSIGN\.EQ\.'L_PIJ'", "separate SNAP/BASIS inputs")
require(asm, r"TEXT4\.EQ\.'FIXB'.*IFIXB\s*=\s*1", "FIXB keyword")
require(asm, r"FIXB REQUIRES A POSITIVE SPOD RANK", "positive fixed-rank gate")
require(asm, r"FIXB REQUIRES A READ-ONLY BASIS OBJECT", "basis-presence gate")
require(asm, r"OUTPUT AND FIXED-BASIS OBJECT MUST BE DISTINCT", "alias rejection")
require(asm, r"BASIS OBJECT PROVIDED WITHOUT FIXB", "unused basis rejection")
require(asm, r"LINK\.BASIS", "basis provenance link")
require(
    asm,
    r"CALL\s+SPOASM\s*\(\s*IPSYS\s*,\s*IPMACR\s*,\s*IPTRK\s*,"
    r"\s*IPSNAP\s*,\s*IPBASIS\s*,\s*IFIXB",
    "fixed-basis SPOASM interface",
)

require(
    spoasm,
    r"IF\s*\(\s*IFIXB\.EQ\.0\s*\)\s*THEN\s*CALL\s+SPOPOD"
    r".*ELSE\s*KPBASIS\s*=\s*LCMGIL",
    "SPOPOD only in the basis-building branch",
)
for record in (
    "NREG2D",
    "NSNAP",
    "POD-NMODE",
    "VOL2D",
    "POD-BASIS",
    "POD-COEFF",
    "POD-SIGMA",
    "POD-REC-ERR",
    "POD-ORTHO",
):
    require(
        spoasm,
        rf"LCM(?:LEN|GET)\s*\(\s*KPBASIS\s*,\s*'{re.escape(record)}'",
        f"fixed {record} validation/copy",
    )

require(spoasm, r"FIXED-BASIS VOLUME MISMATCH", "bitwise geometry gate")
require(spoasm, r"FIXED-BASIS MODE COUNT DOES NOT MATCH RANK", "rank identity gate")
require(
    spoasm,
    r"RANK_POD\.GT\.NREG2D.*FIXED BASIS RANK EXCEEDS RADIAL DIMENSION",
    "fixed rank bounded by radial dimension",
)
require(
    spoasm,
    r"NBASCOL\s*=\s*RANK_POD.*ALLOCATE\s*\(\s*BASIS\s*\(\s*NREG2D\s*,\s*NBASCOL",
    "fixed basis storage sized by requested rank",
)
require(spoasm, r"SPOT-FIXB", "fixed-basis state marker")
require(spoasm, r"POD-FIXED", "fixed-basis type marker")

require(
    state,
    r"rank\(igr\)\s*>\s*nreg2d",
    "SPOSTATE radial-dimension rank bound",
)
for source, label in ((b2i, "B2I"), (b2j, "B2J"), (b2w, "B2W")):
    require(source, r"any\(rank\s*>\s*nreg\)", f"{label} radial-dimension rank bound")
    require(source, r"'POD-FIXED'", f"{label} fixed-basis provenance marker")
require(b2j, r"max_rank\s*=\s*maxval\(rank\)", "B2J maximum-rank extent")
require(
    b2j,
    r"basis_slice32\(nreg,max_rank\).*coordinate_slice64\(max_rank\)",
    "B2J full-rank reconstruction scratch",
)

# RADIAL-OP must still come from the current DB2 reconstruction, outside the
# fixed/dynamic POD selection. The fixed branch copies no reference response.
require(
    spoasm,
    r"DB2\s*\(\s*I,ISNAP,IGR\s*\)\s*=\s*SPOLE2.*"
    r"IF\s*\(\s*IFIXB\.EQ\.0\s*\).*"
    r"LCMPUT\s*\(\s*KPSYS\s*,\s*'RADIAL-OP'.*DB2",
    "current radial response after fixed-basis selection",
)
fixed_branch = re.search(
    r"IF\s*\(\s*IFIXB\.EQ\.0\s*\)\s*THEN(?P<dynamic>.*?)"
    r"ELSE(?P<fixed>.*?)ENDIF\s*\n\s*POD_RANK",
    spoasm,
    re.IGNORECASE | re.DOTALL,
)
if fixed_branch is None:
    violations.append("cannot isolate fixed-basis branch")
else:
    fixed = fixed_branch.group("fixed")
    if re.search(r"\bSPOPOD\b", fixed, re.IGNORECASE):
        violations.append("fixed-basis branch calls SPOPOD")
    if re.search(r"'RADIAL-OP'", fixed, re.IGNORECASE):
        violations.append("fixed-basis branch copies a stale reference RADIAL-OP")

if violations:
    raise SystemExit("FIXED-BASIS CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "FIXED-BASIS CONTRACT PASS: FIXB reuses only the manifested POD package "
    "from a distinct read-only system while RADIAL-OP is rebuilt from the "
    "current radial fixed-source state."
)

#!/usr/bin/env python3
"""Static contract for a fixed POD trial space with a live radial response."""

from __future__ import annotations

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
asm_path = root / "src/ASM.f"
spoasm_path = root / "src/SPOASM.f"

if not asm_path.is_file() or not spoasm_path.is_file():
    raise SystemExit("FIXED-BASIS CONTRACT FAIL: ASM/SPOASM source is missing")

asm = asm_path.read_text(errors="strict")
spoasm = spoasm_path.read_text(errors="strict")
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
require(spoasm, r"SPOT-FIXB", "fixed-basis state marker")
require(spoasm, r"POD-FIXED", "fixed-basis type marker")

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

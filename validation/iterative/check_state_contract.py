#!/usr/bin/env python3
"""Static contract for x=(a,1/k,L) and its unmodified map defect."""

from __future__ import annotations

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
state_path = root / "src/SPOSTATE.f90"
conv_path = root / "src/SPOXCONV.f90"
proj_path = root / "src/SPOPROJ.f90"
driver_path = root / "src/KDRDRV.F"

for path in (state_path, conv_path, proj_path, driver_path):
    if not path.is_file():
        raise SystemExit(f"STATE CONTRACT FAIL: missing {path.relative_to(root)}")

state = state_path.read_text(errors="strict")
conv = conv_path.read_text(errors="strict")
proj = proj_path.read_text(errors="strict")
driver = driver_path.read_text(errors="strict")
violations: list[str] = []


def require(text: str, pattern: str, description: str) -> None:
    if re.search(pattern, text, re.IGNORECASE | re.DOTALL) is None:
        violations.append("missing " + description)


require(driver, r"HMODUL\.EQ\.'SPOSTATE:'.*CALL\s+SPOSTATE", "SPOSTATE registration")
require(driver, r"HMODUL\.EQ\.'SPOXCONV:'.*CALL\s+SPOXCONV", "SPOXCONV registration")

require(state, r"norm\s*=\s*norm\s*\+.*volume.*unknown.*production", "one global nu-fission normalization")
require(state, r"projected_sp\s*=\s*projected_sp\s*\+.*volume.*unknown", "binary32 production restriction")
require(state, r"projected_sp\s*=\s*projected_sp\s*/\s*weight_sp", "binary32 production average")
require(state, r"plane\(i\)\s*=\s*real\s*\(\s*projected_sp\s*,\s*dp\s*\)\s*/\s*norm", "single global normalization after restriction")
require(state, r"call\s+solve_spd\s*\(\s*gram\s*,\s*rhs", "Gram coordinate solve")
require(state, r"call\s+SPOLE1\b", "physical leakage reconstruction")
require(state, r"SPOT-X-BASIS", "stored basis bits")
require(state, r"require_record\s*\(\s*kentry\(2\)\s*,\s*'MATCOD'", "fail-closed geometry reads")

for record in (
    "SPOT-X-DIMS",
    "SPOT-X-RANK",
    "SPOT-X-OFF",
    "SPOT-X-GOFF",
    "SPOT-X-BOFF",
    "SPOT-X-A",
    "SPOT-X-GRAM",
    "SPOT-X-RHO",
    "SPOT-X-L",
    "SPOT-X-H",
    "SPOT-X-NORM",
    "SPOT-X-NID",
):
    require(state, rf"'{re.escape(record)}'", f"{record} output")

require(conv, r"FIXED POD BASIS CHANGED", "bitwise fixed-basis rejection")
require(conv, r"real32_bits\s*\(\s*basis_c\s*\).*real32_bits\s*\(\s*basis_p", "raw basis-bit comparison")
require(conv, r"FIXED SPACE OR AXIAL HEIGHT CHANGED", "Gram/height rejection")
require(conv, r"r_rho\s*=\s*abs\s*\(\s*rho_c\s*-\s*rho_p\s*\)", "inverse-k defect")
require(conv, r"d_leak\s*=\s*maxval\s*\(\s*abs\s*\(\s*leak_c\s*-\s*leak_p", "absolute leakage defect")
require(conv, r"if\s*\(\s*leak_scale\s*==\s*0\.0_dp\s*\)", "exact zero-leakage branch")
require(conv, r"r_a\s*=\s*sqrt\s*\(\s*numerator\s*/\s*denominator\s*\)", "physical coordinate defect")
require(conv, r"numerator\s*=\s*numerator\s*\+\s*height_c\(isnap\)", "plane height in coordinate numerator")
require(conv, r"denominator\s*=\s*denominator\s*\+\s*height_c\(isnap\)", "plane height in coordinate denominator")
for record in ("SPOT-X-RRHO", "SPOT-X-RLEAK", "SPOT-X-DLEAK", "SPOT-X-RA"):
    require(conv, rf"'{re.escape(record)}'", f"{record} residual")

require(proj, r"text4\s*==\s*'FIXB'", "explicit canonical projection option")
require(proj, r"canonical_value\s*=\s*canonical_value\s*\+.*basis_state.*coordinates", "unit-normalized Ba feedback reconstruction")
require(proj, r"raw_value\s*/\s*norm\s*-\s*canonical_value", "off-space diagnostic in the same global normalization")
require(proj, r"project_marker\s*=\s*2", "canonical projection provenance marker")
require(proj, r"'SPOT-PJ-PERP'", "raw-to-canonical projection diagnostic")

for text,name in ((state,"SPOSTATE"),(conv,"SPOXCONV"),(proj,"SPOPROJ")):
    if re.search(r"\bRELA(?:X|XATION)?\b|\bCMFD\b|\bFLU_FLOOR\b", text, re.IGNORECASE):
        violations.append(f"{name} contains forbidden stabilization")
    if re.search(r"\bgroup_scale\b|\bplane_scale\b|\bisclose\b", text, re.IGNORECASE):
        violations.append(f"{name} contains a local fitted scale")

if violations:
    raise SystemExit("STATE CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "STATE CONTRACT PASS: SPOSTATE uses the production binary32 restriction "
    "and one global normalization; explicit SPOPROJ FIXB feeds only B*a, while "
    "SPOXCONV reports separate raw defects and rejects any basis-bit change."
)

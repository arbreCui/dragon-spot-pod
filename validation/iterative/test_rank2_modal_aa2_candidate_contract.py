#!/usr/bin/env python3
"""Seconds-scale static contract for the single offline rank-2 AA(2) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa2_candidate_inputs.tsv").read_text()
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa2_candidate.sh").read_text()
makefile = (ROOT / "Makefile").read_text()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 MODAL AA2 CONTRACT FAIL: {message}")


rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = (
    "xnext_pub", "xnext_plus", "xroll_pub", "xroll_plus",
    "xroll2_pub", "xroll2_plus", "xroll2_plus_snapshots",
    "basis_reference",
)
require(manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa2-candidate-inputs-v1",
        "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in rows),
        "manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rows),
        "manifest path escapes repository")
require(rows[5][1] ==
        "e95e2a7577d82d9c9b8a28f938a121a4c8409e68764a8cdec9910fb3c1c6d70b",
        "latest returned AX changed")
require(rows[6][1] ==
        "bf08f193d745e1bbf66fc200f5fd8041b3b8eb37d1aa0e6b33757ca60f59eeb4",
        "latest returned snapshot changed")

for token in (
    "--rolling-aa2 x0 x0p x1 x1p x2 x2p x2p_snap",
    "d0a=f0a-f2a", "d1a=f1a-f2a",
    "determinant=h00*h11-h01*h01",
    "(determinant <= 0.0_real64)",
    "gamma0=(h01*c1-h11*c0)/determinant",
    "gamma1=(h01*c0-h00*c1)/determinant",
    "alpha2=1.0_real64-gamma0-gamma1",
    "predicted_sq=f2_sq+2.0_real64*gamma0*c0+",
    "(predicted_sq < 0.0_real64)",
    "candidate_a=alpha0*out0%coordinates+alpha1*out1%coordinates+",
    "candidate_l=alpha0*out0%leakage+alpha1*out1%leakage+",
    "rho_affine=alpha0*out0%rho+alpha1*out1%rho+alpha2*out2%rho",
    "call LCMEQU(out2%root,aa2_staged_ax)",
    "call LCMEQU(out2_snap,aa2_staged_snap)",
    "aa2_marker='AA2-RAW-FLUX'",
):
    require(token in builder, f"builder contract missing: {token}")

for token in (
    "trim(mode_argument) /= '--rolling-aa2'",
    "'AA2 XNEXT INPUT','AA1-RAW-FLUX'",
    "'AA2 XROLL INPUT','XNP-RAW-FLUX'",
    "'AA2 XROLL2 INPUT','XRP-RAW-FLUX'",
    "'AA2 MATERIALIZED PROPOSAL','AA2-RAW-FLUX'",
    "determinant=h00*h11-h01*h01",
    "(determinant <= 0.0_real64)",
    "gamma0=(h01*c1-h11*c0)/determinant",
    "gamma1=(h01*c0-h00*c1)/determinant",
    "(predicted_sq < 0.0_real64)",
    "affine_a=alpha0*out0%coordinates+alpha1*out1%coordinates+",
    "call compare_axial_carrier_payload(out2_name,proposal_name)",
    "call check_snapshot_publication(out2_snap_name,proposal_snap_name,",
    "STANDARD 2X2 SYSTEM PASS",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"checker contract missing: {token}")

for token in (
    "rank2_modal_aa2_candidate_inputs.tsv",
    "--rolling-aa2 x0.xsm x0p.xsm x1.xsm x1p.xsm",
    "AA2-RAW-FLUX", "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in runner, f"runner contract missing: {token}")
expected = re.findall(r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", runner)
require(expected == [
    "aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed",
    "a6231acf84ed551e9144811c4bc775368c4a21132817ac757143a4c7e74d51dc",
], "output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loop is forbidden")
require("spot-rank2-modal-aa2-candidate" in makefile,
        "Make target is missing")

combined = "\n".join((builder, checker, runner)).lower()
for forbidden in ("regularization", "pseudoinverse", "pinv", "condition cutoff"):
    require(forbidden not in combined, f"forbidden control present: {forbidden}")

print("RANK2 MODAL AA2 CONTRACT PASS: three real residuals, one exact 2x2 "
      "system, fixed rank two, latest raw carrier and no map solve.")

#!/usr/bin/env python3
"""Seconds-scale static contract for offline rank-2 AA(2) proposals."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa2_candidate_inputs.tsv").read_text()
next_manifest = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_candidate_inputs.tsv"
).read_text()
current_manifest = (
    ITERATIVE / "rank2_current_aa2_candidate_inputs.tsv"
).read_text()
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa2_candidate.sh").read_text()
next_runner = (
    ITERATIVE / "run_rank2_modal_aa2_rolling_next_candidate.sh"
).read_text()
current_runner = (
    ITERATIVE / "run_rank2_current_aa2_candidate.sh"
).read_text()
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

next_rows = [line.split() for line in next_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
next_roles = (
    "x0_pub", "x0_plus", "x1_pub", "x1_plus", "x2_pub", "x2_plus",
    "x2_plus_snapshots", "basis_reference",
)
require(next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa2-rolling-next-candidate-inputs-v1",
        "rolling-next manifest version changed")
require(tuple(row[0] for row in next_rows) == next_roles,
        "rolling-next manifest roles changed")
require(all(len(row) == 3 for row in next_rows),
        "rolling-next manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in next_rows),
        "rolling-next manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in next_rows),
        "rolling-next manifest path escapes repository")
require(next_rows[4][1] ==
        "aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed",
        "rolling-next latest proposal input changed")
require(next_rows[5][1] ==
        "ebab72eb17b6b70e79fd8b48d0903b3dc9388ca417757efa90730bd3859acc17",
        "rolling-next latest returned AX changed")
require(next_rows[6][1] ==
        "3f71736ec3a7b490f8635e9b0dcd7c365e7be05bc4a5af21232431954ac74f21",
        "rolling-next latest returned snapshot changed")

current_rows = [line.split() for line in current_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
current_roles = (
    "w", "x", "c", "d", "y", "e", "e_snapshots", "basis_reference",
)
require(current_manifest.splitlines()[0] ==
        "# spot-rank2-current-aa2-candidate-inputs-v1",
        "current manifest version changed")
require(tuple(row[0] for row in current_rows) == current_roles,
        "current manifest roles changed")
require(all(len(row) == 3 for row in current_rows),
        "current manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in current_rows),
        "current manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in current_rows),
        "current manifest path escapes repository")
require(tuple(row[1] for row in current_rows[:7]) == (
    "defdee0cf442470eb623ebb83c8bed59b8c20308121951ef0c72073ddba3c243",
    "b693b310ae8f499a869254cee77b1b787f9fa66813c24321dbfe5b00994c7196",
    "31579eccb0d6668c21c02add7d9dea9d64752fa9f32e20409ca22e3a53bf3255",
    "4e1d50a42353a8d76e3796539746225de6f62857045275847b5049f28e542a48",
    "fded732054da400dc6000b492287e29f7ae88fa2e8c62f80c7dda972940af2d1",
    "96cb06444bfca395b1765b907944aa2d32c4e877af41dbd58dee258b49025e45",
    "608b4ae084d7c5fdebbe3eaad30e82a453cd81fca160419eed4a7e73be288c91",
), "current w/x/c/d/y/e history changed")

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
    "trim(mode) == '--rolling-aa2-next'",
    "call build_rolling_aa2_candidate(.true.,.false.)",
    "aa2_report_prefix='RANK2-ROLLING-AA2-NEXT'",
    "'AA2-next xroll input'",
    ".true.,'XNP-RAW-FLUX'",
    "'AA2-next xroll2 input'",
    ".true.,'XRP-RAW-FLUX'",
    "'AA2-next xAA2 input'",
    ".true.,'AA2-RAW-FLUX'",
    "aa2_label2='XAA2-PLUS'",
):
    require(token in builder,
            f"rolling-next builder contract missing: {token}")

for token in (
    "trim(mode) == '--current-aa2'",
    "call build_rolling_aa2_candidate(.false.,.true.)",
    "aa2_report_prefix='RANK2-CURRENT-AA2'",
    "'current w input'", "'current x output'",
    "'current c input'", ".true.,'X4-RAW-FLUX'",
    "'current d output'", "'current y input'", ".true.,'Z-RAW-FLUX'",
    "'current e output'",
):
    require(token in builder,
            f"current builder contract missing: {token}")

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
    "trim(mode_argument) == '--rolling-aa2-next'",
    "rolling_aa2_next_mode=.true.",
    "aa2_report_prefix='RANK2-ROLLING-AA2-NEXT'",
    "'AA2-NEXT XROLL INPUT'",
    "'XNP-RAW-FLUX'",
    "'AA2-NEXT XROLL2 INPUT'",
    "'XRP-RAW-FLUX'",
    "'AA2-NEXT XAA2 INPUT'",
    "'AA2-RAW-FLUX'",
    "aa2_latest_output='XAA2-PLUS'",
):
    require(token in checker,
            f"rolling-next checker contract missing: {token}")

for token in (
    "trim(mode_argument) == '--current-aa2'",
    "current_aa2_mode=.true.",
    "aa2_report_prefix='RANK2-CURRENT-AA2'",
    "'CURRENT W INPUT'", "'CURRENT X OUTPUT'",
    "'CURRENT C INPUT','X4-RAW-FLUX'", "'CURRENT D OUTPUT'",
    "'CURRENT Y INPUT','Z-RAW-FLUX'", "'CURRENT E OUTPUT'",
    "aa2_latest_input='Y'", "aa2_latest_output='E'",
):
    require(token in checker,
            f"current checker contract missing: {token}")

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

for token in (
    "rank2_modal_aa2_rolling_next_candidate_inputs.tsv",
    "--rolling-aa2-next",
    "AA2-RAW-FLUX", "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in next_runner,
            f"rolling-next runner contract missing: {token}")
next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", next_runner
)
require(next_expected == [
    "ce9544e8f58b01d933f5937d781a0f1b70a58862468bbd380d5d2bc5c0e07715",
    "61604c1dfb586abe71115544aa73b4628f7528f5da32f6bce14ce8f7f8f30763",
], "rolling-next output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", next_runner),
        "rolling-next retry loop is forbidden")
require("spot-rank2-modal-aa2-rolling-next-candidate" in makefile,
        "rolling-next Make target is missing")

for token in (
    "rank2_current_aa2_candidate_inputs.tsv",
    "--current-aa2 w.xsm x.xsm c.xsm d.xsm y.xsm",
    "AA2-RAW-FLUX", "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in current_runner,
            f"current runner contract missing: {token}")
current_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", current_runner
)
require(current_expected == [
    "dc2251e13fa473ceebee7839c32bd5b3244498134a8acfab93b39c55b1e79469",
    "87ed9359809608c838991d2743914a47d96741fc94cedc07d06d512735970b63",
], "current output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", current_runner),
        "current retry loop is forbidden")
require("spot-rank2-current-aa2-candidate" in makefile,
        "current Make target is missing")

combined = "\n".join(
    (builder, checker, runner, next_runner, current_runner)
).lower()
for forbidden in ("regularization", "pseudoinverse", "pinv", "condition cutoff"):
    require(forbidden not in combined, f"forbidden control present: {forbidden}")

print("RANK2 MODAL AA2 CONTRACT PASS: all three-residual windows use one "
      "exact 2x2 system, fixed rank two, the latest raw carrier and no map "
      "solve.")

#!/usr/bin/env python3
"""Seconds-scale static contract for offline rank-2 AA(2) proposals."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa2_candidate_inputs.tsv").read_text()
next_manifest = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_candidate_inputs.tsv"
).read_text()
current_manifest = (
    ITERATIVE / "rank2_current_aa2_candidate_inputs.tsv"
).read_text()
ptuqv_manifest = (
    ITERATIVE / "rank2_current_ptuqv_aa2_candidate_inputs.tsv"
).read_text()
cefg_manifest = (
    ITERATIVE / "rank2_current_cefg_aa2_candidate_inputs.tsv"
).read_text()
ghi_manifest = (
    ITERATIVE / "rank2_current_ghi_aa2_candidate_inputs.tsv"
).read_text()
ghi_candidate_result = (
    ITERATIVE / "rank2_current_ghi_aa2_candidate_result.md"
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
ptuqv_runner = (
    ITERATIVE / "run_rank2_current_ptuqv_aa2_candidate.sh"
).read_text()
ptuqv_map_runner_path = ITERATIVE / "run_rank2_current_ptuqv_aa2_map.sh"
ptuqv_map_runner = ptuqv_map_runner_path.read_text()
ptuqv_map_parent = (
    ITERATIVE / "rank2_current_ptuqv_aa2_map_parent.tsv"
).read_text()
cefg_map_runner_path = ITERATIVE / "run_rank2_current_cefg_aa2_map.sh"
cefg_map_runner = cefg_map_runner_path.read_text()
cefg_map_parent = (
    ITERATIVE / "rank2_current_cefg_aa2_map_parent.tsv"
).read_text()
cefg_map_policy = (
    ITERATIVE / "rank2_current_cefg_aa2_map_policy.md"
).read_text()
cefg_map_result = (
    ITERATIVE / "rank2_current_cefg_aa2_map_result.md"
).read_text()
ghi_map_runner_path = ITERATIVE / "run_rank2_current_ghi_aa2_map.sh"
ghi_map_runner = ghi_map_runner_path.read_text()
ghi_map_parent = (
    ITERATIVE / "rank2_current_ghi_aa2_map_parent.tsv"
).read_text()
ghi_map_policy = (
    ITERATIVE / "rank2_current_ghi_aa2_map_policy.md"
).read_text()
ghi_map_result = (
    ITERATIVE / "rank2_current_ghi_aa2_map_result.md"
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

ptuqv_rows = [line.split() for line in ptuqv_manifest.splitlines()
              if line.strip() and not line.startswith("#")]
require(ptuqv_manifest.splitlines()[0] ==
        "# spot-rank2-current-ptuqv-aa2-candidate-inputs-v1",
        "PTUQV manifest version changed")
require(tuple(row[0] for row in ptuqv_rows) ==
        ("p", "t", "u", "q", "v", "v_snapshots", "basis_reference"),
        "PTUQV manifest roles changed")
require(all(len(row) == 3 for row in ptuqv_rows),
        "PTUQV manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in ptuqv_rows),
        "PTUQV manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in ptuqv_rows),
        "PTUQV manifest path escapes repository")
require(tuple(row[1] for row in ptuqv_rows[:6]) == (
    "d00a310cffb832cfec6ef2bdaa6cf27cfd51443904afd8d26ca57418e140d225",
    "e35636e5badd21a5deb02964b995a948ea0df4eb110b7fd2783ef5c41f36145e",
    "7620e0a4a7bdfd77e89e83a46c09b5bd66d235c0e9cd0c0c68718a711b96ae3c",
    "75dd254844b001596f3e57e6aad373e6bdec7aa84958e79b9111c555e93556cf",
    "b58e6022a2d56f580038015bc0db2d2d584911d27633eccfbdb2d30ad9296fed",
    "2cb0fdc254599faacd695e25a043e2f3fd9331c848526929fb934ced2074ed81",
), "PTUQV actual-map history changed")

cefg_rows = [line.split() for line in cefg_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
require(cefg_manifest.splitlines()[0] ==
        "# spot-rank2-current-cefg-aa2-candidate-inputs-v1",
        "CEFG manifest version changed")
require(tuple(row[0] for row in cefg_rows) ==
        ("p", "t", "u", "q", "v", "v_snapshots", "basis_reference"),
        "CEFG manifest roles changed")
require(all(len(row) == 3 for row in cefg_rows),
        "CEFG manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in cefg_rows),
        "CEFG manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in cefg_rows),
        "CEFG manifest path escapes repository")
require(tuple(row[1] for row in cefg_rows[:6]) == (
    "978593b2813bad2242ad8c235fdd83e6f5bc33b3aff624b60ccecaaf077d95c6",
    "0b5c8d27b4d2e37d90d56d27d75619842851b7a0e0206947b31c3d5b88936828",
    "6e26d8dc40bf79c0dedad19912557dfed5ccd2c3bdb38ea719ce32b5cc9aba6c",
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "1b52b5ebd421e620f1f9d7d4e60e50fb002f85c25031533cc4d650e858dd030a",
    "7a0e441a25ad2cc3067210dd6ebd90cb26ba5a9722a4c38ea289237590e90602",
), "CEFG actual-map history changed")

ghi_rows = [line.split() for line in ghi_manifest.splitlines()
            if line.strip() and not line.startswith("#")]
require(ghi_manifest.splitlines()[0] ==
        "# spot-rank2-current-ghi-aa2-candidate-inputs-v1",
        "GHI manifest version changed")
require(tuple(row[0] for row in ghi_rows) ==
        ("w", "x", "c", "d", "y", "e", "e_snapshots",
         "basis_reference"),
        "GHI manifest roles changed")
require(all(len(row) == 3 for row in ghi_rows),
        "GHI manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in ghi_rows),
        "GHI manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in ghi_rows),
        "GHI manifest path escapes repository")
require(tuple(row[1] for row in ghi_rows[:7]) == (
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "1b52b5ebd421e620f1f9d7d4e60e50fb002f85c25031533cc4d650e858dd030a",
    "d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe",
    "5e53f33aea3d91db6999cc735d4ffd47677545ba350f34e36a266ff5e6f123ad",
    "c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6",
    "c35dc70d8d6dd35b889622734b81112a3e3fdc09455f8390ef262123f5aa3636",
    "c4f0b6ff6d6ffa28ff3a34061e5cf9e25c78fb1b31546188e932c5e82492f9b1",
), "GHI actual-map history changed")

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
    "trim(mode) == '--current-ptuqv-aa2'",
    "aa2_report_prefix='RANK2-CURRENT-PTUQV-AA2'",
    "'PTUQV p input'", ".true.,'X4-RAW-FLUX'",
    "'PTUQV t output'", "'PTUQV t input'", "'PTUQV u output'",
    "'PTUQV q input'", "'PTUQV v output'",
    "direction_gate_mode=qpzst_mode.or.stuvvw_mode.or.uvvwxy_mode.or.",
):
    require(token in builder,
            f"PTUQV builder contract missing: {token}")

for token in (
    "trim(mode) == '--current-cefg-aa2'",
    "aa2_report_prefix='RANK2-CURRENT-CEFG-AA2'",
    "aa2_label0='E'", "aa2_label1='F'", "aa2_label2='G'",
    "'CEFG c input'", "'AA1-RAW-FLUX'", "'CEFG e output'",
    "'CEFG e input'", "'CEFG f output'", "'CEFG q input'",
    "'CEFG g output'",
):
    require(token in builder,
            f"CEFG builder contract missing: {token}")

for token in (
    "trim(mode) == '--current-ghi-aa2'",
    "aa2_report_prefix='RANK2-CURRENT-GHI-AA2'",
    "aa2_label0='G'", "aa2_label1='H'", "aa2_label2='I'",
    "'GHI q1 input'", "'GHI g output'", "'GHI q2 input'",
    "'AA2-RAW-FLUX'", "'GHI h output'", "'GHI q3 input'",
    "'AA1-RAW-FLUX'", "'GHI i output'",
):
    require(token in builder,
            f"GHI builder contract missing: {token}")

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
    "trim(mode_argument) == '--current-ptuqv-aa2'",
    "current_ptuqv_aa2_mode=.true.",
    "aa2_report_prefix='RANK2-CURRENT-PTUQV-AA2'",
    "'PTUQV P INPUT','X4-RAW-FLUX'", "'PTUQV T OUTPUT'",
    "'PTUQV T INPUT'", "'PTUQV U OUTPUT'",
    "'PTUQV Q INPUT','X4-RAW-FLUX'", "'PTUQV V OUTPUT'",
    "aa2_latest_input='Q'", "aa2_latest_output='V'",
):
    require(token in checker,
            f"PTUQV checker contract missing: {token}")

for token in (
    "trim(mode_argument) == '--current-cefg-aa2'",
    "current_cefg_aa2_mode=.true.",
    "aa2_report_prefix='RANK2-CURRENT-CEFG-AA2'",
    "'CEFG C INPUT','AA1-RAW-FLUX'", "'CEFG E OUTPUT'",
    "'CEFG E INPUT'", "'CEFG F OUTPUT'",
    "'CEFG Q INPUT','AA1-RAW-FLUX'", "'CEFG G OUTPUT'",
    "aa2_latest_input='Q'", "aa2_latest_output='G'",
):
    require(token in checker,
            f"CEFG checker contract missing: {token}")

for token in (
    "trim(mode_argument) == '--current-ghi-aa2'",
    "aa2_report_prefix='RANK2-CURRENT-GHI-AA2'",
    "'GHI Q1 INPUT','AA1-RAW-FLUX'", "'GHI G OUTPUT'",
    "'GHI Q2 INPUT','AA2-RAW-FLUX'", "'GHI H OUTPUT'",
    "'GHI Q3 INPUT','AA1-RAW-FLUX'", "'GHI I OUTPUT'",
    "aa2_latest_input='Q3'", "aa2_latest_output='I'",
):
    require(token in checker,
            f"GHI checker contract missing: {token}")

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
    "CANDIDATE_MODE=${CANDIDATE_MODE:---current-aa2}",
    "--current-aa2)", "--current-ghi-aa2)",
    './build_candidate "$CANDIDATE_MODE" w.xsm x.xsm c.xsm d.xsm',
    './check_candidate "$CANDIDATE_MODE" w.xsm x.xsm c.xsm d.xsm',
    "PARAMETER-FREE DIRECTION GATE PASS", "RECEIPT 9/9 PASS",
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
for token in (
    "spot-rank2-current-ghi-aa2-candidate",
    "rank2_current_ghi_aa2_candidate_inputs.tsv",
    "iterative-rank2-current-ghi-aa2-candidate",
    "CANDIDATE_MODE=--current-ghi-aa2",
    "REPORT_PREFIX=RANK2-CURRENT-GHI-AA2",
    "EXPECTED_AX_SHA_OVERRIDE=5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391",
    "EXPECTED_SNAP_SHA_OVERRIDE=d841554d9bb0b9e158dfda323ead4016c98c450387bb656416218f3b6d1d5548",
):
    require(token in makefile, f"GHI Make binding missing: {token}")
for token in (
    "0.54656692430484066", "0.22903224207636369",
    "0.22440083361879565", "7.9724244756408422e-26",
    "0.085602787687317231", "0.50064418931908561",
    "0.44048518991529284", "8880", "9/9",
    "5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391",
    "d841554d9bb0b9e158dfda323ead4016c98c450387bb656416218f3b6d1d5548",
    "Dragon", "physical map was run", "condition cutoff",
):
    require(token in ghi_candidate_result,
            f"GHI candidate result missing: {token}")

for token in (
    "rank2_current_ptuqv_aa2_candidate_inputs.tsv",
    "CANDIDATE_MODE=${CANDIDATE_MODE:---current-ptuqv-aa2}",
    "--current-ptuqv-aa2)", "--current-cefg-aa2)",
    './build_candidate "$CANDIDATE_MODE" p.xsm t.xsm t.xsm u.xsm',
    './check_candidate "$CANDIDATE_MODE" p.xsm t.xsm t.xsm u.xsm',
    "PARAMETER-FREE DIRECTION GATE PASS",
    "AA2-RAW-FLUX", "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in ptuqv_runner,
            f"PTUQV runner contract missing: {token}")
ptuqv_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", ptuqv_runner
)
require(ptuqv_expected == [
    "0be2f39496fb5de7f4c942ec2e249d484492218e1376a9331b3ec19e7427a2d0",
    "cdd6893892c5ba0140a3f5d3ce82bfef476c9a6537a939f41ecd53b2825e14e0",
], "PTUQV output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", ptuqv_runner),
        "PTUQV retry loop is forbidden")
require("spot-rank2-current-ptuqv-aa2-candidate" in makefile,
        "PTUQV Make target is missing")
for token in (
    "spot-rank2-current-cefg-aa2-candidate",
    "rank2_current_cefg_aa2_candidate_inputs.tsv",
    "iterative-rank2-current-cefg-aa2-candidate",
    "CANDIDATE_MODE=--current-cefg-aa2",
    "REPORT_PREFIX=RANK2-CURRENT-CEFG-AA2",
    "EXPECTED_AX_SHA_OVERRIDE=d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe",
    "EXPECTED_SNAP_SHA_OVERRIDE=b0aac9dd5575fc48ca351e0b330946afc968777152a6356f9846b5c9ac1b1c79",
):
    require(token in makefile, f"CEFG Make binding missing: {token}")

ptuqv_parent_rows = [line.split() for line in ptuqv_map_parent.splitlines()
                     if line.strip() and not line.startswith("#")]
require(ptuqv_map_parent.splitlines()[0] ==
        "# spot-rank2-current-ptuqv-aa2-map-parent-v1",
        "PTUQV map-parent version changed")
require(tuple(row[0] for row in ptuqv_parent_rows) == (
    "axial_track", "axial_macrolib", "radial_track", "basis_reference",
    "parent_axial", "parent_snapshots",
), "PTUQV map-parent roles changed")
require(tuple(row[1] for row in ptuqv_parent_rows[-2:]) == (
    "0be2f39496fb5de7f4c942ec2e249d484492218e1376a9331b3ec19e7427a2d0",
    "cdd6893892c5ba0140a3f5d3ce82bfef476c9a6537a939f41ecd53b2825e14e0",
), "PTUQV map parent proposal changed")
for token in (
    "RUN_RANK2_CURRENT_PTUQV_AA2_MAP=${RUN_RANK2_CURRENT_PTUQV_AA2_MAP:-0}",
    "iterative-rank2-current-ptuqv-aa2-candidate",
    "rank2_current_ptuqv_aa2_map_parent.tsv",
    "rank2_current_ptuqv_aa2_map_policy.md",
    "iterative-rank2-current-ptuqv-aa2-map",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in ptuqv_map_runner,
            f"PTUQV map runner contract missing: {token}")
require(ptuqv_map_runner.index("RUN_RANK2_CURRENT_PTUQV_AA2_MAP=") <
        ptuqv_map_runner.index("ROOT=$("),
        "PTUQV default-off gate must precede filesystem access")
require(ptuqv_map_runner.count("run_continuation_short.sh") == 1,
        "PTUQV map runner must delegate exactly once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", ptuqv_map_runner),
        "PTUQV map retry loop is forbidden")
require("spot-rank2-current-ptuqv-aa2-map" in makefile,
        "PTUQV map Make target is missing")
default_env = os.environ.copy()
default_env["RUN_RANK2_CURRENT_PTUQV_AA2_MAP"] = "0"
default_run = subprocess.run(
    ["sh", str(ptuqv_map_runner_path)], cwd=ROOT, env=default_env,
    capture_output=True, text=True, check=False,
)
require(default_run.returncode == 0 and
        default_run.stdout.strip() ==
        "SPOT-RANK2-CURRENT-PTUQV-AA2-MAP DEFAULT-OFF: no Dragon process started.",
        "PTUQV map default-off execution changed")

cefg_parent_rows = [line.split() for line in cefg_map_parent.splitlines()
                    if line.strip() and not line.startswith("#")]
require(cefg_map_parent.splitlines()[0] ==
        "# spot-rank2-current-cefg-aa2-map-parent-v1",
        "CEFG map-parent version changed")
require(tuple(row[0] for row in cefg_parent_rows) == (
    "axial_track", "axial_macrolib", "radial_track", "basis_reference",
    "parent_axial", "parent_snapshots",
), "CEFG map-parent roles changed")
require(tuple(row[1] for row in cefg_parent_rows[-2:]) == (
    "d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe",
    "b0aac9dd5575fc48ca351e0b330946afc968777152a6356f9846b5c9ac1b1c79",
), "CEFG map parent proposal changed")
for token in (
    "RUN_RANK2_CURRENT_CEFG_AA2_MAP=${RUN_RANK2_CURRENT_CEFG_AA2_MAP:-0}",
    "iterative-rank2-current-cefg-aa2-candidate",
    "rank2_current_cefg_aa2_map_parent.tsv",
    "rank2_current_cefg_aa2_map_policy.md",
    "iterative-rank2-current-cefg-aa2-map",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in cefg_map_runner,
            f"CEFG map runner contract missing: {token}")
require(cefg_map_runner.index("RUN_RANK2_CURRENT_CEFG_AA2_MAP=") <
        cefg_map_runner.index("ROOT=$("),
        "CEFG default-off gate must precede filesystem access")
require(cefg_map_runner.count("run_continuation_short.sh") == 1,
        "CEFG map runner must delegate exactly once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", cefg_map_runner),
        "CEFG map retry loop is forbidden")
for token in (
    "0.37059923635358261", "0.28970803656130206",
    "0.33969272708511533", "h=G_2(q_2)",
    "R_\\rho\\le5\\times10^{-7}", "R_L\\le5\\times10^{-7}",
    "R_a\\le5\\times10^{-7}", "h-q_2", "no second physical map",
):
    require(token in cefg_map_policy,
            f"CEFG map policy missing: {token}")
for token in (
    "1be7a4070d1083592e7e8f966e383ea44196c14a",
    "1.284469506313002", "4.808395175515263",
    "7.045164238661528", "1.190590942018258",
    "0.92198482219461153", "0.078015177805388483",
    "0.11971305975561962", "0.47525043616253554",
    "0.70441518119387303", "AA1_DIRECTION_PASS",
    "AA(2) is not calculated", "no second physical map",
):
    require(token in cefg_map_result,
            f"CEFG map result boundary missing: {token}")
require("spot-rank2-current-cefg-aa2-map" in makefile,
        "CEFG map Make target is missing")
cefg_default_env = os.environ.copy()
cefg_default_env["RUN_RANK2_CURRENT_CEFG_AA2_MAP"] = "0"
cefg_default_run = subprocess.run(
    ["sh", str(cefg_map_runner_path)], cwd=ROOT, env=cefg_default_env,
    capture_output=True, text=True, check=False,
)
require(cefg_default_run.returncode == 0 and
        cefg_default_run.stdout.strip() ==
        "SPOT-RANK2-CURRENT-CEFG-AA2-MAP DEFAULT-OFF: no Dragon process started.",
        "CEFG map default-off execution changed")

ghi_parent_rows = [line.split() for line in ghi_map_parent.splitlines()
                   if line.strip() and not line.startswith("#")]
require(ghi_map_parent.splitlines()[0] ==
        "# spot-rank2-current-ghi-aa2-map-parent-v1",
        "GHI map-parent version changed")
require(tuple(row[0] for row in ghi_parent_rows) == (
    "axial_track", "axial_macrolib", "radial_track", "basis_reference",
    "parent_axial", "parent_snapshots",
), "GHI map-parent roles changed")
require(tuple(row[1] for row in ghi_parent_rows[-2:]) == (
    "5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391",
    "d841554d9bb0b9e158dfda323ead4016c98c450387bb656416218f3b6d1d5548",
), "GHI map parent proposal changed")
for token in (
    "RUN_RANK2_CURRENT_GHI_AA2_MAP=${RUN_RANK2_CURRENT_GHI_AA2_MAP:-0}",
    "iterative-rank2-current-ghi-aa2-candidate",
    "rank2_current_ghi_aa2_map_parent.tsv",
    "rank2_current_ghi_aa2_map_policy.md",
    "iterative-rank2-current-ghi-aa2-map",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120", "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in ghi_map_runner,
            f"GHI map runner contract missing: {token}")
require(ghi_map_runner.index("RUN_RANK2_CURRENT_GHI_AA2_MAP=") <
        ghi_map_runner.index("ROOT=$("),
        "GHI default-off gate must precede filesystem access")
require(ghi_map_runner.count("run_continuation_short.sh") == 1,
        "GHI map runner must delegate exactly once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", ghi_map_runner),
        "GHI map retry loop is forbidden")
for token in (
    "0.54656692430484066", "0.22903224207636369",
    "0.22440083361879565", "7.9724244756408422e-26",
    "0.085602787687317231", "0.50064418931908561",
    "0.44048518991529284", "j=G_2(q_4)",
    "R_\\rho\\le5\\times10^{-7}", "R_L\\le5\\times10^{-7}",
    "R_a\\le5\\times10^{-7}", "j-q_4", "diagnostic only",
    "EXECUTED_ONCE_VALID_NOT_MET", "VALID_NOT_MET",
    "AA1_DIRECTION_PASS", "AA(2) is not calculated",
    "no second physical map",
):
    require(token in ghi_map_policy,
            f"GHI map policy missing: {token}")
for token in (
    "d78482590ca0d9be8078d15407a49b04bc5552dd",
    "6.422346976453497", "4.971869112913671",
    "7.284688763320446", "6.003808415562571",
    "1910e6d0c4bc413cda29713d7bb38191d5ab41ca6f1564f07a9a1a093e240f42",
    "ff2f7e2ab6fbd955212fdf337f318657757eb04e507a65bd4669cefe65d0d587",
    "b468c4381da4093d1055f51c320150faf0162f022942acde5611673c49588c1c",
    "1.1922339465680236", "0.19223394656802359",
    "1.1217162258501826e-11",
    "0.064424480296712869", "0.93186663298811390",
    "0.97357313211276764", "AA1_DIRECTION_PASS",
    "AA(2) is not calculated", "No durable",
    "no second physical map is run",
):
    require(token in ghi_map_result,
            f"GHI map result boundary missing: {token}")
require("spot-rank2-current-ghi-aa2-map" in makefile,
        "GHI map Make target is missing")
ghi_default_env = os.environ.copy()
ghi_default_env["RUN_RANK2_CURRENT_GHI_AA2_MAP"] = "0"
ghi_default_run = subprocess.run(
    ["sh", str(ghi_map_runner_path)], cwd=ROOT, env=ghi_default_env,
    capture_output=True, text=True, check=False,
)
require(ghi_default_run.returncode == 0 and
        ghi_default_run.stdout.strip() ==
        "SPOT-RANK2-CURRENT-GHI-AA2-MAP DEFAULT-OFF: no Dragon process started.",
        "GHI map default-off execution changed")

combined = "\n".join(
    (builder, checker, runner, next_runner, current_runner, ptuqv_runner,
     cefg_map_runner, ghi_map_runner)
).lower()
for forbidden in ("regularization", "pseudoinverse", "pinv", "condition cutoff"):
    require(forbidden not in combined, f"forbidden control present: {forbidden}")

print("RANK2 MODAL AA2 CONTRACT PASS: all three-residual windows use one "
      "exact 2x2 system, fixed rank two, the latest raw carrier and no map "
      "solve.")

#!/usr/bin/env python3
"""Seconds-scale static contract for one offline rank-2 AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa1_inputs.tsv").read_text()
next_manifest = (
    ITERATIVE / "rank2_modal_aa1_next_candidate_inputs.tsv"
).read_text()
u_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_candidate_inputs.tsv"
).read_text()
consecutive_manifest = (
    ITERATIVE / "rank2_modal_aa1_consecutive_candidate_inputs.tsv"
).read_text()
latest_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_candidate_inputs.tsv"
).read_text()
latest_next_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_next_candidate_inputs.tsv"
).read_text()
post_manifest = (
    ITERATIVE / "rank2_modal_aa1_post_candidate_inputs.tsv"
).read_text()
rolling_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_candidate_inputs.tsv"
).read_text()
rolling_next_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_next_candidate_inputs.tsv"
).read_text()
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa1_candidate.sh").read_text()
next_runner = (
    ITERATIVE / "run_rank2_modal_aa1_next_candidate.sh"
).read_text()
u_runner = (
    ITERATIVE / "run_rank2_modal_aa1_u_candidate.sh"
).read_text()
consecutive_runner = (
    ITERATIVE / "run_rank2_modal_aa1_consecutive_candidate.sh"
).read_text()
latest_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_candidate.sh"
).read_text()
latest_next_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_next_candidate.sh"
).read_text()
post_runner = (
    ITERATIVE / "run_rank2_modal_aa1_post_candidate.sh"
).read_text()
rolling_runner = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_candidate.sh"
).read_text()
rolling_next_runner = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_next_candidate.sh"
).read_text()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 MODAL AA1 CONTRACT FAIL: {message}")


rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = ("x0", "x1", "x2", "x2_snapshots", "basis_reference")
require(manifest.splitlines()[0] == "# spot-rank2-modal-aa1-inputs-v1",
        "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in rows),
        "manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and ".." not in Path(row[2]).parts
            for row in rows), "manifest path escapes the repository")

next_rows = [line.split() for line in next_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
next_roles = (
    "x1", "x2", "y_pub", "z", "z_snapshots", "basis_reference"
)
require(next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-next-candidate-inputs-v1",
        "next manifest version changed")
require(tuple(row[0] for row in next_rows) == next_roles,
        "next manifest roles changed")
require(all(len(row) == 3 for row in next_rows),
        "next manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in next_rows),
        "next manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in next_rows),
        "next manifest path escapes the repository")

u_rows = [line.split() for line in u_manifest.splitlines()
          if line.strip() and not line.startswith("#")]
u_roles = (
    "y_pub", "z", "w_pub", "v", "v_snapshots", "basis_reference"
)
require(u_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-u-candidate-inputs-v1",
        "u manifest version changed")
require(tuple(row[0] for row in u_rows) == u_roles,
        "u manifest roles changed")
require(all(len(row) == 3 for row in u_rows),
        "u manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in u_rows),
        "u manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in u_rows),
        "u manifest path escapes the repository")

consecutive_rows = [line.split() for line in consecutive_manifest.splitlines()
                    if line.strip() and not line.startswith("#")]
consecutive_roles = (
    "x1_pub", "x2", "x3", "x3_snapshots", "basis_reference"
)
require(consecutive_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-consecutive-candidate-inputs-v1",
        "consecutive manifest version changed")
require(tuple(row[0] for row in consecutive_rows) == consecutive_roles,
        "consecutive manifest roles changed")
require(all(len(row) == 3 for row in consecutive_rows),
        "consecutive manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in consecutive_rows),
        "consecutive manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in consecutive_rows),
        "consecutive manifest path escapes the repository")

latest_rows = [line.split() for line in latest_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
latest_roles = ("x2", "x3", "x4", "x4_snapshots", "basis_reference")
require(latest_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-candidate-inputs-v1",
        "latest manifest version changed")
require(tuple(row[0] for row in latest_rows) == latest_roles,
        "latest manifest roles changed")
require(all(len(row) == 3 for row in latest_rows),
        "latest manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in latest_rows),
        "latest manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_rows),
        "latest manifest path escapes the repository")
require(latest_rows[2][1] ==
        "ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08",
        "latest x4 AX changed")
require(latest_rows[3][1] ==
        "4b5deac64ec6ab50cd9c1c7a9e868f824bb2078895492eeb56c95863bd85e87a",
        "latest x4 snapshots changed")

latest_next_rows = [
    line.split() for line in latest_next_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
latest_next_roles = (
    "x3", "x4", "qy_pub", "z", "z_snapshots", "basis_reference"
)
require(latest_next_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-next-candidate-inputs-v1",
        "latest-next manifest version changed")
require(tuple(row[0] for row in latest_next_rows) == latest_next_roles,
        "latest-next manifest roles changed")
require(all(len(row) == 3 for row in latest_next_rows),
        "latest-next manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_next_rows),
        "latest-next manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_next_rows),
        "latest-next manifest path escapes the repository")
require(tuple(row[1] for row in latest_next_rows) == (
        "154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651",
        "ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08",
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9",
        "01d8fe5bc2556c1efa0931f72e69b727925589a3d2ad34aeac82c362b83d8647",
        "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        ), "latest-next parents changed")

post_rows = [line.split() for line in post_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
post_roles = (
    "x2", "x3", "aa1_pub", "aa1_plus", "aa1_plus_snapshots",
    "basis_reference",
)
require(post_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-post-candidate-inputs-v1",
        "post-AA1 manifest version changed")
require(tuple(row[0] for row in post_rows) == post_roles,
        "post-AA1 manifest roles changed")
require(all(len(row) == 3 for row in post_rows),
        "post-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in post_rows),
        "post-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in post_rows),
        "post-AA1 manifest path escapes the repository")

rolling_rows = [line.split() for line in rolling_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
rolling_roles = (
    "aa1_pub", "aa1_plus", "xnext_pub", "xnext_plus",
    "xnext_plus_snapshots", "basis_reference",
)
require(rolling_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-candidate-inputs-v1",
        "rolling-AA1 manifest version changed")
require(tuple(row[0] for row in rolling_rows) == rolling_roles,
        "rolling-AA1 manifest roles changed")
require(all(len(row) == 3 for row in rolling_rows),
        "rolling-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_rows),
        "rolling-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rolling_rows),
        "rolling-AA1 manifest path escapes the repository")

rolling_next_rows = [
    line.split() for line in rolling_next_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
rolling_next_roles = (
    "xnext_pub", "xnext_plus", "xroll_pub", "xroll_plus",
    "xroll_plus_snapshots", "basis_reference",
)
require(rolling_next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-next-candidate-inputs-v1",
        "rolling-next-AA1 manifest version changed")
require(tuple(row[0] for row in rolling_next_rows) == rolling_next_roles,
        "rolling-next-AA1 manifest roles changed")
require(all(len(row) == 3 for row in rolling_next_rows),
        "rolling-next-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_next_rows),
        "rolling-next-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rolling_next_rows),
        "rolling-next-AA1 manifest path escapes the repository")
require(rolling_next_rows[3][1] ==
        "dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2",
        "rolling-next-AA1 latest AX output changed")
require(rolling_next_rows[4][1] ==
        "ca57bdfb2f950aa24cf5a42edf9fe59883ccfa9221388fbc6aee8b76c94480fc",
        "rolling-next-AA1 latest snapshot output changed")

for token in (
    "denominator=update_sq(1)+update_sq(2)-2.0_real64*update_dot",
    "beta=(update_sq(1)-update_dot)/denominator",
    "candidate_a=weight1*x1%coordinates+beta*x2%coordinates",
    "candidate_l=weight1*x1%leakage+beta*x2%leakage",
    "published_l=real(candidate_l,real32)",
    "keff_public=real(1.0_real64/rho_star,real32)",
    "rho_public=1.0_real64/real(keff_public,real64)",
    "call LCMOP(staged_ax,' ',0,1,0)",
    "call LCMOP(staged_snap,' ',0,1,0)",
    "SPOT-X-STATE",
    "X2-RAW-FLUX",
):
    require(token in builder, f"builder contract missing: {token}")
for record in (
    "SPOT-X-RRHO", "SPOT-X-RLEAK", "SPOT-X-DLEAK", "SPOT-X-RA",
    "SPOT-X-PERP", "SPOT-X-EPOCH", "SPOT-GBAL", "SPOT-GBAL-MA",
):
    require(f"call delete_if_present(staged_ax,'{record}')" in builder,
            f"stale-record deletion missing: {record}")
for record in ("SPOT-L1-ERR", "SPOT-PJ-PERP", "SPOT-PROJECT"):
    require(f"call delete_if_present(staged_snap,'{record}')" in builder,
            f"snapshot stale-record deletion missing: {record}")
require("fluxes=LCMGID(staged_snap,'FLUX')" in builder,
        "snapshot FLUX publication is missing")
require("LCMGID(staged_snap,'SYSTEM')" not in builder,
        "builder must not rewrite lagged SYSTEM history")

for token in (
    "--next x1 x2 y z z_snap out_ax out_snap",
    "p_a=next_x2%coordinates(il)-next_x1%coordinates(il)",
    "q_a=next_z%coordinates(il)-next_y%coordinates(il)",
    "next_beta=(p_sq-p_dot)/next_denominator",
    "next_candidate_a=next_weight_x2*next_x2%coordinates+",
    "next_candidate_l=next_weight_x2*next_x2%leakage+",
    "next_rho_star=next_weight_x2*next_x2%rho+next_beta*next_z%rho",
    "call LCMEQU(next_z%root,next_staged_ax)",
    "call LCMEQU(next_z_snap,next_staged_snap)",
    "next_marker=output_carrier",
    "call validate_snapshot(trim(next_path(5)),next_y,next_z,next_z_snap)",
):
    require(token in builder, f"next builder contract missing: {token}")
require("LCMGID(next_staged_snap,'SYSTEM')" not in builder,
        "next builder must not rewrite lagged SYSTEM history")
for token in (
    "--u y z w v v_snap out_ax out_snap",
    "call build_next_candidate(.true.,.false.,.false.,.false.,.false.)",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='V-RAW-FLUX'",
    ".true.,'X2-RAW-FLUX'",
    "call load_state(trim(next_path(3)),next_y,'latest proposal input',",
    "call load_state(trim(next_path(4)),next_z,'latest returned output')",
):
    require(token in builder, f"u builder contract missing: {token}")
for token in (
    "--post-aa1 x2 x3 aa1 aa1p aa1p_snap out_ax out_snap",
    "call build_next_candidate(.false.,.true.,.false.,.false.,.false.)",
    "input_carrier='X3-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
    "report_prefix='RANK2-POST-AA1'",
    "latest_output='AA1-PLUS'",
    "previous_output='X3'",
):
    require(token in builder, f"post-AA1 builder contract missing: {token}")
for token in (
    "--rolling-aa1 aa1 aa1p xnext xnextp xnextp_snap",
    "call build_next_candidate(.false.,.false.,.true.,.false.,.false.)",
    "input_carrier='AA1-RAW-FLUX'",
    "output_carrier='XNP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL-AA1'",
    "latest_output='XNEXT-P'",
    "previous_output='AA1-PLUS'",
    ".true.,'X3-RAW-FLUX'",
):
    require(token in builder,
            f"rolling-AA1 builder contract missing: {token}")
for token in (
    "--rolling-aa1-next xnext xnextp xroll xrollp xrollp_snap",
    "call build_next_candidate(.false.,.false.,.false.,.true.,.false.)",
    "input_carrier='XNP-RAW-FLUX'",
    "output_carrier='XRP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL2-AA1'",
    "latest_output='XROLL-P'",
    "previous_output='XNEXT-P'",
    ".true.,'AA1-RAW-FLUX'",
):
    require(token in builder,
            f"rolling-next-AA1 builder contract missing: {token}")
for token in (
    "--next-x4 x3 x4 qy z z_snap out_ax out_snap",
    "call build_next_candidate(.false.,.false.,.false.,.false.,.true.)",
    "input_carrier='X4-RAW-FLUX'",
    "output_carrier='Z-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1-NEXT'",
    "latest_output='Z'",
    "previous_output='X4'",
):
    require(token in builder,
            f"latest-next builder contract missing: {token}")
for token in (
    "--consecutive x1_pub x2 x3 x3_snap out_ax out_snap",
    "call load_state(trim(path(1)),x0,'x1 proposal',.true.,'V-RAW-FLUX')",
    "carrier_marker='X3-RAW-FLUX'",
    "report_prefix='RANK2-CONSECUTIVE-AA1'",
):
    require(token in builder,
            f"consecutive builder contract missing: {token}")
for token in (
    "--consecutive-returned x2 x3 x4 x4_snap out_ax out_snap",
    "consecutive_returned_mode=.true.",
    "call load_state(trim(path(1)),x0,'x2 returned')",
    "carrier_marker='X4-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1'",
):
    require(token in builder,
            f"latest builder contract missing: {token}")

for token in (
    "expected_a=previous_weight*x1%coordinates+beta*x2%coordinates",
    "keff_published=real(1.0_real64/rho_affine,real32)",
    "expected_l32=real(previous_weight*x1%leakage+beta*x2%leakage,real32)",
    "call check_basis_reference",
    "call compare_axial_raw_flux",
    "call check_snapshot_publication",
    "call check_projected_positivity",
    "positive_count_expected=",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"independent checker missing: {token}")
for record in ("SPOT-X-PERP", "SPOT-GBAL", "SPOT-GBAL-MA"):
    require(f"call require_absent(root,'{record}',owner)" in checker,
            f"checker absence gate missing: {record}")
for record in ("SPOT-L1-ERR", "SPOT-PJ-PERP", "SPOT-PROJECT",
               "SPOT-R64"):
    require(f"call require_absent(proposal_root,'{record}'," in checker,
            f"snapshot checker absence gate missing: {record}")

for token in (
    "--next x1 x2 y z z_snap basis",
    "call modal_pair_geometry(state_x1,state_x2,state_y,state_z",
    "beta=(p_sq-p_dot_q)/denominator",
    "affine_a=weight_x2*state_x2%coordinates+beta*state_z%coordinates",
    "affine_l=weight_x2*state_x2%leakage+beta*state_z%leakage",
    "'Z-RAW-FLUX'",
    "call compare_axial_carrier_metadata(state_z,state_proposal,",
    "call validate_input_snapshot(z_snap_name,state_y,state_z,latest_input,",
    "FIXED-SOURCE K DIFFERS FROM",
    "call compare_snapshot_root_carrier(x2_root,proposal_root)",
    "call compare_table_except_leakage(x2_flux,proposal_flux",
    "call compare_named_record(carrier,proposal_root,name,length_left",
    "if (name /= 'SPOT-LEAK1D')",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"next checker contract missing: {token}")

for token in (
    "--u y z w v v_snap basis",
    "if (trim(mode_argument) == '--u')",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='V-RAW-FLUX'",
    "report_prefix='RANK2-MODAL-AA1-U'",
    "call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Y',",
    "call compare_axial_carrier_payload(z_name,proposal_name)",
    "count_table_records(proposal_root) /= expected_count",
    "V-RAW-FLUX",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"u checker contract missing: {token}")
for token in (
    "--next-x4 x3 x4 qy z z_snap basis",
    "x4_history_mode=.true.",
    "input_carrier='X4-RAW-FLUX'",
    "output_carrier='Z-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1-NEXT'",
    "latest_input='QY'",
    "latest_output='Z'",
    "previous_output='X4'",
    "'PREVIOUS MAP INPUT X3'",
):
    require(token in checker,
            f"latest-next checker contract missing: {token}")
for token in (
    "--consecutive x1_pub x2 x3",
    "call load_state(trim(path(1)),2,x0,'X1 PROPOSAL','V-RAW-FLUX')",
    "proposal_carrier='X3-RAW-FLUX'",
    "call validate_input_snapshot(trim(path(4)),x1,x2,'X2','X3')",
    "call compare_axial_carrier_payload(trim(path(3)),trim(path(6)))",
    "report_prefix='RANK2-CONSECUTIVE-AA1'",
):
    require(token in checker,
            f"consecutive checker contract missing: {token}")
for token in (
    "--consecutive-returned x2 x3 x4",
    "consecutive_returned_mode=.true.",
    "call load_state(trim(path(1)),1,x0,'X2 RETURNED')",
    "proposal_carrier='X4-RAW-FLUX'",
    "call validate_input_snapshot(trim(path(4)),x1,x2,'X3','X4')",
    "report_prefix='RANK2-LATEST-AA1'",
):
    require(token in checker,
            f"latest checker contract missing: {token}")
for token in (
    "--post-aa1 x2 x3 aa1 aa1p",
    "post_aa1_mode=.true.",
    "input_carrier='X3-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
    "report_prefix='RANK2-POST-AA1'",
    "latest_input='AA1'",
    "latest_output='AA1-PLUS'",
    "call load_state(x1_name,1,state_x1,'PREVIOUS MAP INPUT X2')",
):
    require(token in checker,
            f"post-AA1 checker contract missing: {token}")
for token in (
    "--rolling-aa1 aa1 aa1p xnext",
    "rolling_mode=.true.",
    "input_carrier='AA1-RAW-FLUX'",
    "output_carrier='XNP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL-AA1'",
    "latest_input='XNEXT'",
    "latest_output='XNEXT-P'",
    "previous_output='AA1-PLUS'",
    "'PREVIOUS PROPOSAL AA1'",
):
    require(token in checker,
            f"rolling-AA1 checker contract missing: {token}")
for token in (
    "trim(mode_argument) == '--rolling-aa1-next'",
    "rolling_next_mode=.true.",
    "input_carrier='XNP-RAW-FLUX'",
    "output_carrier='XRP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL2-AA1'",
    "latest_input='XROLL'",
    "latest_output='XROLL-P'",
    "previous_output='XNEXT-P'",
    "'PREVIOUS PROPOSAL XNEXT'",
):
    require(token in checker,
            f"rolling-next-AA1 checker contract missing: {token}")
for record in (
    "SPOT-X-RRHO", "SPOT-X-RLEAK", "SPOT-X-DLEAK", "SPOT-X-RA",
    "SPOT-X-PERP", "SPOT-X-EPOCH", "SPOT-GBAL", "SPOT-GBAL-MA",
):
    require(record in checker, f"u full-carrier stale gate missing: {record}")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_inputs.tsv",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in runner, f"runner binding missing: {name}")
expected = re.findall(r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", runner)
require(len(expected) == 2 and
        all(re.fullmatch(r"[0-9a-f]{64}", value) for value in expected),
        "output SHA-256 values are not frozen")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_next_candidate_inputs.tsv",
    "--next x1.xsm x2.xsm y_pub.xsm z.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in next_runner, f"next runner binding missing: {name}")
next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", next_runner
)
require(len(next_expected) == 2 and
        all(re.fullmatch(r"[0-9a-f]{64}", value)
            for value in next_expected),
        "next output SHA-256 values are not frozen")
require(not re.search(r"(?m)^\s*(?:while|until)\b", next_runner),
        "next runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_u_candidate_inputs.tsv",
    "--u y.xsm z.xsm w.xsm v.xsm vs.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in u_runner, f"u runner binding missing: {name}")
u_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", u_runner
)
require(u_expected == [
    "77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b",
    "2f526c84f4ef42afd51178dde9481ff7336c0de5b0ff486135635a0b7fc79a81",
], "u output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", u_runner),
        "u runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_consecutive_candidate_inputs.tsv",
    "--consecutive x1.xsm x2.xsm x3.xsm x3s.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in consecutive_runner,
            f"consecutive runner binding missing: {name}")
consecutive_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", consecutive_runner
)
require(consecutive_expected == [
    "7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1",
    "ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2",
], "consecutive output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", consecutive_runner),
        "consecutive runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_candidate_inputs.tsv",
    "--consecutive-returned",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in latest_runner, f"latest runner binding missing: {name}")
latest_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", latest_runner
)
require(latest_expected == [
    "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
    "b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b",
], "latest output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_runner),
        "latest runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-candidate" in
        (ROOT / "Makefile").read_text(), "latest Make target is missing")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_next_candidate_inputs.tsv",
    "--next-x4 x3.xsm x4.xsm qy_pub.xsm z.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in latest_next_runner,
            f"latest-next runner binding missing: {name}")
latest_next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", latest_next_runner
)
require(latest_next_expected == [
    "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
    "8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38",
], "latest-next output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_next_runner),
        "latest-next runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-next-candidate" in
        (ROOT / "Makefile").read_text(),
        "latest-next Make target is missing")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_post_candidate_inputs.tsv",
    "--post-aa1 x2.xsm x3.xsm aa1.xsm aa1p.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in post_runner, f"post-AA1 runner binding missing: {name}")
post_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", post_runner
)
require(post_expected == [
    "58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89",
    "0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c",
], "post-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", post_runner),
        "post-AA1 runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_rolling_candidate_inputs.tsv",
    "--rolling-aa1 aa1.xsm aa1p.xsm xnext.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in rolling_runner,
            f"rolling-AA1 runner binding missing: {name}")
rolling_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", rolling_runner
)
require(rolling_expected == [
    "a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee",
    "6762e58a75cc2bcbffae476187389797a9aebf95e8619355060b6de9c41b5102",
], "rolling-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", rolling_runner),
        "rolling-AA1 runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_rolling_next_candidate_inputs.tsv",
    "--rolling-aa1-next xnext.xsm xnextp.xsm xroll.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in rolling_next_runner,
            f"rolling-next-AA1 runner binding missing: {name}")
rolling_next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", rolling_next_runner
)
require(rolling_next_expected == [
    "5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394",
    "c27fee3d0d396c4427a7389c123b044a8ec61e274a6348b9f83343fb167313ee",
], "rolling-next-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", rolling_next_runner),
        "rolling-next-AA1 runner retry loops are forbidden")

combined = "\n".join((builder, checker, runner, next_runner,
                       u_runner, consecutive_runner, latest_runner,
                       latest_next_runner, post_runner, rolling_runner,
                       rolling_next_runner)).lower()
for forbidden in ("relaxation", "damping", "clipping", "empirical factor"):
    require(forbidden not in combined,
            f"forbidden empirical control present: {forbidden}")

print("RANK2 MODAL AA1 CONTRACT PASS: nine hash-locked offline proposals, "
      "binary publication, fixed basis, strict positivity and no map solve.")

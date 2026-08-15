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
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa1_candidate.sh").read_text()
next_runner = (
    ITERATIVE / "run_rank2_modal_aa1_next_candidate.sh"
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
    "next_marker='Z-RAW-FLUX'",
    "call validate_snapshot(trim(next_path(5)),next_y,next_z,next_z_snap)",
):
    require(token in builder, f"next builder contract missing: {token}")
require("LCMGID(next_staged_snap,'SYSTEM')" not in builder,
        "next builder must not rewrite lagged SYSTEM history")

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
    "call compare_axial_carrier_metadata(state_z,state_proposal)",
    "call validate_input_snapshot(z_snap_name,state_y,state_z)",
    "NEXT Z SNAPSHOT FIXED-SOURCE K DIFFERS FROM Y",
    "call compare_snapshot_root_carrier(x2_root,proposal_root)",
    "call compare_table_except_leakage(x2_flux,proposal_flux",
    "call compare_named_record(carrier,proposal_root,name,length_left",
    "if (name /= 'SPOT-LEAK1D')",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"next checker contract missing: {token}")

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

combined = "\n".join((builder, checker, runner, next_runner)).lower()
for forbidden in ("relaxation", "damping", "clipping", "empirical factor"):
    require(forbidden not in combined,
            f"forbidden empirical control present: {forbidden}")

print("RANK2 MODAL AA1 CONTRACT PASS: two hash-locked offline proposals, "
      "binary publication, fixed basis, strict positivity and no map solve.")

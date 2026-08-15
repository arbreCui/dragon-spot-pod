#!/usr/bin/env python3
"""Seconds-scale static contract for one offline rank-2 AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa1_inputs.tsv").read_text()
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa1_candidate.sh").read_text()


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

combined = "\n".join((builder, checker, runner)).lower()
for forbidden in ("relaxation", "damping", "clipping", "empirical factor"):
    require(forbidden not in combined,
            f"forbidden empirical control present: {forbidden}")

print("RANK2 MODAL AA1 CONTRACT PASS: one hash-locked offline proposal, "
      "binary publication, fixed basis, strict positivity and no map solve.")

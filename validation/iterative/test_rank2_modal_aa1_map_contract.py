#!/usr/bin/env python3
"""Seconds-scale static contract for one fresh map from the AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
runner = (ITERATIVE / "run_rank2_modal_aa1_map.sh").read_text()
common = (ITERATIVE / "run_continuation_short.sh").read_text()
checker = (ITERATIVE / "check_one_map_xsm.f90").read_text()
radial = (ITERATIVE / "continuation_rank2_continued_radial.x2m").read_text()
axial = (ITERATIVE / "continuation_axial.x2m").read_text()
policy = (ITERATIVE / "rank2_modal_aa1_map_policy.md").read_text()
manifest = (ITERATIVE / "rank2_modal_aa1_map_parent.tsv").read_text()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 MODAL AA1 MAP CONTRACT FAIL: {message}")


rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = ("axial_track", "axial_macrolib", "radial_track",
         "basis_reference", "parent_axial", "parent_snapshots")
require(manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-map-parent-v1", "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in rows),
        "manifest SHA-256 is invalid")
require(rows[4][1] ==
        "ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56",
        "proposal AX parent changed")
require(rows[5][1] ==
        "c11f4641897288f355ba60fa05eb7081d3aedfd8078333735d5c85c219f47c75",
        "proposal snapshot parent changed")

require(runner.index("RUN_RANK2_MODAL_AA1_MAP=") < runner.index("ROOT=$("),
        "default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_map_parent.tsv",
    "rank2_modal_aa1_map_policy.md",
    "continuation_rank2_continued_radial.x2m",
    "continuation_axial.x2m",
    "CHECKER_MODE=proposal",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in runner, f"runner binding missing: {token}")
require(runner.count("run_continuation_short.sh") == 1,
        "common host invocation count is not one")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loop is forbidden")

require("initial|continued|reencoded|proposal" in common,
        "common host does not accept proposal mode")
require("./check_one_map_xsm --proposal" in common,
        "proposal checker dispatch is missing")
for token in (
    "trim(mode) == '--proposal'",
    "MATERIALIZED PROPOSAL STATE",
    "SPOT-X-STATE",
    "X2-RAW-FLUX",
    "SPOT-X-PERP",
    "SPOT-GBAL-MA",
    "ONE-MAP-XSM MATERIALIZED-PROPOSAL INPUT PASS",
):
    require(token in checker, f"proposal checker contract missing: {token}")

rcompact = re.sub(r"\s+", " ", radial.upper())
acompact = re.sub(r"\s+", " ", axial.upper())
for token in ("SNAP := SPOPROJ:", "SNAP := SPOTREFFS",
              "SYSTEM_NEXT := ASM:"):
    require(token in rcompact, f"radial physical chain missing: {token}")
for token in ("AX_CURRENT := FLU:", "AX_CURRENT := SPOSTATE:",
              "AX_CURRENT := SPOXCONV:", "SNAP := SPOLEAK:"):
    require(token in acompact, f"axial physical chain missing: {token}")
for text in (runner, radial, axial):
    for forbidden in ("RELA", "ALPHA", "ANDERSON", "CMFD", "CLIP"):
        require(not re.search(rf"\b{forbidden}\b", text.upper()),
                f"empirical control present: {forbidden}")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in policy, f"classification missing: {label}")
require("starts no subsequent map" in policy,
        "automatic-stop boundary is missing")

print("RANK2 MODAL AA1 MAP CONTRACT PASS: one strict proposal map, "
      "fixed rank-2 physics, no retry and no empirical control.")

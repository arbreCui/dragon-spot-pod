#!/usr/bin/env python3
"""Seconds-scale contract for one continued rank-2 Picard map."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
radial = (ITERATIVE / "continuation_rank2_continued_radial.x2m").read_text()
axial = (ITERATIVE / "continuation_axial.x2m").read_text()
runner = (ITERATIVE / "run_rank2_next_map.sh").read_text()
common = (ITERATIVE / "run_continuation_short.sh").read_text()
manifest = (ITERATIVE / "rank2_next_parent.tsv").read_text()
policy = (ITERATIVE / "rank2_next_map_policy.md").read_text()


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.upper())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 NEXT MAP CONTRACT FAIL: {message}")


rcompact = compact(radial)
acompact = compact(axial)

radial_steps = (
    "SNAP := PARENT_SNAP",
    "TRACK := RECOVER: SNAP :: ITEM 3",
    "SNAP := SPOPROJ: SNAP PARENT_AX TRACK_AX :: FIXB",
    "SNAP := SPOTREFFS SNAP TRACK TRACK_F",
    "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF",
)
positions = [rcompact.find(step) for step in radial_steps]
require(all(position >= 0 for position in positions), "radial operator missing")
require(positions == sorted(positions), "radial operator order changed")
require(rcompact.count("SNAP := SPOTREFFS") == 1,
        "radial map call count is not one")
require("INTEGER SPOD_RANK := 2" in rcompact, "rank is not two")
require("REAL SOLVER_EPS := 5.0E-7" in rcompact,
        "radial tolerance changed")
require("SPOSTATE:" not in rcompact, "continued parent is re-encoded")

axial_steps = (
    "AX_CURRENT := FLU:",
    "AX_CURRENT := SPOGBAL:",
    "AX_CURRENT := SPOSTATE:",
    "AX_CURRENT := SPOXCONV:",
    "SNAP := SPOLEAK:",
)
positions = [acompact.find(step) for step in axial_steps]
require(all(position >= 0 for position in positions), "axial operator missing")
require(positions == sorted(positions), "axial operator order changed")
require("REAL SOLVER_EPS := 5.0E-7" in acompact,
        "axial tolerance changed")

for deck in (rcompact, acompact):
    for forbidden in ("RELA", "ALPHA", "ANDERSON", "CMFD", "CLIP"):
        require(not re.search(rf"\b{forbidden}\b", deck),
                f"forbidden control present: {forbidden}")

rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = ("axial_track", "axial_macrolib", "radial_track",
         "basis_reference", "parent_axial", "parent_snapshots")
require(manifest.splitlines()[0] == "# spot-rank2-next-parent-v1",
        "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(rows[4][1] ==
        "5ec5a3576fab3662cd5fabc18226d98e56fd9b936deabe6bd70a09623f596f61",
        "continued axial parent changed")
require(rows[5][1] ==
        "f9c0b78073ba6da05c5e5912b4e5c45045ac2506e72465a33c007b545a667d4c",
        "continued snapshot parent changed")

require(runner.index("RUN_RANK2_NEXT_MAP=") < runner.index("ROOT=$("),
        "default-off gate must precede repository access")
for token in (
    "rank2_next_parent.tsv",
    "rank2_next_map_policy.md",
    "continuation_rank2_continued_radial.x2m",
    "continuation_axial.x2m",
    "MAP_PARENT_FILE=parent_axial.xsm",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
):
    require(token in runner, f"wrapper binding missing: {token}")
require(runner.count("run_continuation_short.sh") == 1,
        "common host invocation count changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loop is forbidden")
require("DRAGON" not in runner.upper().split("ROOT=$(", 1)[1],
        "wrapper must not launch Dragon directly")

for token in (
    "RADIAL_TIMEOUT_SECONDS=${RADIAL_TIMEOUT_SECONDS:-120}",
    "AXIAL_TIMEOUT_SECONDS=${AXIAL_TIMEOUT_SECONDS:-80}",
    'run_bounded "$RADIAL_WORK/radial.x2m"',
    'run_bounded "$AXIAL_WORK/axial.x2m"',
    "./check_one_map_xsm --continued",
):
    require(token in common, f"common host contract missing: {token}")
require(not re.search(r"(?m)^\s*(?:while|until)\b", common),
        "common host contains a retry loop")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(policy.count(label) == 1, f"policy category changed: {label}")
require("No third rank-2\nmap is started automatically" in policy,
        "automatic-stop boundary missing")

print("RANK2 NEXT MAP CONTRACT PASS: one direct rank-2 continued map, "
      "fixed basis and tolerance, bounded once with no empirical control.")

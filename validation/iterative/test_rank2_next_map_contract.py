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
successor_runner = (
    ITERATIVE / "run_rank2_modal_aa2_rolling_next_picard_map.sh"
).read_text()
latest_runner = (
    ITERATIVE / "run_rank2_latest_picard_next_map.sh"
).read_text()
common = (ITERATIVE / "run_continuation_short.sh").read_text()
manifest = (ITERATIVE / "rank2_next_parent.tsv").read_text()
successor_manifest = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_picard_map_parent.tsv"
).read_text()
latest_manifest = (
    ITERATIVE / "rank2_latest_picard_next_map_parent.tsv"
).read_text()
policy = (ITERATIVE / "rank2_next_map_policy.md").read_text()
successor_policy = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_picard_map_policy.md"
).read_text()
latest_policy = (
    ITERATIVE / "rank2_latest_picard_next_map_policy.md"
).read_text()
checker = (ITERATIVE / "check_one_map_xsm.f90").read_text()


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

successor_rows = [
    line.split() for line in successor_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(successor_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa2-rolling-next-picard-map-parent-v1",
        "latest successor manifest version changed")
require(tuple(row[0] for row in successor_rows) == roles,
        "latest successor manifest roles changed")
require(all(len(row) == 3 for row in successor_rows),
        "latest successor manifest row width changed")
require(successor_rows[4][1] ==
        "21e5f4e8660020aee9509a656993c45049deb9a01029d86e63801432c948ab67",
        "latest returned axial parent changed")
require(successor_rows[5][1] ==
        "9c69da5c78d0c6a4a2b99eba54b23e9ce9869df5f142c2ed86c40859ba1176a8",
        "latest returned snapshot parent changed")

latest_rows = [
    line.split() for line in latest_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(latest_manifest.splitlines()[0] ==
        "# spot-rank2-latest-picard-next-map-parent-v1",
        "further Picard manifest version changed")
require(tuple(row[0] for row in latest_rows) == roles,
        "further Picard manifest roles changed")
require(all(len(row) == 3 for row in latest_rows),
        "further Picard manifest row width changed")
require(latest_rows[4][1] ==
        "154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651",
        "further Picard axial parent changed")
require(latest_rows[5][1] ==
        "0cf7d0a46ac84e5d94f9ed11d834c1d854f79c89eceea83c581fb1847e9bf911",
        "further Picard snapshot parent changed")

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

require(successor_runner.index(
        "RUN_RANK2_MODAL_AA2_ROLLING_NEXT_PICARD_MAP=") <
        successor_runner.index("ROOT=$("),
        "latest successor default-off gate must precede repository access")
for token in (
    "rank2_modal_aa2_rolling_next_picard_map_parent.tsv",
    "rank2_modal_aa2_rolling_next_picard_map_policy.md",
    "iterative-rank2-modal-aa2-rolling-next-map",
    "iterative-rank2-modal-aa2-rolling-next-picard-map",
    "VALID_NOT_MET",
    "shasum -a 256 -c result.sha256",
    "MAP_PARENT_FILE=parent_axial.xsm",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
):
    require(token in successor_runner,
            f"latest successor wrapper binding missing: {token}")
require(successor_runner.count("run_continuation_short.sh") == 1,
        "latest successor common host invocation count changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", successor_runner),
        "latest successor retry loop is forbidden")
require("DRAGON" not in
        successor_runner.upper().split("ROOT=$(", 1)[1],
        "latest successor wrapper must not launch Dragon directly")

require(latest_runner.index("RUN_RANK2_LATEST_PICARD_NEXT_MAP=") <
        latest_runner.index("ROOT=$("),
        "further Picard default-off gate must precede repository access")
for token in (
    "rank2_latest_picard_next_map_parent.tsv",
    "rank2_latest_picard_next_map_policy.md",
    "iterative-rank2-modal-aa2-rolling-next-picard-map",
    "iterative-rank2-latest-picard-next-map",
    "VALID_NOT_MET",
    "shasum -a 256 -c result.sha256",
    "MAP_PARENT_FILE=parent_axial.xsm",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
):
    require(token in latest_runner,
            f"further Picard wrapper binding missing: {token}")
require(latest_runner.count("run_continuation_short.sh") == 1,
        "further Picard common host invocation count changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_runner),
        "further Picard retry loop is forbidden")
require("DRAGON" not in latest_runner.upper().split("ROOT=$(", 1)[1],
        "further Picard wrapper must not launch Dragon directly")

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
for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in successor_policy,
            f"latest successor policy category missing: {label}")
require("PREPARED_NOT_RUN" in successor_policy,
        "latest successor policy overstates runtime completion")
require("starts no successor\nproposal or map" in successor_policy,
        "latest successor automatic-stop boundary missing")
for forbidden in ("relaxation", "damping", "Anderson mixing", "clipping",
                  "fitted closure", "regularization", "pseudoinverse",
                  "fallback", "empirical"):
    require(forbidden in successor_policy,
            f"latest successor forbidden-control boundary missing: {forbidden}")
for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in latest_policy,
            f"further Picard policy category missing: {label}")
require("PREPARED_NOT_RUN" in latest_policy,
        "further Picard policy overstates runtime completion")
require("starts no retry or further successor" in latest_policy,
        "further Picard automatic-stop boundary missing")
for forbidden in ("relaxation", "damping", "Anderson mixing", "clipping",
                  "fitted closure", "regularization", "pseudoinverse",
                  "fallback", "empirical"):
    require(forbidden in latest_policy,
            f"further Picard forbidden-control boundary missing: {forbidden}")
for token in (
    "--rank2-directions",
    "--proposal-aa2-directions",
    "proposal_state=.true.,aa2_carrier=.true.",
    "RANK2-DIRECTION MODE REQUIRES RANK TWO.",
    "MAP12 REENCODED-PARENT RAW-DEFECT BITWISE PASS",
    "MAP12 PROPOSAL-AA2-PARENT RAW-DEFECT BITWISE PASS",
    "MODE2-DIAGONAL GRAM-HEIGHT BASIS-DEPENDENT",
    "MODE2-DIAGONAL NORM-RATIO 23/12",
):
    require(token in checker, f"offline direction audit missing: {token}")

print("RANK2 NEXT MAP CONTRACT PASS: one direct rank-2 continued map, "
      "including the latest returned successor; fixed basis and tolerance, "
      "bounded once with no empirical control.")

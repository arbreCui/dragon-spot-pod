#!/usr/bin/env python3
"""Seconds-scale static contract for the single rank-2 sensitivity map."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
radial = (ITERATIVE / "continuation_rank2_radial.x2m").read_text()
axial = (ITERATIVE / "continuation_rank2_axial.x2m").read_text()
runner = (ITERATIVE / "run_rank2_map.sh").read_text()
common_runner = (ITERATIVE / "run_continuation_short.sh").read_text()
checker = (ITERATIVE / "check_one_map_xsm.f90").read_text()
manifest = (ITERATIVE / "rank2_parent.tsv").read_text()
policy = (ITERATIVE / "rank2_map_policy.md").read_text()


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.upper())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 MAP CONTRACT FAIL: {message}")


rcompact = compact(radial)
acompact = compact(axial)

radial_steps = (
    "PARENT_R2 := PARENT_AX",
    "PARENT_R2 := SPOSTATE: PARENT_R2 TRACK_AX BASIS_REF MACROLIB3",
    "SNAP := SPOPROJ: SNAP PARENT_R2 TRACK_AX :: FIXB",
    "SNAP := SPOTREFFS SNAP TRACK TRACK_F",
    "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF",
    "PARENT_R2 := SPOSTATE: PARENT_R2 TRACK_AX SYSTEM_NEXT MACROLIB3",
)
positions = [rcompact.find(step) for step in radial_steps]
require(all(position >= 0 for position in positions), "radial operator missing")
require(positions == sorted(positions), "radial operator order changed")
require(rcompact.count("PARENT_R2 := SPOSTATE:") == 2,
        "parent must be encoded before and after fixed assembly")
require(rcompact.count("SNAP := SPOTREFFS") == 1, "map call count is not one")
require("INTEGER SPOD_RANK := 2" in rcompact, "rank is not two")
require("SPOD <<SPOD_RANK>> FIXB" in rcompact, "fixed rank-2 assembly missing")
for record in ("SPOT-X-RRHO", "SPOT-X-RLEAK", "SPOT-X-DLEAK", "SPOT-X-RA"):
    require(rcompact.count(f"DEL '{record}'") == 1,
            f"stale parent record is not deleted exactly once: {record}")

axial_steps = (
    "AX_CURRENT := FLU:",
    "AX_CURRENT := SPOGBAL:",
    "AX_CURRENT := SPOSTATE:",
    "AX_CURRENT := SPOXCONV: AX_CURRENT PARENT_R2",
    "SNAP := SPOLEAK:",
)
positions = [acompact.find(step) for step in axial_steps]
require(all(position >= 0 for position in positions), "axial operator missing")
require(positions == sorted(positions), "axial operator order changed")
for step in axial_steps:
    require(acompact.count(step) == 1, f"axial operator count changed: {step}")

for deck in (rcompact, acompact):
    require("REAL SOLVER_EPS := 5.0E-7" in deck, "solver tolerance changed")
    for forbidden in ("RELA", "ALPHA", "ANDERSON", "CMFD", "CLIP"):
        require(not re.search(rf"\b{forbidden}\b", deck),
                f"forbidden control present: {forbidden}")

rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = ("axial_track", "axial_macrolib", "radial_track",
         "basis_reference", "parent_axial", "parent_snapshots")
require(manifest.splitlines()[0] == "# spot-rank2-map-parent-v1",
        "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(rows[3][1] ==
        "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        "rank-2 basis hash changed")

require(runner.index("RUN_RANK2_MAP=") < runner.index("ROOT=$("),
        "default-off gate must precede repository access")
for token in (
    "RUN_CONTINUATION=1",
    "rank2_parent.tsv",
    "rank2_map_policy.md",
    "continuation_rank2_radial.x2m",
    "continuation_rank2_axial.x2m",
    "MAP_PARENT_FILE=rank2_parent_axial.xsm",
    "CHECKER_MODE=reencoded",
):
    require(token in runner, f"wrapper binding missing: {token}")
require("DRAGON" not in runner.upper().split("ROOT=$(", 1)[1],
        "wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loop is forbidden")
require(common_runner.count('run_bounded "$RADIAL_WORK/radial.x2m"') == 1,
        "common runner radial launch count changed")
require(common_runner.count('run_bounded "$AXIAL_WORK/axial.x2m"') == 1,
        "common runner axial launch count changed")
require("RADIAL_TIMEOUT_SECONDS=${RADIAL_TIMEOUT_SECONDS:-120}" in common_runner,
        "default radial hard bound changed")
require("AXIAL_TIMEOUT_SECONDS=${AXIAL_TIMEOUT_SECONDS:-80}" in common_runner,
        "default axial hard bound changed")
require("./check_one_map_xsm --reencoded" in common_runner,
        "re-encoded parent checker route missing")
require("ncoef /= 1110" not in checker.lower(),
        "checker still hardcodes rank-1 coefficient count")
require("expected_ncoef=nsnap*sum(data%rank)" in checker.lower(),
        "checker does not derive coefficient count from rank")
require("--reencoded" in checker,
        "checker has no explicit re-encoded-parent mode")
for token in (
    "--mode2",
    "MODE2-DIAG RAW-PARENT RHO/NORM/LEAKAGE BITWISE PASS",
    "MODE2-DIAG GRAM FROM VOLUME/BASIS BITWISE PASS",
    "MODE2-DIAG R_A PRODUCTION-ORDER BITWISE PASS",
    "MODE2-DIAG OFFLINE_MODE2_ANATOMY_ONLY",
):
    require(token in checker, f"offline mode-2 audit token missing: {token}")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(policy.count(label) == 1, f"policy category changed: {label}")

print("RANK2 MAP CONTRACT PASS: same raw x7 is re-encoded before one rank-2 "
      "map; rank, basis, no-retry and no-empirical-control boundaries hold.")

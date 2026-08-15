#!/usr/bin/env python3
"""Seconds-scale static contract for the one rank-2 axial-only attempt."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
runner = (ITERATIVE / "run_rank2_axial_only.sh").read_text()
policy = (ITERATIVE / "rank2_axial_only_policy.md").read_text()
manifest = (ITERATIVE / "rank2_axial_only_parent.tsv").read_text()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RANK2 AXIAL-ONLY CONTRACT FAIL: {message}")


require(runner.index("RUN_RANK2_AXIAL_ONLY=") < runner.index("ROOT=$("),
        "default-off gate must precede repository access")
require("AXIAL_TIMEOUT_SECONDS=420" in runner,
        "the single operational wall bound changed")
require("radial_solve_count=0" in runner, "radial solve count is not zero")
require("axial_solve_count=1" in runner, "axial solve count is not one")
require("retry_count=0" in runner, "retry count is not zero")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner),
        "retry loops are forbidden")
require(runner.count("from run_bounded_dragon import run; run(") == 1,
        "bounded Dragon invocation count changed")
for forbidden in (
    "continuation_rank2_radial.x2m",
    "SpotRefFS",
    "SpotPlaneFS",
    "initial_radial_track.bin",
    "parent_snapshots.xsm",
):
    require(forbidden not in runner, f"radial dependency restored: {forbidden}")
require("shasum -a 256 -c staging.sha256" in runner,
        "full frozen staging receipt is not checked")
require("./check_one_map_xsm.bin --reencoded" in runner,
        "independent re-encoded-parent audit is missing")
for marker in (
    "FLU2DR-TERM OUTER-GATE=PASS",
    "FLU2DR-TERM INNER-TERMINAL",
    "normal end of execution for dragon",
    "CONT-RAW-DEFECT",
    "CONT-CANDIDATE",
    "CONT-AXIAL-COMPLETE",
):
    require(marker in runner, f"acceptance marker is missing: {marker}")
require("mv \"$WORK\" \"$RESULT_DIR\"" in runner,
        "successful result is not atomically published")
require("MAP_VALID=1" in runner and "INVALID_MAP" in runner,
        "validity/publication boundary is missing")

rows = [line.split() for line in manifest.splitlines()
        if line.strip() and not line.startswith("#")]
roles = (
    "staging_receipt",
    "runtime_provenance",
    "candidate_system",
    "candidate_radial",
    "rank2_parent",
    "axial_track",
    "axial_macrolib",
    "basis_reference",
    "axial_deck",
    "checker_source",
    "bounded_runner",
)
require(manifest.splitlines()[0] == "# spot-rank2-axial-only-parent-v1",
        "manifest version changed")
require(tuple(row[0] for row in rows) == roles, "manifest roles changed")
require(all(len(row) == 3 for row in rows), "manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in rows),
        "manifest contains an invalid SHA-256")

require("second, separately authorized operational attempt" in policy,
        "attempt boundary is missing")
require("does not alter or\nretroactively complete the first attempt" in policy,
        "first invalid attempt is being overwritten")
require("No radial equation is solved" in policy,
        "policy does not exclude a radial rerun")
require("420-second host wall bound" in policy,
        "policy wall bound differs from the runner")
for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in policy, f"classification is missing: {label}")
for forbidden in ("relaxation", "damping", "fitted closure", "clipping"):
    require(forbidden not in runner.lower(),
            f"forbidden empirical control present: {forbidden}")

print("RANK2 AXIAL-ONLY CONTRACT PASS: one frozen axial solve, 420-second "
      "host bound, strict audit, no radial rerun and no empirical control.")

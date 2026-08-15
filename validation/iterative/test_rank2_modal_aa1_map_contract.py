#!/usr/bin/env python3
"""Seconds-scale static contract for one fresh map from the AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
runner = (ITERATIVE / "run_rank2_modal_aa1_map.sh").read_text()
next_runner = (ITERATIVE / "run_rank2_modal_aa1_next_map.sh").read_text()
common = (ITERATIVE / "run_continuation_short.sh").read_text()
checker = (ITERATIVE / "check_one_map_xsm.f90").read_text()
radial = (ITERATIVE / "continuation_rank2_continued_radial.x2m").read_text()
axial = (ITERATIVE / "continuation_axial.x2m").read_text()
policy = (ITERATIVE / "rank2_modal_aa1_map_policy.md").read_text()
manifest = (ITERATIVE / "rank2_modal_aa1_map_parent.tsv").read_text()
next_policy = (
    ITERATIVE / "rank2_modal_aa1_next_map_policy.md"
).read_text()
next_manifest = (
    ITERATIVE / "rank2_modal_aa1_next_map_parent.tsv"
).read_text()
u_history_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_history.tsv"
).read_text()


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

next_rows = [line.split() for line in next_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
require(next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-next-map-parent-v1",
        "next-map manifest version changed")
require(tuple(row[0] for row in next_rows) == roles,
        "next-map manifest roles changed")
require(all(len(row) == 3 for row in next_rows),
        "next-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in next_rows),
        "next-map manifest SHA-256 is invalid")
require(next_rows[4][1] ==
        "c2df5e526aa9a0c0c3dc354d3ec539475814fe73c87af19ba04dde05c1475ff4",
        "next proposal AX parent changed")
require(next_rows[5][1] ==
        "530d23485baa006342b08815a9240d61fa4ec63810103307ead66104eb5bef9c",
        "next proposal snapshot parent changed")

u_rows = [line.split() for line in u_history_manifest.splitlines()
          if line.strip() and not line.startswith("#")]
require(u_history_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-u-history-v1",
        "u-history manifest version changed")
require(tuple(row[0] for row in u_rows) == ("y_pub", "z", "w_pub", "v"),
        "u-history roles changed")
require(all(len(row) == 3 for row in u_rows),
        "u-history manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in u_rows),
        "u-history SHA-256 is invalid")
require(tuple(row[1] for row in u_rows) == (
        "ae5f5b328fc6c5b181f40a4122b88771c857fd0200fc6e8351fc6b97d68d5c56",
        "a57feb6e83487561a153ae376874339c116192d0ece3d716cd10e2dac203376e",
        "c2df5e526aa9a0c0c3dc354d3ec539475814fe73c87af19ba04dde05c1475ff4",
        "02f922cf157a0dde1b9d072f45cdb1e39c64fa1f8682ad3a1e4fe21fede12a62",
        ), "u-history parents changed")

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

require(next_runner.index("RUN_RANK2_MODAL_AA1_NEXT_MAP=") <
        next_runner.index("ROOT=$("),
        "next-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_next_map_parent.tsv",
    "rank2_modal_aa1_next_map_policy.md",
    "iterative-rank2-modal-aa1-next-candidate",
    "CHECKER_MODE=proposal-z",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in next_runner, f"next-map runner binding missing: {token}")
require(next_runner.count("run_continuation_short.sh") == 1,
        "next-map common host invocation count is not one")
require(not re.search(r"(?m)^\s*(?:while|until)\b", next_runner),
        "next-map retry loop is forbidden")

require("initial|continued|reencoded|proposal|proposal-z" in common,
        "common host does not accept both proposal modes")
require("./check_one_map_xsm --proposal" in common,
        "proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-z" in common,
        "z-carrier proposal checker dispatch is missing")
require("--proposal-parent-z" in common,
        "z-carrier parent preflight is missing")
require(common.index("--proposal-parent-z") < common.index("MAP_STARTED=1"),
        "z-carrier parent preflight must precede map execution")
require("parent_preflight.log" in common,
        "parent preflight log is absent from the host receipt")
for token in (
    "trim(mode) == '--proposal'",
    "trim(mode) == '--proposal-z'",
    "trim(mode) == '--proposal-parent-z'",
    "MATERIALIZED PROPOSAL STATE",
    "SPOT-X-STATE",
    "X2-RAW-FLUX",
    "Z-RAW-FLUX",
    "RAW-FLUX CARRIER IS NOT X2",
    "RAW-FLUX CARRIER IS NOT Z",
    "SPOT-X-PERP",
    "SPOT-GBAL-MA",
    "ONE-MAP-XSM MATERIALIZED-PROPOSAL INPUT PASS",
    "ONE-MAP-XSM PROPOSAL-PARENT PRECHECK PASS",
):
    require(token in checker, f"proposal checker contract missing: {token}")
for token in (
    "--rank2-aa1-u-history",
    "AA1 NEXT HISTORY PROPOSAL Y",
    "AA1 NEXT HISTORY PROPOSAL W",
    "MAP-W-V RAW-DEFECT BITWISE PASS",
    "BETA WEIGHT-V",
    "NEXT-RAW-OUTPUT U=(1-BETA)*Z+BETA*V",
    "OFFLINE-HISTORY-ONLY NO-CANDIDATE NO-MAP NO-DRAGON",
):
    require(token in checker, f"u-history checker contract missing: {token}")
require("call require_absent(root,'SPOT-X-STATE',owner)" in checker,
        "returned state may retain the proposal lifecycle marker")
require("call require_absent(root,'SPOT-X-CARR',owner)" in checker,
        "returned state may retain the proposal carrier marker")

rcompact = re.sub(r"\s+", " ", radial.upper())
acompact = re.sub(r"\s+", " ", axial.upper())
for token in ("SNAP := SPOPROJ:", "SNAP := SPOTREFFS",
              "SYSTEM_NEXT := ASM:"):
    require(token in rcompact, f"radial physical chain missing: {token}")
for token in ("AX_CURRENT := FLU:", "AX_CURRENT := SPOSTATE:",
              "AX_CURRENT := SPOXCONV:", "SNAP := SPOLEAK:"):
    require(token in acompact, f"axial physical chain missing: {token}")
for text in (runner, next_runner, radial, axial):
    for forbidden in ("RELA", "ALPHA", "ANDERSON", "CMFD", "CLIP"):
        require(not re.search(rf"\b{forbidden}\b", text.upper()),
                f"empirical control present: {forbidden}")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in policy, f"classification missing: {label}")
require("starts no subsequent map" in policy,
        "automatic-stop boundary is missing")
for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in next_policy,
            f"next-map classification missing: {label}")
require("Z-RAW-FLUX" in next_policy,
        "next-map policy does not bind the z carrier")
require("PREPARED_NOT_RUN" in next_policy,
        "next-map policy overstates runtime completion")
require("starts no subsequent map" in next_policy,
        "next-map automatic-stop boundary is missing")

print("RANK2 MODAL AA1 MAP CONTRACT PASS: X2/Z proposal paths remain "
      "distinct; latest u-history is fixed rank-2, read-only and has no "
      "empirical control.")

#!/usr/bin/env python3
"""Seconds-scale static contract for one fresh map from the AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
runner = (ITERATIVE / "run_rank2_modal_aa1_map.sh").read_text()
next_runner = (ITERATIVE / "run_rank2_modal_aa1_next_map.sh").read_text()
u_runner = (ITERATIVE / "run_rank2_modal_aa1_u_map.sh").read_text()
consecutive_runner_path = (
    ITERATIVE / "run_rank2_modal_aa1_consecutive_map.sh"
)
consecutive_runner = consecutive_runner_path.read_text()
post_runner_path = ITERATIVE / "run_rank2_modal_aa1_post_map.sh"
post_runner = post_runner_path.read_text()
rolling_map_runner_path = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_map.sh"
)
rolling_map_runner = rolling_map_runner_path.read_text()
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
u_policy = (ITERATIVE / "rank2_modal_aa1_u_map_policy.md").read_text()
u_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_map_parent.tsv"
).read_text()
consecutive_policy = (
    ITERATIVE / "rank2_modal_aa1_consecutive_map_policy.md"
).read_text()
consecutive_manifest = (
    ITERATIVE / "rank2_modal_aa1_consecutive_map_parent.tsv"
).read_text()
post_policy = (ITERATIVE / "rank2_modal_aa1_post_map_policy.md").read_text()
post_manifest = (
    ITERATIVE / "rank2_modal_aa1_post_map_parent.tsv"
).read_text()
rolling_map_policy = (
    ITERATIVE / "rank2_modal_aa1_rolling_map_policy.md"
).read_text()
rolling_map_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_map_parent.tsv"
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

u_map_rows = [line.split() for line in u_manifest.splitlines()
              if line.strip() and not line.startswith("#")]
require(u_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-u-map-parent-v1",
        "u-map manifest version changed")
require(tuple(row[0] for row in u_map_rows) == roles,
        "u-map manifest roles changed")
require(all(len(row) == 3 for row in u_map_rows),
        "u-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in u_map_rows),
        "u-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in u_map_rows),
        "u-map manifest path escapes the repository")
require(u_map_rows[4][1] ==
        "77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b",
        "u proposal AX parent changed")
require(u_map_rows[5][1] ==
        "2f526c84f4ef42afd51178dde9481ff7336c0de5b0ff486135635a0b7fc79a81",
        "u proposal snapshot parent changed")

consecutive_rows = [line.split() for line in consecutive_manifest.splitlines()
                    if line.strip() and not line.startswith("#")]
require(consecutive_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-consecutive-map-parent-v1",
        "consecutive-map manifest version changed")
require(tuple(row[0] for row in consecutive_rows) == roles,
        "consecutive-map manifest roles changed")
require(all(len(row) == 3 for row in consecutive_rows),
        "consecutive-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in consecutive_rows),
        "consecutive-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in consecutive_rows),
        "consecutive-map manifest path escapes the repository")
require(consecutive_rows[4][1] ==
        "7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1",
        "consecutive proposal AX parent changed")
require(consecutive_rows[5][1] ==
        "ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2",
        "consecutive proposal snapshot parent changed")

post_rows = [line.split() for line in post_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
require(post_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-post-map-parent-v1",
        "post-map manifest version changed")
require(tuple(row[0] for row in post_rows) == roles,
        "post-map manifest roles changed")
require(all(len(row) == 3 for row in post_rows),
        "post-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in post_rows),
        "post-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in post_rows),
        "post-map manifest path escapes the repository")
require(post_rows[4][1] ==
        "58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89",
        "post-AA1 proposal AX parent changed")
require(post_rows[5][1] ==
        "0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c",
        "post-AA1 proposal snapshot parent changed")

rolling_map_rows = [line.split() for line in rolling_map_manifest.splitlines()
                    if line.strip() and not line.startswith("#")]
require(rolling_map_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-map-parent-v1",
        "rolling-map manifest version changed")
require(tuple(row[0] for row in rolling_map_rows) == roles,
        "rolling-map manifest roles changed")
require(all(len(row) == 3 for row in rolling_map_rows),
        "rolling-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_map_rows),
        "rolling-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rolling_map_rows),
        "rolling-map manifest path escapes the repository")
require(rolling_map_rows[4][1] ==
        "a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee",
        "rolling proposal AX parent changed")
require(rolling_map_rows[5][1] ==
        "6762e58a75cc2bcbffae476187389797a9aebf95e8619355060b6de9c41b5102",
        "rolling proposal snapshot parent changed")

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

require(u_runner.index("RUN_RANK2_MODAL_AA1_U_MAP=") <
        u_runner.index("ROOT=$("),
        "u-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_u_map_parent.tsv",
    "rank2_modal_aa1_u_map_policy.md",
    "iterative-rank2-modal-aa1-u-candidate",
    "CHECKER_MODE=proposal-v",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in u_runner, f"u-map runner binding missing: {token}")
require(u_runner.count("run_continuation_short.sh") == 1,
        "u-map common host invocation count is not one")
require(not re.search(r"(?m)^\s*(?:while|until)\b", u_runner),
        "u-map retry loop is forbidden")

require(consecutive_runner.index(
        "RUN_RANK2_MODAL_AA1_CONSECUTIVE_MAP=") <
        consecutive_runner.index("ROOT=$("),
        "consecutive-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_consecutive_map_parent.tsv",
    "rank2_modal_aa1_consecutive_map_policy.md",
    "iterative-rank2-modal-aa1-consecutive-candidate",
    "CHECKER_MODE=proposal-x3",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in consecutive_runner,
            f"consecutive-map runner binding missing: {token}")
require(consecutive_runner.count("run_continuation_short.sh") == 1,
        "consecutive-map common host invocation count is not one")
require("run_bounded_dragon.py" not in consecutive_runner and
        "DRAGON_BIN" not in consecutive_runner,
        "consecutive-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", consecutive_runner),
        "consecutive-map retry loop is forbidden")
default_off = subprocess.run(
    ["sh", str(consecutive_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_CONSECUTIVE_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(default_off.returncode == 0 and default_off.stderr == "" and
        default_off.stdout ==
        "SPOT-RANK2-MODAL-AA1-CONSECUTIVE-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "consecutive-map default-off terminal changed")
bad_activation = subprocess.run(
    ["sh", str(consecutive_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_CONSECUTIVE_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(bad_activation.returncode == 2 and bad_activation.stdout == "" and
        bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA1-CONSECUTIVE-MAP ERROR: activation must be "
        "0 or 1.\n",
        "consecutive-map activation gate changed")

require(post_runner.index("RUN_RANK2_MODAL_AA1_POST_MAP=") <
        post_runner.index("ROOT=$("),
        "post-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_post_map_parent.tsv",
    "rank2_modal_aa1_post_map_policy.md",
    "iterative-rank2-modal-aa1-post-candidate",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in post_runner, f"post-map runner binding missing: {token}")
require(post_runner.count("run_continuation_short.sh") == 1,
        "post-map common host invocation count is not one")
require("run_bounded_dragon.py" not in post_runner and
        "DRAGON_BIN" not in post_runner,
        "post-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", post_runner),
        "post-map retry loop is forbidden")
post_default_off = subprocess.run(
    ["sh", str(post_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_POST_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(post_default_off.returncode == 0 and
        post_default_off.stderr == "" and
        post_default_off.stdout ==
        "SPOT-RANK2-MODAL-AA1-POST-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "post-map default-off terminal changed")
post_bad_activation = subprocess.run(
    ["sh", str(post_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_POST_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(post_bad_activation.returncode == 2 and
        post_bad_activation.stdout == "" and
        post_bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA1-POST-MAP ERROR: activation must be 0 or 1.\n",
        "post-map activation gate changed")

require(rolling_map_runner.index(
        "RUN_RANK2_MODAL_AA1_ROLLING_MAP=") <
        rolling_map_runner.index("ROOT=$("),
        "rolling-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_rolling_map_parent.tsv",
    "rank2_modal_aa1_rolling_map_policy.md",
    "iterative-rank2-modal-aa1-rolling-candidate",
    "CHECKER_MODE=proposal-xnp",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in rolling_map_runner,
            f"rolling-map runner binding missing: {token}")
require(rolling_map_runner.count("run_continuation_short.sh") == 1,
        "rolling-map common host invocation count is not one")
require("run_bounded_dragon.py" not in rolling_map_runner and
        "DRAGON_BIN" not in rolling_map_runner,
        "rolling-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", rolling_map_runner),
        "rolling-map retry loop is forbidden")
rolling_default_off = subprocess.run(
    ["sh", str(rolling_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_ROLLING_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(rolling_default_off.returncode == 0 and
        rolling_default_off.stderr == "" and
        rolling_default_off.stdout ==
        "SPOT-RANK2-MODAL-AA1-ROLLING-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "rolling-map default-off terminal changed")
rolling_bad_activation = subprocess.run(
    ["sh", str(rolling_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_ROLLING_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(rolling_bad_activation.returncode == 2 and
        rolling_bad_activation.stdout == "" and
        rolling_bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA1-ROLLING-MAP ERROR: activation must be "
        "0 or 1.\n",
        "rolling-map activation gate changed")

require(
        "initial|continued|reencoded|proposal|proposal-z|proposal-v|"
        "proposal-x3|proposal-aa1|proposal-xnp" in common,
        "common host does not accept all proposal modes")
require("./check_one_map_xsm --proposal" in common,
        "proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-z" in common,
        "z-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-v" in common,
        "v-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-x3" in common,
        "x3-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-aa1" in common,
        "aa1-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-xnp" in common,
        "xnp-carrier proposal checker dispatch is missing")
require("--proposal-parent-z" in common,
        "z-carrier parent preflight is missing")
require("--proposal-parent-v" in common,
        "v-carrier parent preflight is missing")
require("--proposal-parent-x3" in common,
        "x3-carrier parent preflight is missing")
require("--proposal-parent-aa1" in common,
        "aa1-carrier parent preflight is missing")
require("--proposal-parent-xnp" in common,
        "xnp-carrier parent preflight is missing")
require(common.index("--proposal-parent-z") < common.index("MAP_STARTED=1"),
        "z-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-v") < common.index("MAP_STARTED=1"),
        "v-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-x3") <
        common.index("MAP_STARTED=1"),
        "x3-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-aa1") <
        common.index("MAP_STARTED=1"),
        "aa1-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-xnp") <
        common.index("MAP_STARTED=1"),
        "xnp-carrier parent preflight must precede map execution")
require("parent_preflight.log" in common,
        "parent preflight log is absent from the host receipt")
for token in (
    "trim(mode) == '--proposal'",
    "trim(mode) == '--proposal-z'",
    "trim(mode) == '--proposal-v'",
    "trim(mode) == '--proposal-x3'",
    "trim(mode) == '--proposal-aa1'",
    "trim(mode) == '--proposal-xnp'",
    "trim(mode) == '--proposal-parent-z'",
    "trim(mode) == '--proposal-parent-v'",
    "trim(mode) == '--proposal-parent-x3'",
    "trim(mode) == '--proposal-parent-aa1'",
    "trim(mode) == '--proposal-parent-xnp'",
    "MATERIALIZED PROPOSAL STATE",
    "SPOT-X-STATE",
    "X2-RAW-FLUX",
    "Z-RAW-FLUX",
    "V-RAW-FLUX",
    "X3-RAW-FLUX",
    "AA1-RAW-FLUX",
    "XNP-RAW-FLUX",
    "RAW-FLUX CARRIER IS NOT X2",
    "RAW-FLUX CARRIER IS NOT Z",
    "RAW-FLUX CARRIER IS NOT V",
    "RAW-FLUX CARRIER IS NOT X3",
    "RAW-FLUX CARRIER IS NOT AA1",
    "RAW-FLUX CARRIER IS NOT XNP",
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
for text in (runner, next_runner, u_runner, consecutive_runner, post_runner,
             rolling_map_runner, radial, axial):
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

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in u_policy,
            f"u-map classification missing: {label}")
require("V-RAW-FLUX" in u_policy,
        "u-map policy does not bind the v carrier")
require("PREPARED_NOT_RUN" in u_policy,
        "u-map policy overstates runtime completion")
require("starts no subsequent" in u_policy,
        "u-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in consecutive_policy,
            f"consecutive-map classification missing: {label}")
require("X3-RAW-FLUX" in consecutive_policy,
        "consecutive-map policy does not bind the x3 carrier")
require("PREPARED_NOT_RUN" in consecutive_policy,
        "consecutive-map policy overstates runtime completion")
require("starts no successor map" in consecutive_policy,
        "consecutive-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in post_policy,
            f"post-map classification missing: {label}")
require("AA1-RAW-FLUX" in post_policy,
        "post-map policy does not bind the AA1 carrier")
require("PREPARED_NOT_RUN" in post_policy,
        "post-map policy overstates runtime completion")
require("starts no successor map" in post_policy,
        "post-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in rolling_map_policy,
            f"rolling-map classification missing: {label}")
require("XNP-RAW-FLUX" in rolling_map_policy,
        "rolling-map policy does not bind the XNP carrier")
require("PREPARED_NOT_RUN" in rolling_map_policy,
        "rolling-map policy overstates runtime completion")
require("starts no successor proposal or map" in rolling_map_policy,
        "rolling-map automatic-stop boundary is missing")

print("RANK2 MODAL AA1 MAP CONTRACT PASS: X2/Z/V/X3/AA1/XNP proposal paths "
      "remain distinct; the XNP host is default-off, fixed rank-2 and has no "
      "empirical control.")

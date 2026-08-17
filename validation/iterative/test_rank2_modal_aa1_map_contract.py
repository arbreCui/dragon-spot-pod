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
latest_runner_path = ITERATIVE / "run_rank2_latest_modal_aa1_map.sh"
latest_runner = latest_runner_path.read_text()
latest_next_runner_path = (
    ITERATIVE / "run_rank2_latest_modal_aa1_next_map.sh"
)
latest_next_runner = latest_next_runner_path.read_text()
post_runner_path = ITERATIVE / "run_rank2_modal_aa1_post_map.sh"
post_runner = post_runner_path.read_text()
rolling_map_runner_path = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_map.sh"
)
rolling_map_runner = rolling_map_runner_path.read_text()
rolling_next_map_runner_path = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_next_map.sh"
)
rolling_next_map_runner = rolling_next_map_runner_path.read_text()
aa2_map_runner_path = ITERATIVE / "run_rank2_modal_aa2_map.sh"
aa2_map_runner = aa2_map_runner_path.read_text()
aa2_rolling_next_map_runner_path = (
    ITERATIVE / "run_rank2_modal_aa2_rolling_next_map.sh"
)
aa2_rolling_next_map_runner = aa2_rolling_next_map_runner_path.read_text()
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
latest_policy = (
    ITERATIVE / "rank2_latest_modal_aa1_map_policy.md"
).read_text()
latest_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_map_parent.tsv"
).read_text()
latest_next_policy = (
    ITERATIVE / "rank2_latest_modal_aa1_next_map_policy.md"
).read_text()
latest_next_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_next_map_parent.tsv"
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
rolling_next_map_policy = (
    ITERATIVE / "rank2_modal_aa1_rolling_next_map_policy.md"
).read_text()
rolling_next_map_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_next_map_parent.tsv"
).read_text()
aa2_map_policy = (ITERATIVE / "rank2_modal_aa2_map_policy.md").read_text()
aa2_map_manifest = (
    ITERATIVE / "rank2_modal_aa2_map_parent.tsv"
).read_text()
aa2_rolling_next_map_policy = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_map_policy.md"
).read_text()
aa2_rolling_next_map_manifest = (
    ITERATIVE / "rank2_modal_aa2_rolling_next_map_parent.tsv"
).read_text()
u_history_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_history.tsv"
).read_text()
latest_history_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_history.tsv"
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

latest_rows = [line.split() for line in latest_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(latest_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-map-parent-v1",
        "latest-map manifest version changed")
require(tuple(row[0] for row in latest_rows) == roles,
        "latest-map manifest roles changed")
require(all(len(row) == 3 for row in latest_rows),
        "latest-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_rows),
        "latest-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_rows),
        "latest-map manifest path escapes the repository")
require(latest_rows[4][1] ==
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "latest proposal AX parent changed")
require(latest_rows[5][1] ==
        "b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b",
        "latest proposal snapshot parent changed")

latest_next_rows = [
    line.split() for line in latest_next_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(latest_next_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-next-map-parent-v1",
        "latest-next-map manifest version changed")
require(tuple(row[0] for row in latest_next_rows) == roles,
        "latest-next-map manifest roles changed")
require(all(len(row) == 3 for row in latest_next_rows),
        "latest-next-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_next_rows),
        "latest-next-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_next_rows),
        "latest-next-map manifest path escapes the repository")
require(latest_next_rows[4][1] ==
        "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
        "latest-next proposal AX parent changed")
require(latest_next_rows[5][1] ==
        "8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38",
        "latest-next proposal snapshot parent changed")

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

rolling_next_map_rows = [
    line.split() for line in rolling_next_map_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(rolling_next_map_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-next-map-parent-v1",
        "rolling-next-map manifest version changed")
require(tuple(row[0] for row in rolling_next_map_rows) == roles,
        "rolling-next-map manifest roles changed")
require(all(len(row) == 3 for row in rolling_next_map_rows),
        "rolling-next-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_next_map_rows),
        "rolling-next-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts
            for row in rolling_next_map_rows),
        "rolling-next-map manifest path escapes the repository")
require(rolling_next_map_rows[4][1] ==
        "5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394",
        "rolling-next proposal AX parent changed")
require(rolling_next_map_rows[5][1] ==
        "c27fee3d0d396c4427a7389c123b044a8ec61e274a6348b9f83343fb167313ee",
        "rolling-next proposal snapshot parent changed")

aa2_map_rows = [line.split() for line in aa2_map_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
require(aa2_map_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa2-map-parent-v1",
        "AA2-map manifest version changed")
require(tuple(row[0] for row in aa2_map_rows) == roles,
        "AA2-map manifest roles changed")
require(all(len(row) == 3 for row in aa2_map_rows),
        "AA2-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in aa2_map_rows),
        "AA2-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in aa2_map_rows),
        "AA2-map manifest path escapes the repository")
require(aa2_map_rows[4][1] ==
        "aaa0d6afa2883f5eb528c26c466833454629160e2fd1b2f1a2e53a69168183ed",
        "AA2 proposal AX parent changed")
require(aa2_map_rows[5][1] ==
        "a6231acf84ed551e9144811c4bc775368c4a21132817ac757143a4c7e74d51dc",
        "AA2 proposal snapshot parent changed")

aa2_rolling_next_map_rows = [
    line.split() for line in aa2_rolling_next_map_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(aa2_rolling_next_map_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa2-rolling-next-map-parent-v1",
        "rolling-AA2-map manifest version changed")
require(tuple(row[0] for row in aa2_rolling_next_map_rows) == roles,
        "rolling-AA2-map manifest roles changed")
require(all(len(row) == 3 for row in aa2_rolling_next_map_rows),
        "rolling-AA2-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in aa2_rolling_next_map_rows),
        "rolling-AA2-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts
            for row in aa2_rolling_next_map_rows),
        "rolling-AA2-map manifest path escapes the repository")
require(aa2_rolling_next_map_rows[4][1] ==
        "ce9544e8f58b01d933f5937d781a0f1b70a58862468bbd380d5d2bc5c0e07715",
        "rolling-AA2 proposal AX parent changed")
require(aa2_rolling_next_map_rows[5][1] ==
        "61604c1dfb586abe71115544aa73b4628f7528f5da32f6bce14ce8f7f8f30763",
        "rolling-AA2 proposal snapshot parent changed")

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

latest_history_rows = [
    line.split() for line in latest_history_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(latest_history_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-history-v1",
        "latest-history manifest version changed")
require(tuple(row[0] for row in latest_history_rows) ==
        ("x3", "x4", "qy_pub", "z"),
        "latest-history roles changed")
require(all(len(row) == 3 for row in latest_history_rows),
        "latest-history manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_history_rows),
        "latest-history SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_history_rows),
        "latest-history manifest path escapes the repository")
require(tuple(row[1] for row in latest_history_rows) == (
        "154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651",
        "ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08",
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9",
        ), "latest-history parents changed")

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

require(latest_runner.index("RUN_RANK2_LATEST_MODAL_AA1_MAP=") <
        latest_runner.index("ROOT=$("),
        "latest-map default-off gate must precede repository access")
for token in (
    "rank2_latest_modal_aa1_map_parent.tsv",
    "rank2_latest_modal_aa1_map_policy.md",
    "iterative-rank2-latest-modal-aa1-candidate",
    "iterative-rank2-latest-modal-aa1-map",
    "CHECKER_MODE=proposal-x4",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in latest_runner,
            f"latest-map runner binding missing: {token}")
require(latest_runner.count("run_continuation_short.sh") == 1,
        "latest-map common host invocation count is not one")
require("run_bounded_dragon.py" not in latest_runner and
        "DRAGON_BIN" not in latest_runner,
        "latest-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_runner),
        "latest-map retry loop is forbidden")
latest_default_off = subprocess.run(
    ["sh", str(latest_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(latest_default_off.returncode == 0 and
        latest_default_off.stderr == "" and
        latest_default_off.stdout ==
        "SPOT-RANK2-LATEST-MODAL-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "latest-map default-off terminal changed")
latest_bad_activation = subprocess.run(
    ["sh", str(latest_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(latest_bad_activation.returncode == 2 and
        latest_bad_activation.stdout == "" and
        latest_bad_activation.stderr ==
        "SPOT-RANK2-LATEST-MODAL-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "latest-map activation gate changed")

require(latest_next_runner.index(
        "RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP=") <
        latest_next_runner.index("ROOT=$("),
        "latest-next-map default-off gate must precede repository access")
for token in (
    "rank2_latest_modal_aa1_next_map_parent.tsv",
    "rank2_latest_modal_aa1_next_map_policy.md",
    "iterative-rank2-latest-modal-aa1-next-candidate",
    "iterative-rank2-latest-modal-aa1-next-map",
    "CHECKER_MODE=proposal-z",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=80",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in latest_next_runner,
            f"latest-next-map runner binding missing: {token}")
require(latest_next_runner.count("run_continuation_short.sh") == 1,
        "latest-next-map common host invocation count is not one")
require("run_bounded_dragon.py" not in latest_next_runner and
        "DRAGON_BIN" not in latest_next_runner,
        "latest-next-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_next_runner),
        "latest-next-map retry loop is forbidden")
latest_next_default_off = subprocess.run(
    ["sh", str(latest_next_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(latest_next_default_off.returncode == 0 and
        latest_next_default_off.stderr == "" and
        latest_next_default_off.stdout ==
        "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "latest-next-map default-off terminal changed")
latest_next_bad_activation = subprocess.run(
    ["sh", str(latest_next_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(latest_next_bad_activation.returncode == 2 and
        latest_next_bad_activation.stdout == "" and
        latest_next_bad_activation.stderr ==
        "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP ERROR: activation must be "
        "0 or 1.\n",
        "latest-next-map activation gate changed")
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

require(rolling_next_map_runner.index(
        "RUN_RANK2_MODAL_AA1_ROLLING_NEXT_MAP=") <
        rolling_next_map_runner.index("ROOT=$("),
        "rolling-next-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa1_rolling_next_map_parent.tsv",
    "rank2_modal_aa1_rolling_next_map_policy.md",
    "iterative-rank2-modal-aa1-rolling-next-candidate",
    "CHECKER_MODE=proposal-xrp",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in rolling_next_map_runner,
            f"rolling-next-map runner binding missing: {token}")
require(rolling_next_map_runner.count("run_continuation_short.sh") == 1,
        "rolling-next-map common host invocation count is not one")
require("run_bounded_dragon.py" not in rolling_next_map_runner and
        "DRAGON_BIN" not in rolling_next_map_runner,
        "rolling-next-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b",
                      rolling_next_map_runner),
        "rolling-next-map retry loop is forbidden")
rolling_next_default_off = subprocess.run(
    ["sh", str(rolling_next_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_ROLLING_NEXT_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(rolling_next_default_off.returncode == 0 and
        rolling_next_default_off.stderr == "" and
        rolling_next_default_off.stdout ==
        "SPOT-RANK2-MODAL-AA1-ROLLING-NEXT-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "rolling-next-map default-off terminal changed")
rolling_next_bad_activation = subprocess.run(
    ["sh", str(rolling_next_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA1_ROLLING_NEXT_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(rolling_next_bad_activation.returncode == 2 and
        rolling_next_bad_activation.stdout == "" and
        rolling_next_bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA1-ROLLING-NEXT-MAP ERROR: activation must be "
        "0 or 1.\n",
        "rolling-next-map activation gate changed")

require(aa2_map_runner.index("RUN_RANK2_MODAL_AA2_MAP=") <
        aa2_map_runner.index("ROOT=$("),
        "AA2-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa2_map_parent.tsv",
    "rank2_modal_aa2_map_policy.md",
    "iterative-rank2-modal-aa2-candidate",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in aa2_map_runner,
            f"AA2-map runner binding missing: {token}")
require(aa2_map_runner.count("run_continuation_short.sh") == 1,
        "AA2-map common host invocation count is not one")
require("run_bounded_dragon.py" not in aa2_map_runner and
        "DRAGON_BIN" not in aa2_map_runner,
        "AA2-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", aa2_map_runner),
        "AA2-map retry loop is forbidden")
aa2_default_off = subprocess.run(
    ["sh", str(aa2_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA2_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(aa2_default_off.returncode == 0 and
        aa2_default_off.stderr == "" and
        aa2_default_off.stdout ==
        "SPOT-RANK2-MODAL-AA2-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "AA2-map default-off terminal changed")
aa2_bad_activation = subprocess.run(
    ["sh", str(aa2_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA2_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(aa2_bad_activation.returncode == 2 and
        aa2_bad_activation.stdout == "" and
        aa2_bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA2-MAP ERROR: activation must be 0 or 1.\n",
        "AA2-map activation gate changed")

require(aa2_rolling_next_map_runner.index(
        "RUN_RANK2_MODAL_AA2_ROLLING_NEXT_MAP=") <
        aa2_rolling_next_map_runner.index("ROOT=$("),
        "rolling-AA2-map default-off gate must precede repository access")
for token in (
    "rank2_modal_aa2_rolling_next_map_parent.tsv",
    "rank2_modal_aa2_rolling_next_map_policy.md",
    "iterative-rank2-modal-aa2-rolling-next-candidate",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in aa2_rolling_next_map_runner,
            f"rolling-AA2-map runner binding missing: {token}")
require(aa2_rolling_next_map_runner.count("run_continuation_short.sh") == 1,
        "rolling-AA2-map common host invocation count is not one")
require("run_bounded_dragon.py" not in aa2_rolling_next_map_runner and
        "DRAGON_BIN" not in aa2_rolling_next_map_runner,
        "rolling-AA2-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b",
                      aa2_rolling_next_map_runner),
        "rolling-AA2-map retry loop is forbidden")
aa2_rolling_next_default_off = subprocess.run(
    ["sh", str(aa2_rolling_next_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA2_ROLLING_NEXT_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(aa2_rolling_next_default_off.returncode == 0 and
        aa2_rolling_next_default_off.stderr == "" and
        aa2_rolling_next_default_off.stdout ==
        "SPOT-RANK2-MODAL-AA2-ROLLING-NEXT-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "rolling-AA2-map default-off terminal changed")
aa2_rolling_next_bad_activation = subprocess.run(
    ["sh", str(aa2_rolling_next_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_MODAL_AA2_ROLLING_NEXT_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(aa2_rolling_next_bad_activation.returncode == 2 and
        aa2_rolling_next_bad_activation.stdout == "" and
        aa2_rolling_next_bad_activation.stderr ==
        "SPOT-RANK2-MODAL-AA2-ROLLING-NEXT-MAP ERROR: activation must be "
        "0 or 1.\n",
        "rolling-AA2-map activation gate changed")

require(
        "initial|continued|reencoded|proposal|proposal-z|proposal-v|"
        "proposal-x3|proposal-x4|proposal-aa1|proposal-xnp|proposal-xrp|"
        "proposal-aa2"
        in common,
        "common host does not accept all proposal modes")
require("./check_one_map_xsm --proposal" in common,
        "proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-z" in common,
        "z-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-v" in common,
        "v-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-x3" in common,
        "x3-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-x4" in common,
        "x4-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-aa1" in common,
        "aa1-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-xnp" in common,
        "xnp-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-xrp" in common,
        "xrp-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-aa2" in common,
        "AA2-carrier proposal checker dispatch is missing")
require("--proposal-parent-z" in common,
        "z-carrier parent preflight is missing")
require("--proposal-parent-v" in common,
        "v-carrier parent preflight is missing")
require("--proposal-parent-x3" in common,
        "x3-carrier parent preflight is missing")
require("--proposal-parent-x4" in common,
        "x4-carrier parent preflight is missing")
require("--proposal-parent-aa1" in common,
        "aa1-carrier parent preflight is missing")
require("--proposal-parent-xnp" in common,
        "xnp-carrier parent preflight is missing")
require("--proposal-parent-xrp" in common,
        "xrp-carrier parent preflight is missing")
require("--proposal-parent-aa2" in common,
        "AA2-carrier parent preflight is missing")
require(common.index("--proposal-parent-z") < common.index("MAP_STARTED=1"),
        "z-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-v") < common.index("MAP_STARTED=1"),
        "v-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-x3") <
        common.index("MAP_STARTED=1"),
        "x3-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-x4") <
        common.index("MAP_STARTED=1"),
        "x4-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-aa1") <
        common.index("MAP_STARTED=1"),
        "aa1-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-xnp") <
        common.index("MAP_STARTED=1"),
        "xnp-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-xrp") <
        common.index("MAP_STARTED=1"),
        "xrp-carrier parent preflight must precede map execution")
require(common.index("--proposal-parent-aa2") <
        common.index("MAP_STARTED=1"),
        "AA2-carrier parent preflight must precede map execution")
require("parent_preflight.log" in common,
        "parent preflight log is absent from the host receipt")
for token in (
    "trim(mode) == '--proposal'",
    "trim(mode) == '--proposal-z'",
    "trim(mode) == '--proposal-v'",
    "trim(mode) == '--proposal-x3'",
    "trim(mode) == '--proposal-x4'",
    "trim(mode) == '--proposal-aa1'",
    "trim(mode) == '--proposal-xnp'",
    "trim(mode) == '--proposal-xrp'",
    "trim(mode) == '--proposal-aa2'",
    "trim(mode) == '--proposal-parent-z'",
    "trim(mode) == '--proposal-parent-v'",
    "trim(mode) == '--proposal-parent-x3'",
    "trim(mode) == '--proposal-parent-x4'",
    "trim(mode) == '--proposal-parent-aa1'",
    "trim(mode) == '--proposal-parent-xnp'",
    "trim(mode) == '--proposal-parent-xrp'",
    "trim(mode) == '--proposal-parent-aa2'",
    "MATERIALIZED PROPOSAL STATE",
    "SPOT-X-STATE",
    "X2-RAW-FLUX",
    "Z-RAW-FLUX",
    "V-RAW-FLUX",
    "X3-RAW-FLUX",
    "X4-RAW-FLUX",
    "AA1-RAW-FLUX",
    "XNP-RAW-FLUX",
    "XRP-RAW-FLUX",
    "AA2-RAW-FLUX",
    "RAW-FLUX CARRIER IS NOT X2",
    "RAW-FLUX CARRIER IS NOT Z",
    "RAW-FLUX CARRIER IS NOT V",
    "RAW-FLUX CARRIER IS NOT X3",
    "RAW-FLUX CARRIER IS NOT X4",
    "RAW-FLUX CARRIER IS NOT AA1",
    "RAW-FLUX CARRIER IS NOT XNP",
    "RAW-FLUX CARRIER IS NOT XRP",
    "RAW-FLUX CARRIER IS NOT AA2",
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
for token in (
    "--rank2-aa1-x4-history",
    "MAP-X3-X4 RAW-DEFECT BITWISE PASS",
    "MAP-QY-Z RAW-DEFECT BITWISE PASS",
    "PROPOSAL-QY-TO-RETURNED-Z",
    "WEIGHT-X4",
    "LEAKAGE AFFINE-D_L/CURRENT",
    "LEAKAGE SAME-BETA SCREEN ONLY NO LEAKAGE FIT",
    "NEXT-RAW-OUTPUT (1-BETA)*X4+BETA*Z",
    "OFFLINE_DECISION_ONLY_NO_AUTHORIZATION",
):
    require(token in checker,
            f"latest-history checker contract missing: {token}")
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
for text in (runner, next_runner, u_runner, consecutive_runner, latest_runner,
             latest_next_runner, post_runner,
             rolling_map_runner, rolling_next_map_runner, radial, axial):
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
    require(label in latest_policy,
            f"latest-map classification missing: {label}")
require("X4-RAW-FLUX" in latest_policy,
        "latest-map policy does not bind the x4 carrier")
require("PREPARED_NOT_RUN" in latest_policy,
        "latest-map policy overstates runtime completion")
require("successor map" in latest_policy,
        "latest-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in latest_next_policy,
            f"latest-next-map classification missing: {label}")
require("Z-RAW-FLUX" in latest_next_policy,
        "latest-next-map policy does not bind the z carrier")
require("PREPARED_NOT_RUN" in latest_next_policy,
        "latest-next-map policy overstates runtime completion")
require("successor map" in latest_next_policy,
        "latest-next-map automatic-stop boundary is missing")

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

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in rolling_next_map_policy,
            f"rolling-next-map classification missing: {label}")
require("XRP-RAW-FLUX" in rolling_next_map_policy,
        "rolling-next-map policy does not bind the XRP carrier")
require("PREPARED_NOT_RUN" in rolling_next_map_policy,
        "rolling-next-map policy overstates runtime completion")
require("starts no successor proposal, AA(2) or" in rolling_next_map_policy,
        "rolling-next-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in aa2_map_policy,
            f"AA2-map classification missing: {label}")
require("AA2-RAW-FLUX" in aa2_map_policy,
        "AA2-map policy does not bind the AA2 carrier")
require("PREPARED_NOT_RUN" in aa2_map_policy,
        "AA2-map policy overstates runtime completion")
require("starts no successor proposal or map" in aa2_map_policy,
        "AA2-map automatic-stop boundary is missing")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in aa2_rolling_next_map_policy,
            f"rolling-AA2-map classification missing: {label}")
require("AA2-RAW-FLUX" in aa2_rolling_next_map_policy,
        "rolling-AA2-map policy does not bind the AA2 carrier")
require("PREPARED_NOT_RUN" in aa2_rolling_next_map_policy,
        "rolling-AA2-map policy overstates runtime completion")
require("starts no successor proposal or map" in
        aa2_rolling_next_map_policy,
        "rolling-AA2-map automatic-stop boundary is missing")

print("RANK2 MODAL AA1 MAP CONTRACT PASS: "
      "X2/Z/V/X3/X4/AA1/XNP/XRP/AA2 proposal paths remain distinct; "
      "all hosts are default-off, fixed rank-2 and have no empirical "
      "control.")

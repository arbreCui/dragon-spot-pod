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
latest_next_recovery_runner_path = (
    ITERATIVE / "run_rank2_latest_modal_aa1_next_map_recovery.sh"
)
latest_next_recovery_runner = latest_next_recovery_runner_path.read_text()
latest_recovery_runner_path = (
    ITERATIVE / "run_rank2_latest_modal_aa1_recovery_map.sh"
)
latest_recovery_runner = latest_recovery_runner_path.read_text()
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
current_aa2_map_runner_path = (
    ITERATIVE / "run_rank2_current_aa2_map.sh"
)
current_aa2_map_runner = current_aa2_map_runner_path.read_text()
qvwx_map_runner_path = (
    ITERATIVE / "run_rank2_current_qvwx_aa1_map.sh"
)
qvwx_map_runner = qvwx_map_runner_path.read_text()
qvwx_z_picard_runner_path = (
    ITERATIVE / "run_rank2_current_qvwx_z_picard_map.sh"
)
qvwx_z_picard_runner = qvwx_z_picard_runner_path.read_text()
qvwx_zplus_map_runner_path = (
    ITERATIVE / "run_rank2_current_qvwx_zplus_aa1_map.sh"
)
qvwx_zplus_map_runner = qvwx_zplus_map_runner_path.read_text()
zpcd_map_runner_path = (
    ITERATIVE / "run_rank2_current_zpcd_aa1_map.sh"
)
zpcd_map_runner = zpcd_map_runner_path.read_text()
zpcd_e_picard_runner_path = (
    ITERATIVE / "run_rank2_current_zpcd_e_picard_map.sh"
)
zpcd_e_picard_runner = zpcd_e_picard_runner_path.read_text()
cef_map_runner_path = (
    ITERATIVE / "run_rank2_current_cef_aa1_map.sh"
)
cef_map_runner = cef_map_runner_path.read_text()
gh_map_runner_path = (
    ITERATIVE / "run_rank2_current_gh_aa1_map.sh"
)
gh_map_runner = gh_map_runner_path.read_text()
ij_map_runner_path = (
    ITERATIVE / "run_rank2_current_ij_aa1_map.sh"
)
ij_map_runner = ij_map_runner_path.read_text()
k_picard_runner_path = (
    ITERATIVE / "run_rank2_current_k_picard_map.sh"
)
k_picard_runner = k_picard_runner_path.read_text()
kl_map_runner_path = (
    ITERATIVE / "run_rank2_current_kl_aa1_map.sh"
)
kl_map_runner = kl_map_runner_path.read_text()
klm_map_runner_path = (
    ITERATIVE / "run_rank2_current_klm_aa1_map.sh"
)
klm_map_runner = klm_map_runner_path.read_text()
no_map_runner_path = ITERATIVE / "run_rank2_current_no_aa1_map.sh"
no_map_runner = no_map_runner_path.read_text()
op_map_runner_path = ITERATIVE / "run_rank2_current_op_aa1_map.sh"
op_map_runner = op_map_runner_path.read_text()
pr_map_runner_path = ITERATIVE / "run_rank2_current_pr_aa1_map.sh"
pr_map_runner = pr_map_runner_path.read_text()
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
latest_next_attempt_result = (
    ITERATIVE / "rank2_latest_modal_aa1_next_map_attempt_result.md"
).read_text()
latest_next_recovery_policy = (
    ITERATIVE / "rank2_latest_modal_aa1_next_map_recovery_policy.md"
).read_text()
latest_next_recovery_result = (
    ITERATIVE / "rank2_latest_modal_aa1_next_map_recovery_result.md"
).read_text()
latest_recovery_policy = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_map_policy.md"
).read_text()
latest_recovery_result = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_map_result.md"
).read_text()
latest_recovery_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_map_parent.tsv"
).read_text()
recovery_history_result = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_history_result.md"
).read_text()
qv_history_result = (
    ITERATIVE / "rank2_latest_modal_aa1_qv_history_result.md"
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
current_aa2_map_policy = (
    ITERATIVE / "rank2_current_aa2_map_policy.md"
).read_text()
current_aa2_map_manifest = (
    ITERATIVE / "rank2_current_aa2_map_parent.tsv"
).read_text()
current_aa2_map_result = (
    ITERATIVE / "rank2_current_aa2_map_result.md"
).read_text()
qvwx_map_policy = (
    ITERATIVE / "rank2_current_qvwx_aa1_map_policy.md"
).read_text()
qvwx_map_manifest = (
    ITERATIVE / "rank2_current_qvwx_aa1_map_parent.tsv"
).read_text()
qvwx_map_result = (
    ITERATIVE / "rank2_current_qvwx_aa1_map_result.md"
).read_text()
qvwx_z_picard_policy = (
    ITERATIVE / "rank2_current_qvwx_z_picard_map_policy.md"
).read_text()
qvwx_z_picard_manifest = (
    ITERATIVE / "rank2_current_qvwx_z_picard_map_parent.tsv"
).read_text()
qvwx_z_picard_result = (
    ITERATIVE / "rank2_current_qvwx_z_picard_map_result.md"
).read_text()
qvwx_zplus_map_policy = (
    ITERATIVE / "rank2_current_qvwx_zplus_aa1_map_policy.md"
).read_text()
qvwx_zplus_map_manifest = (
    ITERATIVE / "rank2_current_qvwx_zplus_aa1_map_parent.tsv"
).read_text()
qvwx_zplus_map_result = (
    ITERATIVE / "rank2_current_qvwx_zplus_aa1_map_result.md"
).read_text()
zpcd_map_policy = (
    ITERATIVE / "rank2_current_zpcd_aa1_map_policy.md"
).read_text()
zpcd_map_manifest = (
    ITERATIVE / "rank2_current_zpcd_aa1_map_parent.tsv"
).read_text()
zpcd_map_result = (
    ITERATIVE / "rank2_current_zpcd_aa1_map_result.md"
).read_text()
zpcd_e_picard_policy = (
    ITERATIVE / "rank2_current_zpcd_e_picard_map_policy.md"
).read_text()
zpcd_e_picard_manifest = (
    ITERATIVE / "rank2_current_zpcd_e_picard_map_parent.tsv"
).read_text()
zpcd_e_picard_result = (
    ITERATIVE / "rank2_current_zpcd_e_picard_map_result.md"
).read_text()
cef_map_policy = (
    ITERATIVE / "rank2_current_cef_aa1_map_policy.md"
).read_text()
cef_map_manifest = (
    ITERATIVE / "rank2_current_cef_aa1_map_parent.tsv"
).read_text()
cef_map_result = (
    ITERATIVE / "rank2_current_cef_aa1_map_result.md"
).read_text()
gh_map_policy = (
    ITERATIVE / "rank2_current_gh_aa1_map_policy.md"
).read_text()
gh_map_manifest = (
    ITERATIVE / "rank2_current_gh_aa1_map_parent.tsv"
).read_text()
gh_map_result = (
    ITERATIVE / "rank2_current_gh_aa1_map_result.md"
).read_text()
ij_map_policy = (
    ITERATIVE / "rank2_current_ij_aa1_map_policy.md"
).read_text()
ij_map_manifest = (
    ITERATIVE / "rank2_current_ij_aa1_map_parent.tsv"
).read_text()
ij_map_result = (
    ITERATIVE / "rank2_current_ij_aa1_map_result.md"
).read_text()
k_picard_policy = (
    ITERATIVE / "rank2_current_k_picard_map_policy.md"
).read_text()
k_picard_manifest = (
    ITERATIVE / "rank2_current_k_picard_map_parent.tsv"
).read_text()
k_picard_result = (
    ITERATIVE / "rank2_current_k_picard_map_result.md"
).read_text()
kl_map_policy = (
    ITERATIVE / "rank2_current_kl_aa1_map_policy.md"
).read_text()
kl_map_manifest = (
    ITERATIVE / "rank2_current_kl_aa1_map_parent.tsv"
).read_text()
kl_map_result = (
    ITERATIVE / "rank2_current_kl_aa1_map_result.md"
).read_text()
klm_map_policy = (
    ITERATIVE / "rank2_current_klm_aa1_map_policy.md"
).read_text()
klm_map_manifest = (
    ITERATIVE / "rank2_current_klm_aa1_map_parent.tsv"
).read_text()
klm_map_result = (
    ITERATIVE / "rank2_current_klm_aa1_map_result.md"
).read_text()
no_map_policy = (
    ITERATIVE / "rank2_current_no_aa1_map_policy.md"
).read_text()
no_map_manifest = (
    ITERATIVE / "rank2_current_no_aa1_map_parent.tsv"
).read_text()
no_map_result = (
    ITERATIVE / "rank2_current_no_aa1_map_result.md"
).read_text()
op_map_policy = (
    ITERATIVE / "rank2_current_op_aa1_map_policy.md"
).read_text()
op_map_manifest = (
    ITERATIVE / "rank2_current_op_aa1_map_parent.tsv"
).read_text()
op_map_result = (
    ITERATIVE / "rank2_current_op_aa1_map_result.md"
).read_text()
pr_map_policy = (
    ITERATIVE / "rank2_current_pr_aa1_map_policy.md"
).read_text()
pr_map_manifest = (
    ITERATIVE / "rank2_current_pr_aa1_map_parent.tsv"
).read_text()
pr_map_result = (
    ITERATIVE / "rank2_current_pr_aa1_map_result.md"
).read_text()
u_history_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_history.tsv"
).read_text()
latest_history_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_history.tsv"
).read_text()
recovery_history_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_history.tsv"
).read_text()
qv_history_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_qv_history.tsv"
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

latest_recovery_rows = [
    line.split() for line in latest_recovery_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(latest_recovery_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-recovery-map-parent-v1",
        "latest-recovery-map manifest version changed")
require(tuple(row[0] for row in latest_recovery_rows) == roles,
        "latest-recovery-map manifest roles changed")
require(all(len(row) == 3 for row in latest_recovery_rows),
        "latest-recovery-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_recovery_rows),
        "latest-recovery-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_recovery_rows),
        "latest-recovery-map manifest path escapes the repository")
require(latest_recovery_rows[4][1] ==
        "53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193",
        "latest-recovery proposal AX parent changed")
require(latest_recovery_rows[5][1] ==
        "3404d4295b8f71fa20d9b565fc88c0631184775dcac336be2f50e797999cefaa",
        "latest-recovery proposal snapshot parent changed")

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

current_aa2_map_rows = [
    line.split() for line in current_aa2_map_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(current_aa2_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-aa2-map-parent-v1",
        "current-AA2-map manifest version changed")
require(tuple(row[0] for row in current_aa2_map_rows) == roles,
        "current-AA2-map manifest roles changed")
require(all(len(row) == 3 for row in current_aa2_map_rows),
        "current-AA2-map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in current_aa2_map_rows),
        "current-AA2-map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts
            for row in current_aa2_map_rows),
        "current-AA2-map manifest path escapes the repository")
require(current_aa2_map_rows[4][1] ==
        "dc2251e13fa473ceebee7839c32bd5b3244498134a8acfab93b39c55b1e79469",
        "current-AA2 proposal AX parent changed")
require(current_aa2_map_rows[5][1] ==
        "87ed9359809608c838991d2743914a47d96741fc94cedc07d06d512735970b63",
        "current-AA2 proposal snapshot parent changed")

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

recovery_history_rows = [
    line.split() for line in recovery_history_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(recovery_history_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-recovery-history-v1",
        "recovery-history manifest version changed")
require(tuple(row[0] for row in recovery_history_rows) ==
        ("qy_pub", "z", "qt_pub", "u"),
        "recovery-history roles changed")
require(all(len(row) == 3 for row in recovery_history_rows),
        "recovery-history manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in recovery_history_rows),
        "recovery-history SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in recovery_history_rows),
        "recovery-history manifest path escapes the repository")
require(tuple(row[1] for row in recovery_history_rows) == (
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9",
        "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
        "d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744",
        ), "recovery-history parents changed")

qv_history_rows = [
    line.split() for line in qv_history_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(qv_history_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-qv-history-v1",
        "qv-history manifest version changed")
require(tuple(row[0] for row in qv_history_rows) ==
        ("qt_pub", "u", "qs_pub", "v"),
        "qv-history roles changed")
require(all(len(row) == 3 for row in qv_history_rows),
        "qv-history manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in qv_history_rows),
        "qv-history SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in qv_history_rows),
        "qv-history manifest path escapes the repository")
require(tuple(row[1] for row in qv_history_rows) == (
        "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
        "d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744",
        "53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193",
        "0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737",
        ), "qv-history parents changed")

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

require(latest_next_recovery_runner.index(
        "RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY=") <
        latest_next_recovery_runner.index("ROOT=$("),
        "recovery default-off gate must precede repository access")
for token in (
    "rank2_latest_modal_aa1_next_map_parent.tsv",
    "rank2_latest_modal_aa1_next_map_recovery_policy.md",
    "iterative-rank2-latest-modal-aa1-next-candidate",
    "iterative-rank2-latest-modal-aa1-next-map-attempt",
    "iterative-rank2-latest-modal-aa1-next-map-recovery",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "INVALID_MAP",
    "TIMEOUT_BEFORE_TERMINAL",
    "96f9bc1eacba30a629f35feceb2177d77e3f0bba4ff9ddaaaa03ecb66e5205c3",
    "-type f",
    "-type l",
    "= 11",
    "= 0",
    "CHECKER_MODE=proposal-z",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "shasum -a 256 -c result.sha256",
):
    require(token in latest_next_recovery_runner,
            f"recovery runner binding missing: {token}")
require(latest_next_recovery_runner.count("run_continuation_short.sh") == 1,
        "recovery common host invocation count is not one")
require("run_bounded_dragon.py" not in latest_next_recovery_runner and
        "DRAGON_BIN" not in latest_next_recovery_runner,
        "recovery wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b",
                      latest_next_recovery_runner),
        "recovery retry loop is forbidden")
latest_next_recovery_default_off = subprocess.run(
    ["sh", str(latest_next_recovery_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY": "0"},
    capture_output=True, text=True, check=False,
)
require(latest_next_recovery_default_off.returncode == 0 and
        latest_next_recovery_default_off.stderr == "" and
        latest_next_recovery_default_off.stdout ==
        "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP-RECOVERY DEFAULT-OFF: "
        "no Dragon process started.\n",
        "recovery default-off terminal changed")
latest_next_recovery_bad_activation = subprocess.run(
    ["sh", str(latest_next_recovery_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_NEXT_MAP_RECOVERY": "2"},
    capture_output=True, text=True, check=False,
)
require(latest_next_recovery_bad_activation.returncode == 2 and
        latest_next_recovery_bad_activation.stdout == "" and
        latest_next_recovery_bad_activation.stderr ==
        "SPOT-RANK2-LATEST-MODAL-AA1-NEXT-MAP-RECOVERY ERROR: activation "
        "must be 0 or 1.\n",
        "recovery activation gate changed")

require(latest_recovery_runner.index(
        "RUN_RANK2_LATEST_MODAL_AA1_RECOVERY_MAP=") <
        latest_recovery_runner.index("ROOT=$("),
        "latest-recovery-map default-off gate must precede repository access")
for token in (
    "rank2_latest_modal_aa1_recovery_map_parent.tsv",
    "rank2_latest_modal_aa1_recovery_map_policy.md",
    "iterative-rank2-latest-modal-aa1-recovery-candidate",
    "iterative-rank2-latest-modal-aa1-recovery-map",
    "CHECKER_MODE=proposal-u",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=420",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in latest_recovery_runner,
            f"latest-recovery-map runner binding missing: {token}")
require(latest_recovery_runner.count("run_continuation_short.sh") == 1,
        "latest-recovery-map common host invocation count is not one")
require("run_bounded_dragon.py" not in latest_recovery_runner and
        "DRAGON_BIN" not in latest_recovery_runner,
        "latest-recovery-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_recovery_runner),
        "latest-recovery-map retry loop is forbidden")
latest_recovery_default_off = subprocess.run(
    ["sh", str(latest_recovery_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_RECOVERY_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(latest_recovery_default_off.returncode == 0 and
        latest_recovery_default_off.stderr == "" and
        latest_recovery_default_off.stdout ==
        "SPOT-RANK2-LATEST-MODAL-AA1-RECOVERY-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "latest-recovery-map default-off terminal changed")
latest_recovery_bad_activation = subprocess.run(
    ["sh", str(latest_recovery_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_LATEST_MODAL_AA1_RECOVERY_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(latest_recovery_bad_activation.returncode == 2 and
        latest_recovery_bad_activation.stdout == "" and
        latest_recovery_bad_activation.stderr ==
        "SPOT-RANK2-LATEST-MODAL-AA1-RECOVERY-MAP ERROR: activation must "
        "be 0 or 1.\n",
        "latest-recovery-map activation gate changed")
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

require(current_aa2_map_runner.index("RUN_RANK2_CURRENT_AA2_MAP=") <
        current_aa2_map_runner.index("ROOT=$("),
        "current-AA2-map default-off gate must precede repository access")
for token in (
    "rank2_current_aa2_map_parent.tsv",
    "rank2_current_aa2_map_policy.md",
    "iterative-rank2-current-aa2-candidate",
    "iterative-rank2-current-aa2-map",
    "CHECKER_MODE=proposal-aa2",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in current_aa2_map_runner,
            f"current-AA2-map runner binding missing: {token}")
require(current_aa2_map_runner.count("run_continuation_short.sh") == 1,
        "current-AA2-map common host invocation count is not one")
require("run_bounded_dragon.py" not in current_aa2_map_runner and
        "DRAGON_BIN" not in current_aa2_map_runner,
        "current-AA2-map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b",
                      current_aa2_map_runner),
        "current-AA2-map retry loop is forbidden")
current_aa2_default_off = subprocess.run(
    ["sh", str(current_aa2_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_AA2_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(current_aa2_default_off.returncode == 0 and
        current_aa2_default_off.stderr == "" and
        current_aa2_default_off.stdout ==
        "SPOT-RANK2-CURRENT-AA2-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "current-AA2-map default-off terminal changed")
current_aa2_bad_activation = subprocess.run(
    ["sh", str(current_aa2_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_AA2_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(current_aa2_bad_activation.returncode == 2 and
        current_aa2_bad_activation.stdout == "" and
        current_aa2_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-AA2-MAP ERROR: activation must be 0 or 1.\n",
        "current-AA2-map activation gate changed")

qvwx_rows = [line.split() for line in qvwx_map_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
require(qvwx_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-aa1-map-parent-v1",
        "QVWX map manifest version changed")
require(tuple(row[0] for row in qvwx_rows) == roles,
        "QVWX map manifest roles changed")
require(qvwx_rows[4][1] ==
        "012ccd8e428e7a819ce41cec70eab90745e92dc1bb95735a35631f3ef0e2057d",
        "QVWX proposal AX parent changed")
require(qvwx_rows[5][1] ==
        "8942bf5ca0c2f551200dcf78508093a34da39636c5fe57f167a05b4d1da37504",
        "QVWX proposal snapshots parent changed")
require(qvwx_map_runner.index("RUN_RANK2_CURRENT_QVWX_AA1_MAP=") <
        qvwx_map_runner.index("ROOT=$("),
        "QVWX map default-off gate must precede repository access")
for token in (
    "rank2_current_qvwx_aa1_map_parent.tsv",
    "rank2_current_qvwx_aa1_map_policy.md",
    "iterative-rank2-current-qvwx-aa1-candidate",
    "iterative-rank2-current-qvwx-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in qvwx_map_runner,
            f"QVWX map runner binding missing: {token}")
require(qvwx_map_runner.count("run_continuation_short.sh") == 1,
        "QVWX map common host invocation count is not one")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qvwx_map_runner),
        "QVWX map retry loop is forbidden")
require("run_bounded_dragon.py" not in qvwx_map_runner and
        "DRAGON_BIN" not in qvwx_map_runner,
        "QVWX map wrapper must not launch Dragon directly")
require("spot-rank2-current-qvwx-aa1-map" in
        (ROOT / "Makefile").read_text(), "QVWX map Make target is missing")
for token in ("R_\\rho", "R_L", "R_a", "D_L", "diagnostic only",
              "AA(2) is skipped", "no retry"):
    require(token in qvwx_map_policy,
            f"QVWX map policy contract missing: {token}")
qvwx_default_off = subprocess.run(
    ["sh", str(qvwx_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(qvwx_default_off.returncode == 0 and
        qvwx_default_off.stderr == "" and
        qvwx_default_off.stdout ==
        "SPOT-RANK2-CURRENT-QVWX-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "QVWX map default-off terminal changed")
qvwx_bad_activation = subprocess.run(
    ["sh", str(qvwx_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(qvwx_bad_activation.returncode == 2 and
        qvwx_bad_activation.stdout == "" and
        qvwx_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-QVWX-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "QVWX map activation gate changed")
for token in (
    "Classification: `VALID_NOT_MET`",
    "523d5adcbf2deb5c951c5c56634ff86fc7fcac83",
    "3.779851170520331",
    "5.538167897611856",
    "1.841719645535316",
    "755.970234",
    "3.683439",
    "21/21 receipt",
    "No further map is authorized",
):
    require(token in qvwx_map_result,
            f"QVWX map result boundary missing: {token}")

qvwx_z_rows = [line.split() for line in qvwx_z_picard_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(qvwx_z_picard_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-z-picard-map-parent-v1",
        "QVWX-Z Picard manifest version changed")
require(tuple(row[0] for row in qvwx_z_rows) == roles,
        "QVWX-Z Picard manifest roles changed")
require(tuple(row[1] for row in qvwx_z_rows[-2:]) == (
    "2c2649c4317cc98fb84b0fa441d14d62834736db9dd1b52857004b34804761cb",
    "685a4433acca6f1402df58b373308d5c7e4ccd0d13cda7dd2ca475394999e815",
), "QVWX-Z Picard parent changed")
require(qvwx_z_picard_runner.index(
        "RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP=") <
        qvwx_z_picard_runner.index("ROOT=$("),
        "QVWX-Z default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-qvwx-aa1-map",
    "rank2_current_qvwx_z_picard_map_parent.tsv",
    "rank2_current_qvwx_z_picard_map_policy.md",
    "iterative-rank2-current-qvwx-z-picard-map",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in qvwx_z_picard_runner,
            f"QVWX-Z Picard runner missing: {token}")
require(qvwx_z_picard_runner.count("run_continuation_short.sh") == 1,
        "QVWX-Z Picard runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qvwx_z_picard_runner),
        "QVWX-Z Picard retry loop is forbidden")
require("run_bounded_dragon.py" not in qvwx_z_picard_runner and
        "DRAGON_BIN" not in qvwx_z_picard_runner,
        "QVWX-Z wrapper must not launch Dragon directly")
for token in ("R_\\rho", "R_L", "R_a", "diagnostic only", "no retry",
              "no affine mixing", "three", "one axial solve"):
    require(token in qvwx_z_picard_policy,
            f"QVWX-Z Picard policy missing: {token}")
require("spot-rank2-current-qvwx-z-picard-map" in
        (ROOT / "Makefile").read_text(),
        "QVWX-Z Picard Make target is missing")
qvwx_z_default_off = subprocess.run(
    ["sh", str(qvwx_z_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(qvwx_z_default_off.returncode == 0 and
        qvwx_z_default_off.stderr == "" and
        qvwx_z_default_off.stdout ==
        "SPOT-RANK2-CURRENT-QVWX-Z-PICARD-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "QVWX-Z Picard default-off terminal changed")
qvwx_z_bad_activation = subprocess.run(
    ["sh", str(qvwx_z_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_Z_PICARD_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(qvwx_z_bad_activation.returncode == 2 and
        qvwx_z_bad_activation.stdout == "" and
        qvwx_z_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-QVWX-Z-PICARD-MAP ERROR: activation must be "
        "0 or 1.\n",
        "QVWX-Z Picard activation gate changed")
for token in (
    "Map classification: `VALID_NOT_MET`",
    "3a30ffd94100df023bfb446487a44311a05a181f",
    "5.324646091595354",
    "7.801572792232037",
    "1.309957085222539",
    "21/21 receipt",
    "0.41511181447765411",
    "0.58488818552234589",
    "0.093357573037484751",
    "0.42214650302136536",
    "0.61065652318148245",
    "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "does not materialize",
    "does not run a second physical map",
):
    require(token in qvwx_z_picard_result,
            f"QVWX-Z Picard result boundary missing: {token}")

qvwx_zplus_map_rows = [
    line.split() for line in qvwx_zplus_map_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(qvwx_zplus_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-zplus-aa1-map-parent-v1",
        "QVWX-ZPLUS AA1 map manifest version changed")
require(tuple(row[0] for row in qvwx_zplus_map_rows) == roles,
        "QVWX-ZPLUS AA1 map manifest roles changed")
require(tuple(row[1] for row in qvwx_zplus_map_rows[-2:]) == (
    "5d462c634e7f909ff059d72ac8bb8d9240cb18c21232c682c99d8f34d791c67c",
    "3c216fff2be1336c29e584e4b8b0d6d9eca537f80c6a5fc07bf08f4ad509eb84",
), "QVWX-ZPLUS AA1 map parent changed")
require(qvwx_zplus_map_runner.index(
        "RUN_RANK2_CURRENT_QVWX_ZPLUS_AA1_MAP=") <
        qvwx_zplus_map_runner.index("ROOT=$("),
        "QVWX-ZPLUS AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-qvwx-zplus-aa1-candidate",
    "rank2_current_qvwx_zplus_aa1_map_parent.tsv",
    "rank2_current_qvwx_zplus_aa1_map_policy.md",
    "iterative-rank2-current-qvwx-zplus-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in qvwx_zplus_map_runner,
            f"QVWX-ZPLUS AA1 map runner missing: {token}")
require(qvwx_zplus_map_runner.count("run_continuation_short.sh") == 1,
        "QVWX-ZPLUS AA1 map runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qvwx_zplus_map_runner),
        "QVWX-ZPLUS AA1 map retry loop is forbidden")
require("run_bounded_dragon.py" not in qvwx_zplus_map_runner and
        "DRAGON_BIN" not in qvwx_zplus_map_runner,
        "QVWX-ZPLUS wrapper must not launch Dragon directly")
for token in (
    "R_\\rho", "R_L", "R_a", "diagnostic only", "no retry",
    "three online radial", "one axial solve", "d-c",
    "second physical map",
):
    require(token in qvwx_zplus_map_policy,
            f"QVWX-ZPLUS AA1 map policy missing: {token}")
require("spot-rank2-current-qvwx-zplus-aa1-map" in
        (ROOT / "Makefile").read_text(),
        "QVWX-ZPLUS AA1 map target is missing")
qvwx_zplus_default_off = subprocess.run(
    ["sh", str(qvwx_zplus_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_ZPLUS_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(qvwx_zplus_default_off.returncode == 0 and
        qvwx_zplus_default_off.stderr == "" and
        qvwx_zplus_default_off.stdout ==
        "SPOT-RANK2-CURRENT-QVWX-ZPLUS-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "QVWX-ZPLUS AA1 map default-off terminal changed")
qvwx_zplus_bad_activation = subprocess.run(
    ["sh", str(qvwx_zplus_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_QVWX_ZPLUS_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(qvwx_zplus_bad_activation.returncode == 2 and
        qvwx_zplus_bad_activation.stdout == "" and
        qvwx_zplus_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-QVWX-ZPLUS-AA1-MAP ERROR: activation must be "
        "0 or 1.\n",
        "QVWX-ZPLUS AA1 map activation gate changed")
for token in (
    "Map classification: `VALID_NOT_MET`",
    "246a4cf48e7b2babbf04c089d9d09a0074f079e2",
    "6.422348086676521",
    "4.958958534883100",
    "7.265771273523569",
    "1.309164007655304",
    "21/21 receipt",
    "0.48771444550122545",
    "0.51228555449877455",
    "0.99411674241637549",
    "0.93884958302279575",
    "0.79362266755606770",
    "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "next proposal is not materialized",
    "no second map is run",
):
    require(token in qvwx_zplus_map_result,
            f"QVWX-ZPLUS AA1 map result boundary missing: {token}")

zpcd_map_rows = [
    line.split() for line in zpcd_map_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(zpcd_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-zpcd-aa1-map-parent-v1",
        "ZPCD AA1 map manifest version changed")
require(tuple(row[0] for row in zpcd_map_rows) == roles,
        "ZPCD AA1 map manifest roles changed")
require(tuple(row[1] for row in zpcd_map_rows[-2:]) == (
    "978593b2813bad2242ad8c235fdd83e6f5bc33b3aff624b60ccecaaf077d95c6",
    "cf43ed781a1f86625aa6ae46023eca2e6e000ed76d16c81470a3544b13bb0354",
), "ZPCD AA1 map parent changed")
require(zpcd_map_runner.index("RUN_RANK2_CURRENT_ZPCD_AA1_MAP=") <
        zpcd_map_runner.index("ROOT=$("),
        "ZPCD AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-zpcd-aa1-candidate",
    "rank2_current_zpcd_aa1_map_parent.tsv",
    "rank2_current_zpcd_aa1_map_policy.md",
    "iterative-rank2-current-zpcd-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in zpcd_map_runner,
            f"ZPCD AA1 map runner missing: {token}")
require(zpcd_map_runner.count("run_continuation_short.sh") == 1,
        "ZPCD AA1 map runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", zpcd_map_runner),
        "ZPCD AA1 map retry loop is forbidden")
require("run_bounded_dragon.py" not in zpcd_map_runner and
        "DRAGON_BIN" not in zpcd_map_runner,
        "ZPCD wrapper must not launch Dragon directly")
for token in (
    "R_\\rho", "R_L", "R_a", "diagnostic only", "no retry",
    "three online radial", "one axial solve", "e-c_{\\mathrm{next}}",
    "second physical map",
):
    require(token in zpcd_map_policy,
            f"ZPCD AA1 map policy missing: {token}")
require("spot-rank2-current-zpcd-aa1-map" in
        (ROOT / "Makefile").read_text(), "ZPCD AA1 map target is missing")
zpcd_default_off = subprocess.run(
    ["sh", str(zpcd_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_ZPCD_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(zpcd_default_off.returncode == 0 and
        zpcd_default_off.stderr == "" and
        zpcd_default_off.stdout ==
        "SPOT-RANK2-CURRENT-ZPCD-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "ZPCD AA1 map default-off terminal changed")
zpcd_bad_activation = subprocess.run(
    ["sh", str(zpcd_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_ZPCD_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(zpcd_bad_activation.returncode == 2 and
        zpcd_bad_activation.stdout == "" and
        zpcd_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-ZPCD-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "ZPCD AA1 map activation gate changed")
for token in (
    "Map classification: `VALID_NOT_MET`",
    "fa154ed421598c5f91fe9b5bd1878af46c993386",
    "6.422349219104007",
    "7.777215945396249",
    "1.139502273872495",
    "1.266857654692717",
    "21/21 receipt",
    "1.3920591161462217",
    "1.4891030102954350",
    "1.5185498258021630",
    "0.27450453816512377",
    "1.3654718014730096",
    "1.3434921133428195",
    "AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL",
    "No next proposal is published",
    "no second map is run",
):
    require(token in zpcd_map_result,
            f"ZPCD AA1 map result boundary missing: {token}")

zpcd_e_rows = [
    line.split() for line in zpcd_e_picard_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(zpcd_e_picard_manifest.splitlines()[0] ==
        "# spot-rank2-current-zpcd-e-picard-map-parent-v1",
        "ZPCD-E Picard manifest version changed")
require(tuple(row[0] for row in zpcd_e_rows) == roles,
        "ZPCD-E Picard manifest roles changed")
require(tuple(row[1] for row in zpcd_e_rows[-2:]) == (
    "0b5c8d27b4d2e37d90d56d27d75619842851b7a0e0206947b31c3d5b88936828",
    "ae6ea8d66c581a496eb56feb512ef5dbbcd0e3a9596871b439a80a3c2a1e66e5",
), "ZPCD-E Picard parent changed")
require(zpcd_e_picard_runner.index(
        "RUN_RANK2_CURRENT_ZPCD_E_PICARD_MAP=") <
        zpcd_e_picard_runner.index("ROOT=$("),
        "ZPCD-E default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-zpcd-aa1-map",
    "rank2_current_zpcd_e_picard_map_parent.tsv",
    "rank2_current_zpcd_e_picard_map_policy.md",
    "iterative-rank2-current-zpcd-e-picard-map",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in zpcd_e_picard_runner,
            f"ZPCD-E Picard runner missing: {token}")
require(zpcd_e_picard_runner.count("run_continuation_short.sh") == 1,
        "ZPCD-E Picard runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", zpcd_e_picard_runner),
        "ZPCD-E Picard retry loop is forbidden")
require("run_bounded_dragon.py" not in zpcd_e_picard_runner and
        "DRAGON_BIN" not in zpcd_e_picard_runner,
        "ZPCD-E wrapper must not launch Dragon directly")
for token in (
    "R_\\rho", "R_L", "R_a", "diagnostic only", "no retry",
    "no affine mixing", "three", "one axial solve", "f-e",
    "no second physical map",
):
    require(token in zpcd_e_picard_policy,
            f"ZPCD-E Picard policy missing: {token}")
require("spot-rank2-current-zpcd-e-picard-map" in
        (ROOT / "Makefile").read_text(),
        "ZPCD-E Picard Make target is missing")
zpcd_e_default_off = subprocess.run(
    ["sh", str(zpcd_e_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_ZPCD_E_PICARD_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(zpcd_e_default_off.returncode == 0 and
        zpcd_e_default_off.stderr == "" and
        zpcd_e_default_off.stdout ==
        "SPOT-RANK2-CURRENT-ZPCD-E-PICARD-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "ZPCD-E Picard default-off terminal changed")
zpcd_e_bad_activation = subprocess.run(
    ["sh", str(zpcd_e_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_ZPCD_E_PICARD_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(zpcd_e_bad_activation.returncode == 2 and
        zpcd_e_bad_activation.stdout == "" and
        zpcd_e_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-ZPCD-E-PICARD-MAP ERROR: activation must be "
        "0 or 1.\n",
        "ZPCD-E Picard activation gate changed")
for token in (
    "Map classification: `VALID_NOT_MET`",
    "ce6be5b9c18201bd24af1c9318c830a6e0b8f6b3",
    "1.284469730578053",
    "8.318307793557387",
    "1.218781108036637",
    "1.505196532244700",
    "21/21 receipt",
    "0.54317069088638781",
    "0.45682930911361219",
    "3.3988810913576900e-12",
    "0.059424727376440133",
    "0.19596354669013863",
    "0.28717479223258224",
    "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) is not evaluated",
    "No durable next",
    "no second physical map is run",
):
    require(token in zpcd_e_picard_result,
            f"ZPCD-E Picard result boundary missing: {token}")

cef_map_rows = [line.split() for line in cef_map_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
require(cef_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-cef-aa1-map-parent-v1",
        "CEF AA1 map manifest version changed")
require(tuple(row[0] for row in cef_map_rows) == roles,
        "CEF AA1 map manifest roles changed")
require(tuple(row[1] for row in cef_map_rows[-2:]) == (
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "5b7d6d7c0cf00a4097284b53816d7e3c91ca4e27656f0bc437f6a0472555ac68",
), "CEF AA1 map parent changed")
require(cef_map_runner.index("RUN_RANK2_CURRENT_CEF_AA1_MAP=") <
        cef_map_runner.index("ROOT=$("),
        "CEF AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-cef-aa1-candidate",
    "rank2_current_cef_aa1_map_parent.tsv",
    "rank2_current_cef_aa1_map_policy.md",
    "iterative-rank2-current-cef-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in cef_map_runner,
            f"CEF AA1 map runner missing: {token}")
require(cef_map_runner.count("run_continuation_short.sh") == 1,
        "CEF AA1 map runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", cef_map_runner),
        "CEF AA1 map retry loop is forbidden")
for token in (
    "R_\\rho", "R_L", "R_a", "diagnostic only", "no retry",
    "three online radial", "one axial solve", "g-q_1",
    "no second physical",
):
    require(token in cef_map_policy,
            f"CEF AA1 map policy missing: {token}")
require("spot-rank2-current-cef-aa1-map" in
        (ROOT / "Makefile").read_text(), "CEF AA1 map target is missing")
cef_default_off = subprocess.run(
    ["sh", str(cef_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_CEF_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(cef_default_off.returncode == 0 and
        cef_default_off.stderr == "" and
        cef_default_off.stdout ==
        "SPOT-RANK2-CURRENT-CEF-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "CEF AA1 map default-off terminal changed")
for token in (
    "Map classification: `VALID_NOT_MET`",
    "afbd273a52ac55cd2164b465f59eb94d7f110171",
    "6.422348086676521",
    "3.858515151996695",
    "5.653419066220522",
    "1.741219010720005",
    "21/21 receipt",
    "-0.054660706649195978",
    "1.0546607066491960",
    "1.0164960989601337",
    "1.0021076380581850",
    "0.37059923635358261",
    "0.28970803656130206",
    "0.33969272708511533",
    "6.0576152422719129e-26",
    "0.33342566026806181",
    "0.47696732762436056",
    "0.39981312880450964",
    "AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS",
    "No durable next",
    "no second physical map is run",
):
    require(token in cef_map_result,
            f"CEF AA1 map result boundary missing: {token}")

gh_map_rows = [line.split() for line in gh_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(gh_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-gh-aa1-map-parent-v1",
        "GH AA1 map manifest version changed")
require(tuple(row[0] for row in gh_map_rows) == roles,
        "GH AA1 map manifest roles changed")
require(tuple(row[1] for row in gh_map_rows[-2:]) == (
    "c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6",
    "3cd88d1d7f65ad05cc7a62025cb12a2d50bc016a52d35b251685da71c559b37f",
), "GH AA1 map parent changed")
require(gh_map_runner.index("RUN_RANK2_CURRENT_GH_AA1_MAP=") <
        gh_map_runner.index("ROOT=$("),
        "GH AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-gh-aa1-candidate",
    "rank2_current_gh_aa1_map_parent.tsv",
    "rank2_current_gh_aa1_map_policy.md",
    "iterative-rank2-current-gh-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
):
    require(token in gh_map_runner,
            f"GH AA1 map runner missing: {token}")
require(gh_map_runner.count("run_continuation_short.sh") == 1,
        "GH AA1 map runner must delegate once")
require(not re.search(r"(?m)^\s*(?:while|until)\b", gh_map_runner),
        "GH AA1 map retry loop is forbidden")
for token in (
    "0.92198482219461153", "0.078015177805388483",
    "i=G_2(q_3)", "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "i-q_3",
    "EXECUTED_ONCE_VALID_NOT_MET", "VALID_NOT_MET",
    "1.0001541854604454", "AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS",
    "no second physical map",
):
    require(token in gh_map_policy,
            f"GH AA1 map policy missing: {token}")
for token in (
    "a802ba1031414c4e25c74791f1043d453b5387c1",
    "6.422348086676521", "4.699542341368844",
    "6.885675247758627", "1.040590980549194",
    "c35dc70d8d6dd35b889622734b81112a3e3fdc09455f8390ef262123f5aa3636",
    "c4f0b6ff6d6ffa28ff3a34061e5cf9e25c78fb1b31546188e932c5e82492f9b1",
    "52f6ddd62d50c6cec8357c8bd7b34eb6c396db1e0cbe850a027d7b23cac37bf3",
    "0.46547000956679907", "0.53452999043320093",
    "1.0001541854604454",
    "0.54656692430484066", "0.22903224207636369",
    "0.22440083361879565", "7.9724244756408422e-26",
    "0.085602787687317231", "0.50064418931908561",
    "0.44048518991529284",
    "AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS",
    "No durable", "no second physical map is run",
):
    require(token in gh_map_result,
            f"GH AA1 map result boundary missing: {token}")
require("spot-rank2-current-gh-aa1-map" in
        (ROOT / "Makefile").read_text(), "GH AA1 map target is missing")
gh_default_off = subprocess.run(
    ["sh", str(gh_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_GH_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(gh_default_off.returncode == 0 and
        gh_default_off.stderr == "" and
        gh_default_off.stdout ==
        "SPOT-RANK2-CURRENT-GH-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "GH AA1 map default-off terminal changed")

ij_map_rows = [line.split() for line in ij_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(ij_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-ij-aa1-map-parent-v1",
        "IJ AA1 map manifest version changed")
require(tuple(row[0] for row in ij_map_rows) == roles,
        "IJ AA1 map manifest roles changed")
require(all(len(row) == 3 for row in ij_map_rows),
        "IJ AA1 map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in ij_map_rows),
        "IJ AA1 map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in ij_map_rows),
        "IJ AA1 map manifest path escapes the repository")
require(tuple(row[1] for row in ij_map_rows[-2:]) == (
    "27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743",
    "f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c",
), "IJ AA1 map parent changed")
require(ij_map_runner.index("RUN_RANK2_CURRENT_IJ_AA1_MAP=") <
        ij_map_runner.index("ROOT=$("),
        "IJ AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-ij-aa1-candidate",
    "rank2_current_ij_aa1_map_parent.tsv",
    "rank2_current_ij_aa1_map_policy.md",
    "iterative-rank2-current-ij-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in ij_map_runner,
            f"IJ AA1 map runner missing: {token}")
require(ij_map_runner.count("run_continuation_short.sh") == 1,
        "IJ AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in ij_map_runner and
        "DRAGON_BIN" not in ij_map_runner,
        "IJ AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", ij_map_runner),
        "IJ AA1 map retry loop is forbidden")
for token in (
    "1.1922339465680236", "-0.19223394656802359",
    "k=G_2(q_5)", "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "k-q_5",
    "EXECUTED_ONCE_VALID_NOT_MET", "no retry", "no second physical map",
    "empirical parameter", "AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL",
    "1.0008704340662933", "1.2201877109802688",
):
    require(token in ij_map_policy,
            f"IJ AA1 map policy missing: {token}")
ij_default_off = subprocess.run(
    ["sh", str(ij_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_IJ_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(ij_default_off.returncode == 0 and
        ij_default_off.stderr == "" and
        ij_default_off.stdout ==
        "SPOT-RANK2-CURRENT-IJ-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "IJ AA1 map default-off terminal changed")
ij_bad_activation = subprocess.run(
    ["sh", str(ij_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_IJ_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(ij_bad_activation.returncode == 2 and
        ij_bad_activation.stdout == "" and
        ij_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-IJ-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "IJ AA1 map activation gate changed")
require("spot-rank2-current-ij-aa1-map" in
        (ROOT / "Makefile").read_text(), "IJ AA1 map target is missing")
for token in (
    "fbe6058300a93cc771bc050f81397aa2f563b9e7",
    "6.422348086676521", "3.413471840828782",
    "5.001347744837403", "1.330790586136073",
    "VALID_NOT_MET", "21/21",
    "d8c77928f992adf67136331192a018060f203bedf3d1728d46a39d987c6938de",
    "343afaa62d1c6b0e880afe1cd090c944ffc7ecab837125c76b048987634ea9ae",
    "8c8b9d18f208f91494b3fac79947abcbd2bd46b2605b9af6e441c6eba93bd5f0",
    "0.17292455736665602", "0.82707544263334398",
    "2.3273113779303836e-11", "0.33957735217447371",
    "0.88879107302551907", "1.0008704340662933",
    "0.64695441259132080", "0.029106166249854366",
    "0.38215175365853354", "4.8856879432852540e-24",
    "0.060133483366234260", "0.49773629519031415",
    "1.2201877109802688", "8880/8880",
    "AA1_DIRECTION_FAIL_AA2_DIRECTION_FAIL",
    "No durable successor", "second physical map",
):
    require(token in ij_map_result,
            f"IJ AA1 map result boundary missing: {token}")

k_picard_rows = [line.split() for line in k_picard_manifest.splitlines()
                 if line.strip() and not line.startswith("#")]
require(k_picard_manifest.splitlines()[0] ==
        "# spot-rank2-current-k-picard-map-parent-v1",
        "K direct Picard map manifest version changed")
require(tuple(row[0] for row in k_picard_rows) == roles,
        "K direct Picard map manifest roles changed")
require(all(len(row) == 3 for row in k_picard_rows),
        "K direct Picard map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in k_picard_rows),
        "K direct Picard map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in k_picard_rows),
        "K direct Picard map manifest path escapes the repository")
require(tuple(row[1] for row in k_picard_rows[-2:]) == (
    "d8c77928f992adf67136331192a018060f203bedf3d1728d46a39d987c6938de",
    "343afaa62d1c6b0e880afe1cd090c944ffc7ecab837125c76b048987634ea9ae",
), "K direct Picard map parent changed")
require(k_picard_runner.index("RUN_RANK2_CURRENT_K_PICARD_MAP=") <
        k_picard_runner.index("ROOT=$("),
        "K direct Picard default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-ij-aa1-map",
    "rank2_current_k_picard_map_parent.tsv",
    "rank2_current_k_picard_map_policy.md",
    "iterative-rank2-current-k-picard-map",
    "CHECKER_MODE=continued",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "VALID_NOT_MET",
    "shasum -a 256 -c result.sha256",
):
    require(token in k_picard_runner,
            f"K direct Picard map runner missing: {token}")
require(k_picard_runner.count("run_continuation_short.sh") == 1,
        "K direct Picard map runner must delegate once")
require("run_bounded_dragon.py" not in k_picard_runner and
        "DRAGON_BIN" not in k_picard_runner,
        "K direct Picard wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", k_picard_runner),
        "K direct Picard retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "l=G_2(k)", "R_\\rho", "R_L", "R_a",
    "diagnostic only", "three online radial", "one axial solve", "l-k",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter", "TOLERANCE_MET", "VALID_NOT_MET", "INVALID_MAP",
    "AA1_DIRECTION_PASS_AA2_SKIPPED", "0.81736979605403082",
    "0.80173988821917219", "0.90621455552995278",
):
    require(token in k_picard_policy,
            f"K direct Picard map policy missing: {token}")
k_picard_default_off = subprocess.run(
    ["sh", str(k_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_K_PICARD_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(k_picard_default_off.returncode == 0 and
        k_picard_default_off.stderr == "" and
        k_picard_default_off.stdout ==
        "SPOT-RANK2-CURRENT-K-PICARD-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "K direct Picard map default-off terminal changed")
k_picard_bad_activation = subprocess.run(
    ["sh", str(k_picard_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_K_PICARD_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(k_picard_bad_activation.returncode == 2 and
        k_picard_bad_activation.stdout == "" and
        k_picard_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-K-PICARD-MAP ERROR: activation must be 0 or 1.\n",
        "K direct Picard map activation gate changed")
require("spot-rank2-current-k-picard-map" in
        (ROOT / "Makefile").read_text(),
        "K direct Picard map target is missing")
for token in (
    "de35bc474fa5788acda9ce037d7a31721e07d34d",
    "6.422348086676521", "3.744499849949860",
    "5.486363079398870", "1.628119765098577",
    "VALID_NOT_MET", "21/21",
    "fee603751609b7a9ab79ac854e7ecfa93125f3f4597e411e020728ae267180d0",
    "9ffe3428e70f001a5f0e3384a5030fe4a0334787d7454c0f0d143b2b4a5b165f",
    "393597539ad275c1094afea9d241265c7258dbd14229034c90c31140963766bf",
    "0.99334779753418823", "0.0066522024658117341",
    "3.9604495076589152e-13", "0.81736979605403082",
    "0.80173988821917219", "0.90621455552995278",
    "8880/8880", "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) was not calculated", "no second physical map",
):
    require(token in k_picard_result,
            f"K direct Picard map result boundary missing: {token}")

kl_map_rows = [line.split() for line in kl_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(kl_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-kl-aa1-map-parent-v1",
        "KL AA1 map manifest version changed")
require(tuple(row[0] for row in kl_map_rows) == roles,
        "KL AA1 map manifest roles changed")
require(all(len(row) == 3 for row in kl_map_rows),
        "KL AA1 map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in kl_map_rows),
        "KL AA1 map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in kl_map_rows),
        "KL AA1 map manifest path escapes the repository")
require(tuple(row[1] for row in kl_map_rows[-2:]) == (
    "d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d",
    "c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6",
), "KL AA1 map parent changed")
require(kl_map_runner.index("RUN_RANK2_CURRENT_KL_AA1_MAP=") <
        kl_map_runner.index("ROOT=$("),
        "KL AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-kl-aa1-candidate",
    "rank2_current_kl_aa1_map_parent.tsv",
    "rank2_current_kl_aa1_map_policy.md",
    "iterative-rank2-current-kl-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in kl_map_runner,
            f"KL AA1 map runner missing: {token}")
require(kl_map_runner.count("run_continuation_short.sh") == 1,
        "KL AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in kl_map_runner and
        "DRAGON_BIN" not in kl_map_runner,
        "KL AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", kl_map_runner),
        "KL AA1 map retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "0.99334779753418823",
    "0.0066522024658117341", "m=G_2(q_6)",
    "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "m-q_6",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter",
):
    require(token in kl_map_policy,
            f"KL AA1 map policy missing: {token}")
kl_default_off = subprocess.run(
    ["sh", str(kl_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_KL_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(kl_default_off.returncode == 0 and
        kl_default_off.stderr == "" and
        kl_default_off.stdout ==
        "SPOT-RANK2-CURRENT-KL-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "KL AA1 map default-off terminal changed")
kl_bad_activation = subprocess.run(
    ["sh", str(kl_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_KL_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(kl_bad_activation.returncode == 2 and
        kl_bad_activation.stdout == "" and
        kl_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-KL-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "KL AA1 map activation gate changed")
require("spot-rank2-current-kl-aa1-map" in
        (ROOT / "Makefile").read_text(), "KL AA1 map target is missing")
for token in (
    "5cf970008de0eb600b253fae3e2e6a4a2e1caadc",
    "6.422348086676521", "6.815023315567540",
    "9.985233191400766", "4.087844475064791",
    "VALID_NOT_MET", "21/21",
    "76e4d5e44a6f0a1020fd6280c8da262b322acba80940799a28fc3998ef3da4fc",
    "af1ffa33b39dc9df8e6a7f4813d408974f933bd39f4e512e68f135927d9cb406",
    "2a53e45bcefc7347b0187cfa302cbe4276108fb1dc6bfdaac6e1099cd63ea79c",
    "0.71958187611175339", "0.28041812388824661",
    "1.4220277430317252e-11", "0.089320649038882691",
    "0.82454368960985658", "0.56421285796347498",
    "8880/8880", "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) was not calculated", "no second physical map",
):
    require(token in kl_map_result,
            f"KL AA1 map result boundary missing: {token}")

klm_map_rows = [line.split() for line in klm_map_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
require(klm_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-klm-aa1-map-parent-v1",
        "KLM AA1 map manifest version changed")
require(tuple(row[0] for row in klm_map_rows) == roles,
        "KLM AA1 map manifest roles changed")
require(all(len(row) == 3 for row in klm_map_rows),
        "KLM AA1 map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in klm_map_rows),
        "KLM AA1 map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in klm_map_rows),
        "KLM AA1 map manifest path escapes the repository")
require(tuple(row[1] for row in klm_map_rows[-2:]) == (
    "74cbee2ffcb72db1a86e728f8643cfbe9dfb6f2784965fe440bd20567a50ee89",
    "78a999ff7b2fab8f7fbfd4b29e0d433b9ae9e9ef5b124ff812c776b7422f437c",
), "KLM AA1 map parent changed")
require(klm_map_runner.index("RUN_RANK2_CURRENT_KLM_AA1_MAP=") <
        klm_map_runner.index("ROOT=$("),
        "KLM AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-klm-aa1-candidate",
    "rank2_current_klm_aa1_map_parent.tsv",
    "rank2_current_klm_aa1_map_policy.md",
    "iterative-rank2-current-klm-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120",
    "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in klm_map_runner,
            f"KLM AA1 map runner missing: {token}")
require(klm_map_runner.count("run_continuation_short.sh") == 1,
        "KLM AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in klm_map_runner and
        "DRAGON_BIN" not in klm_map_runner,
        "KLM AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", klm_map_runner),
        "KLM AA1 map retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "0.71958187611175339",
    "0.28041812388824661", "n=G_2(q_7)",
    "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "n-q_7",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter",
):
    require(token in klm_map_policy,
            f"KLM AA1 map policy missing: {token}")
klm_default_off = subprocess.run(
    ["sh", str(klm_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_KLM_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(klm_default_off.returncode == 0 and
        klm_default_off.stderr == "" and
        klm_default_off.stdout ==
        "SPOT-RANK2-CURRENT-KLM-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "KLM AA1 map default-off terminal changed")
klm_bad_activation = subprocess.run(
    ["sh", str(klm_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_KLM_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(klm_bad_activation.returncode == 2 and
        klm_bad_activation.stdout == "" and
        klm_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-KLM-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "KLM AA1 map activation gate changed")
require("spot-rank2-current-klm-aa1-map" in
        (ROOT / "Makefile").read_text(), "KLM AA1 map target is missing")
for token in (
    "767fe7da92de238fdb7face911cf7e487c7e4901",
    "6.422348086676521", "4.990742346753720",
    "7.312337402254343", "4.639312542887599",
    "VALID_NOT_MET", "21/21",
    "973f8951dca356d1f9c3d42bfc8791fda19bb5263b3dea3ca9df8fa3f1712e56",
    "4371455c7fccff86d6586447d1e0433db5743ee1c1af2cdcdb4c5c30f4df4c4f",
    "11d847935af19f6f74b7295980f194880e64ce58d2929bec7dd970279ad73d79",
    "-0.061472310444878220", "1.0614723104448782",
    "6.5246745314225801e-12", "0.86145202366683948",
    "1.0902164970939685", "1.0741288780839371",
    "0.37973124035268829", "0.10995812065327257",
    "0.51031063899403917", "3.0970099337137395e-24",
    "0.16177043590261239", "0.45458049672516687",
    "0.46901724246492071", "8880/8880",
    "AA1_DIRECTION_FAIL_AA2_DIRECTION_PASS", "no second physical map",
):
    require(token in klm_map_result,
            f"KLM AA1 map result boundary missing: {token}")

no_map_rows = [line.split() for line in no_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(no_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-no-aa1-map-parent-v1",
        "NO AA1 map manifest version changed")
require(tuple(row[0] for row in no_map_rows) == roles,
        "NO AA1 map manifest roles changed")
require(all(len(row) == 3 for row in no_map_rows),
        "NO AA1 map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in no_map_rows),
        "NO AA1 map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in no_map_rows),
        "NO AA1 map manifest path escapes the repository")
require(tuple(row[1] for row in no_map_rows[-2:]) == (
    "c5d3275ead6dc8b5afb6d7ec125965678a0659ed8cf027d547edd6a009738b4e",
    "f7476c9f42d5de128e56c01044609e233a11ec147019942d429b8db419ba30ab",
), "NO AA1 map parent changed")
require(no_map_runner.index("RUN_RANK2_CURRENT_NO_AA1_MAP=") <
        no_map_runner.index("ROOT=$("),
        "NO AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-no-aa1-candidate",
    "rank2_current_no_aa1_map_parent.tsv",
    "rank2_current_no_aa1_map_policy.md",
    "iterative-rank2-current-no-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120", "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in no_map_runner,
            f"NO AA1 map runner missing: {token}")
require(no_map_runner.count("run_continuation_short.sh") == 1,
        "NO AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in no_map_runner and
        "DRAGON_BIN" not in no_map_runner,
        "NO AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", no_map_runner),
        "NO AA1 map retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "0.14445266271586943",
    "0.85554733728413057", "3.8680130073227605e-14",
    "0.99405602856832498", "0.78327883203609316",
    "0.82926667695332601", "p=G_2(q_9)",
    "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "p-q_9",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter",
):
    require(token in no_map_policy,
            f"NO AA1 map policy missing: {token}")
for token in (
    "8f1eb8fc19a3ee71a839f0661712910cac9b6a89",
    "6.422348086676521", "6.792180645546773",
    "9.951763786375523", "1.761650656565653",
    "1358.436129", "3.523301313", "VALID_NOT_MET", "21/21",
    "6e7bb36ac9c123e86919bfc4655d23e4b9958a0ae6aa24e9d5815a90acc89132",
    "7c38ad7b197554c22a101664bff5367153f87496007928adaca601bc975a2649",
    "ff37eac4c32abb0bc862a7d2196afa743f9be27b4bac927b0b3a4037ad64a70c",
    "1.2246645215600993", "0.22466452156009933",
    "9.0412608575558238e-13", "0.12764993865086841",
    "0.82141838136874701", "0.89227926518865730",
    "8880/8880", "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) is not", "no durable", "no second physical map",
):
    require(token.lower() in no_map_result.lower(),
            f"NO AA1 map result boundary missing: {token}")
no_default_off = subprocess.run(
    ["sh", str(no_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_NO_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(no_default_off.returncode == 0 and no_default_off.stderr == "" and
        no_default_off.stdout ==
        "SPOT-RANK2-CURRENT-NO-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "NO AA1 map default-off terminal changed")
no_bad_activation = subprocess.run(
    ["sh", str(no_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_NO_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(no_bad_activation.returncode == 2 and
        no_bad_activation.stdout == "" and
        no_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-NO-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "NO AA1 map activation gate changed")
require("spot-rank2-current-no-aa1-map" in
        (ROOT / "Makefile").read_text(), "NO AA1 map target is missing")

op_map_rows = [line.split() for line in op_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(op_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-op-aa1-map-parent-v1",
        "OP AA1 map manifest version changed")
require(tuple(row[0] for row in op_map_rows) == roles,
        "OP AA1 map manifest roles changed")
require(all(len(row) == 3 for row in op_map_rows),
        "OP AA1 map manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in op_map_rows),
        "OP AA1 map manifest SHA-256 is invalid")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in op_map_rows),
        "OP AA1 map manifest path escapes the repository")
require(tuple(row[1] for row in op_map_rows[-2:]) == (
    "bd0785e9f3da27b9639c3ac4c04d3bf25689c5dc7f16fc51cdcdde7306b154fb",
    "4587fcc293ba18c40c0c785e6de4991d969cc10cca8975b4b4fddf114725c209",
), "OP AA1 map parent changed")
require(op_map_runner.index("RUN_RANK2_CURRENT_OP_AA1_MAP=") <
        op_map_runner.index("ROOT=$("),
        "OP AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-op-aa1-candidate",
    "rank2_current_op_aa1_map_parent.tsv",
    "rank2_current_op_aa1_map_policy.md",
    "iterative-rank2-current-op-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120", "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in op_map_runner,
            f"OP AA1 map runner missing: {token}")
require(op_map_runner.count("run_continuation_short.sh") == 1,
        "OP AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in op_map_runner and
        "DRAGON_BIN" not in op_map_runner,
        "OP AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", op_map_runner),
        "OP AA1 map retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "1.2246645215600993",
    "0.22466452156009933", "9.0412608575558238e-13",
    "0.12764993865086841", "0.82141838136874701",
    "0.89227926518865730", "r=G_2(q_{10})",
    "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "r-q_{10}",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter",
):
    require(token in op_map_policy,
            f"OP AA1 map policy missing: {token}")
for token in (
    "25c4f31132290de4c3816d972b4f469c1b682357",
    "6.422348086676521", "9.408223459489815",
    "1.378473825752735", "5.576247465674659",
    "1881.644692", "1.115249493", "VALID_NOT_MET", "21/21",
    "d92f92919316f1abd8b2c00712b0c804c6a82d141d4501c39d2dc77c9dec10ff",
    "4cc762f6932ed42af7ea22d6130b741c14c463d37c388c93fff2269646ee22f9",
    "61e023e4d795618d6f8cf4fd2b4774b84a8fcf55afc24a75ebce47b6ddd92606",
    "0.21697843452735655", "0.78302156547264345",
    "2.1912767600921286e-12", "0.50304720552788507",
    "0.87862793996767796", "0.82134690926235421",
    "8880/8880", "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) is not", "no durable", "no second physical map",
):
    require(token.lower() in op_map_result.lower(),
            f"OP AA1 map result boundary missing: {token}")
op_default_off = subprocess.run(
    ["sh", str(op_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_OP_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(op_default_off.returncode == 0 and op_default_off.stderr == "" and
        op_default_off.stdout ==
        "SPOT-RANK2-CURRENT-OP-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "OP AA1 map default-off terminal changed")
op_bad_activation = subprocess.run(
    ["sh", str(op_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_OP_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(op_bad_activation.returncode == 2 and
        op_bad_activation.stdout == "" and
        op_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-OP-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "OP AA1 map activation gate changed")
require("spot-rank2-current-op-aa1-map" in
        (ROOT / "Makefile").read_text(), "OP AA1 map target is missing")

pr_map_rows = [line.split() for line in pr_map_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
require(pr_map_manifest.splitlines()[0] ==
        "# spot-rank2-current-pr-aa1-map-parent-v1",
        "PR AA1 map manifest version changed")
require(tuple(row[0] for row in pr_map_rows) == roles,
        "PR AA1 map manifest roles changed")
require(all(len(row) == 3 for row in pr_map_rows),
        "PR AA1 map manifest row width changed")
require(tuple(row[1] for row in pr_map_rows[-2:]) == (
    "20b4a9fb31f6baa4f62d9fa5b22cf0801709ceb37579bf9f16dfc7e6c450f05d",
    "d974a4883eaa5460614d25cdf81284644760218308c88f35ed41bd54065d0167",
), "PR AA1 map parent changed")
require(pr_map_runner.index("RUN_RANK2_CURRENT_PR_AA1_MAP=") <
        pr_map_runner.index("ROOT=$("),
        "PR AA1 default-off gate must precede repository access")
for token in (
    "iterative-rank2-current-pr-aa1-candidate",
    "rank2_current_pr_aa1_map_parent.tsv",
    "rank2_current_pr_aa1_map_policy.md",
    "iterative-rank2-current-pr-aa1-map",
    "CHECKER_MODE=proposal-aa1",
    "RADIAL_TIMEOUT_SECONDS=120", "AXIAL_TIMEOUT_SECONDS=180",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "shasum -a 256 -c result.sha256",
):
    require(token in pr_map_runner,
            f"PR AA1 map runner missing: {token}")
require(pr_map_runner.count("run_continuation_short.sh") == 1,
        "PR AA1 map runner must delegate once")
require("run_bounded_dragon.py" not in pr_map_runner and
        "DRAGON_BIN" not in pr_map_runner,
        "PR AA1 map wrapper must not launch Dragon directly")
require(not re.search(r"(?m)^\s*(?:while|until)\b", pr_map_runner),
        "PR AA1 map retry loop is forbidden")
for token in (
    "EXECUTED_ONCE_VALID_NOT_MET", "0.21697843452735655",
    "0.78302156547264345", "2.1912767600921286e-12",
    "0.50304720552788507", "0.87862793996767796",
    "0.82134690926235421", "s=G_2(q_{11})",
    "R_\\rho", "R_L", "R_a", "diagnostic only",
    "three online radial", "one axial solve", "s-q_{11}",
    "120 s", "180 s", "no retry", "no second physical map",
    "empirical parameter",
):
    require(token in pr_map_policy,
            f"PR AA1 map policy missing: {token}")
for token in (
    "9ff16f11d1d29e2268e0205618c29203088248ef",
    "6.422348086676521", "4.372585176123830",
    "6.406626198440790", "4.015641907413114",
    "874.517035", "VALID_NOT_MET", "21/21",
    "7f9b0e62322acde5ffcfee4aab5d5d4da68b1b04dc7dbdc8314b39787b3b0e11",
    "26de1301b2c9773b18258c07686edba6e4bbc18d16168632da14a92483712219",
    "e57c0fb5e3afde903024342d3289b664322019c721d2489b90b56b082b9e7b9c",
    "0.41267816249435374", "0.58732183750564626",
    "3.8071754534215003e-13", "0.30785297571708414",
    "0.94676682054309913", "0.98610570398914554",
    "8880/8880", "AA1_DIRECTION_PASS_AA2_SKIPPED",
    "AA(2) is not", "no durable", "no second physical map",
):
    require(token.lower() in pr_map_result.lower(),
            f"PR AA1 map result boundary missing: {token}")
pr_default_off = subprocess.run(
    ["sh", str(pr_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_PR_AA1_MAP": "0"},
    capture_output=True, text=True, check=False,
)
require(pr_default_off.returncode == 0 and pr_default_off.stderr == "" and
        pr_default_off.stdout ==
        "SPOT-RANK2-CURRENT-PR-AA1-MAP DEFAULT-OFF: "
        "no Dragon process started.\n",
        "PR AA1 map default-off terminal changed")
pr_bad_activation = subprocess.run(
    ["sh", str(pr_map_runner_path)], cwd=ROOT,
    env={"RUN_RANK2_CURRENT_PR_AA1_MAP": "2"},
    capture_output=True, text=True, check=False,
)
require(pr_bad_activation.returncode == 2 and
        pr_bad_activation.stdout == "" and
        pr_bad_activation.stderr ==
        "SPOT-RANK2-CURRENT-PR-AA1-MAP ERROR: activation must be 0 or 1.\n",
        "PR AA1 map activation gate changed")
require("spot-rank2-current-pr-aa1-map" in
        (ROOT / "Makefile").read_text(), "PR AA1 map target is missing")

require(
        "initial|continued|reencoded|proposal|proposal-z|proposal-v|"
        "proposal-u|proposal-x3|proposal-x4|proposal-aa1|proposal-xnp|proposal-xrp|"
        "proposal-aa2"
        in common,
        "common host does not accept all proposal modes")
require("./check_one_map_xsm --proposal" in common,
        "proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-z" in common,
        "z-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-v" in common,
        "v-carrier proposal checker dispatch is missing")
require("./check_one_map_xsm --proposal-u" in common,
        "u-carrier proposal checker dispatch is missing")
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
require("--proposal-parent-u" in common,
        "u-carrier parent preflight is missing")
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
require(common.index("--proposal-parent-u") < common.index("MAP_STARTED=1"),
        "u-carrier parent preflight must precede map execution")
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
    "trim(mode) == '--proposal-u'",
    "trim(mode) == '--proposal-x3'",
    "trim(mode) == '--proposal-x4'",
    "trim(mode) == '--proposal-aa1'",
    "trim(mode) == '--proposal-xnp'",
    "trim(mode) == '--proposal-xrp'",
    "trim(mode) == '--proposal-aa2'",
    "trim(mode) == '--proposal-parent-z'",
    "trim(mode) == '--proposal-parent-v'",
    "trim(mode) == '--proposal-parent-u'",
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
    "U-RAW-FLUX",
    "X3-RAW-FLUX",
    "X4-RAW-FLUX",
    "AA1-RAW-FLUX",
    "XNP-RAW-FLUX",
    "XRP-RAW-FLUX",
    "AA2-RAW-FLUX",
    "RAW-FLUX CARRIER IS NOT X2",
    "RAW-FLUX CARRIER IS NOT Z",
    "RAW-FLUX CARRIER IS NOT V",
    "RAW-FLUX CARRIER IS NOT U",
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
for token in (
    "--rank2-aa1-x4z-history",
    "MAP-QY-Z RAW-DEFECT BITWISE PASS",
    "MAP-QT-U RAW-DEFECT BITWISE PASS",
    "PROPOSAL-QY-TO-RETURNED-Z",
    "PROPOSAL-QT-TO-RETURNED-U",
    "BETA WEIGHT-U",
    "WEIGHT-Z",
    "LEAKAGE AFFINE-D_L/CURRENT",
    "LEAKAGE SAME-BETA SCREEN ONLY NO LEAKAGE FIT",
    "NEXT-RAW-OUTPUT S=(1-BETA)*Z+BETA*U",
    "OFFLINE_DECISION_ONLY_NO_AUTHORIZATION",
):
    require(token in checker,
            f"recovery-history checker contract missing: {token}")
for token in (
    "--rank2-aa1-zu-history",
    "MAP-QT-U RAW-DEFECT BITWISE PASS",
    "MAP-QS-V RAW-DEFECT BITWISE PASS",
    "PROPOSAL-QT-TO-RETURNED-U",
    "PROPOSAL-QS-TO-RETURNED-V",
    "BETA WEIGHT-V",
    "WEIGHT-U",
    "LEAKAGE AFFINE-D_L/CURRENT",
    "LEAKAGE SAME-BETA SCREEN ONLY NO LEAKAGE FIT",
    "NEXT-RAW-OUTPUT NEXT=(1-BETA)*U+BETA*V",
    "OFFLINE_DECISION_ONLY_NO_AUTHORIZATION",
):
    require(token in checker,
            f"qv-history checker contract missing: {token}")
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
             latest_next_runner, latest_next_recovery_runner,
             latest_recovery_runner, post_runner, rolling_map_runner,
             rolling_next_map_runner, zpcd_map_runner,
             zpcd_e_picard_runner, cef_map_runner, k_picard_runner,
             kl_map_runner, klm_map_runner, no_map_runner, op_map_runner,
             pr_map_runner,
             radial, axial):
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
for token in (
    "Classification: `INVALID_MAP`",
    "Reported reason: `TIMEOUT_BEFORE_TERMINAL`",
    "Scientific result: `NONE`",
    "timeout after 80 seconds; no scientific result",
    "$R_\\rho$, $R_L$, $D_L$, or $R_a$ exists",
    "no retry or successor map was started",
):
    require(token in latest_next_attempt_result,
            f"latest-next-map attempt boundary missing: {token}")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in latest_next_recovery_policy,
            f"recovery classification missing: {label}")
for token in (
    "PREPARED_NOT_RUN",
    "INVALID_MAP / TIMEOUT_BEFORE_TERMINAL / Scientific result NONE",
    "Z-RAW-FLUX",
    "radial process cap: 120 seconds",
    "axial process cap: 420 seconds",
    "external process-safety bounds",
    "not an estimated runtime",
    "automatic successor",
):
    require(token in latest_next_recovery_policy,
            f"recovery policy boundary missing: {token}")
require(re.search(r"no loop,\s+automatic\s+retry",
                  latest_next_recovery_policy) is not None,
        "recovery no-retry boundary is missing")
for token in (
    "Classification: `VALID_NOT_MET`",
    "2da48acefe9bb9cd313b785580eed9e2a3b9e3d2",
    "6.422348086676521e-8",
    "4.434556239270658e-4",
    r"6.497430149465799\times10^{-7}",
    "3.704123514999033e-6",
    "50898b375ffd92d7ad2355cf9ed6cc7b72e0f0c5c9318da78b011ad06b0cf3d3",
    "21-entry receipt passes 21/21",
    "22 regular files and no symbolic",
    "does not satisfy the stopping rule",
    "No retry, new proposal, or",
):
    require(token in latest_next_recovery_result,
            f"recovery result boundary missing: {token}")
for token in (
    "Classification: `OFFLINE_DECISION_COMPLETE`",
    "5.65865271195166948e-7",
    "2.46867988169239516e-6",
    "0.184362130017637404",
    "0.815637869982362540",
    "0.0390808376459938628",
    "0.811050772246201479",
    "1.13252774426119052",
    "8880 / 8880",
    "no componentwise physical verdict",
    "does not authorize",
):
    require(token in recovery_history_result,
            f"recovery-history result boundary missing: {token}")
for token in (
    "Classification: `OFFLINE_DECISION_COMPLETE`",
    "2.46867988169239516e-6",
    "1.76823416857308124e-6",
    "3.43937066250607248",
    "-2.43937066250607248",
    "0.198085822192837768",
    "5.25657676352726266",
    "5.90246254652254176",
    "8880 / 8880",
    "high-risk proposal",
    "does not authorize",
):
    require(token in qv_history_result,
            f"qv-history result boundary missing: {token}")

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in latest_recovery_policy,
            f"latest-recovery-map classification missing: {label}")
for token in (
    "PREPARED_NOT_RUN",
    "U-RAW-FLUX",
    "120 and 420 seconds",
    "external",
    "no retry",
    "automatic successor",
):
    require(token in latest_recovery_policy,
            f"latest-recovery-map policy boundary missing: {token}")
for token in (
    "Classification: `VALID_NOT_MET`",
    "2e05b2ad17c568fa6b7a2359d0ae752962ab8409",
    "1.284469730578053e-7",
    "4.207912846624437e-4",
    r"6.165355443954468\times10^{-7}",
    "2.653141867393721e-6",
    "57bdd4825d61f1947dafe1b8564aaae21748cc09ee519a70dd2745616ddb932a",
    "21/21 receipt",
    "22 regular files, no symbolic",
    "does not meet the convergence target",
    "No retry, new proposal or successor map was started",
):
    require(token in latest_recovery_result,
            f"latest-recovery-map result boundary missing: {token}")

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

for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(label in current_aa2_map_policy,
            f"current-AA2-map classification missing: {label}")
for token in (
    "PREPARED_NOT_RUN",
    "AA2-RAW-FLUX",
    "0.72283238162036112",
    "-0.23768716180315402",
    "0.51485478018279296",
    "120-second radial and 180-second axial",
    "not an empirical relaxation coefficient",
    "There is no retry",
    "starts no successor proposal or map",
):
    require(token in current_aa2_map_policy,
            f"current-AA2-map policy boundary missing: {token}")

for token in (
    "Classification: `VALID_NOT_MET`",
    "d6bf4365b04a4c3b9ffd41e112b44c8123f6c106",
    "6.422348086676521e-8",
    "6.224270631088404e-4",
    r"9.119685273617506\times10^{-7}",
    "2.118720252720744e-6",
    "51.57%",
    "359.85%",
    "21/21 payload receipt",
    "No successor",
):
    require(token in current_aa2_map_result,
            f"current-AA2-map result boundary missing: {token}")

print("RANK2 MODAL AA1 MAP CONTRACT PASS: "
      "X2/Z/V/U/X3/X4/AA1/XNP/XRP/AA2 proposal paths remain distinct; "
      "all hosts are default-off, fixed rank-2 and have no empirical "
      "control.")

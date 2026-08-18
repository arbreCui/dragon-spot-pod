#!/usr/bin/env python3
"""Seconds-scale static contract for one offline rank-2 AA(1) proposal."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
manifest = (ITERATIVE / "rank2_modal_aa1_inputs.tsv").read_text()
next_manifest = (
    ITERATIVE / "rank2_modal_aa1_next_candidate_inputs.tsv"
).read_text()
u_manifest = (
    ITERATIVE / "rank2_modal_aa1_u_candidate_inputs.tsv"
).read_text()
consecutive_manifest = (
    ITERATIVE / "rank2_modal_aa1_consecutive_candidate_inputs.tsv"
).read_text()
ptu_manifest = (
    ITERATIVE / "rank2_current_ptu_aa1_candidate_inputs.tsv"
).read_text()
qvwx_manifest = (
    ITERATIVE / "rank2_current_qvwx_aa1_candidate_inputs.tsv"
).read_text()
gh_manifest = (
    ITERATIVE / "rank2_current_gh_aa1_candidate_inputs.tsv"
).read_text()
ij_manifest = (
    ITERATIVE / "rank2_current_ij_aa1_candidate_inputs.tsv"
).read_text()
ij_result = (
    ITERATIVE / "rank2_current_ij_aa1_candidate_result.md"
).read_text()
gh_result = (
    ITERATIVE / "rank2_current_gh_aa1_candidate_result.md"
).read_text()
qvwx_zplus_manifest = (
    ITERATIVE / "rank2_current_qvwx_zplus_aa1_candidate_inputs.tsv"
).read_text()
kl_manifest = (
    ITERATIVE / "rank2_current_kl_aa1_candidate_inputs.tsv"
).read_text()
kl_result = (
    ITERATIVE / "rank2_current_kl_aa1_candidate_result.md"
).read_text()
cef_manifest = (
    ITERATIVE / "rank2_current_cef_aa1_candidate_inputs.tsv"
).read_text()
cef_result = (
    ITERATIVE / "rank2_current_cef_aa1_candidate_result.md"
).read_text()
zpcd_manifest = (
    ITERATIVE / "rank2_current_zpcd_aa1_candidate_inputs.tsv"
).read_text()
zpcd_result = (
    ITERATIVE / "rank2_current_zpcd_aa1_candidate_result.md"
).read_text()
latest_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_candidate_inputs.tsv"
).read_text()
latest_next_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_next_candidate_inputs.tsv"
).read_text()
recovery_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_recovery_candidate_inputs.tsv"
).read_text()
qv_manifest = (
    ITERATIVE / "rank2_latest_modal_aa1_qv_candidate_inputs.tsv"
).read_text()
qv_result = (
    ITERATIVE / "rank2_latest_modal_aa1_qv_candidate_result.md"
).read_text()
qsvw_manifest = (
    ITERATIVE / "rank2_qsvw_aa1_candidate_inputs.tsv"
).read_text()
qsvw_result = (
    ITERATIVE / "rank2_qsvw_aa1_candidate_result.md"
).read_text()
post_manifest = (
    ITERATIVE / "rank2_modal_aa1_post_candidate_inputs.tsv"
).read_text()
rolling_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_candidate_inputs.tsv"
).read_text()
rolling_next_manifest = (
    ITERATIVE / "rank2_modal_aa1_rolling_next_candidate_inputs.tsv"
).read_text()
builder = (ITERATIVE / "build_rank2_modal_aa1_candidate.f90").read_text()
checker = (ITERATIVE / "check_rank2_modal_aa1_candidate.f90").read_text()
runner = (ITERATIVE / "run_rank2_modal_aa1_candidate.sh").read_text()
next_runner = (
    ITERATIVE / "run_rank2_modal_aa1_next_candidate.sh"
).read_text()
u_runner = (
    ITERATIVE / "run_rank2_modal_aa1_u_candidate.sh"
).read_text()
consecutive_runner = (
    ITERATIVE / "run_rank2_modal_aa1_consecutive_candidate.sh"
).read_text()
ptu_runner = (
    ITERATIVE / "run_rank2_current_ptu_aa1_candidate.sh"
).read_text()
qvwx_runner = (
    ITERATIVE / "run_rank2_current_qvwx_aa1_candidate.sh"
).read_text()
qvwx_zplus_runner = (
    ITERATIVE / "run_rank2_current_qvwx_zplus_aa1_candidate.sh"
).read_text()
zpcd_runner = (
    ITERATIVE / "run_rank2_current_zpcd_aa1_candidate.sh"
).read_text()
latest_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_candidate.sh"
).read_text()
latest_next_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_next_candidate.sh"
).read_text()
recovery_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_recovery_candidate.sh"
).read_text()
qv_runner = (
    ITERATIVE / "run_rank2_latest_modal_aa1_qv_candidate.sh"
).read_text()
qsvw_runner = (
    ITERATIVE / "run_rank2_qsvw_aa1_candidate.sh"
).read_text()
post_runner = (
    ITERATIVE / "run_rank2_modal_aa1_post_candidate.sh"
).read_text()
rolling_runner = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_candidate.sh"
).read_text()
rolling_next_runner = (
    ITERATIVE / "run_rank2_modal_aa1_rolling_next_candidate.sh"
).read_text()


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

next_rows = [line.split() for line in next_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
next_roles = (
    "x1", "x2", "y_pub", "z", "z_snapshots", "basis_reference"
)
require(next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-next-candidate-inputs-v1",
        "next manifest version changed")
require(tuple(row[0] for row in next_rows) == next_roles,
        "next manifest roles changed")
require(all(len(row) == 3 for row in next_rows),
        "next manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in next_rows),
        "next manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in next_rows),
        "next manifest path escapes the repository")

u_rows = [line.split() for line in u_manifest.splitlines()
          if line.strip() and not line.startswith("#")]
u_roles = (
    "y_pub", "z", "w_pub", "v", "v_snapshots", "basis_reference"
)
require(u_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-u-candidate-inputs-v1",
        "u manifest version changed")
require(tuple(row[0] for row in u_rows) == u_roles,
        "u manifest roles changed")
require(all(len(row) == 3 for row in u_rows),
        "u manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in u_rows),
        "u manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in u_rows),
        "u manifest path escapes the repository")

consecutive_rows = [line.split() for line in consecutive_manifest.splitlines()
                    if line.strip() and not line.startswith("#")]
consecutive_roles = (
    "x1_pub", "x2", "x3", "x3_snapshots", "basis_reference"
)
require(consecutive_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-consecutive-candidate-inputs-v1",
        "consecutive manifest version changed")
require(tuple(row[0] for row in consecutive_rows) == consecutive_roles,
        "consecutive manifest roles changed")
require(all(len(row) == 3 for row in consecutive_rows),
        "consecutive manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in consecutive_rows),
        "consecutive manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in consecutive_rows),
        "consecutive manifest path escapes the repository")

ptu_rows = [line.split() for line in ptu_manifest.splitlines()
            if line.strip() and not line.startswith("#")]
ptu_roles = ("p", "t", "u", "u_snapshots", "basis_reference")
require(ptu_manifest.splitlines()[0] ==
        "# spot-rank2-current-ptu-aa1-candidate-inputs-v1",
        "PTU manifest version changed")
require(tuple(row[0] for row in ptu_rows) == ptu_roles,
        "PTU manifest roles changed")
require(all(len(row) == 3 for row in ptu_rows),
        "PTU manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in ptu_rows),
        "PTU manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in ptu_rows),
        "PTU manifest path escapes the repository")

qvwx_rows = [line.split() for line in qvwx_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
qvwx_roles = ("q", "v", "w", "x", "x_snapshots", "basis_reference")
require(qvwx_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-aa1-candidate-inputs-v1",
        "QVWX manifest version changed")
require(tuple(row[0] for row in qvwx_rows) == qvwx_roles,
        "QVWX manifest roles changed")
require(all(len(row) == 3 for row in qvwx_rows),
        "QVWX manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in qvwx_rows),
        "QVWX manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in qvwx_rows),
        "QVWX manifest path escapes the repository")

gh_rows = [line.split() for line in gh_manifest.splitlines()
           if line.strip() and not line.startswith("#")]
require(gh_manifest.splitlines()[0] ==
        "# spot-rank2-current-gh-aa1-candidate-inputs-v1",
        "GH manifest version changed")
require(tuple(row[0] for row in gh_rows) == qvwx_roles,
        "GH manifest roles changed")
require(all(len(row) == 3 for row in gh_rows),
        "GH manifest row width changed")
require(tuple(row[1] for row in gh_rows) == (
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "1b52b5ebd421e620f1f9d7d4e60e50fb002f85c25031533cc4d650e858dd030a",
    "d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe",
    "5e53f33aea3d91db6999cc735d4ffd47677545ba350f34e36a266ff5e6f123ad",
    "17da9628503fafe310ae7dc3223e34de61d78b4c9cc6e4a302ea6e1b6345e5de",
    "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
), "GH q1/g/q2/h history changed")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in gh_rows),
        "GH manifest path escapes the repository")

ij_rows = [line.split() for line in ij_manifest.splitlines()
           if line.strip() and not line.startswith("#")]
require(ij_manifest.splitlines()[0] ==
        "# spot-rank2-current-ij-aa1-candidate-inputs-v1",
        "IJ manifest version changed")
require(tuple(row[0] for row in ij_rows) == qvwx_roles,
        "IJ manifest roles changed")
require(all(len(row) == 3 for row in ij_rows),
        "IJ manifest row width changed")
require(tuple(row[1] for row in ij_rows) == (
    "c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6",
    "c35dc70d8d6dd35b889622734b81112a3e3fdc09455f8390ef262123f5aa3636",
    "5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391",
    "1910e6d0c4bc413cda29713d7bb38191d5ab41ca6f1564f07a9a1a093e240f42",
    "ff2f7e2ab6fbd955212fdf337f318657757eb04e507a65bd4669cefe65d0d587",
    "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
), "IJ q3/i/q4/j history changed")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in ij_rows),
        "IJ manifest path escapes the repository")

latest_rows = [line.split() for line in latest_manifest.splitlines()
               if line.strip() and not line.startswith("#")]
latest_roles = ("x2", "x3", "x4", "x4_snapshots", "basis_reference")
require(latest_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-candidate-inputs-v1",
        "latest manifest version changed")
require(tuple(row[0] for row in latest_rows) == latest_roles,
        "latest manifest roles changed")
require(all(len(row) == 3 for row in latest_rows),
        "latest manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in latest_rows),
        "latest manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_rows),
        "latest manifest path escapes the repository")
require(latest_rows[2][1] ==
        "ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08",
        "latest x4 AX changed")
require(latest_rows[3][1] ==
        "4b5deac64ec6ab50cd9c1c7a9e868f824bb2078895492eeb56c95863bd85e87a",
        "latest x4 snapshots changed")

latest_next_rows = [
    line.split() for line in latest_next_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
latest_next_roles = (
    "x3", "x4", "qy_pub", "z", "z_snapshots", "basis_reference"
)
require(latest_next_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-next-candidate-inputs-v1",
        "latest-next manifest version changed")
require(tuple(row[0] for row in latest_next_rows) == latest_next_roles,
        "latest-next manifest roles changed")
require(all(len(row) == 3 for row in latest_next_rows),
        "latest-next manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in latest_next_rows),
        "latest-next manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in latest_next_rows),
        "latest-next manifest path escapes the repository")
require(tuple(row[1] for row in latest_next_rows) == (
        "154c707c0f21a1241fad0c887486867e9953af794fec0aa883220d669de74651",
        "ee50a8cb438aba8bb36a30613975d92bdc93528b070bd61d1a43f2d17e53cc08",
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9",
        "01d8fe5bc2556c1efa0931f72e69b727925589a3d2ad34aeac82c362b83d8647",
        "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        ), "latest-next parents changed")

recovery_rows = [
    line.split() for line in recovery_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
recovery_roles = (
    "qy_pub", "z", "qt_pub", "u", "u_snapshots", "basis_reference"
)
require(recovery_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-recovery-candidate-inputs-v1",
        "recovery-candidate manifest version changed")
require(tuple(row[0] for row in recovery_rows) == recovery_roles,
        "recovery-candidate manifest roles changed")
require(all(len(row) == 3 for row in recovery_rows),
        "recovery-candidate manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in recovery_rows),
        "recovery-candidate manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in recovery_rows),
        "recovery-candidate manifest path escapes the repository")
require(tuple(row[1] for row in recovery_rows) == (
        "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
        "8f641951ded5f7709a074f71313045396930f5c0985b598bcb22adca7d189ec9",
        "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
        "d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744",
        "7d8763c2e3da9082393aee35b79820173f72dc062f75a2a3dd07e5d305d1367c",
        "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        ), "recovery-candidate parents changed")

qv_rows = [
    line.split() for line in qv_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
qv_roles = (
    "qt_pub", "u", "qs_pub", "v", "v_snapshots", "basis_reference"
)
require(qv_manifest.splitlines()[0] ==
        "# spot-rank2-latest-modal-aa1-qv-candidate-inputs-v1",
        "qv-candidate manifest version changed")
require(tuple(row[0] for row in qv_rows) == qv_roles,
        "qv-candidate manifest roles changed")
require(all(len(row) == 3 for row in qv_rows),
        "qv-candidate manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in qv_rows),
        "qv-candidate manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in qv_rows),
        "qv-candidate manifest path escapes the repository")
require(tuple(row[1] for row in qv_rows) == (
        "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
        "d2e394bc4d222cf5515f27ed2a2b1fe3333ba9cb346b25c1424b292b27d1f744",
        "53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193",
        "0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737",
        "a701f41dfc42fb31043befad8c3607d669bbba456c1dda663a6c6a1873d1f9ed",
        "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        ), "qv-candidate parents changed")

qsvw_rows = [
    line.split() for line in qsvw_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(qsvw_manifest.splitlines()[0] ==
        "# spot-rank2-qsvw-aa1-candidate-inputs-v1",
        "qsvw-candidate manifest version changed")
require(tuple(row[0] for row in qsvw_rows) ==
        ("qs_pub", "v", "w", "w_snapshots", "basis_reference"),
        "qsvw-candidate manifest roles changed")
require(all(len(row) == 3 for row in qsvw_rows),
        "qsvw-candidate manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in qsvw_rows),
        "qsvw-candidate manifest contains an invalid SHA-256")
require(tuple(row[1] for row in qsvw_rows) == (
            "53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193",
            "0842ea931a0b53babb7ea7cde6af459ad86d219ea70e83f1242b7b86ce2bf737",
            "defdee0cf442470eb623ebb83c8bed59b8c20308121951ef0c72073ddba3c243",
            "661fa88ed1a8a08907d5a31d90a367565a5c3dbcd0e50a8c3ccecc866436f1ca",
            "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
        ), "qsvw-candidate parents changed")

post_rows = [line.split() for line in post_manifest.splitlines()
             if line.strip() and not line.startswith("#")]
post_roles = (
    "x2", "x3", "aa1_pub", "aa1_plus", "aa1_plus_snapshots",
    "basis_reference",
)
require(post_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-post-candidate-inputs-v1",
        "post-AA1 manifest version changed")
require(tuple(row[0] for row in post_rows) == post_roles,
        "post-AA1 manifest roles changed")
require(all(len(row) == 3 for row in post_rows),
        "post-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in post_rows),
        "post-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in post_rows),
        "post-AA1 manifest path escapes the repository")

rolling_rows = [line.split() for line in rolling_manifest.splitlines()
                if line.strip() and not line.startswith("#")]
rolling_roles = (
    "aa1_pub", "aa1_plus", "xnext_pub", "xnext_plus",
    "xnext_plus_snapshots", "basis_reference",
)
require(rolling_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-candidate-inputs-v1",
        "rolling-AA1 manifest version changed")
require(tuple(row[0] for row in rolling_rows) == rolling_roles,
        "rolling-AA1 manifest roles changed")
require(all(len(row) == 3 for row in rolling_rows),
        "rolling-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_rows),
        "rolling-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rolling_rows),
        "rolling-AA1 manifest path escapes the repository")

rolling_next_rows = [
    line.split() for line in rolling_next_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
rolling_next_roles = (
    "xnext_pub", "xnext_plus", "xroll_pub", "xroll_plus",
    "xroll_plus_snapshots", "basis_reference",
)
require(rolling_next_manifest.splitlines()[0] ==
        "# spot-rank2-modal-aa1-rolling-next-candidate-inputs-v1",
        "rolling-next-AA1 manifest version changed")
require(tuple(row[0] for row in rolling_next_rows) == rolling_next_roles,
        "rolling-next-AA1 manifest roles changed")
require(all(len(row) == 3 for row in rolling_next_rows),
        "rolling-next-AA1 manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in rolling_next_rows),
        "rolling-next-AA1 manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in rolling_next_rows),
        "rolling-next-AA1 manifest path escapes the repository")
require(rolling_next_rows[3][1] ==
        "dbb333c8cd1a00a24de40d7b8685349fb83f63a7f0d92c0d2d225c8a25bc07a2",
        "rolling-next-AA1 latest AX output changed")
require(rolling_next_rows[4][1] ==
        "ca57bdfb2f950aa24cf5a42edf9fe59883ccfa9221388fbc6aee8b76c94480fc",
        "rolling-next-AA1 latest snapshot output changed")

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
    "--next x1 x2 y z z_snap out_ax out_snap",
    "p_a=next_x2%coordinates(il)-next_x1%coordinates(il)",
    "q_a=next_z%coordinates(il)-next_y%coordinates(il)",
    "next_beta=(p_sq-p_dot)/next_denominator",
    "next_candidate_a=next_weight_x2*next_x2%coordinates+",
    "next_candidate_l=next_weight_x2*next_x2%leakage+",
    "next_rho_star=next_weight_x2*next_x2%rho+next_beta*next_z%rho",
    "call LCMEQU(next_z%root,next_staged_ax)",
    "call LCMEQU(next_z_snap,next_staged_snap)",
    "next_marker=output_carrier",
    "call validate_snapshot(trim(next_path(5)),next_y,next_z,next_z_snap)",
):
    require(token in builder, f"next builder contract missing: {token}")
require("LCMGID(next_staged_snap,'SYSTEM')" not in builder,
        "next builder must not rewrite lagged SYSTEM history")
for token in (
    "--u y z w v v_snap out_ax out_snap",
    "call build_next_candidate(.true.,.false.,.false.,.false.,.false.,.false.,.false.)",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='V-RAW-FLUX'",
    ".true.,'X2-RAW-FLUX'",
    "call load_state(trim(next_path(3)),next_y,'latest proposal input',",
    "call load_state(trim(next_path(4)),next_z,'latest returned output')",
):
    require(token in builder, f"u builder contract missing: {token}")
for token in (
    "--post-aa1 x2 x3 aa1 aa1p aa1p_snap out_ax out_snap",
    "call build_next_candidate(.false.,.true.,.false.,.false.,.false.,.false.,.false.)",
    "input_carrier='X3-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
    "report_prefix='RANK2-POST-AA1'",
    "latest_output='AA1-PLUS'",
    "previous_output='X3'",
):
    require(token in builder, f"post-AA1 builder contract missing: {token}")
for token in (
    "--rolling-aa1 aa1 aa1p xnext xnextp xnextp_snap",
    "call build_next_candidate(.false.,.false.,.true.,.false.,.false.,.false.,.false.)",
    "input_carrier='AA1-RAW-FLUX'",
    "output_carrier='XNP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL-AA1'",
    "latest_output='XNEXT-P'",
    "previous_output='AA1-PLUS'",
    ".true.,'X3-RAW-FLUX'",
):
    require(token in builder,
            f"rolling-AA1 builder contract missing: {token}")
for token in (
    "--rolling-aa1-next xnext xnextp xroll xrollp xrollp_snap",
    "call build_next_candidate(.false.,.false.,.false.,.true.,.false.,.false.,.false.)",
    "input_carrier='XNP-RAW-FLUX'",
    "output_carrier='XRP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL2-AA1'",
    "latest_output='XROLL-P'",
    "previous_output='XNEXT-P'",
    ".true.,'AA1-RAW-FLUX'",
):
    require(token in builder,
            f"rolling-next-AA1 builder contract missing: {token}")
for token in (
    "--next-x4 x3 x4 qy z z_snap out_ax out_snap",
    "call build_next_candidate(.false.,.false.,.false.,.false.,.true.,.false.,.false.)",
    "input_carrier='X4-RAW-FLUX'",
    "output_carrier='Z-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1-NEXT'",
    "latest_output='Z'",
    "previous_output='X4'",
):
    require(token in builder,
            f"latest-next builder contract missing: {token}")
for token in (
    "--next-x4z qy z qt u u_snap out_ax out_snap",
    "call build_next_candidate(.false.,.false.,.false.,.false.,.false.,.true.,.false.)",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='U-RAW-FLUX'",
    "report_prefix='RANK2-LATEST2-AA1-NEXT'",
    "latest_output='U'",
    "previous_output='Z'",
    ".true.,'X4-RAW-FLUX'",
):
    require(token in builder,
            f"recovery-candidate builder contract missing: {token}")
for token in (
    "--next-zu qt u qs v v_snap out_ax out_snap",
    "call build_next_candidate(.false.,.false.,.false.,.false.,.false.,.false.,.true.)",
    "input_carrier='U-RAW-FLUX'",
    "output_carrier='V2-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-QV-AA1'",
    "latest_output='V'",
    "previous_output='U'",
    ".true.,'Z-RAW-FLUX'",
):
    require(token in builder,
            f"qv-candidate builder contract missing: {token}")
for token in (
    "--consecutive x1_pub x2 x3 x3_snap out_ax out_snap",
    "call load_state(trim(path(1)),x0,'x1 proposal',.true.,'V-RAW-FLUX')",
    "carrier_marker='X3-RAW-FLUX'",
    "report_prefix='RANK2-CONSECUTIVE-AA1'",
):
    require(token in builder,
            f"consecutive builder contract missing: {token}")
for token in (
    "--consecutive-returned x2 x3 x4 x4_snap out_ax out_snap",
    "consecutive_returned_mode=.true.",
    "call load_state(trim(path(1)),x0,'x2 returned')",
    "carrier_marker='X4-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1'",
):
    require(token in builder,
            f"latest builder contract missing: {token}")

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

for token in (
    "--next x1 x2 y z z_snap basis",
    "call modal_pair_geometry(state_x1,state_x2,state_y,state_z",
    "beta=(p_sq-p_dot_q)/denominator",
    "affine_a=weight_x2*state_x2%coordinates+beta*state_z%coordinates",
    "affine_l=weight_x2*state_x2%leakage+beta*state_z%leakage",
    "'Z-RAW-FLUX'",
    "call compare_axial_carrier_metadata(state_z,state_proposal,",
    "call validate_input_snapshot(z_snap_name,state_y,state_z,latest_input,",
    "FIXED-SOURCE K DIFFERS FROM",
    "call compare_snapshot_root_carrier(x2_root,proposal_root)",
    "call compare_table_except_leakage(x2_flux,proposal_flux",
    "call compare_named_record(carrier,proposal_root,name,length_left",
    "if (name /= 'SPOT-LEAK1D')",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"next checker contract missing: {token}")

for token in (
    "--u y z w v v_snap basis",
    "if (trim(mode_argument) == '--u')",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='V-RAW-FLUX'",
    "report_prefix='RANK2-MODAL-AA1-U'",
    "call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Y',",
    "call compare_axial_carrier_payload(z_name,proposal_name)",
    "count_table_records(proposal_root) /= expected_count",
    "V-RAW-FLUX",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
):
    require(token in checker, f"u checker contract missing: {token}")
for token in (
    "--next-x4 x3 x4 qy z z_snap basis",
    "x4_history_mode=.true.",
    "input_carrier='X4-RAW-FLUX'",
    "output_carrier='Z-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-AA1-NEXT'",
    "latest_input='QY'",
    "latest_output='Z'",
    "previous_output='X4'",
    "'PREVIOUS MAP INPUT X3'",
):
    require(token in checker,
            f"latest-next checker contract missing: {token}")
for token in (
    "--next-x4z qy z qt u u_snap basis",
    "x4z_history_mode=.true.",
    "input_carrier='Z-RAW-FLUX'",
    "output_carrier='U-RAW-FLUX'",
    "report_prefix='RANK2-LATEST2-AA1-NEXT'",
    "latest_input='QT'",
    "latest_output='U'",
    "previous_output='Z'",
    "'PREVIOUS PROPOSAL QY'",
    "'X4-RAW-FLUX'",
):
    require(token in checker,
            f"recovery-candidate checker contract missing: {token}")
for token in (
    "--next-zu qt u qs v v_snap basis",
    "zu_history_mode=.true.",
    "input_carrier='U-RAW-FLUX'",
    "output_carrier='V2-RAW-FLUX'",
    "report_prefix='RANK2-LATEST-QV-AA1'",
    "latest_input='QS'",
    "latest_output='V'",
    "previous_output='U'",
    "'PREVIOUS PROPOSAL QT'",
    "'Z-RAW-FLUX'",
):
    require(token in checker,
            f"qv-candidate checker contract missing: {token}")
for token in (
    "--consecutive x1_pub x2 x3",
    "call load_state(trim(path(1)),2,x0,'X1 PROPOSAL','V-RAW-FLUX')",
    "proposal_carrier='X3-RAW-FLUX'",
    "call validate_input_snapshot(trim(path(4)),x1,x2,'X2','X3')",
    "call compare_axial_carrier_payload(trim(path(3)),trim(path(6)))",
    "report_prefix='RANK2-CONSECUTIVE-AA1'",
):
    require(token in checker,
            f"consecutive checker contract missing: {token}")
for token in (
    "--consecutive-returned x2 x3 x4",
    "consecutive_returned_mode=.true.",
    "call load_state(trim(path(1)),1,x0,'X2 RETURNED')",
    "proposal_carrier='X4-RAW-FLUX'",
    "call validate_input_snapshot(trim(path(4)),x1,x2,'X3','X4')",
    "report_prefix='RANK2-LATEST-AA1'",
):
    require(token in checker,
            f"latest checker contract missing: {token}")
for token in (
    "--post-aa1 x2 x3 aa1 aa1p",
    "post_aa1_mode=.true.",
    "input_carrier='X3-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
    "report_prefix='RANK2-POST-AA1'",
    "latest_input='AA1'",
    "latest_output='AA1-PLUS'",
    "call load_state(x1_name,1,state_x1,'PREVIOUS MAP INPUT X2')",
):
    require(token in checker,
            f"post-AA1 checker contract missing: {token}")
for token in (
    "--rolling-aa1 aa1 aa1p xnext",
    "rolling_mode=.true.",
    "input_carrier='AA1-RAW-FLUX'",
    "output_carrier='XNP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL-AA1'",
    "latest_input='XNEXT'",
    "latest_output='XNEXT-P'",
    "previous_output='AA1-PLUS'",
    "'PREVIOUS PROPOSAL AA1'",
):
    require(token in checker,
            f"rolling-AA1 checker contract missing: {token}")
for token in (
    "trim(mode_argument) == '--rolling-aa1-next'",
    "rolling_next_mode=.true.",
    "input_carrier='XNP-RAW-FLUX'",
    "output_carrier='XRP-RAW-FLUX'",
    "report_prefix='RANK2-ROLL2-AA1'",
    "latest_input='XROLL'",
    "latest_output='XROLL-P'",
    "previous_output='XNEXT-P'",
    "'PREVIOUS PROPOSAL XNEXT'",
):
    require(token in checker,
            f"rolling-next-AA1 checker contract missing: {token}")
for record in (
    "SPOT-X-RRHO", "SPOT-X-RLEAK", "SPOT-X-DLEAK", "SPOT-X-RA",
    "SPOT-X-PERP", "SPOT-X-EPOCH", "SPOT-GBAL", "SPOT-GBAL-MA",
):
    require(record in checker, f"u full-carrier stale gate missing: {record}")

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

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_next_candidate_inputs.tsv",
    "--next x1.xsm x2.xsm y_pub.xsm z.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in next_runner, f"next runner binding missing: {name}")
next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", next_runner
)
require(len(next_expected) == 2 and
        all(re.fullmatch(r"[0-9a-f]{64}", value)
            for value in next_expected),
        "next output SHA-256 values are not frozen")
require(not re.search(r"(?m)^\s*(?:while|until)\b", next_runner),
        "next runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_u_candidate_inputs.tsv",
    "--u y.xsm z.xsm w.xsm v.xsm vs.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in u_runner, f"u runner binding missing: {name}")
u_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", u_runner
)
require(u_expected == [
    "77a4bc3916db21064dc2bae73a0397faeb15fb8033de6f761fcaa4cfd0f6852b",
    "2f526c84f4ef42afd51178dde9481ff7336c0de5b0ff486135635a0b7fc79a81",
], "u output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", u_runner),
        "u runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_consecutive_candidate_inputs.tsv",
    "--consecutive x1.xsm x2.xsm x3.xsm x3s.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in consecutive_runner,
            f"consecutive runner binding missing: {name}")
consecutive_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", consecutive_runner
)
require(consecutive_expected == [
    "7094d4dc57156aae8f0d0180bcac24bf02640f5de0435b46635151ed975186f1",
    "ebd0d7f0ca762f907f6d767273298b80262039f22cc4b36682d73a15d34065b2",
], "consecutive output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", consecutive_runner),
        "consecutive runner retry loops are forbidden")

for token in (
    "--consecutive-ptu-screened",
    "RANK2-CURRENT-PTU-AA1",
    "X4-RAW-FLUX",
    "PARAMETER-FREE DIRECTION GATE PASS",
):
    require(token in builder, f"PTU builder contract missing: {token}")
    require(token in checker, f"PTU checker contract missing: {token}")
for token in (
    "rank2_current_ptu_aa1_candidate_inputs.tsv",
    "--consecutive-ptu-screened",
    "p.xsm t.xsm u.xsm us.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in ptu_runner, f"PTU runner binding missing: {token}")
ptu_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", ptu_runner
)
require(ptu_expected == [
    "75dd254844b001596f3e57e6aad373e6bdec7aa84958e79b9111c555e93556cf",
    "169be7e8f17e7b1985b65ae2522966bbba0768febadb2a031f0e0a860e0a11fd",
], "PTU output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", ptu_runner),
        "PTU runner retry loops are forbidden")
require("spot-rank2-current-ptu-aa1-candidate" in
        (ROOT / "Makefile").read_text(), "PTU Make target is missing")

for token in (
    "--next-x4aa2-screened",
    "RANK2-CURRENT-QVWX-AA1",
    "AA2-RAW-FLUX",
    "AA1-RAW-FLUX",
    "PARAMETER-FREE DIRECTION GATE PASS",
):
    require(token in builder, f"QVWX builder contract missing: {token}")
    require(token in checker, f"QVWX checker contract missing: {token}")
for token in (
    "rank2_current_qvwx_aa1_candidate_inputs.tsv",
    "CANDIDATE_MODE=${CANDIDATE_MODE:---next-x4aa2-screened}",
    "--next-x4aa2-screened)", "--next-aa1aa2-screened)",
    './build_candidate "$CANDIDATE_MODE" q.xsm v.xsm w.xsm x.xsm',
    './check_candidate "$CANDIDATE_MODE" q.xsm v.xsm w.xsm x.xsm',
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in qvwx_runner, f"QVWX runner binding missing: {token}")
qvwx_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", qvwx_runner
)
require(qvwx_expected == [
    "012ccd8e428e7a819ce41cec70eab90745e92dc1bb95735a35631f3ef0e2057d",
    "8942bf5ca0c2f551200dcf78508093a34da39636c5fe57f167a05b4d1da37504",
], "QVWX output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qvwx_runner),
        "QVWX runner retry loops are forbidden")
require("spot-rank2-current-qvwx-aa1-candidate" in
        (ROOT / "Makefile").read_text(), "QVWX Make target is missing")

for token in (
    "--next-aa1aa2-screened",
    "RANK2-CURRENT-GH-AA1",
    "'previous proposal input',.true.,'AA1-RAW-FLUX'",
    "input_carrier='AA2-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
):
    require(token in builder, f"GH builder contract missing: {token}")
for token in (
    "--next-aa1aa2-screened",
    "RANK2-CURRENT-GH-AA1",
    "'PREVIOUS PROPOSAL Q1'", "'AA1-RAW-FLUX'",
    "input_carrier='AA2-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
):
    require(token in checker, f"GH checker contract missing: {token}")

for token in (
    "--next-aa1aa2-ij-screened",
    "RANK2-CURRENT-IJ-AA1",
    "'previous proposal input',.true.,'AA1-RAW-FLUX'",
    "input_carrier='AA2-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
):
    require(token in builder, f"IJ builder contract missing: {token}")
for token in (
    "--next-aa1aa2-ij-screened",
    "RANK2-CURRENT-IJ-AA1",
    "'PREVIOUS PROPOSAL Q3'", "'AA1-RAW-FLUX'",
    "latest_input='Q4'", "latest_output='J'", "previous_output='I'",
):
    require(token in checker, f"IJ checker contract missing: {token}")
for token in (
    "--next-aa2aa1-jk-screened",
    "RANK2-CURRENT-JK-AA1",
    "'previous proposal input',.true.,'AA2-RAW-FLUX'",
    "input_carrier='AA1-RAW-FLUX'",
    "output_carrier='AA1-RAW-FLUX'",
):
    require(token in builder, f"JK builder contract missing: {token}")
for token in (
    "--next-aa2aa1-jk-screened",
    "RANK2-CURRENT-JK-AA1",
    "'PREVIOUS PROPOSAL Q4'", "'AA2-RAW-FLUX'",
    "latest_input='Q5'", "latest_output='K'", "previous_output='J'",
):
    require(token in checker, f"JK checker contract missing: {token}")
for token in (
    "--next-aa1aa2-ij-screened)",
    "RANK2-CURRENT-IJ-AA1",
    "# spot-rank2-current-ij-aa1-candidate-inputs-v1",
    "27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743",
    "f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c",
):
    require(token in qvwx_runner, f"IJ runner binding missing: {token}")
ij_makefile = (ROOT / "Makefile").read_text()
for token in (
    "spot-rank2-current-ij-aa1-candidate",
    "rank2_current_ij_aa1_candidate_inputs.tsv",
    "iterative-rank2-current-ij-aa1-candidate",
    "CANDIDATE_MODE=--next-aa1aa2-ij-screened",
    "REPORT_PREFIX=RANK2-CURRENT-IJ-AA1",
    "EXPECTED_AX_SHA_OVERRIDE=27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743",
    "EXPECTED_SNAP_SHA_OVERRIDE=f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c",
):
    require(token in ij_makefile, f"IJ Make binding missing: {token}")
for token in (
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "1.1922339465680236", "0.19223394656802359",
    "1.1217162258501826e-11", "0.064424480296712869",
    "0.93186663298811390", "0.97357313211276764",
    "8880/8880", "standard", "unconstrained AA(1)", "not clipped",
    "27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743",
    "f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c",
    "00a4011204736be578dd2c65eb94f6505e4fde0e7a29c593e044210f37261752",
    "No Dragon", "No", "AA(2)",
):
    require(token in ij_result, f"IJ candidate result missing: {token}")
gh_makefile = (ROOT / "Makefile").read_text()
for token in (
    "spot-rank2-current-gh-aa1-candidate",
    "rank2_current_gh_aa1_candidate_inputs.tsv",
    "iterative-rank2-current-gh-aa1-candidate",
    "CANDIDATE_MODE=--next-aa1aa2-screened",
    "REPORT_PREFIX=RANK2-CURRENT-GH-AA1",
    "EXPECTED_AX_SHA_OVERRIDE=c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6",
    "EXPECTED_SNAP_SHA_OVERRIDE=3cd88d1d7f65ad05cc7a62025cb12a2d50bc016a52d35b251685da71c559b37f",
):
    require(token in gh_makefile, f"GH Make binding missing: {token}")
for token in (
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "0.92198482219461153", "0.078015177805388483",
    "7.3007449964465324e-13", "0.11971305975561962",
    "0.47525043616253554", "0.70441518119387303",
    "c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6",
    "3cd88d1d7f65ad05cc7a62025cb12a2d50bc016a52d35b251685da71c559b37f",
    "8b7ddf314b8d62c5a60cf3eb75b341157dcdb5ebfa90307d8bf41a2909beafa6",
):
    require(token in gh_result, f"GH candidate result missing: {token}")

qvwx_zplus_rows = [
    line.split() for line in qvwx_zplus_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(qvwx_zplus_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-zplus-aa1-candidate-inputs-v1",
        "QVWX-ZPLUS manifest version changed")
require(tuple(row[0] for row in qvwx_zplus_rows) == (
    "y_aa1_pub", "z", "z_plus", "z_plus_snapshots", "basis_reference"
), "QVWX-ZPLUS manifest roles changed")
require(all(len(row) == 3 for row in qvwx_zplus_rows),
        "QVWX-ZPLUS manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1])
            for row in qvwx_zplus_rows),
        "QVWX-ZPLUS manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in qvwx_zplus_rows),
        "QVWX-ZPLUS manifest path escapes the repository")
for token in (
    "--consecutive-qvwx-zplus-screened",
    "RANK2-QVWX-ZPLUS-AA1",
    "AA1-RAW-FLUX",
    "PARAMETER-FREE DIRECTION GATE PASS",
):
    require(token in builder,
            f"QVWX-ZPLUS builder contract missing: {token}")
    require(token in checker,
            f"QVWX-ZPLUS checker contract missing: {token}")
for token in (
    "rank2_current_qvwx_zplus_aa1_candidate_inputs.tsv",
    "MODE=${MODE:---consecutive-qvwx-zplus-screened}",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in qvwx_zplus_runner,
            f"QVWX-ZPLUS runner binding missing: {token}")
qvwx_zplus_expected = [
    "5d462c634e7f909ff059d72ac8bb8d9240cb18c21232c682c99d8f34d791c67c",
    "3c216fff2be1336c29e584e4b8b0d6d9eca537f80c6a5fc07bf08f4ad509eb84",
]
require(all(digest in qvwx_zplus_runner for digest in qvwx_zplus_expected),
        "QVWX-ZPLUS output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qvwx_zplus_runner),
        "QVWX-ZPLUS runner retry loops are forbidden")
require("spot-rank2-current-qvwx-zplus-aa1-candidate" in
        (ROOT / "Makefile").read_text(),
        "QVWX-ZPLUS Make target is missing")

kl_rows = [line.split() for line in kl_manifest.splitlines()
           if line.strip() and not line.startswith("#")]
require(kl_manifest.splitlines()[0] ==
        "# spot-rank2-current-kl-aa1-candidate-inputs-v1",
        "KL AA1 manifest version changed")
require(tuple(row[0] for row in kl_rows) == (
    "q5_aa1_pub", "k", "l", "l_snapshots", "basis_reference"
), "KL AA1 manifest roles changed")
require(tuple(row[1] for row in kl_rows) == (
    "27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743",
    "d8c77928f992adf67136331192a018060f203bedf3d1728d46a39d987c6938de",
    "fee603751609b7a9ab79ac854e7ecfa93125f3f4597e411e020728ae267180d0",
    "9ffe3428e70f001a5f0e3384a5030fe4a0334787d7454c0f0d143b2b4a5b165f",
    "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
), "KL AA1 inputs changed")
require(all(len(row) == 3 for row in kl_rows),
        "KL AA1 manifest row width changed")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in kl_rows),
        "KL AA1 manifest path escapes the repository")
for token in (
    "--consecutive-q5kl-screened", "RANK2-CURRENT-KL-AA1",
    "previous_output='K'", "latest_output='L'", "AA1-RAW-FLUX",
):
    require(token in builder, f"KL AA1 builder contract missing: {token}")
    require(token.upper() in checker.upper(),
            f"KL AA1 checker contract missing: {token}")
for token in (
    "--consecutive-q5kl-screened:RANK2-CURRENT-KL-AA1",
    "# spot-rank2-current-kl-aa1-candidate-inputs-v1",
    "d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d",
    "c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6",
    "PROPOSAL_ROLE", "PREVIOUS_ROLE", "LATEST_ROLE",
    "LATEST_SNAPSHOTS_ROLE", "PARAMETER-FREE DIRECTION GATE PASS",
):
    require(token in qvwx_zplus_runner,
            f"KL AA1 runner binding missing: {token}")
kl_makefile = (ROOT / "Makefile").read_text()
for token in (
    "spot-rank2-current-kl-aa1-candidate",
    "rank2_current_kl_aa1_candidate_inputs.tsv",
    "iterative-rank2-current-kl-aa1-candidate",
    "MODE=--consecutive-q5kl-screened",
    "REPORT_PREFIX=RANK2-CURRENT-KL-AA1",
    "PROPOSAL_ROLE=q5_aa1_pub PREVIOUS_ROLE=k LATEST_ROLE=l",
    "LATEST_SNAPSHOTS_ROLE=l_snapshots",
):
    require(token in kl_makefile, f"KL AA1 Make binding missing: {token}")
for token in (
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "0.99334779753418823", "0.0066522024658117341",
    "3.9604495076589152e-13", "0.81736979605403082",
    "0.80173988821917219", "0.90621455552995278",
    "8880/8880",
    "d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d",
    "c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6",
    "c0ca1244186e3b70e23efde028cb5bb2fd04a215364cf8728abc95250bcf4e6e",
    "No Dragon", "AA(2) was not calculated", "empirical",
):
    require(token in kl_result, f"KL AA1 result missing: {token}")

cef_rows = [line.split() for line in cef_manifest.splitlines()
            if line.strip() and not line.startswith("#")]
require(cef_manifest.splitlines()[0] ==
        "# spot-rank2-current-qvwx-zplus-aa1-candidate-inputs-v1",
        "CEF AA1 manifest version changed")
require(tuple(row[0] for row in cef_rows) == (
    "y_aa1_pub", "z", "z_plus", "z_plus_snapshots", "basis_reference"
), "CEF AA1 manifest roles changed")
require(tuple(row[1] for row in cef_rows) == (
    "978593b2813bad2242ad8c235fdd83e6f5bc33b3aff624b60ccecaaf077d95c6",
    "0b5c8d27b4d2e37d90d56d27d75619842851b7a0e0206947b31c3d5b88936828",
    "6e26d8dc40bf79c0dedad19912557dfed5ccd2c3bdb38ea719ce32b5cc9aba6c",
    "4e6ede5bb7253999850d8306c8f0683df9c6191e4dc5f19b2381b10f56fb0a2d",
    "2d7fc2bf36f65a203731c34dcea18a679fc0232b58c59caad828178a77ff45a8",
), "CEF AA1 inputs changed")
makefile = (ROOT / "Makefile").read_text()
for token in (
    "spot-rank2-current-cef-aa1-candidate",
    "rank2_current_cef_aa1_candidate_inputs.tsv",
    "iterative-rank2-current-cef-aa1-candidate",
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "5b7d6d7c0cf00a4097284b53816d7e3c91ca4e27656f0bc437f6a0472555ac68",
    "run_rank2_current_qvwx_zplus_aa1_candidate.sh",
):
    require(token in makefile, f"CEF AA1 Make binding missing: {token}")
for token in (
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "0.54317069088638781",
    "0.45682930911361219",
    "3.3988810913576900e-12",
    "0.059424727376440133",
    "0.19596354669013863",
    "0.28717479223258224",
    "76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd",
    "5b7d6d7c0cf00a4097284b53816d7e3c91ca4e27656f0bc437f6a0472555ac68",
    "9/9 receipt",
    "No Dragon, ASM, FLU, transport, or physical map was run",
):
    require(token in cef_result, f"CEF AA1 result missing: {token}")

zpcd_rows = [
    line.split() for line in zpcd_manifest.splitlines()
    if line.strip() and not line.startswith("#")
]
require(zpcd_manifest.splitlines()[0] ==
        "# spot-rank2-current-zpcd-aa1-candidate-inputs-v1",
        "ZPCD manifest version changed")
require(tuple(row[0] for row in zpcd_rows) == (
    "z", "z_plus", "c_aa1_pub", "d", "d_snapshots", "basis_reference"
), "ZPCD manifest roles changed")
require(all(len(row) == 3 for row in zpcd_rows),
        "ZPCD manifest row width changed")
require(all(re.fullmatch(r"[0-9a-f]{64}", row[1]) for row in zpcd_rows),
        "ZPCD manifest contains an invalid SHA-256")
require(all(not Path(row[2]).is_absolute() and
            ".." not in Path(row[2]).parts for row in zpcd_rows),
        "ZPCD manifest path escapes the repository")
for token in (
    "--next-zpcd-screened",
    "RANK2-CURRENT-ZPCD-AA1",
    "AA1-RAW-FLUX",
    "PARAMETER-FREE DIRECTION GATE PASS",
):
    require(token in builder, f"ZPCD builder contract missing: {token}")
    require(token in checker, f"ZPCD checker contract missing: {token}")
for token in (
    "rank2_current_zpcd_aa1_candidate_inputs.tsv",
    "--next-zpcd-screened z.xsm zp.xsm c.xsm d.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in zpcd_runner, f"ZPCD runner binding missing: {token}")
zpcd_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", zpcd_runner
)
require(zpcd_expected == [
    "978593b2813bad2242ad8c235fdd83e6f5bc33b3aff624b60ccecaaf077d95c6",
    "cf43ed781a1f86625aa6ae46023eca2e6e000ed76d16c81470a3544b13bb0354",
], "ZPCD output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", zpcd_runner),
        "ZPCD runner retry loops are forbidden")
require("spot-rank2-current-zpcd-aa1-candidate" in
        (ROOT / "Makefile").read_text(), "ZPCD Make target is missing")
for token in (
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "0.48771444550122545",
    "0.51228555449877455",
    "3.7547749561704630e-14",
    "0.99411674241637549",
    "0.93884958302279575",
    "0.79362266755606770",
    "8880/8880",
    "9/9 receipt",
    "4f47ca2e50e4038fb980cf3ccfa6a4b9998ecf793e6caaec6d06ca4ff1b0d96c",
):
    require(token in zpcd_result,
            f"ZPCD candidate result boundary missing: {token}")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_candidate_inputs.tsv",
    "--consecutive-returned",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in latest_runner, f"latest runner binding missing: {name}")
latest_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", latest_runner
)
require(latest_expected == [
    "0c7d94c9df4b1a7f7f94b8a9d54eb51aacfcead8ab34d5f288c85351b1c0ab9d",
    "b5d03cb519ce54f0ade469288f70a50e303bb6a7bd7d4396c04558d38ffd108b",
], "latest output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_runner),
        "latest runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-candidate" in
        (ROOT / "Makefile").read_text(), "latest Make target is missing")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_next_candidate_inputs.tsv",
    "--next-x4 x3.xsm x4.xsm qy_pub.xsm z.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in latest_next_runner,
            f"latest-next runner binding missing: {name}")
latest_next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", latest_next_runner
)
require(latest_next_expected == [
    "e9e37246df25ef9afb449fad77e55b6ce21cd03f09e2f185d458aea4bd85d28c",
    "8414fb2298bcd9797f5d1b0613d985413c7c87d533feb80e8f24360471c05b38",
], "latest-next output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", latest_next_runner),
        "latest-next runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-next-candidate" in
        (ROOT / "Makefile").read_text(),
        "latest-next Make target is missing")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_recovery_candidate_inputs.tsv",
    "--next-x4z qy_pub.xsm z.xsm qt_pub.xsm u.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in recovery_runner,
            f"recovery-candidate runner binding missing: {name}")
recovery_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", recovery_runner
)
require(recovery_expected == [
    "53f6bb3e48ef583778e54ce0e21ff68f5f63d3d3857c3211c0803bc9a2ef0193",
    "3404d4295b8f71fa20d9b565fc88c0631184775dcac336be2f50e797999cefaa",
], "recovery-candidate output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", recovery_runner),
        "recovery-candidate runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-recovery-candidate" in
        (ROOT / "Makefile").read_text(),
        "recovery-candidate Make target is missing")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_latest_modal_aa1_qv_candidate_inputs.tsv",
    "--next-zu qt_pub.xsm u.xsm qs_pub.xsm v.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in qv_runner,
            f"qv-candidate runner binding missing: {name}")
qv_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", qv_runner
)
require(qv_expected == [
    "bdfc6f8c1a0e4c0d2eb02bffd218cace6bd263ad25bc5439f17751376417549f",
    "b6a92d2c553f535b0066a63e644423cae22848cd012492f89d0cbff535704490",
], "qv-candidate output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qv_runner),
        "qv-candidate runner retry loops are forbidden")
require("spot-rank2-latest-modal-aa1-qv-candidate" in
        (ROOT / "Makefile").read_text(),
        "qv-candidate Make target is missing")
for token in (
    "Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`",
    "3.43937066250607248",
    "-2.43937066250607248",
    "V2-RAW-FLUX",
    "8880 / 8880",
    "passing 9/9 receipt",
    "does not authorize a map",
):
    require(token in qv_result,
            f"qv-candidate result boundary missing: {token}")

for token in (
    "--consecutive-current",
    "U-RAW-FLUX",
    "RANK2-QSVW-AA1",
    "LEAKAGE-AFFINE-L2/CURRENT SAME-MODAL-BETA",
    "LEAKAGE SCREEN ONLY NO LEAKAGE FIT",
):
    require(token in builder, f"qsvw builder contract missing: {token}")
for token in (
    "--consecutive-current",
    "U-RAW-FLUX",
    "RANK2-QSVW-AA1",
    "LEAKAGE AFFINE L2/CURRENT SAME-MODAL-BETA",
    "LEAKAGE SCREEN ONLY NO LEAKAGE FIT",
):
    require(token in checker, f"qsvw checker contract missing: {token}")
for token in (
    "rank2_qsvw_aa1_candidate_inputs.tsv",
    "--consecutive-current qs.xsm v.xsm w.xsm ws.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(token in qsvw_runner,
            f"qsvw-candidate runner binding missing: {token}")
qsvw_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", qsvw_runner
)
require(qsvw_expected == [
    "18860e284a02f104821a6eba26ea7743863ccf1193e01089389685648ef7f6c0",
    "77a3f082955c42ecdcae925a8b52f40217e129715123eca4c5fb45ce6c9440e8",
], "qsvw-candidate output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", qsvw_runner),
        "qsvw-candidate runner loops are forbidden")
require("spot-rank2-qsvw-aa1-candidate" in
        (ROOT / "Makefile").read_text(),
        "qsvw-candidate Make target is missing")
for token in (
    "Classification: `MATERIALIZED_PROPOSAL_NOT_EVALUATED`",
    "0.58613211193957626",
    "0.59562646285803311",
    "0.59916457255893851",
    "8880/8880",
    "passing 9/9",
):
    require(token in qsvw_result,
            f"qsvw-candidate result boundary missing: {token}")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_post_candidate_inputs.tsv",
    "--post-aa1 x2.xsm x3.xsm aa1.xsm aa1p.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in post_runner, f"post-AA1 runner binding missing: {name}")
post_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", post_runner
)
require(post_expected == [
    "58972931170d744f109550866b65a8d2cbf22204ef1fe99cef634c4187d59d89",
    "0c22cc9748beb813757d154ca592f343654e61c710f9b852ad35270ae19e186c",
], "post-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", post_runner),
        "post-AA1 runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_rolling_candidate_inputs.tsv",
    "--rolling-aa1 aa1.xsm aa1p.xsm xnext.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in rolling_runner,
            f"rolling-AA1 runner binding missing: {name}")
rolling_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", rolling_runner
)
require(rolling_expected == [
    "a7166bdfff6a477542118e5f355eacd4e0018c496717cac845df0cd6233108ee",
    "6762e58a75cc2bcbffae476187389797a9aebf95e8619355060b6de9c41b5102",
], "rolling-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", rolling_runner),
        "rolling-AA1 runner retry loops are forbidden")

for name in (
    "build_rank2_modal_aa1_candidate.f90",
    "check_rank2_modal_aa1_candidate.f90",
    "rank2_modal_aa1_rolling_next_candidate_inputs.tsv",
    "--rolling-aa1-next xnext.xsm xnextp.xsm xroll.xsm",
    "proposal_axial.xsm",
    "proposal_snapshots.xsm",
    "MATERIALIZED_PROPOSAL_NOT_EVALUATED",
    "DRAGON/ASM/FLU/TRANSPORT=0",
):
    require(name in rolling_next_runner,
            f"rolling-next-AA1 runner binding missing: {name}")
rolling_next_expected = re.findall(
    r"(?m)^EXPECTED_(?:AX|SNAP)_SHA=([^\n]+)$", rolling_next_runner
)
require(rolling_next_expected == [
    "5a40b39d7945cfd36c1f2b092c207b5cffb019c7a414ea8b84c478da5174e394",
    "c27fee3d0d396c4427a7389c123b044a8ec61e274a6348b9f83343fb167313ee",
], "rolling-next-AA1 output SHA-256 values changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", rolling_next_runner),
        "rolling-next-AA1 runner retry loops are forbidden")

combined = "\n".join((builder, checker, runner, next_runner,
                       u_runner, consecutive_runner, ptu_runner, qvwx_runner,
                       qvwx_zplus_runner, zpcd_runner,
                       latest_runner,
                       latest_next_runner, recovery_runner, qv_runner,
                       qsvw_runner,
                       post_runner,
                       rolling_runner, rolling_next_runner)).lower()
for forbidden in ("relaxation", "damping", "clipping", "empirical factor"):
    require(forbidden not in combined,
            f"forbidden empirical control present: {forbidden}")

print("RANK2 MODAL AA1 CONTRACT PASS: nineteen hash-locked offline proposals, "
      "binary publication, fixed basis, strict positivity and no map solve.")

#!/usr/bin/env python3
"""Static fail-closed contract for the bounded production capture runner."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITER = ROOT / "validation" / "iterative"
PROTOCOL = ITER / "raw_moc_capture_run_protocol.json"
REFERENCE = ITER / "raw_moc_capture_run_reference.sha256"
IMPLEMENTATION = ITER / "raw_moc_capture_run_implementation.sha256"

FILES = {
    "deck": ITER / "raw_moc_capture_probe.x2m.in",
    "bounded runner": ITER / "run_bounded_dragon.py",
    "bounded tests": ITER / "test_bounded_dragon.py",
    "log checker": ITER / "check_raw_moc_capture_run_logs.py",
    "log tests": ITER / "test_raw_moc_capture_run_logs.py",
    "production runner": ITER / "run_raw_moc_capture_production.sh",
    "capture checker": ITER / "check_raw_moc_capture_xsm.f90",
    "capture implementation": ITER / "raw_moc_capture_implementation.sha256",
    "parent receipt": ITER / "radial_floor_result_receipt.sha256",
    "prepare deck": ITER / "radial_floor_prepare.x2m",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RAW-MOC-RUN CONTRACT FAIL: {message}")


def read(name: str) -> str:
    path = FILES[name]
    require(path.is_file() and not path.is_symlink(), f"invalid {name}")
    return path.read_text(encoding="utf-8")


for path in (PROTOCOL, REFERENCE):
    require(path.is_file() and not path.is_symlink(), f"invalid {path.name}")

protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
require(
    protocol["status"] == "FROZEN-BEFORE-PRODUCTION-RUN",
    "run protocol is not frozen before execution",
)
require(
    protocol["source_commit"]
    == "d97a70225b118b2369c94e664b8e9028a1e4a704",
    "capture source commit changed",
)
require(
    protocol["activation"]
    == {
        "default": "PREFLIGHT-ONLY",
        "production_environment": "RUN_CAPTURE=1",
        "other_values": "FAIL-CLOSED",
    },
    "activation gate changed",
)
require(
    protocol["executable"]["sha256"]
    == "b57cb801aeec62e7306897e10f84bca1ad6b011055a651ff37aa1718e6b2b1e5",
    "capture-capable executable hash changed",
)
require(
    protocol["executable"]["clean_git_archive_sha256"]
    == "358fdd0f4b694e6717bbb21aa07e365276437df09fec14d62d3fb710c71cd4e2",
    "clean source archive hash changed",
)
require(
    protocol["parent_evidence"]["plane"] == 1,
    "capture is no longer bound to plane 1",
)
require(
    protocol["parent_evidence"]["result_receipt_sha256"]
    == "8b440f48e4fb7293d72ee4051dd17ff2c897b5dcce9dc14417fab68ffc0a4d1f"
    and protocol["parent_evidence"]["compact_minimal_manifest_sha256"]
    == "f096043e06d68b7cc2fe8b5d246a815d2ab4ca8be2275e00a0d6b485901e5c6c"
    and protocol["parent_evidence"]["compact_full_manifest_sha256"]
    == "b5ada48abade897f115e68fa227a6ac256a5c92441bad66fc8fc8444030dfad3",
    "parent evidence hashes changed",
)
require(
    protocol["frozen_inputs"]["common"]
    == {
        "restart_macro0.xsm": "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
        "restart_source.xsm": "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
        "restart_system.xsm": "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
        "restart_track.xsm": "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
        "initial_radial_track.bin": "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    },
    "common frozen-input identities changed",
)
require(
    protocol["frozen_inputs"]["arms"]
    == [
        {
            "name": "NATIVE",
            "arm_code": 1,
            "pre_sha256": "663a8257b1ecafa2dde9c36d7cff8ccd8201a08fe2b117cdccad46c305e5bea9",
            "frozen_sha256": "df24abbfe1f15e91948e5b930229e09aa13410e1b8985a61a74c8d28db08e208",
        },
        {
            "name": "STATIONARY",
            "arm_code": 2,
            "pre_sha256": "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e",
            "frozen_sha256": "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789",
        },
    ],
    "arm label/hash binding changed",
)
require(
    protocol["probe_controls"]
    == {
        "TYPE": "S",
        "door": "MCCG",
        "INITFL": "ON",
        "rebalancing": "ON",
        "MAXOUT": 1,
        "MAXINR": 740,
        "EPSOUT_decimal": "2.5E-7",
        "EPSUNK_decimal": "2.5E-7",
        "EPSINR_decimal": "2.5E-7",
        "epsilon_binary32_bits": "348637BD",
        "free_steps": 1,
        "accelerated_steps": 0,
        "direct": True,
        "ILEAK": 0,
    },
    "probe controls changed",
)
require(
    protocol["run_matrix"]
    == [
        {"arm": "NATIVE", "mode": "OFF", "MOCA": "ABSENT"},
        {"arm": "NATIVE", "mode": "ON", "MOCA": 1},
        {"arm": "STATIONARY", "mode": "OFF", "MOCA": "ABSENT"},
        {"arm": "STATIONARY", "mode": "ON", "MOCA": 2},
    ],
    "four-process run matrix changed",
)
require(
    protocol["execution_budget"]
    == {
        "production_probe_processes": 4,
        "updates_per_process": 1,
        "wall_timeout_seconds_per_dragon_process": 30,
        "timeout_classification": "INVALID-NO-SCIENTIFIC-RESULT",
        "termination_scope": "exact spawned process group; never killall",
    },
    "execution budget changed",
)
require(
    protocol["classification"]
    == {
        "valid": "CAPTURE-VALID",
        "invalid": "CAPTURE-INVALID",
        "acceptance_threshold": None,
        "outer_convergence_evaluated": False,
        "stage4_authorization": False,
        "stage5_authorization": False,
    },
    "scientific classification changed",
)

reference_rows = [
    line.split()
    for line in REFERENCE.read_text(encoding="ascii").splitlines()
    if line.strip()
]
reference = {label: digest for digest, label in reference_rows}
expected_reference = {
    "Dragon": "b57cb801aeec62e7306897e10f84bca1ad6b011055a651ff37aa1718e6b2b1e5",
    "clean_git_archive.tar": "358fdd0f4b694e6717bbb21aa07e365276437df09fec14d62d3fb710c71cd4e2",
    "raw_moc_capture_implementation.sha256": "35c61aed647f3be452f04226830e726c4dca439e0549b05fbbd3ee40c4c64913",
    "radial_floor_result_receipt.sha256": "8b440f48e4fb7293d72ee4051dd17ff2c897b5dcce9dc14417fab68ffc0a4d1f",
    "minimal_manifest.sha256": "f096043e06d68b7cc2fe8b5d246a815d2ab4ca8be2275e00a0d6b485901e5c6c",
    "full_artifact_manifest.sha256": "b5ada48abade897f115e68fa227a6ac256a5c92441bad66fc8fc8444030dfad3",
    "prepared_manifest.sha256": "a96d6535028870f0271c6e73478e1548d60b8ed501202ed28b95aea922144905",
    "radial_floor_prepare.x2m": "75ffc586d51c7015daa979ec381f32fb7a7475de0aa81dbc5d7735b681574c2f",
    "check_raw_moc_capture_xsm.f90": "1a50431a8279bb98745d9416be81e3848586be2c53ccdb800c561a631792c66a",
    "restart_macro0.xsm": "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
    "restart_source.xsm": "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
    "restart_system.xsm": "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
    "restart_track.xsm": "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
    "initial_radial_track.bin": "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    "native_pre.xsm": "663a8257b1ecafa2dde9c36d7cff8ccd8201a08fe2b117cdccad46c305e5bea9",
    "native_frozen.xsm": "df24abbfe1f15e91948e5b930229e09aa13410e1b8985a61a74c8d28db08e208",
    "stationary_pre.xsm": "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e",
    "stationary_frozen.xsm": "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789",
}
require(
    len(reference_rows) == len(expected_reference)
    and all(len(row) == 2 for row in reference_rows)
    and len(reference) == len(reference_rows)
    and reference == expected_reference,
    "reference manifest differs",
)
require(
    all(re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in reference_rows),
    "invalid reference digest",
)

actual_dependency_hashes = {
    "raw_moc_capture_implementation.sha256": hashlib.sha256(
        FILES["capture implementation"].read_bytes()
    ).hexdigest(),
    "radial_floor_result_receipt.sha256": hashlib.sha256(
        FILES["parent receipt"].read_bytes()
    ).hexdigest(),
    "radial_floor_prepare.x2m": hashlib.sha256(
        FILES["prepare deck"].read_bytes()
    ).hexdigest(),
    "check_raw_moc_capture_xsm.f90": hashlib.sha256(
        FILES["capture checker"].read_bytes()
    ).hexdigest(),
}
for label, digest in actual_dependency_hashes.items():
    require(reference[label] == digest, f"dependency hash differs for {label}")

deck = read("deck")
bounded = read("bounded runner")
bounded_tests = read("bounded tests")
log_checker = read("log checker")
log_tests = read("log tests")
runner = read("production runner")

for token, count in (
    ("@ARM@", 2),
    ("@MODE@", 2),
    ("@AUDIT_CONTROL@", 1),
    ("TYPE S INIT ON REBA", 1),
    ("EXTE <<outer_cap>> <<solver_eps>>", 1),
    ("UNKT <<solver_eps>>", 1),
    ("THER <<inner_cap>> <<solver_eps>>", 1),
    ("ACCE <<free_steps>> <<acc_steps>>", 1),
):
    require(deck.count(token) == count, f"deck token census differs: {token}")
require("outer_cap := 1" in deck, "deck MAXOUT changed")
require("inner_cap := 740" in deck, "deck MAXINR changed")
require("solver_eps := 2.5E-7" in deck, "deck epsilon changed")
require("SPOT" not in deck, "deck activates legacy SPOT")

for arm, mode, code in (
    ("NATIVE", "OFF", 1),
    ("NATIVE", "ON", 1),
    ("STATIONARY", "OFF", 2),
    ("STATIONARY", "ON", 2),
):
    control = "" if mode == "OFF" else f"MOCA {code}"
    rendered = (
        deck.replace("@ARM@", arm)
        .replace("@MODE@", mode)
        .replace("@AUDIT_CONTROL@", control)
    )
    require("@" not in rendered, f"{arm} {mode} rendering incomplete")
    require(
        rendered.count("MOCA") == (0 if mode == "OFF" else 1),
        f"{arm} {mode} audit rendering differs",
    )

for token in (
    "TIMEOUT_SECONDS = 30",
    "start_new_session=True",
    "os.killpg(process.pid, signal.SIGTERM)",
    "os.killpg(process.pid, signal.SIGKILL)",
    "no scientific result",
    "refusing to overwrite log",
):
    require(token in bounded, f"bounded runner lost {token}")
require("killall" not in bounded.lower(), "bounded runner contains killall")
for token in (
    "test_timeout_kills_exact_process_group",
    "test_refuses_existing_log",
    "test_success",
):
    require(token in bounded_tests, f"bounded process tests lost {token}")

for token in (
    "RUN_CAPTURE=${RUN_CAPTURE:-0}",
    'case "$RUN_CAPTURE" in',
    "RAW-MOC-CAPTURE PREFLIGHT PASS",
    "RAW-MOC-CAPTURE PRODUCTION NOT-RUN",
    "test ! -e \"$ARTIFACT\"",
    "native_pre.xsm",
    "native_frozen.xsm",
    "stationary_pre.xsm",
    "stationary_frozen.xsm",
    "require_distinct_inodes",
    "immutable_inputs.sha256",
    "artifact_manifest.sha256",
    'mv "$STAGE" "$ARTIFACT"',
):
    require(token in runner, f"production runner lost {token}")
gate = runner.index('if [ "$RUN_CAPTURE" = 0 ]')
first_dragon = runner.index(
    '"$BOUNDED_RUNNER" "$DRAGON_BIN" "$WORK/prepare/prepare.x2m"'
)
require(gate < first_dragon, "preflight gate occurs after first Dragon call")
run_calls = re.findall(
    r"^run_case (native_off|native_on|stationary_off|stationary_on) ",
    runner,
    re.MULTILINE,
)
require(
    run_calls
    == ["native_off", "native_on", "stationary_off", "stationary_on"],
    "production process matrix differs",
)
require("radial_floor_arm.x2m" not in runner, "runner can rerun six-step arms")
require("killall" not in runner.lower(), "production runner contains killall")
require(
    runner.count("./check_capture native/track.xsm") == 2
    and runner.count("./check_capture stationary/track.xsm") == 2,
    "independent checker replay count differs",
)
require(
    runner.count("verify_run_implementation") == 3,
    "run implementation is not verified before and after production",
)
require(
    runner.count('require_hash Dragon "$DRAGON_BIN"') == 2,
    "Dragon identity is not verified before and after production",
)
require(
    runner.count(
        'require_hash clean_git_archive.tar "$WORK/clean_git_archive.tar"'
    )
    == 2,
    "clean source archive is not verified before and after production",
)

for token in (
    "RAW-MOC-CAPTURE RUN-LOGS PASS",
    "TRACKING CALLED",
    "TOTAL NUMBER OF FLUX CALCULATIONS",
    "MOCA",
    "CPU TIME",
):
    require(token in log_checker, f"log checker lost {token}")
require(
    "subprocess" not in log_checker
    and "check_raw_moc_capture_xsm" not in log_checker,
    "log checker is not independent text parsing",
)
for token in (
    "scientific",
    "tracking",
    "moca",
    "normal",
):
    require(token.lower() in log_tests.lower(), f"log tests lost {token}")

commit_check = subprocess.run(
    [
        "git",
        "cat-file",
        "-e",
        "d97a70225b118b2369c94e664b8e9028a1e4a704^{commit}",
    ],
    cwd=ROOT,
    check=False,
    capture_output=True,
)
require(commit_check.returncode == 0, "frozen source commit is unavailable")

if IMPLEMENTATION.exists():
    rows = [
        line.split()
        for line in IMPLEMENTATION.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    expected_paths = {
        "validation/iterative/raw_moc_capture_run_protocol.json",
        "validation/iterative/raw_moc_capture_run_reference.sha256",
        "validation/iterative/raw_moc_capture_probe.x2m.in",
        "validation/iterative/run_bounded_dragon.py",
        "validation/iterative/test_bounded_dragon.py",
        "validation/iterative/check_raw_moc_capture_run_logs.py",
        "validation/iterative/test_raw_moc_capture_run_logs.py",
        "validation/iterative/check_raw_moc_capture_run_contract.py",
        "validation/iterative/run_raw_moc_capture_production.sh",
        "validation/iterative/raw_moc_capture_implementation.sha256",
        "validation/iterative/radial_floor_result_receipt.sha256",
        "validation/iterative/radial_floor_prepare.x2m",
        "validation/iterative/check_raw_moc_capture_xsm.f90",
    }
    require(
        len(rows) == len(expected_paths)
        and all(len(row) == 2 for row in rows)
        and {row[1] for row in rows} == expected_paths
        and all(re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in rows),
        "run implementation manifest census differs",
    )
    for expected, relative in rows:
        path = ROOT / relative
        require(
            path.is_file()
            and not path.is_symlink()
            and hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"run implementation hash differs for {relative}",
        )

print("RAW-MOC-CAPTURE RUN CONTRACT PASS")

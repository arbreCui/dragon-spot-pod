#!/usr/bin/env python3
"""Static, hash and safety contract for the raw-MOC ULP bridge audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
ITER = ROOT / "validation" / "iterative"
PROTOCOL = ITER / "raw_moc_ulp_bridge_protocol.json"
IMPLEMENTATION = ITER / "raw_moc_ulp_bridge_implementation.sha256"
READER = ITER / "check_raw_moc_ulp_bridge_xsm.f90"
FIXTURE = ITER / "make_raw_moc_ulp_bridge_fixture.f90"
LOG_CHECKER = ITER / "check_raw_moc_ulp_bridge_log.py"
TEST = ITER / "run_raw_moc_ulp_bridge_checker_test.sh"
RUNNER = ITER / "run_raw_moc_ulp_bridge_audit.sh"
PARENT_ARTIFACT = ROOT / "validation" / "artifacts" / "raw-moc-capture"

EXPECTED_IMPLEMENTATION_PATHS = {
    "validation/iterative/raw_moc_ulp_bridge_protocol.json",
    "validation/iterative/check_raw_moc_ulp_bridge_xsm.f90",
    "validation/iterative/make_raw_moc_ulp_bridge_fixture.f90",
    "validation/iterative/check_raw_moc_ulp_bridge_log.py",
    "validation/iterative/run_raw_moc_ulp_bridge_checker_test.sh",
    "validation/iterative/run_raw_moc_ulp_bridge_audit.sh",
    "validation/iterative/check_raw_moc_ulp_bridge_contract.py",
}


def fail(message: str) -> None:
    raise SystemExit(f"RAW-MOC-ULP CONTRACT FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path, owner: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid {owner}")


for path, owner in (
    (PROTOCOL, "protocol"),
    (IMPLEMENTATION, "implementation manifest"),
    (READER, "reader"),
    (FIXTURE, "fixture"),
    (LOG_CHECKER, "log checker"),
    (TEST, "checker test"),
    (RUNNER, "audit runner"),
):
    require_regular(path, owner)

protocol = json.loads(PROTOCOL.read_text(encoding="ascii"))
require(
    protocol["name"] == "SPOT raw-MOC binary32 ULP bridge audit"
    and protocol["version"] == 1
    and protocol["status"] == "FROZEN-BEFORE-IMPLEMENTATION",
    "protocol identity differs",
)
require(
    protocol["frozen_parent_commit"]
    == "fa8eb512769c634e819b607cfa3cd28a890cf12a",
    "frozen parent commit differs",
)
parent = protocol["parent_evidence"]
require(
    parent["capture_run_commit"]
    == "a011fd902398b47e06faa2b23d0682c9d01eef7f"
    and parent["capture_artifact_manifest_sha256"]
    == "1c2c6bbae0a81a3978b09bc158ac0ca7a408c7d6495e734fea2f8e44f48b48a4"
    and parent["capture_result_receipt_sha256"]
    == "485baab029387aeb8212647768be96b6eba438119e7d6ddcf013ccaf5e3359b5",
    "parent evidence identity differs",
)
scope = protocol["scope"]
require(
    scope["transport_runs"] == 0
    and scope["operator_applications"] == 0
    and scope["xsm_access"] == "READ-ONLY-GANLIB"
    and scope["arms"] == ["NATIVE", "STATIONARY"]
    and scope["groups"] == 370
    and scope["regions"] == 8
    and scope["unknowns"] == 14
    and scope["total_scalar_tuples_per_arm_per_ledger"] == 2960,
    "protocol scope differs",
)
rounding = protocol["rounding_contract"]
require(
    rounding["operation"]
    == (
        "IEEE-754 roundTiesToEven from the exact stored binary64 RAW "
        "value to binary32"
    )
    and rounding["conversion_count"] == 1
    and rounding["intermediate_arithmetic"] == "NONE",
    "rounding contract differs",
)
require(
    protocol["ledgers"]["RAW-BRIDGE"]["signed_step"]
    == "unsigned_bits(target)-unsigned_bits(reference)"
    and protocol["ledgers"]["PRODUCTION-STEP"]["signed_step"]
    == "unsigned_bits(target)-unsigned_bits(reference)",
    "signed-step definitions differ",
)
require(
    protocol["acceptance"]["threshold"] is None
    and protocol["acceptance"]["classification"]
    == "DESCRIPTIVE-ULP-CENSUS",
    "an acceptance threshold or new classification was introduced",
)
limits = protocol["interpretation_limits"]
require(
    all(value is False for value in limits.values()),
    "an interpretation prohibition was relaxed",
)

manifest_rows = [
    line.split()
    for line in IMPLEMENTATION.read_text(encoding="ascii").splitlines()
    if line.strip()
]
require(
    len(manifest_rows) == len(EXPECTED_IMPLEMENTATION_PATHS)
    and all(len(row) == 2 for row in manifest_rows)
    and {row[1] for row in manifest_rows} == EXPECTED_IMPLEMENTATION_PATHS
    and all(re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in manifest_rows),
    "implementation manifest census differs",
)
for expected, relative in manifest_rows:
    path = ROOT / relative
    require_regular(path, relative)
    require(sha256(path) == expected, f"implementation hash differs: {relative}")

locked_inputs = parent["locked_inputs"]
require(len(locked_inputs) == 7, "locked input census differs")
for name, record in locked_inputs.items():
    require(
        set(record) == {"path", "sha256"}
        and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is not None,
        f"invalid locked input row: {name}",
    )
    path = ROOT / record["path"]
    if PARENT_ARTIFACT.exists():
        require_regular(path, record["path"])
        require(
            sha256(path) == record["sha256"],
            f"locked input hash differs: {name}",
        )

if PARENT_ARTIFACT.exists():
    parent_manifest = PARENT_ARTIFACT / "artifact_manifest.sha256"
    parent_receipt = ITER / "raw_moc_capture_result_receipt.sha256"
    require_regular(parent_manifest, "parent artifact manifest")
    require_regular(parent_receipt, "parent result receipt")
    require(
        sha256(parent_manifest) == parent["capture_artifact_manifest_sha256"],
        "parent artifact manifest hash differs",
    )
    require(
        sha256(parent_receipt) == parent["capture_result_receipt_sha256"],
        "parent result receipt hash differs",
    )

reader = READER.read_text(encoding="ascii")
require(
    re.search(
        r"\b(LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMDIL|LCMLID|LCMLIL|"
        r"LCMDEL|LCMEQU)\b",
        reader,
        re.IGNORECASE,
    )
    is None,
    "reader source contains LCM mutation",
)
require(
    re.search(
        r"\b(call\s+)?(SPOMOC|DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|"
        r"MCGFLX|MCGMRE|SPOT1P)\b",
        reader,
        re.IGNORECASE,
    )
    is None,
    "reader source contains a solver dependency",
)
for token in (
    "round_binary64_to_binary32_bits",
    "round_shift_right_even",
    "ordered_binary32_key",
    "call require_record(root,'SPOT-MOC-AUD',-1,0,'ON')",
    "(state(5) /= 6).or.(state(6) /= 1).or.(state(9) == 1)",
    "call require_record(group_dir,'SPOT-M-QFR',nu,4",
    "call require_record(group_dir,'SPOT-M-SRC',nu,4",
    "call require_record(group_dir,'SPOT-M-STEP',1,1",
    "call require_record(group_dir,'SPOT-M-ROLE',1,1",
    "ROUND-COLLAPSED-NONZERO",
    "RAW-BRIDGE DECLARED-DIRECT-PROJECTION",
    "LEDGERS NOT-SUBTRACTED",
    "ACCEPTANCE-THRESHOLD NONE",
    "ATTRIBUTION NONE",
    "OUTER-CONVERGENCE NOT-EVALUATED",
    "STAGE4 NOT-AUTHORIZED",
):
    require(token in reader, f"reader lost required token: {token}")
require("spacing(" not in reader.lower(), "reader uses a spacing quotient")
require(
    "real(audit%raw(key,group),real32)" in reader,
    "reader lost hardware RNE cross-check",
)

fixture = FIXTURE.read_text(encoding="ascii")
require("use GANLIB" in fixture, "fixture is not Ganlib-backed")
require("SPOMOC" not in fixture.upper(), "fixture imports production capture")
for token in (
    "keyflux=[8,1,7,2,6,3,5,4]",
    "bridge_step=mod(group+2*region,7)-3",
    "production_step=mod(3*group+region,9)-4",
    "raw-bit",
    "current",
    "raw-type",
    "raw-nan",
    "key-duplicate",
    "key-alternate",
    "pre-type",
    "off-length",
    "eval-type",
    "raw-length",
    "qfr-type",
    "src-length",
    "step-type",
    "role-length",
):
    require(token in fixture, f"fixture lost sentinel/tamper: {token}")

checker = LOG_CHECKER.read_text(encoding="ascii")
for token in (
    "round_f64_bits_to_f32_bits",
    "ordered_key",
    "f32_to_f64_bits",
    "fixture_checks",
    "arm KEYFLX layouts differ",
    "canonical grammar or summary differs",
    "zip(bridge_rows, production_rows, strict=True)",
):
    require(token in checker, f"log checker lost independent gate: {token}")
for forbidden in (
    "subprocess",
    "socket",
    "requests",
    "numpy",
    "isclose",
    "allclose",
    "check_raw_moc_ulp_bridge_xsm",
):
    require(forbidden not in checker, f"log checker contains {forbidden}")

test = TEST.read_text(encoding="ascii")
for token in (
    "cmp \"$WORK/native_a.log\" \"$WORK/native_b.log\"",
    "cmp \"$WORK/native_a.log\" \"$WORK/current.log\"",
    "RAW64 one-bit tamper was invisible",
    "OFF one-bit tamper was invisible",
    "--fixture",
    "raw-negative",
    "eval-zero",
    "off-zero",
    "reader object references solver symbols",
    "selftest_a.err",
    "log_check_a.err",
    "cross-arm KEYFLX mismatch passed",
):
    require(token in test, f"checker test lost gate: {token}")

runner = RUNNER.read_text(encoding="ascii")
for token in (
    'INPUT="$ROOT/validation/artifacts/raw-moc-capture"',
    'ARTIFACT="$ROOT/validation/artifacts/raw-moc-ulp-bridge"',
    "seen_inodes=",
    "inputs_before.sha256",
    "inputs_after.log",
    "parent_native.log",
    "parent_stationary.log",
    "common/restart_system.xsm",
    "native/frozen.xsm",
    "stationary/frozen.xsm",
    "native/check_a.log",
    "stationary/check_a.log",
    "cmp \"$WORK/native_a.log\" \"$WORK/native_b.log\"",
    "cmp \"$WORK/stationary_a.log\" \"$WORK/stationary_b.log\"",
    "checker_a.log",
    "checker_b.log",
    "artifact_manifest.sha256",
    "IMPLEMENTATION_FILES=",
    "git -C \"$ROOT\" ls-files --error-unmatch",
    "git -C \"$ROOT\" show \"HEAD:$relative\"",
    "implementation/validation/iterative/check_raw_moc_ulp_bridge_xsm.f90",
    "verify_package",
    'verify_package "$WORK/payload"',
    'verify_package "$PUBLISH"',
    'verify_package "$ARTIFACT"',
    "artifact contains a symlink",
    'LOCK="$ARTIFACT.lock"',
    "artifact publication lock is busy",
    'mv "$PUBLISH" "$ARTIFACT"',
    "dependency_hashes.sha256",
    "toolchain.txt",
    "reader binary links solver symbols",
    "-ffp-contract=off",
    "-fno-fast-math",
):
    require(token in runner, f"audit runner lost gate: {token}")
require(
    "Dragon" not in runner and "DRAGON_BIN" not in runner,
    "audit runner contains a Dragon execution path",
)
require(
    runner.count('python3 "$PARENT_CHECKER"') == 2,
    "parent artifact checker is not run before and after extraction",
)

print("RAW-MOC-ULP CONTRACT PASS")

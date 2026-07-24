#!/usr/bin/env python3
"""Fail-closed public and local-artifact check for raw-MOC capture."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[2]
ITER = ROOT / "validation" / "iterative"
ARTIFACT = ROOT / "validation" / "artifacts" / "raw-moc-capture"
STATUS = ITER / "raw_moc_capture_status.txt"
XSM = ITER / "raw_moc_capture_xsm_result.txt"
RESULT = ITER / "raw_moc_capture_result.md"
RECEIPT = ITER / "raw_moc_capture_result_receipt.sha256"

RUN_COMMIT = "a011fd902398b47e06faa2b23d0682c9d01eef7f"
ARTIFACT_MANIFEST_HASH = (
    "1c2c6bbae0a81a3978b09bc158ac0ca7a408c7d6495e734fea2f8e44f48b48a4"
)

EXPECTED_STATUS = (
    "RAW-MOC-CAPTURE RESULT CAPTURE-VALID",
    f"RAW-MOC-CAPTURE RUN-COMMIT {RUN_COMMIT}",
    "RAW-MOC-CAPTURE PROCESSES PREPARE=1 PROBES=4 NORMAL=5",
    "RAW-MOC-CAPTURE PRIOR-ATTEMPT CHECKER-CONTRACT-INVALID "
    "NO-CLASSIFICATION",
    "RAW-MOC-CAPTURE LOGS OFF-ON-SCIENCE IDENTICAL-EXCEPT-CPU",
    "RAW-MOC-CAPTURE XSM FROZEN-OFF BYTE-IDENTICAL",
    "RAW-MOC-CAPTURE XSM ON-NON-AUDIT OFF BYTE-IDENTICAL",
    "RAW-MOC-CAPTURE SOURCE MCGFCS-REPLAY BIT-EXACT",
    "RAW-MOC-CAPTURE ACCEPTANCE-THRESHOLD NONE",
    "RAW-MOC-CAPTURE TRANSPORT-ERROR-BOUND NOT-ESTABLISHED",
    "RAW-MOC-CAPTURE ARM-RANKING NOT-AUTHORIZED",
    "RAW-MOC-CAPTURE OUTER-CONVERGENCE NOT-EVALUATED",
    "RAW-MOC-CAPTURE STAGE4 NOT-AUTHORIZED",
    "RAW-MOC-CAPTURE COMPLETE",
)

EXPECTED_SUMMARY = {
    "NATIVE": {
        "norm": (
            "5.74612642427124923E-007",
            "3EA347E2904A264E",
        ),
        "maximum": (
            "2.13063570538973194E-006",
            "3EC1DF815DC6D801",
        ),
        "tie": "RAW-MOC-XSM MAX-TIE 100 2 2 BE4EDDDF63E80000",
        "check_hash": (
            "3309bd89d8094915ad458e4a4fa612a9e3d51fff26bc9a587d800b74c7b99569"
        ),
        "pre_hash": (
            "663a8257b1ecafa2dde9c36d7cff8ccd8201a08fe2b117cdccad46c305e5bea9"
        ),
        "frozen_hash": (
            "df24abbfe1f15e91948e5b930229e09aa13410e1b8985a61a74c8d28db08e208"
        ),
        "on_hash": (
            "e6b737bb0a648c5dab5ffe3e8a60ba862dd40d78e76bd2c87ad095d992ac6b9d"
        ),
    },
    "STATIONARY": {
        "norm": (
            "5.78155360184452634E-007",
            "3EA3665115160BED",
        ),
        "maximum": (
            "2.19029230865145395E-006",
            "3EC25F9DEE4899E9",
        ),
        "tie": "RAW-MOC-XSM MAX-TIE 100 2 2 BE4FBB1F05500000",
        "check_hash": (
            "8a57826442fb9be160fc3c2ce0b9e08e7dbe12ec71992fd14c9f5351022ed930"
        ),
        "pre_hash": (
            "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e"
        ),
        "frozen_hash": (
            "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789"
        ),
        "on_hash": (
            "de27778fb23f035aafab0e6ca877faf0f64a0662d255fa485b8174fea81f87ae"
        ),
    },
}


def fail(message: str) -> None:
    raise SystemExit(f"RAW-MOC-CAPTURE RESULT FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path, description: str) -> None:
    if not path.is_file() or path.is_symlink():
        fail(f"invalid regular file: {description}")


def read_canonical(path: Path, description: str) -> str:
    require_regular(path, description)
    raw = path.read_bytes()
    if not raw or b"\0" in raw or b"\r" in raw or not raw.endswith(b"\n"):
        fail(f"noncanonical text: {description}")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"invalid UTF-8 in {description}: {exc}")


def check_printed_float(decimal: str, bits: str, description: str) -> None:
    actual = struct.pack(">d", float(decimal)).hex().upper()
    if actual != bits:
        fail(f"decimal/binary64 mismatch: {description}")


def expected_xsm_lines() -> tuple[str, ...]:
    lines: list[str] = []
    for arm in ("NATIVE", "STATIONARY"):
        summary = EXPECTED_SUMMARY[arm]
        lines.extend(
            (
                f"RAW-MOC-XSM ARM {arm}",
                "RAW-MOC-XSM DIMS 370 8 14",
                "RAW-MOC-XSM PHASE POST-STIS-PRE-ACA-SCR",
                "RAW-MOC-XSM SCALAR-RELATIVE-TWO-NORM  "
                f"{summary['norm'][0]} {summary['norm'][1]}",
                "RAW-MOC-XSM SCALAR-INPUT-NORMALIZED-MAX  "
                f"{summary['maximum'][0]} {summary['maximum'][1]}",
                str(summary["tie"]),
                "RAW-MOC-XSM LEDGER-COUNT 5180",
                "RAW-MOC-XSM CURRENT-COUNT 2220",
                "RAW-MOC-XSM CAPTURE-VALID",
                "RAW-MOC-XSM OUTER-CONVERGENCE NOT-EVALUATED",
                "RAW-MOC-XSM STAGE4 NOT-AUTHORIZED",
                "RAW-MOC-XSM COMPLETE",
            )
        )
    return tuple(lines)


def read_receipt() -> dict[str, str]:
    text = read_canonical(RECEIPT, RECEIPT.name)
    rows = [line.split() for line in text.splitlines() if line.strip()]
    expected_paths = {
        "validation/iterative/raw_moc_capture_status.txt",
        "validation/iterative/raw_moc_capture_xsm_result.txt",
        "validation/iterative/raw_moc_capture_result.md",
        "validation/iterative/check_raw_moc_capture_result.py",
        "validation/iterative/raw_moc_capture_run_protocol.json",
        "validation/iterative/raw_moc_capture_run_implementation.sha256",
        "validation/artifacts/raw-moc-capture/artifact_manifest.sha256",
        "validation/artifacts/raw-moc-capture/artifact_replay.log",
        "validation/artifacts/raw-moc-capture/run_log_check.txt",
        "validation/artifacts/raw-moc-capture/run_commit.txt",
        "validation/artifacts/raw-moc-capture/native/check_a.log",
        "validation/artifacts/raw-moc-capture/native/check_b.log",
        "validation/artifacts/raw-moc-capture/stationary/check_a.log",
        "validation/artifacts/raw-moc-capture/stationary/check_b.log",
    }
    if (
        len(rows) != len(expected_paths)
        or any(len(row) != 2 for row in rows)
        or {row[1] for row in rows} != expected_paths
        or any(not re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in rows)
    ):
        fail("result receipt census differs")
    return {relative: digest for digest, relative in rows}


def check_public(receipt: dict[str, str]) -> None:
    for relative, expected in receipt.items():
        if relative.startswith("validation/artifacts/"):
            continue
        path = ROOT / relative
        require_regular(path, relative)
        if expected != sha256(path):
            fail(f"public receipt differs for {relative}")

    status_lines = tuple(read_canonical(STATUS, STATUS.name).splitlines())
    if status_lines != EXPECTED_STATUS:
        fail("public status differs")

    xsm_lines = tuple(read_canonical(XSM, XSM.name).splitlines())
    if xsm_lines != expected_xsm_lines():
        fail("public XSM summary differs")
    for arm, summary in EXPECTED_SUMMARY.items():
        check_printed_float(*summary["norm"], f"{arm} norm")
        check_printed_float(*summary["maximum"], f"{arm} maximum")

    result = read_canonical(RESULT, RESULT.name)
    for token in (
        RUN_COMMIT,
        "`CAPTURE-VALID`",
        "not an independently assembled",
        "No model term, empirical coefficient, relaxation, clipping",
        "TRANSPORT-ERROR-BOUND NOT-ESTABLISHED",
        "ARM-RANKING NOT-AUTHORIZED",
        "OUTER-CONVERGENCE NOT-EVALUATED",
        "STAGE4 NOT-AUTHORIZED",
        "checker rejected legal negative",
        "81 regular files",
        "binary artifact is ignored",
        "GitHub retains",
    ):
        if token not in result:
            fail(f"result interpretation lacks: {token}")


def check_manifest(receipt: dict[str, str]) -> None:
    manifest = ARTIFACT / "artifact_manifest.sha256"
    require_regular(manifest, "artifact manifest")
    if (
        sha256(manifest) != ARTIFACT_MANIFEST_HASH
        or receipt[str(manifest.relative_to(ROOT))] != sha256(manifest)
    ):
        fail("artifact manifest identity differs")
    rows = [
        line.split()
        for line in read_canonical(manifest, manifest.name).splitlines()
        if line.strip()
    ]
    if (
        len(rows) != 79
        or any(len(row) != 2 for row in rows)
        or len({row[1] for row in rows}) != len(rows)
        or any(not re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in rows)
        or any(not row[1].startswith("./") for row in rows)
        or any(".." in Path(row[1]).parts for row in rows)
    ):
        fail("artifact manifest census differs")
    for expected, relative in rows:
        path = ARTIFACT / relative[2:]
        require_regular(path, relative)
        if sha256(path) != expected:
            fail(f"artifact hash differs: {relative}")

    all_paths = list(ARTIFACT.rglob("*"))
    if any(path.is_symlink() for path in all_paths):
        fail("artifact contains a symlink")
    if len([path for path in all_paths if path.is_file()]) != 81:
        fail("artifact regular-file census differs")

    replay = ARTIFACT / "artifact_replay.log"
    replay_lines = read_canonical(replay, replay.name).splitlines()
    expected_replay = [f"{relative}: OK" for _, relative in rows]
    if replay_lines != expected_replay:
        fail("artifact replay log differs")


def check_artifact(receipt: dict[str, str]) -> None:
    if not ARTIFACT.is_dir() or ARTIFACT.is_symlink():
        fail("local artifact is unavailable")
    for relative, expected in receipt.items():
        if not relative.startswith("validation/artifacts/"):
            continue
        path = ROOT / relative
        require_regular(path, relative)
        if sha256(path) != expected:
            fail(f"result receipt differs for {relative}")

    check_manifest(receipt)
    if read_canonical(ARTIFACT / "run_commit.txt", "run commit").strip() != RUN_COMMIT:
        fail("run commit differs")
    if (
        read_canonical(ARTIFACT / "run_log_check.txt", "run log check")
        != "RAW-MOC-CAPTURE RUN-LOGS PASS\n"
    ):
        fail("run log classification differs")

    protocol = json.loads(
        read_canonical(
            ARTIFACT / "raw_moc_capture_run_protocol.json",
            "artifact protocol",
        )
    )
    if (
        protocol["status"] != "FROZEN-BEFORE-CORRECTED-REPLAY"
        or protocol["classification"]["valid"] != "CAPTURE-VALID"
        or protocol["classification"]["acceptance_threshold"] is not None
        or protocol["classification"]["outer_convergence_evaluated"]
        or protocol["classification"]["stage4_authorization"]
    ):
        fail("artifact protocol classification differs")

    for arm in ("native", "stationary"):
        upper = arm.upper()
        summary = EXPECTED_SUMMARY[upper]
        check_a = ARTIFACT / arm / "check_a.log"
        check_b = ARTIFACT / arm / "check_b.log"
        if check_a.read_bytes() != check_b.read_bytes():
            fail(f"{upper} checker replays differ")
        if sha256(check_a) != summary["check_hash"]:
            fail(f"{upper} checker output hash differs")
        lines = read_canonical(check_a, f"{arm} checker").splitlines()
        if len(lines) != 7410:
            fail(f"{upper} checker line census differs")
        if sum(line.startswith("RAW-MOC-XSM LEDGER ") for line in lines) != 5180:
            fail(f"{upper} ledger census differs")
        if sum(line.startswith("RAW-MOC-XSM CURRENT ") for line in lines) != 2220:
            fail(f"{upper} current census differs")
        first = 0 if upper == "NATIVE" else 12
        required = set(expected_xsm_lines()[first : first + 12])
        required.discard("RAW-MOC-XSM LEDGER-COUNT 5180")
        required.discard("RAW-MOC-XSM CURRENT-COUNT 2220")
        if not required.issubset(lines):
            fail(f"{upper} checker summary differs")

        pre = ARTIFACT / arm / "pre.xsm"
        frozen = ARTIFACT / arm / "frozen.xsm"
        off = ARTIFACT / arm / "off.xsm"
        on = ARTIFACT / arm / "on.xsm"
        if sha256(pre) != summary["pre_hash"]:
            fail(f"{upper} PRE identity differs")
        if (
            frozen.read_bytes() != off.read_bytes()
            or sha256(frozen) != summary["frozen_hash"]
        ):
            fail(f"{upper} FROZEN/OFF identity differs")
        if sha256(on) != summary["on_hash"] or on.read_bytes() == off.read_bytes():
            fail(f"{upper} ON identity differs")
        paths = (
            ARTIFACT / arm / "track.xsm",
            ARTIFACT / arm / "system.xsm",
            pre,
            frozen,
            off,
            on,
        )
        if len({path.stat().st_ino for path in paths}) != len(paths):
            fail(f"{upper} evidence files alias")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-only", action="store_true")
    args = parser.parse_args()
    receipt = read_receipt()
    check_public(receipt)
    if not args.public_only:
        check_artifact(receipt)
    scope = "PUBLIC" if args.public_only else "PUBLIC+ARTIFACT"
    print(
        f"RAW-MOC-CAPTURE RESULT PASS: {scope}; CAPTURE-VALID; "
        "no transport-error, arm-ranking, outer-convergence, or Stage-4 claim."
    )


if __name__ == "__main__":
    main()

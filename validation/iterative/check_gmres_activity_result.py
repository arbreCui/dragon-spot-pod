#!/usr/bin/env python3
"""Fail-closed verifier for the published passive GMRES activity result."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import stat
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
ARTIFACT = ROOT / "validation" / "artifacts" / "gmres-activity-census"
RECEIPT = ITERATIVE / "gmres_activity_result_receipt.sha256"

RUN_COMMIT = "83e49163d36c4126fe6531500315c67a0162a78b"
CLASSIFICATION = "VALID-GMRES-UPDATE-INACTIVE"
METHOD_PROTOCOL_SHA256 = (
    "8f1e1165e7d30b0e5b693e65a842a10581ec9ecb83b3d6bc3bc52ee8eb130bb9"
)
METHOD_MANIFEST_SHA256 = (
    "22ff5770263a5f100382f4fd9f9d9e91babe51e51f6b32bb51f394ad3c67178b"
)
RUN_PROTOCOL_SHA256 = (
    "feee3d0a4989718137145d8136c246afc4ffebbb9dea9a0d105181be4a7be5d1"
)
RUN_MANIFEST_SHA256 = (
    "8bca8ba22d955cf80c728929afc5d365ce641e9189b2c786023ecf7f996105e6"
)
ARTIFACT_CHECKER_SHA256 = (
    "fe7630765f4ffec5d26bf7ed27f792dcea8c3a18c6f29427752077cde59c3c48"
)
RUNNER_SHA256 = (
    "cb2dde7b3b857b475f4b84a1a42fc0476314b88ad2301e215503d5ee3a3874bb"
)
HISTORICAL_ULP_RECEIPT_SHA256 = (
    "20dc353133c6251021fb87f0196061fb0b1be969d8e73890b7a9b1b073e60935"
)
ARTIFACT_MANIFEST_SHA256 = (
    "aeb7d0b4952cea79ed4288ba8e6e27e82d69ae772054f9a0d9a64d57b5e49e22"
)

EXPECTED_RESULT = """\
GMRES-ACTIVITY RESULT 1
PROCESSES OFF=1 ON=2
CORRECTION-BLOCKS 0
GROUP-BLOCKS 0
K-HISTOGRAM 0 0
K-HISTOGRAM 1 0
K-HISTOGRAM 2 0
K-HISTOGRAM 3 0
K-HISTOGRAM 4 0
K-HISTOGRAM 5 0
K-HISTOGRAM 6 0
K-HISTOGRAM 7 0
K-HISTOGRAM 8 0
K-HISTOGRAM 9 0
K-HISTOGRAM 10 0
NONZERO-K-GROUP-BLOCKS 0
SUM-K 0
MAX-K 0
THRESHOLD NONE
CLASSIFICATION VALID-GMRES-UPDATE-INACTIVE
COMPLETE
""".encode("ascii")

CRITICAL_HASHES = {
    "validation/iterative/gmres_activity_protocol.json":
        METHOD_PROTOCOL_SHA256,
    "validation/iterative/gmres_activity_implementation.sha256":
        METHOD_MANIFEST_SHA256,
    "validation/iterative/gmres_activity_run_protocol.json":
        RUN_PROTOCOL_SHA256,
    "validation/iterative/gmres_activity_run_implementation.sha256":
        RUN_MANIFEST_SHA256,
    "validation/iterative/check_gmres_activity_artifact.py":
        ARTIFACT_CHECKER_SHA256,
    "validation/iterative/run_gmres_activity_production.sh":
        RUNNER_SHA256,
    "validation/iterative/raw_moc_ulp_bridge_result_receipt.sha256":
        HISTORICAL_ULP_RECEIPT_SHA256,
}

TRACKED_RECEIPT_PATHS = (
    "validation/iterative/gmres_activity_result.txt",
    "validation/iterative/gmres_activity_result.md",
    "validation/iterative/check_gmres_activity_result.py",
    "validation/iterative/gmres_activity_protocol.json",
    "validation/iterative/gmres_activity_implementation.sha256",
    "validation/iterative/gmres_activity_run_protocol.json",
    "validation/iterative/gmres_activity_run_implementation.sha256",
    "validation/iterative/check_gmres_activity_artifact.py",
    "validation/iterative/run_gmres_activity_production.sh",
    "validation/iterative/check_raw_moc_ulp_bridge_result_history.py",
    "validation/iterative/raw_moc_ulp_bridge_result_receipt.sha256",
    "README.md",
    "SPOT_doc/validation_plan.md",
    "validation/iterative/README.md",
    "validation/run_fast.sh",
)

ARTIFACT_RECEIPT_PATHS = (
    "validation/artifacts/gmres-activity-census/artifact_manifest.sha256",
    "validation/artifacts/gmres-activity-census/result.txt",
    "validation/artifacts/gmres-activity-census/run_receipt.tsv",
    "validation/artifacts/gmres-activity-census/run_commit.txt",
    "validation/artifacts/gmres-activity-census/on_a/ledger.txt",
    "validation/artifacts/gmres-activity-census/on_b/ledger.txt",
    "validation/artifacts/gmres-activity-census/log_identity.txt",
    "validation/artifacts/gmres-activity-census/artifact_check_a.log",
    "validation/artifacts/gmres-activity-census/artifact_check_b.log",
)

EXPECTED_ARTIFACT_HASHES = {
    ARTIFACT_RECEIPT_PATHS[0]: ARTIFACT_MANIFEST_SHA256,
    ARTIFACT_RECEIPT_PATHS[1]:
        "c542b1ff1dd1cfbe1689b2647c4db42d81b2cbccbb519da474dd4afc100c6fff",
    ARTIFACT_RECEIPT_PATHS[2]:
        "865d0728119f023ba0511da43eda57a3ca46083adea40cb2486a904910babb0c",
    ARTIFACT_RECEIPT_PATHS[3]:
        "cd5dbb2ac8af29832040b776f2da0f93d3819e4a879d1e4c890fc312ab59e248",
    ARTIFACT_RECEIPT_PATHS[4]:
        "0c8a21604b9ef3f0f604da299d53ecc679445d30b25409f7f061ead766f63ba4",
    ARTIFACT_RECEIPT_PATHS[5]:
        "0c8a21604b9ef3f0f604da299d53ecc679445d30b25409f7f061ead766f63ba4",
    ARTIFACT_RECEIPT_PATHS[6]:
        "ca63662bf027869f48cbfd9f64b132d11d792cc4e207a78e778c6bfdf39695b8",
    ARTIFACT_RECEIPT_PATHS[7]:
        "0010eaab8dc9538a9a91dbfe5b1127f96cc0a21a48584261cc3ef0abff35f159",
    ARTIFACT_RECEIPT_PATHS[8]:
        "0010eaab8dc9538a9a91dbfe5b1127f96cc0a21a48584261cc3ef0abff35f159",
}

SHA_ROW = re.compile(r"([0-9a-f]{64})  ([^\t]+)")


class ResultError(RuntimeError):
    """A public-result contract violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResultError(message)


def regular(path: Path) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid file: {path}")


def sha256(path: Path) -> str:
    regular(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(path: Path) -> bytes:
    regular(path)
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"missing final newline: {path}")
    require(b"\r" not in raw and b"\0" not in raw, f"noncanonical text: {path}")
    return raw


def parse_receipt() -> list[tuple[str, str]]:
    try:
        lines = canonical_bytes(RECEIPT).decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise ResultError("receipt is not ASCII") from exc
    rows: list[tuple[str, str]] = []
    for line in lines:
        match = SHA_ROW.fullmatch(line)
        require(match is not None, "malformed receipt row")
        digest, name = match.groups()
        candidate = Path(name)
        require(
            not candidate.is_absolute()
            and ".." not in candidate.parts
            and candidate.as_posix() == name,
            f"unsafe receipt path: {name}",
        )
        rows.append((digest, name))
    require(len({name for _, name in rows}) == len(rows), "duplicate receipt path")
    expected = TRACKED_RECEIPT_PATHS + ARTIFACT_RECEIPT_PATHS
    require(tuple(name for _, name in rows) == expected, "receipt census/order differs")
    return rows


def verify_public(public_only: bool) -> None:
    for name, expected in CRITICAL_HASHES.items():
        require(sha256(ROOT / name) == expected, f"critical hash differs: {name}")

    result = ITERATIVE / "gmres_activity_result.txt"
    require(canonical_bytes(result) == EXPECTED_RESULT, "compact result differs")

    try:
        narrative = canonical_bytes(
            ITERATIVE / "gmres_activity_result.md"
        ).decode("ascii")
    except UnicodeDecodeError as exc:
        raise ResultError("result narrative is not ASCII") from exc
    for token in (
        RUN_COMMIT,
        CLASSIFICATION,
        ARTIFACT_MANIFEST_SHA256,
        "PRIMARY role calls / active groups | 1 / 370",
        "correction blocks / group-block rows | 0 / 0",
        "Stage 4 remains invalid and Stage 5 remains unauthorized",
    ):
        require(token in narrative, f"result narrative token missing: {token}")

    for expected, name in parse_receipt():
        if name in EXPECTED_ARTIFACT_HASHES:
            require(
                expected == EXPECTED_ARTIFACT_HASHES[name],
                f"artifact receipt hash differs: {name}",
            )
            if not public_only:
                require(sha256(ROOT / name) == expected, f"artifact file differs: {name}")
        else:
            require(sha256(ROOT / name) == expected, f"tracked receipt hash differs: {name}")


def verify_local_artifact() -> None:
    require(ARTIFACT.is_dir() and not ARTIFACT.is_symlink(), "invalid artifact root")
    mode = ARTIFACT.lstat().st_mode
    require(stat.S_ISDIR(mode), "artifact root is not a directory")
    require(
        sha256(ARTIFACT / "artifact_manifest.sha256") == ARTIFACT_MANIFEST_SHA256,
        "artifact manifest identity differs",
    )
    require(
        canonical_bytes(ARTIFACT / "result.txt") == EXPECTED_RESULT,
        "artifact and tracked result differ",
    )
    require(
        canonical_bytes(ARTIFACT / "run_commit.txt")
        == f"{RUN_COMMIT}\n".encode("ascii"),
        "artifact run commit differs",
    )
    checker = ROOT / "validation" / "iterative" / "check_gmres_activity_artifact.py"
    completed = subprocess.run(
        [sys.executable, str(checker), str(ARTIFACT)],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(completed.returncode == 0, "independent artifact checker failed")
    require(not completed.stderr, "independent artifact checker wrote stderr")
    require(
        completed.stdout == f"{CLASSIFICATION}\n".encode("ascii"),
        "independent artifact classification differs",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="verify tracked evidence without requiring the ignored local artifact",
    )
    arguments = parser.parse_args()
    verify_public(arguments.public_only)
    if not arguments.public_only:
        verify_local_artifact()
    print("GMRES-ACTIVITY RESULT PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ResultError) as exc:
        print(f"GMRES-ACTIVITY RESULT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

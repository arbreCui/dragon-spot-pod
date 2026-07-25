#!/usr/bin/env python3
"""Replay the immutable ULP result while preserving its historical receipt."""

from __future__ import annotations

import argparse

import check_raw_moc_ulp_bridge_result as frozen


HISTORICAL_RECEIPT_SHA256 = (
    "20dc353133c6251021fb87f0196061fb0b1be969d8e73890b7a9b1b073e60935"
)
HISTORICAL_DOCUMENT_HASHES = {
    "README.md":
        "dce5aeff0e8f0151c27c05cfcc6f1029988b99308bb35559f93243a8f41ef9e1",
    "SPOT_doc/validation_plan.md":
        "72e43af1283119d7c2b1832699fdd3f29cf8b77c37d47acd40f5f150a02195e2",
    "validation/iterative/README.md":
        "929a9d5cbce6d33e91c34e621c1e57022fe9bc0cb80794506bd259712d6d35e3",
    "validation/run_fast.sh":
        "b3d227688f1734bbf366f3dfed711b8d40e4f3e8232727c3295539e709eebc21",
}


def verify_historical_receipt(public_only: bool) -> None:
    frozen.require(
        frozen.sha256(frozen.RECEIPT) == HISTORICAL_RECEIPT_SHA256,
        "historical result receipt bytes differ",
    )
    rows = frozen.parse_sha_lines(frozen.RECEIPT)
    frozen.require(
        tuple(relative for _, relative in rows) == frozen.EXPECTED_RECEIPT_PATHS,
        "historical result receipt path order/set differs",
    )
    receipt = {relative: digest for digest, relative in rows}

    for relative, expected in HISTORICAL_DOCUMENT_HASHES.items():
        frozen.require(
            receipt[relative] == expected,
            f"historical document identity differs: {relative}",
        )

    for relative in frozen.TRACKED_RECEIPT_PATHS:
        if relative in HISTORICAL_DOCUMENT_HASHES:
            continue
        frozen.require(
            frozen.sha256(frozen.ROOT / relative) == receipt[relative],
            f"historical tracked hash differs: {relative}",
        )

    for relative, expected in frozen.EXPECTED_PUBLIC_HASHES.items():
        frozen.require(
            receipt[relative] == expected,
            f"historical public identity differs: {relative}",
        )
    for relative, expected in frozen.EXPECTED_RECEIPT_ARTIFACT_HASHES.items():
        frozen.require(
            receipt[relative] == expected,
            f"historical artifact identity differs: {relative}",
        )
        if not public_only:
            frozen.require(
                frozen.sha256(frozen.ROOT / relative) == expected,
                f"historical artifact hash differs: {relative}",
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Replay the raw-MOC ULP result without rewriting the receipt "
            "that later frozen protocols use as an input."
        )
    )
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="verify tracked science while treating ignored artifact rows as identities",
    )
    arguments = parser.parse_args()

    frozen.verify_public_hashes()
    frozen.verify_protocol()
    frozen.verify_implementation()
    result = frozen.verify_status_and_result()
    frozen.verify_markdown()
    verify_historical_receipt(arguments.public_only)

    if arguments.public_only:
        print(
            "RAW-MOC-ULP HISTORY PASS: PUBLIC; "
            "HISTORICAL-RECEIPT=FROZEN; CURRENT-DOCS=VERSIONED-SEPARATELY"
        )
        return

    frozen.require(
        frozen.ARTIFACT.exists(),
        "artifact is absent; use --public-only for tracked-only verification",
    )
    frozen.verify_artifact_inventory()
    frozen.verify_artifact_manifest()
    frozen.verify_artifact_logs(result)
    print(
        "RAW-MOC-ULP HISTORY PASS: PUBLIC+ARTIFACT; "
        "HISTORICAL-RECEIPT=FROZEN; CURRENT-DOCS=VERSIONED-SEPARATELY"
    )


if __name__ == "__main__":
    main()

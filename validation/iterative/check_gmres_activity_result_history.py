#!/usr/bin/env python3
"""Replay the GMRES result while preserving its historical receipt."""

from __future__ import annotations

import argparse
import sys

import check_gmres_activity_result as frozen


HISTORICAL_RECEIPT_SHA256 = (
    "8b74db6302dd9fc511c7f241b10c5d01f503295a8788eea17e98c90bd4f96ded"
)
HISTORICAL_DOCUMENT_HASHES = {
    "README.md": (
        "a50bc049dd4f1294eaa12f82af731d0ddfb60c8f4fe41baf749ae12376470101"
    ),
    "SPOT_doc/validation_plan.md": (
        "daee553b6678798a384ff01fbbe272947dd6d5be97ec948be7f67d890ba2b2a0"
    ),
    "validation/iterative/README.md": (
        "67d38fa0c066448799cecd52e33f55d481d43d4504709504a9e474ebb43e9825"
    ),
    "validation/run_fast.sh": (
        "71a47fad295bd2d92ed7bc788421b61dfb91b5451e7eb2568e4d77352d621d17"
    ),
}


def verify_historical_public(public_only: bool) -> None:
    frozen.require(
        frozen.sha256(frozen.RECEIPT) == HISTORICAL_RECEIPT_SHA256,
        "historical result receipt bytes differ",
    )
    rows = frozen.parse_receipt()
    receipt = {name: digest for digest, name in rows}

    for name, expected in HISTORICAL_DOCUMENT_HASHES.items():
        frozen.require(
            receipt[name] == expected,
            f"historical document identity differs: {name}",
        )

    for name, expected in frozen.CRITICAL_HASHES.items():
        frozen.require(
            frozen.sha256(frozen.ROOT / name) == expected,
            f"critical hash differs: {name}",
        )

    result = frozen.ITERATIVE / "gmres_activity_result.txt"
    frozen.require(
        frozen.canonical_bytes(result) == frozen.EXPECTED_RESULT,
        "compact result differs",
    )
    try:
        narrative = frozen.canonical_bytes(
            frozen.ITERATIVE / "gmres_activity_result.md"
        ).decode("ascii")
    except UnicodeDecodeError as exc:
        raise frozen.ResultError("result narrative is not ASCII") from exc
    for token in (
        frozen.RUN_COMMIT,
        frozen.CLASSIFICATION,
        frozen.ARTIFACT_MANIFEST_SHA256,
        "PRIMARY role calls / active groups | 1 / 370",
        "correction blocks / group-block rows | 0 / 0",
        "Stage 4 remains invalid and Stage 5 remains unauthorized",
    ):
        frozen.require(token in narrative, f"result narrative token missing: {token}")

    for expected, name in rows:
        if name in HISTORICAL_DOCUMENT_HASHES:
            continue
        if name in frozen.EXPECTED_ARTIFACT_HASHES:
            frozen.require(
                expected == frozen.EXPECTED_ARTIFACT_HASHES[name],
                f"artifact receipt hash differs: {name}",
            )
            if not public_only:
                frozen.require(
                    frozen.sha256(frozen.ROOT / name) == expected,
                    f"artifact file differs: {name}",
                )
        else:
            frozen.require(
                frozen.sha256(frozen.ROOT / name) == expected,
                f"historical tracked hash differs: {name}",
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="verify tracked science while treating artifact rows as identities",
    )
    arguments = parser.parse_args()

    verify_historical_public(arguments.public_only)
    if not arguments.public_only:
        frozen.verify_local_artifact()
    scope = "PUBLIC" if arguments.public_only else "PUBLIC+ARTIFACT"
    print(
        "GMRES-ACTIVITY HISTORY PASS: "
        f"{scope}; HISTORICAL-RECEIPT=FROZEN; "
        "CURRENT-DOCS=VERSIONED-SEPARATELY"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, frozen.ResultError) as exc:
        print(f"GMRES-ACTIVITY HISTORY FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

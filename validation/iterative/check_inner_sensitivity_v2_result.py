#!/usr/bin/env python3
"""Classify the frozen Stage-4 v2 map pair from exact stored bits.

The Ganlib-only checker emits three binary64 vectors.  This program applies
the pre-registered component rule without a tolerance, aggregation, fit, or
floating-point text comparison.  Replay qualification additionally requires
the capture manifest to be present in a named Git commit and both capture and
replay artifacts to match that committed manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_PROTOCOL_SHA256 = (
    "8a870a85ffe7fd4eb53d9494bcf28acea2025f8f3d022579312cd34a22a1d88c"
)
PROTOCOL_COMPONENTS = ("R_rho", "R_L", "D_L", "R_a")
CHECKER_COMPONENTS = ("RRHO", "RLEAK", "DLEAK", "RA")
SCIENTIFIC_FILES = (
    "basis_reference.xsm",
    "state0_axial.xsm",
    "state1_system.xsm",
    "state1_axial.xsm",
    "state1_snapshots.xsm",
)
CAPTURE_EVIDENCE_FILES = (
    "authorization.json",
    "balance_xsm_check.log",
    "coarse_xsm_check.log",
    "dragon.log",
    "input_manifest.sha256",
    "pair_xsm_check.log",
    "process_check.log",
    "raw_log_check.log",
    "result.json",
    "scientific_manifest.sha256",
)
FROZEN_INPUT_HASHES = {
    "basis_reference.xsm": (
        "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504"
    ),
    "state0_axial.xsm": (
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb"
    ),
}
FROZEN_FINE_BITS = (
    0x3EB57E84A0A80000,
    0x3F49F62BC29A3832,
    0x3EB37D4000000000,
    0x3EAEF702EB99D736,
)
SHA_ROW = re.compile(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)")
BIT = r"0x[0-9A-F]{16}"


def fail(message: str) -> None:
    print(
        "INNER-SENSITIVITY-V2 RESULT FAIL: " + message,
        file=sys.stderr,
    )
    raise SystemExit(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, owner: str) -> None:
    require(
        path.is_file() and not path.is_symlink(),
        f"{owner} is not a regular non-symlink file",
    )


def strict_text(path: Path, owner: str) -> str:
    require_regular(path, owner)
    raw = path.read_bytes()
    require(
        raw and b"\0" not in raw and b"\r" not in raw,
        f"{owner} is empty or noncanonical",
    )
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError:
        fail(f"{owner} is not ASCII")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_protocol(path: Path) -> dict[str, Any]:
    text = strict_text(path, "protocol")
    require(
        sha256_bytes(text.encode("ascii")) == EXPECTED_PROTOCOL_SHA256,
        "protocol hash differs from the freeze",
    )
    try:
        protocol = json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        fail(f"invalid protocol JSON: {exc}")
    require(
        protocol["mathematical_definition"]["ordered_components"]
        == list(PROTOCOL_COMPONENTS),
        "protocol component order differs",
    )
    require(
        protocol["independent_checks"]["component_rule"]
        == {
            "positive_coarse_outer": (
                "RESOLVED iff D_in < D_out_2h"
            ),
            "zero_coarse_outer": (
                "RESOLVED iff D_in == 0 at stored precision"
            ),
            "otherwise": "UNRESOLVED",
        },
        "protocol component rule differs",
    )
    pair = protocol["tolerance_pair"]
    require(
        pair["coarse_2h"]["binary32_bits"] == "0x358637bd"
        and pair["fine_h"]["binary32_bits"] == "0x350637bd",
        "protocol tolerance bits differ",
    )
    coarse = struct.unpack(">f", bytes.fromhex("358637bd"))[0]
    fine = struct.unpack(">f", bytes.fromhex("350637bd"))[0]
    rounded_half = struct.unpack(">f", struct.pack(">f", 0.5 * coarse))[0]
    require(rounded_half == fine, "binary32 factor-two identity fails")
    return protocol


def parse_manifest_bytes(
    raw: bytes,
    owner: str,
) -> dict[str, str]:
    require(
        raw.endswith(b"\n")
        and b"\r" not in raw
        and b"\0" not in raw,
        f"{owner} is not canonical text",
    )
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError:
        fail(f"{owner} is not ASCII")
    require(
        len(lines) == len(SCIENTIFIC_FILES),
        f"{owner} must contain exactly five rows",
    )
    result: dict[str, str] = {}
    for line, expected_name in zip(lines, SCIENTIFIC_FILES, strict=True):
        match = SHA_ROW.fullmatch(line)
        require(match is not None, f"malformed {owner} row")
        digest, name = match.groups()
        require(name == expected_name, f"{owner} order differs")
        require(name not in result, f"duplicate {owner} path")
        result[name] = digest
    for name, digest in FROZEN_INPUT_HASHES.items():
        require(
            result[name] == digest,
            f"{owner} frozen input hash differs: {name}",
        )
    return result


def verify_manifest(
    path: Path,
    artifact_dir: Path,
    owner: str,
) -> tuple[bytes, dict[str, str]]:
    require_regular(path, f"{owner} manifest")
    raw = path.read_bytes()
    entries = parse_manifest_bytes(raw, owner)
    root = artifact_dir.resolve(strict=True)
    require(
        artifact_dir.is_dir() and not artifact_dir.is_symlink(),
        f"{owner} artifact directory is invalid",
    )
    for name in SCIENTIFIC_FILES:
        target = root / name
        require_regular(target, f"{owner} {name}")
        require(
            target.parent == root,
            f"{owner} scientific path escaped its directory",
        )
        require(
            sha256_file(target) == entries[name],
            f"{owner} file hash differs: {name}",
        )
    return raw, entries


def git_blob(commit: str, path: Path) -> bytes:
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "capture commit must be a full lowercase Git object id",
    )
    try:
        relative = path.resolve(strict=True).relative_to(ROOT)
    except (OSError, ValueError):
        fail("capture manifest must be a file inside the repository")
    require_regular(path, "capture manifest")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    require(
        ancestor.returncode == 0,
        "capture commit is not an ancestor of HEAD",
    )
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative.as_posix()}"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        result.returncode == 0,
        "capture manifest is unavailable from the named commit",
    )
    require(
        result.stdout == path.read_bytes(),
        "working capture manifest differs from the named commit",
    )
    return result.stdout


def verify_capture_receipt(
    receipt_path: Path,
    commit: str,
    artifact_dir: Path,
    scientific_manifest_raw: bytes,
) -> None:
    committed = git_blob(commit, receipt_path)
    try:
        text = committed.decode("ascii")
        receipt = json.loads(text, object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid capture receipt: {exc}")
    require(
        committed == (json.dumps(receipt, indent=2) + "\n").encode("ascii"),
        "capture receipt is not canonical JSON",
    )
    require(
        tuple(receipt)
        == (
            "schema",
            "protocol_sha256",
            "implementation_receipt_sha256",
            "scientific_manifest_sha256",
            "evidence_sha256",
            "classification",
            "dragon_processes",
        ),
        "capture receipt key order differs",
    )
    require(
        receipt["schema"] == "spot-inner-sensitivity-v2-capture-receipt-1"
        and receipt["protocol_sha256"] == EXPECTED_PROTOCOL_SHA256
        and receipt["classification"] == "PENDING-REPLAY"
        and receipt["dragon_processes"] == 1,
        "capture receipt state is not replayable",
    )
    implementation_receipt = (
        ROOT / "validation" / "iterative"
        / "inner_sensitivity_v2_implementation.sha256"
    )
    require_regular(implementation_receipt, "implementation receipt")
    require(
        receipt["implementation_receipt_sha256"]
        == sha256_file(implementation_receipt),
        "capture implementation receipt differs",
    )
    require(
        receipt["scientific_manifest_sha256"]
        == sha256_bytes(scientific_manifest_raw),
        "capture receipt does not bind the scientific manifest",
    )
    evidence = receipt["evidence_sha256"]
    require(
        isinstance(evidence, dict)
        and tuple(evidence) == CAPTURE_EVIDENCE_FILES,
        "capture receipt evidence census differs",
    )
    root = artifact_dir.resolve(strict=True)
    artifact_receipt = root / "capture_receipt.json"
    require_regular(artifact_receipt, "artifact capture receipt")
    require(
        artifact_receipt.read_bytes() == committed,
        "artifact receipt differs from committed capture receipt",
    )
    for name in CAPTURE_EVIDENCE_FILES:
        target = root / name
        require_regular(target, f"capture evidence {name}")
        require(
            sha256_file(target) == evidence[name],
            f"capture receipt evidence hash differs: {name}",
        )
    try:
        capture_result = json.loads(
            (root / "result.json").read_text(encoding="ascii"),
            object_pairs_hook=unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid captured result JSON: {exc}")
    require(
        capture_result.get("classification") == "PENDING-REPLAY"
        and capture_result.get("scientific_manifest_sha256")
        == sha256_bytes(scientific_manifest_raw),
        "captured result is not the receipt-bound pending result",
    )


def verify_inode_separation(capture_root: Path, replay_root: Path) -> None:
    require(
        capture_root.resolve(strict=True) != replay_root.resolve(strict=True),
        "capture and replay directories are identical",
    )
    for name in SCIENTIFIC_FILES:
        capture_file = capture_root / name
        replay_file = replay_root / name
        require_regular(capture_file, f"capture {name}")
        require_regular(replay_file, f"replay {name}")
        require(
            not os.path.samefile(capture_file, replay_file),
            f"capture and replay share an inode: {name}",
        )


def parse_bits_row(line: str, label: str) -> tuple[int, ...]:
    match = re.fullmatch(
        re.escape(label) + rf"(?:\s+({BIT}))" * 4,
        line,
    )
    require(match is not None, f"invalid {label} row")
    values = tuple(int(token[2:], 16) for token in match.groups())
    for value in values:
        require(value != 0x8000000000000000, f"{label} contains negative zero")
        require(value >> 63 == 0, f"{label} contains a negative value")
        decoded = struct.unpack(">d", value.to_bytes(8, "big"))[0]
        require(math.isfinite(decoded), f"{label} contains NaN or infinity")
    return values


def relation(left: int, right: int) -> str:
    if left < right:
        return "LESS"
    if left > right:
        return "GREATER"
    return "EQUAL"


def parse_pair_log(path: Path) -> tuple[tuple[int, ...], ...]:
    text = strict_text(path, "Ganlib pair-check log")
    require(text.endswith("\n"), "Ganlib pair-check log lacks final newline")
    lines = text.splitlines()
    require(len(lines) == 12, "Ganlib pair-check log must have 12 rows")
    require(
        lines[:4]
        == [
            "INNER-SENSITIVITY-V2 X0 CANONICAL BITWISE IDENTICAL",
            "INNER-SENSITIVITY-V2 TRIAL-SPACE BITWISE IDENTICAL",
            "INNER-SENSITIVITY-V2 RADIAL-INPUTS BITWISE IDENTICAL",
            "INNER-SENSITIVITY-V2 ORDER RRHO RLEAK DLEAK RA",
        ],
        "Ganlib pair-check prefix differs",
    )
    require(
        lines[11] == "INNER-SENSITIVITY-V2 COMPLETE",
        "Ganlib pair-check completion row differs",
    )
    dout_h = parse_bits_row(
        lines[4], "INNER-SENSITIVITY-V2 DOUT-H-BITS"
    )
    dout_2h = parse_bits_row(
        lines[5], "INNER-SENSITIVITY-V2 DOUT-2H-BITS"
    )
    din = parse_bits_row(lines[6], "INNER-SENSITIVITY-V2 DIN-BITS")
    require(
        dout_h == FROZEN_FINE_BITS,
        "fine D_out bits differ from the frozen Stage-3 map",
    )
    for index, component in enumerate(CHECKER_COMPONENTS):
        expected = (
            f"INNER-SENSITIVITY-V2 COMPONENT {component} "
            f"DIN-VS-DOUT-2H {relation(din[index], dout_2h[index])}"
        )
        require(lines[7 + index] == expected, f"{component} relation differs")
    return dout_h, dout_2h, din


def component_rows(
    dout_h: tuple[int, ...],
    dout_2h: tuple[int, ...],
    din: tuple[int, ...],
) -> tuple[list[dict[str, str]], bool]:
    rows: list[dict[str, str]] = []
    all_resolved = True
    for index, name in enumerate(PROTOCOL_COMPONENTS):
        outer = dout_2h[index]
        inner = din[index]
        if outer > 0:
            coarse_case = "POSITIVE"
            status = "RESOLVED" if inner < outer else "UNRESOLVED"
        else:
            coarse_case = "ZERO"
            status = "RESOLVED" if inner == 0 else "UNRESOLVED"
        all_resolved = all_resolved and status == "RESOLVED"
        rows.append(
            {
                "name": name,
                "d_out_h_f64_bits": f"0x{dout_h[index]:016x}",
                "d_out_2h_f64_bits": f"0x{outer:016x}",
                "d_in_f64_bits": f"0x{inner:016x}",
                "coarse_outer_case": coarse_case,
                "relation": relation(inner, outer),
                "status": status,
            }
        )
    return rows, all_resolved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("checker_log", type=Path)
    parser.add_argument("scientific_manifest", type=Path)
    parser.add_argument("protocol", type=Path)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument(
        "--mode",
        required=True,
        choices=("capture", "replay"),
    )
    parser.add_argument("--capture-manifest", type=Path)
    parser.add_argument("--capture-receipt", type=Path)
    parser.add_argument("--capture-artifact-dir", type=Path)
    parser.add_argument("--capture-commit")
    args = parser.parse_args()

    load_protocol(args.protocol)
    current_raw, _ = verify_manifest(
        args.scientific_manifest,
        args.artifact_dir,
        args.mode,
    )
    dout_h, dout_2h, din = parse_pair_log(args.checker_log)
    rows, all_resolved = component_rows(dout_h, dout_2h, din)

    if args.mode == "capture":
        require(
            args.capture_manifest is None
            and args.capture_receipt is None
            and args.capture_artifact_dir is None
            and args.capture_commit is None,
            "capture mode forbids replay arguments",
        )
        classification = (
            "PENDING-REPLAY" if all_resolved else "UNRESOLVED"
        )
        replay = {
            "status": "NOT-RUN",
            "scientific_manifest_sha256": None,
        }
        next_step = (
            "COMMIT-CAPTURE-MANIFEST-BEFORE-EXPLICIT-REPLAY"
            if all_resolved
            else "STOP-NO-TOLERANCE-SEARCH"
        )
    else:
        require(all_resolved, "replay is forbidden after UNRESOLVED capture")
        require(
            args.capture_manifest is not None
            and args.capture_receipt is not None
            and args.capture_artifact_dir is not None
            and args.capture_commit is not None,
            "replay requires committed capture evidence",
        )
        committed_raw = git_blob(args.capture_commit, args.capture_manifest)
        capture_raw, capture_entries = verify_manifest(
            args.capture_manifest,
            args.capture_artifact_dir,
            "capture",
        )
        require(
            committed_raw == capture_raw == current_raw,
            "replay manifest differs from committed capture",
        )
        verify_capture_receipt(
            args.capture_receipt,
            args.capture_commit,
            args.capture_artifact_dir,
            capture_raw,
        )
        replay_root = args.artifact_dir.resolve(strict=True)
        capture_root = args.capture_artifact_dir.resolve(strict=True)
        verify_inode_separation(capture_root, replay_root)
        for name in SCIENTIFIC_FILES:
            capture_file = capture_root / name
            replay_file = replay_root / name
            require(
                sha256_file(replay_file) == capture_entries[name],
                f"replay file differs from capture: {name}",
            )
        classification = "QUALIFIED-ON-2H-TO-H-SCALE"
        replay = {
            "status": "VERIFIED",
            "scientific_manifest_sha256": sha256_bytes(current_raw),
        }
        next_step = "MAY-FREEZE-STAGE5-PROTOCOL"

    result = {
        "schema": "spot-inner-sensitivity-v2-result-1",
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "tolerance_f32_bits": {
            "coarse_2h": "0x358637bd",
            "fine_h": "0x350637bd",
        },
        "scientific_manifest_sha256": sha256_bytes(current_raw),
        "components": rows,
        "replay": replay,
        "classification": classification,
        "outer_convergence": "NOT-EVALUATED",
        "next_step": next_step,
    }
    sys.stdout.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()

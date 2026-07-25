#!/usr/bin/env python3
"""Fail-closed checker for the Stage-4 v2 tolerance-sensitivity freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
PROTOCOL = ITERATIVE / "inner_sensitivity_v2_protocol.json"
RECEIPT = ITERATIVE / "inner_sensitivity_v2_freeze_receipt.sha256"
EXPECTED_PROTOCOL_SHA256 = (
    "8a870a85ffe7fd4eb53d9494bcf28acea2025f8f3d022579312cd34a22a1d88c"
)
EXPECTED_PARENT = "5e84bb39f6945eb25a4798ca07d45ab38d76bf85"
SHA_ROW = re.compile(r"([0-9a-f]{64})  ([^\t]+)")

RECEIPT_PATHS = (
    "validation/iterative/inner_sensitivity_v2_protocol.json",
    "validation/iterative/inner_sensitivity_v2.md",
    "validation/iterative/check_inner_sensitivity_v2_protocol.py",
    "validation/iterative/inner_sensitivity_protocol.json",
    "validation/iterative/one_map_result.md",
    "validation/iterative/inner_sensitivity_result.md",
    "validation/iterative/inner_sensitivity_failure_receipt.sha256",
    "validation/iterative/raw_moc_capture_result.md",
    "validation/iterative/gmres_activity_result.md",
    "data/SpotRefFS.c2m",
    "data/SpotPlaneFS.c2m",
    "validation/iterative/one_corrected_map.x2m",
    "validation/iterative/check_gmres_activity_result_history.py",
    "README.md",
    "SPOT_doc/validation_plan.md",
    "validation/iterative/README.md",
    "validation/run_fast.sh",
)

TOP_LEVEL_KEYS = [
    "name",
    "version",
    "status",
    "amendment",
    "frozen_parent_commit",
    "purpose",
    "prior_evidence",
    "mathematical_definition",
    "tolerance_pair",
    "locked_inputs",
    "locked_solver_controls",
    "execution_budget",
    "required_implementation_properties",
    "independent_checks",
    "classification",
    "forbidden_changes",
    "interpretation_limits",
    "next_decision",
]

PUBLIC_HASHES = {
    "validation/iterative/one_map_result.md": (
        "d2e5c7dd20fe373990f4fe6d90ff6647bb5e66c3b2600eba4550c27b30c9ebff"
    ),
    "validation/iterative/inner_sensitivity_result.md": (
        "c1e5dafa8d041ef799a17db9e8c676fdbb03c338e8c79a3e02d95ecc383c8981"
    ),
    "validation/iterative/inner_sensitivity_failure_receipt.sha256": (
        "3be04bac06c3dbe9616e65a7fca49b95dc3e297ed2cfcbaa7cfca80f909aff85"
    ),
    "validation/iterative/raw_moc_capture_result.md": (
        "f9d52c9b5fc7377d95b2efa235be74dab7c35fee0b4181e00bc4464b9e6e8d5a"
    ),
    "validation/iterative/gmres_activity_result.md": (
        "712719e0c6871f91c60ddfffaa92148ffe890aa6f51c6158a8d74b8d27edbeae"
    ),
    "validation/iterative/inner_sensitivity_protocol.json": (
        "0c5e09527d8542c51d6cc0785c6664c76606967687149a1cb6ce588f68c6ce06"
    ),
    "data/SpotRefFS.c2m": (
        "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742"
    ),
    "data/SpotPlaneFS.c2m": (
        "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5"
    ),
    "validation/iterative/one_corrected_map.x2m": (
        "4c8780b1739b5aaec0c78d0cbe2b23b6021f860d232af8e9c1767ed989c9720e"
    ),
}

LOCAL_HASHES = {
    "validation/artifacts/iterative-map1/basis_reference.xsm": (
        "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504"
    ),
    "validation/artifacts/iterative-map1/state0_axial.xsm": (
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb"
    ),
    "validation/artifacts/iterative-map1/state1_system.xsm": (
        "fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2"
    ),
    "validation/artifacts/iterative-map1/state1_axial.xsm": (
        "2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484"
    ),
    "validation/artifacts/iterative-map1/state1_snapshots.xsm": (
        "1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1"
    ),
    "validation/artifacts/iterative-seed/initial_snapshots.xsm": (
        "37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95"
    ),
    "validation/artifacts/iterative-seed/initial_axial_track.xsm": (
        "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7"
    ),
    "validation/artifacts/iterative-seed/initial_axial_macrolib.xsm": (
        "2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a"
    ),
    "validation/artifacts/iterative-seed/initial_radial_track.bin": (
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8"
    ),
}


def fail(message: str) -> None:
    raise SystemExit(f"INNER-SENSITIVITY-V2 PROTOCOL FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path, owner: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid {owner}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def require_hashes(expected: dict[str, str]) -> None:
    for relative, digest in expected.items():
        path = ROOT / relative
        require_regular(path, relative)
        require(sha256(path) == digest, f"hash changed: {relative}")


def verify_receipt() -> None:
    require_regular(RECEIPT, "freeze receipt")
    raw = RECEIPT.read_bytes()
    require(
        raw.endswith(b"\n") and b"\r" not in raw and b"\0" not in raw,
        "freeze receipt is not canonical text",
    )
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError:
        fail("freeze receipt is not ASCII")
    require(len(lines) == len(RECEIPT_PATHS), "freeze receipt census differs")
    for line, expected_name in zip(lines, RECEIPT_PATHS, strict=True):
        match = SHA_ROW.fullmatch(line)
        require(match is not None, "malformed freeze receipt row")
        expected_digest, name = match.groups()
        require(name == expected_name, "freeze receipt order differs")
        relative = Path(name)
        require(
            not relative.is_absolute()
            and ".." not in relative.parts
            and relative.as_posix() == name,
            "unsafe freeze receipt path",
        )
        path = ROOT / relative
        require_regular(path, f"freeze receipt target {name}")
        require(sha256(path) == expected_digest, f"freeze receipt hash differs: {name}")


def f32_from_bits(text: str) -> float:
    require(
        len(text) == 10 and text.startswith("0x"),
        "invalid binary32 bit spelling",
    )
    try:
        raw = int(text[2:], 16)
    except ValueError:
        fail("invalid binary32 hexadecimal bits")
    return struct.unpack(">f", raw.to_bytes(4, "big"))[0]


def round_f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def verify_protocol() -> dict[str, Any]:
    require_regular(PROTOCOL, "protocol")
    raw = PROTOCOL.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == EXPECTED_PROTOCOL_SHA256,
        "frozen protocol bytes changed",
    )
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        fail("protocol is not ASCII")
    try:
        data = json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    canonical = json.dumps(data, ensure_ascii=True, indent=2) + "\n"
    require(text == canonical, "protocol is not canonical indented JSON")
    require(list(data) == TOP_LEVEL_KEYS, "top-level key order differs")
    return data


def verify_semantics(data: dict[str, Any]) -> None:
    require(data["version"] == 1, "version differs")
    require(
        data["status"] == "FROZEN-BEFORE-IMPLEMENTATION-AND-RUN",
        "freeze status differs",
    )
    require(data["frozen_parent_commit"] == EXPECTED_PARENT, "parent differs")

    amendment = data["amendment"]
    require(amendment["supersedes_result"] is False, "v1 result superseded")
    require(
        amendment["prior_classification"]
        == "INVALID-INNER-NONCONVERGENCE",
        "prior failure classification changed",
    )
    require(
        amendment["new_result_observed_before_freeze"] is False,
        "2h result was observed before freeze",
    )

    definition = data["mathematical_definition"]
    require(
        definition["ordered_components"] == ["R_rho", "R_L", "D_L", "R_a"],
        "component order differs",
    )
    require(definition["aggregation"] is None, "aggregation introduced")
    require(definition["error_estimator"] is None, "error estimator introduced")
    require(
        definition["convergence_order"] is None,
        "convergence-order claim introduced",
    )

    pair = data["tolerance_pair"]
    coarse = f32_from_bits(pair["coarse_2h"]["binary32_bits"])
    fine = f32_from_bits(pair["fine_h"]["binary32_bits"])
    require(
        pair["coarse_2h"]["decimal_input"] == "1.0E-6",
        "coarse tolerance differs",
    )
    require(
        pair["fine_h"]["decimal_input"] == "5.0E-7",
        "fine tolerance differs",
    )
    require(round_f32(0.5 * coarse) == fine, "factor-two identity fails")
    require(coarse > fine > 0.0, "tolerance ordering fails")

    controls = data["locked_solver_controls"]
    require(controls["map_radial_solves"] == 3, "radial solve count differs")
    require(controls["map_axial_solves"] == 1, "axial solve count differs")
    require(controls["maxout"] == 500, "MAXOUT changed")
    require(controls["maxinr"] == 740, "MAXINR changed")
    require(controls["rank"] == 1, "rank changed")
    require(controls["relaxation"] is None, "relaxation introduced")
    require(controls["fit"] is None, "fit introduced")
    require(controls["clipping"] is None, "clipping introduced")
    require(controls["model_terms_added"] == 0, "model term introduced")
    require(controls["online_basis_rebuild"] is False, "basis rebuild enabled")

    budget = data["execution_budget"]
    require(budget["protocol_freeze_transport_processes"] == 0, "run authorized")
    require(budget["current_dragon_run_authorized"] is False, "run authorized")
    require(
        budget["future_first_capture_processes_after_separate_authorization"]
        == 1,
        "future capture count differs",
    )
    require(
        budget["future_replay_processes_after_pending_result"] == 1,
        "future replay count differs",
    )
    require(
        budget["maximum_total_future_processes"] == 2,
        "future process total differs",
    )
    require(budget["automatic_replay"] is False, "automatic replay enabled")
    require(
        budget["wall_clock_limit_seconds_per_process"] == 120,
        "wall-clock bound differs",
    )
    require(
        budget["long_outer_trajectory_authorized"] is False,
        "long trajectory authorized",
    )
    require(budget["fine_map_rerun_required"] is False, "fine rerun enabled")

    rule = data["independent_checks"]["component_rule"]
    require(
        rule
        == {
            "positive_coarse_outer": "RESOLVED iff D_in < D_out_2h",
            "zero_coarse_outer": (
                "RESOLVED iff D_in == 0 at stored precision"
            ),
            "otherwise": "UNRESOLVED",
        },
        "component rule differs",
    )
    require(
        data["independent_checks"]["cross_component_weighting"] is None,
        "cross-component weighting introduced",
    )

    classification = data["classification"]
    require(
        classification["all_components_resolved_with_replay"]
        == "QUALIFIED-ON-2H-TO-H-SCALE",
        "qualification label differs",
    )
    require(
        "QUALIFIED-ON-2H-TO-H-SCALE" in data["next_decision"],
        "qualified decision missing",
    )
    require("INVALID" in data["next_decision"], "invalid stop missing")
    require("UNRESOLVED" in data["next_decision"], "unresolved stop missing")


def verify_parent_commit() -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{EXPECTED_PARENT}^{{commit}}"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "frozen parent commit is unavailable")


def verify_dragon(path: Path) -> None:
    require_regular(path, "Dragon executable")
    require(
        sha256(path)
        == "e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759",
        "Dragon does not match the frozen fine-map executable",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="skip ignored local scientific artifacts",
    )
    parser.add_argument(
        "--dragon",
        type=Path,
        help="optionally verify the exact frozen fine-map executable",
    )
    args = parser.parse_args()

    data = verify_protocol()
    verify_semantics(data)
    verify_parent_commit()
    require_hashes(PUBLIC_HASHES)
    verify_receipt()
    if not args.public_only:
        require_hashes(LOCAL_HASHES)
    if args.dragon is not None:
        verify_dragon(args.dragon)

    scope = "PUBLIC" if args.public_only else "PUBLIC+LOCAL"
    print(f"INNER-SENSITIVITY-V2 PROTOCOL PASS: {scope}; DRAGON-RUNS=0")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed checker for the protocol-only three-return Picard design."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROTOCOL = ROOT / "validation/iterative/picard_three_return_protocol.json"
EXPECTED_CANONICAL_SHA256 = (
    "e3bda278570a98dd3dffe545027348477ee176af6adbf3841bb9627f6610d364"
)
BASELINE_COMMIT = "3162369d66287b3664a16c98cc03481e99d4e421"

EXPECTED_AUTHORITY_HASHES = {
    "SPOT_doc/validation_plan.md":
        "7549c1c7004ba0763b8cc94248b6702d5b99edf1542c2d4f05e87f6404d76744",
    "validation/iterative/inner_sensitivity_v2_protocol.json":
        "8a870a85ffe7fd4eb53d9494bcf28acea2025f8f3d022579312cd34a22a1d88c",
    "validation/iterative/inner_sensitivity_v2_result.md":
        "d30af50b38a05a6ea6135705311bdab153718b781cb75df341b964a27ad2f5ae",
    "validation/iterative/radial_real64_route_protocol.json":
        "d89e7f13e61dfc994d14ca5c9b68439a9665022653b65520c8f566a659fdf472",
}

EXPECTED_INPUT_HASHES = {
    "validation/artifacts/iterative-map1/basis_reference.xsm":
        "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504",
    "validation/artifacts/iterative-map1/state0_axial.xsm":
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb",
    "validation/artifacts/iterative-seed/initial_axial_macrolib.xsm":
        "2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a",
    "validation/artifacts/iterative-seed/initial_axial_track.xsm":
        "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7",
    "validation/artifacts/iterative-seed/initial_radial_track.bin":
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    "validation/artifacts/iterative-seed/initial_snapshots.xsm":
        "37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95",
}

EXPECTED_SOURCE_HASHES = {
    "data/SpotPlaneFS.c2m":
        "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5",
    "data/SpotRefFS.c2m":
        "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742",
    "src/SPOASM.f":
        "6de74dd362a3226ef08913e62f95ecd37ce06e8a671ef97bd241f65e8d674d6e",
    "src/SPOF.f":
        "29e4a8f7ba19c7f1c5941727e2d290665dbb6de03004b49b8f722adbff840f07",
    "src/SPOFSRC.f90":
        "5c35d4e5a40566ab9554a3674bb4b9500fdc6f00d89fff4ab047441462d9d39c",
    "src/SPOGBAL.f90":
        "78bdfa42cc8caf1b6a4022562e5222344b8c85af76cba959372bf2c52c891b69",
    "src/SPOLEAK.f90":
        "6726d7bbd16269dfdce038640ed0d90f5dc310d2c63b03408041f19ecf355c2c",
    "src/SPOPROJ.f90":
        "8d7e93d4b850b45f31303d1cd8ad1c64496014c34d0edf7fc1b08b8932f153a7",
    "src/SPOSTATE.f90":
        "7d70abe19887542f53f6abfc64e180d31c0a24bb25be2337db52b48fd299039b",
    "src/SPOT1P.f90":
        "19fbfca6c6a6eceed90089f5f241f9a1e88e450c8225c2731f46754f9180c91c",
    "src/SPOXCONV.f90":
        "3703ba696939079454ab6b8440dcbdcd27f3b1d423a6da3090f1277f9e97c4b1",
    "validation/iterative/one_corrected_map.x2m":
        "4c8780b1739b5aaec0c78d0cbe2b23b6021f860d232af8e9c1767ed989c9720e",
}

EXPECTED_STATUS = {
    "classification": "FROZEN-PROTOCOL-ONLY",
    "authorized_now": False,
    "dragon_processes_authorized": 0,
    "transport_execution_authorized": False,
    "implementation_authorized": False,
    "governance": "NO-GO-UNDER-CURRENT-STAGE4",
    "stage4_original": "INVALID-INNER-NONCONVERGENCE",
    "stage4_v2": "UNRESOLVED",
    "replay": "NOT-AUTHORIZED",
    "outer_convergence": "NOT-EVALUATED",
    "stage5": "NOT-AUTHORIZED",
    "longer_trajectory": "NOT-AUTHORIZED",
    "real64_phase_b": "NOT-AUTHORIZED",
}

EXPECTED_FORBIDDEN_TOKENS = [
    "PASS",
    "QUALIFIED",
    "PENDING-REPLAY",
    "CONVERGED",
    "DIVERGED",
    "CONTRACTIVE",
    "STABLE",
]


class ProtocolError(RuntimeError):
    """Raised when the design ceases to be fail-closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(payload)


def git_blob(root: Path, commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        result.returncode == 0,
        f"cannot read baseline blob {relative_path}: "
        f"{result.stderr.decode(errors='replace').strip()}",
    )
    return result.stdout


def load_protocol(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"cannot load protocol: {exc}") from exc
    require(isinstance(data, dict), "protocol root must be an object")
    return data


def validate(data: dict[str, Any], root: Path, require_local: bool = False) -> None:
    require(
        canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
        "canonical protocol hash mismatch",
    )
    require(
        set(data) == {
            "schema",
            "title",
            "status",
            "governance",
            "scientific_object",
            "frozen_map",
            "frozen_inputs_sha256",
            "source_reference_sha256",
            "future_execution_shape",
            "initial_state_construction",
            "future_map_block",
            "measurements_per_return",
            "step_contracts",
            "future_result_classification",
            "forbidden_result_tokens",
            "interpretation",
            "current_actions",
        },
        "top-level keyset mismatch",
    )
    require(data["schema"] == "spot-picard-three-return-design-v1", "schema")
    require(data["status"] == EXPECTED_STATUS, "status or authorization changed")

    governance = data["governance"]
    require(governance["baseline_commit"] == BASELINE_COMMIT, "baseline commit")
    require(governance["supersedes_prior_result"] is False, "result supersession")
    require(
        governance["amends_prior_execution_prohibition"] is False,
        "execution prohibition amendment",
    )
    require(
        governance["frozen_authority_sha256"] == EXPECTED_AUTHORITY_HASHES,
        "authority hash map",
    )
    require(
        len(governance["future_execution_prerequisites"]) == 4,
        "future prerequisite count",
    )
    for rel, expected in EXPECTED_AUTHORITY_HASHES.items():
        require(
            sha256_bytes(git_blob(root, BASELINE_COMMIT, rel)) == expected,
            f"baseline authority hash mismatch: {rel}",
        )

    scientific = data["scientific_object"]
    require(scientific["map"] == "G_h_legacy32", "map identity")
    require(scientific["state"] == "x=(a,rho,L), rho=1/k", "state definition")
    require(
        scientific["update_rule"] == "x_next := G_h_legacy32(x_current)",
        "update rule",
    )
    require(scientific["return_indices"] == [0, 1, 2], "return indices")
    require(scientific["state_indices_saved"] == [0, 1, 2, 3], "state indices")
    require(scientific["returns"] == 3, "return count")
    require(scientific["adjustable_outer_parameters"] == [], "outer parameter")
    for field in ("relaxation", "fitting", "clipping", "flux_floor",
                  "adaptive_stopping"):
        require(scientific[field] == "ABSENT", f"{field} must remain absent")
    require(
        scientific["not_a_claim_of"] == [
            "convergence",
            "divergence",
            "contractivity",
            "stability",
            "spectral radius",
            "fixed-point existence",
            "fixed-point uniqueness",
            "asymptotic rate",
            "error bound",
            "physical accuracy",
            "Stage-4 qualification",
            "Stage-5 authorization",
        ],
        "claim boundary",
    )

    frozen = data["frozen_map"]
    require(frozen["arithmetic"] == "legacy binary32 radial working state",
            "arithmetic route")
    require(frozen["real64_lane"] == "OFF", "REAL64 must remain off")
    require(
        (
            frozen["rank"],
            frozen["groups"],
            frozen["radial_planes"],
            frozen["inner_tolerance_binary32_bits"],
            frozen["MAXOUT"],
            frozen["MAXINR"],
        )
        == (1, 370, 3, "0x350637bd", 500, 740),
        "frozen numerical controls",
    )
    require(frozen["online_radial_recalculation"] is True, "online radial map")
    require(frozen["physical_model_changes"] == [], "physical model change")
    require(frozen["control_changes"] == [], "solver control change")

    require(data["frozen_inputs_sha256"] == EXPECTED_INPUT_HASHES,
            "input hash map")
    require(data["source_reference_sha256"] == EXPECTED_SOURCE_HASHES,
            "source hash map")
    for rel, expected in EXPECTED_SOURCE_HASHES.items():
        require(
            sha256_bytes(git_blob(root, BASELINE_COMMIT, rel)) == expected,
            f"baseline source hash mismatch: {rel}",
        )
    if require_local:
        for rel, expected in EXPECTED_INPUT_HASHES.items():
            path = root / rel
            require(path.is_file(), f"missing local frozen input: {rel}")
            require(sha256_file(path) == expected,
                    f"local frozen input hash mismatch: {rel}")

    shape = data["future_execution_shape"]
    require(
        (
            shape["initializer_transport_solves"],
            shape["radial_solves"],
            shape["returned_axial_solves"],
            shape["outer_returns"],
            shape["map_blocks"],
        )
        == (0, 9, 3, 3, 3),
        "future solve shape",
    )
    for field in (
        "same_process",
        "fresh_isolated_work_directory",
        "map_blocks_must_be_explicit",
    ):
        require(shape[field] is True, f"{field} must be true")
    for field in (
        "outer_loop_constructs_allowed",
        "fourth_return_allowed",
        "retry_allowed",
        "resume_allowed",
        "automatic_replay_allowed",
        "archived_x1_splicing_allowed",
    ):
        require(shape[field] is False, f"{field} must be false")
    require(
        shape["wall_clock_safety_limit_seconds"]
        == "MUST-BE-FROZEN-BEFORE-AUTHORIZATION",
        "wall-clock limit was prematurely selected or omitted",
    )

    initial = data["initial_state_construction"]
    require(initial["transport_initializer"] == "FORBIDDEN", "initializer")
    require(initial["initializer_is_not_a_return"] is True, "initializer count")
    require(
        initial["first_map_input"] == "the reconstructed canonical x0 only",
        "first input",
    )
    require(len(data["future_map_block"]) == 11, "map block is incomplete")

    measures = data["measurements_per_return"]
    require(measures["existing_reported"] == ["R_rho", "R_L", "D_L", "R_a"],
            "existing measurements")
    require(
        measures["stored_numerators"] == [
            "D_rho=abs(delta_rho)",
            "D_L=max(abs(delta_L))",
            "D_a=sqrt(delta_a^T*Gram*delta_a)",
        ],
        "separate numerator definitions",
    )
    require(measures["component_aggregation"] == "FORBIDDEN", "aggregation")
    require(
        measures["single_state_norm"] == "UNDEFINED-AND-FORBIDDEN",
        "undeclared full-state norm",
    )
    require(len(measures["trend_relations"]) == 6, "trend relation count")
    require(measures["allowed_relation_tokens"] == ["LESS", "EQUAL", "GREATER"],
            "relation tokens")
    for field in ("ratio_gate", "percentage_gate", "trend_acceptance_gate"):
        require(measures[field] == "FORBIDDEN", f"{field}")

    results = data["future_result_classification"]
    require(set(results) == {"complete", "incomplete"}, "result branch keyset")
    complete = results["complete"]
    incomplete = results["incomplete"]
    require(
        complete["label"] == "CENSUS-COMPLETE-DIAGNOSTIC-ONLY",
        "complete label",
    )
    require(
        incomplete["label"] == "CENSUS-INCOMPLETE-NO-SCIENTIFIC-RESULT",
        "incomplete label",
    )
    require(complete["next"] == incomplete["next"] == "STOP", "result next")
    for field in (
        "replay_authorized",
        "stage4_qualified",
        "stage5_authorized",
        "longer_trajectory_authorized",
    ):
        require(complete[field] is False, f"complete {field}")
        require(incomplete[field] is False, f"incomplete {field}")
    require(complete["scientific_pass"] is False, "scientific pass")
    require(incomplete["trend_interpretation_allowed"] is False,
            "incomplete trend")
    require(incomplete["failed_return_state_reusable"] is False,
            "failed state reuse")
    require(incomplete["retry_authorized"] is False, "incomplete retry")
    require(data["forbidden_result_tokens"] == EXPECTED_FORBIDDEN_TOKENS,
            "forbidden result tokens")

    require(
        data["current_actions"] == [
            "Validate this protocol and its frozen hashes without Dragon.",
            "Do not implement or execute the three-return deck.",
            "Do not change any prior result classification or authorization.",
        ],
        "current actions",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--require-local", action="store_true")
    args = parser.parse_args()
    try:
        validate(load_protocol(args.protocol), ROOT, args.require_local)
    except ProtocolError as exc:
        raise SystemExit(f"PICARD-THREE-RETURN DESIGN REJECTED: {exc}") from exc
    local = " WITH-LOCAL" if args.require_local else " PUBLIC"
    print(
        "PICARD-THREE-RETURN DESIGN PASS:"
        f"{local}; PROTOCOL-ONLY; EXECUTION=NO-GO; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()

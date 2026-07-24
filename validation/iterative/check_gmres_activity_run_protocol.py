#!/usr/bin/env python3
"""Fail-closed checker for the bounded GMRES activity run protocol."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ITER = ROOT / "validation" / "iterative"
PROTOCOL = ITER / "gmres_activity_run_protocol.json"
EXPECTED_PROTOCOL_SHA256 = (
    "879194d5bd7c7fb6ef2538158d91095ff3026eebc329c126e122a526f566e3ee"
)
SOURCE_IMPLEMENTATION_COMMIT = "5816c8aad4fbb43542514d5bd571ebccecdb6d72"

EXPECTED_DEPENDENCIES = {
    "validation/iterative/gmres_activity_protocol.json":
        "27093c87b7321f4ecfd22307c7fac0ecc6d99a2eb5b2019509d2bf11c663cc85",
    "validation/iterative/check_gmres_activity_protocol.py":
        "675ce5191e8fabcdcc4e2884c6868df69f9fd123503bc7567e30f642a74b7726",
    "validation/iterative/gmres_activity_implementation.sha256":
        "8bed8f3726cc4a903024fbbfe32f1ff79bce51bdbeac01054528bfeca1d56f26",
    "validation/iterative/check_gmres_activity_implementation.py":
        "47283f44d5555ea89ecaeddb1878f8c005a2ae30a71e3d8e698fddf4357a0964",
    "validation/iterative/gmres_activity_overlay_manifest.json":
        "b117cea97cfb54b4b043bc923c435a736d01b54fbb8fcfd5fdcb1472c39283a3",
    "validation/iterative/gmres_activity_overlay.patch":
        "ebdc1eee70422e0c881901802602d053b61079ad942ec1dbdf16fbe88fc8f942",
    "validation/iterative/run_gmres_activity_preflight.sh":
        "f880a3d668e34d180011fac51ad58df13cace0c06588d77815f6eca4273389bb",
    "validation/iterative/check_gmres_activity_xsm.f90":
        "9c5ccb762dbb1f9947a7d6c587612862bfd6bdf1e7240172d3b25f316386bf99",
    "validation/iterative/normalize_gmres_activity_log.py":
        "94d244d089c18b2b6371d0910e5979cf9c64881ea663ec3cd3e285edf55b6b1d",
    "validation/iterative/raw_moc_capture_result_receipt.sha256":
        "485baab029387aeb8212647768be96b6eba438119e7d6ddcf013ccaf5e3359b5",
    "validation/iterative/raw_moc_ulp_bridge_result_receipt.sha256":
        "20dc353133c6251021fb87f0196061fb0b1be969d8e73890b7a9b1b073e60935",
}

EXPECTED_INPUTS = {
    "validation/artifacts/raw-moc-capture/stationary/pre.xsm":
        "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e",
    "validation/artifacts/raw-moc-capture/stationary/off.xsm":
        "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789",
    "validation/artifacts/raw-moc-capture/stationary/on.xsm":
        "de27778fb23f035aafab0e6ca877faf0f64a0662d255fa485b8174fea81f87ae",
    "validation/artifacts/raw-moc-capture/stationary_off/probe.log":
        "b15a3c9e0ad3bdc54ed3e50bba9e9cbb22a885bb68f712fb83ea02ef1e109234",
    "validation/artifacts/raw-moc-capture/stationary_on/probe.log":
        "03f802bea77875419e126ec51282924b2717bed7b987c8171febc2738a2bfe25",
    "validation/artifacts/raw-moc-capture/common/restart_macro0.xsm":
        "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
    "validation/artifacts/raw-moc-capture/common/restart_source.xsm":
        "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
    "validation/artifacts/raw-moc-capture/common/restart_system.xsm":
        "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
    "validation/artifacts/raw-moc-capture/common/restart_track.xsm":
        "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
    "validation/artifacts/raw-moc-capture/common/initial_radial_track.bin":
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
}

EXPECTED_IMPLEMENTATION_PATHS = {
    "validation/iterative/build_gmres_activity_overlay.sh",
    "validation/iterative/check_gmres_activity_implementation.py",
    "validation/iterative/check_gmres_activity_protocol.py",
    "validation/iterative/check_gmres_activity_xsm.f90",
    "validation/iterative/gmres_activity.md",
    "validation/iterative/gmres_activity_overlay.patch",
    "validation/iterative/gmres_activity_overlay_manifest.json",
    "validation/iterative/gmres_activity_protocol.json",
    "validation/iterative/make_gmres_activity_fixture.f90",
    "validation/iterative/normalize_gmres_activity_log.py",
    "validation/iterative/run_gmres_activity_checker_test.sh",
    "validation/iterative/run_gmres_activity_preflight.sh",
    "validation/iterative/run_gmres_activity_state_test.sh",
    "validation/iterative/test_gmres_activity_state.f90",
}

EXPECTED_PAYLOAD = [
    "gmres_activity_run_protocol.json",
    "gmres_activity_run_implementation.sha256",
    "run_receipt.tsv",
    "run_commit.txt",
    "source_identity.tsv",
    "build_receipt.tsv",
    "toolchain.sha256",
    "symbol_audit.txt",
    "instrumented_source_manifest.sha256",
    "implementation_replay.log",
    "inputs_before.sha256",
    "inputs_after.sha256",
    "executable.sha256",
    "preflight.log",
    "postflight.log",
    "track.xsm",
    "off/deck.x2m",
    "off/run.log",
    "off/normalized.log",
    "off/result.xsm",
    "on_a/deck.x2m",
    "on_a/run.log",
    "on_a/normalized.log",
    "on_a/result.xsm",
    "on_a/ledger.txt",
    "on_a/ledger_repeat.txt",
    "on_a/non_audit_identity.txt",
    "on_b/deck.x2m",
    "on_b/run.log",
    "on_b/normalized.log",
    "on_b/result.xsm",
    "on_b/ledger.txt",
    "on_b/ledger_repeat.txt",
    "on_b/non_audit_identity.txt",
    "log_identity.txt",
    "reader_replay.sha256",
    "artifact_check_a.log",
    "artifact_check_b.log",
    "result.txt",
    "artifact_manifest.sha256",
]

EXPECTED_NEW_FILES = [
    "validation/iterative/gmres_activity_run_reference.sha256",
    "validation/iterative/gmres_activity_probe.x2m.in",
    "validation/iterative/run_bounded_gmres_activity.py",
    "validation/iterative/test_bounded_gmres_activity.py",
    "validation/iterative/check_gmres_activity_run_logs.py",
    "validation/iterative/test_gmres_activity_run_logs.py",
    "validation/iterative/check_gmres_activity_pair_xsm.f90",
    "validation/iterative/check_gmres_activity_artifact.py",
    "validation/iterative/test_gmres_activity_artifact.py",
    "validation/iterative/run_gmres_activity_production.sh",
    "validation/iterative/gmres_activity_run_implementation.sha256",
]


class ContractError(RuntimeError):
    """A deterministic protocol contract violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_regular(path: Path, label: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid {label}")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def read_protocol() -> dict[str, Any]:
    require_regular(PROTOCOL, "run protocol")
    raw = PROTOCOL.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_PROTOCOL_SHA256,
            "run protocol SHA256 differs")
    require(raw.endswith(b"\n") and b"\r" not in raw and b"\0" not in raw,
            "run protocol is not canonical LF text")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError("run protocol is not UTF-8") from exc
    return json.loads(text, object_pairs_hook=reject_duplicate_pairs)


def assert_integer_json(value: Any) -> None:
    if isinstance(value, float):
        raise ContractError("floating JSON number is forbidden")
    if isinstance(value, dict):
        for child in value.values():
            assert_integer_json(child)
    elif isinstance(value, list):
        for child in value:
            assert_integer_json(child)


def flatten_declared_dependencies(data: dict[str, Any]) -> dict[str, str]:
    frozen = data["frozen_dependencies"]
    result = {
        frozen[name]["path"]: frozen[name]["sha256"]
        for name in (
            "method_protocol",
            "method_protocol_checker",
            "implementation_manifest",
            "implementation_checker",
            "overlay_manifest",
            "overlay_patch",
            "preflight",
            "independent_ledger_reader",
            "log_normalizer",
        )
    }
    result.update(frozen["parent_result_receipts"])
    return result


def flatten_declared_inputs(data: dict[str, Any]) -> dict[str, str]:
    return {
        entry["path"]: entry["sha256"]
        for entry in data["immutable_inputs"]["files"].values()
    }


def verify_implementation_manifest() -> None:
    path = ITER / "gmres_activity_implementation.sha256"
    require_regular(path, "implementation manifest")
    rows = [
        line.split()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    require(
        len(rows) == len(EXPECTED_IMPLEMENTATION_PATHS)
        and all(len(row) == 2 for row in rows)
        and {row[1] for row in rows} == EXPECTED_IMPLEMENTATION_PATHS,
        "implementation manifest census differs",
    )
    for digest, relative in rows:
        require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
                f"invalid manifest SHA256 for {relative}")
        target = ROOT / relative
        require_regular(target, relative)
        require(sha256(target) == digest,
                f"implementation manifest hash differs for {relative}")


def validate_payload(data: dict[str, Any], verify_files: bool) -> None:
    assert_integer_json(data)
    require(
        set(data) == {
            "name",
            "version",
            "status",
            "protocol_freeze_authorizes_execution",
            "source_implementation_commit",
            "scientific_question",
            "scope",
            "frozen_dependencies",
            "clean_build",
            "immutable_inputs",
            "activation",
            "process_execution",
            "run_matrix",
            "solver_controls",
            "execution_budget",
            "runtime_identity",
            "reproducibility_and_closure",
            "independence",
            "classification",
            "artifact",
            "run_implementation_freeze",
            "failure_and_retention",
            "interpretation_limits",
            "next_step_by_class",
        },
        "top-level protocol census differs",
    )
    require(data["version"] == 1, "protocol version differs")
    require(
        data["status"] == "FROZEN-BEFORE-RUNNER-IMPLEMENTATION"
        and data["protocol_freeze_authorizes_execution"] is False,
        "protocol freeze authorizes execution",
    )
    require(
        data["source_implementation_commit"] == SOURCE_IMPLEMENTATION_COMMIT,
        "source implementation commit differs",
    )
    require(
        data["scientific_question"]
        == (
            "Does the frozen STATIONARY one-map MCCG path contain at least "
            "one physical group and correction block with KMAX greater "
            "than zero?"
        ),
        "scientific question differs",
    )
    require(
        data["scope"]
        == {
            "observed_quantity": "existing integer GMRES control-flow activity",
            "one_map_Dragon_processes": 3,
            "DOORFV_calls_per_process": 1,
            "instrumentation_added_operator_applications": 0,
            "floating_point_values_added_to_solver": 0,
            "floating_point_operations_added_to_solver": 0,
            "solver_feedback": False,
            "precision_change": False,
            "physical_equation_change": False,
            "outer_convergence_evaluated": False,
            "long_trajectory": False,
            "rank_comparison": False,
        },
        "scientific scope differs",
    )
    require(
        flatten_declared_dependencies(data) == EXPECTED_DEPENDENCIES,
        "frozen dependency declaration differs",
    )
    require(
        flatten_declared_inputs(data) == EXPECTED_INPUTS,
        "immutable input declaration differs",
    )
    require(
        data["immutable_inputs"]["copy_policy"]
        == (
            "each process receives distinct regular non-symlink copies of "
            "every common input and one PRE-initialized writable result.xsm, "
            "all with distinct inodes"
        )
        and data["immutable_inputs"]["immutability_check"]
        == (
            "common inputs and read-only references are unchanged before "
            "and after every process; result.xsm must equal PRE before "
            "execution and is the only permitted writable XSM during that "
            "process"
        ),
        "mutable result and immutable input boundary differs",
    )

    build = data["clean_build"]
    require(
        build["frozen_parent_commit"]
        == "4d7abb23ac7975d4146beaa3b0049e36cdad8776"
        and build["parent_git_archive_sha256"]
        == "a1ee2a7ef3fb128afe4b1fe14c7021a1cff1b1d80adb18548fb22840969e23aa"
        and build["tracked_live_src"] == "UNCHANGED"
        and build["compiler_path"]
        == "/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15"
        and build["compiler_sha256"]
        == "0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492"
        and build["platform"] == "Darwin arm64"
        and build["build_command"]
        == (
            "env -i LC_ALL=C "
            "PATH=/opt/homebrew/Cellar/gcc/15.2.0_1/bin:"
            "/Library/Developer/CommandLineTools/usr/bin:/usr/bin:/bin "
            "/Library/Developer/CommandLineTools/usr/bin/make "
            "-j4 -C CLEAN_OVERLAY/src Dragon"
        )
        and build["compile_and_link_flags_from_makefile"]
        == (
            "-O2 -march=native -ffp-contract=off -g; Darwin arm64 PIC "
            "defaults; OpenMP off"
        )
        and build["build_toolchain"]
        == {
            "/Library/Developer/CommandLineTools/usr/bin/make":
                "8c221cc6f9e80bd3d48149b5523f932eec8c0656cf98f47655f7bb3064fbc8e4",
            "/Library/Developer/CommandLineTools/usr/bin/ar":
                "7020135f5004b53ddf787cb025dc983654463eab07237ec200d539c451d91acf",
            "/Library/Developer/CommandLineTools/usr/bin/as":
                "06770364632b454317238e79d670c094e27301c7322c3a488323bd42e4d0bcbc",
            "/Library/Developer/CommandLineTools/usr/bin/cpp":
                "c45eaf986e9081c117ad8561ddfad827f0d8ce41d2b4ade56409d15b69c2d3ab",
            "/Library/Developer/CommandLineTools/usr/bin/gcc":
                "f79e77ba3fbdac494bdca6082a891bbd3203b70a29021d1368a943acbc89a882",
            "/Library/Developer/CommandLineTools/usr/bin/ld":
                "765e5fa4e30980ddf2803c8a973b20fcc63e403098d2dd9b6cefa38e0cde3c2e",
            "/Library/Developer/CommandLineTools/usr/bin/python3":
                "4b42b1a117605cafc8607b67b0892a609c2cd125012dd56288abeed8c89cdfb1",
        }
        and build["build_toolchain_versions"]
        == {
            "make": "GNU Make 3.81",
            "cpp_and_gcc":
                "Apple clang version 21.0.0 (clang-2100.1.1.101)",
            "ld": "@(#)PROGRAM:ld PROJECT:ld-1267",
            "python3": "Python 3.9.6",
        }
        and build["selected_developer_directory"]
        == "/Library/Developer/CommandLineTools"
        and build["sdk_path"]
        == "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
        and build["host_os"] == "macOS 26.5.1 build 25F80"
        and build["toolchain_resolution"]
        == (
            "the frozen paths are the actual Command Line Tools executables, "
            "not the common /usr/bin xcrun launcher shim; final library and "
            "executable hashes in the run reference remain authoritative"
        )
        and build["linked_library_outputs_required_in_run_reference"]
        == [
            "Ganlib/lib/Darwin_arm64/libGanlib.a",
            "Utilib/lib/Darwin_arm64/libUtilib.a",
            "Trivac/lib/Darwin_arm64/libTrivac.a",
            "lib/Darwin_arm64/libDragon.a",
            "bin/Darwin_arm64/Dragon",
        ]
        and build["same_executable_for_all_processes"] is True,
        "clean build identity differs",
    )
    require(
        len(build["required_before_RUN"]) == 5
        and any("executable and linked-library SHA256" in row
                for row in build["required_before_RUN"]),
        "executable freeze requirements differ",
    )

    require(
        data["activation"]
        == {
            "runner_environment": "RUN_GMRES_ACTIVITY",
            "absent": "PREFLIGHT-ONLY",
            "value_1": (
                "RUN only after every required committed implementation "
                "and executable gate passes"
            ),
            "any_other_value_including_empty": "FAIL-CLOSED",
            "preflight_must_not_invoke_Dragon": True,
            "production_preflight_invocation": (
                "env -u RUN_GMRES_ACTIVITY -u FC "
                "run_gmres_activity_preflight.sh"
            ),
            "frozen_preflight_rejection_is_not_modified": True,
        },
        "activation gate differs",
    )
    require(
        data["process_execution"]
        == {
            "executable": (
                "one frozen absolute non-overridable Dragon path created "
                "by the clean build"
            ),
            "argv": ["absolute frozen Dragon executable"],
            "stdin": (
                "the exact rendered regular non-symlink deck for that case"
            ),
            "cwd": "the fresh isolated case directory",
            "stdout_and_stderr": (
                "one merged run.log created with exclusive-create semantics"
            ),
            "shell": False,
            "start_new_session": True,
            "environment": {
                "inherit_parent_environment": False,
                "LC_ALL": "C",
                "PATH": "/usr/bin:/bin",
                "TMPDIR": "fresh case-local tmp directory",
            },
            "shell_runner_direct_Dragon_calls": 0,
            "bounded_wrapper_Dragon_call_sites": 1,
            "strict_process_order": ["OFF", "ON-A", "ON-B"],
            "retries": 0,
            "overrides_for_executable_compiler_path_artifact_or_inputs":
                "FORBIDDEN",
        },
        "unique Dragon invocation contract differs",
    )
    require(
        data["run_matrix"]
        == [
            {
                "name": "OFF",
                "MOCA": "ABSENT",
                "GMRA": "ABSENT",
                "repetitions": 1,
            },
            {
                "name": "ON-A",
                "MOCA": 2,
                "GMRA": "PRESENT",
                "repetitions": 1,
            },
            {
                "name": "ON-B",
                "MOCA": 2,
                "GMRA": "PRESENT",
                "repetitions": 1,
            },
        ],
        "three-process run matrix differs",
    )

    controls = data["solver_controls"]
    require(
        controls["TYPE"] == "S"
        and controls["door"] == "MCCG"
        and controls["plane"] == 1
        and controls["MAXOUT"] == 1
        and controls["MAXINR"] == 740
        and controls["EPSOUT_decimal"] == "2.5E-7"
        and controls["EPSUNK_decimal"] == "2.5E-7"
        and controls["EPSINR_decimal"] == "2.5E-7"
        and controls["epsilon_binary32_bits"] == "348637BD"
        and controls["free_steps"] == 1
        and controls["accelerated_steps"] == 0
        and controls["ILEAK"] == 0
        and controls["MCGMRE_MAXI"] == 20
        and controls["MCGMRE_MAXIT"] == 19
        and controls["MCGMRE_KRYL"] == 10
        and controls["MCGMRE_ERRTOL_binary32_bits"] == "3727C5AC",
        "solver controls differ",
    )
    require(
        data["execution_budget"]
        == {
            "Dragon_processes": 3,
            "FLU_outer_updates_per_process": 1,
            "wall_timeout_seconds_per_process": 30,
            "termination_grace_seconds_after_timeout": 5,
            "timeout_role": (
                "operational process bound only; never a scientific "
                "acceptance threshold"
            ),
            "timeout_result": "INVALID-NO-SCIENTIFIC-RESULT",
            "termination_scope": (
                "only the exact spawned process group; never killall"
            ),
            "preparation_Dragon_processes": 0,
            "six_step_arm_reruns": 0,
            "automatic_follow_on_processes": 0,
        },
        "execution budget differs",
    )
    identity = data["runtime_identity"]
    require(
        identity["normal_Dragon_end_count_per_process"] == 1
        and identity["outer_iterations_per_process"] == 1
        and identity["thermal_iterations_per_process"] == 1
        and identity["DOORFV_calls_per_process"] == 1
        and identity["MCCGF_calls_per_process"] == 1
        and identity["ON_MCGMRE_entries"] == 1
        and identity["ON_MCGMRE_normal_exits"] == 1
        and identity["ON_primary_role_events_minimum_exact_integer"] == 1
        and identity["second_ON_MCGMRE_entry"] == "INVALID",
        "runtime identity differs",
    )
    closure = data["reproducibility_and_closure"]
    require(
        len(closure) == 10
        and any("byte-identical to LEGACY_OFF_XSM" in row for row in closure)
        and any("outside the single added SPOT-GMR-AUD" in row
                for row in closure)
        and any("ON-A and ON-B output XSM files are byte-identical" in row
                for row in closure)
        and any("independently closes every event" in row for row in closure),
        "reproducibility closure differs",
    )

    independent = data["independence"]
    require(
        independent["forbidden_trusted_derived_rows"]
        == [
            "STATE",
            "ROLE-SUM",
            "K-HISTOGRAM",
            "NONZERO-K-GROUP-BLOCKS",
            "SUM-K",
            "MAX-K",
            "CLASSIFICATION",
        ]
        and independent["forbidden_reader_symbols"]
        == [
            "Dragon",
            "FLU",
            "DOORFV",
            "MCCGF",
            "MCGFLX",
            "MCGFL1",
            "MCGMRE",
            "SPOMGMR",
            "SPOMOC",
        ]
        and independent["artifact_checker_scientific_reconstruction_input"]
        == (
            "only the raw ROLE, ROLE-ACTIVE, BLOCK and BLOCK-GROUP rows "
            "in the two independently read ledgers"
        )
        and independent["artifact_checker_validity_inputs"]
        == (
            "the complete required payload, including hashes, receipts, "
            "original and normalized logs, XSM identity evidence, reader "
            "replays and publication manifests"
        )
        and "reconstruct every per-block per-group KMAX"
        in independent["artifact_checker_reconstruction"],
        "independent-checker boundary differs",
    )
    require(
        independent["artifact_checker_stdout"]
        == {
            "valid_active": "VALID-GMRES-UPDATE-ACTIVE",
            "valid_inactive": "VALID-GMRES-UPDATE-INACTIVE",
            "invalid": "INVALID",
        }
        and independent["invalid_artifact_checker_behavior"]
        == "nonzero exit; create neither result.txt nor a final artifact",
        "artifact checker result behavior differs",
    )
    require(
        data["classification"]
        == {
            "threshold": None,
            "INVALID": (
                "any identity, hash, process, log, XSM, ledger, "
                "reproducibility, publication or receipt check fails"
            ),
            "VALID-GMRES-UPDATE-INACTIVE": (
                "all checks pass and the exact nonzero-K group-block "
                "count is zero"
            ),
            "VALID-GMRES-UPDATE-ACTIVE": (
                "all checks pass and the exact nonzero-K group-block "
                "count is a positive integer"
            ),
            "valid_classes_are_mutually_exclusive_and_exhaustive": True,
            "zero_is_a_valid_scientific_result": True,
        },
        "classification differs",
    )

    artifact = data["artifact"]
    require(
        artifact["path"] == "validation/artifacts/gmres-activity-census"
        and artifact["existing_path_policy"] == "FAIL-CLOSED-NO-OVERWRITE"
        and artifact["publication_lock"]
        == (
            "exclusive sibling mkdir acquired before the first Dragon "
            "process and released only after final artifact verification"
        )
        and artifact["publication"]
        == "single atomic rename only after every check passes"
        and artifact["publication_sequence"]
        == (
            "verify WORK payload, copy to same-filesystem PUBLISH, verify "
            "PUBLISH completely, atomically rename once, then verify the "
            "final artifact completely"
        )
        and artifact["symlinks_and_special_files"] == "FORBIDDEN"
        and artifact["case_directory_census"].startswith(
            "exact declared common inputs"
        )
        and artifact["required_payload"] == EXPECTED_PAYLOAD
        and len(set(artifact["required_payload"])) == len(EXPECTED_PAYLOAD)
        and artifact["manifest_rule"]
        == (
            "sorted SHA256 rows for every regular payload except "
            "artifact_manifest.sha256 itself"
        ),
        "artifact publication contract differs",
    )
    result_format = artifact["result_format"]
    require(
        len(result_format) == 11
        and result_format[0] == "GMRES-ACTIVITY RESULT 1"
        and result_format[-2:] == [
            "CLASSIFICATION <one frozen valid class>",
            "COMPLETE",
        ]
        and "THRESHOLD NONE" in result_format,
        "result format differs",
    )
    require(
        artifact["scientific_decision_field"]
        == (
            "only CLASSIFICATION answers the frozen scientific question; "
            "histogram, nonzero count, sum and maximum are exact closure "
            "evidence"
        ),
        "scientific decision field differs",
    )
    require(
        artifact["run_receipt_tsv_rows_in_order"]
        == [
            "schema\t1",
            "run_commit\t<40 lowercase hexadecimal Git commit>",
            (
                "source_implementation_commit\t"
                "5816c8aad4fbb43542514d5bd571ebccecdb6d72"
            ),
            (
                "method_protocol_sha256\t"
                "27093c87b7321f4ecfd22307c7fac0ecc6d99a2eb5b2019509d2bf11c663cc85"
            ),
            "run_protocol_sha256\t<SHA256 of frozen run protocol bytes>",
            (
                "method_implementation_manifest_sha256\t"
                "8bed8f3726cc4a903024fbbfe32f1ff79bce51bdbeac01054528bfeca1d56f26"
            ),
            (
                "run_implementation_manifest_sha256\t"
                "<SHA256 of frozen run implementation manifest bytes>"
            ),
            "executable_sha256\t<SHA256 of the frozen linked Dragon>",
            "process_matrix\tOFF=1,ON=2",
            "classification\t<one frozen valid class>",
        ],
        "run receipt schema differs",
    )

    freeze = data["run_implementation_freeze"]
    require(
        freeze["required_new_files"] == EXPECTED_NEW_FILES
        and freeze["required_frozen_inputs_to_future_runner"]
        == [
            "validation/iterative/gmres_activity_run_protocol.json",
            "validation/iterative/check_gmres_activity_run_protocol.py",
            "validation/iterative/gmres_activity_implementation.sha256",
            "validation/iterative/build_gmres_activity_overlay.sh",
            "validation/iterative/check_gmres_activity_implementation.py",
            "validation/iterative/check_gmres_activity_xsm.f90",
            "validation/iterative/normalize_gmres_activity_log.py",
            "validation/iterative/run_gmres_activity_preflight.sh",
        ]
        and freeze["current_state"]
        == "NOT-IMPLEMENTED; RUN_GMRES_ACTIVITY=1 REMAINS UNAUTHORIZED",
        "future run implementation freeze differs",
    )
    require(
        freeze["required_artifact_checker_tests"]
        == [
            "valid raw ACTIVE fixture",
            "valid raw INACTIVE fixture",
            (
                "tampered derived summary with unchanged raw rows is "
                "rejected rather than changing classification"
            ),
            "tampered raw active mask is rejected",
            "tampered raw BLOCK-GROUP KMAX is rejected",
            "missing log, XSM identity, receipt or manifest evidence is rejected",
            "invalid input creates neither result.txt nor a final artifact",
        ],
        "artifact checker test freeze differs",
    )
    require(
        data["failure_and_retention"]["any_failure"]
        == "INVALID-NO-SCIENTIFIC-RESULT"
        and data["failure_and_retention"]["partial_scientific_classification"]
        is False
        and data["failure_and_retention"]["partial_artifact_publication"]
        is False
        and data["failure_and_retention"]["automatic_retry"] is False,
        "failure semantics differ",
    )
    limits = data["interpretation_limits"]
    require(
        len(limits) == 6
        and any("not a residual, error, convergence tolerance" in row
                for row in limits)
        and any("No result authorizes Stage 4, Stage 5" in row
                for row in limits)
        and any("No mismatch may be repaired" in row for row in limits),
        "interpretation limits differ",
    )
    require(
        set(data["next_step_by_class"])
        == {
            "INVALID",
            "VALID-GMRES-UPDATE-ACTIVE",
            "VALID-GMRES-UPDATE-INACTIVE",
        },
        "next-step classification census differs",
    )

    if verify_files:
        for relative, digest in EXPECTED_DEPENDENCIES.items():
            path = ROOT / relative
            require_regular(path, relative)
            require(sha256(path) == digest, f"dependency hash differs: {relative}")
        for relative, digest in EXPECTED_INPUTS.items():
            path = ROOT / relative
            require_regular(path, relative)
            require(sha256(path) == digest, f"input hash differs: {relative}")
        verify_implementation_manifest()

        method = json.loads(
            (ITER / "gmres_activity_protocol.json").read_text(encoding="utf-8")
        )
        require(
            method["bounded_production_run"]["processes"]
            == [
                {
                    "mode": "OFF",
                    "MOCA": "ABSENT",
                    "GMRA": "ABSENT",
                    "repetitions": 1,
                },
                {
                    "mode": "ON",
                    "MOCA": 2,
                    "GMRA": "PRESENT",
                    "repetitions": 2,
                },
            ]
            and method["bounded_production_run"][
                "wall_timeout_seconds_per_process"
            ]
            == 30
            and method["classification"]["threshold"] is None,
            "run protocol does not inherit the frozen method protocol",
        )
        commit = subprocess.run(
            ["git", "cat-file", "-e", f"{SOURCE_IMPLEMENTATION_COMMIT}^{{commit}}"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        require(commit.returncode == 0,
                "source implementation commit is unavailable")
        ancestor = subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                SOURCE_IMPLEMENTATION_COMMIT,
                "HEAD",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        require(ancestor.returncode == 0,
                "source implementation commit is not an ancestor of HEAD")
        require(
            subprocess.run(
                [
                    "git",
                    "diff",
                    "--quiet",
                    "4d7abb23ac7975d4146beaa3b0049e36cdad8776",
                    "--",
                    "src",
                ],
                cwd=ROOT,
                check=False,
            ).returncode
            == 0,
            "tracked live src differs from the frozen parent",
        )


def self_test(data: dict[str, Any]) -> None:
    mutations = []

    def mutate_status(item: dict[str, Any]) -> None:
        item["protocol_freeze_authorizes_execution"] = True

    mutations.append(mutate_status)

    def mutate_operator(item: dict[str, Any]) -> None:
        item["scope"]["instrumentation_added_operator_applications"] = 1

    mutations.append(mutate_operator)

    def mutate_matrix(item: dict[str, Any]) -> None:
        item["run_matrix"][2]["repetitions"] = 2

    mutations.append(mutate_matrix)

    def mutate_invocation(item: dict[str, Any]) -> None:
        item["process_execution"]["shell"] = True

    mutations.append(mutate_invocation)

    def mutate_timeout(item: dict[str, Any]) -> None:
        item["execution_budget"]["wall_timeout_seconds_per_process"] = 31

    mutations.append(mutate_timeout)

    def mutate_threshold(item: dict[str, Any]) -> None:
        item["classification"]["threshold"] = 1

    mutations.append(mutate_threshold)

    def mutate_payload(item: dict[str, Any]) -> None:
        item["artifact"]["required_payload"].pop()

    mutations.append(mutate_payload)

    def mutate_trusted_row(item: dict[str, Any]) -> None:
        item["independence"]["forbidden_trusted_derived_rows"].remove("MAX-K")

    mutations.append(mutate_trusted_row)

    for index, mutation in enumerate(mutations, start=1):
        changed = copy.deepcopy(data)
        mutation(changed)
        try:
            validate_payload(changed, verify_files=False)
        except ContractError:
            continue
        raise ContractError(f"self-test mutation {index} was accepted")


def main() -> None:
    allowed = {"--freeze-audit", "--self-test"}
    require(len(sys.argv) <= 2, "too many arguments")
    option = sys.argv[1] if len(sys.argv) == 2 else ""
    require(option in allowed | {""}, "unknown argument")
    data = read_protocol()
    validate_payload(data, verify_files=True)
    if option == "--self-test":
        self_test(data)
        mode = "SELF-TEST"
    elif option == "--freeze-audit":
        mode = "FREEZE"
    else:
        mode = "STATIC"
    print(
        "GMRES-ACTIVITY-RUN-PROTOCOL PASS "
        f"sha256={EXPECTED_PROTOCOL_SHA256} mode={mode}"
    )


if __name__ == "__main__":
    try:
        main()
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"GMRES-ACTIVITY-RUN-PROTOCOL FAIL: {exc}") from exc

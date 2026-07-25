#!/usr/bin/env python3
"""Fail-closed checker for the frozen passive GMRES activity protocol."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
PROTOCOL = ITERATIVE / "gmres_activity_protocol.json"
EXPECTED_PROTOCOL_SHA256 = (
    "7fedbdf3fd5ae26a709dc1785d9d2bebf4648599d4aa1ccd999c6fbc93c9cac1"
)
FROZEN_PARENT = "4d7abb23ac7975d4146beaa3b0049e36cdad8776"
ARTIFACT_ROOT = ROOT / "validation" / "artifacts" / "raw-moc-capture"

TOP_LEVEL_KEYS = [
    "name",
    "version",
    "status",
    "frozen_parent_commit",
    "purpose",
    "scientific_scope",
    "parent_evidence",
    "activation",
    "locked_production_input",
    "locked_solver_path",
    "counter_semantics",
    "audit_record_contract",
    "implementation_strategy",
    "required_implementation_properties",
    "required_no_transport_tests",
    "bounded_production_run",
    "future_publication_requirements",
    "required_production_checks",
    "classification",
    "interpretation_limits",
    "next_decision",
]

EXPECTED_SOURCE_HASHES = {
    "src/.dragon_deps.mk": (
        "5d837ab375527373e6d40cae413b83672661fb458ebe7670c42bb0819e784ae3"
    ),
    "src/FLUGPI.f": (
        "0155090fc67f38184c4602b0d330cf241a0eeba7f82c203fc25529267b5401ac"
    ),
    "src/FLU.f": (
        "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0"
    ),
    "src/FLUDRV.f": (
        "6bfd74d6cb473619bcf6130fc723502d348b6a3e76da86e5d03934207b3e4934"
    ),
    "src/MCGMRE.f": (
        "61f71a4873a744608d429eaccc61807d76b5b50a3d2c10213734bb5b26bf1379"
    ),
    "src/SPOMOC.f90": (
        "23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc"
    ),
}

EXPECTED_LOCKED_FILES = {
    "PRE": (
        "validation/artifacts/raw-moc-capture/stationary/pre.xsm",
        "6e297fe92b03609ddbac84128623a14ac8638d5d86147ca6a8ee1298f71f3b3e",
    ),
    "LEGACY_OFF_XSM": (
        "validation/artifacts/raw-moc-capture/stationary/off.xsm",
        "c27ec11a833e0435dce5390e1c1ffbe81c931c21108d036b5af5fbd10a4f3789",
    ),
    "LEGACY_ON_XSM": (
        "validation/artifacts/raw-moc-capture/stationary/on.xsm",
        "de27778fb23f035aafab0e6ca877faf0f64a0662d255fa485b8174fea81f87ae",
    ),
    "LEGACY_OFF_LOG": (
        "validation/artifacts/raw-moc-capture/stationary_off/probe.log",
        "b15a3c9e0ad3bdc54ed3e50bba9e9cbb22a885bb68f712fb83ea02ef1e109234",
    ),
    "LEGACY_ON_LOG": (
        "validation/artifacts/raw-moc-capture/stationary_on/probe.log",
        "03f802bea77875419e126ec51282924b2717bed7b987c8171febc2738a2bfe25",
    ),
    "MACRO0": (
        "validation/artifacts/raw-moc-capture/common/restart_macro0.xsm",
        "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
    ),
    "SOURCE": (
        "validation/artifacts/raw-moc-capture/common/restart_source.xsm",
        "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
    ),
    "SYSTEM": (
        "validation/artifacts/raw-moc-capture/common/restart_system.xsm",
        "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
    ),
    "TRACK": (
        "validation/artifacts/raw-moc-capture/common/restart_track.xsm",
        "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
    ),
    "TRACK_BINARY": (
        "validation/artifacts/raw-moc-capture/common/initial_radial_track.bin",
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    ),
}

EXPECTED_STATE_FIELDS = [
    "schema-version",
    "status",
    "MOCA-arm",
    "plane",
    "NGRP",
    "NUN",
    "NGEFF",
    "KRYL",
    "MCGMRE-entry-count",
    "MCGMRE-exit-count",
    "primary-call-count",
    "affine-RHS-call-count",
    "Krylov-call-count",
    "primary-active-group-sum",
    "affine-RHS-active-group-sum",
    "Krylov-active-group-sum",
    "correction-block-count",
    "nonzero-K-group-block-count",
    "sum-K",
    "max-K",
    "MCGMRE-MAXI",
    "MCGMRE-ERRTOL-binary32-bits",
    "operator-applications-added",
    "reserved-zero",
]


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY-PROTOCOL FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require_regular(path: Path, owner: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid {owner}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def require_keys(mapping: dict[str, Any], keys: list[str], owner: str) -> None:
    require(list(mapping) == keys, f"{owner} key order or census differs")


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"git {' '.join(arguments)} failed: {detail}")
    return result


def require_safe_relative(path_text: str, owner: str) -> Path:
    relative = Path(path_text)
    require(
        not relative.is_absolute()
        and ".." not in relative.parts
        and relative.as_posix() == path_text,
        f"unsafe {owner} path",
    )
    return ROOT / relative


def verify_protocol_bytes() -> dict[str, Any]:
    require_regular(PROTOCOL, "protocol")
    raw = PROTOCOL.read_bytes()
    require(
        sha256_bytes(raw) == EXPECTED_PROTOCOL_SHA256,
        "frozen protocol bytes changed",
    )
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        fail("protocol is not ASCII")
    try:
        protocol = json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    canonical = json.dumps(protocol, ensure_ascii=True, indent=2) + "\n"
    require(text == canonical, "protocol is not canonical indented JSON")
    require_keys(protocol, TOP_LEVEL_KEYS, "top-level protocol")
    return protocol


def verify_parent_sources(protocol: dict[str, Any], freeze_audit: bool) -> None:
    parent = protocol["frozen_parent_commit"]
    require(parent == FROZEN_PARENT, "frozen parent identity differs")
    git("cat-file", "-e", f"{parent}^{{commit}}")
    ancestor = git("merge-base", "--is-ancestor", parent, "HEAD", check=False)
    require(ancestor.returncode == 0, "frozen parent is not an ancestor of HEAD")

    declared = protocol["parent_evidence"]["legacy_source_hashes_at_frozen_parent"]
    require(declared == EXPECTED_SOURCE_HASHES, "declared source hashes differ")
    for relative, expected in EXPECTED_SOURCE_HASHES.items():
        blob = git("show", f"{parent}:{relative}").stdout
        require(
            sha256_bytes(blob) == expected,
            f"frozen parent blob hash differs: {relative}",
        )
        live = ROOT / relative
        require_regular(live, relative)
        require(sha256_file(live) == expected, f"live source differs: {relative}")

    if not freeze_audit:
        return
    source_diff = git("diff", "--quiet", parent, "--", "src", check=False)
    require(source_diff.returncode == 0, "tracked src differs from frozen parent")
    source_status = git(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        "src",
    ).stdout
    require(source_status == b"", "live src contains an untracked or dirty path")
    forbidden = git(
        "grep",
        "-n",
        "-E",
        r"GMRA|SPOT-GMR-AUD",
        "--",
        "src",
        check=False,
    )
    require(
        forbidden.returncode == 1 and forbidden.stdout == b"",
        "GMRES activity implementation is present in live src",
    )


def verify_parent_evidence(protocol: dict[str, Any]) -> None:
    evidence = protocol["parent_evidence"]
    require_keys(
        evidence,
        [
            "raw_moc_ulp_bridge_result_receipt",
            "raw_moc_capture_result_receipt",
            "raw_moc_capture_artifact_manifest_sha256",
            "legacy_source_hashes_at_frozen_parent",
            "facts_not_available_from_parent_evidence",
        ],
        "parent evidence",
    )
    receipts = {
        "raw_moc_ulp_bridge_result_receipt": (
            "validation/iterative/raw_moc_ulp_bridge_result_receipt.sha256",
            "20dc353133c6251021fb87f0196061fb0b1be969d8e73890b7a9b1b073e60935",
        ),
        "raw_moc_capture_result_receipt": (
            "validation/iterative/raw_moc_capture_result_receipt.sha256",
            "485baab029387aeb8212647768be96b6eba438119e7d6ddcf013ccaf5e3359b5",
        ),
    }
    for key, (relative, expected) in receipts.items():
        record = evidence[key]
        require(
            record == {"path": relative, "sha256": expected},
            f"{key} declaration differs",
        )
        path = require_safe_relative(relative, key)
        require_regular(path, key)
        require(sha256_file(path) == expected, f"{key} bytes differ")

    manifest_sha = (
        "1c2c6bbae0a81a3978b09bc158ac0ca7a408c7d6495e734fea2f8e44f48b48a4"
    )
    require(
        evidence["raw_moc_capture_artifact_manifest_sha256"] == manifest_sha,
        "parent artifact manifest identity differs",
    )
    require(
        evidence["facts_not_available_from_parent_evidence"]
        == [
            "number of MCGMRE correction blocks",
            "number of groups with KMAX greater than zero",
            "sum or histogram of KMAX",
            "number of affine-RHS and Krylov MCGFL1 calls",
        ],
        "parent-evidence uncertainty changed",
    )

    files = protocol["locked_production_input"]["files"]
    require(list(files) == list(EXPECTED_LOCKED_FILES), "locked file census differs")
    for name, (relative, expected) in EXPECTED_LOCKED_FILES.items():
        require(
            files[name] == {"path": relative, "sha256": expected},
            f"locked file declaration differs: {name}",
        )

    if not ARTIFACT_ROOT.exists():
        return
    require(
        ARTIFACT_ROOT.is_dir() and not ARTIFACT_ROOT.is_symlink(),
        "invalid parent artifact root",
    )
    manifest = ARTIFACT_ROOT / "artifact_manifest.sha256"
    require_regular(manifest, "parent artifact manifest")
    require(
        sha256_file(manifest) == manifest_sha,
        "parent artifact manifest bytes differ",
    )
    for name, (relative, expected) in EXPECTED_LOCKED_FILES.items():
        path = require_safe_relative(relative, name)
        require_regular(path, f"locked artifact {name}")
        require(sha256_file(path) == expected, f"locked artifact differs: {name}")


def verify_scope_and_activation(protocol: dict[str, Any]) -> None:
    require(
        protocol["name"] == "SPOT bounded GMRES correction-activity census"
        and protocol["version"] == 1
        and protocol["status"] == "FROZEN-BEFORE-IMPLEMENTATION",
        "protocol identity differs",
    )
    require(
        protocol["purpose"]
        == [
            (
                "Determine whether the frozen one-map production path actually "
                "reaches any nonzero-K MCGMRE correction update before defining "
                "a precision A/B at that update."
            ),
            (
                "Count the existing primary, affine-RHS and Krylov operator "
                "roles and record every per-group KMAX vector without changing "
                "any floating-point arithmetic."
            ),
            (
                "Use an exact structural result, not a numerical threshold, to "
                "choose the next smallest precision experiment."
            ),
        ],
        "purpose differs",
    )
    scope = protocol["scientific_scope"]
    require(
        scope["kind"] == "PASSIVE-CONTROL-FLOW-CENSUS"
        and scope["production_routine"] == "MCGMRE",
        "scientific scope differs",
    )
    for field in (
        "floating_point_values_added_to_solver",
        "floating_point_operations_added_to_solver",
        "operator_applications_added",
        "model_terms_added",
        "numeric_parameters_added",
    ):
        require(scope[field] == 0, f"{field} is not zero")
    for field in (
        "solver_state_feedback",
        "physical_equation_change",
        "precision_change",
    ):
        require(scope[field] is False, f"{field} is not false")
    require(
        len(scope["observed_control_points"]) == 4
        and "block-entry active-group mask"
        in scope["observed_control_points"][2],
        "observed control points differ",
    )

    activation = protocol["activation"]
    require(
        activation
        == {
            "new_keyword": "GMRA",
            "syntax": "standalone GMRA keyword in FLU input",
            "default": "OFF",
            "numeric_argument": None,
            "duplicate_use": "FAIL-CLOSED",
            "required_existing_capture": "MOCA 2",
            "GMRA_without_MOCA_2": "FAIL-CLOSED",
            "invalid_or_unlocked_path": "FAIL-CLOSED",
            "same_executable_for_OFF_and_ON": True,
            "new_audit_directory": "SPOT-GMR-AUD",
            "existing_SPOT_MOC_AUD_contract": "UNCHANGED",
        },
        "activation contract differs",
    )


def verify_locked_solver(protocol: dict[str, Any]) -> None:
    production = protocol["locked_production_input"]
    require(
        production["choice"] == "STATIONARY PRE",
        "locked production choice differs",
    )
    solver = protocol["locked_solver_path"]
    require(
        solver
        == {
            "calculation_type": "S",
            "door": "MCCG",
            "plane": 1,
            "groups": 370,
            "regions": 8,
            "unknowns": 14,
            "FLU_controls": {
                "MAXOUT": 1,
                "MAXINR": 740,
                "EPSOUT": {
                    "decimal_input": "2.5E-7",
                    "binary32_bits": "348637BD",
                },
                "EPSUNK": {
                    "decimal_input": "2.5E-7",
                    "binary32_bits": "348637BD",
                },
                "EPSINR": {
                    "decimal_input": "2.5E-7",
                    "binary32_bits": "348637BD",
                },
                "IFRITR": 1,
                "IACITR": 0,
                "INITFL": 1,
                "LFORW": True,
                "ILEAK": 0,
                "rebalancing": True,
                "execution_path": "direct vector DOORFV",
            },
            "MCGMRE_controls": {
                "source": (
                    "frozen TRACK MCCG-STATE(13), MCCG-STATE(3) and "
                    "REAL-PARAM(1), also checked on the actual MCGMRE arguments"
                ),
                "MAXI": 20,
                "ERRTOL_EPSI": {
                    "decimal_input": "1.0E-5",
                    "stored_decimal": "9.99999974737875164E-6",
                    "binary32_bits": "3727C5AC",
                },
                "NSTART_KRYL": 10,
                "MAXIT_definition": "MAXI-1",
                "MAXIT": 19,
            },
            "MCCG_controls": {
                "KRYL": 10,
                "STIS": 1,
                "IAAC": 80,
                "ISCR": 0,
                "IDIFC": 0,
                "PACA": 4,
                "IDIR": 0,
            },
        },
        "locked solver path differs",
    )


def verify_counter_and_schema(protocol: dict[str, Any]) -> None:
    semantics = protocol["counter_semantics"]
    require(
        semantics["roles"]
        == {"1": "PRIMARY", "2": "AFFINE-RHS", "3": "KRYLOV"},
        "role map differs",
    )
    require(
        "370-group 0/1 NCONV mask" in semantics["role_event"]
        and semantics["role_block_index"]
        == (
            "PRIMARY uses 0; AFFINE-RHS and KRYLOV use the current "
            "correction-block index created at block entry"
        )
        and semantics["role_call_count"]
        == (
            "increment once immediately before the corresponding existing "
            "MCGFL1 call"
        )
        and semantics["role_active_group_count"]
        == "add COUNT(NCONV) at that same call site",
        "role counter semantics differ",
    )
    require(
        "after KMAX is reset"
        in semantics["block_entry_active_mask"]
        and "iteration limit" in semantics["inactive_group_rule"]
        and semantics["K_histogram"].startswith("eleven exact integer bins"),
        "block/KMAX semantics differ",
    )

    contract = protocol["audit_record_contract"]
    require(
        contract["owner"] == "fresh writable L_FLUX output"
        and contract["directory"] == "SPOT-GMR-AUD"
        and contract["initial_status"] == "INCOMPLETE"
        and contract["published_status"] == "COMPLETE"
        and contract["status_encoding"] == {"INCOMPLETE": 0, "COMPLETE": 1},
        "audit owner or status differs",
    )
    records = contract["records"]
    require(
        [record["name"] for record in records]
        == [
            "STATE-VECTOR",
            "NGIND",
            "CALL-META",
            "ROLE-CALLS",
            "ROLE-GROUPS",
            "ROLE-EVENTS",
            "ROLE-ACTIVE",
            "K-HISTOGRAM",
            "BLOCK-META",
            "BLOCK-ACTIVE",
            "BLOCK-KMAX",
        ],
        "record order or census differs",
    )
    require(
        records[0]
        == {
            "name": "STATE-VECTOR",
            "lcm_type": 1,
            "length": 24,
            "fields": EXPECTED_STATE_FIELDS,
        },
        "STATE-VECTOR schema differs",
    )
    require(
        records[1]["lcm_type"] == 1
        and records[1]["length"] == 370
        and "exactly 1..370" in records[1]["meaning"],
        "NGIND schema differs",
    )
    require(
        records[2]["lcm_type"] == 1
        and records[2]["length"] == "5 * MCGMRE-entry-count"
        and records[2]["row_fields"]
        == [
            "MCGMRE-call-index",
            "normal-exit-flag",
            "role-event-count",
            "correction-block-count",
            "last-global-ITER",
        ],
        "CALL-META schema differs",
    )
    for index, name in ((3, "ROLE-CALLS"), (4, "ROLE-GROUPS")):
        require(
            records[index]["name"] == name
            and records[index]["lcm_type"] == 1
            and records[index]["length"] == 3,
            f"{name} schema differs",
        )
    require(
        records[5]["lcm_type"] == 1
        and records[5]["length"] == "6 * total-role-call-count"
        and records[5]["row_fields"]
        == [
            "MCGMRE-call-index",
            "event-index-within-call",
            "role",
            "global-ITER-at-call",
            "correction-block-index-or-zero",
            "active-group-count",
        ],
        "ROLE-EVENTS schema differs",
    )
    require(
        records[6]["lcm_type"] == 1
        and records[6]["length"] == "370 * total-role-call-count"
        and "0/1 NCONV mask" in records[6]["meaning"],
        "ROLE-ACTIVE schema differs",
    )
    require(
        records[7]["lcm_type"] == 1
        and records[7]["length"] == 11
        and "KMAX=0..10" in records[7]["meaning"],
        "K-HISTOGRAM schema differs",
    )
    require(
        records[8]["lcm_type"] == 1
        and records[8]["length"] == "4 * correction-block-count"
        and records[8]["row_fields"]
        == [
            "MCGMRE-call-index",
            "block-index-within-call",
            "global-ITER-at-update",
            "block-entry-active-group-count",
        ],
        "BLOCK-META schema differs",
    )
    require(
        records[9]["lcm_type"] == 1
        and records[9]["length"] == "370 * correction-block-count"
        and "block-entry active mask" in records[9]["meaning"],
        "BLOCK-ACTIVE schema differs",
    )
    require(
        records[10]["lcm_type"] == 1
        and records[10]["length"] == "370 * correction-block-count"
        and "KMAX" in records[10]["meaning"],
        "BLOCK-KMAX schema differs",
    )
    require(
        "exactly one row with normal-exit-flag 1"
        in contract["zero_call_encoding"]
        and contract["zero_role_event_encoding"].startswith(
            "ROLE-EVENTS and ROLE-ACTIVE are both absent if and only if"
        )
        and contract["zero_block_encoding"].startswith(
            "BLOCK-META, BLOCK-ACTIVE and BLOCK-KMAX are all absent "
            "if and only if"
        )
        and "INCOMPLETE" in contract["write_policy"]
        and "COMPLETE as the last write" in contract["write_policy"]
        and "never read any audit value back into the solver"
        in contract["write_policy"],
        "zero-ledger or publication contract differs",
    )
    closure = contract["exact_closure"]
    require(len(closure) == 12, "exact-closure census differs")
    for token in (
        "370 ROLE-ACTIVE",
        "CALL-META independently closes",
        "contiguous from 1",
        "370 BLOCK-ACTIVE",
        "active-mask 0 implies KMAX 0",
        "exact count of active values",
        "never from 0 to 1",
        "Krylov ROLE-GROUPS equals sum-K",
        "block-entry active group",
        "K-HISTOGRAM sums",
        "max-K is exactly zero",
        "STATE-VECTOR fields 9..20",
    ):
        require(
            any(token in identity for identity in closure),
            f"missing exact closure: {token}",
        )


def verify_implementation_and_tests(protocol: dict[str, Any]) -> None:
    strategy = protocol["implementation_strategy"]
    require(
        strategy["tracked_production_src"] == "UNCHANGED"
        and strategy["instrumented_source_tree"]
        == (
            "a fresh clean Git archive of frozen_parent_commit plus one "
            "tracked validation-only overlay"
        ),
        "validation-only implementation boundary differs",
    )
    require(
        strategy["overlay_scope"]
        == [
            "add one independent GMRES integer-counter and Ganlib-sink module",
            (
                "add GMRA parsing and propagation without changing the "
                "existing MOCA semantics"
            ),
            (
                "insert read-only entry, role, block and exit counter calls "
                "around existing MCGMRE statements"
            ),
            (
                "add only the build dependency required by the new "
                "validation-only module"
            ),
        ],
        "overlay scope differs",
    )
    require(
        strategy["forbidden_overlay_changes"]
        == [
            "SPOMOC.f90 or the SPOT-MOC-AUD schema",
            (
                "any floating-point declaration, expression, assignment or "
                "comparison in the solver"
            ),
            (
                "any existing branch condition, iteration bound, stopping "
                "rule or operator call"
            ),
            (
                "any production XSM record outside SPOT-GMR-AUD"
            ),
        ],
        "forbidden overlay boundary differs",
    )
    require(
        strategy["required_freeze"]
        == [
            "clean parent archive SHA256",
            "overlay manifest and every overlay source SHA256",
            (
                "one implementation manifest covering this protocol checker, "
                "overlay, clean-archive builder, module state tests, fixture "
                "writer, Ganlib checker, log normalizer, preflight runner and "
                "contract checker"
            ),
            "compiler identity and complete flags",
            "instrumented executable SHA256 and symbol census",
        ],
        "implementation freeze requirements differ",
    )
    require(
        strategy["live_workspace_check"]
        == (
            "all tracked src files equal frozen_parent_commit before and "
            "after every build and run"
        ),
        "live-workspace protection differs",
    )

    properties = protocol["required_implementation_properties"]
    require(len(properties) == 8, "implementation-property census differs")
    for token in (
        "byte-for-byte unchanged",
        "default off",
        "original order",
        "integer counter updates",
        "read-only intent(in)",
        "block-entry mask",
        "normal",
        "No relaxation",
    ):
        require(
            any(token in property_text for property_text in properties),
            f"missing implementation property: {token}",
        )

    no_transport = protocol["required_no_transport_tests"]
    require(len(no_transport) == 10, "no-transport test census differs")
    for token in (
        "default-off",
        "fails closed",
        "zero-block",
        "histogram",
        "inactive group",
        "wrong-type",
        "block-major",
        "per-block per-group KMAX reconstruction",
        "byte identical",
        "LCM mutation",
    ):
        require(
            any(token in test for test in no_transport),
            f"missing no-transport test: {token}",
        )
    require(
        all("Dragon" not in test or "no Dragon" in test for test in no_transport),
        "a no-transport test authorizes Dragon",
    )


def verify_run_and_classification(protocol: dict[str, Any]) -> None:
    bounded = protocol["bounded_production_run"]
    require(
        bounded
        == {
            "authorization": "NOT-AUTHORIZED-BY-THIS-PROTOCOL-FREEZE",
            "required_before_execution": (
                "a separately committed and hash-frozen run, checking, "
                "atomic-publication and result-receipt protocol"
            ),
            "default": "PREFLIGHT-ONLY",
            "explicit_execution_gate": "RUN_GMRES_ACTIVITY=1",
            "execution_gate_values": {
                "absent": "PREFLIGHT-ONLY",
                "1": "RUN",
                "any_other": "FAIL-CLOSED",
            },
            "processes": [
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
            ],
            "FLU_outer_updates_per_process": 1,
            "wall_timeout_seconds_per_process": 30,
            "termination_scope": "exact spawned process group only",
            "valid_runtime_identity": {
                "outer_iterations": 1,
                "thermal_iterations": 1,
                "DOORFV_calls": 1,
                "MCCGF_calls": 1,
                "MCGMRE_entries": 1,
                "MCGMRE_normal_exits": 1,
                "second_MCGMRE_entry": "FAIL-CLOSED",
            },
            "ON_log_difference_whitelist": {
                "CPU_telemetry": "the already frozen normalization only",
                "deck_listing": (
                    "replace exactly one ' MOCA 2 GMRA ;' with "
                    "' MOCA 2 ;     ' on source line 0028, restoring the "
                    "five fixed-width CLE-2000 padding columns"
                ),
                "execution_echo": (
                    "replace exactly one ' MOCA 2 GMRA ;' with "
                    "' MOCA 2 ;     ' on echoed source line 0028, restoring "
                    "the five fixed-width CLE-2000 padding columns"
                ),
                "additional_lines": 0,
            },
            "long_trajectory": False,
            "rerun_six_step_arm": False,
            "precision_A_B_run": False,
        },
        "bounded production budget differs",
    )
    publication = protocol["future_publication_requirements"]
    require(len(publication) == 4, "future publication census differs")
    for token in (
        "remains unauthorized",
        "atomic rename",
        "symlinks",
        "final result receipt",
    ):
        require(
            any(token in requirement for requirement in publication),
            f"missing future publication requirement: {token}",
        )
    checks = protocol["required_production_checks"]
    require(len(checks) == 10, "production-check census differs")
    for token in (
        "immutable input hashes",
        "distinct regular byte-identical copy",
        "LEGACY_OFF_XSM byte for byte",
        "outside SPOT-GMR-AUD",
        "exactly one outer iteration",
        "reproduce one another exactly",
        "SPOT-MOC-AUD",
        "independently recomputes",
        "exact Krylov-to-KMAX",
        "zero added operator application",
    ):
        require(
            any(token in check for check in checks),
            f"missing production check: {token}",
        )

    classification = protocol["classification"]
    require(
        classification
        == {
            "threshold": None,
            "invalid": "INVALID",
            "valid_zero": "VALID-GMRES-UPDATE-INACTIVE",
            "valid_nonzero": "VALID-GMRES-UPDATE-ACTIVE",
            (
                "zero_definition"
            ): (
                "all contracts pass and nonzero-K-group-block-count equals "
                "exactly zero"
            ),
            (
                "nonzero_definition"
            ): (
                "all contracts pass and nonzero-K-group-block-count is an "
                "exact positive integer"
            ),
            "zero_is_a_valid_activity_result": True,
            "valid_classes_are_mutually_exclusive_and_exhaustive": True,
            "preference_or_improvement_ranking": False,
        },
        "classification differs",
    )
    require(
        all(value is False for value in protocol["interpretation_limits"].values()),
        "an interpretation prohibition was relaxed",
    )
    decision = protocol["next_decision"]
    require(
        decision["INVALID"].startswith("stop;")
        and "correction-accumulation precision A/B"
        in decision["VALID-GMRES-UPDATE-ACTIVE"]
        and "MCGFCS source-arithmetic precision A/B"
        in decision["VALID-GMRES-UPDATE-INACTIVE"]
        and decision["automatic_next_run"] is False
        and decision["long_trajectory_authorized"] is False,
        "next-decision map differs",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--freeze-audit",
        action="store_true",
        help="also require the complete live src tree to equal the frozen parent",
    )
    arguments = parser.parse_args()

    protocol = verify_protocol_bytes()
    verify_scope_and_activation(protocol)
    verify_parent_evidence(protocol)
    verify_parent_sources(protocol, arguments.freeze_audit)
    verify_locked_solver(protocol)
    verify_counter_and_schema(protocol)
    verify_implementation_and_tests(protocol)
    verify_run_and_classification(protocol)
    mode = "FREEZE" if arguments.freeze_audit else "STATIC"
    print(
        "GMRES-ACTIVITY-PROTOCOL PASS "
        f"sha256={EXPECTED_PROTOCOL_SHA256} mode={mode}"
    )


if __name__ == "__main__":
    main()

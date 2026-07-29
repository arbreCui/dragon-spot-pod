#!/usr/bin/env python3
"""Fail-closed public checker for the static-only REAL64 route freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROTOCOL = ROOT / "validation/iterative/radial_real64_route_protocol.json"
EXPECTED_PROTOCOL_CANONICAL_SHA256 = (
    "6b879ad421d8f1b29a92b2bb2e646fd58ff0ab8e4f7c71e5ea76bec8ca055ab0"
)


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_protocol_sha256(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def git_blob(root: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        result.returncode == 0,
        f"cannot read frozen git blob {commit}:{path}: "
        f"{result.stderr.decode(errors='replace').strip()}",
    )
    return result.stdout


def f32_bits(value: float) -> str:
    return "0x" + struct.pack(">f", value).hex()


def exact_keys(value: dict[str, Any], expected: set[str], name: str) -> None:
    require(isinstance(value, dict), f"{name} must be an object")
    actual = set(value)
    require(actual == expected, f"{name} keys: expected {sorted(expected)}, got {sorted(actual)}")


ROOT_KEYS = {
    "schema",
    "status",
    "decision",
    "scientific_scope",
    "baseline",
    "locked_case",
    "precision_contract",
    "inherited_aca_cutoff",
    "phase_A_static_closure",
    "phase_B_plane1_feasibility",
    "future_stage4",
    "forbidden_actions",
}

EVIDENCE_KEYS = {
    "validation/iterative/inner_sensitivity_result.md",
    "validation/iterative/inner_sensitivity_failure_receipt.sha256",
    "validation/iterative/radial_floor_result.md",
    "validation/iterative/radial_floor_result_receipt.sha256",
    "validation/iterative/raw_moc_capture_result.md",
    "validation/iterative/radial_precision_result.md",
    "validation/iterative/inner_sensitivity_v2_result.md",
    "validation/iterative/inner_sensitivity_v2_ra_geometry_result.md",
}

SOURCE_KEYS = {
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLU2DR.f",
    "src/DOORFV.f",
    "src/MCCGF.f",
    "src/MCGFLX.f",
    "src/MCGMRE.f",
    "src/MCGFL1.f",
    "src/MCGFCS.f",
    "src/MCGFCA.f",
    "src/MCGFCR.f",
    "src/MCGACA.f",
    "src/MCGABG.f",
    "src/MCGABGR.f",
    "src/MCGPRA.f",
    "src/MCGFCF.f",
    "src/MCGFFIR.f",
    "src/MCGSCA.f",
    "src/MCGFST.f",
    "src/MCGFMC.f",
    "src/FLUBAL.f",
    "src/FLU2AC.f",
    "src/SPOFSRC.f90",
    "Utilib/src/ALSBD.f",
}

EXPECTED_PATH_NODES = [
    "FLU/FLUDRV default-off dispatch and initialization",
    "FLU2DR eight-slice state, fixed/off-group source construction, state updates and terminal norms",
    "DOORFV gather/scatter boundary",
    "MCCGF locked branch",
    "MCGFLX iteration state and convergence quantities",
    "MCGMRE PHIIN/QFR/RHS/GAR, correction accumulation and convergence quantities",
    "MCGFL1 same-call source-to-response state",
    "MCGFCS source arithmetic",
    "MCGFCA and MCGFCR old-state/correction arithmetic",
    "MCGABG control-affecting norms and MCGPRA/MSRLUS1 correction path",
    "FLUBAL double rebalancing matrix solved by ALSBD",
    "FLU2AC flux update and acceleration scalar",
    "type-4 authoritative and one-time type-2 terminal archive adapter",
]

EXPECTED_REUSABLE = [
    "MCGFCF",
    "MCGFFIR",
    "MCGFST",
    "MCGPRA",
    "MSRLUS1",
    "ALSBD",
]

EXPECTED_ROUND_TRIPS = [
    "REAL(mutable_state)",
    "REAL(raw_or_corrected_response) assigned to mutable state",
    "type-2 LCM write followed by a type-2 read before terminal acceptance",
    "binary32 convergence norm or acceleration factor controlling the REAL64 lane",
    "diagnostic capture that downcasts a solver input",
]

EXPECTED_ALLOWED_ACTIONS = [
    "implement the default-off locked-branch overlay",
    "compile and link",
    "run static kind/interface checks",
    "run synthetic unit tests without Dragon or a transport sweep",
]

EXPECTED_STATIC_GATE = [
    "every required path node is represented in a machine-readable precision manifest",
    "no mutable-state binary32 round trip exists before terminal acceptance",
    "all cross-kind calls have explicit checked interfaces",
    "legacy OFF is the default and unsupported branches fail closed",
    "no physical term, solver control, iteration order or acceptance rule changes",
    "the inherited ACA cutoff is instrumented but unchanged",
    "the OFF-arm ordered non-timing scientific-log parser is frozen before any feasibility run",
    "tests prove malformed or incomplete manifests fail closed",
]

EXPECTED_CLASSIFICATION = {
    "OFF_identity_failure": "INVALID",
    "timeout_or_abnormal_exit": "INVALID-NO-SCIENTIFIC-RESULT",
    "nonfinite_nonpositive_or_physical_check_failure": "INVALID",
    "cutoff_active": "INCONCLUSIVE-INHERITED-CUTOFF",
    "REAL64_cap_without_strict_termination": "REAL64-NOT-SUFFICIENT",
    "strict_without_cutoff_before_replay": "PENDING-REPLAY",
    "replay_mismatch": "INVALID-NONREPRODUCIBLE",
    "strict_without_cutoff_and_exact_replay": "REAL64-RADIAL-FEASIBLE",
}

EXPECTED_PRECEDENCE = {
    "capture_first_match": [
        "OFF_identity_failure",
        "timeout_or_abnormal_exit",
        "nonfinite_nonpositive_or_physical_check_failure",
        "cutoff_active",
        "REAL64_cap_without_strict_termination",
        "strict_without_cutoff_before_replay",
    ],
    "replay_after_pending_first_match": [
        "OFF_identity_failure",
        "timeout_or_abnormal_exit",
        "nonfinite_nonpositive_or_physical_check_failure",
        "cutoff_active",
        "replay_mismatch",
        "strict_without_cutoff_and_exact_replay",
    ],
}

EXPECTED_FORBIDDEN_ACTIONS = [
    "Do not run Dragon under this static-only freeze.",
    "Do not construct A phi - q from ACA or PJJ records.",
    "Do not use a residual magnitude, ULP count, angle, beta, improvement factor or balance magnitude as a new acceptance threshold.",
    "Do not change MAXOUT, MAXINR, MCCG controls, ACCE, rebalancing, the inherited ACA cutoff, or the h/h2 tolerance pair.",
    "Do not introduce relaxation, damping, fitting, clipping, flux floors or model terms.",
    "Do not call a partial promotion a continuous REAL64 lane.",
    "Do not reuse the forensic cap restart as a Stage-4 map state.",
    "Do not run full Stage-4 or a Picard trajectory before separate qualification and authorization.",
]

EXPECTED_LOCAL_HASHES = {
    "validation/artifacts/iterative-radial-floor/restart_cap.xsm": "7291d8d88b5be07cd570131ea45ce5f283d55a37e3577197626001c59d9b8c89",
    "validation/artifacts/iterative-radial-floor/restart_system.xsm": "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
    "validation/artifacts/iterative-radial-floor/restart_track.xsm": "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
    "validation/artifacts/iterative-radial-floor/restart_source.xsm": "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
}


def load_protocol(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "protocol root must be an object")
    return data


def validate(
    data: dict[str, Any],
    root: Path = ROOT,
    *,
    require_local: bool = False,
) -> None:
    require(
        canonical_protocol_sha256(data) == EXPECTED_PROTOCOL_CANONICAL_SHA256,
        "canonical protocol hash",
    )
    exact_keys(data, ROOT_KEYS, "root")
    require(data["schema"] == "spot-radial-real64-route-v1", "schema")
    require(data["status"] == "FROZEN-STATIC-ONLY", "status")

    decision = data["decision"]
    exact_keys(
        decision,
        {
            "selected_route",
            "archived_independent_Aphi_minus_q",
            "matrix_free_same_kernel_residual",
            "reason",
            "final_method",
            "online_radial_feedback",
        },
        "decision",
    )
    require(
        decision["selected_route"] == "CONTINUOUS-REAL64-RADIAL-WORKING-LANE",
        "selected route",
    )
    require(
        decision["archived_independent_Aphi_minus_q"] == "NO-GO",
        "archived residual must remain NO-GO",
    )
    require(
        decision["matrix_free_same_kernel_residual"] == "DIAGNOSTIC-ONLY",
        "same-kernel residual boundary",
    )
    require(
        decision["final_method"] == "ONLINE-ITERATIVE-2D1D-SPOD",
        "final method",
    )
    require(decision["online_radial_feedback"] == "PRESERVED", "online feedback")

    scope = data["scientific_scope"]
    exact_keys(
        scope,
        {
            "physical_equations_changed",
            "cross_sections_changed",
            "geometry_or_tracking_changed",
            "source_terms_added",
            "rank_changed",
            "relaxation",
            "fitting",
            "clipping",
            "flux_floor",
            "new_empirical_parameters",
            "acceptance_thresholds_added",
        },
        "scientific_scope",
    )
    for key in (
        "physical_equations_changed",
        "cross_sections_changed",
        "geometry_or_tracking_changed",
        "rank_changed",
    ):
        require(scope[key] is False, f"{key} must be false")
    require(scope["source_terms_added"] == 0, "source terms")
    for key in (
        "relaxation",
        "fitting",
        "clipping",
        "flux_floor",
        "new_empirical_parameters",
        "acceptance_thresholds_added",
    ):
        require(scope[key] is None, f"{key} must be null")

    baseline = data["baseline"]
    exact_keys(
        baseline,
        {"commit", "evidence_sha256", "source_sha256_at_commit"},
        "baseline",
    )
    commit = baseline["commit"]
    require(commit == "94cb8b3a455d941a2d6bdcf0721daac289d1880a", "baseline commit")
    require(set(baseline["source_sha256_at_commit"]) == SOURCE_KEYS, "source hash keyset")
    require(set(baseline["evidence_sha256"]) == EVIDENCE_KEYS, "evidence hash keyset")
    for rel, expected in baseline["source_sha256_at_commit"].items():
        require(len(expected) == 64, f"source hash length: {rel}")
        actual = sha256_bytes(git_blob(root, commit, rel))
        require(actual == expected, f"frozen source hash mismatch: {rel}")
    for rel, expected in baseline["evidence_sha256"].items():
        require(len(expected) == 64, f"evidence hash length: {rel}")
        path = root / rel
        require(path.is_file(), f"missing evidence: {rel}")
        require(sha256_file(path) == expected, f"evidence hash mismatch: {rel}")

    case = data["locked_case"]
    exact_keys(
        case,
        {
            "calculation_type",
            "door",
            "IPHASE",
            "dimension",
            "cyclic",
            "vector_door",
            "initial_NGEFF",
            "active_group_contract",
            "mccg_active_subset_contract",
            "LBIHET",
            "LPRISM",
            "groups",
            "regions",
            "unknowns_per_group",
            "NANI",
            "NLIN",
            "NFUNL",
            "forward",
            "ILEAK",
            "IDIR",
            "LREBAL",
            "MAXOUT",
            "MAXINR",
            "solver_tolerance_h2_binary32_bits",
            "solver_tolerance_h2_decimal",
            "ACCE",
            "MCCG",
            "exponential_branch",
            "selected_transport_tuple",
            "selected_aca_tuple",
            "frozen_inactive_branches",
            "out_of_scope_branch",
        },
        "locked_case",
    )
    expected_case = {
        "calculation_type": "S",
        "door": "MCCG",
        "IPHASE": 1,
        "dimension": 2,
        "cyclic": False,
        "vector_door": True,
        "initial_NGEFF": 370,
        "LBIHET": False,
        "LPRISM": False,
        "groups": 370,
        "regions": 8,
        "unknowns_per_group": 14,
        "NANI": 1,
        "NLIN": 1,
        "NFUNL": 1,
        "forward": True,
        "ILEAK": 0,
        "IDIR": 0,
        "LREBAL": True,
        "MAXOUT": 500,
        "MAXINR": 740,
        "solver_tolerance_h2_binary32_bits": "0x348637bd",
        "ACCE": [3, 3],
        "out_of_scope_branch": "FAIL-CLOSED",
    }
    for key, expected in expected_case.items():
        require(case[key] == expected, f"locked case: {key}")
    require(
        case["active_group_contract"]
        == "On each direct-vector call NGIND is the ordered contiguous set IGDEB..370 and NGEFF=371-IGDEB; NGEFF may decrease from 370 as thermal groups terminate.",
        "active group contract",
    )
    require(
        case["mccg_active_subset_contract"]
        == "Within a gathered NGIND set, MCGMRE NCONV may be any ordered non-contiguous subset as individual groups meet the MCCG criterion; the REAL64 lane must preserve that mask.",
        "MCCG active subset contract",
    )
    require(
        f32_bits(float(case["solver_tolerance_h2_decimal"]))
        == case["solver_tolerance_h2_binary32_bits"],
        "h/2 bit identity",
    )
    require(
        case["MCCG"]
        == {
            "STIS": 1,
            "KRYL": 10,
            "IAAC": 80,
            "ISCR": 0,
            "IDIFC": 0,
            "PACA": 4,
        },
        "MCCG controls",
    )
    require(
        case["exponential_branch"]
        == {
            "LEXAC": False,
            "LEXF": False,
            "HDD_positive": False,
            "ISCH_before_STIS": 1,
            "ISCH": 11,
            "scheme": "NON CYCLIC - STIS 1 - SC SCHEME - TABULATED EXP",
        },
        "exponential branch",
    )
    require(
        case["selected_transport_tuple"]
        == ["MCGFCF", "MCGFFIR", "MCGSCA", "MCGFST"],
        "transport tuple",
    )
    require(
        case["selected_aca_tuple"]
        == ["MCGFCA", "MCGFCR", "MCGABG", "MCGPRA", "MSRLUS1"],
        "ACA tuple",
    )
    require(
        case["frozen_inactive_branches"]
        == {
            "MCGABGR_to_MCGACA": "inactive because MCGMRE calls MCGFL1 with LAST=false, so MACFLG and ACA group rebalancing remain false",
            "MCGFMC": "inactive because STIS=1 selects MCGFST instead of ordinary volume normalization",
            "MCGSCR": "inactive because ISCR=0",
        },
        "inactive branch census",
    )

    precision = data["precision_contract"]
    exact_keys(
        precision,
        {
            "mutable_iteration_state",
            "immutable_operator_inputs",
            "frozen_transport_kernel_mixed_precision",
            "authoritative_audit_output",
            "compatibility_output",
            "scope_name",
            "not_claimed",
            "required_path_nodes",
            "reusable_binary64_vector_kernels",
            "forbidden_round_trips",
            "implementation_form",
            "global_default_real_8_build",
        },
        "precision_contract",
    )
    require(
        precision["mutable_iteration_state"]
        == "IEEE-BINARY64-FROM-INITIAL-PROMOTION-THROUGH-TERMINAL-DECISION",
        "mutable precision",
    )
    require(
        precision["authoritative_audit_output"] == "GANLIB-LCM-TYPE-4",
        "authoritative output",
    )
    require(
        precision["required_path_nodes"] == EXPECTED_PATH_NODES,
        "precision path closure",
    )
    require(
        precision["reusable_binary64_vector_kernels"] == EXPECTED_REUSABLE,
        "reusable kernels",
    )
    require(precision["forbidden_round_trips"] == EXPECTED_ROUND_TRIPS, "round-trip prohibitions")
    require(
        "retains its archived storage kind" in precision["immutable_operator_inputs"],
        "operator input kind boundary",
    )
    require(
        "TAU=REAL(TAUD)" in precision["frozen_transport_kernel_mixed_precision"],
        "MCGSCA mixed-precision boundary",
    )
    require(precision["global_default_real_8_build"] is False, "global REAL*8")

    cutoff = data["inherited_aca_cutoff"]
    exact_keys(
        cutoff,
        {
            "locations",
            "source_literal",
            "binary32_bits",
            "change_or_tuning",
            "required_instrumentation",
            "acceptance_use",
            "if_cutoff_active_is_nonzero",
            "interpretation",
        },
        "inherited_aca_cutoff",
    )
    require(cutoff["locations"] == ["src/MCGABG.f"], "cutoff files")
    require(cutoff["source_literal"] == "1E-7", "cutoff literal")
    require(cutoff["binary32_bits"] == f32_bits(1.0e-7), "cutoff bits")
    require(cutoff["change_or_tuning"] == "FORBIDDEN", "cutoff tuning")
    require(cutoff["acceptance_use"] is None, "cutoff acceptance use")
    require(
        cutoff["if_cutoff_active_is_nonzero"]
        == "INCONCLUSIVE-INHERITED-CUTOFF",
        "cutoff classification",
    )
    for marker in ("EPSMAX=0", "cutoff_active", "lucky-breakdown/WI"):
        require(marker in cutoff["required_instrumentation"], f"cutoff instrumentation: {marker}")

    phase_a = data["phase_A_static_closure"]
    exact_keys(
        phase_a,
        {
            "authorized_now",
            "dragon_processes",
            "transport_operator_applications",
            "allowed_actions",
            "required_gate",
            "scientific_classification",
        },
        "phase A",
    )
    require(phase_a["authorized_now"] is True, "phase A authorization")
    require(phase_a["dragon_processes"] == 0, "phase A Dragon count")
    require(phase_a["transport_operator_applications"] == 0, "phase A transport")
    require(phase_a["allowed_actions"] == EXPECTED_ALLOWED_ACTIONS, "phase A allowed actions")
    require(phase_a["required_gate"] == EXPECTED_STATIC_GATE, "phase A required gate")
    require(phase_a["scientific_classification"] == "IMPLEMENTATION-ONLY", "phase A claim")

    phase_b = data["phase_B_plane1_feasibility"]
    exact_keys(
        phase_b,
        {
            "authorized_now",
            "requires_separate_authorization",
            "reason_for_plane",
            "common_restart",
            "legacy_OFF_identity_arm",
            "REAL64_ON_arm",
            "execution_budget",
            "classification",
            "classification_precedence",
            "interpretation",
        },
        "phase B",
    )
    require(phase_b["authorized_now"] is False, "phase B must not be authorized")
    require(phase_b["requires_separate_authorization"] is True, "phase B authorization gate")
    common = phase_b["common_restart"]
    exact_keys(
        common,
        {"role", "may_enter_stage4_map", "local_artifacts_sha256"},
        "phase B common restart",
    )
    require(common["may_enter_stage4_map"] is False, "forensic restart")
    require(
        common["local_artifacts_sha256"] == EXPECTED_LOCAL_HASHES,
        "local input hashes",
    )
    off = phase_b["legacy_OFF_identity_arm"]
    exact_keys(
        off,
        {
            "updates",
            "ACCE",
            "reference_flux_sha256",
            "reference_raw_log_sha256",
            "required_result",
        },
        "phase B OFF arm",
    )
    require(off["updates"] == 6, "OFF identity length")
    require(off["ACCE"] == [3, 3], "OFF ACCE")
    require(
        off["reference_flux_sha256"]
        == "663a8257b1ecafa2dde9c36d7cff8ccd8201a08fe2b117cdccad46c305e5bea9",
        "OFF reference flux hash",
    )
    require(
        off["reference_raw_log_sha256"]
        == "79d030285857269c368a6c0342cb8ea7d57d481ec1615d01d0f1b1d51d3b6beb",
        "OFF raw log provenance hash",
    )
    require(
        off["required_result"]
        == "bitwise-identical standard scientific output and exact equality of ordered non-timing scientific records under a parser frozen before the feasibility run; the raw reference-log hash is provenance, not the comparison rule",
        "OFF identity result",
    )
    on = phase_b["REAL64_ON_arm"]
    exact_keys(
        on,
        {"initial_state", "MAXOUT", "MAXINR", "normal_strict_early_termination", "required_result"},
        "phase B ON arm",
    )
    require(on["MAXOUT"] == 500, "ON MAXOUT")
    require(on["MAXINR"] == 740, "ON MAXINR")
    require(on["normal_strict_early_termination"] is True, "ON early termination")
    require(
        on["required_result"]
        == "strict existing FLU terminal gate before the unchanged iteration cap; finite positive scalar flux; passing existing source, layout and structural checks; finite nonnegative reported balance diagnostics without a magnitude gate; complete type-4 audit state; and cutoff_active=0",
        "ON required result",
    )
    budget = phase_b["execution_budget"]
    require(
        budget
        == {
            "future_capture_processes_after_separate_authorization": 1,
            "future_replay_processes_after_pending_result": 1,
            "automatic_replay": False,
            "wall_clock_limit_seconds_per_process": 120,
            "wall_clock_limit_is_scientific_threshold": False,
            "long_outer_trajectory_authorized": False,
        },
        "phase B execution budget",
    )
    classification = phase_b["classification"]
    require(classification == EXPECTED_CLASSIFICATION, "phase B classification")
    require(
        phase_b["classification_precedence"] == EXPECTED_PRECEDENCE,
        "phase B classification precedence",
    )
    for marker in (
        "pre-existing FLU stopping rule",
        "not an independently evaluated equation residual",
        "not",
        "conservation-accuracy proof",
    ):
        require(marker in phase_b["interpretation"], f"phase B interpretation: {marker}")

    if require_local:
        local = common["local_artifacts_sha256"]
        for rel, expected in local.items():
            path = root / rel
            require(path.is_file(), f"missing local feasibility input: {rel}")
            require(sha256_file(path) == expected, f"local input hash mismatch: {rel}")
        native = root / "validation/artifacts/iterative-radial-floor/native"
        require(
            sha256_file(native / "arm_flux.xsm")
            == off["reference_flux_sha256"],
            "local OFF flux reference",
        )
        require(
            sha256_file(native / "arm.log")
            == off["reference_raw_log_sha256"],
            "local OFF log reference",
        )

    future = data["future_stage4"]
    exact_keys(
        future,
        {
            "authorized_now",
            "requires_phase_B",
            "baseline_map",
            "refined_map",
            "mix_with_archived_binary32_G_h",
            "component_rule",
            "replay",
            "picard_authorization",
        },
        "future Stage 4",
    )
    require(future["authorized_now"] is False, "future Stage 4 authorization")
    require(future["requires_phase_B"] == "REAL64-RADIAL-FEASIBLE", "Stage 4 prerequisite")
    require(future["baseline_map"] == "G_h_REAL64(x0)", "Stage 4 baseline map")
    require(future["refined_map"] == "G_h2_REAL64(x0)", "Stage 4 refined map")
    require(future["mix_with_archived_binary32_G_h"] is False, "mixed-precision Stage 4")
    require(
        future["component_rule"]
        == "For each of R_rho, R_L, D_L and R_a independently: D_in < D_out_h when D_out_h > 0; if D_out_h is exactly zero, D_in must be exactly zero.",
        "component rule",
    )
    require(future["replay"] == "required", "Stage 4 replay")

    forbidden = data["forbidden_actions"]
    require(forbidden == EXPECTED_FORBIDDEN_ACTIONS, "forbidden actions")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--require-local", action="store_true")
    args = parser.parse_args()
    try:
        validate(load_protocol(args.protocol), ROOT, require_local=args.require_local)
    except (ContractError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"RADIAL-REAL64 ROUTE FAIL: {exc}", file=sys.stderr)
        return 1
    local = " WITH-LOCAL" if args.require_local else " PUBLIC"
    print(f"RADIAL-REAL64 ROUTE PASS:{local}; STATIC-ONLY; DRAGON-RUNS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fail-closed checker for the isolated REAL64 Phase-A2 raw façade."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "precision_manifest.json"
IMPLEMENTATION = HERE / "SPOR64_A2.f90"
RUNNER = HERE / "run_phase_a2.sh"
RECEIPT = HERE / "phase_a2_implementation_receipt.sha256"
EXPECTED_CANONICAL_SHA256 = (
    "fe27e6094224d98fdeec0a14c9200450fae2942ee6c4a77e8b96836bf74ae024"
)
BASELINE_COMMIT = "bbf531f7ce9ebb40e4c1dbf5c771b19e76307558"

EXPECTED_A1_HASH = (
    "13f341a99fa99c21ff34821339d0347565489134379193a1bfcf58dfa65726da"
)
EXPECTED_IMPLEMENTATION_HASH = (
    "9c0d209d29d99a910559e3b207d98ec466be751a8d7aa56e040fb382989579c2"
)
EXPECTED_TEST_HASH = (
    "8075157038d4e31ac0f4f951e374b5df1e07287504a4123f84e37e477fdf186b"
)
EXPECTED_REAL32_ACTUAL_HASH = (
    "9173e87d87ded91121d341a5e282b107b0fe21ee4cfecfd66de3c91816f990be"
)
EXPECTED_REAL32_CALLBACK_HASH = (
    "d353969f22b6f44330707eb14d1e15e5e323e4c6bc181da443607050a7028044"
)
EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/real64_phase_a1/SPOR64_A1.f90",
    "validation/iterative/real64_phase_a2/README.md",
    "validation/iterative/real64_phase_a2/SPOR64_A2.f90",
    "validation/iterative/real64_phase_a2/test_spor64_a2.f90",
    "validation/iterative/real64_phase_a2/compile_fail_real32_actual.f90",
    "validation/iterative/real64_phase_a2/compile_fail_real32_callback.f90",
    "validation/iterative/real64_phase_a2/precision_manifest.json",
    "validation/iterative/real64_phase_a2/check_phase_a2.py",
    "validation/iterative/real64_phase_a2/test_phase_a2_contract.py",
    "validation/iterative/real64_phase_a2/run_phase_a2.sh",
]

EXPECTED_LEGACY_HASHES = {
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGFCF.f":
        "60c841dbd2a0a2de2023de8a424b0162bc9898c5c5b877cc4d59f5b892b0deb9",
    "src/MCGFFIR.f":
        "b0400eb5211b5551f86f02608aa122e1301f38996c576dde818834da851cec6b",
    "src/MCGSCA.f":
        "fb16fe47c842d3a8c6e8726efb05195ce47ec88c6fdf6c00c65a91a3573a0159",
    "src/MCGFST.f":
        "bda4ec2376d91e5cf12427288c6bc1c565980cf916639937dca21ad7ad62b5e3",
    "src/Makefile":
        "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
}

EXPECTED_STATUS = {
    "classification": "IMPLEMENTED-PARTIAL-SOURCE-TO-RAW-FACADE-ONLY",
    "phase_a_static_closure": False,
    "source_arithmetic_closed": True,
    "typed_full_matrix_facade_closed": True,
    "actual_moc_response_implemented": False,
    "continuous_real64_lane": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "transport_execution_authorized": False,
    "dragon_processes_authorized": 0,
    "transport_solves": 0,
    "stage4_qualified": False,
    "stage5_authorized": False,
    "outer_convergence": "NOT-EVALUATED",
}

EXPECTED_BRANCH = {
    "NDIM": 2,
    "NANI": 1,
    "NLIN": 1,
    "NFUNL": 1,
    "STIS": 1,
    "CYCLIC": False,
    "LPRISM": False,
    "IDIR": 0,
    "radial_solver": "TYPE S + MCCG",
    "NGIND": "STRICTLY-CONSECUTIVE-TAIL-ENDING-AT-NG",
    "NCONV_true_meaning": "ACTIVE-NOT-CONVERGED",
    "active_subset": "NONEMPTY-ARBITRARY-NONCONTIGUOUS-MASK",
    "raw_response_point": "POST-MCGFST-PRE-MCGFCA",
}

EXPECTED_MATRIX_CONTRACT = {
    "callback_count": "EXACTLY-ONE-ON-A-VALID-NONEMPTY-ACTIVE-SET",
    "local_column_rule":
        "COLUMN-j-USES-LOCAL-j; NGIND(j)-IS-A-PHYSICAL-LABEL-ONLY",
    "source_before_callback":
        "ACTIVE-COLUMNS-REBUILT-BY-MCGFCS64_LOCKED",
    "inactive_source_on_success": "PRESERVE-CALLER-BIT-PATTERN",
    "active_raw_before_callback": "QUIET-NAN-SENTINEL",
    "inactive_raw_before_callback": "POSITIVE-ZERO",
    "active_raw_acceptance": "EVERY-ELEMENT-FINITE",
    "inactive_raw_acceptance": "EVERY-ELEMENT-EXACT-POSITIVE-ZERO",
    "raw_on_success":
        "ACTIVE-CALLBACK-VALUES-AND-INACTIVE-POSITIVE-ZERO",
    "failure_atomicity":
        "SOURCE-AND-RAW_RESPONSE-UNCHANGED-ON-ANY-FAILURE",
}

EXPECTED_REMAINING_PATH = [
    "checked adapter for the real post-STIS MCGFCF and MCGFST response",
    "tracking and KPSYS context without hidden global state",
    "MCGFCA, MCGFCR and live ACA correction",
    "MCGABG cutoff instrumentation",
    "MCGMRE PHIIN QFR RHS GAR and correction accumulation",
    "MCGFLX state and convergence quantities",
    "MCCGF active-group routing",
    "DOORFV gather and scatter",
    "FLU2DR eight-slice mutable state and terminal norms",
    "FLUBAL and ALSBD rebalancing",
    "FLU2AC update and acceleration scalar",
    "FLU and FLUDRV default-off route",
    "type-4 authoritative archive and terminal type-2 adapter",
]


class PhaseA2Error(RuntimeError):
    """Raised when the Phase-A2 boundary is altered or overclaimed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA2Error(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(encoded)


def git_blob(commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=ROOT,
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


def src_build_files() -> list[Path]:
    source_dir = ROOT / "src"
    patterns = ("*.c", "*.f", "*.F", "*.f90", "*.F90")
    return sorted(
        {path for pattern in patterns for path in source_dir.glob(pattern)}
    )


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseA2Error(f"cannot load manifest: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be an object")
    return data


def validate_scoped_receipt() -> None:
    require(RECEIPT.is_file(), "missing receipt")
    entries: dict[str, str] = {}
    for line in RECEIPT.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s].*)", line)
        require(match is not None, "malformed receipt line")
        digest, relative = match.groups()
        require(relative not in entries, f"duplicate receipt path: {relative}")
        entries[relative] = digest

    require(
        list(entries) == EXPECTED_RECEIPT_PATHS,
        "receipt scope or order mismatch",
    )
    for relative, expected in entries.items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"receipt file mismatch: {relative}",
        )


def validate_makefile_contract(makefile: str) -> None:
    target_pattern = re.compile(
        r"(?m)^spot-real64-phase-a2\s*:(?P<prerequisites>[^\n]*)\n"
        r"(?P<recipes>(?:\t[^\n]*(?:\n|$))*)"
    )
    matches = list(target_pattern.finditer(makefile))
    require(len(matches) == 1, "explicit top-level target")
    match = matches[0]
    require(
        match.group("prerequisites").strip() == "",
        "Phase-A2 target has prerequisites or an inline recipe",
    )
    require(
        match.group("recipes").splitlines()
        == ["\tsh validation/iterative/real64_phase_a2/run_phase_a2.sh"],
        "Phase-A2 target recipe is not exact and isolated",
    )
    require(
        len(
            re.findall(
                r"(?m)^\.PHONY:\s+spot-real64-phase-a2\s*$",
                makefile,
            )
        )
        == 1,
        "Phase-A2 phony declaration",
    )

    for target in ("all", "tests", "spot-fast"):
        dependency_match = re.search(
            rf"(?m)^{re.escape(target)}\s*:(.*)$",
            makefile,
        )
        require(
            dependency_match is not None,
            f"missing make target {target}",
        )
        require(
            "spot-real64-phase-a2" not in dependency_match.group(1),
            f"Phase-A2 added to {target}",
        )


def validate(data: dict[str, Any], *, verify_canonical: bool = True) -> None:
    if verify_canonical:
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )

    require(
        data["schema"]
        == "spot-radial-real64-phase-a2-post-stis-raw-facade-v1",
        "schema",
    )
    require(data["status"] == EXPECTED_STATUS, "status or authorization")

    baseline = data["baseline"]
    require(baseline["commit"] == BASELINE_COMMIT, "baseline commit")
    require(
        baseline["phase_a1_source"]
        == "validation/iterative/real64_phase_a1/SPOR64_A1.f90",
        "Phase-A1 source path",
    )
    require(
        baseline["phase_a1_source_sha256"] == EXPECTED_A1_HASH,
        "Phase-A1 manifest hash",
    )
    require(
        sha256_bytes(git_blob(BASELINE_COMMIT, baseline["phase_a1_source"]))
        == EXPECTED_A1_HASH,
        "baseline Phase-A1 source",
    )
    require(
        sha256_file(ROOT / baseline["phase_a1_source"]) == EXPECTED_A1_HASH,
        "live Phase-A1 source",
    )
    require(
        baseline["legacy_source_sha256"] == EXPECTED_LEGACY_HASHES,
        "legacy source hash map",
    )
    for relative, expected in EXPECTED_LEGACY_HASHES.items():
        require(
            sha256_bytes(git_blob(BASELINE_COMMIT, relative)) == expected,
            f"baseline legacy source mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live legacy source changed: {relative}",
        )

    implementation = data["implementation"]
    require(
        implementation == {
            "location":
                "validation/iterative/real64_phase_a2/SPOR64_A2.f90",
            "module": "SPOR64_A2",
            "procedures": [
                "MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED",
            ],
            "abstract_interfaces": [
                "SPOR64_POST_STIS_RAW_RESPONSE_IFACE",
            ],
            "sha256": EXPECTED_IMPLEMENTATION_HASH,
            "validation_tree_only": True,
            "included_by_src_wildcard_build": False,
            "scientific_use": "NONE",
        },
        "implementation contract",
    )
    require(
        sha256_file(IMPLEMENTATION) == EXPECTED_IMPLEMENTATION_HASH,
        "implementation file hash",
    )

    require(data["locked_branch"] == EXPECTED_BRANCH, "locked branch")
    require(
        data["kind_contract"] == {
            "mutable_binary64": ["QN", "FI", "SOURCE", "RAW_RESPONSE"],
            "immutable_binary32_operator_inputs": ["SC", "SIGAL"],
            "phase_a2_binary64_to_binary32_conversions": [],
            "binary32_mutable_actual_at_facade": "COMPILE-TIME-REJECTED",
            "binary32_callback_state": "COMPILE-TIME-REJECTED",
            "global_default_real_8": "FORBIDDEN",
        },
        "kind contract",
    )
    require(
        data["matrix_contract"] == EXPECTED_MATRIX_CONTRACT,
        "matrix contract",
    )
    require(
        data["response_semantics"] == {
            "future_real_operator":
                "MCGFCS64 -> MCGFCF(MCGFFIR -> MCGSCA) -> MCGFST",
            "excluded_after_boundary": [
                "MCGFCA",
                "MCGFCR",
                "MCGABG",
                "MCGPRA",
                "MSRLUS1",
            ],
            "synthetic_callback":
                "EXACT-SIGNED-PERMUTATION-TEST-OPERATOR",
            "synthetic_callback_is_physical_moc": False,
            "legacy_mcgfl1_return_is_raw_response": False,
        },
        "response semantics",
    )

    source = IMPLEMENTATION.read_text()
    lower = source.lower()
    require("module spor64_a2" in lower, "module definition")
    require("use spor64_a1" in lower, "Phase-A1 dependency")
    require(
        lower.count("call mcgfcs64_locked") == 1,
        "source-kernel call count",
    )
    require(
        lower.count("call primary_response") == 1,
        "primary callback count",
    )
    require(
        "procedure(spor64_post_stis_raw_response_iface) :: "
        "primary_response" in lower,
        "typed callback declaration",
    )
    require(
        re.search(
            r"real\(real64\),\s*intent\(in\)\s*::\s*qn\(:,:\),\s*fi\(:,:\)",
            lower,
        )
        is not None,
        "binary64 QN/FI",
    )
    require(
        re.search(
            r"real\(real64\),\s*intent\(inout\)\s*::\s*"
            r"source\(:,:\),\s*raw_response\(:,:\)",
            lower,
        )
        is not None,
        "binary64 source/raw",
    )
    require(
        re.search(
            r"real\(real32\),\s*intent\(in\)\s*::\s*"
            r"sc\(0:,:,:\),\s*sigal\(-6:,:\)",
            lower,
        )
        is not None,
        "binary32 immutable operator inputs",
    )
    require(
        re.search(r"real\s*\([^,\n]+,\s*real32\s*\)", lower) is None,
        "Phase-A2 downcast",
    )
    require("ieee_is_finite" in lower, "active finite completion check")
    require("ieee_quiet_nan" in lower, "active missing-write sentinel")
    require("all_positive_zero" in lower, "inactive exact-zero check")
    require("raw_response = 0.0_real64" in lower, "success raw reset")
    for name in ("mcgfcf", "mcgffir", "mcgsca", "mcgfst", "mcgfca"):
        require(
            re.search(rf"\bcall\s+{name}\b", lower) is None,
            f"real transport call present: {name}",
        )
    for token in ("lcmget", "lcmgpd", "iftrak", "kpsys",
                  "-fdefault-real-8", "relax", "aitken", "anderson"):
        require(token not in lower, f"forbidden implementation token: {token}")

    build_text = "\n".join(
        path.read_text(errors="replace") for path in src_build_files()
        if path.is_file()
    )
    require(
        re.search(
            r"(?i)\bcall\s+mcgfl1r64_post_stis_raw_facade_locked\b",
            build_text,
        )
        is None,
        "new façade connected to production",
    )
    require(
        re.search(r"(?i)\buse\s+spor64_a2\b", build_text) is None,
        "new module connected to production",
    )

    tests = data["synthetic_tests"]
    require(
        tests["source_sha256"] == EXPECTED_TEST_HASH,
        "test manifest hash",
    )
    require(
        sha256_file(ROOT / tests["source"]) == EXPECTED_TEST_HASH,
        "test source hash",
    )
    require(
        tests["real32_actual_compile_fail_sha256"]
        == EXPECTED_REAL32_ACTUAL_HASH,
        "REAL32 actual manifest hash",
    )
    require(
        sha256_file(ROOT / tests["real32_actual_compile_fail_source"])
        == EXPECTED_REAL32_ACTUAL_HASH,
        "REAL32 actual source hash",
    )
    require(
        tests["real32_callback_compile_fail_sha256"]
        == EXPECTED_REAL32_CALLBACK_HASH,
        "REAL32 callback manifest hash",
    )
    require(
        sha256_file(ROOT / tests["real32_callback_compile_fail_source"])
        == EXPECTED_REAL32_CALLBACK_HASH,
        "REAL32 callback source hash",
    )
    require(len(tests["required_checks"]) == 17, "required test count")
    require(tests["dragon_runs"] == 0, "test Dragon count")
    require(
        tests["fortran_compilation"] == "ISOLATED-EXPLICIT-SOURCE-LIST",
        "test compilation",
    )

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a2",
            "build target")
    for field in ("added_to_default_all", "added_to_tests",
                  "added_to_spot_fast"):
        require(build[field] is False, field)
    require(build["temporary_build_directory"] is True, "temporary build")
    require(build["forbidden_flag"] == "-fdefault-real-8", "forbidden flag")
    required_flags = [
        "-std=f2008",
        "-Werror",
        "-Wimplicit-interface",
        "-Wimplicit-procedure",
        "-Wconversion-extra",
        "-fimplicit-none",
        "-fcheck=all",
        "-ffp-contract=off",
        "-fno-fast-math",
    ]
    require(build["required_flags"] == required_flags, "required flags")

    validate_makefile_contract((ROOT / "Makefile").read_text())

    require(data["remaining_open_path"] == EXPECTED_REMAINING_PATH,
            "remaining path")
    require(
        data["next_step"]
        == "Implement a compile-only checked adapter for the frozen real "
           "MCGFCF-to-MCGFST post-STIS response without executing tracking "
           "or connecting production.",
        "next step",
    )
    require(
        data["interpretation"] == [
            "This slice proves the declared full-matrix active-mask "
            "orchestration and typed callback boundary under synthetic "
            "inputs.",
            "The signed-permutation callback is a test oracle and is not a "
            "transport model or MOC approximation.",
            "No real tracking file, MCGFCF, MCGFFIR, MCGSCA, MCGFST, ACA "
            "or transport solve is executed.",
            "It is not a continuous REAL64 radial lane or a "
            "solver-convergence, Stage-4, Picard or physical-accuracy "
            "result.",
            "No empirical coefficient, relaxation, clipping, fitted closure "
            "or new numerical threshold is introduced.",
        ],
        "interpretation",
    )

    require(RUNNER.is_file(), "missing runner")
    validate_scoped_receipt()
    runner = RUNNER.read_text()
    require("run_phase_a1.sh" in runner, "Phase-A1 prerequisite")
    require("phase_a2_implementation_receipt.sha256" in runner,
            "receipt invocation")
    require("-fdefault-real-8" not in runner, "runner default real promotion")
    for flag in required_flags:
        require(flag in runner, f"runner missing flag {flag}")
    require(
        re.search(r"(?i)(?:^|[ /])Dragon(?:\s|$)", runner) is None,
        "runner may invoke Dragon",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        validate(load_manifest(args.manifest))
    except PhaseA2Error as exc:
        raise SystemExit(f"SPOR64 PHASE-A2 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A2 CONTRACT PASS: POST-STIS-PRE-ACA-FACADE-ONLY; "
        "ACTUAL-MOC=NOT-IMPLEMENTED; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed checker for the isolated REAL64 Phase-A1 source slice."""

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
IMPLEMENTATION = HERE / "SPOR64_A1.f90"
RUNNER = HERE / "run_phase_a1.sh"
EXPECTED_CANONICAL_SHA256 = (
    "cb07fd86f77d77b554d0821d7ca310b356c6d3de67c6837a62a16ec7fe3621d6"
)
BASELINE_COMMIT = "feb6c6faa61c1cf87f2b39f4b7273a2840a69f52"

EXPECTED_LEGACY_HASHES = {
    "src/MCGFCS.f":
        "14661cff68e916e0fdc962320c434d5eb7aba247bce138a696cc809aaac78ec6",
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/Makefile":
        "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
}

EXPECTED_IMPLEMENTATION_HASH = (
    "13f341a99fa99c21ff34821339d0347565489134379193a1bfcf58dfa65726da"
)
EXPECTED_TEST_HASH = (
    "8f185cdce55da68a3b1bb9179cafd5db4ad14692a97db373d7bd35ee92997e39"
)
EXPECTED_COMPILE_FAIL_HASH = (
    "dbaeda4eeb8acf366084972e5d790790012fb0127c854f254dd7bee796c7ec95"
)

EXPECTED_STATUS = {
    "classification": "IMPLEMENTED-PARTIAL-SLICE-ONLY",
    "phase_a_static_closure": False,
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

EXPECTED_OPEN_PATH = [
    "FLU and FLUDRV default-off route",
    "FLU2DR eight-slice mutable state and terminal norms",
    "DOORFV gather and scatter",
    "MCCGF active-group routing",
    "MCGFLX state and convergence quantities",
    "MCGMRE PHIIN, QFR, RHS, GAR and correction accumulation",
    "MCGFL1 real64 caller and arbitrary NCONV subset",
    "primary MOC response interface",
    "MCGFCA, MCGFCR and live ACA correction",
    "MCGABG cutoff instrumentation",
    "FLUBAL and ALSBD rebalancing",
    "FLU2AC update and acceleration scalar",
    "type-4 authoritative archive and terminal type-2 adapter",
]


class PhaseA1Error(RuntimeError):
    """Raised when the partial slice is altered or overclaimed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA1Error(message)


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


def subroutine_body(source: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b(.*?)"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        source,
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(1)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseA1Error(f"cannot load manifest: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be an object")
    return data


def validate(data: dict[str, Any], *, verify_canonical: bool = True) -> None:
    if verify_canonical:
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )
    require(data["schema"] == "spot-radial-real64-phase-a1-source-slice-v1",
            "schema")
    require(data["status"] == EXPECTED_STATUS, "status or authorization")

    baseline = data["baseline"]
    require(baseline["commit"] == BASELINE_COMMIT, "baseline commit")
    require(
        baseline["route_protocol_sha256"]
        == "d89e7f13e61dfc994d14ca5c9b68439a9665022653b65520c8f566a659fdf472",
        "route protocol hash",
    )
    require(
        sha256_bytes(git_blob(BASELINE_COMMIT, baseline["route_protocol"]))
        == baseline["route_protocol_sha256"],
        "baseline route protocol content",
    )
    require(baseline["legacy_source_sha256"] == EXPECTED_LEGACY_HASHES,
            "legacy hash map")
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
    require(implementation["location"] == str(IMPLEMENTATION.relative_to(ROOT)),
            "implementation location")
    require(implementation["module"] == "SPOR64_A1", "module name")
    require(
        implementation["procedures"] == [
            "SPOR64_PROMOTE_MUTABLE",
            "MCGFCS64_LOCKED",
            "SPOR64_TERMINAL_COPY",
        ],
        "procedure list",
    )
    require(implementation["sha256"] == EXPECTED_IMPLEMENTATION_HASH,
            "implementation manifest hash")
    require(sha256_file(IMPLEMENTATION) == EXPECTED_IMPLEMENTATION_HASH,
            "implementation file hash")
    require(implementation["validation_tree_only"] is True, "tree isolation")
    require(
        implementation["included_by_src_wildcard_build"] is False,
        "src wildcard inclusion",
    )
    require(implementation["scientific_use"] == "NONE", "scientific use")

    branch = data["locked_branch"]
    require(
        (branch["NDIM"], branch["NANI"], branch["NLIN"],
         branch["NFUNL"], branch["STIS"]) == (2, 1, 1, 1, 1),
        "locked branch metadata",
    )
    require(
        branch["unsupported_metadata"]
        == "RETURN-NONZERO-WITHOUT-MUTATING-S",
        "unsupported branch behavior",
    )

    kinds = data["kind_contract"]
    require(kinds["mutable_entry_binary32"] == ["QN32", "FI32"],
            "entry kinds")
    require(kinds["mutable_working_binary64"] == ["QN", "FI", "S"],
            "working kinds")
    require(
        kinds["immutable_binary32_operator_inputs"] == ["SC", "SIGAL"],
        "operator input kinds",
    )
    require(kinds["preterminal_downcast"] == "FORBIDDEN",
            "preterminal downcast")
    require(
        kinds["binary32_mutable_actual_at_kernel"]
        == "COMPILE-TIME-REJECTED",
        "binary32 mutable actual",
    )
    require(kinds["global_default_real_8"] == "FORBIDDEN",
            "global kind flag")

    conversions = data["allowed_conversion_sites"]
    require(len(conversions) == 3, "conversion site count")
    require(
        conversions[0] == {
            "procedure": "SPOR64_PROMOTE_MUTABLE",
            "direction": "binary32-to-binary64",
            "expressions": [
                "real(qn32, real64)",
                "real(fi32, real64)",
            ],
        },
        "entry conversion sites",
    )
    require(
        conversions[1] == {
            "procedure": "MCGFCS64_LOCKED",
            "direction": "immutable-binary32-to-binary64",
            "expressions": [
                "real(sigal(ibm), real64)",
                "real(sc(ibm, 1), real64)",
            ],
        },
        "operator conversion sites",
    )
    require(
        conversions[2] == {
            "procedure": "SPOR64_TERMINAL_COPY",
            "direction": "terminal-binary64-to-binary32",
            "guard": "terminal_accepted",
            "expressions": ["real(state64, real32)"],
        },
        "terminal conversion site",
    )

    source = IMPLEMENTATION.read_text()
    lower = source.lower()
    require("module spor64_a1" in lower, "module definition")
    require(
        "use, intrinsic :: iso_fortran_env, only : real32, real64" in lower,
        "explicit kind import",
    )
    for token in data["forbidden_implementation_tokens"]:
        require(token.lower() not in lower, f"forbidden implementation token: {token}")
    require("-fdefault-real-8" not in lower, "global real promotion")

    promote = subroutine_body(source, "SPOR64_PROMOTE_MUTABLE").lower()
    kernel = subroutine_body(source, "MCGFCS64_LOCKED").lower()
    terminal = subroutine_body(source, "SPOR64_TERMINAL_COPY").lower()
    require(promote.count("real(qn32, real64)") == 1, "QN promotion count")
    require(promote.count("real(fi32, real64)") == 1, "FI promotion count")
    require("real32)" not in re.sub(r"real\(real32\)", "", promote),
            "entry downcast")
    require(kernel.count("real(sigal(ibm), real64)") == 1,
            "SIGAL promotion count")
    require(kernel.count("real(sc(ibm, 1), real64)") == 1,
            "SC promotion count")
    require("real(state64, real32)" not in kernel, "kernel downcast")
    require(terminal.count("real(state64, real32)") == 1,
            "terminal downcast count")
    require(
        re.search(
            r"if\s*\(\.not\.\s*terminal_accepted\)\s*return",
            terminal,
        )
        is not None,
        "terminal guard",
    )
    require(
        re.search(r"real\(real64\).*::\s*qn\(:\),\s*fi\(:\)", kernel)
        is not None,
        "kernel mutable input kind",
    )
    require(
        re.search(r"real\(real64\).*::\s*s\(:\)", kernel) is not None,
        "kernel mutable output kind",
    )
    require(
        re.search(
            r"real\(real32\).*::\s*sc\(0:,\s*:\),\s*sigal\(-6:\)",
            kernel,
        )
        is not None,
        "kernel immutable input kind",
    )

    require(
        data["legacy_route_identity"] == {
            "legacy_mcgfcs_direct_call_count": 1,
            "new_kernel_call_count_in_src": 0,
            "new_module_use_count_in_src": 0,
            "default_route": "LEGACY-REAL32",
            "new_route": "UNCONNECTED",
        },
        "legacy route identity",
    )

    build_text = "\n".join(
        path.read_text(errors="replace") for path in src_build_files()
        if path.is_file()
    )
    require(
        len(re.findall(r"(?i)\bcall\s+mcgfcs\s*\(", build_text)) == 1,
        "legacy direct call count",
    )
    require(
        re.search(r"(?i)\bcall\s+mcgfcs64_locked\b", build_text) is None,
        "new kernel connected to production",
    )
    require(
        re.search(r"(?i)\buse\s+spor64_a1\b", build_text) is None,
        "new module connected to production",
    )

    tests = data["synthetic_tests"]
    test_path = ROOT / tests["source"]
    bad_path = ROOT / tests["compile_fail_source"]
    require(tests["source_sha256"] == EXPECTED_TEST_HASH, "test manifest hash")
    require(sha256_file(test_path) == EXPECTED_TEST_HASH, "test source hash")
    require(
        tests["compile_fail_source_sha256"] == EXPECTED_COMPILE_FAIL_HASH,
        "compile-fail manifest hash",
    )
    require(sha256_file(bad_path) == EXPECTED_COMPILE_FAIL_HASH,
            "compile-fail source hash")
    require(len(tests["required_checks"]) == 14, "required test count")
    require(tests["dragon_runs"] == 0, "test Dragon count")

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a1",
            "build target")
    for field in ("added_to_default_all", "added_to_tests",
                  "added_to_spot_fast"):
        require(build[field] is False, f"{field}")
    require(build["temporary_build_directory"] is True, "temporary build")
    require(build["forbidden_flag"] == "-fdefault-real-8", "forbidden flag")
    require(
        build["required_flags"] == [
            "-std=f2008",
            "-Werror",
            "-Wimplicit-interface",
            "-Wimplicit-procedure",
            "-Wconversion-extra",
            "-fimplicit-none",
            "-fcheck=all",
            "-ffp-contract=off",
            "-fno-fast-math",
        ],
        "required build flags",
    )

    makefile = (ROOT / "Makefile").read_text()
    require(
        len(re.findall(r"(?m)^spot-real64-phase-a1\s*:", makefile)) == 1,
        "explicit top-level target",
    )
    require(
        "sh validation/iterative/real64_phase_a1/run_phase_a1.sh" in makefile,
        "target command",
    )
    for target in ("all", "tests", "spot-fast"):
        match = re.search(rf"(?m)^{re.escape(target)}\s*:(.*)$", makefile)
        require(match is not None, f"missing make target {target}")
        require("spot-real64-phase-a1" not in match.group(1),
                f"Phase-A1 added to {target}")

    require(data["remaining_open_path"] == EXPECTED_OPEN_PATH,
            "remaining path census")
    require(
        data["next_step"]
        == "Extend upward to an isolated MCGFL1 real64 caller and "
           "primary-response façade while keeping production routing "
           "disconnected.",
        "next step",
    )
    require(
        data["interpretation"] == [
            "This slice proves only the declared source arithmetic and "
            "conversion boundaries under synthetic inputs.",
            "It is not a continuous REAL64 radial lane.",
            "It is not a transport result, solver-convergence result, "
            "Stage-4 result or Picard result.",
            "No empirical coefficient, relaxation, clipping, fitted closure "
            "or new numerical threshold is introduced.",
        ],
        "interpretation boundary",
    )

    require(RUNNER.is_file(), "missing isolated runner")
    runner = RUNNER.read_text()
    require("-fdefault-real-8" not in runner, "runner global real promotion")
    for flag in build["required_flags"]:
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
    except PhaseA1Error as exc:
        raise SystemExit(f"SPOR64 PHASE-A1 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A1 CONTRACT PASS: PARTIAL-SLICE-ONLY; "
        "PRODUCTION-ROUTE=UNCONNECTED; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()

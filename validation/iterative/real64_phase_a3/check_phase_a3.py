#!/usr/bin/env python3
"""Fail-closed checker for the Phase-A3 compile-only legacy ABI seam."""

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
IMPLEMENTATION = HERE / "SPOR64_A3.f90"
RUNNER = HERE / "run_phase_a3.sh"
RECEIPT = HERE / "phase_a3_implementation_receipt.sha256"
EXPECTED_CANONICAL_SHA256 = (
    "e7ddb18ca6d22c182de0cb2e847ba94d6ace2dbda7d77454c28a348144211a7f"
)
EXPECTED_RUNNER_SHA256 = (
    "5293b22136a473a782fbd43d7c620607484575aba715fccee4fa0c864e499d41"
)
BASELINE_COMMIT = "ee780435800b2d5886fa388f930fdedd9737477d"

EXPECTED_A2_HASH = (
    "9c0d209d29d99a910559e3b207d98ec466be751a8d7aa56e040fb382989579c2"
)
EXPECTED_IMPLEMENTATION_HASH = (
    "3d8d9ebb2417f0c2139b88ecee157bcf16fa189e6f87e5dd6e76df8058f05ccc"
)
EXPECTED_ANCHOR_HASH = (
    "259ef9a38466d89410b624c018c74f45e2ead48c60afdd5b659a2de0eeee7702"
)
EXPECTED_NEGATIVE_HASHES = {
    "validation/iterative/real64_phase_a3/"
    "compile_fail_real32_mutable.f90":
        "e7a2c8ff22806c1f1813ad4ad1aac4976b5e3906a595f505f020172c89492cf9",
    "validation/iterative/real64_phase_a3/"
    "compile_fail_integer_kpsys.f90":
        "982069dd21640fd48056ea344df0eb26b2c58451c47aab0c34a67043eca31451",
    "validation/iterative/real64_phase_a3/"
    "compile_fail_flat_pjjind.f90":
        "7f65a32df1233e711786eaf97877b2a33a74abe2d100e207bc8a74879462cc0a",
    "validation/iterative/real64_phase_a3/"
    "compile_fail_real64_operator.f90":
        "bf0173f1878b5cff6e8b6a6d46f8e0fde14faec359f9f0d7048a68101f0b3ba4",
}
EXPECTED_LEGACY_HASHES = {
    "src/MCCGF.f":
        "621fba6d02d1b1efae2d6d6db8e61d1463a3a24bcf4d0efe3579bfba97c55546",
    "src/MCGFL1.f":
        "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGFCF.f":
        "60c841dbd2a0a2de2023de8a424b0162bc9898c5c5b877cc4d59f5b892b0deb9",
    "src/MCGFFIR.f":
        "b0400eb5211b5551f86f02608aa122e1301f38996c576dde818834da851cec6b",
    "src/MCGFFAR.f":
        "4bd72f5ec4c71d22e582afdb7f3d7e259e87b308d59c888a67ce88ec33916461",
    "src/MCGFFAL.f":
        "35f4e9e862e19cce47c0caa40dbe43168265c1170653875813bed0fcaaad7056",
    "src/MCGSCA.f":
        "fb16fe47c842d3a8c6e8726efb05195ce47ec88c6fdf6c00c65a91a3573a0159",
    "src/MCGFST.f":
        "bda4ec2376d91e5cf12427288c6bc1c565980cf916639937dca21ad7ad62b5e3",
    "src/MCGPJJ.f":
        "b695949d91921778a7fbe9e1a377057e87d821b8d2cd8027de9413ccfcc36de2",
    "src/Makefile":
        "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
}

EXPECTED_STATUS = {
    "classification": "IMPLEMENTED-COMPILE-ONLY-LEGACY-ABI-SEAM",
    "phase_a_static_closure": False,
    "source_arithmetic_closed": True,
    "synthetic_full_matrix_facade_closed": True,
    "real_operator_call_sequence_encoded": True,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "actual_moc_response_validated": False,
    "facade_callback_connected": False,
    "tracking_data_bound": False,
    "continuous_real64_lane": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "transport_solves": 0,
    "dragon_processes_authorized": 0,
    "stage4_qualified": False,
    "stage5_authorized": False,
    "outer_convergence": "NOT-EVALUATED",
}

EXPECTED_LOCKED_BRANCH = {
    "calculation_type": "S",
    "door": "MCCG",
    "ISCH": 11,
    "NDIM": 2,
    "K": 14,
    "KPN": 14,
    "NREG": 8,
    "NSOUT": 6,
    "groups": 370,
    "NANI": 1,
    "NLF": 1,
    "NFUNL": 1,
    "NMOD": 4,
    "NLFX": 1,
    "NLIN": 1,
    "NFUNLX": 1,
    "STIS": 1,
    "NPJJM": 1,
    "IDIR": 0,
    "CYCLIC": False,
    "LPRISM": False,
    "NGIND": "STRICTLY-CONSECUTIVE-TAIL-ENDING-AT-370",
    "NCONV_true_meaning": "ACTIVE-NOT-CONVERGED",
    "active_subset": "NONEMPTY-ARBITRARY-NONCONTIGUOUS-MASK",
}

EXPECTED_REMAINING_PATH = [
    "host-associated closure connecting the Phase-A2 callback to this "
    "Phase-A3 seam",
    "conforming XSI acquisition in a suffixed default-off route",
    "real tracking-unit positioning and identity checks",
    "real KPSYS PJJIND V NZON KEYFLX KEYCUR SIGAL context binding",
    "EXP1 tabulated-exponential initialization identity",
    "separately authorized removal of the compile-only link barrier",
    "actual MCGFCF-to-MCGFST execution and exact replay",
    "MCGFCA MCGFCR and live ACA correction",
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

EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/real64_phase_a2/SPOR64_A2.f90",
    *EXPECTED_LEGACY_HASHES.keys(),
    "validation/iterative/real64_phase_a3/README.md",
    "validation/iterative/real64_phase_a3/SPOR64_A3.f90",
    "validation/iterative/real64_phase_a3/compile_spor64_a3_anchor.f90",
    *EXPECTED_NEGATIVE_HASHES.keys(),
    "validation/iterative/real64_phase_a3/precision_manifest.json",
    "validation/iterative/real64_phase_a3/check_phase_a3.py",
    "validation/iterative/real64_phase_a3/test_phase_a3_contract.py",
    "validation/iterative/real64_phase_a3/run_phase_a3.sh",
]

REQUIRED_CHECKED_FLAGS = [
    "-std=f2008",
    "-Werror",
    "-Wimplicit-interface",
    "-Wimplicit-procedure",
    "-Wconversion-extra",
    "-Warray-temporaries",
    "-fimplicit-none",
    "-fcheck=all",
    "-ffp-contract=off",
    "-fno-fast-math",
]


class PhaseA3Error(RuntimeError):
    """Raised when the compile-only boundary is changed or overclaimed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA3Error(message)


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


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseA3Error(f"cannot load manifest: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be an object")
    return data


def src_build_files() -> list[Path]:
    source_dir = ROOT / "src"
    patterns = ("*.c", "*.f", "*.F", "*.f90", "*.F90")
    return sorted(
        {path for pattern in patterns for path in source_dir.glob(pattern)}
    )


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
    phase_a3_block = (
        ".PHONY: spot-real64-phase-a3\n"
        "spot-real64-phase-a3 :\n"
        "\tsh validation/iterative/real64_phase_a3/run_phase_a3.sh\n"
    )
    require(
        makefile.count(phase_a3_block) == 1,
        "exact isolated Phase-A3 Makefile block",
    )
    baseline_makefile = git_blob(BASELINE_COMMIT, "Makefile").decode()
    require(
        makefile.replace(phase_a3_block, "", 1) == baseline_makefile,
        "top-level Makefile changed beyond the isolated Phase-A3 block",
    )

    target_pattern = re.compile(
        r"(?m)^spot-real64-phase-a3\s*:(?P<prerequisites>[^\n]*)\n"
        r"(?P<recipes>(?:\t[^\n]*(?:\n|$))*)"
    )
    matches = list(target_pattern.finditer(makefile))
    require(len(matches) == 1, "explicit top-level Phase-A3 target")
    match = matches[0]
    require(
        match.group("prerequisites").strip() == "",
        "Phase-A3 target has prerequisites or an inline recipe",
    )
    require(
        match.group("recipes").splitlines()
        == ["\tsh validation/iterative/real64_phase_a3/run_phase_a3.sh"],
        "Phase-A3 target recipe is not exact and isolated",
    )
    phony_pattern = r"(?m)^\.PHONY:\s+spot-real64-phase-a3\s*$"
    require(
        len(re.findall(phony_pattern, makefile)) == 1,
        "Phase-A3 phony declaration",
    )

    without_target = (
        makefile[:match.start()] + makefile[match.end():]
    )
    without_a3 = re.sub(phony_pattern, "", without_target)
    require(
        "spot-real64-phase-a3" not in without_a3,
        "Phase-A3 appears elsewhere in Makefile",
    )

    ordinary_targets = re.findall(
        r"(?m)^([A-Za-z][A-Za-z0-9_.-]*)\s*:",
        makefile,
    )
    require(ordinary_targets and ordinary_targets[0] == "all",
            "default Make target changed")
    for target in ("all", "tests", "spot-fast"):
        dependency_match = re.search(
            rf"(?m)^{re.escape(target)}\s*:(.*)$",
            makefile,
        )
        require(dependency_match is not None, f"missing make target {target}")
        require(
            "spot-real64-phase-a3" not in dependency_match.group(1),
            f"Phase-A3 added to {target}",
        )


def validate_runner_contract(
    runner: str,
    *,
    verify_hash: bool = True,
) -> None:
    if verify_hash:
        require(
            sha256_bytes(runner.encode()) == EXPECTED_RUNNER_SHA256,
            "runner hash mismatch",
        )

    require("run_phase_a2.sh" in runner, "Phase-A2 prerequisite runner")
    require("phase_a3_implementation_receipt.sha256" in runner,
            "receipt invocation")
    for flag in REQUIRED_CHECKED_FLAGS:
        require(flag in runner, f"runner missing flag {flag}")
    require(runner.count('"$FC"') == 3, "Fortran command count")
    require(
        len(
            re.findall(
                r'(?m)^\s*(?:if\s+)?"\$FC"[^\n]*\s-c(?:\s|$)',
                runner,
            )
        )
        == 3,
        "a Fortran command is not compile-only",
    )
    for token in (" ld ", "\nld ", "\nar ", "ranlib", "make -c src",
                  "rdragon"):
        require(token not in runner.lower(), f"runner link token: {token}")

    logical_runner = re.sub(r"\\\n\s*", " ", runner)
    require(
        re.search(
            r'(?im)^\s*"\$BUILD_DIR/[^"]+"(?:\s|$)',
            logical_runner,
        )
        is None,
        "runner executes a build artifact",
    )
    require(
        re.search(
            r"(?im)^\s*(?:if\s+)?"
            r"(?:gfortran|ifort|ifx|flang|nvfortran|f90|f95)"
            r"(?:\s|$)",
            logical_runner,
        )
        is None,
        "runner contains an untracked compiler command",
    )
    require(
        re.search(
            r"(?i)(?:^|[/\"'])dragon(?:[\"'\s]|$)",
            logical_runner,
        )
        is None,
        "runner may invoke Dragon",
    )
    require(
        "spor64_a3_compile_only_link_forbidden" in runner.lower(),
        "runner does not require link barrier",
    )
    for symbol in ("mcgfcf", "mcgffir", "mcgffar", "mcgffal",
                   "mcgsca", "mcgfst"):
        require(symbol in runner.lower(), f"runner symbol check: {symbol}")
    for token in (
        "unexpected unresolved symbol",
        "unresolved_count",
        "runtime_symbol_count",
        'test "$unresolved_count" -ne 8',
        'test "$runtime_symbol_count" -ne 1',
    ):
        require(token in runner, f"runner exact unresolved set: {token}")


def validate(data: dict[str, Any], *, verify_canonical: bool = True) -> None:
    if verify_canonical:
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )

    require(
        data["schema"]
        == "spot-radial-real64-phase-a3-compile-only-legacy-abi-seam-v1",
        "schema",
    )
    require(data["status"] == EXPECTED_STATUS, "status or authorization")

    baseline = data["baseline"]
    require(baseline["commit"] == BASELINE_COMMIT, "baseline commit")
    require(
        baseline["phase_a2_source"]
        == "validation/iterative/real64_phase_a2/SPOR64_A2.f90",
        "Phase-A2 source path",
    )
    require(
        baseline["phase_a2_source_sha256"] == EXPECTED_A2_HASH,
        "Phase-A2 hash",
    )
    require(
        sha256_bytes(git_blob(BASELINE_COMMIT, baseline["phase_a2_source"]))
        == EXPECTED_A2_HASH,
        "baseline Phase-A2 source",
    )
    require(
        sha256_file(ROOT / baseline["phase_a2_source"]) == EXPECTED_A2_HASH,
        "live Phase-A2 source",
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

    require(
        data["implementation"] == {
            "location": "validation/iterative/real64_phase_a3/SPOR64_A3.f90",
            "module": "SPOR64_A3",
            "procedure": "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
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
    require(data["locked_branch"] == EXPECTED_LOCKED_BRANCH, "locked branch")

    abi = data["abi_contract"]
    require(
        abi["legacy_data_interfaces"] == "EXPLICIT-SHAPE-ABI-FAITHFUL",
        "legacy ABI",
    )
    require(
        abi["checked_facade_arrays"]
        == "CONTIGUOUS-ASSUMED-SHAPE-WITH-PREFLIGHT",
        "facade arrays",
    )
    require(
        abi["legacy_dummy_intent"]
        == "UNSPECIFIED-AS-IN-LEGACY-DEFINITIONS",
        "legacy dummy INTENT characteristics",
    )
    require(
        abi["forwarded_SUBSCH_interface"]
        == "IMPLICIT-EXTERNAL-AS-IN-LEGACY-DEFINITIONS",
        "forwarded SUBSCH characteristics",
    )
    require(
        abi["procedure_actuals"]
        == ["MCGFFIR", "MCGFFAR", "MCGFFAL", "MCGSCA"],
        "procedure actuals",
    )
    require(
        abi["executed_frozen_procedure_path"]
        == ["MCGFCF", "MCGFFIR", "MCGSCA", "MCGFST"],
        "frozen procedure path",
    )
    require(
        abi["inactive_but_required_procedure_actuals"]
        == ["MCGFFAR", "MCGFFAL"],
        "inactive procedure actuals",
    )
    require(
        abi["transport_call_sequence"] == ["MCGFCF", "MCGFST"],
        "transport call sequence",
    )
    require(
        abi["MCGFCF_call_count"] == 1
        and abi["MCGFST_call_count"] == 1,
        "transport call counts",
    )
    require(abi["source_kind"] == "REAL64-INTENT-IN", "source kind")
    require(
        abi["raw_response_kind"] == "REAL64-INTENT-INOUT",
        "response kind",
    )
    require(
        abi["frozen_real32_operator_inputs"]
        == ["CPO", "ZMU", "WZMU", "SIGAL", "VOLUME"],
        "operator kinds",
    )
    require(
        abi["KPSYS"] == "TYPE-C_PTR-RANK1-NO-VALUE-NO-BIND-C",
        "KPSYS ABI",
    )
    require(
        abi["PJJIND"] == "INTEGER-RANK2-NPJJM-BY-2",
        "PJJIND ABI",
    )
    require(
        abi["KEYFLX_to_MCGFST"]
        == "CONTIGUOUS-POINTER-RANK-REMAP-AFTER-NLIN-EQUALS-1",
        "KEYFLX remap",
    )
    require(
        abi["hidden_array_temporary"] == "COMPILE-TIME-FORBIDDEN",
        "array temporary",
    )
    require(
        abi["binary64_to_binary32_mutable_conversion"] == "NONE",
        "mutable downcast",
    )
    require(
        abi["global_default_real_8"] == "COMPILE-TIME-REJECTED",
        "default REAL promotion",
    )

    require(
        data["context_contract"] == {
            "adapter_performs_io": False,
            "adapter_reads_or_rewinds_tracking": False,
            "tracking_unit_positioned_by_future_caller": True,
            "real_tracking_context_bound": False,
            "real_KPSYS_PJJ_directories_bound": False,
            "EXP1_table_initialization_bound": False,
            "synthetic_or_stub_transport_context_allowed": False,
            "active_KPSYS_must_be_associated_before_transport": True,
            "failure_before_operator_calls": "STATUS-ONLY-NO-OUTPUT-MUTATION",
            "failure_during_legacy_operator": "NOT-CATCHABLE-NOT-EVALUATED",
        },
        "context contract",
    )
    require(
        data["legacy_xsi_conformance"] == {
            "legacy_expression": "XSIXYZ(1,IDIR)",
            "legacy_declared_second_dimension": "1:3",
            "locked_IDIR": 0,
            "legacy_actual_designator_standard_conforming": False,
            "MCGFFIR_reads_XSI_when_locked": False,
            "adapter_rule":
                "CALLER-OWNED-LEGAL-CONTIGUOUS-XSI-OF-LENGTH-NSOUT",
            "legacy_production_call_fixed": False,
            "runtime_safety_validated": False,
        },
        "legacy XSI conformance",
    )
    require(
        data["legacy_callback_interface_warning"] == {
            "MCCGF_MCGFFA_TEMPLATE_matches_MCGFFAR": False,
            "adapter_MCGFFAR_interface_source": "DIRECTLY-FROM-MCGFFAR-F",
            "frozen_isotropic_branch_executes_MCGFFAR": False,
            "legacy_template_fixed": False,
        },
        "legacy callback interface warning",
    )
    require(
        data["link_barrier"] == {
            "symbol": "SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN",
            "must_remain_undefined": True,
            "purpose":
                "PREVENT-ACCIDENTAL-LINK-OR-EXECUTION-BEFORE-A-NEW-GATE",
            "removal_authorized": False,
        },
        "link barrier",
    )

    source = IMPLEMENTATION.read_text()
    lower = source.lower()
    legacy_specification = lower.split("contains", 1)[0]
    require("module spor64_a3" in lower, "module definition")
    require(
        "integer, parameter :: kind_guard = 1 / merge(1, 0," in lower,
        "kind guard",
    )
    calls = re.findall(r"(?i)\bcall\s+([a-z][a-z0-9_]*)", source)
    require(
        [name.lower() for name in calls]
        == [
            "spor64_a3_compile_only_link_forbidden",
            "mcgfcf",
            "mcgfst",
        ],
        "implementation call sequence",
    )
    require(
        "external :: subffi, subffa, subldc, subsch" in lower,
        "ABI-faithful MCGFCF procedure dummies",
    )
    require(
        "intent(" not in legacy_specification,
        "legacy interfaces invent INTENT characteristics",
    )
    require(
        legacy_specification.count("external :: subsch") == 3,
        "forwarded SUBSCH must keep its legacy implicit interface",
    )
    require(
        "procedure(spor64_mcgsch_stis1_iface) :: subsch"
        not in legacy_specification,
        "forwarded SUBSCH was given a non-legacy explicit interface",
    )
    for declaration in (
        "procedure(spor64_mcgffi_stis1_iface) :: mcgffir",
        "procedure(spor64_mcgffa_stis1_iface) :: mcgffar",
        "procedure(spor64_mcgldc_iface) :: mcgffal",
        "procedure(spor64_mcgsch_stis1_iface) :: mcgsca",
    ):
        require(declaration in lower, f"procedure identity: {declaration}")
    require(
        "type(c_ptr), contiguous, intent(in) :: kpsys(:)" in lower,
        "checked C_PTR KPSYS",
    )
    require(
        "integer, contiguous, pointer :: keyflx_stis(:,:)" in lower,
        "KEYFLX remap pointer",
    )
    require(
        "keyflx_stis(1:nreg,1:nfunl) => keyflx" in lower,
        "KEYFLX remap statement",
    )
    require("keyflx(:,1,:)" not in lower, "hidden KEYFLX array section")
    require(
        re.search(
            r"real\(real64\),\s*contiguous,\s*intent\(in\)\s*::"
            r"\s*source\(:,:\),\s*xsi\(:\)",
            lower,
        )
        is not None,
        "REAL64 source and legal XSI storage",
    )
    require(
        re.search(
            r"real\(real64\),\s*contiguous,\s*intent\(inout\)\s*::"
            r"\s*raw_response\(:,:\)",
            lower,
        )
        is not None,
        "REAL64 raw response",
    )
    require("c_associated(kpsys(group))" in lower, "active KPSYS check")
    require(
        re.search(r"real\s*\([^,\n]+,\s*real32\s*\)", lower) is None,
        "binary64-to-binary32 conversion",
    )
    require(
        re.search(
            r"(?im)^\s*(?:read|rewind|open|close|write)\b",
            source,
        )
        is None,
        "I/O in compile-only adapter",
    )
    for token in (
        "lcmget",
        "lcmgpd",
        "c_f_pointer",
        "mcgfca",
        "mcgfcr",
        "mcgabg",
        "mcgpra",
        "msrlus1",
        "relax",
        "aitken",
        "anderson",
    ):
        require(token not in lower, f"forbidden implementation token: {token}")
    require(
        re.search(r"(?im)^\s*(?:save|common)\b", source) is None,
        "hidden mutable state",
    )

    mcgfl1 = (ROOT / "src/MCGFL1.f").read_text()
    require(
        re.search(r"(?i)XSIXYZ\s*\(\s*1\s*,\s*IDIR\s*\)", mcgfl1)
        is not None,
        "legacy XSI expression changed",
    )
    mcgffir = (ROOT / "src/MCGFFIR.f").read_text()
    require(
        re.search(r"(?i)IF\s*\(\s*IDIR\.GT\.0\s*\)\s*THEN", mcgffir)
        is not None,
        "locked MCGFFIR XSI guard",
    )
    mccgf = (ROOT / "src/MCCGF.f").read_text()
    for token in (
        "MCGFFI => MCGFFIR",
        "MCGFFA => MCGFFAR",
        "MCGSCH => MCGSCA",
    ):
        require(token in mccgf, f"frozen MCCGF procedure choice: {token}")
    require(
        "MCGFFI,MCGFFA,MCGSCH,MCGFFAL" in mccgf.replace(" ", ""),
        "frozen MCCGF forwarding",
    )

    production = "\n".join(
        path.read_text(errors="replace")
        for path in src_build_files()
        if path.is_file()
    )
    require(
        re.search(
            r"(?i)\buse\s+spor64_a3\b|"
            r"\bcall\s+mcgfcf_mcgfst_r64_compile_only_locked\b",
            production,
        )
        is None,
        "Phase-A3 connected to production",
    )
    require(
        re.search(
            r"(?i)\bsubroutine\s+spor64_a3_compile_only_link_forbidden\b",
            production,
        )
        is None,
        "link barrier defined in production",
    )

    tests = data["compile_tests"]
    require(
        tests["positive_anchor"]
        == "validation/iterative/real64_phase_a3/"
           "compile_spor64_a3_anchor.f90",
        "positive anchor path",
    )
    require(
        tests["positive_anchor_sha256"] == EXPECTED_ANCHOR_HASH,
        "positive anchor hash",
    )
    anchor = ROOT / tests["positive_anchor"]
    require(sha256_file(anchor) == EXPECTED_ANCHOR_HASH, "live anchor hash")
    require(tests["positive_anchor_has_program"] is False, "anchor program")
    require(
        tests["positive_anchor_active_set"]
        == "EMPTY-SAFE-FAIL-IF-EVER-INVOKED",
        "anchor active set",
    )
    require(
        re.search(r"(?im)^\s*program\b", anchor.read_text()) is None,
        "executable anchor",
    )
    require(tests["negative_sources"] == EXPECTED_NEGATIVE_HASHES,
            "negative source map")
    for relative, expected in EXPECTED_NEGATIVE_HASHES.items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"negative source hash: {relative}",
        )
    require(
        tests["legacy_objects_compiled"]
        == ["MCGFCF.f", "MCGFFIR.f", "MCGFFAR.f", "MCGFFAL.f",
            "MCGSCA.f", "MCGFST.f"],
        "legacy compile list",
    )
    require(tests["phase_a3_objects_linked"] == 0, "A3 links")
    require(tests["phase_a3_executables_built"] == 0, "A3 executables")
    require(tests["phase_a3_objects_executed"] == 0, "A3 executions")
    require(
        tests["prerequisite_phase_a2_synthetic_link"] is True,
        "Phase-A2 prerequisite link",
    )
    require(
        tests["prerequisite_phase_a2_synthetic_execution"] is True,
        "Phase-A2 prerequisite",
    )
    require(tests["tracking_reads"] == 0, "tracking reads")
    require(tests["transport_solves"] == 0, "transport solves")
    require(tests["dragon_runs"] == 0, "Dragon runs")

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a3",
            "build target")
    for field in ("added_to_default_all", "added_to_tests",
                  "added_to_spot_fast"):
        require(build[field] is False, field)
    require(build["temporary_build_directory"] is True, "temporary build")
    require(build["phase_a3_fortran_commands_compile_only"] is True,
            "Phase-A3 compile-only commands")
    require(
        build["runner_sha256"] == EXPECTED_RUNNER_SHA256,
        "runner digest",
    )
    require(
        build["top_level_makefile_delta"]
        == "BASELINE-PLUS-EXACT-ISOLATED-PHASE-A3-BLOCK",
        "top-level Makefile delta",
    )
    require(
        build["unresolved_symbol_policy"]
        == "EXACT-SEVEN-PROJECT-SYMBOLS-PLUS-ONE-COMPILER-RUNTIME",
        "unresolved symbol policy",
    )
    require(build["link_commands_allowed"] == [], "link commands")
    require(build["forbidden_flag"] == "-fdefault-real-8", "forbidden flag")
    require(build["required_checked_flags"] == REQUIRED_CHECKED_FLAGS,
            "checked flags")

    validate_makefile_contract((ROOT / "Makefile").read_text())
    require(data["remaining_open_path"] == EXPECTED_REMAINING_PATH,
            "remaining path")
    require(
        data["next_step"]
        == "Implement a compile-only default-off context carrier and host "
           "closure from the Phase-A2 callback to this Phase-A3 seam, "
           "preserving the link barrier and performing no tracking read or "
           "transport execution.",
        "next step",
    )
    require(
        data["interpretation"] == [
            "This slice encodes the checked data ABI, exact procedure "
            "identities and call order for the frozen real legacy "
            "MCGFCF-to-MCGFST path.",
            "It does not bind real tracking, KPSYS, PJJ, EXP1 or geometry "
            "context and cannot be linked or executed because the link "
            "barrier is intentionally unresolved.",
            "The legacy IDIR-zero XSI actual designator is nonconforming; "
            "the adapter uses legal caller-owned storage but does not "
            "claim the production call is fixed.",
            "No real MOC response, PJJ correction, physical accuracy, "
            "radial convergence, Stage-4 result or Picard trajectory is "
            "validated.",
            "No empirical coefficient, relaxation, clipping, fitted "
            "closure or new numerical threshold is introduced.",
        ],
        "interpretation",
    )

    validate_scoped_receipt()
    require(RUNNER.is_file(), "missing runner")
    validate_runner_contract(RUNNER.read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        validate(load_manifest(args.manifest))
    except (KeyError, PhaseA3Error) as exc:
        raise SystemExit(f"SPOR64 PHASE-A3 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A3 CONTRACT PASS: COMPILE-ONLY-LEGACY-ABI-SEAM; "
        "LINKS=0; EXECUTIONS=0; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()

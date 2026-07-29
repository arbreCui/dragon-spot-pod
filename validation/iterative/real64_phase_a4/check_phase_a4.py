#!/usr/bin/env python3
"""Fail-closed checker for the Phase-A4 compile-only host closure."""

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
IMPLEMENTATION = HERE / "SPOR64_A4.f90"
RUNNER = HERE / "run_phase_a4.sh"
RECEIPT = HERE / "phase_a4_implementation_receipt.sha256"
EXPECTED_CANONICAL_SHA256 = (
    "70f102aa607beba6f56a80505f5cd786c08b1a1daf75e324ca72d7f8f68c4fb4"
)
EXPECTED_RUNNER_SHA256 = (
    "0336225bab799fa95343cead535340bdda538021ddee0296fe8798a3d3004093"
)
BASELINE_COMMIT = "c721bcaf26d637b4eb3710b32c5a960130d0c8c9"

EXPECTED_DEPENDENCY_HASHES = {
    "validation/iterative/real64_phase_a1/SPOR64_A1.f90":
        "13f341a99fa99c21ff34821339d0347565489134379193a1bfcf58dfa65726da",
    "validation/iterative/real64_phase_a2/SPOR64_A2.f90":
        "9c0d209d29d99a910559e3b207d98ec466be751a8d7aa56e040fb382989579c2",
    "validation/iterative/real64_phase_a3/SPOR64_A3.f90":
        "3d8d9ebb2417f0c2139b88ecee157bcf16fa189e6f87e5dd6e76df8058f05ccc",
}
EXPECTED_PREREQUISITE_RECEIPT_HASHES = {
    "validation/iterative/real64_phase_a1/"
    "phase_a1_implementation_receipt.sha256":
        "2b5d6024bfb405d2c6c9c6fcca8fb1c3a8109e53732236674adafe3edd010f8d",
    "validation/iterative/real64_phase_a2/"
    "phase_a2_implementation_receipt.sha256":
        "2c1dcf7c6d9c8b75a234e543402c587103f10e2972e8ed3a2a40a9a052395c4c",
    "validation/iterative/real64_phase_a3/"
    "phase_a3_implementation_receipt.sha256":
        "f4c4a082779898ed481bb8a64aed17a1a884ffb15e80f0d67be3e6e1314486c1",
}
EXPECTED_IMPLEMENTATION_HASH = (
    "a656aac0b3a11a5610c4724ab67b3e66c1cdd0f0a0b7043fdec324b577c27fe8"
)
EXPECTED_ANCHOR_HASH = (
    "ce08f142f9e41f51fc17a65ce5417e7f60345daa57cf7f735f7856ffd0fb931a"
)
EXPECTED_NEGATIVE_HASHES = {
    "validation/iterative/real64_phase_a4/"
    "compile_fail_real32_mutable.f90":
        "b2eb40dbe4952b40eb1dad3aca08f35a00f5590120f81edf148aab291681d8c3",
    "validation/iterative/real64_phase_a4/"
    "compile_fail_wrong_context_type.f90":
        "2a3336cbec09373b65735f38402aef1952f98f6d551afd9879ef00b4e66ce5c3",
    "validation/iterative/real64_phase_a4/"
    "compile_fail_noncontiguous_actual.f90":
        "1a94e0ee8e38a4e16af9610cdfb9a8d10eb9c6ac8609f3475a1a374722234ee6",
}

EXPECTED_STATUS = {
    "classification": "IMPLEMENTED-COMPILE-ONLY-A2-A3-HOST-CLOSURE",
    "phase_a_static_closure": False,
    "source_arithmetic_closed": True,
    "synthetic_full_matrix_facade_closed": True,
    "legacy_abi_seam_encoded": True,
    "a2_to_a3_host_closure_encoded": True,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "context_storage_schema_closed": True,
    "context_population_checked": False,
    "real_context_provenance_bound": False,
    "tracking_position_validated": False,
    "EXP1_identity_bound": False,
    "actual_moc_response_validated": False,
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
    "context_enabled_default": False,
}

EXPECTED_REMAINING_PATH = [
    "checked Phase-A5 population and provenance contract for the A4 "
    "context carrier",
    "conforming XSI acquisition from the real host and separate "
    "production legacy-call repair",
    "real tracking-unit open identity and exact repositioning before "
    "every MCGFCF call",
    "live KPSYS lifetime group ordering and PJJ$MCCG identity",
    "PJJIND$MCCG provenance from the same tracking object",
    "EXP1 tabulated-exponential initialization identity in the same image",
    "SC SIGAL KPSYS geometry material and group-order identity",
    "separately authorized removal of the compile-only link barrier",
    "actual A2-to-A3 execution and exact replay",
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
    *EXPECTED_DEPENDENCY_HASHES.keys(),
    *EXPECTED_PREREQUISITE_RECEIPT_HASHES.keys(),
    "validation/iterative/real64_phase_a4/README.md",
    "validation/iterative/real64_phase_a4/SPOR64_A4.f90",
    "validation/iterative/real64_phase_a4/compile_spor64_a4_anchor.f90",
    *EXPECTED_NEGATIVE_HASHES.keys(),
    "validation/iterative/real64_phase_a4/precision_manifest.json",
    "validation/iterative/real64_phase_a4/check_phase_a4.py",
    "validation/iterative/real64_phase_a4/test_phase_a4_contract.py",
    "validation/iterative/real64_phase_a4/run_phase_a4.sh",
]

REQUIRED_CHECKED_FLAGS = [
    "-std=f2008",
    "-pedantic-errors",
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


class PhaseA4Error(RuntimeError):
    """Raised when the A4 compile-only boundary changes or overclaims."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA4Error(message)


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
        raise PhaseA4Error(f"cannot load manifest: {exc}") from exc
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
    phase_a4_block = (
        ".PHONY: spot-real64-phase-a4\n"
        "spot-real64-phase-a4 :\n"
        "\tsh validation/iterative/real64_phase_a4/run_phase_a4.sh\n"
    )
    require(
        makefile.count(phase_a4_block) == 1,
        "exact isolated Phase-A4 Makefile block",
    )
    baseline_makefile = git_blob(BASELINE_COMMIT, "Makefile").decode()
    require(
        makefile.replace(phase_a4_block, "", 1) == baseline_makefile,
        "top-level Makefile changed beyond the isolated Phase-A4 block",
    )
    ordinary_targets = re.findall(
        r"(?m)^([A-Za-z][A-Za-z0-9_.-]*)\s*:",
        makefile,
    )
    require(
        ordinary_targets and ordinary_targets[0] == "all",
        "default Make target changed",
    )
    for target in ("all", "tests", "spot-fast"):
        match = re.search(rf"(?m)^{re.escape(target)}\s*:(.*)$", makefile)
        require(match is not None, f"missing make target {target}")
        require(
            "spot-real64-phase-a4" not in match.group(1),
            f"Phase-A4 added to {target}",
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
    require("run_phase_a3.sh" not in runner,
            "frozen Phase-A3 runner is Makefile-incompatible")
    require("run_phase_a2.sh" in runner, "Phase-A2 prerequisite runner")
    require("phase_a3_implementation_receipt.sha256" in runner,
            "frozen Phase-A3 receipt recheck")
    require("phase_a4_implementation_receipt.sha256" in runner,
            "receipt invocation")
    for flag in REQUIRED_CHECKED_FLAGS:
        require(flag in runner, f"runner missing flag {flag}")

    logical_runner = re.sub(r"\\\n\s*", " ", runner)
    require(
        len(re.findall(r"\$FC(?![A-Za-z0-9_])", runner)) == 4,
        "compiler variable use count",
    )
    require(runner.count('"$FC"') == 4, "quoted compiler invocation count")
    require("${FC}" not in runner, "alternate compiler expansion")
    for token in (
        'LC_ALL=C',
        'EXPECTED_FC_BANNER="GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"',
        'test "$(uname -s)" != Darwin',
        'test "$(uname -m)" != arm64',
    ):
        require(token in runner, f"audited toolchain gate: {token}")
    require(
        runner.index("EXPECTED_FC_BANNER")
        < runner.index('sh "$A2/run_phase_a2.sh"'),
        "toolchain gate must precede prerequisites",
    )
    require(
        len(
            re.findall(
                r'(?m)^\s*(?:if\s+)?"\$FC"[^\n]*\s-c(?:\s|$)',
                logical_runner,
            )
        )
        == 3,
        "a Fortran command is not compile-only",
    )
    for token in (" ld ", "\nld ", "\nar ", "ranlib", "make -c src",
                  "rdragon"):
        require(token not in runner.lower(), f"runner link token: {token}")
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
            r"(?im)^\s*(?:if\s+)?(?:command\s+)?"
            r"(?:[\"']?/[^ \t\n\"']*/)?"
            r"(?:gfortran(?:-[0-9.]+)?|ifort|ifx|flang|nvfortran|f90|f95)"
            r"[\"']?(?:\s|$)",
            logical_runner,
        )
        is None,
        "runner contains an untracked compiler command",
    )
    require(
        re.search(
            r"(?im)^\s*(?:if\s+)?(?:command\s+)?"
            r"(?:[\"']?/[^ \t\n\"']*/)?"
            r"(?:ld|ar|ranlib|libtool)[\"']?(?:\s|$)",
            logical_runner,
        )
        is None,
        "runner contains an untracked linker command",
    )
    require(
        re.search(
            r"(?i)(?:^|[/\"'])dragon(?:[\"'\s]|$)",
            logical_runner,
        )
        is None,
        "runner may invoke Dragon",
    )
    for token in (
        "a3_unresolved.log",
        "a4_unresolved.log",
        "anchor_unresolved.log",
        'a3_unresolved.log")" -ne 8',
        'a4_unresolved.log")" -ne 10',
        'anchor_unresolved.log")" -ne 7',
        "spor64_a3_compile_only_link_forbidden",
        "unexpected A3 unresolved symbol",
        "unexpected A4 unresolved symbol",
        "unexpected anchor unresolved symbol",
        "phase_a3_primary_response",
        "PREREQUISITE-SYNTHETIC-LINKS=2",
        "PREREQUISITE-SYNTHETIC-EXECUTIONS=2",
    ):
        require(token in runner, f"runner exact symbol gate: {token}")


def validate_implementation_source(source: str) -> None:
    lower = source.lower()
    require("module spor64_a4" in lower, "module definition")
    require(
        "integer, parameter :: kind_guard = 1 / merge(1, 0," in lower,
        "kind guard",
    )
    require(
        "type, public :: spor64_a4_context" in lower,
        "context type",
    )
    context_match = re.search(
        r"(?is)type,\s*public\s*::\s*spor64_a4_context"
        r"(?P<body>.*?)end\s+type\s+spor64_a4_context",
        lower,
    )
    require(context_match is not None, "context type body")
    context_body = context_match.group("body")
    require(
        "logical :: enabled = .false." in context_body,
        "context is not default-off",
    )
    context_declarations = [
        re.sub(r"\s+", "", line)
        for line in context_body.splitlines()
        if line.strip()
    ]
    require(
        context_declarations == [
            "logical::enabled=.false.",
            "integer::iftrak=0",
            "integer::nbtr=0",
            "integer::nmax=0",
            "integer::nbatch=0",
            "integer,allocatable::isgnr(:,:),pjjind(:,:)",
            "type(c_ptr),allocatable::kpsys(:)",
            "real(real32),allocatable::cpo(:),zmu(:),wzmu(:),volume(:)",
            "real(real64),allocatable::caz0(:),caz1(:),caz2(:),xsi(:)",
        ],
        "context component declaration set",
    )
    require("pointer" not in context_body, "context pointer component")
    require("procedure" not in context_body, "context procedure component")
    for declaration in (
        "integer, allocatable :: isgnr(:,:), pjjind(:,:)",
        "type(c_ptr), allocatable :: kpsys(:)",
        "real(real32), allocatable :: cpo(:), zmu(:), wzmu(:), volume(:)",
        "real(real64), allocatable :: caz0(:), caz1(:), caz2(:), xsi(:)",
    ):
        require(declaration in context_body, f"context declaration: {declaration}")
    for forbidden in (
        "ngind",
        "nconv",
        "sigal",
        "keyflx",
        "keycur",
        "source",
        "raw_response",
        "ibc",
    ):
        require(forbidden not in context_body,
                f"duplicated shared context state: {forbidden}")

    module_spec = lower.split("contains", 1)[0]
    module_spec_without_context = (
        module_spec[:context_match.start()]
        + module_spec[context_match.end():]
    )
    logical_module_spec = re.sub(
        r"&\s*\n\s*",
        "",
        module_spec_without_context,
    )
    module_statements = [
        re.sub(r"\s+", "", line)
        for line in logical_module_spec.splitlines()
        if line.strip()
    ]
    require(
        module_statements == [
            "modulespor64_a4",
            "use,intrinsic::iso_c_binding,only:c_ptr",
            "use,intrinsic::iso_fortran_env,only:real32,real64",
            "usespor64_a2,only:mcgfl1r64_post_stis_raw_facade_locked,"
            "spor64_a2_invalid,spor64_a2_ok,spor64_a2_response_failed,"
            "spor64_a2_unsupported",
            "usespor64_a3,only:mcgfcf_mcgfst_r64_compile_only_locked,"
            "spor64_a3_invalid,spor64_a3_ok",
            "implicitnone",
            "private",
            "integer,parameter::kind_guard=1/merge(1,0,"
            "kind(1.0)==real32.and.kind(1.0d0)==real64)",
            "integer,parameter,public::spor64_a4_ok=spor64_a2_ok",
            "integer,parameter,public::spor64_a4_unsupported="
            "spor64_a2_unsupported",
            "integer,parameter,public::spor64_a4_invalid=spor64_a2_invalid",
            "integer,parameter,public::spor64_a4_response_failed="
            "spor64_a2_response_failed",
            "public::mcgfl1r64_a2_a3_host_closure_compile_only_locked",
        ],
        "module specification statement set",
    )
    for declaration in re.findall(
        r"(?im)^\s*(?:integer|real|logical|complex|character|type\s*\()"
        r"[^\n]*::[^\n]*$",
        module_spec_without_context,
    ):
        require(
            "parameter" in declaration,
            f"module mutable declaration: {declaration.strip()}",
        )
    require(
        re.search(r"(?im)^\s*(?:save|common)\b|,\s*save\b", source) is None,
        "hidden mutable state",
    )
    calls = [
        name.lower()
        for name in re.findall(
            r"(?i)\bcall\s+([a-z][a-z0-9_]*)",
            source,
        )
    ]
    require(
        calls
        == [
            "mcgfl1r64_post_stis_raw_facade_locked",
            "mcgfcf_mcgfst_r64_compile_only_locked",
        ],
        "A2-to-A3 call sequence",
    )
    require(
        "subroutine phase_a3_primary_response" in lower,
        "internal callback",
    )
    require(
        lower.count("phase_a3_primary_response") == 3,
        "internal callback identity or escape",
    )
    require(
        "if (.not. context%enabled) return"
        in lower,
        "default-off guard",
    )
    require(
        lower.index("if (.not. context%enabled) return")
        < lower.index("call mcgfl1r64_post_stis_raw_facade_locked"),
        "default-off guard order",
    )
    outer = lower.split(
        "subroutine mcgfl1r64_a2_a3_host_closure_compile_only_locked",
        1,
    )[1].split("\n  contains", 1)[0]
    outer_header, outer_after_header = outer.split("status)", 1)
    require(
        re.sub(r"[\s&]+", "", outer_header)
        == "(n,ndim,nzon,qn,fi,m,nani,nlin,nfunl,sc,source,kpn,nreg,"
           "keyflx,keycur,ibc,sigal,stis,cyclic,lprism,idir,ng,ngeff,"
           "ngind,nconv,context,raw_response,",
        "outer signature",
    )
    outer_declaration_block = outer_after_header.split(
        "status = spor64_a4_unsupported",
        1,
    )[0]
    outer_declarations = [
        re.sub(r"\s+", "", line)
        for line in outer_declaration_block.splitlines()
        if line.strip()
    ]
    require(
        outer_declarations == [
            "integer,intent(in)::n,ndim,m,nani,nlin,nfunl",
            "integer,intent(in)::kpn,nreg,stis,idir,ng,ngeff",
            "integer,contiguous,intent(in)::nzon(:),keycur(:),ibc(:)",
            "integer,contiguous,target,intent(in)::keyflx(:,:,:)",
            "integer,contiguous,intent(in)::ngind(:)",
            "logical,intent(in)::cyclic,lprism",
            "logical,contiguous,intent(in)::nconv(:)",
            "real(real64),contiguous,intent(in)::qn(:,:),fi(:,:)",
            "real(real32),contiguous,intent(in)::sc(0:,:,:),sigal(-6:,:)",
            "real(real64),contiguous,intent(inout)::source(:,:)",
            "real(real64),contiguous,intent(inout)::raw_response(:,:)",
            "type(spor64_a4_context),intent(in)::context",
            "integer,intent(out)::status",
        ],
        "outer declaration set",
    )
    status_declaration = "integer, intent(out) :: status"
    require(status_declaration in outer, "outer status declaration")
    pre_guard = outer.split(status_declaration, 1)[1].split(
        "if (.not. context%enabled) return",
        1,
    )[0]
    require(
        re.sub(r"\s+", "", pre_guard)
        == "status=spor64_a4_unsupported",
        "default-off path has a side effect",
    )
    for host_state in ("source", "raw_response"):
        require(
            re.search(
                rf"(?im)^\s*{host_state}(?:\s*\([^=\n]*\))?\s*=(?!=)",
                outer,
            )
            is None,
            f"outer host state assignment: {host_state}",
        )
    outer_status_assignments = re.findall(
        r"(?im)^\s*status\s*=(?!=)\s*([^\n]+)$",
        outer,
    )
    require(
        outer_status_assignments
        == ["spor64_a4_unsupported", "spor64_a4_invalid"],
        "outer status assignment set",
    )
    a2_call_marker = "call mcgfl1r64_post_stis_raw_facade_locked"
    a2_call_tail = outer.split(a2_call_marker, 1)[1].split(
        "status)",
        1,
    )[0]
    actual_a2_call = re.sub(
        r"[\s&]+",
        "",
        a2_call_marker + a2_call_tail + "status)",
    )
    expected_a2_call = (
        "callmcgfl1r64_post_stis_raw_facade_locked("
        "n,ndim,nzon,qn,fi,m,nani,nlin,nfunl,sc,source,kpn,nreg,keyflx,"
        "keycur,ibc,sigal,stis,cyclic,lprism,idir,ng,ngeff,ngind,nconv,"
        "phase_a3_primary_response,raw_response,status)"
    )
    require(actual_a2_call == expected_a2_call, "exact A2 actual list")

    require("size(context%" in lower, "context dimension checks")
    first_context_size = lower.index("size(context%")
    for component in (
        "isgnr",
        "pjjind",
        "kpsys",
        "cpo",
        "zmu",
        "wzmu",
        "volume",
        "caz0",
        "caz1",
        "caz2",
        "xsi",
    ):
        token = f"if (.not. allocated(context%{component})) return"
        require(token in lower, f"allocated preflight: {component}")
        require(
            lower.index(token) < first_context_size,
            f"SIZE before ALLOCATED: {component}",
        )

    callback = lower.split(
        "subroutine phase_a3_primary_response",
        1,
    )[1]
    callback_header, callback_after_header = callback.split(
        "response_status)",
        1,
    )
    require(
        re.sub(r"[\s&]+", "", callback_header)
        == "(local_ngeff,local_ngind,local_nconv,local_kpn,"
           "local_source,local_raw_response,",
        "callback signature",
    )
    declaration_block = callback_after_header.split(
        "response_status = spor64_a3_invalid",
        1,
    )[0]
    callback_declarations = [
        re.sub(r"\s+", "", line)
        for line in declaration_block.splitlines()
        if line.strip()
    ]
    require(
        callback_declarations == [
            "integer,intent(in)::local_ngeff,local_kpn",
            "integer,intent(in)::local_ngind(:)",
            "logical,intent(in)::local_nconv(:)",
            "real(real64),intent(in)::local_source(:,:)",
            "real(real64),intent(inout)::local_raw_response(:,:)",
            "integer,intent(out)::response_status",
            "integer::allocation_status",
            "real(real64),allocatable::raw_a3(:,:),source_a3(:,:)",
        ],
        "callback declaration set",
    )
    numeric_allocatables = re.findall(
        r"(?im)^\s*real\([^)]*\),\s*allocatable\s*::\s*([^!\n]+)$",
        callback,
    )
    require(
        len(numeric_allocatables) == 1,
        "additional numeric staging declaration",
    )
    staging_declaration = re.sub(r"\s+", "", numeric_allocatables[0])
    require(
        staging_declaration == "raw_a3(:,:),source_a3(:,:)",
        "exact two REAL64 staging arrays",
    )
    require(
        "real(real64), allocatable :: raw_a3(:,:), source_a3(:,:)"
        in callback,
        "REAL64 staging declaration",
    )
    require(
        re.search(
            r"allocate\s*\(\s*source_a3\(kpn,ngeff\)\s*,\s*"
            r"raw_a3\(kpn,ngeff\)\s*,\s*&?\s*"
            r"stat=allocation_status\s*\)",
            callback,
        )
        is not None,
        "staging allocation",
    )
    for identity in (
        "if (local_ngeff /= ngeff .or. local_kpn /= kpn) return",
        "if (any(local_ngind /= ngind)) return",
        "if (any(local_nconv .neqv. nconv)) return",
    ):
        require(identity in callback, f"callback identity: {identity}")
    require("source_a3 = local_source" in callback, "source staging copy")
    require(
        "raw_a3 = local_raw_response" in callback,
        "raw staging copy",
    )
    source_stage_assignments = re.findall(
        r"(?im)^\s*source_a3\s*=(?!=)\s*([^\n]+)$",
        callback,
    )
    raw_stage_assignments = re.findall(
        r"(?im)^\s*raw_a3\s*=(?!=)\s*([^\n]+)$",
        callback,
    )
    require(
        source_stage_assignments == ["local_source"],
        "source staging assignment set",
    )
    require(
        raw_stage_assignments == ["local_raw_response"],
        "raw staging assignment set",
    )
    response_status_assignments = re.findall(
        r"(?im)^\s*response_status\s*=(?!=)\s*([^\n]+)$",
        callback,
    )
    require(
        response_status_assignments == ["spor64_a3_invalid"],
        "callback status assignment set",
    )
    require(
        callback.count("local_raw_response = raw_a3") == 1,
        "raw success copyback count",
    )
    success_guard = "if (response_status == spor64_a3_ok) then"
    require(success_guard in callback, "A3 success guard")
    status_if = callback.index(success_guard)
    raw_copy = callback.index("local_raw_response = raw_a3")
    require("end if" in callback[status_if:], "A3 success guard end")
    status_end = callback.index("end if", status_if)
    require(
        status_if < raw_copy < status_end,
        "raw copyback is not success-only",
    )
    require(
        re.search(r"(?im)^\s*local_source\s*=", callback) is None,
        "source copied back",
    )
    for token in ("reshape", "pack", "unpack", "transfer"):
        require(token not in callback, f"forbidden staging token: {token}")
    require(
        re.search(r"real\s*\([^,\n]+,\s*real32\s*\)", callback) is None,
        "REAL64-to-REAL32 conversion",
    )
    require(
        "integer, contiguous, intent(in) :: ngind(:)" in lower,
        "host NGIND is not contiguous",
    )
    require(
        "logical, contiguous, intent(in) :: nconv(:)" in lower,
        "host NCONV is not contiguous",
    )
    require(
        "integer, intent(in) :: local_ngind(:)" in callback,
        "callback NGIND characteristics changed",
    )
    require(
        "logical, intent(in) :: local_nconv(:)" in callback,
        "callback NCONV characteristics changed",
    )
    require(
        "context%volume, ng, ngind, cyclic, lprism, stis"
        in callback,
        "A3 host-associated NGIND forwarding",
    )
    a3_call_marker = "call mcgfcf_mcgfst_r64_compile_only_locked"
    a3_call_tail = callback.split(a3_call_marker, 1)[1].split(
        "response_status)",
        1,
    )[0]
    actual_a3_call = re.sub(
        r"[\s&]+",
        "",
        a3_call_marker + a3_call_tail + "response_status)",
    )
    expected_a3_call = (
        "callmcgfcf_mcgfst_r64_compile_only_locked("
        "context%iftrak,context%nbtr,context%nmax,ndim,local_kpn,n,nreg,m,"
        "local_ngeff,size(context%caz0),size(context%cpo),nani,nfunl,"
        "size(context%isgnr,1),nani,nlin,size(context%isgnr,2),keyflx,"
        "keycur,nzon,nconv,context%caz0,context%caz1,context%caz2,"
        "context%cpo,context%zmu,context%wzmu,source_a3,sigal,"
        "context%isgnr,idir,size(context%xsi),context%nbatch,context%xsi,"
        "raw_a3,context%kpsys,nani,size(context%pjjind,1),context%pjjind,"
        "context%volume,ng,ngind,cyclic,lprism,stis,response_status)"
    )
    require(actual_a3_call == expected_a3_call, "exact A3 actual list")
    require(
        "local_nconv" not in callback.split(
            "call mcgfcf_mcgfst_r64_compile_only_locked",
            1,
        )[1].split("response_status)", 1)[0],
        "A3 uses callback NCONV instead of host NCONV",
    )

    for token in (
        "read",
        "rewind",
        "open",
        "close",
        "write",
        "print",
        "inquire",
        "backspace",
        "endfile",
        "flush",
        "wait",
        "format",
        "lcmget",
        "lcmgpd",
        "c_f_pointer",
        "mcgfca",
        "mcgfcr",
        "mcgabg",
        "relax",
        "aitken",
        "anderson",
    ):
        require(
            re.search(rf"(?im)^\s*{re.escape(token)}\b", source) is None,
            f"forbidden implementation operation: {token}",
        )
    require(
        "spor64_a3_compile_only_link_forbidden" not in lower,
        "A4 defines or directly invokes a second barrier",
    )


def validate(data: dict[str, Any], *, verify_canonical: bool = True) -> None:
    if verify_canonical:
        require(
            canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
            "canonical manifest hash mismatch",
        )
    require(
        data["schema"]
        == "spot-radial-real64-phase-a4-compile-only-a2-a3-host-closure-v1",
        "schema",
    )
    require(
        data["title"]
        == "Compile-only REAL64 Phase-A2 to Phase-A3 host closure",
        "title",
    )
    require(data["status"] == EXPECTED_STATUS, "status or authorization")

    baseline = data["baseline"]
    require(baseline["commit"] == BASELINE_COMMIT, "baseline commit")
    require(
        baseline["source_sha256"] == EXPECTED_DEPENDENCY_HASHES,
        "dependency source hash map",
    )
    for relative, expected in EXPECTED_DEPENDENCY_HASHES.items():
        require(
            sha256_bytes(git_blob(BASELINE_COMMIT, relative)) == expected,
            f"baseline source mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live dependency changed: {relative}",
        )
    require(
        baseline["prerequisite_receipt_sha256"]
        == EXPECTED_PREREQUISITE_RECEIPT_HASHES,
        "prerequisite receipt hash map",
    )
    for relative, expected in EXPECTED_PREREQUISITE_RECEIPT_HASHES.items():
        require(
            sha256_bytes(git_blob(BASELINE_COMMIT, relative)) == expected,
            f"baseline prerequisite receipt mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live prerequisite receipt changed: {relative}",
        )

    require(
        data["implementation"] == {
            "location": "validation/iterative/real64_phase_a4/SPOR64_A4.f90",
            "module": "SPOR64_A4",
            "context_type": "SPOR64_A4_CONTEXT",
            "procedure":
                "MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED",
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

    require(
        data["context_contract"] == {
            "carrier":
                "CALLER-OWNED-DERIVED-TYPE-WITH-OWNED-ALLOCATABLE-COMPONENTS",
            "scalar_components":
                ["enabled", "iftrak", "nbtr", "nmax", "nbatch"],
            "allocatable_components": {
                "INTEGER": ["isgnr(:,:)", "pjjind(:,:)"],
                "TYPE-C_PTR": ["kpsys(:)"],
                "REAL32":
                    ["cpo(:)", "zmu(:)", "wzmu(:)", "volume(:)"],
                "REAL64":
                    ["caz0(:)", "caz1(:)", "caz2(:)", "xsi(:)"],
            },
            "pointer_components": [],
            "procedure_pointer_components": [],
            "type_bound_execution": False,
            "module_mutable_state": False,
            "SAVE_or_COMMON_state": False,
            "shared_state_excluded_from_carrier": [
                "NZON", "KEYFLX", "KEYCUR", "IBC", "SIGAL", "SC",
                "NGIND", "NCONV", "SOURCE", "RAW_RESPONSE",
            ],
            "derived_dimensions": [
                "NANGL=size(CAZ0)", "NMU=size(CPO)",
                "NMOD=size(ISGNR,1)", "NFUNLX=size(ISGNR,2)",
                "NPJJM=size(PJJIND,1)", "NSOUT=size(XSI)",
            ],
            "borrowed_external_resources": [
                "IFTRAK sequential unit", "KPSYS C_PTR pointees",
            ],
            "carrier_owns_external_resources": False,
            "carrier_proves_provenance": False,
            "public_component_population_kind_checked": False,
        },
        "context contract",
    )
    require(
        data["host_closure_contract"] == {
            "language_feature":
                "FORTRAN-2008-INTERNAL-PROCEDURE-HOST-ASSOCIATION",
            "internal_callback": "phase_a3_primary_response",
            "callback_stored_or_escaped": False,
            "call_sequence": [
                "MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED",
                "phase_a3_primary_response",
                "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
            ],
            "callback_local_identity_checks": [
                "local_ngeff == host_ngeff",
                "local_kpn == host_kpn",
                "local_ngind == host_ngind",
                "local_nconv .EQV. host_nconv",
                "local SOURCE shape == KPN by NGEFF",
                "local RAW_RESPONSE shape == KPN by NGEFF",
            ],
            "A3_uses_host_contiguous_NGIND_NCONV": True,
            "explicit_staging_arrays": ["source_a3", "raw_a3"],
            "staging_count": 2,
            "staging_kind": "REAL64",
            "source_stage_rule": "source_a3 = local_source",
            "raw_stage_rule": "raw_a3 = local_raw_response",
            "source_copyback": "NONE",
            "raw_copyback":
                "ONLY-IF-A3-STATUS-EQUALS-SPOR64-A3-OK",
            "A3_failure_status_mapping":
                "NONZERO-CALLBACK-STATUS-TO-A2-RESPONSE-FAILED",
            "binary64_to_binary32_conversion": "NONE",
            "hidden_array_temporary":
                "GFORTRAN-WARRAY-TEMPORARIES-WERROR-FOR-A3-A4-OBJECT-COMPILE",
        },
        "host closure contract",
    )
    require(
        data["external_state_boundary"] == {
            "caller_SOURCE_RAW_atomic_before_legacy_entry": True,
            "caller_SOURCE_RAW_atomic_on_A3_nonzero_return": True,
            "legacy_operator_has_recoverable_error_status": False,
            "tracking_file_position_atomic": False,
            "process_state_atomic_after_XABORT": False,
            "adapter_performs_io": False,
            "adapter_reads_or_rewinds_tracking": False,
            "tracking_unit_positioned_by_future_caller": True,
            "each_future_MCGFCF_call_consumes_full_NBTR_stream": True,
            "real_tracking_context_bound": False,
            "real_KPSYS_PJJ_directories_bound": False,
            "EXP1_table_initialization_bound": False,
            "legal_XSI_storage_is_production_fix": False,
        },
        "external-state boundary",
    )

    validate_implementation_source(IMPLEMENTATION.read_text())
    a3_source = (
        ROOT / "validation/iterative/real64_phase_a3/SPOR64_A3.f90"
    ).read_text()
    require(
        "call SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN()" in a3_source,
        "A3 link barrier removed",
    )
    production = "\n".join(
        path.read_text(errors="replace")
        for path in src_build_files()
        if path.is_file()
    )
    require(
        re.search(
            r"(?i)\buse\s+spor64_a4\b|"
            r"\bcall\s+mcgfl1r64_a2_a3_host_closure_compile_only_locked\b",
            production,
        )
        is None,
        "Phase-A4 connected to production",
    )
    require(
        re.search(
            r"(?i)\bsubroutine\s+spor64_a3_compile_only_link_forbidden\b",
            production,
        )
        is None,
        "A3 link barrier defined in production",
    )

    tests = data["compile_tests"]
    require(
        tests["positive_anchor"]
        == "validation/iterative/real64_phase_a4/"
           "compile_spor64_a4_anchor.f90",
        "anchor path",
    )
    require(
        tests["positive_anchor_sha256"] == EXPECTED_ANCHOR_HASH,
        "anchor hash",
    )
    anchor = ROOT / tests["positive_anchor"]
    require(sha256_file(anchor) == EXPECTED_ANCHOR_HASH, "live anchor hash")
    require(tests["positive_anchor_has_program"] is False, "anchor program")
    require(
        tests["positive_anchor_context"]
        == "DEFAULT-DISABLED-AND-UNALLOCATED",
        "anchor context",
    )
    require(
        re.search(r"(?im)^\s*program\b", anchor.read_text()) is None,
        "executable anchor",
    )
    require(
        tests["negative_sources"] == EXPECTED_NEGATIVE_HASHES,
        "negative source map",
    )
    for relative, expected in EXPECTED_NEGATIVE_HASHES.items():
        require(
            sha256_file(ROOT / relative) == expected,
            f"negative source hash: {relative}",
        )
    expected_test_values = {
        "A4_unresolved_symbol_count": 10,
        "anchor_unresolved_symbol_count": 7,
        "A3_unresolved_symbol_count_rechecked": 8,
        "A3_link_barrier_rechecked": True,
        "phase_a4_objects_linked": 0,
        "phase_a4_executables_built": 0,
        "phase_a4_objects_executed": 0,
        "prerequisite_phase_a3_compile_only": True,
        "prerequisite_phase_a3_runner_executed": False,
        "prerequisite_phase_a3_receipt_rechecked": True,
        "prerequisite_phase_a3_source_recompiled": True,
        "prerequisite_phase_a2_runner_executed": True,
        "prerequisite_phase_a1_runner_executed": True,
        "prerequisite_phase_a1_synthetic_link": True,
        "prerequisite_phase_a1_synthetic_execution": True,
        "prerequisite_phase_a2_synthetic_link": True,
        "prerequisite_phase_a2_synthetic_execution": True,
        "tracking_reads": 0,
        "transport_solves": 0,
        "dragon_runs": 0,
    }
    for field, expected in expected_test_values.items():
        require(tests[field] == expected, f"compile test field: {field}")

    build = data["build_contract"]
    require(build["top_level_target"] == "spot-real64-phase-a4",
            "build target")
    for field in ("added_to_default_all", "added_to_tests",
                  "added_to_spot_fast"):
        require(build[field] is False, field)
    require(build["temporary_build_directory"] is True, "temporary build")
    require(
        build["phase_a4_fortran_commands_compile_only"] is True,
        "Phase-A4 compile-only commands",
    )
    require(build["runner_sha256"] == EXPECTED_RUNNER_SHA256,
            "runner digest")
    require(build["validated_platform"] == "Darwin-arm64",
            "validated platform")
    require(
        build["validated_compiler_banner"]
        == "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0",
        "validated compiler",
    )
    require(build["validated_locale"] == "C", "validated locale")
    require(
        build["cross_toolchain_portability_claim"]
        == "NONE-SEPARATE-RECEIPT-REQUIRED",
        "cross-toolchain claim",
    )
    require(
        build["top_level_makefile_delta"]
        == "BASELINE-PLUS-EXACT-ISOLATED-PHASE-A4-BLOCK",
        "Makefile delta",
    )
    require(
        build["unresolved_symbol_policy"]
        == "THREE-OBJECT-EXACT-ALLOWLISTS-WITH-EXACT-COUNTS",
        "unresolved symbol policy",
    )
    require(build["link_commands_allowed"] == [], "link commands")
    require(build["forbidden_flag"] == "-fdefault-real-8",
            "forbidden flag")
    require(
        build["required_checked_flags"] == REQUIRED_CHECKED_FLAGS,
        "checked flags",
    )
    validate_makefile_contract((ROOT / "Makefile").read_text())

    require(
        data["remaining_open_path"] == EXPECTED_REMAINING_PATH,
        "remaining path",
    )
    require(
        data["next_step"]
        == "Implement a compile-only default-off Phase-A5 context "
           "population and provenance contract from the real MCGFL1 host, "
           "preserving the A3 link barrier and performing no tracking read "
           "or transport execution.",
        "next step",
    )
    require(
        data["interpretation"] == [
            "This slice encodes the standard Fortran host closure from the "
            "Phase-A2 full-matrix callback to the Phase-A3 legacy ABI seam.",
            "The two explicit REAL64 staging matrices are only a "
            "contiguous-storage adapter required by the frozen Phase-A2 "
            "callback interface; they add no model, coefficient, threshold "
            "or precision conversion.",
            "The context type is typed storage only and does not prove "
            "tracking position, KPSYS PJJ lifetime, EXP1 initialization, "
            "XSI provenance or cross-object identity.",
            "No A4 object is linked or executed, no real MOC response is "
            "evaluated, and no production route is changed.",
            "No physical accuracy, radial convergence, Stage-4 "
            "qualification or Picard trajectory is established.",
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
    except (KeyError, PhaseA4Error) as exc:
        raise SystemExit(f"SPOR64 PHASE-A4 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A4 CONTRACT PASS: COMPILE-ONLY-A2-A3-HOST-CLOSURE; "
        "A4-OBJECT-LINKS=0; A4-OBJECT-EXECUTIONS=0; "
        "PREREQUISITE-SYNTHETIC-EXECUTIONS=2; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()

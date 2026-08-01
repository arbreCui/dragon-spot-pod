#!/usr/bin/env python3
"""Fail-closed static checker for the A9b-B1 production promotion gate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
README = HERE / "README.md"
RUNNER = HERE / "run_phase_a9b_promotion.sh"
ANCHOR = HERE / "compile_spor64_a9b_promotion_anchor.f90"
RECEIPT = HERE / "phase_a9b_promotion_receipt.sha256"
MAKEFILE = ROOT / "Makefile"
ROOT_README = ROOT / "README.md"
ITERATIVE_README = ROOT / "validation/iterative/README.md"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9/phase_a9a_implementation_receipt.sha256"
)

BASELINE_COMMIT = "899630398a09cc7fa62822bed0c8782351eddbc5"
PARENT_RECEIPT_SHA256 = (
    "1251ec474b13ce036ed1c530da71e0de33f27e0c39f7fbaa3b4335b0f01a6c10"
)
BASELINE_MAKEFILE_SHA256 = (
    "db0bc5334396bd14b3c908ddcda8cbe96a3bced7dd660850a76b2abadce8ea3d"
)
EXPECTED_CANONICAL_MANIFEST_SHA256 = (
    "474781a529d65e60059bb37055c8cea0c450ba33a6facde71cf47a747eb2d68c"
)
EXPECTED_RUNNER_SHA256 = (
    "6db3ca51b9b52ad5ec066c38328dbba5f656edad0f8082a6d414ff138a384531"
)

A9A_MAKE_BLOCK = (
    ".PHONY: spot-real64-phase-a9a\n"
    "spot-real64-phase-a9a :\n"
    "\tsh validation/iterative/real64_phase_a9/run_phase_a9a.sh\n"
)
A9B_PROMOTION_MAKE_BLOCK = (
    ".PHONY: spot-real64-phase-a9b-promotion\n"
    "spot-real64-phase-a9b-promotion :\n"
    "\tsh validation/iterative/real64_phase_a9b_promotion/"
    "run_phase_a9b_promotion.sh\n"
)

EXPECTED_PROMOTIONS = [
    {
        "validation": "validation/iterative/real64_phase_a8/SPOR64_A8_ACA.f90",
        "production": "src/SPOR64_A8_ACA.f90",
        "sha256": "a0138a9ad863ef0c6e6eb7c51520d568ee20b6b26c79c332c374f6ba3f09c115",
    },
    {
        "validation": "validation/iterative/real64_phase_a8/SPOR64_A8.f90",
        "production": "src/SPOR64_A8.f90",
        "sha256": "eaa8110ce17e109db22e93a95d2b8d5495edfd57c18b1aa8676bc2cdaba9e8d7",
    },
    {
        "validation": (
            "validation/iterative/real64_phase_a8/"
            "MCGFFIR64_RANK_ADAPTER.f90"
        ),
        "production": "src/MCGFFIR64_RANK_ADAPTER.f90",
        "sha256": "b0f71b95d01e72fe873eae197549ad10cd7f27fca2e3f0e640e7460a2ea4ace7",
    },
    {
        "validation": "validation/iterative/real64_phase_a9/SPOR64_A9.f90",
        "production": "src/SPOR64_A9.f90",
        "sha256": "f0ec2c7292986e4c048bf78108df3a3b8609ad393b77e0012a1a572a5d5c9b4a",
    },
]

EXPECTED_STATUS = {
    "classification": "FROZEN-IMPLEMENTED-COMPILE-ONLY-PRODUCTION-PROMOTION",
    "permitted_claim": "PRODUCTION-OBJECTS-AVAILABLE-COMPILE-ONLY",
    "production_modules_available": True,
    "byte_identical_to_frozen_validation": True,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "r64_parser_implemented": False,
    "host_ingress_implemented": False,
    "xdrta2_epoch_validated": False,
    "spomoc_capture64_implemented": False,
    "archive_implemented": False,
    "continuous_real64_lane": False,
    "runtime_provenance_validated": False,
    "actual_transport_response_validated": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
    "object_links": 0,
    "object_executions": 0,
    "tracking_reads": 0,
    "transport_solves": 0,
    "dragon_runs": 0,
}

EXPECTED_AUTHORITY = {
    "parent_phase": "A9a",
    "parent_commit": BASELINE_COMMIT,
    "parent_receipt": (
        "validation/iterative/real64_phase_a9/"
        "phase_a9a_implementation_receipt.sha256"
    ),
    "parent_receipt_sha256": PARENT_RECEIPT_SHA256,
    "scope": "four additive production sources only; no existing production source is edited",
}

EXPECTED_DEPENDENCIES = [
    "SPOR64_A8.o: SPOR64_A8_ACA.o",
    "SPOR64_A9.o: SPOR64_A8.o",
]

EXPECTED_SEAMS = [
    "SPOMOC_MCCGF_BEGIN",
    "SPOMOC_SET_ROLE",
    "SPOMOC_PUBLISH",
    "SPOMOC_CAPTURE64",
]

EXPECTED_HOST_HASHES = {
    "src/FLUGPI.f": "0155090fc67f38184c4602b0d330cf241a0eeba7f82c203fc25529267b5401ac",
    "src/FLU.f": "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0",
    "src/FLUDRV.f": "6bfd74d6cb473619bcf6130fc723502d348b6a3e76da86e5d03934207b3e4934",
    "src/FLU2DR.f": "edd308054f2977999591a1e9df173212da1a7cb4a6519042295a96fd2c8bbc39",
    "src/SPOMOC.f90": "23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc",
    "src/XDRTA2.f": "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
    "src/Makefile": "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
    "script/make_depend.py": "63e26ac26902eeafa062f656565a1fc6f8a972b11bebf68e228095b757467b64",
}

EXPECTED_NEXT_SUBGATE = {
    "name": "A9b host ingress and accepted-only publication",
    "required_order": (
        "single R64 parse -> full read-only admission -> zero-argument "
        "XDRTA2 exactly once -> selected REAL64 core -> strict accepted publication"
    ),
    "selected_on_may_fallback": False,
    "public_writes_before_strict_acceptance": False,
}

EXPECTED_COMPILE_GATE = {
    "target": "spot-real64-phase-a9b-promotion",
    "platform": "Darwin-arm64",
    "compiler": "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0",
    "promoted_objects": 4,
    "objects_linked": 0,
    "executables_built": 0,
    "objects_executed": 0,
    "default_real8_must_fail": True,
    "exact_nm_allowlists": True,
    "main_symbol_allowed": False,
}

EXPECTED_FORBIDDEN = [
    "editing FLUGPI, FLU, FLUDRV, FLU2DR, SPOMOC, XDRTA2 or src/Makefile",
    "production call site or R64 parser",
    "implementation of SPOMOC_CAPTURE64 or any GANLIB publication",
    "linking or executing a promoted object",
    "tracking read, transport solve or Dragon run",
    "relaxation, fitted coefficient, clipping, flux floor, tuned cutoff or new tolerance",
    "continuous-lane, convergence, Stage-4, Picard or physical-accuracy claim",
]

EXPECTED_NEGATIVES = (
    "compile_fail_real32_state.f90",
    "compile_fail_real64_operator.f90",
    "compile_fail_noncontiguous_state.f90",
    "compile_fail_int32_counter.f90",
    "compile_fail_flat_keyflx.f90",
    "compile_fail_aca_im_extent.f90",
)

EXPECTED_SYMBOL_FILES = tuple(
    f"expected_{stem}_{kind}.txt"
    for stem in ("aca", "a8", "adapter", "a9", "anchor")
    for kind in ("unresolved", "defined")
)

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9/phase_a9a_implementation_receipt.sha256",
    "validation/iterative/real64_phase_a8/SPOR64_A8_ACA.f90",
    "validation/iterative/real64_phase_a8/SPOR64_A8.f90",
    "validation/iterative/real64_phase_a8/MCGFFIR64_RANK_ADAPTER.f90",
    "validation/iterative/real64_phase_a9/SPOR64_A9.f90",
    "src/SPOR64_A8_ACA.f90",
    "src/SPOR64_A8.f90",
    "src/MCGFFIR64_RANK_ADAPTER.f90",
    "src/SPOR64_A9.f90",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLU2DR.f",
    "src/SPOMOC.f90",
    "src/XDRTA2.f",
    "src/Makefile",
    "script/make_depend.py",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "validation/iterative/real64_phase_a9b_promotion/README.md",
    "validation/iterative/real64_phase_a9b_promotion/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_promotion/compile_spor64_a9b_promotion_anchor.f90",
    "validation/iterative/real64_phase_a9b_promotion/check_phase_a9b_promotion.py",
    "validation/iterative/real64_phase_a9b_promotion/test_phase_a9b_promotion_contract.py",
    "validation/iterative/real64_phase_a9b_promotion/run_phase_a9b_promotion.sh",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_real32_state.f90",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_real64_operator.f90",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_noncontiguous_state.f90",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_int32_counter.f90",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_flat_keyflx.f90",
    "validation/iterative/real64_phase_a9b_promotion/compile_fail_aca_im_extent.f90",
    "validation/iterative/real64_phase_a9b_promotion/expected_module_dependencies.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_aca_unresolved.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_aca_defined.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_a8_unresolved.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_a8_defined.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_adapter_unresolved.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_adapter_defined.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_a9_unresolved.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_a9_defined.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_anchor_unresolved.txt",
    "validation/iterative/real64_phase_a9b_promotion/expected_anchor_defined.txt",
)

PROMOTED_PATHS = frozenset(item["production"] for item in EXPECTED_PROMOTIONS)
ROUTE_TOKENS = (
    "SPOR64_A8",
    "SPOR64_A8_ACA",
    "SPOR64_A9",
    "MCGFFIR64_RANK_ADAPTER",
    "DOORFV64",
    "MCCGF64",
    "MCGFLX64",
    "MCGMRE64",
    "MCGFL164",
    "MCGFCS64",
    "FLU2DR64_CORE",
    "FLUBAL64",
    "FLU2AC64",
)


class PhaseA9bPromotionError(RuntimeError):
    """Raised when B1 changes route/runtime state or weakens compile evidence."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA9bPromotionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(data: dict[str, Any]) -> str:
    payload = json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(data: dict[str, Any]) -> None:
    require(
        set(data) == {
            "schema", "phase", "title", "status", "authority",
            "promotions", "generated_dependency_edges",
            "known_unresolved_production_seams", "link_boundary",
            "unchanged_host_hashes", "next_subgate", "compile_gate",
            "forbidden",
        },
        "manifest top-level fields changed",
    )
    require(
        data["schema"] == "spot-real64-phase-a9b-production-promotion-v1",
        "manifest schema changed",
    )
    require(data["phase"] == "A9b-P", "manifest phase changed")
    require(
        data["title"] == "Byte-identical production-module promotion",
        "manifest title changed",
    )
    require(data["status"] == EXPECTED_STATUS, "status/claim boundary changed")
    require(data["authority"] == EXPECTED_AUTHORITY, "authority changed")
    require(data["promotions"] == EXPECTED_PROMOTIONS, "promotion map changed")
    require(
        data["generated_dependency_edges"] == EXPECTED_DEPENDENCIES,
        "expected dependency edges changed",
    )
    require(
        data["known_unresolved_production_seams"] == EXPECTED_SEAMS,
        "unresolved seam list changed",
    )
    require(
        "forbids linking" in data["link_boundary"]
        and "B2" in data["link_boundary"],
        "link boundary no longer reserves unresolved seams for B2",
    )
    require(
        data["unchanged_host_hashes"] == EXPECTED_HOST_HASHES,
        "protected host hash map changed",
    )
    require(data["next_subgate"] == EXPECTED_NEXT_SUBGATE, "B2 order changed")
    require(data["compile_gate"] == EXPECTED_COMPILE_GATE, "compile gate changed")
    require(data["forbidden"] == EXPECTED_FORBIDDEN, "forbidden list changed")
    require(
        canonical_sha256(data) == EXPECTED_CANONICAL_MANIFEST_SHA256,
        "canonical manifest hash changed",
    )


def validate_promotion_pair(
    validation_bytes: bytes,
    production_bytes: bytes,
    expected_sha256: str,
    label: str,
) -> None:
    require(validation_bytes == production_bytes, f"byte promotion changed: {label}")
    actual = hashlib.sha256(production_bytes).hexdigest()
    require(actual == expected_sha256, f"promotion hash changed: {label}")


def validate_promotions(data: dict[str, Any], root: Path = ROOT) -> None:
    for item in data["promotions"]:
        validation = root / item["validation"]
        production = root / item["production"]
        require(validation.is_file(), f"missing frozen source: {validation}")
        require(production.is_file(), f"missing production source: {production}")
        require(not validation.is_symlink(), f"frozen source is a symlink: {validation}")
        require(not production.is_symlink(), f"production source is a symlink: {production}")
        validate_promotion_pair(
            validation.read_bytes(), production.read_bytes(), item["sha256"],
            item["production"],
        )


def validate_host_hashes(data: dict[str, Any], root: Path = ROOT) -> None:
    for relative, expected in data["unchanged_host_hashes"].items():
        path = root / relative
        require(path.is_file(), f"missing protected host/tool file: {relative}")
        require(not path.is_symlink(), f"protected path is a symlink: {relative}")
        require(sha256(path) == expected, f"protected host/tool changed: {relative}")


def validate_production_path_set(
    tracked_changes: dict[str, str],
    untracked_paths: set[str],
    baseline_paths: set[str],
) -> None:
    touched = set(tracked_changes) | untracked_paths
    require(touched == PROMOTED_PATHS, "src delta is not exactly four promotions")
    require(
        all(status == "A" for status in tracked_changes.values()),
        "an existing production path was edited, deleted or renamed",
    )
    require(
        not (PROMOTED_PATHS & baseline_paths),
        "a promoted source already existed at the frozen baseline",
    )


def _git_lines(arguments: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, text=True, capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"git audit failed: {' '.join(arguments)}")
    require(not result.stderr, f"git audit emitted stderr: {' '.join(arguments)}")
    return [line for line in result.stdout.splitlines() if line]


def validate_production_git_state() -> None:
    diff_lines = _git_lines(
        ["diff", "--name-status", "--no-renames", BASELINE_COMMIT, "--", "src"]
    )
    tracked: dict[str, str] = {}
    for line in diff_lines:
        fields = line.split("\t")
        require(len(fields) == 2, f"unparseable src delta: {line}")
        tracked[fields[1]] = fields[0]
    untracked = set(
        _git_lines(["ls-files", "--others", "--exclude-standard", "--", "src"])
    )
    baseline = set(
        _git_lines(["ls-tree", "-r", "--name-only", BASELINE_COMMIT, "--", "src"])
    )
    validate_production_path_set(tracked, untracked, baseline)


def _fortran_without_comments(label: str, source: str) -> str:
    fixed_form = Path(label).suffix.lower() in {".f", ".for"}
    kept: list[str] = []
    for line in source.splitlines():
        if fixed_form and line and line[0] in "cC*!":
            continue
        if not fixed_form and line.lstrip().startswith("!"):
            continue
        kept.append(line.split("!", 1)[0])
    return "\n".join(kept)


def validate_nonpromoted_source(label: str, source: str) -> None:
    code = _fortran_without_comments(label, source)
    for token in ROUTE_TOKENS:
        require(
            re.search(rf"(?i)\b{re.escape(token)}\b", code) is None,
            f"production route token {token} appeared in {label}",
        )


def validate_no_production_callsites(root: Path = ROOT) -> None:
    for path in sorted((root / "src").iterdir()):
        relative = path.relative_to(root).as_posix()
        if relative in PROMOTED_PATHS or not path.is_file():
            continue
        if path.suffix.lower() not in {
            ".f", ".for", ".f90", ".f95", ".f03", ".f08",
        }:
            continue
        validate_nonpromoted_source(relative, path.read_text(errors="replace"))


def validate_dependency_text(text: str) -> None:
    require(
        text == "\n".join(EXPECTED_DEPENDENCIES) + "\n",
        "generated dependency output is not exact",
    )


def generate_dependency_text(root: Path = ROOT) -> str:
    command = [
        "python3", str(root / "script/make_depend.py"), "--make-deps",
        *[str(root / item["production"]) for item in EXPECTED_PROMOTIONS],
    ]
    result = subprocess.run(
        command, cwd=root, text=True, capture_output=True, check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    require(result.returncode == 0, "make_depend failed")
    require(not result.stderr, "make_depend emitted stderr")
    return result.stdout


def validate_symbol_inventory(name: str, text: str) -> None:
    lines = text.splitlines()
    require(lines, f"empty exact symbol inventory: {name}")
    require(lines == sorted(set(lines)), f"unsorted/duplicate symbol inventory: {name}")
    if name.endswith("_defined.txt"):
        require(
            all(re.fullmatch(r"[A-Z] \S+", line) for line in lines),
            f"malformed defined symbol inventory: {name}",
        )
    else:
        require(
            all(re.fullmatch(r"\S+", line) for line in lines),
            f"malformed unresolved symbol inventory: {name}",
        )
    require(
        all(re.search(r"(?i)(^|_)main(__|_|$)", line) is None for line in lines),
        f"executable entry point admitted by {name}",
    )


def validate_symbol_files(here: Path = HERE) -> None:
    for name in EXPECTED_SYMBOL_FILES:
        path = here / name
        require(path.is_file(), f"missing exact symbol inventory: {name}")
        validate_symbol_inventory(name, path.read_text(encoding="utf-8"))
    a8_unresolved = (here / "expected_a8_unresolved.txt").read_text()
    for seam in ("_spomoc_mccgf_begin_", "_spomoc_set_role_",
                 "_spomoc_publish_", "_spomoc_capture64_"):
        require(seam in a8_unresolved.splitlines(), f"missing unresolved seam: {seam}")


def baseline_makefile_text() -> str:
    result = subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:Makefile"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    require(result.returncode == 0, "cannot read frozen parent Makefile")
    require(not result.stderr, "git show emitted stderr for parent Makefile")
    require(
        hashlib.sha256(result.stdout.encode()).hexdigest()
        == BASELINE_MAKEFILE_SHA256,
        "frozen parent Makefile identity changed",
    )
    return result.stdout


def validate_makefile_text(text: str, baseline: str | None = None) -> None:
    if baseline is None:
        baseline = baseline_makefile_text()
    require(baseline.count(A9A_MAKE_BLOCK) == 1,
            "parent A9a Make block is not unique")
    require(A9B_PROMOTION_MAKE_BLOCK not in baseline,
            "parent Makefile already contains B1 target")
    expected = baseline.replace(
        A9A_MAKE_BLOCK, A9A_MAKE_BLOCK + A9B_PROMOTION_MAKE_BLOCK, 1
    )
    require(
        text == expected,
        "top Makefile is not the frozen parent plus the one isolated B1 block",
    )


def _shell_commands(source: str) -> list[str]:
    commands: list[str] = []
    logical = ""
    for raw in source.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        logical = f"{logical} {stripped}".strip()
        if logical.endswith("\\"):
            logical = logical[:-1].rstrip()
            continue
        commands.append(logical)
        logical = ""
    require(not logical, "runner has an unterminated continuation")
    return commands


def validate_runner_text(source: str, verify_hash: bool = True) -> None:
    commands = _shell_commands(source)
    joined = "\n".join(commands)
    if verify_hash:
        require(
            hashlib.sha256(source.encode()).hexdigest()
            == EXPECTED_RUNNER_SHA256,
            "runner hash freeze changed",
        )
    require(source.startswith("#!/bin/sh\nset -eu\n"), "runner is not strict POSIX shell")
    require("EXPECTED_FC_BANNER=" in source, "compiler identity is not locked")
    require("uname -s" in source and "uname -m" in source, "platform is not locked")
    require("CHECKED_FLAGS=" in source, "strict compile flags missing")
    require('RECEIPT="$HERE/phase_a9b_promotion_receipt.sha256"' in source,
            "B1 receipt path is not locked")
    require('shasum -a 256 -c "$RECEIPT"' in source,
            "B1 receipt is not verified before compilation")
    invocation_prefix = (
        r"^\s*(?:(?:if|elif|while|until)\s+)?(?:!\s*)?"
        r"(?:(?:command|exec)\s+)*(?:env(?:\s+[A-Za-z_]\w*=\S+)*\s+)?"
    )
    direct_tool = re.compile(
        invocation_prefix
        + r'''["']?(?:[^\s"']*/)?(?:ld|ar|cc|gcc(?:-\d+)?|'''
        + r'''clang(?:-\d+)?|gfortran(?:-\d+)?|ifort|ifx|'''
        + r'''nvfortran|flang(?:-new)?)["']?(?=\s|$)''',
        re.IGNORECASE,
    )
    require(not any(direct_tool.match(command) for command in commands),
            "runner invokes a direct linker/compiler path")
    configurable_linker = re.compile(
        invocation_prefix
        + r'''["']?\$(?:\{)?(?:LD|CC)(?:\})?["']?(?=\s|$)''',
        re.IGNORECASE,
    )
    require(not any(configurable_linker.match(command) for command in commands),
            "runner invokes a configurable linker or C compiler")
    path_execution = re.compile(
        invocation_prefix + r'''["']?(?:/|\./)[^\s"']+["']?(?=\s|$)''',
        re.IGNORECASE,
    )
    require(not any(path_execution.match(command) for command in commands),
            "runner directly executes a filesystem artifact")
    build_execution = re.compile(
        invocation_prefix
        + r'''["']?\$(?:\{)?BUILD_DIR(?:\})?(?:/|["']/)[^\s]*''',
        re.IGNORECASE,
    )
    require(not any(build_execution.match(command) for command in commands),
            "runner executes a build-directory artifact")
    compiler_invocation = re.compile(
        invocation_prefix
        + r'''["']?\$(?:\{)?FC(?:\})?["']?(?=\s|$)''',
        re.IGNORECASE,
    )
    compiler_commands = [
        command for command in commands if compiler_invocation.match(command)
    ]
    require(len(compiler_commands) == 2,
            "runner compiler invocation count is not exact")
    for command in compiler_commands:
        require(re.search(r"(^|\s)-c(\s|$)", command) is not None,
                "Fortran compiler command without -c")
        require(
            not any(operator in command for operator in (";", "&&", "||")),
            "compiler command can chain a link or execution",
        )
    require(
        source.count('FC_BANNER=$("$FC" --version | sed -n \'1p\')') == 1,
        "compiler version query is not exact",
    )
    require("run_phase_a8.sh" not in source, "A8 runner replayed")
    require("run_phase_a9a.sh" not in source, "A9a runner replayed")
    require(re.search(r"(?m)^\s*(?:make|gmake)\b", source) is None,
            "runner invokes another make target")
    require(re.search(r"(?m)^\s*(?:sh|bash|zsh)\b", source) is None,
            "runner invokes a secondary shell")
    require(re.search(r"(?i)(?:^|[\s/])dragon(?:[\s./'\"]|$)", joined) is None,
            "runner invokes Dragon")
    require("--make-deps" in source, "generated dependency audit missing")
    require("expected_module_dependencies.txt" in source,
            "dependency output is not compared exactly")
    for item in EXPECTED_PROMOTIONS:
        require(item["production"] in source,
                f"promoted source absent from runner: {item['production']}")
    for name in EXPECTED_NEGATIVES:
        require(source.count(name) == 1, f"negative fixture missing/duplicated: {name}")
    require(source.count("-fdefault-real-8") == 1,
            "default-REAL rejection loop changed")
    require("for source_stem in SPOR64_A8_ACA SPOR64_A8 " in source,
            "default-REAL loop does not cover A8 production sources")
    require("MCGFFIR64_RANK_ADAPTER SPOR64_A9" in source,
            "default-REAL loop does not cover all promoted sources")
    require("nm -g" in source and "audit_nm_lines" in source,
            "global symbol audit missing")
    require("cmp -s \"$HERE/expected_${stem}_${symbol_class}.txt\"" in source,
            "symbol inventories are not compared exactly")
    require("a9b_promotion_all_nm.txt" in source,
            "combined entry-point audit missing")
    require("OBJECT-LINKS=0 EXECUTABLES=0 OBJECT-EXECUTIONS=0" in source,
            "zero-link terminal accounting missing")
    require("TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0" in source,
            "zero-transport terminal accounting missing")
    require("PRODUCTION-ROUTE-CONNECTED=false" in source,
            "disconnected-route terminal status missing")


def validate_docs_text(readme: str, root_readme: str, iterative: str) -> None:
    lower = readme.lower()
    compact = re.sub(r"\s+", " ", lower)
    require("production-objects-available-compile-only" in lower,
            "permitted claim missing from README")
    require("does not authorize linking" in lower,
            "README no longer forbids linking")
    require("no `r64` keyword is parsed" in lower,
            "README no longer states parser absence")
    require("default production route is unchanged" in lower,
            "README no longer states route disconnection")
    require(
        "it does not establish a continuous production real64 lane, "
        "radial convergence, physical accuracy or outer picard convergence."
        in compact,
        "README no longer denies continuous-lane/convergence evidence",
    )
    for document, label in (
        (readme, "B1"), (root_readme, "root"), (iterative, "iterative")
    ):
        require("make spot-real64-phase-a9b-promotion" in document,
                f"{label} README omits the B1 gate command")
    combined = "\n".join((readme, root_readme, iterative)).lower()
    overclaims = (
        "continuous-real64-lane=true",
        "production-route-connected=true",
        "radial-convergence=pass",
        "outer-picard-convergence=pass",
        "physical accuracy established",
    )
    require(not any(item in combined for item in overclaims),
            "README contains an unauthorized runtime/convergence claim")


def receipt_entries(text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "malformed B1 receipt line")
        entries.append((match.group(1), match.group(2)))
    return entries


def validate_receipt(text: str, root: Path = ROOT) -> None:
    entries = receipt_entries(text)
    paths = [path for _, path in entries]
    require(paths == list(EXPECTED_RECEIPT_PATHS),
            "B1 receipt exact ordered scope changed")
    require(len(paths) == len(set(paths)), "duplicate path in B1 receipt")
    require(RECEIPT.relative_to(root).as_posix() not in paths,
            "B1 receipt contains a self-cycle")
    for expected, relative in entries:
        path = root / relative
        require(path.is_file(), f"missing receipt artifact: {relative}")
        require(not path.is_symlink(), f"receipt artifact is a symlink: {relative}")
        require(sha256(path) == expected, f"receipt hash changed: {relative}")


def validate_required_artifacts(here: Path = HERE) -> None:
    required = {
        "README.md", "precision_manifest.json", RUNNER.name, ANCHOR.name,
        RECEIPT.name,
        "expected_module_dependencies.txt", *EXPECTED_NEGATIVES,
        *EXPECTED_SYMBOL_FILES, "check_phase_a9b_promotion.py",
        "test_phase_a9b_promotion_contract.py",
    }
    missing = sorted(name for name in required if not (here / name).is_file())
    require(not missing, f"missing B1 gate artifacts: {missing}")


def run_checks() -> None:
    data = load_manifest()
    validate_manifest(data)
    validate_promotions(data)
    validate_host_hashes(data)
    require(sha256(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256,
            "frozen A9a receipt identity changed")
    validate_production_git_state()
    validate_no_production_callsites()
    dependency_text = (HERE / "expected_module_dependencies.txt").read_text()
    validate_dependency_text(dependency_text)
    validate_dependency_text(generate_dependency_text())
    validate_symbol_files()
    validate_makefile_text(MAKEFILE.read_text(encoding="utf-8"))
    validate_runner_text(RUNNER.read_text(encoding="utf-8"))
    validate_docs_text(
        README.read_text(encoding="utf-8"),
        ROOT_README.read_text(encoding="utf-8"),
        ITERATIVE_README.read_text(encoding="utf-8"),
    )
    validate_required_artifacts()
    validate_receipt(RECEIPT.read_text(encoding="utf-8"))


def main() -> int:
    try:
        run_checks()
    except (OSError, ValueError, PhaseA9bPromotionError) as error:
        print(f"SPOR64 PHASE-A9b-P STATIC FAILURE: {error}")
        return 1
    print("SPOR64 PHASE-A9b-P STATIC PASS")
    print("SPOR64 PHASE-A9b-P BYTE-PROMOTIONS=4 PRODUCTION-CALLSITES=0")
    print("SPOR64 PHASE-A9b-P LINK-AUTHORIZED=false EXECUTION-AUTHORIZED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

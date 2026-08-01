#!/usr/bin/env python3
"""Fail-closed static checker for the A9b SPOMOC ABI subgate."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
README = HERE / "README.md"
RUNNER = HERE / "run_phase_a9b_spomoc_abi.sh"
RECEIPT = HERE / "phase_a9b_spomoc_abi_receipt.sha256"
MAKEFILE = ROOT / "Makefile"
SPOMOC = ROOT / "src/SPOMOC.f90"
BRIDGE = ROOT / "src/SPOMOC_R64_BRIDGE.f90"
A8 = ROOT / "src/SPOR64_A8.f90"
DEPS = ROOT / "src/.dragon_deps.mk"
PARENT_RECEIPT = (
    ROOT / "validation/iterative/real64_phase_a9b_promotion/"
    "phase_a9b_promotion_receipt.sha256"
)

PARENT_COMMIT = "4832b9916b93b109903208751f75928f0e60df4e"
PARENT_RECEIPT_SHA256 = (
    "cddf3cf36c7f1f180b441b785c0efcacd4d4bbfb2709ebb804f5da0933be3c18"
)
LEGACY_CAPTURE_SHA256 = (
    "be158b3e097fc75e019ca5d9c113c29a0be4ca5fa5752cbc1df406de10d45a4a"
)
EXPECTED_RUNNER_SHA256 = (
    "690aab70824e8584b61493e57ba64a821c7f9f19f330179539a29eb4d3e9e88c"
)

SEAMS = (
    "SPOMOC_MCCGF_BEGIN",
    "SPOMOC_SET_ROLE",
    "SPOMOC_PUBLISH",
    "SPOMOC_CAPTURE64",
)
HOST_HASHES = {
    "src/FLUGPI.f": "0155090fc67f38184c4602b0d330cf241a0eeba7f82c203fc25529267b5401ac",
    "src/FLU.f": "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0",
    "src/FLUDRV.f": "6bfd74d6cb473619bcf6130fc723502d348b6a3e76da86e5d03934207b3e4934",
    "src/FLU2DR.f": "edd308054f2977999591a1e9df173212da1a7cb4a6519042295a96fd2c8bbc39",
    "src/XDRTA2.f": "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
}
PROMOTED_HASHES = {
    "src/SPOR64_A8_ACA.f90": "a0138a9ad863ef0c6e6eb7c51520d568ee20b6b26c79c332c374f6ba3f09c115",
    "src/SPOR64_A8.f90": "eaa8110ce17e109db22e93a95d2b8d5495edfd57c18b1aa8676bc2cdaba9e8d7",
    "src/MCGFFIR64_RANK_ADAPTER.f90": "b0f71b95d01e72fe873eae197549ad10cd7f27fca2e3f0e640e7460a2ea4ace7",
    "src/SPOR64_A9.f90": "f0ec2c7292986e4c048bf78108df3a3b8609ad393b77e0012a1a572a5d5c9b4a",
    "script/make_depend.py": "63e26ac26902eeafa062f656565a1fc6f8a972b11bebf68e228095b757467b64",
}
SUPPORT_HASHES = {
    "src/MCCGF.f": "621fba6d02d1b1efae2d6d6db8e61d1463a3a24bcf4d0efe3579bfba97c55546",
    "src/MCGFL1.f": "6701db8972bd92e339d99879787a126f1ce38b72936852ba331259877894df9f",
    "src/MCGMRE.f": "61f71a4873a744608d429eaccc61807d76b5b50a3d2c10213734bb5b26bf1379",
    "src/Makefile": "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
    "Ganlib/src/filmod.f90": "cbc2135097e17b4ea6312b87e0fbcfef6c69a96cc39a8ac1b02c52b872865ec3",
    "Ganlib/src/LCMAUX.f90": "25349f228eb258ea168ba73d291b69c7484709fe282c3cd882f6e0c1a3197ef6",
    "Ganlib/src/lcmmod.f90": "06be7716b58cf0f5bcf1e8dec3a0b8efef41daa887ed81db0307d692dcc33ab9",
    "Ganlib/src/LCMTLC.f90": "8ede84d2b5d3d3c7cae5656458ac2ca73c989015eb7eb5a3ddd78daf07326f45",
    "Ganlib/src/OPNMOD.f90": "da771cda350e0f3375b28b2ab8daf8f9266c9b40c6dc1ef48837c839f7f01a5d",
    "Ganlib/src/XDREED.f90": "c9e3e8b19e06a9ad523bbf1f86a22854b809161dfac6fc1aea4a5045a1f67c0a",
    "Ganlib/src/ganlib.f90": "602d69856e85e0d89f6e9f4f69b18a152569ebba624b8a459a2e17c9251e0a1d",
}
EXPECTED_STATUS = {
    "classification": "PRODUCTION-COMPILE-ONLY-SPOMOC-ABI-CLOSURE",
    "permitted_claim": "A8-SPOMOC-EXTERNAL-SYMBOLS-DEFINED-COMPILE-ONLY",
    "spomoc_capture64_body_compiled": True,
    "a8_external_seams_defined": True,
    "legacy_capture_changed": False,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "r64_parser_implemented": False,
    "spomoc_begin64_implemented": False,
    "host_ingress_implemented": False,
    "xdrta2_epoch_validated": False,
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
MAKE_BLOCK = (
    ".PHONY: spot-real64-phase-a9b-spomoc-abi\n"
    "spot-real64-phase-a9b-spomoc-abi :\n"
    "\tsh validation/iterative/real64_phase_a9b_spomoc_abi/"
    "run_phase_a9b_spomoc_abi.sh\n"
)
EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_promotion/phase_a9b_promotion_receipt.sha256",
    "Ganlib/src/filmod.f90",
    "Ganlib/src/LCMAUX.f90",
    "Ganlib/src/lcmmod.f90",
    "Ganlib/src/LCMTLC.f90",
    "Ganlib/src/OPNMOD.f90",
    "Ganlib/src/XDREED.f90",
    "Ganlib/src/ganlib.f90",
    "src/.dragon_deps.mk",
    "src/Makefile",
    "src/SPOMOC.f90",
    "src/SPOMOC_R64_BRIDGE.f90",
    "src/SPOR64_A8_ACA.f90",
    "src/SPOR64_A8.f90",
    "src/MCGFFIR64_RANK_ADAPTER.f90",
    "src/SPOR64_A9.f90",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLU2DR.f",
    "src/XDRTA2.f",
    "src/MCCGF.f",
    "src/MCGFL1.f",
    "src/MCGMRE.f",
    "script/make_depend.py",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "validation/iterative/real64_phase_a9b_spomoc_abi/README.md",
    "validation/iterative/real64_phase_a9b_spomoc_abi/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_spomoc_abi/check_phase_a9b_spomoc_abi.py",
    "validation/iterative/real64_phase_a9b_spomoc_abi/test_phase_a9b_spomoc_abi_contract.py",
    "validation/iterative/real64_phase_a9b_spomoc_abi/run_phase_a9b_spomoc_abi.sh",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_real32_capture.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_real32_source.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_rank1_capture.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_integer_nconv.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_int64_ngind.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_integer_cyclic.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/compile_fail_real32_bridge.f90",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_module_dependencies.txt",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_spomoc_defined.txt",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_spomoc_unresolved.txt",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_bridge_defined.txt",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_bridge_unresolved.txt",
    "validation/iterative/real64_phase_a9b_spomoc_abi/expected_a8_spomoc_unresolved.txt",
)


class GateError(RuntimeError):
    """Raised when the subgate becomes wider or weaker than frozen."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def routine_region(text: str, name: str) -> str:
    match = re.search(
        rf"(?ims)^[ \t]*subroutine\s+{re.escape(name)}\s*\(.*?"
        rf"^[ \t]*end\s+subroutine\s+{re.escape(name)}[ \t]*$",
        text,
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0) + "\n"


def routine_args(text: str, name: str) -> list[str]:
    region = routine_region(text, name)
    header = re.search(
        rf"(?is)^[ \t]*subroutine\s+{re.escape(name)}\s*\((.*?)\)",
        region,
    )
    require(header is not None, f"missing header {name}")
    return [item.strip().lower() for item in header.group(1).replace("&", "").split(",") if item.strip()]


def call_args(text: str, name: str) -> list[str]:
    match = re.search(
        rf"(?is)\bcall\s+{re.escape(name)}\s*\((.*?)\)", text
    )
    require(match is not None, f"missing call {name}")
    return [item.strip().lower() for item in match.group(1).replace("&", "").split(",") if item.strip()]


def check_manifest() -> None:
    data = json.loads(MANIFEST.read_text())
    require(data["schema"] == "spot-real64-phase-a9b-spomoc-abi-v1", "manifest schema")
    require(data["phase"] == "A9b-B2-ABI", "manifest phase")
    require(data["status"] == EXPECTED_STATUS, "manifest status must be exact")
    authority = data["authority"]
    require(authority["parent_commit"] == PARENT_COMMIT, "parent commit")
    require(authority["parent_receipt_sha256"] == PARENT_RECEIPT_SHA256, "parent receipt hash")
    require(data["external_seams"] == list(SEAMS), "ordered seam list")
    capture = data["capture64_contract"]
    require(capture["downcast_or_repromotion"] is False, "capture downcast")
    require(capture["solver_feedback"] is False, "capture feedback")
    bridge = data["bridge_contract"]
    require(bridge["arithmetic"] is False, "bridge arithmetic")
    require(bridge["io"] is False, "bridge I/O")
    require(bridge["ganlib_access"] is False, "bridge GANLIB access")
    require(bridge["mutable_state"] is False, "bridge state")
    require(data["compile_gate"] == {
        "platform": "Darwin-arm64",
        "compiler": "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0",
        "compiler_path": "/opt/homebrew/bin/gfortran",
        "ganlib_interface_bootstrap": "Seven frozen GANLIB module sources are copied and compiled inside the temporary directory; no ignored or prebuilt .mod file is trusted.",
        "compile_working_directory": "the freshly created temporary directory",
        "production_sources_compiled_from_temporary_copies": True,
        "negative_compiles": 8,
        "exact_nm_allowlists": True,
        "links": 0,
        "executions": 0,
    }, "compile gate identity")
    require(len(data["next_subgates"]) == 3, "B2a/B2b/B2c split")


def check_frozen_inputs() -> None:
    require(digest(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256, "parent receipt changed")
    for rel, expected in {**HOST_HASHES, **PROMOTED_HASHES, **SUPPORT_HASHES}.items():
        require(digest(ROOT / rel) == expected, f"frozen input changed: {rel}")
    for rel in HOST_HASHES:
        text = (ROOT / rel).read_text(errors="replace")
        require(not re.search(r"(?i)\bR64\b|SPOR64|SPOMOC_CAPTURE64", text), f"host route changed: {rel}")


def check_spomoc() -> None:
    text = SPOMOC.read_text()
    legacy = routine_region(text, "SPOMOC_CAPTURE")
    require(hashlib.sha256(legacy.encode()).hexdigest() == LEGACY_CAPTURE_SHA256, "legacy capture changed")
    require(len(re.findall(r"(?i)public\s*::\s*SPOMOC_CAPTURE64", text)) == 1, "CAPTURE64 public count")
    region = routine_region(text, "SPOMOC_CAPTURE64")
    require(routine_args(text, "SPOMOC_CAPTURE64") == [
        "ngeff", "ngind", "nun", "qfr", "eval", "source", "raw", "nconv"
    ], "CAPTURE64 argument order")
    compact = canonical(region)
    for declaration in (
        "REAL(REAL64),INTENT(IN)::QFR(NUN,NGEFF),EVAL(NUN,NGEFF)",
        "REAL(REAL64),INTENT(IN)::SOURCE(NUN,NGEFF),RAW(NUN,NGEFF)",
        "LOGICAL,INTENT(IN)::NCONV(NGEFF)",
    ):
        require(declaration in compact, f"CAPTURE64 declaration: {declaration}")
    require("REAL(REAL32)" not in compact, "CAPTURE64 REAL32 dummy")
    executable = region[region.lower().index("    if (.not. spomoc_active()) return"):]
    require(not re.search(r"(?i)\breal\s*\(", executable), "CAPTURE64 conversion")
    require("CALLSPOMOC_CAPTURE(" not in compact, "CAPTURE64 legacy call")
    for name, actual in (
        ("SPOT-M-QFR", "QFR(:,I)"),
        ("SPOT-M-EVAL", "EVAL(:,I)"),
        ("SPOT-M-SRC", "SOURCE(:,I)"),
        ("SPOT-M-RAW", "RAW(:,I)"),
    ):
        expected = f"CALLLCMPUT(GROUP_DIR,'{name}',REQUIRED_UNKNOWNS,4,{actual})"
        require(expected in compact, f"direct type-4 write: {name}")
        require(f"IEEE_IS_FINITE({actual})" in compact, f"finite check: {name}")
    for guard in (
        "IF(.NOT.SPOMOC_ACTIVE())RETURN",
        "IF(.NOT.MCCGF_SEEN)CALLFAIL('MCCGFCONTEXTMISSING')",
        "IF(CURRENT_ROLE/=1)RETURN",
        "IF(TUPLE_WRITTEN)CALLFAIL('PRIMARYTUPLEOVERWRITEATTEMPTED')",
        "IF(CURRENT_ITERATION/=1)CALLFAIL('FIRSTPRIMARYSTEPREQUIRED')",
        "IF(NGEFF/=REQUIRED_GROUPS)CALLFAIL('CAPTURENGEFFDIFFERS')",
        "IF(NUN/=REQUIRED_UNKNOWNS)CALLFAIL('CAPTURENUNDIFFERS')",
        "IF(.NOT.ALL(NCONV))CALLFAIL('ALLGROUPSMUSTREMAINACTIVE')",
        "IF(IG/=I)CALLFAIL('CAPTURENGINDDIFFERS')",
    ):
        require(guard in compact, f"CAPTURE64 guard: {guard}")
    require(compact.count("CALLLCMPUT(") == 7, "CAPTURE64 exact write count")
    forbidden = r"(?i)\b(relax|alpha|aitken|anderson|clip|floor|tune|toleran|transport|mocik3|mcgfcf|mcgfst)\b"
    require(not re.search(forbidden, region), "CAPTURE64 gained model/solver logic")
    legacy_exec = canonical(legacy)
    capture64_exec = canonical(region)
    legacy_exec = legacy_exec[legacy_exec.index("IF(.NOT.SPOMOC_ACTIVE())RETURN"):]
    capture64_exec = capture64_exec[capture64_exec.index("IF(.NOT.SPOMOC_ACTIVE())RETURN"):]
    legacy_exec = legacy_exec.replace("QFR64=REAL(QFR(:,I),REAL64)", "")
    legacy_exec = legacy_exec.replace("EVAL64=REAL(EVAL(:,I),REAL64)", "")
    legacy_exec = legacy_exec.replace("QFR64", "QFR(:,I)")
    legacy_exec = legacy_exec.replace("EVAL64", "EVAL(:,I)")
    legacy_exec = legacy_exec.replace("ENDSUBROUTINESPOMOC_CAPTURE", "")
    capture64_exec = capture64_exec.replace("ENDSUBROUTINESPOMOC_CAPTURE64", "")
    require(
        capture64_exec == legacy_exec,
        "CAPTURE64 state machine drifted from legacy after removing promotions",
    )


def check_bridge() -> None:
    text = BRIDGE.read_text()
    declarations = re.findall(r"(?im)^subroutine\s+(SPOMOC_[A-Z0-9_]+)\s*\(", text)
    require(tuple(declarations) == SEAMS, "bridge routine set/order")
    a8_text = A8.read_text()
    for name in SEAMS:
        require(routine_args(text, name) == routine_args(a8_text, name), f"A8/bridge ABI args: {name}")
        region = routine_region(text, name)
        compact = canonical(region)
        module_alias = f"{name}_MODULE"
        require(f"ONLY:{module_alias}=>{name}" in compact, f"renamed module import: {name}")
        calls = [item.lower() for item in re.findall(
            r"(?i)\bcall\s+([a-z][a-z0-9_]*)\s*\(", region
        )]
        require(calls == [module_alias.lower()], f"single forward call: {name}")
        require(
            call_args(region, module_alias) == routine_args(text, name),
            f"identity argument forwarding: {name}",
        )
    capture = canonical(routine_region(text, "SPOMOC_CAPTURE64"))
    require("REAL(REAL64),INTENT(IN)::QFR64(NUN,NGEFF),EVAL64(NUN,NGEFF)" in capture, "bridge QFR/EVAL kind")
    require("REAL(REAL64),INTENT(IN)::SOURCE64(NUN,NGEFF),RAW64(NUN,NGEFF)" in capture, "bridge source/raw kind")
    require("REAL(REAL32)" not in capture, "bridge REAL32 payload")
    forbidden = r"(?i)\b(save|common|allocate|deallocate|read|write|open|rewind|lcm[a-z0-9_]*|relax|alpha|clip|floor|value|optional|pointer|allocatable|bind\s*\()\b"
    require(not re.search(forbidden, text), "bridge gained state, I/O, GANLIB or arithmetic")
    require(
        not re.search(r"(?im)^[ \t]*(if|do|select|where|associate|block)\b", text),
        "bridge gained control flow",
    )
    require(
        not re.search(r"(?im)^[ \t]*[a-z][a-z0-9_%()]*[ \t]*=(?!=|>)", text),
        "bridge gained assignment",
    )


def check_build_boundary() -> None:
    deps = DEPS.read_text()
    bridge_edges = [
        line for line in deps.splitlines()
        if line.startswith("SPOMOC_R64_BRIDGE.o:")
    ]
    require(
        bridge_edges == ["SPOMOC_R64_BRIDGE.o: SPOMOC.o"],
        "bridge dependency edge",
    )
    make = MAKEFILE.read_text()
    require(make.count(MAKE_BLOCK) == 1, "isolated Make target")
    target = re.findall(
        r"(?m)^spot-real64-phase-a9b-spomoc-abi\s*:(.*)\n((?:\t.*\n)*)",
        make,
    )
    require(len(target) == 1, "unique Make target")
    require(target[0][0].strip() == "", "Make target prerequisites")
    require(
        target[0][1] == (
            "\tsh validation/iterative/real64_phase_a9b_spomoc_abi/"
            "run_phase_a9b_spomoc_abi.sh\n"
        ),
        "Make target recipe",
    )
    require(
        make.count(".PHONY: spot-real64-phase-a9b-spomoc-abi\n") == 1,
        "Make phony declaration",
    )
    stripped = make.replace(MAKE_BLOCK, "")
    require("spot-real64-phase-a9b-spomoc-abi" not in stripped, "extra Make target reference")
    first_target = re.search(r"(?m)^([A-Za-z0-9_.-]+)\s*:", make)
    require(first_target is not None and first_target.group(1) == "all", "default target changed")
    runner = RUNNER.read_text()
    require(digest(RUNNER) == EXPECTED_RUNNER_SHA256, "runner hash changed")
    forbidden = (
        "make -C src", "make -C \"$ROOT/src\"", "Dragon", "rdragon",
        "./Dragon", "./rdragon", "ld ", "/usr/bin/ld", " ar ",
        "exec ", "LCMGET", "LCMGPD", "REWIND", "transport",
    )
    for token in forbidden:
        require(token not in runner, f"runner forbidden token: {token}")
    require(
        runner.count("FC=/opt/homebrew/bin/gfortran\n") == 1,
        "frozen absolute compiler path",
    )
    require("${FC:-" not in runner and "FC=${" not in runner, "FC override forbidden")
    require(runner.count('cd "$BUILD_DIR"\n') == 1, "temporary compile CWD")
    compile_cwd = runner.index('cd "$BUILD_DIR"\n')
    require(
        compile_cwd < runner.index('compile_bootstrap "$BUILD_DIR/'),
        "temporary CWD must precede bootstrap compilation",
    )
    require(
        compile_cwd < runner.index('compile_checked "$BUILD_DIR/SPOMOC.f90"'),
        "temporary CWD must precede production compilation",
    )
    for source_name in (
        "filmod.f90", "LCMAUX.f90", "lcmmod.f90", "LCMTLC.f90",
        "OPNMOD.f90", "XDREED.f90", "ganlib.f90",
    ):
        require(source_name in runner, f"GANLIB bootstrap source: {source_name}")
    for source_name in (
        "SPOMOC.f90", "SPOMOC_R64_BRIDGE.f90", "SPOR64_A8_ACA.f90",
        "SPOR64_A8.f90",
    ):
        require(
            f'compile_checked "$BUILD_DIR/{source_name}"' in runner,
            f"temporary production compile: {source_name}",
        )
        require(
            f'compile_checked "$ROOT/src/{source_name}"' not in runner,
            f"source-directory compile forbidden: {source_name}",
    )
    for line in runner.splitlines():
        stripped_line = line.strip()
        if re.match(r'^(if[ \t]+)?"\$FC"[ \t]+', stripped_line):
            require(" -c " in f" {line} ", "every compiler command must be -c")
        require(
            not re.match(
                r"(?i)^(env[ \t]+|command[ \t]+)?"
                r"(gfortran|gcc|cc|clang|flang|ifort|nvfortran|ld|ar)\b",
                stripped_line,
            ),
            "untracked compiler/linker command",
        )
        require(
            not any(token in line for token in ('"$CC"', '"$LD"', '"$AR"')),
            "untracked compiler/linker variable",
        )


def check_docs() -> None:
    combined = README.read_text() + (ROOT / "README.md").read_text() + (ROOT / "validation/iterative/README.md").read_text()
    for phrase in (
        "A8-SPOMOC-EXTERNAL-SYMBOLS-DEFINED-COMPILE-ONLY",
        "PRODUCTION-ROUTE-CONNECTED=false",
        "CONTINUOUS-REAL64-LANE=false",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(phrase in combined, f"documentation boundary: {phrase}")
    local = README.read_text()
    require("does not expose a selector" in local, "selector disclaimer")
    require("does not link or execute" in local, "execution disclaimer")


def check_receipt_shape() -> None:
    lines = [line for line in RECEIPT.read_text().splitlines() if line]
    require(len(lines) == len(set(lines)), "duplicate receipt line")
    paths = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "receipt syntax")
        rel = match.group(2)
        paths.append(rel)
        require(not rel.startswith("/"), "receipt path must be relative")
        path = ROOT / rel
        require(path.is_file(), f"receipt missing file: {rel}")
        require(digest(path) == match.group(1), f"receipt hash mismatch: {rel}")
    require(tuple(paths) == EXPECTED_RECEIPT_PATHS, "receipt scope/order changed")


def main() -> None:
    check_manifest()
    check_frozen_inputs()
    check_spomoc()
    check_bridge()
    check_build_boundary()
    check_docs()
    check_receipt_shape()
    print("SPOR64 PHASE-A9b SPOMOC-ABI STATIC CONTRACT PASS")


if __name__ == "__main__":
    try:
        main()
    except (GateError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(f"SPOR64 PHASE-A9b SPOMOC-ABI FAILURE: {exc}")

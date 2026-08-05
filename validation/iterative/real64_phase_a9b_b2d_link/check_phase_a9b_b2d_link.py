#!/usr/bin/env python3
"""Fail-closed source and release checker for the B2d production-link seam."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BRIDGE = ROOT / "src/SPOR64_GANLIB_ABI.f90"
A8 = ROOT / "src/SPOR64_A8.f90"
RUNNER = HERE / "run_phase_a9b_b2d_link.sh"
MANIFEST = HERE / "precision_manifest.json"
RECEIPT = HERE / "phase_a9b_b2d_link_receipt.sha256"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2c_publication/"
    "phase_a9b_b2c_publication_receipt.sha256"
)

BRIDGE_SHA256 = "b65b5e1f12c5ca865a207c859c7f450f65cc11a0c72e6580746d93ec001e57bc"
A8_SHA256 = "eaa8110ce17e109db22e93a95d2b8d5495edfd57c18b1aa8676bc2cdaba9e8d7"
PARENT_RECEIPT_SHA256 = (
    "a8038df5630a348004861cdb3e92ee6d2b032ccc5271076b76158c37dffa8bd0"
)
RUNNER_SHA256 = "970abd6635e6879a1384a0497d894dc3d010ba39374984d456758844631d290e"

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_b2c_publication/phase_a9b_b2c_publication_receipt.sha256",
    "Ganlib/lib/Darwin_arm64/libGanlib.a",
    "Utilib/lib/Darwin_arm64/libUtilib.a",
    "Ganlib/src/Makefile",
    "Utilib/src/Makefile",
    "Trivac/src/Makefile",
    "script/make_depend.py",
    "src/SPOR64_A8.f90",
    "src/SPOR64_B2B.f90",
    "src/SPOR64_B2C.f90",
    "src/SPOR64_GANLIB_ABI.f90",
    "src/.dragon_deps.mk",
    "src/Makefile",
    "data/SpotPlaneFS.c2m",
    "validation/iterative/radial_real64_route_protocol.json",
    "validation/iterative/real64_phase_a9b_b2d_link/README.md",
    "validation/iterative/real64_phase_a9b_b2d_link/check_phase_a9b_b2d_link.py",
    "validation/iterative/real64_phase_a9b_b2d_link/expected_bridge_defined.txt",
    "validation/iterative/real64_phase_a9b_b2d_link/expected_bridge_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2d_link/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2d_link/run_phase_a9b_b2d_link.sh",
    "validation/iterative/real64_phase_a9b_b2d_link/test_phase_a9b_b2d_link_contract.py",
    "validation/iterative/real64_phase_a9b_b2d_link/test_spor64_ganlib_abi.f90",
)


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_only(text: str) -> str:
    kept: list[str] = []
    for raw in text.splitlines():
        quote: str | None = None
        line: list[str] = []
        index = 0
        while index < len(raw):
            char = raw[index]
            if quote is not None:
                line.append(char)
                if char == quote:
                    if index + 1 < len(raw) and raw[index + 1] == quote:
                        line.append(raw[index + 1])
                        index += 1
                    else:
                        quote = None
            elif char in "'\"":
                quote = char
                line.append(char)
            elif char == "!":
                break
            else:
                line.append(char)
            index += 1
        kept.append("".join(line))
    return "\n".join(kept)


def compact(text: str) -> str:
    return re.sub(r"\s+", "", code_only(text)).upper()


def check_bridge_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == BRIDGE_SHA256,
            "bridge source hash drift",
        )
    packed = compact(text)
    require(packed.count("SUBROUTINELCMLEN(") == 1, "one LCMLEN wrapper")
    require(packed.count("SUBROUTINELCMGPD(") == 1, "one LCMGPD wrapper")
    require(packed.count("FUNCTIONLCMGIL(") == 1, "one LCMGIL wrapper")
    require(packed.count("ENDSUBROUTINELCMLEN") == 1, "LCMLEN end")
    require(packed.count("ENDSUBROUTINELCMGPD") == 1, "LCMGPD end")
    require(packed.count("ENDFUNCTIONLCMGIL") == 1, "LCMGIL end")
    require(
        packed.count("USEGANLIB,ONLY:GANLIB_LCMLEN=>LCMLEN") == 1,
        "LCMLEN module alias",
    )
    require(
        packed.count("USEGANLIB,ONLY:GANLIB_LCMGPD=>LCMGPD") == 1,
        "LCMGPD module alias",
    )
    require(
        packed.count("USEGANLIB,ONLY:GANLIB_LCMGIL=>LCMGIL") == 1,
        "LCMGIL module alias",
    )
    require(
        "CALLGANLIB_LCMLEN(IPLIST,NAME,LENGTH,ITYLCM)" in packed,
        "LCMLEN forwarding call",
    )
    require(
        "CALLGANLIB_LCMGPD(IPLIST,NAME,ADDRESS)" in packed,
        "LCMGPD forwarding call",
    )
    require(
        "DIRECTORY=GANLIB_LCMGIL(IPLIST,INDEX)" in packed,
        "LCMGIL forwarding call",
    )
    for forbidden in (
        "SAVE",
        "COMMON",
        "ALLOCATE",
        "DEALLOCATE",
        "LCMPUT",
        "LCMPDL",
        "LCMPTC",
        "LCMDID",
        "LCMLID",
        "FLU2DR",
        "DOORFV",
        "MCCGF",
        "SPOR64_B2C",
    ):
        require(forbidden not in packed, f"bridge contains forbidden {forbidden}")


def check_a8_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == A8_SHA256,
            "frozen A8 source hash drift",
        )
    packed = compact(text)
    require("USEGANLIB" not in packed, "A8 cannot bypass the frozen ABI seam")
    for name in ("LCMLEN", "LCMGPD", "LCMGIL"):
        require(
            len(re.findall(rf"(?:SUBROUTINE|FUNCTION){name}\(", packed)) == 1,
            f"one frozen A8 {name} interface",
        )


def check_manifest_data(data: dict[str, Any]) -> None:
    require(
        data["schema"] == "spot.real64.phase-a9b-b2d.production-link.v1",
        "manifest schema",
    )
    require(
        data["claim"] == "PRODUCTION-DRAGON-LINK-CLOSED-NO-SOLVER-EXECUTION",
        "manifest claim",
    )
    require(
        data["parent"]["commit"]
        == "bf6cb73a93903772c3e7d39a95c1d0a7de7e58d8",
        "parent commit",
    )
    require(
        data["parent"]["receipt_sha256"] == PARENT_RECEIPT_SHA256,
        "parent receipt hash",
    )
    require(data["frozen_a8"]["sha256"] == A8_SHA256, "A8 hash")
    require(
        data["frozen_a8"]["bare_external_consumers"]
        == ["LCMLEN", "LCMGPD", "LCMGIL"],
        "A8 consumer inventory",
    )
    bridge = data["abi_bridge"]
    require(
        bridge["defined_external_symbols"]
        == ["_lcmlen_", "_lcmgpd_", "_lcmgil_"],
        "bridge definitions",
    )
    require(
        bridge["forward_targets"]
        == [
            "___lcmaux_MOD_lcmlen",
            "___lcmaux_MOD_lcmgpd",
            "___lcmaux_MOD_lcmgil",
        ],
        "bridge targets",
    )
    for key in (
        "state",
        "numerical_arithmetic",
        "ganlib_mutation",
        "solver_policy",
        "publication_policy",
    ):
        require(bridge[key] is False, f"bridge scope {key}")
    link = data["link_gate"]
    require(link == {
        "full_dragon_builds": 1,
        "full_dragon_links": 1,
        "dragon_executions": 0,
        "ganlib_bridge_links": 1,
        "ganlib_bridge_synthetic_executions": 1,
        "receipt_checks": 2,
        "tracking_reads": 0,
        "transport_solves": 0,
    }, "link execution inventory")
    scope = data["scope"]
    for key in (
        "solver_equations_changed",
        "terminal_rule_changed",
        "empirical_parameters_added",
        "relaxation_parameters_added",
        "multi_epoch_protocol_added",
    ):
        require(scope[key] is False, f"scope {key}")
    require(
        scope["single_epoch_sufficient_for_bounded_plane1_capture"] is True,
        "single-epoch plane-1 decision",
    )
    status = data["status"]
    require(status["production_executable_linked"] is True, "link status")
    require(status["production_executable_executed"] is False, "execution status")
    require(status["runtime_provenance_validated"] is False, "runtime scope")
    require(
        status["actual_transport_response_validated"] is False,
        "transport scope",
    )
    require(status["radial_convergence"] == "NOT-EVALUATED", "radial scope")
    require(
        status["outer_picard_convergence"] == "NOT-EVALUATED",
        "Picard scope",
    )
    require(
        data["next_gate"]
        == "Before any Dragon execution, prove the one-call host topology and FLUX lifecycle: the shipped fresh-output SpotPlaneFS route is incompatible with B2B's recovered-output admission. Freeze a minimal fresh-output plus read-only FLUX_OLD contract, with no solve, replay, empirical quantity, or epoch machinery.",
        "next gate must close the host lifecycle before execution",
    )


def check_runner_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == RUNNER_SHA256,
            "runner source hash drift",
        )
    require(text.count('make -C "$ROOT/src"') == 1, "one production build")
    require(
        text.count('python3 "$HERE/check_phase_a9b_b2d_link.py"') == 2,
        "receipt must be checked before and after the production build",
    )
    require(
        text.count('-o "$BUILD_DIR/test_spor64_ganlib_abi"') == 1,
        "one harness link target",
    )
    require(
        len(
            re.findall(
                r'^\s*"\$BUILD_DIR/test_spor64_ganlib_abi"\s*>',
                text,
                re.MULTILINE,
            )
        )
        == 1,
        "one explicit harness execution",
    )
    for required in (
        '"$ROOT/src/SPOR64_GANLIB_ABI.f90"',
        '"$ROOT/Ganlib/lib/Darwin_arm64/libGanlib.a"',
        '"$ROOT/Utilib/lib/Darwin_arm64/libUtilib.a"',
        'ar t "$ROOT/src/libDragon.a"',
        'nm -g "$DRAGON"',
        "DRAGON-EXECUTIONS=0",
        "RECEIPT-CHECKS=2",
        "TRACKING-READS=0 TRANSPORT-SOLVES=0",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(required in text, f"runner missing {required}")
    require(
        re.search(r'^\s*"\$DRAGON"(?:\s|$)', text, re.MULTILINE) is None,
        "runner cannot execute Dragon",
    )
    require("DRAGON_BIN=" not in text, "runner cannot delegate a Dragon run")


def check_receipt(text: str | None = None, verify_digests: bool = True) -> None:
    if text is None:
        require(RECEIPT.is_file(), "release receipt missing")
        text = RECEIPT.read_text()
    lines = [line for line in text.splitlines() if line]
    require(len(lines) == len(EXPECTED_RECEIPT_PATHS), "receipt entry count")
    found: list[str] = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "receipt line format")
        claimed, relative = match.groups()
        found.append(relative)
        if verify_digests:
            require(digest(ROOT / relative) == claimed, f"receipt digest {relative}")
    require(tuple(found) == EXPECTED_RECEIPT_PATHS, "receipt path inventory")


def check_repository() -> None:
    for path in (BRIDGE, A8, RUNNER, MANIFEST, RECEIPT, PARENT_RECEIPT):
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    require(digest(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256, "parent receipt")
    check_bridge_text(BRIDGE.read_text())
    check_a8_text(A8.read_text())
    check_manifest_data(json.loads(MANIFEST.read_text()))
    check_runner_text(RUNNER.read_text())
    check_receipt()


if __name__ == "__main__":
    try:
        check_repository()
    except (ContractError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"SPOR64 PHASE-A9b-B2d STATIC FAILURE: {error}")
    print("SPOR64 PHASE-A9b-B2d STATIC PASS")

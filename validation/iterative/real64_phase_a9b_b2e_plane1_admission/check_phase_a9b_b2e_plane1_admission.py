#!/usr/bin/env python3
"""Fail-closed checker for the B2e real plane-1 admission census."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
PROJECT_README = ROOT / "README.md"
RUNNER = HERE / "run_phase_a9b_b2e_plane1_admission.sh"
CANDIDATE = HERE / "SpotPlaneFS_R64_candidate.c2m"
STUBS = HERE / "b2e_noop_stubs.f90"
STRIP = HERE / "b2e_strip_legacy_source.f90"
SCHEMA = HERE / "check_b2e_real_schema.f90"
HARNESS = HERE / "test_b2e_current_admission.f90"
RECEIPT = HERE / "phase_a9b_b2e_plane1_admission_receipt.sha256"

PARENT_RECEIPT_SHA256 = (
    "95d24f9acd6cfa3e6743785db1b3d7286f398fcaa303fc50aca82b15af617562"
)

PRODUCTION_SHA256 = {
    "src/SPOR64_B2B.f90": "d13e9bc467d96d4f5dc0e77bb5c238613fdb1071befbb288543e9df42550d3a5",
    "src/SPOR64_B2C.f90": "c35e247d9612377e072a2bd14de5080c9aceb4f90c2d4fac6cf1150e6538fc45",
    "src/SPOR64_A9.f90": "f0ec2c7292986e4c048bf78108df3a3b8609ad393b77e0012a1a572a5d5c9b4a",
    "src/FLU.f": "b828ef79a0eb8b123dea07e556818c0ef2974020aa571eaddef5ce8dd9831705",
    "src/FLUGPI.f": "316fc41c22e7cc45a3d1877ab9e90d680f63718afe4a697ebad9a7013662141d",
    "src/FLU2DR.f": "edd308054f2977999591a1e9df173212da1a7cb4a6519042295a96fd2c8bbc39",
    "data/SpotPlaneFS.c2m": "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5",
    "data/SpotRefFS.c2m": "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742",
}

ARTIFACTS = {
    "validation/artifacts/iterative-radial-floor/restart_cap.xsm": (
        "7291d8d88b5be07cd570131ea45ce5f283d55a37e3577197626001c59d9b8c89",
        904652,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_macro0.xsm": (
        "6eb2920473f4cb8d27b6377bcb59b42833c8ebf9a0fc57925341d12ccac0a617",
        9878532,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_source.xsm": (
        "6942f61ba2cc7ab0d5cf9a4104959809a388fab441da82730cf64de74a48769f",
        303620,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_system.xsm": (
        "a8797a7d42fdab574eb183bc2ecf0e2b53c992fdd2dd4c61d40c72a53746e599",
        840124,
    ),
    "validation/artifacts/raw-moc-capture/common/restart_track.xsm": (
        "2d868b87e2003c10c09da1ec8f8e6fd97f2a2629a680a46d7f898e2e5e1ed598",
        8080,
    ),
    "validation/artifacts/raw-moc-capture/common/initial_radial_track.bin": (
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
        2275636,
    ),
}

CRITICAL_SHA256 = {
    "candidate": "a1b1952833472d083c7bbf0a64d699ed18248d4029601ee66f5d4e5fcccdb513",
    "stubs": "57f8a791c9bc82abe6527946716b37b052238dd30f58ed088ec04c54a0eb682c",
    "strip": "b3ba1aa53dc25379d5df6e51e3039d8cdf98d7811bc46396dce5025a08467278",
    "schema": "639400dd3f360210805e97ee7bf62d4dbd5403908ba9b0cfcd287ab8ad24a401",
    "harness": "5d6e4ecf327e6618fb13aa3af715f8f10ca6549ff4e2e93894751b38befd9e1d",
    "runner": "860390240bb0d4f7e488beba4b7bda64f83f840219abe35ffe12e6a4a507f6ce",
}

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_b2d_link/phase_a9b_b2d_link_receipt.sha256",
    "README.md",
    "Ganlib/lib/Darwin_arm64/libGanlib.a",
    "Ganlib/lib/Darwin_arm64/modules/ganlib.mod",
    "Utilib/lib/Darwin_arm64/libUtilib.a",
    *PRODUCTION_SHA256.keys(),
    "validation/iterative/radial_floor_prepare.x2m",
    "validation/iterative/radial_real64_route_protocol.json",
    "validation/iterative/raw_moc_capture_run_protocol.json",
    *ARTIFACTS.keys(),
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/README.md",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/SpotPlaneFS_R64_candidate.c2m",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/b2e_noop_stubs.f90",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/b2e_strip_legacy_source.f90",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/check_b2e_real_schema.f90",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/check_phase_a9b_b2e_plane1_admission.py",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/run_phase_a9b_b2e_plane1_admission.sh",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/test_b2e_current_admission.f90",
    "validation/iterative/real64_phase_a9b_b2e_plane1_admission/test_phase_a9b_b2e_plane1_admission_contract.py",
)


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_fortran_comments(text: str, *, fixed_form: bool = False) -> str:
    kept: list[str] = []
    for raw in text.splitlines():
        if fixed_form and raw.startswith(("*", "c", "C")):
            continue
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


def compact_fortran(text: str, *, fixed_form: bool = False) -> str:
    return re.sub(
        r"\s+", "", strip_fortran_comments(text, fixed_form=fixed_form)
    ).upper()


def compact_deck(text: str) -> str:
    kept = [line for line in text.splitlines() if not line.lstrip().startswith("*")]
    return re.sub(r"\s+", "", "\n".join(kept)).upper()


def check_production() -> None:
    for relative, expected in PRODUCTION_SHA256.items():
        require(digest(ROOT / relative) == expected, f"production drift {relative}")
    b2b = compact_fortran((ROOT / "src/SPOR64_B2B.f90").read_text())
    for required in (
        "IF(NENTRY/=6)RETURN",
        "IF(JENTRY(1)/=1)RETURN",
        "IF(.NOT.REC.OR.LIMERG)RETURN",
        "FROZEN_TOL_BITS=INT(Z'348637BD',INT32)",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'SOUR'))RETURN",
        "IF(MACRO_STATE(3)/=1.OR.MACRO_STATE(4)/=NIFIS)RETURN",
        "IPFLUX=KENTRY(1)",
        "JPFLUX=LCMGID(IPFLUX,'FLUX')",
    ):
        require(required in b2b, f"missing current B2B blocker {required}")

    plane = compact_deck((ROOT / "data/SpotPlaneFS.c2m").read_text())
    require(plane.count("FLUX:=FLU:") == 1, "one shipped FLU call")
    call = plane.split("FLUX:=FLU:", 1)[1].split("::", 1)[0]
    require(call == "MACRO0TRACKTRACK_FSYSTEMFSOURCE", "shipped six-entry RHS")
    controls = plane.split("FLUX:=FLU:", 1)[1].split(";", 1)[0]
    for forbidden in ("R64", "INITON", "ACCE", "FLUX_OLD"):
        require(forbidden not in controls, f"shipped host unexpectedly has {forbidden}")

    ref = compact_deck((ROOT / "data/SpotRefFS.c2m").read_text())
    ordered = (
        "FLUX:=RECOVER:SNAP::ITEM<<ISNAP>>;",
        "FLUX_OLD:=FLUX;",
        "FLUX:=DELETE:FLUX;",
        "SYSTEMFLUX:=SPOTPLANEFS",
        "SNAP:=BACKUP:SNAPFLUX::ITEM<<ISNAP>>;",
    )
    positions = [ref.find(token) for token in ordered]
    require(all(position >= 0 for position in positions), "shipped lifecycle tokens")
    require(positions == sorted(positions), "shipped fresh-output lifecycle order")

    flu = compact_fortran((ROOT / "src/FLU.f").read_text(), fixed_form=True)
    flu2dr = compact_fortran((ROOT / "src/FLU2DR.f").read_text(), fixed_form=True)
    require(
        "IF(CXDOOR.EQ.'MCCG')THENNLF=ISTATE(6)NANI=ISTATE(6)" in flu,
        "MCCG active-order source",
    )
    require(
        "DO105IAL=0,MIN(NLF-1,NANIS)" in flu2dr,
        "legacy active scattering upper bound",
    )


def check_candidate_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["candidate"],
            "candidate digest drift",
        )
    packed = compact_deck(text)
    require(packed.count("FLUX:=FLU:") == 1, "one candidate FLU call")
    call = packed.split("FLUX:=FLU:", 1)[1].split("::", 1)[0]
    require(
        call == "MACRO0TRACKTRACK_FSYSTEMFSOURCEFLUX_OLD",
        "candidate seven-entry order",
    )
    controls = packed.split("FLUX:=FLU:", 1)[1].split(";", 1)[0]
    for required in (
        "EDIT0",
        "TYPES",
        "INITON",
        "REBA",
        "EXTE500<<FLU_EPS>>",
        "UNKT<<FLU_EPS>>",
        "THER740<<FLU_EPS>>",
        "ACCE33",
    ):
        require(required in controls, f"candidate controls {required}")
    require(controls.count("R64") == 1, "one candidate R64 selector")
    require(controls.count("<<FLU_EPS>>") == 3, "three candidate tolerance uses")
    require("EPOCH" not in packed, "no premature epoch protocol")


def check_stub_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["stubs"],
            "stub digest drift",
        )
    packed = compact_fortran(text)
    for required in (
        "LOGICALFUNCTIONSPOMOC_ACTIVE()",
        "SUBROUTINEFLU2DR64_CORE(",
        "SUBROUTINESPOR64_B2C_PUBLISH(",
        "SUBROUTINEXDRTA2()",
        "SPOMOC_ACTIVE=.FALSE.",
        "ACCEPTED=.FALSE.",
        "OK=.TRUE.",
    ):
        require(required in packed, f"stub contract {required}")
    for forbidden in (
        "DOORFV",
        "MCCGF",
        "MCGMRE",
        "LCMPUT",
        "LCMDEL",
        "LCMDID",
        "LCMLID",
        "READ(",
    ):
        require(forbidden not in packed, f"stub contains {forbidden}")


def check_strip_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["strip"],
            "strip digest drift",
        )
    packed = compact_fortran(text)
    require(packed.count("CALLLCMDEL(ROOT,'SOUR')") == 1, "one fixture deletion")
    require(packed.count("CALLLCMDEL(") == 1, "only one fixture deletion call")
    for forbidden in ("FLUX", "STATE-VECTOR", "SPOT-R64", "SIGNATURE"):
        require(
            f"CALLLCMDEL(ROOT,'{forbidden}')" not in packed,
            f"strip must not delete {forbidden}",
        )
    for forbidden in ("DOORFV", "MCCGF", "READ("):
        require(forbidden not in packed, f"strip contains {forbidden}")


def check_schema_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["schema"],
            "schema digest drift",
        )
    packed = compact_fortran(text)
    for required in (
        "CALLREQUIRE_RECORD(FLUX,'SOUR',NGRP,10)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'KEYFLX',8,1)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'OPTION',1,3)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'LINK.MACRO',3,3)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'LINK.TRACK',3,3)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'LINK.SYSTEM',3,3)",
        "CALLREQUIRE_ABSENT_OR_RECORD(FLUX,'SPOT-LEAK1D',NGRP,2)",
        "CALLREQUIRE_CHARACTER(SYSTEM,'SIGNATURE','L_PIJ')",
        "CALLREQUIRE_CHARACTER(SOURCE,'SIGNATURE','L_SOURCE')",
        "MACRO_STATE(3)/=3",
        "TRACK_STATE(6)/=1",
        "'SCAT01'",
        "'SCAT02'",
        "NONZERO_P1<=0.OR.NONZERO_P2<=0",
        "ALL(IEEE_IS_FINITE(VALUES))",
        "B2ESOUR-FREE-NEXT-BLOCKER=MACRO0/STATE-VECTOR(3)=3",
    ):
        require(required in packed, f"schema census {required}")
    for forbidden in ("LCMPUT", "LCMDEL", "LCMDID", "LCMLID", "READ("):
        require(forbidden not in packed, f"schema census mutates via {forbidden}")


def check_harness_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["harness"],
            "harness digest drift",
        )
    packed = compact_fortran(text)
    require(packed.count("CALLSPOR64_B2B_INGRESS(") == 1, "one real B2B call")
    for scenario in ("REAL-RESTART", "SOUR-FREE-RESTART", "FRESH-CREATE"):
        require(f"'{scenario}'" in packed, f"harness scenario {scenario}")
    for required in (
        "STATUS/=SPOR64_B2B_ADMISSION_FAILED",
        "XDRTA2_CALLS/=0",
        "CORE_CALLS/=0",
        "PUBLISHER_CALLS/=0",
        "FAKE_TRACK%UNIT=77",
        "FAKE_TRACK%KDI_FILE=C_NULL_PTR",
        "REC=.TRUE.",
        "LIMERG=.FALSE.",
        "REC=.FALSE.",
        "LIMERG=.TRUE.",
        "REC,0,LIMERG,370,8,8,32,1,2,1",
    ):
        require(required in packed, f"harness assertion {required}")
    for forbidden in ("FILOPN", "READ(", "DOORFV", "MCCGF", "DRAGON"):
        require(forbidden not in packed, f"harness contains {forbidden}")


def check_manifest_data(data: dict[str, Any]) -> None:
    require(data["schema"] == "spot.real64.phase-a9b-b2e.current-admission.v1", "manifest schema")
    require(data["claim"] == "CURRENT-HOST-ADMISSION-BLOCKED-BEFORE-SOLVER", "manifest claim")
    require(data["parent"]["commit"] == "f20363f9c99c96a23a6b580de644e0d212b59849", "parent commit")
    require(data["parent"]["receipt_sha256"] == PARENT_RECEIPT_SHA256, "parent receipt")
    require(data["real_artifacts"] == {
        path: {"sha256": sha, "bytes": size}
        for path, (sha, size) in ARTIFACTS.items()
    }, "artifact manifest")
    require(data["observed_blockers"] == {
        "real_restart_has_legacy_SOUR_list": True,
        "real_macro_state_vector_3": 3,
        "current_b2b_required_macro_state_vector_3": 1,
        "real_track_state_vector_6": 1,
        "stored_SCAT01_has_nonzero_values": True,
        "stored_SCAT02_has_nonzero_values": True,
        "legacy_active_scattering_order": 0,
        "legacy_active_order_derivation": (
            "MCCG sets NLF=TRACK/STATE-VECTOR(6)=1 and FLU2DR uses "
            "0:MIN(NLF-1,NANIS)."
        ),
    }, "observed blocker census")
    require(data["current_host"] == {
        "output": "fresh FLUX",
        "entry_count": 6,
        "rhs": ["MACRO0", "TRACK", "TRACK_f", "SYSTEM", "FSOURCE"],
        "passes_FLUX_OLD_to_FLU": False,
        "requests_R64": False,
        "requests_INIT_ON": False,
        "derived_REC": False,
        "derived_LIMERG": True,
    }, "current host census")
    require(data["candidate_contract"] == {
        "status": "VALIDATION-ONLY-NOT-EXECUTED",
        "entry_count": 7,
        "entries": [
            "FLUX", "MACRO0", "TRACK", "TRACK_f", "SYSTEM", "FSOURCE",
            "FLUX_OLD",
        ],
        "access": ["create"] + ["read-only"] * 6,
        "output_seed_distinct": True,
        "derived_REC": False,
        "derived_LIMERG": True,
        "tolerance_argument": "flu_eps",
        "tolerance_binary32_bits": "0x348637bd",
        "tolerance_uses": ["EPSOUT", "EPSUNK", "EPSINR"],
        "controls": {
            "TYPE": "S",
            "INIT": "ON",
            "REBA": "ON",
            "EXTE": 500,
            "THER": 740,
            "ACCE": [3, 3],
            "R64": True,
        },
    }, "candidate contract")
    executed = data["executed_gate"]
    require(executed == {
        "real_b2b_source_links": 1,
        "blocked_admission_scenarios": 3,
        "production_XDRTA2_calls": 0,
        "production_core_calls": 0,
        "production_publisher_calls": 0,
        "Dragon_executions": 0,
        "sequential_tracking_record_reads": 0,
        "transport_solves": 0,
        "original_artifact_mutations": 0,
        "temporary_structural_fixture_mutations": 1,
        "synthetic_descriptor_cases": [
            {"name": "real-restart", "JENTRY1": 1, "REC": True, "LIMERG": False},
            {"name": "sour-free-restart", "JENTRY1": 1, "REC": True, "LIMERG": False},
            {"name": "fresh-create", "JENTRY1": 0, "REC": False, "LIMERG": True},
        ],
    }, "executed gate inventory")
    require(data["scope"] == {
        "production_source_changed": False,
        "solver_equations_changed": False,
        "model_completion_added": False,
        "empirical_parameters_added": False,
        "relaxation_parameters_added": False,
        "epoch_protocol_added": False,
    }, "scope boundary")
    require(data["status"] == {
        "production_execution_authorized": False,
        "runtime_host_descriptors_observed": False,
        "runtime_provenance_validated": False,
        "radial_convergence": "NOT-EVALUATED",
        "outer_picard_convergence": "NOT-EVALUATED",
    }, "status boundary")
    require(data["next_gate"] == (
        "Implement the seven-entry fresh-output/read-only-FLUX_OLD contract "
        "in production with separate read and write owners, validate the scalar "
        "active-order equivalence, and stop again before any production XDRTA2 "
        "or transport execution."
    ), "next gate")


def check_runner_text(text: str, verify_digest: bool = True) -> None:
    if verify_digest:
        require(
            hashlib.sha256(text.encode()).hexdigest() == CRITICAL_SHA256["runner"],
            "runner digest drift",
        )
    require(text.count('python3 "$HERE/check_phase_a9b_b2e_plane1_admission.py"') == 2, "two receipt checks")
    require(text.count('"$ROOT/src/SPOR64_B2B.f90"') == 1, "one real B2B compile")
    for scenario in ("real-restart", "sour-free-restart", "fresh-create"):
        require(text.count(f'"$BUILD_DIR/test_b2e_current_admission" {scenario}') == 1, f"runner case {scenario}")
    for forbidden in (
        '"$ROOT/src/SPOR64_A9.f90"',
        '"$ROOT/src/SPOR64_B2C.f90"',
        '"$ROOT/src/XDRTA2.f"',
        '"$ROOT/bin/Darwin_arm64/Dragon"',
        "DRAGON_BIN=",
        "< *.x2m",
    ):
        require(forbidden not in text, f"runner production execution seam {forbidden}")
    for required in (
        "PRODUCTION-XDRTA2-CALLS=0",
        "PRODUCTION-CORE-CALLS=0",
        "PRODUCTION-PUBLISHER-CALLS=0",
        "DRAGON-EXECUTIONS=0",
        "SEQUENTIAL-TRACKING-RECORD-READS=0",
        "TRANSPORT-SOLVES=0",
        "PRODUCTION-EXECUTION-AUTHORIZED=false",
    ):
        require(required in text, f"runner boundary {required}")


def check_project_readme_text(text: str) -> None:
    normalized = re.sub(r"\s+", " ", text)
    for required in (
        "B2e is the current stop point.",
        "`REC=false, LIMERG=true`",
        "`MACRO0/STATE-VECTOR(3)=3`",
        "stored P1/P2 arrays are finite and nonzero",
        "real64_phase_a9b_b2e_plane1_admission/run_phase_a9b_b2e_plane1_admission.sh",
        "Radial and outer Picard convergence remain `NOT-EVALUATED`.",
    ):
        require(required in normalized, f"project README status {required}")


def check_artifacts() -> None:
    for relative, (expected_hash, expected_size) in ARTIFACTS.items():
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"artifact missing {relative}")
        require(path.stat().st_size == expected_size, f"artifact size {relative}")
        require(digest(path) == expected_hash, f"artifact digest {relative}")


def check_receipt(text: str | None = None, verify_digests: bool = True) -> None:
    if text is None:
        require(RECEIPT.is_file(), "receipt missing")
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
    require(tuple(found) == EXPECTED_RECEIPT_PATHS, "receipt inventory")


def check_repository() -> None:
    parent = ROOT / "validation/iterative/real64_phase_a9b_b2d_link/phase_a9b_b2d_link_receipt.sha256"
    require(digest(parent) == PARENT_RECEIPT_SHA256, "B2d parent receipt")
    check_production()
    check_artifacts()
    check_candidate_text(CANDIDATE.read_text())
    check_stub_text(STUBS.read_text())
    check_strip_text(STRIP.read_text())
    check_schema_text(SCHEMA.read_text())
    check_harness_text(HARNESS.read_text())
    check_manifest_data(json.loads(MANIFEST.read_text()))
    check_runner_text(RUNNER.read_text())
    check_project_readme_text(PROJECT_README.read_text())
    check_receipt()


if __name__ == "__main__":
    try:
        check_repository()
    except (ContractError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"SPOR64 PHASE-A9b-B2e STATIC FAILURE: {error}")
    print("SPOR64 PHASE-A9b-B2e STATIC PASS")

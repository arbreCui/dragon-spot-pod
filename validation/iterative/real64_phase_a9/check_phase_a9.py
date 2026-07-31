#!/usr/bin/env python3
"""Fail-closed static checker for the Phase-A9a outer REAL64 closure."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
CORE = HERE / "SPOR64_A9.f90"
HOST = HERE / "SPOR64_A9_HOST.f90"
RUNNER = HERE / "run_phase_a9a.sh"
README = HERE / "README.md"
RECEIPT = HERE / "phase_a9a_implementation_receipt.sha256"
A8_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a8/phase_a8_implementation_receipt.sha256"
)
MAKEFILE = ROOT / "Makefile"
ROOT_README = ROOT / "README.md"
ITERATIVE_README = ROOT / "validation/iterative/README.md"

BASELINE_COMMIT = "9a284ef0b97cfd4b1700ff4e3ace0a694a24fa07"
EXPECTED_A8_RECEIPT_SHA256 = (
    "5c5d0b118269d111360536d8dc6bdead23ad56b22220cc8ace3e4282ee8377fa"
)

UNFROZEN = "TO-BE-FROZEN-BY-ROOT"
EXPECTED_CANONICAL_SHA256 = (
    "df2e17c59b4ed3e8147d10e3273764b334d0f733d95e53efcb3341995cb88727"
)
EXPECTED_CORE_SHA256 = (
    "f0ec2c7292986e4c048bf78108df3a3b8609ad393b77e0012a1a572a5d5c9b4a"
)
EXPECTED_HOST_SHA256 = (
    "7668543afe5402d8977d48c6e542bfa377847c5de6e795a66b473b0fbafa1b04"
)
EXPECTED_RUNNER_SHA256 = (
    "e0162d745d90b9c97be5b227148ba060d203e27a32c5529c40e6a150b8016639"
)
EXPECTED_README_SHA256 = (
    "31cb4447a5e69524621a36c5e493dce99b0f585e2ed1c5d8ead3b211f6319883"
)

EXPECTED_STATUS = {
    "classification": "FROZEN-IMPLEMENTED-COMPILE-ONLY-OUTER-CLOSURE",
    "outer_mathematics_implemented": True,
    "validation_owned_state": True,
    "compile_only": True,
    "link_authorized": False,
    "execution_authorized": False,
    "production_source_changes": 0,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "host_ingress_implemented": False,
    "archive_implemented": False,
    "runtime_provenance_validated": False,
    "actual_transport_response_validated": False,
    "continuous_real64_lane": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
    "object_links": 0,
    "object_executions": 0,
    "tracking_reads": 0,
    "transport_solves": 0,
    "dragon_runs": 0,
}

EXPECTED_LOCKED_BRANCH = {
    "NGRP": 370,
    "NREG": 8,
    "NSOUT": 6,
    "NUNKNO": 14,
    "NMAT": 8,
    "NSLICE": 8,
    "MAXOUT": 500,
    "MAXINR": 740,
    "NCTOT": 6,
    "NCPTM": 3,
    "ITYPEC": 0,
    "ITPIJ": 1,
    "IPHASE": 1,
    "ILEAK": 0,
    "NLIN": 1,
    "NANI": 1,
    "NFUNL": 1,
    "LREBAL": True,
    "LFORW": True,
    "NUSIGF": "finite numerical zero admitted by A9b before entry",
    "tolerance_binary32_bits": "0x348637bd",
    "tolerance_real64_exact_promotion": "2.4999999936881070e-7",
}

EXPECTED_STATE_SLICES = {
    "1": "old outer flux",
    "2": "present outer flux",
    "3": "new outer flux",
    "4": (
        "current outer source; fixed source on entry and final inner "
        "sweep source on return"
    ),
    "5": "old inner flux",
    "6": "present inner flux",
    "7": "new inner flux",
    "8": "current inner sweep source",
}

EXPECTED_OUTER_ORDER = [
    "slice 4 = FIXED_SOURCE64",
    "XCSOU64(g) = sum_r slice4(KEYFLX(r),g)*real(VOL32(r),real64)",
    "slice 6 = slice 2",
    "inner loop",
    "slice 3 = slice 7",
    "slice 4 = slice 8",
    "EEXT64 = 0 for TYPE S",
    "scheduled FLU2AC64 on slices 1:3",
    "outer scalar-key norm",
    "slice 1 = slice 2; slice 2 = slice 3",
    "strict terminal Boolean",
]

EXPECTED_INNER_ORDER = [
    "slice 7 = slice 6",
    "slice 8 = slice 4",
    "off-group source accumulation",
    "DOORFV64(slice 8, slice 7)",
    "FLUBAL64(slice 7)",
    "scheduled FLU2AC64(slices 5:7)",
    "inner scalar-key norm",
    "slice 5 = slice 6; slice 6 = slice 7",
]

EXPECTED_LEGACY_HASHES = {
    "src/FLU2DR.f":
        "edd308054f2977999591a1e9df173212da1a7cb4a6519042295a96fd2c8bbc39",
    "src/FLUBAL.f":
        "005495631cc8234feb1caf0bfccd8c14634dd847091a63ed6a9cae3c1129c6cc",
    "src/FLU2AC.f":
        "3d8817087d106062eed6c155bca11b10171df322eb8fe15d83398e8cf717895a",
    "Utilib/src/ALSBD.f":
        "b0544742d85154b426f4aa5d6f762b5e2e4d9599988f57929dfe11e51c90d5f5",
}

EXPECTED_NEGATIVES = (
    "compile_fail_real32_state.f90",
    "compile_fail_real32_terminal.f90",
    "compile_fail_real64_operator.f90",
    "compile_fail_noncontiguous_state.f90",
    "compile_fail_flu2ac_element.f90",
    "compile_fail_int32_cutoff.f90",
    "compile_fail_nonlogical_selector.f90",
)

EXPECTED_SYMBOL_FILES = tuple(
    f"expected_{stem}_{kind}.txt"
    for stem in ("core", "host", "anchor")
    for kind in ("unresolved", "defined")
)

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a8/phase_a8_implementation_receipt.sha256",
    "validation/iterative/real64_phase_a8/SPOR64_A8_ACA.f90",
    "validation/iterative/real64_phase_a8/SPOR64_A8.f90",
    "src/FLU2DR.f",
    "src/FLUBAL.f",
    "src/FLU2AC.f",
    "Utilib/src/ALSBD.f",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "validation/iterative/real64_phase_a9/README.md",
    "validation/iterative/real64_phase_a9/precision_manifest.json",
    "validation/iterative/real64_phase_a9/SPOR64_A9.f90",
    "validation/iterative/real64_phase_a9/SPOR64_A9_HOST.f90",
    "validation/iterative/real64_phase_a9/compile_spor64_a9_anchor.f90",
    "validation/iterative/real64_phase_a9/check_phase_a9.py",
    "validation/iterative/real64_phase_a9/test_phase_a9_contract.py",
    "validation/iterative/real64_phase_a9/run_phase_a9a.sh",
    "validation/iterative/real64_phase_a9/compile_fail_real32_state.f90",
    "validation/iterative/real64_phase_a9/compile_fail_real32_terminal.f90",
    "validation/iterative/real64_phase_a9/compile_fail_real64_operator.f90",
    "validation/iterative/real64_phase_a9/compile_fail_noncontiguous_state.f90",
    "validation/iterative/real64_phase_a9/compile_fail_flu2ac_element.f90",
    "validation/iterative/real64_phase_a9/compile_fail_int32_cutoff.f90",
    "validation/iterative/real64_phase_a9/compile_fail_nonlogical_selector.f90",
    "validation/iterative/real64_phase_a9/expected_core_unresolved.txt",
    "validation/iterative/real64_phase_a9/expected_core_defined.txt",
    "validation/iterative/real64_phase_a9/expected_host_unresolved.txt",
    "validation/iterative/real64_phase_a9/expected_host_defined.txt",
    "validation/iterative/real64_phase_a9/expected_anchor_unresolved.txt",
    "validation/iterative/real64_phase_a9/expected_anchor_defined.txt",
)


class PhaseA9Error(RuntimeError):
    """Raised when the A9a contract is incomplete or overstated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA9Error(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(data: dict[str, Any]) -> str:
    payload = json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def fortran_code(source: str) -> str:
    """Strip free-form comments before every semantic source check."""
    return "\n".join(line.split("!", 1)[0] for line in source.splitlines())


def unfolded_statements(source: str) -> list[str]:
    statements: list[str] = []
    buffer = ""
    for raw in fortran_code(source).splitlines():
        line = raw.strip()
        if not line:
            continue
        leading = line.startswith("&")
        trailing = line.endswith("&")
        if leading:
            line = line[1:].lstrip()
        if trailing:
            line = line[:-1].rstrip()
        if buffer:
            buffer += " " + line
        else:
            buffer = line
        if not trailing:
            statements.append(buffer)
            buffer = ""
    require(not buffer, "unterminated Fortran continuation")
    return statements


def normalized_statements(source: str) -> list[str]:
    return [re.sub(r"\s+", " ", item.strip()).upper()
            for item in unfolded_statements(source)]


def dense(source: str) -> str:
    return ";".join(
        re.sub(r"[\s&]+", "", statement.upper())
        for statement in unfolded_statements(source)
    )


def routine_region(source: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        fortran_code(source),
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def call_sites(source: str, name: str) -> list[list[str]]:
    code = fortran_code(source)
    pattern = re.compile(rf"(?i)\bcall\s+{re.escape(name)}\s*\(")
    result: list[list[str]] = []
    for match in pattern.finditer(code):
        depth = 1
        quote = ""
        start = match.end()
        item_start = start
        actuals: list[str] = []
        index = start
        while index < len(code) and depth:
            char = code[index]
            if quote:
                if char == quote:
                    quote = ""
            elif char in ("'", '"'):
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    actuals.append(code[item_start:index])
                    break
            elif char == "," and depth == 1:
                actuals.append(code[item_start:index])
                item_start = index + 1
            index += 1
        require(depth == 0, f"unterminated CALL {name}")
        result.append([re.sub(r"[\s&]+", "", x).upper()
                       for x in actuals])
    return result


def require_order(source: str, tokens: tuple[str, ...], message: str) -> None:
    upper = fortran_code(source).upper()
    position = -1
    for token in tokens:
        found = upper.find(token.upper(), position + 1)
        require(found >= 0, f"{message}: missing {token}")
        require(found > position, f"{message}: reordered {token}")
        position = found


def require_no_hidden_control(source: str) -> None:
    code = fortran_code(source)
    forbidden = (
        r"\bSAVE\b", r"\bCOMMON\b", r"\bEQUIVALENCE\b",
        r"\bPOINTER\b", r"\bTARGET\b", r"\bASSOCIATE\b",
        r"\bIF\s*\(\s*\.(?:FALSE|TRUE)\.\s*\)",
        r"\bREAL\s*\([^\n]*,\s*REAL32\s*\)",
        r"\bRELAX", r"\bDAMP", r"\bAITKEN\b", r"\bANDERSON\b",
        r"\bCLIP", r"\bFLOOR", r"\bFITT?ED\b",
    )
    for pattern in forbidden:
        require(re.search(pattern, code, re.I) is None,
                f"forbidden mutable-state/control construct: {pattern}")
    require(re.search(
        r"(?i)TRANSFER\s*\([^,]*(?:FLUX64|SOURCE64|XCSOU64|AKEEP64)"
        r"[^,]*,\s*0\.0(?:_REAL32)?\s*\)",
        code,
    ) is None, "mutable state bit-transfer to REAL32")


def validate_manifest(data: dict[str, Any], verify_hashes: bool = True) -> None:
    require(data.get("schema") == "spot-real64-phase-a9a-v1", "schema")
    require(data.get("phase") == "A9a", "phase")
    require(data.get("status") == EXPECTED_STATUS, "status claim boundary")
    require(data.get("locked_branch") == EXPECTED_LOCKED_BRANCH,
            "locked branch")
    require(data.get("state_slices") == EXPECTED_STATE_SLICES,
            "eight-slice meanings")

    split = data.get("split", {})
    require(split.get("complete_A9_claim_allowed") is False,
            "A9a cannot claim complete A9")
    require("validation-only" in split.get("reason", "").lower(),
            "split reason")
    require("A9b" in split and "production" in split["A9b"].lower(),
            "A9b production boundary")

    authority = data.get("authority", {})
    require(authority.get("parent_phase") == "A8", "parent phase")
    require(authority.get("parent_commit") == BASELINE_COMMIT,
            "parent commit")
    require(authority.get("parent_receipt_sha256") ==
            EXPECTED_A8_RECEIPT_SHA256, "parent receipt identity")
    require(authority.get("implementation") ==
            "validation/iterative/real64_phase_a9/SPOR64_A9.f90",
            "core authority")
    require(authority.get("selector_seam") ==
            "validation/iterative/real64_phase_a9/SPOR64_A9_HOST.f90",
            "host authority")
    require("validation-only" in authority.get("scope", ""),
            "validation-only authority")

    precision = data.get("precision_contract", {})
    require(precision.get("state_shape") ==
            "FLUX64(NUNKNO,NGRP,NSLICE)", "state shape")
    require(precision.get("mutable_state") ==
            "real(real64), unique local owner", "state owner")
    require(precision.get("control_norms_balance_and_acceleration") ==
            "real(real64)", "REAL64 control path")
    require(precision.get("operator_storage") ==
            "VOL/XSTRC/XSDIA0/ALBEDO/SURFAC/SCAT_OFF are real(real32), read-only",
            "REAL32 stored operators")
    require(precision.get("mutable_real64_to_real32_allowed") is False,
            "mutable downcast forbidden")
    require(precision.get("default_real_assumed") is False,
            "default REAL forbidden")

    handle = data.get("runtime_handle_precondition", {})
    require(handle == {
        "A9a_formal": "JPSYS_GROUP",
        "required_identity":
            "the admitted L_PIJ/GROUP list consumed by A8 DOORFV64, not "
            "the root L_PIJ object",
        "IPTRK_and_IFTRAK": "borrowed at the exact A8 tracking epoch",
        "validated_in_A9a": False,
        "owner": "A9b production ingress and lifecycle gate",
    }, "runtime GROUP-list handle precondition")
    wording = data.get("a7_wording_correction", {})
    require(wording.get("correct_role") ==
            "XCSOU64 is the volume integral of outer source slice 4 "
            "before the inner loop", "XCSOU outer-source role")
    require(wording.get("terminal_source_distinction") ==
            "terminal SOUR is final slice 8 copied to slice 4",
            "terminal source/slice distinction")

    outer = data.get("outer_iteration", {})
    inner = data.get("inner_iteration", {})
    require(outer.get("order") == EXPECTED_OUTER_ORDER,
            "outer operation order")
    require(outer.get("initial_flux") ==
            "slice 2 receives INITIAL_FLUX64; the owner initializes all "
            "storage to defined positive zero and later live copies define "
            "every other slice before use",
            "entry state copy-before-use")
    require(outer.get("akeep_initial") ==
            "all zero, then AKEEP64(5:7)=1; each outer iteration assigns "
            "AKEEP64(3)=1 before any scheduled outer acceleration and then "
            "shifts 1=2, 2=3",
            "acceleration history copy-before-use")
    require(inner.get("order") == EXPECTED_INNER_ORDER,
            "inner operation order")
    require(inner.get("strict_convergence") == "EINR64 < EPSINR64",
            "inner strict comparison")
    require("never accepts" in inner.get("near_schedule", ""),
            "near-inner is not acceptance")
    require(inner.get("cap_state") == "state 3; normal non-accepted return",
            "inner cap semantics")

    offgroup = data.get("offgroup_contract", {})
    require(offgroup.get("coefficient_index") ==
            "IPOS_OFF(m,g)+IJJ_OFF(m,g)-j", "off-group coefficient")
    require("j/=g" in offgroup.get("source_rule", ""),
            "self scattering exclusion")
    require(offgroup.get("self_scatter_addition") is False,
            "no self-scatter addition")
    require(offgroup.get("second_LCM_gather") is False,
            "no second gather")

    rebalancing = data.get("rebalancing", {})
    require(rebalancing.get("solver") == "ALSBD", "ALSBD route")
    require(rebalancing.get("matrix_and_rhs") == "real(real64)",
            "REAL64 balance")
    require(rebalancing.get("solver_failure") ==
            "structural fail-closed; no fallback and no publication",
            "rebalancing failure")

    acceleration = data.get("acceleration", {})
    require(acceleration.get("r1") == "present-old", "R1 formula")
    require(acceleration.get("r2") == "new-present", "R2 formula")
    require(acceleration.get("mu") == "-numerator/denominator",
            "mu formula")
    require(acceleration.get("zero_denominator") ==
            "no division and no acceleration; ZMU64=1",
            "exact-zero acceleration branch")
    require(acceleration.get("schedule") == "MOD(iter-1,6)>=3",
            "acceleration schedule")
    require(acceleration.get("relaxation_or_new_threshold") is False,
            "no new acceleration control")

    norms = data.get("norms", {})
    require(norms.get("group_formula") ==
            "max_r abs(present-new) / max_r abs(new)", "norm formula")
    require(norms.get("zero_denominator") ==
            "structural fail-closed; no flux floor or replacement threshold",
            "zero norm denominator")
    require(norms.get("all_real64") is True, "REAL64 norms")

    terminal = data.get("terminal", {})
    require(terminal.get("exact_boolean") ==
            "EEXT64<EPSOUT64 .and. EUNK64<EPSUNK64 .and. "
            "EINR_LAST64<EPSINR64 .and. IINR_STATE==1 .and. IT>=2",
            "strict terminal Boolean")
    require(terminal.get("eext_type_s") == "+0.0_real64", "TYPE S EEXT")
    require(terminal.get("maxout") ==
            "OK=true and ACCEPTED=false; no publication",
            "outer cap is not convergence")

    selector = data.get("selector_seam", {})
    require(selector.get("default_real64_route") is False,
            "selector default OFF")
    require(selector.get("fallback_after_real64_selection") is False,
            "selector no fallback")
    require(selector.get("orthogonal_to_MOCA") is True,
            "MOCA orthogonality")
    require("not production" in selector.get("scope", "").lower(),
            "abstract selector scope")

    require(data.get("legacy_source_hashes") == EXPECTED_LEGACY_HASHES,
            "legacy formula authority")
    gate = data.get("compile_gate", {})
    require(gate.get("target") == "spot-real64-phase-a9a", "gate target")
    for key in (
        "objects_linked", "executables_built", "objects_executed",
        "prerequisite_runners_executed",
    ):
        require(gate.get(key) == 0, f"compile-only gate: {key}")
    require(gate.get("default_real8_must_fail") is True,
            "default-real8 rejection")
    require(gate.get("exact_nm_allowlists") is True,
            "exact nm inventories")
    require(gate.get("main_symbol_allowed") is False, "no main")
    require(gate.get("negative_contract_count") == len(EXPECTED_NEGATIVES),
            "exact negative-contract count")

    forbidden = data.get("forbidden", [])
    required_forbidden = (
        "production source edit or production route connection",
        "GANLIB ingress or archive write",
        "mutable-state REAL64-to-REAL32 conversion",
        "fallback after REAL64 selection",
        "relaxation, fitted coefficient, clipping, flux floor, tuned cutoff or new tolerance",
        "radial, Picard, Stage-4 or physical-accuracy claim",
    )
    for item in required_forbidden:
        require(item in forbidden, f"missing forbidden action: {item}")

    if verify_hashes:
        for label, value in (
            ("canonical", EXPECTED_CANONICAL_SHA256),
            ("core", EXPECTED_CORE_SHA256),
            ("host", EXPECTED_HOST_SHA256),
            ("runner", EXPECTED_RUNNER_SHA256),
            ("README", EXPECTED_README_SHA256),
        ):
            require(value != UNFROZEN, f"unfrozen {label} hash")
        require(canonical_sha256(data) == EXPECTED_CANONICAL_SHA256,
                "canonical manifest freeze")


def validate_core_source(source: str) -> None:
    code = fortran_code(source)
    upper = code.upper()
    packed = dense(source)
    require(re.search(r"(?im)^\s*MODULE\s+SPOR64_A9\s*$", code) is not None,
            "core module identity")
    require("USE,INTRINSIC::ISO_FORTRAN_ENV,ONLY:" in packed and
            all(name in packed for name in ("REAL32", "REAL64", "INT64")),
            "explicit kind imports")
    require("USESPOR64_A8,ONLY:DOORFV64" in packed,
            "checked A8 boundary")
    require("KIND(1.0)==REAL32" in packed and
            "KIND(0.0D0)==REAL64" in packed, "kind guard")
    for name, value in EXPECTED_LOCKED_BRANCH.items():
        if isinstance(value, int) and not isinstance(value, bool) and name in {
            "NGRP", "NREG", "NSOUT", "NUNKNO", "NMAT", "NSLICE",
            "MAXOUT", "MAXINR", "NCTOT", "NCPTM",
        }:
            require(f"INTEGER,PARAMETER::{name}={value}" in packed,
                    f"frozen core dimension/control: {name}")
    require(packed.count("Z'348637BD'") == 1,
            "one exact frozen tolerance bit pattern")
    require("INTEGER,PARAMETER::IINR_STRICT=1" in packed,
            "strict inner state identity")
    require("INTEGER,PARAMETER::IINR_NEAR=2" in packed and
            "INTEGER,PARAMETER::IINR_CAP=3" in packed,
            "near/cap inner state identities")
    for name in (
        "FLU2DR64_CORE", "FLUBAL64", "FLU2AC64",
        "SPOR64_A9_TERMINAL64", "SPOR64_A9_STATE_PROBE",
        "SPOR64_A9_OPERATOR_PROBE", "SPOR64_A9_COUNTER_PROBE",
    ):
        routine_region(source, name)
        require(re.search(rf"(?i)\bPUBLIC\s*::[^\n]*\b{name}\b", code)
                is not None, f"public {name}")

    require_no_hidden_control(source)
    module_spec = code[:re.search(r"(?i)\bCONTAINS\b", code).start()]
    for statement in normalized_statements(module_spec):
        if re.match(
            r"^(?:REAL|INTEGER|LOGICAL)(?:\s*\([^)]*\))?\s*,",
            statement,
        ):
            require("PARAMETER" in statement,
                    "mutable module state forbidden")
    real64_literals = re.findall(
        r"(?i)(?<![A-Z0-9_])([+-]?(?:\d+(?:\.\d*)?|\.\d+))_REAL64\b",
        code,
    )
    require(set(value.lstrip("+") for value in real64_literals) <=
            {"0.0", "1.0", "10.0"},
            "unfrozen REAL64 literal/new numerical control")
    for token in (
        "LCMGET", "LCMGPD", "LCMPUT", "LCMPDL", "LCMLID", "LCMDID",
        "XDRTA2", "SPOMOC_CAPTURE", "SPOMOC_BEGIN", "SPOD", "PICARD",
        "OPEN(", "READ(", "REWIND", "WRITE(",
    ):
        require(token not in upper, f"host/archive/runtime token in A9a core: {token}")

    core = routine_region(source, "FLU2DR64_CORE")
    core_packed = dense(core)
    require(re.search(
        r"(?is)REAL\s*\(\s*REAL64\s*\).*?ALLOCATABLE.*?FLUX64\s*\(",
        core,
    ) is not None, "unique REAL64 FLUX64 owner")
    require(re.search(r"(?i)ALLOCATE\s*\(\s*FLUX64\s*\(\s*NUNKNO\s*,\s*NGRP\s*,\s*NSLICE\s*\)", core)
            is not None, "exact eight-slice allocation")
    require(len(re.findall(r"(?i)\bALLOCATE\s*\([^\n]*\bFLUX64\s*\(", core)) == 1,
            "FLUX64 allocated exactly once")
    require_order(
        core,
        ("ALLOCATE(FLUX64", "FLUX64 = +0.0_REAL64",
         "FLUX64(:,:,2) = INITIAL_FLUX64", "DO IT = 1, MAXOUT",
         "FLUX64(:,:,4) = FIXED_SOURCE64",
         "FLUX64(:,:,6) = FLUX64(:,:,2)", "DO JT = 1, MAXINR",
         "FLUX64(:,IGDEB:NGRP,7) = FLUX64(:,IGDEB:NGRP,6)",
         "FLUX64(:,IGDEB:NGRP,8) = FLUX64(:,IGDEB:NGRP,4)"),
        "copy-before-use state lifecycle",
    )
    require("AKEEP64=+0.0_REAL64" in core_packed,
            "acceleration history defined")
    require("DOAKEEP_INDEX=5,7" in core_packed and
            "AKEEP64(AKEEP_INDEX)=1.0_REAL64" in core_packed,
            "inner acceleration history initialization")
    for slice_index in (1, 3, 5, 6, 7):
        require(f"FLUX64(:,:,{slice_index})=INITIAL_FLUX64" not in core_packed,
                f"unfrozen eager history initialization: slice {slice_index}")
    eps_checks = (
        "TRANSFER(EPSINR64,0_INT64)/=FROZEN_TOL64_BITS",
        "TRANSFER(EPSUNK64,0_INT64)/=FROZEN_TOL64_BITS",
        "TRANSFER(EPSOUT64,0_INT64)/=FROZEN_TOL64_BITS",
    )
    for check in eps_checks:
        require(check in core_packed, f"exact tolerance admission: {check}")

    required_state_updates = (
        "FLUX64(:,:,4)=FIXED_SOURCE64",
        "FLUX64(:,:,6)=FLUX64(:,:,2)",
        "FLUX64(:,IGDEB:NGRP,7)=FLUX64(:,IGDEB:NGRP,6)",
        "FLUX64(:,IGDEB:NGRP,8)=FLUX64(:,IGDEB:NGRP,4)",
        "FLUX64(:,IG,5)=FLUX64(:,IG,6)",
        "FLUX64(:,IG,6)=FLUX64(:,IG,7)",
        "FLUX64(:,:,3)=FLUX64(:,:,7)",
        "FLUX64(:,:,4)=FLUX64(:,:,8)",
        "FLUX64(:,IG,1)=FLUX64(:,IG,2)",
        "FLUX64(:,IG,2)=FLUX64(:,IG,3)",
    )
    for statement in required_state_updates:
        require(statement in core_packed, f"state update: {statement}")

    core_statements = normalized_statements(core)
    flux_writes = [statement for statement in core_statements
                   if re.match(r"^FLUX64(?:\s*\(|\s*=)", statement)]
    require(flux_writes == [
        "FLUX64 = +0.0_REAL64",
        "FLUX64(:,:,2) = INITIAL_FLUX64",
        "FLUX64(:,:,4) = FIXED_SOURCE64",
        "FLUX64(:,:,6) = FLUX64(:,:,2)",
        "FLUX64(:,IGDEB:NGRP,7) = FLUX64(:,IGDEB:NGRP,6)",
        "FLUX64(:,IGDEB:NGRP,8) = FLUX64(:,IGDEB:NGRP,4)",
        "FLUX64(IND,IG,8) = FLUX64(IND,IG,8) + "
        "REAL(SCAT_OFF32(P,IG),REAL64) * FLUX64(IND,JG,7)",
        "FLUX64(:,IG,5) = FLUX64(:,IG,6)",
        "FLUX64(:,IG,6) = FLUX64(:,IG,7)",
        "FLUX64(:,:,3) = FLUX64(:,:,7)",
        "FLUX64(:,:,4) = FLUX64(:,:,8)",
        "FLUX64(:,IG,1) = FLUX64(:,IG,2)",
        "FLUX64(:,IG,2) = FLUX64(:,IG,3)",
    ], "core exact FLUX64 write set")
    xcsou_writes = [statement for statement in core_statements
                    if re.match(r"^XCSOU64(?:\s*\(|\s*=)", statement)]
    require(xcsou_writes == [
        "XCSOU64 = +0.0_REAL64",
        "XCSOU64(IG) = XCSOU64(IG) + FLUX64(IND,IG,4) * "
        "REAL(VOL32(IR),REAL64)",
    ], "core exact XCSOU64 write set")
    akeep_writes = [statement for statement in core_statements
                    if re.match(r"^AKEEP64(?:\s*\(|\s*=)", statement)]
    require(akeep_writes == [
        "AKEEP64 = +0.0_REAL64",
        "AKEEP64(AKEEP_INDEX) = 1.0_REAL64",
        "AKEEP64(3) = 1.0_REAL64",
        "AKEEP64(1) = AKEEP64(2)",
        "AKEEP64(2) = AKEEP64(3)",
    ], "core exact AKEEP64 write set")

    require("REAL(VOL32(IR),REAL64)" in core_packed,
            "volume exact promotion")
    source_statement = (
        "XCSOU64(IG)=XCSOU64(IG)+FLUX64(IND,IG,4)*"
        "REAL(VOL32(IR),REAL64)"
    )
    require(core_packed.count(source_statement) == 1,
            "exact frozen-source integral")
    require("IF(IGDEB/=1.OR.XCSOU64(1)<=0.0_REAL64)RETURN" in
            core_packed, "strict first-source-group admission")
    require("JG=IJJ_OFF(IBM,IG)" in core_packed and
            "P=IPOS_OFF(IBM,IG)+IJJ_OFF(IBM,IG)-JG" in core_packed and
            "JG=JG-1" in core_packed,
            "off-group packed coefficient identity and descending group")
    require("IF(JG/=IG)" in core_packed,
            "self-scattering exclusion")
    require("REAL(SCAT_OFF32(P,IG),REAL64)" in core_packed,
            "off-group exact promotion")
    offgroup_statement = (
        "FLUX64(IND,IG,8)=FLUX64(IND,IG,8)+"
        "REAL(SCAT_OFF32(P,IG),REAL64)*FLUX64(IND,JG,7)"
    )
    require(core_packed.count(offgroup_statement) == 1,
            "exact off-group source update")
    require("MOD(JT-1,NCTOT)>=NCPTM" in core_packed,
            "inner acceleration schedule")
    require("MOD(IT-1,NCTOT)>=NCPTM" in core_packed,
            "outer acceleration schedule")

    door_calls = call_sites(core, "DOORFV64")
    balance_calls = call_sites(core, "FLUBAL64")
    acceleration_calls = call_sites(core, "FLU2AC64")
    terminal_calls = call_sites(core, "SPOR64_A9_TERMINAL64")
    require(len(door_calls) == 1, "one lexical DOORFV64 site")
    require(len(balance_calls) == 1, "one lexical FLUBAL64 site")
    require(len(acceleration_calls) == 2,
            "one inner and one outer FLU2AC64 site")
    require(terminal_calls == [[
        "EEXT64", "EUNK64", "EINR_LAST64", "EPSOUT64", "EPSUNK64",
        "EPSINR64", "IINR_STATE", "IT", "ACCEPTED",
    ]], "one exact terminal decision site")
    require(door_calls[0][0] == "JPSYS_GROUP",
            "DOORFV64 receives the admitted GROUP-list handle")
    require("FLUX64(:,:,8)" in door_calls[0] and
            "FLUX64(:,:,7)" in door_calls[0],
            "DOORFV64 source/flux slices")
    require("FLUX64(:,:,7)" in balance_calls[0],
            "FLUBAL64 new-inner slice")
    accel_flat = [";".join(call) for call in acceleration_calls]
    require(any("FLUX64(:,:,5:7)" in call and
                "AKEEP64(5:7)" in call for call in accel_flat),
            "inner acceleration direct sections")
    require(any("FLUX64(:,:,1:3)" in call and
                "AKEEP64(1:3)" in call for call in accel_flat),
            "outer acceleration direct sections")
    require_order(
        core,
        (
            "CALL DOORFV64", "CALL FLUBAL64",
            "CALL FLU2AC64", "CALL SCALAR_GROUP_NORM64",
            "FLUX64(:,:,3) = FLUX64(:,:,7)",
            "CALL FLU2AC64", "CALL SCALAR_GROUP_NORM64",
            "FLUX64(:,IG,1) = FLUX64(:,IG,2)",
            "CALL SPOR64_A9_TERMINAL64",
        ),
        "outer lane order",
    )

    state_statements = normalized_statements(core)
    iinr_writes = [statement for statement in state_statements
                   if re.search(r"(?:^|\s)IINR_STATE\s*=", statement)]
    require(iinr_writes == [
        "IINR_STATE = 0",
        "IINR_STATE = IINR_STRICT",
        "IINR_STATE = IINR_NEAR",
        "IF (.NOT. INNER_FINISHED) IINR_STATE = IINR_CAP",
    ], "exact inner terminal-state write set")
    require("IF (EINR64 < EPSINR64) THEN" in state_statements,
            "strict inner convergence condition")
    require("IF (IGDEB > 1 .AND. EINR64 < 10.0_REAL64*EPSINR64) THEN"
            in state_statements, "exact inherited near schedule")
    require("IF (.NOT. INNER_FINISHED) IINR_STATE = IINR_CAP"
            in state_statements, "inner cap state")
    require("IF (GROUP_ERROR64 < EPSINR64 .AND. IGDEB == IG) THEN"
            in state_statements, "converged-prefix admission")
    require(state_statements.count("IGDEB = IGDEB + 1") == 1,
            "converged-prefix single increment")
    require_order(
        core,
        ("IF (GROUP_ERROR64 < EPSINR64 .AND. IGDEB == IG) THEN",
         "IGDEB = IGDEB + 1", "IF (EINR64 < EPSINR64) THEN",
         "IINR_STATE = IINR_STRICT",
         "IF (IGDEB > 1 .AND. EINR64 < 10.0_REAL64*EPSINR64) THEN",
         "IINR_STATE = IINR_NEAR", "IF (.NOT. INNER_FINISHED)"),
        "inner state transition order",
    )
    accepted_writes = [statement for statement in state_statements
                       if re.match(r"^ACCEPTED\s*=", statement)]
    ok_writes = [statement for statement in state_statements
                 if re.match(r"^OK\s*=", statement)]
    require(accepted_writes == ["ACCEPTED = .FALSE."] * 4,
            "core cannot bypass the terminal decision")
    require(ok_writes == ["OK = .FALSE.", "OK = .TRUE.", "OK = .TRUE."],
            "core exact completion-status write set")

    require("CUTOFF_VISIT64=0_INT64" in core_packed,
            "visit counter initialized once")
    require(core_packed.count("CUTOFF_VISIT64=0_INT64") == 1,
            "visit counter single initialization")
    require("CUTOFF_VISIT64=CUTOFF_VISIT64+CUTOFF_DELTA64" in
            core_packed, "additive child cutoff propagation")
    cutoff_assignments = [
        statement for statement in normalized_statements(core)
        if re.match(r"^CUTOFF_VISIT64\s*=", statement)
    ]
    require(cutoff_assignments == [
        "CUTOFF_VISIT64 = 0_INT64",
        "CUTOFF_VISIT64 = CUTOFF_VISIT64 + CUTOFF_DELTA64",
    ], "visit counter exact write set")

    norm_calls = call_sites(core, "SCALAR_GROUP_NORM64")
    require(len(norm_calls) == 2, "one inner and one outer norm site")
    norm_flat = [";".join(call) for call in norm_calls]
    require("FLUX64(:,IG,6);FLUX64(:,IG,7);KEYFLX_BASE1" in norm_flat[0],
            "inner norm slices")
    require("FLUX64(:,IG,2);FLUX64(:,IG,3);KEYFLX_BASE1" in norm_flat[1],
            "outer norm slices")

    rebal = routine_region(source, "FLUBAL64")
    rebal_packed = dense(rebal)
    require("REAL(REAL64)" in rebal_packed and "REBAL64" in rebal_packed,
            "REAL64 rebalancing state")
    require("REAL(REAL32)" in rebal_packed and "SCAT_OFF32" in rebal_packed,
            "REAL32 off-group operator")
    require(len(call_sites(rebal, "ALSBD")) == 1, "one ALSBD solve")
    require("CALLALSBD(NGREB,1,REBAL64,IER,NGRP)" in rebal_packed,
            "exact ALSBD ABI")
    require(re.search(r"(?i)\bCALL\s+ALSB\s*\(", rebal) is None,
            "legacy REAL32 ALSB forbidden")
    for token in ("LCMGET", "LCMGPD", "LCMLEN"):
        require(token not in rebal.upper(), f"second gather in FLUBAL64: {token}")
    rebal_formulas = (
        "REBAL64(IOFF,NGREB+1)=XCSOU64(IGR)",
        "REBAL64(IOFF,IOFF)=REBAL64(IOFF,IOFF)+"
        "(1.0_REAL64-REAL(ALBEDO32(-MATALB_SURFACE(ISUR)),REAL64))*"
        "FLUX64(KEYCUR(ISUR),IGR)*REAL(SURFAC32(ISUR),REAL64)",
        "IFSCAT=IJJ_OFF(IBM,IGR)-NJJ_OFF(IBM,IGR)+1",
        "REBAL64(IOFF,NGREB+1)=REBAL64(IOFF,NGREB+1)+"
        "FLUX64(IND,JGR)*REAL(SCAT_OFF32(P,IGR),REAL64)*"
        "REAL(VOL32(IR),REAL64)",
        "REBAL64(IOFF,IOFF)=REBAL64(IOFF,IOFF)+FLUX64(IND,IGR)*"
        "(REAL(XSTRC32(IBM,IGR),REAL64)-"
        "REAL(XSDIA0_32(IBM,IGR),REAL64))*REAL(VOL32(IR),REAL64)",
        "REBAL64(IOFF,JGR-IGDEB+1)=REBAL64(IOFF,JGR-IGDEB+1)-"
        "FLUX64(IND,JGR)*REAL(SCAT_OFF32(P,IGR),REAL64)*"
        "REAL(VOL32(IR),REAL64)",
        "FLUX64(IND,IGR)=FLUX64(IND,IGR)*REBAL64(IOFF,NGREB+1)",
    )
    for formula in rebal_formulas:
        require(rebal_packed.count(formula) == 1,
                f"FLUBAL64 frozen formula: {formula}")
    require(rebal_packed.count(
        "P=IPOS_OFF(IBM,IGR)+IJJ_OFF(IBM,IGR)-JGR") == 2,
        "both FLUBAL64 packed-scatter loops use the frozen index")
    require("IF(IER/=0)RETURN" in rebal_packed,
            "ALSBD failure is fail-closed")
    require("DOIND=1,NUNKNO" in rebal_packed,
            "rebalancing factor applies to every unknown")
    rebal_statements = normalized_statements(rebal)
    rebal_writes = [statement for statement in rebal_statements
                    if re.match(r"^REBAL64(?:\s*\(|\s*=)", statement)]
    require(rebal_writes == [
        "REBAL64 = +0.0_REAL64",
        "REBAL64(IOFF,NGREB+1) = XCSOU64(IGR)",
        "REBAL64(IOFF,IOFF) = REBAL64(IOFF,IOFF) + "
        "(1.0_REAL64-REAL(ALBEDO32(-MATALB_SURFACE(ISUR)),REAL64)) * "
        "FLUX64(KEYCUR(ISUR),IGR) * REAL(SURFAC32(ISUR),REAL64)",
        "REBAL64(IOFF,NGREB+1) = REBAL64(IOFF,NGREB+1) + "
        "FLUX64(IND,JGR) * REAL(SCAT_OFF32(P,IGR),REAL64) * "
        "REAL(VOL32(IR),REAL64)",
        "REBAL64(IOFF,IOFF) = REBAL64(IOFF,IOFF) + "
        "FLUX64(IND,IGR) * (REAL(XSTRC32(IBM,IGR),REAL64) - "
        "REAL(XSDIA0_32(IBM,IGR),REAL64)) * REAL(VOL32(IR),REAL64)",
        "REBAL64(IOFF,JGR-IGDEB+1) = "
        "REBAL64(IOFF,JGR-IGDEB+1) - FLUX64(IND,JGR) * "
        "REAL(SCAT_OFF32(P,IGR),REAL64) * REAL(VOL32(IR),REAL64)",
    ], "FLUBAL64 exact matrix/RHS write set")
    factor_writes = [statement for statement in rebal_statements
                     if re.match(r"^FLUX64\s*\(", statement)]
    require(factor_writes == [
        "FLUX64(IND,IGR) = FLUX64(IND,IGR) * REBAL64(IOFF,NGREB+1)"
    ], "FLUBAL64 exact factor write set")
    require_order(
        rebal,
        ("REBAL64(IOFF,NGREB+1) = XCSOU64(IGR)",
         "IFSCAT = IJJ_OFF",
         "DO JGR = IFSCAT", "DO JGR = MAX(IFSCAT,IGDEB)",
         "IF (JGR == IGR) THEN", "ELSE",
         "CALL ALSBD", "IF (IER /= 0) RETURN",
         "DO IND = 1, NUNKNO", "FLUX64(IND,IGR) = FLUX64(IND,IGR)"),
        "FLUBAL64 physical-matrix order",
    )

    accel = routine_region(source, "FLU2AC64")
    accel_packed = dense(accel)
    for statement in (
        "R1_64=FLUX64(IR,IG,2)-FLUX64(IR,IG,1)",
        "R2_64=FLUX64(IR,IG,3)-FLUX64(IR,IG,2)",
        "NOM64=NOM64+R1_64*(R2_64-R1_64)",
        "DENOM64=DENOM64+(R2_64-R1_64)*(R2_64-R1_64)",
        "DMU64=-NOM64/DENOM64",
        "FLUX64(IR,IG,3)=FLUX64(IR,IG,2)+DMU64*"
        "(FLUX64(IR,IG,3)-FLUX64(IR,IG,2))",
        "FLUX64(IR,IG,2)=FLUX64(IR,IG,1)+DMU64*"
        "(FLUX64(IR,IG,2)-FLUX64(IR,IG,1))",
        "AKEEP64(3)=AKEEP64(2)+DMU64*(AKEEP64(3)-AKEEP64(2))",
        "AKEEP64(2)=AKEEP64(1)+DMU64*(AKEEP64(2)-AKEEP64(1))",
    ):
        require(statement in accel_packed, f"FLU2AC64 formula: {statement}")
    require("DENOM64<=0.0_REAL64" in accel_packed,
            "nonnegative exact-zero acceleration denominator")
    require("ZMU64=1.0_REAL64" in accel_packed,
            "no-acceleration identity")
    require("IEEE_IS_FINITE(DMU64)" in accel_packed and
            "DMU64>0.0_REAL64" in accel_packed,
            "finite positive inherited acceleration")
    accel_statements = normalized_statements(accel)
    flux_updates = [statement for statement in accel_statements
                    if re.match(r"^FLUX64\s*\([^)]*\)\s*=", statement)]
    akeep_updates = [statement for statement in accel_statements
                     if re.match(r"^AKEEP64\s*\([^)]*\)\s*=", statement)]
    zmu_updates = [statement for statement in accel_statements
                   if re.match(r"^ZMU64\s*=", statement)]
    control_updates = [statement for statement in accel_statements
                       if re.match(
                           r"^(?:NOM64|DENOM64|R1_64|R2_64|DMU64)\s*=",
                           statement)]
    require(flux_updates == [
        "FLUX64(IR,IG,3) = FLUX64(IR,IG,2) + DMU64 * "
        "(FLUX64(IR,IG,3)-FLUX64(IR,IG,2))",
        "FLUX64(IR,IG,2) = FLUX64(IR,IG,1) + DMU64 * "
        "(FLUX64(IR,IG,2)-FLUX64(IR,IG,1))",
    ], "FLU2AC64 exact flux write set")
    require(akeep_updates == [
        "AKEEP64(3) = AKEEP64(2) + DMU64*(AKEEP64(3)-AKEEP64(2))",
        "AKEEP64(2) = AKEEP64(1) + DMU64*(AKEEP64(2)-AKEEP64(1))",
    ], "FLU2AC64 exact AKEEP write set")
    require(zmu_updates == ["ZMU64 = 1.0_REAL64", "ZMU64 = DMU64"],
            "FLU2AC64 exact ZMU write set")
    require(control_updates == [
        "NOM64 = +0.0_REAL64",
        "DENOM64 = +0.0_REAL64",
        "R1_64 = FLUX64(IR,IG,2) - FLUX64(IR,IG,1)",
        "R2_64 = FLUX64(IR,IG,3) - FLUX64(IR,IG,2)",
        "NOM64 = NOM64 + R1_64*(R2_64-R1_64)",
        "DENOM64 = DENOM64 + (R2_64-R1_64)*(R2_64-R1_64)",
        "DMU64 = -NOM64/DENOM64",
    ], "FLU2AC64 exact control write set")
    require_order(
        accel,
        ("ZMU64 = 1.0_REAL64", "IF (DENOM64 <= 0.0_REAL64) THEN",
         "OK = .TRUE.", "RETURN", "DMU64 = -NOM64/DENOM64",
         "IF (DMU64 > 0.0_REAL64) THEN", "ZMU64 = DMU64",
         "FLUX64(IR,IG,3) =", "FLUX64(IR,IG,2) =",
         "AKEEP64(3) =", "AKEEP64(2) ="),
        "FLU2AC64 identity/positive-update order",
    )

    terminal = routine_region(source, "SPOR64_A9_TERMINAL64")
    terminal_packed = dense(terminal)
    require("REAL(REAL64)" in terminal_packed, "REAL64 terminal inputs")
    strict = (
        "EEXT64<EPSOUT64.AND.EUNK64<EPSUNK64.AND."
        "EINR_LAST64<EPSINR64.AND.IINR_STATE==IINR_STRICT.AND."
        "OUTER_ITERATION>=2"
    )
    require(strict in terminal_packed, "exact strict terminal Boolean")
    terminal_writes = [statement for statement in
                       normalized_statements(terminal)
                       if re.match(r"^ACCEPTED\s*=", statement)]
    require(len(terminal_writes) == 1,
            "terminal has one authoritative ACCEPTED assignment")
    require("EEXT64=+0.0_REAL64" in core_packed,
            "frozen TYPE S EEXT")

    norm = routine_region(source, "SCALAR_GROUP_NORM64")
    norm_packed = dense(norm)
    for statement in (
        "DIFFERENCE64=ABS(PRESENT64(IND)-NEW64(IND))",
        "GROUP_ERROR64=MAX(GROUP_ERROR64,DIFFERENCE64)",
        "DENOMINATOR64=MAX(DENOMINATOR64,ABS(NEW64(IND)))",
        "DENOMINATOR64<=0.0_REAL64",
        "GROUP_ERROR64=GROUP_ERROR64/DENOMINATOR64",
    ):
        require(statement in norm_packed, f"scalar norm formula: {statement}")
    norm_statements = normalized_statements(norm)
    norm_writes = [statement for statement in norm_statements if re.match(
        r"^(?:GROUP_ERROR64|DENOMINATOR64|DIFFERENCE64)\s*=", statement)]
    require(norm_writes == [
        "GROUP_ERROR64 = +0.0_REAL64",
        "DENOMINATOR64 = +0.0_REAL64",
        "DIFFERENCE64 = ABS(PRESENT64(IND)-NEW64(IND))",
        "GROUP_ERROR64 = MAX(GROUP_ERROR64,DIFFERENCE64)",
        "DENOMINATOR64 = MAX(DENOMINATOR64,ABS(NEW64(IND)))",
        "GROUP_ERROR64 = GROUP_ERROR64/DENOMINATOR64",
    ], "scalar norm exact write set")

    # No REAL32 declaration may own or receive a mutable/control name.
    mutable_names = (
        "FLUX64", "FIXED_SOURCE64", "INITIAL_FLUX64", "XCSOU64",
        "AKEEP64", "EINR64", "EINR_LAST64", "EUNK64", "EEXT64",
        "EPSINR64", "EPSUNK64", "EPSOUT64", "ZMU64", "REBAL64",
    )
    for statement in normalized_statements(code):
        if "REAL(REAL32)" in statement:
            for name in mutable_names:
                require(not re.search(rf"\b{re.escape(name)}\b", statement),
                        f"REAL32 mutable/control declaration: {name}")
    operator_names = (
        "VOL32", "XSTRC32", "XSDIA0_32", "ALBEDO32", "SURFAC32",
        "SCAT_OFF32",
    )
    declarations = [
        statement for statement in normalized_statements(code)
        if "::" in statement and statement.startswith("REAL(")
    ]
    for name in operator_names:
        named = [statement for statement in declarations
                 if re.search(rf"\b{re.escape(name)}\b", statement)]
        require(named, f"missing operator declaration: {name}")
        require(all("REAL(REAL32)" in statement for statement in named),
                f"stored operator kind changed: {name}")


def validate_host_source(source: str) -> None:
    code = fortran_code(source)
    packed = dense(source)
    require(re.search(r"(?im)^\s*MODULE\s+SPOR64_A9_HOST\s*$", code)
            is not None, "host module identity")
    require("DEFAULT_REAL64_ROUTE=.FALSE." in packed,
            "default REAL64 route OFF")
    require("KIND(1.0)==REAL32" in packed and
            "KIND(0.0D0)==REAL64" in packed, "host kind guard")
    dispatch = routine_region(source, "SPOR64_A9_DISPATCH")
    require_no_hidden_control(dispatch)
    dispatch_packed = dense(dispatch)
    require("SELECTED_REAL64=DEFAULT_REAL64_ROUTE" in dispatch_packed,
            "selector begins at default OFF")
    require("IF(REQUESTED)SELECTED_REAL64=.TRUE." in dispatch_packed,
            "only explicit request selects REAL64")
    require("ROUTE_OK=.FALSE." in dispatch_packed,
            "host status fail-closed")
    real_calls = call_sites(dispatch, "REAL64_CALLBACK")
    legacy_calls = call_sites(dispatch, "LEGACY_CALLBACK")
    require(real_calls == [["STATE64", "ROUTE_OK"]],
            "one exact REAL64 callback")
    require(legacy_calls == [["ROUTE_OK"]], "one exact legacy callback")
    require_order(
        dispatch,
        ("IF (SELECTED_REAL64) THEN", "CALL REAL64_CALLBACK", "RETURN",
         "END IF", "CALL LEGACY_CALLBACK"),
        "no-fallback dispatch",
    )
    selected_writes = [statement for statement in
                       normalized_statements(dispatch)
                       if re.search(
                           r"(?:^|\s)(?:SELECTED_REAL64|ROUTE_OK)\s*=",
                           statement)]
    require(selected_writes == [
        "SELECTED_REAL64 = DEFAULT_REAL64_ROUTE",
        "ROUTE_OK = .FALSE.",
        "IF (REQUESTED) SELECTED_REAL64 = .TRUE.",
    ], "selector exact state write set")
    for token in (
        "LCM", "GANLIB", "XDRTA2", "SPOMOC", "FLU2DR", "DOORFV",
        "OPEN(", "READ(", "WRITE(", "REWIND", "DRAGON", "MOCA",
    ):
        require(token not in code.upper(),
                f"production/runtime dependency in abstract host: {token}")
    require(re.search(r"(?i)REAL\s*\(\s*REAL64\s*\).*CONTIGUOUS.*STATE64",
                      dispatch) is not None,
            "REAL64 contiguous selector state")
    require(re.search(r"(?i)REAL\s*\(\s*REAL32\s*\).*STATE", dispatch)
            is None, "no REAL32 selector state")


def validate_runner_contract(source: str, verify_hash: bool = True) -> None:
    require("set -eu" in source, "runner fail-closed shell mode")
    require("run_phase_a9a.sh" not in source,
            "runner cannot recursively invoke itself")
    require("run_phase_a8.sh" not in source and
            not re.search(r"run_phase_a[1-7]", source, re.I),
            "no prerequisite runner execution")
    require('RECEIPT="$HERE/phase_a9a_implementation_receipt.sha256"'
            in source, "receipt path")
    require(EXPECTED_A8_RECEIPT_SHA256 in source,
            "A8 receipt identity")
    require("check_phase_a9.py" in source and
            "test_phase_a9_contract" in source, "checker/test invocation")
    require("SPOR64_A9.f90" in source and
            "SPOR64_A9_HOST.f90" in source, "positive compile matrix")
    require("Utilib/src/ALSBD.f" in source, "ALSBD compile authority")
    for negative in EXPECTED_NEGATIVES:
        require(negative in source, f"negative compile fixture: {negative}")
    require("for stem in core host anchor" in source and
            "for class in unresolved defined" in source and
            'expected_${stem}_${class}.txt' in source,
            "all six exact nm inventories")
    require("-fdefault-real-8" in source, "default-real8 rejection")
    require("cmp -s" in source and "nm -g" in source,
            "exact symbol comparison")
    for forbidden in ("Dragon", "rdragon", "make -C", "ld ", "ar "):
        # The status messages may spell DRAGON-RUNS=0; only commands count.
        if forbidden == "Dragon":
            require(not re.search(r"(?im)^\s*(?:\$[^ ]+\s+)?Dragon\b", source),
                    "Dragon command forbidden")
        else:
            require(forbidden not in source, f"runner command forbidden: {forbidden}")
    shell_commands = source.replace("\\\n", " ").splitlines()
    for line in shell_commands:
        if '"$FC"' in line and "--version" not in line:
            require("-c" in line,
                    "every compiler action is compile-only")
    for claim in (
        "PRODUCTION-ROUTE-CONNECTED=false",
        "CONTINUOUS-REAL64-LANE=false",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
        "OBJECT-LINKS=0", "TRANSPORT-SOLVES=0", "DRAGON-RUNS=0",
    ):
        require(claim in source, f"runner claim boundary: {claim}")
    if verify_hash:
        require(EXPECTED_RUNNER_SHA256 != UNFROZEN,
                "unfrozen runner hash")
        require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256,
                "runner hash freeze")


def validate_makefile_contract(source: str) -> None:
    pattern = re.compile(
        r"(?m)^\.PHONY: spot-real64-phase-a9a\n"
        r"spot-real64-phase-a9a :\n"
        r"\tsh validation/iterative/real64_phase_a9/run_phase_a9a\.sh$"
    )
    matches = list(pattern.finditer(source))
    require(len(matches) == 1, "one exact isolated A9a Make target")
    without = source[:matches[0].start()] + source[matches[0].end():]
    require("phase-a9" not in without.lower() and
            "real64_phase_a9" not in without.lower(),
            "no hidden A9a Make dependency")
    for target in ("all", "tests", "spot-fast"):
        match = re.search(rf"(?m)^{re.escape(target)}\s*:(.*)$", source)
        if match:
            require("a9" not in match.group(1).lower(),
                    f"A9a not a {target} prerequisite")


def validate_docs(readme: str, root_readme: str, iterative: str) -> None:
    combined = "\n".join((readme, root_readme, iterative))
    boundary_tokens = (
        "FROZEN-IMPLEMENTED-COMPILE-ONLY-OUTER-CLOSURE",
        "CONTINUOUS-REAL64-LANE=false",
        "PRODUCTION-ROUTE-CONNECTED=false",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    )
    for token in boundary_tokens:
        require(token in readme, f"A9a README boundary: {token}")
    for document, label in ((readme, "A9a"), (root_readme, "root"),
                            (iterative, "iterative")):
        require("make spot-real64-phase-a9a" in document,
                f"{label} README gate command")
    require("A9b" in readme and "production" in readme.lower(),
            "A9b deferred production boundary")
    overclaims = (
        r"(?i)radial (?:solver )?converged",
        r"(?i)picard converged",
        r"(?i)physical accuracy (?:is )?proved",
        r"(?i)production route (?:is )?connected",
    )
    for pattern in overclaims:
        require(re.search(pattern, combined) is None,
                f"documentation overclaim: {pattern}")


def receipt_paths(receipt_text: str) -> list[str]:
    paths: list[str] = []
    for line in receipt_text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"[0-9a-f]{64}  (.+)", line)
        require(match is not None, "malformed receipt line")
        paths.append(match.group(1))
    return paths


def validate_receipt_scope(text: str) -> None:
    require(EXPECTED_RECEIPT_PATHS, "unfrozen receipt path scope")
    paths = receipt_paths(text)
    require(paths == list(EXPECTED_RECEIPT_PATHS),
            "exact ordered receipt scope")
    require(len(paths) == len(set(paths)), "duplicate receipt path")
    require("validation/iterative/real64_phase_a9/phase_a9a_implementation_receipt.sha256"
            not in paths, "receipt self-cycle")


def validate_production_tree_unchanged() -> None:
    result = subprocess.run(
        ["git", "diff", "--quiet", BASELINE_COMMIT, "--", "src", "Utilib/src"],
        cwd=ROOT,
        check=False,
    )
    require(result.returncode == 0, "production source changed in A9a")


def run_checks(verify_hashes: bool = True) -> None:
    required = (MANIFEST, CORE, HOST, RUNNER, README, RECEIPT, A8_RECEIPT)
    for path in required:
        require(path.is_file(), f"missing A9a artifact: {path}")
    for name in EXPECTED_NEGATIVES + EXPECTED_SYMBOL_FILES:
        require((HERE / name).is_file(), f"missing gate artifact: {name}")

    data = json.loads(MANIFEST.read_text())
    validate_manifest(data, verify_hashes=verify_hashes)
    validate_core_source(CORE.read_text())
    validate_host_source(HOST.read_text())
    validate_runner_contract(RUNNER.read_text(), verify_hash=verify_hashes)
    validate_makefile_contract(MAKEFILE.read_text())
    validate_docs(README.read_text(), ROOT_README.read_text(),
                  ITERATIVE_README.read_text())
    validate_receipt_scope(RECEIPT.read_text())
    validate_production_tree_unchanged()

    require(sha256(A8_RECEIPT) == EXPECTED_A8_RECEIPT_SHA256,
            "live A8 receipt identity")
    for path, expected in EXPECTED_LEGACY_HASHES.items():
        require(sha256(ROOT / path) == expected,
                f"legacy source changed: {path}")
    if verify_hashes:
        require(sha256(CORE) == EXPECTED_CORE_SHA256, "core hash freeze")
        require(sha256(HOST) == EXPECTED_HOST_SHA256, "host hash freeze")
        require(sha256(README) == EXPECTED_README_SHA256,
                "README hash freeze")


def main() -> int:
    try:
        run_checks()
    except (OSError, ValueError, json.JSONDecodeError, PhaseA9Error) as exc:
        print(f"SPOR64 PHASE-A9a CHECK FAILURE: {exc}")
        return 1
    print("SPOR64 PHASE-A9a STATIC CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

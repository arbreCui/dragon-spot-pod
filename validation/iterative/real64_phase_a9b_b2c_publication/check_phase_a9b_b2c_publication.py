#!/usr/bin/env python3
"""Static contract gate for the accepted-only B2c publication boundary."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "validation/iterative/real64_phase_a9b_b2c_publication"
B2C = ROOT / "src/SPOR64_B2C.f90"
B2B = ROOT / "src/SPOR64_B2B.f90"
FLU = ROOT / "src/FLU.f"
DEPS = ROOT / "src/.dragon_deps.mk"
MAKEFILE = ROOT / "Makefile"
MANIFEST = HERE / "precision_manifest.json"
RUNNER = HERE / "run_phase_a9b_b2c_publication.sh"
RECEIPT = HERE / "phase_a9b_b2c_publication_receipt.sha256"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2b_ingress/"
    "phase_a9b_b2b_ingress_receipt.sha256"
)

PARENT_COMMIT = "c00072ca7ba6cbd15f9494dfc943344ec325a21d"
PARENT_RECEIPT_SHA256 = (
    "bfdcffd594ec69f0e259a621945dce3b9a551831c01e2fa7ee5bfcaab41dc2cc"
)
RUNNER_SHA256 = "726369393845c5e595287c218ecf83312e6b13f7c4f95cc6d9cc362f83f6e572"
RUNNER_LOGICAL_COMMANDS_SHA256 = (
    "cdcf2630e20b2961ac170a07de67449ba4278ce7ca1638fafbd36a8e2ce86ec3"
)
MUTATION_TEST_COUNT = 151
EXPECTED_B2C_SOURCE_SHA256 = (
    "c35e247d9612377e072a2bd14de5080c9aceb4f90c2d4fac6cf1150e6538fc45"
)
EXPECTED_B2B_SOURCE_SHA256 = (
    "d13e9bc467d96d4f5dc0e77bb5c238613fdb1071befbb288543e9df42550d3a5"
)
EXPECTED_FLU_SOURCE_SHA256 = (
    "b828ef79a0eb8b123dea07e556818c0ef2974020aa571eaddef5ce8dd9831705"
)
EXPECTED_B2C_STATEMENT_SHA256 = (
    "ed62d88aa78a5b0eb1053b4667bea5c15ad82fc449efaa8d94883d4b2a4a1703"
)
EXPECTED_B2B_STATEMENT_SHA256 = (
    "5b65a035559debd2ad521c61303d35042914b550f009ab081a5a0691c43c3692"
)
EXPECTED_FLU_SELECTED_STATEMENT_SHA256 = (
    "c18fccef6adc9e5787d2b83649fdfb05a4f8966f1d66b3ec62f36892732badbe"
)
EXPECTED_FLU_STATEMENT_SHA256 = (
    "a60fa1ab6176d9c9a498753c76af563b0c543a05286a5898fde500ea598285fa"
)

EXPECTED_B2C_LCM_INVENTORY = Counter(
    {
        "LCMDID": 1,
        "LCMGID": 1,
        "LCMLEL": 1,
        "LCMLEN": 3,
        "LCMLID": 3,
        "LCMPDL": 4,
        "LCMPTC": 4,
        "LCMPUT": 4,
    }
)
EXPECTED_B2B_LCM_INVENTORY = Counter(
    {
        "LCMGET": 29,
        "LCMLEN": 5,
        "LCMGID": 4,
        "LCMLEL": 3,
        "LCMGIL": 3,
        "LCMGTC": 2,
        "LCMGDL": 2,
    }
)
EXPECTED_B2C_CALL_INVENTORY = Counter(
    {
        "LCMPDL": 4,
        "LCMPUT": 4,
        "LCMPTC": 4,
        "XABORT": 4,
        "LCMLEN": 3,
        "LCMLEL": 1,
    }
)
EXPECTED_B2B_CALL_INVENTORY = Counter(
    {
        "LCMGET": 29,
        "LCMLEN": 5,
        "LCMLEL": 3,
        "LCMGDL": 2,
        "LCMGTC": 2,
        "FLU2DR64_CORE": 1,
        "SPOR64_B2C_PUBLISH": 1,
        "XDRTA2": 1,
    }
)
EXPECTED_B2C_PAREN_HEADS = {
    "ABS", "ABSENT_OR_MATCHES", "ABSENT_RECORD", "ALL", "ALLOCATE",
    "ALLOCATED", "ANY", "CHARACTER", "C_ASSOCIATED", "DEALLOCATE",
    "EPS_CONVERGE", "FLUX_STAGE32", "HUGE", "IEEE_IS_FINITE", "IF",
    "INT", "INTEGER", "INTENT", "KEYFLX_BASE1", "KIND", "LCMDID",
    "LCMGID", "LCMLEL", "LCMLEN", "LCMLID", "LCMPDL", "LCMPTC",
    "LCMPUT", "LEAK1D_INPUT32", "MERGE", "REAL", "RECORD_MATCHES",
    "SEEN_UNKNOWN", "SIZE", "SOURCE_STAGE32", "SPOR64_B2C_PUBLISH",
    "STATE_VECTOR", "TERMINAL_FLUX64", "TERMINAL_SOURCE64", "TRANSFER",
    "TYPE", "XABORT",
}
EXPECTED_B2B_PAREN_HEADS = {
    "ABS", "ABSENT_OR_MATCHES", "ABSENT_RECORD", "ALBEDO32", "ALL",
    "ALLOCATE", "ANY", "CHARACTER", "CHARACTER_RECORD_MATCHES",
    "C_ASSOCIATED", "DEALLOCATE", "EPS_STAGE32", "FILUNIT",
    "FIXED_SOURCE64", "FLU2DR64_CORE", "FLUX_STAGE32", "FLUX_STATE",
    "HENTRY", "IEEE_IS_FINITE", "IENTRY", "IF", "IJJ_OFF", "IJJ_STAGE",
    "IMERG", "IMERGE_STAGE", "INITIAL_FLUX64", "INT", "INTEGER",
    "INTENT", "IPOS_OFF", "IPOS_STAGE", "JENTRY", "KENTRY", "KEYCUR",
    "KEYFLX_BASE1", "KIND", "LCMGDL", "LCMGET", "LCMGID", "LCMGIL",
    "LCMGTC", "LCMLEL", "LCMLEN", "LCM_ENTRY_KIND", "LEAK1D_INPUT32",
    "LEN", "MACRO_STATE", "MATALB_SURFACE", "MATCOD", "MCCG_STATE",
    "MERGE", "NJJ_OFF", "NJJ_STAGE", "NSCAT_OFF", "NUSIGF_STAGE32",
    "NZON", "QINT32", "REAL", "REAL_PARAM32", "RECORD_MATCHES",
    "SCAT_OFF32", "SCAT_STAGE32", "SEEN_UNKNOWN", "SIZE",
    "SOURCE_STAGE32", "SOURCE_STATE", "SPOMOC_ACTIVE",
    "SPOR64_B2B_INGRESS", "SPOR64_B2C_PUBLISH", "SURFAC32",
    "SYSTEM_STATE", "TERMINAL_FLUX64", "TERMINAL_SOURCE64", "TRACK_STATE",
    "TRANSFER", "TYPE", "VALUE", "VOL32", "VOLUME_TRACK32", "XDRTA2",
    "XSDIA0_32", "XSTRC32",
}
EXPECTED_FLU_SELECTED_PAREN_HEADS = {
    "DEALLOCATE", "IF", "SPOR64_B2B_INGRESS", "XABORT",
}
B2B_READ_ONLY_LCM_APIS = {
    "LCMGDL",
    "LCMGET",
    "LCMGID",
    "LCMGIL",
    "LCMGTC",
    "LCMLEL",
    "LCMLEN",
}
EXPECTED_PUBLISHER_REFERENCES = {
    "SPOR64_B2C.f90": 3,
    "SPOR64_B2B.f90": 2,
}
EXPECTED_CPP_DIRECTIVES_SHA256 = (
    "1791a86e182b5ddf95cd9360a4b412f130351885343a80c47a3ed7d521516171"
)

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_b2b_ingress/phase_a9b_b2b_ingress_receipt.sha256",
    "Ganlib/lib/Darwin_arm64/libGanlib.a",
    "Utilib/lib/Darwin_arm64/libUtilib.a",
    "Ganlib/src/filmod.f90",
    "Ganlib/src/LCMAUX.f90",
    "Ganlib/src/lcmmod.f90",
    "Ganlib/src/LCMTLC.f90",
    "Ganlib/src/OPNMOD.f90",
    "Ganlib/src/XDREED.f90",
    "Ganlib/src/ganlib.f90",
    "src/SPOMOC.f90",
    "src/SPOMOC_R64_BRIDGE.f90",
    "src/SPOR64_A8_ACA.f90",
    "src/SPOR64_A8.f90",
    "src/MCGFFIR64_RANK_ADAPTER.f90",
    "src/SPOR64_A9.f90",
    "src/SPOR64_B2C.f90",
    "src/SPOR64_B2B.f90",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/XDRTA2.f",
    "src/.dragon_deps.mk",
    "src/Makefile",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "data/SpotPlaneFS.c2m",
    "validation/iterative/real64_phase_a9b_b2c_publication/README.md",
    "validation/iterative/real64_phase_a9b_b2c_publication/b2c_synthetic_publication.f90",
    "validation/iterative/real64_phase_a9b_b2c_publication/b2c_synthetic_publication_driver.f90",
    "validation/iterative/real64_phase_a9b_b2c_publication/check_phase_a9b_b2c_publication.py",
    "validation/iterative/real64_phase_a9b_b2c_publication/compile_b2c_positive.f90",
    "validation/iterative/real64_phase_a9b_b2c_publication/compile_fail_b2c_real32_terminal.f90",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_b2b_defined.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_b2b_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_b2c_defined.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_b2c_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_flu_defined.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/expected_flu_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2c_publication/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2c_publication/run_phase_a9b_b2c_publication.sh",
    "validation/iterative/real64_phase_a9b_b2c_publication/test_b2c_production_publisher.f90",
    "validation/iterative/real64_phase_a9b_b2c_publication/test_phase_a9b_b2c_publication_contract.py",
)

EXPECTED_PUBLICATION_CONTRACT = {
    "accepted_input_status": 4,
    "preflight_failed_status": 5,
    "child_published_status": 6,
    "driver_committed_status": 7,
    "host_committed_status": 8,
    "sole_normal_return_to_flu": 8,
    "epoch_policy": (
        "single epoch; SPOT-R64, root SOUR, AFLUX, DFLUX, and ADFLUX "
        "must be absent"
    ),
    "collision_policy": (
        "B2B catches pre-existing collisions as admission status 1 before the "
        "core; B2C repeats the same no-write check at publication time and "
        "returns status 5 if that last-moment check fails"
    ),
    "authoritative_payload": (
        "SPOT-R64/FLUX and SPOT-R64/SOUR, GANLIB type 4"
    ),
    "compatibility_payload": "root FLUX and root SOUR, GANLIB type 2",
    "compatibility_conversion_passes": 1,
    "completion_marker": False,
    "rollback_claim_after_first_write": False,
}

EXPECTED_ORDERED_OWNER_REFINEMENT = {
    "a7_logical_owners": [
        "terminal child payload publication",
        "driver metadata commit",
        "host links and leakage-cache commit",
    ],
    "a9b_implementation": "one synchronous SPOR64_B2C_PUBLISH routine",
    "semantic_rule": (
        "The three A7 owners remain distinct ordered status phases 6, 7, and 8 "
        "inside one same-lifetime publisher; this is an ordered semantic "
        "refinement, not a change to ownership order or publication authority."
    ),
}

EXPECTED_STATUS = {
    "r64_default": False,
    "accepted_publication_implemented": True,
    "accepted_only_source_handoff_connected": True,
    "single_epoch_collision_preflight": True,
    "real64_authority_bit_checked_synthetically": True,
    "real32_compatibility_conversion_checked_synthetically": True,
    "runtime_provenance_validated": False,
    "actual_transport_response_validated": False,
    "production_solver_execution_authorized": False,
    "production_publisher_synthetic_executions": 5,
    "production_solver_executions": 0,
    "validation_tracking_stream_reads": 0,
    "validation_transport_solves": 0,
    "dragon_runs": 0,
    "empirical_parameters_added": False,
    "relaxation_parameters_added": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
}

EXPECTED_PRODUCTION_SOURCES = (
    "Ganlib/src/filmod.f90",
    "Ganlib/src/LCMAUX.f90",
    "Ganlib/src/lcmmod.f90",
    "Ganlib/src/LCMTLC.f90",
    "Ganlib/src/OPNMOD.f90",
    "Ganlib/src/XDREED.f90",
    "Ganlib/src/ganlib.f90",
    "src/SPOMOC.f90",
    "src/SPOMOC_R64_BRIDGE.f90",
    "src/SPOR64_A8_ACA.f90",
    "src/SPOR64_A8.f90",
    "src/MCGFFIR64_RANK_ADAPTER.f90",
    "src/SPOR64_A9.f90",
    "src/SPOR64_B2C.f90",
    "src/SPOR64_B2B.f90",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/XDRTA2.f",
)
EXPECTED_LINK_ARCHIVES = (
    "Ganlib/lib/Darwin_arm64/libGanlib.a",
    "Utilib/lib/Darwin_arm64/libUtilib.a",
)

PUBLISH_ARGS = [
    "ipflux",
    "accepted_token",
    "terminal_flux64",
    "terminal_source64",
    "keyflx_base1",
    "leak1d_input32",
    "epsout32",
    "epsunk32",
    "epsinr32",
    "coptio",
    "macro_name",
    "track_name",
    "system_name",
    "status",
]


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def strip_fortran_comments(text: str, fixed_form: bool = False) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        if fixed_form and raw and raw[0] in "cC*!":
            continue
        quote: str | None = None
        kept: list[str] = []
        i = 0
        while i < len(raw):
            ch = raw[i]
            if quote is not None:
                kept.append(ch)
                if ch == quote:
                    if i + 1 < len(raw) and raw[i + 1] == quote:
                        kept.append(raw[i + 1])
                        i += 1
                    else:
                        quote = None
            elif ch in "'\"":
                quote = ch
                kept.append(ch)
            elif ch == "!":
                break
            else:
                kept.append(ch)
            i += 1
        lines.append("".join(kept))
    return "\n".join(lines)


def fold_fortran_continuations(text: str, fixed_form: bool = False) -> str:
    """Return compiler-visible logical source lines for the frozen source forms.

    Identifier tokens may legally cross a physical-line boundary in both free
    and fixed source form.  All lexical inventories therefore operate on this
    folded representation, never on raw physical lines.
    """
    cleaned = strip_fortran_comments(text, fixed_form=fixed_form)
    logical_lines: list[str] = []

    if fixed_form:
        current: str | None = None
        for raw in cleaned.splitlines():
            if raw.lstrip().startswith("#"):
                if current is not None:
                    logical_lines.append(current)
                    current = None
                continue
            # The production compile freezes -ffixed-line-length-72.  Columns
            # 1:5 are labels, column 6 is continuation, and 7:72 are source.
            physical = raw[:72]
            continuation = (
                len(physical) >= 6 and physical[5] not in {" ", "0"}
            )
            field = physical[6:] if len(physical) > 6 else ""
            if not field.strip():
                continue
            if continuation:
                require(current is not None,
                        "fixed-form orphan continuation line")
                current += field
            else:
                if current is not None:
                    logical_lines.append(current)
                label = re.sub(r"\s+", "", physical[:5])
                current = f"@LABEL:{label}@{field}" if label else field
        if current is not None:
            logical_lines.append(current)
        return "\n".join(logical_lines)

    current = ""
    continuing = False
    for raw in cleaned.splitlines():
        if raw.lstrip().startswith("#"):
            require(not continuing,
                    "preprocessor directive inside free-form continuation")
            continue
        if continuing and not raw.strip():
            continue
        field = raw
        if continuing:
            field = field.lstrip()
            if field.startswith("&"):
                field = field[1:]
        trimmed = field.rstrip()
        continues = trimmed.endswith("&")
        if continues:
            field = trimmed[:-1]
        if continuing:
            current += field
        else:
            current = field
        if continues:
            continuing = True
        else:
            logical_lines.append(current)
            current = ""
            continuing = False
    require(not continuing, "free-form unterminated continuation")
    return "\n".join(logical_lines)


def mask_fortran_strings(text: str) -> str:
    """Blank character-literal contents while preserving lexical spacing."""
    masked: list[str] = []
    quote: str | None = None
    i = 0
    while i < len(text):
        ch = text[i]
        if quote is None:
            if ch in "'\"":
                quote = ch
                masked.append(" ")
            else:
                masked.append(ch)
        elif ch == quote:
            if i + 1 < len(text) and text[i + 1] == quote:
                masked.extend((" ", " "))
                i += 1
            else:
                quote = None
                masked.append(" ")
        else:
            masked.append("\n" if ch == "\n" else " ")
        i += 1
    require(quote is None, "unterminated Fortran character literal")
    return "".join(masked)


def fortran_code(text: str, fixed_form: bool = False) -> str:
    code = mask_fortran_strings(
        fold_fortran_continuations(text, fixed_form=fixed_form)
    )
    if fixed_form:
        # Blanks are insignificant in fixed source form, including inside a
        # keyword or identifier.  Preserve only logical-statement newlines.
        code = "\n".join(re.sub(r"[^\S\n]+", "", line)
                         for line in code.splitlines())
    return code


def compact(text: str, fixed_form: bool = False) -> str:
    """Compact code spacing while preserving character literals byte-for-byte."""
    source = fold_fortran_continuations(text, fixed_form=fixed_form)
    result: list[str] = []
    quote: str | None = None
    i = 0
    while i < len(source):
        ch = source[i]
        if quote is None:
            if ch in "'\"":
                quote = ch
                result.append(ch)
            elif not ch.isspace():
                result.append(ch.upper())
        else:
            result.append(ch)
            if ch == quote:
                if i + 1 < len(source) and source[i + 1] == quote:
                    result.append(source[i + 1])
                    i += 1
                else:
                    quote = None
        i += 1
    require(quote is None, "unterminated Fortran character literal")
    return "".join(result)


def fortran_statement_digest(text: str, fixed_form: bool = False) -> str:
    """Hash the exact ordered compiler-visible logical-statement inventory."""
    folded = fold_fortran_continuations(text, fixed_form=fixed_form)
    statements = [compact(line) for line in folded.splitlines() if line.strip()]
    return hashlib.sha256("\0".join(statements).encode()).hexdigest()


def lcm_api_inventory(text: str, fixed_form: bool = False) -> Counter[str]:
    cleaned = fortran_code(text, fixed_form=fixed_form)
    return Counter(
        name.upper()
        for name in re.findall(r"(?i)\b(LCM[A-Z0-9]+)\s*\(", cleaned)
    )


def call_inventory(text: str, fixed_form: bool = False) -> Counter[str]:
    cleaned = fortran_code(text, fixed_form=fixed_form)
    pattern = (
        r"(?i)\bCALL([A-Z][A-Z0-9_]*)"
        if fixed_form
        else r"(?i)\bCALL\s+([A-Z][A-Z0-9_]*)"
    )
    return Counter(
        name.upper()
        for name in re.findall(pattern, cleaned)
    )


def paren_head_inventory(text: str, fixed_form: bool = False) -> set[str]:
    """Return every code identifier immediately followed by an opening paren."""
    cleaned = fortran_code(text, fixed_form=fixed_form)
    return {
        name.upper()
        for name in re.findall(r"(?i)\b([A-Z][A-Z0-9_]*)\s*\(", cleaned)
    }


def routine_region(text: str, name: str) -> str:
    text = fold_fortran_continuations(text)
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        text,
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def routine_args(text: str, name: str) -> list[str]:
    text = fold_fortran_continuations(text)
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\((.*?)\)", text
    )
    require(match is not None, f"missing {name} argument list")
    joined = re.sub(r"[\s&]", "", match.group(1))
    return [item.lower() for item in joined.split(",") if item]


def require_order(haystack: str, fragments: list[str], label: str) -> None:
    cursor = -1
    for fragment in fragments:
        position = haystack.find(fragment, cursor + 1)
        require(position >= 0, f"missing {label} fragment: {fragment}")
        require(position > cursor, f"out-of-order {label} fragment: {fragment}")
        cursor = position


def check_publisher_text(text: str) -> None:
    require(
        hashlib.sha256(text.encode()).hexdigest() == EXPECTED_B2C_SOURCE_SHA256,
        "B2C exact source SHA-256",
    )
    require(
        fortran_statement_digest(text) == EXPECTED_B2C_STATEMENT_SHA256,
        "B2C exact ordered logical-statement inventory",
    )
    source = compact(text)
    require("MODULESPOR64_B2C" in source, "missing SPOR64_B2C module")
    require(
        lcm_api_inventory(text) == EXPECTED_B2C_LCM_INVENTORY,
        f"B2C exact LCM API/count inventory differs: {lcm_api_inventory(text)}",
    )
    require(
        call_inventory(text) == EXPECTED_B2C_CALL_INVENTORY,
        f"B2C exact CALL inventory differs: {call_inventory(text)}",
    )
    require(
        paren_head_inventory(text) == EXPECTED_B2C_PAREN_HEADS,
        f"B2C parenthesized-code inventory differs: "
        f"{sorted(paren_head_inventory(text))}",
    )
    require("=>" not in fortran_code(text),
            "B2C cannot hide an LCM operation behind an alias")
    for name, value in (
        ("SPOR64_B2C_PREFLIGHT_FAILED", 5),
        ("SPOR64_B2C_CHILD_PUBLISHED", 6),
        ("SPOR64_B2C_DRIVER_COMMITTED", 7),
        ("SPOR64_B2C_HOST_COMMITTED", 8),
    ):
        require(
            re.search(rf"{name}={value}(?:\D|$)", source) is not None,
            f"{name} value differs",
        )
    require("ACCEPTED_UNPUBLISHED=4" in source, "private accepted token differs")
    require(
        routine_args(text, "SPOR64_B2C_PUBLISH") == PUBLISH_ARGS,
        "SPOR64_B2C_PUBLISH ABI differs",
    )

    region_text = routine_region(text, "SPOR64_B2C_PUBLISH")
    region = compact(region_text)
    require(
        "REAL(REAL64),INTENT(IN)::TERMINAL_FLUX64(:,:),TERMINAL_SOURCE64(:,:)"
        in region,
        "terminal payload is not REAL64 read-only",
    )
    require(
        "REAL(REAL32),ALLOCATABLE::FLUX_STAGE32(:,:),SOURCE_STAGE32(:,:)"
        in region,
        "compatibility staging is not owned REAL32 storage",
    )
    require(
        region.count("STATUS=SPOR64_B2C_PREFLIGHT_FAILED") == 1,
        "preflight status initialization differs",
    )

    first_write = region.find("AUTHORITY=LCMDID(IPFLUX,'SPOT-R64')")
    require(first_write >= 0, "missing first authoritative directory creation")
    preflight = region[:first_write]
    require(
        lcm_api_inventory(region_text[:region_text.upper().find(
            "AUTHORITY = LCMDID"
        )]) == Counter({"LCMGID": 1, "LCMLEL": 1}),
        "B2C preflight LCM inventory is not exactly read-only",
    )
    for forbidden in ("LCMDID(", "LCMLID(", "LCMPUT(", "LCMPDL(", "LCMPTC("):
        require(forbidden not in preflight, f"mutation before preflight: {forbidden}")

    preflight_fragments = [
        "STATUS=SPOR64_B2C_PREFLIGHT_FAILED",
        "IF(ACCEPTED_TOKEN/=ACCEPTED_UNPUBLISHED)RETURN",
        "IF(.NOT.C_ASSOCIATED(IPFLUX))RETURN",
        "SIZE(TERMINAL_FLUX64,1)/=NUNKNO",
        "SIZE(TERMINAL_FLUX64,2)/=NGRP",
        "SIZE(TERMINAL_SOURCE64,1)/=NUNKNO",
        "SIZE(TERMINAL_SOURCE64,2)/=NGRP",
        "IF(.NOT.ALL(IEEE_IS_FINITE(TERMINAL_FLUX64)))RETURN",
        "IF(.NOT.ALL(IEEE_IS_FINITE(TERMINAL_SOURCE64)))RETURN",
        "IF(ANY(ABS(TERMINAL_FLUX64)>REAL32_MAX64))RETURN",
        "IF(ANY(ABS(TERMINAL_SOURCE64)>REAL32_MAX64))RETURN",
        "IF(.NOT.ALL(IEEE_IS_FINITE(LEAK1D_INPUT32)))RETURN",
        "TRANSFER(EPSOUT32,0_INT32)/=FROZEN_TOL_BITS",
        "TRANSFER(EPSUNK32,0_INT32)/=FROZEN_TOL_BITS",
        "TRANSFER(EPSINR32,0_INT32)/=FROZEN_TOL_BITS",
        "IF(COPTIO/='B0  ')RETURN",
        "IF(MACRO_NAME/='MACRO0')RETURN",
        "IF(TRACK_NAME/='TRACK')RETURN",
        "IF(SYSTEM_NAME/='SYSTEM')RETURN",
        "IF(KEYFLX_BASE1(IR)<1.OR.KEYFLX_BASE1(IR)>NUNKNO)RETURN",
        "IF(SEEN_UNKNOWN(KEYFLX_BASE1(IR)))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'SPOT-R64'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'SOUR'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'AFLUX'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'DFLUX'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'ADFLUX'))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'FLUX',NGRP,10))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'EPS-CONVERGE',5,2))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'KEYFLX',NREG,1))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'OPTION',1,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.MACRO',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.TRACK',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.SYSTEM',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'SPOT-LEAK1D',NGRP,2))RETURN",
        "LEGACY_FLUX=LCMGID(IPFLUX,'FLUX')",
        "CALLLCMLEL(LEGACY_FLUX,IG,ILONG,ITYLCM)",
        "IF(ILONG/=NUNKNO.OR.ITYLCM/=2)RETURN",
        "ALLOCATE(FLUX_STAGE32(NUNKNO,NGRP),SOURCE_STAGE32(NUNKNO,NGRP),STAT=ALLOCATION_STATUS)",
    ]
    for fragment in preflight_fragments:
        require(fragment in preflight, f"preflight contract missing: {fragment}")

    require(region.count("LCMDID(") == 1, "unexpected directory creation count")
    require(region.count("LCMLID(") == 3, "unexpected list creation count")
    require(region.count("CALLLCMPDL(") == 4, "payload write count differs")
    require(region.count("CALLLCMPUT(") == 4, "metadata numeric write count differs")
    require(region.count("CALLLCMPTC(") == 4, "metadata character write count differs")
    require(
        region.count("FLUX_STAGE32=REAL(TERMINAL_FLUX64,REAL32)") == 1,
        "FLUX terminal conversion is not exactly one pass",
    )
    require(
        region.count("SOURCE_STAGE32=REAL(TERMINAL_SOURCE64,REAL32)") == 1,
        "SOUR terminal conversion is not exactly one pass",
    )

    require_order(
        region,
        [
            "AUTHORITY=LCMDID(IPFLUX,'SPOT-R64')",
            "AUTHORITY_FLUX=LCMLID(AUTHORITY,'FLUX',NGRP)",
            "CALLLCMPDL(AUTHORITY_FLUX,IG,NUNKNO,4,TERMINAL_FLUX64(:,IG))",
            "AUTHORITY_SOURCE=LCMLID(AUTHORITY,'SOUR',NGRP)",
            "CALLLCMPDL(AUTHORITY_SOURCE,IG,NUNKNO,4,TERMINAL_SOURCE64(:,IG))",
            "FLUX_STAGE32=REAL(TERMINAL_FLUX64,REAL32)",
            "SOURCE_STAGE32=REAL(TERMINAL_SOURCE64,REAL32)",
            "CALLLCMPDL(LEGACY_FLUX,IG,NUNKNO,2,FLUX_STAGE32(:,IG))",
            "LEGACY_SOURCE=LCMLID(IPFLUX,'SOUR',NGRP)",
            "CALLLCMPDL(LEGACY_SOURCE,IG,NUNKNO,2,SOURCE_STAGE32(:,IG))",
            "STATUS=SPOR64_B2C_CHILD_PUBLISHED",
            "CALLLCMPUT(IPFLUX,'STATE-VECTOR',NSTATE,1,STATE_VECTOR)",
            "CALLLCMPUT(IPFLUX,'EPS-CONVERGE',5,2,EPS_CONVERGE)",
            "CALLLCMPUT(IPFLUX,'KEYFLX',NREG,1,KEYFLX_BASE1)",
            "CALLLCMPTC(IPFLUX,'OPTION',4,COPTIO)",
            "STATUS=SPOR64_B2C_DRIVER_COMMITTED",
            "CALLLCMPTC(IPFLUX,'LINK.MACRO',12,MACRO_NAME)",
            "CALLLCMPTC(IPFLUX,'LINK.TRACK',12,TRACK_NAME)",
            "CALLLCMPTC(IPFLUX,'LINK.SYSTEM',12,SYSTEM_NAME)",
            "CALLLCMPUT(IPFLUX,'SPOT-LEAK1D',NGRP,2,LEAK1D_INPUT32)",
            "STATUS=SPOR64_B2C_HOST_COMMITTED",
            "DEALLOCATE(FLUX_STAGE32,SOURCE_STAGE32)",
        ],
        "publication transaction",
    )

    for fragment in (
        "STATE_VECTOR(1)=NGRP",
        "STATE_VECTOR(2)=NUNKNO",
        "STATE_VECTOR(3)=1",
        "STATE_VECTOR(8)=3",
        "STATE_VECTOR(9)=3",
        "STATE_VECTOR(10)=1",
        "STATE_VECTOR(11)=740",
        "STATE_VECTOR(12)=500",
        "STATE_VECTOR(17)=NMAT",
        "STATE_VECTOR(18)=1",
        "EPS_CONVERGE=[EPSINR32,EPSUNK32,EPSOUT32,0.0_REAL32,0.0_REAL32]",
    ):
        require(fragment in region, f"metadata value differs: {fragment}")

    for forbidden in (
        "CALLFLUDRV",
        "CALLFLU2DR",
        "CALLXDRTA2",
        "CALLDRAGON",
        "LCMGET(",
        "LCMGDL(",
        "SIGNATURE",
        "IMERGE-LEAK",
        "COMPLETE",
        "ROLLBACK",
        "RELAX",
        "DAMP",
        "OMEGA",
        "FITTED",
        "TUNED",
    ):
        require(forbidden not in region, f"forbidden publisher feature: {forbidden}")


def check_b2b_text(text: str) -> None:
    require(
        hashlib.sha256(text.encode()).hexdigest() == EXPECTED_B2B_SOURCE_SHA256,
        "B2B exact source SHA-256",
    )
    require(
        fortran_statement_digest(text) == EXPECTED_B2B_STATEMENT_SHA256,
        "B2B exact ordered logical-statement inventory",
    )
    region_text = routine_region(text, "SPOR64_B2B_INGRESS")
    region = compact(region_text)
    inventory = lcm_api_inventory(text)
    require(
        inventory == EXPECTED_B2B_LCM_INVENTORY,
        f"B2B exact read-only LCM API/count inventory differs: {inventory}",
    )
    require(
        call_inventory(text) == EXPECTED_B2B_CALL_INVENTORY,
        f"B2B exact CALL inventory differs: {call_inventory(text)}",
    )
    require(
        paren_head_inventory(text) == EXPECTED_B2B_PAREN_HEADS,
        f"B2B parenthesized-code inventory differs: "
        f"{sorted(paren_head_inventory(text))}",
    )
    require(set(inventory) <= B2B_READ_ONLY_LCM_APIS,
            "B2B contains a non-read-only LCM API")
    require("=>" not in fortran_code(text),
            "B2B cannot hide an LCM operation or publisher behind an alias")
    require(region.count("CALLSPOR64_B2C_PUBLISH(") == 1, "B2B publisher call count")
    expected = (
        "CALLSPOR64_B2C_PUBLISH(IPFLUX,SPOR64_B2B_ACCEPTED_UNPUBLISHED,"
        "TERMINAL_FLUX64,TERMINAL_SOURCE64,KEYFLX_BASE1,LEAK1D_INPUT32,"
        "EPSOUT32,EPSUNK32,EPSINR32,COPTIO,HENTRY(2),HENTRY(3),HENTRY(5),STATUS)"
    )
    require(expected in region, "B2B publisher call ABI differs")
    require("IF(COPTIO/='B0  ')RETURN" in region,
            "B2B does not admit exact B0")
    core_position = region.find("CALLFLU2DR64_CORE(")
    require(core_position >= 0, "B2B core rendezvous missing")
    publisher_position = region.find("CALLSPOR64_B2C_PUBLISH(")
    require(publisher_position > core_position, "B2B publisher is not post-core")
    pre_publisher_text = region_text[:region_text.upper().find(
        "CALL SPOR64_B2C_PUBLISH"
    )]
    require(
        set(lcm_api_inventory(pre_publisher_text)) <= B2B_READ_ONLY_LCM_APIS,
        "B2B performs a non-read-only LCM operation before publication",
    )
    for fragment in (
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'SPOT-R64'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'SOUR'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'AFLUX'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'DFLUX'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'ADFLUX'))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'KEYFLX',NREG,1))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'OPTION',1,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.MACRO',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.TRACK',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'LINK.SYSTEM',3,3))RETURN",
        "IF(.NOT.ABSENT_OR_MATCHES(IPFLUX,'SPOT-LEAK1D',NGRP,2))RETURN",
    ):
        position = region.find(fragment)
        require(position >= 0, f"B2B early publication guard missing: {fragment}")
        require(position < core_position, f"B2B publication guard is post-core: {fragment}")
    require_order(
        region,
        [
            "CALLFLU2DR64_CORE(",
            "ELSEIF(.NOT.ACCEPTED)THEN",
            "ELSE",
            "STATUS=SPOR64_B2B_ACCEPTED_UNPUBLISHED",
            "CALLSPOR64_B2C_PUBLISH(",
            "ENDIF",
        ],
        "B2B accepted-only handoff",
    )
    call_pos = region.find("CALLSPOR64_B2C_PUBLISH(")
    require("LCMPUT(" not in region[:call_pos], "B2B mutated host before publisher")
    require("LCMPDL(" not in region[:call_pos], "B2B wrote payload before publisher")


def check_flu_text(text: str) -> None:
    require(
        hashlib.sha256(text.encode()).hexdigest() == EXPECTED_FLU_SOURCE_SHA256,
        "FLU exact source SHA-256",
    )
    require(
        fortran_statement_digest(text, fixed_form=True)
        == EXPECTED_FLU_STATEMENT_SHA256,
        "FLU exact ordered logical-statement inventory",
    )
    logical_text = fold_fortran_continuations(text, fixed_form=True)
    selected_match = re.search(
        r"(?is)\bIF\s*\(\s*LR64\s*\)\s*THEN.*?"
        r"DEALLOCATE\s*\(\s*IMERG\s*\)\s*RETURN\s*ENDIF",
        logical_text,
    )
    require(selected_match is not None, "missing or unterminated selected R64 branch")
    branch_text = selected_match.group(0)
    require(
        fortran_statement_digest(branch_text)
        == EXPECTED_FLU_SELECTED_STATEMENT_SHA256,
        "selected FLU exact ordered logical-statement inventory",
    )
    branch = compact(branch_text)
    require(
        not lcm_api_inventory(branch_text),
        "selected FLU branch contains an LCM API: "
        f"{lcm_api_inventory(branch_text)}",
    )
    require(
        call_inventory(branch_text)
        == Counter({"XABORT": 8, "SPOR64_B2B_INGRESS": 1}),
        "selected FLU branch exact CALL inventory differs",
    )
    require(
        paren_head_inventory(branch_text) == EXPECTED_FLU_SELECTED_PAREN_HEADS,
        "selected FLU branch parenthesized-code inventory differs",
    )
    require("=>" not in fortran_code(text, fixed_form=True),
            "FLU cannot hide a selected-route call behind an alias")
    require(branch.count("CALLSPOR64_B2B_INGRESS(") == 1, "FLU ingress call count")
    require(
        "IACITR,COPTIO,ILEAK" in branch,
        "FLU does not pass parsed OPTION through B2B",
    )
    require(
        "IF(IB2STAT.EQ.SPOR64_B2C_HOST_COMMITTED)THENCONTINUE" in branch,
        "status 8 is not the sole success arm",
    )
    for name in (
        "SPOR64_B2B_ADMISSION_FAILED",
        "SPOR64_B2B_CORE_FAILED",
        "SPOR64_B2B_NOT_ACCEPTED",
        "SPOR64_B2B_ACCEPTED_UNPUBLISHED",
        "SPOR64_B2C_PREFLIGHT_FAILED",
        "SPOR64_B2C_CHILD_PUBLISHED",
        "SPOR64_B2C_DRIVER_COMMITTED",
    ):
        require(
            f"IB2STAT.EQ.{name}" in branch,
            f"FLU does not close status {name}",
        )
    require(branch.count("CALLXABORT(") == 8, "FLU failure arm count differs")
    require_order(
        branch,
        [
            "CALLSPOR64_B2B_INGRESS(",
            "IF(IB2STAT.EQ.SPOR64_B2C_HOST_COMMITTED)",
            "DEALLOCATE(IMERG)",
            "RETURN",
        ],
        "FLU selected return",
    )
    for forbidden in ("CALLFLUDRV", "CALLXDRTA2", "LCMPUT(", "LCMPDL(", "LCMPTC("):
        require(forbidden not in branch, f"selected branch fallback/mutation: {forbidden}")


def check_build_text(make_text: str, deps_text: str) -> None:
    target = "spot-real64-phase-a9b-b2c-publication"
    require(make_text.count(f".PHONY: {target}") == 1, "B2c phony target count")
    match = re.search(rf"(?m)^{re.escape(target)}\s*:(.*)$", make_text)
    require(match is not None and not match.group(1).strip(), "B2c target has dependencies")
    command = (
        "\tsh validation/iterative/real64_phase_a9b_b2c_publication/"
        "run_phase_a9b_b2c_publication.sh"
    )
    require(make_text.count(command) == 1, "B2c target command differs")
    require("FLU.o: SPOR64_B2B.o SPOR64_B2C.o" in deps_text, "FLU B2c dependency missing")
    require(
        "SPOR64_B2B.o: SPOMOC.o SPOR64_A9.o SPOR64_B2C.o" in deps_text,
        "B2B B2c dependency missing",
    )


def check_manifest(data: dict[str, object] | None = None) -> None:
    if data is None:
        data = json.loads(MANIFEST.read_text())
    require(data.get("schema") == "spot.real64.phase-a9b-b2c.publication.v1",
            "manifest schema")
    require(data.get("stage") == "PHASE-A9b-B2c", "manifest stage")
    require(
        data.get("claim")
        == "ACCEPTED-ONLY-SINGLE-EPOCH-PUBLICATION-STATIC-AND-SYNTHETIC",
        "manifest claim",
    )
    require(data["authority"]["parent_commit"] == PARENT_COMMIT, "parent commit drift")
    require(
        data["authority"]["parent_receipt_sha256"] == PARENT_RECEIPT_SHA256,
        "parent receipt hash drift",
    )
    require(
        data.get("publication_contract") == EXPECTED_PUBLICATION_CONTRACT,
        "manifest publication contract",
    )
    require(
        data.get("ordered_owner_refinement")
        == EXPECTED_ORDERED_OWNER_REFINEMENT,
        "manifest ordered-owner refinement",
    )
    require(data.get("status") == EXPECTED_STATUS, "manifest status boundary")
    evidence = data.get("validation_evidence")
    require(evidence == {
        "mutation_tests": MUTATION_TEST_COUNT,
        "positive_abi_compiles": 1,
        "negative_abi_compiles": 1,
        "validation_state_machine_executions": 12,
        "production_publisher_synthetic_executions": 5,
        "production_solver_executions": 0,
        "production_objects_linked_into_solver": 0,
    }, "manifest exact validation evidence")
    require(
        tuple(data.get("production_strict_compile_sources", ()))
        == EXPECTED_PRODUCTION_SOURCES,
        "manifest production source inventory",
    )
    require(
        tuple(data.get("production_publisher_link_archives", ()))
        == EXPECTED_LINK_ARCHIVES,
        "manifest real publisher link archives",
    )
    require(
        data.get("synthetic_scope")
        == (
            "The validation state machine has no production dependency. The "
            "in-memory LCM harness executes only SPOR64_B2C with GANLIB/UTILIB; "
            "B2B, the REAL64 solver core, transport, tracking input, and Dragon "
            "are neither linked nor executed."
        ),
        "manifest synthetic scope",
    )


def check_global_publisher_callsites(
    source_overrides: dict[str, str] | None = None,
) -> None:
    if source_overrides is None:
        source_overrides = {}
    references: dict[str, int] = {}
    calls: list[str] = []
    cpp_directives: list[str] = []
    reference_pattern = re.compile(r"(?i)\bSPOR64_B2C_PUBLISH\b")
    for path in sorted((ROOT / "src").iterdir()):
        if path.suffix.lower() not in {".f", ".f90", ".for", ".f95"}:
            continue
        fixed_form = path.suffix.lower() in {".f", ".for"}
        raw_text = source_overrides.get(path.name, path.read_text(errors="replace"))
        cpp_directives.extend(
            f"{path.name}:{line_number}:{line.rstrip()}"
            for line_number, line in enumerate(raw_text.splitlines(), start=1)
            if line.lstrip().startswith("#")
        )
        require(
            re.search(r"(?im)^\s*(?:#\s*include\b|include\s*['\"])", raw_text)
            is None,
            f"publisher enumeration forbids source inclusion in {path.name}",
        )
        publisher_cpp = [
            line for line in raw_text.splitlines()
            if line.lstrip().startswith("#")
            and re.search(r"(?i)(?:SPOR64|B2C|PUBLISH|##)", line)
        ]
        require(
            not publisher_cpp,
            f"publisher enumeration forbids relevant CPP expansion in {path.name}",
        )
        text = fortran_code(
            raw_text,
            fixed_form=fixed_form,
        )
        require(
            re.search(
                r"(?im)^(?:@LABEL:[^@]+@)?\s*INCLUDE\b", text
            ) is None,
            f"publisher enumeration forbids normalized INCLUDE in {path.name}",
        )
        count = len(reference_pattern.findall(text))
        if count:
            references[path.name] = count
        calls.extend(
            [path.name]
            * call_inventory(raw_text, fixed_form=fixed_form).get(
                "SPOR64_B2C_PUBLISH", 0
            )
        )
        if reference_pattern.search(text):
            require(
                re.search(
                    r"(?i)(?:=>\s*SPOR64_B2C_PUBLISH|"
                    r"SPOR64_B2C_PUBLISH\s*=>)",
                    text,
                ) is None,
                f"publisher alias in {path.name}",
            )
    require(
        references == EXPECTED_PUBLISHER_REFERENCES,
        f"publisher reference map differs: {references}",
    )
    require(
        hashlib.sha256("\0".join(cpp_directives).encode()).hexdigest()
        == EXPECTED_CPP_DIRECTIVES_SHA256,
        "repository Fortran CPP directive inventory differs",
    )
    require(calls == ["SPOR64_B2B.f90"], f"publisher callsites differ: {calls}")
    require(
        re.search(
            r"(?im)^\s*use\s+SPOR64_B2C\s*,\s*only\s*:\s*"
            r"SPOR64_B2C_PUBLISH\s*$",
            fortran_code(
                source_overrides.get("SPOR64_B2B.f90", B2B.read_text())
            ),
        ) is not None,
        "B2B publisher import is not the exact unaliased ONLY import",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shell_commands(source: str) -> list[str]:
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


def check_runner(text: str, verify_hash: bool = True) -> None:
    if verify_hash:
        require(
            hashlib.sha256(text.encode()).hexdigest() == RUNNER_SHA256,
            "runner exact SHA-256",
        )
    require(text.startswith("#!/bin/sh\nset -eu\n"),
            "runner must be strict POSIX shell")
    require(
        text.count("FC=/opt/homebrew/bin/gfortran\nreadonly FC\n") == 1,
        "runner compiler binding must be exact and readonly",
    )
    fc_assignments = re.findall(
        r"(?m)^[ \t]*(?:(?:export|readonly)[ \t]+)?FC[ \t]*=.*$", text
    )
    require(fc_assignments == ["FC=/opt/homebrew/bin/gfortran"],
            "runner compiler path assigned exactly once")
    require(
        re.search(r"(?m)^[ \t]*(?:unset|read)\b[^\n]*\bFC\b", text) is None,
        "runner compiler binding cannot be unset or read",
    )
    require("SPOT_B2C_DEVELOPMENT" not in text,
            "release runner cannot bypass its receipt")
    require('shasum -a 256 -c "$RECEIPT"' in text,
            "runner verifies the implementation receipt")
    require("EXPECTED_PARENT_COMMIT=" + PARENT_COMMIT in text,
            "runner freezes parent commit")
    require("EXPECTED_PARENT_HASH=" + PARENT_RECEIPT_SHA256 in text,
            "runner freezes parent receipt")
    require("EXPECTED_FC_BANNER=" in text, "runner compiler identity")
    require("uname -s" in text and "uname -m" in text,
            "runner platform identity")

    commands = shell_commands(text)
    require(
        hashlib.sha256("\0".join(commands).encode()).hexdigest()
        == RUNNER_LOGICAL_COMMANDS_SHA256,
        "runner exact ordered logical-command inventory",
    )
    joined = "\n".join(commands)
    require("`" not in text, "runner cannot use backtick command substitution")
    function_names = re.findall(
        r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*(?:\{|$)",
        text,
    )
    require(
        function_names
        == ["compile_free", "compile_fixed", "extract_defined",
            "extract_unresolved"],
        f"runner shell-function inventory differs: {function_names}",
    )
    invocation_prefix = (
        r"(?:^|[|;&({])\s*(?:(?:if|elif|while|until)\s+)?(?:!\s*)?"
    )
    indirect = re.compile(
        invocation_prefix + r"(?:env|command|exec|eval|alias|xargs)\b",
        re.IGNORECASE | re.MULTILINE,
    )
    require(indirect.search(joined) is None,
            "runner cannot use indirect command dispatch")
    dot_source = re.compile(
        r"^\s*(?:(?:if|elif|while|until)\s+)?(?:!\s*)?"
        r"(?:\.|source)(?=\s)",
        re.IGNORECASE,
    )
    require(not any(dot_source.match(command) for command in commands),
            "runner cannot source another script")
    require(
        re.search(r"\b(?:sh|bash|zsh)[ \t]+-c\b", joined, re.I) is None,
        "runner cannot invoke a secondary command shell",
    )
    direct_tool = re.compile(
        invocation_prefix
        + r'''["']?(?:(?:/|\./|\.\./)[^\s"']*/)?'''
        + r'''(?:ld|ar|cc|gcc(?:-\d+)?|clang(?:-\d+)?|'''
        + r'''gfortran(?:-\d+)?|ifort|ifx|nvfortran|flang(?:-new)?)'''
        + r'''["']?(?=\s|$)''',
        re.IGNORECASE | re.MULTILINE,
    )
    require(direct_tool.search(joined) is None,
            "runner cannot invoke an unreviewed direct compiler/linker")
    literal_path = re.compile(
        invocation_prefix + r'''["']?(?:/|\./|\.\./)[^\s;|&()"']+''',
        re.IGNORECASE | re.MULTILINE,
    )
    require(literal_path.search(joined) is None,
            "runner cannot execute an unreviewed literal path")
    dynamic_head = re.compile(
        invocation_prefix
        + r'''["']?\$(?:\{)?([A-Za-z_][A-Za-z0-9_]*)(?:\})?''',
        re.IGNORECASE | re.MULTILINE,
    )
    dynamic_variables = [match.group(1).upper()
                         for match in dynamic_head.finditer(joined)]
    require(
        set(dynamic_variables) <= {"FC", "SYN_DIR", "HARNESS_DIR"},
        f"runner dynamic command head differs: {dynamic_variables}",
    )

    path_execution = re.compile(
        invocation_prefix
        + r'''["']?(\$(?:\{)?(?:BUILD_DIR|PROD_DIR|SYN_DIR|'''
        + r'''HARNESS_DIR|ABI_DIR)(?:\})?/[^\s;|&()"']*)''',
        re.IGNORECASE | re.MULTILINE,
    )
    executed_paths = [item.group(1) for item in path_execution.finditer(joined)]
    require(
        executed_paths
        == ["$SYN_DIR/b2c_state_machine", "$HARNESS_DIR/b2c_publisher_harness"],
        f"runner executable inventory differs: {executed_paths}",
    )

    compiler_commands = [
        command for command in commands
        if re.match(r'''^\s*(?:if\s+)?["']?\$(?:\{)?FC(?:\})?["']?''',
                    command, re.IGNORECASE)
    ]
    require(len(compiler_commands) == 5,
            "runner compiler invocation inventory")
    links = [command for command in compiler_commands if " -c " not in command]
    require(len(links) == 2, "runner must contain exactly two reviewed links")
    state_links = [line for line in links if "b2c_state_machine" in line]
    publisher_links = [line for line in links if "b2c_publisher_harness" in line]
    require(len(state_links) == 1 and len(publisher_links) == 1,
            "runner reviewed link outputs")
    require(
        all(name in state_links[0] for name in ("state.o", "driver.o"))
        and "SPOR64_B2C.o" not in state_links[0],
        "state-machine link inventory",
    )
    require(
        all(name in publisher_links[0] for name in (
            "SPOR64_B2C.o", "harness.o", "libGanlib.a", "libUtilib.a"
        )),
        "production publisher harness link inventory",
    )
    for forbidden in ("SPOR64_B2B.o", "SPOR64_A9.o", "FLU.o", "XDRTA2.o"):
        require(forbidden not in publisher_links[0],
                f"publisher harness links forbidden object {forbidden}")

    require(
        "for source_name in filmod LCMAUX lcmmod LCMTLC OPNMOD XDREED ganlib"
        in text
        and '"$ROOT/Ganlib/src/$source_name.f90"' in text,
        "runner exact GANLIB source loop",
    )
    for source in EXPECTED_PRODUCTION_SOURCES[7:]:
        require(source in text, f"runner omits production source {source}")
    scenario_commands = [
        command for command in commands if command.startswith("for scenario in ")
    ]
    require(
        scenario_commands == [
            "for scenario in wrong-token collision-spot collision-sour "
            "collision-aflux collision-dflux collision-adflux nan-flux "
            "inf-source over-positive over-negative boundary normal",
            "for scenario in valid wrong-token existing-spot nan range",
        ],
        f"runner exact scenario inventories differ: {scenario_commands}",
    )
    require(text.count("test_phase_a9b_b2c_publication_contract") == 1,
            "runner mutation-suite invocation")
    require(f"MUTATION-TESTS={MUTATION_TEST_COUNT}" in text,
            "runner exact mutation count")
    for disclosure in (
        "VALIDATION-STATE-MACHINE-EXECUTIONS=12",
        "PRODUCTION-PUBLISHER-SYNTHETIC-EXECUTIONS=5",
        "PRODUCTION-SOLVER-EXECUTIONS=0",
        "TRACKING-READS=0 TRANSPORT-SOLVES=0 DRAGON-RUNS=0",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(disclosure in text, f"runner missing disclosure {disclosure}")
    dragon_head = re.compile(
        r'''^\s*(?:(?:if|elif|while|until)\s+)?(?:!\s*)?["']?'''
        r'''(?:[^\s"']*/)?r?dragon["']?(?=\s|$)''',
        re.IGNORECASE,
    )
    require(not any(dragon_head.match(command) for command in commands),
            "runner cannot invoke Dragon")
    require("make -C src" not in text and 'make -C "$ROOT/src"' not in text,
            "runner cannot launch a production build")


def check_docs() -> None:
    root_readme = (ROOT / "README.md").read_text()
    iterative_readme = (ROOT / "validation/iterative/README.md").read_text()
    local_readme = (HERE / "README.md").read_text()
    for text, label in (
        (root_readme, "root README"),
        (iterative_readme, "iterative README"),
        (local_readme, "local README"),
    ):
        require("spot-real64-phase-a9b-b2c-publication" in text,
                f"{label} command")
        require("NOT-EVALUATED" in text, f"{label} convergence boundary")
    require("status `1`" in local_readme and "status `5`" in local_readme,
            "local README distinguishes B2B admission from B2C recheck")
    require("no crash-rollback claim" in local_readme,
            "local README rollback boundary")
    spot_plane = (ROOT / "data/SpotPlaneFS.c2m").read_text()
    require(re.search(r"(?i)\bR64\b", spot_plane) is None,
            "shipped SpotPlaneFS must remain default OFF")


def check_receipt(text: str | None = None, verify_digests: bool = True) -> None:
    require(digest(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256,
            "parent receipt hash")
    if text is None:
        require(RECEIPT.is_file(), "implementation receipt missing")
        text = RECEIPT.read_text()
    lines = [line for line in text.splitlines() if line]
    require(len(lines) == len(EXPECTED_RECEIPT_PATHS),
            "receipt entry count")
    paths: list[str] = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "receipt line format")
        claimed, relative = match.groups()
        paths.append(relative)
        if verify_digests:
            require(digest(ROOT / relative) == claimed,
                    f"receipt digest {relative}")
    require(tuple(paths) == EXPECTED_RECEIPT_PATHS,
            "receipt ordered path inventory")


def check_repository() -> None:
    for path in (
        B2C, B2B, FLU, DEPS, MAKEFILE, MANIFEST, RUNNER, PARENT_RECEIPT,
    ):
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    check_publisher_text(B2C.read_text())
    check_b2b_text(B2B.read_text())
    check_flu_text(FLU.read_text())
    check_global_publisher_callsites()
    check_build_text(MAKEFILE.read_text(), DEPS.read_text())
    check_manifest()
    check_runner(RUNNER.read_text())
    check_docs()
    check_receipt()


if __name__ == "__main__":
    try:
        check_repository()
    except ContractError as exc:
        raise SystemExit(f"SPOR64 PHASE-A9b-B2c STATIC FAILURE: {exc}")
    print("SPOR64 PHASE-A9b-B2c STATIC PASS")

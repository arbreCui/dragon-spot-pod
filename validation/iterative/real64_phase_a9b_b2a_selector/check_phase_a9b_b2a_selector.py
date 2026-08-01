#!/usr/bin/env python3
"""Fail-closed static checker for the production B2a selector subgate."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_manifest.json"
LOCAL_README = HERE / "README.md"
RUNNER = HERE / "run_phase_a9b_b2a_selector.sh"
RECEIPT = HERE / "phase_a9b_b2a_selector_receipt.sha256"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9b_spomoc_abi/"
    "phase_a9b_spomoc_abi_receipt.sha256"
)

PARENT_RECEIPT_SHA256 = (
    "eaa570a765afe5be29a71e554edade2ab515b1094d64d43bcfdcbb01f2082ef9"
)
RUNNER_SHA256 = (
    "f926c244f0cd0882252917db7d025baea8a75340a65ee4e2908087ba34e4f617"
)

FLU_ARGS = ["nentry", "hentry", "ientry", "jentry", "kentry"]
FLUGPI_ARGS = [
    "ipflux", "ipmacr", "itypec", "maxout", "maxinr", "epsout",
    "epsunk", "epsinr", "irebal", "ifritr", "iacitr", "coptio",
    "ileak", "b2", "ngroup", "nregio", "nmat", "nifiss", "leaksw",
    "refkef", "itpij", "iprint", "rec", "initfl", "nmerg", "imerg",
    "ipick", "imcaud", "limerg", "lr64",
]
FLUGPI_CALL_ARGS = [
    "ipflux", "ipmacr", "itypec", "maxout", "maxinr", "epsout",
    "epsunk", "epsinr", "irebal", "ifritr", "iacitr", "coptio",
    "ileak", "b2", "ngrp", "nreg", "nmat", "nifis", "leaksw",
    "refkef", "itpij", "iprint", "rec", "initfl", "nmerg", "imerg",
    "ipick", "imcaud", "limerg", "lr64",
]
FLUDRV_ARGS = [
    "iprt", "ipflux", "iptrk", "ipmacr", "ipsou", "iftrak", "ipsys",
    "iphase", "itpij", "cxdoor", "itranc", "title", "b2", "initfl",
    "lforw", "leaksw", "irebal", "ngrp", "nmat", "nifis", "nanis",
    "nlf", "nlin", "nfunl", "option", "nun", "maxinr", "epsinr",
    "maxout", "epsunk", "epsout", "ifritr", "iacitr", "itypec",
    "ileak", "nreg", "nsout", "matcod", "keyflx", "vol", "refkef",
    "nmerg", "imerg", "imcaud", "lr64",
]
FLUDRV_CALL_ARGS = [
    "iprint", "ipflux", "iptrk", "ipmacr", "ipsou", "iftrak", "ipsys",
    "iphase", "itpij", "cxdoor", "itranc", "title", "b2", "initfl",
    "lforw", "leaksw", "irebal", "ngrp", "nmat", "nifis", "nanis",
    "nlf", "nlin", "nfunl", "coptio", "nun", "maxinr", "epsinr",
    "maxout", "epsunk", "epsout", "ifritr", "iacitr", "itypec",
    "ileak", "nreg", "nsout", "matcod", "keyflx", "vol", "refkef",
    "nmerg", "imerg", "imcaud", "lr64",
]

FROZEN_HASHES = {
    "src/KDRDRV.F": "f364e8de2a3046dab93fe2aa944464f94f6bf4d39cc4bc12a494ca0e99e40062",
    "src/FLUGPT.f": "31197d0ff2fd742f5a074d6b601451f8b9d8c1594e3eecdbc6eda7811a51a167",
    "src/FLU2DR.f": "edd308054f2977999591a1e9df173212da1a7cb4a6519042295a96fd2c8bbc39",
    "src/XDRTA2.f": "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
    "src/SPOMOC.f90": "b5b565dac9292722dd89d41c26586e1150a08f1cc6048af57f296fbc4ab7842f",
    "src/SPOMOC_R64_BRIDGE.f90": "acde4d7c0331bdc47489c0d314d4b9e348944aa09253a27c1656af1fd00b0f15",
    "src/SPOR64_A8.f90": "eaa8110ce17e109db22e93a95d2b8d5495edfd57c18b1aa8676bc2cdaba9e8d7",
    "src/SPOR64_A9.f90": "f0ec2c7292986e4c048bf78108df3a3b8609ad393b77e0012a1a572a5d5c9b4a",
    "src/.dragon_deps.mk": "11c4871dc66d0dd7bf9ca067d3c2bfeb84375505d2f85cadee535e108d89cfb4",
    "src/Makefile": "7099dbec67c1ff9cc82deb5a2142ba3256dc7c7712257b96d38ddc4ef6429767",
}

EXPECTED_STATUS = {
    "r64_keyword_recognized": True,
    "r64_default": False,
    "r64_duplicate_rejected": True,
    "r64_route_executable": False,
    "default_runtime_route_changed": False,
    "production_route_connected": False,
    "spomoc_begin64_implemented": False,
    "host_ingress_implemented": False,
    "xdrta2_epoch_validated": False,
    "archive_implemented": False,
    "continuous_real64_lane": False,
    "runtime_provenance_validated": False,
    "actual_transport_response_validated": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
}

MAKE_BLOCK = (
    ".PHONY: spot-real64-phase-a9b-b2a-selector\n"
    "spot-real64-phase-a9b-b2a-selector :\n"
    "\tsh validation/iterative/real64_phase_a9b_b2a_selector/"
    "run_phase_a9b_b2a_selector.sh\n"
)

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_spomoc_abi/phase_a9b_spomoc_abi_receipt.sha256",
    "Ganlib/src/filmod.f90",
    "Ganlib/src/LCMAUX.f90",
    "Ganlib/src/lcmmod.f90",
    "Ganlib/src/LCMTLC.f90",
    "Ganlib/src/OPNMOD.f90",
    "Ganlib/src/XDREED.f90",
    "Ganlib/src/ganlib.f90",
    "src/KDRDRV.F",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLUGPT.f",
    "src/FLU2DR.f",
    "src/XDRTA2.f",
    "src/SPOMOC.f90",
    "src/SPOMOC_R64_BRIDGE.f90",
    "src/SPOR64_A8.f90",
    "src/SPOR64_A9.f90",
    "src/.dragon_deps.mk",
    "src/Makefile",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "validation/iterative/real64_phase_a9b_b2a_selector/README.md",
    "validation/iterative/real64_phase_a9b_b2a_selector/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2a_selector/check_phase_a9b_b2a_selector.py",
    "validation/iterative/real64_phase_a9b_b2a_selector/test_phase_a9b_b2a_selector_contract.py",
    "validation/iterative/real64_phase_a9b_b2a_selector/run_phase_a9b_b2a_selector.sh",
    "validation/iterative/real64_phase_a9b_b2a_selector/b2a_synthetic_ganlib.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/b2a_parser_driver.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/B2A_SELECTOR_ABI.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/compile_b2a_selector_anchor.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/compile_fail_nonlogical_limerg.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/compile_fail_nonlogical_lr64.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/compile_fail_nonlogical_driver.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/compile_fail_rank1_lr64.f90",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_flu_defined.txt",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_flu_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_flugpi_defined.txt",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_flugpi_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_fludrv_defined.txt",
    "validation/iterative/real64_phase_a9b_b2a_selector/expected_fludrv_unresolved.txt",
)


class GateError(RuntimeError):
    """Raised whenever the B2a boundary becomes weaker or wider."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_code(text: str) -> str:
    """Return fixed-form statement fields without comments or labels."""
    statements: list[str] = []
    for raw in text.splitlines():
        if not raw:
            continue
        if raw[0] in "*cC!":
            continue
        padded = raw.ljust(6)
        statements.append(padded[6:72])
    return "\n".join(statements) + "\n"


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text).upper()


def routine_args(text: str, name: str) -> list[str]:
    code = fixed_code(text)
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\((.*?)\)", code
    )
    require(match is not None, f"missing routine {name}")
    return [item.strip().lower() for item in match.group(1).split(",")]


def call_args(text: str, name: str) -> list[str]:
    code = fixed_code(text)
    matches = list(re.finditer(
        rf"(?is)\bcall\s+{re.escape(name)}\s*\((.*?)\)", code
    ))
    require(len(matches) == 1, f"expected one CALL {name}")
    return [item.strip().lower() for item in matches[0].group(1).split(",")]


def require_order(text: str, needles: list[str], message: str) -> None:
    position = -1
    for needle in needles:
        new_position = text.find(needle, position + 1)
        require(new_position >= 0, f"{message}: missing {needle}")
        require(new_position > position, f"{message}: order {needle}")
        position = new_position


def required_index(text: str, needle: str, start: int, message: str) -> int:
    position = text.find(needle, start)
    require(position >= 0, f"{message}: missing {needle}")
    return position


def check_source_contract(
    flu_text: str,
    flugpi_text: str,
    fludrv_text: str,
) -> None:
    require(routine_args(flu_text, "FLU") == FLU_ARGS, "FLU public ABI")
    require(routine_args(flugpi_text, "FLUGPI") == FLUGPI_ARGS,
            "FLUGPI exact 30-argument ABI")
    require(routine_args(fludrv_text, "FLUDRV") == FLUDRV_ARGS,
            "FLUDRV exact 45-argument ABI")
    require(call_args(flu_text, "FLUGPI") == FLUGPI_CALL_ARGS,
            "FLU to FLUGPI exact actuals")
    require(call_args(flu_text, "FLUDRV") == FLUDRV_CALL_ARGS,
            "FLU to FLUDRV exact actuals")

    gpi_code = fixed_code(flugpi_text)
    gpi = compact(gpi_code)
    require("LOGICALLEAKSW,REC,LIMERG,LR64" in gpi,
            "FLUGPI scalar LOGICAL tail declarations")
    require(gpi.count("LR64=.FALSE.") == 1, "LR64 default count")
    require(gpi.count("LR64=.TRUE.") == 1, "LR64 enable count")
    require(gpi.count("LIMERG=.NOT.REC") == 1, "LIMERG default rule")
    require(gpi.count("LIMERG=.TRUE.") == 1, "LIMERG HETE rule count")
    require(gpi.index("LR64=.FALSE.") < gpi.index("IF(REC)THEN"),
            "LR64 defaults before REC branch")
    require(gpi.index("LR64=.FALSE.") < gpi.index("CALLREDGET("),
            "LR64 defaults before token read")
    require(gpi.count("ELSEIF(CARLIR.EQ.'R64')THEN") == 1,
            "one exact R64 parser branch")
    branch = re.search(
        r"ELSEIF\(CARLIR\.EQ\.'R64'\)THEN(.*?)ELSEIF\(CARLIR\.EQ\.'EDIT'\)THEN",
        gpi,
    )
    require(branch is not None, "bounded R64 parser branch")
    r64_branch = branch.group(1)
    require("CALLREDGET" not in r64_branch, "R64 must be parameterless")
    require("IMCAUD" not in r64_branch, "R64 must not change MOCA")
    require_order(
        r64_branch,
        [
            "IF(LR64)THEN",
            "CALLXABORT('FLUGPI:DUPLICATER64KEYWORD.')",
            "RETURN",
            "ENDIF",
            "LR64=.TRUE.",
        ],
        "R64 duplicate fail-closed branch",
    )
    moca = re.search(
        r"ELSEIF\(CARLIR\.EQ\.'MOCA'\)THEN(.*?)ELSEIF\(CARLIR\.EQ\.'R64'\)THEN",
        gpi,
    )
    require(moca is not None, "bounded MOCA parser branch")
    require("LR64" not in moca.group(1), "MOCA cannot select R64")
    require("LIMERG" not in moca.group(1), "MOCA cannot affect metadata staging")
    require(len(re.findall(r"(?i)\bcall\s+REDGET\b", gpi_code)) == 20,
            "one-pass parser REDGET count")
    require(set(re.findall(r"(LCM[A-Z0-9_]+)\(", gpi)) ==
            {"LCMGET", "LCMLEN"},
            "FLUGPI LCM API inventory must remain read-only")
    require("DOIBM=1,NMAT" in gpi and "ENDDOLIMERG=.TRUE." in gpi,
            "LIMERG only after complete HETE loop")
    require(not re.search(r"(?i)\bSAVE\b[^\n]*(?:LR64|LIMERG)", gpi_code),
            "selector/staging state cannot be SAVE")
    require(not re.search(r"(?i)\bCOMMON\b[^\n]*(?:LR64|LIMERG)", gpi_code),
            "selector/staging state cannot be COMMON")
    require(not re.search(r"(?i)GETENV|GET_ENVIRONMENT_VARIABLE", gpi_code),
            "selector cannot use environment")

    flu_code = fixed_code(flu_text)
    flu = compact(flu_code)
    require("LOGICALLTABLE,REC,LEAKSW,LFORW,LIMERG,LR64" in flu,
            "FLU local scalar selector state")
    call_pos = required_index(flu, "CALLFLUGPI(", 0, "FLU parser call")
    guard_pos = required_index(flu, "IF(LR64)THEN", call_pos,
                               "FLU selected guard")
    abort_pos = required_index(
        flu, "CALLXABORT('FLU:R64SELECTEDBEFOREB2BINGRESS.')", guard_pos,
        "FLU selected abort",
    )
    return_pos = required_index(flu, "RETURN", abort_pos,
                                "FLU selected return")
    end_guard_pos = required_index(flu, "ENDIF", return_pos,
                                   "FLU selected guard end")
    require_order(
        flu,
        ["CALLFLUGPI(", "IF(LR64)THEN", "CALLXABORT(", "RETURN", "ENDIF"],
        "FLU selected guard",
    )
    pre_guard = flu[:end_guard_pos]
    cursor_exception = "CALLLCMSIX(IPMACR,'MACROLIB',1)"
    require(pre_guard.count(cursor_exception) == 1,
            "FLU one exact legacy MACROLIB cursor exception")
    pre_guard_without_cursor = pre_guard.replace(cursor_exception, "", 1)
    pre_guard_lcm_apis = set(re.findall(
        r"(LCM[A-Z0-9_]+)\(", pre_guard_without_cursor
    ))
    require(pre_guard_lcm_apis == {"LCMGET", "LCMGTC", "LCMLEN"},
            "FLU pre-selection LCM API inventory must remain read-only")
    mutation_pattern = (
        r"(?:CALL)?(?:LCMPTC|LCMPUT|LCMPDL|LCMPPD|LCMLID|LCMDID)\("
    )
    require(not re.search(mutation_pattern, flu[:end_guard_pos]),
            "no FLU LCM mutation API before selected return")
    mutations = [
        match.start()
        for match in re.finditer(mutation_pattern, flu)
    ]
    require(mutations and min(mutations) > end_guard_pos,
            "all FLU LCM mutations dominated by selected return")
    require("LR64=.FALSE." not in flu, "FLU cannot reset selected route")

    signature = "CALLLCMPTC(IPFLUX,'SIGNATURE',12,HSIGN)"
    link_macro = "CALLLCMPTC(IPFLUX,'LINK.MACRO',12,HPMACR)"
    link_track = "CALLLCMPTC(IPFLUX,'LINK.TRACK',12,HPTRK)"
    link_system = "CALLLCMPTC(IPFLUX,'LINK.SYSTEM',12,HPSYS)"
    imerge = "IF(LIMERG)CALLLCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERG)"
    require(flu.count(signature) == 1, "one deferred SIGNATURE write")
    require(flu.count(link_macro) == 1, "one deferred LINK.MACRO write")
    require(flu.count(link_track) == 2, "two legacy LINK.TRACK branches")
    require(flu.count(link_system) == 1, "one deferred LINK.SYSTEM write")
    require(flu.count(imerge) == 1, "one guarded final IMERGE write")
    require_order(
        flu[end_guard_pos:],
        [signature, link_macro, link_track, link_system, imerge],
        "deferred metadata class order",
    )
    signature_pos = flu.index(signature)
    reset_pos = flu.rfind("HSIGN='L_FLUX'", end_guard_pos, signature_pos)
    require(reset_pos >= 0, "deferred SIGNATURE must reset HSIGN")

    xdrta2_pos = required_index(flu, "CALLXDRTA2(IPTRK)", end_guard_pos,
                                "legacy XDRTA2 call")
    require(xdrta2_pos > end_guard_pos, "XDRTA2 after selected return")
    require(flu.count("CALLXDRTA2(IPTRK)") == 1,
            "legacy extra-actual XDRTA2 call frozen for B2a")
    require(flu.index("CALLFLUGPT(") > xdrta2_pos, "FLUGPT after XDRTA2")
    require(flu.index("CALLFLUDRV(") > xdrta2_pos, "FLUDRV after XDRTA2")

    drv_code = fixed_code(fludrv_text)
    drv = compact(drv_code)
    require("LOGICALLFORW,LEAKSW,LR64" in drv,
            "FLUDRV scalar LOGICAL selector")
    required_index(drv, "IF(LR64)THEN", 0, "FLUDRV selected guard")
    require_order(
        drv,
        [
            "IF(LR64)THEN",
            "CALLXABORT('FLUDRV:R64REQUIRESTHEB2BINGRESS.')",
            "RETURN",
            "ENDIF",
            "ALLOCATE(FLUXO",
            "JPMACR=LCMGID",
            "CALLSPOMOC_BEGIN(",
            "CALLFLU2DR(",
            "CALLSPOMOC_FINISH()",
        ],
        "FLUDRV guard and legacy sequence",
    )
    require("LR64=.FALSE." not in drv, "FLUDRV cannot fall back")
    for forbidden in ("SPOMOC_BEGIN64", "FLU2DR64", "SPOR64_A9"):
        require(forbidden not in flu and forbidden not in drv,
                f"B2a cannot connect {forbidden}")


def check_manifest() -> None:
    data = json.loads(MANIFEST.read_text())
    require(data["schema"] == "spot-real64-phase-a9b-b2a-selector-v1",
            "manifest schema")
    require(data["phase"] == "A9b-B2a", "manifest phase")
    require(data["classification"] ==
            "PRODUCTION-SELECTOR-AND-PRE-ADMISSION-WRITE-DEFERRAL",
            "manifest classification")
    require(data["authority"] == {
        "parent_commit": "0cc8d9083047c026b867dba2530e79c60bb14e2d",
        "parent_receipt": "validation/iterative/real64_phase_a9b_spomoc_abi/phase_a9b_spomoc_abi_receipt.sha256",
        "parent_receipt_sha256": PARENT_RECEIPT_SHA256,
    }, "manifest authority")
    require(data["status"] == EXPECTED_STATUS, "manifest status exact")
    selector = data["selector_contract"]
    require(selector["keyword"] == "R64", "selector keyword")
    require(selector["parameter_count"] == 0, "bare selector")
    require(selector["parse_passes"] == 1, "one parser pass")
    require(selector["default_each_flugpi_call"] is False,
            "selector default false")
    require(selector["orthogonal_to_moca"] is True, "MOCA orthogonality")
    require(selector["fallback_after_selection"] is False,
            "selected route no fallback")
    abi = data["host_abi"]
    require(abi == {
        "flu_public_arguments": 5,
        "flugpi_arguments": 30,
        "flugpi_tail": ["LIMERG", "LR64"],
        "fludrv_arguments": 45,
        "fludrv_tail": ["LR64"],
        "flu2dr_abi_changed": False,
        "xdrta2_abi_changed": False,
    }, "host ABI manifest")
    writes = data["write_deferral"]
    require(writes["flugpi_output_record_writes"] == 0,
            "FLUGPI write count")
    require(writes["selected_flu_flugpi_ipflux_record_writes"] == 0,
            "selected IPFLUX write count")
    require(writes["successful_off_final_record_identity"] is True,
            "OFF final record identity")
    require(writes["legacy_numerical_call_order_unchanged"] is True,
            "OFF numerical order")
    require(writes["legacy_floating_point_statement_order_unchanged"] is True,
            "OFF floating-point order")
    require(writes["metadata_mutation_trace_identity_claimed"] is False,
            "no redundant metadata trace claim")
    boundary = data["scope_boundaries"]
    require(boundary["complete_a7_admission_before_lcmsix_claimed"] is False,
            "no LCMSIX overclaim")
    require(boundary["existing_flugpt_flu2dr_abi_debt_fixed_here"] is False,
            "GPT ABI debt not widened into B2a")
    for key in ("model_completion", "relaxation_or_damping",
                "empirical_parameter", "solver_tolerance_changed"):
        require(boundary[key] is False, f"forbidden numerical change: {key}")
    for key in ("tracking_reads", "transport_solves", "dragon_runs"):
        require(boundary[key] == 0, f"zero runtime count: {key}")
    gate = data["short_gate"]
    require(gate["production_object_links"] == 0, "no production link")
    require(gate["synthetic_parser_links"] == 1, "one parser link")
    require(gate["synthetic_parser_cases"] == 12, "twelve parser cases")
    require(gate["negative_compiles"] == 4, "four negative compiles")


def check_frozen_inputs() -> None:
    require(digest(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256,
            "parent receipt hash")
    for relative, expected in FROZEN_HASHES.items():
        require(digest(ROOT / relative) == expected,
                f"frozen input changed: {relative}")


def _shell_commands(source: str) -> list[str]:
    """Return non-comment POSIX-shell logical lines."""
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
    """Validate the reviewed runner and its explanatory shell semantics."""
    if verify_hash:
        require(hashlib.sha256(source.encode()).hexdigest() == RUNNER_SHA256,
                "runner must match the reviewed exact command inventory")
    require(source.startswith("#!/bin/sh\nset -eu\n"),
            "runner must be strict POSIX shell")
    require(source.count(
        "FC=/opt/homebrew/bin/gfortran\nreadonly FC\n"
    ) == 1, "runner compiler binding must be exact and readonly")
    fc_assignments = re.findall(
        r"(?m)^[ \t]*(?:(?:export|readonly)[ \t]+)?FC[ \t]*=.*$",
        source,
    )
    require(fc_assignments == ["FC=/opt/homebrew/bin/gfortran"],
            "runner compiler path assigned exactly once")
    require(re.search(r"(?m)^[ \t]*(?:unset|read)\b[^\n]*\bFC\b", source)
            is None, "runner compiler binding cannot be unset or read")
    require("EXPECTED_FC_BANNER=" in source, "runner compiler identity")
    require("uname -s" in source and "uname -m" in source,
            "runner platform lock")
    require("test_phase_a9b_b2a_selector_contract" in source,
            "runner mutation suite")
    require("MUTATION-TESTS=55 NEGATIVE-COMPILES=4" in source,
            "runner short-gate counts")
    require("DRAGON-RUNS=0" in source, "runner Dragon boundary")
    require("PRODUCTION-ROUTE-CONNECTED=false" in source,
            "runner route boundary")
    require("OUTER-PICARD-CONVERGENCE=NOT-EVALUATED" in source,
            "runner Picard boundary")

    commands = _shell_commands(source)
    joined = "\n".join(commands)
    invocation_prefix = (
        r"(?:^|[|;&(])\s*(?:(?:if|elif|while|until)\s+)?(?:!\s*)?"
    )
    indirect = re.compile(
        invocation_prefix + r"(?:env|command|exec|eval|alias|xargs)\b",
        re.IGNORECASE | re.MULTILINE,
    )
    require(indirect.search(joined) is None,
            "runner cannot use indirect command dispatch")
    require(re.search(r"\b(?:sh|bash|zsh)[ \t]+-c\b", joined,
                      re.IGNORECASE) is None,
            "runner cannot invoke a secondary command shell")

    direct_tool = re.compile(
        invocation_prefix
        + r'''["']?(?:(?:/|\./|\.\./)[^\s"']*/)?'''
        + r'''(?:ld|ar|cc|gcc(?:-\d+)?|clang(?:-\d+)?|'''
        + r'''gfortran(?:-\d+)?|ifort|ifx|nvfortran|flang(?:-new)?)'''
        + r'''["']?(?=\s|$)''',
        re.IGNORECASE | re.MULTILINE,
    )
    require(direct_tool.search(joined) is None,
            "runner cannot invoke a direct compiler or linker")

    path_execution = re.compile(
        invocation_prefix
        + r'''["']?((?:/|\./|\.\./|\$(?:\{)?'''
        + r'''(?:BUILD_DIR|PROD_DIR|PARSER_DIR|ABI_DIR)(?:\})?/)'''
        + r'''[^\s;|&()"']*)''',
        re.IGNORECASE | re.MULTILINE,
    )
    path_heads = [match.group(1) for match in path_execution.finditer(joined)]
    require(path_heads == ["./b2a_parser", "./b2a_parser"],
            "only the two reviewed synthetic parser calls may execute")

    compiler_commands = [
        command for command in commands
        if re.match(r'''^\s*(?:if\s+)?["']?\$(?:\{)?FC(?:\})?["']?''',
                    command, re.IGNORECASE)
    ]
    require(len(compiler_commands) == 10,
            "runner compiler invocation count must be exact")
    link_commands = [
        command for command in compiler_commands if " -c " not in command
    ]
    require(len(link_commands) == 1, "exactly one compiler link command")
    parser_link = link_commands[0]
    require(parser_link.count(".o") == 3,
            "parser link object count must be exact")
    require("b2a_synthetic_ganlib.o" in parser_link,
            "parser link synthetic GANLIB")
    require("FLUGPI.o" in parser_link and "b2a_parser_driver.o" in parser_link,
            "parser link exact executable components")
    require(" -o b2a_parser" in parser_link, "parser link output")
    require("$PROD_DIR" not in parser_link and "SPOMOC.o" not in parser_link
            and "FLUDRV.o" not in parser_link and "FLU.o" not in parser_link,
            "production objects cannot be linked")

    lowered = source.lower()
    for forbidden in ("dragon_bin", "rdragon", " dragon ", " dragon\""):
        require(forbidden not in lowered, "runner cannot execute Dragon")
    require("for scenario in default r64 moca moca_r64 r64_moca lifetime rec_clean"
            in source, "nine positive parser scenarios")
    require(source.count("expect_parser_failure ") == 3,
            "three negative parser scenarios")


def check_docs_and_runner() -> None:
    root_readme = (ROOT / "README.md").read_text()
    iterative_readme = (ROOT / "validation/iterative/README.md").read_text()
    local = LOCAL_README.read_text()
    makefile = (ROOT / "Makefile").read_text()
    runner = RUNNER.read_text()
    synthetic_ganlib = (HERE / "b2a_synthetic_ganlib.f90").read_text()
    parser_driver = (HERE / "b2a_parser_driver.f90").read_text()
    require(MAKE_BLOCK in makefile, "Makefile B2a target")
    for text, label in ((root_readme, "root README"),
                        (iterative_readme, "iterative README"),
                        (local, "local README")):
        require("spot-real64-phase-a9b-b2a-selector" in text,
                f"{label} command")
        require("PRODUCTION-ROUTE-CONNECTED=false" in text,
                f"{label} route boundary")
        require("RADIAL-CONVERGENCE=NOT-EVALUATED" in text,
                f"{label} convergence boundary")
    require("metadata mutation trace" in local.lower(),
            "local metadata trace disclaimer")
    require("LCMSIX" in local, "local cursor disclaimer")
    validate_runner_text(runner)
    for forbidden in ("LCMPUT", "LCMPTC", "LCMPDL", "LCMPPD",
                      "LCMLID", "LCMDID"):
        require(forbidden not in synthetic_ganlib.upper(),
                f"synthetic GANLIB cannot expose {forbidden}")
    require("CALL FLUGPI" in parser_driver.upper(),
            "synthetic driver executes production parser")
    for forbidden in ("CALL FLU(", "CALL FLUDRV(", "CALL FLUGPT(",
                      "CALL FLU2DR(", "CALL XDRTA2"):
        require(forbidden not in parser_driver.upper(),
                f"synthetic driver cannot execute {forbidden}")


def check_receipt_shape() -> None:
    require(RECEIPT.exists(), "implementation receipt missing")
    lines = [line for line in RECEIPT.read_text().splitlines() if line]
    require(len(lines) == len(EXPECTED_RECEIPT_PATHS), "receipt entry count")
    paths = tuple(line.split(None, 1)[1] for line in lines)
    require(paths == EXPECTED_RECEIPT_PATHS, "receipt ordered path inventory")
    for line in lines:
        require(re.fullmatch(r"[0-9a-f]{64}  .+", line) is not None,
                "receipt line format")


def main() -> None:
    check_manifest()
    check_frozen_inputs()
    check_source_contract(
        (ROOT / "src/FLU.f").read_text(),
        (ROOT / "src/FLUGPI.f").read_text(),
        (ROOT / "src/FLUDRV.f").read_text(),
    )
    check_docs_and_runner()
    check_receipt_shape()
    print("SPOR64 PHASE-A9b-B2a SELECTOR STATIC PASS")


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"SPOR64 PHASE-A9b-B2a SELECTOR FAILURE: {error}")

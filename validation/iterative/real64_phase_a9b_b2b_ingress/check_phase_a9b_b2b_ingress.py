#!/usr/bin/env python3
"""Fail-closed, compile-only contract gate for the B2b host ingress."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FLU = ROOT / "src/FLU.f"
FLUGPI = ROOT / "src/FLUGPI.f"
B2B = ROOT / "src/SPOR64_B2B.f90"
XDRTA2 = ROOT / "src/XDRTA2.f"
ASM = ROOT / "src/ASM.f"
MANIFEST = HERE / "precision_manifest.json"
RUNNER = HERE / "run_phase_a9b_b2b_ingress.sh"
RECEIPT = HERE / "phase_a9b_b2b_ingress_receipt.sha256"
PARENT_RECEIPT = (
    ROOT
    / "validation/iterative/real64_phase_a9b_b2a_selector/"
    "phase_a9b_b2a_selector_receipt.sha256"
)

PARENT_RECEIPT_SHA256 = (
    "cb9469efbe9e98669e57be686b9d1366a4570696d6941e5823ba16283293d2c4"
)
RUNNER_SHA256 = (
    "b48f8a68c3ce7de60e2f75b66fda4020e342b5c741d5a1f84496d8ec1a013eb3"
)

INGRESS_ARGS = [
    "nentry", "hentry", "ientry", "jentry", "kentry", "itypec",
    "maxout", "maxinr", "epsout32", "epsunk32", "epsinr32",
    "irebal", "ifritr", "iacitr", "ileak", "initfl", "nmerg",
    "imerg", "iprint", "rec", "imcaud", "limerg", "ngrp_host",
    "nreg_host", "nmat_host", "nifis_host", "itpij_host",
    "itranc_host", "iphase_host", "leaksw_host", "lforw_host",
    "status", "cutoff_visit64",
]

FLU_INGRESS_ARGS = [
    "nentry", "hentry", "ientry", "jentry", "kentry", "itypec",
    "maxout", "maxinr", "epsout", "epsunk", "epsinr", "irebal",
    "ifritr", "iacitr", "ileak", "initfl", "nmerg", "imerg",
    "iprint", "rec", "imcaud", "limerg", "ngrp", "nreg", "nmat",
    "nifis", "itpij", "itranc", "iphase", "leaksw", "lforw",
    "ib2stat", "cutoff64",
]

STATUS_VALUES = {
    "SPOR64_B2B_ADMISSION_FAILED": 1,
    "SPOR64_B2B_CORE_FAILED": 2,
    "SPOR64_B2B_NOT_ACCEPTED": 3,
    "SPOR64_B2B_ACCEPTED_UNPUBLISHED": 4,
}

READ_ONLY_LCM_APIS = {
    "LCMGET", "LCMGTC", "LCMLEN", "LCMGID", "LCMGIL", "LCMGDL",
    "LCMLEL", "LCM_ENTRY_KIND",
}

EXPECTED_STATUS = {
    "r64_default": False,
    "production_r64_source_route_connected": True,
    "host_ingress_read_only": True,
    "host_ingress_coded": True,
    "xdrta2_zero_argument": True,
    "xdrta2_after_complete_admission": True,
    "global_xdrta2_abi_clean": False,
    "known_global_xdrta2_abi_debt": "src/ASM.f:101",
    "core_rendezvous_connected_compile_only": True,
    "accepted_publication_implemented": False,
    "continuous_real64_lane": False,
    "shipped_spotplanefs_r64_opt_in": False,
    "shipped_spotplanefs_creates_flux": True,
    "runtime_provenance_validated": False,
    "actual_transport_response_validated": False,
    "production_execution_authorized": False,
    "production_core_executions": 0,
    "validation_tracking_stream_reads": 0,
    "validation_transport_solves": 0,
    "synthetic_transport_calls": 0,
    "dragon_runs": 0,
    "empirical_parameters_added": False,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
}

EXPECTED_EVIDENCE = {
    "contract_tests": 40,
    "negative_compiles": 1,
    "synthetic_executions": 4,
    "production_objects_linked": 0,
    "production_objects_executed": 0,
}

EXPECTED_AUTHORITY = {
    "parent_commit": "356c4ce386232dd9bb06d5f3ee1693b09484fb4b",
    "parent_receipt": (
        "validation/iterative/real64_phase_a9b_b2a_selector/"
        "phase_a9b_b2a_selector_receipt.sha256"
    ),
    "parent_receipt_sha256": PARENT_RECEIPT_SHA256,
    "implementation_receipt": (
        "validation/iterative/real64_phase_a9b_b2b_ingress/"
        "phase_a9b_b2b_ingress_receipt.sha256"
    ),
    "compiler": "/opt/homebrew/bin/gfortran",
    "compiler_banner": "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0",
    "platform": "Darwin arm64",
}

MAKE_BLOCK = (
    ".PHONY: spot-real64-phase-a9b-b2b-ingress\n"
    "spot-real64-phase-a9b-b2b-ingress :\n"
    "\tsh validation/iterative/real64_phase_a9b_b2b_ingress/"
    "run_phase_a9b_b2b_ingress.sh\n"
)

EXPECTED_DEPENDENCIES = {
    "FLU.o": "FLU.o: SPOR64_B2B.o",
    "SPOR64_A8.o": "SPOR64_A8.o: SPOR64_A8_ACA.o",
    "SPOR64_A9.o": "SPOR64_A9.o: SPOR64_A8.o",
    "SPOR64_B2B.o": "SPOR64_B2B.o: SPOMOC.o SPOR64_A9.o",
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
    "src/SPOR64_B2B.f90",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/XDRTA2.f",
)

EXPECTED_RECEIPT_PATHS = (
    "validation/iterative/real64_phase_a9b_b2a_selector/phase_a9b_b2a_selector_receipt.sha256",
    "Ganlib/src/filmod.f90",
    "Ganlib/src/LCMAUX.f90",
    "Ganlib/src/lcmmod.f90",
    "Ganlib/src/LCMTLC.f90",
    "Ganlib/src/OPNMOD.f90",
    "Ganlib/src/XDREED.f90",
    "Ganlib/src/ganlib.f90",
    "src/ASM.f",
    "src/FLUGPI.f",
    "src/FLU.f",
    "src/XDRTA2.f",
    "src/SPOMOC.f90",
    "src/SPOMOC_R64_BRIDGE.f90",
    "src/SPOR64_A8_ACA.f90",
    "src/SPOR64_A8.f90",
    "src/MCGFFIR64_RANK_ADAPTER.f90",
    "src/SPOR64_A9.f90",
    "src/SPOR64_B2B.f90",
    "src/.dragon_deps.mk",
    "src/Makefile",
    "data/SpotPlaneFS.c2m",
    "Makefile",
    "README.md",
    "validation/iterative/README.md",
    "validation/iterative/real64_phase_a9b_b2b_ingress/README.md",
    "validation/iterative/real64_phase_a9b_b2b_ingress/precision_manifest.json",
    "validation/iterative/real64_phase_a9b_b2b_ingress/check_phase_a9b_b2b_ingress.py",
    "validation/iterative/real64_phase_a9b_b2b_ingress/test_phase_a9b_b2b_ingress_contract.py",
    "validation/iterative/real64_phase_a9b_b2b_ingress/run_phase_a9b_b2b_ingress.sh",
    "validation/iterative/real64_phase_a9b_b2b_ingress/compile_xdrta2_zeroarg_positive.f90",
    "validation/iterative/real64_phase_a9b_b2b_ingress/compile_xdrta2_extra_actual_negative.f90",
    "validation/iterative/real64_phase_a9b_b2b_ingress/b2b_synthetic_dispatch.f90",
    "validation/iterative/real64_phase_a9b_b2b_ingress/b2b_synthetic_dispatch_driver.f90",
    "validation/iterative/real64_phase_a9b_b2b_ingress/expected_b2b_defined.txt",
    "validation/iterative/real64_phase_a9b_b2b_ingress/expected_b2b_unresolved.txt",
    "validation/iterative/real64_phase_a9b_b2b_ingress/expected_flu_defined.txt",
    "validation/iterative/real64_phase_a9b_b2b_ingress/expected_flu_unresolved.txt",
)


class GateError(RuntimeError):
    """Raised when the B2b boundary is weakened or widened."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_statements(text: str) -> list[str]:
    statements: list[str] = []
    current = ""
    for raw in text.splitlines():
        if not raw or raw[0] in "*cC!":
            continue
        line = raw.expandtabs(8).ljust(6)
        field = line[6:72].strip()
        if not field:
            continue
        continuation = len(line) > 5 and line[5] not in " 0"
        if continuation:
            require(bool(current), "orphan fixed-form continuation")
            current += field
        else:
            if current:
                statements.append(current)
            current = field
    if current:
        statements.append(current)
    return statements


def free_statements(text: str) -> list[str]:
    statements: list[str] = []
    current = ""
    continuing = False
    for raw in text.splitlines():
        code = raw.split("!", 1)[0].strip()
        if not code:
            continue
        if continuing and code.startswith("&"):
            code = code[1:].lstrip()
        has_continuation = code.endswith("&")
        if has_continuation:
            code = code[:-1].rstrip()
        current = f"{current} {code}".strip() if current else code
        continuing = has_continuation
        if not continuing:
            statements.append(current)
            current = ""
    require(not continuing, "unterminated free-form continuation")
    return statements


def dense(statement: str) -> str:
    return re.sub(r"\s+", "", statement).upper()


def call_name(statement: str) -> str | None:
    match = re.search(r"(?i)\bCALL\s+([A-Z][A-Z0-9_$]*)\b", statement)
    return match.group(1).upper() if match else None


def call_args(statement: str, name: str) -> list[str]:
    match = re.search(
        rf"(?is)\bCALL\s+{re.escape(name)}\s*(?:\((.*)\))?\s*$",
        statement,
    )
    require(match is not None, f"missing CALL {name}")
    if match.group(1) is None or not match.group(1).strip():
        return []
    return [part.strip().lower() for part in match.group(1).split(",")]


def routine_region(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bSUBROUTINE\s+{re.escape(name)}\s*\(.*?"
        rf"\bEND\s+SUBROUTINE\s+{re.escape(name)}\b",
        text,
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def routine_args(text: str, name: str) -> list[str]:
    region = routine_region(text, name)
    statement = free_statements(region)[0]
    match = re.search(rf"(?is)SUBROUTINE\s+{name}\s*\((.*)\)", statement)
    require(match is not None, f"missing {name} declaration")
    return [part.strip().lower() for part in match.group(1).split(",")]


def matching_if_end(statements: list[str], start: int) -> int:
    depth = 0
    for index in range(start, len(statements)):
        item = dense(statements[index])
        if re.match(r"^IF\(.*\)THEN$", item):
            depth += 1
        elif item in {"ENDIF", "END IF"}:
            depth -= 1
            if depth == 0:
                return index
    raise GateError("unterminated selected IF block")


def lcm_apis(text: str) -> set[str]:
    function_style = {
        item.upper()
        for item in re.findall(r"(?i)\b(LCM[A-Z0-9_$]+)\s*\(", text)
    }
    call_style = {
        item.upper()
        for item in re.findall(r"(?i)\bCALL\s+(LCM[A-Z0-9_$]+)\b", text)
    }
    return function_style | call_style


def check_flu(flu_text: str) -> None:
    statements = fixed_statements(flu_text)
    packed = [dense(item) for item in statements]
    parser_calls = [i for i, item in enumerate(packed)
                    if "CALLFLUGPI(" in item]
    require(len(parser_calls) == 1, "one FLUGPI call")
    ingress_calls = [i for i, item in enumerate(statements)
                     if call_name(item) == "SPOR64_B2B_INGRESS"]
    require(len(ingress_calls) == 1, "one SPOR64_B2B_INGRESS call")
    require(call_args(statements[ingress_calls[0]],
                      "SPOR64_B2B_INGRESS") == FLU_INGRESS_ARGS,
            "FLU to B2b exact actual list")

    selected_starts = [i for i, item in enumerate(packed)
                       if item == "IF(LR64)THEN" and i > parser_calls[0]]
    require(len(selected_starts) == 1, "one post-parser R64 branch")
    start = selected_starts[0]
    require(start == parser_calls[0] + 1,
            "R64 dispatch immediately follows FLUGPI")
    end = matching_if_end(statements, start)
    require(start < ingress_calls[0] < end,
            "ingress call must be inside selected branch")
    branch = statements[start + 1:end]
    branch_packed = [dense(item) for item in branch]
    branch_calls = [call_name(item) for item in branch if call_name(item)]
    require(branch_calls.count("SPOR64_B2B_INGRESS") == 1,
            "selected branch calls ingress once")
    require("FLUDRV" not in branch_calls and "FLUGPT" not in branch_calls,
            "selected branch cannot enter a legacy driver")
    require("XDRTA2" not in branch_calls,
            "selected branch delegates XDRTA2 to ingress")
    require(not (lcm_apis("\n".join(branch)) - set()),
            "selected branch cannot touch LCM")

    depth = 1
    outer_returns = 0
    for item in branch_packed:
        if re.match(r"^IF\(.*\)THEN$", item):
            depth += 1
        elif item in {"ENDIF", "END IF"}:
            depth -= 1
        elif item == "RETURN" and depth == 1:
            outer_returns += 1
    require(outer_returns == 1, "selected branch has one outer RETURN")
    require(branch_packed[-1] == "RETURN",
            "selected branch terminates with explicit RETURN")
    require(not any("LR64=.FALSE." in item for item in packed[parser_calls[0]:]),
            "selected route cannot reset LR64 or fall back")

    legacy_xdr = [i for i, item in enumerate(statements)
                  if call_name(item) == "XDRTA2"]
    require(len(legacy_xdr) == 1, "one legacy FLU XDRTA2 call")
    require(call_args(statements[legacy_xdr[0]], "XDRTA2") == [],
            "legacy XDRTA2 must be bare zero-argument")
    require(dense(statements[legacy_xdr[0]]).endswith("CALLXDRTA2"),
            "legacy XDRTA2 uses the canonical bare call")
    legacy_driver = [i for i, item in enumerate(statements)
                     if call_name(item) == "FLUDRV"]
    require(len(legacy_driver) == 1, "one legacy FLUDRV call")
    require(end < legacy_xdr[0] < legacy_driver[0],
            "legacy XDRTA2 remains after selected return and before FLUDRV")

    use_dense = dense("\n".join(statements[:20]))
    for name in ("SPOR64_B2B_INGRESS", *STATUS_VALUES):
        require(name in use_dense, f"FLU imports {name}")


def check_flugpi(flugpi_text: str) -> None:
    statements = fixed_statements(flugpi_text)
    packed = [dense(item) for item in statements]
    require(lcm_apis(flugpi_text) == {"LCMLEN", "LCMGET"},
            "FLUGPI remains read-only with exact LCM API inventory")
    lr64_false = [i for i, item in enumerate(packed) if item == "LR64=.FALSE."]
    redget = [i for i, item in enumerate(statements)
              if call_name(item) == "REDGET"]
    require(len(lr64_false) == 1 and redget and lr64_false[0] < redget[0],
            "R64 defaults OFF before parsing")

    guarded_reads = (
        ("CALLLCMLEN(IPFLUX,'STATE-VECTOR',ILCML1,ITYLCM)",
         "IF((ILCML1.NE.NSTATE).OR.(ITYLCM.NE.1))THEN",
         "CALLLCMGET(IPFLUX,'STATE-VECTOR',ISTATE)"),
        ("CALLLCMLEN(IPFLUX,'EPS-CONVERGE',ILCML1,ITYLCM)",
         "IF((ILCML1.NE.5).OR.(ITYLCM.NE.2))THEN",
         "CALLLCMGET(IPFLUX,'EPS-CONVERGE',EPSCON)"),
        ("CALLLCMLEN(IPFLUX,'IMERGE-LEAK',ILCML1,ITYLCM)",
         "IF((ILCML1.NE.NMAT).OR.(ITYLCM.NE.1))THEN",
         "CALLLCMGET(IPFLUX,'IMERGE-LEAK',IMERG)"),
    )
    for metadata, guard, payload in guarded_reads:
        require(packed.count(metadata) == 1, f"one FLUGPI metadata {metadata}")
        require(packed.count(guard) == 1, f"one FLUGPI guard {guard}")
        require(packed.count(payload) == 1, f"one FLUGPI payload {payload}")
        meta_pos = packed.index(metadata)
        guard_pos = packed.index(guard)
        payload_pos = packed.index(payload)
        require(meta_pos < guard_pos < payload_pos,
                f"FLUGPI metadata precedes payload {payload}")
        require(packed[guard_pos + 1].startswith("CALLXABORT(") and
                packed[guard_pos + 2] == "RETURN" and
                packed[guard_pos + 3] == "ENDIF",
                f"FLUGPI guard fails closed {payload}")

    b2_contract = (
        "CALLLCMLEN(IPFLUX,'B2HETE',ILCML1,ITYLCM)",
        "IF(.NOT.(((ILCML1.EQ.0).AND.(ITYLCM.EQ.99)).OR."
        "((ILCML1.EQ.3).AND.(ITYLCM.EQ.2))))THEN",
        "CALLLCMLEN(IPFLUX,'B2B1HOM',ILCML2,ITYLCM)",
        "IF(.NOT.(((ILCML2.EQ.0).AND.(ITYLCM.EQ.99)).OR."
        "((ILCML2.EQ.1).AND.(ITYLCM.EQ.2))))THEN",
        "CALLLCMGET(IPFLUX,'B2HETE',BSDIR)",
        "CALLLCMGET(IPFLUX,'B2B1HOM',BSDIR(5))",
    )
    positions = []
    for statement in b2_contract:
        require(packed.count(statement) == 1,
                f"one FLUGPI B2 contract statement {statement}")
        positions.append(packed.index(statement))
    require(positions == sorted(positions),
            "FLUGPI validates both optional B2 records before reads")

    macro_b2_contract = (
        "CALLLCMLEN(IPMACR,'B2HETE',ILCMLN,ITYLCM)",
        "IF(.NOT.(((ILCMLN.EQ.0).AND.(ITYLCM.EQ.99)).OR."
        "((ILCMLN.EQ.3).AND.(ITYLCM.EQ.2))))THEN",
        "CALLLCMGET(IPMACR,'B2HETE',BSDIR)",
        "CALLLCMLEN(IPMACR,'B2B1HOM',ILCMLN,ITYLCM)",
        "IF(.NOT.(((ILCMLN.EQ.0).AND.(ITYLCM.EQ.99)).OR."
        "((ILCMLN.EQ.1).AND.(ITYLCM.EQ.2))))THEN",
        "CALLLCMGET(IPMACR,'B2B1HOM',BSDIR(5))",
    )
    positions = []
    for statement in macro_b2_contract:
        require(packed.count(statement) == 1,
                f"one FLUGPI IDEM contract statement {statement}")
        positions.append(packed.index(statement))
    require(positions == sorted(positions),
            "FLUGPI IDEM validates optional B2 records before reads")


def check_ingress(b2b_text: str) -> None:
    require(re.search(r"(?im)^\s*MODULE\s+SPOR64_B2B\s*$", b2b_text)
            is not None, "SPOR64_B2B module")
    require(routine_args(b2b_text, "SPOR64_B2B_INGRESS") == INGRESS_ARGS,
            "exact SPOR64_B2B_INGRESS ABI")
    upper = b2b_text.upper()
    module_statements = [dense(item) for item in free_statements(b2b_text)]
    for name, value in STATUS_VALUES.items():
        require(re.search(rf"(?is)\b{name}\s*=\s*{value}\b", upper)
                is not None, f"status value {name}")
        require(any("PUBLIC" in item and name in item
                    for item in module_statements), f"public status {name}")

    require(not re.search(r"(?i)\bSAVE\b|\bCOMMON\b", b2b_text),
            "ingress has no SAVE/COMMON state")
    require(not re.search(r"(?im)^\s*(READ|REWIND|OPEN|BACKSPACE|ENDFILE)\b",
                          b2b_text), "ingress performs no stream I/O")
    require(not re.search(r"(?i)\bCALL\s+XABORT\b", b2b_text),
            "ingress returns status instead of XABORT")
    apis = lcm_apis(b2b_text)
    require(apis == READ_ONLY_LCM_APIS,
            f"exact read-only ingress LCM API inventory: {sorted(apis)}")
    require(not re.search(r"(?i)\bSPOMOC_(BEGIN|PUBLISH|CAPTURE)", b2b_text),
            "B2b cannot publish or arm diagnostics")

    region = routine_region(b2b_text, "SPOR64_B2B_INGRESS")
    statements = free_statements(region)
    packed = [dense(item) for item in statements]
    topology = (
        "IF(NENTRY/=6)RETURN",
        "IF(HENTRY(1)/='FLUX')RETURN",
        "IF(HENTRY(2)/='MACRO0')RETURN",
        "IF(HENTRY(3)/='TRACK')RETURN",
        "IF(HENTRY(4)/='TRACK_F')RETURN",
        "IF(HENTRY(5)/='SYSTEM')RETURN",
        "IF(HENTRY(6)/='FSOURCE')RETURN",
        "IF(IENTRY(4)/=3)RETURN",
        "IF(JENTRY(1)/=1)RETURN",
        "IF(ANY(JENTRY(2:6)/=2))RETURN",
        "IFTRAK=FILUNIT(KENTRY(4))",
    )
    for statement in topology:
        require(statement in packed, f"frozen topology statement {statement}")

    host_state = (
        "IF(.NOT.REC.OR.LIMERG)RETURN",
        "IF(ITYPEC/=0.OR.MAXOUT/=500.OR.MAXINR/=740)RETURN",
        "IF(IREBAL/=1.OR.IFRITR/=3.OR.IACITR/=3)RETURN",
        "IF(ILEAK/=0.OR.INITFL/=1.OR.NMERG/=1)RETURN",
        "IF(ANY(IMERG/=1))RETURN",
        "IF(IMCAUD/=0.OR.SPOMOC_ACTIVE())RETURN",
    )
    for statement in host_state:
        require(statement in packed, f"frozen host state {statement}")

    require("INITIAL_FLUX64(:,IG)=REAL(FLUX_STAGE32,REAL64)" in packed,
            "single binary32-to-binary64 initial-flux promotion")
    require("FIXED_SOURCE64(:,IG)=REAL(SOURCE_STAGE32,REAL64)" in packed,
            "single binary32-to-binary64 source promotion")
    require(not re.search(r"(?i)\b(alpha|omega|relax(?:ation)?|tuning|"
                          r"fitted|clipping|floor)\b", b2b_text),
            "ingress contains no empirical control")
    false_pos = [i for i, item in enumerate(packed)
                 if item == "ADMISSION_COMPLETE=.FALSE."]
    true_pos = [i for i, item in enumerate(packed)
                if item == "ADMISSION_COMPLETE=.TRUE."]
    require(len(false_pos) == 1 and len(true_pos) == 1,
            "single false-to-true admission latch")
    require(false_pos[0] < true_pos[0], "admission latch order")
    require(any(item == "STATUS=SPOR64_B2B_ADMISSION_FAILED"
                for item in packed[:true_pos[0]]),
            "fail-closed initial status")

    xdr_calls = [i for i, item in enumerate(statements)
                 if call_name(item) == "XDRTA2"]
    core_calls = [i for i, item in enumerate(statements)
                  if call_name(item) == "FLU2DR64_CORE"]
    require(len(xdr_calls) == 1, "one ingress XDRTA2 call")
    require(len(core_calls) == 1, "one ingress FLU2DR64_CORE call")
    xdr_pos, core_pos = xdr_calls[0], core_calls[0]
    require(true_pos[0] < xdr_pos < core_pos,
            "complete admission then XDRTA2 then core")
    require(call_args(statements[xdr_pos], "XDRTA2") == [],
            "ingress XDRTA2 is zero-argument")
    require(packed[xdr_pos] == "CALLXDRTA2",
            "ingress XDRTA2 uses the canonical bare call")
    require(any(item == "IF(.NOT.ADMISSION_COMPLETE)RETURN"
                for item in packed[true_pos[0] + 1:xdr_pos]),
            "explicit admission-complete guard before XDRTA2")
    between_calls = [call_name(item) for item in statements[true_pos[0] + 1:]
                     if call_name(item)]
    require(between_calls[:2] == ["XDRTA2", "FLU2DR64_CORE"],
            "XDRTA2 and core are the first two post-admission calls")
    require(between_calls == ["XDRTA2", "FLU2DR64_CORE"],
            "no extra post-admission side-effect call")
    require(not any(api in dense("\n".join(statements[true_pos[0] + 1:]))
                    for api in READ_ONLY_LCM_APIS),
            "no host read after complete admission")

    allowed_calls = {
        "LCMGET", "LCMGTC", "LCMLEN", "LCMLEL", "LCMGDL",
        "XDRTA2", "FLU2DR64_CORE",
    }
    actual_calls = {call_name(item) for item in statements if call_name(item)}
    require(actual_calls <= allowed_calls,
            f"ingress call inventory cannot add an operator: {actual_calls}")

    guard_contract = (
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPFLUX,'SIGNATURE',3,12,'L_FLUX'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPMACR,'SIGNATURE',3,12,'L_MACROLIB'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPTRK,'SIGNATURE',3,12,'L_TRACK'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPSYS,'SIGNATURE',3,12,'L_PIJ'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPSOU,'SIGNATURE',3,12,'L_SOURCE'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'B2HETE'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPFLUX,'B2B1HOM'))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'EPS-CONVERGE',5,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'IMERGE-LEAK',NMAT,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPMACR,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPMACR,'SPOT-FROZEN',1,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPMACR,'SPOT-KEFF',1,2))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPSYS,'LINK.MACRO',3,12,'MACRO0'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPSYS,'LINK.TRACK',3,12,'TRACK'))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSYS,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSYS,'SPOT-LEAK1D',NGRP,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'TITLE',18,3))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPTRK,'TRACK-TYPE',3,12,'MCCG'))RETURN",
        "IF(.NOT.CHARACTER_RECORD_MATCHES(IPTRK,'LINK.FTRACK',3,12,'TRACK_F'))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'MCCG-STATE',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'REAL-PARAM',4,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'MATCOD',NREG,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'VOLUME',NREG,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'KEYFLX$ANIS',NREG,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'KEYCUR$MCCG',NSOUT,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'NZON$MCCG',NUNKNO,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'V$MCCG',NUNKNO,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPTRK,'ALBEDO',NSOUT,2))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPSOU,'NORM-FS'))RETURN",
        "IF(.NOT.ABSENT_RECORD(IPSOU,'NBS'))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSOU,'STATE-VECTOR',NSTATE,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSOU,'SPOT-FROZEN',1,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSOU,'SPOT-KEFF',1,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSOU,'SPOT-QINT',NGRP,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPFLUX,'FLUX',NGRP,10))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSOU,'DSOUR',1,10))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPMACR,'GROUP',NGRP,10))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPMACR,'NUSIGF',NMAT*NIFIS,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPMACR,'NJJS00',NMAT,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPMACR,'IJJS00',NMAT,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPMACR,'IPOS00',NMAT,1))RETURN",
        "IF(.NOT.RECORD_MATCHES(IPSYS,'GROUP',NGRP,10))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPSYS,'DRAGON-TXSC',NMAT+1,2))RETURN",
        "IF(.NOT.RECORD_MATCHES(KPSYS,'DRAGON-S0XSC',NMAT+1,2))RETURN",
    )
    for guard in guard_contract:
        require(packed.count(guard) == 1, f"one exact ingress guard {guard}")

    for payload_pos, payload in enumerate(packed):
        match = re.match(r"CALLLCM(?:GET|GTC)\(([^,]+),'([^']+)'", payload)
        if match is None:
            continue
        object_name, record_name = match.groups()
        if record_name == "SCAT00":
            continue
        guarded = any(
            f"RECORD_MATCHES({object_name},'{record_name}'" in earlier
            for earlier in packed[:payload_pos]
        )
        require(guarded,
                f"metadata guard precedes {object_name}/{record_name} read")

    list_reads = (
        ("CALLLCMLEL(JPFLUX,IG,ILONG,ITYLCM)",
         "CALLLCMGDL(JPFLUX,IG,FLUX_STAGE32)"),
        ("CALLLCMLEL(KPSOURCE,IG,ILONG,ITYLCM)",
         "CALLLCMGDL(KPSOURCE,IG,SOURCE_STAGE32)"),
    )
    for metadata, payload in list_reads:
        require(packed.count(metadata) == 1 and packed.count(payload) == 1,
                f"one guarded list payload {payload}")
        require(packed.index(metadata) < packed.index(payload),
                f"LCMLEL precedes {payload}")

    scat_len = "CALLLCMLEN(KPMACR,'SCAT00',ILONG,ITYLCM)"
    scat_guard = "IF(ILONG<0.OR.ILONG>MAX_SCAT.OR.ITYLCM/=2)RETURN"
    scat_read = "CALLLCMGET(KPMACR,'SCAT00',SCAT_STAGE32)"
    require(packed.count(scat_len) == 1 and packed.count(scat_guard) == 1 and
            packed.count(scat_read) == 1 and
            packed.index(scat_len) < packed.index(scat_guard) <
            packed.index(scat_read), "SCAT00 length/type guard precedes read")
    funk_len = "CALLLCMLEN(KPSYS,'FUNKNO$USS',ILONG,ITYLCM)"
    funk_absent = "IF(ILONG/=0.OR.ITYLCM/=99)RETURN"
    require(packed.count(funk_len) == 1 and packed.count(funk_absent) == 1 and
            packed.index(funk_len) < packed.index(funk_absent),
            "FUNKNO$USS absence is checked")

    expected_core_call = dense(
        "call FLU2DR64_CORE(jpsys,iptrk,iftrak,iprint,title,"
        "keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur,"
        "matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off,"
        "nscat_off,scat_off32,fixed_source64,initial_flux64,"
        "real(epsinr32,real64),real(epsunk32,real64),"
        "real(epsout32,real64),terminal_flux64,terminal_source64,"
        "cutoff_visit64,accepted,core_ok)"
    )
    require(packed[core_pos] == expected_core_call,
            "exact frozen FLU2DR64_CORE actual list")
    expected_status_tail = [
        "IF(.NOT.CORE_OK)THEN",
        "STATUS=SPOR64_B2B_CORE_FAILED",
        "ELSEIF(.NOT.ACCEPTED)THEN",
        "STATUS=SPOR64_B2B_NOT_ACCEPTED",
        "ELSE",
        "STATUS=SPOR64_B2B_ACCEPTED_UNPUBLISHED",
        "ENDIF",
    ]
    require(packed[core_pos + 1:core_pos + 8] == expected_status_tail,
            "exact fail-closed terminal status mapping")


def check_xdrta2(xdr_text: str, asm_text: str) -> None:
    statements = fixed_statements(xdr_text)
    declaration = dense(statements[0])
    require(declaration == "SUBROUTINEXDRTA2",
            "production XDRTA2 has exactly zero arguments")
    asm_calls = [item for item in fixed_statements(asm_text)
                 if call_name(item) == "XDRTA2"]
    require(len(asm_calls) == 1 and
            call_args(asm_calls[0], "XDRTA2") == ["iptrk"],
            "known global XDRTA2 ABI debt remains exactly src/ASM.f:101")


def check_manifest(data: dict[str, object]) -> None:
    require(data.get("stage") == "PHASE-A9b-B2b", "manifest stage")
    require(data.get("authority") == EXPECTED_AUTHORITY,
            "manifest authority boundary")
    require(data.get("status") == EXPECTED_STATUS, "manifest status boundary")
    require(data.get("validation_evidence") == EXPECTED_EVIDENCE,
            "manifest validation evidence")
    require(tuple(data.get("production_compile_only_sources", ())) ==
            EXPECTED_PRODUCTION_SOURCES, "manifest production source inventory")


def check_runner(text: str) -> None:
    require(hashlib.sha256(text.encode()).hexdigest() == RUNNER_SHA256,
            "runner hash")
    require("FC=/opt/homebrew/bin/gfortran" in text and "readonly FC" in text,
            "runner freezes compiler path")
    require('shasum -a 256 -c "$RECEIPT"' in text,
            "runner verifies implementation receipt before work")
    require("EXPECTED_PARENT_HASH=" + PARENT_RECEIPT_SHA256 in text,
            "runner freezes parent receipt hash")
    for forbidden in ("rdragon", "/Dragon", "mpirun", "mpiexec",
                      "make -C src", "make -C \"$ROOT/src\""):
        require(forbidden.lower() not in text.lower(),
                f"runner forbids {forbidden}")
    for source in EXPECTED_PRODUCTION_SOURCES:
        name = Path(source).name
        require(name in text or Path(name).stem in text,
                f"runner compiles declared source {source}")
    require(text.count(' -o "$SYN_DIR/b2b_synthetic_dispatch"') == 1,
            "one synthetic-only link")
    require('"$SYN_DIR/b2b_synthetic_dispatch" "$scenario"' in text,
            "only reviewed synthetic executable is invoked")
    require("CONTRACT-TESTS=40" in text and "NEGATIVE-COMPILES=1" in text and
            "SYNTHETIC-EXECUTIONS=4" in text,
            "runner discloses exact short validation counts")
    require("PRODUCTION-OBJECT-LINKS=0" in text,
            "runner discloses zero production links")
    require("TRANSPORT-SOLVES=0" in text and "DRAGON-RUNS=0" in text,
            "runner discloses no transport/Dragon")


def check_makefile(makefile: str) -> None:
    require(makefile.count(MAKE_BLOCK) == 1,
            "one exact top-level B2b Make target")
    require(makefile.count("spot-real64-phase-a9b-b2b-ingress") == 2,
            "B2b Make target has no extra definition")


def check_dependencies(dependency_text: str) -> None:
    deps = dependency_text.splitlines()
    for target, expected in EXPECTED_DEPENDENCIES.items():
        actual = [line for line in deps if line.startswith(f"{target}:")]
        require(actual == [expected], f"exact generated dependency {target}")


def check_build_and_docs() -> None:
    check_makefile((ROOT / "Makefile").read_text())
    check_dependencies((ROOT / "src/.dragon_deps.mk").read_text())
    src_makefile = (ROOT / "src/Makefile").read_text()
    require("-include $(DEPS_MK)" in src_makefile,
            "production Makefile includes generated dependencies")

    root_readme = (ROOT / "README.md").read_text()
    iterative_readme = (ROOT / "validation/iterative/README.md").read_text()
    local_readme = (HERE / "README.md").read_text()
    for text, label in ((root_readme, "root README"),
                        (iterative_readme, "iterative README"),
                        (local_readme, "local README")):
        require("spot-real64-phase-a9b-b2b-ingress" in text,
                f"{label} command")
        require("GLOBAL-XDRTA2-ABI-CLEAN=false" in text,
                f"{label} global ABI disclaimer")
    for text, label in ((root_readme, "root README"),
                        (iterative_readme, "iterative README")):
        require("PRODUCTION-R64-SOURCE-ROUTE-CONNECTED=true" in text,
                f"{label} source-route status")
        require("RADIAL-CONVERGENCE=NOT-EVALUATED" in text,
                f"{label} convergence boundary")

    spot_plane = (ROOT / "data/SpotPlaneFS.c2m").read_text()
    require(re.search(r"(?im)^FLUX\s*:=\s*FLU:", spot_plane) is not None,
            "shipped SpotPlaneFS still creates FLUX through FLU")
    require(re.search(r"(?i)\bR64\b", spot_plane) is None,
            "shipped SpotPlaneFS remains default OFF")


def check_receipt() -> None:
    require(digest(PARENT_RECEIPT) == PARENT_RECEIPT_SHA256,
            "parent receipt hash")
    require(RECEIPT.is_file(), "implementation receipt missing")
    lines = [line for line in RECEIPT.read_text().splitlines() if line]
    require(len(lines) == len(EXPECTED_RECEIPT_PATHS),
            "receipt entry count")
    paths = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "receipt line format")
        claimed, relative = match.groups()
        paths.append(relative)
        require(digest(ROOT / relative) == claimed,
                f"receipt digest {relative}")
    require(tuple(paths) == EXPECTED_RECEIPT_PATHS,
            "receipt ordered path inventory")


def check_all() -> None:
    require(B2B.is_file(), "missing production SPOR64_B2B.f90")
    check_flu(FLU.read_text())
    check_flugpi(FLUGPI.read_text())
    check_ingress(B2B.read_text())
    check_xdrta2(XDRTA2.read_text(), ASM.read_text())
    check_manifest(json.loads(MANIFEST.read_text()))
    check_runner(RUNNER.read_text())
    check_build_and_docs()
    check_receipt()


def main() -> int:
    try:
        check_all()
    except (GateError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"SPOR64 PHASE-A9b-B2b FAILURE: {exc}")
        return 1
    print("SPOR64 PHASE-A9b-B2b STATIC CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

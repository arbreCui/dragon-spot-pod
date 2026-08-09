#!/usr/bin/env python3
"""Static contract check for the bounded B2W returned-close gate."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_SOURCE = ROOT / "src/SPOR64_B2W.f90"
DEFAULT_HARNESS = HERE / "test_b2w_returned_close.f90"
DEFAULT_POSTERIOR = HERE / "check_b2w_returned_close.f90"
DEFAULT_RUNNER = HERE / "run_phase_a9b_b2w_returned_close.sh"


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def compact(text: str) -> str:
    code = re.sub(r"!.*", "", text)
    return re.sub(r"[\s&]+", "", code).upper()


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\b(?:subroutine|logical\s+function)\s+{name}\b.*?"
        rf"\bend\s+(?:subroutine|function)\s+{name}\b",
        text,
    )
    require(match is not None, f"missing {name} routine")
    return match.group(0)


def check_contract(
    source_text: str,
    harness_text: str,
    posterior_text: str,
    runner_text: str,
) -> None:
    whole = compact(source_text)
    close = compact(routine(source_text, "SPOR64_B2W_CLOSE"))
    axial = compact(routine(source_text, "CANONICAL_AX_IS_VALID"))
    child = compact(routine(source_text, "RETURNED_CHILD_IS_VALID"))

    require(re.search(r"(?im)^\s*module\s+SPOR64_B2W\s*$", source_text) is not None,
            "production module name differs")
    require("PUBLIC::SPOR64_B2W_CLOSE" in whole, "close gate is not public")
    require("SPOR64_B2W_PREFLIGHT_FAILED=1" in whole, "failure status differs")
    require("SPOR64_B2W_CLOSED=2" in whole, "success status differs")
    require(
        "SUBROUTINESPOR64_B2W_CLOSE(IPAXOUT,IPARCHIVEOUT,IPAX,IPFEEDBACK,STATUS)"
        in close,
        "public B2W ABI differs",
    )

    for token in (
        "C_ASSOCIATED(IPAXOUT,IPARCHIVEOUT)",
        "C_ASSOCIATED(IPAXOUT,IPAX)",
        "C_ASSOCIATED(IPAXOUT,IPFEEDBACK)",
        "C_ASSOCIATED(IPARCHIVEOUT,IPAX)",
        "C_ASSOCIATED(IPARCHIVEOUT,IPFEEDBACK)",
        "C_ASSOCIATED(IPAX,IPFEEDBACK)",
        "EMPTY_LCM_ROOT(IPAXOUT)",
        "EMPTY_LCM_ROOT(IPARCHIVEOUT)",
    ):
        require(token in close, f"missing alias/freshness guard: {token}")
    first_copy = close.index("CALLLCMEQU(IPAX,IPAXOUT)")
    last_fresh = close.rindex("EMPTY_LCM_ROOT(IPARCHIVEOUT)")
    require(last_fresh < first_copy, "freshness is not rechecked before writes")

    for token in (
        "CHARACTER_RECORD_MATCHES(IPAX,'SIGNATURE',3,12,'L_FLUX')",
        "ABSENT_RECORD(IPAX,'SPOT-X-STATE')",
        "ABSENT_RECORD(IPAX,'SPOT-X-EPOCH')",
        "RECORD_MATCHES(IPAX,'SPOT-X-RHO',1,4)",
        "RECORD_MATCHES(IPAX,'SPOT-X-L',NGRP*NSNAP,4)",
        "1.0_REAL64/REAL(KEFF32,REAL64)",
    ):
        require(token in axial, f"missing AX canonical check: {token}")
    require("EXACT_INVENTORY(IPAX" not in axial,
            "AX root must permit ordinary FLU records")

    feedback_names = (
        "SIGNATURE", "LISTDIM", "SPOT-ITER-K", "SPOT-L1-ERR", "TRACK",
        "MICROLIB2", "SYSTEM", "FLUX", "SPOT-R64",
    )
    feedback_block = compact(routine(source_text, "FEEDBACK_ROOT_IS_EXACT"))
    for name in feedback_names:
        require(name in feedback_block, f"feedback exact inventory omits {name}")
    require("NAMES(9)" in feedback_block, "feedback root is not exact nine")
    require("NAMES(3)" in compact(routine(source_text,
            "RETURNED_ROOT_AUTHORITY_IS_EXACT")),
            "returned root authority is not exact three")
    require("NAMES(16)" in compact(routine(source_text,
            "RETURNED_CHILD_ROOT_IS_EXACT")),
            "returned child root is not exact sixteen")
    require("NAMES(6)" in compact(routine(source_text,
            "RETURNED_CHILD_AUTHORITY_IS_EXACT")),
            "returned child authority is not exact six")
    system = compact(routine(source_text, "RETURNED_SYSTEM_IS_VALID"))
    require("RETURNED_SYSTEM_IS_VALID(INPUT_SYSTEM(IP),IP," in close,
            "close gate does not validate each returned SYSTEM")
    require("RETURNED_SYSTEM_ROOT_IS_EXACT(SYSTEM)" in system,
            "returned SYSTEM exact-root validator is not used")
    require("RETURNED_SYSTEM_AUTHORITY_IS_EXACT(AUTHORITY)" in system,
            "returned SYSTEM exact-authority validator is not used")
    require("NAMES(8)" in compact(routine(source_text,
            "RETURNED_SYSTEM_ROOT_IS_EXACT")),
            "returned SYSTEM root is not exact eight")
    require("NAMES(3)" in compact(routine(source_text,
            "RETURNED_SYSTEM_AUTHORITY_IS_EXACT")),
            "returned SYSTEM authority is not exact three")
    for token in ("SPOT-L1-SNAP", "'ASSEMBLED'", "TRANSFER(RHO64,0_INT64)"):
        require(token in system, f"missing returned SYSTEM identity: {token}")

    for token in (
        "ABSENT_RECORD(AUTHORITY,'PLANE')",
        "'SOLVED'",
        "1.0_REAL64/REAL(FS_KEFF32,REAL64)",
        "QFISS",
        "REAL32_PROJECTION_MATCHES",
    ):
        require(token in child, f"missing returned-child check: {token}")
    require("TRANSFER(CHILD_RHO64(IP),0_INT64)" in close,
            "cross-plane child RHO bits are not compared")
    require("TRANSFER(FS_KEFF32(IP),0_INT32)" in close,
            "cross-plane child K bits are not compared")
    require("REAL(CHILD_LEAKAGE32(IG,IP),REAL64)" in close,
            "AX/feedback leakage promotion is not exact")
    require("MAXVAL(ABS(CHILD_LEAKAGE32-SYSTEM_LEAKAGE32))" in close,
            "L1 error is not recomputed from returned L1 and lagged SYSTEM L0")
    require("TRANSFER(CHECKED_L1_ERROR32,0_INT32)" in close,
            "L1 error identity is not checked bitwise")

    for token in (
        "CALLLCMEQU(IPAX,IPAXOUT)",
        "'SPOT-X-STATE'", "'SPOT-X-EPOCH'", "'CLOSED'",
        "LCMLID(IPARCHIVEOUT,'TRACK',NSNAP)",
        "LCMLID(IPARCHIVEOUT,'MICROLIB2',NSNAP)",
        "LCMLID(IPARCHIVEOUT,'SYSTEM',NSNAP)",
        "LCMLID(IPARCHIVEOUT,'FLUX',NSNAP)",
        "LCMPUT(OUTPUT_AUTHORITY,'RHO',1,4,RHO1)",
        "STATUS=SPOR64_B2W_CLOSED",
    ):
        require(token in close, f"missing close publication step: {token}")
    require("LCMPUT(IPARCHIVEOUT,'SPOT-L1-ERR'" not in close,
            "transition-only L1 error was propagated")
    require(close.rindex("LCMPUT(OUTPUT_AUTHORITY,'EPOCH'") <
            close.rindex("STATUS=SPOR64_B2W_CLOSED"),
            "status is published before the final epoch commit")

    calls = set(re.findall(r"(?i)\bcall\s+([a-z][a-z0-9_]*)", source_text))
    forbidden_calls = {
        "dragon", "asm", "asmdrv", "spoasm", "spoleak", "flu", "fludrv",
        "flu2dr", "flugpi", "spomoc", "xdrta2", "mccgf", "mcgmre",
    }
    require(not calls.intersection(forbidden_calls),
            "B2W calls a solver or leakage producer")

    harness = compact(harness_text)
    for token in (
        "USESPOR64_B2W", "CALLSPOLEAK", "NREJECTION=25",
        "SPOR64_B2W_PREFLIGHT_FAILED", "SPOR64_B2W_CLOSED",
        "BAD-AX-RHO", "BAD-AX-LAYOUT", "BAD-AX-NAN", "BAD-ROOT-SCHEMA",
        "BAD-ROOT-STATE", "BAD-ROOT-EPOCH", "BAD-ROOT-K", "BAD-LEAK",
        "BAD-L1-NEG", "BAD-L1-NAN", "BAD-L1-WRONG", "BAD-SYSTEM-L0",
        "BAD-SYSTEM-RHO", "BAD-CHILD-RHO", "BAD-CHILD-STATE",
        "BAD-CHILD-EPOCH", "BAD-QFISS", "BAD-FLUX-MIRROR", "BAD-PLANE",
        "BAD-FS-K-PLANE", "BAD-FS-K-RHO", "BAD-Q-MIRROR",
        "ALIASED-OUTPUT", "NONFRESH-AXOUT", "VERIFY_AX_INPUT",
        "VERIFY_FEEDBACK_INPUT",
    ):
        require(token in harness, f"harness coverage marker missing: {token}")

    posterior = compact(posterior_text)
    require("USESPOR64_B2W" not in posterior, "posterior imports B2W")
    require("CALLSPOR64_B2W" not in posterior, "posterior calls B2W")
    require("CALLSPOLEAK" not in posterior, "posterior calls SPOLEAK")
    require("USEGANLIB" in posterior, "posterior is not a GANLIB reader")
    require("OPEN_READ_ONLY" in posterior, "posterior is not read-only")
    require("FOUR-LIST-DEEP-COPIES" in posterior,
            "posterior omits four-list deep-copy report")

    runner = compact(runner_text)
    for token in (
        "-STD=F2008", "-PEDANTIC", "-WERROR", "-FIMPLICIT-NONE",
        "-FFP-CONTRACT=OFF", "-FNO-FAST-MATH", "NM-G",
        "POSTERIOR1.LOG", "POSTERIOR2.LOG", "CMP",
        "SPOR64_B2W.F90", "SPOLEAK.F90", "SPOT_LEAKAGE.F90",
    ):
        require(token in runner, f"runner control missing: {token}")
    require("TRAP" in runner and "RM-RF" in runner,
            "runner does not clean temporary products")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--harness", type=Path, default=DEFAULT_HARNESS)
    parser.add_argument("--posterior", type=Path, default=DEFAULT_POSTERIOR)
    parser.add_argument("--runner", type=Path, default=DEFAULT_RUNNER)
    args = parser.parse_args()
    try:
        check_contract(
            args.source.read_text(), args.harness.read_text(),
            args.posterior.read_text(), args.runner.read_text(),
        )
    except (OSError, ContractError) as exc:
        print(f"B2W STATIC FAILURE: {exc}")
        return 1
    print("B2W STATIC RETURNED-CLOSE PASS")
    print("B2W API=AX+RETURNED-FEEDBACK->CLOSED-PAIR/1")
    print("B2W FEEDBACK-ROOT=EXACT9 OUTPUT-ARCHIVE=EXACT8")
    print("B2W L1=BITWISE-PROMOTION L1ERR=EXACT-MAX-DELTA SYSTEM-L0=RETAINED")
    print("B2W SOLVER-EXECUTIONS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

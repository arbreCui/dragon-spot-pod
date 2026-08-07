#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
B2B_PATH = ROOT / "src/SPOR64_B2B.f90"
B2C_PATH = ROOT / "src/SPOR64_B2C.f90"
B2H_PATH = ROOT / "src/SPOR64_B2H.f90"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strip_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", strip_comments(text)).upper()


def routine(text: str, name: str) -> str:
    start_match = re.search(
        rf"(?im)^\s*subroutine\s+{re.escape(name)}\s*\(", text
    )
    require(start_match is not None, f"missing subroutine {name}")
    end_match = re.search(
        rf"(?im)^\s*end\s+subroutine\s+{re.escape(name)}\s*$",
        text[start_match.start() :],
    )
    require(end_match is not None, f"unterminated subroutine {name}")
    return text[start_match.start() : start_match.start() + end_match.end()]


def logical_function(text: str, name: str) -> str:
    start_match = re.search(
        rf"(?im)^\s*logical\s+function\s+{re.escape(name)}\s*\(", text
    )
    require(start_match is not None, f"missing logical function {name}")
    end_match = re.search(
        rf"(?im)^\s*end\s+function\s+{re.escape(name)}\s*$",
        text[start_match.start() :],
    )
    require(end_match is not None, f"unterminated logical function {name}")
    return text[start_match.start() : start_match.start() + end_match.end()]


def check_contract(b2b: str, b2c: str, b2h: str) -> None:
    old = packed(routine(b2c, "SPOR64_B2C_PUBLISH"))
    cont = packed(routine(b2c, "SPOR64_B2C_PUBLISH_CONT"))
    impl = packed(routine(b2c, "SPOR64_B2C_PUBLISH_IMPL"))
    flux_check = packed(logical_function(b2c, "REAL64_FLUX_IS_VALID"))
    b2b_p = packed(b2b)
    b2c_p = packed(b2c)
    b2h_p = packed(b2h)

    old_signature = (
        "SUBROUTINESPOR64_B2C_PUBLISH(IPFLUX,ACCEPTED_TOKEN,"
        "TERMINAL_FLUX64,TERMINAL_SOURCE64,KEYFLX_BASE1,NMERG_INPUT,"
        "IMERGE_INPUT,LEAK1D_INPUT32,EPSOUT32,EPSUNK32,EPSINR32,COPTIO,"
        "MACRO_NAME,TRACK_NAME,SYSTEM_NAME,STATUS)"
    )
    require(old_signature in old, "legacy B2C public ABI changed")
    require("IPSEED" not in old, "legacy B2C publisher acquired lifecycle input")
    for declaration in (
        "TYPE(C_PTR),INTENT(IN)::IPFLUX",
        "INTEGER,INTENT(IN)::ACCEPTED_TOKEN",
        "REAL(REAL64),INTENT(IN)::TERMINAL_FLUX64(:,:),"
        "TERMINAL_SOURCE64(:,:)",
        "INTEGER,INTENT(IN)::KEYFLX_BASE1(:)",
        "INTEGER,INTENT(IN)::NMERG_INPUT,IMERGE_INPUT(:)",
        "REAL(REAL32),INTENT(IN)::LEAK1D_INPUT32(:)",
        "REAL(REAL32),INTENT(IN)::EPSOUT32,EPSUNK32,EPSINR32",
        "CHARACTER(LEN=4),INTENT(IN)::COPTIO",
        "CHARACTER(LEN=12),INTENT(IN)::MACRO_NAME,TRACK_NAME,SYSTEM_NAME",
        "INTEGER,INTENT(OUT)::STATUS",
    ):
        require(declaration in old,
                f"legacy B2C dummy declaration changed: {declaration}")
    require(old.count("CALLSPOR64_B2C_PUBLISH_IMPL(") == 1,
            "legacy B2C wrapper must call the common implementation once")
    require(old.endswith("ENDSUBROUTINESPOR64_B2C_PUBLISH"),
            "legacy B2C wrapper contains unaudited trailing code")

    cont_signature = (
        "SUBROUTINESPOR64_B2C_PUBLISH_CONT(IPFLUX,IPSEED_LIFECYCLE,"
        "ACCEPTED_TOKEN,TERMINAL_FLUX64,TERMINAL_SOURCE64,KEYFLX_BASE1,"
        "NMERG_INPUT,IMERGE_INPUT,LEAK1D_INPUT32,EPSOUT32,EPSUNK32,"
        "EPSINR32,COPTIO,MACRO_NAME,TRACK_NAME,SYSTEM_NAME,STATUS)"
    )
    require(cont_signature in cont, "CONT publisher ABI changed")
    signature_text = cont.split(")", 1)[0]
    for forbidden in ("RHO", "PLANE", "EPOCH", "RELAX", "ALPHA"):
        require(forbidden not in signature_text,
                f"CONT publisher acquired caller scalar {forbidden}")
    require(cont.count("CALLSPOR64_B2C_PUBLISH_IMPL(") == 1,
            "CONT B2C wrapper must call the common implementation once")
    require(cont.endswith("ENDSUBROUTINESPOR64_B2C_PUBLISH_CONT"),
            "CONT wrapper contains unaudited trailing code")

    for token in (
        "ACCEPTED_TOKEN/=ACCEPTED_UNPUBLISHED",
        "PUBLISH_SOLVED=PRESENT(IPSEED_LIFECYCLE)",
        "C_ASSOCIATED(IPFLUX,IPSEED_LIFECYCLE)",
        "PROJECTED_AUTHORITY_IS_EXACT(LIFECYCLE_AUTHORITY)",
        "RECORD_MATCHES(LIFECYCLE_AUTHORITY,'FLUX',NGRP,10)",
        "REAL64_FLUX_IS_VALID(LIFECYCLE_AUTHORITY)",
        "CHARACTER_RECORD_MATCHES(LIFECYCLE_AUTHORITY,'STATE',3,12,"
        "'PROJECTED')",
        "LCMGET(LIFECYCLE_AUTHORITY,'RHO',LIFECYCLE_RHO64)",
        "LCMGET(LIFECYCLE_AUTHORITY,'PLANE',LIFECYCLE_PLANE)",
        "LCMGET(LIFECYCLE_AUTHORITY,'EPOCH',LIFECYCLE_EPOCH)",
        "IEEE_IS_FINITE(LIFECYCLE_RHO64)",
        "LIFECYCLE_RHO64<=+0.0_REAL64",
        "LIFECYCLE_PLANE<1.OR.LIFECYCLE_PLANE>3",
        "LIFECYCLE_EPOCH<0.OR.LIFECYCLE_EPOCH==HUGE(LIFECYCLE_EPOCH)",
        "LCMPUT(AUTHORITY,'RHO',1,4,LIFECYCLE_RHO64)",
        "LCMPUT(AUTHORITY,'PLANE',1,1,LIFECYCLE_PLANE)",
        "AUTHORITY_STATE='SOLVED'",
        "LCMPTC(AUTHORITY,'STATE',12,AUTHORITY_STATE)",
        "LCMPUT(AUTHORITY,'EPOCH',1,1,LIFECYCLE_EPOCH)",
    ):
        require(token in impl, f"B2C SOLVED lifecycle token missing: {token}")
    require("['RHO','PLANE','FLUX','STATE','EPOCH']" in b2c_p,
            "PROJECTED seed exact inventory changed")

    require(impl.index("PUBLISH_SOLVED=PRESENT(IPSEED_LIFECYCLE)") <
            impl.index("C_ASSOCIATED(IPSEED_LIFECYCLE)"),
            "optional seed is referenced before PRESENT is frozen")
    require(impl.count("EMPTY_LCM_ROOT(IPFLUX)") == 2,
            "fresh output must be checked before staging and before writing")
    first_write = impl.index("AUTHORITY=LCMDID(IPFLUX,'SPOT-R64')")
    require(impl.rfind("EMPTY_LCM_ROOT(IPFLUX)", 0, first_write) > 0,
            "second fresh-output check is not immediately pre-publication")
    for mutator in (
        "LCMDID(", "LCMLID(", "LCMDIL(", "CALLLCMPUT(",
        "CALLLCMPDL(", "CALLLCMPTC(", "CALLLCMEQU(",
        "CALLLCMDEL(", "CALLLCMSIX(",
    ):
        require(mutator not in impl[:first_write],
                f"LCM mutation precedes designated first write: {mutator}")
    for owner in ("IPSEED_LIFECYCLE", "LIFECYCLE_AUTHORITY"):
        for mutator in (
            "LCMDID", "LCMLID", "LCMDIL", "LCMPUT", "LCMPDL",
            "LCMPTC", "LCMEQU", "LCMDEL", "LCMSIX",
        ):
            require(f"{mutator}({owner}" not in impl,
                    f"CONT publisher can mutate sealed seed via {mutator}")
    require("RETURN" not in impl[first_write:],
            "recoverable return remains after first caller-visible write")

    for token in (
        "IPFLUX=LCMGID(IPAUTHORITY,'FLUX')",
        "DOIG=1,NGRPCALLLCMLEL(IPFLUX,IG,ACTUAL_LENGTH,ACTUAL_TYPE)",
        "CALLLCMLEL(IPFLUX,IG,ACTUAL_LENGTH,ACTUAL_TYPE)",
        "IF(ACTUAL_LENGTH/=NUNKNO.OR.ACTUAL_TYPE/=4)RETURN",
        "CALLLCMGDL(IPFLUX,IG,STAGE64)",
        "IF(.NOT.ALL(IEEE_IS_FINITE(STAGE64)))RETURN",
    ):
        require(token in flux_check,
                f"complete seed FLUX validation changed: {token}")

    order = (
        "AUTHORITY=LCMDID(IPFLUX,'SPOT-R64')",
        "LCMPUT(AUTHORITY,'RHO',1,4,LIFECYCLE_RHO64)",
        "LCMPUT(AUTHORITY,'PLANE',1,1,LIFECYCLE_PLANE)",
        "LCMPDL(AUTHORITY_FLUX,IG,NUNKNO,4,TERMINAL_FLUX64(:,IG))",
        "LCMPDL(AUTHORITY_SOURCE,IG,NUNKNO,4,TERMINAL_SOURCE64(:,IG))",
        "LCMPDL(LEGACY_FLUX,IG,NUNKNO,2,FLUX_STAGE32(:,IG))",
        "LCMPDL(LEGACY_SOURCE,IG,NUNKNO,2,SOURCE_STAGE32(:,IG))",
        "LCMPUT(IPFLUX,'SPOT-LEAK1D',NGRP,2,LEAK1D_INPUT32)",
        "LCMPTC(AUTHORITY,'STATE',12,AUTHORITY_STATE)",
        "LCMPUT(AUTHORITY,'EPOCH',1,1,LIFECYCLE_EPOCH)",
        "STATUS=SPOR64_B2C_HOST_COMMITTED",
    )
    positions = [impl.index(token) for token in order]
    require(positions == sorted(positions), "SOLVED publication order changed")
    epoch_write = impl.index("CALLLCMPUT(AUTHORITY,'EPOCH',1,1,LIFECYCLE_EPOCH)")
    require(impl.rfind("CALLLCM") == epoch_write,
            "EPOCH is not the final LCM mutation in the publisher")
    require("LIFECYCLE_EPOCH+1" not in impl and
            "LIFECYCLE_EPOCH=LIFECYCLE_EPOCH+1" not in impl,
            "B2C must preserve, not increment, the accepted generation")

    for token in (
        "USESPOR64_B2C,ONLY:SPOR64_B2C_PUBLISH,SPOR64_B2C_PUBLISH_CONT",
        "IF(R64_MODE==SPOR64_B2B_CONT)THEN",
        "CALLSPOR64_B2C_PUBLISH_CONT(IPFLUX,IPSEED,",
        "CALLSPOR64_B2C_PUBLISH(IPFLUX,SPOR64_B2B_ACCEPTED_UNPUBLISHED,",
    ):
        require(token in b2b_p, f"B2B publisher routing missing: {token}")
    require(b2b_p.count("CALLSPOR64_B2C_PUBLISH_CONT(") == 1,
            "B2B must have one CONT publisher call")
    require(b2b_p.count("CALLSPOR64_B2C_PUBLISH(") == 1,
            "B2B must retain one legacy BOOT publisher call")
    core_at = b2b_p.index("CALLFLU2DR64_CORE(")
    core_failed_at = b2b_p.find("IF(.NOT.CORE_OK)THEN", core_at)
    not_accepted_at = b2b_p.find("ELSEIF(.NOT.ACCEPTED)THEN", core_at)
    require(core_failed_at >= 0 and not_accepted_at >= 0,
            "core-ok/accepted publication guard changed")
    cont_at = b2b_p.index("CALLSPOR64_B2C_PUBLISH_CONT(")
    old_at = b2b_p.index("CALLSPOR64_B2C_PUBLISH(")
    require(core_at < core_failed_at < not_accepted_at < cont_at and
            core_at < old_at,
            "publisher is not confined to the core-ok accepted branch")
    require("STATUS=SPOR64_B2B_CORE_FAILED" in
            b2b_p[core_failed_at:not_accepted_at],
            "core failure status branch changed")
    require("STATUS=SPOR64_B2B_NOT_ACCEPTED" in
            b2b_p[not_accepted_at:cont_at],
            "not-accepted status branch changed")

    require("CHARACTER_RECORD_MATCHES(SEED_AUTHORITY,'STATE',3,12,"
            "'SOLVED')" in b2h_p,
            "B2H no longer consumes a SOLVED authority")
    require("OUTPUT_EPOCH=SEED_EPOCH+1" in b2h_p,
            "B2H no longer owns the SOLVED-to-PROJECTED increment")
    require("LCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,OUTPUT_EPOCH)" in b2h_p,
            "B2H projected commit marker changed")


def main() -> None:
    b2b = B2B_PATH.read_text(encoding="utf-8")
    b2c = B2C_PATH.read_text(encoding="utf-8")
    b2h = B2H_PATH.read_text(encoding="utf-8")
    check_contract(b2b, b2c, b2h)
    print("B2P STATIC SOLVED-LIFECYCLE PASS")
    print("B2P COPIER-CONTRACT=SEALED-PROJECTED(N)->ACCEPTED-SOLVED(N)")
    print("B2P PRODUCTION-ROUTE=PROJECTED/1->SOLVED/1")
    print("B2P B2H=SOLVED(N)->PROJECTED(N+1) CONSUMER-ONLY")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static B2o contract checker; it never launches FLU or Dragon."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
B2B_PATH = ROOT / "src/SPOR64_B2B.f90"
B2O_PATH = ROOT / "src/SPOR64_B2O.f90"
FLU_PATH = ROOT / "src/FLU.f"
A8_PATH = ROOT / "src/SPOR64_A8_ACA.f90"
A9_PATH = ROOT / "src/SPOR64_A9.f90"
HARNESS_PATH = Path(__file__).with_name("test_b2o_cont_binding_cutoff.f90")
STUB_PATH = Path(__file__).with_name("b2o_capture_stubs.f90")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def packed(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        if raw.startswith(("*", "!")):
            continue
        code = raw.split("!", 1)[0]
        lines.append(code)
    return re.sub(r"\s+", "", "".join(lines)).replace("&", "").upper()


def routine(text: str, name: str, kind: str = "function") -> str:
    if kind == "function":
        pattern = rf"(?is)\b(?:logical\s+)?function\s+{name}\b.*?\bend\s+function\s+{name}\b"
    else:
        pattern = rf"(?is)\bsubroutine\s+{name}\b.*?\bend\s+subroutine\s+{name}\b"
    match = re.search(pattern, text)
    require(match is not None, f"missing {kind} {name}")
    return match.group(0)


def check_contract(
    b2b: str,
    flu: str,
    a8: str,
    a9: str,
    b2o: str | None = None,
) -> None:
    if b2o is None:
        b2o = B2O_PATH.read_text(encoding="utf-8")
    b2b_p = packed(b2b)
    lifecycle = packed(routine(b2b, "CONT_LIFECYCLE_IS_BOUND"))
    ingress = packed(routine(b2b, "SPOR64_B2B_INGRESS", "subroutine"))

    abi = (
        "SUBROUTINESPOR64_B2B_INGRESS(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY,"
        "ITYPEC,MAXOUT,MAXINR,EPSOUT32,EPSUNK32,EPSINR32,IREBAL,IFRITR,"
        "IACITR,COPTIO,ILEAK,INITFL,NMERG,IMERG,IPRINT,REC,IMCAUD,LIMERG,"
        "NGRP_HOST,NREG_HOST,NMAT_HOST,NIFIS_HOST,ITPIJ_HOST,ITRANC_HOST,"
        "IPHASE_HOST,LEAKSW_HOST,LFORW_HOST,R64_MODE,STATUS,CUTOFF_VISIT64)"
    )
    require(abi in ingress, "B2B public ABI changed")
    require(ingress.count("CONT_LIFECYCLE_IS_BOUND(") == 1,
            "CONT lifecycle admission call must occur exactly once")
    call_at = ingress.index("CONT_LIFECYCLE_IS_BOUND(")
    require(ingress.index("R64_MODE==SPOR64_B2B_CONT") < call_at,
            "lifecycle admission is not CONT-only")
    require(ingress.index("LCMGET(IPSOU,'SPOT-QINT',QINT32)") < call_at,
            "lifecycle admission moved before read-only root admission")
    require(call_at < ingress.index("INITIAL_FLUX64=+0.0_REAL64"),
            "lifecycle admission must precede type-4 payload staging")
    require(call_at < ingress.index("CALLXDRTA2"),
            "lifecycle admission must precede XDRTA2")

    for token in (
        "CONT_EPOCH=1", "NPLANE=3",
        "CONT_SEED_AUTHORITY_IS_EXACT(SEED_AUTHORITY)",
        "CONT_SOURCE_AUTHORITY_IS_EXACT(SOURCE_AUTHORITY)",
        "CONT_SYSTEM_AUTHORITY_IS_EXACT(SYSTEM_AUTHORITY)",
        "'PROJECTED'", "'FROZEN-QFIS'", "'ASSEMBLED'",
        "RECORD_MATCHES(SEED_AUTHORITY,'PLANE',1,1)",
        "RECORD_MATCHES(SOURCE_AUTHORITY,'PLANE',1,1)",
        "RECORD_MATCHES(IPSYSTEM,'SPOT-L1-SNAP',1,1)",
        "SOURCE_PLANE<1.OR.SOURCE_PLANE>NPLANE",
        "SEED_PLANE/=SOURCE_PLANE",
        "SYSTEM_PLANE/=SOURCE_PLANE",
        "SAME_REAL32_BITS(SEED_LEAKAGE,SYSTEM_LEAKAGE)",
    ):
        require(token in lifecycle, f"missing lifecycle contract: {token}")
    require(lifecycle.count("TRANSFER(SEED_RHO64,0_INT64)") == 2,
            "seed RHO must anchor two exact bit comparisons")
    require(lifecycle.count("TRANSFER(SOURCE_RHO64,0_INT64)") == 1,
            "source RHO bit comparison differs")
    require(lifecycle.count("TRANSFER(SYSTEM_RHO64,0_INT64)") == 1,
            "system RHO bit comparison differs")
    require(lifecycle.count("/=CONT_EPOCH") == 3,
            "all three epochs must equal the frozen epoch")
    for variable in ("SEED_RHO64", "SOURCE_RHO64", "SYSTEM_RHO64"):
        require(f"IEEE_IS_FINITE({variable})" in lifecycle,
                f"{variable} finite check missing or miswired")
        require(f"{variable}<=+0.0_REAL64" in lifecycle,
                f"{variable} positivity check missing or miswired")

    inventory_contracts = {
        "CONT_SEED_AUTHORITY_IS_EXACT": (
            "'RHO'", "'PLANE'", "'FLUX'", "'STATE'", "'EPOCH'"),
        "CONT_SOURCE_AUTHORITY_IS_EXACT": (
            "'RHO'", "'PLANE'", "'STATE'", "'QFISS'", "'EPOCH'"),
        "CONT_SYSTEM_AUTHORITY_IS_EXACT": (
            "'RHO'", "'STATE'", "'EPOCH'"),
    }
    for name, fields in inventory_contracts.items():
        body = packed(routine(b2b, name))
        for field in fields:
            require(field in body, f"{name} missing {field}")
        require(f"{name}=EXACT_INVENTORY(IPLIST,NAMES)" in body,
                f"{name} is not exact-inventory based")
    require("FUNCTIONEXACT_INVENTORY" in b2b_p,
            "exact-inventory implementation missing")
    require("FUNCTIONSAME_REAL32_BITS" in b2b_p,
            "bit-exact leakage comparator missing")
    for write_api in ("LCMPUT(", "LCMPTC(", "LCMPDL(", "LCMDID(", "LCMLID("):
        require(write_api not in b2b_p,
                f"B2B read-only admission acquired write API {write_api}")

    flu_p = packed(flu)
    observer = "WRITE(IOUT,5990)IR64MD,IB2STAT,CUTOFF64"
    require(flu_p.count(observer) == 1,
            "FLU cutoff observer must be one unconditional write")
    ingress_call = flu_p.index("CALLSPOR64_B2B_INGRESS(")
    observer_at = flu_p.index(observer)
    first_status = flu_p.index("IF(IB2STAT.EQ.", ingress_call)
    require(ingress_call < observer_at < first_status,
            "FLU observer must follow ingress and precede status dispatch")
    require("ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCES=" in flu_p,
            "FLU observer label is semantically imprecise")
    require(
        "5990FORMAT('SPOR64R64MODE=',I2,'STATUS=',I2,1"
        "'ACA-CUTOFF-LOCAL-PREDICATE-DIFFERENCES=',I20)" in flu_p,
        "FLU observer format or INT64-safe I20 width changed",
    )
    require(flu_p.count("CUTOFF64") == 3,
            "CUTOFF64 must occur only in declaration, call, and observer")
    require("INTEGER(INT64)CUTOFF64" in flu_p,
            "FLU cutoff observer lost INT64")
    require("IF(CUTOFF64" not in flu_p and "ELSEIF(CUTOFF64" not in flu_p,
            "cutoff count must not decide status or physics")
    for write_api in ("LCMPUT", "LCMPTC", "LCMPDL"):
        for match in re.finditer(write_api + r"\([^)]*CUTOFF64", flu_p):
            require(False, f"cutoff count written into an LCM object: {match.group(0)}")

    a8_p = packed(a8)
    require("INHERITED_EPSMAX32=1.0E-7_REAL32" in a8_p,
            "inherited ACA cutoff changed")
    require("INT(Z'33D6BF95',INT32)" in a8_p,
            "inherited ACA cutoff bit guard changed")
    require(a8_p.count("GUARD_LIVE.NEQV.GUARD_ZERO") == 4,
            "ACA counterfactual sites are not exactly four")
    require(a8_p.count("CUTOFF_DELTA64=CUTOFF_DELTA64+1_INT64") == 4,
            "ACA difference increments are not exactly four")

    a9_p = packed(a9)
    require("INTEGER(INT64),INTENT(OUT)::CUTOFF_VISIT64" in a9_p,
            "A9 cutoff output lost INT64")
    require("CUTOFF_VISIT64>HUGE(CUTOFF_VISIT64)-CUTOFF_DELTA64" in a9_p,
            "A9 cutoff overflow guard missing")
    require("CUTOFF_VISIT64=CUTOFF_VISIT64+CUTOFF_DELTA64" in a9_p,
            "A9 cutoff aggregation changed")

    b2o_p = packed(b2o)
    seal = packed(routine(b2o, "SPOR64_B2O_SEAL_CONT_PAIR", "subroutine"))
    require(
        "SUBROUTINESPOR64_B2O_SEAL_CONT_PAIR(IPASSEMBLED,IPSOURCE,"
        "IPSEED_OUT,IPSYSTEM_OUT,STATUS)" in seal,
        "sealed-pair ABI changed or acquired caller plane/RHO scalars",
    )
    for token in (
        "ASSEMBLED_ROOT_IS_EXACT(IPASSEMBLED)",
        "SOURCE_AUTHORITY_IS_EXACT(SOURCE_AUTHORITY)",
        "INPUT_SEED_AUTHORITY_IS_EXACT(SEED_AUTHORITY)",
        "SYSTEM_AUTHORITY_IS_EXACT(SYSTEM_AUTHORITY)",
        "LCMGIL(FLUXES,NPLANE)",
        "LCMGIL(SYSTEMS,NPLANE)",
        "SYSTEM_PLANE/=NPLANE",
        "SAME_REAL32_BITS(SEED_LEAKAGE32,SYSTEM_LEAKAGE32)",
        "LCMPUT(OUTPUT_SEED_AUTHORITY,'PLANE',1,1,NPLANE)",
        "LCMPUT(OUTPUT_SEED_AUTHORITY,'EPOCH',1,1,ROOT_EPOCH)",
        "LCMPUT(OUTPUT_SYSTEM_AUTHORITY,'EPOCH',1,1,ROOT_EPOCH)",
        "STATUS=SPOR64_B2O_SEALED",
    ):
        require(token in seal, f"sealed same-index contract missing: {token}")
    require(seal.index("LCMGIL(FLUXES,NPLANE)") <
            seal.index("LCMPUT(OUTPUT_SEED_AUTHORITY,'PLANE'"),
            "seed plane was not derived before publication")
    require(b2o_p.count("SPOR64_B2O_SEAL_CONT_PAIR") >= 3,
            "sealed-pair public production symbol missing")


def check_validation_sources() -> None:
    harness = packed(HARNESS_PATH.read_text(encoding="utf-8"))
    stubs = packed(STUB_PATH.read_text(encoding="utf-8"))
    require("NEGATIVE_CASES=32" in harness,
            "synthetic rejection inventory changed")
    require("B2O_CUTOFF_SENTINEL=4294967311_INT64" in stubs,
            "cutoff sentinel must exceed the 32-bit range")
    require("CUTOFF_VISIT64=B2O_CUTOFF_SENTINEL" in stubs,
            "stub does not return the INT64 sentinel")
    require("SPOR64_B2B_CONT" in harness,
            "harness does not exercise real CONT admission")
    require("SPOR64_B2O_SEAL_CONT_PAIR(ASSEMBLED,SOURCE,SEED,SYSTEM," in harness,
            "harness does not execute the production same-index sealer")
    require(harness.count("SPACING(STAGE64(IU))") == 5,
            "three REAL64-only seed/source witness-construction sites changed")
    require("SEALER_CALLS/=7.OR.SEALER_POSITIVES/=2.OR." in harness and
            "SEALER_REJECTIONS/=5" in harness,
            "same-index sealer dynamic inventory changed")
    require("REAL(EXPECTED_PLANE,REAL64)*SPACING(BASE64)" in harness and
            "SEALEDSEEDPAYLOADISNOTSOURCE-SELECTEDINDEX" in harness,
            "plane-distinct sealed-seed payload witness missing")
    require("COREFLUXLOSTITSREAL64-ONLYLOWBITS" in harness,
            "FLUX REAL32-roundtrip rejection missing")
    require("COREQFISSLOSTITSREAL64-ONLYLOWBITS" in harness,
            "QFISS REAL32-roundtrip rejection missing")
    for token in (
        "LOCAL_CUTOFF/=B2O_CUTOFF_SENTINEL",
        "XDRTA2_TOTAL/=1.OR.CORE_TOTAL/=1",
        "LOCAL_STATUS/=SPOR64_B2B_ADMISSION_FAILED",
        "LOCAL_CUTOFF/=0_INT64",
        "REQUIRE_EMPTY_ROOT(OUTPUT)",
    ):
        require(token in harness, f"harness invariant missing: {token}")


def main() -> None:
    check_contract(
        B2B_PATH.read_text(encoding="utf-8"),
        FLU_PATH.read_text(encoding="utf-8"),
        A8_PATH.read_text(encoding="utf-8"),
        A9_PATH.read_text(encoding="utf-8"),
        B2O_PATH.read_text(encoding="utf-8"),
    )
    check_validation_sources()
    print("B2O STATIC CONT-BINDING-CUTOFF PASS")
    print("B2O LIFECYCLE=SEALED-SAME-INDEX/RHO-BITS/LOCAL-EPOCH/STATES/PLANE/LEAK-BITS")
    print("B2O CUTOFF=ALONG-LIVE-LOCAL-PREDICATE-DIFFERENCES OBSERVER-ONLY")


if __name__ == "__main__":
    main()

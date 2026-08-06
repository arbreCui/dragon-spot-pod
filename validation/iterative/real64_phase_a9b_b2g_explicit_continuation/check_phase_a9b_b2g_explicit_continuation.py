#!/usr/bin/env python3
"""Fail-closed static gate for explicit BOOT/CONT REAL64 ingress."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


class GateError(RuntimeError):
    """Raised when the B2g continuation boundary is incomplete."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def compact_free(text: str) -> str:
    code = []
    for raw in text.splitlines():
        line = raw.split("!", 1)[0]
        if line.strip():
            code.append(line)
    return re.sub(r"\s+", "", "\n".join(code)).replace("&", "").upper()


def fixed_code(text: str) -> str:
    fields: list[str] = []
    for raw in text.splitlines():
        if not raw or raw[0] in "*cC!":
            continue
        fields.append(raw.ljust(6)[6:72])
    return "\n".join(fields) + "\n"


def compact_fixed(text: str) -> str:
    return re.sub(r"\s+", "", fixed_code(text)).upper()


def routine_args(code: str, name: str) -> list[str]:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\((.*?)\)", code
    )
    require(match is not None, f"missing subroutine {name}")
    return [item.strip().lower() for item in match.group(1).split(",")]


def call_args(code: str, name: str) -> list[str]:
    matches = list(
        re.finditer(rf"(?is)\bcall\s+{re.escape(name)}\s*\((.*?)\)", code)
    )
    require(len(matches) == 1, f"expected one CALL {name}")
    return [item.strip().lower() for item in matches[0].group(1).split(",")]


def bounded(text: str, start: str, end: str, label: str) -> str:
    first = text.find(start)
    require(first >= 0, f"{label}: missing start")
    last = text.find(end, first + len(start))
    require(last > first, f"{label}: missing end")
    return text[first:last]


def check_b2b_text(text: str) -> None:
    packed = compact_free(text)
    args = routine_args(text, "SPOR64_B2B_INGRESS")
    require(
        args[-4:] == ["lforw_host", "r64_mode", "status", "cutoff_visit64"],
        "B2B mandatory mode ABI tail",
    )
    require(
        "INTEGER,PARAMETER,PUBLIC::SPOR64_B2B_BOOT=1" in packed,
        "public BOOT=1 token",
    )
    require(
        "INTEGER,PARAMETER,PUBLIC::SPOR64_B2B_CONT=2" in packed,
        "public CONT=2 token",
    )
    mode_guard = (
        "IF(R64_MODE/=SPOR64_B2B_BOOT.AND."
        "R64_MODE/=SPOR64_B2B_CONT)RETURN"
    )
    require(packed.count(mode_guard) == 1, "one exact fail-closed mode guard")
    require(
        packed.index(mode_guard) < packed.index("IF(NENTRY/=7)RETURN")
        < packed.index("CALLXDRTA2"),
        "mode guard precedes admission and core boundary",
    )

    namespace = bounded(
        packed,
        "IF(R64_MODE==SPOR64_B2B_BOOT)THEN",
        "IF(.NOT.ABSENT_RECORD(IPSEED,'AFLUX'))RETURN",
        "namespace mode branch",
    )
    require(namespace.count("ABSENT_RECORD(IPSEED,'SPOT-R64')") == 1,
            "BOOT seed authority collision")
    require(namespace.count("ABSENT_RECORD(IPSOU,'SPOT-R64')") == 1,
            "BOOT source authority collision")
    require("ELSE" in namespace, "CONT namespace branch")
    require(
        "RECORD_MATCHES(IPSEED,'SPOT-R64',-1,0)" in namespace
        and "RECORD_MATCHES(IPSOU,'SPOT-R64',-1,0)" in namespace,
        "CONT requires directory authorities",
    )

    load_start = packed.rfind("IF(R64_MODE==SPOR64_B2B_BOOT)THEN")
    load_end = packed.find("XCSOU1=+0.0_REAL64", load_start)
    require(load_start >= 0 and load_end > load_start, "bounded mode load")
    load = packed[load_start:load_end]
    split = load.find("ELSE")
    require(split > 0, "BOOT/CONT load split")
    boot, cont = load[:split], load[split:]
    require("LCMGID(IPSEED,'FLUX')" in boot, "BOOT root FLUX")
    require("LCMGID(IPSOU,'DSOUR')" in boot, "BOOT root DSOUR")
    require(boot.count("ITYLCM/=2") == 2, "BOOT type-2 element checks")
    require("REAL(FLUX_STAGE32,REAL64)" in boot, "BOOT FLUX promotion")
    require("REAL(SOURCE_STAGE32,REAL64)" in boot, "BOOT source promotion")

    for fragment in (
        "SEED_AUTHORITY=LCMGID(IPSEED,'SPOT-R64')",
        "RECORD_MATCHES(SEED_AUTHORITY,'FLUX',NGRP,10)",
        "JPFLUX=LCMGID(SEED_AUTHORITY,'FLUX')",
        "CALLLCMGDL(JPFLUX,IG,INITIAL_FLUX64(:,IG))",
        "SOURCE_AUTHORITY=LCMGID(IPSOU,'SPOT-R64')",
        "RECORD_MATCHES(SOURCE_AUTHORITY,'QFISS',NGRP,10)",
        "JPSOURCE=LCMGID(SOURCE_AUTHORITY,'QFISS')",
        "CALLLCMGDL(JPSOURCE,IG,FIXED_SOURCE64(:,IG))",
    ):
        require(fragment in cont, f"CONT authority read: {fragment}")
    require(cont.count("ITYLCM/=4") == 2, "CONT two type-4 element checks")
    for forbidden in (
        "LCMGID(IPSEED,'FLUX')",
        "LCMGID(IPSOU,'DSOUR')",
        "FLUX_STAGE32",
        "SOURCE_STAGE32",
        "ITYLCM/=2",
        "REAL(",
        "ALPHA",
        "OMEGA",
        "RELAX",
        "DAMP",
        "FALLBACK",
    ):
        require(forbidden not in cont, f"CONT forbidden path: {forbidden}")
    require(
        "CALLFLU2DR64_CORE(" in packed
        and "SCAT_OFF32,FIXED_SOURCE64,INITIAL_FLUX64," in packed,
        "core receives direct REAL64 authority arrays",
    )
    for write_api in ("LCMPUT(", "LCMPDL(", "LCMPPD(", "LCMPTC(",
                      "LCMLID(", "LCMDID(", "LCMDEL("):
        require(write_api not in packed, f"B2B remains read-only: {write_api}")


def check_host_text(flu_text: str, flugpi_text: str, plane_text: str) -> None:
    flu_code = fixed_code(flu_text)
    flu = compact_fixed(flu_text)
    gpi_code = fixed_code(flugpi_text)
    gpi = compact_fixed(flugpi_text)

    require(routine_args(gpi_code, "FLUGPI")[-2:] ==
            ["limerg", "ir64md"], "FLUGPI integer mode ABI")
    require(call_args(flu_code, "FLUGPI")[-2:] ==
            ["limerg", "ir64md"], "FLU passes parser mode")
    require(call_args(flu_code, "SPOR64_B2B_INGRESS")[-4:] ==
            ["lforw", "ir64md", "ib2stat", "cutoff64"],
            "FLU passes mandatory B2B mode")
    require("INTEGERISTATE(NSTATE),IMCAUD,IR64MD,IB2STAT" in flu,
            "FLU integer selector declaration")
    require("LR64=IR64MD.NE.0" in flu, "legacy route guard derives from mode")
    require("IR64MD=0" in gpi, "parser mode defaults off")
    require(gpi.index("IR64MD=0") < gpi.index("IF(REC)THEN")
            < gpi.index("CALLREDGET("), "mode reset precedes REC and tokens")
    require("LOGICALLEAKSW,REC,LIMERG" in gpi and
            "LOGICALLEAKSW,REC,LIMERG,LR64" not in gpi,
            "FLUGPI no stale logical selector")

    branch = re.search(
        r"ELSEIF\(CARLIR\.EQ\.'R64'\)THEN(.*?)"
        r"ELSEIF\(CARLIR\.EQ\.'EDIT'\)THEN",
        gpi,
    )
    require(branch is not None, "bounded R64 parser branch")
    body = branch.group(1)
    for fragment in (
        "IF(IR64MD.NE.0)THEN",
        "CALLXABORT('FLUGPI:DUPLICATER64KEYWORD.')",
        "CALLREDGET(ITYPLU,INTLIR,REALIR,CARLIR,DBLINP)",
        "IF(ITYPLU.NE.3)THEN",
        "CALLXABORT('FLUGPI:R64BOOTORCONTEXPECTED.')",
        "IF(CARLIR.EQ.'BOOT')THENIR64MD=1",
        "ELSEIF(CARLIR.EQ.'CONT')THENIR64MD=2",
    ):
        require(fragment in body, f"parser explicit mode fragment: {fragment}")
    require(body.count("IR64MD=") == 2, "only BOOT/CONT assign selected mode")
    require("R64 BOOT ;" in plane_text, "shipped explicit plane uses BOOT")
    require("R64 ;" not in plane_text, "no bare R64 procedure syntax")


def check_validation_text(
    harness: str, stub: str, parser: str, runner: str
) -> None:
    h = compact_free(harness)
    s = compact_free(stub)
    p = compact_free(parser)
    require(h.count("CALLRUN_BOOT_POSITIVE()") == 1,
            "one real B2B/B2C BOOT success")
    require(h.count("CALLRUN_CONT_POSITIVE()") == 1,
            "one real B2B/B2C CONT success")
    require(h.count("CALLRUN_REJECTION(") == 11, "eleven rejection cases")
    require("REQUIRE_BOOT_CAPTURE_BITS" in h,
            "BOOT exact type-2 promotion proof")
    require("SPACING(STAGE64(IU))" in h, "REAL64-only ULP perturbation")
    require("ROUNDTRIP_FLUX64(:,IG)=REAL(REAL(STAGE64,REAL32),REAL64)" in h,
            "FLUX REAL32 roundtrip witness")
    require("ROUNDTRIP_QFISS64(:,IG)=REAL(REAL(STAGE64,REAL32),REAL64)" in h,
            "QFISS REAL32 roundtrip witness")
    require("COREFLUXLOSTREAL64-ONLYAUTHORITYBITS" in h,
            "FLUX bit-loss rejection")
    require("COREQFISSLOSTREAL64-ONLYAUTHORITYBITS" in h,
            "QFISS bit-loss rejection")
    require("LCMPDL(ROOT_FLUX,IG,NUNKNO,2,POISON32)" in h,
            "root FLUX poison")
    require("LCMPDL(ROOT_SOURCE,IG,NUNKNO,2,POISON32)" in h,
            "root DSOUR poison")
    require(
        "TERMINAL_SOURCE64(IU,IG)=REAL(1000*IG+IU,REAL64)/8.0_REAL64" in s,
        "stub returns an exactly representable terminal SOUR sentinel",
    )
    require("TERMINAL_SOURCE64=FIXED_SOURCE64" not in s,
            "stub must distinguish terminal SOUR from fixed QFISS")
    require("CALLREQUIRE_ABSENT(AUTHORITY,'QFISS')" in h,
            "published output authority excludes QFISS")
    require("CALLLCMGDL(SOURCE,IG,PUBLISHED_SOURCE64)" in h,
            "published type-4 SOUR payload is read back")
    require("PUBLISHEDSOURDIFFERSFROMCORETERMINALSOURCE" in h,
            "published SOUR bitwise identity check")
    require("PUBLISHEDSOURWASCONFUSEDWITHFIXEDQFISS" in h,
            "published SOUR/QFISS distinction check")
    for scenario in ("'off'", "'boot'", "'cont'", "'reset'", "'rec_reset'",
                     "'bare'", "'integer'", "'unknown'", "'duplicate'",
                     "'isolated_boot'", "'isolated_cont'"):
        require(scenario.upper() in p, f"parser scenario {scenario}")
    require("src/FLUGPI.f" in runner, "runner compiles production FLUGPI")
    require("src/FLU.f" in runner, "runner compiles production FLU host")
    require("REAL-B2B-CALLS=13 REJECTIONS=11" in runner,
            "runner freezes both positive modes and rejection inventory")
    require("STUB-XDRTA2-CALLS=2 STUB-CORE-CALLS=2" in runner,
            "runner freezes two positive core-call boundaries")
    require(runner.count("verify_receipts") == 4,
            "runner defines and calls receipt verification three times")
    require(
        runner.rfind("verify_receipts")
        > runner.rfind("check_phase_a9b_b2g_explicit_continuation.py"),
        "runner rechecks receipts after the final static check",
    )
    require("EXPECTED_PARENT_COMMIT=2dc5a870470c2e689e505d583ab6aca8a87d2fa4"
            in runner, "runner freezes B2f parent commit")
    require("EXPECTED_PARENT_HASH="
            "1d0716cb3963fef0550b63db618d1da1a5abc8d72e5d71a8e73b1b951c2c6845"
            in runner, "runner freezes B2f parent receipt")
    require('shasum -a 256 -c "$RECEIPT"' in runner,
            "runner verifies implementation receipt")


def main() -> None:
    b2b = (ROOT / "src/SPOR64_B2B.f90").read_text()
    flu = (ROOT / "src/FLU.f").read_text()
    flugpi = (ROOT / "src/FLUGPI.f").read_text()
    plane = (ROOT / "data/SpotPlaneR64.c2m").read_text()
    harness = (HERE / "test_b2g_explicit_continuation.f90").read_text()
    stub = (HERE / "b2g_capture_stubs.f90").read_text()
    parser = (HERE / "b2g_parser_driver.f90").read_text()
    runner = (HERE / "run_phase_a9b_b2g_explicit_continuation.sh").read_text()
    manifest = json.loads((HERE / "precision_manifest.json").read_text())

    check_b2b_text(b2b)
    check_host_text(flu, flugpi, plane)
    check_validation_text(harness, stub, parser, runner)
    require(manifest["modes"] == {"off": 0, "boot": 1, "continuation": 2},
            "manifest modes")
    require("QFISS absent" in
            manifest["positive_boundary"]["published_output_authority"],
            "manifest separates output SOUR from QFISS")
    require("exact one-time promotion" in
            manifest["positive_boundary"]["boot_production_ingress"],
            "manifest records dynamic BOOT coverage")
    require(
        manifest["receipt"]
        == "phase_a9b_b2g_explicit_continuation_receipt.sha256",
        "implementation receipt name",
    )
    require(manifest["parent_commit"] ==
            "2dc5a870470c2e689e505d583ab6aca8a87d2fa4",
            "manifest B2f parent commit")
    print("SPOR64 PHASE-A9b-B2g STATIC PASS")
    print("CLAIM=EXPLICIT-BOOT-CONT-TYPE4-AUTHORITY-CONTRACT-CLOSED")


if __name__ == "__main__":
    main()

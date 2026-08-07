#!/usr/bin/env python3
"""Static contract for the bounded B2l one-plane real ASM smoke."""

from __future__ import annotations

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECK = HERE / "one_plane_real_asm.x2m"
PREPARER = HERE / "prepare_b2l_projected.f90"
POSTERIOR = HERE / "check_b2l_real_asm.f90"
BOUNDED = HERE / "run_bounded_b2l.py"
RUNNER = HERE / "run_phase_a9b_b2l_one_plane_real_asm.sh"
XSM_HARNESS = HERE / "test_b2j_xsm_target.f90"
ASM = ROOT / "src/ASM.f"
ASMDRV = ROOT / "src/ASMDRV.f"
B2J = ROOT / "src/SPOR64_B2J.f90"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"B2L STATIC CONTRACT FAIL: {message}")


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def fortran_without_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def deck_without_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("*")
    )


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        text,
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def check_deck(text: str) -> None:
    code = deck_without_comments(text).upper()
    compact = packed(code)
    require(code.count(":= ASM:") == 1, "deck must call ASM exactly once")
    require("EDIT0ARMLK1D1;" in compact, "deck must use EDIT 0 ARM LK1D 1")
    require(code.count("RECOVER: PROJECTED :: ITEM 1") == 2,
            "deck must recover same-index plane-1 library and track")
    require("MACRO0:=MICROLIB2;" in compact,
            "deck must deep-copy the plane library to MACRO0")
    require("SYSTEM_OUT:=SYSTEM;" in compact,
            "linked-list ASM result must be persisted after ASM")
    require(
        "MODULERECOVER:ASM:DELETE:END:;" in compact,
        "module allowlist differs",
    )
    for forbidden in (
        "FLU:", "SPOR64K:", "SPOFSRC:", "SPOFCHK:", "CONT",
        "QFISS", "PROCEDURE", "WHILE", "REPEAT", "SPOTPLANER64",
    ):
        require(forbidden not in code, f"forbidden deck token {forbidden}")
    require(code.count("SEQ_BINARY TRACK_F") == 1,
            "deck must expose one sequential tracking file")
    require(code.count("XSM_FILE PROJECTED") == 1,
            "deck must expose one PROJECTED input")
    require(code.count("XSM_FILE SYSTEM_OUT") == 1,
            "deck must have one persistent result")


def check_preparer(text: str) -> None:
    code = fortran_without_comments(text)
    compact = packed(code)
    for token in (
        "CALLSPOR64_B2C_PUBLISH(",
        "CALLSPOR64_B2I_SEAL_BOOTSTRAP(",
        "CALLSPOR64_B2J_PROJECT_ARCHIVE(",
        "CALLLCMEQU(SOURCE_ITEM,OUTPUT_ITEM)",
        "CALLLCMOP(PROJECTED,TRIM(OUTPUT_PATH),0,2,0)",
        "CALLREQUIRE_EMPTY_XSM_ROOT(PROJECTED)",
        "INQUIRE(FILE=TRIM(OUTPUT_PATH),EXIST=OUTPUT_EXISTS)",
        "IF(OUTPUT_EXISTS)ERRORSTOP'PROJECTEDOUTPUTPATHALREADYEXISTS'",
    ):
        require(token in compact, f"preparer missing {token}")
    build = packed(routine(code, "BUILD_FULL_CANDIDATE"))
    require(build.count("CALLLCMEQU(SOURCE_ITEM,OUTPUT_ITEM)") == 3,
            "TRACK/MICROLIB2/SYSTEM must each use full LCMEQU")
    require("CALLPUBLISH_FULL_FLUX(SOURCE_ITEM,OUTPUT_ITEM,B2C_COUNT)" in build,
            "FLUX must be republished through production B2c")
    publish = packed(routine(code, "PUBLISH_FULL_FLUX"))
    for token in (
        "CALLLCMOP(PUBLISHED,PUBLISHED_NAME,0,1,0)",
        "CALLREQUIRE_EMPTY_ROOT(PUBLISHED)",
        "CALLSPOR64_B2C_PUBLISH(PUBLISHED,4,",
        "CALLLCMEQU(PUBLISHED,TARGET)",
        "CALLLCMCL(PUBLISHED,2)",
    ):
        require(token in publish, f"B2c root staging missing {token}")
    require("CALLSPOR64_B2C_PUBLISH(TARGET,4," not in publish,
            "B2c must not publish directly into a list child")
    main = packed(code.split("contains", 1)[0])
    marker = "CALLSPOR64_B2J_PROJECT_ARCHIVE("
    post = main[main.index(marker):]
    for mutation in (
        "LCMPUT(", "LCMPTC(", "LCMEQU(", "LCMDEL(", "LCMDID(",
        "LCMLID(", "LCMDIL(",
    ):
        require(mutation not in post,
                f"mutation {mutation} occurs after production B2j commit")
    require("CALLLCMCL(PROJECTED,1)" in post,
            "persistent PROJECTED must close after B2j")
    require("SPACING(" not in compact and "NEAREST(" not in compact,
            "runtime materializer must not add a ULP perturbation")


def check_posterior(text: str) -> None:
    code = fortran_without_comments(text)
    compact = packed(code)
    for token in (
        "CALLCOMPARE_DICTIONARY(LEFT_ITEM,RIGHT_ITEM,COMPARED_RECORDS,",
        "IF(.NOT.EXACT_INVENTORY(SYSTEM_ROOT,SYSTEM_ROOT_NAMES))",
        "IF(.NOT.EXACT_INVENTORY(SYSTEM_GROUP,GROUP_NAMES))",
        "EXPECTED_TX(IM)=EXPECTED_TX(IM)-TRANC(IM)",
        "EXPECTED_SPHYS(IM)=EXPECTED_SPHYS(IM)-TRANC(IM)",
        "EXPECTED_SUSED(IM)=EXPECTED_SPHYS(IM)-LEAKAGE(IG)",
        "EXPECTED_SUSED(0)=EXPECTED_SPHYS(0)-LEAKAGE(IG)",
        "IEEE_IS_FINITE(RESPONSE)",
        "REAL32_MAGNITUDE_MASK=INT(Z'7FFFFFFF',INT32)",
        "COUNT(IAND(TRANSFER(RESPONSE,0_INT32,SIZE(RESPONSE)),"
        "REAL32_MAGNITUDE_MASK)/=0_INT32)",
        "RESPONSE_LENGTHS(12)=[32,14,32,14,8,8,8,8,8,8,8,14]",
    ):
        require(token in compact, f"posterior missing {token}")
    require(compact.count("CALLCOMPARE_DICTIONARY(LEFT_ITEM,RIGHT_ITEM,") == 2,
            "posterior must recursively compare TRACK and MICROLIB2")
    require("SPOR64_B2K" not in compact and "ASM(" not in compact,
            "posterior must remain independent and solver-free")
    for forbidden in (
        "TOLERANCE", "RELAX", "DAMP", "CLIP", "FLOOR", "FIT",
        "REFERENCE_DISTANCE", "OLD_SYSTEM",
    ):
        require(forbidden not in compact,
                f"posterior contains empirical/model token {forbidden}")


def check_bounded(text: str) -> None:
    compact = packed(text)
    for token in (
        '"WALL_SECONDS":30', '"CPU_SECONDS":20',
        '"RSS_BYTES":2*1024**3', '"FILE_BYTES":512*1024**2',
        '"WALL_SECONDS":15', '"CPU_SECONDS":10',
        '"RSS_BYTES":1024**3', '"FILE_BYTES":64*1024**2',
        "START_NEW_SESSION=TRUE", "OS.KILLPG(PROCESS.PID,SIGNAL.SIGTERM)",
        "OS.KILLPG(PROCESS.PID,SIGNAL.SIGKILL)",
        '"OMP_NUM_THREADS":"1"', '"OPENBLAS_NUM_THREADS":"1"',
        "RESOURCE.RLIMIT_CPU", "RESOURCE.RLIMIT_FSIZE",
        "RESOURCE.RLIMIT_CORE", "PROCESS_RSS_BYTES(PROCESS.PID)",
        'RSS_BYTES>PROFILE["RSS_BYTES"]',
        "EXIT_CENSUS_GRACE_SECONDS=0.1",
        "PROCESS.WAIT(TIMEOUT=EXIT_CENSUS_GRACE_SECONDS)",
    ):
        require(token in compact, f"bounded runner missing {token}")
    require("RETRY" not in compact, "bounded runner must not retry")


def check_xsm_harness(text: str) -> None:
    code = fortran_without_comments(text)
    compact = packed(code)
    main = packed(code.split("contains",1)[0])
    for token in (
        "CALLRUN_POSITIVE_XSM()",
        "CALLRUN_SENTINEL_REJECTION()",
        "CALLRUN_TOMBSTONE_REJECTION()",
        "CALLRUN_EARLY_REJECTION()",
        "CALLRUN_LATE_REJECTION(2,LATE2_PATH)",
        "CALLRUN_LATE_REJECTION(3,LATE3_PATH)",
    ):
        require(main.count(token) == 1,
                f"XSM harness case inventory differs for {token}")
    require("INTEGER,PARAMETER::EXPECTED_CALLS=6" in compact,
            "XSM harness call inventory is not closed")
    require(compact.count("CALLSPOR64_B2J_PROJECT_ARCHIVE(") == 5,
            "XSM harness production-call sites differ")
    require(compact.count("CALLREQUIRE_TARGET_ABSENT(") == 6,
            "XSM harness must start with six nonexistent output paths")
    for token in (
        "CALLLCMOP(ROOT,PATH,0,2,0)",
        "CALLLCMOP(ROOT,PATH,2,2,0)",
        "CALLLCMDEL(OUTPUT,'SENTINEL')",
        "CALLREQUIRE_FRESH_EMPTY_XSM(OUTPUT)",
        "IF(MEMORY_BACKED.OR.OBJECT_LENGTH/=-1.OR."
        "TRIM(OBJECT_NAME)/='/'.OR.EMPTY.NEQV.EXPECTED_EMPTY)",
        "EPS(1)=NEAREST(EPS(1),1.0_REAL32)",
        "SOURCE_GROUP(1)=IEEE_VALUE(0.0_REAL64,IEEE_QUIET_NAN)",
        "CALLB2J_REQUIRE_EXACT_INVENTORY(OUTPUT,",
        "CALLB2J_REQUIRE_ABSENT(OUTPUT,'SYSTEM')",
        "CALLB2J_VERIFY_DEEP_SENTINEL(INPUT,OUTPUT,SENTINEL)",
        "IF(B2J_BITS32(MIRROR32(IU))/="
        "B2J_BITS32(REAL(AUTHORITY64(IU),REAL32)))",
    ):
        require(token in compact, f"XSM harness missing {token}")
    require(compact.count("CALLREQUIRE_TOMBSTONED_XSM(OUTPUT)") == 2,
            "XSM harness must verify tombstone before and after reopen")
    tombstone = packed(routine(code,"RUN_TOMBSTONE_REJECTION"))
    tombstone_order = (
        "CALLLCMDEL(OUTPUT,'SENTINEL')",
        "CALLREQUIRE_TOMBSTONED_XSM(OUTPUT)",
        "CALLLCMCL(OUTPUT,1)",
        "CALLOPEN_READ_ONLY_XSM(TOMBSTONE_PATH,OUTPUT)",
    )
    positions = [tombstone.index(token) for token in tombstone_order]
    second_tombstone = tombstone.index(
        "CALLREQUIRE_TOMBSTONED_XSM(OUTPUT)",positions[1]+1
    )
    require(positions == sorted(positions) and
            positions[-1] < second_tombstone,
            "XSM tombstone close/reopen verification order differs")
    for name in ("RUN_EARLY_REJECTION","RUN_LATE_REJECTION"):
        rejection = packed(routine(code,name))
        close = rejection.index("CALLLCMCL(OUTPUT,1)")
        reopen = rejection.index("CALLOPEN_READ_ONLY_XSM(",close)
        empty = rejection.index("CALLREQUIRE_FRESH_EMPTY_XSM(OUTPUT)",reopen)
        require(close < reopen < empty,
                f"{name} close/reopen/empty verification order differs")
    require(compact.count("CALLLCMCL(OUTPUT,1)") == 10,
            "XSM harness close/reopen sites differ")
    require(compact.count("WRITE(*,'(A)')") == 6,
            "XSM harness fixed output must contain exactly six records")
    for output in (
        "B2LB2J-XSM-TARGETPASS",
        "B2LB2J-XSM-CALLS=6COMMITS=1REJECTIONS=5",
        "B2LB2J-XSM-REOPEN-CHECKS=6PROJECTED=1",
        "B2LB2J-XSM-ROOT-ENTRIES=7AUTHORITY-ENTRIES=4",
        "B2LB2J-XSM-LATE-B2H-REJECTIONS=2EARLY-REJECTIONS=3",
        "B2LB2J-XSM-DRAGON=0ASM=0FLU=0CONT=0",
    ):
        require(output in compact,
                f"XSM harness fixed evidence differs for {output}")
    for forbidden in (
        "CALLASM(", "CALLASMDRV(", "CALLFLU(", "CALLSPOR64K(",
        "RELAX", "DAMP", "CLIP", "FLOOR", "REFERENCE_DISTANCE",
    ):
        require(forbidden not in compact,
                f"XSM harness contains forbidden token {forbidden}")


def check_runner(text: str) -> None:
    compact = packed(text.replace("\\\n",""))
    require("RUN_B2L=${RUN_B2L:-0}" in compact,
            "runtime activation must default off")
    require("PRESERVE_B2L_FAILURE=${PRESERVE_B2L_FAILURE:-0}" in compact,
            "failure preservation must default off")
    require('["$RUN_B2L"=1]' in compact,
            "only exact RUN_B2L=1 may activate Dragon")
    require(compact.count('PYTHON3"$BOUNDED"ASM') == 1,
            "runner must authorize exactly one bounded ASM process")
    require(compact.count('PYTHON3"$BOUNDED"PREPARE') == 2,
            "runner must authorize one XSM harness and one materializer")
    xsm_call = (
        'PYTHON3"$BOUNDED"PREPARE"$BUILD_DIR/'
        'TEST_B2J_XSM_TARGET"-"$XSM_CASE_DIR/XSM_TARGET.LOG"'
        'AX.XSMARCHIVE.XSMAXIAL_TRACK.XSM'
    )
    materializer_call = (
        'PYTHON3"$BOUNDED"PREPARE"$BUILD_DIR/'
        'PREPARE_B2L_PROJECTED"-"$CASE_DIR/PREPARE.LOG"'
        'AX.XSMARCHIVE.XSMAXIAL_TRACK.XSMPROJECTED.XSM'
    )
    require(compact.count(xsm_call) == 1,
            "runner must execute one bounded XSM lifecycle harness")
    require(compact.count(materializer_call) == 1,
            "runner must retain one opt-in PROJECTED materializer")
    default_off = 'IF["$RUN_B2L"=0];THEN'
    require(default_off in compact,
            "runner default-off branch differs")
    require(compact.index(xsm_call) < compact.index(default_off) <
            compact.index(materializer_call),
            "XSM lifecycle must run before the default-off return")
    require("XSM_LOG_LINES=$(WC-L<\"$XSM_CASE_DIR/XSM_TARGET.LOG\")" in
            compact,
            "runner must enforce a closed XSM harness output inventory")
    for symbol in ("DOORFV","MCCGF","MCGMRE"):
        require(symbol in compact,
                f"runner XSM symbol denylist lacks {symbol}")
    require('COUNT_EXACT1"T${SYMBOL}$"' in compact,
            "runner must require defined production procedure symbols")
    for marker in (
        "^>\\|B2L-ONE-PLANE-REAL-ASM-BEGIN",
        "^>\\|B2L-ONE-PLANE-REAL-ASM-COMPLETE",
    ):
        require(text.count(marker) == 1,
                "runner must match one exact CLE ECHO record")
    require("if grep -E -- \\\n  '->@BEGIN MODULE" in text,
            "forbidden-module grep must not parse its pattern as an option")


def check_production(asm_text: str, asmdrv_text: str) -> None:
    asm_code = packed(fortran_without_comments(asm_text))
    asmdrv_code = packed(fortran_without_comments(asmdrv_text))
    require(asm_code.count("CALLXDRTA2") == 1,
            "production ASM must call zero-argument XDRTA2 once")
    require("ELSEIF(TEXT4.EQ.'LK1D')THEN" in asm_code,
            "production ASM lacks LK1D parser")
    require("S0PHYS(0:NBMIX,IGR)=XSSIGW(0:NBMIX,1,IGR)" in asmdrv_code,
            "production ASMDRV lacks physical S0 capture")
    require(
        "XSSIGW(0:NBMIX,1,IGR)=S0PHYS(0:NBMIX,IGR)-LEAK1D(IGR)"
        in asmdrv_code,
        "production ASMDRV leakage order differs",
    )


def check_b2j_target(text: str) -> None:
    code = packed(fortran_without_comments(text))
    project = packed(routine(fortran_without_comments(text),
                             "SPOR64_B2J_PROJECT_ARCHIVE"))
    require(
        "EMPTY_LCM_ROOT=EMPTY.AND.OBJECT_LENGTH==-1.AND."
        "TRIM(OBJECT_NAME)=='/'" in code,
        "production B2j must admit a fresh root independent of medium",
    )
    require("EMPTY_LCM_ROOT=MEMORY_BACKED.AND." not in code,
            "production B2j must not exclude a fresh XSM root")
    alias_tokens = []
    for left,right in (
        ("IPARCHIVEOUT","IPAX"),
        ("IPARCHIVEOUT","IPAXTRACK"),
        ("IPARCHIVEOUT","IPARCHIVE"),
        ("IPAX","IPAXTRACK"),
        ("IPAX","IPARCHIVE"),
        ("IPAXTRACK","IPARCHIVE"),
    ):
        token = f"IF(C_ASSOCIATED({left},{right}))RETURN"
        alias_tokens.append(token)
        require(project.count(token) == 1,
                f"production B2j alias guard inventory differs for "
                f"{left}/{right}")
    entry_fresh = "IF(.NOT.EMPTY_LCM_ROOT(IPARCHIVEOUT))RETURN"
    precommit_fresh = (
        "IF(.NOT.EMPTY_LCM_ROOT(IPARCHIVEOUT))THEN"
        "CALLCLOSE_STAGES(STAGED_FLUX)RETURNENDIF"
    )
    require(project.count(entry_fresh) == 1,
            "production B2j entry freshness guard differs")
    require(project.count(precommit_fresh) == 1,
            "production B2j precommit freshness guard differs")
    require(all(project.index(token) < project.index(entry_fresh)
                for token in alias_tokens),
            "production B2j alias guards must precede target inspection")
    first_stage = "CALLLCMOP(STAGED_FLUX(IP),STAGE_NAME(IP),0,1,0)"
    first_write = "CALLLCMPTC(IPARCHIVEOUT,'SIGNATURE',12,SIGNATURE)"
    require(project.count(first_stage) == 1,
            "production B2j private-stage creation differs")
    require(project.count(first_write) == 1,
            "production B2j first caller-visible write differs")
    require(project.index(entry_fresh) < project.index(first_stage) <
            project.index(precommit_fresh) < project.index(first_write),
            "production B2j freshness/staging/write order differs")
    require(project.count("EMPTY_LCM_ROOT(IPARCHIVEOUT)") == 2,
            "production B2j must repeat freshness before its first write")
    for token in (
        "IF(B2H_STATUS==SPOR64_B2H_ADMISSION_FAILED)THEN"
        "CALLCLOSE_STAGES(STAGED_FLUX)RETURNENDIF",
        "IF(.NOT.STAGED_PROJECTED_OBJECT_IS_COMMITTED(STAGED_FLUX(IP),"
        "RHO64,PROJECTED_EPOCH,LEAKAGE64((IP-1)*NGRP+1:IP*NGRP)))THEN"
        "CALLCLOSE_STAGES(STAGED_FLUX)RETURNENDIF",
        "IF(.NOT.EMPTY_LCM_ROOT(IPARCHIVEOUT))THEN"
        "CALLCLOSE_STAGES(STAGED_FLUX)RETURNENDIF",
    ):
        require(token in project,
                "production B2j staged-failure cleanup differs")
    require(project.count("CALLCLOSE_STAGES(STAGED_FLUX)") == 4,
            "production B2j stage cleanup inventory differs")
    success_cleanup = (
        "CALLCLOSE_STAGES(STAGED_FLUX)"
        "OUTPUT_AUTHORITY=LCMDID(IPARCHIVEOUT,'SPOT-R64')"
    )
    require(project.count(success_cleanup) == 1,
            "production B2j success-path stage cleanup differs")
    epoch = "CALLLCMPUT(OUTPUT_AUTHORITY,'EPOCH',1,1,PROJECTED_EPOCH)"
    require(project.count(epoch) == 1,
            "production B2j must write one final epoch marker")
    post_epoch = project[project.index(epoch)+len(epoch):]
    for mutation in (
        "LCMPUT(", "LCMPTC(", "LCMEQU(", "LCMDEL(",
        "LCMDID(", "LCMLID(", "LCMDIL(",
    ):
        require(mutation not in post_epoch,
                f"production B2j mutation {mutation} follows EPOCH")


def main() -> None:
    for path in (DECK,PREPARER,POSTERIOR,BOUNDED,RUNNER,XSM_HARNESS,
                 ASM,ASMDRV,B2J):
        require(path.is_file(),f"missing {path}")
    check_deck(DECK.read_text(encoding="utf-8"))
    check_preparer(PREPARER.read_text(encoding="utf-8"))
    check_posterior(POSTERIOR.read_text(encoding="utf-8"))
    check_bounded(BOUNDED.read_text(encoding="utf-8"))
    check_xsm_harness(XSM_HARNESS.read_text(encoding="utf-8"))
    check_runner(RUNNER.read_text(encoding="utf-8"))
    check_production(
        ASM.read_text(encoding="utf-8"), ASMDRV.read_text(encoding="utf-8")
    )
    check_b2j_target(B2J.read_text(encoding="utf-8"))
    print("B2L STATIC CONTRACT PASS")
    print("B2L DRAGON-MAX=1 ASM-MAX=1 FLU=0 CONT=0 EMPIRICAL-CONTROLS=0")


if __name__ == "__main__":
    main()

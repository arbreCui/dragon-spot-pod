#!/usr/bin/env python3
"""Fail-closed static contract for the bounded B2m three-plane ASM commit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DECK = HERE / "three_plane_real_asm_commit.x2m"
POSTERIOR = HERE / "check_b2m_three_plane_assembled.f90"
BOUNDED = HERE / "run_bounded_b2m.py"
RUNNER = HERE / "run_phase_a9b_b2m_three_plane_real_asm_commit.sh"
HOST = ROOT / "data/SpotAsmR64.c2m"
B2K = ROOT / "src/SPOR64_B2K.f90"
ASM = ROOT / "src/ASM.f"
ASMDRV = ROOT / "src/ASMDRV.f"
KDRDPR = ROOT / "Ganlib/src/kdrdpr.c"
CLE2000 = ROOT / "Ganlib/src/cle2000_c.c"
README = HERE / "README.md"
MANIFEST = HERE / "precision_manifest.json"
RUNTIME_RESULT = HERE / "runtime_result.txt"
CONTRACT_TESTS = HERE / "test_phase_a9b_b2m_three_plane_real_asm_commit_contract.py"
BOUNDED_TESTS = HERE / "test_run_bounded_b2m.py"


class GateError(RuntimeError):
    """Raised when the narrow B2m contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_without_comments(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def deck_without_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        fortran_without_comments(text),
    )
    require(match is not None, f"missing routine {name}")
    return match.group(0)


def logical_function(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\blogical\s+function\s+{re.escape(name)}\b.*?"
        rf"\bend\s+function\s+{re.escape(name)}\b",
        fortran_without_comments(text),
    )
    require(match is not None, f"missing logical function {name}")
    return match.group(0)


def ordered(code: str, fragments: tuple[str, ...], owner: str) -> None:
    position = -1
    for fragment in fragments:
        found = code.find(fragment, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def check_deck(text: str) -> None:
    code = deck_without_comments(text).upper()
    compact = packed(code)
    for token in (
        "SEQ_BINARYTRACK_F",
        "XSM_FILEPROJ_XSM",
        "XSM_FILEASSM_XSM",
        "LINKED_LISTPROJECTEDASSEMBLED",
        "PROCEDURESPOTASMR64;",
    ):
        require(token in compact, f"wrapper deck missing {token}")

    input_copy = "PROJECTED:=PROJ_XSM;"
    host_call = "ASSEMBLED:=SPOTASMR64PROJECTEDTRACK_F::;"
    evidence_copy = "ASSM_XSM:=ASSEMBLED;"
    cleanup = "PROJECTEDASSEMBLED:=DELETE:PROJECTEDASSEMBLED;"
    require(compact.count(input_copy) == 1,
            "wrapper must make one whole-object PROJECTED XSM-to-memory copy")
    require(compact.count(host_call) == 1,
            "wrapper must call SpotAsmR64 exactly once into memory LCM")
    require(compact.count(evidence_copy) == 1,
            "wrapper must make exactly one whole-object XSM evidence copy")
    require(compact.count(cleanup) == 1,
            "wrapper must release both private memory archives once")
    ordered(compact, (input_copy, host_call, evidence_copy, cleanup),
            "PROJECTED copy, memory commit, XSM evidence copy, cleanup")
    require("ASSM_XSM:=SPOTASMR64" not in compact,
            "SPOR64K must not target the XSM evidence object directly")
    require("SPOTASMR64PROJ_XSM" not in compact,
            "SpotAsmR64 must consume the unique memory PROJECTED copy")
    require(":=ASM:" not in compact and "SPOR64K:" not in compact,
            "wrapper must not duplicate the production host internals")
    for forbidden in (
        "FLU:", "SPOFSRC:", "SPOFCHK:", "QFISS", "CONT",
        "WHILE", "REPEAT", "UNTIL", "PICARD", "RELAX", "DAMP",
        "CLIP", "FLOOR", "FIT",
    ):
        require(forbidden not in code, f"forbidden wrapper token {forbidden}")
    require(code.count("B2M-THREE-PLANE-REAL-ASM-BEGIN") == 1,
            "wrapper begin marker inventory differs")
    require(code.count("B2M-THREE-PLANE-REAL-ASM-COMPLETE") == 1,
            "wrapper completion marker inventory differs")


def check_host(text: str) -> None:
    code = packed(deck_without_comments(text))
    require(
        "PARAMETERASSEMBLEDPROJECTEDTRACK_F::"
        ":::LINKED_LISTASSEMBLEDPROJECTED;:::SEQ_BINARYTRACK_F;;" in code,
        "SpotAsmR64 formal media contract differs",
    )
    require(
        "LINKED_LISTMICROLIB2MACRO0TRACKSYSTEM1SYSTEM2SYSTEM3;" in code,
        "SpotAsmR64 local SYSTEM inventory differs",
    )
    require("MODULERECOVER:ASM:SPOR64K:DELETE:END:;" in code,
            "SpotAsmR64 module allowlist differs")
    require(code.count(":=ASM:") == 3,
            "SpotAsmR64 must contain exactly three ASM calls")
    for plane in (1, 2, 3):
        block = (
            f"MICROLIB2:=RECOVER:PROJECTED::ITEM{plane};"
            "MACRO0:=MICROLIB2;MICROLIB2:=DELETE:MICROLIB2;"
            f"TRACK:=RECOVER:PROJECTED::ITEM{plane};"
            f"SYSTEM{plane}:=ASM:MACRO0TRACKTRACK_FPROJECTED::"
            f"EDIT0ARMLK1D{plane};"
            "MACRO0TRACK:=DELETE:MACRO0TRACK;"
        )
        require(block in code,
                f"SpotAsmR64 same-index plane-{plane} block differs")
    commit = "ASSEMBLED:=SPOR64K:PROJECTEDSYSTEM1SYSTEM2SYSTEM3::;"
    require(code.count(commit) == 1,
            "SpotAsmR64 must make one ordered three-SYSTEM commit")
    require(code.rfind(":=ASM:") < code.index(commit),
            "all three ASM calls must precede SPOR64K")
    for forbidden in (
        "FLU:", "SPOFSRC:", "SPOFCHK:", "QFISS", "CONT",
        "WHILE", "REPEAT", "PICARD", "RELAX", "DAMP", "CLIP",
    ):
        require(forbidden not in code,
                f"SpotAsmR64 overreaches into {forbidden}")


def check_production(asm_text: str, asmdrv_text: str) -> None:
    asm = packed(fortran_without_comments(asm_text))
    asmdrv = packed(fortran_without_comments(asmdrv_text))
    require(asm.count("CALLXDRTA2") == 1,
            "production ASM zero-argument XDRTA2 call differs")
    require("CALLXDRTA2(" not in asm,
            "production ASM XDRTA2 ABI must remain zero-argument")
    require("ELSEIF(TEXT4.EQ.'LK1D')THEN" in asm,
            "production ASM lacks the LK1D selector")
    require("ELSEIF(TEXT4.EQ.'ARM')THENIPHASE=1" in asm,
            "production ASM lacks the ARM selector")
    for token in (
        "CALLLCMGET(KPSNAP,'SPOT-LEAK1D',LEAK1D)",
        "CALLLCMPUT(IPSYS,'SPOT-LEAK1D',NGROUP,2,LEAK1D)",
        "CALLLCMPUT(IPSYS,'SPOT-L1-SNAP',1,1,ISNAP_L1)",
        "XSSIGT(IMAT,IGR,1)=XSSIGT(IMAT,IGR,1)-XSSCOR(IMAT,IGR)",
        "XSSIGW(IMAT,1,IGR)=XSSIGW(IMAT,1,IGR)-XSSCOR(IMAT,IGR)",
        "S0PHYS(0:NBMIX,IGR)=XSSIGW(0:NBMIX,1,IGR)",
        "XSSIGW(0:NBMIX,1,IGR)=S0PHYS(0:NBMIX,IGR)-LEAK1D(IGR)",
        "CALLLCMPUT(KPSYS,'SPOT-S0-PHYS',NBMIX+1,2,",
    ):
        require(token in asmdrv, f"production ASM formula missing {token}")


def check_loader(kdrdpr_text: str, cle2000_text: str) -> None:
    """Freeze source visibility separately from precompiled-object use."""
    kdr = re.sub(r"\s+", "", kdrdpr_text).upper()
    cle = re.sub(r"\s+", "", cle2000_text).upper()
    for token in (
        'SPRINTF(FILINP,"%S.C2M",FILENM);',
        'SPRINTF(FILOBJ,"%S.O2M",FILENM);',
        'FILE=FOPEN(FILINP,"R");',
        'MY_NODE->TYPE=-IPARAM;',
        'STRCPY(MY_NODE->OSNAME,FILOBJ);',
    ):
        require(token in kdr, f"kdrdpr visibility contract missing {token}")
    source_probe = kdr.index('FILE=FOPEN(FILINP,"R");')
    object_name = kdr.index('SPRINTF(FILOBJ,"%S.O2M",FILENM);')
    osname = kdr.index('STRCPY(MY_NODE->OSNAME,FILOBJ);')
    require(object_name < source_probe < osname,
            "kdrdpr must verify source visibility then select the object name")

    object_probe = 'ICFILE=FOPEN(FILOBJ,"R");'
    missing_branch = 'IF(ICFILE==NULL){'
    source_open = 'ICINP=FOPEN(FILINP,"R");'
    compile_call = 'IRETCD=CLEPIL(ICINP,ICOUT,ICOBJ,CLECST);'
    object_open = 'ICOBJ=KDIOP_C(FILOBJ,1);'
    for token in (object_probe, missing_branch, source_open,
                  compile_call, object_open):
        require(token in cle, f"cle2000 selection contract missing {token}")
    require(cle.index(object_probe) < cle.index(missing_branch) <
            cle.index(source_open) < cle.index(compile_call) <
            cle.index(object_open),
            "cle2000 must probe o2m before its missing-object compile branch")
    require("STAT(" not in cle and "MTIME" not in cle,
            "precompiled selection must not depend on source timestamps")


def check_b2k(text: str) -> None:
    code = fortran_without_comments(text)
    compact = packed(code)
    body = packed(routine(code, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE"))
    wrapper = packed(routine(code, "SPOR64K"))
    for token in ("NSNAP=3", "PROJECTED_EPOCH=1", "ASSEMBLED_EPOCH=1"):
        require(token in compact, f"production B2k constant missing {token}")
    for token in (
        "STATUS=SPOR64_B2K_ADMISSION_FAILED",
        "STATUS=SPOR64_B2K_ARCHIVE_ASSEMBLED",
        "IF(C_ASSOCIATED(IPSYSTEMS(IP),IPSYSTEMS(IR)))RETURN",
        "PROJECTED_ARCHIVE_ROOT_IS_EXACT(IPPROJECTED)",
        "CANDIDATE_SYSTEM_ROOT_IS_EXACT(IPSYSTEMS(IP))",
        "ABSENT_RECORD(IPSYSTEMS(IP),'SPOT-R64')",
        "SYSTEM_PAYLOAD_IS_VALID(IPSYSTEMS(IP),INPUT_MACRO(IP),",
        "CALLLCMEQU(IPSYSTEMS(IP),STAGED_SYSTEM(IP))",
        "CALLLCMEQU(STAGED_SYSTEM(IP),OUTPUT_ITEM)",
        "CALLLCMEQU(INPUT_FLUX(IP),OUTPUT_ITEM)",
    ):
        require(token in body, f"production B2k contract missing {token}")
    require(body.count("IF(.NOT.EMPTY_LCM_ROOT(IPOUT))") == 2,
            "production B2k must repeat output freshness before publication")
    root_epoch = "CALLLCMPUT(ROOT_AUTHORITY,'EPOCH',1,1,ASSEMBLED_EPOCH)"
    require(body.count(root_epoch) == 1,
            "production B2k root epoch inventory differs")
    post_epoch = body[body.index(root_epoch) + len(root_epoch):]
    for mutation in (
        "LCMPUT(", "LCMPTC(", "LCMEQU(", "LCMDEL(",
        "LCMDID(", "LCMLID(", "LCMDIL(",
    ):
        require(mutation not in post_epoch,
                f"production B2k mutation follows root EPOCH: {mutation}")

    empty_root = packed(logical_function(code, "EMPTY_LCM_ROOT"))
    require(
        "EMPTY_LCM_ROOT=IS_LCM.AND.EMPTY.AND.OBJECT_LENGTH==-1.AND."
        "TRIM(OBJECT_NAME)=='/'" in empty_root,
        "B2m freezes SPOR64K as a memory-LCM logical commit",
    )
    require(
        "CALLSPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(KENTRY(1),KENTRY(2),"
        "SYSTEMS,STATUS)" in wrapper,
        "production SPOR64K wrapper call differs",
    )
    require("SYSTEMS=KENTRY(3:5)" in wrapper,
            "production SPOR64K SYSTEM order differs")
    require("IF(JENTRY(1)/=0.OR.ANY(JENTRY(2:5)/=2))" in wrapper,
            "production SPOR64K access modes differ")

    stripped = re.sub(r"'[^']*'|\"[^\"]*\"", " ", code)
    identifiers = {item.upper() for item in re.findall(
        r"(?i)\b[A-Z][A-Z0-9_]*\b", stripped
    )}
    for forbidden in (
        "FLU", "FLUDRV", "FLU2DR", "SPOFSRC", "QFISS", "CONT",
        "ALPHA", "OMEGA", "RELAX", "DAMP", "CLIP", "AITKEN",
        "ANDERSON",
    ):
        require(forbidden not in identifiers,
                f"production B2k contains forbidden path/control {forbidden}")


def check_posterior(text: str) -> None:
    code = fortran_without_comments(text)
    compact = packed(code)
    for token in (
        "NGRP=370", "NSNAP=3", "NMAT=8", "NUNKNO=14",
        "RESPONSE_LENGTHS(12)=[32,14,32,14,8,8,8,8,8,8,8,14]",
        "REAL32_MAGNITUDE_MASK=INT(Z'7FFFFFFF',INT32)",
        "CALLVERIFY_ASSEMBLED_ARCHIVE(",
        "CALLVERIFY_PLANE_LIFECYCLES(",
        "CALLVERIFY_COPIED_SUBTREES(",
        "CALLVERIFY_ASSEMBLED_SYSTEMS(",
        "CALLCOMPARE_DICTIONARY(",
        "CALLCOMPARE_LIST(",
        "IF(.NOT.EXACT_INVENTORY(",
        "CALLLCMGET(SYSTEM_GROUP,'DRAGON-TXSC',TX)",
        "CALLLCMGET(SYSTEM_GROUP,'SPOT-S0-PHYS',SPHYS)",
        "CALLLCMGET(SYSTEM_GROUP,'DRAGON-S0XSC',SUSED)",
        "EXPECTED_TX(IM)=EXPECTED_TX(IM)-TRANC(IM)",
        "EXPECTED_SPHYS(IM)=EXPECTED_SPHYS(IM)-TRANC(IM)",
        "EXPECTED_SUSED(0)=EXPECTED_SPHYS(0)-LEAKAGE(IG)",
        "EXPECTED_SUSED(IM)=EXPECTED_SPHYS(IM)-LEAKAGE(IG)",
        "IEEE_IS_FINITE(RESPONSE)",
        "IAND(TRANSFER(RESPONSE,0_INT32,SIZE(RESPONSE)),"
        "REAL32_MAGNITUDE_MASK)/=0_INT32",
    ):
        require(token in compact, f"independent posterior missing {token}")
    for token in (
        "CALLLCMOP(PROJECTED,TRIM(PROJECTED_PATH),2,2,0)",
        "CALLLCMOP(ASSEMBLED,TRIM(ASSEMBLED_PATH),2,2,0)",
        "IF(C_ASSOCIATED(PROJECTED,ASSEMBLED))",
        "COPIED_ITEMS/=3*NSNAP",
        "GROUP_RECORDS/=NSNAP*NGRP*SIZE(GROUP_NAMES)",
        "SYSTEM_STATES/=NSNAP.OR.FLUX_STATES/=NSNAP",
    ):
        require(token in compact, f"posterior closed inventory missing {token}")
    for token in (
        "'ASSEMBLED'", "'PROJECTED'", "'SPOT-R64'", "'EPOCH'",
        "'SYSTEM'", "'SPOT-L1-SNAP'", "'SPOT-LEAK1D'",
    ):
        require(token in compact, f"posterior lifecycle check missing {token}")
    for expected in (
        "RESPONSE_VALUES/=NSNAP*NGRP*SUM(RESPONSE_LENGTHS)",
        "TX_CHECKS/=NSNAP*NGRP*(NMAT+1)",
        "SPHYS_CHECKS/=NSNAP*NGRP*(NMAT+1)",
        "SUSED_CHECKS/=NSNAP*NGRP*(NMAT+1)",
        "LEAKAGE_CHECKS/=NSNAP*NGRP",
    ):
        require(expected in compact,
                f"posterior exact aggregate count missing {expected}")
    require(
        "ANY(RESPONSE_NONZERO_BY_PLANE<=0)" in compact,
        "posterior must reject an all-zero response payload in each plane",
    )
    for fixed_output in (
        "B2MTHREE-PLANECOMMITPOSTERIORPASS",
        "B2MTHREE-PLANE-B2K-POSTERIOR=COMPATIBLEEMPIRICAL-CONTROLS=0",
        "B2MRESPONSE-ACCURACY=NOT-EVALUATEDCONVERGENCE=NOT-EVALUATED",
    ):
        require(fixed_output in compact,
                f"posterior fixed scientific claim differs: {fixed_output}")
    for forbidden in (
        "USESPOR64_B2K", "CALLSPOR64K(", "CALLASM(", "CALLASMDRV(",
        "CALLFLU(", "TOLERANCE", "REFERENCE_DISTANCE", "RELAX", "DAMP",
        "CLIP", "FLOOR", "FIT", "NONZERO_FRACTION",
    ):
        require(forbidden not in compact,
                f"posterior contains solver/empirical token {forbidden}")


def check_bounded(text: str) -> None:
    compact = packed(text)
    for profile in ('"PREPARE":{', '"ASSEMBLE3":{', '"POSTERIOR":{'):
        require(profile in compact, f"bounded runner missing profile {profile}")
    for token in (
        '"WALL_SECONDS":30', '"CPU_SECONDS":20',
        '"RSS_BYTES":2*1024**3', '"FILE_BYTES":512*1024**2',
        '"WALL_SECONDS":30', '"CPU_SECONDS":20',
        '"RSS_BYTES":2*1024**3', '"FILE_BYTES":512*1024**2',
        "START_NEW_SESSION=TRUE", "OS.KILLPG(PROCESS.PID,SIGNAL.SIGTERM)",
        "OS.KILLPG(PROCESS.PID,SIGNAL.SIGKILL)",
        '"OMP_NUM_THREADS":"1"', '"OPENBLAS_NUM_THREADS":"1"',
        "RESOURCE.RLIMIT_CPU", "RESOURCE.RLIMIT_FSIZE",
        "RESOURCE.RLIMIT_CORE", "PROCESS_RSS_BYTES(PROCESS.PID)",
        'RSS_BYTES>PROFILE["RSS_BYTES"]',
    ):
        require(token in compact, f"bounded runner missing {token}")
    # A literal retry loop or subprocess restart is forbidden.  Evidence text
    # such as AUTOMATIC-RETRIES=0 is checked elsewhere and is harmless.
    for forbidden in ("FORATTEMPTIN", "MAX_RETRIES", "RETRY("):
        require(forbidden not in compact,
                f"bounded runner contains retry path {forbidden}")


def check_runner(text: str) -> None:
    compact = packed(text.replace("\\\n", ""))
    require("RUN_B2M=${RUN_B2M:-0}" in compact,
            "real activation must default off")
    require("PRESERVE_B2M_FAILURE=${PRESERVE_B2M_FAILURE:-0}" in compact,
            "failure preservation must default off")
    require('["$RUN_B2M"=1]' in compact,
            "only exact RUN_B2M=1 may activate Dragon")
    default_off = 'IF["$RUN_B2M"=0];THEN'
    require(default_off in compact, "runner lacks a default-off return")
    require(compact.count('PYTHON3"$BOUNDED"ASSEMBLE3') == 1,
            "runner must authorize exactly one bounded Dragon process")
    require(compact.count('PYTHON3"$BOUNDED"PREPARE') == 1,
            "runner must authorize exactly one PROJECTED materializer")
    require(compact.count('PYTHON3"$BOUNDED"POSTERIOR') == 2,
            "runner must repeat the independent read-only posterior twice")
    require(compact.index(default_off) < compact.index('PYTHON3"$BOUNDED"PREPARE'),
            "default-off return must precede all real-process activation")
    for token in (
        "PROJECTED.XSM", "ASSEMBLED.XSM", "THREE_PLANE_REAL_ASM_COMMIT.X2M",
        "SPOTASMR64", "CHECK_B2M_THREE_PLANE_REAL_ASM_COMMIT",
        "PROJECTED_HASH", "ASSEMBLED_HASH",
    ):
        require(token in compact, f"runner evidence path missing {token}")
    for token in (
        "EXPECTED_PROJECTED_HASH=C010C0A860884A4E4D3842DFFE45FFB4898F2AACA99557E0411EE8C66D60B90C",
        "EXPECTED_PROJECTED_BYTES=225315452",
        "EXPECTED_C2M_SOURCE_HASH=31EC89036BBD2EA62B27FBD4DFF5AA1054F3F24997E383F05389E1DDA91E364D",
        "COPY_EXACT\"$C2M_SOURCE\"\"$CASE_DIR/SPOTASMR64.C2M\"",
        "COPY_EXACT\"$BUILD_DIR/SPOTASMR64.O2M\"\"$CASE_DIR/SPOTASMR64.O2M\"",
        "REQUIRE_HASH\"$CASE_DIR/SPOTASMR64.C2M\"\"$EXPECTED_C2M_SOURCE_HASH\"",
        "REQUIRE_HASH\"$CASE_DIR/SPOTASMR64.O2M\"\"$C2M_OBJECT_HASH\"",
        "[!-E\"$CASE_DIR/PROJECTED.XSM\"]",
        "[!-E\"$CASE_DIR/ASSEMBLED.XSM\"]",
        "CMP\"$CASE_DIR/POSTERIOR_A.LOG\"\"$CASE_DIR/POSTERIOR_B.LOG\"",
        "PROJECTEDINPUTMUTATEDDURINGTHREE-PLANEASSEMBLY",
        "PROJECTEDINPUTMUTATEDDURINGPOSTERIOR",
        "COMMIT=MEMORY-LOGICAL-ASSEMBLED/1PERSISTENCE=WHOLE-OBJECT-XSM-EVIDENCE-COPY",
        "RESPONSE-NUMERICAL-ACCURACY=NOT-EVALUATED",
        "RADIAL-CONVERGENCE=NOT-EVALUATEDOUTER-PICARD=NOT-EVALUATED",
    ):
        require(token in compact, f"runner scientific boundary missing {token}")
    require("COMPILING_MAIN\\.C2MFILE|BADOBJECTS_MAIN\\.C2MFILE" in compact,
            "runner must reject both runtime procedure compilation-error markers")
    require("RUNTIMEPROCEDURECOMPILATIONERRORDETECTED" in compact,
            "runner must classify procedure compilation errors as invalid")
    require(compact.count('[!-E"$CASE_DIR/SPOTASMR64.L2M"]') == 3,
            "runner must exclude the source-compilation listing before and after execution")
    require("RUNTIMEPROCEDURESOURCE-COMPILATIONBRANCHDETECTED" in compact,
            "runner must classify an l2m source-compilation witness as invalid")
    for token in (
        "DRAGON-EXECUTIONS=1", "ASM-EXECUTIONS=3", "XDRTA2-CALLS=3",
        "SPOR64K-EXECUTIONS=1", "FLU-FLUX-SOLVES=0", "PICARD-MAPS=0",
        "QFISS=NOT-BUILT", "CONT=NOT-EXECUTED",
        "EMPIRICAL-CONTROLS=0", "AUTOMATIC-RETRIES-WITHIN-ACCEPTED-RUN=0",
    ):
        require(token in compact, f"runner fixed census missing {token}")
    for marker in (
        "^>\\|B2M-THREE-PLANE-REAL-ASM-BEGIN",
        "^>\\|B2M-THREE-PLANE-REAL-ASM-COMPLETE",
    ):
        require(text.count(marker) == 1,
                f"runner must count exact CLE marker {marker}")
    require("SPOR64K" in compact and "->@BEGINMODULE" in compact,
            "runner must census the production SPOR64K execution")
    require("FLU|SPOFSRC|SPOFCHK|CONT" in compact,
            "runner must reject forbidden module execution")
    require("IFGREP-E--" in compact,
            "forbidden-module grep must use an explicit option separator")
    require("SHASUM-A256" in compact,
            "runner must preserve PROJECTED and hash the evidence copy")


def check_assets(readme_text: str, manifest_text: str) -> None:
    for phrase in (
        "in-memory logical commit", "whole-object XSM evidence copy",
        "loader visibility", "does not dynamically recompile",
        "SpotAsmR64.l2m",
        "does **not** establish", "response-matrix numerical accuracy",
        "radial convergence", "outer Picard", "default-off",
        "not claim that `SPOR64K` targeted XSM directly",
    ):
        require(phrase.lower() in readme_text.lower(),
                f"README scientific boundary missing {phrase}")
    manifest = json.loads(manifest_text)
    require(manifest["phase"] == "A9b-B2m", "manifest phase differs")
    require(manifest["host_route"]["asm_calls"] == 3,
            "manifest ASM count differs")
    require(manifest["host_route"]["spor64k_calls"] == 1,
            "manifest SPOR64K count differs")
    require(manifest["host_route"]["flu_calls"] == 0,
            "manifest FLU boundary differs")
    require(manifest["commit_semantics"]["spor64k_target_medium"] ==
            "memory LCM", "manifest must not claim direct XSM commit")
    require(manifest["commit_semantics"]["direct_xsm_spor64k_target"] is False,
            "manifest direct-XSM claim differs")
    loader = manifest["loader_contract"]
    require(loader["runtime_l2m_listing_absence_required"] is True,
            "manifest must require absence of the source-compile listing")
    resources = manifest["resource_policy"]
    require(resources["fixed_wall_cpu_file_and_core_limits"] is True,
            "manifest hard-limit description differs")
    require(resources["sampled_leader_rss_ceiling"] is True and
            resources["rss_sampling_interval_seconds"] == 0.05 and
            resources["process_group_rss_aggregated"] is False,
            "manifest RSS sampling scope differs")
    posterior = manifest["posterior_contract"]
    require(posterior["response_finite_values_total"] == 179820,
            "manifest response count differs")
    require(posterior["group_directories_total"] == 1110,
            "manifest group-directory count differs")
    require(posterior["exact_group_records_total"] == 16650,
            "manifest group-record count differs")
    require(posterior["leakage_binary32_bit_checks"] == 1110,
            "manifest leakage count differs")
    for name in ("txsc", "s0phys", "s0used"):
        require(posterior[f"{name}_binary32_bit_checks"] == 9990,
                f"manifest {name} count differs")
    semantic = manifest["semantic_boundary"]
    for claim in (
        "real_asm_planes_1_to_3_executed",
        "three_plane_spor64k_commit_executed",
        "memory_logical_commit_validated",
        "whole_object_xsm_evidence_copy_validated",
        "b2k_posterior_compatible",
        "real_execution_evaluated",
        "response_schema_and_xs_identities_validated",
    ):
        require(semantic[claim] is True,
                f"accepted semantic claim differs: {claim}")
    require(semantic["response_numerical_accuracy_evaluated"] is False,
            "manifest must not claim response accuracy")
    require(semantic["radial_flux_solved"] is False,
            "manifest must not claim a radial solve")
    accepted_runtime = {
        "utc": "2026-08-07T03:45:31Z",
        "materializer_executions": 1,
        "dragon_executions": 1,
        "procedure_calls": 1,
        "asm_executions": 3,
        "spor64k_executions": 1,
        "xdrta2_calls": 3,
        "radial_operator_assemblies": 3,
        "flu_flux_solves": 0,
        "picard_maps": 0,
        "qfiss_built": False,
        "cont_executed": False,
        "automatic_retries": 0,
        "prepare_wall_seconds": 1.190,
        "assemble3_wall_seconds": 2.325,
        "posterior_wall_seconds": [1.026, 0.534],
        "posterior_repetitions": 2,
        "posterior_outputs_byte_identical": True,
        "full_copy_records": 71280,
        "full_copy_32bit_words": 54477882,
        "response_finite_values": 179820,
        "response_nonzero_values": 106554,
        "response_nonzero_by_plane": [35518, 35518, 35518],
        "leakage_binary32_bit_checks": 1110,
        "txsc_binary32_bit_checks": 9990,
        "s0phys_binary32_bit_checks": 9990,
        "s0used_binary32_bit_checks": 9990,
        "projected_sha256":
            "c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c",
        "projected_bytes": 225315452,
        "assembled_sha256":
            "16f79f8fd97ff90ca9bd892cdeab27337fafb3ec6189d9b00b90375fcc596e79",
        "assembled_bytes": 227840384,
        "empirical_controls": 0,
    }
    require(manifest["accepted_runtime"] == accepted_runtime,
            "accepted runtime evidence differs from the frozen B2m result")
    development = manifest["development_history"]
    require(development["prior_invalid_activations"] == 1,
            "manifest invalid-activation inventory differs")
    require(development["prior_actual_asm_executions"] == 0,
            "manifest must record that the invalid activation never reached ASM")
    require(development["invalid_runs_used_as_scientific_evidence"] == 0,
            "invalid activation cannot contribute scientific evidence")
    validation = manifest["validation"]
    contract_count = len(re.findall(
        r"(?m)^\s+def\s+test_[A-Za-z0-9_]+\(",
        CONTRACT_TESTS.read_text(encoding="utf-8"),
    ))
    bounded_count = len(re.findall(
        r"(?m)^\s+def\s+test_[A-Za-z0-9_]+\(",
        BOUNDED_TESTS.read_text(encoding="utf-8"),
    ))
    require(validation["static_contract_tests"] == contract_count == 49,
            "manifest static mutation-test inventory differs")
    require(validation["bounded_resource_tests"] == bounded_count == 8,
            "manifest bounded-test inventory differs")
    require(validation["total_default_tests"] == contract_count + bounded_count,
            "manifest total default-test inventory differs")
    require(validation["default_dragon_executions"] == 0 and
            validation["default_asm_executions"] == 0 and
            validation["default_spor64k_executions"] == 0,
            "manifest default path must execute no production calculation")


def check_runtime_result(result_text: str, manifest_text: str) -> None:
    expected_hash = (
        "fda987a1bcedc4b416f008f888ce41fd2635fdb9e8b89c09e8d9d7e2c587295d"
    )
    require(hashlib.sha256(result_text.encode("utf-8")).hexdigest() ==
            expected_hash, "accepted runtime-result receipt differs")
    lines = [line for line in result_text.splitlines() if line]
    require(lines[0] == "SPOR64 PHASE-A9b-B2m ACCEPTED RUNTIME RESULT",
            "accepted runtime-result header differs")
    require(len(lines) == 57,
            "accepted runtime-result nonempty-line inventory differs")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        require("=" in line, "accepted runtime-result field is malformed")
        key, value = line.split("=", 1)
        require(key not in fields,
                f"duplicate accepted runtime-result field: {key}")
        fields[key] = value

    manifest = json.loads(manifest_text)
    runtime = manifest["accepted_runtime"]
    expected = {
        "UTC": runtime["utc"],
        "ACCEPTED-RUN-MATERIALIZER-EXECUTIONS":
            str(runtime["materializer_executions"]),
        "ACCEPTED-RUN-DRAGON-EXECUTIONS":
            str(runtime["dragon_executions"]),
        "ACCEPTED-RUN-SPOTASMR64-PROCEDURES":
            str(runtime["procedure_calls"]),
        "ACCEPTED-RUN-ASM-EXECUTIONS": str(runtime["asm_executions"]),
        "ACCEPTED-RUN-SPOR64K-EXECUTIONS":
            str(runtime["spor64k_executions"]),
        "ACCEPTED-RUN-XDRTA2-CALLS": str(runtime["xdrta2_calls"]),
        "ACCEPTED-RUN-PREPARER-WALL-SECONDS":
            f'{runtime["prepare_wall_seconds"]:.3f}',
        "ACCEPTED-RUN-ASSEMBLE3-WALL-SECONDS":
            f'{runtime["assemble3_wall_seconds"]:.3f}',
        "ACCEPTED-RUN-POSTERIOR-A-WALL-SECONDS":
            f'{runtime["posterior_wall_seconds"][0]:.3f}',
        "ACCEPTED-RUN-POSTERIOR-B-WALL-SECONDS":
            f'{runtime["posterior_wall_seconds"][1]:.3f}',
        "RADIAL-OPERATOR-ASSEMBLIES":
            str(runtime["radial_operator_assemblies"]),
        "FLU-FLUX-SOLVES": str(runtime["flu_flux_solves"]),
        "PICARD-MAPS": str(runtime["picard_maps"]),
        "FULL-COPY-RECORDS": str(runtime["full_copy_records"]),
        "FULL-COPY-32BIT-WORDS": str(runtime["full_copy_32bit_words"]),
        "RESPONSE-FINITE-VALUES": str(runtime["response_finite_values"]),
        "RESPONSE-NONZERO-VALUES": str(runtime["response_nonzero_values"]),
        "PLANE1-RESPONSE-NONZERO-VALUES":
            str(runtime["response_nonzero_by_plane"][0]),
        "PLANE2-RESPONSE-NONZERO-VALUES":
            str(runtime["response_nonzero_by_plane"][1]),
        "PLANE3-RESPONSE-NONZERO-VALUES":
            str(runtime["response_nonzero_by_plane"][2]),
        "LEAKAGE-BINARY32-BIT-CHECKS":
            str(runtime["leakage_binary32_bit_checks"]),
        "TXSC-ORDERED-BINARY32-BIT-CHECKS":
            str(runtime["txsc_binary32_bit_checks"]),
        "S0PHYS-ORDERED-BINARY32-BIT-CHECKS":
            str(runtime["s0phys_binary32_bit_checks"]),
        "S0USED-ORDERED-BINARY32-BIT-CHECKS":
            str(runtime["s0used_binary32_bit_checks"]),
        "PROJECTED-SHA256": runtime["projected_sha256"],
        "PROJECTED-BYTES": str(runtime["projected_bytes"]),
        "ASSEMBLED-SHA256": runtime["assembled_sha256"],
        "ASSEMBLED-BYTES": str(runtime["assembled_bytes"]),
        "EMPIRICAL-CONTROLS": str(runtime["empirical_controls"]),
        "AUTOMATIC-RETRIES-WITHIN-ACCEPTED-RUN":
            str(runtime["automatic_retries"]),
        "DEVELOPMENT-HISTORY-PRIOR-INVALID-ACTIVATIONS":
            str(manifest["development_history"]["prior_invalid_activations"]),
        "DEVELOPMENT-HISTORY-PRIOR-ACTUAL-ASM-EXECUTIONS":
            str(manifest["development_history"]["prior_actual_asm_executions"]),
        "DEVELOPMENT-HISTORY-INVALID-RUNS-USED-AS-SCIENTIFIC-EVIDENCE":
            str(manifest["development_history"]
                ["invalid_runs_used_as_scientific_evidence"]),
    }
    for key, value in expected.items():
        require(fields.get(key) == value,
                f"runtime-result/manifest mismatch: {key}")
    require(fields.get("CLAIM") ==
            "REAL-ASM-PLANES1-3-EXECUTED-AND-SPOR64K-ASSEMBLED1-"
            "COMMITTED-AND-B2K-POSTERIOR-COMPATIBLE",
            "accepted runtime-result claim differs")
    require(fields.get("RADIAL-FLUX-SOLVE") == "NOT-EXECUTED" and
            fields.get("RADIAL-CONVERGENCE") == "NOT-EVALUATED" and
            fields.get("OUTER-PICARD-CONVERGENCE") == "NOT-EVALUATED",
            "accepted runtime-result convergence boundary differs")


def check_all() -> None:
    for path in (
        DECK, POSTERIOR, BOUNDED, RUNNER, HOST, B2K, ASM, ASMDRV,
        KDRDPR, CLE2000,
        README, MANIFEST, RUNTIME_RESULT, CONTRACT_TESTS, BOUNDED_TESTS,
    ):
        require(path.is_file(), f"missing {path}")
    check_deck(DECK.read_text(encoding="utf-8"))
    check_host(HOST.read_text(encoding="utf-8"))
    check_production(
        ASM.read_text(encoding="utf-8"), ASMDRV.read_text(encoding="utf-8")
    )
    check_loader(
        KDRDPR.read_text(encoding="utf-8"),
        CLE2000.read_text(encoding="utf-8"),
    )
    check_b2k(B2K.read_text(encoding="utf-8"))
    check_posterior(POSTERIOR.read_text(encoding="utf-8"))
    check_bounded(BOUNDED.read_text(encoding="utf-8"))
    check_runner(RUNNER.read_text(encoding="utf-8"))
    check_assets(
        README.read_text(encoding="utf-8"),
        MANIFEST.read_text(encoding="utf-8"),
    )
    check_runtime_result(
        RUNTIME_RESULT.read_text(encoding="utf-8"),
        MANIFEST.read_text(encoding="utf-8"),
    )


def main() -> None:
    check_all()
    print("B2M STATIC CONTRACT PASS")
    print("B2M DEFAULT-DRAGON=0 ACTIVE-DRAGON-MAX=1 ASM-MAX=3 SPOR64K-MAX=1")
    print("B2M FLU=0 CONT=0 PICARD=0 EMPIRICAL-CONTROLS=0")


if __name__ == "__main__":
    main()

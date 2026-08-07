#!/usr/bin/env python3
"""Fail-closed static gate for the B2k fresh-SYSTEM commit boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "src/SPOR64_B2K.f90"
ASM = ROOT / "src/ASM.f"
ASMDRV = ROOT / "src/ASMDRV.f"
XDRTA2 = ROOT / "src/XDRTA2.f"
KDRDRV = ROOT / "src/KDRDRV.F"
C2M = ROOT / "data/SpotAsmR64.c2m"


class GateError(RuntimeError):
    """Raised when the narrow B2k contract is not satisfied."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def fortran_code(text: str) -> str:
    return "\n".join(line.split("!", 1)[0] for line in text.splitlines())


def c2m_code(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"\s+", "", fortran_code(text)).replace("&", "").upper()


def packed_c2m(text: str) -> str:
    return re.sub(r"\s+", "", c2m_code(text)).upper()


def subroutine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        fortran_code(text),
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def logical_function(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\blogical\s+function\s+{re.escape(name)}\s*\(.*?"
        rf"\bend\s+function\s+{re.escape(name)}\b",
        fortran_code(text),
    )
    require(match is not None, f"missing logical function {name}")
    return match.group(0)


def ordered(code: str, fragments: tuple[str, ...], owner: str) -> None:
    position = -1
    for fragment in fragments:
        found = code.find(fragment, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def check_api(text: str) -> None:
    code = packed(text)
    body = packed(subroutine(text, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE"))
    require(
        "SUBROUTINESPOR64_B2K_COMMIT_SYSTEM_ARCHIVE("
        "IPOUT,IPPROJECTED,IPSYSTEMS,STATUS)" in body,
        "B2k API must accept only fresh output, PROJECTED archive, and systems",
    )
    for token in (
        "SPOR64_B2K_ADMISSION_FAILED=1",
        "SPOR64_B2K_ARCHIVE_ASSEMBLED=2",
        "NSTATE=40",
        "NGRP=370",
        "NREG=8",
        "NSNAP=3",
        "NUNKNO=14",
        "NMAT=8",
        "NSOUT=6",
        "PROJECTED_EPOCH=1",
        "ASSEMBLED_EPOCH=1",
        "TYPE(C_PTR),INTENT(IN)::IPOUT,IPPROJECTED,IPSYSTEMS(NSNAP)",
        "STATUS=SPOR64_B2K_ADMISSION_FAILED",
        "STATUS=SPOR64_B2K_ARCHIVE_ASSEMBLED",
    ):
        require(token in code, f"frozen API/constant missing: {token}")
    for token in (
        "IF(C_ASSOCIATED(IPOUT,IPPROJECTED))RETURN",
        "IF(C_ASSOCIATED(IPOUT,IPSYSTEMS(IP)))RETURN",
        "IF(C_ASSOCIATED(IPPROJECTED,IPSYSTEMS(IP)))RETURN",
        "IF(C_ASSOCIATED(IPSYSTEMS(IP),IPSYSTEMS(IR)))RETURN",
        "IF(.NOT.EMPTY_LCM_ROOT(IPOUT))RETURN",
    ):
        require(token in body, f"pointer/freshness admission missing: {token}")


def check_lifecycle(text: str) -> None:
    code = packed(text)
    body = packed(subroutine(text, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE"))
    for token in (
        "PROJECTED_ARCHIVE_ROOT_IS_EXACT(IPPROJECTED)",
        "CHARACTER_RECORD_MATCHES(ROOT_AUTHORITY,'STATE',3,12,'PROJECTED')",
        "IF(ROOT_PLANES/=NSNAP.OR.ROOT_EPOCH/=PROJECTED_EPOCH)RETURN",
        "CANDIDATE_SYSTEM_ROOT_IS_EXACT(IPSYSTEMS(IP))",
        "ABSENT_RECORD(IPSYSTEMS(IP),'SPOT-R64')",
        "ABSENT_RECORD(IPSYSTEMS(IP),'B2I-SENT')",
        "ABSENT_RECORD(IPSYSTEMS(IP),'B2I-DEEP')",
        "PROJECTED_PLANE_IS_EXACT(INPUT_FLUX(IP),RHO64,",
        "STAGED_SYSTEM_ROOT_IS_EXACT(STAGED_SYSTEM(IP))",
        "SYSTEM_AUTHORITY_IS_COMMITTED(STAGED_SYSTEM(IP),",
        "CALLLCMPTC(STAGED_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
        "CALLLCMPUT(STAGED_AUTHORITY,'EPOCH',1,1,ASSEMBLED_EPOCH)",
        "CALLLCMPTC(ROOT_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
        "CALLLCMPUT(ROOT_AUTHORITY,'EPOCH',1,1,ASSEMBLED_EPOCH)",
    ):
        require(token in body, f"lifecycle condition missing: {token}")
    require("LCMLID(IPOUT,'SYSTEM',NSNAP)" in body,
            "ASSEMBLED archive must contain the fresh SYSTEM list")
    require("CALLLCMEQU(INPUT_FLUX(IP),OUTPUT_ITEM)" in body,
            "PROJECTED plane FLUX must be copied without relabeling")
    require(
        "CHARACTER_RECORD_MATCHES(AUTHORITY,'STATE',3,12,'PROJECTED')"
        in code,
        "plane FLUX authority must remain PROJECTED",
    )
    for fn, count in (("CANDIDATE_SYSTEM_ROOT_IS_EXACT", 7),
                      ("STAGED_SYSTEM_ROOT_IS_EXACT", 8)):
        fn_code = packed(logical_function(text, fn))
        require(f"NAMES({count})" in fn_code, f"{fn} inventory size")
        require("SPOT-R64" not in fn_code if count == 7 else
                "SPOT-R64" in fn_code, f"{fn} SPOT-R64 boundary")


def check_frozen_context(text: str) -> None:
    code = packed(text)
    body = packed(subroutine(text, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE"))
    for token in (
        "TRACK_STATE_EXPECTED(NSTATE)=[NREG,NUNKNO,1,NMAT,6,1,4,0,0,0,"
        "48,1,-1,4,1,2,165,100000,11364,96,96,1,1,0,0,0,0,0,0,0,0,0,"
        "0,0,0,0,0,0,0,0]",
        "MCCG_STATE_EXPECTED(NSTATE)=[-1,4,10,0,17,32,80,0,0,4,0,0,20,"
        "1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]",
        "MACRO_STATE_EXPECTED(NSTATE)=[NGRP,NMAT,3,NIFIS,18,2,6,0,0,0,0,"
        "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]",
        "MCCG_EPSI_BITS=INT(Z'3727C5AC',INT32)",
        "IF(ANY(TRACK_STATE/=TRACK_STATE_EXPECTED))RETURN",
        "RECORD_MATCHES(INPUT_TRACK(IP),'MCCG-STATE',NSTATE,1)",
        "IF(ANY(MCCG_STATE/=MCCG_STATE_EXPECTED))RETURN",
        "RECORD_MATCHES(INPUT_TRACK(IP),'REAL-PARAM',4,2)",
        "TRANSFER(REAL_PARAM32(1),0_INT32)/=MCCG_EPSI_BITS",
        "IF(ANY(MACRO_STATE/=MACRO_STATE_EXPECTED))RETURN",
        "IF(ANY(ABS(AUTHORITY64)>REAL32_MAX64))RETURN",
        "RECORD_MATCHES(INPUT_TRACK(IP),'V$MCCG',NUNKNO,2)",
        "RECORD_MATCHES(INPUT_TRACK(IP),'MATCOD',NREG,1)",
        "RECORD_MATCHES(INPUT_TRACK(IP),'NZON$MCCG',NUNKNO,1)",
        "RECORD_MATCHES(INPUT_TRACK(IP),'KEYCUR$MCCG',NSOUT,1)",
        "IF(ANY(NZON(1:NREG)/=MATCOD))RETURN",
        "IF(ANY(NZON(NREG+1:NUNKNO)<-NSOUT))RETURN",
        "IF(ANY(NZON(NREG+1:NUNKNO)>-1))RETURN",
        "IF(VOLUME_BITS/=TRACK_VOLUME_BITS)RETURN",
        "IF(SEEN_UNKNOWN(KEYCUR(IR)))RETURN",
        "IF(.NOT.ALL(SEEN_UNKNOWN))RETURN",
    ):
        require(token in code or token in body,
                f"frozen real ASM context missing: {token}")
    # MCCGA consumes these positions; they may not be reduced to broad ranges.
    mccg = re.search(
        r"MCCG_STATE_EXPECTED\(NSTATE\)=\[(.*?)\]", code, re.S
    )
    require(mccg is not None, "MCCG frozen vector missing")
    values = [int(x) for x in mccg.group(1).split(",")]
    require(len(values) == 40, "MCCG frozen vector length")
    require(values[10] == 0 and values[13] == 1 and values[16] == 0,
            "MCCG positions 11, 14, and 17 must be frozen")


def check_system_formula(text: str) -> None:
    body = packed(logical_function(text, "SYSTEM_PAYLOAD_IS_VALID"))
    for token in (
        "RECORD_MATCHES(MACRO_GROUP,'NTOT0',NMAT,2)",
        "RECORD_MATCHES(MACRO_GROUP,'SIGW00',NMAT,2)",
        "CALLLCMLEN(MACRO_GROUP,'TRANC',ILONG,ITYLCM)",
        "IF(ILONG/=NMAT.OR.ITYLCM/=2)RETURN",
        "CALLLCMGET(MACRO_GROUP,'TRANC',TRANC32)",
        "CALLLCMGET(SYSTEM_GROUP,'DRAGON-TXSC',TX32)",
        "CALLLCMGET(SYSTEM_GROUP,'SPOT-S0-PHYS',SPHYS32)",
        "CALLLCMGET(SYSTEM_GROUP,'DRAGON-S0XSC',SUSED32)",
        "SAME_REAL32_BITS(TX32,EXPECTED_TX32)",
        "SAME_REAL32_BITS(SPHYS32,EXPECTED_SPHYS32)",
        "SAME_REAL32_BITS(SUSED32,EXPECTED_SUSED32)",
    ):
        require(token in body, f"ASM posterior check missing: {token}")
    ordered(
        body,
        (
            "EXPECTED_TX32=+0.0_REAL32",
            "EXPECTED_SPHYS32=+0.0_REAL32",
            "EXPECTED_SUSED32=+0.0_REAL32",
            "EXPECTED_SUSED32(0)=EXPECTED_SPHYS32(0)-LEAKAGE(IG)",
            "DOIM=1,NMAT",
            "EXPECTED_TX32(IM)=NTOT32(IM)",
            "EXPECTED_SPHYS32(IM)=SIGW32(IM)",
            "EXPECTED_TX32(IM)=EXPECTED_TX32(IM)-TRANC32(IM)",
            "EXPECTED_SPHYS32(IM)=EXPECTED_SPHYS32(IM)-TRANC32(IM)",
            "EXPECTED_SUSED32(IM)=EXPECTED_SPHYS32(IM)-LEAKAGE(IG)",
        ),
        "strict two-step binary32 ASM formula",
    )
    for forbidden in (
        "SIGW32(IM)-(TRANC32(IM)+LEAKAGE(IG))",
        "SIGW32(IM)-TRANC32(IM)-LEAKAGE(IG)",
        "REAL(SIGW32(IM),REAL64)",
    ):
        require(forbidden not in body, f"reassociated/promoted formula: {forbidden}")


def check_response_schema(text: str) -> None:
    body = packed(logical_function(text, "RESPONSE_GROUP_IS_EXACT"))
    for name in (
        "DIAGF$MCCG", "CF$MCCG", "ILUDF$MCCG", "CQ$MCCG",
        "DIAGQ$MCCG", "PJJ$MCCG", "PJJX$MCCG", "PJJY$MCCG",
        "PJJZ$MCCG", "PJJXI$MCCG", "PJJYI$MCCG", "PJJZI$MCCG",
        "DRAGON-TXSC", "SPOT-S0-PHYS", "DRAGON-S0XSC",
    ):
        require(name in body, f"exact response record missing: {name}")
    for name in (
        "DIAGF$MCCG", "CF$MCCG", "ILUDF$MCCG", "CQ$MCCG",
        "DIAGQ$MCCG", "PJJ$MCCG", "PJJX$MCCG", "PJJY$MCCG",
        "PJJZ$MCCG", "PJJXI$MCCG", "PJJYI$MCCG", "PJJZI$MCCG",
    ):
        require(body.count(name) >= 2,
                f"response inventory/length table disagree: {name}")
    require("NAMES(15)" in body, "response inventory must have exactly 15 records")
    require("RESPONSE_LENGTHS(12)=[32,14,32,14,8,8,8,8,8,8,8,14]" in body,
            "ACA/PJJ response lengths differ")
    require("EXACT_INVENTORY(GROUP,NAMES)" in body,
            "response group must reject extra or missing records")
    require("ABSENT_RECORD(GROUP,'FUNKNO$USS')" in body,
            "pre-solve SYSTEM must exclude FUNKNO$USS")


def check_transaction(text: str) -> None:
    body = packed(subroutine(text, "SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE"))
    require(body.count("CALLOPEN_STAGE(STAGED_SYSTEM(IP),IP)") == 1,
            "one all-plane staging loop required")
    require(body.count("CALLLCMEQU(IPSYSTEMS(IP),STAGED_SYSTEM(IP))") == 1,
            "complete candidate SYSTEM must be copied to private stage")
    require(body.count("CALLLCMEQU(STAGED_SYSTEM(IP),OUTPUT_ITEM)") == 1,
            "complete staged SYSTEM must be copied to output")
    preflight = body.index("SYSTEM_PAYLOAD_IS_VALID(IPSYSTEMS(IP)")
    first_stage = body.index("CALLOPEN_STAGE(STAGED_SYSTEM(IP),IP)")
    require(preflight < first_stage, "all candidate preflight must precede staging")
    first_output = body.index("CALLLCMPTC(IPOUT,'SIGNATURE',12,SIGNATURE)")
    require(first_stage < first_output, "private SYSTEM staging must precede output")
    before_output = body[:first_output]
    for mutation in (
        "CALLLCMPUT(IPOUT", "CALLLCMPTC(IPOUT", "LCMLID(IPOUT",
        "LCMDID(IPOUT", "LCMDIL(IPOUT",
    ):
        require(mutation not in before_output,
                f"caller output mutated before all stages: {mutation}")
    require(body.count("IF(.NOT.EMPTY_LCM_ROOT(IPOUT))") == 2,
            "output freshness must be checked at entry and before commit")
    for token in (
        "CALLLCMEQU(INPUT_TRACK(IP),OUTPUT_ITEM)",
        "CALLLCMEQU(INPUT_LIBRARY(IP),OUTPUT_ITEM)",
        "CALLLCMEQU(STAGED_SYSTEM(IP),OUTPUT_ITEM)",
        "CALLLCMEQU(INPUT_FLUX(IP),OUTPUT_ITEM)",
    ):
        require(token in body, f"archive deep copy missing: {token}")
    ordered(
        body,
        (
            "CALLLCMEQU(STAGED_SYSTEM(IP),OUTPUT_ITEM)",
            "CALLCLOSE_STAGES(STAGED_SYSTEM)",
            "ROOT_AUTHORITY=LCMDID(IPOUT,'SPOT-R64')",
            "CALLLCMPUT(ROOT_AUTHORITY,'RHO',1,4,RHO64)",
            "CALLLCMPUT(ROOT_AUTHORITY,'NPLANE',1,1,ROOT_PLANES)",
            "CALLLCMPTC(ROOT_AUTHORITY,'STATE',12,LIFECYCLE_STATE)",
            "CALLLCMPUT(ROOT_AUTHORITY,'EPOCH',1,1,ASSEMBLED_EPOCH)",
            "STATUS=SPOR64_B2K_ARCHIVE_ASSEMBLED",
        ),
        "archive-wide commit order",
    )
    mutations = list(re.finditer(
        r"CALLLCM(?:EQU|PUT|PTC|PDL|DEL)\(|=LCM(?:DID|LID|DIL)\(", body
    ))
    require(mutations, "B2k output publication has no LCM mutation")
    last = mutations[-1].start()
    require(body.startswith(
        "CALLLCMPUT(ROOT_AUTHORITY,'EPOCH',1,1,ASSEMBLED_EPOCH)", last
    ), "archive root EPOCH must be the final LCM mutation")
    require("LCMPUT(OUTPUT_ITEM,'DRAGON-" not in body,
            "minimal SYSTEM rewriting is forbidden")


def check_wrapper(text: str) -> None:
    body = packed(subroutine(text, "SPOR64K"))
    for token in (
        "IF(NENTRY/=5)CALLXABORT",
        "IF(HENTRY(1)/='ASSEMBLED')",
        "IF(HENTRY(2)/='PROJECTED')",
        "HENTRY(3)/='SYSTEM1'",
        "HENTRY(4)/='SYSTEM2'",
        "HENTRY(5)/='SYSTEM3'",
        "IF(JENTRY(1)/=0.OR.ANY(JENTRY(2:5)/=2))",
        "CALLREDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)",
        "IF(INDIC/=3.OR.TEXT4/=';')",
        "SYSTEMS=KENTRY(3:5)",
        "CALLSPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(KENTRY(1),KENTRY(2),SYSTEMS,STATUS)",
    ):
        require(token in body, f"CLE wrapper contract missing: {token}")


def check_forbidden_paths(text: str) -> None:
    code = fortran_code(text)
    stripped = re.sub(r"'[^']*'|\"[^\"]*\"", " ", code)
    identifiers = re.findall(r"(?i)\b[A-Z][A-Z0-9_]*\b", stripped)
    for identifier in identifiers:
        for stem in ("alpha", "omega", "relax", "damp", "clip", "empir",
                     "anderson", "aitken"):
            require(stem not in identifier.lower(),
                    f"empirical control forbidden: {identifier}")
    identifier_set = {identifier.upper() for identifier in identifiers}
    for forbidden in (
        "ASM", "ASMDRV", "DOORAV", "DOORPV", "DRAGON", "FLUDRV",
        "FLU2DR", "MCCGF", "MCGMRE", "SPOMOC", "SPOFSRC", "CONT",
        "QFISS", "MATMUL",
    ):
        require(forbidden not in identifier_set,
                f"solver/source path forbidden in B2k commit: {forbidden}")


def check_host_wiring(*, c2m_text: str | None = None,
                      kdr_text: str | None = None,
                      asm_text: str | None = None,
                      asmdrv_text: str | None = None,
                      xdrta2_text: str | None = None) -> None:
    if c2m_text is None:
        c2m_text = C2M.read_text()
    c2m = packed_c2m(c2m_text)
    require(
        "LINKED_LISTMICROLIB2MACRO0TRACKSYSTEM1SYSTEM2SYSTEM3;" in c2m,
        "candidate procedure LCM declarations differ",
    )
    require("MODULERECOVER:ASM:SPOR64K:DELETE:END:;" in c2m,
            "candidate procedure module declarations differ")
    require(c2m.count(":=ASM:") == 3, "candidate procedure needs three ASM calls")
    for plane in (1, 2, 3):
        block = (
            f"MICROLIB2:=RECOVER:PROJECTED::ITEM{plane};"
            "MACRO0:=MICROLIB2;"
            "MICROLIB2:=DELETE:MICROLIB2;"
            f"TRACK:=RECOVER:PROJECTED::ITEM{plane};"
            f"SYSTEM{plane}:=ASM:MACRO0TRACKTRACK_FPROJECTED::"
            f"EDIT0ARMLK1D{plane};"
            "MACRO0TRACK:=DELETE:MACRO0TRACK;"
        )
        require(block in c2m,
                f"same-index MACRO0/TRACK/ASM/LK1D block differs: plane {plane}")
    require(
        "ASSEMBLED:=SPOR64K:PROJECTEDSYSTEM1SYSTEM2SYSTEM3::;" in c2m,
        "three fresh systems must enter SPOR64K in order",
    )
    for forbidden in ("FLU:", "CONT", "QFISS", "SPOFSRC"):
        require(forbidden not in c2m, f"candidate assembly procedure overreaches: {forbidden}")

    for suffix in ("*.c2m", "*.x2m"):
        for path in (ROOT / "data").rglob(suffix):
            if path.resolve() == C2M.resolve():
                continue
            other = c2m_code(path.read_text(errors="replace")).upper()
            require("SPOR64K:" not in other and "SPOTASMR64" not in other,
                    f"B2k candidate must remain unselected: {path.relative_to(ROOT)}")

    if kdr_text is None:
        kdr_text = KDRDRV.read_text()
    kdr = packed(kdr_text)
    require(
        "ELSEIF(HMODUL.EQ.'SPOR64K:')THENCALLSPOR64K("
        "NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)" in kdr,
        "KDRDRV SPOR64K dispatcher registration missing",
    )
    if asm_text is None:
        asm_text = ASM.read_text()
    asm = packed(asm_text)
    require("CALLXDRTA2" in asm, "ASM XDRTA2 call missing")
    require("CALLXDRTA2(" not in asm,
            "ASM must honor the frozen zero-argument XDRTA2 ABI")

    if xdrta2_text is None:
        xdrta2_text = XDRTA2.read_text()
    definitions = re.findall(
        r"(?im)^[ \t]*SUBROUTINE[ \t]+XDRTA2[^\r\n]*$", xdrta2_text
    )
    require(len(definitions) == 1, "XDRTA2 must have one visible definition")
    require(re.fullmatch(
        r"[ \t]*SUBROUTINE[ \t]+XDRTA2[ \t]*", definitions[0], re.I
    ) is not None, "XDRTA2 definition must have the frozen zero-argument ABI")

    if asmdrv_text is None:
        asmdrv_text = ASMDRV.read_text()
    asmdrv = packed(asmdrv_text)
    for token in (
        "CALLLCMGET(KPSNAP,'SPOT-LEAK1D',LEAK1D)",
        "CALLLCMPUT(IPSYS,'SPOT-LEAK1D',NGROUP,2,LEAK1D)",
        "XSSIGT(IMAT,IGR,1)=XSSIGT(IMAT,IGR,1)-XSSCOR(IMAT,IGR)",
        "XSSIGW(IMAT,1,IGR)=XSSIGW(IMAT,1,IGR)-XSSCOR(IMAT,IGR)",
        "S0PHYS(0:NBMIX,IGR)=XSSIGW(0:NBMIX,1,IGR)",
        "XSSIGW(0:NBMIX,1,IGR)=S0PHYS(0:NBMIX,IGR)-LEAK1D(IGR)",
        "CALLLCMPUT(KPSYS,'SPOT-S0-PHYS',NBMIX+1,2,",
    ):
        require(token in asmdrv, f"real ASM formula boundary missing: {token}")


def check_validation_assets() -> None:
    readme = (HERE / "README.md").read_text()
    manifest = json.loads((HERE / "precision_manifest.json").read_text())
    support = (HERE / "b2k_fixture_support.f90").read_text()
    harness = (HERE / "test_b2k_system_assembly.f90").read_text()
    c2m_helper = (HERE / "compile_c2m.c").read_text()
    runner = (HERE / "run_phase_a9b_b2k_system_assembly.sh").read_text()
    tests = (HERE / "test_phase_a9b_b2k_system_assembly_contract.py").read_text()

    for claim in (
        "seven root entries", "after commit", "REAL-ASM-EXECUTION=NOT-EVALUATED",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
    ):
        require(claim in readme, f"phase boundary documentation missing: {claim}")
    require(manifest["phase"] == "A9b-B2k", "manifest phase")
    require(manifest["candidate_system"]["candidate_root_entries"] == 7,
            "manifest exact candidate root")
    require(manifest["candidate_system"]["committed_root_entries"] == 8,
            "manifest exact committed root")
    require(manifest["semantic_boundary"]["real_asm_execution_evaluated"] is False,
            "manifest must not claim real ASM execution")
    require(manifest["semantic_boundary"]
            ["radial_system_schema_and_xs_identities_validated"] is True,
            "manifest system schema/XS identity claim")
    require(manifest["semantic_boundary"]
            ["radial_response_numerics_evaluated"] is False,
            "synthetic responses cannot validate response numerics")
    require(manifest["semantic_boundary"]["cont_executed"] is False,
            "manifest CONT boundary")

    support_code = packed(support)
    for token in (
        "CALLB2J_BUILD_CLOSED_PAIR",
        "CALLRESTORE_REAL_MACROLIB_XS",
        "CALLSPOR64_B2J_PROJECT_ARCHIVE",
        "CALLB2J_REQUIRE_ABSENT(PROJECTED,'SYSTEM')",
        "TXSC(IM)=NTOT0(IM)-TRANC(IM)",
        "S0PHYS(IM)=SIGW00(IM)-TRANC(IM)",
        "S0USED(IM)=S0PHYS(IM)-LEAKAGE32",
        "S0USED(0)=S0PHYS(0)-LEAKAGE32",
        "B2K_VERIFY_POST_COMMIT_INDEPENDENCE",
    ):
        require(token in support_code, f"fixture contract missing: {token}")
    build_one = packed(subroutine(support, "BUILD_ONE_FRESH_SYSTEM"))
    require("LCMEQU(" not in build_one,
            "fresh synthetic SYSTEM must not copy the lagged SYSTEM")
    require("B2K-SENT" not in support_code and "B2K-DEEP" not in support_code,
            "validation-only SYSTEM root sentinels are forbidden")
    for bits in ("3D000000", "3C000000", "3C000001", "3C7FFFFF", "3C800000"):
        require(bits in support_code, f"rounding witness bit missing: {bits}")

    harness_code = packed(harness)
    for token in (
        "NREJECTION=20",
        "MCCG_STATE(11)=1",
        "MCCG_STATE(14)=0",
        "MCCG_STATE(17)=1",
        "2.0_REAL64*REAL(HUGE(0.0_REAL32),REAL64)",
        "CALLLCMPUT(ITEM,'MATCOD',B2J_NREG,1,MATCOD)",
        "CALLLCMPUT(ITEM,'V$MCCG',B2J_NUNKNO,2,VOLUME_TRACK32)",
        "IF(POST_COMMIT_WITNESSES/=B2K_NGROUP_RECORDS)",
        "B2J_REQUIRE_ABSENT(SYSTEMS(IP),'SPOT-R64')",
    ):
        require(token in harness_code, f"dynamic mutation/claim missing: {token}")

    test_count = len(re.findall(r"(?m)^\s+def\s+test_[A-Za-z0-9_]+\(", tests))
    require(test_count == manifest["validation"]["static_contract_tests"],
            "manifest static test inventory")
    require(
        f"STATIC-CONTRACT-TESTS={test_count} "
        f"MUTATION-REGRESSION-CASES={test_count-1}" in runner,
        "runner mutation inventory",
    )
    for token in (
        "-ffp-contract=off -fno-fast-math",
        "FIXED_FLAGS='-O0 -g -std=legacy -ffixed-line-length-none -cpp'",
        "copy_exact \"$ROOT/src/ASM.f\" \"$SOURCE_DIR/ASM.f\"",
        "copy_exact \"$ROOT/src/XDRTA2.f\" \"$SOURCE_DIR/XDRTA2.f\"",
        "copy_exact \"$ROOT/src/KDRDRV.F\" \"$SOURCE_DIR/KDRDRV.F\"",
        "count_exact 1 ' U _xdrta2_$'",
        "count_exact 1 ' T _xdrta2_$'",
        "count_exact 1 ' U _spor64k_$'",
        "HOST-OBJECT-COMPILE=ASM+XDRTA2+KDRDRV+B2K XDRTA2-ABI=ZERO-ARGUMENT",
        "DRAGON-EXECUTIONS=0 ASM-EXECUTIONS=0 TRANSPORT-SOLVES=0",
        "REAL-ASM-EXECUTION=NOT-EVALUATED",
        "QFISS=NOT-BUILT CONT=NOT-EXECUTED",
        "C2M-COMPILE=CLEPIL+OBJPIL C2M-EXECUTION=NOT-EVALUATED",
    ):
        require(token in runner, f"runner boundary claim missing: {token}")
    for token in (
        "clepil(input, stdout, object, clecst)",
        "objpil(object, stdout, 0)",
        "kdicl_c(object, rc == 0 ? 1 : 2)",
    ):
        require(token in c2m_helper, f"C2M compiler helper missing: {token}")
    for token in (
        '"$CC" -std=c11 -pedantic -Wall -Wextra -Werror',
        './compile_c2m "$ROOT/data/SpotAsmR64.c2m" SpotAsmR64.o2m',
        '[ -s "$BUILD_DIR/SpotAsmR64.o2m" ]',
    ):
        require(token in runner, f"C2M compile gate missing: {token}")

    makefile = (ROOT / "Makefile").read_text()
    root_readme = (ROOT / "README.md").read_text()
    require("spot-real64-phase-a9b-b2k-system-assembly" in makefile,
            "B2k Makefile target missing")
    require("make spot-real64-phase-a9b-b2k-system-assembly" in root_readme,
            "root README B2k command missing")
    require("real64_phase_a9b_b2k_system_assembly/README.md" in root_readme,
            "root README B2k phase link missing")


def check_source(text: str) -> None:
    check_api(text)
    check_lifecycle(text)
    check_frozen_context(text)
    check_system_formula(text)
    check_response_schema(text)
    check_transaction(text)
    check_wrapper(text)
    check_forbidden_paths(text)


def check_all() -> None:
    check_source(SOURCE.read_text())
    check_host_wiring()
    check_validation_assets()


def main() -> None:
    check_all()
    print("B2K STATIC CONTRACT PASS")
    print("B2K REAL-ASM-WIRED=true REAL-ASM-EXECUTION=NOT-EVALUATED")
    print("B2K EMPIRICAL-CONTROLS=0 QFISS=false CONT=false")


if __name__ == "__main__":
    main()

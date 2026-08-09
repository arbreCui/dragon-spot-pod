#!/usr/bin/env python3
"""Fail-closed static contract for the B2x same-call close route."""

from __future__ import annotations

import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HOST = ROOT / "data/SpotCloseR64.c2m"
ADAPTER = ROOT / "src/SPOR64_B2X.f90"
KDRDRV = ROOT / "src/KDRDRV.F"
FLU2DR = ROOT / "src/FLU2DR.f"
B2W = ROOT / "src/SPOR64_B2W.f90"
README = HERE / "README.md"
MANIFEST = HERE / "precision_manifest.json"


class GateError(AssertionError):
    """The narrow B2x contract was violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def strip_fortran_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("!"):
            continue
        if line and line[0] in "cC*":
            continue
        if (len(line) >= 6 and line[:5].isspace()
                and line[5] not in {" ", "0"}):
            line = line[6:]
        lines.append(line.split("!", 1)[0])
    return "\n".join(lines)


def strip_deck_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("*")
    )


def packed(text: str) -> str:
    return re.sub(r"[\s&]+", "", text).upper()


def routine(text: str, name: str) -> str:
    match = re.search(
        rf"(?is)\bsubroutine\s+{re.escape(name)}\b.*?"
        rf"\bend\s+subroutine\s+{re.escape(name)}\b",
        strip_fortran_comments(text),
    )
    require(match is not None, f"missing subroutine {name}")
    return match.group(0)


def require_order(owner: str, text: str, fragments: tuple[str, ...]) -> None:
    code = packed(text)
    position = -1
    for fragment in fragments:
        needle = packed(fragment)
        found = code.find(needle, position + 1)
        require(found > position, f"{owner}: missing or reordered {fragment}")
        position = found


def check_host(text: str) -> None:
    code = packed(strip_deck_comments(text))
    require(
        "PARAMETERAX_CLOSEDARCH_CLOSEDRETURNEDTRACK_AXMACROLIB3BASIS_REF::"
        ":::LINKED_LISTAX_CLOSEDARCH_CLOSEDRETURNEDTRACK_AX"
        "MACROLIB3BASIS_REF;;" in code,
        "SpotCloseR64 formal media contract differs",
    )
    require(
        "LINKED_LISTFEEDBACKSYSTEM_NEXTAX_NEXT;" in code,
        "SpotCloseR64 private-object inventory differs",
    )
    require(
        "MODULESPOR64V:ASM:FLU:SPOSTATE:SPOLEAK:SPOR64X:DELETE:END:;"
        in code,
        "SpotCloseR64 module allowlist differs",
    )
    for call in ("ASM", "FLU", "SPOSTATE", "SPOLEAK", "SPOR64X"):
        require(code.count(f":={call}:") == 1,
                f"SpotCloseR64 must contain exactly one {call} call")
    require(code.count("FEEDBACK:=RETURNED;") == 1,
            "RETURNED must be copied exactly once")
    require(code.count("SPOR64V:FEEDBACK::;") == 1,
            "returned admission must occur exactly once")
    require(
        code.count(
            "SYSTEM_NEXT:=ASM:MACROLIB3TRACK_AXFEEDBACKBASIS_REF::"
            "EDIT0SPOD1FIXB;"
        ) == 1,
        "fixed rank-one ASM call differs",
    )
    require(
        code.count(
            "AX_NEXT:=FLU:MACROLIB3TRACK_AXSYSTEM_NEXT::"
            "EDIT-3TYPEKB1SIGSEXTE5002.5E-7"
            "UNKT2.5E-7THER2.5E-7;"
        ) == 1,
        "fixed axial FLU call differs",
    )
    require(
        code.count(
            "AX_NEXT:=SPOSTATE:AX_NEXTTRACK_AXSYSTEM_NEXTMACROLIB3::;"
        ) == 1,
        "SPOSTATE custody call differs",
    )
    require(
        code.count(
            "FEEDBACK:=SPOLEAK:FEEDBACKAX_NEXTTRACK_AX::>>LEAK_CHANGE<<;"
        ) == 1,
        "SPOLEAK custody call differs",
    )
    require(
        code.count(
            "AX_CLOSEDARCH_CLOSED:=SPOR64X:AX_NEXTFEEDBACK::;"
        ) == 1,
        "SPOR64X terminal call differs",
    )
    require(
        code.count(
            "FEEDBACKSYSTEM_NEXTAX_NEXT:=DELETE:"
            "FEEDBACKSYSTEM_NEXTAX_NEXT;"
        ) == 1,
        "private cleanup differs",
    )
    require_order(
        "SpotCloseR64",
        code,
        (
            "FEEDBACK:=RETURNED;",
            "SPOR64V:FEEDBACK::;",
            "SYSTEM_NEXT:=ASM:",
            "AX_NEXT:=FLU:",
            "AX_NEXT:=SPOSTATE:",
            "FEEDBACK:=SPOLEAK:",
            "AX_CLOSEDARCH_CLOSED:=SPOR64X:",
            "FEEDBACKSYSTEM_NEXTAX_NEXT:=DELETE:",
            "END:;",
        ),
    )
    require(code.count("LEAK_CHANGE") == 2,
            "leak-change diagnostic must be output-only")
    forbidden = (
        "SPOGBAL", "SPOPROJ", "SPOXCONV", "WHILE", "REPEAT",
        "RELAX", "DAMP", "CLIP", "RETRY", "ALPHA", "OMEGA",
    )
    for token in forbidden:
        require(token not in code, f"forbidden B2x host token: {token}")


def check_adapter(text: str) -> None:
    body = routine(text, "SPOR64X")
    code = packed(body)
    require(
        "SUBROUTINESPOR64X(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)" in code,
        "SPOR64X ABI differs",
    )
    required = (
        "IF(NENTRY/=4)THEN",
        "IF(HENTRY(1)/='AX_CLOSED'.OR.HENTRY(2)/='ARCH_CLOSED')THEN",
        "IF(HENTRY(3)/='AX_NEXT'.OR.HENTRY(4)/='FEEDBACK')THEN",
        "IF(ANY(IENTRY/=1))THEN",
        "IF(ANY(JENTRY(1:2)/=0).OR.ANY(JENTRY(3:4)/=2))THEN",
        "CALLREDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)",
        "IF(INDIC/=3.OR.TEXT4/=';')THEN",
        "CALLSPOR64_B2W_CLOSE(KENTRY(1),KENTRY(2),KENTRY(3),KENTRY(4),STATUS)",
        "IF(STATUS/=SPOR64_B2W_CLOSED)THEN",
    )
    for fragment in required:
        require(packed(fragment) in code, f"SPOR64X missing {fragment}")
    require(code.count("CALLREDGET(") == 1,
            "SPOR64X must consume one parser token")
    require(code.count("CALLSPOR64_B2W_CLOSE(") == 1,
            "SPOR64X must call B2W once")
    require_order(
        "SPOR64X",
        code,
        (
            "IF(NENTRY/=4)THEN",
            "IF(HENTRY(1)/='AX_CLOSED'",
            "IF(HENTRY(3)/='AX_NEXT'",
            "IF(ANY(IENTRY/=1))THEN",
            "IF(ANY(JENTRY(1:2)/=0)",
            "CALLREDGET(",
            "IF(INDIC/=3.OR.TEXT4/=';')THEN",
            "CALLSPOR64_B2W_CLOSE(",
            "IF(STATUS/=SPOR64_B2W_CLOSED)THEN",
        ),
    )
    for token in ("LCMPUT", "LCMPTC", "LCMEQU", "ASM(", "FLU(",
                  "SPOSTATE(", "SPOLEAK("):
        require(token not in code, f"SPOR64X contains forbidden action {token}")


def check_admission_adapter(text: str) -> None:
    body = routine(text, "SPOR64V")
    code = packed(body)
    required = (
        "SUBROUTINESPOR64V(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)",
        "IF(NENTRY/=1)THEN",
        "IF(HENTRY(1)/='FEEDBACK')THEN",
        "IF(IENTRY(1)/=1)THEN",
        "IF(JENTRY(1)/=2)THEN",
        "CALLREDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)",
        "IF(INDIC/=3.OR.TEXT4/=';')THEN",
        "CALLSPOR64_B2W_ADMIT_RETURNED(KENTRY(1),STATUS)",
        "IF(STATUS/=SPOR64_B2W_RETURNED_ADMITTED)THEN",
    )
    for fragment in required:
        require(packed(fragment) in code, f"SPOR64V missing {fragment}")
    require(code.count("CALLREDGET(") == 1,
            "SPOR64V must consume one parser token")
    require(code.count("CALLSPOR64_B2W_ADMIT_RETURNED(") == 1,
            "SPOR64V must call returned admission once")
    require_order(
        "SPOR64V",
        code,
        (
            "IF(NENTRY/=1)THEN",
            "IF(HENTRY(1)/='FEEDBACK')THEN",
            "IF(IENTRY(1)/=1)THEN",
            "IF(JENTRY(1)/=2)THEN",
            "CALLREDGET(",
            "IF(INDIC/=3.OR.TEXT4/=';')THEN",
            "CALLSPOR64_B2W_ADMIT_RETURNED(",
            "IF(STATUS/=SPOR64_B2W_RETURNED_ADMITTED)THEN",
        ),
    )
    for token in ("LCMPUT", "LCMPTC", "LCMEQU", "ASM(", "FLU(",
                  "SPOSTATE(", "SPOLEAK(", "SPOR64_B2W_CLOSE("):
        require(token not in code, f"SPOR64V contains forbidden action {token}")


def check_returned_admission(text: str) -> None:
    body = routine(text, "SPOR64_B2W_ADMIT_RETURNED")
    code = packed(body)
    require(
        "STATUS=SPOR64_B2W_PREFLIGHT_FAILED" in code,
        "returned admission lacks fail-closed initial status",
    )
    require(
        "IF(.NOT.RETURNED_FEEDBACK_ROOT_IS_EXACT(IPFEEDBACK))RETURN" in code,
        "returned admission root inventory differs",
    )
    identity = (
        "DOIG=1,NGRP"
        "FOUND32=TRANSFER(CHILD_LEAKAGE32(IG,IP),0_INT32)"
        "EXPECTED32=TRANSFER(SYSTEM_LEAKAGE32(IG,IP),0_INT32)"
        "IF(FOUND32/=EXPECTED32)RETURN"
        "ENDDO"
    )
    require(code.count(identity) == 1,
            "returned admission lacks elementwise child/system L0 identity")
    require(code.count("STATUS=SPOR64_B2W_RETURNED_ADMITTED") == 1,
            "returned admission success status differs")
    require_order(
        "returned admission",
        code,
        (
            "STATUS=SPOR64_B2W_PREFLIGHT_FAILED",
            "RETURNED_FEEDBACK_ROOT_IS_EXACT",
            "RETURNED_CHILD_IS_VALID",
            "RETURNED_SYSTEM_IS_VALID",
            identity,
            "STATUS=SPOR64_B2W_RETURNED_ADMITTED",
        ),
    )
    for token in (
        "LCMPUT", "LCMPTC", "LCMEQU", "LCMDID", "LCMLID", "LCMDIL",
        "LCMCL", "MAXVAL", "TOLER", "RELAX", "DAMP", "CLIP",
    ):
        require(token not in code,
                f"returned admission contains forbidden write/norm {token}")


def check_dispatcher(text: str) -> None:
    code = packed(strip_fortran_comments(text))
    branch = (
        "ELSEIF(HMODUL.EQ.'SPOR64V:')THEN"
        "CALLSPOR64V(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)"
        "ELSEIF(HMODUL.EQ.'SPOR64X:')THEN"
        "CALLSPOR64X(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)"
        "ELSEIF(HMODUL.EQ.'FLU:')THEN"
    )
    require(code.count(branch) == 1, "KDRDRV SPOR64V/SPOR64X route differs")
    require(code.count("CALLSPOR64V(") == 1,
            "KDRDRV must expose SPOR64V exactly once")
    require(code.count("CALLSPOR64X(") == 1,
            "KDRDRV must expose SPOR64X exactly once")


def check_flu2dr(text: str) -> None:
    code = packed(strip_fortran_comments(text))
    strict = (
        "IF((EEXT.LT.EPSOUT).AND.(EINN.LT.EPSUNK).AND."
        "(EINR_LAST.LT.EPSINR).AND.(IINR_STATE.EQ.1).AND."
        "(IT.GE.2))THEN"
    )
    cap_gate = (
        "IF((CXDOOR.EQ.'SPOT').AND.(ITYPEC.GE.2).AND."
        "(ITYPEC.LE.3))THEN"
    )
    abort = "CALLXABORT('FLU2DR:SPOTTYPE-KSTRICTTERMINATIONREQUIRED.')"
    require(code.count(strict) == 1,
            "FLU2DR strict success predicate differs")
    require(code.count(cap_gate) == 1,
            "FLU2DR SPOT TYPE-K cap gate differs")
    require(code.count(abort) == 1,
            "FLU2DR strict cap abort differs")
    require_order(
        "FLU2DR terminal path",
        code,
        (
            strict,
            "GOTO410",
            "400CONTINUE",
            "WRITE(6,1160)",
            "WRITE(6,1170)",
            "CONVERGENCENOTREACHED",
            cap_gate,
            abort,
            "RETURN",
            "MESSOU='*NOT*'",
            "410RKEFF=REAL(AKEFF)",
            "CALLLCMPDL(JPFLUX",
        ),
    )


def check_default_off() -> None:
    selections: list[Path] = []
    for path in (ROOT / "data").rglob("*"):
        if not path.is_file() or path == HOST:
            continue
        if path.suffix.lower() not in {".c2m", ".x2m", ".d2p", ".access"}:
            continue
        code = packed(strip_deck_comments(path.read_text(errors="replace")))
        if "SPOTCLOSER64" in code:
            selections.append(path)
    require(not selections,
            "SpotCloseR64 is selected by shipped decks: " +
            ", ".join(str(path.relative_to(ROOT)) for path in selections))


def check_metadata() -> None:
    readme = README.read_text()
    require("deployment-default-OFF" in readme,
            "README lacks default-off scope")
    require("No ASM, FLU, or SPOSTATE symbol is linked" in readme,
            "README lacks runtime link boundary")
    require("structural evidence only" in readme,
            "README lacks structural-custody nonclaim")
    require("not a numerical solve" in readme,
            "README lacks numerical nonclaim")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["phase"] == "A9b-B2x",
            "manifest phase differs")
    require(manifest["receipt"] in {"pending", "frozen"},
            "manifest receipt state differs")
    require(manifest["runtime"]["dragon"] == 0,
            "manifest Dragon count differs")
    require(manifest["runtime"]["asm"] == 0,
            "manifest ASM count differs")
    require(manifest["runtime"]["flu"] == 0,
            "manifest FLU count differs")
    require(manifest["runtime"]["spostate"] == 0,
            "manifest SPOSTATE count differs")
    require(manifest["runtime"]["spoleak"] == 1,
            "manifest SPOLEAK count differs")
    require(manifest["runtime"]["spor64v"] == 9,
            "manifest SPOR64V count differs")
    require(manifest["runtime"]["spor64x"] == 10,
            "manifest SPOR64X count differs")
    require(manifest["runtime"]["real_b2w_close"] == 2,
            "manifest B2W close count differs")


def check_all() -> None:
    check_host(HOST.read_text())
    check_adapter(ADAPTER.read_text())
    check_admission_adapter(ADAPTER.read_text())
    check_returned_admission(B2W.read_text())
    check_dispatcher(KDRDRV.read_text())
    check_flu2dr(FLU2DR.read_text())
    check_default_off()
    check_metadata()


def main() -> None:
    check_all()
    print("B2X STATIC SAME-CALL RETURNED-CLOSE PASS")
    print("B2X HOST=COPY->SPOR64V->ASM->FLU->SPOSTATE->SPOLEAK->SPOR64X")
    print("B2X ADAPTERS=V-EXACT1->ADMIT-ONCE,X-EXACT4->B2W-ONCE")
    print("B2X FLU2DR=STRICT-PREDICATE CAP-FAIL-BEFORE-LABEL410")
    print("B2X DEPLOYMENT-DEFAULT=OFF SHIPPED-SELECTIONS=0")
    print("B2X RUNTIME-PLAN=ASM0,FLU0,SPOSTATE0,SPOLEAK1,DRAGON0")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static contract for the optional parent-state axial warm start."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
DECK = ROOT / "validation/iterative/continuation_axial_warm.x2m"
BASELINE = ROOT / "validation/iterative/continuation_axial.x2m"
FLU = ROOT / "src/FLU.f"
FLUGPI = ROOT / "src/FLUGPI.f"
FLUDRV = ROOT / "src/FLUDRV.f"


def fail(message: str) -> None:
    raise SystemExit(f"AXIAL WARM CONTRACT FAIL: {message}")


text = DECK.read_text(encoding="utf-8")
compact = re.sub(r"\s+", " ", text.upper())
code = "\n".join(
    line for line in text.splitlines() if not line.lstrip().startswith("*")
)
compact_code = re.sub(r"\s+", " ", code.upper())

baseline = BASELINE.read_text(encoding="utf-8")
expected = baseline.replace("5.0E-7", "2.5E-7", 1)
expected = expected.replace(
    'ECHO "CONT-AXIAL-TOLERANCE" solver_eps ;',
    'ECHO "CONT-AXIAL-TOLERANCE" solver_eps ;\n'
    'ECHO "CONT-AXIAL-INITIAL-GUESS" "PARENT-STATE" ;',
    1,
)
expected = expected.replace(
    "GREP: END: ;",
    "GREP: UTL: END: ;",
    1,
)
expected = expected.replace(
    "SNAP := RADIAL_IN ;",
    "SNAP := RADIAL_IN ;\n"
    "AX_CURRENT := PARENT_AX ;\n"
    "AX_CURRENT := UTL: AX_CURRENT ::\n"
    "  EDIT 0\n"
    "  DEL 'SPOT-X-STATE'\n"
    "  DEL 'SPOT-X-CARR' ;",
    1,
)
expected = expected.replace(
    "AX_CURRENT := FLU: MACROLIB3 TRACK_AX SYSTEM_NEXT ::",
    "AX_CURRENT := FLU: AX_CURRENT MACROLIB3 TRACK_AX SYSTEM_NEXT ::",
    1,
)
expected_code = "\n".join(
    line for line in expected.splitlines() if not line.lstrip().startswith("*")
)
if re.sub(r"\s+", " ", expected_code.upper()).strip() != compact_code.strip():
    fail(
        "executable deck differs from cold path beyond tolerance, initial "
        "state, and removal of inherited proposal markers"
    )

flu = re.sub(r"\s+", "", FLU.read_text(encoding="utf-8").upper())
flugpi = re.sub(r"\s+", "", FLUGPI.read_text(encoding="utf-8").upper())
fludrv = re.sub(r"\s+", "", FLUDRV.read_text(encoding="utf-8").upper())
if "REC=(JENTRY(1).EQ.1)" not in flu:
    fail("FLU no longer derives recovery mode from primary-object modification")
if "IF(REC)THEN" not in flugpi or "INITFL=1" not in flugpi:
    fail("FLUGPI no longer selects the stored flux for a recovered object")
if "IF((ILINIT.EQ.0).OR.(INITFL.EQ.0))THEN" not in fludrv:
    fail("FLUDRV stored-flux preservation condition changed")

parent_copy = "AX_CURRENT := PARENT_AX ;"
warm_call = (
    "AX_CURRENT := FLU: AX_CURRENT MACROLIB3 TRACK_AX SYSTEM_NEXT ::"
)
if text.count(parent_copy) != 1:
    fail("expected exactly one parent-state copy")
if text.count(warm_call) != 1:
    fail("FLU must modify exactly the copied parent state")
if text.index(parent_copy) > text.index(warm_call):
    fail("parent state must be copied before FLU")

required = (
    "REAL SOLVER_EPS := 2.5E-7 ;",
    "TYPE K B1 SIGS EXTE 500 <<SOLVER_EPS>>",
    "UNKT <<SOLVER_EPS>> THER <<SOLVER_EPS>>",
    "AX_CURRENT := SPOGBAL:",
    "AX_CURRENT := SPOSTATE:",
    "DEL 'SPOT-X-STATE' DEL 'SPOT-X-CARR' ;",
    "AX_CURRENT := SPOXCONV: AX_CURRENT PARENT_AX :: ;",
    "SNAP := SPOLEAK: SNAP AX_CURRENT TRACK_AX :: >>LEAK_CHANGE<< ;",
    'ECHO "CONT-AXIAL-INITIAL-GUESS" "PARENT-STATE" ;',
)
for item in required:
    if item not in compact:
        fail(f"missing required contract: {item}")

for operator in ("FLU:", "SPOGBAL:", "SPOSTATE:", "SPOXCONV:", "SPOLEAK:"):
    if compact.count(operator) != 2:
        # One declaration plus one invocation is required.
        fail(f"unexpected invocation count for {operator}")

for forbidden in (
    r"\bR64\s+(?:BOOT|CONT)\b",
    r"\bALPHA\b",
    r"\bBETA\b",
    r"\bDAMP(?:ING)?\b",
    r"\bRELAX(?:ATION)?\b",
    r"\bMIXING\b",
):
    if re.search(forbidden, compact_code):
        fail(f"forbidden model or iteration control: {forbidden}")

print(
    "AXIAL WARM CONTRACT PASS: optional parent flux is only the initial "
    "iterate; TYPE-K/SPOT equation and strict 2.5e-7 terminal are unchanged"
)

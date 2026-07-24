#!/usr/bin/env python3
"""Static fail-closed contract for the frozen raw-MOC capture."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
PROTOCOL = ITERATIVE / "raw_moc_residual_protocol.json"
MANIFEST = ITERATIVE / "raw_moc_capture_implementation.sha256"

FILES = {
    "dependencies": ROOT / "src" / ".dragon_deps.mk",
    "module": ROOT / "src" / "SPOMOC.f90",
    "parser": ROOT / "src" / "FLUGPI.f",
    "flu": ROOT / "src" / "FLU.f",
    "driver": ROOT / "src" / "FLUDRV.f",
    "flu2dr": ROOT / "src" / "FLU2DR.f",
    "mccgf": ROOT / "src" / "MCCGF.f",
    "mcgmre": ROOT / "src" / "MCGMRE.f",
    "mcgfl1": ROOT / "src" / "MCGFL1.f",
    "state test": ITERATIVE / "test_raw_moc_capture_state.f90",
    "state runner": ITERATIVE / "run_raw_moc_capture_state_test.sh",
    "checker": ITERATIVE / "check_raw_moc_capture_xsm.f90",
    "fixture": ITERATIVE / "make_raw_moc_capture_fixture.f90",
    "checker runner": ITERATIVE / "run_raw_moc_capture_checker_test.sh",
    "README": ITERATIVE / "README.md",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"RAW-MOC-CAPTURE CONTRACT FAIL: {message}")


def read(name: str) -> str:
    path = FILES[name]
    require(path.is_file() and not path.is_symlink(), f"invalid {name}")
    return path.read_text(encoding="utf-8")


require(
    hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
    == "1be10a0cb9e7cb34f2cbfa7f9ef73dfb0dbf69095b417d32d97794e543b37e6c",
    "frozen protocol bytes changed",
)
protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
require(
    protocol["status"] == "FROZEN-BEFORE-IMPLEMENTATION",
    "protocol lost its pre-implementation freeze status",
)
require(
    protocol["scope"]["activation"]
    == {
        "keyword": "MOCA",
        "syntax": "MOCA <arm-code>",
        "default_arm_code": 0,
        "arm_codes": {"1": "NATIVE", "2": "STATIONARY"},
        "legacy_SPOT_IPICK": "UNCHANGED",
        "invalid_or_out_of_scope_use": "FAIL-CLOSED",
    },
    "activation contract changed",
)
require(
    protocol["classification"]
    == {
        "valid": "CAPTURE-VALID",
        "invalid": "CAPTURE-INVALID",
        "acceptance_threshold": None,
        "stage4_authorization": False,
        "stage5_authorization": False,
        "outer_convergence_evaluated": False,
    },
    "classification contract changed",
)

dependencies = read("dependencies")
module = read("module")
parser = read("parser")
flu = read("flu")
driver = read("driver")
flu2dr = read("flu2dr")
mccgf = read("mccgf")
mcgmre = read("mcgmre")
mcgfl1 = read("mcgfl1")
state_test = read("state test")
state_runner = read("state runner")
checker = read("checker")
fixture = read("fixture")
checker_runner = read("checker runner")
readme = read("README")

for object_name in ("FLU2DR", "FLUDRV", "MCCGF", "MCGFL1", "MCGMRE"):
    require(
        f"{object_name}.o: SPOMOC.o" in dependencies,
        f"build dependency for {object_name} lost",
    )

for token in (
    "IMCAUD=0",
    "CARLIR.EQ.'MOCA'",
    "DUPLICATE MOCA KEYWORD",
    "MOCA ARM 1 OR 2 EXPECTED",
):
    require(token in parser, f"FLUGPI lost {token}")
require(
    "CARLIR.EQ.'SPOT'" in parser and "IPICK=1" in parser,
    "legacy SPOT/IPICK parser path changed",
)
require(
    "MOCA REQUIRES TYPE S AND MCCG" in flu,
    "FLU does not fail closed outside TYPE S + MCCG",
)

begin_index = driver.index("CALL SPOMOC_BEGIN")
solve_index = driver.index("CALL FLU2DR")
finish_index = driver.index("CALL SPOMOC_FINISH")
require(
    begin_index < solve_index < finish_index,
    "FLUDRV audit lifetime does not bracket FLU2DR",
)
path_index = flu2dr.index("CALL SPOMOC_FLU_PATH")
context_index = flu2dr.index("CALL SPOMOC_FLU_CONTEXT")
door_index = flu2dr.index("CALL SPOMOC_DOOR_BEGIN")
doorfv_index = flu2dr.index("CALL DOORFV", context_index)
require(
    path_index < context_index < door_index < doorfv_index,
    "FLU/DOORFV context ordering changed",
)

mccgf_begin = mccgf.index("CALL SPOMOC_MCCGF_BEGIN")
first_mcgflx = mccgf.index("CALL MCGFLX")
require(
    mccgf_begin < first_mcgflx,
    "MCCGF controls are not checked before MCGFLX",
)
require(mcgmre.count("CALL MCGFL1") == 3, "MCGMRE call-role census changed")
for role in (1, 2, 3):
    require(
        f"CALL SPOMOC_SET_ROLE({role},ITER)" in mcgmre,
        f"MCGMRE role {role} is not explicit",
    )
first_primary = mcgmre.index("CALL MCGFL1")
publish = mcgmre.index("CALL SPOMOC_PUBLISH")
require(
    first_primary < publish < mcgmre.index("ERROR=0.0D0", first_primary),
    "COMPLETE publication is not immediately after first primary return",
)

capture = mcgfl1.index("CALL SPOMOC_CAPTURE")
require(
    capture > mcgfl1.index("CALL MCGFST")
    and capture > mcgfl1.index("PHIOUT(IND,II)=PHIOUT(IND,II)/V(I)")
    and capture < mcgfl1.index("CALL MCGFCA")
    and capture < mcgfl1.index("CALL MCGSCR"),
    "capture is not post-normalization and pre-ACA/SCR",
)

for token in (
    "if (arm == 0) return",
    "required_epsilon_bits",
    "MAXOUT=1 required",
    "MAXINR=740 required",
    "ACCE 1 0 required",
    "direct vector DOORFV path required",
    "all groups must remain active",
    "primary tuple overwrite attempted",
    "audit was not published COMPLETE",
    "state_vector(2) = 1",
):
    require(token in module, f"production helper lost {token}")
require(
    module.index("if (arm == 0) return") < module.index("LCMDID"),
    "default OFF can create an audit directory",
)
for record in (
    "STATE-VECTOR",
    "NGIND",
    "GROUP",
    "SPOT-M-QFR",
    "SPOT-M-EVAL",
    "SPOT-M-SRC",
    "SPOT-M-RAW",
    "SPOT-M-STEP",
    "SPOT-M-ROLE",
    "SPOT-M-GROUP",
):
    require(record in module, f"production schema lost {record}")
require("LCMGET" not in module.upper(), "helper reads an audit value back")
require(
    re.search(
        r"\bcall\s+(DOORFV|MCGFCS|MCGSIG|MCGFCF|MOCFCF|MCGFST|"
        r"MCGFCA|MCGSCR|FLUBAL|FLU2AC)\b",
        module,
        re.IGNORECASE,
    )
    is None,
    "capture helper calls a solver or transport routine",
)
require(
    re.search(
        r"\b(relax(?:ation)?|damp(?:ing)?|alpha|omega|fitt?(?:ed|ing)?|"
        r"clip(?:ping)?|flux[ _-]?floor)\b",
        module,
        re.IGNORECASE,
    )
    is None,
    "capture helper introduced empirical machinery",
)

for token in (
    "RAW-MOC-STATE OFF PASS",
    "RAW-MOC-STATE VALID PASS",
    "partial-publish",
    "wrong-step",
    "overwrite",
):
    require(token in state_test or token in state_runner, f"state gate lost {token}")
require("Dragon" not in state_runner, "state test invokes Dragon")

require(
    re.search(
        r"\b(LCMPUT|LCMPTC|LCMPPD|LCMDID|LCMLID|LCMDIL|LCMLIL|"
        r"LCMDEL|LCMEQU)\b",
        checker,
        re.IGNORECASE,
    )
    is None,
    "independent checker contains LCM mutation",
)
require(
    re.search(r"\buse\s+SPOMOC_AUDIT\b", checker, re.IGNORECASE) is None,
    "independent checker imports the production helper",
)
require(
    re.search(
        r"\bcall\s+(DOORFV|MCCGF|MCGFLX|MCGMRE|MCGFL1|MCGFCS|MCGSIG|"
        r"MCGFCF|MOCFCF)\b",
        checker,
        re.IGNORECASE,
    )
    is None,
    "independent checker calls a production solver",
)
for token in (
    "compare_table(frozen, off, 0, .false.)",
    "compare_table(off, on, 0, .true.)",
    "EVAL differs from frozen PRE input",
    "volume source replay differs",
    "boundary source replay differs",
    "SCALAR-RELATIVE-TWO-NORM",
    "SCALAR-INPUT-NORMALIZED-MAX",
    "MAX-TIE",
    "CURRENT",
    "CAPTURE-VALID",
    "OUTER-CONVERGENCE NOT-EVALUATED",
    "STAGE4 NOT-AUTHORIZED",
):
    require(token in checker, f"independent checker lost {token}")
require(
    "product32 = system%s0(mix, group) * eval32(key)" in checker
    and "sum32 = qfr32(key) + product32" in checker,
    "checker no longer stages MCGFCS binary32 arithmetic",
)
require(
    "albedo_slot = -layout%nzon(nr + surface)" in checker
    and "if (system%nalbedo > 0) then" in checker
    and "layout%icode(albedo_slot)" in checker,
    "checker no longer replays the MCGSIG/MCGFCS boundary path",
)
require("Dragon" not in checker_runner, "checker test invokes Dragon")
for token in (
    "status extra non-audit eval source boundary surface-map icode raw",
    '"$WORK/make_fixture" "$WORK/track" 1 track',
    "RAW one-bit change did not alter the scientific receipt",
    "inputs_before.sha256",
    "inputs_after.sha256",
    "checker object references production solver symbols",
    "positive ICODE exceeds group ALBEDO",
):
    require(token in checker_runner, f"checker runner lost {token}")
require(
    "use SPOMOC_AUDIT" in fixture,
    "fixture does not exercise the production helper",
)
for token in (
    "`arm` and `plane` are protocol labels",
    "`COMPLETE` certifies only that the write-once record structure is complete",
    "checker-contract error",
    "corrected replay is still pending",
    "Stage 4 remains",
):
    require(token in readme, f"README lost evidence boundary: {token}")

if MANIFEST.exists():
    rows = [
        line.split()
        for line in MANIFEST.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    expected_paths = {
        "validation/iterative/raw_moc_residual_protocol.json",
        "src/.dragon_deps.mk",
        "src/SPOMOC.f90",
        "src/FLUGPI.f",
        "src/FLU.f",
        "src/FLUDRV.f",
        "src/FLU2DR.f",
        "src/MCCGF.f",
        "src/MCGMRE.f",
        "src/MCGFL1.f",
        "validation/iterative/test_raw_moc_capture_state.f90",
        "validation/iterative/run_raw_moc_capture_state_test.sh",
        "validation/iterative/check_raw_moc_capture_xsm.f90",
        "validation/iterative/make_raw_moc_capture_fixture.f90",
        "validation/iterative/run_raw_moc_capture_checker_test.sh",
        "validation/iterative/check_raw_moc_capture_contract.py",
        "validation/iterative/check_radial_floor_contract.py",
        "validation/iterative/README.md",
    }
    require(
        len(rows) == len(expected_paths)
        and all(len(row) == 2 for row in rows)
        and {row[1] for row in rows} == expected_paths
        and all(re.fullmatch(r"[0-9a-f]{64}", row[0]) for row in rows),
        "implementation manifest census differs",
    )
    for expected_hash, relative in rows:
        path = ROOT / relative
        require(
            path.is_file()
            and not path.is_symlink()
            and hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
            f"implementation hash differs for {relative}",
        )

print("RAW-MOC-CAPTURE CONTRACT PASS")

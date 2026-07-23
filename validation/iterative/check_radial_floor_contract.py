#!/usr/bin/env python3
"""Static fail-closed contract for the bounded radial-floor diagnostic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
PATHS = {
    "protocol": ITERATIVE / "radial_floor_protocol.json",
    "reference manifest": ITERATIVE / "radial_floor_reference.sha256",
    "prepare deck": ITERATIVE / "radial_floor_prepare.x2m",
    "arm template": ITERATIVE / "radial_floor_arm.x2m.in",
    "probe template": ITERATIVE / "radial_floor_probe.x2m.in",
    "runner": ITERATIVE / "run_radial_floor_diagnostic.sh",
    "status checker": ITERATIVE / "check_radial_floor_status.py",
    "status tests": ITERATIVE / "test_radial_floor_status.py",
    "XSM checker": ITERATIVE / "check_radial_floor_xsm.f90",
    "FLU2DR": ROOT / "src/FLU2DR.f",
    "FLU2AC": ROOT / "src/FLU2AC.f",
    "FLUGPI": ROOT / "src/FLUGPI.f",
    "FLU": ROOT / "src/FLU.f",
    "SPOFSRC": ROOT / "src/SPOFSRC.f90",
    "SPOPROJ": ROOT / "src/SPOPROJ.f90",
    "plane procedure": ROOT / "data/SpotPlaneFS.c2m",
}


def fail(messages: list[str]) -> None:
    raise SystemExit(
        "RADIAL-FLOOR CONTRACT FAIL:\n" + "\n".join(messages)
    )


violations: list[str] = []
for description, path in PATHS.items():
    if not path.is_file():
        violations.append(
            f"missing {description}: {path.relative_to(ROOT)}"
        )
if violations:
    fail(violations)


def read(name: str) -> str:
    return PATHS[name].read_text(encoding="utf-8", errors="strict")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f32_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


protocol_text = read("protocol")
reference = read("reference manifest")
prepare = read("prepare deck")
arm = read("arm template")
probe = read("probe template")
runner = read("runner")
status = read("status checker")
tests = read("status tests")
xsm = read("XSM checker")
flu2dr = read("FLU2DR")
flugpi = read("FLUGPI")
plane = read("plane procedure")
protocol = json.loads(protocol_text)

# Freeze the declared scientific meaning and the absence of tunable
# acceptance machinery.
if sha256(PATHS["protocol"]) != (
    "6a68bb319c382b96df7289e848bbfb4da3341bf6406b72cfe2c381e579d863a2"
):
    violations.append("radial-floor protocol bytes differ from the freeze")
if set(protocol) != {
    "schema",
    "purpose",
    "scientific_scope",
    "plane",
    "groups",
    "production_solver",
    "common_restart",
    "acce_coupling",
    "main_arms",
    "terminal_probes",
    "raw_log_contract",
    "fixed_point_defect",
    "threshold",
    "aggregation",
    "relaxation",
    "fitting",
    "causal_claim",
    "stage4_status",
    "stage5_status",
    "outer_convergence",
}:
    violations.append("protocol key set differs from the frozen schema")
if (
    protocol.get("schema") != "spot-radial-floor-diagnostic-v1"
    or protocol.get("plane") != 1
    or protocol.get("groups") != 370
    or protocol.get("threshold") is not None
    or protocol.get("aggregation") is not None
    or protocol.get("relaxation") is not None
    or protocol.get("fitting") is not None
    or protocol.get("causal_claim") is not None
    or protocol.get("stage4_status") != "INVALID"
    or protocol.get("stage5_status") != "NOT-AUTHORIZED"
    or protocol.get("outer_convergence") != "NOT-EVALUATED"
):
    violations.append("protocol scientific status or null controls changed")
solver = protocol.get("production_solver", {})
if solver != {
    "module": "FLU:",
    "implementation": "FLU2DR",
    "source_modification": False,
    "calculation_type": "S",
    "door": "MCCG",
    "rebalancing": "ON and identical in both arms and both probes",
    "solver_eps_f32_bits": "0x348637bd",
    "maxinr": 740,
    "strict_gate": (
        "EEXT < EPSOUT and EUNK < EPSUNK and EINR < EPSINR "
        "and inner STATE == 1 and IEXTF >= 2"
    ),
}:
    violations.append("production FLU2DR contract changed")
expected_arms = [
    {
        "id": "NATIVE",
        "maxout": 6,
        "free_steps": 3,
        "accelerated_steps": 3,
        "termination": (
            "normal strict early exit at IEXTF 2 through 6, otherwise "
            "a diagnostic cap at IEXTF 6"
        ),
    },
    {
        "id": "STATIONARY",
        "maxout": 6,
        "free_steps": 1,
        "accelerated_steps": 0,
        "termination": (
            "normal strict early exit at IEXTF 2 through 6, otherwise "
            "a diagnostic cap at IEXTF 6"
        ),
    },
]
if protocol.get("main_arms") != expected_arms:
    violations.append("two main-arm controls changed")
common_restart = protocol.get("common_restart", {})
if common_restart.get("cap_leakage_metadata") != (
    "excluded from fixed-input equality because post-radial SPOLEAK "
    "replaced FLUX/SPOT-LEAK1D with returned-axial L1; the actual "
    "cap-solve input is SYSTEM/SPOT-LEAK1D and is copied unchanged to "
    "both arms"
):
    violations.append("cap leakage-metadata timing contract changed")
probes = protocol.get("terminal_probes", {})
if (
    probes.get("count") != 2
    or probes.get("maxout") != 1
    or probes.get("free_steps") != 1
    or probes.get("accelerated_steps") != 0
    or "IEXTF >= 2" not in probes.get("termination", "")
    or "Ganlib-only checker" not in probes.get("quantity", "")
):
    violations.append("terminal-probe controls changed")
for token, owner in (
    ("reset independently", "common restart history"),
    ("no AKEEP or ZMU history", "common restart history"),
    ("inner and outer FLU2DR acceleration", "ACCE coupling"),
    ("counters are distinct", "ACCE coupling"),
    ("Ganlib-only post-minus-pre", "defect scope"),
    ("not an independently assembled A*phi-q", "defect scope"),
    ("NATIVE strict exit before IEXTF 4", "defect scope"),
):
    locations = {
        "common restart history": protocol["common_restart"]["cycle_history"],
        "ACCE coupling": protocol["acce_coupling"],
        "defect scope": protocol["fixed_point_defect"],
    }
    if token not in locations[owner]:
        violations.append(f"protocol no longer binds {owner}: {token}")

# Freeze the current production implementation.  The diagnostic may call it
# but may not patch it to expose or alter an iteration.
expected_source_hashes = {
    "FLU2DR": "9c82fbecbfcbd5637ab3cd2d38ccfd5bbb6a3a575ebfb8089a9ae99f66ec6841",
    "FLU2AC": "3d8817087d106062eed6c155bca11b10171df322eb8fe15d83398e8cf717895a",
    "FLUGPI": "7c8faa89f3d0163cee083e8694ac5ffcfdec528c1681df26a30fad44ed6eba23",
    "FLU": "d820fd3b2d9ff879138daa5ef160221bb703fa03be72f3b4beca2561d17914b1",
    "SPOFSRC": "5c35d4e5a40566ab9554a3674bb4b9500fdc6f00d89fff4ab047441462d9d39c",
    "SPOPROJ": "8d7e93d4b850b45f31303d1cd8ad1c64496014c34d0edf7fc1b08b8932f153a7",
    "plane procedure": (
        "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5"
    ),
}
for name, expected in expected_source_hashes.items():
    if sha256(PATHS[name]) != expected:
        violations.append(f"{name} differs from the frozen production source")
expected_reference = {
    "Dragon": "e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759",
    "FLU2DR.f": expected_source_hashes["FLU2DR"],
    "FLU2AC.f": expected_source_hashes["FLU2AC"],
    "FLUGPI.f": expected_source_hashes["FLUGPI"],
    "FLU.f": expected_source_hashes["FLU"],
    "SPOFSRC.f90": expected_source_hashes["SPOFSRC"],
    "SPOPROJ.f90": expected_source_hashes["SPOPROJ"],
    "initial_snapshots.xsm": (
        "37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95"
    ),
    "state0_axial.xsm": (
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb"
    ),
    "initial_axial_track.xsm": (
        "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7"
    ),
    "initial_radial_track.bin": (
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8"
    ),
    "state1_snapshots.xsm": (
        "f4c01f734ad2a304aa3ef6e2156fea739e2eece0023dd407e33256983775aaad"
    ),
    "inner_sensitivity.log": (
        "fb68de3f1cd345338e2e629170c9bcfd7b69b87be4766590e53aadf7c1ff1abf"
    ),
}
reference_rows = [
    row.split()
    for row in reference.splitlines()
    if row.strip()
]
if (
    len(reference_rows) != len(expected_reference)
    or any(len(row) != 2 for row in reference_rows)
    or {row[1]: row[0] for row in reference_rows} != expected_reference
):
    violations.append("radial-floor reference manifest differs from freeze")
for token in (
    "AKEEP(:8)=0.0D0",
    "NCTOT=NCPTA+NCPTL",
    "MOD(JT-1,NCTOT)",
    "MOD(IT-1,NCTOT)",
    "CALL FLU2AC(NGRP,NUNKNO,IGDEB",
    "CALL FLU2AC(NGRP,NUNKNO,1",
    "(IT.GE.2)",
    "FLU2DR-TERM OUTER-GATE=PASS",
    "FLU2DR-DIAG OUTER",
):
    if token not in flu2dr:
        violations.append(f"FLU2DR no longer exposes frozen token {token}")
for token in (
    "IFRITR=3",
    "IACITR=3",
    "CARLIR.EQ.'ACCE'",
    "IFRITR,IACITR",
):
    if token not in flugpi:
        violations.append(f"FLUGPI no longer binds ACCE token {token}")

# Preparation is extraction/source reconstruction only: no transport solve.
for token in (
    "RADIAL-FLOOR-PREPARE-BEGIN",
    "RADIAL-FLOOR-PREPARE-COMPLETE",
    "state1_snapshots.xsm",
    "ITEM 1",
    "SPOPROJ:",
    "SPOFSRC:",
    "restart_macro0.xsm",
    "restart_source.xsm",
    "restart_system.xsm",
    "restart_track.xsm",
    "restart_cap.xsm",
    "XSM_FILE R_MACRO ::",
    "XSM_FILE R_SOURCE ::",
    "XSM_FILE R_SYSTEM ::",
    "XSM_FILE R_TRACK ::",
    "XSM_FILE R_CAP ::",
    "SYSTEM := RECOVER: CAP_ARCH :: ITEM 1 ;",
    "FLUX := RECOVER: CAP_ARCH :: ITEM 1 ;",
):
    if token not in prepare:
        violations.append(f"prepare deck does not bind {token}")
if re.search(r":=\s*FLU:", prepare, re.IGNORECASE):
    violations.append("prepare deck performs an unauthorized transport solve")
if "SNAP := RECOVER: CAP_ARCH" in prepare:
    violations.append("prepare deck incorrectly nests the cap root archive")
for deck_name, deck_text in (
    ("prepare", prepare),
    ("arm", arm),
    ("probe", probe),
):
    for object_name in re.findall(
        r"^(?:XSM_FILE|SEQ_BINARY|INTEGER|REAL)[ \t]+"
        r"([A-Za-z][A-Za-z0-9_]*)\b",
        deck_text,
        re.MULTILINE,
    ):
        if len(object_name) > 12:
            violations.append(
                f"{deck_name} deck CLE declaration exceeds 12 characters: "
                f"{object_name}"
            )


def require_template(
    text: str,
    role: str,
    maxout: int,
    placeholders: dict[str, int],
) -> None:
    for token, count in placeholders.items():
        found = text.count(token)
        if found != count:
            violations.append(
                f"{role} template token {token}: expected {count}, "
                f"found {found}"
            )
    for token in (
        f"RADIAL-FLOOR-{role}-BEGIN",
        f"RADIAL-FLOOR-{role}-HISTORY",
        f"RADIAL-FLOOR-{role}-CONTROLS",
        f"RADIAL-FLOOR-{role}-COMPLETE",
        "MODULE FLU: END:",
        f"INTEGER outer_cap := {maxout} ;",
        "INTEGER inner_cap := 740 ;",
        "REAL solver_eps := 2.5E-7 ;",
        "TYPE S INIT ON REBA ON",
        "EXTE <<outer_cap>> <<solver_eps>>",
        "UNKT <<solver_eps>>",
        "THER <<inner_cap>> <<solver_eps>>",
        "ACCE <<free_steps>> <<acc_steps>>",
    ):
        if token not in text:
            violations.append(f"{role} template does not bind {token}")
    if len(re.findall(r":=\s*FLU:", text, re.IGNORECASE)) != 1:
        violations.append(f"{role} template must call production FLU once")
    if f32_bits(2.5e-7) != 0x348637BD:
        violations.append("host binary32 h/2 identity is false")
    for pattern, description in (
        (r"\bWHILE\b|\bREPEAT\b", "loop"),
        (r"\bRELAX(?:ATION)?\b|\bDAMP(?:ING)?\b", "relaxation"),
        (r"\bALPHA\b|\bOMEGA\b", "mixing parameter"),
        (r"\bFIT(?:TED|TING)?\b", "fitting"),
    ):
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(
                f"{role} template contains unauthorized {description}"
            )


require_template(
    arm,
    "ARM",
    6,
    {"@ARM@": 2, "@FREE@": 1, "@ACCEL@": 1},
)
for token in (
    "INTEGER free_steps := @FREE@ ;",
    "INTEGER acc_steps := @ACCEL@ ;",
):
    if token not in arm:
        violations.append(f"arm template does not bind {token}")
require_template(
    probe,
    "PROBE",
    1,
    {"@ARM@": 2},
)
for token in (
    "INTEGER free_steps := 1 ;",
    "INTEGER acc_steps := 0 ;",
):
    if token not in probe:
        violations.append(f"probe template does not bind {token}")

# The runner is the provenance boundary: it must instantiate the two and only
# two arm controls, make fresh copies, bind terminal states to probes, and
# call the independent status and Ganlib-only XSM checkers.
for token in (
    "radial_floor_prepare.x2m",
    "radial_floor_arm.x2m.in",
    "radial_floor_probe.x2m.in",
    "radial_floor_protocol.json",
    "check_radial_floor_contract.py",
    "check_radial_floor_status.py",
    "check_radial_floor_xsm.f90",
    "NATIVE",
    "STATIONARY",
    "3 3",
    "1 0",
    "restart_cap.xsm",
    "arm_flux.xsm",
    "probe_post.xsm",
    "git -C",
    "ls-files --error-unmatch",
    "diff --quiet",
    "diff --cached --quiet",
    "protocol_commit.txt",
    "prepared_manifest.sha256",
    "prepared_replay_final.log",
    "artifact_replay.log",
    "shasum",
    "cmp",
    "PREPARED",
    "phrase_count",
    "^ normal end of execution for dragon 5  Version 5\\.1\\.0",
):
    if token not in runner:
        violations.append(f"runner does not bind {token}")
if "preflight/" in runner or "mkdir preflight" in runner:
    violations.append("runner fabricates surrogate preflight solver outputs")
for forbidden, description in (
    (r"\bRELAX(?:ATION)?\b|\bDAMP(?:ING)?\b", "relaxation"),
    (r"\bALPHA\b|\bOMEGA\b", "mixing parameter"),
    (r"\bFIT(?:TED|TING)?\b", "fitting"),
    (
        r"(?:1e|[0-9]\.)-[0-9]+.*(?:accept|classif|threshold)",
        "numeric classification threshold",
    ),
):
    if re.search(forbidden, runner, re.IGNORECASE):
        violations.append(f"runner contains unauthorized {description}")

# The status machine accepts strict/cap main arms and only a one-step DIAG
# probe, while retaining the failed scientific status.
for token in (
    "STRICT",
    "CAP",
    "ONE-STEP-DIAGNOSTIC",
    "BOTH-STRICT",
    "NATIVE-ONLY-STRICT",
    "STATIONARY-ONLY-STRICT",
    "BOTH-CAP",
    "INCONCLUSIVE-NO-OUTER-ACCELERATION",
    "IEXTF >= 2",
    "MAXOUT",
    "ACCE",
    "NOT-A-PHI-MINUS-Q-RESIDUAL",
    "THRESHOLD NONE",
    "STAGE4 INVALID",
    "STAGE5 NOT-AUTHORIZED",
    "OUTER-CONVERGENCE NOT-EVALUATED",
):
    if token not in status:
        violations.append(f"status checker does not bind {token}")
for token in (
    "test_strict",
    "test_cap",
    "probe",
    "tamper",
    "duplicate footer",
    "forged footer suffix",
):
    if token.lower() not in tests.lower():
        violations.append(f"synthetic status tests do not bind {token}")

# The independent postprocessor may read Ganlib objects, but it may not
# mutate them or call production SPOT/FLU solver routines.
for token in (
    "RADIAL-FLOOR-XSM",
    "SOURCE-METADATA BITWISE PASS",
    "CAP LEAKAGE-METADATA EXCLUDED",
    "PREPARED NO SOLVER OUTPUTS",
    "SOLVER-OUTPUT LEAKAGE-METADATA BITWISE PASS",
    "QUANTITY ONE-STEP PRODUCTION-MAP FIXED-POINT DEFECT",
    "V2-NUM",
    "V2-DEN",
    "D-V2",
    "MAX-NUM",
    "MAX-DEN",
    "D-MAX",
    "DELTA-ARGMAX",
    "INPUT-ARGMAX",
    "TRACK-TYPE",
    "TRACK DOES NOT SELECT THE MCCG PRODUCTION DOOR",
    "COMPLETE",
):
    if token not in xsm:
        violations.append(f"XSM checker does not bind output token {token}")
for token in (
    "case(5)",
    "input_count=4",
    "case(nargs)",
    "call load_flux(trim(path(4))",
):
    if token not in xsm:
        violations.append(f"XSM checker does not bind PREPARED split: {token}")
if re.search(
    r"\b(?:LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
    xsm,
    re.IGNORECASE,
):
    violations.append("XSM checker contains an LCM mutation")
if re.search(
    r"\buse\s+(?:SPOT|SPO)|\bcall\s+(?:SPO|FLU)",
    xsm,
    re.IGNORECASE,
):
    violations.append("XSM checker calls a production solver routine")

# The original all-plane procedure remains untouched; the diagnostic uses
# its already-preserved plane-1 state rather than launching another map.
for token in ("TYPE S", "EXTE 500", "UNKT", "THER", "SPOFCHK"):
    if token not in plane:
        violations.append(f"frozen plane procedure lacks {token}")

if violations:
    fail(violations)

print(
    "RADIAL-FLOOR CONTRACT PASS: production FLU2DR; common plane-1 "
    "restart; at-most-six ACCE 3/3 versus 1/0 arms; fresh one-step "
    "stationary probes; no threshold, fit, relaxation, or Stage-4 claim."
)

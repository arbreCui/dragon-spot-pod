#!/usr/bin/env python3
"""Static, fail-closed contract for the Stage-4 h/2 SPOT map deck."""

from __future__ import annotations

import json
from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[2]
DECK_PATH = ROOT / "validation/iterative/inner_sensitivity_map.x2m"
BASELINE_DECK_PATH = ROOT / "validation/iterative/one_corrected_map.x2m"
REFRESH_PATH = ROOT / "data/SpotRefFS.c2m"
PLANE_PATH = ROOT / "data/SpotPlaneFS.c2m"
PROTOCOL_PATH = ROOT / "validation/iterative/inner_sensitivity_protocol.json"
REFERENCE_PATH = ROOT / "validation/iterative/inner_sensitivity_reference.sha256"
RUNTIME_PATH = ROOT / "validation/iterative/check_one_map_runtime.py"
STATUS_PATH = (
    ROOT / "validation/iterative/check_inner_sensitivity_status.py"
)
FAILURE_PATH = (
    ROOT / "validation/iterative/check_inner_sensitivity_failure.py"
)
ONE_MAP_XSM_PATH = ROOT / "validation/iterative/check_one_map_xsm.f90"
PAIR_XSM_PATH = ROOT / "validation/iterative/check_inner_sensitivity_xsm.f90"
RUNNER_PATH = ROOT / "validation/iterative/run_inner_sensitivity.sh"


def fail(messages: list[str]) -> None:
    raise SystemExit(
        "INNER-SENSITIVITY CONTRACT FAIL:\n" + "\n".join(messages)
    )


violations: list[str] = []
for path in (
    DECK_PATH,
    BASELINE_DECK_PATH,
    REFRESH_PATH,
    PLANE_PATH,
    PROTOCOL_PATH,
    REFERENCE_PATH,
    RUNTIME_PATH,
    STATUS_PATH,
    FAILURE_PATH,
    ONE_MAP_XSM_PATH,
    PAIR_XSM_PATH,
    RUNNER_PATH,
):
    if not path.is_file():
        violations.append(f"missing {path.relative_to(ROOT)}")
if violations:
    fail(violations)

deck = DECK_PATH.read_text(encoding="utf-8", errors="strict")
baseline_deck = BASELINE_DECK_PATH.read_text(encoding="utf-8", errors="strict")
refresh = REFRESH_PATH.read_text(encoding="utf-8", errors="strict")
plane = PLANE_PATH.read_text(encoding="utf-8", errors="strict")
runtime = RUNTIME_PATH.read_text(encoding="utf-8", errors="strict")
status_checker = STATUS_PATH.read_text(encoding="utf-8", errors="strict")
failure_checker = FAILURE_PATH.read_text(
    encoding="utf-8", errors="strict"
)
one_map_xsm = ONE_MAP_XSM_PATH.read_text(encoding="utf-8", errors="strict")
pair_xsm = PAIR_XSM_PATH.read_text(encoding="utf-8", errors="strict")
runner = RUNNER_PATH.read_text(encoding="utf-8", errors="strict")
protocol = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8", errors="strict"))
active_deck = "\n".join(
    line for line in deck.splitlines() if not line.lstrip().startswith("*")
)


def require_exact(pattern: str, count: int, description: str) -> None:
    found = len(re.findall(pattern, deck, re.IGNORECASE | re.MULTILINE))
    if found != count:
        violations.append(
            f"{description}: expected {count} occurrence(s), found {found}"
        )


def require_active(pattern: str, description: str) -> None:
    if re.search(
        pattern, active_deck, re.IGNORECASE | re.MULTILINE | re.DOTALL
    ) is None:
        violations.append("missing " + description)


def f32_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


expected_protocol = {
    "schema": "spot-inner-sensitivity-v1",
    "method": "fixed-space Galerkin-SPOD inner-tolerance sensitivity",
    "groups": 370,
    "planes": 3,
    "rank": 1,
    "initializer_solver_eps_f32_bits": "0x350637bd",
    "baseline_map_solver_eps_f32_bits": "0x350637bd",
    "refined_map_solver_eps_f32_bits": "0x348637bd",
    "refinement_identity": (
        "2 * refined_map_solver_eps == baseline_map_solver_eps in binary32"
    ),
    "maxout": 500,
    "maxinr": 740,
    "initializer_axial_solves": 1,
    "map_radial_solves": 3,
    "map_axial_solves": 1,
    "outer_updates": 1,
    "same_x0_evidence": [
        (
            "identical Dragon executable, procedures, seed archives, rank "
            "and initializer controls"
        ),
        "byte-identical basis_reference.xsm",
        "byte-identical state0_axial.xsm",
        (
            "bitwise-identical canonical a, rho, L, basis, Gram matrix, "
            "plane heights and normalization"
        ),
        (
            "bitwise-identical radial SPOT-LEAK1D, SPOT-QFISS and "
            "SPOT-FS-K inputs"
        ),
    ],
    "reported_vectors": [
        "D_out_h = D(x1_h, x0)",
        "D_out_h2 = D(x1_h2, x0)",
        "D_in = D(x1_h2, x1_h)",
    ],
    "components": ["R_rho", "R_L", "D_L", "R_a"],
    "component_rule": {
        "positive_outer": "RESOLVED iff D_in < D_out_h",
        "zero_outer": "RESOLVED iff D_in == 0 at stored precision",
        "otherwise": "UNRESOLVED",
    },
    "aggregation": None,
    "relaxation": None,
    "fitting": None,
    "outer_convergence": "not_evaluated",
    "h2_replay": "required before final Stage-4 qualification",
    "stage4_state_rule": {
        "any_component_unresolved": "UNRESOLVED",
        "all_components_resolved_without_h2_replay": "PENDING-REPLAY",
        "all_components_resolved_with_h2_replay": "QUALIFIED",
    },
    "stage5_authorization": (
        "only if all four components are RESOLVED and both lanes pass every "
        "physical and execution contract"
    ),
}
if protocol != expected_protocol:
    violations.append("protocol content or key set differs from frozen Stage 4")

expected_reference = {
    "Dragon": "e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759",
    "one_corrected_map.x2m": "4c8780b1739b5aaec0c78d0cbe2b23b6021f860d232af8e9c1767ed989c9720e",
    "SpotRefFS.c2m": "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742",
    "SpotPlaneFS.c2m": "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5",
    "initial_snapshots.xsm": "37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95",
    "initial_axial_track.xsm": "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7",
    "initial_axial_macrolib.xsm": "2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a",
    "initial_radial_track.bin": "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8",
    "basis_reference.xsm": "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504",
    "state0_axial.xsm": "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb",
    "state1_system.xsm": "fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2",
    "state1_axial.xsm": "2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484",
    "state1_snapshots.xsm": "1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1",
}
reference_lines = [
    line.split()
    for line in REFERENCE_PATH.read_text(
        encoding="utf-8", errors="strict"
    ).splitlines()
    if line.strip()
]
if (
    len(reference_lines) != len(expected_reference)
    or any(len(fields) != 2 for fields in reference_lines)
    or {fields[1]: fields[0] for fields in reference_lines}
    != expected_reference
):
    violations.append("Stage-3 reference manifest differs from frozen bytes")


# The only intended numerical change from Stage 3 is h -> h/2 inside G.
init_match = re.search(
    r"^\s*REAL\s+init_eps\s*:=\s*([0-9.+\-Ee]+)\s*;\s*$",
    deck,
    re.IGNORECASE | re.MULTILINE,
)
map_match = re.search(
    r"^\s*REAL\s+map_eps\s*:=\s*([0-9.+\-Ee]+)\s*;\s*$",
    deck,
    re.IGNORECASE | re.MULTILINE,
)
if init_match is None or map_match is None:
    violations.append("missing unique init_eps/map_eps declarations")
else:
    init_eps = float(init_match.group(1))
    map_eps = float(map_match.group(1))
    if f32_bits(init_eps) != 0x350637BD:
        violations.append("init_eps is not frozen binary32 h=5.0E-7")
    if f32_bits(map_eps) != 0x348637BD:
        violations.append("map_eps is not frozen binary32 h/2=2.5E-7")
    if f32_bits(map_eps) != f32_bits(init_eps / 2.0):
        violations.append("map_eps is not the binary32 half of init_eps")

require_exact(r"\bREAL\s+init_eps\s*:=", 1, "init_eps declaration")
require_exact(r"\bREAL\s+map_eps\s*:=", 1, "map_eps declaration")
require_exact(r"\binit_eps\b", 5, "init_eps total use")
require_exact(r"\bmap_eps\b", 6, "map_eps total use")
if re.search(r"\bsolver_eps\b", active_deck, re.IGNORECASE):
    violations.append("ambiguous legacy solver_eps remains active")

# After normalizing the two tolerance controls and their explicit markers,
# every active CLE-2000 statement must be the frozen Stage-3 deck.
normalized = re.sub(
    r"^\s*REAL\s+init_eps\s*:=\s*5\.0E-7\s*;\s*\n"
    r"\s*REAL\s+map_eps\s*:=\s*2\.5E-7\s*;\s*$",
    "REAL solver_eps := 5.0E-7 ;",
    active_deck,
    count=1,
    flags=re.IGNORECASE | re.MULTILINE,
)
normalized = re.sub(
    r'^\s*ECHO\s+"ITERATIVE-MAP-INIT-TOLERANCE"\s+init_eps\s*;\s*\n'
    r'\s*ECHO\s+"ITERATIVE-MAP-MAP-TOLERANCE"\s+map_eps\s*;\s*$',
    'ECHO "ITERATIVE-MAP-INNER-TOLERANCE" solver_eps ;',
    normalized,
    count=1,
    flags=re.IGNORECASE | re.MULTILINE,
)
normalized = re.sub(
    r"\b(?:init_eps|map_eps)\b",
    "solver_eps",
    normalized,
    flags=re.IGNORECASE,
)


def canonical_active(source: str) -> str:
    lines = (
        line
        for line in source.splitlines()
        if line.strip() and not line.lstrip().startswith("*")
    )
    return "\n".join(" ".join(line.split()) for line in lines)


if canonical_active(normalized) != canonical_active(baseline_deck):
    violations.append(
        "normalized h/2 deck differs from Stage 3 beyond tolerance controls"
    )
initialized_controls = {
    name.lower()
    for name in re.findall(
        r"^\s*(?:INTEGER|REAL|DOUBLE)\s+"
        r"([A-Za-z][A-Za-z0-9_]*)\s*:=",
        active_deck,
        re.IGNORECASE | re.MULTILINE,
    )
}
if initialized_controls != {"spod_rank", "init_eps", "map_eps"}:
    violations.append(
        "initialized numerical controls differ from "
        "{spod_rank, init_eps, map_eps}"
    )

# Marker names make the initializer/G distinction machine-readable.
for marker in (
    "ITERATIVE-MAP-INIT-TOLERANCE",
    "ITERATIVE-MAP-MAP-TOLERANCE",
):
    require_exact(
        rf'^\s*ECHO\s+"{re.escape(marker)}"\s+\w+\s*;\s*$',
        1,
        f"{marker} marker",
    )
require_active(
    r'ECHO\s+"ITERATIVE-MAP-INIT-TOLERANCE"\s+init_eps\s*;\s*'
    r'ECHO\s+"ITERATIVE-MAP-MAP-TOLERANCE"\s+map_eps\s*;',
    "ordered initializer and map tolerance markers",
)

# The five scientific basenames remain unchanged and can be compared across
# isolated h and h/2 work directories without changing CLE-2000 handles.
expected_xsm = {
    "SNAP_SEED": "./initial_snapshots.xsm",
    "TRACK_AX": "./initial_axial_track.xsm",
    "MACROLIB3": "./initial_axial_macrolib.xsm",
    "BASIS_REF": "./basis_reference.xsm",
    "AX0_ARCH": "./state0_axial.xsm",
    "SYS1_ARCH": "./state1_system.xsm",
    "AX1_ARCH": "./state1_axial.xsm",
    "SNAP1_ARCH": "./state1_snapshots.xsm",
}
xsm_records = re.findall(
    r"^\s*XSM_FILE\s+([A-Za-z][A-Za-z0-9_]*)\s*::\s*"
    r"FILE\s+'([^']+)'\s*;\s*$",
    deck,
    re.MULTILINE,
)
output_records = dict(xsm_records)
for handle, basename in expected_xsm.items():
    if output_records.get(handle) != basename:
        violations.append(f"{handle} does not retain basename {basename}")
if len(xsm_records) != 8 or len(output_records) != 8:
    violations.append(
        "expected exactly eight unique XSM_FILE records, found "
        f"{len(xsm_records)} records and {len(output_records)} unique handles"
    )
require_active(
    r"SEQ_BINARY\s+TRACK_f\s*::\s*"
    r"FILE\s+'\./initial_radial_track\.bin'\s*;",
    "frozen radial tracking basename",
)

# One initializer solve is held at h.
require_active(
    r"AX_PREVIOUS\s*:=\s*FLU:\s+MACROLIB3\s+TRACK_AX\s+BASIS_REF\s*::"
    r"\s*EDIT\s+-3\s+TYPE\s+K\s+B1\s+SIGS\s+EXTE\s+500\s+"
    r"<<init_eps>>\s*UNKT\s+<<init_eps>>\s+THER\s+<<init_eps>>\s*;",
    "initializer axial FLU with all three gates at init_eps",
)

# G contains exactly one all-plane radial traversal and one returned axial
# solve. The frozen three-plane seed is validated independently at runtime.
require_active(
    r"SNAP\s*:=\s*SpotRefFS\s+SNAP\s+TRACK\s+TRACK_f\s*::"
    r"\s*<<k0>>\s+<<map_eps>>\s*;",
    "all-plane radial map at map_eps",
)
require_active(
    r"AX_CURRENT\s*:=\s*FLU:\s+MACROLIB3\s+TRACK_AX\s+SYSTEM_NEXT\s*::"
    r"\s*EDIT\s+-3\s+TYPE\s+K\s+B1\s+SIGS\s+EXTE\s+500\s+"
    r"<<map_eps>>\s*UNKT\s+<<map_eps>>\s+THER\s+<<map_eps>>\s*;",
    "returned axial FLU with all three gates at map_eps",
)
require_exact(r":=\s*FLU:", 2, "top-level axial FLU solves")
require_exact(
    r"SNAP\s*:=\s*SpotRefFS\b", 1, "all-plane radial map invocation"
)

# Bind the procedure forwarding path: one FLU per archived plane, with the
# passed map tolerance controlling EPSOUT, EPSUNK and EPSINR.
if re.search(
    r"SYSTEM\s+FLUX\s*:=\s*SpotPlaneFS.*?"
    r"<<isnap>>\s+<<keff>>\s+<<flu_eps>>\s*;",
    refresh,
    re.IGNORECASE | re.DOTALL,
) is None:
    violations.append("SpotRefFS does not forward flu_eps to every plane")
if len(re.findall(r":=\s*SpotPlaneFS\b", refresh, re.IGNORECASE)) != 1:
    violations.append("SpotRefFS must contain one per-plane procedure call")
if re.search(
    r"FLUX\s*:=\s*FLU:.*?EXTE\s+500\s+<<flu_eps>>"
    r"\s*UNKT\s+<<flu_eps>>\s+THER\s+<<flu_eps>>\s*;",
    plane,
    re.IGNORECASE | re.DOTALL,
) is None:
    violations.append("SpotPlaneFS does not apply flu_eps to all FLU gates")
if len(re.findall(r":=\s*FLU:", plane, re.IGNORECASE)) != 1:
    violations.append("SpotPlaneFS must contain exactly one radial FLU")

# Preserve the fixed-space raw-map sequence and undamped feedback.
ordered_patterns = (
    r"BASIS_REF\s*:=\s*ASM:.*?SPOD\s*<<spod_rank>>\s*;",
    r"AX_PREVIOUS\s*:=\s*FLU:",
    r"AX_PREVIOUS\s*:=\s*SPOSTATE:",
    r"SNAP\s*:=\s*SPOLEAK:\s*SNAP\s+AX_PREVIOUS\s+TRACK_AX",
    r"SNAP\s*:=\s*SPOPROJ:\s*SNAP\s+AX_PREVIOUS\s+TRACK_AX\s*::\s*FIXB",
    r"SNAP\s*:=\s*SpotRefFS",
    r"SYSTEM_NEXT\s*:=\s*ASM:.*?BASIS_REF.*?FIXB",
    r"AX_CURRENT\s*:=\s*FLU:",
    r"AX_CURRENT\s*:=\s*SPOSTATE:",
    r"AX_CURRENT\s*:=\s*SPOXCONV:\s*AX_CURRENT\s+AX_PREVIOUS",
    r"SNAP\s*:=\s*SPOLEAK:\s*SNAP\s+AX_CURRENT\s+TRACK_AX",
)
position = 0
for pattern in ordered_patterns:
    match = re.search(
        pattern,
        active_deck[position:],
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if match is None:
        violations.append(f"missing or reordered map event: {pattern}")
        break
    position += match.end()

# CLE-2000 identifiers are limited to 12 characters.
declarations = re.findall(
    r"^\s*(?:INTEGER|REAL|DOUBLE|LINKED_LIST|XSM_FILE|SEQ_BINARY)\s+"
    r"([^;:]+)",
    deck,
    re.MULTILINE,
)
for declaration in declarations:
    for name in re.findall(r"\b[A-Za-z][A-Za-z0-9_]*\b", declaration):
        if len(name) > 12:
            violations.append(
                f"CLE-2000 identifier exceeds 12 characters: {name}"
            )

# No outer iteration, damping, fitting, stabilization or empirical factor is
# permitted in this one-map sensitivity experiment.
for pattern, description in (
    (r"\bWHILE\b|\bREPEAT\b", "outer iteration"),
    (r"\bRELAX(?:ATION)?\b|\bDAMP(?:ING)?\b", "relaxation or damping"),
    (r"\bALPHA\b|\bOMEGA\b", "mixing parameter"),
    (r"\bFIT(?:TED|TING)?\b", "fitted factor"),
    (r"\bCMFD\b", "empirical stabilization"),
):
    if re.search(pattern, active_deck, re.IGNORECASE):
        violations.append(f"active deck contains forbidden {description}")

for token in (
    "ITERATIVE-MAP-INIT-TOLERANCE",
    "ITERATIVE-MAP-MAP-TOLERANCE",
    "0x350637BD",
    "0x348637BD",
    "expected_end_source",
    "source_line + 1",
):
    if token not in runtime:
        violations.append(f"runtime checker does not bind {token}")
if "|<0097" in runtime:
    violations.append("runtime checker retains a Stage-3 END line number")
for name in (
    "inner_sensitivity_map.x2m",
    "inner_sensitivity_protocol.json",
    "inner_sensitivity_reference.sha256",
    "check_inner_sensitivity_contract.py",
    "check_inner_sensitivity_failure.py",
    "check_inner_sensitivity_status.py",
    "check_one_map_runtime.py",
    "check_one_map_xsm.f90",
    "check_inner_sensitivity_xsm.f90",
):
    if name not in runner:
        violations.append(f"runner does not bind {name}")
dragon_runs = re.findall(
    r'"\$DRAGON_BIN"\s*<\s*"\$DECK"',
    runner,
    re.MULTILINE,
)
if len(dragon_runs) != 1:
    violations.append(
        "runner must execute exactly one Dragon deck evaluation"
    )
if re.search(
    r'shasum\s+-a\s+256\s+-c\s+"\$WORK/input_manifest\.sha256"',
    runner,
    re.MULTILINE,
) is None:
    violations.append("runner does not replay its frozen input manifest")
for token in (
    "validate_h2_reference",
    "h2_reference.sha256",
    "INNER-SENSITIVITY CAPTURE PASS",
    'separator != "  "',
    "NR != 5",
):
    if token not in runner:
        violations.append(f"runner does not enforce {token}")
for index, name in enumerate(
    (
        "basis_reference.xsm",
        "state0_axial.xsm",
        "state1_system.xsm",
        "state1_axial.xsm",
        "state1_snapshots.xsm",
    ),
    1,
):
    if f'expected[{index}] = "{name}"' not in runner:
        violations.append(f"runner H2 reference position {index} changed")
for token in (
    "PENDING-REPLAY",
    "UNRESOLVED",
    "QUALIFIED",
    "NOT-AUTHORIZED",
):
    if token not in status_checker:
        violations.append(f"status checker does not bind {token}")
for token in (
    "INVALID-INNER-NONCONVERGENCE",
    "STAGE4 INVALID",
    "STAGE5 NOT-AUTHORIZED",
    "OUTER-CONVERGENCE NOT-EVALUATED",
):
    if token not in failure_checker:
        violations.append(f"failure checker does not bind {token}")
for source, owner in (
    (one_map_xsm, "one-map XSM checker"),
    (pair_xsm, "pair XSM checker"),
):
    if re.search(
        r"\b(?:LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
        source,
        re.IGNORECASE,
    ):
        violations.append(f"{owner} contains an LCM mutation")
    if re.search(
        r"\buse\s+(?:SPOT|SPO)|\bcall\s+(?:SPO|FLU)",
        source,
        re.IGNORECASE,
    ):
        violations.append(f"{owner} calls a production solver routine")

if violations:
    fail(violations)

print(
    "INNER-SENSITIVITY CONTRACT PASS: initializer=h; "
    "three radial plus returned axial map solves=h/2; "
    "fixed basis, no outer loop, relaxation, fit, or empirical factor."
)

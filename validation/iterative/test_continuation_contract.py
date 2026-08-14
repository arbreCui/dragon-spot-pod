#!/usr/bin/env python3
"""Static, seconds-scale contract for the generic SPOT continuation host."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation/iterative"
radial = (ITERATIVE / "continuation_radial.x2m").read_text(encoding="utf-8")
axial = (ITERATIVE / "continuation_axial.x2m").read_text(encoding="utf-8")
runner = (ITERATIVE / "run_continuation_short.sh").read_text(encoding="utf-8")
policy = (ITERATIVE / "continuation_policy.md").read_text(encoding="utf-8")
manifest = (ITERATIVE / "current_parent.tsv").read_text(encoding="utf-8")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.upper())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CONTINUATION CONTRACT FAIL: {message}")


rcompact = compact(radial)
acompact = compact(axial)

for token in (
    "SNAP := PARENT_SNAP",
    "TRACK := RECOVER: SNAP :: ITEM 3",
    "GREP: PARENT_AX :: GETVAL 'K-EFFECTIVE'",
    "SNAP := SPOPROJ: SNAP PARENT_AX TRACK_AX :: FIXB",
    "SNAP := SPOTREFFS SNAP TRACK TRACK_F",
    "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF",
    "SPOD <<SPOD_RANK>> FIXB",
):
    require(token in rcompact, f"radial deck is missing: {token}")
require(rcompact.count("SNAP := SPOTREFFS") == 1, "radial map call count is not one")
require("INTEGER SPOD_RANK := 1" in rcompact, "rank must remain one")
require("REAL SOLVER_EPS := 5.0E-7" in rcompact, "radial tolerance changed")
require("SPOLEAK:" not in rcompact, "parent leakage must not be returned twice")

axial_steps = (
    "AX_CURRENT := FLU:",
    "AX_CURRENT := SPOGBAL:",
    "AX_CURRENT := SPOSTATE:",
    "AX_CURRENT := SPOXCONV:",
    "SNAP := SPOLEAK:",
)
positions = [acompact.find(step) for step in axial_steps]
require(all(position >= 0 for position in positions), "axial operator is missing")
require(positions == sorted(positions), "axial operator order changed")
for step in axial_steps:
    require(acompact.count(step) == 1, f"axial operator count changed: {step}")
require("REAL SOLVER_EPS := 5.0E-7" in acompact, "axial tolerance changed")
require(
    'ECHO "CONT-RAW-DEFECT" RRHO RLEAK DLEAK RA' in acompact,
    "raw defect order changed",
)
for token in (
    "GETVAL 'SPOT-X-RRHO' 1 >>RRHO<<",
    "GETVAL 'SPOT-X-RLEAK' 1 >>RLEAK<<",
    "GETVAL 'SPOT-X-DLEAK' 1 >>DLEAK<<",
    "GETVAL 'SPOT-X-RA' 1 >>RA<<",
    "GETVAL 'K-EFFECTIVE' 1 >>K_CANDIDATE<<",
    "GETVAL 'SPOT-GBAL' 1 >>GBAL<<",
    "GETVAL 'SPOT-GBAL-MAX' 1 >>GBAL_GROUP<<",
    'ECHO "CONT-CANDIDATE" K_CANDIDATE GBAL GBAL_GROUP',
):
    require(token in acompact, f"reported-field binding changed: {token}")

for deck in (rcompact, acompact):
    require(not re.search(r"\b(?:MAP|STATE)[0-9]+\b", deck), "numbered deck leaked in")
    for forbidden in ("RELA", "ALPHA", "ANDERSON", "CMFD", "CLIP"):
        require(not re.search(rf"\b{forbidden}\b", deck), f"forbidden control: {forbidden}")

rows = [
    line.split()
    for line in manifest.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
roles = (
    "axial_track",
    "axial_macrolib",
    "radial_track",
    "basis_reference",
    "parent_axial",
    "parent_snapshots",
)
require(manifest.splitlines()[0] == "# spot-continuation-parent-v1", "manifest version")
require(len(rows) == len(roles), "manifest must contain six rows")
require(tuple(row[0] for row in rows) == roles, "manifest role order changed")
for row in rows:
    require(len(row) == 3, f"manifest row is not three fields: {row[0]}")
    require(bool(re.fullmatch(r"[0-9a-f]{64}", row[1])), f"invalid hash: {row[0]}")
    path = Path(row[2])
    require(not path.is_absolute() and ".." not in path.parts, f"unsafe path: {row[0]}")

require(
    runner.index("RUN_CONTINUATION=") < runner.index("ROOT=$("),
    "default-off gate must precede repo access",
)
require(
    runner.index("ROOT=$(") < runner.index("WORK=$(mktemp"),
    "setup must precede temporary work",
)
require(runner.count('run_bounded "$RADIAL_WORK/radial.x2m"') == 1, "radial launch count")
require(runner.count('run_bounded "$AXIAL_WORK/axial.x2m"') == 1, "axial launch count")
require("RADIAL_TIMEOUT_SECONDS=120" in runner, "radial process bound changed")
require("AXIAL_TIMEOUT_SECONDS=80" in runner, "axial process bound changed")
require(not re.search(r"(?m)^\s*(?:while|until)\b", runner), "retry loop is forbidden")
require(
    runner.count("./check_one_map_xsm --continued") == 1,
    "continued independent checker must run exactly once",
)
require(
    runner.index("./check_one_map_xsm --continued")
    < runner.index("PUBLISH_DIR=$(mktemp"),
    "candidate publication precedes independent validation",
)
require('test ! -e "$RESULT_DIR"' in runner, "result overwrite guard is missing")
require(
    runner.index('mkdir "$LOCK_DIR"') < runner.index("MAP_STARTED=1"),
    "single-writer lock must precede the map",
)
require('rmdir "$LOCK_DIR"' in runner, "single-writer lock is not released")
require('mkdir "$RESULT_DIR"' not in runner, "final result is exposed before receipt")
require(
    runner.index("shasum -a 256 -c result.sha256")
    < runner.index('mv "$PUBLISH_DIR" "$RESULT_DIR"'),
    "receipt must pass before atomic publication",
)
require(runner.count('mv "$PUBLISH_DIR" "$RESULT_DIR"') == 1, "publication count")
require(
    'DRAGON_HASH_AFTER" = "$DRAGON_HASH_BEFORE' in runner,
    "Dragon provenance is not stable across the run",
)
for frozen in (
    "SpotRefFS.c2m",
    "SpotPlaneFS.c2m",
    "check_one_map_xsm.f90",
    "run_bounded_dragon.py",
):
    require(
        f'"$HOST_WORK/{frozen}"' in runner,
        f"runtime provenance is not frozen: {frozen}",
    )
for marker in (
    r"^>\|CONT-RADIAL-CONTRACT ",
    r"^>\|CONT-RADIAL-COMPLETE ",
    r"^>\|CONT-RAW-DEFECT ",
    r"^>\|CONT-CANDIDATE ",
    r"^>\|CONT-AXIAL-COMPLETE ",
):
    require(marker in runner, f"runtime ECHO is not anchored: {marker}")
require("values[0] <= eps and values[1] <= eps and values[3] <= eps" in runner,
        "three-component decision rule changed")
for label in ("INVALID_MAP", "TOLERANCE_MET", "VALID_NOT_MET"):
    require(policy.count(label) == 1, f"policy category count changed: {label}")
    require(label in runner, f"runner cannot report policy category: {label}")

classifier_match = re.search(
    r"classification=\$\(\n"
    r"\s+PYTHONDONTWRITEBYTECODE=1 python3 -c '\n"
    r"(.*?)\n' \"\$AXIAL_WORK/axial\.log\"\n"
    r"\)",
    runner,
    re.DOTALL,
)
require(classifier_match is not None, "embedded classifier cannot be located")
classifier = classifier_match.group(1)
with tempfile.TemporaryDirectory(prefix="spot-continuation-test.") as temporary:
    log = Path(temporary) / "axial.log"
    for defect, expected in (
        ("0.0 2.094E-4 3.07D-7 7.58E-7", "VALID_NOT_MET"),
        ("0.0 4.0E-7 8.0D-7 5.0E-7", "TOLERANCE_MET"),
    ):
        record = (
            'ECHO "CONT-RAW-DEFECT" rrho rleak dleak ra ;\n'
            f">|CONT-RAW-DEFECT {defect} |>0038\n"
            'ECHO "CONT-CANDIDATE" k_candidate gbal gbal_group ;\n'
            ">|CONT-CANDIDATE 1.364173E+0 3.92E-9 3.24E-3 |>0039\n"
        )
        log.write_text(record, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, "-c", classifier, str(log)],
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, "classifier rejected a finite record")
        require(completed.stdout.strip() == expected, f"classifier result: {expected}")
    log.write_text(
        ">|CONT-RAW-DEFECT NaN 0.0 0.0 0.0 |>0038\n"
        ">|CONT-CANDIDATE 1.0 0.0 0.0 |>0039\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, "-c", classifier, str(log)],
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode != 0, "classifier accepted a non-finite record")

print("CONTINUATION CONTRACT PASS")

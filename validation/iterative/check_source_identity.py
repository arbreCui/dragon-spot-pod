#!/usr/bin/env python3
"""Static contract for the online radial fixed-source identity."""

from __future__ import annotations

from pathlib import Path
import re


root = Path(__file__).resolve().parents[2]
paths = {
    "kernel": root / "src/SPOT_LEAKAGE.f90",
    "source": root / "src/SPOFSRC.f90",
    "assembly": root / "src/SPOASM.f",
    "plane": root / "data/SpotPlaneFS.c2m",
    "test": root / "validation/level2/test_radial_closure.f90",
}

missing = [str(path.relative_to(root)) for path in paths.values() if not path.is_file()]
if missing:
    raise SystemExit(
        "ITERATIVE SOURCE CONTRACT FAIL: missing files: " + ", ".join(missing)
    )

text = {name: path.read_text(errors="strict") for name, path in paths.items()}
violations: list[str] = []


def require(name: str, pattern: str, description: str) -> None:
    if re.search(pattern, text[name], re.IGNORECASE | re.DOTALL) is None:
        violations.append(f"{paths[name].relative_to(root)}: missing {description}")


def forbid(name: str, pattern: str, description: str) -> None:
    if re.search(pattern, text[name], re.IGNORECASE | re.DOTALL) is not None:
        violations.append(f"{paths[name].relative_to(root)}: {description}")


# The radial solve freezes fission from its input field and removes live
# fission from the temporary macrolib.
require(
    "source",
    r"source\s*\(\s*keyflx\(ireg\),igr\s*\)\s*=.*chi.*fis\s*/\s*keff",
    "frozen F*p/k construction",
)
require(
    "source",
    r"LCMPUT\s*\(\s*kpmacro\s*,\s*'NUSIGF'.*zeros",
    "live-fission removal",
)
require("plane", r"SPOFSRC:.*FLUX_OLD", "projected old-field source input")
require("plane", r"TYPE\s+S", "radial fixed-source solve")

# The exact frozen fission vector and its k are persisted on the radial output
# before the temporary source object is deleted.
require(
    "source",
    r"LCMLID\s*\(\s*kentry\(1\)\s*,\s*'SPOT-QFISS'",
    "persisted frozen-fission list",
)
require(
    "source",
    r"LCMPUT\s*\(\s*kentry\(1\)\s*,\s*'SPOT-FS-EQN'",
    "fixed-source equation marker",
)
require(
    "source",
    r"LCMPUT\s*\(\s*kentry\(1\)\s*,\s*'SPOT-FS-K'",
    "persisted frozen-source eigenvalue",
)

# The response kernel begins with qfrozen and adds only off-group scattering.
require("kernel", r"subroutine\s+SPOQFS\b", "SPOQFS kernel")
require(
    "kernel",
    r"source\s*=\s*dble\s*\(\s*qfrozen\(i\)\s*\)",
    "frozen-fission RHS seed",
)
require(
    "kernel",
    r"if\s*\(\s*jg\s*/=\s*igr\s*\)\s*source\s*=\s*source\s*\+",
    "final off-group scattering",
)
spoqfs = re.search(
    r"subroutine\s+SPOQFS\b(?P<body>.*?)end\s+subroutine\s+SPOQFS",
    text["kernel"],
    re.IGNORECASE | re.DOTALL,
)
if spoqfs is None:
    violations.append("src/SPOT_LEAKAGE.f90: cannot isolate SPOQFS")
else:
    body = spoqfs.group("body")
    if re.search(r"\bNUSIGF\b|\bCHI\b|\bSPOF00\b", body, re.IGNORECASE):
        violations.append(
            "src/SPOT_LEAKAGE.f90: SPOQFS re-evaluates final-field fission"
        )

# Assembly selects the equation from an explicit record and fails on a mixed
# online/offline snapshot set. Both branches feed the same SPOLE2 closure.
require(
    "assembly",
    r"IF\s*\(\s*FS_MODE\(ISNAP\)\.EQ\.0\s*\)\s*THEN.*CALL\s+SPOQ00"
    r".*ELSE.*CALL\s+SPOQFS",
    "separate eigenvalue/fixed-source RHS branches",
)
require(
    "assembly",
    r"MIXED EIGENVALUE AND FIXED-SOURCE SNAPSHOTS",
    "mixed-snapshot rejection",
)
require(
    "assembly",
    r"DB2\s*\(\s*I,ISNAP,IGR\s*\)\s*=\s*SPOLE2"
    r"\s*\(.*QREG\(I\).*PHIRK.*LEAK1D",
    "common source-consistent radial closure",
)

# The executable algebra fixture must distinguish the two fission sources.
require(
    "test",
    r"fixed fission is not replaced by final-field fission",
    "source-identity regression assertion",
)

for name in ("kernel", "source", "assembly", "plane"):
    forbid(name, r"\bRELA(?:X|XATION)?\b", "contains a relaxation control")
    forbid(name, r"\bCMFD\b", "contains a CMFD correction")
    forbid(name, r"\bFLU_FLOOR\b", "contains a flux floor")

if violations:
    raise SystemExit("ITERATIVE SOURCE CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "ITERATIVE SOURCE CONTRACT PASS: online radial fixed-source snapshots "
    "preserve F*p/k and combine it only with final off-group scattering; "
    "offline eigenvalue snapshots retain the final-state source branch."
)

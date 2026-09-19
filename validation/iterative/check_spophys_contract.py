#!/usr/bin/env python3
"""Static registration/lifecycle supplement for the executable SPOPHYS smoke."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
driver_path = ROOT / "src/KDRDRV.F"
source_path = ROOT / "src/SPOPHYS.f90"
assembly_path = ROOT / "src/SPOASM.f"
solver_paths = (ROOT / "src/SPOT1P.f90", ROOT / "src/SPOT1P64.f90")
ignore_path = ROOT / ".gitignore"

for path in (driver_path, source_path, assembly_path, *solver_paths, ignore_path):
    if not path.is_file():
        raise SystemExit(f"SPOPHYS CONTRACT FAIL: missing {path.relative_to(ROOT)}")

driver = driver_path.read_text(errors="strict")
source = source_path.read_text(errors="strict")
assembly = assembly_path.read_text(errors="strict")
solvers = {path.name: path.read_text(errors="strict") for path in solver_paths}
violations: list[str] = []

if re.search(
    r"HMODUL\.EQ\.'SPOPHYS:'.*?CALL\s+SPOPHYS\s*\(\s*NENTRY\s*,"
    r"\s*HENTRY\s*,\s*IENTRY\s*,\s*JENTRY\s*,\s*KENTRY\s*\)",
    driver,
    re.IGNORECASE | re.DOTALL,
) is None:
    violations.append("KDRDRV does not register and call SPOPHYS")

required = (
    r"LCMPUT\s*\(\s*kentry\(1\)\s*,\s*'SPOT-FIXB'\s*,\s*1\s*,\s*1",
    r"root_basis_type\s*=\s*'POD-FIXED'",
    r"group_basis_type\s*=\s*'PHYSICAL-ID'",
    r"LCMPUT\s*\(\s*kentry\(1\)\s*,\s*'SPOT-PHYS'",
    r"SNAPSHOT SPECTRUM COPY CHANGED",
    r"LCMPUT\s*\(\s*kpout\s*,\s*'POD-REC-ERR'\s*,\s*1\s*,\s*4\s*,"
    r"\s*rec_error_old",
    r"LCMPUT\s*\(\s*kpout\s*,\s*'PHYS-SNAP'\s*,\s*1\s*,\s*4\s*,"
    r"\s*equiv_group",
    r"invariant_tolerance\s*=\s*invariant_roundoff_factor\s*\*\s*machine_epsilon",
    r"ortho_group\s*>\s*invariant_tolerance.*?XABORT",
    r"complete_group\s*>\s*invariant_tolerance.*?XABORT",
    r"equiv_group\s*>\s*invariant_tolerance.*?XABORT",
    r"norm_ref\s*==\s*0\.0d0.*?equiv_group\s*=\s*0\.0d0",
)
for pattern in required:
    if re.search(pattern, source, re.IGNORECASE | re.DOTALL) is None:
        violations.append(f"SPOPHYS is missing contract pattern {pattern!r}")

if re.search(r"nmode_old\s*>\s*nsnap", source, re.IGNORECASE):
    violations.append("SPOPHYS retains the obsolete NMODE <= NSNAP admission limit")

for pattern in (r"/Users/", r"/private/tmp", r"validation/artifacts"):
    if re.search(pattern, source, re.IGNORECASE):
        violations.append(f"SPOPHYS contains a local diagnostic path matching {pattern!r}")

assembly_required = (
    r"LCMGET\s*\(\s*IPBASIS\s*,\s*'SPOT-PHYS'\s*,\s*IPHYS\s*\)",
    r"RANK_POD\.NE\.NREG2D.*?PHYSICAL BASIS MUST HAVE FULL RADIAL RANK",
    r"GBTYPE\.NE\.'PHYSICAL-ID'.*?XABORT",
    r"PHYSICAL IDENTITY BASIS MISMATCH",
    r"LCMPTC\s*\(\s*KPSYS\s*,\s*'SPOT-BTYPE'\s*,\s*12\s*,\s*GBTYPE",
    r"LCMPUT\s*\(\s*IPSYS\s*,\s*'SPOT-PHYS'\s*,\s*1\s*,\s*1\s*,\s*IPHYS",
    r"LCMPUT\s*\(\s*IPSYS\s*,\s*'POD-RANK-OLD'",
)
for pattern in assembly_required:
    if re.search(pattern, assembly, re.IGNORECASE | re.DOTALL) is None:
        violations.append(f"SPOASM is missing physical-basis round-trip pattern {pattern!r}")

solver_required = (
    r"diagonal_basis\s*=\s*nmode\s*==\s*nreg2d",
    r"mode_separable\s*=\s*\.true\.",
    r"call\s+boundary_solve\s*\(\s*a\s*,\s*a\s*,",
    r"call\s+translation_solve\s*\(\s*a\s*,\s*a\s*,",
    r"local_state\s*=\s*\(\s*last_mode-first_mode\+1\s*\)\s*\*\s*npq",
)
for solver_name, solver in solvers.items():
    for pattern in solver_required:
        if re.search(pattern, solver, re.IGNORECASE | re.DOTALL) is None:
            violations.append(
                f"{solver_name} is missing physical separability pattern {pattern!r}"
            )

ignored = subprocess.run(
    ["git", "check-ignore", "-q", "src/SPOPHYS.f90"],
    cwd=ROOT,
    check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
).returncode
if ignored == 0:
    violations.append("src/SPOPHYS.f90 is still ignored")

if violations:
    raise SystemExit("SPOPHYS CONTRACT FAIL:\n" + "\n".join(violations))

print(
    "SPOPHYS CONTRACT PASS: trackable diagnostic registration, POD-FIXED root "
    "lifecycle, physical provenance, separated POD/coordinate errors, preserved "
    "snapshot spectra, zero-snapshot handling, SPOASM round-trip provenance, "
    "separable physical transport, and fail-closed roundoff invariants are present."
)

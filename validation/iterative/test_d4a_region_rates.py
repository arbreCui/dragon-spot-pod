#!/usr/bin/env python3
"""Short synthetic checks only; no archived input, transport, or acceptance gate."""

import argparse
import csv
import io
from pathlib import Path
import platform
import subprocess
import tempfile


FLAGS = (
    "-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror "
    "-Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math"
).split()
BAD_CASES = {
    "bad_key": "KEYFLX INDEX OUT OF RANGE",
    "duplicate_key": "DUPLICATE REGION KEYFLX INDEX",
    "bad_material": "INCONSISTENT SIX-MATERIAL SNAPSHOT OFFSETS",
    "bad_volume": "VOLUME MUST BE FINITE AND POSITIVE",
    "nan_flux": "NON-FINITE FLUX UNKNOWN",
    "flux64_type": "FLUX MUST CONTAIN NUNK REAL32 VALUES",
    "nusigf_shape": "NUSIGF MUST BE REAL32 WITH MIXTURE-FASTEST NMIX*NFIS LAYOUT",
    "nusigf_type": "NUSIGF MUST BE REAL32 WITH MIXTURE-FASTEST NMIX*NFIS LAYOUT",
    "extra_fissile": "NONFUEL MATERIAL HAS NONZERO NUSIGF",
    "missing_fissile": "FISSILE MATERIALS MUST INCLUDE 4,10,16",
    "bad_dimensions": "INCONSISTENT D4-A FLUX/TRACK/MACROLIB DIMENSIONS",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(command, cwd, *, check=True):
    return subprocess.run(
        [str(arg) for arg in command], cwd=cwd, timeout=10,
        capture_output=True, text=True, check=check,
    )


def check_good(result, output):
    require(result.returncode == 0, result.stdout + result.stderr)
    own = [line.removeprefix("D4A-REGION NU-FISSION-FRACTIONS")
           for line in result.stdout.splitlines()
           if line.startswith("D4A-REGION NU-FISSION-FRACTIONS")]
    reference = [line.removeprefix("SPORATE NU-FISSION-FRACTIONS")
                 for line in result.stdout.splitlines()
                 if line.startswith("SPORATE NU-FISSION-FRACTIONS")]
    require(len(own) == 1 and own == reference, "SPORATE E16.8 mismatch")
    rows = list(csv.DictReader(io.StringIO(output.read_text())))
    # Exact integer fixture formula: V=r+f, FLUX[KEYFLX]=g+i,
    # and the two NUSIGF components sum to 3*g+2*f. FLUX64 is twice FLUX.
    expected = {
        (r, f): sum((r + f) * (g + (r - 1) * 3 + f) * (3 * g + 2 * f)
                    for g in range(1, 371))
        for r in range(1, 26) for f in range(1, 4)
    }
    total = sum(expected.values())
    keys = [(int(row["radial_region"]), int(row["floor"])) for row in rows]
    require(len(rows) == 75 and set(keys) == set(expected), "Incomplete/duplicate CSV regions")
    for row, (r, f) in zip(rows, keys):
        require(int(row["material"]) == 4 + (f - 1) * 6, "Material mismatch")
        require(float(row["volume"]) == r + f, "Volume mismatch")
        require(float(row["nu_fission_rate"]) == expected[r, f], "Integer-reference rate mismatch")
        require(float(row["global_fraction"]) == expected[r, f] / total, "Global fraction mismatch")


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exporter", type=Path, default=here / "export_d4a_region_rates",
                        help="already-built read-only exporter")
    args = parser.parse_args()
    exporter = args.exporter.resolve()
    require(exporter.is_file(), "Build export_d4a_region_rates first, or supply --exporter.")
    root = here.parent.parent
    ganlib = root / "Ganlib" / "lib" / f"{platform.system()}_{platform.machine()}"
    with tempfile.TemporaryDirectory(prefix="d4a-region-tests-") as temporary:
        work = Path(temporary)
        fixture = work / "fixture"
        run(["gfortran", *FLAGS, "-I", ganlib / "modules",
             here / "test_d4a_region_rates.f90", ganlib / "libGanlib.a",
             "-lstdc++", "-o", fixture], work)
        for mode in ("good", *BAD_CASES):
            case = work / mode
            case.mkdir()
            run([fixture, mode], case)
            command = [exporter, "flux.xsm", "track.xsm", "macro.xsm", "rates.csv"]
            result = run(command, case, check=False)
            output = case / "rates.csv"
            if mode == "good":
                check_good(result, output)
                before = output.read_bytes()
                repeated = run(command, case, check=False)
                require(repeated.returncode != 0 and "REFUSING TO OVERWRITE" in repeated.stderr,
                        "Existing output was not rejected")
                require(output.read_bytes() == before, "Existing output changed")
                print("good: 75 exact rates/fractions; SPORATE E16.8 identical; overwrite rejected")
            else:
                require(result.returncode != 0 and BAD_CASES[mode] in result.stderr,
                        f"{mode}: wrong rejection: {result.stdout}{result.stderr}")
                require(not output.exists(), f"{mode}: invalid input published CSV")
                print(f"{mode}: expected rejection")
    print("D4A REGION SYNTHETIC CHECKS COMPLETE (not a physics/convergence acceptance)")


if __name__ == "__main__":
    main()

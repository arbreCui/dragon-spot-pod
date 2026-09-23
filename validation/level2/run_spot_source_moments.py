#!/usr/bin/env python3
"""Build only temporary test objects; never launch a transport solver."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    arch = f"{platform.system()}_{platform.machine()}"
    dragon = root / "lib" / arch
    ganlib = root / "Ganlib/lib" / arch
    libraries = [dragon / "libDragon.a", root / "Trivac/lib" / arch / "libTrivac.a",
                 root / "Utilib/lib" / arch / "libUtilib.a", ganlib / "libGanlib.a"]
    protected = libraries + [p for p in (root / "bin" / arch / "Dragon",
                                         root / "release/Dragon") if p.exists()]
    before = {p: digest(p) for p in protected}
    compiler = os.environ.get("FC", "gfortran")
    flags = ["-O0", "-g", "-fcheck=all", "-ffp-contract=off", "-fno-fast-math"]
    includes = ["-I" + str(ganlib / "modules"), "-I" + str(dragon / "modules")]
    try:
        with tempfile.TemporaryDirectory(prefix="spot-source-moments-") as tmp:
            work = Path(tmp)
            objects = []
            for name in ("FLU2DR", "FLU2DR64"):
                obj = work / (name + ".o")
                subprocess.run([compiler, *flags, *includes, "-J" + tmp, "-c",
                                str(root / "src" / (name + ".f")), "-o", str(obj)],
                               cwd=work, check=True, timeout=10)
                objects.append(obj)
            exe = work / "source_moments"
            subprocess.run([compiler, *flags, *includes, "-J" + tmp,
                            str(root / "validation/level2/test_spot_source_moments.f90"),
                            *map(str, objects), *map(str, libraries), "-lstdc++",
                            "-o", str(exe)], cwd=work, check=True, timeout=10)
            for precision, door in (("32", "SPOT"), ("64", "SPOT"), ("32", "MCCG")):
                for path in ("scalar", "vector"):
                    for spectrum in ("down", "thermal"):
                        result = subprocess.run([str(exe), precision, door, path, spectrum],
                                                cwd=work, check=False, text=True,
                                                capture_output=True, timeout=10)
                        if result.returncode:
                            print(result.stdout, end="", file=sys.stderr)
                            print(result.stderr, end="", file=sys.stderr)
                            result.check_returncode()
                        if "PASS source moments:" not in result.stdout:
                            raise RuntimeError("missing source-moment PASS marker")
                        print(result.stdout.strip())
    finally:
        for path, expected in before.items():
            if digest(path) != expected:
                raise RuntimeError(f"protected executable/library changed: {path}")
    print("SOURCE-MOMENT REGRESSION PASS: 12 cases; protected files unchanged")


if __name__ == "__main__":
    main()

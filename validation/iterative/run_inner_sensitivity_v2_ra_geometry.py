#!/usr/bin/env python3
"""Run the read-only Stage-4 v2 R_a geometry diagnostic."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
SOURCE = ITERATIVE / "check_inner_sensitivity_v2_ra_geometry_xsm.f90"
GANLIB_DIR = ROOT / "Ganlib" / "src"
GANLIB_MODULE = GANLIB_DIR / "ganlib.mod"
GANLIB_LIBRARY = GANLIB_DIR / "libGanlib.a"

INPUTS = (
    (
        "x0.xsm",
        ROOT / "validation" / "artifacts" / "iterative-map1"
        / "state0_axial.xsm",
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb",
    ),
    (
        "x2h.xsm",
        ROOT / "validation" / "artifacts"
        / "inner-sensitivity-v2-capture-898ffc7" / "state1_axial.xsm",
        "34928aca2cbc8ac7e61966919e8ebbf1c2cb0cf496cde3acfb3d489a2c46bf73",
    ),
    (
        "xh.xsm",
        ROOT / "validation" / "artifacts" / "iterative-map1"
        / "state1_axial.xsm",
        "2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484",
    ),
)

DEPENDENCY_HASHES = {
    GANLIB_MODULE: (
        "9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0"
    ),
    GANLIB_LIBRARY: (
        "204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c"
    ),
}

EXPECTED_OUTPUT_SHA256 = (
    "aba4db91e0bbb99e5fd2d305facdc21d663e4dc3b53e345ed490b4bc928c47bb"
)

FORBIDDEN_MUTATION = re.compile(
    rb"\b(?:LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
    re.IGNORECASE,
)
FORBIDDEN_SOLVER = re.compile(
    rb"SPOASM|SPOPOD|SPOT1P|SPOFSRC|SPOFCHK|SPOGBAL|SPOPROJ|"
    rb"SPOSTATE|SPOXCONV|Dragon",
    re.IGNORECASE,
)
FORBIDDEN_SOURCE_SOLVER = re.compile(
    rb"\b(?:call|use)\s+(?:SPOASM|SPOPOD|SPOT1P|SPOFSRC|SPOFCHK|"
    rb"SPOGBAL|SPOPROJ|SPOSTATE|SPOXCONV|Dragon)\b",
    re.IGNORECASE,
)


class GeometryError(RuntimeError):
    """Fail-closed diagnostic error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GeometryError(message)


def require_regular(path: Path, label: str, *, executable: bool = False) -> Path:
    try:
        status = path.lstat()
    except FileNotFoundError as exc:
        raise GeometryError(f"missing {label}: {path}") from exc
    require(stat.S_ISREG(status.st_mode), f"{label} is not a regular file")
    require(not path.is_symlink(), f"{label} must not be a symlink")
    if executable:
        require(os.access(path, os.X_OK), f"{label} is not executable")
    return path.resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_hash(path: Path, expected: str, label: str) -> None:
    resolved = require_regular(path, label)
    require(sha256(resolved) == expected, f"frozen input hash differs: {label}")


def run_checked(command: list[str], *, cwd: Path) -> bytes:
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        completed.returncode == 0,
        "command failed: "
        + " ".join(command)
        + ("\n" + completed.stderr.decode("utf-8", "replace")
           if completed.stderr else ""),
    )
    require(not completed.stderr, "command produced stderr: " + " ".join(command))
    return completed.stdout


def verify_frozen_inputs() -> None:
    for short_name, path, expected in INPUTS:
        verify_hash(path, expected, short_name)
    for path, expected in DEPENDENCY_HASHES.items():
        verify_hash(path, expected, path.name)


def compile_checker(
    compiler: str,
    work: Path,
    optimization: str,
    target_name: str,
) -> Path:
    target = work / target_name
    flags = [
        compiler,
        "-std=f2008",
        optimization,
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wno-compare-reals",
        "-fcheck=all",
        "-ffp-contract=off",
        "-fno-fast-math",
        "-I",
        str(GANLIB_DIR),
        str(SOURCE),
        str(GANLIB_LIBRARY),
        "-lstdc++",
        "-o",
        str(target),
    ]
    run_checked(flags, cwd=ROOT)
    return require_regular(target, target_name, executable=True)


def verify_binary(binary: Path, work: Path) -> None:
    symbols = run_checked(["nm", str(binary)], cwd=work)
    require(re.search(rb"lcmop", symbols, re.IGNORECASE) is not None, "LCMOP absent")
    require(
        FORBIDDEN_SOLVER.search(symbols) is None,
        f"{binary.name} links a production solver symbol",
    )


def validate_output(output: bytes) -> None:
    require(
        hashlib.sha256(output).hexdigest() == EXPECTED_OUTPUT_SHA256,
        "checker output hash differs",
    )
    try:
        text = output.decode("ascii")
    except UnicodeDecodeError as exc:
        raise GeometryError("checker output is not ASCII") from exc
    lines = text.splitlines()
    prefix = "INNER-SENSITIVITY-V2 RA-GEOMETRY "
    require(len(lines) == 402, "checker output line census differs")
    require(
        all(line.startswith(prefix) for line in lines),
        "checker output prefix differs",
    )
    plane_pattern = re.compile(r".* RA-GEOMETRY PLANE ([1-3]) .*")
    group_pattern = re.compile(r".* RA-GEOMETRY GROUP ([0-9]+) .*")
    plane_indices = [
        int(match.group(1))
        for line in lines
        if (match := plane_pattern.fullmatch(line)) is not None
    ]
    group_indices = [
        int(match.group(1))
        for line in lines
        if (match := group_pattern.fullmatch(line)) is not None
    ]
    require(plane_indices == [1, 2, 3], "plane output order differs")
    require(
        group_indices == list(range(1, 371)),
        "group output order differs",
    )
    required_fragments = (
        "GLOBAL NOUT-NORM2 0x3DEF2965794487DC",
        "GLOBAL NIN-NORM2 0x3DF0049209708CAC",
        "GLOBAL V-NORM2 0x3D5AB404C9FA1891",
        "GLOBAL CROSS-U-E 0xBDEF9297C4E05217",
        "GLOBAL COS-U-E 0xBFEFFA05B4D445A1",
        "GLOBAL PARALLEL-BETA 0xBFF03603613BD3BB",
        "GLOBAL ORTH-NORM2 0x3D57EDC4DA2DA144",
        "GLOBAL ORTH-REL-U 0x3FA3D409224E4EA5",
        "GLOBAL DELTA2-POST 0x3DAF61EA2CD57AC0",
        "GLOBAL DELTA2-CELL-FOLD 0x3DAF61EA2CD57B76",
        "GLOBAL DELTA2-PLANE-FOLD 0x3DAF61EA2CD57B6C",
        "GLOBAL DELTA2-GROUP-FOLD 0x3DAF61EA2CD57B6D",
        "RA-BITS ROUT-2H 0x3EF7A721405AFAAF "
        "RIN 0x3EF7FB7522398B1F ROUT-H 0x3EAEF702EB99D736",
        "PLANE 1 NOUT-NORM2 0x3DE0190D3941789A",
        "DELTA2 0xBD75E92E6E876417",
        "PLANE 2 NOUT-NORM2 0x3D4E671038CDD2B1",
        "DELTA2 0xBD6090808B86C6AF",
        "PLANE 3 NOUT-NORM2 0x3DDE117CF7E9B79A",
        "DELTA2 0x3DB1940C01AF6A2D",
        "PLANE-DELTA2-SIGNS NEG 2 ZERO 0 POS 1 TOTAL 3",
        "GROUP-DELTA2-SIGNS NEG 42 ZERO 0 POS 328 TOTAL 370",
        "GROUP-DELTA2-MAXABS GROUP 80 BITS 0x3D5AA96EBA84B12A",
    )
    for fragment in required_fragments:
        require(fragment in text, f"missing frozen output fragment: {fragment}")
    require(
        lines[-1] == "INNER-SENSITIVITY-V2 RA-GEOMETRY COMPLETE",
        "checker completion marker differs",
    )


def run_binary(binary: Path, work: Path) -> bytes:
    output = run_checked(
        [str(binary), "x0.xsm", "x2h.xsm", "xh.xsm"],
        cwd=work,
    )
    validate_output(output)
    return output


def main() -> None:
    source = require_regular(SOURCE, SOURCE.name)
    source_bytes = source.read_bytes()
    require(b"use GANLIB" in source_bytes, "checker is not Ganlib-based")
    require(
        FORBIDDEN_MUTATION.search(source_bytes) is None,
        "checker source contains Ganlib mutation",
    )
    require(
        FORBIDDEN_SOURCE_SOLVER.search(source_bytes) is None,
        "checker source contains a production solver symbol",
    )
    verify_frozen_inputs()

    compiler = shutil.which("gfortran")
    require(compiler is not None, "gfortran is unavailable")
    with tempfile.TemporaryDirectory(prefix="spot-s4v2-ra-geometry.") as raw:
        work = Path(raw)
        for short_name, source_path, _expected in INPUTS:
            (work / short_name).symlink_to(source_path.resolve())
        checked = compile_checker(compiler, work, "-O0", "check_ra_o0")
        optimized = compile_checker(compiler, work, "-O2", "check_ra_o2")
        verify_binary(checked, work)
        verify_binary(optimized, work)
        output_checked = run_binary(checked, work)
        output_optimized = run_binary(optimized, work)
        require(
            output_checked == output_optimized,
            "checked and optimized outputs differ",
        )

    sys.stdout.buffer.write(output_checked)
    print("INNER-SENSITIVITY-V2 RA-GEOMETRY RUNNER PASS: BUILDS=2")
    print("INNER-SENSITIVITY-V2 RA-GEOMETRY DRAGON-RUNS=0")


if __name__ == "__main__":
    try:
        main()
    except (GeometryError, OSError) as exc:
        print(
            "INNER-SENSITIVITY-V2 RA-GEOMETRY RUNNER FAIL: " + str(exc),
            file=sys.stderr,
        )
        raise SystemExit(2)

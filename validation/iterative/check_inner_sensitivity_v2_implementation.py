#!/usr/bin/env python3
"""Static fail-closed audit of the Stage-4 v2 implementation."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
RECEIPT = ITERATIVE / "inner_sensitivity_v2_implementation.sha256"
IMPLEMENTATION_PATHS = (
    "validation/iterative/inner_sensitivity_v2_coarse_map.x2m",
    "validation/iterative/check_one_map_xsm.f90",
    "validation/iterative/check_inner_sensitivity_xsm.f90",
    "validation/iterative/check_inner_sensitivity_v2_log.py",
    "validation/iterative/test_inner_sensitivity_v2_log.py",
    "validation/iterative/check_inner_sensitivity_v2_result.py",
    "validation/iterative/test_inner_sensitivity_v2_result.py",
    "validation/iterative/run_inner_sensitivity_v2_process.py",
    "validation/iterative/test_inner_sensitivity_v2_process.py",
    "validation/iterative/run_inner_sensitivity_v2.py",
    "validation/iterative/test_inner_sensitivity_v2_runner.py",
    "validation/iterative/inner_sensitivity_v2_implementation.md",
    "validation/iterative/run_inner_sensitivity_v2_tests.sh",
    "validation/iterative/check_inner_sensitivity_v2_implementation.py",
    "validation/iterative/check_inner_sensitivity_v2_balance_xsm.f90",
)
SHA_ROW = re.compile(r"([0-9a-f]{64})  ([^\t]+)")


def fail(message: str) -> None:
    print(
        "INNER-SENSITIVITY-V2 IMPLEMENTATION FAIL: " + message,
        file=sys.stderr,
    )
    raise SystemExit(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"invalid {relative}")
    raw = path.read_bytes()
    require(
        raw and b"\0" not in raw and b"\r" not in raw,
        f"noncanonical {relative}",
    )
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError:
        fail(f"non-ASCII implementation file: {relative}")


def exactly(source: str, pattern: str, count: int, owner: str) -> None:
    actual = len(re.findall(pattern, source, re.MULTILINE))
    require(actual == count, f"{owner}: expected {count}, found {actual}")


def verify_receipt() -> None:
    raw = text(
        "validation/iterative/inner_sensitivity_v2_implementation.sha256"
    )
    require(raw.endswith("\n"), "implementation receipt lacks final newline")
    lines = raw.splitlines()
    require(
        len(lines) == len(IMPLEMENTATION_PATHS),
        "implementation receipt census differs",
    )
    for line, expected in zip(lines, IMPLEMENTATION_PATHS, strict=True):
        match = SHA_ROW.fullmatch(line)
        require(match is not None, "malformed implementation receipt row")
        digest, relative = match.groups()
        require(relative == expected, "implementation receipt order differs")
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"invalid {relative}")
        require(sha256(path) == digest, f"receipt hash differs: {relative}")


def verify_deck() -> None:
    deck = text(IMPLEMENTATION_PATHS[0])
    exactly(deck, r"^REAL coarse_eps := 1\.0E-6 ;$", 1, "coarse tolerance")
    exactly(deck, r"\bSpotRefFS SNAP TRACK TRACK_f\b", 1, "radial map")
    exactly(deck, r"^AX_CURRENT := FLU:", 1, "returned axial solve")
    exactly(deck, r"^SNAP := SPOLEAK:", 2, "direct leakage updates")
    exactly(deck, r"^SNAP := SPOPROJ:.*$", 1, "fixed projection")
    exactly(deck, r"^  <<k0>> <<coarse_eps>> ;$", 1, "radial tolerance")
    exactly(
        deck,
        r"EXTE 500 <<coarse_eps>>\n"
        r"  UNKT <<coarse_eps>> THER <<coarse_eps>> ;",
        1,
        "axial tolerance",
    )
    exactly(
        deck,
        r"^AX_CURRENT := SPOXCONV: AX_CURRENT AX0_ARCH :: ;$",
        1,
        "coarse defect order",
    )
    exactly(deck, r"^SYS1_ARCH := SYSTEM_NEXT ;$", 1, "system archive")
    exactly(deck, r"^AX1_ARCH := AX_CURRENT ;$", 1, "axial archive")
    exactly(deck, r"^SNAP1_ARCH := SNAP ;$", 1, "snapshot archive")
    require("BASIS_REF := ASM:" not in deck, "deck rebuilds the POD basis")
    require("AX0_ARCH :=" not in deck, "deck overwrites frozen x0")
    require("WHILE" not in deck, "deck contains an outer loop")
    require("init_eps" not in deck, "deck contains initializer tolerance")
    require("2.5E-7" not in deck, "failed h/2 tolerance entered the deck")
    require("SPOGBAL" not in deck, "deck enters the unsafe SPOGBAL path")
    require("SPOT-GBAL" not in deck, "deck reads a production balance record")
    require(
        all(
            token not in deck.upper()
            for token in ("RELAX ", "DAMP ", "CLIP ", " FIT ")
        ),
        "deck contains an empirical stabilization control",
    )
    markers = (
        "STAGE4V2-COARSE-BEGIN",
        "STAGE4V2-COARSE-X0-REUSED",
        "STAGE4V2-COARSE-RADIAL-BEGIN",
        "STAGE4V2-COARSE-RADIAL-END",
        "STAGE4V2-COARSE-AXIAL-BEGIN",
        "STAGE4V2-COARSE-AXIAL-END",
        "STAGE4V2-COARSE-DOUT-2H",
        "STAGE4V2-COARSE-COMPLETE",
    )
    for marker in markers:
        exactly(deck, re.escape(marker), 1, marker)


def verify_fortran_checkers() -> None:
    one_map = text(IMPLEMENTATION_PATHS[1])
    pair = text(IMPLEMENTATION_PATHS[2])
    balance = text(IMPLEMENTATION_PATHS[14])
    forbidden = re.compile(
        r"\b(?:LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
        re.IGNORECASE,
    )
    require(forbidden.search(one_map) is None, "one-map checker mutates XSM")
    require(forbidden.search(pair) is None, "pair checker mutates XSM")
    require(forbidden.search(balance) is None, "balance checker mutates XSM")
    for token in (
        "'SPOT-LEAK1D'",
        "'SPOT-FS-K'",
        "'SPOT-FS-MIN'",
        "'SPOT-FS-QSUM'",
        "'SPOT-FS-RBAL'",
    ):
        require(token in one_map, f"one-map checker omits {token}")
    require("SPOT-GBAL" not in one_map, "one-map checker trusts stored balance")
    for token in (
        "'MATCOD'",
        "'KEYFLX'",
        "'AREA2D'",
        "'DRAGON-TXSC'",
        "'DRAGON-S0XSC'",
        "'RADIAL-OP'",
        "'POD-BASIS'",
        "'NUSIGF'",
        "'CHI'",
        "'SCAT00'",
        "PHYSICAL-SOURCE REBUILT",
        "GLOBAL/GROUP/GALERKIN-BITS",
        "LEGACY-ANCHOR BITWISE PASS",
    ):
        require(token in balance, f"balance checker omits {token}")
    require(
        "SPOT-GBAL-MAX" not in balance,
        "balance checker contains an overlong Ganlib key",
    )
    for owner, source in (
        ("one-map", one_map),
        ("pair", pair),
        ("balance", balance),
    ):
        keys = re.findall(
            r"\bLCM(?:GET|LEN|GTC|GID)\s*\(\s*[^,]+,\s*'([^']+)'",
            source,
            re.IGNORECASE,
        )
        require(keys, f"{owner} checker has no auditable Ganlib keys")
        require(
            all(len(key) <= 12 for key in keys),
            f"{owner} checker has an overlong Ganlib literal",
        )
    require(
        "call recompute_defect(x1_h2,x1_h,din)" in pair,
        "v2 D_in order is not D(x1_h,x1_2h)",
    )
    require(
        "call recompute_defect(x1_h,x1_h2,din)" in pair,
        "legacy D_in path was not preserved",
    )
    for token in (
        "V2-2H",
        "DOUT-H-BITS",
        "DOUT-2H-BITS",
        "DIN-BITS",
        "DIN-VS-DOUT-2H",
    ):
        require(token in pair, f"pair checker omits {token}")


def verify_python() -> None:
    paths = (
        IMPLEMENTATION_PATHS[3],
        IMPLEMENTATION_PATHS[4],
        IMPLEMENTATION_PATHS[5],
        IMPLEMENTATION_PATHS[6],
        IMPLEMENTATION_PATHS[7],
        IMPLEMENTATION_PATHS[8],
        IMPLEMENTATION_PATHS[9],
        IMPLEMENTATION_PATHS[10],
        IMPLEMENTATION_PATHS[13],
    )
    sources = {}
    for relative in paths:
        source = text(relative)
        try:
            ast.parse(source, filename=relative)
        except SyntaxError as exc:
            fail(f"invalid Python syntax in {relative}: {exc}")
        sources[relative] = source

    log = sources[IMPLEMENTATION_PATHS[3]]
    for token in (
        "EXPECTED_TOLERANCE_BITS = 0x358637BD",
        "EXPECTED_MAXOUT = 500",
        "EXPECTED_MAXINR = 740",
        "== outer_total == inner_total == 4",
        "STATE",
        '"SPOGBAL" not in text',
    ):
        require(token in log, f"log checker omits {token}")

    result = sources[IMPLEMENTATION_PATHS[5]]
    require(
        'PROTOCOL_COMPONENTS = ("R_rho", "R_L", "D_L", "R_a")'
        in result,
        "result checker component set differs",
    )
    require("D_out_2h" in result or "dout_2h" in result, "coarse gate absent")
    require("inner < outer" in result, "strict component inequality absent")
    require("isclose" not in result and "allclose" not in result, "tolerance used")
    require(
        "QUALIFIED-ON-2H-TO-H-SCALE" in result,
        "qualified label differs",
    )
    require("git_blob" in result, "committed replay evidence is absent")
    require("os.path.samefile" in result, "replay inode separation is absent")

    process = sources[IMPLEMENTATION_PATHS[7]]
    for token in (
        "TIMEOUT_SECONDS = 120",
        "TERM_GRACE_SECONDS = 5",
        "signal.SIGTERM",
        "signal.SIGKILL",
        "start_new_session=True",
    ):
        require(token in process, f"bounded process wrapper omits {token}")

    runner = sources[IMPLEMENTATION_PATHS[9]]
    for token in (
        'default="preflight"',
        "spot-inner-sensitivity-v2-run-authorization-1",
        "capture-spent.json",
        'f"{mode}-spent.json"',
        '"PROCESS-RESERVED"',
        "automatic_replay",
        "DRAGON-RUNS 0",
        "PROCESS_WRAPPER",
        "verify_artifact_manifest",
        "published_inode",
        "LEDGER_RELATIVE",
        "verify_authorized_implementation",
        "require_authorization_postdates_capture",
        "capture_scientific_manifest_sha256",
        "capture_receipt_sha256",
        "rename_no_replace",
        "require_absent(output, \"output immediately before Dragon\")",
        "BALANCE_XSM_SOURCE",
        '"./check_balance"',
        '"balance_xsm_check.log"',
    ):
        require(token in runner, f"production runner omits {token}")
    require(
        "maximum_dragon_processes" in runner
        and "wall_clock_limit_seconds" in runner,
        "run budget gate is incomplete",
    )
    require("--ledger-dir" not in runner, "runner exposes a selectable ledger")
    require("os.rename(" not in runner, "runner uses replace-capable publication")


def verify_shell() -> None:
    script = ROOT / IMPLEMENTATION_PATHS[12]
    result = subprocess.run(
        ["sh", "-n", str(script)],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "test runner shell syntax is invalid")


def verify_protocol_freeze() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ITERATIVE / "check_inner_sensitivity_v2_protocol.py"),
            "--public-only",
        ],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "frozen v2 protocol check failed")


def main() -> None:
    verify_protocol_freeze()
    verify_receipt()
    verify_deck()
    verify_fortran_checkers()
    verify_python()
    verify_shell()
    print("INNER-SENSITIVITY-V2 IMPLEMENTATION PASS: DRAGON-RUNS=0")


if __name__ == "__main__":
    main()

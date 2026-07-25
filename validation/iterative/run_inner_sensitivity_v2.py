#!/usr/bin/env python3
"""Preflight, capture, or explicitly replay the frozen Stage-4 v2 map.

The default mode is preflight and starts no Dragon process.  Capture and
replay each require a separate committed authorization JSON and atomically
consume a permanent one-shot ledger entry before Dragon is started.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
PROTOCOL = ITERATIVE / "inner_sensitivity_v2_protocol.json"
PROTOCOL_CHECKER = ITERATIVE / "check_inner_sensitivity_v2_protocol.py"
IMPLEMENTATION_CHECKER = (
    ITERATIVE / "check_inner_sensitivity_v2_implementation.py"
)
IMPLEMENTATION_RECEIPT = (
    ITERATIVE / "inner_sensitivity_v2_implementation.sha256"
)
DECK = ITERATIVE / "inner_sensitivity_v2_coarse_map.x2m"
PROCESS_WRAPPER = ITERATIVE / "run_inner_sensitivity_v2_process.py"
LOG_CHECKER = ITERATIVE / "check_inner_sensitivity_v2_log.py"
RESULT_CHECKER = ITERATIVE / "check_inner_sensitivity_v2_result.py"
ONE_MAP_XSM_SOURCE = ITERATIVE / "check_one_map_xsm.f90"
BALANCE_XSM_SOURCE = (
    ITERATIVE / "check_inner_sensitivity_v2_balance_xsm.f90"
)
PAIR_XSM_SOURCE = ITERATIVE / "check_inner_sensitivity_xsm.f90"
EXPECTED_PROTOCOL_SHA256 = (
    "8a870a85ffe7fd4eb53d9494bcf28acea2025f8f3d022579312cd34a22a1d88c"
)
EXPECTED_DRAGON_SHA256 = (
    "e4c61fa45ba0fe62be3a15e21785c5e27b9a3c10d727a02754d43d7c79ef2759"
)
LEDGER_RELATIVE = (
    "validation/artifacts/inner-sensitivity-v2-execution-ledger"
)
SCIENCE_FILES = (
    "basis_reference.xsm",
    "state0_axial.xsm",
    "state1_system.xsm",
    "state1_axial.xsm",
    "state1_snapshots.xsm",
)
CAPTURE_EVIDENCE_FILES = (
    "authorization.json",
    "balance_xsm_check.log",
    "coarse_xsm_check.log",
    "dragon.log",
    "input_manifest.sha256",
    "pair_xsm_check.log",
    "process_check.log",
    "raw_log_check.log",
    "result.json",
    "scientific_manifest.sha256",
)
FINE_HASHES = {
    "basis_reference.xsm": (
        "dc65467731947901393f9fb7114b7cd2e956a9992bb97db18e665b47e7446504"
    ),
    "state0_axial.xsm": (
        "0a54da1236f863a7574f17bc7d931f9a18629aceeb5f99ebfdb7dae29464fceb"
    ),
    "state1_system.xsm": (
        "fa693cbcc8a60f64521f6ad5be660c8d13414586f03da91506a01021ed5981c2"
    ),
    "state1_axial.xsm": (
        "2323a256002f1e6f75f5af72c31479b0f6a7bff561d401cee363dcf9fc6ff484"
    ),
    "state1_snapshots.xsm": (
        "1b5a0c98aba0f5b4f366b64a8157f4a104df0f89f4cdeafc60eb6ce7811018e1"
    ),
}
SEED_HASHES = {
    "initial_snapshots.xsm": (
        "37656f3269c59db9a5df59ac3686a6da65bc07afa051e2473ffbefadcb2c2b95"
    ),
    "initial_axial_track.xsm": (
        "101ba0ad64c91723fdeb002e62c6226347fcfaeff188e125d699d70e113febc7"
    ),
    "initial_axial_macrolib.xsm": (
        "2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a"
    ),
    "initial_radial_track.bin": (
        "f7b27cb4a5d37f903b93e49610e2daa2290d55c164e2ca0e73ccb8d22fe486b8"
    ),
}
PROCEDURE_HASHES = {
    "SpotRefFS.c2m": (
        "db763e8c013d9f753ae6eb635dc5490c6bb34b9f23ea211dd3b282b6ec031742"
    ),
    "SpotPlaneFS.c2m": (
        "69a2931c817d298a3af36f5e1f55760c58dd55229c73002b4b01d3a4797e27b5"
    ),
}
CAPTURE_AUTH_KEYS = (
    "schema",
    "protocol_sha256",
    "implementation_commit",
    "ledger_relative_path",
    "mode",
    "maximum_dragon_processes",
    "wall_clock_limit_seconds",
    "automatic_replay",
)
REPLAY_AUTH_KEYS = (
    "schema",
    "protocol_sha256",
    "implementation_commit",
    "ledger_relative_path",
    "mode",
    "capture_commit",
    "capture_scientific_manifest_sha256",
    "capture_receipt_sha256",
    "maximum_dragon_processes",
    "wall_clock_limit_seconds",
    "automatic_replay",
)


def fail(message: str) -> None:
    print("INNER-SENSITIVITY-V2 RUNNER FAIL: " + message, file=sys.stderr)
    raise SystemExit(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, owner: str, executable: bool = False) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    require(
        stat.S_ISREG(status.st_mode) and not stat.S_ISLNK(status.st_mode),
        f"{owner} is not a regular non-symlink file",
    )
    resolved = path.resolve(strict=True)
    if executable:
        require(os.access(resolved, os.X_OK), f"{owner} is not executable")
    return resolved


def require_directory(path: Path, owner: str) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    require(
        stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode),
        f"{owner} is not a regular non-symlink directory",
    )
    return path.resolve(strict=True)


def require_absent(path: Path, owner: str) -> None:
    try:
        path.lstat()
    except FileNotFoundError:
        return
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    fail(f"{owner} already exists")


def rename_no_replace(source: Path, target: Path) -> None:
    """Atomically publish SOURCE while refusing to replace TARGET."""

    require_absent(target, "publication target")
    libc = ctypes.CDLL(None, use_errno=True)
    source_raw = os.fsencode(source)
    target_raw = os.fsencode(target)
    if sys.platform == "darwin" and hasattr(libc, "renameatx_np"):
        rename = libc.renameatx_np
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            -2,
            source_raw,
            -2,
            target_raw,
            0x00000004,
        )
    elif sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
        rename = libc.renameat2
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            -100,
            source_raw,
            -100,
            target_raw,
            0x00000001,
        )
    else:
        fail("atomic no-replace publication is unavailable")
    if result != 0:
        error = ctypes.get_errno()
        fail(f"atomic publication failed: {os.strerror(error)}")


def validate_output_path(
    path: Path,
    mode: str,
    fine_dir: Path,
    seed_dir: Path,
    capture_dir: Path | None,
) -> Path:
    require(path.is_absolute(), "output directory must be absolute")
    artifact_root = require_directory(
        ROOT / "validation" / "artifacts",
        "artifact root",
    )
    parent = require_directory(path.parent, "output parent")
    require(parent == artifact_root, "output must be a direct artifact-root child")
    normalized = parent / path.name
    require(path == normalized, "output path is not canonical")
    require(
        re.fullmatch(
            rf"inner-sensitivity-v2-{mode}-[A-Za-z0-9][A-Za-z0-9._-]*",
            path.name,
        )
        is not None,
        "output name differs from the mode-specific artifact namespace",
    )
    protected = [fine_dir, seed_dir, ROOT / LEDGER_RELATIVE]
    if capture_dir is not None:
        protected.append(capture_dir)
    for item in protected:
        require(
            normalized != item.resolve(strict=False),
            f"output aliases protected path: {item.name}",
        )
    require_absent(normalized, "output directory")
    return normalized


def run_checked(
    command: list[str],
    *,
    cwd: Path = ROOT,
    output: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    if output is None:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    else:
        require(
            not output.exists() and not output.is_symlink(),
            f"refusing to overwrite {output.name}",
        )
        with output.open("xb") as stream:
            result = subprocess.run(
                command,
                cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=stream,
                stderr=subprocess.PIPE,
                check=False,
            )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        if output is None:
            stdout = result.stdout.decode("utf-8", errors="replace").strip()
            detail = "\n".join(item for item in (stdout, detail) if item)
        fail(
            "command failed"
            + (f": {detail}" if detail else "")
        )
    return result


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_json(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, indent=2) + "\n").encode("ascii")


def load_canonical_json(path: Path, owner: str) -> dict[str, Any]:
    require_regular(path, owner)
    raw = path.read_bytes()
    require(
        raw and b"\0" not in raw and b"\r" not in raw,
        f"{owner} is empty or noncanonical",
    )
    try:
        text = raw.decode("ascii")
        data = json.loads(text, object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid {owner}: {exc}")
    require(isinstance(data, dict), f"{owner} must be a JSON object")
    require(raw == canonical_json(data), f"{owner} is not canonical JSON")
    return data


def git_bytes(commit: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        result.returncode == 0,
        f"{relative} is unavailable from commit {commit}",
    )
    return result.stdout


def git_bytes_optional(commit: str, relative: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    require(
        result.returncode == 128,
        f"cannot inspect {relative} at commit {commit}",
    )
    return None


def require_head_identity(path: Path, owner: str) -> None:
    resolved = require_regular(path, owner)
    try:
        relative = resolved.relative_to(ROOT).as_posix()
    except ValueError:
        fail(f"{owner} is outside the repository")
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", relative],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    require(tracked.returncode == 0, f"{owner} is not tracked")
    require(
        git_bytes("HEAD", relative) == path.read_bytes(),
        f"{owner} differs from HEAD",
    )


def verify_implementation_head() -> None:
    require_head_identity(IMPLEMENTATION_RECEIPT, "implementation receipt")
    rows = IMPLEMENTATION_RECEIPT.read_text(encoding="ascii").splitlines()
    require(rows, "implementation receipt is empty")
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\t]+)", row)
        require(match is not None, "malformed implementation receipt")
        digest, relative = match.groups()
        require(
            not Path(relative).is_absolute()
            and ".." not in Path(relative).parts,
            "unsafe implementation receipt path",
        )
        path = ROOT / relative
        require_head_identity(path, f"implementation file {relative}")
        require(
            sha256_file(path) == digest,
            f"implementation receipt hash differs: {relative}",
        )


def verify_authorized_implementation(commit: str) -> None:
    require_commit_ancestor(commit, "authorized implementation commit")
    receipt_relative = IMPLEMENTATION_RECEIPT.relative_to(ROOT).as_posix()
    current_receipt = IMPLEMENTATION_RECEIPT.read_bytes()
    require(
        git_bytes(commit, receipt_relative) == current_receipt,
        "authorized implementation receipt differs from the current freeze",
    )
    for row in current_receipt.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\t]+)", row)
        require(match is not None, "malformed implementation receipt")
        digest, relative = match.groups()
        current = ROOT / relative
        require_regular(current, f"authorized implementation file {relative}")
        current_bytes = current.read_bytes()
        require(
            hashlib.sha256(current_bytes).hexdigest() == digest,
            f"authorized implementation hash differs: {relative}",
        )
        require(
            git_bytes(commit, relative) == current_bytes,
            f"authorized implementation blob differs: {relative}",
        )


def verify_inputs(
    dragon: Path,
    fine_dir: Path,
    seed_dir: Path,
) -> None:
    require(
        sha256_file(require_regular(dragon, "Dragon", executable=True))
        == EXPECTED_DRAGON_SHA256,
        "Dragon hash differs from the frozen executable",
    )
    for name, digest in FINE_HASHES.items():
        path = fine_dir / name
        require_regular(path, f"fine artifact {name}")
        require(sha256_file(path) == digest, f"fine hash differs: {name}")
    for name, digest in SEED_HASHES.items():
        path = seed_dir / name
        require_regular(path, f"seed artifact {name}")
        require(sha256_file(path) == digest, f"seed hash differs: {name}")
    for name, digest in PROCEDURE_HASHES.items():
        path = ROOT / "data" / name
        require_regular(path, f"procedure {name}")
        require(
            sha256_file(path) == digest,
            f"procedure hash differs: {name}",
        )


def compile_checkers(
    work: Path,
    fc: str,
    ganlib_lib: Path,
    ganlib_mod: Path,
) -> None:
    compiler = shutil.which(fc)
    require(compiler is not None, f"Fortran compiler is unavailable: {fc}")
    require_regular(ganlib_lib, "Ganlib library")
    require_regular(ganlib_mod / "ganlib.mod", "Ganlib module")
    forbidden_mutation = re.compile(
        rb"\b(?:LCMPUT|LCMPTC|LCMPPD|LCMLID|LCMLIL|LCMEQU|LCMDEL)\b",
        re.IGNORECASE,
    )
    for source in (
        ONE_MAP_XSM_SOURCE,
        BALANCE_XSM_SOURCE,
        PAIR_XSM_SOURCE,
    ):
        require_regular(source, source.name)
        require(
            forbidden_mutation.search(source.read_bytes()) is None,
            f"XSM checker contains LCM mutation: {source.name}",
        )
    flags = [
        compiler,
        "-std=f2008",
        "-O0",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wno-compare-reals",
        "-fcheck=all",
        "-ffp-contract=off",
        "-fno-fast-math",
        "-I",
        str(ganlib_mod),
    ]
    targets = (
        (ONE_MAP_XSM_SOURCE, work / "check_one"),
        (BALANCE_XSM_SOURCE, work / "check_balance"),
        (PAIR_XSM_SOURCE, work / "check_pair"),
    )
    for source, target in targets:
        run_checked(
            flags
            + [
                str(source),
                str(ganlib_lib),
                "-lstdc++",
                "-o",
                str(target),
            ]
        )
        require_regular(target, target.name, executable=True)
        nm = run_checked(["nm", str(target)]).stdout
        require(re.search(rb"lcmop", nm, re.IGNORECASE) is not None, "LCMOP absent")
        require(
            re.search(
                rb"SPOASM|SPOPOD|SPOT1P|SPOFSRC|SPOFCHK|SPOGBAL|"
                rb"SPOPROJ|SPOSTATE|SPOXCONV|Dragon",
                nm,
                re.IGNORECASE,
            )
            is None,
            f"{target.name} links production solver symbols",
        )


def copy_inputs(work: Path, fine_dir: Path, seed_dir: Path) -> None:
    for name in SEED_HASHES:
        shutil.copyfile(seed_dir / name, work / name)
    for name in PROCEDURE_HASHES:
        shutil.copyfile(ROOT / "data" / name, work / name)
    shutil.copyfile(fine_dir / "basis_reference.xsm", work / "basis_reference.xsm")
    shutil.copyfile(fine_dir / "state0_axial.xsm", work / "state0_axial.xsm")
    fine = work / "fine"
    fine.mkdir()
    shutil.copyfile(fine_dir / "state0_axial.xsm", fine / "x0.xsm")
    shutil.copyfile(fine_dir / "state1_axial.xsm", fine / "x1.xsm")
    shutil.copyfile(fine_dir / "state1_snapshots.xsm", fine / "snap1.xsm")
    shutil.copyfile(DECK, work / "case.x2m")
    (work / "tmp").mkdir()


def write_science_manifest(work: Path) -> Path:
    path = work / "scientific_manifest.sha256"
    require(not path.exists(), "scientific manifest already exists")
    rows = []
    for name in SCIENCE_FILES:
        target = work / name
        require_regular(target, f"scientific output {name}")
        rows.append(f"{sha256_file(target)}  {name}")
    path.write_text("\n".join(rows) + "\n", encoding="ascii")
    return path


def write_input_manifest(
    work: Path,
    dragon: Path,
    ganlib_lib: Path,
    ganlib_mod: Path,
    authorization: Path | None,
) -> None:
    entries = [
        ("Dragon", dragon),
        ("protocol", PROTOCOL),
        ("implementation-receipt", IMPLEMENTATION_RECEIPT),
        ("deck", DECK),
        ("Ganlib-library", ganlib_lib),
        ("Ganlib-module", ganlib_mod / "ganlib.mod"),
        ("check-one-binary", work / "check_one"),
        ("check-balance-binary", work / "check_balance"),
        ("check-pair-binary", work / "check_pair"),
    ]
    if authorization is not None:
        entries.append(("authorization", authorization))
    rows = [
        f"{sha256_file(require_regular(path, label))}  {label}"
        for label, path in entries
    ]
    (work / "input_manifest.sha256").write_text(
        "\n".join(rows) + "\n",
        encoding="ascii",
    )


def write_artifact_manifest(work: Path) -> None:
    path = work / "artifact_manifest.sha256"
    unexpected_directories = [
        item.name for item in work.iterdir() if item.is_dir()
    ]
    require(
        not unexpected_directories,
        f"unpruned artifact directories: {unexpected_directories}",
    )
    require(
        not any(item.is_symlink() for item in work.iterdir()),
        "artifact contains a symlink",
    )
    names = sorted(
        item.name
        for item in work.iterdir()
        if item.is_file()
        and not item.is_symlink()
        and item.name != path.name
    )
    rows = [f"{sha256_file(work / name)}  {name}" for name in names]
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def verify_artifact_manifest(root: Path) -> None:
    directory = require_directory(root, "published artifact")
    manifest = directory / "artifact_manifest.sha256"
    require_regular(manifest, "artifact manifest")
    raw = manifest.read_bytes()
    require(
        raw.endswith(b"\n") and b"\r" not in raw and b"\0" not in raw,
        "artifact manifest is noncanonical",
    )
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError:
        fail("artifact manifest is not ASCII")
    actual_names = sorted(
        item.name
        for item in directory.iterdir()
        if item.name != manifest.name
    )
    require(
        len(lines) == len(actual_names),
        "artifact manifest census differs",
    )
    for line, expected_name in zip(lines, actual_names, strict=True):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        require(match is not None, "malformed artifact manifest row")
        digest, name = match.groups()
        require(name == expected_name, "artifact manifest order differs")
        target = directory / name
        require_regular(target, f"published artifact {name}")
        require(
            sha256_file(target) == digest,
            f"published artifact hash differs: {name}",
        )


def prune_private_inputs(work: Path) -> None:
    for name in (
        *SEED_HASHES,
        *PROCEDURE_HASHES,
        "case.x2m",
        "check_one",
        "check_balance",
        "check_pair",
    ):
        path = work / name
        require_regular(path, f"private work input {name}")
        path.unlink()
    shutil.rmtree(work / "fine")
    (work / "tmp").rmdir()


def write_run_receipt(
    work: Path,
    mode: str,
    classification: str,
) -> Path:
    evidence = {}
    for name in CAPTURE_EVIDENCE_FILES:
        target = work / name
        require_regular(target, f"run receipt evidence {name}")
        evidence[name] = sha256_file(target)
    receipt = {
        "schema": f"spot-inner-sensitivity-v2-{mode}-receipt-1",
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "implementation_receipt_sha256": sha256_file(
            IMPLEMENTATION_RECEIPT
        ),
        "scientific_manifest_sha256": sha256_file(
            work / "scientific_manifest.sha256"
        ),
        "evidence_sha256": evidence,
        "classification": classification,
        "dragon_processes": 1,
    }
    path = work / f"{mode}_receipt.json"
    require(
        not path.exists() and not path.is_symlink(),
        f"{mode} receipt already exists",
    )
    path.write_bytes(canonical_json(receipt))
    return path


def require_commit_ancestor(commit: str, owner: str) -> None:
    require(
        re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        f"{owner} must be a full lowercase commit id",
    )
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    require(ancestor.returncode == 0, f"{owner} is not an ancestor of HEAD")


def require_strict_commit_ancestor(commit: str, owner: str) -> None:
    require_commit_ancestor(commit, owner)
    head = run_checked(["git", "rev-parse", "HEAD"]).stdout.decode(
        "ascii"
    ).strip()
    require(commit != head, f"{owner} must strictly precede HEAD")


def require_authorization_postdates_capture(
    authorization: Path,
    capture_commit: str,
) -> None:
    require_strict_commit_ancestor(capture_commit, "capture commit")
    resolved = require_regular(authorization, "replay authorization")
    try:
        relative = resolved.relative_to(ROOT).as_posix()
    except ValueError:
        fail("replay authorization is outside the repository")
    prior = git_bytes_optional(capture_commit, relative)
    require(
        prior is None or prior != resolved.read_bytes(),
        "replay authorization was already committed at capture time",
    )


def require_committed_bytes(path: Path, commit: str, owner: str) -> bytes:
    require_commit_ancestor(commit, "capture commit")
    resolved = require_regular(path, owner)
    try:
        relative = resolved.relative_to(ROOT).as_posix()
    except ValueError:
        fail(f"{owner} must be inside the repository")
    committed = git_bytes(commit, relative)
    require(committed == path.read_bytes(), f"{owner} differs from commit")
    return committed


def parse_science_manifest(raw: bytes) -> dict[str, str]:
    require(
        raw.endswith(b"\n") and b"\r" not in raw and b"\0" not in raw,
        "capture scientific manifest is noncanonical",
    )
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError:
        fail("capture scientific manifest is not ASCII")
    require(
        len(lines) == len(SCIENCE_FILES),
        "capture scientific manifest must have five rows",
    )
    result = {}
    for line, expected_name in zip(lines, SCIENCE_FILES, strict=True):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        require(match is not None, "malformed capture manifest row")
        digest, name = match.groups()
        require(name == expected_name, "capture manifest order differs")
        result[name] = digest
    for name in ("basis_reference.xsm", "state0_axial.xsm"):
        require(
            result[name] == FINE_HASHES[name],
            f"capture frozen input hash differs: {name}",
        )
    return result


def verify_replay_preconditions(
    args: argparse.Namespace,
    authorization: dict[str, Any],
) -> str:
    require(
        args.capture_manifest is not None
        and args.capture_receipt is not None
        and args.capture_artifact_dir is not None
        and args.capture_commit is not None,
        "replay requires committed capture manifest and receipt",
    )
    require(
        authorization["capture_commit"] == args.capture_commit,
        "replay authorization capture commit differs",
    )
    require_authorization_postdates_capture(
        args.authorization,
        args.capture_commit,
    )
    committed_manifest = require_committed_bytes(
        args.capture_manifest,
        args.capture_commit,
        "capture manifest",
    )
    require(
        hashlib.sha256(committed_manifest).hexdigest()
        == authorization["capture_scientific_manifest_sha256"],
        "replay authorization manifest hash differs",
    )
    entries = parse_science_manifest(committed_manifest)
    capture_root = require_directory(
        args.capture_artifact_dir,
        "capture artifact directory",
    )
    artifact_manifest = capture_root / "scientific_manifest.sha256"
    require_regular(artifact_manifest, "artifact capture manifest")
    require(
        artifact_manifest.read_bytes() == committed_manifest,
        "artifact capture manifest differs from committed manifest",
    )
    for name in SCIENCE_FILES:
        target = capture_root / name
        require_regular(target, f"capture artifact {name}")
        require(
            sha256_file(target) == entries[name],
            f"capture artifact hash differs: {name}",
        )

    committed_receipt = require_committed_bytes(
        args.capture_receipt,
        args.capture_commit,
        "capture receipt",
    )
    require(
        hashlib.sha256(committed_receipt).hexdigest()
        == authorization["capture_receipt_sha256"],
        "replay authorization receipt hash differs",
    )
    artifact_receipt = capture_root / "capture_receipt.json"
    require_regular(artifact_receipt, "artifact capture receipt")
    require(
        artifact_receipt.read_bytes() == committed_receipt,
        "artifact capture receipt differs from committed receipt",
    )
    try:
        receipt = json.loads(
            committed_receipt.decode("ascii"),
            object_pairs_hook=unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid capture receipt: {exc}")
    require(
        committed_receipt == canonical_json(receipt),
        "capture receipt is not canonical JSON",
    )
    require(
        tuple(receipt)
        == (
            "schema",
            "protocol_sha256",
            "implementation_receipt_sha256",
            "scientific_manifest_sha256",
            "evidence_sha256",
            "classification",
            "dragon_processes",
        ),
        "capture receipt key order differs",
    )
    require(
        receipt["schema"] == "spot-inner-sensitivity-v2-capture-receipt-1"
        and receipt["protocol_sha256"] == EXPECTED_PROTOCOL_SHA256
        and receipt["implementation_receipt_sha256"]
        == sha256_file(IMPLEMENTATION_RECEIPT)
        and receipt["scientific_manifest_sha256"]
        == sha256_file(artifact_manifest)
        and receipt["classification"] == "PENDING-REPLAY"
        and receipt["dragon_processes"] == 1,
        "capture receipt is not replayable",
    )
    evidence = receipt["evidence_sha256"]
    require(
        isinstance(evidence, dict)
        and tuple(evidence) == CAPTURE_EVIDENCE_FILES,
        "capture receipt evidence census differs",
    )
    for name in CAPTURE_EVIDENCE_FILES:
        target = capture_root / name
        require_regular(target, f"capture evidence {name}")
        require(
            sha256_file(target) == evidence[name],
            f"capture evidence hash differs: {name}",
        )
    capture_result = load_canonical_json(
        capture_root / "result.json",
        "capture result",
    )
    require(
        capture_result.get("classification") == "PENDING-REPLAY",
        "capture result does not authorize replay",
    )
    capture_authorization_sha = evidence["authorization.json"]
    require(
        isinstance(capture_authorization_sha, str)
        and re.fullmatch(r"[0-9a-f]{64}", capture_authorization_sha)
        is not None,
        "capture authorization hash is invalid",
    )
    return capture_authorization_sha


def load_authorization(path: Path, mode: str) -> tuple[dict[str, Any], str]:
    data = load_canonical_json(path, "run authorization")
    expected_keys = (
        CAPTURE_AUTH_KEYS if mode == "capture" else REPLAY_AUTH_KEYS
    )
    require(tuple(data) == expected_keys, "authorization key order differs")
    expected = {
        "schema": "spot-inner-sensitivity-v2-run-authorization-1",
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "implementation_commit": data["implementation_commit"],
        "ledger_relative_path": LEDGER_RELATIVE,
        "mode": mode,
    }
    if mode == "replay":
        expected.update(
            {
                "capture_commit": data["capture_commit"],
                "capture_scientific_manifest_sha256": data[
                    "capture_scientific_manifest_sha256"
                ],
                "capture_receipt_sha256": data["capture_receipt_sha256"],
            }
        )
    expected.update(
        {
            "maximum_dragon_processes": 1,
            "wall_clock_limit_seconds": 120,
            "automatic_replay": False,
        }
    )
    require(data == expected, "authorization fields differ from the frozen run gate")
    commit = data["implementation_commit"]
    require(
        isinstance(commit, str)
        and re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
        "invalid implementation commit",
    )
    if mode == "replay":
        require(
            isinstance(data["capture_commit"], str)
            and re.fullmatch(r"[0-9a-f]{40}", data["capture_commit"])
            is not None,
            "invalid authorized capture commit",
        )
        for key in (
            "capture_scientific_manifest_sha256",
            "capture_receipt_sha256",
        ):
            require(
                isinstance(data[key], str)
                and re.fullmatch(r"[0-9a-f]{64}", data[key]) is not None,
                f"invalid {key}",
            )
    verify_authorized_implementation(commit)
    require_head_identity(path, "run authorization")
    return data, sha256_file(path)


def atomic_json(path: Path, data: dict[str, Any], *, exclusive: bool) -> None:
    raw = canonical_json(data)
    if exclusive:
        try:
            with path.open("xb") as stream:
                stream.write(raw)
        except FileExistsError:
            fail(f"process budget is already spent: {path.name}")
        return
    temporary = path.with_name(path.name + ".new")
    require(
        not temporary.exists() and not temporary.is_symlink(),
        "ledger update path already exists",
    )
    with temporary.open("xb") as stream:
        stream.write(raw)
    os.replace(temporary, path)


class Ledger:
    def __init__(
        self,
        root: Path,
        mode: str,
        authorization_sha: str,
        capture_authorization_sha: str | None = None,
    ) -> None:
        self.root = require_directory(root, "execution ledger")
        self.mode = mode
        self.authorization_sha = authorization_sha
        self.capture_authorization_sha = capture_authorization_sha
        self.lock = self.root / ".stage4v2.lock"
        self.tombstone = self.root / f"{mode}-spent.json"
        self.closed = False
        try:
            self.lock.mkdir()
        except FileExistsError:
            fail("execution ledger is locked by another process")

    def close(self) -> None:
        if self.closed:
            return
        try:
            self.lock.rmdir()
        except OSError as exc:
            fail(f"cannot release execution ledger lock: {exc}")
        self.closed = True

    def reserve(self) -> None:
        if self.mode == "replay":
            require(
                self.capture_authorization_sha is not None,
                "replay lacks a bound capture authorization hash",
            )
            capture = self.root / "capture-spent.json"
            data = load_canonical_json(capture, "capture budget record")
            require(
                tuple(data)
                == (
                    "schema",
                    "mode",
                    "authorization_sha256",
                    "dragon_processes",
                    "status",
                )
                and data["schema"]
                == "spot-inner-sensitivity-v2-budget-1"
                and data["mode"] == "capture"
                and isinstance(data["authorization_sha256"], str)
                and re.fullmatch(
                    r"[0-9a-f]{64}",
                    data["authorization_sha256"],
                )
                is not None
                and data["authorization_sha256"]
                == self.capture_authorization_sha
                and data["dragon_processes"] == 1
                and data["status"] == "PENDING-REPLAY",
                "replay requires a successful PENDING-REPLAY capture",
            )
        atomic_json(
            self.tombstone,
            {
                "schema": "spot-inner-sensitivity-v2-budget-1",
                "mode": self.mode,
                "authorization_sha256": self.authorization_sha,
                "dragon_processes": 1,
                "status": "PROCESS-RESERVED",
            },
            exclusive=True,
        )

    def finish(self, status: str) -> None:
        atomic_json(
            self.tombstone,
            {
                "schema": "spot-inner-sensitivity-v2-budget-1",
                "mode": self.mode,
                "authorization_sha256": self.authorization_sha,
                "dragon_processes": 1,
                "status": status,
            },
            exclusive=False,
        )


def preflight(
    dragon: Path,
    fine_dir: Path,
    seed_dir: Path,
    fc: str,
    ganlib_lib: Path,
    ganlib_mod: Path,
) -> None:
    run_checked(
        [
            sys.executable,
            str(PROTOCOL_CHECKER),
            "--dragon",
            str(dragon),
        ]
    )
    run_checked([sys.executable, str(IMPLEMENTATION_CHECKER)])
    verify_inputs(dragon, fine_dir, seed_dir)
    with tempfile.TemporaryDirectory(prefix="spot-s4v2-preflight.") as raw:
        work = Path(raw)
        compile_checkers(work, fc, ganlib_lib, ganlib_mod)


def execute(
    args: argparse.Namespace,
    dragon: Path,
    fine_dir: Path,
    seed_dir: Path,
    ganlib_lib: Path,
    ganlib_mod: Path,
) -> None:
    require(args.authorization is not None, "execution requires authorization")
    require(args.output is not None, "execution requires an output directory")
    if args.mode == "capture":
        require(
            args.capture_manifest is None
            and args.capture_receipt is None
            and args.capture_artifact_dir is None
            and args.capture_commit is None,
            "capture forbids replay evidence",
        )
    else:
        require(
            args.capture_manifest is not None
            and args.capture_receipt is not None
            and args.capture_artifact_dir is not None
            and args.capture_commit is not None,
            "replay requires capture manifest, artifact, and commit",
        )
    authorization, authorization_sha = load_authorization(
        args.authorization,
        args.mode,
    )
    verify_implementation_head()
    capture_authorization_sha = None
    if args.mode == "replay":
        capture_authorization_sha = verify_replay_preconditions(
            args,
            authorization,
        )
    output = validate_output_path(
        args.output,
        args.mode,
        fine_dir,
        seed_dir,
        args.capture_artifact_dir,
    )
    output_parent = output.parent
    ledger_path = ROOT / LEDGER_RELATIVE
    if not ledger_path.exists() and not ledger_path.is_symlink():
        parent = require_directory(ledger_path.parent, "ledger parent")
        require(parent == ledger_path.parent.resolve(), "ledger parent differs")
        try:
            ledger_path.mkdir()
        except FileExistsError:
            pass
    ledger = Ledger(
        ledger_path,
        args.mode,
        authorization_sha,
        capture_authorization_sha,
    )
    work: Path | None = None
    published = False
    published_inode: tuple[int, int] | None = None
    reserved = False

    def invalidate_and_rollback() -> None:
        if reserved:
            try:
                ledger.finish("INVALID-NO-SCIENTIFIC-RESULT")
            except BaseException:
                pass
        if published_inode is None:
            return
        try:
            status = output.lstat()
            if (
                stat.S_ISDIR(status.st_mode)
                and not stat.S_ISLNK(status.st_mode)
                and (status.st_dev, status.st_ino) == published_inode
            ):
                shutil.rmtree(output)
        except FileNotFoundError:
            pass

    try:
        work = Path(
            tempfile.mkdtemp(prefix=".spot-s4v2.", dir=output_parent)
        )
        copy_inputs(work, fine_dir, seed_dir)
        compile_checkers(work, args.fc, ganlib_lib, ganlib_mod)
        write_input_manifest(
            work,
            dragon,
            ganlib_lib,
            ganlib_mod,
            args.authorization,
        )
        ledger.reserve()
        reserved = True
        require_absent(output, "output immediately before Dragon")
        run_checked(
            [
                sys.executable,
                str(PROCESS_WRAPPER),
                str(dragon),
                str(work / "case.x2m"),
                str(work),
                str(work / "dragon.log"),
            ],
            output=work / "process_check.log",
        )
        run_checked(
            [
                sys.executable,
                str(LOG_CHECKER),
                str(work / "dragon.log"),
            ],
            output=work / "raw_log_check.log",
        )
        run_checked(
            [
                "./check_one",
                "basis_reference.xsm",
                "state1_system.xsm",
                "state0_axial.xsm",
                "state1_axial.xsm",
                "state1_snapshots.xsm",
            ],
            cwd=work,
            output=work / "coarse_xsm_check.log",
        )
        run_checked(
            [
                "./check_balance",
                "initial_axial_track.xsm",
                "initial_axial_macrolib.xsm",
                "state1_system.xsm",
                "state1_axial.xsm",
            ],
            cwd=work,
            output=work / "balance_xsm_check.log",
        )
        run_checked(
            [
                "./check_pair",
                "fine/x0.xsm",
                "fine/x1.xsm",
                "state0_axial.xsm",
                "state1_axial.xsm",
                "fine/snap1.xsm",
                "state1_snapshots.xsm",
                "V2-2H",
            ],
            cwd=work,
            output=work / "pair_xsm_check.log",
        )
        manifest = write_science_manifest(work)
        result_command = [
            sys.executable,
            str(RESULT_CHECKER),
            str(work / "pair_xsm_check.log"),
            str(manifest),
            str(PROTOCOL),
            "--artifact-dir",
            str(work),
            "--mode",
            args.mode,
        ]
        if args.mode == "replay":
            result_command.extend(
                [
                    "--capture-manifest",
                    str(args.capture_manifest),
                    "--capture-receipt",
                    str(args.capture_receipt),
                    "--capture-artifact-dir",
                    str(args.capture_artifact_dir),
                    "--capture-commit",
                    args.capture_commit,
                ]
            )
        run_checked(
            result_command,
            output=work / "result.json",
        )
        result = load_canonical_json(work / "result.json", "result")
        expected_status = (
            ("PENDING-REPLAY", "UNRESOLVED")
            if args.mode == "capture"
            else ("QUALIFIED-ON-2H-TO-H-SCALE",)
        )
        require(
            result.get("classification") in expected_status,
            "unexpected result classification",
        )
        verify_inputs(dragon, fine_dir, seed_dir)
        shutil.copyfile(args.authorization, work / "authorization.json")
        write_run_receipt(work, args.mode, result["classification"])
        prune_private_inputs(work)
        write_artifact_manifest(work)
        work_status = work.stat()
        owned_inode = (work_status.st_dev, work_status.st_ino)
        require_absent(output, "output immediately before publication")
        rename_no_replace(work, output)
        published_inode = owned_inode
        output_status = output.lstat()
        require(
            stat.S_ISDIR(output_status.st_mode)
            and not stat.S_ISLNK(output_status.st_mode)
            and (output_status.st_dev, output_status.st_ino) == owned_inode,
            "published artifact identity differs",
        )
        verify_artifact_manifest(output)
        ledger.finish(result["classification"])
    except BaseException as body_error:
        invalidate_and_rollback()
        try:
            ledger.close()
        except BaseException as close_error:
            raise close_error from body_error
        raise
    else:
        try:
            ledger.close()
        except BaseException:
            invalidate_and_rollback()
            raise
        published = True
        print(
            "INNER-SENSITIVITY-V2 "
            f"{args.mode.upper()} {result['classification']}"
        )
        print(f"INNER-SENSITIVITY-V2 ARTIFACT {output}")
        print("INNER-SENSITIVITY-V2 DRAGON-PROCESSES 1")
    finally:
        if not published and work is not None:
            shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("preflight", "capture", "replay"),
        default="preflight",
    )
    parser.add_argument("--dragon", required=True, type=Path)
    parser.add_argument(
        "--fine-dir",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "iterative-map1",
    )
    parser.add_argument(
        "--seed-dir",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "iterative-seed",
    )
    parser.add_argument("--ganlib-lib", type=Path, default=ROOT / "Ganlib/src/libGanlib.a")
    parser.add_argument("--ganlib-mod", type=Path, default=ROOT / "Ganlib/src")
    parser.add_argument("--fc", default="gfortran")
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--capture-manifest", type=Path)
    parser.add_argument("--capture-receipt", type=Path)
    parser.add_argument("--capture-artifact-dir", type=Path)
    parser.add_argument("--capture-commit")
    args = parser.parse_args()

    require(args.dragon.is_absolute(), "Dragon path must be absolute")
    dragon = require_regular(args.dragon, "Dragon", executable=True)
    fine_dir = require_directory(args.fine_dir, "fine artifact directory")
    seed_dir = require_directory(args.seed_dir, "seed artifact directory")
    ganlib_lib = require_regular(args.ganlib_lib, "Ganlib library")
    ganlib_mod = require_directory(args.ganlib_mod, "Ganlib module directory")

    preflight(
        dragon,
        fine_dir,
        seed_dir,
        args.fc,
        ganlib_lib,
        ganlib_mod,
    )
    if args.mode == "preflight":
        require(
            args.authorization is None
            and args.output is None
            and args.capture_manifest is None
            and args.capture_receipt is None
            and args.capture_artifact_dir is None
            and args.capture_commit is None,
            "preflight forbids execution and replay arguments",
        )
        print("INNER-SENSITIVITY-V2 PREFLIGHT PASS")
        print("INNER-SENSITIVITY-V2 DRAGON-RUNS 0")
        return
    execute(
        args,
        dragon,
        fine_dir,
        seed_dir,
        ganlib_lib,
        ganlib_mod,
    )


if __name__ == "__main__":
    main()

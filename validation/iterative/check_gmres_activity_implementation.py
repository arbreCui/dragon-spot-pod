#!/usr/bin/env python3
"""Fail-closed static checker for the passive GMRES activity overlay.

This checker builds a validation-only source tree and performs syntax checks.
It never links or executes Dragon and never performs a transport calculation.
"""

from __future__ import annotations

import argparse
from collections import Counter
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ITERATIVE = ROOT / "validation" / "iterative"
PROTOCOL = ITERATIVE / "gmres_activity_protocol.json"
PROTOCOL_CHECKER = ITERATIVE / "check_gmres_activity_protocol.py"
OVERLAY_MANIFEST = ITERATIVE / "gmres_activity_overlay_manifest.json"
OVERLAY_PATCH = ITERATIVE / "gmres_activity_overlay.patch"
OVERLAY_BUILDER = ITERATIVE / "build_gmres_activity_overlay.sh"
IMPLEMENTATION_MANIFEST = ITERATIVE / "gmres_activity_implementation.sha256"

PARENT = "4d7abb23ac7975d4146beaa3b0049e36cdad8776"
PARENT_ARCHIVE_SHA256 = (
    "a1ee2a7ef3fb128afe4b1fe14c7021a1cff1b1d80adb18548fb22840969e23aa"
)
PROTOCOL_SHA256 = (
    "27093c87b7321f4ecfd22307c7fac0ecc6d99a2eb5b2019509d2bf11c663cc85"
)
PROTOCOL_CHECKER_SHA256 = (
    "675ce5191e8fabcdcc4e2884c6868df69f9fd123503bc7567e30f642a74b7726"
)
OVERLAY_MANIFEST_SHA256 = (
    "b117cea97cfb54b4b043bc923c435a736d01b54fbb8fcfd5fdcb1472c39283a3"
)
OVERLAY_PATCH_SHA256 = (
    "ebdc1eee70422e0c881901802602d053b61079ad942ec1dbdf16fbe88fc8f942"
)
OVERLAY_BUILDER_SHA256 = (
    "5daf045948a5844eb6ec7537d08333643445101016b609de2ea0cf0f2f72b32d"
)

FROZEN_COMPILER = Path(
    "/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15"
)
FROZEN_COMPILER_VERSION = (
    "GNU Fortran (Homebrew GCC 15.2.0_1) 15.2.0"
)
FROZEN_COMPILER_SHA256 = (
    "0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492"
)
GANLIB_MODULE = ROOT / "Ganlib/lib/Darwin_arm64/modules/ganlib.mod"
GANLIB_LIBRARY = ROOT / "Ganlib/lib/Darwin_arm64/libGanlib.a"
UTILIB_LIBRARY = ROOT / "Utilib/lib/Darwin_arm64/libUtilib.a"
GANLIB_MODULE_SHA256 = (
    "9ad2be2ae13310aa8273409d5cb3e70dfaa2201ada7bfc29a135bd566c4651d0"
)
GANLIB_LIBRARY_SHA256 = (
    "204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c"
)
UTILIB_LIBRARY_SHA256 = (
    "a6c5cca8825691fd1da7554acabe542ba9986aabdbc935ecc46d1993240244ca"
)

ALLOWED_CHANGED_PATHS = [
    "src/.dragon_deps.mk",
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLUGPI.f",
    "src/MCGMRE.f",
    "src/SPOMGMR.f90",
]
PARENT_SOURCE_SHA256 = {
    "src/.dragon_deps.mk": (
        "5d837ab375527373e6d40cae413b83672661fb458ebe7670c42bb0819e784ae3"
    ),
    "src/FLU.f": (
        "f9391eb48be9ab1f8d9c3250a23409de2dcfb6111d22db283d1c29d030d26fd0"
    ),
    "src/FLUDRV.f": (
        "6bfd74d6cb473619bcf6130fc723502d348b6a3e76da86e5d03934207b3e4934"
    ),
    "src/FLUGPI.f": (
        "0155090fc67f38184c4602b0d330cf241a0eeba7f82c203fc25529267b5401ac"
    ),
    "src/MCGMRE.f": (
        "61f71a4873a744608d429eaccc61807d76b5b50a3d2c10213734bb5b26bf1379"
    ),
}
PATCHED_SOURCE_SHA256 = {
    "src/.dragon_deps.mk": (
        "070caabdfffcee6cd33bead91a9f5604998c6ba262723ca603b88f6a795f1295"
    ),
    "src/FLU.f": (
        "8befd86f9ee77bf5d25186eaf914349b2d4259f354f9bff504f4622339033c0e"
    ),
    "src/FLUDRV.f": (
        "49fbb86905726c59d75bcb9f67507ffe6bc0a7624d748dc1cb7dea71115dc951"
    ),
    "src/FLUGPI.f": (
        "3c5e6e675311761839605422e26a59fc25eb690ea363f2c513708a12d259329a"
    ),
    "src/MCGMRE.f": (
        "16cf1c03933b1f5c1aa26cc5955999180b0149e6a9ef9fd26a2d54fad7264988"
    ),
    "src/SPOMGMR.f90": (
        "608203a9c23714bc2ace276172be4c8e84613f42c83565e30f752819fe79e274"
    ),
}
SPOMOC_SHA256 = (
    "23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc"
)

FREE_FORM_FLAGS = [
    "-fsyntax-only",
    "-Wall",
    "-Wextra",
    "-Werror",
    "-std=f2008",
    "-ffp-contract=off",
    "-fno-fast-math",
    "-ffpe-summary=none",
]
FIXED_FORM_FLAGS = [
    "-fsyntax-only",
    "-Wall",
    "-Werror",
    "-ffpe-summary=none",
    "-ffixed-form",
    "-ffixed-line-length-72",
    "-ffp-contract=off",
    "-fno-fast-math",
    "-frecord-marker=4",
]

IMPLEMENTATION_PATHS = {
    "validation/iterative/gmres_activity_protocol.json",
    "validation/iterative/check_gmres_activity_protocol.py",
    "validation/iterative/gmres_activity.md",
    "validation/iterative/gmres_activity_overlay.patch",
    "validation/iterative/gmres_activity_overlay_manifest.json",
    "validation/iterative/build_gmres_activity_overlay.sh",
    "validation/iterative/check_gmres_activity_implementation.py",
    "validation/iterative/test_gmres_activity_state.f90",
    "validation/iterative/run_gmres_activity_state_test.sh",
    "validation/iterative/check_gmres_activity_xsm.f90",
    "validation/iterative/make_gmres_activity_fixture.f90",
    "validation/iterative/run_gmres_activity_checker_test.sh",
    "validation/iterative/normalize_gmres_activity_log.py",
    "validation/iterative/run_gmres_activity_preflight.sh",
}

INSERTED_LINES = {
    "src/FLU.f": [
        "      USE SPOMGMR_AUDIT, ONLY: SPOMGMR_FLU_RESET,SPOMGMR_FINISH",
        "      CALL SPOMGMR_FLU_RESET()",
        "      CALL SPOMGMR_FINISH()",
    ],
    "src/FLUDRV.f": [
        "      USE SPOMGMR_AUDIT, ONLY: SPOMGMR_BEGIN",
        "      CALL SPOMGMR_BEGIN(IPFLUX,IPTRK,IMCAUD,CXDOOR,ITYPEC,NGRP,NUN,",
        "     1 NREG,MAXOUT,MAXINR,EPSOUT,EPSUNK,EPSINR,LFORW,ILEAK,LREBAL,",
        "     2 INITFL,IFRITR,IACITR)",
    ],
    "src/FLUGPI.f": [
        "      USE SPOMGMR_AUDIT, ONLY: SPOMGMR_PARSE_GMRA,",
        "     > SPOMGMR_REQUIRE_MOCA",
        "      ELSE IF(CARLIR.EQ.'GMRA') THEN",
        "        CALL SPOMGMR_PARSE_GMRA()",
        "      CALL SPOMGMR_REQUIRE_MOCA(IMCAUD)",
    ],
    "src/MCGMRE.f": [
        "      USE SPOMGMR_AUDIT, ONLY: SPOMGMR_MCGMRE_ENTER,SPOMGMR_ROLE,",
        "     1 SPOMGMR_BLOCK_BEGIN,SPOMGMR_BLOCK_END,SPOMGMR_MCGMRE_EXIT",
        "      CALL SPOMGMR_MCGMRE_ENTER(MAXI,ERRTOL,NSTART,NGROUP,NGEFF,",
        "     1 NGIND,NUN,NDIM,NLONG,NREG,NSOUT,NANI,NLIN,NFUNL,IAAC,ISCR,",
        "     2 PACA,STIS,IDIR,CYCLIC,LFORW)",
        "        CALL SPOMGMR_ROLE(1,ITER,NGEFF,NCONV)",
        "        CALL SPOMGMR_BLOCK_BEGIN(ITER,NGEFF,NCONV)",
        "          CALL SPOMGMR_ROLE(2,ITER,NGEFF,NCONV)",
        "          CALL SPOMGMR_ROLE(3,ITER,NGEFF,NCONV)",
        "        CALL SPOMGMR_BLOCK_END(ITER,NGEFF,KMAX)",
        "      CALL SPOMGMR_MCGMRE_EXIT(ITER)",
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY IMPLEMENTATION CHECK FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require_regular(path: Path, owner: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"invalid {owner}")


def require_hash(path: Path, expected: str, owner: str) -> None:
    require_regular(path, owner)
    require(sha256_file(path) == expected, f"{owner} SHA256 differs")


def require_canonical_text(path: Path, owner: str) -> str:
    require_regular(path, owner)
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), f"{owner} has no final LF")
    require(b"\r" not in raw and b"\0" not in raw, f"{owner} is not LF text")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"{owner} is not UTF-8")
    require(text.encode("utf-8") == raw, f"{owner} UTF-8 is not canonical")
    return text


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def run_checked(
    command: list[str],
    *,
    cwd: Path = ROOT,
    expected_stdout: str | None = None,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        command,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"command failed ({command[0]}): {detail}")
    if expected_stdout is not None:
        stdout = result.stdout.decode("utf-8", "strict")
        require(stdout == expected_stdout, f"unexpected output from {command[0]}")
    require(not result.stderr, f"unexpected stderr from {command[0]}")
    return result


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"git {' '.join(arguments)} failed: {detail}")
    return result


def require_safe_relative(text: str, owner: str) -> Path:
    path = PurePosixPath(text)
    require(
        text != ""
        and not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == text,
        f"unsafe {owner} path",
    )
    return ROOT.joinpath(*path.parts)


def verify_live_source() -> None:
    require(
        git("cat-file", "-e", f"{PARENT}^{{commit}}", check=False).returncode == 0,
        "frozen parent commit is unavailable",
    )
    require(
        git("diff", "--quiet", PARENT, "--", "src", check=False).returncode == 0,
        "live tracked src differs from frozen parent",
    )
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--", "src"
    ).stdout
    require(status == b"", "live src contains dirty or untracked paths")
    tree = git("ls-tree", "-r", PARENT).stdout.decode("utf-8", "strict")
    for line in tree.splitlines():
        mode = line.split(None, 1)[0]
        require(mode not in {"120000", "160000"}, "parent has symlink or gitlink")


def verify_protocol() -> None:
    require_hash(PROTOCOL, PROTOCOL_SHA256, "frozen protocol")
    checker_text = require_canonical_text(PROTOCOL_CHECKER, "protocol checker")
    require(
        sha256_bytes(checker_text.encode("utf-8"))
        == PROTOCOL_CHECKER_SHA256,
        "protocol checker SHA256 differs",
    )
    expected = (
        "GMRES-ACTIVITY-PROTOCOL PASS "
        f"sha256={PROTOCOL_SHA256} mode=FREEZE\n"
    )
    run_checked(
        [sys.executable, str(PROTOCOL_CHECKER), "--freeze-audit"],
        expected_stdout=expected,
    )


def verify_overlay_manifest() -> dict[str, Any]:
    text = require_canonical_text(OVERLAY_MANIFEST, "overlay manifest")
    require(
        sha256_bytes(text.encode("utf-8")) == OVERLAY_MANIFEST_SHA256,
        "overlay manifest bytes changed",
    )
    try:
        manifest = json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as exc:
        fail(f"invalid overlay manifest JSON: {exc}")

    require(
        manifest["name"] == "SPOT passive GMRES activity validation overlay"
        and manifest["version"] == 1
        and manifest["status"] == "FROZEN"
        and manifest["frozen_parent_commit"] == PARENT,
        "overlay identity differs",
    )
    require(
        manifest["parent_archive"]
        == {
            "format": "git-archive-tar",
            "command": f"git archive --format=tar {PARENT}",
            "sha256": PARENT_ARCHIVE_SHA256,
        },
        "parent archive contract differs",
    )
    require(
        manifest["overlay_patch"]
        == {
            "path": "validation/iterative/gmres_activity_overlay.patch",
            "sha256": OVERLAY_PATCH_SHA256,
            "strip_components": 1,
            "fuzz": 0,
        },
        "overlay patch contract differs",
    )
    require(
        manifest["allowed_changed_paths"] == ALLOWED_CHANGED_PATHS,
        "allowed changed paths differ",
    )
    require(
        manifest["parent_source_sha256"] == PARENT_SOURCE_SHA256,
        "parent source hashes differ",
    )
    require(
        manifest["patched_source_sha256"] == PATCHED_SOURCE_SHA256,
        "patched source hashes differ",
    )
    require(
        manifest["preserved_source_sha256"]
        == {"src/SPOMOC.f90": SPOMOC_SHA256},
        "preserved source contract differs",
    )
    require(
        manifest["fixed_form_hook_sources"]
        == ["src/FLU.f", "src/FLUDRV.f", "src/FLUGPI.f", "src/MCGMRE.f"],
        "fixed-form hook source census differs",
    )
    require(
        manifest["toolchain"]
        == {
            "platform": "Darwin arm64",
            "compiler_path": str(FROZEN_COMPILER),
            "compiler_version_line": FROZEN_COMPILER_VERSION,
            "compiler_sha256": FROZEN_COMPILER_SHA256,
            "ganlib_module_path": (
                "Ganlib/lib/Darwin_arm64/modules/ganlib.mod"
            ),
            "ganlib_module_sha256": GANLIB_MODULE_SHA256,
            "ganlib_library_path": "Ganlib/lib/Darwin_arm64/libGanlib.a",
            "ganlib_library_sha256": GANLIB_LIBRARY_SHA256,
            "utilib_library_path": "Utilib/lib/Darwin_arm64/libUtilib.a",
            "utilib_library_sha256": UTILIB_LIBRARY_SHA256,
        },
        "toolchain contract differs",
    )
    require(
        manifest["syntax_compile"]
        == {
            "support_source": "src/SPOMOC.f90",
            "overlay_sources_in_order": [
                "src/SPOMGMR.f90",
                "src/FLU.f",
                "src/FLUDRV.f",
                "src/FLUGPI.f",
                "src/MCGMRE.f",
            ],
            "free_form_flags": FREE_FORM_FLAGS,
            "fixed_form_flags": FIXED_FORM_FLAGS,
            "link": False,
        },
        "syntax compile contract differs",
    )
    require(
        manifest["safety"]
        == {
            "tracked_live_src": "UNCHANGED",
            "clean_parent_archive": True,
            "strict_patch_without_fuzz_or_offset": True,
            "reject_symlinks_and_special_files": True,
            "network_access": False,
            "Dragon_execution": False,
            "transport_execution": False,
        },
        "overlay safety contract differs",
    )
    return manifest


def verify_patch() -> None:
    text = require_canonical_text(OVERLAY_PATCH, "overlay patch")
    require(
        sha256_bytes(text.encode("utf-8")) == OVERLAY_PATCH_SHA256,
        "overlay patch bytes changed",
    )
    require("GIT binary patch" not in text, "binary patch is forbidden")
    paths = re.findall(r"(?m)^diff --git a/([^ ]+) b/([^ ]+)$", text)
    require(
        paths == [(path, path) for path in ALLOWED_CHANGED_PATHS],
        "patch path order or census differs",
    )
    require(text.count("new file mode ") == 1, "new-file census differs")
    require(
        "new file mode 100644\n" in text
        and "diff --git a/src/SPOMGMR.f90 b/src/SPOMGMR.f90\n" in text,
        "new module mode or path differs",
    )
    require("deleted file mode" not in text, "file deletion is forbidden")


def extract_archive(archive: Path, destination: Path) -> None:
    destination.mkdir()
    seen: set[str] = set()
    with tarfile.open(archive, "r:") as handle:
        members = handle.getmembers()
        require(members, "parent archive is empty")
        for member in members:
            raw_name = member.name.rstrip("/")
            relative = PurePosixPath(raw_name)
            require(
                raw_name
                and not relative.is_absolute()
                and ".." not in relative.parts
                and relative.as_posix() == raw_name,
                "unsafe parent archive path",
            )
            require(raw_name not in seen, "duplicate parent archive path")
            seen.add(raw_name)
            require(
                member.isdir() or member.isreg(),
                "parent archive contains a special entry",
            )
            target = destination.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                target.chmod(member.mode & 0o700)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            source = handle.extractfile(member)
            require(source is not None, "cannot read parent archive member")
            target.write_bytes(source.read())
            target.chmod(member.mode & 0o700)


def source_census(root: Path) -> dict[str, tuple[int, str]]:
    src = root / "src"
    require(src.is_dir() and not src.is_symlink(), "invalid source directory")
    result: dict[str, tuple[int, str]] = {}
    for path in sorted(src.rglob("*")):
        relative = "src/" + path.relative_to(src).as_posix()
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), f"source symlink: {relative}")
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode), f"source special file: {relative}")
        result[relative] = (stat.S_IMODE(mode), sha256_file(path))
    return result


def verify_source_census(parent_tree: Path, patched_tree: Path) -> None:
    parent = source_census(parent_tree)
    patched = source_census(patched_tree)
    observed: list[str] = []
    for relative in sorted(parent.keys() | patched.keys()):
        if relative not in parent or relative not in patched:
            observed.append(relative)
        elif parent[relative] != patched[relative]:
            observed.append(relative)
    require(
        observed == sorted(ALLOWED_CHANGED_PATHS),
        f"source change census differs: {observed!r}",
    )
    require(
        patched["src/SPOMGMR.f90"][0] == 0o644,
        "SPOMGMR source mode is not 100644",
    )
    for relative, digest in PARENT_SOURCE_SHA256.items():
        require(parent[relative][1] == digest, f"parent hash differs: {relative}")
    for relative, digest in PATCHED_SOURCE_SHA256.items():
        require(patched[relative][1] == digest, f"patched hash differs: {relative}")
    require(
        parent["src/SPOMOC.f90"][1] == SPOMOC_SHA256
        and patched["src/SPOMOC.f90"][1] == SPOMOC_SHA256,
        "SPOMOC was not preserved",
    )


def inserted_lines(parent: str, patched: str, owner: str) -> list[str]:
    before = parent.splitlines()
    after = patched.splitlines()
    result: list[str] = []
    matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    for tag, left_a, left_b, right_a, right_b in matcher.get_opcodes():
        if tag == "equal":
            continue
        require(tag == "insert" and left_a == left_b, f"{owner} is not insertion-only")
        result.extend(after[right_a:right_b])
    return result


def require_once(text: str, sequence: str, owner: str) -> int:
    require(text.count(sequence) == 1, f"{owner} sequence census differs")
    return text.index(sequence)


def verify_hook_sources(parent_tree: Path, patched_tree: Path) -> None:
    for relative, expected in INSERTED_LINES.items():
        parent = require_canonical_text(parent_tree / relative, f"parent {relative}")
        patched = require_canonical_text(patched_tree / relative, f"patched {relative}")
        require(
            inserted_lines(parent, patched, relative) == expected,
            f"{relative} inserted lines differ",
        )

    deps_parent = require_canonical_text(
        parent_tree / "src/.dragon_deps.mk", "parent dependency file"
    )
    deps_patched = require_canonical_text(
        patched_tree / "src/.dragon_deps.mk", "patched dependency file"
    )
    expected_deps = deps_parent
    replacements = [
        (
            "FLU2DR.o: SPOMOC.o\nFLUDRV.o: SPOMOC.o\nINFNDA.o:",
            "FLU.o: SPOMGMR.o\nFLU2DR.o: SPOMOC.o\n"
            "FLUDRV.o: SPOMGMR.o SPOMOC.o\nFLUGPI.o: SPOMGMR.o\nINFNDA.o:",
        ),
        (
            "MCGMRE.o: SPOMOC.o",
            "MCGMRE.o: SPOMGMR.o SPOMOC.o",
        ),
    ]
    for old, new in replacements:
        require(expected_deps.count(old) == 1, "parent dependency anchor differs")
        expected_deps = expected_deps.replace(old, new)
    require(deps_patched == expected_deps, "dependency changes differ")

    flu = (patched_tree / "src/FLU.f").read_text(encoding="utf-8")
    flu_reset = require_once(
        flu,
        "      CALL SPOMGMR_FLU_RESET()\n"
        "      IF(NENTRY.LE.1) CALL XABORT('FLU: TWO PARAMETERS EXPECTED.')",
        "FLU reset hook",
    )
    flu_finish = require_once(
        flu,
        "      CALL LCMSIX(IPMACR,' ',0)\n"
        "      CALL SPOMGMR_FINISH()\n"
        "      RETURN",
        "FLU finish hook",
    )
    require(flu_reset < flu_finish, "FLU hook order differs")

    fludrv = (patched_tree / "src/FLUDRV.f").read_text(encoding="utf-8")
    begin = require_once(
        fludrv,
        "      CALL SPOMOC_BEGIN(IPFLUX,IMCAUD,CXDOOR,ITYPEC,NGRP,NUN,NREG,\n"
        "     1 MAXOUT,MAXINR,EPSOUT,EPSUNK,EPSINR,LFORW,ILEAK,LREBAL,INITFL,\n"
        "     2 IFRITR,IACITR)\n"
        "      CALL SPOMGMR_BEGIN(IPFLUX,IPTRK,IMCAUD,CXDOOR,ITYPEC,NGRP,NUN,\n"
        "     1 NREG,MAXOUT,MAXINR,EPSOUT,EPSUNK,EPSINR,LFORW,ILEAK,LREBAL,\n"
        "     2 INITFL,IFRITR,IACITR)\n"
        "      CALL FLU2DR(",
        "FLUDRV begin hook",
    )
    require(begin >= 0, "FLUDRV begin hook missing")

    flugpi = (patched_tree / "src/FLUGPI.f").read_text(encoding="utf-8")
    parse = require_once(
        flugpi,
        "        IMCAUD=INTLIR\n"
        "      ELSE IF(CARLIR.EQ.'GMRA') THEN\n"
        "        CALL SPOMGMR_PARSE_GMRA()\n"
        "      ELSE IF(CARLIR.EQ.'EDIT') THEN",
        "FLUGPI parser hook",
    )
    gate = require_once(
        flugpi,
        " 140  CONTINUE\n"
        "      CALL SPOMGMR_REQUIRE_MOCA(IMCAUD)\n"
        "      IF(ITYPEC.EQ.3) THEN",
        "FLUGPI MOCA gate",
    )
    require(parse < gate, "FLUGPI hook order differs")

    mcgmre = (patched_tree / "src/MCGMRE.f").read_text(encoding="utf-8")
    require(mcgmre.count("CALL MCGFL1(") == 3, "MCGFL1 call census differs")
    hook_sequences = [
        (
            "CALL SPOMGMR_MCGMRE_ENTER",
            "      CALL SPOMGMR_MCGMRE_ENTER(MAXI,ERRTOL,NSTART,NGROUP,NGEFF,\n"
            "     1 NGIND,NUN,NDIM,NLONG,NREG,NSOUT,NANI,NLIN,NFUNL,IAAC,ISCR,\n"
            "     2 PACA,STIS,IDIR,CYCLIC,LFORW)\n"
            "      ALLOCATE(DENOM",
        ),
        (
            "PRIMARY role hook",
            "        CALL SPOMOC_SET_ROLE(1,ITER)\n"
            "        CALL SPOMGMR_ROLE(1,ITER,NGEFF,NCONV)\n"
            "        CALL MCGFL1(",
        ),
        (
            "block begin hook",
            "        KMAX(:)=0\n"
            "        CALL SPOMGMR_BLOCK_BEGIN(ITER,NGEFF,NCONV)\n"
            "        DO II=1,NGEFF",
        ),
        (
            "affine role hook",
            "          CALL SPOMOC_SET_ROLE(2,ITER)\n"
            "          CALL SPOMGMR_ROLE(2,ITER,NGEFF,NCONV)\n"
            "          CALL MCGFL1(",
        ),
        (
            "Krylov role hook",
            "          CALL SPOMOC_SET_ROLE(3,ITER)\n"
            "          CALL SPOMGMR_ROLE(3,ITER,NGEFF,NCONV)\n"
            "          CALL MCGFL1(",
        ),
        (
            "block end hook",
            "        CALL SPOMGMR_BLOCK_END(ITER,NGEFF,KMAX)\n"
            "        DO II=1,NGEFF\n"
            "          K=KMAX(II)",
        ),
        (
            "normal exit hook",
            "      DEALLOCATE(FLOUT, KMAX, RHO, DENOM)\n"
            "      CALL SPOMGMR_MCGMRE_EXIT(ITER)\n"
            "      RETURN",
        ),
    ]
    positions = [require_once(mcgmre, sequence, owner) for owner, sequence in hook_sequences]
    require(positions == sorted(positions), "MCGMRE hook order differs")


def verify_module(patched_tree: Path) -> None:
    path = patched_tree / "src/SPOMGMR.f90"
    text = require_canonical_text(path, "SPOMGMR module")
    require(sha256_file(path) == PATCHED_SOURCE_SHA256["src/SPOMGMR.f90"], "module hash differs")
    require(
        re.search(r"(?im)^\s*(write|print)\b", text) is None,
        "module contains output I/O",
    )
    call_names = Counter(
        match.group(1).upper()
        for match in re.finditer(r"(?im)^\s*call\s+([a-z][a-z0-9_]*)", text)
    )
    require(
        set(call_names)
        == {
            "FAIL",
            "LCMGET",
            "LCMLEN",
            "LCMPUT",
            "RELEASE_MEMORY",
            "REQUIRE_ABSENT",
            "XABORT",
        },
        "module call graph contains an unexpected routine",
    )
    forbidden_solver = re.compile(
        r"\b(DOORFV|FLU2DR|FLU2AC|FLUBAL|MCCGF|MCGFLX|"
        r"MCGFL1|MCGFCS|MCGSIG|MCGFCF|MOCFCF|MCGFST|MCGFCA|"
        r"MCGSCR|SPOT1P|SPOLEAK|SPOPROJ)\b",
        re.IGNORECASE,
    )
    require(forbidden_solver.search(text) is None, "module references solver code")
    lcmget = re.findall(
        r"(?i)call\s+LCMGET\s*\(\s*([a-z_][a-z0-9_]*)\s*,\s*'([^']+)'",
        text,
    )
    require(
        [(owner.lower(), name) for owner, name in lcmget]
        == [("iptrk", "MCCG-STATE"), ("iptrk", "REAL-PARAM")],
        "LCMGET source or record census differs",
    )
    lcmput = re.findall(
        r"(?i)call\s+LCMPUT\s*\(\s*([a-z_][a-z0-9_]*)\s*,\s*'([^']+)'",
        text,
    )
    require(
        all(owner.lower() == "audit_root" for owner, _ in lcmput),
        "LCMPUT escaped the audit root",
    )
    require(
        Counter(name for _, name in lcmput)
        == Counter(
            {
                "STATE-VECTOR": 2,
                "NGIND": 1,
                "CALL-META": 1,
                "ROLE-CALLS": 1,
                "ROLE-GROUPS": 1,
                "ROLE-EVENTS": 1,
                "ROLE-ACTIVE": 1,
                "K-HISTOGRAM": 1,
                "BLOCK-META": 1,
                "BLOCK-ACTIVE": 1,
                "BLOCK-KMAX": 1,
            }
        ),
        "LCMPUT record census differs",
    )
    require(
        text.count("audit_root = LCMDID(ipflux, 'SPOT-GMR-AUD')") == 1,
        "audit sink creation differs",
    )
    require(
        "        if (first_event /= 0) then\n"
        "          if (role_active(group, event) > &\n"
        "               role_active(group, first_event)) &\n"
        "               call fail('Krylov active mask changed 0 to 1')\n"
        "        end if\n" in text
        and "if ((first_event /= 0) .and." not in text,
        "Krylov mask guard relies on nonstandard short-circuit evaluation",
    )
    require(
        "      if (event > 1) then\n"
        "        if (role_events(4, event) < role_events(4, event - 1)) &\n"
        "             call fail('role ITER order differs')\n"
        "      end if\n" in text
        and "if ((event > 1) .and." not in text,
        "role-order guard relies on nonstandard short-circuit evaluation",
    )
    for token in (
        "integer, parameter :: required_groups = 370",
        "integer, parameter :: required_unknowns = 14",
        "integer, parameter :: required_regions = 8",
        "integer, parameter :: required_maxi = 20",
        "integer, parameter :: required_nstart = 10",
        "required_role_capacity = required_maxi",
        "required_block_capacity = required_maxi - 1",
        "int(z'348637BD', int32)",
        "int(z'3727C5AC', int32)",
        "state_vector(24)",
        "operator-applications-added",
    ):
        if token == "operator-applications-added":
            require(
                "state_vector(23) = 0" in text and "state_vector(23:24) = 0" in text,
                "zero added-operator fields differ",
            )
        else:
            require(token in text, f"module lost frozen token: {token}")
    for forbidden in (
        "relax",
        "damping",
        "clipping",
        "empirical",
        "heuristic",
        "fitting",
        "tunable",
        "isclose",
        "allclose",
        "epsilon(",
        "tiny(",
        "huge(",
    ):
        require(forbidden not in text.lower(), f"module contains {forbidden}")
    require(text.lower().count("transfer(") == 5, "floating-bit checks differ")
    require(text.lower().count("real(real32)") == 3, "REAL inputs differ")
    require(
        re.search(r"(?i)(?<![a-z0-9_])\d+\.\d+(?:[de][+-]?\d+)?", text)
        is None,
        "module contains floating arithmetic constants",
    )


def verify_toolchain() -> None:
    require(
        platform.system() == "Darwin" and platform.machine() == "arm64",
        "platform differs from frozen toolchain",
    )
    override = os.environ.get("FC")
    require(
        override is None or override == str(FROZEN_COMPILER),
        "unfrozen FC override",
    )
    require_hash(FROZEN_COMPILER, FROZEN_COMPILER_SHA256, "frozen compiler")
    require_hash(GANLIB_MODULE, GANLIB_MODULE_SHA256, "Ganlib module")
    require_hash(GANLIB_LIBRARY, GANLIB_LIBRARY_SHA256, "Ganlib library")
    require_hash(UTILIB_LIBRARY, UTILIB_LIBRARY_SHA256, "Utilib library")
    version = run_checked([str(FROZEN_COMPILER), "--version"]).stdout
    first = version.decode("utf-8", "strict").splitlines()[0]
    require(first == FROZEN_COMPILER_VERSION, "compiler version differs")


def syntax_compile(patched_tree: Path, work: Path) -> None:
    module_dir = work / "modules"
    module_dir.mkdir()
    include = str(GANLIB_MODULE.parent)
    free_sources = [
        patched_tree / "src/SPOMOC.f90",
        patched_tree / "src/SPOMGMR.f90",
    ]
    for source in free_sources:
        run_checked(
            [
                str(FROZEN_COMPILER),
                *FREE_FORM_FLAGS,
                "-I",
                include,
                "-I",
                str(module_dir),
                "-J",
                str(module_dir),
                str(source),
            ]
        )
    for name in ("FLU.f", "FLUDRV.f", "FLUGPI.f", "MCGMRE.f"):
        run_checked(
            [
                str(FROZEN_COMPILER),
                *FIXED_FORM_FLAGS,
                "-I",
                include,
                "-I",
                str(module_dir),
                "-J",
                str(module_dir),
                str(patched_tree / "src" / name),
            ]
        )


def verify_clean_build(work: Path) -> tuple[Path, Path]:
    archive = work / "parent.tar"
    with archive.open("wb") as stream:
        result = subprocess.run(
            ["git", "archive", "--format=tar", PARENT],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.PIPE,
            check=False,
        )
    require(result.returncode == 0 and not result.stderr, "git archive failed")
    require_hash(archive, PARENT_ARCHIVE_SHA256, "parent archive")
    parent_tree = work / "parent"
    extract_archive(archive, parent_tree)

    patched_tree = work / "patched"
    result = run_checked([str(OVERLAY_BUILDER), str(patched_tree)])
    expected = (
        f"PASS: GMRES activity overlay built at {patched_tree.resolve()}\n"
    ).encode()
    require(result.stdout == expected, "overlay builder output differs")
    return parent_tree, patched_tree


def verify_implementation_manifest() -> None:
    text = require_canonical_text(
        IMPLEMENTATION_MANIFEST, "implementation manifest"
    )
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([!-~]+)", line)
        require(match is not None, "implementation manifest grammar differs")
        assert match is not None
        digest, relative = match.groups()
        require_safe_relative(relative, "implementation manifest")
        rows.append((digest, relative))
    paths = [relative for _, relative in rows]
    require(
        paths == sorted(IMPLEMENTATION_PATHS)
        and set(paths) == IMPLEMENTATION_PATHS
        and len(paths) == len(set(paths)),
        "implementation manifest path census or order differs",
    )
    require(
        "validation/iterative/gmres_activity_implementation.sha256" not in paths,
        "implementation manifest contains itself",
    )
    for expected, relative in rows:
        path = require_safe_relative(relative, "implementation file")
        require_canonical_text(path, relative)
        require(sha256_file(path) == expected, f"implementation hash differs: {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--structural-only",
        action="store_true",
        help="skip the final aggregate implementation manifest",
    )
    arguments = parser.parse_args()

    verify_live_source()
    if not arguments.structural_only:
        verify_implementation_manifest()
    verify_protocol()
    verify_overlay_manifest()
    verify_patch()
    builder_text = require_canonical_text(OVERLAY_BUILDER, "overlay builder")
    require(
        sha256_bytes(builder_text.encode("utf-8")) == OVERLAY_BUILDER_SHA256,
        "overlay builder SHA256 differs",
    )
    verify_toolchain()

    with tempfile.TemporaryDirectory(
        prefix="spot-gmres-implementation-"
    ) as temporary:
        work = Path(temporary)
        parent_tree, patched_tree = verify_clean_build(work)
        verify_source_census(parent_tree, patched_tree)
        verify_hook_sources(parent_tree, patched_tree)
        verify_module(patched_tree)
        syntax_compile(patched_tree, work)

    verify_live_source()
    print("GMRES-ACTIVITY IMPLEMENTATION CHECK PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Atomically publish one completed B2z evidence directory without replacement."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path
import stat
import sys


RENAME_EXCL = 0x00000004
AT_FDCWD = -2


def fail(message: str) -> None:
    raise SystemExit(f"B2Z ATOMIC PUBLICATION FAILURE: {message}")


def lstat_absent(path: Path, owner: str) -> None:
    try:
        path.lstat()
    except FileNotFoundError:
        return
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    fail(f"{owner} already exists")


def require_directory(path: Path, owner: str) -> os.stat_result:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    if not stat.S_ISDIR(status.st_mode) or stat.S_ISLNK(status.st_mode):
        fail(f"{owner} is not a non-symlink directory")
    return status


def main() -> None:
    if len(sys.argv) != 3:
        fail("expected STAGE-DIRECTORY FINAL-DIRECTORY")
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    if not source.is_absolute() or not target.is_absolute():
        fail("paths must be absolute")
    if source.parent != target.parent:
        fail("stage and final must have the same parent")
    parent_status = require_directory(source.parent, "publication parent")
    source_status = require_directory(source, "stage")
    if source_status.st_dev != parent_status.st_dev:
        fail("stage is not on the publication filesystem")
    lstat_absent(target, "publication target")

    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform != "darwin" or not hasattr(libc, "renameatx_np"):
        fail("Darwin renameatx_np is unavailable")
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
        AT_FDCWD,
        os.fsencode(source),
        AT_FDCWD,
        os.fsencode(target),
        RENAME_EXCL,
    )
    if result != 0:
        error = ctypes.get_errno()
        fail(f"atomic no-replace rename failed: {os.strerror(error)}")

    target_status = require_directory(target, "published target")
    if (target_status.st_dev, target_status.st_ino) != (
        source_status.st_dev,
        source_status.st_ino,
    ):
        fail("published directory identity differs")
    try:
        source.lstat()
    except FileNotFoundError:
        pass
    else:
        fail("stage name remains after publication")
    print("B2Z ATOMIC NO-REPLACE PUBLICATION PASS")


if __name__ == "__main__":
    main()

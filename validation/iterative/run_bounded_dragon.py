#!/usr/bin/env python3
"""Run one Dragon deck with a process-group wall-clock bound."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import sys
import time


TIMEOUT_SECONDS = 30
TERM_GRACE_SECONDS = 5


def fail(message: str) -> None:
    raise SystemExit(f"RAW-MOC-CAPTURE PROCESS FAIL: {message}")


def require_regular(path: Path, executable: bool = False) -> Path:
    resolved = path.resolve(strict=True)
    if path.is_symlink() or not resolved.is_file():
        fail(f"not a regular non-symlink file: {path}")
    if executable and not os.access(resolved, os.X_OK):
        fail(f"not executable: {path}")
    return resolved


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + TERM_GRACE_SECONDS
    while process.poll() is None and time.monotonic() < deadline:
        time.sleep(0.05)
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait()


def run(
    dragon_path: Path,
    deck_path: Path,
    log_path: Path,
    timeout_seconds: float = TIMEOUT_SECONDS,
) -> int:
    dragon = require_regular(dragon_path, executable=True)
    deck = require_regular(deck_path)
    if timeout_seconds <= 0:
        fail("timeout must be positive")
    if log_path.exists() or log_path.is_symlink():
        fail(f"refusing to overwrite log: {log_path}")
    log_parent = log_path.parent.resolve(strict=True)
    if not log_parent.is_dir():
        fail("log parent is not a directory")

    with deck.open("rb") as deck_stream, log_path.open("xb") as log_stream:
        process = subprocess.Popen(
            [str(dragon)],
            cwd=str(deck.parent),
            stdin=deck_stream,
            stdout=log_stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            terminate_group(process)
            fail(
                f"timeout after {timeout_seconds:g} seconds; "
                "no scientific result"
            )
    if return_code != 0:
        fail(f"Dragon exit status {return_code}; no scientific result")
    return return_code


def main() -> None:
    if len(sys.argv) != 4:
        fail("expected DRAGON DECK LOG")
    dragon = Path(sys.argv[1])
    deck = Path(sys.argv[2])
    log = Path(sys.argv[3])
    run(dragon, deck, log)
    print("RAW-MOC-CAPTURE PROCESS PASS")


if __name__ == "__main__":
    main()

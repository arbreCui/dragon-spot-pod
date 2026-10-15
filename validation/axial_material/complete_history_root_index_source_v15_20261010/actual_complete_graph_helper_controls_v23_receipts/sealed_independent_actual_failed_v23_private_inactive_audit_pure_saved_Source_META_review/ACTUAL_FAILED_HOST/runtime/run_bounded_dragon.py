#!/usr/bin/env python3
"""Run one Dragon deck with bounded process-group cleanup."""

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


def process_group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def terminate_process_group(
    pgid: int,
    grace_seconds: float,
    process: subprocess.Popen[bytes] | None = None,
) -> None:
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + grace_seconds
    while process_group_exists(pgid) and time.monotonic() < deadline:
        if process is not None:
            process.poll()
        time.sleep(0.05)
    if process_group_exists(pgid):
        try:
            os.killpg(pgid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    terminate_process_group(process.pid, TERM_GRACE_SECONDS, process)
    process.wait()


def watch_liveness(read_fd: int, pgid: int, grace_seconds: float) -> None:
    """Kill one running child group if its supervising process disappears."""
    try:
        while os.read(read_fd, 1):
            pass
    finally:
        os.close(read_fd)
    if process_group_exists(pgid):
        terminate_process_group(pgid, grace_seconds)


def start_liveness_watchdog(
    read_fd: int,
    pgid: int,
    grace_seconds: float,
) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--watch-liveness",
            str(read_fd),
            str(pgid),
            f"{grace_seconds:.17g}",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        pass_fds=(read_fd,),
        start_new_session=True,
    )


def finish_liveness_watchdog(
    write_fd: int,
    watchdog: subprocess.Popen[bytes],
) -> None:
    os.close(write_fd)
    try:
        watchdog.wait(timeout=TERM_GRACE_SECONDS + 1.0)
    except subprocess.TimeoutExpired:
        watchdog.kill()
        watchdog.wait()


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

    handled_signals = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)
    previous_handlers = {
        item: signal.signal(item, signal.default_int_handler)
        for item in handled_signals
    }
    try:
        with deck.open("rb") as deck_stream, log_path.open("xb") as log_stream:
            process = subprocess.Popen(
                [str(dragon)],
                cwd=str(deck.parent),
                stdin=deck_stream,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            read_fd, write_fd = os.pipe()
            try:
                watchdog = start_liveness_watchdog(
                    read_fd,
                    process.pid,
                    TERM_GRACE_SECONDS,
                )
            except BaseException:
                os.close(read_fd)
                os.close(write_fd)
                terminate_group(process)
                raise
            os.close(read_fd)
            try:
                try:
                    return_code = process.wait(timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    terminate_group(process)
                    fail(
                        f"timeout after {timeout_seconds:g} seconds; "
                        "no scientific result"
                    )
                except BaseException:
                    terminate_group(process)
                    raise
            finally:
                finish_liveness_watchdog(write_fd, watchdog)
    finally:
        for item, handler in previous_handlers.items():
            signal.signal(item, handler)
    if return_code != 0:
        fail(f"Dragon exit status {return_code}; no scientific result")
    return return_code


def main() -> None:
    if len(sys.argv) == 5 and sys.argv[1] == "--watch-liveness":
        read_fd = int(sys.argv[2])
        pgid = int(sys.argv[3])
        grace_seconds = float(sys.argv[4])
        if read_fd < 0 or pgid <= 0 or grace_seconds < 0.0:
            fail("invalid liveness-watchdog arguments")
        watch_liveness(read_fd, pgid, grace_seconds)
        return
    if len(sys.argv) not in (4, 5):
        fail("expected DRAGON DECK LOG [TIMEOUT_SECONDS]")
    dragon = Path(sys.argv[1])
    deck = Path(sys.argv[2])
    log = Path(sys.argv[3])
    timeout_seconds = TIMEOUT_SECONDS
    if len(sys.argv) == 5:
        try:
            timeout_seconds = float(sys.argv[4])
        except ValueError:
            fail("timeout must be a number")
    run(dragon, deck, log, timeout_seconds)
    print("RAW-MOC-CAPTURE PROCESS PASS")


if __name__ == "__main__":
    main()

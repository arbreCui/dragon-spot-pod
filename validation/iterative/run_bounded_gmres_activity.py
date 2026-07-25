#!/usr/bin/env python3
"""Run one frozen GMRES-activity deck in one bounded process group."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Optional


TIMEOUT_SECONDS = 30
TERM_GRACE_SECONDS = 5
PASS_LINE = "GMRES-ACTIVITY PROCESS PASS"
TMP_DIRECTORY_NAME = "tmp"
MANAGED_SIGNALS = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)


class TerminationSignal(Exception):
    """A managed outer signal that must first terminate the child group."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


def fail(message: str) -> None:
    raise SystemExit(f"GMRES-ACTIVITY PROCESS FAIL: {message}")


def require_regular_non_symlink(
    path: Path,
    *,
    executable: bool = False,
) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect input file {path}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
        fail(f"not a regular non-symlink file: {path}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve input file {path}: {exc}")
    if executable and not os.access(resolved, os.X_OK):
        fail(f"not executable: {path}")
    return resolved


def require_case_directory(path: Path) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect case directory {path}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
        fail(f"case directory is not a regular non-symlink directory: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve case directory {path}: {exc}")


def path_exists_without_following(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as exc:
        fail(f"cannot inspect output path {path}: {exc}")
    return True


def process_group_exists(process_group: int) -> bool:
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # Some sandboxed Darwin runtimes deny signal 0 after TERM even for a
        # group we created.  Treat that as "possibly alive" and retain the
        # fail-safe KILL at the end of the frozen grace period.
        return True
    return True


def terminate_exact_process_group(
    process: subprocess.Popen[bytes],
) -> None:
    process_group = process.pid
    deadline = time.monotonic() + TERM_GRACE_SECONDS
    try:
        os.killpg(process_group, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return

    while time.monotonic() < deadline:
        process.poll()
        if not process_group_exists(process_group):
            process.wait()
            return
        time.sleep(0.02)

    if process_group_exists(process_group):
        try:
            os.killpg(process_group, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait()


def raise_termination_signal(
    signum: int,
    _frame: object,
) -> None:
    # Make cleanup non-interruptible by repeated terminal/job-control signals.
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, signal.SIG_IGN)
    raise TerminationSignal(signum)


def run(
    dragon_path: Path,
    deck_path: Path,
    log_path: Path,
) -> int:
    if not dragon_path.is_absolute():
        fail("Dragon executable path must be absolute")
    dragon = require_regular_non_symlink(
        dragon_path,
        executable=True,
    )
    deck = require_regular_non_symlink(deck_path)
    case_directory = require_case_directory(deck_path.parent)
    if deck.parent != case_directory:
        deck = deck.resolve(strict=True)
    if deck.parent != case_directory:
        fail("deck is not directly inside its case directory")

    log_parent = require_case_directory(log_path.parent)
    if log_parent != case_directory:
        fail("deck and log must share one isolated case directory")
    output_log = log_parent / log_path.name
    if path_exists_without_following(output_log):
        fail(f"refusing to overwrite log: {log_path}")

    temporary_directory = require_case_directory(
        case_directory / TMP_DIRECTORY_NAME
    )
    try:
        temporary_entries = tuple(temporary_directory.iterdir())
    except OSError as exc:
        fail(f"cannot inspect case-local tmp directory: {exc}")
    if temporary_entries:
        fail("case-local tmp directory is not fresh and empty")

    child_environment = {
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin",
        "TMPDIR": str(temporary_directory),
    }
    output_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    output_flags |= getattr(os, "O_CLOEXEC", 0)

    try:
        descriptor = os.open(output_log, output_flags, 0o600)
    except OSError as exc:
        fail(f"cannot exclusively create merged log: {exc}")

    process: Optional[subprocess.Popen[bytes]] = None
    with deck.open("rb") as deck_stream, os.fdopen(
        descriptor,
        "wb",
    ) as log_stream:
        try:
            process = subprocess.Popen(
                [str(dragon)],
                cwd=str(case_directory),
                stdin=deck_stream,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
                env=child_environment,
                shell=False,
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            fail(f"cannot start frozen Dragon executable: {exc}")

        try:
            return_code = process.wait(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            terminate_exact_process_group(process)
            fail(
                f"timeout after {TIMEOUT_SECONDS} seconds; "
                "invalid with no scientific result"
            )
        except BaseException:
            if process.poll() is None:
                terminate_exact_process_group(process)
            raise

    if return_code != 0:
        fail(
            f"Dragon exit status {return_code}; "
            "invalid with no scientific result"
        )
    return return_code


def main() -> None:
    if len(sys.argv) != 4:
        fail("expected exactly DRAGON DECK LOG")
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, raise_termination_signal)
    try:
        run(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
        print(PASS_LINE)
    except TerminationSignal as exc:
        signal_name = signal.Signals(exc.signum).name
        fail(
            f"received {signal_name}; "
            "invalid with no scientific result"
        )


if __name__ == "__main__":
    main()

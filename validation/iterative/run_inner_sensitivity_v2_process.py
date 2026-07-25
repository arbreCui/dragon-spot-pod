#!/usr/bin/env python3
"""Run one Stage-4 v2 Dragon process with a 120 s process-group bound."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time
from typing import Optional


TIMEOUT_SECONDS = 120
TERM_GRACE_SECONDS = 5
MANAGED_SIGNALS = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)


class TerminationSignal(Exception):
    """A managed outer signal that must first terminate the child group."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


def fail(message: str) -> None:
    print("INNER-SENSITIVITY-V2 PROCESS FAIL: " + message, file=sys.stderr)
    raise SystemExit(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_regular(path: Path, owner: str, executable: bool = False) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
        fail(f"{owner} is not a regular non-symlink file")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve {owner}: {exc}")
    if executable and not os.access(resolved, os.X_OK):
        fail(f"{owner} is not executable")
    return resolved


def require_directory(path: Path, owner: str) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect {owner}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
        fail(f"{owner} is not a regular non-symlink directory")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve {owner}: {exc}")


def process_group_exists(process_group: int) -> bool:
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    process_group = process.pid
    try:
        os.killpg(process_group, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return
    deadline = time.monotonic() + TERM_GRACE_SECONDS
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


def raise_termination_signal(signum: int, _frame: object) -> None:
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, signal.SIG_IGN)
    raise TerminationSignal(signum)


def run(
    dragon_path: Path,
    deck_path: Path,
    work_dir: Path,
    log_path: Path,
    timeout_seconds: float = TIMEOUT_SECONDS,
) -> int:
    if not dragon_path.is_absolute():
        fail("Dragon path must be absolute")
    dragon = require_regular(dragon_path, "Dragon", executable=True)
    deck = require_regular(deck_path, "deck")
    work = require_directory(work_dir, "work directory")
    require(
        deck.parent == work,
        "deck must be directly inside the isolated work directory",
    )
    log_parent = require_directory(log_path.parent, "log parent")
    if log_parent != work:
        fail("log must be a direct child of the isolated work directory")
    if log_path.exists() or log_path.is_symlink():
        fail("refusing to overwrite the Dragon log")
    if timeout_seconds <= 0.0 or timeout_seconds > TIMEOUT_SECONDS:
        fail("timeout is outside the frozen 120 s bound")

    temporary = require_directory(work / "tmp", "case-local tmp directory")
    try:
        require(
            not tuple(temporary.iterdir()),
            "case-local tmp directory is not empty",
        )
    except OSError as exc:
        fail(f"cannot inspect case-local tmp directory: {exc}")
    child_environment = {
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin",
        "TMPDIR": str(temporary),
    }
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(log_path, flags, 0o600)
    except OSError as exc:
        fail(f"cannot exclusively create Dragon log: {exc}")

    process: Optional[subprocess.Popen[bytes]] = None
    with deck.open("rb") as deck_stream, os.fdopen(
        descriptor,
        "wb",
    ) as log_stream:
        try:
            process = subprocess.Popen(
                [str(dragon)],
                cwd=str(work),
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
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            terminate_group(process)
            fail(
                f"timeout after {timeout_seconds:g} seconds; "
                "INVALID-NO-SCIENTIFIC-RESULT"
            )
        except BaseException:
            if process.poll() is None:
                terminate_group(process)
            raise
    if return_code != 0:
        fail(
            f"Dragon exit status {return_code}; "
            "INVALID-NO-SCIENTIFIC-RESULT"
        )
    return return_code


def main() -> None:
    if len(sys.argv) != 5:
        fail("expected DRAGON DECK WORK-DIRECTORY LOG")
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, raise_termination_signal)
    try:
        run(
            Path(sys.argv[1]),
            Path(sys.argv[2]),
            Path(sys.argv[3]),
            Path(sys.argv[4]),
        )
        print("INNER-SENSITIVITY-V2 PROCESS PASS: one bounded process")
    except TerminationSignal as exc:
        signal_name = signal.Signals(exc.signum).name
        fail(
            f"received {signal_name}; "
            "INVALID-NO-SCIENTIFIC-RESULT"
        )


if __name__ == "__main__":
    main()

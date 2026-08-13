#!/usr/bin/env python3
"""Run one B2y child in a fresh process group with frozen resource caps."""

from __future__ import annotations

import ctypes
from contextlib import ExitStack
import errno
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


PROFILES = {
    "close": {
        "wall_seconds": 80,
        "cpu_seconds": 75,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 512 * 1024**2,
        "log_bytes": 64 * 1024**2,
    },
    "posterior": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 16 * 1024**2,
        "log_bytes": 16 * 1024**2,
    },
}
RESOURCE_CLASS = {
    "close": "INVALID-RUNTIME-BUDGET-NO-CLOSED-RESULT",
    "posterior": "INVALID-CLOSED-EVIDENCE",
}
EXIT_CLASS = {
    "close": "FAILED-NO-CLOSED",
    "posterior": "INVALID-CLOSED-EVIDENCE",
}
class ManagedInterruption(Exception):
    """A wrapper signal that requires terminating the owned process group."""

    def __init__(self, signal_number: int) -> None:
        super().__init__(f"managed wrapper signal {signal_number}")
        self.signal_number = signal_number


class CleanupState:
    """Idempotent record for one owned process-group cleanup."""

    def __init__(self) -> None:
        self.attempted = False
        self.outcome = "NOT-ATTEMPTED"


def fail(message: str) -> None:
    raise SystemExit(f"B2Y BOUNDED PROCESS FAILURE: {message}")


def require_regular(path: Path, executable: bool = False) -> Path:
    resolved = path.resolve(strict=True)
    if path.is_symlink() or not resolved.is_file():
        fail(f"not a regular non-symlink file: {path}")
    if executable and not os.access(resolved, os.X_OK):
        fail(f"not executable: {path}")
    return resolved


def set_limits(profile: dict[str, int]) -> None:
    resource.setrlimit(
        resource.RLIMIT_CPU,
        (profile["cpu_seconds"], profile["cpu_seconds"]),
    )
    resource.setrlimit(
        resource.RLIMIT_FSIZE,
        (profile["file_bytes"], profile["file_bytes"]),
    )
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def group_census(process_group: int) -> str:
    """Classify the owned group without claiming more than the kernel reports."""
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return "GROUP-ABSENT"
    except PermissionError:
        return "CLEANUP-UNVERIFIED-EPERM"
    except OSError as error:
        return f"CLEANUP-UNVERIFIED-ERRNO-{error.errno}"
    return "CLEANUP-UNVERIFIED-GROUP-PRESENT"


def terminate_group(
    process: subprocess.Popen[bytes], state: CleanupState
) -> str:
    """Immediately kill once; return a non-throwing, auditable cleanup state."""
    if state.attempted:
        return state.outcome
    state.attempted = True
    state.outcome = "CLEANUP-INCOMPLETE"
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        try:
            process.wait()
        except BaseException:
            pass
        state.outcome = "GROUP-ABSENT"
        return state.outcome
    except PermissionError:
        try:
            os.kill(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            try:
                process.wait()
            except BaseException:
                pass
        except (PermissionError, OSError):
            pass
        else:
            try:
                process.wait()
            except BaseException:
                pass
        state.outcome = group_census(process.pid)
        return state.outcome
    except OSError as error:
        state.outcome = f"CLEANUP-UNVERIFIED-ERRNO-{error.errno}"
        return state.outcome
    try:
        process.wait()
    except BaseException:
        state.outcome = "CLEANUP-UNVERIFIED-REAP-FAILURE"
        return state.outcome
    state.outcome = group_census(process.pid)
    return state.outcome


def fail_after_cleanup(
    process: subprocess.Popen[bytes],
    state: CleanupState,
    message: str,
) -> None:
    outcome = terminate_group(process, state)
    fail(f"{message}; CLEANUP={outcome}")


def kill_group_at_hard_deadline(
    process: subprocess.Popen[bytes], state: CleanupState
) -> str:
    """Stop computation immediately when the absolute wall deadline arrives."""
    return terminate_group(process, state)


class ProcTaskInfo(ctypes.Structure):
    _fields_ = [
        ("virtual_size", ctypes.c_uint64),
        ("resident_size", ctypes.c_uint64),
        ("total_user", ctypes.c_uint64),
        ("total_system", ctypes.c_uint64),
        ("threads_user", ctypes.c_uint64),
        ("threads_system", ctypes.c_uint64),
        ("policy", ctypes.c_int32),
        ("faults", ctypes.c_int32),
        ("pageins", ctypes.c_int32),
        ("cow_faults", ctypes.c_int32),
        ("messages_sent", ctypes.c_int32),
        ("messages_received", ctypes.c_int32),
        ("syscalls_mach", ctypes.c_int32),
        ("syscalls_unix", ctypes.c_int32),
        ("context_switches", ctypes.c_int32),
        ("thread_count", ctypes.c_int32),
        ("running_threads", ctypes.c_int32),
        ("priority", ctypes.c_int32),
    ]


def process_rss_bytes(pid: int) -> int:
    libproc = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    proc_pidinfo = libproc.proc_pidinfo
    proc_pidinfo.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_uint64,
        ctypes.c_void_p,
        ctypes.c_int,
    ]
    proc_pidinfo.restype = ctypes.c_int
    info = ProcTaskInfo()
    size = ctypes.sizeof(info)
    found = proc_pidinfo(pid, 4, 0, ctypes.byref(info), size)
    if found != size:
        raise OSError(ctypes.get_errno(), "proc_pidinfo failed")
    return int(info.resident_size)


def reap_esrch_exit(
    process: subprocess.Popen[bytes], hard_deadline: float
) -> int | None:
    """Reconcile an ESRCH exit race only inside the original wall budget."""
    remaining = hard_deadline - time.monotonic()
    if remaining <= 0:
        return None
    try:
        return process.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        return None


def wait_bounded(
    process: subprocess.Popen[bytes],
    profile: dict[str, int],
    log_path: Path,
    resource_class: str,
    hard_deadline: float,
    cleanup_state: CleanupState,
) -> int:
    while True:
        return_code = process.poll()
        if return_code is not None:
            return return_code
        remaining = hard_deadline - time.monotonic()
        if remaining <= 0:
            outcome = kill_group_at_hard_deadline(process, cleanup_state)
            fail(f"wall timeout; {resource_class}; CLEANUP={outcome}")
        try:
            rss_bytes = process_rss_bytes(process.pid)
        except OSError as census_error:
            return_code = process.poll()
            if return_code is not None:
                return return_code
            if census_error.errno == errno.ESRCH:
                return_code = reap_esrch_exit(process, hard_deadline)
                if return_code is not None:
                    return return_code
                remaining = hard_deadline - time.monotonic()
                if remaining <= 0:
                    outcome = kill_group_at_hard_deadline(
                        process, cleanup_state
                    )
                    fail(
                        f"wall timeout; {resource_class}; CLEANUP={outcome}"
                    )
            fail_after_cleanup(
                process, cleanup_state,
                f"RSS census failed; {resource_class}",
            )
        except (subprocess.SubprocessError, ValueError):
            return_code = process.poll()
            if return_code is not None:
                return return_code
            fail_after_cleanup(
                process, cleanup_state,
                f"RSS census failed; {resource_class}",
            )
        if rss_bytes > profile["rss_bytes"]:
            fail_after_cleanup(
                process, cleanup_state,
                f"RSS cap exceeded; {resource_class}",
            )
        try:
            log_bytes = log_path.stat().st_size
        except OSError:
            fail_after_cleanup(
                process, cleanup_state,
                f"log census failed; {resource_class}",
            )
        if log_bytes > profile["log_bytes"]:
            fail_after_cleanup(
                process, cleanup_state,
                f"log cap exceeded; {resource_class}",
            )
        remaining = hard_deadline - time.monotonic()
        if remaining <= 0:
            outcome = kill_group_at_hard_deadline(process, cleanup_state)
            fail(f"wall timeout; {resource_class}; CLEANUP={outcome}")
        time.sleep(min(0.05, remaining))


def run(
    profile_name: str,
    executable_path: Path,
    input_path: Path | None,
    log_path: Path,
    arguments: list[str],
) -> float:
    if profile_name not in PROFILES:
        fail(f"unknown profile: {profile_name}")
    profile = PROFILES[profile_name]
    executable = require_regular(executable_path, executable=True)
    input_file = None if input_path is None else require_regular(input_path)
    if log_path.exists() or log_path.is_symlink():
        fail(f"refusing to overwrite log: {log_path}")
    log_path.parent.resolve(strict=True)

    environment = os.environ.copy()
    environment.update(
        {
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "VECLIB_MAXIMUM_THREADS": "1",
        }
    )
    command = [str(executable), *arguments]
    start = time.monotonic()
    hard_deadline = start + profile["wall_seconds"]
    managed_signals = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)
    previous_handlers = {
        signal_number: signal.getsignal(signal_number)
        for signal_number in managed_signals
    }

    def interrupt_handler(signal_number: int, _frame: object) -> None:
        raise ManagedInterruption(signal_number)

    process: subprocess.Popen[bytes] | None = None
    cleanup_state = CleanupState()
    for signal_number in managed_signals:
        signal.signal(signal_number, interrupt_handler)
    try:
        with ExitStack() as stack:
            log_stream = stack.enter_context(log_path.open("xb"))
            input_stream = (
                subprocess.DEVNULL
                if input_file is None
                else stack.enter_context(input_file.open("rb"))
            )
            process = subprocess.Popen(
                command,
                cwd=str(
                    log_path.parent if input_file is None else input_file.parent
                ),
                stdin=input_stream,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env=environment,
                preexec_fn=lambda: set_limits(profile),
            )
            return_code = wait_bounded(
                process, profile, log_path, RESOURCE_CLASS[profile_name],
                hard_deadline, cleanup_state,
            )
    except ManagedInterruption as interruption:
        for signal_number in managed_signals:
            signal.signal(signal_number, signal.SIG_IGN)
        if process is not None and process.poll() is None:
            cleanup_outcome = terminate_group(process, cleanup_state)
        else:
            cleanup_outcome = cleanup_state.outcome
        fail(
            f"wrapper interrupted by signal {interruption.signal_number}; "
            f"{RESOURCE_CLASS[profile_name]}; CLEANUP={cleanup_outcome}"
        )
    except BaseException as primary_error:
        for signal_number in managed_signals:
            signal.signal(signal_number, signal.SIG_IGN)
        if process is not None:
            try:
                running = process.poll() is None
            except BaseException:
                running = True
            if running:
                cleanup_outcome = terminate_group(process, cleanup_state)
                if cleanup_outcome.startswith("CLEANUP-UNVERIFIED"):
                    primary_error.add_note(
                        f"B2y cleanup status: {cleanup_outcome}"
                    )
        raise
    finally:
        for signal_number, previous_handler in previous_handlers.items():
            signal.signal(signal_number, previous_handler)
    elapsed = time.monotonic() - start
    if return_code < 0:
        signal_number = -return_code
        managed_signals = {
            signal.SIGHUP,
            signal.SIGINT,
            signal.SIGKILL,
            signal.SIGTERM,
            signal.SIGXCPU,
            signal.SIGXFSZ,
        }
        classification = (
            RESOURCE_CLASS[profile_name]
            if signal_number in managed_signals
            else EXIT_CLASS[profile_name]
        )
        fail(f"terminated by signal {signal_number}; {classification}")
    if return_code != 0:
        fail(f"exit status {return_code}; {EXIT_CLASS[profile_name]}")
    if log_path.stat().st_size > profile["log_bytes"]:
        fail(f"log cap exceeded; {RESOURCE_CLASS[profile_name]}")
    return elapsed


def main() -> None:
    if len(sys.argv) < 5:
        fail("expected PROFILE EXECUTABLE INPUT-or-- LOG [ARG ...]")
    profile_name = sys.argv[1]
    executable = Path(sys.argv[2])
    input_path = None if sys.argv[3] == "-" else Path(sys.argv[3])
    log_path = Path(sys.argv[4])
    elapsed = run(profile_name, executable, input_path, log_path, sys.argv[5:])
    print(
        f"B2Y BOUNDED PROCESS PASS PROFILE={profile_name} "
        f"ELAPSED={elapsed:.3f}s"
    )


if __name__ == "__main__":
    main()

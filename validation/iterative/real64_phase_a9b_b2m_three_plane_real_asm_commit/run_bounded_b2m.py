#!/usr/bin/env python3
"""Run one B2m child in a fresh process group with frozen resource caps."""

from __future__ import annotations

import ctypes
from contextlib import ExitStack
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


PROFILES = {
    "prepare": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 512 * 1024**2,
        "log_bytes": 16 * 1024**2,
    },
    "assemble3": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
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
TERM_GRACE_SECONDS = 5
EXIT_CENSUS_GRACE_SECONDS = 0.1


def fail(message: str) -> None:
    raise SystemExit(f"B2M BOUNDED PROCESS INVALID: {message}")


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


def wait_bounded(
    process: subprocess.Popen[bytes], profile: dict[str, int]
) -> int:
    deadline = time.monotonic() + profile["wall_seconds"]
    while True:
        return_code = process.poll()
        if return_code is not None:
            return return_code
        try:
            rss_bytes = process_rss_bytes(process.pid)
        except (OSError, subprocess.SubprocessError, ValueError):
            return_code = process.poll()
            if return_code is not None:
                return return_code
            try:
                return process.wait(timeout=EXIT_CENSUS_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                pass
            terminate_group(process)
            fail("RSS census failed; INVALID-NO-SCIENTIFIC-RESULT")
        if rss_bytes > profile["rss_bytes"]:
            terminate_group(process)
            fail("RSS cap exceeded; INVALID-NO-SCIENTIFIC-RESULT")
        if time.monotonic() >= deadline:
            terminate_group(process)
            fail("wall timeout; INVALID-NO-SCIENTIFIC-RESULT")
        time.sleep(0.05)


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
    with ExitStack() as stack:
        log_stream = stack.enter_context(log_path.open("xb"))
        input_stream = (
            subprocess.DEVNULL
            if input_file is None
            else stack.enter_context(input_file.open("rb"))
        )
        process = subprocess.Popen(
            command,
            cwd=str(log_path.parent if input_file is None else input_file.parent),
            stdin=input_stream,
            stdout=log_stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=environment,
            preexec_fn=lambda: set_limits(profile),
        )
        return_code = wait_bounded(process, profile)
    elapsed = time.monotonic() - start
    if return_code != 0:
        fail(f"exit status {return_code}; INVALID-NO-SCIENTIFIC-RESULT")
    if log_path.stat().st_size > profile["log_bytes"]:
        fail("log cap exceeded; INVALID-NO-SCIENTIFIC-RESULT")
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
        f"B2M BOUNDED PROCESS PASS PROFILE={profile_name} "
        f"ELAPSED={elapsed:.3f}s"
    )


if __name__ == "__main__":
    main()

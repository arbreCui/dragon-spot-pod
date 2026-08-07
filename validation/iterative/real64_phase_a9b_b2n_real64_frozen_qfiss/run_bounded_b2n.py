#!/usr/bin/env python3
"""Run one non-Dragon B2n helper in one fresh, bounded process group.

The RSS ceiling is a 50 ms census of the direct child (the process-group
leader).  It is deliberately described as a sampled leader ceiling, not as a
hard or aggregate process-group memory limit.  Wall time, CPU time, file size,
and core-file limits are fixed independently.
"""

from __future__ import annotations

import ctypes
from contextlib import ExitStack
import os
from pathlib import Path
import resource
import signal
import stat
import subprocess
import sys
import time
from typing import Sequence


PROFILES = {
    "prepare": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 512 * 1024**2,
        "log_bytes": 16 * 1024**2,
    },
    "build": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 128 * 1024**2,
        "log_bytes": 16 * 1024**2,
    },
    "posterior": {
        "wall_seconds": 30,
        "cpu_seconds": 20,
        "rss_bytes": 2 * 1024**3,
        "file_bytes": 16 * 1024**2,
        "log_bytes": 16 * 1024**2,
    },
}

RSS_SAMPLE_SECONDS = 0.05
EXIT_CENSUS_GRACE_SECONDS = 0.10
TERM_GRACE_SECONDS = 5.0
KILL_CENSUS_GRACE_SECONDS = 1.0
MANAGED_SIGNALS = (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)

# Loader, language-startup, and shell-startup injection variables are never
# inherited by the scientific helper.  Build commands and input paths belong
# in the frozen command line, not in ambient process state.
DANGEROUS_ENVIRONMENT_NAMES = frozenset(
    {
        "BASH_ENV",
        "CDPATH",
        "ENV",
        "GCONV_PATH",
        "GLOBIGNORE",
        "IFS",
        "LD_LIBRARY_PATH",
        "LD_PRELOAD",
        "LOCPATH",
        "NLSPATH",
        "PERL5LIB",
        "PERL5OPT",
        "PYTHONHOME",
        "PYTHONINSPECT",
        "PYTHONPATH",
        "PYTHONSTARTUP",
        "PYTHONWARNINGS",
        "RUBYLIB",
        "RUBYOPT",
        "SHELLOPTS",
    }
)
DANGEROUS_ENVIRONMENT_PREFIXES = ("DYLD_",)
SINGLE_THREAD_ENVIRONMENT = {
    "BLIS_NUM_THREADS": "1",
    "CMAKE_BUILD_PARALLEL_LEVEL": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "RAYON_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}
SAFE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin"


class TerminationSignal(Exception):
    """A managed external signal that requires child-group cleanup first."""

    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


def fail(message: str) -> None:
    raise SystemExit(f"B2N BOUNDED PROCESS INVALID: {message}")


def path_exists_without_following(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as exc:
        fail(f"cannot inspect path {path}: {exc}")
    return True


def require_regular_non_symlink(
    path: Path, *, executable: bool = False
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


def require_directory_non_symlink(path: Path) -> Path:
    try:
        status = path.lstat()
    except OSError as exc:
        fail(f"cannot inspect output directory {path}: {exc}")
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
        fail(f"not a regular non-symlink directory: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve output directory {path}: {exc}")


def sanitized_environment() -> dict[str, str]:
    environment = {
        name: value
        for name, value in os.environ.items()
        if name not in DANGEROUS_ENVIRONMENT_NAMES
        and not name.startswith(DANGEROUS_ENVIRONMENT_PREFIXES)
    }
    environment.update(SINGLE_THREAD_ENVIRONMENT)
    environment.update({"LC_ALL": "C", "LANG": "C", "PATH": SAFE_PATH})
    # Prevent an inherited make jobserver or parallel flag from changing the
    # fixed single-process character of a standalone build helper.
    environment["MAKEFLAGS"] = "-j1"
    environment.pop("MFLAGS", None)
    environment.pop("MAKELEVEL", None)
    return environment


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
    """Return only the direct child/leader RSS, never an aggregate."""
    if sys.platform == "darwin":
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

    # This fallback keeps the no-Dragon unit tests usable on Linux while the
    # accepted macOS evidence continues to use proc_pidinfo above.
    statm = Path(f"/proc/{pid}/statm").read_text(encoding="ascii").split()
    return int(statm[1]) * resource.getpagesize()


def process_group_exists(process_group: int) -> bool:
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # The group may still exist even if a sandbox denies signal zero.
        return True
    return True


def wait_for_group_exit(process_group: int, seconds: float) -> bool:
    deadline = time.monotonic() + seconds
    while process_group_exists(process_group):
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.02)
    return True


def terminate_exact_process_group(process: subprocess.Popen[bytes]) -> bool:
    """TERM then KILL the exact fresh group; return whether it disappeared."""
    process_group = process.pid
    process.poll()
    try:
        os.killpg(process_group, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return True

    deadline = time.monotonic() + TERM_GRACE_SECONDS
    while time.monotonic() < deadline:
        process.poll()
        if not process_group_exists(process_group):
            process.wait()
            return True
        time.sleep(0.02)

    if process_group_exists(process_group):
        try:
            os.killpg(process_group, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait()
    return wait_for_group_exit(process_group, KILL_CENSUS_GRACE_SECONDS)


def fail_after_group_cleanup(
    process: subprocess.Popen[bytes], message: str
) -> None:
    cleaned = terminate_exact_process_group(process)
    if not cleaned:
        fail(f"{message}; process-group cleanup unverified")
    fail(message)


def completed_return_code(
    process: subprocess.Popen[bytes], return_code: int
) -> int:
    process_group = process.pid
    if not process_group_exists(process_group):
        return return_code
    if wait_for_group_exit(process_group, EXIT_CENSUS_GRACE_SECONDS):
        return return_code
    fail_after_group_cleanup(
        process,
        "leader exited with a lingering process-group member; "
        "INVALID-NO-SCIENTIFIC-RESULT",
    )
    raise AssertionError("unreachable")


def log_size_bytes(log_descriptor: int) -> int:
    return int(os.fstat(log_descriptor).st_size)


def wait_bounded(
    process: subprocess.Popen[bytes],
    profile: dict[str, int],
    log_descriptor: int,
) -> int:
    deadline = time.monotonic() + profile["wall_seconds"]
    while True:
        if log_size_bytes(log_descriptor) > profile["log_bytes"]:
            fail_after_group_cleanup(
                process,
                "live log cap exceeded; INVALID-NO-SCIENTIFIC-RESULT",
            )

        return_code = process.poll()
        if return_code is not None:
            return completed_return_code(process, return_code)

        try:
            rss_bytes = process_rss_bytes(process.pid)
        except (OSError, subprocess.SubprocessError, ValueError):
            return_code = process.poll()
            if return_code is None:
                try:
                    return_code = process.wait(
                        timeout=EXIT_CENSUS_GRACE_SECONDS
                    )
                except subprocess.TimeoutExpired:
                    fail_after_group_cleanup(
                        process,
                        "RSS census failed; INVALID-NO-SCIENTIFIC-RESULT",
                    )
            return completed_return_code(process, return_code)

        if rss_bytes > profile["rss_bytes"]:
            fail_after_group_cleanup(
                process,
                "sampled leader RSS cap exceeded; "
                "INVALID-NO-SCIENTIFIC-RESULT",
            )
        if time.monotonic() >= deadline:
            fail_after_group_cleanup(
                process,
                "wall timeout; INVALID-NO-SCIENTIFIC-RESULT",
            )
        time.sleep(RSS_SAMPLE_SECONDS)


def open_regular_input(path: Path):
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        fail(f"cannot open input file exclusively from symlinks: {exc}")
    status = os.fstat(descriptor)
    if not stat.S_ISREG(status.st_mode):
        os.close(descriptor)
        fail(f"input is no longer a regular file: {path}")
    return os.fdopen(descriptor, "rb")


def create_exclusive_log(path: Path) -> int:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(path, flags, 0o600)
    except OSError as exc:
        fail(f"refusing to overwrite or follow log {path}: {exc}")


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
    executable = require_regular_non_symlink(
        executable_path, executable=True
    )
    input_file = (
        None
        if input_path is None
        else require_regular_non_symlink(input_path)
    )
    log_parent = require_directory_non_symlink(log_path.parent)
    output_log = log_parent / log_path.name
    if not log_path.name or path_exists_without_following(output_log):
        fail(f"refusing to overwrite or follow log: {log_path}")

    command = [str(executable), *arguments]
    environment = sanitized_environment()
    working_directory = (
        log_parent if input_file is None else input_file.parent
    )
    start = time.monotonic()
    log_descriptor = create_exclusive_log(output_log)
    process: subprocess.Popen[bytes] | None = None

    with ExitStack() as stack:
        log_stream = stack.enter_context(os.fdopen(log_descriptor, "wb"))
        input_stream = (
            subprocess.DEVNULL
            if input_file is None
            else stack.enter_context(open_regular_input(input_file))
        )
        try:
            # Exactly one Popen call is permitted: B2n never retries a helper.
            process = subprocess.Popen(
                command,
                cwd=str(working_directory),
                stdin=input_stream,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                close_fds=True,
                shell=False,
                env=environment,
                preexec_fn=lambda: set_limits(profile),
            )
            return_code = wait_bounded(
                process, profile, log_stream.fileno()
            )
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            if process is not None and process_group_exists(process.pid):
                terminate_exact_process_group(process)
            fail(f"cannot execute helper: {exc}; INVALID-NO-SCIENTIFIC-RESULT")
        except BaseException:
            if process is not None and process_group_exists(process.pid):
                terminate_exact_process_group(process)
            raise

    elapsed = time.monotonic() - start
    if return_code != 0:
        fail(f"exit status {return_code}; INVALID-NO-SCIENTIFIC-RESULT")
    if output_log.stat().st_size > profile["log_bytes"]:
        fail("log cap exceeded; INVALID-NO-SCIENTIFIC-RESULT")
    return elapsed


def raise_termination_signal(signum: int, _frame: object) -> None:
    # Repeated signals cannot interrupt the cleanup caused by the first one.
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, signal.SIG_IGN)
    raise TerminationSignal(signum)


def main(arguments: Sequence[str] | None = None) -> None:
    argv = list(sys.argv[1:] if arguments is None else arguments)
    if len(argv) < 4:
        fail("expected PROFILE EXECUTABLE INPUT-or-- LOG [ARG ...]")
    previous_handlers = {
        managed_signal: signal.getsignal(managed_signal)
        for managed_signal in MANAGED_SIGNALS
    }
    for managed_signal in MANAGED_SIGNALS:
        signal.signal(managed_signal, raise_termination_signal)
    try:
        input_path = None if argv[2] == "-" else Path(argv[2])
        elapsed = run(
            argv[0], Path(argv[1]), input_path, Path(argv[3]), argv[4:]
        )
        print(
            f"B2N BOUNDED PROCESS PASS PROFILE={argv[0]} "
            f"ELAPSED={elapsed:.3f}s"
        )
    except TerminationSignal as exc:
        signal_name = signal.Signals(exc.signum).name
        fail(
            f"received {signal_name}; INVALID-NO-SCIENTIFIC-RESULT"
        )
    finally:
        for managed_signal, previous_handler in previous_handlers.items():
            signal.signal(managed_signal, previous_handler)


if __name__ == "__main__":
    main()

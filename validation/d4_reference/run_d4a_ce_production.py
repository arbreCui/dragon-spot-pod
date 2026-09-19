#!/usr/bin/env python3
"""Run the one frozen corrected D4-A continuous-energy production job."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
CANONICAL_BUILDER = HERE / "build_d4a_ce_reference.py"
PARTICLES = 20_000
BATCHES = 300
INACTIVE = 100
SEED = 731_942
THREADS = 18
TIMEOUT_SECONDS = 900
TERM_GRACE_SECONDS = 5.0
SUCCESS_RECEIPT = "result_receipt.sha256"
INCOMPLETE_MARKER = "PRODUCTION_INCOMPLETE"


class ProductionFailure(RuntimeError):
    """The frozen production run did not complete successfully."""


def build_command(
    output: Path,
    cross_sections: Path,
    openmc_exec: Path,
    builder: Path = CANONICAL_BUILDER,
) -> list[str]:
    return [
        sys.executable,
        str(builder),
        "--output", str(output),
        "--cross-sections", str(cross_sections),
        "--run",
        "--particles", str(PARTICLES),
        "--batches", str(BATCHES),
        "--inactive", str(INACTIVE),
        "--seed", str(SEED),
        "--threads", str(THREADS),
        "--openmc-exec", str(openmc_exec),
    ]


def process_group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def terminate_process_group(
    process: subprocess.Popen[bytes], grace_seconds: float
) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        process.wait()
        return
    deadline = time.monotonic() + grace_seconds
    while process_group_exists(process.pid) and time.monotonic() < deadline:
        process.poll()
        time.sleep(0.05)
    if process_group_exists(process.pid):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait()


def mark_incomplete(output: Path, reason: str) -> None:
    if output.is_dir():
        receipt = output / SUCCESS_RECEIPT
        if receipt.exists() or receipt.is_symlink():
            receipt.unlink()
    else:
        output.mkdir(parents=False, exist_ok=True)
    (output / INCOMPLETE_MARKER).write_text(
        f"INCOMPLETE: {reason}\n", encoding="utf-8"
    )


def run_production(
    output: Path,
    cross_sections: Path,
    openmc_exec: Path,
    *,
    builder: Path = CANONICAL_BUILDER,
    timeout_seconds: float = TIMEOUT_SECONDS,
    term_grace_seconds: float = TERM_GRACE_SECONDS,
) -> None:
    output = output.absolute()
    cross_sections = cross_sections.absolute()
    openmc_exec = openmc_exec.absolute()
    if output.exists() or output.is_symlink():
        raise ProductionFailure(f"output path must be fresh: {output}")
    if not output.parent.is_dir():
        raise ProductionFailure(f"output parent is not a directory: {output.parent}")
    if not builder.is_file():
        raise ProductionFailure(f"missing canonical builder: {builder}")
    if timeout_seconds <= 0.0 or term_grace_seconds < 0.0:
        raise ProductionFailure("invalid internal timeout controls")

    command = build_command(output, cross_sections, openmc_exec, builder)
    process = subprocess.Popen(command, start_new_session=True)
    try:
        return_code = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        terminate_process_group(process, term_grace_seconds)
        reason = "900-second process-group wall cap exceeded"
        mark_incomplete(output, reason)
        raise ProductionFailure(reason) from None
    except BaseException:
        terminate_process_group(process, term_grace_seconds)
        raise

    if return_code != 0:
        reason = f"builder exit status {return_code}"
        mark_incomplete(output, reason)
        raise ProductionFailure(reason)
    receipt = output / SUCCESS_RECEIPT
    if not receipt.is_file():
        reason = f"builder returned success without {SUCCESS_RECEIPT}"
        mark_incomplete(output, reason)
        raise ProductionFailure(reason)
    print(f"D4A CE PRODUCTION COMPLETE: {receipt}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the frozen corrected D4-A CE production protocol"
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cross-sections", required=True, type=Path)
    parser.add_argument("--openmc-exec", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_production(args.output, args.cross_sections, args.openmc_exec)


if __name__ == "__main__":
    try:
        main()
    except (ProductionFailure, OSError) as exc:
        print(f"D4A CE PRODUCTION INCOMPLETE: {exc}", file=sys.stderr)
        raise SystemExit(1)

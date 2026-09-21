#!/usr/bin/env python3
"""Format and seal corrected D4-A results after authoritative acceptance.

This read-only exporter neither runs a solver nor replaces
``check_d4a_corrected_acceptance.sh``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


FLOAT = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"
MAP_INPUTS = {
    "parent_axial_closed.xsm",
    "parent_snapshots_closed.xsm",
    "initial_radial_track.bin",
    "initial_axial_track.xsm",
    "initial_axial_macrolib.xsm",
    "basis_reference.xsm",
    "route_contract.xsm",
    "projected_proposal.xsm",
}
MAP_OUTPUTS = {
    "candidate_system.xsm",
    "candidate_radial.xsm",
    "candidate_axial.xsm",
    "candidate_snapshots.xsm",
    "closed_axial.xsm",
    "closed_snapshots.xsm",
}
OBSERVABLES = {
    "closed_axial.xsm",
    "initial_axial_track.xsm",
    "initial_axial_macrolib.xsm",
    "observables.x2m",
    "observables.log",
}


class ExportFailure(RuntimeError):
    """A required frozen receipt or unique physical record is invalid."""


def fail(message: str) -> None:
    raise ExportFailure(message)


def contains_or_equals(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail(f"cannot hash {path}: {exc}")
    return digest.hexdigest()


def read_text(path: Path, label: str) -> str:
    if not path.is_file() or path.is_symlink():
        fail(f"{label} is not a regular non-symlink file: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read {label}: {exc}")


def verify_receipt(receipt: Path, root: Path) -> dict[str, str]:
    lines = read_text(receipt, receipt.name).splitlines()
    if not lines:
        fail(f"empty receipt: {receipt.name}")
    entries: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if match is None:
            fail(f"malformed receipt line: {receipt.name}")
        expected, raw_name = match.groups()
        relative = Path(raw_name)
        name = relative.as_posix()
        if relative.is_absolute() or ".." in relative.parts or name in entries:
            fail(f"unsafe or duplicate receipt entry: {raw_name}")
        path = root / relative
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            fail(f"receipt hash mismatch: {receipt.name}: {raw_name}")
        entries[name] = expected
    return entries


def require_exact_inventory(root: Path, sealed: set[str], receipt_name: str) -> None:
    try:
        children = list(root.iterdir())
    except OSError as exc:
        fail(f"cannot inspect directory {root}: {exc}")
    if any(child.is_symlink() or not child.is_file() for child in children):
        fail(f"directory contains a link or non-regular entry: {root}")
    actual = {child.name for child in children}
    if actual != sealed | {receipt_name}:
        fail(f"directory inventory differs from {receipt_name}: {root}")


def unique_match(pattern: str, text: str, label: str) -> tuple[str, ...]:
    matches = re.findall(pattern, text, re.MULTILINE)
    if len(matches) != 1:
        fail(f"expected exactly one {label}")
    value = matches[0]
    return value if isinstance(value, tuple) else (value,)


def finite_number(token: str, label: str, *, positive: bool = False) -> float:
    try:
        value = float(token.replace("D", "E").replace("d", "e"))
    except ValueError:
        fail(f"{label} is not numeric")
    if not math.isfinite(value) or value < 0.0 or (positive and value == 0.0):
        fail(f"{label} is not physically admissible")
    return value


def parse_map(directory: Path) -> tuple[int, dict[str, float], dict[str, str]]:
    result_entries = verify_receipt(directory / "result.sha256", directory)
    require_exact_inventory(directory, set(result_entries), "result.sha256")
    required_sealed = {
        "portable_classification.txt",
        "input_manifest.sha256",
        "output_manifest.sha256",
        "prepare.log",
        "admission.log",
        "close.log",
        "independent_check.log",
        "gate.log",
    }
    if not required_sealed <= set(result_entries):
        fail("portable map receipt is missing required lifecycle evidence")

    role = read_text(
        directory / "portable_classification.txt", "portable classification"
    ).splitlines()
    if role != ["MAP_CLASSIFICATION=VALID_MET", "PORTABLE_ROLE=CONVERGED_MAP"]:
        fail("map is not the frozen VALID_MET/CONVERGED_MAP result")

    input_entries = verify_receipt(directory / "input_manifest.sha256", directory)
    output_entries = verify_receipt(directory / "output_manifest.sha256", directory)
    if set(input_entries) != MAP_INPUTS or set(output_entries) != MAP_OUTPUTS:
        fail("map input/output manifest inventory is not canonical")

    independent = read_text(
        directory / "independent_check.log", "independent map check"
    ).splitlines()
    if independent.count("ONE-MAP-XSM COMPLETE") != 1 or independent[-1:] != [
        "ONE-MAP-XSM COMPLETE"
    ]:
        fail("independent map check has no unique complete terminus")

    gate = read_text(directory / "gate.log", "convergence gate")
    if gate.splitlines().count("CLASSIFICATION=VALID_MET") != 1:
        fail("map convergence classification is not uniquely VALID_MET")
    if gate.splitlines().count("SPOT-GATE COMPLETE") != 1 or gate.splitlines()[-1:] != [
        "SPOT-GATE COMPLETE"
    ]:
        fail("map convergence gate has no unique complete terminus")
    residuals: dict[str, float] = {}
    for receipt_name, output_name in (
        ("RRHO", "Rrho"),
        ("RLEAK", "Rleak"),
        ("RA", "Ra"),
    ):
        token = unique_match(
            rf"^SPOT-GATE {receipt_name}\s+({FLOAT})\s+PASS\s*$",
            gate,
            f"passing {receipt_name} record",
        )[0]
        residuals[output_name] = finite_number(token, receipt_name)

    prepare = read_text(directory / "prepare.log", "prepare receipt")
    parent_epoch, projected_epoch = unique_match(
        r"^SPOT-R64 B2J CLOSED/(\d+) -> PROJECTED/(\d+)$",
        prepare,
        "CLOSED-to-PROJECTED epoch record",
    )
    close = read_text(directory / "close.log", "close receipt")
    (closed_epoch,) = unique_match(
        r"^SPOT-R64 CLOSED/(\d+) COMPLETE NO-TRANSPORT$",
        close,
        "CLOSED epoch record",
    )
    if not (
        int(parent_epoch) + 1 == int(projected_epoch) == int(closed_epoch)
    ):
        fail("map lifecycle epochs are inconsistent")
    admission = read_text(directory / "admission.log", "admission receipt")
    if admission.splitlines().count(
        "H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3"
    ) != 1:
        fail("map has no unique returned-state admission")

    receipt_hashes = {
        "map_result_receipt_sha256": sha256(directory / "result.sha256"),
        "map_input_manifest_sha256": sha256(directory / "input_manifest.sha256"),
        "map_output_manifest_sha256": sha256(directory / "output_manifest.sha256"),
    }
    return int(closed_epoch), residuals, receipt_hashes


def parse_observables(
    directory: Path, map_directory: Path
) -> tuple[float, list[float], list[str], str]:
    entries = verify_receipt(directory / "observables.sha256", directory)
    if set(entries) != OBSERVABLES:
        fail("observables receipt has the wrong file set")
    require_exact_inventory(directory, set(entries), "observables.sha256")

    for name in (
        "closed_axial.xsm",
        "initial_axial_track.xsm",
        "initial_axial_macrolib.xsm",
    ):
        if sha256(directory / name) != sha256(map_directory / name):
            fail(f"observables input does not match final map: {name}")
    canonical_deck = Path(__file__).with_name("d4a_corrected_final_observables.x2m")
    if sha256(directory / "observables.x2m") != sha256(canonical_deck):
        fail("observables deck is not the repository canonical deck")

    log = read_text(directory / "observables.log", "observables log")
    (k_token,) = unique_match(
        rf"^>\|D4A-CORRECTED-K-EFFECTIVE\s+({FLOAT})\s+\|>0011\s*$",
        log,
        "corrected k-effective record",
    )
    power_tokens = list(
        unique_match(
            rf"^SPORATE NU-FISSION-FRACTIONS\s+({FLOAT})\s+({FLOAT})\s+({FLOAT})\s*$",
            log,
            "normalized nu-fission fraction record",
        )
    )
    if log.count("normal end of execution for dragon") != 1:
        fail("observables log has no unique normal Dragon terminus")
    if re.search(
        r"D4A-MAP8|LEGACY|XABORT|ABORT:|FATAL|"
        r"SIG(?:SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error",
        log,
        re.IGNORECASE,
    ):
        fail("observables log contains a legacy or abnormal marker")
    k_effective = finite_number(k_token, "k-effective", positive=True)
    fractions = [
        finite_number(token, f"nu-fission fraction {index}")
        for index, token in enumerate(power_tokens, start=1)
    ]
    # This is the existing finite-width SPORATE receipt contract, unchanged.
    if not 0.99999995 <= math.fsum(fractions) <= 1.00000005:
        fail("three-floor nu-fission fractions are not globally normalized")
    return (
        k_effective,
        fractions,
        power_tokens,
        sha256(directory / "observables.sha256"),
    )


def export(map_directory: Path, observables: Path, output: Path) -> None:
    try:
        map_directory = map_directory.resolve(strict=True)
        observables = observables.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve an input directory: {exc}")
    if not map_directory.is_dir() or map_directory.is_symlink():
        fail("map directory is missing or is a symlink")
    if not observables.is_dir() or observables.is_symlink():
        fail("observables directory is missing or is a symlink")
    if output.exists() or output.is_symlink():
        fail("output directory must be fresh")
    try:
        output_parent = output.parent.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve output parent directory: {exc}")
    if not output_parent.is_dir():
        fail("output parent is not a directory")
    output = output_parent / output.name
    for input_directory, label in (
        (map_directory, "map"),
        (observables, "observables"),
    ):
        if contains_or_equals(input_directory, output) or contains_or_equals(
            output, input_directory
        ):
            fail(f"output and {label} directories must be disjoint")

    epoch, residuals, input_hashes = parse_map(map_directory)
    k_effective, fractions, power_tokens, observables_hash = parse_observables(
        observables, map_directory
    )
    input_hashes["observables_receipt_sha256"] = observables_hash
    result = {
        "map_epoch": epoch,
        "classification": "VALID_MET",
        **residuals,
        "k_effective": k_effective,
        "normalized_nu_fission_fractions": dict(
            zip(("bottom", "middle", "top"), fractions)
        ),
        "input_hashes": input_hashes,
    }

    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        (stage / "result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        with (stage / "power.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(("floor", "normalized_nu_fission_fraction"))
            writer.writerows(zip(("bottom", "middle", "top"), power_tokens))
        (stage / "export_result.sha256").write_text(
            f"{sha256(stage / 'result.json')}  result.json\n"
            f"{sha256(stage / 'power.csv')}  power.csv\n",
            encoding="utf-8",
        )
        os.replace(stage, output)
    except (OSError, TypeError, ValueError, ExportFailure) as exc:
        shutil.rmtree(stage, ignore_errors=True)
        if isinstance(exc, ExportFailure):
            raise
        fail(f"cannot publish result interface: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Format and seal machine-readable values only after "
            "check_d4a_corrected_acceptance.sh has passed; this exporter does "
            "not replace that authoritative acceptance"
        )
    )
    parser.add_argument("map", type=Path, help="frozen VALID_MET portable map")
    parser.add_argument("observables", type=Path, help="sealed observables directory")
    parser.add_argument("output", type=Path, help="fresh output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    export(args.map.resolve(), args.observables.resolve(), args.output.absolute())
    print(f"D4A CORRECTED RESULT EXPORT PASS: {args.output.absolute()}")


if __name__ == "__main__":
    try:
        main()
    except ExportFailure as exc:
        print(f"D4A CORRECTED RESULT EXPORT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

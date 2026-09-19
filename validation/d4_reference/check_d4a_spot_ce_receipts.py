#!/usr/bin/env python3
"""Read-only, fail-closed comparison of sealed corrected D4-A results."""

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
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SPOT_ACCEPTANCE = ROOT / "validation/iterative/check_d4a_corrected_acceptance.sh"
SPOT_CHECKER_DIR = ROOT / "validation/iterative"
CE_STATIC_CHECKER = Path(__file__).with_name("check_d4a_ce_static.py")
N_FLOORS = 3
N_PINS = 217
N_BINS = N_FLOORS * N_PINS
OPENMC_PYTHON_CRITICAL_FILES = {
    "__init__.py",
    "executor.py",
    "statepoint.py",
    "tallies.py",
    "model/model.py",
}
SPOT_FILES = {
    "closed_axial.xsm",
    "initial_axial_track.xsm",
    "initial_axial_macrolib.xsm",
    "observables.x2m",
    "observables.log",
}
SIGMA_LIMIT_PCM = 50.0
REACTIVITY_BASE_LIMIT_PCM = 500.0
SIGMA_MULTIPLIER = 3.0
FLOAT = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?"


class ComparisonFailure(RuntimeError):
    """A malformed, unsealed, or physically inadmissible receipt."""


def fail(message: str) -> None:
    raise ComparisonFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_python_tree(root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*.py") if path.is_file())
    if not files:
        fail(f"OpenMC Python package contains no sources: {root}")
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def executable_version(path: Path) -> tuple[str, list[int], str | None]:
    try:
        completed = subprocess.run(
            [str(path), "--version"],
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        fail(f"cannot query sealed OpenMC executable: {exc}")
    text = completed.stdout
    if completed.returncode != 0 or not text.strip():
        detail = completed.stderr.strip() or "no version text"
        fail(f"sealed OpenMC executable --version failed: {detail}")
    match = re.search(
        r"^OpenMC version (\d+)\.(\d+)\.(\d+)(?:-dev\d+)?$",
        text,
        re.MULTILINE,
    )
    if match is None:
        fail("sealed OpenMC executable version text is malformed")
    commit = re.search(r"^Commit hash: ([0-9a-fA-F]{7,64})$", text, re.MULTILINE)
    return (
        text,
        [int(value) for value in match.groups()],
        commit.group(1).lower() if commit is not None else None,
    )


def validate_runtime_environment(
    runtime,
    executable_override: str | None,
    openmc_module=None,
) -> Path:
    """Replay sealed runtime identity; relocation requires an explicit override."""
    if (not isinstance(runtime, dict) or
            runtime.get("schema") != "D4A_OPENMC_RUNTIME_PROVENANCE_V1"):
        fail("CE production runtime provenance is missing or malformed")
    executable_record = runtime.get("executable")
    package_record = runtime.get("python_package")
    if not isinstance(executable_record, dict) or not isinstance(package_record, dict):
        fail("CE production runtime provenance records are malformed")

    identifier = (
        executable_override
        if executable_override is not None
        else executable_record.get("resolved_path")
    )
    if not isinstance(identifier, str) or not identifier:
        fail("sealed OpenMC executable path is missing")
    located = shutil.which(identifier)
    if located is None:
        if executable_override is None:
            fail(
                "sealed OpenMC executable moved; provide explicit --openmc-exec "
                "for a same-hash relocation"
            )
        fail(f"cannot resolve OpenMC executable override: {identifier}")
    executable = Path(located).resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        fail(f"OpenMC executable is not executable: {executable}")
    if sha256(executable) != executable_record.get("sha256"):
        fail("OpenMC executable hash differs from production provenance")
    version_text, version, git_sha1 = executable_version(executable)
    if (version_text != executable_record.get("version_text") or
            hashlib.sha256(version_text.encode("utf-8")).hexdigest() !=
            executable_record.get("version_text_sha256") or
            version != executable_record.get("openmc_version") or
            git_sha1 != executable_record.get("git_sha1")):
        fail("OpenMC executable version identity differs from production provenance")

    if openmc_module is None:
        try:
            import openmc as openmc_module
        except ImportError as exc:
            fail(f"OpenMC Python API is required to audit provenance: {exc}")
    module_file = getattr(openmc_module, "__file__", None)
    package_version = getattr(openmc_module, "__version__", None)
    if not isinstance(module_file, str) or not isinstance(package_version, str):
        fail("OpenMC Python package identity is unavailable")
    package_root = Path(module_file).resolve(strict=True).parent
    if package_version != package_record.get("version"):
        fail("OpenMC Python package version differs from production provenance")
    critical = package_record.get("critical_files")
    if not isinstance(critical, dict) or set(critical) != OPENMC_PYTHON_CRITICAL_FILES:
        fail("OpenMC Python critical-file provenance differs")
    for relative, expected in critical.items():
        path = package_root / relative
        if not path.is_file() or sha256(path) != expected:
            fail(f"OpenMC Python critical file differs: {relative}")
    if (package_record.get("stable_hash_rule") !=
            "sorted *.py: relative-posix NUL content NUL" or
            sha256_python_tree(package_root) !=
            package_record.get("stable_python_tree_sha256")):
        fail("OpenMC Python package tree differs from production provenance")
    return executable


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def verify_receipt(receipt: Path, root: Path) -> set[str]:
    try:
        lines = receipt.read_text().splitlines()
    except OSError as exc:
        fail(f"cannot read receipt {receipt}: {exc}")
    if not lines:
        fail(f"empty receipt: {receipt}")
    names: set[str] = set()
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if match is None:
            fail(f"malformed receipt line: {receipt}")
        expected, name = match.groups()
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name in names:
            fail(f"unsafe or duplicate receipt entry: {name}")
        path = root / relative
        if not path.is_file() or sha256(path) != expected:
            fail(f"receipt hash mismatch: {name}")
        names.add(name)
    return names


def finite_positive(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        fail(f"{label} is not numeric")
    if not math.isfinite(number) or number <= 0.0:
        fail(f"{label} is not finite and positive")
    return number


def fractions(values, label: str, printed: bool = False) -> list[float]:
    if not isinstance(values, (list, tuple)) or len(values) != 3:
        fail(f"{label} does not contain exactly three floors")
    result = []
    for index, value in enumerate(values, start=1):
        try:
            number = float(value)
        except (TypeError, ValueError):
            fail(f"{label} floor {index} is not numeric")
        if not math.isfinite(number) or number < 0.0:
            fail(f"{label} floor {index} is invalid")
        result.append(number)
    total = math.fsum(result)
    # SPORATE prints a finite-width record.  Reuse its already frozen receipt
    # contract; JSON values are required to close to one within floating ULPs.
    if printed:
        if not 0.99999995 <= total <= 1.00000005:
            fail(f"{label} is not globally normalized")
    elif abs(total - 1.0) > 8.0 * math.ulp(1.0):
        fail(f"{label} is not globally normalized")
    return result


def run_spot_acceptance(
    corrected_build: Path,
    maps: list[Path],
    observables: Path,
) -> None:
    """Replay the authoritative corrected lineage and XSM/gate checkers."""
    if not SPOT_ACCEPTANCE.is_file():
        fail(f"SPOT acceptance checker is missing: {SPOT_ACCEPTANCE}")
    if not maps:
        fail("at least one ordered corrected SPOT map is required")
    command = [
        "sh",
        str(SPOT_ACCEPTANCE),
        str(corrected_build),
        *(str(path) for path in maps),
    ]
    environment = os.environ.copy()
    environment["D4A_OBSERVABLES_DIR"] = str(observables)
    # The release verifier must replay the repository's admitted binaries;
    # an inherited test override may not substitute checker executables.
    environment["CHECKER_DIR"] = str(SPOT_CHECKER_DIR)
    try:
        completed = subprocess.run(
            command,
            env=environment,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        fail(f"corrected SPOT acceptance replay failed to run: {exc}")
    marker = "D4A-CORRECTED-ACCEPT OVERALL PASS"
    if completed.returncode != 0 or completed.stdout.splitlines().count(marker) != 1:
        detail = completed.stdout.strip().splitlines()
        terminal = detail[-1] if detail else completed.stderr.strip() or "no output"
        fail(f"corrected SPOT lineage/XSM acceptance failed: {terminal}")


def read_spot(directory: Path) -> tuple[float, list[float]]:
    if not directory.is_dir():
        fail(f"SPOT observables directory is missing: {directory}")
    names = verify_receipt(directory / "observables.sha256", directory)
    if names != SPOT_FILES:
        fail("SPOT observables receipt has the wrong file set")
    try:
        log = (directory / "observables.log").read_text()
    except OSError as exc:
        fail(f"cannot read SPOT observables log: {exc}")
    k_matches = re.findall(
        rf"^>\|D4A-CORRECTED-K-EFFECTIVE\s+({FLOAT})\s*$",
        log,
        re.MULTILINE,
    )
    p_matches = re.findall(
        rf"^SPORATE NU-FISSION-FRACTIONS\s+({FLOAT})\s+({FLOAT})\s+({FLOAT})\s*$",
        log,
        re.MULTILINE,
    )
    if len(k_matches) != 1 or len(p_matches) != 1:
        fail("SPOT log does not contain exactly one corrected k and power row")
    if log.count("normal end of execution for dragon") != 1:
        fail("SPOT observables did not end normally")
    if re.search(
        r"D4A-MAP8|LEGACY|XABORT|ABORT:|FATAL|fortran runtime error",
        log,
        re.IGNORECASE,
    ):
        fail("SPOT log contains a legacy or abnormal marker")
    k_spot = finite_positive(
        k_matches[0].replace("D", "E").replace("d", "e"), "SPOT k"
    )
    power = fractions(
        [value.replace("D", "E").replace("d", "e") for value in p_matches[0]],
        "SPOT floor power",
        printed=True,
    )
    return k_spot, power


def run_ce_static_audit(directory: Path, cross_sections: Path) -> None:
    if not CE_STATIC_CHECKER.is_file():
        fail(f"CE static checker is missing: {CE_STATIC_CHECKER}")
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(CE_STATIC_CHECKER),
                str(directory),
                "--cross-sections",
                str(cross_sections),
            ],
            text=True,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        fail(f"CE static audit failed to run: {exc}")
    marker = "D4A CE STATIC PASS:"
    if (completed.returncode != 0 or
            sum(line.startswith(marker) for line in completed.stdout.splitlines()) != 1):
        detail = completed.stderr.strip() or completed.stdout.strip() or "no output"
        fail(f"CE static audit failed: {detail.splitlines()[-1]}")


def read_pin_map(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as exc:
        fail(f"cannot read CE pin map: {exc}")
    return rows


def recompute_ce_result(
    keff: float,
    sigma_k: float,
    cell_bins,
    means,
    standard_deviations,
    pin_rows: list[dict[str, str]],
) -> dict:
    """Independently reconstruct the production JSON with an explicit sum."""
    keff = finite_positive(keff, "statepoint k")
    sigma_k = finite_positive(sigma_k, "statepoint k standard deviation")
    if len(pin_rows) != N_BINS:
        fail(f"pin map has {len(pin_rows)} rows, expected {N_BINS}")

    by_cell: dict[int, dict[str, int]] = {}
    floor_pins: set[tuple[int, int]] = set()
    for row in pin_rows:
        try:
            cell_id = int(row["fuel_cell_id"])
            floor = int(row["floor"])
            pin_index = int(row["pin_index"])
            ring = int(row["ring_from_center"])
        except (KeyError, TypeError, ValueError) as exc:
            fail(f"pin map row is malformed: {exc}")
        if (cell_id in by_cell or floor not in range(1, N_FLOORS + 1) or
                pin_index not in range(N_PINS) or ring not in range(9) or
                (floor, pin_index) in floor_pins):
            fail("pin map does not contain 651 unique cell/floor/pin mappings")
        by_cell[cell_id] = {
            "floor": floor,
            "pin_index": pin_index,
            "ring_from_center": ring,
        }
        floor_pins.add((floor, pin_index))
    expected_floor_pins = {
        (floor, pin) for floor in range(1, N_FLOORS + 1)
        for pin in range(N_PINS)
    }
    if floor_pins != expected_floor_pins:
        fail("pin map floor/pin coverage differs")

    try:
        cells = [int(value) for value in cell_bins]
        rates = [float(value) for value in means]
        deviations = [float(value) for value in standard_deviations]
    except (TypeError, ValueError) as exc:
        fail(f"statepoint tally is malformed: {exc}")
    if (len(cells) != N_BINS or len(rates) != N_BINS or
            len(deviations) != N_BINS or len(set(cells)) != N_BINS or
            set(cells) != set(by_cell)):
        fail("statepoint CellFilter and pin map are not the same 651 bins")
    if not all(math.isfinite(value) and value >= 0.0 for value in rates):
        fail("statepoint nu-fission means are non-finite or negative")
    if not all(math.isfinite(value) and value >= 0.0 for value in deviations):
        fail("statepoint nu-fission standard deviations are invalid")

    # Both producer and checker use math.fsum over the statepoint CellFilter
    # order.  There is no tolerance or alternative normalization convention.
    total = math.fsum(rates)
    if not math.isfinite(total) or total <= 0.0:
        fail("statepoint global nu-fission is not finite and positive")
    floor_rates = [
        math.fsum(
            rate for cell_id, rate in zip(cells, rates)
            if by_cell[cell_id]["floor"] == floor
        )
        for floor in range(1, N_FLOORS + 1)
    ]
    bins = []
    for cell_id, rate, deviation in zip(cells, rates, deviations):
        row = by_cell[cell_id]
        bins.append({
            "floor": row["floor"],
            "pin_index": row["pin_index"],
            "ring_from_center": row["ring_from_center"],
            "fuel_cell_id": cell_id,
            "nu_fission": rate,
            "nu_fission_std_dev": deviation,
            "global_fraction": rate / total,
        })
    return {
        "schema": "D4A_CORRECTED_CE_RESULT_V1",
        "keff": keff,
        "keff_standard_deviation": sigma_k,
        "global_nu_fission": total,
        "floor_nu_fission_fractions": [value / total for value in floor_rates],
        "bins": bins,
    }


def exact_float(actual, expected, label: str) -> None:
    if (isinstance(actual, bool) or not isinstance(actual, (int, float)) or
            not math.isfinite(float(actual)) or
            float(actual).hex() != float(expected).hex()):
        fail(f"{label} differs from the sealed statepoint")


def compare_ce_result_exact(actual, expected) -> None:
    top_fields = {
        "schema",
        "keff",
        "keff_standard_deviation",
        "global_nu_fission",
        "floor_nu_fission_fractions",
        "bins",
    }
    if not isinstance(actual, dict) or set(actual) != top_fields:
        fail("CE result field set differs")
    if actual.get("schema") != expected["schema"]:
        fail("CE result schema differs")
    for name in ("keff", "keff_standard_deviation", "global_nu_fission"):
        exact_float(actual.get(name), expected[name], f"CE result {name}")
    fractions_actual = actual.get("floor_nu_fission_fractions")
    if not isinstance(fractions_actual, list) or len(fractions_actual) != N_FLOORS:
        fail("CE result floor fractions differ")
    for floor, (left, right) in enumerate(
        zip(fractions_actual, expected["floor_nu_fission_fractions"]), start=1
    ):
        exact_float(left, right, f"CE result floor {floor} fraction")

    bins_actual = actual.get("bins")
    bins_expected = expected["bins"]
    if not isinstance(bins_actual, list) or len(bins_actual) != N_BINS:
        fail("CE result does not contain exactly 651 statepoint bins")
    integer_fields = {"floor", "pin_index", "ring_from_center", "fuel_cell_id"}
    float_fields = {"nu_fission", "nu_fission_std_dev", "global_fraction"}
    required = integer_fields | float_fields
    for index, (left, right) in enumerate(zip(bins_actual, bins_expected)):
        if not isinstance(left, dict) or set(left) != required:
            fail(f"CE result bin {index} field set differs")
        for name in integer_fields:
            if type(left.get(name)) is not int or left[name] != right[name]:
                fail(f"CE result bin {index} {name} differs")
        for name in float_fields:
            exact_float(left.get(name), right[name], f"CE result bin {index} {name}")


def _decoded(value):
    if isinstance(value, bytes):
        return value.decode()
    if hasattr(value, "item"):
        value = value.item()
        if isinstance(value, bytes):
            return value.decode()
    return value


def _statepoint_energy_mode(state) -> str:
    if hasattr(state, "energy_mode"):
        return str(_decoded(state.energy_mode))
    handle = getattr(state, "_f", None)
    if handle is None or "energy_mode" not in handle:
        fail("statepoint does not expose energy_mode")
    return str(_decoded(handle["energy_mode"][()]))


def _statepoint_git_sha1(state) -> str | None:
    for name in ("git_sha1", "git_sha"):
        if hasattr(state, name):
            value = _decoded(getattr(state, name))
            return str(value).lower() if value else None
    handle = getattr(state, "_f", None)
    if handle is not None and "git_sha1" in handle.attrs:
        value = _decoded(handle.attrs["git_sha1"])
        return str(value).lower() if value else None
    return None


def validate_statepoint_contract(state, tally, execution: dict, runtime: dict) -> None:
    executable = runtime.get("executable", {})
    expected_version = executable.get("openmc_version")
    try:
        state_version = [int(value) for value in state.version]
        controls = {
            "particles": int(state.n_particles),
            "batches": int(state.n_batches),
            "inactive": int(state.n_inactive),
            "seed": int(state.seed),
        }
        current_batch = int(state.current_batch)
        n_realizations = int(state.n_realizations)
    except (AttributeError, TypeError, ValueError) as exc:
        fail(f"statepoint metadata is incomplete: {exc}")
    if state_version != expected_version:
        fail("statepoint OpenMC version differs from production executable")
    expected_git = executable.get("git_sha1")
    state_git = _statepoint_git_sha1(state)
    if state_git != expected_git:
        fail("statepoint OpenMC git SHA differs from production executable")
    if _statepoint_energy_mode(state) != "continuous-energy":
        fail("statepoint energy_mode is not continuous-energy")
    if state.run_mode != "eigenvalue" or any(
        controls[name] != execution.get(name) for name in controls
    ):
        fail("statepoint execution controls differ from the model contract")
    if current_batch != execution.get("batches"):
        fail("statepoint current_batch is not the final batch")
    if n_realizations != execution.get("batches") - execution.get("inactive"):
        fail("statepoint n_realizations differs from batches minus inactive")
    if (list(tally.scores) != ["nu-fission"] or
            tally.estimator != "tracklength" or
            list(tally.nuclides) != ["total"] or
            len(tally.filters) != 1 or
            type(tally.filters[0]).__name__ != "CellFilter"):
        fail("statepoint tally metadata differs from the production contract")


def read_statepoint_result(
    statepoint: Path,
    pin_rows: list[dict[str, str]],
    execution: dict | None = None,
    runtime: dict | None = None,
) -> dict:
    try:
        import numpy as np
        import openmc
    except ImportError as exc:
        fail(f"OpenMC Python API is required to audit the statepoint: {exc}")
    try:
        with openmc.StatePoint(statepoint, autolink=False) as state:
            if execution is not None:
                if runtime is None:
                    fail("statepoint runtime provenance is required")
            keff = float(state.keff.nominal_value)
            sigma_k = float(state.keff.std_dev)
            tally = state.get_tally(name="d4a_floor_pin_nu_fission")
            if execution is not None:
                validate_statepoint_contract(state, tally, execution, runtime)
            means = tally.get_values(
                scores=["nu-fission"], value="mean"
            ).reshape(-1)
            deviations = tally.get_values(
                scores=["nu-fission"], value="std_dev"
            ).reshape(-1)
            cell_bins = [int(value) for value in np.ravel(tally.filters[0].bins)]
    except ComparisonFailure:
        raise
    except Exception as exc:
        fail(f"cannot read sealed OpenMC statepoint: {exc}")
    return recompute_ce_result(
        keff, sigma_k, cell_bins, means, deviations, pin_rows
    )


def read_ce(
    directory: Path,
    cross_sections: Path,
    executable_override: str | None = None,
) -> tuple[float, float, list[float]]:
    if not directory.is_dir():
        fail(f"CE result directory is missing: {directory}")
    source_names = verify_receipt(
        directory / "source_manifest.sha256", directory
    )
    if source_names != {"source_manifest.json"}:
        fail("CE source-manifest receipt has the wrong file set")
    result_names = verify_receipt(directory / "result_receipt.sha256", directory)
    if "reference_result.json" not in result_names or len(result_names) != 2:
        fail("CE result receipt must seal one statepoint and reference_result.json")
    statepoints = [
        name for name in result_names
        if re.fullmatch(r"statepoint\.\d+\.h5", name)
    ]
    if len(statepoints) != 1:
        fail("CE result receipt does not seal exactly one final statepoint")

    run_ce_static_audit(directory, cross_sections)

    contract = load_json(directory / "model_contract.json")
    if (contract.get("schema") != "D4A_CORRECTED_CE_REFERENCE_V1" or
            contract.get("result_role") != "PRODUCTION_INPUT"):
        fail("CE model contract is not a corrected production input")
    execution = contract.get("execution", {})
    if execution.get("mode") != "RUN":
        fail("CE execution contract is not RUN")
    runtime = contract.get("runtime_provenance")
    validate_runtime_environment(runtime, executable_override)
    batches = execution.get("batches")
    if (not isinstance(batches, int) or batches <= 1 or
            statepoints[0] != f"statepoint.{batches}.h5"):
        fail("CE final statepoint does not match the sealed batch count")

    pin_rows = read_pin_map(directory / "pin_map.csv")
    recomputed = read_statepoint_result(
        directory / statepoints[0], pin_rows, execution, runtime
    )
    result = load_json(directory / "reference_result.json")
    compare_ce_result_exact(result, recomputed)
    return (
        recomputed["keff"],
        recomputed["keff_standard_deviation"],
        recomputed["floor_nu_fission_fractions"],
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare sealed corrected D4-A SPOT and CE receipts"
    )
    parser.add_argument("--corrected-build", required=True, type=Path)
    parser.add_argument(
        "--spot-map",
        required=True,
        action="append",
        type=Path,
        help="one corrected map in epoch order; repeat for every map",
    )
    parser.add_argument("--spot-observables", required=True, type=Path)
    parser.add_argument("--ce-result", required=True, type=Path)
    parser.add_argument("--cross-sections", required=True, type=Path)
    parser.add_argument(
        "--openmc-exec",
        help=(
            "explicit relocated OpenMC executable; accepted only when its "
            "SHA-256 and version identity match the production receipt"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    corrected_build = args.corrected_build.resolve()
    maps = [path.resolve() for path in args.spot_map]
    observables = args.spot_observables.resolve()
    cross_sections = args.cross_sections.resolve()
    run_spot_acceptance(corrected_build, maps, observables)
    print("D4A SPOT CORRECTED LINEAGE REPLAY PASS")
    k_spot, spot_power = read_spot(observables)
    k_ce, sigma_k, ce_power = read_ce(
        args.ce_result.resolve(), cross_sections, args.openmc_exec
    )
    print("D4A CE STATIC AND STATEPOINT REPLAY PASS")

    sigma_pcm = 1.0e5 * sigma_k / (k_ce * k_ce)
    delta_rho_pcm = 1.0e5 * abs(1.0 / k_spot - 1.0 / k_ce)
    rho_limit_pcm = REACTIVITY_BASE_LIMIT_PCM + SIGMA_MULTIPLIER * sigma_pcm
    sigma_ok = sigma_pcm <= SIGMA_LIMIT_PCM
    rho_ok = delta_rho_pcm <= rho_limit_pcm

    print(
        f"D4A SPOT-CE K: spot={k_spot:.17g} ce={k_ce:.17g} "
        f"sigma_k={sigma_k:.17g}"
    )
    print(
        f"D4A SPOT-CE SIGMA_PCM: value={sigma_pcm:.9g} "
        f"limit={SIGMA_LIMIT_PCM:.9g} "
        f"status={'PASS' if sigma_ok else 'FAIL'}"
    )
    print(
        f"D4A SPOT-CE DELTA_RHO_PCM: value={delta_rho_pcm:.9g} "
        f"limit={rho_limit_pcm:.9g} "
        f"status={'PASS' if rho_ok else 'FAIL'}"
    )
    labels = ("bottom", "middle", "top")
    differences = []
    for label, spot, ce in zip(labels, spot_power, ce_power):
        delta = spot - ce
        differences.append(delta)
        print(
            f"D4A SPOT-CE POWER-DIFFERENCE floor={label} "
            f"spot={spot:.17g} ce={ce:.17g} delta={delta:.17g}"
        )
    print(
        "D4A SPOT-CE POWER-DIFFERENCE "
        f"max_abs={max(abs(value) for value in differences):.17g} "
        "status=REPORTED_ONLY"
    )
    if not sigma_ok:
        fail("CE eigenvalue uncertainty exceeds 50 pcm")
    if not rho_ok:
        fail("SPOT-CE reactivity difference exceeds 500 pcm + 3 sigma")
    print("D4A SPOT-CE RECEIPT COMPARISON PASS")


if __name__ == "__main__":
    try:
        main()
    except (ComparisonFailure, OSError) as exc:
        print(f"D4A SPOT-CE RECEIPT COMPARISON FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

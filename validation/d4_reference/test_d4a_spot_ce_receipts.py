#!/usr/bin/env python3
"""Transport-free unit and fail-closed tests for the receipt comparator."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import math
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace


HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_d4a_spot_ce_receipts.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("d4a_receipt_checker", CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load receipt checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expect_refusal(module, callback, label: str) -> None:
    try:
        callback()
    except module.ComparisonFailure:
        return
    raise RuntimeError(f"{label} was not refused")


def write_receipt(module, directory: Path, names: tuple[str, ...]) -> None:
    (directory / "observables.sha256").write_text(
        "".join(
            f"{module.sha256(directory / name)}  {name}\n" for name in names
        )
    )


def make_spot_observables(
    module, directory: Path, *, trailer: str = "|>0011", abnormal: str = ""
) -> None:
    directory.mkdir()
    for name in (
        "closed_axial.xsm",
        "initial_axial_track.xsm",
        "initial_axial_macrolib.xsm",
    ):
        (directory / name).write_text(f"synthetic {name}\n")
    (directory / "observables.x2m").write_text("synthetic deck\n")
    (directory / "observables.log").write_text(
        f">|D4A-CORRECTED-K-EFFECTIVE 1.2 {trailer}\n"
        "SPORATE NU-FISSION-FRACTIONS 0.3 0.4 0.3\n"
        "normal end of execution for dragon\n"
        f"{abnormal}"
    )
    write_receipt(
        module,
        directory,
        (
            "closed_axial.xsm",
            "initial_axial_track.xsm",
            "initial_axial_macrolib.xsm",
            "observables.x2m",
            "observables.log",
        ),
    )


def pin_rows():
    rows = []
    for floor in range(1, 4):
        for pin in range(217):
            rows.append({
                "floor": str(floor),
                "pin_index": str(pin),
                "ring_from_center": str(min(8, pin // 25)),
                "fuel_cell_id": str(10000 + (floor - 1) * 217 + pin),
            })
    return rows


def test_exact_reconstruction(module) -> None:
    rows = pin_rows()
    cells = [int(row["fuel_cell_id"]) for row in rows]
    means = [float(1 + index % 19) for index in range(651)]
    deviations = [float(index + 1) / 1.0e6 for index in range(651)]
    expected = module.recompute_ce_result(
        1.2, 0.0001, cells, means, deviations, rows
    )
    module.compare_ce_result_exact(copy.deepcopy(expected), expected)

    one_bit = copy.deepcopy(expected)
    one_bit["floor_nu_fission_fractions"][1] = math.nextafter(
        one_bit["floor_nu_fission_fractions"][1], math.inf
    )
    expect_refusal(
        module,
        lambda: module.compare_ce_result_exact(one_bit, expected),
        "one-ULP CE JSON mismatch",
    )

    duplicate = copy.deepcopy(rows)
    duplicate[-1]["fuel_cell_id"] = duplicate[0]["fuel_cell_id"]
    expect_refusal(
        module,
        lambda: module.recompute_ce_result(
            1.2, 0.0001, cells, means, deviations, duplicate
        ),
        "duplicate cell/floor/pin map",
    )

    duplicate_position = copy.deepcopy(rows)
    duplicate_position[-1]["floor"] = duplicate_position[0]["floor"]
    duplicate_position[-1]["pin_index"] = duplicate_position[0]["pin_index"]
    expect_refusal(
        module,
        lambda: module.recompute_ce_result(
            1.2, 0.0001, cells, means, deviations, duplicate_position
        ),
        "duplicate floor/pin mapping",
    )


def test_fake_inputs(module, root: Path) -> None:
    build = root / "fake-build"
    map1 = root / "fake-map1"
    observables = root / "fake-observables"
    for directory in (build, map1, observables):
        directory.mkdir()
    for name in (
        "closed_axial.xsm",
        "initial_axial_track.xsm",
        "initial_axial_macrolib.xsm",
    ):
        (observables / name).write_text(f"synthetic {name}\n")
    (observables / "observables.x2m").write_text("synthetic deck\n")
    (observables / "observables.log").write_text(
        ">|D4A-CORRECTED-K-EFFECTIVE 1.2 |>0011\n"
        "SPORATE NU-FISSION-FRACTIONS 0.3 0.4 0.3\n"
        "normal end of execution for dragon\n"
    )
    expect_refusal(
        module,
        lambda: module.run_spot_acceptance(build, [map1], observables),
        "text-only SPOT XSM lineage",
    )

    fake_statepoint = root / "statepoint.100.h5"
    fake_statepoint.write_bytes(b"synthetic statepoint, not HDF5\n")
    expect_refusal(
        module,
        lambda: module.read_statepoint_result(fake_statepoint, pin_rows()),
        "text-only OpenMC statepoint",
    )


def test_spot_observables_receipt(module, root: Path) -> None:
    good = root / "good-spot-observables"
    make_spot_observables(module, good)
    k_effective, power = module.read_spot(good)
    if k_effective != 1.2 or power != [0.3, 0.4, 0.3]:
        raise RuntimeError("canonical SPOT observables were parsed incorrectly")

    wrong_trailer = root / "wrong-trailer-spot-observables"
    make_spot_observables(module, wrong_trailer, trailer="|>0012")
    expect_refusal(
        module,
        lambda: module.read_spot(wrong_trailer),
        "re-sealed SPOT k record with wrong ECHO trailer",
    )

    abnormal = root / "abnormal-spot-observables"
    make_spot_observables(module, abnormal, abnormal="SIGSEGV\n")
    expect_refusal(
        module,
        lambda: module.read_spot(abnormal),
        "re-sealed SPOT observables with abnormal signal",
    )


def test_runtime_provenance(module, root: Path) -> None:
    package = root / "openmc"
    (package / "model").mkdir(parents=True)
    for relative in module.OPENMC_PYTHON_CRITICAL_FILES:
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# synthetic OpenMC file {relative}\n")
    (package / "extra.py").write_text("VALUE = 1\n")
    fake_module = SimpleNamespace(
        __file__=str(package / "__init__.py"),
        __version__="9.8.7.dev6+gabcdef1",
    )

    executable = root / "openmc-original"
    version_text = "OpenMC version 9.8.7-dev6\nCommit hash: abcdef1\n"
    executable.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' 'OpenMC version 9.8.7-dev6' "
        "'Commit hash: abcdef1'\n"
    )
    executable.chmod(0o755)
    runtime = {
        "schema": "D4A_OPENMC_RUNTIME_PROVENANCE_V1",
        "executable": {
            "requested_identifier": str(executable),
            "resolved_path": str(executable.resolve()),
            "sha256": module.sha256(executable),
            "version_text": version_text,
            "version_text_sha256": hashlib.sha256(
                version_text.encode("utf-8")
            ).hexdigest(),
            "openmc_version": [9, 8, 7],
            "git_sha1": "abcdef1",
        },
        "python_package": {
            "version": fake_module.__version__,
            "root_identifier": str(package.resolve()),
            "critical_files": {
                relative: module.sha256(package / relative)
                for relative in module.OPENMC_PYTHON_CRITICAL_FILES
            },
            "stable_python_tree_sha256": module.sha256_python_tree(package),
            "stable_hash_rule": "sorted *.py: relative-posix NUL content NUL",
        },
    }
    module.validate_runtime_environment(runtime, None, fake_module)

    relocated_package = root / "relocated-package" / "openmc"
    shutil.copytree(package, relocated_package)
    relocated_module = SimpleNamespace(
        __file__=str(relocated_package / "__init__.py"),
        __version__=fake_module.__version__,
    )
    module.validate_runtime_environment(runtime, None, relocated_module)
    (relocated_package / "statepoint.py").write_text("# changed reader\n")
    expect_refusal(
        module,
        lambda: module.validate_runtime_environment(
            runtime, None, relocated_module
        ),
        "different-hash Python package relocation",
    )

    relocated = root / "openmc-relocated"
    shutil.copy2(executable, relocated)
    executable.unlink()
    expect_refusal(
        module,
        lambda: module.validate_runtime_environment(runtime, None, fake_module),
        "implicit executable relocation",
    )
    module.validate_runtime_environment(runtime, str(relocated), fake_module)
    relocated.write_text(relocated.read_text() + "# changed bytes\n")
    expect_refusal(
        module,
        lambda: module.validate_runtime_environment(
            runtime, str(relocated), fake_module
        ),
        "different-hash executable relocation",
    )


def test_statepoint_contract(module) -> None:
    class CellFilter:
        bins = [1]

    execution = {
        "mode": "RUN",
        "particles": 1000,
        "batches": 100,
        "inactive": 20,
        "seed": 17,
        "threads": 1,
    }
    runtime = {
        "executable": {
            "openmc_version": [9, 8, 7],
            "git_sha1": "abcdef1",
        }
    }

    def valid_state():
        return SimpleNamespace(
            version=(9, 8, 7),
            git_sha1="abcdef1",
            energy_mode="continuous-energy",
            n_particles=1000,
            n_batches=100,
            n_inactive=20,
            seed=17,
            current_batch=100,
            n_realizations=80,
            run_mode="eigenvalue",
        )

    def valid_tally():
        return SimpleNamespace(
            scores=["nu-fission"],
            estimator="tracklength",
            nuclides=["total"],
            filters=[CellFilter()],
        )

    module.validate_statepoint_contract(
        valid_state(), valid_tally(), execution, runtime
    )
    for attribute, bad_value in (
        ("version", (9, 8, 6)),
        ("git_sha1", "7654321"),
        ("git_sha1", None),
        ("energy_mode", "multi-group"),
        ("current_batch", 99),
        ("n_realizations", 79),
    ):
        state = valid_state()
        setattr(state, attribute, bad_value)
        expect_refusal(
            module,
            lambda state=state: module.validate_statepoint_contract(
                state, valid_tally(), execution, runtime
            ),
            f"statepoint {attribute} mismatch",
        )
    for attribute, bad_value in (
        ("estimator", "analog"),
        ("nuclides", ["U235"]),
    ):
        tally = valid_tally()
        setattr(tally, attribute, bad_value)
        expect_refusal(
            module,
            lambda tally=tally: module.validate_statepoint_contract(
                valid_state(), tally, execution, runtime
            ),
            f"statepoint tally {attribute} mismatch",
        )

    # Missing Git metadata is compatible only with the one audited runtime
    # and HDF5 format; it never suppresses other statepoint checks.
    class H5Handle(dict):
        def __init__(self):
            super().__init__()
            self.attrs = {"version": [18, 2]}

    known_runtime = {
        "schema": "D4A_OPENMC_RUNTIME_PROVENANCE_V1",
        "executable": copy.deepcopy(module.GITLESS_STATEPOINT_EXECUTABLE),
        "python_package": {
            "stable_python_tree_sha256": module.GITLESS_STATEPOINT_PYTHON_TREE,
        },
    }

    def known_state():
        state = valid_state()
        state.version = (0, 15, 4)
        state.git_sha1 = None
        state._f = H5Handle()
        return state

    module.validate_statepoint_contract(
        known_state(), valid_tally(), execution, known_runtime
    )
    present_sha = known_state()
    present_sha.git_sha1 = known_runtime["executable"]["git_sha1"]
    module.validate_statepoint_contract(
        present_sha, valid_tally(), execution, known_runtime
    )
    for field, bad_value in (
        ("sha256", "0" * 64),
        ("git_sha1", "0" * 40),
        ("version_text_sha256", "0" * 64),
    ):
        bad_runtime = copy.deepcopy(known_runtime)
        bad_runtime["executable"][field] = bad_value
        expect_refusal(module, lambda: module.validate_statepoint_contract(
            known_state(), valid_tally(), execution, bad_runtime
        ), f"missing Git with unknown runtime {field}")
    bad_runtime = copy.deepcopy(known_runtime)
    bad_runtime["python_package"]["stable_python_tree_sha256"] = "0" * 64
    expect_refusal(module, lambda: module.validate_statepoint_contract(
        known_state(), valid_tally(), execution, bad_runtime
    ), "missing Git with unknown Python reader")
    for attribute, bad_value in (
        ("git_sha1", "0" * 40),
        ("version", (0, 15, 3)),
        ("current_batch", 99),
        ("n_realizations", 79),
        ("energy_mode", "multi-group"),
    ):
        state = known_state()
        setattr(state, attribute, bad_value)
        expect_refusal(module, lambda: module.validate_statepoint_contract(
            state, valid_tally(), execution, known_runtime
        ), f"audited build with wrong {attribute}")
    for metadata in ([], [18, 1], [19, 2]):
        state = known_state()
        state._f.attrs["version"] = metadata
        expect_refusal(module, lambda: module.validate_statepoint_contract(
            state, valid_tally(), execution, known_runtime
        ), "missing Git with unknown HDF5 format")
    for value in ("0" * 40, ""):
        state = known_state()
        state._f.attrs["git_sha1"] = value
        expect_refusal(module, lambda: module.validate_statepoint_contract(
            state, valid_tally(), execution, known_runtime
        ), "API None masking explicit HDF5 Git metadata")


def main() -> None:
    module = load_checker()
    test_exact_reconstruction(module)
    with tempfile.TemporaryDirectory(prefix="d4a_receipt_checker_") as temp:
        root = Path(temp)
        test_fake_inputs(module, root)
        test_spot_observables_receipt(module, root)
        test_runtime_provenance(module, root)
    test_statepoint_contract(module)
    print(
        "D4A SPOT-CE SYNTHETIC PASS: exact 651-bin reconstruction accepted; "
        "one-ULP JSON mismatch, provenance relocation/hash mismatch, "
        "statepoint metadata mismatch, unknown gitless build/format, "
        "duplicate mapping, text XSM lineage, "
        "wrong SPOT ECHO trailer, abnormal signal, and text statepoint refused"
    )


if __name__ == "__main__":
    main()

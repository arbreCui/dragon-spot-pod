#!/usr/bin/env python3
"""Synthetic positive and fail-closed tests for the D4-A result exporter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_d4a_corrected_result.py"
CANONICAL_DECK = HERE / "d4a_corrected_final_observables.x2m"
MAP_INPUTS = (
    "parent_axial_closed.xsm",
    "parent_snapshots_closed.xsm",
    "initial_radial_track.bin",
    "initial_axial_track.xsm",
    "initial_axial_macrolib.xsm",
    "basis_reference.xsm",
    "route_contract.xsm",
    "projected_proposal.xsm",
)
MAP_OUTPUTS = (
    "candidate_system.xsm",
    "candidate_radial.xsm",
    "candidate_axial.xsm",
    "candidate_snapshots.xsm",
    "closed_axial.xsm",
    "closed_snapshots.xsm",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(directory: Path, name: str, files: tuple[str, ...]) -> None:
    (directory / name).write_text(
        "".join(f"{sha256(directory / file)}  {file}\n" for file in files),
        encoding="utf-8",
    )


def seal_map(directory: Path) -> None:
    files = sorted(path for path in directory.iterdir() if path.name != "result.sha256")
    (directory / "result.sha256").write_text(
        "".join(f"{sha256(path)}  ./{path.name}\n" for path in files),
        encoding="utf-8",
    )


def inventory(directory: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        (path.relative_to(directory).as_posix(), sha256(path))
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    )


def make_map(directory: Path, *, valid: bool = True) -> None:
    directory.mkdir()
    for name in MAP_INPUTS + MAP_OUTPUTS:
        (directory / name).write_text(f"{name}\n", encoding="utf-8")
    write_manifest(directory, "input_manifest.sha256", MAP_INPUTS)
    write_manifest(directory, "output_manifest.sha256", MAP_OUTPUTS)
    (directory / "prepare.log").write_text(
        "SPOT-R64 B2J CLOSED/3 -> PROJECTED/4\n"
        "SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT\n",
        encoding="utf-8",
    )
    (directory / "admission.log").write_text(
        "H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=3\n",
        encoding="utf-8",
    )
    (directory / "close.log").write_text(
        "SPOT-R64 B2W CLOSE PASS STATUS=2\n"
        "SPOT-R64 CLOSED/4 COMPLETE NO-TRANSPORT\n",
        encoding="utf-8",
    )
    (directory / "independent_check.log").write_text(
        "ONE-MAP-XSM POD-PACKAGE BITWISE PASS\nONE-MAP-XSM COMPLETE\n",
        encoding="utf-8",
    )
    if valid:
        classification = "VALID_MET"
        status = "PASS"
        role = "CONVERGED_MAP"
    else:
        classification = "VALID_NOT_MET"
        status = "NOT MET"
        role = "NEXT_MAP_PARENT_ONLY"
    (directory / "gate.log").write_text(
        "SPOT-GATE THRESHOLD        4.9999999999999998E-07\n"
        f"SPOT-GATE RRHO             1.0000000000000000E-08 {status}\n"
        f"SPOT-GATE RLEAK            2.0000000000000000E-08 {status}\n"
        f"SPOT-GATE RA               3.0000000000000000E-08 {status}\n"
        f"CLASSIFICATION={classification}\nSPOT-GATE COMPLETE\n",
        encoding="utf-8",
    )
    role_lines = [
        f"MAP_CLASSIFICATION={classification}",
        f"PORTABLE_ROLE={role}",
    ]
    if not valid:
        role_lines.append("FINAL_CONVERGENCE=NOT_CLAIMED")
    (directory / "portable_classification.txt").write_text(
        "\n".join(role_lines) + "\n", encoding="utf-8"
    )
    seal_map(directory)


def make_observables(directory: Path, map_directory: Path) -> None:
    directory.mkdir()
    for name in (
        "closed_axial.xsm",
        "initial_axial_track.xsm",
        "initial_axial_macrolib.xsm",
    ):
        (directory / name).write_bytes((map_directory / name).read_bytes())
    (directory / "observables.x2m").write_bytes(CANONICAL_DECK.read_bytes())
    (directory / "observables.log").write_text(
        ">|D4A-CORRECTED-K-EFFECTIVE   1.234567890123456E+00   |>0011\n"
        "SPORATE NU-FISSION-FRACTIONS   2.00000000E-01  3.00000000E-01  5.00000000E-01\n"
        " normal end of execution for dragon 5  Version 5.1.0\n",
        encoding="utf-8",
    )
    write_manifest(
        directory,
        "observables.sha256",
        (
            "closed_axial.xsm",
            "initial_axial_track.xsm",
            "initial_axial_macrolib.xsm",
            "observables.x2m",
            "observables.log",
        ),
    )


class ExportResultTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="d4a-result-export-test.")
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_export(self, map_dir: Path, obs_dir: Path, output: Path):
        return subprocess.run(
            [sys.executable, str(EXPORTER), str(map_dir), str(obs_dir), str(output)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_sealed_result_is_exported(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        output = self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads((output / "result.json").read_text())
        self.assertEqual(result["map_epoch"], 4)
        self.assertEqual(result["classification"], "VALID_MET")
        self.assertEqual(result["Rrho"], 1.0e-8)
        self.assertEqual(result["k_effective"], 1.234567890123456)
        self.assertEqual(
            (output / "power.csv").read_text(),
            "floor,normalized_nu_fission_fraction\n"
            "bottom,2.00000000E-01\n"
            "middle,3.00000000E-01\n"
            "top,5.00000000E-01\n",
        )
        receipt = (output / "export_result.sha256").read_text().splitlines()
        self.assertEqual(
            receipt,
            [
                f"{sha256(output / 'result.json')}  result.json",
                f"{sha256(output / 'power.csv')}  power.csv",
            ],
        )
        self.assertEqual(
            {path.name for path in output.iterdir()},
            {"result.json", "power.csv", "export_result.sha256"},
        )

    def test_valid_not_met_map_is_refused_without_output(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        output = self.root / "output"
        make_map(map_dir, valid=False)
        make_observables(obs_dir, map_dir)
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())

    def test_resealed_pass_label_cannot_hide_a_large_residual(self) -> None:
        map_dir, obs_dir, output = self.root / "map", self.root / "observables", self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        gate = map_dir / "gate.log"
        gate.write_text(gate.read_text().replace("1.0000000000000000E-08 PASS", "1.0000000000000000E-03 PASS"))
        seal_map(map_dir)
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exceeds the declared gate", completed.stderr)
        self.assertFalse(output.exists())

    def test_resealed_relaxed_threshold_is_refused(self) -> None:
        map_dir, obs_dir, output = self.root / "map", self.root / "observables", self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        gate = map_dir / "gate.log"
        gate.write_text(gate.read_text().replace("4.9999999999999998E-07", "1.0000000000000000E-03"))
        seal_map(map_dir)
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("does not use the declared 5e-7 gate", completed.stderr)
        self.assertFalse(output.exists())

    def test_tampered_observables_are_refused_without_output(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        output = self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        with (obs_dir / "observables.log").open("a", encoding="utf-8") as stream:
            stream.write(">|D4A-CORRECTED-K-EFFECTIVE 9.0\n")
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())

    def test_wrong_echo_trailer_is_refused_even_when_resealed(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        output = self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        log = obs_dir / "observables.log"
        log.write_text(log.read_text().replace("|>0011", "|>0012"))
        write_manifest(
            obs_dir,
            "observables.sha256",
            (
                "closed_axial.xsm",
                "initial_axial_track.xsm",
                "initial_axial_macrolib.xsm",
                "observables.x2m",
                "observables.log",
            ),
        )
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())

    def test_duplicate_k_record_is_refused_even_when_resealed(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        output = self.root / "output"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        with (obs_dir / "observables.log").open("a", encoding="utf-8") as stream:
            stream.write(
                ">|D4A-CORRECTED-K-EFFECTIVE 1.234567890123456E+00 |>0011\n"
            )
        write_manifest(
            obs_dir,
            "observables.sha256",
            (
                "closed_axial.xsm",
                "initial_axial_track.xsm",
                "initial_axial_macrolib.xsm",
                "observables.x2m",
                "observables.log",
            ),
        )
        completed = self.run_export(map_dir, obs_dir, output)
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(output.exists())

    def test_output_inside_either_input_is_refused_without_pollution(self) -> None:
        map_dir = self.root / "map"
        obs_dir = self.root / "observables"
        make_map(map_dir)
        make_observables(obs_dir, map_dir)
        for input_directory in (map_dir, obs_dir):
            with self.subTest(input_directory=input_directory.name):
                output = input_directory / "published-result"
                map_before = inventory(map_dir)
                obs_before = inventory(obs_dir)
                completed = self.run_export(map_dir, obs_dir, output)
                self.assertNotEqual(completed.returncode, 0)
                self.assertFalse(output.exists())
                self.assertEqual(inventory(map_dir), map_before)
                self.assertEqual(inventory(obs_dir), obs_before)


if __name__ == "__main__":
    unittest.main()

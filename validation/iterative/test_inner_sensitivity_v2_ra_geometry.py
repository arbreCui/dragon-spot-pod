#!/usr/bin/env python3
"""Short, no-Dragon tests for the Stage-4 v2 R_a geometry diagnostic."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import run_inner_sensitivity_v2_ra_geometry as runner


class RAGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        command = [sys.executable, "-B", str(Path(runner.__file__))]
        cls.first = subprocess.run(
            command,
            cwd=runner.ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        cls.second = subprocess.run(
            command,
            cwd=runner.ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_frozen_inputs_and_dependencies(self) -> None:
        runner.verify_frozen_inputs()
        inodes = []
        for _name, path, expected in runner.INPUTS:
            self.assertEqual(runner.sha256(path), expected)
            status = path.stat()
            inodes.append((status.st_dev, status.st_ino))
        self.assertEqual(len(set(inodes)), 3)
        with self.assertRaises(runner.GeometryError):
            runner.verify_hash(
                runner.INPUTS[0][1],
                runner.INPUTS[2][2],
                "role-swapped-x0",
            )
        with tempfile.TemporaryDirectory() as raw:
            tampered = Path(raw) / "tampered.xsm"
            tampered.write_bytes(b"\x00")
            with self.assertRaises(runner.GeometryError):
                runner.verify_hash(
                    tampered,
                    runner.INPUTS[0][2],
                    "one-byte-tamper",
                )

    def test_source_is_read_only_ganlib(self) -> None:
        source = runner.SOURCE.read_bytes()
        self.assertIn(b"use GANLIB", source)
        self.assertIsNone(runner.FORBIDDEN_MUTATION.search(source))
        self.assertIsNone(runner.FORBIDDEN_SOURCE_SOLVER.search(source))
        self.assertIn(b"negative_zero(orth_norm2)", source)
        self.assertIn(
            b"btest(real64_bits(value),bit_size(0_int64)-1)",
            source,
        )

    def test_two_builds_are_deterministic(self) -> None:
        for completed in (self.first, self.second):
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(completed.stderr, b"")
        self.assertEqual(self.first.stdout, self.second.stdout)

    def test_output_census_and_exact_bits(self) -> None:
        text = self.first.stdout.decode("ascii")
        lines = text.splitlines()
        self.assertEqual(len(lines), 404)
        prefix = "INNER-SENSITIVITY-V2 RA-GEOMETRY "
        self.assertTrue(all(line.startswith(prefix) for line in lines))
        planes = [
            line
            for line in lines
            if re.match(r".* RA-GEOMETRY PLANE [1-3] ", line)
        ]
        groups = [
            line
            for line in lines
            if re.match(r".* RA-GEOMETRY GROUP [0-9]+ ", line)
        ]
        self.assertEqual(len(planes), 3)
        self.assertEqual(len(groups), 370)
        self.assertEqual(
            [
                int(re.match(r".* RA-GEOMETRY GROUP ([0-9]+) ", line).group(1))
                for line in groups
            ],
            list(range(1, 371)),
        )
        self.assertIn(
            "RA-BITS ROUT-2H 0x3EF7A721405AFAAF "
            "RIN 0x3EF7FB7522398B1F ROUT-H 0x3EAEF702EB99D736",
            text,
        )
        self.assertIn(
            "PLANE-DELTA2-SIGNS NEG 2 ZERO 0 POS 1 TOTAL 3",
            text,
        )
        self.assertIn(
            "GROUP-DELTA2-SIGNS NEG 42 ZERO 0 POS 328 TOTAL 370",
            text,
        )
        self.assertIn(
            "GROUP-DELTA2-MAXABS GROUP 80 "
            "BITS 0x3D5AA96EBA84B12A",
            text,
        )
        self.assertNotRegex(text, r"\b(?:NaN|Inf)\b")
        self.assertEqual(
            lines[-2:],
            [
                "INNER-SENSITIVITY-V2 RA-GEOMETRY RUNNER PASS: BUILDS=2",
                "INNER-SENSITIVITY-V2 RA-GEOMETRY DRAGON-RUNS=0",
            ],
        )

    def test_output_tamper_is_rejected(self) -> None:
        lines = self.first.stdout.splitlines(keepends=True)
        raw = b"".join(lines[:-2])
        runner.validate_output(raw)
        variants = [
            b"".join(raw.splitlines(keepends=True)[:-1]),
            raw + raw.splitlines(keepends=True)[30],
            b"".join(
                raw.splitlines(keepends=True)[:30]
                + raw.splitlines(keepends=True)[31:32]
                + raw.splitlines(keepends=True)[30:31]
                + raw.splitlines(keepends=True)[32:]
            ),
            raw.replace(b"0x3DAF61EA2CD57B76", b"0x3DAF61EA2CD57B77", 1),
            raw + b"INNER-SENSITIVITY-V2 RA-GEOMETRY EXTRA\n",
        ]
        for variant in variants:
            with self.subTest(length=len(variant)):
                with self.assertRaises(runner.GeometryError):
                    runner.validate_output(variant)

    def test_manufactured_cell_first_marginals(self) -> None:
        heights = (Fraction(1), Fraction(2))
        gram = (Fraction(1, 2), Fraction(2))
        u = ((Fraction(1), Fraction(2)), (Fraction(3), Fraction(1)))
        e = ((Fraction(-1), Fraction(1)), (Fraction(1), Fraction(-2)))
        qh2 = Fraction(16)
        q2h2 = Fraction(8)
        plane = [Fraction(0), Fraction(0)]
        group = [Fraction(0), Fraction(0)]
        canonical = Fraction(0)
        for group_index in range(2):
            for plane_index in range(2):
                delta = (
                    heights[plane_index]
                    * gram[group_index]
                    * e[group_index][plane_index] ** 2
                    / qh2
                    - heights[plane_index]
                    * gram[group_index]
                    * u[group_index][plane_index] ** 2
                    / q2h2
                )
                canonical += delta
                plane[plane_index] += delta
                group[group_index] += delta
        self.assertEqual(sum(plane, Fraction(0)), canonical)
        self.assertEqual(sum(group, Fraction(0)), canonical)
        self.assertTrue(any(value < 0 for value in plane + group))
        self.assertTrue(any(value > 0 for value in plane + group))

    def test_result_bits_are_the_frozen_unresolved_pair(self) -> None:
        result_path = (
            runner.ITERATIVE
            / "inner_sensitivity_v2_result"
            / "result.json"
        )
        result = json.loads(result_path.read_text(encoding="ascii"))
        component = next(
            item for item in result["components"] if item["name"] == "R_a"
        )
        self.assertEqual(component["status"], "UNRESOLVED")
        self.assertEqual(component["relation"], "GREATER")
        self.assertEqual(
            component["d_out_2h_f64_bits"],
            "0x3ef7a721405afaaf",
        )
        self.assertEqual(component["d_in_f64_bits"], "0x3ef7fb7522398b1f")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""No-Dragon tests for the exact Stage-4 v2 result classifier."""

from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest

import check_inner_sensitivity_v2_result as result


def bits_row(label: str, values: tuple[int, ...]) -> str:
    return label + " " + " ".join(f"0x{value:016X}" for value in values)


def relation(left: int, right: int) -> str:
    if left < right:
        return "LESS"
    if left > right:
        return "GREATER"
    return "EQUAL"


def pair_log(
    coarse: tuple[int, ...],
    inner: tuple[int, ...],
    *,
    components: tuple[str, ...] = result.CHECKER_COMPONENTS,
) -> str:
    lines = [
        "INNER-SENSITIVITY-V2 X0 CANONICAL BITWISE IDENTICAL",
        "INNER-SENSITIVITY-V2 TRIAL-SPACE BITWISE IDENTICAL",
        "INNER-SENSITIVITY-V2 RADIAL-INPUTS BITWISE IDENTICAL",
        "INNER-SENSITIVITY-V2 ORDER RRHO RLEAK DLEAK RA",
        bits_row(
            "INNER-SENSITIVITY-V2 DOUT-H-BITS",
            result.FROZEN_FINE_BITS,
        ),
        bits_row("INNER-SENSITIVITY-V2 DOUT-2H-BITS", coarse),
        bits_row("INNER-SENSITIVITY-V2 DIN-BITS", inner),
    ]
    lines.extend(
        "INNER-SENSITIVITY-V2 COMPONENT "
        f"{name} DIN-VS-DOUT-2H {relation(inner[index], coarse[index])}"
        for index, name in enumerate(components)
    )
    lines.append("INNER-SENSITIVITY-V2 COMPLETE")
    return "\n".join(lines) + "\n"


class ResultClassifierTest(unittest.TestCase):
    def parse(
        self,
        text: str,
    ) -> tuple[tuple[int, ...], ...]:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "pair.log"
            path.write_text(text, encoding="ascii")
            return result.parse_pair_log(path)

    def assert_rejected(self, text: str, message: str) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                self.parse(text)
        self.assertIn(message, stderr.getvalue())

    def test_positive_and_zero_component_rules(self) -> None:
        coarse = (
            0x3FF0000000000000,
            0x4000000000000000,
            0,
            0x4010000000000000,
        )
        inner = (
            0x3FE0000000000000,
            0x3FF0000000000000,
            0,
            0x4000000000000000,
        )
        dout_h, dout_2h, din = self.parse(pair_log(coarse, inner))
        rows, resolved = result.component_rows(dout_h, dout_2h, din)
        self.assertTrue(resolved)
        self.assertEqual(
            [row["coarse_outer_case"] for row in rows],
            ["POSITIVE", "POSITIVE", "ZERO", "POSITIVE"],
        )
        self.assertTrue(all(row["status"] == "RESOLVED" for row in rows))

    def test_equal_and_greater_are_unresolved(self) -> None:
        coarse = (
            0x3FF0000000000000,
            0x3FF0000000000000,
            0,
            0,
        )
        inner = (
            0x3FF0000000000000,
            0x4000000000000000,
            0,
            0x0010000000000000,
        )
        rows, resolved = result.component_rows(
            result.FROZEN_FINE_BITS,
            coarse,
            inner,
        )
        self.assertFalse(resolved)
        self.assertEqual(
            [row["status"] for row in rows],
            ["UNRESOLVED", "UNRESOLVED", "RESOLVED", "UNRESOLVED"],
        )

    def test_rule_uses_coarse_outer_not_fine_outer(self) -> None:
        coarse = list(result.FROZEN_FINE_BITS)
        inner = list(result.FROZEN_FINE_BITS)
        coarse[0] = 0x3FF0000000000000
        inner[0] = 0x3FE0000000000000
        rows, _ = result.component_rows(
            result.FROZEN_FINE_BITS,
            tuple(coarse),
            tuple(inner),
        )
        self.assertEqual(rows[0]["status"], "RESOLVED")

        coarse[0] = 0x3FD0000000000000
        rows, _ = result.component_rows(
            result.FROZEN_FINE_BITS,
            tuple(coarse),
            tuple(inner),
        )
        self.assertEqual(rows[0]["status"], "UNRESOLVED")

    def test_negative_zero_and_nonfinite_are_rejected(self) -> None:
        coarse = (
            0x8000000000000000,
            0x7FF0000000000000,
            0,
            0x3FF0000000000000,
        )
        inner = (0, 0, 0, 0)
        self.assert_rejected(pair_log(coarse, inner), "negative zero")

        coarse = (
            0x3FF0000000000000,
            0x7FF8000000000001,
            0,
            0x3FF0000000000000,
        )
        self.assert_rejected(pair_log(coarse, inner), "NaN or infinity")

    def test_both_infinities_are_rejected_and_positive_zero_is_accepted(
        self,
    ) -> None:
        inner = (0, 0, 0, 0)
        for infinity, message in (
            (0x7FF0000000000000, "NaN or infinity"),
            (0xFFF0000000000000, "negative value"),
        ):
            coarse = (
                0x3FF0000000000000,
                infinity,
                0,
                0x3FF0000000000000,
            )
            self.assert_rejected(pair_log(coarse, inner), message)
        parsed = self.parse(
            pair_log(
                (0, 0x3FF0000000000000, 0, 0x3FF0000000000000),
                inner,
            )
        )
        self.assertEqual(parsed[1][0], 0)

    def test_extra_fifth_component_is_rejected(self) -> None:
        coarse = (0x3FF0000000000000,) * 4
        inner = (0,) * 4
        text = pair_log(coarse, inner).replace(
            "INNER-SENSITIVITY-V2 COMPLETE\n",
            "INNER-SENSITIVITY-V2 COMPONENT EXTRA "
            "DIN-VS-DOUT-2H LESS\n"
            "INNER-SENSITIVITY-V2 COMPLETE\n",
        )
        self.assert_rejected(text, "must have 12 rows")

    def test_reordered_component_is_rejected(self) -> None:
        coarse = (0x3FF0000000000000,) * 4
        inner = (0,) * 4
        components = ("RLEAK", "RRHO", "DLEAK", "RA")
        self.assert_rejected(
            pair_log(coarse, inner, components=components),
            "RRHO relation differs",
        )

    def test_fine_lane_bits_are_frozen(self) -> None:
        coarse = (0x3FF0000000000000,) * 4
        inner = (0,) * 4
        text = pair_log(coarse, inner).replace(
            "0x3EB57E84A0A80000",
            "0x3EB57E84A0A80001",
        )
        self.assert_rejected(text, "fine D_out bits differ")


class ManifestTest(unittest.TestCase):
    def valid_manifest(self) -> bytes:
        rows = []
        for name in result.SCIENTIFIC_FILES:
            digest = result.FROZEN_INPUT_HASHES.get(name, "1" * 64)
            rows.append(f"{digest}  {name}")
        return ("\n".join(rows) + "\n").encode("ascii")

    def test_manifest_census_and_order(self) -> None:
        parsed = result.parse_manifest_bytes(
            self.valid_manifest(),
            "fixture",
        )
        self.assertEqual(tuple(parsed), result.SCIENTIFIC_FILES)

    def test_manifest_extra_and_path_escape_are_rejected(self) -> None:
        extra = self.valid_manifest() + b"2" * 64 + b"  extra.xsm\n"
        with self.assertRaises(SystemExit):
            result.parse_manifest_bytes(extra, "fixture")
        escaped = self.valid_manifest().replace(
            b"state1_system.xsm",
            b"../state1_system.xsm",
        )
        with self.assertRaises(SystemExit):
            result.parse_manifest_bytes(escaped, "fixture")

    def test_manifest_frozen_input_hash_is_rejected(self) -> None:
        tampered = self.valid_manifest().replace(
            next(iter(result.FROZEN_INPUT_HASHES.values())).encode("ascii"),
            b"0" * 64,
        )
        with self.assertRaises(SystemExit):
            result.parse_manifest_bytes(tampered, "fixture")

    def test_capture_and_replay_hardlinks_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            capture = root / "capture"
            replay = root / "replay"
            capture.mkdir()
            replay.mkdir()
            for name in result.SCIENTIFIC_FILES:
                source = capture / name
                source.write_bytes(name.encode("ascii"))
                os.link(source, replay / name)
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    result.verify_inode_separation(capture, replay)


if __name__ == "__main__":
    unittest.main()

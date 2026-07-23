#!/usr/bin/env python3
"""Tests for the threshold-free Stage-4 status state machine."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "validation/iterative/check_inner_sensitivity_status.py"
PROTOCOL = ROOT / "validation/iterative/inner_sensitivity_protocol.json"
COMPONENTS = ("RRHO", "RLEAK", "DLEAK", "RA")


def relation(left: float, right: float) -> str:
    if left < right:
        return "LESS"
    if left > right:
        return "GREATER"
    return "EQUAL"


def fixture(
    dout_h: tuple[float, ...],
    dout_h2: tuple[float, ...],
    din: tuple[float, ...],
) -> str:
    rows = [
        "INNER-SENSITIVITY X0 CANONICAL BITWISE IDENTICAL",
        "INNER-SENSITIVITY TRIAL-SPACE BITWISE IDENTICAL",
        "INNER-SENSITIVITY RADIAL-INPUTS BITWISE IDENTICAL",
        "INNER-SENSITIVITY ORDER RRHO RLEAK DLEAK RA",
        "INNER-SENSITIVITY DOUT-H " + " ".join(map(str, dout_h)),
        "INNER-SENSITIVITY DOUT-H2 " + " ".join(map(str, dout_h2)),
        "INNER-SENSITIVITY DIN " + " ".join(map(str, din)),
    ]
    for index, component in enumerate(COMPONENTS):
        rows.append(
            f"INNER-SENSITIVITY COMPONENT {component} "
            f"DIN-VS-DOUT-H {relation(din[index], dout_h[index])} "
            f"DIN-VS-DOUT-H2 {relation(din[index], dout_h2[index])}"
        )
    rows.append("INNER-SENSITIVITY COMPLETE")
    return "\n".join(rows) + "\n"


class StatusTests(unittest.TestCase):
    def run_checker(self, content: str, replay: bool = False) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "pair.log"
            log.write_text(content, encoding="utf-8")
            command = [sys.executable, str(CHECKER), str(log), str(PROTOCOL)]
            if replay:
                command.append("--replay")
            return subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_resolved_capture_remains_pending(self) -> None:
        result = self.run_checker(
            fixture((1.0, 2.0, 3.0, 4.0), (1.1, 2.1, 3.1, 4.1),
                    (0.5, 1.0, 2.0, 3.0))
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS STAGE4 PENDING-REPLAY", result.stdout)
        self.assertIn("STATUS STAGE5 NOT-AUTHORIZED", result.stdout)

    def test_resolved_fresh_replay_authorizes_stage5(self) -> None:
        result = self.run_checker(
            fixture((1.0, 2.0, 3.0, 4.0), (1.1, 2.1, 3.1, 4.1),
                    (0.5, 1.0, 2.0, 3.0)),
            replay=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS STAGE4 QUALIFIED", result.stdout)
        self.assertIn("STATUS STAGE5 AUTHORIZED", result.stdout)

    def test_unresolved_component_is_absorbing(self) -> None:
        result = self.run_checker(
            fixture((1.0, 2.0, 3.0, 4.0), (1.1, 2.1, 3.1, 4.1),
                    (1.0, 1.0, 2.0, 3.0)),
            replay=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("COMPONENT RRHO UNRESOLVED", result.stdout)
        self.assertIn("STATUS STAGE4 UNRESOLVED", result.stdout)
        self.assertIn("STATUS STAGE5 NOT-AUTHORIZED", result.stdout)

    def test_zero_outer_zero_inner_is_resolved(self) -> None:
        result = self.run_checker(
            fixture((0.0, 2.0, 3.0, 4.0), (0.0, 2.1, 3.1, 4.1),
                    (0.0, 1.0, 2.0, 3.0))
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("COMPONENT RRHO RESOLVED", result.stdout)

    def test_tampered_relation_is_rejected(self) -> None:
        content = fixture(
            (1.0, 2.0, 3.0, 4.0),
            (1.1, 2.1, 3.1, 4.1),
            (0.5, 1.0, 2.0, 3.0),
        ).replace("DIN-VS-DOUT-H LESS", "DIN-VS-DOUT-H GREATER", 1)
        result = self.run_checker(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("relation row differs", result.stderr)


if __name__ == "__main__":
    unittest.main()

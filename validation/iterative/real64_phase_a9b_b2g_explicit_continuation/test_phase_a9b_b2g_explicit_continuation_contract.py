#!/usr/bin/env python3
"""Mutation checks for the independent B2g static gate."""

from __future__ import annotations

import unittest
from pathlib import Path

from check_phase_a9b_b2g_explicit_continuation import (
    GateError,
    check_b2b_text,
    check_host_text,
    check_validation_text,
)


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


class ExplicitContinuationContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2b = (ROOT / "src/SPOR64_B2B.f90").read_text()
        cls.flu = (ROOT / "src/FLU.f").read_text()
        cls.flugpi = (ROOT / "src/FLUGPI.f").read_text()
        cls.plane = (ROOT / "data/SpotPlaneR64.c2m").read_text()
        cls.harness = (HERE / "test_b2g_explicit_continuation.f90").read_text()
        cls.stub = (HERE / "b2g_capture_stubs.f90").read_text()
        cls.parser = (HERE / "b2g_parser_driver.f90").read_text()
        cls.runner = (HERE / "run_phase_a9b_b2g_explicit_continuation.sh").read_text()

    def mutate_once(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation anchor count: {old}")
        return text.replace(old, new, 1)

    def test_current_contract(self) -> None:
        check_b2b_text(self.b2b)
        check_host_text(self.flu, self.flugpi, self.plane)
        check_validation_text(self.harness, self.stub, self.parser, self.runner)

    def test_boot_token_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2b, "SPOR64_B2B_BOOT = 1", "SPOR64_B2B_BOOT = 9"
        )
        with self.assertRaises(GateError):
            check_b2b_text(bad)

    def test_mode_guard_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2b,
            "r64_mode /= SPOR64_B2B_CONT",
            "r64_mode == SPOR64_B2B_CONT",
        )
        with self.assertRaises(GateError):
            check_b2b_text(bad)

    def test_qfiss_name_mutation_rejected(self) -> None:
        old = "RECORD_MATCHES(source_authority,'QFISS',NGRP,10)"
        bad = self.mutate_once(self.b2b, old, old.replace("QFISS", "SOUR"))
        with self.assertRaises(GateError):
            check_b2b_text(bad)

    def test_cont_type4_mutation_rejected(self) -> None:
        old = "if (ilong /= NUNKNO .or. itylcm /= 4) return"
        self.assertEqual(self.b2b.count(old), 2)
        bad = self.b2b.replace(old, old.replace("/= 4", "/= 2"), 1)
        with self.assertRaises(GateError):
            check_b2b_text(bad)

    def test_cont_root_fallback_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2b,
            "jpflux = LCMGID(seed_authority,'FLUX')",
            "jpflux = LCMGID(ipseed,'FLUX')",
        )
        with self.assertRaises(GateError):
            check_b2b_text(bad)

    def test_parser_cont_assignment_mutation_rejected(self) -> None:
        bad = self.mutate_once(self.flugpi, "IR64MD=2", "IR64MD=1")
        with self.assertRaises(GateError):
            check_host_text(self.flu, bad, self.plane)

    def test_parser_reset_mutation_rejected(self) -> None:
        bad = self.mutate_once(self.flugpi, "IR64MD=0", "IR64MD=2")
        with self.assertRaises(GateError):
            check_host_text(self.flu, bad, self.plane)

    def test_flu_mode_forwarding_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.flu,
            "LFORW,IR64MD,IB2STAT,CUTOFF64)",
            "LFORW,1,IB2STAT,CUTOFF64)",
        )
        with self.assertRaises(GateError):
            check_host_text(bad, self.flugpi, self.plane)

    def test_bare_procedure_mode_rejected(self) -> None:
        bad = self.mutate_once(self.plane, "R64 BOOT ;", "R64 ;")
        with self.assertRaises(GateError):
            check_host_text(self.flu, self.flugpi, bad)

    def test_roundtrip_witness_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.harness,
            "roundtrip_flux64(:,ig)=real(real(stage64,real32),real64)",
            "roundtrip_flux64(:,ig)=stage64",
        )
        with self.assertRaises(GateError):
            check_validation_text(bad, self.stub, self.parser, self.runner)

    def test_terminal_source_alias_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.stub,
            "terminal_source64(iu,ig)=real(1000*ig+iu,real64)/8.0_real64",
            "terminal_source64(iu,ig)=fixed_source64(iu,ig)",
        )
        with self.assertRaises(GateError):
            check_validation_text(self.harness, bad, self.parser, self.runner)


if __name__ == "__main__":
    unittest.main()

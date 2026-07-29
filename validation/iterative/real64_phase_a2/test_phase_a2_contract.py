#!/usr/bin/env python3
"""Semantic mutation tests for the REAL64 Phase-A2 manifest."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a2 import (
    PhaseA2Error,
    ROOT,
    validate,
    validate_makefile_contract,
)


MANIFEST = (
    ROOT / "validation/iterative/real64_phase_a2/precision_manifest.json"
)


class PhaseA2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA2Error):
            validate(candidate, verify_canonical=False)

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA2Error):
            validate(candidate)

    def test_full_closure_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "phase_a_static_closure", True
            )
        )

    def test_actual_moc_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "actual_moc_response_implemented", True
            )
        )

    def test_production_connection_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "production_route_connected", True
            )
        )

    def test_dragon_cannot_be_authorized(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "dragon_processes_authorized", 1
            )
        )

    def test_empty_active_set_cannot_be_allowed(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__(
                "active_subset", "ARBITRARY-INCLUDING-EMPTY"
            )
        )

    def test_raw_response_point_cannot_move(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__(
                "raw_response_point", "PRE-MCGFST"
            )
        )

    def test_downcast_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["kind_contract"][
                "phase_a2_binary64_to_binary32_conversions"
            ].append("real(source,real32)")
        )

    def test_callback_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["matrix_contract"].__setitem__(
                "callback_count", "ONE-PER-ACTIVE-GROUP"
            )
        )

    def test_inactive_raw_rule_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["matrix_contract"].__setitem__(
                "inactive_raw_acceptance", "IGNORE"
            )
        )

    def test_synthetic_callback_cannot_be_physical(self) -> None:
        self.rejected(
            lambda data: data["response_semantics"].__setitem__(
                "synthetic_callback_is_physical_moc", True
            )
        )

    def test_aca_cannot_enter_boundary(self) -> None:
        self.rejected(
            lambda data: data["response_semantics"][
                "excluded_after_boundary"
            ].remove("MCGFCA")
        )

    def test_default_all_cannot_include_slice(self) -> None:
        self.rejected(
            lambda data: data["build_contract"].__setitem__(
                "added_to_default_all", True
            )
        )

    def test_make_target_cannot_gain_prerequisite(self) -> None:
        makefile = (ROOT / "Makefile").read_text().replace(
            "spot-real64-phase-a2 :",
            "spot-real64-phase-a2 : tests",
            1,
        )
        with self.assertRaises(PhaseA2Error):
            validate_makefile_contract(makefile)

    def test_make_target_cannot_gain_recipe(self) -> None:
        makefile = (ROOT / "Makefile").read_text().replace(
            "\tsh validation/iterative/real64_phase_a2/run_phase_a2.sh",
            "\tsh validation/iterative/real64_phase_a2/run_phase_a2.sh\n"
            "\t./rdragon unsafe.x2m",
            1,
        )
        with self.assertRaises(PhaseA2Error):
            validate_makefile_contract(makefile)

    def test_open_path_cannot_be_hidden(self) -> None:
        self.rejected(lambda data: data["remaining_open_path"].clear())

    def test_interpretation_cannot_claim_convergence(self) -> None:
        self.rejected(
            lambda data: data["interpretation"].append(
                "The radial iteration converged."
            )
        )


if __name__ == "__main__":
    unittest.main()

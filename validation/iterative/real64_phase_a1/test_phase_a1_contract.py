#!/usr/bin/env python3
"""Mutation tests for the fail-closed Phase-A1 precision manifest."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a1 import PhaseA1Error, ROOT, validate


MANIFEST = (
    ROOT / "validation/iterative/real64_phase_a1/precision_manifest.json"
)


class PhaseA1ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA1Error):
            validate(candidate, verify_canonical=False)

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA1Error):
            validate(candidate)

    def test_full_closure_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "phase_a_static_closure", True
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

    def test_transport_solve_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__("transport_solves", 1)
        )

    def test_locked_branch_cannot_expand(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("NANI", 2)
        )

    def test_mutable_kernel_kind_cannot_fall(self) -> None:
        self.rejected(
            lambda data: data["kind_contract"].__setitem__(
                "mutable_working_binary64", ["QN", "S"]
            )
        )

    def test_preterminal_downcast_cannot_be_allowed(self) -> None:
        self.rejected(
            lambda data: data["kind_contract"].__setitem__(
                "preterminal_downcast", "ALLOWED"
            )
        )

    def test_conversion_site_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["allowed_conversion_sites"].append(
                {
                    "procedure": "MCGFCS64_LOCKED",
                    "direction": "binary64-to-binary32",
                    "expressions": ["real(s, real32)"],
                }
            )
        )

    def test_global_real8_flag_cannot_be_enabled(self) -> None:
        self.rejected(
            lambda data: data["kind_contract"].__setitem__(
                "global_default_real_8", "ALLOWED"
            )
        )

    def test_legacy_route_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["legacy_route_identity"].__setitem__(
                "new_kernel_call_count_in_src", 1
            )
        )

    def test_test_dragon_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["synthetic_tests"].__setitem__("dragon_runs", 1)
        )

    def test_default_all_cannot_include_slice(self) -> None:
        self.rejected(
            lambda data: data["build_contract"].__setitem__(
                "added_to_default_all", True
            )
        )

    def test_forbidden_flag_cannot_clear(self) -> None:
        self.rejected(
            lambda data: data["build_contract"].__setitem__(
                "forbidden_flag", ""
            )
        )

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

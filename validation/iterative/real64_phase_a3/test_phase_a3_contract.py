#!/usr/bin/env python3
"""Fail-closed semantic mutation tests for the REAL64 Phase-A3 seam."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a3 import (
    PhaseA3Error,
    ROOT,
    validate,
    validate_makefile_contract,
    validate_runner_contract,
)


MANIFEST = (
    ROOT / "validation/iterative/real64_phase_a3/precision_manifest.json"
)
MAKEFILE = ROOT / "Makefile"
RUNNER = (
    ROOT / "validation/iterative/real64_phase_a3/run_phase_a3.sh"
)


class PhaseA3ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA3Error):
            validate(candidate, verify_canonical=False)

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA3Error):
            validate(candidate)

    def test_phase_a_closure_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "phase_a_static_closure", True
            )
        )

    def test_link_or_execution_cannot_be_authorized(self) -> None:
        for field in ("link_authorized", "execution_authorized"):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field: data["status"].__setitem__(
                        field, True
                    )
                )

    def test_actual_moc_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "actual_moc_response_validated", True
            )
        )

    def test_real_context_cannot_be_claimed_bound(self) -> None:
        for field in (
            "facade_callback_connected",
            "tracking_data_bound",
            "continuous_real64_lane",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field: data["status"].__setitem__(
                        field, True
                    )
                )

    def test_production_connection_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "production_route_connected", True
            )
        )

    def test_transport_or_dragon_cannot_be_authorized(self) -> None:
        for field in ("transport_solves", "dragon_processes_authorized"):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field: data["status"].__setitem__(
                        field, 1
                    )
                )

    def test_convergence_cannot_be_claimed(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "outer_convergence", "CONVERGED"
            )
        )

    def test_transport_call_order_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"].__setitem__(
                "transport_call_sequence", ["MCGFST", "MCGFCF"]
            )
        )

    def test_transport_call_count_cannot_change(self) -> None:
        for field, value in (
            ("MCGFCF_call_count", 2),
            ("MCGFST_call_count", 0),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["abi_contract"].__setitem__(field, value)
                )

    def test_real64_mutable_kinds_cannot_change(self) -> None:
        for field, value in (
            ("source_kind", "REAL32-INTENT-IN"),
            ("raw_response_kind", "REAL32-INTENT-INOUT"),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["abi_contract"].__setitem__(field, value)
                )

    def test_legacy_intent_cannot_be_invented(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"].__setitem__(
                "legacy_dummy_intent", "INTENT-IN-AND-INOUT"
            )
        )

    def test_forwarded_subsch_cannot_gain_explicit_interface(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"].__setitem__(
                "forwarded_SUBSCH_interface", "EXPLICIT-PROCEDURE-INTERFACE"
            )
        )

    def test_kpsys_type_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"].__setitem__(
                "KPSYS", "INTEGER-RANK1"
            )
        )

    def test_pjjind_rank_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"].__setitem__(
                "PJJIND", "INTEGER-RANK1-FLAT"
            )
        )

    def test_frozen_operator_kind_cannot_be_promoted(self) -> None:
        self.rejected(
            lambda data: data["abi_contract"][
                "frozen_real32_operator_inputs"
            ].remove("SIGAL")
        )

    def test_synthetic_transport_context_cannot_be_allowed(self) -> None:
        self.rejected(
            lambda data: data["context_contract"].__setitem__(
                "synthetic_or_stub_transport_context_allowed", True
            )
        )

    def test_unbound_context_cannot_be_claimed_bound(self) -> None:
        for field in (
            "real_tracking_context_bound",
            "real_KPSYS_PJJ_directories_bound",
            "EXP1_table_initialization_bound",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["context_contract"].__setitem__(field, True)
                )

    def test_legacy_xsi_cannot_be_claimed_conforming(self) -> None:
        for field in (
            "legacy_actual_designator_standard_conforming",
            "legacy_production_call_fixed",
            "runtime_safety_validated",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["legacy_xsi_conformance"].__setitem__(field, True)
                )

    def test_callback_template_cannot_be_claimed_matching_or_fixed(self) -> None:
        for field in (
            "MCCGF_MCGFFA_TEMPLATE_matches_MCGFFAR",
            "legacy_template_fixed",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["legacy_callback_interface_warning"].__setitem__(
                        field, True
                    )
                )

    def test_link_barrier_cannot_be_removed(self) -> None:
        for field, value in (
            ("must_remain_undefined", False),
            ("removal_authorized", True),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["link_barrier"].__setitem__(field, value)
                )

    def test_link_barrier_symbol_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["link_barrier"].__setitem__(
                "symbol", "SPOR64_A3_LINK_ALLOWED"
            )
        )

    def test_compile_only_build_contract_cannot_change(self) -> None:
        for field, value in (
            ("phase_a3_fortran_commands_compile_only", False),
            ("link_commands_allowed", ["gfortran -o phase_a3"]),
            ("added_to_default_all", True),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["build_contract"].__setitem__(field, value)
                )

    def test_open_path_cannot_be_hidden(self) -> None:
        self.rejected(lambda data: data["remaining_open_path"].clear())

    def test_make_target_cannot_gain_prerequisite(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "spot-real64-phase-a3 :",
            "spot-real64-phase-a3 : spot-real64-phase-a2",
            1,
        )
        self.assertNotEqual(mutated, makefile, "Phase-A3 target missing")
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_make_target_cannot_gain_extra_recipe(self) -> None:
        makefile = MAKEFILE.read_text()
        recipe = (
            "\tsh validation/iterative/real64_phase_a3/run_phase_a3.sh"
        )
        mutated = makefile.replace(
            recipe,
            recipe + "\n\t./rdragon unsafe.x2m",
            1,
        )
        self.assertNotEqual(mutated, makefile, "Phase-A3 recipe missing")
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_phase_a3_cannot_join_default_all_dependencies(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "all :",
            "all : spot-real64-phase-a3",
            1,
        )
        self.assertNotEqual(mutated, makefile, "default all target missing")
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_phase_a3_runner_cannot_enter_default_recipe(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "\t$(MAKE) -C src",
            "\t$(MAKE) -C src\n"
            "\tsh validation/iterative/real64_phase_a3/run_phase_a3.sh",
            1,
        )
        self.assertNotEqual(mutated, makefile, "default recipe missing")
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_phase_a3_runner_alias_cannot_enter_makefile(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = (
            "A3_RUNNER = "
            "validation/iterative/real64_phase_a3/run_phase_a3.sh\n"
            + makefile
        )
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_default_make_target_cannot_change(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = "bootstrap :\n\t@:\n" + makefile
        with self.assertRaises(PhaseA3Error):
            validate_makefile_contract(mutated)

    def test_quoted_dragon_command_is_rejected(self) -> None:
        mutated = (
            RUNNER.read_text()
            + '\n"$ROOT/bin/Darwin_arm64/Dragon" unsafe.x2m\n'
        )
        with self.assertRaises(PhaseA3Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_runner_content_is_hash_locked(self) -> None:
        with self.assertRaises(PhaseA3Error):
            validate_runner_contract(RUNNER.read_text() + "\n")

    def test_unresolved_symbol_count_cannot_be_loosened(self) -> None:
        runner = RUNNER.read_text()
        mutated = runner.replace(
            'test "$unresolved_count" -ne 8',
            'test "$unresolved_count" -ne 9',
            1,
        )
        self.assertNotEqual(mutated, runner, "unresolved count check missing")
        with self.assertRaises(PhaseA3Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_untracked_compiler_and_artifact_execution_are_rejected(
        self,
    ) -> None:
        mutated = (
            RUNNER.read_text()
            + '\ngfortran helper.f90 -o "$BUILD_DIR/helper"\n'
            + '"$BUILD_DIR/helper" --run\n'
        )
        with self.assertRaises(PhaseA3Error):
            validate_runner_contract(mutated, verify_hash=False)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Fail-closed mutation tests for the Phase-A6 rendezvous boundary."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a6 import (
    PhaseA6Error,
    ROOT,
    validate,
    validate_implementation_source,
    validate_legacy_mcgfl1_facts,
    validate_makefile_contract,
    validate_positive_fixture,
    validate_runner_contract,
)


HERE = ROOT / "validation/iterative/real64_phase_a6"
MANIFEST = HERE / "precision_manifest.json"
IMPLEMENTATION = HERE / "SPOR64_A6.f90"
POSITIVE_FIXTURE = HERE / "compile_spor64_a6_host_callsite.f90"
MAKEFILE = ROOT / "Makefile"
RUNNER = HERE / "run_phase_a6.sh"
MCGFL1 = ROOT / "src/MCGFL1.f"
SYMBOL_COUNTS = {
    "a3_poison_sentinel_object": 8,
    "a6": 2,
    "host_callsite": 5,
}


class PhaseA6ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())
        cls.source = IMPLEMENTATION.read_text()
        cls.fixture = POSITIVE_FIXTURE.read_text()
        cls.makefile = MAKEFILE.read_text()
        cls.runner = RUNNER.read_text()
        cls.mcgfl1 = MCGFL1.read_text()

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA6Error):
            validate(candidate, verify_canonical=False)

    def source_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.source, "source mutation missed")
        with self.assertRaises(PhaseA6Error):
            validate_implementation_source(mutated)

    def fixture_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.fixture, "fixture mutation missed")
        with self.assertRaises(PhaseA6Error):
            validate_positive_fixture(mutated)

    def makefile_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.makefile, "Makefile mutation missed")
        with self.assertRaises(PhaseA6Error):
            validate_makefile_contract(mutated)

    def runner_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.runner, "runner mutation missed")
        with self.assertRaises(PhaseA6Error):
            validate_runner_contract(
                mutated,
                verify_hash=False,
                expected_counts=SYMBOL_COUNTS,
            )

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA6Error):
            validate(candidate)

    def test_status_cannot_claim_runtime_or_production(self) -> None:
        changes = (
            ("phase_a_static_closure", True),
            ("link_authorized", True),
            ("execution_authorized", True),
            ("production_admission", True),
            ("runtime_preflight_implemented", True),
            ("runtime_object_provenance_validated", True),
            ("tracking_position_validated", True),
            ("real_KPSYS_PJJ_directories_bound", True),
            ("EXP1_identity_bound", True),
            ("continuous_real64_lane", True),
            ("production_route_connected", True),
            ("default_runtime_route_changed", True),
            ("actual_moc_response_validated", True),
            ("transport_solves", 1),
            ("dragon_processes_authorized", 1),
            ("outer_convergence", "CONVERGED"),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["status"].__setitem__(field, value)
                )

    def test_rendezvous_must_remain_default_off_and_mutually_exclusive(
        self,
    ) -> None:
        changes = (
            ("default_enabled", True),
            ("arms_mutually_exclusive", False),
            ("host_legacy_response_and_A5_permitted_in_same_visit", True),
            ("host_MCGFST_after_A5_permitted", True),
            ("enabled_route_selected_before_admission_checks", False),
            ("production_insertion_present", True),
            ("production_admission_satisfied", True),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["host_rendezvous"].__setitem__(field, value)
                )

    def test_mutable_state_blocker_cannot_be_repaired_by_conversion(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["production_admission_blockers"][
                "mutable_state"
            ].__setitem__("rendezvous_conversion_allowed", True)
        )
        self.rejected(
            lambda data: data["production_admission_blockers"][
                "mutable_state"
            ].__setitem__("current_QFR_kind", "REAL64")
        )

    def test_sc_blocker_cannot_be_repaired_by_gather_or_lcm(self) -> None:
        for field in (
            "complete_bundle_available",
            "rendezvous_gather_allowed",
            "rendezvous_LCM_read_allowed",
            "last_group_pointer_reuse_allowed",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["production_admission_blockers"][
                        "sc_bundle"
                    ].__setitem__(field, True)
                )

    def test_direct_host_map_cannot_be_relabelled(self) -> None:
        self.rejected(
            lambda data: data["direct_host_map"]["qn"].__setitem__(
                "state", "DIRECT-REAL64"
            )
        )
        self.rejected(
            lambda data: data["direct_host_map"]["sc"].__setitem__(
                "host", "LAST-XSSC-POINTER"
            )
        )

    def test_static_lifetime_cannot_be_promoted_to_runtime(self) -> None:
        self.rejected(
            lambda data: data["static_lifetime_contract"].__setitem__(
                "runtime_lifetime_validated", True
            )
        )
        self.rejected(
            lambda data: data["static_lifetime_contract"].__setitem__(
                "one_group_XSSC_is_complete_bundle", True
            )
        )

    def test_provenance_boundary_cannot_be_promoted(self) -> None:
        for field, value in self.original["provenance_boundary"].items():
            if value is False:
                with self.subTest(field=field):
                    self.rejected(
                        lambda data, field=field:
                        data["provenance_boundary"].__setitem__(field, True)
                    )

    def test_forbidden_actions_cannot_be_authorized(self) -> None:
        for field in (
            "mutable_state_kind_conversion",
            "SC_gather_or_reconstruction",
            "file_IO",
            "LCM_IO",
            "transport_application",
            "object_link",
            "object_execution",
            "Dragon_execution",
            "default_on_switch",
            "empirical_parameter",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["forbidden_actions"].__setitem__(field, False)
                )

    def test_call_boundary_cannot_expand(self) -> None:
        changes = (
            ("direct_A4_calls", 1),
            ("direct_A3_calls", 1),
            ("direct_legacy_calls", 1),
            ("link_barrier_count", 2),
            ("A6_link_barriers", 1),
            ("production_callers", 1),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["call_boundary"].__setitem__(field, value)
                )

    def test_compile_only_counts_must_remain_zero(self) -> None:
        for field in (
            "phase_a6_fortran_objects_linked",
            "phase_a6_fortran_executables_built",
            "phase_a6_fortran_objects_executed",
            "prerequisite_runners_executed",
            "synthetic_executions",
            "host_rendezvous_executions",
            "tracking_reads",
            "transport_solves",
            "dragon_runs",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["compile_tests"].__setitem__(field, 1)
                )

    def test_build_contract_cannot_link_or_join_defaults(self) -> None:
        changes = (
            ("added_to_default_all", True),
            ("added_to_tests", True),
            ("added_to_spot_fast", True),
            ("all_fortran_commands_compile_only", False),
            ("link_commands_allowed", ["gfortran -o unsafe"]),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["build_contract"].__setitem__(field, value)
                )

    def test_original_implementation_passes_static_contract(self) -> None:
        validate_implementation_source(self.source)

    def test_default_switch_cannot_be_enabled(self) -> None:
        self.source_rejected(
            self.source.replace(
                "SPOR64_A6_DEFAULT_ENABLED = .false.",
                "SPOR64_A6_DEFAULT_ENABLED = .true.",
                1,
            )
        )

    def test_route_selection_must_be_fail_closed_and_ordered(self) -> None:
        for statement in (
            "    route_selected = .false.\n",
            "    if (.not. enabled) return\n",
            "    route_selected = .true.\n",
        ):
            with self.subTest(statement=statement.strip()):
                self.source_rejected(self.source.replace(statement, "", 1))

    def test_locked_branch_guard_cannot_be_removed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    if (isch /= 11 .or. npjjm /= 1) return\n", "", 1
            )
        )

    def test_shape_guards_cannot_be_removed(self) -> None:
        guards = (
            "    if (size(kpsys) /= ngeff) return\n",
            "    if (size(nzon) /= nlong) return\n",
            "    if (size(volume) /= nlong) return\n",
        )
        for guard in guards:
            with self.subTest(guard=guard.strip()):
                self.source_rejected(self.source.replace(guard, "", 1))

    def test_complete_sc_bundle_guard_cannot_be_removed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    if (size(sc_by_group,1) /= m+1 .or. &\n"
                "        size(sc_by_group,2) /= 1 .or. &\n"
                "        size(sc_by_group,3) /= ngeff) return\n",
                "",
                1,
            )
        )

    def test_a5_call_map_and_count_are_exact(self) -> None:
        self.source_rejected(
            self.source.replace(
                "        ndim, nzon, qfr64_host, phiin64_host,",
                "        ndim, nzon, phiin64_host, qfr64_host,",
                1,
            )
        )
        self.source_rejected(
            self.source.replace(
                "    call "
                "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(",
                "    call "
                "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED()\n"
                "    call "
                "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(",
                1,
            )
        )

    def test_direct_legacy_or_prerequisite_call_is_rejected(self) -> None:
        for call in (
            "MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED",
            "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
            "MCGFCF",
            "MCGFST",
        ):
            with self.subTest(call=call):
                self.source_rejected(
                    self.source.replace(
                        "    call "
                        "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(",
                        f"    call {call}()\n"
                        "    call "
                        "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(",
                        1,
                    )
                )

    def test_conversion_gather_io_and_model_mechanisms_are_rejected(
        self,
    ) -> None:
        insertions = (
            "    source64 = real(qfr64_host, real64)\n",
            "    allocate(hidden_sc(1))\n",
            "    read(iftrak) status\n",
            "    alpha = 0.5_real64\n",
        )
        marker = (
            "    call "
            "MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED("
        )
        for insertion in insertions:
            with self.subTest(insertion=insertion.strip()):
                self.source_rejected(
                    self.source.replace(marker, insertion + marker, 1)
                )

    def test_save_and_common_state_are_rejected(self) -> None:
        declarations = (
            "  integer, save :: hidden_state = 0\n",
            "  common /hidden/ hidden_state\n",
        )
        for declaration in declarations:
            with self.subTest(declaration=declaration.strip()):
                self.source_rejected(
                    self.source.replace(
                        "  private\n", "  private\n" + declaration, 1
                    )
                )

    def test_original_positive_fixture_passes(self) -> None:
        validate_positive_fixture(self.fixture)

    def test_fixture_must_pass_default_constant_once_as_first_actual(
        self,
    ) -> None:
        self.fixture_rejected(
            self.fixture.replace(
                "      SPOR64_A6_DEFAULT_ENABLED, kpsys,",
                "      .true., kpsys,",
                1,
            )
        )
        call = (
            "  call "
            "MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED("
        )
        self.fixture_rejected(
            self.fixture.replace(call, call + ")\n" + call, 1)
        )

    def test_legacy_mcgfl1_facts_are_lexically_locked(self) -> None:
        validate_legacy_mcgfl1_facts(self.mcgfl1)
        with self.assertRaises(PhaseA6Error):
            validate_legacy_mcgfl1_facts(
                self.mcgfl1.replace(
                    "      REAL QFR", "      DOUBLE PRECISION QFR", 1
                )
            )
        with self.assertRaises(PhaseA6Error):
            validate_legacy_mcgfl1_facts(
                self.mcgfl1.replace(
                    "           CALL LCMGPD(JPSYS,'DRAGON-S0XSC',XSSC_PTR)\n",
                    "",
                    1,
                )
            )

    def test_makefile_delta_is_exact_and_isolated(self) -> None:
        mutations = (
            self.makefile.replace(
                "spot-real64-phase-a6 :",
                "spot-real64-phase-a6 : spot-real64-phase-a5",
                1,
            ),
            self.makefile.replace(
                "all :", "all : spot-real64-phase-a6", 1
            ),
            self.makefile.replace(
                "\tsh validation/iterative/real64_phase_a6/run_phase_a6.sh",
                "\tsh validation/iterative/real64_phase_a6/run_phase_a6.sh\n"
                "\t./rdragon unsafe.x2m",
                1,
            ),
        )
        for mutation in mutations:
            with self.subTest():
                self.makefile_rejected(mutation)

    def test_runner_is_object_only_and_count_exact(self) -> None:
        validate_runner_contract(
            self.runner,
            expected_counts=SYMBOL_COUNTS,
        )
        mutations = (
            self.runner + "\nld -o unsafe SPOR64_A6.o\n",
            self.runner + "\ngfortran -c unsafe.f90 -o unsafe.o\n",
            self.runner + '\n"$BUILD_DIR/SPOR64_A6.o"\n',
            self.runner.replace(
                ' -c "$1" -o "$2"', ' "$1" -o "$2"', 1
            ),
            self.runner.replace(
                'a6_unresolved.log")" -ne 2',
                'a6_unresolved.log")" -ne 3',
                1,
            ),
            self.runner.replace("DRAGON-RUNS=0", "DRAGON-RUNS=1", 1),
        )
        for mutation in mutations:
            with self.subTest():
                self.runner_rejected(mutation)


if __name__ == "__main__":
    unittest.main()

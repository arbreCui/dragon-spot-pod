#!/usr/bin/env python3
"""Fail-closed mutation tests for the Phase-A5 population boundary."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a5 import (
    PhaseA5Error,
    ROOT,
    validate,
    validate_implementation_source,
    validate_makefile_contract,
    validate_runner_contract,
)


HERE = ROOT / "validation/iterative/real64_phase_a5"
MANIFEST = HERE / "precision_manifest.json"
IMPLEMENTATION = HERE / "SPOR64_A5.f90"
MAKEFILE = ROOT / "Makefile"
RUNNER = HERE / "run_phase_a5.sh"
SYMBOL_COUNTS = {"a3": 8, "a4": 10, "a5": 6, "anchor": 5}


class PhaseA5ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())
        cls.source = IMPLEMENTATION.read_text()
        cls.makefile = MAKEFILE.read_text()
        cls.runner = RUNNER.read_text()

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA5Error):
            validate(candidate, verify_canonical=False)

    def source_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.source, "source mutation missed")
        with self.assertRaises(PhaseA5Error):
            validate_implementation_source(mutated)

    def runner_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.runner, "runner mutation missed")
        with self.assertRaises(PhaseA5Error):
            validate_runner_contract(
                mutated,
                verify_hash=False,
                expected_counts=SYMBOL_COUNTS,
            )

    def makefile_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.makefile, "Makefile mutation missed")
        with self.assertRaises(PhaseA5Error):
            validate_makefile_contract(mutated)

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA5Error):
            validate(candidate)

    def test_status_cannot_overclaim(self) -> None:
        changes = (
            ("phase_a_static_closure", True),
            ("link_authorized", True),
            ("execution_authorized", True),
            ("context_population_executed", True),
            ("real_context_provenance_bound", True),
            ("runtime_object_provenance_validated", True),
            ("carrier_proves_provenance", True),
            ("current_MCGFL1_callsite_bound", True),
            ("production_REAL64_host_inputs_bound", True),
            ("tracking_position_validated", True),
            ("real_KPSYS_PJJ_directories_bound", True),
            ("EXP1_identity_bound", True),
            ("actual_moc_response_validated", True),
            ("continuous_real64_lane", True),
            ("production_route_connected", True),
            ("default_runtime_route_changed", True),
            ("transport_solves", 1),
            ("dragon_processes_authorized", 1),
            ("stage4_qualified", True),
            ("stage5_authorized", True),
            ("outer_convergence", "CONVERGED"),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["status"].__setitem__(field, value)
                )

    def test_canonical_storage_cannot_be_called_physical_data(self) -> None:
        self.rejected(
            lambda data: data["population_contract"].__setitem__(
                "defined_zero_is_physical_coefficient", True
            )
        )
        self.rejected(
            lambda data: data["population_contract"][
                "locked_storage_definitions"
            ].__setitem__("context%caz0", "EXACT-LEGACY-VALUE")
        )

    def test_population_contract_cannot_add_model_mechanisms(self) -> None:
        changes = (
            ("empirical_coefficients_added", 1),
            ("relaxation_or_acceleration_added", True),
            ("threshold_or_tolerance_added", True),
            ("interpolation_fit_clip_or_model_added", True),
            ("A5_staging_matrices", 1),
            ("binary64_to_binary32_mutable_state_conversion", True),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["population_contract"].__setitem__(field, value)
                )

    def test_population_lifecycle_is_exact(self) -> None:
        for field, value in (
            ("public_context_result", True),
            ("A4_calls", 2),
            ("A4_call_only_after_population_OK", False),
            ("enabled_true_assignments", 2),
            ("enabled_reset_after_A4", False),
            ("context_escapes", True),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["population_contract"].__setitem__(field, value)
                )

    def test_provenance_boundary_cannot_be_promoted(self) -> None:
        for field, value in self.original["provenance_boundary"].items():
            if value is False:
                with self.subTest(field=field):
                    self.rejected(
                        lambda data, field=field:
                        data["provenance_boundary"].__setitem__(field, True)
                    )

    def test_call_boundary_cannot_expand(self) -> None:
        for field, value in (
            ("direct_A2_calls", 1),
            ("direct_A3_calls", 1),
            ("direct_legacy_calls", 1),
            ("link_barrier_count", 2),
            ("A5_link_barriers", 1),
            ("production_callers", 1),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["call_boundary"].__setitem__(field, value)
                )

    def test_compile_only_counts_cannot_change(self) -> None:
        for field in (
            "phase_a5_fortran_objects_linked",
            "phase_a5_fortran_executables_built",
            "phase_a5_fortran_objects_executed",
            "prerequisite_runners_executed",
            "synthetic_executions",
            "context_population_executions",
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
        for field, value in (
            ("added_to_default_all", True),
            ("all_fortran_commands_compile_only", False),
            ("link_commands_allowed", ["gfortran -o a5"]),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["build_contract"].__setitem__(field, value)
                )

    def test_frozen_legacy_hash_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["baseline"]["legacy_source_sha256"].__setitem__(
                "src/MCGFCF.f", "0" * 64
            )
        )

    def test_open_path_cannot_be_hidden(self) -> None:
        self.rejected(lambda data: data["remaining_open_path"].clear())

    def test_original_implementation_passes_static_contract(self) -> None:
        validate_implementation_source(self.source)

    def test_context_cannot_escape_public_signature(self) -> None:
        self.source_rejected(
            self.source.replace(
                "wzmu, volume, raw_response, status)",
                "wzmu, volume, raw_response, status, context)",
                1,
            )
        )

    def test_private_population_cannot_be_exposed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "public :: MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED",
                "public :: MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED\n"
                "  public :: populate_context",
                1,
            )
        )

    def test_context_cannot_enable_before_population_success(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    call populate_context(",
                "    context%enabled = .true.\n    call populate_context(",
                1,
            )
        )

    def test_context_must_reset_after_A4(self) -> None:
        head, separator, tail = self.source.rpartition(
            "    context%enabled = .false."
        )
        self.assertTrue(separator, "reset assignment missing")
        self.source_rejected(
            head + "    context%enabled = .true." + tail
        )

    def test_A4_call_must_be_unique(self) -> None:
        marker = "    context%enabled = .false.\n  end subroutine"
        self.source_rejected(
            self.source.replace(
                marker,
                "    call "
                "MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED()\n"
                + marker,
                1,
            )
        )

    def test_direct_A3_or_legacy_call_is_rejected(self) -> None:
        for call in (
            "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
            "MCGFCF",
            "MCGFST",
        ):
            with self.subTest(call=call):
                self.source_rejected(
                    self.source.replace(
                        "    call populate_context(",
                        f"    call {call}()\n    call populate_context(",
                        1,
                    )
                )

    def test_scalar_population_sources_cannot_be_swapped(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    context%nmax = n2max",
                "    context%nmax = nbtr",
                1,
            )
        )

    def test_array_population_sources_cannot_be_swapped(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    context%zmu = zmu",
                "    context%zmu = wzmu",
                1,
            )
        )

    def test_unread_formal_storage_must_be_canonical_zero(self) -> None:
        for old, new in (
            ("context%caz0 = 0.0_real64", "context%caz0 = 1.0_real64"),
            ("context%cpo = 0.0_real32", "context%cpo = 1.0_real32"),
            ("context%xsi = 0.0_real64", "context%xsi = 1.0_real64"),
        ):
            with self.subTest(component=old.split("%", 1)[1].split()[0]):
                self.source_rejected(self.source.replace(old, new, 1))

    def test_discrete_identities_must_remain_one(self) -> None:
        for old, new in (
            ("context%isgnr = 1", "context%isgnr = -1"),
            ("context%pjjind = 1", "context%pjjind = 2"),
        ):
            with self.subTest(component=old.split("%", 1)[1].split()[0]):
                self.source_rejected(self.source.replace(old, new, 1))

    def test_allocation_failure_must_fail_closed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    if (allocation_status /= 0) return\n",
                "",
                1,
            )
        )

    def test_shape_guards_cannot_be_removed(self) -> None:
        guards = (
            "    if (size(kpsys) /= ngeff) return\n",
            "    if (size(caz1) <= 0 .or. size(caz2) /= size(caz1)) return\n",
            "    if (size(zmu) <= 0 .or. size(wzmu) /= size(zmu)) return\n",
            "    if (size(volume) /= n) return\n",
        )
        for guard in guards:
            with self.subTest(guard=guard.strip()):
                self.source_rejected(self.source.replace(guard, "", 1))

    def test_group_order_guard_cannot_be_removed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "      if (ngind(group) /= ngind(group-1)+1) return\n",
                "",
                1,
            )
        )

    def test_active_KPSYS_association_guard_cannot_be_removed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "      if (nconv(group) .and. "
                ".not. c_associated(kpsys(group))) return\n",
                "",
                1,
            )
        )

    def test_direct_mutable_output_assignment_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    call populate_context(",
                "    source = 0.0_real64\n    call populate_context(",
                1,
            )
        )

    def test_IO_and_LCM_access_are_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    call populate_context(",
                "    read(iftrak) group\n    call populate_context(",
                1,
            )
        )

    def test_empirical_parameter_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    integer :: group, population_status",
                "    integer :: group, population_status\n"
                "    real(real64) :: alpha = 0.5_real64",
                1,
            )
        )

    def test_hidden_save_or_pointer_state_is_rejected(self) -> None:
        mutations = (
            "  integer, save :: hidden_state = 0\n",
            "  real(real64), pointer :: hidden_state(:)\n",
        )
        for declaration in mutations:
            with self.subTest(declaration=declaration.strip()):
                self.source_rejected(
                    self.source.replace(
                        "  private\n",
                        "  private\n" + declaration,
                        1,
                    )
                )

    def test_precision_conversion_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    context%volume = volume",
                "    context%volume = real(volume, real32)",
                1,
            )
        )

    def test_population_transform_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    context%caz1 = caz1",
                "    context%caz1 = reshape(caz1, shape(context%caz1))",
                1,
            )
        )

    def test_make_target_cannot_gain_prerequisite(self) -> None:
        self.makefile_rejected(
            self.makefile.replace(
                "spot-real64-phase-a5 :",
                "spot-real64-phase-a5 : spot-real64-phase-a4",
                1,
            )
        )

    def test_A5_cannot_join_default_all(self) -> None:
        self.makefile_rejected(
            self.makefile.replace(
                "all :",
                "all : spot-real64-phase-a5",
                1,
            )
        )

    def test_make_target_cannot_gain_extra_recipe(self) -> None:
        recipe = "\tsh validation/iterative/real64_phase_a5/run_phase_a5.sh"
        self.makefile_rejected(
            self.makefile.replace(
                recipe,
                recipe + "\n\t./rdragon unsafe.x2m",
                1,
            )
        )

    def test_original_runner_passes_static_contract(self) -> None:
        validate_runner_contract(
            self.runner,
            expected_counts=SYMBOL_COUNTS,
        )

    def test_runner_cannot_link(self) -> None:
        self.runner_rejected(self.runner + "\nld -o a5 SPOR64_A5.o\n")

    def test_runner_cannot_use_untracked_compiler(self) -> None:
        self.runner_rejected(
            self.runner + "\ngfortran -c unsafe.f90 -o unsafe.o\n"
        )

    def test_runner_cannot_invoke_old_runner(self) -> None:
        self.runner_rejected(
            self.runner + '\nsh "$A4/run_phase_a4.sh"\n'
        )

    def test_runner_cannot_execute_build_artifact(self) -> None:
        self.runner_rejected(
            self.runner + '\n"$BUILD_DIR/SPOR64_A5.o"\n'
        )

    def test_runner_compiler_commands_must_remain_object_only(self) -> None:
        self.runner_rejected(
            self.runner.replace(
                ' -c "$1" -o "$2"',
                ' "$1" -o "$2"',
                1,
            )
        )

    def test_runner_zero_execution_declarations_are_locked(self) -> None:
        self.runner_rejected(
            self.runner.replace("DRAGON-RUNS=0", "DRAGON-RUNS=1", 1)
        )

    def test_runner_symbol_count_is_exact(self) -> None:
        self.runner_rejected(
            self.runner.replace(
                'a5_unresolved.log")" -ne 6',
                'a5_unresolved.log")" -ne 7',
                1,
            )
        )


if __name__ == "__main__":
    unittest.main()

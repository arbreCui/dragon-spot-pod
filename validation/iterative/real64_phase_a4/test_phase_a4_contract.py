#!/usr/bin/env python3
"""Fail-closed mutation tests for the REAL64 Phase-A4 host closure."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a4 import (
    PhaseA4Error,
    ROOT,
    validate,
    validate_implementation_source,
    validate_makefile_contract,
    validate_runner_contract,
)


HERE = ROOT / "validation/iterative/real64_phase_a4"
MANIFEST = HERE / "precision_manifest.json"
MAKEFILE = ROOT / "Makefile"
RUNNER = HERE / "run_phase_a4.sh"
IMPLEMENTATION = HERE / "SPOR64_A4.f90"


class PhaseA4ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())
        cls.source = IMPLEMENTATION.read_text()

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA4Error):
            validate(candidate, verify_canonical=False)

    def source_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.source, "source mutation missed")
        with self.assertRaises(PhaseA4Error):
            validate_implementation_source(mutated)

    def test_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original))

    def test_canonical_hash_rejects_any_change(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["title"] = "altered"
        with self.assertRaises(PhaseA4Error):
            validate(candidate)

    def test_status_cannot_overclaim(self) -> None:
        changes = (
            ("phase_a_static_closure", True),
            ("link_authorized", True),
            ("execution_authorized", True),
            ("context_population_checked", True),
            ("real_context_provenance_bound", True),
            ("tracking_position_validated", True),
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

    def test_context_cannot_claim_ownership_or_provenance(self) -> None:
        changes = (
            ("carrier_owns_external_resources", True),
            ("carrier_proves_provenance", True),
            ("public_component_population_kind_checked", True),
            ("module_mutable_state", True),
            ("SAVE_or_COMMON_state", True),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["context_contract"].__setitem__(field, value)
                )

    def test_context_cannot_gain_pointer_execution(self) -> None:
        self.rejected(
            lambda data: data["context_contract"][
                "pointer_components"
            ].append("source(:,:)")
        )
        self.rejected(
            lambda data: data["context_contract"].__setitem__(
                "type_bound_execution", True
            )
        )

    def test_host_closure_contract_is_exact(self) -> None:
        changes = (
            ("staging_count", 3),
            ("staging_kind", "REAL32"),
            ("source_copyback", "ON-SUCCESS"),
            ("raw_copyback", "UNCONDITIONAL"),
            ("binary64_to_binary32_conversion", "PRESENT"),
            ("hidden_array_temporary", "ALLOWED"),
            ("callback_stored_or_escaped", True),
            ("A3_uses_host_contiguous_NGIND_NCONV", False),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["host_closure_contract"].__setitem__(field, value)
                )

    def test_call_sequence_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["host_closure_contract"].__setitem__(
                "call_sequence",
                [
                    "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED",
                    "MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED",
                ],
            )
        )

    def test_external_state_cannot_be_claimed_atomic_or_bound(self) -> None:
        for field in (
            "legacy_operator_has_recoverable_error_status",
            "tracking_file_position_atomic",
            "process_state_atomic_after_XABORT",
            "real_tracking_context_bound",
            "real_KPSYS_PJJ_directories_bound",
            "EXP1_table_initialization_bound",
            "legal_XSI_storage_is_production_fix",
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field:
                    data["external_state_boundary"].__setitem__(field, True)
                )

    def test_compile_only_counts_cannot_change(self) -> None:
        changes = (
            ("A4_unresolved_symbol_count", 11),
            ("phase_a4_objects_linked", 1),
            ("phase_a4_executables_built", 1),
            ("phase_a4_objects_executed", 1),
            ("tracking_reads", 1),
            ("transport_solves", 1),
            ("dragon_runs", 1),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["compile_tests"].__setitem__(field, value)
                )

    def test_build_contract_cannot_expand_scope(self) -> None:
        changes = (
            ("added_to_default_all", True),
            ("phase_a4_fortran_commands_compile_only", False),
            ("link_commands_allowed", ["gfortran -o a4"]),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["build_contract"].__setitem__(field, value)
                )

    def test_open_path_cannot_be_hidden(self) -> None:
        self.rejected(lambda data: data["remaining_open_path"].clear())

    def test_original_implementation_passes_static_contract(self) -> None:
        validate_implementation_source(self.source)

    def test_context_must_remain_default_off(self) -> None:
        self.source_rejected(
            self.source.replace(
                "logical :: enabled = .false.",
                "logical :: enabled = .true.",
                1,
            )
        )

    def test_context_cannot_gain_pointer_component(self) -> None:
        self.source_rejected(
            self.source.replace(
                "integer, allocatable :: isgnr(:,:), pjjind(:,:)",
                "integer, pointer :: isgnr(:,:), pjjind(:,:)",
                1,
            )
        )

    def test_context_cannot_duplicate_shared_state(self) -> None:
        self.source_rejected(
            self.source.replace(
                "integer :: nbatch = 0",
                "integer :: nbatch = 0\n    integer, allocatable :: ngind(:)",
                1,
            )
        )

    def test_context_cannot_gain_empirical_or_hidden_component(self) -> None:
        for declaration in (
            "real(real64) :: relaxation_factor = 0.5_real64",
            "real(real64), allocatable :: hidden(:)",
        ):
            with self.subTest(declaration=declaration):
                self.source_rejected(
                    self.source.replace(
                        "integer :: nbatch = 0",
                        "integer :: nbatch = 0\n    " + declaration,
                        1,
                    )
                )

    def test_module_cannot_gain_hidden_save_state(self) -> None:
        self.source_rejected(
            self.source.replace(
                "private",
                "private\n  integer, save :: hidden_state = 0",
                1,
            )
        )

    def test_module_cannot_gain_old_style_implicit_save_state(self) -> None:
        self.source_rejected(
            self.source.replace(
                "  private\n",
                "  private\n  integer hidden_state\n",
                1,
            )
        )

    def test_third_staging_array_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "raw_a3(:,:), source_a3(:,:)",
                "raw_a3(:,:), source_a3(:,:), third_a3(:,:)",
                1,
            )
        )

    def test_nonreal_or_automatic_staging_is_rejected(self) -> None:
        for declaration in (
            "integer, allocatable :: extra_stage(:)",
            "real(real64) :: hidden(kpn,ngeff)",
        ):
            with self.subTest(declaration=declaration):
                self.source_rejected(
                    self.source.replace(
                        "integer :: allocation_status",
                        "integer :: allocation_status\n      " + declaration,
                        1,
                    )
                )

    def test_real32_staging_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "real(real64), allocatable :: raw_a3",
                "real(real32), allocatable :: raw_a3",
                1,
            )
        )

    def test_callback_identity_checks_cannot_be_removed(self) -> None:
        self.source_rejected(
            self.source.replace(
                "      if (any(local_ngind /= ngind)) return\n",
                "",
                1,
            )
        )

    def test_default_off_guard_cannot_have_prior_side_effect(self) -> None:
        self.source_rejected(
            self.source.replace(
                "status = SPOR64_A4_UNSUPPORTED\n"
                "    if (.not. context%enabled) return",
                "status = SPOR64_A4_UNSUPPORTED\n"
                "    source = 0.0_real64\n"
                "    if (.not. context%enabled) return",
                1,
            )
        )

    def test_outer_mutable_intent_and_context_intent_are_locked(self) -> None:
        mutations = (
            (
                "intent(inout) :: source(:,:)",
                "intent(out) :: source(:,:)",
            ),
            (
                "type(SPOR64_A4_CONTEXT), intent(in) :: context",
                "type(SPOR64_A4_CONTEXT), intent(inout) :: context",
            ),
        )
        for old, new in mutations:
            with self.subTest(new=new):
                self.source_rejected(self.source.replace(old, new, 1))

    def test_a2_source_and_raw_actuals_cannot_be_swapped(self) -> None:
        call_marker = (
            "    call MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED"
        )
        self.assertEqual(self.source.count(call_marker), 1)
        prefix, call_tail = self.source.split(call_marker, 1)
        mutated_tail = call_tail.replace(
            "m, nani, nlin, nfunl, sc, source, kpn",
            "m, nani, nlin, nfunl, sc, raw_response, kpn",
            1,
        ).replace(
            "phase_a3_primary_response, raw_response, status)",
            "phase_a3_primary_response, source, status)",
            1,
        )
        self.assertNotEqual(mutated_tail, call_tail, "A2 call mutation missed")
        self.source_rejected(prefix + call_marker + mutated_tail)

    def test_outer_status_cannot_forge_success(self) -> None:
        self.source_rejected(
            self.source.replace(
                "        phase_a3_primary_response, raw_response, status)\n",
                "        phase_a3_primary_response, raw_response, status)\n"
                "    status = SPOR64_A4_OK\n",
                1,
            )
        )

    def test_size_cannot_precede_allocated_preflight(self) -> None:
        size_check = (
            "    if (size(context%isgnr,1) /= 4 .or. &\n"
            "        size(context%isgnr,2) /= 1) return\n"
        )
        self.assertEqual(self.source.count(size_check), 1)
        mutated = self.source.replace(size_check, "", 1).replace(
            "    if (.not. allocated(context%isgnr)) return\n",
            size_check
            + "    if (.not. allocated(context%isgnr)) return\n",
            1,
        )
        self.source_rejected(mutated)

    def test_a3_must_use_host_nconv(self) -> None:
        self.source_rejected(
            self.source.replace(
                "keyflx, keycur, nzon, nconv, &",
                "keyflx, keycur, nzon, local_nconv, &",
                1,
            )
        )

    def test_a3_must_use_host_ngind(self) -> None:
        self.source_rejected(
            self.source.replace(
                "context%volume, ng, ngind, cyclic",
                "context%volume, ng, local_ngind, cyclic",
                1,
            )
        )

    def test_a3_tracking_identity_cannot_be_replaced(self) -> None:
        self.source_rejected(
            self.source.replace(
                "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(context%iftrak, &",
                "MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(0, &",
                1,
            )
        )

    def test_callback_cannot_forge_success(self) -> None:
        self.source_rejected(
            self.source.replace(
                "          response_status)\n"
                "      if (response_status == SPOR64_A3_OK) then",
                "          response_status)\n"
                "      response_status = SPOR64_A3_OK\n"
                "      if (response_status == SPOR64_A3_OK) then",
                1,
            )
        )

    def test_staging_cannot_be_overwritten(self) -> None:
        mutations = (
            (
                "      source_a3 = local_source\n"
                "      raw_a3 = local_raw_response",
                "      source_a3 = local_source\n"
                "      raw_a3 = local_raw_response\n"
                "      source_a3 = 0.0_real64",
            ),
            (
                "          response_status)\n"
                "      if (response_status == SPOR64_A3_OK) then",
                "          response_status)\n"
                "      raw_a3 = 0.0_real64\n"
                "      if (response_status == SPOR64_A3_OK) then",
            ),
        )
        for old, new in mutations:
            with self.subTest(new=new.splitlines()[-1]):
                self.source_rejected(self.source.replace(old, new, 1))

    def test_raw_copyback_must_be_success_only(self) -> None:
        self.source_rejected(
            self.source.replace(
                "      if (response_status == SPOR64_A3_OK) then\n"
                "        local_raw_response = raw_a3\n"
                "      end if\n",
                "      local_raw_response = raw_a3\n",
                1,
            )
        )

    def test_source_copyback_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "        local_raw_response = raw_a3",
                "        local_source = source_a3\n"
                "        local_raw_response = raw_a3",
                1,
            )
        )

    def test_reshape_staging_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "source_a3 = local_source",
                "source_a3 = reshape(local_source, shape(source_a3))",
                1,
            )
        )

    def test_adapter_io_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "response_status = SPOR64_A3_INVALID",
                "read(context%iftrak) response_status\n"
                "      response_status = SPOR64_A3_INVALID",
                1,
            )
        )

    def test_adapter_print_is_rejected(self) -> None:
        self.source_rejected(
            self.source.replace(
                "    if (.not. context%enabled) return",
                "    if (.not. context%enabled) return\n"
                "    print *, status",
                1,
            )
        )

    def test_make_target_cannot_gain_prerequisite(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "spot-real64-phase-a4 :",
            "spot-real64-phase-a4 : spot-real64-phase-a3",
            1,
        )
        self.assertNotEqual(mutated, makefile, "Phase-A4 target missing")
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_make_target_cannot_gain_extra_recipe(self) -> None:
        makefile = MAKEFILE.read_text()
        recipe = (
            "\tsh validation/iterative/real64_phase_a4/run_phase_a4.sh"
        )
        mutated = makefile.replace(
            recipe,
            recipe + "\n\t./rdragon unsafe.x2m",
            1,
        )
        self.assertNotEqual(mutated, makefile, "Phase-A4 recipe missing")
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_phase_a4_cannot_join_default_all_dependencies(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "all :",
            "all : spot-real64-phase-a4",
            1,
        )
        self.assertNotEqual(mutated, makefile, "default all target missing")
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_phase_a4_runner_cannot_enter_default_recipe(self) -> None:
        makefile = MAKEFILE.read_text()
        mutated = makefile.replace(
            "\t$(MAKE) -C src",
            "\t$(MAKE) -C src\n"
            "\tsh validation/iterative/real64_phase_a4/run_phase_a4.sh",
            1,
        )
        self.assertNotEqual(mutated, makefile, "default recipe missing")
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_phase_a4_runner_alias_cannot_enter_makefile(self) -> None:
        mutated = (
            "A4_RUNNER = "
            "validation/iterative/real64_phase_a4/run_phase_a4.sh\n"
            + MAKEFILE.read_text()
        )
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_default_make_target_cannot_change(self) -> None:
        mutated = "bootstrap :\n\t@:\n" + MAKEFILE.read_text()
        with self.assertRaises(PhaseA4Error):
            validate_makefile_contract(mutated)

    def test_quoted_dragon_command_is_rejected(self) -> None:
        mutated = (
            RUNNER.read_text()
            + '\n"$ROOT/bin/Darwin_arm64/Dragon" unsafe.x2m\n'
        )
        with self.assertRaises(PhaseA4Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_original_runner_passes_static_contract(self) -> None:
        validate_runner_contract(RUNNER.read_text(), verify_hash=False)

    def test_frozen_a3_runner_cannot_replace_a2_prerequisite(self) -> None:
        runner = RUNNER.read_text()
        mutated = runner.replace(
            'sh "$A2/run_phase_a2.sh"',
            'sh "$A3/run_phase_a3.sh"',
            1,
        )
        self.assertNotEqual(mutated, runner, "A2 prerequisite call missing")
        with self.assertRaises(PhaseA4Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_runner_content_is_hash_locked(self) -> None:
        with self.assertRaises(PhaseA4Error):
            validate_runner_contract(RUNNER.read_text() + "\n")

    def test_unresolved_symbol_count_cannot_be_loosened(self) -> None:
        runner = RUNNER.read_text()
        mutated = runner.replace(
            'a4_unresolved.log")" -ne 10',
            'a4_unresolved.log")" -ne 11',
            1,
        )
        self.assertNotEqual(mutated, runner, "A4 symbol count check missing")
        with self.assertRaises(PhaseA4Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_untracked_compiler_and_artifact_execution_are_rejected(
        self,
    ) -> None:
        mutated = (
            RUNNER.read_text()
            + '\ngfortran helper.f90 -o "$BUILD_DIR/helper"\n'
            + '"$BUILD_DIR/helper" --run\n'
        )
        with self.assertRaises(PhaseA4Error):
            validate_runner_contract(mutated, verify_hash=False)

    def test_absolute_compiler_and_linker_are_rejected(self) -> None:
        commands = (
            '/usr/bin/gfortran helper.f90 -o "$BUILD_DIR/helper"',
            '/usr/bin/ld -o "$BUILD_DIR/a4" "$BUILD_DIR/SPOR64_A4.o"',
        )
        for command in commands:
            with self.subTest(command=command):
                with self.assertRaises(PhaseA4Error):
                    validate_runner_contract(
                        RUNNER.read_text() + "\n" + command + "\n",
                        verify_hash=False,
                    )


if __name__ == "__main__":
    unittest.main()

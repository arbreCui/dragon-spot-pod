#!/usr/bin/env python3
"""Isolated fail-closed mutation tests for the Phase-A7 blueprint."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a7 import (
    EXPECTED_RECEIPT_PATHS,
    MANIFEST,
    README,
    ROOT,
    RUNNER,
    SELF_NORMALIZED_FIELDS,
    PhaseA7Error,
    normalized_freeze_view,
    sha256_file,
    validate,
    validate_makefile_contract,
    validate_readme_contract,
    validate_runner_contract,
    validate_scoped_receipt,
)


class PhaseA7ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(MANIFEST.read_text())
        cls.readme = README.read_text()
        cls.runner = RUNNER.read_text()
        cls.makefile = (ROOT / "Makefile").read_text()

    @staticmethod
    def live_receipt_lines() -> list[str]:
        return [
            f"{sha256_file(ROOT / relative)}  {relative}"
            for relative in EXPECTED_RECEIPT_PATHS
        ]

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(PhaseA7Error):
            validate(
                candidate,
                verify_freeze=False,
                verify_environment=False,
            )

    def test_blueprint_passes_structural_contract(self) -> None:
        validate(
            copy.deepcopy(self.original),
            verify_freeze=False,
            verify_environment=False,
        )

    def test_release_rejects_a_reintroduced_hash_placeholder(self) -> None:
        candidate = copy.deepcopy(self.original)
        candidate["hash_freeze"][
            "precision_ownership_manifest_sha256"
        ] = "PLACEHOLDER"
        with self.assertRaisesRegex(PhaseA7Error, "unfrozen hash field"):
            validate(candidate, verify_environment=False)

    def test_normalized_freeze_view_resets_exact_three_fields(self) -> None:
        candidate = copy.deepcopy(self.original)
        for index, field in enumerate(SELF_NORMALIZED_FIELDS):
            candidate["hash_freeze"][field] = f"{index + 1:064x}"
        before = copy.deepcopy(candidate)
        normalized = normalized_freeze_view(candidate)
        self.assertEqual(candidate, before)
        for field in SELF_NORMALIZED_FIELDS:
            self.assertEqual(
                normalized["hash_freeze"][field],
                "PLACEHOLDER",
            )

    def test_readme_passes_static_contract(self) -> None:
        validate_readme_contract(self.readme)

    def test_runner_is_exact_python_only_gate(self) -> None:
        validate_runner_contract(self.runner)

    def test_makefile_passes_exact_isolated_delta(self) -> None:
        validate_makefile_contract(self.makefile)

    def test_synthetic_live_scoped_receipt_passes(self) -> None:
        validate_scoped_receipt("\n".join(self.live_receipt_lines()) + "\n")

    def test_current_frozen_receipt_passes(self) -> None:
        validate_scoped_receipt()

    def test_mutation_status_cannot_claim_implementation(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "implementation_present", True
            )
        )

    def test_mutation_status_cannot_claim_production_route(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "production_route_connected", True
            )
        )

    def test_mutation_status_cannot_claim_transport(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "transport_operator_applications", 1
            )
        )

    def test_mutation_source_baseline_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["hash_freeze"]["source_baseline"].__setitem__(
                "parent_source_count", 23
            )
        )

    def test_mutation_extra_mcgsig_hash_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["hash_freeze"]["source_baseline"][
                "additional_source_sha256"
            ].__setitem__("src/MCGSIG.f", "0" * 64)
        )

    def test_mutation_status_cannot_claim_radial_convergence(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "radial_convergence", "CONVERGED"
            )
        )

    def test_mutation_route_receipt_live_whitelist_cannot_expand(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"]["live_replay_targets"].append(
                "validation/iterative/radial_real64_route.md"
            )
        )

    def test_mutation_online_feedback_cannot_be_removed(self) -> None:
        self.rejected(
            lambda data: data["scientific_scope"].__setitem__(
                "online_radial_feedback_preserved", False
            )
        )

    def test_mutation_relaxation_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["scientific_scope"].__setitem__(
                "relaxation", 0.5
            )
        )

    def test_mutation_empirical_parameter_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["scientific_scope"].__setitem__(
                "new_empirical_parameters", {"alpha": 0.8}
            )
        )

    def test_mutation_locked_branch_cannot_change_kryl(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("kryl", 9)
        )

    def test_mutation_locked_branch_cannot_change_itypec(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("itypec", 1)
        )

    def test_mutation_locked_branch_cannot_enable_mcgfmc(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"][
                "derived_inner_control_flow"
            ].__setitem__("mcgfmc_live", True)
        )

    def test_mutation_locked_branch_cannot_enable_cyclic(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("cyclic", True)
        )

    def test_mutation_locked_maxout_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("maxout", 501)
        )

    def test_mutation_locked_tolerance_bits_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__(
                "solver_tolerance_h2_binary32_bits", "0x348637be"
            )
        )

    def test_mutation_group_tail_order_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"]["group_tail"].__setitem__(
                "ordering", "NGIND(II)=II"
            )
        )

    def test_mutation_nconv_mask_cannot_be_forced_contiguous(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"]["group_tail"].__setitem__(
                "nconv_within_tail", "CONTIGUOUS-ONLY"
            )
        )

    def test_mutation_terminal_rounding_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["route_invariants"].__setitem__(
                "terminal_public_rounding_events", 2
            )
        )

    def test_mutation_real64_lane_cannot_read_type2_back(self) -> None:
        self.rejected(
            lambda data: data["route_invariants"].__setitem__(
                "type2_readback_before_terminal", True
            )
        )

    def test_mutation_complete_graph_cannot_omit_outer_owner(self) -> None:
        self.rejected(
            lambda data: data["complete_call_graph"].remove("FLU2DR64")
        )

    def test_mutation_complete_graph_cannot_omit_source_abi(self) -> None:
        self.rejected(
            lambda data: data["complete_call_graph"].remove("MCGFCS64")
        )

    def test_mutation_complete_graph_cannot_omit_mcgsig(self) -> None:
        self.rejected(
            lambda data: data["complete_call_graph"].remove(
                "MCCGF64 -> MCGSIG and SPOMOC_MCCGF_BEGIN"
            )
        )

    def test_mutation_complete_graph_cannot_omit_mocik3(self) -> None:
        self.rejected(
            lambda data: data["complete_call_graph"].remove("MOCIK3")
        )

    def test_mutation_outer_keyflx_cannot_use_sequence_association(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "outer_keyflx_base1"
            ].__setitem__("actual", "KEYFLX(1,1,1)")
        )

    def test_mutation_tracking_keyflx_requires_integer_record(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_keyflx_trk3"
            ].__setitem__(
                "admission",
                "Require exact record length NREG*NLIN*NFUNL.",
            )
        )

    def test_mutation_rank2_keyflx_cannot_create_pointer_alias(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "stis_aca_keyflx_stis2"
            ].__setitem__("pointer_alias_created", True)
        )

    def test_mutation_pjjind_cannot_reach_mcgfca64(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_pjjind_trk2"
            ]["passed_rank2_to"].append("MCGFCA64")
        )

    def test_mutation_flux_owner_cannot_be_real32(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][0]["owns"][0]["declaration"] = (
                "real(real32), allocatable :: FLUX64(NUNKNO,NGRP,8)"
            )

        self.rejected(mutate)

    def test_mutation_eight_slice_meaning_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][0]["owns"][0]["slots"].__setitem__(
                "8", "temperature change"
            )
        )

    def test_mutation_fixed_source_cannot_be_reread(self) -> None:
        self.rejected(
            lambda data: data["owners"][0]["owns"][3].__setitem__(
                "later_lcm_payload_reads_allowed", True
            )
        )

    def test_mutation_visit_cutoff_counter_cannot_be_int32(self) -> None:
        self.rejected(
            lambda data: data["owners"][0]["owns"][5].__setitem__(
                "kind", "integer(int32)"
            )
        )

    def test_mutation_terminal_print_view_cannot_be_real32(self) -> None:
        self.rejected(
            lambda data: data["owners"][0]["owns"][6].__setitem__(
                "declaration",
                "real(real32), allocatable :: FL_PRINT64(:)",
            )
        )

    def test_mutation_dead_rkeff_downcast_cannot_return(self) -> None:
        self.rejected(
            lambda data: data["owners"][0][
                "terminal_diagnostic_contract"
            ].__setitem__(
                "locked_dead_rkeff_assignment",
                "Execute RKEFF=REAL(AKEFF).",
            )
        )

    def test_mutation_door_qfr_tail_cannot_be_real32(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][1]["owns"][0]["declaration"] = (
                "real(real32), allocatable :: QFR_TAIL64(NUN,NGEFF)"
            )

        self.rejected(mutate)

    def test_mutation_door_diagnostic_fgar_cannot_be_real32(self) -> None:
        self.rejected(
            lambda data: data["owners"][1]["owns"][3].__setitem__(
                "declaration",
                "real(real32), allocatable :: FGAR64(:)",
            )
        )

    def test_mutation_door_failure_cannot_update_parent(self) -> None:
        self.rejected(
            lambda data: data["owners"][1]["tail_contract"].__setitem__(
                "failure_is_atomic_for_parent_state", False
            )
        )

    def test_mutation_door_scatter_cannot_require_mccgf_convergence(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][1]["tail_contract"].__setitem__(
                "mccgf_numerical_convergence_required_for_scatter", True
            )
        )

    def test_mutation_door_inner_cap_cannot_become_scatter_veto(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][1]["tail_contract"].__setitem__(
                "mccgf_or_aca_cap_changes_scatter_rule", True
            )
        )

    def test_mutation_door_npsys_identity_cannot_be_removed(self) -> None:
        self.rejected(
            lambda data: data["owners"][1]["tail_contract"].__setitem__(
                "npsys_is_zero_before_tail_and_identity_on_tail", False
            )
        )

    def test_mutation_funkno_uss_cannot_enter_real64_lane(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"][
                "optional_funkno_uss"
            ].__setitem__("required_length", 1)
        )

    def test_mutation_sc_bundle_cannot_be_real64(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][2]["owns"][0]["declaration"] = (
                "real(real64), allocatable :: "
                "SC_BY_GROUP32(0:NBMIX,1,NGEFF)"
            )

        self.rejected(mutate)

    def test_mutation_mccgf_cannot_borrow_owned_nconv(self) -> None:
        self.rejected(
            lambda data: data["owners"][2]["borrows"].__setitem__(
                2, "NGIND and NCONV group identities"
            )
        )

    def test_mutation_mccgf_diagnostic_temp_cannot_be_omitted(self) -> None:
        self.rejected(
            lambda data: data["owners"][2]["owns"][3][
                "members"
            ].remove("TEMP64")
        )

    def test_mutation_sc_bundle_cannot_use_nani_generalization(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][2]["owns"][0]["declaration"] = (
                "real(real32), allocatable :: "
                "SC_BY_GROUP32(0:NBMIX,NANI,NGEFF)"
            )

        self.rejected(mutate)

    def test_mutation_sc_population_cannot_follow_nconv(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][2]["owns"][0]["population"] = (
                "Copy only active NCONV groups."
            )

        self.rejected(mutate)

    def test_mutation_sc_order_cannot_use_physical_group_as_local_index(
        self,
    ) -> None:
        def mutate(data: dict) -> None:
            data["owners"][2]["owns"][0]["ordering_identity"] = (
                "SC_BY_GROUP32(:,1,NGIND(II)) uses the physical group."
            )

        self.rejected(mutate)

    def test_mutation_sc_cannot_be_gathered_downstream(self) -> None:
        self.rejected(
            lambda data: data["owners"][2].__setitem__(
                "downstream_lcm_sc_reads_allowed", True
            )
        )

    def test_mutation_gmres_cannot_drop_roundtrip_prohibition(self) -> None:
        self.rejected(
            lambda data: data["owners"][4][
                "forbidden_conversions"
            ].pop()
        )

    def test_mutation_mcgflx_cannot_call_prinam_for_real64_state(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][3].__setitem__(
                "diagnostic_contract",
                "Call PRINAM with a REAL32 staging array.",
            )
        )

    def test_mutation_gmres_maxi_cannot_use_flu_maxinr(self) -> None:
        self.rejected(
            lambda data: data["owners"][4]["inherited_controls"].__setitem__(
                "maxi", 740
            )
        )

    def test_mutation_gmres_epsinto_cannot_round_through_real32(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][4]["inherited_controls"].__setitem__(
                "epsinto_chain",
                "EPSINTO32=REAL(ERRTOL64/100.0_real64)",
            )
        )

    def test_mutation_response_cannot_traverse_tracking_twice(self) -> None:
        def mutate(data: dict) -> None:
            data["owners"][5]["ordered_operations"][2] = (
                "Exactly two MCGFCF traversals"
            )

        self.rejected(mutate)

    def test_mutation_response_cannot_use_legacy_spomoc_capture(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][5][
                "audit_capture_contract"
            ].__setitem__("legacy_spomoc_capture_allowed_on_arm", True)
        )

    def test_mutation_kryl_derived_branch_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][5][
                "derived_locked_flags"
            ].__setitem__("rebflg_passed_to_mcgfca64", True)
        )

    def test_mutation_source_assembly_cannot_add_term(self) -> None:
        self.rejected(
            lambda data: data["owners"][6]["writes"].append(
                "A fitted correction source"
            )
        )

    def test_mutation_source_formula_cannot_form_three_term_sum(self) -> None:
        self.rejected(
            lambda data: data["owners"][6].__setitem__(
                "arithmetic_contract",
                "S=QN64+SC32*FI64+SIGAL32*FI64",
            )
        )

    def test_mutation_source_sc_slice_cannot_drop_rank(self) -> None:
        self.rejected(
            lambda data: data["owners"][6]["borrows"].__setitem__(
                2, "SC_BY_GROUP32(:,1,II) as rank-1 SC32"
            )
        )

    def test_mutation_source_must_remain_inout(self) -> None:
        self.rejected(
            lambda data: data["owners"][6].__setitem__(
                "untouched_storage_contract", "SOURCE64 is write-only."
            )
        )

    def test_mutation_aca_cutoff_cannot_be_tuned(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "inherited_cutoff"
            ].__setitem__("change_or_tuning", "TUNED")
        )

    def test_mutation_aca_inactive_lucf_cannot_be_one_element(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "legal_inactive_paca4_storage"
            ]["members"][0].__setitem__("allocation_shape", "(1)")
        )

    def test_mutation_aca_inactive_storage_cannot_enter_arithmetic(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "legal_inactive_paca4_storage"
            ]["members"][1].__setitem__("live_reads_allowed", True)
        )

    def test_mutation_aca_epsaca_cannot_be_promoted_after_real32_division(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][7].__setitem__(
                "control_chain",
                "Promote a binary32 EPSACA after EPSI/100.",
            )
        )

    def test_mutation_aca_active_cf_cannot_use_n1_extent(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "active_paca4_operator_views"
            ]["records"]["CF$MCCG"].__setitem__("length", "N1")
        )

    def test_mutation_mcgpra64_im_cannot_drop_terminal_index(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "mcgpra64_shape_correction"
            ].__setitem__(
                "im_dummy",
                "integer, contiguous, intent(in) :: IM(NLONG)",
            )
        )

    def test_mutation_legacy_mcgpra_cannot_enter_on_arm(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "mcgpra64_shape_correction"
            ].__setitem__("legacy_mcgpra_allowed_on_arm", True)
        )

    def test_mutation_cutoff_guard_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "inherited_cutoff"
            ].__setitem__("guard_count", 3)
        )

    def test_mutation_cutoff_counterfactual_cannot_change_state(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "inherited_cutoff"
            ].__setitem__("counterfactual_may_modify_production_state", True)
        )

    def test_mutation_cutoff_counterfactual_cannot_change_publication(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "inherited_cutoff"
            ].__setitem__("counterfactual_may_modify_publication", True)
        )

    def test_mutation_terminal_mirror_cannot_run_twice(self) -> None:
        self.rejected(
            lambda data: data["owners"][10][
                "compatibility_records"
            ].__setitem__("mirror_passes", 2)
        )

    def test_mutation_cutoff_delta_chain_cannot_omit_level(self) -> None:
        self.rejected(
            lambda data: data[
                "cutoff_counterfactual_aggregation"
            ]["propagation_chain"].remove("MCGMRE64 -> MCGFLX64")
        )

    def test_mutation_cutoff_delta_cannot_reset_below_owner(self) -> None:
        self.rejected(
            lambda data: data[
                "cutoff_counterfactual_aggregation"
            ].__setitem__("reset_below_visit_owner", True)
        )

    def test_mutation_cutoff_leaf_cannot_be_shared_mutable(self) -> None:
        self.rejected(
            lambda data: data[
                "cutoff_counterfactual_aggregation"
            ].__setitem__("shared_mutable_leaf_counter_allowed", True)
        )

    def test_mutation_mcgfcs64_abi_cannot_be_omitted(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"].pop(7)
        )

    def test_mutation_mcgfcs64_abi_cannot_use_real32_state(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][7].__setitem__(
                "qn_fi_and_s", "real(real32), contiguous, rank 1"
            )
        )

    def test_mutation_mcgfcs64_abi_cannot_make_source_write_only(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][7].__setitem__(
                "access", "QN and FI read-only; S write-only"
            )
        )

    def test_mutation_upstream_pjjind_abi_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][3].__setitem__(
                "pjjind",
                "integer, contiguous, rank 2, shape (NPJJM,2)",
            )
        )

    def test_mutation_mcgflx_abi_cannot_use_prinam(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][3].__setitem__(
                "iprint_gt5_diagnostic",
                "PRINAM receives a REAL32 adapter.",
            )
        )

    def test_mutation_mcgfl164_abi_cannot_downcast_audit_inputs(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][5].__setitem__(
                "audit_capture",
                "SPOMOC_CAPTURE receives REAL32 QFR and EVAL.",
            )
        )

    def test_mutation_entry_promotion_cannot_repeat(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"].__setitem__("events", 2)
        )

    def test_mutation_initial_flux_record_cannot_change_length(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"]["record_contracts"][
                "initial_flux_group_list"
            ].__setitem__("expected_length", "NUNKNO*NGRP")
        )

    def test_mutation_frozen_dsour_staging_cannot_change(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["entry_promotion"]["record_contracts"][
                "frozen_dsour_with_ipsou"
            ].__setitem__("staging", "REAL32(NUNKNO+1)")
        )

    def test_mutation_dsour_hierarchy_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"]["record_contracts"][
                "frozen_dsour_with_ipsou"
            ].__setitem__("hierarchy", "flat list")
        )

    def test_mutation_zero_nusigf_contract_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"]["record_contracts"][
                "frozen_dsour_with_ipsou"
            ].__setitem__("zero_nusigf", "Allow nonzero NUSIGF.")
        )

    def test_mutation_source_nbs_absence_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"]["record_contracts"][
                "frozen_dsour_with_ipsou"
            ].__setitem__("nbs", "NBS is optional.")
        )

    def test_mutation_locked_itpij_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("itpij", 2)
        )

    def test_mutation_locked_itranc_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("itranc", 0)
        )

    def test_mutation_xdrta2_count_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["route_invariants"].__setitem__(
                "xdrta2_initializations_per_on_visit", 2
            )
        )

    def test_mutation_source_order_cannot_restore_chi_read(self) -> None:
        self.rejected(
            lambda data: data["owners"][0]["source_update_order"][
                "outer_iteration"
            ].__setitem__(
                1,
                "Multiply CHI by zero NUSIGF.",
            )
        )

    def test_mutation_dead_fission_actuals_cannot_return(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][0].__setitem__(
                "dead_fission_actuals",
                "Pass unallocated XSCHI and XSNUF actuals.",
            )
        )

    def test_mutation_offgroup_storage_shape_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][0][
                "off_group_operator_admission"
            ]["storage"].__setitem__(
                "SCAT_OFF32",
                "real(real32) :: SCAT_OFF32(NMAT,NGRP)",
            )
        )

    def test_mutation_offgroup_matcod_cannot_admit_zero(self) -> None:
        self.rejected(
            lambda data: data["owners"][0][
                "off_group_operator_admission"
            ].__setitem__(
                "value_guards",
                "MATCOD values may be zero.",
            )
        )

    def test_mutation_flubal_offgroup_dummy_cannot_change_kind(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][9].__setitem__(
                "offgroup_read_only_dummies",
                "real(real64) :: SCAT_OFF32(NMAT*NGRP,NGRP)",
            )
        )

    def test_mutation_flubal_cannot_reread_offgroup_lcm(self) -> None:
        self.rejected(
            lambda data: data["abi_requirements"][9].__setitem__(
                "later_offgroup_lcm_reads_allowed", True
            )
        )

    def test_mutation_source64_positive_zero_init_cannot_change(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][3]["owns"][0].__setitem__(
                "initialization", "Leave SOURCE64 undefined."
            )
        )

    def test_mutation_response64_per_call_init_cannot_change(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][3]["owns"][1].__setitem__(
                "initialization", "Initialize RESPONSE64 once per visit."
            )
        )

    def test_mutation_funkno_uss_cannot_be_later_ingress(self) -> None:
        self.rejected(
            lambda data: data["entry_promotion"].__setitem__(
                "funkno_uss_policy", "Read optional FUNKNO$USS after entry."
            )
        )

    def test_mutation_type2_mirror_cannot_affect_acceptance(self) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"].__setitem__(
                "type2_conversion_can_affect_acceptance", True
            )
        )

    def test_mutation_type2_conversion_position_cannot_move(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"].__setitem__(
                "type2_conversion_position",
                "Before strict terminal acceptance.",
            )
        )

    def test_mutation_publication_preflight_cannot_drop_finite_check(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"][
                "accepted_publication_preflight"
            ].__setitem__(
                "authoritative_finite_check",
                "Do not check authoritative values.",
            )
        )

    def test_mutation_publication_preflight_cannot_drop_real32_range(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"][
                "accepted_publication_preflight"
            ].__setitem__(
                "compatibility_binary32_finite_range_check",
                "Downcast first and inspect afterward.",
            )
        )

    def test_mutation_publication_preflight_cannot_change_convergence(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"][
                "accepted_publication_preflight"
            ].__setitem__(
                "role",
                "Add a new convergence threshold.",
            )
        )

    def test_mutation_inner_cap_cannot_become_terminal_rejection(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"].__setitem__(
                "inner_solver_cap_is_new_rejection_gate", True
            )
        )

    def test_mutation_strict_terminal_boolean_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["terminal_boundary"].__setitem__(
                "strict_boolean",
                "(EEXT < EPSOUT) AND (EINN < EPSUNK)",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_downcast(self) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][5].__setitem__(
                "locked_action", "KEEP-REAL32-DOWNCAST"
            )
        )

    def test_mutation_conversion_ledger_cannot_round_epsinto(self) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][10].__setitem__(
                "replacement", "Compute EPSINTO in REAL32 and promote it."
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_fgar_downcast(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][6].__setitem__(
                "locked_action",
                "KEEP-REAL32-DIAGNOSTIC",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_temp_downcast(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][7].__setitem__(
                "locked_action",
                "KEEP-IMPLICIT-REAL-TEMP",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_terminal_fl(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][16].__setitem__(
                "locked_action",
                "KEEP-REAL32-FL",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_dead_rkeff(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][17].__setitem__(
                "locked_action",
                "KEEP-DEAD-DOWNCAST",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_prinam(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][18].__setitem__(
                "locked_action",
                "USE-PRINAM-WITH-REAL32-ADAPTER",
            )
        )

    def test_mutation_conversion_ledger_cannot_restore_spomoc_downcast(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["conversion_ledger"][19].__setitem__(
                "locked_action",
                "DOWNCAST-QFR-EVAL",
            )
        )

    def test_mutation_default_route_cannot_be_on(self) -> None:
        self.rejected(
            lambda data: data["default_off_and_fail_closed"].__setitem__(
                "default_enabled", True
            )
        )

    def test_mutation_selected_on_route_cannot_fallback(self) -> None:
        self.rejected(
            lambda data: data["default_off_and_fail_closed"].__setitem__(
                "fallback_after_on_selection", True
            )
        )

    def test_mutation_forbidden_empirical_action_cannot_be_removed(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["forbidden_actions"].pop(6)
        )

    def test_mutation_a8_cannot_claim_complete_lane(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "does_not_prove"
            ].remove("complete continuous REAL64 lane")
        )

    def test_mutation_a8_cannot_drop_paca4_shape_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "PACA=4 inactive explicit-shape formals use conforming "
                "defined storage, and negative compile contracts reject "
                "one-element substitutes."
            )
        )

    def test_mutation_a8_cannot_drop_diagnostic_precision_gate(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "IMPX diagnostics compile with FGAR64 and TEMP64; "
                "negative checks reject REAL32 captures of QFR_TAIL64, "
                "PHIIN_TAIL64 or EPS64 and the warning compares TEMP64 "
                "to EPSI64."
            )
        )

    def test_mutation_a8_cannot_drop_prindm_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "IPRINT>5 diagnostics call PRINDM with REAL64 state; "
                "negative checks reject PRINAM and any REAL32 adapter."
            )
        )

    def test_mutation_a8_cannot_drop_spomoc_capture64_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "MCGFL164 compiles against SPOMOC_CAPTURE64 with four "
                "REAL64 rank-2 inputs; negative checks reject legacy "
                "SPOMOC_CAPTURE or REAL32 QFR/EVAL actuals."
            )
        )

    def test_mutation_a9_cannot_omit_flubal(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A9"][
                "required_nodes"
            ].remove("FLUBAL64 and ALSBD")
        )

    def test_mutation_a9_cannot_drop_visit_cutoff_aggregation(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A9"][
                "required_checks"
            ].remove(
                "CUTOFF_ACTIVE_VISIT64 is initialized once and every "
                "normally returned DOORFV64 delta is added exactly once."
            )
        )

    def test_mutation_a9_cannot_drop_terminal_diagnostic_gate(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A9"][
                "required_checks"
            ].remove(
                "IPRT diagnostics compile with FL_PRINT64 or a direct "
                "REAL64 indexed view; negative checks reject a REAL32 FL "
                "capture, and the locked ITYPEC=0 route contains no "
                "RKEFF=REAL(AKEFF) assignment."
            )
        )

    def test_mutation_a9_cannot_drop_spomoc_capture64_implementation(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A9"][
                "required_checks"
            ].remove(
                "SPOMOC_CAPTURE64 preserves the legacy audit admission/"
                "finite checks, writes SPOT-M-QFR/EVAL/SRC/RAW directly "
                "as type 4, and cannot change solver state, terminal "
                "acceptance or publication."
            )
        )

    def test_mutation_locked_initfl_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["locked_branch"].__setitem__("initfl", 0)
        )

    def test_mutation_double_precision_identity_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["kind_policy"][
                "legacy_double_precision_identity"
            ].__setitem__(
                "required_relation",
                "kind(0.0d0)/=real64",
            )
        )

    def test_mutation_a8_cannot_drop_double_precision_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "The selected toolchain proves kind(0.0d0)==real64 "
                "before any checked legacy DOUBLE PRECISION kernel, "
                "including PRINDM, is accepted."
            )
        )

    def test_mutation_audit_begin_admission_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["audit_lifecycle"][
                "on_begin_admission"
            ].__setitem__("maxout", 1)
        )

    def test_mutation_audit_hook_order_cannot_change(self) -> None:
        def mutate(data: dict) -> None:
            hooks = data["audit_lifecycle"]["ordered_on_hooks"]
            hooks[0], hooks[1] = hooks[1], hooks[0]

        self.rejected(mutate)

    def test_mutation_audit_cannot_feed_solver(self) -> None:
        self.rejected(
            lambda data: data["audit_lifecycle"].__setitem__(
                "may_feed_solver_branch_state_terminal_or_publication",
                True,
            )
        )

    def test_mutation_response_borrow_set_cannot_drop_keyflx(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][5]["borrows"].remove(
                "KEYFLX_TRK3 as an immutable checked tracking-index view"
            )
        )

    def test_mutation_tracking_keyflx_cannot_map_flat(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_keyflx_trk3"
            ].__setitem__(
                "mapping",
                "C_F_POINTER directly with shape "
                "(NREG*NLIN*NFUNL)",
            )
        )

    def test_mutation_tracking_keyflx_rank_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_keyflx_trk3"
            ].__setitem__("rank", 1)
        )

    def test_mutation_pjjind_admission_cannot_drop_type(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_pjjind_trk2"
            ].__setitem__(
                "admission",
                "Require exact record length 2*NPJJM.",
            )
        )

    def test_mutation_pjjind_lifetime_cannot_escape(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "tracking_pjjind_trk2"
            ].__setitem__("lifetime", "saved across response calls")
        )

    def test_mutation_a8_cannot_drop_keyflx_pjj_rank_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "KEYFLX_BASE1, KEYFLX_TRK3, the direct "
                "KEYFLX_TRK3(:,1,:) rank-2 section and PJJIND_TRK2 "
                "compile with their frozen distinct ranks; sequence "
                "association and flat PJJIND are rejected."
            )
        )

    def test_mutation_rank_bridge_cannot_use_descriptor_abi(self) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "mcgfcf_to_mcgffir_keyflx_rank2"
            ].__setitem__(
                "adapter_dummy",
                "integer :: KEYFLX_TRK3(:,:,:)",
            )
        )

    def test_mutation_rank_bridge_cannot_reuse_legacy_pointer(self) -> None:
        self.rejected(
            lambda data: data["owners"][5][
                "callback_selection"
            ].__setitem__("legacy_mcgffi_template_reused", True)
        )

    def test_mutation_xsi_cannot_use_column_zero(self) -> None:
        self.rejected(
            lambda data: data["owners"][5]["owns"][2][
                "members"
            ][1].__setitem__(
                "actual",
                "Pass XSIXYZ(:,0).",
            )
        )

    def test_mutation_regular_header_extent_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][2][
                "regular_tracking_header_admission"
            ]["required_equalities"].pop()
        )

    def test_mutation_mccgf_record_type_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][2]["owns"][5][
                "record_admission"
            ].__setitem__(
                "NZON$MCCG",
                "length NLONG, GANLIB type 2",
            )
        )

    def test_mutation_mcgsig_record_gate_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][2][
                "mcgsig_record_admission"
            ].__setitem__(
                "IPTRK/ICODE",
                "length at most 6",
            )
        )

    def test_mutation_bc_record_extent_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][5]["owns"][4].__setitem__(
                "mapping",
                "Map BC-REFL+TRAN without LCMLEN.",
            )
        )

    def test_mutation_pjj_record_type_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][5][
                "stis_record_admission"
            ].__setitem__("required_ganlib_type", 1)
        )

    def test_mutation_pjjind_value_identity_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][5][
                "discrete_index_value_admission"
            ].__setitem__(
                "PJJIND_TRK2",
                "Accept any in-range pair.",
            )
        )

    def test_mutation_cf_record_type_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "active_paca4_operator_views"
            ]["records"]["CF$MCCG"].__setitem__("ganlib_type", 1)
        )

    def test_mutation_im_record_length_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "active_paca4_operator_views"
            ]["records"]["IM$MCCG"].__setitem__("length", "N1")
        )

    def test_mutation_im_record_type_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "active_paca4_operator_views"
            ]["records"]["IM$MCCG"].__setitem__("ganlib_type", 2)
        )

    def test_mutation_active_record_admission_order_cannot_change(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "active_paca4_operator_views"
            ].__setitem__(
                "admission_order",
                "Map first and inspect later.",
            )
        )

    def test_mutation_diagf_inactive_cannot_enter_mcgabg(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "legal_inactive_paca4_storage"
            ]["members"][1]["passed_to"].append("MCGABG64")
        )

    def test_mutation_inactive_im0_cannot_use_save(self) -> None:
        self.rejected(
            lambda data: data["owners"][7][
                "legal_inactive_paca4_integer_storage"
            ].__setitem__("save_common_or_module_state_allowed", True)
        )

    def test_mutation_a8_cannot_drop_all_active_record_gate(self) -> None:
        self.rejected(
            lambda data: data["phase_split"]["A8"][
                "required_checks"
            ].remove(
                "All nine active PACA=4 records "
                "IM/MCU/PI/JU/DIAGQ/CQ/ILUDF/CF/DIAGF pass exact "
                "LCMLEN type-and-extent admission before mapping to "
                "their frozen one-dimensional views."
            )
        )

    def test_mutation_host_ingress_record_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["host_ingress_and_return_contract"][
                "records_before_payload"
            ].__setitem__(
                "IPTRK/STATE-VECTOR",
                "length 24, GANLIB type 1",
            )
        )

    def test_mutation_host_signature_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["host_ingress_and_return_contract"][
                "records_before_payload"
            ].__setitem__(
                "IPSOU/SIGNATURE",
                "length 3, GANLIB type 3 and exact value L_MACROLIB",
            )
        )

    def test_mutation_b2_heterogeneity_ingress_cannot_be_enabled(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["host_ingress_and_return_contract"][
                "records_before_payload"
            ].__setitem__(
                "IPFLUX/B2  HETE",
                "length 8, GANLIB type 2",
            )
        )

    def test_mutation_tracking_title_contract_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["host_ingress_and_return_contract"][
                "records_before_payload"
            ].__setitem__(
                "IPTRK/TITLE",
                "unchecked diagnostic text",
            )
        )

    def test_mutation_norm_fs_ingress_cannot_be_enabled(self) -> None:
        self.rejected(
            lambda data: data["host_ingress_and_return_contract"][
                "records_before_payload"
            ].__setitem__(
                "IPSOU/NORM-FS",
                "length 1, GANLIB type 2",
            )
        )

    def test_mutation_flugpi_cannot_parse_twice(self) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "selection_mechanism",
                "Parse once for legacy controls and again for R64.",
            )
        )

    def test_mutation_r64_selector_cannot_alias_moca(self) -> None:
        self.rejected(
            lambda data: data["default_off_and_fail_closed"][
                "selection_authority"
            ].__setitem__(
                "audit_control_relation",
                "MOCA enables the REAL64 route.",
            )
        )

    def test_mutation_r64_selector_cannot_use_saved_state(self) -> None:
        self.rejected(
            lambda data: data["default_off_and_fail_closed"][
                "selection_authority"
            ].__setitem__(
                "storage_and_lifetime",
                "SAVE across FLU calls.",
            )
        )

    def test_mutation_off_identity_requirement_cannot_be_dropped(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["default_off_and_fail_closed"].__setitem__(
                "legacy_off_identity_requirement",
                "Only compare final keff.",
            )
        )

    def test_mutation_keyflx_host_rank_owner_cannot_flatten(
        self,
    ) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "keyflx_rank_owner",
                "FLU allocates flat KEYFLX_HOST1.",
            )
        )

    def test_mutation_region_identity_cannot_drop_bitwise_volume(
        self,
    ) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "region_identity",
                "MATCOD and VOLUME are not cross-checked.",
            )
        )

    def test_mutation_leak1d_cannot_feed_solver(self) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "leak1d_staging",
                "LEAK1D_INPUT32 is a solver source.",
            )
        )

    def test_mutation_layered_success_status_cannot_collapse(
        self,
    ) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "return_status",
                "One Boolean is true before all outer writes.",
            )
        )

    def test_mutation_a7_cannot_claim_failure_atomicity(self) -> None:
        def mutate(data: dict) -> None:
            items = data["a7_can_establish"]
            index = items.index(
                "Default-off, no-fallback, pre-acceptance write gating "
                "and the limited post-acceptance failure scope are "
                "explicit."
            )
            items[index] = (
                "Default-off, no-fallback and failure-atomicity rules "
                "are explicit."
            )

        self.rejected(mutate)

    def test_mutation_cutoff_observation_cannot_narrow_to_int32(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["owners"][0]["owns"][5].__setitem__(
                "observation",
                "Print CUTOFF_ACTIVE_VISIT64 through an int32 temporary.",
            )
        )

    def test_mutation_host_failure_cannot_write_metadata(self) -> None:
        self.rejected(
            lambda data: data[
                "host_ingress_and_return_contract"
            ].__setitem__(
                "authoritative_compatibility_or_host_metadata_mutation_before_success",
                True,
            )
        )

    def test_mutation_preterminal_publication_cannot_be_allowed(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["publication_lexical_gate"].__setitem__(
                "static_negative_gate",
                "Allow preterminal SOUR creation.",
            )
        )

    def test_mutation_spomoc_diagnostic_cannot_become_authority(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["publication_lexical_gate"].__setitem__(
                "diagnostic_exception",
                "SPOT-MOC-AUD is scientific authority.",
            )
        )

    def test_mutation_flubal_direct_section_cannot_use_element(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "flubal64_outer_sections"
            ].__setitem__("mutable_flux", "FLUX64(1,1,7)")
        )

    def test_mutation_flu2ac_direct_section_cannot_use_element(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["rank_shape_adapters"][
                "flu2ac64_history_sections"
            ].__setitem__("inner_flux", "FLUX64(1,1,5)")
        )

    def test_mutation_route_receipt_freeze_commit_cannot_change(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"].__setitem__(
                "receipt_freeze_commit",
                "0" * 40,
            )
        )

    def test_mutation_route_receipt_must_replay_all_history(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"].__setitem__(
                "historical_replay_all_entries",
                False,
            )
        )

    def test_mutation_evolved_docs_cannot_be_live_authority(
        self,
    ) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"].__setitem__(
                "evolved_documents_are_not_live_hash_authorities",
                False,
            )
        )

    def test_mutation_a6_receipt_must_replay_live(self) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["phase_a6"].__setitem__(
                "live_replay_all_entries",
                False,
            )
        )

    def test_mutation_evolved_doc_whitelist_cannot_shrink(self) -> None:
        self.rejected(
            lambda data: data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"]["evolved_document_targets"].pop()
        )

    def test_mutation_evolved_doc_whitelist_cannot_reorder(self) -> None:
        def mutate(data: dict) -> None:
            targets = data["hash_freeze"][
                "upstream_receipt_validation"
            ]["radial_route"]["evolved_document_targets"]
            targets[0], targets[1] = targets[1], targets[0]

        self.rejected(mutate)

    def test_mutation_runtime_preflight_cannot_apply_transport(self) -> None:
        self.rejected(
            lambda data: data["later_runtime_sequence"][0].__setitem__(
                "transport_applications", 1
            )
        )

    def test_runner_mutation_cannot_add_compiler(self) -> None:
        with self.assertRaises(PhaseA7Error):
            validate_runner_contract(self.runner + "\ngfortran -c unsafe.f90\n")

    def test_runner_mutation_cannot_add_dragon(self) -> None:
        with self.assertRaises(PhaseA7Error):
            validate_runner_contract(self.runner + "\nrdragon unsafe.x2m\n")

    def test_runner_mutation_cannot_skip_receipt(self) -> None:
        receipt_block = (
            "(\n"
            "  cd \"$ROOT\"\n"
            "  shasum -a 256 -c \"$RECEIPT\" >/dev/null\n"
            ")\n"
            "echo \"SPOR64 PHASE-A7 RECEIPT PASS\"\n\n"
        )
        with self.assertRaises(PhaseA7Error):
            validate_runner_contract(
                self.runner.replace(receipt_block, "", 1)
            )

    def test_makefile_mutation_cannot_add_prerequisite(self) -> None:
        mutated = self.makefile.replace(
            "spot-real64-phase-a7 :",
            "spot-real64-phase-a7 : spot-real64-phase-a6",
            1,
        )
        with self.assertRaises(PhaseA7Error):
            validate_makefile_contract(mutated)

    def test_makefile_mutation_cannot_join_default_all(self) -> None:
        mutated = self.makefile.replace(
            "all :",
            "all : spot-real64-phase-a7",
            1,
        )
        with self.assertRaises(PhaseA7Error):
            validate_makefile_contract(mutated)

    def test_makefile_mutation_cannot_add_recipe(self) -> None:
        recipe = (
            "\tsh validation/iterative/real64_phase_a7/run_phase_a7.sh"
        )
        mutated = self.makefile.replace(
            recipe,
            recipe + "\n\tsh validation/iterative/real64_phase_a6/"
            "run_phase_a6.sh",
            1,
        )
        with self.assertRaises(PhaseA7Error):
            validate_makefile_contract(mutated)

    def test_receipt_mutation_cannot_omit_path(self) -> None:
        lines = self.live_receipt_lines()
        with self.assertRaises(PhaseA7Error):
            validate_scoped_receipt(
                "\n".join(lines[:-1]) + "\n",
                verify_hashes=False,
            )

    def test_receipt_mutation_cannot_reorder_paths(self) -> None:
        lines = self.live_receipt_lines()
        lines[0], lines[1] = lines[1], lines[0]
        with self.assertRaises(PhaseA7Error):
            validate_scoped_receipt(
                "\n".join(lines) + "\n",
                verify_hashes=False,
            )

    def test_receipt_mutation_cannot_duplicate_path(self) -> None:
        lines = self.live_receipt_lines()
        lines.insert(1, lines[0])
        with self.assertRaises(PhaseA7Error):
            validate_scoped_receipt(
                "\n".join(lines) + "\n",
                verify_hashes=False,
            )

    def test_receipt_mutation_cannot_use_wrong_hash(self) -> None:
        lines = self.live_receipt_lines()
        _, relative = lines[0].split("  ", 1)
        lines[0] = f"{'0' * 64}  {relative}"
        with self.assertRaises(PhaseA7Error):
            validate_scoped_receipt("\n".join(lines) + "\n")

    def test_receipt_mutation_cannot_hash_itself(self) -> None:
        lines = self.live_receipt_lines()
        lines.append(
            f"{'0' * 64}  validation/iterative/real64_phase_a7/"
            "phase_a7_implementation_receipt.sha256"
        )
        with self.assertRaises(PhaseA7Error):
            validate_scoped_receipt(
                "\n".join(lines) + "\n",
                verify_hashes=False,
            )

    def test_readme_mutation_cannot_claim_convergence(self) -> None:
        mutated = self.readme.replace(
            "RADIAL-CONVERGENCE=NOT-EVALUATED",
            "RADIAL-CONVERGENCE=CONVERGED",
            1,
        )
        with self.assertRaises(PhaseA7Error):
            validate_readme_contract(mutated)


if __name__ == "__main__":
    unittest.main()

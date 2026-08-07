#!/usr/bin/env python3
"""Targeted mutation regressions for the B2s static bridge contract."""

from __future__ import annotations

import copy
import unittest

from check_phase_a9b_b2s_immediate_host_bridge import (
    GateError,
    check_all,
    check_manifest,
    check_source,
    load_manifest,
    load_source,
)


class ImmediateHostBridgeMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = load_source()
        cls.manifest = load_manifest()

    @staticmethod
    def changed(text: str, old: str, new: str, count: int = 1) -> str:
        actual = text.count(old)
        if actual < count:
            raise AssertionError(
                f"mutation anchor missing: {old!r}; found {actual}"
            )
        return text.replace(old, new, count)

    def reject_manifest(self, path: tuple[str, ...], value: object) -> None:
        manifest = copy.deepcopy(self.manifest)
        owner = manifest
        for key in path[:-1]:
            owner = owner[key]
        owner[path[-1]] = value
        with self.assertRaises(GateError):
            check_manifest(manifest)

    def reject_source(self, old: str, new: str, count: int = 1) -> None:
        source = self.changed(self.source, old, new, count)
        with self.assertRaises(GateError):
            check_source(source)

    def test_01_current_contract(self) -> None:
        check_all(self.source, self.manifest)

    # 27 manifest mutations.
    def test_02_parent_commit_change_rejected(self) -> None:
        self.reject_manifest(("parent_commit",), "0" * 40)

    def test_03_parent_receipt_change_rejected(self) -> None:
        self.reject_manifest(("parent_receipt_sha256",), "0" * 64)

    def test_04_api_argument_change_rejected(self) -> None:
        self.reject_manifest(
            ("api", "arguments"),
            ["ipout", "ipassembled", "ipsolved(3)", "enable(optional)"],
        )

    def test_05_external_solved_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_solved_objects"), True)

    def test_06_external_plane_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_plane"), True)

    def test_07_external_rho_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_rho"), True)

    def test_08_external_tolerance_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_tolerance"), True)

    def test_09_nonoptional_enable_rejected(self) -> None:
        self.reject_manifest(("default_off", "enable_is_optional"), False)

    def test_10_absent_enable_execution_rejected(self) -> None:
        self.reject_manifest(
            ("default_off", "absent_enable_returns_disabled"), False
        )

    def test_11_source_plane_set_change_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "source_plane_labels"), [1, 1, 3]
        )

    def test_12_same_slot_pairing_change_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "same_slot_macro_source_pairing"),
            False,
        )

    def test_13_nonfresh_output_permission_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "output_must_be_fresh"), False
        )

    def test_14_input_mutation_permission_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "all_caller_objects_immutable"),
            False,
        )

    def test_15_b2o_call_count_change_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "b2o_calls"), 2)

    def test_16_radial_before_all_seals_rejected(self) -> None:
        self.reject_manifest(
            ("causal_chain", "all_b2o_calls_before_first_b2b"), False
        )

    def test_17_sealed_plane_set_change_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "sealed_plane_set"), [0, 1, 2])

    def test_18_noncanonical_b2b_order_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "b2b_order"), [3, 2, 1])

    def test_19_b2b_call_count_change_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "b2b_calls"), 2)

    def test_20_noncont_mode_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "b2b_mode"), "BOOT")

    def test_21_noncommitted_success_token_rejected(self) -> None:
        self.reject_manifest(
            ("causal_chain", "b2b_only_success_status"), "CORE_OK"
        )

    def test_22_b2r_call_count_change_rejected(self) -> None:
        self.reject_manifest(("causal_chain", "b2r_calls"), 2)

    def test_23_early_collection_permission_rejected(self) -> None:
        self.reject_manifest(
            ("causal_chain", "b2r_after_all_three_host_commits"), False
        )

    def test_24_cutoff_acceptance_role_rejected(self) -> None:
        self.reject_manifest(("cutoff_diagnostic", "feeds_acceptance"), True)

    def test_25_cutoff_aggregation_rejected(self) -> None:
        self.reject_manifest(("cutoff_diagnostic", "aggregated"), True)

    def test_26_empirical_parameter_rejected(self) -> None:
        self.reject_manifest(
            ("numerical_controls", "new_empirical_parameters"), 1
        )

    def test_27_macro_history_overclaim_rejected(self) -> None:
        self.reject_manifest(
            (
                "provenance_scope",
                "macro0_historically_derived_from_archive_microlib2",
            ),
            True,
        )

    def test_28_true_transport_execution_claim_rejected(self) -> None:
        self.reject_manifest(("short_gate_design", "true_transport_solves"), 1)

    # 18 source mutations.  Together with the 27 above: 45 mutations.
    def test_29_module_name_change_rejected(self) -> None:
        self.reject_source("module SPOR64_B2S", "module SPOR64_B2X")

    def test_30_disabled_status_change_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2S_DISABLED = 0", "SPOR64_B2S_DISABLED = 9"
        )

    def test_31_external_solved_argument_rejected(self) -> None:
        self.reject_source(
            "ipsources,iptrack_file,status,cutoff_by_plane,enable)",
            "ipsources,ipsolved,iptrack_file,status,cutoff_by_plane,enable)",
        )

    def test_32_nonoptional_source_enable_rejected(self) -> None:
        self.reject_source(
            "logical, intent(in), optional :: enable",
            "logical, intent(in) :: enable",
        )

    def test_33_missing_absent_enable_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. present(enable)) return",
            "if (.not. present(enable)) continue",
        )

    def test_34_missing_false_enable_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. enable) return", "if (.not. enable) continue"
        )

    def test_35_object_access_before_enable_rejected(self) -> None:
        anchor = "cutoff_by_plane = 0_int64"
        self.reject_source(
            anchor,
            anchor + "\n    if (c_associated(ipout)) continue",
        )

    def test_36_scratch_before_enable_rejected(self) -> None:
        anchor = "cutoff_by_plane = 0_int64"
        self.reject_source(
            anchor,
            anchor + "\n    call OPEN_PRIVATE(solved_by_plane(1),'BAD',1)",
        )

    def test_37_wrong_source_sent_to_b2o_rejected(self) -> None:
        self.reject_source(
            "call SPOR64_B2O_SEAL_CONT_PAIR(ipassembled,ipsources(slot), &",
            "call SPOR64_B2O_SEAL_CONT_PAIR(ipassembled,ipsources(1), &",
        )

    def test_38_hardcoded_sealed_plane_rejected(self) -> None:
        self.reject_source("plane = source_plane(slot)", "plane = 1")

    def test_39_duplicate_plane_acceptance_rejected(self) -> None:
        self.reject_source(
            "if (slot_for_plane(plane) /= 0) then", "if (.false.) then"
        )

    def test_40_missing_plane_omission_gate_rejected(self) -> None:
        self.reject_source(
            "if (any(slot_for_plane == 0)) then", "if (.false.) then"
        )

    def test_41_noncanonical_plane_loop_rejected(self) -> None:
        self.reject_source(
            "do plane = 1, NSNAP\n      slot = slot_for_plane(plane)",
            "do plane = NSNAP, 1, -1\n      slot = slot_for_plane(plane)",
        )

    def test_42_wrong_slot_macro_rejected(self) -> None:
        self.reject_source(
            "LCM_STORAGE_KIND(ipmacros(slot))",
            "LCM_STORAGE_KIND(ipmacros(plane))",
        )

    def test_43_wrong_slot_source_rejected(self) -> None:
        self.reject_source(
            "iptrack_file,sealed_system(slot),ipsources(slot),sealed_seed(slot)]",
            "iptrack_file,sealed_system(slot),ipsources(plane),sealed_seed(slot)]",
        )

    def test_44_boot_route_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2B_CONT,radial_status, &",
            "SPOR64_B2B_BOOT,radial_status, &",
        )

    def test_45_noncommitted_radial_status_rejected(self) -> None:
        self.reject_source(
            "radial_status /= SPOR64_B2C_HOST_COMMITTED",
            "radial_status /= SPOR64_B2S_RETURNED",
        )

    def test_46_noncausal_collector_input_rejected(self) -> None:
        self.reject_source(
            "call SPOR64_B2R_COLLECT(ipout,ipassembled,solved_by_plane, &",
            "call SPOR64_B2R_COLLECT(ipout,ipassembled,sealed_seed, &",
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Mutation regressions for the B2r returned-archive static contract."""

from __future__ import annotations

import copy
import unittest

from check_phase_a9b_b2r_returned_archive import (
    GateError,
    check_all,
    check_manifest,
    check_source,
    load_manifest,
    load_source,
)


class ReturnedArchiveMutationTests(unittest.TestCase):
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

    def test_02_parent_commit_change_rejected(self) -> None:
        self.reject_manifest(("parent_commit",), "0" * 40)

    def test_03_parent_receipt_change_rejected(self) -> None:
        self.reject_manifest(("parent_receipt_sha256",), "0" * 64)

    def test_04_api_argument_change_rejected(self) -> None:
        self.reject_manifest(
            ("api", "arguments"),
            ["ipout", "ipassembled", "ipsolved(3)", "status"],
        )

    def test_05_loose_scalar_permission_rejected(self) -> None:
        self.reject_manifest(
            ("api", "loose_plane_rho_k_epoch_arguments"), True
        )

    def test_06_solved_plane_set_change_rejected(self) -> None:
        self.reject_manifest(
            ("input_contract", "solved_plane_labels"), [1, 2, 2]
        )

    def test_07_source_plane_set_change_rejected(self) -> None:
        self.reject_manifest(
            ("input_contract", "qsource_plane_labels"), [0, 1, 2]
        )

    def test_08_argument_order_binding_rejected(self) -> None:
        self.reject_manifest(
            ("input_contract", "bind_by_label_not_argument_order"), False
        )

    def test_09_duplicate_acceptance_rejected(self) -> None:
        self.reject_manifest(("input_contract", "reject_duplicates"), False)

    def test_10_omission_acceptance_rejected(self) -> None:
        self.reject_manifest(("input_contract", "reject_omissions"), False)

    def test_11_nonfresh_output_permission_rejected(self) -> None:
        self.reject_manifest(
            ("input_contract", "output_must_be_fresh"), False
        )

    def test_12_input_mutation_permission_rejected(self) -> None:
        self.reject_manifest(("input_contract", "all_inputs_immutable"), False)

    def test_13_rho_tolerance_contract_rejected(self) -> None:
        self.reject_manifest(
            ("same_index_binding", "rho"), "RHO values are close enough"
        )

    def test_14_epoch_change_rejected(self) -> None:
        self.reject_manifest(
            ("same_index_binding", "epoch"), "matching epochs"
        )

    def test_15_source_k_binding_change_rejected(self) -> None:
        self.reject_manifest(
            ("same_index_binding", "k"), "derive K from terminal SOUR"
        )

    def test_16_qfiss_authority_change_rejected(self) -> None:
        self.reject_manifest(
            ("same_index_binding", "qfiss"), "terminal SOUR is authoritative"
        )

    def test_17_root_k_inventory_rejected(self) -> None:
        inventory = list(self.manifest["output_contract"]["root_inventory"])
        inventory.insert(2, "SPOT-ITER-K")
        self.reject_manifest(("output_contract", "root_inventory"), inventory)

    def test_18_closed_root_state_rejected(self) -> None:
        self.reject_manifest(("output_contract", "root_state"), "CLOSED")

    def test_19_root_rho_rejected(self) -> None:
        self.reject_manifest(("output_contract", "root_has_rho"), True)

    def test_20_root_iter_k_rejected(self) -> None:
        self.reject_manifest(
            ("output_contract", "root_has_spot_iter_k"), True
        )

    def test_21_drop_authoritative_qfiss_rejected(self) -> None:
        inventory = list(
            self.manifest["output_contract"]["child_authority_inventory"]
        )
        inventory.remove("QFISS")
        self.reject_manifest(
            ("output_contract", "child_authority_inventory"), inventory
        )

    def test_22_duplicate_child_plane_owner_rejected(self) -> None:
        self.reject_manifest(("output_contract", "child_has_plane"), True)

    def test_23_fixed_source_marker_change_rejected(self) -> None:
        self.reject_manifest(("output_contract", "fixed_source_marker"), 0)

    def test_24_sour_substitution_rejected(self) -> None:
        self.reject_manifest(("source_roles", "SOUR_may_replace_QFISS"), True)

    def test_25_accidental_inequality_gate_rejected(self) -> None:
        self.reject_manifest(
            ("source_roles", "numerical_inequality_is_required"), True
        )

    def test_26_closed_output_claim_rejected(self) -> None:
        self.reject_manifest(("lifecycle", "output_is_closed"), True)

    def test_27_ax_next_binding_rejected(self) -> None:
        self.reject_manifest(("lifecycle", "binds_ax_next"), True)

    def test_28_rho1_publication_rejected(self) -> None:
        self.reject_manifest(("lifecycle", "publishes_rho_1"), True)

    def test_29_k1_publication_rejected(self) -> None:
        self.reject_manifest(("lifecycle", "publishes_k_1"), True)

    def test_30_historical_derivation_overclaim_rejected(self) -> None:
        self.reject_manifest(
            (
                "provenance_scope",
                "historical_derivation_proved_from_detached_bits_alone",
            ),
            True,
        )

    def test_31_metadata_only_provenance_rejected(self) -> None:
        self.reject_manifest(
            (
                "provenance_scope",
                "matching_plane_rho_epoch_alone_is_sufficient",
            ),
            True,
        )

    def test_32_transport_execution_rejected(self) -> None:
        self.reject_manifest(("execution_scope", "transport_solves"), 1)

    def test_33_picard_execution_rejected(self) -> None:
        self.reject_manifest(("execution_scope", "picard_maps"), 1)

    def test_34_missing_closed_nonclaim_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["not_claimed"].remove("a CLOSED/1 archive")
        with self.assertRaises(GateError):
            check_manifest(manifest)

    def test_35_empirical_controls_rejected(self) -> None:
        self.reject_manifest(("empirical_controls_added",), True)

    def test_36_module_name_change_rejected(self) -> None:
        self.reject_source("module SPOR64_B2R", "module SPOR64_B2X")

    def test_37_preflight_status_change_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2R_PREFLIGHT_FAILED = 1",
            "SPOR64_B2R_PREFLIGHT_FAILED = 0",
        )

    def test_38_returned_status_change_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2R_RETURNED = 2", "SPOR64_B2R_RETURNED = 3"
        )

    def test_39_add_loose_rho_argument_rejected(self) -> None:
        self.reject_source(
            "ipsolved,ipsources,status)",
            "ipsolved,ipsources,rho64,status)",
        )

    def test_40_plane_count_change_rejected(self) -> None:
        self.reject_source("NSNAP = 3", "NSNAP = 4")

    def test_41_remove_fresh_output_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. EMPTY_LCM_ROOT(ipout)) return", "continue"
        )

    def test_42_accept_nonassembled_parent_rejected(self) -> None:
        self.reject_source("'ASSEMBLED')) return", "'PROJECTED')) return")

    def test_43_accept_nonsolved_child_rejected(self) -> None:
        self.reject_source("'SOLVED')) return", "'PROJECTED')) return")

    def test_44_accept_nonfrozen_source_rejected(self) -> None:
        self.reject_source("'FROZEN-QFIS')) return", "'SOLVED')) return")

    def test_45_hardcode_solved_plane_rejected(self) -> None:
        self.reject_source(
            "plane = solved_plane(slot)",
            "plane = 1",
        )

    def test_46_hardcode_source_plane_rejected(self) -> None:
        self.reject_source(
            "plane = source_plane(slot)",
            "plane = 1",
        )

    def test_47_stop_label_reordering_rejected(self) -> None:
        self.reject_source(
            "solved_slot(plane) = slot",
            "solved_slot(slot) = slot",
        )

    def test_48_wrong_system_index_rejected(self) -> None:
        self.reject_source(
            "if (found_plane /= plane) return",
            "if (found_plane /= 1) return",
        )

    def test_49_remove_key_binding_rejected(self) -> None:
        self.reject_source(
            "if (any(solved_key(:,slot) /= track_key(:,plane))) return",
            "continue",
        )

    def test_50_remove_leakage_binding_rejected(self) -> None:
        self.reject_source(
            "SAME_REAL32_BITS(solved_leak(:,slot), &\n"
            "          system_leak(:,plane))",
            ".true.",
        )

    def test_51_change_reciprocal_rejected(self) -> None:
        self.reject_source(
            "1.0_real64/iter_keff64", "2.0_real64/iter_keff64"
        )

    def test_52_change_k_conversion_rejected(self) -> None:
        self.reject_source(
            "real(iter_keff,real32)", "real(rho,real32)"
        )

    def test_53_use_sour_as_qfiss_rejected(self) -> None:
        self.reject_source(
            "authority_qfiss = LCMGID(authority,'QFISS')",
            "authority_qfiss = LCMGID(authority,'SOUR')",
        )

    def test_54_drop_plane_deletion_rejected(self) -> None:
        self.reject_source(
            "call LCMDEL(output_authority,'PLANE')", "continue"
        )

    def test_55_publish_closed_root_rejected(self) -> None:
        self.reject_source(
            "lifecycle_state = 'RETURNED'", "lifecycle_state = 'CLOSED'"
        )

    def test_56_publish_root_rho_rejected(self) -> None:
        anchor = "root_authority = LCMDID(ipout,'SPOT-R64')"
        self.reject_source(
            anchor,
            anchor + "\n    call LCMPUT(root_authority,'RHO',1,4,root_rho64)",
        )

    def test_57_publish_root_k_rejected(self) -> None:
        anchor = "call LCMPTC(ipout,'SIGNATURE',12,signature)"
        self.reject_source(
            anchor,
            anchor + "\n    call LCMPUT(ipout,'SPOT-ITER-K',1,4,iter_keff64)",
        )

    def test_58_add_return_after_first_write_rejected(self) -> None:
        anchor = "call LCMPTC(ipout,'SIGNATURE',12,signature)"
        self.reject_source(anchor, anchor + "\n    if (.true.) return")

    def test_59_root_epoch_not_final_rejected(self) -> None:
        anchor = (
            "call LCMPUT(root_authority,'EPOCH',1,1,root_epoch)"
        )
        self.reject_source(
            anchor,
            anchor + "\n    call LCMPUT(ipout,'LATE-WRITE',1,1,root_planes)",
        )

    def test_60_output_qfiss_precision_change_rejected(self) -> None:
        self.reject_source(
            "call LCMPDL(output_qfiss,ip,NUNKNO,4,qfiss64(:,ip,jp))",
            "call LCMPDL(output_qfiss,ip,NUNKNO,2,qmirror32(:,ip,jp))",
        )

    def test_61_missing_track_keyflx_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. RECORD_MATCHES(track,'KEYFLX',NREG,1)) return",
            "continue",
        )

    def test_62_track_key_map_divergence_rejected(self) -> None:
        self.reject_source(
            "if (any(keyflx /= keyanis)) return",
            "continue",
        )

    def test_63_prepublication_input_mutator_rejected(self) -> None:
        anchor = "if (.not. ASSEMBLED_ROOT_IS_EXACT(ipassembled)) return"
        self.reject_source(
            anchor,
            anchor + "\n    call LCMPUT(ipassembled,'BAD',1,1,root_planes)",
        )

    def test_64_validation_helper_mutator_rejected(self) -> None:
        anchor = "TRACK_IS_VALID = .false."
        self.reject_source(
            anchor,
            anchor + "\n    call LCMPUT(track,'BAD',1,1,keyanis(1))",
        )

    def test_65_empty_inventory_guard_rejected(self) -> None:
        self.reject_source(
            "if (empty .or. object_length /= -1) return",
            "continue",
        )


if __name__ == "__main__":
    unittest.main()

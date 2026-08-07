#!/usr/bin/env python3
"""Targeted mutation regressions for the B2t static ownership contract."""

from __future__ import annotations

import copy
import unittest

from check_phase_a9b_b2t_owned_source_host_step import (
    GateError,
    check_all,
    check_manifest,
    check_source,
    load_manifest,
    load_source,
)


class OwnedSourceHostStepMutationTests(unittest.TestCase):
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

    # 22 manifest mutations.
    def test_02_parent_commit_change_rejected(self) -> None:
        self.reject_manifest(("parent_commit",), "0" * 40)

    def test_03_api_argument_change_rejected(self) -> None:
        self.reject_manifest(
            ("api", "arguments"),
            ["ipout", "ipprojected", "ipsolved(3)", "enable(optional)"],
        )

    def test_04_external_assembled_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_assembled_objects"), True)

    def test_05_external_macro_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_macro0_objects"), True)

    def test_06_external_source_permission_rejected(self) -> None:
        self.reject_manifest(("api", "caller_source_objects"), True)

    def test_07_nonoptional_enable_rejected(self) -> None:
        self.reject_manifest(("default_off", "enable_is_optional"), False)

    def test_08_disabled_object_access_rejected(self) -> None:
        self.reject_manifest(("default_off", "object_accesses_before_return"), 1)

    def test_09_common_projected_parent_change_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "projected"),
            "one arbitrary detached archive",
        )

    def test_10_system_alias_permission_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "systems_pairwise_distinct"), False
        )

    def test_11_nonfresh_output_permission_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "output_must_be_fresh_memory_lcm"),
            False,
        )

    def test_12_b2k_call_count_change_rejected(self) -> None:
        self.reject_manifest(("owned_chain", "b2k_calls"), 2)

    def test_13_b2k_status_change_rejected(self) -> None:
        self.reject_manifest(
            ("owned_chain", "b2k_only_success_status"), "B2K_COMPLETE"
        )

    def test_14_b2n_call_count_change_rejected(self) -> None:
        self.reject_manifest(("owned_chain", "b2n_calls"), 2)

    def test_15_noncanonical_b2n_order_rejected(self) -> None:
        self.reject_manifest(("owned_chain", "b2n_order"), [3, 2, 1])

    def test_16_nonprivate_b2n_outputs_rejected(self) -> None:
        self.reject_manifest(
            ("owned_chain", "b2n_outputs_are_private_same_call_pairs"),
            False,
        )

    def test_17_early_b2s_permission_rejected(self) -> None:
        self.reject_manifest(
            ("owned_chain", "all_b2n_commits_before_b2s"), False
        )

    def test_18_false_b2s_enable_rejected(self) -> None:
        self.reject_manifest(("owned_chain", "b2s_enable_argument"), False)

    def test_19_cleanup_weakening_rejected(self) -> None:
        self.reject_manifest(
            ("owned_chain", "recoverable_failure_cleanup"), False
        )

    def test_20_empirical_parameter_rejected(self) -> None:
        self.reject_manifest(
            ("numerical_controls", "new_empirical_parameters"), 1
        )

    def test_21_cutoff_acceptance_role_rejected(self) -> None:
        self.reject_manifest(("cutoff_diagnostic", "feeds_acceptance"), True)

    def test_22_candidate_asm_history_overclaim_rejected(self) -> None:
        self.reject_manifest(
            (
                "provenance_scope",
                "candidate_systems_historically_from_same_call_asm",
            ),
            True,
        )

    def test_23_track_file_history_overclaim_rejected(self) -> None:
        self.reject_manifest(
            (
                "provenance_scope",
                "track_file_historically_matches_archive_track",
            ),
            True,
        )

    # 23 source mutations.  Four additional manifest mutations follow them.
    def test_24_module_name_change_rejected(self) -> None:
        self.reject_source("module SPOR64_B2T", "module SPOR64_B2X")

    def test_25_disabled_status_change_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2T_DISABLED = 0", "SPOR64_B2T_DISABLED = 9"
        )

    def test_26_external_assembled_argument_rejected(self) -> None:
        self.reject_source(
            "iptrack_file,status,cutoff_by_plane,enable)",
            "ipassembled,iptrack_file,status,cutoff_by_plane,enable)",
        )

    def test_27_nonoptional_source_enable_rejected(self) -> None:
        self.reject_source(
            "logical, intent(in), optional :: enable",
            "logical, intent(in) :: enable",
        )

    def test_28_missing_absent_enable_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. present(enable)) return",
            "if (.not. present(enable)) continue",
        )

    def test_29_missing_false_enable_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. enable) return", "if (.not. enable) continue"
        )

    def test_30_object_access_before_enable_rejected(self) -> None:
        anchor = "cutoff_by_plane = 0_int64"
        self.reject_source(
            anchor,
            anchor + "\n    if (c_associated(ipout)) continue",
        )

    def test_31_subcall_before_enable_rejected(self) -> None:
        anchor = "cutoff_by_plane = 0_int64"
        self.reject_source(
            anchor,
            anchor + "\n    call OPEN_PRIVATE(assembled,'BAD',0)",
        )

    def test_32_output_projected_alias_gate_rejected(self) -> None:
        self.reject_source(
            "if (c_associated(ipout,ipprojected)) return",
            "if (c_associated(ipout,ipprojected)) continue",
        )

    def test_33_system_pair_alias_gate_rejected(self) -> None:
        self.reject_source(
            "if (c_associated(ipsystems(plane),ipsystems(other))) return",
            "if (.false.) return",
        )

    def test_34_freshness_gate_rejected(self) -> None:
        self.reject_source(
            "if (.not. EMPTY_LCM_ROOT(ipout)) return",
            "if (.false.) return",
        )

    def test_35_private_assembled_name_change_rejected(self) -> None:
        self.reject_source(
            "call OPEN_PRIVATE(assembled,'B2T-ASMB',0)",
            "call OPEN_PRIVATE(assembled,'B2T-LOOSE',0)",
        )

    def test_36_wrong_b2k_parent_rejected(self) -> None:
        self.reject_source(
            "call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(assembled,ipprojected, &",
            "call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(assembled,ipsystems(1), &",
        )

    def test_37_nonassembled_b2k_status_rejected(self) -> None:
        self.reject_source(
            "assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED",
            "assemble_status /= SPOR64_B2T_RETURNED",
        )

    def test_38_reverse_b2n_loop_rejected(self) -> None:
        self.reject_source(
            "do plane = 1, NSNAP\n      call SPOR64_B2N_BUILD",
            "do plane = NSNAP, 1, -1\n      call SPOR64_B2N_BUILD",
        )

    def test_39_hardcoded_b2n_plane_rejected(self) -> None:
        self.reject_source(
            "call SPOR64_B2N_BUILD(ipprojected,plane,macros(plane), &",
            "call SPOR64_B2N_BUILD(ipprojected,1,macros(plane), &",
        )

    def test_40_wrong_b2n_macro_slot_rejected(self) -> None:
        self.reject_source(
            "SPOR64_B2N_BUILD(ipprojected,plane,macros(plane), &",
            "SPOR64_B2N_BUILD(ipprojected,plane,macros(1), &",
        )

    def test_41_wrong_b2n_source_slot_rejected(self) -> None:
        self.reject_source(
            "sources(plane),source_status)",
            "sources(1),source_status)",
        )

    def test_42_noncommitted_b2n_status_rejected(self) -> None:
        self.reject_source(
            "source_status /= SPOR64_B2N_COMMITTED",
            "source_status /= SPOR64_B2T_RETURNED",
        )

    def test_43_disabled_b2s_subcall_rejected(self) -> None:
        self.reject_source(
            "iptrack_file,bridge_status,cutoff_by_plane,.true.)",
            "iptrack_file,bridge_status,cutoff_by_plane,.false.)",
        )

    def test_44_missing_b2k_failure_cleanup_rejected(self) -> None:
        self.reject_source(
            "if (assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) then\n"
            "      call CLOSE_PRIVATE(assembled,macros,sources)",
            "if (assemble_status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) then\n"
            "      continue",
        )

    def test_45_missing_b2n_failure_cleanup_rejected(self) -> None:
        self.reject_source(
            "if (source_status /= SPOR64_B2N_COMMITTED) then\n"
            "        call CLOSE_PRIVATE(assembled,macros,sources)",
            "if (source_status /= SPOR64_B2N_COMMITTED) then\n"
            "        continue",
        )

    def test_46_missing_final_cleanup_rejected(self) -> None:
        self.reject_source(
            "if (bridge_status == SPOR64_B2S_RETURNED) &\n"
            "      status = SPOR64_B2T_RETURNED\n"
            "    call CLOSE_PRIVATE(assembled,macros,sources)",
            "if (bridge_status == SPOR64_B2S_RETURNED) &\n"
            "      status = SPOR64_B2T_RETURNED\n"
            "    continue",
        )

    def test_47_track_mode_overclaim_rejected(self) -> None:
        self.reject_manifest(
            ("enabled_input_contract", "track_os_read_only_mode_verified_by_b2t"),
            True,
        )

    def test_48_production_b2n_count_change_rejected(self) -> None:
        self.reject_manifest(("short_gate_design", "production_b2n_builds"), 2)

    def test_49_content_posterior_count_change_rejected(self) -> None:
        self.reject_manifest(("short_gate_design", "content_posterior_runs"), 1)

    def test_50_recursive_macro_check_weakening_rejected(self) -> None:
        self.reject_manifest(
            ("short_gate_design", "unchanged_macro_records_recursive_bitwise"),
            False,
        )


if __name__ == "__main__":
    unittest.main()

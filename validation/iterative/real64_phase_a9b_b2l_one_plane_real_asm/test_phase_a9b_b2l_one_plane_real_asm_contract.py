#!/usr/bin/env python3
"""Mutation checks for the B2l static contract."""

from __future__ import annotations

import unittest

import check_phase_a9b_b2l_one_plane_real_asm as contract


class B2LContractMutationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = contract.DECK.read_text(encoding="utf-8")
        cls.preparer = contract.PREPARER.read_text(encoding="utf-8")
        cls.posterior = contract.POSTERIOR.read_text(encoding="utf-8")
        cls.bounded = contract.BOUNDED.read_text(encoding="utf-8")
        cls.b2j = contract.B2J.read_text(encoding="utf-8")
        cls.runner = contract.RUNNER.read_text(encoding="utf-8")
        cls.xsm_harness = contract.XSM_HARNESS.read_text(encoding="utf-8")

    def rejected(self, function, text: str) -> None:
        with self.assertRaises(SystemExit):
            function(text)

    def replaced_after(
        self, text: str, marker: str, old: str, new: str
    ) -> str:
        before,after = text.split(marker,1)
        self.assertIn(old,after)
        return before + marker + after.replace(old,new,1)

    def test_baseline(self) -> None:
        contract.check_deck(self.deck)
        contract.check_preparer(self.preparer)
        contract.check_posterior(self.posterior)
        contract.check_bounded(self.bounded)
        contract.check_b2j_target(self.b2j)
        contract.check_xsm_harness(self.xsm_harness)
        contract.check_runner(self.runner)

    def test_second_asm_rejected(self) -> None:
        self.rejected(contract.check_deck, self.deck.replace(
            "SYSTEM_OUT := SYSTEM ;", "SYSTEM_OUT := SYSTEM ;\nSYSTEM := ASM: ;"
        ))

    def test_plane_two_rejected(self) -> None:
        self.rejected(contract.check_deck,self.deck.replace("LK1D 1","LK1D 2"))

    def test_flu_rejected(self) -> None:
        self.rejected(contract.check_deck,self.deck.replace(
            "MODULE RECOVER: ASM: DELETE: END: ;",
            "MODULE RECOVER: ASM: FLU: DELETE: END: ;",
        ))

    def test_spor64k_rejected(self) -> None:
        self.rejected(contract.check_deck,self.deck.replace(
            "MODULE RECOVER: ASM: DELETE: END: ;",
            "MODULE RECOVER: ASM: SPOR64K: DELETE: END: ;",
        ))

    def test_loop_rejected(self) -> None:
        self.rejected(contract.check_deck,self.deck + "\nWHILE 1 2 < DO\n")

    def test_wrong_index_recovery_rejected(self) -> None:
        self.rejected(contract.check_deck,self.deck.replace(
            "RECOVER: PROJECTED :: ITEM 1", "RECOVER: PROJECTED :: ITEM 2", 1
        ))

    def test_post_b2j_mutation_rejected(self) -> None:
        needle = "if (status /= SPOR64_B2J_ARCHIVE_PROJECTED)"
        changed = self.preparer.replace(needle,"call LCMPUT(projected,'BAD',1,1,status)\n  " + needle)
        self.rejected(contract.check_preparer,changed)

    def test_minimal_library_builder_rejected(self) -> None:
        changed = self.preparer.replace(
            "call LCMEQU(source_item,output_item)",
            "call LCMPUT(output_item,'STATE-VECTOR',1,1,ip)",1,
        )
        self.rejected(contract.check_preparer,changed)

    def test_ulp_perturbation_rejected(self) -> None:
        changed = self.preparer.replace(
            "flux64(:,ig)=real(flux32,real64)",
            "flux64(:,ig)=spacing(real(flux32,real64))",
        )
        self.rejected(contract.check_preparer,changed)

    def test_direct_list_child_publication_rejected(self) -> None:
        changed = self.preparer.replace(
            "call SPOR64_B2C_PUBLISH(published,4,",
            "call SPOR64_B2C_PUBLISH(target,4,",
        )
        self.rejected(contract.check_preparer,changed)

    def test_missing_publication_stage_copy_rejected(self) -> None:
        changed = self.preparer.replace(
            "call LCMEQU(published,target)",
            "call REQUIRE_ASSOCIATED(target,'not a stage copy')",
        )
        self.rejected(contract.check_preparer,changed)

    def test_missing_nonexistent_output_guard_rejected(self) -> None:
        changed = self.preparer.replace(
            "if (output_exists) error stop 'PROJECTED output path already exists'",
            "if (.false.) error stop 'PROJECTED output path already exists'",
        )
        self.rejected(contract.check_preparer,changed)

    def test_memory_only_b2j_target_rejected(self) -> None:
        changed = self.b2j.replace(
            "EMPTY_LCM_ROOT = empty .and.",
            "EMPTY_LCM_ROOT = memory_backed .and. empty .and.",
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_weakened_b2j_root_predicates_rejected(self) -> None:
        mutations = (
            ("EMPTY_LCM_ROOT = empty .and.",
             "EMPTY_LCM_ROOT = .true. .and."),
            ("object_length == -1","object_length >= -1"),
            ("trim(object_name) == '/'","trim(object_name) /= ''"),
        )
        for old,new in mutations:
            with self.subTest(old=old):
                self.rejected(
                    contract.check_b2j_target,self.b2j.replace(old,new,1)
                )

    def test_each_b2j_alias_guard_is_required(self) -> None:
        guards = (
            "if (c_associated(iparchiveout,ipax)) return",
            "if (c_associated(iparchiveout,ipaxtrack)) return",
            "if (c_associated(iparchiveout,iparchive)) return",
            "if (c_associated(ipax,ipaxtrack)) return",
            "if (c_associated(ipax,iparchive)) return",
            "if (c_associated(ipaxtrack,iparchive)) return",
        )
        for guard in guards:
            with self.subTest(guard=guard):
                self.assertEqual(self.b2j.count(guard),1)
                self.rejected(
                    contract.check_b2j_target,
                    self.b2j.replace(guard,"if (.false.) return",1),
                )

    def test_b2j_entry_freshness_check_is_required(self) -> None:
        needle = "if (.not. EMPTY_LCM_ROOT(iparchiveout)) return"
        self.assertEqual(self.b2j.count(needle),1)
        changed = self.b2j.replace(
            needle,
            "if (.false.) return",1,
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_precommit_freshness_check_is_required(self) -> None:
        needle = "if (.not. EMPTY_LCM_ROOT(iparchiveout)) then"
        self.assertEqual(self.b2j.count(needle),1)
        changed = self.b2j.replace(
            needle,
            "if (.false.) then",1,
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_rejected_b2h_stage_cleanup_is_required(self) -> None:
        marker = "if (b2h_status == SPOR64_B2H_ADMISSION_FAILED) then"
        self.assertEqual(self.b2j.count(marker),1)
        changed = self.replaced_after(
            self.b2j,marker,"call CLOSE_STAGES(staged_flux)","continue"
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_invalid_staged_payload_cleanup_is_required(self) -> None:
        marker = "if (.not. STAGED_PROJECTED_OBJECT_IS_COMMITTED"
        self.assertEqual(self.b2j.count(marker),1)
        changed = self.replaced_after(
            self.b2j,marker,"call CLOSE_STAGES(staged_flux)","continue"
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_precommit_collision_cleanup_is_required(self) -> None:
        marker = "if (.not. EMPTY_LCM_ROOT(iparchiveout)) then"
        self.assertEqual(self.b2j.count(marker),1)
        changed = self.replaced_after(
            self.b2j,marker,"call CLOSE_STAGES(staged_flux)","continue"
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_success_stage_cleanup_is_required(self) -> None:
        needle = "    call CLOSE_STAGES(staged_flux)\n\n    ! Archive EPOCH"
        self.assertEqual(self.b2j.count(needle),1)
        changed = self.b2j.replace(needle,"    ! Archive EPOCH",1)
        self.rejected(contract.check_b2j_target,changed)

    def test_b2j_epoch_must_be_final_mutation(self) -> None:
        epoch = "call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)"
        self.assertEqual(self.b2j.count(epoch),1)
        changed = self.b2j.replace(
            epoch,epoch + "\n    call LCMPUT(iparchiveout,'BAD',1,1,status)",1
        )
        self.rejected(contract.check_b2j_target,changed)

    def test_formula_reassociation_rejected(self) -> None:
        changed = self.posterior.replace(
            "expected_sused(im)=expected_sphys(im)-leakage(ig)",
            "expected_sused(im)=sigw(im)-(tranc(im)+leakage(ig))",
        )
        self.rejected(contract.check_posterior,changed)

    def test_missing_full_copy_comparison_rejected(self) -> None:
        changed = self.posterior.replace(
            "call COMPARE_DICTIONARY(left_item,right_item,compared_records, &",
            "call REQUIRE_ASSOCIATED(left_item,'not a comparison') !",1,
        )
        self.rejected(contract.check_posterior,changed)

    def test_tolerance_rejected(self) -> None:
        self.rejected(
            contract.check_posterior,
            self.posterior.replace("implicit none", "implicit none\n  real :: tolerance"),
        )

    def test_negative_zero_is_not_a_nonzero_response(self) -> None:
        needle = (
            "count(iand( &\n"
            "            transfer(response,0_int32,size(response)), &\n"
            "            REAL32_MAGNITUDE_MASK) /= 0_int32)"
        )
        self.assertEqual(self.posterior.count(needle),1)
        changed = self.posterior.replace(
            needle,
            "count(transfer(response,0_int32,size(response)) /= 0_int32)",
            1,
        )
        self.rejected(contract.check_posterior,changed)

    def test_wall_limit_change_rejected(self) -> None:
        self.rejected(contract.check_bounded,self.bounded.replace(
            '"wall_seconds": 15','"wall_seconds": 60'
        ))

    def test_cpu_limit_change_rejected(self) -> None:
        self.rejected(contract.check_bounded,self.bounded.replace(
            '"cpu_seconds": 10','"cpu_seconds": 30'
        ))

    def test_process_group_removal_rejected(self) -> None:
        self.rejected(contract.check_bounded,self.bounded.replace(
            "start_new_session=True","start_new_session=False"
        ))

    def test_unanchored_echo_marker_rejected(self) -> None:
        changed = self.runner.replace(
            "^>\\|B2L-ONE-PLANE-REAL-ASM-BEGIN",
            "B2L-ONE-PLANE-REAL-ASM-BEGIN",
        )
        self.rejected(contract.check_runner,changed)

    def test_forbidden_module_grep_without_separator_rejected(self) -> None:
        changed = self.runner.replace("if grep -E -- \\","if grep -E \\")
        self.rejected(contract.check_runner,changed)

    def test_xsm_lifecycle_harness_is_required_once(self) -> None:
        block = (
            'if ! python3 "$BOUNDED" prepare '
            '"$BUILD_DIR/test_b2j_xsm_target" - \\\n'
            '  "$XSM_CASE_DIR/xsm_target.log" ax.xsm archive.xsm '
            'axial_track.xsm\n'
        )
        self.assertEqual(self.runner.count(block),1)
        self.rejected(contract.check_runner,self.runner.replace(block,"",1))
        self.rejected(contract.check_runner,self.runner.replace(block,block+block,1))

    def test_xsm_lifecycle_precedes_default_off_return(self) -> None:
        marker = (
            'if ! python3 "$BOUNDED" prepare '
            '"$BUILD_DIR/test_b2j_xsm_target" - \\\n'
        )
        self.assertEqual(self.runner.count(marker),1)
        early_return = 'if [ "$RUN_B2L" = 0 ]; then\n  :\nfi\n'
        changed = self.runner.replace(marker,early_return+marker,1)
        self.rejected(contract.check_runner,changed)

    def test_each_xsm_lifecycle_case_is_required(self) -> None:
        calls = (
            "call RUN_POSITIVE_XSM()",
            "call RUN_SENTINEL_REJECTION()",
            "call RUN_TOMBSTONE_REJECTION()",
            "call RUN_EARLY_REJECTION()",
            "call RUN_LATE_REJECTION(2,LATE2_PATH)",
            "call RUN_LATE_REJECTION(3,LATE3_PATH)",
        )
        for call in calls:
            with self.subTest(call=call):
                self.assertEqual(self.xsm_harness.count(call),1)
                changed = self.xsm_harness.replace(call,"continue",1)
                self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_tombstone_deletion_is_required(self) -> None:
        needle = "call LCMDEL(output,'SENTINEL')"
        self.assertEqual(self.xsm_harness.count(needle),1)
        changed = self.xsm_harness.replace(needle,"continue",1)
        self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_tombstone_must_be_checked_after_reopen(self) -> None:
        marker = "call OPEN_READ_ONLY_XSM(TOMBSTONE_PATH,output)"
        needle = "call REQUIRE_TOMBSTONED_XSM(output)"
        self.assertEqual(self.xsm_harness.count(marker),1)
        before,after = self.xsm_harness.split(marker,1)
        self.assertEqual(after.count(needle),1)
        changed = before + marker + after.replace(needle,"continue",1)
        self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_reopen_must_be_read_only(self) -> None:
        needle = "call LCMOP(root,path,2,2,0)"
        self.assertEqual(self.xsm_harness.count(needle),1)
        changed = self.xsm_harness.replace(
            needle,"call LCMOP(root,path,0,2,0)",1
        )
        self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_medium_check_is_required(self) -> None:
        needle = "if (memory_backed .or. object_length /= -1 .or. &"
        self.assertEqual(self.xsm_harness.count(needle),1)
        changed = self.xsm_harness.replace(
            needle,"if (.false. .or. object_length /= -1 .or. &",1
        )
        self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_late_plane_two_mutation_is_required(self) -> None:
        needle = "eps(1)=nearest(eps(1),1.0_real32)"
        self.assertEqual(self.xsm_harness.count(needle),1)
        changed = self.xsm_harness.replace(needle,"eps(1)=eps(1)",1)
        self.rejected(contract.check_xsm_harness,changed)

    def test_xsm_late_plane_three_nan_is_required(self) -> None:
        needle = "source_group(1)=ieee_value(0.0_real64,ieee_quiet_nan)"
        self.assertEqual(self.xsm_harness.count(needle),1)
        changed = self.xsm_harness.replace(needle,"source_group(1)=0.0_real64",1)
        self.rejected(contract.check_xsm_harness,changed)


if __name__ == "__main__":
    unittest.main()

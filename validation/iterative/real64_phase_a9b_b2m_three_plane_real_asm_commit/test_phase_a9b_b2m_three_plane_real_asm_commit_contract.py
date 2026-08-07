#!/usr/bin/env python3
"""Mutation regressions for the B2m three-plane real-ASM commit contract."""

from __future__ import annotations

import unittest

import check_phase_a9b_b2m_three_plane_real_asm_commit as contract


class B2MContractMutationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = contract.DECK.read_text(encoding="utf-8")
        cls.host = contract.HOST.read_text(encoding="utf-8")
        cls.asm = contract.ASM.read_text(encoding="utf-8")
        cls.asmdrv = contract.ASMDRV.read_text(encoding="utf-8")
        cls.kdrdpr = contract.KDRDPR.read_text(encoding="utf-8")
        cls.cle2000 = contract.CLE2000.read_text(encoding="utf-8")
        cls.b2k = contract.B2K.read_text(encoding="utf-8")
        cls.posterior = contract.POSTERIOR.read_text(encoding="utf-8")
        cls.bounded = contract.BOUNDED.read_text(encoding="utf-8")
        cls.runner = contract.RUNNER.read_text(encoding="utf-8")
        cls.readme = contract.README.read_text(encoding="utf-8")
        cls.manifest = contract.MANIFEST.read_text(encoding="utf-8")
        cls.runtime_result = contract.RUNTIME_RESULT.read_text(encoding="utf-8")

    def rejected(self, function, text: str, *extra: str) -> None:
        with self.assertRaises(contract.GateError):
            function(text, *extra)

    def changed(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation needle differs: {old}")
        return text.replace(old, new, 1)

    def test_baseline(self) -> None:
        contract.check_all()

    def test_projected_xsm_to_memory_copy_required(self) -> None:
        changed = self.changed(
            self.deck, "PROJECTED := PROJ_XSM ;", "PROJECTED := ASSM_XSM ;"
        )
        self.rejected(contract.check_deck, changed)

    def test_spotasmr64_must_be_called_once(self) -> None:
        changed = self.changed(
            self.deck,
            "ASSEMBLED := SpotAsmR64 PROJECTED TRACK_f :: ;",
            "ASSEMBLED := SpotAsmR64 PROJECTED TRACK_f :: ;\n"
            "ASSEMBLED := SpotAsmR64 PROJECTED TRACK_f :: ;",
        )
        self.rejected(contract.check_deck, changed)

    def test_spotasmr64_must_consume_memory_projected(self) -> None:
        changed = self.changed(
            self.deck,
            "SpotAsmR64 PROJECTED TRACK_f",
            "SpotAsmR64 PROJ_XSM TRACK_f",
        )
        self.rejected(contract.check_deck, changed)

    def test_whole_object_evidence_copy_required(self) -> None:
        changed = self.changed(
            self.deck, "ASSM_XSM := ASSEMBLED ;", "ASSM_XSM := PROJECTED ;"
        )
        self.rejected(contract.check_deck, changed)

    def test_direct_xsm_spor64k_target_rejected(self) -> None:
        changed = self.changed(
            self.deck,
            "ASSEMBLED := SpotAsmR64 PROJECTED TRACK_f :: ;",
            "ASSM_XSM := SpotAsmR64 PROJECTED TRACK_f :: ;",
        )
        self.rejected(contract.check_deck, changed)

    def test_wrapper_flu_rejected(self) -> None:
        changed = self.changed(
            self.deck, "MODULE DELETE: END: ;", "MODULE FLU: DELETE: END: ;"
        )
        self.rejected(contract.check_deck, changed)

    def test_wrapper_loop_rejected(self) -> None:
        self.rejected(contract.check_deck, self.deck + "\nWHILE 1 2 < DO\n")

    def test_host_plane_two_track_mismatch_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "TRACK := RECOVER: PROJECTED :: ITEM 2 ;",
            "TRACK := RECOVER: PROJECTED :: ITEM 1 ;",
        )
        self.rejected(contract.check_host, changed)

    def test_host_lk1d_three_mismatch_rejected(self) -> None:
        changed = self.changed(
            self.host, "EDIT 0 ARM LK1D 3 ;", "EDIT 0 ARM LK1D 2 ;"
        )
        self.rejected(contract.check_host, changed)

    def test_host_missing_spor64k_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "ASSEMBLED := SPOR64K: PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 :: ;",
            "ASSEMBLED := SYSTEM1 ;",
        )
        self.rejected(contract.check_host, changed)

    def test_host_flu_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "MODULE RECOVER: ASM: SPOR64K: DELETE: END: ;",
            "MODULE RECOVER: ASM: FLU: SPOR64K: DELETE: END: ;",
        )
        self.rejected(contract.check_host, changed)

    def test_production_xdrta2_argument_rejected(self) -> None:
        changed = self.changed(self.asm, "CALL XDRTA2\n", "CALL XDRTA2(IPTRK)\n")
        self.rejected(contract.check_production, changed, self.asmdrv)

    def test_production_s0_reassociation_rejected(self) -> None:
        changed = self.changed(
            self.asmdrv,
            "S0PHYS(0:NBMIX,IGR)-LEAK1D(IGR)",
            "XSSIGW(0:NBMIX,1,IGR)-LEAK1D(IGR)",
        )
        self.rejected(contract.check_production, self.asm, changed)

    def test_loader_source_visibility_probe_required(self) -> None:
        changed = self.changed(
            self.kdrdpr, 'file = fopen(filinp, "r");',
            'file = fopen(filobj, "r");',
        )
        self.rejected(contract.check_loader, changed, self.cle2000)

    def test_loader_precompiled_object_probe_required(self) -> None:
        changed = self.changed(
            self.cle2000, 'icfile = fopen(filobj, "r");',
            'icfile = NULL;',
        )
        self.rejected(contract.check_loader, self.kdrdpr, changed)

    def test_b2k_direct_xsm_output_admission_rejected(self) -> None:
        changed = self.changed(
            self.b2k,
            "EMPTY_LCM_ROOT = is_lcm .and. empty .and.",
            "EMPTY_LCM_ROOT = empty .and.",
        )
        self.rejected(contract.check_b2k, changed)

    def test_b2k_system_alias_guard_required(self) -> None:
        changed = self.changed(
            self.b2k,
            "if (c_associated(ipsystems(ip),ipsystems(ir))) return",
            "if (.false.) return",
        )
        self.rejected(contract.check_b2k, changed)

    def test_b2k_second_freshness_check_required(self) -> None:
        changed = self.changed(
            self.b2k,
            "if (.not. EMPTY_LCM_ROOT(ipout)) then",
            "if (.false.) then",
        )
        self.rejected(contract.check_b2k, changed)

    def test_b2k_complete_system_copy_required(self) -> None:
        changed = self.changed(
            self.b2k,
            "call LCMEQU(staged_system(ip),output_item)",
            "call LCMEQU(input_flux(ip),output_item)",
        )
        self.rejected(contract.check_b2k, changed)

    def test_b2k_epoch_must_be_final_mutation(self) -> None:
        epoch = "call LCMPUT(root_authority,'EPOCH',1,1,ASSEMBLED_EPOCH)"
        self.assertEqual(self.b2k.count(epoch), 1)
        changed = self.b2k.replace(
            epoch, epoch + "\n    call LCMPUT(ipout,'BAD',1,1,status)", 1
        )
        self.rejected(contract.check_b2k, changed)

    def test_posterior_formula_reassociation_rejected(self) -> None:
        changed = self.changed(
            self.posterior,
            "expected_sused(im)=expected_sphys(im)-leakage(ig)",
            "expected_sused(im)=sigw(im)-(tranc(im)+leakage(ig))",
        )
        self.rejected(contract.check_posterior, changed)

    def test_posterior_signed_zero_rule_required(self) -> None:
        old = (
            "iand( &\n"
            "              transfer(response,0_int32,size(response)), &\n"
            "              REAL32_MAGNITUDE_MASK) /= 0_int32"
        )
        new = "transfer(response,0_int32,size(response)) /= 0_int32"
        changed = self.changed(self.posterior, old, new)
        self.rejected(contract.check_posterior, changed)

    def test_posterior_per_plane_nonzero_required(self) -> None:
        changed = self.changed(
            self.posterior,
            "if (any(response_nonzero_by_plane <= 0))",
            "if (sum(response_nonzero_by_plane) <= 0)",
        )
        self.rejected(contract.check_posterior, changed)

    def test_posterior_all_three_response_count_required(self) -> None:
        changed = self.changed(
            self.posterior,
            "response_values /= NSNAP*NGRP*sum(RESPONSE_LENGTHS)",
            "response_values /= NGRP*sum(RESPONSE_LENGTHS)",
        )
        self.rejected(contract.check_posterior, changed)

    def test_posterior_tolerance_rejected(self) -> None:
        changed = self.changed(
            self.posterior, "implicit none", "implicit none\n  real :: tolerance"
        )
        self.rejected(contract.check_posterior, changed)

    def test_posterior_solver_link_rejected(self) -> None:
        changed = self.changed(
            self.posterior, "implicit none", "implicit none\n  use SPOR64_B2K"
        )
        self.rejected(contract.check_posterior, changed)

    def test_assemble3_profile_required(self) -> None:
        changed = self.changed(
            self.bounded, '"assemble3": {', '"assemble": {'
        )
        self.rejected(contract.check_bounded, changed)

    def test_wall_limit_change_rejected(self) -> None:
        # Change every identical profile wall value so the required frozen
        # inventory is absent rather than accidentally satisfied elsewhere.
        self.assertGreaterEqual(self.bounded.count('"wall_seconds": 30'), 1)
        changed = self.bounded.replace('"wall_seconds": 30', '"wall_seconds": 60')
        self.rejected(contract.check_bounded, changed)

    def test_process_group_removal_rejected(self) -> None:
        changed = self.changed(
            self.bounded, "start_new_session=True", "start_new_session=False"
        )
        self.rejected(contract.check_bounded, changed)

    def test_retry_path_rejected(self) -> None:
        changed = self.changed(
            self.bounded, "def main() -> None:",
            "def retry(count: int) -> None:\n    pass\n\ndef main() -> None:",
        )
        self.rejected(contract.check_bounded, changed)

    def test_runtime_activation_defaults_off(self) -> None:
        changed = self.changed(
            self.runner, "RUN_B2M=${RUN_B2M:-0}", "RUN_B2M=${RUN_B2M:-1}"
        )
        self.rejected(contract.check_runner, changed)

    def test_second_bounded_dragon_rejected(self) -> None:
        needle = 'python3 "$BOUNDED" assemble3'
        self.assertEqual(self.runner.count(needle), 1)
        changed = self.runner.replace(needle, needle + "\n" + needle, 1)
        self.rejected(contract.check_runner, changed)

    def test_runtime_exact_source_visibility_copy_required(self) -> None:
        changed = self.changed(
            self.runner,
            'copy_exact "$C2M_SOURCE" "$CASE_DIR/SpotAsmR64.c2m"',
            'copy_exact "$DECK" "$CASE_DIR/SpotAsmR64.c2m"',
        )
        self.rejected(contract.check_runner, changed)

    def test_runtime_precompiled_object_copy_required(self) -> None:
        changed = self.changed(
            self.runner,
            'copy_exact "$BUILD_DIR/SpotAsmR64.o2m" '
            '"$CASE_DIR/SpotAsmR64.o2m"',
            'copy_exact "$C2M_SOURCE" "$CASE_DIR/SpotAsmR64.o2m"',
        )
        self.rejected(contract.check_runner, changed)

    def test_runtime_compilation_error_marker_denylist_required(self) -> None:
        changed = self.changed(
            self.runner,
            "COMPILING _MAIN\\.c2m FILE|BAD OBJECTS _MAIN\\.c2m FILE",
            "UNRELATED RUNTIME TEXT",
        )
        self.rejected(contract.check_runner, changed)

    def test_runtime_source_compilation_listing_absence_required(self) -> None:
        needle = '[ ! -e "$CASE_DIR/SpotAsmR64.l2m" ]'
        self.assertEqual(self.runner.count(needle), 3)
        changed = self.runner.replace(needle, ':', 1)
        self.rejected(contract.check_runner, changed)

    def test_unanchored_begin_marker_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            "^>\\|B2M-THREE-PLANE-REAL-ASM-BEGIN",
            "B2M-THREE-PLANE-REAL-ASM-BEGIN",
        )
        self.rejected(contract.check_runner, changed)

    def test_flu_zero_census_required(self) -> None:
        changed = self.changed(
            self.runner, "FLU-FLUX-SOLVES=0", "FLU-FLUX-SOLVES=1"
        )
        self.rejected(contract.check_runner, changed)

    def test_readme_direct_xsm_claim_rejected(self) -> None:
        changed = self.changed(
            self.readme,
            "not claim that `SPOR64K` targeted XSM directly",
            "claim that `SPOR64K` targeted XSM directly",
        )
        self.rejected(contract.check_assets, changed, self.manifest)

    def test_manifest_asm_count_rejected(self) -> None:
        changed = self.changed(self.manifest, '"asm_calls": 3', '"asm_calls": 2')
        self.rejected(contract.check_assets, self.readme, changed)

    def test_manifest_direct_xsm_claim_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"direct_xsm_spor64k_target": false',
            '"direct_xsm_spor64k_target": true',
        )
        self.rejected(contract.check_assets, self.readme, changed)

    def test_manifest_response_accuracy_claim_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"response_numerical_accuracy_evaluated": false',
            '"response_numerical_accuracy_evaluated": true',
        )
        self.rejected(contract.check_assets, self.readme, changed)

    def test_runtime_result_hash_and_manifest_link_required(self) -> None:
        changed = self.changed(
            self.runtime_result,
            "ASSEMBLED-BYTES=227840384",
            "ASSEMBLED-BYTES=227840383",
        )
        self.rejected(contract.check_runtime_result, changed, self.manifest)

    def test_manifest_accepted_timestamp_and_elapsed_times_frozen(self) -> None:
        mutations = (
            ('"utc": "2026-08-07T03:45:31Z"',
             '"utc": "2026-08-07T03:45:32Z"'),
            ('"prepare_wall_seconds": 1.190',
             '"prepare_wall_seconds": 1.191'),
            ('"assemble3_wall_seconds": 2.325',
             '"assemble3_wall_seconds": 2.326'),
            ('"posterior_wall_seconds": [1.026, 0.534]',
             '"posterior_wall_seconds": [1.026, 0.535]'),
        )
        for old,new in mutations:
            with self.subTest(old=old):
                changed = self.changed(self.manifest,old,new)
                self.rejected(contract.check_assets,self.readme,changed)

    def test_manifest_accepted_execution_census_frozen(self) -> None:
        mutations = (
            ('"dragon_executions": 1', '"dragon_executions": 2'),
            ('"asm_executions": 3', '"asm_executions": 2'),
            ('"spor64k_executions": 1', '"spor64k_executions": 0'),
            ('"xdrta2_calls": 3', '"xdrta2_calls": 2'),
            ('"flu_flux_solves": 0', '"flu_flux_solves": 1'),
            ('"flu_flux_solves": 0,\n    "picard_maps": 0',
             '"flu_flux_solves": 0,\n    "picard_maps": 1'),
        )
        for old,new in mutations:
            with self.subTest(old=old):
                changed = self.changed(self.manifest,old,new)
                self.rejected(contract.check_assets,self.readme,changed)

    def test_manifest_accepted_posterior_counts_frozen(self) -> None:
        mutations = (
            ('"full_copy_records": 71280', '"full_copy_records": 71279'),
            ('"full_copy_32bit_words": 54477882',
             '"full_copy_32bit_words": 54477881'),
            ('"response_finite_values": 179820',
             '"response_finite_values": 179819'),
            ('"response_nonzero_values": 106554',
             '"response_nonzero_values": 106553'),
            ('"response_nonzero_by_plane": [35518, 35518, 35518]',
             '"response_nonzero_by_plane": [35518, 35518, 35517]'),
        )
        for old,new in mutations:
            with self.subTest(old=old):
                changed = self.changed(self.manifest,old,new)
                self.rejected(contract.check_assets,self.readme,changed)

    def test_manifest_accepted_hashes_and_sizes_frozen(self) -> None:
        mutations = (
            ("c010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c",
             "d010c0a860884a4e4d3842dffe45ffb4898f2aaca99557e0411ee8c66d60b90c"),
            ("16f79f8fd97ff90ca9bd892cdeab27337fafb3ec6189d9b00b90375fcc596e79",
             "26f79f8fd97ff90ca9bd892cdeab27337fafb3ec6189d9b00b90375fcc596e79"),
            ('"projected_bytes": 225315452',
             '"projected_bytes": 225315451'),
            ('"assembled_bytes": 227840384',
             '"assembled_bytes": 227840383'),
        )
        for old,new in mutations:
            with self.subTest(old=old):
                changed = self.changed(self.manifest,old,new)
                self.rejected(contract.check_assets,self.readme,changed)

    def test_manifest_accepted_semantic_state_required(self) -> None:
        changed = self.changed(
            self.manifest,
            '"real_execution_evaluated": true',
            '"real_execution_evaluated": false',
        )
        self.rejected(contract.check_assets,self.readme,changed)


if __name__ == "__main__":
    unittest.main()

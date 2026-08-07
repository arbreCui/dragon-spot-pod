#!/usr/bin/env python3
"""Mutation regressions for the B2k static system-assembly contract."""

from __future__ import annotations

import unittest

from check_phase_a9b_b2k_system_assembly import (
    ASM,
    ASMDRV,
    C2M,
    KDRDRV,
    XDRTA2,
    GateError,
    SOURCE,
    check_host_wiring,
    check_source,
)


class SystemAssemblyContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text()

    def rejected(self, old: str, new: str) -> None:
        self.assertIn(old, self.source)
        mutated = self.source.replace(old, new, 1)
        with self.assertRaises(GateError):
            check_source(mutated)

    def injected(self, addition: str) -> None:
        marker = "end module SPOR64_B2K"
        self.assertIn(marker, self.source)
        mutated = self.source.replace(marker, addition + "\n" + marker, 1)
        with self.assertRaises(GateError):
            check_source(mutated)

    def host_rejected(self, *, path: str, old: str, new: str) -> None:
        sources = {
            "c2m": C2M.read_text(),
            "kdr": KDRDRV.read_text(),
            "asm": ASM.read_text(),
            "asmdrv": ASMDRV.read_text(),
            "xdrta2": XDRTA2.read_text(),
        }
        self.assertIn(old, sources[path])
        sources[path] = sources[path].replace(old, new, 1)
        kwargs = {
            "c2m_text": sources["c2m"],
            "kdr_text": sources["kdr"],
            "asm_text": sources["asm"],
            "asmdrv_text": sources["asmdrv"],
            "xdrta2_text": sources["xdrta2"],
        }
        with self.assertRaises(GateError):
            check_host_wiring(**kwargs)

    def test_current_contract(self) -> None:
        check_source(self.source)
        check_host_wiring()

    def test_loose_api_argument_rejected(self) -> None:
        self.rejected("ipsystems,status)", "ipsystems,rho,status)")

    def test_output_epoch_mutation_rejected(self) -> None:
        self.rejected("ASSEMBLED_EPOCH = 1", "ASSEMBLED_EPOCH = 2")

    def test_projected_epoch_mutation_rejected(self) -> None:
        self.rejected("PROJECTED_EPOCH = 1", "PROJECTED_EPOCH = 0")

    def test_projected_root_exactness_removed_rejected(self) -> None:
        self.rejected("PROJECTED_ARCHIVE_ROOT_IS_EXACT(ipprojected)",
                      "c_associated(ipprojected)")

    def test_projected_state_mutation_rejected(self) -> None:
        self.rejected("root_authority,'STATE',3,12, &\n        'PROJECTED'",
                      "root_authority,'STATE',3,12, &\n        'ASSEMBLED'")

    def test_candidate_root_exactness_removed_rejected(self) -> None:
        self.rejected("CANDIDATE_SYSTEM_ROOT_IS_EXACT(ipsystems(ip))",
                      "c_associated(ipsystems(ip))")

    def test_staged_root_exactness_removed_rejected(self) -> None:
        self.rejected("STAGED_SYSTEM_ROOT_IS_EXACT(staged_system(ip))",
                      "c_associated(staged_system(ip))")

    def test_candidate_authority_absence_removed_rejected(self) -> None:
        self.rejected("ABSENT_RECORD(ipsystems(ip),'SPOT-R64')",
                      "c_associated(ipsystems(ip))")

    def test_system_alias_guard_removed_rejected(self) -> None:
        self.rejected("c_associated(ipsystems(ip),ipsystems(ir))",
                      "c_associated(ipout,ipprojected)")

    def test_track_state_vector_mutation_rejected(self) -> None:
        self.rejected("165,100000,11364,96", "165,100001,11364,96")

    def test_mccg_state_11_mutation_rejected(self) -> None:
        self.rejected("[-1,4,10,0,17,32,80,0,0,4,0,0,20,1,1,1,0,0,1,1, &",
                      "[-1,4,10,0,17,32,80,0,0,4,1,0,20,1,1,1,0,0,1,1, &")

    def test_mccg_state_14_mutation_rejected(self) -> None:
        self.rejected("[-1,4,10,0,17,32,80,0,0,4,0,0,20,1,1,1,0,0,1,1, &",
                      "[-1,4,10,0,17,32,80,0,0,4,0,0,20,0,1,1,0,0,1,1, &")

    def test_mccg_state_17_mutation_rejected(self) -> None:
        self.rejected("[-1,4,10,0,17,32,80,0,0,4,0,0,20,1,1,1,0,0,1,1, &",
                      "[-1,4,10,0,17,32,80,0,0,4,0,0,20,1,1,1,1,0,1,1, &")

    def test_macro_state_transport_flag_mutation_rejected(self) -> None:
        self.rejected("[NGRP,NMAT,3,NIFIS,18,2,6", "[NGRP,NMAT,3,NIFIS,18,0,6")

    def test_real_param_schema_mutation_rejected(self) -> None:
        self.rejected("'REAL-PARAM',4,2", "'REAL-PARAM',3,2")

    def test_real_param_bits_mutation_rejected(self) -> None:
        self.rejected("MCCG_EPSI_BITS = int(z'3727c5ac',int32)",
                      "MCCG_EPSI_BITS = int(z'3727c5ad',int32)")

    def test_real32_range_guard_removed_rejected(self) -> None:
        self.rejected("if (any(abs(authority64) > REAL32_MAX64)) return",
                      "if (.false.) return")

    def test_matcod_nzon_identity_removed_rejected(self) -> None:
        self.rejected("if (any(nzon(1:NREG) /= matcod)) return",
                      "if (.false.) return")

    def test_volume_bit_identity_removed_rejected(self) -> None:
        self.rejected("if (volume_bits /= track_volume_bits) return",
                      "if (.false.) return")

    def test_keycur_full_cover_removed_rejected(self) -> None:
        self.rejected("if (.not. all(seen_unknown)) return",
                      "if (.false.) return")

    def test_mandatory_tranc_schema_removed_rejected(self) -> None:
        self.rejected("if (ilong /= NMAT .or. itylcm /= 2) return",
                      "if (ilong /= 0 .and. itylcm /= 99) return")

    def test_txsc_subtraction_mutation_rejected(self) -> None:
        self.rejected("expected_tx32(im) = expected_tx32(im)-tranc32(im)",
                      "expected_tx32(im) = expected_tx32(im)+tranc32(im)")

    def test_s0phys_subtraction_mutation_rejected(self) -> None:
        self.rejected("expected_sphys32(im) = expected_sphys32(im)-tranc32(im)",
                      "expected_sphys32(im) = expected_sphys32(im)+tranc32(im)")

    def test_s0used_zero_slot_mutation_rejected(self) -> None:
        self.rejected("expected_sused32(0) = expected_sphys32(0)-leakage(ig)",
                      "expected_sused32(0) = expected_sphys32(0)")

    def test_s0used_material_mutation_rejected(self) -> None:
        self.rejected("expected_sused32(im) = expected_sphys32(im)-leakage(ig)",
                      "expected_sused32(im) = expected_sphys32(im)+leakage(ig)")

    def test_txsc_bit_identity_removed_rejected(self) -> None:
        self.rejected("SAME_REAL32_BITS(tx32,expected_tx32)",
                      "all(ieee_is_finite(tx32))")

    def test_s0phys_bit_identity_removed_rejected(self) -> None:
        self.rejected("SAME_REAL32_BITS(sphys32,expected_sphys32)",
                      "all(ieee_is_finite(sphys32))")

    def test_s0used_bit_identity_removed_rejected(self) -> None:
        self.rejected("SAME_REAL32_BITS(sused32,expected_sused32)",
                      "all(ieee_is_finite(sused32))")

    def test_response_inventory_size_mutation_rejected(self) -> None:
        self.rejected("names(15)", "names(14)")

    def test_response_length_mutation_rejected(self) -> None:
        self.rejected("[32,14,32,14,8,8,8,8,8,8,8,14]",
                      "[32,14,31,14,8,8,8,8,8,8,8,14]")

    def test_missing_response_name_rejected(self) -> None:
        self.rejected("'PJJZI$MCCG  '", "'PJJZZ$MCCG  '")

    def test_funkno_absence_removed_rejected(self) -> None:
        self.rejected("ABSENT_RECORD(group,'FUNKNO$USS')",
                      "c_associated(group)")

    def test_private_stage_call_mutation_rejected(self) -> None:
        self.rejected("call OPEN_STAGE(staged_system(ip),ip)",
                      "call OTHER_STAGE(staged_system(ip),ip)")

    def test_complete_candidate_copy_mutation_rejected(self) -> None:
        self.rejected("call LCMEQU(ipsystems(ip),staged_system(ip))",
                      "call LCMEQU(input_flux(ip),staged_system(ip))")

    def test_complete_output_system_copy_mutation_rejected(self) -> None:
        self.rejected("call LCMEQU(staged_system(ip),output_item)",
                      "call LCMEQU(input_flux(ip),output_item)")

    def test_projected_flux_relabel_copy_mutation_rejected(self) -> None:
        self.rejected("call LCMEQU(input_flux(ip),output_item)",
                      "call LCMEQU(staged_system(ip),output_item)")

    def test_second_freshness_check_mutation_rejected(self) -> None:
        self.rejected("if (.not. EMPTY_LCM_ROOT(ipout)) then",
                      "if (.false.) then")

    def test_root_epoch_order_mutation_rejected(self) -> None:
        old = ("    call LCMPTC(root_authority,'STATE',12,lifecycle_state)\n"
               "    call LCMPUT(root_authority,'EPOCH',1,1,ASSEMBLED_EPOCH)")
        new = ("    call LCMPUT(root_authority,'EPOCH',1,1,ASSEMBLED_EPOCH)\n"
               "    call LCMPTC(root_authority,'STATE',12,lifecycle_state)")
        self.rejected(old, new)

    def test_wrapper_entry_count_mutation_rejected(self) -> None:
        self.rejected("if (nentry /= 5)", "if (nentry /= 4)")

    def test_wrapper_system_order_mutation_rejected(self) -> None:
        self.rejected("systems = kentry(3:5)", "systems = kentry([4,3,5])")

    def test_wrapper_readonly_mutation_rejected(self) -> None:
        self.rejected("any(jentry(2:5) /= 2)", "any(jentry(2:5) /= 1)")

    def test_wrapper_semicolon_mutation_rejected(self) -> None:
        self.rejected("text4 /= ';'", "text4 /= '::'")

    def test_empirical_alpha_rejected(self) -> None:
        self.injected("subroutine B2K_BAD_ALPHA\nreal :: alpha\nend subroutine")

    def test_qfiss_cont_rejected(self) -> None:
        self.injected("subroutine B2K_BAD_CONT\ncharacter(6) :: qfiss\n"
                      "qfiss='CONT'\nend subroutine")

    def test_solver_call_rejected(self) -> None:
        self.injected("subroutine B2K_BAD_SOLVE\ncall ASMDRV\nend subroutine")

    def test_c2m_track_plane_mismatch_rejected(self) -> None:
        self.host_rejected(path="c2m",
                           old="TRACK := RECOVER: PROJECTED :: ITEM 2 ;",
                           new="TRACK := RECOVER: PROJECTED :: ITEM 1 ;")

    def test_c2m_linked_list_declaration_mutation_rejected(self) -> None:
        self.host_rejected(
            path="c2m",
            old="LINKED_LIST MICROLIB2 MACRO0 TRACK SYSTEM1 SYSTEM2 SYSTEM3 ;",
            new="LINKED_LIST MICROLIB2 MACRO0 TRACK SYSTEM1 SYSTEM2 ;",
        )

    def test_c2m_module_declaration_mutation_rejected(self) -> None:
        self.host_rejected(path="c2m", old="MODULE RECOVER: ASM: SPOR64K: DELETE: END: ;",
                           new="MODULE RECOVER: ASM: DELETE: END: ;")

    def test_c2m_macro_name_mutation_rejected(self) -> None:
        self.host_rejected(path="c2m", old="MACRO0 := MICROLIB2 ;",
                           new="MACRO1 := MICROLIB2 ;")

    def test_c2m_lk1d_plane_mismatch_rejected(self) -> None:
        self.host_rejected(path="c2m", old="EDIT 0 ARM LK1D 3 ;",
                           new="EDIT 0 ARM LK1D 2 ;")

    def test_kdr_dispatch_mutation_rejected(self) -> None:
        self.host_rejected(path="kdr", old="HMODUL.EQ.'SPOR64K:'",
                           new="HMODUL.EQ.'SPOR64X:'")

    def test_xdrta2_argument_mutation_rejected(self) -> None:
        self.host_rejected(path="asm", old="CALL XDRTA2\n",
                           new="CALL XDRTA2(IPTRK)\n")

    def test_xdrta2_definition_argument_mutation_rejected(self) -> None:
        self.host_rejected(path="xdrta2", old="SUBROUTINE XDRTA2\n",
                           new="SUBROUTINE XDRTA2(IPTRK)\n")

    def test_asmdrv_reassociation_rejected(self) -> None:
        self.host_rejected(
            path="asmdrv",
            old="S0PHYS(0:NBMIX,IGR)-LEAK1D(IGR)",
            new="XSSIGW(0:NBMIX,1,IGR)-LEAK1D(IGR)",
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Mutation regressions for the B2j static contract."""

from __future__ import annotations

import unittest

from check_phase_a9b_b2j_archive_projection import GateError, SOURCE, check_source


class ArchiveProjectionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text()

    def rejected(self, old: str, new: str) -> None:
        self.assertIn(old, self.source)
        mutated = self.source.replace(old, new, 1)
        with self.assertRaises(GateError):
            check_source(mutated)

    def injected(self, addition: str) -> None:
        mutated = self.source.replace("end module SPOR64_B2J", addition +
                                      "\nend module SPOR64_B2J", 1)
        with self.assertRaises(GateError):
            check_source(mutated)

    def test_current_contract(self) -> None:
        check_source(self.source)

    def test_loose_rho_argument_rejected(self) -> None:
        self.rejected("iparchive,status)", "iparchive,rho,status)")

    def test_input_epoch_mutation_rejected(self) -> None:
        self.rejected("BOOTSTRAP_INPUT_EPOCH = 0",
                      "BOOTSTRAP_INPUT_EPOCH = 2")

    def test_output_epoch_mutation_rejected(self) -> None:
        self.rejected("BOOTSTRAP_OUTPUT_EPOCH = 1",
                      "BOOTSTRAP_OUTPUT_EPOCH = 3")

    def test_ax_state_mutation_rejected(self) -> None:
        self.rejected("'SPOT-X-STATE',3,12, &\n        'CLOSED'",
                      "'SPOT-X-STATE',3,12, &\n        'PROJECTED'")

    def test_root_state_mutation_rejected(self) -> None:
        self.rejected("root_authority,'STATE',3,12, &\n        'CLOSED'",
                      "root_authority,'STATE',3,12, &\n        'SOLVED'")

    def test_plane_state_mutation_rejected(self) -> None:
        self.rejected("plane_authority,'STATE',3,12, &\n          'SOLVED'",
                      "plane_authority,'STATE',3,12, &\n          'PROJECTED'")

    def test_archive_inventory_mutation_rejected(self) -> None:
        self.rejected("CLOSED_ARCHIVE_ROOT_IS_EXACT(iparchive)",
                      "c_associated(iparchive)")

    def test_root_rho_tolerance_rejected(self) -> None:
        self.rejected(
            "transfer(root_rho64,0_int64) /= transfer(rho64,0_int64)",
            "abs(root_rho64-rho64) > 1.0e-8_real64",
        )

    def test_plane_rho_tolerance_rejected(self) -> None:
        self.rejected(
            "transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)",
            "abs(plane_rho64-rho64) > 1.0e-8_real64",
        )

    def test_inverse_eigenvalue_mutation_rejected(self) -> None:
        self.rejected("1.0_real64/real(keff32,real64)",
                      "real(keff32,real64)")

    def test_iter_keff_mutation_rejected(self) -> None:
        self.rejected("real(keff32,real64),0_int64",
                      "1.0_real64/real(keff32,real64),0_int64")

    def test_rank_schema_mutation_rejected(self) -> None:
        self.rejected("'SPOT-X-RANK',NGRP,1", "'SPOT-X-RANK',NGRP-1,1")

    def test_basis_index_mutation_rejected(self) -> None:
        self.rejected("basis_offset(ig)+(a-1)*NREG+1",
                      "basis_offset(ig)+a*NREG+1")

    def test_coordinate_index_mutation_rejected(self) -> None:
        self.rejected("offset(ig)+(ip-1)*nmode+1", "offset(ig)+ip*nmode+1")

    def test_reconstruct_call_mutation_rejected(self) -> None:
        self.rejected("call SPOR64_B2H_RECONSTRUCT", "call OTHER_RECONSTRUCT")

    def test_reconstruct_rejection_mutation_rejected(self) -> None:
        self.rejected("if (.not. reconstruction_ok) return",
                      "if (.false.) return")

    def test_matmul_mutation_rejected(self) -> None:
        self.injected("subroutine B2J_BAD_MATMUL\nreal :: a(1,1),b(1),c(1)\n"
                      "c=matmul(a,b)\nend subroutine B2J_BAD_MATMUL")

    def test_leakage_schema_mutation_rejected(self) -> None:
        self.rejected("'SPOT-X-L',NGRP*NSNAP,4",
                      "'SPOT-X-L',NGRP,4")

    def test_leakage_plane_index_mutation_rejected(self) -> None:
        self.rejected("leakage64((ip-1)*NGRP+ig)",
                      "leakage64((ip-1)*NGRP+1)")

    def test_system_plane_identity_mutation_rejected(self) -> None:
        self.rejected("if (system_snapshot /= ip) return",
                      "if (system_snapshot < 1) return")

    def test_track_state_mutation_rejected(self) -> None:
        self.rejected("plane_track_state(14) /= 4",
                      "plane_track_state(14) /= 3")

    def test_track_type_mutation_rejected(self) -> None:
        self.rejected("3,12,'MCCG'", "3,12,'MOC '")

    def test_track_key_identity_mutation_rejected(self) -> None:
        self.rejected("if (plane_key(ir) /= anis_key(ir)) return",
                      "if (plane_key(ir) < 1) return")

    def test_output_system_creation_rejected(self) -> None:
        self.rejected("output_fluxes = LCMLID(iparchiveout,'FLUX',NSNAP)",
                      "output_fluxes = LCMLID(iparchiveout,'SYSTEM',NSNAP)")

    def test_lagged_system_copy_rejected(self) -> None:
        self.rejected("call LCMEQU(input_library(ip),output_item)",
                      "call LCMEQU(input_system(ip),output_item)")

    def test_unstaged_flux_copy_rejected(self) -> None:
        self.rejected("call LCMEQU(staged_flux(ip),output_item)",
                      "call LCMEQU(input_flux(ip),output_item)")

    def test_b2h_project_call_mutation_rejected(self) -> None:
        self.rejected("call SPOR64_B2H_PROJECT", "call SPOPROJ")

    def test_staged_root_inventory_mutation_rejected(self) -> None:
        self.rejected("if (.not. PROJECTED_PLANE_ROOT_IS_EXACT(iplist)) return",
                      "if (.not. c_associated(iplist)) return")

    def test_staged_authority_type_mutation_rejected(self) -> None:
        self.rejected("ilong /= NUNKNO .or. itylcm /= 4",
                      "ilong /= NUNKNO .or. itylcm /= 2")

    def test_stage_close_order_mutation_rejected(self) -> None:
        old = "    call CLOSE_STAGES(staged_flux)\n\n    ! Archive EPOCH"
        new = "    ! Archive EPOCH"
        self.rejected(old, new)

    def test_root_epoch_order_mutation_rejected(self) -> None:
        old = ("    call LCMPTC(output_authority,'STATE',12,lifecycle_state)\n"
               "    call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)")
        new = ("    call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)\n"
               "    call LCMPTC(output_authority,'STATE',12,lifecycle_state)")
        self.rejected(old, new)

    def test_second_freshness_check_mutation_rejected(self) -> None:
        old = "if (.not. EMPTY_LCM_ROOT(iparchiveout)) then"
        self.rejected(old, "if (.false.) then")

    def test_empirical_alpha_rejected(self) -> None:
        self.injected("real(real64) :: alpha")

    def test_qfiss_and_cont_path_rejected(self) -> None:
        self.injected("subroutine B2J_BAD_CONT\ncharacter(len=5) :: qfiss\n"
                      "qfiss='CONT'\nend subroutine B2J_BAD_CONT")


if __name__ == "__main__":
    unittest.main()

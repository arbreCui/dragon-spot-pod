#!/usr/bin/env python3
"""Mutation tests for the independent B2i bootstrap-lifecycle gate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from check_phase_a9b_b2i_bootstrap_lifecycle import (  # noqa: E402
    GateError,
    check_all,
    check_api_and_isolation,
    check_archive_admission,
    check_canonical_bundle,
    check_no_empirical_or_solver_path,
    check_publication_boundary,
    load_production_files,
)


ROOT = Path(__file__).resolve().parents[3]


class BootstrapLifecycleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = (ROOT / "src/SPOR64_B2I.f90").read_text()
        cls.production = load_production_files(ROOT)

    def mutate_once(self, old: str, new: str) -> str:
        self.assertEqual(self.source.count(old), 1, f"mutation anchor: {old}")
        return self.source.replace(old, new, 1)

    def mutate_last(self, old: str, new: str) -> str:
        self.assertGreaterEqual(self.source.count(old), 1)
        prefix, separator, suffix = self.source.rpartition(old)
        self.assertEqual(separator, old)
        return prefix + new + suffix

    def test_current_contract(self) -> None:
        check_all(self.source, self.production)

    def test_production_connection_rejected(self) -> None:
        fake = {
            ROOT / "src/connected.f90":
                "use, non_intrinsic :: SPOR64_B2I\n"
        }
        with self.assertRaises(GateError):
            check_api_and_isolation(self.source, fake)

    def test_bootstrap_epoch_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "integer, parameter :: BOOTSTRAP_EPOCH = 0",
            "integer, parameter :: BOOTSTRAP_EPOCH = 1",
        )
        with self.assertRaises(GateError):
            check_api_and_isolation(bad, {})

    def test_loose_alpha_argument_rejected(self) -> None:
        bad = self.mutate_once(
            "ipaxtrack,iparchive,status)",
            "ipaxtrack,iparchive,alpha,status)",
        )
        with self.assertRaises(GateError):
            check_api_and_isolation(bad, {})

    def test_inverse_eigenvalue_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "1.0_real64/real(keff32,real64)",
            "2.0_real64/real(keff32,real64)",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_perp_type_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "'SPOT-X-PERP',NGRP*NSNAP,4",
            "'SPOT-X-PERP',NGRP*NSNAP,2",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_height_map_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "height_check64(mat1d(ir)) = height_check64(mat1d(ir)) + &",
            "height_check64(1) = height_check64(1) + &",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_gram_loop_order_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "do a = 1, nmode\n        do b = 1, nmode",
            "do b = 1, nmode\n        do a = 1, nmode",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_gram_index_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "index_g = gram_offset(ig)+(b-1)*nmode+a",
            "index_g = gram_offset(ig)+(a-1)*nmode+b",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_gerr_identity_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "transfer(gram_error_check64,0_int64) /= &",
            "transfer(gram_error64,0_int64) /= &",
        )
        with self.assertRaises(GateError):
            check_canonical_bundle(bad)

    def test_iter_keff_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "transfer(real(keff32,real64),0_int64)) return",
            "transfer(1.0_real64,0_int64)) return",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_exact_leakage_promotion_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "real(plane_leak32(ig),real64),0_int64",
            "real(real(leakage64((ip-1)*NGRP+ig),real32),real64),0_int64",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_volume_tolerance_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "transfer(volume32(ir),0_int32) /= &\n            transfer(area32(ir),0_int32)",
            "abs(volume32(ir)-area32(ir)) > 1.0e-4_real32",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_key_identity_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "if (plane_key(ir) /= anis_key(ir)) return",
            "if (plane_key(ir) < 1) return",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_library_macro_group_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "RECORD_MATCHES(library_macro,'GROUP',NGRP,10)",
            "RECORD_MATCHES(library_macro,'GROUP',NGRP-1,10)",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_system_state_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "[1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0]",
            "[1,1,1,0,1,1,3,NGRP,NUNKNO,NMAT,1,0,0,0]",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_system_plane_identity_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "if (system_snapshot /= ip) return",
            "if (system_snapshot < 1) return",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_authority_inventory_call_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "if (.not. AUTHORITY_HAS_EXACT_PAYLOAD(plane_authority(ip))) return",
            "if (.not. c_associated(plane_authority(ip))) return",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_authority_inventory_count_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "item_count == 2 .and. &",
            "item_count >= 2 .and. &",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_source_mirror_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "real(authority_source64(iu),real32),0_int32",
            "real(authority_flux64(iu),real32),0_int32",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_representability_guard_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            "if (any(abs(authority_source64) > REAL32_MAX64)) return",
            "if (any(abs(authority_source64) > huge(0.0_real64))) return",
        )
        with self.assertRaises(GateError):
            check_archive_admission(bad)

    def test_write_before_preflight_rejected(self) -> None:
        bad = self.mutate_once(
            "status = SPOR64_B2I_ADMISSION_FAILED",
            "status = SPOR64_B2I_ADMISSION_FAILED\n"
            "    call LCMPUT(ipaxout,'EARLY',1,1,status)",
        )
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_whole_archive_clone_rejected(self) -> None:
        bad = self.mutate_once(
            "call LCMEQU(ipax,ipaxout)",
            "call LCMEQU(ipax,ipaxout)\n"
            "    call LCMEQU(iparchive,iparchiveout)",
        )
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_plane_epoch_before_state_rejected(self) -> None:
        old = """call LCMPUT(output_authority,'RHO',1,4,rho64)
      call LCMPTC(output_authority,'STATE',12,lifecycle_state)
      call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)"""
        new = """call LCMPUT(output_authority,'RHO',1,4,rho64)
      call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)
      call LCMPTC(output_authority,'STATE',12,lifecycle_state)"""
        bad = self.mutate_once(old, new)
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_root_epoch_not_last_rejected(self) -> None:
        old = "call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)"
        bad = self.mutate_last(old, old + "\n    call LCMPUT(iparchiveout,'LATE',1,1,status)")
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_commit_status_before_root_epoch_rejected(self) -> None:
        old = """call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)
    status = SPOR64_B2I_BOOTSTRAP_COMMITTED"""
        new = """status = SPOR64_B2I_BOOTSTRAP_COMMITTED
    call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)"""
        bad = self.mutate_once(old, new)
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_historical_root_diagnostic_copy_rejected(self) -> None:
        bad = self.mutate_once(
            "call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)",
            "call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)\n"
            "    call LCMPUT(iparchiveout,'SPOT-L1-ERR',1,2,keff32)",
        )
        with self.assertRaises(GateError):
            check_publication_boundary(bad)

    def test_empirical_alpha_declaration_rejected(self) -> None:
        bad = self.mutate_once(
            "integer :: allocation_status",
            "integer :: allocation_status\n    real(real64) :: alpha64",
        )
        with self.assertRaises(GateError):
            check_no_empirical_or_solver_path(bad)

    def test_qfiss_write_rejected(self) -> None:
        bad = self.mutate_once(
            "status = SPOR64_B2I_ADMISSION_FAILED",
            "status = SPOR64_B2I_ADMISSION_FAILED\n"
            "    call LCMPUT(iparchiveout,'QFISS',1,1,status)",
        )
        with self.assertRaises(GateError):
            check_no_empirical_or_solver_path(bad)

    def test_transport_call_rejected(self) -> None:
        bad = self.mutate_once(
            "status = SPOR64_B2I_ADMISSION_FAILED",
            "status = SPOR64_B2I_ADMISSION_FAILED\n    call FLUDRV()",
        )
        with self.assertRaises(GateError):
            check_no_empirical_or_solver_path(bad)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Mutation tests for the independent B2h projection-authority static gate."""

from __future__ import annotations

import unittest
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from check_phase_a9b_b2h_projection_authority import (
    GateError,
    check_all,
    check_no_empirical_controls,
    check_production_isolation,
    check_project,
    check_reconstruct,
    check_spoproj_stale_hazard,
    load_production_files,
)


ROOT = Path(__file__).resolve().parents[3]


class ProjectionAuthorityContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.b2h = (ROOT / "src/SPOR64_B2H.f90").read_text()
        cls.spoproj = (ROOT / "src/SPOPROJ.f90").read_text()
        cls.production = load_production_files(ROOT)

    def mutate_once(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation anchor count: {old}")
        return text.replace(old, new, 1)

    def test_current_contract(self) -> None:
        check_all(self.b2h, self.spoproj, self.production)

    def test_character_buffer_auto_reallocation_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "found(:) = ' '",
            "found = ' '",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_real64_basis_promotion_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "real(basis32(i,a),real64) * coordinates64(a)",
            "real(basis32(i,a),real32) * coordinates64(a)",
        )
        with self.assertRaises(GateError):
            check_reconstruct(bad)

    def test_contraction_loop_order_mutation_rejected(self) -> None:
        old = """do i = 1, size(projected64)
      do a = 1, size(coordinates64)"""
        new = """do a = 1, size(coordinates64)
      do i = 1, size(projected64)"""
        bad = self.mutate_once(self.b2h, old, new)
        with self.assertRaises(GateError):
            check_reconstruct(bad)

    def test_matmul_reassociation_mutation_rejected(self) -> None:
        old = """do i = 1, size(projected64)
      do a = 1, size(coordinates64)
        projected64(i) = projected64(i) + &
            real(basis32(i,a),real64) * coordinates64(a)
      end do
    end do"""
        new = "projected64 = matmul(real(basis32,real64),coordinates64)"
        bad = self.mutate_once(self.b2h, old, new)
        with self.assertRaises(GateError):
            check_reconstruct(bad)

    def test_seed_state_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "'SOLVED')) return",
            "'PROJECTED')) return",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_output_state_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "authority_state = 'PROJECTED'",
            "authority_state = 'SOLVED'",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_epoch_increment_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "output_epoch = seed_epoch + 1",
            "output_epoch = seed_epoch",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_epoch_overflow_guard_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "seed_epoch == huge(seed_epoch)",
            "seed_epoch > huge(seed_epoch)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_unused_state_slot_guard_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "if (any(state_vector(19:NSTATE) /= 0)) return",
            "if (any(state_vector(20:NSTATE) /= 0)) return",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_frozen_tolerance_bits_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "int(z'348637bd',int32)",
            "int(z'350637bd',int32)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_unused_tolerance_slot_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "eps_converge(4:5)",
            "eps_converge(5:5)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_authority_payload_type_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "call LCMPDL(output_flux,ig,NUNKNO,4,projected_flux64(:,ig))",
            "call LCMPDL(output_flux,ig,NUNKNO,2,projected_flux64(:,ig))",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_root_payload_type_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "call LCMPDL(legacy_flux,ig,NUNKNO,2,flux_stage32(:,ig))",
            "call LCMPDL(legacy_flux,ig,NUNKNO,4,flux_stage32(:,ig))",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_root_bypasses_downcast_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "call LCMPDL(legacy_flux,ig,NUNKNO,2,flux_stage32(:,ig))",
            "call LCMPDL(legacy_flux,ig,NUNKNO,2,projected_flux64(:,ig))",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_root_write_before_authority_mutation_rejected(self) -> None:
        anchor = "output_authority = LCMDID(ipout,'SPOT-R64')"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            "legacy_flux = LCMLID(ipout,'FLUX',NGRP)\n    " + anchor,
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_output_sour_creation_mutation_rejected(self) -> None:
        anchor = "output_flux = LCMLID(output_authority,'FLUX',NGRP)"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            anchor + "\n    output_flux = LCMLID(output_authority,'SOUR',NGRP)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_output_qfiss_creation_mutation_rejected(self) -> None:
        anchor = "legacy_flux = LCMLID(ipout,'FLUX',NGRP)"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            anchor + "\n    legacy_flux = LCMLID(ipout,'QFISS',NGRP)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_whole_seed_copy_mutation_rejected(self) -> None:
        anchor = "output_authority = LCMDID(ipout,'SPOT-R64')"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            "call LCMEQU(ipseed,ipout)\n    " + anchor,
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_seed_rho_republication_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "call LCMPUT(output_authority,'RHO',1,4,rho64)",
            "call LCMPUT(output_authority,'RHO',1,4,seed_rho64)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_keff_record_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.b2h,
            "call LCMPUT(output_authority,'RHO',1,4,rho64)",
            "call LCMPUT(output_authority,'KEFF',1,4,rho64)",
        )
        with self.assertRaises(GateError):
            check_project(bad)

    def test_empirical_relaxation_mutation_rejected(self) -> None:
        anchor = "integer :: i, a"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            anchor + "\n    real(real64) :: alpha",
        )
        with self.assertRaises(GateError):
            check_no_empirical_controls(bad)

    def test_physical_source_construction_mutation_rejected(self) -> None:
        anchor = "integer :: i, a"
        bad = self.mutate_once(
            self.b2h,
            anchor,
            anchor + "\n    real(real64) :: nusigf",
        )
        with self.assertRaises(GateError):
            check_no_empirical_controls(bad)

    def test_production_call_mutation_rejected(self) -> None:
        bad = dict(self.production)
        bad["src/FLU.f"] = bad["src/FLU.f"] + (
            "\n      CALL SPOR64_B2H_PROJECT(IPOUT,IPSEED,IPTRACK,P,K,S)\n"
        )
        with self.assertRaises(GateError):
            check_production_isolation(bad)

    def test_recursive_production_scan_rejects_nested_c2m_caller(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            nested = root / "data/shipped/nested"
            nested.mkdir(parents=True)
            caller = nested / "b2h_host.c2m"
            caller.write_text(
                "CALL SPOR64_B2H_PROJECT(IPOUT IPSEED IPTRACK P RHO STATUS);\n"
            )

            production = load_production_files(root)
            self.assertIn("data/shipped/nested/b2h_host.c2m", production)
            with self.assertRaises(GateError):
                check_production_isolation(production)

    def test_spoproj_authority_awareness_mutation_rejected(self) -> None:
        anchor = "jpplane=LCMGID(kpflux,'FLUX')"
        bad = self.mutate_once(
            self.spoproj,
            anchor,
            anchor + "\n    jpplane=LCMGID(kpflux,'SPOT-R64')",
        )
        with self.assertRaises(GateError):
            check_spoproj_stale_hazard(bad)

    def test_spoproj_type4_mutation_rejected(self) -> None:
        bad = self.mutate_once(
            self.spoproj,
            "call LCMPDL(jpplane,igr,nunk2d,2,u2d)",
            "call LCMPDL(jpplane,igr,nunk2d,4,u2d)",
        )
        with self.assertRaises(GateError):
            check_spoproj_stale_hazard(bad)


if __name__ == "__main__":
    unittest.main()

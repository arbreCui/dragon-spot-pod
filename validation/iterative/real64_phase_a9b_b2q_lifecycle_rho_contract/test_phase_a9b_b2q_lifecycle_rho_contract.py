#!/usr/bin/env python3
"""Mutation regressions for the B2q lifecycle/RHO static contract."""

from __future__ import annotations

import copy
import unittest

from check_phase_a9b_b2q_lifecycle_rho_contract import (
    GateError,
    RUNNER_PATH,
    check_all,
    check_b2b,
    check_b2c,
    check_b2h,
    check_b2i,
    check_b2j,
    check_b2k,
    check_b2n,
    check_b2o,
    check_manifest,
    check_runner,
    check_source_hashes,
    load_manifest,
    load_sources,
)


class LifecycleRhoContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = load_sources()
        cls.manifest = load_manifest()
        cls.runner = RUNNER_PATH.read_text(encoding="utf-8")

    def changed(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation anchor: {old}")
        return text.replace(old, new, 1)

    def reject_source(self, name: str, old: str, new: str, checker) -> None:
        mutated = self.changed(self.sources[name], old, new)
        with self.assertRaises(GateError):
            checker(mutated)

    def reject_manifest(self, path: tuple[str, ...], value) -> None:
        manifest = copy.deepcopy(self.manifest)
        owner = manifest
        for key in path[:-1]:
            owner = owner[key]
        owner[path[-1]] = value
        with self.assertRaises(GateError):
            check_manifest(manifest)

    def test_01_current_contract(self) -> None:
        check_all(self.sources, self.manifest, self.runner)

    def test_02_source_hash_change_rejected(self) -> None:
        sources = dict(self.sources)
        sources["src/SPOR64_B2H.f90"] += "\n! mutation\n"
        with self.assertRaises(GateError):
            check_source_hashes(sources, self.manifest)

    def test_03_parent_commit_change_rejected(self) -> None:
        self.reject_manifest(("parent_commit",), "0" * 40)

    def test_04_generation_owner_change_rejected(self) -> None:
        self.reject_manifest(
            ("generation_convention", "closed_n"),
            "SOLVED may introduce rho_n",
        )

    def test_05_b2h_canonical_overclaim_rejected(self) -> None:
        self.reject_manifest(("b2h_boundary", "direct_output_is_canonical"),
                             True)

    def test_06_epoch_iteration_claim_rejected(self) -> None:
        self.reject_manifest(("epoch_contract", "solver_iteration_counter"),
                             True)

    def test_07_missing_nonclaim_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["not_claimed"].remove("outer Picard convergence")
        with self.assertRaises(GateError):
            check_manifest(manifest)

    def test_08_b2i_reciprocal_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2I.f90",
            "1.0_real64/real(keff32,real64)",
            "2.0_real64/real(keff32,real64)",
            check_b2i,
        )

    def test_09_b2i_plane_rho_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2I.f90",
            "call LCMPUT(output_authority,'RHO',1,4,rho64)\n"
            "      call LCMPTC(output_authority,'STATE',12,lifecycle_state)",
            "call LCMPUT(output_authority,'RHO',1,4,1.0_real64)\n"
            "      call LCMPTC(output_authority,'STATE',12,lifecycle_state)",
            check_b2i,
        )

    def test_10_b2j_root_rho_tolerance_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2J.f90",
            "transfer(root_rho64,0_int64) /= transfer(rho64,0_int64)",
            "abs(root_rho64-rho64) > 1.0e-8_real64",
            check_b2j,
        )

    def test_11_b2j_plane_rho_tolerance_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2J.f90",
            "transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)",
            "abs(plane_rho64-rho64) > 1.0e-8_real64",
            check_b2j,
        )

    def test_12_b2j_projection_rho_owner_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2J.f90",
            "projected_region64(:,:,ip),rho64,b2h_status)",
            "projected_region64(:,:,ip),plane_rho64,b2h_status)",
            check_b2j,
        )

    def test_13_b2k_reciprocal_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2K.f90",
            "1.0_real64/iter_keff64",
            "iter_keff64",
            check_b2k,
        )

    def test_14_b2k_plane_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2K.f90",
            "transfer(plane_rho64,0_int64) /= &\n          transfer(rho64,0_int64)",
            "abs(plane_rho64-rho64) > 1.0e-8_real64",
            check_b2k,
        )

    def test_15_b2k_system_rho_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2K.f90",
            "call LCMPUT(staged_authority,'RHO',1,4,rho64)",
            "call LCMPUT(staged_authority,'RHO',1,4,1.0_real64)",
            check_b2k,
        )

    def test_16_b2n_reciprocal_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2N.f90",
            "1.0_real64/iter_keff64",
            "iter_keff64",
            check_b2n,
        )

    def test_17_b2n_rho_factor_removed_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2N.f90",
            "contribution64 = contribution64 * rho64",
            "contribution64 = contribution64",
            check_b2n,
        )

    def test_18_b2n_output_rho_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2N.f90",
            "call LCMPUT(source_authority,'RHO',1,4,rho64)",
            "call LCMPUT(source_authority,'RHO',1,4,1.0_real64)",
            check_b2n,
        )

    def test_19_b2o_reciprocal_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2O.f90",
            "1.0_real64/iter_keff64",
            "iter_keff64",
            check_b2o,
        )

    def test_20_b2o_source_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2O.f90",
            "transfer(source_rho64,0_int64) /= &\n        transfer(root_rho64,0_int64)",
            "abs(source_rho64-root_rho64) > 1.0e-8_real64",
            check_b2o,
        )

    def test_21_b2o_seed_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2O.f90",
            "transfer(seed_rho64,0_int64) /= &\n        transfer(root_rho64,0_int64)",
            "abs(seed_rho64-root_rho64) > 1.0e-8_real64",
            check_b2o,
        )

    def test_22_b2o_system_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2O.f90",
            "transfer(system_rho64,0_int64) /= &\n        transfer(root_rho64,0_int64)",
            "abs(system_rho64-root_rho64) > 1.0e-8_real64",
            check_b2o,
        )

    def test_23_b2o_loose_rho_argument_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2O.f90",
            "ipseed_out,ipsystem_out,status)",
            "ipseed_out,ipsystem_out,rho,status)",
            check_b2o,
        )

    def test_24_b2b_seed_source_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2B.f90",
            "transfer(seed_rho64,0_int64) /= &\n        transfer(source_rho64,0_int64)",
            "abs(seed_rho64-source_rho64) > 1.0e-8_real64",
            check_b2b,
        )

    def test_25_b2b_seed_system_identity_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2B.f90",
            "transfer(seed_rho64,0_int64) /= &\n        transfer(system_rho64,0_int64)",
            "abs(seed_rho64-system_rho64) > 1.0e-8_real64",
            check_b2b,
        )

    def test_26_b2b_admission_order_change_rejected(self) -> None:
        admission = (
            "    if (r64_mode == SPOR64_B2B_CONT) then\n"
            "      if (.not. CONT_LIFECYCLE_IS_BOUND(ipseed,ipsou,ipsys, &\n"
            "          seed_leak1d32,leak1d_input32)) return\n"
            "    end if\n"
        )
        mutated = self.changed(self.sources["src/SPOR64_B2B.f90"],
                               admission, "")
        mutated = self.changed(mutated, "    call XDRTA2\n",
                               "    call XDRTA2\n" + admission)
        with self.assertRaises(GateError):
            check_b2b(mutated)

    def test_27_b2c_rho_read_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2C.f90",
            "call LCMGET(lifecycle_authority,'RHO',lifecycle_rho64)",
            "lifecycle_rho64=1.0_real64",
            check_b2c,
        )

    def test_28_b2c_rho_write_change_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2C.f90",
            "call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)",
            "call LCMPUT(authority,'RHO',1,4,1.0_real64)",
            check_b2c,
        )

    def test_29_b2c_epoch_increment_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2C.f90",
            "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch)",
            "call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch+1)",
            check_b2c,
        )

    def test_30_b2h_seed_rho_substitution_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2H.f90",
            "call LCMPUT(output_authority,'RHO',1,4,rho64)",
            "call LCMPUT(output_authority,'RHO',1,4,seed_rho64)",
            check_b2h,
        )

    def test_31_b2h_epoch_increment_removed_rejected(self) -> None:
        self.reject_source(
            "src/SPOR64_B2H.f90",
            "output_epoch = seed_epoch + 1",
            "output_epoch = seed_epoch",
            check_b2h,
        )

    def test_32_runner_solver_injection_rejected(self) -> None:
        runner = self.runner + "\n$ROOT/bin/Darwin_arm64/Dragon\n"
        with self.assertRaises(GateError):
            check_runner(runner)

    def test_33_runner_fp_contract_removal_rejected(self) -> None:
        runner = self.changed(self.runner, "-ffp-contract=off", "")
        with self.assertRaises(GateError):
            check_runner(runner)

    def test_34_duplicate_archive_plane_owner_rejected(self) -> None:
        self.reject_manifest(
            ("plane_identity_contract", "archive_member_has_plane_record"),
            True,
        )


if __name__ == "__main__":
    unittest.main()

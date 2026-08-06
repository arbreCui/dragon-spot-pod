#!/usr/bin/env python3
"""High-value mutation tests for the B2f contract checker."""

from __future__ import annotations

import copy
import json
import unittest

from check_phase_a9b_b2f_fresh_host import (
    B2B,
    B2C,
    HARNESS,
    LEGACY_PLANE,
    LEGACY_REFERENCE,
    MANIFEST,
    PLANE,
    PROJECT_README,
    REFERENCE,
    RUNNER,
    STUBS,
    ContractError,
    check_b2b_text,
    check_b2c_text,
    check_global_publisher_callsites,
    check_harness_text,
    check_legacy_bytes,
    check_manifest_data,
    check_plane_text,
    check_readme_text,
    check_reference_text,
    check_runner_text,
    check_stub_text,
)


class B2fContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plane = PLANE.read_text()
        cls.reference = REFERENCE.read_text()
        cls.b2b = B2B.read_text()
        cls.b2c = B2C.read_text()
        cls.harness = HARNESS.read_text()
        cls.stubs = STUBS.read_text()
        cls.runner = RUNNER.read_text()
        cls.manifest = json.loads(MANIFEST.read_text())
        cls.readme = PROJECT_README.read_text()

    def reject_text(self, checker, text: str, old: str, new: str) -> None:
        changed = text.replace(old, new, 1)
        self.assertNotEqual(changed, text)
        with self.assertRaises(ContractError):
            checker(changed)

    def mutate_manifest(self, path: tuple[str, ...], value: object) -> None:
        changed = copy.deepcopy(self.manifest)
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        with self.assertRaises(ContractError):
            check_manifest_data(changed)

    def test_baseline(self) -> None:
        check_plane_text(self.plane)
        check_reference_text(self.reference)
        check_b2b_text(self.b2b)
        check_b2c_text(self.b2c)
        check_harness_text(self.harness)
        check_stub_text(self.stubs)
        check_runner_text(self.runner)
        check_manifest_data(self.manifest)
        check_readme_text(self.readme)

    def test_legacy_plane_is_immutable(self) -> None:
        changed = LEGACY_PLANE.read_bytes().replace(b"TYPE S", b"TYPE K", 1)
        with self.assertRaises(ContractError):
            check_legacy_bytes(changed, LEGACY_REFERENCE.read_bytes())

    def test_legacy_reference_is_immutable(self) -> None:
        changed = LEGACY_REFERENCE.read_bytes() + b"\n"
        with self.assertRaises(ContractError):
            check_legacy_bytes(LEGACY_PLANE.read_bytes(), changed)

    def test_plane_seed_cannot_be_removed(self) -> None:
        self.reject_text(check_plane_text, self.plane,
                         " FSOURCE FLUX_OLD ::", " FSOURCE ::")

    def test_plane_seed_order_is_frozen(self) -> None:
        self.reject_text(
            check_plane_text, self.plane,
            "MACRO0 TRACK TRACK_f SYSTEM FSOURCE FLUX_OLD",
            "FLUX_OLD MACRO0 TRACK TRACK_f SYSTEM FSOURCE",
        )

    def test_plane_init_on_is_required(self) -> None:
        self.reject_text(check_plane_text, self.plane,
                         "TYPE S INIT ON REBA", "TYPE S REBA")

    def test_plane_r64_is_required(self) -> None:
        self.reject_text(check_plane_text, self.plane,
                         "ACCE 3 3 R64", "ACCE 3 3")

    def test_plane_cannot_add_relaxation(self) -> None:
        self.reject_text(check_plane_text, self.plane,
                         "ACCE 3 3 R64", "ACCE 3 3 R64 RELAXATION 0.5")

    def test_reference_must_copy_seed(self) -> None:
        self.reject_text(check_reference_text, self.reference,
                         "FLUX_OLD := FLUX ;", "FLUX_OLD := DELETE: FLUX ;")

    def test_reference_must_delete_old_output(self) -> None:
        self.reject_text(check_reference_text, self.reference,
                         "FLUX := DELETE: FLUX ;", "ECHO \"KEEP FLUX\" ;")

    def test_reference_call_must_receive_seed(self) -> None:
        self.reject_text(check_reference_text, self.reference,
                         " TRACK_f FLUX_OLD ::", " TRACK_f ::")

    def test_b2b_requires_seven_entries(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "nentry /= 7", "nentry /= 6")

    def test_b2b_output_must_be_create(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "jentry(1) /= 0", "jentry(1) /= 1")

    def test_b2b_rhs_must_be_read_only(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "jentry(2:7) /= 2", "jentry(2:7) /= 1")

    def test_b2b_alias_guard_cannot_be_removed(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (c_associated(ipflux,kentry(ir))) return",
                         "continue")

    def test_b2b_empty_output_guard_cannot_be_removed(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (.not. output_lcm .or. ilong /= -1 .or. .not. output_empty) return",
                         "continue")

    def test_b2b_output_must_be_at_root(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (trim(output_name) /= '/') return",
                         "continue")

    def test_b2b_fresh_parser_state_is_frozen(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (rec .or. .not. limerg) return",
                         "if (.not. rec .or. limerg) return")

    def test_b2b_initial_flux_cannot_come_from_output(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "jpflux = LCMGID(ipseed,'FLUX')",
                         "jpflux = LCMGID(ipflux,'FLUX')")

    def test_b2b_fixed_source_cannot_come_from_seed(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "jpsource = LCMGID(ipsou,'DSOUR')",
                         "jpsource = LCMGID(ipseed,'SOUR')")

    def test_b2b_continuation_fallback_is_rejected(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (.not. ABSENT_RECORD(ipseed,'SPOT-R64')) return",
                         "continue")

    def test_b2b_stored_components_remain_three(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "MACRO_STORED_COMPONENTS = 3",
                         "MACRO_STORED_COMPONENTS = 1")

    def test_b2b_active_components_remain_one(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "TRACK_ACTIVE_COMPONENTS = 1",
                         "TRACK_ACTIVE_COMPONENTS = 3")

    def test_b2b_p1_shape_cannot_be_omitted(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "if (.not. RECORD_MATCHES(kpmacr,'NJJS01',NMAT,1)) return",
                         "continue")

    def test_b2b_cannot_load_inactive_scattering(self) -> None:
        self.reject_text(check_b2b_text, self.b2b,
                         "call LCMGET(kpmacr,'SCAT00',scat_stage32)",
                         "call LCMGET(kpmacr,'SCAT01',scat_stage32)")

    def test_b2b_cannot_write_lcm(self) -> None:
        changed = self.b2b.replace(
            "admission_complete = .true.",
            "call LCMPUT(ipflux,'BAD-WRITE',1,1,frozen_flag)\n"
            "    admission_complete = .true.",
            1,
        )
        self.assertNotEqual(changed, self.b2b)
        with self.assertRaises(ContractError):
            check_b2b_text(changed)

    def test_b2c_requires_empty_root(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "if (.not. EMPTY_LCM_ROOT(ipflux)) return",
                         "continue")

    def test_b2c_target_must_be_at_root(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "trim(object_name) == '/'",
                         ".true.")

    def test_b2c_named_lists_must_be_created(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "legacy_flux = LCMLID(ipflux,'FLUX',NGRP)",
                         "legacy_flux = LCMGID(ipflux,'FLUX')")

    def test_b2c_authority_must_be_type_four(self) -> None:
        self.reject_text(
            check_b2c_text, self.b2c,
            "LCMPDL(authority_flux,ig,NUNKNO,4,terminal_flux64(:,ig))",
            "LCMPDL(authority_flux,ig,NUNKNO,2,terminal_flux64(:,ig))",
        )

    def test_b2c_compatibility_must_be_type_two(self) -> None:
        self.reject_text(
            check_b2c_text, self.b2c,
            "LCMPDL(legacy_flux,ig,NUNKNO,2,flux_stage32(:,ig))",
            "LCMPDL(legacy_flux,ig,NUNKNO,4,flux_stage32(:,ig))",
        )

    def test_b2c_conversion_must_precede_first_write(self) -> None:
        changed = self.b2c.replace(
            "    flux_stage32 = real(terminal_flux64,real32)\n", "", 1
        ).replace(
            "    authority = LCMDID(ipflux,'SPOT-R64')",
            "    authority = LCMDID(ipflux,'SPOT-R64')\n"
            "    flux_stage32 = real(terminal_flux64,real32)",
            1,
        )
        self.assertNotEqual(changed, self.b2c)
        with self.assertRaises(ContractError):
            check_b2c_text(changed)

    def test_b2c_signature_cannot_be_omitted(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "call LCMPTC(ipflux,'SIGNATURE',12,signature)",
                         "continue")

    def test_b2c_merge_map_cannot_be_omitted(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "call LCMPUT(ipflux,'IMERGE-LEAK',NMAT,1,imerge_input)",
                         "continue")

    def test_b2c_final_status_must_be_host_commit(self) -> None:
        self.reject_text(check_b2c_text, self.b2c,
                         "status = SPOR64_B2C_HOST_COMMITTED",
                         "status = SPOR64_B2C_DRIVER_COMMITTED")

    def test_publisher_cannot_gain_second_production_caller(self) -> None:
        changed_flu = "      CALL SPOR64_B2C_PUBLISH(BAD)\n" + (
            PROJECT_README.parent / "src/FLU.f"
        ).read_text()
        with self.assertRaises(ContractError):
            check_global_publisher_callsites({"FLU.f": changed_flu})

    def test_harness_character_check_cannot_ignore_padding(self) -> None:
        self.reject_text(check_harness_text, self.harness,
                         "if (found /= expected) error stop 'character record differs'",
                         "if (found(1:len(expected)) /= expected) error stop 'character record differs'")

    def test_stub_cannot_fabricate_a_model_update(self) -> None:
        self.reject_text(check_stub_text, self.stubs,
                         "terminal_flux64 = initial_flux64",
                         "terminal_flux64 = 0.5_real64*initial_flux64")

    def test_runner_cannot_compile_real_core(self) -> None:
        with self.assertRaises(ContractError):
            check_runner_text(self.runner + '\n"$FC" -c "$ROOT/src/SPOR64_A9.f90"\n')

    def test_runner_cannot_execute_dragon(self) -> None:
        with self.assertRaises(ContractError):
            check_runner_text(self.runner + '\n"$ROOT/bin/Darwin_arm64/Dragon"\n')

    def test_manifest_default_cannot_be_enabled(self) -> None:
        self.mutate_manifest(("default_off", "r64_default"), True)

    def test_manifest_cannot_claim_continuous_iteration(self) -> None:
        self.mutate_manifest(("host_contract", "continuous_REAL64_iteration"), True)

    def test_manifest_cannot_add_relaxation(self) -> None:
        self.mutate_manifest(("scope", "relaxation_parameters_added"), True)

    def test_manifest_cannot_claim_transport(self) -> None:
        self.mutate_manifest(("execution_evidence", "transport_solves"), 1)

    def test_manifest_cannot_claim_radial_convergence(self) -> None:
        self.mutate_manifest(("status", "radial_convergence"), "PASSED")

    def test_manifest_cannot_claim_outer_convergence(self) -> None:
        self.mutate_manifest(("status", "outer_picard_convergence"), "PASSED")

    def test_readme_cannot_drop_bootstrap_boundary(self) -> None:
        self.reject_text(
            check_readme_text, self.readme,
            "first fresh-output REAL64 bootstrap contract only",
            "continuous REAL64 Picard convergence contract",
        )


if __name__ == "__main__":
    unittest.main()

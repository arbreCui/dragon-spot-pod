#!/usr/bin/env python3
"""Independent mutation tests for the Phase-A9a static contract."""

from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

import check_phase_a9 as check


class PhaseA9ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(check.MANIFEST.read_text())
        cls.core = check.CORE.read_text()
        cls.host = check.HOST.read_text()
        cls.runner = check.RUNNER.read_text()
        cls.makefile = check.MAKEFILE.read_text()
        cls.readme = check.README.read_text()
        cls.root_readme = check.ROOT_README.read_text()
        cls.iterative_readme = check.ITERATIVE_README.read_text()

    def reject(self, validator, value, label: str) -> None:
        with self.subTest(label=label):
            with self.assertRaises(check.PhaseA9Error):
                validator(value)

    def changed(self, source: str, old: str, new: str,
                count: int = 1) -> str:
        self.assertEqual(source.count(old), count,
                         f"mutation anchor count changed: {old!r}")
        return source.replace(old, new, count)

    def test_live_nohash_contracts_pass(self) -> None:
        check.validate_manifest(self.manifest, verify_hashes=False)
        check.validate_core_source(self.core)
        check.validate_host_source(self.host)
        check.validate_runner_contract(self.runner, verify_hash=False)
        check.validate_makefile_contract(self.makefile)
        check.validate_docs(self.readme, self.root_readme,
                            self.iterative_readme)

    def test_a8_receipt_identity_is_live(self) -> None:
        self.assertEqual(check.sha256(check.A8_RECEIPT),
                         check.EXPECTED_A8_RECEIPT_SHA256)

    def test_production_tree_is_unchanged(self) -> None:
        check.validate_production_tree_unchanged()

    def test_manifest_claim_mutations_are_rejected(self) -> None:
        mutations = (
            ("continuous lane overclaim",
             ("status", "continuous_real64_lane"), True),
            ("radial convergence overclaim",
             ("status", "radial_convergence"), "CONVERGED"),
            ("production route overclaim",
             ("status", "production_route_connected"), True),
            ("complete A9 overclaim",
             ("split", "complete_A9_claim_allowed"), True),
            ("operator precision drift",
             ("precision_contract", "operator_storage"), "real(real64)"),
            ("terminal weakening",
             ("terminal", "exact_boolean"), "EUNK64<EPSUNK64"),
            ("default route enabled",
             ("selector_seam", "default_real64_route"), True),
            ("fallback enabled",
             ("selector_seam", "fallback_after_real64_selection"), True),
            ("negative count drift",
             ("compile_gate", "negative_contract_count"), 6),
            ("root handle admitted",
             ("runtime_handle_precondition", "required_identity"),
             "root L_PIJ object"),
            ("XCSOU relabelled inner",
             ("a7_wording_correction", "correct_role"),
             "integrated inner source"),
        )
        for label, path, replacement in mutations:
            data = copy.deepcopy(self.manifest)
            data[path[0]][path[1]] = replacement
            self.reject(lambda value: check.validate_manifest(
                value, verify_hashes=False), data, label)

    def test_core_slice_and_source_mutations_are_rejected(self) -> None:
        mutations = (
            ("seven slices", "integer, parameter :: NSLICE = 8",
             "integer, parameter :: NSLICE = 7"),
            ("eager old outer history",
             "flux64(:,:,2) = initial_flux64",
             "flux64(:,:,1) = initial_flux64\n    "
             "flux64(:,:,2) = initial_flux64"),
            ("wrong XCSOU slice", "flux64(ind,ig,4) * &",
             "flux64(ind,ig,8) * &"),
            ("weak first source admission", "xcsou64(1) <= 0.0_real64",
             "xcsou64(1) < 0.0_real64"),
            ("self scattering admitted", "if (jg /= ig) then",
             "if (jg == ig) then"),
            ("wrong source coefficient", "ipos_off(ibm,ig) + "
             "ijj_off(ibm,ig) - jg", "ipos_off(ibm,ig) + "
             "ijj_off(ibm,ig) - ig"),
            ("wrong offgroup source slice", "flux64(ind,jg,7)",
             "flux64(ind,jg,6)"),
            ("wrong inner history shift", "flux64(:,ig,5) = "
             "flux64(:,ig,6)", "flux64(:,ig,5) = flux64(:,ig,7)"),
            ("wrong outer history shift", "flux64(:,ig,1) = "
             "flux64(:,ig,2)", "flux64(:,ig,1) = flux64(:,ig,3)"),
            ("GROUP handle lost", "call DOORFV64(jpsys_group,",
             "call DOORFV64(iptrk,"),
        )
        for label, old, new in mutations:
            self.reject(check.validate_core_source,
                        self.changed(self.core, old, new), label)

    def test_core_call_order_mutation_is_rejected(self) -> None:
        source = self.changed(self.core, "call DOORFV64(",
                              "call TEMP_A9(")
        source = self.changed(source, "call FLUBAL64(", "call DOORFV64(")
        source = self.changed(source, "call TEMP_A9(", "call FLUBAL64(")
        self.reject(check.validate_core_source, source,
                    "DOORFV64/FLUBAL64 order swapped")

    def test_inner_state_mutations_are_rejected(self) -> None:
        mutations = (
            ("weak strict comparison", "if (einr64 < epsinr64) then",
             "if (einr64 <= epsinr64) then"),
            ("near accepts as strict", "iinr_state = IINR_NEAR",
             "iinr_state = IINR_STRICT"),
            ("near coefficient changed", "10.0_real64*epsinr64",
             "1.0_real64*epsinr64"),
            ("prefix can skip", "igdeb == ig", "igdeb <= ig"),
            ("cap accepted", "iinr_state = IINR_CAP",
             "iinr_state = IINR_STRICT"),
        )
        for label, old, new in mutations:
            self.reject(check.validate_core_source,
                        self.changed(self.core, old, new), label)

    def test_flubal_physics_mutations_are_rejected(self) -> None:
        mutations = (
            ("RHS no longer XCSOU", "= xcsou64(igr)",
             "= +0.0_real64"),
            ("surface sign changed", "1.0_real64-real(albedo32",
             "1.0_real64+real(albedo32"),
            ("IFSCAT off by one", "- njj_off(ibm,igr) + 1",
             "- njj_off(ibm,igr)"),
            ("converged RHS sign changed",
             "rebal64(ioff,ngreb+1) + &",
             "rebal64(ioff,ngreb+1) - &"),
            ("reaction diagonal sign changed",
             "real(xstrc32(ibm,igr),real64) - &",
             "real(xstrc32(ibm,igr),real64) + &"),
            ("offdiagonal sign changed",
             "rebal64(ioff,jgr-igdeb+1) - flux64",
             "rebal64(ioff,jgr-igdeb+1) + flux64"),
            ("REAL32 ALSB substituted", "call ALSBD(ngreb,1,",
             "call ALSB(ngreb,1,"),
            ("solver error ignored", "if (ier /= 0) return",
             "if (ier == 0) return"),
            ("factor misses unknowns", "do ind = 1, NUNKNO",
             "do ind = 1, 1"),
        )
        for label, old, new in mutations:
            self.reject(check.validate_core_source,
                        self.changed(self.core, old, new), label)

    def test_flu2ac_formula_mutations_are_rejected(self) -> None:
        mutations = (
            ("R1 reversed", "flux64(ir,ig,2) - flux64(ir,ig,1)",
             "flux64(ir,ig,1) - flux64(ir,ig,2)"),
            ("numerator sign changed", "r1_64*(r2_64-r1_64)",
             "r1_64*(r2_64+r1_64)"),
            ("mu sign changed", "dmu64 = -nom64/denom64",
             "dmu64 = nom64/denom64"),
            ("zero denominator threshold changed",
             "if (denom64 <= 0.0_real64) then",
             "if (denom64 <= 1.0_real64) then"),
            ("new update drifts", "flux64(ir,ig,2) + dmu64 * &",
             "flux64(ir,ig,2) - dmu64 * &"),
            ("present update drifts", "flux64(ir,ig,1) + dmu64 * &",
             "flux64(ir,ig,1) - dmu64 * &"),
            ("AKEEP new update drifts", "akeep64(2) + dmu64*",
             "akeep64(2) - dmu64*"),
            ("AKEEP present update drifts", "akeep64(1) + dmu64*",
             "akeep64(1) - dmu64*"),
        )
        for label, old, new in mutations:
            self.reject(check.validate_core_source,
                        self.changed(self.core, old, new), label)

    def test_norm_and_terminal_mutations_are_rejected(self) -> None:
        mutations = (
            ("norm denominator uses present", "abs(new64(ind))",
             "abs(present64(ind))"),
            ("norm gets empirical floor",
             "group_error64 = group_error64/denominator64",
             "denominator64 = max(denominator64,0.5_real64)\n    "
             "group_error64 = group_error64/denominator64"),
            ("terminal EUNK weak", "eunk64 < epsunk64",
             "eunk64 <= epsunk64"),
            ("terminal iteration weakened", "outer_iteration >= 2",
             "outer_iteration >= 1"),
        )
        for label, old, new in mutations:
            self.reject(check.validate_core_source,
                        self.changed(self.core, old, new), label)

    def test_dead_branch_and_postoverwrite_are_rejected(self) -> None:
        dead = self.changed(
            self.core, "contains\n", "contains\n\n  if (.false.) continue\n")
        self.reject(check.validate_core_source, dead, "dead branch")
        overwrite = self.changed(
            self.core, "  end subroutine FLU2AC64",
            "    flux64(:,:,3) = flux64(:,:,1)\n"
            "  end subroutine FLU2AC64")
        self.reject(check.validate_core_source, overwrite,
                    "post-formula overwrite")
        source_overwrite = self.changed(
            self.core, "      if (.not. all(ieee_is_finite(xcsou64))) return",
            "      xcsou64(1) = +0.0_real64\n"
            "      if (.not. all(ieee_is_finite(xcsou64))) return")
        self.reject(check.validate_core_source, source_overwrite,
                    "source post-overwrite")
        dmu_overwrite = self.changed(
            self.core, "    if (.not. ieee_is_finite(dmu64)) return",
            "    dmu64 = 1.0_real64\n"
            "    if (.not. ieee_is_finite(dmu64)) return")
        self.reject(check.validate_core_source, dmu_overwrite,
                    "acceleration-control post-overwrite")

    def test_host_mutations_are_rejected(self) -> None:
        mutations = (
            ("default on", "DEFAULT_REAL64_ROUTE = .false.",
             "DEFAULT_REAL64_ROUTE = .true."),
            ("implicit selection", "if (requested) selected_real64 = .true.",
             "selected_real64 = .true."),
            ("fallback enabled", "      return\n    end if",
             "    end if"),
            ("status forged", "route_ok = .false.",
             "route_ok = .true."),
        )
        for label, old, new in mutations:
            self.reject(check.validate_host_source,
                        self.changed(self.host, old, new), label)
        post = self.changed(
            self.host, "    call legacy_callback(route_ok)",
            "    selected_real64 = .false.\n"
            "    call legacy_callback(route_ok)")
        self.reject(check.validate_host_source, post,
                    "selector post-overwrite")
        downcast = self.changed(
            self.host,
            "real(real64), intent(inout), contiguous :: state64(:)",
            "real(real32), intent(inout), contiguous :: state64(:)",
            count=2)
        self.reject(check.validate_host_source, downcast,
                    "selector state downcast")

    def test_runner_mutations_are_rejected(self) -> None:
        mutations = (
            ("Dragon command admitted", "echo \"SPOR64 PHASE-A9a "
             "COMPILE-ONLY OUTER CLOSURE PASS\"",
             "Dragon case.x2m\n"
             "echo \"SPOR64 PHASE-A9a COMPILE-ONLY OUTER CLOSURE PASS\""),
            ("convergence overclaim", "RADIAL-CONVERGENCE=NOT-EVALUATED",
             "RADIAL-CONVERGENCE=CONVERGED"),
            ("negative removed", "compile_fail_real32_terminal.f90",
             "compile_fail_missing_terminal.f90"),
        )
        for label, old, new in mutations:
            self.reject(lambda value: check.validate_runner_contract(
                value, verify_hash=False), self.changed(self.runner, old, new),
                label)
        no_compile_only = self.changed(
            self.runner,
            '"$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"',
            '"$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" "$1" -o "$2"')
        self.reject(lambda value: check.validate_runner_contract(
            value, verify_hash=False), no_compile_only,
            "compiler action can link")

    def test_make_and_document_overclaims_are_rejected(self) -> None:
        make = self.changed(self.makefile, "spot-real64-phase-a9a :",
                            "spot-real64-phase-a9a : spot-fast")
        self.reject(check.validate_makefile_contract, make,
                    "hidden Make prerequisite")
        self.reject(lambda value: check.validate_docs(
            value, self.root_readme, self.iterative_readme),
            self.readme + "\nRadial solver converged.\n",
            "radial convergence prose")

    def test_receipt_scope_is_exact_ordered_and_nonrecursive(self) -> None:
        paths = ("a", "b")
        valid = "0" * 64 + "  a\n" + "1" * 64 + "  b\n"
        with mock.patch.object(check, "EXPECTED_RECEIPT_PATHS", paths):
            check.validate_receipt_scope(valid)
            for label, bad in (
                ("reordered", "1" * 64 + "  b\n" + "0" * 64 + "  a\n"),
                ("malformed", "0" * 64 + " a\n" + "1" * 64 + "  b\n"),
            ):
                self.reject(check.validate_receipt_scope, bad, label)
        duplicate = "0" * 64 + "  a\n" + "1" * 64 + "  a\n"
        with mock.patch.object(check, "EXPECTED_RECEIPT_PATHS", ("a", "a")):
            self.reject(check.validate_receipt_scope, duplicate, "duplicate")
        self_path = (
            "validation/iterative/real64_phase_a9/"
            "phase_a9a_implementation_receipt.sha256"
        )
        recursive = "0" * 64 + "  " + self_path + "\n"
        with mock.patch.object(check, "EXPECTED_RECEIPT_PATHS", (self_path,)):
            self.reject(check.validate_receipt_scope, recursive,
                        "receipt self-cycle")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Mutation tests for the Phase-A8 compile-only inner closure."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Callable

from check_phase_a8 import (
    ACA,
    ADAPTER,
    CORE,
    HERE,
    MANIFEST,
    PhaseA8Error,
    ROOT,
    RUNNER,
    validate,
    validate_aca_source,
    validate_adapter_source,
    validate_core_source,
    validate_makefile_contract,
    validate_runner_contract,
)


class PhaseA8ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text())
        cls.core = CORE.read_text()
        cls.aca = ACA.read_text()
        cls.adapter = ADAPTER.read_text()
        cls.makefile = (ROOT / "Makefile").read_text()
        cls.runner = RUNNER.read_text()

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.manifest)
        mutate(candidate)
        with self.assertRaises(PhaseA8Error):
            validate(candidate, verify_hashes=False)

    def core_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.core)
        with self.assertRaises(PhaseA8Error):
            validate_core_source(mutated)

    def replace_ci_once(self, source: str, old: str, new: str) -> str:
        mutated, count = re.subn(
            re.escape(old), new, source, count=1, flags=re.IGNORECASE
        )
        self.assertEqual(count, 1, old)
        return mutated

    def replace_ci_all(self, source: str, old: str, new: str) -> str:
        mutated, count = re.subn(
            re.escape(old), new, source, flags=re.IGNORECASE
        )
        self.assertGreater(count, 0, old)
        return mutated

    def aca_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.aca)
        with self.assertRaises(PhaseA8Error):
            validate_aca_source(mutated)

    def adapter_rejected(self, mutated: str) -> None:
        self.assertNotEqual(mutated, self.adapter)
        with self.assertRaises(PhaseA8Error):
            validate_adapter_source(mutated)

    def test_unfrozen_contract_passes_semantically(self) -> None:
        validate(copy.deepcopy(self.manifest), verify_hashes=False)

    def test_status_cannot_overclaim_runtime_or_convergence(self) -> None:
        changes = (
            ("link_authorized", True),
            ("execution_authorized", True),
            ("production_source_changes", 1),
            ("production_route_connected", True),
            ("default_runtime_route_changed", True),
            ("spomoc_capture64_implemented", True),
            ("runtime_provenance_validated", True),
            ("tracking_position_validated", True),
            ("actual_transport_response_validated", True),
            ("continuous_real64_lane", True),
            ("radial_convergence", "CONVERGED"),
            ("outer_picard_convergence", "CONVERGED"),
            ("object_links", 1),
            ("object_executions", 1),
            ("tracking_reads", 1),
            ("transport_solves", 1),
            ("dragon_runs", 1),
        )
        for field, value in changes:
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["status"].__setitem__(field, value)
                )

    def test_status_abi_cannot_drop_or_narrow_results(self) -> None:
        self.rejected(
            lambda data: data["a8_addendum"]["status_abi"].__setitem__(
                "nodes", data["a8_addendum"]["status_abi"]["nodes"][:-1]
            )
        )
        self.rejected(
            lambda data: data["a8_addendum"]["status_abi"].__setitem__(
                "counter_dummy", "integer, intent(out) :: CUTOFF_DELTA64"
            )
        )

    def test_capture_boundary_stays_unresolved_until_a9(self) -> None:
        self.rejected(
            lambda data: data["a8_addendum"]["capture_boundary"].__setitem__(
                "checked_a8_signature",
                "SPOMOC_CAPTURE64(NGEFF,NGIND,QFR64,EVAL64,"
                "SOURCE64,RAW64,NCONV)",
            )
        )
        self.rejected(
            lambda data: data["a8_addendum"]["capture_boundary"].__setitem__(
                "src_spomoc_changes_in_a8", 1
            )
        )
        self.rejected(
            lambda data: data["a8_addendum"]["capture_boundary"].__setitem__(
                "solver_feedback", True
            )
        )

    def test_ddot_identity_and_reuse_are_frozen(self) -> None:
        self.rejected(
            lambda data: data["a8_addendum"]["ddot_reuse"].__setitem__(
                "sha256", "0" * 64
            )
        )
        self.rejected(
            lambda data: data["a8_addendum"]["ddot_reuse"].__setitem__(
                "replacement_by_intrinsic_allowed", True
            )
        )

    def test_locked_numerical_controls_cannot_change(self) -> None:
        for field, value in (
            ("KRYL", 0), ("IAAC", 0), ("PACA", 3), ("MAXI", 21),
            ("NSTART", 11), ("MAXIT", 20), ("MAXACC", 201),
            ("LFORW", False), ("MACFLG", True), ("COMBFLG", True),
        ):
            with self.subTest(field=field):
                self.rejected(
                    lambda data, field=field, value=value:
                    data["locked_branch"].__setitem__(field, value)
                )

    def test_precision_rank_and_aca_shortcuts_are_rejected(self) -> None:
        self.rejected(
            lambda data: data["precision_contract"].__setitem__(
                "mutable_real64_to_real32_allowed", True
            )
        )
        self.rejected(
            lambda data: data["rank_contract"].__setitem__(
                "flat_or_sequence_association_allowed", True
            )
        )
        self.rejected(
            lambda data: data["aca_contract"].__setitem__(
                "MCGPRA64_IM", "IM(NLONG)"
            )
        )
        self.rejected(
            lambda data: data["aca_contract"].__setitem__(
                "CF32", "CF32(N1)"
            )
        )
        self.rejected(
            lambda data: data["aca_contract"].__setitem__(
                "JU_partition_bounds", "unchecked"
            )
        )
        self.rejected(
            lambda data: data["aca_contract"].__setitem__(
                "biCGSTAB_rho_breakdown", "reject non-positive"
            )
        )
        self.rejected(
            lambda data: data["record_admission"].__setitem__(
                "tracking_stream_entry",
                "rewind -> header/comments -> five skipped records",
            )
        )
        self.rejected(
            lambda data: data["record_admission"]["mcgsig"].__setitem__(
                "ICODE_semantics", "reject negative ICODE"
            )
        )

    def test_core_rejects_removed_call_chain_nodes(self) -> None:
        for token in (
            "call MCGSIG", "call MCGFLX64", "call MCGMRE64",
            "call MCGFCS64", "call MOCIK3", "call MCGFCF",
            "call MCGFST", "call SPOMOC_CAPTURE64", "call MCGFCA64",
        ):
            with self.subTest(token=token):
                self.core_rejected(
                    self.replace_ci_once(self.core, token, "call OMITTED")
                )

    def test_core_rejects_mutable_downcast_and_legacy_diagnostics(self) -> None:
        marker = "end module SPOR64_A8"
        self.core_rejected(
            self.core.replace(marker, "x32 = real(x64, real32)\n" + marker)
        )
        self.core_rejected(self.core.replace("PRINDM", "PRINAM", 1))

    def test_core_rejects_downstream_sc_gather(self) -> None:
        region = "subroutine MCGFL164"
        self.core_rejected(
            self.core.replace(region, region + " ! DRAGON-S0XSC", 1)
        )

    def test_core_rejects_mask_reactivation(self) -> None:
        old = "nconv(ii) = nconv(ii) .and."
        self.assertIn(old, self.core.lower())
        mutated = self.core.lower().replace(old, "nconv(ii) =", 1)
        self.core_rejected(mutated)

    def test_mre_rejects_role_or_response_actual_drift(self) -> None:
        cases = (
            (
                "call SPOMOC_SET_ROLE(2, iter)",
                "call SPOMOC_SET_ROLE(3, iter)",
            ),
            (
                "qfr64, rhs64, source64, flout64",
                "qfr64, phiin64, source64, flout64",
            ),
            (
                "qfr64, gar64, source64, flout64",
                "qfr64, rhs64, source64, flout64",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mre_rejects_rhs_residual_or_arnoldi_drift(self) -> None:
        cases = (
            ("rhs_pending = .false.", "rhs_pending = .true."),
            (
                "response64(:,ii) - phiin64(:,ii)",
                "response64(:,ii) + phiin64(:,ii)",
            ),
            (
                "v64(:,:,k) - flout64 + rhs64",
                "v64(:,:,k) + flout64 + rhs64",
            ),
            (
                "if (nconv(ii)) rhs64(:,ii) = flout64(:,ii)",
                "rhs64(:,ii) = flout64(:,ii)",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mre_rejects_mgs_givens_or_backsolve_drift(self) -> None:
        cases = (
            (
                "h64(j,k,ii) = h64(j,k,ii) + hr64",
                "h64(j,k,ii) = h64(j,k,ii) - hr64",
            ),
            (
                "w1 = c64(i,ii) * h64(i,k,ii) - &",
                "w1 = c64(i,ii) * h64(i,k,ii) + &",
            ),
            (
                "sn64(k,ii) = -h64(k+1,k,ii) / znu64",
                "sn64(k,ii) = h64(k+1,k,ii) / znu64",
            ),
            ("k = kmax(ii)", "k = NSTART"),
            (
                "phiin64(:,ii) = phiin64(:,ii) + &",
                "phiin64(:,ii) = phiin64(:,ii) - &",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_core_rejects_eight_simple_semantic_bypasses(self) -> None:
        cases: list[tuple[str, str]] = []

        old = "        rhs_pending = .false.\n"
        new = (
            old
            + "        associate (pending_again => rhs_pending)\n"
            + "          pending_again = .true.\n"
            + "        end associate\n"
        )
        cases.append((
            "RHS alias overwrite",
            self.replace_ci_once(self.core, old, new),
        ))

        start = self.core.index(
            "          ! Second modified Gram-Schmidt pass "
            "(reorthogonalization)."
        )
        end = self.core.index(
            "          if (h64(k+1,k,ii) > 0.0_real64) then", start
        )
        second_mgs = self.core[start:end]
        cases.append((
            "dead second MGS",
            self.core[:start]
            + "          if (.false.) then\n"
            + second_mgs
            + "          end if\n"
            + self.core[end:],
        ))

        old = "            sn64(k,ii) = -h64(k+1,k,ii) / znu64\n"
        new = old + "            sn64(k,ii) = h64(k+1,k,ii) / znu64\n"
        cases.append((
            "Givens post-overwrite",
            self.replace_ci_once(self.core, old, new),
        ))

        old = (
            "          phiin64(:,ii) = phiin64(:,ii) + &\n"
            "              g64(j,ii) * v64(:,ii,j)\n"
        )
        new = (
            old
            + "          phiin64(:,ii) = phiin64(:,ii) - &\n"
            + "              2.0_real64 * g64(j,ii) * v64(:,ii,j)\n"
        )
        cases.append((
            "backsolve post-overwrite",
            self.replace_ci_once(self.core, old, new),
        ))

        old = (
            "    if (state_vector(9) /= 0 .or. "
            "state_vector(14) /= 4) return\n"
        )
        new = (
            "    if (.false.) then\n"
            + old
            + "    end if\n"
            + "    if (state_vector(9) /= 0 .or. "
            + "state_vector(14) /= 3) return\n"
        )
        cases.append((
            "dead STATE guard decoy",
            self.replace_ci_once(self.core, old, new),
        ))

        old = (
            "        if (.not. RECORD_MATCHES(kpsys(i), 'PJJ$MCCG', &\n"
            "            NREG*NFUNL, 2)) return\n"
        )
        new = (
            "        if (.false.) then\n"
            + old
            + "        end if\n"
            + "        if (.not. RECORD_MATCHES(kpsys(i), "
            + "'PJJ$MCCG', &\n"
            + "            NFUNL, 2)) return\n"
        )
        cases.append((
            "dead PJJ guard decoy",
            self.replace_ci_once(self.core, old, new),
        ))

        old = (
            "    if (keyani(1) /= 0 .or. "
            ".not. all(isgnr(:,1) == 1)) return\n"
        )
        new = (
            "    if (.false.) then\n"
            + old
            + "    end if\n"
            + "    if (keyani(1) /= 1 .or. "
            + ".not. all(isgnr(:,1) == 1)) return\n"
        )
        cases.append((
            "dead MOCIK guard decoy",
            self.replace_ci_once(self.core, old, new),
        ))

        old = (
            "        s64(ind) = qn64(ind) + &\n"
            "            real(sc32(ibm,1), real64) * fi64(ind)\n"
        )
        new = (
            old
            + "        associate (source_alias => s64(ind))\n"
            + "          source_alias = qn64(ind) - &\n"
            + "              real(sc32(ibm,1), real64) * fi64(ind)\n"
            + "        end associate\n"
        )
        cases.append((
            "FCS alias overwrite",
            self.replace_ci_once(self.core, old, new),
        ))

        self.assertEqual(len(cases), 8)
        for label, mutated in cases:
            with self.subTest(label=label):
                self.core_rejected(mutated)

    def test_core_rejects_block_math_wrapper(self) -> None:
        old = "    rhs_pending = .true.\n"
        new = old + "    block\n    end block\n"
        self.core_rejected(
            self.replace_ci_once(self.core, old, new)
        )

        start = self.core.index(
            "          ! Second modified Gram-Schmidt pass "
            "(reorthogonalization)."
        )
        end = self.core.index(
            "          if (h64(k+1,k,ii) > 0.0_real64) then", start
        )
        second_mgs = self.core[start:end]
        self.core_rejected(
            self.core[:start]
            + "          if (1 == 0) then\n"
            + second_mgs
            + "          end if\n"
            + self.core[end:]
        )

    def test_mre_rejects_cap_or_convergence_predicate_drift(self) -> None:
        self.core_rejected(
            self.replace_ci_once(
                self.core, "iter < MAXIT", "iter <= MAXIT"
            )
        )
        self.core_rejected(
            self.replace_ci_once(
                self.core,
                "rho64(ii) >= epsi64 * denom64(ii)",
                "rho64(ii) > epsi64 * denom64(ii)",
            )
        )
        marker = (
            "    lnconv = count(nconv)\n"
            "    if (.not. all(ieee_is_finite(phiin64))) return"
        )
        injected = (
            "    if (iter == MAXIT) return\n" + marker
        )
        self.core_rejected(
            self.replace_ci_once(self.core, marker, injected)
        )

    def test_mccgf_rejects_frozen_state_or_real_parameter_drift(self) -> None:
        cases = (
            ("state_vector(14) /= 4", "state_vector(14) /= 3"),
            ("mccg_state(7) /= IAAC", "mccg_state(7) /= 79"),
            (
                "transfer(real_param32(1), 0_int32) /= "
                "int(z'3727c5ac',int32)",
                "transfer(real_param32(1), 0_int32) /= "
                "int(z'3727c5ad',int32)",
            ),
            (
                "transfer(real_param32(4), 0_int32) /= 0_int32",
                "transfer(real_param32(4), 0_int32) /= 1_int32",
            ),
            (
                "call MAP_INTEGER1(iptrk, 'STATE-VECTOR', 40",
                "call MAP_INTEGER1(iptrk, 'STATE-VECTOR', 39",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mccgf_rejects_weak_or_late_mcgsig_admission(self) -> None:
        cases = (
            (
                "call MAP_INTEGER1(iptrk, 'ICODE', NSOUT",
                "call MAP_INTEGER1(iptrk, 'ICODE', NSOUT-1",
            ),
            (
                "call MAP_REAL321(iptrk, 'ALBEDO', NSOUT",
                "call MAP_REAL321(iptrk, 'ALBEDO', NSOUT-1",
            ),
            (
                "RECORD_MATCHES(kpsys(i), 'DRAGON-TXSC', NBMIX+1, 2)",
                "RECORD_MATCHES(kpsys(i), 'DRAGON-TXSC', NBMIX+1, 1)",
            ),
            ("if (j /= 0) return", "if (j < 0) return"),
            (
                "if (any(icode_trk1 > nalbp)) return",
                "if (any(icode_trk1 < 0) .or. "
                "any(icode_trk1 > nalbp)) return",
            ),
            (
                "if (any(icode_trk1 > nalbp)) return",
                "if (any(icode_trk1 >= nalbp)) return",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

        mcgsig = (
            "    call MCGSIG(iptrk, NBMIX, ngeff, nalbp, kpsys, "
            "sigal32, lvoid)\n"
        )
        without_late_call = self.core.replace(mcgsig, "", 1)
        self.assertNotEqual(without_late_call, self.core)
        icode = "    call MAP_INTEGER1(iptrk, 'ICODE', NSOUT,"
        moved = without_late_call.replace(icode, mcgsig + icode, 1)
        self.core_rejected(moved)

    def test_mccgf_rejects_begin_actual_or_header_order_drift(self) -> None:
        self.core_rejected(
            self.replace_ci_once(
                self.core,
                "NUN, NDIM, .false., &",
                "NUN, NDIM, .true., &",
            )
        )
        self.core_rejected(
            self.replace_ci_once(
                self.core,
                "IAAC, ISCR, &\n        0, PACA, IDIR)",
                "IAAC, ISCR, &\n        1, PACA, IDIR)",
            )
        )

        begin = (
            "    call SPOMOC_MCCGF_BEGIN(NGRP, ngeff, ngind, nun, "
            "NDIM, .false., &\n"
            "        NLONG, NREG, NSOUT, NANI, NLIN, NFUNL, KRYL, "
            "STIS, IAAC, ISCR, &\n"
            "        0, PACA, IDIR)\n\n"
        )
        without_begin = self.core.replace(begin, "", 1)
        self.assertNotEqual(without_begin, self.core)
        header_guard = "    if (i /= NDIM .or. n2reg /= NREG"
        moved = without_begin.replace(
            header_guard, begin + header_guard, 1
        )
        self.core_rejected(moved)

    def test_mccgf_rejects_non_short_circuit_seen_guard(self) -> None:
        old = (
            "      if (j < 1 .or. j > KPN) return\n"
            "      if (seen(j)) return\n"
        )
        new = (
            "      if (j < 1 .or. j > KPN .or. seen(j)) return\n"
        )
        self.core_rejected(
            self.replace_ci_all(self.core, old, new)
        )

    def test_mcgfcs_rejects_exact_formula_or_branch_drift(self) -> None:
        cases = (
            (
                "real(sigal32(ibm), real64) * fi64(ind2)",
                "-real(sigal32(ibm), real64) * fi64(ind2)",
            ),
            (
                "qn64(ind) + &\n"
                "            real(sc32(ibm,1), real64) * fi64(ind)",
                "qn64(ind) - &\n"
                "            real(sc32(ibm,1), real64) * fi64(ind)",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mcgfl1_rejects_record_mapping_drift(self) -> None:
        cases = (
            (
                "call MAP_INTEGER2(iptrk, 'PJJIND$MCCG', NFUNL, 2",
                "call MAP_INTEGER2(iptrk, 'PJJIND$MCCG', NREG, 2",
            ),
            (
                "call MAP_INTEGER1(iptrk, 'IM$MCCG', NLONG+1",
                "call MAP_INTEGER1(iptrk, 'IM$MCCG', NLONG",
            ),
            (
                "call MAP_REAL321(kpsys(i), 'CF$MCCG', lc",
                "call MAP_REAL321(kpsys(i), 'CF$MCCG', NLONG",
            ),
            (
                "call MAP_INTEGER1(iptrk, 'BC-REFL+TRAN', NLONG-NREG",
                "call MAP_INTEGER1(iptrk, 'BC-REFL+TRAN', NLONG",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mcgabg_rejects_rho_sign_or_zero_breakdown_drift(self) -> None:
        self.aca_rejected(
            self.replace_ci_once(
                self.aca,
                "abs(rt1_64) <= 0.0_real64",
                "rt1_64 <= 0.0_real64",
            )
        )
        self.aca_rejected(
            self.replace_ci_once(
                self.aca,
                "abs(rt1_64) <= 0.0_real64",
                "abs(rt1_64) < 0.0_real64",
            )
        )

    def test_mcgpra_rejects_missing_or_weak_ju_partition_guard(self) -> None:
        cases = (
            (
                "ju(i) < im(i)+1 .or. ju(i) > im(i+1)+1",
                "ju(i) < im(i) .or. ju(i) > im(i+1)+1",
            ),
            (
                "ju(i) < im(i)+1 .or. ju(i) > im(i+1)+1",
                "ju(i) < im(i)+1 .or. ju(i) > im(i+1)",
            ),
        )
        for old, new in cases:
            with self.subTest(new=new):
                self.aca_rejected(
                    self.replace_ci_once(self.aca, old, new)
                )

    def test_mcgfl1_rejects_moc_call_actual_or_active_loop_drift(self) -> None:
        cases = (
            (
                "call MOCIK3(NANI-1, NFUNL, 4, isgnr, keyani)",
                "call MOCIK3(NANI-1, NFUNL, 4, keyani, isgnr)",
            ),
            ("keyani(1) /= 0", "keyani(1) /= 1"),
            (
                "keycur_trk1, nzon_trk1, nconv, caz0_inactive64",
                "keycur_trk1, matalb_trk, nconv, caz0_inactive64",
            ),
            (
                "pjjind_trk2, &\n        nzon_trk1, volume_trk32",
                "pjjind_trk2, &\n        matalb_trk, volume_trk32",
            ),
            (
                "if (nconv(i)) then\n"
                "        if (.not. RECORD_MATCHES(kpsys(i), 'PJJ$MCCG'",
                "if (.true.) then\n"
                "        if (.not. RECORD_MATCHES(kpsys(i), 'PJJ$MCCG'",
            ),
            (
                "if (nconv(i)) then\n"
                "        call MCGFCS64",
                "if (.true.) then\n"
                "        call MCGFCS64",
            ),
        )
        for old, new in cases:
            with self.subTest(old=old):
                self.core_rejected(
                    self.replace_ci_once(self.core, old, new)
                )

    def test_mcgfl1_rejects_five_record_tracking_skip(self) -> None:
        self.core_rejected(
            self.replace_ci_once(
                self.core, "do icom = 1, 6", "do icom = 1, 5"
            )
        )

    def test_aca_rejects_legacy_calls_and_shape_regression(self) -> None:
        self.aca_rejected(
            self.replace_ci_once(
                self.aca, "call MCGPRA64", "call MCGPRA"
            )
        )
        self.aca_rejected(
            self.replace_ci_once(
                self.aca, "im(nlong+1), mcu(lc), ju(nlong)",
                "im(nlong), mcu(lc), ju(nlong)"
            )
        )
        self.aca_rejected(
            self.replace_ci_once(
                self.aca, "diagf32(nlong), cf32(lc)",
                "diagf32(nlong), cf32(nlong)"
            )
        )

    def test_aca_rejects_missing_active_inactive_separation(self) -> None:
        self.aca_rejected(
            self.replace_ci_all(
                self.aca, "DIAGF_INACTIVE32", "DIAGF32"
            )
        )
        self.aca_rejected(
            self.replace_ci_all(
                self.aca, "LUCF_INACTIVE32", "LUCF32"
            )
        )

    def test_aca_rejects_delta_loss_or_counterfactual_feedback(self) -> None:
        self.aca_rejected(
            self.replace_ci_once(
                self.aca,
                "cutoff_delta64 = cutoff_delta64 + child_delta64\n"
                "        if (.not. child_ok) return",
                "if (.not. child_ok) return\n"
                "        cutoff_delta64 = cutoff_delta64 + child_delta64",
            )
        )
        marker = "if (guard_live) then"
        self.aca_rejected(
            self.replace_ci_once(
                self.aca, marker, "if (guard_zero) then"
            )
        )

    def test_adapter_rejects_descriptor_or_module_abi(self) -> None:
        self.adapter_rejected("module BAD\n" + self.adapter)
        self.adapter_rejected(
            self.adapter.replace("KEYFLX_TRK3(NREG,1,1)",
                                 "KEYFLX_TRK3(:,:,:)", 1)
        )
        self.adapter_rejected(
            self.adapter.replace("subroutine MCGFFIR64_RANK_ADAPTER(",
                                 "subroutine MCGFFIR64_RANK_ADAPTER( bind(c) ",
                                 1)
        )

    def test_makefile_rejects_dependency_or_default_integration(self) -> None:
        self.assertIn("spot-real64-phase-a8 :\n", self.makefile)
        with self.assertRaises(PhaseA8Error):
            validate_makefile_contract(
                self.makefile.replace(
                    "spot-real64-phase-a8 :\n",
                    "spot-real64-phase-a8 : all\n", 1
                )
            )
        with self.assertRaises(PhaseA8Error):
            validate_makefile_contract(
                self.makefile.replace("tests :\n", "tests : spot-real64-phase-a8\n", 1)
            )

    def test_runner_rejects_old_runner_dragon_or_linker(self) -> None:
        for injected in ("run_phase_a2.sh", "Dragon", "\nld unsafe.o\n"):
            with self.subTest(injected=injected):
                with self.assertRaises(PhaseA8Error):
                    validate_runner_contract(
                        self.runner + "\n" + injected, verify_hash=False
                    )

    def test_runner_rejects_repeated_negative_substitution(self) -> None:
        removed = "compile_fail_real32_capture.f90"
        repeated = "compile_fail_real32_mutable_tail.f90"
        self.assertEqual(self.runner.count(removed), 1)
        with self.assertRaises(PhaseA8Error):
            validate_runner_contract(
                self.runner.replace(removed, repeated, 1), verify_hash=False
            )


if __name__ == "__main__":
    unittest.main()

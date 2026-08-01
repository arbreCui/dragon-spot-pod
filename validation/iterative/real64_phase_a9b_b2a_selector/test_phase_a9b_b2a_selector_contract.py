#!/usr/bin/env python3
"""Targeted fail-closed mutations for the production B2a selector gate."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_phase_a9b_b2a_selector as gate


class SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.flu = (gate.ROOT / "src/FLU.f").read_text()
        cls.flugpi = (gate.ROOT / "src/FLUGPI.f").read_text()
        cls.fludrv = (gate.ROOT / "src/FLUDRV.f").read_text()

    @staticmethod
    def replace_once(text: str, old: str, new: str) -> str:
        if text.count(old) != 1:
            raise AssertionError(f"mutation anchor count for {old!r}")
        return text.replace(old, new, 1)

    def rejected(self, *, flu: str | None = None, flugpi: str | None = None,
                 fludrv: str | None = None) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_source_contract(
                self.flu if flu is None else flu,
                self.flugpi if flugpi is None else flugpi,
                self.fludrv if fludrv is None else fludrv,
            )

    def test_unmodified_contract_passes(self) -> None:
        gate.check_source_contract(self.flu, self.flugpi, self.fludrv)

    def test_flu_public_abi_cannot_expand(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "SUBROUTINE FLU(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)",
            "SUBROUTINE FLU(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY,LR64)",
        ))

    def test_flugpi_cannot_drop_limerg(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "IPICK,IMCAUD,LIMERG,LR64)",
            "IPICK,IMCAUD,LR64)",
        ))

    def test_flugpi_tail_order_is_exact(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "IPICK,IMCAUD,LIMERG,LR64)",
            "IPICK,IMCAUD,LR64,LIMERG)",
        ))

    def test_fludrv_cannot_drop_selector(self) -> None:
        self.rejected(fludrv=self.replace_once(
            self.fludrv, "NMERG,IMERG,IMCAUD,LR64)",
            "NMERG,IMERG,IMCAUD)",
        ))

    def test_flugpi_actual_tail_order_is_exact(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu, "IMCAUD,LIMERG,LR64)", "IMCAUD,LR64,LIMERG)",
        ))

    def test_fludrv_actual_cannot_drop_selector(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu, "NMERG,IMERG,IMCAUD,LR64)",
            "NMERG,IMERG,IMCAUD)",
        ))

    def test_selector_default_cannot_be_true(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "LR64=.FALSE.", "LR64=.TRUE.",
        ))

    def test_selector_must_reset_each_call(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "      LR64=.FALSE.\n", "",
        ))

    def test_selector_default_must_precede_rec(self) -> None:
        text = self.replace_once(self.flugpi, "      LR64=.FALSE.\n", "")
        text = self.replace_once(
            text, "      IF(REC) THEN\n",
            "      IF(REC) THEN\n      LR64=.FALSE.\n",
        )
        self.rejected(flugpi=text)

    def test_duplicate_guard_cannot_be_disabled(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "        IF(LR64) THEN\n",
            "        IF(.FALSE.) THEN\n",
        ))

    def test_duplicate_guard_must_return_if_xabort_returns(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi,
            "          CALL XABORT('FLUGPI: DUPLICATE R64 KEYWORD.')\n"
            "          RETURN\n",
            "          CALL XABORT('FLUGPI: DUPLICATE R64 KEYWORD.')\n",
        ))

    def test_r64_must_not_consume_a_parameter(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "        LR64=.TRUE.\n",
            "        CALL REDGET(ITYPLU,INTLIR,REALIR,CARLIR,DBLINP)\n"
            "        LR64=.TRUE.\n",
        ))

    def test_r64_cannot_change_moca(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "        LR64=.TRUE.\n",
            "        IMCAUD=1\n        LR64=.TRUE.\n",
        ))

    def test_moca_cannot_enable_r64(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "        IMCAUD=INTLIR\n",
            "        IMCAUD=INTLIR\n        LR64=.TRUE.\n",
        ))

    def test_flugpi_cannot_write_ipflux(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "      RETURN\n      END\n",
            "      CALL LCMPUT(IPFLUX,'R64',1,1,IMCAUD)\n"
            "      RETURN\n      END\n",
        ))

    def test_limerg_default_must_follow_rec(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "LIMERG=.NOT.REC", "LIMERG=.TRUE.",
        ))

    def test_limerg_cannot_be_set_inside_hete_loop(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi,
            "                ENDDO\n                LIMERG=.TRUE.\n",
            "                  LIMERG=.TRUE.\n                ENDDO\n",
        ))

    def test_selector_cannot_be_saved(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "      SAVE        CBUCKN,CLEAK,CSDIR\n",
            "      SAVE        CBUCKN,CLEAK,CSDIR,LR64\n",
        ))

    def test_selector_cannot_use_common_state(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "      DOUBLE PRECISION DBLINP\n",
            "      DOUBLE PRECISION DBLINP\n      COMMON /R64S/ LR64\n",
        ))

    def test_selector_cannot_use_environment(self) -> None:
        self.rejected(flugpi=self.replace_once(
            self.flugpi, "      LR64=.FALSE.\n",
            "      LR64=.FALSE.\n      CALL GETENV('SPOT_R64',CARLIR)\n",
        ))

    def test_flu_cannot_restore_early_signature_write(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu, "         HSIGN='L_FLUX'\n      ENDIF\n",
            "         HSIGN='L_FLUX'\n"
            "         CALL LCMPTC(IPFLUX,'SIGNATURE',12,HSIGN)\n"
            "      ENDIF\n",
        ))

    def test_flu_alias_cannot_hide_an_early_write(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
            "      IPFLUP=IPFLUX\n"
            "      CALL LCMPTC(IPFLUP,'EARLY-R64',12,HSIGN)\n"
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
        ))

    def test_flu_function_style_lcm_mutation_is_rejected(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
            "      IPTRK=IPFLUX\n"
            "      IPFLUP=LCMDIL(IPTRK,1)\n"
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
        ))

    def test_flu_cannot_expand_the_lcmsix_cursor_exception(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
            "      IPFLUP=IPFLUX\n"
            "      CALL LCMSIX(IPFLUP,'EARLY',1)\n"
            "      CALL FLUGPI(IPFLUX,IPMACR,ITYPEC,MAXOUT,MAXINR,EPSOUT,EPSUNK,\n",
        ))

    def test_flu_selected_guard_cannot_be_removed(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      IF(LR64) THEN\n"
            "        CALL XABORT('FLU: R64 SELECTED BEFORE B2B INGRESS.')\n"
            "        RETURN\n"
            "      ENDIF\n",
            "",
        ))

    def test_flu_selected_guard_must_return(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "        CALL XABORT('FLU: R64 SELECTED BEFORE B2B INGRESS.')\n"
            "        RETURN\n",
            "        CALL XABORT('FLU: R64 SELECTED BEFORE B2B INGRESS.')\n",
        ))

    def test_flu_cannot_reset_selector_for_fallback(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu, "      IF(LR64) THEN\n",
            "      LR64=.FALSE.\n      IF(LR64) THEN\n",
        ))

    def test_xdrta2_cannot_move_before_selected_return(self) -> None:
        text = self.replace_once(
            self.flu, "      IF(CXDOOR.EQ.'MCCG') CALL XDRTA2(IPTRK)\n", "",
        )
        text = self.replace_once(
            text, "      IF(LR64) THEN\n",
            "      CALL XDRTA2(IPTRK)\n      IF(LR64) THEN\n",
        )
        self.rejected(flu=text)

    def test_xdrta2_zero_argument_change_waits_for_b2b(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu, "CALL XDRTA2(IPTRK)", "CALL XDRTA2",
        ))

    def test_deferred_signature_must_reset_hsign(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      IF(.NOT.REC) THEN\n"
            "        HSIGN='L_FLUX'\n"
            "        CALL LCMPTC(IPFLUX,'SIGNATURE',12,HSIGN)\n",
            "      IF(.NOT.REC) THEN\n"
            "        CALL LCMPTC(IPFLUX,'SIGNATURE',12,HSIGN)\n",
        ))

    def test_imerg_commit_must_be_dirty_guarded(self) -> None:
        self.rejected(flu=self.replace_once(
            self.flu,
            "      IF(LIMERG) CALL LCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERG)",
            "      CALL LCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERG)",
        ))

    def test_deferred_record_class_order_is_locked(self) -> None:
        text = self.replace_once(
            self.flu, "      CALL LCMPTC(IPFLUX,'LINK.MACRO',12,HPMACR)\n", "",
        )
        text = self.replace_once(
            text,
            "      IF(LIMERG) CALL LCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERG)\n",
            "      IF(LIMERG) CALL LCMPUT(IPFLUX,'IMERGE-LEAK',NMAT,1,IMERG)\n"
            "      CALL LCMPTC(IPFLUX,'LINK.MACRO',12,HPMACR)\n",
        )
        self.rejected(flu=text)

    def test_fludrv_guard_must_precede_allocation(self) -> None:
        guard = (
            "      IF(LR64) THEN\n"
            "        CALL XABORT('FLUDRV: R64 REQUIRES THE B2B INGRESS.')\n"
            "        RETURN\n"
            "      ENDIF\n"
        )
        text = self.replace_once(self.fludrv, guard, "")
        text = self.replace_once(
            text, "      ALLOCATE(FLUXO(NUN,NGRP),XSTRC(0:NMAT,NGRP),\n",
            "      ALLOCATE(FLUXO(NUN,NGRP),XSTRC(0:NMAT,NGRP),\n" + guard,
        )
        self.rejected(fludrv=text)

    def test_fludrv_guard_must_return(self) -> None:
        self.rejected(fludrv=self.replace_once(
            self.fludrv,
            "        CALL XABORT('FLUDRV: R64 REQUIRES THE B2B INGRESS.')\n"
            "        RETURN\n",
            "        CALL XABORT('FLUDRV: R64 REQUIRES THE B2B INGRESS.')\n",
        ))

    def test_fludrv_cannot_reset_selector(self) -> None:
        self.rejected(fludrv=self.replace_once(
            self.fludrv, "      IF(LR64) THEN\n",
            "      LR64=.FALSE.\n      IF(LR64) THEN\n",
        ))

    def test_fludrv_cannot_call_spomoc_begin64(self) -> None:
        self.rejected(fludrv=self.replace_once(
            self.fludrv, "CALL SPOMOC_BEGIN(", "CALL SPOMOC_BEGIN64(",
        ))

    def test_fludrv_cannot_call_flu2dr64(self) -> None:
        self.rejected(fludrv=self.replace_once(
            self.fludrv, "CALL FLU2DR(", "CALL FLU2DR64(",
        ))


class RunnerMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = gate.RUNNER.read_text()

    def rejected(self, addition: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.validate_runner_text(
                self.runner + addition, verify_hash=False
            )

    def test_unmodified_runner_contract_passes(self) -> None:
        gate.validate_runner_text(self.runner)
        gate.validate_runner_text(self.runner, verify_hash=False)
        with self.assertRaises(gate.GateError):
            gate.validate_runner_text(self.runner + "\n# drift\n")

    def test_absolute_compiler_link_is_rejected(self) -> None:
        self.rejected(
            "\n/opt/homebrew/bin/gfortran \"$PROD_DIR/FLU.o\" "
            "fake_stubs.o -o forbidden\n"
        )

    def test_env_compiler_link_is_rejected(self) -> None:
        self.rejected(
            "\nenv \"$FC\" \"$PROD_DIR/FLU.o\" fake_stubs.o "
            "-o forbidden\n"
        )

    def test_absolute_production_execution_is_rejected(self) -> None:
        self.rejected("\n/tmp/forbidden_production_executable\n")

    def test_env_production_execution_is_rejected(self) -> None:
        self.rejected("\nenv ./forbidden_production_executable\n")

    def test_compiler_reassignment_is_rejected(self) -> None:
        self.rejected("\nFC=/tmp/fake-gfortran\n")


class ManifestMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(gate.MANIFEST.read_text())

    def rejected(self, mutation) -> None:
        data = copy.deepcopy(self.data)
        mutation(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(data))
            original = gate.MANIFEST
            gate.MANIFEST = path
            try:
                with self.assertRaises(gate.GateError):
                    gate.check_manifest()
            finally:
                gate.MANIFEST = original

    def test_manifest_baseline_passes(self) -> None:
        gate.check_manifest()

    def test_route_cannot_be_claimed_executable(self) -> None:
        self.rejected(lambda d: d["status"].__setitem__(
            "r64_route_executable", True))

    def test_production_route_cannot_be_claimed_connected(self) -> None:
        self.rejected(lambda d: d["status"].__setitem__(
            "production_route_connected", True))

    def test_continuous_lane_cannot_be_claimed(self) -> None:
        self.rejected(lambda d: d["status"].__setitem__(
            "continuous_real64_lane", True))

    def test_convergence_cannot_be_claimed(self) -> None:
        self.rejected(lambda d: d["status"].__setitem__(
            "radial_convergence", "PASS"))

    def test_fallback_cannot_be_allowed(self) -> None:
        self.rejected(lambda d: d["selector_contract"].__setitem__(
            "fallback_after_selection", True))

    def test_moca_cannot_be_coupled(self) -> None:
        self.rejected(lambda d: d["selector_contract"].__setitem__(
            "orthogonal_to_moca", False))

    def test_metadata_trace_cannot_be_overclaimed(self) -> None:
        self.rejected(lambda d: d["write_deferral"].__setitem__(
            "metadata_mutation_trace_identity_claimed", True))

    def test_empirical_parameter_cannot_be_added(self) -> None:
        self.rejected(lambda d: d["scope_boundaries"].__setitem__(
            "empirical_parameter", True))

    def test_dragon_count_must_remain_zero(self) -> None:
        self.rejected(lambda d: d["scope_boundaries"].__setitem__(
            "dragon_runs", 1))

    def test_lcmsix_boundary_cannot_be_overclaimed(self) -> None:
        self.rejected(lambda d: d["scope_boundaries"].__setitem__(
            "complete_a7_admission_before_lcmsix_claimed", True))


if __name__ == "__main__":
    unittest.main()

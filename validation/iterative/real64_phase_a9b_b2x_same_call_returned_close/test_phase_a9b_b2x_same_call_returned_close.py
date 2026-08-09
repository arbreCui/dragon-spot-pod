#!/usr/bin/env python3
"""Directed mutations for the B2x static contract."""

from __future__ import annotations

import unittest

import check_phase_a9b_b2x_same_call_returned_close as gate


HOST = gate.HOST.read_text()
ADAPTER = gate.ADAPTER.read_text()
DISPATCHER = gate.KDRDRV.read_text()
FLU2DR = gate.FLU2DR.read_text()


def changed(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError(f"mutation anchor is absent: {old!r}")
    result = text.replace(old, new, 1)
    if result == text:
        raise AssertionError("mutation did not change source")
    return result


class B2XContractTests(unittest.TestCase):
    def reject_host(self, old: str, new: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_host(changed(HOST, old, new))

    def reject_adapter(self, old: str, new: str) -> None:
        body = gate.routine(ADAPTER, "SPOR64X")
        with self.assertRaises(gate.GateError):
            gate.check_adapter(changed(body, old, new))

    def reject_admission_adapter(self, old: str, new: str) -> None:
        body = gate.routine(ADAPTER, "SPOR64V")
        with self.assertRaises(gate.GateError):
            gate.check_admission_adapter(changed(body, old, new))

    def reject_admission(self, old: str, new: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_returned_admission(changed(gate.B2W.read_text(), old, new))

    def reject_dispatcher(self, old: str, new: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_dispatcher(changed(DISPATCHER, old, new))

    def reject_flu2dr(self, old: str, new: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_flu2dr(changed(FLU2DR, old, new))

    def test_00_baseline(self) -> None:
        gate.check_all()

    def test_01_reject_detached_feedback_source(self) -> None:
        self.reject_host("FEEDBACK := RETURNED", "FEEDBACK := BASIS_REF")

    def test_02_reject_asm_archive_substitution(self) -> None:
        self.reject_host(
            "MACROLIB3 TRACK_AX FEEDBACK BASIS_REF",
            "MACROLIB3 TRACK_AX RETURNED BASIS_REF",
        )

    def test_03_reject_asm_basis_substitution(self) -> None:
        self.reject_host(
            "MACROLIB3 TRACK_AX FEEDBACK BASIS_REF",
            "MACROLIB3 TRACK_AX FEEDBACK RETURNED",
        )

    def test_04_reject_rank_change(self) -> None:
        self.reject_host("EDIT 0 SPOD 1 FIXB", "EDIT 0 SPOD 2 FIXB")

    def test_05_reject_missing_fixb(self) -> None:
        self.reject_host("EDIT 0 SPOD 1 FIXB", "EDIT 0 SPOD 1")

    def test_06_reject_second_asm(self) -> None:
        self.reject_host(
            "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX FEEDBACK BASIS_REF ::",
            "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX FEEDBACK BASIS_REF ::\n"
            "  EDIT 0 SPOD 1 FIXB ;\n"
            "SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX FEEDBACK BASIS_REF ::",
        )

    def test_06a_reject_missing_spor64v(self) -> None:
        self.reject_host("SPOR64V: FEEDBACK :: ;", "SPOR64V: RETURNED :: ;")

    def test_07_reject_flu_system_substitution(self) -> None:
        self.reject_host(
            "MACROLIB3 TRACK_AX SYSTEM_NEXT",
            "MACROLIB3 TRACK_AX BASIS_REF",
        )

    def test_08_reject_flu_type_change(self) -> None:
        self.reject_host("TYPE K B1 SIGS", "TYPE S B1 SIGS")

    def test_09_reject_flu_cap_change(self) -> None:
        self.reject_host("EXTE 500", "EXTE 501")

    def test_10_reject_flu_tolerance_change(self) -> None:
        self.reject_host("EXTE 500 2.5E-7", "EXTE 500 5.0E-7")

    def test_11_reject_spostate_system_substitution(self) -> None:
        self.reject_host(
            "AX_NEXT TRACK_AX SYSTEM_NEXT MACROLIB3",
            "AX_NEXT TRACK_AX BASIS_REF MACROLIB3",
        )

    def test_12_reject_spoleak_archive_substitution(self) -> None:
        self.reject_host(
            "FEEDBACK := SPOLEAK: FEEDBACK AX_NEXT TRACK_AX",
            "FEEDBACK := SPOLEAK: RETURNED AX_NEXT TRACK_AX",
        )

    def test_13_reject_spoleak_ax_substitution(self) -> None:
        self.reject_host(
            "FEEDBACK AX_NEXT TRACK_AX", "FEEDBACK BASIS_REF TRACK_AX"
        )

    def test_14_reject_terminal_input_swap(self) -> None:
        self.reject_host(
            "SPOR64X: AX_NEXT FEEDBACK", "SPOR64X: FEEDBACK AX_NEXT"
        )

    def test_15_reject_cleanup_loss(self) -> None:
        self.reject_host(
            "FEEDBACK SYSTEM_NEXT AX_NEXT := DELETE:",
            "SYSTEM_NEXT AX_NEXT := DELETE:",
        )

    def test_16_reject_loop(self) -> None:
        self.reject_host(
            "REAL leak_change ;", "REAL leak_change ;\nWHILE 1 1 = DO"
        )

    def test_17_reject_adapter_output_name(self) -> None:
        self.reject_adapter("hentry(2) /= 'ARCH_CLOSED'", "hentry(2) /= 'ARCHIVE'")

    def test_18_reject_adapter_input_name(self) -> None:
        self.reject_adapter("hentry(4) /= 'FEEDBACK'", "hentry(4) /= 'RETURNED'")

    def test_19_reject_adapter_ientry(self) -> None:
        self.reject_adapter("any(ientry /= 1)", "any(ientry /= 2)")

    def test_20_reject_adapter_jentry(self) -> None:
        self.reject_adapter("any(jentry(3:4) /= 2)", "any(jentry(3:4) /= 1)")

    def test_21_reject_adapter_parser_loss(self) -> None:
        self.reject_adapter(
            "call REDGET(indic,nitma,flott,text4,dflott)",
            "indic=3\n  text4=';'",
        )

    def test_22_reject_adapter_b2w_order(self) -> None:
        self.reject_adapter(
            "kentry(1),kentry(2),kentry(3),kentry(4)",
            "kentry(1),kentry(2),kentry(4),kentry(3)",
        )

    def test_23_reject_adapter_success_token(self) -> None:
        self.reject_adapter(
            "status /= SPOR64_B2W_CLOSED", "status == SPOR64_B2W_CLOSED"
        )

    def test_24_reject_dispatcher_route_loss(self) -> None:
        self.reject_dispatcher("'SPOR64X:'", "'SPOR64Y:'")

    def test_24a_reject_admission_adapter_write_access(self) -> None:
        self.reject_admission_adapter("jentry(1) /= 2", "jentry(1) /= 1")

    def test_24b_reject_admission_adapter_input(self) -> None:
        self.reject_admission_adapter("hentry(1) /= 'FEEDBACK'", "hentry(1) /= 'RETURNED'")

    def test_24c_reject_elementwise_l0_identity_loss(self) -> None:
        self.reject_admission(
            "if (found32 /= expected32) return",
            "if (found32 == expected32) return",
        )

    def test_25_reject_strict_nonstrict_outer(self) -> None:
        self.reject_flu2dr("IF((EEXT.LT.EPSOUT)", "IF((EEXT.LE.EPSOUT)")

    def test_26_reject_strict_inner_state_loss(self) -> None:
        self.reject_flu2dr(
            ".AND.(IINR_STATE.EQ.1)", ".AND.(IINR_STATE.GE.0)"
        )

    def test_27_reject_strict_minimum_iteration_loss(self) -> None:
        self.reject_flu2dr("     2   (IT.GE.2)", "     2   (IT.GE.1)")

    def test_28_reject_cap_gate_narrowing(self) -> None:
        self.reject_flu2dr(
            "(ITYPEC.GE.2).AND.\n     1   (ITYPEC.LE.3)",
            "(ITYPEC.EQ.3)",
        )

    def test_29_reject_cap_return_loss(self) -> None:
        self.reject_flu2dr(
            "CALL XABORT('FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.')\n"
            "         RETURN",
            "CALL XABORT('FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.')",
        )


if __name__ == "__main__":
    unittest.main()

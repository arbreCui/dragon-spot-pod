#!/usr/bin/env python3
"""Directed mutations for the B2y one-real-close static boundary."""

from __future__ import annotations

import re
import unittest

import check_phase_a9b_b2y_one_real_returned_close as contract


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(
            f"mutation anchor must occur once, found {text.count(old)}: {old}"
        )
    return text.replace(old, new, 1)


class B2YContractMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = contract.DECK.read_text(encoding="utf-8")
        cls.runner = contract.RUNNER.read_text(encoding="utf-8")
        cls.bounded = contract.BOUNDED.read_text(encoding="utf-8")
        cls.host = contract.HOST.read_text(encoding="utf-8")
        cls.flu2dr = contract.FLU2DR.read_text(encoding="utf-8")

    def reject_deck(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_deck(mutated)

    def reject_runner(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_runner(mutated)

    def reject_bounded(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_bounded(mutated)

    def reject_host(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_production_host(mutated)

    def reject_flu2dr(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_flu2dr(mutated)

    def test_00_positive_baseline(self) -> None:
        contract.check_deck(self.deck)
        contract.check_runner(self.runner)
        contract.check_bounded(self.bounded)
        contract.check_production_host(self.host)
        contract.check_flu2dr(self.flu2dr)

    # The runtime deck owns no preparation or iteration policy.  It imports
    # the six named XSM paths, invokes the production procedure once, and
    # persists only the two returned roots.
    def test_01_deck_rejects_second_close(self) -> None:
        call = (
            "AX_CLOSED ARCH_CLOSED := SpotCloseR64\n"
            "  RETURNED TRACK_AX MACROLIB3 BASIS_REF :: ;"
        )
        self.reject_deck(replace_once(self.deck, call, call + "\n" + call))

    def test_02_deck_rejects_spotstep(self) -> None:
        self.reject_deck(self.deck + "\nPROCEDURE SpotStepR64 ;\n")

    def test_03_deck_rejects_wrong_returned_binding(self) -> None:
        self.reject_deck(replace_once(
            self.deck, "RETURNED := RET_XSM ;", "RETURNED := BASIS_XSM ;"
        ))

    def test_04_deck_rejects_wrong_close_argument_order(self) -> None:
        self.reject_deck(replace_once(
            self.deck,
            "RETURNED TRACK_AX MACROLIB3 BASIS_REF :: ;",
            "RETURNED TRACK_AX BASIS_REF MACROLIB3 :: ;",
        ))

    def test_05_deck_rejects_missing_axial_output_copy(self) -> None:
        self.reject_deck(replace_once(self.deck, "AX_OUT := AX_CLOSED ;", ""))

    def test_06_deck_rejects_output_before_close(self) -> None:
        line = "AX_OUT := AX_CLOSED ;\n"
        moved = self.deck.replace(line, "", 1)
        moved = replace_once(
            moved,
            'ECHO "B2Y-REAL-RETURNED-CLOSE-BEGIN" ;\n',
            line + 'ECHO "B2Y-REAL-RETURNED-CLOSE-BEGIN" ;\n',
        )
        self.reject_deck(moved)

    def test_07_deck_rejects_loop(self) -> None:
        self.reject_deck(self.deck + "\nWHILE 1 1 = DO\nENDWHILE ;\n")

    def test_08_deck_rejects_tolerance_override(self) -> None:
        self.reject_deck(self.deck + "\nREAL EXTE := 1.0E-4 ;\n")

    # The shell gate is off unless explicitly armed.  Its one input is an
    # externally supplied immutable B2v artifact; it cannot manufacture or
    # search for a replacement, and it has one close-profile launch site.
    def test_09_runner_rejects_default_on(self) -> None:
        self.reject_runner(replace_once(
            self.runner, "RUN_B2Y=${RUN_B2Y:-0}", "RUN_B2Y=${RUN_B2Y:-1}"
        ))

    def test_10_runner_rejects_changed_returned_hash(self) -> None:
        self.reject_runner(replace_once(
            self.runner, contract.RETURNED_SHA256, "0" * 64
        ))

    def test_11_runner_rejects_changed_returned_size(self) -> None:
        self.reject_runner(replace_once(
            self.runner, str(contract.RETURNED_BYTES),
            str(contract.RETURNED_BYTES + 1),
        ))

    def test_12_runner_rejects_missing_external_copy(self) -> None:
        anchor = 'copy_exact "$B2Y_RETURNED_XSM" "$CASE_DIR/returned.xsm"'
        self.reject_runner(replace_once(self.runner, anchor, ":"))

    def test_13_runner_rejects_symlinked_external_input(self) -> None:
        anchor = '[ ! -L "$B2Y_RETURNED_XSM" ]'
        self.reject_runner(replace_once(self.runner, anchor, "[ 1 -eq 1 ]"))

    def test_14_runner_rejects_b2v_regeneration(self) -> None:
        self.reject_runner(self.runner + "\nRUN_B2V=1\n")

    def test_15_runner_rejects_retry_loop(self) -> None:
        self.reject_runner(self.runner + "\nwhile false; do :; done\n")

    def test_16_runner_rejects_second_close_launch(self) -> None:
        match = re.search(
            r'(?m)^\s*(?:if\s+!\s+)?python3\s+"?\$BOUNDED"?\s+close\b.*$',
            self.runner,
        )
        self.assertIsNotNone(match)
        line = match.group(0)
        self.reject_runner(
            self.runner[:match.end()] + "\n" + line + self.runner[match.end():]
        )

    def test_17_runner_rejects_missing_flu_census(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            "runtime_count_exact 1 '^->@BEGIN MODULE : FLU:'",
            "runtime_count_exact 1 '^->@BEGIN MODULE : FLU-NOT-CHECKED:'",
        ))

    # One shared Popen site may service the close once and each independent
    # posterior in separate invocations.  The profile values and process-
    # group termination mechanics are nevertheless immutable.
    def test_18_bounded_rejects_relaxed_close_wall(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded, '"wall_seconds": 80', '"wall_seconds": 81'
        ))

    def test_19_bounded_rejects_relaxed_close_cpu(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded, '"cpu_seconds": 75', '"cpu_seconds": 76'
        ))

    def test_20_bounded_rejects_second_popen_site(self) -> None:
        anchor = "        process = subprocess.Popen("
        injected = "        if False:\n            subprocess.Popen([])\n" + anchor
        self.reject_bounded(replace_once(self.bounded, anchor, injected))

    def test_21_bounded_rejects_subprocess_run(self) -> None:
        self.reject_bounded(self.bounded + "\nif False:\n    subprocess.run([])\n")

    def test_22_bounded_rejects_shared_process_group(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded, "start_new_session=True", "start_new_session=False"
        ))

    def test_23_bounded_rejects_missing_sigkill(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded,
            "os.killpg(process.pid, signal.SIGKILL)",
            "os.killpg(process.pid, signal.SIGTERM)",
        ))

    # Re-freeze the production method, not merely the wrapper spelling.
    def test_24_host_rejects_rank_change(self) -> None:
        self.reject_host(replace_once(self.host, "SPOD 1 FIXB", "SPOD 2 FIXB"))

    def test_25_host_rejects_tolerance_change(self) -> None:
        self.reject_host(replace_once(self.host, "EXTE 500 2.5E-7", "EXTE 500 5.0E-7"))

    def test_26_host_rejects_cap_change(self) -> None:
        self.reject_host(replace_once(self.host, "EXTE 500", "EXTE 501"))

    def test_27_host_rejects_feedback_alias(self) -> None:
        self.reject_host(replace_once(
            self.host,
            "FEEDBACK := SPOLEAK: FEEDBACK AX_NEXT TRACK_AX",
            "FEEDBACK := SPOLEAK: RETURNED AX_NEXT TRACK_AX",
        ))

    def test_28_host_rejects_relaxation_keyword(self) -> None:
        self.reject_host(self.host + "\nRELAX 0.5\n")

    # Cap exhaustion must not fall into label 410, and the only success path
    # remains all three strict norms plus strict inner state and visit >= 2.
    def test_29_flu2dr_rejects_missing_cap_abort(self) -> None:
        self.reject_flu2dr(replace_once(
            self.flu2dr,
            "CALL XABORT('FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.')",
            "CONTINUE",
        ))

    def test_30_flu2dr_rejects_missing_cap_return(self) -> None:
        block = (
            "         CALL XABORT('FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.')\n"
            "         RETURN"
        )
        self.reject_flu2dr(replace_once(
            self.flu2dr,
            block,
            "         CALL XABORT('FLU2DR: SPOT TYPE-K STRICT TERMINATION REQUIRED.')",
        ))

    def test_31_flu2dr_rejects_nonstrict_outer_norm(self) -> None:
        self.reject_flu2dr(replace_once(
            self.flu2dr,
            "IF((EEXT.LT.EPSOUT).AND.(EINN.LT.EPSUNK)",
            "IF((EEXT.LE.EPSOUT).AND.(EINN.LT.EPSUNK)",
        ))

    def test_32_flu2dr_rejects_early_outer_visit(self) -> None:
        self.reject_flu2dr(replace_once(self.flu2dr, "IT.GE.2", "IT.GE.1"))

    def test_33_bounded_rejects_changed_resource_class(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded,
            '"close": "INVALID-RUNTIME-BUDGET-NO-CLOSED-RESULT"',
            '"close": "GARBAGE"',
        ))

    def test_34_runner_rejects_missing_spor64v_end_census(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            "runtime_count_exact 1 '^->@END MODULE   : SPOR64V:'",
            "runtime_count_exact 0 '^->@END MODULE   : SPOR64V:'",
        ))

    def test_35_runner_rejects_missing_outer_terminal_census(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            "runtime_count_exact 1 '^ FLU2DR-TERM OUTER-GATE=PASS '",
            "runtime_count_exact 0 '^ FLU2DR-TERM OUTER-GATE=PASS '",
        ))

    def test_36_runner_rejects_reversed_route_order(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ "$BEGIN_LINE" -lt "$V_BEGIN" ]',
            '[ "$BEGIN_LINE" -gt "$V_BEGIN" ]',
        ))

    def test_37_runner_rejects_changed_maxout_census(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ "$MAXOUT" -eq 500 ]',
            '[ "$MAXOUT" -eq 501 ]',
        ))

    def test_38_runner_rejects_changed_maxinr_census(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ "$MAXINR" -eq 740 ]',
            '[ "$MAXINR" -eq 741 ]',
        ))

    def test_39_runner_rejects_changed_inner_state(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ "$INNER_STATE" -eq 1 ]',
            '[ "$INNER_STATE" -eq 2 ]',
        ))

    def test_40_runner_rejects_hardcoded_outer_values(self) -> None:
        self.reject_runner(replace_once(
            self.runner, "set -- $OUTER_VALUES", "set -- 2 500 1"
        ))

    def test_41_runner_rejects_hardcoded_inner_values(self) -> None:
        self.reject_runner(replace_once(
            self.runner, "set -- $INNER_VALUES", "set -- 1 740 371 1 370"
        ))

    def test_42_runner_rejects_fake_outer_log_line(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            "OUTER_LINE=$(grep '^ FLU2DR-TERM OUTER-GATE=PASS ' "
            '"$CASE_DIR/dragon.log")',
            "OUTER_LINE='fake'",
        ))

    def test_43_runner_rejects_shortcut_outer_parser(self) -> None:
        expression = (
            "'s/^ FLU2DR-TERM OUTER-GATE=PASS IEXTF= *([0-9]+) "
            "MAXOUT= *([0-9]+).* EUNK-VALID=([0-9]+)$/\\1 \\2 \\3/'"
        )
        self.reject_runner(replace_once(
            self.runner, expression, "'s/.*/2 500 1/'"
        ))

    def test_44_bounded_rejects_missing_sigterm_handler(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded,
            "(signal.SIGHUP, signal.SIGINT, signal.SIGTERM)",
            "(signal.SIGHUP, signal.SIGINT)",
        ))

    def test_45_bounded_rejects_missing_exception_cleanup(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded, "except BaseException:", "except RuntimeError:"
        ))

    def test_46_runner_rejects_changed_a9_module_hash(self) -> None:
        self.reject_runner(replace_once(
            self.runner, contract.A9_MODULE_SHA256, "1" * 64
        ))

    def test_47_runner_rejects_changed_spomoc_module_hash(self) -> None:
        self.reject_runner(replace_once(
            self.runner, contract.SPOMOC_MODULE_SHA256, "2" * 64
        ))


if __name__ == "__main__":
    unittest.main()

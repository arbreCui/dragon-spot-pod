#!/usr/bin/env python3
"""Directed mutations for the B2y one-real-close static boundary."""

from __future__ import annotations

import re
from pathlib import Path
import subprocess
import tempfile
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
        cls.attempt_result = contract.ATTEMPT_RESULT.read_text(encoding="utf-8")
        cls.manifest = contract.MANIFEST.read_text(encoding="utf-8")
        cls.deck = contract.DECK.read_text(encoding="utf-8")
        cls.runner = contract.RUNNER.read_text(encoding="utf-8")
        cls.bounded = contract.BOUNDED.read_text(encoding="utf-8")
        cls.publisher = contract.PUBLISHER.read_text(encoding="utf-8")
        cls.host = contract.HOST.read_text(encoding="utf-8")
        cls.flu2dr = contract.FLU2DR.read_text(encoding="utf-8")

    def reject_deck(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_deck(mutated)

    def reject_attempt_result(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_attempt_result(mutated)

    def reject_manifest(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_manifest(mutated)

    def reject_runner(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_runner(mutated)

    def reject_bounded(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_bounded(mutated)

    def reject_publisher(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_publisher(mutated)

    def reject_host(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_production_host(mutated)

    def reject_flu2dr(self, mutated: str) -> None:
        with self.assertRaises(contract.GateError):
            contract.check_flu2dr(mutated)

    def test_00_positive_baseline(self) -> None:
        contract.check_attempt_result(self.attempt_result)
        contract.check_manifest(self.manifest)
        contract.check_deck(self.deck)
        contract.check_runner(self.runner)
        contract.check_bounded(self.bounded)
        contract.check_publisher(self.publisher)
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
    # canonical immutable B2z artifact; it cannot accept a same-hash copy at
    # another path, manufacture a replacement, or add a close launch site.
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
        start = self.bounded.index("def terminate_group(")
        stop = self.bounded.index("\n\ndef kill_group_at_hard_deadline", start)
        block = self.bounded[start:stop]
        self.assertEqual(block.count("signal.SIGKILL"), 1)
        changed = (
            self.bounded[:start]
            + block.replace("signal.SIGKILL", "signal.SIGTERM", 1)
            + self.bounded[stop:]
        )
        self.reject_bounded(changed)

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

    def test_48_publisher_rejects_nonexclusive_rename(self) -> None:
        self.reject_publisher(replace_once(
            self.publisher,
            "RENAME_EXCL = 0x00000004",
            "RENAME_EXCL = 0x00000000",
        ))

    def test_49_publisher_rejects_overwrite_fallback(self) -> None:
        self.reject_publisher(
            self.publisher + "\nos.replace(source, target)\n"
        )

    def test_50_runner_rejects_artifact_path_drift(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            'ARTIFACT_DIR="$ARTIFACT_PARENT/real64-phase-a9b-b2y"',
            'ARTIFACT_DIR="$ARTIFACT_PARENT/b2y-overwrite"',
        ))

    def test_51_runner_rejects_missing_activation_lock(self) -> None:
        block = (
            'if ! mkdir "$LOCK_DIR"; then\n'
            '  fail "B2y activation lock is already held"\n'
            'fi'
        )
        self.reject_runner(replace_once(self.runner, block, ":"))

    def test_52_runner_rejects_cross_filesystem_stage(self) -> None:
        old = (
            'PUBLISH_STAGE=$(mktemp -d '
            '"$ARTIFACT_PARENT/.real64-phase-a9b-b2y-publish.XXXXXX")'
        )
        new = (
            'PUBLISH_STAGE=$(mktemp -d "$' +
            '{TMPDIR:-/tmp}/real64-phase-a9b-b2y-publish.XXXXXX")'
        )
        self.reject_runner(replace_once(self.runner, old, new))

    def test_53_runner_rejects_second_publication(self) -> None:
        call = 'python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"'
        self.reject_runner(replace_once(
            self.runner, call, call + "\n" + call
        ))

    def test_54_runner_rejects_missing_closed_archive_copy(self) -> None:
        copy = (
            'copy_exact "$CASE_DIR/archive_closed.xsm" '
            '"$PUBLISH_STAGE/archive_closed.xsm"'
        )
        self.reject_runner(replace_once(self.runner, copy, ":"))

    def test_55_runner_rejects_early_staging(self) -> None:
        stage = (
            'PUBLISH_STAGE=$(mktemp -d '
            '"$ARTIFACT_PARENT/.real64-phase-a9b-b2y-publish.XXXXXX")'
        )
        without = replace_once(self.runner, stage, "")
        anchor = "verify_lineage\nverify_receipt\nverify_frozen_build_inputs"
        position = without.rfind(anchor)
        self.assertGreater(position, 0)
        changed = without[:position] + stage + "\n" + without[position:]
        self.reject_runner(changed)

    def test_56_runner_rejects_unowned_final_cleanup(self) -> None:
        guard = (
            '[ "$(stat -f \'%d:%i\' "$ARTIFACT_DIR")" = '
            '"$owned_final_id" ]'
        )
        self.reject_runner(replace_once(
            self.runner, guard, '[ -d "$ARTIFACT_DIR" ]'
        ))

    def test_57_publisher_dynamic_no_replace(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spot-b2y-publish-") as directory:
            parent = Path(directory)
            source = parent / "stage"
            target = parent / "final"
            source.mkdir()
            (source / "evidence").write_text("closed")
            before = source.stat()
            result = subprocess.run(
                ["python3", str(contract.PUBLISHER), str(source), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            after = target.stat()
            self.assertEqual(
                (before.st_dev, before.st_ino),
                (after.st_dev, after.st_ino),
            )
            source2 = parent / "stage2"
            source2.mkdir()
            (source2 / "other").write_text("other")
            rejected = subprocess.run(
                ["python3", str(contract.PUBLISHER), str(source2), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual((target / "evidence").read_text(), "closed")
            self.assertEqual((source2 / "other").read_text(), "other")

    def test_58_runner_rejects_missing_durable_attempt(self) -> None:
        block = (
            'if ! mkdir "$ATTEMPT_DIR"; then\n'
            '  fail "B2y one-real activation authorization could not be consumed"\n'
            'fi'
        )
        self.reject_runner(replace_once(self.runner, block, ":"))

    def test_59_runner_rejects_signal_window_rollback_gap(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            "owned_final_id=$PUBLISH_STAGE_ID",
            "owned_final_id=",
        ))

    def test_60_runner_rejects_noncanonical_b2z_path(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ "$B2Y_RETURNED_XSM" = "$B2Z_RETURNED" ]',
            '[ -n "$B2Y_RETURNED_XSM" ]',
        ))

    def test_61_runner_rejects_changed_b2z_receipt_hash(self) -> None:
        self.reject_runner(replace_once(
            self.runner, contract.B2Z_RECEIPT_SHA256, "3" * 64
        ))

    def test_62_runner_rejects_missing_b2z_receipt_check(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            'shasum -a 256 -c "$B2Z_RECEIPT" >/dev/null',
            ':',
        ))

    def test_63_runner_rejects_changed_b2z_manifest_hash(self) -> None:
        self.reject_runner(replace_once(
            self.runner, contract.B2Z_ARTIFACT_MANIFEST_SHA256, "4" * 64
        ))

    def test_64_runner_rejects_missing_b2z_manifest_check(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            'cd "$B2Z_ARTIFACT_DIR"\n'
            '    shasum -a 256 -c artifact_manifest.sha256 >/dev/null',
            'cd "$B2Z_ARTIFACT_DIR"\n    :',
        ))

    def test_65_runner_rejects_missing_b2z_runtime_cmp(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            'cmp "$B2Z_RUNTIME_RESULT" "$B2Z_ARTIFACT_RUNTIME_RESULT"',
            ':',
        ))

    def test_66_runner_rejects_b2z_check_after_attempt(self) -> None:
        call = "verify_b2z_staged_input"
        first = self.runner.index("\n" + call + "\n") + 1
        without = self.runner[:first] + self.runner[first + len(call) + 1:]
        anchor = 'ATTEMPT_ID=$(stat -f \'%d:%i\' "$ATTEMPT_DIR")\n'
        self.assertEqual(without.count(anchor), 1)
        changed = without.replace(anchor, anchor + call + "\n", 1)
        self.reject_runner(changed)

    def test_67_runner_rejects_missing_second_b2z_check(self) -> None:
        call = "\nverify_b2z_staged_input\n"
        last = self.runner.rfind(call)
        self.assertGreater(last, 0)
        changed = self.runner[:last] + "\n:\n" + self.runner[last + len(call):]
        self.reject_runner(changed)

    def test_68_runner_rejects_symlinked_b2z_artifact_dir(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '[ ! -L "$B2Z_ARTIFACT_DIR" ]',
            '[ -d "$B2Z_ARTIFACT_DIR" ]',
        ))

    def test_69_bounded_rejects_grace_after_hard_deadline(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded,
            "kill_group_at_hard_deadline(process)\n"
            "            fail(f\"wall timeout; {resource_class}\")",
            "terminate_group(process)\n"
            "            fail(f\"wall timeout; {resource_class}\")",
        ))

    def test_70_bounded_rejects_late_absolute_deadline(self) -> None:
        self.reject_bounded(replace_once(
            self.bounded,
            'hard_deadline = start + profile["wall_seconds"]',
            'hard_deadline = start + profile["wall_seconds"] + 5',
        ))

    def test_71_bounded_rejects_failure_cleanup_grace(self) -> None:
        start = self.bounded.index("def terminate_group(")
        stop = self.bounded.index("\n\ndef kill_group_at_hard_deadline", start)
        block = self.bounded[start:stop]
        changed_block = block.replace(
            "os.killpg(process.pid, signal.SIGKILL)",
            "os.killpg(process.pid, signal.SIGTERM)\n"
            "        time.sleep(5)\n"
            "        os.killpg(process.pid, signal.SIGKILL)",
            1,
        )
        self.reject_bounded(
            self.bounded[:start] + changed_block + self.bounded[stop:]
        )

    def test_72_bounded_rejects_census_wait_before_kill(self) -> None:
        anchor = (
            "            terminate_group(process)\n"
            "            fail(f\"RSS census failed; {resource_class}\")"
        )
        replacement = (
            "            process.wait(timeout=0.1)\n"
            "            terminate_group(process)\n"
            "            fail(f\"RSS census failed; {resource_class}\")"
        )
        self.reject_bounded(replace_once(self.bounded, anchor, replacement))

    def test_73_attempt_rejects_success_classification(self) -> None:
        self.reject_attempt_result(replace_once(
            self.attempt_result,
            "SCIENTIFIC-CLASSIFICATION=INVALID-RUNTIME-EVIDENCE",
            "SCIENTIFIC-CLASSIFICATION=ONE-REAL-SUPPLIED-RETURNED-CLOSE",
        ))

    def test_74_attempt_rejects_retry(self) -> None:
        self.reject_attempt_result(replace_once(
            self.attempt_result,
            "AUTHORIZATION=CONSUMED ATTEMPTS=1 RETRIES=0",
            "AUTHORIZATION=CONSUMED ATTEMPTS=1 RETRIES=1",
        ))

    def test_75_attempt_rejects_snapshot_drift(self) -> None:
        self.reject_attempt_result(replace_once(
            self.attempt_result,
            contract.EXECUTION_SNAPSHOT_COMMIT,
            "0" * 40,
        ))

    def test_76_attempt_rejects_wrapper_pass(self) -> None:
        self.reject_attempt_result(replace_once(
            self.attempt_result,
            "DRAGON-LAUNCHES=1 BOUNDED-WRAPPER-PASS=NO",
            "DRAGON-LAUNCHES=1 BOUNDED-WRAPPER-PASS=YES",
        ))

    def test_77_manifest_rejects_not_evaluated_runtime(self) -> None:
        self.reject_manifest(replace_once(
            self.manifest, '"status": "INVALID"',
            '"status": "NOT-EVALUATED"',
        ))

    def test_78_manifest_rejects_zero_historical_dragon(self) -> None:
        self.reject_manifest(replace_once(
            self.manifest, '"dragon_executions": 1',
            '"dragon_executions": 0',
        ))

    def test_79_manifest_rejects_accepted_closed(self) -> None:
        self.reject_manifest(replace_once(
            self.manifest, '"accepted_closed_result": false',
            '"accepted_closed_result": true',
        ))

    def test_80_runner_rejects_reactivation(self) -> None:
        self.reject_runner(replace_once(
            self.runner,
            '1) fail "B2y authorization was consumed; '
            'future B2y activation is forbidden" ;;',
            '1) ;;',
        ))


if __name__ == "__main__":
    unittest.main()

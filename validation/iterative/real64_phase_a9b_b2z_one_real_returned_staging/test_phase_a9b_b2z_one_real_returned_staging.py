#!/usr/bin/env python3
"""Directed short tests for the B2z production staging contract."""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

import check_phase_a9b_b2z_one_real_returned_staging as contract


class B2ZProductionStagingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.deck = contract.DECK.read_text()
        cls.host = contract.HOST.read_text()
        cls.adapter = contract.ADAPTER.read_text()
        cls.b2s = contract.B2S.read_text()
        cls.b2t = contract.B2T.read_text()
        cls.bounded = contract.BOUNDED.read_text()
        cls.publisher = contract.PUBLISHER.read_text()
        cls.runner = contract.RUNNER.read_text()
        cls.posterior = contract.POSTERIOR.read_text()
        cls.manifest = contract.MANIFEST.read_text()
        cls.readme = contract.README.read_text()
        cls.runtime_result = contract.RUNTIME_RESULT.read_text()
        cls.receipt = contract.RECEIPT.read_text()

    def changed(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation needle differs: {old}")
        return text.replace(old, new, 1)

    def rejected(self, function, *args) -> None:
        with self.assertRaises(contract.GateError):
            function(*args)

    def rejected_bounded(self, text: str) -> None:
        with tempfile.TemporaryDirectory(prefix="spot-b2z-bounded-") as directory:
            path = Path(directory) / "run_bounded_b2z.py"
            path.write_text(text)
            self.rejected(contract.check_bounded, path)

    def test_00_baseline(self) -> None:
        contract.check_deck(self.deck)
        contract.check_host(self.host)
        contract.check_adapter(self.adapter)
        contract.check_chain(self.b2s, self.b2t)
        contract.check_bounded(contract.BOUNDED)
        contract.check_publisher(self.publisher)
        contract.check_runner(self.runner)
        contract.check_posterior(self.posterior)
        contract.check_documents(self.manifest, self.readme)
        contract.check_frozen_result(self.runtime_result, self.manifest)
        contract.check_receipt(self.receipt)

    def test_01_second_spot_step_rejected(self) -> None:
        call = "RETURNED := SpotStepR64 PROJECTED TRACK_f :: ;"
        self.rejected(contract.check_deck,
                      self.changed(self.deck, call, call + "\n" + call))

    def test_02_deck_loop_rejected(self) -> None:
        self.rejected(contract.check_deck, self.deck + "\nWHILE 1 DO\nENDWHILE ;\n")

    def test_03_deck_axial_close_rejected(self) -> None:
        self.rejected(contract.check_deck, self.deck + "\nAX := FLU: AX :: ;\n")

    def test_04_deck_marker_drift_rejected(self) -> None:
        changed = self.changed(
            self.deck,
            "B2Z-REAL-PRODUCTION-STAGING-BEGIN",
            "B2Z-REAL-PRODUCTION-BEGIN",
        )
        self.rejected(contract.check_deck, changed)

    def test_05_fourth_asm_rejected(self) -> None:
        call = (
            "SYSTEM3 := ASM: MACRO0 TRACK TRACK_f PROJECTED ::\n"
            "  EDIT 0 ARM LK1D 3 ;"
        )
        self.rejected(contract.check_host,
                      self.changed(self.host, call, call + "\n" + call))

    def test_06_system_order_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f",
            "PROJECTED SYSTEM1 SYSTEM3 SYSTEM2 TRACK_f",
        )
        self.rejected(contract.check_host, changed)

    def test_07_adapter_observer_write_rejected(self) -> None:
        marker = "  if (status /= SPOR64_B2T_RETURNED) then"
        changed = self.changed(
            self.adapter,
            marker,
            "  write(6,*) 'B2V-OBSERVER'\n" + marker,
        )
        self.rejected(contract.check_adapter, changed)

    def test_08_adapter_second_host_step_rejected(self) -> None:
        call = (
            "  call SPOR64_B2T_HOST_STEP(kentry(1),kentry(2),systems,kentry(6), &\n"
            "      status,cutoff_by_plane,.true.)"
        )
        self.rejected(contract.check_adapter,
                      self.changed(self.adapter, call, call + "\n" + call))

    def test_09_radial_status_gate_rejected(self) -> None:
        changed = self.changed(
            self.b2s,
            "if (radial_status /= SPOR64_B2C_HOST_COMMITTED) then",
            "if (radial_status == SPOR64_B2C_HOST_COMMITTED) then",
        )
        self.rejected(contract.check_chain, changed, self.b2t)

    def test_10_dragon_wall_cap_rejected(self) -> None:
        marker = '    "dragon": {'
        start = self.bounded.index(marker)
        stop = self.bounded.index("    },", start) + len("    },")
        block = self.bounded[start:stop]
        changed = self.bounded[:start] + block.replace(
            '"wall_seconds": 60', '"wall_seconds": 61', 1
        ) + self.bounded[stop:]
        self.rejected_bounded(changed)

    def test_11_signal_cleanup_rejected(self) -> None:
        changed = self.changed(
            self.bounded,
            "    except BaseException:",
            "    except Exception:",
        )
        self.rejected_bounded(changed)

    def test_12_publisher_exclusive_flag_rejected(self) -> None:
        changed = self.changed(
            self.publisher,
            "RENAME_EXCL = 0x00000004",
            "RENAME_EXCL = 0x00000000",
        )
        self.rejected(contract.check_publisher, changed)

    def test_13_publisher_overwrite_fallback_rejected(self) -> None:
        self.rejected(contract.check_publisher, self.publisher + "\nos.replace(source, target)\n")

    def test_14_runner_default_on_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            "RUN_B2Z=$" + "{RUN_B2Z:-0}",
            "RUN_B2Z=$" + "{RUN_B2Z:-1}",
        )
        self.rejected(contract.check_runner, changed)

    def test_15_second_dragon_rejected(self) -> None:
        call = 'python3 "$BOUNDED" dragon '
        self.rejected(contract.check_runner,
                      self.changed(self.runner, call, call + call))

    def test_16_observer_compile_rejected(self) -> None:
        changed = self.runner + "\ncopy_exact observer.f90 b2z_spor64t_observer.f90\n"
        self.rejected(contract.check_runner, changed)

    def test_17_b2x_overlay_omission_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            '-o "$HOST_DIR/SPOR64_B2X.o"',
            '-o "$HOST_DIR/SPOR64_B2Y.o"',
        )
        self.rejected(contract.check_runner, changed)

    def test_18_identity_hash_drift_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            "EXPECTED_RETURNED_HASH=dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054",
            "EXPECTED_RETURNED_HASH=ed41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054",
        )
        self.rejected(contract.check_runner, changed)

    def test_19_second_publication_rejected(self) -> None:
        call = 'python3 "$PUBLISHER" "$PUBLISH_STAGE" "$ARTIFACT_DIR"'
        self.rejected(contract.check_runner,
                      self.changed(self.runner, call, call + "\n" + call))

    def test_20_cross_filesystem_stage_rejected(self) -> None:
        old = 'PUBLISH_STAGE=$(mktemp -d "$ARTIFACT_PARENT/.iterative-b2z-publish.XXXXXX")'
        new = 'PUBLISH_STAGE=$(mktemp -d "$' + \
              '{TMPDIR:-/tmp}/iterative-b2z-publish.XXXXXX")'
        self.rejected(contract.check_runner,
                      self.changed(self.runner, old, new))

    def test_21_lock_after_dragon_rejected(self) -> None:
        lock = 'if ! mkdir "$LOCK_DIR"; then\n  fail "B2z activation lock is already held"\nfi'
        self.assertEqual(self.runner.count(lock), 1)
        without = self.runner.replace(lock, "", 1)
        anchor = "DRAGON_STARTED=1"
        changed = without.replace(anchor, anchor + "\n" + lock, 1)
        self.rejected(contract.check_runner, changed)

    def test_22_owned_cleanup_guard_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            '[ "$(stat -f \'%d:%i\' "$ARTIFACT_DIR")" = "$owned_final_id" ]',
            '[ -d "$ARTIFACT_DIR" ]',
        )
        self.rejected(contract.check_runner, changed)

    def test_23_automatic_b2y_rejected(self) -> None:
        self.rejected(contract.check_runner, self.runner + "\nRUN_B2Y=1\n")

    def test_24_publisher_fresh_dynamic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spot-b2z-publish-") as directory:
            parent = Path(directory)
            source = parent / "stage"
            target = parent / "final"
            source.mkdir()
            (source / "evidence").write_text("fixed")
            before = source.stat()
            result = subprocess.run(
                ["python3", str(contract.PUBLISHER), str(source), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(source.exists())
            after = target.stat()
            self.assertEqual((before.st_dev, before.st_ino),
                             (after.st_dev, after.st_ino))
            self.assertEqual((target / "evidence").read_text(), "fixed")

    def test_25_publisher_existing_target_dynamic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="spot-b2z-publish-") as directory:
            parent = Path(directory)
            source = parent / "stage"
            target = parent / "final"
            source.mkdir()
            target.mkdir()
            (source / "source").write_text("source")
            (target / "target").write_text("target")
            result = subprocess.run(
                ["python3", str(contract.PUBLISHER), str(source), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((source / "source").read_text(), "source")
            self.assertEqual((target / "target").read_text(), "target")

    def test_26_runner_patch_residue_rejected(self) -> None:
        self.rejected(
            contract.check_runner,
            self.runner.replace("&& \\\n     [ ! -L", "&& +     [ ! -L", 1),
        )

    def test_27_runner_symbol_loop_duplication_rejected(self) -> None:
        line = (
            "for symbol in spor64_a9_MOD_flu2dr64_core "
            "spor64_a8_MOD_doorfv64"
        )
        self.rejected(
            contract.check_runner,
            self.changed(self.runner, line, line + "\n" + line),
        )

    def test_28_runner_missing_durable_attempt_rejected(self) -> None:
        block = (
            'if ! mkdir "$ATTEMPT_DIR"; then\n'
            '  fail "B2z one-real activation authorization could not be consumed"\n'
            'fi'
        )
        self.rejected(
            contract.check_runner,
            self.changed(self.runner, block, ":"),
        )

    def test_29_runner_signal_window_rollback_rejected(self) -> None:
        self.rejected(
            contract.check_runner,
            self.changed(
                self.runner,
                "owned_final_id=$PUBLISH_STAGE_ID",
                "owned_final_id=",
            ),
        )

    def test_30_manifest_durable_attempt_drift_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"removed_after_failure": false',
            '"removed_after_failure": true',
        )
        self.rejected(contract.check_documents, changed, self.readme)

    def test_31_runtime_result_drift_rejected(self) -> None:
        changed = self.changed(
            self.runtime_result,
            "DRAGON-EXECUTIONS=1 SPOTSTEPR64-CALLS=1",
            "DRAGON-EXECUTIONS=2 SPOTSTEPR64-CALLS=1",
        )
        self.rejected(contract.check_frozen_result, changed, self.manifest)

    def test_32_manifest_frozen_result_drift_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"radial_cont_returns": 3',
            '"radial_cont_returns": 2',
        )
        self.rejected(
            contract.check_frozen_result,
            self.runtime_result,
            changed,
        )

    def test_33_receipt_hash_drift_rejected(self) -> None:
        lines = self.receipt.splitlines()
        self.assertGreater(len(lines), 1)
        replacement = ("0" if lines[0][0] != "0" else "1") + lines[0][1:]
        changed = "\n".join([replacement, *lines[1:]]) + "\n"
        self.rejected(contract.check_receipt, changed)

    def test_34_receipt_inventory_drift_rejected(self) -> None:
        lines = self.receipt.splitlines()
        self.rejected(contract.check_receipt, "\n".join(lines[:-1]) + "\n")


if __name__ == "__main__":
    unittest.main()

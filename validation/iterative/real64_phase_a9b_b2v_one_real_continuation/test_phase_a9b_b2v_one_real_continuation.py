#!/usr/bin/env python3
"""Targeted mutation tests for the bounded B2v static contract."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import check_phase_a9b_b2v_one_real_continuation as contract


class B2VOneRealContinuationMutationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.observer = contract.OBSERVER.read_text(encoding="utf-8")
        cls.production = contract.PRODUCTION_ADAPTER.read_text(encoding="utf-8")
        cls.deck = contract.DECK.read_text(encoding="utf-8")
        cls.host = contract.HOST.read_text(encoding="utf-8")
        cls.b2s = contract.B2S.read_text(encoding="utf-8")
        cls.b2t = contract.B2T.read_text(encoding="utf-8")
        cls.bounded = contract.BOUNDED.read_text(encoding="utf-8")
        cls.runner = contract.RUNNER.read_text(encoding="utf-8")
        cls.posterior = contract.POSTERIOR.read_text(encoding="utf-8")
        cls.runtime_result = contract.RUNTIME_RESULT.read_text(encoding="utf-8")
        cls.manifest = contract.MANIFEST.read_text(encoding="utf-8")
        cls.phase_readme = contract.README.read_text(encoding="utf-8")
        cls.root_readme = contract.ROOT_README.read_text(encoding="utf-8")
        cls.iterative_readme = contract.ITERATIVE_README.read_text(encoding="utf-8")

    def changed(self, text: str, old: str, new: str) -> str:
        self.assertEqual(text.count(old), 1, f"mutation needle differs: {old}")
        return text.replace(old, new, 1)

    def rejected(self, function, *arguments: str) -> None:
        with self.assertRaises(contract.GateError):
            function(*arguments)

    def rejected_bounded(self, text: str) -> None:
        with tempfile.TemporaryDirectory(prefix="spot-b2v-test-") as directory:
            path = Path(directory) / "run_bounded_b2v.py"
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(contract.GateError):
                contract.check_bounded(path)

    def changed_dragon_cap(self, old: str, new: str) -> str:
        marker = '    "dragon": {'
        start = self.bounded.index(marker)
        stop = self.bounded.index("    },", start) + len("    },")
        block = self.bounded[start:stop]
        self.assertEqual(block.count(old), 1, f"Dragon cap needle differs: {old}")
        return self.bounded[:start] + block.replace(old, new, 1) + self.bounded[stop:]

    def test_00_baseline(self) -> None:
        contract.check_observer(self.observer, self.production)
        contract.check_deck(self.deck)
        contract.check_host(self.host)
        contract.check_chain(self.b2s, self.b2t)
        contract.check_bounded(contract.BOUNDED)
        contract.check_runner(self.runner)
        contract.check_posterior(self.posterior)
        contract.check_frozen_result(
            self.runtime_result,
            self.manifest,
            self.phase_readme,
            self.root_readme,
            self.iterative_readme,
        )

    # The validation observer may report the three counters, but may neither
    # branch on them, aggregate them, nor move the write across status dispatch.
    def test_01_observer_conditional_write_rejected(self) -> None:
        changed = self.changed(
            self.observer,
            "  write(6,'(A,I0,A,I0,A,I0,A,I0)') 'B2V-OBSERVER STATUS=',status, &",
            "  if (status == SPOR64_B2T_RETURNED) then\n"
            "  write(6,'(A,I0,A,I0,A,I0,A,I0)') 'B2V-OBSERVER STATUS=',status, &",
        )
        changed = self.changed(
            changed,
            "  ! B2V_OBSERVER_END",
            "  end if\n  ! B2V_OBSERVER_END",
        )
        self.rejected(contract.check_observer, changed, self.production)

    def test_02_observer_cutoff_aggregation_rejected(self) -> None:
        changed = self.changed(
            self.observer,
            "cutoff_by_plane(1), &",
            "sum(cutoff_by_plane), &",
        )
        self.rejected(contract.check_observer, changed, self.production)

    def test_03_observer_after_status_dispatch_rejected(self) -> None:
        begin = self.observer.index("  ! B2V_OBSERVER_BEGIN")
        end_marker = "  ! B2V_OBSERVER_END"
        end = self.observer.index(end_marker, begin) + len(end_marker)
        block = self.observer[begin:end]
        without = self.observer[:begin] + self.observer[end:]
        status_block = (
            "  if (status /= SPOR64_B2T_RETURNED) then\n"
            "    call XABORT('SPOR64T: B2T OWNED HOST STEP FAILED.')\n"
            "    return\n"
            "  end if"
        )
        moved = self.changed(without, status_block, status_block + "\n\n" + block)
        self.rejected(contract.check_observer, moved, self.production)

    def test_04_observer_cannot_change_production_adapter_rejected(self) -> None:
        changed = self.changed(
            self.observer,
            "  if (nentry /= 6) then",
            "  if (nentry /= 5) then",
        )
        self.rejected(contract.check_observer, changed, self.production)

    # The deck owns exactly one projected-to-returned call and no iteration or
    # axial module.  Evidence publication must remain after the returned call.
    def test_05_deck_second_host_call_rejected(self) -> None:
        call = "RETURNED := SpotStepR64 PROJECTED TRACK_f :: ;"
        changed = self.changed(self.deck, call, call + "\n" + call)
        self.rejected(contract.check_deck, changed)

    def test_06_deck_loop_rejected(self) -> None:
        changed = self.deck + "\nWHILE 0 1 < DO\nENDWHILE ;\n"
        self.rejected(contract.check_deck, changed)

    def test_07_deck_axial_module_rejected(self) -> None:
        changed = self.deck + "\nAX := FLU: AX :: ;\n"
        self.rejected(contract.check_deck, changed)

    def test_08_deck_evidence_before_return_rejected(self) -> None:
        evidence = "RET_XSM := RETURNED ;\n"
        without = self.changed(self.deck, evidence, "")
        call = "RETURNED := SpotStepR64 PROJECTED TRACK_f :: ;"
        changed = self.changed(without, call, evidence + call)
        self.rejected(contract.check_deck, changed)

    # SpotStepR64 must assemble each canonical plane once, then dispatch the
    # three still-live systems in the same order.
    def test_09_host_plane_index_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "EDIT 0 ARM LK1D 2 ;",
            "EDIT 0 ARM LK1D 3 ;",
        )
        self.rejected(contract.check_host, changed)

    def test_10_host_dispatch_order_rejected(self) -> None:
        changed = self.changed(
            self.host,
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM2 SYSTEM3 TRACK_f :: ;",
            "RETURNED := SPOR64T: PROJECTED SYSTEM1 SYSTEM3 SYSTEM2 TRACK_f :: ;",
        )
        self.rejected(contract.check_host, changed)

    def test_11_host_fourth_asm_rejected(self) -> None:
        call = (
            "SYSTEM3 := ASM: MACRO0 TRACK TRACK_f PROJECTED ::\n"
            "  EDIT 0 ARM LK1D 3 ;"
        )
        changed = self.changed(self.host, call, call + "\n" + call)
        self.rejected(contract.check_host, changed)

    # B2S is the strict owner of the per-plane continuation status and
    # diagnostic counter binding.  Neither can be weakened or duplicated.
    def test_12_b2s_status_gate_rejected(self) -> None:
        changed = self.changed(
            self.b2s,
            "if (radial_status /= SPOR64_B2C_HOST_COMMITTED) then",
            "if (radial_status == SPOR64_B2C_HOST_COMMITTED) then",
        )
        self.rejected(contract.check_chain, changed, self.b2t)

    def test_13_b2s_cutoff_plane_binding_rejected(self) -> None:
        changed = self.changed(
            self.b2s,
            "cutoff_by_plane(plane))",
            "cutoff_by_plane(slot))",
        )
        self.rejected(contract.check_chain, changed, self.b2t)

    def test_14_b2s_second_radial_call_site_rejected(self) -> None:
        call = "call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &"
        changed = self.changed(self.b2s, call, call + "\n" + call)
        self.rejected(contract.check_chain, changed, self.b2t)

    # Runtime activation stays explicit, one-shot, and scoped to its own
    # process group.  Textual retry or broad termination paths fail closed.
    def test_15_runner_default_on_rejected(self) -> None:
        changed = self.changed(
            self.runner,
            "RUN_B2V=${RUN_B2V:-0}",
            "RUN_B2V=${RUN_B2V:-1}",
        )
        self.rejected(contract.check_runner, changed)

    def test_16_runner_second_dragon_rejected(self) -> None:
        activation = 'python3 "$BOUNDED" dragon '
        changed = self.changed(self.runner, activation, activation + activation)
        self.rejected(contract.check_runner, changed)

    def test_17_runner_killall_rejected(self) -> None:
        changed = self.runner + "\nkillall Dragon\n"
        self.rejected(contract.check_runner, changed)

    def test_18_runner_missing_no_retry_classification_rejected(self) -> None:
        self.assertIn("NO-RETRY", self.runner)
        changed = self.runner.replace("NO-RETRY", "NO_RETRY")
        self.rejected(contract.check_runner, changed)

    def test_19_manifest_private_dragon_hash_drift_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"private_dragon_sha256": "cda682f5ee2579acbf901b394d06ed6e37fd815077e233e358da22c76eb9bb1f"',
            '"private_dragon_sha256": "dda682f5ee2579acbf901b394d06ed6e37fd815077e233e358da22c76eb9bb1f"',
        )
        self.rejected(
            contract.check_frozen_result,
            self.runtime_result,
            changed,
            self.phase_readme,
            self.root_readme,
            self.iterative_readme,
        )

    # Every frozen Dragon cap is part of the scientific scope.  Changing any
    # one, including the group-termination grace, invalidates the static gate.
    def test_20_bounded_wall_cap_rejected(self) -> None:
        self.rejected_bounded(
            self.changed_dragon_cap('"wall_seconds": 60', '"wall_seconds": 61')
        )

    def test_21_bounded_cpu_cap_rejected(self) -> None:
        self.rejected_bounded(
            self.changed_dragon_cap('"cpu_seconds": 55', '"cpu_seconds": 56')
        )

    def test_22_bounded_rss_cap_rejected(self) -> None:
        self.rejected_bounded(
            self.changed_dragon_cap(
                '"rss_bytes": 2 * 1024**3',
                '"rss_bytes": 3 * 1024**3',
            )
        )

    def test_23_bounded_file_cap_rejected(self) -> None:
        self.rejected_bounded(
            self.changed_dragon_cap(
                '"file_bytes": 512 * 1024**2',
                '"file_bytes": 513 * 1024**2',
            )
        )

    def test_24_bounded_log_cap_rejected(self) -> None:
        self.rejected_bounded(
            self.changed_dragon_cap(
                '"log_bytes": 64 * 1024**2',
                '"log_bytes": 65 * 1024**2',
            )
        )

    def test_25_bounded_termination_grace_rejected(self) -> None:
        changed = self.changed(
            self.bounded,
            "TERM_GRACE_SECONDS = 5",
            "TERM_GRACE_SECONDS = 6",
        )
        self.rejected_bounded(changed)

    def test_26_bounded_live_log_census_rejected(self) -> None:
        changed = self.changed(
            self.bounded,
            '        if log_bytes > profile["log_bytes"]:',
            '        if log_bytes > profile["file_bytes"]:',
        )
        self.rejected_bounded(changed)

    def test_27_bounded_resource_signal_classification_rejected(self) -> None:
        changed = self.changed(
            self.bounded,
            "            signal.SIGXCPU,",
            "            signal.SIGUSR1,",
        )
        self.rejected_bounded(changed)

    def test_28_bounded_posterior_resource_class_rejected(self) -> None:
        needle = '    "posterior": "INVALID-RETURNED-EVIDENCE",'
        self.assertEqual(self.bounded.count(needle), 2)
        changed = self.bounded.replace(
            needle, '    "posterior": "FAILED-NO-RETURN",', 1
        )
        self.rejected_bounded(changed)

    def test_29_bounded_dragon_exit_class_rejected(self) -> None:
        changed = self.changed(
            self.bounded,
            '    "dragon": "FAILED-NO-RETURN",',
            '    "dragon": "INVALID-NO-SCIENTIFIC-RESULT",',
        )
        self.rejected_bounded(changed)

    def test_30_runtime_cutoff_drift_rejected(self) -> None:
        changed = self.changed(
            self.runtime_result,
            "CUTOFF-P1=59 CUTOFF-P2=138 CUTOFF-P3=126",
            "CUTOFF-P1=59 CUTOFF-P2=138 CUTOFF-P3=127",
        )
        self.rejected(
            contract.check_frozen_result,
            changed,
            self.manifest,
            self.phase_readme,
            self.root_readme,
            self.iterative_readme,
        )

    def test_31_runtime_outer_overclaim_rejected(self) -> None:
        changed = self.changed(
            self.runtime_result,
            "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
            "OUTER-PICARD-CONVERGENCE=CONVERGED",
        )
        self.rejected(
            contract.check_frozen_result,
            changed,
            self.manifest,
            self.phase_readme,
            self.root_readme,
            self.iterative_readme,
        )

    def test_32_manifest_returned_hash_drift_rejected(self) -> None:
        changed = self.changed(
            self.manifest,
            '"returned_sha256": "dd41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054"',
            '"returned_sha256": "ed41a37d484b85612a495ff7b1f2233a53fbae1b462d89bd84db2a8809cef054"',
        )
        self.rejected(
            contract.check_frozen_result,
            self.runtime_result,
            changed,
            self.phase_readme,
            self.root_readme,
            self.iterative_readme,
        )

    def test_33_phase_readme_elapsed_drift_rejected(self) -> None:
        changed = self.changed(self.phase_readme, "16.332", "16.333")
        self.rejected(
            contract.check_frozen_result,
            self.runtime_result,
            self.manifest,
            changed,
            self.root_readme,
            self.iterative_readme,
        )


if __name__ == "__main__":
    unittest.main()

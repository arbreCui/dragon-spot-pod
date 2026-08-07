#!/usr/bin/env python3
"""Mutation tests for the fail-closed B2n static contract."""

from __future__ import annotations

from copy import deepcopy
import json
import re
import unittest

import check_phase_a9b_b2n_real64_frozen_qfiss as gate


class B2nContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = gate.SOURCE.read_text()
        cls.builder = gate.BUILDER.read_text()
        cls.posterior = gate.POSTERIOR.read_text()
        cls.bounded = gate.BOUNDED.read_text()
        cls.runner = gate.RUNNER.read_text()
        cls.manifest = json.loads(gate.MANIFEST.read_text())
        cls.runtime = gate.RUNTIME_RESULT.read_text()
        cls.readme = gate.README.read_text()
        cls.root_readme = gate.ROOT_README.read_text()
        cls.iterative_readme = gate.ITERATIVE_README.read_text()
        cls.makefile = gate.MAKEFILE.read_text()

    def rejected(self, function, value) -> None:
        with self.assertRaises(gate.GateError):
            function(value)

    def test_01_baseline_source(self) -> None:
        gate.check_source(self.source)

    def test_02_baseline_builder(self) -> None:
        gate.check_builder(self.builder)

    def test_03_baseline_posterior(self) -> None:
        gate.check_posterior(self.posterior)

    def test_04_baseline_bounded_runner(self) -> None:
        gate.check_bounded(self.bounded)

    def test_05_baseline_shell_runner(self) -> None:
        gate.check_runner(self.runner)

    def test_06_baseline_manifest(self) -> None:
        gate.check_manifest(self.manifest)

    def test_07_missing_preflight_status_rejected(self) -> None:
        text = re.sub(
            r"SPOR64_B2N_PREFLIGHT_FAILED", "SPOR64_B2N_UNKNOWN",
            self.source, count=1, flags=re.I,
        )
        self.rejected(gate.check_source, text)

    def test_08_duplicate_commit_rejected(self) -> None:
        match = re.search(
            r"status\s*=\s*SPOR64_B2N_COMMITTED", self.source, re.I
        )
        self.assertIsNotNone(match)
        text = self.source[: match.end()] + "\nstatus=SPOR64_B2N_COMMITTED" + self.source[match.end():]
        self.rejected(gate.check_source, text)

    def test_09_wrong_authority_state_rejected(self) -> None:
        text = self.source.replace("FROZEN-QFIS", "SOLVED      ", 1)
        self.rejected(gate.check_source, text)

    def test_10_missing_type4_publication_rejected(self) -> None:
        text = re.sub(r",\s*4\s*,", ",2,", self.source)
        self.rejected(gate.check_source, text)

    def test_11_root_real32_flux_fallback_rejected(self) -> None:
        text = re.sub(
            r"(?i)(end\s+subroutine\s+SPOR64_B2N_BUILD)",
            "jpflux=LCMGID(ipflux,'FLUX')\n\\1", self.source, count=1,
        )
        self.rejected(gate.check_source, text)

    def test_12_flu_call_rejected(self) -> None:
        text = re.sub(
            r"(?i)(end\s+subroutine\s+SPOR64_B2N_BUILD)",
            "call FLU()\n\\1", self.source, count=1,
        )
        self.rejected(gate.check_source, text)

    def test_13_missing_region_loop_rejected(self) -> None:
        formula_start = self.source.lower().find("q64 = +0.0_real64")
        self.assertGreaterEqual(formula_start, 0)
        prefix = self.source[:formula_start]
        formula_and_tail = self.source[formula_start:]
        formula_and_tail, replacements = re.subn(
            r"(?i)\bdo\s+(ir|ireg)\s*=\s*1\s*,\s*NREG",
            "if (.true.) then", formula_and_tail, count=1,
        )
        self.assertEqual(replacements, 1)
        text = prefix + formula_and_tail
        self.rejected(gate.check_source, text)

    def test_14_missing_recursive_copy_rejected(self) -> None:
        text = re.sub(r"(?i)\bLCMEQU\b", "LCM_NO_COPY", self.source)
        self.rejected(gate.check_source, text)

    def test_15_builder_call_removed_rejected(self) -> None:
        text = re.sub(r"(?i)CALL\s+SPOR64_B2N_BUILD", "CALL REMOVED", self.builder, count=1)
        self.rejected(gate.check_builder, text)

    def test_16_builder_call_duplicated_rejected(self) -> None:
        match = re.search(r"(?i)CALL\s+SPOR64_B2N_BUILD\s*\([^\n]+", self.builder)
        self.assertIsNotNone(match)
        text = self.builder[:match.end()] + "\n" + match.group(0) + self.builder[match.end():]
        self.rejected(gate.check_builder, text)

    def test_17_builder_plane_two_rejected(self) -> None:
        text = re.sub(
            r"(?i)SPOR64_B2N_BUILD\s*\(\s*PROJECTED\s*,\s*1\s*,",
            "SPOR64_B2N_BUILD(PROJECTED,2,", self.builder, count=1,
        )
        self.rejected(gate.check_builder, text)

    def test_18_posterior_producer_link_rejected(self) -> None:
        text = self.posterior.replace("use GANLIB", "use GANLIB\nuse SPOR64_B2N", 1)
        self.rejected(gate.check_posterior, text)

    def test_19_posterior_qfiss_count_rejected(self) -> None:
        text = self.posterior.replace("5180", "5179")
        self.rejected(gate.check_posterior, text)

    def test_20_bounded_build_profile_removed_rejected(self) -> None:
        text = re.sub(r'(?ms)^\s*"build"\s*:\s*\{.*?^\s*\},', "", self.bounded, count=1)
        self.rejected(gate.check_bounded, text)

    def test_21_bounded_cpu_cap_changed_rejected(self) -> None:
        text = self.bounded.replace('"cpu_seconds": 20', '"cpu_seconds": 21', 1)
        self.rejected(gate.check_bounded, text)

    def test_22_runtime_default_on_rejected(self) -> None:
        text = self.runner.replace("RUN_B2N=${RUN_B2N:-0}", "RUN_B2N=${RUN_B2N:-1}", 1)
        self.rejected(gate.check_runner, text)

    def test_23_duplicate_real_build_rejected(self) -> None:
        needle = 'python3 "$BOUNDED" build'
        text = self.runner.replace(needle, needle + "\n" + needle, 1)
        self.rejected(gate.check_runner, text)

    def test_24_nested_b2m_runtime_rejected(self) -> None:
        self.rejected(gate.check_runner, self.runner + "\nRUN_B2M=1\n")

    def test_25_manifest_relaxation_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["formula"]["relaxation_or_damping"] = True
        self.rejected(gate.check_manifest, data)

    def test_26_manifest_loop_reorder_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["formula"]["loop_order"][2:] = list(reversed(data["formula"]["loop_order"][2:]))
        self.rejected(gate.check_manifest, data)

    def test_27_manifest_flu_execution_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["execution_policy"]["flu_executions"] = 1
        self.rejected(gate.check_manifest, data)

    def test_28_docs_missing_b2n_rejected(self) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_docs(
                self.readme, self.root_readme.replace("B2n", "BXX"),
                self.iterative_readme, self.makefile,
            )

    def test_29_make_target_removed_rejected(self) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_docs(
                self.readme, self.root_readme, self.iterative_readme,
                self.makefile.replace(
                    "spot-real64-phase-a9b-b2n-real64-frozen-qfiss", "removed"
                ),
            )

    def test_30_production_wrong_chi_operand_rejected(self) -> None:
        text = self.source.replace(
            "real(chi32(im,ifis,g),real64) * fis64",
            "real(nusigf32(im,ifis,g),real64) * fis64", 1,
        )
        self.rejected(gate.check_source, text)

    def test_31_production_missing_rho_rejected(self) -> None:
        text = self.source.replace(
            "contribution64 = contribution64 * rho64",
            "contribution64 = contribution64 * 1.0_real64", 1,
        )
        self.rejected(gate.check_source, text)

    def test_32_production_old_group_index_rejected(self) -> None:
        text = self.source.replace("phi64(iu,h)", "phi64(iu,g)", 1)
        self.rejected(gate.check_source, text)

    def test_33_posterior_wrong_chi_operand_rejected(self) -> None:
        text = self.posterior.replace(
            "real(chi32(ibm,ifis,g),real64)*fission_rate",
            "real(nusigf32(ibm,ifis,g),real64)*fission_rate", 1,
        )
        self.rejected(gate.check_posterior, text)

    def test_34_posterior_qfiss_self_comparison_rejected(self) -> None:
        text = self.posterior.replace(
            "expected64_bits=transfer(qfiss(:,g),0_int64,NUNKNO)",
            "expected64_bits=transfer(authority_qfiss,0_int64,NUNKNO)", 1,
        )
        self.rejected(gate.check_posterior, text)

    def test_35_posterior_dsour_self_comparison_rejected(self) -> None:
        text = self.posterior.replace(
            "expected32_bits=transfer(real(qfiss(:,g),real32),0_int32,NUNKNO)",
            "expected32_bits=transfer(dsour32,0_int32,NUNKNO)", 1,
        )
        self.rejected(gate.check_posterior, text)

    def test_36_posterior_qint_self_comparison_rejected(self) -> None:
        text = self.posterior.replace(
            "expected_qint32=real(qint,real32)",
            "expected_qint32=qint32", 1,
        )
        self.rejected(gate.check_posterior, text)

    def test_37_all_fresh_root_guards_removed_rejected(self) -> None:
        text = re.sub(
            r"(?im)^\s*if\s*\(\.not\.\s*EMPTY_LCM_ROOT\([^\n]+\)\s*return\s*$",
            "", self.source,
        )
        self.rejected(gate.check_source, text)

    def test_38_output_mutation_after_epoch_rejected(self) -> None:
        needle = "status = SPOR64_B2N_COMMITTED"
        replacement = (
            "call LCMPUT(ipsource_out,'LATE-WRITE',1,1,status)\n    " + needle
        )
        text = self.source.replace(needle, replacement, 1)
        self.rejected(gate.check_source, text)

    def test_39_writable_posterior_open_rejected(self) -> None:
        text = self.posterior.replace(",2,2,0)", ",1,2,0)")
        self.rejected(gate.check_posterior, text)

    def test_40_builder_log_count_change_rejected(self) -> None:
        text = self.runner.replace('-eq 5 ]', '-eq 4 ]', 1)
        self.rejected(gate.check_runner, text)

    def test_41_manifest_default_on_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["execution_policy"]["runtime_default_off"] = False
        self.rejected(gate.check_manifest, data)

    def test_42_manifest_posterior_repeatability_removed_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["posterior_contract"]["posterior_outputs_byte_identical"] = False
        self.rejected(gate.check_manifest, data)

    def test_43_tiny_formula_anchor(self) -> None:
        rho = 0.5
        phi = [2.0, 3.0]
        nusigf = [[1.0, 2.0], [3.0, 4.0]]
        chi = [[5.0, 7.0], [6.0, 8.0]]
        q = [0.0, 0.0]
        for fissile in range(2):
            rate = 0.0
            for old_group in range(2):
                rate += nusigf[fissile][old_group] * phi[old_group]
            for destination_group in range(2):
                q[destination_group] += (
                    chi[fissile][destination_group] * rate
                ) * rho
        self.assertEqual(q, [74.0, 100.0])

    def test_44_manifest_output_hash_change_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["accepted_runtime"]["fsource_sha256"] = "0" * 64
        self.rejected(gate.check_manifest, data)

    def test_45_runtime_time_mismatch_rejected(self) -> None:
        text = self.runtime.replace(
            "ACCEPTED-RUN-BUILD-WALL-SECONDS=0.695",
            "ACCEPTED-RUN-BUILD-WALL-SECONDS=0.696", 1,
        )
        with self.assertRaises(gate.GateError):
            gate.check_runtime_result(text, self.manifest)

    def test_46_manifest_dsour_count_change_rejected(self) -> None:
        data = deepcopy(self.manifest)
        data["posterior_contract"]["dsour_binary32_projection_checks"] = 1
        self.rejected(gate.check_manifest, data)


if __name__ == "__main__":
    unittest.main()

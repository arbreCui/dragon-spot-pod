#!/usr/bin/env python3
"""Targeted fail-closed mutations for the B2b ingress gate."""

from __future__ import annotations

import copy
import json
import re
import unittest

import check_phase_a9b_b2b_ingress as gate


class B2bSourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.flu = gate.FLU.read_text()
        cls.flugpi = gate.FLUGPI.read_text()
        cls.b2b = gate.B2B.read_text()

    def rejected_flu(self, text: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_flu(text)

    def rejected_b2b(self, text: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_ingress(text)

    def rejected_flugpi(self, text: str) -> None:
        with self.assertRaises(gate.GateError):
            gate.check_flugpi(text)

    @staticmethod
    def replace_ci(text: str, pattern: str, replacement: str) -> str:
        updated, count = re.subn(pattern, replacement, text, count=1,
                                 flags=re.IGNORECASE)
        if count != 1:
            raise AssertionError(f"mutation anchor count for {pattern!r}")
        return updated

    def test_unmodified_contract_passes(self) -> None:
        gate.check_flu(self.flu)
        gate.check_ingress(self.b2b)

    def test_flu_cannot_drop_ingress(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu, r"CALL\s+SPOR64_B2B_INGRESS", "CALL B2B_REMOVED",
        ))

    def test_flu_cannot_duplicate_ingress(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu, r"CALL\s+SPOR64_B2B_INGRESS",
            "CALL SPOR64_B2B_INGRESS\n      CALL SPOR64_B2B_INGRESS",
        ))

    def test_flu_selected_branch_cannot_write_lcm(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu, r"(\n\s*DEALLOCATE\(IMERG\)\s*\n\s*RETURN\s*\n\s*ENDIF)",
            "\n        CALL LCMPUT(IPFLUX,'B2B-BAD',1,1,IB2STAT)\\1",
        ))

    def test_flu_selected_branch_cannot_call_legacy_driver(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu, r"(\n\s*DEALLOCATE\(IMERG\))",
            "\n        CALL FLUDRV()\\1",
        ))

    def test_flu_selected_branch_must_return(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu,
            r"(DEALLOCATE\(IMERG\)\s*)RETURN(\s*\n\s*ENDIF\s*\n\*----\s*\n\*  COMMIT)",
            r"\1\2",
        ))

    def test_legacy_xdrta2_cannot_take_an_actual(self) -> None:
        self.rejected_flu(self.replace_ci(
            self.flu, r"CALL\s+XDRTA2(?!\s*\()", "CALL XDRTA2(IPTRK)",
        ))

    def test_ingress_abi_cannot_expand(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"cutoff_visit64\s*\)",
            "cutoff_visit64, empirical_alpha)",
        ))

    def test_topology_count_is_exact(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"nentry\s*/=\s*6", "nentry /= 7",
        ))

    def test_flux_state_guard_cannot_be_deleted(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b,
            r"if\s*\(\.not\.\s*RECORD_MATCHES\(ipflux,'STATE-VECTOR',NSTATE,1\)\)\s*return",
            "continue",
        ))

    def test_pre_admission_operator_is_rejected(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"call MCGFL1()\n    \1",
        ))

    def test_core_source_and_flux_order_is_exact(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"fixed_source64,initial_flux64",
            "initial_flux64,fixed_source64",
        ))

    def test_terminal_status_mapping_is_exact(self) -> None:
        text = self.replace_ci(
            self.b2b, r"status\s*=\s*SPOR64_B2B_CORE_FAILED",
            "status = B2B_STATUS_SWAP",
        )
        text = self.replace_ci(
            text, r"status\s*=\s*SPOR64_B2B_NOT_ACCEPTED",
            "status = SPOR64_B2B_CORE_FAILED",
        )
        text = self.replace_ci(
            text, r"status\s*=\s*B2B_STATUS_SWAP",
            "status = SPOR64_B2B_NOT_ACCEPTED",
        )
        self.rejected_b2b(text)

    def test_admission_latch_cannot_start_true(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"admission_complete\s*=\s*\.false\.",
            "admission_complete = .true.",
        ))

    def test_admission_latch_cannot_be_omitted(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"admission_complete\s*=\s*\.true\.",
            "admission_complete = .false.",
        ))

    def test_host_read_cannot_follow_complete_admission(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"\1\n    call LCMGET(kentry(1),'BAD',status)",
        ))

    def test_ingress_cannot_write_lcm(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"call LCMPUT(kentry(1),'BAD',1,1,status)\n    \1",
        ))

    def test_ingress_cannot_hide_a_bare_lcm_write(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"call LCMDEL\n    \1",
        ))

    def test_ingress_cannot_xabort(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"call XABORT('BAD')\n    \1",
        ))

    def test_ingress_cannot_read_tracking_stream(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"read(iftrak) status\n    \1",
        ))

    def test_ingress_cannot_rewind_tracking_stream(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(admission_complete\s*=\s*\.true\.)",
            r"rewind(iftrak)\n    \1",
        ))

    def test_ingress_cannot_save_state(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"(implicit\s+none)", r"\1\n  save",
        ))

    def test_xdrta2_cannot_take_an_actual(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"CALL\s+XDRTA2(?:\s*\(\s*\))?",
            "call XDRTA2(iptrk)",
        ))

    def test_xdrta2_call_syntax_is_canonical_bare(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"CALL\s+XDRTA2(?!\s*\()", "call XDRTA2()",
        ))

    def test_xdrta2_cannot_be_duplicated(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"CALL\s+XDRTA2(?:\s*\(\s*\))?",
            "call XDRTA2\n    call XDRTA2",
        ))

    def test_core_cannot_be_duplicated(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"CALL\s+FLU2DR64_CORE\s*\(",
            "call FLU2DR64_CORE()\n    call FLU2DR64_CORE(",
        ))

    def test_core_cannot_precede_xdrta2(self) -> None:
        text = self.replace_ci(self.b2b, r"CALL\s+XDRTA2", "call B2B_SWAP")
        text = self.replace_ci(text, r"CALL\s+FLU2DR64_CORE", "call XDRTA2")
        text = self.replace_ci(text, r"CALL\s+B2B_SWAP", "call FLU2DR64_CORE")
        self.rejected_b2b(text)

    def test_extra_post_admission_call_is_rejected(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"CALL\s+XDRTA2(?:\s*\(\s*\))?",
            "call SIDE_EFFECT()\n    call XDRTA2",
        ))

    def test_status_values_are_exact(self) -> None:
        self.rejected_b2b(self.replace_ci(
            self.b2b, r"SPOR64_B2B_CORE_FAILED\s*=\s*2\b",
            "SPOR64_B2B_CORE_FAILED = 7",
        ))

    def test_flugpi_state_guard_cannot_be_weakened(self) -> None:
        self.rejected_flugpi(self.replace_ci(
            self.flugpi,
            r"\(ILCML1\.NE\.NSTATE\)\.OR\.\(ITYLCM\.NE\.1\)",
            "(ILCML1.NE.NSTATE)",
        ))

    def test_flugpi_idem_type_guard_cannot_be_weakened(self) -> None:
        self.rejected_flugpi(self.replace_ci(
            self.flugpi,
            r"\(\(ILCMLN\.EQ\.3\)\.AND\.\(ITYLCM\.EQ\.2\)\)",
            "(ILCMLN.EQ.3)",
        ))


class MetadataContractTests(unittest.TestCase):
    def test_unmodified_manifest_passes(self) -> None:
        gate.check_manifest(json.loads(gate.MANIFEST.read_text()))

    def test_manifest_cannot_claim_publication(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        mutated = copy.deepcopy(data)
        mutated["status"]["accepted_publication_implemented"] = True
        with self.assertRaises(gate.GateError):
            gate.check_manifest(mutated)

    def test_manifest_cannot_claim_convergence(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        mutated = copy.deepcopy(data)
        mutated["status"]["radial_convergence"] = "CONVERGED"
        with self.assertRaises(gate.GateError):
            gate.check_manifest(mutated)

    def test_manifest_cannot_claim_global_xdrta2_cleanup(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        mutated = copy.deepcopy(data)
        mutated["status"]["global_xdrta2_abi_clean"] = True
        with self.assertRaises(gate.GateError):
            gate.check_manifest(mutated)

    def test_manifest_cannot_drop_source_route_claim(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        mutated = copy.deepcopy(data)
        mutated["status"]["production_r64_source_route_connected"] = False
        with self.assertRaises(gate.GateError):
            gate.check_manifest(mutated)

    def test_runner_cannot_add_dragon(self) -> None:
        source = gate.RUNNER.read_text() + "\nrdragon b2b.x2m\n"
        with self.assertRaises(gate.GateError):
            gate.check_runner(source)

    def test_runner_cannot_add_quoted_dragon_path(self) -> None:
        source = (gate.RUNNER.read_text() +
                  '\n"$ROOT/bin/Darwin_arm64/Dragon" "$HERE/fake.x2m"\n')
        with self.assertRaises(gate.GateError):
            gate.check_runner(source)

    def test_make_target_cannot_change_recipe(self) -> None:
        source = (gate.ROOT / "Makefile").read_text().replace(
            "run_phase_a9b_b2b_ingress.sh",
            "run_phase_a9b_b2b_ingress_CHANGED.sh",
            1,
        )
        with self.assertRaises(gate.GateError):
            gate.check_makefile(source)

    def test_dependency_cannot_be_dropped(self) -> None:
        source = (gate.ROOT / "src/.dragon_deps.mk").read_text().replace(
            "FLU.o: SPOR64_B2B.o\n", "", 1,
        )
        with self.assertRaises(gate.GateError):
            gate.check_dependencies(source)


if __name__ == "__main__":
    unittest.main()

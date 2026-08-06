#!/usr/bin/env python3
"""Mutation tests for the B2e blocked-admission contract."""

from __future__ import annotations

import copy
import json
import unittest

from check_phase_a9b_b2e_plane1_admission import (
    CANDIDATE,
    HARNESS,
    MANIFEST,
    PROJECT_README,
    RUNNER,
    SCHEMA,
    STRIP,
    STUBS,
    ContractError,
    check_candidate_text,
    check_harness_text,
    check_manifest_data,
    check_project_readme_text,
    check_runner_text,
    check_schema_text,
    check_strip_text,
    check_stub_text,
)


class B2eContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate = CANDIDATE.read_text()
        cls.stubs = STUBS.read_text()
        cls.strip = STRIP.read_text()
        cls.schema = SCHEMA.read_text()
        cls.harness = HARNESS.read_text()
        cls.runner = RUNNER.read_text()
        cls.manifest = json.loads(MANIFEST.read_text())
        cls.project_readme = PROJECT_README.read_text()

    def reject_candidate(self, old: str, new: str) -> None:
        changed = self.candidate.replace(old, new, 1)
        self.assertNotEqual(changed, self.candidate)
        with self.assertRaises(ContractError):
            check_candidate_text(changed, verify_digest=False)

    def mutate_manifest(self, path: tuple[str, ...], value: object) -> None:
        changed = copy.deepcopy(self.manifest)
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        with self.assertRaises(ContractError):
            check_manifest_data(changed)

    def test_baseline(self) -> None:
        check_candidate_text(self.candidate)
        check_stub_text(self.stubs)
        check_strip_text(self.strip)
        check_schema_text(self.schema)
        check_harness_text(self.harness)
        check_manifest_data(self.manifest)
        check_project_readme_text(self.project_readme)
        check_runner_text(self.runner)

    def test_seed_cannot_be_omitted(self) -> None:
        self.reject_candidate(" FSOURCE FLUX_OLD ::", " FSOURCE ::")

    def test_seed_order_is_frozen(self) -> None:
        self.reject_candidate(
            "MACRO0 TRACK TRACK_f SYSTEM FSOURCE FLUX_OLD",
            "FLUX_OLD MACRO0 TRACK TRACK_f SYSTEM FSOURCE",
        )

    def test_r64_cannot_be_omitted(self) -> None:
        self.reject_candidate("ACCE 3 3 R64", "ACCE 3 3")

    def test_r64_cannot_be_duplicated(self) -> None:
        self.reject_candidate("ACCE 3 3 R64", "ACCE 3 3 R64 R64")

    def test_init_on_is_required(self) -> None:
        self.reject_candidate("TYPE S INIT ON REBA", "TYPE S REBA")

    def test_outer_cap_is_frozen(self) -> None:
        self.reject_candidate("EXTE 500", "EXTE 1")

    def test_three_tolerances_share_the_frozen_argument(self) -> None:
        self.reject_candidate(
            "UNKT <<flu_eps>> THER 740 <<flu_eps>>",
            "UNKT <<flu_eps>> THER 740 1.0E-4",
        )

    def test_active_order_census_cannot_be_removed(self) -> None:
        changed = self.schema.replace("track_state(6) /= 1", "track_state(6) /= 3", 1)
        with self.assertRaises(ContractError):
            check_schema_text(changed, verify_digest=False)

    def test_stub_cannot_select_acceptance(self) -> None:
        changed = self.stubs.replace("accepted = .false.", "accepted = .true.", 1)
        with self.assertRaises(ContractError):
            check_stub_text(changed, verify_digest=False)

    def test_fixture_cannot_delete_real64_authority(self) -> None:
        changed = self.strip.replace(
            "call LCMDEL(root,'SOUR')", "call LCMDEL(root,'SPOT-R64')", 1
        )
        with self.assertRaises(ContractError):
            check_strip_text(changed, verify_digest=False)

    def test_production_execution_cannot_be_authorized(self) -> None:
        self.mutate_manifest(("status", "production_execution_authorized"), True)

    def test_tolerance_bits_are_frozen(self) -> None:
        self.mutate_manifest(
            ("candidate_contract", "tolerance_binary32_bits"), "0x00000000"
        )

    def test_model_completion_cannot_be_claimed(self) -> None:
        self.mutate_manifest(("scope", "model_completion_added"), True)

    def test_runner_cannot_link_production_core(self) -> None:
        changed = self.runner + '\n"$FC" -c "$ROOT/src/SPOR64_A9.f90"\n'
        with self.assertRaises(ContractError):
            check_runner_text(changed, verify_digest=False)

    def test_runner_cannot_drop_fresh_case(self) -> None:
        changed = self.runner.replace(
            '"$BUILD_DIR/test_b2e_current_admission" fresh-create',
            ': fresh-create',
            1,
        )
        with self.assertRaises(ContractError):
            check_runner_text(changed, verify_digest=False)

    def test_harness_cannot_hide_core_call(self) -> None:
        changed = self.harness.replace("core_calls /= 0", "core_calls < 0", 1)
        with self.assertRaises(ContractError):
            check_harness_text(changed, verify_digest=False)

    def test_fresh_descriptor_requires_limerg(self) -> None:
        changed = self.harness.replace("limerg=.true.", "limerg=.false.", 1)
        with self.assertRaises(ContractError):
            check_harness_text(changed, verify_digest=False)

    def test_project_readme_cannot_claim_convergence(self) -> None:
        changed = self.project_readme.replace(
            "Radial\nand outer Picard convergence remain `NOT-EVALUATED`.",
            "Radial\nand outer Picard convergence are validated.",
            1,
        )
        with self.assertRaises(ContractError):
            check_project_readme_text(changed)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Short fail-closed tests for the REAL64 route protocol."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKER_PATH = HERE / "check_radial_real64_route_protocol.py"
SPEC = importlib.util.spec_from_file_location("radial_real64_checker", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class RadialReal64RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = CHECKER.load_protocol(CHECKER.DEFAULT_PROTOCOL)

    def assert_rejected(self, mutate) -> None:
        data = copy.deepcopy(self.base)
        mutate(data)
        with self.assertRaises(CHECKER.ContractError):
            CHECKER.validate(data, CHECKER.ROOT)

    def test_public_contract_passes(self) -> None:
        CHECKER.validate(copy.deepcopy(self.base), CHECKER.ROOT)

    def test_dragon_authorization_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"].__setitem__(
                "authorized_now", True
            )
        )

    def test_empirical_parameter_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["scientific_scope"].__setitem__(
                "new_empirical_parameters", {"alpha": 0.7}
            )
        )

    def test_partial_precision_path_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["precision_contract"]["required_path_nodes"].pop()
        )

    def test_archived_residual_claim_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["decision"].__setitem__(
                "archived_independent_Aphi_minus_q", "GO"
            )
        )

    def test_cutoff_tuning_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["inherited_aca_cutoff"].__setitem__(
                "change_or_tuning", "CHANGE"
            )
        )

    def test_phase_a_cannot_add_dragon_action(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_A_static_closure"]["allowed_actions"].append(
                "run Dragon"
            )
        )

    def test_source_hash_census_cannot_be_cleared(self) -> None:
        self.assert_rejected(
            lambda data: data["baseline"].__setitem__("source_sha256_at_commit", {})
        )

    def test_round_trip_prohibitions_are_exact(self) -> None:
        self.assert_rejected(
            lambda data: data["precision_contract"].__setitem__(
                "forbidden_round_trips", ["allowed"] * 5
            )
        )

    def test_unknown_scope_coefficient_fails(self) -> None:
        self.assert_rejected(
            lambda data: data["scientific_scope"].__setitem__("alpha", 0.7)
        )

    def test_on_required_result_is_exact(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"]["REAL64_ON_arm"].__setitem__(
                "required_result", "looks improved"
            )
        )

    def test_classification_is_exact(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"]["classification"].__setitem__(
                "REAL64_cap_without_strict_termination", "PASS"
            )
        )

    def test_aca_path_cannot_omit_mcgpra(self) -> None:
        self.assert_rejected(
            lambda data: data["locked_case"]["selected_aca_tuple"].remove("MCGPRA")
        )

    def test_decision_reason_is_frozen(self) -> None:
        self.assert_rejected(
            lambda data: data["decision"].__setitem__(
                "reason", "Dragon authorized now"
            )
        )

    def test_picard_authorization_text_is_frozen(self) -> None:
        self.assert_rejected(
            lambda data: data["future_stage4"].__setitem__(
                "picard_authorization", "AUTHORIZED NOW"
            )
        )

    def test_terminal_rounding_boundary_is_frozen(self) -> None:
        self.assert_rejected(
            lambda data: data["precision_contract"].__setitem__(
                "compatibility_output", "write type-2 every iteration"
            )
        )

    def test_cutoff_counterfactual_cannot_feed_production(self) -> None:
        self.assert_rejected(
            lambda data: data["inherited_aca_cutoff"].__setitem__(
                "required_instrumentation",
                data["inherited_aca_cutoff"]["required_instrumentation"]
                + " Feed cutoff into production.",
            )
        )

    def test_public_contract_freezes_local_hash_values(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"]["common_restart"][
                "local_artifacts_sha256"
            ].__setitem__(
                "validation/artifacts/iterative-radial-floor/restart_cap.xsm",
                "0" * 64,
            )
        )

    def test_replay_mismatch_classification_is_frozen(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"]["classification"].__setitem__(
                "replay_mismatch", "PASS"
            )
        )

    def test_classification_precedence_is_frozen(self) -> None:
        self.assert_rejected(
            lambda data: data["phase_B_plane1_feasibility"][
                "classification_precedence"
            ]["capture_first_match"].reverse()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

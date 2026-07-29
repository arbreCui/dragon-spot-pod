#!/usr/bin/env python3
"""Mutation tests for the fail-closed protocol-only Picard design."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Callable

from validation.iterative.check_picard_three_return_protocol import (
    ProtocolError,
    ROOT,
    validate,
)


PROTOCOL = ROOT / "validation/iterative/picard_three_return_protocol.json"


class PicardThreeReturnProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original = json.loads(PROTOCOL.read_text())

    def rejected(self, mutate: Callable[[dict], None]) -> None:
        candidate = copy.deepcopy(self.original)
        mutate(candidate)
        with self.assertRaises(ProtocolError):
            validate(candidate, ROOT, require_local=False)

    def test_public_contract_passes(self) -> None:
        validate(copy.deepcopy(self.original), ROOT, require_local=False)

    def test_execution_cannot_be_authorized(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "transport_execution_authorized", True
            )
        )

    def test_dragon_process_cannot_be_added(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "dragon_processes_authorized", 1
            )
        )

    def test_old_result_cannot_be_superseded(self) -> None:
        self.rejected(
            lambda data: data["governance"].__setitem__(
                "supersedes_prior_result", True
            )
        )

    def test_execution_prohibition_cannot_be_amended_here(self) -> None:
        self.rejected(
            lambda data: data["governance"].__setitem__(
                "amends_prior_execution_prohibition", True
            )
        )

    def test_stage4_cannot_be_reclassified(self) -> None:
        self.rejected(
            lambda data: data["status"].__setitem__(
                "stage4_v2", "QUALIFIED"
            )
        )

    def test_return_count_is_exact(self) -> None:
        self.rejected(
            lambda data: data["scientific_object"].__setitem__("returns", 4)
        )

    def test_adjustable_outer_parameter_is_rejected(self) -> None:
        self.rejected(
            lambda data: data["scientific_object"][
                "adjustable_outer_parameters"
            ].append({"alpha": 0.7})
        )

    def test_real64_lane_cannot_be_enabled(self) -> None:
        self.rejected(
            lambda data: data["frozen_map"].__setitem__("real64_lane", "ON")
        )

    def test_tolerance_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["frozen_map"].__setitem__(
                "inner_tolerance_binary32_bits", "0x348637bd"
            )
        )

    def test_source_hash_cannot_be_cleared(self) -> None:
        self.rejected(lambda data: data["source_reference_sha256"].clear())

    def test_input_hash_cannot_change(self) -> None:
        self.rejected(
            lambda data: data["frozen_inputs_sha256"].__setitem__(
                "validation/artifacts/iterative-map1/state0_axial.xsm",
                "0" * 64,
            )
        )

    def test_outer_loop_cannot_be_enabled(self) -> None:
        self.rejected(
            lambda data: data["future_execution_shape"].__setitem__(
                "outer_loop_constructs_allowed", True
            )
        )

    def test_archived_x1_cannot_be_spliced(self) -> None:
        self.rejected(
            lambda data: data["future_execution_shape"].__setitem__(
                "archived_x1_splicing_allowed", True
            )
        )

    def test_incomplete_map_path_is_rejected(self) -> None:
        self.rejected(lambda data: data["future_map_block"].pop())

    def test_single_full_state_norm_is_rejected(self) -> None:
        self.rejected(
            lambda data: data["measurements_per_return"].__setitem__(
                "single_state_norm", "L2"
            )
        )

    def test_component_aggregation_is_rejected(self) -> None:
        self.rejected(
            lambda data: data["measurements_per_return"].__setitem__(
                "component_aggregation", "WEIGHTED-SCORE"
            )
        )

    def test_complete_cannot_be_called_pass(self) -> None:
        self.rejected(
            lambda data: data["future_result_classification"]["complete"].
            __setitem__("label", "PASS")
        )

    def test_complete_cannot_continue(self) -> None:
        self.rejected(
            lambda data: data["future_result_classification"]["complete"].
            __setitem__("next", "CONTINUE")
        )

    def test_incomplete_state_cannot_be_reused(self) -> None:
        self.rejected(
            lambda data: data["future_result_classification"]["incomplete"].
            __setitem__("failed_return_state_reusable", True)
        )


if __name__ == "__main__":
    unittest.main()

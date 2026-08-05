#!/usr/bin/env python3
"""Mutation tests for the narrow B2d link contract."""

from __future__ import annotations

import copy
import json
import unittest

from check_phase_a9b_b2d_link import (
    A8,
    BRIDGE,
    ContractError,
    MANIFEST,
    RUNNER,
    check_a8_text,
    check_bridge_text,
    check_manifest_data,
    check_runner_text,
)


class B2dContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bridge = BRIDGE.read_text()
        cls.a8 = A8.read_text()
        cls.runner = RUNNER.read_text()
        cls.manifest = json.loads(MANIFEST.read_text())

    def reject_bridge(self, old: str, new: str) -> None:
        changed = self.bridge.replace(old, new, 1)
        self.assertNotEqual(changed, self.bridge)
        with self.assertRaises(ContractError):
            check_bridge_text(changed, verify_digest=False)

    def test_baseline(self) -> None:
        check_bridge_text(self.bridge)
        check_a8_text(self.a8)
        check_manifest_data(self.manifest)
        check_runner_text(self.runner)

    def test_wrong_lcmlen_target(self) -> None:
        self.reject_bridge("GANLIB_LCMLEN => LCMLEN", "GANLIB_LCMLEN => LCMGPD")

    def test_wrong_lcmgpd_call(self) -> None:
        self.reject_bridge("call GANLIB_LCMGPD", "call GANLIB_LCMLEN")

    def test_wrong_lcmgil_result(self) -> None:
        self.reject_bridge("directory = GANLIB_LCMGIL", "iplist = GANLIB_LCMGIL")

    def test_state_is_rejected(self) -> None:
        self.reject_bridge("implicit none", "implicit none\n  save",)

    def test_ganlib_write_is_rejected(self) -> None:
        self.reject_bridge(
            "call GANLIB_LCMLEN(iplist,name,length,itylcm)",
            "call LCMPUT(iplist,name,length,itylcm,length)",
        )

    def test_extra_wrapper_is_rejected(self) -> None:
        check = self.bridge + "\nsubroutine LCMLEN(a,b,c,d)\nend subroutine LCMLEN\n"
        with self.assertRaises(ContractError):
            check_bridge_text(check, verify_digest=False)

    def test_a8_direct_module_bypass_is_rejected(self) -> None:
        changed = self.a8.replace("implicit none", "use GANLIB\n  implicit none", 1)
        with self.assertRaises(ContractError):
            check_a8_text(changed, verify_digest=False)

    def mutate_manifest(self, path: tuple[str, ...], value: object) -> None:
        changed = copy.deepcopy(self.manifest)
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        with self.assertRaises(ContractError):
            check_manifest_data(changed)

    def test_solver_change_cannot_be_claimed(self) -> None:
        self.mutate_manifest(("scope", "solver_equations_changed"), True)

    def test_multi_epoch_cannot_be_added(self) -> None:
        self.mutate_manifest(("scope", "multi_epoch_protocol_added"), True)

    def test_dragon_execution_cannot_be_hidden(self) -> None:
        self.mutate_manifest(("link_gate", "dragon_executions"), 1)

    def test_runner_cannot_drop_full_build(self) -> None:
        changed = self.runner.replace('make -C "$ROOT/src"', ":", 1)
        with self.assertRaises(ContractError):
            check_runner_text(changed, verify_digest=False)

    def test_runner_cannot_execute_dragon(self) -> None:
        changed = self.runner + '\n"$DRAGON" < case.x2m\n'
        with self.assertRaises(ContractError):
            check_runner_text(changed, verify_digest=False)


if __name__ == "__main__":
    unittest.main()

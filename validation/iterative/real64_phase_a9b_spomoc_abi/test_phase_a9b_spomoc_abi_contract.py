#!/usr/bin/env python3
"""Targeted fail-closed mutations for the SPOMOC ABI gate."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check_phase_a9b_spomoc_abi as gate


class ContractMutations(unittest.TestCase):
    def mutate_file(self, source: Path, old: str, new: str) -> Path:
        text = source.read_text()
        self.assertEqual(text.count(old), 1, old)
        path = Path(self.temp.name) / source.name
        path.write_text(text.replace(old, new))
        return path

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_spomoc_rejected(self, old: str, new: str) -> None:
        path = self.mutate_file(gate.SPOMOC, old, new)
        with mock.patch.object(gate, "SPOMOC", path):
            with self.assertRaises(gate.GateError):
                gate.check_spomoc()

    def assert_capture64_rejected(self, old: str, new: str) -> None:
        text = gate.SPOMOC.read_text()
        region = gate.routine_region(text, "SPOMOC_CAPTURE64")
        self.assertEqual(region.count(old), 1, old)
        mutated = region.replace(old, new)
        path = Path(self.temp.name) / "SPOMOC.f90"
        path.write_text(text.replace(region, mutated))
        with mock.patch.object(gate, "SPOMOC", path):
            with self.assertRaises(gate.GateError):
                gate.check_spomoc()

    def assert_bridge_rejected(self, old: str, new: str) -> None:
        path = self.mutate_file(gate.BRIDGE, old, new)
        with mock.patch.object(gate, "BRIDGE", path):
            with self.assertRaises(gate.GateError):
                gate.check_bridge()

    def test_public_capture64_cannot_disappear(self) -> None:
        self.assert_spomoc_rejected("  public :: SPOMOC_CAPTURE64\n", "")

    def test_legacy_capture_is_frozen(self) -> None:
        text = gate.SPOMOC.read_text()
        region = gate.routine_region(text, "SPOMOC_CAPTURE")
        mutated = region.replace("call fail('nonfinite QFR')", "call fail('QFR invalid')")
        path = Path(self.temp.name) / "SPOMOC.f90"
        path.write_text(text.replace(region, mutated))
        with mock.patch.object(gate, "SPOMOC", path):
            with self.assertRaises(gate.GateError):
                gate.check_spomoc()

    def test_capture_qfr_cannot_be_real32(self) -> None:
        self.assert_capture64_rejected(
            "real(real64), intent(in) :: qfr(nun, ngeff), eval(nun, ngeff)",
            "real(real32), intent(in) :: qfr(nun, ngeff), eval(nun, ngeff)",
        )

    def test_capture_cannot_call_legacy(self) -> None:
        self.assert_capture64_rejected(
            "    if (.not. SPOMOC_ACTIVE()) return\n",
            "    call SPOMOC_CAPTURE(ngeff, ngind, nun, qfr, eval, source, raw, nconv)\n"
            "    if (.not. SPOMOC_ACTIVE()) return\n",
        )

    def test_inactive_return_cannot_move(self) -> None:
        self.assert_capture64_rejected(
            "    if (.not. SPOMOC_ACTIVE()) return\n"
            "    if (.not. mccgf_seen) call fail('MCCGF context missing')\n",
            "    if (.not. mccgf_seen) call fail('MCCGF context missing')\n"
            "    if (.not. SPOMOC_ACTIVE()) return\n",
        )

    def test_type4_payload_cannot_become_type2(self) -> None:
        self.assert_capture64_rejected(
            "call LCMPUT(group_dir, 'SPOT-M-QFR', required_unknowns, 4, &",
            "call LCMPUT(group_dir, 'SPOT-M-QFR', required_unknowns, 2, &",
        )

    def test_finite_check_cannot_disappear(self) -> None:
        self.assert_capture64_rejected(
            "      if (.not. all(ieee_is_finite(raw(:, i)))) &\n           call fail('nonfinite RAW')\n",
            "",
        )

    def test_group_identity_guard_cannot_disappear(self) -> None:
        self.assert_capture64_rejected(
            "      if (ig /= i) call fail('capture NGIND differs')\n",
            "",
        )

    def test_tuple_state_update_cannot_disappear(self) -> None:
        self.assert_capture64_rejected(
            "    state_vector(24) = required_groups\n",
            "",
        )

    def test_payload_mapping_cannot_swap(self) -> None:
        self.assert_capture64_rejected(
            "           qfr(:, i))\n",
            "           eval(:, i))\n",
        )

    def test_bridge_routine_cannot_disappear(self) -> None:
        region = gate.routine_region(gate.BRIDGE.read_text(), "SPOMOC_PUBLISH")
        self.assert_bridge_rejected(region, "")

    def test_bridge_cannot_add_second_call(self) -> None:
        self.assert_bridge_rejected(
            "  call SPOMOC_SET_ROLE_MODULE(role, iteration)\n",
            "  call SPOMOC_SET_ROLE_MODULE(role, iteration)\n"
            "  call SPOMOC_SET_ROLE_MODULE(role, iteration)\n",
        )

    def test_bridge_cannot_reorder_forwarded_arguments(self) -> None:
        self.assert_bridge_rejected(
            "  call SPOMOC_SET_ROLE_MODULE(role, iteration)\n",
            "  call SPOMOC_SET_ROLE_MODULE(iteration, role)\n",
        )

    def test_bridge_source_cannot_be_real32(self) -> None:
        self.assert_bridge_rejected(
            "  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)\n",
            "  real(real32), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)\n",
        )

    def test_bridge_cannot_gain_ganlib_access(self) -> None:
        self.assert_bridge_rejected(
            "  call SPOMOC_PUBLISH_MODULE()\n",
            "  call LCMGET()\n  call SPOMOC_PUBLISH_MODULE()\n",
        )

    def test_bridge_cannot_gain_branch(self) -> None:
        self.assert_bridge_rejected(
            "  call SPOMOC_SET_ROLE_MODULE(role, iteration)\n",
            "  if (role > 0) call SPOMOC_SET_ROLE_MODULE(role, iteration)\n",
        )

    def test_bridge_cannot_use_bind_c(self) -> None:
        self.assert_bridge_rejected(
            "subroutine SPOMOC_SET_ROLE(role, iteration)\n",
            "subroutine SPOMOC_SET_ROLE(role, iteration) bind(c)\n",
        )

    def test_manifest_cannot_claim_route(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        data["status"]["production_route_connected"] = True
        path = Path(self.temp.name) / "manifest.json"
        path.write_text(json.dumps(data))
        with mock.patch.object(gate, "MANIFEST", path):
            with self.assertRaises(gate.GateError):
                gate.check_manifest()

    def test_manifest_cannot_claim_begin64(self) -> None:
        data = json.loads(gate.MANIFEST.read_text())
        data["status"]["spomoc_begin64_implemented"] = True
        path = Path(self.temp.name) / "manifest.json"
        path.write_text(json.dumps(data))
        with mock.patch.object(gate, "MANIFEST", path):
            with self.assertRaises(gate.GateError):
                gate.check_manifest()

    def test_dependency_edge_cannot_disappear(self) -> None:
        dep = Path(self.temp.name) / "deps.mk"
        dep.write_text(gate.DEPS.read_text().replace("SPOMOC_R64_BRIDGE.o: SPOMOC.o\n", ""))
        with mock.patch.object(gate, "DEPS", dep), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(gate.RUNNER)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_dependency_edge_cannot_expand(self) -> None:
        dep = Path(self.temp.name) / "deps.mk"
        dep.write_text(gate.DEPS.read_text() + "SPOMOC_R64_BRIDGE.o: OTHER.o\n")
        with mock.patch.object(gate, "DEPS", dep), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(gate.RUNNER)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_make_target_cannot_gain_recipe(self) -> None:
        make = Path(self.temp.name) / "Makefile"
        make.write_text(gate.MAKEFILE.read_text().replace(
            gate.MAKE_BLOCK,
            gate.MAKE_BLOCK + "\ttrue\n",
        ))
        with mock.patch.object(gate, "MAKEFILE", make), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(gate.RUNNER)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_runner_cannot_gain_linker(self) -> None:
        runner = Path(self.temp.name) / "runner.sh"
        runner.write_text(gate.RUNNER.read_text() + "\n/usr/bin/ld objects.o\n")
        with mock.patch.object(gate, "RUNNER", runner), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(runner)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_runner_cannot_compile_bridge_from_src(self) -> None:
        runner = Path(self.temp.name) / "runner.sh"
        text = gate.RUNNER.read_text().replace(
            'compile_checked "$BUILD_DIR/SPOMOC_R64_BRIDGE.f90"',
            'compile_checked "$ROOT/src/SPOMOC_R64_BRIDGE.f90"',
        )
        runner.write_text(text)
        with mock.patch.object(gate, "RUNNER", runner), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(runner)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_runner_cannot_omit_temporary_cwd(self) -> None:
        runner = Path(self.temp.name) / "runner.sh"
        runner.write_text(gate.RUNNER.read_text().replace('cd "$BUILD_DIR"\n', ""))
        with mock.patch.object(gate, "RUNNER", runner), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(runner)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_runner_cannot_restore_fc_override(self) -> None:
        runner = Path(self.temp.name) / "runner.sh"
        runner.write_text(gate.RUNNER.read_text().replace(
            "FC=/opt/homebrew/bin/gfortran\n", "FC=${FC:-gfortran}\n"
        ))
        with mock.patch.object(gate, "RUNNER", runner), \
             mock.patch.object(gate, "EXPECTED_RUNNER_SHA256", gate.digest(runner)):
            with self.assertRaises(gate.GateError):
                gate.check_build_boundary()

    def test_receipt_cannot_drop_path(self) -> None:
        lines = gate.RECEIPT.read_text().splitlines()
        receipt = Path(self.temp.name) / "receipt.sha256"
        receipt.write_text("\n".join(lines[:-1]) + "\n")
        with mock.patch.object(gate, "RECEIPT", receipt):
            with self.assertRaises(gate.GateError):
                gate.check_receipt_shape()

    def test_receipt_cannot_duplicate_path(self) -> None:
        text = gate.RECEIPT.read_text()
        receipt = Path(self.temp.name) / "receipt.sha256"
        receipt.write_text(text + text.splitlines()[0] + "\n")
        with mock.patch.object(gate, "RECEIPT", receipt):
            with self.assertRaises(gate.GateError):
                gate.check_receipt_shape()


if __name__ == "__main__":
    unittest.main()

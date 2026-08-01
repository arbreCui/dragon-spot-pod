#!/usr/bin/env python3
"""Mutation tests for the A9b-B1 compile-only promotion contract."""

from __future__ import annotations

import copy
import unittest

import check_phase_a9b_promotion as gate


class PhaseA9bPromotionContractTests(unittest.TestCase):
    def assert_rejected(self, function, *arguments) -> None:
        with self.assertRaises(gate.PhaseA9bPromotionError):
            function(*arguments)

    def assert_runner_rejected(self, source: str) -> None:
        with self.assertRaises(gate.PhaseA9bPromotionError):
            gate.validate_runner_text(source, verify_hash=False)

    def mutate(self, text: str, old: str, new: str) -> str:
        self.assertIn(old, text)
        return text.replace(old, new, 1)

    def test_live_contract_passes(self) -> None:
        gate.run_checks()

    def test_every_status_leaf_is_closed(self) -> None:
        baseline = gate.load_manifest()
        for key, value in gate.EXPECTED_STATUS.items():
            with self.subTest(key=key):
                mutated = copy.deepcopy(baseline)
                if isinstance(value, bool):
                    mutated["status"][key] = not value
                elif isinstance(value, int):
                    mutated["status"][key] = value + 1
                else:
                    mutated["status"][key] = "PASS"
                self.assert_rejected(gate.validate_manifest, mutated)

    def test_promotion_map_and_parent_authority_are_closed(self) -> None:
        baseline = gate.load_manifest()
        mutation = copy.deepcopy(baseline)
        mutation["promotions"][0]["production"] = "src/OTHER.f90"
        self.assert_rejected(gate.validate_manifest, mutation)
        mutation = copy.deepcopy(baseline)
        mutation["authority"]["parent_commit"] = "0" * 40
        self.assert_rejected(gate.validate_manifest, mutation)

    def test_byte_identity_and_hash_are_both_required(self) -> None:
        payload = b"frozen source\n"
        digest = gate.hashlib.sha256(payload).hexdigest()
        gate.validate_promotion_pair(payload, payload, digest, "source")
        self.assert_rejected(
            gate.validate_promotion_pair, payload, payload + b"!", digest, "source"
        )
        self.assert_rejected(
            gate.validate_promotion_pair, payload, payload, "0" * 64, "source"
        )

    def test_src_delta_is_exactly_additive_four(self) -> None:
        promoted = set(gate.PROMOTED_PATHS)
        gate.validate_production_path_set({}, promoted, set())
        tracked = {path: "A" for path in promoted}
        gate.validate_production_path_set(tracked, set(), set())
        self.assert_rejected(
            gate.validate_production_path_set,
            {}, promoted | {"src/FLU.f"}, set(),
        )
        missing = set(promoted)
        missing.pop()
        self.assert_rejected(gate.validate_production_path_set, {}, missing, set())
        edited = {next(iter(promoted)): "M"}
        self.assert_rejected(
            gate.validate_production_path_set,
            edited, promoted - set(edited), set(),
        )
        self.assert_rejected(
            gate.validate_production_path_set,
            {}, promoted, {next(iter(promoted))},
        )

    def test_production_callsite_is_rejected(self) -> None:
        gate.validate_nonpromoted_source("legacy.f", "      CALL FLU2DR(A,B)\n")
        self.assert_rejected(
            gate.validate_nonpromoted_source,
            "FLU.f", "      CALL FLU2DR64_CORE(A,B)\n",
        )
        self.assert_rejected(
            gate.validate_nonpromoted_source,
            "FLUGPI.f", "      USE SPOR64_A9\n",
        )
        self.assert_rejected(
            gate.validate_nonpromoted_source,
            "host.f90", "call SPOR64_A9()\n",
        )

    def test_dependency_output_is_exact_and_ordered(self) -> None:
        baseline = "\n".join(gate.EXPECTED_DEPENDENCIES) + "\n"
        gate.validate_dependency_text(baseline)
        self.assert_rejected(
            gate.validate_dependency_text,
            "\n".join(reversed(gate.EXPECTED_DEPENDENCIES)) + "\n",
        )
        self.assert_rejected(
            gate.validate_dependency_text, baseline + "EXTRA.o: OTHER.o\n"
        )

    def test_symbol_inventory_is_exactly_shaped(self) -> None:
        gate.validate_symbol_inventory("expected_x_unresolved.txt", "_foo_\n")
        gate.validate_symbol_inventory("expected_x_defined.txt", "T _foo_\n")
        self.assert_rejected(
            gate.validate_symbol_inventory,
            "expected_x_unresolved.txt", "_z_\n_a_\n",
        )
        self.assert_rejected(
            gate.validate_symbol_inventory,
            "expected_x_defined.txt", "_foo_\n",
        )
        self.assert_rejected(
            gate.validate_symbol_inventory,
            "expected_x_defined.txt", "T _main\n",
        )

    def test_make_target_has_no_prerequisite_or_extra_recipe(self) -> None:
        source = gate.MAKEFILE.read_text(encoding="utf-8")
        gate.validate_makefile_text(source)
        mutation = self.mutate(
            source,
            "spot-real64-phase-a9b-promotion :\n",
            "spot-real64-phase-a9b-promotion : spot-real64-phase-a9a\n",
        )
        self.assert_rejected(gate.validate_makefile_text, mutation)
        mutation = self.mutate(
            source,
            "\tsh validation/iterative/real64_phase_a9b_promotion/run_phase_a9b_promotion.sh\n",
            "\tsh validation/iterative/real64_phase_a9b_promotion/run_phase_a9b_promotion.sh\n\tsh validation/iterative/real64_phase_a9/run_phase_a9a.sh\n",
        )
        self.assert_rejected(gate.validate_makefile_text, mutation)
        mutation = self.mutate(source, "all :\n", "all : spot-real64-phase-a9b-promotion\n")
        self.assert_rejected(gate.validate_makefile_text, mutation)

    def test_runner_rejects_link_command(self) -> None:
        source = gate.RUNNER.read_text(encoding="utf-8")
        gate.validate_runner_text(source)
        marker = '  "$FC" $CHECKED_FLAGS -J"$BUILD_DIR" -I"$BUILD_DIR" -c "$1" -o "$2"'
        mutation = self.mutate(source, marker, marker.replace(" -c ", " "))
        self.assert_runner_rejected(mutation)
        for injected in (
            'ld -r "$BUILD_DIR/SPOR64_A9.o" -o "$BUILD_DIR/rogue.o"',
            'ar rcs "$BUILD_DIR/rogue.a" "$BUILD_DIR/SPOR64_A9.o"',
            'cc "$BUILD_DIR/SPOR64_A9.o" -o "$BUILD_DIR/rogue"',
            '/usr/bin/ld -r one.o -o linked.o',
            '/usr/bin/cc one.o -o rogue',
            'env gfortran one.f90 -o rogue',
            '$FC one.f90 -o rogue',
            'exec "$BUILD_DIR/rogue"',
            '"$BUILD_DIR/rogue"',
        ):
            with self.subTest(injected=injected):
                self.assert_runner_rejected(source + "\n" + injected + "\n")

    def test_runner_hash_is_frozen(self) -> None:
        source = gate.RUNNER.read_text(encoding="utf-8")
        self.assert_rejected(gate.validate_runner_text, source + "\n# drift\n")

    def test_runner_rejects_prerequisite_replay_and_dragon(self) -> None:
        source = gate.RUNNER.read_text(encoding="utf-8")
        mutation = source + "\nsh validation/iterative/real64_phase_a9/run_phase_a9a.sh\n"
        self.assert_runner_rejected(mutation)
        mutation = source + "\nDragon case.x2m\n"
        self.assert_runner_rejected(mutation)

    def test_runner_requires_all_negative_compiles(self) -> None:
        source = gate.RUNNER.read_text(encoding="utf-8")
        name = gate.EXPECTED_NEGATIVES[0]
        mutation = source.replace(name, "compile_fail_removed.f90", 1)
        self.assert_runner_rejected(mutation)

    def test_runner_requires_default_real8_and_exact_nm(self) -> None:
        source = gate.RUNNER.read_text(encoding="utf-8")
        mutation = source.replace("-fdefault-real-8", "-fno-default-real-8", 1)
        self.assert_runner_rejected(mutation)
        mutation = source.replace(
            'cmp -s "$HERE/expected_${stem}_${symbol_class}.txt"',
            'test -s "$BUILD_DIR/${stem}_${symbol_class}.txt"',
            1,
        )
        self.assert_runner_rejected(mutation)

    def test_docs_reject_runtime_or_convergence_claim(self) -> None:
        source = gate.README.read_text(encoding="utf-8")
        root = gate.ROOT_README.read_text(encoding="utf-8")
        iterative = gate.ITERATIVE_README.read_text(encoding="utf-8")
        gate.validate_docs_text(source, root, iterative)
        self.assert_rejected(
            gate.validate_docs_text,
            source + "\nCONTINUOUS-REAL64-LANE=true\n", root, iterative,
        )
        self.assert_rejected(
            gate.validate_docs_text,
            source + "\nRADIAL-CONVERGENCE=PASS\n", root, iterative,
        )

    def test_receipt_scope_is_exact_and_noncyclic(self) -> None:
        source = gate.RECEIPT.read_text(encoding="utf-8")
        gate.validate_receipt(source)
        self.assert_rejected(
            gate.validate_receipt,
            source + "0" * 64 + "  validation/iterative/extra.txt\n",
        )


if __name__ == "__main__":
    unittest.main()

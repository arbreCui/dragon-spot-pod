#!/usr/bin/env python3
"""Input-level integration contracts; these tests run no transport."""

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

from production_inputs import ProductionConfig, build_decks, write_inputs


class ProductionInputsTest(unittest.TestCase):
    def test_common_mesh_and_fixed_basis_are_identical_between_cases(self):
        decks = build_decks()
        setup = decks["case_setup.x2m"]
        self.assertIn("CAR1D 12", setup)
        self.assertIn("ALLG DIAM 0 SN 8 SCAT 3", setup)
        mesh = setup.split("  MESHX\n", 1)[1].split("  MIX", 1)[0]
        self.assertEqual([float(x) for x in mesh.split()],
                         [12.5 * x for x in range(13)])
        self.assertIn("SPOD 2 FIXB", setup)
        self.assertIn("SPOD 2 FIXB", decks["picard_radial.x2m"])
        self.assertNotIn("SPOD", decks["bootstrap_axial.x2m"])
        self.assertNotIn("SPOD", decks["picard_axial.x2m"])

    def test_geo_mix_tokens_are_integers_and_match_physical_cell_midpoints(self):
        # GEOIN1's integer MIX branch stores the material index; its character
        # branch activates CELL/sub-geometries. Validate actual token types and
        # compare their spatial interpretation with the physical zone edges.
        specification = json.loads(Path(__file__).with_name("case_spec.json").read_text())
        physical_edges = specification["geometry"]["physical_z_edges_cm"]
        for cells_per_zone in (1, 4, 8):
            config = replace(ProductionConfig(), cells_per_zone=cells_per_zone)
            for name in ("common_basis.x2m", "case_setup.x2m"):
                geometry = build_decks(config)[name].split("GEOM_AX := GEO:", 1)[1].split(";", 1)[0]
                mesh_text, mix_text = geometry.split("MESHX", 1)[1].split("MIX", 1)
                mesh = [float(token) for token in mesh_text.split()]
                tokens = mix_text.split()
                self.assertTrue(all(re.fullmatch(r"[1-9][0-9]*", token) for token in tokens))
                mixtures = [int(token) for token in tokens]
                self.assertEqual(len(mixtures), len(mesh) - 1)
                expected = [next(zone for zone in range(1, len(physical_edges))
                                 if physical_edges[zone - 1] <= (left + right) / 2 < physical_edges[zone])
                            for left, right in zip(mesh, mesh[1:])]
                self.assertEqual(mixtures, expected)
                self.assertIn("X- VOID X+ VOID", geometry)

    def test_rank_gate_runs_after_svd_before_basis_publication(self):
        deck = build_decks()["common_basis.x2m"]
        self.assertLess(deck.index("SYSTEM := ASM:"), deck.index("WHILE igr"))
        self.assertLess(deck.index("ENDWHILE"), deck.index("BASIS_ARCH := SYSTEM"))
        self.assertIn("GETVAL 'POD-RANK-G' <<igr>> >>nmode<<", deck)
        self.assertIn("IF nmode 2 <>", deck)
        self.assertIn("ABORT:", deck)
        self.assertNotIn("FLU:", deck)

    def test_rank1_uses_one_common_training_and_fixed_basis_throughout(self):
        rank1 = build_decks(ProductionConfig(rank=1))
        rank2 = build_decks()
        for name in rank1:
            # The experiment rank changes only SPOD selection and exact NMODE
            # checks; geometry, transport controls and continuation stay shared.
            self.assertEqual(rank1[name], rank2[name].replace("SPOD 2", "SPOD 1")
                             .replace("IF nmode 2 <>", "IF nmode 1 <>"))
        self.assertIn("SPOD 1 ;", rank1["common_basis.x2m"])
        self.assertIn("IF nmode 1 <>", rank1["case_setup.x2m"])
        for name in ("case_setup.x2m", "picard_radial.x2m"):
            self.assertIn("SPOD 1 FIXB", rank1[name])

    def test_runtime_control_contract_uses_same_radial_values(self):
        config = replace(ProductionConfig(), eps_radial=7.5e-7, maxout=121,
                         maxinr=123, radial_acce_free=4, radial_acce_accel=2)
        args = config.contract_arguments("AAA")
        self.assertEqual(args[2], "7.50000000E-07")
        self.assertEqual(args[5:9], ["121", "123", "4", "2"])
        radial = build_decks(config)["bootstrap_radial.x2m"]
        self.assertIn("<<keff>> 7.50000000E-07\n  121 123 4 2", radial)
        for case in ("AAA", "ABA"):
            self.assertEqual(config.contract_arguments(case)[2:], args[2:])

    def test_production_lifecycle_and_audits_are_present(self):
        decks = build_decks()
        self.assertIn("SPOPROJ: SNAP AX_CURRENT TRACK_AX :: FIXB", decks["bootstrap_radial.x2m"])
        self.assertIn("SpotRefR64", decks["bootstrap_radial.x2m"])
        self.assertIn("SpotStepR64", decks["picard_radial.x2m"])
        for name in ("bootstrap_axial.x2m", "picard_axial.x2m"):
            self.assertIn("SPOGBAL: AX_CURRENT TRACK_AX SYSTEM_NEXT MACROLIB3", decks[name])
            self.assertIn("SPOSTATE:", decks[name])
            self.assertIn("SPOLEAK:", decks[name])
        self.assertIn("SPOXCONV: AX_CURRENT PARENT_AX", decks["picard_axial.x2m"])
        self.assertNotIn("SPOXCONV:", decks["bootstrap_axial.x2m"])

    def test_generated_names_obey_cle_limit(self):
        for deck in build_decks().values():
            for decl in re.findall(r"^(?:LINKED_LIST|XSM_FILE|SEQ_BINARY) (.*?) ;", deck, re.M):
                for name in decl.split("::")[0].split():
                    self.assertLessEqual(len(name), 12, name)

    def test_invalid_controls_do_not_create_output(self):
        for field, value in (("cells_per_zone", 0), ("sn", 3), ("rank", 3),
                             ("eps_axial", float("nan")), ("maxout", True)):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "inputs"
                with self.assertRaises(ValueError):
                    write_inputs(output, replace(ProductionConfig(), **{field: value}))
                self.assertFalse(output.exists())

    def test_output_is_fresh_and_manifest_hashes_are_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            first, second = write_inputs(a), write_inputs(b)
            self.assertEqual(first, second)
            self.assertEqual(json.loads((a / "production_inputs.json").read_text()), first)
            for name, digest in first["deck_sha256"].items():
                self.assertEqual(hashlib.sha256((a / name).read_bytes()).hexdigest(), digest)
            with self.assertRaises(FileExistsError):
                write_inputs(a)
            self.assertEqual((a / "production_inputs.json").read_bytes(),
                             (b / "production_inputs.json").read_bytes())


if __name__ == "__main__":
    unittest.main()

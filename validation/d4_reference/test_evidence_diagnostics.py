#!/usr/bin/env python3
"""Small analytic fixtures for saved-data diagnostics; no solver or build."""
import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest

from audit_mgxexp import audit
from report_d4a_evidence import consumed, cpu_time, decode, markdown, number, pin_differences, summarize


FIXTURE = """MGXEXP 1
DIM 2 1 2 0
ENERGY_EV_DESCENDING
4 2 0
MATERIAL 1
TOTAL
1 1
ABSORPTION
0.40625 0.5
SCATTER_SUM
0.625 0.5
EXCESS_MULTIPLICITY
0.03125 0
SCATTER 0
1 1 0.5
1 2 0.125
2 1 0.25
2 2 0.25
END_SCATTER
SCATTER 1
1 1 -0.125
2 1 0.03125
END_SCATTER
END_MATERIAL
END_MGXEXP
"""


class ScatteringDiagnostic(unittest.TestCase):
    def test_source_rows_and_multiplicity_convention(self):
        summary, rows = audit(FIXTURE)
        self.assertEqual(summary["maximum_absolute_difference"], 0)
        self.assertEqual([r["p0_outgoing_sum"] for r in rows], [0.625, 0.5])
        self.assertEqual([r["p0_incoming_sum"] for r in rows], [0.75, 0.375])
        self.assertEqual([r["absorption_identity_difference"] for r in rows], [0, 0])
        self.assertEqual(summary["negative_p0_entries"], 0)

    def test_discrepancy_is_reported_without_repair(self):
        summary, rows = audit(FIXTURE.replace("1 2 0.125", "1 2 -0.125"))
        self.assertEqual(rows[0]["p0_outgoing_sum"], 0.375)
        self.assertEqual(rows[0]["p0_minus_sigs00"], -0.25)
        self.assertEqual(summary["negative_p0_entries"], 1)
        self.assertEqual(summary["negative_p0_absolute_sum"], 0.125)

    def test_malformed_data_refused(self):
        for bad in (FIXTURE.replace("1 1 0.5", "1 1 nan"),
                    FIXTURE.replace("1 1 0.5", "1 1 0.5\n1 1 0.5"),
                    FIXTURE.replace("1 2 0.125", "1 3 0.125"),
                    FIXTURE.replace("4 2 0", "2 4 0"),
                    FIXTURE.replace("END_MGXEXP", ""), FIXTURE + "extra\n"):
            with self.subTest(bad=bad[-50:]), self.assertRaises(ValueError):
                audit(bad)


class EvidenceDiagnostic(unittest.TestCase):
    def test_complete_reducer_and_wrong_state_refusal(self):
        # Analytic two-bin fixture, not a physical D4 result.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def package(directory, files, manifest="result.sha256"):
                folder = root / directory
                folder.mkdir(exist_ok=True)
                records = []
                for name, value in files.items():
                    raw = value.encode() if isinstance(value, str) else json.dumps(value).encode()
                    (folder / name).write_bytes(raw)
                    records.append(hashlib.sha256(raw).hexdigest()+"  "+name)
                raw = ("\n".join(records)+"\n").encode()
                (folder / manifest).write_bytes(raw)
                return hashlib.sha256(raw).hexdigest()

            package("ce", {"reference_result.json": {"keff": 2.5, "keff_standard_deviation": 0.01,
                "bins": [{"floor": 1, "pin_index": 0, "global_fraction": 0.25},
                         {"floor": 1, "pin_index": 1, "global_fraction": 0.75}]}}, "result_receipt.sha256")
            identity = package("work", {"gate.log": "SPOT-GATE THRESHOLD 5e-7\n"
                "SPOT-GATE RRHO 0\nSPOT-GATE RLEAK 0\nSPOT-GATE RA 0\nCLASSIFICATION=VALID_MET\n",
                "radial.log": "cle2000_c: cpu time= 100 second\n",
                "axial.log": "cle2000_c: cpu time= 2 second\n"})
            review = {"closed_epoch": 1, "numerical_cells": 12, "physical_zones": 3,
                "independent_review": "PASS", "result_manifest_sha256": identity,
                "k64": 2, "Rrho": 0, "Rleak": 0, "Ra": 0,
                "gate_all_required": 5e-7, "classification": "VALID_MET", "elapsed_seconds": 120}
            package("review", {"review.json": review})
            package("current", {"summary.json": {"work_result_manifest_sha256": identity,
                "same_state_k64": 2, "source_normalized_net_leakage_kL_over_F": 0.1,
                "ce_source_normalized_leakage": 0.08}})
            pin_inputs = (identity + "  /saved/work/result.sha256\n" +
                hashlib.sha256((root / "ce/reference_result.json").read_bytes()).hexdigest() +
                "  /saved/ce/reference_result.json\n")
            pin_files = {"pin_rates.csv": "floor,pin_index,global_fraction\n1,0,0.25\n1,1,0.75\n",
                         "inputs.sha256": pin_inputs}
            package("pins", pin_files)
            config = {"label": "TEST ONLY", "ce": "ce", "maps": [
                {key: key for key in ("work", "review", "current", "pins")}]}
            report = summarize(config, root)
            self.assertAlmostEqual(report["maps"][0]["ce_reactivity_difference_pcm"], -10000)
            self.assertEqual(report["existing_ce_budget_pcm"], 980)
            self.assertAlmostEqual(report["maps"][0]["ce_leakage_difference_percentage_points"], 2)
            self.assertEqual(report["classification"], "SAVED_EVIDENCE_DIAGNOSTIC_ONLY")
            for omitted in (("current",), ("pins",), ("current", "pins")):
                selected = {k: v for k, v in config["maps"][0].items() if k not in omitted}
                partial = summarize(dict(config, maps=[selected]), root)
                row = partial["maps"][0]
                with self.subTest(omitted=omitted):
                    self.assertEqual(row["classification"], "VALID_MET")
                    self.assertEqual(row["k64"], 2)
                    self.assertEqual(row["source_normalized_leakage"] is None, "current" in omitted)
                    self.assertEqual(row["ce_leakage_difference_percentage_points"] is None, "current" in omitted)
                    self.assertEqual(row["maximum_relative_pin_fraction_difference_percent"] is None, "pins" in omitted)
                    self.assertEqual(row["rms_relative_pin_fraction_difference_percent"] is None, "pins" in omitted)
                    self.assertIn("not evaluated", markdown(partial))
                    self.assertIn("null", json.dumps(partial, allow_nan=False))
            for declared in ("current", "pins"):
                selected = dict(config["maps"][0], **{declared: "does-not-exist"})
                with self.subTest(missing_declared=declared), self.assertRaises(FileNotFoundError):
                    summarize(dict(config, maps=[selected]), root)
            for field, value in (("closed_epoch", 2), ("numerical_cells", 3),
                                 ("Rrho", 1), ("gate_all_required", 1e-3)):
                changed = dict(review, **{field: value})
                package("review", {"review.json": changed})
                with self.subTest(field=field), self.assertRaises(ValueError):
                    summarize(config, root)
                with self.subTest(field=field, diagnostics="omitted"), self.assertRaises(ValueError):
                    summarize(dict(config, maps=[{"work": "work", "review": "review"}]), root)
            package("review", {"review.json": review})
            bad_current = {"work_result_manifest_sha256": "0"*64, "same_state_k64": 2}
            package("current", {"summary.json": bad_current})
            with self.assertRaises(ValueError):
                summarize(config, root)
            package("current", {"summary.json": {"work_result_manifest_sha256": identity,
                "same_state_k64": 2, "source_normalized_net_leakage_kL_over_F": 0.1,
                "ce_source_normalized_leakage": 0.08}})
            for bad in (pin_inputs.replace(identity, "0"*64),
                        pin_inputs.replace("/saved/work/", "/saved/other-map/"),
                        pin_inputs.replace("/saved/ce/", "/saved/other-ce/")):
                package("pins", dict(pin_files, **{"inputs.sha256": bad}))
                with self.subTest(inputs=bad), self.assertRaises(ValueError):
                    summarize(config, root)

    def test_pin_join_is_keyed_and_rms_is_relative(self):
        ce = {"bins": [{"floor": 1, "pin_index": 0, "global_fraction": 0.25},
                       {"floor": 1, "pin_index": 1, "global_fraction": 0.75}]}
        raw = b"floor,pin_index,global_fraction\n1,1,0.6\n1,0,0.275\n"
        maximum, rms = pin_differences(raw, ce)
        self.assertAlmostEqual(maximum, 20)
        self.assertAlmostEqual(rms, 100 * math.sqrt(0.025))
        for bad in (raw + b"1,0,0.275\n", raw.replace(b"1,0,", b"2,0,")):
            with self.assertRaises(ValueError):
                pin_differences(bad, ce)

    def test_nonfinite_values_refused(self):
        for bad in (float("nan"), float("inf"), -1):
            with self.assertRaises(ValueError):
                number(bad)
        with self.assertRaises(ValueError):
            decode(b'{"x": NaN}')

    def test_changed_or_unlisted_consumed_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = b"original\n"
            (root / "data").write_bytes(raw)
            (root / "result.sha256").write_text(hashlib.sha256(raw).hexdigest()+"  data\n")
            self.assertEqual(consumed(root, "data", {}), raw)
            (root / "data").write_bytes(b"changed\n")
            with self.assertRaises(ValueError):
                consumed(root, "data", {})
            (root / "lookalike").write_bytes(raw)
            with self.assertRaises(ValueError):
                consumed(root, "lookalike", {})

    def test_timing_is_completed_cpu_not_wall(self):
        raw = b"WALL 20\ncle2000_c: cpu time= 5.00 second\n"
        self.assertEqual(cpu_time(raw), 5)
        for bad in (b"WALL 20", raw + raw):
            with self.assertRaises(ValueError):
                cpu_time(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)

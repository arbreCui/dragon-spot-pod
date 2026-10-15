#!/usr/bin/env python3
"""Exercise provenance, budget, and stop contracts without any solver call."""

from dataclasses import asdict
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from production_inputs import ProductionConfig
from test_snapshot_control_preflight import write_snapshot
from production_runner import (Budget, DRAGON_SHA, Refusal, SerialExecutor, ROOT, REFERENCE_CHECKS,
                               check_dragon_log, check_protocol, check_rank_addendum, pack_archives_deck, parse_gate,
                               preflight, prepare, qualify_aba, rank_precision_deck, parse_rank_admission,
                               read_manifest, run, sha256, verify_prepared, DiskResources,
                               ResourceFailure, validate_resource_roots)


def valid_gate(rho=1e-8, leak=2e-8, modal=3e-8):
    classification = "VALID_MET" if max(rho, leak, modal) <= 5e-7 else "VALID_NOT_MET"
    return (f"SPOT-GATE THRESHOLD      4.9999999999999998E-07\n"
            f"SPOT-GATE RRHO {rho:.17E} PASS\n"
            f"SPOT-GATE RLEAK {leak:.17E} PASS\n"
            f"SPOT-GATE RA {modal:.17E} PASS\n"
            f"CLASSIFICATION={classification}\nSPOT-GATE COMPLETE\n")


def declared_budget():
    return dict(setup_seconds=120, bootstrap_axial_seconds=300,
                bootstrap_radial_seconds=600, radial_seconds=300,
                axial_seconds=300, host_seconds=120, max_maps=100, total_seconds=21600)


class FakeExecutor:
    """Exercise real orchestration with inert text files; never spawn an engine."""
    instances = []
    rank_pass = True

    def __init__(self, work, total_seconds, case, resources):
        self.work, self.total_seconds, self.case = work, total_seconds, case
        self.rank = json.loads((work / "prepared.json").read_text())["production_config"]["rank"]
        self.calls = []
        self.__class__.instances.append(self)

    def execute(self, directory, label, command, cap, marker=None, deck=None):
        self.calls.append((directory, label, command, cap))
        outputs = {
            "pack_archives": ["training_snapshots.xsm", "aaa_snapshots.xsm", "aba_snapshots.xsm"],
            "common_basis": ["common_basis.xsm"],
            "case_setup": ["initial_axial_track.xsm", "initial_axial_macrolib.xsm", "initial_system.xsm"],
            "make_route_contract": ["route_contract.xsm"],
            "bootstrap_axial": ["seed_axial.xsm", "seed_snapshots.xsm"],
            "bootstrap_radial": ["refreshed_snapshots.xsm"],
            "b2i_seal_bootstrap": ["closed_axial.xsm", "closed_snapshots.xsm"],
            "prepare_r64_next_projected": ["projected_proposal.xsm"],
            "picard_radial": ["candidate_radial.xsm", "candidate_system.xsm"],
            "picard_axial": ["candidate_axial.xsm", "candidate_snapshots.xsm"],
            "close_r64_returned": ["closed_axial.xsm", "closed_snapshots.xsm"],
            "checker_parent": ["parent_for_checker.xsm"],
        }
        for name in outputs.get(label, []):
            (directory / name).write_text(f"inert test output {label} {name}")
        result = valid_gate() if label == "check_convergence_gate" else ""
        if label == "rank_precision":
            second, flag = ("1.0E-3", "TRUE") if self.rank_pass else ("1.0E-8", "FALSE")
            first = "1.0E+0"
            if self.rank == 1:
                first, second = ("1.0E+0" if self.rank_pass else "0.0E+0"), "0.0E+0"
            result = "".join(f">|AXMAT-RANK-SPECTRUM {i} {self.rank} {first} {second} 0.0E+0 .{flag}.\n"
                             for i in range(1, 371))
            result += ">|AXMAT-RANK-INPUT-PRECISION-" + ("PASS" if self.rank_pass else "FAIL") + "\n"
        (directory / f"{label}.log").write_text(result)
        return result


class RunnerContracts(unittest.TestCase):
    def test_gate_requires_all_three_without_tolerance_relaxation(self):
        self.assertEqual(parse_gate(valid_gate())["classification"], "VALID_MET")
        self.assertEqual(parse_gate(valid_gate(leak=5.000000001e-7))["classification"], "VALID_NOT_MET")
        self.assertEqual(parse_gate(valid_gate(modal=5e-7))["classification"], "VALID_MET")
        for bad in (valid_gate().replace("VALID_MET", "VALID_NOT_MET"),
                    valid_gate().replace("4.9999999999999998E-07", "6E-7"),
                    valid_gate() + "SPOT-GATE RRHO 0 PASS\n",
                    valid_gate().replace("SPOT-GATE COMPLETE", "")):
            with self.assertRaises(Refusal):
                parse_gate(bad)

    def test_declared_caps_cannot_be_missing_zero_or_boolean(self):
        values = dict(setup_seconds=60, bootstrap_axial_seconds=60,
                      bootstrap_radial_seconds=120, radial_seconds=120,
                      axial_seconds=80, host_seconds=10, max_maps=50, total_seconds=20000)
        Budget(**values).validate()
        for key in values:
            with self.subTest(key=key), self.assertRaises(Refusal):
                Budget(**dict(values, **{key: 0})).validate()
        with self.assertRaises(Refusal):
            Budget(**dict(values, max_maps=True)).validate()

    def test_marker_must_have_executed_not_just_appear_in_listing(self):
        text = 'ECHO "DONE" ;'.ljust(123) + '0001\nnormal end of execution for dragon\n'
        with self.assertRaises(Refusal):
            check_dragon_log(text, "DONE")
        listed_abort = "MODULE GREP: ABORT: END: ;".ljust(123) + "0002\n"
        check_dragon_log(text + listed_abort + "<|MODULE ABORT: ; |<0002\n>|DONE\n", "DONE")
        with self.assertRaises(Refusal):
            check_dragon_log(text + ">|DONE\n XABORT: actual failure\n", "DONE")
        check_dragon_log("normal end of execution for dragon\n", "")

    def test_pack_has_exact_slots_and_uses_no_numerical_solver(self):
        text = pack_archives_deck()
        for forbidden in ("FLU:", "ASM:", "LIB:", "SPOPOD"):
            self.assertNotIn(forbidden, text)
        self.assertEqual(text.count("RECOVER: STATE_A :: ITEM 1"), 7)
        self.assertEqual(text.count("RECOVER: STATE_B :: ITEM 1"), 2)
        self.assertEqual(text.count("LIST 3 ITEM 1"), 3)
        self.assertEqual(text.count("GETVAL 'LISTDIM'"), 2)

    def test_manifest_rejects_duplicates_and_directory_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest"
            for body in ("a" * 64 + "  ../Dragon\n",
                         ("a" * 64 + "  Dragon\n") * 2):
                path.write_text(body)
                with self.assertRaises(Refusal):
                    read_manifest(path, sha256(path))

    def fixture(self, root, rank=2):
        root = root.resolve()
        for patcher in (patch("production_runner.ARTIFACTS_ROOT", root.parent),
                        patch("production_runner.shutil.disk_usage", return_value=SimpleNamespace(free=100 * 2**30))):
            patcher.start()
            self.addCleanup(patcher.stop)
        inputs = {}
        payload = {"snapshot_A": "A-archive", "snapshot_B": "B-archive",
                   "radial_track_A": "same geometry", "radial_track_B": "same geometry",
                   "snapshot_log_A": ">|AXMAT-SNAPSHOT-A-COMPLETE\nnormal end of execution for dragon\n",
                   "snapshot_log_B": ">|AXMAT-SNAPSHOT-B-COMPLETE\nnormal end of execution for dragon\n",
                   "material_manifest": "{}"}
        source_spec = ROOT / "validation/axial_material" / ("case_spec.json" if rank == 2
                                                          else "case_spec_rank1_sensitivity.json")
        spec = json.loads(source_spec.read_text())
        # Private synthetic declaration: its actual records and offline/online
        # controls agree. The historical declarations remain unchanged failures.
        spec["production"]["offline_snapshot_controls"].update(eps=2.5e-7, eps_mccg=1e-5)
        specpath = root / "test_case_spec.json"
        specpath.write_text(json.dumps(spec))
        geometry = ROOT / "data/rnr_0burn_spot_proc/irena_pincell.dat"
        manifest = {"geometry": {"regions": 8, "hex_side_cm": .61776479,
                    "radii_cm": spec["geometry"]["radii_inner_to_outer_cm"]},
                    "cases": spec["cases"], "training_slots": list("ABA"),
                    "source_files": {"geometry.dat": {"path": str(geometry), "sha256": sha256(geometry)}},
                    "config": dict(pu_A=.21, u_A=.79, pu_B=.2436, u_B=.7564,
                                   fuel_C=750., clad_C=620., sodium_C=475., snapshot_eps=2.5e-7,
                                   mccg_eps=1e-5, maxout=500, track_angles=48, track_density=100.)}
        payload["material_manifest"] = json.dumps(manifest)
        for name, text in payload.items():
            path = root / name
            if name in ("snapshot_A", "snapshot_B"):
                write_snapshot(path, tag=name[-1])
            else:
                path.write_text(text)
            inputs[name] = {"path": str(path), "sha256": sha256(path)}
        receipt = {"schema_version": 1, "classification": "VALID_SNAPSHOTS",
                   "runtime_sha256": DRAGON_SHA,
                   "inputs_manifest_sha256": inputs["material_manifest"]["sha256"], "states": {}}
        for state in ("A", "B"):
            receipt["states"][state] = {
                "groups": 370, "regions": 8, "snapshots": 1, "fission_components": 32,
                "archive_sha256": inputs[f"snapshot_{state}"]["sha256"],
                "radial_track_sha256": inputs[f"radial_track_{state}"]["sha256"],
                "snapshot_log_sha256": inputs[f"snapshot_log_{state}"]["sha256"]}
        path = root / "material_results"
        path.write_text(json.dumps(receipt))
        inputs["material_results"] = {"path": str(path), "sha256": sha256(path)}
        source_addendum = ROOT / "validation/axial_material" / ("case_spec_rank_addendum.json" if rank == 2
                                                               else "case_spec_rank1_sensitivity_addendum.json")
        rank_rules = json.loads(source_addendum.read_text())
        rank_rules["case_spec_sha256"] = sha256(specpath)
        addendum = root / "test_rank_addendum.json"
        addendum.write_text(json.dumps(rank_rules))
        declaration = {"schema_version": 1, "experiment_id": spec["experiment_id"], "cases": ["AAA", "ABA"],
                       "case_spec": {"path": str(specpath), "sha256": sha256(specpath)},
                       "rank_addendum": {"path": str(addendum), "sha256": sha256(addendum)},
                       "artifact_root": str(root.parent), "resource_roots": [str(root)],
                       "production_config": asdict(ProductionConfig(rank=rank)), "inputs": inputs,
                       "budgets": declared_budget()}
        file = root / "declaration.json"
        file.write_text(json.dumps(declaration))
        return file, declaration

    def test_preflight_is_readonly_and_rejects_tampered_material(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            declaration, data = self.fixture(root)
            before = {p.name: sha256(p) for p in root.iterdir()}
            with patch("production_runner.pinned_runtime_files", return_value={}):
                result = preflight(declaration, sha256(declaration))
            self.assertEqual(result["cases"], ["AAA", "ABA"])
            self.assertEqual(before, {p.name: sha256(p) for p in root.iterdir()})
            (root / "snapshot_B").write_text("changed")
            with patch("production_runner.pinned_runtime_files", side_effect=AssertionError("too late")):
                with self.assertRaises(Refusal):
                    preflight(declaration, sha256(declaration))

    def test_historical_failed_declaration_is_rejected_before_runtime_or_solver(self):
        declaration = ROOT / "validation/artifacts/axial-material-inputs-20261003/production_declaration_rank1.json"
        if not declaration.exists():
            self.skipTest("sealed local historical experiment is unavailable")
        before = sha256(declaration)
        with patch("production_runner.resource_monitor", return_value=SimpleNamespace(check=lambda: {})), \
                patch("production_runner.pinned_runtime_files", side_effect=AssertionError("must reject first")), \
                patch("production_runner.subprocess.Popen", side_effect=AssertionError("no solver")):
            with self.assertRaisesRegex(Refusal, "snapshot control preflight failed") as caught:
                preflight(declaration, before)
        reports = json.loads(str(caught.exception).split(": ", 1)[1])
        self.assertEqual(set(reports), {"A", "B"})
        for state in reports.values():
            self.assertTrue(all(not record["pass"] for record in state["records"].values()))
            self.assertEqual(state["records"]["FLUX/EPS-CONVERGE"]["allowed_field1_bits"],
                             ["0x348637bd", "0x3356bf95"])
            self.assertEqual(state["records"]["TRACK/REAL-PARAM"]["allowed_field1_bits"], ["0x3727c5ac"])
        self.assertEqual(sha256(declaration), before)

    def test_resource_only_bundle_imports_but_cannot_skip_missing_control_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            declaration, _ = self.fixture(root)
            runtime = root / "runtime"
            runtime.mkdir()
            for name in ("production_runner.py", "production_inputs.py"):
                shutil.copyfile(Path(__file__).with_name(name), runtime / name)
            script = runtime / "check_import.py"
            script.write_text('''import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parent))
import production_runner as runner
assert runner.DiskResources is not None
assert "snapshot_control_preflight" not in sys.modules
runner.ARTIFACTS_ROOT = Path(sys.argv[3])
with patch.object(runner, "resource_monitor", return_value=SimpleNamespace(check=lambda: {})), \\
     patch.object(runner, "pinned_runtime_files", side_effect=AssertionError("must reject first")), \\
     patch.object(runner.subprocess, "Popen", side_effect=AssertionError("no solver")):
    try:
        runner.preflight(Path(sys.argv[1]), sys.argv[2])
    except runner.Refusal as error:
        assert str(error) == "snapshot control preflight reader unavailable", str(error)
    else:
        raise AssertionError("production preflight skipped its mandatory reader")
print("RESOURCE_IMPORT_PASS_PRODUCTION_PREFLIGHT_REFUSED")
''')
            checked = subprocess.run([sys.executable, "-I", "-B", str(script), str(declaration),
                                      sha256(declaration), str(root.parent)],
                                     capture_output=True, text=True, timeout=10)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(checked.stdout.strip(), "RESOURCE_IMPORT_PASS_PRODUCTION_PREFLIGHT_REFUSED")
            self.assertFalse((runtime / "snapshot_control_preflight.py").exists())

    def test_old_runtime_and_unfinished_material_never_reach_runtime_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            declaration, data = self.fixture(root)
            receipt = root / "material_results"
            content = json.loads(receipt.read_text())
            content["runtime_sha256"] = "old"
            receipt.write_text(json.dumps(content))
            data["inputs"]["material_results"]["sha256"] = sha256(receipt)
            declaration.write_text(json.dumps(data))
            with patch("production_runner.pinned_runtime_files", side_effect=AssertionError("too late")):
                with self.assertRaises(Refusal):
                    preflight(declaration, sha256(declaration))

    def test_prepared_local_file_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = root / "deck.x2m"
            deck.write_text("original")
            prepared = root / "prepared.json"
            _, data = self.fixture(root)
            data.update(classification="PREPARED_NO_TRANSPORT", local_files={deck.name: sha256(deck)})
            prepared.write_text(json.dumps(data))
            digest = sha256(prepared)
            verify_prepared(prepared, digest)
            deck.write_text("modified tolerance")
            with self.assertRaises(Refusal):
                verify_prepared(prepared, digest)

    def test_total_deadline_refuses_before_opening_log_or_spawning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executor = SerialExecutor.__new__(SerialExecutor)
            executor.work = root
            executor.deadline = time.monotonic() - 1
            with patch("production_runner.subprocess.Popen", side_effect=AssertionError("must not spawn")):
                with self.assertRaises(Refusal):
                    executor.execute(root, "expired", ["not-run"], 10)
            self.assertEqual(list(root.iterdir()), [])

    def test_existing_run_claim_prevents_retry_before_executor_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepared = root / "prepared.json"
            _, data = self.fixture(root)
            data.update(classification="PREPARED_NO_TRANSPORT", local_files={})
            prepared.write_text(json.dumps(data))
            (root / "AAA").mkdir()
            with patch("production_runner.SerialExecutor", side_effect=AssertionError("must not start")):
                with self.assertRaises(FileExistsError):
                    run(prepared, sha256(prepared))

    def prepare_fixture(self, root, rank=2):
        declaration, _ = self.fixture(root, rank)
        runtime_files = {}
        for name in ("Dragon", "SpotRefR64.c2m", "SpotPlaneR64.c2m", "SpotStepR64.c2m"):
            path = root / name
            path.write_text("inert runtime")
            runtime_files[name] = {"path": str(path), "sha256": sha256(path)}
        with patch("production_runner.pinned_runtime_files", return_value=runtime_files):
            result = prepare(declaration, sha256(declaration), root / "prepared_work")
        return Path(result["prepared"]), result["sha256"]

    def test_default_aaa_stops_waiting_reference_and_does_not_start_aba(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ("long-artifact-directory-" * 5)
            root.mkdir()
            prepared, digest = self.prepare_fixture(root)
            with patch("production_runner.SerialExecutor", FakeExecutor):
                result = run(prepared, digest)
            self.assertEqual(result["classification"], "WAITING_REFERENCE")
            self.assertEqual(result["cases"]["AAA"]["classification"], "VALID_MET")
            self.assertEqual(result["max_maps_per_case"], 100)
            self.assertEqual(result["wall_cap_seconds_per_case"], 21600)
            self.assertFalse((prepared.parent / "ABA").exists())
            for _, _, command, _ in FakeExecutor.instances[-1].calls:
                for argument in command[1:]:
                    if argument.endswith(".xsm"):
                        self.assertLessEqual(len(argument), 72)
                        self.assertEqual(Path(argument).name, argument)
            with patch("production_runner.SerialExecutor", side_effect=AssertionError("must not start")):
                with self.assertRaisesRegex(Refusal, "explicit independent"):
                    run(prepared, digest, "ABA")
            self.assertFalse((prepared.parent / "ABA").exists())

    def test_prepare_freezes_control_reader_and_refuses_modified_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared, digest = self.prepare_fixture(Path(tmp))
            info = verify_prepared(prepared, digest)
            reader = prepared.parent / "runtime/snapshot_control_preflight.py"
            self.assertEqual(sha256(reader), sha256(Path(__file__).with_name(reader.name)))
            self.assertEqual(info["local_files"]["runtime/snapshot_control_preflight.py"], sha256(reader))
            self.assertTrue(all(item["classification"] == "PASS_SNAPSHOT_CONTROL_COMPATIBILITY"
                                for item in info["snapshot_control_audits"].values()))
            reader.write_text(reader.read_text() + "\n# changed frozen reader\n")
            with self.assertRaises(Refusal):
                verify_prepared(prepared, digest)

    def test_rank_input_precision_failure_stops_before_any_case_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared, digest = self.prepare_fixture(Path(tmp))
            with patch("production_runner.SerialExecutor", FakeExecutor), patch.object(FakeExecutor, "rank_pass", False):
                result = run(prepared, digest)
            self.assertEqual(result["classification"], "INCONCLUSIVE_RANK_INPUT_PRECISION")
            self.assertFalse((prepared.parent / "AAA/bootstrap").exists())
            self.assertFalse((prepared.parent / "ABA").exists())

    def test_protocol_rejects_wrong_zone_boundary_rank_or_budget(self):
        spec = json.loads((ROOT / "validation/axial_material/case_spec.json").read_text())
        check_protocol(spec, ProductionConfig(), Budget(**declared_budget()))
        for change in (dict(zone_height_cm=40), dict(cells_per_zone=8), dict(rank=1), dict(sn=16)):
            with self.subTest(change=change), self.assertRaises(Refusal):
                check_protocol(spec, ProductionConfig(**change), Budget(**declared_budget()))
        for field, value in (("max_maps", 200), ("total_seconds", 43200)):
            with self.assertRaises(Refusal):
                check_protocol(spec, ProductionConfig(), Budget(**dict(declared_budget(), **{field: value})))
        spec["geometry"]["radial_boundary"] = "specular reflection"
        with self.assertRaises(Refusal):
            check_protocol(spec, ProductionConfig(), Budget(**declared_budget()))

    def test_rank_record_check_reads_full_spectrum_and_strict_real32_floor(self):
        text = rank_precision_deck()
        self.assertIn("9.5367431640625D-7", text)
        self.assertIn("stwo limit >", text)
        self.assertEqual(text.count("GETVAL 'POD-SIGMA-G'"), 3)
        self.assertIn("rank 2 =", text)
        self.assertNotIn("FLU:", text)
        rows = "".join(f">|AXMAT-RANK-SPECTRUM {i} 2 1.0E+0 9.5367431640625E-7 0.0E+0 .FALSE.\n"
                       for i in range(1, 371)) + ">|AXMAT-RANK-INPUT-PRECISION-FAIL\n"
        self.assertEqual(parse_rank_admission(rows)["classification"], "INCONCLUSIVE_RANK_INPUT_PRECISION")
        for bad in (rows.replace(".FALSE.", ".TRUE."), rows.replace("SPECTRUM 370", "SPECTRUM 369")):
            with self.assertRaises(Refusal):
                parse_rank_admission(bad)

    def test_rank1_retains_full_spectrum_without_a_second_direction_floor(self):
        deck = rank_precision_deck(1)
        self.assertIn("rank 1 =", deck)
        self.assertIn("sone limit >", deck)
        self.assertNotIn("stwo limit >", deck)
        self.assertEqual(deck.count("GETVAL 'POD-SIGMA-G'"), 3)
        for second in ("0.0E+0", "1.0E-8", "1.0E-3"):
            rows = "".join(f">|AXMAT-RANK-SPECTRUM {i} 1 1.0E+0 {second} 0.0E+0 .TRUE.\n"
                           for i in range(1, 371)) + ">|AXMAT-RANK-INPUT-PRECISION-PASS\n"
            result = parse_rank_admission(rows, 1)
            self.assertEqual(result["classification"], "VALID_RANK_INPUT_PRECISION")
            self.assertEqual(result["requested_rank"], 1)
            self.assertEqual(result["groups"][0]["sigma"], [1., float(second), 0.])
            self.assertEqual(result["groups"][0]["input_resolution_floor"], 9.5367431640625e-7)
            with self.assertRaises(Refusal):
                parse_rank_admission(rows, 2)
        for rank, first in ((1, "0.0E+0"), (2, "1.0E+0"), (1, "1.0E+999")):
            rows = "".join(f">|AXMAT-RANK-SPECTRUM {i} {rank} {first} 0.0E+0 0.0E+0 .FALSE.\n"
                           for i in range(1, 371)) + ">|AXMAT-RANK-INPUT-PRECISION-FAIL\n"
            self.assertEqual(parse_rank_admission(rows, 1)["classification"],
                             "INCONCLUSIVE_RANK_INPUT_PRECISION")

    def test_rank_addendum_is_bound_to_rank_spec_and_unchanged_floor(self):
        for rank, filename, threshold in ((1, "case_spec_rank1_sensitivity_addendum.json", "selected_sigma_over_sigma1_strict_min"),
                                           (2, "case_spec_rank_addendum.json", "sigma2_over_sigma1_strict_min")):
            addendum = json.loads((ROOT / "validation/axial_material" / filename).read_text())
            digest = addendum["case_spec_sha256"]
            check_rank_addendum(addendum, digest, rank)
            for changed, spec_sha, requested in ((addendum, "wrong-spec", rank),
                                                (addendum, digest, 3-rank),
                                                (dict(addendum, **{threshold: 1e-8}), digest, rank)):
                with self.assertRaises(Refusal):
                    check_rank_addendum(changed, spec_sha, requested)

    def test_rank1_preparation_and_aaa_keep_reference_and_budget_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared, digest = self.prepare_fixture(Path(tmp), rank=1)
            info = verify_prepared(prepared, digest)
            self.assertEqual(info["production_config"]["rank"], 1)
            self.assertIn("rank 1 =", (prepared.parent / "decks/rank_precision.x2m").read_text())
            self.assertIn("SPOD 1 FIXB", (prepared.parent / "decks/case_setup.x2m").read_text())
            with patch("production_runner.SerialExecutor", FakeExecutor):
                result = run(prepared, digest)
            self.assertEqual(result["classification"], "WAITING_REFERENCE")
            self.assertEqual(result["cases"]["AAA"]["classification"], "VALID_MET")
            self.assertEqual(result["max_maps_per_case"], 100)
            self.assertEqual(result["wall_cap_seconds_per_case"], 21600)
            admission = json.loads((prepared.parent / "training/rank_admission.json").read_text())
            self.assertEqual(admission["requested_rank"], 1)
            self.assertEqual(len(admission["groups"]), 370)
            with patch("production_runner.SerialExecutor", side_effect=AssertionError("must not start")):
                with self.assertRaisesRegex(Refusal, "explicit independent"):
                    run(prepared, digest, "ABA")
            self.assertFalse((prepared.parent / "ABA").exists())

    def test_aba_requires_all_reference_checks_and_fresh_per_case_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepared, digest = self.prepare_fixture(root)
            with patch("production_runner.SerialExecutor", FakeExecutor):
                aaa = run(prepared, digest)
            info = verify_prepared(prepared, digest)
            receipt = {"schema_version": 1, "case": "AAA", "classification": "AAA_REFERENCE_QUALIFIED",
                       "method": "independent_continuous_energy_openmc", "experiment_id": info["experiment_id"],
                       "aaa_run_status_sha256": sha256(prepared.parent / "AAA/run_status.json"),
                       "prepared_sha256": digest, "case_spec_sha256": info["case_spec"]["sha256"],
                       "rank_addendum_sha256": info["rank_addendum"]["sha256"],
                       "common_basis_sha256": aaa["common_basis_sha256"],
                       "checks": dict.fromkeys(REFERENCE_CHECKS, "PASS"), "evidence": {}}
            for name in ("statistics", "input_equivalence", "currents_balance_symmetry"):
                path = root / (name + ".json")
                path.write_text('{"status":"PASS"}')
                receipt["evidence"][name] = {"path": str(path), "sha256": sha256(path)}
            qualification = root / "reference.json"
            for name in REFERENCE_CHECKS:
                bad = dict(receipt, checks=dict(receipt["checks"], **{name: "INCONCLUSIVE"}))
                qualification.write_text(json.dumps(bad))
                with self.assertRaises(Refusal):
                    qualify_aba(info, prepared.parent, digest, qualification, sha256(qualification))
            qualification.write_text(json.dumps(receipt))
            with patch("production_runner.SerialExecutor", FakeExecutor):
                aba = run(prepared, digest, "ABA", qualification, sha256(qualification))
            self.assertEqual(aba["classification"], "WAITING_REFERENCE")
            self.assertEqual(aba["case"], "ABA")
            self.assertEqual(aba["common_basis_sha256"], aaa["common_basis_sha256"])
            self.assertEqual(aba["max_maps_per_case"], 100)
            self.assertEqual(FakeExecutor.instances[-1].total_seconds, 21600)
            self.assertNotIn("common_basis", [c[1] for c in FakeExecutor.instances[-1].calls])

    def test_resource_scope_rejects_outside_overlapping_and_symlink_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            first = base / "new-material"
            first.mkdir()
            alias = base / "alias"
            alias.symlink_to(first, target_is_directory=True)
            self.assertEqual(validate_resource_roots([str(first), str(base / "future-production")], base),
                             [first, base / "future-production"])
            for roots in ([], [str(base)], [str(base.parent)], [str(first), str(first)],
                          [str(first), str(first / "nested")], [str(alias)]):
                with self.subTest(roots=roots), self.assertRaises(Refusal):
                    validate_resource_roots(roots, base)

    def test_resource_usage_counts_regular_files_without_following_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            current, old = base / "new-case", base / "old-d4-not-declared"
            current.mkdir()
            old.mkdir()
            (current / "result.bin").write_bytes(b"x" * 11)
            (current / "nested").mkdir()
            (current / "nested/flux.bin").write_bytes(b"y" * 7)
            (old / "immutable.bin").write_bytes(b"z" * 500)
            (current / "old_file").symlink_to(old / "immutable.bin")
            (current / "old_directory").symlink_to(old, target_is_directory=True)
            monitor = DiskResources(base, [str(current), str(base / "future")], 100, 18)
            with patch("production_runner.shutil.disk_usage", return_value=SimpleNamespace(free=100)):
                snapshot = monitor.check()
            self.assertEqual(snapshot["artifact_bytes"], 18)
            self.assertEqual(snapshot["regular_files"], 2)
            (current / "overflow").write_bytes(b"!")
            with patch("production_runner.shutil.disk_usage", return_value=SimpleNamespace(free=100)):
                with self.assertRaisesRegex(ResourceFailure, "artifact budget"):
                    monitor.check()
            self.assertTrue((current / "overflow").exists())
            with patch("production_runner.shutil.disk_usage", return_value=SimpleNamespace(free=99)):
                with self.assertRaisesRegex(ResourceFailure, "free disk"):
                    DiskResources(base, [str(current)], 100, 1000).check()

    def test_pre_stage_resource_failure_records_failure_without_child_or_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executor = SerialExecutor.__new__(SerialExecutor)
            executor.work, executor.stages_path = root, root / "stages.json"
            executor.deadline, executor.records = time.monotonic() + 60, []
            executor.resources = Mock()
            executor.resources.check.side_effect = ResourceFailure({"reason": "disk floor"})
            with patch("production_runner.subprocess.Popen", side_effect=AssertionError("must not spawn")):
                with self.assertRaises(ResourceFailure):
                    executor.execute(root, "blocked", ["not-run"], 10)
            self.assertFalse((root / "blocked.log").exists())
            record = json.loads((root / "stages.json").read_text())["stages"][0]
            self.assertEqual(record["status"], "FAIL_RESOURCE")

    def test_active_child_is_terminated_when_resource_limit_fails(self):
        executor = SerialExecutor.__new__(SerialExecutor)
        executor.env = {}
        executor.resources = Mock()
        executor.resources.check.side_effect = [{"artifact_bytes": 1}, ResourceFailure({"reason": "cap exceeded"})]
        executor.bounded = Mock(TERM_GRACE_SECONDS=5)
        executor.bounded.finish_liveness_watchdog.side_effect = lambda fd, _: os.close(fd)
        process = Mock(pid=12345)
        process.wait.side_effect = subprocess.TimeoutExpired(["inert"], 1)
        with patch("production_runner.subprocess.Popen", return_value=process):
            with self.assertRaises(ResourceFailure):
                executor._process(["inert"], Path("."), subprocess.DEVNULL, Mock(), 100)
        executor.bounded.terminate_group.assert_called_once_with(process)
        executor.bounded.finish_liveness_watchdog.assert_called_once()
        self.assertLessEqual(process.wait.call_args.kwargs["timeout"], 1.0)

    def test_case_resource_failure_is_retained_as_fail_resource(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared, digest = self.prepare_fixture(Path(tmp))
            with patch("production_runner.SerialExecutor", FakeExecutor), patch.object(
                    DiskResources, "check", side_effect=ResourceFailure({"reason": "budget exceeded"})):
                with self.assertRaises(ResourceFailure):
                    run(prepared, digest)
            status = json.loads((prepared.parent / "AAA/run_status.json").read_text())
            self.assertEqual(status["classification"], "FAIL_RESOURCE")
            self.assertTrue((prepared.parent / "AAA/run_claim.json").is_file())
            self.assertFalse((prepared.parent / "archives").exists())


if __name__ == "__main__":
    unittest.main()

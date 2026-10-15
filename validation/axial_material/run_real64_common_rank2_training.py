#!/usr/bin/env python3
"""One bounded A/B/A training attempt using the already qualified REAL64 states.

This entry never produces material or snapshots and never starts AAA or ABA.
The caller supplies the newly built Dragon with a content pin.  The actual
basis must independently report ROOT-FLUX64/type 4 before the unchanged rank2
input-resolution gate can pass.  No failed attempt is resumed or overwritten.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import re
import shutil
import signal
import sys
import time

from production_inputs import ProductionConfig, build_decks
from production_runner import (
    ARTIFACTS_ROOT, ROOT, DiskResources, Refusal, ResourceFailure,
    check_rank_addendum, dump_json, pack_archives_deck,
    parse_rank_admission, rank_precision_deck, require_file, sha256,
    validate_resource_roots,
)
from qualify_refined_AAA_layered_full import OwnRSSSerialExecutor
from moment_order_complete_history_resource_trie_20261010 import DynamicHistoryResources


SPEC = ROOT / "validation/axial_material/case_spec.json"
SPEC_SHA = "ac3e67ffdc25f5bfa45bca5170253de8e875c983550e5ee878ee30c5d1a4c2c4"
ADDENDUM = ROOT / "validation/axial_material/case_spec_rank_addendum.json"
ADDENDUM_SHA = "1f80d491636dbddd3eba1661bb7debbc2992978e827ae9385a27ca9172161910"
RECEIPT = ARTIFACTS_ROOT / "axial-material-qualified-AB-admission-v2-20261004/producer_ingestion_receipt.json"
RECEIPT_SHA = "077ffb8114351131c7f8cd6553c52f952f0c7cd769c3ca7315670226f5d1bc7a"
BOUNDED = ARTIFACTS_ROOT / "d4a-scattering-mesh12-picard-runtime-20260925/run_bounded_dragon.py"
BOUNDED_SHA = "bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09"
TOTAL_CAP_SECONDS = 1800
FRESH_OUTPUT_CAP_BYTES = 2 * 2**30


class TrainingResources:
    """Compose the existing history guard with the tighter fresh-output cap."""
    def __init__(self, output: Path, extra_resource_roots=()):
        roots = [str(output), *(str(path) for path in extra_resource_roots)]
        self.history = DynamicHistoryResources(
            ARTIFACTS_ROOT, roots, 8 * 2**30, 96 * 2**30,
            failure_type=ResourceFailure,
        )
        self.fresh = DiskResources(
            ARTIFACTS_ROOT, roots, 8 * 2**30, FRESH_OUTPUT_CAP_BYTES,
        )

    def check(self) -> dict:
        return {"complete_history": self.history.check(), "fresh_output": self.fresh.check()}


def pinned_json(path: Path, digest: str) -> dict:
    return json.loads(require_file(path, digest).read_text())


def configuration(spec: dict) -> ProductionConfig:
    basis, geometry, production = spec["basis"], spec["geometry"], spec["production"]
    if (basis["requested_rank"] != 2 or basis["training_slots"] != ["A", "B", "A"]
            or basis["fixed_once_for_both_cases"] is not True
            or geometry["physical_z_edges_cm"] != [0, 50, 100, 150]):
        raise Refusal("original fixed common rank2/physical-height contract differs")
    radial, axial = production["radial_controls"], production["axial_controls"]
    config = ProductionConfig(
        cells_per_zone=geometry["cells_per_zone"], zone_height_cm=50.0,
        sn=production["sn"], rank=2,
        eps_radial=radial["eps"], eps_axial=axial["eps"],
        eps_mccg=radial["eps_mccg"], maxout=radial["maxout"],
        maxinr=radial["maxinr"], radial_acce_free=radial["acce"][0],
        radial_acce_accel=radial["acce"][1], axial_acce_free=axial["acce"][0],
        axial_acce_accel=axial["acce"][1],
    )
    config.validate()
    return config


def verify_inputs(dragon: Path, dragon_sha: str) -> tuple[dict, dict, dict]:
    """Stream the fixed inputs and read saved audit META; run no producer/audit."""
    spec = pinned_json(SPEC, SPEC_SHA)
    check_rank_addendum(pinned_json(ADDENDUM, ADDENDUM_SHA), SPEC_SHA, 2)
    receipt = pinned_json(RECEIPT, RECEIPT_SHA)
    if (receipt["schema"] != "AXMAT_QUALIFIED_OFFLINE_PRODUCER_TO_LEGACY_BOOT_V1"
            or receipt["offline_r64_directly_consumed_by_boot"] is not False):
        raise Refusal("existing offline producer receipt or BOOT semantics differ")
    evidence = {
        "case_spec": {"path": str(SPEC), "sha256": SPEC_SHA},
        "rank_addendum": {"path": str(ADDENDUM), "sha256": ADDENDUM_SHA},
        "producer_receipt": {"path": str(RECEIPT), "sha256": RECEIPT_SHA},
        "Dragon": {"path": str(require_file(dragon, dragon_sha, True)), "sha256": dragon_sha},
        "bounded_runner": {"path": str(require_file(BOUNDED, BOUNDED_SHA)), "sha256": BOUNDED_SHA},
    }
    for letter in ("A", "B"):
        state = receipt["states"][letter]
        for name in ("archive", "track", "material", "audit_status"):
            item = state[name]
            require_file(Path(item["path"]), item["sha256"])
            evidence[f"{letter}_{name}"] = dict(item)
        audit = json.loads(Path(state["audit_status"]["path"]).read_text())
        if (audit["classification"] != "R64_SNAPSHOT_TERMINAL_AUDIT_PASS"
                or audit["snapshot_qualified"] is not True
                or audit["frozen_inputs_unchanged"] is not True
                or state["payload_audit"]["classification"] != "PASS_OFFLINE_PAYLOAD_AND_LEGACY_BOOT_MIRROR"
                or state["payload_audit"]["archive_sha256"] != state["archive"]["sha256"]):
            raise Refusal(f"state {letter} has no retained qualified REAL64 snapshot")
    if receipt["states"]["A"]["track"]["sha256"] != receipt["states"]["B"]["track"]["sha256"]:
        raise Refusal("A/B tracks differ")
    if receipt["states"]["A"]["payload_audit"]["volume64_sha256"] != receipt["states"]["B"]["payload_audit"]["volume64_sha256"]:
        raise Refusal("A/B saved collision-normalization owners differ")
    return spec, receipt, evidence


def training_deck(config: ProductionConfig) -> str:
    # Match production_runner.prepare: publish even a deficient basis first,
    # then read its independent complete spectrum; case FIXB gates stay intact.
    text = build_decks(config)["common_basis.x2m"]
    start = text.index("GREP: SYSTEM :: GETVAL 'STATE-VECTOR'")
    end = text.index("BASIS_ARCH := SYSTEM ;", start)
    return text[:start] + text[end:]


def independent_rank_deck() -> str:
    text = rank_precision_deck(2)
    text = text.replace("MODULE GREP: END: ;", "MODULE GREP: ABORT: END: ;", 1)
    anchor = "INTEGER igr idx rank ngroup ;\n"
    declarations = ("INTEGER in_type in_tkind in_twords ;\n"
                    "INTEGER in_skind in_swords ;\nSTRING in_source ;\n")
    text = text.replace(anchor, anchor + declarations, 1)
    anchor = "EVALUATE igr := 0 ;\n"
    provenance = """GREP: BASIS :: TYPE 'POD-INPUT-TY' >>in_tkind<< ;
GREP: BASIS :: LENGTH 'POD-INPUT-TY' >>in_twords<< ;
IF in_tkind 1 <> THEN
  ABORT: ;
ENDIF ;
IF in_twords 1 <> THEN
  ABORT: ;
ENDIF ;
GREP: BASIS :: GETVAL 'POD-INPUT-TY' 1 >>in_type<< ;
GREP: BASIS :: TYPE 'POD-IN-SRC' >>in_skind<< ;
GREP: BASIS :: LENGTH 'POD-IN-SRC' >>in_swords<< ;
IF in_skind 3 <> THEN
  ABORT: ;
ENDIF ;
IF in_swords 3 <> THEN
  ABORT: ;
ENDIF ;
GREP: BASIS :: GETVAL 'POD-IN-SRC' 1 12 >>in_source<< ;
ECHO "AXMAT-POD-INPUT" in_type in_source ;
IF in_type 4 <> THEN
  ABORT: ;
ENDIF ;
IF in_source "ROOT-FLUX64" <> THEN
  ABORT: ;
ENDIF ;
"""
    return text.replace(anchor, provenance + anchor, 1)


def check_provenance(log: str) -> None:
    rows = re.findall(
        r'^>\|AXMAT-POD-INPUT\s+(\d+)\s+("[^"\n]*"|[^\s|]+)'
        r'\s*(?:\|>\d+)?\s*$', log, re.M)
    if [(kind, source.strip('"').strip()) for kind, source in rows] != [("4", "ROOT-FLUX64")]:
        raise Refusal("actual independent basis input is not exactly type4 ROOT-FLUX64")


def run(dragon: Path, dragon_sha: str, output: Path,
        whole_seconds: int = TOTAL_CAP_SECONDS, extra_resource_roots=()) -> dict:
    if not re.fullmatch(r"[a-f0-9]{64}", dragon_sha):
        raise Refusal("explicit Dragon SHA256 required")
    if type(whole_seconds) is not int or not 1 <= whole_seconds <= TOTAL_CAP_SECONDS:
        raise Refusal("whole-seconds may only tighten the 1800-second cap")
    if not output.is_absolute() or ".." in output.parts:
        raise Refusal("fresh absolute validation/artifacts output required")
    extra_resource_roots = tuple(extra_resource_roots)
    resource_roots = [str(output), *(str(path) for path in extra_resource_roots)]
    validate_resource_roots(resource_roots, ARTIFACTS_ROOT)
    if output.exists() or output.is_symlink():
        raise Refusal("output already exists: one permanent attempt, no retry/overwrite")
    start = time.monotonic()
    dragon = require_file(dragon, dragon_sha, True)
    spec, receipt, evidence = verify_inputs(dragon, dragon_sha)
    source_pins = {}
    for name in ("production_runner", "production_inputs", "qualify_refined_AAA_layered_full",
                 "moment_order_complete_history_resource_trie_20261010"):
        path = Path(sys.modules[name].__file__).resolve()
        source_pins[name] = {"path": str(path), "sha256": sha256(require_file(path))}
    source_pins["training_entry"] = {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__))}

    def verify_fixed_inputs() -> None:
        verify_inputs(dragon, dragon_sha)
        for item in source_pins.values():
            require_file(Path(item["path"]), item["sha256"])

    config = configuration(spec)
    caps = spec["resource_caps"]
    setup_cap, check_cap = caps["common_basis_wall_s"], caps["postchecks_wall_s"]
    resources = TrainingResources(output, extra_resource_roots)
    output.mkdir()
    for name in ("runtime", "archives", "training"):
        (output / name).mkdir()
    shutil.copy2(BOUNDED, output / "runtime/run_bounded_dragon.py")
    require_file(output / "runtime/run_bounded_dragon.py", BOUNDED_SHA)
    for letter in ("A", "B"):
        (output / "archives" / f"snapshot_{letter}.xsm").symlink_to(receipt["states"][letter]["archive"]["path"])
    decks = {"archives/pack_archives.x2m": pack_archives_deck(),
             "training/common_basis.x2m": training_deck(config),
             "training/rank_precision.x2m": independent_rank_deck()}
    for name, text in decks.items():
        (output / name).write_text(text)
    result = dict(
        schema="AXMAT_REAL64_ORIGINAL_COMMON_RANK2_TRAINING_V1",
        classification="FAILED_NO_RETRY", training_slots=["A", "B", "A"],
        requested_rank=2, production_config=asdict(config),
        original_sigma2_over_sigma1_strict_min=9.5367431640625e-7,
        weight_source="Original TRACK/VOLUME REAL32 bits promoted to REAL64; not AXMAT-V64",
        runtime_and_input_pins=evidence,
        source_pins=source_pins,
        resource_roots=resource_roots,
        deck_sha256={name: sha256(output / name) for name in decks},
        caps=dict(pack_seconds=setup_cap, common_basis_seconds=setup_cap,
                  independent_read_seconds=check_cap, total_seconds=whole_seconds,
                  numerical_stage_total_seconds=2 * setup_cap + check_cap,
                  sampled_child_rss_cap_mib=512, fresh_output_cap_bytes=FRESH_OUTPUT_CAP_BYTES,
                  complete_history_cap_bytes=96 * 2**30, disk_min_free_bytes=8 * 2**30,
                  children_at_once=1, threads=1, automatic_retries=0),
        actual_real64_training_verified=False, common_rank2_admitted=False,
        production_qualified=False, AAA_accuracy_qualified=False, ABA_started=False,
        scope="Common-basis input quality only; no online solve, CE accuracy or ABA qualification.",
    )
    dump_json(output / "run_claim.json", dict(pid=os.getpid(), started_unix=time.time(), Dragon_sha256=dragon_sha))
    dump_json(output / "run_status.json", result)
    remaining = int(whole_seconds - (time.monotonic() - start))
    if remaining <= 0:
        raise Refusal("whole training-harness wall cap exhausted before launch")
    executor = OwnRSSSerialExecutor(output, remaining, "training", resources)
    executor.env["GFORTRAN_UNBUFFERED_ALL"] = "1"
    handlers = {s: signal.signal(s, signal.default_int_handler)
                for s in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    try:
        for directory, deck_name, cap, marker in (
            ("archives", "pack_archives", setup_cap, "AXMAT-ARCHIVE-PACK-COMPLETE"),
            ("training", "common_basis", setup_cap, "AXMAT-COMMON-BASIS-COMPLETE"),
            ("training", "rank_precision", check_cap, "AXMAT-RANK-RECORD-CHECK-COMPLETE"),
        ):
            verify_fixed_inputs()
            if directory == "training" and deck_name == "common_basis":
                (output / "training/training_snapshots.xsm").symlink_to(output / "archives/training_snapshots.xsm")
            text = executor.execute(output / directory, deck_name, [str(dragon)], cap, marker, deck_name + ".x2m")
        check_provenance(text)
        result["actual_real64_training_verified"] = True
        admission = parse_rank_admission(text, 2)
        dump_json(output / "training/rank_admission.json", admission)
        result["classification"] = admission["classification"]
        result["common_rank2_admitted"] = admission["classification"] == "VALID_RANK_INPUT_PRECISION"
        result["failed_groups"] = [g["group"] for g in admission["groups"] if not g["pass"]]
        result["common_basis_sha256"] = sha256(require_file(output / "training/common_basis.xsm"))
    except BaseException as error:
        result["classification"] = "FAIL_RESOURCE" if isinstance(error, ResourceFailure) else "FAILED_NO_RETRY"
        result["error"] = repr(error)
        result["common_rank2_admitted"] = False
    finally:
        result["elapsed_seconds"] = time.monotonic() - start
        try:
            verify_fixed_inputs()
            result["frozen_inputs_unchanged"] = True
            result["resources_after"] = resources.check()
        except BaseException as error:
            result.update(classification="FAIL_RESOURCE" if isinstance(error, ResourceFailure) else "INPUT_IDENTITY_FAILURE",
                          final_check_error=repr(error), common_rank2_admitted=False)
        for folder in ("archives", "training"):
            outputs = {p.name: sha256(p) for p in sorted((output / folder).iterdir())
                       if p.is_file() and not p.is_symlink() and p.name != "result.json"}
            folder_records = [row for row in executor.records if row["label"].startswith(folder + "/")]
            complete = (len(folder_records) == (1 if folder == "archives" else 2)
                        and all(row["status"] == "PASS" for row in folder_records))
            dump_json(output / folder / "result.json", {
                "classification": "SEALED_STAGE_OUTPUTS" if complete else "FAILED_STAGE_OUTPUTS_RETAINED",
                "sha256": outputs,
            })
        result["elapsed_seconds"] = time.monotonic() - start
        if result["elapsed_seconds"] >= whole_seconds:
            result.update(classification="FAIL_RESOURCE", common_rank2_admitted=False,
                          final_check_error="whole training budget exceeded during closeout")
        dump_json(output / "run_status.json", result)
        for signum, handler in handlers.items():
            signal.signal(signum, handler)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dragon", required=True, type=Path)
    parser.add_argument("--dragon-sha256", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--whole-seconds", type=int, default=TOTAL_CAP_SECONDS,
                        help="Root's shared remaining wall budget, integer 1..1800; only tightens the cap")
    args = parser.parse_args()
    result = run(args.dragon, args.dragon_sha256, args.output, args.whole_seconds)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result["common_rank2_admitted"] else 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the direct REAL64 POD consumer, then attempt the original common rank2.

One fresh build and one fresh training attempt share the original 1800-second
engineering envelope.  The training's original 120-second stage caps and all
spectral gates remain in force.  No AAA or ABA solve follows this entry.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import sys
import time

from production_runner import ROOT, ARTIFACTS_ROOT, dump_json, require_file, sha256
from qualify_refined_AAA_layered_full import OwnRSSSerialExecutor
import run_real64_common_rank2_training as training

TOTAL_SECONDS = 1800
LIBRARIES = {
    "lib/Darwin_arm64/libDragon.a": "954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9",
    "Trivac/lib/Darwin_arm64/libTrivac.a": "0b4dc12a834503223adb708751724cd1050b13b97cb8938dcf2ad7dafbde8002",
    "Utilib/lib/Darwin_arm64/libUtilib.a": "a6c5cca8825691fd1da7554acabe542ba9986aabdbc935ecc46d1993240244ca",
    "Ganlib/lib/Darwin_arm64/libGanlib.a": "204d9f3aeaf4e06d8fbb62225e14859a767476cd845ba0096f166b5f9e14822c",
}


def experiment(build_output: Path, training_output: Path,
               spoasm_sha: str, spopod_sha: str) -> dict:
    started = time.monotonic()
    roots = [str(build_output), str(training_output)]
    training.validate_resource_roots(roots, ARTIFACTS_ROOT)
    if any(p.exists() or p.is_symlink() for p in (build_output, training_output)):
        raise ValueError("fresh build and training directories required; no retry")
    compiler = Path(shutil.which("gfortran") or "").resolve(strict=True)
    pins = {str(ROOT / name): digest for name, digest in LIBRARIES.items()}
    pins.update({str(ROOT / "src/SPOASM.f"): spoasm_sha,
                 str(ROOT / "src/SPOPOD.f90"): spopod_sha,
                 str(ROOT / "src/DRAGON.o"): "1ef2ec69741bd0841c1250811b68170d46b96581d27d0c21cb00600c83ae32bb",
                 str(training.BOUNDED): training.BOUNDED_SHA})
    for path in (compiler, Path(__file__).resolve(), Path(training.__file__).resolve(),
                 ROOT / "lib/Darwin_arm64/modules/spot_leakage.mod",
                 ROOT / "Ganlib/lib/Darwin_arm64/modules/ganlib.mod",
                 ROOT / "validation/axial_material/production_runner.py",
                 ROOT / "validation/axial_material/production_inputs.py",
                 ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py",
                 ROOT / "validation/axial_material/moment_order_complete_history_resource_trie_20261010.py"):
        pins[str(path)] = sha256(require_file(path))

    def verify() -> None:
        for name, digest in pins.items():
            require_file(Path(name), digest)

    verify()
    # The retained positive/over-cap controls are for this exact original guard.
    require_file(ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py",
                 "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6")
    build_output.mkdir()
    for name in ("build", "runtime"):
        (build_output / name).mkdir()
    shutil.copy2(training.BOUNDED, build_output / "runtime/run_bounded_dragon.py")
    resources = training.TrainingResources(build_output, (str(training_output),))
    resources.check()
    remaining = int(TOTAL_SECONDS - (time.monotonic() - started))
    if remaining <= 0:
        raise RuntimeError("whole experiment budget exhausted before build")
    executor = OwnRSSSerialExecutor(build_output, remaining, "build", resources)
    executor.env["NUMEXPR_NUM_THREADS"] = "1"
    flags = [str(compiler), "-O2", "-march=native", "-ffp-contract=off",
             "-fcheck=all", "-fbacktrace", "-g", "-fPIC", "-frecord-marker=4",
             "-ffixed-line-length-none", "-ffree-line-length-none",
             "-I" + str(ROOT / "lib/Darwin_arm64/modules"),
             "-I" + str(ROOT / "Ganlib/lib/Darwin_arm64/modules"),
             "-J" + str(build_output / "build")]
    commands = [flags + ["-c", str(ROOT / "src" / source), "-o", str(build_output / "build" / obj)]
                for source, obj in (("SPOPOD.f90", "SPOPOD.o"), ("SPOASM.f", "SPOASM.o"))]
    dragon = build_output / "runtime/Dragon"
    commands.append([str(compiler), "-O2", "-ffp-contract=off", str(ROOT / "src/DRAGON.o"),
                     str(build_output / "build/SPOASM.o"), str(build_output / "build/SPOPOD.o"),
                     *[str(ROOT / name) for name in LIBRARIES], "-o", str(dragon)])
    result = dict(schema="AXMAT_DIRECT_REAL64_POD_ORIGINAL_RANK2_EXPERIMENT_V1",
                  classification="FAILED_NO_RETRY", full_input_sha256=pins,
                  original_case_spec={"path": str(training.SPEC), "sha256": training.SPEC_SHA},
                  commands=commands, whole_wall_cap_seconds=TOTAL_SECONDS,
                  build_stage_wall_cap_seconds=600, training_stage_wall_cap_seconds=120,
                  rss_cap_mib=512, joint_fresh_output_cap_bytes=2 * 2**30,
                  complete_history_cap_bytes=96 * 2**30, free_disk_floor_bytes=8 * 2**30,
                  threads=1, children_at_once=1, retries=0,
                  build_completed=False, common_rank2_admitted=False,
                  AAA_accuracy_qualified=False, ABA_started=False, goal_complete=False)
    dump_json(build_output / "run_claim.json", dict(pid=os.getpid(), started_unix=time.time()))
    dump_json(build_output / "experiment.json", result)
    handlers = {sig: signal.signal(sig, signal.default_int_handler)
                for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM)}
    try:
        for index, command in enumerate(commands):
            verify()
            executor.execute(build_output / "build", f"build_{index:02d}", command, 600)
        verify()
        result["build_completed"] = True
        result["Dragon_sha256"] = sha256(require_file(dragon, executable=True))
        result["object_sha256"] = {name: sha256(build_output / "build" / name)
                                   for name in ("SPOASM.o", "SPOPOD.o")}
        dump_json(build_output / "experiment.json", result)
        remaining = int(TOTAL_SECONDS - (time.monotonic() - started))
        if remaining <= 0:
            raise RuntimeError("whole experiment budget exhausted before training")
        trained = training.run(dragon, result["Dragon_sha256"], training_output,
                               whole_seconds=remaining, extra_resource_roots=(str(build_output),))
        result["training_result"] = {key: trained[key] for key in
            ("classification", "actual_real64_training_verified", "common_rank2_admitted",
             "frozen_inputs_unchanged", "elapsed_seconds") if key in trained}
        result["common_rank2_admitted"] = trained["common_rank2_admitted"]
        result["classification"] = trained["classification"]
        if "failed_groups" in trained:
            result["failed_groups"] = trained["failed_groups"]
    except BaseException as error:
        result.update(classification="FAILED_NO_RETRY", error=repr(error), common_rank2_admitted=False)
    finally:
        result["elapsed_seconds"] = time.monotonic() - started
        try:
            verify()
            result["frozen_inputs_unchanged"] = True
            result["resources_after"] = resources.check()
            result["elapsed_seconds"] = time.monotonic() - started
            if result["elapsed_seconds"] >= TOTAL_SECONDS:
                raise RuntimeError("whole experiment including closeout exceeded original cap")
        except BaseException as error:
            result.update(classification="FINAL_CHECK_FAILURE", final_check_error=repr(error),
                          common_rank2_admitted=False)
        dump_json(build_output / "experiment.json", result)
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-output", type=Path, required=True)
    parser.add_argument("--training-output", type=Path, required=True)
    parser.add_argument("--spoasm-sha256", required=True)
    parser.add_argument("--spopod-sha256", required=True)
    args = parser.parse_args()
    result = experiment(args.build_output, args.training_output, args.spoasm_sha256, args.spopod_sha256)
    print(json.dumps({key: result[key] for key in
        ("classification", "elapsed_seconds", "build_completed", "common_rank2_admitted",
         "failed_groups", "error", "final_check_error") if key in result}, sort_keys=True))
    return 0 if result["common_rank2_admitted"] else 2


if __name__ == "__main__":
    sys.exit(main())

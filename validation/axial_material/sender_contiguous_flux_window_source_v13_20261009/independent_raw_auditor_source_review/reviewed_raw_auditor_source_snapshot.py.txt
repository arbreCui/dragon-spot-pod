"""Independent, bounded raw audit of the FLUSP64 window observer controls.

The observer replaces SPOF64 only in the wrapper unit executable. These checks
prove routing, aliasing and bit preservation; the original real SPOT controls
and a fresh complete native run remain separate requirements.
"""

import hashlib
import json
import math
from pathlib import Path
import stat
import struct


MODES = (
    "all", "suffix", "interior", "scalar_first", "scalar_last", "scalar_one",
    "sparse", "empty_ileak0", "empty_ileak3", "transition",
    "unsupported_reference_active", "unsupported_candidate_active",
    "unsupported_reference_empty", "unsupported_candidate_empty",
)
MAGIC = 0x41584657494E3133
TITLE = b"V13 original sender contiguous output window observer scope only".ljust(72, b" ")
MESSAGE = "FLUSP64: UNSUPPORTED LEAKAGE MODEL."
MASK64 = (1 << 64) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "regular owned raw file required")
    before = identity(path)
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    require(identity(path) == before, "raw file changed during full hash")
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": h.hexdigest()}


def identity(path):
    require(not Path(path).is_symlink(), "owned evidence may contain no symbolic links")
    info = Path(path).stat()
    require(stat.S_ISDIR(info.st_mode) or (stat.S_ISREG(info.st_mode) and info.st_nlink == 1),
            "unique regular files and ordinary directories required")
    return [info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns]


def identity_snapshot(root):
    return {str(path.relative_to(root)): identity(path) for path in [root, *sorted(root.rglob("*"))]}


def same_range(left, right, offset, length):
    with Path(left).open("rb") as a, Path(right).open("rb") as b:
        a.seek(offset); b.seek(offset)
        while length:
            count = min(length, 1024 * 1024)
            x, y = a.read(count), b.read(count)
            require(len(x) == count and x == y, "complete byte comparison failed")
            length -= count


def f32_word(value):
    return struct.unpack("<i", struct.pack("<f", value))[0]


def f64_word(value):
    return struct.unpack("<Q", struct.pack("<d", value))[0]


def fixture(mode, step):
    cid = MODES.index(mode) + 1
    nun, ng = (1800, 370) if mode == "all" else (12, 1 if mode == "scalar_one" else 8)
    active, leak, b4 = [], 0, 0.0
    if cid in (1, 11, 12): active = list(range(1, ng + 1))
    elif cid == 2: active, leak, b4 = list(range(3, ng + 1)), 3, 1.25
    elif cid == 3: active = list(range(2, 6))
    elif cid == 4: active, leak, b4 = [1], 3, -0.0
    elif cid == 5: active, leak, b4 = [ng], 3, -0.75
    elif cid == 6: active = [1]
    elif cid == 7: active, leak, b4 = [1, 3, ng], 3, 1.25
    elif cid == 9: leak, b4 = 3, 1.25
    elif cid == 10:
        leak, b4 = 3, 1.25
        active = {1: list(range(3, ng + 1)), 2: [ng], 3: [1, 3, ng], 4: []}[step]
    if cid >= 11: leak = 2
    route = 0 if not active else 1 if active[-1] - active[0] + 1 == len(active) else 2
    np = [ng + 1 - g if g in active else 0 for g in range(1, ng + 1)]
    return {"id": cid, "nun": nun, "ng": ng, "active": active, "route": route,
            "np": np, "leak": leak, "b4": b4, "nsteps": 1 if cid >= 11 else 4 if cid == 10 else 2}


def layout(f):
    n, g, a = f["nun"], f["ng"], len(f["active"])
    # Header, NPSYS, MAT, KEY, IMERG, VOL, B2, DIFHET, then 72-byte title.
    flux = 8 * (18 + g + 14 + 4 + 7 + 4 + 3 * g) + 72
    maps = flux + 8 * 8 * n * g
    source = maps + 16 * a
    return {"flux": flux, "maps": maps, "source": source, "size": source + 8 * n * a}


def read_record(path, f, step, who):
    offsets = layout(f)
    require(path.stat().st_size == offsets["size"], "raw record must have exact EOF")
    with path.open("rb") as stream:
        header = struct.unpack("<18q", stream.read(144))
        calls = int(bool(f["active"])) if who else 0
        wanted = (MAGIC, 1, f["id"], who, step, f["nun"], f["ng"], 7, 4, 3,
                  len(f["active"]), calls, f["leak"], f["route"])
        require(header[:14] == wanted, "complete dimension, route and call header differs")
        caller, observed, expected_direct, observed_direct = header[14:]
        direct = int(who == 2 and f["route"] == 1)
        if who and f["active"]:
            require(caller > 0 and observed > 0 and caller % 8 == observed % 8 == 0,
                    "actual aligned caller and receiver LOC values required")
            require(expected_direct == observed_direct == direct and int(caller == observed) == direct,
                    "actual receiver alias must match independently derived route")
        else:
            require(header[14:] == (0, 0, 0, 0), "input or empty call addresses must be zero")
        integers = f["np"] + [1, 2, 0, 3, 4, 2, 1] + [1, 0, 4, 5, 1, f["nun"], f["nun"] - 1] + [1, 0, 2, 3]
        integers += [f32_word(i / 8) for i in range(1, 8)]
        integers += [0, 0, 0, f32_word(f["b4"])]
        integers += [f32_word((-1 if (i + g) % 2 else 1) * (i / 4 + g / 128))
                     for g in range(1, f["ng"] + 1) for i in range(1, 4)]
        require(stream.read(8 * len(integers)) == struct.pack("<" + str(len(integers)) + "q", *integers),
                "every input integer and float32 bit word must match independent fixture")
        require(stream.read(72) == TITLE and stream.tell() == offsets["flux"], "exact title/body layout differs")
        stream.seek(offsets["maps"])
        maps = f["active"] + [f["ng"] + 1 - g for g in f["active"]]
        require(stream.read(8 * len(maps)) == struct.pack("<" + str(len(maps)) + "q", *maps),
                "full energy group and actual LCM system ID maps differ")
    return offsets


def initial_flux(path, f, offsets):
    with path.open("rb") as stream:
        stream.seek(offsets["flux"])
        for plane in range(1, 9):
            for group in range(1, f["ng"] + 1):
                block = stream.read(8 * f["nun"])
                require(len(block) == 8 * f["nun"], "complete initial flux required")
                for row, (word,) in enumerate(struct.iter_unpack("<Q", block), 1):
                    wanted = 1 << 63 if (row + group + plane) % 17 == 0 else f64_word(
                        (-1 if (row + group + plane) % 2 else 1) * (plane + group / 32 + row / 1024))
                    require(word == wanted, "all eight initial caller planes must match independent bits")


def source_and_output(inputs, records, f, offsets, negative=False):
    n, g = f["nun"], f["ng"]
    mats, keys, merged = [1, 2, 0, 3, 4, 2, 1], [1, 0, 4, 5, 1, n, n - 1], [1, 0, 2, 3]
    scalar_pairs = 0
    with inputs.open("rb") as base:
        streams = [path.open("rb") for path in records]
        try:
            for col, group in enumerate(f["active"], 1):
                base.seek(offsets["flux"] + ((7 * g + group - 1) * n) * 8)
                raw_sun = base.read(n * 8)
                require(len(raw_sun) == n * 8, "source plane must be complete")
                values = list(struct.unpack("<" + str(n) + "d", raw_sun))
                if f["leak"] == 3 and f["b4"] != 0.0:
                    base.seek(offsets["flux"] + ((g + group - 1) * n) * 8)
                    old = struct.unpack("<" + str(n) + "d", base.read(n * 8))
                    for mat, key in zip(mats, keys):
                        if not key or not mat or not merged[mat - 1]: continue
                        mixture = merged[mat - 1]
                        dif = (-1 if (mixture + group) % 2 else 1) * (mixture / 4 + group / 128)
                        values[key - 1] = values[key - 1] - float(dif) * float(f["b4"]) * old[key - 1]
                require(all(math.isfinite(x) for x in values), "complete source must be finite")
                expected = struct.pack("<" + str(n) + "d", *values)
                for stream in streams:
                    stream.seek(offsets["source"] + (col - 1) * n * 8)
                    require(stream.read(n * 8) == expected, "complete original B1 source/order must match bits")
                if negative: continue
                words = []
                for row, value in enumerate(values, 1):
                    word = (f64_word(value) ^ ((group << 20) + row)) & 0x800FFFFFFFFFFFFF | 0x3FF0000000000000
                    words.append(1 << 63 if (row + col) % 11 == 0 else word)
                wanted_output = struct.pack("<" + str(n) + "Q", *words)
                for stream in streams[1:]:
                    stream.seek(offsets["flux"] + ((6 * g + group - 1) * n) * 8)
                    require(stream.read(n * 8) == wanted_output, "actual full output must match independent finite observer bits")
                    scalar_pairs += n
        finally:
            for stream in streams: stream.close()
    return scalar_pairs


def validate_contract(contract):
    require(contract["schema"] == "AXMAT_FLUSP64_WINDOW_WRAPPER_CONTROL_CONTRACT_V1", "full frozen wrapper contract required")
    require([case["name"] for case in contract["cases"]] == list(MODES), "all fourteen declared cases required")
    total_files, total_bytes = 0, 0
    for case in contract["cases"]:
        f = fixture(case["name"], 1); negative = f["id"] >= 11
        require(case["args"] == [case["name"]] and case["case_id"] == f["id"]
                and case["expected_returncode"] == int(negative) and case["negative"] == negative,
                "fixed actual command/exit contract differs")
        require((case["nun"], case["ngrp"], case["nreg"], case["nmat"], case["nmerg"], case["ileak"])
                == (f["nun"], f["ng"], 7, 4, 3, f["leak"]), "independent fixture dimensions differ")
        expected_raw = []
        for step in range(1, f["nsteps"] + 1):
            f = fixture(case["name"], step)
            for role in (("input",) if negative else ("input", "reference", "candidate")):
                expected_raw.append({"name": f"{case['name']}.s{step}.{role}.bin", "size_bytes": layout(f)["size"], "who": role})
        require(case["raw_files"] == expected_raw, "whole raw filename/size/role declaration differs")
        require(set(case["strict_case_namespace"]) == {x["name"] for x in expected_raw}
                | {"execute.log", "execute.watchdog.json", "wrapper_manifest.jsonl"}, "complete namespace differs")
        require(case["manifest_lines"] == (0 if negative else f["nsteps"]), "complete manifest line count required")
        if negative: require(case["expected_message"] == MESSAGE, "actual unsupported leakage guard message differs")
        else:
            require(len(case["steps"]) == f["nsteps"], "every positive repeated step required")
            require([row["step"] for row in case["steps"]] == list(range(1, f["nsteps"] + 1)),
                    "all declared repeated steps must occur exactly once in order")
            for row in case["steps"]:
                state = fixture(case["name"], row["step"])
                require(row["active_groups"] == len(state["active"]) and row["expected_route"] == state["route"]
                        and row["each_raw_size_bytes"] == layout(state)["size"]
                        and row["reference_observer_calls"] == row["candidate_observer_calls"] == int(bool(state["active"])),
                        "complete independent step/route/size plan differs")
        total_files += len(expected_raw); total_bytes += sum(x["size_bytes"] for x in expected_raw)
    require(total_files == 70 and total_bytes == 288241824, "complete independent raw byte forecast differs")
    return total_files, total_bytes


def audit_sender_controls(controls_root, contract):
    controls_root = Path(controls_root)
    validate_contract(contract)
    require(controls_root.is_dir() and not controls_root.is_symlink(), "owned controls namespace required")
    require({p.name for p in controls_root.iterdir()} == set(MODES), "entire sender case directory namespace required")
    require(not any(p.is_symlink() for p in controls_root.rglob("*")), "sender controls may contain no aliases")
    identities_before = identity_snapshot(controls_root)
    cases, all_raw = [], {}
    steps, observers, compared_scalars, direct_steps, fallback_steps, empty_steps = 0, 0, 0, 0, 0, 0
    for case in contract["cases"]:
        mode = case["name"]; folder = controls_root / mode; f = fixture(mode, 1)
        require(folder.is_dir() and {p.name for p in folder.iterdir()} == set(case["strict_case_namespace"]),
                "every raw/log/watch/manifest file must belong to the exact case")
        watch = json.loads((folder / "execute.watchdog.json").read_text())
        require(type(watch["returncode"]) is int and watch["returncode"] == case["expected_returncode"]
                and watch["command"] == [str(controls_root.parent / "runtime/flusp64_window_observer_controls"), mode],
                "actual numeric child command and return code differ")
        require(watch["limit_failure"] is None and watch["own_child_only"] is True
                and watch["liveness_group_cleanup"] is True and watch["rss_cap_mib"] == 512
                and 0 <= watch["sampled_peak_rss_mib"] < 512
                and 0 < watch["wall_cap_seconds"] <= 600 and 0 <= watch["elapsed_seconds"] < watch["wall_cap_seconds"],
                "original own-child resource and cleanup contract required")
        log = (folder / "execute.log").read_text(); manifest_text = (folder / "wrapper_manifest.jsonl").read_text()
        if case["negative"]:
            require(MESSAGE in log and "ERROR STOP 92" not in log
                    and "OBSERVER_ONLY" not in log and not manifest_text,
                    "unsupported leakage must genuinely abort before observer/normal return")
        else:
            require("AXMAT_FLUSP64_WINDOW_WRAPPER_OBSERVER_CONTROL_V1 OBSERVER_ONLY " + mode in log,
                    "actual observer-only normal completion marker required")
        rows = [json.loads(line) for line in manifest_text.splitlines()]
        wanted_rows = []
        previous = None
        for step in range(1, f["nsteps"] + 1):
            state = fixture(mode, step); offsets = layout(state)
            input_path = folder / f"{mode}.s{step}.input.bin"
            read_record(input_path, state, step, 0)
            if previous is None: initial_flux(input_path, state, offsets)
            else: same_range(previous, input_path, offsets["flux"], 8 * 8 * state["nun"] * state["ng"])
            if case["negative"]:
                source_and_output(input_path, [input_path], state, offsets, negative=True)
                continue
            reference = folder / f"{mode}.s{step}.reference.bin"
            candidate = folder / f"{mode}.s{step}.candidate.bin"
            for path, who in ((reference, 1), (candidate, 2)): read_record(path, state, step, who)
            same_range(reference, candidate, 144, offsets["size"] - 144)
            for path in (reference, candidate):
                for plane in range(1, 9):
                    if plane != 7:
                        same_range(input_path, path, offsets["flux"] + (plane - 1) * state["nun"] * state["ng"] * 8,
                                   state["nun"] * state["ng"] * 8)
                    else:
                        for group in range(1, state["ng"] + 1):
                            if group not in state["active"]:
                                same_range(input_path, path, offsets["flux"] + (6 * state["ng"] + group - 1) * state["nun"] * 8,
                                           state["nun"] * 8)
            compared_scalars += source_and_output(input_path, [input_path, reference, candidate], state, offsets)
            previous = candidate; steps += 1; observers += 2 * int(bool(state["active"]))
            direct_steps += int(state["route"] == 1); fallback_steps += int(state["route"] == 2); empty_steps += int(state["route"] == 0)
            wanted_rows.append({"schema": "AXMAT_FLUSP64_WINDOW_WRAPPER_OBSERVER_CONTROL_V1", "case_id": state["id"],
                                "step": step, "expected_route": state["route"], "bitwise_passed": True, "solver_math_credit": False})
        require(rows == wanted_rows, "complete manifest must match all actual raw repeated steps")
        raw = {x["name"]: pin(folder / x["name"]) for x in case["raw_files"]}
        all_raw.update({mode + "/" + name: value for name, value in raw.items()})
        cases.append({"name": mode, "status": "EXPECTED_REJECTION" if case["negative"] else "PASS",
                      "actual_returncode": watch["returncode"], "raw_files": raw,
                      "actual_log": pin(folder / "execute.log"), "actual_watchdog": pin(folder / "execute.watchdog.json"),
                      "actual_manifest": pin(folder / "wrapper_manifest.jsonl")})
    require(steps == 22 and observers == 34 and len(all_raw) == 70
            and sum(v["bytes"] for v in all_raw.values()) == 288241824, "all actual wrapper steps, observer calls and bytes required")
    require(identity_snapshot(controls_root) == identities_before, "whole raw namespace changed during audit")
    return {"schema": "AXMAT_FLUSP64_WINDOW_COMPLETE_RAW_OBSERVER_CONTROLS_AUDIT_V13", "status": "PASS",
            "counts": {"positive_cases": 10, "expected_guard_rejection_cases": 4, "positive_steps": steps,
                       "reference_wrapper_calls": 24, "candidate_wrapper_calls": 24, "wrapper_calls_total": 48,
                       "observer_calls_total": observers, "direct_candidate_steps": direct_steps,
                       "sparse_fallback_steps": fallback_steps, "empty_steps": empty_steps,
                       "raw_file_count": len(all_raw), "raw_bytes": sum(v["bytes"] for v in all_raw.values()),
                       "independently_verified_active_output_scalars": compared_scalars},
            "cases": cases, "all_raw_files": all_raw, "complete_raw_scope_verified": True,
            "all_successful_caller_bits_equal_to_original": True, "all_sources_independently_reconstructed": True,
            "actual_contiguous_alias_and_sparse_nonalias_verified": True, "all_other_caller_planes_and_inactive_output_unchanged": True,
            "repeated_calls_and_active_set_transition_verified": True,
            "raw_identity_before_after_equal": True, "raw_identity_snapshot": identities_before,
            "solver_math_credit": False,
            "real_SPOT_receiver_calls_in_this_observer_executable": 0, "native_RSS_verified": False,
            "AAA_accuracy_qualified": False, "ABA_admitted": False}

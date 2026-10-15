#!/usr/bin/env python3
"""Summarize explicitly selected completed D4 maps; never launch a solver.

Consumed files are checked against their existing manifests. This report does
not replay the full provenance chain or replace the independent acceptance tools.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def decode(raw: bytes):
    def bad(value):
        raise ValueError(f"nonfinite JSON constant: {value}")
    return json.loads(raw, parse_constant=bad)


def manifest_entries(inventory: bytes) -> dict[str, str]:
    entries = {}
    for line in inventory.decode().splitlines():
        checksum, relative = line.split(maxsplit=1)
        relative = relative.removeprefix("*")
        if relative in entries:
            raise ValueError(f"duplicate manifest entry: {relative}")
        entries[relative] = checksum
    return entries


def consumed(directory: Path, name: str, evidence: dict,
             manifest: str = "result.sha256") -> bytes:
    inventory = (directory / manifest).read_bytes()
    entries = manifest_entries(inventory)
    raw = (directory / name).read_bytes()
    if entries.get(name) != digest(raw):
        raise ValueError(f"consumed file absent from manifest or changed: {directory / name}")
    evidence[str(directory / manifest)] = digest(inventory)
    evidence[str(directory / name)] = digest(raw)
    return raw


def number(value, positive=False) -> float:
    value = float(value)
    if not math.isfinite(value) or (value <= 0 if positive else value < 0):
        raise ValueError("invalid numeric evidence")
    return value


def pin_differences(raw: bytes, ce: dict) -> tuple[float, float]:
    target = {(b["floor"], b["pin_index"]): number(b["global_fraction"], True)
              for b in ce["bins"]}
    actual = {}
    for row in csv.DictReader(io.StringIO(raw.decode())):
        key = int(row["floor"]), int(row["pin_index"])
        if key in actual:
            raise ValueError("duplicate pin/zone")
        actual[key] = number(row["global_fraction"])
    if len(target) != len(ce["bins"]) or set(actual) != set(target):
        raise ValueError("pin/zone coverage mismatch")
    differences = [(actual[k] - target[k]) / target[k] for k in sorted(target)]
    return 100 * max(map(abs, differences)), 100 * math.sqrt(
        math.fsum(x*x for x in differences) / len(differences))


def cpu_time(raw: bytes) -> float:
    values = re.findall(rb"cle2000_c: cpu time=\s*([0-9.]+) second", raw)
    if len(values) != 1:
        raise ValueError("expected exactly one completed CPU timing")
    return number(values[0])


def summarize(config: dict, artifacts: Path) -> dict:
    evidence, rows = {}, []
    ce_raw = consumed(artifacts / config["ce"], "reference_result.json",
                      evidence, "result_receipt.sha256")
    ce = decode(ce_raw)
    kce = number(ce["keff"], True)
    sigma = 1e5 * number(ce["keff_standard_deviation"]) / kce**2
    for expected, entry in enumerate(config["maps"], 1):
        work, review = (artifacts / entry[key] for key in ("work", "review"))
        reviewed = decode(consumed(review, "review.json", evidence))
        if (reviewed["closed_epoch"], reviewed["numerical_cells"], reviewed["physical_zones"]) != (expected, 12, 3):
            raise ValueError("report requires an ordered, completed 12-cell D4 prefix")
        if reviewed.get("artifact_independent_review", reviewed.get("independent_review")) != "PASS":
            raise ValueError("missing completed independent review")
        identity = digest((work / "result.sha256").read_bytes())
        if identity != reviewed["result_manifest_sha256"]:
            raise ValueError("map and review identities differ")
        k = number(reviewed["k64"], True)
        leakage = leakage_difference = None
        if "current" in entry:
            currents = decode(consumed(artifacts / entry["current"], "summary.json", evidence))
            if identity != currents["work_result_manifest_sha256"] or currents["same_state_k64"] != k:
                raise ValueError("current diagnostic belongs to a different state")
            leakage = number(currents["source_normalized_net_leakage_kL_over_F"])
            leakage_difference = 100*(leakage-number(currents["ce_source_normalized_leakage"]))
        gate = consumed(work, "gate.log", evidence).decode()
        defects = {}
        for label, key in (("RRHO", "Rrho"), ("RLEAK", "Rleak"), ("RA", "Ra")):
            found = re.findall(rf"^SPOT-GATE {label}\s+(\S+)", gate, re.MULTILINE)
            if len(found) != 1:
                raise ValueError("missing or repeated outer defect")
            value = number(found[0])
            if value != reviewed[key]:
                raise ValueError("review and original gate differ")
            defects[key] = value
        thresholds = re.findall(r"^SPOT-GATE THRESHOLD\s+(\S+)", gate, re.MULTILINE)
        if len(thresholds) != 1 or float(thresholds[0]) != 5e-7 or reviewed["gate_all_required"] != 5e-7:
            raise ValueError("unexpected outer threshold")
        classification = "VALID_MET" if max(defects.values()) <= 5e-7 else "VALID_NOT_MET"
        if reviewed["classification"] != classification or f"CLASSIFICATION={classification}" not in gate:
            raise ValueError("outer classification disagrees with numeric defects")
        # Saved receipts use absolute paths. Match the final directory/file pair
        # so a relocated artifact tree retains its explicit input identity.
        maxpin = rmspin = None
        if "pins" in entry:
            pins = artifacts / entry["pins"]
            pin_inputs = manifest_entries(consumed(pins, "inputs.sha256", evidence))
            for folder, filename, checksum in (
                    (work.name, "result.sha256", identity),
                    (Path(config["ce"]).name, "reference_result.json", digest(ce_raw))):
                selected = [value for path, value in pin_inputs.items()
                            if Path(path).parts[-2:] == (folder, filename)]
                if selected != [checksum]:
                    raise ValueError("pin diagnostic belongs to different map or CE inputs")
            maxpin, rmspin = pin_differences(consumed(pins, "pin_rates.csv", evidence), ce)
        radial = cpu_time(consumed(work, "radial.log", evidence))
        axial = cpu_time(consumed(work, "axial.log", evidence))
        rows.append({
            "map": expected, "classification": classification, "k64": k, **defects,
            "ce_reactivity_difference_pcm": 1e5 * (1/kce - 1/k),
            "last_map_reactivity_change_pcm": None if not rows else 1e5*(1/rows[-1]["k64"] - 1/k),
            "source_normalized_leakage": leakage,
            "ce_leakage_difference_percentage_points": leakage_difference,
            "maximum_relative_pin_fraction_difference_percent": maxpin,
            "rms_relative_pin_fraction_difference_percent": rmspin,
            "radial_cpu_seconds": radial, "axial_cpu_seconds": axial,
            "elapsed_seconds": number(reviewed["elapsed_seconds"], True),
        })
    if not rows:
        raise ValueError("no completed maps selected")
    return {"classification": "SAVED_EVIDENCE_DIAGNOSTIC_ONLY", "label": config["label"],
            "ce_k": kce, "ce_sigma_pcm": sigma, "existing_ce_budget_pcm": 500 + 3*sigma,
            "maps": rows, "consumed_sha256": evidence,
            "limits": "Checks consumed-file integrity, not full provenance or new acceptance. "
                      "Pin differences include CE noise; no covariance or shape PASS. "
                      "CPU and wall time are different quantities. No transport, fitting or extrapolation."}


def markdown(report: dict) -> str:
    rows = report["maps"]
    lines = ["# D4-A saved-evidence report", "", report["label"], "",
             "Generated from an explicitly selected completed prefix; this is a dated diagnostic,",
             "not live run status or final physical acceptance. No transport is performed.", "",
             f"CE k = {report['ce_k']:.12f}; sigma = {report['ce_sigma_pcm']:.5f} pcm;",
             f"existing k comparison budget = {report['existing_ce_budget_pcm']:.5f} pcm.", "",
             "The signed difference is 1e5 (1/k_CE - 1/k_SPOT); negative means SPOT is lower.", "",
             "| Map | Rrho | Rleak | Ra | CE difference (pcm) | Leakage excess (percentage points) | Pin max / RMS (%) | Wall (h) |",
             "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |"]
    for row in rows:
        leakage = row["ce_leakage_difference_percentage_points"]
        maximum, rms = (row["maximum_relative_pin_fraction_difference_percent"],
                        row["rms_relative_pin_fraction_difference_percent"])
        leakage_text = "not evaluated" if leakage is None else f"{leakage:.6f}"
        pin_text = "not evaluated" if maximum is None else f"{maximum:.5f} / {rms:.5f}"
        lines.append(f"| {row['map']} | {row['Rrho']:.5e} | {row['Rleak']:.5e} | {row['Ra']:.5e} | "
                     f"{row['ce_reactivity_difference_pcm']:.5f} | {leakage_text} | "
                     f"{pin_text} | {row['elapsed_seconds']/3600:.3f} |")
    last = rows[-1]
    lines += ["", f"Latest selected classification: **{last['classification']}**.",
              "All three outer defects must independently satisfy 5e-7.", "",
              f"Latest radial/axial CPU: **{last['radial_cpu_seconds']:.0f} / {last['axial_cpu_seconds']:.0f} seconds**.",
              f"Completed-prefix wall time: **{sum(r['elapsed_seconds'] for r in rows)/3600:.3f} hours**",
              "(excludes snapshot construction, bootstrap and earlier experiments)."]
    if len(rows) > 1:
        lines += ["", f"The last map changes reactivity by {last['last_map_reactivity_change_pcm']:.5f} pcm,",
                  f"while its CE difference remains {last['ce_reactivity_difference_pcm']:.5f} pcm.",
                  "These are observed differences, not a bound on future iterations or an error decomposition."]
    lines += ["", "Optional leakage/pin diagnostics omitted from the input selection are marked not evaluated;",
              "they are never filled with zero or borrowed from another map. Declared inputs still must verify.",
              "Pin quantities are globally normalized nu-fission fractions, not thermal power.",
              "The maximum and unweighted RMS relative differences include CE sampling noise.",
              "No normalized-fraction covariance or shape-accuracy verdict is inferred.", "",
              "Regenerate with `make spot-evidence`; `--json` emits computed values and input hashes.",
              "The tool checks only files it consumes against existing manifests and binds map",
              "identity to the saved reviews. It does not rerun checkers or the full lineage audit.", "",
              "See the [experiment matrix](../../SPOT_doc/validation_plan.md),",
              "[current handoff](../iterative/d4a_final_validation_handoff.md), and",
              "[acceptance matrix](../iterative/d4a_corrected_acceptance_matrix.md).", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=ROOT / "validation/artifacts")
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("d4a_evidence_inputs.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = summarize(decode(args.inputs.read_bytes()), args.artifacts)
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
    else:
        print(markdown(report), end="")


if __name__ == "__main__":
    main()

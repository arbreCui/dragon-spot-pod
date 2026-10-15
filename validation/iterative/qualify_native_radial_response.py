#!/usr/bin/env python3
"""Qualify saved raw native MOC flight actions; no production solver mutation.

Requires NumPy. The two phases intentionally separate matrix extraction from
fresh native evaluation of the sources after boundary elimination.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

NR, NB = 8, 6
GROUPS = (1, 185, 370)
BOUNDARIES = (("vacuum", 0.0), ("half_albedo", 0.5), ("stored_white", 1.0))


def save_json(path, value):
    with Path(path).open("x") as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write("\n")


def relative(actual, expected):
    return float(np.linalg.norm(actual - expected, ord=np.inf) /
                 max(np.linalg.norm(expected, ord=np.inf), np.finfo(float).tiny))


def weighted_relative(actual, expected, weights):
    return float(np.sqrt(np.dot(weights, (actual - expected)**2) /
                         np.dot(weights, expected**2)))


def close_boundary(t, boundary, nr):
    """Map volume source to scalar flux and outgoing current, jin=B*jout.

    Multiplication order matters for nonuniform albedo/return permutations.
    """
    t_vv, t_vb = t[:nr, :nr], t[:nr, nr:]
    t_bv, t_bb = t[nr:, :nr], t[nr:, nr:]
    j = np.linalg.solve(np.eye(len(boundary)) - t_bb @ boundary, t_bv)
    r = t_vv + t_vb @ boundary @ j
    return r, j


def current_balance(source, response, weights, total, nr):
    q, incoming = source[:nr], source[nr:]
    phi, outgoing = response[:nr], response[nr:]
    v, surface = weights[:nr], weights[nr:]
    volume_source = float(v @ q)
    inflow, outflow = float(surface @ incoming), float(surface @ outgoing)
    collision = float((v * total) @ phi)
    defect = volume_source + inflow - collision - outflow
    source_norm = float(v @ abs(q))
    norm = source_norm + float(surface @ abs(incoming))
    return {"volume_source": volume_source, "incoming_current": inflow,
            "outgoing_current": outflow, "net_outflow": outflow - inflow,
            "total_collision": collision, "signed_defect": defect,
            "relative_to_all_inflow": abs(defect) / max(norm, np.finfo(float).tiny),
            "relative_to_volume_source": (abs(defect) / source_norm if source_norm else None)}


def load_runs(path):
    runs = {}
    with Path(path).open() as f:
        for row in csv.DictReader(f):
            key = (int(row["group"]), int(row["probe"]))
            runs.setdefault(key, []).append(row)
    result = {}
    for key, rows in runs.items():
        assert [int(r["slot"]) for r in rows] == list(range(1, NR + NB + 1))
        s = np.array([float(r["source"]) for r in rows])
        y = np.array([float(r["response"]) for r in rows])
        assert np.isfinite(s).all() and np.isfinite(y).all()
        result[key] = (s, y)
    return result


def load_metadata(path):
    grouped = {}
    with Path(path).open() as f:
        for row in csv.DictReader(f):
            g, slot = int(row["group"]), int(row["slot"])
            old = grouped.setdefault(g, {}).setdefault(slot, row)
            assert row == old, "metadata changed between flights"
    result = {}
    for g, slots in grouped.items():
        assert sorted(slots) == list(range(1, NR + NB + 1))
        result[g] = {name: np.array([float(slots[i][name]) for i in sorted(slots)])
                     for name in ("key", "zone", "weight", "total", "stored_self_scatter", "albedo", "return_index")}
    return result


def prescribed_sources(weights):
    # Fixed analytic patterns, not fitted to flight outputs or an eigenvector.
    patterns = {
        "uniform_anchor": np.ones(NR),
        "positive_ramp": np.arange(1, NR + 1, dtype=float),
        "first_region": np.eye(NR)[0],
        "last_region": np.eye(NR)[-1],
        "signed_perturbation": (-1.0)**np.arange(NR) * np.arange(1, NR + 1),
    }
    return {name: q / (weights @ abs(q)) for name, q in patterns.items()}


def prepare(artifact):
    a = Path(artifact)
    runs = load_runs(a / "runs/flight.csv")
    meta = load_metadata(a / "runs/metadata.csv")
    plan = json.loads((a / "plan.json").read_text())
    result = {"scope": plan["scope"], "groups": [], "closure_cases": [], "checks": {}}
    fixtures = []
    for g in GROUPS:
        cases = [v for (group, _), v in runs.items() if group == g]
        assert len(cases) == 18
        source, response = (np.column_stack([c[i] for c in cases]) for i in (0, 1))
        np.testing.assert_array_equal(source[:, :NR + NB], np.eye(NR + NB))
        t = response[:, :NR + NB]
        m = meta[g]; weights = m["weight"]; v = weights[:NR]; total = m["total"][:NR]
        linearity = [relative(t @ source[:, i], response[:, i]) for i in range(NR + NB, 18)]
        balances = [current_balance(s, y, weights, total, NR) for s, y in cases]
        group = {"group": g, "metadata": {k: x.tolist() for k, x in m.items()},
                 "flight_matrix": t.tolist(), "independent_linearity_relative": linearity,
                 "raw_flight_balances": balances,
                 "max_raw_balance_relative": max(b["relative_to_all_inflow"] for b in balances)}
        result["groups"].append(group)
        permutation = np.eye(NB)[m["return_index"][NR:].astype(int) - 1]
        patterns = prescribed_sources(v)
        for name, scale in BOUNDARIES:
            b = np.diag(scale * m["albedo"][NR:]) @ permutation
            r, j = close_boundary(t, b, NR)
            h = np.linalg.solve(r, np.eye(NR)); c = h - np.diag(total)
            anchor = r @ patterns["uniform_anchor"]
            diagonal = patterns["uniform_anchor"] / anchor
            # H maps arbitrary scalar fields to source; J H maps them to outgoing current.
            boundary_row = weights[NR:] @ (np.eye(NB) - b) @ j @ h
            conservation_row = v @ c - boundary_row
            row_scale = v @ abs(h) + v * abs(total) + abs(boundary_row)
            wc = v[:, None] * c
            wr = v[:, None] * r
            entry = {"group": g, "boundary": name, "boundary_matrix": b.tolist(),
                     "scalar_response": r.tolist(), "outgoing_response": j.tolist(),
                     "loss_operator": h.tolist(), "radial_operator": c.tolist(),
                     "condition_scalar_response": float(np.linalg.cond(r)),
                     "condition_boundary_solve": float(np.linalg.cond(np.eye(NB) - t[NR:, NR:] @ b)),
                     "boundary_row": boundary_row.tolist(), "weighted_balance_row_defect": conservation_row.tolist(),
                     "operator_balance_scaled_max": float(max(abs(conservation_row) / row_scale)),
                     "weighted_reciprocity_relative": relative(wr, wr.T),
                     "constant_field_radial_action": (c @ np.ones(NR)).tolist(),
                     "positive_radial_offdiagonal_count": int(np.sum((c > 0) & ~np.eye(NR, dtype=bool))),
                     "weighted_radial_symmetry_relative": relative(wc, wc.T),
                     "anchor_diagonal": diagonal.tolist(), "source_cases": []}
            for label, q in patterns.items():
                phi = r @ q; outgoing = j @ q; incoming = b @ outgoing
                full_source = np.r_[q, incoming]; expected = np.r_[phi, outgoing]
                diagonal_phi = q / diagonal
                record = {"source_name": label, "probe": len(fixtures) + 1,
                          "source": q.tolist(), "expected_response": expected.tolist(),
                          "minimum_scalar_flux": float(min(phi)), "minimum_outgoing": float(min(outgoing)),
                          "diagonal_flux_relative": weighted_relative(diagonal_phi, phi, v),
                          "diagonal_true_operator_residual": relative(h @ diagonal_phi, q),
                          "balance": current_balance(full_source, expected, weights, total, NR)}
                entry["source_cases"].append(record)
                fixtures.append((g, full_source))
            result["closure_cases"].append(entry)
    result["checks"]["independent_linearity"] = max(max(g["independent_linearity_relative"]) for g in result["groups"]) <= plan["thresholds"]["independent_linearity_relative"]
    result["checks"]["raw_current_balance"] = max(g["max_raw_balance_relative"] for g in result["groups"]) <= plan["thresholds"]["native_balance_relative"]
    save_json(a / "analysis/prepared.json", result)
    with (a / "runs/closed_sources.txt").open("x") as f:
        f.write(f"{len(fixtures)}\n")
        for g, s in fixtures:
            f.write(str(g) + " " + " ".join(format(float(x), ".17e") for x in s) + "\n")


def finish(artifact):
    a = Path(artifact)
    result = json.loads((a / "analysis/prepared.json").read_text())
    actual = load_runs(a / "runs/closed.csv")
    meta = load_metadata(a / "runs/closed_metadata.csv")
    original_meta = load_metadata(a / "runs/metadata.csv")
    for g in GROUPS:
        for name in meta[g]:
            np.testing.assert_array_equal(meta[g][name], original_meta[g][name])
    assert len(actual) == 45
    for case in result["closure_cases"]:
        g = case["group"]; b = np.array(case["boundary_matrix"])
        m = meta[g]
        for probe in case["source_cases"]:
            s, y = actual[(g, probe["probe"])]
            np.testing.assert_array_equal(s[:NR], probe["source"])
            expected = np.array(probe["expected_response"])
            np.testing.assert_allclose(s[NR:], b @ expected[NR:], rtol=0, atol=0)
            probe["fresh_native_response_relative"] = relative(y, expected)
            probe["fresh_boundary_closure_relative"] = float(np.max(abs(s[NR:] - b @ y[NR:])) / max(np.max(abs(y[NR:])), np.finfo(float).tiny))
            probe["fresh_native_balance"] = current_balance(s, y, m["weight"], m["total"][:NR], NR)
    cases = [p for c in result["closure_cases"] for p in c["source_cases"]]
    threshold = json.loads((a / "plan.json").read_text())["thresholds"]
    metrics = {
        "max_independent_linearity_relative": max(max(g["independent_linearity_relative"]) for g in result["groups"]),
        "max_raw_current_balance_relative": max(g["max_raw_balance_relative"] for g in result["groups"]),
        "max_closed_native_response_relative": max(p["fresh_native_response_relative"] for p in cases),
        "max_closed_boundary_closure_relative": max(p["fresh_boundary_closure_relative"] for p in cases),
        "max_closed_balance_relative_to_all_inflow": max(p["fresh_native_balance"]["relative_to_all_inflow"] for p in cases),
        "max_closed_balance_relative_to_volume_source": max(p["fresh_native_balance"]["relative_to_volume_source"] for p in cases),
        "max_operator_balance_scaled": max(c["operator_balance_scaled_max"] for c in result["closure_cases"]),
        "max_condition_scalar_response": max(c["condition_scalar_response"] for c in result["closure_cases"]),
        "minimum_positive_source_scalar_flux": min(p["minimum_scalar_flux"] for p in cases if p["source_name"] != "signed_perturbation"),
    }
    result["metrics"] = metrics
    result["checks"].update({
        "closed_native_action": metrics["max_closed_native_response_relative"] <= threshold["closed_native_residual_relative"],
        "closed_boundary_condition": metrics["max_closed_boundary_closure_relative"] <= threshold["closed_native_residual_relative"],
        "closed_current_balance": metrics["max_closed_balance_relative_to_all_inflow"] <= threshold["native_balance_relative"],
        "positive_source_response": metrics["minimum_positive_source_scalar_flux"] > 0,
    })
    result["classification"] = "NATIVE-FLIGHT-RESPONSE-QUALIFIED" if all(result["checks"].values()) else "NATIVE-FLIGHT-RESPONSE-NOT-QUALIFIED"
    save_json(a / "analysis/result.json", result)
    print(json.dumps({"classification": result["classification"], "checks": result["checks"], "metrics": metrics}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "finish"))
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else finish)(args.artifact)

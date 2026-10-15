#!/usr/bin/env python3
"""Same-operator full 370-group fixed-source/POD study on the historical pin.

NumPy only. This script does not run native code or mutate saved transport data.
Native source construction and fresh sweeps are separate recorded invocations.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np

from qualify_native_radial_response import close_boundary, load_runs, load_metadata, relative

NG, NR, NB = 370, 8, 6


def save_json(path, value):
    with Path(path).open("x") as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write("\n")


def load_data(path):
    with Path(path).open("rb") as f:
        def read(dtype, shape):
            n = int(np.prod(shape))
            x = np.fromfile(f, dtype=dtype, count=n)
            if x.size != n:
                raise ValueError("truncated native export")
            return x.reshape(shape, order="F")
        header = read("<i4", (6,))
        np.testing.assert_array_equal(header, [NR, NB, NG, NR, 0, 2])
        d = {}
        for key, shape in (("zone", (14,)), ("key", (14,)), ("return", (6,))):
            d[key] = read("<i4", shape)
        shapes = [("weights", (14,)), ("volume", (8,)), ("leak", (370,)),
                  ("total", (9, 370)), ("used", (9, 370)), ("physical", (9, 370)),
                  ("macro_total", (8, 370)), ("sigw", (8, 370)), ("sigs", (8, 370)),
                  ("scatter_packed", (370, 370, 8)), ("frozen", (14, 370))]
        for key, shape in shapes:
            d[key] = read("<f4", shape)
        if f.read():
            raise ValueError("trailing native export data")
    if any(not np.isfinite(v).all() for v in d.values()):
        raise ValueError("nonfinite data")
    np.testing.assert_array_equal(d["weights"][:NR], d["volume"])
    np.testing.assert_array_equal(d["used"][1:], d["physical"][1:] - d["leak"])
    d["v"] = d["volume"].astype(float)
    region = d["zone"][:NR] - 1
    d["total_r"] = d["total"][region + 1].T.astype(float)
    d["used_r"] = d["used"][region + 1].T.astype(float)
    d["physical_r"] = d["physical"][region + 1].T.astype(float)
    d["scatter"] = d["scatter_packed"][:, :, region].astype(float)
    for g in range(NG):
        d["scatter"][g, g] = d["used_r"][g]
    d["fixed"] = d["frozen"][d["key"][:NR] - 1].T.astype(float)
    d["fixed"] /= np.sum(d["v"] * d["fixed"])
    return d


def scatter_action(scatter, phi):
    return np.einsum("ghi,hi->gi", scatter, phi, optimize=True)


def full_operator(h, scatter, leakage=0.):
    ng, nr = h.shape[:2]
    a = np.zeros((ng, nr, ng, nr))
    for i in range(nr):
        a[:, i, :, i] = -scatter[:, :, i]
    for g in range(ng):
        a[g, :, g, :] += h[g] + leakage * np.eye(nr)
    return a.reshape(ng * nr, ng * nr)


def projected_operator(h, scatter, v, b, leakage=0.):
    ng, nr, rank = b.shape
    ar = -np.einsum("gia,ghi,hib,i->gahb", b, scatter, b, v, optimize=True)
    for g in range(ng):
        ar[g, :, g, :] += b[g].T @ (v[:, None] * (h[g] + leakage * np.eye(nr))) @ b[g]
    return ar.reshape(ng * rank, ng * rank)


def project_source(v, b, q):
    return np.einsum("gia,i,gi->ga", b, v, q).reshape(-1)


def lift(b, modal):
    return np.einsum("gia,ga->gi", b, modal.reshape(b.shape[0], b.shape[2]))


def source_normalize(q, v):
    return q / np.sum(abs(q) * v)


def operator_action(h, scatter, phi, leakage):
    return np.einsum("gij,gj->gi", h, phi) - scatter_action(scatter, phi) + leakage * phi


def diagnostics(d, h, phi, q, leakage, reference=None, basis=None):
    v = d["v"]
    action = operator_action(h, d["scatter"], phi, leakage)
    residual = action - q
    denom = max(float(np.max(abs(q))), np.finfo(float).tiny)
    weighted_residual = float(np.sum(v * residual))
    # Stored self already includes the legacy leakage reduction.
    physical_ledger = d["total_r"] * phi - scatter_action(d["scatter"], phi) + leakage * phi - q
    raw_balance = float(np.sum(v * physical_ledger))
    radial = np.einsum("gij,gj->gi", h, phi) - d["total_r"] * phi
    radial_balance = float(np.sum(v * radial))
    out = {"full_residual_relative": float(np.max(abs(residual)) / denom),
           "weighted_operator_residual": weighted_residual,
           "raw_collision_scattering_leakage_balance": raw_balance,
           "native_radial_balance_defect": radial_balance,
           "balance_identity_error": raw_balance - (weighted_residual - radial_balance),
           "minimum_flux": float(phi.min()), "negative_flux_count": int(np.sum(phi < 0)),
           "zero_flux_count": int(np.sum(phi == 0))}
    if reference is not None:
        out["relative_flux_l2"] = float(np.sqrt(np.sum(v * (phi - reference)**2) / np.sum(v * reference**2)))
    if basis is not None:
        projected = project_source(v, basis, residual)
        projected_q = project_source(v, basis, q)
        out["projected_residual_relative"] = float(np.max(abs(projected)) / np.max(abs(projected_q)))
    return out


def extract_flights(a, d):
    t = np.empty((NG, NR + NB, NR + NB))
    r = np.empty((NG, NR, NR)); j = np.empty((NG, NB, NR)); h = np.empty_like(r)
    seen = set()
    for path in sorted((a / "runs").glob("flight_[0-9]*_[0-9]*.csv")):
        if path.name.endswith("_meta.csv"):
            continue
        runs = load_runs(path); meta = load_metadata(path.with_name(path.stem + "_meta.csv"))
        for group, m in meta.items():
            if group in seen or group < 1 or group > NG:
                raise ValueError("duplicate/out-of-range flight group")
            seen.add(group)
            g = group - 1
            values = [p for (gg, _), p in runs.items() if gg == group]
            s, y = [np.column_stack([p[k] for p in values]) for k in (0, 1)]
            np.testing.assert_array_equal(s, np.eye(14))
            np.testing.assert_array_equal(m["weight"], d["weights"])
            np.testing.assert_array_equal(m["total"][:NR], d["total_r"][g])
            np.testing.assert_array_equal(m["stored_self_scatter"][:NR], d["used_r"][g])
            np.testing.assert_array_equal(m["albedo"][NR:], np.ones(NB))
            np.testing.assert_array_equal(m["return_index"][NR:], np.arange(1, NB + 1))
            t[g] = y
            r[g], j[g] = close_boundary(y, np.eye(NB), NR)
            h[g] = np.linalg.solve(r[g], np.eye(NR))
    if seen != set(range(1, NG + 1)):
        raise ValueError("incomplete group coverage")
    old = json.loads((a / "inputs/previous_flight_result.json").read_text())
    for group in old["groups"]:
        np.testing.assert_array_equal(t[group["group"] - 1], group["flight_matrix"])
    return t, r, j, h


def prepare(artifact):
    a = Path(artifact); d = load_data(a / "analysis/data.bin")
    t, r, j, h = extract_flights(a, d)
    audit = {"all_used_self_matches_binary32_physical_minus_saved_leak": True,
             "saved_leak_min": float(d["leak"].min()), "saved_leak_max": float(d["leak"].max()),
             "max_effective_leak_rounding_difference": float(np.max(abs(d["physical_r"] - d["used_r"] - d["leak"][:, None]))),
             "negative_packed_entries": int(np.sum(d["scatter_packed"] < 0)),
             "negative_offgroup_entries": int(np.sum(d["scatter"] < 0) - np.sum(d["used_r"] < 0)),
             "negative_used_self_entries": int(np.sum(d["used_r"] < 0)),
             "max_total_vs_macro_difference": float(np.max(abs(d["total"][1:].astype(float) - d["macro_total"]))),
             "max_physical_self_vs_macro_difference": float(np.max(abs(d["physical"][1:].astype(float) - d["sigw"]))),
             "max_radial_condition": float(max(np.linalg.cond(x) for x in r)),
             "previous_three_groups_bitwise_recovered": True}
    save_json(a / "analysis/audit.json", audit)
    # Native callbacks get independent analytic fields before the solved states.
    sources = []; names = []
    for signed in (False, True):
        field = .2 + np.arange(1, NG + 1)[:, None] / (NG + 1) + np.arange(1, 15)[None, :] / 15
        if signed:
            field *= (-1.)**np.arange(14)
        sources.append((np.full(NG, .03 if not signed else .07), d["fixed"], field))
        names.append("analytic_signed" if signed else "analytic_positive")
    qset = [d["fixed"], source_normalize(np.exp(-np.arange(NG)[:, None] / 53.) * np.arange(1, NR + 1)[None, :], d["v"])]
    references = []; fluxes = []
    for lam in (0., .05):
        mat = full_operator(h, d["scatter"], lam)
        sol = np.linalg.solve(mat, np.column_stack([q.ravel() for q in qset]))
        for i, q in enumerate(qset):
            phi = sol[:, i].reshape(NG, NR)
            label = f"extra_{lam:g}_" + ("archived" if i == 0 else "ramp")
            native_q = np.einsum("gij,gj->gi", h, phi)
            outgoing = np.einsum("gsi,gi->gs", j, native_q)
            fields = np.column_stack([phi, outgoing])
            sources.append((np.full(NG, lam), q, fields));names.append(label)
            references.append({"name": label, "extra_leakage": lam, "source_index": i,
                               **diagnostics(d, h, phi, q, lam)})
            fluxes.append(phi)
        print(f"full native operator references solved: extra leakage {lam:g}", flush=True)
    with (a / "runs/source_fields.bin").open("xb") as f:
        np.array([len(sources)], dtype="<i4").tofile(f)
        for lam, q, field in sources:
            for x in (lam, q, field):
                np.asarray(x, dtype="<f8").tofile(f)
    save_json(a / "analysis/references.json", {"cases": references, "source_field_names": names})
    np.savez_compressed(a / "analysis/operator_fields.npz", flight=t, response=r, outgoing=j, loss=h,
                        references=np.array(fluxes), sources=np.array(qset))
    print(json.dumps(audit, indent=2), flush=True)


def native_sources(artifact):
    a = Path(artifact);d = load_data(a / "analysis/data.bin")
    fields = []
    with (a / "runs/source_fields.bin").open("rb") as f:
        n = int(np.fromfile(f, "<i4", 1)[0])
        for _ in range(n):
            lam = np.fromfile(f, "<f8", NG)
            q = np.fromfile(f, "<f8", NG * NR).reshape(NG, NR)
            phi = np.fromfile(f, "<f8", NG * 14).reshape(NG, 14)
            fields.append((lam, q, phi))
        assert not f.read()
    outputs = []
    with (a / "runs/native_sources.bin").open("rb") as f:
        np.testing.assert_array_equal(np.fromfile(f, "<i4", 4), [n, NR, NB, NG])
        for _ in range(n):
            off = np.fromfile(f, "<f8", NG * NR).reshape(NG, NR)
            full = np.fromfile(f, "<f8", NG * 14).reshape(NG, 14)
            outputs.append((off, full))
        assert not f.read()
    metrics = []
    for i, ((lam, q, phi), (off, full)) in enumerate(zip(fields, outputs)):
        pyoff = q + scatter_action(d["scatter"], phi[:, :NR]) - d["used_r"] * phi[:, :NR]
        pyfull = np.column_stack([pyoff + (d["used_r"] - lam[:, None]) * phi[:, :NR], phi[:, NR:]])
        metrics.append({"case": i, "offgroup_source_relative": relative(pyoff, off),
                        "whole_source_relative": relative(pyfull, full)})
        # Only the freshly evaluated native source enters the follow-up sweep.
        path = a / "runs" / f"check_source_{i}.txt"
        with path.open("x") as f:
            f.write(f"{NG}\n")
            for g, row in enumerate(full, 1):
                f.write(str(g) + " " + " ".join(format(float(x), ".17e") for x in row) + "\n")
    save_json(a / "analysis/source_checks.json", metrics)
    print(json.dumps(metrics, indent=2))


def bases(snapshots, v):
    # snapshots: sample, group, region; normalization is global per sample.
    plain = []; enriched = []; spectra = []
    root = np.sqrt(v); constant = root / np.linalg.norm(root)
    for g in range(snapshots.shape[1]):
        x = root[:, None] * snapshots[:, g, :].T
        u, s, _ = np.linalg.svd(x, full_matrices=True)
        residual = x - constant[:, None] * (constant @ x)
        ur, sr, _ = np.linalg.svd(residual, full_matrices=True)
        qe, _ = np.linalg.qr(np.column_stack([constant, ur[:, :len(v)-1]]))
        plain.append(u / root[:, None]);enriched.append(qe / root[:, None])
        spectra.append({"plain": s.tolist(), "off_constant": sr.tolist()})
    return np.array(plain), np.array(enriched), spectra


def projection(artifact):
    a = Path(artifact);d = load_data(a / "analysis/data.bin")
    fields = np.load(a / "analysis/operator_fields.npz");h = fields["loss"]
    refs = json.loads((a / "analysis/references.json").read_text())["cases"]
    spectrum = np.sum(d["fixed"] * d["v"], axis=1);spectrum /= spectrum.sum()
    training_q = np.zeros((NG, NR, NR))
    for i in range(NR):
        training_q[:, i, i] = spectrum / d["v"][i]
    snapshots = []
    for lam in (.01, .1, 1.):
        matrix = full_operator(h, d["scatter"], lam)
        sol = np.linalg.solve(matrix, training_q.reshape(NG * NR, NR))
        for i in range(NR):
            phi = sol[:, i].reshape(NG, NR)
            snapshots.append(phi / np.sqrt(np.sum(d["v"] * phi**2)))
        print(f"training snapshots solved: extra leakage {lam:g}", flush=True)
    snapshots = np.array(snapshots)
    plain, enriched, spectra = bases(snapshots, d["v"])
    rows = []; coordinate_checks = []; reduced_fields = []
    for family, all_basis in (("plain", plain), ("constant_enriched", enriched)):
        for rank in range(1, NR + 1):
            b = all_basis[:, :, :rank]
            constant_error = max(float(np.linalg.norm(np.ones(NR) - bg @ np.linalg.solve(bg.T @ (d["v"][:, None] * bg), bg.T @ d["v"]))) for bg in b)
            ar0 = projected_operator(h, d["scatter"], d["v"], b)
            gram = np.array([bg.T @ (d["v"][:, None] * bg) for bg in b])
            for lam in (0., .05):
                ar = ar0.copy().reshape(NG, rank, NG, rank)
                for g in range(NG):
                    ar[g, :, g, :] += lam * gram[g]
                ar = ar.reshape(NG * rank, NG * rank)
                rhs = np.column_stack([project_source(d["v"], b, q) for q in fields["sources"]])
                modal = np.linalg.solve(ar, rhs)
                for source_index in range(2):
                    index = source_index + (0 if lam == 0 else 2)
                    q = fields["sources"][source_index];phi = lift(b, modal[:, source_index])
                    rows.append({"family": family, "rank": rank, "reference": refs[index]["name"],
                                 "constant_span_error": constant_error,
                                 **diagnostics(d, h, phi, q, lam, fields["references"][index], b)})
                    reduced_fields.append(phi)
                # A congruence solve in oblique coordinates checks Gram handling.
                if rank in (3, 8) and lam == 0:
                    change = np.eye(rank) + .2 * np.diag(np.ones(rank - 1), 1)
                    change[:, 0] *= 1.7
                    changed_basis = b @ change
                    changed_matrix = projected_operator(h, d["scatter"], d["v"], changed_basis)
                    changed_rhs = project_source(d["v"], changed_basis, fields["sources"][0])
                    changed_flux = lift(changed_basis, np.linalg.solve(changed_matrix, changed_rhs))
                    base_flux = lift(b, modal[:, 0])
                    coordinate_checks.append({"family": family, "rank": rank,
                        "relative_flux": float(np.sqrt(np.sum(d["v"] * (changed_flux - base_flux)**2) / np.sum(d["v"] * base_flux**2)))})
            print(f"fixed POD projection: {family} rank {rank} complete", flush=True)
    np.savez_compressed(a / "analysis/projection_fields.npz", snapshots=snapshots, plain_basis=plain,
                        enriched_basis=enriched, reduced_fields=np.array(reduced_fields))
    save_json(a / "analysis/projection.json", {"rows": rows, "coordinate_checks": coordinate_checks,
        "training_minimum_flux": float(snapshots.min()), "snapshot_spectra": spectra})


def finish(artifact):
    a = Path(artifact);d = load_data(a / "analysis/data.bin")
    f = np.load(a / "analysis/operator_fields.npz")
    refs = json.loads((a / "analysis/references.json").read_text())
    source_checks = json.loads((a / "analysis/source_checks.json").read_text())
    proj = json.loads((a / "analysis/projection.json").read_text())
    native = []
    for i, name in enumerate(refs["source_field_names"]):
        runs = load_runs(a / "runs" / f"check_flight_{i}.csv")
        assert len(runs) == NG
        source = np.array([x[0] for x in runs.values()]);out = np.array([x[1] for x in runs.values()])
        predicted = np.einsum("gij,gj->gi", f["flight"], source)
        record = {"name": name, "matrix_vs_fresh_native_relative": relative(predicted, out),
                  "max_group_relative": max(relative(predicted[g], out[g]) for g in range(NG))}
        if i >= 2:
            expected_phi = f["references"][i - 2]
            record["fixed_source_relative"] = relative(out[:, :NR], expected_phi)
            record["fixed_source_max_group_relative"] = max(relative(out[g, :NR], expected_phi[g]) for g in range(NG))
            record["boundary_return_relative"] = relative(out[:, NR:], source[:, NR:])
        native.append(record)
    thresholds = json.loads((a / "plan.json").read_text())["thresholds"]
    metrics = {
        "max_source_constructor_relative": max(max(x["offgroup_source_relative"], x["whole_source_relative"]) for x in source_checks),
        "max_reference_residual": max(x["full_residual_relative"] for x in refs["cases"]),
        "max_fresh_native_fixed_source_relative": max(x.get("fixed_source_relative", 0) for x in native),
        "max_fresh_native_fixed_source_group_relative": max(x.get("fixed_source_max_group_relative", 0) for x in native),
        "max_full_rank_flux_error": max(x["relative_flux_l2"] for x in proj["rows"] if x["rank"] == NR),
        "max_oblique_coordinate_flux_difference": max(x["relative_flux"] for x in proj["coordinate_checks"]),
        "max_projected_residual": max(x["projected_residual_relative"] for x in proj["rows"]),
        "max_constant_weighted_residual": max(abs(x["weighted_operator_residual"]) for x in proj["rows"] if x["family"] == "constant_enriched"),
        "minimum_reference_flux": min(x["minimum_flux"] for x in refs["cases"]),
        "minimum_reduced_flux": min(x["minimum_flux"] for x in proj["rows"]),
        "max_reference_raw_balance": max(abs(x["raw_collision_scattering_leakage_balance"]) for x in refs["cases"]),
        "max_enriched_raw_balance": max(abs(x["raw_collision_scattering_leakage_balance"]) for x in proj["rows"] if x["family"] == "constant_enriched"),
    }
    checks = {
        "source_construction": metrics["max_source_constructor_relative"] <= thresholds["source_constructor_relative"],
        "full_reference_residual": metrics["max_reference_residual"] <= thresholds["dense_solve_relative_residual"],
        "fresh_native_action": metrics["max_fresh_native_fixed_source_relative"] <= thresholds["fresh_native_fixed_source_relative"],
        "full_space_recovery": metrics["max_full_rank_flux_error"] <= thresholds["full_space_relative_flux"],
        "coordinate_invariance": metrics["max_oblique_coordinate_flux_difference"] <= thresholds["full_space_relative_flux"],
        "projected_residual": metrics["max_projected_residual"] <= thresholds["projected_relative_residual"],
        "constant_weighted_residual": metrics["max_constant_weighted_residual"] <= thresholds["constant_weighted_residual_relative"],
        "positive_full_reference": metrics["minimum_reference_flux"] > 0,
    }
    save_json(a / "analysis/result.json", {"metrics": metrics, "checks": checks, "native_replays": native,
        "references": refs["cases"], "projection": proj["rows"], "coordinate_checks": proj["coordinate_checks"],
        "classification": "SAME-OPERATOR-FIXED-SOURCE-QUALIFIED" if all(checks.values()) else "FIXED-SOURCE-DIAGNOSTIC-ONLY"})
    print(json.dumps({"checks": checks, "metrics": metrics}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "native_sources", "projection", "finish"))
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    globals()[args.phase](args.artifact)

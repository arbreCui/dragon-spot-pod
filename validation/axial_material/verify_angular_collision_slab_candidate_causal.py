"""Independent mathematical controls for the unqualified angular slab modules.

This file defines a future serial stage.  It does not run controls on import.
The expanded reference solves the SAME constant-subcell source discretization;
agreement is not native transport, continuous propagation, reaction-data,
scattering/fission, AAA, or ABA qualification.  Every returned numerical solve
is archived before its fields or residuals are judged.  Sparse matrices use
explicit CSR arrays, never object arrays or pickle.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True

import numpy as np
from scipy.sparse import issparse

import angular_collision_slab_candidate as candidate
from angular_collision_slab_expanded_reference_causal import solve_expanded


FIELD_LIMIT = 5e-12
ALGEBRAIC_LIMIT = 1e-10
WALL_LIMIT_SECONDS = 600
RSS_LIMIT_MIB = 512
ANALYTIC_DECIMAL_PRECISION = 1024
EXPECTED_CASE_PAIRS = 20
EXPECTED_NUMERICAL_SOLVES = 40
EXPECTED_NEGATIVE_CONTROLS = 11

FIELDS = (
    "fine_angular_means", "fine_angular_faces", "coarse_angular_means",
    "coarse_angular_faces", "fine_scalar_mean", "coarse_scalar_mean",
    "fine_signed_jz", "coarse_signed_jz", "fine_signed_face_jz",
    "coarse_signed_face_jz", "bottom_top_outgoing_angular_flux",
    "bottom_top_angular_escape_current", "bottom_top_escape_current",
    "vacuum_incoming_angular_flux", "effective_algebraic_sources",
    "algebraic_birth", "algebraic_collision",
)
POSITIVE_FIELDS = (
    "fine_angular_means", "fine_angular_faces", "coarse_angular_means",
    "coarse_angular_faces", "fine_scalar_mean", "coarse_scalar_mean",
    "bottom_top_outgoing_angular_flux", "bottom_top_angular_escape_current",
    "bottom_top_escape_current", "effective_algebraic_sources",
)
ACTION_DIAGNOSTICS = (
    "matrix_residual_relative", "characteristic_face_relative",
    "characteristic_mean_relative",
)
ALGEBRAIC_DIAGNOSTICS = (
    "full_directional_cell_equation_relative", "raw_algebraic_balance_relative",
)


def _write_json(path, value):
    with Path(path).open("x") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def _digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def _archive(folder, stem, value):
    """Preserve all returned arrays, sparse systems, and textual witnesses."""
    arrays, metadata = {}, {}

    def collect(prefix, item):
        if issparse(item):
            matrix = item.tocsr(copy=True)
            arrays[prefix + "__csr_data"] = matrix.data
            arrays[prefix + "__csr_indices"] = matrix.indices
            arrays[prefix + "__csr_indptr"] = matrix.indptr
            arrays[prefix + "__csr_shape"] = np.asarray(matrix.shape, dtype=np.int64)
            metadata[prefix] = {"storage": "explicit CSR data/indices/indptr/shape"}
        elif isinstance(item, np.ndarray):
            if item.dtype.hasobject:
                raise ValueError("object arrays cannot enter scientific archives: " + prefix)
            arrays[prefix] = item
        elif isinstance(item, dict):
            for name, child in item.items():
                collect(prefix + "__" + str(name) if prefix else str(name), child)
        elif isinstance(item, (tuple, list)):
            if all(isinstance(child, (str, int, float, bool, type(None))) for child in item):
                metadata[prefix] = list(item)
            else:
                metadata[prefix + "__sequence_length"] = len(item)
                for index, child in enumerate(item):
                    collect(prefix + "__" + str(index), child)
        elif isinstance(item, (np.generic, int, float, bool)):
            arrays[prefix] = np.asarray(item)
        elif isinstance(item, (str, type(None))):
            metadata[prefix] = item
        elif isinstance(item, Decimal):
            metadata[prefix] = str(item)
        else:
            raise TypeError("unsupported raw scientific value: " + prefix + ": " + repr(type(item)))

    collect("", value)
    path = folder / (stem + ".npz")
    with path.open("xb") as handle:
        np.savez_compressed(handle, **arrays)
    text_path = folder / (stem + ".metadata.json")
    _write_json(text_path, metadata)
    return dict(
        arrays_file=path.name, arrays_sha256=_digest(path), arrays_bytes=path.stat().st_size,
        metadata_file=text_path.name, metadata_sha256=_digest(text_path),
        numeric_arrays=len(arrays), object_arrays=False,
    )


def _source_family(mu):
    """Construct the 32 units and six specified holdouts independently."""
    sources = np.zeros((8, 4, 38))
    labels = []
    for angle in range(8):
        for layer in range(4):
            sources[angle, layer, 4 * angle + layer] = 1.0
            labels.append(f"angle_{angle + 1}_layer_{layer + 1}")
    for angle in range(8):
        for layer in range(4):
            z = (layer + 0.5) / 4
            m = float(mu[angle])
            sources[angle, layer, 32:] = [
                1.0, 1 + 0.5 * m, 1 - 0.5 * m, 1 + z, 2 - z,
                (1 + 0.25 * m + 0.1 * (3 * (m * m) - 1) / 2) * (1 + 0.5 * z),
            ]
    labels += ["uniform", "positive_odd_plus", "positive_odd_minus",
               "axial_ramp_plus", "axial_ramp_minus", "positive_mixed"]
    generated = candidate.source_family(mu)
    if (generated["unit_coordinates"] != 32 or tuple(labels) != generated["labels"]
            or not np.array_equal(sources, generated["sources"])
            or not np.array_equal(sources.reshape(32, 38)[:, 32:],
                                  generated["holdout_unit_coefficients"])):
        raise ValueError("independently constructed source coordinates differ")
    if not np.isfinite(sources).all() or np.any(sources < 0):
        raise ValueError("all fixed source combinations must be finite and nonnegative")
    return sources, labels


def _array_error(actual, expected, label):
    actual, expected = np.asarray(actual), np.asarray(expected)
    if actual.shape != expected.shape or not np.isfinite(actual).all() or not np.isfinite(expected).all():
        raise ValueError("finite equal-shaped fields required: " + label)
    if actual.ndim == 0:
        actual, expected = actual.reshape(1), expected.reshape(1)
    axes = tuple(range(expected.ndim - 1))
    scale = np.max(abs(expected), axis=axes) if axes else abs(expected)
    defect = abs(actual - expected)
    relative = np.divide(defect, scale, out=np.zeros_like(defect, dtype=float), where=scale > 0)
    if np.any((scale == 0) & (defect != 0)):
        raise ValueError("a zero reference coordinate must stay exactly zero: " + label)
    value = float(np.max(relative))
    if not np.isfinite(value) or value >= FIELD_LIMIT:
        raise ValueError("unchanged field/action gate failed: " + label + ": " + repr(value))
    return value


def _compare(actual, expected, label):
    return {name: _array_error(actual[name], expected[name], label + "/" + name)
            for name in FIELDS}


def _audit_result(result, inputs, role):
    source = inputs["sources"]
    n, k = 4 * inputs["subdivisions"], source.shape[-1]
    shapes = {
        "fine_angular_means": (8, n, k), "fine_angular_faces": (8, n + 1, k),
        "coarse_angular_means": (8, 4, k), "coarse_angular_faces": (8, 5, k),
        "fine_scalar_mean": (n, k), "coarse_scalar_mean": (4, k),
        "fine_signed_jz": (n, k), "coarse_signed_jz": (4, k),
        "fine_signed_face_jz": (n + 1, k), "coarse_signed_face_jz": (5, k),
        "bottom_top_outgoing_angular_flux": (2, 8, k),
        "bottom_top_angular_escape_current": (2, 8, k),
        "bottom_top_escape_current": (2, k), "vacuum_incoming_angular_flux": (8, k),
        "effective_algebraic_sources": (8, n, k),
        "algebraic_birth": (k,), "algebraic_collision": (k,),
    }
    for name, shape in shapes.items():
        value = np.asarray(result[name])
        if value.shape != shape or not np.isfinite(value).all():
            raise ValueError("complete finite raw field required: " + role + "/" + name)
    if not np.array_equal(result["external_sources"], source):
        raise ValueError("returned external source coordinates differ: " + role)
    if not np.array_equal(result["fine_external_sources"],
                          np.repeat(source, inputs["subdivisions"], axis=1)):
        raise ValueError("fine-source lift must repeat each declared coarse layer: " + role)
    if np.any(np.asarray(result["vacuum_incoming_angular_flux"]) != 0):
        raise ValueError("vacuum incoming fields must be exactly zero: " + role)
    minima = {}
    for name in POSITIVE_FIELDS:
        minimum = float(np.min(result[name]))
        minima[name] = minimum
        if minimum < 0:
            raise ValueError("positive-source response is negative: " + role + "/" + name)
    diagnostics = result["diagnostics"]
    for name, value in diagnostics.items():
        if not np.isfinite(value).all():
            raise ValueError("all diagnostics must be finite: " + role + "/" + name)
    checked = {}
    names = list(ACTION_DIAGNOSTICS)
    if "reconstructed_mean_relative" in diagnostics:
        names.append("reconstructed_mean_relative")
    for name in names + list(ALGEBRAIC_DIAGNOSTICS):
        value = float(np.max(diagnostics[name]))
        limit = ALGEBRAIC_LIMIT if name in ALGEBRAIC_DIAGNOSTICS else FIELD_LIMIT
        if value >= limit:
            raise ValueError("unchanged residual gate failed: " + role + "/" + name + ": " + repr(value))
        checked[name] = value
    if np.any(diagnostics["vacuum_incoming_absolute"] != 0):
        raise ValueError("vacuum diagnostic must be exactly zero: " + role)
    if not np.all(diagnostics["external_source_column_nonnegative"]):
        raise ValueError("this control family contains only positive external sources")
    if float(diagnostics["angular_weights_sum"]) != float(inputs["weights"].sum()):
        raise ValueError("angular weights were changed or rescaled: " + role)
    for name in ("AAA_accuracy_qualified", "ABA_admitted", "axial_propagation_qualified",
                 "scattering_fission_iteration_qualified", "physical_collision_balance_assessed"):
        if result.get(name) is not False:
            raise ValueError("mathematical controls cannot carry physics qualification: " + role + "/" + name)
    if role == "expanded":
        dimension = 8 * n + 8 * (n + 1)
        matrix, rhs, solution = (result["expanded_matrix"], result["expanded_rhs"],
                                 result["expanded_solution"])
        if (not issparse(matrix) or matrix.shape != (dimension, dimension)
                or rhs.shape != (dimension, k) or solution.shape != (dimension, k)
                or result["mean_unknowns"] != 8 * n or result["face_unknowns"] != 8 * (n + 1)):
            raise ValueError("expanded complete mean/face coordinate system required")
        if not np.isfinite(matrix.data).all() or not np.isfinite(rhs).all() or not np.isfinite(solution).all():
            raise ValueError("expanded raw system must be finite")
        recomputed = matrix @ solution - rhs
        checked["raw_expanded_residual_recomputed"] = _array_error(
            recomputed, result["raw_matrix_residual"], "expanded/raw residual preservation"
        )
    return dict(residual_maxima=checked, positive_field_minima=minima,
                vacuum_incoming_exact_zero=True, explicit_weights_unchanged=True)


def _normal_angles():
    # Fixed native-style input rule; no experiment/archive is read or selected.
    zmu = np.asarray([1.0172609090805054, 1.1754008531570435,
                      1.654481053352356, 3.5841732025146484])
    wzmu = np.asarray([0.35652974247932434, 0.26689332723617554,
                       0.13441134989261627, 0.028243202716112137])
    positive = np.sqrt(1 - 1 / zmu**2)
    mu = np.empty(8)
    mu[0::2], mu[1::2] = -positive, positive
    weights = np.repeat(wzmu * zmu / 2, 2)
    return mu, weights


def _coupled_matrix(weights):
    # Positive, weighted-conserving angular exchange plus prescribed loss.
    # This is an analytical fixture, never measured native collision data.
    loss = np.repeat(np.asarray([0.12, 0.18, 0.24, 0.30]), 2)
    rate = 0.16
    return np.diag(loss + rate * weights.sum()) - rate * np.ones((8, 1)) * weights[None, :]


def _analytic_decoupled(inputs):
    """Closed-form diagonal/void characteristic control at 1024 decimal digits.

    The precision resolves the thin fixture's SECOND-order exponential term
    near 1e-800, required by the two direct subtractions defining D when the
    optical length is near 1e-400.  It uses neither module's primitive helper,
    eliminated matrix, source sweep, or sparse equation assembly.
    """
    mu, weights, h = inputs["mu"], inputs["weights"], inputs["H"]
    if np.any(h - np.diag(np.diag(h)) != 0):
        raise ValueError("analytic decoupled control requires diagonal H")
    subdivisions, height = inputs["subdivisions"], inputs["height"]
    n, k = 4 * subdivisions, inputs["sources"].shape[-1]
    width, coarse_width = height / n, height / 4
    source = np.repeat(inputs["sources"], subdivisions, axis=1)
    means, faces = np.zeros((8, n, k)), np.zeros((8, n + 1, k))
    coarse = np.zeros((8, 4, k))
    primitives, normalized, witnesses = [], [], []
    with localcontext() as context:
        context.prec = ANALYTIC_DECIMAL_PRECISION
        D = Decimal.from_float
        for angle in range(8):
            length = D(float(width / abs(mu[angle])))
            sigma = D(float(h[angle, angle]))
            if sigma == 0:
                transmission, b, integral_d = Decimal(1), length, length * length / 2
            else:
                transmission = (-(length * sigma)).exp()
                b = (1 - transmission) / sigma
                integral_d = (length - b) / sigma
            beta, delta = b / length, integral_d / length
            primitives.append([float(transmission), float(b), float(integral_d)])
            normalized.append([float(beta), float(delta)])
            witnesses.append(dict(angle=angle, length_hex=float(length).hex(),
                                  attenuation_hex=float(sigma).hex(),
                                  T=str(transmission), B=str(b), D=str(integral_d),
                                  beta=str(beta), delta=str(delta)))
            incoming = [Decimal(0) for _ in range(k)]
            decimal_means = [[Decimal(0) for _ in range(k)] for _ in range(n)]
            indices = range(n) if mu[angle] > 0 else range(n - 1, -1, -1)
            for cell in indices:
                outgoing_face = cell + 1 if mu[angle] > 0 else cell
                outgoing = []
                for column in range(k):
                    q = D(float(source[angle, cell, column]))
                    mean = beta * incoming[column] + delta * q
                    out = transmission * incoming[column] + b * q
                    decimal_means[cell][column] = mean
                    means[angle, cell, column] = float(mean)
                    faces[angle, outgoing_face, column] = float(out)
                    outgoing.append(out)
                incoming = outgoing
            represented_ratio = D(float(width / coarse_width))
            for cell in range(4):
                for column in range(k):
                    coarse[angle, cell, column] = float(sum(
                        (decimal_means[i][column] * represented_ratio
                         for i in range(cell * subdivisions, (cell + 1) * subdivisions)), Decimal(0)
                    ))
    outgoing = np.zeros((2, 8, k))
    outgoing[0, mu < 0] = faces[mu < 0, 0]
    outgoing[1, mu > 0] = faces[mu > 0, -1]
    angular_escape = abs(mu)[None, :, None] * outgoing
    face_jz = np.einsum("s,sfk->fk", weights * mu, faces)
    return dict(
        fine_angular_means=means, fine_angular_faces=faces,
        coarse_angular_means=coarse, coarse_angular_faces=faces[:, ::subdivisions],
        fine_scalar_mean=np.einsum("s,szk->zk", weights, means),
        coarse_scalar_mean=np.einsum("s,szk->zk", weights, coarse),
        fine_signed_jz=np.einsum("s,szk->zk", weights * mu, means),
        coarse_signed_jz=np.einsum("s,szk->zk", weights * mu, coarse),
        fine_signed_face_jz=face_jz, coarse_signed_face_jz=face_jz[::subdivisions],
        bottom_top_outgoing_angular_flux=outgoing,
        bottom_top_angular_escape_current=angular_escape,
        bottom_top_escape_current=np.einsum("s,bsk->bk", weights, angular_escape),
        vacuum_incoming_angular_flux=np.zeros((8, k)), effective_algebraic_sources=source,
        algebraic_birth=np.einsum("s,z,szk->k", weights, np.full(n, width), source),
        algebraic_collision=np.einsum("s,z,szk->k", weights, np.full(n, width),
                                      np.einsum("st,tzk->szk", h, means)),
        primitive_TBD=np.asarray(primitives), primitive_beta_delta=np.asarray(normalized),
        decimal_primitive_witnesses=witnesses, decimal_precision=ANALYTIC_DECIMAL_PRECISION,
        analytic_scope="closed-form independent diagonal/void controls, not general coupled propagation",
    )


def _permuted_fields(result, permutation):
    transformed = {}
    angular = {"fine_angular_means", "fine_angular_faces", "coarse_angular_means",
               "coarse_angular_faces", "vacuum_incoming_angular_flux", "effective_algebraic_sources"}
    boundary_angular = {"bottom_top_outgoing_angular_flux", "bottom_top_angular_escape_current"}
    for name in FIELDS:
        if name in angular:
            transformed[name] = result[name][permutation]
        elif name in boundary_angular:
            transformed[name] = result[name][:, permutation]
        else:
            transformed[name] = result[name].copy()
    return transformed


def _reflected_fields(result, partner):
    transformed = {}
    angular_layer = {"fine_angular_means", "fine_angular_faces", "coarse_angular_means",
                     "coarse_angular_faces", "effective_algebraic_sources"}
    scalar_layer = {"fine_scalar_mean", "coarse_scalar_mean"}
    signed_layer = {"fine_signed_jz", "coarse_signed_jz", "fine_signed_face_jz", "coarse_signed_face_jz"}
    for name in FIELDS:
        if name in angular_layer:
            transformed[name] = result[name][partner, ::-1]
        elif name in scalar_layer:
            transformed[name] = result[name][::-1]
        elif name in signed_layer:
            transformed[name] = -result[name][::-1]
        elif name in {"bottom_top_outgoing_angular_flux", "bottom_top_angular_escape_current"}:
            transformed[name] = result[name][::-1, partner]
        elif name == "bottom_top_escape_current":
            transformed[name] = result[name][::-1]
        elif name == "vacuum_incoming_angular_flux":
            transformed[name] = result[name][partner]
        else:
            transformed[name] = result[name].copy()
    return transformed


def verify_controls(output_dir):
    """Run the preselected controls later, retaining every solve and audit."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    _write_json(folder / "run_claim.json", dict(started_unix=time.time(),
                                                control_source_sha256=_digest(Path(__file__))))
    started = time.monotonic()
    mu, weights = _normal_angles()
    sources, labels = _source_family(mu)
    coupled = _coupled_matrix(weights)
    rows, negative, solves = [], [], []

    def solve_pair(name, h, height=20.0, subdivisions=1, q=sources, m=mu, w=weights,
                   analytic=False, q_labels=None):
        if time.monotonic() - started >= WALL_LIMIT_SECONDS:
            raise RuntimeError("mathematical control stage wall cap reached")
        case_dir = folder / name
        case_dir.mkdir()
        inputs = dict(mu=np.asarray(m), weights=np.asarray(w), H=np.asarray(h),
                      height=float(height), subdivisions=subdivisions, sources=np.asarray(q))
        actual_labels = labels if q_labels is None else list(q_labels)
        if len(actual_labels) != q.shape[-1]:
            raise ValueError("each actual source column requires its matching identity label")
        input_archive = _archive(case_dir, "inputs", dict(**inputs, source_labels=actual_labels))
        system = candidate.build_slab(m, h, height, angular_weights=w,
                                      coarse_layers=4, subdivisions=subdivisions)
        system_archive = _archive(case_dir, "candidate_system", system)
        primary = candidate.solve_slab(system, q)
        primary_archive = _archive(case_dir, "candidate_raw", primary)
        solves.append(dict(case=name, role="candidate", archive=primary_archive))
        expanded = solve_expanded(m, h, height, angular_weights=w, coarse_layers=4,
                                  subdivisions=subdivisions, sources=q)
        expanded_archive = _archive(case_dir, "expanded_raw", expanded)
        solves.append(dict(case=name, role="expanded", archive=expanded_archive))
        row = dict(case=name, input_archive=input_archive, candidate_system_archive=system_archive,
                   height=height, subdivisions=subdivisions, source_columns=q.shape[-1],
                   candidate=_audit_result(primary, inputs, "candidate"),
                   expanded=_audit_result(expanded, inputs, "expanded"),
                   independent_expanded_fields=_compare(primary, expanded, name + "/expanded"))
        if analytic:
            literal = _analytic_decoupled(inputs)
            row["analytic_archive"] = _archive(case_dir, "analytic_raw", literal)
            row["candidate_analytic_fields"] = _compare(primary, literal, name + "/analytic candidate")
            row["expanded_analytic_fields"] = _compare(expanded, literal, name + "/analytic expanded")
            raw_tbd = np.asarray([[s["transmission"][0], s["B"][0], s["D"][0]] for s in system["sweeps"]])
            raw_mean = np.asarray([[s["mean_incoming"][0], s["mean_source"][0]] for s in system["sweeps"]])
            row["candidate_analytic_primitives"] = _array_error(raw_tbd, literal["primitive_TBD"], name + "/TBD")
            row["candidate_analytic_mean_coefficients"] = _array_error(raw_mean, literal["primitive_beta_delta"], name + "/beta delta")
        _write_json(case_dir / "audit.json", row)
        rows.append(row)
        return primary, expanded

    def reject(name, operation):
        try:
            operation()
        except (ValueError, ArithmeticError, np.linalg.LinAlgError) as error:
            negative.append(dict(control=name, rejected=True, exception_type=type(error).__name__, error=str(error)))
        else:
            raise ValueError("invalid mathematical input was accepted: " + name)

    result = dict(classification="FAILED_ANGULAR_SLAB_MATHEMATICAL_CONTROLS", error=None)
    try:
        diagonal = np.diag(np.repeat(np.asarray([0.08, 0.20, 0.55, 1.30]), 2))
        baseline = None
        for subdivisions in (1, 4):
            solve_pair(f"void_m{subdivisions}", np.zeros((8, 8)), subdivisions=subdivisions, analytic=True)
            solve_pair(f"diagonal_m{subdivisions}", diagonal, subdivisions=subdivisions, analytic=True)
        for subdivisions in (1, 2, 4):
            pair = solve_pair(f"coupled_m{subdivisions}", coupled, subdivisions=subdivisions)
            if subdivisions == 2:
                baseline = pair
        for subdivisions in (1, 4):
            solve_pair(f"thin_void_m{subdivisions}", np.zeros((8, 8)), height=4e-200,
                       subdivisions=subdivisions, analytic=True)
            solve_pair(f"thin_diagonal_m{subdivisions}", np.eye(8) * 1e-200, height=4e-200,
                       subdivisions=subdivisions, analytic=True)

        permutation = np.asarray([5, 1, 7, 0, 4, 6, 2, 3])
        pair = solve_pair("coupled_permutation", coupled[np.ix_(permutation, permutation)],
                          subdivisions=2, q=sources[permutation], m=mu[permutation], w=weights[permutation])
        permutation_checks = {
            role: _compare(actual, _permuted_fields(original, permutation), "permutation/" + role)
            for role, actual, original in zip(("candidate", "expanded"), pair, baseline, strict=True)
        }
        partner = np.asarray([1, 0, 3, 2, 5, 4, 7, 6])
        if (not np.array_equal(mu[partner], -mu) or not np.array_equal(weights[partner], weights)
                or not np.array_equal(coupled[np.ix_(partner, partner)], coupled)):
            raise ValueError("the prescribed reflection fixture must have exact paired identity")
        pair = solve_pair("coupled_reflection", coupled, subdivisions=2, q=sources[partner, ::-1])
        reflection_checks = {
            role: _compare(actual, _reflected_fields(original, partner), "reflection/" + role)
            for role, actual, original in zip(("candidate", "expanded"), pair, baseline, strict=True)
        }
        units = solve_pair("coupled_units_only", coupled, subdivisions=2,
                           q=sources[:, :, :32], q_labels=labels[:32])
        assembly = []
        for index in range(6):
            holdout = solve_pair("coupled_holdout_" + str(index + 1), coupled,
                                 subdivisions=2, q=sources[:, :, 32 + index:33 + index],
                                 q_labels=labels[32 + index:33 + index])
            coefficients = sources[:, :, 32 + index].reshape(32)
            audits = {}
            for role, unit, independently_solved in zip(("candidate", "expanded"), units, holdout, strict=True):
                assembled = {name: np.einsum("...c,c->...", unit[name], coefficients)[..., None] for name in FIELDS}
                audits[role] = _compare(independently_solved, assembled, "independent source assembly/" + role)
            assembly.append(dict(holdout=labels[32 + index], fields=audits))
        base_system = candidate.build_slab(mu, coupled, 20, angular_weights=weights, subdivisions=2)
        bad_h = coupled.copy(); bad_h[0, 1] = 1e-12
        reject("positive_off_diagonal_H", lambda: candidate.build_slab(mu, bad_h, 20, angular_weights=weights))
        bad_h = coupled.copy(); bad_h[0, 0] = -1e-12
        reject("negative_diagonal_H", lambda: candidate.build_slab(mu, bad_h, 20, angular_weights=weights))
        bad_h = coupled.copy(); bad_h[0, 0] = np.nan
        reject("nonfinite_H", lambda: candidate.build_slab(mu, bad_h, 20, angular_weights=weights))
        bad_mu = mu.copy(); bad_mu[0] = np.nan
        reject("nonfinite_mu", lambda: candidate.build_slab(bad_mu, coupled, 20, angular_weights=weights))
        bad_weights = weights.copy(); bad_weights[0] = np.inf
        reject("nonfinite_weights", lambda: candidate.build_slab(mu, coupled, 20, angular_weights=bad_weights))
        reject("nonfinite_height", lambda: candidate.build_slab(mu, coupled, np.inf, angular_weights=weights))
        bad_source = sources.copy(); bad_source[0, 0, 0] = np.nan
        reject("nonfinite_source", lambda: candidate.solve_slab(base_system, bad_source))
        reject("nonfinite_primitive_length", lambda: candidate.coefficients(np.nan, 0))
        reject("zero_primitive_length", lambda: candidate.coefficients(0, 0))
        reject("NaN_relative_scale", lambda: candidate._relative_max(np.nan, np.nan, ()))
        reject("negative_relative_scale", lambda: candidate._relative_max(1.0, -1.0, ()))
        _write_json(folder / "negative_controls.json", dict(controls=negative, all_rejected=True))
        if (len(rows) != EXPECTED_CASE_PAIRS or len(solves) != EXPECTED_NUMERICAL_SOLVES
                or len(negative) != EXPECTED_NEGATIVE_CONTROLS or len(assembly) != 6
                or len({(s["case"], s["role"]) for s in solves}) != EXPECTED_NUMERICAL_SOLVES):
            raise ValueError("every prescribed actual control case, solve and rejection is required")
        elapsed = time.monotonic() - started
        divisor = 1024**2 if sys.platform == "darwin" else 1024
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / divisor
        if elapsed >= WALL_LIMIT_SECONDS or peak >= RSS_LIMIT_MIB:
            raise RuntimeError("mathematical control stage resource cap exceeded")
        result.update(
            classification="COMPLETE_ANGULAR_SLAB_MATHEMATICAL_CONTROLS_ONLY",
            all_controls_passed=True, actual_numerical_solves=len(solves), actual_case_pairs=len(rows),
            expected_numerical_solves=EXPECTED_NUMERICAL_SOLVES, expected_case_pairs=EXPECTED_CASE_PAIRS,
            unit_coordinates=32, fixed_positive_holdouts=6, internal_subdivisions=[1, 2, 4],
            normal_cosines=mu.tolist(), explicit_weights=weights.tolist(), weights_rescaled=False,
            field_action_relative_limit=FIELD_LIMIT, cell_global_algebraic_relative_limit=ALGEBRAIC_LIMIT,
            vacuum_incoming_exact_zero=True, positive_fields_without_clipping=True,
            permutation_checks=permutation_checks, reflection_checks=reflection_checks,
            independent_holdout_assembly=assembly, negative_controls=len(negative),
            case_audits=rows, solve_archives=solves, elapsed_seconds=elapsed, peak_rss_mib=peak,
            mathematical_program_controls_verified=True, continuous_BVP_qualified=False,
            native_response_qualified=False, axial_propagation_qualified=False,
            physical_collision_balance_assessed=False, scattering_fission_iteration_qualified=False,
            AAA_accuracy_qualified=False, ABA_admitted=False,
            scope="same finite-subcell mathematical discretization and analytical fixtures only",
        )
    except BaseException as error:
        result["error"] = repr(error)
        result["completed_solve_archives"] = solves
        result["completed_case_audits"] = rows
        result["elapsed_seconds"] = time.monotonic() - started
        _write_json(folder / "failure.json", result)
        raise
    _write_json(folder / "result.json", result)
    _write_json(folder / "seal.json", dict(
        schema="ANGULAR_SLAB_MATHEMATICAL_CONTROLS_SEAL_V1",
        files={str(path.relative_to(folder)): _digest(path) for path in folder.rglob("*") if path.is_file()},
    ))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    arguments = parser.parse_args()
    report = verify_controls(arguments.output_dir)
    print("ANGULAR-COLLISION-SLAB-MATHEMATICAL-CONTROLS-PASSED")
    print(json.dumps(dict(classification=report["classification"], actual_numerical_solves=report["actual_numerical_solves"])))

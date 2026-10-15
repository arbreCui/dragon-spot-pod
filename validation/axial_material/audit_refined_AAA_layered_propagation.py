"""Unfrozen final audit for a separately declared finite-height comparison.

No audit or solve runs on import. The future final stage reads complete raw
archives and checks algebra, coordinates, provenance, and resource receipts.
It never solves a new linear system and never qualifies native propagation,
continuous propagation, physical reaction data, AAA, or ABA.
"""

from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation/axial_material"))

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix

from verify_angular_collision_slab_candidate import _normal_angles, _source_family
from white_side_trace_kernel import trace_exchange

OUT = ROOT / "validation/artifacts/axial-material-AAA-white-trace-refined-layered-propagation-20261005"
FULL = ROOT / "validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005"
ANGULAR = ROOT / "validation/artifacts/axial-material-AAA-white-trace-refined-native-angular-response-20261005"
ANGULAR_SEAL = "8862154f1fb3458676460f8a4074a1a52070322332dd08e66c2773b0e4345540"
GROUPS = (51, 61, 98)
MODELS = ("trace", "reduced")
LEVELS = (1, 2, 4, 8, 16, 32)
PERMUTATION = (1, 3, 5, 7, 0, 2, 4, 6)
FIELD_LIMIT = 5e-12
BALANCE_LIMIT = 1e-10
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
COARSE_FIELDS = (
    "coarse_angular_means", "coarse_angular_faces", "coarse_scalar_mean",
    "coarse_signed_jz", "coarse_signed_face_jz",
    "bottom_top_angular_escape_current", "bottom_top_escape_current",
)
SCOPE_FALSE = (
    "physical_collision_balance_assessed", "axial_propagation_qualified",
    "scattering_fission_iteration_qualified", "AAA_accuracy_qualified", "ABA_admitted",
)


def _read(path):
    return json.loads(Path(path).read_text())


def _write_new(path, value):
    with Path(path).open("x") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def _digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _require_hash(path, expected):
    _require(isinstance(expected, str) and len(expected) == 64,
             "an explicit SHA256 identity is required: " + str(path))
    _require(Path(path).is_file() and _digest(path) == expected,
             "frozen file identity differs: " + str(path))


def _provenance(root, path, receipts):
    path = Path(path)
    _require(path.is_file() and not path.is_symlink(), "regular archive required: " + str(path))
    name = str(path.relative_to(root))
    entry = dict(sha256=_digest(path), bytes=path.stat().st_size)
    _require(name not in receipts or receipts[name] == entry,
             "archive changed while being audited: " + name)
    receipts[name] = entry


def _npz(path):
    with np.load(path, allow_pickle=False) as archive:
        result = {name: archive[name].copy() for name in archive.files}
    for name, value in result.items():
        _require(not value.dtype.hasobject, "pickle/object archive prohibited: " + str(path) + "/" + name)
        if value.dtype.kind in "biufc":
            _require(np.isfinite(value).all(), "nonfinite raw archive: " + str(path) + "/" + name)
    return result


def _shape(value, shape, label):
    value = np.asarray(value)
    _require(value.shape == shape and value.dtype.kind in "biuf"
             and np.isfinite(value).all(), "complete finite coordinate shape differs: " + label)
    return value


def _exact(actual, expected, label):
    _require(np.array_equal(actual, expected), "exact identity differs: " + label)


def _columns(actual, expected, label, *, gate=None):
    actual, expected = np.asarray(actual), np.asarray(expected)
    _require(actual.shape == expected.shape and expected.ndim >= 1
             and np.isfinite(actual).all() and np.isfinite(expected).all(),
             "matching finite raw columns required: " + label)
    count = expected.shape[-1]
    scale = abs(expected).reshape(-1, count).max(axis=0)
    defect = abs(actual - expected).reshape(-1, count).max(axis=0)
    _require(not np.any((scale == 0) & (defect != 0)),
             "nonzero discrepancy on an exactly zero reference: " + label)
    ratio = np.divide(defect, scale, out=np.zeros_like(defect), where=scale > 0)
    _require(np.isfinite(ratio).all(), "nonfinite field discrepancy: " + label)
    if gate is not None:
        _require(np.max(ratio) < gate, "unchanged complete-field gate failed: " + label)
    return ratio


def _relative(defect, scale, axes, label, limit):
    defect, scale = np.asarray(defect), np.asarray(scale)
    _require(np.isfinite(defect).all() and np.isfinite(scale).all() and np.all(scale >= 0),
             "finite nonnegative residual scale required: " + label)
    scale = np.broadcast_to(scale, defect.shape)
    _require(not np.any((scale == 0) & (defect != 0)), "nonzero residual with zero scale: " + label)
    value = np.divide(abs(defect), scale, out=np.zeros_like(defect, dtype=float), where=scale > 0)
    maxima = np.max(value, axis=axes)
    _require(np.isfinite(maxima).all() and np.max(maxima) < limit,
             "unchanged raw residual gate failed: " + label)
    return maxima


def _weighted(actual, expected, weights, label):
    _require(actual.shape == expected.shape and weights.shape == expected.shape[:-1]
             and np.isfinite(actual).all() and np.isfinite(expected).all()
             and np.isfinite(weights).all() and np.all(weights > 0),
             "finite complete weighted fields required: " + label)
    axes = tuple(range(weights.ndim))
    numerator = ((actual - expected)**2 * weights[..., None]).sum(axis=axes)
    denominator = (expected**2 * weights[..., None]).sum(axis=axes)
    _require(np.isfinite(numerator).all() and np.isfinite(denominator).all()
             and np.all(denominator > 0), "positive finite reference norm required: " + label)
    result = np.sqrt(numerator / denominator)
    _require(np.isfinite(result).all(), "finite discrepancy report required: " + label)
    return result


def _scope(value, names=SCOPE_FALSE):
    for name in names:
        _require(value.get(name) is False, "comparison cannot grant qualification: " + name)


def _watch(stage, root):
    label = stage["label"]
    log = root / (label + ".log")
    _require_hash(log, stage["log_sha256"])
    receipt = _read(log.with_suffix(".watchdog.json"))
    _require(receipt["command"] == stage["command"] and receipt["returncode"] == 0
             and receipt["limit_failure"] is None and receipt["own_child_only"] is True
             and receipt["liveness_group_cleanup"] is True and receipt["rss_cap_mib"] == 512
             and 0 <= receipt["sampled_peak_rss_mib"] < 512
             and 0 <= receipt["elapsed_seconds"] < 600
             and 0 < receipt["wall_cap_seconds"] <= 600
             and 0 < stage["wall_cap_seconds"] <= 600 and 0 <= stage["elapsed_seconds"] < 600,
             "healthy bounded actual own-child receipt required: " + label)
    return receipt


def _seal(root, expected):
    _require_hash(root / "seal.json", expected)
    seal = _read(root / "seal.json")
    names = set(seal["files"])
    actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
              and p != root / "seal.json"}
    _require(names == actual, "complete sealed path set differs: " + str(root))
    for name, wanted in seal["files"].items():
        path = root / name
        _require(path.resolve().is_relative_to(root.resolve()), "seal path escapes its root")
        _require_hash(path, wanted)
    for path, wanted in _read(root / "declaration.json")["files"].items():
        _require_hash(path, wanted)
    return seal


def _dependencies(declaration):
    _require(Path(declaration["full_root"]).resolve() == FULL.resolve()
             and Path(declaration["angular_root"]).resolve() == ANGULAR.resolve(),
             "only the fixed current-data source roots are admitted")
    _require(declaration["angular_seal_sha256"] == ANGULAR_SEAL,
             "fixed angular source seal differs")
    _require(tuple(declaration["groups"]) == GROUPS and tuple(declaration["models"]) == MODELS
             and tuple(declaration["levels"]) == LEVELS and declaration["total_wall_seconds"] == 7200,
             "frozen complete comparison plan differs")
    for path, wanted in declaration["files"].items():
        _require_hash(path, wanted)
    _require_hash(FULL / "declaration.json", declaration["full_declaration_sha256"])
    _seal(FULL, declaration["full_seal_sha256"])
    _seal(ANGULAR, ANGULAR_SEAL)
    native, driver = _read(FULL / "result.json"), _read(FULL / "driver_result.json")
    _require(native["classification"] == "COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY"
             and native["full_current_discrete_fixed_source_qualified"] is True
             and native["full_current_geometric_white_qualified"] is True
             and driver["classification"] == "COMPLETE_BOUNDED_CURRENT_FULL_FIXED_SOURCE_WHITE_ONLY"
             and driver.get("error") is None, "completed source family and parent completion required")
    _require(native["groups"] == list(GROUPS) and native["original_tracks"] == 11364
             and native["primary_batches"] == native["exact_replay_batches"] == 180
             and native["actual_stages"] == 368 and native["independent_full_field_traces"] == 48
             and native["complete_coverage"] is True and native["complete_scientific_replay"] is True,
             "source-family complete counters differ")
    for phase in ("primary", "replay"):
        _require(native["observed_scientific_counters"][phase] == dict(
            physical_states=1090944, coordinate_evaluations=72002304, polar_records=45456),
            "complete observed source-family coverage differs")
    stages = _read(FULL / "AAA/stages.json")["stages"]
    _require(len(stages) == 368 and len({s["label"] for s in stages}) == 368
             and all(s["status"] == "PASS" for s in stages), "all 368 source stages must be PASS")
    watches = [_watch(stage, FULL) for stage in stages]
    _scope(native, ("AAA_accuracy_qualified", "scattering_fission_iteration_qualified",
                    "local_inverse_propagation_qualified", "ABA_admitted"))
    angular = _read(ANGULAR / "result.json")
    _require(angular["classification"] == "COMPLETE_CURRENT_DATA_FULL_ANGULAR_COLLISION_RESPONSE_ONLY"
             and [g["group"] for g in angular["groups"]] == list(GROUPS)
             and angular["all_original_tracks"] == 11364
             and angular["complete_angular_region_fields_retained"] is True
             and angular["projection_after_full_response"] is True,
             "complete fixed angular source required")
    _scope(angular, ("physical_accuracy_qualified", "axial_propagation_qualified",
                     "scattering_fission_iteration_qualified", "ABA_admitted"))
    return dict(full_root=str(FULL), full_seal_sha256=declaration["full_seal_sha256"],
                full_declaration_sha256=declaration["full_declaration_sha256"],
                angular_root=str(ANGULAR), angular_seal_sha256=ANGULAR_SEAL,
                source_stages=368, source_watchdogs=368,
                source_maximum_sampled_rss_mib=max(w["sampled_peak_rss_mib"] for w in watches))


def _sparse(arrays, prefix, shape, storage):
    if storage == "csc":
        _exact(arrays[prefix + "_format"], np.asarray("csc"), "explicit CSC format")
        suffix, constructor = "_", csc_matrix
    else:
        suffix, constructor = "__csr_", csr_matrix
    _exact(arrays[prefix + suffix + "shape"], shape, "expanded sparse shape")
    data = arrays[prefix + suffix + "data"]
    indices, indptr = arrays[prefix + suffix + "indices"], arrays[prefix + suffix + "indptr"]
    _require(data.ndim == indices.ndim == indptr.ndim == 1 and data.size == indices.size
             and indices.dtype.kind in "iu" and indptr.dtype.kind in "iu"
             and indptr.shape == (shape[0] + 1,) and indptr[0] == 0
             and indptr[-1] == data.size and np.all(np.diff(indptr) >= 0)
             and np.all(indices >= 0) and np.all(indices < shape[0]),
             "complete legal sparse expanded coordinates required")
    return constructor((data, indices, indptr), shape=tuple(shape))


def _audit_fields(fields, system, inputs, role, *, matrix=None):
    mu, weights, h = inputs["mu"], inputs["weights"], inputs["H"]
    height, m, q = inputs["height"], inputs["subdivisions"], inputs["sources"]
    n, k = 4 * m, q.shape[-1]
    shapes = dict(fine_angular_means=(8, n, k), fine_angular_faces=(8, n + 1, k),
        coarse_angular_means=(8, 4, k), coarse_angular_faces=(8, 5, k),
        fine_scalar_mean=(n, k), coarse_scalar_mean=(4, k), fine_signed_jz=(n, k),
        coarse_signed_jz=(4, k), fine_signed_face_jz=(n + 1, k), coarse_signed_face_jz=(5, k),
        bottom_top_outgoing_angular_flux=(2, 8, k), bottom_top_angular_escape_current=(2, 8, k),
        bottom_top_escape_current=(2, k), vacuum_incoming_angular_flux=(8, k),
        effective_algebraic_sources=(8, n, k), algebraic_birth=(k,), algebraic_collision=(k,))
    for name, shape in shapes.items():
        _shape(fields[name], shape, role + "/" + name)
    _exact(fields["external_sources"], q, role + "/external source order")
    fine_q = np.repeat(q, m, axis=1)
    _exact(fields["fine_external_sources"], fine_q, role + "/fine source lift")
    _require(np.all(q >= 0), "this comparison requires positive external columns")
    minima = {name: float(fields[name].min()) for name in POSITIVE_FIELDS}
    _require(min(minima.values()) >= 0, "positive response must be unclipped and nonnegative")
    diagnostics = fields["diagnostics"]
    for name, value in diagnostics.items():
        _require(np.isfinite(value).all(), "finite diagnostic required: " + role + "/" + name)
    for name in ("matrix_residual_relative", "characteristic_face_relative", "characteristic_mean_relative",
                 "full_directional_cell_equation_relative", "raw_algebraic_balance_relative"):
        _shape(diagnostics[name], (k,), role + "/diagnostic/" + name)
    for name, value in diagnostics.items():
        if name.endswith("_relative"):
            limit = BALANCE_LIMIT if name in (
                "full_directional_cell_equation_relative", "raw_algebraic_balance_relative") else FIELD_LIMIT
            _require(np.max(value) < limit, "stored unchanged diagnostic gate failed: " + role + "/" + name)
    _exact(diagnostics["external_source_column_nonnegative"], np.ones(k, dtype=bool), "source positivity diagnostic")
    _exact(diagnostics["angular_weights_sum"], weights.sum(), "explicit angular weights sum")
    for name, field in (("minimum_angular_mean", "fine_angular_means"),
                        ("minimum_angular_face", "fine_angular_faces"),
                        ("minimum_coarse_angular_mean", "coarse_angular_means"),
                        ("minimum_effective_algebraic_source", "effective_algebraic_sources")):
        _exact(diagnostics[name], fields[field].min(axis=(0, 1)), "actual raw minimum diagnostic")
    widths, coarse_width = np.full(n, height / n), np.full(4, height / 4)
    if role == "candidate":
        for name, value in (("mu", mu), ("angular_weights", weights), ("H", h),
                            ("fine_widths", widths), ("coarse_widths", coarse_width)):
            _exact(system[name], value, "candidate supplied " + name)
    else:
        _exact(fields["fine_widths"], widths, "expanded fine widths")
        _exact(fields["coarse_widths"], coarse_width, "expanded coarse widths")
        _exact(fields["coarse_restriction_weights"], np.repeat(widths.reshape(4, m)[:, 0] / coarse_width, m),
               "unrescaled expanded restriction weights")
    a, faces = fields["fine_angular_means"], fields["fine_angular_faces"]
    h_action = np.einsum("st,tzk->szk", h, a)
    effective = fine_q.copy()
    for s in range(8):
        for t in range(8):
            if s != t:
                effective[s] -= h[s, t] * a[t]
    _columns(fields["effective_algebraic_sources"], effective, role + "/effective source", gate=FIELD_LIMIT)
    restricted = (a.reshape(8, 4, m, k) * (widths.reshape(4, m) / coarse_width[:, None])[None, :, :, None]).sum(axis=2)
    derived = dict(coarse_angular_means=restricted, coarse_angular_faces=faces[:, ::m],
        fine_scalar_mean=np.einsum("s,szk->zk", weights, a),
        coarse_scalar_mean=np.einsum("s,szk->zk", weights, restricted),
        fine_signed_jz=np.einsum("s,szk->zk", weights * mu, a),
        coarse_signed_jz=np.einsum("s,szk->zk", weights * mu, restricted),
        fine_signed_face_jz=np.einsum("s,sfk->fk", weights * mu, faces))
    derived["coarse_signed_face_jz"] = derived["fine_signed_face_jz"][::m]
    incoming = np.stack([faces[s, 0 if mu[s] > 0 else -1] for s in range(8)])
    outgoing = np.stack([faces[:, 0] * (mu < 0)[:, None], faces[:, -1] * (mu > 0)[:, None]])
    angular_escape = abs(mu)[None, :, None] * outgoing
    escape = np.einsum("s,bsk->bk", weights, angular_escape)
    derived.update(vacuum_incoming_angular_flux=incoming, bottom_top_outgoing_angular_flux=outgoing,
                   bottom_top_angular_escape_current=angular_escape, bottom_top_escape_current=escape)
    _require(np.all(incoming == 0) and np.all(fields["vacuum_incoming_angular_flux"] == 0)
             and np.all(diagnostics["vacuum_incoming_absolute"] == 0), "incoming vacuum must be exactly zero")
    _exact(diagnostics["vacuum_incoming_absolute"], abs(incoming).max(axis=0), "actual vacuum diagnostic")
    derivation = {name: float(_columns(fields[name], value, role + "/derived/" + name,
                                     gate=FIELD_LIMIT).max()) for name, value in derived.items()}
    streaming = mu[:, None, None] * np.diff(faces, axis=1)
    cell = streaming + widths[None, :, None] * (h_action - fine_q)
    cell_scale = abs(streaming) + widths[None, :, None] * (abs(h_action) + abs(fine_q))
    birth = np.einsum("s,z,szk->k", weights, widths, fine_q)
    collision = np.einsum("s,z,szk->k", weights, widths, h_action)
    balance = escape.sum(axis=0) + collision - birth
    balance_scale = abs(escape).sum(axis=0) + np.einsum("s,z,szk->k", weights, widths, abs(h_action) + abs(fine_q))
    for name, value in (("algebraic_birth", birth), ("algebraic_collision", collision)):
        _columns(fields[name], value, role + "/" + name, gate=FIELD_LIMIT)
    checks = {}
    for name, raw, scale, axes, limit in (
        ("directional_cell_equation", cell, cell_scale, (0, 1), BALANCE_LIMIT),
        ("algebraic_balance", balance, balance_scale, (), BALANCE_LIMIT)):
        stored_name = "raw_directional_cell_equation" if name == "directional_cell_equation" else "raw_algebraic_balance"
        _shape(fields[stored_name + "_defect"], raw.shape, role + "/" + stored_name)
        _shape(fields[stored_name + "_scale"], scale.shape, role + "/" + stored_name + " scale")
        checks[name] = float(_relative(raw, scale, axes, role + "/" + name, limit).max())
        checks[name + "_archive_agreement"] = float(_relative(
            fields[stored_name + "_defect"] - raw, scale, axes, role + "/stored " + name, limit).max())
        _columns(fields[stored_name + "_scale"], scale, role + "/stored residual scale", gate=FIELD_LIMIT)
    face_defect, mean_defect, char_scale = np.zeros_like(a), np.zeros_like(a), np.zeros_like(a)
    for s in range(8):
        inc, out = (faces[s, :-1], faces[s, 1:]) if mu[s] > 0 else (faces[s, 1:], faces[s, :-1])
        lengths = np.full(n, (height / n) / abs(float(mu[s])))
        if role == "candidate":
            sweep = system["sweeps"][s]
            for name in ("transmission", "B", "D", "mean_incoming", "mean_source", "lengths"):
                _shape(sweep[name], (n,), "candidate sweep " + name)
            _exact(sweep["lengths"], lengths, "candidate characteristic lengths")
            transmission, b, beta, delta = (sweep[name] for name in ("transmission", "B", "mean_incoming", "mean_source"))
            face_defect[s] = out - (transmission[:, None] * inc + b[:, None] * effective[s])
            mean_defect[s] = a[s] - (beta[:, None] * inc + delta[:, None] * effective[s])
        else:
            _shape(fields["primitive_TBD"], (8, 3), "expanded independent T/B/D")
            _shape(fields["primitive_beta_delta"], (8, 2), "expanded independent mean coefficients")
            transmission, b, unused_d = fields["primitive_TBD"][s]
            beta, delta = fields["primitive_beta_delta"][s]
            face_defect[s] = out - transmission * inc - b * effective[s]
            mean_defect[s] = a[s] - beta * inc - delta * effective[s]
        char_scale[s] = abs(inc) + lengths[:, None] * abs(effective[s])
    for name, raw in (("face", face_defect), ("mean", mean_defect)):
        _shape(fields["raw_characteristic_" + name + "_defect"], raw.shape, role + "/raw characteristic " + name)
        checks["characteristic_" + name] = float(_relative(raw, char_scale, (0, 1), role + "/characteristic " + name, FIELD_LIMIT).max())
        checks["characteristic_" + name + "_archive_agreement"] = float(_relative(
            fields["raw_characteristic_" + name + "_defect"] - raw, char_scale, (0, 1),
            role + "/stored characteristic " + name, FIELD_LIMIT).max())
    _columns(fields["raw_characteristic_scale"], char_scale, role + "/characteristic scale", gate=FIELD_LIMIT)
    flat = a.reshape(8 * n, k)
    if role == "candidate":
        for name in ("flight", "coupling", "matrix"):
            _shape(system[name], (8 * n, 8 * n), "complete candidate " + name)
        off = h.copy(); np.fill_diagonal(off, 0)
        _exact(system["coupling"], np.kron(-off, np.eye(n)), "declared candidate angular coupling")
        expected_matrix = np.eye(8 * n)
        for s in range(8):
            rows = slice(s * n, (s + 1) * n)
            sweep = system["sweeps"][s]
            _shape(sweep["means"], (n, n), "complete angular mean sweep")
            _shape(sweep["faces"], (n + 1, n), "complete angular face sweep")
            _exact(system["flight"][rows, rows], sweep["means"], "diagonal angular flight block")
            _columns(sweep["faces"] @ fields["effective_algebraic_sources"][s], faces[s],
                     "candidate shared-face sweep reconstruction", gate=FIELD_LIMIT)
            for t in range(8):
                cols = slice(t * n, (t + 1) * n)
                if s != t:
                    _exact(system["flight"][rows, cols], np.zeros((n, n)), "angular flight block zeros")
                expected_matrix[rows, cols] -= (-off[s, t]) * sweep["means"]
        _columns(system["matrix"], expected_matrix, "candidate eliminated matrix construction", gate=FIELD_LIMIT)
        rhs = system["flight"] @ fine_q.reshape(8 * n, k)
        matrix_defect = system["matrix"] @ flat - rhs
        mean_defect_flat = system["flight"] @ fields["effective_algebraic_sources"].reshape(8 * n, k) - flat
        checks["reconstructed_mean"] = float(_relative(mean_defect_flat, abs(flat).max(axis=0), 0,
                                                      "candidate reconstructed mean", FIELD_LIMIT).max())
        _shape(fields["raw_mean_reconstruction_defect"], mean_defect_flat.shape, "candidate raw mean reconstruction")
        _relative(fields["raw_mean_reconstruction_defect"] - mean_defect_flat, abs(flat).max(axis=0), 0,
                  "candidate raw mean preservation", FIELD_LIMIT)
    else:
        dimension = 16 * n + 8
        _require(matrix is not None and matrix.shape == (dimension, dimension), "complete independent sparse system required")
        rhs = _shape(fields["expanded_rhs"], (dimension, k), "expanded rhs")
        solution = _shape(fields["expanded_solution"], (dimension, k), "expanded solution")
        _exact(solution[:8 * n], flat, "expanded mean unknown order")
        _exact(solution[8 * n:], faces.reshape(8 * (n + 1), k), "expanded face unknown order")
        matrix_defect = matrix @ solution - rhs
    _shape(fields["raw_matrix_residual"], matrix_defect.shape, role + "/raw matrix residual")
    checks["matrix"] = float(_relative(matrix_defect, abs(rhs).max(axis=0), 0, role + "/matrix", FIELD_LIMIT).max())
    checks["matrix_archive_agreement"] = float(_relative(fields["raw_matrix_residual"] - matrix_defect,
        abs(rhs).max(axis=0), 0, role + "/matrix preservation", FIELD_LIMIT).max())
    return dict(raw_residual_maxima=checks, recomputed_field_maxima=derivation,
                positive_field_minima=minima, source_columns=k, fine_layers=n,
                exact_source_order=True, exact_vacuum=True)


def _decimal_witnesses(witnesses, fields, inputs, precision):
    _require(len(witnesses) == 8 and precision in (80, 1024), "all independent Decimal witnesses required")
    tbd, normalized = [], []
    for s, witness in enumerate(witnesses):
        length = (inputs["height"] / (4 * inputs["subdivisions"])) / abs(float(inputs["mu"][s]))
        _require(witness["angle"] == s and witness["length_hex"] == float(length).hex()
                 and witness["attenuation_hex"] == float(inputs["H"][s, s]).hex(),
                 "Decimal witness inputs or angular order differ")
        values = [Decimal(witness[name]) for name in ("T", "B", "D", "beta", "delta")]
        _require(all(v.is_finite() and v >= 0 for v in values)
                 and values[0] <= 1 and values[3] <= 1, "legal finite independent Decimal primitives required")
        tbd.append([float(v) for v in values[:3]])
        normalized.append([float(v) for v in values[3:]])
    _exact(fields["primitive_TBD"], np.asarray(tbd), "Decimal-to-float T/B/D identity")
    _exact(fields["primitive_beta_delta"], np.asarray(normalized), "Decimal-to-float beta/delta identity")


def _reference(root, group, declaration, receipts):
    folder = root / "references" / ("g" + str(group))
    for name in ("reference.json", "reference.npz", "raw_native_action.npz"):
        _provenance(root, folder / name, receipts)
    report, saved, raw = _read(folder / "reference.json"), _npz(folder / "reference.npz"), _npz(folder / "raw_native_action.npz")
    _require(report["schema"] == "AXMAT_LAYERED_PROJECTED_REFERENCE_V1"
             and report["group"] == group and report["height"] == 20 and report["coarse_layers"] == 4
             and report["actual_source_columns"] == 38
             and report["all_32_coordinates_and_6_positive_controls"] is True
             and report["full_fields_retained_before_projection"] is True
             and report["geometric_white_incoming_measure"] is True
             and report["angular_to_full_permutation"] == list(PERMUTATION)
             and report["native_seal_sha256"] == declaration["full_seal_sha256"]
             and report["angular_seal_sha256"] == ANGULAR_SEAL
             and report["original_accuracy_thresholds_changed"] is False,
             "complete reference declaration and provenance differ")
    _scope(report, ("axial_propagation_qualified", "AAA_accuracy_qualified", "ABA_admitted"))
    inventory = _npz(FULL / "inputs/inventory.npz")
    vol = _shape(inventory["weights"][:8], (8,), "stored native region volumes")
    zmu, wzmu = inventory["zmu"], inventory["wzmu"]
    totals = _shape(inventory["group_totals"][GROUPS.index(group)], (8,), "actual group total coefficients")
    angular = _npz(ANGULAR / ("angular_response_g" + str(group) + ".npz"))
    mu, omega = _shape(angular["native_mu"], (8,), "native mu"), _shape(angular["omega"], (8,), "native weights")
    full_mu = np.asarray([sign * value for value in np.sqrt(1 - 1 / zmu**2) for sign in (-1, 1)])
    full_omega = np.repeat(wzmu * zmu / 2, 2)
    permutation = np.asarray(PERMUTATION)
    _exact(mu, full_mu[permutation], "native-to-slab angular permutation")
    _exact(omega, full_omega[permutation], "unrescaled native angular weights")
    _require(np.all(vol > 0) and np.all(omega > 0), "positive fixed measures required")
    basis = angular["source_lifting"][:8, 0]
    _shape(basis, (8,), "frozen radial basis")
    _require(np.all(basis > 0), "positive frozen radial basis required")
    _exact(angular["source_lifting"], np.kron(np.eye(8), basis[:, None]), "angular radial lifting")
    total_volume = sum(float(v) for v in vol)
    radial_weights = vol / total_volume
    gram, tau = 0.0, 0.0
    for w, b, total in zip(radial_weights, basis, totals, strict=True):
        gram += float(w) * float(b) * float(b)
        tau += float(w) * float(b) * float(b) * float(total)
    _require(gram > 0 and float(angular["gram"]) == gram and report["gram"] == gram,
             "original nonunit Gram differs")
    testing = radial_weights * basis / gram
    _exact(angular["testing"], np.kron(np.eye(8), testing[None]), "frozen nonunit Gram testing")
    trace = trace_exchange(mu, 2 * omega, 6 * .61776479, total_volume)
    h_trace = (tau * np.eye(8) + basis[0]**2 * trace) / gram
    _require(np.max(abs(h_trace @ angular["conditional_response"] - np.eye(8))) < FIELD_LIMIT,
             "trace hypothesis differs from its frozen conditional response")
    sources, labels = _source_family(mu)
    _require(report["source_labels"] == labels, "complete reference source labels differ")
    coefficients = sources.reshape(32, 38)
    lift = np.zeros((256, 32))
    for a, s in enumerate(PERMUTATION):
        for r in range(8):
            for layer in range(4):
                lift[s * 32 + r * 4 + layer, a * 4 + layer] = basis[r]
    polar = []
    for p in range(4):
        original = _npz(FULL / ("verification/p" + str(p) + "_h20_n4/operators.npz"))
        _exact(original["coverage"], np.ones((3, 2, 2, 11364), dtype=np.uint8), "full original record coverage")
        _shape(original["operators"], (2, 3, 2, 2, 72, 66), "complete two-order native operator")
        polar.append(original["operators"][1, GROUPS.index(group)].sum(axis=1))
    operator = np.concatenate(polar, axis=0)
    white = _npz(FULL / ("white/h20_n4/g" + str(group) + "_q32.npz"))
    _shape(white["white_amplitudes"], (24, 258), "native complete white amplitudes")
    amplitudes = white["white_amplitudes"][:, :256] @ lift @ coefficients
    phi = white["white_phi"][:, :256] @ lift @ coefficients
    jz = white["white_jz"][:, :256] @ lift @ coefficients
    geometry = _npz(FULL / "white/h20_n4/geometry.npz")
    gv, gr = _shape(geometry["volume"], (8, 32), "geometric volume"), _shape(geometry["radial"], (8, 24), "geometric radial incoming")
    _exact(geometry["mu"], full_mu, "geometric native angular order")
    stored_volume = np.repeat(vol * 5, 4)
    _exact(geometry["stored_volume"], stored_volume, "stored native volume convention")
    x = np.zeros((8, 66, 38))
    x[:, :32] = (lift @ coefficients).reshape(8, 32, 38)
    x[:, 32:56] = amplitudes[None]
    _exact(x[:, 56:], np.zeros((8, 10, 38)), "physical vacuum and unused axial controls")
    y = np.einsum("srk,skc->src", operator, x, optimize=True)
    _require(np.isfinite(y).all() and np.all(y >= 0), "complete native physical output must be finite and positive")
    for key, expected in dict(operator=operator, inputs=x, outputs=y, angular_to_full=permutation,
            source_lifting=lift, source_coefficients=coefficients, sources=sources, mu=mu, omega=omega,
            basis=basis, gram=gram, volume=vol, geometric_volume=gv, geometric_radial=gr,
            stored_volume=stored_volume, saved_phi=phi, saved_jz=jz).items():
        _exact(raw[key], expected, "raw native action identity/" + key)
    integrals = y[:, :32]
    reconstruction = dict(scalar=_columns(integrals.sum(axis=0) / stored_volume[:, None], phi,
                         "native scalar reconstruction", gate=FIELD_LIMIT),
        signed_jz=_columns(np.einsum("s,src->rc", full_mu, integrals) / stored_volume[:, None], jz,
                           "native signed jz reconstruction", gate=FIELD_LIMIT))
    birth = np.einsum("sr,src->c", gv, x[:, :32])
    collision = (integrals * np.repeat(totals, 4)[None, :, None]).sum(axis=(0, 1))
    physical_escape = y[:, 56:].sum(axis=(0, 1))
    physical_defect = birth - collision - physical_escape
    _require(np.all(birth > 0), "native physical birth must be positive for all 38 sources")
    balance = float(_relative(physical_defect, birth, (), "native physical balance", BALANCE_LIMIT).max())
    radial_target = gr.sum(axis=0)[:, None] * amplitudes
    closure = y[:, 32:56].sum(axis=0) - radial_target
    closure_max = float(_columns(y[:, 32:56].sum(axis=0), radial_target,
                                "geometric common-white closure", gate=FIELD_LIMIT).max())
    _require(np.all(y[full_mu > 0, 56:64] == 0) and np.all(y[full_mu < 0, 64:72] == 0),
             "native outgoing axial faces must follow their physical signs")
    complete = integrals[permutation].reshape(8, 8, 4, 38) / (omega[:, None, None, None] * vol[None, :, None, None] * 5)
    projected = np.einsum("r,srzc->szc", testing, complete)
    discarded = complete - basis[None, :, None, None] * projected[:, None]
    outgoing = y[permutation, 56:].reshape(8, 2, 8, 38) / (omega[:, None, None, None] * vol[None, None, :, None])
    projected_escape = np.einsum("r,sbrc->bsc", testing, outgoing)
    field_weights = omega[:, None, None] * radial_weights[None, :, None] * np.full((1, 1, 4), 5.)
    offspace = _weighted(complete - discarded, complete, field_weights, "discarded radial field")
    expected = dict(mu=mu, omega=omega, basis=basis, radial_weights=radial_weights, gram=gram, tau=tau,
        H_trace=h_trace, H_reduced=angular["projected_inverse"], sources=sources,
        source_lifting=lift, source_coefficients=coefficients, native_operator=operator,
        native_input=x, native_output=y, native_white_amplitudes=amplitudes,
        native_complete_angular_means=complete, native_projected_angular_means=projected,
        native_discarded_angular_means=discarded, native_projected_angular_escape=projected_escape,
        native_projected_signed_jz=np.einsum("s,szc->zc", omega * mu, projected),
        native_complete_field_weights=field_weights, native_field_offspace=offspace,
        raw_native_physical_birth=birth, raw_native_collision=collision,
        raw_native_physical_escape=physical_escape, raw_native_physical_defect=physical_defect,
        raw_native_white_closure_defect=closure,
        native_scalar_reconstruction_relative=reconstruction["scalar"],
        native_signed_jz_reconstruction_relative=reconstruction["signed_jz"])
    for name, value in expected.items():
        _exact(saved[name], value, "complete retained native reference/" + name)
    _require(report["native_reconstruction_max"] == max(float(v.max()) for v in reconstruction.values())
             and report["native_physical_balance_max"] == balance, "reference maxima must match actual raw fields")
    return saved, dict(group=group, source_columns=38, complete_field_shape=list(complete.shape),
        native_physical_balance_max=balance, native_white_closure_max=closure_max,
        discarded_radial_field_per_coordinate=offspace.tolist(), nonunit_gram=gram,
        source_order=labels, geometric_white_measure=True, stored_volume_mean_convention=True)


def _model_fields(arrays, role):
    fields = {name[len(role) + 1:]: value for name, value in arrays.items()
              if name.startswith(role + "_") and not name.startswith(role + "_diagnostic_")
              and not name.startswith("candidate_system_") and not name.startswith("candidate_sweep_")}
    fields["diagnostics"] = {name[len(role) + 12:]: value for name, value in arrays.items()
                             if name.startswith(role + "_diagnostic_")}
    return fields


def _model_system(arrays):
    system = {name[len("candidate_system_"):]: value for name, value in arrays.items()
              if name.startswith("candidate_system_")}
    system["sweeps"] = tuple({name[len("candidate_sweep_" + str(s) + "_"):]: value
        for name, value in arrays.items() if name.startswith("candidate_sweep_" + str(s) + "_")}
        for s in range(8))
    return system


def _compare_fields(actual, expected, label):
    return {name: float(_columns(actual[name], expected[name], label + "/" + name,
                                 gate=FIELD_LIMIT).max()) for name in FIELDS}


def _model(root, group, model, reference, receipts):
    folder = root / "models" / ("g" + str(group) + "_" + model)
    report = _read(folder / "result.json")
    _provenance(root, folder / "result.json", receipts)
    _require(report["schema"] == "AXMAT_LAYERED_PROPAGATION_COMPARISON_V1"
             and report["model"] == model and report["height"] == 20 and report["coarse_layers"] == 4
             and report["source_columns"] == 38 and report["prescribed_subdivisions"] == list(LEVELS)
             and report["actual_returned_linear_solves"] == 12
             and report["actual_source_column_solves"] == 456
             and report["all_prescribed_levels_executed"] is True
             and report["fine_refinement_is_report_only"] is True
             and report["original_accuracy_thresholds_changed"] is False,
             "all predeclared actual model levels and counters required")
    _scope(report, ("continuous_BVP_converged", "native_propagation_qualified", "model_chosen_by_CE",
                    "physical_collision_balance_assessed", "scattering_fission_iteration_qualified",
                    "AAA_accuracy_qualified", "ABA_admitted"))
    _require(len(report["refinements"]) == 6, "all six actual refinement reports required")
    q, mu, weights, h = (reference[name] for name in ("sources", "mu", "omega", "H_" + model))
    _shape(h, (8, 8), "complete predeclared hypothesis")
    _require(np.all(np.diag(h) >= 0), "declared H attenuation must not be repaired")
    off = h.copy(); np.fill_diagonal(off, 0)
    _require(np.all(off <= 0), "declared H off-diagonal signs must not be repaired")
    previous, audits = None, []
    for m, row in zip(LEVELS, report["refinements"], strict=True):
        _require(row["subdivisions"] == m and row["candidate_source_columns"] == 38
                 and row["expanded_source_columns"] == 38 and row["actual_returned_linear_solves"] == 2
                 and row["numerical_program_checks_passed"] is True, "actual returned level counters differ")
        inputs = dict(mu=mu, weights=weights, H=h, height=20., subdivisions=m, sources=q)
        paths = {role: folder / (f"subdivisions_{m:02d}_" + role + ".npz") for role in ("candidate", "expanded")}
        metadata = {}
        raw = {}
        for role in ("candidate", "expanded"):
            path = paths[role]
            metadata[role] = _read(path.with_suffix(".metadata.json"))
            _provenance(root, path, receipts)
            _provenance(root, path.with_suffix(".metadata.json"), receipts)
            raw[role] = _npz(path)
            meta = metadata[role]
            _require(meta["schema"] == "AXMAT_LAYERED_CANDIDATE_RETURN_V1" and meta["role"] == role
                     and meta["source_columns"] == 38 and meta["fine_layers"] == 4 * m,
                     "actual returned model archive metadata differs")
            _scope(meta)
            if role == "expanded":
                _scope(meta, ("continuous_BVP_qualified", "native_response_qualified"))
                _require(meta["sparse_format"] == "csc" and meta["decimal_precision"] == 80
                         and meta["mean_unknowns"] == 32 * m and meta["face_unknowns"] == 32 * m + 8
                         and meta["expanded_dimension"] == 64 * m + 8,
                         "complete independent expanded unknowns required")
        candidate, expanded = (_model_fields(raw[role], role) for role in ("candidate", "expanded"))
        system = _model_system(raw["candidate"])
        matrix = _sparse(raw["expanded"], "expanded_matrix", (64 * m + 8, 64 * m + 8), "csc")
        candidate_audit = _audit_fields(candidate, system, inputs, "candidate")
        expanded_audit = _audit_fields(expanded, None, inputs, "expanded", matrix=matrix)
        decimal_path = folder / f"subdivisions_{m:02d}_decimal.json"
        witnesses = _read(decimal_path)
        _provenance(root, decimal_path, receipts)
        _require(witnesses["schema"] == "AXMAT_LAYERED_DECIMAL_WITNESSES_V1"
                 and witnesses["precision"] == 80 and witnesses["angle_count"] == 8,
                 "all independent Decimal80 witnesses required")
        _decimal_witnesses(witnesses["witnesses"], expanded, inputs, 80)
        candidate_tbd = np.asarray([[system["sweeps"][s][name][0] for name in ("transmission", "B", "D")] for s in range(8)])
        candidate_mean = np.asarray([[system["sweeps"][s][name][0] for name in ("mean_incoming", "mean_source")] for s in range(8)])
        _columns(candidate_tbd, expanded["primitive_TBD"], "candidate independent T/B/D", gate=FIELD_LIMIT)
        _columns(candidate_mean, expanded["primitive_beta_delta"], "candidate independent beta/delta", gate=FIELD_LIMIT)
        independent = _compare_fields(candidate, expanded, "all-column independent expanded model")
        _require(set(row["independent_complete_field_max"]) == set(FIELDS), "complete shared independent fields required")
        for name, value in independent.items():
            _exact(row["independent_complete_field_max"][name], value, "reported actual independent field maximum")
        lifted = reference["basis"][None, :, None, None] * candidate["coarse_angular_means"][:, None]
        errors = dict(
            projected_angular_mean=_weighted(candidate["coarse_angular_means"], reference["native_projected_angular_means"],
                weights[:, None] * np.full((1, 4), 5.), "projected native discrepancy"),
            complete_angular_region_mean=_weighted(lifted, reference["native_complete_angular_means"],
                reference["native_complete_field_weights"], "complete native radial field discrepancy"),
            basis_tested_signed_jz=_columns(candidate["coarse_signed_jz"], reference["native_projected_signed_jz"], "signed jz discrepancy"),
            basis_tested_outgoing_angular_current=_columns(candidate["bottom_top_angular_escape_current"],
                reference["native_projected_angular_escape"], "basis-tested outgoing current discrepancy"))
        _require(set(row["native_discrepancy_per_coordinate"]) == set(errors), "all native discrepancy fields required")
        for name, value in errors.items():
            _shape(value, (38,), "all actual native discrepancy columns")
            _exact(np.asarray(row["native_discrepancy_per_coordinate"][name]), value, "actual discrepancy report/" + name)
        changes = {} if previous is None else {
            name: _columns(candidate[name], previous[name], "prescribed refinement change/" + name) for name in COARSE_FIELDS}
        _require(set(row["change_from_previous_per_coordinate"]) == set(changes), "all prescribed refinement changes required")
        for name, value in changes.items():
            _shape(value, (38,), "all actual refinement change columns")
            _exact(np.asarray(row["change_from_previous_per_coordinate"][name]), value, "actual refinement report/" + name)
        _require(row["minimum_angular_mean"] == float(candidate["fine_angular_means"].min())
                 and row["minimum_angular_face"] == float(candidate["fine_angular_faces"].min()),
                 "actual field minima differ")
        audits.append(dict(subdivisions=m, source_columns=38, candidate=candidate_audit,
            expanded=expanded_audit, independent_field_maxima=independent,
            native_discrepancy_per_coordinate={name: value.tolist() for name, value in errors.items()},
            change_from_previous_per_coordinate={name: value.tolist() for name, value in changes.items()}))
        previous = {name: candidate[name].copy() for name in COARSE_FIELDS}
        del candidate, expanded, system, matrix, raw
    return dict(group=group, model=model, actual_case_pairs=6, actual_linear_solves=12,
                actual_source_column_solves=456, refinements=audits, fine_refinement_is_report_only=True)


def _control_archive(root, folder, stem, receipt, provenance):
    _require(receipt["arrays_file"] == stem + ".npz"
             and receipt["metadata_file"] == stem + ".metadata.json"
             and receipt["object_arrays"] is False, "exact raw control archive names required")
    array_path, metadata_path = folder / receipt["arrays_file"], folder / receipt["metadata_file"]
    _require_hash(array_path, receipt["arrays_sha256"])
    _require_hash(metadata_path, receipt["metadata_sha256"])
    _require(array_path.stat().st_size == receipt["arrays_bytes"], "actual archive byte receipt differs")
    arrays, metadata = _npz(array_path), _read(metadata_path)
    _require(len(arrays) == receipt["numeric_arrays"], "all actual raw numeric arrays required")
    _provenance(root, array_path, provenance)
    _provenance(root, metadata_path, provenance)
    return arrays, metadata


def _control_fields(arrays):
    fields = {name: value for name, value in arrays.items() if not name.startswith("diagnostics__")}
    fields["diagnostics"] = {name[len("diagnostics__"):]: value for name, value in arrays.items()
                             if name.startswith("diagnostics__")}
    return fields


def _control_system(arrays, metadata):
    _require(metadata["sweeps__sequence_length"] == 8, "all eight raw characteristic sweeps required")
    system = {name: value for name, value in arrays.items() if not name.startswith("sweeps__")}
    system["sweeps"] = tuple({name[len("sweeps__" + str(s) + "__"):]: value
        for name, value in arrays.items() if name.startswith("sweeps__" + str(s) + "__")} for s in range(8))
    return system


def _control_scope(arrays, metadata, role):
    combined = dict(metadata)
    combined.update({name: value.item() for name, value in arrays.items() if value.ndim == 0})
    _scope(combined)
    if role == "expanded":
        _scope(combined, ("continuous_BVP_qualified", "native_response_qualified"))
    return combined


def _archived_witnesses(arrays, metadata):
    _require(metadata["decimal_primitive_witnesses__sequence_length"] == 8, "all raw Decimal witness angles required")
    witnesses = []
    for s in range(8):
        prefix = "decimal_primitive_witnesses__" + str(s) + "__"
        witness = {name: metadata[prefix + name] for name in ("length_hex", "attenuation_hex", "T", "B", "D", "beta", "delta")}
        witness["angle"] = arrays[prefix + "angle"].item()
        witnesses.append(witness)
    return witnesses


def _permuted(result, permutation):
    angular = {"fine_angular_means", "fine_angular_faces", "coarse_angular_means", "coarse_angular_faces",
               "effective_algebraic_sources", "vacuum_incoming_angular_flux"}
    boundary = {"bottom_top_outgoing_angular_flux", "bottom_top_angular_escape_current"}
    return {name: result[name][permutation] if name in angular else
            result[name][:, permutation] if name in boundary else result[name] for name in FIELDS}


def _reflected(result, partner):
    angular = {"fine_angular_means", "fine_angular_faces", "coarse_angular_means",
               "coarse_angular_faces", "effective_algebraic_sources"}
    scalar = {"fine_scalar_mean", "coarse_scalar_mean"}
    signed = {"fine_signed_jz", "coarse_signed_jz", "fine_signed_face_jz", "coarse_signed_face_jz"}
    boundary = {"bottom_top_outgoing_angular_flux", "bottom_top_angular_escape_current"}
    answer = {}
    for name in FIELDS:
        value = result[name]
        if name in angular:
            value = value[partner, ::-1]
        elif name in scalar:
            value = value[::-1]
        elif name in signed:
            value = -value[::-1]
        elif name in boundary:
            value = value[::-1][:, partner]
        elif name == "bottom_top_escape_current":
            value = value[::-1]
        elif name == "vacuum_incoming_angular_flux":
            value = value[partner]
        answer[name] = value
    return answer


def _math_controls(root, provenance):
    folder = root / "math_controls"
    report = _read(folder / "result.json")
    claim = _read(folder / "run_claim.json")
    _require(claim["control_source_sha256"] == _digest(
        ROOT / "validation/axial_material/verify_angular_collision_slab_candidate.py"),
        "actual mathematical control source identity differs")
    _require(report["classification"] == "COMPLETE_ANGULAR_SLAB_MATHEMATICAL_CONTROLS_ONLY"
             and report["all_controls_passed"] is True and report["actual_case_pairs"] == 20
             and report["actual_numerical_solves"] == 40 and report["negative_controls"] == 11
             and report["unit_coordinates"] == 32 and report["fixed_positive_holdouts"] == 6
             and report["field_action_relative_limit"] == FIELD_LIMIT
             and report["cell_global_algebraic_relative_limit"] == BALANCE_LIMIT
             and report["weights_rescaled"] is False and report["vacuum_incoming_exact_zero"] is True
             and report["positive_fields_without_clipping"] is True
             and 0 <= report["elapsed_seconds"] < 600 and 0 <= report["peak_rss_mib"] < 512,
             "complete bounded mathematical controls required")
    _scope(report)
    _scope(report, ("continuous_BVP_qualified", "native_response_qualified"))
    mu, weights = _normal_angles()
    q, labels = _source_family(mu)
    _exact(np.asarray(report["normal_cosines"]), mu, "control prescribed angular identity")
    _exact(np.asarray(report["explicit_weights"]), weights, "control unrescaled angular weights")
    coupled = np.diag(np.repeat(np.asarray([.12, .18, .24, .30]), 2) + .16 * weights.sum()) - .16 * np.ones((8, 1)) * weights[None]
    diagonal = np.diag(np.repeat(np.asarray([.08, .20, .55, 1.30]), 2))
    presets = []
    def preset(name, h, m=1, height=20., sources=q, normal=mu, angular=weights, source_labels=labels, analytic=False):
        presets.append((name, dict(mu=normal, weights=angular, H=h, height=height, subdivisions=m, sources=sources),
                        source_labels, analytic))
    for m in (1, 4):
        preset("void_m" + str(m), np.zeros((8, 8)), m, analytic=True)
        preset("diagonal_m" + str(m), diagonal, m, analytic=True)
    for m in (1, 2, 4):
        preset("coupled_m" + str(m), coupled, m)
    for m in (1, 4):
        preset("thin_void_m" + str(m), np.zeros((8, 8)), m, 4e-200, analytic=True)
        preset("thin_diagonal_m" + str(m), np.eye(8) * 1e-200, m, 4e-200, analytic=True)
    permutation = np.asarray([5, 1, 7, 0, 4, 6, 2, 3])
    partner = np.asarray([1, 0, 3, 2, 5, 4, 7, 6])
    preset("coupled_permutation", coupled[np.ix_(permutation, permutation)], 2,
           sources=q[permutation], normal=mu[permutation], angular=weights[permutation])
    preset("coupled_reflection", coupled, 2, sources=q[partner, ::-1])
    preset("coupled_units_only", coupled, 2, sources=q[:, :, :32], source_labels=labels[:32])
    for i in range(6):
        preset("coupled_holdout_" + str(i + 1), coupled, 2, sources=q[:, :, 32 + i:33 + i],
               source_labels=labels[32 + i:33 + i])
    _require([row["case"] for row in report["case_audits"]] == [p[0] for p in presets],
             "every preselected actual mathematical case is required in order")
    solve_map = {(s["case"], s["role"]): s for s in report["solve_archives"]}
    _require(len(solve_map) == len(report["solve_archives"]) == 40
             and set(solve_map) == {(name, role) for name, unused, ignored, analytic in presets
                                    for role in ("candidate", "expanded")}, "all actual returned raw solves required")
    expected_paths = {"run_claim.json", "negative_controls.json", "result.json", "seal.json"}
    retained, audits, column_count = {}, [], 0
    for (name, inputs, source_labels, analytic), row in zip(presets, report["case_audits"], strict=True):
        case_folder = folder / name
        _require(_read(case_folder / "audit.json") == row, "actual case audit/report identity differs")
        _provenance(root, case_folder / "audit.json", provenance)
        k, m = inputs["sources"].shape[-1], inputs["subdivisions"]
        _require(row["source_columns"] == k and row["height"] == inputs["height"]
                 and row["subdivisions"] == m, "actual control input counters differ")
        original, metadata = _control_archive(root, case_folder, "inputs", row["input_archive"], provenance)
        _require(set(original) == set(inputs) and metadata["source_labels"] == list(source_labels),
                 "all actual control coordinates and labels required")
        for key, value in inputs.items():
            _exact(original[key], value, "actual prescribed control input/" + key)
        system_arrays, system_metadata = _control_archive(root, case_folder, "candidate_system",
                                                         row["candidate_system_archive"], provenance)
        system = _control_system(system_arrays, system_metadata)
        actual, role_audits = {}, {}
        for role in ("candidate", "expanded"):
            arrays, metadata = _control_archive(root, case_folder, role + "_raw",
                solve_map[(name, role)]["archive"], provenance)
            fields = _control_fields(arrays)
            scope = _control_scope(arrays, metadata, role)
            matrix = None
            if role == "expanded":
                _require(metadata["expanded_matrix"]["storage"] == "explicit CSR data/indices/indptr/shape"
                         and scope["decimal_precision"] == 80 and scope["mean_unknowns"] == 32 * m
                         and scope["face_unknowns"] == 32 * m + 8 and scope["expanded_dimension"] == 64 * m + 8,
                         "complete raw independent expanded unknowns required")
                matrix = _sparse(arrays, "expanded_matrix", (64 * m + 8, 64 * m + 8), "csr")
                _decimal_witnesses(_archived_witnesses(arrays, metadata), fields, inputs, 80)
            role_audits[role] = _audit_fields(fields, system if role == "candidate" else None,
                                            inputs, role, matrix=matrix)
            actual[role] = {key: fields[key].copy() for key in FIELDS}
            if name == "coupled_m2" or name == "coupled_units_only" or name.startswith("coupled_holdout_"):
                retained[(name, role)] = actual[role]
            del fields, arrays, matrix
        independent = _compare_fields(actual["candidate"], actual["expanded"], "actual mathematical expanded control/" + name)
        analytic_audits = {}
        if analytic:
            literal, metadata = _control_archive(root, case_folder, "analytic_raw", row["analytic_archive"], provenance)
            _require(literal["decimal_precision"].item() == 1024, "thin direct-exponential control must retain 1024 digits")
            _decimal_witnesses(_archived_witnesses(literal, metadata), literal, inputs, 1024)
            analytic_audits = {role: _compare_fields(actual[role], literal, "actual analytic control/" + name + "/" + role)
                              for role in ("candidate", "expanded")}
            candidate_tbd = np.asarray([[system["sweeps"][s][key][0] for key in ("transmission", "B", "D")] for s in range(8)])
            candidate_mean = np.asarray([[system["sweeps"][s][key][0] for key in ("mean_incoming", "mean_source")] for s in range(8)])
            _columns(candidate_tbd, literal["primitive_TBD"], "independent analytic candidate T/B/D", gate=FIELD_LIMIT)
            _columns(candidate_mean, literal["primitive_beta_delta"], "independent analytic candidate beta/delta", gate=FIELD_LIMIT)
            del literal
        if name == "coupled_permutation":
            for role in ("candidate", "expanded"):
                _compare_fields(actual[role], _permuted(retained[("coupled_m2", role)], permutation), "actual angular permutation/" + role)
        if name == "coupled_reflection":
            _exact(mu[partner], -mu, "paired control axial cosines")
            _exact(weights[partner], weights, "paired control angular weights")
            _exact(coupled[np.ix_(partner, partner)], coupled, "paired control H")
            for role in ("candidate", "expanded"):
                _compare_fields(actual[role], _reflected(retained[("coupled_m2", role)], partner), "actual axial reflection/" + role)
        case_paths = [name + "/" + stem + suffix for stem in ("inputs", "candidate_system", "candidate_raw", "expanded_raw")
                      for suffix in (".npz", ".metadata.json")] + [name + "/audit.json"]
        if analytic:
            case_paths += [name + "/analytic_raw.npz", name + "/analytic_raw.metadata.json"]
        expected_paths.update(case_paths)
        column_count += 2 * k
        audits.append(dict(case=name, source_columns=k, fine_layers=4 * m, role_audits=role_audits,
                           independent_fields=independent, analytic_fields=analytic_audits))
        del actual, system, system_arrays, original
    assembly = []
    for i in range(6):
        name = "coupled_holdout_" + str(i + 1)
        coefficients = q[:, :, 32 + i].reshape(32)
        role_checks = {}
        for role in ("candidate", "expanded"):
            unit = retained[("coupled_units_only", role)]
            assembled = {key: np.einsum("...c,c->...", unit[key], coefficients)[..., None] for key in FIELDS}
            role_checks[role] = _compare_fields(retained[(name, role)], assembled, "actual independent holdout assembly/" + name + "/" + role)
        assembly.append(dict(holdout=labels[32 + i], role_checks=role_checks))
    negative = _read(folder / "negative_controls.json")
    names = ("positive_off_diagonal_H", "negative_diagonal_H", "nonfinite_H", "nonfinite_mu",
             "nonfinite_weights", "nonfinite_height", "nonfinite_source", "nonfinite_primitive_length",
             "zero_primitive_length", "NaN_relative_scale", "negative_relative_scale")
    _require(negative["all_rejected"] is True and [c["control"] for c in negative["controls"]] == list(names)
             and all(c["rejected"] is True and c["exception_type"] in ("ValueError", "ArithmeticError", "LinAlgError")
                     and isinstance(c["error"], str) for c in negative["controls"]),
             "all eleven fixed negative-control rejection receipts required")
    _require(column_count == 1064 and len(audits) == 20 and len(assembly) == 6, "actual mathematical solve coverage differs")
    actual_paths = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file()}
    _require(actual_paths == expected_paths and len(actual_paths) == 200, "complete exact mathematical archive path set required")
    seal = _read(folder / "seal.json")
    _require(seal["schema"] == "ANGULAR_SLAB_MATHEMATICAL_CONTROLS_SEAL_V1"
             and set(seal["files"]) == expected_paths - {"seal.json"}, "complete mathematical source seal coverage required")
    for name, wanted in seal["files"].items():
        _require_hash(folder / name, wanted)
        _provenance(root, folder / name, provenance)
    _provenance(root, folder / "seal.json", provenance)
    return dict(actual_case_pairs=20, actual_linear_solves=40, actual_source_column_solves=1064,
        negative_controls=11, mathematical_seal_sha256=_digest(folder / "seal.json"),
        exact_archive_files=200, case_audits=audits, independently_recomputed_holdout_assembly=assembly,
        negative_control_scope="frozen-program rejection receipts; no negative-control numerical replay in this final audit")


def _stage_receipts(root, provenance):
    index_path = root / "stage_receipts.json"
    index = _read(index_path)
    _provenance(root, index_path, provenance)
    outputs = {"mathematical_controls": root / "math_controls"}
    outputs.update({"reference_g" + str(group): root / "references" / ("g" + str(group)) for group in GROUPS})
    outputs.update({"model_g" + str(group) + "_" + model: root / "models" / ("g" + str(group) + "_" + model)
                    for group in GROUPS for model in MODELS})
    _require(set(index) == set(outputs) and len(index) == 10, "all ten completed actual stage receipts required")
    reports = []
    for name, folder in outputs.items():
        path = root / "runs" / (name + ".receipt.json")
        _require(index[name]["path"] == str(path), "exact completed-stage receipt path required")
        _require_hash(path, index[name]["sha256"])
        receipt = _read(path)
        _require(receipt["root"] == str(folder), "exact completed-stage output root required")
        actual = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file()}
        _require(set(receipt["files"]) == actual, "complete completed-stage namespace differs")
        if name == "mathematical_controls":
            expected = 200
        elif name.startswith("reference_"):
            _require(actual == {"reference.json", "reference.npz", "raw_native_action.npz"},
                     "complete original reference output namespace required")
            expected = 3
        else:
            expected_names = {"result.json"}
            for m in LEVELS:
                for role in ("candidate", "expanded"):
                    expected_names.add(f"subdivisions_{m:02d}_" + role + ".npz")
                    expected_names.add(f"subdivisions_{m:02d}_" + role + ".metadata.json")
                expected_names.add(f"subdivisions_{m:02d}_decimal.json")
            _require(actual == expected_names, "every predeclared raw model return and witness is required")
            expected = 31
        _require(len(actual) == expected, "complete actual stage file count differs")
        for filename, wanted in receipt["files"].items():
            archive = folder / filename
            _require(archive.resolve().is_relative_to(folder.resolve()) and not archive.is_symlink(),
                     "regular stage archive must stay in its declared root")
            _require_hash(archive, wanted)
            _provenance(root, archive, provenance)
        _provenance(root, path, provenance)
        reports.append(dict(stage=name, root=str(folder), files=expected, receipt_sha256=index[name]["sha256"]))
    return reports


def _execution_contract(root, declaration, provenance):
    expected = (["runs/mathematical_controls"] + ["runs/reference_g" + str(g) for g in GROUPS]
                + ["runs/model_g" + str(g) + "_" + model for g in GROUPS for model in MODELS] + ["verification"])
    _require(declaration["schema"] == "AXMAT_CURRENT_LAYERED_COMPARISON_DECLARATION_V1"
             and declaration["expected_stage_labels"] == expected
             and declaration["stage_wall_seconds"] == 600 and declaration["rss_cap_mib"] == 512
             and declaration["artifact_budget_bytes"] == 96 * 2**30 and declaration["min_free_bytes"] == 8 * 2**30
             and declaration["threads"] == declaration["numeric_children_at_once"] == 1
             and declaration["retries"] == 0 and declaration["rss_poll_seconds"] == .2
             and declaration["complete_storage_admitted"] is True
             and 0 < declaration["complete_uncompressed_bound_bytes"] < 2 * 2**30
             and declaration["field_action_relative_limit"] == FIELD_LIMIT
             and declaration["cell_global_algebraic_relative_limit"] == BALANCE_LIMIT,
             "unchanged bounded execution, storage admission and mathematical gates required")
    counters = dict(expected_math_case_pairs=20, expected_math_solves=40, expected_negative_controls=11,
        expected_model_case_pairs=36, expected_model_solves=72, expected_total_case_pairs=56,
        expected_total_linear_solves=112, expected_total_source_column_solves=3800, reference_source_columns=38)
    for name, wanted in counters.items():
        _require(declaration[name] == wanted, "frozen complete scientific counter differs: " + name)
    _scope(declaration, ("continuous_BVP_qualified", "native_propagation_qualified",
        "physical_collision_balance_assessed", "scattering_fission_iteration_qualified",
        "AAA_accuracy_qualified", "ABA_admitted", "original_accuracy_thresholds_changed",
        "production_solver_changed", "CE_data_used"))
    required_sources = (Path(__file__).resolve(),
        ROOT / "validation/axial_material/qualify_refined_AAA_layered_propagation.py",
        ROOT / "validation/axial_material/compare_refined_AAA_layered_propagation.py",
        ROOT / "validation/axial_material/verify_angular_collision_slab_candidate.py",
        ROOT / "validation/axial_material/angular_collision_slab_candidate.py",
        ROOT / "validation/axial_material/angular_collision_slab_expanded_reference.py",
        ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py", Path(sys.executable).resolve())
    _require(all(str(path.resolve()) in declaration["files"] for path in required_sources),
             "all executing numerical and audit sources must be frozen")
    for name, expected_alias in declaration["native_library_aliases"].items():
        _require(str(Path(name).resolve()) == expected_alias and expected_alias in declaration["files"],
                 "fixed canonical numerical library and alias required")
    loader = declaration["numerical_loader_environment"]
    relevant = {k for k in os.environ if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
    _require(relevant == {k for k in loader if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
             and all(os.environ[k] == loader[k] for k in relevant), "fixed numerical loader environment required")
    _require(all(os.environ.get(k) == "1" for k in
        ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")),
        "actual serial child must use the declared single-thread environment")
    import scipy
    _require(dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__)
             == declaration["numeric_environment"], "unchanged actual numerical environment required")
    claim = _read(root / "run_claim.json")
    _require_hash(root / "declaration.json", claim["declaration_sha256"])
    _require(os.getppid() == claim["parent_pid"], "final audit requires the actual admitted parent process")
    stages = _read(root / "AAA/stages.json")["stages"]
    _require([s["label"] for s in stages] == expected and len(stages) == 11
             and all(s["status"] == "PASS" for s in stages[:-1])
             and stages[-1]["status"] == "RUNNING"
             and stages[-1]["command"] == [sys.executable, *sys.argv],
             "all ten prior stages and the actual parent-admitted final child required")
    for stage in stages[:-1]:
        for name in ("resource_before", "resource_after"):
            resource = stage[name]
            _require(resource["resource_roots"] == declaration["resource_roots"]
                     and resource["min_free_bytes"] == declaration["min_free_bytes"]
                     and resource["artifact_budget_bytes"] == declaration["artifact_budget_bytes"]
                     and resource["artifact_bytes"] <= declaration["artifact_budget_bytes"]
                     and resource["disk_free_bytes"] >= declaration["min_free_bytes"],
                     "actual stage resource scope or cap differs")
    resources = declaration["resources_before"]
    _require(resources["artifact_bytes"] + declaration["complete_uncompressed_bound_bytes"] < 96 * 2**30
             and resources["disk_free_bytes"] - declaration["complete_uncompressed_bound_bytes"] >= 8 * 2**30,
             "complete conservative storage admission must precede the numerical run")
    watchdogs = []
    for stage in stages[:-1]:
        watchdogs.append(_watch(stage, root))
        log = root / (stage["label"] + ".log")
        _provenance(root, log, provenance)
        _provenance(root, log.with_suffix(".watchdog.json"), provenance)
    _provenance(root, root / "declaration.json", provenance)
    _provenance(root, root / "run_claim.json", provenance)
    return dict(actual_stage_entries=11, preceding_passed_stages=10, preceding_live_watchdogs=10,
        final_stage_status_at_verification="RUNNING",
        final_watchdog_and_all_PASS_checked_by_parent_after_return=True,
        maximum_preceding_sampled_rss_mib=max(w["sampled_peak_rss_mib"] for w in watchdogs),
        parent_pid=claim["parent_pid"], declaration_sha256=claim["declaration_sha256"])


def main(root=OUT):
    """Future parent-admitted final stage; checks raw data without new solves."""
    root = Path(root).resolve()
    _require(root == OUT.resolve(), "only the separately declared fixed output root is admitted")
    declaration = _read(root / "declaration.json")
    provenance = {}
    execution = _execution_contract(root, declaration, provenance)
    sources = _dependencies(declaration)
    stage_receipts = _stage_receipts(root, provenance)
    controls = _math_controls(root, provenance)
    references, model_audits = [], []
    for group in GROUPS:
        reference, audit = _reference(root, group, declaration, provenance)
        references.append(audit)
        for model in MODELS:
            model_audits.append(_model(root, group, model, reference, provenance))
        del reference
    pairs = controls["actual_case_pairs"] + sum(row["actual_case_pairs"] for row in model_audits)
    solves = controls["actual_linear_solves"] + sum(row["actual_linear_solves"] for row in model_audits)
    columns = controls["actual_source_column_solves"] + sum(row["actual_source_column_solves"] for row in model_audits)
    _require((pairs, solves, columns) == (56, 112, 3800) and len(references) == 3 and len(model_audits) == 6,
             "all observed complete scientific counters required")
    scientific = {name: value for name, value in provenance.items()
                  if name.startswith(("math_controls/", "references/", "models/"))}
    _require(len(scientific) == 395, "all 395 actual scientific and witness archive files required")
    # Recheck immutable sources and all observed outputs after deriving the
    # reports. The current stages.json/final log are deliberately omitted:
    # their finished state belongs to the parent's subsequent final seal.
    _dependencies(declaration)
    for name, wanted in provenance.items():
        _require_hash(root / name, wanted["sha256"])
        _require((root / name).stat().st_size == wanted["bytes"], "archive changed before final publication")
    result = dict(schema="AXMAT_CURRENT_LAYERED_COMPARISON_AUDIT_V1",
        classification="COMPLETE_CURRENT_FINITE_HEIGHT_COMPARISON_ONLY",
        groups=list(GROUPS), models=list(MODELS), height=20, coarse_layers=4, prescribed_subdivisions=list(LEVELS),
        actual_total_case_pairs=pairs, actual_total_linear_solves=solves,
        actual_total_source_column_solves=columns, actual_math_case_pairs=20, actual_math_linear_solves=40,
        actual_math_source_column_solves=1064, actual_model_case_pairs=36, actual_model_linear_solves=72,
        actual_model_source_column_solves=2736, actual_reference_groups=3,
        reference_source_columns_per_group=38, independent_angular_layer_units=32, fixed_positive_holdouts=6,
        actual_negative_controls=11, actual_scientific_archive_files=len(scientific),
        field_action_relative_limit=FIELD_LIMIT, cell_global_algebraic_relative_limit=BALANCE_LIMIT,
        complete_raw_fields_and_residuals_audited=True, exact_source_order_and_coverage=True,
        vacuums_exact_zero=True, positive_fields_without_clipping=True, angular_weights_rescaled=False,
        frozen_nonunit_gram_preserved=True, geometric_white_and_stored_volume_conventions_separate=True,
        source_provenance=sources, execution=execution, completed_stage_receipts=stage_receipts,
        mathematical_controls=controls, references=references, comparisons=model_audits,
        actual_archive_provenance=dict(sorted(provenance.items())),
        mathematical_program_controls_verified=True, fine_refinement_is_report_only=True,
        native_model_discrepancy_is_report_only=True, continuous_BVP_converged=False,
        continuous_BVP_qualified=False, native_response_qualified=False, native_propagation_qualified=False,
        axial_propagation_qualified=False, physical_collision_balance_assessed=False,
        scattering_fission_iteration_qualified=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        model_chosen_by_CE=False, source_or_operator_fitted=False, CE_data_used=False,
        original_accuracy_thresholds_changed=False, production_solver_changed=False,
        scope="Three selected groups, H20/Nz4, two declared algebraic hypotheses; same-discrete-program agreement and complete comparison archive only.")
    _write_new(root / "result.json", result)
    with (root / "REPORT.txt").open("x") as handle:
        handle.write("当前数据有限高度模型比较（2026-10-05）\n\n")
        handle.write("三个预选群51/61/98，20 cm/4粗层，固定8角与原始非单位Gram。\n")
        handle.write("数学控制20对/40次求解及11项负控制；六组模型比较36对/72次求解。\n")
        handle.write("共112次实际线性求解、3800个实际RHS列，395个科学归档文件逐项核验。\n")
        handle.write("全部32单位源与6固定正源、原始字段及代数残差通过原始数学门槛。\n")
        handle.write("几何白返回的物理账目与存储体积的角均值分别保留；基测试逃逸不冒充物理总逃逸。\n\n")
        for row in model_audits:
            last = row["refinements"][-1]
            error = last["native_discrepancy_per_coordinate"]["complete_angular_region_mean"]
            handle.write(f"群{row['group']} {row['model']} m32完整角/区域均值相对差范围 "
                         f"{min(error):.6e}至{max(error):.6e}（38个源列，完整数组见result.json）。\n")
        handle.write("\n全部固定细分与模型差异仅报告；不宣称连续问题已收敛、原生传播已资格或模型已选择。\n")
        handle.write("原AAA精度规则保持，AAA仍未资格，ABA未准入；最终第11个watchdog由父进程核验后封存。\n")
    print("AXMAT-LAYERED-COMPARISON-ARCHIVE-VERIFIED")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=OUT)
    arguments = parser.parse_args()
    main(arguments.root)

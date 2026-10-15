"""Helpers for a separately declared causal finite-height model comparison.

Nothing runs on import.  A caller must first freeze this program and its
dependencies, admit the completed native family, and execute serially under
the existing resource guards.  The two supplied H matrices are hypotheses;
no fitting, native propagation qualification, or AAA/ABA admission is implied.
"""

import json
from pathlib import Path

import numpy as np

from angular_collision_slab_candidate import build_slab, solve_slab, source_family
from angular_collision_slab_expanded_reference_causal import solve_expanded
from probe_refined_AAA_white_odd_response import read, require_file, verify, write_new
from white_side_trace_kernel import trace_exchange


GROUPS = (51, 61, 98)
LEVELS = (1, 2, 4, 8, 16, 32)
ANGULAR_TO_FULL = (1, 3, 5, 7, 0, 2, 4, 6)
FIELD_LIMIT = 5e-12
BALANCE_LIMIT = 1e-10
COMMON_FIELDS = (
    "fine_angular_means", "fine_angular_faces", "coarse_angular_means",
    "coarse_angular_faces", "fine_scalar_mean", "coarse_scalar_mean",
    "fine_signed_jz", "coarse_signed_jz", "fine_signed_face_jz",
    "coarse_signed_face_jz", "bottom_top_outgoing_angular_flux",
    "bottom_top_angular_escape_current", "bottom_top_escape_current",
    "vacuum_incoming_angular_flux", "effective_algebraic_sources",
    "algebraic_birth", "algebraic_collision",
)
COARSE_FIELDS = (
    "coarse_angular_means", "coarse_angular_faces", "coarse_scalar_mean",
    "coarse_signed_jz", "coarse_signed_face_jz",
    "bottom_top_angular_escape_current", "bottom_top_escape_current",
)


def _columns_relative(actual, expected):
    actual, expected = np.asarray(actual), np.asarray(expected)
    if actual.shape != expected.shape or not np.isfinite(actual).all() or not np.isfinite(expected).all():
        raise ValueError("matching finite complete fields required")
    n = expected.shape[-1]
    scale = abs(expected).reshape(-1, n).max(axis=0)
    defect = abs(actual - expected).reshape(-1, n).max(axis=0)
    if np.any((scale == 0) & (defect != 0)):
        raise ValueError("nonzero discrepancy on an exactly zero field")
    result = np.divide(defect, scale, out=np.zeros_like(defect), where=scale > 0)
    if not np.isfinite(result).all():
        raise ValueError("nonfinite complete-field discrepancy")
    return result


def _weighted_columns(actual, expected, weights):
    if actual.shape != expected.shape or weights.shape != expected.shape[:-1]:
        raise ValueError("matching complete fields and fixed measure required")
    if not all(np.isfinite(a).all() for a in (actual, expected, weights)) or np.any(weights <= 0):
        raise ValueError("finite complete fields and positive weights required")
    axes = tuple(range(weights.ndim))
    with np.errstate(over="ignore", invalid="ignore"):
        numerator = ((actual - expected)**2 * weights[..., None]).sum(axis=axes)
        denominator = (expected**2 * weights[..., None]).sum(axis=axes)
    if not np.isfinite(numerator).all() or not np.isfinite(denominator).all():
        raise ValueError("nonfinite derived field norm")
    if np.any(denominator <= 0):
        raise ValueError("positive field norm required for every source coordinate")
    value = np.sqrt(numerator / denominator)
    if not np.isfinite(value).all():
        raise ValueError("nonfinite weighted discrepancy")
    return value


def _verify_seal(root, expected_sha):
    root = Path(root).resolve()
    require_file(root / "seal.json", expected_sha)
    seal = read(root / "seal.json")
    verify({str(root / name): sha for name, sha in seal["files"].items()})
    verify(read(root / "declaration.json")["files"])
    return root


def prepare_reference(native_root, angular_root, group, output_dir, *,
                      native_seal_sha256, angular_seal_sha256):
    """Retain full angular/region/layer fields before rank1 testing.

    The native common white amplitudes use independent geometric incoming
    measure.  Angular means retain the stored-volume convention of the prior
    zero-gradient response.  These two conventions are never silently equated.
    """
    if group not in GROUPS:
        raise ValueError("only the three already selected groups are in scope")
    native_root = _verify_seal(native_root, native_seal_sha256)
    angular_root = _verify_seal(angular_root, angular_seal_sha256)
    qualified = read(native_root / "result.json")
    if (qualified["classification"] != "COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY"
            or qualified["full_current_discrete_fixed_source_qualified"] is not True
            or qualified["full_current_geometric_white_qualified"] is not True):
        raise ValueError("completed, sealed current-data finite-height family required")
    if read(angular_root / "result.json")["classification"] != "COMPLETE_CURRENT_DATA_FULL_ANGULAR_COLLISION_RESPONSE_ONLY":
        raise ValueError("completed current-data angular response required")
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=False)
    gi = GROUPS.index(group)
    with np.load(native_root / "inputs/inventory.npz", allow_pickle=False) as z:
        vol = z["weights"][:8].copy()
        zmu, wzmu = z["zmu"].copy(), z["wzmu"].copy()
        totals = z["group_totals"][gi].copy()
    with np.load(angular_root / f"angular_response_g{group}.npz", allow_pickle=False) as z:
        saved_lifting = z["source_lifting"].copy()
        b = saved_lifting[:8, 0].copy()
        saved_testing = z["testing"].copy()
        saved_gram = float(z["gram"])
        mu, omega = z["native_mu"].copy(), z["omega"].copy()
        h_reduced = z["projected_inverse"].copy()
        conditional_response = z["conditional_response"].copy()
    polar_mu = np.sqrt(1 - 1 / zmu**2)
    full_mu = np.array([s * m for m in polar_mu for s in (-1, 1)])
    full_omega = np.repeat(wzmu * zmu / 2, 2)
    permutation = np.array(ANGULAR_TO_FULL)
    if (not np.array_equal(mu, full_mu[permutation])
            or not np.array_equal(omega, full_omega[permutation]) or np.any(b <= 0)
            or not np.array_equal(saved_lifting, np.kron(np.eye(8), b[:, None]))):
        raise ValueError("native angular identity or frozen positive rank1 basis differs")
    # Preserve the previously used sequential arithmetic and nonunit Gram.
    total_volume = sum(float(v) for v in vol)
    radial_weights = vol / total_volume
    gram, tau = 0.0, 0.0
    for w, v, t in zip(radial_weights, b, totals, strict=True):
        gram += float(w) * float(v) * float(v)
        tau += float(w) * float(v) * float(v) * float(t)
    testing = radial_weights * b / gram
    if gram != saved_gram or not np.array_equal(saved_testing, np.kron(np.eye(8), testing[None, :])):
        raise ValueError("fixed basis testing or exact nonunit Gram differs")
    trace = trace_exchange(mu, 2 * omega, 6 * .61776479, total_volume)
    h_trace = (tau * np.eye(8) + b[0]**2 * trace) / gram
    if np.max(abs(h_trace @ conditional_response - np.eye(8))) >= FIELD_LIMIT:
        raise ValueError("declared trace hypothesis differs from the prior conditional response")
    family = source_family(mu)
    sources = family["sources"]
    coefficients = sources.reshape(32, -1)
    lift = np.zeros((256, 32))
    for a, s in enumerate(ANGULAR_TO_FULL):
        for r in range(8):
            for layer in range(4):
                lift[s * 32 + r * 4 + layer, a * 4 + layer] = b[r]
    polar_operators = []
    for p in range(4):
        with np.load(native_root / f"verification/p{p}_h20_n4/operators.npz", allow_pickle=False) as z:
            if not np.array_equal(z["coverage"], np.ones_like(z["coverage"])):
                raise ValueError("complete original-record coverage required")
            # order32, selected group, independent sign, planar orientation.
            polar_operators.append(z["operators"][1, gi].sum(axis=1))
    operator = np.concatenate(polar_operators, axis=0)
    if operator.shape != (8, 72, 66):
        raise ValueError("complete native finite-height operator dimensions differ")
    with np.load(native_root / f"white/h20_n4/g{group}_q32.npz", allow_pickle=False) as z:
        amplitudes = z["white_amplitudes"][:, :256] @ lift @ coefficients
        saved_phi = z["white_phi"][:, :256] @ lift @ coefficients
        saved_jz = z["white_jz"][:, :256] @ lift @ coefficients
    with np.load(native_root / "white/h20_n4/geometry.npz", allow_pickle=False) as z:
        geometric_volume, geometric_radial = z["volume"].copy(), z["radial"].copy()
        geometric_mu = z["mu"].copy()
        stored_volume = z["stored_volume"].copy()
    if not np.array_equal(geometric_mu, full_mu) or not np.array_equal(stored_volume, np.repeat(vol * 5, 4)):
        raise ValueError("native geometric state order or stored-volume convention differs")
    x = np.zeros((8, 66, coefficients.shape[1]))
    x[:, :32] = (lift @ coefficients).reshape(8, 32, -1)
    x[:, 32:56] = amplitudes[None, :, :]
    y = np.einsum("srk,skc->src", operator, x, optimize=True)
    # Retain the returned native action before judging its reconstruction.
    with (output_dir / "raw_native_action.npz").open("xb") as handle:
        np.savez_compressed(handle, operator=operator, inputs=x, outputs=y,
            angular_to_full=permutation, source_lifting=lift, source_coefficients=coefficients,
            sources=sources, mu=mu, omega=omega, basis=b, gram=gram, volume=vol,
            geometric_volume=geometric_volume, geometric_radial=geometric_radial,
            stored_volume=stored_volume, saved_phi=saved_phi, saved_jz=saved_jz)
    integrals = y[:, :32]
    reconstruction = dict(
        scalar=_columns_relative(integrals.sum(axis=0) / stored_volume[:, None], saved_phi),
        signed_jz=_columns_relative(
            np.einsum("s,src->rc", full_mu, integrals) / stored_volume[:, None], saved_jz
        ),
    )
    if max(float(v.max()) for v in reconstruction.values()) >= FIELD_LIMIT or np.any(y < 0):
        raise ValueError("independent full angular field reconstruction failed")
    birth = np.einsum("sr,src->c", geometric_volume, x[:, :32])
    collision = (integrals * np.repeat(totals, 4)[None, :, None]).sum(axis=(0, 1))
    physical_escape = y[:, 56:].sum(axis=(0, 1))
    physical_defect = birth - collision - physical_escape
    closure_defect = y[:, 32:56].sum(axis=0) - geometric_radial.sum(axis=0)[:, None] * amplitudes
    if (not all(np.isfinite(v).all() for v in (
            birth, collision, physical_escape, physical_defect, closure_defect, y, amplitudes
        )) or np.any(birth <= 0)):
        raise ValueError("nonfinite native physical ledger or nonpositive birth")
    balance_relative = abs(physical_defect) / birth
    if (not np.isfinite(balance_relative).all() or np.max(balance_relative) >= BALANCE_LIMIT
            or np.max(_columns_relative(y[:, 32:56].sum(axis=0),
                geometric_radial.sum(axis=0)[:, None] * amplitudes)) >= FIELD_LIMIT):
        raise ValueError("unchanged native physical balance or common-white closure failed")
    complete = integrals[permutation].reshape(8, 8, 4, -1)
    complete = complete / (omega[:, None, None, None] * vol[None, :, None, None] * 5)
    projected = np.einsum("r,srzc->szc", testing, complete)
    discarded = complete - b[None, :, None, None] * projected[:, None]
    end_escape = y[permutation, 56:].reshape(8, 2, 8, -1)
    end_escape = end_escape / (omega[:, None, None, None] * vol[None, None, :, None])
    projected_escape = np.einsum("r,sbrc->bsc", testing, end_escape)
    field_weights = omega[:, None, None] * radial_weights[None, :, None] * np.full((1, 1, 4), 5.)
    offspace = _weighted_columns(complete - discarded, complete, field_weights)
    with (output_dir / "reference.npz").open("xb") as handle:
        np.savez_compressed(handle, mu=mu, omega=omega, basis=b,
        radial_weights=radial_weights, gram=gram, tau=tau, H_trace=h_trace, H_reduced=h_reduced,
        sources=sources, source_lifting=lift, source_coefficients=coefficients,
        native_operator=operator, native_input=x, native_output=y, native_white_amplitudes=amplitudes,
        native_complete_angular_means=complete, native_projected_angular_means=projected,
        native_discarded_angular_means=discarded, native_projected_angular_escape=projected_escape,
        native_projected_signed_jz=np.einsum("s,szc->zc", omega * mu, projected),
        native_complete_field_weights=field_weights, native_field_offspace=offspace,
        raw_native_physical_birth=birth, raw_native_collision=collision,
        raw_native_physical_escape=physical_escape, raw_native_physical_defect=physical_defect,
        raw_native_white_closure_defect=closure_defect,
        native_scalar_reconstruction_relative=reconstruction["scalar"],
        native_signed_jz_reconstruction_relative=reconstruction["signed_jz"])
    write_new(output_dir / "reference.json", dict(schema="AXMAT_LAYERED_PROJECTED_REFERENCE_V1",
        group=group, height=20, coarse_layers=4, actual_source_columns=sources.shape[-1],
        source_labels=family["labels"], all_32_coordinates_and_6_positive_controls=True,
        angular_to_full_permutation=list(ANGULAR_TO_FULL), gram=gram,
        full_fields_retained_before_projection=True, geometric_white_incoming_measure=True,
        angular_mean_convention="omega times stored native region volume times 5 cm",
        escape_comparison="basis-tested angular outgoing current; distinct from physical total escape",
        candidate_discrepancy_scope="combined hypothesis, kernel and white-return convention differences",
        native_reconstruction_max=max(float(v.max()) for v in reconstruction.values()),
        native_physical_balance_max=float(np.max(abs(physical_defect) / birth)),
        native_seal_sha256=native_seal_sha256, angular_seal_sha256=angular_seal_sha256,
        original_accuracy_thresholds_changed=False, axial_propagation_qualified=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))


def _check_fields(fields, sources, subdivisions):
    n, k = 4 * subdivisions, sources.shape[-1]
    shapes = dict(fine_angular_means=(8, n, k), fine_angular_faces=(8, n + 1, k),
        coarse_angular_means=(8, 4, k), coarse_angular_faces=(8, 5, k),
        fine_scalar_mean=(n, k), coarse_scalar_mean=(4, k), fine_signed_jz=(n, k),
        coarse_signed_jz=(4, k), fine_signed_face_jz=(n + 1, k),
        coarse_signed_face_jz=(5, k), bottom_top_outgoing_angular_flux=(2, 8, k),
        bottom_top_angular_escape_current=(2, 8, k), bottom_top_escape_current=(2, k),
        vacuum_incoming_angular_flux=(8, k), effective_algebraic_sources=(8, n, k),
        algebraic_birth=(k,), algebraic_collision=(k,))
    for name, shape in shapes.items():
        if fields[name].shape != shape or not np.isfinite(fields[name]).all():
            raise ValueError("complete finite candidate field required: " + name)
    if (not np.array_equal(fields["external_sources"], sources)
            or not np.array_equal(fields["fine_external_sources"], np.repeat(sources, subdivisions, axis=1))):
        raise ValueError("candidate source columns or layer lift differ")
    for name, value in fields["diagnostics"].items():
        if not np.isfinite(value).all():
            raise ValueError("nonfinite candidate diagnostic")
        if name.endswith("_relative"):
            limit = BALANCE_LIMIT if name in (
                "full_directional_cell_equation_relative", "raw_algebraic_balance_relative"
            ) else FIELD_LIMIT
            if np.max(value) >= limit:
                raise ValueError("original independent-program residual screen failed: " + name)
    for name in ("fine_angular_means", "fine_angular_faces", "effective_algebraic_sources"):
        if np.min(fields[name]) < 0:
            raise ValueError("positive external source produced a negative candidate field")
    if np.any(fields["vacuum_incoming_angular_flux"] != 0):
        raise ValueError("incoming vacuum face is nonzero")


def _save_fields(path, system, fields, role):
    arrays = {}
    arrays.update({role + "_" + k: v for k, v in fields.items() if isinstance(v, np.ndarray)})
    arrays.update({role + "_diagnostic_" + k: np.asarray(v) for k, v in fields["diagnostics"].items()})
    if role == "expanded":
        for name in ("expanded_matrix", "expanded_solve_matrix"):
            matrix = fields[name].tocsc(copy=False)
            arrays.update({name + "_data": matrix.data, name + "_indices": matrix.indices,
                name + "_indptr": matrix.indptr, name + "_shape": np.array(matrix.shape),
                name + "_format": np.asarray("csc")})
    else:
        arrays.update({"candidate_system_" + k: v for k, v in system.items() if isinstance(v, np.ndarray)})
        for angle, sweep in enumerate(system["sweeps"]):
            arrays.update({f"candidate_sweep_{angle}_" + k: v for k, v in sweep.items()
                if isinstance(v, np.ndarray)})
    with Path(path).open("xb") as handle:
        np.savez_compressed(handle, **arrays)
    metadata = {k: v for k, v in fields.items() if isinstance(v, (str, bool, int, float)) or v is None}
    if role == "expanded":
        metadata["expanded_factorization"] = fields["expanded_factorization"]
    metadata.update(schema="AXMAT_LAYERED_CANDIDATE_RETURN_V1", role=role,
        source_columns=fields["external_sources"].shape[-1],
        fine_layers=fields["fine_angular_means"].shape[1],
        sparse_format="csc" if role == "expanded" else None,
        archive_scope="all ndarray fields, diagnostics, scalar metadata, original/actual sparse systems, factorization settings and candidate sweep arrays")
    write_new(Path(path).with_suffix(".metadata.json"), metadata)


def compare_model(reference_dir, model, output_dir):
    """All six preset refinements; report errors without a convergence claim."""
    if model not in ("trace", "reduced"):
        raise ValueError("only the two independently declared hypotheses are supported")
    with np.load(Path(reference_dir) / "reference.npz", allow_pickle=False) as z:
        mu, omega, h = z["mu"].copy(), z["omega"].copy(), z["H_" + model].copy()
        q, b = z["sources"].copy(), z["basis"].copy()
        complete = z["native_complete_angular_means"].copy()
        reduced = z["native_projected_angular_means"].copy()
        native_escape = z["native_projected_angular_escape"].copy()
        native_jz = z["native_projected_signed_jz"].copy()
        complete_weights = z["native_complete_field_weights"].copy()
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=False)
    reports, previous = [], None
    reduced_weights = omega[:, None] * np.full((1, 4), 5.)
    for m in LEVELS:
        system = build_slab(mu, h, 20., angular_weights=omega, subdivisions=m)
        candidate = solve_slab(system, q)
        _save_fields(output_dir / f"subdivisions_{m:02d}_candidate.npz", system, candidate, "candidate")
        expanded = solve_expanded(mu, h, 20., angular_weights=omega, subdivisions=m, sources=q)
        _save_fields(output_dir / f"subdivisions_{m:02d}_expanded.npz", system, expanded, "expanded")
        write_new(output_dir / f"subdivisions_{m:02d}_decimal.json", dict(
            schema="AXMAT_LAYERED_DECIMAL_WITNESSES_V1", precision=expanded["decimal_precision"],
            angle_count=8, witnesses=expanded["decimal_primitive_witnesses"]))
        _check_fields(candidate, q, m)
        _check_fields(expanded, q, m)
        independent = {name: _columns_relative(candidate[name], expanded[name]) for name in COMMON_FIELDS}
        if max(float(v.max()) for v in independent.values()) >= FIELD_LIMIT:
            raise ValueError("independent complete expanded-equation field screen failed")
        lifted = b[None, :, None, None] * candidate["coarse_angular_means"][:, None]
        errors = dict(
            projected_angular_mean=_weighted_columns(candidate["coarse_angular_means"], reduced, reduced_weights),
            complete_angular_region_mean=_weighted_columns(lifted, complete, complete_weights),
            basis_tested_signed_jz=_columns_relative(candidate["coarse_signed_jz"], native_jz),
            basis_tested_outgoing_angular_current=_columns_relative(
                candidate["bottom_top_angular_escape_current"], native_escape
            ),
        )
        changes = {} if previous is None else {
            name: _columns_relative(candidate[name], previous[name]) for name in COARSE_FIELDS
        }
        reports.append(dict(subdivisions=m, independent_complete_field_max={
            k: float(v.max()) for k, v in independent.items()}, native_discrepancy_per_coordinate={
            k: v.tolist() for k, v in errors.items()}, change_from_previous_per_coordinate={
            k: v.tolist() for k, v in changes.items()},
            minimum_angular_mean=float(candidate["fine_angular_means"].min()),
            minimum_angular_face=float(candidate["fine_angular_faces"].min()),
            candidate_source_columns=candidate["external_sources"].shape[-1],
            expanded_source_columns=expanded["external_sources"].shape[-1],
            actual_returned_linear_solves=2,
            numerical_program_checks_passed=True))
        previous = {name: candidate[name].copy() for name in COARSE_FIELDS}
        del system, candidate, expanded
    write_new(output_dir / "result.json", dict(schema="AXMAT_LAYERED_PROPAGATION_COMPARISON_V1",
        model=model, height=20, coarse_layers=4, actual_returned_linear_solves=2 * len(reports),
        actual_source_column_solves=2 * q.shape[-1] * len(reports),
        prescribed_subdivisions=LEVELS, source_columns=q.shape[-1], refinements=reports,
        all_prescribed_levels_executed=True, fine_refinement_is_report_only=True,
        continuous_BVP_converged=False, native_propagation_qualified=False,
        model_chosen_by_CE=False, original_accuracy_thresholds_changed=False,
        physical_collision_balance_assessed=False, scattering_fission_iteration_qualified=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))

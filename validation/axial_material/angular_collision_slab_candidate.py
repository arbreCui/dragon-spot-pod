"""Unqualified eight-angle fixed-source slab candidate.

The explicitly supplied matrix H defines the candidate equation

    mu_s * d_z a_s + sum_t H[s,t] * a_t = q_s.

H is an algebraic angular collision/coupling matrix.  Neither its diagonal
nor its off-diagonal entries are identified with physical reaction data.
In particular, an inverse of a measured zero-gradient response does not
uniquely identify this propagation law.  This module reads no experiment or
CE data and performs no fitting, clipping, or normalization repair.

External sources are constant in each of four coarse layers.  Equal internal
subdivision applies a constant-cell-source characteristic discretization to
the angular coupling.  All fine-layer angular means are solved simultaneously;
fine means and shared faces remain available before conservative restriction.
The coupling's within-subcell source approximation must be assessed by a
separately declared internal refinement and independent expanded-equation
comparison.  No accuracy, physics, or production qualification is implied.

All arrays use angular-major/layer-inner order.  Explicit angular weights are
required for currents and algebraic ledgers; their values are never rescaled.
No command-line entry point or import-time numerical calculation is provided.
"""

import math

import numpy as np


N_ANGLE = 8
N_COARSE = 4


def _coefficient_family(length, attenuation):
    """Exact primitives and directly evaluated cell-mean coefficients.

    These formulas follow the previously checked S2 cell-characteristic
    implementation.  That earlier check does not qualify this eight-angle
    source elimination or any supplied H matrix.
    """
    length, attenuation = np.broadcast_arrays(
        np.asarray(length, dtype=float), np.asarray(attenuation, dtype=float)
    )
    if (
        np.any(length <= 0)
        or np.any(attenuation < 0)
        or not np.isfinite(length).all()
        or not np.isfinite(attenuation).all()
    ):
        raise ValueError("finite positive lengths and nonnegative attenuation required")
    tau = length * attenuation
    if not np.isfinite(tau).all():
        raise ValueError("finite optical lengths required")
    transmission = np.exp(-tau)
    mean_incoming = np.divide(
        -np.expm1(-tau), tau, out=np.ones_like(tau), where=tau > 0
    )
    x = np.where(tau <= 0.5, tau, 0.0)
    series = np.polynomial.polynomial.polyval(
        x, [(-1.0) ** k / math.factorial(k + 2) for k in range(19)]
    )
    safe = np.where(attenuation > 0, attenuation, 1.0)
    mean_source = np.where(
        tau <= 0.5, length * series, (1 - mean_incoming) / safe
    )
    b = length * mean_incoming
    d = length * mean_source
    if not all(np.isfinite(v).all() for v in (
        transmission, b, d, mean_incoming, mean_source
    )):
        raise ValueError("finite characteristic primitives required")
    return transmission, b, d, mean_incoming, mean_source


def coefficients(length, attenuation):
    """Return T/B/D; an unrepresentably small raw D may round to zero.

    Cell means use directly evaluated B/L and D/L, preserving representable
    mean coefficients even when the corresponding unnormalized primitive
    underflows.  A positive optical length that underflows uses its zero
    optical-length limit without losing the represented geometric length.
    """
    transmission, b, d, _, _ = _coefficient_family(length, attenuation)
    return transmission, b, d


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(name + " must be a positive integer")
    if value < 1:
        raise ValueError(name + " must be a positive integer")
    return int(value)


def _sweep(widths, mu, attenuation):
    """Directional cell-mean/face response to each fine-cell source."""
    n = len(widths)
    lengths = widths / abs(mu)
    transmission, b, d, mean_incoming, mean_source = _coefficient_family(
        lengths, attenuation
    )
    means = np.zeros((n, n))
    faces = np.zeros((n + 1, n))
    indices = range(n) if mu > 0 else range(n - 1, -1, -1)
    for i in indices:
        incoming, outgoing = (i, i + 1) if mu > 0 else (i + 1, i)
        means[i] = mean_incoming[i] * faces[incoming]
        means[i, i] += mean_source[i]
        faces[outgoing] = transmission[i] * faces[incoming]
        faces[outgoing, i] += b[i]
    return dict(
        means=means, faces=faces, lengths=lengths,
        transmission=transmission, B=b, D=d,
        mean_incoming=mean_incoming, mean_source=mean_source,
    )


def build_slab(mu, angular_collision, height, *, angular_weights,
               coarse_layers=N_COARSE, subdivisions=1):
    """Assemble a candidate with vacuum incoming axial faces.

    ``angular_collision`` is the complete supplied H (8 by 8), constant in
    height.  Negative diagonal attenuation or positive off-diagonal H entries
    are rejected, rather than repaired.  Nonnegative row sums, positivity of
    the final response, and invertibility are not silently presumed.

    The source-to-mean flight P is block diagonal by angle.  C=-offdiag(H)
    couples angles within each fine layer.  The full linear system is
    (I-P*C)*a=P*q.  This is a cell-source discretization of the candidate
    equation, not an exact finite-height native flight or matrix-exponential
    propagation of an arbitrary H.
    """
    coarse_layers = _positive_integer(coarse_layers, "coarse_layers")
    subdivisions = _positive_integer(subdivisions, "subdivisions")
    if coarse_layers != N_COARSE:
        raise ValueError("this undeclared candidate supports exactly four coarse layers")
    mu = np.array(mu, dtype=float, copy=True)
    h_matrix = np.array(angular_collision, dtype=float, copy=True)
    weights = np.array(angular_weights, dtype=float, copy=True)
    if mu.shape != (N_ANGLE,) or weights.shape != (N_ANGLE,):
        raise ValueError("eight explicit directional cosines and weights required")
    if (
        not np.isfinite(mu).all()
        or np.any(mu == 0)
        or np.any(abs(mu) >= 1)
        or np.count_nonzero(mu > 0) != N_ANGLE // 2
        or np.count_nonzero(mu < 0) != N_ANGLE // 2
    ):
        raise ValueError("four positive and four negative finite interior cosines required")
    if (
        not np.isfinite(weights).all()
        or np.any(weights <= 0)
        or not np.isfinite(weights.sum())
    ):
        raise ValueError("positive finite explicit angular weights required")
    if h_matrix.shape != (N_ANGLE, N_ANGLE) or not np.isfinite(h_matrix).all():
        raise ValueError("complete finite eight-by-eight algebraic H required")
    attenuation = np.diag(h_matrix).copy()
    off_diagonal = h_matrix.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    if np.any(attenuation < 0) or np.any(off_diagonal > 0):
        raise ValueError("H requires nonnegative diagonal and nonpositive off-diagonal entries")
    height = float(height)
    if not np.isfinite(height) or height <= 0:
        raise ValueError("finite positive slab height required")
    n = coarse_layers * subdivisions
    widths = np.full(n, height / n)
    if np.any(widths <= 0):
        raise ValueError("positive represented subcell widths required")
    sweeps = tuple(_sweep(widths, m, d) for m, d in zip(mu, attenuation, strict=True))
    flight = np.zeros((N_ANGLE * n, N_ANGLE * n))
    for angle, sweep in enumerate(sweeps):
        block = slice(angle * n, (angle + 1) * n)
        flight[block, block] = sweep["means"]
    coupling = np.kron(-off_diagonal, np.eye(n))
    matrix = np.eye(N_ANGLE * n) - flight @ coupling
    if not all(np.isfinite(a).all() for a in (flight, coupling, matrix)):
        raise ValueError("finite assembled candidate matrices required")
    return dict(
        mu=mu, angular_weights=weights, H=h_matrix,
        diagonal_attenuation=attenuation, angular_algebraic_coupling=-off_diagonal,
        height=height, coarse_layers=coarse_layers, subdivisions=subdivisions,
        fine_layers=n, fine_widths=widths,
        coarse_widths=np.full(coarse_layers, height / coarse_layers),
        sweeps=sweeps, flight=flight, coupling=coupling, matrix=matrix,
        algebraic_row_sums=h_matrix.sum(axis=1),
        axial_incoming_is_vacuum=True,
        axial_propagation_qualified=False,
    )


def source_family(mu, coarse_layers=N_COARSE):
    """All 32 angular/layer units plus six fixed positive source combinations.

    Holdouts are prescribed before any H-dependent solve.  They are not
    selected using errors, experiments, or CE.  A caller must compare an
    independently solved holdout against assembled unit responses before
    claiming a separate source-assembly verification.
    """
    mu = np.asarray(mu, dtype=float)
    if mu.shape != (N_ANGLE,) or not np.isfinite(mu).all() or np.any(abs(mu) >= 1):
        raise ValueError("eight finite interior directional cosines required")
    coarse_layers = _positive_integer(coarse_layers, "coarse_layers")
    if coarse_layers != N_COARSE:
        raise ValueError("four coarse layers required")
    ncoord = N_ANGLE * coarse_layers
    units = np.eye(ncoord).reshape(N_ANGLE, coarse_layers, ncoord)
    z = (np.arange(coarse_layers, dtype=float) + 0.5) / coarse_layers
    one = np.ones((N_ANGLE, coarse_layers))
    angular_plus = np.broadcast_to(1 + 0.5 * mu[:, None], one.shape)
    angular_minus = np.broadcast_to(1 - 0.5 * mu[:, None], one.shape)
    axial_plus = np.broadcast_to(1 + z[None, :], one.shape)
    axial_minus = np.broadcast_to(2 - z[None, :], one.shape)
    mixed = (
        1 + 0.25 * mu[:, None] + 0.1 * (3 * mu[:, None] ** 2 - 1) / 2
    ) * (1 + 0.5 * z[None, :])
    holdouts = np.stack(
        [one, angular_plus, angular_minus, axial_plus, axial_minus, mixed], axis=-1
    )
    labels = tuple(
        f"angle_{a + 1}_layer_{layer + 1}"
        for a in range(N_ANGLE) for layer in range(coarse_layers)
    ) + (
        "uniform", "positive_odd_plus", "positive_odd_minus",
        "axial_ramp_plus", "axial_ramp_minus", "positive_mixed",
    )
    return dict(
        sources=np.concatenate([units, holdouts], axis=-1),
        labels=labels, unit_coordinates=ncoord,
        holdout_unit_coefficients=holdouts.reshape(ncoord, len(labels) - ncoord),
    )


def _relative_max(defect, scale, axes):
    """An exactly zero scale accepts only an exactly zero defect."""
    defect, scale = np.broadcast_arrays(abs(defect), np.asarray(scale))
    if (not np.isfinite(defect).all() or not np.isfinite(scale).all()
            or np.any(scale < 0)):
        raise ValueError("finite defects and nonnegative finite scales required")
    values = np.divide(defect, scale, out=np.zeros_like(defect), where=scale > 0)
    values[(scale == 0) & (defect != 0)] = np.inf
    return np.max(values, axis=axes)


def solve_slab(system, sources=None):
    """Solve all supplied source columns and retain the raw candidate fields.

    ``sources`` has shape (8,4,k).  The default is the full declared source
    family.  Finite signed linear probes are supported, but positivity
    diagnostics only have a positive-source interpretation when a column is
    nonnegative.  No result is clipped and no accuracy threshold is applied.
    """
    labels = None
    if sources is None:
        family = source_family(system["mu"], system["coarse_layers"])
        sources, labels = family["sources"], family["labels"]
    sources = np.array(sources, dtype=float, copy=True)
    coarse, n, subdivisions = (
        system["coarse_layers"], system["fine_layers"], system["subdivisions"]
    )
    if (
        sources.ndim != 3
        or sources.shape[:2] != (N_ANGLE, coarse)
        or sources.shape[-1] < 1
        or not np.isfinite(sources).all()
    ):
        raise ValueError("finite source columns of shape (8,4,k) required")
    k = sources.shape[-1]
    fine_source = np.repeat(sources, subdivisions, axis=1)
    source_flat = fine_source.reshape(N_ANGLE * n, k)
    rhs = system["flight"] @ source_flat
    solved_flat = np.linalg.solve(system["matrix"], rhs)
    effective_flat = source_flat + system["coupling"] @ solved_flat
    recovered_flat = system["flight"] @ effective_flat
    angular = solved_flat.reshape(N_ANGLE, n, k)
    effective = effective_flat.reshape(N_ANGLE, n, k)
    faces = np.stack([
        sweep["faces"] @ effective[angle]
        for angle, sweep in enumerate(system["sweeps"])
    ])
    if not all(np.isfinite(a).all() for a in (rhs, angular, effective, faces)):
        raise ValueError("candidate solve produced a nonfinite field")
    fine_widths = system["fine_widths"]
    restriction_weights = (
        fine_widths.reshape(coarse, subdivisions)
        / system["coarse_widths"][:, None]
    )
    coarse_angular = (
        angular.reshape(N_ANGLE, coarse, subdivisions, k)
        * restriction_weights[None, :, :, None]
    ).sum(axis=2)
    coarse_faces = faces[:, ::subdivisions, :]
    weights, mu = system["angular_weights"], system["mu"]
    phi_fine = np.einsum("s,szk->zk", weights, angular)
    jz_fine = np.einsum("s,szk->zk", weights * mu, angular)
    phi_coarse = np.einsum("s,szk->zk", weights, coarse_angular)
    jz_coarse = np.einsum("s,szk->zk", weights * mu, coarse_angular)
    jz_faces = np.einsum("s,sfk->fk", weights * mu, faces)
    outgoing_angles = np.stack([
        faces[:, 0] * (mu < 0)[:, None],
        faces[:, -1] * (mu > 0)[:, None],
    ])
    angular_escape = abs(mu)[None, :, None] * outgoing_angles
    escape = np.einsum("s,bsk->bk", weights, angular_escape)
    characteristic_faces = np.zeros_like(angular)
    characteristic_means = np.zeros_like(angular)
    characteristic_scale = np.zeros_like(angular)
    incoming_angles = np.zeros((N_ANGLE, k))
    for angle, sweep in enumerate(system["sweeps"]):
        if mu[angle] > 0:
            incoming, outgoing = faces[angle, :-1], faces[angle, 1:]
            incoming_angles[angle] = faces[angle, 0]
        else:
            incoming, outgoing = faces[angle, 1:], faces[angle, :-1]
            incoming_angles[angle] = faces[angle, -1]
        characteristic_faces[angle] = outgoing - (
            sweep["transmission"][:, None] * incoming
            + sweep["B"][:, None] * effective[angle]
        )
        characteristic_means[angle] = angular[angle] - (
            sweep["mean_incoming"][:, None] * incoming
            + sweep["mean_source"][:, None] * effective[angle]
        )
        characteristic_scale[angle] = (
            abs(incoming) + sweep["lengths"][:, None] * abs(effective[angle])
        )
    h_action = np.einsum("st,tzk->szk", system["H"], angular)
    streaming = mu[:, None, None] * np.diff(faces, axis=1)
    equation_defect = streaming + fine_widths[None, :, None] * (h_action - fine_source)
    equation_scale = (
        abs(streaming)
        + fine_widths[None, :, None] * (abs(h_action) + abs(fine_source))
    )
    algebraic_birth = np.einsum("s,z,szk->k", weights, fine_widths, fine_source)
    algebraic_collision = np.einsum("s,z,szk->k", weights, fine_widths, h_action)
    algebraic_balance_defect = escape.sum(axis=0) + algebraic_collision - algebraic_birth
    algebraic_balance_scale = (
        abs(escape).sum(axis=0)
        + np.einsum("s,z,szk->k", weights, fine_widths, abs(h_action) + abs(fine_source))
    )
    matrix_defect = system["matrix"] @ solved_flat - rhs
    mean_reconstruction = recovered_flat - solved_flat
    derived = (
        coarse_angular, coarse_faces, phi_fine, jz_fine, phi_coarse, jz_coarse,
        jz_faces, outgoing_angles, angular_escape, escape, characteristic_faces,
        characteristic_means, characteristic_scale, incoming_angles, h_action,
        streaming, equation_defect, equation_scale, algebraic_birth,
        algebraic_collision, algebraic_balance_defect, algebraic_balance_scale,
        matrix_defect, mean_reconstruction,
    )
    if not all(np.isfinite(value).all() for value in derived):
        raise ValueError("candidate derived fields or algebraic ledgers are nonfinite")
    diagnostics = dict(
        matrix_residual_relative=_relative_max(matrix_defect, abs(rhs).max(axis=0), 0),
        reconstructed_mean_relative=_relative_max(
            mean_reconstruction, abs(solved_flat).max(axis=0), 0
        ),
        characteristic_face_relative=_relative_max(
            characteristic_faces, characteristic_scale, (0, 1)
        ),
        characteristic_mean_relative=_relative_max(
            characteristic_means, characteristic_scale, (0, 1)
        ),
        full_directional_cell_equation_relative=_relative_max(
            equation_defect, equation_scale, (0, 1)
        ),
        raw_algebraic_balance_relative=_relative_max(
            algebraic_balance_defect, algebraic_balance_scale, ()
        ),
        vacuum_incoming_absolute=abs(incoming_angles).max(axis=0),
        minimum_angular_mean=angular.min(axis=(0, 1)),
        minimum_angular_face=faces.min(axis=(0, 1)),
        minimum_coarse_angular_mean=coarse_angular.min(axis=(0, 1)),
        minimum_effective_algebraic_source=effective.min(axis=(0, 1)),
        external_source_column_nonnegative=np.all(sources >= 0, axis=(0, 1)),
        angular_weights_sum=float(weights.sum()),
    )
    if not all(np.isfinite(value).all() for value in diagnostics.values()):
        raise ValueError("candidate diagnostics are nonfinite")
    return dict(
        source_labels=labels, external_sources=sources, fine_external_sources=fine_source,
        fine_angular_means=angular, fine_angular_faces=faces,
        coarse_angular_means=coarse_angular, coarse_angular_faces=coarse_faces,
        fine_scalar_mean=phi_fine, coarse_scalar_mean=phi_coarse,
        fine_signed_jz=jz_fine, coarse_signed_jz=jz_coarse,
        fine_signed_face_jz=jz_faces, coarse_signed_face_jz=jz_faces[::subdivisions],
        bottom_top_outgoing_angular_flux=outgoing_angles,
        bottom_top_angular_escape_current=angular_escape,
        bottom_top_escape_current=escape,
        vacuum_incoming_angular_flux=incoming_angles,
        effective_algebraic_sources=effective,
        algebraic_birth=algebraic_birth, algebraic_collision=algebraic_collision,
        raw_algebraic_balance_defect=algebraic_balance_defect,
        raw_algebraic_balance_scale=algebraic_balance_scale,
        raw_matrix_residual=matrix_defect,
        raw_mean_reconstruction_defect=mean_reconstruction,
        raw_characteristic_face_defect=characteristic_faces,
        raw_characteristic_mean_defect=characteristic_means,
        raw_characteristic_scale=characteristic_scale,
        raw_directional_cell_equation_defect=equation_defect,
        raw_directional_cell_equation_scale=equation_scale,
        diagnostics=diagnostics,
        model_scope="unqualified declared algebraic eight-angle slab candidate",
        internal_coupling_is_cell_mean_source=True,
        physical_collision_balance_assessed=False,
        axial_propagation_qualified=False,
        scattering_fission_iteration_qualified=False,
        AAA_accuracy_qualified=False,
        ABA_admitted=False,
    )

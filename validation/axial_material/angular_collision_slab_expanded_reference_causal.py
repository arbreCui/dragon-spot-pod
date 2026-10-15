"""Independent expanded equations with an explicitly recorded causal ordering.

This module solves the SAME constant-subcell angular-coupling discretization
as the slab candidate, retaining every angular cell mean and shared face as
an independent unknown.  It is not a continuous boundary-value reference, a
native finite-height truth, or physical/coupled AAA qualification.

It does not import the candidate or use its primitives, sweeps, flight matrix,
coupling matrix, or eliminated system.  T/B/D are independently evaluated
using 80-digit standard-library Decimal arithmetic.  NumPy/SciPy are used for
array handling, expanded sparse assembly, and the direct solve.  Each angle's
vacuum equation and unknown come first, followed by cell mean and outgoing
face pairs in upwind cell order.  SuperLU receives this explicit row/column
ordering with natural columns, no threshold pivoting, and no equilibration.
The supplied equation coefficients, right-hand side, and solved fields are
never clipped or amended to impose an expected zero or positive value.  Both
the original and actual permuted systems and solutions are returned.  No
numerical action occurs on import, and no command-line entry point is provided.

The declared equation is mu*d_z a + H*a = q.  H is an explicitly supplied
algebraic angular matrix; no entry is called physical scattering data.  Sources
are constant in four coarse layers and are repeated over their equal internal
subcells.  Angular ordering and weights are explicit and never repaired.
"""

from decimal import Decimal, localcontext
from functools import lru_cache

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu


N_ANGLE = 8
N_COARSE = 4
DECIMAL_PRECISION = 80


def _positive_integer(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(name + " must be a positive integer")
    if value < 1:
        raise ValueError(name + " must be a positive integer")
    return int(value)


@lru_cache(maxsize=128)
def _decimal_integrals(length, attenuation):
    """Return T/B/D and normalized B/L,D/L with Decimal witnesses.

    B=int_0^L exp(-d*x) dx and D=int_0^L (L-x)*exp(-d*x) dx.
    For optical length <=1, convergent integral series are accumulated until
    both sums cease changing at the 80-digit working precision.  This is not
    the candidate's binary64 fixed polynomial.  Otherwise direct Decimal
    integral identities avoid cancellation.  The void limit is exact before
    conversion back to binary64.
    """
    length, attenuation = float(length), float(attenuation)
    if (
        not np.isfinite(length)
        or length <= 0
        or not np.isfinite(attenuation)
        or attenuation < 0
        or not np.isfinite(length * attenuation)
    ):
        raise ValueError("finite positive length and nonnegative finite attenuation required")
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        l = Decimal.from_float(length)
        d = Decimal.from_float(attenuation)
        tau = l * d
        if d == 0:
            transmission, b, integral_d = Decimal(1), l, l * l / 2
        else:
            transmission = (-tau).exp()
            if tau <= 1:
                b_sum = b_term = Decimal(1)
                d_sum = d_term = Decimal(1) / 2
                for order in range(1, 10001):
                    b_term = b_term * (-tau) / Decimal(order + 1)
                    d_term = d_term * (-tau) / Decimal(order + 2)
                    old_b, old_d = b_sum, d_sum
                    b_sum += b_term
                    d_sum += d_term
                    if b_sum == old_b and d_sum == old_d:
                        break
                else:
                    raise ArithmeticError("Decimal integral series did not converge")
                b, integral_d = l * b_sum, l * l * d_sum
            else:
                b = (1 - transmission) / d
                integral_d = (l - b) / d
        # Normalize in Decimal BEFORE binary64 conversion.  A raw D may be
        # genuinely too small to represent even while D/L remains representable.
        beta, delta = b / l, integral_d / l
        complete_values = (transmission, b, integral_d, beta, delta)
        decimal_values = tuple(str(value) for value in complete_values)
        values = tuple(float(value) for value in complete_values)
    if not np.isfinite(values).all():
        raise ArithmeticError("independent integral conversion is not finite")
    return values, decimal_values


def _relative_max(defect, scale, axes):
    """Reject invalid accounting inputs and undefined/nonfinite ratios."""
    defect, scale = np.broadcast_arrays(abs(defect), np.asarray(scale))
    if not np.isfinite(defect).all() or not np.isfinite(scale).all() or np.any(scale < 0):
        raise ArithmeticError("nonfinite defect or invalid accounting scale")
    if np.any((scale == 0) & (defect != 0)):
        raise ArithmeticError("nonzero accounting defect has exactly zero scale")
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        ratio = np.divide(defect, scale, out=np.zeros_like(defect), where=scale > 0)
    if not np.isfinite(ratio).all():
        raise ArithmeticError("nonfinite relative accounting result")
    return np.max(ratio, axis=axes)


def solve_expanded(mu, H, height, *, angular_weights, coarse_layers=N_COARSE,
                   subdivisions=1, sources):
    """Independently assemble and solve 16*n+8 equations per source column.

    For angle s, fine cell i, and global face j, the zero-based unknowns are

        mean(s,i) = s*n+i
        face(s,j) = 8*n+s*(n+1)+j.

    Let in/out=(i,i+1) for positive mu, reversed for negative mu, and
    L=h/abs(mu), d=H[s,s].  The independently assembled cell rows are

        f_out-T*f_in+B*sum(t!=s,H[s,t]*a[t,i]) = B*q[s,i]
        a[s,i]-(B/L)*f_in+(D/L)*sum(t!=s,H[s,t]*a[t,i]) = (D/L)*q[s,i].

    The second row is normalized in Decimal before conversion to binary64.
    Raw D underflow therefore does not erase a representable D/L mean term.

    Eight additional rows impose face(s,0)=0 for positive mu, and face(s,n)=0
    for negative mu.  Shared interfaces are single global face unknowns;
    there is no duplicated-face penalty or eliminated flight response.

    For the factorization, both equations and unknowns are independently
    permuted to vacuum first, then mean/outgoing-face pairs in physical upwind
    order, separately for each angle.  The two permutation arrays map a new
    coordinate to its original coordinate.  The original matrix above remains
    independently assembled and returned; the actual permuted matrix, RHS,
    solution, residual, and SuperLU permutations/configuration are returned
    alongside it.  Restoring coordinates does not alter a solved value.

    Sources have shape (8,4,k) and may be signed finite linear probes.  Raw
    signs and residuals are returned; this routine neither applies admission
    thresholds nor asserts that H identifies native axial transport.
    """
    coarse_layers = _positive_integer(coarse_layers, "coarse_layers")
    subdivisions = _positive_integer(subdivisions, "subdivisions")
    if coarse_layers != N_COARSE:
        raise ValueError("exactly four coarse layers required by this reference scope")
    mu = np.array(mu, dtype=float, copy=True)
    weights = np.array(angular_weights, dtype=float, copy=True)
    h_matrix = np.array(H, dtype=float, copy=True)
    source = np.array(sources, dtype=float, copy=True)
    height = float(height)
    if (
        mu.shape != (N_ANGLE,)
        or not np.isfinite(mu).all()
        or np.any(mu == 0)
        or np.any(abs(mu) >= 1)
        or np.count_nonzero(mu > 0) != 4
        or np.count_nonzero(mu < 0) != 4
    ):
        raise ValueError("four positive and four negative finite interior cosines required")
    if (
        weights.shape != (N_ANGLE,)
        or not np.isfinite(weights).all()
        or np.any(weights <= 0)
        or not np.isfinite(weights.sum())
    ):
        raise ValueError("eight positive finite explicit angular weights required")
    if h_matrix.shape != (N_ANGLE, N_ANGLE) or not np.isfinite(h_matrix).all():
        raise ValueError("complete finite eight-by-eight algebraic H required")
    if np.any(np.diag(h_matrix) < 0):
        raise ValueError("nonnegative diagonal attenuation required")
    for s in range(N_ANGLE):
        for t in range(N_ANGLE):
            if s != t and h_matrix[s, t] > 0:
                raise ValueError("nonpositive off-diagonal algebraic H required")
    if not np.isfinite(height) or height <= 0:
        raise ValueError("finite positive height required")
    if (
        source.ndim != 3
        or source.shape[:2] != (N_ANGLE, N_COARSE)
        or source.shape[-1] < 1
        or not np.isfinite(source).all()
    ):
        raise ValueError("finite source columns of shape (8,4,k) required")
    n, k = N_COARSE * subdivisions, source.shape[-1]
    fine_width = height / n
    if not np.isfinite(fine_width) or fine_width <= 0:
        raise ValueError("positive finite represented subcell widths required")
    dimension = 16 * n + 8
    rows, columns, entries = [], [], []
    rhs = np.zeros((dimension, k))
    fine_source = np.zeros((N_ANGLE, n, k))
    primitives = np.zeros((N_ANGLE, 5))
    lengths = np.zeros(N_ANGLE)
    decimal_witnesses = []

    def add(row, column, value):
        # Exact structural zeros are omitted; nonzero coefficients are never
        # dropped by magnitude or fitted to a balance or response.
        if value != 0:
            rows.append(row)
            columns.append(column)
            entries.append(float(value))

    def mean_index(angle, cell):
        return angle * n + cell

    def face_index(angle, face):
        return 8 * n + angle * (n + 1) + face

    for s in range(N_ANGLE):
        length = fine_width / abs(float(mu[s]))
        lengths[s] = length
        values, witness = _decimal_integrals(length, h_matrix[s, s])
        transmission, b, integral_d, beta, delta = values
        primitives[s] = values
        decimal_witnesses.append(dict(
            angle=s, length_hex=float(length).hex(),
            attenuation_hex=float(h_matrix[s, s]).hex(),
            T=witness[0], B=witness[1], D=witness[2],
            beta=witness[3], delta=witness[4],
        ))
        for i in range(n):
            coarse_cell = i // subdivisions
            fine_source[s, i] = source[s, coarse_cell]
            incoming, outgoing = (i, i + 1) if mu[s] > 0 else (i + 1, i)
            face_row, mean_row = s * n + i, 8 * n + s * n + i
            add(face_row, face_index(s, outgoing), 1.0)
            add(face_row, face_index(s, incoming), -transmission)
            add(mean_row, mean_index(s, i), 1.0)
            add(mean_row, face_index(s, incoming), -beta)
            for t in range(N_ANGLE):
                if t == s:
                    continue
                add(face_row, mean_index(t, i), b * h_matrix[s, t])
                add(mean_row, mean_index(t, i), delta * h_matrix[s, t])
            rhs[face_row] = b * fine_source[s, i]
            rhs[mean_row] = delta * fine_source[s, i]
        entry_face = 0 if mu[s] > 0 else n
        add(16 * n + s, face_index(s, entry_face), 1.0)
    matrix = coo_matrix(
        (entries, (rows, columns)), shape=(dimension, dimension)
    ).tocsc()
    if not np.isfinite(matrix.data).all() or not np.isfinite(rhs).all():
        raise ArithmeticError("nonfinite expanded equation coefficients or sources")
    # Pair the unit vacuum equation with its actual incoming face unknown,
    # then each cell mean and outgoing face equation with its own unknown.
    # With diagonal H this gives an exactly lower-triangular characteristic
    # system in every angular block.  In particular, no downstream nonzero
    # RHS is subtracted to recover an upstream zero face.  With off-diagonal
    # coupling the full equations remain coupled; no angle/source is removed.
    # H's sign screen alone does not certify a nonsingular M-matrix, so this
    # ordering asserts neither positivity nor qualification of arbitrary H.
    row_order, column_order = [], []
    for s in range(N_ANGLE):
        entry_face = 0 if mu[s] > 0 else n
        row_order.append(16 * n + s)
        column_order.append(face_index(s, entry_face))
        cells = range(n) if mu[s] > 0 else range(n - 1, -1, -1)
        for i in cells:
            outgoing = i + 1 if mu[s] > 0 else i
            row_order.extend((8 * n + s * n + i, s * n + i))
            column_order.extend((mean_index(s, i), face_index(s, outgoing)))
    row_permutation = np.asarray(row_order, dtype=np.int64)
    column_permutation = np.asarray(column_order, dtype=np.int64)
    original_indices = np.arange(dimension, dtype=np.int64)
    if (not np.array_equal(np.sort(row_permutation), original_indices)
            or not np.array_equal(np.sort(column_permutation), original_indices)):
        raise ArithmeticError("causal equation/unknown permutation is not a complete bijection")
    permuted_matrix = matrix[row_permutation, :][:, column_permutation].tocsc()
    permuted_rhs = rhs[row_permutation].copy()
    if not np.array_equal(permuted_matrix.diagonal(), np.ones(dimension)):
        raise ArithmeticError("causal ordering failed to pair the unit equation diagonals")
    factorization_config = dict(
        solver="scipy.sparse.linalg.splu",
        equation_order="angle, vacuum, then upwind cell mean and outgoing face",
        unknown_order="angle, vacuum face, then upwind cell mean and outgoing face",
        permutation_direction="new coordinate to original coordinate",
        permc_spec="NATURAL", diag_pivot_thresh=0.0,
        Equil=False, SymmetricMode=True,
        solve_trans="N",
        solution_modification="none",
        no_additional_numerical_solve=True,
    )
    factor = splu(permuted_matrix, permc_spec="NATURAL", diag_pivot_thresh=0.0,
                  options=dict(Equil=False, SymmetricMode=True))
    factor_row_permutation = factor.perm_r.copy()
    factor_column_permutation = factor.perm_c.copy()
    factor_pivots = factor.U.diagonal().copy()
    if (not np.array_equal(factor_row_permutation, original_indices)
            or not np.array_equal(factor_column_permutation, original_indices)):
        raise ArithmeticError("causal factorization introduced an undeclared row or column pivot")
    if not np.isfinite(factor_pivots).all() or np.any(factor_pivots <= 0):
        raise ArithmeticError("causal factorization requires finite positive actual pivots")
    permuted_solution = factor.solve(permuted_rhs, trans="N")
    solution = np.empty_like(permuted_solution)
    solution[column_permutation] = permuted_solution
    if not np.isfinite(solution).all() or not np.isfinite(permuted_solution).all():
        raise ArithmeticError("expanded solve produced a nonfinite field")
    angular = solution[:8 * n].reshape(N_ANGLE, n, k)
    faces = solution[8 * n:].reshape(N_ANGLE, n + 1, k)
    widths = np.full(n, fine_width)
    coarse_widths = np.full(N_COARSE, height / N_COARSE)
    # Form dimensionless geometric weights first.  Multiplying a tiny but
    # representable mean by a tiny width before division would spuriously
    # erase that mean.  These are direct h_fine/h_coarse ratios, never fitted
    # or rescaled to make their sum equal one.
    restriction_weights = np.zeros(n)
    coarse_angular = np.zeros((N_ANGLE, N_COARSE, k))
    for coarse_cell in range(N_COARSE):
        for i in range(coarse_cell * subdivisions, (coarse_cell + 1) * subdivisions):
            restriction_weights[i] = widths[i] / coarse_widths[coarse_cell]
            coarse_angular[:, coarse_cell] += angular[:, i] * restriction_weights[i]
    coarse_faces = faces[:, ::subdivisions, :]
    fine_scalar = np.einsum("s,szk->zk", weights, angular)
    coarse_scalar = np.einsum("s,szk->zk", weights, coarse_angular)
    fine_jz = np.einsum("s,szk->zk", weights * mu, angular)
    coarse_jz = np.einsum("s,szk->zk", weights * mu, coarse_angular)
    face_jz = np.einsum("s,sfk->fk", weights * mu, faces)
    incoming_angles = np.zeros((N_ANGLE, k))
    outgoing_angles = np.zeros((2, N_ANGLE, k))
    cell_face_defect = np.zeros_like(angular)
    cell_mean_defect = np.zeros_like(angular)
    characteristic_scale = np.zeros_like(angular)
    effective = np.zeros_like(angular)
    for s in range(N_ANGLE):
        # Directly evaluate q - sum(t!=s)H[s,t]*a[t] from the supplied H.
        effective[s] = fine_source[s]
        for t in range(N_ANGLE):
            if t != s:
                effective[s] -= h_matrix[s, t] * angular[t]
        if mu[s] > 0:
            incoming, outgoing = faces[s, :-1], faces[s, 1:]
            incoming_angles[s] = faces[s, 0]
            outgoing_angles[1, s] = faces[s, -1]
        else:
            incoming, outgoing = faces[s, 1:], faces[s, :-1]
            incoming_angles[s] = faces[s, -1]
            outgoing_angles[0, s] = faces[s, 0]
        transmission, b, integral_d, beta, delta = primitives[s]
        cell_face_defect[s] = outgoing - transmission * incoming - b * effective[s]
        cell_mean_defect[s] = angular[s] - beta * incoming - delta * effective[s]
        characteristic_scale[s] = abs(incoming) + lengths[s] * abs(effective[s])
    angular_escape = abs(mu)[None, :, None] * outgoing_angles
    escape = np.einsum("s,bsk->bk", weights, angular_escape)
    h_action = np.einsum("st,tzk->szk", h_matrix, angular)
    streaming = mu[:, None, None] * np.diff(faces, axis=1)
    equation_defect = streaming + widths[None, :, None] * (h_action - fine_source)
    equation_scale = abs(streaming) + widths[None, :, None] * (
        abs(h_action) + abs(fine_source)
    )
    algebraic_birth = np.einsum("s,z,szk->k", weights, widths, fine_source)
    algebraic_collision = np.einsum("s,z,szk->k", weights, widths, h_action)
    algebraic_defect = escape.sum(axis=0) + algebraic_collision - algebraic_birth
    algebraic_scale = abs(escape).sum(axis=0) + np.einsum(
        "s,z,szk->k", weights, widths, abs(h_action) + abs(fine_source)
    )
    matrix_defect = matrix @ solution - rhs
    permuted_matrix_defect = permuted_matrix @ permuted_solution - permuted_rhs
    derived = (
        angular, faces, coarse_angular, coarse_faces, fine_scalar, coarse_scalar,
        fine_jz, coarse_jz, face_jz, incoming_angles, outgoing_angles,
        cell_face_defect, cell_mean_defect, characteristic_scale, effective,
        angular_escape, escape, h_action, streaming, equation_defect, equation_scale,
        algebraic_birth, algebraic_collision, algebraic_defect, algebraic_scale,
        matrix_defect, permuted_matrix_defect, restriction_weights,
    )
    if not all(np.isfinite(value).all() for value in derived):
        raise ArithmeticError("nonfinite derived field, residual, or accounting scale")
    diagnostics = dict(
        matrix_residual_relative=_relative_max(
            matrix_defect, abs(rhs).max(axis=0), 0
        ),
        expanded_matrix_residual_relative=_relative_max(
            matrix_defect, abs(rhs).max(axis=0), 0
        ),
        permuted_matrix_residual_relative=_relative_max(
            permuted_matrix_defect, abs(permuted_rhs).max(axis=0), 0
        ),
        characteristic_face_relative=_relative_max(
            cell_face_defect, characteristic_scale, (0, 1)
        ),
        characteristic_mean_relative=_relative_max(
            cell_mean_defect, characteristic_scale, (0, 1)
        ),
        full_directional_cell_equation_relative=_relative_max(
            equation_defect, equation_scale, (0, 1)
        ),
        raw_algebraic_balance_relative=_relative_max(algebraic_defect, algebraic_scale, ()),
        vacuum_incoming_absolute=abs(incoming_angles).max(axis=0),
        minimum_angular_mean=angular.min(axis=(0, 1)),
        minimum_angular_face=faces.min(axis=(0, 1)),
        minimum_coarse_angular_mean=coarse_angular.min(axis=(0, 1)),
        minimum_effective_algebraic_source=effective.min(axis=(0, 1)),
        external_source_column_nonnegative=np.all(source >= 0, axis=(0, 1)),
        angular_weights_sum=float(weights.sum()),
    )
    return dict(
        sources=source, external_sources=source, fine_external_sources=fine_source,
        fine_angular_means=angular, fine_angular_faces=faces,
        coarse_angular_means=coarse_angular, coarse_angular_faces=coarse_faces,
        fine_scalar_mean=fine_scalar, coarse_scalar_mean=coarse_scalar,
        fine_signed_jz=fine_jz, coarse_signed_jz=coarse_jz,
        fine_signed_face_jz=face_jz, coarse_signed_face_jz=face_jz[::subdivisions],
        bottom_top_outgoing_angular_flux=outgoing_angles,
        bottom_top_angular_escape_current=angular_escape,
        bottom_top_escape_current=escape,
        vacuum_incoming_angular_flux=incoming_angles,
        effective_algebraic_sources=effective,
        algebraic_birth=algebraic_birth, algebraic_collision=algebraic_collision,
        raw_algebraic_balance_defect=algebraic_defect,
        raw_algebraic_balance_scale=algebraic_scale,
        expanded_matrix=matrix, expanded_rhs=rhs, expanded_solution=solution,
        expanded_solve_matrix=permuted_matrix,
        expanded_solve_rhs=permuted_rhs,
        expanded_solve_solution=permuted_solution,
        expanded_row_permutation=row_permutation,
        expanded_column_permutation=column_permutation,
        expanded_factor_row_permutation=factor_row_permutation,
        expanded_factor_column_permutation=factor_column_permutation,
        expanded_factor_pivots=factor_pivots,
        expanded_factorization=factorization_config,
        raw_matrix_residual=matrix_defect,
        raw_permuted_matrix_residual=permuted_matrix_defect,
        raw_characteristic_face_defect=cell_face_defect,
        raw_characteristic_mean_defect=cell_mean_defect,
        raw_characteristic_scale=characteristic_scale,
        raw_directional_cell_equation_defect=equation_defect,
        raw_directional_cell_equation_scale=equation_scale,
        primitive_TBD=primitives[:, :3], primitive_beta_delta=primitives[:, 3:],
        decimal_primitive_witnesses=decimal_witnesses,
        decimal_precision=DECIMAL_PRECISION,
        mean_unknowns=8 * n, face_unknowns=8 * (n + 1), expanded_dimension=dimension,
        fine_widths=widths, coarse_widths=coarse_widths,
        coarse_restriction_weights=restriction_weights,
        diagnostics=diagnostics,
        model_scope="independent expanded equations for the same constant-subcell candidate",
        internal_coupling_is_cell_mean_source=True,
        continuous_BVP_qualified=False,
        native_response_qualified=False,
        physical_collision_balance_assessed=False,
        axial_propagation_qualified=False,
        scattering_fission_iteration_qualified=False,
        AAA_accuracy_qualified=False,
        ABA_admitted=False,
    )

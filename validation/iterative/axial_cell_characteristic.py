"""Positive constant-cell-source S2 characteristics; no native radial lift."""
import math
import numpy as np
from scipy.linalg import lu_factor, lu_solve


def coefficients(length, total):
    """Exact T, B, D, with a convergent thin-cell series for D."""
    length, total = np.broadcast_arrays(np.asarray(length, float), np.asarray(total, float))
    if np.any(length <= 0) or np.any(total < 0) or not np.isfinite(length + total).all():
        raise ValueError('finite positive lengths and nonnegative totals required')
    tau = length * total
    safe = np.where(total > 0, total, 1.)
    transmission = np.exp(-tau)
    b = np.where(total == 0, length, -np.expm1(-tau) / safe)
    # D/L^2 = sum_k (-tau)^k/(k+2)!; at tau <= 0.5 the omitted
    # term is below double precision. The other branch is well separated.
    x = np.where(tau <= .5, tau, 0.)
    series = np.polynomial.polynomial.polyval(x, [(-1.)**k / math.factorial(k + 2) for k in range(19)])
    d = np.where(tau <= .5, length**2 * series, (length - b) / safe)
    return transmission, b, d


def sweep_response(widths, total, mu, sign, periodic=False):
    """Angular means/faces as linear functions of directional cell sources."""
    n = len(widths); length = widths / mu
    t, b, d = coefficients(length, total)
    face = np.zeros((n + 1, n)); boundary = np.zeros(n + 1)
    mean = np.zeros((n, n)); mean_boundary = np.zeros(n)
    boundary[0 if sign == 1 else n] = 1.
    indices = range(n) if sign == 1 else range(n - 1, -1, -1)
    for i in indices:
        incoming, outgoing = (i, i + 1) if sign == 1 else (i + 1, i)
        mean[i] = b[i] / length[i] * face[incoming]
        mean[i, i] += d[i] / length[i]
        mean_boundary[i] = b[i] / length[i] * boundary[incoming]
        face[outgoing] = t[i] * face[incoming]
        face[outgoing, i] += b[i]
        boundary[outgoing] = t[i] * boundary[incoming]
    if periodic:
        attenuation = -np.expm1(-np.dot(total, length))
        if attenuation <= 0:
            raise ValueError('periodic void has no positive-source steady state')
        incoming_response = face[-1 if sign == 1 else 0].copy() / attenuation
        mean += mean_boundary[:, None] * incoming_response
        face += boundary[:, None] * incoming_response
        mean_boundary = np.zeros(n); boundary = np.zeros(n + 1)
    return mean, mean_boundary, face, boundary


def assemble(widths, total, scattering, mu, periodic=False):
    widths = np.asarray(widths, float)
    total = np.broadcast_to(total, widths.shape).copy()
    scattering = np.broadcast_to(scattering, widths.shape).copy()
    if widths.ndim != 1 or not len(widths) or not 0 < mu <= 1:
        raise ValueError('one-dimensional nonempty grid and 0 < mu <= 1 required')
    if np.any(scattering < 0) or np.any(scattering > total) or not np.isfinite(scattering).all():
        raise ValueError('require 0 <= scattering <= total')
    if periodic and np.all(total == scattering):
        raise ValueError('conservative periodic positive source is incompatible with integrated balance')
    length = widths / mu; t, b, d = coefficients(length, total)
    sweeps = [sweep_response(widths, total, mu, sign, periodic) for sign in (1, -1)]
    matrix = np.eye(len(widths)) - (sweeps[0][0] + sweeps[1][0]) * scattering[None, :] / 2
    local_denominator = 1 - scattering * d / length
    if np.any(local_denominator <= 0):
        raise ValueError('nonpositive local source-elimination denominator')
    return dict(widths=widths, total=total, scattering=scattering, mu=mu,
                periodic=periodic, T=t, B=b, D=d, matrix=matrix,
                local_denominator=local_denominator, sweeps=sweeps,
                factor=lu_factor(matrix))


def solve(system, source, incoming):
    """Solve all spatial coordinates and all RHS columns without truncation."""
    source = np.asarray(source, float); incoming = np.asarray(incoming, float)
    n = len(system['widths'])
    if source.ndim != 3 or source.shape[:2] != (2, n) or incoming.shape != (2, source.shape[2]):
        raise ValueError('source shape (2,n,k), incoming shape (2,k) required')
    if not np.isfinite(source).all() or not np.isfinite(incoming).all():
        raise ValueError('finite sources required')
    if system['periodic'] and np.any(incoming != 0):
        raise ValueError('periodic response has no independent incoming boundary')
    rhs = sum(s[0] @ source[j] + s[1][:, None] * incoming[j] for j, s in enumerate(system['sweeps'])) / 2
    phi = lu_solve(system['factor'], rhs)
    q = source + system['scattering'][None, :, None] * phi
    angular = np.stack([s[0] @ q[j] + s[1][:, None] * incoming[j] for j, s in enumerate(system['sweeps'])])
    faces = np.stack([s[2] @ q[j] + s[3][:, None] * incoming[j] for j, s in enumerate(system['sweeps'])])
    current = system['mu'] * (angular[0] - angular[1]) / 2
    face_current = system['mu'] * (faces[0] - faces[1]) / 2
    return dict(phi=phi, angular=angular, current=current, faces=faces, face_current=face_current,
                face_second_moment=system['mu']**2 * (faces[0] + faces[1]) / 2,
                escape=system['mu'] * np.stack([faces[1, 0], faces[0, -1]]) / 2,
                source=source, incoming=incoming, rhs=rhs,
                matrix_residual=system['matrix'] @ phi - rhs)


def relative_max(defect, scale, axes):
    """Zero scales require exact zero defects, with no numerical clipping."""
    defect, scale = np.broadcast_arrays(np.abs(defect), scale)
    ratio = np.divide(defect, scale, out=np.zeros_like(defect), where=scale > 0)
    ratio[(scale == 0) & (defect != 0)] = np.inf
    return np.max(ratio, axis=axes)


def diagnostics(system, fields):
    h = system['widths']; mu = system['mu']; length = h / mu
    t, b, d = (system[k][:, None] for k in ['T', 'B', 'D'])
    angular = fields['angular']; faces = fields['faces']; phi = fields['phi']
    source = fields['source']; q = source + system['scattering'][None, :, None] * phi
    inflow = np.stack([faces[0, :-1], faces[1, 1:]])
    outflow = np.stack([faces[0, 1:], faces[1, :-1]])
    face_defect = outflow - (t * inflow + b * q)
    mean_defect = angular - (b * inflow + d * q) / length[:, None]
    scale = np.abs(inflow) + length[:, None] * np.abs(q)
    even = np.diff(fields['face_current'], axis=0) + h[:, None] * (
        (system['total'] - system['scattering'])[:, None] * phi - source.mean(axis=0))
    odd = np.diff(fields['face_second_moment'], axis=0) + h[:, None] * (
        system['total'][:, None] * fields['current'] - mu * (source[0] - source[1]) / 2)
    incoming_scale = h[:, None] * np.abs(source).mean(axis=0) + mu * np.abs(inflow).mean(axis=0)
    absorbed = np.sum(h[:, None] * (system['total'] - system['scattering'])[:, None] * phi, axis=0)
    supplied = np.sum(h[:, None] * source.mean(axis=0), axis=0) + mu * (faces[0, 0] + faces[1, -1]) / 2
    global_defect = fields['escape'].sum(axis=0) + absorbed - supplied
    boundary_defect = (np.stack([faces[0, 0] - faces[0, -1], faces[1, -1] - faces[1, 0]])
                       if system['periodic'] else np.stack([faces[0, 0], faces[1, -1]]) - fields['incoming'])
    flux_scale = np.max(np.abs(faces), axis=(0, 1))
    metrics = dict(matrix_residual_relative=relative_max(fields['matrix_residual'], np.max(abs(fields['rhs']), axis=0), 0),
        characteristic_consistency_relative=np.maximum(relative_max(face_defect, scale, (0, 1)), relative_max(mean_defect, scale, (0, 1))),
        scalar_consistency_relative=relative_max(phi - angular.mean(axis=0), np.max(abs(phi), axis=0), 0),
        boundary_consistency_relative=relative_max(boundary_defect, flux_scale, 0),
        raw_global_balance_relative=np.abs(global_defect) / supplied,
        even_cell_balance_relative=relative_max(even, incoming_scale, 0),
        odd_cell_balance_relative=relative_max(odd, mu * incoming_scale, 0),
        minimum_angular=angular.min(axis=(0, 1)), minimum_face=faces.min(axis=(0, 1)))
    raw = dict(face_defect=face_defect, mean_defect=mean_defect, even_cell_defect=even,
               odd_cell_defect=odd, global_defect=global_defect, boundary_defect=boundary_defect)
    return metrics, raw


def unit_inputs(n):
    """Independent directional-volume and left/right boundary unit inputs."""
    source = np.zeros((2, n, 2 * n + 2)); source[:, :, :2 * n] = np.eye(2 * n).reshape(2, n, 2 * n)
    incoming = np.zeros((2, 2 * n + 2)); incoming[:, -2:] = np.eye(2)
    return source, incoming

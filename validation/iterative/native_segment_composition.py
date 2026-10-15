"""Direct flights and independent augmented-matrix composition diagnostics."""
from pathlib import Path
import numpy as np
from axial_cell_characteristic import coefficients


def read_native(path):
    with Path(path).open('rb') as f:
        header = np.fromfile(f, '<i4', 3)
        if len(header) != 3 or header[0] != 290930 or header[1] < 1 or header[2] != 6:
            raise ValueError('invalid native coefficient header')
        data = np.fromfile(f, '<f8')
    if data.size != int(header[1])*18:
        raise ValueError('native coefficient size mismatch')
    return data.reshape(int(header[1]), 6, 3)


def exact_coefficients(lengths, totals):
    return np.stack(coefficients(lengths, totals), axis=-1)


def input_patterns(n):
    boundary = np.zeros(n+3); boundary[0] = 1.
    source = np.zeros((n, n+3)); source[:, 1] = 1.
    source[:, 2:2+n] = np.eye(n); source[:, -1] = np.arange(n) % 2
    return boundary, source


def scaled_error(value, scale):
    value, scale = np.broadcast_arrays(np.abs(value), scale)
    result = np.divide(value, scale, out=np.zeros_like(value), where=scale > 0)
    result[(scale == 0) & (value != 0)] = np.inf
    return result


def flight(lengths, totals, kernel, boundary, source, reverse=False, native=False, trace=False):
    """All source columns in both formulations; source indexes stay physical."""
    lengths = np.asarray(lengths, float); kernel = np.asarray(kernel, float)
    totals = np.broadcast_to(totals, lengths.shape)
    r, n = lengths.shape; c = len(boundary)
    if kernel.shape != (r, n, 3) or source.shape != (n, c) or np.any(lengths <= 0):
        raise ValueError('invalid flight shapes or lengths')
    incoming = np.broadcast_to(boundary, (r, c)).copy()
    integral = np.zeros_like(incoming); birth = np.zeros_like(incoming); collision = np.zeros_like(incoming)
    minimum_angle = incoming.copy(); minimum_integral = np.full_like(incoming, np.inf)
    local_balance = np.zeros_like(incoming)
    product = np.broadcast_to(np.eye(3), (r, c, 3, 3)).copy()
    step_records = []
    order = list(range(n-1, -1, -1) if reverse else range(n))
    for i in order:
        t, b, d = (kernel[:, i, j, None] for j in range(3))
        q = source[i][None, :]; sigma = totals[:, i, None]; length = lengths[:, i, None]
        outgoing = incoming+b*(q-sigma*incoming) if native else t*incoming+b*q
        own_integral = b*incoming+d*q
        defect = outgoing-incoming+sigma*own_integral-length*q
        local_balance = np.maximum(local_balance, scaled_error(defect, abs(incoming)+length*abs(q)))
        minimum_angle = np.minimum(minimum_angle, outgoing)
        minimum_integral = np.minimum(minimum_integral, own_integral)
        integral += own_integral; collision += sigma*own_integral; birth += length*q
        matrix = np.zeros((r, c, 3, 3))
        matrix[:, :, 0, 0] = t; matrix[:, :, 0, 2] = b*q
        matrix[:, :, 1, 0] = b; matrix[:, :, 1, 1] = 1.; matrix[:, :, 1, 2] = d*q
        matrix[:, :, 2, 2] = 1.
        product = np.einsum('...ij,...jk->...ik', matrix, product)
        if trace: step_records.append(np.stack([incoming, outgoing, own_integral, defect], axis=-1))
        incoming = outgoing
    initial = np.stack([boundary, np.zeros(c), np.ones(c)], axis=-1)
    mapped = np.einsum('rcij,cj->rci', product, initial)
    supply = abs(boundary)[None, :]+birth
    global_defect = outgoing-boundary+collision-birth
    result = dict(outgoing=outgoing, integral=integral, global_defect=global_defect,
        minimum_angle=minimum_angle, minimum_integral=minimum_integral,
        maximum_local_balance_relative=local_balance,
        global_balance_relative=scaled_error(global_defect, supply),
        matrix_outgoing=mapped[:, :, 0], matrix_integral=mapped[:, :, 1],
        matrix_outgoing_relative=scaled_error(outgoing-mapped[:, :, 0], supply),
        matrix_integral_relative=scaled_error(integral-mapped[:, :, 1], lengths.sum(axis=1)[:, None]*supply))
    if trace:
        result['trace'] = np.stack(step_records, axis=1)
        result['trace_piece_index'] = np.asarray(order)
    return result


def preservation(result, whole, length):
    """T, B_out, B_integral, D relative errors for the two uniform controls."""
    expected = np.column_stack([whole[:, 0], whole[:, 1], whole[:, 1], whole[:, 2]])
    measured = np.column_stack([result['outgoing'][:, 0], result['outgoing'][:, 1],
                                result['integral'][:, 0], result['integral'][:, 1]])
    natural = np.column_stack([np.ones_like(length), length, length, length**2])
    return abs(measured-expected)/np.where(expected != 0, abs(expected), natural)

"""Unweighted radial white transfer; axial incoming amplitudes are exactly zero.

One physical geometry supplies all 1..370 groups and all white input columns.
Signed P2 volume sources remain in the separate, unchanged multigroup action.
This interface supplies boundary terms for a future whole-inventory consumer.
"""
import ctypes
from functools import lru_cache
import numpy as np
from native_layered_multigroup import _quadrature

GEOMETRY_NAMES = ('offset_intervals', 'chords', 'pieces',
                  'radial_entering_chords', 'axial_entering_chords',
                  'minimum_piece_length')


@lru_cache(maxsize=4)
def kernel_white_transfer(library):
    function = ctypes.CDLL(str(library)).layered_white_radial_transfer
    pointer = ctypes.c_void_p
    function.argtypes = ([ctypes.c_int]*3 + [pointer]*3 + [ctypes.c_int]*2 +
                         [ctypes.c_double]*2 + [ctypes.c_int]*2 + [pointer]*6)
    function.restype = ctypes.c_int
    return function


def white_radial_transfer(library, widths, regions, total, entry, exit_surface,
                          H, nz, mu, orientation, order):
    """Return complete raw T, leakage L and geometric incoming D.

    Caller supplies actual track end surfaces for the selected orientation;
    reverse tracks swap those surfaces. Local side0/1 never determines a hex
    face ID. total=(8,nz,k), T=(6*nz,6*nz,k), L=(2,8,6*nz,k), D=(6*nz).
    Rows of T are outgoing face/layer, columns incoming face/layer; L's first
    axis is bottom/top and second axis the axial exit region. D is independent
    of the group total, accumulated only at each radial-entering chord's first
    piece. Axial-entering chords contribute zero to T and L.

    Explicit downstream interface: stream each real track/polar/sign/orientation
    once and apply its original angular/track weight once to T,L,D. Sum BEFORE
    normalizing: the global white equation is (diag(D_sum)-T_sum_g)*a_g=b_g,
    where b_g is the separately accumulated signed-source radial outgoing
    current. Axial leakage is L_sum_g*a_g plus that source action's leakage.
    The consumer must establish coverage, nonzero D, closure/residual/cost
    limits and source compatibility; this function performs no white solve.
    """
    if not isinstance(nz, (int, np.integer)) or not 1 <= nz <= 64:
        raise ValueError('nz must be an integer in 1..64')
    widths = np.ascontiguousarray(widths, dtype='d')
    original_regions = np.asarray(regions)
    total = np.ascontiguousarray(total, dtype='d')
    if (total.ndim != 3 or total.shape[:2] != (8, nz) or
            not 1 <= total.shape[2] <= 370):
        raise ValueError('total must have shape (8,nz,k), k=1..370')
    if (widths.ndim != 1 or not 1 <= len(widths) <= 15 or
            original_regions.shape != widths.shape):
        raise ValueError('complete segment widths and region map required')
    if (not np.isfinite(widths).all() or np.any(widths <= 0) or
            not np.isfinite(original_regions).all() or
            np.any(original_regions != np.floor(original_regions)) or
            np.any((original_regions < 0) | (original_regions >= 8)) or
            not np.isfinite(total).all() or np.any(total < 0)):
        raise ValueError('finite widths, region IDs and nonnegative totals required')
    if (not np.isfinite(H) or H <= 0 or not np.isfinite(mu) or not 0 < abs(mu) < 1 or
            not isinstance(orientation, (int, np.integer)) or orientation not in (-1, 1) or
            not isinstance(entry, (int, np.integer)) or not 0 <= entry < 6 or
            not isinstance(exit_surface, (int, np.integer)) or not 0 <= exit_surface < 6 or
            entry == exit_surface or not isinstance(order, (int, np.integer)) or
            not 2 <= order <= 128):
        raise ValueError('invalid physical geometry, oriented surfaces or quadrature')
    regions = np.ascontiguousarray(original_regions, dtype=np.int32)
    nodes, weights = _quadrature(int(order)); k = total.shape[2]; nwhite = 6*nz
    geometry = np.zeros(6)
    transfer = np.zeros((nwhite, nwhite, k))
    leakage = np.zeros((2, 8, nwhite, k))
    incoming = np.zeros(nwhite)
    status = kernel_white_transfer(str(library))(
        len(widths), nz, k, widths.ctypes.data, regions.ctypes.data, total.ctypes.data,
        int(entry), int(exit_surface), H, mu, orientation, order,
        nodes.ctypes.data, weights.ctypes.data, geometry.ctypes.data,
        transfer.ctypes.data, leakage.ctypes.data, incoming.ctypes.data)
    if status:
        raise RuntimeError(f'layered white radial transfer failed with code {status}')
    return dict(geometry=geometry, geometry_names=GEOMETRY_NAMES,
                transfer=transfer, leakage=leakage, incoming=incoming,
                component_only=True, angular_track_weight_applied=False,
                geometric_normalizer_applied=False, white_closure_qualified=False,
                full_reference_qualified=False, actual_A_B_input_qualified=False,
                physical_balance_qualified=False, AAA_qualified=False, ABA_admitted=False)

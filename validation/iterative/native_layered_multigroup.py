"""Independent group totals on the unchanged physical layered geometry.

Each of 1..370 columns has total[region,layer,column]. All source and face
arrays are explicit and signed. This is a fixed-source component; it does
not establish current A/B input identity, white closure or an eigenreference.
The caller chooses the original H/grid/ray/offset rule; no weights are fitted.
"""
import ctypes
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_layered_transport import METRICS


@lru_cache(maxsize=4)
def kernel_multigroup(library):
    function = ctypes.CDLL(str(library)).layered_transport_multigroup
    pointer = ctypes.c_void_p
    function.argtypes = ([ctypes.c_int] * 3 + [pointer] * 3 +
                         [ctypes.c_int, ctypes.c_double, ctypes.c_double,
                          ctypes.c_int, ctypes.c_int] + [pointer] * 8)
    function.restype = ctypes.c_int
    return function


@lru_cache(maxsize=8)
def _quadrature(order):
    nodes, weights = leggauss(order)
    nodes.setflags(write=False)
    weights.setflags(write=False)
    return nodes, weights


def transport_multigroup(library, widths, regions, total, entry, H, nz, mu,
                         orientation, order, q, radial, axial):
    """Unweighted full cell/face response; no matched or default inflow.

    total=(8,nz,k), q=(8*nz,k), radial=(6*nz,k), axial=(8,k), C order.
    k=1..370 preserves caller column order. Current150 is H150/three physical
    zones; this geometry component also permits the original control grids.
    """
    if not isinstance(nz, (int, np.integer)) or not 1 <= nz <= 64:
        raise ValueError('nz must be an integer in 1..64')
    widths = np.ascontiguousarray(widths, dtype='d')
    original_regions = np.asarray(regions)
    total = np.ascontiguousarray(total, dtype='d')
    q, radial, axial = [np.ascontiguousarray(value, dtype='d')
                        for value in (q, radial, axial)]
    if q.ndim != 2 or not 1 <= q.shape[1] <= 370:
        raise ValueError('explicit source must have 1..370 columns')
    columns = q.shape[1]
    if (widths.ndim != 1 or not 1 <= len(widths) <= 15 or
            original_regions.shape != widths.shape or
            total.shape != (8, nz, columns) or q.shape != (8*nz, columns) or
            radial.shape != (6*nz, columns) or axial.shape != (8, columns)):
        raise ValueError('complete segment map and regional/layer/group arrays required')
    if (not np.isfinite(widths).all() or np.any(widths <= 0) or
            not np.isfinite(original_regions).all() or
            np.any(original_regions != np.floor(original_regions)) or
            np.any((original_regions < 0) | (original_regions >= 8)) or
            np.any(total < 0) or
            any(not np.isfinite(value).all() for value in (total, q, radial, axial))):
        raise ValueError('finite inputs, positive widths and nonnegative group totals required')
    if (not np.isfinite(H) or H <= 0 or not np.isfinite(mu) or
            not 0 < abs(mu) < 1 or
            not isinstance(orientation, (int, np.integer)) or orientation not in (-1, 1) or
            not isinstance(entry, (int, np.integer)) or not 0 <= entry < 6 or
            not isinstance(order, (int, np.integer)) or not 2 <= order <= 128):
        raise ValueError('invalid physical geometry or quadrature controls')
    regions = np.ascontiguousarray(original_regions, dtype=np.int32)
    nodes, weights = _quadrature(int(order))
    geometry = np.zeros(6)
    fields = np.zeros((len(widths)*nz, 9, columns))
    metrics = np.zeros((columns, len(METRICS)))
    status = kernel_multigroup(str(library))(
        len(widths), nz, columns, widths.ctypes.data, regions.ctypes.data,
        total.ctypes.data, int(entry), H, mu, orientation, order,
        nodes.ctypes.data, weights.ctypes.data, q.ctypes.data, radial.ctypes.data,
        axial.ctypes.data, geometry.ctypes.data, fields.ctypes.data, metrics.ctypes.data)
    if status:
        raise RuntimeError(f'layered multigroup transport failed with code {status}')
    return dict(geometry=geometry, fields=fields, metrics=metrics, q=q,
                radial_input=radial, axial_input=axial, total=total,
                component_only=True, full_reference_qualified=False,
                physical_balance_qualified=False, AAA_qualified=False, ABA_admitted=False)

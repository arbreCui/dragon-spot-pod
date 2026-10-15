"""Layer-resolved collision totals for the independent physical ray kernel.

This is a fixed-source support interface, not a multigroup eigenreference.
Totals have explicit shape (8, nz), C order: region * nz + layer. Sources and
face inputs retain their signs. No matched-regression inflow is accepted.
"""
import ctypes
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_layered_transport import METRICS, basis


@lru_cache(maxsize=4)
def kernel_zonal(library):
    function = ctypes.CDLL(str(library)).layered_transport_zonal
    pointer = ctypes.c_void_p
    function.argtypes = ([ctypes.c_int] * 3 + [pointer] * 3 +
                         [ctypes.c_int, ctypes.c_double, ctypes.c_double,
                          ctypes.c_int, ctypes.c_int] + [pointer] * 8)
    function.restype = ctypes.c_int
    return function


def transport_zonal(library, widths, regions, total, entry, H, nz, mu,
                    orientation, order, q=None, radial=None, axial=None):
    if not isinstance(nz, (int, np.integer)) or not 1 <= nz <= 64:
        raise ValueError('nz must be an integer in 1..64')
    widths = np.ascontiguousarray(widths, dtype='d')
    original_regions = np.asarray(regions)
    total = np.ascontiguousarray(total, dtype='d')
    if (widths.ndim != 1 or not 1 <= len(widths) <= 15 or
            original_regions.shape != widths.shape or total.shape != (8, nz)):
        raise ValueError('segment map and explicit totals shape (8,nz) required')
    if (not np.isfinite(widths).all() or np.any(widths <= 0) or
            not np.isfinite(original_regions).all() or
            np.any(original_regions != np.floor(original_regions)) or
            np.any((original_regions < 0) | (original_regions >= 8)) or
            not np.isfinite(total).all() or np.any(total < 0)):
        raise ValueError('finite positive widths, region indices, nonnegative totals required')
    regions = np.ascontiguousarray(original_regions, dtype=np.int32)
    if (not np.isfinite(H) or H <= 0 or not np.isfinite(mu) or
            not 0 < abs(mu) < 1 or
            not isinstance(orientation, (int, np.integer)) or orientation not in (-1, 1) or
            not isinstance(entry, (int, np.integer)) or not 0 <= entry < 6 or
            not isinstance(order, (int, np.integer)) or not 2 <= order <= 128):
        raise ValueError('invalid physical geometry or quadrature controls')
    if q is None:
        if radial is not None or axial is not None:
            raise ValueError('provide all three source/face arrays together')
        q, radial, axial = basis(nz, total[:, 0])
        q[:, -1] = total.ravel(order='C')
    elif radial is None or axial is None:
        raise ValueError('provide all three source/face arrays together')
    q, radial, axial = [np.ascontiguousarray(value, dtype='d')
                        for value in (q, radial, axial)]
    if q.ndim != 2 or not 1 <= q.shape[1] <= 2048:
        raise ValueError('source must have 1..2048 columns')
    columns = q.shape[1]
    if (q.shape != (8*nz, columns) or radial.shape != (6*nz, columns) or
            axial.shape != (8, columns) or
            any(not np.isfinite(value).all() for value in (q, radial, axial))):
        raise ValueError('finite region-major source and complete face arrays required')
    nodes, weights = leggauss(order)
    geometry = np.zeros(6)
    fields = np.zeros((len(widths)*nz, 9, columns))
    metrics = np.zeros((columns, len(METRICS)))
    status = kernel_zonal(str(library))(
        len(widths), nz, columns, widths.ctypes.data, regions.ctypes.data,
        total.ctypes.data, int(entry), H, mu, orientation, order,
        nodes.ctypes.data, weights.ctypes.data, q.ctypes.data, radial.ctypes.data,
        axial.ctypes.data, geometry.ctypes.data, fields.ctypes.data, metrics.ctypes.data)
    if status:
        raise RuntimeError(f'layered zonal transport failed with code {status}')
    return dict(geometry=geometry, fields=fields, metrics=metrics, q=q,
                radial_input=radial, axial_input=axial, total=total)

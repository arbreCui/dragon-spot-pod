"""Nonuniform original-segment geometry; derived from the qualified strip construction."""
import numpy as np
from numpy.polynomial.legendre import leggauss


def geometry(widths, H, nz, mu, orientation, order):
    widths = np.asarray(widths, float)
    nr = len(widths); S = float(np.sum(widths))
    if np.any(widths <= 0) or not np.isfinite(widths).all() or H <= 0 or nr < 1 or nz < 1 or orientation not in (-1, 1):
        raise ValueError('positive dimensions and a signed planar orientation required')
    x = np.r_[0., np.cumsum(widths)]; S = float(x[-1]); z = np.linspace(0, H, nz + 1)
    se = x if orientation == 1 else S - x[::-1]
    breaks = np.unique((z[:, None] - mu * se).ravel())
    gn, gw = leggauss(order)
    u = ((breaks[:-1, None] + breaks[1:, None]) / 2 + np.diff(breaks)[:, None] * gn / 2).ravel()
    weight = (np.diff(breaks)[:, None] * gw / 2).ravel()
    records = []; entry_cell = []; entry_side = []; entry_s = []
    # Every offset is strictly inside a topology interval. Interior corner
    # coincidences therefore cannot occur; boundary cases use deterministic ties.
    for ray, offset in enumerate(u):
        if mu > 0:
            start = max(0., -offset / mu); stop = min(S, (H - offset) / mu)
            ins = (0 if orientation == 1 else 1) if start == 0 else 2
            outs = (1 if orientation == 1 else 0) if stop == S else 3
        elif mu < 0:
            start = max(0., (H - offset) / mu); stop = min(S, -offset / mu)
            ins = (0 if orientation == 1 else 1) if start == 0 else 3
            outs = (1 if orientation == 1 else 0) if stop == S else 2
        else:
            start, stop = 0., S; ins, outs = ((0, 1) if orientation == 1 else (1, 0))
        assert stop > start
        points = [(start, ins)]
        for v in se[1:-1]:
            if start < v < stop: points.append((v, 1 if orientation == 1 else 0))
        if mu:
            for zv in z[1:-1]:
                v = (zv - offset) / mu
                if start < v < stop: points.append((v, 3 if mu > 0 else 2))
        points.append((stop, outs)); points.sort()
        side_in = ins
        for step, ((a, _), (b, side_out)) in enumerate(zip(points[:-1], points[1:])):
            if b == a: continue
            mid = (a + b) / 2; xp = mid if orientation == 1 else S - mid
            zp = offset + mu * mid
            i = np.searchsorted(x, xp, side='right') - 1
            j = np.searchsorted(z, zp, side='right') - 1
            assert 0 <= i < nr and 0 <= j < nz, (xp, zp, i, j)
            cell = i * nz + j
            if step == 0:
                entry_cell.append(cell); entry_side.append(ins); entry_s.append(start)
            records.append((ray, step, cell, side_in, side_out, a, b))
            side_in = side_out ^ 1
    rec = np.array(records)
    result = dict(S=np.array(S), H=np.array(H), nr=np.array(nr), nz=np.array(nz),
                  mu=np.array(mu), orientation=np.array(orientation), order=np.array(order),
                  x=x, z=z, breaks=breaks, u=u, weight=weight,
                  entry_cell=np.array(entry_cell), entry_side=np.array(entry_side), entry_s=np.array(entry_s))
    for i, key in enumerate(['ray', 'step', 'cell', 'in_side', 'out_side', 's0', 's1']):
        result[key] = rec[:, i].astype(int) if i < 5 else rec[:, i]
    result['length'] = result['s1'] - result['s0']
    w = weight[result['ray']]
    result['volume'] = np.bincount(result['cell'], weights=w * result['length'], minlength=nr*nz)
    fi = np.zeros((nr*nz, 4)); fo = np.zeros_like(fi)
    np.add.at(fi, (result['cell'], result['in_side']), w)
    np.add.at(fo, (result['cell'], result['out_side']), w)
    result['face_in_measure'] = fi; result['face_out_measure'] = fo
    result['area'] = (widths[:, None] * np.diff(z)).ravel()
    result['original_widths'] = widths.copy()
    result['represented_widths'] = np.diff(x)
    measures = np.zeros_like(fi)
    measures[:, :2] = np.tile(np.diff(z), nr)[:, None]
    measures[:, 2:] = abs(mu) * np.repeat(widths, nz)[:, None]
    result['face_measure'] = measures
    return result


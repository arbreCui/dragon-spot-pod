"""Exact flights through physical radial/axial cells of a manufactured strip."""
import numpy as np
from numpy.polynomial.legendre import leggauss
from axial_cell_characteristic import coefficients


def relative(defect, scale):
    d, s = np.broadcast_arrays(np.abs(defect), np.asarray(scale))
    ans = np.divide(d, s, out=np.zeros_like(d), where=s > 0)
    return np.where((s == 0) & (d != 0), np.inf, ans)


def geometry(S, H, nr, nz, mu, orientation, order):
    if S <= 0 or H <= 0 or nr < 1 or nz < 1 or orientation not in (-1, 1):
        raise ValueError('positive dimensions and a signed planar orientation required')
    x = np.linspace(0, S, nr + 1); z = np.linspace(0, H, nz + 1)
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
    result['area'] = (np.diff(x)[:, None] * np.diff(z)).ravel()
    measures = np.zeros_like(fi)
    measures[:, :2] = np.tile(np.diff(z), nr)[:, None]
    measures[:, 2:] = abs(mu) * np.repeat(np.diff(x), nz)[:, None]
    result['face_measure'] = measures
    return result


def boundary_mask(g):
    nr, nz = int(g['nr']), int(g['nz'])
    mask = np.zeros((nr, nz, 4), bool)
    mask[0, :, 0] = True; mask[-1, :, 1] = True
    mask[:, 0, 2] = True; mask[:, -1, 3] = True
    return mask.reshape(nr*nz, 4)


def inputs(g, totals, one_d):
    nr, nz = int(g['nr']), int(g['nz']); n = nr*nz
    units = n + nz + (nr if g['mu'] != 0 else 0); k = units + 4
    q = np.zeros((n, k)); q[:, :n] = np.eye(n)
    incoming = np.zeros((len(g['u']), k))
    radial = g['entry_side'] < 2
    rows = np.arange(len(incoming))
    cols = np.where(radial, n + g['entry_cell'] % nz, n + nz + g['entry_cell'] // nz)
    incoming[rows, cols] = 1
    sigma = np.repeat(totals, nz)
    q[:, units] = sigma; incoming[:, units] = 1
    q[:, units+1] = 1
    source_1d = np.array([1.] if nr == 1 else [1., .3])
    q[:, units+2] = np.repeat(source_1d, nz)
    incoming[:, units+2] = one_d(g['entry_s'], totals, source_1d, float(g['S']), int(g['orientation']))
    q[:, units+3] = np.tile(np.arange(nz) % 2, nr)
    return q, incoming, units


def sweep(g, totals, one_d):
    q, incoming, units = inputs(g, totals, one_d)
    n, k = q.shape; ray = g['ray']; cell = g['cell']; length = g['length']
    sigma = np.repeat(totals, int(g['nz'])); t, b, d = coefficients(length, sigma[cell])
    state = incoming.copy(); integrals = np.zeros_like(q)
    fi = np.zeros((n, 4, k)); fo = np.zeros_like(fi)
    minimum_angle = np.empty(len(ray)); minimum_integral = np.empty(len(ray))
    worst_defect = np.empty(len(ray)); worst_scale = np.empty(len(ray)); worst_column = np.empty(len(ray), int)
    piece_relative = np.zeros(k); point_relative = 0.
    matched_source = np.array([1.] if int(g['nr']) == 1 else [1., .3])
    ref0 = one_d(g['s0'], totals, matched_source, float(g['S']), int(g['orientation']))
    ref1 = one_d(g['s1'], totals, matched_source, float(g['S']), int(g['orientation']))
    for step in range(int(g['step'].max()) + 1):
        ix = np.flatnonzero(g['step'] == step); r = ray[ix]; c = cell[ix]
        psi = state[r].copy(); source = q[c]
        integrated = b[ix, None] * psi + d[ix, None] * source
        out = t[ix, None] * psi + b[ix, None] * source
        w = g['weight'][r, None]
        np.add.at(integrals, c, w * integrated)
        np.add.at(fi, (c, g['in_side'][ix]), w * psi)
        np.add.at(fo, (c, g['out_side'][ix]), w * out)
        defect = out - psi + sigma[c, None] * integrated - length[ix, None] * source
        scale = psi + length[ix, None] * source
        error = relative(defect, scale); col = error.argmax(axis=1)
        worst_defect[ix] = defect[np.arange(len(ix)), col]
        worst_scale[ix] = scale[np.arange(len(ix)), col]; worst_column[ix] = col
        piece_relative = np.maximum(piece_relative, error.max(axis=0))
        minimum_angle[ix] = np.minimum(psi.min(axis=1), out.min(axis=1))
        minimum_integral[ix] = integrated.min(axis=1)
        point_relative = max(point_relative, float(relative(psi[:, units+2]-ref0[ix], ref0[ix]).max()),
                             float(relative(out[:, units+2]-ref1[ix], ref1[ix]).max()))
        state[r] = out
    birth = g['area'][:, None] * q
    defect = birth + fi.sum(axis=1) - fo.sum(axis=1) - sigma[:, None] * integrals
    scale = birth + fi.sum(axis=1)
    mask = boundary_mask(g)
    supply = birth.sum(axis=0) + fi[mask].sum(axis=0)
    global_defect = supply - fo[mask].sum(axis=0) - (sigma[:, None]*integrals).sum(axis=0)
    nr, nz = int(g['nr']), int(g['nz']); inf = fi.reshape(nr,nz,4,k); outf = fo.reshape(nr,nz,4,k)
    if g['orientation'] == 1:
        a, bface = outf[:-1,:,1], inf[1:,:,0]
    else:
        a, bface = outf[1:,:,0], inf[:-1,:,1]
    shared_defects = [(a-bface).reshape(-1,k)]; shared_scales = [(abs(a)+abs(bface)).reshape(-1,k)]
    if g['mu'] >= 0:
        a, bface = outf[:,:-1,3], inf[:,1:,2]
    else:
        a, bface = outf[:,1:,2], inf[:,:-1,3]
    shared_defects.append((a-bface).reshape(-1,k)); shared_scales.append((abs(a)+abs(bface)).reshape(-1,k))
    return dict(q=q, incoming=incoming, units=np.array(units), total=sigma,
                integral=integrals, face_in=fi, face_out=fo, exit_angle=state,
                T=t, B=b, D=d, minimum_piece_angle=minimum_angle, minimum_piece_integral=minimum_integral,
                worst_piece_signed_defect=worst_defect, worst_piece_scale=worst_scale, worst_piece_column=worst_column,
                maximum_piece_relative=piece_relative, cell_birth=birth, cell_defect=defect, cell_scale=scale,
                global_defect=global_defect, global_scale=supply,
                shared_defect=np.concatenate(shared_defects), shared_scale=np.concatenate(shared_scales),
                matched_point_relative=np.array(point_relative))

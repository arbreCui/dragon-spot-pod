"""Complete source-coordinate Green action on retained native radial tracks."""
import numpy as np
from axial_cell_characteristic import coefficients
from qualify_native_signed_axial import axial_mu, angular_measures, ledger


def ratio(value, scale):
    value, scale = np.broadcast_arrays(np.abs(value), scale)
    result = np.divide(value, scale, out=np.zeros_like(value), where=scale > 0)
    result[(scale == 0) & (value != 0)] = np.inf
    return result


def green_sweep(d, a, fractions=(1.,), native=False, chunk=4096):
    """Every region/surface coordinate, polar node and planar orientation.

    Each Green flight has the original half-sign weight. The two independent
    axial signs are evaluated separately later, without mixing their inputs.
    """
    if native and tuple(fractions) != (1.,): raise ValueError('native calibration is unsplit only')
    if min(fractions) <= 0 or abs(sum(fractions)-1) > 1e-15: raise ValueError('invalid partition')
    nr, nb, npole = d['nr'], d['nb'], d['nmu']; ns = nr+nb; nl = len(d['track'])
    g = {k: np.zeros((2, npole, nr, ns)) for k in ['iso', 'own', 'jx', 'abs_jx']}
    g['boundary'] = np.zeros((2, npole, nb, ns))
    track = {k: np.zeros((2, nl, ns)) for k in ['outgoing', 'integral', 'defect', 'scale', 'minimum_angle', 'minimum_integral', 'maximum_local_balance']}
    for oi, orientation in enumerate([1, -1]):
        for first in range(0, nl, chunk):
            ids = np.arange(first, min(first+chunk, nl)); m = len(ids)
            entrance = np.zeros(m, int) if orientation == 1 else d['length'][ids]-1
            surface = -d['region'][ids, entrance]-1
            initial = np.zeros((m, ns)); initial[np.arange(m), nr+surface] = 1.
            state = initial.copy(); collision = np.zeros_like(state); birth = np.zeros_like(state); integ = np.zeros_like(state)
            minimum = state.copy(); min_integral = np.full_like(state, np.inf); max_local = np.zeros_like(state)
            for step in range(1, d['nmax']-1):
                active = np.flatnonzero(step < d['length'][ids]-1); lines = ids[active]
                if not len(lines): continue
                seg = np.full(len(lines), step) if orientation == 1 else d['length'][lines]-1-step
                reg = d['region'][lines, seg]-1; polar = d['polar'][lines]
                source = np.zeros((len(lines), ns)); source[np.arange(len(lines)), reg] = 1.
                sigma = a['total'][reg]; length = d['h'][lines, seg]
                incoming = state[active].copy(); outgoing = incoming.copy()
                isolated = np.zeros_like(incoming); own = np.zeros_like(incoming)
                alpha = np.ones(len(lines)); beta = np.zeros(len(lines))
                order = fractions if orientation == 1 else tuple(reversed(fractions))
                for fraction in order:
                    h = length*fraction
                    if native:
                        b = a['b'][lines, seg]; own_d = a['self_d'][lines, seg]; t = 1-sigma*b
                    else: t, b, own_d = coefficients(h, sigma)
                    piece_integral = b[:, None]*outgoing+own_d[:, None]*source
                    next_state = (outgoing+b[:, None]*(source-sigma[:, None]*outgoing) if native
                                  else t[:, None]*outgoing+b[:, None]*source)
                    defect = next_state-outgoing+sigma[:, None]*piece_integral-h[:, None]*source
                    scale = abs(outgoing)+h[:, None]*source
                    max_local[active] = np.maximum(max_local[active], ratio(defect, scale))
                    minimum[active] = np.minimum(minimum[active], next_state)
                    min_integral[active] = np.minimum(min_integral[active], piece_integral)
                    isolated += (b*alpha)[:, None]*incoming
                    own += (b*beta+own_d)[:, None]*source
                    alpha = t*alpha; beta = t*beta+b; outgoing = next_state
                full = isolated+own; weight = d['weight'][lines, None]/2
                np.add.at(g['iso'][oi], (polar, reg), isolated*weight)
                np.add.at(g['own'][oi], (polar, reg), own*weight)
                np.add.at(g['jx'][oi], (polar, reg), full*weight*(orientation*d['mx'][lines, None]))
                np.add.at(g['abs_jx'][oi], (polar, reg), full*weight*abs(d['mx'][lines, None]))
                state[active] = outgoing; collision[active] += sigma[:, None]*full
                birth[active] += length[:, None]*source; integ[active] += full
            end = d['length'][ids]-1 if orientation == 1 else np.zeros(m, int)
            surface = -d['region'][ids, end]-1
            np.add.at(g['boundary'][oi], (d['polar'][ids], surface), state*d['weight'][ids, None]/2)
            for key, value in dict(outgoing=state, integral=integ, defect=state-initial+collision-birth,
                    scale=initial+birth, minimum_angle=minimum, minimum_integral=min_integral,
                    maximum_local_balance=max_local).items(): track[key][oi, ids] = value
    g.update({'track_'+k: v for k, v in track.items()})
    return g


def evaluate(d, a, green, q, inflow):
    x = np.concatenate([q, inflow], axis=2)
    if x.shape[:3] != (2, d['nmu'], d['nr']+d['nb']): raise ValueError('invalid full input coordinates')
    f = {k: np.einsum('opru,zpuc->zprc', green[k], x) for k in ['iso', 'own', 'boundary']}
    integrals = f['iso']+f['own']; vol = d['weights'][:d['nr'], None]; surf = d['weights'][d['nr']:, None]
    mu = axial_mu(d)
    f['phi'] = integrals.sum(axis=(0, 1))/vol
    f['jz'] = np.einsum('prc,p->rc', integrals[0]-integrals[1], mu)/vol
    f['jx'] = np.einsum('opru,zpuc->rc', green['jx'], x)/vol
    f['outgoing'] = f['boundary'].sum(axis=(0, 1))/surf
    absolute = np.einsum('opru,zpuc->zprc', green['iso']+green['own'], abs(x))
    f['phi_scale'] = absolute.sum(axis=(0, 1))/vol
    f['jz_scale'] = np.einsum('zprc,p->rc', absolute, mu)/vol
    f['jx_scale'] = np.einsum('opru,zpuc->rc', green['abs_jx'], abs(x))/vol
    f['outgoing_scale'] = np.einsum('opsu,zpuc->sc', green['boundary'], abs(x))/surf
    f.update(ledger(d, a, q, inflow, integrals, f['boundary']))
    f['q'] = q; f['inflow'] = inflow
    # Stored-volume/surface ledger is deliberately separate from geometry.
    vw, sw = angular_measures(d)
    f['stored_volume_birth'] = np.einsum('zprc,pr,r->c', q, vw, vol[:, 0]/(2*vw.sum(axis=0)))
    f['stored_surface_incoming'] = np.einsum('zpsc,ps,s->c', inflow, sw, surf[:, 0]/(2*sw.sum(axis=0)))
    return f


def compare(d, value, reference):
    metrics = {}
    for key in ['phi', 'jx', 'jz', 'outgoing']:
        w = d['weights'][d['nr']:] if key == 'outgoing' else d['weights'][:d['nr']]
        scale = reference[key+'_scale']; error = value[key]-reference[key]
        norm = lambda x: np.sqrt(np.sum(w[:, None]*x*x, axis=0))
        metrics[key+'_weighted_induced_relative'] = ratio(norm(error), norm(scale))
        metrics[key+'_component_induced_relative'] = np.max(ratio(error, scale), axis=0)
        net = norm(reference[key]); induced = norm(scale)
        valid = net > 1e-10*induced
        metrics[key+'_net_relative_valid'] = valid
        metrics[key+'_weighted_net_relative'] = np.divide(norm(error), net, out=np.zeros_like(net), where=valid)
    return metrics


def close_white(d, a, green, fixed, tags):
    tags = np.asarray(tags); volume = np.flatnonzero(tags == 'angular_volume_vacuum')
    boundary = np.flatnonzero(tags == 'angular_boundary_open')
    targets = np.flatnonzero((tags == 'angular_volume_white') | (tags == 'pair_white'))
    response = fixed['outgoing'][:, boundary]; common_map = np.tile(np.eye(d['nb']), (2*d['nmu'], 1))
    tbb = response@common_map; matrix = np.eye(d['nb'])-tbb
    inverse = np.linalg.solve(matrix, np.eye(d['nb']))
    q = fixed['q'][..., targets]; rhs = fixed['outgoing'][:, volume]@q.reshape(len(volume), -1)
    amplitudes = np.linalg.solve(matrix, rhs)
    incoming = np.broadcast_to(amplitudes, (2, d['nmu'], *amplitudes.shape)).copy()
    fields = evaluate(d, a, green, q, incoming)
    fields.update(tbb=tbb, boundary_inverse=inverse, white_rhs=rhs, white_amplitudes=amplitudes,
                  white_matrix_residual=matrix@amplitudes-rhs,
                  white_closure_defect=fields['outgoing']-amplitudes,
                  target_indices=targets,
                  stored_white_net_current=(d['weights'][d['nr']:, None]*(fields['outgoing']-amplitudes)).sum(axis=0))
    return fields

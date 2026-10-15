"""A declared side-wall angular trace model, never a 3D eigenreference.

Exact local white-return fact for a vertical normal: the axial cosine of an
incoming particle has density 2*sqrt(1-mu**2)/pi. Its first axial moment is zero,
second moment 1/4, and Legendre P2 moment -1/8.

The volume operator below ALSO assumes a regionwise constant boundary trace,
uniform transverse azimuth, and a straight prism. Those are model choices;
they do not follow from a saved scalar radial flux or qualify the heterogeneous
AAA transport solution. No coefficient may be fitted to the CE/SPOT gap.

For axial angular flux psi(mu), azimuth averaging gives outgoing wall current
sqrt(1-mu**2)*psi(mu)/pi. White incoming flux is constant on the incoming
hemisphere and is fixed by total outgoing current. Per cross-sectional volume,

  L psi = P/(pi*A) * s(mu) * (psi - integral(s*psi)/integral(s)),
  s(mu)=sqrt(1-mu**2).

Replacing both integrals by the SAME quadrature gives the conservative finite
angular model. Its weighted similarity transform is symmetric positive
semidefinite; isotropic flux is null, and no scalar particles are removed.
Continuous Legendre moments through P2 give wall-removal coefficients
0, 3*P/(16*A), 45*P/(256*A). These are conditional trace-model coefficients,
not independent removal cross sections measured in AAA.
"""
import numpy as np


def cosine_grid(mu, weights):
    mu=np.asarray(mu,dtype=float)
    weights=np.asarray(weights,dtype=float)
    if mu.ndim!=1 or weights.shape!=mu.shape or len(mu)<2:
        raise ValueError('complete one-dimensional angular grid required')
    if not np.isfinite(mu).all() or not np.isfinite(weights).all() or np.any(abs(mu)>=1) or np.any(weights<=0):
        raise ValueError('strictly interior cosines and positive finite weights required')
    if abs(weights.sum()-2)>8*np.finfo(np.float32).eps:
        raise ValueError('weights must integrate the full axial interval')
    return mu,weights,np.sqrt(1-mu*mu)


def trace_exchange(mu, weights, perimeter, area):
    mu,weights,s=cosine_grid(mu,weights)
    if not np.isfinite([perimeter,area]).all() or min(perimeter,area)<=0:
        raise ValueError('positive finite prism perimeter/area required')
    rate=perimeter/(np.pi*area)*s
    normalization=float(weights@rate)
    kernel=np.diag(rate)-np.outer(rate,weights*rate)/normalization
    return kernel


def white_return_density(mu):
    mu=np.asarray(mu,dtype=float)
    if not np.isfinite(mu).all() or np.any(abs(mu)>1):
        raise ValueError('axial cosine outside its physical interval')
    return 2/np.pi*np.sqrt(1-mu*mu)


def legendre_projection(kernel, mu, weights, order=2):
    mu,weights,_=cosine_grid(mu,weights)
    kernel=np.asarray(kernel,dtype=float)
    if kernel.shape!=(len(mu),len(mu)) or not np.isfinite(kernel).all():
        raise ValueError('complete finite directional operator required')
    polynomials=np.polynomial.legendre.legvander(mu,order)
    lifting=polynomials*(2*np.arange(order+1)+1)[None,:]/2
    testing=polynomials.T*weights[None,:]
    return testing@kernel@lifting


def projected_boundary_block(kernel, boundary_basis):
    """Weak-form constant-trace model; boundary_basis is an explicit input.

The returned mode-by-angle block uses radial weights normalized by whole
cross-sectional area, as in SPOT1P64. It does not infer a boundary trace from
the old radial response or silently enable any native solver modification.
"""
    basis=np.asarray(boundary_basis,dtype=float)
    if basis.ndim!=1 or not len(basis) or not np.isfinite(basis).all():
        raise ValueError('explicit complete boundary trial-space trace required')
    return np.einsum('ab,ij->aibj',np.outer(basis,basis),kernel)

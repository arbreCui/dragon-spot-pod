"""Independent Cartesian integrals and direct 1D controls, without ray quadrature."""
import math
import numpy as np
from scipy.integrate import quad


def source_field(length, total):
    return length if total == 0 else -math.expm1(-total*length)/total


def integrate(f, a, b, points=()):
    breaks = [a, *sorted(set(v for v in points if a < v < b)), b]
    return sum(quad(f, x, y, epsabs=2e-13, epsrel=2e-13)[0] for x,y in zip(breaks[:-1],breaks[1:]))


def one_d(s, totals, sources, S, orientation):
    """Direct forward solution; physical material/source order is explicit."""
    s = np.asarray(s); edges = np.linspace(0, S, len(totals)+1)
    ts = totals if orientation == 1 else totals[::-1]
    qs = sources if orientation == 1 else sources[::-1]
    out = np.full(s.shape, .4); upstream = .4
    for i,(total,q) in enumerate(zip(ts,qs)):
        mask = (s >= edges[i]) & ((s <= edges[i+1]) if i == len(ts)-1 else (s < edges[i+1]))
        ell = s[mask]-edges[i]
        B = ell if total == 0 else -np.expm1(-total*ell)/total
        out[mask] = np.exp(-total*ell)*upstream + q*B
        length = edges[i+1]-edges[i]
        upstream = math.exp(-total*length)*upstream + q*source_field(length,total)
    return out


def homogeneous(S,H,nr,nz,mu,orientation,total):
    x=np.linspace(0,S,nr+1); z=np.linspace(0,H,nz+1); m=abs(mu)
    integral=np.zeros((nr,nz)); face=np.zeros((nr,nz,4))
    def radial_integral(s,a,b):
        if m == 0:return (b-a)*source_field(s,total)
        return integrate(lambda zp:source_field(min(s,zp/m),total),a,b,[m*s])
    for i in range(nr):
        sa,sb=(x[i],x[i+1]) if orientation == 1 else (S-x[i+1],S-x[i])
        for j in range(nz):
            za,zb=(z[j],z[j+1]) if mu >= 0 else (H-z[j+1],H-z[j])
            integral[i,j]=integrate(lambda s:radial_integral(s,za,zb),sa,sb,[] if m==0 else [za/m,zb/m])
            face[i,j,1 if orientation == 1 else 0]=radial_integral(sb,za,zb)
            if m:
                face[i,j,3 if mu > 0 else 2]=m*integrate(lambda s:source_field(min(s,zb/m),total),sa,sb,[zb/m])
    return integral.reshape(-1),face.reshape(nr*nz,4)


def matched(S,H,nr,nz,mu,orientation,totals):
    x=np.linspace(0,S,nr+1);z=np.linspace(0,H,nz+1)
    source=np.array([1.] if nr==1 else [1.,.3]);integral=np.zeros((nr,nz));face=np.zeros((nr,nz,4))
    def field(s):return float(one_d(np.array(s),totals,source,S,orientation))
    for i in range(nr):
        sa,sb=(x[i],x[i+1]) if orientation==1 else (S-x[i+1],S-x[i])
        line=integrate(field,sa,sb)
        for j in range(nz):
            integral[i,j]=line*(z[j+1]-z[j])
            face[i,j,1 if orientation==1 else 0]=field(sb)*(z[j+1]-z[j])
            if mu:face[i,j,3 if mu>0 else 2]=abs(mu)*line
    return integral.reshape(-1),face.reshape(nr*nz,4)

"""Full axial-cell characteristic coefficients; no regional inverse-H lift."""
import numpy as np
from scipy.linalg import expm
from scipy.special import gammainc


def upwind(widths, sign=1, periodic=False):
    h=np.asarray(widths,float)
    if np.any(h<=0) or sign not in [-1,1]:raise ValueError('invalid axial grid/sign')
    n=len(h);d=np.zeros((n,n))
    for i in range(n):
        d[i,i]+=1/h[i];j=i-sign
        if periodic:d[i,j%n]-=1/h[i]
        elif 0<=j<n:d[i,j]-=1/h[i]
    return d


def scalar_integrals(length,total):
    l,s=np.broadcast_arrays(np.asarray(length,float),np.asarray(total,float))
    safe=np.where(s>0,s,1.);tau=s*l
    b=gammainc(1,tau)/safe
    own=(l*gammainc(1,tau)-gammainc(2,tau)/safe)/safe
    return np.where(s==0,l,b),np.where(s==0,l*l/2,own)


def polynomial_coefficients(length,total,rate,n,kind='exact',native_b=None,native_d=None):
    """Coefficients of powers of the upstream shift on a uniform vacuum grid.

    The shift is nilpotent of degree n, so n coefficients are the complete
    matrix function, not an axial-state approximation beyond the chosen grid.
    B/D coefficients are positive exponential integrals evaluated via gamma.
    """
    l,s,r=np.broadcast_arrays(np.asarray(length,float),np.asarray(total,float),np.asarray(rate,float))
    if np.any(l<0) or np.any(s<0) or np.any(r<0) or n<1:raise ValueError('nonnegative segment data required')
    alpha=s+r;safe=np.where(alpha>0,alpha,1.);tau=alpha*l
    t=np.zeros((*l.shape,n));b=np.zeros_like(t);own=np.zeros_like(t)
    t[...,0]=np.exp(-tau)
    factor=1/safe
    for k in range(n):
        if k:
            factor=factor*r/safe;t[...,k]=t[...,k-1]*r*l/k
        p=gammainc(k+1,tau);pn=gammainc(k+2,tau)
        b[...,k]=factor*p
        own[...,k]=factor*(l*p-(k+1)*pn/safe)
    b[...,0]=np.where(alpha==0,l,b[...,0]);own[...,0]=np.where(alpha==0,l*l/2,own[...,0])
    if kind=='native':
        if native_b is None or native_d is None:raise ValueError('native B/D required')
        b0,d0=scalar_integrals(l,s)
        bn,dn=np.broadcast_arrays(native_b,native_d)
        if np.any(l<=0) or np.any(bn<0) or np.any(dn<0):raise ValueError('positive native segment required')
        tn=1-s*bn
        if np.any(tn<0):raise ValueError('native scalar transmission is negative')
        t[...,0]=tn*np.exp(-r*l)
        for k in range(1,n):t[...,k]=t[...,k-1]*r*l/k
        b*=np.asarray(bn/b0)[...,None];own*=np.asarray(dn/d0)[...,None]
    elif kind!='exact':raise ValueError('unknown coefficient kernel')
    if not all(np.isfinite(x).all() for x in [t,b,own]):raise ArithmeticError('nonfinite coefficient')
    return t,b,own


def dense_coefficients(length,total,mu,widths,sign=1,periodic=False,native_b=None,native_d=None):
    d=abs(mu)*upwind(widths,sign,periodic);n=len(widths);a=total*np.eye(n)+d
    block=np.zeros((3*n,3*n));block[:n,:n]=-a;block[:n,n:2*n]=np.eye(n);block[n:2*n,2*n:]=np.eye(n)
    e=expm(length*block);t=e[:n,:n];b=e[:n,n:2*n];own=e[:n,2*n:]
    if native_b is not None:
        if native_d is None:raise ValueError('native own-source coefficient required')
        b0,d0=scalar_integrals(length,total)
        t=(1-total*native_b)*expm(-length*d);b=b*(native_b/b0);own=own*(native_d/d0)
    return t,b,own,a


def shift_matrix(coefficients,sign=1):
    c=np.asarray(coefficients);n=c.shape[-1];result=np.zeros((*c.shape[:-1],n,n))
    for k in range(n):
        row=np.arange(k,n) if sign==1 else np.arange(n-k)
        col=row-sign*k
        result[...,row,col]=c[...,k,None]
    return result


def green_sweep(d,a,n,height,kind):
    """Complete half-sign/polar radial Green function, as axial shift powers.

    Result axes: polar, shift power, output region/surface, source region/surface.
    A single sign has half of the historical planar weight. Both planar ray
    directions are explicitly swept. The other axial sign reverses cell order.
    """
    from qualify_native_signed_axial import axial_mu
    nr,nb,nl=d['nr'],d['nb'],len(d['track']);ns=nr+nb
    rate=np.zeros(nl) if n==0 else axial_mu(d)[d['polar']]/(height/n)
    order=max(n,1);gv=np.zeros((d['nmu'],nr,order,ns));gb=np.zeros((d['nmu'],nb,order,ns))
    stats=dict(min_T=1.,min_B=1.,min_D=1.,min_incoming=1.,min_outgoing=1.,min_integral=1.)
    for orientation in [1,-1]:
        end=np.zeros(nl,dtype=int) if orientation==1 else d['length']-1
        surface=-d['region'][np.arange(nl),end]-1
        incoming=np.zeros((nl,order,ns));incoming[np.arange(nl),0,nr+surface]=1
        for step in range(1,d['nmax']-1):
            lines=np.flatnonzero(step<d['length']-1)
            seg=np.full(len(lines),step) if orientation==1 else d['length'][lines]-1-step
            region=d['region'][lines,seg]-1;polar=d['polar'][lines]
            t,b,own=polynomial_coefficients(d['h'][lines,seg],a['total'][region],rate[lines],order,kind,
                                           a['b'][lines,seg],a['self_d'][lines,seg])
            for key,x in [('min_T',t),('min_B',b),('min_D',own)]:stats[key]=min(stats[key],float(x.min()))
            inc=incoming[lines];out=np.zeros_like(inc);integ=np.zeros_like(inc)
            for k in range(order):
                out[:,k:]+=t[:,k,None,None]*inc[:,:order-k]
                integ[:,k:]+=b[:,k,None,None]*inc[:,:order-k]
            index=np.arange(len(lines))[:,None];power=np.arange(order)[None,:]
            out[index,power,region[:,None]]+=b
            integ[index,power,region[:,None]]+=own
            for key,x in [('min_incoming',inc),('min_outgoing',out),('min_integral',integ)]:stats[key]=min(stats[key],float(x.min()))
            np.add.at(gv,(polar,region),integ*d['weight'][lines,None,None]/2)
            incoming[lines]=out
        end=d['length']-1 if orientation==1 else np.zeros(nl,dtype=int)
        surface=-d['region'][np.arange(nl),end]-1
        np.add.at(gb,(d['polar'],surface),incoming*d['weight'][:,None,None]/2)
    green=np.concatenate([gv,gb],axis=1).transpose(0,2,1,3)
    return green,stats


def expand_green(d,green):
    """Normalize and expand all cell shifts; keep both independent axial signs."""
    npole,n,ns,_=green.shape
    # Normalize every output by its original native region/surface measure.
    c=green/d['weights'][None,None,:,None]
    result=np.zeros((2,npole,ns*n,ns*n))
    for z,sign in enumerate([1,-1]):
        for p in range(npole):
            for k in range(n):
                row=np.arange(k,n) if sign==1 else np.arange(n-k);col=row-sign*k
                for i,j in zip(row,col):result[z,p].reshape(ns,n,ns,n)[:,i,:,j]=c[p,k]
    return result

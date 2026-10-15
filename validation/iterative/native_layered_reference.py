"""Independent rectangle-clipping rays and offset integration for physical inputs."""
import numpy as np
from functools import lru_cache
from decimal import Decimal, localcontext
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, quad_vec
from scipy.special import exprel, hyp1f1


def homogeneous_source(S,H,mu,total):
    """Constant unit volume source, all entering faces vacuum.

    Backward flights longer than t occupy area (S-t)*(H-|mu|*t).
    Integration of this survival area gives volume and both outgoing currents.
    This does not use the ray topology or characteristic implementation.
    """
    a=abs(mu);end=min(S,H/a)
    if total==0:
        return np.array([S*H*end-(S*a+H)*end**2/2+a*end**3/3,
                         H*end-a*end**2/2,a*(S*end-end**2/2)])
    functions=[lambda t:(S-t)*(H-a*t),lambda t:H-a*t,lambda t:a*(S-t)]
    return np.array([quad(lambda t:np.exp(-total*t)*f(t),0,end,epsabs=2e-14,epsrel=2e-14)[0] for f in functions])


class RectangleReference:
    def __init__(self,widths,regions,total,entry,exit_surface,H,nz,mu,orientation,q,radial,axial):
        self.widths=np.asarray(widths);self.regions=np.asarray(regions);self.total=np.asarray(total)
        self.entry=entry;self.exit=exit_surface;self.H=H;self.nz=nz;self.mu=mu;self.orientation=orientation
        self.q=q;self.radial=radial;self.axial=axial;self.k=q.shape[-1];self.nout=14*nz+16
        self.x=np.r_[0.,np.cumsum(widths)];self.S=self.x[-1];self.z=np.linspace(0,H,nz+1)
        # Build all cell rectangles, then intersect them with each whole line.
        # This is separate from the production-style sorted-crossing sweep.
        if orientation==1:lo,hi=self.x[:-1],self.x[1:]
        else:lo,hi=self.S-self.x[1:],self.S-self.x[:-1]
        self.radlo=np.repeat(lo,nz);self.radhi=np.repeat(hi,nz)
        self.zlo=np.tile(self.z[:-1],len(widths));self.zhi=np.tile(self.z[1:],len(widths))
        self.region=np.repeat(regions,nz);self.layer=np.tile(np.arange(nz),len(widths))
        self.source=q[self.region*nz+self.layer];self.sigma=self.total[self.region]
        self.breaks=np.unique((self.z[:,None]-mu*np.r_[lo,hi][None,:]).ravel())
        # Binary64 coordinates are the input data. Accumulate and intersect
        # them in decimal arithmetic so a tiny overlap is not obtained by
        # subtracting two rounded whole-track offsets. No geometry tolerance,
        # snapping, deleted sliver, or fitted source is introduced.
        with localcontext() as ctx:
            ctx.prec=50
            D=Decimal.from_float;self.dm=D(float(mu));self.dx=[Decimal(0)]
            for w in widths:self.dx.append(self.dx[-1]+D(float(w)))
            self.dz=[D(float(H))*j/nz for j in range(nz+1)]
            dl=self.dx[:-1] if orientation==1 else [self.dx[-1]-x for x in self.dx[1:]]
            dh=self.dx[1:] if orientation==1 else [self.dx[-1]-x for x in self.dx[:-1]]
            self.rectangles=[(dl[i],dh[i],self.dz[j],self.dz[j+1]) for i in range(len(widths)) for j in range(nz)]
            self.dbreaks=sorted(set(z-self.dm*x for z in self.dz for x in dl+dh))

    def ray(self,u,full=False):
        # Every node is an interior point of a topology interval.
        with localcontext() as ctx:
            ctx.prec=50
            if not isinstance(u,Decimal):u=Decimal.from_float(float(u))
            intersections=[]
            for c,(lo,hi,zlo,zhi) in enumerate(self.rectangles):
                za=(zlo-u)/self.dm;zb=(zhi-u)/self.dm
                a=max(lo,min(za,zb));b=min(hi,max(za,zb))
                if b>a:intersections.append((a,c,float(b-a),a==lo,b==hi))
            intersections.sort()
        active=np.array([r[1] for r in intersections],dtype=int)
        length=np.array([r[2] for r in intersections]);radin=[r[3] for r in intersections];radout=[r[4] for r in intersections]
        value=np.zeros((self.nout,self.k));fields=np.zeros((len(self.region),9,self.k)) if full else None
        if not len(active):return fields if full else value
        first=active[0];radial=radin[0]
        state=(self.radial[self.entry*self.nz+self.layer[first]] if radial else self.axial[self.region[first]]).copy()
        tau=self.sigma[active]*length
        # Integral identities independent of the worker's thin-cell series:
        # B=l*exprel(-tau), D=l*l/2 * 1F1(1;3;-tau).
        B=length*exprel(-tau);D=length**2*hyp1f1(1.,3.,-tau)/2;T=np.exp(-tau)
        for pos,c in enumerate(active):
            source=self.source[c];integral=B[pos]*state+D[pos]*source;out=T[pos]*state+B[pos]*source
            value[self.region[c]*self.nz+self.layer[c]]+=integral
            ins=(0 if self.orientation==1 else 1) if radin[pos] else (2 if self.mu>0 else 3)
            outs=(1 if self.orientation==1 else 0) if radout[pos] else (3 if self.mu>0 else 2)
            if full:fields[c,0]=integral;fields[c,1+ins]=state;fields[c,5+outs]=out
            if pos==len(active)-1:
                if outs<2:value[8*self.nz+self.exit*self.nz+self.layer[c]]+=out
                else:value[14*self.nz+(outs-2)*8+self.region[c]]+=out
            state=out
        return fields if full else value

    def fixed(self,order,full=False):
        gn,gw=leggauss(order)
        shape=(len(self.region),9,self.k) if full else (self.nout,self.k)
        result=np.zeros(shape)
        with localcontext() as ctx:
            ctx.prec=50
            for a,b in zip(self.dbreaks[:-1],self.dbreaks[1:]):
                for n,w in zip(gn,gw):
                    u=(a+b)/2+(b-a)*Decimal.from_float(float(n))/2
                    result+=self.ray(u,full)*float(b-a)*w/2
        return result

    def scale(self,values):
        result=np.empty_like(values)
        for start,stop in [(0,8*self.nz),(8*self.nz,14*self.nz),(14*self.nz,self.nout)]:
            result[start:stop]=abs(values[start:stop]).max(axis=0)
        return result

    def adaptive(self,approximation):
        scale=self.scale(approximation);normalizer=np.where(scale>0,scale,1.)
        result=np.zeros_like(approximation);error=0.;neval=0;statuses=[]
        count=len(self.dbreaks)-1
        def interval_value(index,t):
            with localcontext() as ctx:
                ctx.prec=50;a,b=self.dbreaks[index:index+2]
                u=a+(b-a)*Decimal.from_float(float(t))
                return self.ray(u)*float(b-a)/normalizer
        for interval in range(count):
            val,err,info=quad_vec(lambda t:interval_value(interval,t),0.,1.,epsabs=5e-14/count,
                epsrel=2e-14,norm='max',cache_size=1048576,limit=256,workers=1,quadrature='gk21',full_output=True)
            result+=val;error+=err;neval+=info.neval;statuses.append(int(info.status))
        vector_error=float(error)
        # Sum-of-interval vector maxima can accumulate unrelated components'
        # roundoff floors. Resolve that conservative bound by independently
        # integrating each output/input component, retaining QUADPACK's error
        # estimate for that component. Cache whole rays, not integrals.
        if error>=2e-13:
            @lru_cache(maxsize=2048)
            def evaluate(t):
                interval=min(int(t),count-1)
                return interval_value(interval,t-interval)
            result=np.zeros_like(approximation);errors=np.zeros_like(result)
            for index in np.ndindex(result.shape):
                val,err=quad(lambda t:float(evaluate(t)[index]),0.,float(count),
                    points=np.arange(1,count),epsabs=3e-14,epsrel=3e-14,limit=max(256,count*4))
                result[index]=val;errors[index]=err
            neval+=evaluate.cache_info().misses;error=float(errors.max())
            evaluate.cache_clear()
        return result*normalizer,dict(estimated_normalized_error=float(error),vector_conservative_error=vector_error,
            component_quadrature_used=vector_error>=2e-13,evaluations=neval,interval_statuses=statuses,
            zero_scale_handling='Unit normalization is only for integration; exact-zero columns must still compare exactly.')


def packed(result):
    return np.concatenate([result['volume'].reshape(-1,result['volume'].shape[-1]),
        result['radial'].reshape(-1,result['radial'].shape[-1]),result['axial'].reshape(-1,result['axial'].shape[-1])])

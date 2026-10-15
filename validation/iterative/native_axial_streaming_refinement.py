"""Bounded-memory application of the frozen full directional streaming model."""
import resource
import sys
import time
import numpy as np
from native_axial_streaming import green_sweep,upwind,polynomial_coefficients
from qualify_native_signed_axial import axial_mu,angular_measures
from qualify_native_directional import relative


class Budget:
    def __init__(self,mib,seconds):
        self.mib=mib;self.seconds=seconds;self.start=time.perf_counter()
    def snapshot(self):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return dict(elapsed_seconds=time.perf_counter()-self.start,
                    peak_rss_mib=rss/(1024**2 if sys.platform=='darwin' else 1024))
    def check(self):
        s=self.snapshot()
        if s['elapsed_seconds']>self.seconds or s['peak_rss_mib']>self.mib:
            raise RuntimeError(f'Predeclared resource cap exceeded: {s}')


def batched_green(d,a,n,height,kind,batch_lines,budget=None):
    if batch_lines<1:raise ValueError('batch_lines must be positive')
    total=np.zeros((d['nmu'],n,d['nr']+d['nb'],d['nr']+d['nb']))
    stats=None;defects=dict(incoming_defect_inf=0.,source_defect_inf_over_length=0.,segment_polar_samples=0)
    for start in range(0,len(d['track']),batch_lines):
        stop=min(start+batch_lines,len(d['track']));sl=slice(start,stop)
        x={k:d[k] for k in ['nr','nb','nmu','zmu','weights']}
        x.update({k:d[k][sl] for k in ['track','polar','length','region','h','weight']})
        x['nmax']=int(x['length'].max())
        y=dict(total=a['total'],b=a['b'][sl],self_d=a['self_d'][sl])
        piece,small=green_sweep(x,y,n,height,kind);total+=piece
        stats=small if stats is None else {k:min(stats[k],small[k]) for k in stats}
        line,seg=np.where(x['region']>0);region=x['region'][line,seg]-1
        length=x['h'][line,seg];sigma=y['total'][region]
        rate=axial_mu(x)[x['polar'][line]]*n/height
        t,b,own=polynomial_coefficients(length,sigma,rate,n,kind,y['b'][line,seg],y['self_d'][line,seg])
        incoming=t+(sigma+rate)[:,None]*b;source=b+(sigma+rate)[:,None]*own
        incoming[:,0]-=1;source[:,0]-=length
        incoming[:,1:]-=rate[:,None]*b[:,:-1];source[:,1:]-=rate[:,None]*own[:,:-1]
        defects['incoming_defect_inf']=max(defects['incoming_defect_inf'],float(np.sum(abs(incoming),axis=1).max()))
        defects['source_defect_inf_over_length']=max(defects['source_defect_inf_over_length'],float((np.sum(abs(source),axis=1)/length).max()))
        defects['segment_polar_samples']+=len(line)
        if budget:budget.check()
    return total,stats,defects


def apply_shift_green(coefficients,source):
    """Apply every retained shift directly, without an expanded cell matrix."""
    npole,n,ns,_=coefficients.shape
    result=np.zeros((2,npole,ns,n,source.shape[-1]))
    for z in range(2):
        for p in range(npole):
            for k in range(n):
                target=slice(k,n) if z==0 else slice(0,n-k)
                origin=slice(0,n-k) if z==0 else slice(k,n)
                result[z,p,:,target]+=np.einsum('oi,ijc->ojc',coefficients[p,k],source[:,origin])
    return result


def white_return_matrix(coefficients,nr):
    npole,n,ns,_=coefficients.shape;nb=ns-nr
    c=coefficients[:,:,nr:,nr:].sum(axis=0);result=np.zeros((nb,n,nb,n))
    for k in range(n):
        for i in range(n-k):
            result[:,i+k,:,i]+=c[k]
            result[:,i,:,i+k]+=c[k]
    return result.reshape(nb*n,nb*n)


def heldout_boundary(d,a,green,n,height,boundary):
    """Two positive sources, vacuum axial faces, unchanged common radial return."""
    nr,nb,npole=d['nr'],d['nb'],d['nmu'];nv=nr*n;h=height/n
    if boundary not in ['vacuum','white']:raise ValueError('unknown radial boundary')
    coefficients=green/d['weights'][None,None,:,None];mu=axial_mu(d);vw,sw=angular_measures(d)
    q=np.ones((nr,n,2));q[:,:,-1]=np.arange(1,nr+1)[:,None]/nr
    source=np.concatenate([q,np.zeros((nb,n,2))],axis=0)
    births=apply_shift_green(coefficients,source)
    tbb=white_return_matrix(coefficients,nr)
    inverse=np.linalg.solve(np.eye(nb*n)-tbb,np.eye(nb*n)) if boundary=='white' else np.eye(nb*n)
    incoming=inverse@births[:,:,nr:].sum(axis=(0,1)).reshape(nb*n,2) if boundary=='white' else np.zeros((nb*n,2))
    boundary_source=np.concatenate([np.zeros_like(q),incoming.reshape(nb,n,2)],axis=0)
    half=births+apply_shift_green(coefficients,boundary_source)
    phi_half=half[:,:,:nr]
    out_half=half[:,:,nr:]
    phi=phi_half.sum(axis=(0,1));jz=np.einsum('pric,p->ric',phi_half[0]-phi_half[1],mu)
    outgoing=out_half.sum(axis=(0,1));incoming=incoming.reshape(nb,n,2)
    fp=np.zeros((npole,nr,n+1,2));fm=np.zeros_like(fp)
    fp[:,:,1:]=phi_half[0];fm[:,:,:-1]=phi_half[1]
    faces=np.einsum('pric,p->ric',fp-fm,mu);faces2=np.einsum('pric,p->ric',fp+fm,mu**2)
    v=d['weights'][:nr];surface=d['weights'][nr:]
    born=h*np.einsum('ric,r->ic',q,2*vw.sum(axis=0))
    r_in=h*np.einsum('sic,s->ic',incoming,2*sw.sum(axis=0))
    r_out=h*np.einsum('sic,s->ic',outgoing,surface)
    collision=h*np.einsum('ric,r->ic',phi,v*a['total'])
    axial_loss=np.einsum('ric,r->ic',np.diff(faces,axis=1),v)
    residual=born+r_in-r_out-collision-axial_loss
    r_out_odd=h*np.einsum('psic,p,s->ic',out_half[0]-out_half[1],mu,surface)
    odd_collision=h*np.einsum('ric,r->ic',jz,v*a['total'])
    odd_loss=np.einsum('ric,r->ic',np.diff(faces2,axis=1),v)
    odd_residual=-r_out_odd-odd_collision-odd_loss
    ax_enter=np.einsum('pric,p,r->ic',fp[:,:,:-1]+fm[:,:,1:],mu,v)
    ax_enter_odd=np.einsum('pric,p,r->ic',fp[:,:,:-1]+fm[:,:,1:],mu**2,v)
    source_odd_abs=h*np.einsum('ric,pr,p->ic',q,2*vw,mu)
    radial_odd_abs=h*np.einsum('sic,ps,p->ic',incoming,2*sw,mu)
    even_cell=abs(residual)/np.maximum(born+r_in+ax_enter,1e-300)
    odd_cell=abs(odd_residual)/np.maximum(source_odd_abs+radial_odd_abs+ax_enter_odd,1e-300)
    even_global=abs(residual.sum(axis=0))/born.sum(axis=0)
    odd_global=abs(odd_residual.sum(axis=0))/source_odd_abs.sum(axis=0)
    stream_even=np.zeros((n,2));stream_odd=np.zeros_like(stream_even)
    for z,sign in enumerate([1,-1]):
        du=upwind([h]*n,sign)
        for p in range(npole):
            action=np.einsum('ij,rjc->ric',du,phi_half[z,p])
            term=h*mu[p]*np.einsum('ric,r->ic',action,v)
            stream_even+=term;stream_odd+=sign*mu[p]*term
    face_error=max(float(np.max(abs(stream_even-axial_loss))),float(np.max(abs(stream_odd-odd_loss))))
    closure=relative(incoming,outgoing) if boundary=='white' else float(np.max(abs(incoming)))
    escape=np.einsum('prc,p,r->c',fp[:,:,-1]+fm[:,:,0],mu,v)
    row=dict(n=n,boundary=boundary,cases=2,min_response=min(0.,float(coefficients.min())),min_white_inverse=float(inverse.min()),
             min_incoming=float(incoming.min()),min_half_flux=float(phi_half.min()),min_half_outgoing=float(out_half.min()),
             even_global_balance_relative=float(even_global.max()),odd_global_balance_relative=float(odd_global.max()),
             even_cell_balance_relative=float(even_cell.max()),odd_cell_balance_relative=float(odd_cell.max()),
             face_streaming_consistency_absolute=face_error,radial_boundary_relative=closure,axial_escape=escape.tolist())
    fields=dict(phi=phi,jz=jz,half_flux=phi_half,half_outgoing=out_half,incoming=incoming,
                face_current=faces,face_second_moment=faces2,volume_source=q,
                even_cell_defect=residual,odd_cell_defect=odd_residual,even_cell_relative=even_cell,odd_cell_relative=odd_cell,
                even_global_relative=even_global,odd_global_relative=odd_global,white_inverse=inverse,axial_escape=escape)
    return row,fields


def mesh_difference(coarse,fine,volume,height):
    c=coarse['phi'];f=fine['phi'];nr,n,nc=c.shape
    if f.shape!=(nr,2*n,nc):raise ValueError('nested factor-two meshes required')
    restricted=f.reshape(nr,n,2,nc).mean(axis=2);weight=volume[:,None,None]*height/n
    flux=np.sqrt(np.sum(weight*(c-restricted)**2,axis=(0,1))/np.sum(weight*restricted**2,axis=(0,1)))
    escape=abs(coarse['axial_escape']-fine['axial_escape'])/fine['axial_escape']
    return flux,escape

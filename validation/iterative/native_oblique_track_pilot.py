"""Full source-coordinate native-path pilot with bounded column batches."""
import math
import numpy as np
from scipy.integrate import quad
from axial_cell_characteristic import coefficients
from oblique_strip_geometry import relative,boundary_mask


def direct_flight(widths,totals,regions,entry_surface,orientation):
    """Independent literal 1D action; B/D come from ordinary scalar quadrature."""
    nr=len(widths);q=np.eye(14)[regions];inc=np.zeros((nr,14));out=inc.copy();integ=inc.copy()
    state=np.eye(14)[8+entry_surface].copy()
    indices=range(nr) if orientation==1 else range(nr-1,-1,-1)
    for i in indices:
        l,s=float(widths[i]),float(totals[i]);t=math.exp(-s*l)
        b=quad(lambda x:math.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0]
        d=quad(lambda x:(l-x)*math.exp(-s*x),0,l,epsabs=1e-13,epsrel=1e-13)[0]
        inc[i]=state;out[i]=t*state+b*q[i];integ[i]=b*state+d*q[i];state=out[i].copy()
    return dict(source=q,incoming=inc,outgoing=out,integral=integ,track_integral=integ.sum(axis=0),track_outgoing=state)


def reference_at(g,totals,flight,s):
    x=s if g['orientation']==1 else float(g['S'])-s
    i=np.minimum(np.searchsorted(g['x'],x,side='right')-1,len(totals)-1)
    assert np.all(i>=0)
    length=x-g['x'][i] if g['orientation']==1 else g['x'][i+1]-x
    assert np.min(length)>=0
    sig=totals[i];safe=np.where(sig>0,sig,1.);b=np.where(sig==0,length,-np.expm1(-sig*length)/safe)
    return np.exp(-sig*length)[:,None]*flight['incoming'][i]+b[:,None]*flight['source'][i]


def problem(g,totals,regions,flight):
    nr,nz=int(g['nr']),int(g['nz']);c=nr*nz;u=c+nz+nr;k=u+16
    q=np.zeros((c,k));q[:,:c]=np.eye(c);sigma=np.repeat(totals,nz)
    q[:,u]=sigma;q[:,u+1]=np.repeat((regions+1)/8,nz)*np.tile(np.arange(nz)%2,nr)
    q[:,u+2:]=np.repeat(flight['source'],nz,axis=0)
    inflow=np.zeros((len(g['u']),k));radial=g['entry_side']<2
    cols=np.where(radial,c+g['entry_cell']%nz,c+nz+g['entry_cell']//nz)
    inflow[np.arange(len(inflow)),cols]=1;inflow[:,u]=1
    inflow[:,u+2:]=reference_at(g,totals,flight,g['entry_s'])
    assembly=np.zeros((c,8*nz));assembly[np.arange(c),np.repeat(regions,nz)*nz+np.tile(np.arange(nz),nr)]=1
    return q,inflow,u,sigma,assembly


def transport(g,totals,regions,flight,half_weight,native_mx,effective_orientation,column_batch=16):
    q,inflow,u,sigma,assembly=problem(g,totals,regions,flight)
    c,k=q.shape;ray,cell=g['ray'],g['cell'];length=g['length'];n=len(ray)
    t,b,d=coefficients(length,sigma[cell]);integral=np.zeros((c,k));fi=np.zeros((c,4,k));fo=fi.copy()
    minimum_angle=np.full(n,np.inf);minimum_integral=minimum_angle.copy()
    worst=np.full(n,-1.);worst_defect=np.zeros(n);worst_scale=np.zeros(n);worst_column=np.zeros(n,int)
    piece_relative=np.zeros(k);matched_exit=np.zeros((len(g['u']),14));endpoint_error=np.zeros(14)
    input_min_angle=np.full(k,np.inf);input_min_integral=input_min_angle.copy()
    input_worst=np.full(k,-1.);input_piece=np.zeros(k,int);input_witness=np.zeros((k,5))
    ref0=reference_at(g,totals,flight,g['s0']);ref1=reference_at(g,totals,flight,g['s1'])
    refscale=np.maximum(ref0.max(axis=0),ref1.max(axis=0))
    steps=[np.flatnonzero(g['step']==step) for step in range(int(g['step'].max())+1)]
    for first in range(0,k,column_batch):
        stop=min(first+column_batch,k);state=inflow[:,first:stop].copy()
        for ix in steps:
            rr,cc=ray[ix],cell[ix];psi=state[rr].copy();source=q[cc,first:stop]
            value=b[ix,None]*psi+d[ix,None]*source;out=t[ix,None]*psi+b[ix,None]*source
            w=g['weight'][rr,None]
            np.add.at(integral[:,first:stop],cc,w*value)
            np.add.at(fi[:,:,first:stop],(cc,g['in_side'][ix]),w*psi)
            np.add.at(fo[:,:,first:stop],(cc,g['out_side'][ix]),w*out)
            defect=out-psi+sigma[cc,None]*value-length[ix,None]*source
            scale=psi+length[ix,None]*source;error=relative(defect,scale);col=error.argmax(axis=1)
            maximum=error[np.arange(len(ix)),col];replace=maximum>worst[ix];at=ix[replace];pick=col[replace]
            worst[at]=maximum[replace];worst_defect[at]=defect[replace,pick];worst_scale[at]=scale[replace,pick];worst_column[at]=first+pick
            piece_relative[first:stop]=np.maximum(piece_relative[first:stop],error.max(axis=0))
            arg=error.argmax(axis=0);cols=np.arange(stop-first);maxima=error[arg,cols]
            take=maxima>input_worst[first:stop];ccase=first+cols[take];rrcase=arg[take];local=cols[take]
            input_worst[ccase]=maxima[take];input_piece[ccase]=ix[rrcase]
            input_witness[ccase]=np.column_stack([psi[rrcase,local],out[rrcase,local],value[rrcase,local],defect[rrcase,local],scale[rrcase,local]])
            input_min_angle[first:stop]=np.minimum(input_min_angle[first:stop],np.minimum(psi.min(axis=0),out.min(axis=0)))
            input_min_integral[first:stop]=np.minimum(input_min_integral[first:stop],value.min(axis=0))
            minimum_angle[ix]=np.minimum(minimum_angle[ix],np.minimum(psi.min(axis=1),out.min(axis=1)))
            minimum_integral[ix]=np.minimum(minimum_integral[ix],value.min(axis=1))
            lo=max(first,u+2)
            if lo<stop:
                a,b0=lo-first,lo-(u+2);j=stop-(u+2)
                endpoint_error[b0:j]=np.maximum(endpoint_error[b0:j],np.maximum(
                    abs(psi[:,a:]-ref0[ix,b0:j]).max(axis=0),abs(out[:,a:]-ref1[ix,b0:j]).max(axis=0)))
            state[rr]=out
        lo=max(first,u+2)
        if lo<stop:matched_exit[:,lo-(u+2):stop-(u+2)]=state[:,lo-first:]
    birth=g['area'][:,None]*q;scale=birth+fi.sum(axis=1)
    defect=birth+fi.sum(axis=1)-fo.sum(axis=1)-sigma[:,None]*integral
    mask=boundary_mask(g);supply=birth.sum(axis=0)+fi[mask].sum(axis=0)
    global_defect=supply-fo[mask].sum(axis=0)-(sigma[:,None]*integral).sum(axis=0)
    nr,nz=int(g['nr']),int(g['nz']);inf=fi.reshape(nr,nz,4,k);outf=fo.reshape(nr,nz,4,k)
    aa,bb=(outf[:-1,:,1],inf[1:,:,0]) if g['orientation']==1 else (outf[1:,:,0],inf[:-1,:,1])
    sd=[(aa-bb).reshape(-1,k)];ss=[(abs(aa)+abs(bb)).reshape(-1,k)]
    aa,bb=(outf[:,:-1,3],inf[:,1:,2]) if g['mu']>0 else (outf[:,1:,2],inf[:,:-1,3])
    sd.append((aa-bb).reshape(-1,k));ss.append((abs(aa)+abs(bb)).reshape(-1,k))
    partial=(assembly.T@integral).reshape(8,nz,k)*half_weight
    # Explicit source assembly retains every regional/axial input coordinate.
    regional_response=(assembly.T@integral[:,:c]@assembly)*half_weight
    regional_alt=np.repeat(np.arange(1,9)/8,nz)*np.tile(np.arange(nz)%2,8)
    assembly_errors=[]
    for value in [integral,fi,fo]:
        alt=value[...,:c]@(assembly@regional_alt)
        const=value[...,:c]@sigma+value[...,c:u].sum(axis=-1)
        assembly_errors.extend([float(relative(alt-value[...,u+1],abs(value[...,u+1]).max()).max()),
                                float(relative(const-value[...,u],abs(value[...,u]).max()).max())])
    return dict(q=q,units=np.array(u),total=sigma,source_assembly=assembly,integral=integral,face_in=fi,face_out=fo,
        matched_incoming=inflow[:,u+2:],matched_exit_angle=matched_exit,T=t,B=b,D=d,
        minimum_piece_angle=minimum_angle,minimum_piece_integral=minimum_integral,
        worst_piece_signed_defect=worst_defect,worst_piece_scale=worst_scale,worst_piece_column=worst_column,
        maximum_piece_relative=piece_relative,cell_birth=birth,cell_scale=scale,cell_defect=defect,
        global_scale=supply,global_defect=global_defect,shared_defect=np.concatenate(sd),shared_scale=np.concatenate(ss),
        matched_endpoint_defect=endpoint_error,matched_endpoint_scale=refscale,
        minimum_input_angle=input_min_angle,minimum_input_integral=input_min_integral,
        worst_input_piece=input_piece,worst_input_witness=input_witness,
        partial_regional_integral=partial,partial_regional_jx=partial*(effective_orientation*native_mx),
        partial_regional_jz=partial*float(g['mu']),regional_response=regional_response,
        source_assembly_relative=np.array(assembly_errors),native_half_weight=np.array(half_weight))


def matched_fields(g,flight):
    nr,nz=int(g['nr']),int(g['nz']);k=14;dz=np.diff(g['z'])
    volume=(flight['integral'][:,None,:]*dz[None,:,None]).reshape(nr*nz,k)
    face=np.zeros((nr,nz,4,k));xs=1 if g['orientation']==1 else 0;zs=3 if g['mu']>0 else 2
    face[:,:,xs]=flight['outgoing'][:,None,:]*dz[None,:,None]
    face[:,:,zs]=abs(float(g['mu']))*flight['integral'][:,None,:]
    return volume,face.reshape(nr*nz,4,k)


def column_error(value,ref):
    scale=abs(ref).max(axis=tuple(range(ref.ndim-1)))
    return float(relative(value-ref,scale).max())


def reflections(target,ref,nr,nz,axis):
    c=nr*nz;u=int(target['units']);cells=np.arange(c).reshape(nr,nz)
    perm=(cells[:,::-1] if axis=='z' else cells[::-1,:]).ravel()
    radial=np.arange(c,c+nz);axial=np.arange(c+nz,u)
    if axis=='z':radial=radial[::-1]
    else:axial=axial[::-1]
    cols=np.r_[perm,radial,axial,u,np.arange(u+2,u+16)]
    actualcols=np.r_[np.arange(u+1),np.arange(u+2,u+16)]
    sides=[0,1,3,2] if axis=='z' else [1,0,2,3];error=0.
    for key in ['integral','face_in','face_out']:
        v=ref[key][perm]
        if v.ndim==3:v=v[:,sides]
        error=max(error,column_error(target[key][...,actualcols],v[...,cols]))
    return error

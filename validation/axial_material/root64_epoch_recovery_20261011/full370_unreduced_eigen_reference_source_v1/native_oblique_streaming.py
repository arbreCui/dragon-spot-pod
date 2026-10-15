"""Original-coordinate streaming kernel and independent full-flight quadrature."""
import ctypes
import numpy as np
from numpy.polynomial.legendre import leggauss

METRICS=['minimum_angle','minimum_integral','primitive_relative','primitive_index',
 'primitive_in','primitive_out','primitive_integral','primitive_defect','primitive_scale','primitive_length','primitive_total','primitive_source',
 'cell_relative','cell_index','cell_birth','cell_in','cell_out','cell_collision','cell_defect','cell_scale',
 'global_birth','global_in','global_out','global_collision','global_defect','global_scale',
 'point_abs_error','point_scale','integral_abs_error','integral_scale','outface_abs_error','outface_scale',
 'track_integral','track_radial_out','reference_track_integral','reference_track_out',
 'point_piece','point_end','point_actual','point_reference','integral_cell','integral_actual','integral_reference',
 'outface_index','outface_actual','outface_reference','source_assembly_relative','shared_face_abs_error']


def independent_flight(widths,counts,regions,totals,entrance,orientation,order=64):
    """GL quadrature of B and D, independent of the characteristic series.

    No native PJJ or tabulated primitive is used. Callers calibrate every
    original track/polar/group against the sealed exact whole-flight action.
    """
    widths=np.asarray(widths);counts=np.asarray(counts);ng=len(totals);nt=len(counts)
    gn,gw=leggauss(order);active=np.arange(15)[None,:]<counts[:,None]
    safe_regions=np.where(active,regions,0)
    sigma=np.asarray(totals)[:,safe_regions]
    s=widths[:,:,None]*(gn+1)/2;w=widths[:,:,None]*gw/2
    attenuation=np.exp(-sigma[:,:,:,None]*s[None,:,:,:])
    b=(attenuation*w).sum(axis=-1)
    d=(attenuation*(widths[:,:,None]-s)*w).sum(axis=-1)
    t=np.exp(-sigma*widths)
    out={k:np.zeros((ng,nt,15,14)) for k in ['incoming','outgoing','integral']}
    state=np.broadcast_to(np.eye(14)[8+np.asarray(entrance)],(ng,nt,14)).copy()
    for step in range(int(counts.max())):
        ix=np.flatnonzero(step<counts);seg=np.full(len(ix),step) if orientation==1 else counts[ix]-1-step
        q=np.eye(14)[regions[ix,seg]]
        out['incoming'][:,ix,seg]=state[:,ix]
        value=b[:,ix,seg,None]*state[:,ix]+d[:,ix,seg,None]*q
        state[:,ix]=t[:,ix,seg,None]*state[:,ix]+b[:,ix,seg,None]*q
        out['integral'][:,ix,seg]=value;out['outgoing'][:,ix,seg]=state[:,ix]
    return out


def transport(library,widths,counts,regions,totals,reference,H,nz,mu,orientation,order,debug=False):
    widths=np.ascontiguousarray(widths,dtype=np.float64);counts=np.ascontiguousarray(counts,dtype=np.int32)
    regions=np.ascontiguousarray(regions,dtype=np.int32);totals=np.ascontiguousarray(totals,dtype=np.float64)
    nt=len(counts);ng=len(totals)
    if widths.shape!=(nt,15) or regions.shape!=(nt,15) or totals.shape!=(ng,8):raise ValueError('original native-coordinate shapes required')
    refs=[np.ascontiguousarray(reference[k],dtype=np.float64) for k in ['incoming','outgoing','integral']]
    if any(r.shape!=(ng,nt,15,14) for r in refs):raise ValueError('full 14-coordinate reference required')
    geom=np.zeros((nt,6));metrics=np.zeros((nt,ng,16,len(METRICS)));regional=np.zeros((nt,ng,8,nz,14))
    fields=np.zeros((nt,ng,15*nz,9,16)) if debug else None
    gn,gw=leggauss(order);kernel=ctypes.CDLL(str(library)).streaming_transport;ptr=ctypes.c_void_p
    kernel.argtypes=[ctypes.c_int]*2+[ptr]*7+[ctypes.c_double,ctypes.c_int,ctypes.c_double,ctypes.c_int,ctypes.c_int]+[ptr]*6
    kernel.restype=ctypes.c_int
    rc=kernel(nt,ng,counts.ctypes.data,widths.ctypes.data,regions.ctypes.data,totals.ctypes.data,
        *[r.ctypes.data for r in refs],H,nz,mu,orientation,order,gn.ctypes.data,gw.ctypes.data,geom.ctypes.data,metrics.ctypes.data,regional.ctypes.data,
        fields.ctypes.data if fields is not None else None)
    if rc:raise RuntimeError(f'bounded oblique transport failed with code {rc}')
    return dict(geometry=geom,metrics=metrics,regional=regional,**({'fields':fields} if debug else {}))


def ratio(defect,scale):
    defect,scale=np.broadcast_arrays(abs(defect),scale)
    value=np.divide(defect,scale,out=np.zeros_like(defect),where=scale>0)
    value[(scale==0)&(defect!=0)]=np.inf
    return value


def checks(result,order):
    m=result['metrics'];g=result['geometry']
    row=dict(minimum_angle=float(m[...,0].min()),minimum_integral=float(m[...,1].min()),
        primitive_relative=float(m[...,2].max()),cell_relative=float(m[...,12].max()),
        global_relative=float(ratio(m[...,24],m[...,25]).max()),point_relative=float(ratio(m[...,26],m[...,27]).max()),
        integral_relative=float(ratio(m[...,28],m[...,29]).max()),outface_relative=float(ratio(m[...,30],m[...,31]).max()),
        source_assembly_relative=float(m[...,46].max()),shared_face_abs_error=float(m[...,47].max()),
        geometry_relative=float(g[:,3].max()),represented_width_relative=float(g[:,5].max()),
        finite=bool(all(np.isfinite(v).all() for v in result.values())),order=int(order))
    # Constant control at both orders; matched quadrature-dependent fields are
    # gated at order 16 and retained diagnostically at order 8.
    row['constant_integral_relative']=float(ratio(m[:,:,15,28],m[:,:,15,29]).max())
    row['constant_outface_relative']=float(ratio(m[:,:,15,30],m[:,:,15,31]).max())
    row['passed']=bool(row['finite'] and min(row['minimum_angle'],row['minimum_integral'])>=0
        and max(row[k] for k in ['primitive_relative','cell_relative','global_relative'])<1e-10
        and max(row[k] for k in ['point_relative','source_assembly_relative','geometry_relative','represented_width_relative','constant_integral_relative','constant_outface_relative'])<5e-12
        and row['shared_face_abs_error']==0
        and (order==8 or max(row['integral_relative'],row['outface_relative'])<5e-12))
    return row

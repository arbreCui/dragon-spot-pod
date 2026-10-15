"""Full layered source coordinates and physical boundary transport."""
import ctypes
from functools import lru_cache
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_oblique_streaming import ratio

METRICS=['minimum_angle','minimum_integral','primitive_relative','primitive_index',
 'primitive_in','primitive_out','primitive_integral','primitive_defect','primitive_scale','primitive_length','primitive_total','primitive_source',
 'cell_relative','cell_index','cell_birth','cell_in','cell_out','cell_collision','cell_defect','cell_scale',
 'global_birth','global_in','global_out','global_collision','global_defect','global_scale','shared_face_absolute']


def basis(nz,total,controls=True):
    n=14*nz+8;k=n+2 if controls else n
    q=np.zeros((8*nz,k));rad=np.zeros((6*nz,k));ax=np.zeros((8,k))
    q[:,:8*nz]=np.eye(8*nz);rad[:,8*nz:14*nz]=np.eye(6*nz);ax[:,14*nz:n]=np.eye(8)
    if controls:
        # Last two columns are swept separately, not computed from the basis.
        alpha=(np.arange(n)+1)/(n+1)
        q[:,n]=alpha[:8*nz];rad[:,n]=alpha[8*nz:14*nz];ax[:,n]=alpha[14*nz:]
        q[:,n+1]=np.repeat(total,nz);rad[:,n+1]=1.;ax[:,n+1]=1.
    return q,rad,ax


@lru_cache(maxsize=4)
def kernel(library):
    f=ctypes.CDLL(str(library)).layered_transport;p=ctypes.c_void_p
    f.argtypes=[ctypes.c_int]*3+[p]*3+[ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_int]+[p]*5+[ctypes.c_int]+[p]*4
    f.restype=ctypes.c_int
    return f


def transport(library,widths,regions,total,entry,H,nz,mu,orientation,order,q=None,radial=None,axial=None,matched_reference=None):
    w=np.ascontiguousarray(widths,dtype='d');r=np.ascontiguousarray(regions,dtype=np.int32);sig=np.ascontiguousarray(total,dtype='d')
    if w.ndim!=1 or r.shape!=w.shape or sig.shape!=(8,):raise ValueError('original segment map and eight totals required')
    if q is None:q,radial,axial=basis(nz,sig)
    q,radial,axial=[np.ascontiguousarray(v,dtype='d') for v in [q,radial,axial]]
    k=q.shape[-1]
    if q.shape!=(8*nz,k) or radial.shape!=(6*nz,k) or axial.shape!=(8,k):raise ValueError('all layer/surface/axial input coordinates required')
    if any(not np.isfinite(v).all() or v.min()<0 for v in [q,radial,axial]):raise ValueError('physical basis controls must be finite and nonnegative')
    ref=None if matched_reference is None else np.ascontiguousarray(matched_reference,dtype='d')
    if ref is not None and (ref.shape!=(len(w),k) or not np.isfinite(ref).all() or ref.min()<0):raise ValueError('invalid matched-regression reference')
    gn,gw=leggauss(order);g=np.zeros(6);f=np.zeros((len(w)*nz,9,k));m=np.zeros((k,len(METRICS)))
    rc=kernel(str(library))(len(w),nz,k,w.ctypes.data,r.ctypes.data,sig.ctypes.data,int(entry),H,mu,orientation,order,
        gn.ctypes.data,gw.ctypes.data,q.ctypes.data,radial.ctypes.data,axial.ctypes.data,int(ref is not None),
        None if ref is None else ref.ctypes.data,g.ctypes.data,f.ctypes.data,m.ctypes.data)
    if rc:raise RuntimeError(f'layered transport failed with code {rc}')
    return dict(geometry=g,fields=f,metrics=m,q=q,radial_input=radial,axial_input=axial)


def aggregate(fields,regions,nz,orientation,exit_surface):
    nr=len(regions);k=fields.shape[-1];f=fields.reshape(nr,nz,9,k)
    volume=np.zeros((8,nz,k));radial=np.zeros((6,nz,k));axial=np.zeros((2,8,k))
    np.add.at(volume,regions,f[:,:,0])
    end=nr-1 if orientation==1 else 0;radial[exit_surface]=f[end,:,6 if orientation==1 else 5]
    np.add.at(axial[0],regions,f[:,0,7]);np.add.at(axial[1],regions,f[:,-1,8])
    return dict(volume=volume,radial=radial,axial=axial)


def checks(result,widths,regions,total,H,nz,mu):
    f=result['fields'];m=result['metrics'];g=result['geometry'];q=result['q'];nr=len(widths);k=q.shape[-1]
    born=np.repeat(widths,nz)[:,None]*(H/nz)*q[(np.repeat(regions,nz)*nz+np.tile(np.arange(nz),nr))]
    collision=np.repeat(np.asarray(total)[regions],nz)[:,None]*f[:,0]
    defect=born+f[:,1:5].sum(axis=1)-f[:,5:9].sum(axis=1)-collision
    cell=float(ratio(defect,born+f[:,1:5].sum(axis=1)).max())
    row=dict(primitive_relative=float(m[:,2].max()),cell_relative=cell,global_relative=float(ratio(m[:,24],m[:,25]).max()),
        minimum_angle=float(m[:,0].min()),minimum_integral=float(m[:,1].min()),shared_face_absolute=float(m[:,26].max()),
        geometry_relative=float(g[3]),represented_width_relative=float(g[5]))
    n=14*nz+8
    if k==n+2:
        coefficients=np.stack([(np.arange(n)+1)/(n+1),np.r_[np.repeat(total,nz),np.ones(6*nz+8)]],axis=1)
        row['source_assembly_relative']=float(ratio(f[:,:,:n]@coefficients-f[:,:,n:],abs(f[:,:,n:]).max(axis=(0,1))).max())
        expected=np.zeros((nr*nz,9));expected[:,0]=np.repeat(widths,nz)*(H/nz)
        orientation_inferred=int(np.argmax(f.reshape(nr,nz,9,k)[0,0,1:3,-1]))
        # Every physical face has exactly one active direction for a state.
        expected[:,1+orientation_inferred]=H/nz;expected[:,5+(orientation_inferred^1)]=H/nz
        zs=2 if mu>0 else 3;expected[:,1+zs]=abs(mu)*np.repeat(widths,nz);expected[:,5+(zs^1)]=expected[:,1+zs]
        row['constant_relative']=float(ratio(f[:,:,-1]-expected,expected).max())
        incoming_axial=f.reshape(nr,nz,9,k)[:,0 if mu>0 else -1,1+zs,:14*nz]
        row['vacuum_axial_incoming_absolute']=float(abs(incoming_axial).max())
    row['passed']=bool(np.isfinite(f).all() and np.isfinite(m).all() and min(row['minimum_angle'],row['minimum_integral'])>=0
        and max(row[x] for x in ['primitive_relative','cell_relative','global_relative'])<1e-10
        and max(row[x] for x in ['geometry_relative','represented_width_relative'])<5e-12
        and row['shared_face_absolute']==0 and row.get('source_assembly_relative',0)<5e-12
        and row.get('constant_relative',0)<5e-12 and row.get('vacuum_axial_incoming_absolute',0)==0)
    return row

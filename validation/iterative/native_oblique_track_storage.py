"""Exact geometry/assembled-response packing, plus declared primitive certificates."""
import numpy as np


DERIVED_GEOMETRY={'ray','step','cell','in_side','out_side','s0','s1','length','volume','face_in_measure',
    'face_out_measure','area','face_measure','represented_widths'}


def unpack_geometry(p):
    g={k:v for k,v in p.items() if k not in ['piece_pointer','piece_cell','piece_end','piece_out_side']}
    counts=np.diff(p['piece_pointer'].astype(np.int64));rays=len(counts);n=int(counts.sum())
    ray=np.repeat(np.arange(rays),counts);step=np.arange(n)-np.repeat(p['piece_pointer'][:-1].astype(np.int64),counts)
    cell=p['piece_cell'].astype(np.int64);side=p['piece_out_side'].astype(np.int64);s1=p['piece_end']
    previous=np.maximum(np.arange(n)-1,0);s0=np.where(step==0,g['entry_s'][ray],s1[previous])
    incoming=np.where(step==0,g['entry_side'][ray],side[previous]^1)
    g.update(ray=ray,step=step,cell=cell,in_side=incoming,out_side=side,s0=s0,s1=s1,length=s1-s0)
    nr,nz=int(g['nr']),int(g['nz']);w=g['weight'][ray]
    g['volume']=np.bincount(cell,weights=w*g['length'],minlength=nr*nz)
    fi=np.zeros((nr*nz,4));fo=fi.copy();np.add.at(fi,(cell,incoming),w);np.add.at(fo,(cell,side),w)
    g.update(face_in_measure=fi,face_out_measure=fo,area=(g['original_widths'][:,None]*np.diff(g['z'])).ravel(),
             represented_widths=np.diff(g['x']))
    measure=np.zeros_like(fi);measure[:,:2]=np.tile(np.diff(g['z']),nr)[:,None]
    measure[:,2:]=abs(float(g['mu']))*np.repeat(g['original_widths'],nz)[:,None];g['face_measure']=measure
    return g


def pack_geometry(g):
    counts=np.bincount(g['ray'],minlength=len(g['u']));pointer=np.r_[0,np.cumsum(counts)]
    assert pointer[-1]<2**32 and g['cell'].max()<2**16
    p={k:v for k,v in g.items() if k not in DERIVED_GEOMETRY}
    p.update(piece_pointer=pointer.astype(np.uint32),piece_cell=g['cell'].astype(np.uint16),
             piece_end=g['s1'],piece_out_side=g['out_side'].astype(np.uint8))
    restored=unpack_geometry(p)
    assert set(restored)==set(g)
    for k,v in g.items():np.testing.assert_array_equal(restored[k],v,err_msg=k)
    return p


def unpack_responses(g,p):
    nr,nz=int(g['nr']),int(g['nz']);k=p['integral'].shape[1]
    fi=np.zeros((nr,nz,4,k));fo=fi.copy();x=p['radial_face'];z=p['axial_face']
    if g['orientation']==1:fi[:,:,0]=x[:-1];fo[:,:,1]=x[1:]
    else:fi[:,:,1]=x[1:];fo[:,:,0]=x[:-1]
    if g['mu']>0:fi[:,:,2]=z[:,:-1];fo[:,:,3]=z[:,1:]
    else:fi[:,:,3]=z[:,1:];fo[:,:,2]=z[:,:-1]
    return dict(integral=p['integral'],face_in=fi.reshape(nr*nz,4,k),face_out=fo.reshape(nr*nz,4,k),units=p['units'])


def pack_responses(g,f):
    nr,nz=int(g['nr']),int(g['nz']);k=f['integral'].shape[1];fi=f['face_in'].reshape(nr,nz,4,k);fo=f['face_out'].reshape(nr,nz,4,k)
    x=np.empty((nr+1,nz,k));z=np.empty((nr,nz+1,k))
    if g['orientation']==1:x[0]=fi[0,:,0];x[1:]=fo[:,:,1]
    else:x[-1]=fi[-1,:,1];x[:-1]=fo[:,:,0]
    if g['mu']>0:z[:,0]=fi[:,0,2];z[:,1:]=fo[:,:,3]
    else:z[:,-1]=fi[:,-1,3];z[:,:-1]=fo[:,:,2]
    keys=['integral','units','native_half_weight','maximum_piece_relative','minimum_input_angle','minimum_input_integral',
          'worst_input_piece','worst_input_witness','matched_endpoint_defect','matched_endpoint_scale','source_assembly_relative']
    p={k:f[k] for k in keys};p.update(radial_face=x,axial_face=z)
    restored=unpack_responses(g,p)
    for k in ['integral','face_in','face_out']:np.testing.assert_array_equal(restored[k],f[k],err_msg=k)
    return p

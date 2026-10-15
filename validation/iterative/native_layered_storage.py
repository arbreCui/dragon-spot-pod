"""Lossless structural-zero storage, with every named coordinate reconstructible."""
import numpy as np


def pack(response,metrics,regions,nz,entry,exit_surface,sign):
    regions=np.unique(regions);n=14*nz+8;k=n+2
    volume=(regions[:,None]*nz+np.arange(nz)).ravel()
    columns=np.r_[volume,8*nz+entry*nz+np.arange(nz),14*nz+regions,n,n+1]
    rows=np.r_[volume,8*nz+exit_surface*nz+np.arange(nz),14*nz+(8 if sign>0 else 0)+regions]
    inactive=np.setdiff1d(np.arange(k),columns)
    compact=response[np.ix_(rows,columns)].copy();witness=metrics[columns].copy()
    template=metrics[inactive[0]].copy() if len(inactive) else np.zeros(27)
    if len(inactive):
        assert np.broadcast_to(template,metrics[inactive].shape).copy().tobytes()==metrics[inactive].tobytes()
    result=dict(rows=rows,columns=columns,values=compact,metrics=witness,inactive_metrics=template,
                shape=np.array(response.shape,dtype=np.int64))
    a,m=unpack(result)
    assert a.tobytes()==response.tobytes() and m.tobytes()==metrics.tobytes()
    return result


def unpack(data):
    rows,columns=data['rows'],data['columns'];shape=tuple(data['shape'])
    a=np.zeros(shape,dtype=data['values'].dtype);a[np.ix_(rows,columns)]=data['values']
    m=np.tile(data['inactive_metrics'],(shape[1],1));m[columns]=data['metrics']
    return a,m

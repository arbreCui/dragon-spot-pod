"""Bounded ragged archives and in-memory replay of exact scientific bytes."""
import hashlib
import io
import json
from pathlib import Path
import numpy as np
from native_layered_storage import pack,unpack


class Collector:
    def __init__(self):self.items=[]

    def add(self,track,result,response,regions,nz,entry,exit_surface,sign):
        item=pack(response,result['metrics'],regions,nz,entry,exit_surface,sign)
        item['track']=track;item['geometry']=result['geometry'];self.items.append(item)

    def arrays(self):
        offsets=np.zeros((len(self.items)+1,3),np.int64)
        for i,x in enumerate(self.items):offsets[i+1]=offsets[i]+[len(x['rows']),len(x['columns']),x['values'].size]
        return dict(original_tracks=np.array([x['track'] for x in self.items],np.int64),offsets=offsets,
            shapes=np.stack([x['shape'] for x in self.items]),geometry=np.stack([x['geometry'] for x in self.items]),
            rows=np.concatenate([x['rows'] for x in self.items]),columns=np.concatenate([x['columns'] for x in self.items]),
            values=np.concatenate([x['values'].ravel() for x in self.items]),
            metrics=np.concatenate([x['metrics'] for x in self.items]),
            inactive_metrics=np.stack([x['inactive_metrics'] for x in self.items]))


def records(data):
    for i,track in enumerate(data['original_tracks']):
        a,b=data['offsets'][i:i+2];rows=data['rows'][a[0]:b[0]];cols=data['columns'][a[1]:b[1]]
        item=dict(rows=rows,columns=cols,shape=data['shapes'][i],
            values=data['values'][a[2]:b[2]].reshape(len(rows),len(cols)),
            metrics=data['metrics'][a[1]:b[1]],inactive_metrics=data['inactive_metrics'][i])
        response,metrics=unpack(item)
        yield int(track),data['geometry'][i],response,metrics


def serialize_npz(arrays):
    f=io.BytesIO();np.savez_compressed(f,**arrays);return f.getvalue()


def scientific(root,phase,case,name,value,receipt):
    payload=serialize_npz(value) if name.endswith('.npz') else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    sha=hashlib.sha256(payload).hexdigest();path=Path(root)/'primary'/case/name
    if phase=='primary':
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f:f.write(payload)
    else:
        assert path.stat().st_size==len(payload),(case,name,'length')
        with path.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
        assert actual==sha,(case,name,'replay mismatch')
    receipt[name]=dict(sha256=sha,bytes=len(payload))

"""Exact TRACK-copy admission for the declared conditional white receiver.

No transport, file mutation, source fitting, or physical accuracy claim.
"""
from pathlib import Path
import struct

from snapshot_control_preflight import _open_xsm


def verify_white_tracking_copy(original,marked):
    original,marked=Path(original),Path(marked)
    inherited=0
    with _open_xsm(original) as old,_open_xsm(marked) as new:
        active=set()
        def walk(previous,actual,root=False):
            nonlocal inherited
            additions={'AXMAT-WHITE','AXMAT-W-P'} if root else set()
            if set(actual)!=set(previous)|additions:
                raise ValueError('conditional receiver TRACK names changed')
            for name,p in previous.items():
                n=actual[name]
                if p[1:]!=n[1:]:raise ValueError('TRACK record kind/length changed: '+name)
                if p[2]==0:
                    pair=(p[0],n[0])
                    if pair in active:raise ValueError('cyclic TRACK object')
                    active.add(pair);walk(old.directory(p[0]),new.directory(n[0]));active.remove(pair)
                elif p[2]==10:
                    for a,b in zip(old.integers(p[0],p[1]),new.integers(n[0],n[1]),strict=True):
                        pair=(a,b)
                        if pair in active:raise ValueError('cyclic TRACK list')
                        active.add(pair);walk(old.directory(a),new.directory(b));active.remove(pair)
                else:
                    if old.read(p[0],p[1])!=new.read(n[0],n[1]):raise ValueError('TRACK inherited words changed: '+name)
                    inherited+=1
        walk(old.root,new.root,True)
        state=struct.unpack('<40i',old.record(old.root,'STATE-VECTOR',40,1))
        if (state[5],state[6],state[7],state[8],state[14],state[15])!=(8,12,3,1,8,3):
            raise ValueError('TRACK outside declared constant-diamond SN8 SCAT3 layout')
        if old.record(old.root,'NCODE',2,1)!=struct.pack('<2i',1,1) or old.record(old.root,'ZCODE',2,2)!=struct.pack('<2f',0,0):
            raise ValueError('original axial vacuum data differs')
        if new.record(new.root,'AXMAT-WHITE',4,1)!=struct.pack('<4i',1,1,8,3):
            raise ValueError('conditional white version/trace row differs')
        if new.record(new.root,'AXMAT-W-P',2,4)!=struct.pack('<d',6*.61776479):
            raise ValueError('conditional white physical perimeter differs')
    return dict(status='PASS_ONLY_TWO_WHITE_MARKERS_ADDED',inherited_records=inherited,new_records=2,
        physical_geometry_and_boundary_records_unchanged=True,model='conditional constant outer-sodium trace, uniform transverse azimuth',
        AAA_accuracy_qualified=False,ABA_admitted=False)

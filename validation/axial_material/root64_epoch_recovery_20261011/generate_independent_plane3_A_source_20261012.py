#!/usr/bin/env python3
"""Prepare a genuine third-plane producer; no transport or qualification.

Keep the A material, geometry, native seed, algorithms and numerical controls.
Only the independent entry/case, plane binding and fresh output names change.
The old frozen sources and all actual outputs remain untouched.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat

ROOT = Path('/Users/wen/spot')
REC = ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT = REC/'native_warm_A3_case_source_v1'

def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(p):
    before=identity(p)
    assert stat.S_ISREG(before[2])
    with p.open('rb') as f:
        s=os.fstat(f.fileno())
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
        b=f.read()
        s=os.fstat(f.fileno())
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
    assert identity(p)==before
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before)

def offsets(b, literal):
    return [m.start() for m in re.finditer(re.escape(literal),b)]

def replay(b, at, old, new):
    for i in reversed(at):
        assert b[i:i+len(old)]==old
        b=b[:i]+new+b[i+len(old):]
    return b

def transform(path, name, changes):
    old,old_pin=read(path); current=old; proof=[]
    for a,b,count in changes:
        a=a.encode(); b=b.encode(); before=offsets(current,a)
        assert len(before)==count,(name,a,len(before),count)
        current=replay(current,before,a,b)
        # Track only the replacement spans, not identical literals elsewhere.
        after=[pos+j*(len(b)-len(a)) for j,pos in enumerate(before)]
        proof.append(dict(old=a.decode(),new=b.decode(),count=count,
                          before_byte_offsets=before,after_byte_offsets=after))
    inverse=current
    for step in reversed(proof):
        inverse=replay(inverse,step['after_byte_offsets'],step['new'].encode(),step['old'].encode())
    assert inverse==old
    return name,current,dict(original_source=old_pin,literal_changes=proof,
                             full_byte_forward_and_inverse_equal=True)

def main():
    assert not OUT.exists()
    assert len('AXNCASEA364:')==12 and len('R64-A3-WARM1')==12
    sources=[
      transform(REC/'native_case_route_source_v2/AXNCASE64.f90','AXNCASEA364.f90',[
        ('ROOT64_NEW_WARM_A_20261011','ROOT64_NEW_WARM_A3_20261012',1),
        ('AXNCASE64','AXNCASEA364',13),
        ('R64WARM-A-V1 ','R64-A3-WARM1 ',1),
        ('plane=1,epoch=0','plane=3,epoch=0',1)]),
      transform(REC/'native_warm_B_case_source_v1/KDRDRV.F','KDRDRV.F',[
        ("      ELSE IF(HMODUL.EQ.'AXNCASEB64:') THEN\n",
         "      ELSE IF(HMODUL.EQ.'AXNCASEA364:') THEN\n         CALL AXNCASEA364(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n      ELSE IF(HMODUL.EQ.'AXNCASEB64:') THEN\n",1)]),
      transform(REC/'native_case_route_source_v1/ROOT64_NEW_WARM_A_20261011.x2m',
                'ROOT64_NEW_WARM_A3_20261012.x2m',[
        ('ROOT64_NEW_WARM_A_20261011','ROOT64_NEW_WARM_A3_20261012',1),
        ('R64WARM-A-V1','R64-A3-WARM1',1),
        ('Plane 1 / epoch 0','Plane 3 / epoch 0',1),
        ('new_native_A.xsm','new_native_A3.xsm',1),
        ('AXNCASE64:','AXNCASEA364:',2),
        ('ROOT64-NEW-WARM-A-NATIVE-COMPLETE','ROOT64-NEW-WARM-A3-NATIVE-COMPLETE',1)]),
      transform(REC/'native_warm_A_bounded_host_source_v3/verify_native_A_archive64.f90',
                'verify_native_A3_archive64.f90',[
        ('verify_native_A_archive64','verify_native_A3_archive64',2),
        ('plane1','plane3',2),
        ('WARM_A_','WARM_A3_',3),
        ('AXNCASE64_current','AXNCASEA364_current',1),
        ('R64WARM-A-V1 ','R64-A3-WARM1 ',2),
        ('"plane":1','"plane":3',2),
        ('material,contract,1,0,admitted','material,contract,3,0,admitted',1),
        ('plane/=1.or.epoch/=0','plane/=3.or.epoch/=0',1)])]
    binding_path=REC/'native_warm_A_bounded_host_source_v3/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'
    binding_bytes,binding_pin=read(binding_path)
    binding=json.loads(binding_bytes)
    inputs=[]
    for row in binding['physical_inputs']:
        _,actual=read(Path(row['pin']['path']))
        assert all(actual[k]==row['pin'][k] for k in ('path','sha256','size_bytes','identity'))
        inputs.append(dict(role=row['role'],pin=actual))
    OUT.mkdir()
    proofs=[]
    for name,b,proof in sources:
        p=OUT/name
        with p.open('xb') as f:f.write(b)
        _,proof['new_source']=read(p)
        proofs.append(proof)
    report=dict(schema='INDEPENDENT_A_MATERIAL_PLANE3_SOURCE_ONLY_V1',
      sources=proofs,actual_A_physical_input_binding_pin=binding_pin,physical_inputs=inputs,
      case_name='R64-A3-WARM1',plane=3,epoch=0,archive_listdim=1,archive_item=1,
      full_original_solver_and_thresholds_unchanged=True,
      source_only=True,compiled=False,transport_executed=False,
      producer_qualified=False,GLOBAL_qualified=False,online_BOOT_qualified=False,
      AAA_qualified=False,ABA_admitted=False,
      requires_genuine_fresh_plane3_solve=True,A1_copy_or_relabel_allowed=False)
    with (OUT/'COMPLETE_PLANE3_SOURCE_BYTE_INVERSE_AND_PHYSICAL_METADATA.json').open('x') as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(dict(path=str(OUT),source_files=len(sources),plane=3,source_only=True)))

if __name__=='__main__':main()

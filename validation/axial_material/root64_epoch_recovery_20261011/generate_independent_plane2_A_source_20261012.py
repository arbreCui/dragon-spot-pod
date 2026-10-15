#!/usr/bin/env python3
"""Prepare the A-material middle plane required for the homogeneous AAA control.

Do not substitute the B-material middle plane or relabel an existing A archive.
Only source is prepared; each plane still requires its own genuine native solve.
"""
import json
from pathlib import Path
from generate_independent_plane3_A_source_20261012 import read,transform

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
A3=REC/'native_warm_A3_case_source_v1'
OUT=REC/'native_warm_A2_case_source_v1'

def main():
    assert not OUT.exists()
    assert len('AXNCASEA264:')==12 and len('R64-A2-WARM1')==12
    sources=[
      transform(A3/'AXNCASEA364.f90','AXNCASEA264.f90',[
        ('ROOT64_NEW_WARM_A3_20261012','ROOT64_NEW_WARM_A2_20261012',1),
        ('AXNCASEA364','AXNCASEA264',13),
        ('R64-A3-WARM1 ','R64-A2-WARM1 ',1),
        ('plane=3,epoch=0','plane=2,epoch=0',1)]),
      transform(REC/'three_native_plane_contract_route_source_v1/KDRDRV.F','KDRDRV.F',[
        ("      ELSE IF(HMODUL.EQ.'AXNCASEA364:') THEN\n",
         "      ELSE IF(HMODUL.EQ.'AXNCASEA264:') THEN\n         CALL AXNCASEA264(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n      ELSE IF(HMODUL.EQ.'AXNCASEA364:') THEN\n",1)]),
      transform(A3/'ROOT64_NEW_WARM_A3_20261012.x2m','ROOT64_NEW_WARM_A2_20261012.x2m',[
        ('ROOT64_NEW_WARM_A3_20261012','ROOT64_NEW_WARM_A2_20261012',1),
        ('R64-A3-WARM1','R64-A2-WARM1',1),
        ('Plane 3 / epoch 0','Plane 2 / epoch 0',1),
        ('new_native_A3.xsm','new_native_A2.xsm',1),
        ('AXNCASEA364:','AXNCASEA264:',2),
        ('ROOT64-NEW-WARM-A3-NATIVE-COMPLETE','ROOT64-NEW-WARM-A2-NATIVE-COMPLETE',1)]),
      transform(A3/'verify_native_A3_archive64.f90','verify_native_A2_archive64.f90',[
        ('verify_native_A3_archive64','verify_native_A2_archive64',2),
        ('plane3','plane2',2),
        ('WARM_A3_','WARM_A2_',3),
        ('AXNCASEA364_current','AXNCASEA264_current',1),
        ('R64-A3-WARM1 ','R64-A2-WARM1 ',2),
        ('"plane":3','"plane":2',2),
        ('material,contract,3,0,admitted','material,contract,2,0,admitted',1),
        ('plane/=3.or.epoch/=0','plane/=2.or.epoch/=0',1)])]
    _,a3_pin=read(A3/'COMPLETE_PLANE3_SOURCE_BYTE_INVERSE_AND_PHYSICAL_METADATA.json')
    a3_meta=json.loads(Path(a3_pin['path']).read_text())
    for row in a3_meta['physical_inputs']:
        _,actual=read(Path(row['pin']['path']))
        assert all(actual[k]==row['pin'][k] for k in ('path','sha256','size_bytes','identity'))
    OUT.mkdir()
    proofs=[]
    for name,b,proof in sources:
        p=OUT/name
        with p.open('xb') as f:f.write(b)
        _,proof['new_source']=read(p)
        proofs.append(proof)
    report=dict(schema='INDEPENDENT_A_MATERIAL_PLANE2_SOURCE_ONLY_V1',sources=proofs,
      A3_source_metadata_pin=a3_pin,physical_inputs=a3_meta['physical_inputs'],
      actual_A_physical_input_binding_pin=a3_meta['actual_A_physical_input_binding_pin'],
      case_name='R64-A2-WARM1',plane=2,epoch=0,archive_listdim=1,archive_item=1,
      experiment_roles=dict(AAA=['A1','A2','A3'],ABA=['A1','B2','A3']),
      full_original_solver_and_thresholds_unchanged=True,source_only=True,
      compiled=False,transport_executed=False,producer_qualified=False,
      GLOBAL_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,
      requires_genuine_fresh_plane2_solve=True,A1_copy_or_B_substitution_allowed=False)
    with (OUT/'COMPLETE_PLANE2_SOURCE_BYTE_INVERSE_AND_PHYSICAL_METADATA.json').open('x') as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(dict(path=str(OUT),source_files=len(sources),plane=2,source_only=True)))

if __name__=='__main__':main()

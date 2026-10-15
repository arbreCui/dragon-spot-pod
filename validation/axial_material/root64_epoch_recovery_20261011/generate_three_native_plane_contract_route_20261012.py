#!/usr/bin/env python3
"""Separate initial native-three-plane entry from the existing online route.

Every native producer is read against its own external contract; GLOBAL remains
a separate case declaration. This source preparation grants no runtime result.
"""
import json
from pathlib import Path
from generate_independent_plane3_A_source_20261012 import read,transform

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'online_boot_native64_source_v1/operator_source_v2'
OUT=REC/'three_native_plane_contract_route_source_v1'

def main():
    assert not OUT.exists()
    alias_old="  if(.not.EMPTY_ROOT(kentry(1)))call XABORT('SPOOPP64: FRESH EMPTY ROOT REQUIRED.')\n"
    alias_new="""  ! GLOBAL and each plane contract are distinct readonly operands.
  ! This structural check does not replace the host's independent full-file pins.
  do i=6,9
    do j=2,i-1
      if(c_associated(kentry(i),kentry(j)))call XABORT('SPOOPP64: CONTRACT OPERAND ALIAS.')
    enddo
  enddo
  if(.not.EMPTY_ROOT(kentry(1)))call XABORT('SPOOPP64: FRESH EMPTY ROOT REQUIRED.')
"""
    load_old="""  call SPOR64_RCONTRACT_LOAD(kentry(6),contract,ok)
  if(.not.ok)call XABORT('SPOOPP64: COMPLETE RCONTRACT REQUIRED.')
"""
    load_new="""  call SPOR64_RCONTRACT_LOAD(kentry(6),contract,ok)
  if(.not.ok)call XABORT('SPOOPP64: COMPLETE GLOBAL RCONTRACT REQUIRED.')
  plane_rcontracts=kentry(7:9)
  do i=1,3
    call SPOR64_RCONTRACT_LOAD(plane_rcontracts(i),plane_contract,ok)
    if(.not.ok)call XABORT('SPOOPP64: COMPLETE PLANE RCONTRACT REQUIRED.')
  enddo
"""
    sources=[
      transform(OLD/'SPOOPG64.f90','SPOOPP64.f90',[
        ('SPOOPG64','SPOOPP64',19),
        ('integer::i,indic,nitma,rank,impx','integer::i,j,indic,nitma,rank,impx',1),
        ('type(SPOR64_ROUTE_CONTRACT)::contract',
         'type(SPOR64_ROUTE_CONTRACT)::contract,plane_contract\n  type(c_ptr)::plane_rcontracts(3)',1),
        ('nentry/=6','nentry/=9',1),
        ('SIX FULL OPERANDS REQUIRED.','NINE FULL OPERANDS REQUIRED.',1),
        ('jentry(2:6)','jentry(2:9)',1),
        ('do i=1,6','do i=1,9',1),
        (alias_old,alias_new,1),
        (load_old,load_new,1),
        ('call SPOASMG64(kentry(1),kentry(2),kentry(3),kentry(4),kentry(5),1,impx,rank,kentry(6))',
         'call SPOASMP64(kentry(1),kentry(2),kentry(3),kentry(4),kentry(5),1,impx,rank,kentry(6),plane_rcontracts)',1)]),
      transform(OLD/'SPOASMG64.f','SPOASMP64.f',[
        ('SPOASMG64','SPOASMP64',14),
        ('     1 IMPX,RANK_POD,IPCONTRACT)\n',
         '     1 IMPX,RANK_POD,IPCONTRACT,IPPLANE_CONTRACTS)\n',1),
        ('      TYPE(C_PTR) IPSYS,IPMACR,IPTRK,IPSNAP,IPBASIS,IPCONTRACT\n',
         '      TYPE(C_PTR) IPSYS,IPMACR,IPTRK,IPSNAP,IPBASIS,IPCONTRACT\n      TYPE(C_PTR) IPPLANE_CONTRACTS(3)\n',1),
        ('      LPOD64=NDPOD.EQ.NSNAP\n',
         '      LPOD64=NDPOD.EQ.NSNAP\n      IF(.NOT.LPOD64.OR.LDPOP) CALL XABORT(\n     1 "SPOASMP64: THREE INITIAL NATIVE PRODUCERS REQUIRED.")\n',1),
        ('     4     IPCONTRACT,ISNAP,0,ADMITTED_FLUX64,NATIVE_READ_STATUS)',
         '     4     IPPLANE_CONTRACTS(ISNAP),ISNAP,0,ADMITTED_FLUX64,\n     5     NATIVE_READ_STATUS)',1)]),
      transform(REC/'native_warm_A3_case_source_v1/KDRDRV.F','KDRDRV.F',[
        ("      ELSE IF(HMODUL.EQ.'SPOOPG64:') THEN\n",
         "      ELSE IF(HMODUL.EQ.'SPOOPP64:') THEN\n         CALL SPOOPP64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n      ELSE IF(HMODUL.EQ.'SPOOPG64:') THEN\n",1)])]
    # All mathematical code, original rank/370/3/32 checks and NativeRead CASE,
    # seal/tree/plane/epoch verification survive the full-source inverse proof.
    caller=sources[0][1];kernel=sources[1][1]
    assert b'jentry(2:9)' in caller and b'plane_rcontracts=kentry(7:9)' in caller
    assert b'IPPLANE_CONTRACTS(ISNAP),ISNAP,0,ADMITTED_FLUX64' in kernel
    assert b'IF(.NOT.LPOD64.OR.LDPOP)' in kernel
    OUT.mkdir()
    proofs=[]
    for name,b,proof in sources:
        p=OUT/name
        with p.open('xb') as f:f.write(b)
        _,proof['new_source']=read(p)
        proofs.append(proof)
    report=dict(schema='THREE_NATIVE_PLANE_CONTRACT_INITIAL_ROUTE_SOURCE_ONLY_V1',sources=proofs,
      CLE_entry='SPOOPP64:',native_assembler='SPOASMP64',
      operand_roles=['fresh_operator','axial_macro','axial_track','three_native_producer_archive',
                     'fixed_basis','GLOBAL_RCONTRACT','plane1_RCONTRACT','plane2_RCONTRACT','plane3_RCONTRACT'],
      original_source_and_ABI_preserved=['ASM','SPOASM','SPOOPG64','SPOASMG64'],
      initial_NATIVE_only=True,online_LDPOP_is_separate_unqualified_route=True,
      required_external_host_evidence='Actual admitted producer reports, complete external SHA/7ID and exact per-plane contract origins; no inference from internal seal or reference records',
      formula_rank_threshold_resource_change=False,source_only=True,compiled=False,
      transport_executed=False,three_plane_qualified=False,GLOBAL_qualified=False,
      online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False)
    with (OUT/'COMPLETE_THREE_PLANE_CONTRACT_ROUTE_BYTE_INVERSE.json').open('x') as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(dict(path=str(OUT),source_files=len(sources),source_only=True)))

if __name__=='__main__':main()

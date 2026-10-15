#!/usr/bin/env python3
"""Complete new native eigen/online radial operator Source. No business runs."""
from pathlib import Path
import json,ast,runpy
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'online_boot_native64_source_v1/operator_source_v2'
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
Transform=base['Transform'];read_pin=base['read_pin'];fresh=base['fresh'];fresh_json=base['fresh_json']

CALLER='''subroutine SPOOPG64(nentry,hentry,ientry,jentry,kentry)
  ! Actual standard CLE entry. Mandatory RANK comes from the externally pinned
  ! case/prepared deck; internal canonical labels never supply authorization.
  use GANLIB
  use SPOR64_VERIFY, only: EMPTY_ROOT,CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  integer::i,indic,nitma,rank,impx
  real::flott
  double precision::dflott
  character(len=4)::text4
  character(len=12)::signature
  logical::rank_seen,ok
  type(SPOR64_ROUTE_CONTRACT)::contract
  if(nentry/=6)call XABORT('SPOOPG64: SIX FULL OPERANDS REQUIRED.')
  if(any(ientry/=1.and.ientry/=2))call XABORT('SPOOPG64: LCM/XSM REQUIRED.')
  if(jentry(1)/=0.or.any(jentry(2:6)/=2))call XABORT('SPOOPG64: FRESH OUTPUT/READONLY INPUTS REQUIRED.')
  do i=1,6
    if(.not.c_associated(kentry(i)))call XABORT('SPOOPG64: NULL OPERAND.')
    if(i>1)then
      if(c_associated(kentry(1),kentry(i)))call XABORT('SPOOPG64: OUTPUT ALIAS.')
    endif
  enddo
  if(.not.EMPTY_ROOT(kentry(1)))call XABORT('SPOOPG64: FRESH EMPTY ROOT REQUIRED.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(2),'SIGNATURE',3,12,'L_MACROLIB'))call XABORT('SPOOPG64: AX MACRO.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(3),'SIGNATURE',3,12,'L_TRACK'))call XABORT('SPOOPG64: AX TRACK.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(4),'SIGNATURE',3,12,'L_ARCHIVE'))call XABORT('SPOOPG64: ARCHIVE.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(5),'SIGNATURE',3,12,'L_PIJ'))call XABORT('SPOOPG64: FIXED BASIS.')
  call SPOR64_RCONTRACT_LOAD(kentry(6),contract,ok)
  if(.not.ok)call XABORT('SPOOPG64: COMPLETE RCONTRACT REQUIRED.')
  rank=0;rank_seen=.false.;impx=1
  do
    call REDGET(indic,nitma,flott,text4,dflott)
    if(indic/=3)call XABORT('SPOOPG64: KEYWORD EXPECTED.')
    if(text4==';')exit
    if(text4=='RANK')then
      if(rank_seen)call XABORT('SPOOPG64: DUPLICATE RANK.')
      call REDGET(indic,rank,flott,text4,dflott)
      if(indic/=1.or.rank<=0)call XABORT('SPOOPG64: EXPLICIT POSITIVE RANK REQUIRED.')
      rank_seen=.true.
    else if(text4=='EDIT')then
      call REDGET(indic,impx,flott,text4,dflott)
      if(indic/=1)call XABORT('SPOOPG64: INTEGER EDIT REQUIRED.')
    else
      call XABORT('SPOOPG64: ONLY RANK/EDIT ARE VALID.')
    endif
  enddo
  if(.not.rank_seen)call XABORT('SPOOPG64: RANK MUST BE EXPLICIT, NO DEFAULT.')
  call SPOASMG64(kentry(1),kentry(2),kentry(3),kentry(4),kentry(5),1,impx,rank,kentry(6))
  signature='L_PIJ'
  call LCMPTC(kentry(1),'SIGNATURE',12,signature)
  call LCMPTC(kentry(1),'LINK.MACRO',12,hentry(2))
  call LCMPTC(kentry(1),'LINK.TRACK',12,hentry(3))
end subroutine SPOOPG64
'''

def main():
    OUT.mkdir(exist_ok=True)
    assert not(OUT/'SPOASMG64.f').exists()
    paths=[ROOT/'src/SPOASM.f',ROOT/'src/SPOT_LEAKAGE.f90',ROOT/'src/SPOPOD.f90',REC/'new_source/SPOR64_BOOT64.f90']
    before=[read_pin(p)[1] for p in paths]
    raw,pin=read_pin(paths[0]);t=Transform(raw)
    t.splice('independent complete DECK','*DECK SPOASM\n','*DECK SPOASMG64\n')
    t.splice('actual new entry with complete contract operand','      SUBROUTINE SPOASM(','      SUBROUTINE SPOASMG64(')
    t.splice('independent required native producer contract ABI','     1 IMPX,RANK_POD)\n','     1 IMPX,RANK_POD,IPCONTRACT)\n')
    t.splice('explicit full native eigen Source helpers and reader','      USE GANLIB\n','      USE GANLIB\n      USE SPOT_RADIAL_NATIVE_MATH64, ONLY:\n     1 SPOF00_NATIVE64,SPOQ00_NATIVE64\n      USE SPOR64_BOOT64, ONLY: SPOR64_BOOT64_READ_NATIVE,ROOT64_LOADED\n')
    t.splice('native contract handle and admitted full unknown staging','      TYPE(C_PTR) IPSYS,IPMACR,IPTRK,IPSNAP,IPBASIS\n','      TYPE(C_PTR) IPSYS,IPMACR,IPTRK,IPSNAP,IPBASIS,IPCONTRACT\n      DOUBLE PRECISION, ALLOCATABLE :: ADMITTED_FLUX64(:,:)\n      DOUBLE PRECISION KEFF_S64\n      INTEGER NATIVE_READ_STATUS,NATIVE_EIGEN_STATE(NSTATE)\n      LOGICAL LRAD64\n')
    # NSTATE is declared below the handle statement in the original; the new
    # fixed-size state declaration uses the literal original size, not forward
    # use of an undeclared implicit parameter.
    t.splice('original fixed state extent without forward specification reference',
             '      INTEGER NATIVE_READ_STATUS,NATIVE_EIGEN_STATE(NSTATE)\n',
             '      INTEGER NATIVE_READ_STATUS,NATIVE_EIGEN_STATE(40)\n')
    t.splice('require genuine native path and allocate eigen dynamic64 buffers',
             '      LPOD64=NDPOD.EQ.NSNAP\n',
             '      LPOD64=NDPOD.EQ.NSNAP\n      LRAD64=LDPOP.OR.LPOD64\n'
             '      IF(.NOT.LRAD64) CALL XABORT(\n     1 "SPOASMG64: COMPLETE NATIVE RADIAL DATA REQUIRED.")\n'
             '      IF(NGRP.NE.370.OR.NSNAP.NE.3) CALL XABORT(\n     1 "SPOASMG64: COMPLETE 370 GROUP/3 PLANE SCOPE REQUIRED.")\n'
             '      IF(RANK_POD.LE.0.OR.IFIXB.NE.1) CALL XABORT(\n     1 "SPOASMG64: EXPLICIT FIXED CASE RANK REQUIRED.")\n'
             '      IF(LPOD64) THEN\n'
             '        ALLOCATE(FLUX2D64(MAXK2D,NSNAP,NGRP),\n'
             '     1   SOUR2D64(MAXK2D,NSNAP,NGRP),\n'
             '     2   QFISS2D64(MAXK2D,NSNAP,NGRP))\n'
             '        FLUX2D64=0.0D0\n        SOUR2D64=0.0D0\n'
             '        QFISS2D64=0.0D0\n      ENDIF\n')
    t.splice('actual native producer reader before offline field consumption',
             '        IF(LPOD64) THEN\n          JPPOD64=LCMGID(KPSNAP,\'FLUX64\')\n',
             '        IF(LPOD64) THEN\n'
             '          CALL SPOR64_BOOT64_READ_NATIVE(KPSNAP,\n'
             '     1     LCMGIL(JPSNAP1,ISNAP),\n'
             '     2     LCMGIL(LCMGID(IPSNAP,"SYSTEM"),ISNAP),\n'
             '     3     LCMGIL(LCMGID(IPSNAP,"MICROLIB2"),ISNAP),\n'
             '     4     IPCONTRACT,ISNAP,0,ADMITTED_FLUX64,NATIVE_READ_STATUS)\n'
             '          IF(NATIVE_READ_STATUS.NE.ROOT64_LOADED) CALL XABORT(\n'
             '     1     "SPOASMG64: GENUINE COMPLETE NATIVE INPUT REQUIRED.")\n'
             '          IF(ANY(SHAPE(ADMITTED_FLUX64).NE.\n'
             '     1     [MAXK2D,NGRP])) CALL XABORT(\n'
             '     2     "SPOASMG64: COMPLETE NATIVE UNKNOWN EXTENT REQUIRED.")\n'
             '          CALL LCMGET(KPSNAP,"STATE-VECTOR",NATIVE_EIGEN_STATE)\n'
             '          IF(NATIVE_EIGEN_STATE(6).NE.2.OR.\n'
             '     1     NATIVE_EIGEN_STATE(7).NE.0) CALL XABORT(\n'
             '     2     "SPOASMG64: ORIGINAL NATIVE TYPE K REQUIRED.")\n'
             '          JPPOD64=LCMGID(KPSNAP,\'FLUX64\')\n')
    t.splice('typed offline producer must not masquerade as fixed-source feedback',
             '        DO IGR=1,NGRP\n          IF(LPOD64) THEN\n',
             '        IF(LPOD64.AND.FS_MODE(ISNAP).NE.0) CALL XABORT(\n'
             '     1   "SPOASMG64: NATIVE EIGEN SOURCE CANNOT BE FAKED QFISS.")\n'
             '        DO IGR=1,NGRP\n          IF(LPOD64) THEN\n')
    t.splice('save all actual native flux/source bits for eigen radial balance',
             '            DO IMIR=1,MAXK2D\n              IF((.NOT.IEEE_IS_FINITE(FLUXPOD64(IMIR,ISNAP,IGR)))\n',
             '            FLUX2D64(:,ISNAP,IGR)=ADMITTED_FLUX64(:,IGR)\n'
             '            SOUR2D64(:,ISNAP,IGR)=SOURCEPOD64(:)\n'
             '            IF(ANY(TRANSFER(FLUXPOD64(:,ISNAP,IGR),\n'
             '     1       [0_INT64],MAXK2D).NE.\n'
             '     2       TRANSFER(ADMITTED_FLUX64(:,IGR),\n'
             '     3       [0_INT64],MAXK2D))) CALL XABORT(\n'
             '     4       "SPOASMG64: NATIVE PRODUCER FLUX BIT MISMATCH.")\n'
             '            DO IMIR=1,MAXK2D\n              IF((.NOT.IEEE_IS_FINITE(FLUXPOD64(IMIR,ISNAP,IGR)))\n')
    t.splice('release native reader staging only after all group records consumed',
             '      NFS_SNAP=SUM(FS_MODE)\n',
             '      IF(ALLOCATED(ADMITTED_FLUX64)) DEALLOCATE(ADMITTED_FLUX64)\n      NFS_SNAP=SUM(FS_MODE)\n')
    # Only the downstream dynamic buffers/operator/publication are LRAD64.
    # The original online ingestion and QFISS branch remain LDPOP-only.
    t.splice('all native radial flux/operator staging',
             '      IF(LDPOP) THEN\n        ALLOCATE(PHIRK64(NREG2D,NSNAP,NGRP),DB264(NREG2D,NSNAP,NGRP))\n',
             '      IF(LRAD64) THEN\n        ALLOCATE(PHIRK64(NREG2D,NSNAP,NGRP),DB264(NREG2D,NSNAP,NGRP))\n')
    t.splice('native leakage allocated for eigen and online',
             '      IF(LDPOP) ALLOCATE(LEAK1D64(NGRP))\n','      IF(LRAD64) ALLOCATE(LEAK1D64(NGRP))\n')
    t.splice('reject same-length wrong TYPE before REAL32 leakage buffer read',
             '        ELSE IF(ILONG.EQ.NGRP) THEN\n',
             '        ELSE IF((ILONG.EQ.NGRP).AND.(ITYLCM.EQ.2)) THEN\n')
    t.splice('cold native eigen absent leakage is original exact mathematical zero',
             '        IF(LDPOP) THEN\n          CALL LCMLEN(KPSNAP,\'LEAK1D64\',ILONGD,ITYLCD)\n',
             '        IF(LRAD64) THEN\n'
             '          CALL LCMLEN(KPSNAP,\'LEAK1D64\',ILONGD,ITYLCD)\n'
             '          IF(LPOD64.AND.ILONG.EQ.0.AND.ILONGD.EQ.0) THEN\n'
             '*           Original no-leak native TYPE K boundary: exact zero.\n'
             '            LEAK1D64=0.0D0\n          ELSE\n')
    t.splice('close native leakage guard and mirror branch',
             '          ENDDO\n        ENDIF\n        KPSNAP=LCMGIL(JPSNAP1,ISNAP)\n',
             '          ENDDO\n          ENDIF\n        ENDIF\n        KPSNAP=LCMGIL(JPSNAP1,ISNAP)\n')
    t.splice('native regional multigroup work buffers',
             '        IF(LDPOP) THEN\n          ALLOCATE(REGFLUX64',
             '        IF(LRAD64) THEN\n          ALLOCATE(REGFLUX64')
    t.splice('map actual native scalar flux before all full-group source arithmetic',
             '            IF(LDPOP) THEN\n              REGFLUX64',
             '            IF(LRAD64) THEN\n              REGFLUX64')
    t.splice('actual native eigen keff rather than its legacy mirror',
             '        IPLIB=LCMGIL(JPSNAP4,ISNAP)\n',
             '        IF(LPOD64) THEN\n'
             '          CALL LCMLEN(KPSNAP,"SPOT-KEFF64",ILONGD,ITYLCD)\n'
             '          IF(ILONGD.NE.1.OR.ITYLCD.NE.4) CALL XABORT(\n'
             '     1     "SPOASMG64: ACTUAL NATIVE KEFF64 REQUIRED.")\n'
             '          CALL LCMGET(KPSNAP,"SPOT-KEFF64",KEFF_S64)\n'
             '          IF(.NOT.IEEE_IS_FINITE(KEFF_S64).OR.\n'
             '     1     KEFF_S64.LE.0.0D0) CALL XABORT(\n'
             '     2     "SPOASMG64: INVALID NATIVE KEFF64.")\n'
             '          IF(TRANSFER(REAL(KEFF_S64),0).NE.\n'
             '     1     TRANSFER(KEFF_S,0)) CALL XABORT(\n'
             '     2     "SPOASMG64: NATIVE KEFF MIRROR MISMATCH.")\n'
             '        ENDIF\n        IPLIB=LCMGIL(JPSNAP4,ISNAP)\n')
    t.splice('preserve complete 32 physical fission slots',
             '        JPMACR2=LCMGID(IPMACR2,\'GROUP\')\n',
             '        IF(NIFIS.NE.32) CALL XABORT(\n'
             '     1   "SPOASMG64: ALL 32 FISSION SLOTS REQUIRED.")\n'
             '        JPMACR2=LCMGID(IPMACR2,\'GROUP\')\n')
    t.splice('complete native eigen fission producer with original loop order',
             '          CALL SPOF00(NREG2D,NGRP,NMIX2D,NIFIS,MAT2D,REGFLUX,\n',
             '          CALL SPOF00_NATIVE64(NREG2D,NGRP,NMIX2D,NIFIS,\n'
             '     1      MAT2D,REGFLUX64,\n')
    t.splice('complete native eigen physical RHS, original multiply divide order',
             '          ELSE IF(FS_MODE(ISNAP).EQ.0) THEN\n',
             '          ELSE IF(LPOD64) THEN\n'
             '            CALL SPOQ00_NATIVE64(NREG2D,NGRP,NMIX2D,NIFIS,\n'
             '     1       IGR,MAT2D,REGFLUX64,KEFF_S64,NJJS,IJJS,IPOS,\n'
             '     2       SCAT,CHI,NUSIGF,QREG64,FISPROD)\n'
             '          ELSE IF(FS_MODE(ISNAP).EQ.0) THEN\n')
    t.splice('actual native leakage/operator computation on both valid paths',
             '            IF(LDPOP) THEN\n              DB264',
             '            IF(LRAD64) THEN\n              DB264')
    t.splice('native regional scratch cleanup','        IF(LDPOP) DEALLOCATE(QFREG64,QREG64,REGFLUX64)\n','        IF(LRAD64) DEALLOCATE(QFREG64,QREG64,REGFLUX64)\n')
    t.splice('native complete operator finite checks',
             '      IF(LDPOP) THEN\n        IF(ANY(.NOT.IEEE_IS_FINITE(PHIRK64)))',
             '      IF(LRAD64) THEN\n        IF(ANY(.NOT.IEEE_IS_FINITE(PHIRK64)))')
    t.splice('native actual operator publication for both valid paths',
             '        IF(LDPOP) THEN\n*         THE REAL64 OPERATOR',
             '        IF(LRAD64) THEN\n*         THE REAL64 OPERATOR')
    t.splice('native complete dynamic scratch cleanup',
             '      IF(LDPOP) DEALLOCATE(RADSTG,DB264,PHIRK64,QFISS2D64,SOUR2D64,\n',
             '      IF(LRAD64) DEALLOCATE(RADSTG,DB264,PHIRK64,QFISS2D64,SOUR2D64,\n')
    mr,mp=read_pin(paths[1]);m=Transform(mr)
    m.rename('SPOT_LEAKAGE','SPOT_RADIAL_NATIVE_MATH64',2)
    m.rename('SPOF00','SPOF00_NATIVE64',9)
    m.rename('SPOQ00','SPOQ00_NATIVE64',13)
    m.splice('native eigen fission phi ABI','    real, intent(in) :: phi(nreg,ngrp)\n','    double precision, intent(in) :: phi(nreg,ngrp)\n')
    m.splice('native eigen multigroup phi and k ABI',
             '    real, intent(in) :: phi(nreg,ngrp),keff,scat(:)\n',
             '    double precision, intent(in) :: phi(nreg,ngrp),keff\n'
             '    real, intent(in) :: scat(:)\n')
    m.splice('native eigen physical RHS return',
             '    real, intent(out) :: qtotal(nreg)\n',
             '    double precision, intent(out) :: qtotal(nreg)\n',2)
    # Only native eigen SPOQ00 output is changed; the unrelated copied legacy
    # SPOQFS in this private module stays untouched and is never called.
    # The two exact declarations above occurred in SPOQ00 and SPOQFS: restore
    # that latter unrelated declaration by its complete neighboring signature.
    m.splice('retain unrelated complete legacy SPOQFS body',
             '    real, intent(in) :: phi(nreg,ngrp),scat(:),qfrozen(nreg)\n'
             '    double precision, intent(out) :: qtotal(nreg)\n',
             '    real, intent(in) :: phi(nreg,ngrp),scat(:),qfrozen(nreg)\n'
             '    real, intent(out) :: qtotal(nreg)\n')
    m.splice('keep native physical RHS without a demote promote',
             '      qtotal(i)=real(source)\n',
             '      qtotal(i)=source\n',2)
    m.splice('retain unrelated legacy SPOQFS output',
             '      qtotal(i)=source\n    enddo\n    if (any(.not.ieee_is_finite(qtotal))) &\n'
             "      call XABORT('SPOQFS: NON-FINITE FIXED-SOURCE RHS.')\n",
             '      qtotal(i)=real(source)\n    enddo\n    if (any(.not.ieee_is_finite(qtotal))) &\n'
             "      call XABORT('SPOQFS: NON-FINITE FIXED-SOURCE RHS.')\n")
    proofs={'SPOASMG64':t.verify(),'native_math':m.verify()}
    fresh(OUT/'SPOASMG64.f',t.raw);fresh(OUT/'SPOT_RADIAL_NATIVE_MATH64.f90',m.raw)
    fresh(OUT/'SPOOPG64.f90',CALLER.encode())
    fresh(OUT/'ORIGINAL_COMPLETE_SPOASM.f',raw);fresh(OUT/'ORIGINAL_COMPLETE_SPOT_LEAKAGE.f90',mr)
    fresh_json(OUT/'COMPLETE_NATIVE_RADIAL_OPERATOR_WHOLE_BYTE_PROOFS.json',proofs)
    after=[read_pin(p)[1] for p in paths];assert before==after
    ast.parse(read_pin(Path(__file__))[0])
    pins=[read_pin(OUT/n)[1] for n in ['SPOASMG64.f','SPOT_RADIAL_NATIVE_MATH64.f90','SPOOPG64.f90']]
    fresh_json(OUT/'CURRENT_COMPLETE_NATIVE_RADIAL_OPERATOR_SOURCE_BINDING.json',{
      'scope':'Complete new Source-only real RADIAL-OP64 producer for native eigen/online inputs; no compile/solve/qualification',
      'source_pins':pins,'basis_and_protected_dependencies_before':before,'after':after,
      'actual_SPOASMG64_argument_count':9,'actual_SPOF00_NATIVE64_argument_count':8,'actual_SPOQ00_NATIVE64_argument_count':16,
      'required_case_rank':'Independent mandatory RANK in CLE from truly frozen case/prepared, no default or internal inferred rank.',
      'native_eigen_ingress':'Full actual SPOR64_BOOT64_READ_NATIVE per same-index track/system/material/contract/plane/e0; full ROOT-FLUX64 matched to FLUX64, full SOUR64 and mirrors, native SPOT-KEFF64.',
      'dynamic':'LRAD64=LDPOP.OR.LPOD64; offline native eigen and online native fixed source paths remain distinct; no false QFISS/FS_MODE labels. Original SPOF00/SPOQ00 loops/guards/optional fission hoist and multiply-then-divide order preserved with dynamic phi/k/q REAL64.',
      'leakage':'Original absence for native TYPE K is exact mathematical zero; any present type2 leakage requires real LEAK1D64; never promote dynamic type2 leakage.',
      'original_diagnostics_scope':'SPOT-REM-MIN remains original type2 diagnostic, is not native authority and never feeds RADIAL-OP64.',
      'remaining':['Independent full Source review','New dispatcher/owning actual ASM route and current physical native producer/input/tool pins','Guarded actual compile and true per-group operator production','Full global solve/BOOT/17/wholeinput qualification'],
      'Fortran_or_transport_executed':False,'qualified':False})
    print(json.dumps({'status':'COMPLETE_NATIVE_RADIAL_OPERATOR_SOURCE_WRITTEN','source_pins':pins,'inverse_step_counts':{k:v['actual_transform_steps'] for k,v in proofs.items()},'protected_unchanged':True,'Fortran_or_numeric_executed':False}))

if __name__=='__main__':main()

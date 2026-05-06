*DECK SPOF
      SUBROUTINE SPOF(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,
     1 KEYFLX,FUNKNO,SUNKNO,TITR)
*
*-----------------------------------------------------------------------
*
*Purpose:
* Solve N-group transport equation for fluxes using the 2d/1d synthesis
* Proper orthogonal tracking (SPOT) method.
*
*Copyright:
* Copyright (C) 2024 Ecole Polytechnique de Montreal
* This library is free software; you can redistribute it and/or
* modify it under the terms of the GNU Lesser General Public
* License as published by the Free Software Foundation; either
* version 2.1 of the License, or (at your option) any later version
*
*Author(s): A. Hebert
*
*Parameters: input
* KPSYS   pointer to the assembly LCM object (L_PIJ signature). KPSYS is
*         an array of directories.
* IPTRK   pointer to the tracking (L_TRACK signature).
* IMPX    print flag (equal to zero for no print).
* NGEFF   number of energy groups processed in parallel.
* NGIND   energy group indices assign to the NGEFF set.
* NREG    total number of regions for which specific values of the
*         neutron flux and reactions rates are required.
* NMAT    number of mixtures in the internal library.
* NUN     total number of unknowns in vectors SUNKNO and FUNKNO.
* MAT     index-number of the mixture type assigned to each volume.
* KEYFLX  position of averaged flux elements in FUNKNO vector.
* SUNKNO  input source vector.
* TITR    title.
*
*Parameters: input/output
* FUNKNO  unknown vector.
*
*-----------------------------------------------------------------------
*
      USE GANLIB
*----
*  SUBROUTINE ARGUMENTS
*----
      CHARACTER   TITR*72
      TYPE(C_PTR) KPSYS(NGEFF),IPTRK
      INTEGER     NGEFF,NGIND(NGEFF),IMPX,NREG,NMAT,NUN,MAT(NREG),
     >            KEYFLX(NREG)
      REAL        FUNKNO(NUN,NGEFF),SUNKNO(NUN,NGEFF)
*----
*  LOCAL VARIABLES
*----
      PARAMETER  (IUNOUT=6,NSTATE=40,ITPIJ=1)
      INTEGER     IPAR(NSTATE),NCODE(2)
      REAL        ZCODE(2)
      LOGICAL     LFIXUP
*----
*  ALLOCATABLE ARRAYS
*----
      INTEGER, ALLOCATABLE, DIMENSION(:) :: MAT1D
      REAL, ALLOCATABLE, DIMENSION(:) :: VOL1D,GAR
      REAL, ALLOCATABLE, DIMENSION(:,:) :: SGAR
      REAL, ALLOCATABLE, DIMENSION(:,:,:) :: SGAS
      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:) :: DB2
      TYPE(C_PTR) DU_PTR,W_PTR,PL_PTR
      REAL, POINTER, DIMENSION(:) :: DU,W,PL
*----
*  PRINT INPUT SOURCES
*----
      IF(IMPX.GT.2) THEN
        WRITE(IUNOUT,'(//7H SPOF: ,A72)') TITR
        CALL KDRCPU(TK1)
      ENDIF
      IF(IMPX.GT.3) THEN
        ALLOCATE(GAR(NREG))
        DO II=1,NGEFF
          GAR(:NREG)=0.0
          DO I=1,NREG
            IF(KEYFLX(I).NE.0) GAR(I)=SUNKNO(KEYFLX(I),II)
          ENDDO
          WRITE(IUNOUT,'(/33H N E U T R O N    S O U R C E S (,I5,
     1    3H ):)') NGIND(II)
          WRITE(IUNOUT,'(1P,6(5X,E15.7))') (GAR(I),I=1,NREG)
        ENDDO
        DEALLOCATE(GAR)
      ENDIF
*----
*  RECOVER SPOT TRACKING PARAMETERS.
*----
      CALL LCMGET(IPTRK,'STATE-VECTOR',IPAR)
      NREG=IPAR(1)
      NUN=IPAR(2)
      NREG2D=IPAR(6)
      NFLOOR=IPAR(7)
      NSNAP=IPAR(8)
      IELEM=IPAR(9)
      NLF=IPAR(15)
      ISCHM=IPAR(10)
      LL4=IPAR(11)
      LL5=IPAR(12)
      ISCAT=IPAR(16)
      LFIXUP=(IPAR(18).EQ.1)
      IF(IPAR(4).GT.NMAT) CALL XABORT('SPOF: INVALID NMAT.')
      ALLOCATE(MAT1D(NFLOOR),VOL1D(NFLOOR))
      CALL LCMGET(IPTRK,'MAT1D',MAT1D)
      CALL LCMGET(IPTRK,'VOL1D',VOL1D)
*----
*  SCRATCH STORAGE ALLOCATION.
*----
      ALLOCATE(SGAR(0:NMAT,NGEFF),SGAS(0:NMAT,ISCAT,NGEFF))
*----
*  RECOVER TOTAL AND WITHIN-GROUP SCATTERING MULTIGROUP CROSS SECTIONS.
*----
      SGAS(0:NMAT,:ISCAT,:NGEFF)=0.0
      NANI=1
      DO 10 II=1,NGEFF
      CALL LCMLEN(KPSYS(II),'DRAGON-TXSC',ILONG,ITYLCM)
      IF(ILONG.NE.NMAT+1) CALL XABORT('SPOF: INVALID TXSC LENGTH.')
      CALL LCMLEN(KPSYS(II),'DRAGON-S0XSC',ILONG,ITYLCM)
      NANI=MAX(NANI,ILONG/(NMAT+1))
      IF(NANI.GT.ISCAT) CALL XABORT('SPOF: INVALID S0XSC LENGTH.')
      CALL LCMGET(KPSYS(II),'DRAGON-TXSC',SGAR(0,II))
      CALL LCMGET(KPSYS(II),'DRAGON-S0XSC',SGAS(0,1,II))
*----
*  PRINT ZEROTH MOMENT OF SOURCES.
*----
      IF(IMPX.GT.3) THEN
        WRITE(IUNOUT,6001) NGIND(II)
        WRITE(IUNOUT,'(1P,6(5X,E15.7))') (SUNKNO(KEYFLX(I),II),I=1,NREG)
      ENDIF
   10 CONTINUE
*----
*  MAIN LOOP OVER ENERGY GROUPS.
*----
      ALLOCATE(GAR(NUN))
      GAR(:NUN)=0.0
      DO 130 II=1,NGEFF
      IGR=NGIND(II)
      IF(IMPX.GT.-3) WRITE(IUNOUT,'(/23H SPOF: PROCESSING GROUP,I5,
     1 6H WITH ,A,1H.)') IGR,'SPOT'
      CALL LCMGET(KPSYS(II),'NREG2D',NREG2D)
      CALL LCMGET(KPSYS(II),'NSNAP',NSNAP)
      ALLOCATE(DB2(NSNAP,NREG2D))
      CALL LCMGET(KPSYS(II),'LEAK2D',DB2)
*----
*  COMPUTE WEIGHTED CROSS SECTIONS AND SOURCE AND SOLVE FOR THE FLUXES.
*----
      NSCT=ISCAT
      CALL LCMGPD(IPTRK,'U',DU_PTR)
      CALL LCMGPD(IPTRK,'W',W_PTR)
      CALL LCMGPD(IPTRK,'PL',PL_PTR)
      CALL C_F_POINTER(DU_PTR,DU,(/ NLF /))
      CALL C_F_POINTER(W_PTR,W,(/ NLF /))
      CALL C_F_POINTER(PL_PTR,PL,(/ NSCT*NLF /))
      CALL LCMGET(IPTRK,'NCODE',NCODE)
      CALL LCMGET(IPTRK,'ZCODE',ZCODE)
      CALL SPOT1P(NREG2D,NFLOOR,IELEM,NMAT,NSNAP,ISCHM,NLF,NSCT,
     1 LFIXUP,MAT1D,VOL1D,MAT,KEYFLX,SGAR(0,II),SGAS(0,1,II),DB2,
     2 NCODE,ZCODE,SUNKNO(1,II),DU,W,PL,FUNKNO(1,II),FUNKNO(LL4+1,II),
     3 FUNKNO(LL4+LL5+1,II))
*----
* END OF LOOP OVER ENERGY GROUPS
*----
      DEALLOCATE(DB2)
  130 CONTINUE ! II
*----
*  PRINT CPU TIME
*----
      IF(IMPX.GT.2) THEN
        CALL KDRCPU(TK2)
        WRITE(IUNOUT,'(16H SPOF: CPU TIME=,1P,E11.3,8H SECOND./)')
     1  TK2-TK1
      ENDIF
*----
*  SCRATCH STORAGE DEALLOCATION
*----
      DEALLOCATE(VOL1D,MAT1D,GAR)
      DEALLOCATE(SGAS,SGAR)
      RETURN
 6001 FORMAT(//39H SPOF: N E U T R O N    S O U R C E S (,I5,3H ):)
      END

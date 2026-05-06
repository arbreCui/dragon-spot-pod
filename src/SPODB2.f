*DECK SPODB2
      SUBROUTINE SPODB2(IPFLUX,IPTRK,IPSNAP,NUNKNO,NGRP,NREG,MATCOD,
     1 KEYFLX,VOL,IPICK,IMPX)
*
*-----------------------------------------------------------------------
*
*Purpose:
* Compute the axial flux and axial leakage cross sections for the 2d/1d
* synthesis Proper orthogonal tracking (SPOT) method.
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
* IPFLUX  pointer to the flux LCM object.
* IPTRK   pointer to the tracking (L_TRACK signature).
* IPSNAP  pointer to the snapshot information (L_ARCHIVE signature).
* NUNKNO  total number of unknowns in vector FUNKNO.
* NGRP    number of energy groups.
* NREG    number of regions.
* MATCOD  mixture indices.
* KEYFLX  index of the flux components in unknown vector.
* VOL     volumes.
* IPICK   SPOT LEAK1D accuracy recovery (0/1: no/yes).
* IMPX    print flag (equal to zero for no print).
*
*-----------------------------------------------------------------------
*
      USE GANLIB
*----
*  SUBROUTINE ARGUMENTS
*----
      TYPE(C_PTR) IPFLUX,IPTRK,IPSNAP
      INTEGER     NUNKNO,NGRP,NREG,MATCOD(NREG),KEYFLX(NREG),IMPX
      REAL        VOL(NREG)
*----
*  LOCAL VARIABLES
*----
      PARAMETER  (IOUT=6,NSTATE=40)
      INTEGER     IPAR(NSTATE),IPICK
      CHARACTER   TEXT4*4
      DOUBLE PRECISION DFLOTT
      TYPE(C_PTR) JPFLUX,JPSNAP,KPSNAP
*----
*  ALLOCATABLE ARRAYS
*----
      INTEGER, ALLOCATABLE, DIMENSION(:) :: MAT1D
      REAL, ALLOCATABLE, DIMENSION(:) :: VOL1D
      REAL, ALLOCATABLE, DIMENSION(:,:) :: FUNKNO,DB2,FLU2,OLD
*----
*  RECOVER SPOT SPECIFIC PARAMETERS
*----
      CALL LCMGET(IPTRK,'STATE-VECTOR',IPAR)
      NBMIX=IPAR(4)
      NREG2D=IPAR(6)
      NFLOOR=IPAR(7)
      NSNAP=IPAR(8)
      LL4=IPAR(11)
      ISCAT=IPAR(16)
      ALLOCATE(MAT1D(NFLOOR),VOL1D(NFLOOR))
      CALL LCMGET(IPTRK,'MAT1D',MAT1D)
      CALL LCMGET(IPTRK,'VOL1D',VOL1D)
*----
*  RECOVER AXIAL LEAKAGE CROSS SECTIONS
*  DB2 values are recovered as net current difference evaluated on each
*  interface of each axial mesh.
*----
      ALLOCATE(DB2(NGRP,NSNAP),FLU2(NGRP,NSNAP),FUNKNO(NUNKNO,NGRP))
      JPFLUX=LCMGID(IPFLUX,'FLUX')
      DO IG=1,NGRP
        CALL LCMGDL(JPFLUX,IG,FUNKNO(1,IG))
      ENDDO
      DB2(:NGRP,:NSNAP)=0.0
      FLU2(:NGRP,:NSNAP)=0.0
      DO IFLOOR=1,NFLOOR
        ISNAP=MAT1D(IFLOOR)
        DO I=1,NREG2D
          IOF0=(I-1)*NFLOOR+IFLOOR
          IOF1=(I-1)*(NFLOOR+1)+IFLOOR
          IOF2=(I-1)*(NFLOOR+1)+IFLOOR+1
          IBM=MATCOD(IOF0)
          IF(IBM.EQ.0) CYCLE
          IF(IBM.GT.NBMIX) CALL XABORT('SPODB2: IBM OVERFLOW.')
          IUNK=KEYFLX(IOF0)
          IF(IUNK.EQ.0) CYCLE
          DO IG=1,NGRP
            FLU2(IG,ISNAP)=FLU2(IG,ISNAP)+VOL(IOF0)*FUNKNO(IUNK,IG)
            DB2(IG,ISNAP)=DB2(IG,ISNAP)+VOL(IOF0)*(FUNKNO(LL4+IOF2,IG)-
     1      FUNKNO(LL4+IOF1,IG))/VOL1D(IFLOOR)
          ENDDO
        ENDDO
      ENDDO
      DEALLOCATE(FUNKNO)
*     Guard against zero or negative integrated flux. FLU2 can vanish
*     for snapshots whose floors are all KEYFLX=0 or have phi below the
*     SPOASM zero-flux floor. Without the guard the division produces
*     NaN/Inf which then corrupts SPOT-LEAK1D. (Fix: review 2026-05-05.)
      DO ISNAP=1,NSNAP
        IND=FINDLOC(MAT1D,ISNAP,DIM=1)
        IF(IND.EQ.0) CYCLE
        DO IG=1,NGRP
          IF(FLU2(IG,ISNAP).GT.0.0D0) THEN
            DB2(IG,ISNAP)=DB2(IG,ISNAP)/FLU2(IG,ISNAP)
          ELSE
            DB2(IG,ISNAP)=0.0D0
          ENDIF
        ENDDO
      ENDDO
*----
*  PRINT AXIAL LEAKAGE CROSS SECTIONS
*----
      IF(IMPX.GT.1) THEN
        DO IG=1,NGRP
          SSUM2=0.0
          DO ISNAP=1,NSNAP
            SSUM1=DB2(IG,ISNAP)*FLU2(IG,ISNAP)
            SSUM2=SSUM2+SSUM1
            WRITE(IOUT,300) ISNAP,IG,SSUM1
          ENDDO
          WRITE(IOUT,310) IG,SSUM2
        ENDDO
      ENDIF
      DEALLOCATE(VOL1D,MAT1D)
*----
*  STORE THE AXIAL LEAKAGE CROSS SECTIONS
*  Read previous SPOT-LEAK1D from IPSNAP (persistent across CLE-2000
*  outer iterations) rather than from IPFLUX. CLE-2000 forbids same
*  LCM name being recreated by FLU each iteration without DELETE,
*  but DELETE'ing FLUX_INT loses its SPOT-LEAK1D and prevents
*  under-relaxation / convergence detection. IPSNAP is the snapshot
*  archive on the procedure side; it survives across outer iterations
*  and SPODB2 itself writes back into it (lines 162-165 below), so
*  reading from IPSNAP is consistent storage.
*  Patch: B. Cui, W4 D5 prep, 2026-05-02.
*----
      ERROR=0.0
      DENOM=0.0
      DO ISNAP=1,NSNAP
        DO IG=1,NGRP
          DENOM=MAX(DENOM,ABS(DB2(IG,ISNAP)))
        ENDDO
      ENDDO
      IF(.NOT.C_ASSOCIATED(IPSNAP)) THEN
        ERROR=1.0E10
      ELSE
        JPSNAP=LCMGID(IPSNAP,'FLUX')
        ILONG=0
        IF(NSNAP.GT.0) THEN
          KPSNAP=LCMGIL(JPSNAP,1)
          CALL LCMLEN(KPSNAP,'SPOT-LEAK1D',ILONG,ITYLCM)
        ENDIF
        IF(ILONG.EQ.0) THEN
          ERROR=1.0E10
        ELSE
          ALLOCATE(OLD(NGRP,NSNAP))
          DO ISNAP=1,NSNAP
            KPSNAP=LCMGIL(JPSNAP,ISNAP)
            CALL LCMGET(KPSNAP,'SPOT-LEAK1D',OLD(:,ISNAP))
          ENDDO
          DO ISNAP=1,NSNAP
            DO IG=1,NGRP
              ! perform underrelaxation
              DB2(IG,ISNAP)=0.5*DB2(IG,ISNAP)+0.5*OLD(IG,ISNAP)
              SSUM1=ABS(DB2(IG,ISNAP)-OLD(IG,ISNAP))
              ERROR=MAX(ERROR,SSUM1)
            ENDDO
          ENDDO
          DEALLOCATE(OLD)
        ENDIF
      ENDIF
      IF(IMPX.GT.0) THEN
        DO ISNAP=1,NSNAP
          WRITE(6,'(31H SPODB2: AXIAL LEAKAGE IN FLOOR,I5,1H:)') ISNAP
          WRITE(6,'(1P,12E12.4)') DB2(:NGRP,ISNAP)
        ENDDO
      ENDIF
      CALL LCMPUT(IPFLUX,'SPOT-LEAK1D',NGRP*NSNAP,2,DB2)
      IF(IMPX.GT.0) WRITE(IOUT,320) ERROR,DENOM
*----
*  SAVE LEAK1D INFORMATION IN IPSNAP
*----
      IF(.NOT.C_ASSOCIATED(IPSNAP)) CALL XABORT('SPODB2: IPSNAP IS NOT'
     1 //' DEFINED.')
      JPSNAP=LCMGID(IPSNAP,'FLUX')
      DO ISNAP=1,NSNAP
        KPSNAP=LCMGIL(JPSNAP,ISNAP)
        CALL LCMPUT(KPSNAP,'SPOT-LEAK1D',NGRP,2,DB2(:NGRP,ISNAP))
      ENDDO
      DEALLOCATE(FLU2,DB2)
*----
*  SAVE THE LEAK1D ACCURACY IN A CLE-2000 VARIABLE
*----
      IF(IPICK.EQ.1) THEN
        CALL REDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)
        IF(INDIC.NE.-2) CALL XABORT('SPODB2: OUTPUT REAL EXPECTED.')
        INDIC=2
        CALL REDPUT(INDIC,NITMA,ERROR,TEXT4,DFLOTT)
        CALL REDGET(INDIC,NITMA,FLOTT,TEXT4,DFLOTT)
        IF((INDIC.NE.3).OR.(TEXT4.NE.';')) THEN
          CALL XABORT('SPODB2: ; CHARACTER EXPECTED.')
        ENDIF
      ENDIF
      RETURN
*
  300 FORMAT(43H SPODB2: AXIAL NEUTRON BALANCE FOR SNAPSHOT,I5,
     1 9H IN GROUP,I5,2H =,1P,E12.4)
  310 FORMAT(46H SPODB2: GLOBAL AXIAL NEUTRON BALANCE IN GROUP,
     1 I5,2H =,1P,E12.4)
  320 FORMAT(/25H SPODB2: LEAK1D ACCURACY=,1P,E11.4,3X,
     1 16HMAXIMUM LEAKAGE=,E11.4)
      END

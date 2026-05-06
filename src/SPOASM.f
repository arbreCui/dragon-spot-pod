*DECK SPOASM
      SUBROUTINE SPOASM(IPSYS,IPMACR,IPTRK,IPSNAP,IMPX,EPS_POD,RANK_POD)
*
*-----------------------------------------------------------------------
*
*Purpose:
* Dragon assembly of SPOT information.
*
* When EPS_POD > 0 or RANK_POD > 0 the per-group radial leakage matrix
* LEAK2D is compressed by Proper Orthogonal Decomposition through the
* SPOPOD subroutine before being stored in the SPOT system. This
* regularises the SPOT external leakage iteration.
*
*Copyright:
* Copyright (C) 2024 Ecole Polytechnique de Montreal
* This library is free software; you can redistribute it and/or
* modify it under the terms of the GNU Lesser General Public
* License as published by the Free Software Foundation; either
* version 2.1 of the License, or (at your option) any later version
*
*Author(s): A. Hebert (2D/1D synthesis), B. Cui (POD extension)
*
*Parameters: input
* IPSYS    pointer to the pij LCM object.
* IPMACR   pointer to the macrolib LCM object.
* IPTRK    pointer to the tracking LCM object.
* IPSNAP   pointer to the snapshot archive object.
* IMPX     print flag (equal to zero for no print).
* EPS_POD  POD truncation tolerance (sigma_r/sigma_1). <=0 disables POD.
* RANK_POD POD explicit rank cap. <=0 means use EPS_POD only.
*
*-----------------------------------------------------------------------
*
      USE GANLIB
*----
*  SUBROUTINE ARGUMENTS
*----
      TYPE(C_PTR) IPSYS,IPMACR,IPTRK,IPSNAP
      INTEGER IMPX,RANK_POD
      REAL    EPS_POD
*----
*  LOCAL VARIABLES
*----
      PARAMETER(NSTATE=40,IOUT=6)
      INTEGER IPAR(NSTATE),ISTATE(NSTATE),IRANK,IRMIN,IRMAX,LSIG_LEN,
     1 ISIG
      LOGICAL LPOD
      REAL    PHI_MIN_POD,FLU_FLOOR,FLUX_MEAN
      INTEGER NFLUX_BELOW
      DOUBLE PRECISION ERR_PRE_POD,ERR_POST_POD
      DOUBLE PRECISION SSUM
      TYPE(C_PTR) JPSNAP1,JPSNAP2,JPSNAP3,KPSNAP,LPSNAP,MPSNAP,IPFLUX,
     1 IPSOUR,JPSYS,KPSYS
      CHARACTER HSMG*131
*----
*  ALLOCATABLE ARRAYS
*----
      INTEGER, ALLOCATABLE, DIMENSION(:) :: IDL2D,MAT2D
      REAL, ALLOCATABLE, DIMENSION(:) :: VOL2D,TXSC2D,LEAK1D
      REAL, ALLOCATABLE, DIMENSION(:,:) :: SXSC2D,TXSC
      REAL, ALLOCATABLE, DIMENSION(:,:,:) :: SXSC,FLUX2D,SOUR2D
      INTEGER, ALLOCATABLE, DIMENSION(:) :: POD_RANK
      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:) :: W
      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:) :: POD_SIG
      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:,:) :: DB2
*     Variant III: arrays for snapshot fluxes and volumes
      REAL, ALLOCATABLE, DIMENSION(:)     :: VOLREG
      REAL, ALLOCATABLE, DIMENSION(:,:,:) :: PHIRK
*----
*  RECOVER GENERAL TRACKING INFORMATION
*----
      CALL LCMGET(IPTRK,'STATE-VECTOR',IPAR)
      NREG=IPAR(1)
      NUNKN=IPAR(2)
      NMIX=IPAR(4)
      NREG2D=IPAR(6)
      NFLOOR=IPAR(7)
      ISCAT=IPAR(16)
*----
*  RECOVER 2D TRACKING INFORMATION FROM IPSNAP
*----
      ALLOCATE(MAT2D(NREG),IDL2D(NREG),VOL2D(NREG))
      CALL LCMGET(IPSNAP,'LISTDIM',NSNAP)
      JPSNAP1=LCMGID(IPSNAP,'TRACK')
      NUNK2D=0
      NMIX2D=0
      IBIHET=0
      DO ISNAP=1,NSNAP
        KPSNAP=LCMGIL(JPSNAP1,ISNAP)
        CALL LCMGET(KPSNAP,'STATE-VECTOR',IPAR)
        NMIX2D=MAX(NMIX2D,IPAR(4))
        IF(NREG2D.NE.IPAR(1)) THEN
          CALL XABORT('SPOASM: INVALID VALUE OF NREG2D.')
        ENDIF
        IF(ISNAP.EQ.1) THEN
          NUNK2D=IPAR(2)
          IBIHET=IPAR(40)
        ELSE
          IF(NUNK2D.NE.IPAR(2)) THEN
            CALL XABORT('SPOASM: INVALID VALUE OF NUNK2D.')
          ELSE IF(IBIHET.NE.IPAR(40)) THEN
            CALL XABORT('SPOASM: INVALID VALUE OF IBIHET.')
          ENDIF
        ENDIF
      ENDDO
      IF(NMIX2D.NE.NMIX) CALL XABORT('SPOASM: INCONSISTENT MIXTURES.')
*----
*  RECOVER MACROLIB INFORMATION
*----
      CALL LCMGET(IPMACR,'STATE-VECTOR',IPAR)
      NGRP=IPAR(1)
      MAXMIX=IPAR(2)
      IF(IMPX.GE.3) WRITE(IOUT,'(A,I0)') ' SPOASM: MAXMIX=',MAXMIX
      NANIS=IPAR(3)
      ITRANC=IPAR(6)
      NALBP=IPAR(8)
      NW=IPAR(10)
      IF(NMIX.GT.MAXMIX) THEN
         WRITE(HSMG,'(45HSPOASM: THE NUMBER OF MIXTURES IN THE TRACKIN,
     1   3HG (,I5,49H) IS GREATER THAN THE NUMBER OF MIXTURES IN THE M,
     2   9HACROLIB (,I5,2H).)') NMIX,MAXMIX
         CALL XABORT(HSMG)
      ENDIF
*----
*  FIND MAXK2D
*----
      JPSNAP3=LCMGID(IPSNAP,'FLUX')
      MAXK2D=0
      DO ISNAP=1,NSNAP
        KPSNAP=LCMGIL(JPSNAP3,ISNAP)
        IPFLUX=LCMGID(KPSNAP,'FLUX')
        CALL LCMLEL(IPFLUX,1,ILONG,ITYLCM)
        MAXK2D=MAX(MAXK2D,ILONG)
      ENDDO
*----
*  RECOVER THE FLUX AND SOURCE SNAPSHOTS
*----
      ALLOCATE(FLUX2D(MAXK2D,NSNAP,NGRP),SOUR2D(MAXK2D,NSNAP,NGRP))
      DO ISNAP=1,NSNAP
        KPSNAP=LCMGIL(JPSNAP3,ISNAP)
        IPFLUX=LCMGID(KPSNAP,'FLUX')
        DO IGR=1,NGRP
          CALL LCMGDL(IPFLUX,IGR,FLUX2D(1,ISNAP,IGR))
        ENDDO
        IPSOUR=LCMGID(KPSNAP,'SOUR')
        DO IGR=1,NGRP
          CALL LCMGDL(IPSOUR,IGR,SOUR2D(1,ISNAP,IGR))
        ENDDO
      ENDDO
*----
*   RECOVER RADIAL LEAKAGE CROSS SECTIONS
*----
      ALLOCATE(DB2(NSNAP,NREG2D,NGRP),TXSC(0:MAXMIX,NGRP),
     1 SXSC(0:MAXMIX,NANIS,NGRP))
      DB2(:NSNAP,:NREG2D,:NGRP)=0.D0
      TXSC(0:MAXMIX,:NGRP)=0.0
      SXSC(0:MAXMIX,:NANIS,:NGRP)=0.0
*     Variant III: allocate phi^k_{g,i} and V_i arrays
      ALLOCATE(PHIRK(NREG2D,NSNAP,NGRP),VOLREG(NREG2D))
      PHIRK(:NREG2D,:NSNAP,:NGRP)=0.0
      VOLREG(:NREG2D)=0.0
*     FLU_FLOOR: absolute hard floor below which a cell flux is treated
*     as numerically zero to avoid SOUR2D/FLUX2D blow-up. Set very tiny
*     so legitimate low-flux cells (void regions, deep reflector) are
*     NOT modified -- only true zeros / negatives / sub-tiny() values.
*     Reviewer's concern: an aggressive relative floor (e.g. 1E-12 of mean)
*     changes baseline keff because it zeros out cells that should still
*     contribute. Stick to absolute tiny value to preserve baseline.
      FLU_FLOOR=1.0E-30
      NFLUX_BELOW=0
      JPSNAP1=LCMGID(IPSNAP,'TRACK')
      JPSNAP2=LCMGID(IPSNAP,'SYSTEM')
      JPSNAP3=LCMGID(IPSNAP,'FLUX')
      ALLOCATE(LEAK1D(NGRP))
      DO ISNAP=1,NSNAP
        ! recover axial leakage information
        KPSNAP=LCMGIL(JPSNAP3,ISNAP)
        CALL LCMLEN(KPSNAP,'SPOT-LEAK1D',ILONG,ITYLCM)
        IF(ILONG.EQ.NGRP) THEN
          CALL LCMGET(KPSNAP,'SPOT-LEAK1D',LEAK1D)
        ELSE
          LEAK1D(:NGRP)=0.0
        ENDIF
        ! recover other reaction rates
        KPSNAP=LCMGIL(JPSNAP1,ISNAP)
        CALL LCMGET(KPSNAP,'KEYFLX',IDL2D)
        CALL LCMGET(KPSNAP,'MATCOD',MAT2D)
        CALL LCMGET(KPSNAP,'VOLUME',VOL2D)
        KPSNAP=LCMGIL(JPSNAP2,ISNAP)
        CALL LCMGET(KPSNAP,'STATE-VECTOR',IPAR)
        IF(NGRP.NE.IPAR(8)) THEN
          print *,'NGRP=',NGRP,' IPAR(8)=',IPAR(8)
          CALL XABORT('SPOASM: INVALID VALUE OF NGRP.')
        ELSE IF(NUNK2D.NE.IPAR(9)) THEN
          print *,'NUNK2D=',NUNK2D,' IPAR(9)=',IPAR(9)
          CALL XABORT('SPOASM: INVALID VALUE OF NUNK2D.')
        ENDIF   
        LPSNAP=LCMGID(KPSNAP,'GROUP')
        DO IGR=1,NGRP
          ALLOCATE(TXSC2D(0:MAXMIX),SXSC2D(0:MAXMIX,NANIS))
          MPSNAP=LCMGIL(LPSNAP,IGR)
          CALL LCMGET(MPSNAP,'DRAGON-TXSC',TXSC2D)
          CALL LCMGET(MPSNAP,'DRAGON-S0XSC',SXSC2D)
          TXSC(0:MAXMIX,IGR)=TXSC2D(0:MAXMIX)
          SXSC(0:MAXMIX,:NANIS,IGR)=SXSC2D(0:MAXMIX,:NANIS)
          SSUM=0.0
          DO I=1,NREG2D
            IBM=MAT2D(I)
            IF(IBM.EQ.0) CYCLE
            IF(IBM.GT.MAXMIX) CALL XABORT('SPOASM: IBM OVERFLOW.')
            IUNK=IDL2D(I)
            IF(IUNK.EQ.0) CYCLE
*           Zero/low-flux guard: only triggers for true zero or negative.
*           Strict < (not <=) so FLUX2D = FLU_FLOOR exactly is treated as
*           legitimate. With FLU_FLOOR=1E-30 this is a defensive net only;
*           genuine void cells with phi ~ 1E-13 are NOT modified.
            IF(FLUX2D(IUNK,ISNAP,IGR).LT.FLU_FLOOR) THEN
              DB2(ISNAP,I,IGR)=0.0D0
              PHIRK(I,ISNAP,IGR)=0.0
              IF(ISNAP.EQ.1.AND.IGR.EQ.1) VOLREG(I)=VOL2D(I)
              NFLUX_BELOW=NFLUX_BELOW+1
              CYCLE
            ENDIF
            DB2(ISNAP,I,IGR)=-TXSC2D(IBM)+SXSC2D(IBM,1)-LEAK1D(IGR)+
     1      SOUR2D(IUNK,ISNAP,IGR)/FLUX2D(IUNK,ISNAP,IGR)
            SSUM=SSUM+DB2(ISNAP,I,IGR)*FLUX2D(IUNK,ISNAP,IGR)*VOL2D(I)
*           Variant III: store the per-region snapshot flux and (once)
*           the region volume for downstream POD on V*L*phi.
            PHIRK(I,ISNAP,IGR)=FLUX2D(IUNK,ISNAP,IGR)
            IF(ISNAP.EQ.1.AND.IGR.EQ.1) VOLREG(I)=VOL2D(I)
          ENDDO
          IF(IMPX.GT.1) WRITE(IOUT,100) ISNAP,IGR,SSUM
          DEALLOCATE(SXSC2D,TXSC2D)
        ENDDO
      ENDDO
      DEALLOCATE(LEAK1D)
*----
*   CREATE SPOT SYSTEM OBJECT
*----
      ISTATE(:NSTATE)=0
      ISTATE(1)=1
      ISTATE(2)=1
      ISTATE(3)=1
      ISTATE(5)=1
      ISTATE(6)=1
      ISTATE(8)=NGRP
      ISTATE(9)=NUNKN
      ISTATE(10)=MAXMIX
      ISTATE(11)=ISCAT
      ISTATE(14)=-1
      CALL LCMPUT(IPSYS,'STATE-VECTOR',NSTATE,1,ISTATE)
      JPSYS=LCMLID(IPSYS,'GROUP',NGRP)
*----
*  POD COMPRESSION OF LEAK2D (per energy group).
*  Active when EPS_POD > 0 or RANK_POD > 0; otherwise SPOPOD returns
*  DB2 unchanged. Singular spectrum and effective rank are stored in
*  the SPOT system for downstream diagnostics.
*----
      ALLOCATE(W(NSNAP))
      ALLOCATE(POD_RANK(NGRP))
      LSIG_LEN=NSNAP
      ALLOCATE(POD_SIG(LSIG_LEN,NGRP))
      POD_SIG(:LSIG_LEN,:NGRP)=0.0D0
      LPOD=(EPS_POD.GT.0.0).OR.(RANK_POD.GT.0)
*     S1 phi floor: tied to FLU_FLOOR computed earlier so that POD
*     reconstruction matches the SPOASM zero-flux guard policy.
*     Could be exposed as a CLE-2000 keyword later.
      PHI_MIN_POD=FLU_FLOOR
      ERR_PRE_POD =0.0D0
      ERR_POST_POD=0.0D0
      IF(IMPX.GE.1.AND.LPOD) THEN
        WRITE(IOUT,200) EPS_POD,RANK_POD
      ENDIF
      DO IGR=1,NGRP
        KPSYS=LCMDIL(JPSYS,IGR)
        CALL LCMPUT(KPSYS,'DRAGON-TXSC',MAXMIX+1,2,TXSC(0,IGR))
        CALL LCMPUT(KPSYS,'DRAGON-S0XSC',(MAXMIX+1)*NANIS,2,
     1  SXSC(0,1,IGR))
        CALL LCMPUT(KPSYS,'NREG2D',1,1,NREG2D)
        CALL LCMPUT(KPSYS,'NSNAP',1,1,NSNAP)
*       Variant III: POD filtering of L^{2D} via SVD on V*L*phi.
*       SPOPOD is called only when POD is actively requested (LPOD true);
*       otherwise we skip to keep baseline byte-identical with H\'ebert
*       ev3809. This is critical: even calling SPOPOD with EPS_POD<=0
*       writes diagnostic LCM records that perturb the LCM directory layout
*       and shift baseline keff (W2 D2 finding).
        IF(LPOD) THEN
          CALL SPOPOD(NREG2D,NSNAP,DB2(1,1,IGR),
     1                PHIRK(1,1,IGR),VOLREG,
     2                EPS_POD,RANK_POD,PHI_MIN_POD,
     3                IRANK,W,
     4                ERR_PRE_POD,ERR_POST_POD,
     5                IMPX,IGR)
          POD_RANK(IGR)=IRANK
          DO ISIG=1,MIN(NSNAP,LSIG_LEN)
            POD_SIG(ISIG,IGR)=W(ISIG)
          ENDDO
        ELSE
          POD_RANK(IGR)=NSNAP
        ENDIF
        CALL LCMPUT(KPSYS,'LEAK2D',NSNAP*NREG2D,4,DB2(1,1,IGR))
        IF(LPOD) THEN
          CALL LCMPUT(KPSYS,'POD-RANK',1,1,IRANK)
          CALL LCMPUT(KPSYS,'POD-SIGMA',NSNAP,4,W)
          CALL LCMPUT(KPSYS,'POD-ERR-PRE',1,4,ERR_PRE_POD)
          CALL LCMPUT(KPSYS,'POD-ERR-POST',1,4,ERR_POST_POD)
        ENDIF
      ENDDO
      IF(LPOD) THEN
        CALL LCMPUT(IPSYS,'POD-RANK-G',NGRP,1,POD_RANK)
        CALL LCMPUT(IPSYS,'POD-SIGMA-G',LSIG_LEN*NGRP,4,POD_SIG)
      ENDIF
      IF(IMPX.GE.1.AND.LPOD) THEN
        IRMIN=POD_RANK(1)
        IRMAX=POD_RANK(1)
        DO IGR=2,NGRP
          IF(POD_RANK(IGR).LT.IRMIN) IRMIN=POD_RANK(IGR)
          IF(POD_RANK(IGR).GT.IRMAX) IRMAX=POD_RANK(IGR)
        ENDDO
        WRITE(IOUT,210) NGRP,IRMIN,IRMAX,NSNAP
      ENDIF
      IF(IMPX.GE.1.AND.NFLUX_BELOW.GT.0) THEN
        WRITE(IOUT,220) NFLUX_BELOW,FLU_FLOOR
      ENDIF
*----
*  SCRATCH STORAGE DEALLOCATION
*----
      DEALLOCATE(POD_SIG,POD_RANK,W)
      DEALLOCATE(VOLREG,PHIRK)
      DEALLOCATE(VOL2D,IDL2D,MAT2D)
      DEALLOCATE(SXSC,TXSC,DB2,SOUR2D,FLUX2D)
      RETURN
  100 FORMAT(44H SPOASM: RADIAL NEUTRON BALANCE FOR SNAPSHOT,I5,
     1 9H IN GROUP,I5,2H =,1P,E12.4)
  200 FORMAT(/' SPOASM: POD compression of LEAK2D enabled. ',
     1 'eps_pod=',1P,E10.3,'  rank_max=',I3)
  210 FORMAT(' SPOASM: POD ranks across',I4,' groups: min=',I3,
     1 ', max=',I3,' (out of NSNAP=',I3,')')
  220 FORMAT(' SPOASM: ',I0,' (snap,reg,grp) cells had FLUX2D <= ',
     1 1P,E10.3,' and were guarded against zero-flux division')
      END

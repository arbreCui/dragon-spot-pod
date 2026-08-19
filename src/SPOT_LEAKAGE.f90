module SPOT_LEAKAGE
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  private
  public :: SPOLE1, SPOLE1D, SPOLE2, SPOLE2D, SPOF00, SPOQ00, SPOQFS
  public :: SPOQFSD

contains

  ! Return the axial leakage coefficient for every snapshot.  Positive
  ! LEAK1D means net axial loss.  AREA is the 2D region volume (cm2 in an
  ! extruded model), DZ is the floor height, PHI is the cell scalar flux,
  ! and CURRENT is the signed axial current on the floor faces.
  subroutine SPOLE1(nreg,nfloor,nsnap,mat1d,dz,area,phi,current, &
                    leak1d,numerator,denominator)
    integer, intent(in) :: nreg,nfloor,nsnap
    integer, intent(in) :: mat1d(nfloor)
    real, intent(in) :: dz(nfloor),area(nreg)
    real, intent(in) :: phi(nfloor,nreg),current(nfloor+1,nreg)
    real, intent(out) :: leak1d(nsnap),numerator(nsnap),denominator(nsnap)

    integer :: i,ifloor,isnap

    if (nreg <= 0 .or. nfloor <= 0 .or. nsnap <= 0) &
      call XABORT('SPOLE1: INVALID DIMENSION.')
    if (any(mat1d < 1) .or. any(mat1d > nsnap)) &
      call XABORT('SPOLE1: INVALID SNAPSHOT INDEX.')
    if (any(dz <= 0.0) .or. any(area <= 0.0)) &
      call XABORT('SPOLE1: NONPOSITIVE GEOMETRIC MEASURE.')

    numerator=0.0
    denominator=0.0
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      do i=1,nreg
        numerator(isnap)=numerator(isnap)+area(i)* &
          (current(ifloor+1,i)-current(ifloor,i))
        denominator(isnap)=denominator(isnap)+ &
          area(i)*dz(ifloor)*phi(ifloor,i)
      enddo
    enddo

    leak1d=0.0
    do isnap=1,nsnap
      if (denominator(isnap) > 0.0) then
        leak1d(isnap)=numerator(isnap)/denominator(isnap)
      else if (denominator(isnap) < 0.0) then
        call XABORT('SPOLE1: NEGATIVE FLUX INTEGRAL.')
      endif
    enddo
  end subroutine SPOLE1

  ! Double-precision twin of SPOLE1: identical geometry and admission
  ! checks, REAL64 flux/current input and REAL64 accumulation.
  subroutine SPOLE1D(nreg,nfloor,nsnap,mat1d,dz,area,phi,current, &
                     leak1d,numerator,denominator)
    integer, intent(in) :: nreg,nfloor,nsnap
    integer, intent(in) :: mat1d(nfloor)
    real, intent(in) :: dz(nfloor),area(nreg)
    double precision, intent(in) :: phi(nfloor,nreg)
    double precision, intent(in) :: current(nfloor+1,nreg)
    double precision, intent(out) :: leak1d(nsnap),numerator(nsnap), &
      denominator(nsnap)

    integer :: i,ifloor,isnap

    if (nreg <= 0 .or. nfloor <= 0 .or. nsnap <= 0) &
      call XABORT('SPOLE1D: INVALID DIMENSION.')
    if (any(mat1d < 1) .or. any(mat1d > nsnap)) &
      call XABORT('SPOLE1D: INVALID SNAPSHOT INDEX.')
    if (any(dz <= 0.0) .or. any(area <= 0.0)) &
      call XABORT('SPOLE1D: NONPOSITIVE GEOMETRIC MEASURE.')

    numerator=0.0d0
    denominator=0.0d0
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      do i=1,nreg
        numerator(isnap)=numerator(isnap)+dble(area(i))* &
          (current(ifloor+1,i)-current(ifloor,i))
        denominator(isnap)=denominator(isnap)+ &
          dble(area(i))*dble(dz(ifloor))*phi(ifloor,i)
      enddo
    enddo

    leak1d=0.0d0
    do isnap=1,nsnap
      if (denominator(isnap) > 0.0d0) then
        leak1d(isnap)=numerator(isnap)/denominator(isnap)
      else if (denominator(isnap) < 0.0d0) then
        call XABORT('SPOLE1D: NEGATIVE FLUX INTEGRAL.')
      endif
    enddo
  end subroutine SPOLE1D

  ! Local radial current-divergence coefficient obtained from the converged
  ! 2D scalar balance.  LEAK1D is positive for axial loss and is therefore
  ! subtracted from the right-hand-side balance.
  elemental real function SPOLE2(total,scatter0,qfixed,phi,leak1d)
    real, intent(in) :: total,scatter0,qfixed,phi,leak1d

    SPOLE2=-total+scatter0+qfixed/phi-leak1d
  end function SPOLE2

  ! Double-precision twin of SPOLE2.  The state-dependent source and
  ! flux arrive in double precision; the frozen REAL32 cross sections
  ! and the REAL32 axial leakage are promoted at the point of use,
  ! mirroring SPOLE1D's treatment of REAL32 inputs.  Same expression.
  elemental double precision function SPOLE2D(total,scatter0,qfixed, &
      phi,leak1d)
    real, intent(in) :: total,scatter0,leak1d
    double precision, intent(in) :: qfixed,phi

    SPOLE2D=-dble(total)+dble(scatter0)+qfixed/phi-dble(leak1d)
  end function SPOLE2D

  ! Precompute sum_h(nu*Sigma_f)_h*phi_h for every active cell and fission
  ! component.  Keeping this intermediate in double precision preserves
  ! SPOQ00's original multiply-then-divide operation order for every target
  ! group.  This is an exact loop hoist, not an approximation or new model.
  subroutine SPOF00(nreg,ngrp,nmix,nfis,mat,phi,nusigf,fission_prod)
    integer, intent(in) :: nreg,ngrp,nmix,nfis
    integer, intent(in) :: mat(nreg)
    real, intent(in) :: phi(nreg,ngrp)
    real, intent(in) :: nusigf(nmix,nfis,ngrp)
    double precision, intent(out) :: fission_prod(nreg,nfis)

    integer :: i,ibm,ifis,jg
    double precision :: production

    if ((nreg <= 0).or.(ngrp <= 0).or.(nmix <= 0).or.(nfis < 0)) &
      call XABORT('SPOF00: INVALID DIMENSION.')
    if (any((mat < 0).or.(mat > nmix))) &
      call XABORT('SPOF00: MATERIAL INDEX OVERFLOW.')
    if (any(.not.ieee_is_finite(phi)).or. &
        any(.not.ieee_is_finite(nusigf))) &
      call XABORT('SPOF00: NON-FINITE PHYSICAL INPUT.')

    fission_prod=0.0d0
    do i=1,nreg
      ibm=mat(i)
      if (ibm == 0) cycle
      do ifis=1,nfis
        production=0.0d0
        do jg=1,ngrp
          production=production+dble(nusigf(ibm,ifis,jg))* &
            dble(phi(i,jg))
        enddo
        fission_prod(i,ifis)=production
      enddo
    enddo
    if (any(.not.ieee_is_finite(fission_prod))) &
      call XABORT('SPOF00: NON-FINITE FISSION PRODUCTION.')
  end subroutine SPOF00

  ! Evaluate the physical P0 right-hand side on one final multigroup
  ! state.  The optional FISSION_PROD is the exact SPOF00 result and avoids
  ! repeating the source-group reduction for every target group.  If it is
  ! absent, this routine evaluates the same reduction itself.
  !
  ! The compressed scattering map follows FLU2DR exactly: IJJS is the
  ! first source group and the following NJJS entries descend one group at
  ! a time.  Self scattering is excluded because it remains on the left-
  ! hand side.  No saved iteration work source enters.
  subroutine SPOQ00(nreg,ngrp,nmix,nfis,igr,mat,phi,keff,njjs,ijjs, &
                    ipos,scat,chi,nusigf,qtotal,fission_prod)
    integer, intent(in) :: nreg,ngrp,nmix,nfis,igr
    integer, intent(in) :: mat(nreg),njjs(nmix),ijjs(nmix),ipos(nmix)
    real, intent(in) :: phi(nreg,ngrp),keff,scat(:)
    real, intent(in) :: chi(nmix,nfis),nusigf(nmix,nfis,ngrp)
    real, intent(out) :: qtotal(nreg)
    double precision, intent(in), optional :: fission_prod(nreg,nfis)

    integer :: i,ibm,ifis,jg,jnd,index0
    double precision :: source
    double precision, allocatable :: fission_work(:,:)

    if ((nreg <= 0).or.(ngrp <= 0).or.(nmix <= 0).or.(nfis < 0)) &
      call XABORT('SPOQ00: INVALID DIMENSION.')
    if ((igr < 1).or.(igr > ngrp)) &
      call XABORT('SPOQ00: INVALID TARGET GROUP.')
    if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0)) &
      call XABORT('SPOQ00: INVALID SNAPSHOT EIGENVALUE.')
    if (any((mat < 0).or.(mat > nmix))) &
      call XABORT('SPOQ00: MATERIAL INDEX OVERFLOW.')
    if (any(.not.ieee_is_finite(phi)).or. &
        any(.not.ieee_is_finite(chi)).or. &
        any(.not.ieee_is_finite(scat))) &
      call XABORT('SPOQ00: NON-FINITE PHYSICAL INPUT.')

    allocate(fission_work(nreg,nfis))
    if (present(fission_prod)) then
      if (any(.not.ieee_is_finite(fission_prod))) &
        call XABORT('SPOQ00: NON-FINITE FISSION PRODUCTION.')
      fission_work=fission_prod
    else
      call SPOF00(nreg,ngrp,nmix,nfis,mat,phi,nusigf,fission_work)
    endif

    qtotal=0.0
    do i=1,nreg
      ibm=mat(i)
      if (ibm == 0) cycle
      source=0.0d0
      do ifis=1,nfis
        source=source+dble(chi(ibm,ifis))*fission_work(i,ifis)/ &
          dble(keff)
      enddo

      if (njjs(ibm) < 0) call XABORT('SPOQ00: NEGATIVE NJJS00.')
      jg=ijjs(ibm)
      do jnd=1,njjs(ibm)
        index0=ipos(ibm)+jnd-1
        if ((jg < 1).or.(jg > ngrp).or.(index0 < 1).or. &
            (index0 > size(scat))) &
          call XABORT('SPOQ00: COMPRESSED SCATTER MAP OVERFLOW.')
        if (jg /= igr) source=source+dble(scat(index0))*dble(phi(i,jg))
        jg=jg-1
      enddo
      qtotal(i)=real(source)
    enddo
    if (any(.not.ieee_is_finite(qtotal))) &
      call XABORT('SPOQ00: NON-FINITE RECONSTRUCTED SOURCE.')
    deallocate(fission_work)
  end subroutine SPOQ00

  ! Evaluate the physical P0 source for an online radial fixed-source
  ! update. QFROZEN is exactly the fission source F*p_old/k_old used by that
  ! solve. Off-group scattering is evaluated on the final radial flux. This
  ! keeps the response operator and the radial equation on the same RHS.
  subroutine SPOQFS(nreg,ngrp,nmix,igr,mat,phi,njjs,ijjs,ipos,scat, &
                    qfrozen,qtotal)
    integer, intent(in) :: nreg,ngrp,nmix,igr
    integer, intent(in) :: mat(nreg),njjs(nmix),ijjs(nmix),ipos(nmix)
    real, intent(in) :: phi(nreg,ngrp),scat(:),qfrozen(nreg)
    real, intent(out) :: qtotal(nreg)

    integer :: i,ibm,jg,jnd,index0
    double precision :: source

    if ((nreg <= 0).or.(ngrp <= 0).or.(nmix <= 0)) &
      call XABORT('SPOQFS: INVALID DIMENSION.')
    if ((igr < 1).or.(igr > ngrp)) &
      call XABORT('SPOQFS: INVALID TARGET GROUP.')
    if (any((mat < 0).or.(mat > nmix))) &
      call XABORT('SPOQFS: MATERIAL INDEX OVERFLOW.')
    if (any(.not.ieee_is_finite(phi)).or. &
        any(.not.ieee_is_finite(scat)).or. &
        any(.not.ieee_is_finite(qfrozen))) &
      call XABORT('SPOQFS: NON-FINITE PHYSICAL INPUT.')

    qtotal=0.0
    do i=1,nreg
      ibm=mat(i)
      if (ibm == 0) cycle
      source=dble(qfrozen(i))
      if (njjs(ibm) < 0) call XABORT('SPOQFS: NEGATIVE NJJS00.')
      jg=ijjs(ibm)
      do jnd=1,njjs(ibm)
        index0=ipos(ibm)+jnd-1
        if ((jg < 1).or.(jg > ngrp).or.(index0 < 1).or. &
            (index0 > size(scat))) &
          call XABORT('SPOQFS: COMPRESSED SCATTER MAP OVERFLOW.')
        if (jg /= igr) source=source+dble(scat(index0))*dble(phi(i,jg))
        jg=jg-1
      enddo
      qtotal(i)=real(source)
    enddo
    if (any(.not.ieee_is_finite(qtotal))) &
      call XABORT('SPOQFS: NON-FINITE FIXED-SOURCE RHS.')
  end subroutine SPOQFS

  ! Double-precision twin of SPOQFS.  The accumulation was already
  ! double precision; this variant takes the state-dependent flux and
  ! frozen fission source in double precision and keeps the result in
  ! double precision instead of demoting it.  Same loop, same guards.
  subroutine SPOQFSD(nreg,ngrp,nmix,igr,mat,phi,njjs,ijjs,ipos,scat, &
                     qfrozen,qtotal)
    integer, intent(in) :: nreg,ngrp,nmix,igr
    integer, intent(in) :: mat(nreg),njjs(nmix),ijjs(nmix),ipos(nmix)
    double precision, intent(in) :: phi(nreg,ngrp),qfrozen(nreg)
    real, intent(in) :: scat(:)
    double precision, intent(out) :: qtotal(nreg)

    integer :: i,ibm,jg,jnd,index0
    double precision :: source

    if ((nreg <= 0).or.(ngrp <= 0).or.(nmix <= 0)) &
      call XABORT('SPOQFSD: INVALID DIMENSION.')
    if ((igr < 1).or.(igr > ngrp)) &
      call XABORT('SPOQFSD: INVALID TARGET GROUP.')
    if (any((mat < 0).or.(mat > nmix))) &
      call XABORT('SPOQFSD: MATERIAL INDEX OVERFLOW.')
    if (any(.not.ieee_is_finite(phi)).or. &
        any(.not.ieee_is_finite(scat)).or. &
        any(.not.ieee_is_finite(qfrozen))) &
      call XABORT('SPOQFSD: NON-FINITE PHYSICAL INPUT.')

    qtotal=0.0d0
    do i=1,nreg
      ibm=mat(i)
      if (ibm == 0) cycle
      source=qfrozen(i)
      if (njjs(ibm) < 0) call XABORT('SPOQFSD: NEGATIVE NJJS00.')
      jg=ijjs(ibm)
      do jnd=1,njjs(ibm)
        index0=ipos(ibm)+jnd-1
        if ((jg < 1).or.(jg > ngrp).or.(index0 < 1).or. &
            (index0 > size(scat))) &
          call XABORT('SPOQFSD: COMPRESSED SCATTER MAP OVERFLOW.')
        if (jg /= igr) source=source+dble(scat(index0))*phi(i,jg)
        jg=jg-1
      enddo
      qtotal(i)=source
    enddo
    if (any(.not.ieee_is_finite(qtotal))) &
      call XABORT('SPOQFSD: NON-FINITE FIXED-SOURCE RHS.')
  end subroutine SPOQFSD

end module SPOT_LEAKAGE

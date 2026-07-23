!DECK SPOLEAK
subroutine SPOLEAK(nentry,hentry,ientry,jentry,kentry)
  ! Update the axial leakage coefficients stored in a SPOT snapshot archive.
  !
  !   SNAP := SPOLEAK: SNAP AXFLUX SPOTRK :: >>error<< ;
  !
  ! Positive SPOT-LEAK1D denotes net axial loss.  ERROR is the maximum
  ! absolute direct change, in inverse length.  The interface intentionally
  ! has no relaxation factor: the freshly integrated leakage is stored.
  use GANLIB
  use SPOT_LEAKAGE, only : SPOLE1
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate)
  integer :: ngrp,nunk,nreg,nreg2d,nfloor,nsnap,ll4,ll5
  integer :: igr,i,ifloor,iface,ireg,isnap,ilong,itylcm
  integer :: indic,nitma
  integer, allocatable :: keyflx(:),mat1d(:)
  real :: error,flott,keff
  double precision :: dflott,dkeff,expected_volume,volume_bound
  real, allocatable :: dz(:),volume(:),area(:),unknown(:)
  real, allocatable :: phi(:,:),current(:,:)
  real, allocatable :: fresh(:,:),old(:,:)
  real, allocatable :: numerator(:),denominator(:)
  character(len=4) :: text4
  character(len=12) :: signature,track_type
  type(c_ptr) :: jpflux,jpsnap,kpsnap

  if (nentry /= 3) call XABORT('SPOLEAK: THREE ENTRIES EXPECTED.')
  if ((ientry(1) /= 1).and.(ientry(1) /= 2)) &
    call XABORT('SPOLEAK: SNAPSHOT ARCHIVE EXPECTED.')
  if (jentry(1) /= 1) &
    call XABORT('SPOLEAK: SNAPSHOT ARCHIVE MUST BE MODIFIABLE.')
  if (any((ientry(2:3) /= 1).and.(ientry(2:3) /= 2)) .or. &
      any(jentry(2:3) /= 2)) &
    call XABORT('SPOLEAK: READ-ONLY FLUX AND TRACK EXPECTED.')

  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_ARCHIVE') &
    call XABORT('SPOLEAK: '//trim(hentry(1))//' IS NOT L_ARCHIVE.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') &
    call XABORT('SPOLEAK: '//trim(hentry(2))//' IS NOT L_FLUX.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') &
    call XABORT('SPOLEAK: '//trim(hentry(3))//' IS NOT L_TRACK.')
  call LCMGTC(kentry(3),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') call XABORT('SPOLEAK: SPOT TRACKING EXPECTED.')

  call LCMGET(kentry(1),'LISTDIM',nsnap)
  call LCMGET(kentry(2),'STATE-VECTOR',iflux)
  call LCMGET(kentry(3),'STATE-VECTOR',itrack)
  call LCMLEN(kentry(2),'K-EFFECTIVE',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 2)) &
    call XABORT('SPOLEAK: INVALID K-EFFECTIVE RECORD.')
  call LCMGET(kentry(2),'K-EFFECTIVE',keff)
  if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0)) &
    call XABORT('SPOLEAK: INVALID K-EFFECTIVE VALUE.')
  ngrp=iflux(1)
  nunk=iflux(2)
  nreg=itrack(1)
  nreg2d=itrack(6)
  nfloor=itrack(7)
  ll4=itrack(11)
  ll5=itrack(12)
  if ((ngrp <= 0).or.(nunk <= 0).or.(nunk /= itrack(2)).or. &
      (nsnap <= 0).or.(nsnap /= itrack(8))) &
    call XABORT('SPOLEAK: INCONSISTENT FLUX/TRACK/ARCHIVE DIMENSIONS.')
  if ((nreg2d <= 0).or.(nfloor <= 0).or.(ll4 < 0).or. &
      (nreg /= nreg2d*nfloor).or.(ll5 /= nreg2d*(nfloor+1)).or. &
      (ll4+ll5 > nunk)) &
    call XABORT('SPOLEAK: INVALID SPOT UNKNOWN LAYOUT.')

  allocate(keyflx(nreg),mat1d(nfloor))
  allocate(dz(nfloor),volume(nreg),area(nreg2d),unknown(nunk))
  allocate(phi(nfloor,nreg2d),current(nfloor+1,nreg2d))
  allocate(fresh(ngrp,nsnap),old(ngrp,nsnap))
  allocate(numerator(nsnap),denominator(nsnap))
  call LCMLEN(kentry(3),'AREA2D',ilong,itylcm)
  if ((ilong /= nreg2d).or.(itylcm /= 2)) &
    call XABORT('SPOLEAK: INVALID AREA2D RECORD.')
  call LCMGET(kentry(3),'KEYFLX',keyflx)
  call LCMGET(kentry(3),'MAT1D',mat1d)
  call LCMGET(kentry(3),'VOL1D',dz)
  call LCMGET(kentry(3),'VOLUME',volume)
  call LCMGET(kentry(3),'AREA2D',area)

  if (any(keyflx < 0).or.any(keyflx > nunk)) &
    call XABORT('SPOLEAK: INVALID KEYFLX INDEX.')

  if (any(.not.ieee_is_finite(area)).or.any(area <= 0.0)) &
    call XABORT('SPOLEAK: NON-FINITE OR NONPOSITIVE AREA2D.')
  if (any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0).or. &
      any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0)) &
    call XABORT('SPOLEAK: INVALID EXTRUDED GEOMETRY.')
  do i=1,nreg2d
    do ifloor=1,nfloor
      ireg=(i-1)*nfloor+ifloor
      expected_volume=dble(area(i))*dble(dz(ifloor))
      volume_bound=0.5d0*dble(spacing(volume(ireg)))
      if (abs(dble(volume(ireg))-expected_volume) > volume_bound) &
        call XABORT('SPOLEAK: INCONSISTENT EXTRUDED VOLUME.')
    enddo
  enddo

  jpflux=LCMGID(kentry(2),'FLUX')
  do igr=1,ngrp
    call LCMLEL(jpflux,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 2)) &
      call XABORT('SPOLEAK: INVALID AXIAL FLUX LIST ITEM.')
    call LCMGDL(jpflux,igr,unknown)
    if (any(.not.ieee_is_finite(unknown))) &
      call XABORT('SPOLEAK: NON-FINITE AXIAL FLUX UNKNOWN.')
    do i=1,nreg2d
      do ifloor=1,nfloor
        ireg=(i-1)*nfloor+ifloor
        if (keyflx(ireg) > 0) then
          phi(ifloor,i)=unknown(keyflx(ireg))
        else
          phi(ifloor,i)=0.0
        endif
      enddo
      do iface=1,nfloor+1
        current(iface,i)=unknown(ll4+(i-1)*(nfloor+1)+iface)
      enddo
    enddo
    call SPOLE1(nreg2d,nfloor,nsnap,mat1d,dz,area,phi,current, &
                fresh(igr,:),numerator,denominator)
  enddo

  old=0.0
  jpsnap=LCMGID(kentry(1),'FLUX')
  do isnap=1,nsnap
    kpsnap=LCMGIL(jpsnap,isnap)
    call LCMLEN(kpsnap,'SPOT-LEAK1D',ilong,itylcm)
    if (ilong == 0) then
      cycle
    else if ((ilong /= ngrp).or.(itylcm /= 2)) then
      call XABORT('SPOLEAK: INVALID STORED SPOT-LEAK1D LENGTH.')
    else
      call LCMGET(kpsnap,'SPOT-LEAK1D',old(:,isnap))
    endif
  enddo
  if (any(.not.ieee_is_finite(fresh)) .or. &
      any(.not.ieee_is_finite(old))) &
    call XABORT('SPOLEAK: NON-FINITE LEAKAGE COEFFICIENT.')

  error=maxval(abs(fresh-old))
  do isnap=1,nsnap
    kpsnap=LCMGIL(jpsnap,isnap)
    call LCMPUT(kpsnap,'SPOT-LEAK1D',ngrp,2,fresh(:,isnap))
  enddo
  dkeff=dble(keff)
  call LCMPUT(kentry(1),'SPOT-ITER-K',1,4,dkeff)
  call LCMPUT(kentry(1),'SPOT-L1-ERR',1,2,error)
  write(6,'(A,ES24.16)') 'SPOLEAK ITER K ',dkeff
  write(6,'(A,1P,3E24.16)') 'SPOLEAK DIRECT ERROR/MIN/MAX ',error, &
    minval(fresh),maxval(fresh)

  call REDGET(indic,nitma,flott,text4,dflott)
  if (indic /= -2) call XABORT('SPOLEAK: OUTPUT ERROR EXPECTED.')
  indic=2
  call REDPUT(indic,nitma,error,text4,dflott)
  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOLEAK: ; CHARACTER EXPECTED.')

  deallocate(denominator,numerator,old,fresh,current,phi)
  deallocate(unknown,area,volume,dz,mat1d,keyflx)
end subroutine SPOLEAK

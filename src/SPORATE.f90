!DECK SPORATE
subroutine SPORATE(nentry,hentry,ientry,jentry,kentry)
  ! Print snapshot-floor nu-fission fractions from a converged SPOT flux.
  use GANLIB
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate),imacro(nstate)
  integer :: ngrp,nreg,nunk,nreg2d,nfloor,nsnap,nmix,nfis
  integer :: igr,ireg,ibm,ifis,ifloor,isnap,ilong,itylcm
  integer, allocatable :: mat(:),keyflx(:),mat1d(:)
  real, allocatable :: volume(:),unknown(:),nufis(:)
  real(kind=dp), allocatable :: rate(:)
  real(kind=dp) :: nusigf,total_rate
  character(len=12) :: signature,track_type
  type(c_ptr) :: jpflux,jpmacro,kpmacro

  if (nentry /= 3) call XABORT('SPORATE: THREE READ-ONLY ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2)) .or. any(jentry /= 2)) &
    call XABORT('SPORATE: READ-ONLY LCM ENTRIES EXPECTED.')

  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPORATE: L_FLUX EXPECTED.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPORATE: L_TRACK EXPECTED.')
  call LCMGTC(kentry(2),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') call XABORT('SPORATE: SPOT TRACKING EXPECTED.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_MACROLIB') call XABORT('SPORATE: L_MACROLIB EXPECTED.')

  call LCMGET(kentry(1),'STATE-VECTOR',iflux)
  call LCMGET(kentry(2),'STATE-VECTOR',itrack)
  call LCMGET(kentry(3),'STATE-VECTOR',imacro)
  ngrp=iflux(1)
  nreg=itrack(1)
  nunk=itrack(2)
  nreg2d=itrack(6)
  nfloor=itrack(7)
  nsnap=itrack(8)
  nmix=imacro(2)
  nfis=imacro(4)
  if (ngrp /= imacro(1) .or. nreg /= nreg2d*nfloor) &
    call XABORT('SPORATE: INCONSISTENT FLUX/TRACK/MACROLIB DIMENSIONS.')
  if (nfis <= 0 .or. nsnap <= 0) &
    call XABORT('SPORATE: FISSILE SNAPSHOTS EXPECTED.')

  allocate(mat(nreg),keyflx(nreg),mat1d(nfloor),volume(nreg))
  allocate(unknown(nunk),nufis(nmix*nfis),rate(nsnap))
  call LCMGET(kentry(2),'MATCOD',mat)
  call LCMGET(kentry(2),'KEYFLX',keyflx)
  call LCMGET(kentry(2),'VOLUME',volume)
  call LCMGET(kentry(2),'MAT1D',mat1d)
  rate=0.0_dp
  jpflux=LCMGID(kentry(1),'FLUX')
  jpmacro=LCMGID(kentry(3),'GROUP')

  do igr=1,ngrp
    call LCMGDL(jpflux,igr,unknown)
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'NUSIGF',ilong,itylcm)
    if (ilong == 0) cycle
    if (ilong /= nmix*nfis) call XABORT('SPORATE: INVALID NUSIGF LENGTH.')
    call LCMGET(kpmacro,'NUSIGF',nufis)
    do ireg=1,nreg
      ibm=mat(ireg)
      if (ibm <= 0 .or. keyflx(ireg) <= 0) cycle
      ifloor=mod(ireg-1,nfloor)+1
      isnap=mat1d(ifloor)
      if (isnap < 1 .or. isnap > nsnap) &
        call XABORT('SPORATE: INVALID SNAPSHOT/FLOOR MAP.')
      nusigf=0.0_dp
      do ifis=1,nfis
        nusigf=nusigf+real(nufis((ifis-1)*nmix+ibm),dp)
      enddo
      rate(isnap)=rate(isnap)+real(volume(ireg),dp)* &
        real(unknown(keyflx(ireg)),dp)*nusigf
    enddo
  enddo

  total_rate=0.0_dp
  do isnap=1,nsnap
    total_rate=total_rate+rate(isnap)
  enddo
  if (total_rate <= 0.0_dp) call XABORT('SPORATE: NONPOSITIVE FISSION RATE.')
  write(6,'(A,1P,100E16.8)') 'SPORATE NU-FISSION-FRACTIONS ', &
    (rate(isnap)/total_rate,isnap=1,nsnap)

  deallocate(rate,nufis,unknown,volume,mat1d,keyflx,mat)
end subroutine SPORATE

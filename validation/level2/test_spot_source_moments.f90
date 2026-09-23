! Source-assembly regression, not a transport/eigenvalue accuracy test.
! The actual FLU2DR/FLU2DR64 routines consume small real LCM macrolibs.
! Only the eigenvalue normalizer and transport door are test doubles: the
! latter checks the assembled source, prescribes flux, and stops before any
! transport solve.  Binary-fraction fixtures permit exact equality checks.
module source_moment_probe
  use, intrinsic :: iso_fortran_env, only: real64, error_unit
  implicit none
  logical :: thermal, scalar, spot
  integer :: visits(2)=0
  real(real64), parameter :: initial(3,2)=reshape( &
    [2.0_real64,1.0_real64,0.5_real64, &
     4.0_real64,-0.5_real64,0.25_real64],[3,2])
  character(16) :: precision_name, path_name, spectrum_name, door_name
contains
  subroutine inspect_source(groups, source, output)
    integer, intent(in) :: groups(:)
    real(real64), intent(in) :: source(:,:)
    real(real64), intent(out) :: output(:,:)
    real(real64) :: want(3), multiplier
    integer :: j,g,other
    ! Evaluate all vector-door sources before advancing either prescribed
    ! flux.  A scalar door instead sees the preceding group update.
    do j=1,size(groups)
      g=groups(j)
      other=3-g
      multiplier=1.0_real64
      if (thermal.and.visits(other)>0) multiplier=2.0_real64
      if (g==1) then
        ! Integral P_l(source): upscatter [1/8,1/32,1/64] times
        ! phi_2=[4,-1/2,1/4], with no within-group contribution.
        want=[0.5_real64,-0.015625_real64,0.00390625_real64]
        if (.not.thermal) want=0.0_real64
      else
        ! Downscatter [1/2,1/16,1/32] times phi_1=[2,1,1/2].
        want=[1.0_real64,0.0625_real64,0.015625_real64]
      endif
      want=multiplier*want
      if (.not.spot) want=want*[1.0_real64,3.0_real64,5.0_real64]
      ! nuSigma_f,1=1/2, chi_1=chi_2=1/2, phi_01=2, and
      ! the test normalizer fixes 1/k=1: isotropic outer source is 1/2.
      want(1)=want(1)+0.5_real64
      if (any(source(:,j)/=want)) then
        write(error_unit,'(a,4(1x,a),2(a,i0))') 'FAIL source moments:', &
          trim(precision_name),trim(door_name),trim(path_name), &
          trim(spectrum_name),' group=',g,' visit=',visits(g)+1
        write(error_unit,'(a,3es24.16)') 'actual:  ',source(:,j)
        write(error_unit,'(a,3es24.16)') 'expected:',want
        error stop 1
      endif
    enddo
    do j=1,size(groups)
      g=groups(j)
      visits(g)=visits(g)+1
      output(:,j)=initial(:,g)
      ! Force an actual second thermal iteration, including both groups.
      if (thermal) output(:,j)=2.0_real64*output(:,j)
    enddo
    if (all(visits>=merge(2,1,thermal))) then
      write(*,'(a,4(1x,a),a,2i3)') 'PASS source moments:', &
        trim(precision_name),trim(door_name),trim(path_name), &
        trim(spectrum_name),' visits=',visits
      stop
    endif
  end subroutine inspect_source
end module source_moment_probe

program test_spot_source_moments
  use GANLIB
  use source_moment_probe
  implicit none
  type(c_ptr) :: mac,flux,sys,trk,groups,node,list,unused
  integer :: state(40),g,l,key(1,1,3),mat(1),imerge(1)
  real :: total(0:1,2),self(0:1,0:2,2),nuf(0:1,1,2),chi(0:1,1,2)
  real :: down(3),up(3),compressed(2),volume(1),buf(3)
  character(2) :: suffix
  character(12) :: door
  character(72) :: title
  character(4) :: option
  call get_command_argument(1,precision_name)
  call get_command_argument(2,door_name)
  call get_command_argument(3,path_name)
  call get_command_argument(4,spectrum_name)
  if (precision_name/='32'.and.precision_name/='64') error stop 'bad precision'
  if (door_name/='SPOT'.and.door_name/='MCCG') error stop 'bad door'
  if (path_name/='scalar'.and.path_name/='vector') error stop 'bad path'
  if (spectrum_name/='down'.and.spectrum_name/='thermal') error stop 'bad spectrum'
  spot=door_name=='SPOT'
  scalar=path_name=='scalar'
  thermal=spectrum_name=='thermal'
  if (precision_name=='64'.and..not.spot) error stop '64 SPOT only'
  door=door_name
  title='isolated source moment regression: NO TRANSPORT SOLVER'
  option='B0'
  call LCMOP(mac,'SOURCE-MAC',0,1,0)
  call LCMOP(flux,'SOURCE-FLX',0,1,0)
  call LCMOP(sys,'SOURCE-SYS',0,1,0)
  call LCMOP(trk,'SOURCE-TRK',0,1,0)
  unused=c_null_ptr
  state=0
  if (spot) then
    state(15)=8
    state(16)=3
    state(27)=merge(0,1,scalar)
  else
    state(6)=3
    state(16)=1
    state(22)=merge(0,1,scalar)
  endif
  call LCMPUT(trk,'STATE-VECTOR',40,1,state)
  groups=LCMLID(mac,'GROUP',2)
  down=[0.5,0.0625,0.03125]
  up=[0.125,0.03125,0.015625]
  if (.not.thermal) up=0.0
  do g=1,2
    node=LCMDIL(groups,g)
    do l=0,2
      write(suffix,'(i2.2)') l
      call LCMPUT(node,'NJJS'//suffix,1,1,[2])
      call LCMPUT(node,'IJJS'//suffix,1,1,[2])
      call LCMPUT(node,'IPOS'//suffix,1,1,[1])
      ! Compressed storage is decreasing source-group index: 2, then 1.
      compressed=[up(l+1),0.0]
      if (g==2) compressed=[0.0,down(l+1)]
      call LCMPUT(node,'SCAT'//suffix,2,2,compressed)
    enddo
  enddo
  list=LCMLID(flux,'FLUX',2)
  do g=1,2
    buf=real(initial(:,g))
    call LCMPDL(list,g,3,2,buf)
  enddo
  list=LCMLID(sys,'GROUP',2)
  do g=1,2
    node=LCMDIL(list,g)
    call LCMPUT(node,'TEST-GROUP',1,1,[g])
  enddo
  key(1,1,:)=[1,2,3]
  mat=1
  imerge=1
  volume=1.0
  total=0.0
  total(1,:)=2.0
  self=0.0
  nuf=0.0
  nuf(1,1,1)=0.5
  chi=0.0
  chi(1,1,:)=0.5
  if (precision_name=='64') then
    call FLU2DR64(0,mac,flux,sys,trk,unused,unused, &
      1,0,door,title,3,1,0,2,8,1,3,2,1,1,.true.,.false., &
      3,1.0e-6,1,1.0e-6,1.0e-6,1,0,2,1,1,0,option,1.0_real64, &
      mat,key,volume,total,self,nuf,chi,.false.,1,1,imerge)
  else
    call FLU2DR(0,mac,flux,sys,trk,unused,unused, &
      1,0,door,title,3,1,0,2,8,1,3,2,1,1,.true.,.false., &
      3,1.0e-6,1,1.0e-6,1.0e-6,1,0,2,1,1,0,option,1.0_real64, &
      mat,key,volume,total,self,nuf,chi,.false.,1,1,imerge)
  endif
  error stop 'source probe did not reach all required visits'
end program test_spot_source_moments

! Intercept only the solver dispatch; real source assembly has already run.
subroutine SPOF64(kpsys,iptrk,impx,ngeff,ngind,nreg,nmat,nun,mat,key,fun,sun,title)
  use GANLIB
  use source_moment_probe
  implicit none
  integer :: impx,ngeff,nreg,nmat,nun,ngind(ngeff),mat(nreg),key(nreg)
  type(c_ptr) :: kpsys(ngeff),iptrk
  real(real64) :: fun(nun,ngeff),sun(nun,ngeff)
  character(72) :: title
  if (nun/=3.or.nreg/=1) error stop 'unexpected SPOF64 shape'
  call inspect_source(ngind,sun,fun)
end subroutine SPOF64

subroutine DOORFV(cdoor,ipsys,npsys,iptrk,iftrak,impx,ngrp,nmat, &
                  idir,nreg,nun,iphase,lexac,mat,vol,key,title,sun,fun, &
                  ipmacr,ipsou,rebflg,fluxc,evalrho)
  use GANLIB
  use source_moment_probe
  implicit none
  type(c_ptr) :: ipsys,iptrk,ipmacr,ipsou
  integer :: iftrak,impx,ngrp,nmat,idir,nreg,nun,iphase
  integer :: npsys(ngrp),mat(nreg),key(nreg),indices(ngrp),j,n
  character(12) :: cdoor
  character(72) :: title
  logical :: lexac,rebflg
  real :: vol(nreg),sun(nun,ngrp),fun(nun,ngrp),fluxc(nreg),evalrho
  real(real64) :: captured(3,ngrp),prescribed(3,ngrp)
  if (nun/=3.or.ngrp/=2.or.cdoor/=door_name) error stop 'unexpected DOORFV'
  n=0
  do j=1,ngrp
    if (npsys(j)==0) cycle
    n=n+1
    indices(n)=j
    captured(:,n)=real(sun(:,j),real64)
  enddo
  call inspect_source(indices(:n),captured(:,:n),prescribed(:,:n))
  do j=1,n
    fun(:,indices(j))=real(prescribed(:,j))
  enddo
end subroutine DOORFV

! Fix the scalar outer normalization, independently of the source fixture.
subroutine FLUKEF(iprt,ipmacr,ngrp,nreg,nun,nmat,nifis,nanis, &
                  mat,vol,key,total,self,nuf,chi,nmerge,imerge,difhet, &
                  flux,b2,ileak,leaksw,oldbil,keff,normalizer)
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer :: iprt,ngrp,nreg,nun,nmat,nifis,nanis,nmerge,ileak
  integer :: mat(nreg),key(nreg),imerge(nmat)
  type(c_ptr) :: ipmacr
  real :: vol(nreg),total(0:nmat,ngrp),self(0:nmat,0:nanis,ngrp)
  real :: nuf(0:nmat,nifis,ngrp),chi(0:nmat,nifis,ngrp)
  real :: difhet(nmerge,ngrp),flux(nun,ngrp),b2(4)
  logical :: leaksw
  real(real64) :: oldbil,keff,normalizer
  oldbil=1.0_real64
  keff=1.0_real64
  normalizer=1.0_real64
end subroutine FLUKEF

program check_anderson1_trial_xsm
  ! Independent read-only Ganlib audit of the leakage-Anderson TRIAL pair.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  character(len=1024) :: paths(6)
  type(c_ptr) :: x4,x5,x6,snap6,trial_ax,trial_snap
  type(c_ptr) :: original_fluxes,trial_fluxes,original_systems,trial_systems
  type(c_ptr) :: original_plane,trial_plane,original_system,trial_system
  integer :: i,s,g,index_l,ngrp,nsnap,ncoef
  integer :: dims4(4),dims5(4),dims6(4),dimst(4)
  integer :: rank_count,gram_count,basis_count
  integer, allocatable :: rank6(:),off6(:),goff6(:),boff6(:)
  real(real32) :: keff5,keff6,kefft
  real(real32), allocatable :: expected_l32(:),found_l32(:),original_l32(:)
  real(real64) :: rho5,rho6,rhot,numerator,denominator,gamma,weight6
  real(real64) :: iter_k6,iter_kt
  real(real64), allocatable :: h4(:),h5(:),h6(:)
  real(real64), allocatable :: a5(:),a6(:),at(:)
  real(real64), allocatable :: l4(:),l5(:),l6(:),lt(:),expected_l64(:)
  real(real64) :: f4,f5,delta

  if (command_argument_count() /= 6) error stop &
    'expected x4 AX, x5 AX, x6 AX, x6 snapshots, trial AX, trial snapshots'
  do i=1,6
    call get_command_argument(i,paths(i))
    if (len_trim(paths(i)) == 0.or.len_trim(paths(i)) > 72) &
      error stop 'XSM path is empty or exceeds GANLIB limit'
  enddo
  call LCMOP(x4,trim(paths(1)),2,2,0)
  call LCMOP(x5,trim(paths(2)),2,2,0)
  call LCMOP(x6,trim(paths(3)),2,2,0)
  call LCMOP(snap6,trim(paths(4)),2,2,0)
  call LCMOP(trial_ax,trim(paths(5)),2,2,0)
  call LCMOP(trial_snap,trim(paths(6)),2,2,0)
  call require_character(x4,'SIGNATURE','L_FLUX','x4 AX')
  call require_character(x5,'SIGNATURE','L_FLUX','x5 AX')
  call require_character(x6,'SIGNATURE','L_FLUX','x6 AX')
  call require_character(trial_ax,'SIGNATURE','L_FLUX','trial AX')
  call require_character(snap6,'SIGNATURE','L_ARCHIVE','x6 snapshots')
  call require_character(trial_snap,'SIGNATURE','L_ARCHIVE','trial snapshots')

  call read_integer_record(x4,'SPOT-X-DIMS',4,dims4,'x4 AX')
  call read_integer_record(x5,'SPOT-X-DIMS',4,dims5,'x5 AX')
  call read_integer_record(x6,'SPOT-X-DIMS',4,dims6,'x6 AX')
  call read_integer_record(trial_ax,'SPOT-X-DIMS',4,dimst,'trial AX')
  if (any(dims4 /= dims5).or.any(dims4 /= dims6).or. &
      any(dims4 /= dimst).or.dims4(1) /= 1) &
    error stop 'canonical dimensions differ'
  ngrp=dims4(2)
  nsnap=dims4(3)
  ncoef=dims4(4)
  if (ngrp /= 370.or.nsnap /= 3.or.ncoef <= 0) &
    error stop 'frozen SPOT dimensions differ'

  allocate(h4(nsnap),h5(nsnap),h6(nsnap))
  allocate(a5(ncoef),a6(ncoef),at(ncoef))
  allocate(l4(ngrp*nsnap),l5(ngrp*nsnap),l6(ngrp*nsnap))
  allocate(lt(ngrp*nsnap),expected_l64(ngrp*nsnap))
  allocate(expected_l32(ngrp*nsnap),found_l32(ngrp),original_l32(ngrp))
  call read_real64_record(x4,'SPOT-X-H',h4,'x4 AX')
  call read_real64_record(x5,'SPOT-X-H',h5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-H',h6,'x6 AX')
  call read_real64_record(x5,'SPOT-X-A',a5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-A',a6,'x6 AX')
  call read_real64_record(trial_ax,'SPOT-X-A',at,'trial AX')
  call read_real64_record(x4,'SPOT-X-L',l4,'x4 AX')
  call read_real64_record(x5,'SPOT-X-L',l5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-L',l6,'x6 AX')
  call read_real64_record(trial_ax,'SPOT-X-L',lt,'trial AX')
  if (any(bits64(h4) /= bits64(h5)).or. &
      any(bits64(h4) /= bits64(h6)).or. &
      any(.not.ieee_is_finite(h4)).or.any(h4 <= 0.0_real64)) &
    error stop 'height metric differs or is invalid'

  numerator=0.0_real64
  denominator=0.0_real64
  do s=1,nsnap
    do g=1,ngrp
      index_l=(s-1)*ngrp+g
      f4=l5(index_l)-l4(index_l)
      f5=l6(index_l)-l5(index_l)
      delta=f5-f4
      denominator=denominator+h4(s)*delta**2
      numerator=numerator+h4(s)*delta*f5
    enddo
  enddo
  if ((.not.ieee_is_finite(denominator)).or.denominator <= 0.0_real64) &
    error stop 'leakage Anderson scalar system is invalid'
  gamma=numerator/denominator
  weight6=1.0_real64-gamma
  expected_l32=real(gamma*l5+weight6*l6,real32)
  expected_l64=real(expected_l32,real64)
  if (any(bits64(at) /= bits64(gamma*a5+weight6*a6))) &
    error stop 'trial modal coordinates differ from candidate'
  if (any(bits64(lt) /= bits64(expected_l64))) &
    error stop 'trial canonical leakage differs from publication'

  call require_character(trial_ax,'SPOT-X-STATE','TRIAL','trial AX')
  call require_character(trial_ax,'SPOT-X-CARR','X6-RAW-FLUX','trial AX')
  call require_absent(trial_ax,'SPOT-X-EPOCH','trial AX')
  call require_absent(trial_ax,'SPOT-X-RRHO','trial AX')
  call require_absent(trial_ax,'SPOT-X-RLEAK','trial AX')
  call require_absent(trial_ax,'SPOT-X-DLEAK','trial AX')
  call require_absent(trial_ax,'SPOT-X-RA','trial AX')
  call require_absent(trial_ax,'SPOT-X-PERP','trial AX')

  allocate(rank6(ngrp),off6(ngrp+1),goff6(ngrp+1),boff6(ngrp+1))
  call read_integer_record(x6,'SPOT-X-RANK',ngrp,rank6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-OFF',ngrp+1,off6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-GOFF',ngrp+1,goff6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-BOFF',ngrp+1,boff6,'x6 AX')
  rank_count=size(rank6)
  gram_count=goff6(ngrp+1)
  basis_count=boff6(ngrp+1)
  if (rank_count /= ngrp.or.gram_count <= 0.or.basis_count <= 0) &
    error stop 'fixed-space layout is invalid'
  call compare_integer_record(x5,x6,'SPOT-X-RANK',ngrp)
  call compare_integer_record(x5,x6,'SPOT-X-OFF',ngrp+1)
  call compare_integer_record(x5,x6,'SPOT-X-GOFF',ngrp+1)
  call compare_integer_record(x5,x6,'SPOT-X-BOFF',ngrp+1)
  call compare_real32_record(x5,x6,'SPOT-X-BASIS',basis_count)
  call compare_real64_record(x5,x6,'SPOT-X-GRAM',gram_count)
  call compare_real64_record(x5,x6,'SPOT-X-H',nsnap)
  call compare_real64_record(x5,x6,'SPOT-X-GERR',1)
  call compare_integer_record(x5,x6,'SPOT-X-FIXB',1)
  call compare_character_record(x5,x6,'SPOT-X-NID')
  call compare_character_record(x5,x6,'SPOT-X-BTYP')
  call compare_integer_record(x6,trial_ax,'SPOT-X-RANK',ngrp)
  call compare_integer_record(x6,trial_ax,'SPOT-X-OFF',ngrp+1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-GOFF',ngrp+1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-BOFF',ngrp+1)
  call compare_real32_record(x6,trial_ax,'SPOT-X-BASIS',basis_count)
  call compare_real64_record(x6,trial_ax,'SPOT-X-GRAM',gram_count)
  call compare_real64_record(x6,trial_ax,'SPOT-X-H',nsnap)
  call compare_real64_record(x6,trial_ax,'SPOT-X-NORM',1)
  call compare_real64_record(x6,trial_ax,'SPOT-X-GERR',1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-FIXB',1)
  call compare_character_record(x6,trial_ax,'SPOT-X-NID')
  call compare_character_record(x6,trial_ax,'SPOT-X-BTYP')

  call read_real32_scalar(x5,'K-EFFECTIVE',keff5,'x5 AX')
  call read_real32_scalar(x6,'K-EFFECTIVE',keff6,'x6 AX')
  call read_real32_scalar(trial_ax,'K-EFFECTIVE',kefft,'trial AX')
  call read_real64_scalar(x5,'SPOT-X-RHO',rho5,'x5 AX')
  call read_real64_scalar(x6,'SPOT-X-RHO',rho6,'x6 AX')
  call read_real64_scalar(trial_ax,'SPOT-X-RHO',rhot,'trial AX')
  if (bits32(keff5) /= bits32(keff6).or. &
      bits32(keff6) /= bits32(kefft).or. &
      bits64(rho5) /= bits64(rho6).or. &
      bits64(rho6) /= bits64(rhot).or. &
      bits64(rhot) /= bits64(1.0_real64/real(kefft,real64))) &
    error stop 'trial K-effective/rho identity differs'
  call compare_axial_raw_flux(x6,trial_ax,ngrp)

  call require_absent(trial_snap,'SPOT-R64','trial snapshots')
  call require_absent(trial_snap,'SPOT-L1-ERR','trial snapshots')
  call require_absent(trial_snap,'SPOT-PJ-PERP','trial snapshots')
  call require_absent(trial_snap,'SPOT-PROJECT','trial snapshots')
  call read_real64_scalar(snap6,'SPOT-ITER-K',iter_k6,'x6 snapshots')
  call read_real64_scalar(trial_snap,'SPOT-ITER-K',iter_kt, &
    'trial snapshots')
  if (bits64(iter_k6) /= bits64(iter_kt).or. &
      bits64(iter_kt) /= bits64(real(kefft,real64))) &
    error stop 'trial snapshot K-effective differs'

  original_fluxes=LCMGID(snap6,'FLUX')
  trial_fluxes=LCMGID(trial_snap,'FLUX')
  original_systems=LCMGID(snap6,'SYSTEM')
  trial_systems=LCMGID(trial_snap,'SYSTEM')
  do s=1,nsnap
    original_plane=LCMGIL(original_fluxes,s)
    trial_plane=LCMGIL(trial_fluxes,s)
    original_system=LCMGIL(original_systems,s)
    trial_system=LCMGIL(trial_systems,s)
    call require_absent(trial_plane,'SPOT-R64','trial snapshot FLUX')
    call read_real32_record(original_plane,'SPOT-LEAK1D',original_l32, &
      'x6 snapshot FLUX')
    call read_real32_record(trial_plane,'SPOT-LEAK1D',found_l32, &
      'trial snapshot FLUX')
    if (any(bits64(real(original_l32,real64)) /= &
        bits64(l6((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'x6 snapshot leakage differs from canonical x6 L'
    if (any(bits32(found_l32) /= &
        bits32(expected_l32((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'trial snapshot leakage differs from publication'
    if (any(bits64(real(found_l32,real64)) /= &
        bits64(lt((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'trial snapshot and canonical leakage differ'
    call compare_real32_record(original_system,trial_system, &
      'SPOT-LEAK1D',ngrp)
    call compare_integer_record(original_system,trial_system, &
      'SPOT-L1-SNAP',1)
    call compare_plane_raw_flux(original_plane,trial_plane,ngrp)
  enddo

  call LCMCL(trial_snap,1)
  call LCMCL(trial_ax,1)
  call LCMCL(snap6,1)
  call LCMCL(x6,1)
  call LCMCL(x5,1)
  call LCMCL(x4,1)
  write(*,'(A)') 'ANDERSON1-TRIAL FIXED-BUNDLE BITWISE PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL A/RHO/L PUBLICATION BITWISE PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL X6 RAW-FLUX CARRIER BITWISE PASS'
  write(*,'(A)') &
    'ANDERSON1-TRIAL LAGGED SYSTEM LEAKAGE RECORDS PRESERVED PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL STALE-DIAGNOSTICS ABSENT PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL COMPLETE NO-DRAGON NO-MAP'

contains

  subroutine require_record(object,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= length_expected.or.type_found /= type_expected) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'required GANLIB record differs'
    endif
  end subroutine require_record

  subroutine require_absent(object,name,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'GANLIB record must be absent'
    endif
  end subroutine require_absent

  subroutine require_character(object,name,expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found
    call require_record(object,name,3,3,owner)
    call LCMGTC(object,name,12,found)
    if (found /= expected) error stop 'required character record differs'
  end subroutine require_character

  subroutine read_integer_record(object,name,n,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: n
    integer, intent(out) :: value(n)
    call require_record(object,name,n,1,owner)
    call LCMGET(object,name,value)
  end subroutine read_integer_record

  subroutine read_real32_record(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real32), intent(out) :: value(:)
    call require_record(object,name,size(value),2,owner)
    call LCMGET(object,name,value)
    if (any(.not.ieee_is_finite(value))) error stop 'nonfinite real32 record'
  end subroutine read_real32_record

  subroutine read_real64_record(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real64), intent(out) :: value(:)
    call require_record(object,name,size(value),4,owner)
    call LCMGET(object,name,value)
    if (any(.not.ieee_is_finite(value))) error stop 'nonfinite real64 record'
  end subroutine read_real64_record

  subroutine read_real32_scalar(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real32), intent(out) :: value
    call require_record(object,name,1,2,owner)
    call LCMGET(object,name,value)
    if (.not.ieee_is_finite(value)) error stop 'nonfinite real32 scalar'
  end subroutine read_real32_scalar

  subroutine read_real64_scalar(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real64), intent(out) :: value
    call require_record(object,name,1,4,owner)
    call LCMGET(object,name,value)
    if (.not.ieee_is_finite(value)) error stop 'nonfinite real64 scalar'
  end subroutine read_real64_scalar

  subroutine compare_integer_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    integer, allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_integer_record(left,name,n,lv,'comparison left')
    call read_integer_record(right,name,n,rv,'comparison right')
    if (any(lv /= rv)) error stop 'integer records differ'
    deallocate(rv,lv)
  end subroutine compare_integer_record

  subroutine compare_real32_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    real(real32), allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_real32_record(left,name,lv,'comparison left')
    call read_real32_record(right,name,rv,'comparison right')
    if (any(bits32(lv) /= bits32(rv))) error stop 'real32 records differ'
    deallocate(rv,lv)
  end subroutine compare_real32_record

  subroutine compare_real64_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    real(real64), allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_real64_record(left,name,lv,'comparison left')
    call read_real64_record(right,name,rv,'comparison right')
    if (any(bits64(lv) /= bits64(rv))) error stop 'real64 records differ'
    deallocate(rv,lv)
  end subroutine compare_real64_record

  subroutine compare_character_record(left,right,name)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    character(len=12) :: lv,rv
    call require_record(left,name,3,3,'comparison left')
    call require_record(right,name,3,3,'comparison right')
    call LCMGTC(left,name,12,lv)
    call LCMGTC(right,name,12,rv)
    if (lv /= rv) error stop 'character records differ'
  end subroutine compare_character_record

  subroutine compare_axial_raw_flux(left,right,groups)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: groups
    type(c_ptr) :: left_flux,right_flux
    integer :: ig,nleft,nright,tleft,tright
    real(real32), allocatable :: lv(:),rv(:)
    left_flux=LCMGID(left,'FLUX')
    right_flux=LCMGID(right,'FLUX')
    do ig=1,groups
      call LCMLEL(left_flux,ig,nleft,tleft)
      call LCMLEL(right_flux,ig,nright,tright)
      if (nleft <= 0.or.nleft /= nright.or.tleft /= 2.or.tright /= 2) &
        error stop 'axial raw FLUX layout differs'
      allocate(lv(nleft),rv(nright))
      call LCMGDL(left_flux,ig,lv)
      call LCMGDL(right_flux,ig,rv)
      if (any(bits32(lv) /= bits32(rv))) &
        error stop 'axial raw FLUX carrier differs'
      deallocate(rv,lv)
    enddo
  end subroutine compare_axial_raw_flux

  subroutine compare_plane_raw_flux(left,right,groups)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: groups
    type(c_ptr) :: left_flux,right_flux
    integer :: ig,nleft,nright,tleft,tright
    real(real32), allocatable :: lv(:),rv(:)
    left_flux=LCMGID(left,'FLUX')
    right_flux=LCMGID(right,'FLUX')
    do ig=1,groups
      call LCMLEL(left_flux,ig,nleft,tleft)
      call LCMLEL(right_flux,ig,nright,tright)
      if (nleft <= 0.or.nleft /= nright.or.tleft /= 2.or.tright /= 2) &
        error stop 'plane raw FLUX layout differs'
      allocate(lv(nleft),rv(nright))
      call LCMGDL(left_flux,ig,lv)
      call LCMGDL(right_flux,ig,rv)
      if (any(bits32(lv) /= bits32(rv))) &
        error stop 'plane raw FLUX carrier differs'
      deallocate(rv,lv)
    enddo
  end subroutine compare_plane_raw_flux

  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32

  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64

end program check_anderson1_trial_xsm

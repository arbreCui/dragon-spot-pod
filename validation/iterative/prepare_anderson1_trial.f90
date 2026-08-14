program prepare_anderson1_trial
  ! Build the single preselected leakage-Anderson trial without Dragon.
  ! The copied axial FLUX is an explicitly labelled x6 carrier only.  The
  ! complete map state consumed by the fixed-space continuation is (A,rho,L).
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  character(len=1024) :: x4_path,x5_path,x6_path,snap6_path
  character(len=1024) :: trial_ax_path,trial_snap_path
  character(len=12) :: marker
  type(c_ptr) :: x4,x5,x6,snap6,trial_ax,trial_snap
  type(c_ptr) :: fluxes,plane
  integer :: dims4(4),dims5(4),dims6(4)
  integer :: ngrp,nsnap,ncoef,s,g,index_l
  real(real32) :: keff5,keff6
  real(real64) :: rho5,rho6,numerator,denominator,gamma,weight6
  real(real64), allocatable :: h4(:),h5(:),h6(:)
  real(real64), allocatable :: a5(:),a6(:),candidate_a(:)
  real(real64), allocatable :: l4(:),l5(:),l6(:),candidate_l(:)
  real(real32), allocatable :: published_l(:)
  real(real64) :: f4,f5,delta,roundtrip_max,iter_keff

  if (command_argument_count() /= 6) error stop &
    'expected x4 AX, x5 AX, x6 AX, x6 snapshots, trial AX, trial snapshots'
  call get_command_argument(1,x4_path)
  call get_command_argument(2,x5_path)
  call get_command_argument(3,x6_path)
  call get_command_argument(4,snap6_path)
  call get_command_argument(5,trial_ax_path)
  call get_command_argument(6,trial_snap_path)
  call require_fresh_path(trial_ax_path)
  call require_fresh_path(trial_snap_path)

  call LCMOP(x4,trim(x4_path),2,2,0)
  call LCMOP(x5,trim(x5_path),2,2,0)
  call LCMOP(x6,trim(x6_path),2,2,0)
  call LCMOP(snap6,trim(snap6_path),2,2,0)
  call require_character(x4,'SIGNATURE','L_FLUX','x4 AX')
  call require_character(x5,'SIGNATURE','L_FLUX','x5 AX')
  call require_character(x6,'SIGNATURE','L_FLUX','x6 AX')
  call require_character(snap6,'SIGNATURE','L_ARCHIVE','x6 snapshots')
  call require_absent(x6,'SPOT-X-STATE','x6 AX')
  call require_absent(x6,'SPOT-X-EPOCH','x6 AX')
  call require_absent(snap6,'SPOT-R64','x6 snapshots')

  call require_record(x4,'SPOT-X-DIMS',4,1,'x4 AX')
  call require_record(x5,'SPOT-X-DIMS',4,1,'x5 AX')
  call require_record(x6,'SPOT-X-DIMS',4,1,'x6 AX')
  call LCMGET(x4,'SPOT-X-DIMS',dims4)
  call LCMGET(x5,'SPOT-X-DIMS',dims5)
  call LCMGET(x6,'SPOT-X-DIMS',dims6)
  if (any(dims4 /= dims5).or.any(dims4 /= dims6).or. &
      dims4(1) /= 1.or.any(dims4(2:4) <= 0)) &
    error stop 'canonical dimensions differ'
  ngrp=dims4(2)
  nsnap=dims4(3)
  ncoef=dims4(4)
  if (ngrp /= 370.or.nsnap /= 3) &
    error stop 'frozen SPOT dimensions differ'

  allocate(h4(nsnap),h5(nsnap),h6(nsnap))
  allocate(a5(ncoef),a6(ncoef),candidate_a(ncoef))
  allocate(l4(ngrp*nsnap),l5(ngrp*nsnap),l6(ngrp*nsnap))
  allocate(candidate_l(ngrp*nsnap),published_l(ngrp*nsnap))
  call require_record(x4,'SPOT-X-H',nsnap,4,'x4 AX')
  call require_record(x5,'SPOT-X-H',nsnap,4,'x5 AX')
  call require_record(x6,'SPOT-X-H',nsnap,4,'x6 AX')
  call require_record(x5,'SPOT-X-A',ncoef,4,'x5 AX')
  call require_record(x6,'SPOT-X-A',ncoef,4,'x6 AX')
  call require_record(x4,'SPOT-X-L',ngrp*nsnap,4,'x4 AX')
  call require_record(x5,'SPOT-X-L',ngrp*nsnap,4,'x5 AX')
  call require_record(x6,'SPOT-X-L',ngrp*nsnap,4,'x6 AX')
  call LCMGET(x4,'SPOT-X-H',h4)
  call LCMGET(x5,'SPOT-X-H',h5)
  call LCMGET(x6,'SPOT-X-H',h6)
  call LCMGET(x5,'SPOT-X-A',a5)
  call LCMGET(x6,'SPOT-X-A',a6)
  call LCMGET(x4,'SPOT-X-L',l4)
  call LCMGET(x5,'SPOT-X-L',l5)
  call LCMGET(x6,'SPOT-X-L',l6)
  if (any(bits64(h4) /= bits64(h5)).or. &
      any(bits64(h4) /= bits64(h6)).or. &
      any(.not.ieee_is_finite(h4)).or.any(h4 <= 0.0_real64)) &
    error stop 'height metric differs or is invalid'
  call compare_record_bits(x5,x6,'SPOT-X-RANK',1)
  call compare_record_bits(x5,x6,'SPOT-X-OFF',1)
  call compare_record_bits(x5,x6,'SPOT-X-GOFF',1)
  call compare_record_bits(x5,x6,'SPOT-X-BOFF',1)
  call compare_record_bits(x5,x6,'SPOT-X-BASIS',2)
  call compare_record_bits(x5,x6,'SPOT-X-GRAM',4)
  call compare_record_bits(x5,x6,'SPOT-X-H',4)
  call compare_record_bits(x5,x6,'SPOT-X-GERR',4)
  call compare_record_bits(x5,x6,'SPOT-X-FIXB',1)
  call compare_record_bits(x5,x6,'SPOT-X-NID',3)
  call compare_record_bits(x5,x6,'SPOT-X-BTYP',3)
  if (any(.not.ieee_is_finite(a5)).or. &
      any(.not.ieee_is_finite(a6)).or. &
      any(.not.ieee_is_finite(l4)).or. &
      any(.not.ieee_is_finite(l5)).or. &
      any(.not.ieee_is_finite(l6))) &
    error stop 'nonfinite Anderson input'
  if (any(bits64(l4) /= bits64(real(real(l4,real32),real64))).or. &
      any(bits64(l5) /= bits64(real(real(l5,real32),real64))).or. &
      any(bits64(l6) /= bits64(real(real(l6,real32),real64)))) &
    error stop 'canonical input leakage is not promoted binary32'

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
  if ((.not.ieee_is_finite(denominator)).or.denominator <= 0.0_real64.or. &
      (.not.ieee_is_finite(numerator))) &
    error stop 'leakage Anderson scalar system is invalid'
  gamma=numerator/denominator
  weight6=1.0_real64-gamma
  if ((.not.ieee_is_finite(gamma)).or.gamma < 0.0_real64.or. &
      gamma > 1.0_real64) error stop 'leakage Anderson weight is not convex'
  candidate_a=gamma*a5+weight6*a6
  candidate_l=gamma*l5+weight6*l6
  published_l=real(candidate_l,real32)
  roundtrip_max=maxval(abs(real(published_l,real64)-candidate_l))
  if (any(.not.ieee_is_finite(candidate_a)).or. &
      any(.not.ieee_is_finite(published_l)).or. &
      (.not.ieee_is_finite(roundtrip_max))) &
    error stop 'candidate publication is nonfinite'

  call require_record(x5,'K-EFFECTIVE',1,2,'x5 AX')
  call require_record(x6,'K-EFFECTIVE',1,2,'x6 AX')
  call require_record(x5,'SPOT-X-RHO',1,4,'x5 AX')
  call require_record(x6,'SPOT-X-RHO',1,4,'x6 AX')
  call LCMGET(x5,'K-EFFECTIVE',keff5)
  call LCMGET(x6,'K-EFFECTIVE',keff6)
  call LCMGET(x5,'SPOT-X-RHO',rho5)
  call LCMGET(x6,'SPOT-X-RHO',rho6)
  if (bits32(keff5) /= bits32(keff6).or. &
      bits64(rho5) /= bits64(rho6).or. &
      bits64(rho6) /= bits64(1.0_real64/real(keff6,real64))) &
    error stop 'x5/x6 K-effective and rho identity differs'

  call LCMOP(trial_ax,trim(trial_ax_path),0,2,0)
  call LCMEQU(x6,trial_ax)
  call LCMPUT(trial_ax,'SPOT-X-A',ncoef,4,candidate_a)
  call LCMPUT(trial_ax,'SPOT-X-L',ngrp*nsnap,4, &
    real(published_l,real64))
  call LCMPUT(trial_ax,'SPOT-X-RHO',1,4,rho6)
  call delete_if_present(trial_ax,'SPOT-X-RRHO')
  call delete_if_present(trial_ax,'SPOT-X-RLEAK')
  call delete_if_present(trial_ax,'SPOT-X-DLEAK')
  call delete_if_present(trial_ax,'SPOT-X-RA')
  call delete_if_present(trial_ax,'SPOT-X-PERP')
  call delete_if_present(trial_ax,'SPOT-X-EPOCH')
  marker='TRIAL'
  call LCMPTC(trial_ax,'SPOT-X-STATE',12,marker)
  marker='X6-RAW-FLUX'
  call LCMPTC(trial_ax,'SPOT-X-CARR',12,marker)

  call require_record(snap6,'LISTDIM',1,1,'x6 snapshots')
  call LCMGET(snap6,'LISTDIM',s)
  if (s /= nsnap) error stop 'snapshot count differs'
  call require_record(snap6,'SPOT-ITER-K',1,4,'x6 snapshots')
  call LCMGET(snap6,'SPOT-ITER-K',iter_keff)
  if (bits64(iter_keff) /= bits64(real(keff6,real64))) &
    error stop 'snapshot K-effective differs from axial state'
  call LCMOP(trial_snap,trim(trial_snap_path),0,2,0)
  call LCMEQU(snap6,trial_snap)
  call delete_if_present(trial_snap,'SPOT-L1-ERR')
  call delete_if_present(trial_snap,'SPOT-PJ-PERP')
  call delete_if_present(trial_snap,'SPOT-PROJECT')
  fluxes=LCMGID(trial_snap,'FLUX')
  do s=1,nsnap
    plane=LCMGIL(fluxes,s)
    call require_absent(plane,'SPOT-R64','x6 snapshot FLUX')
    call LCMPUT(plane,'SPOT-LEAK1D',ngrp,2, &
      published_l((s-1)*ngrp+1:s*ngrp))
  enddo

  call LCMCL(trial_snap,1)
  call LCMCL(trial_ax,1)
  call LCMCL(snap6,1)
  call LCMCL(x6,1)
  call LCMCL(x5,1)
  call LCMCL(x4,1)

  write(*,'(A,ES24.16)') 'ANDERSON1-TRIAL GAMMA ',gamma
  write(*,'(A,ES24.16)') 'ANDERSON1-TRIAL WEIGHT-X6 ',weight6
  write(*,'(A,ES24.16)') &
    'ANDERSON1-TRIAL L-PUBLICATION-MAX ',roundtrip_max
  write(*,'(A)') 'ANDERSON1-TRIAL AX=TRIAL CARRIER=X6-RAW-FLUX'
  write(*,'(A)') 'ANDERSON1-TRIAL SNAPSHOT-L PUBLISHED'
  write(*,'(A)') 'ANDERSON1-TRIAL NO-DRAGON NO-MAP'

contains

  subroutine require_fresh_path(path)
    character(len=*), intent(in) :: path
    logical :: exists
    if (len_trim(path) == 0.or.len_trim(path) > 72) &
      error stop 'output XSM path is empty or exceeds GANLIB limit'
    inquire(file=trim(path),exist=exists)
    if (exists) error stop 'output XSM path already exists'
  end subroutine require_fresh_path

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

  subroutine require_character(object,name,expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found
    call require_record(object,name,3,3,owner)
    call LCMGTC(object,name,12,found)
    if (found /= expected) error stop 'required character record differs'
  end subroutine require_character

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

  subroutine delete_if_present(object,name)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) call LCMDEL(object,name)
  end subroutine delete_if_present

  subroutine compare_record_bits(left,right,name,type_expected)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: type_expected
    integer :: nleft,nright,tleft,tright
    integer, allocatable :: ileft(:),iright(:)
    real(real32), allocatable :: rleft(:),rright(:)
    real(real64), allocatable :: dleft(:),dright(:)
    character(len=72) :: cleft,cright
    call LCMLEN(left,name,nleft,tleft)
    call LCMLEN(right,name,nright,tright)
    if (nleft <= 0.or.nleft /= nright.or. &
        tleft /= type_expected.or.tright /= type_expected) &
      error stop 'fixed POD record layout differs'
    select case(type_expected)
    case(1)
      allocate(ileft(nleft),iright(nright))
      call LCMGET(left,name,ileft)
      call LCMGET(right,name,iright)
      if (any(ileft /= iright)) error stop 'fixed POD integer bits differ'
      deallocate(iright,ileft)
    case(2)
      allocate(rleft(nleft),rright(nright))
      call LCMGET(left,name,rleft)
      call LCMGET(right,name,rright)
      if (any(bits32(rleft) /= bits32(rright))) &
        error stop 'fixed POD real32 bits differ'
      deallocate(rright,rleft)
    case(3)
      if (4*nleft > len(cleft)) error stop 'fixed POD character is too long'
      call LCMGTC(left,name,4*nleft,cleft)
      call LCMGTC(right,name,4*nright,cright)
      if (cleft(:4*nleft) /= cright(:4*nright)) &
        error stop 'fixed POD character bits differ'
    case(4)
      allocate(dleft(nleft),dright(nright))
      call LCMGET(left,name,dleft)
      call LCMGET(right,name,dright)
      if (any(bits64(dleft) /= bits64(dright))) &
        error stop 'fixed POD real64 bits differ'
      deallocate(dright,dleft)
    case default
      error stop 'unsupported fixed POD record type'
    end select
  end subroutine compare_record_bits

  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32

  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64

end program prepare_anderson1_trial

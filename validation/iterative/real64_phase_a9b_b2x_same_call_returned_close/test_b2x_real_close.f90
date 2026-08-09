program TEST_B2X_REAL_CLOSE
  use GANLIB
  use B2W_FIXTURE_SUPPORT
  use B2X_REAL_PARSER_PROBES
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  implicit none

  interface
    subroutine SPOR64V(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOR64V
    subroutine SPOLEAK(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOLEAK
    subroutine SPOR64X(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOR64X
  end interface

  character(len=1024) :: ax_path, feedback_path, axout_path, archive_path
  character(len=12) :: admit_hentry(1), leak_hentry(3)
  character(len=12) :: close_hentry(4), state
  integer :: admit_ientry(1), admit_jentry(1), ilong, itylcm
  integer :: leak_ientry(3), leak_jentry(3)
  integer :: close_ientry(4), close_jentry(4), epoch
  real(real64) :: bad_k
  real(real32) :: before_l0(NGRP), after_l0(NGRP)
  type(c_ptr) :: admit_kentry(1), leak_kentry(3), close_kentry(4)
  type(c_ptr) :: ax, feedback, axtrack, bad_feedback, bad_l0_feedback
  type(c_ptr) :: fluxes, child
  type(c_ptr) :: rejected_ax, rejected_archive, axout, archiveout, authority

  if (command_argument_count() /= 4) error stop &
      'expected AX, feedback, closed AX, and closed archive paths'
  call get_command_argument(1,ax_path)
  call get_command_argument(2,feedback_path)
  call get_command_argument(3,axout_path)
  call get_command_argument(4,archive_path)
  call REQUIRE_FRESH_PATH(ax_path)
  call REQUIRE_FRESH_PATH(feedback_path)
  call REQUIRE_FRESH_PATH(axout_path)
  call REQUIRE_FRESH_PATH(archive_path)

  call BUILD_AX(ax)
  call BUILD_AX_TRACK(axtrack)
  call BUILD_FEEDBACK_BEFORE_SPOLEAK(feedback)

  admit_hentry=[character(len=12) :: 'FEEDBACK']
  admit_ientry=[1]
  admit_jentry=[2]
  call B2X_RESET_FULL_PARSER()

  ! A child/SYSTEM L0 mismatch is rejected by the read-only admission before
  ! any downstream object exists.  The mismatch itself remains bit-identical
  ! after the call and no SPOLEAK root records are introduced.
  call CLONE_ROOT(feedback,'B2X-BAD-L0',bad_l0_feedback)
  fluxes=LCMGID(bad_l0_feedback,'FLUX')
  child=LCMGIL(fluxes,2)
  call LCMGET(child,'SPOT-LEAK1D',before_l0)
  before_l0(17)=nearest(before_l0(17),+1.0)
  call LCMPUT(child,'SPOT-LEAK1D',NGRP,2,before_l0)
  admit_kentry=[bad_l0_feedback]
  call B2X_START_ADAPTER_PARSE(.true.)
  call SPOR64V(1,admit_hentry,admit_ientry,admit_jentry,admit_kentry)
  if (xabort_calls /= 1 .or. trim(last_abort) /= &
      'SPOR64V: RETURNED ADMISSION FAILED.') &
    error stop 'B2X L0 mismatch was not rejected'
  call LCMGET(child,'SPOT-LEAK1D',after_l0)
  if (any(BITS32(before_l0) /= BITS32(after_l0))) &
    error stop 'B2X returned admission mutated child L0'
  call LCMLEN(bad_l0_feedback,'SPOT-ITER-K',ilong,itylcm)
  if (ilong /= 0 .or. itylcm /= 99) &
    error stop 'B2X returned rejection introduced SPOT-ITER-K'
  call LCMCL(bad_l0_feedback,2)

  admit_kentry=[feedback]
  call B2X_START_ADAPTER_PARSE(.false.)
  call SPOR64V(1,admit_hentry,admit_ientry,admit_jentry,admit_kentry)
  if (xabort_calls /= 0) error stop 'B2X canonical returned admission aborted'

  leak_hentry=[character(len=12) :: 'FEEDBACK','AX_NEXT','TRACK_AX']
  leak_ientry=[1,1,1]
  leak_jentry=[1,2,2]
  leak_kentry=[feedback,ax,axtrack]
  call B2X_START_SPOLEAK_PARSE()
  call SPOLEAK(3,leak_hentry,leak_ientry,leak_jentry,leak_kentry)
  if (total_redget_calls /= 4 .or. total_redput_calls /= 1) &
    error stop 'B2X real SPOLEAK parser inventory differs'
  if (returned_error_bits /= transfer(0.5_real32,0_int32)) &
    error stop 'B2X real SPOLEAK error bits differ'
  call VERIFY_AX_INPUT(ax)
  call VERIFY_FEEDBACK_INPUT(feedback)

  close_hentry=[character(len=12) :: &
      'AX_CLOSED','ARCH_CLOSED','AX_NEXT','FEEDBACK']
  close_ientry=[1,1,1,1]
  close_jentry=[0,0,2,2]

  ! One content rejection proves that the production adapter propagates a
  ! B2W failure without writing either fresh target.
  call CLONE_ROOT(feedback,'B2X-BAD-K',bad_feedback)
  call LCMGET(bad_feedback,'SPOT-ITER-K',bad_k)
  bad_k=nearest(bad_k,+1.0_real64)
  call LCMPUT(bad_feedback,'SPOT-ITER-K',1,4,bad_k)
  call OPEN_FRESH('B2X-REJECT-AX',rejected_ax)
  call OPEN_FRESH('B2X-REJECT-ARCH',rejected_archive)
  close_kentry=[rejected_ax,rejected_archive,ax,bad_feedback]
  call B2X_START_ADAPTER_PARSE(.true.)
  call SPOR64X(4,close_hentry,close_ientry,close_jentry,close_kentry)
  if (xabort_calls /= 1 .or. trim(last_abort) /= &
      'SPOR64X: B2W RETURNED-CLOSE ADMISSION FAILED.') &
    error stop 'B2X real rejection was not propagated'
  if (.not. EMPTY_ROOT(rejected_ax) .or. &
      .not. EMPTY_ROOT(rejected_archive)) &
    error stop 'B2X real rejection wrote an output'
  call LCMCL(rejected_archive,2)
  call LCMCL(rejected_ax,2)
  call LCMCL(bad_feedback,2)

  call OPEN_FRESH('B2X-CLOSED-AX',axout)
  call OPEN_FRESH('B2X-CLOSED-ARCH',archiveout)
  close_kentry=[axout,archiveout,ax,feedback]
  call B2X_START_ADAPTER_PARSE(.false.)
  call SPOR64X(4,close_hentry,close_ientry,close_jentry,close_kentry)
  if (xabort_calls /= 0) error stop 'B2X canonical close aborted'
  if (total_redget_calls /= 6 .or. total_redput_calls /= 1) &
    error stop 'B2X complete parser inventory differs'

  call LCMGTC(axout,'SPOT-X-STATE',12,state)
  if (state /= 'CLOSED') error stop 'B2X AX state differs'
  call LCMGET(axout,'SPOT-X-EPOCH',epoch)
  if (epoch /= 1) error stop 'B2X AX epoch differs'
  authority=LCMGID(archiveout,'SPOT-R64')
  call LCMGTC(authority,'STATE',12,state)
  if (state /= 'CLOSED') error stop 'B2X archive state differs'
  call LCMGET(authority,'EPOCH',epoch)
  if (epoch /= 1) error stop 'B2X archive epoch differs'
  call VERIFY_AX_INPUT(ax)
  call VERIFY_FEEDBACK_INPUT(feedback)

  call WRITE_XSM(ax,ax_path)
  call WRITE_XSM(feedback,feedback_path)
  call WRITE_XSM(axout,axout_path)
  call WRITE_XSM(archiveout,archive_path)

  call LCMCL(archiveout,2)
  call LCMCL(axout,2)
  call LCMCL(axtrack,2)
  call LCMCL(feedback,2)
  call LCMCL(ax,2)

  write(*,'(A)') 'B2X REAL-SPOLEAK-B2W-SPOR64X SYNTHETIC PASS'
  write(*,'(A)') 'B2X REAL-RETURNED-ADMISSION SUCCESS=1 L0-REJECTION=1'
  write(*,'(A)') 'B2X REAL-CALLS=SPOLEAK:1,B2W:2,SPOR64X:2'
  write(*,'(A)') 'B2X CLOSES=1 REJECTIONS=1 ZERO-WRITE=1'
  write(*,'(A)') 'B2X AX=CLOSED/1 ARCHIVE=CLOSED/1 L1ERR=DROPPED'
  write(*,'(A)') 'B2X ASM=0 FLU=0 SPOSTATE=0 DRAGON=0 TRANSPORT=0 PICARD=0'

contains

  subroutine REQUIRE_FRESH_PATH(path)
    character(len=*), intent(in) :: path
    logical :: exists
    inquire(file=trim(path),exist=exists)
    if (exists) error stop 'B2X evidence path is not fresh'
  end subroutine REQUIRE_FRESH_PATH


  subroutine WRITE_XSM(source,path)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: path
    type(c_ptr) :: target

    call LCMOP(target,trim(path),0,2,0)
    if (.not. c_associated(target)) error stop 'B2X XSM create failed'
    call LCMEQU(source,target)
    call LCMCL(target,1)
  end subroutine WRITE_XSM

end program TEST_B2X_REAL_CLOSE

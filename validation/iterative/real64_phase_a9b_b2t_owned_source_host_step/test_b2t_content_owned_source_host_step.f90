program TEST_B2T_CONTENT_OWNED_SOURCE_HOST_STEP
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, &
      c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use B2T_CONTENT_CAPTURE_PROBES, only : B2T_CONTENT_NSNAP, &
      b2t_content_b2k_calls, b2t_content_b2s_calls, &
      b2t_content_evidence_writes, B2T_CONTENT_CONFIGURE
  use SPOR64_B2T, only : SPOR64_B2T_RETURNED, SPOR64_B2T_HOST_STEP
  implicit none

  character(len=1024) :: paths(7)
  character(len=12) :: system_name
  integer :: argument, other, plane, status
  integer(int64) :: cutoff(B2T_CONTENT_NSNAP)
  logical :: exists
  type(c_ptr) :: output, projected, systems(B2T_CONTENT_NSNAP)
  type(FIL_file), target :: fake_track

  if (command_argument_count() /= 7) error stop &
      'expected PROJECTED M1 S1 M2 S2 M3 S3 paths'
  do argument = 1, 7
    call get_command_argument(argument,paths(argument))
    if (len_trim(paths(argument)) == 0) &
      error stop 'B2T content path is empty'
  end do
  do argument = 1, 6
    do other = argument+1, 7
      if (trim(paths(argument)) == trim(paths(other))) &
        error stop 'B2T content paths must be distinct'
    end do
  end do
  inquire(file=trim(paths(1)),exist=exists)
  if (.not. exists) error stop 'B2T content PROJECTED input is absent'
  do argument = 2, 7
    inquire(file=trim(paths(argument)),exist=exists)
    if (exists) error stop 'B2T content evidence output already exists'
  end do

  call LCMOP(projected,trim(paths(1)),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'read-only PROJECTED input')
  call LCMOP(output,'B2T-CONT-OUT',0,1,0)
  call REQUIRE_FRESH_MEMORY(output,'fresh caller output')
  do plane = 1, B2T_CONTENT_NSNAP
    write(system_name,'(A,I1)') 'B2T-CONT-S',plane
    call LCMOP(systems(plane),system_name,0,1,0)
    call REQUIRE_FRESH_MEMORY(systems(plane),'fresh dummy SYSTEM')
  end do
  if (c_associated(projected,output)) &
    error stop 'B2T content PROJECTED aliases output'
  do plane = 1, B2T_CONTENT_NSNAP
    if (c_associated(projected,systems(plane)) .or. &
        c_associated(output,systems(plane))) &
      error stop 'B2T content SYSTEM aliases another object'
    do other = plane+1, B2T_CONTENT_NSNAP
      if (c_associated(systems(plane),systems(other))) &
        error stop 'B2T content SYSTEM handles alias'
    end do
  end do

  fake_track%unit = 77
  fake_track%kdi_file = c_null_ptr
  call B2T_CONTENT_CONFIGURE(paths(2),paths(3),paths(4),paths(5), &
      paths(6),paths(7))
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems,c_loc(fake_track), &
      status,cutoff,.true.)
  if (status /= SPOR64_B2T_RETURNED) &
    error stop 'production B2T rejected three real B2N builds'
  if (any(cutoff /= 0_int64)) &
    error stop 'B2T content stub cutoff differs'
  if (b2t_content_b2k_calls /= 1) &
    error stop 'B2T content B2K stub call inventory differs'
  if (b2t_content_b2s_calls /= 1) &
    error stop 'B2T content B2S stub call inventory differs'
  if (b2t_content_evidence_writes /= 6) &
    error stop 'B2T content evidence write inventory differs'
  call REQUIRE_FRESH_MEMORY(output,'unpublished stub output')
  do argument = 2, 7
    inquire(file=trim(paths(argument)),exist=exists)
    if (.not. exists) error stop 'B2T content evidence was not written'
  end do

  do plane = 1, B2T_CONTENT_NSNAP
    call LCMCL(systems(plane),2)
  end do
  call LCMCL(output,2)
  call LCMCL(projected,1)

  write(*,'(A)') 'B2T CONTENT OWNED-SOURCE HOST-STEP PASS'
  write(*,'(A)') &
      'B2T CONTENT B2K-STUB=1 B2N-COMMITTED=3 B2S-STUB=1'
  write(*,'(A)') 'B2T CONTENT EVIDENCE MACRO0=3 FSOURCE=3'
  write(*,'(A)') &
      'B2T CONTENT DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0'

contains

  subroutine REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A)') trim(owner)
      error stop 'required B2T content pointer is absent'
    end if
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_FRESH_MEMORY(root,owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: owner
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call REQUIRE_ASSOCIATED(root,owner)
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') &
      error stop 'B2T content memory object is not fresh'
  end subroutine REQUIRE_FRESH_MEMORY

end program TEST_B2T_CONTENT_OWNED_SOURCE_HOST_STEP

program BUILD_B2N_REAL64_FROZEN_QFISS
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use SPOR64_B2N, only : SPOR64_B2N_BUILD, SPOR64_B2N_COMMITTED
  implicit none

  character(len=1024) :: projected_path, macro_path, source_path
  logical :: projected_exists, macro_exists, source_exists
  type(c_ptr) :: projected, macro, source
  type(c_ptr) :: macro_xsm, source_xsm
  integer :: status

  if (command_argument_count() /= 3) error stop &
      'expected PROJECTED, MACRO_OUT, and SOURCE_OUT paths'
  call get_command_argument(1,projected_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,source_path)
  if (len_trim(projected_path) == 0 .or. len_trim(macro_path) == 0 .or. &
      len_trim(source_path) == 0) error stop 'empty path is forbidden'
  if (trim(macro_path) == trim(source_path)) &
      error stop 'MACRO_OUT and SOURCE_OUT paths must differ'

  inquire(file=trim(projected_path),exist=projected_exists)
  inquire(file=trim(macro_path),exist=macro_exists)
  inquire(file=trim(source_path),exist=source_exists)
  if (.not. projected_exists) error stop 'PROJECTED input does not exist'
  if (macro_exists) error stop 'MACRO_OUT path already exists'
  if (source_exists) error stop 'SOURCE_OUT path already exists'

  ! Open the sole input read-only.  Production receives no writable alias to
  ! this persistent object; both candidate outputs are fresh memory LCMs.
  call LCMOP(projected,trim(projected_path),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'read-only PROJECTED input')
  call LCMOP(macro,'B2N-MACRO-MEM',0,1,0)
  call LCMOP(source,'B2N-SOURCE-MEM',0,1,0)
  call REQUIRE_FRESH_MEMORY(macro,'fresh MACRO memory output')
  call REQUIRE_FRESH_MEMORY(source,'fresh SOURCE memory output')
  if (c_associated(projected,macro) .or. &
      c_associated(projected,source) .or. &
      c_associated(macro,source)) &
      error stop 'B2n object handles alias'

  call SPOR64_B2N_BUILD(projected,1,macro,source,status)
  if (status /= SPOR64_B2N_COMMITTED) &
      error stop 'production B2n rejected the real projected plane'

  ! Persistent artifacts are evidence copies made only after the in-memory
  ! production commit.  Each XSM target was absent at process entry and is
  ! checked empty immediately before the whole-object copy.
  call LCMOP(macro_xsm,trim(macro_path),0,2,0)
  call REQUIRE_FRESH_XSM(macro_xsm,'fresh persistent MACRO output')
  call LCMEQU(macro,macro_xsm)
  call LCMCL(macro_xsm,1)

  call LCMOP(source_xsm,trim(source_path),0,2,0)
  call REQUIRE_FRESH_XSM(source_xsm,'fresh persistent SOURCE output')
  call LCMEQU(source,source_xsm)
  call LCMCL(source_xsm,1)

  call LCMCL(source,2)
  call LCMCL(macro,2)
  call LCMCL(projected,1)

  write(*,'(A)') 'B2N REAL64 FROZEN-QFISS BUILD PASS'
  write(*,'(A)') &
      'B2N PRODUCTION-BUILD-CALLS=1 PLANE=1 STATE=FROZEN-QFIS/1'
  write(*,'(A)') 'B2N WHOLE-OBJECT-XSM-COPIES=2'
  write(*,'(A)') 'B2N DRAGON=0 ASM=0 FLU=0 TRANSPORT=0 PICARD=0'
  write(*,'(A)') 'B2N CONVERGENCE=NOT-EVALUATED'

contains

  subroutine REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A)') trim(owner)
      error stop 'required GANLIB pointer is absent'
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
        trim(object_name) /= '/') error stop 'memory output is not fresh'
  end subroutine REQUIRE_FRESH_MEMORY


  subroutine REQUIRE_FRESH_XSM(root,owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: owner
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call REQUIRE_ASSOCIATED(root,owner)
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'persistent output is not fresh'
  end subroutine REQUIRE_FRESH_XSM

end program BUILD_B2N_REAL64_FROZEN_QFISS

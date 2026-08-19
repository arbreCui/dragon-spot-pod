program prepare_r64_aa1_projected
  ! Submit one independently checked AA(1) proposal to the REAL64
  ! PROJECTED lifecycle.  The production B2J proposal entry owns all
  ! private staging; this host only opens immutable inputs and a fresh
  ! output, then verifies the committed epoch.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real64
  use GANLIB
  use SPOR64_B2J, only : SPOR64_B2J_ADMISSION_FAILED, &
      SPOR64_B2J_ARCHIVE_PROJECTED, SPOR64_B2J_PROJECT_PROPOSAL
  implicit none

  integer, parameter :: nsnap = 3
  character(len=1024) :: proposal_path, archive_path, track_path, output_path
  type(c_ptr) :: proposal, archive, track, output
  type(c_ptr) :: archive_authority, output_authority
  type(c_ptr) :: fluxes, plane, plane_authority
  integer :: status, template_epoch, output_epoch, plane_epoch, ip
  integer(int64) :: expected_bits, found_bits
  real(real64) :: proposal_rho, output_rho, plane_rho
  logical :: exists

  if (command_argument_count() /= 4) call fail( &
      'EXPECTED PROPOSAL_AX CLOSED_ARCHIVE AXIAL_TRACK FRESH_OUTPUT.')
  call get_command_argument(1,proposal_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,output_path)
  if (len_trim(proposal_path) == 0 .or. len_trim(archive_path) == 0 .or. &
      len_trim(track_path) == 0 .or. len_trim(output_path) == 0) &
    call fail('EMPTY PATH.')
  if (trim(output_path) == trim(proposal_path) .or. &
      trim(output_path) == trim(archive_path) .or. &
      trim(output_path) == trim(track_path)) &
    call fail('OUTPUT MUST DIFFER FROM EVERY INPUT.')
  inquire(file=trim(output_path),exist=exists)
  if (exists) call fail('OUTPUT PATH IS NOT FRESH.')

  call LCMOP(proposal,trim(proposal_path),2,2,0)
  call LCMOP(archive,trim(archive_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call require_character(proposal,'SPOT-X-STATE','PROPOSAL','PROPOSAL AX')
  call require_character(proposal,'SPOT-X-CARR','X4-RAW-FLUX', &
      'PROPOSAL AX')
  call require_absent(proposal,'SPOT-X-EPOCH','PROPOSAL AX')
  call require_real64(proposal,'SPOT-X-RHO',proposal_rho,'PROPOSAL AX')
  archive_authority = require_directory(archive,'SPOT-R64', &
      'CLOSED TEMPLATE')
  call require_character(archive_authority,'STATE','CLOSED', &
      'CLOSED TEMPLATE AUTHORITY')
  call require_integer(archive_authority,'EPOCH',template_epoch, &
      'CLOSED TEMPLATE AUTHORITY')
  if (template_epoch < 0 .or. template_epoch == huge(template_epoch)) &
    call fail('CLOSED TEMPLATE EPOCH CANNOT ADVANCE.')

  call LCMOP(output,trim(output_path),0,2,0)
  call SPOR64_B2J_PROJECT_PROPOSAL(output,proposal,track,archive,status)
  if (status == SPOR64_B2J_ADMISSION_FAILED) &
    call fail('B2J REJECTED THE CHECKED AA1 PROPOSAL.')
  if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
    call fail('B2J RETURNED AN UNKNOWN STATUS.')

  output_authority = require_directory(output,'SPOT-R64', &
      'PROJECTED OUTPUT')
  call require_character(output_authority,'STATE','PROJECTED', &
      'PROJECTED OUTPUT AUTHORITY')
  call require_integer(output_authority,'EPOCH',output_epoch, &
      'PROJECTED OUTPUT AUTHORITY')
  call require_real64(output_authority,'RHO',output_rho, &
      'PROJECTED OUTPUT AUTHORITY')
  if (output_epoch /= template_epoch+1) &
    call fail('PROJECTED EPOCH IS NOT TEMPLATE EPOCH PLUS ONE.')
  expected_bits = transfer(proposal_rho,0_int64)
  found_bits = transfer(output_rho,0_int64)
  if (found_bits /= expected_bits) &
    call fail('PROJECTED ROOT RHO DIFFERS FROM PROPOSAL.')

  fluxes = require_list(output,'FLUX',nsnap,'PROJECTED OUTPUT')
  do ip = 1, nsnap
    plane = require_list_directory(fluxes,ip,'PROJECTED FLUX')
    plane_authority = require_directory(plane,'SPOT-R64', &
        'PROJECTED FLUX')
    call require_character(plane_authority,'STATE','PROJECTED', &
        'PROJECTED FLUX AUTHORITY')
    call require_integer(plane_authority,'EPOCH',plane_epoch, &
        'PROJECTED FLUX AUTHORITY')
    call require_real64(plane_authority,'RHO',plane_rho, &
        'PROJECTED FLUX AUTHORITY')
    if (plane_epoch /= output_epoch) &
      call fail('PROJECTED CHILD EPOCH DIFFERS FROM ROOT.')
    if (transfer(plane_rho,0_int64) /= expected_bits) &
      call fail('PROJECTED CHILD RHO DIFFERS FROM PROPOSAL.')
  end do

  call LCMCL(output,1)
  call LCMCL(track,1)
  call LCMCL(archive,1)
  call LCMCL(proposal,1)
  write(*,'(A,I0,A,I0)') 'SPOT-R64 AA1 PROPOSAL -> PROJECTED ', &
      template_epoch,' -> ',output_epoch
  write(*,'(A,I0)') 'SPOT-R64 B2J PROPOSAL COMMIT PASS STATUS=',status
  write(*,'(A)') 'SPOT-R64 AA1 PROJECT PREPARATION COMPLETE NO-TRANSPORT'

contains

  function require_directory(root,name,label) result(directory)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, label
    type(c_ptr) :: directory
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= -1 .or. type_found /= 0) &
      call fail(trim(label)//' MISSING DIRECTORY '//trim(name)//'.')
    directory = LCMGID(root,name)
    if (.not. c_associated(directory)) &
      call fail(trim(label)//' NULL DIRECTORY '//trim(name)//'.')
  end function require_directory

  function require_list(root,name,length_expected,label) result(list)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, label
    integer, intent(in) :: length_expected
    type(c_ptr) :: list
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= length_expected .or. type_found /= 10) &
      call fail(trim(label)//' INVALID LIST '//trim(name)//'.')
    list = LCMGID(root,name)
    if (.not. c_associated(list)) &
      call fail(trim(label)//' NULL LIST '//trim(name)//'.')
  end function require_list

  function require_list_directory(list,index,label) result(directory)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    character(len=*), intent(in) :: label
    type(c_ptr) :: directory
    integer :: length_found, type_found
    call LCMLEL(list,index,length_found,type_found)
    if (length_found /= -1 .or. type_found /= 0) &
      call fail(trim(label)//' ITEM IS NOT A DIRECTORY.')
    directory = LCMGIL(list,index)
    if (.not. c_associated(directory)) &
      call fail(trim(label)//' ITEM IS NULL.')
  end function require_list_directory

  subroutine require_integer(root,name,value,label)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, label
    integer, intent(out) :: value
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= 1 .or. type_found /= 1) &
      call fail(trim(label)//' INVALID INTEGER '//trim(name)//'.')
    call LCMGET(root,name,value)
  end subroutine require_integer

  subroutine require_real64(root,name,value,label)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, label
    real(real64), intent(out) :: value
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= 1 .or. type_found /= 4) &
      call fail(trim(label)//' INVALID REAL64 '//trim(name)//'.')
    call LCMGET(root,name,value)
  end subroutine require_real64

  subroutine require_character(root,name,expected,label)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected, label
    character(len=12) :: value
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= 3 .or. type_found /= 3) &
      call fail(trim(label)//' INVALID CHARACTER '//trim(name)//'.')
    value = ' '
    call LCMGTC(root,name,12,value)
    if (value /= expected) &
      call fail(trim(label)//' UNEXPECTED '//trim(name)//'.')
  end subroutine require_character

  subroutine require_absent(root,name,label)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, label
    integer :: length_found, type_found
    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(label)//' FORBIDDEN RECORD '//trim(name)//'.')
  end subroutine require_absent

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(0,'(A)') 'SPOT-R64 AA1 PROJECT ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program prepare_r64_aa1_projected

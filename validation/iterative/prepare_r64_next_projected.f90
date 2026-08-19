program prepare_r64_next_projected
  ! Advance one sealed REAL64 continuation epoch without assembly or transport.
  !
  !   prepare_r64_next_projected closed_ax.xsm closed_archive.xsm \
  !       axial_track.xsm fresh_projected_archive.xsm
  !
  ! The negative provenance test is performed on a private in-memory copy:
  ! only the archive-root epoch is changed, so production B2J must reject it
  ! and leave its private target empty.  The caller should additionally hash
  ! the three read-only input files before and after this executable.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use GANLIB
  use SPOR64_B2J, only : SPOR64_B2J_ADMISSION_FAILED, &
      SPOR64_B2J_ARCHIVE_PROJECTED, SPOR64_B2J_PROJECT_ARCHIVE
  implicit none

  integer, parameter :: nsnap = 3
  character(len=1024) :: ax_path, archive_path, track_path, output_path
  character(len=72) :: object_file
  character(len=12) :: object_name
  type(c_ptr) :: ax, archive, track, output
  type(c_ptr) :: archive_authority, output_authority
  type(c_ptr) :: fluxes, plane, plane_authority
  type(c_ptr) :: bad_archive, bad_output, bad_authority
  integer :: ax_epoch, archive_epoch, projected_epoch, plane_epoch
  integer :: bad_epoch, status, ip, object_length
  logical :: exists, empty, memory_backed

  if (command_argument_count() /= 4) call fail( &
      'EXPECTED CLOSED_AX CLOSED_ARCHIVE AXIAL_TRACK FRESH_OUTPUT.')
  call get_command_argument(1,ax_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,output_path)
  if (len_trim(ax_path) == 0 .or. len_trim(archive_path) == 0 .or. &
      len_trim(track_path) == 0 .or. len_trim(output_path) == 0) &
    call fail('EMPTY PATH.')
  if (trim(output_path) == trim(ax_path) .or. &
      trim(output_path) == trim(archive_path) .or. &
      trim(output_path) == trim(track_path)) &
    call fail('OUTPUT MUST DIFFER FROM EVERY INPUT.')
  inquire(file=trim(output_path),exist=exists)
  if (exists) call fail('OUTPUT PATH IS NOT FRESH.')

  ! Mode 2 opens every physical input read-only.
  call LCMOP(ax,trim(ax_path),2,2,0)
  call LCMOP(archive,trim(archive_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call require_character(ax,'SPOT-X-STATE','CLOSED','AX')
  call require_integer(ax,'SPOT-X-EPOCH',ax_epoch,'AX')
  archive_authority = require_directory(archive,'SPOT-R64','ARCHIVE')
  call require_character(archive_authority,'STATE','CLOSED', &
      'ARCHIVE AUTHORITY')
  call require_integer(archive_authority,'EPOCH',archive_epoch, &
      'ARCHIVE AUTHORITY')
  if (archive_epoch /= ax_epoch) &
    call fail('CLOSED INPUT EPOCHS DO NOT MATCH.')
  if (ax_epoch < 0 .or. ax_epoch == huge(ax_epoch)) &
    call fail('CLOSED INPUT EPOCH CANNOT ADVANCE.')
  projected_epoch = ax_epoch+1

  ! Negative test: one inconsistent root epoch is the only mutation, and it
  ! occurs in memory.  B2J must reject before opening any output record.
  call LCMOP(bad_archive,'B2J-BAD-IN',0,1,0)
  call LCMEQU(archive,bad_archive)
  bad_authority = require_directory(bad_archive,'SPOT-R64', &
      'PRIVATE BAD ARCHIVE')
  bad_epoch = archive_epoch+1
  call LCMPUT(bad_authority,'EPOCH',1,1,bad_epoch)
  call LCMOP(bad_output,'B2J-BAD-OUT',0,1,0)
  call SPOR64_B2J_PROJECT_ARCHIVE(bad_output,ax,track,bad_archive,status)
  if (status /= SPOR64_B2J_ADMISSION_FAILED) &
    call fail('B2J ACCEPTED THE MISMATCHED ARCHIVE EPOCH.')
  call LCMINF(bad_output,object_file,object_name,empty,object_length, &
      memory_backed)
  if (.not. empty .or. object_length /= -1 .or. &
      trim(object_name) /= '/') &
    call fail('REJECTED NEGATIVE OUTPUT WAS MUTATED.')
  call LCMCL(bad_output,2)
  call LCMCL(bad_archive,2)

  ! Positive test and the only caller-visible output mutation.
  call LCMOP(output,trim(output_path),0,2,0)
  call SPOR64_B2J_PROJECT_ARCHIVE(output,ax,track,archive,status)
  if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
    call fail('B2J REJECTED THE VALID CLOSED EPOCH.')
  output_authority = require_directory(output,'SPOT-R64', &
      'PROJECTED ARCHIVE')
  call require_character(output_authority,'STATE','PROJECTED', &
      'PROJECTED ARCHIVE AUTHORITY')
  call require_integer(output_authority,'EPOCH',archive_epoch, &
      'PROJECTED ARCHIVE AUTHORITY')
  if (archive_epoch /= projected_epoch) &
    call fail('PROJECTED ROOT EPOCH IS NOT INPUT EPOCH PLUS ONE.')
  fluxes = require_list(output,'FLUX',nsnap,'PROJECTED ARCHIVE')
  do ip = 1, nsnap
    plane = require_list_directory(fluxes,ip,'PROJECTED FLUX')
    plane_authority = require_directory(plane,'SPOT-R64', &
        'PROJECTED FLUX')
    call require_character(plane_authority,'STATE','PROJECTED', &
        'PROJECTED FLUX AUTHORITY')
    call require_integer(plane_authority,'EPOCH',plane_epoch, &
        'PROJECTED FLUX AUTHORITY')
    if (plane_epoch /= projected_epoch) &
      call fail('PROJECTED CHILD EPOCH DOES NOT MATCH ROOT.')
  end do

  ! Re-read both lifecycle inputs after production B2J returns.  File hashes
  ! remain an independent shell-level check of their complete byte content.
  call require_character(ax,'SPOT-X-STATE','CLOSED','AX AFTER B2J')
  call require_integer(ax,'SPOT-X-EPOCH',archive_epoch,'AX AFTER B2J')
  if (archive_epoch /= ax_epoch) call fail('B2J MUTATED AX EPOCH.')
  archive_authority = require_directory(archive,'SPOT-R64', &
      'ARCHIVE AFTER B2J')
  call require_character(archive_authority,'STATE','CLOSED', &
      'ARCHIVE AUTHORITY AFTER B2J')
  call require_integer(archive_authority,'EPOCH',archive_epoch, &
      'ARCHIVE AUTHORITY AFTER B2J')
  if (archive_epoch /= ax_epoch) call fail('B2J MUTATED ARCHIVE EPOCH.')

  call LCMCL(output,1)
  call LCMCL(track,1)
  call LCMCL(archive,1)
  call LCMCL(ax,1)
  write(*,'(A,I0,A,I0)') 'SPOT-R64 B2J CLOSED/',ax_epoch, &
      ' -> PROJECTED/',projected_epoch
  write(*,'(A)') &
      'SPOT-R64 B2J NEGATIVE EPOCH-MISMATCH REJECTED OUTPUT-EMPTY'
  write(*,'(A)') 'SPOT-R64 B2J PROJECT PREPARATION COMPLETE NO-TRANSPORT'

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


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'SPOT-R64 B2J PREPARE ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program prepare_r64_next_projected

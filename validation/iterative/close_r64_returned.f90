program close_r64_returned
  ! One production axial-feedback RETURNED/e -> CLOSED/e commit into two
  ! fresh outputs.  Radial RETURNED admission is a separate pre-axial gate;
  ! the feedback input here already contains SPOT-ITER-K/SPOT-L1-ERR from
  ! SPOLEAK and is therefore admitted by SPOR64_B2W_CLOSE itself.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use GANLIB
  use SPOR64_B2W, only : SPOR64_B2W_CLOSED, SPOR64_B2W_CLOSE
  implicit none

  character(len=1024) :: ax_path, archive_path, ax_out_path, archive_out_path
  type(c_ptr) :: ax, archive, ax_out, archive_out
  type(c_ptr) :: input_authority, output_authority
  integer :: close_status
  integer :: input_epoch, ax_epoch, archive_epoch
  character(len=12) :: marker
  logical :: exists

  if (command_argument_count() /= 4) &
    error stop 'expected candidate AX/archive and two fresh output paths'
  call get_command_argument(1,ax_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,ax_out_path)
  call get_command_argument(4,archive_out_path)
  inquire(file=trim(ax_out_path),exist=exists)
  if (exists) error stop 'closed AX output already exists'
  inquire(file=trim(archive_out_path),exist=exists)
  if (exists) error stop 'closed archive output already exists'

  call LCMOP(ax,trim(ax_path),2,2,0)
  call LCMOP(archive,trim(archive_path),2,2,0)
  input_authority = LCMGID(archive,'SPOT-R64')
  if (.not. c_associated(input_authority)) &
    error stop 'returned archive authority is missing'
  call LCMGTC(input_authority,'STATE',12,marker)
  if (marker /= 'RETURNED') error stop 'returned state expected'
  call LCMGET(input_authority,'EPOCH',input_epoch)

  call LCMOP(ax_out,trim(ax_out_path),0,2,0)
  call LCMOP(archive_out,trim(archive_out_path),0,2,0)
  call SPOR64_B2W_CLOSE(ax_out,archive_out,ax,archive,close_status)
  if (close_status /= SPOR64_B2W_CLOSED) &
    error stop 'B2W rejected the rank-two feedback pair'

  call LCMGTC(ax_out,'SPOT-X-STATE',12,marker)
  if (marker /= 'CLOSED') error stop 'closed AX marker differs'
  call LCMGET(ax_out,'SPOT-X-EPOCH',ax_epoch)
  output_authority = LCMGID(archive_out,'SPOT-R64')
  if (.not. c_associated(output_authority)) &
    error stop 'closed archive authority is missing'
  call LCMGTC(output_authority,'STATE',12,marker)
  if (marker /= 'CLOSED') error stop 'closed archive marker differs'
  call LCMGET(output_authority,'EPOCH',archive_epoch)
  if (ax_epoch /= input_epoch .or. archive_epoch /= input_epoch) &
    error stop 'closed outputs changed the returned epoch'

  write(*,'(A,I0)') 'SPOT-R64 B2W CLOSE PASS STATUS=',close_status
  write(*,'(A,I0,A)') 'SPOT-R64 CLOSED/',input_epoch, &
      ' COMPLETE NO-TRANSPORT'

  call LCMCL(archive_out,1)
  call LCMCL(ax_out,1)
  call LCMCL(archive,1)
  call LCMCL(ax,1)
end program close_r64_returned

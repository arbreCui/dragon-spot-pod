program b2i_seal_bootstrap
  ! Seal the initial CLOSED/0 bootstrap pair from a freshly minted
  ! canonical axial state and its leakage-carrying snapshot archive.
  ! This is the lifecycle genesis commit: every later map continues the
  ! chain through B2J projection and B2W close.  Fail-closed: any
  ! admission defect leaves the two fresh outputs untouched.
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB
  use SPOR64_B2I, only : SPOR64_B2I_BOOTSTRAP_COMMITTED, &
      SPOR64_B2I_SEAL_BOOTSTRAP
  implicit none

  character(len=1024) :: ax_path, track_path, archive_path
  character(len=1024) :: contract_path
  character(len=1024) :: ax_out_path, archive_out_path
  type(c_ptr) :: ax, track, archive, ax_out, archive_out
  type(c_ptr) :: ax_mem, archive_mem, contract
  integer :: status
  logical :: exists

  if (command_argument_count() /= 6) error stop &
    'expected seed AX, axial track, archive, sealed route contract '// &
    'and two fresh output paths'
  call get_command_argument(1,ax_path)
  call get_command_argument(2,track_path)
  call get_command_argument(3,archive_path)
  call get_command_argument(4,contract_path)
  call get_command_argument(5,ax_out_path)
  call get_command_argument(6,archive_out_path)
  inquire(file=trim(ax_out_path),exist=exists)
  if (exists) error stop 'bootstrap AX output already exists'
  inquire(file=trim(archive_out_path),exist=exists)
  if (exists) error stop 'bootstrap archive output already exists'

  call LCMOP(ax,trim(ax_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call LCMOP(archive,trim(archive_path),2,2,0)
  call LCMOP(contract,trim(contract_path),2,2,0)
  ! B2I seals only into fresh in-memory roots (EMPTY_MEMORY_ROOT); the
  ! sealed pair is then exported record-for-record to the two XSM files.
  call LCMOP(ax_mem,'AXBOOT',0,1,0)
  call LCMOP(archive_mem,'ARBOOT',0,1,0)

  call SPOR64_B2I_SEAL_BOOTSTRAP(ax_mem,archive_mem,ax,track,archive, &
      contract,status)
  if (status /= SPOR64_B2I_BOOTSTRAP_COMMITTED) then
    write(6,'(A,I0)') 'SPOT-R64 B2I STATUS ', status
    error stop 'B2I refused the bootstrap pair'
  endif

  call LCMOP(ax_out,trim(ax_out_path),0,2,0)
  call LCMOP(archive_out,trim(archive_out_path),0,2,0)
  call LCMEQU(ax_mem,ax_out)
  call LCMEQU(archive_mem,archive_out)
  call LCMCL(ax_out,1)
  call LCMCL(archive_out,1)
  call LCMCL(ax_mem,2)
  call LCMCL(archive_mem,2)
  call LCMCL(contract,1)
  call LCMCL(archive,1)
  call LCMCL(track,1)
  call LCMCL(ax,1)
  write(6,'(A)') 'SPOT-R64 B2I BOOTSTRAP COMMITTED CLOSED/0'

end program b2i_seal_bootstrap

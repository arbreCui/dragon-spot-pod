program admit_candidate_radial
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB
  use SPOR64_B2W, only : SPOR64_B2W_RETURNED_ADMITTED, &
      SPOR64_B2W_ADMIT_RETURNED
  implicit none

  character(len=1024) :: path, contract_path
  type(c_ptr) :: archive, contract
  integer :: status

  if (command_argument_count() /= 2) error stop &
    'expected RETURNED archive path and sealed route contract path'
  call get_command_argument(1,path)
  call get_command_argument(2,contract_path)
  call LCMOP(archive,trim(path),2,2,0)
  call LCMOP(contract,trim(contract_path),2,2,0)
  call SPOR64_B2W_ADMIT_RETURNED(archive,contract,status)
  if (status /= SPOR64_B2W_RETURNED_ADMITTED) &
    error stop 'B2W rejected RETURNED archive'
  write(*,'(A,I0)') 'H2-X2 R64 RETURNED PRODUCTION-ADMISSION PASS STATUS=', &
    status
  call LCMCL(contract,1)
  call LCMCL(archive,1)
end program admit_candidate_radial

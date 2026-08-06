program B2E_STRIP_LEGACY_SOURCE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  implicit none

  type(c_ptr) :: root
  character(len=1024) :: path
  character(len=12) :: signature
  integer :: length, record_type

  if (command_argument_count() /= 1) error stop 'expected one fixture path'
  call get_command_argument(1,path)
  call LCMOP(root,trim(path),1,2,0)
  call LCMGTC(root,'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') error stop 'fixture is not L_FLUX'
  call LCMLEN(root,'SOUR',length,record_type)
  if (length /= 370 .or. record_type /= 10) &
    error stop 'expected one legacy SOUR collision'
  call LCMLEN(root,'SPOT-R64',length,record_type)
  if (length /= 0 .or. record_type /= 99) &
    error stop 'fixture already has REAL64 authority'
  call LCMDEL(root,'SOUR')
  call LCMLEN(root,'SOUR',length,record_type)
  if (length /= 0 .or. record_type /= 99) &
    error stop 'temporary SOUR removal failed'
  call LCMCL(root,1)
  write(*,'(A)') 'B2E TEMPORARY STRUCTURAL FIXTURE PASS'
end program B2E_STRIP_LEGACY_SOURCE

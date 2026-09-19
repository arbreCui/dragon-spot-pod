program make_route_contract
  ! Generate one sealed route-contract XSM from the case DECLARATION.
  ! The values come from the command line (the same declaration the
  ! case's decks carry), never from any object under admission, so the
  ! contract cannot be self-certified.  The lane's input manifest then
  ! hash-seals the produced file.
  !
  !   make_route_contract <out.xsm> <case-name> \
  !     <eps_radial> <eps_axial> <eps_mccg> \
  !     <maxout> <maxinr> <acce_free> <acce_accel> <option>
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32
  use GANLIB
  implicit none

  type(c_ptr) :: out
  character(len=1024) :: path, arg
  character(len=12) :: name12, sig12
  character(len=4) :: option4
  real(real32) :: eps32(3)
  integer :: caps(2), acce(2), i, ios
  logical :: exists

  if (command_argument_count() /= 10) error stop &
    'expected out case-name eps_radial eps_axial eps_mccg '// &
    'maxout maxinr acce_free acce_accel option'
  call get_command_argument(1,path)
  inquire(file=trim(path),exist=exists)
  if (exists) error stop 'contract output already exists'
  call get_command_argument(2,arg)
  if (len_trim(arg) == 0 .or. len_trim(arg) > 12) &
    error stop 'case name must be 1..12 characters'
  name12 = arg(1:12)
  do i = 1, 3
    call get_command_argument(i+2,arg)
    read(arg,*,iostat=ios) eps32(i)
    if (ios /= 0) error stop 'terminal tolerances must be reals'
    if (.not. ieee_is_finite(eps32(i)) .or. eps32(i) <= 0.0_real32) &
      error stop 'terminal tolerances must be finite and positive'
  end do
  do i = 1, 2
    call get_command_argument(i+5,arg)
    read(arg,*,iostat=ios) caps(i)
    if (ios /= 0 .or. caps(i) <= 0) error stop 'caps must be positive'
  end do
  do i = 1, 2
    call get_command_argument(i+7,arg)
    read(arg,*,iostat=ios) acce(i)
    if (ios /= 0 .or. acce(i) < 0) error stop 'acce must be nonnegative'
  end do
  call get_command_argument(10,arg)
  if (len_trim(arg) == 0 .or. len_trim(arg) > 4) &
    error stop 'option must be 1..4 characters'
  option4 = arg(1:4)

  call LCMOP(out,trim(path),0,2,0)
  sig12 = 'L_RCONTRACT'
  call LCMPTC(out,'SIGNATURE',12,sig12)
  call LCMPTC(out,'CASE-NAME',12,name12)
  call LCMPUT(out,'EPS-TERMINAL',3,2,eps32)
  call LCMPUT(out,'FLU-CAPS',2,1,caps)
  call LCMPUT(out,'FLU-ACCE',2,1,acce)
  call LCMPTC(out,'FLU-OPTION',4,option4)
  call LCMCL(out,1)

  write(6,'(A,A)') 'ROUTE CONTRACT SEALED: ', trim(path)
  write(6,'(A,A)') '  CASE-NAME    ', name12
  write(6,'(A,3ES15.7)') '  EPS-TERMINAL', eps32
  write(6,'(A,2I8)') '  FLU-CAPS    ', caps
  write(6,'(A,2I8)') '  FLU-ACCE    ', acce
  write(6,'(A,A)') '  FLU-OPTION   ', option4
end program make_route_contract

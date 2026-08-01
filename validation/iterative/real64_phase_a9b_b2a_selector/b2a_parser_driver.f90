module B2A_TOKEN_STREAM
  implicit none
  integer, parameter :: MAX_TOKENS = 24
  integer :: token_count = 0, token_position = 0
  integer :: token_type(MAX_TOKENS) = 0
  integer :: token_integer(MAX_TOKENS) = 0
  real :: token_real(MAX_TOKENS) = 0.0
  character(len=4) :: token_character(MAX_TOKENS) = ' '

contains

  subroutine RESET_STREAM()
    token_count = 0
    token_position = 0
    token_type = 0
    token_integer = 0
    token_real = 0.0
    token_character = ' '
  end subroutine RESET_STREAM

  subroutine ADD_CHARACTER(value)
    character(len=*), intent(in) :: value
    token_count = token_count + 1
    token_type(token_count) = 3
    token_character(token_count) = value
  end subroutine ADD_CHARACTER

  subroutine ADD_INTEGER(value)
    integer, intent(in) :: value
    token_count = token_count + 1
    token_type(token_count) = 1
    token_integer(token_count) = value
  end subroutine ADD_INTEGER

  subroutine LOAD_CASE(name)
    character(len=*), intent(in) :: name

    call RESET_STREAM()
    select case (trim(name))
    case ('default', 'rec_clean')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER(';')
    case ('r64')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER(';')
    case ('moca')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('MOCA')
      call ADD_INTEGER(1)
      call ADD_CHARACTER(';')
    case ('moca_r64')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('MOCA')
      call ADD_INTEGER(1)
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER(';')
    case ('r64_moca')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('MOCA')
      call ADD_INTEGER(2)
      call ADD_CHARACTER(';')
    case ('rec_hete')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('K')
      call ADD_CHARACTER('B0')
      call ADD_CHARACTER('HETE')
      call ADD_INTEGER(2)
      call ADD_INTEGER(1)
      call ADD_CHARACTER(';')
    case ('rec_r64_hete')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('K')
      call ADD_CHARACTER('B0')
      call ADD_CHARACTER('HETE')
      call ADD_INTEGER(2)
      call ADD_INTEGER(1)
      call ADD_CHARACTER(';')
    case ('duplicate')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('R64')
    case ('parameter')
      call ADD_CHARACTER('R64')
      call ADD_INTEGER(1)
    case ('bogus')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('BOGU')
    case default
      error stop 'unknown parser case'
    end select
  end subroutine LOAD_CASE

end module B2A_TOKEN_STREAM

subroutine REDGET(item_type, integer_value, real_value, character_value, &
                  double_value)
  use B2A_TOKEN_STREAM
  implicit none
  integer, intent(out) :: item_type, integer_value
  real, intent(out) :: real_value
  character(len=*), intent(out) :: character_value
  double precision, intent(out) :: double_value

  token_position = token_position + 1
  if (token_position > token_count) then
    item_type = 10
    integer_value = 0
    real_value = 0.0
    character_value = ' '
    double_value = 0.0d0
    return
  end if
  item_type = token_type(token_position)
  integer_value = token_integer(token_position)
  real_value = token_real(token_position)
  character_value = token_character(token_position)
  double_value = dble(real_value)
end subroutine REDGET

subroutine XABORT(message)
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  character(len=*), intent(in) :: message
  write (error_unit, '(A)') 'B2A-XABORT '//trim(message)
  flush (error_unit)
  error stop 86
end subroutine XABORT

program B2A_PARSER_DRIVER
  use, intrinsic :: iso_c_binding, only : c_null_ptr
  use B2A_TOKEN_STREAM, only : LOAD_CASE
  implicit none
  character(len=32) :: scenario

  call get_command_argument(1, scenario)
  select case (trim(scenario))
  case ('default')
    call RUN_CASE('default', .false., .false., .true., 0)
  case ('r64')
    call RUN_CASE('r64', .false., .true., .true., 0)
  case ('moca')
    call RUN_CASE('moca', .false., .false., .true., 1)
  case ('moca_r64')
    call RUN_CASE('moca_r64', .false., .true., .true., 1)
  case ('r64_moca')
    call RUN_CASE('r64_moca', .false., .true., .true., 2)
  case ('lifetime')
    call RUN_CASE('r64', .false., .true., .true., 0)
    call RUN_CASE('default', .false., .false., .true., 0)
  case ('rec_clean')
    call RUN_CASE('rec_clean', .true., .false., .false., 0)
  case ('rec_hete')
    call RUN_CASE('rec_hete', .true., .false., .true., 0)
  case ('rec_r64_hete')
    call RUN_CASE('rec_r64_hete', .true., .true., .true., 0)
  case ('duplicate', 'parameter', 'bogus')
    call RUN_CASE(trim(scenario), .false., .false., .true., 0)
    error stop 'negative parser case unexpectedly returned'
  case default
    error stop 'parser scenario expected'
  end select

contains

  subroutine RUN_CASE(name, rec, expected_r64, expected_limerg, &
                      expected_moca)
    character(len=*), intent(in) :: name
    logical, intent(in) :: rec, expected_r64, expected_limerg
    integer, intent(in) :: expected_moca
    integer :: itypec, maxout, maxinr, irebal, ifritr, iacitr, ileak
    integer :: ngroup, nregio, nmat, nifiss, itpij, iprint
    integer :: initfl, nmerg, imerg(2), ipick, imcaud
    real :: epsout, epsunk, epsinr, b2(4)
    double precision :: refkef
    character(len=4) :: coptio
    logical :: limerg, lr64, leaksw

    call LOAD_CASE(name)
    leaksw = .false.
    ngroup = 2
    nregio = 2
    nmat = 2
    nifiss = 1
    itpij = 1
    iprint = 0
    call FLUGPI(c_null_ptr, c_null_ptr, itypec, maxout, maxinr, &
      epsout, epsunk, epsinr, irebal, ifritr, iacitr, coptio, ileak, &
      b2, ngroup, nregio, nmat, nifiss, leaksw, refkef, itpij, &
      iprint, rec, initfl, nmerg, &
      imerg, ipick, imcaud, limerg, lr64)
    if (lr64 .neqv. expected_r64) error stop 'LR64 mismatch'
    if (limerg .neqv. expected_limerg) error stop 'LIMERG mismatch'
    if (imcaud /= expected_moca) error stop 'IMCAUD mismatch'
    if (itypec < 0) error stop 'ITYPEC mismatch'
    if ((name == 'rec_hete') .or. (name == 'rec_r64_hete')) then
      if (any(imerg /= [2, 1])) error stop 'IMERG staging mismatch'
      if (nmerg /= 2) error stop 'NMERG staging mismatch'
    end if
    write (*, '(A,1X,A,1X,L1,1X,L1,1X,I0)') &
      'B2A-PARSER-PASS', trim(name), lr64, limerg, imcaud
  end subroutine RUN_CASE

end program B2A_PARSER_DRIVER

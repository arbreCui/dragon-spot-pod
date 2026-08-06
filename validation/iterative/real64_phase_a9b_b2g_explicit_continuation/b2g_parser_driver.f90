module B2G_TOKEN_STREAM
  implicit none
  integer, parameter :: MAX_TOKENS=24
  integer :: token_count=0, token_position=0
  integer :: token_type(MAX_TOKENS)=0
  integer :: token_integer(MAX_TOKENS)=0
  real :: token_real(MAX_TOKENS)=0.0
  character(len=4) :: token_character(MAX_TOKENS)=' '
contains
  subroutine RESET_STREAM()
    token_count=0
    token_position=0
    token_type=0
    token_integer=0
    token_real=0.0
    token_character=' '
  end subroutine RESET_STREAM

  subroutine ADD_CHARACTER(value)
    character(len=*), intent(in) :: value
    if (token_count >= MAX_TOKENS) error stop 'token stream overflow'
    token_count=token_count+1
    token_type(token_count)=3
    token_character(token_count)=value
  end subroutine ADD_CHARACTER

  subroutine ADD_INTEGER(value)
    integer, intent(in) :: value
    if (token_count >= MAX_TOKENS) error stop 'token stream overflow'
    token_count=token_count+1
    token_type(token_count)=1
    token_integer(token_count)=value
  end subroutine ADD_INTEGER

  subroutine LOAD_CASE(name)
    character(len=*), intent(in) :: name

    call RESET_STREAM()
    select case(trim(name))
    case('off','rec_off')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER(';')
    case('boot')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('BOOT')
      call ADD_CHARACTER(';')
    case('cont')
      call ADD_CHARACTER('TYPE')
      call ADD_CHARACTER('S')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('CONT')
      call ADD_CHARACTER(';')
    case('bare')
      call ADD_CHARACTER('R64')
    case('integer')
      call ADD_CHARACTER('R64')
      call ADD_INTEGER(1)
    case('unknown')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('NOPE')
    case('duplicate')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('BOOT')
      call ADD_CHARACTER('R64')
      call ADD_CHARACTER('CONT')
    case('isolated_boot')
      call ADD_CHARACTER('BOOT')
    case('isolated_cont')
      call ADD_CHARACTER('CONT')
    case default
      error stop 'unknown parser case'
    end select
  end subroutine LOAD_CASE
end module B2G_TOKEN_STREAM


subroutine REDGET(item_type,integer_value,real_value,character_value, &
                  double_value)
  use B2G_TOKEN_STREAM
  implicit none
  integer, intent(out) :: item_type, integer_value
  real, intent(out) :: real_value
  character(len=*), intent(out) :: character_value
  double precision, intent(out) :: double_value

  token_position=token_position+1
  if (token_position > token_count) then
    item_type=10
    integer_value=0
    real_value=0.0
    character_value=' '
    double_value=0.0d0
    return
  end if
  item_type=token_type(token_position)
  integer_value=token_integer(token_position)
  real_value=token_real(token_position)
  character_value=token_character(token_position)
  double_value=dble(real_value)
end subroutine REDGET


subroutine XABORT(message)
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  character(len=*), intent(in) :: message

  write(error_unit,'(A)') 'B2G-XABORT '//trim(message)
  flush(error_unit)
  error stop 87
end subroutine XABORT


program B2G_PARSER_DRIVER
  use, intrinsic :: iso_c_binding, only : c_null_ptr
  use B2G_TOKEN_STREAM, only : LOAD_CASE
  implicit none
  character(len=32) :: scenario

  call get_command_argument(1,scenario)
  select case(trim(scenario))
  case('off')
    call RUN_CASE('off',.false.,0,.true.)
  case('boot')
    call RUN_CASE('boot',.false.,1,.true.)
  case('cont')
    call RUN_CASE('cont',.false.,2,.true.)
  case('reset')
    call RUN_CASE('boot',.false.,1,.true.)
    call RUN_CASE('off',.false.,0,.true.)
  case('rec_reset')
    call RUN_CASE('cont',.false.,2,.true.)
    call RUN_CASE('rec_off',.true.,0,.false.)
  case('bare','integer','unknown','duplicate','isolated_boot','isolated_cont')
    call RUN_CASE(trim(scenario),.false.,0,.true.)
    error stop 'negative parser case unexpectedly returned'
  case default
    error stop 'parser scenario expected'
  end select
contains
  subroutine RUN_CASE(name,rec,expected_mode,expected_limerg)
    character(len=*), intent(in) :: name
    logical, intent(in) :: rec, expected_limerg
    integer, intent(in) :: expected_mode
    integer :: itypec, maxout, maxinr, irebal, ifritr, iacitr, ileak
    integer :: ngroup, nregio, nmat, nifiss, itpij, iprint
    integer :: initfl, nmerg, imerg(2), ipick, imcaud, ir64md
    real :: epsout, epsunk, epsinr, b2(4)
    double precision :: refkef
    character(len=4) :: coptio
    logical :: limerg, leaksw

    call LOAD_CASE(name)
    leaksw=.false.
    ngroup=2
    nregio=2
    nmat=2
    nifiss=1
    itpij=1
    iprint=0
    call FLUGPI(c_null_ptr,c_null_ptr,itypec,maxout,maxinr, &
      epsout,epsunk,epsinr,irebal,ifritr,iacitr,coptio,ileak, &
      b2,ngroup,nregio,nmat,nifiss,leaksw,refkef,itpij, &
      iprint,rec,initfl,nmerg,imerg,ipick,imcaud,limerg,ir64md)
    if (ir64md /= expected_mode) error stop 'IR64MD mismatch'
    if (limerg .neqv. expected_limerg) error stop 'LIMERG mismatch'
    if (imcaud /= 0) error stop 'IMCAUD mismatch'
    if (itypec < 0) error stop 'ITYPEC mismatch'
    write(*,'(A,1X,A,1X,I0,1X,L1)') &
      'B2G-PARSER-PASS',trim(name),ir64md,limerg
  end subroutine RUN_CASE
end program B2G_PARSER_DRIVER
